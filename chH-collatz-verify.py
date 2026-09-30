#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""chH-collatz-verify.py -- companion to Observation 4 of chH-collatz.html (Base 12, Base 60, and the Ulam Spiral).

Written 2026-09-29 (R24). The page said the Dual Ulam Spiral's mod-6 mode shows "diagonals of constant residue".
It also states the LCMs and the odd-orbit transition table as exhaustively checked; this script re-runs those.

  [1] the page as found (git ref pinned below)
  [2] the LCMs: 12 = LCM(1..4), 60 = LCM(1..5) = LCM(1..6)
  [3] the odd-orbit table over all odd n < 10^5 (3n+1 with the factors of 2 removed), and residue 3 never produced
  [4] primes greater than 3 are +-1 mod 6
  [5] the diagonals of the page's Ulam spiral (book7/ulam-dual.html, spiral ported line for line): parity and residue mod 6
  [6] the corrected page

Prints SKIP, never PASS, when the pinned ref or the page is missing. Not checked: "shared cause" (the page says it is not offered).
"""
import math, os, re, subprocess, sys, html
from collections import defaultdict
BASELINE = '36d30dc'
ROOT = os.path.dirname(os.path.abspath(__file__))
PAGE = 'chH-collatz.html'
fails, skips = [], []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg, ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def note(s): print('          ' + s)
def head(n, t): print('\n' + '=' * 72 + '\n  [%s]  %s\n' % (n, t) + '=' * 72)
def sq(s): return re.sub(r'\s+', '', html.unescape(re.sub(r'<[^>]+>', ' ', s)).lower())

head(1, 'THE PAGE AS FOUND   (git %s)' % BASELINE)
r = subprocess.run(['git', '-C', ROOT, 'show', '%s:%s' % (BASELINE, PAGE)], capture_output=True, text=True, errors='ignore')
if r.returncode != 0: print('    SKIP  %s not in this checkout' % BASELINE); skips.append('baseline')
else:
    check('thediagonalsalongwhichprimesconcentrateare' + 'diagonalsofconstantresidue' in sq(r.stdout), 'as found: "the diagonals along which primes concentrate are diagonals of constant residue"')

head(2, 'THE LCMS')
def lcm(*a):
    r_ = 1
    for x in a: r_ = r_ * x // math.gcd(r_, x)
    return r_
check(lcm(1, 2, 3, 4) == 12 and lcm(1, 2, 3, 4, 5) == 60 and lcm(1, 2, 3, 4, 5, 6) == 60, 'LCM(1..4) = 12, LCM(1..5) = LCM(1..6) = 60')

head(3, 'THE ODD-ORBIT TABLE, ALL ODD n < 10^5')
def succ(n):
    m = 3 * n + 1
    while m % 2 == 0: m //= 2
    return m
tab = {1: set(), 3: set(), 5: set()}
for n in range(1, 100000, 2): tab[n % 6].add(succ(n) % 6)
note('n mod 6 -> odd-succ(n) mod 6: %s' % {k: sorted(v) for k, v in tab.items()})
check(all(v <= {1, 5} for v in tab.values()), 'every residue class maps into {1, 5}')
check(all(3 not in v for v in tab.values()), 'residue 3 is never produced')
check(all(succ(n) % 3 != 0 for n in range(3, 100000, 6)), '3 | n implies 3n+1 = 1 (mod 3): the factor 3 is lost')

head(4, 'PRIMES GREATER THAN 3 ARE +-1 MOD 6')
N = 10 ** 6; c = bytearray(N + 1)
for i in range(2, int(N ** .5) + 1):
    if not c[i]:
        for j in range(i * i, N + 1, i): c[j] = 1
pr = [n for n in range(5, N + 1) if not c[n]]
check(all(n % 6 in (1, 5) for n in pr), 'all %d primes from 5 to 10^6 are 1 or 5 mod 6' % len(pr))

head(5, 'DIAGONALS OF THE PAGE\'S ULAM SPIRAL   (101 x 101; buildSpiral ported from book7/ulam-dual.html)')
def spiral(N):
    pos = [None] * (N * N + 1); x = y = N // 2; dx, dy = 0, -1; steps = 1; sc = 0; tc = 0
    for n in range(1, N * N + 1):
        pos[n] = (x, y); x += dx; y += dy; sc += 1
        if sc == steps:
            sc = 0; dx, dy = -dy, dx; tc += 1
            if tc % 2 == 0: steps += 1
    return pos
Ng = 101; p = spiral(Ng); cc = Ng // 2; D = defaultdict(list)
for n in range(1, Ng * Ng + 1):
    u, v = p[n][0] - cc, p[n][1] - cc
    D[('d', u - v)].append(n); D[('a', u + v)].append(n)
big = [l for l in D.values() if len(l) > 5]
m2 = sum(len(set(m % 2 for m in l)) == 1 for l in big); m6 = sum(len(set(m % 6 for m in l)) == 1 for l in big)
note('%d diagonals with more than 5 cells; constant parity on %d of them; constant residue mod 6 on %d' % (len(big), m2, m6))
check(m2 == len(big), 'every diagonal has constant parity')
check(m6 == 0, 'no diagonal has constant residue mod 6 (the main diagonal runs through 1, 5, 9, 17, 25, 37, 49, ... : residues %s)' % sorted(set(m % 6 for m in D[('d', 0)])))
check(len(set(m % 6 for m in D[('d', 0)])) >= 3, 'the main diagonal alone carries at least three residues mod 6')

head(6, 'THE PAGE AS CORRECTED   (working tree)')
try: cur = sq(open(os.path.join(ROOT, PAGE), encoding='utf-8').read())
except OSError: print('    SKIP  page not found'); skips.append('page'); cur = None
if cur is not None:
    check('diagonalsofconstantresidue' not in cur.replace('notdiagonalsofconstantresidue', ''), 'the false statement is gone')
    check('alongany diagonaltheparityisconstant'.replace(' ', '') in cur, 'corrected: parity is constant along a diagonal')

print('\n' + '=' * 72)
if skips: print('  SKIPPED (not passed, not failed): %s' % ', '.join(skips))
if fails:
    print('  %d FAIL:' % len(fails)); [print('    - ' + f) for f in fails]; sys.exit(1)
print('  all run checks passed.')
print('  Not checked: the rest of Observation 4 (WP-45, WP-46 references, "shared cause"), and the other observations on the page.')
