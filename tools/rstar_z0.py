#!/usr/bin/env python3
"""rstar_z0.py -- how the inner basin boundary r* of the dm3 toy depends on the initial z(0).  (R12 producing tool, 2026-11-15)

System (eps = 2): r' = r(1-r^2) + eps (r-1) e^-z,  z' = r^2 - eps (r-1)^2 e^-z.
For each z0, bisection on r(0) in [0.05, 0.99] (DOP853, rtol 1e-12, atol 1e-14, 45 steps; a start 'converges' if r reaches |r-1| < 1e-7
before r < 1e-3 or |z| > 60).  Accuracy of the printed r* is limited to about 1e-9 by the bisection and the convergence test.

  python3 tools/rstar_z0.py            prints r*(z0) for z0 = 0, 0.01, 0.05, 0.5 and exits 0 if each is within 5e-6 of the value recorded
                                       in docs/audit-log.md (0.775941, 0.773158, 0.761945, 0.629892) and r*(0) is within 1e-8 of 0.7759405755
It does not say which z0 any other file used; it shows that the figure 0.7732 is what the same system gives at z0 = 0.01.
Needs numpy and scipy.
"""
import sys
import numpy as np
from scipy.integrate import solve_ivp
E = 2.0
def f(t, y):
    r, z = y
    return [r*(1-r*r)+E*(r-1)*np.exp(-z), r*r-E*(r-1)**2*np.exp(-z)]
def conv(r0, z0, T=400):
    def mk(fn):
        fn.terminal = True; return fn
    evs = [mk(lambda t, y: y[0]-1e-3), mk(lambda t, y: abs(y[0]-1)-1e-7), mk(lambda t, y: y[1]-60), mk(lambda t, y: y[1]+60)]
    s = solve_ivp(f, [0, T], [r0, z0], method='DOP853', rtol=1e-12, atol=1e-14, events=evs)
    if s.t_events[1].size: return True
    if any(x.size for i, x in enumerate(s.t_events) if i != 1): return False
    return abs(s.y[0, -1]-1) < 1e-4
def rstar(z0):
    lo, hi = 0.05, 0.99
    for _ in range(45):
        m = (lo+hi)/2
        if conv(m, z0): hi = m
        else: lo = m
    return hi
if __name__ == '__main__':
    rec = {0.0: 0.775941, 0.01: 0.773158, 0.05: 0.761945, 0.5: 0.629892}
    bad = 0
    for z0, v in rec.items():
        r = rstar(z0); ok = abs(r - v) < 5e-6
        print(('PASS' if ok else 'FAIL'), 'z0=%-5g r*=%.9f  recorded %.6f' % (z0, r, v)); bad += (not ok)
    r0 = rstar(0.0); ok = abs(r0 - 0.7759405755) < 1e-8
    print(('PASS' if ok else 'FAIL'), 'r*(z0=0) = %.10f vs 0.7759405755' % r0); bad += (not ok)
    sys.exit(1 if bad else 0)
