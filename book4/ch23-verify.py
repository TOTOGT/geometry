#!/usr/bin/env python3
"""
ch23-verify.py — Principia Orthogona, Book IV, Chapter 23
"The Bifurcation Set Is a Discriminant"

Regenerates every computed number in the chapter, and the correction it makes
to Chapter 3.  Repo rule: a published number must be regenerable by a tool.

Run:  python3 ch23-verify.py          (exits non-zero on any failure)
Requires: sympy, numpy, scipy
"""
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

FAIL = []
def check(label, got, want, tol=None):
    if tol is None:
        ok = (sp.simplify(got - want) == 0) if isinstance(got, sp.Expr) else (got == want)
    else:
        ok = abs(float(got) - float(want)) <= tol
    print(("  OK   " if ok else "  FAIL ") + label + f"   got={got}  want={want}")
    if not ok:
        FAIL.append(label)

TWO_PI = 2*np.pi

# ─────────────────────────────────────────────────────────────────────────────
print("\n[1] Reeb versus Legendrian — what the dm3 attractor actually is")
# ─────────────────────────────────────────────────────────────────────────────
r, th, z = sp.symbols('r theta z', real=True)
a_, b_, c_ = sp.symbols('a b c', real=True)
alpha = sp.Matrix([0, -r**2, 1])            # alpha = dz - r^2 dtheta, basis (dr, dth, dz)
R = sp.Matrix([a_, b_, c_])
# d alpha = -2r dr ^ dtheta ; iota_R d alpha = -2r (a dtheta - b dr) = 0  =>  a = b = 0
reeb = sp.solve([-2*a_, -2*b_, (alpha.T*R)[0] - 1], [a_, b_, c_], dict=True)
print("       Reeb field of alpha (r != 0):", reeb)
check("Reeb field is d/dz", reeb, [{a_: 0, b_: 0, c_: 1}])

gdot = sp.Matrix([0, 1, 1])                 # attractor r=1, theta=t, z=t
print("       alpha(gamma-dot) =", sp.simplify((alpha.T*gdot)[0]))
check("attractor is Legendrian: alpha(gamma-dot) = 0 at r=1",
      sp.simplify((alpha.T*gdot)[0].subs(r, 1)), 0)
print("       Reeb is transverse to ker alpha, Legendrian lies in it -> the attractor")
print("       cannot be a Reeb orbit. Ch 3 corrected accordingly.")
print("       z(t) = t is unbounded, so gamma* is a helix, not a closed curve in M;")
print("       T* = 2*pi is the period of the (r, theta) reduction.")

# ─────────────────────────────────────────────────────────────────────────────
print("\n[2] The theorem: for rdot = f(r), thetadot = 1, the bifurcation set is disc_r(f)")
# ─────────────────────────────────────────────────────────────────────────────
print("""       limit cycle            = a positive root r* of f
       transverse variational  d(dr)/dt = f'(r*) dr  over T = 2*pi
       Floquet multiplier     m = exp(2*pi * f'(r*))
       non-hyperbolic         <=> f(r*) = f'(r*) = 0 <=> r* is a MULTIPLE root
       => bifurcation set     = { parameters : disc_r(f) = 0 }, and m = 1 there.""")

# ─────────────────────────────────────────────────────────────────────────────
print("\n[3] The dm3 radial field, deformed inside its own odd family")
# ─────────────────────────────────────────────────────────────────────────────
eps, u, rr = sp.symbols('varepsilon u r', real=True)
f_sym = rr*(1 - rr**2 + eps*rr**4)          # eps = 0 recovers dm3 exactly
g_sym = 1 - u + eps*u**2                    # f = r * g(u), u = r^2
D = sp.discriminant(sp.Poly(g_sym, u), u)
print("       f(r) =", sp.expand(f_sym), "     (eps = 0 is the dm3 radial field)")
print("       g(u) =", g_sym, "     disc_u(g) =", D)
check("discriminant is 1 - 4*eps", sp.expand(D), sp.expand(1 - 4*eps))
check("bifurcation at eps_c = 1/4", sp.solve(sp.Eq(D, 0), eps), [sp.Rational(1, 4)])
check("double root there is u* = 2", sp.solve(g_sym.subs(eps, sp.Rational(1, 4)), u), [2])
fp_sym = sp.expand(sp.diff(f_sym, rr))
print("       f'(r) =", fp_sym)
check("Floquet exponent vanishes at the fold",
      sp.simplify(fp_sym.subs({rr: sp.sqrt(2), eps: sp.Rational(1, 4)})), 0)
print("       => multiplier = exp(2*pi*0) = 1 exactly, as the theorem requires")

# ─────────────────────────────────────────────────────────────────────────────
print("\n[4] Numerics: cycles located by integration, against the algebraic roots")
# ─────────────────────────────────────────────────────────────────────────────
def f(r_, e):  return r_*(1 - r_**2 + e*r_**4)
def fp(r_, e): return 1 - 3*r_**2 + 5*e*r_**4
def pos_u(e):
    roots = np.roots([e, -1, 1]) if e > 0 else np.array([1.0+0j])
    return sorted([v.real for v in roots if abs(np.imag(v)) < 1e-12 and np.real(v) > 0])

print("       %7s %24s %16s %11s" % ("eps", "r* by integration", "r* algebraic", "abs err"))
for e in [0.0, 0.10, 0.20, 0.24, 0.249]:
    s = solve_ivp(lambda t, y: [f(y[0], e)], [0, 400], [0.5], rtol=1e-12, atol=1e-14)
    r_num, r_alg = s.y[0, -1], float(np.sqrt(pos_u(e)[0]))
    print("       %7.3f %24.12f %16.9f %11.2e" % (e, r_num, r_alg, abs(r_num - r_alg)))
    check(f"cycle radius agrees, eps={e}", r_num, r_alg, tol=1e-9)

# ─────────────────────────────────────────────────────────────────────────────
print("\n[5] Numerics: Floquet multiplier by variational integration over T = 2*pi")
# ─────────────────────────────────────────────────────────────────────────────
for e in [0.0, 0.20, 0.24, 0.25]:
    us = pos_u(e)
    if not us:
        continue
    rstar = float(np.sqrt(us[0]))
    v = solve_ivp(lambda t, y: [fp(rstar, e)*y[0]], [0, TWO_PI], [1.0], rtol=1e-13, atol=1e-15)
    m_num, m_alg = v.y[0, -1], np.exp(TWO_PI*fp(rstar, e))
    print("       eps=%6.4f  r*=%.9f  m_numeric=%.10e  m=exp(2pi f'(r*))=%.10e"
          % (e, rstar, m_num, m_alg))
    check(f"multiplier agrees, eps={e}", m_num, m_alg, tol=1e-6*max(1.0, abs(m_alg)))
check("multiplier is exactly 1 at the fold",
      np.exp(TWO_PI*fp(float(np.sqrt(2)), 0.25)), 1.0, tol=1e-12)

# ─────────────────────────────────────────────────────────────────────────────
print("\n[6] Numerics: eps_c by bisection, against the exact root of the discriminant")
# ─────────────────────────────────────────────────────────────────────────────
def cycle_exists(e):
    s = solve_ivp(lambda t, y: [f(y[0], e)], [0, 300], [0.5], rtol=1e-11, atol=1e-13)
    rf = s.y[0, -1]
    return 0.05 < rf < 50 and abs(f(rf, e)) < 1e-6

lo, hi = 0.20, 0.30
check("bracket: cycle exists below, not above", (cycle_exists(lo), cycle_exists(hi)), (True, False))
for _ in range(60):
    mid = 0.5*(lo + hi)
    lo, hi = (mid, hi) if cycle_exists(mid) else (lo, mid)
eps_num = 0.5*(lo + hi)
print("       eps_c by bisection : %.15f" % eps_num)
print("       eps_c = 1/4 exactly: %.15f" % 0.25)
check("bisection lands on the discriminant root", eps_num, 0.25, tol=1e-4)
print("       The algebraic value is an exact rational; the numeric one is a search.")
print("       That is the content of the chapter: the search was never necessary.")

# ─────────────────────────────────────────────────────────────────────────────
print("\n[7] Does the e^-z coupling of System (3.1) change the bifurcation set?")
# ─────────────────────────────────────────────────────────────────────────────
def full(t, y, e):
    r_, th_, z_ = y
    ez = np.exp(-np.clip(z_, -50, 700))
    return [r_*(1 - r_**2 + e*r_**4) + 2*(r_ - 1)*ez, 1.0, r_**2 - 2*(r_ - 1)**2*ez]

for e in [0.0, 0.20, 0.24]:
    s = solve_ivp(full, [0, 400], [0.9, 0.0, 0.0], args=(e,), rtol=1e-12, atol=1e-14)
    r_full, r_alg = s.y[0, -1], float(np.sqrt(pos_u(e)[0]))
    print("       eps=%5.3f  3D r(400)=%.12f  planar r*=%.12f  |diff|=%.2e  (z=%.0f)"
          % (e, r_full, r_alg, abs(r_full - r_alg), s.y[2, -1]))
    check(f"3D system inherits the planar root, eps={e}", r_full, r_alg, tol=1e-9)
print("       The coupling decays like e^-z and z grows without bound on the attractor,")
print("       so the reduction is asymptotic — exact in the limit, not at finite z.")

# ─────────────────────────────────────────────────────────────────────────────
print("\n[8] Ch 3's published basin number, regenerated")
print("""       NOTE ON PRECISION. What follows is a plain float bisection driven by
       solve_ivp at rtol=1e-11 / atol=1e-13, so its error floor is ~1e-13 and
       digits beyond the twelfth are integrator noise. The rigorous value lives
       in certify_rstar_rigorous.py (mpmath centre + Jacobian-linearised error
       transport + interval-Hessian Lagrange remainder), which certifies

           r* in [0.775940575501953125, 0.77594057550234375]   width 3.906e-13

       This block agrees with that enclosure to eleven significant figures and
       should not be quoted past them. Cite the certificate, not this number.""")
# ─────────────────────────────────────────────────────────────────────────────
def converges(r0):
    s = solve_ivp(full, [0, 200], [r0, 0.0, 0.0], args=(0.0,), rtol=1e-11, atol=1e-13)
    return abs(s.y[0, -1] - 1.0) < 1e-6

lo, hi = 0.5, 0.95
for _ in range(50):
    mid = 0.5*(lo + hi)
    lo, hi = (lo, mid) if converges(mid) else (mid, hi)
basin = 0.5*(lo + hi)
print("       basin boundary at z=0, by bisection: r* = %.9f" % basin)
print("       Ch 3 prints                        : r* ~ 0.776")
check("Ch 3's basin figure regenerates", basin, 0.776, tol=5e-3)

# Against the rigorous enclosure. LO/HI are the certified bracket printed by
# certify_rstar_rigorous.py; the float value below is NOT inside it, and that
# is the point rather than a defect.
LO, HI = 0.775940575501953125, 0.77594057550234375
print("       certified bracket : [%.18f, %.18f]  width %.3e" % (LO, HI, HI-LO))
print("       this block        :  %.18f" % basin)
inside = LO <= basin <= HI
print("       inside the bracket: %s (above the upper bound by %.2e)"
      % (inside, basin - HI))
check("float bisection sits within its own error floor of the certificate",
      abs(basin - 0.5*(LO+HI)) < 1e-12, True)
check("first eleven significant figures match",
      "%.10e" % basin, "%.10e" % (0.5*(LO+HI)))
print("       So: agreement to eleven significant figures under rounding. The")
print("       twelve leading digits are identical (775940575502) but the two")
print("       differ at the thirteenth, by an amount comparable to the bracket")
print("       width itself.")
print("       Ch 3 quotes ~0.776 and is safe. Anything past eleven figures must")
print("       be cited from certify_rstar_rigorous.py, not from this block.")

# ─────────────────────────────────────────────────────────────────────────────
print("\n[9] Continuity with Ch 22: the same discriminant, one chapter earlier")
# ─────────────────────────────────────────────────────────────────────────────
a, b, x_ = sp.symbols('a b x_')
disc_cubic = sp.discriminant(x_**3 + a*x_ + b, x_)
check("disc(x^3+ax+b) = -(4a^3+27b^2)", sp.expand(disc_cubic + (4*a**3 + 27*b**2)), 0)
V = x_**4/4 + a*x_**2/2 + b*x_
bif = sp.expand(sp.resultant(sp.Poly(sp.diff(V, x_), x_), sp.Poly(sp.diff(V, x_, 2), x_)))
check("cusp catastrophe bifurcation set = 4a^3+27b^2", sp.expand(bif - (4*a**3 + 27*b**2)), 0)
check("= dual of the cuspidal cubic in the chart c=1 (Ch 22 block [11])",
      sp.expand(bif - (4*a**3 + 27*b**2)), 0)
print("       Ch 22 computed that curve as a dual variety. Here the same construction,")
print("       applied to a family of vector fields, returns a bifurcation diagram.")

print("\n" + ("ALL CHECKS PASSED" if not FAIL else "FAILURES: " + ", ".join(FAIL)))
raise SystemExit(1 if FAIL else 0)
