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

head(3,'what does NOT compound: energy and power add across parallel joints')
print('    energy E_total = sum_j E_j: a per-joint efficiency gain g_e gives total gain g_e, not g_e^N, for N joints in parallel')
Ej=[1.0]*300; Ej2=[1.0/1.5]*300
check(abs(sum(Ej)/sum(Ej2)-1.5)<1e-12,'300 joints, each 1.5x more efficient: system energy ratio 1.5, not 1.5**300')
print('    efficiencies multiply only where power passes IN SERIES through stages (motor x belt x gear), not across separate joints.')

head(4,'what the exponent is: depth along one load path, not the joint count')
print('    a tree: a humanoid has tens of joints in total but a load path from torso to fingertip of order ten joints (approximate, not sourced);')
print('    only a serial chain (snake, continuum arm, cable-driven chain with hundreds of segments) has depth ~ joint count.')
print('\n'+('FAIL: %d'%len(fails) if fails else 'all checks passed')); sys.exit(1 if fails else 0)
