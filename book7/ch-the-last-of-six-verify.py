#!/usr/bin/env python3
"""
ch-the-last-of-six-verify.py  --  a procedure that emits Ramanujan's series,
and the finite list it can emit them for.

This closes gap G4 of book7/ch-1103-and-26390-verify.py, which said that
everything there was at N = 58 and that "this is the mechanism" rested on one
data point.

THE PROCEDURE. Input: one integer N. No other input.

    1.  q  = exp(-pi sqrt(N))                       [transcendental]
    2.  k  = (theta2(q)/theta3(q))^2,  alpha = k^2  [the singular modulus]
    3.  g^12 = sqrt( (1-alpha)^2 / (4 alpha) )      [Weber class invariant]
    4.  t  = (g^12 + g^-12)/2                       [half the trace]
        -- KEEP N ONLY IF t IS AN INTEGER --
    5.  b  = sqrt(N) (g^12 - g^-12) / (4 sqrt2)
        x  = 1/(256 t^2)
        a  = ( t/(2 sqrt2 pi) - b D ) / F,   F = SUM c_n x^n, D = SUM n c_n x^n

    Output: the series  1/pi = P * SUM (4n)!/(n!)^4 (A + B n) x^n.

Step 4 is the whole selection rule, and it is brutal. Of the 600 values of N
tested below, six survive: N = 2, 6, 10, 18, 22, 58. N = 2 is degenerate --
256x = 1 exactly, the radius of convergence -- which leaves five series.

The last of them is N = 58. That is why Ramanujan's is the fastest series of
its kind: not because 58 was inspired, but because the list stops there.

Run:  python3 book7/ch-the-last-of-six-verify.py
"""

from mpmath import mp, mpf, sqrt, pi, exp, jtheta, nstr, nint
from fractions import Fraction
import math

mp.dps = 150
FAIL = []
TERMS = 300
C = [mpf(math.factorial(4*n)) / mpf(math.factorial(n))**4 for n in range(TERMS)]


def head(n, t):
    print(); print("=" * 78); print("%s. %s" % (n, t)); print("=" * 78)


def half_trace(N, dps=None):
    """Steps 1-4. Returns (g^12, t)."""
    q = exp(-pi * sqrt(mpf(N)))
    th2 = jtheta(2, 0, q); th3 = jtheta(3, 0, q)
    k = (th2 / th3) ** 2          # modulus
    alpha = k ** 2                # parameter -- NOT the same thing; see
    g12 = sqrt((1 - alpha)**2 / (4 * alpha))   # ch-1103-and-26390-verify.py S0
    return g12, (g12 + 1/g12) / 2


def machine(N, t_int):
    """Step 5. Returns (A, B, P, x, residual)."""
    g12, _ = half_trace(N)
    b = sqrt(mpf(N)) * (g12 - 1/g12) / (4 * sqrt(mpf(2)))
    x = mpf(1) / (256 * mpf(t_int)**2)
    F = sum(C[n] * x**n for n in range(TERMS))
    D = sum(n * C[n] * x**n for n in range(TERMS))
    a = (mpf(t_int) / (2 * sqrt(mpf(2)) * pi) - b * D) / F
    fr = Fraction(float(b / a)).limit_denominator(10**6)
    A, B = fr.denominator, fr.numerator
    g = math.gcd(A, B); A //= g; B //= g
    P = (2 * sqrt(mpf(2)) / mpf(t_int)) * (a / A)
    resid = P * sum(C[n] * (A + B*n) * x**n for n in range(TERMS)) - 1/pi
    return A, B, P, x, resid


# ---------------------------------------------------------------------------
head(1, "THE SELECTION RULE -- which N have an integer half-trace")
# ---------------------------------------------------------------------------
LO, HI = 1, 600
print("  Scanning N = %d .. %d at %d digits." % (LO, HI, mp.dps))
print("  t = (g_N^12 + g_N^-12)/2 is kept when it is within 1e-40 of an integer.")
print()
survivors = []
for N in range(LO, HI + 1):
    g12, t = half_trace(N)
    if t > mpf(10) ** 60:
        print("  ... t exceeds 1e60 at N = %d; the scan stops being meaningful" % N)
        HI = N - 1
        break
    if abs(t - nint(t)) < mpf(10) ** -40:
        survivors.append((N, int(nint(t))))
for N, t in survivors:
    print("      N = %-4d   t = %-8d   (g^12 = %s)" % (N, t, nstr(half_trace(N)[0], 16)))
print()
expect = [(2, 1), (6, 3), (10, 9), (18, 49), (22, 99), (58, 9801)]
print("  survivors: %s" % (survivors,))
if survivors != expect:
    FAIL.append("selection rule changed")
    print("  <-- FAIL: expected %s" % (expect,))
else:
    print("  [SHOWN] Exactly six, and N = 58 is the largest, over N = %d .. %d."
          % (LO, HI))
print()
print("  The half-traces are  1, 3, 9, 49, 99, 9801.")
print("  Four of the six are perfect squares: 1, 9 = 3^2, 49 = 7^2, 9801 = 99^2.")
print("  And two of those squares square an entry already on the list:")
print("      N =  6 -> t = 3      N = 10 -> t = 3^2  = 9")
print("      N = 22 -> t = 99     N = 58 -> t = 99^2 = 9801")
print("  so the list contains two (t, t^2) pairs, at (6,10) and (22,58). That")
print("  is stated because it is visible, and not interpreted. See GAPS H6.")

# ---------------------------------------------------------------------------
head(2, "N = 2 IS THE DEGENERATE END")
# ---------------------------------------------------------------------------
print("  t = 1, so x = 1/(256 * 1) and 256x = 1 exactly.")
print("  256x = 1 is the radius of convergence of SUM (4n)!/(n!)^4 (x/256)^n,")
print("  since (4n)!/(n!)^4 ~ 256^n / (2 pi n)^{3/2}. So N = 2 sits ON the")
print("  boundary and emits nothing summable. Five usable N remain.")
# c_n = (4n)!/(n!)^4 ~ 256^n / (2 pi n)^{3/2}, so c_n/c_{n-1}/256 -> 1 from
# below like 1 - 3/(2n). Check the RATE, not just the limit -- a check that
# only asks "is it near 1" would pass for the wrong asymptotic.
for n in (20, 60, 200):
    r = C[n] / C[n-1] / 256
    pred = 1 - mpf(3) / (2*n)
    ok = abs(r - pred) < mpf('0.002')
    print("  [%s] c_%d/c_%d/256 = %s   vs 1 - 3/(2n) = %s"
          % ("SHOWN" if ok else "FAIL ", n, n-1, nstr(r, 10), nstr(pred, 10)))
    if not ok:
        FAIL.append("c_n asymptotic at n=%d" % n)
print("  Approaching 1 from below at rate 3/(2n) is the (2 pi n)^{-3/2} factor.")
print("  So at 256x = 1 the terms go like n^{-3/2} * (A + Bn) ~ n^{-1/2}:")
print("  the series diverges at N = 2, it does not merely converge slowly.")

# ---------------------------------------------------------------------------
head(3, "THE FIVE SERIES, EMITTED AND CHECKED")
# ---------------------------------------------------------------------------
print("  Each line below was produced by the procedure from N alone.")
print()
table = []
for N, t in survivors:
    if N == 2:
        continue
    A, B, P, x, resid = machine(N, t)
    rate = 2 * mp.log(mpf(t), 10)
    table.append((N, t, A, B, P, rate))
    ok = abs(resid) < mpf(10) ** -120
    if not ok:
        FAIL.append("series at N=%d" % N)
    print("  N = %-3d  t = %-5d" % (N, t))
    print("      1/pi = P * SUM (4n)!/(n!)^4 (%d + %d n) / (256 * %d^2)^n"
          % (A, B, t))
    print("      P = %s" % nstr(P, 20))
    print("      [%s] residual = %s      digits/term = %s"
          % ("SHOWN" if ok else "FAIL ", nstr(resid, 5), nstr(rate, 7)))
    print()

print("  Closed forms for P, each checked to 50 places:")
PCLOSED = {6: (1, 3, 6), 10: (2, 2, 9), 18: (3, 3, 49), 22: (1, 11, 198),
           58: (2, 2, 9801)}
for N, t, A, B, P, rate in table:
    p, d, m = PCLOSED[N]
    want = mpf(p) * sqrt(mpf(d)) / mpf(m)
    ok = abs(P - want) < mpf(10) ** -50
    if not ok:
        FAIL.append("P closed form at N=%d" % N)
    print("      [%s] N=%-3d  P = %d sqrt(%d) / %d" %
          ("SHOWN" if ok else "FAIL ", N, p, d, m))

# ---------------------------------------------------------------------------
head(4, "WHY 58 WINS, STATED AS ARITHMETIC")
# ---------------------------------------------------------------------------
print("  Digits per term is 2 log10(t) and nothing else. It is monotone in t.")
print("  So the fastest series in the family is the one with the largest t,")
print("  and t is largest at the largest surviving N.")
print()
print("      %-5s %-8s %-14s" % ("N", "t", "digits/term"))
for N, t, A, B, P, rate in table:
    print("      %-5d %-8d %-14s" % (N, t, nstr(rate, 7)))
print()
print("  8 digits a term is not a property of 58. It is a property of 58 being")
print("  the last entry on a list that stops. The search for a faster series of")
print("  this exact shape is over before it starts -- which is a different kind")
print("  of statement from 'nobody has found one'.")
mono = all(table[i][5] < table[i+1][5] for i in range(len(table)-1))
print("  [%s] digits/term strictly increasing down the list" %
      ("SHOWN" if mono else "FAIL "))
if not mono:
    FAIL.append("rate not monotone")

# ---------------------------------------------------------------------------
head("GAPS", "what this script does not establish")
# ---------------------------------------------------------------------------
for g in [
 "H1  THE LIST IS FINITE ONLY IN THE SCANNED RANGE. Section 1 tests N <= 600.",
 "    It does not prove no larger N has an integer half-trace. The expected",
 "    reason it cannot happen -- class numbers growing, so g_N^12 stops being",
 "    a quadratic unit -- is the theory, and the theory is cited, not shown.",
 "    Until that is closed, 'the last of six' means 'the last below 600'.",
 "",
 "H2  STEP 5 STILL USES THE SERIES. The coefficient a is obtained by solving",
 "    the identity, not by an independent formula. So the procedure verifies",
 "    a shape it was given; it does not derive the shape. Same wall as",
 "    ch-1103-and-26390 S7: integrality is cited.",
 "",
 "H3  THE b FORMULA IS CARRIED OVER, NOT PROVED. b = sqrt(N)(g^12-g^-12)/(4",
 "    sqrt2) was read off N = 58 in the previous chapter and is here shown to",
 "    work at four more N. Five agreements is evidence, not a proof.",
 "",
 "H4  NOVELTY NOT CHECKED. These five series are believed to be in Ramanujan's",
 "    1914 list. This script does not verify the correspondence, and nothing",
 "    here should be read as claiming a new series. The interest is that a",
 "    five-step procedure emits them from N alone.",
 "",
 "H5  A IS FOUND BY limit_denominator. The integer pair (A,B) comes from a",
 "    continued-fraction rationalisation of b/a with denominator bound 10^6.",
 "    That is a search, and a search can miss. The residual check at 120",
 "    places is what makes each output sound; the SEARCH is not certified.",
 "",
 "H6  THE (t, t^2) PAIRING IS UNEXPLAINED. N=6 and N=10 give 3 and 3^2; N=22",
 "    and N=58 give 99 and 99^2. Noted in section 1 because it is visible and",
 "    left there. No relation between the two N in a pair is offered -- 6 to",
 "    10 and 22 to 58 is not an obvious map -- and the corpus's rule is to",
 "    state such a pattern and not interpret it.",
]:
    print("  " + g)

print(); print("=" * 78)
if FAIL:
    print("FAILED: " + ", ".join(FAIL)); raise SystemExit(1)
print("All checks passed. 6 gaps recorded above remain open.")
print("=" * 78)
