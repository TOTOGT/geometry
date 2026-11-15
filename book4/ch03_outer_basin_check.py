#!/usr/bin/env python3
"""
ch03_outer_basin_check.py  (added 2026-11-14, book4 audit, rule R29)

Produces the numbers Chapter 3 quotes for Theorem 3.2, with an ADAPTIVE integrator
(scipy DOP853, rtol 1e-13, atol 1e-15). It is a numerical check, not a proof.

System (3.1):  r' = r(1-r^2) + 2(r-1)e^{-z},   z' = r^2 - 2(r-1)^2 e^{-z}   (theta' = 1 decouples)

Checks (all numerical; none is a proof):
  1. at z(0)=0 an ESTIMATE of the largest r(0) for which convergence to r=1 is observed (bisection) -> about 6.859221
  2. at z(0)=0 an estimate of the inner boundary r* between "convergence observed" and not          -> about 0.77594058
  3. named starts for which convergence is NOT OBSERVED during the tested interval (t <= 80); each is
     classified: bad region reached, solver stopped early, or interval exhausted. This is evidence
     against "every r(0)>1 converges", not a proof that those orbits never converge (no analytic
     argument or validated bound is used here).
  4. named starts for which convergence IS observed
"Observed" means |r-1| < 1e-9 was reached before any stopping condition, at the stated tolerances.
Why not ch10-outer-basin-check.py's 6.8963: that script uses fixed-step RK4 at dt=0.01,
too coarse where r' ~ -r^3 (r near 7); the adaptive result above is 6.859221.
Usage: python3 ch03_outer_basin_check.py   (a few seconds)
"""
import sys
import numpy as np
from scipy.integrate import solve_ivp

def f(t, y):
    r, z = y; e = np.exp(-z)
    return [r * (1 - r * r) + 2 * (r - 1) * e, r * r - 2 * (r - 1) ** 2 * e]

def outcome(r0, z0=0.0, T=80.0):
    """Returns (observed, label). observed is True only if |r-1| < 1e-9 is reached before the stopping conditions."""
    ev = lambda t, y: abs(y[0] - 1) - 1e-9
    ev.terminal = True
    bad = lambda t, y: (1.0 if (y[1] < -40 or y[0] > 1e4 or y[0] < 1e-6) else 0.0) - 0.5
    bad.terminal = True
    s = solve_ivp(f, [0, T], [r0, z0], method='DOP853', rtol=1e-13, atol=1e-15, events=[ev, bad])
    if len(s.t_events[0]) > 0 and len(s.t_events[1]) == 0: return True, 'convergence observed'
    if len(s.t_events[1]) > 0: return False, 'bad region reached (z<-40, r>1e4 or r<1e-6) at t=%.4g' % s.t_events[1][0]
    if s.status == -1: return False, 'solver stopped early at t=%.4g (%s)' % (s.t[-1], s.message)
    return False, 'interval t<=%g exhausted without |r-1|<1e-9' % T

def converges(r0, z0=0.0, T=80.0):
    return outcome(r0, z0, T)[0]

def bisect(lo, hi, lo_val, n=60):
    assert converges(lo) == lo_val and converges(hi) != lo_val
    for _ in range(n):
        m = (lo + hi) / 2
        if converges(m) == lo_val: lo = m
        else: hi = m
    return lo

ok = True
outer = bisect(3.0, 12.0, True)
print('1. estimated largest r(0) with convergence observed at z(0)=0 (DOP853 rtol 1e-13, atol 1e-15, t<=80): %.8f' % outer); ok &= abs(outer - 6.859221) < 1e-5
inner = bisect(0.5, 0.95, False)   # largest r0 that does NOT converge, i.e. r* from below
print('2. estimated inner boundary r* at z(0)=0 (largest r(0) with convergence not observed): %.8f' % inner); ok &= abs(inner - 0.77594058) < 1e-7
for p in [(8, 0), (10, 0), (1.5, -2), (2, -1), (1.001, -3)]:
    c, why = outcome(*p); print('3. start (r0, z0)=%s: convergence not observed -> %s' % (p, why) if not c else '3. start %s: UNEXPECTEDLY observed' % (p,)); ok &= (not c)
for p in [(1.5, 0), (3, 0), (5, 0), (0.9, 0)]:
    c, why = outcome(*p); print('4. start (r0, z0)=%s: %s' % (p, why)); ok &= c
print('ALL CHECKS PASSED' if ok else 'CHECK FAILED'); sys.exit(0 if ok else 1)
