#!/usr/bin/env python3
"""
Abrams and Strogatz -- verifier for book7/ch-abrams-strogatz.html.

The model as read from the paper's text in the session that wrote this page (see the page for the labels):
    dx/dt = (1 - x) P_yx(x, s) - x P_xy(x, s),   P_yx = c x^a s,   P_xy = c (1 - x)^a (1 - s),
x = fraction speaking language X, s = X's status (0..1), c = 1 (a time scale). So  f(x) = s x^a (1-x) - (1-s)(1-x)^a x.

CHECKS:
  1. f(0) = f(1) = 0 for all a, s.
  2. For a > 1 and 0 < s < 1: the interior fixed point is unique, at x* = 1 / (1 + (s/(1-s))^(1/(a-1))), is unstable,
     and 0 and 1 are stable. Checked on a grid of s (0.05..0.95) and a in {1.1, 1.31, 2, 3}: sign pattern of f on
     (0,1) is  - below x*, + above, found by evaluation, and x* agrees with bisection to 1e-10 wherever 1e-6 < x* < 1 - 1e-6.
  3. For a < 1 the interior fixed point is stable and 0, 1 are unstable (a in {0.5, 0.8}), same grid.
  4. For a = 1 there is no interior fixed point unless s = 1/2: f(x) = (2s - 1) x (1 - x).
  5. Trajectories (RK4, step 0.01 to t = 400): for a = 1.31, s = 0.55, x* = printed; start x* - 0.02 -> 0, x* + 0.02 -> 1.
  6. The page's figures equal the computed values.

DOES NOT ESTABLISH: that the equation fits any real language shift (the fitted a = 1.31 +/- 0.25 is CITED from the paper
and was not re-fitted here), that two-language competition with no bilinguals is the right model, or any statement
about the number of languages in danger (CITED).

    python3 book7/ch-abrams-strogatz-verify.py
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
fails = []
def check(ok, msg):
    print('    %s  %s' % ('PASS' if ok else 'FAIL', msg))
    if not ok: fails.append(msg)
def head(n, t): print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)
def f(x, a, s): return s * x ** a * (1 - x) - (1 - s) * (1 - x) ** a * x
def xstar(a, s): return 1 / (1 + (s / (1 - s)) ** (1 / (a - 1)))
def bisect(a, s):
    lo, hi = 1e-9, 1 - 1e-9; flo = f(lo, a, s)
    for _ in range(200):
        mid = (lo + hi) / 2; fm = f(mid, a, s)
        if (fm > 0) == (flo > 0): lo, flo = mid, fm
        else: hi = mid
    return (lo + hi) / 2
grid_s = [i / 20 for i in range(1, 20) if i != 10]

head(1, 'ENDPOINTS')
check(all(f(0, a, s) == 0 and f(1, a, s) == 0 for a in (0.5, 1, 1.31, 2) for s in (0.1, 0.5, 0.9)), 'f(0) = f(1) = 0')

head(2, 'a > 1: BISTABLE, ONE UNSTABLE INTERIOR POINT')
ok_sign = ok_x = True; n_cmp = 0
for a in (1.1, 1.31, 2, 3):
    for s in grid_s + [0.5]:
        xs = xstar(a, s)
        if 1e-6 < xs < 1 - 1e-6:
            n_cmp += 1
            if abs(xs - bisect(a, s)) > 1e-10: ok_x = False
        lo = [f(xs * k / 50, a, s) for k in range(1, 50)]; hi = [f(xs + (1 - xs) * k / 50, a, s) for k in range(1, 50)]
        if not (all(v < 0 for v in lo) and all(v > 0 for v in hi)): ok_sign = False
print('    bisection compared on %d (a, s) pairs where 1e-6 < x* < 1 - 1e-6 (outside that the bracket is too tight)' % n_cmp)
check(ok_x and n_cmp > 40, 'closed form x* matches bisection to 1e-10 on those pairs')
check(ok_sign, 'f < 0 below x* and f > 0 above it: x* unstable, 0 and 1 stable')
check(abs(xstar(1.31, 0.5) - 0.5) < 1e-12, 'with equal status (s = 1/2) the unstable point is at x* = 1/2')

head(3, 'a < 1: COEXISTENCE IS STABLE')
ok3 = True
for a in (0.5, 0.8):
    for s in grid_s + [0.5]:
        xs = xstar(a, s)
        lo = [f(xs * k / 50, a, s) for k in range(1, 50)]; hi = [f(xs + (1 - xs) * k / 50, a, s) for k in range(1, 50)]
        if not (all(v > 0 for v in lo) and all(v < 0 for v in hi)): ok3 = False
check(ok3, 'f > 0 below x* and f < 0 above it: x* stable, 0 and 1 unstable')

head(4, 'a = 1')
check(all(abs(f(x, 1, s) - (2 * s - 1) * x * (1 - x)) < 1e-15 for s in (0.2, 0.55, 0.9) for x in (0.1, 0.5, 0.8)), 'f = (2s - 1) x (1 - x): no interior fixed point for s != 1/2')

head(5, 'TRAJECTORIES, a = 1.31, s = 0.55')
a, s = 1.31, 0.55; xs = xstar(a, s)
print('    x* = %.4f  (status 0.55 for X lowers the threshold below 1/2)' % xs)
def run(x0):
    x = x0; h = 0.01
    for _ in range(40000):
        k1 = f(x, a, s); k2 = f(x + h * k1 / 2, a, s); k3 = f(x + h * k2 / 2, a, s); k4 = f(x + h * k3, a, s)
        x += h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
    return x
below, above = run(xs - 0.02), run(xs + 0.02)
print('    start x* - 0.02 -> %.6f   start x* + 0.02 -> %.6f' % (below, above))
check(below < 0.01 and above > 0.99, 'just below x* the trajectory goes to 0; just above it goes to 1')
check(xs < 0.5, 'x* is below 1/2 when X has the higher status')

head(6, "THE PAGE'S FIGURES")
html = open(os.path.join(HERE, 'ch-abrams-strogatz.html'), encoding='utf-8').read()
m = re.search(r'data-xstar="([0-9.]+)"', html)
check(bool(m) and m.group(1) == '%.4f' % xs, 'page states x* = %.4f' % xs)
for lab in ('CITED RESULT', 'CHECKED INSTANCE', 'OPEN QUESTION', 'THEOREM'):
    check(('<b>%s</b>' % lab) in html, 'visible evidence label %s present' % lab)
check('ch-abrams-strogatz-verify.py' in html, 'page names this verifier')
check('were not checked for this page' in html, 'page states which items were not checked')
check('href="ch-strogatz.html"' in html, 'link to ch-strogatz')
print('\n' + '=' * 70)
if fails:
    print('  %d CHECK(S) FAILED:' % len(fails)); [print('    - ' + f) for f in fails]; sys.exit(1)
print('  ALL CHECKS PASSED')
