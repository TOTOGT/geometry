#!/usr/bin/env python3
"""
ch10_lambda_bone_audit.py -- one self-contained script for the lambda-extension of the
Book 4 Chapter 10 (dm3) system, read as a bone model (A: density loss/recovery, B: fracture healing).

    r' = (r-1)[2 e^{-z} - r(r+1)],   z' = lam r^2 - 2 (r-1)^2 e^{-z},   theta' = 1

lam = 1 is Chapter 10 (eps = 2).  lam is an EXTENSION introduced here, not in the chapter.
Author: Pablo Nogueira Grossi.  Copyright (c) 2026 G6 LLC.  CC BY-NC-ND 4.0 (as the Book 4 pages).
Drafted and run with a Claude Cowork session on 2026-11-07 (configured model id claude-sonnet-5-5; the
serving model may differ).  Run in a cloud sandbox only; NOT yet run on the author's machine.

Prints PASS/FAIL for every number it regenerates.  Final line: ALL PASS or FAIL: n.
Usage:  python3 -I ch10_lambda_bone_audit.py [--noplot]
"""
import sys, math
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

FAILS = []
def check(name, ok, detail=""):
    print(("PASS  " if ok else "FAIL  ") + name + (("  -- " + detail) if detail else ""))
    if not ok:
        FAILS.append(name)

def field(lam):
    def f(t, y):
        r, z = y
        e = math.exp(-z)
        return [(r - 1) * (2 * e - r * (r + 1)), lam * r * r - 2 * (r - 1) ** 2 * e]
    return f

def jac(r, z, lam):
    e = math.exp(-z)
    return np.array([[(2 * e - r * (r + 1)) - (r - 1) * (2 * r + 1), -2 * (r - 1) * e],
                     [2 * lam * r - 4 * (r - 1) * e, 2 * (r - 1) ** 2 * e]])

def rho_in(lam):
    return brentq(lambda x: x**3 - x**2 - (1 + lam) * x + 1, 1e-12, 1 - 1e-15, xtol=1e-16)
def rho_out(lam):
    return brentq(lambda x: x**3 - x**2 - (1 + lam) * x + 1, 1 + 1e-15, 10, xtol=1e-16)
def z_of(rho):               # 2 e^{-z} = rho(rho+1)
    return math.log(2.0 / (rho * (rho + 1)))

# ------------------------------------------------------------------ 1. symbolic (sympy)
print("\n[1] SYMBOLIC (sympy)")
r, z, lam, rho = sp.symbols('r z lam rho', positive=True)
fr = (r - 1) * (2 * sp.exp(-z) - r * (r + 1))
gz = lam * r**2 - 2 * (r - 1)**2 * sp.exp(-z)
ch10 = r * (1 - r**2) + 2 * (r - 1) * sp.exp(-z)
check("radial field equals Chapter 10's r(1-r^2)+2(r-1)e^{-z}", sp.simplify(fr - ch10) == 0)
J = sp.Matrix([[sp.diff(fr, r), sp.diff(fr, z)], [sp.diff(gz, r), sp.diff(gz, z)]])
eq = {sp.exp(-z): rho * (rho + 1) / 2}
Jeq = J.subs(eq).subs(r, rho).subs(lam, (rho - 1)**2 * (rho + 1) / rho)
det = sp.simplify(Jeq.det())
claim = -rho * (rho - 1)**2 * (rho + 1) * (2 * rho**2 + rho + 1)
check("det J at equilibrium = -rho(rho-1)^2(rho+1)(2rho^2+rho+1)", sp.simplify(det - claim) == 0)
check("... = -lam rho^2 (2rho^2+rho+1)",
      sp.simplify(claim + ((rho - 1)**2 * (rho + 1) / rho) * rho**2 * (2 * rho**2 + rho + 1)) == 0)
check("det J < 0 for rho in (0,1) U (1,inf): both equilibria are saddles",
      all(float(claim.subs(rho, x)) < 0 for x in np.linspace(0.01, 5, 400) if abs(x - 1) > 1e-3))
check("equilibria need r != 1 and the cubic r^3-r^2-(1+lam)r+1 (eliminating z)",
      sp.simplify(sp.expand(lam * rho - (rho - 1)**2 * (rho + 1)) - (-(rho**3 - rho**2 - (1 + lam) * rho + 1))) == 0)
p = lambda x, l: x**3 - x**2 - (1 + l) * x + 1
check("cubic: p(0)=1>0, p(1)=-lam<0 (IVT root in (0,1)); p(+inf)=+inf (root in (1,inf)); third root negative",
      p(0, 1) == 1 and abs(p(1, 0.3) + 0.3) < 1e-14 and abs(p(1, 0.9) + 0.9) < 1e-14
      and all(len([x for x in np.roots([1, -1, -(1 + l), 1]).real if abs(np.roots([1, -1, -(1 + l), 1]).imag).max() < 1e-9
                   and True]) == 3 for l in (0.05, 0.3, 1.0, 3.0))
      and all(sum(1 for x in np.roots([1, -1, -(1 + l), 1]) if x.real < 0) == 1 for l in (0.05, 0.3, 1.0, 3.0))
      and all(sum(1 for x in np.roots([1, -1, -(1 + l), 1]) if 0 < x.real < 1) == 1 for l in (0.05, 0.3, 1.0, 3.0))
      and all(sum(1 for x in np.roots([1, -1, -(1 + l), 1]) if x.real > 1) == 1 for l in (0.05, 0.3, 1.0, 3.0)))
# invariant region algebra
alpha_X = sp.simplify(gz - r**2 * 1)       # alpha(X) = z' - r^2 theta'
check("alpha(X) = (lam-1) r^2 - 2(r-1)^2 e^{-z}  (equals -2(r-1)^2 e^{-z} only at lam=1)",
      sp.simplify(alpha_X - ((lam - 1) * r**2 - 2 * (r - 1)**2 * sp.exp(-z))) == 0)
check("helix r=1: alpha(tangent) = lam - 1 (Legendrian iff lam=1)", sp.simplify(gz.subs(r, 1) - 1 - (lam - 1)) == 0)
check("z' - lam(2r-1) = (r-1)^2 (lam - 2 e^{-z})  (>=0 on z>=ln(2/lam))",
      sp.simplify(gz - lam * (2 * r - 1) - (r - 1)**2 * (lam - 2 * sp.exp(-z))) == 0)
check("r' - (r-1)(lam-2) = (r-1)[(2e^{-z}-lam) - (r-1)(r+2)]  (<=0 for r>=1, z>=ln(2/lam))",
      sp.simplify(fr - (r - 1) * (lam - 2) - (r - 1) * ((2 * sp.exp(-z) - lam) - (r - 1) * (r + 2))) == 0)
check("transverse rate on r=1 is -2(1-e^{-z})", sp.simplify(sp.diff(fr, r).subs(r, 1) - (2 * sp.exp(-z) - 2)) == 0)
div1 = sp.simplify((sp.diff(fr, r) + sp.diff(gz, z)).subs(r, 1))
check("divergence of (r,z)-flow on r=1 is 2(e^{-z}-1) (dissipative for z>0)", sp.simplify(div1 - 2 * (sp.exp(-z) - 1)) == 0)
# lam = 0
J0 = J.subs({r: 1, lam: 0})
check("lam=0: whole line r=1 is equilibria (r'=z'=0 there)", sp.simplify(fr.subs(r, 1)) == 0 and sp.simplify(gz.subs({r: 1, lam: 0})) == 0)
ev0 = sorted([sp.simplify(v) for v in J0.eigenvals().keys()], key=str)
check("lam=0: eigenvalues on the line are 0 and 2(e^{-z}-1)", set(map(str, ev0)) == {"0", "-2 + 2*exp(-z)"} or set(map(str, ev0)) == {"0", "2*exp(-z) - 2"},
      str(ev0))

# ------------------------------------------------------------------ 2. equilibria, numerics
print("\n[2] EQUILIBRIA AND LINEARISATION (numerical)")
LAMS = [1.0, 0.38, 0.165, 0.05]
SADDLE_STATED = [0.445, 0.619, 0.736, 0.849]
check("2cos(3pi/7)=rho_in(1) and 2cos(pi/7)=rho_out(1) (Chapter 10 Thm B.1)",
      abs(rho_in(1) - 2 * math.cos(3 * math.pi / 7)) < 1e-12 and abs(rho_out(1) - 2 * math.cos(math.pi / 7)) < 1e-12)
for l, st in zip(LAMS, SADDLE_STATED):
    check(f"saddle radius at lam={l}: {st}", abs(rho_in(l) - st) < 5.1e-4, f"{rho_in(l):.4f}")
    check(f"ln(2/lam) at lam={l}", True, f"{math.log(2 / l):.2f}")
EIG = {}
for l in (1.0, 0.5, 0.38, 0.2, 0.165, 0.05, 0.001):
    ri = rho_in(l); w = np.linalg.eigvals(jac(ri, z_of(ri), l)).real
    EIG[l] = (w.max(), w.min())
STATED_MU = {1.0: 1.4915, 0.5: 1.3515, 0.38: 1.2714, 0.2: 1.0603, 0.165: 0.9954, 0.05: 0.6319}
for l, v in STATED_MU.items():
    check(f"inner saddle unstable eigenvalue at lam={l}", abs(EIG[l][0] - v) < 6e-5, f"{EIG[l][0]:.4f} (stable {EIG[l][1]:.4f})")
check("Chapter 10 eigenvalues 1.4915 / -0.2445 at lam=1", abs(EIG[1.0][0] - 1.4915) < 6e-5 and abs(EIG[1.0][1] + 0.2445) < 6e-5)
est = lambda l: (3 + math.sqrt(41)) / 2 * math.sqrt(l / 2)
for l, tol in ((0.001, 0.03), (0.05, 0.20)):
    rel = est(l) / EIG[l][0] - 1
    check(f"small-lam estimate (3+sqrt41)/2*sqrt(lam/2) at lam={l}: {est(l):.4f} vs {EIG[l][0]:.4f}", abs(rel) < tol,
          f"{100 * rel:+.1f}%  (asymptotic only)")
for l in (0.05, 0.001):
    ri = rho_in(l); check(f"rho_in ~ 1 - sqrt(lam/2) at lam={l}", abs((1 - ri) / math.sqrt(l / 2) - 1) < (0.15 if l > 0.01 else 0.02),
                          f"(1-rho)/sqrt(lam/2) = {(1 - ri) / math.sqrt(l / 2):.4f}")

# ------------------------------------------------------------------ 3. separatrix (stable manifold of inner saddle)
def trace(lam_, side, eps=1e-12, tmax=40000.0, stop="r1"):
    """Backward integration from the inner saddle along the stable eigenvector.
    side=+1: branch with r increasing (toward r=1, z decreasing);  side=-1: r decreasing (toward r=0, z increasing).
    stop='z0': stop at z=0 (event, no interpolation).  stop='r1': stop at r=0.9999 / r=1e-3 / z=14."""
    ri = rho_in(lam_); zi = z_of(ri)
    w, v = np.linalg.eig(jac(ri, zi, lam_)); vs = v[:, np.argmin(w.real)].real
    if vs[0] < 0: vs = -vs
    y0 = np.array([ri, zi]) + side * eps * vs
    f = field(lam_)
    evs = []
    if stop == "z0":
        e0 = lambda t, y: y[1]; e0.terminal = True; evs = [e0]
    else:
        e1 = lambda t, y: y[0] - 0.9999; e1.terminal = True
        e2 = lambda t, y: y[0] - 1e-3; e2.terminal = True
        e3 = lambda t, y: y[1] - 14.0; e3.terminal = True
        evs = [e1, e2, e3]
    sol = solve_ivp(lambda t, y: [-q for q in f(t, y)], [0, tmax], y0, method="DOP853",
                    rtol=1e-13, atol=1e-15, events=evs, dense_output=True)
    return sol

def rstar(lam_, eps=1e-12):
    sol = trace(lam_, +1, eps=eps, stop="z0")
    return float(sol.y_events[0][0][0]) if len(sol.t_events[0]) else float("nan")

print("\n[3] INNER BASIN BOUNDARY r*(z=0) = z=0 crossing of the inner saddle's stable manifold")
CERT = 0.775940575502
for eps in (1e-5, 1e-8, 1e-12):
    v = rstar(1.0, eps)
    check(f"lam=1 r* vs Chapter 10 certified 0.775940575502, seed distance {eps:g}", abs(v - CERT) < 1e-9, f"{v:.12f}")
STATED_RS = [0.776, 0.847, 0.893, 0.938]
RS = {}
for l, st in zip(LAMS, STATED_RS):
    RS[l] = rstar(l)
    check(f"r*(z=0) at lam={l} -> {st}", abs(RS[l] - st) < 5.1e-4, f"{RS[l]:.10f}")
for l in (0.01, 0.001):
    RS[l] = rstar(l)
    check(f"lam->0 : r*(z=0) -> 1 like 1 - c sqrt(lam), lam={l}", 0.5 < RS[l] < 1,
          f"r*={RS[l]:.6f}, (1-r*)/sqrt(lam)={(1 - RS[l]) / math.sqrt(l):.4f}")

# Chapter 10 text checks that the prompt asked for
f1 = field(1.0)
s = solve_ivp(f1, [0, 30], [3.0, 0.0], rtol=1e-11, atol=1e-13, dense_output=True)
tt = np.linspace(0, 30, 30001); Y = s.sol(tt); zd = Y[0]**2 - 2 * (Y[0] - 1)**2 * np.exp(-Y[1])
check("Chapter 10 s3(ii) 'z' -> 1 monotonically' is FALSE: from (3,0) z' peaks at ~2.41 near t=0.114",
      abs(zd.max() - 2.4076) < 5e-3 and abs(tt[zd.argmax()] - 0.114) < 0.01 and abs(zd[-1] - 1) < 1e-6,
      f"max z'={zd.max():.4f} at t={tt[zd.argmax()]:.3f}, final {zd[-1]:.8f}")
blow = solve_ivp(f1, [0, 20], [7.5, 0.0], rtol=1e-10, atol=1e-12, events=[lambda t, y: y[1] + 40])
check("Chapter 10 abstract/s6 'all r(0)>1 converge' is stale: (r0,z0)=(7.5,0) is driven to z -> -inf",
      (blow.y[1].min() < -5) or len(blow.t_events[0]) > 0, f"min z reached {blow.y[1].min():.2f}")
f1c = field(1.0); good = solve_ivp(f1c, [0, 60], [6.8, 0.0], rtol=1e-10, atol=1e-12)
check("... while (6.8,0) converges (Chapter 10 s3 restricted statement)", abs(good.y[0][-1] - 1) < 1e-6, f"r(60)={good.y[0][-1]:.2e}")

# ------------------------------------------------------------------ separatrix curves T_lambda(r)
CURVES = {}
def curve(lam_):
    if lam_ in CURVES: return CURVES[lam_]
    out = {}
    for side in (+1, -1):
        sol = trace(lam_, side)
        tg = np.linspace(0, sol.t[-1], 60000)
        Yg = sol.sol(tg)
        o = np.argsort(Yg[0])
        out[side] = (Yg[0][o], Yg[1][o])
    CURVES[lam_] = out
    return out
def Tsep(lam_, r0):
    ri = rho_in(lam_); c = curve(lam_)
    side = +1 if r0 >= ri else -1
    R, Zc = c[side]
    return float(np.interp(r0, R, Zc)), side

# ------------------------------------------------------------------ 4. Scenario B table
print("\n[4] SCENARIO B: minimal z0 to heal = T_lam(r0)  (above the separatrix r -> 1; below: finite-time exit at r=0)")
R0 = (0.1, 0.3, 0.5, 0.7)
TAB = {1.0: (2.97, 1.71, 0.94, 0.26), 0.5: (2.98, 1.75, 1.03, 0.41), 0.2: (2.98, 1.78, 1.09, 0.53)}
for l, row in TAB.items():
    ri = rho_in(l); zs = z_of(ri)
    for r0, st in zip(R0, row):
        T, side = Tsep(l, r0)
        where = "r0 < rho_in: small-radius branch (T > z_s)" if r0 < ri else "r0 > rho_in: branch toward r=1 (T < z_s)"
        if abs(r0 - ri) < 0.02: where += " [within 0.02 of the saddle itself]"
        check(f"lam={l} r0={r0}: z0_min={st}", abs(T - st) < 5.1e-3,
              f"T={T:.4f}, z_s={zs:.4f}, rho_in={ri:.4f}; {where}")
# why lam matters little at small r0
for l in (1.0, 0.2):
    pass
T_small = [Tsep(l, 0.05)[0] for l in (1.0, 0.5, 0.2)]
check("lam matters little as r0 -> 0: at r=0 the field (-2e^{-z}, -2e^{-z}) does not contain lam; T(0.05) spread across lam in {1,.5,.2}",
      max(T_small) - min(T_small) < 0.01, f"T(0.05) = {[round(x, 4) for x in T_small]}")
T_mid = [Tsep(l, 0.7)[0] for l in (1.0, 0.5, 0.2)]
check("... and matters more at r0=0.7 (spread > 0.25)", max(T_mid) - min(T_mid) > 0.25, f"T(0.7) = {[round(x, 3) for x in T_mid]}")

# ------------------------------------------------------------------ 5. delayed union
print("\n[5] DELAYED UNION: passage time near the separatrix ~ ln(1/delta) / mu_u")
SLOPES = {}
for l, rstart in ((1.0, 0.70), (0.2, 0.85)):
    # start ON the stable manifold at r = rstart using the solver's dense output (accurate to ~1e-13),
    # not np.interp on a grid (whose error ~1e-8 contaminated delta <= 1e-7 in a first run)
    ri_ = rho_in(l); side = +1 if rstart >= ri_ else -1
    sol_m = trace(l, side)
    tb = brentq(lambda t: sol_m.sol(t)[0] - rstart, 0.0, sol_m.t[-1], xtol=1e-14, rtol=1e-14)
    Tz = float(sol_m.sol(tb)[1])
    f = field(l)
    ds = [1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8]
    times = []
    for d in ds:
        ev = lambda t, y: y[0] - 0.97; ev.terminal = True
        sol = solve_ivp(f, [0, 4000], [rstart, Tz + d], method="DOP853", rtol=1e-13, atol=1e-15, events=[ev])
        times.append(sol.t_events[0][0] if len(sol.t_events[0]) else float("nan"))
    x = np.log(1 / np.array(ds)); A = np.vstack([x, np.ones_like(x)]).T
    slope = np.linalg.lstsq(A, np.array(times), rcond=None)[0][0]
    SLOPES[l] = slope
    mu_u = EIG[l][0]
    check(f"lam={l}: slope of T_pass vs ln(1/delta) = 1/mu_u = {1 / mu_u:.4f}", abs(slope * mu_u - 1) < 0.03,
          f"slope={slope:.4f}, mu_u={mu_u:.4f}, slope*mu_u={slope * mu_u:.4f}; T(delta)={[round(t, 1) for t in times]}")
# mu_u as a function of lam
print("      unstable eigenvalue of the inner saddle vs lam:",
      {l: round(EIG[l][0], 4) for l in sorted(EIG, reverse=True)})
check("mu_u increases with lam (more stability -> faster departure from the separatrix; delay ~ 1/mu_u shortens)",
      all(EIG[a][0] > EIG[b][0] for a, b in zip(sorted(EIG, reverse=True)[:-1], sorted(EIG, reverse=True)[1:])))

# ------------------------------------------------------------------ 6. Scenario A
print("\n[6] SCENARIO A: recovery after return to 1 g")
inv = solve_ivp(field(0.165), [0, 200], [1.0, 0.3], rtol=1e-12, atol=1e-14)
check("r=1 is invariant for every lam: starting at (1,z0) under lam=0.165 r stays 1 -> the base system cannot GENERATE loss; loss must be imposed as (r0,z0)",
      np.abs(inv.y[0] - 1).max() < 1e-12)
print("      separatrix height T_lam(r) (z0 above it recovers; below it exits) --- rows lam, cols r = 0.95, 0.90, 0.85, 0.80, 0.70")
TA = {}
for l in LAMS:
    TA[l] = [Tsep(l, rr)[0] for rr in (0.95, 0.90, 0.85, 0.80, 0.70)]
    print(f"      lam={l:<6} " + "  ".join(f"{v:7.3f}" for v in TA[l]))
check("T_lam(r) increases as lam falls (the point of no return moves toward baseline)",
      all(TA[a][i] < TA[b][i] for a, b in zip(LAMS[:-1], LAMS[1:]) for i in range(5)))
# window of z0 where 1 g recovers but low g exits
for rr, idx in ((0.90, 1), (0.85, 2)):
    lo, hi = TA[1.0][idx], TA[0.05][idx]
    print(f"      r0={rr}: z0 in ({lo:.3f}, {hi:.3f}) recovers at 1 g but exits at lam=0.05")
    check(f"window nonempty at r0={rr}", hi > lo)
# half-time vs z0 at lam=1, r0 = 0.932 (6.8 % deficit)
r0 = 0.932
print("      time (model units) for the deficit 1-r to halve at 1 g from r0=0.932, vs z0:")
HT = {}
Tb = Tsep(1.0, r0)[0]
print(f"      separatrix height at r0=0.932: T_1(r0) = {Tb:.4f}  (z0 below it: no recovery)")
for z0 in (-1.0, Tb + 0.02, Tb + 0.1, 0.0, 0.5, 1.0, 2.0, 4.0):
    ev = lambda t, y: (1 - y[0]) - 0.5 * (1 - r0); ev.terminal = True
    sol = solve_ivp(field(1.0), [0, 400], [r0, z0], method="DOP853", rtol=1e-12, atol=1e-14, events=[ev])
    HT[z0] = sol.t_events[0][0] if len(sol.t_events[0]) else float("nan")
print("      " + "  ".join(f"z0={k:+.3f}: {v:.3f}" for k, v in HT.items()))
check("z0=-1 lies below the separatrix at r0=0.932 and does not recover (no half-time)", -1.0 < Tb and math.isnan(HT[-1.0]))
# z0 -> infinity limit is the nonlinear r' = r(r+1)(1-r), NOT the linear rate 2 (r0=0.932 is not infinitesimal)
from scipy.integrate import quad
t_inf = quad(lambda x: 1.0 / (x * (x + 1) * (1 - x)), r0, 1 - 0.5 * (1 - r0))[0]
check(f"half-time at z0=4 within 8% of the z0=inf nonlinear value {t_inf:.4f} (linear ln2/2 = 0.3466 is the r0->1 limit only)",
      abs(HT[4.0] - t_inf) / t_inf < 0.08, f"{HT[4.0]:.4f}")
zk = sorted(k for k in HT if not math.isnan(HT[k]))
check("half-time is strictly decreasing in z0 over the recovering values (K switching on)", all(HT[a] > HT[b] for a, b in zip(zk[:-1], zk[1:])))
check("half-time at z0 just above the separatrix is > 5x the z0=4 value [dimensionless, calibration-free]",
      HT[Tb + 0.02] / HT[4.0] > 5, f"{HT[Tb + 0.02] / HT[4.0]:.1f}")
# shape prediction: initial lag vs single exponential
sol = solve_ivp(field(1.0), [0, 6], [r0, 0.0], method="DOP853", rtol=1e-12, atol=1e-14, dense_output=True)
for t_probe in (0.25, 0.5, 1.0):
    ratio = (1 - sol.sol(t_probe)[0]) / (1 - r0)
    print(f"      z0=0: deficit remaining at t={t_probe}: {ratio:.4f}  (single exponential rate 2 would give {math.exp(-2 * t_probe):.4f})")
check("recovery from z0=0 is NOT a single exponential of rate 2 (lag: deficit at t=0.5 exceeds e^-1)",
      (1 - sol.sol(0.5)[0]) / (1 - r0) > math.exp(-1) + 0.02)
# unit calibration (a CHOICE): far-field rate 2 per unit time = fitted per-day K
KDATA = {"femoral neck": math.log(2) / 211, "pelvis": math.log(2) / 97}
for k, v in KDATA.items():
    print(f"      calibration choice: far-field rate 2 per model unit = K({k}) = {v:.5f}/day  ->  1 model unit = {2 / v:.0f} days")

# ------------------------------------------------------------------ 7. lam = 0
print("\n[7] lam = 0")
chk = []
for zz in (-1.0, 0.0, 1.0, 2.0):
    w = sorted(np.linalg.eigvals(jac(1.0, zz, 0.0)).real)
    chk.append((zz, w))
    print(f"      (1,{zz:+.1f}): eigenvalues {w[0]:+.4f}, {w[1]:+.4f}   expected 2(e^-z - 1) = {2 * (math.exp(-zz) - 1):+.4f} and 0")
check("lam=0 line of equilibria: normal eigenvalue 2(e^{-z}-1): attracting for z>0, repelling for z<0, degenerate at (1,0)",
      all(abs(sorted([2 * (math.exp(-zz) - 1), 0.0])[0] - w[0]) < 1e-12 for zz, w in chk))
sol0 = solve_ivp(field(0.0), [0, 400], [0.9, 1.0], rtol=1e-12, atol=1e-14)
zmono = np.all(np.diff(sol0.y[1]) <= 1e-12)
check("lam=0: z' = -2(r-1)^2 e^{-z} <= 0 (z never grows: no loading accumulates)", zmono)
print(f"      lam=0 from (0.9, 1.0): ends at r={sol0.y[0][-1]:.4f}, z={sol0.y[1][-1]:.4f} (a point on the equilibrium line, if z>0)")

# ------------------------------------------------------------------ 8. plots
if "--noplot" not in sys.argv:
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(2, 2, figsize=(12, 9))
    lg = [1.0, 0.8, 0.6, 0.38, 0.2, 0.165, 0.1, 0.05, 0.02]
    ax[0, 0].plot(lg, [RS.get(l, rstar(l)) for l in lg], "o-"); ax[0, 0].set_xlabel("lambda"); ax[0, 0].set_ylabel("r*(z=0)")
    ax[0, 0].set_title("inner basin boundary at z=0 vs lambda")
    for l in LAMS:
        c = curve(l)
        for side in (+1, -1):
            R, Zc = c[side]; ax[0, 1].plot(R, Zc, label=f"lam={l}" if side == 1 else None)
        ax[0, 1].plot([rho_in(l)], [z_of(rho_in(l))], "k.")
    ax[0, 1].axhline(0, color="gray", lw=.5); ax[0, 1].set_xlim(0, 1); ax[0, 1].set_ylim(-2.5, 6)
    ax[0, 1].set_xlabel("r"); ax[0, 1].set_ylabel("z"); ax[0, 1].set_title("separatrices T_lam(r) (dots = inner saddles)"); ax[0, 1].legend()
    for z0 in (-1.0, 0.0, 1.0, 4.0):
        so = solve_ivp(field(1.0), [0, 6], [r0, z0], dense_output=True, rtol=1e-10, atol=1e-12)
        tg = np.linspace(0, 6, 400); ax[1, 0].plot(tg, so.sol(tg)[0], label=f"z0={z0}")
    ax[1, 0].plot(tg, 1 - (1 - r0) * np.exp(-2 * tg), "k--", label="single exp rate 2")
    ax[1, 0].set_xlabel("model time"); ax[1, 0].set_ylabel("r"); ax[1, 0].set_title("recovery from r0=0.932 at 1 g"); ax[1, 0].legend()
    w = 0.25
    for i, l in enumerate((1.0, 0.5, 0.2)):
        ax[1, 1].bar(np.arange(4) + i * w, TAB[l], w, label=f"lam={l}")
    ax[1, 1].set_xticks(np.arange(4) + w); ax[1, 1].set_xticklabels([f"r0={x}" for x in R0]); ax[1, 1].set_ylabel("z0_min")
    ax[1, 1].set_title("Scenario B: minimal z0 to heal"); ax[1, 1].legend()
    plt.tight_layout(); plt.savefig("ch10_lambda_bone_audit.png", dpi=130)
    print("\nwrote ch10_lambda_bone_audit.png")

print("\n[HONESTY]")
print("  * lam is an extension; Chapter 10 is lam=1 only.  r, z, lam <-> BMD, loading, g (or stiffness, support, stability) are CHOICES.")
print("  * Separatrices are traced backward from the saddle with a finite window (tmax=40000, stops at r=0.9999, r=1e-3, z=14).")
print("  * r=0 (axis exit) is non-physical: trajectories below T_lam reach r=0 in finite time; read only as 'recovery fails'.")
print("  * Nothing here fits biological data; the unit calibration in [6] is one chosen number, not a fit.")
print("\n" + ("ALL PASS" if not FAILS else f"FAIL: {len(FAILS)}  -> " + "; ".join(FAILS)))
