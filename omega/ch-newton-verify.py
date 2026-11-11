#!/usr/bin/env python3
"""
omega/ch-newton-verify.py -- every number in the numerical section of omega/ch-newton.html, produced here.

Blocks:
  [1] pi by Machin's formula in 60-digit Decimal (no library constant)
  [2] 6 * arcsin(1/2) summed from Newton's arcsine series: the first 22 terms give an error below 1e-15, 21 do not; the
      error ratio between successive terms approaches 4
  [3] 4 * (1 - 1/3 + 1/5 - ...): the error after n terms is within 10% of 1/n for n = 100..2000, so reaching 1e-15
      needs about 1e15 terms (an extrapolation of that ratio, not a summation to 1e15)
  [4] the page: prints 22 terms and the 1e15 figure, lists what is not checked, and asserts no influence or transmission

This script checks arithmetic only. That Newton used the arcsine series, computed pi to about fifteen places, or any
biographical claim on the page is NOT checked here.
Standard library only.  Run:  python3 omega/ch-newton-verify.py
"""
import os, sys
from decimal import Decimal as D, getcontext
getcontext().prec = 60
here = os.path.dirname(os.path.abspath(__file__))
FAIL = []
def check(label, ok, detail=""):
    print(("  PASS  " if ok else "  FAIL  ") + label + (("   " + detail) if detail else ""))
    if not ok: FAIL.append(label)
def atan_inv(x):
    x = D(x); s = D(0); t = 1/x; k = 0
    while abs(t) > D(10)**-58:
        s += t/(2*k+1)*(1 if k % 2 == 0 else -1); t /= x*x; k += 1
    return s
PI = 4*(4*atan_inv(5) - atan_inv(239))
check('Machin pi starts 3.14159265358979323846264338327950288', str(PI).startswith('3.14159265358979323846264338327950288'))
x = D(1)/2; coef = D(1); s = D(0); errs = []
for n in range(0, 60):
    s += coef*x**(2*n+1)/(2*n+1); errs.append(abs(6*s - PI)); coef *= D(2*n+1)/D(2*n+2)
first = next(i+1 for i, e in enumerate(errs) if e < D(10)**-15)
check('arcsine series: first N with error < 1e-15 is 22 (found %d)' % first, first == 22)
check('arcsine series: 21 terms do not reach 1e-15', errs[20] >= D(10)**-15)
ratio = float(errs[40]/errs[41])
check('arcsine series: successive error ratio is 4.1 to one decimal at term 41 (%.3f) and decreasing toward 4' % ratio, round(ratio, 1) == 4.1 and float(errs[20]/errs[21]) > ratio)
S = D(0); ok = True
for n in range(1, 2001):
    S += D((-1)**(n-1))/(2*n-1)
    if n >= 100 and n in (100, 500, 1000, 2000):
        e4 = abs(PI - 4*S); ok &= (D('0.9') < e4*n < D('1.1'))
check('alternating series: 4 * error is within 10% of 1/n at n = 100, 500, 1000, 2000', ok)
check('alternating series: from 4*error ~ 1/n, an error of 1e-15 needs about 1e15 terms (between 0.9e15 and 1.1e15)', True and ok)
page = open(os.path.join(here, 'ch-newton.html'), encoding='utf-8').read()
check('page prints the 22-term result', 'first 22 terms' in page)
check('page prints the 10^15 figure', '10^{15}' in page)
check('page lists what is not checked', 'What is not checked' in page and 'not matched against a source' in page)
check('page asserts no influence or transmission', 'no claim of influence' in page and 'no transmission' in page)
check('page calls the word mystic contested', 'contested' in page)
print()
print("RESULT:", "ALL PASS" if not FAIL else "FAILURES: %s" % FAIL)
sys.exit(0 if not FAIL else 1)
