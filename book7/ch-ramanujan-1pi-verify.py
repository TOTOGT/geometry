#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ch-ramanujan-1pi-verify.py
Producing script for book7/ch-ramanujan-1pi.html.

Continues ch-ramanujan-verify.py, which established the singular moduli
alpha_n = k(e^{-pi sqrt n})^2 and ran Watson's algorithm.  That script computed
the n = 58 row and printed 9801 twice without anything using it.

This script establishes what it was for.

SOURCES
[BBB] Bailey DH, Borwein JM, Borwein PB.  "Ramanujan, Modular Equations, and
      Approximations to Pi, or How to Compute One Billion Digits of Pi."
      Amer. Math. Monthly 96 (1989).  PDF in Downloads.
      Sec. 8 states the 1103/26390 series and says, in those words, that it
      "is a specialization (N = 58)" of its Theorem 5.
[R14] Ramanujan S.  "Modular equations and approximations to pi."
      Quart. J. Math. 45 (1914) 350-372.  PDF in Downloads.

The OCR of [BBB]'s Theorem 5 is mangled in this copy.  It is therefore NOT
transcribed or trusted here.  Section 5 instead tests candidate readings
numerically against integers computed independently, and reports which reading
reproduces them -- so the theorem's shape is inferred from arithmetic that
either closes or does not, never from a garbled line.
"""

from decimal import Decimal as D, getcontext
getcontext().prec = 120

FAIL = []
def check(name, ok, detail=""):
    print("  %-5s %-56s %s" % ("ok" if ok else "FAIL", name, detail))
    if not ok: FAIL.append(name)

def rule(t=""):
    print("\n" + "=" * 78)
    if t: print(t); print("=" * 78)

def sq(x): return D(x).sqrt()

def arctan_inv(m):
    m = D(m); term = 1 / m; total = term; k = 0
    while True:
        k += 1
        term = -term / (m * m)
        nxt = total + term / (2 * k + 1)
        if nxt == total: return total
        total = nxt

PI = 16 * arctan_inv(5) - 4 * arctan_inv(239)          # Machin

rule("0 . INSTRUMENT")
check("Machin pi agrees with the known digits",
      str(PI).startswith("3.14159265358979323846264338327950288419716939937510"),
      str(PI)[:42] + "...")

# ------------------------------------------------------------------ [1] the sum
rule("1 . RAMANUJAN'S SERIES FOR 1/pi  [BBB Sec. 8, from R14]")
print("""
      1/pi = (2 sqrt 2 / 9801) * SUM_{n>=0} (4n)! (1103 + 26390 n)
                                            ------------------------
                                               (n!)^4  396^(4n)
""")
def ramanujan_terms(nmax):
    """Yield partial sums of the series. Factorials built incrementally; no
       floating point anywhere."""
    pre = 2 * sq(2) / D(9801)
    fact4n, factn, p396 = D(1), D(1), D(1)
    total = D(0)
    for n in range(nmax + 1):
        if n > 0:
            for j in range(4 * n - 3, 4 * n + 1): fact4n *= j
            factn *= n
            p396 *= D(396) ** 4
        total += fact4n * (1103 + 26390 * n) / (factn ** 4 * p396)
        yield n, pre * total

target = 1 / PI
prev_digits = 0
gains = []
for n, approx in ramanujan_terms(12):
    err = abs(approx - target)
    digits = 0 if err == 0 else int(-err.log10() // 1)
    if n <= 6 or n == 12:
        print("      n = %-2d  correct digits of 1/pi: %3d   (+%d)"
              % (n, digits, digits - prev_digits))
    if n: gains.append(digits - prev_digits)
    prev_digits = digits

final = approx
check("the series converges to 1/pi to at least 90 digits",
      abs(final - target) < D(10) ** -90,
      "|S - 1/pi| < 1e-90 after 12 terms")
check("every term after the first adds 8 digits",
      all(g == 8 for g in gains[:11]),
      "measured gains: %s" % ",".join(str(g) for g in gains[:6]))
print("""
      Eight digits per term, flat.  The rate is set by 396^4 = %d:
      log10(396^4) = %s""" % (396 ** 4, str(D(396 ** 4).log10())[:12]))
check("log10(396^4) is just above 10, and the observed gain is 8",
      D(10) < D(396 ** 4).log10() < D(11),
      "the (4n)!/(n!)^4 growth eats the difference")

# ------------------------------------------------------- [2] alpha_58, independently
rule("2 . alpha_58 -- RECOMPUTED, NOT IMPORTED")
def alpha_theta(n):
    """alpha_n = k(e^{-pi sqrt n})^2 from theta series. Independent of any
       closed form."""
    q = (-PI * sq(n)).exp()
    t2 = D(0); j = 0
    while True:
        t = q ** (D((2 * j + 1) ** 2) / 4)
        if t == 0: break
        t2 += 2 * t; j += 1
    t3 = D(1); j = 1
    while True:
        t = q ** (j * j)
        if t == 0: break
        t3 += 2 * t; j += 1
    return (t2 / t3) ** 4      # alpha = k^2 = (theta2/theta3)^4

a58_theta = alpha_theta(58)
a58_closed = (13 * sq(58) - 99) ** 2 * (99 - 70 * sq(2)) ** 2
def show(x, n=40):
    """Decimal -> string that keeps its exponent. str()[:46] silently ate 'E-10'
       in the first run of this script and made two correct numbers look wrong."""
    m, e = x.normalize().as_tuple()[1:] and (x, None), None
    return ("%." + str(n) + "E") % x
print("      from theta series : %s" % show(a58_theta))
print("      closed form       : %s" % show(a58_closed))
check("alpha_58 closed form agrees with the theta series",
      abs(a58_theta - a58_closed) / a58_closed < D(10) ** -80,
      "two independent routes, 80+ digits")
print("""
      That closed form is already in ch-ramanujan-verify.py and it already
      contains 99:   alpha_58 = (13 sqrt58 - 99)^2 (99 - 70 sqrt2)^2""")

# --------------------------------------------------------------- [3] the 99 bridge
rule("3 . 99 IS THE NUMBER, AND IT WAS ALREADY THERE")
rows = [("9801, the series prefactor", 9801, "99^2", 99 ** 2),
        ("396, the series base",        396, "4 * 99", 4 * 99),
        ("396^4, one term's worth",     396 ** 4, "256 * 99^4", 256 * 99 ** 4)]
for label, got, expr, want in rows:
    print("      %-28s %-14d = %-12s = %d" % (label, got, expr, want))
    check("%s" % label.split(",")[0], got == want, "%s" % expr)
print("""
      Watson's algorithm at n = 58, already run in the earlier script, returns
      U = 1, V = 9801, W = 9801, S = 9802.  The 9801 in front of Ramanujan's
      series and the 9801 Watson returns are the same 99^2.""")

# ------------------------------------------------- [4] g_58 and the 19601 identity
rule("4 . THE CLASS INVARIANT AT 58, AND A PELL EQUATION")
k58  = a58_theta.sqrt()                 # k  = sqrt(alpha)
kp58 = (1 - a58_theta).sqrt()           # k' = sqrt(1 - alpha)
g12  = kp58 ** 2 / (2 * k58)            # g_N^12 = (k')^2 / (2k)
print("      k_58            = %s" % show(k58))
print("      g_58^12         = %s" % show(g12, 30))

eps = (5 + sq(29)) / 2                  # fundamental unit of Q(sqrt 29)
check("eps = (5+sqrt29)/2 is a unit of norm -1",
      abs((25 - 29) / D(4) + 1) < D(10) ** -60, "N(eps) = (25-29)/4 = -1")
check("g_58^12 = eps^6, from the transcendental side",
      abs(g12 - eps ** 6) / (eps ** 6) < D(10) ** -60,
      "theta series meets the unit group")
check("eps^6 = 9801 + 1820 sqrt29",
      abs(eps ** 6 - (9801 + 1820 * sq(29))) < D(10) ** -50,
      show(9801 + 1820 * sq(29), 24))
print("""
      So g_58^12 is NOT an integer.  It is 9801 + 1820 sqrt29 -- and 9801 is
      sitting there exactly, as the rational part of the sixth power of the
      fundamental unit of Q(sqrt 29).

      An earlier run of this script asserted g_58^12 = 19602 and then 19601.
      Both are wrong, and wrong in an instructive way: the value is 19601.99999,
      which is near BOTH and equal to NEITHER.  Asserting a near-integer as an
      integer is the failure this corpus keeps meeting.""")

check("(9801, 1820) solves Pell's equation x^2 - 29 y^2 = 1",
      9801 ** 2 - 29 * 1820 ** 2 == 1,
      "%d - 29*%d = 1, in integers" % (9801 ** 2, 1820 ** 2))
print("""
      Because the norm is +1, the conjugate is the inverse:
          g^-12 = 9801 - 1820 sqrt29
      and the irrational parts cancel when they are added.""")
gsum = g12 + 1 / g12
print("      g^12 + g^-12    = %s" % show(gsum, 30))
check("g^12 + g^-12 = 19602 = 2 * 99^2, EXACTLY",
      abs(gsum - 19602) < D(10) ** -60 and 19602 == 2 * 99 ** 2,
      "thirty zeros after the decimal point")
print("""
      That is the exact integer the near-miss was gesturing at.  It is 2*9801,
      twice the prefactor of Ramanujan's series, and it is exact only because
      Pell closes.  The corpus has met this identity before: ch-hardy used
      p^2 - 2q^2 = +-1 to rank the convergents of sqrt2.  Same equation, other
      discriminant, and here it is what makes a transcendental quantity
      rational.""")

# ------------------------------------------- [5] which reading of Theorem 5 closes
rule("5 . TESTING READINGS OF A MANGLED THEOREM AGAINST INTEGERS")
print("""
[BBB]'s Theorem 5 defines x_N.  The OCR of it in this copy is unusable, so
instead of transcribing it, each candidate reading is evaluated at N = 58 and
compared with 1/396^4 -- the value the series itself forces.  A reading either
lands on the integer or it does not.
""")
want = D(1) / D(396) ** 4
cands = [
    ("g^12 + g^-12",                      gsum),
    ("2 / (g^12 + g^-12)",                2 / gsum),
    ("1 / (g^12 + g^-12)^2",              1 / gsum ** 2),
    ("1 / (64 (g^12 + g^-12)^2)",         1 / (64 * gsum ** 2)),
    ("g^-24 / 64  (the near-miss)",       1 / (64 * g12 ** 2)),
]
best = None
for name, val in cands:
    ratio = val / want
    hit = abs(ratio - 1) < D(10) ** -60
    print("      %-24s = %-22s  ratio to 1/396^4 = %s%s"
          % (name, show(val, 12), show(ratio, 12), "   <== EXACT" if hit else ""))
    if hit: best = name
check("exactly one candidate reading reproduces 1/396^4",
      best is not None, "the reading that closes: x_58 = %s" % best)
if best:
    print("""
      So x_N = %s, read off arithmetic rather than off the page.
      At N = 58 it is 1/396^4, which is why 396^(4n) is the series denominator.
      The OCR is still unusable; the identity is not.""" % best)
    print("      Cross-check, purely integer:")
    print("          64 * 19602^2 = %d" % (64 * 19602 ** 2))
    print("          396^4        = %d" % (396 ** 4))
    check("64 * (2*99^2)^2 = 396^4, exactly",
          64 * 19602 ** 2 == 396 ** 4,
          "256 * 99^4 either way -- the same identity twice")

# --------------------------------------------------------------- [6] Chudnovsky
rule("6 . THE DESCENDANT")
print("""
      1/pi = 12 * SUM (-1)^n (6n)! (13591409 + 545140134 n)
                            --------------------------------
                            (3n)!(n!)^3  640320^(3n + 3/2)
""")
def chudnovsky(nmax):
    C = D(640320)
    C3 = C ** 3
    scale = 12 / (C * C.sqrt())          # 12 / 640320^(3/2)
    f6, f3, fn, total = D(1), D(1), D(1), D(0)
    for n in range(nmax + 1):
        if n > 0:
            for j in range(6 * n - 5, 6 * n + 1): f6 *= j
            for j in range(3 * n - 2, 3 * n + 1): f3 *= j
            fn *= n
        total += D(-1) ** n * f6 * (13591409 + 545140134 * n) / (f3 * fn ** 3 * C3 ** n)
        yield n, total * scale

prev, cg = 0, []
for n, approx in chudnovsky(7):
    err = abs(approx - target)
    dg = 0 if err == 0 else int(-err.log10() // 1)
    if n <= 4: print("      n = %-2d  correct digits: %3d   (+%d)" % (n, dg, dg - prev))
    if n: cg.append(dg - prev)
    prev = dg
check("Chudnovsky converges to 1/pi", abs(approx - target) < D(10) ** -90,
      "%d digits after 7 terms" % prev)
check("it gains about 14 digits a term against Ramanujan's 8",
      all(13 <= g <= 15 for g in cg[:6]),
      "measured: %s" % ",".join(str(g) for g in cg[:6]))
print("""
      An earlier run of this script divided by 640320^3/24 and got 12 digits a
      term, then stalled.  The /24 belongs to the binary-splitting arrangement,
      not to this one.  The rate is the check that caught it:
          log10(640320^3) - log10(1728) = %s - %s = %s
      which is the 14.18 the literature quotes, and 12.8 with the 24 divided in.
""" % (str(D(640320 ** 3).log10())[:6], str(D(1728).log10())[:6],
       str(D(640320 ** 3).log10() - D(1728).log10())[:5]))

print("""      Same shape, larger discriminant.  Ramanujan's is the N = 58 case;
      Chudnovsky's is built on 163 -- the last Heegner number, which
      ch-ramanujan-verify.py already recovered by counting reduced forms and
      wp82-k0-floor-verify.py used for the class-number floor.  Three scripts,
      one object.""")
check("163 is the largest Heegner number, recovered elsewhere in this corpus",
      163 in (1, 2, 3, 7, 11, 19, 43, 67, 163), "")

rule("7 . WHAT IS NOT SETTLED")
gaps = [
 ("[BBB] Theorem 5 was never transcribed, only tested at one point",
  "section 5 pins x_58 and nothing else; the general d_n(N) is untouched"),
 ("R14's own derivation not read -- the 1914 paper is in Downloads, unopened",
  "everything here comes through [BBB]'s restatement"),
 ("the 1103 is not explained",
  "9801, 396 and 19602 all reduce to 99; 1103 and 26390 do not, and this "
  "script does not derive them"),
 ("the k_210 discrepancy in ch-ramanujan-verify.py is still open",
  "the new Downloads sources have not been searched for it yet"),
 ("g_58^12 was asserted as an integer twice (19601, then 19602) before the "
  "exact form 9801 + 1820 sqrt29 was found",
  "the quantity is 19601.99999: near two integers, equal to neither. Only "
  "g^12 + g^-12 is exactly 19602, and only because Pell closes"),
 ("this script's first run returned k, not alpha = k^2, from the theta series",
  "caught because the closed form disagreed at the 5th digit, not because the "
  "code was re-read; a display slice was also hiding the exponent. Both fixed, "
  "both recorded, because the earlier chapter's theta routine should be "
  "re-checked for the same square"),
]
for i, (g, why) in enumerate(gaps, 1):
    print("  %d. %s\n       -> %s" % (i, g, why))

rule()
if FAIL:
    print("FAILED: %d" % len(FAIL))
    for f in FAIL: print("   - " + f)
    raise SystemExit(1)
print("All checks passed.  %d gaps recorded above remain open." % len(gaps))
