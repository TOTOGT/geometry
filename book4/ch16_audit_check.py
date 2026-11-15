#!/usr/bin/env python3
"""ch16_audit_check.py -- read-only numeric checks of Chapter 16 statements (audit 2026-11-15). Complements ch16_colony_count_check.py."""
import math, sys
from fractions import Fraction as Fr
bad = 0
def ck(n, ok):
    global bad; bad += (not ok); print(('PASS ' if ok else 'FAIL ') + n)
# hexagon vs square, regular tilings: A/P^2
hex_r = math.sqrt(3)/24; sq = 1/16
ck('hex A/P^2 = sqrt3/24 = 0.0722 > 1/16 (hexagon of side s: A=3sqrt3/2 s^2, P=6s)', abs(hex_r - (1.5*math.sqrt(3))/36) < 1e-12 and hex_r > sq)
ck('advantage = 2sqrt3/3 - 1 = 15.47% > 15%', abs(hex_r/sq - 2*math.sqrt(3)/3) < 1e-12 and hex_r/sq > 1.15)
ck('advantage > 15% iff sqrt3 > 1.725 (Task 1)', (math.sqrt(3) > 1.725) == (hex_r/sq > 1.15))
# APF
apf = {'diamond': math.pi*math.sqrt(3)/16, 'sc': math.pi/6, 'bcc': math.pi*math.sqrt(3)/8, 'fcc/hcp': math.pi/(3*math.sqrt(2))}
ck('APF 0.34/0.52/0.68/0.74', [round(v, 2) for v in apf.values()] == [0.34, 0.52, 0.68, 0.74])
# hexagonal interplanar spacing formula vs reciprocal lattice
a, c = 1.0, 1.633
import itertools
def d_recip(h, k, l):
    a1 = (a, 0, 0); a2 = (-a/2, a*math.sqrt(3)/2, 0); a3 = (0, 0, c)
    cr = lambda u, v: (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])
    dot = lambda u, v: sum(x*y for x, y in zip(u, v))
    V = dot(a1, cr(a2, a3))
    b = [tuple(x/V for x in cr(a2, a3)), tuple(x/V for x in cr(a3, a1)), tuple(x/V for x in cr(a1, a2))]
    g = [h*b[0][i] + k*b[1][i] + l*b[2][i] for i in range(3)]
    return 1/math.sqrt(dot(g, g))
ok = all(abs(1/d_recip(h, k, l)**2 - (4/3*(h*h+h*k+k*k)/a**2 + l*l/c**2)) < 1e-9 for h, k, l in itertools.product(range(-2, 3), repeat=3) if (h, k, l) != (0, 0, 0))
ck('hexagonal 1/d^2 formula matches reciprocal lattice', ok)
# eps0 arithmetic as printed on the page
ck('page prints eps0 = 2/(2*2) = 1/3, but 2/(2*2) = 1/2', Fr(2, 2*2) == Fr(1, 2) and Fr(2, 2*2) != Fr(1, 3))
H = Fr(2, 2*3)
ck('eps0 = 1/3 needs 1+H = 3 i.e. H = 2 (Lean: epsilon0_of_eq_third_iff), not H = 1', H == Fr(1, 3) and Fr(2, 2*(1+1)) == Fr(1, 2))
ck('noise tolerance tau*eps0 = 2/3 given eps0 = 1/3', 2*Fr(1, 3) == Fr(2, 3))
# aspect / metres / scaling
ck('33000/500 = 66 = 33*2; 33000*0.4572 = 15087.6; 250*0.4572 = 114.3', 33000/500 == 66 == 33*2 and abs(33000*0.4572-15087.6) < 1e-9 and abs(250*0.4572-114.3) < 1e-9)
ck('Moon ~6.0, Mars 2.64, Mars height ~39.8 km', abs(9.80665/1.62-6.05) < 0.05 and abs(9.80665/3.71-2.643) < 0.01 and abs(15.0876*9.80665/3.71-39.88) < 0.1)
# Schumann: ideal-cavity formula
c0 = 299792.458
for R in (6371.0,):
    f = lambda n: c0/(2*math.pi*R)*math.sqrt(n*(n+1))
    print('INFO ideal-cavity f1..f5 (R=6371 km):', [round(f(n), 2) for n in range(1, 6)])
    ck('f4 (ideal) = 33.50 Hz with R=6371 km; page prints 33.516 (implies R~6366 km)', abs(f(4)-33.50) < 0.02 and abs(f(4)-33.516) > 0.01)
    ck('|33-f4|/f4 = 1.5%', abs(abs(33-f(4))/f(4) - 0.0149) < 0.001)
print('NOTE hand argument, not computed: the ideal-cavity formula overestimates the MEASURED Schumann modes; commonly reported measured values are ~7.8, 14.3, 20.8, 27.3, 33.8 Hz, so ideal f4 sits near the measured 5th mode (from memory, verify against a source before citing).')
print('NOTE hand argument, not computed: the Schumann section rows are already withdrawn on the page; 33 (a count) vs hertz is dimensionally unrelated, as the page itself says.')
sys.exit(1 if bad else 0)
