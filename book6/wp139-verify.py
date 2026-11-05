#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""wp139-verify.py -- companion to book6/wp139-two-convex-curves-money-inflation-phillips.html. Written 2026-11-05.
RECOMPUTED here: the identity example, the three policy points for the INVENTED curve p = a + b m^2, the Phillips fitted-curve values.
READ FROM THE PDFS: Phillips y + 0.900 = 9.638 x^-1.394 (printed); Colwell's shape claims and the ordering of his rules (his claims).
NOT CHECKED: any estimation in Colwell; Phillips's data; Gagnon and Collins beyond the abstract."""
import html as _h, re
from math import log10, sqrt
from pathlib import Path
fails = []
def check(ok, msg):
    print('    %s  %s' % ('PASS' if ok else 'FAIL', msg))
    if not ok: fails.append(msg)
def head(n, t): print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)
PAGE = Path(__file__).resolve().parent / 'wp139-two-convex-curves-money-inflation-phillips.html'
raw = PAGE.read_text(encoding='utf-8') if PAGE.exists() else ''
txt = re.sub(r'\s+', ' ', _h.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)[^>]*>.*?</\1>', '', raw, flags=re.S))))

head(1, 'identity example')
nom = 1.06 * 1.01 - 1; q = 1.06 * 1.01 / 1.03 - 1
check(abs(nom - 0.0706) < 1e-12, 'nominal growth 7.06%')
check(abs(q - 0.0394) < 5e-5, 'real growth 3.94%')
check(abs((0.06 + 0.01 - 0.03) - 0.04) < 1e-12 and abs(q - 0.04 - (-0.0006)) < 1e-4, 'additive rule 4.00%, gap about 0.06 points')

head(2, 'invented curve p = a + b m^2, a=0.02, b=2.5')
a, b = 0.02, 2.5
p = lambda m: a + b * m * m
g = lambda m: m - p(m)
ratio = lambda m: g(m) / p(m)
m1, m2, m3 = sqrt(a / b), 1 / (4 * b), 1 / (2 * b)
grid = [i / 100000 for i in range(1, 60000)]
check(abs(max(grid, key=ratio) - m1) < 2e-5, 'ratio maximiser = sqrt(a/b) = 0.0894 (grid)')
check(abs(max(grid, key=lambda m: g(m) - p(m)) - m2) < 2e-5, 'net-benefit maximiser = 1/(4b) = 0.1 (grid)')
check(abs(max(grid, key=g) - m3) < 2e-5, 'growth maximiser = 1/(2b) = 0.2 (grid)')
check(m1 < m2 < m3 and a * b < 1 / 16, 'ordering ratio < net < growth, with a*b < 1/16')
check((round(p(m1), 4), round(g(m1), 4)) == (0.0400, 0.0494), 'row 1: p 0.0400, q 0.0494')
check((round(p(m2), 4), round(g(m2), 4)) == (0.0450, 0.0550), 'row 2: p 0.0450, q 0.0550')
check((round(p(m3), 4), round(g(m3), 4)) == (0.1200, 0.0800), 'row 3: p 0.1200, q 0.0800')
check(not (16 * 0.3 * 1 < 1) , 'control: with a=0.3, b=1 (a*b > 1/16) the ordering condition fails, sqrt(a/b) > 1/(4b)') 
check(sqrt(0.3) > 1 / 4, 'control: confirm the failing case directly')

head(3, 'Phillips fitted curve as printed')
B, C, A = 9.638, 1.394, 0.900
y = lambda x: B * x ** (-C) - A
check(abs(log10(B) - 0.984) < 5e-4, 'log10 9.638 = 0.984 (the two printed forms agree)')
check(abs((B / A) ** (1 / C) - 5.48) < 0.005, 'y = 0 at x = 5.48')
for x, v in [(2, 2.77), (4, 0.50), (6, -0.11), (8, -0.37), (10, -0.51)]:
    check(abs(y(x) - v) < 0.005, 'y(%d) = %.2f' % (x, v))
check(abs((y(2) - y(3)) - 1.58) < 0.005 and abs((y(8) - y(9)) - 0.08) < 0.005, 'fall 2 to 3 is 1.58; fall 8 to 9 is 0.08')
check(all(y(x) > -A for x in (10, 50, 500)), 'y stays above -0.9 for every x')
check(abs(y(5.48)) < 0.01 and y(5.0) > 0 > y(6.0), 'control: sign change between x = 5 and 6')

head(4, 'page carries the numbers and the honesty statements')
for s in ['7.06%', '3.94%', '0.0894', '0.1000', '0.2000', '0.0494', '5.48%', '9.638', '1.394', '0.900', '1.58', 'ln(p + 0.025)', 'a&middot;b']:
    check(s in raw or s in txt, 'page carries ' + s)
check('shared functional form, not a shared invariant' in txt.lower(), 'states: shared functional form, not a shared invariant')
check('not reproduced' in txt, 'says Colwell results were not reproduced')
check('invented' in txt, 'says the curve numbers are invented')
check('Gagnon' in txt and 'abstract and introduction only' in txt, 'says Gagnon and Collins read only in part')
check('not investment' in txt.lower(), 'not investment advice')
print('\n' + ('ALL PASS' if not fails else 'FAILED %d' % len(fails)))
raise SystemExit(1 if fails else 0)
