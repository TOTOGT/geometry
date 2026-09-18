#!/usr/bin/env python3
"""
ch-1103-and-26390-verify.py  -- the constants in Ramanujan's 1/pi series.

    1/pi = (2 sqrt2 / 9801) * SUM_{n>=0} (4n)!/(n!)^4 * (1103 + 26390 n) / 396^{4n}

The corpus has been quoting 1103 and 26390. Quoting is [CITED]. This script
asks where they come from and answers as much of that as can be computed.

WHAT IS ESTABLISHED HERE
  A. eps = (5+sqrt29)/2 is the fundamental unit of Q(sqrt29);
     eps^3 = 70 + 13 sqrt29  (norm -1),  eps^6 = 9801 + 1820 sqrt29  (norm +1).
  B. The Weber invariant g_58^12 IS eps^6. Verified to 200 places.
     So 9801 is half the trace of a unit, not a decoration.
  C. 396^4 = 256 * 9801^2, exactly, in integers. The 256 is the 256 already
     inside (4n)!/(n!)^4. So the series' real argument is 1/9801^2 and 396 is
     a costume.
  D. 26390 = 29*1820/2 = 13*29*70 -- built from the coefficients of eps^3 and
     eps^6. Stated without numerology as the exact identity
         2 sqrt2 * 26390 / 9801 = sqrt58 * tanh(6 log eps).
  E. 1103 is FORCED. Not fitted: for any integer b with |b| < 5*10^8, the
     equation admits a = 1103 and no other integer.
  F. 8*1103 = 8824 is the coefficient of sqrt2 * eps^6 in the elliptic alpha
     function alpha(58). So 1103 sits inside the same object 9801 and 26390
     come from. Verified to 250 places.

WHAT IS NOT ESTABLISHED HERE -- see GAPS at the end. In particular this script
does not derive that a and b must be INTEGERS. That is the modular theory, and
it is cited, not shown.

Run:  python3 book7/ch-1103-and-26390-verify.py
"""

from mpmath import (mp, mpf, sqrt, pi, exp, log, tanh, jtheta, ellipk, ellipe,
                    nstr, floor, mpmathify)
import math

mp.dps = 320
FAIL = []


def check(tag, name, got, want, tol_dps, note=""):
    """Assert |got - want| < 10^-tol_dps. Record, print, never silently pass."""
    d = abs(mpf(got) - mpf(want))
    ok = d < mpf(10) ** (-tol_dps)
    line = "  [%s] %-52s  |diff| = %s" % (tag, name, nstr(d, 4))
    if not ok:
        line += "   <-- FAIL (wanted < 1e-%d)" % tol_dps
        FAIL.append(name)
    print(line)
    if note:
        print("        " + note)
    return ok


def head(n, t):
    print()
    print("=" * 78)
    print("%s. %s" % (n, t))
    print("=" * 78)


# ---------------------------------------------------------------------------
head(0, "THE MODULUS AT N = 58 -- and the trap this corpus has already paid for")
# ---------------------------------------------------------------------------
# k(q) = (theta2/theta3)^2 is the MODULUS. alpha = k^2 is the PARAMETER.
# Returning (theta2/theta3)^2 where k^2 was wanted -- or the reverse -- is the
# error recorded in book4/ch-modular-equations-and-pi.html, where it survived
# to the fifth digit before a closed form caught it. Ramanujan made it too.
# The guard below is the cheapest possible statement of which is which.
N = 58
q = exp(-pi * sqrt(mpf(N)))
th2 = jtheta(2, 0, q)
th3 = jtheta(3, 0, q)
k = (th2 / th3) ** 2          # the modulus k
alpha = k ** 2                # the parameter alpha = k^2
kp = sqrt(1 - k ** 2)         # complementary modulus k'

print("  q = e^(-pi sqrt58) = %s" % nstr(q, 14))
print("  k_58              = %s" % nstr(k, 24))
print("  alpha_58 = k^2    = %s" % nstr(alpha, 24))
# GUARD: K'/K must be exactly sqrt(N). If k and alpha were swapped it is not.
K = ellipk(alpha)             # mpmath's ellipk takes the PARAMETER m = k^2
Kp = ellipk(1 - alpha)
check("SHOWN", "K'/K = sqrt(58)  (confirms k vs alpha not swapped)",
      Kp / K, sqrt(mpf(58)), 200)

# ---------------------------------------------------------------------------
head(1, "THE UNIT -- eps = (5 + sqrt29)/2, and its cube and sixth power")
# ---------------------------------------------------------------------------
s29 = sqrt(mpf(29))
s2 = sqrt(mpf(2))
s58 = sqrt(mpf(58))
eps = (5 + s29) / 2

# These are integer identities. Check them in integers, not in floats.
print("  eps^3 = 70 + 13 sqrt29 :  norm = 70^2 - 13^2*29 = %d" % (70**2 - 13**2*29))
print("  eps^6 = 9801 + 1820 sqrt29 : norm = 9801^2 - 1820^2*29 = %d"
      % (9801**2 - 1820**2*29))
assert 70**2 - 13**2*29 == -1, "eps^3 norm"
assert 9801**2 - 1820**2*29 == 1, "eps^6 norm"
check("SHOWN", "eps^3 = 70 + 13 sqrt29", eps**3, 70 + 13*s29, 250)
check("SHOWN", "eps^6 = 9801 + 1820 sqrt29", eps**6, 9801 + 1820*s29, 250)
print("        eps^6 has norm +1, so eps^-6 = 9801 - 1820 sqrt29 and")
print("        eps^6 + eps^-6 = 19602 = 2 * 9801  -- 9801 is HALF A TRACE.")
check("SHOWN", "eps^6 + eps^-6 = 19602", eps**6 + eps**-6, 19602, 250)

# ---------------------------------------------------------------------------
head(2, "9801 IS A CLASS INVARIANT -- g_58^12 = eps^6")
# ---------------------------------------------------------------------------
# Weber: g_N^24 = (1-alpha)^2 / (4 alpha).  Computed from the modulus above,
# not from the product formula, so this is independent of any q-product
# truncation.
g24 = (1 - alpha) ** 2 / (4 * alpha)
g12 = sqrt(g24)
print("  g_58^12 = %s" % nstr(g12, 26))
print("  eps^6   = %s" % nstr(eps**6, 26))
check("SHOWN", "g_58^12 = eps^6", g12, eps**6, 200,
      "This is the whole reason 9801 appears. Cross-ref:\n"
      "        book4/ch-modular-equations-and-pi.html (g_58^12 and its 5 ppm near-miss)\n"
      "        book4/ch-euclidean-algorithm.html      (eps^6 = 9801 + 1820 sqrt29)")

# ---------------------------------------------------------------------------
head(3, "396 IS A COSTUME -- 396^4 = 256 * 9801^2, in integers")
# ---------------------------------------------------------------------------
print("  396^4        = %d" % 396**4)
print("  256 * 9801^2 = %d" % (256 * 9801**2))
assert 396**4 == 256 * 9801**2, "396^4 != 256*9801^2"
print("  equal: True   (396 = 4*99 and 9801 = 99^2, so this is 4^4 * 99^4)")
print()
print("  And 256 is not a new number either. The standard factorial identity")
print("      (4n)!/(n!)^4 = 256^n * (1/4)_n (1/2)_n (3/4)_n / (n!)^3")
print("  puts a 256^n in the numerator. It cancels the 256 in 396^4.")
# verify the factorial identity for small n, exactly, in integers
def poch(a_num, a_den, n):
    """(a)_n for a = a_num/a_den, returned as an exact Fraction."""
    from fractions import Fraction
    r = Fraction(1)
    for j in range(n):
        r *= Fraction(a_num, a_den) + j
    return r
from fractions import Fraction
for n in range(0, 7):
    lhs = Fraction(math.factorial(4*n), math.factorial(n)**4)
    rhs = (Fraction(256)**n * poch(1, 4, n) * poch(1, 2, n) * poch(3, 4, n)
           / Fraction(math.factorial(n))**3)
    assert lhs == rhs, ("256^n identity fails at n=%d" % n)
print("  (4n)!/(n!)^4 = 256^n (1/4)_n(1/2)_n(3/4)_n/(n!)^3 verified exactly, n = 0..6")
print()
print("  So the series' argument is 256/396^4 = 1/9801^2 :")
x = mpf(1) / mpf(396) ** 4
check("SHOWN", "256 / 396^4 = 1 / 9801^2", 256 * x, mpf(1)/mpf(9801)**2, 280)
print("        The series is a series in 1/9801^2. Every 396 on the page is")
print("        4 * 99 wearing a fourth power.")

# ---------------------------------------------------------------------------
head(4, "THE SERIES ITSELF -- does it hold?")
# ---------------------------------------------------------------------------
TERMS = 45
c = [mpf(math.factorial(4*n)) / mpf(math.factorial(n)) ** 4 for n in range(TERMS)]
F = sum(c[n] * x**n for n in range(TERMS))            # SUM c_n x^n
D = sum(n * c[n] * x**n for n in range(TERMS))        # SUM n c_n x^n
pref = 2 * s2 / mpf(9801)
check("SHOWN", "Ramanujan's series, %d terms" % TERMS,
      pref * (1103 * F + 26390 * D), 1 / pi, 300)
print("  F = SUM c_n x^n   = %s" % nstr(F, 26))
print("  D = SUM n c_n x^n = %s" % nstr(D, 26))

# ---------------------------------------------------------------------------
head(5, "WHY IT IS FAST -- and it is the same fact as 9801")
# ---------------------------------------------------------------------------
rate = 2 * mp.log(mpf(9801), 10)
print("  each term shrinks by 256 x = 1/9801^2, so digits per term = 2 log10(9801)")
print("  = %s" % nstr(rate, 12))
# measured, not asserted: ratio of successive terms
meas = mp.log(abs(c[1] * x / (c[2] * x**2)), 10)
print("  measured log10(term1/term2) = %s" % nstr(meas, 12))
print("  It is short of the asymptotic rate because c_{n+1}/c_n reaches 256")
print("  only in the limit; at n = 1 it is 105. The rate is approached from")
print("  below, so 7.98 is a ceiling the series climbs toward, not a promise")
print("  about its first terms.")
check("SHOWN", "digits/term = 2 log10(9801)", rate, mpf('7.982538'), 5)
print()
print("  9801 is large because eps^6 is large; eps^6 is large because eps is")
print("  the fundamental unit of a field with a large regulator. The series")
print("  converges fast for an arithmetic reason, not a lucky one.")

# ---------------------------------------------------------------------------
head(6, "26390 -- the n-coefficient is sqrt58 tanh(6 log eps)")
# ---------------------------------------------------------------------------
print("  26390 = 29*1820/2 = %d      13*29*70 = %d" % (29*1820//2, 13*29*70))
assert 26390 == 29*1820//2 == 13*29*70
print("  1820 is the sqrt29-part of eps^6; 13 and 70 are the parts of eps^3.")
print()
print("  Stated so that it is an identity and not a coincidence: the whole")
print("  n-coefficient of the series, prefactor included, is")
print()
print("      2 sqrt2 * 26390 / 9801  =  sqrt58 * tanh(6 log eps)")
print()
B = 2 * s2 * mpf(26390) / 9801
check("SHOWN", "2 sqrt2 * 26390/9801 = sqrt58 tanh(6 log eps)",
      B, s58 * tanh(6 * log(eps)), 280)
print("  B       = %s" % nstr(B, 28))
print("  sqrt58  = %s" % nstr(s58, 28))
print("  B/sqrt58 - 1 = %s   (this is -2/(eps^12 + 1), exactly)" % nstr(B/s58 - 1, 8))
check("SHOWN", "B/sqrt58 = 1 - 2/(eps^12 + 1)",
      B / s58, 1 - 2 / (eps**12 + 1), 280)

# ---------------------------------------------------------------------------
head(7, "1103 -- forced, not fitted")
# ---------------------------------------------------------------------------
T = mpf(9801) / (2 * s2 * pi)          # what a*F + b*D must equal
print("  Write the identity as  a*F + b*D = T,  T = 9801/(2 sqrt2 pi).")
print("  T = %s" % nstr(T, 26))
print("  T - 1103 = %s" % nstr(T - 1103, 10))
print()
print("  D = %s, so |b*D| < 1/2 for every integer b with" % nstr(D, 10))
bound = mpf('0.5') / D
print("  |b| < %s  --  that is |b| < 5*10^8." % nstr(bound, 10))
print("  For any such b, a = (T - b*D)/F is within 1/2 of T, and T is within")
print("  3*10^-5 of the integer 1103. So a = 1103 or a is not an integer.")
print()
# demonstrate: a is forced across the whole admissible range of b
worst = mpf(0)
for b in (-500000000, -26390, -1, 0, 1, 26390, 500000000):
    a_req = (T - b * D) / F
    worst = max(worst, abs(a_req - 1103))
    print("      b = %12d  ->  a = %s" % (b, nstr(a_req, 14)))
ok = worst < mpf('0.5')
print("  [%s] worst deviation of a from 1103 over that range = %s"
      % ("SHOWN" if ok else "FAIL ", nstr(worst, 10)))
print("        which is below 1/2 -- with no margin to spare at the ends.")
if not ok:
    FAIL.append("a not forced")
print()
print("  With a = 1103 fixed, b is then determined outright:")
b_forced = (T - 1103 * F) / D
print("      b = (T - 1103 F)/D = %s" % nstr(b_forced, 26))
check("SHOWN", "b forced by a = 1103 is 26390", b_forced, 26390, 25)
print()
print("  UNIQUENESS, and its exact scope. The argument above needs no")
print("  irrationality and no theory: it is the bound |b*D| < 1/2 and nothing")
print("  else. So what is proved is BOUNDED uniqueness --")
print()
print("      (1103, 26390) is the only integer pair with |b| <= 5*10^8.")
print()
print("  Unbounded uniqueness would follow from F/D being irrational, since")
print("  two solutions force (a-a')F + (b-b')D = 0. This script cannot say")
print("  that. Its F and D are 45-term truncations, hence rational by")
print("  construction, so a rationality test on them tests the truncation and")
print("  not the series. What the test below does establish is that no")
print("  rational of small height sits at F/D, which is the only thing a")
print("  bounded search could have collided with:")
from mpmath import pslq
rel = pslq([F/D, mpf(1)], maxcoeff=10**14, maxsteps=10**5, tol=mpf(10)**-250)
print("      F/D = %s" % nstr(F/D, 22))
print("      pslq(F/D, 1), coefficients < 10^14, 250 places -> %s" % (rel,))
if rel is not None:
    FAIL.append("F/D matched a low-height rational")
print("  Note F/D is 1024635736.25 to eight decimals and is NOT that number;")
print("  it misses by 8*10^-9. Reading the printed digits would have gone")
print("  wrong here, which is the reason the test is run and not eyeballed.")

# ---------------------------------------------------------------------------
head(8, "1103 INSIDE THE ELLIPTIC ALPHA FUNCTION")
# ---------------------------------------------------------------------------
E = ellipe(alpha)
Ep = ellipe(1 - alpha)
a58 = Ep / K - pi / (4 * K ** 2)       # the elliptic alpha function at N=58
print("  alpha(58) = E'/K - pi/(4K^2) = %s" % nstr(a58, 34))
print("  It is algebraic. Its expression on the basis {1, sqrt29, sqrt2, sqrt58}")
print("  of Q(sqrt2, sqrt29) is unique, and it is:")
print()
print("      alpha(58) = 8824 sqrt2 eps^6 + sqrt58 - 122306883 - 22711818 sqrt29")
print()
closed = 8824 * s2 * eps**6 + s58 - 122306883 - 22711818 * s29
check("SHOWN", "alpha(58) closed form", a58, closed, 250)
print("  and  8824 = 8 * 1103, with 1103 prime -- so that factorisation is")
print("  forced, not chosen. Equivalently, on the basis the sqrt2-block is")
print("      8824*9801 = %d   and   8824*1820 + 1 = %d" % (8824*9801, 8824*1820+1))
assert 8824*9801 == 86484024 and 8824*1820+1 == 16059681
print("  1103 is therefore not a stranger to 9801 and 26390. All three live in")
print("  the same object: the unit eps and the alpha function built on it.")
print()
print("  BASE RATE, stated because this corpus requires it. The closed form is")
print("  a unique expression on a fixed basis, verified to 250 places -- there")
print("  is no search and no choice in it. The only reading-in is writing")
print("  8824 as 8*1103, and since 1103 is prime and 8824 = 2^3 * 1103, that")
print("  factorisation is the only one available. What is NOT shown is that")
print("  this is the mechanism rather than a consequence. See GAPS.")

# ---------------------------------------------------------------------------
head(9, "THE NEAR-MISSES, MEASURED")
# ---------------------------------------------------------------------------
e58 = exp(pi * sqrt(mpf(58)))
print("  e^(pi sqrt58)      = %s" % nstr(e58, 22))
print("  396^4              = %d" % 396**4)
print("  396^4 - e^(pi sq58)= %s   (not 104; 104 plus 1.8e-7)"
      % nstr(mpf(396)**4 - e58, 14))
check("SHOWN", "396^4 - e^(pi sqrt58) is near 104", mpf(396)**4 - e58, 104, 6)
print()
print("  26390/1103 = %s" % nstr(mpf(26390)/1103, 20))
print("  pi sqrt58  = %s" % nstr(pi*s58, 20))
print("  difference = %s   -- a near-miss, not an identity."
      % nstr(mpf(26390)/1103 - pi*s58, 10))
if abs(mpf(26390)/1103 - pi*s58) < mpf(10)**-12:
    FAIL.append("ratio was an identity after all")
print("  The corpus does not get to call this one exact. It is the same")
print("  near-miss as e^(pi sqrt58) being close to an integer, seen twice.")

# ---------------------------------------------------------------------------
head("GAPS", "what this script does not establish")
# ---------------------------------------------------------------------------
GAPS = [
 "G1  INTEGRALITY IS CITED, NOT SHOWN. Section 7 forces a = 1103 GIVEN that a",
 "    is an integer, and then b. That a and b must be integers at all is the",
 "    modular theory (Ramanujan 1914; Borwein & Borwein, Pi and the AGM, ch.5).",
 "    Nothing here proves it.",
 "",
 "G2  NO CLOSED FORM FOR 1103. Section 8 finds 8*1103 inside alpha(58) and",
 "    stops there. It does not run the derivation the other way -- from the",
 "    alpha function to the coefficient -- which is what would make 1103 as",
 "    derived as 9801 and 26390 now are.",
 "",
 "G3  THE tanh IDENTITY IS VERIFIED, NOT DERIVED. Section 6 checks",
 "    2sqrt2*26390/9801 = sqrt58 tanh(6 log eps) to 280 places. It is exact",
 "    rational arithmetic once expanded, so the check is sound; but no",
 "    argument here says WHY the n-coefficient should be a tanh of the",
 "    regulator. That is the shape of the general theorem and is not proved.",
 "",
 "G4  ONE VALUE OF N. Everything is at N = 58. The claims are stated about 58",
 "    and nothing here tests whether the same descriptions hold at other N in",
 "    the family (N = 22, 37, 142, ...). Until they do, 'this is the mechanism'",
 "    is one data point.",
 "",
 "G5  THE MODULUS COMES FROM mpmath's jtheta. The k_58 above is computed, not",
 "    proved; its closed form is not derived here. Section 0's K'/K test is a",
 "    guard against the swap error, not a proof of the value.",
 "",
 "G7  UNIQUENESS IS BOUNDED. Section 7 proves the integer pair is unique for",
 "    |b| <= 5*10^8 and no further. Unbounded uniqueness needs F/D irrational,",
 "    which cannot be tested on a truncated series -- see the note there.",
 "",
 "G6  CONVERGENCE RATE IS ASYMPTOTIC. Section 5's 7.98 digits/term is the",
 "    limiting rate. The early terms are slower and the script prints the",
 "    measured n=1 -> n=2 ratio rather than smoothing it.",
]
for g in GAPS:
    print("  " + g)

print()
print("=" * 78)
if FAIL:
    print("FAILED: " + ", ".join(FAIL))
    raise SystemExit(1)
print("All checks passed. %d gaps recorded above remain open." % 7)
print("=" * 78)
