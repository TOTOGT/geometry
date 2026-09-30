#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""chIV-15-verify.py -- companion to book4/chIV-15.html (Cap IV-15, A Virada Complexa / The Complex Turn).

Written 2026-09-29 (R24). The chapter is a block list in JavaScript (PT primary, EN and six partial translations).
It announces Theorems 15.1-15.2 without proof and carries three "Lean 4" badges; what a script can check is the
ladder of algebras (section 1), the arithmetic J = Psi/lambda, the dimension of any J with J^2 = -id, and the
page's own structure.

  [1] the page as found (git ref pinned below)
  [2] the Cayley-Dickson ladder: where each property is lost (dimensions 1, 2, 4, 8, 16, 32)
  [3] J^2 = -id: only in even dimension (odd: det argument); Psi^2 = -lambda^2 id gives J^2 = -id
  [4] the page's own structure: languages, blocks per language, badges
  [5] the corrected page

Prints SKIP, never PASS, when the pinned ref, the page or node is missing. Not checked: Theorems 15.1, 15.2 (announced), the Lean
files (not in this checkout), F and T as operators (F is a map M -> M and T a vector field: [F,T] as written needs a definition).
"""
import itertools, json, math, os, random, re, subprocess, sys
BASELINE = '1113366'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = 'book4/chIV-15.html'
fails, skips = [], []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg, ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def note(s): print('          ' + s)
def head(n, t): print('\n' + '=' * 72 + '\n  [%s]  %s\n' % (n, t) + '=' * 72)
def read_page(ref=None):
    if ref:
        r = subprocess.run(['git', '-C', ROOT, 'show', '%s:%s' % (ref, PAGE)], capture_output=True, text=True, errors='ignore')
        return r.stdout if r.returncode == 0 else None
    try: return open(os.path.join(ROOT, PAGE), encoding='utf-8').read()
    except OSError: return None
def blocks(src):
    m = re.search(r'<script>\s*(const PT = \[.*?)</script>', src, flags=re.S)
    if not m: return None
    js = m.group(1); js = js[:js.index('function renderBlocks')] + '\nprocess.stdout.write(JSON.stringify({PT:PT,TR:Object.fromEntries(Object.entries(TR).map(function(e){return [e[0],e[1].blocks]}))}));'
    r = subprocess.run(['node', '-e', js], capture_output=True, text=True)
    return json.loads(r.stdout) if r.returncode == 0 else None
def alltext(bl): return ' '.join((b.get('text') or '') + ' ' + (b.get('body') or '') + ' ' + (b.get('title') or '') + ' ' + (b.get('label') or '') for b in bl)

head(1, 'THE PAGE AS FOUND   (git %s)' % BASELINE)
old = read_page(BASELINE); D0 = blocks(old) if old else None
if D0 is None: print('    SKIP  baseline page or node missing'); skips.append('baseline')
else:
    check('trigintaduonions (32 dimensões, perde norma multiplicativa)' in alltext(D0['PT']), 'as found (PT): "trigintaduonions (32 dimensões, perde norma multiplicativa)"')
    check('trigintaduonions (32-dim, lose multiplicative norm)' in alltext(D0['TR']['EN']), 'as found (EN): "trigintaduonions (32-dim, lose multiplicative norm)"')

# ---------------------------------------------------------------------------
head(2, 'THE CAYLEY-DICKSON LADDER   (built by (a,b)(c,d) = (ac - d*b, da + bc*))')
def conj(x):
    if len(x) == 1: return list(x)
    h = len(x) // 2; return conj(x[:h]) + [-t for t in x[h:]]
def add(x, y): return [a + b for a, b in zip(x, y)]
def sub(x, y): return [a - b for a, b in zip(x, y)]
def mul(x, y):
    if len(x) == 1: return [x[0] * y[0]]
    h = len(x) // 2; a, b, c, d = x[:h], x[h:], y[:h], y[h:]
    return sub(mul(a, c), mul(conj(d), b)) + add(mul(d, a), mul(b, conj(c)))
def nrm(x): return sum(t * t for t in x)
def rnd(n): return [random.uniform(-1, 1) for _ in range(n)]
random.seed(15)
def prop(n, trials=300):
    comm = ass = alt = mult = 0; worst = 0.0
    for _ in range(trials):
        x, y, z = rnd(n), rnd(n), rnd(n)
        if max(abs(a - b) for a, b in zip(mul(x, y), mul(y, x))) > 1e-9: comm += 1
        if max(abs(a - b) for a, b in zip(mul(mul(x, y), z), mul(x, mul(y, z)))) > 1e-9: ass += 1
        if max(abs(a - b) for a, b in zip(mul(mul(x, x), y), mul(x, mul(x, y)))) > 1e-9: alt += 1
        r_ = abs(nrm(mul(x, y)) - nrm(x) * nrm(y)); worst = max(worst, r_)
        if r_ > 1e-9: mult += 1
    return comm, ass, alt, mult, worst
res = {}
for n in (1, 2, 4, 8, 16, 32):
    res[n] = prop(n, 300 if n < 32 else 60)
    note('dim %2d: non-commuting %3d, non-associative %3d, non-alternative %3d, norm not multiplicative %3d  (of %d random triples)' % ((n,) + res[n][:4] + (300 if n < 32 else 60,)))
check(res[1][0] == 0 and res[2][0] == 0 and res[4][0] > 0, 'commutativity holds in dimensions 1 and 2 and is lost at 4 (the quaternions)')
check(res[4][1] == 0 and res[8][1] > 0, 'associativity holds at 4 and is lost at 8 (the octonions)')
check(res[8][2] == 0 and res[16][2] > 0, 'alternativity holds at 8 and is lost at 16 (the sedenions)')
check(all(res[n][3] == 0 for n in (1, 2, 4, 8)), 'the norm is multiplicative in dimensions 1, 2, 4 and 8')
check(res[16][3] > 0, 'the norm is NOT multiplicative at dimension 16 (sedenions): already lost there')
# explicit zero divisors at 16 and 32
def unit(n, i):
    e = [0.0] * n; e[i] = 1.0; return e
def find_zd(n):
    E = [(s, i) for i in range(n) for s in (1, -1)]
    for i, j in itertools.combinations(range(n), 2):
        for s in (1, -1):
            x = add(unit(n, i), [s * t for t in unit(n, j)])
            for k, l in itertools.combinations(range(n), 2):
                for s2 in (1, -1):
                    y = add(unit(n, k), [s2 * t for t in unit(n, l)])
                    if max(abs(t) for t in mul(x, y)) < 1e-12: return (i, s, j, k, s2, l)
    return None
zd = find_zd(16)
check(zd is not None, 'sedenion zero divisors exist: (e%d %+d e%d)(e%d %+d e%d) = 0' % (zd[0], zd[1], zd[2], zd[3], zd[4], zd[5]) if zd else 'no zero divisor found')
if zd:
    i, s, j, k, s2, l = zd
    x32 = add(unit(32, i), [s * t for t in unit(32, j)]); y32 = add(unit(32, k), [s2 * t for t in unit(32, l)])
    check(max(abs(t) for t in mul(x32, y32)) < 1e-12, 'the same pair (embedded) is a zero-divisor pair in dimension 32: the 32-dimensional algebra loses nothing new that the sedenions had not lost')
check(res[32][3] > 0, 'the norm is not multiplicative at 32 either (it is not where it was lost)')
note('(C loses ordering because i^2 = -1 < 0, while squares are non-negative in an ordered field: a one-line fact, not run.)')

# ---------------------------------------------------------------------------
head(3, 'J^2 = -id')
def det(M):
    n = len(M); M = [r[:] for r in M]; d = 1.0
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        if abs(M[p][c]) < 1e-14: return 0.0
        if p != c: M[c], M[p] = M[p], M[c]; d = -d
        d *= M[c][c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            for k in range(c, n): M[r][k] -= f * M[c][k]
    return d
for n in (1, 2, 3, 4, 5, 6):
    sgn = (-1) ** n
    note('n = %d: det(J)^2 >= 0 but det(-I) = %+d: a real n x n matrix with J^2 = -I %s' % (n, sgn, 'is possible' if sgn > 0 else 'is impossible'))
check(all((-1) ** n < 0 for n in (1, 3, 5)) and all((-1) ** n > 0 for n in (2, 4, 6)), 'J^2 = -id on a real vector space forces even dimension (det argument)')
lam = 1.7; Psi = [[0, -lam], [lam, 0]]; J = [[Psi[i][j] / lam for j in range(2)] for i in range(2)]
P2 = [[sum(Psi[i][k] * Psi[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
J2 = [[sum(J[i][k] * J[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
check(all(abs(P2[i][j] + lam * lam * (i == j)) < 1e-12 for i in range(2) for j in range(2)) and all(abs(J2[i][j] + (i == j)) < 1e-12 for i in range(2) for j in range(2)), 'Psi^2 = -lambda^2 id implies (Psi/lambda)^2 = -id (2 x 2 example)')
note('so if M is a contact 3-manifold (as elsewhere in the series) Psi and J cannot be endomorphisms of TM; they can act on the contact distribution (rank 2), on C^infty(M) (Book 6, ch.1), or on a stabilisation. The chapter does not say which.')

# ---------------------------------------------------------------------------
head(4, 'THE PAGE\'S OWN STRUCTURE')
cur = read_page(); D = blocks(cur) if cur else None
if D is None: print('    SKIP  page or node missing'); skips.append('page')
else:
    nb = {k: len(v) for k, v in D['TR'].items()}
    note('blocks: PT %d; translations: %s' % (len(D['PT']), nb))
    check(len(D['PT']) == 16 or len(D['PT']) == 15, 'the primary text has 15 blocks (16 with the verification note)')
    check(nb['EN'] >= 15 and all(nb[k] <= 3 for k in nb if k != 'EN'), 'EN has the full chapter; ES has 3 blocks and FR, DE, ZH, JA, AR one each')
    lean = [b.get('num') for b in D['PT'] if b.get('lean')]; sorry = [b.get('num') for b in D['PT'] if b.get('sorry')]
    note('"Lean 4" badges on: %s; "sorry" badges on: %s' % (lean, sorry))
    check(lean == ['15.1', '15.2', '15.3'], 'the three Lean badges are on Definitions 15.1, 15.2, 15.3 (theorems 15.1 and 15.2 carry none, as announced)')
    lf = subprocess.run(['git', '-C', ROOT, 'ls-files', '*.lean'], capture_output=True, text=True).stdout.split()
    hit = [f for f in lf if re.search(r'Vol4|Complex|Commutator', f) and 'lake' not in f]
    note('Lean files in this checkout that could hold Vol4.Complex.Commutator: %s' % (hit or 'none'))
    check(not hit, 'no Lean file for this chapter is in the repository: the badges are claims, WANTED')

# ---------------------------------------------------------------------------
head(5, 'THE PAGE AS CORRECTED   (working tree)')
if D is None: print('    SKIP'); 
else:
    pt, en = alltext(D['PT']), alltext(D['TR']['EN'])
    check('perde norma multiplicativa' not in pt or 'já se perdeu' in pt, 'PT: the 32-dimensional clause no longer says the norm is lost there')
    check('trigintaduonions (32 dimensões; a norma multiplicativa já se perdeu nos sedenions)' in pt, 'PT: corrected clause')
    check('trigintaduonions (32-dim; the multiplicative norm was already lost at the sedenions)' in en, 'EN: corrected clause')
    check('chIV-15-verify.py' in pt and 'chIV-15-verify.py' in en, 'a verification note naming this script is in PT and EN')

print('\n' + '=' * 72)
if skips: print('  SKIPPED (not passed, not failed): %s' % ', '.join(skips))
if fails:
    print('  %d FAIL:' % len(fails)); [print('    - ' + f) for f in fails]; sys.exit(1)
print('  all run checks passed.')
print('  Recorded as open, NOT checked here:')
print('   - Theorems 15.1 and 15.2 are announced without proof (Volume VI); the AXLE stub Vol4.Complex.Commutator is sorry-marked (Book 6, ch.1); no Lean file is in this checkout.')
print('   - [F,T] = F o T - T o F with F a map M -> M and T a vector field: composition of these is not defined without a convention (Book 6 ch.1 uses operators on C^infty(M)).')
print('   - the chapter numbering "Rung IV" for C, the second algebra, against "Vol IV": the author decides; and the same title as book4/ch15-complex-turn.html (R9).')
print('   - the partial translations (ES, FR, DE, ZH, JA, AR carry one to three blocks): not judged for accuracy here.')
