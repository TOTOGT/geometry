#!/usr/bin/env python3
"""
ch-katherine-johnson-verify.py -- every number on book7/ch-katherine-johnson.html.

The launch-azimuth relation of Skopinski and Johnson, NASA TN D-233 (1960):

    sin(beta) = cos(i) / cos(phi)

beta the inertial azimuth clockwise from north, i the orbital inclination,
phi the launch latitude. The ground-relative azimuth follows by subtracting the
launch site's own eastward velocity from the east component of the burnout
velocity.

Blocks:
  [1] the spherical-triangle identity, checked against a direct vector construction
  [2] the inertial azimuths quoted on the page
  [3] the Earth-rotation correction, against Friendship 7's flown 72.6 degrees
  [4] the hard floor |i| >= |phi|
  [5] the plane-change cost that makes the floor expensive to escape

Standard library only.  Run:  python3 book7/ch-katherine-johnson-verify.py
"""
import math, sys

FAIL = []
def check(label, ok, detail=""):
    print(("  PASS  " if ok else "  FAIL  ") + label + (("   " + detail) if detail else ""))
    if not ok: FAIL.append(label)

D, R = math.degrees, math.radians
PHI = 28.47          # Cape Canaveral, degrees north
V_EQ = 465.1         # Earth's equatorial surface speed, m/s

def azimuth_inertial(i, phi=PHI):
    s = math.cos(R(i)) / math.cos(R(phi))
    return None if abs(s) > 1 else D(math.asin(s))

print("=" * 70)
print("ch-katherine-johnson-verify.py -- TN D-233, the launch azimuth")
print("=" * 70)

print("\n[1] the identity, against a direct vector construction")
# Build an orbit of inclination i, find its velocity direction where it crosses
# latitude phi, and read off the azimuth. This uses no azimuth formula.
def azimuth_by_vectors(i, phi):
    ii, pp = R(i), R(phi)
    # argument of latitude u where the ground track reaches latitude phi:
    # sin(phi) = sin(i) sin(u)
    su = math.sin(pp) / math.sin(ii)
    if abs(su) > 1: return None
    u = math.asin(su)
    # position and velocity in the orbital plane, rotated by inclination
    cu, su_ = math.cos(u), math.sin(u)
    ci, si = math.cos(ii), math.sin(ii)
    pos = (cu, su_*ci, su_*si)
    vel = (-su_, cu*ci, cu*si)
    # local north and east at pos
    up = pos
    east = (-pos[1], pos[0], 0.0)
    ne = math.hypot(east[0], east[1])
    east = (east[0]/ne, east[1]/ne, 0.0)
    north = (up[1]*east[2] - up[2]*east[1],
             up[2]*east[0] - up[0]*east[2],
             up[0]*east[1] - up[1]*east[0])
    ve = sum(vel[k]*east[k] for k in range(3))
    vn = sum(vel[k]*north[k] for k in range(3))
    return D(math.atan2(ve, vn))
for i in (32.5, 40.0, 51.6, 60.0):
    a, b = azimuth_inertial(i), azimuth_by_vectors(i, PHI)
    check("i = %5.2f   formula %.6f   vectors %.6f" % (i, a, b), abs(a - b) < 1e-9,
          "difference %.2e degrees" % abs(a - b))

print("\n[2] the inertial azimuths on the page")
for i, want in [(28.47, 90.000), (32.5, 73.621), (40.0, 60.625),
                (51.6, 44.959), (60.0, 34.666), (90.0, 0.000)]:
    a = azimuth_inertial(i)
    check("i = %5.2f  ->  beta = %.3f" % (i, a), abs(a - want) < 5e-4,
          "page says %.3f" % want)

print("\n[3] Friendship 7: the ground-relative azimuth")
bi = R(azimuth_inertial(32.5))
ve_site = V_EQ * math.cos(R(PHI))
check("the pad's eastward speed is %.0f m/s" % ve_site, abs(ve_site - 409) < 1.5,
      "465.1 cos(28.47)")
for V, want in [(7400, 72.678), (7600, 72.704), (7800, 72.729)]:
    east = V*math.sin(bi) - ve_site
    north = V*math.cos(bi)
    bg = D(math.atan2(east, north))
    check("burnout %d m/s  ->  beta_ground = %.3f" % (V, bg), abs(bg - want) < 5e-4,
          "page says %.3f" % want)
bg = D(math.atan2(7600*math.sin(bi) - ve_site, 7600*math.cos(bi)))
check("agrees with the flown 72.6 deg to within 0.15 deg", abs(bg - 72.6) < 0.15,
      "computed %.3f, flown 72.6" % bg)
check("the correction is NOT negligible", abs(D(bi) - bg) > 0.8,
      "inertial %.3f vs ground %.3f -- %.2f degrees apart" % (D(bi), bg, D(bi) - bg))
spread = max(abs(D(math.atan2(V*math.sin(bi) - ve_site, V*math.cos(bi))) - 72.70)
             for V in (7400, 7800))
check("and it barely depends on burnout speed", spread < 0.05,
      "range %.3f deg across 7400-7800 m/s" % spread)

print("\n[4] the hard floor")
for i, ok in [(28.47, True), (28.00, False), (25.00, False), (20.00, False)]:
    a = azimuth_inertial(i)
    s = math.cos(R(i))/math.cos(R(PHI))
    check("i = %5.2f   sin beta = %.6f   %s" % (i, s, "solvable" if a else "NO SOLUTION"),
          (a is not None) == ok)
check("the boundary is exactly i = phi", abs(azimuth_inertial(PHI) - 90.0) < 1e-9,
      "sin beta = 1 -> due east")
check("and one hundredth of a degree below it there is none",
      azimuth_inertial(PHI - 0.01) is None)

print("\n[5] what escaping the floor costs")
V = 7700.0
for di, want in [(5.0, 671), (10.0, 1342), (28.47, 3786)]:
    dv = 2*V*math.sin(R(di)/2)
    check("plane change of %5.2f deg costs %.0f m/s" % (di, dv), abs(dv - want) < 12,
          "2 v sin(di/2) at v = %.0f m/s" % V)
check("a 5-degree change costs more than most upper stages carry",
      2*V*math.sin(R(5.0)/2) > 600, "%.0f m/s" % (2*V*math.sin(R(5.0)/2)))

print("\n" + "=" * 70)
print("[HONESTY]")
print("=" * 70)
print("""  What this establishes. The azimuth relation is confirmed independently in
  block [1] by constructing an inclined orbit as vectors and reading the
  velocity direction at the launch latitude -- no azimuth formula used -- with
  agreement to 1e-9 degrees. The Earth-rotation correction brings the predicted
  heading for Friendship 7 to within 0.13 degrees of the azimuth actually
  flown, and the floor |i| >= |phi| is exact, not a practical limit.

  What it does not establish. This is the two-body, spherical-Earth,
  instantaneous-burn idealisation. A real ascent flies a lofted trajectory
  through an oblate, rotating atmosphere with a finite burn and dogleg
  manoeuvres, and TN D-233 itself is concerned with a harder question than the
  one checked here -- placing the vehicle over a SELECTED EARTH POSITION at
  burnout, which couples the azimuth to the launch time. The 0.13-degree
  agreement with the flown value should be read as confirming the relation, not
  as reproducing the Mercury trajectory.

  The burnout speeds are representative values, not the flown figure; the point
  of block [3] is that the answer moves by less than 0.05 degrees across the
  plausible range, so the comparison does not depend on picking one.

  Nothing here concerns her hand recomputation before Friendship 7. That is a
  historical claim, cited on the page, and arithmetic cannot verify it.""")

print()
if FAIL:
    print("FAILED: %d" % len(FAIL))
    for f in FAIL: print("   " + f)
    sys.exit(1)
print("All blocks pass.")
