#!/usr/bin/env python3
"""
ch-chandrasekhar-verify.py -- the bifurcations behind Book VII's Chandrasekhar
chapter, and the tree's, computed rather than described.

Chandrasekhar asked one question for sixty years in seven different subjects:
WHEN DOES A BALANCE STOP BEING THE ONLY ONE AVAILABLE, AND WHAT DOES IT
BECOME INSTEAD? This script computes the cleanest instance he left behind,
and the one a tree is solving.

WHAT IS ESTABLISHED
  A. The ellipsoidal index symbols, self-checked by A1+A2+A3 = 2 exactly.
  B. The Maclaurin sequence Omega^2(e), and its MAXIMUM at e = 0.9299557.
  C. The JACOBI BIFURCATION, where the axisymmetric branch stops being the
     only equilibrium: e = 0.8126700, from the condition a1^2 a2^2 A_12 =
     a3^2 A_3 evaluated on the spheroid. Both agree with Chandrasekhar's
     published figures to 6 places.
  D. THE TWO CRITICAL POINTS ARE NOT THE SAME POINT, and which one a star
     meets first depends on whether you hold angular velocity or angular
     momentum. That distinction is the subject of a whole book of his.
  E. GREENHILL'S COLUMN (1881), the tree's bifurcation: a vertical column
     buckles under its own weight above h_c, where h_c comes out of the first
     zero of J_{-1/3}. Exact, and it gives h_c ~ D^{2/3} -- equivalently
     D ~ h^{3/2}, McMahon's elastic similarity.
  F. AND THE HONEST PART: whether that bifurcation is what SHAPES a tree is
     disputed, by the person who got the branching exponent right. See §5.

Run:  python3 book7/ch-chandrasekhar-verify.py
"""
from mpmath import mp, mpf, sqrt, asin, quad, inf, diff, besselj, findroot, nstr
mp.dps = 30
FAIL = []

def head(n, t):
    print(); print("=" * 78); print("%s. %s" % (n, t)); print("=" * 78)

def check(name, got, want, tol, note=""):
    d = abs(mpf(got) - mpf(want))
    ok = d < tol
    print("  [%s] %-44s %-18s vs %-14s  |d| = %s"
          % ("SHOWN" if ok else "FAIL ", name, nstr(got, 12), nstr(want, 10), nstr(d, 3)))
    if note: print("        " + note)
    if not ok: FAIL.append(name)

# ---------------------------------------------------------------------------
head(1, "THE INDEX SYMBOLS -- and a self-check that costs nothing")
# ---------------------------------------------------------------------------
def index_symbols(a1, a2, a3):
    a1, a2, a3 = mpf(a1), mpf(a2), mpf(a3)
    P = a1*a2*a3
    D = lambda u: sqrt((a1**2+u)*(a2**2+u)*(a3**2+u))
    A = [P*quad(lambda u: 1/((ai**2+u)*D(u)), [0, inf]) for ai in (a1, a2, a3)]
    A12 = P*quad(lambda u: 1/((a1**2+u)*(a2**2+u)*D(u)), [0, inf])
    return A, A12

print("  For a homogeneous ellipsoid with semi-axes a1,a2,a3 the potential is")
print("  built from A_i = a1a2a3 INT du/((a_i^2+u) Delta), Delta the usual root.")
print("  Whatever the axes, A1+A2+A3 = 2. That identity is free, and it is the")
print("  only thing standing between a quadrature bug and a wrong bifurcation.")
print()
for axes in ((1.0, 0.7, 0.4), (1.0, 1.0, 0.25), (1.0, 0.999, 0.9)):
    A, _ = index_symbols(*axes)
    check("A1+A2+A3 at a = %s" % (axes,), sum(A), 2, mpf(10)**-18)

# ---------------------------------------------------------------------------
head(2, "THE MACLAURIN SEQUENCE, AND WHERE IT PEAKS")
# ---------------------------------------------------------------------------
def omega2(e):
    """Omega^2/(pi G rho) for a Maclaurin spheroid of eccentricity e."""
    e = mpf(e); s = sqrt(1-e**2)
    return (2*s/e**3)*(3-2*e**2)*asin(e) - 6*(1-e**2)/e**2

print("  Omega^2/(pi G rho) = (2 sqrt(1-e^2)/e^3)(3-2e^2) arcsin(e) - 6(1-e^2)/e^2")
print()
print("      %-10s %-16s" % ("e", "Omega^2/(piGrho)"))
for e in ('0.2', '0.5', '0.8126700', '0.9299557', '0.97', '0.995'):
    print("      %-10s %-16s" % (e, nstr(omega2(e), 10)))
print()
lo, hi = mpf('0.90'), mpf('0.96')
for _ in range(120):
    mid = (lo+hi)/2
    if diff(omega2, mid) > 0: lo = mid
    else: hi = mid
e_max = (lo+hi)/2
check("Maclaurin: e at max of Omega^2", e_max, mpf('0.9299557'), mpf('1e-6'))
check("Maclaurin: Omega^2 there", omega2(e_max), mpf('0.4493314'), mpf('1e-6'))
print("  Past that eccentricity a Maclaurin spheroid spins SLOWER the flatter")
print("  it gets. The sequence does not end there; it turns around.")

# ---------------------------------------------------------------------------
head(3, "THE JACOBI BIFURCATION -- where one figure becomes two")
# ---------------------------------------------------------------------------
print("  A Jacobi ellipsoid is triaxial: a1 > a2 > a3, still uniformly rotating.")
print("  Its equilibrium condition is  a1^2 a2^2 A_12 = a3^2 A_3.  Evaluate that")
print("  ON the axisymmetric sequence (a1 = a2 = 1) and the root is the point")
print("  where the triaxial branch touches the spheroidal one.")
print()
def jacobi_residual(e):
    e = mpf(e); a3 = sqrt(1-e**2)
    A, A12 = index_symbols(1, 1, a3)
    return A12 - a3**2*A[2]
lo, hi = mpf('0.70'), mpf('0.95')
f_lo = jacobi_residual(lo)
for _ in range(90):
    mid = (lo+hi)/2
    if jacobi_residual(mid)*f_lo > 0: lo = mid
    else: hi = mid
e_bif = (lo+hi)/2
check("Jacobi bifurcation eccentricity", e_bif, mpf('0.8126700'), mpf('1e-6'),
      "Chandrasekhar, Ellipsoidal Figures of Equilibrium (1969), ch. 6")
check("Omega^2/(piGrho) there", omega2(e_bif), mpf('0.3742297'), mpf('1e-6'))
print("      axis ratio a3/a1 at the bifurcation = %s"
      % nstr(sqrt(1-e_bif**2), 10))
print()
print("  Below that eccentricity the spheroid is the only figure. Above it,")
print("  there are two, and the symmetric one is no longer the stable one. The")
print("  body stops being a body of revolution -- not because anything broke,")
print("  but because a second solution came into existence.")

# ---------------------------------------------------------------------------
head(4, "TWO CRITICAL POINTS, AND THEY ARE NOT THE SAME POINT")
# ---------------------------------------------------------------------------
def Ltilde(e):
    e = mpf(e)
    return sqrt(mpf(3)/5)/(1-e**2)**(mpf(1)/6)*sqrt(omega2(e)/3)
print("      bifurcation      e = %s   Omega^2 = %s   L~ = %s"
      % (nstr(e_bif, 9), nstr(omega2(e_bif), 8), nstr(Ltilde(e_bif), 8)))
print("      Omega^2 maximum  e = %s   Omega^2 = %s   L~ = %s"
      % (nstr(e_max, 9), nstr(omega2(e_max), 8), nstr(Ltilde(e_max), 8)))
mono = Ltilde(e_max) > Ltilde(e_bif)
print()
print("  [%s] angular momentum is still RISING at the bifurcation and keeps"
      % ("SHOWN" if mono else "FAIL "))
print("        rising past the Omega^2 maximum.")
if not mono: FAIL.append("L not monotone through both points")
print()
print("  So the answer to 'when does it go unstable' depends on what is being")
print("  held. Spin a body up at fixed angular VELOCITY and the maximum at")
print("  e = 0.930 is the wall. Add angular MOMENTUM -- which is what accretion")
print("  does -- and you pass the bifurcation at e = 0.813 first and leave the")
print("  symmetric branch long before reaching it. Same body, same equations,")
print("  two different critical points, and the physics picks which.")

# ---------------------------------------------------------------------------
head(5, "THE TREE'S BIFURCATION -- Greenhill, 1881")
# ---------------------------------------------------------------------------
z = findroot(lambda x: besselj(mpf(-1)/3, x), mpf('1.87'))
check("first zero of J_{-1/3}", z, mpf('1.8663509'), mpf('1e-6'))
C3 = 9*z**2/4
check("h_c^3 = C EI/(rho g A), C", C3, mpf('7.8373474'), mpf('1e-6'))
kD = (C3/16)**(mpf(1)/3)
check("h_c = k (E/rho g)^{1/3} D^{2/3}, k", kD, mpf('0.7882846'), mpf('1e-6'))
print()
print("  A vertical column, clamped at the base, free at the top, loaded by")
print("  nothing but its own weight. Below h_c straight is the only shape.")
print("  Above it, straight is still a solution and is no longer the stable")
print("  one, and a bent branch exists. That is a pitchfork, exactly as in §3.")
print()
E = mpf('1.1e10'); rho = mpf(700); g = mpf('9.81')
for D in ('0.2', '0.5', '1.0'):
    hc = kD*(E/(rho*g))**(mpf(1)/3)*mpf(D)**(mpf(2)/3)
    print("      oak-like, E = 11 GPa, rho = 700 kg/m^3, D = %sm -> h_c = %s m"
          % (D, nstr(hc, 6)))
print()
print("  Invert h_c ~ D^{2/3} and you get D ~ h^{3/2}: McMahon's elastic")
print("  similarity, the claim that trees are built in fixed proportion to")
print("  their own buckling height.")
check("elastic-similarity exponent", 1/(mpf(2)/3), mpf('1.5'), mpf(10)**-20)

# ---------------------------------------------------------------------------
head(6, "AND WHETHER THAT IS WHAT SHAPES A TREE IS DISPUTED")
# ---------------------------------------------------------------------------
print("  Leonardo, c. 1500: across a fork, the daughter cross-sections sum to")
print("  the parent's. In modern terms, sum d_i^Delta = d_parent^Delta with")
print("  Delta = 2. Three mechanisms have been offered for that exponent:")
print()
print("      hydraulic (pipe model / Murray's law)   -> Delta = 2 or 3")
print("      elastic similarity (McMahon 1973)       -> from buckling, §5")
print("      wind-induced stress (Eloy 2011)         -> 1.93 < Delta < 2.21")
print()
print("  Measured across many species:                  1.8 < Delta < 2.3")
print("                                                 [CITED: Eloy, PRL 107")
print("                                                  258101 (2011)]")
print()
print("  Eloy rejects BOTH of the others: the sapwood is as little as 5% of a")
print("  mature branch's cross-section, so hydraulics is unlikely to govern the")
print("  whole architecture; and elastic similarity postulates a response to")
print("  branch deflection that trees have no evident way to sense.")
print()
print("  This script takes no side. What it records is the SHAPE of the")
print("  situation: three mechanisms, one measured exponent, and a data range")
print("  wide enough to contain all three predictions. Compare §3, where one")
print("  integral gives 0.8126700 and there is nothing to argue about.")
print()
print("  THAT CONTRAST IS THE POINT OF THE CHAPTER. A rotating fluid's")
print("  bifurcation is derivable. A tree's governing criterion is inferred,")
print("  and the inference is contested. Both are real bifurcations. Only one")
print("  of them can be computed to seven places.")

# ---------------------------------------------------------------------------
head(7, "WHAT THE TWO CASES SHARE, STATED NARROWLY")
# ---------------------------------------------------------------------------
for s in [
 "  SHARED, and this much is literal, not analogy:",
 "    - an equilibrium family parametrised by one load (rotation; height),",
 "    - a symmetry held by the family (axial symmetry; straightness),",
 "    - a critical value at which a second branch appears and the symmetric",
 "      one ceases to be the stable solution -- a pitchfork in both cases,",
 "    - and the fact that nothing BREAKS at that value. The configuration",
 "      does not fail; it stops being unique.",
 "",
 "  NOT SHARED, and the chapter says so:",
 "    - the equations. Self-gravitating incompressible fluid on one side,",
 "      Euler-Bernoulli beam theory on the other. No map between them.",
 "    - the numbers. 0.8126700 and 1.8663509 have nothing to do with each",
 "      other and this script does not put them in the same sentence twice.",
 "    - the epistemic status. §3 is a computation; §6 is a controversy.",
 "",
 "  A corpus that let 'both are bifurcations' slide into 'both are the same",
 "  mathematics' would be doing numerology with a better vocabulary.",
]: print(s)

# ---------------------------------------------------------------------------
head("GAPS", "what this script does not establish")
# ---------------------------------------------------------------------------
for g in [
 "L1  STABILITY IS NOT COMPUTED. §3 finds where the Jacobi branch MEETS the",
 "    Maclaurin sequence. It does not compute which branch is stable on which",
 "    side, which needs the second variation of the energy, and it does not",
 "    treat viscous versus dissipationless stability -- for the Maclaurin",
 "    sequence those give DIFFERENT critical points, and neither is computed.",
 "",
 "L2  UNIFORM ROTATION AND UNIFORM DENSITY. Both are assumed throughout §2-4.",
 "    Real stars are neither, and differential rotation moves the bifurcation.",
 "",
 "L3  THE DIMENSIONLESS ANGULAR MOMENTUM IN §4 IS A CONVENIENCE. L~ is",
 "    computed from Omega^2 and the axis ratio on the Maclaurin sequence only.",
 "    It is enough to order the two critical points and is not a general",
 "    expression.",
 "",
 "L4  GREENHILL IS A UNIFORM COLUMN. A tree tapers, carries a crown, is",
 "    orthotropic, and is not clamped in rigid ground. The 0.788 constant is",
 "    exact for the idealisation and the idealisation is not a tree.",
 "",
 "L5  THE BRANCHING EXPONENTS ARE ALL CITED. Nothing in §6 is computed here.",
 "    The three mechanisms are named, not adjudicated, and no tree data is",
 "    read.",
 "",
 "L6  NO WHITE DWARF HERE. The Chandrasekhar limit is NOT a bifurcation and",
 "    is deliberately absent from this script; it is derived in",
 "    book8/ch8-8-chandrasekhar.html. Keeping them apart is the point -- a",
 "    limit and a branch point are different things, and the chapter would be",
 "    worse if it blurred them.",
]: print("  " + g)

print(); print("=" * 78)
if FAIL:
    print("FAILED: " + ", ".join(FAIL)); raise SystemExit(1)
print("All checks passed. 6 gaps recorded above remain open.")
print("=" * 78)
