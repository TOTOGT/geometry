#!/usr/bin/env python3
"""ch-local-equivalence-verify.py  --  Book 7, Lipshitz / local equivalence chapters.

What this checks, and what it does not.

It re-does, in exact integer/rational arithmetic and from the formulas printed in
R. Lipshitz, "On Khovanov local equivalence groups", arXiv:2610.37595v1 (27 Oct 2026):

  A. the bowtie complexes D_{p,m,n} (Section 2.2): grading, d^2 = 0, that h^-1 D has
     the homology of a point, the s_c computation for D_{2,1,1} that proves it is
     not trivial (Lemma 2.8), and that D_{2,1,1} is self-dual (so has order <= 2);
  B. Table 2 of the paper (typed in below from the paper's text, not from a knot
     program): the three relations the paper states for its census, and Corollary 3.1,
     "view Table 2 as a matrix and row-reduce it", with a control that must fail;
  C. the arithmetic inside Table 3 (row totals; column totals).

It does NOT check: the Z-infinity summand theorem, the 2-torsion independence over
all primes (Theorem 1.1 beyond the invariant calculation), anything about the
chain-homotopy-equivalence that makes D_{p,m,n} knot-like beyond rational homology,
or that any entry of Table 2 is the true value for that knot (those came from code
written and run by Claude, per the paper, which its author says he did not examine).
Run:  python3 ch-local-equivalence-verify.py
"""
from fractions import Fraction
from itertools import product
import sys

fails = []
def check(name, ok, detail=""):
    print(("PASS  " if ok else "FAIL  ") + name + (("  -- " + detail) if detail else ""))
    if not ok: fails.append(name)

# ---------------------------------------------------------------- A. bowtie complexes
# generators in order x, y+, y0, y-, z ; bigrading (homological, quantum), n = n of D_{p,m,n}
def bowtie(p, m, n):
    P = p**m
    grad = {'x': (-1, -2*n), 'y+': (0, 2*n), 'y0': (0, 0), 'y-': (0, -2*n), 'z': (1, 2*n)}
    # d(g) = list of (coefficient, h-power, target)
    d = {
        'x':  [(2*P, n, 'y0'), (1, 2*n, 'y+'), (2*P*P, 0, 'y-')],
        'y0': [(-2*P, n, 'z')],
        'y+': [(2*P*P, 0, 'z')],
        'y-': [(1, 2*n, 'z')],
        'z':  [],
    }
    return grad, d

def dd(d, g):
    """d(d(g)) as {(target, hpower): coeff}"""
    out = {}
    for c, k, t in d[g]:
        for c2, k2, t2 in d[t]:
            key = (t2, k + k2)
            out[key] = out.get(key, 0) + c * c2
    return {k: v for k, v in out.items() if v}

ok_all = True; ok_grad = True; combos = 0
for p, m, n in product([2, 3, 5, 7], [1, 2, 3, 4], [1, 2, 3, 4]):
    grad, d = bowtie(p, m, n)
    combos += 1
    for g in d:
        if dd(d, g): ok_all = False
        for c, k, t in d[g]:
            # d raises homological degree by 1 and preserves quantum grading (h has q = -2)
            if grad[t][0] != grad[g][0] + 1 or grad[t][1] - 2*k != grad[g][1]: ok_grad = False
check("A1  d^2 = 0 on D_{p,m,n}", ok_all, f"{combos} parameter triples, p in 2,3,5,7, m,n in 1..4")
check("A2  d is homogeneous of bidegree (1, 0)", ok_grad)

# control: break one entry; d^2 = 0 must fail
grad, d = bowtie(2, 1, 1)
d['y+'] = [(2*4 + 1, 0, 'z')]
check("A3  control: perturbing d(y+) breaks d^2 = 0 (the test can fail)", bool(dd(d, 'x')))

# rational homology of h^-1 D (h a unit: set h = 1; the quantum grading no longer separates)
def rank(M):
    M = [[Fraction(x) for x in r] for r in M]; r = 0
    if not M: return 0
    for c in range(len(M[0])):
        pv = next((k for k in range(r, len(M)) if M[k][c] != 0), None)
        if pv is None: continue
        M[r], M[pv] = M[pv], M[r]
        for k in range(len(M)):
            if k != r and M[k][c] != 0:
                f = M[k][c] / M[r][c]; M[k] = [a - f*b for a, b in zip(M[k], M[r])]
        r += 1
    return r

grad, d = bowtie(2, 1, 1)
# degree -1: x ; degree 0: y+, y0, y- ; degree 1: z.   d(-1->0) is a 3x1, d(0->1) is a 1x3
d_m1 = [[c for (c, k, t) in d['x'] if t == tt][0] for tt in ('y+', 'y0', 'y-')]
d_0 = [[ [c for (c, k, t) in d[g] if t == 'z'][0] for g in ('y+', 'y0', 'y-')]]
r1 = rank([[v] for v in d_m1]); r0 = rank(d_0)
hom = (1 - r1, 3 - r1 - r0, 1 - r0)
check("A4  h^-1 D_{2,1,1} has rational homology of rank 1 in degree 0 only", hom == (0, 1, 0), f"ranks of homology in degrees -1,0,1 = {hom}")

# s_c(D_{2,1,1}) from Lemma 2.8.  Cycles of bidegree (0, j) are a y+ h^a + b y0 h^b + c y- h^c with
# nonnegative powers fixed by j; psi sends h^k y+ -> -2 p^m h^(k-n), y0 -> 1, others -> 0.
p, m, n = 2, 1, 1
P = p**m
def cycles_value_set(j, bound=6):
    """returns (dimension of cycle lattice in bidegree (0,j), list of psi-values of cycles with small coefficients)"""
    gens = []
    # (name, hpower) with quantum grading q(gen) - 2*hpower == j
    for name, q in (('y+', 2*n), ('y0', 0), ('y-', -2*n)):
        k2 = q - j
        if k2 >= 0 and k2 % 2 == 0: gens.append((name, k2 // 2))
    if not gens: return 0, []
    # d of each into z: coefficient * h^(power)  (single target z, a single h-power, so one linear equation)
    def dz(name, k):
        c = [cc for (cc, kk, tt) in d_gen[name]][0]; kk = [kk for (cc, kk, tt) in d_gen[name]][0]
        return c
    vals = []; dim = 0
    coef_range = range(-bound, bound + 1)
    sols = []
    for cs in product(coef_range, repeat=len(gens)):
        if not any(cs): continue
        if sum(c * dz(g[0], g[1]) for c, g in zip(cs, gens)) == 0:
            sols.append(cs)
    # psi value (coefficient of the monomial in Z) of each cycle
    def psi(name):
        return {'y+': -2*P, 'y0': 1, 'y-': 0}[name]
    for cs in sols:
        vals.append(sum(c * psi(g[0]) for c, g in zip(cs, gens)))
    rk = rank(sols) if sols else 0
    return rk, vals
d_gen = {g: d[g] for g in d}
sc = None
rows_sc = []
for j in range(4, -7, -2):
    rk, vals = cycles_value_set(j)
    gen_possible = any(abs(v) == 1 for v in vals)
    rows_sc.append((j, rk, gen_possible))
    if gen_possible and sc is None: sc = j
for j, rk, g in rows_sc: print(f"        bidegree (0,{j:>2}): cycle rank {rk}, a cycle maps to a generator: {g}")
check("A5  s_c(D_{2,1,1}) = -2, not 0, so D_{2,1,1} is not locally trivial", sc == -2, f"s_c = {sc}")
# the witness from the paper: h y0 + 4 y-  is a cycle and psi of it is h, a unit
wit_cycle = sum(c * [cc for (cc, kk, tt) in d['y0']][0] if g == 'y0' else c * [cc for (cc, kk, tt) in d['y-']][0] for c, g in ((1, 'y0'), (4, 'y-')))
check("A6  the witness h*y0 + 4*y- is a cycle (the paper's witness)", wit_cycle == 0)

# self-duality: dual differential is (up to a global sign convention) the transpose.  The paper's map
# x <-> z, y+ <-> y-, y0 -> -y0.  Check phi o d = eps * d* o phi with one sign eps per homological degree.
order = ['x', 'y+', 'y0', 'y-', 'z']
idx = {g: i for i, g in enumerate(order)}
Mtx = [[0]*5 for _ in range(5)]          # Mtx[target][source], h set to 1 (powers match under the swap)
for g in d:
    for c, k, t in d[g]: Mtx[idx[t]][idx[g]] += c
star = {'x': 'z', 'y+': 'y-', 'y0': 'y0', 'y-': 'y+', 'z': 'x'}      # image generator, as a dual basis vector
sgn = {'x': 1, 'y+': 1, 'y0': -1, 'y-': 1, 'z': 1}
# phi(g) = sgn[g] * (star[g])^*.  d^*((t)^*) = sum_g Mtx[t][g] g^*   (transpose).
# phi(d g) = sum_t Mtx[t][g] sgn[t] star[t]^*   versus   d^*(phi g) = sgn[g] * sum_s Mtx[star[g]... ]
ok_pairs = {}
for g in order:
    lhs = {}
    for t in order:
        c = Mtx[idx[t]][idx[g]]
        if c: lhs[star[t]] = lhs.get(star[t], 0) + c * sgn[t]
    # d^* of star[g]^*: coefficient of s^* is Mtx[star[g]][s]
    rhs = {}
    for s in order:
        c = Mtx[idx[star[g]]][idx[s]]
        if c: rhs[s] = rhs.get(s, 0) + c * sgn[g]
    # compare lhs (in dual basis labelled by star-targets) with rhs: lhs keys are 'star[t]^*' labels, rhs keys are 's^*'
    ok_pairs[g] = (lhs, rhs)
degree = {'x': -1, 'y+': 0, 'y0': 0, 'y-': 0, 'z': 1}
eps_by_degree = {}
selfdual = True
for g, (lhs, rhs) in ok_pairs.items():
    if lhs == {} and rhs == {}: continue
    e_vals = set()
    for e in (1, -1):
        if lhs == {k: e * v for k, v in rhs.items()} and set(lhs) == set(rhs): e_vals.add(e)
    if not e_vals: selfdual = False
    else: eps_by_degree.setdefault(degree[g], set()).update(e_vals)
check("A7  D_{2,1,1} is isomorphic to its dual under x<->z, y+<->y-, y0->-y0 (up to the usual sign) ",
      selfdual, f"signs found per homological degree: { {k: sorted(v) for k, v in eps_by_degree.items()} }")

# ---------------------------------------------------------------- B. Table 2
COLS = ["sQ", "sF2", "tau", "psi1o", "phio1", "phio2", "phio3", "phio4", "phio5", "phie1", "psi1e", "phiHF1", "phiHF2", "phiHF3"]
ROWS = [
    ('31', (2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0)),
    ('819', (6, 6, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0)),
    ('942', (0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
    ('12n200', (-2, -2, -1, 3, 1, 0, 0, 0, 0, 0, 0, -1, 0, 0)),
    ('12n475', (0, 0, 0, -1, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0)),
    ('13n309', (0, 0, 0, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0)),
    ('13n4587', (10, 10, 5, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1)),
    ('14n19265', (0, -2, 0, 1, 1, 0, 0, 0, 0, 1, -1, 0, 0, 0)),
    ('14n26039', (0, 0, -1, 1, 0, -1, 0, 0, 0, 0, 0, -1, 0, 0)),
    ('15n5319', (-2, -2, -1, 1, 0, 0, 0, 1, 0, 0, 0, -1, 0, 0)),
    ('16n956730', (-2, -2, -1, 1, 0, 0, 0, 0, 1, 0, 0, -1, 0, 0)),
]
ci = {c: i for i, c in enumerate(COLS)}
check("B0  Table 2 has 11 knots and 14 invariant columns (the caption says 13)", len(ROWS) == 11 and len(COLS) == 14)
v = lambda r, c: r[1][ci[c]]
check("B1  tau = phiHF1 + 2 phiHF2 + 3 phiHF3 on every row (DHST formula, as the paper uses it)",
      all(v(r, "tau") == v(r, "phiHF1") + 2*v(r, "phiHF2") + 3*v(r, "phiHF3") for r in ROWS))
check("B2  sF2 - sQ = 2 psi1e on every row (as the paper states for its census)",
      all(v(r, "sF2") - v(r, "sQ") == 2*v(r, "psi1e") for r in ROWS))
check("B3  phie1 = - psi1e on every row (as the paper states)", all(v(r, "phie1") == -v(r, "psi1e") for r in ROWS))

def rank_of(colnames, rows=ROWS):
    return rank([[v(r, c) for c in colnames] for r in rows])
six = ["psi1o", "phio1", "phio2", "phio3", "phio4", "phio5"]
others = [c for c in COLS if c not in six]
r_all, r_oth = rank_of(COLS), rank_of(others)
check("B4  Corollary 3.1: the six invariants are independent of each other and of the rest, on these 11 knots",
      r_all - r_oth == 6, f"rank(all 14 columns) = {r_all}, rank(the other 8) = {r_oth}, gain = {r_all - r_oth}")
# control: delete the information in phio5 (zero the column); the gain must drop to 5, or the test is blind
ROWS_ctl = [(n, tuple(0 if COLS[i] == "phio5" else x for i, x in enumerate(vals))) for n, vals in ROWS]
r_all_c = rank_of(COLS, ROWS_ctl); r_oth_c = rank_of(others, ROWS_ctl)
check("B5  control: with phio5 zeroed the gain falls to 5 (the rank test can fail)", r_all_c - r_oth_c == 5, f"gain = {r_all_c - r_oth_c}")
# and a second control: replace phio5 by a copy of tau; it is dependent on the others, so the gain must fall to 5 as well
ROWS_dep = [(n, tuple(vals[ci["tau"]] if COLS[i] == "phio5" else x for i, x in enumerate(vals))) for n, vals in ROWS]
g2 = rank_of(COLS, ROWS_dep) - rank_of(others, ROWS_dep)
check("B6  control: phio5 replaced by a copy of tau gives gain 5", g2 == 5, f"gain = {g2}")
print("        note: this is a certificate on the table as printed. It is only as true as the table; the table's entries")
print("        came from code that the paper says its author did not read.")

# ---------------------------------------------------------------- C. Table 3
T3 = {
    "trivial": [249, 185, 888, 5110, 27434, 167989, 1008744, 1210599],
    "(1,-1)":  [0, 0, 0, 0, 1, 26, 88, 115],
    "(-1,1)":  [0, 0, 0, 0, 1, 15, 74, 90],
}
T3cols = ["<=10", "11n", "12n", "13n", "14n", "15n", "16n"]
for name, row in T3.items():
    check(f"C1  Table 3 row {name}: seven columns sum to the stated total", sum(row[:7]) == row[7], f"{sum(row[:7])} vs {row[7]}")
col_sums = [sum(T3[k][i] for k in T3) for i in range(7)]
print("        column sums (knots surveyed per crossing class, as Table 3 implies):", dict(zip(T3cols, col_sums)))
print("        compare these seven numbers with a knot census (non-alternating counts 11n..16n); this script has no census.")

print()
if fails:
    print("FAILED:", ", ".join(fails)); sys.exit(1)
print("All checks passed. See the header for what they do not cover.")
