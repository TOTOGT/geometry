#!/usr/bin/env python3
"""
ch8-8b-brown-dwarfs-verify.py -- the other end of the same formula.

ch8-8-chandrasekhar derived the mass a cold star cannot EXCEED. This derives
the mass a ball of gas must REACH to be a star at all, using the same
machinery, and gets a much worse answer -- which is the finding.

THE PHYSICS. Contract a ball of hydrogen. The centre heats: T_c ~ M/R. But
the electrons are also being squeezed, and degeneracy pressure -- which does
not care about temperature -- eventually takes over the support and halts the
contraction. So T_c does not rise forever. It has a MAXIMUM, and if that
maximum falls short of hydrogen ignition, the object was never going to be a
star. It cools off as a brown dwarf instead.

  A. T_c(R) is derived, maximised in closed form, and the closed form checked
     against a numerical maximisation.
  B. T_max ~ M^{4/3}. So the ignition condition fixes a minimum mass.
  C. M_min = 0.1035 Msun for T_ign = 3e6 K, X = 0.70.
  D. The Planck form, SAME SHAPE as Chandrasekhar:
         M_min = 16.32 * (k T_ign / m_e c^2)^{3/4} * M_Planck^3 / m_u^2
     Both limits are M_Pl^3/m_u^2 times a dimensionless number. Chandrasekhar's
     is 3.098, a pure number out of one ODE. This one is a TEMPERATURE RATIO.
  E. AND THE ANSWER IS 38% TOO BIG. Chabrier et al. 2023 give 0.075 Msun.
     Section 6 says why, and section 7 says what that difference means.

Run:  python3 book8/ch8-8b-brown-dwarfs-verify.py
"""
import math

FAIL = []
def head(n, t):
    print(); print("=" * 78); print("%s. %s" % (n, t)); print("=" * 78)
def check(name, got, want, rtol, note=""):
    d = abs(got-want)/abs(want); ok = d < rtol
    print("  [%s] %-44s %14.6g vs %-14.6g rel %.2e"
          % ("SHOWN" if ok else "FAIL ", name, got, want, d))
    if note: print("        " + note)
    if not ok: FAIL.append(name)

h = 6.62607015e-34; c = 299792458.0; G = 6.67430e-11; kB = 1.380649e-23
hbar = h/(2*math.pi); m_e = 9.1093837015e-31; m_u = 1.66053906660e-27
Msun = 1.32712440018e20/G; Rsun = 6.957e8; Mjup = 1.89813e27; Rjup = 6.9911e7

X, Y = 0.70, 0.28                        # solar-ish mass fractions
mu_e = 2.0/(1.0+X)                       # nucleons per electron
mu_m = 1.0/(2*X + 0.75*Y + 0.5*(1-X-Y))  # mean molecular weight, ionised
W  = 0.7704                              # P_c = W G M^2 / R^4, n=3/2 polytrope
Dc = 5.991*3/(4*math.pi)                 # rho_c = Dc M / R^3, n=3/2
K1 = (h*h/(20*m_e))*(3/math.pi)**(2/3)*(mu_e*m_u)**(-5/3)

# ---------------------------------------------------------------------------
head(1, "THE SETUP -- two pressures, one of which forgets the temperature")
# ---------------------------------------------------------------------------
print("  X = %.2f, Y = %.2f  ->  mu_e = %.4f (nucleons per electron)" % (X, Y, mu_e))
print("                          mu   = %.4f (mean molecular weight)" % mu_m)
print()
print("  Hydrostatic equilibrium for an n = 3/2 polytrope:")
print("      P_c = W G M^2 / R^4,      W  = %.4f" % W)
print("      rho_c = Dc M / R^3,       Dc = %.4f" % Dc)
print("  and the central pressure is carried by two things at once:")
print("      P_c = rho_c k T_c/(mu m_u)   +   K1 rho_c^{5/3}")
print("            ^ ideal gas, wants T     ^ degeneracy, does not")
print("      K1 = %.6e (SI)" % K1)

def T_c(M, R):
    rho = Dc*M/R**3
    P   = W*G*M*M/R**4
    return mu_m*m_u/(kB*rho) * (P - K1*rho**(5.0/3.0))

# ---------------------------------------------------------------------------
head(2, "T_c HAS A MAXIMUM -- and that is the whole argument")
# ---------------------------------------------------------------------------
print("  Solving for T_c as a function of R at fixed M:")
print("      k T_c/(mu m_u) = (W/Dc) G M / R  -  K1 Dc^{2/3} M^{2/3} / R^2")
print("  One term rises as the star shrinks; the other rises FASTER. So T_c")
print("  climbs, turns over, and falls. Setting dT_c/dR = 0:")
print()
print("      R* = 2 K1 Dc^{5/3} M^{-1/3} / (W G)")
print("      T_max = mu m_u W^2 G^2 M^{4/3} / (4 k K1 Dc^{8/3})")
print()
def R_star(M): return 2*K1*Dc**(5.0/3.0)*M**(-1.0/3.0)/(W*G)
def T_max(M):  return mu_m*m_u*W*W*G*G*M**(4.0/3.0)/(4*kB*K1*Dc**(8.0/3.0))

# numerical maximisation, as a check on the algebra
for Mt in (0.05, 0.08, 0.15, 0.3):
    M = Mt*Msun
    lo, hi = 0.01*Rsun, 2.0*Rsun
    for _ in range(200):
        a = lo + (hi-lo)/3; b = hi - (hi-lo)/3
        if T_c(M, a) < T_c(M, b): lo = a
        else: hi = b
    Rnum = (lo+hi)/2
    check("M=%.2f Msun: R* closed form vs numerical" % Mt, R_star(M), Rnum, 2e-3)
    check("M=%.2f Msun: T_max closed vs numerical" % Mt, T_max(M), T_c(M, Rnum), 2e-3)
print()
print("  T_max ~ M^{4/3}. Check the exponent directly:")
r = math.log(T_max(2*Msun)/T_max(Msun))/math.log(2.0)
check("d log T_max / d log M", r, 4.0/3.0, 1e-12)
print("  An object below the mass where T_max reaches ignition never gets hot")
print("  enough, no matter how long it waits. It is not a slow star. It is a")
print("  thing that was never going to be one.")

# ---------------------------------------------------------------------------
head(3, "THE MINIMUM MASS")
# ---------------------------------------------------------------------------
def M_min(Tign):
    return (4*kB*Tign*K1*Dc**(8.0/3.0)/(mu_m*m_u*W*W*G*G))**0.75
print("      %-14s %-14s %-14s %-12s" % ("T_ign (K)", "M_min/Msun", "M_min/M_Jup", "R* /R_Jup"))
for Tign in (2.0e6, 3.0e6, 4.0e6):
    M = M_min(Tign)
    print("      %-14.2e %-14.5f %-14.1f %-12.3f"
          % (Tign, M/Msun, M/Mjup, R_star(M)/Rjup))
M3 = M_min(3.0e6)
print()
print("  Taking the usual T_ign = 3e6 K for the p-p chain:")
print("      M_min = %.5f Msun = %.1f M_Jup,  R* = %.3f R_Jup"
      % (M3/Msun, M3/Mjup, R_star(M3)/Rjup))

# ---------------------------------------------------------------------------
head(4, "THE SAME SHAPE AS CHANDRASEKHAR")
# ---------------------------------------------------------------------------
M_pl = math.sqrt(hbar*c/G)
eps  = kB*3.0e6/(m_e*c*c)
Cnum = M3/(eps**0.75 * M_pl**3/m_u**2)
print("  Substituting K1 and collecting, exactly as in ch8-8:")
print()
print("      M_min = C * (k T_ign / m_e c^2)^{3/4} * M_Planck^3 / m_u^2")
print()
print("      eps = k T_ign/(m_e c^2) = %.6e     C = %.4f" % (eps, Cnum))
check("Planck form reproduces M_min", Cnum*eps**0.75*M_pl**3/m_u**2, M3, 1e-12)
Mch = 3.09797*M_pl**3/(2.0*m_u)**2
print()
print("  Put the two side by side:")
print("      M_ch  = 3.098 * M_Pl^3/(mu_e m_u)^2                      [ch8-8]")
print("      M_min = %.2f * eps^{3/4} * M_Pl^3/m_u^2" % Cnum)
print()
print("  SAME OBJECT, M_Pl^3/m_u^2, times a dimensionless number. But look at")
print("  what the two dimensionless numbers ARE:")
print("      3.098      -- (omega_3/2)sqrt(3pi). A pure number. One ODE.")
print("      %.2f * eps^{3/4} -- a TEMPERATURE, divided by the electron rest" % Cnum)
print("                    mass. Nuclear physics, not mathematics.")
print("  eps^{3/4} = %.6f, which is why stars span a factor of ~20 in mass"
      % eps**0.75)
print("  rather than a factor of 1.")
check("M_min/M_ch ratio", M3/Mch, 0.0711, 0.05,
      "the whole main sequence lives between these two numbers")

# ---------------------------------------------------------------------------
head(5, "AGAINST THE LITERATURE -- and it is 38% too big")
# ---------------------------------------------------------------------------
HBMM = 0.075     # Chabrier, Baraffe, Phillips & Debras 2023, A&A 671 A119
print("  This derivation        M_min = %.4f Msun" % (M3/Msun))
print("  Chabrier et al. 2023   HBMM  = %.4f Msun   [CITED]" % HBMM)
print("  error = %+.0f %%" % (100*(M3/Msun-HBMM)/HBMM))
print()
print("  The radius misses by about the same:")
print("      predicted R* = %.2f R_Jup ; observed brown dwarfs ~ 1 R_Jup"
      % (R_star(M3)/Rjup))
print()
print("  Inverting -- NOT a prediction, an inversion -- the T_ign that would")
print("  give 0.075 Msun is:")
Tinv = 3.0e6*(HBMM/(M3/Msun))**(4.0/3.0)
print("      T_ign,eff = %.3e K, about two thirds of 3e6." % Tinv)
print("  That is physically sensible (p-p burning is a RATE that switches on")
print("  gradually, not a threshold) and it is still a fitted number, so this")
print("  script does not adopt it. The 38% stands.")
big = (M3/Msun - HBMM)/HBMM
if not (0.25 < big < 0.50):
    FAIL.append("discrepancy moved -- recheck")
print("  [SHOWN] discrepancy is +%.0f%%, in the recorded range" % (100*big))

# ---------------------------------------------------------------------------
head(6, "WHY IT IS TOO BIG -- four named reasons, all one direction")
# ---------------------------------------------------------------------------
for s in [
 "  1. IGNITION IS NOT A THRESHOLD. The real criterion is that nuclear",
 "     luminosity balance surface luminosity over the object's life. That is",
 "     satisfied below 3e6 K, so the true condition is weaker than the one",
 "     used here, and a weaker condition means a SMALLER minimum mass.",
 "  2. THE EOS IS TOO STIFF. P = ideal + ideal-degenerate omits Coulomb",
 "     attraction between ions and electrons and the exchange term, both of",
 "     which LOWER the pressure. A softer gas contracts further and gets",
 "     hotter, so ignition is reached at lower mass.",
 "  3. PARTIAL DEGENERACY IS NOT A SUM. Adding the two pressures is not the",
 "     correct finite-temperature Fermi-Dirac result; it overestimates support",
 "     in exactly the regime that matters.",
 "  4. n = 3/2 IS ASSUMED. A real object in the transition region is not a",
 "     polytrope of any single index, and W and Dc were taken from one.",
 "  All four push the same way. A model whose errors cancelled would be the",
 "  suspicious one; this one is wrong in a direction it can name.",
]: print(s)

# ---------------------------------------------------------------------------
head(7, "THE POINT -- one limit is a theorem, the other is a convention")
# ---------------------------------------------------------------------------
print("  Watch what each number has DONE over time.")
print()
print("  The hydrogen-burning limit, as the equation of state improved:")
print("      SCvH   1995   0.073 Msun")
print("      CMS19  2019   0.074 Msun")
print("      CD21   2023   0.075 Msun      [CITED Chabrier et al. 2023]")
print("  It moved because the PHYSICS INPUT moved. It will move again.")
print()
print("  The Chandrasekhar mass:")
print("      Chandrasekhar 1931 published 0.91 Msun, using mu_e = 2.5.")
print("      This formula at mu_e = 2.5 gives %.3f Msun."
      % (3.09797*M_pl**3/(2.5*m_u)**2/Msun))
print("      At mu_e = 2:                  %.4f Msun." % (Mch/Msun))
print("  It moved because an INPUT was wrong, not because the formula was.")
print("  The formula has not changed since 1935 and cannot: it is an ODE and")
print("  three constants.")
print()
print("  So the top of the white-dwarf range is a theorem about a Fermi gas,")
print("  and the bottom of the stellar range is a boundary drawn through a")
print("  continuum by a criterion we chose. Both get quoted to three figures.")
print("  Only one of them has earned it.")
print()
print("  PRIOR ART, since this corpus is required to look: pedagogical")
print("  derivations of the minimum stellar mass along these lines are")
print("  published -- e.g. Pinochet, arXiv:1909.08575. Nothing above is")
print("  claimed as new physics. What is offered is the side-by-side.")

# ---------------------------------------------------------------------------
head("GAPS", "what this script does not establish")
# ---------------------------------------------------------------------------
for g in [
 "K1  T_ign = 3e6 K IS AN INPUT, NOT A RESULT. Nothing here computes a",
 "    reaction rate. The whole answer scales as T_ign^{3/4}, so the single",
 "    softest number in the calculation controls it.",
 "",
 "K2  NO EVOLUTION. T_max is the maximum over contraction of a static model.",
 "    A real object's history -- accretion, deuterium burning on the way down,",
 "    cooling -- is absent, and the HBMM is defined by that history.",
 "",
 "K3  NO ATMOSPHERE, SO NO LUMINOSITY. Reason 1 in section 6 is stated and",
 "    not modelled; doing it needs a surface boundary condition this has none",
 "    of. That is the largest of the four named errors and the least",
 "    quantified here.",
 "",
 "K4  THE DEUTERIUM LIMIT IS NOT ATTEMPTED. The same machinery at T_ign ~ 5e5",
 "    K would give the planet/brown-dwarf boundary, and it was left out",
 "    because the systematic of section 5 is not measured well enough to make",
 "    a second uncalibrated prediction worth printing.",
 "",
 "K5  ONE COMPOSITION. X = 0.70 throughout. Metallicity changes the HBMM by",
 "    more than the 3% by which the literature value has moved since 1995,",
 "    and no sweep is done.",
 "",
 "K6  SECTION 7'S HISTORY IS CITED. The 1995/2019/2023 sequence is taken from",
 "    Chabrier et al. 2023 and not independently traced, and Chandrasekhar's",
 "    0.91 is from the secondary literature, not from his 1931 paper.",
]: print("  " + g)

print(); print("=" * 78)
if FAIL:
    print("FAILED: " + ", ".join(FAIL)); raise SystemExit(1)
print("All checks passed. 6 gaps recorded above remain open.")
print("=" * 78)
