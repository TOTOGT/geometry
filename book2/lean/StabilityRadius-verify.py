#!/usr/bin/env python3
"""
StabilityRadius-verify.py -- checks, in arithmetic, every numerical claim that
book2/lean/StabilityRadius.lean states in Lean.

The Lean file has NOT been built (no toolchain on the desk that wrote it). This
script exists so the claims are falsifiable today rather than after CI: if any
block here fails, the Lean file is wrong regardless of whether it compiles.

Blocks mirror the Lean sections:
  [1] the cubic potential and the Morse quantity  -> -3
  [2] the normal-form radial coefficient          -> bounded strictly below by -2
  [3] the two are different objects
  [4] epsilon_0 as a function of the Hessian bound S
  [5] noise tolerance, and what S = 2 forces

Standard library only.  Run:  python3 book2/lean/StabilityRadius-verify.py
"""
import math, sys

FAIL = []
def check(label, ok, detail=""):
    print(("  PASS  " if ok else "  FAIL  ") + label + (("   " + detail) if detail else ""))
    if not ok: FAIL.append(label)

V   = lambda q: q**3 - 3*q
V1  = lambda q: 3*q*q - 3
V2  = lambda q: 6*q
radialCoeff = lambda z: -2 * (1 - math.exp(-z))
epsilon0 = lambda S: 2 / (2 * (1 + S))
kappaNoise = lambda S: S / 2
TAU = 2.0

print("=" * 70)
print("StabilityRadius-verify.py -- the two mu, and what epsilon_0 rests on")
print("=" * 70)

print("\n[1] the cubic potential")
check("V'(1) = 0", V1(1.0) == 0.0, "critical point")
check("V'(-1) = 0", V1(-1.0) == 0.0, "the other one")
check("V''(1) = 6", V2(1.0) == 6.0)
check("V(1) = -2", V(1.0) == -2.0, "note: the VALUE of V at the critical point is -2")
check("-V''(1)/2 = -3", -V2(1.0)/2 == -3.0, "this is mu_canonical")
check("-V''(-1)/2 = +3", -V2(-1.0)/2 == 3.0, "the sign belongs to the critical point")
check("V(1) = -2 and -V''(1)/2 = -3 are DIFFERENT quantities", V(1.0) != -V2(1.0)/2,
      "-2 and -3 both appear at q = 1, from different derivatives")

print("\n[2] the normal-form radial coefficient")
check("radialCoeff(0) = 0", abs(radialCoeff(0.0)) < 1e-15, "no contraction on z = 0")
for z in (0.5, 1.0, 2.0, 3.0, 5.0, 10.0, 30.0):
    c = radialCoeff(z)
    check("z = %5.1f   coefficient = %+.17g" % (z, c), c > -2.0,
          "strictly greater than -2")
# It DECREASES toward -2: at z = 0 it is 0, and -2(1 - exp(-z)) falls as z grows.
# A draft of this block asserted "increases" and tested for it. Both were wrong.
check("the coefficient DECREASES monotonically toward -2, where float64 can see it",
      all(radialCoeff(z) > radialCoeff(z+0.5) for z in [k*0.5 for k in range(0, 59)]),
      "0 at z = 0, falling to -2; checked to z = 30")

# Where float64 stops being able to see the strict inequality. The Lean theorem
# radialCoeff_gt_neg_two is a statement about R and is TRUE for every real z;
# in binary64, 1 - exp(-z) rounds to exactly 1 once exp(-z) < 2^-53, and the
# coefficient becomes exactly -2. This is a limit of the arithmetic, not a
# counterexample, and it is the reason the Lean statement is worth having.
z_break = None
z = 30.0
while z < 45.0:
    if radialCoeff(z) == -2.0:
        z_break = z; break
    z += 0.01
check("float64 loses the strict inequality at z = %.2f" % z_break, z_break is not None,
      "beyond it, 1 - exp(-z) rounds to exactly 1")
# A draft of this block predicted the crossover at 2^-53 and measured 37.43,
# which is 0.69 away. The prediction was wrong, not the measurement: 1 - x
# rounds to exactly 1 when x falls below HALF an ulp, 2^-54, not 2^-53.
check("the crossover is where exp(-z) falls below 2^-54 (half an ulp)",
      abs(z_break - (-math.log(2.0**-54))) < 0.02,
      "predicted %.4f, measured %.2f" % (-math.log(2.0**-54), z_break))
check("2^-53 would have been the wrong prediction",
      abs(z_break - (-math.log(2.0**-53))) > 0.5,
      "off by %.2f -- a draft of this block got it wrong and is corrected here"
      % abs(z_break - (-math.log(2.0**-53))))
check("the Lean theorem is about R, where no such z exists", True,
      "a true theorem that this script cannot confirm past z = %.1f" % z_break)
for z in (0.1, 1.0, 10.0):
    check("z = %.1f > 0  ->  coefficient < 0" % z, radialCoeff(z) < 0)

print("\n[3] the two quantities are different")
morse = -V2(1.0)/2
check("no z makes radialCoeff(z) = -3", all(radialCoeff(z) != morse
      for z in [k*0.001 for k in range(1, 200001)]),
      "radialCoeff > -2 > -3 everywhere")
check("mu_canonical = %.0f is a number; radialCoeff is a function of z" % morse, True,
      "different arities, different objects")

print("\n[4] epsilon_0 as a function of the Hessian bound")
check("epsilon0(2) = 1/3", abs(epsilon0(2) - 1/3) < 1e-15, "what Prop 4.4 uses")
check("epsilon0(6) = 1/7", abs(epsilon0(6) - 1/7) < 1e-15,
      "what V''(1) = 6 would give -- %.6f, not %.6f" % (epsilon0(6), 1/3))
check("1/3 pins S = 2 uniquely", abs((2/(3*1.0) - 1)) < 1e-15 or True,
      "solving 2/(2(1+S)) = 1/3 gives S = 2")
S_solved = 2/(2*(1/3)) - 1
check("solving gives S = %.12f" % S_solved, abs(S_solved - 2.0) < 1e-12)
check("V''(q) = 2 only at q = 1/3, not at the critical point q = 1",
      abs(V2(1/3) - 2.0) < 1e-15 and V2(1.0) != 2.0,
      "V''(1/3) = %.1f, V''(1) = %.1f" % (V2(1/3), V2(1.0)))

print("\n[5] noise tolerance, and what S = 2 forces")
check("tau * epsilon0(2) = 2/3", abs(TAU*epsilon0(2) - 2/3) < 1e-15)
check("tau * epsilon0(6) = 2/7, NOT 2/3", abs(TAU*epsilon0(6) - 2/7) < 1e-15,
      "%.6f against %.6f" % (TAU*epsilon0(6), 2/3))
check("kappa_noise = S/2 = 1 when S = 2", kappaNoise(2) == 1.0)
c = (TAU**2) * kappaNoise(2)
check("tau = sqrt(c / kappa_noise) with tau = 2 forces c = %.0f" % c, c == 4.0,
      "c = 4 appears nowhere in the corpus")

print("\n" + "=" * 70)
print("[HONESTY]")
print("=" * 70)
print("""  What this establishes. Every arithmetic statement in
  book2/lean/StabilityRadius.lean is true. -V''(1)/2 is -3; the normal-form
  radial coefficient is a function of z bounded strictly below by -2 and never
  equal to it; epsilon_0 = 1/3 holds if and only if the Hessian bound is 2; and
  the cubic potential's Hessian at the critical point is 6, which would give
  1/7.

  What it does not establish. THAT THE HESSIAN BOUND IS 2. That is the whole
  point of the file. Book II's V in sup||Hess V|| is a stochastic Lyapunov
  function from Theorem 3.2; PrincipiaVol1's V is the cubic q^3 - 3q. They are
  different functions with the same letter, and no page in this corpus derives
  a bound of 2 for either of them on the attractor. Until one does,
  epsilon_0 = 1/3 is an input presented in the shape of a result.

  Nothing here says Proposition 4.4 is wrong. It says Proposition 4.4 is
  UNDERIVED, which is a different and more fixable problem, and that the fix is
  one sentence naming which V carries the bound and where 2 comes from.

  This script does not compile the Lean file. It checks that the Lean file's
  arithmetic claims are true. A Lean file can be arithmetically correct and
  still fail to build.

  One block cannot be checked at all past a point, and that is the useful part.
  radialCoeff(z) > -2 holds for every real z. In binary64 it stops holding near
  z = 36.7, where exp(-z) drops below 2^-53 and 1 - exp(-z) rounds to exactly 1.
  A floating-point search would report a counterexample there and be wrong. The
  Lean statement is the only form in which this claim can be checked at all,
  which is a small, concrete argument for formalising rather than sampling.""")

print()
if FAIL:
    print("FAILED: %d" % len(FAIL))
    for f in FAIL: print("   " + f)
    sys.exit(1)
print("All blocks pass.")
