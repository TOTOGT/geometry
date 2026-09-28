#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book28/ch05-verify.py -- every number and quotation on book28/ch05-the-space-of-fredholm-operators.html. Run first (R24).
    python3 book28/ch05-verify.py [--downloads DIR]
  [1] Atiyah, K-Theory (1967), Appendix; Zois Part II Lecture 3: the sentences quoted, by PDF page
  [2] kernels jump, the index does not: a family T(t) : Q^3 -> Q^2, and Atiyah's fixed subspace V
  [3] Atiyah's two inequalities for kernels and cokernels of a product, on 400 random matrices (exact)
  [4] the Whitehead lemma: a path of invertible matrices from diag(U, U^-1) to the identity (numerical)
  [5] Mathlib at the pinned revision: no Fredholm operators, no Kuiper theorem
  [6] the Lean: book28/FredholmSpace.lean
  [HONESTY]
"""
import json, os, random, re, subprocess, sys
from fractions import Fraction as Fr
from pathlib import Path
import numpy as np
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
sq = lambda s: re.sub(r"\s+", "", s.replace("-\n", "")).lower()
def pages(name):
    return subprocess.run(["pdftotext", "-layout", str(dl() / name), "-"], stdout=subprocess.PIPE,
                          stderr=subprocess.DEVNULL, text=True).stdout.split("\f")

print("[1] the texts")
AT = pages("K-THEORY LECTURES BY NOTES BY M. F. A.TIYAH* D. W. ANDERSON.pdf")
ZO = pages("18 LECTURES ON K-THEORY.pdf")
QS = [(AT, "Atiyah", 158, "The space of Fredholm operators. In this appendix we shall"),
      (AT, "Atiyah", 158, "give a Hilbert space interpretation"),
      (AT, "Atiyah", 158, "in connection with the theory of the index for elliptic operators"),
      (AT, "Atiyah", 158, "is called the index of T"),
      (AT, "Atiyah", 158, "These results have been obtained independently by K. Janich"),
      (AT, "Atiyah", 158, "(Bonn dissertation 1964)"),
      (AT, "Atiyah", 159, "is in fact the index which explains our use of the word in the more general context"),
      (AT, "Atiyah", 160, "is a classifying or representing"),
      (AT, "Atiyah", 163, "index T = [H/V] - [H/T(V)]"),
      (ZO, "Zois", 69, "Unfortunately these might not be vector bundles since the dimensions may jump"),
      (ZO, "Zois", 70, "is a weak homotopy equivalence"),
      (ZO, "Zois", 71, "The group GLH is contractible (this is difficult to prove)"),
      (ZO, "Zois", 71, "Whitehead Lemma")]
for T, who, pg, q in QS:
    check(f'{who} PDF p.{pg}: "{q[:60]}"', sq(q) in sq(T[pg - 1]))
check("Atiyah's PDF p.158 is printed p.153 (the Appendix)", re.match(r"\s*153\.", AT[157]) is not None)
check("p.154's inequality, as the scan's text layer has it: 'dim Ker TS < dirn Ker T + dim Ker S' (≤ read as <, 'dim' as 'dirn')",
      sq("dim Ker TS < dirn Ker T + dim Ker S") in sq(AT[158]))

print("[2] kernels jump, the index does not: T(t) = [[t,0,0],[0,1,0]] : Q^3 -> Q^2")
def rank(M):
    M = [[Fr(x) for x in r] for r in M]; r = 0
    for c in range(len(M[0]) if M else 0):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                q = M[i][c] / M[r][c]; M[i] = [a - q * b for a, b in zip(M[i], M[r])]
        r += 1
    return r
rows = []
for t in [Fr(-2), Fr(-1), Fr(-1, 2), Fr(0), Fr(1, 3), Fr(1), Fr(5)]:
    Tm = [[t, 0, 0], [0, 1, 0]]
    r = rank(Tm); ker, cok = 3 - r, 2 - r
    # Atiyah's choice V = span(e2): V meets Ker T(t) in 0 for every t; index = dim H/V - dim(Q^2 / T(V))
    TV = [[Tm[0][1]], [Tm[1][1]]]                         # T(e2)
    inter0 = (Tm[0][1], Tm[1][1]) != (0, 0)                   # T(e2) != 0, so V ∩ Ker T(t) = 0
    atiyah = (3 - 1) - (2 - rank(TV))
    rows.append((t, ker, cok, ker - cok, inter0, atiyah))
for t, a, b, i, v, at in rows: print(f"     t = {str(t):>5}: ker {a}, coker {b}, index {i};  V ∩ Ker = 0: {v};  dim H/V - dim H'/T(V) = {at}")
check("dim Ker jumps from 1 to 2 at t = 0, and dim Coker from 0 to 1", {(a, b) for _, a, b, *_ in rows} == {(1, 0), (2, 1)})
check("the index is 1 for every t", all(r[3] == 1 for r in rows))
check("Atiyah's construction with the fixed V = span(e2) gives 1 for every t, with no jump", all(r[4] and r[5] == 1 for r in rows))

print("[3] Atiyah's inequalities for a product TS, on random matrices over Q")
random.seed(5)
ok_k = ok_c = True; n = 0
for _ in range(400):
    a, b, c = (random.randint(1, 5) for _ in range(3))           # S : Q^a -> Q^b, T : Q^b -> Q^c
    S = [[Fr(random.choice([0, 0, 1, -1, 2])) for _ in range(a)] for _ in range(b)]
    T = [[Fr(random.choice([0, 0, 1, -1, 2])) for _ in range(b)] for _ in range(c)]
    TS = [[sum((T[i][l] * S[l][j] for l in range(b)), Fr(0)) for j in range(a)] for i in range(c)]
    kS, kT, kTS = a - rank(S), b - rank(T), a - rank(TS)
    cS, cT, cTS = b - rank(S), c - rank(T), c - rank(TS)
    ok_k &= kTS <= kT + kS; ok_c &= cTS <= cT + cS
    assert (kTS - cTS) == (kT - cT) + (kS - cS)                # and the index adds
    n += 1
check(f"dim Ker TS <= dim Ker T + dim Ker S, all {n}", ok_k)
check(f"dim Coker TS <= dim Coker T + dim Coker S, all {n}", ok_c)
check(f"…and Ind TS = Ind T + Ind S, all {n}", True)

print("[4] the Whitehead lemma: diag(U, U^-1) ~ identity through invertible matrices")
rng = np.random.default_rng(1)
worst = []
for trial in range(20):
    m = 3
    U = rng.normal(size=(m, m)) + 1j * rng.normal(size=(m, m))
    Ui = np.linalg.inv(U); I = np.eye(m); Z = np.zeros((m, m))
    A = np.block([[U, Z], [Z, I]]); B = np.block([[I, Z], [Z, Ui]])
    def R(th): return np.block([[np.cos(th) * I, -np.sin(th) * I], [np.sin(th) * I, np.cos(th) * I]])
    path = [A @ R(th) @ B @ R(th).T for th in np.linspace(0, np.pi / 2, 201)]
    start_ok = np.allclose(path[0], np.block([[U, Z], [Z, Ui]]))
    end_ok = np.allclose(path[-1], np.eye(2 * m))
    dets = [abs(np.linalg.det(P)) for P in path]
    worst.append((start_ok, end_ok, min(dets), max(dets)))
check("20 random U in GL3(C): the path starts at diag(U, U^-1) and ends at the identity",
      all(s and e for s, e, *_ in worst))
check("|det| = 1 along every path (201 points each): it never leaves the invertibles",
      all(abs(lo - 1) < 1e-9 and abs(hi - 1) < 1e-9 for *_, lo, hi in worst))

print("[5] Mathlib at the pinned revision")
man = json.loads((ROOT / "lake-manifest.json").read_text())
rev = next(p["rev"] for p in man["packages"] if p["name"] == "mathlib")
ML = ROOT / ".lake/packages/mathlib"
def gg(*a): return [l for l in subprocess.run(["git", "-C", str(ML), "grep", *a, rev, "--", "Mathlib"],
                                              capture_output=True, text=True).stdout.splitlines() if l]
check("no Fredholm operator is defined", not gg("-En", r"^(public )?(noncomputable )?(def|structure|class|abbrev) \S*[Ff]redholm"))
check("no statement that the invertibles of Hilbert space are contractible (searched for its usual name, Kuiper)", not gg("-n", "Kuiper"))
kt = gg("-Eil", r"K-theory|KTheory")
check("no K-theory: the only file mentioning it is QuadraticForm/Dual.lean", kt == [f"{rev}:Mathlib/LinearAlgebra/QuadraticForm/Dual.lean"], str(kt))

print("[6] the Lean")
lean = (ROOT / "book28/FredholmSpace.lean").read_text(encoding="utf-8")
check("FredholmSpace.lean: rank_ker_comp_le and every_integer_is_an_index",
      re.findall(r"^theorem (\w+)", lean, re.M) == ["rank_ker_comp_le", "every_integer_is_an_index"])
check("no sorry in code", "sorry" not in re.sub(r"/-.*?-/|--[^\n]*", "", lean, flags=re.S))
ax = (ROOT / "book28/fredholmspace.axioms.txt").read_text()
check("axiom report: both on [propext, Classical.choice, Quot.sound]", ax.count("[propext, Classical.choice, Quot.sound]") == 2)
check("lakefile builds it in lean_lib Book28", "`FredholmSpace" in (ROOT / "lakefile.lean").read_text())

print("[HONESTY]")
print("  [2] and [3] are exact but finite-dimensional: they show the bookkeeping Atiyah's proof relies")
print("  on, not his theorem [X, F] = K(X), which needs Hilbert space, compact X and homotopy and is")
print("  quoted, not proved. [4] is floating point on 20 random 3x3 matrices. The Lean proves the kernel")
print("  inequality in general and the cokernel one not at all ([3] checks it on matrices).")
print(f"\n{len(FAIL)} FAIL" + (": " + ", ".join(FAIL) if FAIL else ""))
sys.exit(1 if FAIL else 0)
