#!/usr/bin/env python3
"""
GCM framework -- the contact form is Gibbs's, minus the heat term.

[1] checks the substitution numerically rather than asserting it. alpha_G =
dU - T dS - Omega dJ at dS = 0, against alpha_cat = dz - r^2 dtheta under
z = U, theta = J, r^2 = Omega. Random values, many trials: if the two forms
disagree anywhere on a tangent vector, this finds it.

[2] recomputes the corpus counts the page cites instead of quoting them. The
2026-09-06 audit recorded Gibbs in 1 file, Carnot in 1, Legendre transform in
0, against contact form and Reeb in 164 each. Quoted numbers rot; these are
re-derived, printed beside the recorded ones, and the drift is reported.

[3] reads the page back: the wrong attribution is gone, Lie is named, and the
identification is present with its consequence rather than as a slogan.

Standard library only.  python3 gcm-framework-verify.py
"""
import os, re, sys, random

fails = []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg, ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def head(n, t):
    print('\n' + '=' * 68 + '\n  [%s]  %s\n' % (n, t) + '=' * 68)

ROOT = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(ROOT, 'gcm-framework.html')

# ==========================================================================
head(1, 'THE SUBSTITUTION, CHECKED ON RANDOM TANGENT VECTORS')
print("  alpha_G(dU,dS,dJ) = dU - T*dS - Omega*dJ, evaluated at dS = 0")
print("  alpha_cat(dz,dtheta) = dz - r^2*dtheta,  with z=U, theta=J, r^2=Omega\n")
random.seed(20260920)
worst = 0.0
for _ in range(200000):
    T, Om = random.uniform(-9, 9), random.uniform(-9, 9)
    dU, dJ = random.uniform(-9, 9), random.uniform(-9, 9)
    a_G = dU - T * 0.0 - Om * dJ          # dS = 0
    r2, dz, dth = Om, dU, dJ
    a_cat = dz - r2 * dth
    worst = max(worst, abs(a_G - a_cat))
print('      worst disagreement over 200000 random tangent vectors: %.3e' % worst)
check(worst == 0.0, 'the two forms agree exactly under the substitution')

# and the heat term is the whole difference: at dS != 0 they must differ by T*dS
diffs_ok = True
for _ in range(50000):
    T, Om = random.uniform(-9, 9), random.uniform(-9, 9)
    dU, dS, dJ = random.uniform(-9, 9), random.uniform(-9, 9), random.uniform(-9, 9)
    a_G = dU - T * dS - Om * dJ
    a_cat = dU - Om * dJ
    if abs((a_cat - a_G) - T * dS) > 1e-9:
        diffs_ok = False; break
check(diffs_ok, 'off the adiabat the two differ by exactly T dS -- the deleted term')
print("\n      So alpha_cat is not LIKE the Gibbs form. It is the Gibbs form with")
print("      one term removed, and the removed term is the heat.")

# ==========================================================================
head(2, 'THE CORPUS COUNTS, RECOMPUTED')
RECORDED = {'Gibbs': 1, 'Carnot': 1, 'Legendre transform': 0,
            'contact form': 164, 'Reeb': 164}
def files_with(word):
    n = 0
    for root, dirs, fs in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in ('.git', '_to_delete', '_archive')]
        for f in fs:
            if not f.endswith('.html'): continue
            try:
                if word in open(os.path.join(root, f), encoding='utf-8', errors='replace').read():
                    n += 1
            except OSError:
                pass
    return n
print('      term                  2026-09-06   today   drift')
for w, rec in RECORDED.items():
    now = files_with(w)
    print('      %-20s %7d %9d   %+d' % (w, rec, now, now - rec))
check(files_with('Gibbs') > RECORDED['Gibbs'],
      'Gibbs is no longer in one file only -- the name has spread since the audit')
check(files_with('contact form') > 100,
      'the structure is still everywhere, which was the point')

# ==========================================================================
head(3, 'THE PAGE')
if not os.path.exists(PAGE):
    check(False, 'gcm-framework.html present', PAGE)
else:
    raw = open(PAGE, encoding='utf-8').read()
    # Strip the correction box before scanning. It QUOTES the wrong sentence in
    # order to retract it, and a scanner that reads the quotation as the claim
    # fails the page for having been corrected. Fifth time today.
    body = re.sub(r'<div style="[^"]*background:#fdeaea[^"]*">.*?</div>', ' ', raw, flags=re.S)
    flat = re.sub(r'<[^>]+>', ' ', body)
    flat = re.sub(r'\s+', ' ', flat)
    check('introduced by Gibbs' not in flat,
          'the page no longer ASSERTS that contact geometry was introduced by Gibbs')
    check('introduced by Gibbs' in raw,
          'and the retraction still quotes the sentence it retracts')
    check('Sophus Lie' in flat, 'Lie is named as the origin')
    check('reappearing in Gibbs' in flat or 'reappeared in Gibbs' in flat,
          "and Gibbs's actual role is stated -- it reappeared in his thermodynamics")
    check('adiabat' in flat.lower(),
          'the consequence is present: the Legendrian submanifolds are adiabats')
    check('dS = 0' in flat or 'dS = 0' in raw, 'the condition is written out')
    check('subtraction' in flat.lower(),
          'and the identification is stated as a subtraction -- what the framework leaves out')

# ==========================================================================
print('\n' + '=' * 68)
if fails:
    print('  %d FAILED' % len(fails))
    for f in fails: print('    - ' + f)
    sys.exit(1)
print('  ALL CHECKS PASSED')
print('=' * 68)
