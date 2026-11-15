#!/usr/bin/env python3
"""wp56_audit_check.py -- read-only checks for the corrected Section 10 (audit 2026-11-15). Units: c=1, years, light-years."""
import random, math, sys
bad = 0
def ck(n, ok):
    global bad; bad += (not ok); print(('PASS ' if ok else 'FAIL ') + n)
d = 2.537e6
s2 = lambda a, b: -(a[0]-b[0])**2 + sum((u-v)**2 for u, v in zip(a[1:], b[1:]))
A, B = (0, -d/2), (0, d/2)
ck('s2(A,B)=d^2>0 (spacelike, invariant)', s2(A, B) == d*d)
T0 = d/2
M = (T0, 0.0)
ck('at T=d/2c both connections are null', abs(s2(A, M)) < 1e-3 and abs(s2(B, M)) < 1e-3)
ck('d/2c = 1.2685 Myr', abs(T0/1e6 - 1.2685) < 1e-4)
ck('for T>d/2c both are timelike-past of M, A-B stays spacelike', s2(A, (T0+1, 0.0)) < 0 and s2(B, (T0+1, 0.0)) < 0 and s2(A, B) > 0)
# extended-source formula: T_CI(y) = max over history of t + |x-y|/c, checked against brute force reception condition
random.seed(1)
H = [(random.uniform(0, 1e5), (random.uniform(-d/2-5e4, -d/2+5e4), random.uniform(-5e4, 5e4), 0.0)) for _ in range(200)] + \
    [(random.uniform(0, 1e5), (random.uniform(d/2-5e4, d/2+5e4), random.uniform(-5e4, 5e4), 0.0)) for _ in range(200)]
y = (0.0, 0.0, 0.0)
f = max(t + math.dist(x, y) for t, x in H)
brute_ok = all(f - t >= math.dist(x, y) - 1e-6 for t, x in H)
just_before = any((f - 1.0) - t < math.dist(x, y) for t, x in H)
ck('formula: all sources in past of receiver at T_CI, and a source fails 1 yr earlier', brute_ok and just_before)
# simultaneity shift at walking speed (page value ~4 days, 0.012 yr)
v = 5/3.6/299792.458/1000  # 5 km/h in units of c, km->... 
v = (5/3600)/299792.458     # km/s / (km/s)
ck('walking-speed shift ~0.012 yr', abs(v*d - 0.012) < 0.001)
print('NOTE hand argument, not computed: merger time depends on a dynamical criterion; Sawala et al. 2025 report about 50% no merger within 10 Gyr (press reports read, paper not read).')
sys.exit(1 if bad else 0)
