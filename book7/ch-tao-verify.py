#!/usr/bin/env python3
"""
Tao -- what changing the measure buys, computed.

WHY THIS FILE EXISTS. Book 3, Ch.H says the Collatz conjecture "is visible from
within the crystal geometry before it is axiomatic within it," and that "the gap
between visibility and proof is a gap in formal language, not in underlying
truth." That sentence is either a real insight or a comfortable one, and nothing
in the corpus tests which. Tao's 2019 Collatz paper is the case where somebody
closed a gap of exactly that shape -- not by finding new truth, but by changing
the language the statement was made in -- so it is the right thing to hold the
sentence against.

Standard library only.  python3 book7/ch-tao-verify.py
"""

import math, sys

fails = []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg,
                            ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def head(n, t):
    print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)

# ---------------------------------------------------------------------------
head(1, 'THE MAP, AND THE FACT THAT NOBODY DOUBTS THE ANSWER')
print('  Col(N) = 3N+1 for odd N, N/2 for even. Col_min(N) is the least value')
print('  the orbit of N ever reaches.\n')

def col_min_and_peak(n):
    lo, hi, x = n, n, n
    while x != 1:
        x = 3*x + 1 if x % 2 else x // 2
        lo = min(lo, x); hi = max(hi, x)
    return min(lo, 1), hi

LIM = 200000
worst_peak, worst_n = 0, 0
for n in range(1, LIM + 1):
    lo, hi = col_min_and_peak(n)
    if hi > worst_peak: worst_peak, worst_n = hi, n
check(True, 'every orbit up to %d reaches 1' % LIM)
print('     tallest excursion below %d: n = %d rises to %d (%.0fx its start)'
      % (LIM, worst_n, worst_peak, worst_peak / worst_n))
print('\n    The conjecture is not in numerical doubt and never has been. What is')
print('    missing is a proof, and that is the whole subject.')

# ---------------------------------------------------------------------------
head(2, "KOREC'S RESULT, AND WHAT 'ALMOST ALL' MEANT BEFORE 2019")
korec = math.log(3) / math.log(4)
print('  Korec: for any theta > log3/log4, Col_min(N) <= N^theta for almost all')
print('  N -- in the sense of NATURAL density.\n')
check(abs(korec - 0.7924812504) < 1e-9,
      'log 3 / log 4 = %.10f, the paper\'s ~0.7924' % korec)
print('     so the bound was still a POWER of N. Col_min(N) <= N^0.7925 says')
print('     an orbit starting at a trillion need only come down to about ten')
print('     billion. That is very far from saying it reaches 1.')

# ---------------------------------------------------------------------------
head(3, 'THE TWO DENSITIES ARE NOT THE SAME INSTRUMENT')
print("""  Tao 2019 proves: for ANY f with f(N) -> infinity, Col_min(N) <= f(N) for
  almost all N -- in the sense of LOGARITHMIC density. The bound went from a
  power of N to an arbitrarily slow function. The measure changed too, and the
  obvious question is whether that is a weakening dressed as a strengthening.

  It is not, and here is a set that shows why. Take

      A = { n : the leading decimal digit of n is 1 }

  Natural density     d(A)    = lim (1/N) #{n <= N : n in A}
  Logarithmic density dlog(A) = lim (1/log N) sum_{n <= N, n in A} 1/n
""")
c, ss = 0, 0.0
marks = sorted({2*10**k - 1 for k in range(1, 8)} | {10**k - 1 for k in range(2, 9)})
rows = []
for n in range(1, marks[-1] + 1):
    if str(n)[0] == '1':
        c += 1; ss += 1.0 / n
    if n in marks:
        rows.append((n, c/n, ss/math.log(n)))
print('     %12s %18s %18s' % ('N', 'natural (partial)', 'logarithmic'))
for n, nat, lg in rows:
    print('     %12d %18.4f %18.6f' % (n, nat, lg))
print('\n     log10(2) = %.6f' % math.log10(2))

# Marks below 1000 are pre-asymptotic -- at N = 19 the partial is 0.5789, still
# 0.023 from the value it settles on. Test the lock-on where it has locked, and
# say which rows were excluded rather than loosening the tolerance to hide them.
lows  = [nat for n, nat, _ in rows if str(n)[0] == '9' and n >= 1000]
highs = [nat for n, nat, _ in rows if str(n)[0] == '1' and n >= 1000]
check(max(lows) - min(lows) < 1e-3 and max(highs) - min(highs) < 1e-3,
      'from N = 1000 up, the natural-density partials lock onto TWO values',
      'spreads %.4f / %.4f' % (max(lows)-min(lows), max(highs)-min(highs)))
print('     (the N = 19 and N = 99 rows are pre-asymptotic and excluded from')
print('      that check: 0.5789 has not yet reached the 0.5556 it settles on)')
check(abs(min(highs) - 0.5556) < 1e-3 and abs(min(lows) - 0.1111) < 1e-3,
      'those values are ~0.5556 and ~0.1111, four decades apart and not closing',
      '%.4f / %.4f' % (min(highs), min(lows)))
logs9 = [lg for n, _, lg in rows if str(n)[0] == '9']
check(all(logs9[i] > logs9[i+1] for i in range(len(logs9)-1)),
      'the logarithmic column decreases monotonically toward log10(2)')
check(logs9[-1] > math.log10(2), 'and stays above it, as it must')
print('\n     Natural density of A does not exist -- the limit oscillates forever.')
print('     Logarithmic density does, and equals log10(2). Convergence is slow,')
print('     like 1/log N, which is why the last row is still 0.319 and not 0.301.')
print('     One measure cannot see this set at all. The other can.')
print('\n     THAT is what Tao changed. Not a weaker claim in the same language --')
print('     the same claim in a language that can state it.')

# ---------------------------------------------------------------------------
head(4, 'THE OTHER PROJECT: A MAP OF WHICH THEORIES IMPLY WHICH')
EQ = 4694
print('  The Equational Theories Project, opened 25 September 2024: every')
print('  equational law of magmas using at most four operations, ordered by')
print('  implication, each implication settled and checked in Lean.\n')
print('     equational laws              : %s' % f'{EQ:,}')
print('     ordered pairs to resolve     : %s x %s = %s'
      % (f'{EQ:,}', f'{EQ-1:,}', f'{EQ*(EQ-1):,}'))
check(EQ * (EQ - 1) == 22028942,
      'the stated 22,028,942 implications is exactly 4694 x 4693',
      str(EQ*(EQ-1)))
print('\n     This is Volume XIII Chapter 9 at industrial scale: not one dictionary')
print('     between two theories, but the entire directed graph of them, machine-')
print('     checked. A corpus asking "what does an interpretation transport?" has')
print('     a worked atlas of that question to read.')

# ---------------------------------------------------------------------------
head(5, 'CONTROL: THIS SCRIPT COMPUTED SOMETHING')
check(worst_peak > 10 * worst_n, 'the Collatz loop actually ran and found a real excursion')
check(len(rows) >= 12, 'the density table has %d rows' % len(rows))
check(c > 10000000, 'the leading-digit scan counted %s members of A' % f'{c:,}')
print('    A vacuous pass is a pass. Block [5] exists so that block [3] cannot')
print('    report a divergence by having summed nothing.')

# ---------------------------------------------------------------------------
head('HONESTY', 'What this establishes, and what it must not be read as.')
print("""
  ESTABLISHED. Korec's exponent is log3/log4. Natural and logarithmic density
  are genuinely different instruments, demonstrated on a set the first cannot
  measure and the second can. The Equational Theories Project's implication
  count is exactly 4694 x 4693. Collatz orbits below 200,000 all terminate.

  NOT ESTABLISHED, AND THE POINT OF SAYING SO. Tao did not prove the Collatz
  conjecture and this chapter must never be read as saying he did. "Almost all"
  in logarithmic density leaves a set of exceptions that could still be infinite
  and could still contain a divergent orbit. The conjecture is open.

  AND THE PART THAT BEARS ON THIS CORPUS. Book 3 Ch.H holds that the gap between
  seeing Collatz in the crystal geometry and proving it there is "a gap in formal
  language, not in underlying truth." Tao's paper is the strongest evidence that
  such gaps are real and closable -- and his own writing is the strongest warning
  about them: "The point of rigour is not to destroy all intuition; instead, it
  should be used to destroy BAD intuition while clarifying and elevating GOOD
  intuition." Nothing distinguishes a true "I can see it" from a false one except
  the work of trying to write it down. Ch.H's sentence is a hypothesis about
  which kind it has, and it has not been tested. This script does not test it
  either. It only shows what testing one looks like.
""")

print('=' * 70)
if fails:
    print('  %d CHECK(S) FAILED' % len(fails))
    for f in fails: print('    - ' + f)
    print('=' * 70); sys.exit(1)
print('  ALL CHECKS PASSED')
print('=' * 70)
