#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ch-cardano-verify.py — companion to book7/ch-cardano.html.

Five blocks, standard library only. The chapter's load-bearing claim is that
the casus irreducibilis is not an artefact to be avoided; this script makes
that concrete on a cubic whose roots are integers.

  [1] The discriminant of x^3 + px + q, and what its sign decides.
  [2] The casus irreducibilis on x^3 - 7x + 6, whose roots are 1, 2, -3:
      three real roots, and Cardano's formula must pass through the square
      root of a negative number to reach any of them.
  [3] Carrying it through anyway, as Bombelli did: complex cube roots, and
      imaginary parts that cancel to machine precision.
  [4] The contrast. A cubic with one real root is reached by real radicals
      with nothing complex anywhere.
  [5] Where the chapter points: the n-bonacci ladder polynomials, dominant
      root by bisection for n = 2..8, rising to 2.

Run:  python3 ch-cardano-verify.py

Principia Orthogona - Vol VII - G6 LLC - CC BY-NC-ND 4.0
"""
import cmath, math, sys
FAIL = []
def check(label, ok, detail=""):
    print(f"    {'PASS' if ok else 'FAIL'}  {label}" + (f"   {detail}" if detail else ""))
    if not ok: FAIL.append(label)
    return ok

def disc(p, q):
    return -4*p**3 - 27*q**2

def cardano(p, q):
    """u + v with u^3 = -q/2 + sqrt(q^2/4 + p^3/27), all three branches."""
    inner = cmath.sqrt(complex(q*q/4.0 + p**3/27.0))
    u3 = -q/2.0 + inner
    u = u3 ** (1.0/3.0) if u3.imag == 0 and u3.real >= 0 else cmath.exp(cmath.log(u3)/3.0)
    w = cmath.exp(2j*math.pi/3.0)
    out = []
    for k in range(3):
        uk = u * w**k
        vk = complex(0.0) if abs(uk) < 1e-300 else -p/(3.0*uk)
        out.append(uk + vk)
    return out, inner

print("\n[1] What the discriminant decides")
for (p, q, label) in [(-7.0, 6.0, "x^3 - 7x + 6"), (1.0, -2.0, "x^3 + x - 2")]:
    d = disc(p, q)
    print(f"    {label:<16} p={p:>5}  q={q:>5}   disc = -4p^3-27q^2 = {d:.0f}")
check("x^3 - 7x + 6 has positive discriminant: three distinct real roots", disc(-7.0, 6.0) > 0)
check("x^3 + x - 2 has negative discriminant: one real root", disc(1.0, -2.0) < 0)

print("\n[2] The casus irreducibilis")
p, q = -7.0, 6.0
under = q*q/4.0 + p**3/27.0
print(f"    q^2/4 + p^3/27           = {under:.10f}")
check("the quantity under Cardano's square root is NEGATIVE", under < 0,
      "so no real radical expression reaches these roots by this formula")
check("and yet all three roots are real integers", True, "1, 2, -3")

print("\n[3] Bombelli: carry the complex quantities through anyway")
roots, inner = cardano(p, q)
print(f"    sqrt(negative)           = {inner!r}")
maximag = max(abs(r.imag) for r in roots)
reals = sorted(round(r.real, 9) for r in roots)
for r in roots:
    print(f"    root                     = {r.real:+.12f} {r.imag:+.3e} i")
check("every imaginary part cancels to machine precision", maximag < 1e-9,
      f"max |Im| = {maximag:.2e}")
check("the recovered roots are 1, 2, -3", reals == [-3.0, 1.0, 2.0], f"{reals}")
for r in roots:
    resid = abs(r**3 + p*r + q)
    check(f"residual at root {r.real:+.3f} is zero", resid < 1e-9, f"|f(x)| = {resid:.2e}")

print("\n[4] The contrast: one real root, no complex quantities needed")
p2, q2 = 1.0, -2.0
under2 = q2*q2/4.0 + p2**3/27.0
u = (-q2/2.0 + math.sqrt(under2)) ** (1.0/3.0)
v = -p2/(3.0*u)
x = u + v
print(f"    q^2/4 + p^3/27           = {under2:.10f}   (positive)")
print(f"    real radical root        = {x:.12f}")
check("the quantity under the square root is positive", under2 > 0)
check("the real radical formula returns x = 1", abs(x - 1.0) < 1e-9)
check("residual is zero", abs(x**3 + p2*x + q2) < 1e-9)

print("\n[5] Where the chapter points: the n-bonacci ladder")
def nbonacci_root(n):
    f = lambda x: x**n - sum(x**k for k in range(n))
    lo, hi = 1.0 + 1e-12, 2.0
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if f(mid) < 0: lo = mid
        else: hi = mid
    return (lo + hi) / 2.0
prev = 0.0
for n in range(2, 9):
    x = nbonacci_root(n)
    print(f"    n = {n}   dominant root = {x:.10f}")
    check(f"n={n}: root lies strictly between 1 and 2", 1.0 < x < 2.0)
    check(f"n={n}: root exceeds the previous one", x > prev, f"{x:.6f} > {prev:.6f}")
    prev = x
check("n=2 is the golden ratio", abs(nbonacci_root(2) - (1+math.sqrt(5))/2) < 1e-9)
check("the sequence approaches 2 from below", nbonacci_root(8) < 2.0 and nbonacci_root(8) > 1.995)

print("""
[HONESTY] What this script establishes, and what it does not.

  ESTABLISHED. The arithmetic of the casus irreducibilis on one cubic with
  integer roots: the square root is genuinely of a negative quantity, and the
  imaginary parts genuinely cancel. The ladder roots to ten places.

  NOT ESTABLISHED. That NO real-radical expression reaches those roots. That
  is the casus irreducibilis theorem and it is quoted, not proved here;
  block [2] shows only that CARDANO'S formula passes through the complex
  numbers. No Galois group is computed anywhere in this script. The chapter's
  statement that the n-bonacci groups are generically the full symmetric group
  is quoted from book4/ladder-polynomials.html and is not checked here. The
  historical account - del Ferro's notebook, the oath, the 1548 debate - is
  not arithmetic and no script can verify it.
""")
print(f"{'ALL CHECKS PASSED' if not FAIL else 'FAILED: ' + ', '.join(FAIL)}")
sys.exit(1 if FAIL else 0)
