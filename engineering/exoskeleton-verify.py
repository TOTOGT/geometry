#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""exoskeleton-verify.py -- first pass for engineering/beltdraulic-paper.html section 9 (exoskeleton in space).
Written 2026-09-30 (R24). QUOTED inputs (sources on the page): NASA X1: 10 degrees of freedom, four motorized (hips and knees),
six passive, 'under 60 lbs'; Frontiers Robot. AI 2020 (10.3389/frobt.2020.00013): recommended maximum moments for daily life,
2.4 Nm/kg hip, 1.5 Nm/kg knee, 1.9 Nm/kg ankle. ASSUMED (not data): wearer mass 80 kg; the self-feeding fraction kappa.
Everything else is arithmetic on the joint-compounding model of joint-compounding-verify.py."""
import sys, math
fails=[]
def check(ok,msg):
    print('    %s  %s'%('PASS' if ok else 'FAIL',msg))
    if not ok: fails.append(msg)
def head(n,t): print('\n'+'='*72+'\n  [%s]  %s\n'%(n,t)+'='*72)

head(1,'the X1 as a load-path chain, and the torque it must supply (quoted per-kg maxima x ASSUMED 80 kg wearer)')
lb=0.45359237; m_x1=60*lb
print('    X1: 4 motorized + 6 passive = 10 DOF; "under 60 lbs" = under %.1f kg'%m_x1)
check(4+6==10,'4 motorized + 6 passive = 10 degrees of freedom')
W=80.0
for j,nm in (('hip',2.4),('knee',1.5),('ankle',1.9)):
    print('    %-5s %.1f Nm/kg x %.0f kg = %5.0f Nm  (a capability ceiling for daily life, not a walking average)'%(j,nm,W,nm*W))
print('    powered load-path depth per leg on the X1: 2 (hip, knee)')

head(2,'gravity: the gravitational part of the joint torque scales with local g; the inertial part does not  [first-order MODEL]')
g0=9.80665
for nm,g in (('Earth',9.80665),('Mars',3.71),('Moon',1.62),('microgravity',0.0)):
    print('    %-13s g = %5.2f m/s^2 -> gravitational torque x %.3f of Earth'%(nm,g,g/g0))
print('    Moon = %.3f of Earth (about 1/6); in microgravity the wearer has no weight to support, and the torque left is inertial (limb acceleration) and exercise/suit loads.'%(1.62/g0))
check(abs(1.62/g0-0.165)<5e-4,'Moon gravity is 0.165 of Earth')

head(3,'does per-joint compounding matter at this depth?  R(n) = ((1+a)^n-1)/((1+a/g)^n-1), a=0.05, g=2')
for n in (2,3,4,7):
    R=((1.05)**n-1)/((1.025)**n-1)
    print('    depth n=%d: R = %.3f (g = 2)'%(n,R))
R2=(1.05**2-1)/(1.025**2-1)
check(2.0<R2<2.1,'at depth 2 (X1 leg) R = %.3f, essentially g: per-joint compounding is negligible for a leg exoskeleton'%R2)
print('    so the "hundreds of joints" compounding does not apply to a leg exoskeleton; it belongs to deep or serial structures (hands, snakes, cable chains).')

head(4,'a loop that DOES compound at shallow depth: carried mass feeds itself (battery <- energy <- mass)  [MODEL, kappa ASSUMED]')
print('    total mass M = M0 + kappa*M  =>  M = M0/(1-kappa),  kappa = fraction of M that is added to carry M (battery+actuators sized by the load they add)')
print('    improving efficiency by g divides kappa by g:  M_before/M_after = (1 - kappa/g)/(1 - kappa)')
print('      kappa    g=2      g=3      g=5')
for k in (0.3,0.5,0.7,0.9,0.95):
    print('      %.2f   %6.2f   %6.2f   %6.2f'%((k,)+tuple((1-k/g)/(1-k) for g in (2,3,5))))
check(abs((1-0.95/2)/(1-0.95)-10.5)<1e-9,'kappa=0.95, g=2 gives 10.5: a 10x gain needs a baseline within 5% of runaway')
print('    a 10x-20x mass gain from a 2x-3x efficiency gain exists only if the baseline is nearly self-defeating (kappa >= ~0.9); for kappa=0.5 the gain is under 2 even at g=5')
check((1-0.5/5)/(1-0.5)<2.0,'kappa=0.5, g=5 gives %.2f (< 2)'%((1-0.5/5)/(1-0.5)))
print('\n'+('FAIL: %d'%len(fails) if fails else 'all checks passed')); sys.exit(1 if fails else 0)
