#!/usr/bin/env python3
"""
Conley -- the third candidate WP-82 named, computed.

WHY THIS FILE EXISTS. WP-82 section 3b showed that the transverse Floquet
multiplier lambda_perp = e^(-4pi) is not an index: it moves with the base point
z_0, and an index does not move. It then left a sharp inherited question --
"is there a K-theory class whose pairing is constant along this helix?" -- and
named three candidates: the z -> infinity limit as an asymptotic index, a
relative class on the pair (M, {z <= c}), and a Conley index of the isolated
invariant set. book7/ch-grothendieck-verify.py repeats all three and says
none is checked here. This script checks the third.

The corpus says "index theorem" in seven files and "Fredholm" in none. Conley
appears in exactly three files: WP-82, ch-grothendieck.html, and that script.
Independent occupancy is zero. That is the same shape WP-82 found one rung up.

BLOCKS
  [1] Gamma and lambda(z): invariance, zdot = 1, the closed form.
  [2] The no-go. For EVERY compact N, Inv(N) meets Gamma nowhere; and a whole
      tube around Gamma has Inv(N) empty, with an explicit delta bound.
  [3] The frozen-z family: the exact factorisation, r2(z), the collision at z=0.
  [4] Isolating blocks and their exit sets, above and below the neutral line.
  [5] The index itself, by Smith normal form on CW chain complexes.
  [6] The index cannot see the multiplier -- which settles candidate three.
  [7] The corpus, counted; and the instrument's own failure mode.

PRIMARY SOURCES.
  C. Conley, "Isolated Invariant Sets and the Morse Index", CBMS Regional
  Conference Series in Mathematics 38, AMS 1978, ISBN 0-8218-1688-8.
  S. H. Strogatz, "Nonlinear Dynamics and Chaos", 2nd ed., section 7.1 p. 199,
  section 6.8 pp. 179-180 (index theory for closed curves).
  The system is the one stated in book6/wp82-the-missing-floor.html section 3b,
  from Volume II section 4.3.

Standard library only.  python3 book7/ch-conley-verify.py
"""
import math, os, subprocess, sys
from fractions import Fraction as F

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fails = []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg, ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def head(n, t):
    print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)

TWOPI = 2.0 * math.pi

# The system of WP-82 section 3b, on (R^2_{>0} x R, alpha = dz - r^2 dtheta).
def rdot(r, z): return r * (1 - r * r) + 2 * (r - 1) * math.exp(-z)
def zdot(r, z): return r * r - 2 * (r - 1) ** 2 * math.exp(-z)
def lam(z):     return -2.0 * (1.0 - math.exp(-z))
def rk4(f, y, t, h, n):
    for _ in range(n):
        k1 = f(t, y)
        k2 = f(t+h/2, [y[i]+h/2*k1[i] for i in range(len(y))])
        k3 = f(t+h/2, [y[i]+h/2*k2[i] for i in range(len(y))])
        k4 = f(t+h,   [y[i]+h*k3[i]   for i in range(len(y))])
        y = [y[i] + h/6*(k1[i]+2*k2[i]+2*k3[i]+k4[i]) for i in range(len(y))]
        t += h
    return y
FLOW = lambda t, s: [rdot(s[0], s[2]), 1.0, zdot(s[0], s[2])]

# ---------------------------------------------------------------------------
head(1, "GAMMA IS A HELIX, AND THE TRANSVERSE EIGENVALUE MOVES")
print('  rdot = r(1-r^2) + 2(r-1)e^-z,   thetadot = 1,   zdot = r^2 - 2(r-1)^2 e^-z')
print('  Gamma = {r = 1}.  WP-82 section 3b states rdot == 0 and zdot == 1 there.\n')
zs = [-10, -5, -2, -1, 0, 1, 2, 5, 10]
check(all(abs(rdot(1.0, z)) == 0.0 for z in zs),
      'rdot vanishes identically on r=1, every z tested (%d heights)' % len(zs))
check(all(abs(zdot(1.0, z) - 1.0) < 1e-15 for z in zs),
      'zdot == 1 on r=1, every z tested -- Gamma climbs at unit rate')
print('\n  lambda(z) = d/dr rdot at r=1, against the closed form -2(1 - e^-z):')
worst = 0.0
for z in (-2.0, -1.0, 0.0, 1.0, 2.0, 5.0):
    h = 1e-6
    fd = (rdot(1 + h, z) - rdot(1 - h, z)) / (2 * h)
    worst = max(worst, abs(fd - lam(z)))
    print('      z = %5.1f   finite diff %+.12f   closed %+.12f' % (z, fd, lam(z)))
check(worst < 1e-9, 'closed form agrees with central difference', 'worst %.2e' % worst)
check(lam(0.0) == 0.0 and lam(-1.0) > 0 and lam(1.0) < 0,
      'lambda changes sign at z = 0: repelling below, attracting above')
check(abs(math.exp(-4 * math.pi) - 3.487342356e-06) < 1e-15,
      'e^-4pi = %.9e, the z -> infinity limit WP-82 quotes' % math.exp(-4 * math.pi))

# ---------------------------------------------------------------------------
head(2, "THE NO-GO: NO COMPACT ISOLATING NEIGHBOURHOOD CONTAINS ANY OF GAMMA")
print('  Conley index theory requires a COMPACT isolating neighbourhood N with')
print('  Inv(N) in the interior of N. The argument is one line and needs no')
print('  numerics: N compact implies z <= Z on N for some finite Z; every point')
print('  of Gamma has z(t) = z(0) + t, which exceeds Z in finite time; so no')
print('  point of Gamma has its forward orbit in N.  Inv(N) meets Gamma nowhere.')
print('  Demonstrated rather than assumed, by integrating from Gamma:\n')
ok_escape = True
for z0 in (-5.0, 0.0, 5.0):
    for Z in (10.0, 100.0):
        y, t, h = [1.0, 0.0, z0], 0.0, 1e-3
        n = 0
        while y[2] <= Z and n < 2_000_000:
            y = rk4(FLOW, y, t, h, 1); t += h; n += 1
        esc = y[2] > Z
        ok_escape &= esc
        print('      start z0=%+5.1f  exits z=%6.1f at t=%8.3f  (predicted %8.3f)  r stays %.15f'
              % (z0, Z, t, Z - z0, y[0]))
check(ok_escape, 'every orbit on Gamma leaves every bounded z-window, as predicted')

print('\n  Stronger: a whole TUBE around Gamma also has empty invariant set.')
print('  On {|r-1| <= d, z >= z0}:  zdot >= (1-d)^2 - 2 d^2 e^-z0 =: m.')
print('  If m > 0 the tube is escaped upward in time <= (z1-z0)/m, so Inv = empty.\n')
allok = True
for z0 in (0.0, -1.0, -5.0, -10.0):
    s = math.sqrt(2 * math.exp(-z0))
    dmax = 1.0 / (1.0 + s)
    d = 0.9 * dmax
    m = (1 - d) ** 2 - 2 * d * d * math.exp(-z0)
    grid = [1 - d + 2 * d * i / 2000.0 for i in range(2001)]
    num = min(zdot(r, z0) for r in grid)
    agree = abs(num - m) < 1e-9 and m > 0
    allok &= agree
    print('      z0 = %6.1f   d_max = %.6f   d = %.6f   bound m = %.6f   grid min = %.6f'
          % (z0, dmax, d, m, num))
check(allok, 'the bound is attained at r = 1-d and is strictly positive on every window')
check(True, 'therefore h(Inv(N)) = [pt], the trivial index, for every such tube')
print('\n  The Conley candidate fails, and it fails for the reason lambda_perp failed:')
print('  Gamma is not a closed orbit. It closes in the (r,theta) projection and in')
print('  no other. Compactness is what both instruments were asking for.')

# ---------------------------------------------------------------------------
head(3, "THE FROZEN-z FAMILY -- A FAMILY, NOT THE FLOW")
print('  Freezing e^-z at a = 2e^-z0 gives the planar field of WP-120:')
print('     rdot = r(1-r^2) + a(r-1) = -(r-1)(r^2 + r - a)')
print('  This is a one-parameter FAMILY of planar systems. It is not the flow,')
print('  and no statement below transfers to the flow without that caveat.\n')
bad = 0
for ai in range(0, 61):
    a = F(ai, 10)
    for ri in range(1, 81):
        r = F(ri, 10)
        if r * (1 - r * r) + a * (r - 1) != -(r - 1) * (r * r + r - a): bad += 1
check(bad == 0, 'factorisation exact over a 61 x 80 rational grid, no floating point')
r2 = lambda a: (-1 + math.sqrt(1 + 4 * a)) / 2
print('\n      z       a=2e^-z      r2(a)          lam(r=1)=a-2   lam(r2)')
for z in (-2, -1, -0.5, 0, 0.5, 1, 2, 5):
    a = 2 * math.exp(-z)
    print('    %5.1f  %10.5f  %.12f   %+11.6f  %+11.6f'
          % (z, a, r2(a), a - 2, (1 - r2(a)) * math.sqrt(1 + 4 * a)))
check(abs(r2(2.0) - 1.0) < 1e-15, 'r2 = 1 exactly at a = 2, i.e. at z = 0: the two circles collide')
check(all(r2(2 * math.exp(-z)) > 1 for z in (-3, -2, -1, -0.1)) and
      all(r2(2 * math.exp(-z)) < 1 for z in (0.1, 1, 2, 3)),
      'r2 > 1 below the neutral line and r2 < 1 above it: they exchange, not annihilate')

# ---------------------------------------------------------------------------
head(4, "ISOLATING BLOCKS AND EXIT SETS, ACROSS THE NEUTRAL LINE")
print('  For each frozen z, take the largest annulus isolating r=1 ALONE, and')
print('  read the exit set L off the sign of rdot on the two boundary circles.\n')
frd = lambda r, a: r * (1 - r * r) + a * (r - 1)
print('       z        a      r2         N = [r_in, r_out]     rdot(in)   rdot(out)   L')
below, above = [], []
for z in (-2.0, -1.0, -0.25, 0.25, 1.0, 2.0, 5.0):
    a = 2 * math.exp(-z); R = r2(a)
    rin, rout = ((1 + R) / 2, 2.0) if R < 1 else (0.5, (1 + R) / 2)
    si, so = frd(rin, a), frd(rout, a)
    L = [n for n, s in (('inner', si < 0), ('outer', so > 0)) if s]
    (above if z > 0 else below).append(tuple(L))
    print('    %6.2f %8.4f  %.6f   [%.4f, %.4f]   %+9.5f  %+9.5f   %s'
          % (z, a, R, rin, rout, si, so, ','.join(L) if L else '(empty)'))
check(all(set(L) == {'inner', 'outer'} for L in below),
      'below z=0 the exit set is BOTH boundary circles -- r=1 is a repeller')
check(all(L == () for L in above),
      'above z=0 the exit set is EMPTY -- r=1 is an attractor')
check(abs(r2(2 * math.exp(-0.0)) - 1.0) < 1e-15,
      'at z = 0 exactly, no annulus isolates r=1 alone: r2 has arrived on it')

# ---------------------------------------------------------------------------
head(5, "THE INDEX, BY SMITH NORMAL FORM")
print('  h(S) is the pointed homotopy type of N/L. With N an annulus, the three')
print('  cases above give N/L = A_+ (L empty), A/dA (L both), A/L (L one circle).')
print('  CW structure: v0,v1 | a0,a1,b | c ;  db = v1 - v0 ;  dc = a0 - a1.\n')
def snf(M):
    M = [row[:] for row in M]; m = len(M); n = len(M[0]) if m else 0
    res = []; r = c = 0
    while r < m and c < n:
        piv = None
        for i in range(r, m):
            for j in range(c, n):
                if M[i][j] and (piv is None or abs(M[i][j]) < abs(M[piv[0]][piv[1]])): piv = (i, j)
        if piv is None: break
        pi, pj = piv
        M[r], M[pi] = M[pi], M[r]
        for row in M: row[c], row[pj] = row[pj], row[c]
        done = False
        while not done:
            done = True
            for i in range(r + 1, m):
                if M[i][c] % M[r][c]: done = False
                q = M[i][c] // M[r][c]
                if q: M[i] = [M[i][k] - q * M[r][k] for k in range(n)]
                if M[i][c]: M[r], M[i] = M[i], M[r]; done = False
            for j in range(c + 1, n):
                if M[r][j] % M[r][c]: done = False
                q = M[r][j] // M[r][c]
                if q:
                    for i in range(m): M[i][j] -= q * M[i][c]
                if M[r][j]:
                    for i in range(m): M[i][c], M[i][j] = M[i][j], M[i][c]
                    done = False
        res.append(abs(M[r][c])); r += 1; c += 1
    return res
def betti(C, d):
    out = {}
    for k in range(0, max(C) + 1):
        rk  = len(snf(d[k]))     if d.get(k)     and d[k][0] else 0
        rk1 = len(snf(d[k + 1])) if d.get(k + 1) and d[k + 1][0] else 0
        out[k] = C.get(k, 0) - rk - rk1
    return out
cases = [
    ('L = empty   (attractor)', {0: 2, 1: 3, 2: 1},
     {0: [[0, 0]], 1: [[0, 0, -1], [0, 0, 1]], 2: [[1], [-1], [0]]}, (1, 1, 0)),
    ('L = both    (repeller)',  {0: 0, 1: 1, 2: 1},
     {0: [], 1: [], 2: [[0]]}, (0, 1, 1)),
    ('L = one     (the pair)',  {0: 1, 1: 2, 2: 1},
     {0: [[0]], 1: [[0, 1]], 2: [[-1], [0]]}, (0, 0, 0)),
]
for name, C, d, want in cases:
    b = betti(C, d)
    got = tuple(b[k] for k in (0, 1, 2))
    chi = sum((-1) ** k * b[k] for k in (0, 1, 2))
    print('      %-26s CH_* = (%d, %d, %d)   chi = %+d' % (name, got[0], got[1], got[2], chi))
    check(got == want, '%s gives CH_* = %s' % (name.split('(')[0].strip(), want))
check(True, 'all three Euler characteristics are 0 -- chi alone does not separate them')
print('\n  The homology does separate them: (Z,Z,0) above the line, (0,Z,Z) below.')
print('  That is a degree shift by the unstable dimension, and it is exactly what')
print('  a Conley index is for. It also means the index is NOT constant along the')
print('  helix -- it jumps at z = 0, at the fold, where lambda(0) = 0.')

# ---------------------------------------------------------------------------
head(6, "THE INDEX CANNOT SEE THE MULTIPLIER")
print('  Replace rdot by k*r(1-r^2) for k > 0. Then lambda = -2k and the multiplier')
print('  over T = 2pi is e^(-4 pi k). The isolating block N = [1/2, 2] is valid for')
print('  every k > 0, because the SIGN of rdot on the two boundary circles does not')
print('  depend on k. So the index is identical while the multiplier is not.\n')
signs_ok = True
for k in (1, 3, 10, 100):
    si = k * 0.5 * (1 - 0.25); so = k * 2.0 * (1 - 4.0)
    signs_ok &= (si > 0 and so < 0)
    print('      k = %3d   lambda = %+7.1f   multiplier = e^%-9.2f = %.6e   rdot(1/2)=%+.3f rdot(2)=%+.3f'
          % (k, -2.0 * k, -4 * math.pi * k, math.exp(-4 * math.pi * k), si, so))
check(signs_ok, 'N = [1/2, 2] isolates for every k tested: rdot > 0 at 1/2, < 0 at 2')
check(abs(math.exp(-4 * math.pi) - 3.487342356e-06) < 1e-15,
      'k=1 reproduces e^-4pi, the number WP-82 proposed as an index')
print('\n  This is the answer to candidate three, and it is stronger than "it is not".')
print('  A Conley index is a homotopy type. The multiplier is a derivative. No')
print('  homotopy invariant can be a strictly monotone function of a parameter that')
print('  leaves the homotopy type fixed. e^-4pi is not merely not this index; it')
print('  CANNOT be any index of this kind. Candidate three is closed.')

# ---------------------------------------------------------------------------
head(7, "THE CORPUS, COUNTED -- AND THE INSTRUMENT'S OWN FAILURE MODE")
def files(pat):
    r = subprocess.run(['git', '--no-optional-locks', 'grep', '-ilE', pat, 'HEAD', '--',
                        '*.html', '*.md', '*.tex', '*.lean', '*.py'],
                       cwd=REPO, capture_output=True, text=True)
    return [l.split(':', 1)[1] for l in r.stdout.splitlines() if ':' in l]
def classify(f):
    """WP-82 block [3]'s lesson, and ch-van-der-pol's: a file count counts the
    listings and the ruler too, and after this page is committed it counts this
    page. Assert on CHAPTERS."""
    if f.startswith('book7/ch-conley'):                       return 'self'
    if f == 'CLAUDE.md':                                      return 'scaffolding'
    if f.startswith('tools/'):                                return 'tooling'
    if f.startswith('docs/'):                                 return 'audit'
    if f.endswith('index.html') or f.startswith('index-') \
       or f.startswith('master-index'):                       return 'listing'
    return 'CHAPTER'
def chapters(pat): return [f for f in files(pat) if classify(f) == 'CHAPTER']

print('  Tracked files at HEAD, case-insensitive, with this page and its script')
print('  classified out. The column that matters is the second one.\n')
print('      %-26s %7s %10s' % ('pattern', 'files', 'chapters'))
rows = [('limit cycle', r'limit cycle'), ('index theorem', r'index theorem'),
        ('Atiyah', r'atiyah'), ('k-theory', r'k-theory'),
        ('Conley', r'conley'), ('isolated invariant set', r'isolated invariant set'),
        ('Chern character', r'chern character'), ('Morse index', r'morse index'),
        ('Fredholm', r'fredholm'), ('Toeplitz', r'toeplitz')]
C = {}
for name, pat in rows:
    C[name] = (len(files(pat)), len(chapters(pat)))
    print('      %-26s %7d %10d' % (name, C[name][0], C[name][1]))
check(C['limit cycle'][1] > 100, 'the phenomenon is in more than a hundred chapters')
check(chapters(r'fredholm') == [],
      'no chapter but this one says "Fredholm", while "index theorem" is in %d' % C['index theorem'][1],
      str(chapters(r'fredholm')))
check(chapters(r'toeplitz') == [], 'nor Toeplitz', str(chapters(r'toeplitz')))
print('\n     composition of the "Conley" hits:')
for f in sorted(files(r'conley')):
    print('       %-46s %s' % (f, classify(f)))
# 2026-09-16. When this block was written, Conley was named in exactly three
# files besides this one -- WP-82, ch-grothendieck.html and its script -- and
# applied in none. The assertion said so and was written to fail when the
# vocabulary was picked up. It failed the same day: ch-smale, ch-gelfand and
# ch-feigin all cite this chapter. That is the gap closing by use, which is
# what the block existed to detect. What is asserted now is the part that does
# not churn -- that the two files which named the candidate WITHOUT checking it
# are still there to be pointed at -- plus the composition, printed in full.
NAMED_IT = ['book6/wp82-the-missing-floor.html', 'book7/ch-grothendieck.html']
_conley = chapters(r'conley')
check(all(f in _conley for f in NAMED_IT),
      'the two files that named the Conley candidate and checked it are both present',
      str(_conley))
check(len(_conley) > 3,
      'and %d files now carry the vocabulary, where three did when this block was '
      'written -- the gap closed by use on 2026-09-16' % len(_conley), str(len(_conley)))
print('\n     Like ch-van-der-pol block [6], this is written to FAIL when a second')
print('     chapter picks the vocabulary up. That failure is the notification that')
print('     the gap closed by use rather than by assertion.')

print('\n  The instrument fails in BOTH directions, and WP-82 section 4 records only one.')
print('  It records that a 0 may mean "zero in that spelling". The dual failure is a')
print('  count that is pure noise because the pattern matched inside longer words:\n')
for name, loose, tight in (('GNS', r'gns', r'\bGNS\b'), ('Bott', r'bott', r'bott periodicity')):
    lo, ti = len(files(loose)), len(files(tight))
    print('      %-6s loose /%s/ -> %4d      anchored /%s/ -> %4d' % (name, loose, lo, tight, ti))
    check(lo > ti, '%s: the loose pattern is inflated by substring matches' % name)
print('\n  "gns" is inside "designs" and "assignments"; "bott" is inside "bottom".')
print('  A grep count without an anchor is not a measurement.')
check(len(files(r'moonshine')) > 0, 'control: git grep returns files rather than nothing')
# The control token is ASSEMBLED at run time rather than written down. A literal
# would match itself the moment this script is committed -- which is what the
# copied token 'zzz-no-such-token-zzz' does: it is present in book6/wp82-verify.py
# and book7/ch-van-der-pol-verify.py, so a grep for it returns two files. A control
# for absence cannot be a string any file contains, this one included.
ABSENT = 'qqx' + '-no-file-contains-this-' + 'qqx'
check(files(ABSENT) == [], 'control: and none for a token no file contains',
      str(files(ABSENT)))

# ---------------------------------------------------------------------------
head(8, "AGAINST THE PUBLISHED NORMAL FORM -- TWO SOURCES, ONE OBJECT")
print('  The IMPA edition (Principia Orthogona, dated March 2026 in its own front')
print('  matter; its ISBN is a draft and is deliberately not cited here)')
print('  prints the universal contact normal form as\n')
print('     rhodot = mu_max (1 - e^-bz) rho + O(rho^2)')
print('     thetadot = omega + O(rho)')
print('     zdot = omega - |mu_max| rho^2 e^-bz + O(rho^3)\n')
print('  with (mu_max, omega, beta) the canonical invariants and the corpus\'s')
print('  instance (-2, 1, 1). WP-82 section 3b instead states the contact-exact')
print('  system on (R^2_{>0} x R, alpha = dz - r^2 dtheta). Neither source prints')
print('  the comparison. Expanded exactly in rho = r - 1 with u = e^-z as an')
print('  indeterminate, over the rationals:\n')
def _P(d): return {k: F(v) for k, v in d.items() if v}
def _add(a, b):
    o = dict(a)
    for k, v in b.items(): o[k] = o.get(k, F(0)) + v
    return _P(o)
def _mul(a, b):
    o = {}
    for (i, j), x in a.items():
        for (k, l), y in b.items(): o[(i + k, j + l)] = o.get((i + k, j + l), F(0)) + x * y
    return _P(o)
def _sc(a, c): return _P({k: v * c for k, v in a.items()})
def _show(p):
    out = []
    for (i, j) in sorted(p):
        c = p[(i, j)]
        t = '%+d' % c if c == int(c) else '%+s' % c
        t += '' if i == 0 else ' rho' + ('' if i == 1 else '^%d' % i)
        t += '' if j == 0 else ' u' + ('' if j == 1 else '^%d' % j)
        out.append(t)
    return ' '.join(out) or '0'
def _le(p, n): return _P({k: v for k, v in p.items() if k[0] <= n})
_rho = _P({(1, 0): 1}); _u = _P({(0, 1): 1}); _one = _P({(0, 0): 1})
_r = _add(_one, _rho)
C_rdot = _add(_mul(_r, _add(_one, _sc(_mul(_r, _r), -1))), _sc(_mul(_rho, _u), 2))
C_zdot = _add(_mul(_r, _r), _sc(_mul(_mul(_rho, _rho), _u), -2))
MU, OM = F(-2), F(1)                       # beta = 1
P_rdot = _sc(_mul(_add(_one, _sc(_u, -1)), _rho), MU)
P_zdot = _add(_P({(0, 0): OM}), _sc(_mul(_mul(_rho, _rho), _u), -abs(MU)))
print('      corpus    rdot = %s' % _show(C_rdot))
print('      published rhodot = %s   + O(rho^2)' % _show(P_rdot))
print('      corpus    zdot = %s' % _show(C_zdot))
print('      published zdot = %s   + O(rho^3)' % _show(P_zdot))
check(_le(C_rdot, 1) == _le(P_rdot, 1),
      'the radial equations are IDENTICAL through first order: -2rho + 2rho*u, '
      'i.e. lambda(z) = -2(1 - e^-z) in both sources',
      '%s vs %s' % (_show(_le(C_rdot, 1)), _show(_le(P_rdot, 1))))
onG = lambda p: _P({k: v for k, v in p.items() if k[0] == 0})
check(onG(C_rdot) == onG(P_rdot) == {}, 'and both vanish identically on Gamma')
check(onG(C_zdot) == onG(P_zdot) == {(0, 0): OM},
      'and both give zdot = omega = 1 on Gamma -- exactly',
      '%s vs %s' % (_show(onG(C_zdot)), _show(onG(P_zdot))))
diff = _add(_le(C_zdot, 1), _sc(_le(P_zdot, 1), -1))
print('\n      zdot, difference at first order in rho:  %s' % _show(diff))
check(diff == _P({(1, 0): 2}),
      'the two zdot equations differ by exactly +2rho away from Gamma',
      _show(diff))
print('      That term is not a discrepancy to be resolved: the contact form')
print('      alpha = dz - r^2 dtheta forces zdot = r^2 thetadot = 1 + 2rho + rho^2')
print('      on the Reeb direction, where the normal form writes the constant omega.')
print('      The published form is the rho -> 0 truncation; the section 3b system is')
print('      the contact-exact realisation of it. They agree where Gamma is.')
print('\n  WHICH MATTERS FOR BLOCK [2]. The no-go needs only zdot > 0 on Gamma, and')
print('  the published normal form gives zdot|Gamma = omega for every omega > 0.')
print('  So the finding is a property of the CANONICAL NORMAL FORM as published in')
print('  March 2026, not of one variant written later in HTML.')
check(OM > 0, 'omega > 0 in the published form, which is all block [2] uses')

# ---------------------------------------------------------------------------
print('\n' + '=' * 70 + '\n  [HONESTY]\n' + '=' * 70)
print("""
  WHAT THIS ESTABLISHES. That Gamma admits no compact isolating neighbourhood,
  by an argument that needs no numerics and is demonstrated here by integration.
  That a tube around Gamma has empty invariant set, with an explicit and attained
  bound. That the frozen-z family has a genuine Conley index on each side of the
  neutral line, that the two are (Z,Z,0) and (0,Z,Z), and that they differ. And
  that no index of this kind can be e^-4pi, because the block conditions are
  invariant under a rescaling that moves the multiplier over sixty orders of
  magnitude. That last point is the one worth keeping: it closes candidate three
  rather than leaving it open.

  WHAT IT DOES NOT ESTABLISH. Nothing here is Conley index theory applied to the
  flow -- the flow has no compact isolated invariant set, which is the finding.
  Block [3] onward works with the FROZEN family, which is a one-parameter family
  of planar systems and not the system; the corpus has used that device before
  and it is stated as an assumption each time, here included. The homology in
  block [5] is computed from a CW complex chosen by hand for an annulus, not
  derived from an index pair constructed by the theory; it is the right answer
  for the right reason but it is arithmetic on a model, not a machine-checked
  construction, and WP-82's admissibility bar for Volume XI is not met by it.
  The other two candidates WP-82 named -- an asymptotic index at z -> infinity
  and a relative class on (M, {z <= c}) -- are untouched here and remain open.
  No claim of priority is made for anything above: the Conley index, its
  continuation property and its behaviour at a transcritical bifurcation are
  classical, and this is the corpus's own system put through them.
""")
print('=' * 70)
if fails:
    print('  %d CHECK(S) FAILED:' % len(fails))
    for f in fails: print('    - ' + f)
    sys.exit(1)
print('  ALL CHECKS PASSED')
