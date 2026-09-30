#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""moonbase-hangar-verify.py -- companion to engineering/beltdraulic-paper.html section 12 (a hangar printed from regolith).
Written 2026-09-30 (R24). QUOTED (sources on the page): heating 1 t of regolith to 1000 C needs at least 233 kWh (specific heat
0.84 kJ/(kg K), losses excluded); compressive strengths: regolith bagging 2-3 MPa, microwave sintering 12.6-37, direct sintering
84.6-218.8, sintered basalt regolith 206 MPa; direct-sintered tensile/flexural 7.2-8.2 MPa; RASSOR 2.0 dry mass ~66 kg, payload 80 kg.
ASSUMED (not data): hangar geometry, shell thickness, printed density 2000 kg/m3, printer system mass 2000 kg, trip time, duty factor,
K = 5.09-6.66 from moonbase-warehouse-verify.py. The hangar's real size is not known: results are an ILLUSTRATION, not a design."""
import math, sys
fails=[]
def check(ok,msg):
    print('    %s  %s'%('PASS' if ok else 'FAIL',msg))
    if not ok: fails.append(msg)
def head(n,t): print('\n'+'='*72+'\n  [%s]  %s\n'%(n,t)+'='*72)
gM=1.62

head(1,'the quoted energy figure re-derived')
cp=0.84; dT=1000.0
E_kwh=1000*cp*dT/3600
print('    1 t x 0.84 kJ/(kg K) x 1000 K = %.0f MJ = %.1f kWh (the source says at least 233 kWh; it assumed a 1000 K rise)'%(1000*cp*dT/1e3,E_kwh))
check(abs(E_kwh-233.3)<0.1,'233 kWh per tonne to raise 1 t by 1000 K')

head(2,'an ILLUSTRATIVE hangar: half-cylinder vault, span 20 m, length 50 m, shell 0.5 m  [ASSUMED]')
r=10.0; L=50.0; t=0.5; rho=2000.0
A=math.pi*r*L; V=A*t; M=V*rho
print('    shell area pi r L = %.0f m2 ; volume = %.0f m3 ; mass at 2000 kg/m3 = %.0f t'%(A,V,M/1e3))
check(abs(A-1570.8)<0.1,'shell area 1571 m2')
print('    if sintered end to end: %.0f MWh (233 kWh/t is a ceiling for full heating, not a printer figure) ; over one year = %.0f kW average'%(M/1e3*E_kwh/1e3,M/1e3*E_kwh/8766))
K0,K1=5.09,6.66
print('    if launched instead: %.0f t on the surface = %.0f-%.0f t in Earth orbit'%(M/1e3,M/1e3*K0,M/1e3*K1))
Mbot=2000.0
print('    a printer-and-power system of an assumed %.0f kg = %.0f-%.0f t in orbit: payback ratio (hangar mass / bot mass) = %.0f : 1'%(Mbot,Mbot/1e3*K0,Mbot/1e3*K1,M/Mbot))
check(M/Mbot>500,'the local build pays back its delivery mass by a factor above 500')

head(3,'time: excavation by RASSOR-class robots (66 kg dry, 80 kg payload per trip)  [trip time and duty ASSUMED]')
trips=M/80.0
for trip_h,duty,fleet in ((1.0,0.5,10),(1.0,0.5,50),(2.0,0.5,50)):
    hours=trips*trip_h/(duty*fleet)
    print('    trips needed = %.0f ; trip %.1f h, duty %.0f%% (day only), fleet %d -> %.0f h = %.2f years'%(trips,trip_h,100*duty,fleet,hours,hours/8766))
check(abs(trips-19635)<1,'about 19,635 trips of 80 kg')
print('    the excavator fleet is 10-50 x 66 kg = %.1f-%.1f t: small against the shell it builds.'%(10*66/1e3,50*66/1e3))

head(4,'is self-weight the binding load on a compression vault?  sigma ~ rho g r  [MODEL, order of magnitude, ignores bending and thermal]')
sig_m=rho*gM*r; sig_e=rho*9.80665*r
print('    Moon: rho g r = %.3f MPa ; Earth: %.3f MPa'%(sig_m/1e6,sig_e/1e6))
for name,lo in (('regolith bagging (2-3 MPa)',2.0),('microwave sintering (12.6-37 MPa)',12.6),('direct sintering (84.6-218.8 MPa)',84.6)):
    print('      %-36s lower bound %.1f MPa -> margin over self-weight x %.0f'%(name,lo,lo*1e6/sig_m))
check(sig_m/1e6<0.05,'self-weight stress about 0.03 MPa on the Moon')
print('    self-weight is not the constraint: the margin is 60-2600x. The binding loads are the 254 K thermal swing, impacts, and tension (sintered tensile 7.2-8.2 MPa; bags have little).')

head(5,'what can be made locally and what must be shipped')
print('    shell mass can come from the site; actuators, motors, electronics, belts, power hardware cannot be made from regolith (no source read for that either way).')
print('    if the structure is local, the delivered mass is mostly actuators and electronics, so a per-joint gain g acts on a larger share of what must be launched.')
print('\n'+('FAIL: %d'%len(fails) if fails else 'all checks passed')); sys.exit(1 if fails else 0)
