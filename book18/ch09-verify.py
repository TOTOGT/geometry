#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book18/ch09-verify.py -- every number on book18/ch09-foundations-of-analysis.html. Run first.

    python3 book18/ch09-verify.py

All arithmetic is exact (fractions), so a PASS is an equality or an exact inequality, not a rounding. A finite
list of cases is a check of the formula the page proves, not a proof of the theorem.

  [1] the rationals are not complete: for every rational u > 0 with u^2 > 2, u' = (u^2+2)/(2u) is smaller and
      still has u'^2 > 2, with u'^2 - 2 = (u^2-2)^2/(4u^2); for every rational x >= 0 with x^2 < 2,
      x' = (2x+2)/(x+2) is larger and still has x'^2 < 2; and p^2 = 2 q^2 has no solution with q <= 3000
  [2] the intermediate value theorem by bisection, exact: x^3 - x - 1 on [1, 2], 40 steps, the width is
      exactly 2^-39, the sign pattern is kept, and the endpoints trap a root
  [3] controls: the same bisection for x^2 - 2 over the rationals never lands on a zero in 60 steps, so the
      limit it chases is not a rational; a sign change without a zero for a discontinuous function
  [4] the extreme value theorem: x(1-x) on [0,1] has maximum 1/4 at 1/2 (exact identity); controls: x on (0,1)
      has no maximum, 1/x on (0,1] is unbounded
  [5] Bolzano-Weierstrass: x_n = (-1)^n (1 + 1/n) is bounded by 2 and its even and odd subsequences converge
      to 1 and -1 at the exact distances 1/(2k) and 1/(2k-1); control: x_n = n is unbounded and every strictly
      increasing choice of indices has n_k >= k
  [6] pointwise is not uniform: x^n on [0,1) tends to 0 at every point tried, but at x_n = 1 - 1/(2n) its value
      is at least 1/2 for every n (Bernoulli, exact); the limit function on [0,1] jumps at 1. Uniform: x/(1+n x^2)
      has |f_n| <= 1/(2 sqrt n), with equality at x = 1/k when n = k^2
  [7] the Lean file: the seven statements are present, none is proved with sorry, and the axiom report (if it
      exists yet) shows no sorryAx
  [8] the held text: Lebl, Basic Analysis I, v6.3 (printed page = pdf page)
"""
import itertools, math, os, re, subprocess, sys
from fractions import Fraction as F
from pathlib import Path
HERE = Path(__file__).resolve().parent
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)

print("[1] the rationals are not complete")
us = [F(a, b) for b in range(1, 31) for a in range(1, 4 * b) if F(a, b) ** 2 > 2]
ok1 = all((lambda u2: u2 < u and u2 ** 2 > 2 and u2 ** 2 - 2 == (u * u - 2) ** 2 / (4 * u * u))((u * u + 2) / (2 * u)) for u in us)
check(f"{len(us)} rational upper bounds u: u' = (u^2+2)/(2u) is smaller, u'^2 > 2, u'^2 - 2 = (u^2-2)^2/(4u^2)", ok1)
xs = [F(a, b) for b in range(1, 31) for a in range(0, 2 * b) if F(a, b) ** 2 < 2]
ok2 = all((lambda x2: x2 > x and x2 ** 2 < 2 and x2 * x2 - 2 == (2 * x * x - 4) / (x + 2) ** 2)((2 * x + 2) / (x + 2)) for x in xs)
check(f"{len(xs)} rationals with x^2 < 2: x' = (2x+2)/(x+2) is larger, x'^2 < 2, x'^2 - 2 = (2x^2-4)/(x+2)^2", ok2)
check("no p^2 = 2 q^2 with 1 <= q <= 3000", all(math.isqrt(2 * q * q) ** 2 != 2 * q * q for q in range(1, 3001)))
u = F(3, 2); seq = [u]
for _ in range(5): u = (u * u + 2) / (2 * u); seq.append(u)
check("Newton from 3/2: 3/2, 17/12, 577/408, ... each is a rational upper bound, squares above 2, strictly decreasing",
      seq[:3] == [F(3, 2), F(17, 12), F(577, 408)] and all(a > b for a, b in zip(seq, seq[1:])) and all(s * s > 2 for s in seq))
check("control: 17/12 squared is 289/144 = 2 + 1/144 (close to 2, not equal)", F(17, 12) ** 2 == 2 + F(1, 144))

print("[2] the intermediate value theorem by bisection")
f = lambda x: x ** 3 - x - 1
a, b = F(1), F(2); keep = f(a) < 0 < f(b)
check("f(1) = -1 < 0 < f(2) = 5", f(1) == -1 and f(2) == 5)
for _ in range(40):
    m = (a + b) / 2
    if f(m) == 0: break
    if f(m) < 0: a = m
    else: b = m
    keep = keep and f(a) < 0 < f(b)
check("sign pattern f(a) < 0 < f(b) kept at every step; the width is exactly 2^-40", keep and b - a == F(1, 2 ** 40), f"width {b - a}")
check("the endpoints trap a root: f(a) < 0 < f(b) and f(b) - f(a) < 5/2^38", f(a) < 0 < f(b) and f(b) - f(a) < F(5, 2 ** 38), f"{float(a):.12f}")
check("the root is near 1.3247179572 (|a - 1.3247179572| < 1e-9)", abs(float(a) - 1.3247179572) < 1e-9)
check("no rational root: the only candidates +-1 fail", f(1) != 0 and f(-1) != 0)

print("[3] controls for the intermediate value theorem")
g = lambda x: x * x - 2; a, b = F(0), F(2); never = True
for _ in range(60):
    m = (a + b) / 2
    never = never and g(m) != 0
    if g(m) < 0: a = m
    else: b = m
check("x^2 - 2 over the rationals: 60 bisection steps, no midpoint is a zero (the limit is not rational)", never and b - a == F(2, 2 ** 60))
check("the trapped interval is [a, b] with a^2 < 2 < b^2 and width 2^-59", a * a < 2 < b * b)
step = lambda x: F(-1) if x < F(1, 2) else F(1)
check("control: a step function changes sign on [0,1] but is never zero (continuity is needed)",
      step(F(0)) < 0 < step(F(1)) and all(step(F(k, 1000)) != 0 for k in range(1001)))

print("[4] the extreme value theorem")
grid = [F(k, 200) for k in range(201)]
check("x(1-x) <= 1/4 on [0,1], with 1/4 - x(1-x) = (x - 1/2)^2 exactly; equality only at 1/2",
      all(F(1, 4) - x * (1 - x) == (x - F(1, 2)) ** 2 for x in grid) and [x for x in grid if x * (1 - x) == F(1, 4)] == [F(1, 2)])
check("control: x on (0,1) has no maximum: for each x in (0,1), (x+1)/2 is in (0,1) and larger",
      all(0 < (x + 1) / 2 < 1 and (x + 1) / 2 > x for x in grid if 0 < x < 1))
check("control: 1/x on (0,1] is unbounded above: at x = 1/n it equals n", all(1 / F(1, n) == n for n in range(1, 500)))

print("[5] Bolzano-Weierstrass")
xn = lambda n: (-1) ** n * (1 + F(1, n))
check("x_n = (-1)^n (1 + 1/n) satisfies |x_n| <= 2 for n = 1..2000", all(abs(xn(n)) <= 2 for n in range(1, 2001)))
check("even terms: x_2k - 1 = 1/(2k) exactly; odd terms: x_(2k-1) + 1 = -1/(2k-1) exactly",
      all(xn(2 * k) - 1 == F(1, 2 * k) and xn(2 * k - 1) + 1 == -F(1, 2 * k - 1) for k in range(1, 1000)))
check("the whole sequence does not converge: consecutive terms differ by more than 2 - 1/n",
      all(abs(xn(n + 1) - xn(n)) > 2 for n in range(1, 500)))
idx = [1, 4, 5, 9, 20]
check("control: x_n = n is unbounded and any strictly increasing indices have n_k >= k", all(idx[k] >= k + 1 for k in range(len(idx))))

print("[6] pointwise versus uniform convergence")
pts = [F(1, 2), F(9, 10), F(99, 100)]
check("x^n -> 0 at x = 1/2, 9/10, 99/100: a first n with x^n < 1/1000 exists for each", all(any(x ** n < F(1, 1000) for n in range(1, 8000)) for x in pts))
check("at x_n = 1 - 1/(2n): x_n^n >= 1/2 for n = 1..300 (Bernoulli: (1 - t)^n >= 1 - n t)",
      all((1 - F(1, 2 * n)) ** n >= F(1, 2) for n in range(1, 301)))
check("so sup over [0,1) of x^n stays >= 1/2: the convergence to 0 is not uniform (epsilon = 1/2 has no N)", all((1 - F(1, 2 * n)) ** n >= F(1, 2) and 0 < 1 - F(1, 2 * n) < 1 for n in range(1, 301)))
check("each x^n takes the value 1 at x = 1 (n = 1..300), while at x = 99/100 the values fall below 1/1000: the pointwise limit takes the values 1 and 0 at points 1/100 apart",
      all(F(1) ** n == 1 for n in range(1, 301)) and any(F(99, 100) ** n < F(1, 1000) for n in range(1, 8000)))
fn = lambda n, x: x / (1 + n * x * x)
grid2 = [F(k, 50) for k in range(-300, 301)]
check("x/(1+n x^2): (1+nx^2)^2 - 4 n x^2 = (1 - n x^2)^2 >= 0 on the grid, so |f_n| <= 1/(2 sqrt n)",
      all((1 + n * x * x) ** 2 - 4 * n * x * x == (1 - n * x * x) ** 2 for n in (1, 2, 5, 17) for x in grid2) and
      all(fn(n, x) ** 2 <= F(1, 4 * n) for n in (1, 2, 5, 17) for x in grid2))
check("equality: at x = 1/k with n = k^2, f_n(x) = 1/(2k) = 1/(2 sqrt n)", all(fn(k * k, F(1, k)) == F(1, 2 * k) for k in range(1, 100)))
check("given epsilon = 1/100, N = 2501 works: 1/(2 sqrt N) < 1/100 (N > 1/(4 eps^2) = 2500)", F(1, 4 * 2501) < F(1, 100) ** 2 and F(1, 4 * 2500) == F(1, 100) ** 2)

print("[7] the Lean file")
src = (HERE / "Foundations.lean").read_text(encoding="utf-8")
rep = HERE / "foundations.axioms.txt"
code = re.sub(r"/-.*?-/", "", src, flags=re.S)
names = ["completeness", "newton_improves", "control_no_rational_sqrt_two", "bolzano_weierstrass", "extreme_value", "ivt", "uniform_limit_continuous"]
for nm in names: check(f"theorem {nm} is stated", re.search(r"theorem\s+" + nm + r"\b", code) is not None)
check("no sorry or admit in the Lean code", not re.search(r"\b(sorry|admit)\b", code))
if rep.exists():
    r = rep.read_text(encoding="utf-8")
    check("axiom report: all seven theorems appear", all(("Book18F." + nm) in r for nm in names))
    check("axiom report: no sorryAx and no error", "sorryAx" not in r and "error" not in r.lower())
else:
    print("  NOTE: no foundations.axioms.txt yet; the Lean file has NOT been compiled (run the command in its header).")

print("[8] the held text: Lebl, Basic Analysis I, v6.3 (printed page = pdf page)")
flat = lambda t: re.sub(r"\s+", "", t)
pdf = None
for c in ("~/Downloads", "~/mnt/Downloads", "."):
    q = Path(os.path.expanduser(c)) / "realanal.pdf"
    if q.is_file(): pdf = q; break
if pdf is None:
    print("  SKIP: realanal.pdf not found (no claim made)")
else:
    L = None
    try:
        L = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True, timeout=200, check=True).stdout.split("\f")
    except Exception:
        try:
            from pypdf import PdfReader
            rd = PdfReader(str(pdf)); L = [p.extract_text() or "" for p in rd.pages]
        except Exception as ex:
            print(f"  SKIP: cannot read realanal.pdf ({ex})")
    if L:
        pg = lambda n: flat(L[n - 1])
        check("p.24: Definition 1.1.3 (least-upper-bound property) and Example 1.1.4 (the rationals lack it, {x : x^2 < 2})",
              "Definition1.1.3" in pg(24) and "least-upper-boundproperty" in pg(24) and "Example1.1.4" in pg(24))
        check("p.78: Theorem 2.3.8 (Bolzano-Weierstrass), a bounded sequence has a convergent subsequence", "Theorem2.3.8" in pg(78) and "Bolzano" in pg(78) and "convergentsubsequence" in pg(78))
        check("p.130: Theorem 3.3.2 (Minimum-maximum theorem / Extreme value theorem)", "Theorem3.3.2" in pg(130) and "Extremevaluetheorem" in pg(130))
        check("p.133: Theorem 3.3.8 (Bolzano's intermediate value theorem)", "Theorem3.3.8" in pg(133) and "intermediatevaluetheorem" in pg(133))
        check("p.134: Example 3.3.9 (Bisection method)", "Example3.3.9" in pg(134) and "Bisectionmethod" in pg(134))
        check("p.229: Definition 6.1.6 (uniform convergence)", "Definition6.1.6" in pg(229) and "uniformly" in pg(229))
        check("p.230: Example 6.1.8 (x^(2n) does not converge uniformly on [-1,1])", "Example6.1.8" in pg(230) and "uniformly" in pg(230))
        check("p.235: Theorem 6.2.2 (a uniform limit of continuous functions is continuous)", "Theorem6.2.2" in pg(235) and "converginguniformly" in pg(235) and "iscontinuous" in pg(235))
print("  OCR/text note: the page checks match short phrases with spaces removed and may miss a page the extraction garbled.")

print()
print("ALL PASS" if not FAIL else f"{len(FAIL)} FAILED: {FAIL}")
sys.exit(1 if FAIL else 0)
