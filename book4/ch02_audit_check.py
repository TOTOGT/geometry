#!/usr/bin/env python3
"""ch02_audit_check.py -- read-only checks of Chapter 2 (audit 2026-11-15). sympy exterior-algebra computations by hand-coded wedge."""
import sys, sympy as sp
from sympy.combinatorics import Permutation
bad = 0
def ck(n, ok):
    global bad; bad += (not ok); print(('PASS ' if ok else 'FAIL ') + n)
x, y, t, p = sp.symbols('x y t p')
def d(form, coords):  # 1-form as dict {i: coeff} -> 2-form dict {(i,j): coeff}, i<j
    out = {}
    for i, ci in form.items():
        for j, c in enumerate(coords):
            dc = sp.diff(ci, c)
            if dc == 0 or j == i: continue
            k, sgn = ((j, i), 1) if j < i else ((i, j), -1)
            out[k] = out.get(k, 0) + sgn*dc
    return out
def wedge13(a, b2, n):  # 1-form ^ 2-form coefficient of dx^dy^dt style 3-form (n=3)
    tot = 0
    for i, ai in a.items():
        for (j, k), c in b2.items():
            if len({i, j, k}) == 3:
                perm = [i, j, k]; sgn = Permutation(perm).signature()
                tot += sgn*ai*c
    return sp.simplify(tot)
f = sp.Function('f')
# coordinates (x,y,t) = indices 0,1,2.  alpha = dy - f(x,y) dx
al = {1: 1, 0: -f(x, y)}
ck('alpha = dy - f(x,y)dx on (x,y,t): alpha^dalpha = 0 (integrable, NOT contact)', wedge13(al, d(al, [x, y, t]), 3) == 0)
al_t = {1: 1, 0: -f(x, y, t)}
w = wedge13(al_t, d(al_t, [x, y, t]), 3)
ck('with f depending on t: alpha^dalpha = +-f_t dx^dy^dt (nonzero iff f_t != 0)', sp.simplify(w**2 - sp.diff(f(x, y, t), t)**2) == 0 and w != 0)
# J^1(R,R): coords (x,y,p): alpha = dy - p dx
aj = {1: 1, 0: -p}
wj = wedge13(aj, d(aj, [x, y, p]), 3)
ck('J^1: alpha = dy - p dx has alpha^dalpha = +-dx^dy^dp (nonzero): contact lives on the jet space with slope as a coordinate', wj != 0)
# oscillator rescaled form
ab = {0: x, 1: y}
ck('x dx + y dy is closed (= d(r^2/2)): d(alpha~) = 0, so it is a first integral, not a contact form', all(sp.simplify(c) == 0 for c in d(ab, [x, y, t]).values()))
ck('x dx + y dy has alpha^dalpha = 0 on (x,y,t)', wedge13(ab, d(ab, [x, y, t]), 3) == 0)
# helix is a solution and tangent to ker alpha~
g = (sp.cos(t), -sp.sin(t), t)
gd = [sp.diff(c, t) for c in g]
ck('helix (cos t, -sin t, t) solves xdot=y, ydot=-x and alpha~(gamma dot)=0', sp.simplify(gd[0] - g[1]) == 0 and sp.simplify(gd[1] + g[0]) == 0 and sp.simplify(g[0]*gd[0] + g[1]*gd[1]) == 0)
print('NOTE hand argument, not computed: alpha has no dt component, so the vertical line (x0,y0,t) is tangent to ker(alpha); "a curve is a solution iff tangent to ker alpha" therefore fails on (x,y,t).')
print('NOTE hand argument, not computed: J^0(R,R) is (x,y)=R^2 and J^1(R,R) is (x,y,p)=R^3; the page writes J^0(R,R)=R^3.')
print('NOTE hand argument, not computed: ch01 writes the occupied state as psi=1; psi is an odd generator and 1 is even, so "psi in {0,1}" is a heuristic about occupation numbers, not a statement about the Grassmann algebra Lambda(psi) = {a + b psi}.')
sys.exit(1 if bad else 0)
