#!/usr/bin/env python3
"""Checks behind gcm-v2-draft.tex Part I (hand derivations re-done numerically/symbolically). Not Lean."""
import numpy as np, sympy as sp
from scipy.linalg import solve_continuous_lyapunov
ok=True
def chk(n,c,i=""):
    global ok; ok&=bool(c); print(("PASS  " if c else "FAIL  ")+n+(("  | "+str(i)) if i else ""))

# L1 adapted Lyapunov function: Q solves (A+kI)^T Q + Q(A+kI) = -I, V=x^T Q x.  Then QA + A^T Q = -I - 2kQ,
# so Vdot = -|x|^2 - 2kV <= -2kV for every k < |mu_max|  (the paper's non-normal counterexample, A=[[-1,10],[0,-1]]).
A=np.array([[-1.,10.],[0.,-1.]])
for k in (0.5,0.9,0.99):
    Q=solve_continuous_lyapunov((A+k*np.eye(2)).T,-np.eye(2))
    res=Q@A+A.T@Q+np.eye(2)+2*k*Q
    posdef=np.all(np.linalg.eigvalsh(Q)>0)
    xs=np.random.default_rng(0).normal(size=(2000,2))
    vdot=np.einsum('ij,jk,ik->i',xs,Q@A+A.T@Q,xs); V=np.einsum('ij,jk,ik->i',xs,Q,xs)
    chk(f"L1 k={k}: Q>0, QA+A^TQ=-I-2kQ (res {np.abs(res).max():.1e}), Vdot<=-2kV on 2000 samples",
        posdef and np.abs(res).max()<1e-8 and np.all(vdot<=-2*k*V+1e-9))
# scalar case closed form
x,k=sp.symbols('x k',positive=True); V=x**2/(2-2*k); Vd=sp.diff(V,x)*(-x)
chk("L1 scalar xdot=-x: Vdot = -x^2 - 2kV", sp.simplify(Vd-(-x**2-2*k*V))==0)

# L2 ultimate bound: m' <= -c m + K gives m(t) <= e^{-ct} m0 + K/c  (equality case)
t,c,K,m0=sp.symbols('t c K m0',positive=True)
m=sp.exp(-c*t)*m0+K/c*(1-sp.exp(-c*t))
chk("L2 Gronwall equality case solves m'=-c m+K", sp.simplify(sp.diff(m,t)-(-c*m+K))==0)

# L3 holonomy first variation on the toy: W(a)=2*pi*a, cycle r=sqrt(a); dW/da = int omega(d_a Gamma, Gamma') dtheta
a,r,th=sp.symbols('a r theta',positive=True)
omega_rt=2*r                     # omega = 2r dr ^ dtheta
dGamma=1/(2*sp.sqrt(a))          # d r0/da
integrand=(omega_rt*dGamma).subs(r,sp.sqrt(a))   # omega(dGamma d_r, d_theta)
chk("L3 first variation of W equals int omega(delta Gamma, Gamma') : %s*2pi = dW/da"%sp.simplify(integrand),
    sp.simplify(sp.integrate(integrand,(th,0,2*sp.pi))-sp.diff(2*sp.pi*a,a))==0)

# L4 resonance locus: k phi1 - m phi2 in Z on the torus has gcd(k,m) components
from math import gcd
def components(kk,mm,N=240):
    # points (i/N, j/N) with (kk*i - mm*j) % N == 0 ; count connected components under 4-neighbour wraparound after thickening
    import itertools
    pts={(i,j) for i in range(N) for j in range(N) if (kk*i-mm*j)%N==0}
    seen=set(); comp=0
    # adjacency by the group step: (i,j)->(i+mm/g, j+kk/g) generates each component
    g=gcd(kk,mm); st=(mm//g,kk//g)
    for p in pts:
        if p in seen: continue
        comp+=1; q=p
        while q not in seen:
            seen.add(q); q=((q[0]+st[0])%N,(q[1]+st[1])%N)
    return comp
for kk,mm in ((2,3),(2,4),(4,6),(1,2)):
    chk(f"L4 k:m={kk}:{mm}: components={components(kk,mm)} == gcd={gcd(kk,mm)}", components(kk,mm)==gcd(kk,mm))
print("\nALL PASS" if ok else "\nFAIL")
