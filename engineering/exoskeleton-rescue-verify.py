#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""exoskeleton-rescue-verify.py -- companion to engineering/beltdraulic-paper.html section 9 (suit walks the wearer back).
Written 2026-09-30 (R24). QUOTED (sources on the page): NASA lunar rescue requirement: one crew member transports a suited,
fully incapacitated crew member (343 kg) up to 2 km and 20 degrees without a rover; EMU joints near neutral stability at
4.3 psid (29.6 kPa); metabolic rates, lunar surface EVA 490-2607 kJ/h, advanced walkback test 1675-3167 kJ/h.
ASSUMED (not data, marked on the page): cost of transport c_t, drive efficiency, battery specific energy, walking speed,
limb geometry. Nothing here is a design; it asks whether energy or torque is the binding constraint."""
import math, sys
fails=[]
def check(ok,msg):
    print('    %s  %s'%('PASS' if ok else 'FAIL',msg))
    if not ok: fails.append(msg)
def head(n,t): print('\n'+'='*72+'\n  [%s]  %s\n'%(n,t)+'='*72)
gM=1.62; m=343.0; d=2000.0; th=math.radians(20)

head(1,'the load: 343 kg suited, incapacitated, on the Moon')
W=m*gM
print('    weight on the Moon = %.1f N (= %.0f kg-force on Earth); Earth weight of an 80 kg person = %.1f N'%(W,W/9.80665,80*9.80665))
check(abs(W-555.66)<0.01,'weight 555.7 N')
print('    so the lunar weight of the whole suited load (%.0f N) is %.0f%% of an unsuited 80 kg person on Earth'%(W,100*W/(80*9.80665)))

head(2,'energy: climbing 2 km at 20 degrees is the worst case in the requirement')
h=d*math.sin(th); Epe=m*gM*h
print('    height gained = %.1f m ; potential energy m g h = %.0f kJ = %.1f Wh'%(h,Epe/1e3,Epe/3600))
check(abs(Epe-380.1e3)<0.5e3,'climb energy about 380 kJ')
print('    flat-ground gait cost E = c_t * m g d, c_t = dimensionless cost of transport (ASSUMED values):')
eta=0.7; spec=200.0   # ASSUMED: drive eta, battery Wh/kg
print('      c_t    mech energy (kJ)   + climb 380 kJ, /eta=%.1f (kJ)   Wh    battery kg at %.0f Wh/kg'%(eta,spec))
rows=[]
for ct in (0.1,0.3,1.0):
    Ef=ct*m*gM*d
    Et=(Ef+Epe)/eta
    rows.append((ct,Ef,Et))
    print('      %.1f    %10.0f          %14.0f              %5.0f   %6.2f'%(ct,Ef/1e3,Et/1e3,Et/3600,Et/3600/spec))
check(all(r[2]/3600/spec<10 for r in rows),'in all three cases the battery for the walk is under 10 kg at 200 Wh/kg')
print('    compare: the quoted human metabolic rate for the advanced walkback test is 1675-3167 kJ/h; at 1 m/s a 2 km walk takes %.2f h,'%(d/1.0/3600))
print('    i.e. about %.0f-%.0f kJ of METABOLIC energy (a human at ~20-25%% efficiency; not comparable one-to-one with electrical energy).'%(1675*(d/1.0/3600),3167*(d/1.0/3600)))
print('    energy is a battery-mass question of a few kilograms, not the binding constraint.')

head(3,'torque: what the legs must supply (first-order scaling of the quoted 2.4/1.5/1.9 Nm/kg ceilings)')
Wh=80*9.80665
for j,nm in (('hip',2.4),('knee',1.5),('ankle',1.9)):
    T_e=nm*80; T_m=T_e*W/Wh
    print('    %-5s Earth ceiling for 80 kg = %5.0f Nm ; scaled by weight to the Moon load (%.0f N): %5.0f Nm'%(j,T_e,W,T_m))
check(abs(2.4*80*W/Wh-136.1)<0.5,'hip about 136 Nm at lunar weight 556 N (proportional scaling, same proportions)')
print('    first-order only: assumes torque proportional to weight with human proportions; inertia during swing and a 20 degree slope add to it.')

head(4,'the "barrier": pressure loads in the suit  [MODEL, geometry ASSUMED]')
psi=6894.757; P=4.3*psi
print('    4.3 psid = %.2f kPa (source: 29.6 kPa)'%(P/1e3))
check(abs(P/1e3-29.65)<0.05,'4.3 psid is 29.6 kPa')
for D in (0.05,0.10):
    A=math.pi*D*D/4
    print('    an end-cap of diameter %.2f m carries a pressure force P*A = %.0f N (= %.0f kgf); the restraint layer must react it, and a joint that is not at neutral stability adds a restoring torque'%(D,P*A,P*A/9.80665))
print('    The EMU is designed for near-neutral stability at 4.3 psid, so the resisting torque is the residual, not P*A; the sources give no residual torque value.')

print('\n'+('FAIL: %d'%len(fails) if fails else 'all checks passed')); sys.exit(1 if fails else 0)
