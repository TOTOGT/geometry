#!/usr/bin/env python3
"""
ch-turing-verify.py -- every number on book7/ch-turing.html.

Model: Schnakenberg, u_t = gamma(a - u + u^2 v) + lap u, v_t = gamma(b - u^2 v) + d lap v,
with a = 0.1, b = 0.9, gamma = 1.

Blocks:
  [1] the steady state and the Jacobian printed on the page
  [2] conditions 1 and 2 -- the reaction alone is stable
  [3] condition 3 -- the d > 1.25 bound
  [4] condition 4 -- the threshold d_c = 8.567627
  [5] the selected wavenumber k_c^2 = 0.341641
  [6] the three growth rates quoted at 0.98 d_c, d_c, 1.02 d_c
  [7] below d_c EVERY wavenumber decays -- the claim the page actually makes

Standard library only.  Run:  python3 book7/ch-turing-verify.py
"""
import math, sys

FAIL = []
def check(label, ok, detail=""):
    print(("  PASS  " if ok else "  FAIL  ") + label + (("   " + detail) if detail else ""))
    if not ok: FAIL.append(label)

A, B = 0.1, 0.9
us = A + B
vs = B / (A + B) ** 2
fu = -1 + 2 * us * vs
fv = us * us
gu = -2 * us * vs
gv = -us * us
tr = fu + gv
det = fu * gv - fv * gu

print("=" * 70)
print("ch-turing-verify.py -- diffusion-driven instability, Schnakenberg a=0.1 b=0.9")
print("=" * 70)

print("\n[1] steady state and Jacobian")
check("u* = 1", abs(us - 1.0) < 1e-15, "%.15f" % us)
check("v* = 0.9", abs(vs - 0.9) < 1e-15, "%.15f" % vs)
for nm, got, want in [("f_u", fu, 0.8), ("f_v", fv, 1.0), ("g_u", gu, -1.8), ("g_v", gv, -1.0)]:
    check("%s = %+.4f" % (nm, got), abs(got - want) < 1e-12, "page says %+.1f" % want)

print("\n[2] the reaction alone is stable")
check("trace = -0.2 < 0", abs(tr + 0.2) < 1e-12 and tr < 0, "%.12f" % tr)
check("det = +1.0 > 0", abs(det - 1.0) < 1e-12 and det > 0, "%.12f" % det)

print("\n[3] condition 3:  d f_u + g_v > 0")
d3 = -gv / fu
check("requires d > 1.25", abs(d3 - 1.25) < 1e-12, "%.12f" % d3)

print("\n[4] condition 4:  (d f_u + g_v)^2 > 4 d det  ->  d_c")
qa, qb, qc = fu * fu, 2 * fu * gv - 4 * det, gv * gv
disc = qb * qb - 4 * qa * qc
dc = (-qb + math.sqrt(disc)) / (2 * qa)
lo = (-qb - math.sqrt(disc)) / (2 * qa)
check("d_c = 8.567627", abs(dc - 8.567627) < 1e-6, "%.9f" % dc)
check("the other root is below the condition-3 bound and is not the threshold",
      lo < d3, "lower root %.6f < %.2f" % (lo, d3))
check("condition 4 is an equality at d_c",
      abs((dc * fu + gv) ** 2 - 4 * dc * det) < 1e-9,
      "residual %.2e" % abs((dc * fu + gv) ** 2 - 4 * dc * det))

print("\n[5] the selected wavenumber")
kc2 = math.sqrt(det / dc)
check("k_c^2 = 0.341641", abs(kc2 - 0.341641) < 1e-6, "%.9f" % kc2)
check("k_c = 0.584500", abs(math.sqrt(kc2) - 0.584500) < 1e-6, "%.9f" % math.sqrt(kc2))
# at d_c the critical k is also the argmin of the dispersion relation
h = 1e-6
def hk(k2, d): return (1 - k2) * 0 + (fu - k2) * (gv - d * k2) - fv * gu
check("h(k^2) has its minimum at k_c^2", abs((hk(kc2 + h, dc) - hk(kc2 - h, dc)) / (2 * h)) < 1e-6,
      "dh/dk^2 = %.2e" % ((hk(kc2 + h, dc) - hk(kc2 - h, dc)) / (2 * h)))

def max_growth(d, kmax=20.0, n=200000):
    best, bk = -1e30, None
    for i in range(1, n + 1):
        k2 = i * (kmax / n)
        t2 = tr - k2 * (1 + d)
        d2 = (fu - k2) * (gv - d * k2) - fv * gu
        r = t2 * t2 - 4 * d2
        lam = (t2 + math.sqrt(r)) / 2 if r >= 0 else t2 / 2
        if lam > best: best, bk = lam, k2
    return best, bk

print("\n[6] the three growth rates on the page")
for mult, want, tol in [(0.98, -7.861e-3, 5e-6), (1.00, 0.0, 1e-6), (1.02, +7.615e-3, 5e-6)]:
    g, k2 = max_growth(dc * mult)
    check("d = %.2f d_c   max Re(lambda) = %+.6e" % (mult, g), abs(g - want) < tol,
          "page says %+.3e, at k^2 = %.4f" % (want, k2))

print("\n[7] below d_c, EVERY wavenumber decays")
for mult in (0.5, 0.8, 0.95, 0.99):
    g, k2 = max_growth(dc * mult)
    check("d = %.2f d_c   every mode decays" % mult, g < 0, "max growth %+.3e" % g)
for mult in (1.01, 1.5, 2.33):
    g, k2 = max_growth(dc * mult)
    check("d = %.2f d_c   some mode grows" % mult, g > 0, "max growth %+.3e at k^2 = %.4f" % (g, k2))

print("\n" + "=" * 70)
print("[HONESTY]")
print("=" * 70)
print("""  What this establishes. For this system, at these parameters, the four
  Turing conditions hold exactly as the page states them; d_c and k_c are
  closed-form roots and are exact to the digits printed; and the sign of the
  maximum growth rate flips at d_c and nowhere else in the range searched.

  What it does not establish. Blocks [6] and [7] scan k^2 on a grid of 200,000
  points up to k^2 = 20. An exhaustion over a finite grid is evidence, not
  proof, though here the dispersion relation is a quadratic in k^2 whose
  behaviour at large k is known, so the grid is a check on arithmetic rather
  than a search for a counterexample.

  This is LINEAR stability about the homogeneous state. It says when the flat
  state stops being stable and which wavelength goes first. It says nothing
  about the amplitude, the final pattern, or whether the pattern that forms is
  the one the linear analysis picks -- all of which are nonlinear questions.

  Nothing here is a claim that biological morphogenesis proceeds by Turing's
  mechanism. The page marks that OPEN and cites both the chemical confirmation
  (Castets et al. 1990) and one of the stronger biological cases (Sheth et al.
  2012). The mathematics is what the corpus uses; the biology is contested and
  the page says so.""")

print()
if FAIL:
    print("FAILED: %d" % len(FAIL))
    for f in FAIL: print("   " + f)
    sys.exit(1)
print("All blocks pass.")
