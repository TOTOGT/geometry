#!/usr/bin/env python3
"""ch19-neural-transition audit (stdlib). Exit 0 = pass."""
import math,re,sys
bad=0
def ck(n,c):
    global bad; print(('PASS ' if c else 'FAIL ')+n); bad+=(not c)
mu,w,b=0.55,0.45,2.1
ck('half-life ln2/0.55 = 1.26 s > 1 and > 0.2',math.log(2)/mu>1 and math.log(2)/mu>0.2)
ck('fold time pi/0.45 = 6.98 s > 6.9',math.pi/w>6.9)
ck('omega .45 rad/s is a 14 s period',abs(2*math.pi/w-13.96)<0.05)
sign=lambda z:-mu*(1-math.exp(-b*z))
ck('rho-dot coefficient negative iff z>0',sign(0.1)<0 and sign(-0.1)>0 and abs(sign(0))<1e-12)
ok=True
for z0,r0 in [(0.5,1.0),(-0.5,0.2),(0.0,0.5)]:
    r,z,dt=r0,z0,2e-3; z_start=None
    for i in range(int(40/dt)):
        r+=-mu*(1-math.exp(-b*z))*r*dt; z+=(w-mu*r*r*math.exp(-b*z))*dt
        if i==int(20/dt): z20=z
    ok&= r<1e-3 and abs((z-z20)/20-w)<0.01
ck('numeric: rho->0 and z grows at ~omega (no closed cycle)',ok)
t=re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',open('ch19-neural-transition.html',encoding='utf-8').read()))
for g in ['What holds, and what it does not (audit, 2026-10-25)','not a closed limit cycle','contain no input','neural_timescales_exceed_window']:
    ck('present: '+g,g in t)
sys.exit(1 if bad else 0)
