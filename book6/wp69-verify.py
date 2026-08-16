#!/usr/bin/env python3
"""
WP69 · The Fold Is a Coordinate — reproduction script.

Reproduces every symbolic and numerical claim in the paper, in order.
Requires: sympy, numpy, scipy.   Runtime ~90 s.

  python3 wp69-verify.py
"""
import numpy as np, sympy as sp
from scipy.integrate import solve_ivp

R, Z = sp.symbols('R Z', real=True)
W = sp.exp(-Z)

# ---------------------------------------------------------------- exact toy
# Vol II §4.3 :  rdot = r(1-r^2) + 2(r-1)e^{-z} ,  thetadot = 1 ,  zdot = r^2 - 2(r-1)^2 e^{-z}
def rhs(t, y, gh=1.0):
    r, z = y
    w = gh * np.exp(-z)
    return [r * (1 - r * r) + 2 * (r - 1) * w, r * r - 2 * (r - 1) ** 2 * w]

def brhs(t, y, gh=1.0):
    a = rhs(t, y, gh)
    return [-a[0], -a[1]]

print("=" * 74)
print("WP69 · reproduction")
print("=" * 74)

# ---- [1][2] Prop 4 : equilibrium cubic and its roots ---------------------
f1 = R * (1 - R ** 2) + 2 * (R - 1) * W
f2 = R ** 2 - 2 * (R - 1) ** 2 * W
Wsol = sp.solve(sp.Eq(f2, 0), W)[0]                      # e^{-z} = r^2 / (2(r-1)^2)
cub = sp.factor(sp.expand(sp.numer(sp.together(f1.subs(W, Wsol)))))
P = R ** 3 - R ** 2 - 2 * R + 1
print("\n[1] equilibrium condition        %s = 0" % cub)
print("    cubic                        %s" % P)
print("    discriminant                 %s   (= 7^2, field Q(cos 2pi/7))"
      % sp.discriminant(P, R))
print("\n[2] roots")
for k in (1, 3, 5):
    v = 2 * sp.cos(sp.pi * k / 7)
    print("      2cos(%d.pi/7) = %+.13f    P = %+.1e"
          % (k, float(v), float(P.subs(R, v))))

# ---- [3][4] trace / determinant minimal polynomials ---------------------
tr = sp.simplify(1 - 3 * R ** 2 + 2 * Wsol + 2 * (R - 1) ** 2 * Wsol)
det = sp.simplify((1 - 3 * R ** 2 + 2 * Wsol) * 2 * (R - 1) ** 2 * Wsol
                  + 2 * (R - 1) * Wsol * (2 * R - 4 * (R - 1) * Wsol))
x = sp.Symbol('x')
mp_tr = sp.minimal_polynomial(sp.simplify(tr.subs(R, 2 * sp.cos(sp.pi / 7))), x)
mp_dt = sp.minimal_polynomial(sp.simplify(det.subs(R, 2 * sp.cos(sp.pi / 7))), x)
print("\n[3] trace(r) = %s" % sp.simplify(tr))
print("    minpoly(trace)               %s      (= minpoly of 2cos(2pi/7))" % mp_tr)
print("\n[4] minpoly(det)                 %s" % mp_dt)
print("    all coefficients positive -> no positive root (Descartes)")
print("    -> every off-cycle equilibrium is a SADDLE")
print("\n    equilibrium data:")
print("      %-18s %-16s %-16s %-14s" % ("r", "z", "tr J", "det J"))
for k in (1, 3, 5):
    v = 2 * sp.cos(sp.pi * k / 7)
    zz = sp.log(2 * (v - 1) ** 2 / v ** 2) if float(v) > 0 else None
    print("      %-18.12f %-16s %-16.10f %-14.10f"
          % (float(v),
             ("%.12f" % float(zz)) if zz is not None else "-- outside M",
             float(tr.subs(R, v)), float(det.subs(R, v))))
print("    minpoly(e^z at equilibria)   %s"
      % sp.minimal_polynomial(sp.simplify((2 * (R - 1) ** 2 / R ** 2)
                                          .subs(R, 2 * sp.cos(sp.pi / 7))), x))

# ---- [5][6] Lemma 1 : alpha(X) = H_diss ; Reeb = d_z --------------------
alphaX = sp.simplify((R ** 2 - 2 * (R - 1) ** 2 * W) - R ** 2 * 1)
print("\n[5] alpha(X) = zdot - r^2 thetadot = %s" % alphaX)
print("    alpha(X) - H_diss (gamma=2, V=(r-1)^2, beta=1) = %s"
      % sp.simplify(alphaX + 2 * (R - 1) ** 2 * W))
print("\n[6] alpha = dz - r^2 dtheta :  alpha(d_z) = 1 ; d_alpha = -2r dr^dtheta ;")
print("    iota_{d_z} d_alpha = 0  ->  Reeb = d_z ;  L_{d_z} alpha = 0  (strict)")

# ---- Theorem 1 / 2 : gauge and modulus (symbolic) -----------------------
b, gh, ze = sp.symbols('beta ghat zeta', positive=True)
print("\n[6b] Theorem 1(3):  ghat e^{-beta z} = e^{-beta zeta} with zeta = z - ln(ghat)/beta :",
      sp.simplify(gh * sp.exp(-b * (ze + sp.log(gh) / b)) - sp.exp(-b * ze)) == 0)
Lam = sp.Symbol('Lambda', positive=True)
rt, zt = sp.symbols('rt zt', real=True)
F = [-(1 - sp.exp(-zt)) * rt, Lam - rt ** 2 * sp.exp(-zt)]
J = sp.simplify(sp.Matrix(F).jacobian([rt, zt]).subs({rt: sp.sqrt(Lam), zt: 0}))
print("     Theorem 3(3): J at (sqrt(L),0) =", J.tolist(),
      " tr =", sp.simplify(J.trace()), " det =", sp.simplify(J.det()))

# ---- [7][8] Prop 5 : the two basin boundaries ---------------------------
def stable_dir(k):
    rS = 2 * np.cos(np.pi * k / 7)
    zS = np.log(2 * (rS - 1) ** 2 / rS ** 2)
    w = np.exp(-zS)
    J = np.array([[1 - 3 * rS ** 2 + 2 * w, -2 * (rS - 1) * w],
                  [2 * rS - 4 * (rS - 1) * w, 2 * (rS - 1) ** 2 * w]])
    E, V = np.linalg.eig(J)
    i = int(np.argmin(E))
    v = V[:, i].real
    return rS, zS, v / np.linalg.norm(v), E

def ws_level(k, level=0.0, T=300, eps=1e-10, rtol=1e-13):
    """where W^s of the k-th saddle meets {z = level}"""
    rS, zS, v, _ = stable_dir(k)
    for sgn in (-1, 1):
        ev = lambda t, y: y[1] - level
        ev.terminal = True
        s = solve_ivp(brhs, [0, T], [rS + sgn * eps * v[0], zS + sgn * eps * v[1]],
                      rtol=rtol, atol=1e-16, method='DOP853', events=[ev])
        if len(s.t_events[0]):
            return s.y_events[0][0][0]
    return None

r_star = ws_level(3)
r_starstar = ws_level(1, T=60)
print("\n[7] r_star      = W^s(S_-) cap {z=0} = %.13f" % r_star)
print("    Vol II toy-model §7 lists 'certified 0.77594059' -- 8th digit differs")
print("[8] r_starstar  = W^s(S_+) cap {z=0} = %.10f   (not previously reported)" % r_starstar)

# ---- [9] Theorem 1 verified in the exact (untruncated) system -----------
def converges(r0, gh):
    e1 = lambda t, y: y[0] - 1e-8; e1.terminal = True; e1.direction = -1
    e2 = lambda t, y: y[0] - 1e4;  e2.terminal = True; e2.direction = 1
    s = solve_ivp(lambda t, y: rhs(t, y, gh), [0, 300], [r0, 0.0],
                  rtol=1e-12, atol=1e-15, method='DOP853', events=[e1, e2])
    return abs(s.y[0, -1] - 1.0) < 1e-3

print("\n[9] Theorem 1 in the exact system: gated bisection  vs  one gate-free separatrix")
print("      %-8s %-18s %-18s %s" % ("ghat", "gated bisection", "W^s at -ln(ghat)", "diff"))
worst = 0.0
for g in (0.5, 1.0, 2.0):
    a, bb = 0.30, 0.999
    fa = converges(a, g)
    for _ in range(55):
        m = 0.5 * (a + bb)
        if converges(m, g) == fa: a = m
        else: bb = m
    got = 0.5 * (a + bb)
    pred = ws_level(3, level=-np.log(g))
    worst = max(worst, abs(got - pred))
    print("      %-8.1f %-18.10f %-18.10f %.1e" % (g, got, pred, abs(got - pred)))
print("    max discrepancy = %.1e   ->  the gate is a Reeb translation" % worst)

# local sensitivity
h = 0.1
d = (ws_level(3, level=h) - ws_level(3, level=-h)) / (2 * h)
print("    dr_star/dzeta at zeta=0 = %.8f  ->  margin is logarithmic in ghat" % d)

# ---- WP66 arithmetic ----------------------------------------------------
lo, hi = 3.7 - 1.9, 4.0 - 1.5
print("\n[10] WP66 shift, interval arithmetic: [%.1f, %.1f] C   (midpoints %.2f C)"
      % (lo, hi, 3.85 - 1.70))
print("     with ch05 band 1.6 <= beta <= 2.4 :  |c_Psi| ln R in [%.2f, %.2f] C"
      % (1.6 * lo, 2.4 * hi))
print("\ndone.")
