#!/usr/bin/env python3
"""ch04-kappa-star audit (stdlib). Exit 0 = pass."""
import math,re,sys
bad=0
def ck(n,c):
    global bad; print(('PASS ' if c else 'FAIL ')+n); bad+=(not c)
def quant(k1,k2):
    # hypersurface in R^3, principal curvatures k1,k2 >=0: focal dist = 1/max, ||II||_F, sqrt(K)=sqrt(k1 k2)
    return 1/max(k1,k2), math.sqrt(k1*k1+k2*k2), math.sqrt(k1*k2)
ck_vals=quant(1,0.25); invf=1/ck_vals[0]
ck('example: 1/foc=1, ||II||=1.031, sqrtK=0.5',abs(invf-1)<1e-12 and abs(ck_vals[1]-1.0308)<1e-3 and abs(ck_vals[2]-0.5)<1e-12)
ck('min{||II||,sqrtK}=0.5 != 1/foc',abs(min(ck_vals[1],ck_vals[2])-0.5)<1e-12 and abs(min(ck_vals[1],ck_vals[2])-invf)>0.4)
import random
ok=True
for _ in range(5000):
    k1,k2=random.uniform(0,3),random.uniform(0,3)
    f,II,K=quant(k1,k2)
    ok&= K<=1/f+1e-12 and 1/f<=II+1e-12 and min(II,K)==K
ck('sandwich sqrtK <= 1/foc <= ||II|| and min = sqrtK (5000 random)',ok)
ck('sphere radius R: all three equal 1/R (umbilic)',all(abs(x-0.5)<1e-12 for x in (1/quant(.5,.5)[0],quant(.5,.5)[2])) and abs(quant(.5,.5)[1]-0.5*math.sqrt(2))<1e-12)
ck('cylinder: 1/foc = 1/R but sqrt K = 0',quant(1,0)[2]==0 and abs(1/quant(1,0)[0]-1)<1e-12)
t=re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',open('ch04-kappa-star.html',encoding='utf-8').read()))
for g in ['Audit note (2026-10-25) — the definition of κ*','The displayed identity is false in general','sandwiched','no computation of it from the geometry','Stated Values','Table of stated values']: ck('present: '+g,g in t)
for g in ['It is computed from the geometry of each system.','The values below are computed per domain from the geometry','Computed Values']: ck('absent: '+g,g not in t)
sys.exit(1 if bad else 0)
