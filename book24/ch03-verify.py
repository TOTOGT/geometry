#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book24/ch03-verify.py -- every check behind book24/ch03-vector-spaces.html. Run first.

    python3 book24/ch03-verify.py

All checks over finite fields are exhaustive (every element, every pair or triple), so a PASS is a
statement about the whole finite structure, not a sample.

  [1] F_p^n satisfies the nine vector-space axioms (Lax (1)-(9)), p = 2, 3, n = 2
  [2] Lax's quotient example: in F_3^4 modulo the vectors whose first two components are zero,
      x ~ x' iff the first two components agree; there are 3^2 classes
  [3] intersection, sum and {0} of subspaces of F_3^3 are subspaces
  [4] congruence modulo a subspace is an equivalence relation, and addition and scalar
      multiplication respect it (the quotient operations are well defined), F_3^3
  [5] controls: a set that is not a subspace breaks transitivity (rationals, F_3^2)
  [6] the held text: Lax, Linear Algebra and Its Applications, 2nd ed. (printed page = pdf page - 17)
  [7] the Lean file: the twelve theorems are present, none uses sorry, and the axiom report
      (if it exists yet) shows no sorryAx
"""
import itertools, os, re, subprocess, sys
from fractions import Fraction as F
from pathlib import Path

FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  [{detail}]" if detail else ""))
    if not ok: FAIL.append(label)

# ---- finite vector spaces F_p^n -------------------------------------------------------------
def space(p, n):
    els = list(itertools.product(range(p), repeat=n))
    add = lambda x, y: tuple((a + b) % p for a, b in zip(x, y))
    smul = lambda k, x: tuple((k * a) % p for a in x)
    neg = lambda x: tuple((-a) % p for a in x)
    return els, add, smul, neg

def span(gens, p, n):
    els, add, smul, _ = space(p, n)
    S = {tuple([0] * n)}
    changed = True
    while changed:
        changed = False
        for s in list(S):
            for g in gens:
                for k in range(p):
                    t = add(s, smul(k, g))
                    if t not in S: S.add(t); changed = True
    return S

def is_sub(S, p, n):
    _, add, smul, _ = space(p, n)
    return (tuple([0] * n) in S and all(add(x, y) in S for x in S for y in S)
            and all(smul(k, x) in S for k in range(p) for x in S))

print("[1] the nine axioms on F_p^2")
for p in (2, 3):
    els, add, smul, neg = space(p, 2)
    z = (0, 0)
    ok = True
    ok &= all(add(x, y) == add(y, x) for x in els for y in els)                        # (2)
    ok &= all(add(x, add(y, w)) == add(add(x, y), w) for x in els for y in els for w in els)  # (3)
    ok &= all(add(x, z) == x for x in els)                                                # (4)
    ok &= all(add(x, neg(x)) == z for x in els)                                           # (5)
    ok &= all(smul(k, smul(a, x)) == smul(k * a % p, x) for x in els for k in range(p) for a in range(p))  # (6)
    ok &= all(smul(k, add(x, y)) == add(smul(k, x), smul(k, y)) for x in els for y in els for k in range(p))  # (7)
    ok &= all(smul((a + b) % p, x) == add(smul(a, x), smul(b, x)) for x in els for a in range(p) for b in range(p))  # (8)
    ok &= all(smul(1, x) == x for x in els)                                               # (9)
    ok &= all(smul(0, x) == z for x in els)                                               # (10)
    ok &= all(smul(p - 1, x) == neg(x) for x in els)                                      # (-1)x = -x
    check(f"p = {p}: axioms (2)-(9), and the deductions 0x = 0 and (-1)x = -x, hold on all of F_{p}^2", ok)
    zeros = [w for w in els if all(add(x, w) == x for x in els)]
    check(f"p = {p}: the zero of addition is unique (Lax Exercise 1)", zeros == [z])

print("[2] Lax's quotient example")
p, n = 3, 4
els, add, smul, neg = space(p, n)
Y = {x for x in els if x[0] == 0 and x[1] == 0}
sub = lambda x, y: add(x, neg(y))
check("Y = vectors with first two components zero is a subspace of F_3^4", is_sub(Y, p, n))
check("x ~ x' (x - x' in Y) iff the first two components agree, all 81 x 81 pairs",
      all((sub(x, y) in Y) == (x[:2] == y[:2]) for x in els for y in els))
classes = {frozenset(y for y in els if sub(x, y) in Y) for x in els}
check("the number of congruence classes is 3^2 = 9", len(classes) == 9, f"{len(classes)} classes")
check("two classes are identical or disjoint (Lax Exercise 14)",
      all(a == b or not (a & b) for a in classes for b in classes))

print("[3] subspaces in F_3^3")
p, n = 3, 3
els, add, smul, neg = space(p, n)
Ys = span([(1, 0, 0), (0, 1, 0)], p, n)
Zs = span([(0, 1, 0), (0, 0, 1)], p, n)
check("Y = span(e1, e2) and Z = span(e2, e3) are subspaces", is_sub(Ys, p, n) and is_sub(Zs, p, n))
check("Y intersect Z is a subspace (Exercise 7)", is_sub(Ys & Zs, p, n), f"{len(Ys & Zs)} elements")
sumYZ = {add(y, z) for y in Ys for z in Zs}
check("Y + Z is a subspace (Exercise 6)", is_sub(sumYZ, p, n), f"{len(sumYZ)} elements")
check("{0} is a subspace (Exercise 8)", is_sub({(0, 0, 0)}, p, n))
check("illustration of Theorem 7 (not a proof): |Y+Z| |Y∩Z| = |Y| |Z|", len(sumYZ) * len(Ys & Zs) == len(Ys) * len(Zs))

print("[4] congruence in F_3^3")
for name, gens in (("a line", [(1, 1, 0)]), ("a plane", [(1, 0, 0), (0, 1, 1)])):
    Yc = span(gens, p, n)
    C = lambda x, y: add(x, neg(y)) in Yc
    check(f"modulo {name} ({len(Yc)} elements): reflexive", all(C(x, x) for x in els))
    check(f"modulo {name}: symmetric", all((not C(x, y)) or C(y, x) for x in els for y in els))
    check(f"modulo {name}: transitive", all((not (C(x, y) and C(y, w))) or C(x, w) for x in els for y in els for w in els))
    check(f"modulo {name}: x1~x2, z1~z2 implies x1+z1 ~ x2+z2 (Exercise 15)",
          all((not (C(x1, x2) and C(z1, z2))) or C(add(x1, z1), add(x2, z2))
              for x1 in els for x2 in els for z1 in els for z2 in els))
    check(f"modulo {name}: x1~x2 implies k x1 ~ k x2",
          all((not C(x1, x2)) or C(smul(k, x1), smul(k, x2)) for x1 in els for x2 in els for k in range(p)))
    nc = len({frozenset(y for y in els if C(x, y)) for x in els})
    check(f"modulo {name}: number of classes is 3^(3 - dim) (illustration of Theorem 6, which is chapter 4)",
          nc == len(els) // len(Yc), f"{nc} classes")

print("[5] controls")
Yq = {F(0), F(1)}
Cq = lambda x, y: (x - y) in Yq
check("Y = {0, 1} in the rationals is not a subspace (1 + 1 = 2 not in Y)", F(1) + F(1) not in Yq)
check("so congruence mod {0, 1} is not transitive: 2 ~ 1, 1 ~ 0, but 2 !~ 0",
      Cq(F(2), F(1)) and Cq(F(1), F(0)) and not Cq(F(2), F(0)))
els2, add2, smul2, neg2 = space(3, 2)
Bad = {(0, 0), (1, 0)}
Cb = lambda x, y: add2(x, neg2(y)) in Bad
check("Y = {(0,0),(1,0)} in F_3^2 is not a subspace", not is_sub(Bad, 3, 2))
check("and congruence mod it fails transitivity somewhere",
      any(Cb(x, y) and Cb(y, w) and not Cb(x, w) for x in els2 for y in els2 for w in els2))

print("[6] the held text: Lax (printed page = pdf page - 17)")
flat = lambda t: re.sub(r"\s+", " ", t).lower()
pdf = None
for c in ("~/Downloads", "~/mnt/Downloads", "."):
    q = Path(os.path.expanduser(c)) / "lax.pdf"
    if q.is_file(): pdf = q; break
if pdf is None:
    print("  SKIP: lax.pdf not found (no claim made)")
else:
    L = subprocess.run(["pdftotext", "-layout", "-f", "18", "-l", "30", str(pdf), "-"],
                       capture_output=True, text=True, timeout=150).stdout.split("\f")
    pg = lambda n: flat(L[n + 17 - 18])
    check("p.2: Exercise 1, the zero of vector addition is unique", "zero of vector addition is unique" in pg(2))
    check("p.3: (-1)x = -x is deduced from the axioms", "(-1)x = -x" in pg(3) or "(-1)x=-x" in pg(3))
    check("p.4: subspace, sum Y + Z, intersection, trivial subspace",
          "definition. a subset" in pg(4) and "the sum of two subsets" in pg(4) and "trivial subspace" in pg(4))
    check("p.7: congruence modulo a subspace is an equivalence relation", "congruent modulo" in pg(7) and "equivalence relation" in pg(7))
    check("p.8: representatives (Exercise 15) and the quotient space X/Y", "choice of representatives" in pg(8) and "quotient space" in pg(8))
    check("p.8: Theorem 6, dim Y + dim(X/Y) = dim X (stated in chapter 4, not proved here)", "theorem 6" in pg(8))
print("  OCR note: lax.pdf is a scan; these checks match short phrases and may miss a page the scan garbled.")

print("[7] the Lean file")
here = Path(__file__).resolve().parent
src = (here / "VectorSpace.lean").read_text(encoding="utf-8")
rep = here / "vectorspace.axioms.txt"
code = re.sub(r"/-.*?-/", "", src, flags=re.S)
code = re.sub(r"--[^\n]*", "", code)
names = ["zero_unique", "zero_smul_axioms", "neg_one_smul_eq_neg", "inter_isSub", "sum_isSub", "trivial_isSub",
         "cong_refl", "cong_symm", "cong_trans", "cong_add", "cong_smul", "control_cong_not_trans"]
for nme in names:
    check(f"theorem {nme} is declared", re.search(r"\btheorem\s+" + nme + r"\b", code) is not None)
check("no proof in the file uses sorry", re.search(r"\bsorry\b", code) is None)
if not rep.is_file():
    print("  NOT YET RUN: vectorspace.axioms.txt does not exist.")
else:
    lines = [l for l in rep.read_text(encoding="utf-8").splitlines() if l.startswith("'Book24VS.")]
    check("the axiom report has one line per theorem", len(lines) == len(names), f"{len(lines)} lines")
    check("no theorem line shows sorryAx", all("sorryAx" not in l for l in lines))

print("[HONESTY]")
print("  Finite-field checks are exhaustive but are checks of examples; the theorems are in the page and the Lean file.")
print("  The Lean file was compiled by the author (see vectorspace.axioms.txt). Held text: Lax only (Wiley-copyrighted, page references, nothing copied).")
print("  Fields beyond the reals and complexes, and finite fields in particular, go beyond Lax, who restricts to R or C.")
print()
print("0 FAIL" if not FAIL else f"{len(FAIL)} FAIL: {FAIL}")
sys.exit(1 if FAIL else 0)
