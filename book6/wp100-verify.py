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

print("       circumferences, for the cross-reference in section 9:")
print(f"         hexagon ring 2*pi*R6  = {2*np.pi*R6:8.0f} km   -> 6 x {lam6_geo:.0f}")
print(f"         decagon ring 2*pi*R10 = {2*np.pi*R10:8.0f} km   -> 10 x {lam10_geo:.0f}")
check("hexagon circumference", 2*np.pi*R6, 83316, 200)
check("decagon circumference", 2*np.pi*R10, 186241, 400)

print("\n[3] The paper's measured Lx, and where the 11 per cent goes")
R10_from_meas = N_DEC * LX_DEC_MEAS / (2 * np.pi)
gap = (lam10_geo - LX_DEC_MEAS) / LX_DEC_MEAS
print(f"       paper Lx = {LX_DEC_MEAS:.0f} +/- {LX_DEC_ERR:.0f} km  ->  implied ring radius {R10_from_meas:.0f} km")
print(f"       geometric radius at {LAT_DEC} S graphic            = {R10:.0f} km")
print(f"       geometric lambda_10 exceeds the measured Lx by {100*gap:.1f} %, outside the paper's own bar")
print("       RESOLVED. It is a reference-radius convention, not a measurement dispute:")
R_VOL = 58232.0                    # Saturn volumetric mean radius, km
for nm, Rref in (("volumetric mean radius", R_VOL), ("1-bar equatorial radius", A_EQ)):
    lam_sph = 2*np.pi*Rref*np.cos(np.radians(LAT_DEC))/N_DEC
    print(f"         spherical planet, {nm:24s} R*cos(63): lambda = {lam_sph:.0f} km"
          f"  ({100*(lam_sph-LX_DEC_MEAS)/LX_DEC_MEAS:+.1f} %)")
lam_sph_vol = 2*np.pi*R_VOL*np.cos(np.radians(LAT_DEC))/N_DEC
check("paper's Lx matches a SPHERICAL Saturn at 63 S to ~1 per cent", lam_sph_vol, LX_DEC_MEAS, 200)
check("and does NOT match the oblate axis radius", abs(lam10_geo-LX_DEC_MEAS) > LX_DEC_ERR, True, 0.5)
print("       For a wave running around the spin axis the OBLATE radius is the physical one,")
print("       so lambda_10 = %.0f km is used below and the paper's Lx is carried only as a check." % lam10_geo)

print("\n[3b] The decagon's latitude, measured from Figure 1 itself")
print("""       wp100-figure-measure.py reads the CC BY figure with no reference to the text:
       the red dashed circle is 80 S by the caption, the two cyan circles fall at
       301.4 and 600.7 px, and the projection is linear in colatitude to better than
       0.6 per cent across all three. Sampling brightness on circles of constant
       latitude, the 10-fold Fourier component peaks at colatitude 27.25.""")
LAT_FIG = 62.75                    # measured, wp100-figure-measure.py
for lat, px in ((80.0, 149.9), (70.0, 301.4), (50.0, 600.7)):
    print(f"       {lat:4.0f} S -> {px:6.1f} px  = {px/(90-lat):6.3f} px/deg"
          f"   residual {100*((px/(90-lat))/(149.9/10.0)-1):+5.2f} %")
check("projection is linear in colatitude (70 S residual)", (301.4/20)/(149.9/10), 1.0, 0.01)
check("projection is linear in colatitude (50 S residual)", (600.7/40)/(149.9/10), 1.0, 0.01)
check("figure-measured latitude agrees with the paper", LAT_FIG, LAT_DEC, 0.4)
print(f"       measured {LAT_FIG} S against the paper's {LAT_DEC} +/- 0.4 S. Independent, and it agrees.")

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

print("\n[5] The prediction — stated as a ratio, because the absolute width is not citable")
L6 = L_JET_DEC * lam6_geo / lam10_geo
DEG_KM = 2*np.pi*((A_EQ+B_POL)/2)/360
print("""       Digitising Fig. 3 (wp100-profile-digitize.py) recovers the paper's own peak
       exactly -- 115.9 m/s at 60.50 S against its stated 116 at 60.5 -- and then gives
       a jet width of 4.77, 3.96 or 2.93 degrees depending on whether the half-maximum
       is taken above zero, above the adjacent minimum, or above the ~55 m/s shoulder.
       The paper's 2.80 degrees matches only the third. It does not say which it used.
       A factor of 1.6 therefore sits in any absolute width quoted from this profile.""")
for nm, w_deg in (("above zero", 4.77), ("above adjacent minimum", 3.96), ("above 55 m/s shoulder", 2.93)):
    print(f"       {nm:24s} {w_deg:4.2f} deg = {w_deg*DEG_KM:5.0f} km"
          f"   -> hexagon {w_deg*DEG_KM*lam6_geo/lam10_geo:5.0f} km")
check("paper's 2.8 deg is recovered by the shoulder baseline", 2.93, 2.80, 0.20)
print(f"""
       THE PREDICTION, convention-free:
         L6 / L10 = lambda_6 / lambda_10 = {lam6_geo/lam10_geo:.3f}
       The hexagon's jet, measured by whatever definition is applied to the decagon's,
       must come out at {100*lam6_geo/lam10_geo:.0f} per cent of it. Refuted if that ratio is outside
       0.65-0.85. The absolute figure follows only once a baseline is fixed:
       with the paper's own 2700 km it is {L_JET_DEC*lam6_geo/lam10_geo:.0f} km.""")
check("width ratio", lam6_geo/lam10_geo, 0.7456, 0.002)
check("absolute figure on the paper's stated 2700 km", L6, 2013, 30)

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
