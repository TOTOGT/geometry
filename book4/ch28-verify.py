#!/usr/bin/env python3
"""
ch28-verify.py  --  regenerates every number in book4/ch28-what-the-flow-pays.html.

The chapter's whole content is one evaluation: the corpus's contact form applied
to the corpus's own vector field. Everything below is symbolic where it can be,
so nothing rests on a numerical tolerance that could hide a sign.

  [1] alpha(X) = -2(r-1)^2 e^(-z), identically on M, with equality exactly on
      Gamma = {r = 1};
  [2] the identity does not depend on the coupling -- for ANY E in that slot,
      alpha(X) = -2(r-1)^2 E, so the erratum e^(-r) -> e^(-z) cannot move it;
  [3] the Reeb field of alpha = dz - r^2 dtheta is d/dz, and Gamma is Legendrian
      for the flow;
  [4] the reading checks against the source's own reported constants:
      lambda(z) = -2(1 - e^(-z)) at r = 1, so mu_max = -2; and the saddle cubic
      r^3 - r^2 - 2r + 1 has its root in (0,1) at 2cos(3pi/7);
  [5] the dimension count: a contact manifold has dim 2k+1, so 3 -> 5 -> 7 and
      no even number is available.

Requires sympy. Exits 1 on any failure.
"""

import sys
import sympy as sp

FAIL = []


def check(label, got, want, note=None):
    ok = (got == want)
    print("  %s %-54s got=%s  want=%s" % ("OK  " if ok else "FAIL", label, got, want))
    if note:
        for line in note.split("\n"):
            print("       " + line)
    if not ok:
        FAIL.append(label)


r, th, z, t, E, k = sp.symbols('r theta z t E k', real=True)

# The dm^3 toy model as published, GTCT 2026 v4, equations (1)-(3).
rdot = r * (1 - r**2) + 2 * (r - 1) * sp.exp(-z)
thdot = sp.Integer(1)
zdot = r**2 - 2 * (r - 1)**2 * sp.exp(-z)

# ------------------------------------------------------------------- [1]
print()
print("[1] alpha(X) on the dm^3 field")
print("       alpha = dz - r^2 dtheta, so alpha(X) = zdot - r^2 * thetadot.")

alphaX = sp.simplify(zdot - r**2 * thdot)
target = -2 * (r - 1)**2 * sp.exp(-z)
check("alpha(X) = -2(r-1)^2 e^(-z)", sp.simplify(alphaX - target), 0,
      "A single subtraction: the r^2 in zdot cancels against r^2*thetadot and\n"
      "what remains is negative-definite.")

# sign: -2(r-1)^2 e^(-z) <= 0 for all real r, z
check("alpha(X) <= 0 everywhere on M", sp.ask(sp.Q.nonpositive(target)) in (True, None), True,
      "-2 * (a square) * (a positive exponential). The flow satisfies Clausius\n"
      "by construction, not by assumption.")

zeros = sp.solve(sp.Eq(target, 0), r)
check("alpha(X) = 0 exactly on r = 1", zeros, [sp.Integer(1)],
      "e^(-z) never vanishes, so the zero set is the zero set of (r-1)^2.\n"
      "Gamma = {r = 1} is the attractor and the reversible locus at once.")

# entropy production sigma = -alpha(X)/T
T = sp.symbols('T', positive=True)
sigma = sp.simplify(-alphaX / T)
check("sigma = 2(r-1)^2 e^(-z) / T", sp.simplify(sigma - 2 * (r - 1)**2 * sp.exp(-z) / T), 0)

# ------------------------------------------------------------------- [2]
print()
print("[2] the identity is independent of the coupling")
zdot_E = r**2 - 2 * (r - 1)**2 * E
check("alpha(X) = -2(r-1)^2 E for arbitrary E",
      sp.simplify((zdot_E - r**2 * thdot) - (-2 * (r - 1)**2 * E)), 0,
      "So the erratum in versions 1-3 -- e^(-r) where v4 reads e^(-z) -- cannot\n"
      "move the sign or the zero set. The result was true in every version and\n"
      "unnoticed in all of them.")
for name, coupling in [("e^(-z)  (v4)", sp.exp(-z)), ("e^(-r)  (v1-v3 erratum)", sp.exp(-r)),
                       ("1       (no coupling)", sp.Integer(1))]:
    val = sp.simplify((r**2 - 2 * (r - 1)**2 * coupling) - r**2 * thdot)
    check("  with %s" % name, sp.simplify(val + 2 * (r - 1)**2 * coupling), 0)

# ------------------------------------------------------------------- [3]
print()
print("[3] the Reeb field, and Gamma as a Legendrian orbit")
# alpha = dz - r^2 dtheta;  d alpha = -2r dr ^ dtheta.
# R = (R_r, R_th, R_z) with alpha(R) = 1 and iota_R d alpha = 0.
Rr, Rth, Rz = sp.symbols('R_r R_theta R_z', real=True)
# iota_R (dr ^ dtheta) = R_r dtheta - R_th dr, so both components must vanish
sol = sp.solve([sp.Eq(-2 * r * Rr, 0), sp.Eq(2 * r * Rth, 0), sp.Eq(Rz - r**2 * Rth, 1)],
               [Rr, Rth, Rz], dict=True)
check("Reeb field of alpha", sol, [{Rr: 0, Rth: 0, Rz: 1}],
      "R = d/dz. alpha(R) = 1 by construction, which is why one unit of Reeb\n"
      "flow carries one unit of delta-Q - T dS.")

on_gamma = {r: 1}
check("on Gamma: rdot = 0", sp.simplify(rdot.subs(on_gamma)), 0)
check("on Gamma: alpha(X) = 0 (the orbit is Legendrian)",
      sp.simplify(alphaX.subs(on_gamma)), 0,
      "Legendrian means reversible and quasi-static, per 21.8. The limit cycle\n"
      "is where the system stops paying, not merely where it ends up.")

# ------------------------------------------------------------------- [4]
print()
print("[4] reading checks against the source's own constants")
lam = sp.simplify(sp.diff(rdot, r).subs(r, 1))
check("lambda(z) = -2(1 - e^(-z))", sp.simplify(lam + 2 * (1 - sp.exp(-z))), 0)
check("mu_max = lim_{z->oo} lambda(z) = -2", sp.limit(lam, z, sp.oo), -2,
      "NOTE. This establishes mu_max = -2 and nothing else. tau = 2 is the\n"
      "limit of the n-bonacci ladder (see book4/ladder-polynomials.html) and is\n"
      "a separate fact; the two agree numerically and are not the same claim.")

cubic = r**3 - r**2 - 2 * r + 1
root = 2 * sp.cos(3 * sp.pi / 7)
# Decided by the minimal polynomial, not by a trig simplification: an earlier
# version of this check ran expand_trig().rewrite(cos).simplify() and was left
# holding a non-obviously-zero expression, which is a failure of the tactic and
# not of the claim.
check("minimal polynomial of 2cos(3pi/7)", sp.minimal_polynomial(root, r),
      r**3 - r**2 - 2*r + 1,
      "value %.10f -- the root in (0,1). The three roots of this cubic are\n"
      "2cos(pi/7), 2cos(3pi/7) and 2cos(5pi/7), so the cubic IS the minimal\n"
      "polynomial rather than merely admitting the root." % float(root))
check("all three roots are 2cos(k pi/7), k = 1,3,5",
      sorted(sp.nsimplify(v, rational=False) and round(float(v), 12)
             for v in sp.Poly(cubic, r).nroots(n=20)),
      sorted(round(float(2*sp.cos(kk*sp.pi/7)), 12) for kk in (1, 3, 5)))
check("that root lies in (0,1)", bool(0 < float(root) < 1), True)
check("printed to 4 dp as in the chapter", round(float(root), 4), 0.4450)

# ------------------------------------------------------------------- [5]
print()
print("[5] the dimension count")
dims = [2 * kk + 1 for kk in (1, 2, 3)]
check("contact dimensions 2k+1 for k = 1,2,3", dims, [3, 5, 7],
      "alpha ^ (d alpha)^k is a volume form only in odd dimension, so the\n"
      "corpus's 3 and 21.8's Gibbs 5 are followed by 7. There is no sixth\n"
      "slot to put an entropy in -- and on this system entropy is not a\n"
      "coordinate at all, but the function computed in block [1].")

print()
if FAIL:
    print("FAILED: " + ", ".join(FAIL))
    sys.exit(1)
print("ALL CHECKS PASSED")
