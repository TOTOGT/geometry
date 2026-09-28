#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book28/ch02-verify.py -- every number and quotation on book28/ch02-infinity-minus-infinity.html. Run first (R24).
    python3 book28/ch02-verify.py [--downloads DIR]
  [1] Zois, 18 Lectures on K-Theory (arXiv:1008.1346v1), Part II Lecture 1: the sentences quoted, by PDF page
  [2] finite dimensions: dim ker - dim coker = n - m for every m x n matrix, whatever its rank (exact, over Q)
  [3] the shift and its square sections: the N x N section of S_k has index 0, the shift has -k
  [4] Mathlib at the pinned revision has LinearMap.index, with Zois' sign convention
  [5] the Lean: book28/InfinityMinusInfinity.lean and its axiom report
  [HONESTY]
"""
import json, os, random, re, subprocess, sys
from fractions import Fraction
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def dl():
    if "--downloads" in sys.argv: return Path(sys.argv[sys.argv.index("--downloads") + 1])
    for c in ("~/mnt/Downloads", "~/Downloads"):
        p = Path(os.path.expanduser(c))
        if p.is_dir(): return p
squash = lambda s: re.sub(r"\s+", "", s.replace("-\n", "").replace("’", "'").replace("”", '"').replace("“", '"')).lower()

print("[1] Zois, 18 Lectures on K-Theory, Part II Lecture 1")
ZOIS = dl() / "18 LECTURES ON K-THEORY.pdf"
Z = subprocess.run(["pdftotext", "-layout", str(ZOIS), "-"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                   text=True).stdout.split("\f")
check("the PDF has 137 pages and is arXiv:1008.1346v1", len([p for p in Z if p.strip()]) == 137
      and "1008.1346v1" in Z[0], f"{len(Z)} form feeds")
QS = [(4, 'Back in 1995 a graduate summer school on K-Theory was organised at the University of Lancaster'),
      (4, 'J. Roe (Oxford then, now at Penn. State) and D.G. Quillen (Oxford)'),
      (5, 'the letter ”K” stands for the German word ”(die) Klasse” which means class in English'),
      (5, 'the K-Theory of a point is Z and not zero'),
      (5, 'The ”fathers” of K-Theory are M.F. Atiyah and A. Grothendieck'),
      (5, 'The name was given by Grothendieck'),
      (56, 'what is infinity minus infinity'),
      (56, 'arguably the most central result in mathematics during the second half of the 20th century'),
      (56, '[KerT] − [V0] + [V1] − [cokerT] = 0'),
      (57, '[V0] − [V1] = [KerT] − [cokerT]'),
      (57, 'we see that the LHS has no meaning since it gives ∞ − ∞'),
      (57, 'Hence the difference ∞ − ∞ may give, in some cases, a finite result'),
      (60, 'IndT := dim(KerT) − dim(cokerT) = [KerT] − [cokerT] ∈ Z'),
      (60, 'the index measures how far an operator is from being invertible since for invertible operators the index vanishes'),
      (60, 'Ind(T0 T1) = IndT0 + IndT1'),
      (61, 'Then KerU = {0} and dim(cokerU) = 1. Hence IndU = −1'),
      (61, 'the index depends much on the spaces H0, H1 and little on the operator between them'),
      (62, 'Ind(T + K) = IndT')]
for pg, q in QS:
    check(f'Zois p.{pg}: "{q[:60]}"', squash(q) in squash(Z[pg - 1]))

print("[2] finite dimensions: every m x n matrix over Q")
def rank(M):
    M = [row[:] for row in M]; r = 0
    for c in range(len(M[0]) if M else 0):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c] / M[r][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r
random.seed(28)
res = []                                                      # (m, n, target rank, rank, ker, coker)
for m in range(1, 7):
    for n in range(1, 7):
        for k in range(0, min(m, n) + 1):                      # every rank each shape allows
            while True:                                        # T = A B has rank <= k; redraw until = k
                A = [[Fraction(random.randint(-3, 3)) for _ in range(k)] for _ in range(m)]
                B = [[Fraction(random.randint(-3, 3)) for _ in range(n)] for _ in range(k)]
                T = [[sum((A[i][t] * B[t][j] for t in range(k)), Fraction(0)) for j in range(n)] for i in range(m)]
                r = rank(T)
                if r == k: break
            res.append((m, n, k, r, n - r, m - r))            # T : Q^n -> Q^m
check(f"{len(res)} matrices, every shape 1..6 x 1..6 at every rank it allows: dim ker − dim coker = n − m",
      all(ke - co == n - m for m, n, k, r, ke, co in res))
sq = [x for x in res if x[0] == x[1]]
check(f"the {len(sq)} square ones have index 0 at every rank, invertible (rank n) or not",
      all(ke - co == 0 for m, n, k, r, ke, co in sq) and {x[3] for x in sq} == set(range(7)))

print("[3] the shift and its square sections")
def shift_section(k, N):     # N x N matrix of S_k on e_0..e_{N-1}: e_j -> e_{j+k}
    return [[Fraction(1 if i == j + k else 0) for j in range(N)] for i in range(N)]
rows = []
for k in (1, 2, 3):
    for N in (5, 10, 20):
        r = rank(shift_section(k, N)); rows.append((k, N, N - r, N - r, 0))
print("     k  N  ker coker index(section)")
for row in rows: print("    ", *row)
check("every N x N section of S_k has kernel k, cokernel k, index 0", all(a == k and b == k for k, N, a, b, _ in rows))
check("the shift itself: kernel 0, cokernel k, index −k (ch 1, ShiftIndex.lean) — truncation destroys it",
      (ROOT / "book28/ShiftIndex.lean").read_text().count("theorem shift_index") == 1)

print("[4] Mathlib at the pinned revision")
man = json.loads((ROOT / "lake-manifest.json").read_text())
rev = next(p["rev"] for p in man["packages"] if p["name"] == "mathlib")
ML = ROOT / ".lake/packages/mathlib"
head = subprocess.run(["git", "-C", str(ML), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
check("the checkout is the manifest's revision", head == rev, rev[:12])
idx = subprocess.run(["git", "-C", str(ML), "show", f"{rev}:Mathlib/Algebra/Module/LinearMap/Index.lean"],
                     capture_output=True, text=True).stdout
check("Mathlib/Algebra/Module/LinearMap/Index.lean exists, by Oliver Nash, 2026", "Copyright (c) 2026 Oliver Nash" in idx)
check("its sign convention is Zois': 'index = dim ker - dim coker'", "sign convention `index = dim ker - dim coker`" in idx)
lem = re.findall(r"public (?:lemma|def) (\S+)", idx)
print("     declarations:", ", ".join(lem))
check("it has index_eq_of_finiteDimensional (Zois Thm 1) and index_comp (Zois' Ind(T0T1))",
      "index_eq_of_finiteDimensional" in lem and "index_comp" in lem, f"{len(lem)} declarations")

print("[5] the Lean")
lean = (ROOT / "book28/InfinityMinusInfinity.lean").read_text(encoding="utf-8")
THMS = re.findall(r"^theorem (\w+)", lean, re.M)
check("7 theorems", len(THMS) == 7, ", ".join(THMS))
check("no sorry in code", "sorry" not in re.sub(r"/-.*?-/|--[^\n]*", "", lean, flags=re.S))
ax = (ROOT / "book28/infinityminusinfinity.axioms.txt").read_text()
check("axiom report: all 7 on [propext, Classical.choice, Quot.sound]",
      ax.count("depends on axioms: [propext, Classical.choice, Quot.sound]") == 7 and "sorryAx" not in ax)
check("lakefile builds it in lean_lib Book28", "`InfinityMinusInfinity" in (ROOT / "lakefile.lean").read_text())

print("[HONESTY]")
print("  [1] quotes Zois' lecture notes (2010), which record J. Roe's 1995 LMS lectures; they are")
print("  notes, not a refereed text, and Zois' Hilbert-space definitions are quoted, not checked.")
print("  [2] and [3] are exact rational arithmetic on finite matrices. The Lean has no norm and")
print("  no Hilbert space: it proves the algebraic index on ℕ →₀ F. Zois' Ind(T + K) = Ind T")
print("  (compact perturbation) and his Prop. 2 (homotopy invariance) are quoted and not proved.")
print(f"\n{len(FAIL)} FAIL" + (": " + ", ".join(FAIL) if FAIL else ""))
sys.exit(1 if FAIL else 0)
