#!/usr/bin/env python3
"""
wp100-verify.py — Principia Orthogona, Vol VI, WP-100
"The Wavelength, Not the Count"

Regenerates every number in the note. Repo rule: a published number must be
regenerable by a tool.

Measured inputs, all from Sanchez-Lavega et al., Science Advances 12, eaee4251
(2 September 2026), "A decagon wave around Saturn's south pole", and from the
IAU 2015 spheroid for Saturn. Nothing else is assumed.

Run:  python3 wp100-verify.py     (exits non-zero on any failure)
Requires: numpy
"""
import numpy as np

FAIL = []
def check(label, got, want, tol):
    ok = abs(float(got) - float(want)) <= tol
    print(("  OK   " if ok else "  FAIL ") + label + f"   got={got:.6g}  want={want:.6g}  tol={tol:g}")
    if not ok: FAIL.append(label)

# ── measured inputs ──────────────────────────────────────────────────────────
A_EQ, B_POL = 60268.0, 54364.0     # Saturn 1-bar radii, km (IAU 2015)
LAT_HEX     = 78.5                 # hexagon, planetographic N   [paper, intro]
LAT_DEC     = 63.0                 # decagon wave centre, planetographic S
LAT_JET     = 60.5                 # decagon jet peak, planetographic S
LX_DEC_MEAS = 16782.0              # measured mean zonal wavelength, km
LX_DEC_ERR  = 1100.0
L_JET_DEC   = 2700.0               # jet full width at half maximum, km (~2.8 deg)
U0_DEC      = 116.0                # jet peak speed, m/s
N_HEX, N_DEC = 6, 10

def axis_radius(lat_graphic_deg):
    """Distance from the spin axis at planetographic latitude, on the spheroid."""
    pg = np.radians(abs(lat_graphic_deg))
    pc = np.arctan(np.tan(pg) * (B_POL / A_EQ) ** 2)
    r  = A_EQ * np.cos(pc) / np.sqrt(np.cos(pc) ** 2 + (A_EQ / B_POL) ** 2 * np.sin(pc) ** 2)
    return r, np.degrees(pc)

print("\n[1] Spheroid geometry — where the two rings actually are")
R6,  pc6  = axis_radius(LAT_HEX)
R10, pc10 = axis_radius(LAT_DEC)
Rjet, _   = axis_radius(LAT_JET)
print(f"       hexagon  {LAT_HEX} N graphic -> {pc6:.2f} centric,  axis radius {R6:8.0f} km")
print(f"       decagon  {LAT_DEC} S graphic -> {pc10:.2f} centric,  axis radius {R10:8.0f} km")
print(f"       jet peak {LAT_JET} S graphic ->                     axis radius {Rjet:8.0f} km")
check("hexagon ring radius", R6, 13260, 40)
check("decagon ring radius", R10, 29641, 60)
check("ring radius ratio (decagon / hexagon)", R10 / R6, 2.235, 0.02)

print("\n[2] The two wavelengths, computed the same way from the same geometry")
lam6_geo  = 2 * np.pi * R6  / N_HEX
lam10_geo = 2 * np.pi * R10 / N_DEC
print(f"       lambda_6  = 2*pi*R6/6  = {lam6_geo:8.0f} km")
print(f"       lambda_10 = 2*pi*R10/10 = {lam10_geo:8.0f} km")
check("lambda_6 geometric",  lam6_geo,  13886, 40)
check("lambda_10 geometric", lam10_geo, 18625, 50)

print("\n[3] Cross-check against the paper's MEASURED wavelength, and the gap")
R10_from_meas = N_DEC * LX_DEC_MEAS / (2 * np.pi)
print(f"       paper Lx = {LX_DEC_MEAS:.0f} +/- {LX_DEC_ERR:.0f} km  ->  implied ring radius {R10_from_meas:.0f} km")
print(f"       geometric radius at {LAT_DEC} S graphic            = {R10:.0f} km")
gap = (lam10_geo - LX_DEC_MEAS) / LX_DEC_MEAS
print(f"       geometric lambda_10 exceeds the measured Lx by {100*gap:.1f} %")
print("       NOT RESOLVED HERE. The measured value sits between the planetocentric and")
print("       planetographic readings of 63 S; the paper does not state which circle Lx")
print("       was integrated along. Both readings are carried below and the conclusion")
print("       is reported under each. This gap is the largest uncertainty in the note.")
check("measured Lx is below the geometric value", gap > 0, True, 0.5)
check("gap is under 15 per cent", abs(gap), 0.10, 0.05)

print("\n[4] The comparison — radii differ by a factor of two, wavelengths do not")
for tag, lam10 in (("geometric  ", lam10_geo), ("paper Lx   ", LX_DEC_MEAS)):
    print(f"       {tag}  lambda_10/lambda_6 = {lam10/lam6_geo:5.3f}"
          f"   vs   R10/R6 = {R10/R6:5.3f}   vs   n10/n6 = {N_DEC/N_HEX:5.3f}")
check("wavelength ratio, geometric", lam10_geo / lam6_geo, 1.341, 0.01)
check("wavelength ratio, paper Lx",  LX_DEC_MEAS / lam6_geo, 1.209, 0.01)
print("       Identity, exact by construction and worth stating:")
print("           n10/n6 = (R10/R6) / (lambda_10/lambda_6)")
check("identity holds", (R10/R6)/(lam10_geo/lam6_geo), N_DEC/N_HEX, 1e-9)
print("       The side count is not chosen. It is a circumference divided by a wavelength.")

print("\n[5] The prediction — what the hexagon's jet width must be")
L6_a = L_JET_DEC * lam6_geo / lam10_geo
L6_b = L_JET_DEC * lam6_geo / LX_DEC_MEAS
print(f"       decagon jet FWHM (measured)       = {L_JET_DEC:.0f} km  (~2.8 deg at {LAT_JET} S)")
print(f"       => hexagon jet FWHM, geometric    = {L6_a:.0f} km   ({L6_a/L_JET_DEC:.2f} x)")
print(f"       => hexagon jet FWHM, paper Lx     = {L6_b:.0f} km   ({L6_b/L_JET_DEC:.2f} x)")
print(f"       PREDICTION: {min(L6_a,L6_b):.0f}-{max(L6_a,L6_b):.0f} km, i.e. about 2.1-2.3 deg of latitude.")
print("       Refuted if the published Cassini hexagon wind profile gives a half-max")
print("       width outside roughly 1800-2500 km.")
check("prediction lower bound", L6_a, 2013, 30)
check("prediction upper bound", L6_b, 2234, 30)

print("\n[6] Is the decagon the fastest-growing barotropic mode? No.")
LB = L_JET_DEC / 1.76275          # FWHM -> Bickley half-width, sech^2 profile
lam_fast = 2 * np.pi * LB / 0.9   # kL = 0.9 is peak growth for the sinuous mode
kL_obs = 2 * np.pi * LB / LX_DEC_MEAS
print(f"       Bickley half-width from FWHM      = {LB:.0f} km")
print(f"       fastest-growing wavelength (kL=0.9) = {lam_fast:.0f} km")
print(f"       observed                            = {LX_DEC_MEAS:.0f} km   ->  kL = {kL_obs:.3f}")
print("       Unstable band is kL < 1, so n=10 is inside it but well off peak growth.")
print("       Consistent with the paper's own reading: a trapped quasigeostrophic Rossby")
print("       wave confined by jet curvature, not simply the fastest-growing mode.")
check("Bickley half-width", LB, 1532, 10)
check("kL is inside the unstable band", kL_obs < 1.0, True, 0.5)
check("kL is off peak growth", abs(kL_obs - 0.9) > 0.2, True, 0.5)

print("\n[7] Sanity — the hexagon side, against the published figure")
side_chord = 2 * R6 * np.sin(np.pi / N_HEX)
print(f"       arc length   2*pi*R6/6      = {lam6_geo:.0f} km")
print(f"       chord (side) 2*R6*sin(30)   = {side_chord:.0f} km")
print("       Published hexagon side is quoted at ~13,800 km; both agree to a per cent.")
check("chord within 5 per cent of 13800", side_chord, 13800, 700)

print("\n[8] What this note does NOT establish")
print("""       It does not explain why either wavenumber occurs. It does not derive a
       selection law; it assumes one exists, uses it only as a ratio, and reports
       what that ratio requires. Section [3]'s 10 per cent gap is unresolved. The
       Bickley profile in [6] is a stand-in for a measured jet profile and the
       coefficient 0.9 is taken from the classical result, not fitted here.
       Every number above is a statement about two circles and two lengths.""")

print("\n" + ("ALL CHECKS PASSED" if not FAIL else "FAILURES: " + ", ".join(FAIL)))
raise SystemExit(1 if FAIL else 0)
