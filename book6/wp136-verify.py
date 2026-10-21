#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""wp136-verify.py -- companion to book6/wp136-living-in-a-moon-habitat.html. Written 2026-10-21 (R6, R24: run BEFORE the page's sentences).
RECOMPUTED: length of the lunar day; axial room modes f = n c / 2L; speed of sound vs pressure and gas mix; what '10 dB' means as a ratio;
the night-watch fraction under a rotation with a 3-night cap (and the fixed-night control); per-person volume and crew-days for a 4-person station;
cost-per-minute and cost-per-day arithmetic on the prices a secondary source lists.
QUOTED, NOT CHECKED (no source file in the repo; read once by fetch on 2026-10-21): the NASA acoustics technical brief limits (NC-40 sleep quarters for missions
over 30 days, NC-50 work areas, tones 10 dB below the octave band, alarms under 95 dBA, intermittent noise within 10 dB of background in sleep periods),
the Haven-1 figures (45 m3, 4 crew, no on-board bathroom, durations), and the operator prices (aggregator page, not operator pages).
NOT A SOURCE FOR: any health effect. Nothing here measures sleep, mood or stress."""
import math, os, sys
fails=[]
def check(ok,msg):
    print('    %s  %s'%('PASS' if ok else 'FAIL',msg))
    if not ok: fails.append(msg)
def head(n,t): print('\n'+'='*72+'\n  [%s]  %s\n'%(n,t)+'='*72)
R=8.314462618

head(1,'the lunar day (synodic month) against the 24-hour day')
SYN=29.530588
print('    synodic month %.6f d; light half %.3f d; dark half %.3f d'%(SYN,SYN/2,SYN/2))
check(abs(SYN/2-14.765)<0.001,'half a lunar day is about 14.77 Earth days')
check(abs(SYN*24-708.7)<0.1,'one lunar day is about 708.7 hours, i.e. %.2f cycles of 24 h'%(SYN))
print('    so any 24-hour cycle in a habitat is supplied by the habitat, not by the sky')

head(2,'axial room modes: f_n = n c / (2 L), c = 343.2 m/s at 20 C in air (the 20 C is an assumption of this page)')
c20=331.3*math.sqrt(1+20/273.15)
print('    c(20 C, air) = %.1f m/s'%c20)
check(abs(c20-343.2)<0.3,'c at 20 C is about 343 m/s')
for L in (5,10,15):
    fs=[n*c20/(2*L) for n in (1,2,3)]
    print('    L = %2d m : f1 = %.1f Hz, f2 = %.1f, f3 = %.1f'%(L,*fs))
check(abs(c20/(2*10)-17.2)<0.1,'a 10 m axial mode is 17.2 Hz')
check(c20/(2*10)<20,'that mode is below 20 Hz (the nominal lower edge of hearing); this says nothing about how it is perceived')

head(3,'sound speed and acoustic impedance against total pressure, and against gas mix (ideal gas, 293.15 K)')
T=293.15
def c_ideal(gamma,M): return math.sqrt(gamma*R*T/M)
cair=c_ideal(1.4,0.02897)
print('    air: c = %.1f m/s at ANY pressure (c = sqrt(gamma R T / M) has no p in it)'%cair)
rho0=101325*0.02897/(R*T)
for p in (101.325,70.3,55.2):   # kPa: sea level, and two ILLUSTRATIVE reduced pressures (not a NASA spec checked here)
    rho=p*1000*0.02897/(R*T); Z=rho*cair
    print('    p = %6.1f kPa : rho = %.3f kg/m3, rho*c = %.1f Pa s/m  (%.0f%% of sea level)'%(p,rho,Z,100*rho/rho0))
check(abs((70.3*1000*0.02897/(R*T)*cair)/(rho0*cair)-70.3/101.325)<1e-9,'impedance rho*c scales linearly with pressure at fixed gas and temperature')
xO2,xHe=0.21,0.79
Cv=(xO2*2.5+xHe*1.5)*R; Cp=Cv+R; g=Cp/Cv; M=xO2*0.032+xHe*0.004
che=c_ideal(g,M)
print('    21%% O2 / 79%% He: gamma = %.3f, M = %.5f kg/mol, c = %.0f m/s (%.2fx air)'%(g,M,che,che/cair))
check(abs(che/cair-1.82)<0.01,'a 21/79 O2/He mix has c = 1.82x air (first guess of >2.5x was wrong; the run says 1.82x); every mode frequency scales by that factor')
check(abs((1*che/(2*10))/(1*cair/(2*10))-che/cair)<1e-9 and abs(che/(2*10)-17.2*che/c20)<0.2,'mode frequencies scale linearly with c at fixed L: the 10 m first mode in the mix is %.1f Hz'%(che/(2*10)))

head(4,'what 10 dB is: a factor of 10 in power, 3.16 in pressure amplitude')
print('    10 dB -> power x %.1f, pressure x %.3f'%(10**(10/10),10**(10/20)))
check(abs(10**(10/20)-3.1623)<1e-3,'10 dB = 3.16x pressure amplitude')
check(abs(10**(10/10)-10)<1e-12,'10 dB = 10x power')
print('    so "a tone 10 dB below its octave band" and "intermittent noise within 10 dB of background" are 10x-in-power statements')

head(5,'the night watch: one person awake every night, nights on watch per person under a rotation (the 3-night cap is the AUTHOR\'S HYPOTHESIS, not a finding)')
def schedule(N,block=3,days=None):
    days=days or block*N*2
    return [ (d//block)%N for d in range(days) ]
for N in (3,4,5,6):
    s=schedule(N); share=[s.count(i)/len(s) for i in range(N)]
    run=1; mx=1
    for a,b in zip(s,s[1:]):
        run=run+1 if a==b else 1; mx=max(mx,run)
    print('    crew %d: every person on watch %.1f%% of nights, longest run %d nights, every night covered by exactly one person: %s'%(N,100*share[0],mx,all(0<=x<N for x in s)))
    check(max(share)-min(share)<1e-12 and abs(share[0]-1/N)<1e-12,'crew %d: equal share = 1/%d'%(N,N))
    check(mx<=3,'crew %d: no run longer than 3 nights'%N)
fixed=[0]*60
check(fixed.count(0)/len(fixed)==1.0,'CONTROL: a fixed night watch puts one person on 100%% of nights (and the other N-1 on 0%%)')
print('    the trade-off in numbers: with 4 crew, rotation puts %.0f%% of nights on each person; fixed puts 100%% on one and 0%% on three' % (100*schedule(4).count(0)/len(schedule(4))))
print('    on-call model (sleep normally, woken only by a real alarm): 0% of nights shifted; the cost is a waking event, not a schedule shift')

head(6,'Haven-1 as quoted (planned, not achieved): 45 m3, 4 crew')
V,crew=45,4
pp=V/crew; side=pp**(1/3)
print('    %.2f m3 per person = a cube %.2f m on a side'%(pp,side))
check(abs(pp-11.25)<1e-9,'45 / 4 = 11.25 m3 per person')
check(abs(side-2.24)<0.01,'11.25 m3 is a cube 2.24 m on a side')
for d in (10,14,30):
    print('    %2d days x 4 crew = %3d crew-days'%(d,d*crew))
print('    the quoted durations disagree on the source page (30 days / 10-30 days / typically two weeks); this script does not resolve that')

head(7,'prices as an aggregator page lists them (NOT operator pages): arithmetic only')
ns_min=11; ns_lo,ns_hi=150e3,450e3
print('    New Shepard ~%d min at $%.0fk-$%.0fk: $%.1fk-$%.1fk per minute'%(ns_min,ns_lo/1e3,ns_hi/1e3,ns_lo/ns_min/1e3,ns_hi/ns_min/1e3))
ax=55e6
print('    Axiom ~$55M for 10-14 days: $%.2fM-$%.2fM per day'%(ax/14/1e6,ax/10/1e6))
check(abs(ax/14/1e6-3.93)<0.01 and abs(ax/10/1e6-5.5)<0.01,'$55M / 14 d = $3.93M per day; / 10 d = $5.5M per day')
check(abs(ns_lo/ns_min/1e3-13.6)<0.1 and abs(ns_hi/ns_min/1e3-40.9)<0.1,'$150k/11 = $13.6k, $450k/11 = $40.9k per minute')

head(9,'the retreat, the practice and the load: closet mass, jump scaling, practice hours, tempo (the section added 2026-10-21)')
VOLF=133.1   # kg per m3, lunar-surface ESM volume factor QUOTED from ICES-2026-160 Table 2 (read in an earlier session; not re-read here)
for v_ in (1,2):
    print('    a %d m3 private room: %.0f kg equivalent system mass at that factor (volume only)'%(v_,v_*VOLF))
check(abs(1*VOLF-133.1)<1e-9 and abs(2*VOLF-266.2)<1e-9,'1 m3 = 133.1 kg, 2 m3 = 266.2 kg at 133.1 kg/m3')
g_e,g_m=9.80665,1.62
v0=3.0   # takeoff speed, m/s: an ILLUSTRATIVE number chosen here, not a measurement
he,hm=v0**2/(2*g_e),v0**2/(2*g_m)
te,tm=2*v0/g_e,2*v0/g_m
print('    takeoff %.1f m/s: height %.2f m on Earth, %.2f m on the Moon; flight time %.2f s vs %.2f s'%(v0,he,hm,te,tm))
check(abs(he-0.459)<0.001 and abs(hm-2.778)<0.001,'height 0.459 m on Earth, 2.778 m at g = 1.62')
check(abs(hm/he-g_e/g_m)<1e-9 and abs(tm/te-g_e/g_m)<1e-9,'height and flight time both scale by g_Earth/g_Moon = %.2f'%(g_e/g_m))
d_=2*15/60*6/7*180
print('    2 x 15 min a day, 6 days in 7, 180 days = %.1f h per person; %.1f crew-hours for four'%(d_,4*d_))
check(abs(d_-77.14)<0.01,'2 x 15 min x 6/7 x 180 = 77.1 h per person')
step=60/(104*2)
print('    atabaque 12-step cycle at 104 BPM, 2 steps per beat: step %.4f s, cycle %.2f s'%(step,12*step))
check(abs(step-0.2885)<0.0005 and abs(12*step-3.462)<0.005,'step 0.2885 s, cycle 3.46 s')
D2=440*2**(-31/12)   # D2 is 31 semitones below A4 (D4 is 7 below; D2 is two octaves, 24, lower). First try used 33 and gave C2 = 65.41 Hz; the check caught it
print('    D2 = %.2f Hz (A4 = 440 Hz, equal temperament)'%D2)
check(abs(D2-73.42)<0.01,'D2 = 73.42 Hz')

head(8,'the page carries these numbers (SKIP if the page is absent)')
page=os.path.join(os.path.dirname(os.path.abspath(__file__)),'wp136-living-in-a-moon-habitat.html')
if os.path.exists(page):
    h=open(page,encoding='utf8').read()
    for s in ('14.77','17.2','11.25','2.24','3.16','25%','13.6','40.9','3.93','133.1','2.78','77.1','3.46','73.42'):
        check(s in h,'page contains %s'%s)
else:
    print('    SKIP  page not written yet')

head('HONESTY','what this script establishes and what it does not')
print("""    It recomputes arithmetic: the lunar day, room-mode frequencies for assumed lengths, the pressure and gas-mix dependence of sound speed and
    impedance under the ideal-gas model, the dB ratios, the watch-share arithmetic under a stated rotation rule, and per-person volume and unit
    prices from figures quoted elsewhere. It checks a control (the fixed night watch) against the rotation.
    It does NOT establish that any sound, light, smell, touch, plant, animal or schedule improves sleep, mood or allostatic load; nothing here
    measures a person. The NASA limits, the Haven-1 figures and the prices are quotations read once by fetch from secondary or summary pages on
    2026-10-21, not checked against NASA-STD-3001, Vast or the operators. The 3-night cap and the shared-time rules are the author's design hypotheses.
    Block 9 recomputes closet mass at a quoted factor, jump scaling at an illustrative takeoff speed, practice hours and the machine's tempo. It does not
    show that any practice loads bone, relieves back pain or lowers sick leave; the sick-leave figure and the Brasilia law are not sourced.""")
if fails:
    print('\nFAILED: %d'%len(fails)); [print('  -',f) for f in fails]; sys.exit(1)
print('\nAll checks passed.')
