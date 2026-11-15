#!/usr/bin/env python3
"""
ch10_rstar_rigorous_check.py  (added 2026-11-14, book4 audit, rule R29)

Why certify_rstar_rigorous.py is NOT a certificate. It runs the script's own
fixed-step RK4 centre trajectory (rk4_step_center_mp) at step dt and at dt/2 from
the same start, and compares the two. The script's reported error radius at
decision time is printed beside it. A rigorous radius cannot be smaller than the
method's own discretisation error.

Read-only: imports the original script, does not modify it.
Usage: python3 ch10_rstar_rigorous_check.py        (about 1-2 minutes)
"""
import importlib.util, os, mpmath as mp
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('crr', os.path.join(HERE, 'certify_rstar_rigorous.py'))
crr = importlib.util.module_from_spec(spec); spec.loader.exec_module(crr)

R0 = '0.7759405754'

def centre(dt, T):
    r, z, d = mp.mpf(R0), mp.mpf(0), mp.mpf(dt)
    for _ in range(int(round(T / dt))): r, z = crr.rk4_step_center_mp(r, z, d)
    return r, z

print('Centre trajectory from r0=%s, z0=0, RK4 at dt=5e-4 versus dt=2.5e-4' % R0)
worst = 0.0
for T in (2, 6):
    a, b = centre(0.0005, T), centre(0.00025, T)
    e = max(float(abs(a[0] - b[0])), float(abs(a[1] - b[1]))); worst = max(worst, e)
    print('  T=%d   max(|dr|,|dz|) between step sizes = %.3e' % (T, e))
res, t, rad = crr.classify_rigorous(R0)
print('Script classification of r0=%s: %s at t=%.3f, its reported error radius (max over run) = %.3e' % (R0, res, t, float(rad)))
ok = float(rad) < worst
print('Reported radius is SMALLER than the measured step-size error: %s' % ('YES -> the radius is not a valid enclosure' if ok else 'no'))
raise SystemExit(0 if ok else 1)
