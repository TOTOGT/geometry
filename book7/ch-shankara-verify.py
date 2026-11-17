#!/usr/bin/env python3
"""
Shankara -- verifier for book7/ch-shankara.html.

CHECKS (exact arithmetic):
  1. The Sulba-style approximation of sqrt(2): partial sums of 1 + 1/3 + 1/(3*4) - 1/(3*4*34),
     as exact fractions; 577^2 - 2*408^2 = 1; decimals and absolute errors against sqrt(2) to 40 digits.
  2. The rectangle-diagonal rule on four integer triples (3,4,5) (5,12,13) (8,15,17) (7,24,25).
  3. The page's table equals the computed values, the evidence labels are present, and the page
     says which items were not checked.

DOES NOT ESTABLISH: anything about Shankara's life, dates, works or arguments; the Sulba Sutras'
text, authorship or dating; the Kerala results; any dream report; any neural mechanism.
Those items on the page are CITED and were not checked here.

    python3 book7/ch-shankara-verify.py
"""
import os, re, sys
from decimal import Decimal, getcontext
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
getcontext().prec = 40
fails = []
def check(ok, msg):
    print('    %s  %s' % ('PASS' if ok else 'FAIL', msg))
    if not ok: fails.append(msg)
def head(n, t): print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)

head(1, 'THE SULBA-STYLE APPROXIMATION OF SQRT(2), EXACT')
r2 = Decimal(2).sqrt()
terms = [F(1), F(1, 3), F(1, 3 * 4), F(-1, 3 * 4 * 34)]
rows = []
s = F(0)
for k, t in enumerate(terms, 1):
    s += t
    d = Decimal(s.numerator) / Decimal(s.denominator)
    err = abs(d - r2)
    rows.append((k, s, format(d, '.9f'), format(err, '.3e'), s.numerator ** 2 - 2 * s.denominator ** 2))
    print('    terms=%d  %s  = %s  error %s  n^2-2d^2 = %d' % rows[-1])
check(rows[-1][1] == F(577, 408), 'four terms sum to exactly 577/408')
check(F(577, 408) ** 2 - 2 == F(1, 408 ** 2), '(577/408)^2 - 2 = 1/408^2')
check(577 ** 2 - 2 * 408 ** 2 == 1, '577^2 - 2*408^2 = 1 (577/408 solves the Pell equation x^2 - 2y^2 = 1)')
check(Decimal(rows[-1][3]) < Decimal('2.2e-6'), 'error of the four-term value is below 2.2e-6')
check(all(rows[i][3] > rows[i + 1][3] or Decimal(rows[i][3]) > Decimal(rows[i + 1][3]) for i in range(3)),
      'absolute error falls at each added term')

head(2, 'THE RECTANGLE-DIAGONAL RULE ON FOUR INTEGER TRIPLES')
for a, b, c in ((3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)):
    check(a * a + b * b == c * c, '%d^2 + %d^2 = %d^2' % (a, b, c))
check(not (2 * 2 + 3 * 3 == 4 * 4), 'control: (2,3,4) is not a triple')

head(3, "THE PAGE'S TABLE AND LABELS")
html = open(os.path.join(HERE, 'ch-shankara.html'), encoding='utf-8').read()
pr = re.findall(r'<tr data-terms="(\d)" data-frac="([\d/]+)" data-dec="([\d.]+)" data-err="([\d.e+-]+)"', html)
check(len(pr) == 4, 'page table has four rows')
for (k, frac, dec, err), (k2, s2, d2, e2, _) in zip(pr, rows):
    n, d = frac.split('/') if '/' in frac else (frac, '1')
    check(int(k) == k2 and F(int(n), int(d)) == s2 and dec == d2 and err == e2, 'page row %s = computed %s, %s, %s' % (k, s2, d2, e2))
for lab in ('CITED RESULT', 'CHECKED INSTANCE', 'OPEN QUESTION'):
    check(('<b>%s</b>' % lab) in html, 'visible evidence label %s present' % lab)
check('ch-shankara-verify.py' in html, 'page names this verifier')
check('were not checked for this page' in html, 'page states which items were not checked')
check('href="ch-ramanujan.html"' in html, 'link to ch-ramanujan')
check('An older witness' in html and 'Aṅguttara Nikāya 3.65' in html, 'older-witness section cites AN 3.65')
check('Majjhima Nikāya 22' in html and 'Dīgha Nikāya 33' in html, 'older-witness section cites MN 22 and DN 33')
check('Lost in Quotation' in html, 'page records the caution that the Kalama Sutta is often misquoted')
print('\n' + '=' * 70)
if fails:
    print('  %d CHECK(S) FAILED:' % len(fails)); [print('    - ' + f) for f in fails]; sys.exit(1)
print('  ALL CHECKS PASSED')
