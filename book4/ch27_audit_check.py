#!/usr/bin/env python3
"""ch27 audit evidence (read-only). Tests Result 27.1's second display and the constants. Requires numpy, sympy, mpmath."""
import numpy as np, math, sympy as sp, mpmath as mp
F=[]
def ck(ok,m):
    print('[%s] %s'%('PASS' if ok else 'FAIL',m))
    if not ok: F.append(m)
N=4_000_000
# W by divisor sieve
W=np.zeros(N+1,dtype=np.int64)
for k in range(1,N+1):
    c=1 if k%3==1 else (-1 if k%3==2 else 0)
    if c: W[k::k]+=c
# 1 constants: K = sqrt(L(1,chi) H(1)/pi),  H(s) = (1-3^-s)^-1 prod_{p=2 mod 3} (1-p^-2s)^-1   (Delange)
mp.mp.dps=30
L1=mp.pi/(3*mp.sqrt(3))
def Hlog(P):
    s=mp.log(1/(1-mp.mpf(1)/3))
    for p in sp.primerange(2,P):
        if p%3==2: s+=-mp.log(1-mp.mpf(p)**-2)
    return s
P=10**7; h=Hlog(P)
# tail of sum over p=2 mod 3, p>P of p^-2 ~ (1/2) * 1/(P log P)
tail=0.5/(P*math.log(P)); H1=mp.e**(h+tail)
K=mp.sqrt(L1*H1/mp.pi); lat=mp.pi/mp.sqrt(27); C=lat/K
print('   K = %s   pi/sqrt27 = %s   C = %s'%(mp.nstr(K,8),mp.nstr(lat,8),mp.nstr(C,8)))
ck(abs(K-mp.mpf('0.63899'))<2e-4,'Loeschian Landau-Ramanujan constant K = %s (page 0.6389.../0.638995)'%mp.nstr(K,7))
ck(abs(C-mp.mpf('0.94617'))<2e-4,'C = (pi/sqrt27)/K = %s (page 0.94617)'%mp.nstr(C,7))
# 2 mean of W vs mean of log W over allowed sizes
T=np.arange(N+1); allowed=(W>0)
for x in (10**3,10**4,10**5,10**6,4*10**6):
    a=allowed[1:x+1]; w=W[1:x+1][a]
    mW=w.mean(); mlogW=np.log(w).mean(); lx=math.log(x)
    page=0.5*math.log(lx)+math.log(float(C)); log_of_mean=math.log(mW)
    print('   x=%8d  mean W=%.4f  log(mean W)=%.4f  mean log W=%.4f  page 0.5 loglog x + log C = %.4f   (ln2/2) loglog x = %.4f'%(x,mW,log_of_mean,mlogW,page,0.5*math.log(2)*math.log(lx)))
x=4*10**6; a=allowed[1:x+1]; w=W[1:x+1][a]
mlog=np.log(w).mean(); page=0.5*math.log(math.log(x))+math.log(float(C))
ck(mlog<page-0.15,'measured <log W | W>0> = %.3f at x=4e6, page formula gives %.3f: the formula is the LOG OF THE MEAN, and mean of log < log of mean (Jensen)'%(mlog,page))
# slope in loglog x of the measured mean log W
xs=[10**4,10**5,10**6,4*10**6]
ml=[np.log(W[1:x+1][allowed[1:x+1]]).mean() for x in xs]; ll=[math.log(math.log(x)) for x in xs]
slope=(ml[-1]-ml[0])/(ll[-1]-ll[0]); print('   measured slope d<log W>/d loglog x between 1e4 and 4e6: %.3f  (page: 0.5; ln2/2 = %.3f)'%(slope,0.5*math.log(2)))
sl=[(ml[i+1]-ml[i])/(ll[i+1]-ll[i]) for i in range(len(xs)-1)]
print('   local slopes d<log W>/d loglog x over the four intervals:',['%.3f'%v for v in sl])
ck(sl[0]>sl[1]>sl[2],'local slope of <log W> in loglog x is FALLING (%s), not constant at 1/2; the Poisson heuristic gives asymptotic (ln 2)/2 = 0.347 (heuristic, unproved here)'%', '.join('%.3f'%v for v in sl))
okall=all(np.log(W[1:y+1][allowed[1:y+1]]).mean()<0.5*math.log(math.log(y))+math.log(float(C)) for y in (10**3,10**4,10**5,10**6,4*10**6))
ck(okall,'measured <log W> is below the page formula 0.5 loglog x + log C at every x checked (gap 0.20 at 1e3 to 0.18 at 4e6)')
# the mean of W does track C sqrt(log x)
ck(abs(W[1:x+1][a].mean()/math.sqrt(math.log(x))-0.9045)<0.002,'mean W/sqrt(log x) = %.4f at 4e6 (page 0.90454)'%(w.mean()/math.sqrt(math.log(x))))
# 3 permitted fractions
f1=allowed[1:10**3+1].mean(); f2=allowed[1:x+1].mean(); print('   permitted fraction: %.3f (x=1e3), %.3f (x=1e4: page 0.230), %.3f (4e6, page 0.171)'%(f1,allowed[1:10**4+1].mean(),f2))
ck(abs(allowed[1:10**4+1].mean()-0.230)<0.001 and abs(f2-0.171)<0.001,'permitted fractions 0.230 -> 0.171 reproduced')
# 4 Z[i] analogue (Exercise 27.2)
Kls=0.7642236535892206; Ci=(math.pi/4)/Kls; print('   Z[i]: pi/4 = %.5f, K_LR = %.5f, C = %.5f; reciprocal of unit-cell area (=1) is NOT the analogue of pi/sqrt27'%(math.pi/4,Kls,Ci))
ck(abs(Ci-1.0277)<0.001,'Exercise 27.2: C for Z[i] = pi/4 / 0.76422 = %.4f'%Ci)
# 5 Exercise 27.3
lg=(10/float(C))**2; print('   mean W first exceeds 10 (asymptotic form): log T = %.1f, T ~ 10^%.1f'%(lg,lg/math.log(10)))
raise SystemExit(1 if F else 0)
