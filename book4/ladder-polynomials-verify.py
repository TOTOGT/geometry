#!/usr/bin/env python3
"""
ladder-polynomials-verify.py  --  regenerates every number in
book4/ladder-polynomials.html.

The page carried a "Reproduce" code block and no runnable companion, so the
repo rule that a published number must be regenerable by a tool was not met for
it.  This is that tool.  Blocks follow the page's sections.

  [1] the family collapses to p_n(x) = x^(n+1) - 2x^n + 1, and each q_n is
      irreducible over Q on the tested range;
  [2] the exact gap identity 2 - r_n = r_n^(-n), to 50 digits;
  [3] the ADE / affine spectral threshold at 2;
  [4] phi = 2cos(pi/5) = rho(A_4), and no further coincidence below n = 40;
  [5] discriminants, the Galois groups that are proved, and the n = 8
      transposition witness;
  [6] NEW: the computed discriminants against Luca's closed form
      (Fibonacci Quarterly 62-3, 2024).  Nine independent agreements.

Full run: about a minute.  Pass --slow to redo the p < 60000 transposition
search from scratch instead of checking the recorded witness p = 17921.
"""

import sys

import sympy as sp
from mpmath import mp, mpf, findroot

mp.dps = 60
x = sp.symbols('x')
SLOW = "--slow" in sys.argv
FAIL = []


def check(label, got, want, note=None):
    ok = got == want
    print("  %s %-52s got=%s  want=%s" % ("OK  " if ok else "FAIL", label, got, want))
    if note:
        for line in note.split("\n"):
            print("       " + line)
    if not ok:
        FAIL.append(label)


def q(n):
    return x**n - sum(x**k for k in range(n))


# ------------------------------------------------------------------ [1]
print()
print("[1] the family collapses to one one-parameter polynomial")
collapse = all(
    sp.simplify(sp.expand((x - 1) * q(n)) - (x**(n + 1) - 2 * x**n + 1)) == 0
    for n in range(2, 9))
check("(x-1) q_n(x) = x^(n+1) - 2x^n + 1, n = 2..8", collapse, True,
      "The 2 in the middle coefficient is what the telescoping leaves; it is\n"
      "not put there.")
irred = all(sp.Poly(q(n), x).is_irreducible for n in range(2, 11))
check("q_n irreducible over Q, n = 2..10", irred, True)

# ------------------------------------------------------------------ [2]
print()
print("[2] the gap to tau = 2 is the root's own reciprocal power, exactly")
worst = mpf(0)
for n in range(2, 21):
    r = findroot(lambda z: z**(n + 1) - 2 * z**n + 1,
                 mpf('1.9') if n > 4 else mpf('1.6'))
    worst = max(worst, abs((2 - r) - r**(-n)))
check("max |(2 - r_n) - r_n^(-n)|, n = 2..20, < 1e-40", worst < mpf('1e-40'), True,
      "worst residual %s" % sp.nsimplify(0) if worst == 0 else "worst residual %.3e" % float(worst))

# every r_n is Pisot: conjugates strictly inside the unit disc
pisot = True
maxconj = 0.0
for n in range(2, 13):
    roots = sp.Poly(q(n), x).nroots(n=30)
    mods = sorted(abs(complex(r)) for r in roots)
    maxconj = max(maxconj, mods[-2])
    if mods[-2] >= 1:
        pisot = False
check("every r_n is Pisot, n = 2..12", pisot, True,
      "largest conjugate modulus over the range: %.6f, never reaching 1" % maxconj)

# ------------------------------------------------------------------ [3][4]
print()
print("[3] and [4] the ADE threshold, and the single coincidence at n = 2")


def path_rho(m):
    A = sp.zeros(m, m)
    for i in range(m - 1):
        A[i, i + 1] = A[i + 1, i] = 1
    return max(abs(e) for e in A.eigenvals())


phi = (1 + sp.sqrt(5)) / 2
check("rho(A_4) = phi", sp.simplify(path_rho(4) - phi) == 0, True,
      "phi = 2 cos(pi/5), and 5 is the Coxeter number of A_4.")

from mpmath import acos, pi as MPPI


def ladder_root(n):
    """The unique root of q_n in (1, 2).  Selected, not taken by position:
    nroots() does not order its output, and reading off [-1] silently returns
    a different root for some n."""
    keep = []
    for r in sp.Poly(q(n), x).nroots(n=40):
        re, im = r.as_real_imag()
        if abs(im) < sp.Float('1e-25') and 1 < re < 2:
            keep.append(mpf(str(re)))
    assert len(keep) == 1, "n=%d: expected one root in (1,2), got %r" % (n, keep)
    return keep[0]


check("r_2 is the golden ratio", abs(ladder_root(2) - mpf('1.61803398874989484820458683436564')) < mpf('1e-25'), True,
      "a positional sanity check on the root selector, which an earlier version\n"
      "of this script got wrong by reading nroots()[-1].")

hits = []
for n in range(2, 40):
    h = MPPI / acos(ladder_root(n) / 2)
    for hh in range(3, 61):
        if abs(h - hh) < mpf('1e-6'):
            hits.append((n, hh))
check("coincidences (n, h) with 2cos(pi/h) = r_n, n < 40, h < 60",
      hits, [(2, 5)],
      "Exactly one.  The reason is structural, not numerical: the ladder roots\n"
      "are Pisot (conjugates inside the unit disc) and the numbers 2cos(pi/h)\n"
      "are totally real with all conjugates in [-2, 2].  The families are\n"
      "essentially disjoint and phi is the accident that is both.")

# the n = 5 near miss, flagged on the page so it does not become a false claim
h5 = MPPI / acos(ladder_root(5) / 2)
check("the n = 5 near miss is close to 17 but is not 17",
      mpf('1e-4') < abs(h5 - 17) < mpf('1e-2'), True,
      "h = %.6f.  Off by %.1e.  It is the kind of number that becomes a false\n"
      "claim if nobody computes the next three digits." % (float(h5), float(abs(h5 - 17))))

# ------------------------------------------------------------------ [5]
print()
print("[5] discriminants and Galois groups")

disc = {n: sp.discriminant(sp.expand(q(n)), x) for n in range(2, 11)}
check("disc(q_n), n = 2..10",
      [disc[n] for n in range(2, 11)],
      [5, -44, -563, 9584, 205937, -5390272, -167398247, 6042477824, 249317139869])
def is_rational_square(d):
    d = int(d)
    return d >= 0 and sp.integer_nthroot(d, 2)[1]


nosq = not any(is_rational_square(disc[n]) for n in range(2, 11))
check("no disc(q_n) is a perfect square in Q, n = 2..10", nosq, True,
      "so no rung lies in A_n: every Galois group on the ladder contains an\n"
      "odd permutation.")

groups = {n: sp.galois_group(sp.Poly(q(n), x))[0].order() for n in range(2, 7)}
check("|Gal(q_n)| for n = 2..6", [groups[n] for n in range(2, 7)],
      [2, 6, 24, 120, 720],
      "C_2 at n = 2; S_n from n = 3 to 6.")


def cycle_type_mod(n, p):
    poly = sp.Poly(q(n), x)
    return sorted(int(sp.Poly(f, x).degree())
                  for f, _ in sp.factor_list(poly.as_expr(), modulus=p)[1])


# n = 7 is rigorous: irreducible + degree prime => primitive; one transposition => S_7 (Jordan)
t7 = None
for p in sp.primerange(3, 4000):
    if disc[7] % p == 0:
        continue
    if cycle_type_mod(7, p) == sorted([2] + [1] * 5):
        t7 = p
        break
check("a transposition mod p for n = 7 exists below 4000", t7 is not None, True,
      "first at p = %s.  7 is prime, so transitive implies primitive, and a\n"
      "primitive group containing a transposition is S_n (Jordan).  No sampling\n"
      "assumption enters: one transposition suffices." % t7)

target8 = sorted([2] + [1] * 6)
if SLOW:
    p8 = next(p for p in sp.primerange(3, 60000)
              if disc[8] % p != 0 and cycle_type_mod(8, p) == target8)
else:
    p8 = 17921
check("p = 17921 realises a transposition for n = 8",
      cycle_type_mod(8, p8) == target8, True,
      "The scan to p < 4000 found none.  That was under-sampling against an\n"
      "expected density C(8,2)/8! of about one in 1440, not evidence of absence.\n"
      "8 is not prime, so transitivity does not give primitivity and Jordan does\n"
      "not apply: this note does not prove Gal(q_8) = S_8.  See block [6] for\n"
      "what the literature has to say about that, which this note does not.")

# ------------------------------------------------------------------ [6]
print()
print("[6] the computed discriminants against Luca's closed form")
print("       Luca, Fibonacci Quarterly 62-3 (2024), 'On the discriminant of the")
print("       k-generalized Fibonacci polynomial, II':")
print("         Disc(f_k) = (-1)^(C(k+1,2)-1) [ 2^(k+1) k^k - (k+1)^(k+1) ] / (k-1)^2")

agree = []
for k in range(2, 11):
    sign = (-1)**(sp.binomial(k + 1, 2) - 1)
    d_luca = sp.Rational(sign * (2**(k + 1) * k**k - (k + 1)**(k + 1)), (k - 1)**2)
    agree.append(disc[k] == d_luca)
check("closed form reproduces disc(q_k), k = 2..10", all(agree), True,
      "Nine independent agreements.  The table in this note was computed before\n"
      "the formula was known to it, so this is a genuine cross-check in both\n"
      "directions and not a restatement.")

print()
if FAIL:
    print("FAILED: " + ", ".join(FAIL))
    sys.exit(1)
print("ALL CHECKS PASSED")
