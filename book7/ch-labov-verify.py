#!/usr/bin/env python3
"""
Labov -- verifier for book7/ch-labov.html.

THE MODEL (the logistic S-curve of language change in the form usually attributed to Kroch's constant-rate
hypothesis; the attribution is CITED and was not checked): the share p(t) of an incoming variant in a context is
    logit p(t) = s t + c,   i.e.   p(t) = 1/(1 + exp(-(s t + c))),   dp/dt = s p (1 - p).

CHECKS:
  1. A fourth-order Runge-Kutta integration of dp/dt = s p (1-p), s = 0.1 per year, p(0) from c = -3, run for 100 years
     (step 0.01), agrees with the closed form to better than 1e-9 at every whole year.
  2. Two contexts with the same slope s = 0.1 and intercepts c1 = -3, c2 = -1: logit p2 - logit p1 = 2 exactly
     (to 1e-12) at every whole year from 0 to 100. Control: if the second context has slope 0.15 the gap is not constant.
  3. The time to go from 10% to 90% is 2 ln 9 / s for s = 0.1 (value printed), checked by root-finding on the closed form.
  4. The page's figures equal the computed values.

DOES NOT ESTABLISH: that any real change follows an S-curve, that contexts share a slope (the constant-rate hypothesis
is a CITED empirical claim), or anything about Labov's data or studies, which are CITED and were not checked. The
numbers are model values, not data.

    python3 book7/ch-labov-verify.py
"""
import math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
fails = []
def check(ok, msg):
    print('    %s  %s' % ('PASS' if ok else 'FAIL', msg))
    if not ok: fails.append(msg)
def head(n, t): print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)
def P(t, s, c): return 1 / (1 + math.exp(-(s * t + c)))
def logit(p): return math.log(p / (1 - p))

head(1, 'THE ODE AND THE CLOSED FORM AGREE')
s, c = 0.1, -3.0; p = P(0, s, c); h = 0.01; worst = 0.0
for step in range(1, 10001):
    k1 = s * p * (1 - p); k2 = s * (p + h * k1 / 2) * (1 - p - h * k1 / 2)
    k3 = s * (p + h * k2 / 2) * (1 - p - h * k2 / 2); k4 = s * (p + h * k3) * (1 - p - h * k3)
    p += h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
    if step % 100 == 0: worst = max(worst, abs(p - P(step * h, s, c)))
check(worst < 1e-9, 'RK4 and the closed form agree to %.1e at every whole year (0..100)' % worst)

head(2, 'CONSTANT RATE: EQUAL SLOPES, DIFFERENT INTERCEPTS')
gaps = [logit(P(t, 0.1, -1.0)) - logit(P(t, 0.1, -3.0)) for t in range(0, 101)]
check(max(abs(g - 2.0) for g in gaps) < 1e-12, 'logit gap between the two contexts is 2 at every year 0..100')
gaps2 = [logit(P(t, 0.15, -1.0)) - logit(P(t, 0.1, -3.0)) for t in range(0, 101)]
check(max(gaps2) - min(gaps2) > 1, 'control: with unequal slopes the gap is not constant (it ranges over %.1f)' % (max(gaps2) - min(gaps2)))

head(3, 'TIME FROM 10% TO 90%')
T = 2 * math.log(9) / 0.1
lo, hi = 0.0, 200.0
def t_at(target, s=0.1, c=-3.0):
    lo, hi = -500.0, 500.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if P(mid, s, c) < target: lo = mid
        else: hi = mid
    return (lo + hi) / 2
Tnum = t_at(0.9) - t_at(0.1)
print('    2 ln 9 / s = %.4f years   root-finding gives %.4f years' % (T, Tnum))
check(abs(T - Tnum) < 1e-9, 'closed form for the 10-90 time agrees with root-finding')

head(4, "THE PAGE'S FIGURES")
html = open(os.path.join(HERE, 'ch-labov.html'), encoding='utf-8').read()
m = re.search(r'data-T="([0-9.]+)" data-gap="([0-9.]+)"', html)
check(bool(m) and m.group(1) == '%.4f' % T and m.group(2) == '2.0', 'page states 10-90 time %.4f and gap 2.0' % T)
for lab in ('CITED RESULT', 'CHECKED INSTANCE', 'OPEN QUESTION', 'THEOREM'):
    check(('<b>%s</b>' % lab) in html, 'visible evidence label %s present' % lab)
check('ch-labov-verify.py' in html, 'page names this verifier')
check('were not checked for this page' in html, 'page states which items were not checked')
check('href="ch-nowak.html"' in html, 'link to ch-nowak')
print('\n' + '=' * 70)
if fails:
    print('  %d CHECK(S) FAILED:' % len(fails)); [print('    - ' + f) for f in fails]; sys.exit(1)
print('  ALL CHECKS PASSED')
