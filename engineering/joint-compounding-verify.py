#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""joint-compounding-verify.py -- companion to engineering/beltdraulic-paper.html section 7 (compounding).
Written 2026-09-30 (R24). MODEL, not a measurement: each actuator's mass is a fixed fraction alpha of the load it must carry,
and that load is the payload plus every actuator distal to it on the SAME load path. Link mass and lever arms are ignored
(they make the real compounding stronger). alpha and g are free parameters, not data."""
import sympy as sp, sys
fails=[]
def check(ok,msg):
    print('    %s  %s'%('PASS' if ok else 'FAIL',msg)); 
    if not ok: fails.append(msg)
def head(n,t): print('\n'+'='*72+'\n  [%s]  %s\n'%(n,t)+'='*72)

head(1,'closed form: L_{k-1} = (1+alpha) L_k  =>  total mass M = P((1+alpha)^n - 1)')
a,n,P,g=sp.symbols('alpha n P g',positive=True)
def M_rec(nn,al,Pv=1.0):
    L=Pv; M=0.0
    for _ in range(nn):
        m=al*L; M+=m; L+=m
    return M
check(abs(M_rec(12,0.07)-((1.07)**12-1))<1e-9,'recursion equals closed form (n=12, alpha=0.07)')

head(2,'gain when alpha falls by a factor g:  R(n) = ((1+alpha)^n - 1) / ((1+alpha/g)^n - 1)')
print('    alpha = 0.05 (actuator mass 5% of the load it carries), g = 2')
print('      depth n     M/P before    M/P after     R = before/after')
for nn in (7,10,30,50,100,150,300):
    b=(1.05)**nn-1; af=(1.025)**nn-1
    print('      %5d     %10.3g   %10.3g     %8.2f'%(nn,b,af,b/af))
r7=(1.05**7-1)/(1.025**7-1); r100=(1.05**100-1)/(1.025**100-1)
check(2.0<r7<2.3,'shallow chain (n=7): R = %.2f, barely above g=2: compounding has hardly begun'%r7)
check(10<r100<14,'R = %.1f at n=100: a 2x per-joint gain reaches 10x-20x only at load-path depth of order 100'%r100)
lo=next(nn for nn in range(1,1000) if ((1.05**nn-1)/(1.025**nn-1))>=10)
hi=next(nn for nn in range(1,1000) if ((1.05**nn-1)/(1.025**nn-1))>=20)
print('    smallest depth with R>=10: n=%d ; with R>=20: n=%d  (alpha=0.05, g=2)'%(lo,hi))
print('    for g=3: R>=10 at n=%d ; R>=20 at n=%d'%(
  next(nn for nn in range(1,2000) if ((1.05**nn-1)/((1+.05/3)**nn-1))>=10),
  next(nn for nn in range(1,2000) if ((1.05**nn-1)/((1+.05/3)**nn-1))>=20)))
lim=(sp.log(1+sp.Symbol('a'))/sp.log(1+sp.Symbol('a')/g))
print('    asymptotically R ~ (1+alpha)^n / (1+alpha/g)^n = exp(n*[ln(1+alpha)-ln(1+alpha/g)]): exponential in DEPTH n')


head(5,'lever arms: torque = sum of distal mass x distance; actuator mass m_k = beta x torque  [MODEL] -- is it factorial?')
import math
def lever(n,beta,payload=1.0):
    m=[0.0]*(n+2)
    for k in range(n,0,-1):
        T=payload*(n-k+1)+sum(m[i]*(i-k) for i in range(k+1,n+1))
        m[k]=beta*T
    return m
x=sp.Symbol('x',positive=True); b=sp.Symbol('beta',positive=True)
sol=[sp.simplify(z) for z in sp.solve(sp.Eq((1-x)**2,b*x),x)]
print('    growth per joint inward r = 1/x, with (1-x)^2 = beta x ; roots x =',sol)
for beta in (0.02,0.05):
    m=lever(160,beta)
    xr=((2+beta)-math.sqrt(beta*beta+4*beta))/2
    ratios=[m[k]/m[k+1] for k in (100,60,20)]
    print('    beta=%.2f: numeric m_k/m_{k+1} = %s ; closed form 1/x = %.4f ; 1+sqrt(beta) = %.4f'%(beta,['%.4f'%r for r in ratios],1/xr,1+math.sqrt(beta)))
    check(all(abs(r-1/xr)<1e-6 for r in ratios),'beta=%.2f: successive ratios are constant = 1/x (exponential, NOT factorial)'%beta)
b1,b2=0.05,0.025
r1=1/(((2+b1)-math.sqrt(b1*b1+4*b1))/2); r2=1/(((2+b2)-math.sqrt(b2*b2+4*b2))/2)
print('    halving beta 0.05 -> 0.025 changes the per-joint growth %.4f -> %.4f; ratio %.4f per joint; over depth 100: %.0fx (asymptotic)'%(r1,r2,r1/r2,(r1/r2)**100))
print('    a factorial would need successive ratios that themselves grow with depth; here they are constant, so growth is exponential with base ~ 1+sqrt(beta).')


head(6,'the 1/k! series: (1+alpha)^n = sum_k C(n,k) alpha^k ~ sum_k x^k / k!  with x = n*alpha  [exact identity, then the limit]')
from math import comb, factorial, exp
al,nn=0.05,100; xx=al*nn
exact=sum(comb(nn,k)*al**k for k in range(nn+1))
check(abs(exact-(1+al)**nn)<1e-6*exact,'sum_k C(n,k) alpha^k = (1+alpha)^n  (n=100, alpha=0.05)')
print('    C(n,k) = n(n-1)...(n-k+1)/k!  (falling factorial over k!) ; term k = number of k-subsets of the n joints, each weighted alpha^k')
terms=[comb(nn,k)*al**k for k in range(0,16)]
lim=[xx**k/factorial(k) for k in range(0,16)]
print('      k   C(n,k)a^k   x^k/k!')
for k in (0,1,2,3,4,5,6,8,10,15): print('     %2d   %9.4f   %9.4f'%(k,terms[k],lim[k]))
peak=max(range(16),key=lambda k:terms[k]); print('    x = n*alpha = %.1f ; largest term at k=%d (the limit series peaks at k ~ x)'%(xx,peak))
tail=sum(comb(nn,k)*al**k for k in range(16,nn+1)); print('    mass fraction beyond k=15 terms: %.2e of the total'%(tail/exact))
check(peak in (4,5),'largest term at k = 4 or 5 for x = 5')
print('    the form replaces ln(1+alpha) by alpha: its relative error is of order n*alpha^2 (small only while depth x alpha^2 << 1)')
print('    small-alpha form:  R ~ (e^x - 1)/(e^(x/g) - 1) ;  for large x this tends to exp( x (1 - 1/g) )  (the -1 is the payload)')
for (nq,aq,gq) in ((100,0.05,2),(50,0.05,2),(30,0.05,2),(100,0.02,3),(300,0.05,2)):
    Rex=((1+aq)**nq-1)/((1+aq/gq)**nq-1); x_=nq*aq
    Rap=(exp(x_)-1)/(exp(x_/gq)-1); Rlim=exp(x_*(1-1/gq))
    print('      n=%3d alpha=%.2f g=%d x=%4.1f:  exact R = %8.2f   (e^x-1)/(e^(x/g)-1) = %8.2f   exp(x(1-1/g)) = %8.2f'%(nq,aq,gq,x_,Rex,Rap,Rlim))
    check(abs(Rap-Rex)/Rex<0.6*nq*aq*aq+0.03,'  form within its own error bound 0.6*n*alpha^2+3%% at n=%d alpha=%.2f g=%d (n*alpha^2=%.2f, actual error %.1f%%)'%(nq,aq,gq,nq*aq*aq,100*abs(Rap-Rex)/Rex))
for g_ in (2,3,4):
    print('    large-x limit: R = 10 / 20 needs x = n*alpha >= %.2f / %.2f (g=%d); the finite-x form needs slightly more'%(math.log(10)/(1-1/g_),math.log(20)/(1-1/g_),g_))
print('    so the robot enters only through one number, x = (depth) x (actuator mass fraction), and, to first order in alpha, the gain is (e^x-1)/(e^(x/g)-1).')


head(7,'where to improve: the marginal value of improving joint k  [MODEL]')
import numpy as np
def total_simple(alphas,Pv=1.0):
    L=Pv
    for a_ in reversed(alphas): L*= (1+a_)     # joint n is outermost; L grows going inward
    return L-Pv
n7=12; al=[0.05]*n7
base=total_simple(al)
sens=[]
for k in range(n7):
    a2=list(al); a2[k]*=0.5
    sens.append(base-total_simple(a2))
print('    simple model, equal alpha: mass saved by halving alpha_k, joint k=1 (base) .. %d (tip):'%n7)
print('      '+'  '.join('%.4f'%v for v in sens))
check(max(sens)-min(sens)<1e-9,'simple model: every joint is worth the same (proximal: bigger mass, fewer beneficiaries; distal: smaller mass, more) -- the product is symmetric')
Rall=total_simple(al)/total_simple([a_/2 for a_ in al])
print('    halving alpha at ALL %d joints: R = %.3f; halving only one joint: R = %.3f each'%(n7,Rall,base/(base-sens[0])))
# lever-arm model, beta_k per joint: total mass as a function of the beta vector
def lever_total(betas,payload=1.0):
    n=len(betas); m=[0.0]*(n+2)
    for k in range(n,0,-1):
        T=payload*(n-k+1)+sum(m[i]*(i-k) for i in range(k+1,n+1))
        m[k]=betas[k-1]*T
    return sum(m[1:n+1])
nb=12; be=[0.05]*nb; bt=lever_total(be)
lv=[]
for k in range(nb):
    b2=list(be); b2[k]*=0.5; lv.append(bt-lever_total(b2))
print('    lever-arm model, equal beta=0.05, n=%d: mass saved by halving beta_k (k=1 base .. %d tip):'%(nb,nb))
print('      '+'  '.join('%.3f'%v for v in lv))
print('    ratio tip/base = %.2f ; base/tip = %.2f'%(lv[-1]/lv[0],lv[0]/lv[-1]))
check(True,'ranking reported (see numbers); not asserted as a general law')
print('    So "counting where joints can be improved" is a sensitivity ranking: dM/d(beta_k) at the robot\'s actual numbers. In the simple model it is flat;')
print('    with lever arms it is not, and the ranking must be computed from the robot\'s own geometry, masses and torques.')


head(8,'the limit n -> infinity: finite iff the per-joint fractions are summable  [MODEL]')
print('    total mass M/P = prod_k (1+alpha_k) - 1 ; with equal alpha it diverges as n -> infinity (exponentially).')
print('    The infinite product converges to a finite value iff sum_k alpha_k converges. Example: alpha_k = c/k^2 (fractions taper toward the tip):')
print('        prod_{k>=1} (1 + c/k^2) = sinh(pi*sqrt(c)) / (pi*sqrt(c))')
cc=sp.Symbol('c',positive=True)
for c_ in (0.05,0.5,1.0):
    N=200000
    pr=1.0
    for k in range(1,N+1): pr*=1+c_/(k*k)
    cf=math.sinh(math.pi*math.sqrt(c_))/(math.pi*math.sqrt(c_))
    check(abs(pr-cf)<1e-4,'c=%.2f: partial product to k=%d = %.6f ; sinh(pi sqrt c)/(pi sqrt c) = %.6f'%(c_,N,pr,cf))
c_=0.5
for g_ in (2,3):
    P0=math.sinh(math.pi*math.sqrt(c_))/(math.pi*math.sqrt(c_))
    P1=math.sinh(math.pi*math.sqrt(c_/g_))/(math.pi*math.sqrt(c_/g_))
    print('    infinite chain, c=%.2f: total mass/payload = %.4f ; after dividing every fraction by g=%d: %.4f ; R = %.3f (finite)'%(c_,P0-1,g_,P1-1,(P0-1)/(P1-1)))
print('    and R tends to g as c -> 0 (little compounding) and grows with c: the infinite chain has a finite, computable gain once its taper is known.')
print('    the real limits are physical (material strength, joint size, control bandwidth), not infinity: the equal-fraction model is valid only while x = n*alpha stays in the range where those hold.')

head(3,'what does NOT compound: energy and power add across parallel joints')
print('    energy E_total = sum_j E_j: a per-joint efficiency gain g_e gives total gain g_e, not g_e^N, for N joints in parallel')
Ej=[1.0]*300; Ej2=[1.0/1.5]*300
check(abs(sum(Ej)/sum(Ej2)-1.5)<1e-12,'300 joints, each 1.5x more efficient: system energy ratio 1.5, not 1.5**300')
print('    efficiencies multiply only where power passes IN SERIES through stages (motor x belt x gear), not across separate joints.')

head(4,'what the exponent is: depth along one load path, not the joint count')
print('    a tree: a humanoid has tens of joints in total but a load path from torso to fingertip of order ten joints (approximate, not sourced);')
print('    only a serial chain (snake, continuum arm, cable-driven chain with hundreds of segments) has depth ~ joint count.')
print('\n'+('FAIL: %d'%len(fails) if fails else 'all checks passed')); sys.exit(1 if fails else 0)
