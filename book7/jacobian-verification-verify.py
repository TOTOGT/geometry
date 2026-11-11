#!/usr/bin/env python3
"""Verify the Jacobian-conjecture counterexample claims on
book7/jacobian-verification.html (WP60), by exact arithmetic over Q.

Written 2026-11-11 (R24: the script ran before the correction box was written).
Needs sympy:  pip install sympy
Checks (1) the map printed on the page, (2) the map in Gao, arXiv:2608.00222
Thm 3.3 (Alpoge's example), and (3) controls that must fail.
Exit code 0 only if every expectation below holds.
"""
import sys
from sympy import symbols, Matrix, diff, expand, Rational as R

x, y, z = symbols('x y z')
V = (x, y, z)

def det_jac(F):
    return expand(Matrix(3, 3, lambda i, j: diff(F[i], V[j])).det())

def at(F, p):
    return tuple(f.subs(dict(zip(V, p))) for f in F)

# (1) the map as printed on the WP60 page
page = [(1+x*y)**3*z + y**2*(1+x*y)*(4+3*x*y), -(1+x*y)**4, x]
page_pts = [(-2, R(1, 2), R(-3, 4)), (-2, -1, 3), (-2, -4, R(3, 4))]

# (2) Alpoge's map in Gao's expanded form (Thm 3.3)
f1 = (1+x*y)**3*z + y**2*(1+x*y)*(4+3*x*y)
f2 = y + 3*x*(1+x*y)**2*z + 3*x*y**2*(4+3*x*y)
f3 = 2*x - 3*x**2*y - x**3*z
gao = [f1, f2, f3]
gao_pts = [(0, 0, R(-1, 4)), (1, R(-3, 2), R(13, 2)), (-1, R(3, 2), R(13, 2))]

fails = 0
def expect(label, ok):
    global fails
    print(('PASS ' if ok else 'FAIL ') + label)
    fails += (not ok)

d_page, d_gao = det_jac(page), det_jac(gao)
img_page = [at(page, p) for p in page_pts]
img_gao = [at(gao, p) for p in gao_pts]

print('page map: det =', d_page)
print('page map images:', img_page)
print('Gao map: det =', d_gao, ' images:', img_gao)

expect('Gao/Alpoge map: det Jac == -2', d_gao == -2)
expect('Gao/Alpoge map: three distinct points share one image',
       len(set(gao_pts)) == 3 and len(set(img_gao)) == 1)
# The printed map is wrong; the page now says so (correction box). These two lines
# pin the defect: if someone 'fixes' the arithmetic claim they must change this too.
expect('page map: det Jac is NOT the constant -2 (defect documented in the correction box)',
       d_page != -2)
expect('page map: its three points do NOT share one image (defect documented)',
       len(set(img_page)) != 1)
html = open(__file__.rsplit('/', 1)[0] + '/jacobian-verification.html', encoding='utf-8').read() if '/' in __file__ else open('jacobian-verification.html', encoding='utf-8').read()
expect('page carries the 2026-11-11 correction box', 'id="correction-2026-11-11"' in html)
# controls: the checks above must be able to fail
bad = [f1, f2, f3 + 1 + x]
expect('control: a perturbed map is NOT det -2', det_jac(bad) != -2)
expect('control: a wrong point does NOT collide',
       at(gao, (0, 0, R(-1, 3))) != img_gao[0])
print('FAILS:', fails)
sys.exit(0 if fails == 0 else 1)
