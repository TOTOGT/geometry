#!/usr/bin/env python3
"""ch24 audit evidence (read-only). Tests statements ch24-verify.py does not: scope of the Theorem, degree drop, 3-D near the fold. Requires sympy, numpy, scipy."""
import sympy as sp, numpy as np
from scipy.integrate import solve_ivp
F=[]
def ck(ok,m):
    print('[%s] %s'%('PASS' if ok else 'FAIL',m))
    if not ok: F.append(m)
r,lam,eps,u=sp.symbols('r lambda epsilon u')
# 1 Theorem 24.2 scope: disc_r f = 0 does not imply a cycle with multiplier 1
f=(r+1)**2*(r-lam)
ck(sp.simplify(sp.discriminant(sp.expand(f),r))==0,'f=(r+1)^2(r-lambda): disc_r f == 0 for every lambda (double root at r=-1)')
fp=sp.diff(f,r).subs(r,lam)
ck(sp.simplify(fp-(lam+1)**2)==0 and all((l+1)**2>0 for l in (0.5,1,3)),"  yet the only positive cycle r=lambda has f'(lambda)=(lambda+1)^2>0, so m=exp(2pi(lambda+1)^2)!=1 for every lambda>0")
g=r*(r**2+lam)
d=sp.factor(sp.discriminant(sp.expand(g),r)); print('   f=r(r^2+lambda): disc_r =',d,' (zero at lambda=0 where r=0 is a triple root; no positive root, no cycle, multiplier undefined)')
ck(sp.solve(d,lam)==[0] and [k for k in sp.roots(sp.Poly(sp.expand(g.subs(lam,0)),r)) if k>0]==[],'disc vanishes at lambda=0 where f=r^3 has no positive root')
# 2 degree drop: bifurcation of cycle count at eps=0 not seen by disc_u g
gu=1-u+eps*u**2
discg=sp.discriminant(gu,u); print('   disc_u g =',discg)
def npos(e):
    rts=np.roots([e,-1,1]) if e!=0 else np.array([1.0])
    return int(sum(1 for x in rts if abs(x.imag)<1e-12 and x.real>0))
cnt={e:npos(e) for e in (-0.1,-1e-3,0.0,1e-3,0.1,0.24)}
print('   number of positive cycles (u=r^2>0 roots of g):',cnt)
ck(cnt[-1e-3]==1 and cnt[1e-3]==2 and discg.subs(eps,0)!=0,'cycle count jumps 1 -> 2 across eps=0 although disc_u g(0)=1 != 0 (cycle born at infinity: leading coefficient, not discriminant)')
# 3 disc_r of the full odd quintic has factors besides (1-4 eps)
fr=eps*r**5-r**3+r
print('   disc_r f =',sp.factor(sp.discriminant(fr,r)))
# 4 cuspidal-cubic dual = discriminant of depressed binary cubic (section of the twisted-cubic dual): same polynomial 4a^3+27b^2c
c0,c2,c3,s,t=sp.symbols('c0 c2 c3 s t')
bc=c0*t**3+c2*t+c3  # binary cubic c0 s^3 + c2 s t^2 + c3 t^3 in affine s=1... t -> variable
disc3=sp.factor(sp.discriminant(c0*t**3+c2*t+c3,t)); print('   disc of c0 t^3 + c2 t + c3 =',disc3)
a_,b_,cc=sp.symbols('a b c')
ck(sp.simplify(disc3.subs({c2:a_,c3:b_,c0:cc})/(-cc)-(4*a_**3+27*b_**2*cc))==0,'disc(c0 t^3+c2 t+c3) = -c0(4c2^3+27c0c3^2): dual of cuspidal cubic 4a^3+27b^2c with (a,b,c)=(c2,c3,c0)')
# 5 3-D system near the fold, outside the table of block [7] (eps<=0.24)
def rhs(t,y,e):
    R,th,z=y
    return [R*(1-R**2+e*R**4)+2*(R-1)*np.exp(-z),1.0,R**2-2*(R-1)**2*np.exp(-z)]
def run(e,r0=0.9,T=400):
    ev=lambda t,y,e: y[0]-50; ev.terminal=True
    sol=solve_ivp(rhs,[0,T],[r0,0,0],args=(e,),rtol=1e-11,atol=1e-13,events=ev,method='LSODA')
    return sol.y[0,-1],sol.t[-1],sol.y[2,-1]
for e in (0.249,0.2499,0.2501,0.26):
    R,tt,z=run(e); planar=None
    if e<0.25: planar=np.sqrt((1-np.sqrt(1-4*e))/(2*e))
    print('   eps=%.4f: r_end=%.9f at t=%.1f z=%.1f planar r*=%s'%(e,R,tt,z,'%.9f'%planar if planar else 'none (no root)'))
R1,t1,_=run(0.2499); R2,t2,_=run(0.2501,T=400)
ck(R2>=50 or t2<400,'3-D: eps=0.2501 > 1/4 escapes (r reaches 50 before t=400)')
ck(abs(R1-np.sqrt((1-np.sqrt(1-4*0.2499))/(2*0.2499)))<1e-3,'3-D: eps=0.2499 settles near the planar root (slow near the fold, tolerance 1e-3)')
raise SystemExit(1 if F else 0)
