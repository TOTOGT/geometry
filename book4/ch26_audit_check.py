#!/usr/bin/env python3
"""ch26 audit evidence (read-only). Tests scope statements ch26-verify.py does not: tolerance dependence of 'forbids nothing', forbidden fractions by rank, Hurwitz counts. Requires numpy, sympy."""
import numpy as np, math, itertools, sympy as sp
F=[]
def ck(ok,m):
    print('[%s] %s'%('PASS' if ok else 'FAIL',m))
    if not ok: F.append(m)
# 1 Theorem 26.1 with INTEGER rungs: nearest-rung error <= f^2/(2(c-f)); sup of relative error; tolerance dependence
c=700.0
def nearest_rel(f):
    n=math.floor(c/f)
    cands=[c/n]+([c/(n+1)])
    return min(abs(r-f) for r in cands)/f
fs=np.concatenate([np.linspace(1,200,400001),np.random.default_rng(2).uniform(1,200,200000)])
rel=np.array([nearest_rel(f) for f in fs]); bound=fs/(2*(c-fs))
ck(bool((rel<=bound+1e-15).all()),'integer ladder 700/N: nearest-rung relative error <= f/(2(c-f)) on %d targets (max ratio %.4f)'%(len(fs),(rel/bound).max()))
for f0 in (10,50,100,200):
    m=fs[(fs>f0*0.9)&(fs<f0*1.1)]; r=np.array([nearest_rel(f) for f in m])
    print('   near f=%3d: max rel error %.4f, bound %.4f'%(f0,r.max(),f0/(2*(c-f0))))
# tolerance dependence: fraction of targets in (40,60) matched within a given relative tolerance
m=np.linspace(40,60,200001); r=np.array([nearest_rel(f) for f in m])
for tol in (0.04,0.01,0.001,0.0001):
    print('   tolerance %.4f: fraction of targets in (40,60) Hz matched by 700/N = %.3f'%(tol,(r<=tol).mean()))
ck((r<=0.04).mean()==1.0 and (r<=0.001).mean()<0.1,'700/N matches all targets only at tolerance >= ~f/(2c); at 0.1%% it matches %.1f%% of targets in (40,60) Hz: it forbids the rest'%(100*(r<=0.001).mean()))
# 2 forbidden fractions
def loesch(N):
    a=np.zeros(N+1,bool); m=1
    while m*m<=N:
        n=np.arange(0,N); t=m*m+m*n+n*n; a[t[t<=N]]=True; m+=1
    a[0]=False; return a
def twosq(N):
    a=np.zeros(N+1,bool); m=0
    while m*m<=N:
        n=np.arange(0,N); t=m*m+n*n; a[t[t<=N]]=True; m+=1
    a[0]=False; return a
L=loesch(200000); fe=100*(1-L[1:].mean()); print('   Z[w]: forbidden to 2e5 = %.1f%%'%fe); ck(abs(fe-80.6)<0.1,'page: 80.6% forbidden to 200,000')
L2=loesch(2000);T2=twosq(2000); print('   to 2000: Z[w] forbidden %.1f%%, Z[i] forbidden %.1f%%'%(100*(1-L2[1:].mean()),100*(1-T2[1:].mean())))
ck(abs(100*(1-L2[1:].mean())-74.0)<0.1 and abs(100*(1-T2[1:].mean())-69.0)<0.1,'page: 74.0% and 69.0% forbidden to 2000')
# 3 forbidding depends on the number of variables, not on the unit-group order
def rep_ternary(N):
    a=np.zeros(N+1,bool); r=int(N**.5)+1
    for x in range(r):
        for y in range(r):
            if x*x+y*y>N: break
            zs=np.arange(0,r); t=x*x+y*y+zs*zs; a[t[t<=N]]=True
    a[0]=False; return a
Tn=rep_ternary(200000); ft=100*(1-Tn[1:].mean()); print('   x^2+y^2+z^2: forbidden %.2f%% (Legendre: 4^a(8b+7), density 1/6 = 16.67%%)'%ft)
ck(abs(ft-100/6)<0.3,'ternary sum of three squares (cubic lattice Z^3) forbids ~16.7%, strictly between planar (~70-80%) and Hurwitz (0%)')
def rep_form(N,coef):
    a=np.zeros(N+1,bool); r=int(N**.5)+1
    for x in range(r):
        for y in range(r):
            t=x*x+coef*y*y
            if t>N: break
            a[t]=True
    a[0]=False; return a
F5=rep_form(200000,5); f5=100*(1-F5[1:].mean()); print('   x^2+5y^2 (|mu|=2): forbidden %.1f%%'%f5)
ck(f5>fe,'binary form with unit group of order 2 (Q(sqrt-5)) forbids %.1f%%, MORE than Z[omega] (|mu|=6, %.1f%%) at the same bound: group order is not what drives forbidding'%(f5,fe))
# non-universal quaternary form
def rep4(N,co):
    a=np.zeros(N+1,bool); r=int(N**.5)+1
    xs=[np.arange(0,int((N/c_)**.5)+1)**2*c_ for c_ in co]
    s=xs[0][:,None]+xs[1][None,:]; s=s[s<=N].ravel(); s=np.unique(s)
    t=xs[2][:,None]+xs[3][None,:]; t=t[t<=N].ravel(); t=np.unique(t)
    for v in t:
        u=s+v; a[u[u<=N]]=True
    a[0]=False; return a
Q=rep4(20000,(1,1,1,8)); miss=[n for n in range(1,200) if not Q[n]]
print('   x^2+y^2+z^2+8w^2 misses:',miss[:10])
ck(len(miss)>0,'a quaternary form (x^2+y^2+z^2+8w^2) is non-universal: "quaternary => forbids nothing" is a property of the sum of four squares')
# 4 Hurwitz vs Lipschitz counts
def lipschitz(n):
    r=int(n**.5)+1; c_=0
    for a in range(-r,r+1):
        for b in range(-r,r+1):
            for c2 in range(-r,r+1):
                d2=n-a*a-b*b-c2*c2
                if d2>=0:
                    d=int(round(d2**.5))
                    if d*d==d2: c_+= 1 if d==0 else 2
    return c_
def hurwitz(n):  # integer + half-integer quaternions of norm n  (all coords integers, or all half-odd-integers: 4n = sum of four odd squares)
    cnt=lipschitz(n)
    N4=4*n; r=int(N4**.5)+1; odd=[x for x in range(-r,r+1) if x%2]
    half=sum(1 for q in itertools.product(odd,repeat=4) if sum(x*x for x in q)==N4)
    return cnt+half
for n in (1,2,3,4,5,6,7):
    m=n
    while m%2==0: m//=2
    print('   n=%d: Lipschitz r4=%d, Hurwitz=%d, 24*sigma(odd part)=%d'%(n,lipschitz(n),hurwitz(n),24*sp.divisor_sigma(m)))
ck(all(hurwitz(n)==24*sp.divisor_sigma(next(m for m in [n>>k for k in range(0,20)] if m%2==1)) for n in (1,2,3,4,5,6,7)),'Hurwitz-order elements of norm n number 24*sigma(odd part of n) (n=1: 24 units), not Jacobi r4(n) (n=1: 8)')
raise SystemExit(1 if F else 0)
