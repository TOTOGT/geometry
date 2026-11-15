#!/usr/bin/env python3
"""ch28 audit evidence (read-only). Tests scope/sign statements ch28-verify.py does not. Requires sympy, numpy, scipy."""
import sympy as sp, numpy as np
from scipy.integrate import solve_ivp
F=[]
def note(m):
    print('[NOTE hand argument, not computed] '+m)
def ck(ok,m):
    print('[%s] %s'%('PASS' if ok else 'FAIL',m))
    if not ok: F.append(m)
r,th,z=sp.symbols('r theta z',positive=True)
E=sp.exp(-z)
rd=r*(1-r**2)+2*(r-1)*E; td=sp.Integer(1); zd=r**2-2*(r-1)**2*E
aX=sp.simplify(zd-r**2*td)
ck(sp.simplify(aX+2*(r-1)**2*E)==0,'alpha(X) = zdot - r^2 thetadot = -2(r-1)^2 e^-z')
ck(sp.simplify(zd-r**2*td-(zd-r**2))==0,'alpha(X) is zdot with r^2 removed: it renames the negative-definite coupling term written into the zdot equation')
# 1 Gamma = {r=1} is a 2-D cylinder (all theta,z); is invariant; contact planes meet it in a line field (characteristic foliation by helices)
ck(sp.simplify(rd.subs(r,1))==0,'r=1 is invariant (rdot=0 there)')
# cylinder tangent plane span(d_theta,d_z); ker alpha = {a d_r + b d_theta + c d_z : c = r^2 b}
# intersection at r=1: vectors (0,b,c) with c=b -> 1-dimensional
b,c=sp.symbols('b c'); sol=sp.solve(sp.Eq(c,1**2*b),c); print('   at r=1: tangent vectors (0,b,c) in ker alpha satisfy c =',sol[0],'*b  -> a line, not the whole tangent plane')
note('the cylinder r=1 (dim 2) is not Legendrian (Legendrian curves are 1-dim in a contact 3-manifold); it is foliated by Legendrian helices z - theta = const')
# helices: on r=1 flow is thetadot=1, zdot=1, so z-theta is conserved; alpha(gammadot)=0 for every one
ck(sp.simplify(zd.subs(r,1)-1*td)==0,'on r=1: alpha(gamma-dot)=0 for every orbit (all helices z-theta=c are Legendrian, not only gamma*(t)=(1,t,t))')
# 2 Reeb vs dissipation sign
note('Reeb field d_z has alpha(xi)=+1 > 0, whereas alpha(X) <= 0 is dissipation in 28.1: one unit of Reeb flow has the OPPOSITE sign (entropy production -alpha/T = -1/T < 0), i.e. anti-Clausius; not a unit of dissipated energy')
# 3 on the constant-entropy slice alpha(gamma-dot)=dQ, not zero
print('   on dS=0: alpha(gamma-dot) = dQ - T dS = dQ; evaluated on X it is -2(r-1)^2 e^-z != 0 off r=1, so the cost with dS=0 is nonzero')
ck(sp.simplify(aX.subs(r,2))!=0,'with dS=0 the cost alpha(X) is nonzero off r=1: "under dS=0 the same calculation returns zero" is not what 28.1 computes')
# 4 saddle fixed point: rdot=zdot=0 with r!=1 -> r^3 - r^2 - 2r + 1 = 0
rr=[x for x in sp.Poly(r**3-r**2-2*r+1,r).nroots() if abs(sp.im(x))<1e-12 and 0<sp.re(x)<1]
r0_=float(sp.re(rr[0])); E0=r0_*(r0_+1)/2; z0=-np.log(E0)
rdot=r0_*(1-r0_**2)+2*(r0_-1)*E0; zdot=r0_**2-2*(r0_-1)**2*E0
print('   cubic root in (0,1): r=%.10f, E=e^-z=r(r+1)/2=%.6f, z=%.4f, rdot=%.2e, zdot=%.2e'%(r0_,E0,z0,rdot,zdot))
ck(abs(r0_-0.4450418679)<1e-8 and abs(rdot)<1e-12 and abs(zdot)<1e-12,'fixed point of (rdot,zdot) with r != 1 is the root 0.4450418679 of r^3-r^2-2r+1 (derived: 2E=r(r+1), r=(r-1)^2(r+1)); the page quotes the cubic without this derivation')
# 5 coupling-independence (any E>0) and e^{-r}
Ec=sp.Function('Ec')(r,z); ck(sp.simplify((r**2-2*(r-1)**2*Ec)-r**2+2*(r-1)**2*Ec)==0,'alpha(X) = -2(r-1)^2 E for any coupling E (algebra)')
# 6 the dissipation is finite along a trajectory: integrate sigma*T = 2(r-1)^2 e^-z
def rhs(t,y):
    R,Th,Z,_=y; e=np.exp(-Z)
    return [R*(1-R**2)+2*(R-1)*e,1.0,R**2-2*(R-1)**2*e,2*(R-1)**2*e]
for r0 in (0.9,1.2,2.0):
    # integrate sigma*T with an augmented state
    s=solve_ivp(lambda t,y: rhs(t,y),[0,60],[r0,0,0,0],rtol=1e-11,atol=1e-13)
    print('   r0=%.1f: r(60)=%.9f, total sigma*T dt = %.6f (finite)'%(r0,s.y[0,-1],s.y[3,-1]))
note('(informational) total dissipation along orbits is finite; it depends on the initial condition and on the undefined constant T')
raise SystemExit(1 if F else 0)
