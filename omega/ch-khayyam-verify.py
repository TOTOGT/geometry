#!/usr/bin/env python3
"""
ch-khayyam-verify.py -- every number on omega/ch-khayyam.html.

Blocks:
  [1] Khayyam's construction: parabola x^2 = sqrt(a) y meets circle
      x^2 + y^2 = (b/a) x at the real root of x^3 + a x = b
  [2] the quoted case a=2, b=5 -> x = 1.328268855669
  [3] the three calendar rules and their drift
  [4] 8/33 is a continued-fraction convergent of the tropical-year fraction
  [5] 97/400 is not a convergent, and 31/128 beats it with a smaller denominator

Standard library only.  Run:  python3 omega/ch-khayyam-verify.py
"""
import math, sys
from fractions import Fraction

FAIL = []
def check(label, ok, detail=""):
    print(("  PASS  " if ok else "  FAIL  ") + label + (("   " + detail) if detail else ""))
    if not ok: FAIL.append(label)

def bisect(f, lo, hi, n=300):
    for _ in range(n):
        m = (lo + hi) / 2
        if f(m) < 0: lo = m
        else: hi = m
    return (lo + hi) / 2

def khayyam_x(a, b):
    """Second intersection of x^2 = sqrt(a) y with x^2 + y^2 = (b/a) x, x > 0."""
    p = math.sqrt(a)
    return bisect(lambda x: x*x + (x*x/p)**2 - (b/a)*x, 1e-12, 50.0)

def real_root(a, b):
    return bisect(lambda x: x**3 + a*x - b, 0.0, 50.0)

print("=" * 70)
print("ch-khayyam-verify.py")
print("=" * 70)

print("\n[1] the construction returns the real root of the cubic")
for a, b in [(2.0, 5.0), (1.0, 1.0), (3.0, 10.0), (0.5, 0.2), (7.0, 3.0), (0.25, 12.0)]:
    xi, xr = khayyam_x(a, b), real_root(a, b)
    check("a = %.2f  b = %5.2f   x = %.12f" % (a, b, xi), abs(xi - xr) < 1e-12,
          "cubic root %.12f, difference %.2e" % (xr, abs(xi - xr)))
    check("   and it satisfies x^3 + a x = b", abs(xi**3 + a*xi - b) < 1e-10,
          "residual %.2e" % abs(xi**3 + a*xi - b))

print("\n[2] the case printed on the page")
check("a = 2, b = 5  ->  1.328268855669", abs(khayyam_x(2.0, 5.0) - 1.328268855669) < 1e-11,
      "%.12f" % khayyam_x(2.0, 5.0))

print("\n[3] the calendar table")
TROP = 365.242190
for name, num, den, ln, err, adrift in [
        ("Jalali 8/33",     8, 33,  365.242424242, 0.000234242, 4269),
        ("Gregorian 97/400", 97, 400, 365.242500000, 0.000310000, 3226),
        ("Julian 1/4",       1,  4,  365.250000000, 0.007810000,  128)]:
    L = 365 + num/den
    e = L - TROP
    check("%-18s mean year %.9f" % (name, L), abs(L - ln) < 5e-9, "page says %.9f" % ln)
    check("%-18s drift %+.9f d/yr" % (name, e), abs(e - err) < 5e-9, "page says %+.9f" % err)
    check("%-18s one day in %.0f years" % (name, abs(1/e)), abs(round(abs(1/e)) - adrift) <= 1,
          "page says %d" % adrift)
check("Jalali is more accurate than Gregorian",
      abs(365 + 8/33 - TROP) < abs(365 + 97/400 - TROP), "by a factor %.2f"
      % (abs(365 + 97/400 - TROP) / abs(365 + 8/33 - TROP)))

print("\n[4] the continued fraction of 0.242190")
x = 0.242190
cf, v = [], x
for _ in range(6):
    a = int(v // 1); cf.append(a); v -= a
    if v < 1e-12: break
    v = 1 / v
check("cf = [0; 4, 7, 1, 3, 24, ...]", cf[:6] == [0, 4, 7, 1, 3, 24], str(cf))
h, k = [0, 1], [1, 0]
conv = []
for a in cf:
    h.append(a*h[-1] + h[-2]); k.append(a*k[-1] + k[-2])
    if k[-1] > 1: conv.append((h[-1], k[-1]))
check("convergents include 1/4, 7/29, 8/33, 31/128",
      [(1, 4), (7, 29), (8, 33), (31, 128)] == conv[:4], str(conv[:5]))
check("8/33 IS a convergent", (8, 33) in conv)

print("\n[5] what 97/400 is not")
check("97/400 is NOT a convergent", (97, 400) not in conv, str(conv[:6]))
best = min(((round(x*q), q) for q in range(1, 401)), key=lambda pq: abs(pq[0]/pq[1] - x))
check("the best rational with denominator <= 400 is 31/128, not 97/400",
      best == (31, 128), "found %d/%d, error %+.3e" % (best[0], best[1], best[0]/best[1] - x))
check("31/128 beats 97/400 with a smaller denominator",
      abs(31/128 - x) < abs(97/400 - x) and 128 < 400,
      "%.3e vs %.3e" % (abs(31/128 - x), abs(97/400 - x)))
# a convergent is a best approximation: no smaller denominator comes closer than 8/33
closer = [(q, round(x*q)) for q in range(1, 33) if abs(round(x*q)/q - x) < abs(8/33 - x)]
check("no denominator below 33 comes closer than 8/33", not closer, "found %s" % closer)

print("\n" + "=" * 70)
print("[HONESTY]")
print("=" * 70)
print("""  What this establishes. Khayyam's circle-and-parabola construction returns
  the real root of x^3 + ax = b, checked on six cases to twelve digits and by
  direct substitution into the cubic. The calendar arithmetic is exact. 8/33 is
  a continued-fraction convergent of 0.242190 and 97/400 is not, and no
  denominator below 33 approximates the tropical-year fraction better than
  8/33 does.

  What it does not establish. Block [1] finds both the intersection and the
  root by bisection. Agreement to twelve digits on six cases is strong evidence
  that the construction is exact; the proof is Khayyam's and is a substitution,
  not a search. The construction is stated here for a, b > 0; Khayyam treats
  fourteen cases precisely because he cannot write the others this way, and
  this script checks one of them.

  The tropical year is taken as 365.242190 days, a J2000 mean value. It is not
  a constant -- it drifts slowly, and it was slightly longer in 1079. The
  "one day adrift in N years" figures are therefore right to about their first
  two digits and should not be quoted more precisely than the page quotes them.

  Nothing here is a claim about how Khayyam's committee arrived at 8/33. The
  page marks that OPEN and this script cannot touch it: arithmetic cannot
  recover a method from its result.""")

print()
if FAIL:
    print("FAILED: %d" % len(FAIL))
    for f in FAIL: print("   " + f)
    sys.exit(1)
print("All blocks pass.")
