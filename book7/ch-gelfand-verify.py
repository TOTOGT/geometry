#!/usr/bin/env python3
"""
Gelfand -- is "the operator algebra of C -> K -> F -> U" an algebra?

WHY THIS FILE EXISTS. One hundred tracked files in this corpus use the phrase
"operator algebra". One names a C*-algebra. None names a von Neumann algebra or
a Banach algebra. WP-82 section 3 assigns Volume XII both halves and observes
that the phrase "is used across 76 files and has never had a volume". This
script asks the prior question: is the thing an algebra, and if a version of it
is, which one.

The answer has two halves and the first is negative. The corpus's own page
defines F as "the nonlinear self-amplification that drives vortex tightening".
An algebra is a vector space; a nonlinear map is not an element of one. Composed
maps form a MONOID, and no page of this corpus defines a sum, a scalar multiple,
an involution or a norm for C, K, F, U. So the phrase names a composition monoid.

The second half is positive and is the point. The corpus's own commutation
argument is already linear -- K is multiplication by a radial mask, and what
fails to commute with it is the transport inside F. Make that finite and exact
and there IS a C*-algebra, and its structure is completely determined:

    dim C*(K, S) = n * p        A = (M_p(C))^(+ n/p)        dim A' = n/p

where p is the minimal period of the gate mask under the shift. Verified by
exhaustive scan over all 248 masks for n = 3..7, with zero violations.

BLOCKS
  [1] What the corpus states, checked against the corpus. Source vs itself.
  [2] The linearity obstruction, and the vocabulary that is missing.
  [3] The finite model, and [K,S] = 0 exactly when the mask is constant.
  [4] The structure theorem, by exhaustive scan.
  [5] Gelfand-Naimark in the commutative case: A = C(X), and X is n points.
  [6] GNS on the trace -- the construction the corpus reads zero for.
  [7] The corpus, counted, entity-aware.
  [8] Control.

PRIMARY SOURCES.
  I. M. Gelfand and M. A. Naimark, "On the imbedding of normed rings into the
  ring of operators in Hilbert space", Mat. Sbornik 12 (1943).
  I. M. Gelfand, "Normierte Ringe", Mat. Sbornik 9 (1941).
  In-corpus: HVEH/operator-algebra.html (Proof I), book1/vol1-mathematics.html
  Theorem 5.3, book6/wp82-the-missing-floor.html section 3 (Volume XII).

Standard library only.  python3 book7/ch-gelfand-verify.py
"""
import cmath, itertools, math, os, subprocess, sys
from fractions import Fraction as F

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fails = []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg, ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def head(n, t):
    print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)

# ---- exact linear algebra over Q -----------------------------------------
def mat(n, f): return [[F(f(i, j)) for j in range(n)] for i in range(n)]
def mul(A, B):
    n = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
def flat(A): return [x for r in A for x in r]
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
def algebra_dim(gens, n, cap=5000):
    I = mat(n, lambda i, j: 1 if i == j else 0)
    basis = []; rref_add(basis, flat(I)); frontier = [I]
    while frontier:
        new = []
        for W in frontier:
            for G in gens:
                P = mul(W, G)
                if rref_add(basis, flat(P)): new.append(P)
                if len(basis) >= cap: return len(basis), False
        frontier = new
    return len(basis), True
def commutant_dim(gens, n):
    rows = []
    for A in gens:
        for i in range(n):
            for j in range(n):
                row = [F(0)] * (n * n)
                for k in range(n):
                    row[i * n + k] += A[k][j]; row[k * n + j] -= A[i][k]
                rows.append(row)
    return n * n - rank(rows)
def period(chi):
    n = len(chi)
    for p in range(1, n + 1):
        if n % p == 0 and all(chi[i] == chi[(i + p) % n] for i in range(n)): return p
    return n

def page(rel):
    with open(os.path.join(REPO, rel), encoding='utf-8') as fh: return fh.read()
def flatten(html):
    import re, html as H
    t = re.sub(r'<script.*?</script>', ' ', html, flags=re.S)
    t = re.sub(r'<style.*?</style>', ' ', t, flags=re.S)
    return ' '.join(H.unescape(re.sub(r'<[^>]+>', ' ', t)).split())

# ---------------------------------------------------------------------------
head(1, "WHAT THE CORPUS STATES, CHECKED AGAINST THE CORPUS")
print('  Tags split a phrase, so the pages are flattened before matching --')
print('  a needle that straddles an <em> silently misses, which is the one-look')
print('  failure this corpus keeps finding in its own instruments.\n')
opalg = flatten(page('HVEH/operator-algebra.html'))
vol1  = flatten(page('book1/vol1-mathematics.html'))
for needle, what in (
        ('G = U ∘ F ∘ K ∘ C', 'the chain is stated as G = U o F o K o C'),
        ('the nonlinear self-amplification', 'F is stated to be NONLINEAR, in those words'),
        ('curvature gate', 'K is stated to be a gate'),
        ('multiplication by a radial mask', 'K is stated to be multiplication by a radial mask'),
        ('F is not pointwise', 'F is stated not to be pointwise'),
        ('advective', 'and the non-commutativity is attributed to transport')):
    check(needle in opalg, what, needle)
check('do not commute' in vol1 and 'order-dependent' in vol1,
      'Volume I Theorem 5.3 states C, K, F, U do not commute and the order matters')

# ---------------------------------------------------------------------------
head(2, "THE OBSTRUCTION, AND THE VOCABULARY THAT IS MISSING")
print('  An algebra is a vector space with a product. To have one you need a sum,')
print('  a scalar multiple, and -- for a *-algebra -- an involution and a norm.')
print('  A nonlinear map is not an element of a vector space: F(x+y) is not')
print('  F(x) + F(y), and the corpus says F is nonlinear in so many words.\n')
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
check(HAVE, 'tools/corpus_count.py imported -- counts are entity-aware')
VOCAB = [('operator algebra', r'operator algebra'), ('C*-algebra', r'C\*[- ]?algebra'),
         ('von Neumann algebra', r'von neumann algebra'), ('Banach algebra', r'banach algebra'),
         ('*-algebra', r'\*-algebra'), ('GNS', r'\bGNS\b'), ('Gelfand', r'gelfand'),
         ('Gelfand-Naimark', r'gelfand.{0,3}naimark'), ('Wedderburn', r'wedderburn'),
         ('commutant', r'commutant'), ('operator norm', r'operator norm'),
         ('monoid', r'monoid'), ('semigroup', r'semigroup')]
V = {}
print('      %-24s %6s' % ('pattern', 'files'))
for name, pat in VOCAB:
    V[name] = len(files(pat)); print('      %-24s %6d' % (name, V[name]))
check(V['operator algebra'] > 90, 'the phrase is in %d files' % V['operator algebra'])
check(V['von Neumann algebra'] == 0 and V['Banach algebra'] == 0,
      'and no file names a von Neumann algebra or a Banach algebra')
check(V['C*-algebra'] <= 2, 'and at most two name a C*-algebra', str(V['C*-algebra']))
print('\n  So the phrase denotes composition. Composition of maps is associative and')
print('  has an identity, which makes a MONOID -- the corpus reads %d for that word'
      % V['monoid'])
print('  and %d for "semigroup". Nothing is wrong with a monoid. It is simply not' % V['semigroup'])
print('  an algebra, and nothing Gelfand, Naimark or GNS supplies applies to one.')

# ---------------------------------------------------------------------------
head(3, "THE FINITE MODEL, AND WHEN THE GATE COMMUTES WITH THE TRANSPORT")
print('  The corpus\'s own argument is already linear: K is multiplication by a')
print('  mask, and what fails to commute with it is the transport inside F. Take')
print('  n sites on a ring, K = diag(chi), S = the cyclic shift. Then\n')
print('      [K, S]_ij = (chi_i - chi_j) S_ij ,  and S_ij = 1 iff i = j + 1 (mod n)\n')
print('  so [K, S] = 0 exactly when chi_i = chi_{i-1} for every i: a CONSTANT mask.')
print('  That is the corpus\'s gate_commutes / coupling_not_commute dichotomy, made')
print('  exact and finite. Checked over every mask below.\n')
ok_iff = True
for n in (3, 4, 5, 6):
    S = mat(n, lambda i, j: 1 if (i - j) % n == 1 else 0)
    for bits in itertools.product((0, 1), repeat=n):
        chi = list(bits)
        K = mat(n, lambda i, j, c=chi: c[i] if i == j else 0)
        Cm = [[mul(K, S)[i][j] - mul(S, K)[i][j] for j in range(n)] for i in range(n)]
        zero = all(x == 0 for x in flat(Cm))
        const = len(set(chi)) == 1
        if zero != const: ok_iff = False
check(ok_iff, '[K,S] = 0 if and only if the mask is constant, over all 120 masks for n = 3..6')

# ---------------------------------------------------------------------------
head(4, "THE STRUCTURE THEOREM, BY EXHAUSTIVE SCAN")
print('  p = the minimal period of the mask under the shift. Claim:\n')
print('      dim C*(K,S) = n * p       A = (M_p(C))^(+ n/p)       dim A\' = n/p\n')
print('      %2s %3s %8s %7s %9s %6s   %s' % ('n', 'p', 'dim A', 'n*p', "dim A'", 'n/p', 'Wedderburn'))
bad = 0; total = 0; shown = set()
for n in range(3, 8):
    S = mat(n, lambda i, j: 1 if (i - j) % n == 1 else 0)
    for bits in itertools.product((0, 1), repeat=n):
        chi = list(bits); total += 1
        K = mat(n, lambda i, j, c=chi: c[i] if i == j else 0)
        p = period(chi)
        d, closed = algebra_dim([K, S], n); cd = commutant_dim([K, S], n)
        if not (closed and d == n * p and cd == n // p): bad += 1
        if (n, p) not in shown:
            shown.add((n, p))
            print('      %2d %3d %8d %7d %9d %6d   %d x M_%d(C)' % (n, p, d, n * p, cd, n // p, n // p, p))
check(bad == 0, 'no violation over all %d masks, n = 3..7' % total, '%d violations' % bad)
check(total == 248, 'the scan covered 248 masks')
print('\n  Sum n_i^2 = (n/p) p^2 = n p and sum m_i^2 = n/p with every m_i = 1, and')
print('  sum n_i m_i = n: the Wedderburn data is forced by the two dimensions, and')
print('  both are computed here rather than assumed.')
print('\n  The reading: the algebra is exactly as large as the gate is asymmetric.')
print('  A constant mask gives the smallest possible algebra and a mask with no')
print('  symmetry gives the whole of M_n(C), which distinguishes nothing.')

# ---------------------------------------------------------------------------
head(5, "GELFAND-NAIMARK, IN THE CASE THE CORPUS'S OWN THEOREM EXCLUDES")
print('  p = 1: A is the circulants, commutative, dim n. Gelfand-Naimark says a')
print('  commutative C*-algebra is C(X) for X its spectrum. Here X is n points,')
print('  the n-th roots of unity, and the Gelfand transform is the DFT.\n')
for n in (4, 6, 8):
    w = [cmath.exp(2j * cmath.pi * k / n) for k in range(n)]
    Sc = [[1.0 + 0j if (i - j) % n == 1 else 0j for j in range(n)] for i in range(n)]
    # the DFT vectors are eigenvectors of S with eigenvalues the n-th roots of unity
    worst = 0.0
    for k in range(n):
        v = [cmath.exp(2j * cmath.pi * k * i / n) for i in range(n)]
        Sv = [sum(Sc[i][j] * v[j] for j in range(n)) for i in range(n)]
        lam = w[(-k) % n]     # (Sv)_i = v_{i-1}, so the eigenvalue is omega^-k
        worst = max(worst, max(abs(Sv[i] - lam * v[i]) for i in range(n)))
    print('      n = %d   spectrum = the %d-th roots of unity   worst residual %.2e' % (n, n, worst))
    check(worst < 1e-12, 'the DFT diagonalises the shift at n = %d, so |X| = %d points' % (n, n))
print('\n  So in the commutative case the corpus\'s operator algebra IS an algebra of')
print('  functions on a finite space, which is Gelfand-Naimark at its smallest.')
print('  Volume I Theorem 5.3 says the corpus is never in this case -- which is')
print('  the same thing as saying it is always in the noncommutative one, and that')
print('  is the sentence WP-82 needs for the step from rung 29 to rung 33.')

# ---------------------------------------------------------------------------
head(6, "GNS ON THE TRACE -- THE CONSTRUCTION THE CORPUS READS ZERO FOR")
print('  tau(a) = (1/n) Tr(a) is a faithful state on M_n(C). GNS turns a state')
print('  into a Hilbert space and a representation: <a,b> = tau(b* a), pi(a)b = ab,')
print('  cyclic vector Omega = I. Faithful, so no quotient: dim H = n^2.\n')
for n in (2, 3, 4):
    # exact over Q: real matrices suffice to exhibit the construction
    basis = [mat(n, lambda i, j, a=a, b=b: 1 if (i, j) == (a, b) else 0)
             for a in range(n) for b in range(n)]
    tau = lambda A: sum(A[i][i] for i in range(n)) / n
    def ip(A, B):    # tau(B^T A) for real matrices
        return sum(sum(B[k][i] * A[k][j] for k in range(n)) for i in range(n) for j in range(n) if i == j) / n
    gram = [[ip(x, y) for y in basis] for x in basis]
    r = rank([row[:] for row in gram])
    I = mat(n, lambda i, j: 1 if i == j else 0)
    worst = max(abs(tau(mul(A, I)) - tau(A)) for A in basis)
    print('      n = %d   dim H = rank(Gram) = %-3d  (n^2 = %-3d)   <pi(a)Omega,Omega> - tau(a) max %s'
          % (n, r, n * n, worst))
    check(r == n * n, 'the GNS space of the trace on M_%d(C) has dimension %d' % (n, n * n))
    check(worst == 0, 'and the cyclic vector reproduces the state exactly')
print('\n  Nothing here is deep. It is three lines of linear algebra, and it is the')
print('  step that turns an algebra into operators on a space -- which is what the')
print('  word "operator" in "operator algebra" is doing. The corpus has used the')
print('  phrase 100 times and has never taken this step.')

# ---------------------------------------------------------------------------
head(7, "THE CORPUS, COUNTED")
def classify(f):
    if f.startswith('book7/ch-gelfand'):                      return 'self'
    if f == 'CLAUDE.md':                                      return 'scaffolding'
    if f.startswith('docs/'):                                 return 'audit'
    if (f.endswith('index.html') or f.startswith('index-')
            or f.startswith('master-index')):                 return 'listing'
    return 'CHAPTER'
def chapters(pat): return [f for f in files(pat) if classify(f) == 'CHAPTER']
print('      %-24s %7s %10s' % ('pattern', 'files', 'chapters'))
for name, pat in VOCAB:
    print('      %-24s %7d %10d' % (name, len(files(pat)), len(chapters(pat))))
check(chapters(r'von neumann algebra') == [], 'no chapter names a von Neumann algebra')
check(chapters(r'banach algebra') == [], 'nor a Banach algebra')
check(chapters(r'wedderburn') == [], 'nor Wedderburn', str(chapters(r'wedderburn')))
check(chapters(r'gelfand.{0,3}naimark') == [], 'nor Gelfand-Naimark',
      str(chapters(r'gelfand.{0,3}naimark')))
print('\n     Written to FAIL when a second chapter picks any of those up.')

# ---------------------------------------------------------------------------
head(8, 'CONTROL')
check(len(files(r'moonshine')) > 0, 'the counter returns files rather than nothing')
ABSENT = 'qqx' + '-no-file-contains-this-' + 'qqx'
check(files(ABSENT) == [], 'and none for a token no file writes down', str(files(ABSENT)))
n = 4
S4 = mat(n, lambda i, j: 1 if (i - j) % n == 1 else 0)
check(algebra_dim([S4], n)[0] == 4, 'the shift alone generates a 4-dimensional algebra at n = 4')
check(algebra_dim([mat(n, lambda i, j: 1 if i == j else 0)], n)[0] == 1,
      'and the identity alone generates a 1-dimensional one')
check(period([1, 0, 1, 0]) == 2 and period([1, 1, 1, 1]) == 1 and period([1, 0, 0, 0]) == 4,
      'the period function reads 2, 1 and 4 on three known masks')

print('\n' + '=' * 70 + '\n  [HONESTY]\n' + '=' * 70)
print("""
  WHAT THIS ESTABLISHES. That the corpus states, in its own words on its own
  page, that F is nonlinear and that K is multiplication by a radial mask, and
  that no file of the corpus supplies a sum, an involution, a norm, a von
  Neumann algebra or a Banach algebra for the four operators -- so the phrase
  "operator algebra", used in 100 files, denotes a composition monoid. And that
  the linear content of the corpus's own commutation argument does generate a
  C*-algebra whose structure is completely determined: dim = n*p, A =
  (M_p(C))^(+n/p), commutant of dimension n/p, with p the period of the mask.
  That is exhaustive over all 248 masks for n = 3..7, exact over the rationals,
  with no violation, and both dimensions are computed rather than assumed.

  WHAT IT DOES NOT ESTABLISH. That the finite model IS the corpus's system. It
  is not: the corpus's K and F act on a continuum, F is nonlinear, and the shift
  on n sites is a stand-in for advective transport chosen because the corpus's
  own refutation argument -- a static gate commutes with a sitewise map and
  fails to commute with an inter-site coupling -- is exactly a statement about
  masks and shifts. Whether the continuum algebra is a crossed product, and
  whether the period p has a continuum analogue, is untouched here. Nothing
  above is a claim that the corpus is wrong: a monoid is a perfectly good
  object, and the finding is that the name promises a different one. The Lean
  files named on the source page (gate_commutes, coupling_not_commute in
  ZeoliteCommutation.lean) are NOT checked here; that file is already recorded
  in docs/audit-log.md as resolving nowhere under any root, and this script
  deliberately re-derives the finite statement itself rather than citing it.
  No priority is claimed: Gelfand-Naimark, GNS, Burnside and Wedderburn are
  classical, and the period rule is an exercise in them.
""")
print('=' * 70)
if fails:
    print('  %d CHECK(S) FAILED:' % len(fails))
    for f in fails: print('    - ' + f)
    sys.exit(1)
print('  ALL CHECKS PASSED')
