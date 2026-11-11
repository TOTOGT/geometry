#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book24/ch11-verify.py -- every check behind book24/ch11-normal-matrices.html. Run first.

    python3 book24/ch11-verify.py

Integers are exact; square roots use 60-digit Decimal and say so. Finite checks are exhaustive within the stated bounds.
Nothing here proves a theorem; the proofs are on the page.

  [1] all 2401 real 2x2 matrices with entries -3..3: normality (A A^T = A^T A) tested exactly; for every normal one
      spectral radius = operator norm and every entry <= spectral radius; for the non-normal ones, how many break the
      entry bound and how many have spectral radius strictly below the norm
  [2] the controls: [[1,t],[0,1]] (spectral radius 1, entry t, norm (t+sqrt(t^2+4))/2 type) and the nilpotent [[0,1],[0,0]]
  [3] real rotations [[a,-b],[b,a]]: normal, no real eigenvalue when b != 0, entries <= spectral radius = sqrt(a^2+b^2)
  [4] 3x3 integer circulants with entries -2..2: normal, every entry <= spectral radius (floating point, tolerance 1e-9)
  [5] the Lean file: statements present, no sorry, labelled uncompiled, no axiom report
  [6] the page: prints the numbers above, says the Lean file is uncompiled, does not claim the convex-hull statement
"""
import itertools, os, re, sys, cmath, math
from decimal import Decimal, getcontext
getcontext().prec = 60
here = os.path.dirname(os.path.abspath(__file__))
ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(('PASS ' if cond else 'FAIL ') + name)
EPS = Decimal(10) ** -45
def sq(x): return Decimal(x).sqrt()
def stats(a, b, c, d):
    """exact normality; rho and norm in 60-digit Decimal"""
    normal = (a*a + b*b == a*a + c*c) and (a*c + b*d == a*b + c*d)   # A A^T = A^T A
    tr, det = a + d, a*d - b*c
    disc = tr*tr - 4*det
    if disc < 0: rho = Decimal(det).sqrt()
    else:
        r = sq(disc); rho = max(abs((Decimal(tr) + r)/2), abs((Decimal(tr) - r)/2))
    F = a*a + b*b + c*c + d*d
    nrm = ((Decimal(F) + sq(F*F - 4*det*det)) / 2).sqrt()
    return normal, rho, nrm, Decimal(max(abs(a), abs(b), abs(c), abs(d)))
# [1]
n_norm = n_non = bad_norm = viol_entry = viol_entry_normal = strict_non = 0
for a, b, c, d in itertools.product(range(-3, 4), repeat=4):
    normal, rho, nrm, mx = stats(a, b, c, d)
    if normal:
        n_norm += 1
        if abs(rho - nrm) > EPS: bad_norm += 1
        if mx > rho + EPS: viol_entry_normal += 1
    else:
        n_non += 1
        if mx > rho + EPS: viol_entry += 1
        if rho < nrm - EPS: strict_non += 1
chk('2401 matrices counted: %d normal + %d not normal' % (n_norm, n_non), n_norm + n_non == 2401)
chk('every normal matrix: spectral radius = operator norm (60-digit decimal)', bad_norm == 0)
chk('every normal matrix: every entry <= spectral radius', viol_entry_normal == 0)
chk('not normal: %d of %d break the entry bound' % (viol_entry, n_non), viol_entry > 0)
chk('not normal: %d of %d have spectral radius strictly below the norm' % (strict_non, n_non), strict_non > 0)
print('   numbers: normal=%d non-normal=%d break-entry=%d radius<norm=%d' % (n_norm, n_non, viol_entry, strict_non))
# [2]
for t in range(2, 8):
    normal, rho, nrm, mx = stats(1, t, 0, 1)
    ok_t = (not normal) and rho == 1 and mx == t and abs(nrm - (Decimal(t) + sq(t*t + 4)) / 2) < EPS and mx > rho
    chk('[[1,%d],[0,1]]: not normal, rho = 1, entry %d > rho, norm = (t+sqrt(t^2+4))/2' % (t, t), ok_t)
normal, rho, nrm, mx = stats(0, 1, 0, 0)
chk('nilpotent [[0,1],[0,0]]: square is zero, rho = 0, norm = 1, entry 1 > 0', (not normal) and rho == 0 and nrm == 1 and mx == 1)
# [3]
rot_ok = rot_noreal = rot_bound = True; nrot = 0
for a, b in itertools.product(range(-5, 6), repeat=2):
    if b == 0: continue
    nrot += 1
    normal, rho, nrm, mx = stats(a, -b, b, a)
    tr, det = 2*a, a*a + b*b
    rot_ok &= normal
    rot_noreal &= (tr*tr - 4*det < 0)
    rot_bound &= (max(abs(a), abs(b))**2 <= det) and abs(rho - nrm) < EPS
chk('%d rotations-with-scaling [[a,-b],[b,a]], b != 0: all normal' % nrot, rot_ok)
chk('same: discriminant negative, so no real eigenvalue at all', rot_noreal)
chk('same: entries <= complex spectral radius sqrt(a^2+b^2) = operator norm', rot_bound)
# [4]
circ_ok = True; ncirc = 0; nnormal = 0
for c0, c1, c2 in itertools.product(range(-2, 3), repeat=3):
    A = [[c0, c1, c2], [c2, c0, c1], [c1, c2, c0]]
    AAt = [[sum(A[i][k]*A[j][k] for k in range(3)) for j in range(3)] for i in range(3)]
    AtA = [[sum(A[k][i]*A[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    ncirc += 1; nnormal += (AAt == AtA)
    w = cmath.exp(2j*math.pi/3)
    rho = max(abs(c0 + c1*w**k + c2*w**(2*k)) for k in range(3))
    circ_ok &= all(abs(x) <= rho + 1e-9 for r in A for x in r)
chk('%d circulants: all normal (exact A A^T = A^T A)' % ncirc, nnormal == ncirc)
chk('same: every entry <= spectral radius', circ_ok)
# [5]
lean = open(os.path.join(here, 'SpectralDiagonalBound.lean'), encoding='utf-8').read()
for name in ('entry_norm_le_opNorm', 'entry_norm_le_of_spectrum_bound', 'diag_norm_le_of_spectrum_bound', 'real_entry_abs_le_of_complex_spectrum_bound'):
    chk('Lean: statement %s present' % name, ('theorem ' + name) in lean)
code = re.sub(r'/-.*?-/', '', lean, flags=re.S)
chk('Lean: no sorry in the code', 'sorry' not in code)
chk('Lean: file labels itself UNCOMPILED', 'UNCOMPILED' in lean)
chk('Lean: no axiom report exists (so nothing is claimed compiled)', not os.path.exists(os.path.join(here, 'spectraldiagonalbound.axioms.txt')))
# [6]
page = open(os.path.join(here, 'ch11-normal-matrices.html'), encoding='utf-8').read()
chk('page prints %d normal, %d not normal' % (n_norm, n_non), ('%d' % n_norm) in page and ('%d' % n_non) in page)
chk('page prints %d break the entry bound and %d have radius below norm' % (viol_entry, strict_non), ('%d' % viol_entry) in page and ('%d' % strict_non) in page)
chk('page says the Lean file is uncompiled', 'uncompiled' in page.lower() and 'compiled by the author' not in page.lower())
chk('page does not claim the convex-hull statement is proved here', 'convex hull' in page.lower() and 'not proved' in page.lower())
chk('page states the complex-spectrum caveat', 'complex spectrum' in page.lower() and 'no real eigenvalue' in page.lower())
print('%d/%d checks passed' % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
