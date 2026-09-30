#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""moonbase-warehouse-verify.py -- companion to engineering/beltdraulic-paper.html section 10 (moonbase distribution warehouse).
Written 2026-09-30 (R24). QUOTED (sources on the page): TLI 3.05-3.25 km/s (Apollo, J-2); Apollo LM powered descent 5925 ft/s
(1.806 km/s), landing budget 7050 ft/s (2.150 km/s); lunar equator +121 C day, -133 C night; polar shadowed craters below -246 C
(NASA). ASSUMED / NOT READ: Isp values, LOI delta-v about 0.9 km/s (not read), stage inert fractions, alpha, warehouse actuator mass.
The warehouse SIZE is not known: results are per tonne and per unit, not a design."""
import math, sys
fails=[]
def check(ok,msg):
    print('    %s  %s'%('PASS' if ok else 'FAIL',msg))
    if not ok: fails.append(msg)
def head(n,t): print('\n'+'='*72+'\n  [%s]  %s\n'%(n,t)+'='*72)
g0=9.80665; ft=0.3048

head(1,'what one kilogram delivered to the lunar surface costs in Earth-orbit mass  [lower bounds; Isp and inert fractions ASSUMED]')
dv_tli=3.15; dv_loi=0.9; dv_desc=5925*ft/1000
print('    TLI %.2f km/s (quoted 3.05-3.25) ; LOI %.2f km/s (NOT READ, assumed ~0.9) ; powered descent %.3f km/s (quoted 5925 ft/s)'%(dv_tli,dv_loi,dv_desc))
check(abs(5925*ft/1000-1.806)<1e-3,'5925 ft/s = 1.806 km/s')
def ratio(dv,isp,f):
    ve=isp*g0/1000; R=math.exp(dv/ve)
    payload_frac=1/R - f*(1-1/R)
    return 1/payload_frac
for f in (0.0,0.1):
    a=ratio(dv_tli,420,f); b=ratio(dv_loi+dv_desc,320,f)
    print('    inert fraction f=%.1f of propellant: TLI stage (Isp 420 s) x%.2f ; LOI+descent (Isp 320 s) x%.2f ; LEO mass per kg on the surface = %.2f kg'%(f,a,b,a*b))
K0=ratio(dv_tli,420,0)*ratio(dv_loi+dv_desc,320,0); K1=ratio(dv_tli,420,0.1)*ratio(dv_loi+dv_desc,320,0.1)
check(5.0<K0<5.2 and 6.5<K1<6.8,'about 5.1 kg (propellant only) to 6.6 kg (10%% inert) in LEO per kg landed: K = %.2f to %.2f'%(K0,K1))
print('    the multiplier is a product over stages of exp(dv/ve): exponential in delta-v, the rocket-equation form of compounding.')

head(2,'a per-actuator gain g on a load path of depth n, priced in Earth-orbit mass  (alpha=0.05 Earth-referenced, g=2)')
def R(n,a,g): return ((1+a)**n-1)/((1+a/g)**n-1)
print('      depth n   surface mass ratio R   per tonne of actuator mass saved at the surface -> LEO tonnes saved (K=%.1f..%.1f)'%(K0,K1))
for n in (2,7,30,100):
    r=R(n,0.05,2)
    print('      %5d     %8.2f              1 t on the surface before => %.2f t after: saves %.2f t there, %.1f-%.1f t in LEO'%(n,r,1/r,1-1/r,(1-1/r)*K0,(1-1/r)*K1))
print('    The launch multiplier does not change R; it scales every tonne saved by K. Depth changes R.')

head(3,'the Moon lowers static loads more than dynamic ones: actuator force ~ m (g_local + a)')
print('    ratio of required actuator force Moon/Earth = (1.62 + a)/(9.80665 + a)')
for a_ in (0.0,0.5,1.0,2.0):
    print('      a = %.1f m/s^2: %.3f'%(a_,(1.62+a_)/(g0+a_)))
check(abs((1.62+1.0)/(g0+1.0)-0.2424)<1e-3,'a = 1 m/s^2 gives 0.242, not 1/6 = 0.165')
print('    a warehouse that accelerates loads gets less than the 6x static relief; fast throughput erodes the Moon advantage.')

head(4,'the thermal swing a fluid-free actuator must live in (NASA: +121 C day, -133 C night at the equator; below -246 C in polar shadow)')
print('    equator swing = %d K (121 - (-133)) ; kelvin: %.0f K day, %.0f K night, %.0f K polar shadow'%(121+133,121+273.15,-133+273.15,-246+273.15))
check(121+133==254,'254 K swing at the equator')
print('    the sources give no rated range for any belt or fluid; whether a polyurethane belt survives this swing is UNREAD (a concrete risk).')
print('\n'+('FAIL: %d'%len(fails) if fails else 'all checks passed')); sys.exit(1 if fails else 0)
