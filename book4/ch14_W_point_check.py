#!/usr/bin/env python3
"""Explicit-point record for the Wronskian W of book4/ch11-ch14 (2026-11-15). Read-only.

Definitions (the pages'): s = sigma + i t;  H(s) = -zeta'(s)/zeta(s) = c - i g,  i.e. c = Re H, g = -Im H.
For sigma > 1, H = sum Lambda(n) n^-s, so c = sum Lambda(n) n^-sigma cos(t log n), g = sum Lambda(n) n^-sigma sin(t log n).
For sigma <= 1 the series do not define c, g (see ch11 audit E9); here c, g are those of the meromorphic continuation of H.
d/dt H(sigma + i t) = i H'(s), so  dc/dt = Re(iH'),  dg/dt = -Im(iH').   W = c dg/dt - g dc/dt.
Route 1: analytic, H' = -(zeta'' zeta - zeta'^2)/zeta^2.   Route 2: central differences of c, g in t (step h).
Route 3: H computed from a numerical derivative of zeta (mp.diff) instead of mpmath's derivative argument.
Stability: working precision 30, 50, 80 digits; h in 1e-3, 1e-5, 1e-7 (precision raised so h does not cancel).
"""
import sys
from mpmath import mp, mpf, mpc, zeta, diff, nstr
POINTS = [(mpf("0.99"), mpf(286) / 3), (mpf("0.9"), mpf(60)), (mpf("0.25"), mpf("59.35"))]
def H_analytic(s):
    z, z1 = zeta(s), zeta(s, derivative=1); return -z1 / z
def Hp_analytic(s):
    z, z1, z2 = zeta(s), zeta(s, derivative=1), zeta(s, derivative=2); return -(z2 * z - z1 * z1) / (z * z)
def cg(sig, t, route=1):
    s = mpc(sig, t)
    H = H_analytic(s) if route == 1 else -diff(zeta, s) / zeta(s)
    return H.real, -H.imag
def W_analytic(sig, t):
    s = mpc(sig, t); H = H_analytic(s); d = 1j * Hp_analytic(s)
    c, g = H.real, -H.imag; ct, gt = d.real, -d.imag
    return c * gt - g * ct
def W_fd(sig, t, h, route=1):
    c, g = cg(sig, t, route); c1, g1 = cg(sig, t + h, route); c0, g0 = cg(sig, t - h, route)
    return c * (g1 - g0) / (2 * h) - g * (c1 - c0) / (2 * h)
bad = 0
for sig, t in POINTS:
    print("point sigma=%s  t=%s" % (nstr(sig, 6), nstr(t, 12)))
    vals = []
    for dps in (30, 50, 80):
        mp.dps = dps
        w = W_analytic(sig, t); vals.append(w)
        s = mpc(sig, t); c, g = cg(sig, t)
        print("   dps=%2d  c=%s  g=%s  |zeta|=%s  W(analytic)=%s" % (dps, nstr(c, 12), nstr(g, 12), nstr(abs(zeta(s)), 6), nstr(w, 15)))
    mp.dps = 50
    for h in (mpf("1e-3"), mpf("1e-5"), mpf("1e-7")):
        print("   h=%s  W(central difference)=%s" % (nstr(h, 2), nstr(W_fd(sig, t, h), 15)))
    mp.dps = 30
    print("   route 3 (numerical derivative of zeta, h=1e-6): W=%s" % nstr(W_fd(sig, t, mpf("1e-6"), route=3), 12))
    mp.dps = 80
    ref = W_analytic(sig, t)
    spread = max(abs(v - ref) for v in vals)
    ok = ref < 0 and spread < mpf("1e-20")
    print("   W<0 and stable across precision (spread %s): %s" % (nstr(spread, 3), "PASS" if ok else "FAIL")); bad += (not ok)
sys.exit(1 if bad else 0)
