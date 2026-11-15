#!/usr/bin/env python3
"""ch00_student_audit_check.py -- read-only checks of book4/ch00-student-edition.html (audit 2026-11-15). numpy/scipy."""
import sys, numpy as np
from scipy.integrate import solve_ivp
bad = 0
def ck(n, ok):
    global bad; bad += (not ok); print(('PASS ' if ok else 'FAIL ') + n)
# 1. page example "Theorem: every orbit with r(0) > 1 converges to r = 1" (system: r' = r(1-r^2)+2(r-1)e^{-z}, z' = r^2 - 2(r-1)^2 e^{-z})
def rhs(t, y):
    r, z = y; e = np.exp(-z)
    return [r*(1-r*r) + 2*(r-1)*e, r*r - 2*(r-1)**2*e]
def blow(t, y): return 1e6 - abs(y[0]) if abs(y[1]) < 60 else -1.0
blow.terminal = True
def final_r(r0, z0=0.0, T=60):
    with np.errstate(all='ignore'):
        s = solve_ivp(rhs, [0, T], [r0, z0], method='RK45', rtol=1e-9, atol=1e-12, events=blow)
    return s.y[0, -1], s.t[-1], s.y[1, -1]
r_in, _, _ = final_r(2.0)
ck('r(0)=2, z(0)=0 converges to r=1 (final r = %.6f)' % r_in, abs(r_in-1) < 1e-4)
# Observed trajectory for r(0)=7.5, z(0)=0, recorded with solver status. A numerical stop is NOT evidence of finite-time
# blow-up or of non-convergence by itself: the word "blows up" is reserved for an analytic argument or validated bound,
# and this script has neither. The claim that "every orbit with r(0)>1 converges" is flagged on SEPARATE evidence:
# ch03_outer_basin_check.py (DOP853 rtol 1e-13 bisection: largest converging r(0) at z(0)=0 is ~6.859, numerical, not a proof).
import warnings
def run(method, rtol, atol):
    with np.errstate(all='ignore'), warnings.catch_warnings():
        warnings.simplefilter('ignore')
        s = solve_ivp(rhs, [0, 60], [7.5, 0.0], method=method, rtol=rtol, atol=atol)  # no event: plain integration
    return s
print('INFO r(0)=7.5, z(0)=0, T=60 (observations, not a blow-up proof):')
stops = []
for m, rt, at in [('RK45', 1e-9, 1e-12), ('RK45', 1e-12, 1e-14), ('DOP853', 1e-13, 1e-15), ('Radau', 1e-10, 1e-12)]:
    s = run(m, rt, at)
    stops.append(s.t[-1])
    print('INFO   %-6s rtol=%g atol=%g: status=%d (%s) stopped at t=%.5f after %d steps; r=%.4g z=%.4g' % (m, rt, at, s.status, s.message, s.t[-1], len(s.t), s.y[0, -1], s.y[1, -1]))
print('INFO   all four integrations stopped with a step-size failure (status -1) before t=60; the final z differs between runs (about -27 to -29), so the endpoint is solver-dependent and is not a limiting value.')
r_out = run('RK45', 1e-9, 1e-12).y[0, -1]
ck('r(0)=7.5, z(0)=0: the integrations did not reach t=60 at r=1 (all four solver runs failed at t=%.5f +/- %.1e); this is an observation, and the claim "every orbit with r(0)>1 converges" is flagged on the separate ch03/ch10 evidence, not on this stop' % (stops[0], max(stops) - min(stops)), max(stops) < 1.0 and abs(r_out - 1) > 1e-2)
rz, tz, zz = final_r(1.5, z0=-8.0)
print('INFO r(0)=1.5, z(0)=-8: r = %.4g, z = %.3g at t = %.3g (ch12 notes the global statement also fails at very negative z)' % (rz, zz, tz))
# 2. Collatz reading order on chapters 0..28
def step(n): return n//2 if n % 2 == 0 else 3*n+1
exits = []
for s0 in range(1, 29):
    n = s0; seen = 0
    while n != 1 and seen < 200:
        if n > 28: exits.append(s0); break
        n = step(n); seen += 1
ck('Pass 2: orbits starting at chapters 1..28 that leave the book (reach a chapter > 28): %d of 28 (first: %s)' % (len(exits), exits[:6]), len(exits) > 0)
ck('chapter 0 maps to itself (0/2 = 0), never to chapter 1', step(0) == 0)
print('NOTE hand argument, not computed: "every orbit converges to Chapter 1" is the Collatz conjecture, open; verified computationally for very large ranges but not proved.')
print('NOTE hand argument, not computed: chapter pointers are stale: "Does the attractor persist? (Yes - Chapter 11)", "Chapter 12 lives here (jet space)", "GTCT ... Chapter 13 onward", "Chapters 0 -> 15"; the book has ch11 = Arithmetic Seed, ch12 = Critical Contact, GTCT in ch06, and chapters 0-28.')
print('NOTE hand argument, not computed: the ladder row "(x, y, p), p = dy/dx -> 5D contact structure" lists the 3D jet coordinates of J^1(R,R) and calls J^1(R,R^2) a 5D contact structure; ch05 (2026-10-09 correction) shows it is a rank-2 Pfaffian system. "theta-dot = 1 (varying)" is a constant.')
sys.exit(1 if bad else 0)
