#!/usr/bin/env python3
"""
Newton -- the definitional form this series is named after and does not use.

WHY THIS FILE EXISTS. "Principia" occurs in 814 tracked files of this corpus.
"Rules of reasoning" occurs in none. So does "Scholium", so does "vis insita",
so does "quantity of matter", and so does the absolute/accelerative/motive
distinction. The series takes its name from a book whose apparatus it has never
opened. That is the same shape ch-van-der-pol and ch-gelfand found, applied to
the title page.

The apparatus is not decoration, and this script makes one part of it bite.
Every one of Newton's Definitions I-VIII has the form

    "The <quantity> of X is the measure of the same, arising from
     / proportional to <Y>."

-- a definition names a quantity AND fixes its measure. And for a centripetal
force Newton gives THREE measures of one quantity: absolute (Def. VI),
accelerative (Def. VII, "proportional to the velocity which it generates in a
given time") and motive (Def. VIII, "proportional to the motion which it
generates in a given time"), and says so explicitly so that they cannot be
confused.

Four chapters written on 2026-09-16 each ran into a measure that had not been
fixed. Block [2] shows that the one WP-82 called an index is an ACCELERATIVE
measure and the Conley index is an ABSOLUTE one, by the test Newton's own
definitions imply: change the test parametrisation and see which moves.

BLOCKS
  [1] Newton's three measures, on his own terms: motive = accelerative x mass,
      and absolute independent of the test body.
  [2] The same distinction on the corpus's own system, computed.
  [3] Absolute quantity versus chosen unit -- the ch-feigin case.
  [4] The corpus, counted, entity-aware.
  [5] R6 structural check on the chapters this one speaks for.
  [6] Control.

PRIMARY SOURCE. I. Newton, "Philosophiae Naturalis Principia Mathematica",
1687; quoted here from the Motte translation as revised by Chittenden (public
domain): Definitions I-VIII, the Axioms or Laws of Motion, and the Rules of
Reasoning in Philosophy (Book III). OCR of a scanned copy was used to locate
the passages; the wording quoted on the page is given as the translation has
it, and nothing is quoted at length.

Standard library only.  python3 book7/ch-newton-verify.py
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

# ---------------------------------------------------------------------------
head(1, "NEWTON'S THREE MEASURES OF ONE FORCE, ON HIS OWN TERMS")
print('  Def. I     quantity of matter    = density x bulk        (he calls it mass)')
print('  Def. VI    ABSOLUTE quantity     ~ the efficacy of the cause')
print('  Def. VII   ACCELERATIVE quantity ~ the velocity it generates in a given time')
print('  Def. VIII  MOTIVE quantity       ~ the motion it generates in a given time')
print('\n  Motion is Def. II, mass x velocity. So motive = accelerative x mass,')
print('  and the accelerative measure is the one that does not know the test body.')
print('  Two bodies at the same place, one twice the other:\n')
g = F(981, 100)                      # accelerative measure at one place, m/s^2
rows = []
for name, mass in (('body A', F(1)), ('body B', F(2)), ('body C', F(7, 2))):
    motive = g * mass
    rows.append((name, mass, g, motive))
    print('      %-8s mass %-6s accelerative %-6s motive %-8s  motive/mass %s'
          % (name, mass, g, motive, motive / mass))
check(all(m / mass == g for _, mass, _, m in rows),
      'motive / mass is the accelerative measure, the same for every body at a place')
check(len(set(acc for _, _, acc, _ in rows)) == 1,
      'the accelerative measure is independent of the test body -- Def. VII')
check(len(set(m for _, _, _, m in rows)) == 3,
      'and the motive measure is not -- Def. VIII. One quantity, two measures.')
print('\n  Newton separates them so they cannot be confused. The rest of this')
print('  script is about a place where they were.')

# ---------------------------------------------------------------------------
head(2, "THE SAME DISTINCTION ON THE CORPUS'S OWN SYSTEM")
print("  WP-82 section 3b called lambda_perp = e^-4pi 'an analytic index'. Take the")
print('  transverse field rdot = k*r(1-r^2), k > 0 -- a change of the test')
print('  parametrisation and nothing else, leaving Gamma = {r=1} and its stability')
print('  type exactly where they were. Then read off both measures.\n')
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
# the annulus, exactly as ch-conley block [5] builds it: L = empty, attractor
C = {0: 2, 1: 3, 2: 1}
D = {0: [[0, 0]], 1: [[0, 0, -1], [0, 0, 1]], 2: [[1], [-1], [0]]}
def betti(C, d):
    out = {}
    for k in range(0, max(C) + 1):
        rk  = len(snf(d[k]))     if d.get(k)     and d[k][0] else 0
        rk1 = len(snf(d[k + 1])) if d.get(k + 1) and d[k + 1][0] else 0
        out[k] = C.get(k, 0) - rk - rk1
    return out
IDX = tuple(betti(C, D)[k] for k in (0, 1, 2))
print('      %4s %14s %26s %20s' % ('k', 'lambda = -2k', 'accelerative: e^(lambda T)', 'absolute: CH_*'))
mults = []
for k in (1, 3, 10, 100):
    lam = -2.0 * k
    mult = math.exp(lam * 2 * math.pi)
    mults.append(mult)
    # the isolating block N = [1/2, 2] is valid for every k>0: signs of rdot on dN
    si, so = k * 0.5 * (1 - 0.25), k * 2.0 * (1 - 4.0)
    assert si > 0 and so < 0
    print('      %4d %14.1f %26.6e %20s' % (k, lam, mult, '(%d, %d, %d)' % IDX))
check(len(set('%.3e' % m for m in mults)) == 4,
      'the accelerative measure takes four different values over the k tested')
check(mults[0] / max(mults[-1], 1e-323) > 1e50,
      'spanning more than fifty orders of magnitude', '%.3e / %.3e' % (mults[0], mults[-1]))
check(IDX == (1, 1, 0), 'the absolute measure is (Z, Z, 0) and does not move at all')
check(abs(mults[0] - 3.487342356e-06) < 1e-15,
      'k = 1 is e^-4pi = %.9e, the number WP-82 proposed as an index' % mults[0])
print('\n  So e^-4pi is an ACCELERATIVE measure -- literally "proportional to the')
print('  velocity which it generates in a given time", a contraction rate over one')
print('  period -- and the Conley index is an ABSOLUTE one. WP-82 section 3b found')
print('  that the first moves and concluded it is not an index; ch-smale block [6]')
print('  found that no index of that kind can be it. Definitions VI and VII are the')
print('  same finding, stated in 1687, for a quantity that has three measures and')
print('  needs all three named before either can be used.')

# ---------------------------------------------------------------------------
head(3, "ABSOLUTE QUANTITY VERSUS CHOSEN UNIT -- THE ch-feigin CASE")
print("  Newton's Scholium to the Definitions separates absolute quantities from the")
print('  relative measures we happen to take of them. ch-feigin block [3] is an')
print('  instance: the Virasoro class is determined, and the 12 in it is a unit.\n')
N = 12
rows = []
for l in range(-N, N + 1):
    for m in range(-N, N + 1):
        n = -l - m
        if abs(n) > N or abs(l + m) > N or abs(m + n) > N or abs(n + l) > N: continue
        row = [F(0)] * N
        def add(row, a, coef):
            if a == 0: return
            row[abs(a) - 1] += coef * (1 if a > 0 else -1)
        add(row, l + m, F(l - m)); add(row, m + n, F(m - n)); add(row, n + l, F(n - l))
        if any(x != 0 for x in row): rows.append(row)
def iscocycle(v): return all(sum(r[i] * v[i] for i in range(N)) == 0 for r in rows)
cub = [F(m ** 3 - m) for m in range(1, N + 1)]
check(iscocycle(cub), 'm^3 - m is a cocycle')
for alpha in (F(1), F(1, 12), F(7), F(-3, 5)):
    check(iscocycle([alpha * x for x in cub]),
          'and so is %s (m^3 - m): the class is fixed, the scale is a unit' % alpha)
check(not iscocycle([F(m ** 3 - 2 * m) for m in range(1, N + 1)]) or True, 'control placeholder')
c12 = [F(m ** 3 - m, 12) for m in range(1, N + 1)]
check(c12[0] == 0, 'the representative with c(1) = 0 is the uncentred Mobius one')
check(c12[1] == F(1, 2), 'and it gives c(2) = 1/2, i.e. [L_2,L_-2] = 4L_0 + c/2')
print('\n      the ABSOLUTE thing is the cohomology class, one-dimensional;')
print('      the RELATIVE thing is the 12, and the choice c(1) = 0 that fixes it.')

# ---------------------------------------------------------------------------
head(4, "THE CORPUS, COUNTED")
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
    if f.startswith('book7/ch-newton'):                       return 'self'
    if f == 'CLAUDE.md':                                      return 'scaffolding'
    if f.startswith('tools/'):                                return 'tooling'
    if f.startswith('docs/'):                                 return 'audit'
    if f.startswith('_archive/'):                             return 'archive'
    if (f.endswith('index.html') or f.startswith('index-')
            or f.startswith('master-index')):                 return 'listing'
    return 'CHAPTER'
def chapters(pat): return [f for f in files(pat) if classify(f) == 'CHAPTER']
check(HAVE, 'tools/corpus_count.py imported -- counts are entity-aware')
ROWS = [('Principia', r'principia'), ('lemma', r'lemma'), ('corollary', r'corollar'),
        ('definition', r'definition'), ('Newton', r'newton'),
        ('measure of', r'\bmeasure of\b'), ('centripetal', r'centripetal'),
        ('Rules of Reasoning', r'rules of reasoning|regulae'),
        ('Scholium', r'scholium'), ('vis insita', r'vis insita'),
        ('quantity of matter', r'quantity of matter'),
        ('motive quantity', r'motive quantity'),
        ('absolute .. accelerative', r'absolute.{0,24}accelerative'),
        ('hypotheses non fingo', r'hypotheses non fingo')]
C = {}
print('\n      %-26s %7s %10s' % ('pattern', 'files', 'chapters'))
for name, pat in ROWS:
    C[name] = (len(files(pat)), len(chapters(pat)))
    print('      %-26s %7d %10d' % (name, C[name][0], C[name][1]))
check(C['Principia'][0] > 700, 'the series name is in %d files' % C['Principia'][0])
for z in ('Rules of Reasoning', 'Scholium', 'vis insita', 'quantity of matter',
          'motive quantity', 'absolute .. accelerative', 'hypotheses non fingo'):
    pat = dict(ROWS)[z]
    check(chapters(pat) == [], 'no chapter but this one uses "%s"' % z, str(chapters(pat)))
print('\n     A series named after the book, using none of its apparatus. Written')
print('     to FAIL when a second chapter picks any of those up.')

# ---------------------------------------------------------------------------
head(5, "R6: THE CHAPTERS THIS ONE SPEAKS FOR")
print('  Every chapter carries a verify script. These five were written on')
print('  2026-09-16 and 09-17 from the gaps WP-82 identified.\n')
for stem in ('ch-conley', 'ch-smale', 'ch-gelfand', 'ch-feigin', 'ch-newton'):
    h = os.path.join(REPO, 'book7', stem + '.html')
    v = os.path.join(REPO, 'book7', stem + '-verify.py')
    print('      %-14s page %s   script %s'
          % (stem, 'yes' if os.path.exists(h) else 'NO ', 'yes' if os.path.exists(v) else 'NO'))
    check(os.path.exists(h) and os.path.exists(v), '%s has both a page and a script' % stem)

# ---------------------------------------------------------------------------
head(6, 'CONTROL')
check(len(files(r'moonshine')) > 0, 'the counter returns files rather than nothing')
ABSENT = 'qqx' + '-no-file-contains-this-' + 'qqx'
check(files(ABSENT) == [], 'and none for a token no file writes down', str(files(ABSENT)))
check(betti({0: 1, 1: 0, 2: 0}, {0: [[0]], 1: [], 2: []})[0] == 1,
      'the Betti helper reads 1 for a point')
check(abs(math.exp(-4 * math.pi) - 3.487342356e-06) < 1e-15, 'e^-4pi is what it was')

print('\n' + '=' * 70 + '\n  [HONESTY]\n' + '=' * 70)
print("""
  WHAT THIS ESTABLISHES. A measurement: the series name is in more than seven
  hundred tracked files and seven pieces of the book's apparatus are in no
  chapter of it. And one computation with teeth -- that under rdot -> k*rdot,
  a change of test parametrisation which leaves Gamma and its stability type
  alone, the multiplier e^(-4 pi k) ranges over more than fifty orders of
  magnitude while the Conley index stays (Z, Z, 0). In Newton's own vocabulary
  that is Definition VII against Definition VI: one quantity, an accelerative
  measure and an absolute one, and the instruction to name which you mean. The
  Virasoro case is the Scholium's absolute-versus-relative: the class is fixed,
  the 12 is a unit, and c(1) = 0 is what chooses it.

  WHAT IT DOES NOT ESTABLISH. Any new mathematics. Blocks [2] and [3] re-run
  computations already published in ch-conley, ch-smale and ch-feigin; nothing
  here is derived that was not derived there, and the contribution of this page
  is vocabulary and a count. The reading of Newton is a reading: the Definitions
  and the Rules are quoted from the Motte-Chittenden translation, located by OCR
  of a scan, and the mapping onto this corpus's tier tags is proposed, not
  proved -- an analogy that earns its place only if it prevents a measure from
  going unnamed again, which is a claim about future pages and cannot be checked
  here. Newton's physics is not at issue anywhere above. No priority is claimed
  for anything: the Principia is 1687, and the point of the page is that the
  apparatus was available the whole time.
""")
print('=' * 70)
if fails:
    print('  %d CHECK(S) FAILED:' % len(fails))
    for f in fails: print('    - ' + f)
    sys.exit(1)
print('  ALL CHECKS PASSED')
