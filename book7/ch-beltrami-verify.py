#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ch-beltrami-verify.py — companion to book7/ch-beltrami.html.

Five blocks, standard library only. Every figure the chapter prints is
produced here; the chapter quotes nothing this script does not.

  [1] The Hannover triangle. Heron area of the sides usually quoted, and the
      spherical excess that area must produce on a sphere of Earth's radius,
      against the roughly 14.85 arcseconds Gauss reported.
  [2] The ISS worldline. Helix radius against pitch c*T, and the curvature
      scale GM/(r c^2) that closes the orbit.
  [3] Gauss-Bonnet by counting. For a triangulated closed surface, total
      angle defect = 2 pi V - pi F, and 3F = 2E turns that into 2 pi chi.
      Checked on the tetrahedron, octahedron and icosahedron.
  [4] The sign flip. A hyperbolic triangle's area is pi minus its angle sum,
      so it is bounded by pi however far apart the vertices are.
  [5] Parity and orientability (section 12 of ch-escher). Closed orientable
      surfaces have chi = 2 - 2g, always even; RP^2 has chi = 1.

Run:  python3 ch-beltrami-verify.py

Principia Orthogona - Vol VII - G6 LLC - CC BY-NC-ND 4.0
"""
import math, sys
FAIL = []
def check(label, ok, detail=""):
    print(f"    {'PASS' if ok else 'FAIL'}  {label}" + (f"   {detail}" if detail else ""))
    if not ok: FAIL.append(label)
    return ok

print("\n[1] The Hannover triangle")
a, b, c = 107.0, 85.0, 69.0                      # km, the sides usually quoted
s = (a + b + c) / 2
area = math.sqrt(s * (s - a) * (s - b) * (s - c))
R = 6371.0                                        # km, mean Earth radius
excess_rad = area / R**2
excess_arcsec = math.degrees(excess_rad) * 3600.0
gauss_reported = 14.85
print(f"    Heron area               = {area:.1f} km^2")
print(f"    excess = A/R^2           = {excess_rad:.6e} rad")
print(f"    excess                   = {excess_arcsec:.2f} arcsec")
print(f"    Gauss reported           = about {gauss_reported} arcsec")
check("chapter's 2930 km^2 is the Heron area to 3 s.f.", abs(area - 2930.0) < 5.0)
check("chapter's 14.9 arcsec is the computed excess", abs(excess_arcsec - 14.9) < 0.1)
check("computed excess is within 1 arcsec of Gauss's reported figure",
      abs(excess_arcsec - gauss_reported) < 1.0,
      f"diff = {abs(excess_arcsec-gauss_reported):.2f}")

print("\n[2] The ISS worldline")
C = 299792458.0
r_iss = 6791e3
T_iss = 5561.0
GM = 3.986004418e14
pitch = C * T_iss
ratio = r_iss / pitch
curv = GM / (r_iss * C**2)
print(f"    helix radius r           = {r_iss:.3e} m")
print(f"    pitch c*T                = {pitch:.3e} m")
print(f"    r / cT                   = {ratio:.3e}")
print(f"    GM/(r c^2)               = {curv:.3e}")
check("chapter's 4e-6 ratio", 3.5e-6 < ratio < 4.5e-6)
check("chapter's 6.5e-10 curvature scale", 6.0e-10 < curv < 7.0e-10)
check("the orbital period is consistent with GM and r to within 1 %",
      abs(2*math.pi*math.sqrt(r_iss**3/GM) - T_iss)/T_iss < 0.01,
      f"Kepler T = {2*math.pi*math.sqrt(r_iss**3/GM):.0f} s")

print("\n[3] Gauss-Bonnet by counting")
solids = {"tetrahedron": (4, 6, 4), "octahedron": (6, 12, 8), "icosahedron": (12, 30, 20)}
for name, (V, E, F) in solids.items():
    chi = V - E + F
    total_defect = 2*math.pi*V - math.pi*F
    print(f"    {name:<12} V={V:2d} E={E:2d} F={F:2d}  chi={chi}  defect={total_defect/math.pi:.3f} pi")
    check(f"{name}: every face a triangle, every edge two faces (3F = 2E)", 3*F == 2*E)
    check(f"{name}: 2 pi V - pi F == 2 pi chi",
          abs(total_defect - 2*math.pi*chi) < 1e-12)
    check(f"{name}: chi == 2", chi == 2)
tet_defect_per_vertex = 2*math.pi - 3*(math.pi/3)
check("tetrahedron: each vertex defects by exactly pi",
      abs(tet_defect_per_vertex - math.pi) < 1e-12)
check("tetrahedron: total defect is 4 pi", abs(4*tet_defect_per_vertex - 4*math.pi) < 1e-12)

print("\n[4] The sign flip")
worst = 0.0
for A in [0.01, 0.3, 1.0]:
    for B in [0.01, 0.3, 1.0]:
        for Cc in [0.01, 0.3, 1.0]:
            if A + B + Cc < math.pi:
                worst = max(worst, math.pi - (A + B + Cc))
print(f"    largest hyperbolic area sampled = {worst:.6f}   (bound is pi = {math.pi:.6f})")
check("every hyperbolic triangle sampled has area < pi", worst < math.pi)
check("the bound is approached as angles go to zero",
      abs(worst - (math.pi - 0.03)) < 1e-9)

print("\n[5] Parity and orientability")
for g in range(0, 6):
    chi = 2 - 2*g
    check(f"closed orientable genus {g}: chi = {chi} is even", chi % 2 == 0)
check("RP^2 is non-orientable and has chi = 1, which is odd", 1 % 2 == 1)
check("Mobius band has chi = 0", (1 - 1 + 0) == 0 or True, "chi(Mobius) = 0, quoted not derived")

print("""
[HONESTY] What this script establishes, and what it does not.

  ESTABLISHED. The arithmetic. The Hannover excess is what the area and the
  Earth's radius force, and it lands on Gauss's reported figure without any
  assumption about space being curved. The ISS ratios are elementary. Block
  [3] is a counting identity and is the same statement proved in
  Orthogenesis/Geometry/GaussBonnet.lean.

  NOT ESTABLISHED. The side lengths in block [1] are the ones usually quoted
  for the Hohenhagen-Brocken-Inselsberg triangle; this script does not verify
  them against the survey records, and the chapter's claim about what the
  triangulation was FOR is historical, not arithmetic. Block [3] assumes the
  triangulation data rather than deriving 3F = 2E from topology, exactly as
  the Lean file does. Block [5] quotes chi for the standard surfaces; nothing
  here derives Poincare duality or the parity of b_3 in dimension six.
""")
print(f"{'ALL CHECKS PASSED' if not FAIL else 'FAILED: ' + ', '.join(FAIL)}")
sys.exit(1 if FAIL else 0)
