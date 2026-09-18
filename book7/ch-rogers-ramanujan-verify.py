#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ch-rogers-ramanujan-verify.py
Producing script for book7/ch-rogers-ramanujan.html.

Every number in that chapter is computed here at 120-digit precision, from the
standard library only. pi is built by Machin's formula before anything is
tested against it.

  [1] instrument
  [2] the two Rogers-Ramanujan identities, sum side against product side
  [3] R(q) = q^(1/5) H(q)/G(q) -- the continued fraction IS that ratio
  [4] the value Ramanujan sent Hardy in the first letter
  [5] the second value, with its fifth root
  [6] R(e^-2pi) is ALGEBRAIC: a root of x^2 + (1+sqrt5)x - 1
  [7] equivalently 1/R - R = 1 + sqrt5 = 2*phi
  [8] and it is special to that point, not generic

Closed forms are from Ramanujan's first letter to Hardy, 16 January 1913.
Hardy on receiving them: they "defeated me completely; I had never seen
anything in the least like them before."
"""

from decimal import Decimal as D, getcontext
getcontext().prec = 120

FAIL = []
def check(name, ok, detail=""):
    print("  %-5s %-54s %s" % ("ok" if ok else "FAIL", name, detail))
    if not ok: FAIL.append(name)

def rule(t=""):
    print("\n" + "=" * 78)
    if t: print(t); print("=" * 78)

def sq(x): return D(x).sqrt()

def places(a, b):
    d = (a - b).copy_abs()
    return 999 if d == 0 else int(-d.log10())

def arctan_inv(m):
    m = D(m); t = 1/m; s = t; k = 0
    while True:
        k += 1
        t = -t/(m*m)
        n = s + t/(2*k+1)
        if n == s: return s
        s = n

PI = 16*arctan_inv(5) - 4*arctan_inv(239)
PHI = (1 + sq(5))/2

rule("1 . INSTRUMENT")
check("Machin pi agrees with the known digits",
      str(PI).startswith("3.14159265358979323846264338327950288419716939937510"),
      str(PI)[:40] + "...")
check("phi satisfies phi^2 = phi + 1", places(PHI*PHI, PHI+1) > 100, "to 100+ places")

rule("2 . THE ROGERS-RAMANUJAN IDENTITIES")
print("""
      G(q) = SUM q^(n^2)   / (q;q)_n  =  PROD 1/((1-q^(5n+1))(1-q^(5n+4)))
      H(q) = SUM q^(n^2+n) / (q;q)_n  =  PROD 1/((1-q^(5n+2))(1-q^(5n+3)))

      A sum over partitions on the left; a product over two residue classes
      mod 5 on the right. The 5 enters here and never leaves.
""")
def G_sum(q, N=200):
    tot, poch = D(0), D(1)
    for n in range(N):
        if n: poch *= (1 - q**n)
        t = q**(n*n) / poch
        tot += t
        if n > 3 and t < D(10)**-130: break
    return tot

def H_sum(q, N=200):
    tot, poch = D(0), D(1)
    for n in range(N):
        if n: poch *= (1 - q**n)
        t = q**(n*n + n) / poch
        tot += t
        if n > 3 and t < D(10)**-130: break
    return tot

def G_prod(q, N=400):
    p = D(1)
    for n in range(N):
        p *= (1 - q**(5*n+1)) * (1 - q**(5*n+4))
        if q**(5*n+1) < D(10)**-130: break
    return 1/p

def H_prod(q, N=400):
    p = D(1)
    for n in range(N):
        p *= (1 - q**(5*n+2)) * (1 - q**(5*n+3))
        if q**(5*n+2) < D(10)**-130: break
    return 1/p

qt = (-2*PI).exp()
gs, gp, hs, hp = G_sum(qt), G_prod(qt), H_sum(qt), H_prod(qt)
print("      at q = e^-2pi:")
print("        G sum     = %s" % str(gs)[:40])
print("        G product = %s" % str(gp)[:40])
print("        H sum     = %s" % str(hs)[:40])
print("        H product = %s" % str(hp)[:40])
check("first Rogers-Ramanujan identity holds", places(gs, gp) > 100,
      "sum = product to %d places" % places(gs, gp))
check("second Rogers-Ramanujan identity holds", places(hs, hp) > 100,
      "sum = product to %d places" % places(hs, hp))

rule("3 . THE CONTINUED FRACTION IS THE RATIO OF THOSE TWO SERIES")
def R(q, depth=4000):
    acc = D(1)
    for n in range(depth, 0, -1):
        acc = 1 + q**n / acc
    return (q.ln()/5).exp() / acc

r_cf = R(qt)
r_ratio = (qt.ln()/5).exp() * hs / gs
print("      R from the continued fraction : %s" % str(r_cf)[:44])
print("      q^(1/5) H(q)/G(q)             : %s" % str(r_ratio)[:44])
check("the continued fraction equals q^(1/5) H/G",
      places(r_cf, r_ratio) > 100,
      "to %d places -- the 5 in q^(1/5) is the 5 mod 5" % places(r_cf, r_ratio))

rule("4 . THE VALUE IN THE FIRST LETTER TO HARDY")
closed1 = sq((5 + sq(5))/2) - (1 + sq(5))/2
print("      R(e^-2pi)                       = %s" % str(r_cf)[:44])
print("      sqrt((5+sqrt5)/2) - (1+sqrt5)/2 = %s" % str(closed1)[:44])
check("R(e^-2pi) matches the closed form Ramanujan sent",
      places(r_cf, closed1) > 110, "to %d places" % places(r_cf, closed1))

rule("5 . THE SECOND VALUE, WITH THE FIFTH ROOT")
q5 = (-2*PI*sq(5)).exp()
r5 = R(q5)
closed2 = sq(5)/(1 + (D(5)**(D(3)/4) * (PHI-1)**(D(5)/2) - 1)**(D(1)/5)) - PHI
print("      R(e^-2pi*sqrt5) = %s" % str(r5)[:44])
print("      closed form     = %s" % str(closed2)[:44])
check("the second value matches too",
      places(r5, closed2) > 110, "to %d places" % places(r5, closed2))

rule("6 . R(e^-2pi) IS ALGEBRAIC")
poly = r_cf*r_cf + (1 + sq(5))*r_cf - 1
print("      R^2 + (1+sqrt5)R - 1 = %s" % str(poly)[:30])
check("R is a root of x^2 + (1+sqrt5)x - 1 over Q(sqrt5)",
      places(poly, D(0)) > 110, "zero to %d places" % places(poly, D(0)))
root = (-(1+sq(5)) + sq((1+sq(5))**2 + 4))/2
print("      quadratic formula gives %s" % str(root)[:44])
check("solving the quadratic recovers every digit",
      places(root, r_cf) > 110, "to %d places" % places(root, r_cf))

rule("7 . THE GOLDEN RATIO IS FORCED, NOT DECORATIVE")
print("      1/R - R           = %s" % str(1/r_cf - r_cf)[:44])
print("      1 + sqrt5 = 2*phi = %s" % str(2*PHI)[:44])
check("1/R - R = 1 + sqrt5 = 2*phi",
      places(1/r_cf - r_cf, 2*PHI) > 110,
      "to %d places" % places(1/r_cf - r_cf, 2*PHI))
print("""
      The same statement twice. A continued fraction built from nothing but 1s
      and powers of q, evaluated at e^-2pi, differs from its own reciprocal by
      exactly twice the golden ratio.""")

rule("8 . IS IT SPECIAL TO THAT POINT?")
pts = [("e^-pi", (-PI).exp()), ("e^-2pi", qt), ("e^-3pi", (-3*PI).exp()),
       ("e^-4pi", (-4*PI).exp()), ("e^-2pi*sqrt5", q5)]
hits = []
for lab, q in pts:
    v = 1/R(q) - 1 - R(q)
    ok = places(v, sq(5)) > 100
    hits.append(ok)
    print("      %-14s 1/R - 1 - R = %-30s %s"
          % (lab, str(v)[:28], "= sqrt5" if ok else ""))
check("exactly one of the five points gives sqrt5",
      sum(hits) == 1, "e^-2pi and nothing else -- this is not generic")

rule("9 . WHY THE 5")
print("""
      Every 5 in this chapter is the same 5.

        - the products run over residue classes 5n+1, 5n+4 and 5n+2, 5n+3
        - so R carries a factor q^(1/5)
        - the field that appears is Q(sqrt5)
        - and phi = (1+sqrt5)/2 generates its ring of integers

      Same mechanism as the 9801 of the 1/pi series: a q-series evaluated at a
      special point becomes algebraic, and the algebra is a quadratic field.
      There it was Q(sqrt29) and a Pell equation. Here it is Q(sqrt5) and the
      golden ratio. One machine, two discriminants.""")

rule("10 . WHAT IS NOT SETTLED")
gaps = [
 ("nothing here is proved; everything is verified",
  "120 digits is evidence. The Rogers-Ramanujan identities have real proofs "
  "(Rogers 1894, Ramanujan independently, Schur); this reproduces neither"),
 ("the closed forms are taken from the letter, not derived",
  "why R(e^-2pi) should be algebraic at all is complex multiplication, and "
  "that theory is Vol XI's, unwritten"),
 ("the second value's closed form is transcribed and not understood",
  "the 5^(3/4) and the fifth root are checked numerically and explained "
  "nowhere in this chapter"),
 ("no claim is made about which q give an algebraic R",
  "section 8 tests five points; the general criterion is not stated here"),
]
for i, (g, why) in enumerate(gaps, 1):
    print("  %d. %s\n       -> %s" % (i, g, why))

rule()
if FAIL:
    print("FAILED: %d" % len(FAIL))
    for f in FAIL: print("   - " + f)
    raise SystemExit(1)
print("All checks passed.  %d gaps recorded above remain open." % len(gaps))
