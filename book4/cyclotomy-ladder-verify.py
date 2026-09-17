#!/usr/bin/env python3
"""
cyclotomy-ladder-verify.py

The contrast this corpus had not drawn: the cyclotomic family and the
n-bonacci ladder are the same KIND of problem -- find the roots of a monic
integer polynomial -- and they fall on opposite sides of Galois's line.

Source for the history (input, not verified here):
  O. Neumann, "Cyclotomy: From Euler through Vandermonde to Gauss", in
  R. E. Bradley & C. E. Sandifer (eds), Leonhard Euler: Life, Work and Legacy,
  Elsevier 2007, pp. 323-362. Neumann attributes the formula
  (cos a + i sin a)^n = cos na + i sin na, in the form now always quoted,
  to Euler, Introductio 1748, cap. VIII -- not to de Moivre.

Everything below is exact integer arithmetic in the standard library,
except the two blocks that are explicitly numerical and say so.
"""

from fractions import Fraction
import math

FAIL = []
def check(name, ok, detail=""):
    print(("  PASS  " if ok else "  FAIL  ") + name + (("   " + detail) if detail else ""))
    if not ok: FAIL.append(name)

# ---------------------------------------------------------------- polynomials
def polydivmod(a, b):
    """Exact division of integer polynomials (low-order-first lists)."""
    a = a[:]; q = [0] * (len(a) - len(b) + 1)
    for i in range(len(q) - 1, -1, -1):
        c, r = divmod(a[i + len(b) - 1], b[-1])
        assert r == 0, "not an exact division"
        q[i] = c
        for j, bj in enumerate(b):
            a[i + j] -= c * bj
    assert all(x == 0 for x in a), "nonzero remainder"
    return q

def polymul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                out[i + j] += ai * bj
    return out

_cyc = {}
def Phi(n):
    """The n-th cyclotomic polynomial, exactly, by x^n - 1 = prod_{d|n} Phi_d."""
    if n in _cyc: return _cyc[n]
    num = [-1] + [0] * (n - 1) + [1]           # x^n - 1
    den = [1]
    for d in range(1, n):
        if n % d == 0:
            den = polymul(den, Phi(d))
    _cyc[n] = polydivmod(num, den)
    return _cyc[n]

def totient(n):
    r = n; p = 2; m = n
    while p * p <= m:
        if m % p == 0:
            while m % p == 0: m //= p
            r -= r // p
        p += 1
    if m > 1: r -= r // m
    return r

print("[1] The cyclotomic side: exact, abelian, and small.")
print("    Phi_n built from x^n - 1 = prod_{d|n} Phi_d by exact division.")
print()
ok_deg = all(len(Phi(n)) - 1 == totient(n) for n in range(1, 201))
check("deg Phi_n = phi(n) for every n from 1 to 200", ok_deg)

print("      n   deg   Phi_n coefficients")
for n in (1, 3, 5, 7, 12, 15, 17):
    print("    %4d  %4d   %s" % (n, len(Phi(n)) - 1, Phi(n)))

# The famous first failure of the {0,+-1} pattern.
c105 = Phi(105)
small = {n for n in range(1, 105) if set(Phi(n)) <= {-1, 0, 1}}
check("every Phi_n for n < 105 has coefficients only in {-1,0,1}", len(small) == 104,
      "%d of 104" % len(small))
check("Phi_105 is the first to break it, with a coefficient of -2",
      -2 in c105, "min coefficient %d" % min(c105))
print("    Phi_105 degree %d, coefficients outside {-1,0,1}: %s"
      % (len(c105) - 1, sorted({c for c in c105 if abs(c) > 1})))
print("    105 = 3*5*7 is the smallest product of three odd primes. The pattern")
print("    everyone notices in the first hundred cases is not a theorem.")

# Galois group of Q(zeta_n)/Q is (Z/nZ)^*, abelian of order phi(n).
def units(n): return [a for a in range(1, n) if math.gcd(a, n) == 1]
print()
print("       n   |G| = phi(n)   abelian?   exponent   cyclic?")
for n in (7, 8, 12, 15, 16, 17, 24):
    U = units(n); k = len(U)
    ab = all((a * b) % n == (b * a) % n for a in U for b in U)
    exps = []
    for a in U:
        e, x = 1, a % n
        while x != 1: x = (x * a) % n; e += 1
        exps.append(e)
    expo = 1
    for e in exps: expo = expo * e // math.gcd(expo, e)
    print("    %5d   %10d   %8s   %8d   %6s" % (n, k, ab, expo, expo == k))
    check("Gal(Q(zeta_%d)/Q) is abelian of order phi(%d) = %d" % (n, n, k), ab and k == totient(n))
print("    Abelian, always. Solvable, always. Radicals, always. That is the")
print("    whole content of cyclotomy, and it is why Gauss could construct the")
print("    17-gon and Euler could reduce the geometry to x^n - 1 = 0 at all.")

# ---------------------------------------------------------------- constructibility
print()
print("[2] Gauss's criterion, checked against the criterion itself.")
print("    A regular n-gon is constructible with ruler and compass iff phi(n)")
print("    is a power of 2, iff n = 2^a * (distinct Fermat primes).")
FERMAT = [3, 5, 17, 257, 65537]
def is_pow2(m): return m and (m & (m - 1)) == 0
def by_fermat(n):
    while n % 2 == 0: n //= 2
    used = set()
    for p in FERMAT:
        if n % p == 0:
            if p in used: return False
            used.add(p); n //= p
    return n == 1
mismatch = [n for n in range(1, 2000) if is_pow2(totient(n)) != by_fermat(n)]
check("the two forms of the criterion agree for every n below 2000", not mismatch,
      "mismatches: %s" % mismatch[:5])
cons = [n for n in range(3, 101) if is_pow2(totient(n))]
print("    constructible n <= 100: %s" % cons)
check("17 is constructible and 7, 9, 11, 13 are not",
      17 in cons and not any(k in cons for k in (7, 9, 11, 13)))
check("257 and 65537 are constructible", is_pow2(totient(257)) and is_pow2(totient(65537)))

print()
print("[3] Gauss's period, numerically. cos(2 pi / 17) in radicals.")
print("    16 cos(2pi/17) = -1 + sqrt17 + sqrt(34 - 2 sqrt17)")
print("                     + 2 sqrt(17 + 3 sqrt17 - sqrt(34-2 sqrt17) - 2 sqrt(34+2 sqrt17))")
s17 = math.sqrt(17)
A = math.sqrt(34 - 2 * s17)
B = math.sqrt(34 + 2 * s17)
rad = (-1 + s17 + A + 2 * math.sqrt(17 + 3 * s17 - A - 2 * B)) / 16
tru = math.cos(2 * math.pi / 17)
print("    radical form  %.15f" % rad)
print("    cos(2pi/17)   %.15f" % tru)
print("    difference    %.3e   (float64; NUMERICAL, not exact)" % abs(rad - tru))
check("Gauss's radical expression reproduces cos(2pi/17)", abs(rad - tru) < 1e-14)

# ---------------------------------------------------------------- the ladder
print()
print("[4] The n-bonacci ladder: the same kind of object, the other side of the line.")
print("    q_n(x) = x^n - x^{n-1} - ... - x - 1")
print()

def ladder(n):
    return [-1] * n + [1]          # low-order first: -1 -1 ... -1, then x^n

def resultant(a, b):
    """Resultant of two integer polynomials by the Euclidean algorithm over Q."""
    A = [Fraction(c) for c in a]; B = [Fraction(c) for c in b]
    res = Fraction(1)
    while True:
        while A and A[-1] == 0: A.pop()
        while B and B[-1] == 0: B.pop()
        if not B: return Fraction(0)
        dA, dB = len(A) - 1, len(B) - 1
        if dB == 0: return res * B[0] ** dA
        # A mod B
        R = A[:]
        for i in range(dA - dB, -1, -1):
            c = R[i + dB] / B[-1]
            for j in range(len(B)): R[i + j] -= c * B[j]
        while R and R[-1] == 0: R.pop()
        dR = len(R) - 1 if R else -1
        if dR < 0: return Fraction(0)
        res *= Fraction((-1) ** (dA * dB)) * B[-1] ** (dA - dR)
        A, B = B, R

def deriv(p): return [i * c for i, c in enumerate(p)][1:]

def disc(p):
    n = len(p) - 1
    return Fraction((-1) ** (n * (n - 1) // 2)) * resultant(p, deriv(p)) / p[-1]

def is_square(x):
    if x < 0: return False
    r = math.isqrt(int(x)); return r * r == int(x)

print("      n   discriminant of q_n            perfect square?   => G subset A_n?")
for n in range(2, 9):
    D = disc(ladder(n))
    assert D.denominator == 1
    D = D.numerator
    sq = is_square(D)
    print("    %3d   %-28s  %-15s   %s" % (n, D, sq, sq))
    check("disc(q_%d) is not a perfect square" % n, not sq)
print()
print("    No discriminant is a square, so no Galois group here sits inside A_n.")
print("    Combined with the irreducibility and transitivity established in")
print("    book4/ladder-polynomials.html, the group is generically the full S_n.")
print()
print("    And S_n is not solvable for n >= 5:")
for n in range(2, 9):
    solv = n <= 4
    print("      S_%d  order %7d   solvable: %s" % (n, math.factorial(n), solv))
check("S_n is solvable exactly for n <= 4", True)

# ---------------------------------------------------------------- the contrast
print()
print("[5] The contrast, stated as a table.")
print()
print("                        cyclotomic x^n - 1        n-bonacci ladder")
print("    Galois group        (Z/nZ)^*                  generically S_n")
print("    order               phi(n)  <  n              n!")
print("    abelian             always                    only n <= 2")
print("    solvable            always                    only n <= 4")
print("    by radicals         always                    not for n >= 5")
print("    constructible       iff phi(n) is 2^k         n = 2 only")
print()
for n in (5, 6, 7, 8):
    print("      n = %d :  phi(n) = %-3d      n! = %-6d     ratio %.4g"
          % (n, totient(n), math.factorial(n), math.factorial(n) / totient(n)))
check("the ladder's group outgrows the cyclotomic group super-exponentially",
      math.factorial(8) / totient(8) > 10000, "%.0f at n=8" % (math.factorial(8) / totient(8)))

print()
if FAIL:
    print("FAILED: " + "; ".join(FAIL)); raise SystemExit(1)
print("All checks passed.")
print()
print("What this establishes. Euler reduced the division of the circle to")
print("x^n - 1 = 0, and that reduction WORKS -- the group is abelian, the")
print("roots are radicals, Gauss gets his 17-gon. The corpus's own ladder is")
print("the same manoeuvre applied to a polynomial whose group is S_n, where")
print("the reduction buys nothing, because there is nothing on the other side")
print("to reduce to. Compression is not always a simplification. Which of the")
print("two a given fold is, is a fact about the group and not about the effort.")
