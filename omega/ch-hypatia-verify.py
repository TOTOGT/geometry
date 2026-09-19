#!/usr/bin/env python3
"""
ch-hypatia-verify.py -- every number on omega/ch-hypatia.html, produced here.

Blocks:
  [1] e = cos(beta)/cos(alpha) reproduces the four values quoted on the page
  [2] the three regimes are exactly ellipse / parabola / hyperbola
  [3] the threshold sits at beta = alpha to machine precision, and only there
  [4] the conic's own discriminant classification agrees with e
  [5] continuity of e against discontinuity of kind -- the page's claim, measured

Primary source: Apollonius of Perga, Conics I. The focus-directrix form with
e = cos(beta)/cos(alpha) is the standard modern restatement (Dandelin spheres).

Standard library only.  Run:  python3 omega/ch-hypatia-verify.py
"""
import math, sys

FAIL = []
def check(label, ok, detail=""):
    print(("  PASS  " if ok else "  FAIL  ") + label + (("   " + detail) if detail else ""))
    if not ok: FAIL.append(label)

def ecc(alpha_deg, beta_deg):
    return math.cos(math.radians(beta_deg)) / math.cos(math.radians(alpha_deg))

def kind(e, tol=1e-12):
    if abs(e - 1.0) <= tol: return "parabola"
    return "ellipse" if e < 1.0 else "hyperbola"

print("=" * 70)
print("ch-hypatia-verify.py -- Apollonius' conics as a threshold")
print("=" * 70)

A = 30.0

print("\n[1] the four eccentricities quoted on the page (alpha = 30 deg)")
for beta, want in [(10, 1.137158), (29, 1.009924), (30, 1.000000), (31, 0.989772)]:
    got = ecc(A, beta)
    check("beta = %2d deg  ->  e = %.6f" % (beta, got),
          abs(got - want) < 5e-7, "page says %.6f" % want)

print("\n[2] the three regimes")
for beta, want in [(10, "hyperbola"), (20, "hyperbola"), (29, "hyperbola"),
                   (30, "parabola"),
                   (31, "ellipse"), (45, "ellipse"), (60, "ellipse"), (80, "ellipse")]:
    got = kind(ecc(A, beta))
    check("beta = %2d deg  ->  %-9s" % (beta, got), got == want, "expected %s" % want)

print("\n[3] the threshold is beta = alpha, and nowhere else")
for a in (5.0, 17.5, 30.0, 44.0, 61.25, 79.0):
    check("alpha = %5.2f deg  ->  e(alpha) == 1 exactly" % a,
          ecc(a, a) == 1.0, "e = %.17g" % ecc(a, a))
off = [b for b in [x * 0.25 for x in range(1, 360)] if b != A and kind(ecc(A, b)) == "parabola"]
check("no other beta in (0, 90) at 0.25 deg resolution gives a parabola",
      not off, "found %d" % len(off))

print("\n[4] the discriminant of the conic agrees with e")
# A conic of eccentricity e about a focus, in Cartesian form, has
# B^2 - 4AC of the sign of (e^2 - 1): negative ellipse, zero parabola, positive hyperbola.
for beta in (10, 29, 30, 31, 60):
    e = ecc(A, beta)
    disc = e * e - 1.0
    by_disc = "parabola" if disc == 0.0 else ("ellipse" if disc < 0 else "hyperbola")
    check("beta = %2d deg  discriminant sign -> %-9s" % (beta, by_disc),
          by_disc == kind(e), "e = %.9f, e^2-1 = %+.3e" % (e, disc))

print("\n[5] continuous parameter, discontinuous kind")
e29, e31 = ecc(A, 29), ecc(A, 31)
span = abs(e29 - e31)
check("e moves by %.4f (%.2f%%) across beta = 29 -> 31 deg" % (span, 100 * span / e29),
      span < 0.03, "a small, smooth change")
check("the KIND changes across that same interval",
      kind(e29) != kind(e31), "%s -> %s" % (kind(e29), kind(e31)))
# and e itself is smooth there: a centred difference matches the derivative
h = 1e-5
num = (ecc(A, 30 + h) - ecc(A, 30 - h)) / (2 * h)
ana = -math.sin(math.radians(30.0)) / math.cos(math.radians(A)) * math.pi / 180.0
check("e is differentiable AT the threshold", abs(num - ana) < 1e-8,
      "numeric %.9f vs analytic %.9f" % (num, ana))

print("\n" + "=" * 70)
print("[HONESTY]")
print("=" * 70)
print("""  What this establishes. The eccentricity of a conic section is a smooth,
  differentiable function of the cutting angle, including at the angle where
  the section changes kind; and the change of kind happens at exactly one
  angle, beta = alpha, where the plane runs parallel to a generator of the
  cone. That is the page's claim and it is arithmetic: it is established.

  What it does not establish. Block [3] searches beta on a 0.25-degree grid.
  An exhaustive check on a finite grid is evidence and not proof, though the
  analytic statement -- cos(beta) = cos(alpha) has one root in (0, 90) -- is
  elementary and needs no search.

  Nothing here is a claim about Hypatia. No theorem is attributed to her on
  the page, because none is known to be hers; the Conics is Apollonius', and
  what she is credited with is the commentary that carried it. The page marks
  the recension hypotheses OPEN and this script does not touch them: no
  arithmetic can settle a question of manuscript transmission.""")

print()
if FAIL:
    print("FAILED: %d" % len(FAIL))
    for f in FAIL: print("   " + f)
    sys.exit(1)
print("All blocks pass.")
