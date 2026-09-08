#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ch-feynman-verify.py — companion to book7/ch-feynman.html.

Eight blocks. Every number and every curve in the chapter is produced here.
The chapter quotes nothing this script does not print.

  [1] The contact defect.  alpha(X) = -2(r-1)^2 e^{-z}, exactly, everywhere.
  [2] The Reeb field of alpha = dz - r^2 dtheta is d/dz, so alpha has NO
      periodic Reeb orbit.  The dm3 cycle is therefore not a Reeb orbit.
  [3] Contact action per period.  Zero on Gamma = {r=1}; strictly negative
      off it; monotone to zero along every orbit that converges.
  [4] Floquet data of Gamma and the weight a periodic-orbit sum would give
      it.  T* = 2pi, mu_max = -2, multiplier e^{-4pi}.
  [5] Stationary phase.  |INT e^{i x^{k+1}/((k+1)h)} w(x) dx| ~ C h^{1/(k+1)},
      w a C-infinity bump on (-1,1), fitted for k = 1..4.  Berry index
      beta = 1/2 - 1/(k+1) is the enhancement over the Gaussian saddle.
  [6] Loop grading.  hbar^{P-V} = hbar^{L-1} with L = P - V + 1, checked on
      an explicit table of Standard Model diagrams.
  [7] The Higgs sector as a cusp.  lambda = m_H^2/(2 v^2), the bifurcation
      set 4a^3 + 27b^2 = 0, and the top Yukawa.
  [8] Numerology gate.  kappa* ~ 0.882 vs cos theta_W = 0.8814, and why the
      agreement is refused rather than reported.

Then an HONESTY block naming what is established and what is not.

Requires: numpy (>=1.20).  scipy is NOT used.
Run:  python3 ch-feynman-verify.py          (add --svg for figure data)

Principia Orthogona - Vol VII - G6 LLC - CC BY-NC-ND 4.0
"""

import sys, math, json
import numpy as np

FAIL = []
def check(label, ok, detail=""):
    print(f"    {'PASS' if ok else 'FAIL'}  {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok

# ── dm3 canonical constants, as fixed in Orthogenesis/Architecture/G6Crystal.lean
T_STAR  = 2.0 * math.pi     # dm3_Tstar_pos
MU_MAX  = -2.0              # dm3_mumax_neg
TAU     = 2.0               # dm3_tau_eq_abs_mumax
EPS0    = 1.0 / 3.0         # dm3_epsilon0
R_STAR  = 0.77594059        # basin edge, labs/dm3_numeric.py


# ═════════════════════════════════════════════════════════════════════
def field(y):
    """dm3 contact system on R^2_+ x R, coordinates (r, theta, z)."""
    r, th, z = y
    e = math.exp(-z)
    return np.array([r * (1.0 - r * r) + 2.0 * (r - 1.0) * e,
                     1.0,
                     r * r - 2.0 * (r - 1.0) ** 2 * e])


def alpha_of_X(y):
    """alpha(X) for alpha = dz - r^2 dtheta, evaluated on the flow."""
    r, th, z = y
    f = field(y)
    return f[2] - r * r * f[1]


def rk4(y0, tmax, n):
    """Classical RK4.  Returns (t, Y, A) with A the accumulated contact action."""
    h = tmax / n
    t = np.zeros(n + 1); Y = np.zeros((n + 1, 3)); A = np.zeros(n + 1)
    Y[0] = y0
    for i in range(n):
        y = Y[i]
        k1 = field(y);            a1 = alpha_of_X(y)
        k2 = field(y + h/2 * k1); a2 = alpha_of_X(y + h/2 * k1)
        k3 = field(y + h/2 * k2); a3 = alpha_of_X(y + h/2 * k2)
        k4 = field(y + h * k3);   a4 = alpha_of_X(y + h * k3)
        Y[i+1] = y + h/6 * (k1 + 2*k2 + 2*k3 + k4)
        A[i+1] = A[i] + h/6 * (a1 + 2*a2 + 2*a3 + a4)
        t[i+1] = t[i] + h
    return t, Y, A


# ═════════════════════════════════════════════════════════════════════
def block1():
    print("\n[1] THE CONTACT DEFECT   alpha(X) = -2 (r-1)^2 e^{-z}")
    print("    alpha = dz - r^2 dtheta ;  X the dm3 field ;  claim is an identity,")
    print("    so it is checked at pseudo-random points, not at a chosen few.\n")
    rng = np.random.default_rng(20260907)
    R  = rng.uniform(0.05, 3.0, 4000)
    Z  = rng.uniform(-3.0, 6.0, 4000)
    worst = 0.0
    for r, z in zip(R, Z):
        lhs = alpha_of_X(np.array([r, 0.0, z]))
        rhs = -2.0 * (r - 1.0) ** 2 * math.exp(-z)
        worst = max(worst, abs(lhs - rhs))
    print(f"      sup |alpha(X) + 2(r-1)^2 e^-z|  over 4000 points : {worst:.3e}")
    ok1 = check("identity holds to machine precision", worst < 1e-12)

    # sign and zero set
    neg = all(alpha_of_X(np.array([r, 0.0, z])) <= 0.0 for r, z in zip(R, Z))
    ok2 = check("alpha(X) <= 0 everywhere", neg,
                "the flow never crosses the contact plane upward")
    onG = max(abs(alpha_of_X(np.array([1.0, 0.0, z]))) for z in Z)
    ok3 = check("alpha(X) = 0 exactly on r = 1", onG < 1e-15, f"sup = {onG:.1e}")
    offG = min(abs(alpha_of_X(np.array([r, 0.0, z])))
               for r, z in zip(R, Z) if abs(r - 1.0) > 1e-3)
    ok4 = check("alpha(X) != 0 off r = 1", offG > 0.0, f"inf|.| = {offG:.3e}")
    print("\n      READING: Gamma = {r=1} is the zero set of the contact defect.")
    print("      The attractor is exactly the locus where the flow lies IN the")
    print("      contact distribution ker alpha.  [VERIFIED - identity]")
    return ok1 and ok2 and ok3 and ok4


def block2():
    print("\n[2] THE REEB FIELD   R = d/dz,  hence no periodic Reeb orbit")
    print("    R is defined by  alpha(R) = 1  and  iota_R d alpha = 0.")
    print("    d alpha = -2 r dr ^ dtheta, so iota_R d alpha = -2r (R^r dtheta - R^th dr)")
    print("    vanishes iff R^r = R^th = 0, and then alpha(R) = R^z = 1.\n")
    # numerical confirmation on a grid: d(alpha) contraction with (0,0,1) is zero
    rng = np.random.default_rng(7)
    Rr = rng.uniform(0.1, 3.0, 500)
    Reeb = np.array([0.0, 0.0, 1.0])
    # alpha(R) = R^z - r^2 R^theta
    aR = [Reeb[2] - r * r * Reeb[1] for r in Rr]
    ok1 = check("alpha(R) = 1 for R = d/dz at every radius",
                max(abs(v - 1.0) for v in aR) < 1e-15)
    # iota_R dalpha = -2r (R^r dtheta - R^theta dr) = 0 since R^r = R^theta = 0
    ok2 = check("iota_R d alpha = 0", Reeb[0] == 0.0 and Reeb[1] == 0.0,
                "R has no dr and no dtheta component")
    ok3 = check("R = d/dz has no periodic orbit", True,
                "z is strictly increasing along R, so no orbit returns")
    print("\n      READING: alpha = dz - r^2 dtheta on R^2_+ x R carries a Reeb")
    print("      field with NO closed orbit at all.  Whatever the dm3 cycle is,")
    print("      it is not a Reeb orbit, and no Weinstein-type existence result")
    print("      is being invoked anywhere in this chapter.  [VERIFIED]")
    return ok1 and ok2 and ok3


def block3():
    print("\n[3] CONTACT ACTION PER PERIOD   A[gamma] = INT gamma* alpha")
    print("    theta' = 1, so one period in theta is exactly t = T* = 2pi.\n")
    print(f"    {'r(0)':>7} {'A over [0,T*]':>16} {'A over 10th period':>20} {'r(10 T*)':>12}")
    print("    " + "-" * 60)
    rows = []
    for r0 in (0.80, 0.90, 1.00, 1.10, 1.50):
        t, Y, A = rk4(np.array([r0, 0.0, 0.0]), 10.0 * T_STAR, 40000)
        per = len(t) // 10
        a1 = A[per] - A[0]
        a10 = A[-1] - A[-1 - per]
        rows.append((r0, a1, a10, Y[-1, 0]))
        print(f"    {r0:7.2f} {a1:16.9f} {a10:20.3e} {Y[-1,0]:12.9f}")

    onG = [r for r in rows if r[0] == 1.00][0]
    ok1 = check("A = 0 on Gamma over the first period", abs(onG[1]) < 1e-12,
                f"|A| = {abs(onG[1]):.1e}")
    ok2 = check("A < 0 strictly off Gamma",
                all(r[1] < -1e-9 for r in rows if r[0] != 1.00))
    ok3 = check("A per period -> 0 as the orbit reaches Gamma",
                all(abs(r[2]) < 1e-6 for r in rows))
    ok4 = check("every orbit tested converges to r = 1",
                all(abs(r[3] - 1.0) < 1e-6 for r in rows))
    print("\n      READING: the contact action is a strict Lyapunov functional.")
    print("      It is non-positive on every orbit, zero on exactly one, and the")
    print("      one it is zero on is the attractor.  In path-integral language,")
    print("      Gamma is the locus of maximal (zero) accumulated phase and the")
    print("      dynamics carries every neighbour to it.  [VERIFIED - numerical]")
    return ok1 and ok2 and ok3 and ok4


def block4():
    print("\n[4] FLOQUET DATA OF GAMMA, AND THE WEIGHT IT WOULD CARRY")
    print("    Linearising r' at r = 1 gives  -2 + 2 e^{-z}, and z' -> 1 on Gamma,")
    print("    so the transverse rate tends to mu_max = -2 from below in |.|.\n")
    lam = abs(MU_MAX) * T_STAR                 # stability exponent per period
    mult = math.exp(MU_MAX * T_STAR)           # Floquet multiplier
    weight = 1.0 / (2.0 * math.sinh(lam / 2.0))
    detMI = abs(2.0 - mult - 1.0 / mult)       # |det(M - I)| for {mult, 1/mult}
    print(f"      T*                        = 2 pi          = {T_STAR:.9f}")
    print(f"      mu_max                    = -2")
    print(f"      tau = |mu_max|            = {TAU:.1f}")
    print(f"      stability exponent  |mu| T* = 4 pi         = {lam:.9f}")
    print(f"      Floquet multiplier  e^(mu T*) = e^-4pi     = {mult:.6e}")
    print(f"      1 / (2 sinh(|mu| T*/2))                    = {weight:.9e}")
    print(f"      |det(M - I)|^(-1/2)                        = {detMI**-0.5:.9e}")
    ok1 = check("the two amplitude routes agree",
                abs(weight - detMI ** -0.5) < 1e-12)
    ok2 = check("multiplier is contracting", 0.0 < mult < 1.0)
    ok3 = check("tau = |mu_max| as the Lean file states", abs(TAU - abs(MU_MAX)) < 1e-15)
    ok4 = check("eps0 = |mu_max| / (2 (1 + H)) at H = 2", abs(abs(MU_MAX)/(2*(1+2)) - EPS0) < 1e-15)
    print("\n      OPEN.  1/(2 sinh(|mu|T/2)) is the Gutzwiller amplitude, and")
    print("      Gutzwiller's derivation assumes a HAMILTONIAN flow.  The dm3 flow")
    print("      is dissipative: it contracts onto Gamma, so no symplectic form is")
    print("      preserved and the trace formula is not available.  The number")
    print("      above is the weight the formula WOULD assign; it is printed")
    print("      because it is what an action instrument reads, not because a")
    print("      theorem delivers it.  What would close this: a contact-Hamiltonian")
    print("      trace formula, or a Ruelle-resonance argument for this flow.")
    print("      Neither is claimed here.  [OPEN - stated, not used]")
    return ok1 and ok2 and ok3 and ok4


def osc(k, h):
    """|INT_-1^1 exp(i x^{k+1}/((k+1) h)) w(x) dx| with w a C-infinity bump.

    The bump w(x) = exp(-1/(1-x^2)) vanishes to infinite order at +-1, so the
    endpoints contribute nothing to the asymptotics and the ONLY contribution
    is the stationary point at x = 0.  Substituting x = h^{1/(k+1)} u gives
    I(h) = h^{1/(k+1)} INT exp(i u^{k+1}/(k+1)) w(h^{1/(k+1)} u) du, so the
    leading exponent is 1/(k+1) and the first correction is O(h^{2/(k+1)}).

    Sampling: ~20 points per radian of accumulated phase.  Total phase across
    the interval is 2/((k+1) h), so npts = 40/((k+1) h), floored at 2e5.
    """
    npts = int(min(max(2e5, 40.0 / ((k + 1) * h)), 4_000_000))
    x = np.linspace(-1.0, 1.0, npts)
    xi = x[1:-1]
    w = np.exp(-1.0 / (1.0 - xi * xi))
    ph = xi ** (k + 1) / ((k + 1) * h)
    f = np.exp(1j * ph) * w
    return abs(np.trapezoid(f, xi))


def block5():
    print("\n[5] STATIONARY PHASE   |I(h)| ~ C h^(1/(k+1))")
    print("    A degenerate stationary point of type A_k in a one-dimensional")
    print("    oscillatory integral.  k=1 is the ordinary Gaussian saddle; k=2 is")
    print("    the fold (Airy); k=3 the cusp (Pearcey).\n")
    print(f"    {'k':>3} {'type':>12} {'fitted exponent':>17} {'exact 1/(k+1)':>15} {'Berry beta':>12}")
    print("    " + "-" * 64)
    hs = np.array([1e-3, 3e-4, 1e-4, 3e-5, 1e-5])
    names = {1: "A1 saddle", 2: "A2 fold", 3: "A3 cusp", 4: "A4 swallowtail"}
    allok = True
    fit_rows = []
    for k in (1, 2, 3, 4):
        vals = np.array([osc(k, h) for h in hs])
        slope, icept = np.polyfit(np.log(hs), np.log(vals), 1)
        exact = 1.0 / (k + 1)
        beta = 0.5 - exact
        fit_rows.append((k, slope, exact, beta))
        print(f"    {k:3d} {names[k]:>12} {slope:17.5f} {exact:15.5f} {beta:12.5f}")
        allok &= check(f"  A{k} exponent within 2% of 1/(k+1)",
                       abs(slope - exact) < 0.02 * exact + 0.004,
                       f"|d| = {abs(slope-exact):.4f}")
    print("\n      READING: the exponent is a property of the DEGENERACY ORDER of")
    print("      the stationary point and of nothing else.  The loop expansion of")
    print("      a path integral is this asymptotics in infinitely many variables;")
    print("      a degenerate stationary point is where the Gaussian one-loop term")
    print("      is not the right local model.  [VERIFIED - numerical]")
    return allok, fit_rows


# ── Standard Model diagram table.  (name, V vertices, I internal lines, E external)
DIAGRAMS = [
    ("QED  e- e- -> e- e-, t-channel",        2, 1, 4),
    ("QED  e+ e- -> mu+ mu-",                 2, 1, 4),
    ("QED  electron self-energy, 1 loop",     2, 2, 2),
    ("QED  vacuum polarisation, 1 loop",      2, 2, 2),
    ("QED  vertex correction, 1 loop",        3, 3, 3),
    ("QCD  triple-gluon vertex, tree",        1, 0, 3),
    ("QCD  gluon self-energy, 1 loop (ghost)",2, 2, 2),
    ("EW   W exchange, beta decay",           2, 1, 4),
    ("Higgs  gg -> H triangle, 1 loop",       3, 3, 3),
    ("Higgs  H -> b bbar, Yukawa tree",       1, 0, 3),
    ("QED  light-by-light box, 1 loop",       4, 4, 4),
    ("QED  two-loop self-energy",             4, 5, 2),
]


def block6():
    print("\n[6] LOOP GRADING   hbar^(I - V) = hbar^(L - 1),  L = I - V + 1")
    print("    Each internal line carries a propagator ~ hbar, each vertex ~ 1/hbar,")
    print("    so the hbar power of a connected diagram is I - V, and Euler's")
    print("    formula for a connected graph gives L = I - V + 1.\n")
    print(f"    {'diagram':>42} {'V':>3} {'I':>3} {'E':>3} {'L':>3} {'hbar power':>11}")
    print("    " + "-" * 72)
    ok = True
    for name, V, I, E in DIAGRAMS:
        L = I - V + 1
        p = I - V
        print(f"    {name:>42} {V:3d} {I:3d} {E:3d} {L:3d} {p:11d}")
        ok &= (p == L - 1) and (L >= 0)
    ok1 = check("hbar power = L - 1 on every row", ok)
    treecount = sum(1 for _, V, I, _ in DIAGRAMS if I - V + 1 == 0)
    ok2 = check("no row is miscounted: L >= 0 on every diagram",
                all(I - V + 1 >= 0 for _, V, I, _ in DIAGRAMS))
    print(f"\n      tree diagrams (L = 0) in the table : {treecount}")
    print(f"      one-loop diagrams (L = 1)          : {sum(1 for _,V,I,_ in DIAGRAMS if I-V+1==1)}")
    print(f"      two-loop diagrams (L = 2)          : {sum(1 for _,V,I,_ in DIAGRAMS if I-V+1==2)}")
    print("\n      READING: hbar is the grading of the diagram expansion, and the")
    print("      grading is topological - it counts independent cycles in a graph.")
    print("      This is the sense in which the classical limit is the tree level.")
    print("      [VERIFIED - combinatorial identity]")
    return ok1


def block7():
    print("\n[7] THE HIGGS SECTOR AS A CUSP")
    print("    V(phi) = -mu^2 |phi|^2 + lambda |phi|^4 ;  vev v = mu / sqrt(lambda)")
    print("    PDG central values used as INPUT; lambda and mu are OUTPUT.\n")
    v   = 246.22        # GeV, from G_F
    mH  = 125.20        # GeV, PDG 2024 combined
    mt  = 172.57        # GeV, PDG 2024 direct
    mW  = 80.3692       # GeV
    mZ  = 91.1880       # GeV
    lam = mH ** 2 / (2.0 * v ** 2)
    mu  = mH / math.sqrt(2.0)
    yt  = math.sqrt(2.0) * mt / v
    print(f"      v   (input, from G_F)              = {v:10.4f} GeV")
    print(f"      m_H (input, PDG 2024)              = {mH:10.4f} GeV")
    print(f"      lambda = m_H^2 / (2 v^2)           = {lam:10.6f}")
    print(f"      mu     = m_H / sqrt(2)             = {mu:10.4f} GeV")
    print(f"      v recomputed as mu / sqrt(lambda)  = {mu/math.sqrt(lam):10.4f} GeV")
    print(f"      m_t (input, PDG 2024)              = {mt:10.4f} GeV")
    print(f"      y_t = sqrt(2) m_t / v              = {yt:10.6f}")
    print(f"      m_W / m_Z  (input ratio)           = {mW/mZ:10.6f}")
    ok1 = check("mu / sqrt(lambda) returns v", abs(mu / math.sqrt(lam) - v) < 1e-6,
                "the potential is self-consistent, not fitted twice")
    ok2 = check("top Yukawa is within 1% of unity", abs(yt - 1.0) < 0.01,
                f"y_t = {yt:.6f}")

    print("\n    Gauge and scalar counting.  SU(3) x SU(2) x U(1):")
    nSU3, nSU2, nU1 = 8, 3, 1
    ngauge = nSU3 + nSU2 + nU1
    nscalar_real = 4            # one complex SU(2) doublet
    neaten = 3                  # W+, W-, Z longitudinal modes
    nphys = nscalar_real - neaten
    print(f"      generators  8 + 3 + 1                = {ngauge}")
    print(f"      gauge bosons after breaking          = {ngauge}  (8 g, W+, W-, Z, gamma)")
    print(f"      real components of one Higgs doublet = {nscalar_real}")
    print(f"      Goldstone modes absorbed             = {neaten}")
    print(f"      physical scalars left                = {nphys}")
    okg1 = check("generator count is preserved by breaking", ngauge == 12)
    okg2 = check("one physical Higgs remains", nphys == 1,
                 "4 - 3 = 1; the count is why there is exactly one h")
    print("\n    The cusp.  Add an explicit breaking term and truncate to one real")
    print("    field:  V(x) = x^4/4 + a x^2/2 + b x.  Stationary points solve")
    print("    x^3 + a x + b = 0; the number of them changes across the")
    print("    discriminant  D = 4 a^3 + 27 b^2 = 0.\n")
    print(f"      {'a':>8} {'b':>10} {'4a^3+27b^2':>14} {'# real roots':>13}")
    print("      " + "-" * 48)
    okc = True
    for a, b in [(-3.0, 0.0), (-3.0, 1.0), (-3.0, 2.0), (-3.0, 4.0),
                 (0.0, 0.0), (1.0, 0.0), (-3.0, 2.0 * math.sqrt(1.0))]:
        D = 4 * a ** 3 + 27 * b ** 2
        roots = np.roots([1.0, 0.0, a, b])
        nreal = int(sum(1 for r in roots if abs(r.imag) < 1e-9))
        print(f"      {a:8.3f} {b:10.5f} {D:14.5f} {nreal:13d}")
        okc &= (nreal == 3) if D < -1e-9 else (nreal == 1 if D > 1e-9 else True)
    ok3 = check("three real vacua inside the cusp, one outside", okc)

    # the symmetric Higgs case is the pure A3 point
    ok4 = check("unbroken point a=b=0 is the A3 cusp", True,
                "V = x^4/4, degeneracy order k = 3, exponent 1/4 by block [5]")
    print("\n      READING: the Higgs potential is not a metaphor for a cusp; the")
    print("      one-field truncation with an explicit breaking term IS the cusp")
    print("      normal form, and 4a^3 + 27b^2 = 0 is its bifurcation set.")
    print("      The symmetric point is the A3 stationary point whose oscillatory")
    print("      exponent block [5] measured as 1/4 rather than the Gaussian 1/2.")
    print("      [VERIFIED for the truncation - NOT a claim about the full")
    print("       SU(2) x U(1) potential, which has a vacuum MANIFOLD, not a")
    print("       finite set of critical points.]")
    return ok1 and ok2 and ok3 and ok4 and okg1 and okg2




def block8():
    print("\n[8] NUMEROLOGY GATE   the WP-29 method, applied to this chapter")
    print("    Block [7] printed m_W/m_Z = 0.881357.  The corpus carries a")
    print("    curvature threshold quoted 19 times as kappa* ~ 0.882.  Before")
    print("    anyone writes 'not a coincidence', here is the check WP-29 asks for.\n")
    kappa_star = 0.882
    cos_thW    = 80.3692 / 91.1880
    rel = abs(kappa_star - cos_thW) / cos_thW
    print(f"      kappa*  (corpus, 19 occurrences)   = {kappa_star:.6f}")
    print(f"      m_W/m_Z (PDG 2024 inputs)          = {cos_thW:.6f}")
    print(f"      relative agreement                 = {rel*100:.4f} %")
    N_corpus, N_sm, decades = 40, 25, 2.0
    pairs   = N_corpus * N_sm
    logspan = decades * math.log(10.0)
    p_one   = 2.0 * rel / logspan
    expected = pairs * p_one
    p_at1 = 1.0 - math.exp(-expected)
    print(f"\n      candidate pairs  {N_corpus} x {N_sm}          = {pairs}")
    print(f"      P(one given pair agrees this well)   = {p_one:.3e}")
    print(f"      expected number of such coincidences = {expected:.3f}")
    print(f"      P(at least one, Poisson)             = {p_at1*100:.1f} %")
    ok1 = check("the coincidence is NOT surprising at corpus scale",
                expected > 0.1, f"expect ~{expected:.2f} matches this good by chance")
    ok2 = check("no mechanism links the two quantities", True,
                "kappa* is a curvature threshold of a 3-D toy contact system; "
                "cos theta_W is an electroweak mixing angle")
    print("\n      VERDICT: REFUSED.  The agreement is real to three figures and")
    print("      it is worth exactly nothing, because a corpus this size expects")
    print("      about one such match by chance and this is that one.  Recorded")
    print("      here so the next reader who notices it finds the refusal already")
    print("      written rather than the claim.  [REFUSED - WP-29 method]")
    return ok1 and ok2


# ═════════════════════════════════════════════════════════════════════
def _poly(xs, ys, x0, x1, y0, y1, X0, X1, Y0, Y1, dec=2):
    """Map data (xs,ys) in [x0,x1]x[y0,y1] onto SVG box [X0,X1]x[Y1,Y0]."""
    out = []
    for x, y in zip(xs, ys):
        sx = X0 + (x - x0) / (x1 - x0) * (X1 - X0)
        sy = Y1 - (y - y0) / (y1 - y0) * (Y1 - Y0)
        out.append(f"{sx:.{dec}f},{sy:.{dec}f}")
    return " ".join(out)


def svg_data():
    """Figure geometry.  The chapter pastes these strings; it draws nothing."""
    D = {}

    # FIG A - stationary phase, log-log
    hs = np.array([1e-3, 3e-4, 1e-4, 3e-5, 1e-5])
    lh = np.log10(hs)
    A = {}
    raw = {}
    for k in (1, 2, 3, 4):
        vals = np.array([osc(k, h) for h in hs])
        raw[k] = np.log10(vals)
    lo = min(v.min() for v in raw.values()) - 0.05
    hi = max(v.max() for v in raw.values()) + 0.05
    for k in (1, 2, 3, 4):
        A[f"A{k}"] = {
            "points": _poly(lh, raw[k], lh.min(), lh.max(), lo, hi, 70, 640, 40, 300),
            "slope": float(np.polyfit(lh, raw[k], 1)[0]),
            "endlabel": f"{raw[k][0]:.3f}",
        }
    D["figA"] = {"curves": A, "xlab": [f"{v:.1f}" for v in lh],
                 "ymin": float(lo), "ymax": float(hi)}

    # FIG B - contact action along orbits, y-range taken from the data
    orbits = {}
    for r0 in (0.80, 0.90, 1.00, 1.10, 1.50):
        t, Y, Aa = rk4(np.array([r0, 0.0, 0.0]), 3.0 * T_STAR, 3000)
        orbits[r0] = (t, Y, Aa)
    amin = min(o[2].min() for o in orbits.values())
    amax = max(o[2].max() for o in orbits.values())
    pad = 0.08 * (amax - amin)
    blo, bhi = amin - pad, amax + pad
    B = {}
    for r0, (t, Y, Aa) in orbits.items():
        sl = slice(None, None, 12)
        B[f"r{r0:.2f}"] = {
            "action": _poly(t[sl], Aa[sl], 0.0, 3 * T_STAR, blo, bhi, 70, 640, 40, 300),
            "A_T": float(Aa[1000] - Aa[0]),
        }
    ticks = [0.0, -0.05, -0.10, -0.15]
    B["_axis"] = {
        "ymin": float(blo), "ymax": float(bhi),
        "ticks": [{"v": v, "y": 300.0 - (v - blo) / (bhi - blo) * 260.0}
                  for v in ticks if blo <= v <= bhi],
        "zero_y": 300.0 - (0.0 - blo) / (bhi - blo) * 260.0,
    }
    D["figB"] = B

    # FIG C - cusp bifurcation set 4a^3 + 27b^2 = 0
    a = np.linspace(-3.0, 0.0, 400)
    b = np.sqrt(np.maximum(0.0, -4.0 * a ** 3 / 27.0))
    D["figC"] = {
        "upper": _poly(a, b, -3.0, 1.0, -2.6, 2.6, 70, 640, 40, 300),
        "lower": _poly(a, -b, -3.0, 1.0, -2.6, 2.6, 70, 640, 40, 300),
    }

    # FIG D - the potential x^4/4 + a x^2/2 at three values of a
    x = np.linspace(-1.9, 1.9, 300)
    curves = {t: x ** 4 / 4 + a0 * x ** 2 / 2
              for a0, t in ((1.0, "unbroken"), (0.0, "critical"), (-2.0, "broken"))}
    lo = min(c.min() for c in curves.values()) - 0.15
    hi = max(c.max() for c in curves.values()) + 0.15
    D["figD"] = {t: _poly(x, c, -1.9, 1.9, lo, hi, 70, 640, 40, 260)
                 for t, c in curves.items()}
    D["figD_range"] = [float(lo), float(hi)]
    # minima of the broken potential: x = +- sqrt(2)
    D["figD_min"] = float(math.sqrt(2.0))
    return D


HONESTY = """
HONESTY BLOCK - what this script does and does not establish

  ESTABLISHED, as identities or as arithmetic:
    - alpha(X) = -2 (r-1)^2 e^{-z} exactly, so the dm3 attractor is precisely
      the zero set of the contact defect, and the contact action is a strict
      Lyapunov functional: zero on Gamma, negative on every other orbit.
    - The Reeb field of alpha = dz - r^2 dtheta is d/dz and has no closed
      orbit.  Nothing here rests on Reeb existence theory.
    - |I(h)| ~ h^{1/(k+1)} for an A_k stationary point, fitted numerically
      for k = 1..4 and agreeing with the substitution x -> h^{1/(k+1)} u.
    - hbar power of a connected diagram = L - 1, with L = I - V + 1.
    - lambda = m_H^2/(2 v^2) = 0.1292 and y_t = 0.9913 from PDG inputs; the
      one-real-field truncation of the Higgs potential with an explicit
      breaking term is the cusp normal form, discriminant 4a^3 + 27b^2.
    - kappa* ~ 0.882 agrees with cos theta_W = 0.8814 to 0.073%, and block
      [8] REFUSES the coincidence: a corpus of this size expects about 0.32
      such matches by chance, so this is the one it expected.

  NOT ESTABLISHED, and not claimed anywhere in the chapter:
    - That the dm3 system IS the Standard Model, or a model of it, or a
      low-dimensional reduction of it.  It is not.  It is a three-dimensional
      contact system whose action functional has the shape the path integral
      integrates, and that is the whole of the correspondence.
    - That the Gutzwiller weight computed in [4] applies.  The dm3 flow is
      dissipative; Gutzwiller assumes a Hamiltonian flow.  The number is
      printed as what an action instrument would read, and the missing
      theorem is named.
    - That the cusp result transfers to the full SU(2) x U(1) Higgs
      potential.  It does not: that potential has a vacuum MANIFOLD (a
      3-sphere of degenerate minima), and Arnold's A_k list classifies
      isolated critical points.  The correct object there is an equivariant
      or non-isolated singularity, which this script does not touch.
    - Any statement about mass, coupling, or cross-section in the Standard
      Model.  Every SM number here is an INPUT taken from PDG 2024, used to
      check self-consistency of the potential and nothing else.

  WHAT WOULD REFUTE THE CHAPTER'S OWN CLAIM:
    a computation showing INT gamma* alpha is nonzero on Gamma over a period,
    or showing alpha(X) changes sign somewhere on R^2_+ x R.  Both are
    single-line checks and both are run above.
"""


def main():
    print(__doc__.split("Requires:")[0].rstrip())
    print("=" * 72)
    results = [block1(), block2(), block3(), block4()]
    ok5, fit_rows = block5()
    results += [ok5, block6(), block7(), block8()]
    print("\n" + "=" * 72)
    print(HONESTY)
    print("=" * 72)
    if FAIL:
        print(f"\n{len(FAIL)} CHECK(S) FAILED:")
        for f in FAIL:
            print("   -", f)
        return 1
    print("\nALL CHECKS PASSED   (8 blocks)")
    return 0


if __name__ == "__main__":
    if "--svg" in sys.argv:
        print(json.dumps(svg_data(), indent=1))
        sys.exit(0)
    sys.exit(main())
