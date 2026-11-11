#!/usr/bin/env python3
"""
omega/ch-madhava-verify.py -- every number in the numerical section of omega/ch-madhava.html, produced here.

Blocks:
  [1] the Madhava-Leibniz series: |pi/4 - S_n| < 1/(2n+1) (alternating-series bound), and the error is close to 1/(4n)
  [2] the correction terms attributed to Madhava by later sources, checked as formulas: adding 1/(4n), then n/(4n^2+1),
      then (n^2+1)/(4n^3+5n), each with alternating sign, shrinks the error at every n tested, by orders of magnitude
  [3] the orders: the errors after the corrections scale like n^-3, n^-5 and n^-7 (ratio of errors at n and 2n)
  [4] the page: prints the numbers above, calls the quotation a paraphrase, separates what Madhava wrote from what
      successors recorded, and says what was not checked

pi is computed here by Machin's formula in 60-digit Decimal, not taken from a library constant.
This script checks that the formulas converge as stated. It does NOT check that Madhava wrote them, nor their dates:
those attributions are cited from the history of mathematics and are not verified here.
Standard library only.  Run:  python3 omega/ch-madhava-verify.py
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
check('Machin pi agrees with the known digits 3.14159265358979323846264338327950288', str(PI).startswith('3.14159265358979323846264338327950288'))
def S(n): return sum(D((-1)**k)/(2*k+1) for k in range(n))
def errs(n):
    s = S(n); sg = (-1)**n
    return (abs(PI/4 - s),
            abs(PI/4 - (s + sg*D(1)/(4*n))),
            abs(PI/4 - (s + sg*D(n)/(4*n*n+1))),
            abs(PI/4 - (s + sg*D(n*n+1)/(4*n**3+5*n))))
tested = (5, 10, 50, 100, 1000)
E = {n: errs(n) for n in tested}
for n in tested:
    check('n=%d: |pi/4 - S_n| < 1/(2n+1)' % n, E[n][0] < D(1)/(2*n+1))
    check('n=%d: error of S_n is within 2%% of 1/(4n)' % n, abs(E[n][0]*4*n - 1) < D('0.02') + D(1)/n)
    check('n=%d: each correction term shrinks the error' % n, E[n][0] > E[n][1] > E[n][2] > E[n][3])
for n in tested:
    print('   n=%-5d  S_n %.3e   +1 term %.3e   +2 terms %.3e   +3 terms %.3e' % ((n,) + tuple(float(x) for x in E[n])))
def order(i, n):
    a, b = errs(n)[i], errs(2*n)[i]
    return float((a/b).ln()/D(2).ln())
for i, want in ((1, 3), (2, 5), (3, 7)):
    o = order(i, 100)
    check('after %d correction term(s) the error falls like n^-%d (measured exponent %.2f)' % (i, want, o), abs(o - want) < 0.1)
page = open(os.path.join(here, 'ch-madhava.html'), encoding='utf-8').read().replace('&nbsp;', ' ')
for n in (10, 100):
    check('page prints the n=%d error after three corrections (%.1e)' % (n, float(E[n][3])), ('%.1e' % float(E[n][3])).replace('e-0', 'e-') in page or ('%.1e' % float(E[n][3])) in page)
check('page calls the English quotation a paraphrase', 'paraphrase' in page.lower())
check('page separates what Madhava wrote from what successors recorded', 'successors' in page.lower() and 'Nilakantha' in page.replace('ī', 'i').replace('ṇ', 'n').replace('ṭ', 't').replace('Nīlakaṇṭha', 'Nilakantha') or 'Nīlakaṇṭha' in page)
check('page lists what was not checked', 'not checked' in page.lower())
print()
print("RESULT:", "ALL PASS" if not FAIL else "FAILURES: %s" % FAIL)
sys.exit(0 if not FAIL else 1)
