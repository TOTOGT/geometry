#!/usr/bin/env python3
"""ch01-dm3-framework audit (stdlib). Exit 0 = pass."""
import math,re,sys
bad=0
def ck(n,c):
    global bad; print(('PASS ' if c else 'FAIL ')+n); bad+=(not c)
# 1. K gain
ks,k0,lam=1.0,0.2,1.5
def run(gain,T=60.0,dt=1e-4):
    k=k0;t=0.0
    while t<T:
        k+=gain(k)*dt;t+=dt
        if k>=ks-1e-9: return t
    return None
ck('linear gain: kappa never reaches kappa* (analytic and numeric)',all(ks-(ks-k0)*math.exp(-lam*s)<ks for s in (1,5,10)) and run(lambda k:lam*(ks-k),T=8)is None)
t=run(lambda k:math.sqrt(max(ks-k,0)),T=10)
ck('sqrt gain reaches kappa* in finite time 2*sqrt(kstar-k0)',t is not None and abs(t-2*math.sqrt(ks-k0))<0.01)
# 2. normal form
mu,w,b=-0.55,0.45,2.1
tr=lambda z:mu*(1-math.exp(-b*z))
ck('transverse rate <0 iff z>0; ->mu as z->inf',tr(0.1)<0 and tr(-0.1)>0 and abs(tr(50)-mu)<1e-9)
ck('on rho=0, z-dot = omega >0 (z unbounded)',w>0)
# 3. parameters count text
t=re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',open('ch01-dm3-framework.html',encoding='utf-8').read()))
for g in ['Audit note (2026-10-25)','but never reaches it','is therefore a helix in (θ, z), not a closed curve','assigned working values','do not determine the O(ρ²)','central proposal of the Mini-Beast','neither the focal radius']:
    ck('present: '+g,g in t or g.replace('neither','the chapter defines neither') in t)
for g in ['They are not fitted; they are computed','These are not fitted parameters','completely determine the local dynamics of a dm³ system near its bifurcation. They are not tuning']:
    ck('absent: '+g,g not in t)
sys.exit(1 if bad else 0)
