#!/usr/bin/env python3
"""ch-frenkel-verify.py — the necessary condition for Feigin-Frenkel duality,
checked on every simple type tested, and anchored to three known values.

Verification companion to ch-frenkel.html; extends ch-feigin-verify.py, which
computes dual Coxeter numbers and Langlands duals from Cartan matrices and says
plainly that the Feigin-Frenkel isomorphism is not checked even for sl_2.

It still is not checked here. What is checked is a NECESSARY condition: if
W^k(g) is isomorphic to W^k'(^L g) with  r (k+h)(k'+h') = 1  (r = lacing
number), their Virasoro central charges must agree. With t = k + h^vee and
t' = k' + ^Lh^vee, the central charge of the W-algebra is

    c_g(t) = l - 12 |rho - t rho^vee|^2 / t           (Fateev-Lukyanov form)

and the condition is   c_g(t) = c_{^L g}(1/(r t)).

  [1] The inner product is right: |rho|^2 = h^vee dim(g) / 12  (Freudenthal-
      de Vries strange formula, long root squared = 2), every type.
  [2] Anchors that did not come from the formula: Virasoro (sl_2) at t = p/q
      gives 1/2 (Ising, 3/4), 7/10 (tricritical Ising, 4/5), 0 (2/3);
      W_3 (sl_3) at t = 4/5 gives 4/5 (three-state Potts).
  [3] Duality condition c_g(t) = c_Lg(1/(r t)) for all types, many t.
  [4] At the self-dual point t = 1, c = rank.
  [5] Controls — must FAIL: the wrong dual level (t' = 1/t) for non-simply-
      laced types; g and ^Lg do NOT have equal c at the SAME t.

    python3 book7/ch-frenkel-verify.py
"""
import sys
from fractions import Fraction as F

FAIL = []
def check(ok, msg):
    print(("    PASS  " if ok else "    FAIL  ") + msg)
    if not ok: FAIL.append(msg)
def head(n, t):
    print('\n' + '=' * 68 + '\n  [%s]  %s\n' % (n, t) + '=' * 68)

# ---- root-system code, same conventions as ch-feigin-verify.py ------------
def cartan(t, n):
    A = [[F(0)] * n for _ in range(n)]
    for i in range(n): A[i][i] = F(2)
    if t in 'ABC':
        for i in range(n - 1): A[i][i + 1] = A[i + 1][i] = F(-1)
        if t == 'B' and n > 1: A[n - 1][n - 2] = F(-2)
        if t == 'C' and n > 1: A[n - 2][n - 1] = F(-2)
    elif t == 'D':
        for i in range(n - 2): A[i][i + 1] = A[i + 1][i] = F(-1)
        A[n - 3][n - 1] = A[n - 1][n - 3] = F(-1)
    elif t == 'G': A = [[F(2), F(-1)], [F(-3), F(2)]]
    elif t == 'F': A = [[F(2), F(-1), F(0), F(0)], [F(-1), F(2), F(-2), F(0)],
                        [F(0), F(-1), F(2), F(-1)], [F(0), F(0), F(-1), F(2)]]
    elif t == 'E':
        for a, b in [(1, 3), (3, 4), (4, 5), (2, 4)] + [(i, i + 1) for i in range(5, n)]:
            A[a - 1][b - 1] = A[b - 1][a - 1] = F(-1)
    return A

def transpose(A):
    n = len(A); return [[A[j][i] for j in range(n)] for i in range(n)]

def symmetrizer(A):
    """d_i with d_i A_ij = d_j A_ji, scaled so the largest is 1 (long root^2 = 2)."""
    n = len(A); d = [None] * n; d[0] = F(1); st = [0]
    while st:
        i = st.pop()
        for j in range(n):
            if i != j and A[i][j] != 0 and d[j] is None:
                d[j] = d[i] * A[j][i] / A[i][j]   # d_j = d_i A_ji / A_ij ... see assert
                st.append(j)
    # verify the defining relation instead of trusting the recurrence
    for i in range(n):
        for j in range(n):
            if d[i] * A[i][j] != d[j] * A[j][i]:
                # recurrence had the other orientation; flip
                d = [1 / x for x in d]; break
    for i in range(n):
        for j in range(n):
            assert d[i] * A[i][j] == d[j] * A[j][i], 'not symmetrizable'
    mx = max(d); return [x / mx for x in d]

def roots(A):
    n = len(A)
    simple = [tuple(1 if j == i else 0 for j in range(n)) for i in range(n)]
    R = set(simple); fr = set(simple)
    while fr:
        new = set()
        for a in fr:
            for i in range(n):
                p = sum(F(a[j]) * A[i][j] for j in range(n))
                b = list(a); b[i] -= int(p); b = tuple(b)
                if any(b) and (all(x >= 0 for x in b) or all(x <= 0 for x in b)) and b not in R:
                    new.add(b)
        R |= new; fr = new
    return R

class RS:
    def __init__(s, A):
        s.A = A; s.n = len(A); s.d = symmetrizer(A)
        s.G = [[s.d[i] * A[i][j] for j in range(s.n)] for i in range(s.n)]
        s.pos = [r for r in roots(A) if all(x >= 0 for x in r)]
    def ip(s, u, v):
        return sum(u[i] * v[j] * s.G[i][j] for i in range(s.n) for j in range(s.n))
    def rho(s):
        return [F(sum(r[i] for r in s.pos), 2) for i in range(s.n)]
    def rhov(s):
        out = [F(0)] * s.n
        for r in s.pos:
            nr = s.ip(r, r)
            for i in range(s.n): out[i] += F(r[i]) * 2 / nr
        return [x / 2 for x in out]
    def hv(s):
        th = max(s.pos, key=sum)
        return 1 + s.ip(s.rho(), th)           # h^vee = 1 + (rho, theta), theta long
    def dim(s):
        return s.n + 2 * len(s.pos)
    def lacing(s):
        return max(s.d) / min(s.d)
    def c(s, t):
        rho, rv = s.rho(), s.rhov()
        v = [rho[i] - t * rv[i] for i in range(s.n)]
        return s.n - 12 * s.ip(v, v) / t

TYPES = [('A', 1), ('A', 2), ('A', 3), ('A', 4), ('B', 2), ('B', 3), ('B', 4),
         ('C', 3), ('C', 4), ('D', 4), ('D', 5), ('E', 6), ('E', 7), ('E', 8),
         ('F', 4), ('G', 2)]
KNOWN_H = {('A',1):2,('A',2):3,('A',3):4,('A',4):5,('B',2):3,('B',3):5,('B',4):7,
           ('C',3):4,('C',4):5,('D',4):6,('D',5):8,('E',6):12,('E',7):18,
           ('E',8):30,('F',4):9,('G',2):4}
S = {ty: RS(cartan(*ty)) for ty in TYPES}
SD = {ty: RS(transpose(cartan(*ty))) for ty in TYPES}

head(1, 'the inner product: |rho|^2 = h^vee dim(g) / 12, every type')
bad = []
for ty in TYPES:
    s = S[ty]
    rho = s.rho()
    lhs = s.ip(rho, rho); rhs = s.hv() * s.dim() / 12
    if lhs != rhs or s.hv() != KNOWN_H[ty]: bad.append(ty)
check(not bad, 'strange formula and the dual Coxeter number agree with the table for all %d types%s'
      % (len(TYPES), (' (bad: %s)' % bad) if bad else ''))

head(2, 'anchors the formula did not produce')
vir = S[('A', 1)]; w3 = S[('A', 2)]
check(vir.c(F(4, 3)) == F(1, 2) and vir.c(F(3, 4)) == F(1, 2), 'Virasoro, t = 3/4 or 4/3: c = 1/2 (Ising)')
check(vir.c(F(5, 4)) == F(7, 10), 'Virasoro, t = 5/4: c = 7/10 (tricritical Ising)')
check(vir.c(F(3, 2)) == 0 and vir.c(F(2, 3)) == 0, 'Virasoro, t = 3/2: c = 0')
check(w3.c(F(5, 4)) == F(4, 5), 'W_3, t = 5/4: c = 4/5 (three-state Potts)')
check(vir.c(F(1)) == 1, 'Virasoro, t = 1: c = 1 (a free boson)')

head(3, 'duality: c_g(t) = c_{Lg}(1/(r t)), all types, 12 values of t')
TS = [F(1, 2), F(2, 3), F(3, 4), F(1, 3), F(5, 7), F(7, 5), F(3), F(11, 4), F(13, 9), F(2), F(9, 5), F(17, 6)]
for ty in TYPES:
    r = S[ty].lacing()
    ok = all(S[ty].c(t) == SD[ty].c(1 / (r * t)) for t in TS)
    check(ok and r == SD[ty].lacing(), '%s_%d  (r = %s): equal at all 12 t' % (ty[0], ty[1], r))

head(4, 'self-dual point t = 1 (k = 1 - h^vee), simply laced: c = rank')
SL = [ty for ty in TYPES if S[ty].lacing() == 1]
check(all(S[ty].c(F(1)) == ty[1] for ty in SL), 'c = rank for all %d simply-laced types tested' % len(SL))
NSL = [ty for ty in TYPES if S[ty].lacing() != 1]
check(all(S[ty].c(F(1)) != ty[1] for ty in NSL if ty != ('B', 2)),
      'and NOT for non-simply-laced types (there rho != rho^vee; the fixed point of t -> 1/(r t) is t = 1/sqrt(r))')

head(5, 'controls: each must fail')
nsl = [ty for ty in TYPES if S[ty].lacing() != 1]
wrong = [ty for ty in nsl if all(S[ty].c(t) == SD[ty].c(1 / t) for t in TS)]
check(nsl and not wrong, 'with t\' = 1/t (r forgotten) duality FAILS for all %d non-simply-laced types' % len(nsl))
# B_2 = C_2 (so_5 = sp_4), F_4 and G_2 are self-dual: only B_n, C_n (n >= 3) can differ
pair = [('B', 3), ('B', 4), ('C', 3), ('C', 4)]
differ = [ty for ty in pair if any(S[ty].c(t) != SD[ty].c(t) for t in TS)]
check(len(differ) == len(pair), 'g and Lg have different c at the same t for B_3, B_4, C_3, C_4 (the check can tell them apart)')
check(all(S[ty].c(t) == SD[ty].c(t) for ty in (('B', 2), ('F', 4), ('G', 2)) for t in TS),
      'and equal for B_2 (= C_2), F_4, G_2, which are self-dual -- as they must be')
check(S[('B', 3)].c(F(2, 3)) != SD[('B', 3)].c(1 / (S[('B', 3)].lacing() * F(3, 2))),
      'a mis-paired t (1/(r t) at the wrong t) does not match')

print()
if FAIL:
    print('FAILED: %d check(s)' % len(FAIL)); sys.exit(1)
print('all checks passed'); sys.exit(0)
