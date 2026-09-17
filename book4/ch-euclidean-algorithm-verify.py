#!/usr/bin/env python3
"""ch-euclidean-algorithm-verify.py -- Book IV, the object worked.

WHY THIS FILE EXISTS. Measured 2026-09-17, entity-aware over tracked files:
"Euclid" appears in 36 files across seven books, "Elements" in 48, "Euclidean"
in 24 -- and **"Euclidean algorithm" in 0**. `gcd` appears in 6.

The corpus computes class numbers by reduced-form counting, runs a Pell solution
as load-bearing work in the Ramanujan 1/pi material, and gives Volume XI an
identity that is entirely the algebraic floor. All of that rests on one
procedure, and the procedure is never named. This chapter names it and works it,
which is Book IV's role: could a reader DO something after reading it?

THE SPINE. Four statements, each checked here, ending on a number the corpus
already publishes:

  1. Euclid's algorithm on (a, b) produces exactly the partial quotients of the
     continued fraction of a/b. Same divisions, read twice.
  2. Its worst case is consecutive Fibonacci numbers (Lame, 1844), so the
     slowest input to the oldest algorithm is the corpus's own phi ladder at
     n = 2.
  3. Run on sqrt(29) it is periodic, [5; 2,1,1,2,10], and its fourth convergent
     70/13 solves x^2 - 29 y^2 = -1.
  4. That solution is eps^3 for eps = (5 + sqrt29)/2, the fundamental unit of
     O_K, and **eps^6 = 9801 + 1820 sqrt29** -- where 9801 = 99^2 is the
     denominator in Ramanujan's 1/pi series.

So the 9801 that `book7/ch-ramanujan-1pi.html` reports and
`docs/math-placement-map.md` places in XI is reachable from Euclid by division
alone. No modular forms are needed to arrive at it, which is not a claim that
none are needed to explain it -- see [HONESTY].

BLOCKS
  [1] The algorithm, and that it terminates.
  [2] Bezout, by the extended form.
  [3] Euclid's quotients ARE the continued fraction.
  [4] Lame: the worst case is the Fibonacci ladder.
  [5] sqrt(29): periodic, and the convergent that solves Pell.
  [6] The fundamental unit, and eps^6 = 9801 + 1820 sqrt29.
  [7] The corpus, counted: the procedure everything rests on is unnamed.
  [8] Control.

Standard library only.  python3 book4/ch-euclidean-algorithm-verify.py
"""
import math, os, random, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools'))

fails = []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg,
                            ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def head(n, t):
    print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)

def euclid(a, b):
    """(gcd, quotients, steps) -- the divisions, kept."""
    q = []
    while b:
        q.append(a // b)
        a, b = b, a % b
    return a, q, len(q)

# ---------------------------------------------------------------------------
head(1, "THE ALGORITHM, AND THAT IT TERMINATES")
print('  Replace (a, b) by (b, a mod b) until b is 0. The remainder strictly')
print('  decreases and is a non-negative integer, so it reaches 0 in finitely')
print('  many steps. What is left is the gcd.\n')
print('      %8s %8s %8s %7s   %s' % ('a', 'b', 'gcd', 'steps', 'quotients'))
for a, b in ((1071, 462), (9801, 1820), (55, 34), (270, 192), (17, 5)):
    g, q, n = euclid(a, b)
    print('      %8d %8d %8d %7d   %s' % (a, b, g, n, q))
    check(g == math.gcd(a, b), 'gcd(%d, %d) = %d agrees with the library' % (a, b, g))
random.seed(29)
bad = 0
for _ in range(4000):
    a, b = random.randint(1, 10 ** 9), random.randint(1, 10 ** 9)
    if euclid(a, b)[0] != math.gcd(a, b): bad += 1
check(bad == 0, 'and agrees on 4000 random pairs up to 10^9', str(bad))

# ---------------------------------------------------------------------------
head(2, "BEZOUT, BY THE EXTENDED FORM")
def ext(a, b):
    if b == 0: return a, 1, 0
    g, x, y = ext(b, a % b)
    return g, y, x - (a // b) * y
print('      %8s %8s   %-28s %s' % ('a', 'b', 'gcd = a x + b y', 'check'))
for a, b in ((1071, 462), (9801, 1820), (240, 46)):
    g, x, y = ext(a, b)
    print('      %8d %8d   %4d = %d(%d) + %d(%d)' % (a, b, g, a, x, b, y))
    check(a * x + b * y == g, 'Bezout holds for (%d, %d)' % (a, b))
bad = 0
for _ in range(3000):
    a, b = random.randint(1, 10 ** 7), random.randint(1, 10 ** 7)
    g, x, y = ext(a, b)
    if a * x + b * y != g or g != math.gcd(a, b): bad += 1
check(bad == 0, 'and on 3000 random pairs', str(bad))
print('\n  That is why the algorithm is load-bearing rather than merely old: it')
print('  returns the certificate, not just the answer. Every modular inverse in')
print('  this corpus is one of these x values.')

# ---------------------------------------------------------------------------
head(3, "EUCLID'S QUOTIENTS *ARE* THE CONTINUED FRACTION")
from fractions import Fraction
def cf_of(fr):
    out = []
    n, d = fr.numerator, fr.denominator
    while d:
        out.append(n // d); n, d = d, n % d
    return out
print('  The divisions of the algorithm on (a, b), read as a list, are the')
print('  partial quotients of a/b. One computation, two readings.\n')
for a, b in ((1071, 462), (355, 113), (9801, 1820), (70, 13)):
    _, q, _ = euclid(a, b)
    c = cf_of(Fraction(a, b))
    print('      %5d/%-5d  euclid %s' % (a, b, q))
    check(q == c, '  and the continued fraction of %d/%d is the same list' % (a, b),
          '%s vs %s' % (q, c))
bad = 0
for _ in range(2000):
    a, b = random.randint(1, 10 ** 6), random.randint(1, 10 ** 6)
    if euclid(a, b)[1] != cf_of(Fraction(a, b)): bad += 1
check(bad == 0, 'identical on 2000 random pairs', str(bad))

# ---------------------------------------------------------------------------
head(4, "LAME: THE WORST CASE IS THE FIBONACCI LADDER")
fib = [1, 1]
for _ in range(20): fib.append(fib[-1] + fib[-2])
print('      %8s %8s %7s   quotients' % ('F(n+1)', 'F(n)', 'steps'))
for i in range(4, 12):
    a, b = fib[i + 1], fib[i]
    g, q, n = euclid(a, b)
    print('      %8d %8d %7d   %s' % (a, b, n, q))
    check(n == i, 'consecutive Fibonacci (%d, %d) costs exactly %d steps' % (a, b, i))
    check(set(q[:-1]) == {1}, '  and every quotient but the last is 1 -- the slowest '
          'possible division', str(q))
worst = {}
for b in range(2, 400):
    for a in range(b + 1, 400):
        n = euclid(a, b)[2]
        if n > worst.get('n', 0): worst = {'n': n, 'a': a, 'b': b}
print('\n      exhaustive search, all pairs under 400: worst is (%d, %d) at %d steps'
      % (worst['a'], worst['b'], worst['n']))
check((worst['a'], worst['b']) == (fib[worst['n'] + 1], fib[worst['n']]),
      'and the worst pair under 400 is a consecutive Fibonacci pair',
      '%d, %d' % (worst['a'], worst['b']))
print("""
  So the slowest input to the oldest algorithm in mathematics is this corpus's
  own ladder at n = 2. The ratio F(n+1)/F(n) -> phi, and phi is the operator
  chain's second constant. The connection is Lame's, not this corpus's: the
  number of steps is bounded by five times the digit count of the smaller
  number, and the bound is attained on Fibonacci pairs.""")

# ---------------------------------------------------------------------------
head(5, "SQRT(29): PERIODIC, AND THE CONVERGENT THAT SOLVES PELL")
def cf_sqrt(n, k):
    a0 = math.isqrt(n); m, d, a = 0, 1, a0; out = [a0]
    for _ in range(k):
        m = d * a - m; d = (n - m * m) // d; a = (a0 + m) // d; out.append(a)
    return out
cf = cf_sqrt(29, 10)
print('      cf(sqrt 29) = %s' % cf)
check(cf[:6] == [5, 2, 1, 1, 2, 10], 'the expansion is [5; 2,1,1,2,10]', str(cf[:6]))
check(cf[1:6] == cf[6:11], 'and it repeats with period 5', str(cf))
h, k = [1, cf[0]], [0, 1]
for ai in cf[1:]:
    h.append(ai * h[-1] + h[-2]); k.append(ai * k[-1] + k[-2])
print('\n      %3s %14s %12s' % ('i', 'convergent', 'p^2 - 29 q^2'))
hit = None
for i in range(1, 7):
    p, q = h[i + 1], k[i + 1]
    v = p * p - 29 * q * q
    print('      %3d %8d/%-5d %12d' % (i, p, q, v))
    if v == -1 and hit is None: hit = (p, q, i)
check(hit == (70, 13, 4), 'the fourth convergent 70/13 gives p^2 - 29 q^2 = -1',
      str(hit))
check(euclid(70, 13)[1] == [5, 2, 1, 1, 2],
      'and running Euclid on 70/13 returns exactly one period of sqrt 29')
check(euclid(9801, 1820)[1] == [5, 2, 1, 1, 2, 10, 2, 1, 1, 2],
      '-- while 9801/1820 returns TWO periods')

# ---------------------------------------------------------------------------
head(6, "THE FUNDAMENTAL UNIT, AND eps^6 = 9801 + 1820 sqrt29")
def mul(x, y):
    a, b = x; c, d = y
    return ((a * c + 29 * b * d) // 2, (a * d + b * c) // 2)
def norm(x):
    return (x[0] ** 2 - 29 * x[1] ** 2) // 4
eps = (5, 1)
print('  29 = 1 mod 4, so O_K = Z[(1 + sqrt29)/2] and eps = (5 + sqrt29)/2.\n')
print('      %6s %26s %8s' % ('power', 'value', 'norm'))
p = eps
print('      %6s %20d + %-5d /2 %6d' % ('eps', p[0], p[1], norm(p)))
check(norm(eps) == -1, 'eps has norm -1')
for n in range(2, 7):
    p = mul(p, eps)
    print('      %6s %20d + %-5d /2 %6d' % ('eps^%d' % n, p[0], p[1], norm(p)))
check(p == (19602, 3640), 'eps^6 = (19602 + 3640 sqrt29)/2', str(p))
check((p[0] // 2, p[1] // 2) == (9801, 1820),
      'which is 9801 + 1820 sqrt29 -- the value docs/math-placement-map.md places in XI')
check(99 * 99 == 9801, 'and 9801 = 99^2, the denominator of Ramanujan\'s 1/pi series')
check(norm(p) == 1, 'eps^6 has norm +1, so it is a Pell solution proper')
print("""
  Reached from Euclid by division alone: run the algorithm on sqrt 29, take the
  convergent where the norm first hits -1, cube the unit it names, square that.
  9801 arrives without a modular form being written down. That is a statement
  about this ROUTE, not about what explains the 1/pi series -- block [HONESTY].""")

# ---------------------------------------------------------------------------
head(7, "THE CORPUS: THE PROCEDURE EVERYTHING RESTS ON IS UNNAMED")
from corpus_count import files                                  # noqa: E402
BASELINE = 'cc9a045'          # last commit before this chapter; see the note below
print('  Counted entity-aware at %s, the commit before this page joined the' % BASELINE)
print('  corpus it measures. A page that names a term cannot be counted as')
print('  evidence that the term was already there.\n')
print('      %-26s %5s' % ('term', 'files'))
ROWS = [('Euclid (any form)', r'\beuclid', 36), ('Elements', r'\belements\b', 48),
        ('Euclidean', r'euclidean', 24), ('gcd', r'\bgcd\b', 6),
        ('continued fraction', r'continued fraction', None),
        ('fundamental unit', r'fundamental unit', None),
        ('Pell', r'\bpell\b', None), ('9801', r'9801', None),
        ('Euclidean algorithm', r'euclidean algorithm', 0)]
got = {}
for lab, pat, want in ROWS:
    n = len(files(pat, ref=BASELINE)); got[lab] = n
    print('      %-26s %5d' % (lab, n))
for lab, pat, want in ROWS:
    if want is not None:
        check(got[lab] == want, '%r reads %d at %s' % (lab, want, BASELINE), str(got[lab]))
check(got['Euclidean algorithm'] == 0 and got['Euclid (any form)'] > 30,
      'Euclid is named in more than thirty files and his algorithm in none')
check(got['9801'] > 0 and got['fundamental unit'] > 0,
      'while 9801 and the fundamental unit are both already in use')

# ---------------------------------------------------------------------------
head(8, "CONTROL")
ABSENT = 'qqx' + '-no-file-writes-this-' + 'qqx'
check(len(files(ABSENT, ref=BASELINE)) == 0, 'a token no file contains returns 0')
check(math.gcd(0, 7) == 7 and euclid(0, 7)[0] == 7, 'gcd(0, 7) = 7, the edge case')
check(euclid(7, 0)[0] == 7 and euclid(7, 0)[2] == 0, 'and gcd(7, 0) costs no steps')
check(euclid(13, 13)[2] == 1, 'equal inputs cost one step')

print("""
======================================================================
  [HONESTY]
======================================================================
  WHAT THIS ESTABLISHES. That the algorithm agrees with the library gcd on 4000
  random pairs to 10^9 and that the extended form returns a Bezout certificate on
  3000 more. That the quotients it produces on (a, b) are identically the
  continued fraction of a/b, on 2000 random pairs. That consecutive Fibonacci
  numbers cost exactly n steps with every quotient but the last equal to 1, and
  that an exhaustive search of all pairs under 400 finds the worst case at a
  Fibonacci pair. That cf(sqrt 29) = [5; 2,1,1,2,10] with period 5; that its
  fourth convergent 70/13 is the first to give norm -1; that Euclid on 70/13
  returns one period and on 9801/1820 returns two. And that for the fundamental
  unit eps = (5 + sqrt29)/2 of O_K, eps^6 = 9801 + 1820 sqrt29 with norm +1,
  where 9801 = 99^2.

  WHAT IT DOES NOT ESTABLISH. It does not explain Ramanujan's 1/pi series. It
  shows that the integer 9801 is reachable from Euclid by division alone, along
  one route; the series itself comes from singular moduli and modular equations,
  which `book4/ch-modular-equations-and-pi.html` works and this page does not
  touch. Treating the arrival of the same integer as an explanation would be the
  vocabulary-correspondence error the placement map warns about in its own
  section 2, and the map places the Pell row in XI as a **core candidate**, not
  as a result. Nor is Lame's theorem proved here: block [4] exhibits the bound
  being attained, which is evidence and not a proof, and the five-times-the-digits
  statement is quoted rather than derived. The periodicity of cf(sqrt n) for
  non-square n is likewise used and not proved. Block [7] is pinned to commit
  cc9a045 because this page names every term it counts. No priority is claimed
  for anything: the algorithm is Elements VII.1-2, Bezout is 1779, Lame is 1844,
  and the unit is classical.
""")
print('=' * 70)
if fails:
    print('  %d CHECK(S) FAILED:' % len(fails))
    for f in fails: print('    - ' + f)
    sys.exit(1)
print('  ALL CHECKS PASSED')
