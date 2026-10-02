#!/usr/bin/env python3
"""qm2-verify.py — Chapter QM2: measurement, entanglement, CHSH and Tsirelson.

Standard library only. Everything is computed from explicit state vectors and
explicit observables (matrices), never from the closed form -cos(a-b) alone.

  [1] Born rule: for projective measurement in an orthonormal basis the
      probabilities are nonnegative and sum to 1; the post-measurement state
      is the normalised projection; measuring twice repeats the result.
  [2] Expectation <psi|A|psi> of Pauli observables; Z and X cannot both be
      sharp: variance(Z) + variance(X) >= 1/2... checked as the Robertson
      bound  Var(A) Var(B) >= |<[A,B]>|^2 / 4  on random states.
  [3] Schmidt decomposition of a two-qubit state = singular values of its
      2x2 coefficient matrix; entropy of the singlet is exactly 1 bit; of a
      product state 0.
  [4] The singlet correlator: <A(a) (x) B(b)> = -cos(a - b), from the explicit
      state and explicit observables cos(a) Z + sin(a) X, for a grid of angles.
  [5] CHSH, local: all 16 deterministic assignments A0,A1,B0,B1 in {+1,-1}
      give |S| <= 2 (exhaustive) — hence every mixture does.
  [6] CHSH, quantum: at a = 0, a' = pi/2, b = -pi/4... the singlet gives
      |S| = 2 sqrt 2 exactly (to 1e-12), and NO angle choice on a fine grid
      exceeds it.
  [7] Tsirelson, algebraically: for ANY observables A0, A1, B0, B1 with square
      identity, S^2 = 4 I - [A0,A1] (x) [B0,B1], so ||S|| <= 2 sqrt 2 because
      ||[A,A']|| <= 2. The operator identity is checked on random observables
      and the operator norm of S on random ones never exceeds 2 sqrt 2.
  [8] Controls (each must FAIL): the correlator -cos(a-b) replaced by
      -cos(2(a-b)) breaks the singlet match; the product state gives S <= 2;
      a non-involutory 'observable' breaks the S^2 identity.

    python3 quantum-maths/qm2-verify.py
"""
import cmath, itertools, math, os, random, re, subprocess, sys

random.seed(20261002)
FAIL = []
def check(ok, msg):
    print(("    PASS  " if ok else "    FAIL  ") + msg)
    if not ok: FAIL.append(msg)
def head(n, t):
    print('\n' + '=' * 68 + '\n  [%s]  %s\n' % (n, t) + '=' * 68)

TOL = 1e-12
def mm(A, B):
    n, m, p = len(A), len(B), len(B[0])
    return [[sum(A[i][k] * B[k][j] for k in range(m)) for j in range(p)] for i in range(n)]
def dag(A): return [[A[j][i].conjugate() for j in range(len(A))] for i in range(len(A[0]))]
def madd(A, B): return [[a + b for a, b in zip(r, s)] for r, s in zip(A, B)]
def msub(A, B): return [[a - b for a, b in zip(r, s)] for r, s in zip(A, B)]
def msc(c, A): return [[c * a for a in r] for r in A]
def eye(n): return [[1 + 0j if i == j else 0j for j in range(n)] for i in range(n)]
def dist(A, B): return max(abs(a - b) for r, s in zip(A, B) for a, b in zip(r, s))
def kron(A, B):
    return [[A[i][j] * B[k][l] for j in range(len(A[0])) for l in range(len(B[0]))]
            for i in range(len(A)) for k in range(len(B))]
def mv(A, v): return [sum(A[i][j] * v[j] for j in range(len(v))) for i in range(len(A))]
def ip(u, v): return sum(a.conjugate() * b for a, b in zip(u, v))
def nrm(v): return math.sqrt(sum(abs(a) ** 2 for a in v))
def expval(A, v): return ip(v, mv(A, v)).real
def opnorm(A, iters=400):
    """spectral norm by power iteration on A^dagger A"""
    n = len(A); M = mm(dag(A), A)
    v = [complex(random.gauss(0, 1), random.gauss(0, 1)) for _ in range(n)]
    for _ in range(iters):
        w = mv(M, v); r = nrm(w); v = [x / r for x in w]
    return math.sqrt(ip(v, mv(M, v)).real)

s2 = 1 / math.sqrt(2)
I2 = eye(2)
X = [[0j, 1 + 0j], [1 + 0j, 0j]]; Y = [[0j, -1j], [1j, 0j]]; Z = [[1 + 0j, 0j], [0j, -1 + 0j]]
def obs(a): return madd(msc(math.cos(a), Z), msc(math.sin(a), X))     # real-plane observable
singlet = [0j, s2 + 0j, -s2 + 0j, 0j]
def rand_state(n):
    v = [complex(random.gauss(0, 1), random.gauss(0, 1)) for _ in range(n)]
    r = nrm(v); return [x / r for x in v]

head(1, 'Born rule and collapse')
worst = 0.0; rep = 0.0
for _ in range(100):
    psi = rand_state(4)
    # random orthonormal basis by Gram-Schmidt
    basis = []
    for _ in range(4):
        w = rand_state(4)
        for b in basis:
            c = ip(b, w); w = [x - c * y for x, y in zip(w, b)]
        r = nrm(w); basis.append([x / r for x in w])
    p = [abs(ip(b, psi)) ** 2 for b in basis]
    worst = max(worst, abs(sum(p) - 1))
    # collapse onto outcome 0, then measure again
    proj = [ip(basis[0], psi) * x for x in basis[0]]; r = nrm(proj)
    post = [x / r for x in proj]
    rep = max(rep, abs(abs(ip(basis[0], post)) ** 2 - 1))
check(worst < TOL, 'probabilities in a random orthonormal basis sum to 1 (worst %.1e)' % worst)
check(rep < TOL, 'a repeated measurement returns the same outcome with probability 1 (worst %.1e)' % rep)

head(2, 'expectations and the Robertson uncertainty bound')
worst = 1.0
for _ in range(500):
    psi = rand_state(2)
    A, B = Z, X
    ea, eb = expval(A, psi), expval(B, psi)
    va, vb = 1 - ea ** 2, 1 - eb ** 2                    # A^2 = B^2 = I
    comm = msub(mm(A, B), mm(B, A))
    rhs = abs(ip(psi, mv(comm, psi))) ** 2 / 4
    worst = min(worst, va * vb - rhs)
check(worst > -TOL, 'Var(Z) Var(X) >= |<[Z,X]>|^2/4 on 500 random states (min slack %.1e)' % worst)

head(3, 'Schmidt decomposition and entanglement entropy')
def schmidt(psi):
    a, b, c, d = psi
    M = [[a, b], [c, d]]
    G = mm(M, dag(M))                                    # 2x2 Hermitian
    tr = (G[0][0] + G[1][1]).real; det = (G[0][0] * G[1][1] - G[0][1] * G[1][0]).real
    disc = math.sqrt(max(tr * tr / 4 - det, 0))
    return [max(tr / 2 + disc, 0), max(tr / 2 - disc, 0)]  # squared Schmidt coefficients
def entropy(ev): return -sum(x * math.log2(x) for x in ev if x > 1e-15)
check(abs(entropy(schmidt(singlet)) - 1) < 1e-12, 'the singlet has entanglement entropy exactly 1 bit')
pa, pb = rand_state(2), rand_state(2)
prod = [x * y for x in pa for y in pb]
check(entropy(schmidt(prod)) < 1e-9, 'a product state has entropy 0')
worst = 0.0
for _ in range(100):
    ev = schmidt(rand_state(4)); worst = max(worst, abs(sum(ev) - 1))
check(worst < 1e-12, 'squared Schmidt coefficients sum to 1 on random 2-qubit states')

head(4, 'singlet correlator: <A(a) (x) B(b)> = -cos(a - b)')
worst = 0.0
for i in range(0, 25):
    for j in range(0, 25):
        a, b = i * math.pi / 12, j * math.pi / 12
        e = ip(singlet, mv(kron(obs(a), obs(b)), singlet)).real
        worst = max(worst, abs(e + math.cos(a - b)))
check(worst < TOL, 'on a 25x25 angle grid, from explicit matrices (worst %.1e)' % worst)

head(5, 'CHSH, local deterministic: |S| <= 2, exhaustively')
mx = 0
for A0, A1, B0, B1 in itertools.product((1, -1), repeat=4):
    mx = max(mx, abs(A0 * B0 + A0 * B1 + A1 * B0 - A1 * B1))
check(mx == 2, 'all 16 assignments: max |S| = %d' % mx)

head(6, 'CHSH, quantum: 2 sqrt 2 is reached and not exceeded')
def S_val(a0, a1, b0, b1):
    E = lambda a, b: ip(singlet, mv(kron(obs(a), obs(b)), singlet)).real
    return E(a0, b0) + E(a0, b1) + E(a1, b0) - E(a1, b1)
best = S_val(0, math.pi / 2, math.pi / 4, -math.pi / 4)
check(abs(abs(best) - 2 * math.sqrt(2)) < TOL, '|S| = %.15f at (0, pi/2, pi/4, -pi/4); 2 sqrt 2 = %.15f' % (abs(best), 2 * math.sqrt(2)))
top = 0.0; step = math.pi / 8
for i in range(16):
    for j in range(16):
        for k in range(16):
            for m in range(16):
                top = max(top, abs(S_val(i * step, j * step, k * step, m * step)))
check(top < 2 * math.sqrt(2) + 1e-12, '16^4 angle choices: max |S| = %.12f <= 2 sqrt 2' % top)
check(top > 2.8, 'and the grid does reach the quantum value (the bound is not vacuous)')

head(7, 'Tsirelson: S^2 = 4I - [A0,A1] (x) [B0,B1], so ||S|| <= 2 sqrt 2')
def rand_obs(n):
    """random Hermitian unitary (involution): reflect through a random subspace"""
    v = rand_state(n); P = [[v[i] * v[j].conjugate() for j in range(n)] for i in range(n)]
    return msub(msc(2, P), eye(n))
worst = 0.0; topnorm = 0.0
for _ in range(60):
    n = 2
    A0, A1, B0, B1 = rand_obs(n), rand_obs(n), rand_obs(n), rand_obs(n)
    S = madd(madd(kron(A0, B0), kron(A0, B1)), msub(kron(A1, B0), kron(A1, B1)))
    comm = lambda P, Q: msub(mm(P, Q), mm(Q, P))
    rhs = msub(msc(4, eye(n * n)), kron(comm(A0, A1), comm(B0, B1)))
    worst = max(worst, dist(mm(S, S), rhs))
    topnorm = max(topnorm, opnorm(S))
check(worst < 1e-10, 'S^2 = 4I - [A0,A1](x)[B0,B1] on 60 random observable quadruples (worst %.1e)' % worst)
check(topnorm <= 2 * math.sqrt(2) + 1e-9, 'spectral norm of S never exceeds 2 sqrt 2 (max %.6f)' % topnorm)

head(8, 'controls')
bad = max(abs(ip(singlet, mv(kron(obs(i * math.pi / 12), obs(j * math.pi / 12)), singlet)).real + math.cos(2 * (i - j) * math.pi / 12))
          for i in range(25) for j in range(25))
check(bad > 0.5, 'replacing -cos(a-b) by -cos(2(a-b)) fails against the explicit singlet')
def S_prod(a0, a1, b0, b1, st):
    E = lambda a, b: ip(st, mv(kron(obs(a), obs(b)), st)).real
    return E(a0, b0) + E(a0, b1) + E(a1, b0) - E(a1, b1)
topp = max(abs(S_prod(i * step, j * step, k * step, m * step, prod)) for i in range(8) for j in range(8) for k in range(8) for m in range(8))
check(topp <= 2 + 1e-9, 'a product state on the same grid stays within the local bound: max |S| = %.6f' % topp)
NI = [[1 + 0j, 1 + 0j], [0j, 1 + 0j]]                       # NI^2 != I (the earlier [[1,1],[0,-1]] squares to I: it is a non-Hermitian involution, and the identity needs only A^2 = I)
S_bad = madd(madd(kron(NI, X), kron(NI, Z)), msub(kron(X, X), kron(X, Z)))
comm = lambda P, Q: msub(mm(P, Q), mm(Q, P))
rhs_bad = msub(msc(4, eye(4)), kron(comm(NI, X), comm(X, Z)))
check(dist(mm(S_bad, S_bad), rhs_bad) > 0.1, 'with a non-involutory A0 the S^2 identity fails')

head(9, 'the CHSH game and no-signalling boxes: win probability (1+eps)/2, S = 4 eps')
# Game: referee sends x, y in {0,1}; Alice answers a, Bob answers b; they win iff a xor b = x AND y.
def win_prob(P):
    return sum(0.25 * P[(a, b, x, y)] for x in (0, 1) for y in (0, 1) for a in (0, 1) for b in (0, 1) if (a ^ b) == (x & y))
def corr(P, x, y):
    return sum((-1) ** (a ^ b) * P[(a, b, x, y)] for a in (0, 1) for b in (0, 1))
def S_of(P): return corr(P, 0, 0) + corr(P, 0, 1) + corr(P, 1, 0) - corr(P, 1, 1)
def no_signalling(P):
    # P(a | x, y) must not depend on y; P(b | x, y) must not depend on x.
    w = 0.0
    for x in (0, 1):
        for a in (0, 1):
            w = max(w, abs(sum(P[(a, b, x, 0)] for b in (0, 1)) - sum(P[(a, b, x, 1)] for b in (0, 1))))
    for y in (0, 1):
        for b in (0, 1):
            w = max(w, abs(sum(P[(a, b, 0, y)] for a in (0, 1)) - sum(P[(a, b, 1, y)] for a in (0, 1))))
    return w
def box(eps):
    return {(a, b, x, y): 0.5 * ((1 + eps) / 2 if (a ^ b) == (x & y) else (1 - eps) / 2)
            for a in (0, 1) for b in (0, 1) for x in (0, 1) for y in (0, 1)}
def normalised(P):
    return max(abs(sum(P[(a, b, x, y)] for a in (0, 1) for b in (0, 1)) - 1) for x in (0, 1) for y in (0, 1))
worst_ns = worst_w = worst_S = worst_n = 0.0
for i in range(0, 101):
    e = i / 100
    P = box(e)
    worst_ns = max(worst_ns, no_signalling(P)); worst_n = max(worst_n, normalised(P))
    worst_w = max(worst_w, abs(win_prob(P) - (1 + e) / 2)); worst_S = max(worst_S, abs(S_of(P) - 4 * e))
check(worst_ns < 1e-12 and worst_n < 1e-12, 'the box family is a no-signalling distribution for every eps in [0,1] (worst %.1e)' % worst_ns)
check(worst_w < 1e-12, 'win probability = (1+eps)/2 on 101 values of eps (worst %.1e)' % worst_w)
check(worst_S < 1e-12, 'S = 4 eps on 101 values of eps (worst %.1e)' % worst_S)
check(abs(win_prob(box(1.0)) - 1) < 1e-15 and abs(S_of(box(1.0)) - 4) < 1e-15, 'eps = 1 is the Popescu-Rohrlich box: wins always, S = 4')
check(abs(win_prob(box(0.0)) - 0.5) < 1e-15, 'eps = 0 is the uniformly random box: wins half the time')

# Local deterministic strategies: a = f(x), b = g(y), 16 of them; every local model is a mixture, so the maximum is at a vertex.
strategies = list(itertools.product((0, 1), repeat=4))          # (f0, f1, g0, g1)
def det_P(st):
    f0, f1, g0, g1 = st
    return {(a, b, x, y): 1.0 if (a == (f0, f1)[x] and b == (g0, g1)[y]) else 0.0
            for a in (0, 1) for b in (0, 1) for x in (0, 1) for y in (0, 1)}
wins = [win_prob(det_P(st)) for st in strategies]
check(abs(max(wins) - 0.75) < 1e-15 and sum(1 for w in wins if abs(w - 0.75) < 1e-15) == 8, 'deterministic strategies: best win probability 3/4, reached by exactly 8 of the 16')
check(max(abs(S_of(det_P(st))) for st in strategies) == 2, 'deterministic strategies: |S| <= 2, reached')
best = [st for st, w in zip(strategies, wins) if abs(w - 0.75) < 1e-15]
mix = {k: sum(det_P(st)[k] for st in best) / len(best) for k in box(0).keys()}
dm = max(abs(mix[k] - box(0.5)[k]) for k in mix)
check(dm < 1e-15, 'the uniform mixture of the 8 best deterministic strategies IS the eps = 1/2 box (diff %.1e)' % dm)
check(all(abs(win_prob(box(e)) - (1 + e) / 2) < 1e-12 and (1 + e) / 2 > 0.75 for e in (0.51, 0.6, 0.9)), 'eps > 1/2 wins above 3/4, hence lies outside every mixture of local strategies')

# Quantum: explicit singlet probabilities from projectors (I +- A)/2 (x) (I +- B)/2
def quantum_box(a0, a1, b0, b1, st, bob_sign):
    A = (obs(a0), obs(a1)); B = (msc(bob_sign, obs(b0)), msc(bob_sign, obs(b1)))
    P = {}
    for x in (0, 1):
        for y in (0, 1):
            for a in (0, 1):
                for b in (0, 1):
                    Pa = msc(0.5, madd(eye(2), msc((-1) ** a, A[x])))
                    Pb = msc(0.5, madd(eye(2), msc((-1) ** b, B[y])))
                    P[(a, b, x, y)] = ip(st, mv(kron(Pa, Pb), st)).real
    return P
Q = quantum_box(0, math.pi / 2, math.pi / 4, -math.pi / 4, singlet, -1)
check(no_signalling(Q) < 1e-12 and normalised(Q) < 1e-12, 'the singlet box is no-signalling (worst %.1e)' % no_signalling(Q))
check(abs(win_prob(Q) - math.cos(math.pi / 8) ** 2) < 1e-12, 'quantum win probability = cos^2(pi/8) = %.10f' % win_prob(Q))
check(abs(win_prob(Q) - (0.5 + S_of(Q) / 8)) < 1e-12, 'win = 1/2 + S/8 on the singlet box (S = %.10f)' % S_of(Q))
eps_q = 2 * win_prob(Q) - 1
check(abs(eps_q - 1 / math.sqrt(2)) < 1e-12, 'the quantum box is the eps = 1/sqrt 2 member in its win probability (eps = %.10f)' % eps_q)
check(0.5 < eps_q < 1, 'strictly between the local boundary 1/2 and the PR box 1')
Qc = quantum_box(0, math.pi / 2, math.pi / 4, -math.pi / 4, singlet, -1)
dev = max(abs(Qc[k] - box(eps_q)[k]) for k in Qc)
check(dev < 1e-12, 'on this singlet box every probability equals the eps = 1/sqrt 2 box entry (diff %.1e)' % dev)

head(10, 'controls for the game section')
sig = {(a, b, x, y): (0.5 if a == y else 0.0) for a in (0, 1) for b in (0, 1) for x in (0, 1) for y in (0, 1)}   # a = y, b uniform: Bob's input reaches Alice
check(no_signalling(sig) > 0.1, 'a box where Alice\'s output equals Bob\'s input signals, and the (corrected) no-signalling check sees it (%.2f)' % no_signalling(sig))
wrong = quantum_box(0, math.pi / 2, math.pi / 4, -math.pi / 4, singlet, +1)
check(abs(win_prob(wrong) - math.cos(math.pi / 8) ** 2) > 0.1, 'with Bob\'s observables left un-negated the singlet wins only %.4f, so the sign convention in the check is not decoration' % win_prob(wrong))
check(abs(win_prob(box(0.5)) - 0.75) < 1e-15 and not abs(win_prob(box(0.5)) - 0.5 - 1 / (2 * math.sqrt(2))) < 1e-3, 'the local boundary and the quantum value are different numbers')

head(12, "Cirel'son 1980, Theorem 1: correlations are inner products of unit vectors (condition (4) -> (3))")
Yp = [[0j, -1j], [1j, 0j]]
def jw_gammas(d):
    q = (d + 1) // 2
    gs = []
    for j in range(q):
        for P in (X, Yp):
            M = [[1 + 0j]]
            for t in range(q):
                F = Z if t < j else (P if t == j else eye(2))
                M = kron(M, F)
            gs.append(M)
    return gs[:d]
def transpose(M): return [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]
def rand_unit(d):
    v = [random.gauss(0, 1) for _ in range(d)]
    n = math.sqrt(sum(a * a for a in v)); return [a / n for a in v]
def lin(vec, mats):
    out = msc(vec[0], mats[0])
    for c, M in zip(vec[1:], mats[1:]): out = madd(out, msc(c, M))
    return out
random.seed(5)
worst = 0.0
for (m, n) in [(2, 2), (3, 3), (2, 3), (4, 3)]:
    d = m + n
    G = jw_gammas(d); D = len(G[0])
    anti = max(dist(madd(mm(G[i], G[j]), mm(G[j], G[i])), msc(2, eye(D)) if i == j else msc(0, eye(D))) for i in range(d) for j in range(d))
    check(anti < 1e-12, 'm=%d n=%d: the %d Jordan-Wigner generators are Hermitian-involution-anticommuting (worst %.1e), Hilbert space dim %d' % (m, n, d, anti, D))
    phi = [0j] * (D * D)
    for i in range(D): phi[i * D + i] = 1 / math.sqrt(D)
    xs = [rand_unit(d) for _ in range(m)]; ys = [rand_unit(d) for _ in range(n)]
    sq = 0.0; gap = 0.0
    for xk in xs:
        A = lin(xk, G); sq = max(sq, dist(mm(A, A), eye(D)))
        for yl in ys:
            B = transpose(lin(yl, G)); sq = max(sq, dist(mm(B, B), eye(D)))
            c = ip(phi, mv(kron(A, B), phi))
            gap = max(gap, abs(c - sum(a * b for a, b in zip(xk, yl))))
    worst = max(worst, gap)
    check(sq < 1e-12, 'm=%d n=%d: every A_k and B_l squares to the identity (worst %.1e)' % (m, n, sq))
    check(gap < 1e-12, 'm=%d n=%d: <Phi| A_k (x) B_l |Phi> = <x_k, y_l> for all %d pairs (worst gap %.1e)' % (m, n, m * n, gap))
# the same objects at the CHSH vectors: the maximum of <x1,y1>+<x1,y2>+<x2,y1>-<x2,y2> over unit vectors is 2 sqrt 2, over signs it is 2
best_vec = 0.0
for _ in range(20000):
    x1, x2, y1, y2 = [rand_unit(4) for _ in range(4)]
    dp = lambda u, v: sum(a * b for a, b in zip(u, v))
    best_vec = max(best_vec, dp(x1, y1) + dp(x1, y2) + dp(x2, y1) - dp(x2, y2))
check(best_vec <= 2 * math.sqrt(2) + 1e-12 and best_vec > 2.5, 'random unit vectors in R^4: CHSH combination never exceeds 2 sqrt 2 (max seen %.4f)' % best_vec)
sx = math.sqrt(0.5)
x1, x2, y1, y2 = [1, 0], [0, 1], [sx, sx], [sx, -sx]
vv = sum(a * b for a, b in zip(x1, y1)) + sum(a * b for a, b in zip(x1, y2)) + sum(a * b for a, b in zip(x2, y1)) - sum(a * b for a, b in zip(x2, y2))
check(abs(vv - 2 * math.sqrt(2)) < 1e-12, 'unit vectors in R^2 (0, 90, 45, -45 degrees) attain exactly 2 sqrt 2 = %.12f' % vv)
check(max(abs(a0 * (b0 + b1) + a1 * (b0 - b1)) for a0 in (-1, 1) for a1 in (-1, 1) for b0 in (-1, 1) for b1 in (-1, 1)) == 2, 'one-dimensional unit vectors (signs): maximum is 2, ratio sqrt 2 between the two thresholds')

head(13, "Cirel'son 1980, p. 95: the sum-of-squares identity behind S <= 2 sqrt 2")
def rand_herm(n):
    M = [[complex(random.gauss(0, 1), random.gauss(0, 1)) for _ in range(n)] for _ in range(n)]
    return msc(0.5, madd(M, dag(M)))
r2 = math.sqrt(2); kk = (r2 - 1) / 8
def sos_gap(coefs=None, shape=None):
    n = 3
    a1, a2, b1, b2 = rand_herm(n), rand_herm(n), rand_herm(n), rand_herm(n)
    I3 = eye(n)
    A1, A2 = kron(a1, I3), kron(a2, I3); B1, B2 = kron(I3, b1), kron(I3, b2)
    lhs = msub(madd(madd(mm(A1, B1), mm(A1, B2)), mm(A2, B1)), mm(A2, B2))
    sq = lambda M: mm(M, M)
    u = r2 + 1
    t1 = madd(msc(u, msub(A1, B1)), msub(A2, B2))
    t2 = msub(msc(u, msub(A1, B2)), madd(A2, B1))
    t3 = madd(msc(u, msub(A2, B1)), madd(A1, B2))
    t4 = msub(msc(u, madd(A2, B2)), madd(A1, B1))
    ssum = madd(madd(sq(A1), sq(A2)), madd(sq(B1), sq(B2)))
    rhs = msc(1 / r2, ssum)
    for t in (t1, t2, t3, t4): rhs = msub(rhs, msc(kk, sq(t)))
    return dist(lhs, rhs)
g = max(sos_gap() for _ in range(25))
check(g < 1e-9, 'A1B1+A1B2+A2B1-A2B2 = (1/sqrt2)(A1^2+A2^2+B1^2+B2^2) - ((sqrt2-1)/8) * sum of four squares, on 25 random Hermitian 9x9 quadruples with [A,B]=0 (worst %.1e)' % g)
# control: change one coefficient and the identity must fail
_k = kk
kk = kk * 1.1
gbad = max(sos_gap() for _ in range(5)); kk = _k
check(gbad > 1e-3, 'control: scaling the (sqrt2-1)/8 coefficient by 1.1 breaks the identity (gap %.2f)' % gbad)
# (the step from the identity to S <= 2 sqrt 2 is the inequality A^2, B^2 <= I plus positivity of squares; it is not a numerical check and is not counted as one)

head(14, 'the sourcing, against the CHSH paper and Wehner in ~/Downloads')
def _pdf(names):
    path = next((q for n in names for q in (os.path.expanduser('~/Downloads/' + n), os.path.expanduser('~/mnt/Downloads/' + n)) if os.path.exists(q)), None)
    if not path: return None
    try:
        o = subprocess.run(['pdftotext', '-layout', path, '-'], capture_output=True, text=True, timeout=120)
        if o.returncode == 0 and o.stdout:
            return re.sub(r'\s+', ' ', o.stdout.replace('\ufb01', 'fi').replace('\ufb02', 'fl').replace('\u2019', "'"))
    except Exception:
        pass
    return None
ctxt = _pdf(['VOLUME 23, NUMBER 15 PHYSI CA I. REVIEW I.ETTERS.pdf'])
if ctxt is None:
    print('    SKIP  the CHSH paper is not available; none of that sourcing is checked')
else:
    for label, needle in [('title', 'PROPOSED EXPERIMENT TO TEST LOCAL HIDDEN-VARIABLE THEORIES'), ('date', '13 OcToBER 1969'), ('volume', 'VOLUME 23, NUMBER 15')]:
        check(needle in ctxt, 'CHSH paper records: ' + label)
wtxt = _pdf(['Tsirelson bounds for generalized Clauser-Horne-Shimony-Holt inequalities.pdf'])
if wtxt is None:
    print('    SKIP  Wehner is not available; none of that sourcing is checked')
else:
    for label, needle in [('Tsirelson bound named', "known as Tsirelson's bound"), ('arXiv id', 'quant-ph/0510076')]:
        check(needle in wtxt, 'Wehner records: ' + label)
    check('Quantum theory' in wtxt and 'up to the value' in wtxt, 'Wehner: quantum theory violates CHSH up to a stated value (the abstract names it as Tsirelson bound)')

print()
if FAIL:
    print('FAILED: %d check(s)' % len(FAIL)); sys.exit(1)
print('all checks passed'); sys.exit(0)
