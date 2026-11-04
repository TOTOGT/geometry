#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book24/ch04-verify.py -- every check behind book24/ch04-basis-dimension.html. Run first.

    python3 book24/ch04-verify.py

All checks over finite fields are exhaustive within the stated bounds (every list, every subspace,
every pair), so a PASS is a statement about the whole finite structure, not a sample. Nothing here
proves a theorem for all fields; the proofs are on the page.

  [1] Exercise 10, Lemma 1, Lemma 2, Theorem 3, Theorem 4 on F_2^2, F_3^2, F_2^3, F_3^3 (lists of
      length up to n+1); the count of ordered bases equals the product of (p^n - p^i)
  [2] Theorem 5 and Exercise 12: every subspace of F_p^n has complements, each gives a unique
      decomposition and adds dimensions; there are p^(j(n-j)) of them; isomorphism counts
  [3] Theorem 6, Corollary 6', Exercise 16: the classes of the added vectors form a basis of the
      quotient; a subspace of full dimension is everything; polynomials vanishing at points
  [4] Theorem 7 (and the identity without the hypothesis X = U + V), the proof's intermediate
      claims, Exercise 18, Exercise 19 (an explicit isomorphism)
  [5] the held text: Lax, Linear Algebra and Its Applications, 2nd ed., pp.5-11 (printed page =
      pdf page - 17)
  [6] the Lean file: the fourteen theorems are present, none uses sorry, and the axiom report
      (if it exists yet) shows no sorryAx
"""
import itertools, os, re, subprocess, sys
from pathlib import Path

FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  [{detail}]" if detail else ""))
    if not ok: FAIL.append(label)

# ---- F_p^n -------------------------------------------------------------------------------------
class Sp:
    def __init__(self, p, n):
        self.p, self.n = p, n
        self.els = list(itertools.product(range(p), repeat=n))
        self.zero = tuple([0] * n)
    def add(self, x, y): return tuple((a + b) % self.p for a, b in zip(x, y))
    def smul(self, k, x): return tuple((k * a) % self.p for a in x)
    def neg(self, x): return tuple((-a) % self.p for a in x)
    def sub(self, x, y): return self.add(x, self.neg(y))
    def span(self, gens):
        S = {self.zero}
        for g in gens:
            S = {self.add(s, self.smul(k, g)) for s in S for k in range(self.p)}
        return frozenset(S)
    def dim(self, S):
        d, size = 0, 1
        while size < len(S): size *= self.p; d += 1
        assert size == len(S)
        return d
    def is_sub(self, S):
        S = set(S)
        return (self.zero in S and all(self.add(x, y) in S for x in S for y in S)
                and all(self.smul(k, x) in S for k in range(self.p) for x in S))
    def indep(self, lst):  # list of vectors
        return len(self.span(lst)) == self.p ** len(lst)
    def subspaces(self):
        found = set()
        for r in range(self.n + 1):
            for gens in itertools.combinations(self.els, r):
                found.add(self.span(gens))
        return sorted(found, key=lambda S: (len(S), sorted(S)))
    def coset(self, x, W): return frozenset(self.add(x, w) for w in W)
    def coset_key(self, x, W): return min(self.coset(x, W))

def gl_order(p, n):
    out = 1
    for i in range(n): out *= p ** n - p ** i
    return out

SPACES = [(2, 2), (3, 2), (2, 3), (3, 3)]

print("[1] independence, spanning lists, bases (lists up to length n+1; up to n for F_3^3)")
for p, n in SPACES:
    X = Sp(p, n)
    tag = f"F_{p}^{n}"
    maxlen = n + 1
    ind_lens, span_lens, basis_count = set(), set(), 0
    zero_in_indep = False
    extend_ok = True
    allbases = []
    basis_lens = set()
    for L in range(0, maxlen + 1):
        if (p, n) == (3, 3) and L > 3: break  # F_3^3: lists of length 4 are 531441; bound is n there
        for lst in itertools.product(X.els, repeat=L):
            sp_size = len(X.span(lst))
            if sp_size == p ** L:
                ind_lens.add(L)
                if X.zero in lst: zero_in_indep = True
            if sp_size == p ** n: span_lens.add(L)
            if sp_size == p ** L and sp_size == p ** n:
                basis_lens.add(L)
                if L == n: allbases.append(lst)
    check(f"{tag}: Exercise 10: no independent list has a zero vector", not zero_in_indep)
    check(f"{tag}: Lemma 1: max independent length {max(ind_lens)} <= min spanning length {min(span_lens)}",
          max(ind_lens) <= min(span_lens))
    check(f"{tag}: Lemma 2/Theorem 3: bases exist and every basis has length exactly n = {n}",
          len(allbases) > 0)
    # all independent+spanning lists have length n
    check(f"{tag}: Theorem 3: lengths of independent+spanning lists (up to {'n' if (p, n) == (3, 3) else 'n+1'}): {sorted(basis_lens)}", basis_lens == {n})
    check(f"{tag}: ordered bases = product (p^n - p^i) = {gl_order(p, n)}", len(allbases) == gl_order(p, n),
          f"{len(allbases)} found")
    # Theorem 4: every independent list (length <= n) extends by appending vectors to a basis
    for L in range(0, n + 1):
        for lst in itertools.product(X.els, repeat=L):
            if not X.indep(lst): continue
            cur = list(lst)
            while len(cur) < n:
                nxt = None
                for v in X.els:
                    if v not in X.span(cur):
                        nxt = v; break
                if nxt is None: extend_ok = False; break
                cur.append(nxt)
            if not (X.indep(cur) and len(X.span(cur)) == p ** n): extend_ok = False
            if not extend_ok: break
        if not extend_ok: break
    check(f"{tag}: Theorem 4: every independent list (length <= n) completes to a basis by adjoining vectors", extend_ok)

print("[2] Theorem 5: complements; Exercise 12")
for p, n in SPACES:
    X = Sp(p, n)
    subs = X.subspaces()
    tag = f"F_{p}^{n}"
    ok_all, ok_count, noncomp = True, True, True
    for Y in subs:
        j = X.dim(Y)
        comps = []
        for Z in subs:
            sums = {}
            for y in Y:
                for z in Z:
                    s = X.add(y, z)
                    sums[s] = sums.get(s, 0) + 1
            # complement iff every x decomposes uniquely
            if len(sums) == len(X.els) and all(c == 1 for c in sums.values()):
                comps.append(Z)
        if not comps: ok_all = False
        for Z in comps:
            if X.dim(Y) + X.dim(Z) != n: ok_all = False
        if len(comps) != p ** (j * (n - j)): ok_count = False
        if 0 < j < n and len(comps) < 2: noncomp = False
    check(f"{tag}: all {len(subs)} subspaces have a complement; every complement adds dimensions", ok_all)
    check(f"{tag}: number of complements of a j-dimensional subspace is p^(j(n-j)) for every subspace", ok_count)
    check(f"{tag}: for 0 < j < n the complement is never unique", noncomp)
    # Exercise 12: linear bijections F_p^n -> F_p^n
    iso = 0
    basis_imgs = list(itertools.product(X.els, repeat=n))
    for imgs in basis_imgs:
        if len(X.span(imgs)) == p ** n: iso += 1
    check(f"{tag}: Exercise 12: number of isomorphisms F_p^n -> F_p^n is {gl_order(p, n)} (more than one when n > 1)",
          iso == gl_order(p, n) and (iso > 1 if n > 1 else True), f"{iso}")
check("F_2^1: the isomorphism K -> K is unique (1); F_3^1 has 2 (so 'not unique' needs n > 1 only for F_2)",
      gl_order(2, 1) == 1 and gl_order(3, 1) == 2)

print("[3] Theorem 6, Corollary 6', Exercise 16")
for p, n in SPACES:
    X = Sp(p, n)
    tag = f"F_{p}^{n}"
    t6 = True; basis_ok = True; cor = True
    for Y in X.subspaces():
        j = X.dim(Y)
        classes = {X.coset(x, Y) for x in X.els}
        if len(classes) != p ** (n - j): t6 = False
        if j == n and Y != frozenset(X.els): cor = False
        if Y == frozenset(X.els) and j != n: cor = False
        # Lax's proof: basis y_1..y_j of Y, completed by x_{j+1}..x_n; the classes of the x's form a basis of X/Y
        ys = []
        for v in sorted(Y):
            if X.indep(ys + [v]): ys.append(v)
        xs = []
        cur = list(ys)
        for v in X.els:
            if len(cur) == n: break
            if X.indep(cur + [v]): cur.append(v); xs.append(v)
        assert len(ys) == j and len(xs) == n - j
        key = lambda x: X.coset_key(x, Y)
        zero_key = key(X.zero)
        # spanning: every class is sum b_k {x_k}
        reach = set()
        for bs in itertools.product(range(p), repeat=len(xs)):
            s = X.zero
            for b, xk in zip(bs, xs): s = X.add(s, X.smul(b, xk))
            reach.add(key(s))
        if len(reach) != len(classes): basis_ok = False
        # independence: sum c_k {x_k} = {0} only for c = 0
        for cs in itertools.product(range(p), repeat=len(xs)):
            s = X.zero
            for c, xk in zip(cs, xs): s = X.add(s, X.smul(c, xk))
            if key(s) == zero_key and any(cs): basis_ok = False
    check(f"{tag}: Theorem 6: every subspace Y has p^(n - dim Y) classes, i.e. dim X/Y = n - dim Y", t6)
    check(f"{tag}: the classes of x_(j+1)..x_n span X/Y and are independent (the proof's claim)", basis_ok)
    check(f"{tag}: Corollary 6': a subspace of dimension n is the whole space", cor)

# Exercise 16 over F_3: polynomials of degree < n as coefficient vectors, vanishing at j distinct points of F_3
p, n = 3, 3
X = Sp(p, n)
ev = lambda c, t: sum(ci * pow(t, i, p) for i, ci in enumerate(c)) % p
ok16 = True
detail16 = []
for j in range(0, 4):
    for pts in itertools.combinations(range(p), j):
        Y = frozenset(c for c in X.els if all(ev(c, t) == 0 for t in pts))
        if not X.is_sub(Y): ok16 = False
        if len(Y) != p ** (n - j): ok16 = False
        if len({X.coset(x, Y) for x in X.els}) != p ** j: ok16 = False
    detail16.append(j)
check("Exercise 16 (F_3, n = 3): Y is a subspace, dim Y = n - j and dim X/Y = j for every set of j distinct points, j = 0..3", ok16)

print("[4] Theorem 7, Exercise 18, Exercise 19")
for p, n in [(2, 2), (3, 2), (2, 3), (3, 3)]:
    X = Sp(p, n)
    subs = X.subspaces()
    tag = f"F_{p}^{n}"
    full = frozenset(X.els)
    t7 = True; gen = True; interm = True; npairs = 0
    for U in subs:
        for V in subs:
            W = U & V
            S = frozenset(X.add(u, v) for u in U for v in V)
            dU, dV, dW, dS = X.dim(U), X.dim(V), X.dim(W), X.dim(S)
            if dS + dW != dU + dV: gen = False
            if S == full:
                npairs += 1
                if n != dU + dV - dW: t7 = False
                # the proof: U0 = image of U in X/W, V0 likewise; U0 and V0 meet only in the zero class,
                # U0 + V0 is all of X/W, and dim X0 = dim U0 + dim V0
                key = lambda x: X.coset_key(x, W)
                U0 = {key(u) for u in U}; V0 = {key(v) for v in V}
                allc = {key(x) for x in X.els}
                zk = key(X.zero)
                if len(U0) != len(U) // len(W): interm = False
                if len(V0) != len(V) // len(W): interm = False
                if U0 & V0 != {zk}: interm = False
                sums0 = {key(X.add(u, v)) for u in U for v in V}
                if sums0 != allc: interm = False
                if len(allc) != len(U0) * len(V0): interm = False
    check(f"{tag}: Theorem 7 on all {npairs} pairs (U, V) with U + V = X: dim X = dim U + dim V - dim(U cap V)", t7 and npairs > 0)
    check(f"{tag}: the general identity dim(U+V) + dim(U cap V) = dim U + dim V on every pair of subspaces", gen)
    check(f"{tag}: the proof's claims (|U0| = |U|/|W|, U0 cap V0 = {{0}}, U0 + V0 = X/W, |X/W| = |U0||V0|)", interm)
# Exercise 18: Cartesian sum
ok18 = True
for (p, n1, n2) in [(2, 1, 2), (3, 1, 2), (2, 2, 2)]:
    A, B = Sp(p, n1), Sp(p, n2)
    prod = list(itertools.product(A.els, B.els))
    if len(prod) != p ** (n1 + n2): ok18 = False
check("Exercise 18: the Cartesian sum F_p^n1 x F_p^n2 has p^(n1+n2) elements, i.e. dimension n1 + n2 (size check only)", ok18)
# Exercise 19: explicit isomorphism Y x X/Y -> X using a complement Z
ok19 = True; cnt19 = 0
for p, n in [(2, 2), (3, 2), (2, 3), (3, 3)]:
    X = Sp(p, n)
    subs = X.subspaces()
    for Y in subs:
        Z = None
        for cand in subs:
            sums = {X.add(y, z) for y in Y for z in cand}
            if len(sums) == len(X.els) and len(Y) * len(cand) == len(X.els):
                Z = cand; break
        classes = {X.coset(x, Y) for x in X.els}
        # each class meets Z in exactly one point
        pick = {}
        for c in classes:
            inter = [z for z in c if z in Z]
            if len(inter) != 1: ok19 = False; break
            pick[c] = inter[0]
        dom = [(y, c) for y in Y for c in classes]
        f = lambda y, c: X.add(y, pick[c])
        if len({f(y, c) for y, c in dom}) != len(X.els) or len(dom) != len(X.els): ok19 = False
        # linearity: (y, c) + (y', c') -> sum; class addition by representatives
        cl_add = lambda c, d: X.coset(X.add(next(iter(c)), next(iter(d))), Y)
        for (y, c), (y2, c2) in itertools.islice(itertools.product(dom, dom), 0, 4000):
            if f(X.add(y, y2), cl_add(c, c2)) != X.add(f(y, c), f(y2, c2)): ok19 = False
        cnt19 += 1
check(f"Exercise 19: Y x X/Y -> X, (y, class) |-> y + (the point of the class lying in a chosen complement Z), is a bijection and respects +, for all {cnt19} subspaces of the four spaces", ok19)

print("[5] the held text: Lax pp.5-11 (printed page = pdf page - 17)")
flat = lambda t: re.sub(r"\s+", " ", t).lower()
pdf = None
for c in ("~/Downloads", "~/mnt/Downloads", "."):
    q = Path(os.path.expanduser(c)) / "lax.pdf"
    if q.is_file(): pdf = q; break
if pdf is None:
    print("  SKIP: lax.pdf not found (no claim made)")
else:
    L = subprocess.run(["pdftotext", "-layout", "-f", "22", "-l", "29", str(pdf), "-"],
                       capture_output=True, text=True, timeout=150).stdout.split("\f")
    pg = lambda n: flat(L[n + 17 - 22])
    check("p.5: Exercise 10, Lemma 1, definition of basis, Lemma 2, Theorem 3",
          "exercise 10" in pg(5) and "lemma 1" in pg(5) and "lemma 2" in pg(5) and "theorem 3" in pg(5) and "basis" in pg(5))
    check("p.6: Theorem 4, Theorem 5, direct sum", "theorem 4" in pg(6) and "theorem 5" in pg(6) and "direct sum" in pg(6))
    check("p.7: Exercise 11, hyperplane, Exercise 12, isomorphic", "exercise 11" in pg(7) and "hyperplane" in pg(7) and "exercise 12" in pg(7))
    check("p.8: Theorem 6 and the quotient space", "theorem 6" in pg(8) and "quotient space" in pg(8))
    check("p.9: Corollary 6 and Exercise 16", "corollary 6" in pg(9) and "exercise 16" in pg(9))
    check("p.10: Exercise 17, Theorem 7, Cartesian sum", "exercise 17" in pg(10) and "theorem 7" in pg(10) and "cartesian sum" in pg(10))
    check("p.11: Exercise 18 and Exercise 19", "exercise 18" in pg(11) and "exercise 19" in pg(11))
print("  OCR note: lax.pdf is a scan; these checks match short phrases and may miss a page the scan garbled.")

print("[6] the Lean file")
here = Path(__file__).resolve().parent
src = (here / "BasisDimension.lean").read_text(encoding="utf-8")
rep = here / "basisdimension.axioms.txt"
code = re.sub(r"/-.*?-/", "", src, flags=re.S)
code = re.sub(r"--[^\n]*", "", code)
names = ["indep_ne_zero", "lemma1", "single_vector_not_span_plane", "control_dependent_family", "lemma2",
         "theorem3", "theorem5a", "theorem5b", "theorem6", "corollary6", "theorem7", "exercise12",
         "exercise18", "exercise19"]
for nme in names:
    check(f"theorem {nme} is declared", re.search(r"\btheorem\s+" + nme + r"\b", code) is not None)
check("no proof in the file uses sorry", re.search(r"\bsorry\b", code) is None)
if not rep.is_file():
    print("  NOT YET RUN: basisdimension.axioms.txt does not exist. The Lean file is untested.")
else:
    lines = [l for l in rep.read_text(encoding="utf-8").splitlines() if l.startswith("'Book24Basis.")]
    check("the axiom report has one line per theorem", len(lines) == len(names), f"{len(lines)} lines")
    check("no theorem line shows sorryAx", all("sorryAx" not in l for l in lines))

print("[HONESTY]")
print("  Finite-field checks are exhaustive but are checks of examples; the theorems are on the page and in the Lean file.")
print("  The Lean file is untested until the author runs it. Theorem 4, Exercises 11, 16, 17 and the non-uniqueness in Exercise 12 are not in it.")
print("  Held text: Lax only (Wiley-copyrighted, page references, nothing copied). Lax works over R or C; finite fields go beyond him.")
print()
print("0 FAIL" if not FAIL else f"{len(FAIL)} FAIL: {FAIL}")
sys.exit(1 if FAIL else 0)
