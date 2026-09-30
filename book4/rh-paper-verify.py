#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rh-paper-verify.py -- companion to book4/rh-paper.html (source: RH_arithmetic_contact_structure.md).

Written 2026-09-29 (R24). The page is generated from the markdown by tools/build_rh_paper.py, so this
script checks the MARKDOWN as found (git ref pinned below) and as corrected. Uses mpmath and sympy.

  [1] the manuscript as found
  [2] section 2: the prototype forms (alpha = dy + x dx, alpha = dy - g(x,y) dx) on (x, y, t)
  [3] section 4.4: the numbers at gamma_1 (g near the pole, residue, the limit of c)
  [4] section 4.5, Corollary 4.5: c(1/2, t) = theta'(t)
  [5] section 4.5: the two reflection laws, at 40 digits, on the page's own grid
  [6] Proposition 4.2: d_t g has sign changes, so alpha ^ d alpha = 0 on some surfaces
  [7] section 5.2: the local factor g_p against the Euler factor of -zeta'/zeta
  [8] the Lean axiom report beside the page
  [9] the corrected manuscript prints the corrected statements

Prints SKIP, never PASS, when the pinned ref, the source or a library is missing. NOT checked: the Lean
source (not in this checkout), RH, section 6, the p-adic remarks, the citations in section 4.7.
"""
import os, re, subprocess, sys
BASELINE = 'd1e8ad0'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = 'RH_arithmetic_contact_structure.md'
fails, skips = [], []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg, ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def note(s): print('          ' + s)
def head(n, t): print('\n' + '=' * 72 + '\n  [%s]  %s\n' % (n, t) + '=' * 72)
def sq(s): return re.sub(r'\s+', '', s)
try:
    import mpmath as mp, sympy as sp
    from sympy.combinatorics import Permutation
except ImportError:
    print('SKIP  mpmath or sympy missing'); sys.exit(0)
mp.mp.dps = 40

head(1, 'THE MANUSCRIPT AS FOUND   (git %s)' % BASELINE)
r = subprocess.run(['git', '-C', ROOT, 'show', '%s:%s' % (BASELINE, SRC)], capture_output=True, text=True, errors='ignore')
if r.returncode != 0: print('    SKIP  %s not in this checkout' % BASELINE); skips.append('baseline')
else:
    old = sq(r.stdout)
    for needle, msg in (('=g-g\\cdot1=0', 'section 2.2: alpha(gamma-dot) = g - g.1'),
                        ('\\quadd\\alpha=dx\\wedgedy.$$', 'section 2.3: d alpha = dx ^ dy for alpha = dy + x dx'),
                        ('quasi-periodicfunctionthatisdenseandnon-vanishing', 'Prop 4.2: d_t g "dense and non-vanishing"'),
                        ('g_p(t_p)=\\frac{\\logp}{1-p^{-\\sigma}e^{-it_p\\logp}}', 'section 5.2: g_p = log p / (1 - c)'),
                        ('verifiednumericallyto30significantdigits', 'section 4.5: verified to 30 significant digits'),
                        ('maximumdeviation$8.8\\times10^{-16}$', 'status table: maximum deviation 8.8e-16'),
                        ('verifyα∧dα≠0onthecomplementofthezeros'.replace('α∧dα≠0', '$\\alpha_{\\text{arith}}\\wedged\\alpha_{\\text{arith}}\\neq0$'), 'Step 1: non-integrability verified on the complement of the zeros')):
        check(needle in old, 'as found: ' + msg)

head(2, 'SECTION 2: THE PROTOTYPE FORMS ON (x, y, t)')
x, y, t = sp.symbols('x y t', real=True); X = [x, y, t]
def wedge3(a):
    F = sp.Matrix(3, 3, lambda i, j: sp.diff(a[j], X[i]) - sp.diff(a[i], X[j]))
    from itertools import permutations
    def sgn(p): return Permutation(list(p)).signature()
    return sp.simplify(sum(sgn(p) * a[p[0]] * F[p[1], p[2]] for p in permutations(range(3))) / 2), F
c1, F1 = wedge3([x, 1, 0])                              # alpha = dy + x dx
note('alpha = dy + x dx: d alpha components (dx^dy) = %s;  alpha ^ d alpha = %s' % (F1[0, 1], c1))
check(F1[0, 1] == 0 and c1 == 0, 'd(dy + x dx) = 0, so alpha ^ d alpha = 0 (the page has d alpha = dx ^ dy and alpha ^ d alpha = dx ^ dy ^ dt)')
g = sp.Function('g')(x, y)
c2, F2 = wedge3([-g, 1, 0])                             # alpha = dy - g(x,y) dx
check(c2 == 0, 'alpha = dy - g(x,y) dx: alpha ^ d alpha = 0 for every g(x, y): the 3-form has no dt (page: "holds everywhere ... generically non-vanishing")')
f = sp.Function('f')(x, y)
vec = sp.Matrix([f, g, 1]); alpha_on_curve = sp.simplify(1 * g - g * f)   # alpha(gamma') = y' - g x' with x' = f
note('alpha(gamma-dot) = g - g f = %s (page: g - g.1 = 0, which needs f = 1)' % alpha_on_curve)
check(sp.simplify(alpha_on_curve - g * (1 - f)) == 0, 'alpha(gamma-dot) = g(1 - f), zero only where f = 1')
# the section 4 form, where g depends on t
gt = sp.Function('g')(t)
U, V = sp.symbols('U V', real=True)
X2 = [U, V, t]
a2 = [-gt, 1, 0]
F3 = sp.Matrix(3, 3, lambda i, j: sp.diff(a2[j], X2[i]) - sp.diff(a2[i], X2[j]))
from itertools import permutations
c3 = sp.simplify(sum(Permutation(list(p)).signature() * a2[p[0]] * F3[p[1], p[2]] for p in permutations(range(3))) / 2)
note('section 4 form dV - g(t) dU on (U, V, t): alpha ^ d alpha = %s (in dU^dV^dt)' % c3)
check(sp.simplify(c3 + sp.diff(gt, t)) == 0 or sp.simplify(c3 - sp.diff(gt, t)) == 0, 'it is +-(d_t g) dU^dV^dt: non-zero exactly where d_t g != 0 (page Prop 4.2: -(d_t g) dV^dt^dU)')
note('so the smooth prototype of section 2 is not contact as written; the section 4 form is, only because g depends on t. Appendix B row "alpha ^ d alpha != 0 (local, automatic)" is not true for g(x,y).')

head(3, 'SECTION 4.4: THE NUMBERS AT gamma_1')
g1 = mp.zetazero(1).imag
check(abs(g1 - mp.mpf('14.134725141734693790')) < 1e-15, 'gamma_1 = 14.134725141734693790...  (page 14.134725142)')
def lz(s): return mp.zeta(s, derivative=1) / mp.zeta(s)          # zeta'/zeta
def g_(sig, tt): return mp.im(lz(mp.mpc(sig, tt)))               # g = Im(zeta'/zeta) = -Im(-zeta'/zeta)
def c_(sig, tt): return -mp.re(lz(mp.mpc(sig, tt)))              # c = Re(-zeta'/zeta)
page = {1: -10.076, 2: -100.08, 3: -1000.08, 4: -10000.08, 5: -100000.08}
allok = True
for k, want in page.items():
    d = mp.mpf(10) ** (-k); v = g_(0.5, g1 + d); allok &= abs(float(v) - want) < 0.006 * (1 if k == 1 else 1)
    note('delta = 1e-%d: g = %s   (page %s)' % (k, mp.nstr(v, 10), want))
check(allok, 'g(1/2, gamma_1 + delta) matches the five printed values to 3 decimals')
res = mp.mpf(10) ** (-5) * g_(0.5, g1 + mp.mpf(10) ** (-5))
check(abs(res + 1) < 1e-3, 'the pole has residue -1 in g: delta * g -> -1  (%s)' % mp.nstr(res, 8))
cl = c_(0.5, g1 + mp.mpf(10) ** (-12)); note('c at gamma_1 + 1e-12 = %s' % mp.nstr(cl, 10))
check(abs(float(cl) - 0.4052744) < 5e-7, 'c converges to 0.4052744 (page)')

head(4, 'COROLLARY 4.5: c(1/2, t) = theta\'(t)')
def theta_p(tt): return (mp.re(mp.digamma(mp.mpc(0.25, tt / 2))) - mp.log(mp.pi)) / 2
mx = max(abs(c_(0.5, mp.mpf(tt)) - theta_p(mp.mpf(tt))) for tt in (0.7, 3, 9.9, 14.5, 21.02, 25))
note('largest |c - theta\'| over 6 values of t: %s' % mp.nstr(mx, 5))
check(mx < mp.mpf(10) ** -30, 'c(1/2,t) = theta\'(t) to better than 30 digits')
th = lambda tt: mp.siegeltheta(tt)
check(abs(mp.diff(th, mp.mpf('9.9')) - theta_p(mp.mpf('9.9'))) < mp.mpf(10) ** -12, 'and theta\' is the derivative of the Riemann-Siegel theta function (mpmath siegeltheta)')

head(5, 'THE TWO REFLECTION LAWS   (sigma in {0.3,0.5,0.8,1.1,1.5,2.3}, t in [0.7, 25])')
def chi_lg(s): return mp.log(mp.pi) - mp.digamma(s / 2) / 2 - mp.digamma((1 - s) / 2) / 2
tvals = [mp.mpf(v) for v in ('0.7', '1.9', '4.3', '7.7', '11.3', '14.1', '18.2', '21.0', '25')]
mg = mc = mp.mpf(0); n = 0
for sg in ('0.3', '0.5', '0.8', '1.1', '1.5', '2.3'):
    for tt in tvals:
        s = mp.mpc(sg, tt); sg2 = 1 - mp.mpf(sg)
        lhs_g = g_(sg, tt) - g_(sg2, tt); rhs_g = mp.im(chi_lg(s))
        lhs_c = c_(sg, tt) + c_(sg2, tt); rhs_c = -mp.re(chi_lg(s))
        mg = max(mg, abs(lhs_g - rhs_g)); mc = max(mc, abs(lhs_c - rhs_c)); n += 1
note('%d points; largest deviation: g law %s, c law %s' % (n, mp.nstr(mg, 4), mp.nstr(mc, 4)))
check(mg < mp.mpf(10) ** -30 and mc < mp.mpf(10) ** -30, 'both laws hold to better than 30 digits at all %d points (mp.dps = 40)' % n)
note('the page says "30 significant digits" (abstract, 4.5) and, in the status table, "30 digits at eight points ... maximum deviation 8.8e-16"; 8.8e-16 is a 15-digit figure, and the grid is six sigmas, not eight points. Recorded OPEN.')

head(6, 'PROPOSITION 4.2: d_t g CHANGES SIGN')
def gt_(sig, tt):                                                   # d_t g = Re[(zeta'/zeta)'(s)]
    s = mp.mpc(sig, tt); z, z1, z2 = mp.zeta(s), mp.zeta(s, derivative=1), mp.zeta(s, derivative=2)
    return mp.re(z2 / z - (z1 / z) ** 2)
mp.mp.dps = 20
sg = 2; vals = [(k * 0.05, gt_(sg, k * 0.05)) for k in range(0, 1201)]
flips = [(vals[i][0], vals[i + 1][0]) for i in range(len(vals) - 1) if vals[i][1] * vals[i + 1][1] < 0]
note('sigma = 2, t in [0, 60]: d_t g starts at %s and changes sign %d times, first between t = %.2f and %.2f' % (mp.nstr(vals[0][1], 6), len(flips), flips[0][0], flips[0][1]))
check(vals[0][1] > 0 and len(flips) > 5, 'd_t g(2, t) is positive at t = 0 and has several sign changes on [0, 60]')
tz = mp.findroot(lambda tt: gt_(sg, tt), sum(flips[0]) / 2)
check(abs(gt_(sg, tz)) < 1e-12, 'a zero of d_t g at sigma = 2, t = %s: there alpha ^ d alpha = 0' % mp.nstr(tz, 8))
partial = mp.nsum(lambda n: mp.log(n) * mp.mangoldt(int(n)) * mp.cos(1 * mp.log(n)) / n ** 2, [1, 20000]) if False else None
mp.mp.dps = 40
note('so "alpha ^ d alpha != 0 everywhere" (section 3.2 condition 2; Step 1; Conj 6.1 "contradiction with maximal non-integrability") cannot hold: it fails on the zero set of d_t g, at any sigma. Recorded OPEN.')

head(7, 'SECTION 5.2: THE LOCAL FACTOR')
s_, p_, L = sp.symbols('s p L', positive=True); tp, sig = sp.symbols('t_p sigma', real=True)
Ep = 1 / (1 - p_ ** (-s_))                                      # local Euler factor
loc = sp.simplify(-sp.diff(sp.log(Ep), s_))                     # -zeta_p'/zeta_p
cc = p_ ** (-s_)
check(sp.simplify(loc - sp.log(p_) * cc / (1 - cc)) == 0, "-zeta_p'/zeta_p = log p . c / (1 - c),  c = p^-s")
check(sp.simplify(sp.log(p_) / (1 - cc) - loc - sp.log(p_)) == 0, 'the page\'s log p / (1 - c) exceeds it by exactly log p (the k = 0 term)')
cs = sp.symbols('c', positive=True); Tt = sp.symbols('T')
cT = p_ ** (-sig) * sp.exp(-sp.I * Tt * sp.log(p_))
d_page = sp.simplify(sp.diff(sp.log(p_) / (1 - cT), Tt) - (-sp.I * sp.log(p_) ** 2 * cT / (1 - cT) ** 2))
d_true = sp.simplify(sp.diff(sp.log(p_) * cT / (1 - cT), Tt) - (-sp.I * sp.log(p_) ** 2 * cT / (1 - cT) ** 2))
check(d_page == 0 and d_true == 0, 'd/dt of either form = -i (log p)^2 c / (1-c)^2: section 5.3 is unchanged by the constant')
note('not addressed: g_p is complex here while g at infinity is an imaginary part; e^{-i t_p log p} for t_p in Q_p has no meaning in Q_p; the p-adic norm remarks are not checked.')

head(8, 'THE LEAN AXIOM REPORT BESIDE THE PAGE')
ax = os.path.join(ROOT, 'tools/verify-audit/2026-09-08/ZetaReflection.axioms.txt')
if not os.path.exists(ax): print('    SKIP  axiom report missing'); skips.append('axioms')
else:
    lines = [l for l in open(ax, encoding='utf-8') if 'depends on axioms' in l]
    bad = [l for l in lines if 'sorryAx' in l]
    ok_ax = all(re.search(r'\[(propext|Classical\.choice|Quot\.sound)(, (propext|Classical\.choice|Quot\.sound))*\]', l) for l in lines)
    note('%d declarations reported; sorryAx in %d; every report within {propext, Classical.choice, Quot.sound}: %s' % (len(lines), len(bad), ok_ax))
    check(len(bad) == 0 and ok_ax, 'the report names no sorryAx and no axiom beyond the three standard ones')
    check(len(lines) >= 16, 'at least 16 declarations are reported (page: "18 theorems")')
    for nm in ('reflection_law', 'Zlog_add_Zlog_one_sub', 'chiLog_real_on_critical_line', 'logDeriv_Gammaℝ', 'gCoef_odd_in_t', 'cCoef_even_in_t', 'lseries_vonMangoldt_eq_neg_Zlog'):
        check(any(nm in l for l in lines), 'the report contains ' + nm)
    note('book4/ZetaReflection.lean itself is not in this checkout: the report is a receipt for a file I cannot read; the theorem statements are WANTED.')

head(9, 'THE CORRECTED MANUSCRIPT   (working tree)')
try: cur = sq(open(os.path.join(ROOT, SRC), encoding='utf-8').read())
except OSError: print('    SKIP  source not found'); skips.append('src'); cur = None
if cur is not None:
    for needle, msg in (('real-analyticin$t$andnotidenticallyzero', 'Prop 4.2: d_t g real-analytic in t, not identically zero, and it changes sign'),
                        ('g_p(t_p)=\\frac{\\logp\\;p^{-\\sigma}e^{-it_p\\logp}}{1-p^{-\\sigma}e^{-it_p\\logp}}', 'section 5.2: g_p = log p . c / (1 - c)'),
                        ('###4.8Editor\'sverificationnote', 'section 4.8 verification note'),
                        ('thatisdenseandnon-vanishing', None)):
        if msg is None: check(needle not in cur, 'the sentence "... that is dense and non-vanishing" is gone'); continue
        check(needle in cur, 'corrected: ' + msg)

try: htm = sq(open(os.path.join(ROOT, 'book4/rh-paper.html'), encoding='utf-8').read().replace('&#x27;', "'"))
except OSError: htm = None
if htm is not None:
    for needle, msg in (('real-analyticin$t$andnotidenticallyzero', 'HTML: Prop 4.2 corrected'),
                        ('\\frac{\\logp\\;p^{-\\sigma}e^{-it_p\\logp}}{1-p^{-\\sigma}e^{-it_p\\logp}}', 'HTML: g_p corrected'),
                        ('4.8Editor', 'HTML: section 4.8 present')):
        check(needle in htm, msg)
    check('thatisdenseandnon-vanishing' not in htm, 'HTML: the "dense and non-vanishing" sentence is gone')

print('\n' + '=' * 72)
if skips: print('  SKIPPED (not passed, not failed): %s' % ', '.join(skips))
if fails:
    print('  %d FAIL:' % len(fails)); [print('    - ' + f) for f in fails]; sys.exit(1)
print('  all run checks passed.')
print('  Recorded as open, NOT checked here:')
print('   - the Lean source book4/ZetaReflection.lean and ZetaFELogDeriv.lean are not in this checkout; the axiom report is a receipt only.')
print('   - Conjecture 6.1, Weil/Connes comparisons (7.1, 7.2): the "morally identical" and "Reeb vector field = our Reeb flow" statements are analogies, not derivations.')
print('   - the citations of section 4.7 (Anthropic 2026-08-11, Baluyot et al. arXiv:2306.04799, Lamzouri arXiv:2609.02882, Pratt et al.): cited, not read here; Lamzouri 2609.02882 and the Anthropic page exist (web search 2026-09-29, titles only). Search listings also show later arXiv items (2609.07918, 2609.24167, 2609.33043) dated after version 3: not read.')
print('   - "Proposition 4.6", the contactomorphism refutation, is argued not proved; "Step 3" in section 8 predates section 4.5 (the involution is s -> 1 - conj(s), not sigma -> 1 - sigma alone).')
