#!/usr/bin/env python3
"""
Nowak -- verifier for book7/ch-nowak.html.

The equation, as read from Nowak, Komarova and Niyogi (Nature 417, 2002), their Eq. 1:
    dx_j/dt = sum_i f_i(x) Q_ij x_i - phi(x) x_j,   f_i = sum_j x_j F_ij,   phi = sum_i f_i x_i.
THIS PAGE'S REDUCTION (not in the paper): two grammars, payoff F = [[1, a], [a, 1]] with 0 <= a < 1, learning
matrix Q = [[q, 1-q], [1-q, q]], x = fraction of speakers of grammar 1.  Then
    F(x) = x f1 q + (1-x) f2 (1-q) - phi x,  f1 = x + a(1-x), f2 = a x + (1-x), phi = x f1 + (1-x) f2.

CHECKS:
  1. Exact identity (Fractions, 41 sample points, several (a, q)):  F(x) = (2x-1)(a x^2 - a x + q - x^2 + x - 1).
  2. Hence x = 1/2 is a fixed point and F'(1/2) = (4q - 3 - a)/2: stable iff q < (3 + a)/4.
  3. For q > (3 + a)/4 and a < 1, two more fixed points x = 1/2 +- sqrt(D)/(2(1-a)), D = (1-a)(4q-3-a), lie in (0,1),
     are roots of F, and are stable; 1/2 is then unstable.
  4. Trajectories (RK4) for a = 0.5 (threshold q* = 7/8): q = 0.80 from x = 0.6 ends at 1/2; q = 0.95 from x = 0.51 ends
     at 1/2 + sqrt(D)/(2(1-a)) (printed).
  5. The page's figures equal the computed values.

DOES NOT ESTABLISH: the paper's coherence thresholds in terms of the number of example sentences N and grammars n
(CITED: N > C1 n for a memoryless learner, N > C2 log n for a batch learner, with unspecified constants), that the
two-grammar reduction has any bearing on real populations, or anything about Nowak's life or other work.

    python3 book7/ch-nowak-verify.py
"""
import math, os, re, sys
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
fails = []
def check(ok, msg):
    print('    %s  %s' % ('PASS' if ok else 'FAIL', msg))
    if not ok: fails.append(msg)
def head(n, t): print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)
def Fx(x, a, q):
    f1 = x + a * (1 - x); f2 = a * x + (1 - x); phi = x * f1 + (1 - x) * f2
    return x * f1 * q + (1 - x) * f2 * (1 - q) - phi * x
def fact(x, a, q): return (2 * x - 1) * (a * x * x - a * x + q - x * x + x - 1)

head(1, 'EXACT FACTORIZATION')
ok = all(Fx(Fr(i, 40), a, q) == fact(Fr(i, 40), a, q) for i in range(41) for a in (Fr(0), Fr(1, 2), Fr(9, 10)) for q in (Fr(1, 2), Fr(4, 5), Fr(95, 100)))
check(ok, 'F(x) equals the factored form exactly at 41 points for 9 pairs (a, q)')

head(2, 'STABILITY OF THE SYMMETRIC STATE')
def dF(x, a, q, h=1e-6): return (Fx(x + h, a, q) - Fx(x - h, a, q)) / (2 * h)
ok2 = all(abs(dF(0.5, a, q) - (4 * q - 3 - a) / 2) < 1e-6 for a in (0.0, 0.5, 0.9) for q in (0.5, 0.8, 0.95, 1.0))
check(ok2, "F'(1/2) = (4q - 3 - a)/2 (central difference, 12 pairs)")
check(all((dF(0.5, a, q) < 0) == (q < (3 + a) / 4) for a in (0.0, 0.5, 0.9) for q in (0.5, 0.7, 0.8, 0.95)), '1/2 is stable exactly when q < (3 + a)/4')

head(3, 'THE TWO OFF-CENTRE STATES')
ok3 = True; n3 = 0
for a in (0.0, 0.5, 0.9):
    qs = (3 + a) / 4
    for q in (qs + 0.01, qs + 0.04, qs + (1 - qs) / 2):  # q = 1 is excluded: the roots then sit exactly at 0 and 1
        if q <= qs or q > 1: continue
        D = (1 - a) * (4 * q - 3 - a); r = math.sqrt(D) / (2 * (1 - a)); xs = (0.5 + r, 0.5 - r); n3 += 1
        for x in xs:
            if not (0 < x < 1 and abs(Fx(x, a, q)) < 1e-12): ok3 = False
        if not (dF(xs[0], a, q) < 0 and dF(xs[1], a, q) < 0 and dF(0.5, a, q) > 0): ok3 = False
check(ok3 and n3 >= 6, 'for q above (3 + a)/4 both off-centre roots are in (0,1), solve F = 0, and are stable (%d cases)' % n3)

ok3b = all(all(Fx(i / 200, a, q) > 0 for i in range(1, 100)) and all(Fx(i / 200, a, q) < 0 for i in range(101, 200))
           for a in (0.0, 0.5, 0.9) for q in (0.5, 0.6, (3 + a) / 4 - 0.01))
check(ok3b, 'below the threshold F > 0 left of 1/2 and F < 0 right of it: no other fixed point and no bistability (the transition has no hysteresis)')

head(4, 'TRAJECTORIES, a = 0.5')
def run(x0, a, q):
    x = x0; h = 0.01
    for _ in range(40000):
        k1 = Fx(x, a, q); k2 = Fx(x + h * k1 / 2, a, q); k3 = Fx(x + h * k2 / 2, a, q); k4 = Fx(x + h * k3, a, q)
        x += h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
    return x
a = 0.5; low = run(0.6, a, 0.80); D = (1 - a) * (4 * 0.95 - 3 - a); xc = 0.5 + math.sqrt(D) / (2 * (1 - a)); high = run(0.51, a, 0.95)
print('    threshold q* = (3 + a)/4 = %.4f;  q = 0.80 from 0.6 -> %.6f;  q = 0.95 from 0.51 -> %.6f (predicted %.6f)' % ((3 + a) / 4, low, high, xc))
check(abs(low - 0.5) < 1e-6, 'below the threshold the population returns to the mixed state 1/2')
check(abs(high - xc) < 1e-6, 'above the threshold it settles on the off-centre state %.4f' % xc)

head(5, "THE PAGE'S FIGURES")
html = open(os.path.join(HERE, 'ch-nowak.html'), encoding='utf-8').read()
m = re.search(r'data-xc="([0-9.]+)"', html)
check(bool(m) and m.group(1) == '%.4f' % xc, 'page states the coherent state %.4f' % xc)
for lab in ('CITED RESULT', 'CHECKED INSTANCE', 'OPEN QUESTION', 'THEOREM'):
    check(('<b>%s</b>' % lab) in html, 'visible evidence label %s present' % lab)
check('ch-nowak-verify.py' in html, 'page names this verifier')
check('were not checked for this page' in html, 'page states which items were not checked')
check('href="ch-abrams-strogatz.html"' in html, 'link to ch-abrams-strogatz')
print('\n' + '=' * 70)
if fails:
    print('  %d CHECK(S) FAILED:' % len(fails)); [print('    - ' + f) for f in fails]; sys.exit(1)
print('  ALL CHECKS PASSED')
