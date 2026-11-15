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
r_out, tend, zend = final_r(7.5)
ck('r(0)=7.5, z(0)=0 (r(0)>1) does NOT converge to 1 (r = %.4g, z = %.3g when integration stops at t=%.3g): the statement "every orbit with r(0)>1 converges" is false as written' % (r_out, zend, tend), abs(r_out-1) > 1e-2)
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
