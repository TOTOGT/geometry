#!/usr/bin/env python3
"""ch06_audit_check.py -- read-only checks of Chapter 6 (audit 2026-11-15). Parses the two 6x6 arrays in book4/ch06.html."""
import re, sys, itertools, os
import sympy as sp
bad = 0
def ck(n, ok):
    global bad; bad += (not ok); print(('PASS ' if ok else 'FAIL ') + n)
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, 'ch06.html'), encoding='utf-8', errors='replace').read()
def grab(start):
    i = src.index(start); block = src[i:i+700]
    rows = re.findall(r'\[\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\s*\]', block)[:6]
    return [list(map(int, r)) for r in rows]
# 2026-11-15: the page was corrected (last cell 34 -> 31, fallback removed). The pre-correction arrays are kept here as historical records.
SOLAR_NOW = grab('const SOLAR')
SOLAR = [r[:] for r in SOLAR_NOW]; SOLAR[5][5] = 34
fb = [[1,32,3,34,35,6],[7,11,27,28,8,30],[24,14,16,15,23,19],[13,20,22,21,17,18],[25,29,10,9,26,12],[31,5,33,4,2,36]]
def report(name, sq):
    flat = sorted(x for r in sq for x in r)
    perm = flat == list(range(1, 37))
    rows = [sum(r) for r in sq]; cols = [sum(c) for c in zip(*sq)]
    d1 = sum(sq[i][i] for i in range(6)); d2 = sum(sq[i][5-i] for i in range(6))
    print('INFO', name, 'rows', rows, 'cols', cols, 'diag', d1, d2, 'is permutation of 1..36:', perm)
    return perm, all(s == 111 for s in rows + cols + [d1, d2])
pS, sS = report('SOLAR (primary array)', SOLAR)
pF, sF = report('fallback array', fb)
ck('(historical) pre-correction primary array was NOT a valid magic square (34 repeated, 31 missing; rows/cols/diagonals fail)', not (pS and sS))
ck('(historical) the removed fallback array was ALSO not a valid magic square: columns sum to %s' % [sum(c) for c in zip(*fb)], pF and not sF)
ck('(historical) the page code took the fallback when the primary fails its own check, so the displayed square is not magic', not (pS and sS) and not sF)
# candidate correction: primary array with the final 34 replaced by 31 (the classical Agrippa Sun square)
cand = [r[:] for r in SOLAR_NOW]
pC, sC = report('primary with last cell 34 -> 31', cand)
ck('the CURRENT page array is a valid 6x6 magic square (permutation of 1..36, all rows, columns, both diagonals = 111)', pC and sC)
# arithmetic
ck('M6 = 6*37/2 = 111; total 666 = 6*111 = T(36)', 6*37//2 == 111 and 36*37//2 == 666 == 6*111)
ck('111 = 3*37 and 37 is the 12th prime', 111 == 3*37 and sp.prime(12) == 37)
# magic squares do not have every path/broken diagonal summing to 111: count broken diagonals of the corrected square
bd = [sum(cand[i][(i+k) % 6] for i in range(6)) for k in range(6)] + [sum(cand[i][(k-i) % 6] for i in range(6)) for k in range(6)]
ck('"every path sums to 111" is false: broken diagonals of the corrected square sum to %s' % sorted(set(bd)), set(bd) != {111})
# one cell per row/column, any permutation: not all 111
import random
random.seed(0)
sums = {sum(cand[i][p[i]] for i in range(6)) for p in itertools.islice(itertools.permutations(range(6)), 720)}
ck('transversals (one cell per row and column) take many values, e.g. %d distinct sums' % len(sums), len(sums) > 20)
# Galilean prototype
x, y1, p1, t, v, dx, dy1, dp1, dt = sp.symbols('x y1 p1 t v dx dy1 dp1 dt')
a1 = lambda y, p, DY, DX: DY - p*DX
# pullback by phi_v: y1 -> y1+v t, p1 -> p1+v: d(y1+vt) = dy1 + v dt
pull = a1(y1+v*t, p1+v, dy1 + v*dt, dx)
ck('phi_v^* alpha1 = alpha1 + v (dt - dx)', sp.expand(pull - (dy1 - p1*dx) - v*(dt - dx)) == 0)
pull2 = a1(y1+v*x, p1+v, dy1 + v*dx, dx)
ck('boost y1->y1+vx, p1->p1+v preserves alpha1', sp.expand(pull2 - (dy1 - p1*dx)) == 0)
ck('boosts commute: phi_v o phi_w = phi_{v+w}', sp.simplify((y1+v*t)+sp.Symbol('w')*t - (y1+(v+sp.Symbol('w'))*t)) == 0)
print('NOTE hand argument, not computed: a contact structure (maximally non-integrable hyperplane field) needs an odd-dimensional manifold, so "contact invariants of the 6D extended jet space" (Theorem 6.1) has no contact structure on a 6-manifold to preserve as stated; 16 = 6*5/2+1 is not derived.')
print('NOTE hand argument, not computed: the sum of a magic square depends on the labelling 1..36, not on any geometric structure; no map from 111 to a group invariant is given, so Theorem 6.1\'s "primary invariant" is not a mathematical statement.')
sys.exit(1 if bad else 0)
