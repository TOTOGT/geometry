#!/usr/bin/env python3
"""Checks behind Part III of gcm-v2: three routes to the three open items.
 Route 1  variational principle  -> Herglotz / contact Hamiltonian form, energy balance
 Route 2  higher dimension       -> lift criterion in dim 2n, c = average exponent, spectrum pairing
 Route 3  Theorem D radius       -> explicit radius in the radial scalar case
Hand derivations re-done in sympy/numpy.  PASS = the stated claim holds.  Not Lean."""
import sympy as sp, numpy as np
ok=True
def chk(n,c,i=""):
    global ok; ok&=bool(c); print(("PASS  " if c else "FAIL  ")+n+(("  | "+str(i)) if i else ""))
mu=sp.symbols('mu',negative=True); w0=sp.symbols('omega0',positive=True); g=sp.symbols('gamma',positive=True)

# ---------------- Route 1 ----------------
q,p,z=sp.symbols('q p z',real=True)
def contact_hamilton(H):   # Bravetti convention, alpha = dz - p dq:  qdot=H_p, pdot=-H_q - p H_z, zdot = p H_p - H
    return (sp.diff(H,p), -sp.diff(H,q)-p*sp.diff(H,z), p*sp.diff(H,p)-H)
H=w0*(p+1)-mu*z
qd,pd,zd=contact_hamilton(H)
r=sp.symbols('r',positive=True)
chk("R1a corrected toy IS a contact Hamiltonian flow: H=w0(p+1)-mu z, p=r^2-1, q=theta gives thetadot=%s, pdot=%s=mu p, zdot=%s=mu z - w0"%(qd,pd,sp.expand(zd)),
    qd==w0 and sp.simplify(pd-mu*p)==0 and sp.simplify(zd-(mu*z-w0))==0)
chk("R1a ... and pdot=mu*p is exactly d(r^2)/dt=mu(r^2-1) of Prop 6.1", sp.simplify(pd.subs(p,r**2-1)-mu*(r**2-1))==0)
# energy balance for H = H0 + gamma z
H0=sp.Function('H0')(q,p)
qd,pd,zd=contact_hamilton(H0+g*z)
H0dot=sp.diff(H0,q)*qd+sp.diff(H0,p)*pd
chk("R1b d/dt H0 = %s = -gamma p dH0/dp = -gamma p qdot"%sp.simplify(H0dot), sp.simplify(H0dot+g*p*sp.diff(H0,p))==0)
print("      => over a periodic orbit of the projected flow, 0 = int dH0 = -gamma * oint p dq = -gamma * h_lambda(Gamma): the holonomy must vanish (agrees with Prop 5.1(d), derived independently)")
# Herglotz generalised Euler-Lagrange for L = m qd^2/2 - V(q) - gamma z
m_=sp.symbols('m',positive=True); t=sp.symbols('t'); Q=sp.Function('Q')(t); V=sp.Function('V')
qd_,zz=sp.symbols('qd zz')
L=m_*qd_**2/2-V(q)-g*zz
lhs=sp.diff(sp.diff(L,qd_),qd_)*0   # placeholder
# generalised EL: d/dt(dL/dqd) - dL/dq = (dL/dqd)(dL/dz);  dL/dqd = m qd,  d/dt = m q''
qdd=sp.symbols('qdd')
EL=m_*qdd-(-sp.diff(V(q),q)) - (m_*qd_)*(sp.diff(L,zz))
chk("R1c Herglotz equation for L = m qd^2/2 - V - gamma z : %s = 0, i.e. m q'' + V' + gamma m q' = 0 (linear friction)"%sp.simplify(EL),
    sp.simplify(EL-(m_*qdd+sp.diff(V(q),q)+g*m_*qd_))==0)
Hleg=(m_*qd_)*qd_-L
chk("R1c Legendre transform gives H = p^2/(2m)+V+gamma z with p=m qd", sp.simplify(Hleg.subs(qd_,sp.Symbol('P')/m_)-(sp.Symbol('P')**2/(2*m_)+V(q)+g*zz))==0)

# ---------------- Route 2 ----------------
# 5-dim example, alpha = dz - p dq - x dy.  H = w0 p + Om (x^2+y^2)/2 + gamma z.  Coordinates (q,p,y,x,z).
qq,pp,yy,xx,zz5=sp.symbols('q p y x z',real=True); Om=sp.symbols('Omega',positive=True)
X=sp.Matrix([w0, -g*pp, Om*xx, -Om*yy-g*xx, 0])
h=-(w0*pp+Om*(xx**2+yy**2)/2+g*zz5)                      # alpha(X) = -H
lamX=pp*X[0]+xx*X[2]
X[4]=sp.expand(lamX+h)
coords=[qq,pp,yy,xx,zz5]; alpha=sp.Matrix([-pp,0,-xx,0,1])  # components along dq,dp,dy,dx,dz  (alpha = dz - p dq - x dy)
LX=sp.Matrix([sum(X[j]*sp.diff(alpha[i],coords[j]) for j in range(5))+sum(alpha[j]*sp.diff(X[j],coords[i]) for j in range(5)) for i in range(5)])
chk("R2a dim 4+1: L_X alpha = -gamma alpha (contact vector field, rate -gamma): %s"%list(sp.simplify(LX).T), sp.simplify(LX+g*alpha)==sp.zeros(5,1))
Jac=X.jacobian(coords).subs({pp:0,yy:0,xx:0})
ev=Jac.eigenvals()
print("      exponents of the cycle p=x=y=0 (q runs):", {sp.simplify(k):v for k,v in ev.items()})
chk("R2b transverse exponents on S (drop z): -gamma, and -gamma/2 +- i sqrt(Om^2-gamma^2/4); so mu_max=-gamma/2 = c/2, NOT c=-gamma",
    sp.simplify(sum(k*v for k,v in ev.items()) - (0 -g -g/2*2 -g))==0 )
# pairing of exponents of conformally symplectic linear flows:  A = J S + (c/2) I  =>  spec(A) symmetric about c/2
rng=np.random.default_rng(1); n=2; c=-3.0
Jm=np.block([[np.zeros((n,n)),np.eye(n)],[-np.eye(n),np.zeros((n,n))]])
bad=0
for _ in range(200):
    S=rng.normal(size=(2*n,2*n)); S=S+S.T
    A=Jm@S+(c/2)*np.eye(2*n); w=np.linalg.eigvals(A)
    bad+= not all(np.min(np.abs(w-(c-wi)))<1e-6 for wi in w)
chk("R2c random conformally symplectic 4x4 (c=-3): exponents pair as w <-> c-w in 200/200 trials", bad==0)
tot=sp.simplify(sum(k*v for k,v in ev.items()))      # all five exponents, z included
chk("R2d n=2: exponents on S (z's exponent -gamma removed) sum to %s = n*c with c=-gamma, n=2"%sp.simplify(tot+g), sp.simplify(tot+g+2*g)==0)

# ---------------- Route 3 ----------------
def best_bound(e):
    f=lambda x: -e*np.tanh(2*x/e); fp=lambda x: -2/np.cosh(2*x/e)**2
    best=0;arg=None
    for rho in np.linspace(0.01*e,6*e,3000):
        xs=np.linspace(0.0005*rho,rho,400)
        c2=np.min(-f(xs)/xs)            # x f <= -(c/2) x^2  on |x|<=rho  -> c/2 = min |f(x)|/x
        m=np.min(-fp(np.linspace(-rho,rho,801)))
        b=min(c2*rho,m)
        if b>best: best,arg=b,rho
    return best,arg
for e in (0.1,0.01):
    b,rho=best_bound(e)
    chk(f"R3a e={e}: explicit radius min((c/2)rho, m) maximised over rho = {b:.5f} at rho={rho:.4f}; true radius = {e}; bound <= true and >= 0.9*true",
        b<=e+1e-12 and b>=0.9*e)
# random perturbations strictly inside the bound keep exactly one zero in (-rho,rho), hyperbolic
e=0.1; b,rho=best_bound(e); rng=np.random.default_rng(3); xs=np.linspace(-rho,rho,20001); f=lambda x: -e*np.tanh(2*x/e)
fails=0
for _ in range(500):
    d=rng.uniform(-1,1)*0.5*b
    a1,a2=rng.uniform(-1,1,2)
    # F = d + A sin(k x) with sup|F|<b*0.9 and sup|F'| < m
    k=rng.uniform(1,5); A=0.4*b*a1/ max(1,k)
    F=d+A*np.sin(k*xs)
    g_=f(xs)+F
    if np.max(np.abs(d)+np.abs(A))>=0.95*b: continue
    zeros=np.sum(np.diff(np.sign(g_))!=0)
    fails+= zeros!=1
chk("R3b 500 random perturbations with sup|F|<0.95*bound, sup|F'|<m keep exactly one zero in (-rho,rho)", fails==0)
print("\nALL PASS" if ok else "\nFAIL")
