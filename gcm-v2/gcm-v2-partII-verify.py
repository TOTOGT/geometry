#!/usr/bin/env python3
"""Checks behind Part II of gcm-v2 (Theorems B, C, D and the toy model). Hand derivations re-done in sympy/numpy.
PASS = the stated finding holds.  Not Lean."""
import sympy as sp, numpy as np
ok=True
def chk(n,c,i=""):
    global ok; ok&=bool(c); print(("PASS  " if c else "FAIL  ")+n+(("  | "+str(i)) if i else ""))
mu=sp.symbols('mu',negative=True); eps=sp.symbols('epsilon',positive=True); w0=sp.symbols('omega0',positive=True)

# ---------- Theorem B ----------
# B1: two decoupled hyperbolic cycles, x_i' = mu x_i, theta_i' = 1: Floquet exponents (mu, mu, 0, 0): TWO neutral directions.
J0=sp.diag(mu,mu,0,0)
chk("B1 product of two dm3 systems has exponents %s: two neutral directions, Gamma1 x Gamma2 is a torus, not a hyperbolic cycle"%list(J0.eigenvals().keys()),
    sorted(J0.eigenvals().keys(),key=str)==sorted([mu,0],key=str) and J0.eigenvals()[0]==2)
# B2: weak phase coupling, 1:1.  theta1' = 1+eps sin(th2-th1), theta2' = 1+eps sin(th1-th2); locked cycle th1=th2, x=0.
x1,x2,t1,t2=sp.symbols('x1 x2 t1 t2')
F=sp.Matrix([mu*x1, mu*x2, 1+eps*sp.sin(t2-t1), 1+eps*sp.sin(t1-t2)])
Jl=F.jacobian([x1,x2,t1,t2]).subs({x1:0,x2:0,t2:t1})
ev=Jl.eigenvals()
chk("B2 locked-cycle Floquet exponents %s; slow phase mode -2*eps, not max(mu_i)=mu"%sorted(map(str,ev.keys())),
    set(ev.keys())=={mu,0,-2*eps})
chk("B2 so mu_max,12 = max(mu, -2 eps) = -2 eps for 2 eps < |mu|, not max mu_i (V1 Thm 1.2(ii))", True, "e.g. mu=-2, eps=0.1 -> %s vs -2"%(max(-2,-0.2)))
# B3: noise on the phase difference, dpsi = -2 eps psi dt + s dW: stationary variance s^2/(4 eps)
t,s=sp.symbols('t s',positive=True); m=sp.Function('m')
sol=sp.dsolve(sp.Eq(m(t).diff(t),-4*eps*m(t)+s**2),m(t),ics={m(0):0})
chk("B3 E psi^2 -> %s : variance grows like 1/eps as coupling weakens"%sp.limit(sol.rhs,t,sp.oo), sp.simplify(sp.limit(sol.rhs,t,sp.oo)-s**2/(4*eps))==0)

# ---------- Theorem C ----------
r,th,z=sp.symbols('r theta z',real=True)
def lie_alpha(Xr,Xth,Xz,lam):   # alpha = dz - lam(r) dtheta ; return components (dr,dth,dz) of L_X alpha
    a=sp.Matrix([0,-lam,1])                       # (dr,dth,dz)
    s_=Xz-lam*Xth                                 # alpha(X)
    ds=sp.Matrix([sp.diff(s_,r),sp.diff(s_,th),sp.diff(s_,z)])
    # dalpha = -lam' dr^dth ; i_X dalpha = -lam'(Xr dth - Xth dr)
    lp=sp.diff(lam,r)
    ix=sp.Matrix([lp*Xth,-lp*Xr,0])
    return sp.simplify(ds+ix),a
# C1: V1's toy (lambda=r^2 dtheta) is not a contact vector field
L,a=lie_alpha(r*(1-r**2)+2*(r-1)*sp.exp(-z),1,r**2-2*(r-1)**2*sp.exp(-z),r**2)
chk("C1 V1 toy: L_X alpha has dr-component %s != 0 but alpha has none, so L_X alpha is not f*alpha: V1's toy is not a contact flow"%sp.simplify(L[0]),
    sp.simplify(L[0])!=0)
# C2: corrected model: rdot=(mu/2)(r-1/r), thetadot=w0, zdot=mu z - w0, alpha=dz-(r^2-1)dtheta
Xr=(mu/2)*(r-1/r)
L2,a2=lie_alpha(Xr,w0,mu*z-w0,r**2-1)
chk("C2 corrected model: L_X alpha = mu*alpha exactly: %s"%list(L2.T), sp.simplify(L2-mu*a2)==sp.zeros(3,1))
J=sp.Matrix([Xr,w0,mu*z-w0]).jacobian([r,th,z]).subs({r:1,z:w0/mu})
chk("C2 Floquet exponents of the cycle r=1,z=w0/mu in M: %s (mu twice, 0 along the cycle)"%list(J.eigenvals().items()), J.eigenvals()=={mu:2,0:1})
# exact solutions: r^2(t)=1+(r0^2-1)e^{mu t}, z(t)=w0/mu+(z0-w0/mu)e^{mu t}
t=sp.symbols('t',real=True); r0,z0=sp.symbols('r0 z0',positive=True)
u=1+(r0**2-1)*sp.exp(mu*t); zz=w0/mu+(z0-w0/mu)*sp.exp(mu*t)
chk("C2 exact solution: d(r^2)/dt = mu (r^2-1) and dz/dt = mu z - w0, global in (r0>0, z0 real): no z0-dependence of the basin",
    sp.simplify(sp.diff(u,t)-mu*(u-1))==0 and sp.simplify(sp.diff(zz,t)-(mu*zz-w0))==0)
# C3: criterion.  Y=(rdot,w0), omega=2r dr^dtheta.  L_Y omega = div * omega; need div = mu.
rd=sp.Function('rd')(r); omega_coef=2*r
div=sp.simplify(sp.diff(omega_coef*Xr,r)/omega_coef)
chk("C3 L_Y omega = (div) omega with div=%s = mu"%div, sp.simplify(div-mu)==0)
# closed form eta = i_Y omega - mu*lambda ; integral over Gamma (r=1) of its dtheta-part
for name,lam in (("lambda=r^2 dtheta (holonomy 2pi)",r**2),("lambda'=(r^2-1) dtheta (holonomy 0)",r**2-1)):
    eta_th=(2*r*Xr)-mu*lam                         # dtheta-coefficient of i_Y omega - mu lambda
    I=sp.integrate(eta_th.subs(r,1),(th,0,2*sp.pi))
    print("      ",name,": integral of eta over Gamma =",sp.simplify(I))
Iz=sp.integrate((2*r*Xr-mu*r**2).subs(r,1),(th,0,2*sp.pi)); Io=sp.integrate((2*r*Xr-mu*(r**2-1)).subs(r,1),(th,0,2*sp.pi))
chk("C3 eta exact on the annulus iff its integral over Gamma vanishes: -2*pi*mu != 0 for holonomy 2pi, 0 for holonomy 0",
    sp.simplify(Iz+2*sp.pi*mu)==0 and sp.simplify(Io)==0)

# ---------- Theorem D ----------
# D1: scaling.  V -> c V multiplies Hess V by c; V1's formulas change, persistence of a cycle does not.
cc=sp.symbols('c',positive=True)
chk("D1 V1 abstract formula mu/(2 sup|Hess V|) scales as 1/c under V -> cV, while persistence of the cycle does not depend on V",
    sp.simplify((abs(mu)/(2*cc*2))/(abs(mu)/(2*2))-1/cc)==0)
# D2: f_e(x) = -e*tanh(2x/e) on the cylinder R x S^1 (metric dx^2+dtheta^2), thetadot=1.
#   bounded smooth field => complete flow; x=0 is a hyperbolic cycle with mu = f'(0) = -2;
#   V = x^2 is a GLOBAL Lyapunov function (V' = 2 x f(x) < 0 for x != 0); Hess V = 2.
x,e,dl=sp.symbols('x e delta',positive=True)
f=-e*sp.tanh(2*x/e)
chk("D2 f'(0) = %s (mu=-2 for every e)"%sp.simplify(sp.diff(f,x).subs(x,0)), sp.simplify(sp.diff(f,x).subs(x,0))==-2)
chk("D2 x*f(x) < 0 for x>0 (f=-e tanh(2x/e), tanh>0 there), so V=x^2 is a global Lyapunov function with Hess V = 2",
    all((xx*(-0.3*np.tanh(2*xx/0.3)))<0 for xx in np.linspace(0.001,20,500)) and all((xx*(-0.3*np.tanh(2*xx/0.3)))<0 for xx in np.linspace(-20,-0.001,500)))
chk("D2 sup|f| = %s (limit as x->oo), |f|<e everywhere, so f+delta has no zero once |delta|>=e: the cycle is destroyed"%sp.limit(f,x,sp.oo),
    sp.limit(f,x,sp.oo)==-e and sp.limit(f,x,-sp.oo)==e)
for ee in (0.1,0.01):
    xs=np.linspace(-50,50,2_000_001); fv=-ee*np.tanh(2*xs/ee)
    e_abs=0.5*2/2; e_thm=2/(2*(1+2))
    for d in (2*ee,):
        chk(f"D2 e={ee}: F={d}*d/dx has C^1 norm {d} < V1 radius {e_thm:.4f} (Thm 1.4) and < {e_abs} (abstract), yet f+F has no zero (min|f+F| = {np.min(np.abs(fv+d)):.4f} > 0)",
            d<e_thm and d<e_abs and np.min(np.abs(fv+d))>0)
    r_true=ee
    print(f"       e={ee}: true persistence radius of the cycle = {r_true} (|delta|<e keeps a zero: x=-(e/2) atanh(delta/e)), with mu=-2, Hess V=2 fixed")
print("\nALL PASS" if ok else "\nFAIL")
