#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""polylaminin-verify.py -- companion to book7/Polylaminin.html (Chapter B).

Written 2026-09-29 (R24: the script runs before the sentence). The page carried no script;
its Lean file (AutophagyDm3_v3.lean) is not in this repository and docs/ml-evidence/.../axioms.txt
is empty, so the Lean claims are NOT verified here. What a script can check:

  [1] the page as found (git ref pinned below): the figure caption and the figure code
  [2] the algebra of V(q) = q^3 - 3q (critical points, V'', V(1), the factorisation)
  [3] the figure's own curve: V_k(q) = q^3 - 3q - 2.5 k q  (what is drawn at k = 0 .. 1)
  [4] the contact form alpha = dz - rho^2 dtheta: alpha ^ d alpha = -2 rho (dz ^ drho ^ dtheta)
  [5] the Gronwall arithmetic 2/(2(1+2)) = 1/3, and the page's own patient counts
  [6] the corrected page prints the corrected statement

Prints SKIP, never PASS, when the pinned ref, the page or sympy is missing.
"""
import os, re, subprocess, sys, html
BASELINE = '7cb3891'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = 'book7/Polylaminin.html'
fails, skips = [], []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg, ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def note(s): print('          ' + s)
def head(n, t): print('\n' + '=' * 72 + '\n  [%s]  %s\n' % (n, t) + '=' * 72)
def sq(s): return re.sub(r'\s+', '', html.unescape(re.sub(r'<[^>]+>', ' ', s)).lower())
def raw(s): return re.sub(r'\s+', '', s)

head(1, 'THE PAGE AS FOUND   (git %s)' % BASELINE)
r = subprocess.run(['git', '-C', ROOT, 'show', '%s:%s' % (BASELINE, PAGE)], capture_output=True, text=True, errors='ignore')
if r.returncode != 0:
    print('    SKIP  %s not in this checkout' % BASELINE); skips.append('baseline')
else:
    old = sq(r.stdout); oldraw = raw(r.stdout)
    check('atκ=100%,thesystemcrosseswhitneya₁:v′(q*)=0,v″(q*)≠0,v(q*)=−2' in old, 'as found: caption says that at kappa = 100% V\'(q*) = 0 and V(q*) = -2')
    check('k*2.5*q' in oldraw, 'as found: the figure code draws V = q^3 - 3q - k*2.5*q')
    check('constqstar=1;' in oldraw, 'as found: the figure marker is fixed at q = 1 for every kappa')

try: import sympy as sp
except ImportError: print('    SKIP  sympy missing'); skips.append('sympy'); sp = None
if sp:
    q, k, rho = sp.symbols('q k rho', real=True)
    head(2, 'V(q) = q^3 - 3q')
    V = q**3 - 3*q
    check(sp.diff(V, q).subs(q, 1) == 0, "V'(1) = 0")
    check(sp.diff(V, q, 2).subs(q, 1) == 6, "V''(1) = 6, not zero")
    check(V.subs(q, 1) == -2, 'V(1) = -2')
    check(sp.expand((q - 1)**2 * (q + 2)) == sp.expand(V + 2), 'V + 2 = (q-1)^2 (q+2)')
    crit = sorted(sp.solve(sp.diff(V, q), q))
    check(crit == [-1, 1], 'critical points are q = -1 and q = +1 only')
    note("V''(-1) = %s (a maximum), V''(+1) = %s (a minimum): both are non-degenerate (Morse)" % (sp.diff(V, q, 2).subs(q, -1), sp.diff(V, q, 2).subs(q, 1)))
    d2zero = sp.solve(sp.diff(V, q, 2), q)
    check(d2zero == [0] and sp.diff(V, q).subs(q, 0) == -3, "V'' vanishes only at q = 0, where V' = -3: no critical point is degenerate")
    note('a fold (A2) needs V\' = V\'\' = 0 and V\'\'\' != 0, e.g. q^3 at the origin; V(q) = q^3 - 3q is its unfolding at parameter -3, away from the fold.')
    note('the page\'s condition "V\'(q*) = 0, V\'\'(q*) != 0" is the non-degenerate (Morse) case, which Arnold labels A1; "fold" is A2. Recorded OPEN.')

    head(3, 'THE FIGURE\'S OWN CURVE   V_k(q) = q^3 - 3q - 2.5 k q')
    Vk = q**3 - 3*q - sp.Rational(5, 2) * k * q
    qc = sp.sqrt(sp.Rational(1, 3) * (3 + sp.Rational(5, 2) * k))
    check(sp.simplify(sp.diff(Vk, q).subs(q, qc)) == 0, 'critical point at q = sqrt(1 + 5k/6)')
    for kk in (0, sp.Rational(1, 2), 1):
        v1 = Vk.subs({q: 1, k: kk}); d1 = sp.diff(Vk, q).subs({q: 1, k: kk})
        note('k = %s: V\'(1) = %s, V(1) = %s, critical point q = %.4f, V there = %.4f' % (kk, d1, v1, float(qc.subs(k, kk)), float(Vk.subs(k, kk).subs(q, qc.subs(k, kk)))))
    check(sp.diff(Vk, q).subs({q: 1, k: 1}) == sp.Rational(-5, 2), "at k = 100%: V'(1) = -2.5, not 0")
    check(Vk.subs({q: 1, k: 1}) == sp.Rational(-9, 2), 'at k = 100%: V(1) = -4.5, not -2')
    check(abs(float(qc.subs(k, 1)) - 1.3540) < 1e-3, 'at k = 100% the drawn curve has its minimum at q = 1.354, not at the marker q = 1')
    bif = sp.solve(3 + sp.Rational(5, 2) * k, k)
    check(bif == [sp.Rational(-6, 5)], 'the two critical points merge (the fold of the unfolding) only at k = -1.2')
    note('so over k = 0..1 the tilt moves AWAY from the fold: two non-degenerate critical points throughout; no crossing happens.')
    note('the label "fold crossed" switches at k > 0.5 in the code: a display threshold, not a computed transition.')

    head(4, 'THE CONTACT FORM   alpha = dz - rho^2 dtheta   (coordinates rho, theta, z)')
    # alpha = a_i dx^i ; d alpha = (d_i a_j - d_j a_i) dx^i ^ dx^j /2 ; alpha ^ d alpha coefficient of drho^dtheta^dz
    x = sp.symbols('rho theta z', real=True)
    a = [0, -x[0]**2, 1]
    F = sp.Matrix(3, 3, lambda i, j: sp.diff(a[j], x[i]) - sp.diff(a[i], x[j]))
    from itertools import permutations
    def perm_sign(p):
        s = 1
        for i in range(3):
            for j in range(i + 1, 3):
                if p[i] > p[j]: s = -s
        return s
    coef = sum(perm_sign(p) * a[p[0]] * F[p[1], p[2]] for p in permutations(range(3))) / 2
    coef = sp.simplify(coef)
    note('alpha ^ d alpha = (%s) drho ^ dtheta ^ dz' % coef)
    check(coef == -2 * x[0], 'the coefficient is -2 rho (page: contactCoeff rho = -2 rho), negative for rho > 0')

    head(5, 'GRONWALL ARITHMETIC AND THE PAGE\'S OWN COUNTS')
    check(sp.Rational(2, 2 * (1 + 2)) == sp.Rational(1, 3), '2 / (2 (1 + 2)) = 1/3')
    check(sp.Rational(6, 8) == sp.Rational(3, 4), '6 of 8 = 75%')
    note('NOT checked: any clinical figure (6 of 8; 5 patients; 33 / 38 / 59 patients or decisions; BBB 4.2 -> 8.8), the Lean theorems, and the beta values in section 4.')
    note('The page\'s own dates differ: "~10 court orders by Feb 2026" (table) against "59 judicial decisions as of 11 March 2026" (box). Recorded OPEN.')

head(6, 'THE PAGE AS CORRECTED   (working tree)')
cur = None
try:
    txt = open(os.path.join(ROOT, PAGE), encoding='utf-8').read(); cur = sq(txt)
except OSError: print('    SKIP  page not found'); skips.append('page')
if cur is not None:
    check('atκ=100%,thesystemcrosseswhitneya₁:v′(q*)=0' not in cur, 'the false caption sentence is gone')
    for needle, msg in (('theconditionsv′(q*)=0,v″(q*)≠0,v(q*)=−2holdfortheuntiltedpotential(κ=0)', 'caption: the conditions hold for the untilted potential'),
                        ('v(1)=−4.5', 'caption: V(1) = -4.5 for the drawn curve at kappa = 100%'),
                        ('verificationnote', 'a verification note is on the page')):
        check(needle in cur, 'corrected page: ' + msg)

print('\n' + '=' * 72)
if skips: print('  SKIPPED (not passed, not failed): %s' % ', '.join(skips))
if fails:
    print('  %d FAIL:' % len(fails)); [print('    - ' + f) for f in fails]; sys.exit(1)
print('  all run checks passed.')
print('  Recorded as open, NOT checked here:')
print('   - the Lean file AutophagyDm3_v3.lean is not in this repository (axioms.txt beside the probe is empty): every "proved without sorry" is a claim, WANTED.')
print('   - "Whitney A1 fold": non-degenerate critical point is A1; a fold is A2 (block 2). The falsifiability condition F.B.1 (sigma\' = 0, sigma\'\' != 0) is the Morse case.')
print('   - the model claim that polylaminin "is" Operator F, the mTOR coordinate rho, the Gronwall radius 1/3 as a clinical prediction: MODEL, not derived from data.')
print('   - the beta column in section 4 ("estimated from Menezes 2024 timeline data"): no fit, script or data on the page or beside it; WANTED. The table header names two columns but the rows carry one value.')
print('   - clinical and regulatory facts (Menezes preprint, Chize 2025, PNAS 2009, ANVISA, Lei 13.269/2016, ADI 5501): cited, not held; the box is dated 2026-08-17 and now needs a re-check.')
print('   - the page calls itself Book 3 Chapter B but lives in book7/ (R9; the author decides).')
