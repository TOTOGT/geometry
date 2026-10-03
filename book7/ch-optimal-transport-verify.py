#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ch-optimal-transport-verify.py -- companion to book7/ch-optimal-transport.html.

Standard library only (exact integer or Fraction arithmetic wherever possible). Checks the
elementary statements in Caffarelli's review, "The Monge-Ampere equation and optimal
transportation, an elementary review" (LNM 1813, 2003), on small finite and Gaussian examples:

  [1] discrete transport, quadratic cost: the optimal plan is cyclically monotone (no
      rearrangement of the matched pairs lowers the cost); a non-optimal plan is not
  [2] duality: a Hungarian-algorithm dual pair (u, v) has u_i + v_j <= c_ij, equality on the
      optimal matching, and sum u + sum v = the brute-force primal minimum
  [3] the c-transform: replacing v by v*(y) = min_x [c(x,y) - u(x)] keeps the pair admissible and
      never lowers v (control: replacing min by max breaks admissibility)
  [4] one dimension: the optimal plan for quadratic cost is the sorted (monotone) matching
  [5] the 1-D cost |x - y| on two separated segments: every matching has the same cost, so the optimal
      map is not unique; for the quadratic cost on the same data it is
  [6] the review's non-convex-target example: T(x) = x + sign(x) pushes [-1,1] onto [-2,-1] u [1,2]
      with Jacobian 1, is monotone, and phi(x) = |x| + x^2/2 has second derivative 1 plus a point mass at 0
  [7] Monge-Ampere in closed form: for Gaussians, g(T x) det DT = f(x) with T the optimal affine map
      (1-D and 2-D); T is the gradient of a convex quadratic; controls with a wrong map fail
  [8] sourcing against the review in ~/Downloads (SKIP if absent)

It does not prove existence, uniqueness or regularity. It checks examples.

    python3 book7/ch-optimal-transport-verify.py
"""
import itertools, math, os, random, re, subprocess, sys
from fractions import Fraction as Fr

FAIL = []
def check(ok, msg):
    print(('    PASS  ' if ok else '    FAIL  ') + msg)
    if not ok: FAIL.append(msg)
def head(n, t): print('\n' + '=' * 72 + '\n  [%s]  %s\n' % (n, t) + '=' * 72)
def norm(s): return re.sub(r'\s+', ' ', s.replace('ﬁ', 'fi').replace('ﬂ', 'fl'))

random.seed(1813)
def sq(a, b): return sum((p - q) ** 2 for p, q in zip(a, b))
def dot(a, b): return sum(p * q for p, q in zip(a, b))

def optimal(cost, n):
    best = None
    for p in itertools.permutations(range(n)):
        c = sum(cost[i][p[i]] for i in range(n))
        if best is None or c < best[0]: best = (c, p)
    return best

head(1, 'cyclical monotonicity of an optimal plan (quadratic cost, 2-D, integer points)')
n = 6
X = [(random.randint(-20, 20), random.randint(-20, 20)) for _ in range(n)]
Y = [(random.randint(-20, 20), random.randint(-20, 20)) for _ in range(n)]
C = [[sq(X[i], Y[j]) for j in range(n)] for i in range(n)]
copt, popt = optimal(C, n)
def cyc_mono(perm):
    base = sum(dot(Y[perm[i]], X[i]) for i in range(n))
    return all(sum(dot(Y[perm[q[i]]], X[i]) for i in range(n)) <= base for q in itertools.permutations(range(n)))
check(cyc_mono(popt), 'the optimal plan maximises sum <y_i, x_i> over every rearrangement of its own targets (cyclical monotonicity, %d permutations)' % math.factorial(n))
worst = max(itertools.permutations(range(n)), key=lambda p: sum(C[i][p[i]] for i in range(n)))
check(not cyc_mono(worst), 'control: the worst plan is NOT cyclically monotone')

head(2, 'duality: Hungarian potentials against the brute-force minimum')
def hungarian(c):
    n = len(c); INF = float('inf')
    u = [0] * (n + 1); v = [0] * (n + 1); p = [0] * (n + 1); way = [0] * (n + 1)
    for i in range(1, n + 1):
        p[0] = i; j0 = 0; minv = [INF] * (n + 1); used = [False] * (n + 1)
        while True:
            used[j0] = True; i0 = p[j0]; delta = INF; j1 = 0
            for j in range(1, n + 1):
                if not used[j]:
                    cur = c[i0 - 1][j - 1] - u[i0] - v[j]
                    if cur < minv[j]: minv[j] = cur; way[j] = j0
                    if minv[j] < delta: delta = minv[j]; j1 = j
            for j in range(n + 1):
                if used[j]: u[p[j]] += delta; v[j] -= delta
                else: minv[j] -= delta
            j0 = j1
            if p[j0] == 0: break
        while True:
            j1 = way[j0]; p[j0] = p[j1]; j0 = j1
            if j0 == 0: break
    match = [0] * n
    for j in range(1, n + 1): match[p[j] - 1] = j - 1
    return u[1:], v[1:], match
U, V, match = hungarian(C)
check(all(U[i] + V[j] <= C[i][j] for i in range(n) for j in range(n)), 'admissible: u_i + v_j <= c_ij for all i, j')
check(all(U[i] + V[match[i]] == C[i][match[i]] for i in range(n)), 'equality u_i + v_j = c_ij on the matched pairs')
check(sum(U) + sum(V) == copt, 'strong duality: sum u + sum v = %d = the brute-force minimum' % copt)
U2 = list(U); U2[0] += 1
check(not all(U2[i] + V[j] <= C[i][j] for i in range(n) for j in range(n)), 'control: raising one u by 1 breaks admissibility')

head(3, 'the c-transform improves an admissible pair')
u0 = [min(C[i][j] - V[j] for j in range(n)) - random.randint(0, 5) for i in range(n)]     # admissible with V, then lowered
v0 = [V[j] - random.randint(0, 3) for j in range(n)]
adm = lambda a, b: all(a[i] + b[j] <= C[i][j] for i in range(n) for j in range(n))
check(adm(u0, v0), 'start from an admissible pair (u0, v0)')
vstar = [min(C[i][j] - u0[i] for i in range(n)) for j in range(n)]
check(adm(u0, vstar) and all(vstar[j] >= v0[j] for j in range(n)), 'v*(y) = min_x [c(x,y) - u(x)] is admissible and at least v0 everywhere')
vbad = [max(C[i][j] - u0[i] for i in range(n)) for j in range(n)]
check(not adm(u0, vbad), 'control: with max in place of min the pair is NOT admissible')

head(4, 'one dimension: the optimal plan is the sorted matching')
ok = True
for _ in range(40):
    m = 6
    xs = sorted(random.sample(range(-30, 30), m)); ys = random.sample(range(-30, 30), m)
    c1 = [[(x - y) ** 2 for y in ys] for x in xs]
    best, bp = optimal(c1, m)
    srt = sum((xs[i] - sorted(ys)[i]) ** 2 for i in range(m))
    ok = ok and best == srt
check(ok, 'over 40 random 6-point sets the brute-force optimum equals the sorted matching')
xs = [0, 1, 2, 3]; ys = [0, 1, 2, 3]
rev = sum((xs[i] - ys[3 - i]) ** 2 for i in range(4)); idn = sum((xs[i] - ys[i]) ** 2 for i in range(4))
check(rev > idn, 'control: the order-reversing matching costs more (%d > %d)' % (rev, idn))

head(5, 'cost |x - y| on separated segments: many optimal maps; quadratic cost: one')
A = [Fr(-2) + Fr(k, 8) for k in range(9)]; B = [Fr(1) + Fr(k, 8) for k in range(9)]
m = len(A)
cl = [[abs(x - y) for y in B] for x in A]
ok = True; vals = set()
for _ in range(200):
    p = list(range(m)); random.shuffle(p)
    vals.add(sum(cl[i][p[i]] for i in range(m)))
check(len(vals) == 1, 'all 200 random matchings of [-2,-1] onto [1,2] have the same |x - y| cost (%s)' % sorted(vals))
cq = [[(x - y) ** 2 for y in B] for x in A]
qv = set(sum(cq[i][p[i]] for i in range(m)) for p in (random.sample(range(m), m) for _ in range(200)))
check(len(qv) > 1, 'control: with the quadratic cost the matchings do NOT all cost the same')
srtq = sum(cq[i][i] for i in range(m))
check(srtq == min(qv | {srtq}), 'and the sorted matching is the cheapest of them')

head(6, "the review's example with a non-convex target")
T = lambda x: x + (1 if x > 0 else -1)
pts = [Fr(k, 50) for k in range(-50, 51) if k != 0]
check(all((-2 <= T(x) <= -1) if x < 0 else (1 <= T(x) <= 2) for x in pts), 'T maps [-1,1] into [-2,-1] u [1,2]')
check(all(T(pts[i]) <= T(pts[i + 1]) for i in range(len(pts) - 1)), 'T is monotone')
check(all(T(x + Fr(1, 1000)) - T(x) == Fr(1, 1000) for x in pts if abs(x) > Fr(1, 100)), 'the Jacobian is 1 away from 0, and f = g = 1, so g(Tx) T\'(x) = f(x) there')
h = Fr(1, 100)
second = lambda x: (abs(x + h) + (x + h) ** 2 / 2 - 2 * (abs(x) + x ** 2 / 2) + abs(x - h) + (x - h) ** 2 / 2) / h ** 2
check(second(Fr(1, 2)) == 1 and second(Fr(0)) == 1 + 2 / h, 'phi = |x| + x^2/2: second difference is 1 away from 0 and grows like 2/h at 0 (a point mass of weight 2)')
check(second(Fr(0)) != 1, 'control: at 0 the second difference is NOT the a.e. value 1')

head(7, 'Monge-Ampere for Gaussians: g(Tx) det DT = f(x)')
def gauss1(x, m, s): return math.exp(-0.5 * ((x - m) / s) ** 2) / (s * math.sqrt(2 * math.pi))
m1, s1, m2, s2 = 0.7, 1.3, -1.1, 0.6
T1 = lambda x: m2 + (s2 / s1) * (x - m1)
err = max(abs(gauss1(T1(x), m2, s2) * (s2 / s1) - gauss1(x, m1, s1)) for x in [i / 10 for i in range(-40, 41)])
check(err < 1e-14, '1-D: g(T x) T\'(x) = f(x) to %.1e at 81 points' % err)
Tbad = lambda x: m2 + 1.5 * (s2 / s1) * (x - m1)
errb = max(abs(gauss1(Tbad(x), m2, s2) * 1.5 * (s2 / s1) - gauss1(x, m1, s1)) for x in [i / 10 for i in range(-40, 41)])
check(errb > 1e-3, 'control: with the slope changed the identity fails (error %.2f)' % errb)

def mm(a, b): return [[sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def det(a): return a[0][0] * a[1][1] - a[0][1] * a[1][0]
def inv(a): d = det(a); return [[a[1][1] / d, -a[0][1] / d], [-a[1][0] / d, a[0][0] / d]]
def sqrtm(a):                      # 2x2 symmetric positive definite
    s = math.sqrt(det(a)); t = math.sqrt(a[0][0] + a[1][1] + 2 * s)
    return [[(a[0][0] + s) / t, a[0][1] / t], [a[1][0] / t, (a[1][1] + s) / t]]
S1 = [[2.0, 0.6], [0.6, 1.0]]; S2 = [[1.0, -0.3], [-0.3, 0.5]]
R = sqrtm(S1); Ri = inv(R)
A2 = mm(mm(Ri, sqrtm(mm(mm(R, S2), R))), Ri)
def g2(x, S): 
    Si = inv(S); q = sum(x[i] * Si[i][j] * x[j] for i in range(2) for j in range(2))
    return math.exp(-0.5 * q) / (2 * math.pi * math.sqrt(det(S)))
pts2 = [(a / 3, b / 3) for a in range(-6, 7) for b in range(-6, 7)]
Tx = lambda x, A: (A[0][0] * x[0] + A[0][1] * x[1], A[1][0] * x[0] + A[1][1] * x[1])
e2 = max(abs(g2(Tx(x, A2), S2) * det(A2) - g2(x, S1)) for x in pts2)
check(e2 < 1e-14, '2-D: g(Ax) det A = f(x) to %.1e on 169 points, A = S1^-1/2 (S1^1/2 S2 S1^1/2)^1/2 S1^-1/2' % e2)
check(abs(A2[0][1] - A2[1][0]) < 1e-14 and A2[0][0] > 0 and det(A2) > 0, 'A is symmetric positive definite, so T x = A x is the gradient of the convex phi(x) = x.A x / 2')
Q = [[math.cos(0.4), -math.sin(0.4)], [math.sin(0.4), math.cos(0.4)]]
Arot = mm(mm(sqrtm(S2), Q), Ri)          # S2^1/2 Q S1^-1/2 : a valid transport map for any rotation Q
e3 = max(abs(g2(Tx(x, Arot), S2) * det(Arot) - g2(x, S1)) for x in pts2)
asym = abs(Arot[0][1] - Arot[1][0])
check(e3 < 1e-14 and asym > 1e-3, 'control: S2^1/2 Q S1^-1/2 (Q a rotation) pushes the density forward just as well (error %.1e) but is NOT symmetric (asymmetry %.2f), so it is not a gradient of a convex function' % (e3, asym))

head(8, 'sourcing against the review in ~/Downloads')
_D = next((q for q in (os.path.expanduser('~/Downloads/'), os.path.expanduser('~/mnt/Downloads/')) if os.path.isdir(q)), None)
txt = None
if _D:
    for fn in os.listdir(_D):
        if 'monge-amp' in fn.lower() and fn.lower().endswith('.pdf'):
            try:
                o = subprocess.run(['pdftotext', '-layout', os.path.join(_D, fn), '-'], capture_output=True, text=True, timeout=120)
                if o.returncode == 0 and o.stdout: txt = norm(o.stdout)
            except Exception: txt = None
if txt is None:
    print('    SKIP  the review (or pdftotext) is not available; none of the sourcing below is checked')
else:
    for label, needle in [
        ('title', 'an elementary review'),
        ('LNM 1813', 'LNM 1813'),
        ('cyclical monotonicity', 'cyclical'),
        ('the convex-potential theorem is credited to Rockafellar (spelled Rockafeller there)', 'Rockafeller'),
        ('the dual problem told as a shipper', 'shipping company'),
        ('c-concave functions', 'C-concave'),
        ('Brenier', 'Brenier'),
        ('the non-convex target example', '[−2, −1] ∪ [1, 2]'),
        ('Alexandrov sense', 'Alexandrov'),
        ('the original Monge problem', 'original Monge problem'),
    ]:
        check(needle in txt, 'review: ' + label)
    check('Villani' not in txt, 'control: a name the review does not contain is not found')

print()
if FAIL:
    print('FAILED: %d check(s)' % len(FAIL)); sys.exit(1)
print('all checks passed'); sys.exit(0)
