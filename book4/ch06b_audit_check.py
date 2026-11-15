#!/usr/bin/env python3
"""ch06b_audit_check.py -- read-only arithmetic checks of Chapter 6b (audit 2026-11-15)."""
import math, sys
bad = 0
def ck(n, ok):
    global bad; bad += (not ok); print(('PASS ' if ok else 'FAIL ') + n)
n = 2*math.pi/math.sqrt(3)
ck('2*pi/sqrt(3) = %.4f (SBIR draft value 3.6276); page prints n ~ 3.64, which is not the rounding of that value (3.63)' % n, abs(n-3.6276) < 1e-4 and round(n, 2) == 3.63)
eps0, rstar, kappa = 1/3, 0.77594058, 0.882
ck('page chain eps0=1/3 < r*=0.7759 < kappa*=0.882 < 1 compares a radius (1/3) with locations; as locations the Gronwall inner edge is 1-eps0 = 0.6667 < r* = 0.7759', abs((1-eps0)-0.6667) < 1e-4 and (1-eps0) < rstar)
ck('1/3 < 0.7759 is true but compares a radius with a location', eps0 < rstar)
# whole 6b outer limit statement vs ch12 note: 1 < r <= 6.8 verified, outer limit ~ 6.859 at z0=0
ck('6.8 < 6.859 (page range lies inside the later-quoted outer limit)', 6.8 < 6.859)
# Hill-type sigmoid with exponent n: width of 10%-90% transition in log-dose = 2*ln(9)/n
w = 2*math.log(9)/n
print('INFO Hill n = %.4f: 10-90%% transition spans a factor %.2f in the input' % (n, math.exp(w)))
print('NOTE hand argument, not computed: Whitney fold is A2 (x^3 + u x). ch06b uses A2 correctly; ch15 calls F "the Whitney A1 fold" (A1 is a nondegenerate critical point).')
print('NOTE hand argument, not computed: a rigid island rotating about the channel centre has a marked shoreline point at constant r, so "r converges to 1" is not an observable of El Ojo as described; the model-to-object map is not defined (page says: a model, not a field measurement).')
sys.exit(1 if bad else 0)
