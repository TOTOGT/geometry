#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cislunar-space-verify.py -- companion to book6/cislunar-space.html. Written 2026-11-01. Run BEFORE trusting the page's numbers.
RECOMPUTED here by a second method (Newton, not bisection): L1-L3, Jacobi constants, Hill radius, linear periods and growth times,
synodic month, scaling factors, two-body transfer, Jacobi conservation of a Runge-Kutta orbit.
QUOTED FROM THE AFRL PRIMER (checked against the PDF in Downloads, 2026-11-01): 384,402 km; 42,164 km; 1,728; 1.5 M km; 29.5 d;
12.2 / 14.5 / 20.35 d; mm/s maneuvers. STANDARD VALUES FROM MEMORY: Moon/Earth mass ratio 1/81.3006, sidereal month, year, c, Earth GM.
NOT A SOURCE FOR: radiation, habitats, power, any mission, or any detection limit."""
import math, re, sys
from pathlib import Path
fails=[]
def check(ok,msg):
    print('    %s  %s'%('PASS' if ok else 'FAIL',msg))
    if not ok: fails.append(msg)
def head(n,t): print('\n'+'='*70+'\n  [%s]  %s\n'%(n,t)+'='*70)
HERE=Path(__file__).resolve().parent
html=(HERE/'cislunar-space.html').read_text(encoding='utf-8')
txt=re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',re.sub(r'<style>.*?</style>|<script>.*?</script>|<svg.*?</svg>','',html,flags=re.S)))
m=1/81.3005682; mu=m/(1+m)
def g(x): return x-(1-mu)*(x+mu)/abs(x+mu)**3-mu*(x-1+mu)/abs(x-1+mu)**3
def newton(x):
    for _ in range(100):
        h=1e-7; d=(g(x+h)-g(x-h))/(2*h); x-=g(x)/d
    return x
L1,L2,L3=newton(0.84),newton(1.16),newton(-1.0)
D=384402.; GEO=42164.
head(1,'collinear points (Newton)')
print('    mu=%.7f L1=%.4f L2=%.4f L3=%.4f'%(mu,L1,L2,L3))
for v in ('%.7f'%mu,'%.4f'%L1,'%.4f'%L2,'%.4f'%L3,'{:,.0f}'.format((1-mu-L1)*D),'{:,.0f}'.format((L2-1+mu)*D),'{:,.0f}'.format((-L3-mu)*D)):
    check(v in txt,'page shows '+v)
check(all(abs(g(x))<1e-9 for x in (L1,L2,L3)),'each root satisfies the equation')
r1=math.hypot(.5,math.sqrt(3)/2); check(abs(r1-1)<1e-12,'L4 at (1/2-mu, sqrt3/2) is at distance 1 from Earth and Moon (equilateral): |(1/2,sqrt3/2)|=1')

head(2,'Routh, Jacobi, Hill')
rt=(1-math.sqrt(23/27))/2; check(mu<rt and '%.4f'%rt in txt,'Routh limit %.4f > mu and shown'%rt)
def Om(x,y):
    return .5*(x*x+y*y)+(1-mu)/math.hypot(x+mu,y)+mu/math.hypot(x-1+mu,y)+.5*mu*(1-mu)
C=[2*Om(x,0) for x in (L1,L2,L3)]; C4=2*Om(.5-mu,math.sqrt(3)/2)
print('    C: %s  C4 %.6f'%(['%.4f'%c for c in C],C4))
check(C[0]>C[1]>C[2]>C4 and abs(C4-3)<1e-12,'C(L1)>C(L2)>C(L3)>C(L4), C(L4)=3 in this convention')
for c in C+[C4]: check('%.3f'%c in txt,'page shows C %.3f'%c)
hill=D*(mu/3)**(1/3); check('{:,.0f}'.format(hill) in txt,'Hill radius %.0f km shown'%hill)

head(3,'linear periods and growth')
TS,TY=27.321661,365.256363; tu=TS/(2*math.pi)
def lin(x):
    c=mu/abs(x-1+mu)**3+(1-mu)/abs(x+mu)**3
    # direct 4x4 Jacobian eigenvalues via characteristic polynomial roots
    A=1+2*c; B=1-c
    # lam^4 + (2-A-B)lam^2 + (A*B-... ) : use standard form with uxx=A, uyy=B
    b=4-A-B; cc=A*B
    disc=b*b-4*cc
    l2=[(-b+math.sqrt(disc))/2,(-b-math.sqrt(disc))/2]
    pos=max(l2); neg=min(l2)
    return 2*math.pi/math.sqrt(-neg)*tu, tu/math.sqrt(pos)
for name,x in (('L1',L1),('L2',L2)):
    T,e=lin(x); print('    %s period %.2f d, e-fold %.2f d'%(name,T,e))
    check('%.1f'%T in txt and '%.1f'%e in txt,'page shows %.1f d and %.1f d'%(T,e))
    check(10<T<20 and 1<e<3,'%s values in a sensible range'%name)
check(lin(L2)[0]>lin(L1)[0],'L2 period longer than L1 (as in the primer: 14.5 > 12.2)')

head(4,'clocks and scaling')
syn=1/(1/TS-1/TY); check('%.2f'%syn in txt and abs(syn-29.5)<0.1,'synodic %.2f d agrees with the primer 29.5'%syn)
check('%.3f'%(D/299792.458) in txt,'light time %.3f s'%(D/299792.458))
check('%.2f'%(D/GEO) in txt and abs(D/GEO-9.12)<0.01,'%.2f GEO matches the primer 9.12'%(D/GEO))
check(12**3==1728,'12 cubed is 1728'); check('%.1f'%(1.5e6/GEO) in txt,'1.5 M km is %.1f GEO (primer rounds to 35)'%(1.5e6/GEO))
mag=2.5*math.log10((D/GEO)**2); check('%.1f'%mag in txt and '{:,.0f}'.format((D/GEO)**4) in txt,'%.1f mag, R^4 = %s'%(mag,'{:,.0f}'.format((D/GEO)**4)))
GM=398600.4418; r0=6378.137+300; v0=math.sqrt(GM/r0); vp=math.sqrt(GM*(2/r0-2/(r0+D)))
tt=math.pi*math.sqrt(((r0+D)/2)**3/GM)/86400
print('    TLI %.3f km/s, coast %.3f d'%(vp-v0,tt)); check('%.2f'%(vp-v0) in txt and '%.2f'%tt in txt,'two-body burn and coast shown')
check(abs(.001*86400-86.4)<1e-9 and '86.4' in txt and '2.6 km' in txt,'1 mm/s: 86.4 m/day, 2.6 km/30 d')

head(4.5,'Figure 1 reading (distances from Earth centre in GEO radii)')
for nm,v in (('L1',(L1+mu)*D/GEO),('L2',(L2+mu)*D/GEO),('L3',(-L3-mu)*D/GEO)):
    print('    %s %.2f GEO'%(nm,v)); check('%.2f'%v in txt,'page shows %s %.2f GEO'%(nm,v))
check(7<(L1+mu)*D/GEO<8 and 10<(L2+mu)*D/GEO<11,'L1 in (7,8) and L2 in (10,11) as read off the primer Figure 1')
check('%.1f'%((L2-L1)*D/GEO) in txt,'L1-to-L2 span %.1f GEO shown'%((L2-L1)*D/GEO))

head(4.6,'Figures 2 and 3 (redrawn)')
hills=D*(mu/3)**(1/3)/GEO
check('%.2f'%hills in txt and 3.3>hills*2,'Hill radius %.2f GEO shown, and the by-eye Moon zone (3.3) is more than twice it'%hills)
for lab in ('Reading the primer&rsquo;s Figure 2','Reading the primer&rsquo;s Figure 3','by eye','Top view, z toward you'):
    check(lab in html,'present: '+lab)
x4,y4=.5*(D/GEO),(D/GEO)*math.sqrt(3)/2
check(abs(math.hypot(x4,y4)-D/GEO)<1e-9,'L4 is at the Moon distance %.2f GEO from Earth (all three zones: outside the 5.7 Earth-Moon circle, inside 13.8)'%(D/GEO))
check(5.7<D/GEO<13.8 and 5.7<(-L3-mu)*D/GEO<13.8,'L3, L4, L5 lie between the Earth-Moon and outer circles (by-eye radii 5.7, 13.8)')
check(abs(((L1+mu)-1)*D/GEO)<3.3 and abs(((L2+mu)-1)*D/GEO)<3.3,'L1 and L2 within 3.3 GEO of the Moon (inside the by-eye Moon zone)')

head(5,'Runge-Kutta conserves the Jacobi constant (the page applet uses the same equations)')
def acc(s):
    x,y,u,v=s; r1=math.hypot(x+mu,y); r2=math.hypot(x-1+mu,y)
    return [u,v,x-(1-mu)*(x+mu)/r1**3-mu*(x-1+mu)/r2**3+2*v, y-(1-mu)*y/r1**3-mu*y/r2**3-2*u]
def rk4(s,h):
    k1=acc(s);k2=acc([a+h/2*b for a,b in zip(s,k1)]);k3=acc([a+h/2*b for a,b in zip(s,k2)]);k4=acc([a+h*b for a,b in zip(s,k3)])
    return [a+h/6*(p+2*q+2*r+w) for a,p,q,r,w in zip(s,k1,k2,k3,k4)]
s=[L1+100/D,0,0,0]; c0=2*Om(s[0],s[1]); n=20000
for _ in range(n): s=rk4(s,(60/tu)/n)
c1=2*Om(s[0],s[1])-(s[2]**2+s[3]**2); print('    C start %.8f end %.8f'%(c0,c1))
check(abs(c1-c0)<1e-6,'Jacobi constant conserved to 1e-6 over 60 days')

head(6,'labels and exclusions')
low=txt.lower()
for lab in ['not peer-reviewed','not for navigation or operations','from memory','quoted from the afrl primer','not established here','checked against the pdf']:
    check(lab in low,'label present: '+lab)
check(not re.search(r'lonsdaleite|>\s*90\s*%\s*crew dose',low),'cut lunar claims not reintroduced')
check('radiation' in low and 'does not give radiation doses' in low,'radiation stated as out of scope')
for p in ('wp71-lunar-survivability.html','wp136-living-in-a-moon-habitat.html','../Orthogenesis/Architecture/hex-habitat.html','../index.html'):
    check((HERE/p).exists(),'link target exists: '+p)
check(not any(b in html for b in ('fetch(','localStorage','XMLHttpRequest','<script src')),'no network, storage or external scripts')
print('\n[HONESTY] Arithmetic and labels only. It does not show a detection limit, a dose, a mission design, or that any orbit is usable.')
print('\nALL PASS' if not fails else '\nFAILED: %d'%len(fails)); sys.exit(1 if fails else 0)
