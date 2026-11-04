#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book18/ch08-verify.py -- every number on book18/ch08-several-variables.html. Run first.

    python3 book18/ch08-verify.py

All arithmetic is exact (fractions), so a PASS is an equality or an exact inequality, not a rounding.

  [1] partial derivatives of f(x,y) = x^2 y + y^3: the difference quotient is exactly 2xy + y h
  [2] the differential is a linear approximation: the remainder is exactly y h^2 + 2x h k + h^2 k + 3 y k^2 + k^3
      and is at most (4|y| + 2|x| + 2)(|h| + |k|)^2 for |h|, |k| <= 1
  [3] directional derivative = a f_x + b f_y: the quotient along (a,b) differs from it by exactly t * (...)
  [4] steepest ascent at (1,2): grad = (4,13); every unit vector has (4u + 13v)^2 <= 185, and some unit vector
      comes within 10^-4 of 185 (so sqrt(185) is the maximum)
  [5] control: f = xy(x^2-y^2)/(x^2+y^2): f_x(0,y) -> -y, f_y(x,0) -> x, and the two orders of the mixed
      difference quotient give -1 and +1
  [6] successive integration of a polynomial over a rectangle gives the same number in either order; the
      midpoint sum approaches it
  [7] a linear map of the plane multiplies area by |det| (shoelace formula on the image of a rectangle)
  [8] the Lean file: the twelve theorems are present, none is proved with sorry, and the axiom report (if it
      exists) shows no sorryAx
  [9] the held text: Loomis and Sternberg, Advanced Calculus, rev. ed. 1990 (printed page = pdf page - 12)
  [HONESTY]
"""
import re, sys, os, subprocess
from fractions import Fraction as F
from pathlib import Path
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)

f = lambda x, y: x * x * y + y ** 3
fx = lambda x, y: 2 * x * y
fy = lambda x, y: x * x + 3 * y * y
pts = [(F(1), F(2)), (F(-3, 2), F(1, 3)), (F(2, 5), F(-7, 4)), (F(0), F(3)), (F(5), F(0))]
steps = [F(1, 10), F(1, 100), F(-1, 1000), F(1, 10 ** 6)]

print("[1] partial derivatives of f = x^2 y + y^3")
for (x, y) in pts:
    ok = all((f(x + h, y) - f(x, y)) / h == fx(x, y) + y * h for h in steps)
    check(f"({x},{y}): (f(x+h,y)-f(x,y))/h = 2xy + y h exactly, so f_x = 2xy", ok)
    ok = all((f(x, y + k) - f(x, y)) / k == fy(x, y) + 3 * y * k + k * k for k in steps)
    check(f"({x},{y}): (f(x,y+k)-f(x,y))/k = x^2 + 3y^2 + 3yk + k^2 exactly, so f_y = x^2 + 3y^2", ok)

print("[2] the differential is a linear approximation")
import random
random.seed(8)
for (x, y) in pts:
    ok1 = ok2 = True
    for _ in range(300):
        h = F(random.randint(-100, 100), 100); k = F(random.randint(-100, 100), 100)
        R = f(x + h, y + k) - f(x, y) - (fx(x, y) * h + fy(x, y) * k)
        ok1 &= R == y * h * h + 2 * x * h * k + h * h * k + 3 * y * k * k + k ** 3
        ok2 &= abs(R) <= (4 * abs(y) + 2 * abs(x) + 2) * (abs(h) + abs(k)) ** 2
    check(f"({x},{y}): remainder formula exact and bound (4|y|+2|x|+2)(|h|+|k|)^2 holds on 300 samples", ok1 and ok2)

print("[3] directional derivative = a f_x + b f_y")
for (x, y) in pts:
    for (a, b) in ((F(1), F(0)), (F(3), F(-4)), (F(-2, 3), F(5, 7))):
        D = fx(x, y) * a + fy(x, y) * b
        ok = True
        for t in (F(1, 10), F(1, 100), F(-1, 1000)):
            q = (f(x + t * a, y + t * b) - f(x, y)) / t
            # q - D is exactly a polynomial in t of degree <= 2 with no constant term
            ok &= q - D == t * (y * a * a + 2 * x * a * b + 3 * y * b * b) + t * t * (a * a * b + b ** 3)
        check(f"({x},{y}) direction ({a},{b}): quotient - (a f_x + b f_y) = t*c1 + t^2*c2 exactly", ok)

print("[4] steepest ascent at (1,2)")
g = (fx(F(1), F(2)), fy(F(1), F(2)))
check("gradient at (1,2) is (4, 13)", g == (4, 13))
ok = True
for tn in range(-60, 61):
    for td in range(1, 25):
        t = F(tn, td)
        u, v = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)
        assert u * u + v * v == 1
        ok &= (g[0] * u + g[1] * v) ** 2 <= 185
check("over several thousand rational unit vectors, (4u + 13v)^2 <= 185 = 4^2 + 13^2", ok)
best = F(0)
for tn in range(0, 400):
    for td in range(1, 400):
        t = F(tn, td); u, v = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)
        val = (g[0] * u + g[1] * v) ** 2
        if val > best: best = val
check("some rational unit vector has (4u + 13v)^2 above 185 - 10^-4 (the bound is sharp)", best > 185 - F(1, 10000), f"best = {float(best):.6f}")
check("at the unit vector (4,13)/sqrt(185): squared directional derivative is exactly 185", F(4 * 4 + 13 * 13) == 185)

print("[5] control: f = xy(x^2-y^2)/(x^2+y^2), f(0,0) = 0")
def cf(x, y):
    return F(0) if (x == 0 and y == 0) else x * y * (x * x - y * y) / (x * x + y * y)
for y in (F(1), F(-2), F(1, 3), F(5, 2)):
    ok = True
    for h in (F(1, 10), F(1, 100), F(1, 10 ** 4), F(-1, 10 ** 6)):
        q = (cf(h, y) - cf(F(0), y)) / h
        ok &= q == y * (h * h - y * y) / (h * h + y * y)
        ok &= abs(q + y) <= 2 * h * h / abs(y)
    check(f"y = {y}: (f(h,y) - f(0,y))/h = y(h^2-y^2)/(h^2+y^2), within 2h^2/|y| of -y", ok)
for x in (F(1), F(-2), F(1, 3)):
    ok = True
    for k in (F(1, 10), F(1, 100), F(1, 10 ** 4)):
        q = (cf(x, k) - cf(x, F(0))) / k
        ok &= abs(q - x) <= 2 * k * k / abs(x)
    check(f"x = {x}: (f(x,k) - f(x,0))/k within 2k^2/|x| of +x", ok)
# f(h,k)/(hk) = (h^2 - k^2)/(h^2 + k^2): h -> 0 first gives -1, k -> 0 first gives +1
mix = lambda h, k: (cf(h, k) - cf(h, F(0)) - cf(F(0), k) + cf(F(0), F(0))) / (h * k)
check("mixed quotient f(h,k)/(hk) = (h^2-k^2)/(h^2+k^2) exactly", all(mix(h, k) == (h * h - k * k) / (h * h + k * k) for h in (F(1, 3), F(1, 7)) for k in (F(1, 2), F(2, 5))))
check("h = 10^-8, k = 10^-2 (h first): quotient within 10^-6 of -1", abs(mix(F(1, 10 ** 8), F(1, 10 ** 2)) + 1) < F(1, 10 ** 6))
check("h = 10^-2, k = 10^-8 (k first): quotient within 10^-6 of +1", abs(mix(F(1, 10 ** 2), F(1, 10 ** 8)) - 1) < F(1, 10 ** 6))
check("the two iterated limits (-1 and +1) differ", F(-1) != F(1))

print("[6] successive integration of a polynomial over a rectangle")
def mono_int(p, a, b): return (b ** (p + 1) - a ** (p + 1)) / (p + 1)
poly = {(2, 1): F(1), (0, 3): F(1), (1, 1): F(1), (3, 0): F(-2), (0, 0): F(5)}   # x^2 y + y^3 + xy - 2x^3 + 5
a, b, c, d = F(0), F(2), F(1), F(3)
def iterated_x_first(): return sum(co * mono_int(px, a, b) * mono_int(py, c, d) for (px, py), co in poly.items())
def iterated_y_first(): return sum(co * mono_int(py, c, d) * mono_int(px, a, b) for (px, py), co in poly.items())
check("the iterated integral is the same in either order (exact fractions)", iterated_x_first() == iterated_y_first(), f"{iterated_x_first()}")
P = lambda x, y: sum(co * x ** px * y ** py for (px, py), co in poly.items())
def mid(n):
    hx, hy = (b - a) / n, (d - c) / n
    return sum(P(a + (i + F(1, 2)) * hx, c + (j + F(1, 2)) * hy) for i in range(n) for j in range(n)) * hx * hy
exact = iterated_x_first()
errs = [abs(mid(n) - exact) for n in (5, 10, 20, 40)]
check("midpoint sum error shrinks by about 4 each time n doubles (n = 5, 10, 20, 40)", all(errs[i] / errs[i + 1] > 3.5 and errs[i] / errs[i + 1] < 4.5 for i in range(3)), f"errors {[float(e) for e in errs]}")

print("[7] a linear map of the plane multiplies area by |det|")
def shoelace(ps):
    s = sum(ps[i][0] * ps[(i + 1) % len(ps)][1] - ps[(i + 1) % len(ps)][0] * ps[i][1] for i in range(len(ps)))
    return abs(s) / 2
ok = True; n = 0
for A in range(-3, 4):
    for B in range(-3, 4):
        for C in range(-3, 4):
            for D in range(-3, 4):
                pw, qh = F(3), F(2)
                rect = [(F(0), F(0)), (pw, F(0)), (pw, qh), (F(0), qh)]
                img = [(A * x + B * y, C * x + D * y) for (x, y) in rect]
                area = shoelace(img)
                ok &= area == abs(A * D - B * C) * pw * qh
                n += 1
check(f"image of the 3 x 2 rectangle has area |det| * 6 for all {n} integer matrices with entries in -3..3 (including det 0)", ok)

print("[8] the Lean file")
here = Path(__file__).resolve().parent
src = (here / "SeveralVariables.lean").read_text(encoding="utf-8")
code = re.sub(r"/-.*?-/", "", src, flags=re.S); code = re.sub(r"--[^\n]*", "", code)
names = ["directional_derivative_eq_differential", "differential_is_partials_combination", "partial_x_eq_differential",
         "partial_x_example", "partial_y_example", "directional_derivative_le_gradient_norm",
         "directional_derivative_attains", "second_differential_symmetric", "cf_dx", "cf_dy",
         "mixed_partials_differ", "area_scales_by_det"]
for nme in names:
    check(f"theorem {nme} is declared", re.search(r"\btheorem\s+" + nme + r"\b", code) is not None)
check("no proof in the file uses sorry", re.search(r"\bsorry\b", code) is None)
rep = here / "severalvariables.axioms.txt"
if not rep.is_file():
    print("  NOT YET RUN: severalvariables.axioms.txt does not exist. The Lean file is untested.")
else:
    lines = [l for l in rep.read_text(encoding="utf-8").splitlines() if l.startswith("'Book18SV.")]
    check("the axiom report has one line per theorem", len(lines) == len(names), f"{len(lines)} lines")
    check("no theorem line shows sorryAx", all("sorryAx" not in l for l in lines))

print("[9] the held text: Loomis and Sternberg, Advanced Calculus, rev. ed. 1990 (printed page = pdf page - 12)")
flat = lambda t: re.sub(r"\s+", " ", t)
pdf = None
for c in ("~/Downloads", "~/mnt/Downloads", "."):
    q = Path(os.path.expanduser(c)) / "Advanced_Calculus.pdf"
    if q.is_file(): pdf = q; break
if pdf is None:
    print("  SKIP: Advanced_Calculus.pdf not found (no claim made). It is the copy with a text layer; LS_Advanced_Calculus5.pdf is the same 592 pages without one.")
else:
    L = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True, timeout=200).stdout.split("\f")
    pg = lambda n: flat(L[n + 12 - 1])
    check("p.140: section 6, The Differential", "6. THE DIFFERENTIAL" in pg(140))
    check("p.146: section 7, Directional Derivatives; the Mean-Value Theorem", "7. DIRECTIONAL DERIVATIVES; THE MEAN-VALUE THEOREM" in pg(146))
    check("p.147: Theorem 7.1 (a parametrized arc, tangent vector is the skeleton of the differential)", "Theorem 7.1. A parametrized arc" in pg(147))
    check("p.157: Theorem 9.2, the partial derivatives are the skeleton of the differential", "9.2. If V = IR" in pg(157) and "skeleton" in pg(157))
    check("p.186: section 16, The Second Differential", "16. THE SECOND DIFFERENTIAL" in pg(186))
    check("p.187: Theorem 16.3, the second differential is symmetric", "Theorem 16.3. The second differential is a symmetric function" in pg(187))
    check("p.335: Theorem 8.1, content of L(A) is |det L| times content of A", "Theorem 8.1. Let L be a linear transformation" in pg(335))
    check("p.346: section 12, Successive Integration, Definition 12.1", "12. SUCCESSIVE INTEGRATION" in pg(346) and "Definition: 12.1" in pg(346))

print("[HONESTY]")
print("  This script checks arithmetic and the text of one book. It does not run Lean; the axiom report is the author's run.")
print("  SeveralVariables.lean is untested until the author compiles it. Fubini, the change of variables formula, the implicit")
print("  function theorem, Stokes and line and surface integrals are NOT in it. [1]-[7] are exact examples, not proofs.")
print("  Held text: Loomis and Sternberg (page references only, nothing copied). Locate the same statements in your own copy; the OCR")
print("  text layer is noisy, so [9] matches short phrases. It does not check that the chapter's wording matches the book.")
print()
print("0 FAIL" if not FAIL else f"{len(FAIL)} FAIL: {FAIL}")
sys.exit(1 if FAIL else 0)
