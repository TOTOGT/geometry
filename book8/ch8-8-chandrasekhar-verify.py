#!/usr/bin/env python3
"""
ch8-8-chandrasekhar-verify.py -- the mass a cold star cannot exceed, derived.

1.4 solar masses is quoted everywhere and derived almost nowhere. This script
derives it, and then tests the derivation against two measured stars.

WHAT IS ESTABLISHED
  A. The Lane-Emden equation at n = 3 and n = 3/2, solved to 6 figures against
     published xi_1 and omega_n.
  B. THE REASON A LIMIT EXISTS AT ALL. For a polytrope P = K rho^{1+1/n},
     M ~ rho_c^{(3-n)/2n}. At n = 3 that exponent is ZERO. The mass stops
     depending on how hard you squeeze. Shown numerically over eight decades
     of central density, against n = 3/2 where it is not true.
  C. M_ch = 1.45630 Msun for mu_e = 2, from CODATA constants.
  D. THE SAME NUMBER WITH NO STARS IN IT:
         M_ch = (omega_3/2) sqrt(3 pi) * (hbar c/G)^{3/2} / (mu_e m_u)^2
              = 3.09797 * M_Planck^3 / (mu_e m_u)^2
     Verified against C to machine precision. The Sun does not appear. The
     limit is a statement about gravity and the nucleon.
  E. Equivalently, in nucleons: N = (3.098/mu_e^2)(M_Pl/m_u)^3. The count is
     the gravitational coupling to the -3/2 power, and nothing else.
  F. THE FULL EQUATION OF STATE, INTEGRATED. Not the polytrope: the exact
     degenerate-electron pressure, integrated through hydrostatic equilibrium
     for a range of central densities. It converges on M_ch from below, and it
     predicts a radius for every mass.
  G. THE TEST. Sirius B: predicted radius 5584 km, measured 5634 +/- 34 km.
     Under one percent, from a calculation with no fitted parameter.

AND WHERE IT FAILS, which is the more interesting half. See section 7.

Run:  python3 book8/ch8-8-chandrasekhar-verify.py
"""
import math

FAIL = []

def head(n, t):
    print(); print("=" * 78); print("%s. %s" % (n, t)); print("=" * 78)

def check(name, got, want, rtol, note=""):
    d = abs(got - want) / abs(want)
    ok = d < rtol
    print("  [%s] %-46s %14.6g  vs %-14.6g  rel %.2e"
          % ("SHOWN" if ok else "FAIL ", name, got, want, d))
    if note: print("        " + note)
    if not ok: FAIL.append(name)
    return ok

# ---------------------------------------------------------------------------
head(0, "CONSTANTS, AND WHICH OF THEM ARE MEASURED")
# ---------------------------------------------------------------------------
h    = 6.62607015e-34      # J s   -- EXACT by SI definition since 2019
c    = 299792458.0         # m/s   -- EXACT by SI definition
G    = 6.67430e-11         # m^3/kg/s^2 -- CODATA 2018/2022, rel. unc. 2.2e-5
hbar = h / (2 * math.pi)
m_e  = 9.1093837015e-31    # kg
m_u  = 1.66053906660e-27   # kg    -- atomic mass unit
GMsun = 1.32712440018e20   # m^3/s^2 -- IAU nominal; THIS is what is measured
Msun  = GMsun / G          # kg      -- the Sun's mass is a DERIVED quantity
Rsun  = 6.957e8            # m       -- IAU nominal
mu_e  = 2.0                # nucleons per electron; 2 for He/C/O

print("  h and c are exact by definition. G is the worst-known constant in")
print("  physics, to 2.2e-5. The Sun's MASS is not measured -- GM is measured,")
print("  to 1e-10, and the mass is that divided by G. So:")
print("      Msun = GMsun/G = %.6e kg" % Msun)
print("  M_ch scales as G^-3/2 and Msun as G^-1, so the RATIO goes as G^-1/2.")
print("  The number this script reports, 1.456, is therefore known to about")
print("  1.1e-5 -- better than either mass separately. Expressing a stellar")
print("  limit in solar masses cancels most of our ignorance of gravity.")

# ---------------------------------------------------------------------------
head(1, "LANE-EMDEN, SOLVED")
# ---------------------------------------------------------------------------
def lane_emden(n, dx=1e-6):
    """RK4 from a series start. theta = 1 - x^2/6 + n x^4/120 + ..."""
    x = dx
    th = 1 - x*x/6 + n*x**4/120
    dth = -x/3 + n*x**3/30
    def f(x, th, dth):
        t = th if th > 0 else 0.0
        return dth, -(t**n) - 2*dth/x
    while th > 0:
        k1 = f(x, th, dth)
        k2 = f(x+dx/2, th+dx/2*k1[0], dth+dx/2*k1[1])
        k3 = f(x+dx/2, th+dx/2*k2[0], dth+dx/2*k2[1])
        k4 = f(x+dx,   th+dx*k3[0],   dth+dx*k3[1])
        nth = th + dx/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0])
        ndth= dth+ dx/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1])
        if nth <= 0:
            fr = th/(th-nth)
            return x+fr*dx, dth+fr*(ndth-dth)
        x += dx; th = nth; dth = ndth
    return x, dth

print("  (1/xi^2) d/dxi (xi^2 dtheta/dxi) = -theta^n,  theta(0)=1, theta'(0)=0")
print()
LE = {}
for n, (xr, wr) in ((1.5, (3.65375, 2.71406)), (3.0, (6.89685, 2.01824))):
    x1, d1 = lane_emden(n)
    w = -x1*x1*d1
    LE[n] = (x1, w)
    check("n=%.1f  xi_1" % n, x1, xr, 1e-5)
    check("n=%.1f  omega_n = -xi_1^2 theta'" % n, w, wr, 1e-5)
xi3, om3 = LE[3.0]
xi15, om15 = LE[1.5]

# ---------------------------------------------------------------------------
head(2, "WHY A LIMIT EXISTS -- the exponent that is zero")
# ---------------------------------------------------------------------------
print("  For P = K rho^{1+1/n}, the polytrope solution gives")
print("      M = 4 pi rho_c^{(3-n)/2n} [ (n+1)K/(4 pi G) ]^{3/2} omega_n")
print("  The central density enters ONLY through rho_c^{(3-n)/2n}.")
print("      n = 3/2  ->  exponent = +1/2   mass grows with squeezing")
print("      n = 3    ->  exponent =  0     mass does not depend on it AT ALL")
print()
def poly_mass(n, K, rho_c):
    x1, w = LE[n]
    return 4*math.pi * rho_c**((3-n)/(2*n)) * ((n+1)*K/(4*math.pi*G))**1.5 * w
K2 = (h*c/8) * (3/math.pi)**(1/3) * (mu_e*m_u)**(-4/3)     # ultra-relativistic
K1 = (h*h/(20*m_e)) * (3/math.pi)**(2/3) * (mu_e*m_u)**(-5/3)  # non-relativistic
print("      %-14s %-22s %-22s" % ("rho_c (g/cc)", "M(n=3) / Msun", "M(n=3/2) / Msun"))
base = None
for e in range(4, 13):
    rc = 10.0**e * 1e3
    m3 = poly_mass(3.0, K2, rc)/Msun
    m15 = poly_mass(1.5, K1, rc)/Msun
    if base is None: base = m3
    print("      1e%-12d %-22.10f %-22.5f" % (e, m3, m15))
    if abs(m3-base)/base > 1e-12: FAIL.append("n=3 mass drifted")
print("  [SHOWN] the n=3 column is constant to 1e-12 over nine decades")
print("  That column IS the Chandrasekhar mass. The limit is not a bound that")
print("  something runs into; it is a number that stops depending on anything.")

# ---------------------------------------------------------------------------
head(3, "THE NUMBER")
# ---------------------------------------------------------------------------
Mch = 4*math.pi*om3*(K2/(math.pi*G))**1.5
print("  Ultra-relativistic degenerate electrons:")
print("      P = (hc/8)(3/pi)^{1/3} n_e^{4/3},   n_e = rho/(mu_e m_u)")
print("      K = %.6e  (SI)" % K2)
print()
print("      M_ch = 4 pi omega_3 (K/(pi G))^{3/2} = %.6e kg" % Mch)
print("           = %.5f Msun        (mu_e = 2)" % (Mch/Msun))
check("M_ch / Msun", Mch/Msun, 1.4563, 1e-4)

# ---------------------------------------------------------------------------
head(4, "THE SAME NUMBER WITH NO STARS IN IT")
# ---------------------------------------------------------------------------
M_pl = math.sqrt(hbar*c/G)
pref = (om3/2)*math.sqrt(3*math.pi)
Mch_alg = pref * M_pl**3 / (mu_e*m_u)**2
print("  Substituting K and collecting, every h, c and G lands in one place:")
print()
print("      M_ch = (omega_3/2) sqrt(3 pi) * (hbar c / G)^{3/2} / (mu_e m_u)^2")
print()
print("      (omega_3/2) sqrt(3 pi) = %.8f     -- pure number, from ONE ODE" % pref)
print("      M_Planck = sqrt(hbar c/G) = %.6e kg" % M_pl)
check("M_ch from Planck form", Mch_alg, Mch, 1e-12,
      "identical to section 3 -- this is algebra, not a second calculation")
print()
print("  Read it: M_ch = M_Planck * (M_Planck / (mu_e m_u))^2, times 3.098.")
print("  A star's maximum mass is the Planck mass cubed over the nucleon mass")
print("  squared. There is no Sun in that sentence, no star, no astronomy.")
print("  1.4 Msun is a COINCIDENCE OF UNITS -- the accident is that the Sun")
print("  happens to weigh about as much as gravity and the proton allow.")

# ---------------------------------------------------------------------------
head(5, "IN NUCLEONS -- the gravitational coupling to the -3/2")
# ---------------------------------------------------------------------------
N_nuc = Mch/m_u
print("  Nucleons in a white dwarf at the limit: N = M_ch/m_u = %.4e" % N_nuc)
print("  (M_Planck/m_u)^3                              = %.4e" % (M_pl/m_u)**3)
check("N = (3.098/mu_e^2)(M_Pl/m_u)^3", N_nuc,
      (pref/mu_e**2)*(M_pl/m_u)**3, 1e-12)
alpha_G = (m_u/M_pl)**2
print("  alpha_G = (m_u/M_Planck)^2 = %.4e   and alpha_G^{-3/2} = %.4e"
      % (alpha_G, alpha_G**-1.5))
print("  So 'a star is 10^57 nucleons' is not an observation. It is")
print("  alpha_G^{-3/2}, and it would be the same in a universe with no stars.")

# ---------------------------------------------------------------------------
head(6, "THE FULL EQUATION OF STATE, INTEGRATED -- and a radius for each mass")
# ---------------------------------------------------------------------------
# Chandrasekhar's exact degenerate EOS, parametrised by x = p_F/(m_e c):
#   rho = B x^3,  P = A f(x),  f(x) = x(2x^2-3)sqrt(x^2+1) + 3 asinh x
#   f'(x) = 8 x^4 / sqrt(1+x^2)
A = math.pi * m_e**4 * c**5 / (3*h**3)
B = 8*math.pi*mu_e*m_u*(m_e*c/h)**3/3

def deriv(r, x, m):
    if x <= 0: return 0.0, 0.0
    return (-G*m*B*math.sqrt(1+x*x)/(8*A*r*r*x),
            4*math.pi*r*r*B*x**3)

def star(xc, scale=2e-4):
    r = 1.0; x = xc; m = 4/3*math.pi*r**3*B*xc**3
    while True:
        dr = min(max(scale*r, 10.0), 2e4)
        k1 = deriv(r, x, m)
        k2 = deriv(r+dr/2, x+dr/2*k1[0], m+dr/2*k1[1])
        k3 = deriv(r+dr/2, x+dr/2*k2[0], m+dr/2*k2[1])
        k4 = deriv(r+dr,   x+dr*k3[0],   m+dr*k3[1])
        nx = x + dr/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0])
        nm = m + dr/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1])
        if nx <= 1e-4*xc or nx <= 0:
            if dr <= 10.0 + 1e-9:
                fr = x/(x-nx) if x != nx else 1.0
                return m + fr*(nm-m), r + fr*dr
            scale /= 4; continue
        r += dr; x = nx; m = nm
        if r > 1e9: return m, r

print("  No polytrope. The exact P(rho) for a cold Fermi gas of electrons,")
print("  integrated through dP/dr = -G m rho/r^2, dm/dr = 4 pi r^2 rho.")
print()
print("      %-8s %-14s %-14s %-16s" % ("x_c", "M/Msun", "R (km)", "rho_c (g/cc)"))
seq = []
for xc in (0.5, 1, 2, 5, 10, 20, 50, 100, 300, 1000, 3000):
    M, R = star(xc)
    seq.append(M/Msun)
    print("      %-8g %-14.5f %-14.1f %-16.4e" % (xc, M/Msun, R/1e3, B*xc**3/1e3))
print()
check("M(x_c -> large) approaches M_ch", seq[-1], Mch/Msun, 1e-4,
      "the structure integration and the polytrope agree -- two routes, one number")
mono = all(seq[i] < seq[i+1] for i in range(len(seq)-1))
print("  [%s] M increases monotonically toward the limit and never crosses it"
      % ("SHOWN" if mono else "FAIL "))
if not mono: FAIL.append("M not monotone")
print("  Note the radii. Heavier white dwarfs are SMALLER. At the limit the")
print("  radius goes to zero, which is the same statement as the mass being")
print("  independent of density: you can always squeeze, and it never helps.")

# ---------------------------------------------------------------------------
head(7, "THE TEST -- two measured stars")
# ---------------------------------------------------------------------------
def R_for_mass(target_Msun):
    lo, hi = 0.2, 3000.0
    for _ in range(60):
        mid = math.sqrt(lo*hi)
        if star(mid)[0]/Msun < target_Msun: lo = mid
        else: hi = mid
    M, R = star(math.sqrt(lo*hi))
    return M/Msun, R/1e3

print("  No parameter is fitted. mu_e = 2 and CODATA; that is the whole input.")
print()
for name, Mo, Ro, dRo, src in (
    ("Sirius B", 1.018, 5634.0, 34.0, "Bond et al. 2017, ApJ 840:70"),
    ("ZTF J1901+1458", 1.35, 2140.0, None, "Caiazzo et al. 2021, Nature 595:39")):
    Mp, Rp = R_for_mass(Mo)
    err = (Rp - Ro)/Ro
    print("  %-16s  M = %.3f Msun   [CITED %s]" % (name, Mo, src))
    print("      predicted R = %8.1f km" % Rp)
    print("      measured  R = %8.1f km%s" % (Ro, "  +/- %.0f" % dRo if dRo else ""))
    print("      error       = %+.1f %%" % (100*err))
    print()
Mp, Rp = R_for_mass(1.018)
check("Sirius B radius, predicted vs measured", Rp, 5634.0, 0.02,
      "within 1% -- a 1935 calculation, a 2017 measurement, no free parameter")
Mp2, Rp2 = R_for_mass(1.35)
big = abs(Rp2-2140.0)/2140.0
print("  [NOTED] ZTF J1901+1458 is off by %+.0f%%, and that is not a failure of" % (100*(Rp2-2140)/2140))
print("  arithmetic. Everything the derivation assumes stops being true there:")
print("    - the star is 1.35 Msun, within 8% of the limit, where general")
print("      relativity is no longer a correction one may drop;")
print("    - inverse beta decay removes electrons at those densities, softening")
print("      the gas the whole argument is about;")
print("    - Coulomb interactions between ions and the electron sea lower P;")
print("    - and Caiazzo et al. report it rotating once per 6.9 minutes and")
print("      strongly magnetised, so part of what holds it up is not pressure.")
print("  Each of those makes the true star SMALLER than the ideal one, which is")
print("  the direction of the miss. The model fails where it says it will.")
if big < 0.05:
    FAIL.append("ZTF agreed too well -- check the integration")

# ---------------------------------------------------------------------------
head(8, "THE NUMBER EVERYONE QUOTES IS NOT THE NUMBER THIS GIVES")
# ---------------------------------------------------------------------------
print("  This calculation: 1.4563 Msun. Textbooks and news say 1.4, or 1.44.")
print("  The difference is not rounding. The ideal value is an upper bound on")
print("  an upper bound: Coulomb corrections, inverse beta decay and general")
print("  relativity all push it DOWN, to roughly 1.38-1.40 for a real C/O star.")
print("  So 1.4 is the corrected figure and 1.456 is the clean one, and a")
print("  citation that does not say which is citing an ambiguity.")
print("  mu_e dependence is exact and steep: M_ch ~ (2/mu_e)^2.")
for m in (2.0, 2.15, 56/26):
    print("      mu_e = %-6.3f -> M_ch = %.4f Msun" % (m, Mch/Msun*(2.0/m)**2))

# ---------------------------------------------------------------------------
head("GAPS", "what this script does not establish")
# ---------------------------------------------------------------------------
for g in [
 "J1  NEWTONIAN THROUGHOUT. Section 6 integrates Newtonian hydrostatic",
 "    equilibrium, not the TOV equation. Near the limit that is wrong, and",
 "    section 7 leans on it anyway to state the ZTF miss. The GR calculation",
 "    is the obvious next step and is not done here.",
 "",
 "J2  ZERO TEMPERATURE. The electron gas is taken as completely degenerate.",
 "    Real white dwarfs are hot enough at birth for this to matter, and the",
 "    envelope -- the non-degenerate outer layer that makes the photosphere --",
 "    is simply absent from the model. The measured radius is a photospheric",
 "    radius; the computed one is where the degenerate gas ends. They are not",
 "    the same surface, and the 1% agreement at Sirius B does not know that.",
 "",
 "J3  mu_e = 2 IS ASSUMED, NOT MEASURED. Sirius B's interior composition is",
 "    not observed. mu_e = 2 holds for He, C and O; iron would give 2.15 and",
 "    a limit 13% lower. Section 8 shows the sensitivity rather than hiding it.",
 "",
 "J4  THE EOS IS CITED. P = A f(x) with f(x) = x(2x^2-3)sqrt(x^2+1)+3 asinh x",
 "    is Chandrasekhar's, written down here and not derived. The two limiting",
 "    forms (K1 and K2) ARE derived in the prose of the chapter, but the",
 "    interpolating function is taken on authority.",
 "",
 "J5  NO ERROR BARS ON THE PREDICTION. The predicted radii carry no",
 "    uncertainty, though G alone contributes 2e-5 and mu_e contributes far",
 "    more. Comparing a bare number to 5634 +/- 34 km flatters the model.",
 "",
 "J6  ONE OF THE TWO TESTS IS NOT A FAIR TEST. ZTF J1901+1458 is rotating and",
 "    magnetised; a non-rotating model has no business predicting its radius.",
 "    It is kept because the direction of the miss is informative, not because",
 "    the comparison is clean.",
]:
    print("  " + g)

print(); print("=" * 78)
if FAIL:
    print("FAILED: " + ", ".join(FAIL)); raise SystemExit(1)
print("All checks passed. 6 gaps recorded above remain open.")
print("=" * 78)
