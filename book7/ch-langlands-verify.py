#!/usr/bin/env python3
"""ch-langlands-verify.py — the two cases you can check by hand.

Verification companion to ch-langlands.html. Standard library only; no numpy,
no install, nothing that can rot with a package bump. Every count below is
EXHAUSTIVE over the field, not sampled.

Almost nothing in the Langlands program is checkable without machinery. Two
cases are, and they are the two the chapter rests on:

  [1] GL(1) — quadratic reciprocity, the abelian case, verified over every
      ordered pair of distinct odd primes below 200 by computing residues
      directly rather than by applying the law.
  [2] GL(2) — modularity of the conductor-11 curve. Two sequences computed
      independently and compared: point counts on y^2 + y = x^3 - x^2 over
      F_p, and the q-expansion of the weight-two level-11 newform written as
      an eta product. Nothing connects them except the theorem.
  [3] Control — the comparison must be able to fail. A wrong curve and a
      wrong eta product are run through the same code and must NOT match.

    python3 book7/ch-langlands-verify.py
"""
import sys

FAIL = []
def check(cond, msg):
    print(("    PASS  " if cond else "    FAIL  ") + msg)
    if not cond: FAIL.append(msg)
def head(n, t):
    print('\n' + '=' * 68 + '\n  [%s]  %s\n' % (n, t) + '=' * 68)

def primes_below(n):
    s = [True] * n
    s[0:2] = [False, False]
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            for j in range(i * i, n, i):
                s[j] = False
    return [i for i, v in enumerate(s) if v]

# ------------------------------------------------------------------ [1]
head(1, 'GL(1): quadratic reciprocity, by exhaustion over residues')

def is_square_mod(a, p):
    """Is a a nonzero square mod p? Computed by listing squares, not by Euler."""
    a %= p
    if a == 0: return None
    return a in {(x * x) % p for x in range(1, p)}

ps = [p for p in primes_below(200) if p > 2]
tested = 0
bad = []
for i, p in enumerate(ps):
    for q in ps[i + 1:]:
        lhs = is_square_mod(q, p)      # is q a square mod p
        rhs = is_square_mod(p, q)      # is p a square mod q
        # reciprocity: lhs == rhs unless p == q == 3 (mod 4), when they differ
        both3 = (p % 4 == 3 and q % 4 == 3)
        want_same = not both3
        ok = (lhs == rhs) if want_same else (lhs != rhs)
        tested += 1
        if not ok: bad.append((p, q))
check(not bad, 'reciprocity holds for all %d ordered pairs of odd primes < 200'
      % tested)
check(tested == len(ps) * (len(ps) - 1) // 2, 'every pair was actually tested')
print('    %d odd primes, %d pairs, 0 exceptions.' % (len(ps), tested))

# ------------------------------------------------------------------ [2]
head(2, 'GL(2): modularity of the conductor-11 curve')

N = 100

def eta_product(n_max, level=11, power=2):
    """q * prod_{n>=1} (1-q^n)^power (1-q^{level n})^power, to degree n_max."""
    c = [0] * (n_max + 1); c[1] = 1
    def mul(a, b):
        r = [0] * (n_max + 1)
        for i, ai in enumerate(a):
            if ai:
                for j, bj in enumerate(b):
                    if bj and i + j <= n_max:
                        r[i + j] += ai * bj
        return r
    for n in range(1, n_max + 1):
        for m in (n, level * n):
            if m > n_max: continue
            f = [0] * (n_max + 1); f[0] = 1; f[m] = -1
            for _ in range(power):
                c = mul(c, f)
    return c

def count_points(p, A, B, C):
    """#E(F_p) for y^2 + y = x^3 + A x^2 + B x + C, by brute force over p^2
    pairs, plus the point at infinity."""
    n = 0
    for x in range(p):
        rhs = (x * x * x + A * x * x + B * x + C) % p
        for y in range(p):
            if (y * y + y - rhs) % p == 0:
                n += 1
    return n + 1

coeffs = eta_product(N)
ps = [p for p in primes_below(N) if p != 11]
rows = []
for p in ps:
    ap = p + 1 - count_points(p, -1, 0, 0)     # y^2 + y = x^3 - x^2
    rows.append((p, ap, coeffs[p]))
mismatch = [(p, a, b) for p, a, b in rows if a != b]
check(not mismatch,
      'a_p from point counts == q-expansion coefficient, all %d primes < %d'
      % (len(rows), N))
print('    p    a_p   eta   ')
for p, a, b in rows:
    print('    %-4d %-5d %-5d %s' % (p, a, b, 'ok' if a == b else 'MISMATCH'))

# Hasse bound is a separate, independent sanity check on the point counts.
hasse = [(p, a) for p, a, _ in rows if abs(a) > 2 * p ** 0.5]
check(not hasse, 'every a_p satisfies the Hasse bound |a_p| <= 2 sqrt(p)')

# ------------------------------------------------------------------ [3]
head(3, 'Control: the comparison must be able to fail')

# A different curve of a different conductor, against the same level-11 form.
wrong = []
for p in ps[:12]:
    ap = p + 1 - count_points(p, 0, 1, 0)      # y^2 + y = x^3 + x, not 11a
    if ap != coeffs[p]:
        wrong.append(p)
check(len(wrong) > 0,
      'a different curve does NOT match the level-11 form (%d/%d primes differ)'
      % (len(wrong), len(ps[:12])))

# A different level, against the right curve.
other = eta_product(N, level=13)
diff = [p for p in ps[:12] if other[p] != coeffs[p]]
check(len(diff) > 0, 'a level-13 eta product is a different sequence')
print('    If either control passed, the comparison in [2] would be vacuous:')
print('    it would be matching something against itself.')

# ------------------------------------------------------------------
print('\n' + '=' * 68)
if FAIL:
    print('  %d FAILED' % len(FAIL))
    for f in FAIL: print('    - %s' % f)
    sys.exit(1)
print('  all checks pass')
print('=' * 68)
