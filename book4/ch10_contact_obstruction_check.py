#!/usr/bin/env python3
"""Checks for Chapter 10, Propositions 3.2 (contact form on the attracting tube) and
3.3 (no contact form near either saddle periodic orbit), lambda = 1; their complements (explicit tube formulas, general-lambda trace) are in sections 6-7.
System: r' = (r-1)[2e^{-z} - r(r+1)], z' = r^2 - 2(r-1)^2 e^{-z}, theta' = 1.
Needs numpy and sympy only. Prints PASS/FAIL per check; exit code 1 on any FAIL.
Hand-derived statements; this script checks the algebra and numbers, not the proofs.
Author: Pablo Nogueira Grossi. Copyright (c) 2026 G6 LLC. CC BY-NC-ND 4.0.
Drafted and run with a Claude Cowork session on 2026-11-08 (configured model id
claude-sonnet-5-5; the serving model may differ).
Run: python3 -I ch10_contact_obstruction_check.py
"""
import sys
import numpy as np
import sympy as sp

fails = []
def check(name, ok, detail=""):
    print(("PASS  " if ok else "FAIL  ") + name + (("  " + detail) if detail else ""))
    if not ok:
        fails.append(name)

r, z, rho = sp.symbols('r z rho', real=True)
f = (r - 1) * (2 * sp.exp(-z) - r * (r + 1))
g = r**2 - 2 * (r - 1)**2 * sp.exp(-z)
J = sp.Matrix([[sp.diff(f, r), sp.diff(f, z)], [sp.diff(g, r), sp.diff(g, z)]])
cubic = rho**3 - rho**2 - 2 * rho + 1          # equilibria, lambda = 1
zrho = sp.log(2 / (rho * (rho + 1)))
Jeq = J.subs({r: rho, z: zrho}).applyfunc(sp.simplify)

# 1. Trace and determinant at an equilibrium, reduced modulo the cubic.
tr = sp.simplify(Jeq.trace())
det = sp.simplify(Jeq.det())
check("tr J = 1 + rho - rho^2 mod cubic", sp.rem(sp.expand(tr - (1 + rho - rho**2)), cubic, rho) == 0)
check("det J = -rho^2 (2 rho^2 + rho + 1) mod cubic",
      sp.rem(sp.expand(det + rho**2 * (2 * rho**2 + rho + 1)), cubic, rho) == 0)

# 2. Numerical multipliers at both positive saddles.
for root in sorted(x.real for x in np.roots([1, -1, -2, 1]) if x.real > 0):
    M = np.array(Jeq.subs(rho, root).evalf(), dtype=float)
    ev = np.linalg.eigvals(M).real
    lm, lp = ev.min(), ev.max()
    check(f"saddle at rho={root:.6f}: lambda- < 0 < lambda+", lm < 0 < lp, f"({lm:.4f}, {lp:.4f})")
    check(f"  tr J nonzero, product of multipliers e^(2 pi tr J) != 1", abs(np.trace(M)) > 0.4,
          f"tr J = {np.trace(M):.6f}, 1+rho-rho^2 = {1 + root - root**2:.6f}")

# 3. The book's alpha = dz - r^2 dtheta: kernel not preserved (dr-coefficient of L_X alpha).
alpha_X = g - r**2                                  # alpha(X) = z' - r^2 * theta'
dr_coef = sp.simplify(sp.diff(alpha_X, r) + 2 * r)   # d(alpha(X)) + i_X d alpha, dr part
check("dr-coefficient of L_X alpha is 2r - 4(r-1)e^{-z}", sp.simplify(dr_coef - (2 * r - 4 * (r - 1) * sp.exp(-z))) == 0)
check("  it is not identically zero (kernel of alpha not preserved)", sp.simplify(dr_coef.subs({r: 1, z: 0})) == 2)

# 4. Strip {4/5 <= r <= 6/5, z >= ln 2}: boundary signs and z' >= 3/5.
fn = sp.lambdify((r, z), f, 'numpy'); gn = sp.lambdify((r, z), g, 'numpy')
zs = np.linspace(np.log(2), 12, 400); rs = np.linspace(0.8, 1.2, 201)
ok_in = np.all(fn(0.8, zs) > 0); ok_out = np.all(fn(1.2, zs) < 0)
R, Z = np.meshgrid(rs, zs)
ok_z = np.all(gn(R, Z) >= 0.6 - 1e-12)
check("r' > 0 on r=4/5 and r' < 0 on r=6/5 for z >= ln 2", ok_in and ok_out)
check("z' >= 3/5 throughout the strip", ok_z, f"min z' = {gn(R, Z).min():.6f}")

# 5. The saddles lie outside the strip.
for root in sorted(x.real for x in np.roots([1, -1, -2, 1]) if x.real > 0):
    zr = float(zrho.subs(rho, root))
    inside = (0.8 <= root <= 1.2) and zr >= np.log(2)
    check(f"saddle rho={root:.4f}, z={zr:.4f} is outside the strip", not inside)


# 6. General lambda: tr J = (rho-1)(rho^3-3rho-1) at an equilibrium; sign of the outer trace.
lam = sp.symbols('lam', positive=True)
gl = lam * r**2 - 2 * (r - 1)**2 * sp.exp(-z)
Jl = sp.Matrix([[sp.diff(f, r), sp.diff(f, z)], [sp.diff(gl, r), sp.diff(gl, z)]])
Jleq = Jl.subs({r: rho, z: zrho}).applyfunc(sp.simplify)
cubic_l = rho**3 - rho**2 - (1 + lam) * rho + 1
trl = sp.simplify(Jleq.trace())
check("general lambda: tr J = (rho-1)(rho^3-3rho-1) mod cubic",
      sp.rem(sp.expand(sp.simplify(trl - (rho - 1) * (rho**3 - 3 * rho - 1))), cubic_l, rho) == 0)
def lam_of(rr): return (rr - 1)**2 * (rr + 1) / rr
rho_star = 2 * np.cos(np.pi / 9); lam_star = lam_of(rho_star)
check("tr J vanishes at rho = 2cos(pi/9), lambda* = (rho-1)^2(rho+1)/rho", abs((rho_star - 1) * (rho_star**3 - 3 * rho_star - 1)) < 1e-12,
      f"lambda* = {lam_star:.6f}")
signs_ok = True
for l in [0.05, 0.38, 1.0, 1.1, 1.18, 1.19, 1.5, 3.0, 10.0]:
    rts = [x.real for x in np.roots([1, -1, -(1 + l), 1]) if x.real > 0 and abs(x.real - 1) > 1e-9]
    lo, hi = min(rts), max(rts)
    t_in = (lo - 1) * (lo**3 - 3 * lo - 1); t_out = (hi - 1) * (hi**3 - 3 * hi - 1)
    signs_ok &= (t_in > 0) and ((t_out < 0) == (l < lam_star)) and abs(t_out) > 1e-6
check("inner trace > 0 and outer trace nonzero with sign change at lambda* (9 lambdas)", signs_ok)

# 7. Tube formulas: variational equations by RK4 (numpy only).
def rk4(F, y, t1, n=20000):
    hh = t1 / n
    for _ in range(n):
        k1 = F(y); k2 = F(y + hh / 2 * k1); k3 = F(y + hh / 2 * k2); k4 = F(y + hh * k3)
        y = y + hh / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return y
def aug(y):
    R_, Z_, Rp, Zp, I = y; e = np.exp(-Z_)
    fr = 2 * e - 3 * R_**2 + 1; fz = -2 * (R_ - 1) * e
    gr = 2 * R_ - 4 * (R_ - 1) * e; gz = 2 * (R_ - 1)**2 * e
    return np.array([(R_ - 1) * (2 * e - R_ * (R_ + 1)), R_**2 - 2 * (R_ - 1)**2 * e,
                     fr * Rp + fz * Zp, gr * Rp + gz * Zp, fr + gz])
h0 = np.log(2); tube_ok = True; cyl_ok = True
for p0 in [0.0, 0.1, -0.15]:
    for t1 in [0.5, 2.0, 5.0]:
        R_, Z_, Rp, Zp, I = rk4(aug, np.array([1 + p0, h0, 1.0, 0.0, 0.0]), t1)
        fR = (R_ - 1) * (2 * np.exp(-Z_) - R_ * (R_ + 1)); gZ = R_**2 - 2 * (R_ - 1)**2 * np.exp(-Z_)
        Delta = Rp * gZ - fR * Zp
        tube_ok &= abs(Delta - (1 + 2 * p0) * np.exp(I)) < 1e-8 * max(1.0, Delta) and Delta > 0
        if p0 == 0.0:
            j = np.exp(1 - np.exp(-t1) - 2 * t1); k = 2 * np.e * (1 + np.exp(-t1)) * np.exp(-np.exp(-t1)) - 4
            cyl_ok &= abs(Rp - j) < 1e-8 and abs(Zp - k) < 1e-8 and abs(Delta - j) < 1e-8
check("Delta(t,p) = (1+2p) exp(int div) > 0 on the tube (9 samples)", tube_ok)
check("on the cylinder: j = e^(1-e^-t-2t), k = 2e(1+e^-t)e^(-e^-t)-4, Delta = j", cyl_ok)

print("\nALL PASS" if not fails else "\nFAILED: " + "; ".join(fails))
sys.exit(1 if fails else 0)
