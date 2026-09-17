#!/usr/bin/env python3
"""
Euler -- the first number a shape had that did not come from measuring it.

WHY THIS FILE EXISTS. "Euler" occurs in 64 tracked files of this corpus and
"Euler characteristic" in 19; the symbol chi appears in 89. ch-conley computed
three Conley indices and recorded, as a curiosity, that all three have chi = 0
and that chi therefore separates nothing. That is not a curiosity. It is Euler's
number behaving exactly as Euler's number behaves, and the reason was available
in 1750.

Measured at HEAD, the apparatus around it is missing: "index of a vector field"
0, "hairy ball" 0, "Euler's method" 0, "Euler-Lagrange" 0, "Basel problem" 0,
Konigsberg 1, "graph theory" 1 -- while the corpus integrates with Runge-Kutta
in 20 files and never names the method Euler wrote first.

BLOCKS
  [1] F - E + V = 2, as Euler stated it to Goldbach, on nine solids.
  [2] Where it stops being 2: the polyhedral torus and the cylinder.
  [3] chi by two routes -- cell counts and Betti numbers -- agreeing.
  [4] Why chi could not separate ch-conley's three indices.
  [5] The index of a closed curve, by winding number.
  [6] The corpus's own field: where its zeros are, and what encloses index 1.
  [7] The corpus, counted, entity-aware.
  [8] Control.

PRIMARY SOURCES.
  L. Euler to C. Goldbach, 14 November 1750; E230 (statement, written 1750) and
  E231 (proof, written 1751), both published 1758. Euler's statement, in
  translation: "In every solid enclosed by plane faces, the number of faces
  along with the number of solid angles exceeds the number of edges by two."
  D. Richeson, "The Polyhedral Formula", and B. Hopkins and R. Wilson, "The
  Truth about Konigsberg", both in R. E. Bradley and C. E. Sandifer (eds.),
  "Leonhard Euler: Life, Work and Legacy", Elsevier 2007.
  S. H. Strogatz, "Nonlinear Dynamics and Chaos", 2nd ed., section 6.8
  pp. 179-180, index theory for closed curves; Theorem 6.8.2.

Standard library only.  python3 book7/ch-euler-verify.py
"""
import math, os, subprocess, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fails = []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg, ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def head(n, t):
    print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)

# ---------------------------------------------------------------------------
head(1, "F - E + V = 2, AS STATED TO GOLDBACH ON 14 NOVEMBER 1750")
print('  "In every solid enclosed by plane faces, the number of faces along with')
print('   the number of solid angles exceeds the number of edges by two."\n')
SOLIDS = {'tetrahedron': (4, 6, 4), 'cube': (8, 12, 6), 'octahedron': (6, 12, 8),
          'dodecahedron': (20, 30, 12), 'icosahedron': (12, 30, 20),
          'triangular prism': (6, 9, 5), 'square pyramid': (5, 8, 5),
          'pentagonal antiprism': (10, 20, 12), 'truncated icosahedron': (60, 90, 32)}
print('      %-24s %4s %4s %4s   %s' % ('solid', 'V', 'E', 'F', 'F-E+V'))
allok = True
for n, (V, E, F) in SOLIDS.items():
    chi = F - E + V
    allok &= (chi == 2)
    print('      %-24s %4d %4d %4d   %d' % (n, V, E, F, chi))
check(allok, 'every one of the %d solids gives 2, exactly, in integer arithmetic' % len(SOLIDS))
print('\n  Before 1750 everything known about polyhedra was metric -- volume, area,')
print('  angle. This is the first quantity a solid has that survives bending it.')

# ---------------------------------------------------------------------------
head(2, "AND WHERE IT STOPS BEING 2")
print('  Euler said "solid enclosed by plane faces", and the hypothesis does work.')
print('  Glue an n x m grid of quadrilaterals into a torus and the count changes.\n')
print('      %-22s %5s %5s %5s   %s' % ('surface', 'V', 'E', 'F', 'F-E+V'))
tor_ok = cyl_ok = True
for n, m in ((3, 3), (4, 3), (5, 4), (8, 6)):
    V, E, F = n * m, 2 * n * m, n * m
    tor_ok &= (F - E + V == 0)
    print('      %-22s %5d %5d %5d   %d' % ('%dx%d torus' % (n, m), V, E, F, F - E + V))
for n, m in ((3, 3), (5, 4)):
    V, E, F = n * (m + 1), n * (m + 1) + n * m, n * m
    cyl_ok &= (F - E + V == 0)
    print('      %-22s %5d %5d %5d   %d' % ('%dx%d cylinder' % (n, m), V, E, F, F - E + V))
check(tor_ok, 'the polyhedral torus gives 0, not 2, at every grid size tested')
check(cyl_ok, 'and so does the cylinder -- which is where this corpus keeps Gamma')

# ---------------------------------------------------------------------------
head(3, "CHI BY TWO ROUTES, AGREEING")
def snf(M):
    M = [r[:] for r in M]; m = len(M); n = len(M[0]) if m else 0
    res = []; r = c = 0
    while r < m and c < n:
        piv = None
        for i in range(r, m):
            for j in range(c, n):
                if M[i][j] and (piv is None or abs(M[i][j]) < abs(M[piv[0]][piv[1]])): piv = (i, j)
        if piv is None: break
        pi, pj = piv; M[r], M[pi] = M[pi], M[r]
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
        rk  = len(snf(d[k]))     if d.get(k)     and d[k] and d[k][0] else 0
        rk1 = len(snf(d[k + 1])) if d.get(k + 1) and d[k + 1] and d[k + 1][0] else 0
        out[k] = C.get(k, 0) - rk - rk1
    return out
SPACES = {
    'annulus A':    ({0: 2, 1: 3, 2: 1}, {0: [[0, 0]], 1: [[0, 0, -1], [0, 0, 1]], 2: [[1], [-1], [0]]}),
    'A/dA  (both)': ({0: 0, 1: 1, 2: 1}, {0: [], 1: [], 2: [[0]]}),
    'A/L   (one)':  ({0: 1, 1: 2, 2: 1}, {0: [[0]], 1: [[0, 1]], 2: [[-1], [0]]}),
    'sphere S^2':   ({0: 1, 1: 0, 2: 1}, {0: [[0]], 1: [], 2: [[0]]}),
    'torus T^2':    ({0: 1, 1: 2, 2: 1}, {0: [[0]], 1: [[0, 0]], 2: [[0], [0]]}),
    'disk D^2':     ({0: 1, 1: 1, 2: 1}, {0: [[0]], 1: [[0]], 2: [[1]]}),
}
print('  chi = alternating sum of cell counts, and chi = alternating sum of Betti')
print('  numbers. Euler counted cells; the second route was not available to him.\n')
print('      %-16s %-26s %11s %11s' % ('space', 'homology', 'chi(Betti)', 'chi(cells)'))
agree = True
CHI = {}
for name, (C, d) in SPACES.items():
    b = betti(C, d)
    cb = sum((-1) ** k * b[k] for k in sorted(b))
    cc = sum((-1) ** k * C.get(k, 0) for k in C)
    CHI[name] = cb
    agree &= (cb == cc)
    hs = ', '.join('H%d=%s' % (k, ('Z^%d' % b[k] if b[k] > 1 else ('Z' if b[k] == 1 else '0')))
                   for k in sorted(b))
    print('      %-16s %-26s %11d %11d' % (name, hs, cb, cc))
check(agree, 'the two routes agree on every space tested')
check(CHI['sphere S^2'] == 2 and CHI['disk D^2'] == 1 and CHI['torus T^2'] == 0,
      'sphere 2, disk 1, torus 0 -- computed, not quoted')

# ---------------------------------------------------------------------------
head(4, "WHY CHI COULD NOT SEPARATE ch-conley's THREE INDICES")
print('  ch-conley block [5] computed the Conley index in three cases and recorded')
print('  that all three have chi = 0, so chi separates nothing. Here is the reason.\n')
for name in ('annulus A', 'A/dA  (both)', 'A/L   (one)'):
    print('      %-16s chi = %d' % (name, CHI[name]))
check(all(CHI[n] == 0 for n in ('annulus A', 'A/dA  (both)', 'A/L   (one)')),
      'all three are 0, and so is the annulus every one of them is built from')
print('\n  The three homologies are (Z,Z,0), (0,Z,Z) and (0,0,0). The first two')
print('  differ by a shift of two degrees -- the unstable dimension -- and chi is')
print('  an ALTERNATING sum, so a shift by an even number leaves it fixed. chi was')
print('  never going to see the difference. It is not a weak invariant here; it is')
print('  the wrong one, and Euler\'s construction says which question it answers:')
print('  how many cells, counted with sign. Not: which cells, in which degree.')

# ---------------------------------------------------------------------------
head(5, "THE INDEX OF A CLOSED CURVE")
print('  Strogatz section 6.8, pp. 179-180: the index of a closed curve is the')
print('  number of turns the field direction makes as you go round it once.')
print('  Computed here by winding, not looked up.\n')
def index_of(f, cx, cy, R, N=200000):
    tot = 0.0; prev = None
    for i in range(N + 1):
        t = 2 * math.pi * i / N
        u, v = f(cx + R * math.cos(t), cy + R * math.sin(t))
        a = math.atan2(v, u)
        if prev is not None:
            d = a - prev
            while d > math.pi:  d -= 2 * math.pi
            while d < -math.pi: d += 2 * math.pi
            tot += d
        prev = a
    return tot / (2 * math.pi)
KNOWN = [('center   (-y, x)', lambda x, y: (-y, x), 1),
         ('saddle   (x, -y)', lambda x, y: (x, -y), -1),
         ('node     (x, y)',  lambda x, y: (x, y), 1),
         ('dipole   (x^2-y^2, 2xy)', lambda x, y: (x * x - y * y, 2 * x * y), 2)]
for name, f, want in KNOWN:
    got = index_of(f, 0, 0, 1.0)
    print('      %-26s index = %+.6f   (expected %+d)' % (name, got, want))
    check(abs(got - want) < 1e-6, '%s has index %+d' % (name.split('(')[0].strip(), want))

# ---------------------------------------------------------------------------
head(6, "THE CORPUS'S OWN FIELD")
A = 5.436563656918
R2 = (-1 + math.sqrt(1 + 4 * A)) / 2
def corpus(x, y):
    r = math.hypot(x, y)
    if r == 0: return (0.0, 0.0)
    rd = -(r - 1) * (r * r + r - A)
    c, s = x / r, y / r
    return (rd * c - r * s, rd * s + r * c)
print('  rdot = -(r-1)(r^2+r-a), thetadot = 1, a = %.6f; invariant circles at' % A)
print('  r = 1 and r = r2 = %.6f. The thetadot term never vanishes, so:\n' % R2)
nonzero = True
for r in (1.0, R2, 2.0):
    u, v = corpus(r, 0.0)
    m = math.hypot(u, v)
    nonzero &= (m > 1e-9)
    print('      on r = %-9.6f  field = (%+.3e, %+.6f)   |F| = %.6f' % (r, u, v, m))
check(nonzero, 'the field does NOT vanish on either invariant circle -- an invariant '
      'circle is not a fixed point')
print('\n      index about the origin, on circles of radius R:')
ok1 = True
for R in (0.3, 0.999, 1.001, R2 - 0.01, R2 + 0.01, 3.0, 10.0):
    i = index_of(corpus, 0, 0, R)
    ok1 &= abs(i - 1) < 1e-6
    print('        R = %-9.4f index = %+.6f' % (R, i))
check(ok1, 'every circle about the origin has index +1')
print('\n      small loops enclosing no zero:')
ok0 = True
for cx in (1.0, R2, 2.0):
    i = index_of(corpus, cx, 0, 0.05)
    ok0 &= abs(i) < 1e-6
    print('        centred at (%.4f, 0), radius 0.05: index = %+.6f' % (cx, i))
check(ok0, 'and a loop enclosing no zero has index 0')
print('\n  Strogatz Theorem 6.8.2: any closed orbit encloses fixed points whose')
print('  indices sum to +1. Both invariant circles enclose exactly the origin, and')
print('  the origin has index +1. The theorem is satisfied, and the reason the')
print('  corpus\'s 3-D flow has no fixed point AT ALL is the same reason its')
print('  surface is a cylinder: chi = 0 permits a nowhere-zero field, and on the')
print('  sphere, where chi = 2, it does not. That is the hairy ball theorem, and')
print('  block [3] computed both numbers.')

# ---------------------------------------------------------------------------
head(7, "THE CORPUS, COUNTED")
sys.path.insert(0, os.path.join(REPO, 'tools'))
try:
    from corpus_count import files as cfiles
    HAVE = True
except Exception:
    HAVE = False
def files(pat):
    if HAVE: return cfiles(pat)
    r = subprocess.run(['git', '--no-optional-locks', 'grep', '-ilE', pat, 'HEAD', '--',
                        '*.html', '*.md'], cwd=REPO, capture_output=True, text=True)
    return sorted(l.split(':', 1)[1] for l in r.stdout.splitlines() if ':' in l)
def classify(f):
    if f.startswith('book7/ch-euler'):                        return 'self'
    if f == 'CLAUDE.md':                                      return 'scaffolding'
    if f.startswith('tools/'):                                return 'tooling'
    if f.startswith('docs/'):                                 return 'audit'
    if f.startswith('_archive/'):                             return 'archive'
    if (f.endswith('index.html') or f.startswith('index-')
            or f.startswith('master-index')):                 return 'listing'
    return 'CHAPTER'
def chapters(pat): return [f for f in files(pat) if classify(f) == 'CHAPTER']
check(HAVE, 'tools/corpus_count.py imported -- counts are entity-aware')
ROWS = [('Euler', r'euler'), ('chi / χ', r'\bchi\b|χ'),
        ('Euler characteristic', r'euler characteristic'), ('zeta', r'\bzeta\b'),
        ('Runge-Kutta / RK4', r'\bRK4\b|runge.{0,3}kutta'),
        ('Euler product', r'euler product'), ('genus', r'genus'),
        ('Gauss-Bonnet', r'gauss.{0,3}bonnet'), ('totient', r'totient'),
        ('Poincare-Hopf', r'poincar(e|é|&eacute;).{0,3}hopf'),
        ('polyhedron formula', r'polyhedron formula|polyhedral formula'),
        ('Konigsberg', r'k(o|ö|&ouml;)nigsberg'), ('graph theory', r'graph theory'),
        ('index of a vector field', r'index of a vector field'),
        ('hairy ball', r'hairy ball'), ("Euler's method", r'euler.{0,3}s method'),
        ('Euler-Lagrange', r'euler.{0,3}lagrange'), ('Basel problem', r'basel problem')]
C = {}
print('\n      %-26s %7s %10s' % ('pattern', 'files', 'chapters'))
for name, pat in ROWS:
    C[name] = (len(files(pat)), len(chapters(pat)))
    print('      %-26s %7d %10d' % (name, C[name][0], C[name][1]))
check(C['Euler'][0] > 50, 'Euler is in %d files' % C['Euler'][0])
check(C['Runge-Kutta / RK4'][1] > 10,
      'the corpus integrates with Runge-Kutta in %d chapters' % C['Runge-Kutta / RK4'][1])
for z in ('index of a vector field', 'hairy ball', "Euler's method", 'Euler-Lagrange',
          'Basel problem'):
    pat = dict(ROWS)[z]
    check(chapters(pat) == [], 'no chapter but this one uses "%s"' % z, str(chapters(pat)))
print('\n     Written to FAIL when a second chapter picks any of those up.')

# ---------------------------------------------------------------------------
head(8, 'CONTROL')
check(len(files(r'moonshine')) > 0, 'the counter returns files rather than nothing')
ABSENT = 'qqx' + '-no-file-contains-this-' + 'qqx'
check(files(ABSENT) == [], 'and none for a token no file writes down', str(files(ABSENT)))
check(abs(index_of(lambda x, y: (1.0, 0.0), 0, 0, 1.0)) < 1e-9,
      'a constant field has index 0 -- the winding routine is not always +1')
check(betti({0: 1}, {0: [[0]], 1: []})[0] == 1, 'the Betti helper reads 1 for a point')

print('\n' + '=' * 70 + '\n  [HONESTY]\n' + '=' * 70)
print("""
  WHAT THIS ESTABLISHES. That Euler's count gives 2 on nine solids and 0 on the
  polyhedral torus and cylinder, in integer arithmetic. That chi computed from
  cell counts agrees with chi computed from Betti numbers on six spaces, giving
  sphere 2, disk 1, torus 0. That all three of ch-conley's Conley indices have
  chi = 0 because each is built from the annulus and the two that differ do so by
  an even degree shift, which an alternating sum cannot see -- so chi was the
  wrong invariant there rather than a weak one. That the winding routine returns
  +1, -1, +1, +2 on centre, saddle, node and dipole. And that this corpus's own
  planar field does not vanish on either invariant circle, has index +1 about the
  origin at every radius tested and 0 about loops enclosing nothing, which is
  Strogatz Theorem 6.8.2 satisfied on the corpus's own equations.

  WHAT IT DOES NOT ESTABLISH. Poincare-Hopf itself, or the hairy ball theorem.
  Block [6] computes chi for a cylinder and a sphere and computes indices for
  particular fields; it does not prove that the index sum equals chi, and the
  remark connecting the corpus's zero-free flow to chi = 0 is a reading of two
  computed facts, not a derivation of one from the other. The winding numbers are
  numerical quadrature on a finite grid -- they land within 1e-6 of integers,
  which is evidence that the integers are right and not a proof. Euler's own
  proof of the polyhedral formula, which Richeson shows to be flawed and
  repairable, is not reproduced or assessed here; nor is the question of which
  hypotheses on a solid make the theorem true, which is the substance of the
  nineteenth-century work. No priority is claimed for anything: the letter to
  Goldbach is dated 14 November 1750.
""")
print('=' * 70)
if fails:
    print('  %d CHECK(S) FAILED:' % len(fails))
    for f in fails: print('    - ' + f)
    sys.exit(1)
print('  ALL CHECKS PASSED')
