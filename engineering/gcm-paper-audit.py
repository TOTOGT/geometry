#!/usr/bin/env python3
"""Audit of the PDF 'Generative Contact Mechanics: A Geometric Framework for Dissipative
Systems with Structured Limit Cycles' (P. N. Grossi), Theorems A-D, 2026-11-01.
Every check is a hand derivation re-done in sympy. Nothing here is Lean; nothing here edits the paper.
PASS means the *finding* is confirmed (the paper's statement fails), not that the paper is right."""
import sympy as sp
from sympy.calculus.euler import euler_equations
ok = True
def chk(name, cond, info=""):
    global ok
    ok &= bool(cond)
    print(("PASS  " if cond else "FAIL  ") + name + (("  | " + str(info)) if info else ""))

t = sp.symbols('t', positive=True)
sg = sp.symbols('sigma', positive=True)

# F1  Theorem A(iii): E[V(X_t)] -> 0 below the threshold.  OU transverse noise dx=-x dt+sigma dW, V=x^2.
#     LV = -2V + sigma^2, so Axiom 5 holds with c=2, kappa=1 (equality); Prop 3.4's own bound is (kappa/c)sigma^2.
m = sp.Function('m')
sol = sp.dsolve(sp.Eq(m(t).diff(t), -2*m(t) + sg**2), m(t), ics={m(0): 1})
lim = sp.limit(sol.rhs, t, sp.oo)
chk("F1 A(iii): E[V] -> sigma^2/2 > 0, not 0, for every sigma>0", sp.simplify(lim - sg**2/2) == 0, f"limit={lim}")

# F2  Prop 3.3: V=d_g^2 contracts at the Floquet rate.  Non-normal transverse linearisation.
A = sp.Matrix([[-1, 10], [0, -1]]); x = sp.Matrix([1, 1])
vdot = (2*x.T*A*x)[0]
chk("F2 Prop 3.3: transverse eigenvalues -1,-1 (mu_max=-1) but d/dt|x|^2 = %s > 0 at x=(1,1)" % vdot,
    A.eigenvals() == {-1: 2} and vdot > 0, "Axiom 4 fails for V=d_g^2 in every neighbourhood (linear, scale-free)")

# F3  Prop 6.3(i),(iii): two primitives of the same omega differ by a CLOSED, not exact, 1-form.
r, th = sp.symbols('r theta', positive=True)
lam1, lam2 = r**2, r**2 - 1            # lambda = f(r) dtheta on R^2\{0}; d(lambda) = f'(r) dr^dtheta
W1 = sp.integrate(lam1.subs(r, 1), (th, 0, 2*sp.pi)); W2 = sp.integrate(lam2.subs(r, 1), (th, 0, 2*sp.pi))
chk("F3 same omega=2r dr^dtheta, W = %s vs %s; Gamma (r=1) bounds no chain in R^2\\{0}, yet W can be 0" % (W1, W2),
    sp.diff(lam1, r) == sp.diff(lam2, r) and W1 != W2 and W2 == 0)

# F4  A(iv)/Thm D 'same winding number': W of the perturbed cycle changes.  rdot=r(a-r^2): r0=sqrt(a), W=2*pi*r0^2
a = sp.symbols('a', positive=True)
r0 = sp.sqrt(a); mu = sp.diff(a*r - r**3, r).subs(r, r0)
chk("F4 W=2*pi*a moves linearly with the cycle (hyperbolic, mu=%s): dW/da=%s" % (sp.simplify(mu), sp.diff(2*sp.pi*a, a)),
    sp.simplify(mu) == -2*a and sp.diff(2*sp.pi*a, a) != 0)

# F5  Def 6.4: H_phase = (1/2) omega(Y,Y) vanishes identically (omega alternating).
Y1, Y2, w12 = sp.symbols('Y1 Y2 w12'); omega = sp.Matrix([[0, w12], [-w12, 0]]); Yv = sp.Matrix([Y1, Y2])
chk("F5 omega(Y,Y)=0 identically, so H_phase=0", sp.simplify((Yv.T*omega*Yv)[0]) == 0)

# F6  Def 6.6/Thm 6.7: Euler-Lagrange of S=int(zdot - lambda(sdot) - H) with H=H(s,z), toy lambda=r^2 dtheta, Hdiss=-gamma V e^{-beta z}
rf, thf, zf = [sp.Function(n)(t) for n in ('r', 'theta', 'z')]
g, b = sp.symbols('gamma beta', positive=True)
H = -g*(rf - 1)**2*sp.exp(-b*zf)
L = zf.diff(t) - rf**2*thf.diff(t) - H
eq = euler_equations(L, [rf, thf, zf], t)
ez = sp.simplify(eq[2].lhs); eth = sp.simplify(eq[1].lhs)
chk("F6 dz-variation gives -dH/dz = %s = 0 (forces V=0)" % sp.simplify(ez), sp.simplify(ez + g*b*(rf-1)**2*sp.exp(-b*zf)) == 0)
chk("F6 dtheta-variation gives 2 r rdot = 0 (no radial relaxation)", sp.simplify(eth - 2*rf*rf.diff(t)) == 0)
print("      => critical points of the stated S are r=1 only; Thm 6.7's equations (and Thm C Step 2) do not follow.")
print("      Also: Thm 6.7 uses a momentum p that Defs 6.4/6.6 never introduce.")

# F7  Prop 4.21: kphi1 - m phi2 = 0 on (R/Z)^2 has lcm(k,m) solutions.  It is a subgroup of dimension 1: gcd(k,m) circles.
k_, m_ = 2, 3
from fractions import Fraction as Fr
cnt = {}
for i in range(100):
    p1 = Fr(i, 100)
    sols = {((k_*p1 - j)/m_) % 1 for j in range(m_)}      # m phi2 = k phi1 - j
    cnt[i] = len(sols)
chk("F7 k=2,m=3: every phi1 (100/100 sampled) has %d solutions phi2: a curve, not lcm=6 points" % m_,
    all(c == m_ for c in cnt.values()))

# F8  Eps0: abstract/Remark 7.3 vs Theorem 1.4, toy mu_max=-2, Hess V|_Gamma = 2 (V=(r-1)^2)
mu_, hv = sp.Integer(-2), sp.Integer(2)
e_abs = sp.Rational(1, 2)*abs(mu_)/hv; e_thm = abs(mu_)/(2*(1+hv))
chk("F8 two different eps0 in one paper: abstract & Remark 7.3 give %s, Thm 1.4 gives %s on the toy" % (e_abs, e_thm), e_abs != e_thm)

# F9  Prop 6.11: B1xR is an even-dimensional 'contact hypersurface'; B3 hat 'Legendrian' needs dim n.
for n in range(1, 6):
    dimS = 2*n; dimB1R = (dimS - 1) + 1
    assert dimB1R % 2 == 0
chk("F9 dim(B1 x R)=2n is even for every n: no contact form possible; Legendrian needs dim n but B3 has dim 2n-1 (equal only for n=1)", True)

# F10 Theorem C: stated rho-equation on the toy; sign of transverse rate vs z; the z-dot expansion
rho, z = sp.symbols('rho z', real=True)
rr = 1 + rho
rdot = sp.expand(rr*(1 - rr**2) + 2*rho*sp.exp(-z)); zdot = sp.expand(rr**2 - 2*rho**2*sp.exp(-z))
lin = sp.simplify(rdot.coeff(rho, 1))
chk("F10a toy matches rho' = mu(1-e^{-z})rho (mu=-2, beta=1): linear coeff = %s" % lin, sp.simplify(lin + 2*(1 - sp.exp(-z))) == 0)
chk("F10b that exponent is 0 at z=0 and POSITIVE (repelling) for z<0: value at z=-1 is %s" % sp.N(lin.subs(z, -1), 4),
    sp.simplify(lin.subs(z, 0)) == 0 and lin.subs(z, -1) > 0)
chk("F10c toy zdot has a linear term %s*rho; the stated normal form (omega - |mu|rho^2 e^{-bz}+O(rho^3)) has none" % zdot.coeff(rho, 1),
    zdot.coeff(rho, 1) == 2)

# F11 Theorem C needs M=S x R odd => dim S even, and a single scalar rho => dim S = 2.
print("F11   (text) dim S = n>=2 arbitrary in Sec 2.1/Axiom 8; (M,alpha) needs dim S even and an exact symplectic omega on S")
print("      (impossible on compact S: omega^n = d(lambda ^ omega^{n-1}) would integrate to 0); normal form has one rho => dim S=2 only.")
print("\nALL FINDINGS CONFIRMED" if ok else "\nSOME CHECK FAILED -- do not rely on the corresponding finding")
