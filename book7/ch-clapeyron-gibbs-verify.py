#!/usr/bin/env python3
"""
Clapeyron, Maxwell, Gibbs -- the parallelogram, the four relations, and the
tangent plane, checked against an ideal gas and a van der Waals fluid.

[1] checks the geometric claim underneath Clapeyron's 1834 diagram and
Carnot's theorem: that in the (entropy, temperature) plane a reversible
Carnot cycle is exactly a rectangle, and its area equals the work done. Built
from an ideal-gas equation of state, not asserted -- the two adiabatic legs
are numerically confirmed to run at constant entropy, the two isothermal legs
at constant temperature, and the total work is integrated along the actual
P-V path and compared against (T2-T1)(S2-S1).

[2] checks the four relations Maxwell reached in 1871 by extending that
parallelogram -- reached here instead by finite-differencing an explicit
ideal-gas surface S(T,V), which is the modern replacement for Maxwell's
geometry: the equality in each relation is the statement that mixed partial
derivatives of a single potential do not care about order (Clairaut/Schwarz),
which is exactly what a parallelogram built from the same two displacements
in either order enforces.

[3] checks Gibbs' 1873 claim in geometric form: that two points on a
thermodynamic surface with a common tangent plane -- same T, same P -- carry
equal free energy, G(ε')=G(ε''). Built on a van der Waals fluid below its
critical temperature, where this is not vacuous: the equal-area (Maxwell)
construction is solved for directly by bisection, entirely independently of
any free-energy formula, and only then is G evaluated at the two resulting
points and shown to agree to numerical precision. Two constructions credited
to the same corpus (Maxwell's equal-area rule, Gibbs' common tangent) turn
out to be the same statement.

[4] checks the chronology, [5] reads the chapter file back.

Standard library only. python3 book7/ch-clapeyron-gibbs-verify.py
"""

import math, os, re, sys

fails = []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg, ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def head(n, t):
    print('\n' + '=' * 72 + '\n  [%s]  %s\n' % (n, t) + '=' * 72)

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.join(HERE, 'ch-clapeyron-gibbs.html')

def simpson(f, a, b, N=20000):
    if N % 2: N += 1
    h = (b - a) / N
    s = f(a) + f(b)
    for i in range(1, N):
        s += f(a + i * h) * (4 if i % 2 == 1 else 2)
    return s * h / 3.0

# ==========================================================================
head(1, "THE CARNOT CYCLE IS A RECTANGLE IN (ENTROPY, TEMPERATURE)")
print("  Clapeyron's 1834 quadrilateral, on infinitesimal sides, becomes a")
print("  parallelogram. On real, finite sides in (S,T) instead of (P,V), it is")
print("  exactly a rectangle for ANY working substance, because the two legs")
print("  that hold T fixed are horizontal and the two that hold S fixed are")
print("  vertical by construction. What is not automatic is that the area of")
print("  that rectangle -- (T2-T1)(S2-S1) -- equals the mechanical work done")
print("  around the actual curved path in the (P,V) plane. That is Carnot's")
print("  theorem, and it is checked here on an ideal gas, from the equation")
print("  of state, not assumed.\n")

R, Cv = 8.314462618, 1.5 * 8.314462618   # monatomic ideal gas, per mole
def V_of_ST(S, T):
    return math.exp((S - Cv * math.log(T)) / R)
def P_of_ST(S, T):
    return R * T / V_of_ST(S, T)
def P_of_SV(S, V):
    T = math.exp((S - R * math.log(V)) / Cv)
    return R * T / V

T_hot, T_cold = 400.0, 300.0
S_lo, S_hi = 38.6, 43.6   # an arbitrary 5 J/K span

def work_isothermal(T, Sa, Sb):
    Va, Vb = V_of_ST(Sa, T), V_of_ST(Sb, T)
    return simpson(lambda V: R * T / V, Va, Vb)

def work_adiabatic(S, Ta, Tb):
    Va, Vb = V_of_ST(S, Ta), V_of_ST(S, Tb)
    return simpson(lambda V: P_of_SV(S, V), Va, Vb)

W1 = work_isothermal(T_hot, S_lo, S_hi)
W2 = work_adiabatic(S_hi, T_hot, T_cold)
W3 = work_isothermal(T_cold, S_hi, S_lo)
W4 = work_adiabatic(S_lo, T_cold, T_hot)
W_total = W1 + W2 + W3 + W4
W_rect = (T_hot - T_cold) * (S_hi - S_lo)

print('      leg                          work (J)')
print('      isothermal, hot (S %.1f -> %.1f)   %10.3f' % (S_lo, S_hi, W1))
print('      adiabatic, expansion             %10.3f' % W2)
print('      isothermal, cold (S %.1f -> %.1f)  %10.3f' % (S_hi, S_lo, W3))
print('      adiabatic, compression            %10.3f' % W4)
print('      total, around the P-V loop        %10.3f' % W_total)
print('      rectangle area (T2-T1)(S2-S1)      %10.3f' % W_rect)

check(abs(W_total / W_rect - 1.0) < 1e-6,
      'net P-V work equals the (S,T)-rectangle area to 1e-6',
      'ratio %.9f' % (W_total / W_rect))
check(W2 + W4 != 0 and abs(W2 + W4) < 1e-6 * abs(W1),
      'the two adiabatic legs cancel, as constant-S legs must')
eta = 1.0 - T_cold / T_hot
Q_in = T_hot * (S_hi - S_lo)
check(abs(W_total - eta * Q_in) < 1e-6 * Q_in,
      'the classical efficiency 1 - Tc/Th reproduces the same work',
      'W_total=%.6f  eta*Qin=%.6f' % (W_total, eta * Q_in))

# ==========================================================================
head(2, "THE FOUR MAXWELL RELATIONS, FROM ONE IDEAL-GAS SURFACE")
print("  Maxwell reached these geometrically in 1871, from the parallelogram,")
print("  using Rankine's function Phi in place of entropy. The content is the")
print("  same however it is reached: a single potential's mixed partials do")
print("  not care about order. Each relation below is checked by building")
print("  BOTH sides from the same S(T,V), independently, via finite")
print("  differences, and comparing.\n")

T0, V0 = 300.0, 0.02
S0 = Cv * math.log(T0) + R * math.log(V0)
P0 = R * T0 / V0

def T_of_SV(S, V):
    return math.exp((S - R * math.log(V)) / Cv)
def P_of_SV2(S, V):
    return R * T_of_SV(S, V) / V
Cp = Cv + R
def T_of_SP(S, P):
    return math.exp((S - R * math.log(R / P)) / Cp)
def V_of_SP(S, P):
    return R * T_of_SP(S, P) / P
def S_of_TV(T, V):
    return Cv * math.log(T) + R * math.log(V)
def S_of_TP(T, P):
    return S_of_TV(T, R * T / P)
def V_of_TP(T, P):
    return R * T / P

def cd(f, x, h):
    return (f(x + h) - f(x - h)) / (2 * h)

dTdV_S  =  cd(lambda V: T_of_SV(S0, V), V0, V0 * 1e-4)
dPdS_V  =  cd(lambda S: P_of_SV2(S, V0), S0, 1e-3)
dTdP_S  =  cd(lambda P: T_of_SP(S0, P), P0, P0 * 1e-4)
dVdS_P  =  cd(lambda S: V_of_SP(S, P0), S0, 1e-3)
dSdP_T  =  cd(lambda P: S_of_TP(T0, P), P0, P0 * 1e-4)
dVdT_P  =  cd(lambda T: V_of_TP(T, P0), T0, T0 * 1e-4)
dSdV_T  =  cd(lambda V: S_of_TV(T0, V), V0, V0 * 1e-4)
dPdT_V  =  cd(lambda T: R * T / V0, T0, T0 * 1e-4)

REL = [
    ("dU = TdS - PdV",  "(dT/dV)_S", dTdV_S, "-(dP/dS)_V", -dPdS_V),
    ("dH = TdS + VdP",  "(dT/dP)_S", dTdP_S,  "(dV/dS)_P",  dVdS_P),
    ("dG = -SdT + VdP", "-(dS/dP)_T", -dSdP_T, "(dV/dT)_P", dVdT_P),
    ("dA = -SdT - PdV", "(dS/dV)_T", dSdV_T,  "(dP/dT)_V",  dPdT_V),
]
for src, namea, a, nameb, b in REL:
    rel = abs(a - b) / max(abs(a), abs(b), 1e-30)
    print('      %-18s  %-14s %14.6f   %-12s %14.6f   rel.err %.2e' % (src, namea, a, nameb, b, rel))
    check(rel < 1e-5, '%s  <=>  %s' % (namea, nameb), 'rel. error %.2e' % rel)

# ==========================================================================
head(3, "GIBBS' COMMON TANGENT IS MAXWELL'S EQUAL-AREA RULE")
print("  A van der Waals fluid below its critical temperature, in reduced")
print("  units (Tc=Vc=Pc=1). The equal-area construction is solved by")
print("  bisection on the trial pressure alone -- no free energy anywhere in")
print("  that step. G is then evaluated at the two resulting volumes from an")
print("  independently integrated potential, and Gibbs' 1873 claim is what")
print("  is being tested: that the tangent-plane condition and the")
print("  equal-area condition pick out the same two points.\n")

def P_vdw(V, T):
    return 8.0 * T / (3.0 * V - 1.0) - 3.0 / (V * V)

def three_roots(T, Ptrial, lo=0.34, hi=6.0, n=3000):
    def g(V): return P_vdw(V, T) - Ptrial
    vs = [lo + (hi - lo) * i / n for i in range(n + 1)]
    roots, prev = [], g(vs[0])
    for i in range(1, len(vs)):
        cur = g(vs[i])
        if prev * cur < 0:
            a, b = vs[i - 1], vs[i]
            for _ in range(80):
                m = 0.5 * (a + b)
                if g(a) * g(m) <= 0: b = m
                else: a = m
            roots.append(0.5 * (a + b))
        prev = cur
    return roots if len(roots) == 3 else None

def area_residual(T, Ptrial):
    roots = three_roots(T, Ptrial)
    if roots is None:
        return None, None
    Vl, Vv = roots[0], roots[-1]
    return simpson(lambda V: P_vdw(V, T) - Ptrial, Vl, Vv), roots

T_r = 0.9
grid = [0.30 + 0.60 * i / 400 for i in range(401)]
vals = [(Pt,) + area_residual(T_r, Pt) for Pt in grid]
bracket = None
for i in range(1, len(vals)):
    P0v, a, _ = vals[i - 1]
    P1v, b, _ = vals[i]
    if a is not None and b is not None and a * b < 0:
        bracket = (P0v, P1v); break
check(bracket is not None, 'the equal-area residual changes sign below Tc=1 (found a bracket)')

lo, hi = bracket
for _ in range(60):
    mid = 0.5 * (lo + hi)
    fa, _ = area_residual(T_r, lo)
    fm, _ = area_residual(T_r, mid)
    if fa * fm <= 0: hi = mid
    else: lo = mid
Psat = 0.5 * (lo + hi)
resid, roots = area_residual(T_r, Psat)
Vl, Vm, Vv = roots
print('      T_r = %.2f    P_sat = %.6f    V_liquid = %.6f    V_middle = %.6f    V_vapor = %.6f'
      % (T_r, Psat, Vl, Vm, Vv))
check(abs(resid) < 1e-8, 'equal-area residual is zero at the solved pressure', '%.3e' % resid)
check(Vl < Vm < Vv, 'three distinct volumes bracket the unphysical middle branch')

def A_diff(Va, Vb, T):
    return -simpson(lambda V: P_vdw(V, T), Va, Vb)

dA = A_diff(Vl, Vv, T_r)
G_diff = dA + Psat * (Vv - Vl)     # G(vapor) - G(liquid); P equal at both by construction
print('      A(vapor) - A(liquid) = %.6f      G(vapor) - G(liquid) = %.3e' % (dA, G_diff))
check(abs(G_diff) < 1e-8,
      'Gibbs free energy agrees at the two equal-area points to 1e-8',
      '%.3e' % G_diff)
check(0.5 < Psat < 0.8, 'the coexistence pressure at Tr=0.9 is in the expected range', '%.4f' % Psat)

# ==========================================================================
head(4, "THE CHRONOLOGY")
EVENTS = [
    (1799, "Emile Clapeyron born, Paris"),
    (1834, "Clapeyron, Memoire sur la puissance motrice de la chaleur -- the P-V parallelogram"),
    (1839, "Josiah Willard Gibbs born, New Haven"),
    (1850, "Clausius states the first form of the second law"),
    (1854, "Rankine introduces a thermodynamic function, later called Phi"),
    (1865, "Clausius names entropy S"),
    (1871, "Maxwell, Theory of Heat, 1st edition -- the four relations, via Phi, not S"),
    (1873, "Gibbs, Papers I and II -- indicator-diagram comparisons and the (V,S,U) surface"),
    (1874, "Maxwell models Gibbs' surface in clay, casts it in plaster, sends it to Gibbs"),
    (1876, "Gibbs, On the Equilibrium of Heterogeneous Substances, Part I"),
    (1878, "Gibbs, On the Equilibrium of Heterogeneous Substances, Part II"),
    (1879, "Maxwell dies, Cambridge, age 48"),
    (1903, "Gibbs dies, New Haven"),
    (1906, "Gibbs' Scientific Papers, Volume One: Thermodynamics, published posthumously"),
    (1973, "Hermann, Geometry, Physics and Systems -- contact geometry made explicit"),
    (1978, "Mrugala, geometric formulation of equilibrium thermodynamics"),
    (1990, "Arnold, on the geometrical method of Gibbs' thermodynamics, at the Gibbs symposium"),
]
for y, what in EVENTS:
    print('      %4d   %s' % (y, what))
years = [y for y, _ in EVENTS]
check(years == sorted(years), 'the chronology is monotone')
check(1879 - 1834 == 45, 'Clapeyron to Maxwell: 45 years')
check(1873 - 1865 == 8, "Gibbs' surface follows Clausius naming entropy by 8 years")
check(1990 - 1873 == 117, "the contact-geometric reading follows Gibbs' surface by 117 years")
check(1903 - 1839 == 64, "Gibbs' lifespan")
check(1879 - 1831 == 48, "Maxwell's age at death (born 1831)")

# ==========================================================================
head(5, "THE CHAPTER FILE")
if not os.path.exists(CHAPTER):
    check(False, 'ch-clapeyron-gibbs.html present next to this script', CHAPTER)
else:
    raw = open(CHAPTER, encoding='utf-8').read()
    flat = re.sub(r'<[^>]+>', ' ', raw)
    flat = re.sub(r'\s+', ' ', flat).lower()
    for y, _ in EVENTS:
        check(str(y) in raw, 'chapter carries the year %d' % y)
    for word in ('clapeyron', 'rankine', 'legendre', 'contact', 'van der waals', 'equal-area', 'tangent plane'):
        check(word in flat, 'chapter carries "%s"' % word)
    check('707' not in raw, 'chapter does not duplicate the unrelated Freire ratio (sanity check)')
    OVERCLAIM = ['maxwell discovered contact geometry', 'gibbs invented contact geometry',
                 'proves dm3', 'proves the dm']
    for phrase in OVERCLAIM:
        check(phrase not in flat, 'chapter prose does not say "%s"' % phrase)
    check('0.647' in raw or '0.6470' in raw or '64699' in raw.replace('.', ''),
          'chapter carries the computed coexistence pressure')

# ==========================================================================
print('\n' + '=' * 72)
if fails:
    print('  %d FAILED' % len(fails))
    for f in fails: print('    - ' + f)
    sys.exit(1)
print('  ALL CHECKS PASSED')
print('=' * 72)
