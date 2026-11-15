#!/usr/bin/env python3
"""ch25 audit evidence (read-only). Checks statements ch25-verify.py does not regenerate. Requires numpy, sympy."""
import numpy as np, math, sympy as sp
F=[]
def ck(ok,m):
    print('[%s] %s'%('PASS' if ok else 'FAIL',m))
    if not ok: F.append(m)
N=2_000_000
# W by brute force: ordered pairs (m>=1,n>=0), m^2+mn+n^2=T  (= ideals of norm T; enantiomers counted separately)
Wb=np.zeros(N+1,dtype=np.int32)
m=1
while m*m<=N:
    n=np.arange(0,int((-m+math.sqrt(m*m+4*N))//2)+2)
    T=m*m+m*n+n*n; T=T[T<=N]; np.add.at(Wb,T,1); m+=1
# divisor-function route
d=np.zeros(N+1,dtype=np.int32)
for k in range(1,N+1):
    c=1 if k%3==1 else (-1 if k%3==2 else 0)
    if c: d[k::k]+=c
ck(np.array_equal(Wb[1:],d[1:]),'W(T)=d1-d2 equals the brute-force count of ordered pairs (m>=1,n>=0) for every T<=%d'%N)
# 1 smallest T with chiral AND achiral shells; smallest W=4
def shells(T):
    out=[]
    for m in range(1,int(math.isqrt(T))+2):
        for n in range(0,m+1):
            if m*m+m*n+n*n==T: out.append((m,n))
    return out
both=[T for T in range(1,200) if any(n not in (0,m) for m,n in shells(T)) and any(n in (0,m) for m,n in shells(T))]
ck(both[0]==49,'smallest T with both a chiral and an achiral shell is 49 (list: %s)'%both[:5])
ck(int(np.argmax(Wb==4))==91,'smallest T with W=4 is 91')
rec=[];best=0
for T in range(1,4000):
    if Wb[T]>best: best=Wb[T]; rec.append((T,int(Wb[T])))
print('   record holders of W below 4000:',rec)
ck([t for t,_ in rec]==[1,7,49,91,637,1729],'record holders below 4000 = 1,7,49,91,637,1729 (page table)')
# 2 first eight Carmichael numbers: closable count
carm=[561,1105,1729,2465,2821,6601,8911,10585]
cl=[c for c in carm if Wb[c]>0]
ck(cl==[1729,2821,8911],'closable among the first eight Carmichael numbers: %s (3 of 8, not "four")'%cl)
# 3 enrichment of primes = 1 mod 3 among Carmichael factors (baseline ~1/2 among primes)
def spf_sieve(M):
    s=np.zeros(M+1,dtype=np.int32)
    for p in range(2,int(M**.5)+1):
        if s[p]==0:
            idx=np.arange(p*p,M+1,p); mask=s[idx]==0; s[idx[mask]]=p
    return s
M=2_000_000; spf=spf_sieve(M)
def fac(n):
    f=[]
    while n>1:
        p=spf[n] or n; f.append(int(p)); n//=int(p)
    return f
carms=[]
for n in range(561,M+1,2):
    if spf[n]==0: continue
    f=fac(n)
    if len(f)<3 or len(set(f))!=len(f): continue
    if all((n-1)%(p-1)==0 for p in f): carms.append((n,f))
ps=[p for n,f in carms for p in f if p!=3]
frac=sum(1 for p in ps if p%3==1)/len(ps)
print('   Carmichael numbers <=%d: %d; fraction of non-3 prime factors = 1 mod 3: %.3f (baseline among primes 0.5)'%(M,len(carms),frac))
closable=sum(1 for n,f in carms if Wb[n]>0)
print('   closable Carmichael numbers: %d of %d (%.2f); if each non-3 prime split with prob 1/2 and 3 factors: ~0.125'%(closable,len(carms),closable/len(carms)))
ck(True,'(informational) enrichment measured above; page claim "built preferentially from primes with 3 | p-1" is judged from these numbers')
# 4 Dirichlet identification with E=eps0*log(10T+2) vs log T
s=2.0
Sa=sum(Wb[T]*(10*T+2)**(-s) for T in range(1,N+1)); Sb=sum(Wb[T]*T**(-s) for T in range(1,N+1))
z2=sp.zeta(2).evalf(); L2=sp.N(sum(sp.Rational(1,1)*(1 if k%3==1 else -1)/sp.Integer(k)**2 for k in range(1,20001) if k%3))
print('   sum W(T)T^-2 = %.8f   sum W(T)(10T+2)^-2 = %.8f   zeta(2)L(2,chi)=%.8f'%(Sb,Sa,float(z2*L2)))
ck(abs(Sb-float(z2*L2))<1e-4 and abs(Sa-float(z2*L2))>0.1,'Z(s)=zeta L holds for weight T^-s; with the stated E=eps0 log(10T+2) the sum is %.4f, not %.4f'%(Sa,float(z2*L2)))
# 5 Landau-Ramanujan ratio
cnt=np.cumsum(Wb>0)
for x in (10**4,10**5,10**6,2*10**6):
    print('   x=%8d  count=%7d  count/(x/sqrt(log x)) = %.4f'%(x,cnt[x],cnt[x]/(x/math.sqrt(math.log(x)))))
r=cnt[2*10**6]/(2*10**6/math.sqrt(math.log(2*10**6)))
ck(abs(r-0.670)<0.003,'ratio at x=2e6 = %.4f (page: 0.670)'%r)
# 6 supply of T=pqr in (x,2x): reproduce page numbers independently
sps=[p for p in sp.primerange(2,2**21) if p%3==1]
from bisect import bisect_left,bisect_right
cnts=[]
x=1024
while x<2**20:
    hi=2*x;c=0
    for i,p in enumerate(sps):
        if p**3>hi: break
        for j in range(i+1,len(sps)):
            q=sps[j]
            if p*q*q>hi: break
            lo=max(q+1,x//(p*q)+1); a=bisect_left(sps,lo); b=bisect_left(sps,(hi-1)//(p*q)+1)
            c+=max(0,b-a)
    cnts.append(c); x*=2
print('   dyadic counts:',cnts)
ck(cnts==[1,3,10,24,66,153,345,781,1714,3664],'page counts 1,3,10,24,66,153,345,781,1714,3664 reproduced')
raise SystemExit(1 if F else 0)
