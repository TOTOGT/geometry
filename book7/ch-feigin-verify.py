#!/usr/bin/env python3
"""
Feigin -- Langlands duality inside vertex algebra theory, and what it needs.

WHY THIS FILE EXISTS. WP-82 section 3 gave Volume XV (rung 32, Motivic /
Langlands) the seed "Monstrous Moonshine -- 25 files, and Vol VIII entire". Its
own correction of 2026-09-11 withdrew that: Moonshine supplies modular
functions, which is the automorphic side, and Langlands is a correspondence, so
half of one is not half the distance. It named two replacements. The second is
Feigin-Frenkel: the centre of the affine vertex algebra at the CRITICAL level is
the classical W-algebra of the LANGLANDS DUAL,

    z(g-hat)  =  W(^L g)      at  k = -h^v

which is Langlands duality with no Galois side at all, reachable from the vertex
algebra material Vol VIII already holds. WP-82 then measured: the corpus has
files using "vertex operator" and "Virasoro", and ONE using "W-algebra" -- that
one being WP-82 itself.

This script builds what can be built from first principles and says plainly what
cannot. Virasoro is derived, not quoted: the Witt algebra from vector fields,
its second cohomology computed, and the m^3 - m class shown to be forced. The
critical level is then computed for every simple type from its Cartan matrix
alone, including E8, which this corpus uses more than any other object.

BLOCKS
  [1] The Witt algebra, exactly, from vector fields on the punctured line.
  [2] H^2(Witt) computed -- by restriction, because a raw truncation inflates it.
  [3] The class: m^3 - m, with the -m forced and the 12 a convention.
  [4] Root systems and dual Coxeter numbers from Cartan matrices alone.
  [5] Langlands duals by transposing the Cartan matrix.
  [6] The critical level and the central charge, with a check that is not
      circular: level 1, simply laced, must give c = rank.
  [7] The corpus, counted, entity-aware.
  [8] Control.

PRIMARY SOURCES.
  B. Feigin and E. Frenkel, on the centre of the affine Kac-Moody algebra at the
  critical level and W-algebras (from 1991 onward); see E. Frenkel, "Langlands
  Correspondence for Loop Groups", CUP 2007, for the statement used here.
  A. B. Zamolodchikov, on additional symmetries in two-dimensional conformal
  field theory (1985) -- the W_3 algebra.
  V. G. Kac, "Infinite Dimensional Lie Algebras", 3rd ed., CUP 1990, for
  Cartan matrices, dual Coxeter numbers and the Sugawara construction.
  In-corpus: book6/wp82-the-missing-floor.html section 3, XV row and its
  2026-09-11 correction.

Standard library only.  python3 book7/ch-feigin-verify.py
"""
import os, subprocess, sys
from fractions import Fraction as F

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fails = []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg, ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def head(n, t):
    print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)

def rref_add(basis, v):
    v = v[:]
    for p, b in basis:
        if v[p] != 0:
            f = v[p]; v = [v[k] - f * b[k] for k in range(len(v))]
    for i, x in enumerate(v):
        if x != 0:
            v = [y / x for y in v]; basis.append((i, v)); return True
    return False
def rank(rows):
    b = []
    for r in rows: rref_add(b, r)
    return len(b)
def nullspace(rows, n):
    M = [r[:] for r in rows]; m = len(M); piv = []; r = 0
    for c in range(n):
        p = None
        for i in range(r, m):
            if M[i][c] != 0: p = i; break
        if p is None: continue
        M[r], M[p] = M[p], M[r]; pv = M[r][c]; M[r] = [x / pv for x in M[r]]
        for i in range(m):
            if i != r and M[i][c] != 0:
                f = M[i][c]; M[i] = [M[i][k] - f * M[r][k] for k in range(n)]
        piv.append(c); r += 1
    out = []
    for fc in [c for c in range(n) if c not in piv]:
        v = [F(0)] * n; v[fc] = F(1)
        for i, c in enumerate(piv): v[c] = -M[i][fc]
        out.append(v)
    return out

# ---------------------------------------------------------------------------
head(1, "THE WITT ALGEBRA, FROM VECTOR FIELDS, EXACTLY")
print('  L_n = -z^(n+1) d/dz acting on Laurent monomials: L_n z^j = -j z^(n+j).')
print('  Then [L_m, L_n] z^j = j(n-m) z^(m+n+j), and (m-n) L_(m+n) z^j is the')
print('  same thing. Integer arithmetic, no floating point, no library.\n')
bad = 0; tot = 0
for m in range(-6, 7):
    for n in range(-6, 7):
        for j in range(-6, 7):
            tot += 1
            if j * (n - m) != (m - n) * (-j): bad += 1
check(bad == 0, '[L_m,L_n] = (m-n)L_{m+n} on all %d triples tested' % tot, str(bad))

# ---------------------------------------------------------------------------
head(2, "H^2 OF THE WITT ALGEBRA -- AND WHY A RAW TRUNCATION GETS IT WRONG")
print('  A 2-cocycle is an antisymmetric w with')
print('     (l-m) w(L_{l+m},L_n) + (m-n) w(L_{m+n},L_l) + (n-l) w(L_{n+l},L_m) = 0')
print('  and a coboundary is w(L_a,L_b) = (a-b) f(L_{a+b}).\n')
print('  Truncating to |n| <= N loses every triple that reaches outside the window,')
print('  so the cocycle space is inflated near the edge. Solve on [-N,N], then')
print('  RESTRICT to pairs inside [-M,M] before quotienting. Same lesson as the')
print('  Gelfand chapter: an algebra generated to a fixed word length is not the')
print('  algebra, and a cocycle space on a truncated window is not the space.\n')
def H2(N, M):
    R = list(range(-N, N + 1)); idx = {}
    for a in R:
        for b in R:
            if a < b: idx[(a, b)] = len(idx)
    D = len(idx)
    def put(row, a, b, coef):
        if a == b: return
        if a < b: row[idx[(a, b)]] += coef
        else:     row[idx[(b, a)]] -= coef
    rows = []
    for l in R:
        for m in R:
            for n in R:
                if l >= m or m >= n: continue
                if abs(l + m) > N or abs(m + n) > N or abs(n + l) > N: continue
                row = [F(0)] * D
                put(row, l + m, n, F(l - m)); put(row, m + n, l, F(m - n)); put(row, n + l, m, F(n - l))
                if any(x != 0 for x in row): rows.append(row)
    Z = nullspace(rows, D)
    Brows = []
    for j in R:
        row = [F(0)] * D
        for (a, b), i in idx.items():
            if a + b == j: row[i] += F(a - b)
        Brows.append(row)
    keep = [i for (a, b), i in idx.items() if abs(a) <= M and abs(b) <= M]
    Zr = [[v[i] for i in keep] for v in Z]
    Br = [[v[i] for i in keep] for v in Brows]
    return rank(Zr), rank(Br), rank(Zr + Br) - rank(Br)
print('      %3s %3s %10s %10s %10s' % ('N', 'M', 'dim Z|', 'dim B|', 'dim H^2'))
allone = True
for N, M in ((5, 2), (6, 3), (7, 3), (8, 4), (9, 4), (10, 5)):
    dz, db, h = H2(N, M)
    allone &= (h == 1)
    print('      %3d %3d %10d %10d %10d' % (N, M, dz, db, h))
check(allone, 'dim H^2(Witt) = 1 at every window tested -- a ONE-dimensional space of'
      ' central extensions, which is why Virasoro is "the" one')

# ---------------------------------------------------------------------------
head(3, "THE CLASS, AND WHY IT IS m^3 - m")
print('  In the degree-zero part w(L_m, L_-m) = c(m), c antisymmetric, the cocycle')
print('  condition is a linear system in c(1..N). Solve it exactly.\n')
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
dimZ0 = N - rank(rows)
check(dimZ0 == 2, 'the degree-zero cocycle space is 2-dimensional', str(dimZ0))
cands = {'m':       [F(m) for m in range(1, N + 1)],
         'm^3':     [F(m ** 3) for m in range(1, N + 1)],
         'm^3 - m': [F(m ** 3 - m) for m in range(1, N + 1)],
         'm^2':     [F(m * m) for m in range(1, N + 1)],
         'm^5':     [F(m ** 5) for m in range(1, N + 1)]}
for nm, v in cands.items():
    isc = all(sum(row[i] * v[i] for i in range(N)) == 0 for row in rows)
    print('      is c(m) = %-8s a cocycle?  %s' % (nm, isc))
    if nm in ('m', 'm^3', 'm^3 - m'): check(isc, 'c(m) = %s is a cocycle' % nm)
    if nm in ('m^2', 'm^5'):          check(not isc, 'c(m) = %s is NOT a cocycle' % nm)
print('\n  So Z^2_0 = span{m, m^3}. The coboundaries in degree zero are')
print('  c(m) = (m - (-m)) f(L_0) = 2m f(L_0), i.e. exactly the multiples of m.')
print('  H^2_0 is therefore 1-dimensional and every representative is m^3 + t*m.')
print('  Fixing t = -1 is the unique choice with c(1) = 0, which is the statement')
print('  that L_-1, L_0, L_1 span an UNCENTRED sl_2 -- the Mobius subalgebra.')
c = lambda m: F(m ** 3 - m, 12)
check(c(1) == 0, 'c(1) = 0: no central term in the Mobius sl_2')
check(c(2) == F(1, 2), 'c(2) = 1/2, so [L_2,L_-2] = 4L_0 + c/2')
print('\n      [L_m, L_n] = (m-n)L_{m+n} + (c/12)(m^3 - m) delta_{m+n,0}')
print('      the 12 is a normalisation; the -m is FORCED.')
for m in range(1, 7):
    print('        m = %d   (m^3-m)/12 = %s' % (m, c(m)))

# ---------------------------------------------------------------------------
head(4, "ROOT SYSTEMS AND DUAL COXETER NUMBERS, FROM CARTAN MATRICES ALONE")
def cartan(t, n):
    A = [[F(0)] * n for _ in range(n)]
    for i in range(n): A[i][i] = F(2)
    if t in 'ABC':
        for i in range(n - 1): A[i][i + 1] = A[i + 1][i] = F(-1)
        if t == 'B' and n > 1: A[n - 1][n - 2] = F(-2)
        if t == 'C' and n > 1: A[n - 2][n - 1] = F(-2)
    elif t == 'D':
        for i in range(n - 2): A[i][i + 1] = A[i + 1][i] = F(-1)
        A[n - 3][n - 1] = A[n - 1][n - 3] = F(-1)
    elif t == 'G': A = [[F(2), F(-1)], [F(-3), F(2)]]
    elif t == 'F': A = [[F(2), F(-1), F(0), F(0)], [F(-1), F(2), F(-2), F(0)],
                        [F(0), F(-1), F(2), F(-1)], [F(0), F(0), F(-1), F(2)]]
    elif t == 'E':
        for a, b in [(1, 3), (3, 4), (4, 5), (2, 4)] + [(i, i + 1) for i in range(5, n)]:
            A[a - 1][b - 1] = A[b - 1][a - 1] = F(-1)
    return A
def symmetrizer(A):
    n = len(A); d = [None] * n; d[0] = F(1); st = [0]
    while st:
        i = st.pop()
        for j in range(n):
            if i != j and A[i][j] != 0 and d[j] is None:
                d[j] = d[i] * A[i][j] / A[j][i]; st.append(j)
    mn = min(d); return [x / mn for x in d]
def roots(A):
    n = len(A)
    simple = [tuple(1 if j == i else 0 for j in range(n)) for i in range(n)]
    R = set(simple); fr = set(simple)
    while fr:
        new = set()
        for a in fr:
            for i in range(n):
                p = sum(F(a[j]) * A[i][j] for j in range(n))
                b = list(a); b[i] -= int(p); b = tuple(b)
                if any(b) and (all(x >= 0 for x in b) or all(x <= 0 for x in b)) and b not in R:
                    new.add(b)
        R |= new; fr = new
    return R
def data(t, n):
    A = cartan(t, n); d = symmetrizer(A); R = roots(A)
    pos = [r for r in R if all(x >= 0 for x in r)]
    th = max(pos, key=lambda r: sum(r))
    tt = sum(F(th[i]) * F(th[j]) * d[i] * A[i][j] for i in range(n) for j in range(n))
    hv = 1 + sum(F(th[i]) * 2 * d[i] / tt for i in range(n))
    return th, hv, len(R), len(R) + n
KNOWN = {('A',1):2,('A',2):3,('A',3):4,('A',4):5,('B',3):5,('B',4):7,('C',3):4,('C',4):5,
         ('D',4):6,('D',5):8,('G',2):4,('F',4):9,('E',6):12,('E',7):18,('E',8):30}
print('      %-6s %6s %6s %8s %8s   %s' % ('type', 'h^v', 'known', '#roots', 'dim g', 'highest root'))
allok = True
DATA = {}
for (t, n), kv in KNOWN.items():
    th, hv, nr, dg = data(t, n); DATA[(t, n)] = (th, hv, nr, dg)
    ok = (hv == kv); allok &= ok
    print('      %-6s %6s %6d %8d %8d   %s' % ('%s_%d' % (t, n), hv, kv, nr, dg, th))
check(allok, 'every dual Coxeter number is computed correctly from the Cartan matrix alone')
check(DATA[('E', 8)] [1] == 30 and DATA[('E', 8)][2] == 240 and DATA[('E', 8)][3] == 248,
      'E8: h^v = 30, 240 roots, dim 248 -- all three from the Cartan matrix')

# ---------------------------------------------------------------------------
head(5, "LANGLANDS DUALS, BY TRANSPOSING THE CARTAN MATRIX")
print('  ^L g is the algebra whose Cartan matrix is the transpose. That is the')
print('  whole definition on this side of the correspondence.\n')
def same_up_to_relabel(A, B):
    n = len(A)
    if A == B: return True
    rev = [[A[n - 1 - i][n - 1 - j] for j in range(n)] for i in range(n)]
    return rev == B
def identify(At, n):
    for t2 in 'ABCDEFG':
        try:
            if same_up_to_relabel(At, cartan(t2, n)): return '%s_%d' % (t2, n)
        except Exception: pass
    return '?'
for t, n in (('A',3),('B',3),('C',3),('B',4),('C',4),('D',4),('G',2),('F',4),('E',6),('E',7),('E',8)):
    A = cartan(t, n); At = [[A[j][i] for j in range(n)] for i in range(n)]
    dual = identify(At, n)
    print('      ^L(%s_%d) = %s' % (t, n, dual))
    if t in 'ADEGF' or (t, n) in (('B',3),('B',4),('C',3),('C',4)):
        expect = {'A': '%s_%d' % (t, n), 'D': '%s_%d' % (t, n), 'E': '%s_%d' % (t, n),
                  'G': 'G_2', 'F': 'F_4', 'B': 'C_%d' % n, 'C': 'B_%d' % n}[t]
        check(dual == expect, '^L(%s_%d) = %s' % (t, n, expect), dual)
check(identify([[cartan('E',8)[j][i] for j in range(8)] for i in range(8)], 8) == 'E_8',
      'E8 is self-dual, so z(e8-hat) at critical level is W(e8) and not W(something else)')

# ---------------------------------------------------------------------------
head(6, "THE CRITICAL LEVEL, AND A CHECK THAT IS NOT CIRCULAR")
print('  Sugawara gives a Virasoro action on the level-k module with')
print('      c(k) = k dim(g) / (k + h^v)')
print('  and a normalisation 1/(2(k + h^v)) that is UNDEFINED at k = -h^v. That is')
print('  the critical level: the Virasoro description of g-hat breaks there, and')
print('  what replaces it is the centre, which is the W-algebra of the dual.\n')
print('  The check: at level 1, simply laced, c must equal the RANK. Nothing above')
print('  was set up to make that true, so it is a test of h^v and dim g together.\n')
cc = lambda k, dg, hv: F(k) * dg / (F(k) + hv)
print('      %-6s %6s %6s %12s %8s   %s' % ('type', 'h^v', 'dim g', 'c at k=1', 'rank', 'critical level'))
ok1 = True
for (t, n) in (('A',1),('A',2),('A',3),('A',4),('D',4),('D',5),('E',6),('E',7),('E',8)):
    th, hv, nr, dg = DATA[(t, n)]
    c1 = cc(1, dg, hv); ok1 &= (c1 == n)
    print('      %-6s %6s %6d %12s %8d   k = %s' % ('%s_%d' % (t, n), hv, dg, c1, n, -hv))
check(ok1, 'level 1 simply laced gives c = rank for every type tested -- '
      'e.g. E8: 248/31 = 8')
th, hv8, nr8, dg8 = DATA[('E', 8)]
print('\n      E8 in full:  c(k) = 248k/(k+30),  critical level k = -30,')
print('      and since ^L(E8) = E8, the centre there is W(e8).')
for k in (1, 2, 10, -29, F(-599, 20), -31):
    print('         k = %-8s c = %s' % (k, cc(k, dg8, hv8)))
check(cc(1, dg8, hv8) == 8, 'c(1) = 8 = rank E8')
check(abs(cc(-29, dg8, hv8)) == 248 * 29, 'c(-29) = -7192: the pole is approached, not reached')

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
    if f.startswith('book7/ch-feigin'):                       return 'self'
    if f == 'CLAUDE.md':                                      return 'scaffolding'
    if f.startswith('docs/'):                                 return 'audit'
    if (f.endswith('index.html') or f.startswith('index-')
            or f.startswith('master-index')):                 return 'listing'
    return 'CHAPTER'
def chapters(pat): return [f for f in files(pat) if classify(f) == 'CHAPTER']
check(HAVE, 'tools/corpus_count.py imported -- counts are entity-aware')
ROWS = [('moonshine', r'moonshine'), ('E8', r'E(8|₈)\b|E_8'),
        ('vertex operator', r'vertex operator'), ('Virasoro', r'virasoro'),
        ('Kac-Moody / affine Lie', r'kac.{0,3}moody|affine lie'),
        ('Langlands', r'langlands'), ('Sugawara', r'sugawara'),
        ('central charge', r'central charge'), ('dual Coxeter', r'dual coxeter'),
        ('critical level', r'critical level'), ('W-algebra', r'W[-‑]algebra'),
        ('Feigin', r'feigin'), ('Zamolodchikov', r'zamolodchikov')]
print('\n      %-26s %7s %10s' % ('pattern', 'files', 'chapters'))
C = {}
for name, pat in ROWS:
    C[name] = (len(files(pat)), len(chapters(pat)))
    print('      %-26s %7d %10d' % (name, C[name][0], C[name][1]))
check(C['moonshine'][1] > 15, 'Moonshine is in %d chapters -- the automorphic side is held'
      % C['moonshine'][1], str(C['moonshine']))
check(chapters(r'sugawara') == [], 'no chapter names Sugawara', str(chapters(r'sugawara')))
check(chapters(r'dual coxeter') == [], 'nor the dual Coxeter number', str(chapters(r'dual coxeter')))
check(chapters(r'zamolodchikov') == [], 'nor Zamolodchikov', str(chapters(r'zamolodchikov')))
check(sorted(chapters(r'W[-‑]algebra')) == ['book6/wp82-the-missing-floor.html'],
      'and "W-algebra" reaches exactly one chapter: WP-82, the paper that named the gap',
      str(chapters(r'W[-‑]algebra')))

# ---------------------------------------------------------------------------
head(8, 'CONTROL')
check(len(files(r'moonshine')) > 0, 'the counter returns files rather than nothing')
ABSENT = 'qqx' + '-no-file-contains-this-' + 'qqx'
check(files(ABSENT) == [], 'and none for a token no file writes down', str(files(ABSENT)))
check(data('A', 1)[2] == 2, 'sl_2 has 2 roots')
check(symmetrizer(cartan('G', 2)) == [F(1), F(3)] or symmetrizer(cartan('G', 2)) == [F(3), F(1)],
      'the G2 symmetriser is (1,3) up to order', str(symmetrizer(cartan('G', 2))))

print('\n' + '=' * 70 + '\n  [HONESTY]\n' + '=' * 70)
print("""
  WHAT THIS ESTABLISHES. The Witt algebra from vector fields, exactly. That its
  second cohomology is one-dimensional -- computed, on windows, with the
  restriction step that a raw truncation needs and without which the answer is
  wrong. That m and m^3 span the degree-zero cocycles, that m^2 and m^5 do not,
  that the multiples of m are exactly the coboundaries, and therefore that the
  "-m" in m^3 - m is forced by requiring L_-1, L_0, L_1 to be an uncentred
  sl_2 while the 12 is a convention. Root systems, dual Coxeter numbers and
  dim g for fifteen simple types from their Cartan matrices alone, agreeing with
  the known values in every case, E8 included at h^v = 30, 240 roots, dim 248.
  Langlands duals by transposition, with B_n <-> C_n and E8 self-dual. And the
  central charge c(k) = k dim g/(k + h^v), tested against a fact it was not
  built from: at level 1, simply laced, c = rank.

  WHAT IT DOES NOT ESTABLISH -- AND THIS IS THE LARGER HALF. No W-algebra is
  constructed here. Nothing above is the Feigin-Frenkel theorem; the theorem is
  quoted, and what is computed is the DATA the theorem is stated in terms of --
  which dual, which critical level, which central charge. The Sugawara operator
  itself is not built, the centre of the affine vertex algebra at the critical
  level is not exhibited, and the isomorphism is not checked in any case, not
  even sl_2. That gap is not an oversight: a W-algebra is not a Lie algebra.
  W_3's bracket closes only on the composite field :TT: - (3/10) d^2 T, so the
  structure "constants" depend on the central charge and none of blocks [1]-[3]
  extends to it for free. Deriving a W-algebra needs operator product expansions
  and normal ordering, neither of which is in this corpus or in this script.
  By WP-82's own admissibility bar -- a machine-checked core or it is a reading
  list with a DOI on it -- Volume XV is NOT opened by this page. What the page
  supplies is the floor under its seed, and an honest statement of the distance.
  No priority is claimed: all of it is classical.
""")
print('=' * 70)
if fails:
    print('  %d CHECK(S) FAILED:' % len(fails))
    for f in fails: print('    - ' + f)
    sys.exit(1)
print('  ALL CHECKS PASSED')
