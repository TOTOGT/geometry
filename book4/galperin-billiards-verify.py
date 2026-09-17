#!/usr/bin/env python3
"""
galperin-billiards-verify.py

Two blocks on a frictionless line, a wall on the left, all collisions
perfectly elastic. The small block has mass m, the large one M = 100^n * m
and slides in from the right. Count every collision, block-on-block and
block-on-wall.

The count is the leading digits of pi:  3, 31, 314, 3141, 31415, 314159.

Source of the result (input, not proved here):
  G. Galperin, "Playing pool with pi (the number pi from a billiard point of
  view)", Regular and Chaotic Dynamics 8 (2003) 375-394. See also
  arXiv:1712.06698, "The Dynamics of Digits: Calculating Pi with Galperin's
  Billiards".
  It reached this project by way of Grant Sanderson's exposition.

Standard library only. Blocks [1] and [2] use exact rational arithmetic;
block [3] says where it switches to floating point and why.
"""

from fractions import Fraction as F
import math

FAIL = []
def check(name, ok, detail=""):
    print(("  PASS  " if ok else "  FAIL  ") + name + (("   " + detail) if detail else ""))
    if not ok: FAIL.append(name)

PI_DIGITS = "314159265358979"

def collide(m1, u1, m2, u2):
    """Elastic collision. Rational in the masses and velocities, so exact."""
    v1 = ((m1 - m2) * u1 + 2 * m2 * u2) / (m1 + m2)
    v2 = ((m2 - m1) * u2 + 2 * m1 * u1) / (m1 + m2)
    return v1, v2

def simulate(mass_ratio, exact=True):
    """Return the total number of collisions for M/m = mass_ratio.
       Small block starts at rest; big block moves left at unit speed."""
    T = F if exact else float
    m1, m2 = T(1), T(mass_ratio)
    u1, u2 = T(0), T(-1)          # rightward positive; big block comes in leftward
    n = 0
    while True:
        # BUG FOUND AND FIXED. The first version tested `u2 >= 0 and u1 <= u2`,
        # which fires while the small block is still moving LEFT toward the
        # wall -- it counted the block-block collisions and stopped before the
        # wall bounce that must follow, returning roughly half the true count.
        # Both blocks must be moving right, with the big one not slower.
        if u1 >= 0 and u2 >= u1:
            return n
        if u1 < 0:                # small block is heading into the wall
            u1 = -u1
        else:                     # blocks meet
            u1, u2 = collide(m1, u1, m2, u2)
        n += 1

print("[1] Direct simulation, exact rational arithmetic.")
print("    Every velocity is a fraction throughout; no rounding anywhere.")
print()
print("      M/m        collisions    leading digits of pi   match")
for k in range(3):
    ratio = 100 ** k
    n = simulate(ratio, exact=True)
    want = int(PI_DIGITS[:k + 1])
    print("    %9d   %10d    %-20s   %s" % (ratio, n, PI_DIGITS[:k + 1], n == want))
    check("M/m = 100^%d gives %d collisions" % (k, want), n == want, "got %d" % n)

print()
print("[2] Why pi, and not merely a number that looks like pi.")
print("    Rescale to y1 = sqrt(m1) x1, y2 = sqrt(m2) x2. Kinetic energy becomes")
print("    the squared length of the velocity vector, so every collision is a")
print("    REFLECTION preserving speed, and the whole motion is a billiard in a")
print("    wedge. The wedge angle is theta = arctan(sqrt(m1/m2)), and the number")
print("    of reflections that fit before the trajectory escapes is ceil(pi/theta) - 1.")
print()
print("      n     theta (rad)      ceil(pi/theta)-1   pi digits")
for k in range(8):
    ratio = 100 ** k
    theta = math.atan(math.sqrt(1.0 / ratio))
    # BUG FOUND AND FIXED. The first version used ceil(pi/theta) and was off by
    # exactly one on every row. The count is ceil(pi/theta) - 1: the trajectory
    # gets one reflection per full wedge angle it turns through, and the last
    # partial wedge does not produce a collision. At n = 0 the ratio pi/theta is
    # exactly 4 and the answer is 3, which is the case that exposes it.
    pred = math.ceil(math.pi / theta) - 1
    want = int(PI_DIGITS[:k + 1])
    print("    %3d   %.12f   %14d   %s" % (k, theta, pred, PI_DIGITS[:k + 1]))
    check("ceil(pi/theta) gives the first %d digits of pi at n = %d" % (k + 1, k),
          pred == want, "got %d want %d" % (pred, want))
print()
print("    theta = arctan(10^-n), and arctan(x) -> x, so pi/theta -> pi * 10^n.")
print("    The digits of pi appear because the wedge angle is being driven to")
print("    zero in a way that makes the ceiling read off pi's decimal expansion.")
print("    Nothing about the blocks knows this. The count is forced by geometry.")

print()
print("[3] Larger n, where the arithmetic has to change.")
print("    Exact fractions grow without bound here: after a few hundred")
print("    collisions the numerators are thousands of digits and the run stops")
print("    being a check and starts being a stress test. From n = 3 the")
print("    simulation switches to floating point and is labelled as such.")
print()
print("      M/m          collisions   expected   match   arithmetic")
for k in (3, 4):
    ratio = 100 ** k
    n = simulate(ratio, exact=False)
    want = int(PI_DIGITS[:k + 1])
    print("    %11d   %10d   %8d   %5s   float64" % (ratio, n, want, n == want))
    check("M/m = 100^%d gives %d collisions (float)" % (k, want), n == want, "got %d" % n)

print()
print("    The float run agreeing with the exact run where they overlap, and")
print("    with the closed form where they do not, is the only reason block [3]")
print("    is worth printing at all.")
for k in range(3):
    ratio = 100 ** k
    check("exact and float agree at n = %d" % k,
          simulate(ratio, True) == simulate(ratio, False))

print()
if FAIL:
    print("FAILED: " + "; ".join(FAIL)); raise SystemExit(1)
print("All checks passed.")
print()
print("Why this sits in Book 4. The corpus opens its operator chain at pi with")
print("the period T* = 2 pi, and takes pi as a fact about closure. Galperin's")
print("billiard is pi arriving from somewhere else entirely: a counting problem")
print("in Newtonian mechanics, with no circle anywhere in the statement, where")
print("pi appears because the configuration space turns out to be a wedge and")
print("reflections in a wedge are counted by an angle. It is the cleanest")
print("available demonstration that pi is not about circles. It is about how")
print("much turning fits before a thing comes back.")
