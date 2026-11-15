#!/usr/bin/env python3
"""wp58_audit_check.py -- read-only independent check of the r*(eps) table in WP58 (audit 2026-11-15).
Bisection on the dm3 ODE r' = r(1-r^2)+eps(r-1)e^-z, z' = r^2-eps(r-1)^2 e^-z from z0 = 0 (DOP853, rtol 1e-12, 45 bisection steps, so
accuracy is limited to about 1e-9 by the convergence test, not 1e-10). Compares with the values printed on the page.
Not checked: the galactic identification eps_gal = nu/kappa (MODEL), the kappa, nu values (unsourced), the 2:1 resonance (not derived here)."""
import re, os, sys
import numpy as np
from scipy.integrate import solve_ivp
def f(t, y, e):
    r, z = y
    return [r*(1-r*r)+e*(r-1)*np.exp(-z), r*r-e*(r-1)**2*np.exp(-z)]
def conv(r0, e, T=400):
    def mk(fn):
        fn.terminal = True; return fn
    evs = [mk(lambda t, y, e: y[0]-1e-3), mk(lambda t, y, e: abs(y[0]-1)-1e-7), mk(lambda t, y, e: y[1]-60), mk(lambda t, y, e: y[1]+60)]
    s = solve_ivp(f, [0, T], [r0, 0.0], args=(e,), method='DOP853', rtol=1e-12, atol=1e-14, events=evs)
    if s.t_events[1].size: return True
    if any(x.size for i, x in enumerate(s.t_events) if i != 1): return False
    return abs(s.y[0, -1]-1) < 1e-4
def rstar(e):
    lo, hi = 0.05, 0.99
    for _ in range(45):
        m = (lo+hi)/2
        if conv(m, e): hi = m
        else: lo = m
    return hi
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, 'wp58-galactic-fold.html'), encoding='utf-8', errors='replace').read()
page = {0.5: 0.3779748572, 1.0: 0.5722354585, 1.5: 0.6931303713, 2.5: 0.8353301711, 3.0: 0.8789150842, 4.0: 0.9352791770}
bad = 0
def ck(n, ok):
    global bad; bad += (not ok); print(('PASS ' if ok else 'FAIL ') + n)
for e, v in page.items():
    ck('printed value %.10f present on the page' % v, ('%.10f' % v) in src)
    got = rstar(e); ck('eps=%s: independent r* = %.10f agrees with page to 5e-9 (diff %.1e)' % (e, got, abs(got-v)), abs(got-v) < 5e-9)
got2 = rstar(2.0); ck('eps=2: r* = %.10f vs 0.77594058 (diff %.1e)' % (got2, abs(got2-0.77594058)), abs(got2-0.77594058) < 5e-9)
for k, n, v in [(155.6, 177, 0.611), (88.9, 143, 0.714), (62.2, 115, 0.754), (37.9, 73, 0.765)]:
    e = n/k; got = rstar(e); ck('galactic row nu/kappa=%.4f: r* = %.4f agrees with page %.3f' % (e, got, v), abs(got-v) < 6e-4)
ln2 = float(np.log(2)); d = abs(rstar(1.5)-ln2)
ck('r*(1.5) differs from ln 2 by %.2e, far above the numerical error ~1e-9: NOT equal' % d, d > 1e-6)
for e0, r in [(1.138, 0.610), (1.607, 0.713), (1.853, 0.755), (1.924, 0.765)]:
    pass
ck('R* = r* x 3.5 kpc for the rows: 0.611x3.5=2.14, 0.714x3.5=2.50, 0.754x3.5=2.64, 0.765x3.5=2.68', all(abs(a*3.5-b) < 0.006 for a, b in [(0.611, 2.14), (0.714, 2.50), (0.754, 2.64), (0.765, 2.68)]))
print('NOTE hand argument, not computed: kappa, nu at 2.0/3.5/5.0/8.2 kpc are unsourced; the identification eps_gal = nu/kappa is a MODEL (page says so); "2:1 vertical resonance" is not derived here.')
print('NOTE: certify_rstar.py is described on the page with bisection tolerance 1e-7; figures past the 7th decimal are not backed by that script (this script reproduces them to ~5e-9).')
sys.exit(1 if bad else 0)
