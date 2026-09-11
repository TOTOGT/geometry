#!/usr/bin/env python3
"""ch-weil-verify.py — the Riemann hypothesis that is true.

Verification companion to ch-weil.html. Standard library only (math, cmath);
no numpy, no install, nothing that can rot with a package bump.

Every count below is EXHAUSTIVE over the field, not sampled.
"""
import math, cmath, sys

FAIL = []
def check(cond, msg):
    print(("    PASS  " if cond else "    FAIL  ") + msg)
    if not cond: FAIL.append(msg)

def legendre_squares(p):
    return {(x * x) % p for x in range(p)}

def count_affine(a, b, p):
    """#{(x,y) in F_p^2 : y^2 = x^3+ax+b}, by exhaustion over all p^2 pairs."""
    sq = {}
    for y in range(p):
        sq[(y * y) % p] = sq.get((y * y) % p, 0) + 1
    n = 0
    for x in range(p):
        rhs = (x * x * x + a * x + b) % p
        n += sq.get(rhs, 0)
    return n

def discriminant(a, b, p):
    return (-16 * (4 * a**3 + 27 * b**2)) % p

CURVES = [(0, 1), (1, 0), (1, 1), (2, 3), (3, 5)]
PRIMES = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]

print("=" * 68)
print("  [1]  EXHAUSTIVE POINT COUNTS AND THE HASSE BOUND")
print("=" * 68)
print("  For each curve and prime, every one of the p^2 pairs (x,y) is tested.")
print("  a_p := p + 1 - #E(F_p).  Hasse (1930s): |a_p| <= 2*sqrt(p).")
print()
data = {}
worst = 0.0
for (a, b) in CURVES:
    for p in PRIMES:
        if discriminant(a, b, p) == 0:
            continue                      # singular over this p: not a curve
        N = count_affine(a, b, p) + 1     # + the point at infinity
        ap = p + 1 - N
        data[(a, b, p)] = (N, ap)
        ratio = abs(ap) / (2 * math.sqrt(p))
        worst = max(worst, ratio)
print(f"    {len(data)} curve/prime pairs counted exhaustively")
check(all(abs(ap) <= 2 * math.sqrt(p) for (a, b, p), (N, ap) in data.items()),
      f"every |a_p| <= 2*sqrt(p)   (tightest observed: {worst:.4f} of the bound)")
print()
print("    sample:  E: y^2 = x^3 + x + 1")
for p in [11, 23, 47]:
    if (1, 1, p) in data:
        N, ap = data[(1, 1, p)]
        print(f"      p={p:3d}   #E(F_p)={N:3d}   a_p={ap:+3d}   2*sqrt(p)={2*math.sqrt(p):6.3f}")

print()
print("=" * 68)
print("  [2]  THE RIEMANN HYPOTHESIS FOR THESE CURVES")
print("=" * 68)
print("  Numerator of the zeta function: P(T) = 1 - a_p T + p T^2.")
print("  RH over F_p says every reciprocal root has absolute value sqrt(p).")
print()
maxerr = 0.0
for (a, b, p), (N, ap) in data.items():
    disc = ap * ap - 4 * p
    roots = [(ap + cmath.sqrt(disc)) / 2, (ap - cmath.sqrt(disc)) / 2]
    for r in roots:
        maxerr = max(maxerr, abs(abs(r) - math.sqrt(p)))
check(maxerr < 1e-9,
      f"|alpha| = sqrt(p) for all {2*len(data)} reciprocal roots  (max error {maxerr:.2e})")
check(all(ap * ap - 4 * p < 0 for (a, b, p), (N, ap) in data.items()),
      "a_p^2 - 4p < 0 in every case, so the roots are a conjugate pair")
print()
print("    Why that is exact and not numerical: the roots satisfy")
print("    alpha*beta = p and, by Hasse, a_p^2 < 4p, so they are complex")
print("    conjugates. Then |alpha|^2 = alpha*conj(alpha) = alpha*beta = p.")
print("    The float check above only confirms the arithmetic did not slip.")

print()
print("=" * 68)
print("  [3]  THE FUNCTIONAL EQUATION")
print("=" * 68)
print("  Z(T) = P(T) / ((1-T)(1-pT)).  For genus 1, Z(1/(pT)) = Z(T).")
print()
def Z(T, ap, p):
    return (1 - ap * T + p * T * T) / ((1 - T) * (1 - p * T))
ferr = 0.0
for (a, b, p), (N, ap) in data.items():
    for T in (0.3, 0.55, 1.7, -0.4):
        lhs, rhs = Z(1.0 / (p * T), ap, p), Z(T, ap, p)
        ferr = max(ferr, abs(lhs - rhs))
check(ferr < 1e-9, f"Z(1/(pT)) = Z(T) at every sampled T  (max error {ferr:.2e})")

print()
print("=" * 68)
print("  [4]  EXTENSION FIELDS: THE COUNT IS FORCED BY THE ROOTS")
print("=" * 68)
print("  #E(F_{p^2}) should equal p^2 + 1 - (alpha^2 + beta^2), with no new")
print("  counting. Checked against a direct exhaustion over all p^4 pairs.")
print()
def count_Fp2(a, b, p):
    """Exhaustive count over F_{p^2} = F_p[t]/(t^2 - n), n a non-residue."""
    sq = legendre_squares(p)
    n = next(k for k in range(2, p) if k not in sq)
    def mul(u, v):
        return ((u[0]*v[0] + n*u[1]*v[1]) % p, (u[0]*v[1] + u[1]*v[0]) % p)
    def add(u, v):
        return ((u[0]+v[0]) % p, (u[1]+v[1]) % p)
    els = [(i, j) for i in range(p) for j in range(p)]
    squares = {}
    for y in els:
        s = mul(y, y)
        squares[s] = squares.get(s, 0) + 1
    tot = 0
    A, B = (a % p, 0), (b % p, 0)
    for x in els:
        rhs = add(add(mul(mul(x, x), x), mul(A, x)), B)
        tot += squares.get(rhs, 0)
    return tot + 1
ok2 = True
tested = 0
for (a, b) in CURVES[:3]:
    for p in [5, 7, 11, 13]:
        if (a, b, p) not in data:
            continue
        N, ap = data[(a, b, p)]
        disc = ap * ap - 4 * p
        al = (ap + cmath.sqrt(disc)) / 2
        be = (ap - cmath.sqrt(disc)) / 2
        pred = round((p**2 + 1 - (al**2 + be**2)).real)
        actual = count_Fp2(a, b, p)
        tested += 1
        if pred != actual:
            ok2 = False
            print(f"      MISMATCH a={a} b={b} p={p}: predicted {pred}, counted {actual}")
check(ok2, f"#E(F_p^2) matches p^2+1-(alpha^2+beta^2) in all {tested} cases, by exhaustion")

print()
print("=" * 68)
print("  [5]  CONTROL: A SINGULAR CASE IS NOT A CURVE")
print("=" * 68)
sing = [(a, b, p) for (a, b) in CURVES for p in PRIMES if discriminant(a, b, p) == 0]
check(all((a, b, p) not in data for (a, b, p) in sing),
      f"all {len(sing)} singular (a,b,p) triples were excluded, not counted")
print("    A vacuous pass is a pass. This block exists so that block [1]")
print("    cannot report success by having quietly tested nothing.")
check(len(data) > 60, f"block [1] actually tested {len(data)} cases, not zero")

print()
print("=" * 68)
print("  [HONESTY] What this script establishes, and what it does not.")
print("=" * 68)
print("""
  ESTABLISHED. Exhaustive counts, over every element of every field used --
  no sampling anywhere. On each curve and prime tested: the Hasse bound
  holds; the reciprocal roots of the zeta numerator have absolute value
  exactly sqrt(p), which is the Riemann hypothesis for that curve, and which
  follows algebraically from a_p^2 < 4p rather than from the float check;
  the functional equation holds; and the count over F_{p^2} is forced by the
  roots, confirmed by direct exhaustion over all p^4 pairs.

  NOT ESTABLISHED. Hasse's theorem itself, which is quoted and does the work
  in block [2]. The Weil conjectures for varieties of any dimension:
  rationality (Dwork 1960), the whole etale-cohomology apparatus built for
  them, and the Riemann hypothesis in general (Deligne 1974) are all quoted
  and none is proved here. Grothendieck's standard conjectures, his intended
  route to the same result, remain open and are untouched by any of this.

  AND, THE POINT OF THE CHAPTER. Nothing here bears on the classical Riemann
  hypothesis for zeta(s) over the rationals. That is a different problem,
  still open, and the analogy does not transport: the positivity that closes
  the function-field case has no number-field counterpart. Every entry in
  this corpus's own RELATED-WORK table stops at exactly that wall.
""")
print("=" * 68)
if FAIL:
    print(f"  {len(FAIL)} CHECK(S) FAILED")
    for m in FAIL: print("    - " + m)
    sys.exit(1)
print("  ALL CHECKS PASSED")
print("=" * 68)
