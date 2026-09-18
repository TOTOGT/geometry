#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
to_hub_verify.py -- the numerics behind the TO hub page's dm3 block.

WHY. grossi-ops.github.io/TO prints the dm3 contact equations with e^{-r} in
the coupling term, and on the next line prints lambda(z) = -2(1 - e^{-z}) and
mu_max = -2. Those cannot both be true. This script decides which one is the
typo, from the equations alone, with no appeal to any certificate.

Standard library only.  Exit 0 iff every block holds.
"""
import math, sys

def bisect(f, a, b, n=200):
    fa = f(a)
    for _ in range(n):
        m = (a + b) / 2.0
        fm = f(m)
        if (fa < 0) == (fm < 0):
            a, fa = m, fm
        else:
            b = m
    return (a + b) / 2.0

# as printed on the page
f_r = lambda r: r * (1 - r**2) + 2 * (r - 1) * math.exp(-r)
# with the coupling on z, as lambda(z) on the same page implies
f_z = lambda r, z: r * (1 - r**2) + 2 * (r - 1) * math.exp(-z)

H = 1e-7
ok = True
def check(cond, msg):
    global ok
    print(("  ok   " if cond else "  FAIL ") + msg)
    if not cond: ok = False

print("[1] Gamma = {r=1} is a fixed point of BOTH readings")
check(abs(f_r(1.0)) < 1e-15, "e^{-r}: rdot(1) = 0")
check(all(abs(f_z(1.0, z)) < 1e-15 for z in (0, 1, 5, 20)), "e^{-z}: rdot(1) = 0 for every z")

print("\n[2] The transverse eigenvalue at Gamma decides it")
d_r = (f_r(1 + H) - f_r(1 - H)) / (2 * H)
print("      e^{-r}:  f'(1) = %.9f   = -2 + 2/e" % d_r)
check(abs(d_r - (-2 + 2 / math.e)) < 1e-6, "e^{-r} gives -2 + 2/e = -1.264241, NOT -2")
check(abs(d_r + 2.0) > 0.7, "so the page's mu_max = -2 is false for the printed equations")
for z in (1, 2, 5, 10, 20):
    d = (f_z(1 + H, z) - f_z(1 - H, z)) / (2 * H)
    check(abs(d - (-2 * (1 - math.exp(-z)))) < 1e-6,
          "e^{-z}, z=%-3g: f'(1) = -2(1 - e^-z) = %.9f  <- the page's own formula" % (z, d))
check(abs(-2 * (1 - math.exp(-40)) + 2) < 1e-15, "e^{-z}: lambda(z) -> -2 as z -> inf, giving mu_max = -2")

print("\n[3] The inner zero of the PRINTED system is not r*")
root = bisect(f_r, 0.3, 0.95)
print("      inner zero of e^{-r} system:  r = %.9f" % root)
check(abs(root - 0.6414946) < 1e-6, "it is 0.641494576, matching the coupling erratum on file")
check(abs(f_r(0.77594058)) > 0.1, "rdot(0.77594058) = %.6f -- r* is NOT a zero of the printed system" % f_r(0.77594058))

print("\n[4] The Reeb field is not the helix")
# alpha = dz - r^2 dtheta on (r, theta, z);  d alpha = -2r dr ^ dtheta
alpha  = lambda r, v: (-r**2) * v[1] + v[2]
dalpha = lambda r, u, v: -2 * r * (u[0] * v[1] - u[1] * v[0])
Reeb = (0, 0, 1)
check(abs(alpha(2.3, Reeb) - 1) < 1e-15, "alpha(d/dz) = 1")
check(all(abs(dalpha(r, Reeb, w)) < 1e-15
          for r in (0.5, 1.0, 2.3) for w in ((1,0,0), (0,1,0), (0,0,1))),
      "iota_R dalpha = 0  -> R = d/dz IS the Reeb field")
print("      its integral curves are (r0, th0, z0+t): r and theta constant.")
check(True, "that is a vertical line -- no winding, no period, not a helix")
zdot = lambda r, z: r**2 - 2 * (r - 1)**2 * math.exp(-z)
check(all(abs(f_z(1.0, z)) < 1e-15 and abs(zdot(1.0, z) - 1) < 1e-15 for z in (0, 1, 7.5)),
      "on Gamma the dm3 flow has rdot=0, thetadot=1, zdot=1 -> (1, t, z0+t), a helix of pitch 2*pi")
tangent = (0, 1, 1)
check(abs(alpha(1.0, tangent)) < 1e-15, "alpha(d/dth + d/dz) = 1 - r^2 = 0 at r=1 -> Gamma is LEGENDRIAN")
check(abs(alpha(0.8, tangent)) > 0.3 and abs(alpha(1.2, tangent)) > 0.4,
      "and nonzero off Gamma -- the limit cycle sits on the Legendrian locus of alpha")

print("\n[5] VERDICT")
print("      The equations are the typo, not the constants. With e^{-z} the page's own")
print("      lambda(z) and mu_max = -2 are exact. With e^{-r} neither holds and the")
print("      basin edge moves to 0.641. r* = 0.77594058 is not re-derived here; its")
print("      provenance is settled in docs/audit-log.md and is cited, not recomputed.")

print()
print("  all blocks hold." if ok else "  FAILURES ABOVE.")
sys.exit(0 if ok else 1)
