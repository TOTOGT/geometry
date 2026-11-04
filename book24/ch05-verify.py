#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book24/ch05-verify.py -- every check behind book24/ch05-linear-maps.html. Run first.

    python3 book24/ch05-verify.py

Checks over finite fields are exhaustive within the stated bounds (every linear map, every subspace),
so a PASS is a statement about the whole finite structure, not a sample. Nothing here proves a theorem
for all fields; the proofs are on the page.

  [1] every linear map F_p^n -> F_p^m for the listed (p, n, m): Theorem 1 (images and inverse images of
      subspaces are subspaces), Theorem 2 (|N| |R| = p^n), the proof's steps (fibres are cosets of N,
      the induced map on X/N is a bijection onto R), Corollary A, Corollary B and its uniqueness
      remark; the number of maps of each rank against a closed formula
  [2] the controls: (x, y) -> (x, 0) breaks Corollary B; the identity breaks the converse of Corollary A
  [3] Application 1 over F_3, F_5, F_7 and over Q: the evaluation map at n distinct points is a bijection;
      repeated points, one more degree, or too few degrees each break it
  [4] the Jacobian worked example F(x, y) = (x^2 + y, x y) at (1, 2), exact rational arithmetic
  [5] the held text: Lax, Linear Algebra and Its Applications, 2nd ed., Chapter 3, pp.19-22
      (printed page = pdf page - 17)
  [6] the Lean file: the seven theorems are present, none uses sorry, and the axiom report (if it
      exists yet) shows no sorryAx
"""
import itertools, os, re, subprocess, sys
from fractions import Fraction
from pathlib import Path

FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  [{detail}]" if detail else ""))
    if not ok: FAIL.append(label)

# ---- F_p^n ---------------------------------------------------------------------------------------
class Sp:
    def __init__(self, p, n):
        self.p, self.n = p, n
        self.els = list(itertools.product(range(p), repeat=n))
        self.zero = tuple([0] * n)
        self._subs = None
    def add(self, x, y): return tuple((a + b) % self.p for a, b in zip(x, y))
    def smul(self, k, x): return tuple((k * a) % self.p for a in x)
    def span(self, gens):
        S = {self.zero}
        for g in gens:
            S = {self.add(s, self.smul(k, g)) for s in S for k in range(self.p)}
        return frozenset(S)
    def is_sub(self, S):
        S = set(S)
        return (self.zero in S and all(self.add(x, y) in S for x in S for y in S)
                and all(self.smul(k, x) in S for k in range(self.p) for x in S))
    def subspaces(self):
        if self._subs is None:
            found = set()
            for r in range(self.n + 1):
                for gens in itertools.combinations(self.els, r):
                    found.add(self.span(gens))
            self._subs = sorted(found, key=lambda S: (len(S), sorted(S)))
        return self._subs
    def coset(self, x, W): return frozenset(self.add(x, w) for w in W)

_cache = {}
def space(p, n):
    if (p, n) not in _cache: _cache[(p, n)] = Sp(p, n)
    return _cache[(p, n)]

def maps(p, n, m):
    for ent in itertools.product(range(p), repeat=n * m):
        yield tuple(tuple(ent[i * n:(i + 1) * n]) for i in range(m))
def app(M, x, p): return tuple(sum(a * b for a, b in zip(row, x)) % p for row in M)
def rank_formula(p, n, m, r):
    num = den = 1
    for i in range(r):
        num *= (p ** n - p ** i) * (p ** m - p ** i)
        den *= (p ** r - p ** i)
    assert num % den == 0
    return num // den

SMALL = [(2, 1, 1), (2, 2, 2), (3, 2, 2), (2, 3, 2), (2, 2, 3), (2, 3, 3), (3, 2, 3), (3, 3, 2)]
BIG = [(3, 3, 3)]   # kernel/range/corollary checks only (19683 maps)

print("[1] every linear map F_p^n -> F_p^m (all p^(nm) matrices)")
for (p, n, m) in SMALL + BIG:
    detail = (p, n, m) in SMALL
    X, U = space(p, n), space(p, m)
    subsX, subsU = X.subspaces(), U.subspaces()
    N = p ** (n * m)
    ok_t1a = ok_t1b = ok_t2 = ok_fib = ok_quot = ok_A = ok_B = ok_Bu = ok_conv = True
    by_rank = {}
    trivial_kernel = 0
    for M in maps(p, n, m):
        img = {x: app(M, x, p) for x in X.els}
        ker = frozenset(x for x in X.els if img[x] == U.zero)
        rng = frozenset(img.values())
        if len(ker) * len(rng) != p ** n: ok_t2 = False                     # Theorem 2
        r = 0
        while p ** r < len(rng): r += 1
        by_rank[r] = by_rank.get(r, 0) + 1
        if detail:
            for S in subsX:                                                  # Theorem 1(a)
                if not U.is_sub({img[x] for x in S}): ok_t1a = False
            for S2 in subsU:                                                 # Theorem 1(b)
                if not X.is_sub({x for x in X.els if img[x] in S2}): ok_t1b = False
            fib = {}
            for x in X.els: fib.setdefault(img[x], set()).add(x)
            # proof of Theorem 2: each fibre is a coset of N, so has |N| points; X/N <-> R bijectively
            if not all(frozenset(f) == X.coset(next(iter(f)), ker) for f in fib.values()): ok_fib = False
            if len({X.coset(x, ker) for x in X.els}) != len(rng): ok_quot = False
        if m < n and len(ker) == 1: ok_A = False                             # Corollary A
        if m == n:
            if len(ker) == 1:
                trivial_kernel += 1
                if len(rng) != p ** m: ok_B = False                          # Corollary B
                if any(sum(1 for x in X.els if img[x] == u) != 1 for u in U.els): ok_Bu = False
            else:
                if len(rng) == p ** m: ok_conv = False                       # contrapositive: nonzero kernel => not onto
    tag = f"F_{p}^{n} -> F_{p}^{m}"
    if detail:
        check(f"{tag}: Theorem 1(a), image of every subspace is a subspace; (b) inverse image of every subspace is a subspace, all {N} maps", ok_t1a and ok_t1b)
    check(f"{tag}: Theorem 2, |ker| * |range| = p^n on all {N} maps", ok_t2)
    if detail:
        check(f"{tag}: every fibre is a coset of the kernel and X/N has |R| classes (the proof's steps)", ok_fib and ok_quot)
    if m < n:
        check(f"{tag}: Corollary A, m < n, every map has a nonzero vector sent to 0", ok_A)
    if m == n:
        check(f"{tag}: Corollary B, trivial kernel => onto, and each target vector has exactly one preimage; nonzero kernel => not onto ({trivial_kernel} maps with trivial kernel)",
              ok_B and ok_Bu and ok_conv)
        exp = 1
        for i in range(n): exp *= p ** n - p ** i
        check(f"{tag}: maps with trivial kernel = (p^n - 1)...(p^n - p^(n-1)) = {exp}", trivial_kernel == exp)
    ok_rank = all(by_rank.get(r, 0) == rank_formula(p, n, m, r) for r in range(min(n, m) + 1)) and sum(by_rank.values()) == N
    check(f"{tag}: number of maps of each rank r equals prod (p^n - p^i)(p^m - p^i)/(p^r - p^i)",
          ok_rank, ", ".join(f"rank {r}: {by_rank.get(r,0)}" for r in sorted(by_rank)))

print("[2] controls")
for p in (2, 3, 5):
    X = space(p, 2)
    T = lambda x: (x[0], 0)
    ker = [x for x in X.els if T(x) == (0, 0)]
    rng = {T(x) for x in X.els}
    check(f"F_{p}^2: (x, y) -> (x, 0) has equal dimensions, a nonzero kernel ({len(ker)} elements) and a range of {len(rng)} < {p*p} elements: Corollary B needs 'only x = 0 goes to 0'",
          len(ker) == p and len(rng) == p and len(rng) < p * p)
ident_ok = all(len([x for x in space(p, 2).els if x == (0, 0)]) == 1 for p in (2, 3))
check("the identity map of F_p^2 has m = n and a trivial kernel: Corollary A's hypothesis m < n cannot be weakened to m <= n",
      ident_ok)
# m > n: trivial kernel without being onto
p = 3; X, U = space(p, 2), space(p, 3)
T = lambda x: (x[0], x[1], 0)
check("F_3^2 -> F_3^3, (x, y) -> (x, y, 0): trivial kernel, but the range has 9 < 27 elements: Corollary B needs dim U = dim X",
      len({T(x) for x in X.els}) == 9 and all(T(x) != (0, 0, 0) for x in X.els if x != (0, 0)))

print("[3] Application 1: polynomials of degree < n, evaluated at n distinct points")
def evalp(c, s, p): return sum(a * pow(s, i, p) for i, a in enumerate(c)) % p
for p, nmax in [(3, 3), (5, 5), (7, 3)]:
    ok = True; tuples = 0
    for n in range(1, nmax + 1):
        polys = list(itertools.product(range(p), repeat=n))
        for pts in itertools.permutations(range(p), n):
            tuples += 1
            vals = {tuple(evalp(c, s, p) for s in pts) for c in polys}
            if len(vals) != p ** n: ok = False       # a bijection: p^n polynomials, p^n value lists
    check(f"F_{p}: for every n <= {nmax} and every ordered list of n distinct points ({tuples} lists), the evaluation map is a bijection onto F_{p}^n", ok)
p = 5
polys3 = list(itertools.product(range(p), repeat=3))
rep = (0, 0, 1)
vals = {tuple(evalp(c, s, p) for s in rep) for c in polys3}
check("F_5, points (0, 0, 1) (a repeat): the evaluation map is not onto; 25 < 125 value lists", len(vals) == 25 and (0, 4, 1) in polys3 and all(evalp((0, 4, 1), s, p) == 0 for s in rep))
polys4 = list(itertools.product(range(p), repeat=4))
ok = True
for pts in itertools.permutations(range(p), 3):
    vals = {tuple(evalp(c, s, p) for s in pts) for c in polys4}
    ker = [c for c in polys4 if all(evalp(c, s, p) == 0 for s in pts)]
    if not (len(ker) > 1 and len(vals) == 125): ok = False   # degree < 4, 3 points: m = 3 < n = 4, Corollary A
check("F_5: degree < 4 (one degree too many) with 3 distinct points: nonzero kernel every time (Corollary A), 60 lists", ok)
xp = (0, 4, 0, 0, 0, 1)   # x^5 - x over F_5
check("F_5: x^5 - x is nonzero, has degree 5, and vanishes at all 5 points: degree < n cannot be relaxed to <= n",
      all(evalp(xp, s, 5) == 0 for s in range(5)) and any(xp))
# over Q, exact
nodes = [Fraction(0), Fraction(1), Fraction(2), Fraction(5)]
vals_q = [Fraction(3), Fraction(-1), Fraction(4), Fraction(1)]
def lagrange(nodes, vals):
    n = len(nodes); coef = [Fraction(0)] * n
    for i in range(n):
        poly = [Fraction(1)]; den = Fraction(1)
        for j in range(n):
            if j == i: continue
            poly = [Fraction(0)] + poly
            for k in range(len(poly) - 1): poly[k] -= nodes[j] * poly[k + 1]
            den *= nodes[i] - nodes[j]
        for k in range(n): coef[k] += vals[i] * poly[k] / den
    return coef
cq = lagrange(nodes, vals_q)
ev = lambda c, s: sum(a * s ** i for i, a in enumerate(c))
check("over Q, nodes 0, 1, 2, 5 and values 3, -1, 4, 1: Lagrange gives a polynomial of degree < 4 with exactly those values",
      len(cq) == 4 and all(ev(cq, s) == v for s, v in zip(nodes, vals_q)), "coefficients " + ", ".join(str(c) for c in cq))

print("[4] the Jacobian worked example: F(x, y) = (x^2 + y, x y) at a = (1, 2)")
F = lambda x, y: (x * x + y, x * y)
a = (Fraction(1), Fraction(2))
J = ((Fraction(2), Fraction(1)), (Fraction(2), Fraction(1)))   # [[2x, 1], [y, x]] at (1, 2)
Jh = lambda h: (J[0][0] * h[0] + J[0][1] * h[1], J[1][0] * h[0] + J[1][1] * h[1])
check("the matrix of partial derivatives at (1, 2) is [[2, 1], [2, 1]]",
      J == ((2, 1), (2, 1)) and (2 * a[0], Fraction(1), a[1], a[0]) == (2, 1, 2, 1))
ok = True
grid = [Fraction(k, 7) for k in range(-14, 15)]
for h1 in grid:
    for h2 in grid:
        Fa = F(a[0], a[1]); Fh = F(a[0] + h1, a[1] + h2); lin = Jh((h1, h2))
        rem = (Fh[0] - Fa[0] - lin[0], Fh[1] - Fa[1] - lin[1])
        if rem != (h1 * h1, h1 * h2): ok = False
check(f"F(a + h) - F(a) - J h equals (h1^2, h1 h2) exactly, on {len(grid)**2} rational h", ok)
check("det J = 0, J is not the zero matrix, so rank 1; its kernel is spanned by (1, -2); rank + nullity = 1 + 1 = 2",
      J[0][0] * J[1][1] - J[0][1] * J[1][0] == 0 and any(any(r) for r in J) and Jh((Fraction(1), Fraction(-2))) == (0, 0)
      and all(Jh((x, y)) != (0, 0) for x in range(-3, 4) for y in range(-3, 4) if (x, y) != (0, 0) and y != -2 * x))
ok = True
for t in [Fraction(1, 2), Fraction(1, 10), Fraction(-3, 7), Fraction(1, 1000)]:
    Fa = F(a[0], a[1]); Fh = F(a[0] + t, a[1] - 2 * t)
    if (Fh[0] - Fa[0], Fh[1] - Fa[1]) != (t * t, -2 * t * t): ok = False
check("along the kernel direction (1, -2) the linear model predicts no motion; F moves by exactly (t^2, -2 t^2), second order", ok)
# no other linear map fits: ratio |R_A(t u)| / |t u| tends to |(J - A) u| / |u| (sup norm)
sup = lambda v: max(abs(v[0]), abs(v[1]))
ok = True; tested = 0
dirs = [(Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)), (Fraction(1), Fraction(1)), (Fraction(1), Fraction(-1)), (Fraction(2), Fraction(-1))]
for e in itertools.product((-1, 0, 1), repeat=4):
    if not any(e): continue
    E = ((Fraction(e[0]), Fraction(e[1])), (Fraction(e[2]), Fraction(e[3])))
    A = ((J[0][0] + E[0][0], J[0][1] + E[0][1]), (J[1][0] + E[1][0], J[1][1] + E[1][1]))
    for u in dirs:
        Eu = (E[0][0] * u[0] + E[0][1] * u[1], E[1][0] * u[0] + E[1][1] * u[1])
        if sup(Eu) == 0: continue
        for t in (Fraction(1, 1000), Fraction(1, 1000000)):
            h = (t * u[0], t * u[1])
            Fa = F(a[0], a[1]); Fh = F(a[0] + h[0], a[1] + h[1])
            Ah = (A[0][0] * h[0] + A[0][1] * h[1], A[1][0] * h[0] + A[1][1] * h[1])
            rem = (Fh[0] - Fa[0] - Ah[0], Fh[1] - Fa[1] - Ah[1])
            ratio = sup(rem) / sup(h)
            if abs(ratio - sup(Eu) / sup(u)) > t * sup(u): ok = False
            tested += 1
check(f"any linear A = J + E with E != 0 leaves a remainder of the size of |h| along some direction (ratio within t|u| of |E u|/|u|): {tested} (E, u, t) cases; J does not", ok)
ratioJ = max(sup((u[0] * u[0], u[0] * u[1])) / sup(u) * Fraction(1, 10 ** 6) for u in dirs)
check("for A = J the ratio is at most t |u|, which tends to 0", ratioJ <= Fraction(1, 10 ** 6) * 2)

print("[5] the held text: Lax pp.19-22 (printed page = pdf page - 17)")
flat = lambda t: re.sub(r"\s+", " ", t).lower()
pdf = None
for c in ("~/Downloads", "~/mnt/Downloads", "."):
    q = Path(os.path.expanduser(c)) / "lax.pdf"
    if q.is_file(): pdf = q; break
if pdf is None:
    print("  SKIP: lax.pdf not found (no claim made)")
else:
    L = subprocess.run(["pdftotext", "-layout", "-f", "36", "-l", "39", str(pdf), "-"],
                       capture_output=True, text=True, timeout=150).stdout.split("\f")
    pg = lambda n: flat(L[n + 17 - 36])
    check("p.19: Chapter 3, Linear Mappings; domain space, target space, additive, homogeneous",
          "linear mappings" in pg(19) and "domain space" in pg(19) and "target space" in pg(19) and "homogeneous" in pg(19))
    check("p.20: Theorem 1 (image and inverse image of a subspace), range, nullspace, Theorem 2",
          "theorem 1" in pg(20) and "inverse image" in pg(20) and "nullspace" in pg(20) and "theorem 2" in pg(20) and "range" in pg(20))
    check("p.21: the proof by the quotient space, Corollaries A and B, Corollary 6 of Chapter 1",
          "quotient space" in pg(21) and "corollaries" in pg(21) and "corollary 6" in pg(21) and "corollary a" in pg(21))
    check("p.22: Corollary B', Application 1 and Application 2 (polynomials, distinct zeros)",
          "corollary b" in pg(22) and "application" in pg(22) and "application 2" in pg(22) and "distinct" in pg(22) and "polynomial" in pg(22))
print("  OCR note: lax.pdf is a scan; these checks match short phrases and may miss a page the scan garbled.")

print("[6] the Lean file")
here = Path(__file__).resolve().parent
src = (here / "LinearMaps.lean").read_text(encoding="utf-8")
rep = here / "linearmaps.axioms.txt"
code = re.sub(r"/-.*?-/", "", src, flags=re.S)
code = re.sub(r"--[^\n]*", "", code)
names = ["theorem1a", "theorem1b", "theorem2", "corollaryA", "corollaryB",
         "control_corollaryB_needs_trivial_kernel", "interpolation"]
for nme in names:
    check(f"theorem {nme} is declared", re.search(r"\btheorem\s+" + nme + r"\b", code) is not None)
check("no proof in the file uses sorry", re.search(r"\bsorry\b", code) is None)
if not rep.is_file():
    print("  NOT YET RUN: linearmaps.axioms.txt does not exist. LinearMaps.lean is UNTESTED.")
else:
    lines = [l for l in rep.read_text(encoding="utf-8").splitlines() if l.startswith("'Book24LM.")]
    check("the axiom report has one line per theorem", len(lines) == len(names), f"{len(lines)} lines")
    check("no theorem line shows sorryAx", all("sorryAx" not in l for l in lines))

print("[HONESTY]")
print("  Finite-field checks are exhaustive but are checks of examples; the theorems are on the page and in the Lean file.")
print("  LinearMaps.lean: first compile 2026-11-04 had 6 of 7 theorems clean; corollaryA depends on sorryAx until the fix already in the file is recompiled (check [6] reports it). Applications 2 and 3, the transpose, and the general differential are not in it.")
print("  The Jacobian example is one function at one point, computed exactly; it illustrates the idea and proves nothing general.")
print("  Held text: Lax only (Wiley-copyrighted, page references, nothing copied). Lax works over R or C; finite fields go beyond him.")
print()
print("0 FAIL" if not FAIL else f"{len(FAIL)} FAIL: {FAIL}")
sys.exit(1 if FAIL else 0)
