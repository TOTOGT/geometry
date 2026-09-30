#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""g6-architecture-check-verify.py -- checks the building/architecture numbers of Book 2 (TOGT) ch. 5 and ch. 9 (MATHS for life PDF
Book2_VolII_TOGT_eBook.pdf; the chapter text is NOT in the repo HTML) against textbook mechanics, and links them to the joint-compounding
model. Written 2026-09-30 (R24). QUOTED from the book: aspect ratio height/apothem = 66 = 33*tau, tau=2; h_Earth ~ 15,080 m for apothem 229 m;
h_Mars = h_Earth/gamma ~ 39,808 m with gamma = 0.379; lonsdaleite Vickers hardness 114 GPa (Yang et al., Nature 2026, NOT verified); a
1:1000 scale test at 33.5 Hz. QUOTED from other sources (paper sec. 12): compressive strengths of regolith products; basalt 144-292 MPa.
ASSUMED (not data): density 2000 and 2500 kg/m3, Young's modulus 50 GPa. Standard: hexagon geometry, Greenhill self-weight buckling
h_cr = (7.8373 E I / (rho g A))^(1/3)."""
import math, sys
import numpy as np
fails=[]
def check(ok,msg):
    print('    %s  %s'%('PASS' if ok else 'FAIL',msg))
    if not ok: fails.append(msg)
def head(n,t): print('\n'+'='*72+'\n  [%s]  %s\n'%(n,t)+'='*72)
gE=9.80665; gMars=3.71; gMoon=1.62

head(1,'the chapter-5 and chapter-9 arithmetic')
print('    66 = 33 * tau with tau = 2 : %d'%(33*2)); check(33*2==66,'66 = 33 * 2')
print('    apothem 229 m x 66 = %d m ; the book says h_Earth ~ 15,080 m (implied apothem %.2f m); difference %.2f%%'%(229*66,15080/66,100*(229*66-15080)/15080))
check(abs(229*66-15080)/15080<0.005,'229 x 66 is within 0.5% of 15,080')
for gam_lbl,gam in (('book 0.379',0.379),('3.71/9.80665',gMars/gE)):
    print('    h_Mars = 15,080 / %.4f (%s) = %.0f m (the book says 39,808)'%(gam,gam_lbl,15080/gam))
print('    Moon: gamma = %.4f, the same rule gives h_Moon = %.0f m'%(gMoon/gE,15080/(gMoon/gE)))
print('    (the book says the aspect ratio stays 66, so a taller tower has a proportionally wider apothem: %.0f m for the Mars height)'%(39808/66))

head(2,'the 2D claim: "the hexagon is the isoperimetric optimum ... among regular polygons"')
print('    perimeter^2 / area for a regular n-gon = 4 n tan(pi/n)   (smaller = more efficient)')
for n in (3,4,6,8,12,24):
    print('      n=%2d : %.3f'%(n,4*n*math.tan(math.pi/n)))
print('      circle: %.3f'%(4*math.pi))
check(4*12*math.tan(math.pi/12)<4*6*math.tan(math.pi/6),'a regular 12-gon has less perimeter per area than the hexagon')
print('    so "among regular polygons" is false as written. The true statement is the honeycomb theorem (Hales, 1999): among ways to tile the plane with cells of equal area, the hexagonal tiling has the least perimeter.')

head(3,'can a solid hexagonal tower of the stated height stand?  [density 2500 kg/m3, E = 50 GPa ASSUMED]')
rho=2500.0; E=50e9
a=229.0; h=15080.0
A=2*math.sqrt(3)*a*a
print('    hexagon of apothem %.0f m: area = 2 sqrt(3) a^2 = %.0f m2 ; solid prism volume = %.3g m3 ; mass = %.3g kg'%(a,A,A*h,A*h*rho))
print('    base stress of a uniform column = rho g h = %.0f MPa (Earth); sourced strengths: basalt 144-292 MPa, sintered basalt regolith 206 MPa, microwave-sintered 12.6-37, bagging 2-3'%(rho*gE*h/1e6))
check(rho*gE*h/1e6>292,'uniform-column base stress %.0f MPa exceeds the top of the basalt range (292 MPa)'%(rho*gE*h/1e6))
s=2*a/math.sqrt(3); rg2=(5/24)*s*s
hcr=(7.8373*E*rg2/(rho*gE))**(1/3)
print('    Greenhill self-weight buckling: r_g^2 = (5/24) s^2 = %.0f m2 ; h_cr = %.0f m ; the stated height is %.2f x h_cr'%(rg2,hcr,h/hcr))
check(h/hcr>1,'the stated 15,080 m exceeds the Greenhill limit (%.0f m) for a solid prism'%hcr)
hcr_mars=(7.8373*E*(5/18)*(39808/66)**2/(rho*gMars))**(1/3)
print('    Mars tower: apothem %.0f m, h_cr = %.0f m ; the stated 39,808 m is %.2f x h_cr'%(39808/66,hcr_mars,39808/hcr_mars))
check(39808>hcr_mars,'the Mars height exceeds its Greenhill limit too')

head(4,'the proposed 1:1000 model test cannot see a full-scale structural failure')
L=1000.0; hm=h/L; hcr_m=(7.8373*E*(rg2/L**2)/(rho*gE))**(1/3)
print('    full scale: h/h_cr = %.2f (unstable) ; 1:1000 model, same material and shape: h = %.2f m, h_cr = %.1f m, h/h_cr = %.3f (stable)'%(h/hcr,hm,hcr_m,hm/hcr_m))
check(hm/hcr_m<1 and h/hcr>1,'the model is stable where the full tower is not: h_cr scales as L^(2/3), the height as L')
print('    self-weight stress also scales as L: the model sees %.2f MPa against %.0f MPa full scale.'%(rho*gE*hm/1e6,rho*gE*h/1e6))

head(5,'what the gravity-rescaling rule is: the constant-stress limit  h0 = sigma / (rho g)  (rho 2000 kg/m3 ASSUMED)')
print('    uniform-column limit h0 (km): rows = sourced strengths; columns = Earth, Mars, Moon')
for lbl,sig in (('bagging 2 MPa',2e6),('microwave-sintered 12.6 MPa',12.6e6),('direct-sintered 84.6 MPa',84.6e6),('sintered basalt 206 MPa',206e6)):
    print('      %-30s %8.1f  %8.1f  %8.1f'%(lbl,sig/(2000*gE)/1e3,sig/(2000*gMars)/1e3,sig/(2000*gMoon)/1e3))
check(abs(206e6/(2000*gMoon)/1e3-63.58)<0.05,'206 MPa on the Moon: h0 = 63.6 km')
print('    so height limits scale as 1/g exactly as the book\'s rule says; the base height 15,080 m is the unsupported number, not the scaling.')

head(6,'the tie to the joint-compounding model: a constant-stress (tapered) column is its continuous limit')
sigma=12.6e6; rho2=2000.0; g_=gMoon; P=1000.0  # payload mass 1000 kg on top
F0=P*g_; A_top=F0/sigma
for hgt in (1000.0,3000.0,6000.0):
    x=rho2*g_*hgt/sigma
    z=np.linspace(0,hgt,200001)
    Az=A_top*np.exp(rho2*g_*(hgt-z)/sigma)
    M=rho2*np.trapezoid(Az,z)
    print('    h = %5.0f m: x = rho g h / sigma = %.4f ; column mass / payload = %.4f ; e^x - 1 = %.4f'%(hgt,x,M/P,math.exp(x)-1))
    check(abs(M/P-(math.exp(x)-1))/(math.exp(x)-1)<1e-4,'h=%.0f m: column mass / payload = e^x - 1'%hgt)
print('    the discrete model M = P[(1+alpha)^n - 1] tends to P[e^x - 1] with x = n alpha: a tower and a robot arm obey the same law, with x the height in units of h0.')

head(7,'the minimum necessary logistics: the lunar night (standard: half a synodic month, not read here)')
night=29.530588/2*24
print('    night = %.1f h at the equator; energy storage for a continuous load P  (200 Wh/kg battery ASSUMED, K = 5.09-6.66 kg LEO per kg landed)'%night)
for Pk in (5,10,20):
    Ek=Pk*night; mb=Ek/0.2
    print('      P = %2d kW : %6.0f kWh -> %6.1f t of battery -> %5.0f-%5.0f t in Earth orbit'%(Pk,Ek,mb/1e3,mb/1e3*5.09,mb/1e3*6.66))
check(abs(night-354.4)<0.1,'lunar night about 354 h')
print('    the alternative is to work by day only and wait (half the duty), trading time for battery mass.')
print('\n'+('FAIL: %d'%len(fails) if fails else 'all checks passed')); sys.exit(1 if fails else 0)
