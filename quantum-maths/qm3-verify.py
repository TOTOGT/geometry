#!/usr/bin/env python3
"""qm3-verify.py — Chapter QM3: the Fourier transform and phase estimation.

Standard library only. The QFT is built two ways — as the explicit matrix and
as a circuit of Hadamards, controlled phases and swaps simulated on a state
vector — and the two are compared. Phase estimation is simulated on the
explicit amplitude vector and compared with its closed-form distribution.

  [1] The QFT matrix F_N[j][k] = exp(2 pi i jk/N)/sqrt(N) is unitary, N = 2..64.
  [2] The circuit (H on each qubit, controlled R_k phases, final bit reversal)
      equals the matrix on every basis state, n = 1..7 qubits.
  [3] F_2^n over Z_2^n IS the n-fold Hadamard: the group the Deutsch-Jozsa and
      Bernstein-Vazirani circuits transform over (chapter in book7).
  [4] F diagonalises the cyclic shift: F S F^dagger = diag(omega^k).
  [5] Phase estimation, dyadic: for eigenphase phi = m/2^t the output is |m>
      with probability 1 (t = 2..9, all m).
  [6] Phase estimation, general: the simulated outcome distribution equals
      sin^2(pi 2^t d) / (2^(2t) sin^2(pi d)) with d = phi - m/2^t; and the
      best t-bit estimate occurs with probability >= 4/pi^2 (random phi).
  [7] Continued fractions recover a rational phase p/q from a t-bit estimate
      with 2^-t <= 1/(2 q^2): over every p/q, q <= 40, t = 2*ceil(log2 q)+1.
  [8] Controls (each must FAIL): omitting the bit reversal; using F instead of
      F^dagger in the inverse step; a non-dyadic phase NOT returning one
      outcome with probability 1.

    python3 quantum-maths/qm3-verify.py
"""
import cmath, math, random, sys
from fractions import Fraction

random.seed(20261002)
FAIL = []
def check(ok, msg):
    print(("    PASS  " if ok else "    FAIL  ") + msg)
    if not ok: FAIL.append(msg)
def head(n, t):
    print('\n' + '=' * 68 + '\n  [%s]  %s\n' % (n, t) + '=' * 68)

TOL = 1e-10
def qft_matrix(N, sign=1):
    r = 1 / math.sqrt(N)
    return [[r * cmath.exp(sign * 2j * math.pi * j * k / N) for k in range(N)] for j in range(N)]
def mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def dag(A): return [[A[j][i].conjugate() for j in range(len(A))] for i in range(len(A[0]))]
def dist(A, B): return max(abs(a - b) for r, s in zip(A, B) for a, b in zip(r, s))
def eye(n): return [[1 + 0j if i == j else 0j for j in range(n)] for i in range(n)]
def mv(A, v): return [sum(A[i][j] * v[j] for j in range(len(v))) for i in range(len(A))]

head(1, 'the QFT matrix is unitary')
worst = max(dist(mm(dag(qft_matrix(N)), qft_matrix(N)), eye(N)) for N in range(2, 65))
check(worst < TOL, 'F^dagger F = I for N = 2..64 (worst %.1e)' % worst)

# ---- circuit simulation on an n-qubit state vector (qubit 0 = most significant)
def apply_1q(state, n, q, G):
    out = state[:]; step = 1 << (n - 1 - q)
    for i in range(1 << n):
        if not i & step:
            a, b = state[i], state[i | step]
            out[i] = G[0][0] * a + G[0][1] * b
            out[i | step] = G[1][0] * a + G[1][1] * b
    return out
def apply_cphase(state, n, c, t, theta):
    out = state[:]; sc, st = 1 << (n - 1 - c), 1 << (n - 1 - t)
    for i in range(1 << n):
        if i & sc and i & st: out[i] *= cmath.exp(1j * theta)
    return out
def bit_reverse(state, n):
    out = [0j] * len(state)
    for i in range(len(state)):
        j = int(format(i, '0%db' % n)[::-1], 2); out[j] = state[i]
    return out
Hm = [[1 / math.sqrt(2) + 0j, 1 / math.sqrt(2) + 0j], [1 / math.sqrt(2) + 0j, -1 / math.sqrt(2) + 0j]]
def qft_circuit(state, n, reverse=True, inverse=False):
    sgn = -1 if inverse else 1
    ops = []
    for q in range(n):
        ops.append(('h', q))
        for k in range(q + 1, n): ops.append(('cp', k, q, sgn * 2 * math.pi / (1 << (k - q + 1))))
    if inverse: ops = ops[::-1]
    s = state
    if inverse and reverse: s = bit_reverse(s, n)
    for op in ops:
        s = apply_1q(s, n, op[1], Hm) if op[0] == 'h' else apply_cphase(s, n, op[1], op[2], op[3])
    if (not inverse) and reverse: s = bit_reverse(s, n)
    return s

head(2, 'the circuit equals the matrix')
worst = 0.0
for n in range(1, 8):
    N = 1 << n; F = qft_matrix(N)
    for j in range(N):
        e = [0j] * N; e[j] = 1 + 0j
        col = qft_circuit(e, n)
        worst = max(worst, max(abs(col[k] - F[k][j]) for k in range(N)))
check(worst < TOL, 'circuit = F_N on every basis state, n = 1..7 (worst %.1e)' % worst)
rnd = [complex(random.gauss(0, 1), random.gauss(0, 1)) for _ in range(32)]
nr = math.sqrt(sum(abs(x) ** 2 for x in rnd)); rnd = [x / nr for x in rnd]
back = qft_circuit(qft_circuit(rnd, 5), 5, inverse=True)
check(max(abs(a - b) for a, b in zip(back, rnd)) < TOL, 'the inverse circuit undoes it on a random 5-qubit state')

head(3, 'F over Z_2^n is the n-fold Hadamard')
def had_n(n):
    H1 = [[1, 1], [1, -1]]; M = [[1]]
    for _ in range(n):
        M = [[a * b for a in row for b in r] for row in M for r in H1]
    return [[x / math.sqrt(1 << n) + 0j for x in row] for row in M]
def wht_char(n):
    N = 1 << n
    return [[(-1) ** bin(j & k).count('1') / math.sqrt(N) + 0j for k in range(N)] for j in range(N)]
check(all(dist(had_n(n), wht_char(n)) < TOL for n in range(1, 7)), 'H^(x)n equals the Z_2^n character table / sqrt(2^n), n = 1..6')

head(4, 'F diagonalises the cyclic shift')
worst = 0.0
for N in (4, 8, 16, 32):
    S = [[1 + 0j if i == (j + 1) % N else 0j for j in range(N)] for i in range(N)]
    D = mm(mm(qft_matrix(N, -1), S), qft_matrix(N, +1))          # F^dagger S F
    om = [cmath.exp(2j * math.pi * k / N) for k in range(N)]
    exp1 = [[om[k] if i == k else 0j for k in range(N)] for i in range(N)]
    exp2 = [[om[k].conjugate() if i == k else 0j for k in range(N)] for i in range(N)]
    worst = max(worst, min(dist(D, exp1), dist(D, exp2)))
check(worst < TOL, 'F^dagger S F is diagonal with the N-th roots of unity, N = 4, 8, 16, 32 (worst %.1e)' % worst)

def pe_distribution(t, phi):
    """simulate: (1/sqrt T) sum_k e^{2 pi i k phi}|k>, then inverse QFT; return probabilities"""
    T = 1 << t
    state = [cmath.exp(2j * math.pi * k * phi) / math.sqrt(T) for k in range(T)]
    out = mv(qft_matrix(T, -1), state)
    return [abs(a) ** 2 for a in out]

head(5, 'phase estimation, dyadic phases')
ok = True
for t in range(2, 8):
    for m in range(1 << t):
        p = pe_distribution(t, m / (1 << t))
        if abs(p[m] - 1) > 1e-9: ok = False
check(ok, 'phi = m/2^t gives |m> with probability 1, t = 2..7, every m')

head(6, 'phase estimation, general phases')
worst = 0.0; minbest = 1.0
for _ in range(40):
    t = random.choice([3, 4, 5, 6]); phi = random.random(); T = 1 << t
    p = pe_distribution(t, phi)
    for m in range(T):
        d = phi - m / T
        denom = (T ** 2) * math.sin(math.pi * d) ** 2
        f = (math.sin(math.pi * T * d) ** 2 / denom) if abs(math.sin(math.pi * d)) > 1e-12 else 1.0
        worst = max(worst, abs(p[m] - f))
    best = round(phi * T) % T
    minbest = min(minbest, p[best])
check(worst < 1e-9, 'simulated distribution = sin^2(pi T d)/(T^2 sin^2(pi d)), 40 random (t, phi) (worst %.1e)' % worst)
check(minbest >= 4 / math.pi ** 2 - 1e-9, 'the nearest t-bit estimate has probability >= 4/pi^2 = %.4f (min seen %.4f)' % (4 / math.pi ** 2, minbest))

head(7, 'continued fractions recover p/q')
def cf_best(x, qmax):
    """best rational approximation to Fraction x with denominator <= qmax via convergents"""
    a = []; num, den = x.numerator, x.denominator
    while den:
        a.append(num // den); num, den = den, num % den
    h0, h1, k0, k1 = 0, 1, 1, 0; best = Fraction(a[0])
    for ai in a:
        h0, h1 = h1, ai * h1 + h0
        k0, k1 = k1, ai * k1 + k0
        if k1 > qmax: break
        best = Fraction(h1, k1)
    return best
bad = []
for q in range(2, 41):
    t = 2 * math.ceil(math.log2(q)) + 1; T = 1 << t
    for p in range(0, q):
        if math.gcd(p, q) != 1 and not (p == 0 and q == 1): continue
        m = round(Fraction(p, q) * T)                         # the t-bit estimate
        if cf_best(Fraction(m, T), q) != Fraction(p, q): bad.append((p, q, t))
check(not bad, 'every reduced p/q with q <= 40 is recovered from its t-bit estimate (t = 2 ceil(log2 q) + 1)%s' % ('' if not bad else ' (failures: %s)' % bad[:4]))

head(8, 'controls')
n = 4; N = 16; F = qft_matrix(N); worst_nr = 0.0
for j in range(N):
    e = [0j] * N; e[j] = 1 + 0j
    col = qft_circuit(e, n, reverse=False)
    worst_nr = max(worst_nr, max(abs(col[k] - F[k][j]) for k in range(N)))
check(worst_nr > 0.1, 'without the bit reversal the circuit does not equal the matrix')
p_wrong = [abs(a) ** 2 for a in mv(qft_matrix(16, +1), [cmath.exp(2j * math.pi * k * 3 / 16) / 4 for k in range(16)])]
check(p_wrong[3] < 1e-9 and abs(p_wrong[13] - 1) < 1e-9, 'using F instead of F^dagger returns |-3 mod 16> = |13>, not |3>: it reads the phase backwards')
p_nd = pe_distribution(5, 0.3)
check(max(p_nd) < 0.99, 'a non-dyadic phase does not give one outcome with probability 1 (max %.4f)' % max(p_nd))

print()
if FAIL:
    print('FAILED: %d check(s)' % len(FAIL)); sys.exit(1)
print('all checks passed'); sys.exit(0)
