#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book28/ch04-verify.py -- every number and quotation on book28/ch04-riemann-roch-and-the-letter-k.html. Run first (R24).
    python3 book28/ch04-verify.py [--downloads DIR]
  [1] Blackadar, Rosenberg (GTM 147), Dugger, Atiyah 1967: the sentences quoted, by PDF page
  [2] CP^1 by Cech cochains: the index of delta : O(U0) + O(U1) -> O(U01) is d + 1, for d = -8..8
  [3] hyperelliptic curves, genus 0..4: l(n.inf) = n - g + 1 once n >= 2g - 1, and exactly g gaps
  [4] Mathlib at the pinned revision: no Riemann-Roch, no genus
  [5] the Lean: book28/RiemannRoch.lean
  [HONESTY]
"""
import json, os, re, subprocess, sys
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
squash = lambda s: re.sub(r"\s+", "", s.replace("-\n", "")).lower()
def pages(name):
    return subprocess.run(["pdftotext", "-layout", str(dl() / name), "-"], stdout=subprocess.PIPE,
                          stderr=subprocess.DEVNULL, text=True).stdout.split("\f")

print("[1] the texts")
BL = pages("K-THEORY FOR OPERATOR ALGEBRAS Bruce Blackadar.pdf")
RO = pages("Graduate Texts in Mathematics 147.pdf")
DU = pages("A GEOMETRIC INTRODUCTION TO K-THEORY DANIEL DUGGER.pdf")
AT = pages("K-THEORY LECTURES BY NOTES BY M. F. A.TIYAH* D. W. ANDERSON.pdf")
QS = [(BL, "Blackadar", 15, "The first notions of K-theory were developed by Grothendieck in his work on the Riemann–Roch theorem in algebraic geometry"),
      (BL, "Blackadar", 15, "K-theory as a part of algebraic topology was begun by Atiyah and Hirzebruch [1961]"),
      (BL, "Blackadar", 263, "Theorem 24.1.1 (Atiyah–Singer Index Theorem)"),
      (BL, "Blackadar", 263, "Two special cases illustrate the typical content of the Index Theorem in the odd"),
      (BL, "Blackadar", 263, "and even-dimensional cases respectively"),
      (BL, "Blackadar", 263, "The Index Theorem in this case gives the Riemann–Roch Theorem"),
      (BL, "Blackadar", 263, "where d is the degree of L, defined via intersection theory"),
      (RO, "Rosenberg", 3, "Jonathan Rosenberg"),
      (RO, "Rosenberg", 10, "which motivated Grothendieck’s first work on K-theory"),
      (RO, "Rosenberg", 10, "the Riemann-Roth theorem gives a formula for the difference of the dimensions of two vector spaces"),
      (RO, "Rosenberg", 10, "Thus both involve a formal difference of two free modules"),
      (RO, "Rosenberg", 5, "K-theory in algebraic geometry is basic to Grothendieck’s approach to the Riemann-Roth problem"),
      (DU, "Dugger", 219, "Theorem 28.16 (Riemann-Roch). For any divisor D on a Riemann surface X"),
      (DU, "Dugger", 219, "The first equality, with 1 + deg(D) − g, is the classical statement"),
      (DU, "Dugger", 218, "So `(n[0]) = n + 1"),
      (AT, "Atiyah", 4, "These notes are based on the course of lectures I gave at Harvard in the fall of 1964")]
for T, who, pg, q in QS:
    check(f'{who} PDF p.{pg}: "{q[:58]}"', squash(q) in squash(T[pg - 1]))
check("Blackadar's page 263 is printed page 249", re.search(r"^\s*24\. Survey of Applications to Geometry and Topology\s+249", BL[262]) is not None)
ro = " ".join(RO)
n_roth, n_roch = len(re.findall(r"Riemann-Roth", ro)), len(re.findall(r"Riemann-Roch", ro))
check("the scan of Rosenberg reads 'Roch' as 'Roth' in its text layer", n_roth >= 5 and n_roch == 0, f"Roth {n_roth}, Roch {n_roch}")

print("[2] CP^1 by Cech cochains, in the monomial basis z^k")
def rank(M):
    M = [[Fraction(x) for x in r] for r in M]; r = 0
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
for d in range(-8, 9):
    # sections of O(d): on U0 = {z != inf}: z^k, k >= 0; on U1 = {z != 0}: z^k, k <= d; on U01: all k.
    ker = len([k for k in range(0, d + 1)])                   # f = g: monomials in both
    cok = len([k for k in range(d + 1, 0)])                   # monomials in neither
    N = 12                                                    # the same count from a matrix, window |k| <= N
    dom = [("0", k) for k in range(0, N + 1)] + [("1", k) for k in range(-N, d + 1)]
    cod = list(range(-N, N + 1))
    M = [[(1 if s == "0" else -1) if k == c else 0 for s, k in dom] for c in cod]
    r = rank(M); kerM, cokM = len(dom) - r, len(cod) - r
    rows.append((d, ker, cok, ker - cok, kerM, cokM))
print("      d  h0  h1  index  (matrix ker, coker)")
for row in rows: print("    %3d %3d %3d %5d   (%d, %d)" % row)
check("h0 - h1 = d + 1 for every d from -8 to 8", all(i == d + 1 for d, a, b, i, *_ in rows))
check("the Cech matrix on a window |k| <= 12 gives the same kernel and cokernel", all(a == km and b == cm for d, a, b, i, km, cm in rows))
check("h1 is zero exactly when d >= -1 (Serre duality: h1(O(d)) = h0(O(-2-d)))",
      all((b == 0) == (d >= -1) and b == max(0, -2 - d + 1) for d, a, b, *_ in rows))

print("[3] hyperelliptic y^2 = f(x), deg f = 2g + 1: poles at the one point over x = inf")
gaps_ok, rr_ok, tab = True, True, []
for g in range(0, 5):
    orders = sorted({2 * a + b * (2 * g + 1) for a in range(0, 40) for b in (0, 1)})   # x^a y^b
    ell = {n: len([o for o in orders if o <= n]) for n in range(0, 31)}
    gaps = [n for n in range(1, 31) if n not in orders]
    gaps_ok &= gaps == list(range(1, 2 * g, 2))
    rr_ok &= all(ell[n] == n - g + 1 for n in range(max(0, 2 * g - 1), 31))
    tab.append((g, [ell[n] for n in range(0, 11)], gaps))
for g, e, gp in tab: print(f"     g={g}: l(n.inf), n=0..10: {e}   gaps {gp}")
check("l(n.inf) = n - g + 1 for every n >= 2g - 1 (where l(K - D) = 0), g = 0..4, n <= 30", rr_ok)
check("exactly g gaps, 1, 3, ..., 2g - 1 (Weierstrass)", gaps_ok)

print("[4] Mathlib at the pinned revision")
man = json.loads((ROOT / "lake-manifest.json").read_text())
rev = next(p["rev"] for p in man["packages"] if p["name"] == "mathlib")
ML = ROOT / ".lake/packages/mathlib"
def gg(*a): return [l for l in subprocess.run(["git", "-C", str(ML), "grep", *a, rev, "--", "Mathlib"],
                                              capture_output=True, text=True).stdout.splitlines() if l]
check("no Riemann-Roch anywhere in Mathlib", not gg("-Ein", r"Riemann.?Roch"))
check("no genus of a curve", not gg("-Eiw", "genus"))
check("degreeLTEquiv is there (the space L(d.inf) on CP^1)", bool(gg("-n", "def degreeLTEquiv")))

print("[5] the Lean")
lean = (ROOT / "book28/RiemannRoch.lean").read_text(encoding="utf-8")
check("RiemannRoch.lean: finrank_degreeLT and ell_P1", re.findall(r"^theorem (\w+)", lean, re.M) == ["finrank_degreeLT", "ell_P1"])
check("no sorry in code", "sorry" not in re.sub(r"/-.*?-/|--[^\n]*", "", lean, flags=re.S))
ax = (ROOT / "book28/riemannroch.axioms.txt").read_text()
check("axiom report: both on [propext, Classical.choice, Quot.sound]", ax.count("[propext, Classical.choice, Quot.sound]") == 2)
check("lakefile builds it in lean_lib Book28", "`RiemannRoch" in (ROOT / "lakefile.lean").read_text())

print("[HONESTY]")
print("  [2] models O(d) on CP^1 by monomials on the two standard charts; that model is classical and")
print("  is assumed, not derived. [3] assumes the functions regular away from infinity are spanned by")
print("  x^a y^b with pole orders 2a + (2g+1)b, as for y^2 = f(x) with deg f odd; it counts, it does")
print("  not prove Riemann-Roch. The Lean proves dim(polynomials of degree <= d) = d + 1 only.")
print(f"\n{len(FAIL)} FAIL" + (": " + ", ".join(FAIL) if FAIL else ""))
sys.exit(1 if FAIL else 0)
