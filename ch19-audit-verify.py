#!/usr/bin/env python3
"""ch19-enzyme-noncommutativity audit (stdlib). Exit 0 = pass. Mirrors Ch19Enzyme.lean (UNTESTED there)."""
import math,re,sys,random
bad=0
def ck(n,c):
    global bad; print(('PASS ' if c else 'FAIL ')+n); bad+=(not c)
# 1. toy gating/fold on R^2 with linear R
def inside(c,cb,cs,p): return abs(c(p)-cb)<=cs
def K(c,cb,cs,p): return p if inside(c,cb,cs,p) else (0.0,0.0)
def F(Rm,l,p): return (p[0]+l*(Rm[0][0]*p[0]+Rm[0][1]*p[1]), p[1]+l*(Rm[1][0]*p[0]+Rm[1][1]*p[1]))
c=lambda p:p[0]; cb,cs=1.0,0.3; Rm=[[1.0,0],[0,0.5]]; l=1.0
p=(0.9,1.0)
Fp=F(Rm,l,p)
ck('toy: psi inside, F psi outside, F psi != 0',inside(c,cb,cs,p) and not inside(c,cb,cs,Fp) and Fp!=(0.0,0.0))
ck('toy: K(F psi) != F(K psi)',K(c,cb,cs,Fp)!=F(Rm,l,K(c,cb,cs,p)))
# commutes when indicator agrees
q=(1.0,1.0); ck('toy: commute when F keeps psi inside tolerance',inside(c,cb,cs,F(Rm,0.1,q)) and K(c,cb,cs,F(Rm,0.1,q))==F(Rm,0.1,K(c,cb,cs,q)))
# 2. tilt gives Hill exponent 1; exponent 2 needs slope 2
ok1=ok2=True
for _ in range(2000):
    a=random.uniform(-3,3); Kd=random.uniform(.1,5); L=random.uniform(.1,50)
    lhs1=1/(1+math.exp(a-math.log(L/Kd))); r1=1/(1+math.exp(a)*(Kd/L))
    lhs2=1/(1+math.exp(a-2*math.log(L/Kd))); r2=1/(1+math.exp(a)*(Kd/L)**2)
    ok1&=abs(lhs1-r1)<1e-9; ok2&=abs(lhs2-r2)<1e-9
ck('tilt slope 1 -> Hill n=1',ok1); ck('slope 2 -> Hill n=2',ok2)
# local Hill slope of the page's tilted fraction (a=0) at L=Kd: d phi/d lnL * 4 = n
h=1e-6; f=lambda lnL:1/(1+math.exp(-lnL))
n_eff=(f(h)-f(-h))/(2*h)*4
ck('numeric Hill exponent of page tilt at L=Kd is 1 (not 2)',abs(n_eff-1)<1e-6)
raw=open('ch19-enzyme-noncommutativity.html',encoding='utf-8').read()
t=re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',raw))
for g in ['Audit note (2026-10-25)','Hill exponent 1','Proposition 19.1','Modelling statement 19.2','Claim 19.3','Ch19Enzyme.lean']:
    ck('present: '+g,g.lower() in t.lower())
for g in ['THEOREM 19.1','THEOREM 19.2','n = 2 at leading order from μmax = −2']:
    ck('absent: '+g,g.lower() not in t.lower())
sys.exit(1 if bad else 0)
