#!/usr/bin/env python3
"""forced-urgency-check.py -- companion to wp32 and wp56, written 2026-11-08 (R24: run before the corrected text was written).
Checks the discrete forced-sale model: keep pays v - chi*1{g>0}; sell at p pays p - chi*1{p<g} (g>0), p (g<=0). Ties accept.
Claims checked: reservation price r(v,g,chi); forced sale below v; sale at price 1 rejected in the counterexample;
non-identification by construction. NOT checked: anything about real data, or that a fitted loss-aversion parameter absorbs clustering."""
import random,sys
fails=[]
def check(ok,m):
    print(('PASS  ' if ok else 'FAIL  ')+m)
    if not ok: fails.append(m)
def accept(p,v,g,chi):
    keep=v-(chi if g>0 else 0)
    sell=p-(chi if (g>0 and p<g) else 0)
    return sell>=keep
def r(v,g,chi):
    if g<=0 or v<=g: return v
    return max(g,v-chi)
random.seed(1);bad=0;N=200000
for _ in range(N):
    v,g,chi=random.uniform(.1,200),random.uniform(-50,150),random.uniform(0,400);p=random.uniform(0,300)
    if accept(p,v,g,chi)!=(p>=r(v,g,chi)): bad+=1
check(bad==0,'reservation price formula matches the accept rule on %d random draws (%d misses)'%(N,bad))
check(accept(50,100,50,1000) and not accept(1,100,50,1000),'counterexample v=100,g=50,chi=1000: accepts 50, rejects 1')
check(accept(50,100,50,1000) and not accept(50,100,0,1000),'p=50 is a forced sale: accepted with g=50, rejected with g=0, v and chi fixed')
bad=0
for _ in range(N):
    R=random.uniform(.1,200);v=R+random.uniform(.01,100);chi=v-R+random.uniform(0,100);p=random.uniform(0,400)
    if accept(p,R,0,0)!=accept(p,v,R,chi): bad+=1
check(bad==0,'non-identification: unconstrained (v=r) and constrained (g=r, v>r, chi>=v-r) give the same accept decision at every offer (%d misses)'%bad)
# control: the check above must detect a wrong construction
bad=0
for _ in range(20000):
    R=random.uniform(.1,200);v=R+random.uniform(1,100);chi=0;p=random.uniform(0,400)
    if accept(p,R,0,0)!=accept(p,v,R,chi): bad+=1
check(bad>0,'control: with chi=0 the construction breaks and the check reports it (%d mismatches)'%bad)
# Response Gap v2 section 5 and 7 checks
import math
a_,b_,k=1.0,8.0,0.5
L=lambda t:a_*t+b_*math.exp(-k*t)
ts=[i/1000 for i in range(0,40001)];tn=min(ts,key=L);ta=math.log(b_*k/a_)/k
check(abs(tn-ta)<0.002,'interior lender optimum t*=ln(bk/a)/k when a<bk: grid %.3f, formula %.3f'%(tn,ta))
a2=5.0;L2=lambda t:a2*t+b_*math.exp(-k*t);check(min(ts,key=L2)==0,'a>=bk: immediate liquidation minimizes lender loss')
eta=0.5;h=lambda t:math.exp(-t);Lp=lambda t,e:L(t)+e*h(t)
check(min(ts,key=lambda t:Lp(t,1.0))>min(ts,key=lambda t:Lp(t,0.0)),'adding a decreasing penalty h lengthens the chosen window')
kap,sl=0.4,-1.5;rho=-kap*sl;mu=100.0;f=lambda m:(m-kap*200)/(1+kap*sl) # p=m-kap*(200+sl*p)
dp=(f(mu+1e-4)-f(mu))/1e-4;check(abs(dp-1/(1-rho))<1e-6,'dp/dmu = 1/(1-rho) for linear supply, rho=%.2f'%rho)
print('RESULT:','ALL PASS' if not fails else '%d FAIL'%len(fails));sys.exit(bool(fails))
