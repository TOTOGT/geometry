#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ch-escher-verify.py — companion to book7/ch-escher.html.

Six blocks, standard library only. Every number §4 and its verification box
quote is produced here, and checked against the primary source:

  B. de Smit and H. W. Lenstra Jr., "The Mathematical Structure of Escher's
  Print Gallery", Notices of the AMS 50(4), April 2003, 446-451.

  [1] The exponent alpha = (2 pi i + log 256) / (2 pi i).
  [2] gamma = exp(2 pi i log 256 / (2 pi i + log 256)), against the paper's
      printed value exp(3.1172277221 + 2.7510856371 i).
  [3] INTERNAL CONSISTENCY OF THE PAPER. p.446 states the rotation and scale
      as 157.6255960832 degrees and 22.5836845286. p.450 states gamma in
      exponential form. Those are different pages and different expressions
      of the same number; this block checks they agree.
  [4] The lattices. L_256 = 2 pi i Z + Z log 256 is rectangular; L_gamma is
      oblique. log 256 = 4 log 4 = 8 log 2 is Escher's 4^4 = 256.
  [5] Why alpha is "the easy formula": in log coordinates it is multiplication
      by alpha, and it carries 2 pi i to 2 pi i + log 256.
  [6] What Escher actually drew. |gamma| = 22.58 against the roughly 20
      measurable in his grid: the drawing is NOT perfectly conformal.

Run:  python3 ch-escher-verify.py

Principia Orthogona - Vol VII - G6 LLC - CC BY-NC-ND 4.0
"""

import cmath, math, sys

FAIL = []
def check(label, ok, detail=""):
    print(f"    {'PASS' if ok else 'FAIL'}  {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok

def close(a, b, tol):
    return abs(a - b) <= tol

TWOPII = 2j * math.pi
LOG256 = math.log(256.0)

# ── [1] ───────────────────────────────────────────────────────────────────────
print("\n[1] The exponent")
alpha = (TWOPII + LOG256) / TWOPII
print(f"    log 256                  = {LOG256!r}")
print(f"    alpha                    = {alpha!r}")
check("alpha has real part exactly 1", close(alpha.real, 1.0, 1e-15),
      f"Re = {alpha.real}")
check("alpha imaginary part = -log256/(2pi)",
      close(alpha.imag, -LOG256 / (2 * math.pi), 1e-15),
      f"Im = {alpha.imag:.10f}")

# ── [2] ───────────────────────────────────────────────────────────────────────
print("\n[2] gamma against the paper's printed exponential form")
gamma = cmath.exp(TWOPII * LOG256 / (TWOPII + LOG256))
paper_log_gamma = complex(3.1172277221, 2.7510856371)
print(f"    gamma                    = {gamma!r}")
print(f"    log gamma  (computed)    = {cmath.log(gamma)!r}")
print(f"    log gamma  (paper p.450) = {paper_log_gamma!r}")
check("log gamma matches the paper to its printed digits",
      close(cmath.log(gamma), paper_log_gamma, 5e-10),
      f"|diff| = {abs(cmath.log(gamma) - paper_log_gamma):.2e}")

# ── [3] ───────────────────────────────────────────────────────────────────────
print("\n[3] p.446 against p.450 — two pages, one number")
paper_scale_446 = 22.5836845286
paper_degrees_446 = 157.6255960832
scale = abs(gamma)
degrees = math.degrees(cmath.phase(gamma))
print(f"    |gamma|        computed  = {scale!r}")
print(f"    scale  p.446             = {paper_scale_446!r}")
print(f"    arg gamma (deg) computed = {degrees!r}")
print(f"    rotation p.446           = {paper_degrees_446!r}")
check("scale on p.446 equals |gamma| from p.450",
      close(scale, paper_scale_446, 5e-10), f"|diff| = {abs(scale-paper_scale_446):.2e}")
check("rotation on p.446 equals arg gamma from p.450",
      close(degrees, paper_degrees_446, 5e-10), f"|diff| = {abs(degrees-paper_degrees_446):.2e}")
check("the rotation is clockwise in Escher's picture, i.e. arg gamma > 0 here",
      degrees > 0, "sign convention, not a claim about the print")

# ── [4] ───────────────────────────────────────────────────────────────────────
print("\n[4] The two lattices")
print(f"    L_256   generators       = 2*pi*i = {TWOPII!r},  log 256 = {LOG256!r}")
print(f"    L_gamma generators       = 2*pi*i,  log gamma = {cmath.log(gamma)!r}")
check("L_256 is rectangular: its second generator is real",
      close(complex(LOG256, 0).imag, 0.0, 1e-15))
check("L_gamma is oblique: its second generator is not real",
      abs(cmath.log(gamma).imag) > 1.0, f"Im = {cmath.log(gamma).imag:.4f}")
check("log 256 = 4 log 4  (Escher's four studies, each a blow-up by 4)",
      close(LOG256, 4 * math.log(4.0), 1e-14))
check("log 256 = 8 log 2", close(LOG256, 8 * math.log(2.0), 1e-14))
check("4**4 == 256", 4 ** 4 == 256)

# ── [5] ───────────────────────────────────────────────────────────────────────
print("\n[5] In log coordinates the map is multiplication by alpha")
image = alpha * TWOPII
print(f"    alpha * (2 pi i)         = {image!r}")
print(f"    2 pi i + log 256         = {TWOPII + LOG256!r}")
check("alpha carries the loop generator of L_gamma to that of L_256",
      close(image, TWOPII + LOG256, 1e-12))
check("h(w) = w**alpha agrees with exp(alpha log w) on a test point",
      close(cmath.exp(alpha * cmath.log(2.7 + 1.3j)), (2.7 + 1.3j) ** alpha, 1e-12))

# ── [6] ───────────────────────────────────────────────────────────────────────
print("\n[6] What Escher actually achieved")
escher_measured = 20.0     # paper: "|gamma| is somewhat smaller than 20"
rel = abs(scale - escher_measured) / scale
print(f"    true |gamma|             = {scale:.4f}")
print(f"    Escher's grid, measured  = about {escher_measured}")
print(f"    relative shortfall       = {rel*100:.2f} %")
check("the drawing is NOT perfectly conformal", rel > 0.05,
      "the paper says so explicitly; this block refuses the stronger claim")
check("but the shortfall is under 15 %", rel < 0.15)

# ── HONESTY ───────────────────────────────────────────────────────────────────
print("""
[HONESTY] What this script establishes, and what it does not.

  ESTABLISHED. The arithmetic of de Smit-Lenstra reproduces, to the digits
  they print, from their own formulae; and their p.446 figures agree with
  their p.450 exponential form, which is an internal check of the paper that
  the paper does not print.

  NOT ESTABLISHED. Nothing here verifies that the map describes Escher's
  lithograph. That is a claim about a physical print and a measurement of its
  grid, and it rests on de Smit and Lenstra's reading, not on this script.
  The figure "about 20" for Escher's own grid is quoted from them, not
  measured here, so block [6] inherits their measurement and cannot improve
  on it. Nothing here is about the elliptic curve as an algebraic object; the
  lattice arithmetic alone does not establish the isomorphism class.
""")

print(f"{'ALL CHECKS PASSED' if not FAIL else 'FAILED: ' + ', '.join(FAIL)}")
sys.exit(1 if FAIL else 0)
