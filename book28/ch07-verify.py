#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book28/ch07-verify.py -- every number and quotation on book28/ch07-one-number-two-ways.html. Run first (R24).
    python3 book28/ch07-verify.py [--downloads DIR]
  [1] Blackadar §24.1 (Atiyah-Singer, its two examples, its generalisations) and Dugger §27: quoted, by PDF page
  [2] the analytic side on CP^n: chi(O(k)) from the cohomology table, three cases, for n = 1..8 and k = -25..25
  [3] the topological side: the Todd number, coefficient of x^n in (x/(1-e^-x))^(n+1) e^(kx), in exact fractions
  [4] the two sides agree, and both equal C(n+k, n)
  [5] the two examples of ch 3 and ch 4 as Todd numbers: the circle (no Todd class) and genus g (c1(TM) = 2 - 2g)
  [6] the Lean: book28/IndexTwoWays.lean
  [HONESTY]
"""
import os, re, subprocess, sys
from fractions import Fraction as Fr
from math import comb, factorial
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
sq = lambda s: re.sub(r"\s+", "", s.replace("-\n", "")).lower()
def pages(name):
    return subprocess.run(["pdftotext", "-layout", str(dl() / name), "-"], stdout=subprocess.PIPE,
                          stderr=subprocess.DEVNULL, text=True).stdout.split("\f")

print("[1] the texts")
BL = pages("K-THEORY FOR OPERATOR ALGEBRAS Bruce Blackadar.pdf")
DU = pages("A GEOMETRIC INTRODUCTION TO K-THEORY DANIEL DUGGER.pdf")
ZO = pages("18 LECTURES ON K-THEORY.pdf")
QS = [(BL, "Blackadar", 262, "is regarded as one of the great achievements of modern mathematics"),
      (BL, "Blackadar", 262, "the Fredholm index of an elliptic pseudodifferential operator can be calculated from purely topological data"),
      (BL, "Blackadar", 263, "the analytic index of D is defined to be"),
      (BL, "Blackadar", 263, "the topological index of D is defined as"),
      (BL, "Blackadar", 263, "Theorem 24.1.1 (Atiyah–Singer Index Theorem)"),
      (BL, "Blackadar", 263, "Two special cases illustrate the typical content of the Index Theorem in the odd"),
      (BL, "Blackadar", 263, "The Index Theorem then says that Inda (Df ) = −(winding number of f )"),
      (BL, "Blackadar", 263, "The Index Theorem in this case gives the Riemann–Roch Theorem"),
      (BL, "Blackadar", 263, "the first difficulty is to make sense of the analytic index"),
      (BL, "Blackadar", 264, "another K-group element defined in purely topological terms from the symbol of the operator"),
      (BL, "Blackadar", 264, "24.1.3. The first generalization we consider is the index theorem for families"),
      (BL, "Blackadar", 264, "which is a generalization of the previous ones"),
      (BL, "Blackadar", 264, "takes values in K 0 (Y )"),
      (BL, "Blackadar", 263, "usually the analytic index is instead interpreted as an element of a certain K-group"),
      (BL, "Blackadar", 265, "Kasparov [1984b] proved that these two indexes coincide"),
      (BL, "Blackadar", 265, "which is due to Connes and Moscovici"),
      (BL, "Blackadar", 265, "The Atiyah–Singer Index Theorem is the case B = C, and the Index Theorem for Families is the case B = C0 (Y )"),
      (BL, "Blackadar", 265, "the longitudinal index theorem for foliations of Connes and Skandalis [1984]"),
      (DU, "Dugger", 215, "Table 27.2. Cohomology groups H i (CP n ; O(k))"),
      (DU, "Dugger", 215, "Td-numX (E) = χ(X; E)"),
      (DU, "Dugger", 215, "We leave the reader to check that all three cases"),
      (DU, "Dugger", 216, "Res"),
      (ZO, "Zois", 56, "arguably the most central result in mathematics during the second half of the 20th century")]
for T, who, pg, q in QS:
    check(f'{who} PDF p.{pg}: "{q[:62]}"', sq(q) in sq(T[pg - 1]))
check("Blackadar's PDF p.262-265 are printed pp.248-251", all(str(n) in BL[262 + i - 1][:200] for i, n in enumerate((248, 249, 250, 251), 0)))

print("[2] the analytic side: chi(CP^n; O(k)) from Dugger's cohomology table")
def dimS(d, n): return comb(n + d, n) if d >= 0 else 0          # homogeneous polynomials of degree d in n+1 variables
def chi_analytic(n, k):
    if k >= 0: return dimS(k, n)                                # H^0 = S^k
    if k >= -n: return 0                                        # no cohomology at all
    return (-1) ** n * dimS(-k - (n + 1), n)                    # H^n = S^{-k-n-1}, in degree n
def betti(n, k):
    h0 = dimS(k, n) if k >= 0 else 0
    hn = dimS(-k - (n + 1), n) if k <= -(n + 1) else 0
    return h0, hn
N = range(1, 9); K = range(-25, 26)
check("cohomology of O(k) on CP^n sits in degree 0 (k >= 0) or degree n (k <= -n-1), never both, never elsewhere",
      all(not (betti(n, k)[0] and betti(n, k)[1]) for n in N for k in K))
check("the middle range -n <= k <= -1 has no cohomology at all", all(betti(n, k) == (0, 0) for n in N for k in range(-n, 0)))
print("     chi(CP^3; O(k)), k = -8..4:", [chi_analytic(3, k) for k in range(-8, 5)])

print("[3] the topological side: Td-num = coefficient of x^n in (x/(1-e^-x))^(n+1) * e^(kx), exact")
M = 12                                                          # series to x^M
def series_exp(c, deg):                                         # e^(c x) as a list of Fractions
    return [Fr(c) ** i / factorial(i) for i in range(deg + 1)]
def mul(a, b, deg):
    out = [Fr(0)] * (deg + 1)
    for i, x in enumerate(a):
        if x == 0: continue
        for j, y in enumerate(b):
            if i + j > deg: break
            out[i + j] += x * y
    return out
def inv(a, deg):                                                # 1/a, a[0] != 0
    out = [Fr(0)] * (deg + 1); out[0] = 1 / a[0]
    for n in range(1, deg + 1):
        out[n] = -sum(a[i] * out[n - i] for i in range(1, n + 1) if i < len(a)) / a[0]
    return out
# (1 - e^-x) = sum_{i>=1} (-1)^(i+1) x^i / i!
one_minus_e = [Fr(0)] + [Fr((-1) ** (i + 1), factorial(i)) for i in range(1, M + 3)]
todd1 = inv(one_minus_e[1:], M)                                  # x / (1 - e^-x) = 1 / ((1 - e^-x)/x)
print("     x/(1-e^-x) = ", " + ".join(f"({c})x^{i}" for i, c in enumerate(todd1[:5])), "+ ...")
check("the Todd series x/(1-e^-x) starts 1 + x/2 + x^2/12 + 0 x^3 - x^4/720", todd1[:5] == [1, Fr(1, 2), Fr(1, 12), 0, Fr(-1, 720)])
def todd_number(n, k):
    t = [Fr(1)] + [Fr(0)] * n
    for _ in range(n + 1): t = mul(t, todd1[:n + 1], n)
    return mul(t, series_exp(k, n), n)[n]
chi_top = {(n, k): todd_number(n, k) for n in N for k in K}
check("the topological number is an integer in all 8 x 51 cases", all(v.denominator == 1 for v in chi_top.values()))

print("[4] the two sides agree, and both are C(n+k, n)")
def binom_poly(n, k):                                            # (k+1)(k+2)...(k+n)/n!, valid for every integer k
    p = Fr(1)
    for i in range(1, n + 1): p *= Fr(k + i, i)
    return p
check("analytic = topological, all 8 x 51 pairs (n = 1..8, k = -25..25)", all(chi_analytic(n, k) == chi_top[(n, k)] for n in N for k in K))
check("both equal the polynomial (k+1)...(k+n)/n! in k, for every k, negative ones included", all(binom_poly(n, k) == chi_top[(n, k)] for n in N for k in K))
check("that polynomial vanishes at k = -1, ..., -n: the middle case", all(binom_poly(n, -j) == 0 for n in N for j in range(1, n + 1)))
check("Serre duality shape: chi(O(-k-n-1)) = (-1)^n chi(O(k))", all(chi_top[(n, -k - n - 1)] == (-1) ** n * chi_top[(n, k)] for n in N for k in range(-10, 11)) )

print("[5] the two examples of ch 3 and ch 4")
def hrr_curve(d, g):                                             # ch(L) = 1 + d [pt], Td(TM) = 1 + c1(TM)/2, c1(TM)[M] = 2 - 2g
    return d + Fr(2 - 2 * g, 2)
check("genus g, degree d: integral of ch(L) Td(TM) = d + (2 - 2g)/2 = d - g + 1 (Riemann-Roch), g = 0..6, d = -5..12",
      all(hrr_curve(d, g) == d - g + 1 for g in range(7) for d in range(-5, 13)))
check("g = 0 is the n = 1 case above: (d + 1) = todd_number(1, d)", all(hrr_curve(d, 0) == chi_top[(1, d)] for d in range(-10, 11)))
print("     (the circle has no Todd class to compute: its topological index is the winding number, ch 3)")

print("[6] the Lean")
lean = (ROOT / "book28/IndexTwoWays.lean").read_text(encoding="utf-8")
check("IndexTwoWays.lean: card_monomials, choose_zero_between, P1_count",
      re.findall(r"^theorem (\w+)", lean, re.M) == ["card_monomials", "choose_zero_between", "P1_count"])
check("no sorry in code", "sorry" not in re.sub(r"/-.*?-/|--[^\n]*", "", lean, flags=re.S))
ax = (ROOT / "book28/indextwoways.axioms.txt").read_text()
check("axiom report: 3 theorems, all within [propext, Classical.choice, Quot.sound]", ax.count("depends on axioms") == 3 and "sorryAx" not in ax)
check("lakefile builds it in lean_lib Book28", "`IndexTwoWays" in (ROOT / "lakefile.lean").read_text())

print("[HONESTY]")
print("  This chapter checks one instance of the index theorem, line bundles on CP^n, where both sides can")
print("  be computed by hand: the analytic side from Dugger's cohomology table (quoted), the topological side")
print("  from the Todd residue (computed). Agreement for n <= 8 and |k| <= 25 is a test of that instance and")
print("  not a proof of the theorem. The Lean proves only the monomial count under the analytic side.")
print("  Blackadar's Theorem 24.1.1 for pseudodifferential operators is quoted, not proved; Atiyah-Singer's")
print("  own papers (1968a, b) are not held.")
print(f"\n{len(FAIL)} FAIL" + (": " + ", ".join(FAIL) if FAIL else ""))
sys.exit(1 if FAIL else 0)
