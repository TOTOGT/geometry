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

head(3,'what does NOT compound: energy and power add across parallel joints')
print('    energy E_total = sum_j E_j: a per-joint efficiency gain g_e gives total gain g_e, not g_e^N, for N joints in parallel')
Ej=[1.0]*300; Ej2=[1.0/1.5]*300
check(abs(sum(Ej)/sum(Ej2)-1.5)<1e-12,'300 joints, each 1.5x more efficient: system energy ratio 1.5, not 1.5**300')
print('    efficiencies multiply only where power passes IN SERIES through stages (motor x belt x gear), not across separate joints.')

head(4,'what the exponent is: depth along one load path, not the joint count')
print('    a tree: a humanoid has tens of joints in total but a load path from torso to fingertip of order ten joints (approximate, not sourced);')
print('    only a serial chain (snake, continuum arm, cable-driven chain with hundreds of segments) has depth ~ joint count.')
print('\n'+('FAIL: %d'%len(fails) if fails else 'all checks passed')); sys.exit(1 if fails else 0)
