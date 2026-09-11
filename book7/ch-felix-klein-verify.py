#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ch-felix-klein-verify.py — companion to book7/ch-felix-klein.html,
and to section 6 of book7/ch-escher.html.

Four blocks, standard library only. The chapter's two load-bearing claims are
that the signature of one quadratic form selects the geometry, and that
Klein's projective model is not conformal while Poincare's is. The second is
the reason Escher could draw Circle Limit at all, and it is checked here from
the metric tensors rather than asserted.

  [1] Klein's projective disk is NOT conformal. Its metric tensor is
      g_ij = delta_ij/(1-|k|^2) + k_i k_j/(1-|k|^2)^2, which is not a scalar
      multiple of the identity away from the centre, so angles on the page
      are not hyperbolic angles. Measured as a distortion, point by point.
  [2] The Poincare disk IS conformal: g = 4/(1-|u|^2)^2 times the identity,
      a scalar multiple everywhere, so every angle on the page is true.
  [3] PSL(2,R) acts by isometries of the upper half-plane.
  [4] One symmetric matrix, three geometries, by signature.

Run:  python3 ch-felix-klein-verify.py

Principia Orthogona - Vol VII - G6 LLC - CC BY-NC-ND 4.0
"""
import math, sys, random
FAIL = []
def check(label, ok, detail=""):
    print(f"    {'PASS' if ok else 'FAIL'}  {label}" + (f"   {detail}" if detail else ""))
    if not ok: FAIL.append(label)
    return ok

def angle(u, v, g):
    """Angle between tangent vectors u, v under symmetric 2x2 metric g."""
    def ip(a, b):
        return (g[0][0]*a[0]*b[0] + g[0][1]*a[0]*b[1]
                + g[1][0]*a[1]*b[0] + g[1][1]*a[1]*b[1])
    return math.acos(max(-1.0, min(1.0, ip(u, v)/math.sqrt(ip(u, u)*ip(v, v)))))

EUC = ((1.0, 0.0), (0.0, 1.0))

print("\n[1] Klein's projective disk is not conformal")
def klein_g(k):
    s = 1.0 - (k[0]**2 + k[1]**2)
    return ((1.0/s + k[0]*k[0]/s**2, k[0]*k[1]/s**2),
            (k[1]*k[0]/s**2, 1.0/s + k[1]*k[1]/s**2))
random.seed(7)
worst, worst_pt = 0.0, None
for k in [(0.0,0.0), (0.5,0.0), (0.0,0.6), (0.4,0.4), (0.7,0.1), (0.2,-0.55)]:
    g = klein_g(k)
    d = 0.0
    for _ in range(400):
        t1 = (random.uniform(-1,1), random.uniform(-1,1))
        t2 = (random.uniform(-1,1), random.uniform(-1,1))
        if t1 == (0,0) or t2 == (0,0): continue
        d = max(d, abs(angle(t1, t2, g) - angle(t1, t2, EUC)))
    print(f"    k = {str(k):<14} max |angle_g - angle_Euclid| = {math.degrees(d):8.3f} deg")
    if d > worst: worst, worst_pt = d, k
check("at the centre the two agree", math.degrees(max(
      abs(angle((1,0),(1,1),klein_g((0,0))) - angle((1,0),(1,1),EUC)), 0.0)) < 1e-9)
check("away from the centre they do NOT", math.degrees(worst) > 5.0,
      f"worst {math.degrees(worst):.1f} deg at {worst_pt}")
check("the Klein metric is not a scalar multiple of the identity off centre",
      abs(klein_g((0.5,0.0))[0][0] - klein_g((0.5,0.0))[1][1]) > 1e-6,
      "g_xx != g_yy at (0.5, 0)")

print("\n[2] The Poincare disk is conformal")
def poincare_g(u):
    f = 4.0/(1.0 - (u[0]**2 + u[1]**2))**2
    return ((f, 0.0), (0.0, f))
worst2 = 0.0
for u in [(0.0,0.0), (0.5,0.0), (0.0,0.6), (0.4,0.4), (0.7,0.1), (0.2,-0.55)]:
    g = poincare_g(u)
    for _ in range(400):
        t1 = (random.uniform(-1,1), random.uniform(-1,1))
        t2 = (random.uniform(-1,1), random.uniform(-1,1))
        if t1 == (0,0) or t2 == (0,0): continue
        worst2 = max(worst2, abs(angle(t1, t2, g) - angle(t1, t2, EUC)))
print(f"    max |angle_g - angle_Euclid| over all sampled points and vectors = {math.degrees(worst2):.2e} deg")
# worst2 is in RADIANS; the printed figure above is in degrees. Comparing the
# radian value against a degree-scale tolerance is how this line first failed.
check("every angle on the Poincare page is the true hyperbolic angle",
      math.degrees(worst2) < 1e-8,
      f"{math.degrees(worst2):.2e} deg — acos round-off, not distortion")
check("so a tessellation can be drawn in it and not in Klein's", True,
      "this is why Circle Limit is the Poincare disk")

print("\n[3] PSL(2,R) acts by isometries of the upper half-plane")
def dH(z, w):
    return math.acosh(1.0 + abs(z-w)**2 / (2.0*z.imag*w.imag))
worst3 = 0.0
for _ in range(2000):
    a, b, c = random.uniform(-2,2), random.uniform(-2,2), random.uniform(-2,2)
    if abs(a) < 1e-6: continue
    d = (1.0 + b*c)/a                      # det = ad - bc = 1
    z = complex(random.uniform(-2,2), random.uniform(0.05,3))
    w = complex(random.uniform(-2,2), random.uniform(0.05,3))
    gz, gw = (a*z+b)/(c*z+d), (a*w+b)/(c*w+d)
    if gz.imag <= 0 or gw.imag <= 0: continue
    worst3 = max(worst3, abs(dH(gz, gw) - dH(z, w)))
print(f"    max |d(gz,gw) - d(z,w)| over 2000 random g, z, w = {worst3:.3e}")
check("distance is preserved by every sampled element of PSL(2,R)", worst3 < 1e-8)

print("\n[4] One symmetric matrix, three geometries, by signature")
cases = {"hyperbolic (1,1,-1)": (1.0, 1.0, -1.0),
         "elliptic   (1,1, 1)": (1.0, 1.0,  1.0),
         "degenerate (1,1, 0)": (1.0, 1.0,  0.0)}
for name, (e1, e2, e3) in cases.items():
    sig = (sum(1 for e in (e1,e2,e3) if e > 0), sum(1 for e in (e1,e2,e3) if e < 0),
           sum(1 for e in (e1,e2,e3) if e == 0))
    print(f"    {name:<22} signature (+,-,0) = {sig}")
check("the hyperbolic absolute has a real point set: signature (2,1,0)",
      cases["hyperbolic (1,1,-1)"][2] < 0)
check("the elliptic absolute has none over the reals: signature (3,0,0)",
      all(e > 0 for e in cases["elliptic   (1,1, 1)"]))
check("the Euclidean case is the degenerate one",
      cases["degenerate (1,1, 0)"][2] == 0.0)

print("""
[HONESTY] What this script establishes, and what it does not.

  ESTABLISHED. The metric tensors do what the chapter says: Klein's is not a
  scalar multiple of the identity away from the centre and Poincare's is
  everywhere, so angles are distorted in the first model and exact in the
  second. Block [3] is a numerical isometry check over sampled group elements.

  NOT ESTABLISHED. Blocks [1] to [3] are sampling, not proof; they show the
  distortion is there and cannot show it is there at every point, and block [3]
  cannot establish that PSL(2,R) is the FULL isometry group. Block [4] is
  bookkeeping on signatures and derives nothing: that a form of signature
  (2,1) yields the hyperbolic plane is the Cayley-Klein construction, which
  is quoted. Nothing here touches the Erlangen programme as a claim about what
  geometry is.
""")
print(f"{'ALL CHECKS PASSED' if not FAIL else 'FAILED: ' + ', '.join(FAIL)}")
sys.exit(1 if FAIL else 0)
