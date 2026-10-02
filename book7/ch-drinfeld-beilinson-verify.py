#!/usr/bin/env python3
"""ch-drinfeld-beilinson-verify.py — the volume of the space the geometric
Langlands correspondence is about.

Verification companion to ch-drinfeld-beilinson.html. Standard library only
(fractions). Exact rational arithmetic throughout; no floating point decides
any PASS except the one labelled asymptotic.

The geometric Langlands correspondence is a statement about sheaves on Bun_G,
the moduli stack of G-bundles on a curve. Almost nothing about it is checkable
by hand. One number is: over a finite field, the groupoid of vector bundles on
P^1 can be enumerated completely (Grothendieck: every bundle splits as a sum of
line bundles O(a)), and its total mass  sum 1/|Aut E|  has a closed form
(Siegel-Harder-Weil mass formula):

    sum_{E : rank n, degree d} 1/|Aut E|
        = q^{(n^2-1)(g-1)} / (q-1) * |Pic^0| * zeta_C(2) ... zeta_C(n)

For C = P^1: g = 0, |Pic^0| = 1, zeta(s) = 1 / ((1-q^-s)(1-q^(1-s))).

  [1] rank 2, degree 0:  enumerate O(a)+O(-a), sum exactly, compare.
  [2] rank 2, degree 1:  enumerate O(a)+O(1-a), sum exactly, compare.
  [3] the answer does not depend on the degree (checked: d=0 and d=1 agree).
  [4] dimension: the mass scales like q^{dim Bun_G}, dim = (g-1) dim G = -4
      for GL_2 on P^1 — the one place where 'dimension of the moduli
      stack' is a number you can watch.
  [5] controls — the comparison must be able to fail. Wrong Aut order, a
      dropped zeta factor, and a wrong degree-1 enumeration must NOT match.

    python3 book7/ch-drinfeld-beilinson-verify.py
"""
import sys
from fractions import Fraction as F

FAIL = []
def check(cond, msg):
    print(("    PASS  " if cond else "    FAIL  ") + msg)
    if not cond: FAIL.append(msg)
def head(n, t):
    print('\n' + '=' * 68 + '\n  [%s]  %s\n' % (n, t) + '=' * 68)

def gl2_order(q):
    return (q * q - 1) * (q * q - q)

def zeta_P1(q, s):
    return 1 / ((1 - F(1, q ** s)) * (1 - F(q, q ** s)))

def mass_formula(q, n=2):
    """Siegel-Harder-Weil on P^1: q^{-(n^2-1)} / (q-1) * zeta(2)...zeta(n)."""
    m = F(1, q ** (n * n - 1)) / (q - 1)
    for k in range(2, n + 1):
        m *= zeta_P1(q, k)
    return m

# Aut(O(a)+O(b)), a>=b: diagonal units (q-1)^2 times Hom(O(b),O(a)) = H^0(O(a-b)),
# which has q^(a-b+1) elements. For a=b it is GL_2(F_q) instead.
def aut_order(a, b, q):
    if a == b:
        return gl2_order(q)
    return (q - 1) ** 2 * q ** (a - b + 1)

def enumerate_mass(q, d, terms):
    """Partial sum over bundles O(a)+O(d-a), a >= d-a, first `terms` bundles."""
    tot = F(0)
    a = (d + 1) // 2 if d % 2 else d // 2
    for _ in range(terms):
        tot += F(1, aut_order(a, d - a, q))
        a += 1
    return tot

def exact_mass(q, d):
    """Closed-form value of the full infinite enumeration (geometric tail)."""
    if d % 2 == 0:
        a0 = d // 2
        first = F(1, aut_order(a0, a0, q))
        # a = a0+j, j>=1: Aut = (q-1)^2 q^(2j+1)
        tail = F(1, (q - 1) ** 2 * q ** 3) / (1 - F(1, q * q))
        return first + tail
    else:
        # b = d-a, a-b = 2j+1, j>=0, Aut = (q-1)^2 q^(2j+2)
        return F(1, (q - 1) ** 2 * q ** 2) / (1 - F(1, q * q))

QS = [2, 3, 4, 5, 7, 8, 9, 11, 13, 16, 17, 19, 23, 25, 27, 29, 31, 32]

# ------------------------------------------------------------------ [0]
head(0, 'the enumeration itself: partial sums converge to the closed form')
for d in (0, 1):
    q = 3
    part = enumerate_mass(q, d, 60)
    full = exact_mass(q, d)
    gap = full - part
    check(0 < gap < F(1, 10 ** 25),
          'd=%d, q=3: 60 enumerated bundles within 1e-25 of closed form (gap=%s)'
          % (d, float(gap)))

# ------------------------------------------------------------------ [1]
head(1, 'rank 2, degree 0: sum over O(a)+O(-a) = mass formula')
bad = [q for q in QS if exact_mass(q, 0) != mass_formula(q)]
check(not bad, 'equal, exactly, for all %d field sizes q in %s'
      % (len(QS), QS))

# ------------------------------------------------------------------ [2]
head(2, 'rank 2, degree 1: sum over O(a)+O(1-a) = mass formula')
bad = [q for q in QS if exact_mass(q, 1) != mass_formula(q)]
check(not bad, 'equal, exactly, for all %d field sizes q' % len(QS))

# ------------------------------------------------------------------ [3]
head(3, 'the mass does not depend on the degree')
for d in range(-3, 6):
    bad = [q for q in QS if exact_mass(q, d) != mass_formula(q)]
    # and from the raw enumeration, not the closed form of the series:
    enum_bad = [q for q in (2, 3, 4, 5, 7)
                if not (0 < mass_formula(q) - enumerate_mass(q, d, 80)
                        < F(1, q ** 100))]
    check(not bad and not enum_bad,
          'degree %+d: closed form and 80-bundle enumeration both match the formula' % d)

# ------------------------------------------------------------------ [4]
head(4, 'dimension: mass ~ q^(dim Bun) with dim Bun_GL2(P^1) = -4')
for q in (10 ** 3, 10 ** 6, 10 ** 9):
    ratio = float(mass_formula(q) * q ** 4)
    print('    q = 10^%d :  mass * q^4 = %.9f' % (len(str(q)) - 1, ratio))
q = 10 ** 9
r = float(mass_formula(q) * q ** 4)
check(abs(r - 1) < 1e-8, 'mass * q^4 -> 1 as q -> infinity (dimension -4)')
q = 10 ** 9
r5 = float(mass_formula(q) * q ** 5)
check(r5 > 1e8, 'mass * q^5 diverges: the exponent is not -5')

# ------------------------------------------------------------------ [5]
head(5, 'controls: the comparison can fail')
q = 5
bad_aut = F(1, aut_order(0, 0, q) + 1) + F(1, (q - 1) ** 2 * q ** 3) / (1 - F(1, q * q))
check(bad_aut != mass_formula(q), 'wrong |Aut| for O+O does not match')
no_zeta = F(1, q ** 3) / (q - 1)
check(no_zeta != mass_formula(q), 'formula without the zeta(2) factor does not match')
wrong_deg1 = F(1, (q - 1) ** 2 * q ** 3) / (1 - F(1, q * q))   # Hom dim off by one
check(wrong_deg1 != mass_formula(q), 'wrong Hom dimension in degree 1 does not match')
check(mass_formula(5, 3) != mass_formula(5, 2), 'rank 3 mass differs from rank 2 (formula is sensitive to n)')

print()
if FAIL:
    print('FAILED: %d check(s)' % len(FAIL)); sys.exit(1)
print('all checks passed'); sys.exit(0)
