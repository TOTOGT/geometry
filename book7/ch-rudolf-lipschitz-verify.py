#!/usr/bin/env python3
"""ch-rudolf-lipschitz-verify.py -- Book 7, Rudolf Lipschitz / the contraction-mapping example.

Source: Chapter 1, "Solution of equations by iteration", a course-notes PDF filed under the name 'suli' on the
NYU MATH-UA 252 (spring 2022) course page.  Section 1.2, Definition 1.2, Theorem 1.3, Example 1.2 and Table 1.1.

Checked here, with 60-digit decimal arithmetic and exact rationals (standard library only):
  1  Table 1.1: the twelve iterates x_k of x -> ln(2x+1) from x_0 = 1, to the six decimals printed;
  2  g maps [1,2] into itself, and g'(x) = 2/(2x+1) ranges over [2/5, 2/3] on [1,2], so L = 2/3 works;
  3  the error bound |x_k - xi| <= L^k |x_0 - xi| (formula 1.6) for k = 0..40, with xi solved to 50 digits;
  4  |x| is Lipschitz with L = 1 but has different one-sided slopes at 0 (the source's remark after 1.11);
  controls (the test must be able to fail):
  5  g(x) = x on [1,2] has L = 1 and does NOT have a unique fixed point (the strict L < 1 is doing work);
  6  sqrt(x) on [0,1] has no Lipschitz constant (difference quotient grows without bound);
  7  the bound (1.6) with a wrong L (= 0.3) is violated, so check 3 is not vacuous.

Not checked: the proof of Theorem 1.3 beyond what these numbers show; that a Lipschitz function is differentiable
almost everywhere (Rademacher, the source's footnote); anything about Lipschitz's life (the source's footnote gives
dates and fields; there is nothing numerical to test).
Run:  python3 ch-rudolf-lipschitz-verify.py
"""
from decimal import Decimal, getcontext
from fractions import Fraction
import sys
getcontext().prec = 60
fails = []
def check(name, ok, detail=""):
    print(("PASS  " if ok else "FAIL  ") + name + (("  -- " + detail) if detail else ""))
    if not ok: fails.append(name)

TABLE = [(0, '1.000000'), (1, '1.098612'), (2, '1.162283'), (3, '1.201339'), (4, '1.224563'), (5, '1.238121'), (6, '1.245952'), (7, '1.250447'), (8, '1.253018'), (9, '1.254486'), (10, '1.255323'), (11, '1.255800')]
D = Decimal
g = lambda x: (2*x + 1).ln()
x = D(1); xs = [x]
for _ in range(40): x = g(x); xs.append(x)

# 1  Table 1.1
ok = all(f"{xs[k]:.6f}" == s for k, s in TABLE)
check("1  Table 1.1 reproduced to 6 decimals (x_0..x_11)", ok and len(TABLE) == 12, f"{len(TABLE)} rows compared")
# control inside the check: change one printed digit and it must disagree
bad = [(k, s if k != 5 else "1.238122") for k, s in TABLE]
check("1c control: a corrupted table entry is detected", not all(f"{xs[k]:.6f}" == s for k, s in bad))

# 2  invariance and slope range on [1,2]
check("2a g(1) and g(2) lie in [1,2]", D(1) <= g(D(1)) <= D(2) and D(1) <= g(D(2)) <= D(2), f"g(1) = {g(D(1)):.6f}, g(2) = {g(D(2)):.6f}")
gp = lambda x: Fraction(2) / (2*x + 1)
lo, hi = gp(Fraction(2)), gp(Fraction(1))      # g' is decreasing, so extremes are at the endpoints
check("2b g'(x) = 2/(2x+1) decreasing on [1,2] with range [2/5, 2/3]", (lo, hi) == (Fraction(2, 5), Fraction(2, 3)), f"{lo} .. {hi}")
check("2c g'' = -4/(2x+1)^2 < 0 on [1,2] (why g' is decreasing)", all(Fraction(-4) / (2*Fraction(k, 100) + 1)**2 < 0 for k in range(100, 201)))

# 3  error bound with xi to 50 digits (bisection on f(x) = e^x - 2x - 1 over [1,2])
f = lambda x: x.exp() - 2*x - 1
a, b = D(1), D(2)
for _ in range(190):
    m = (a + b) / 2
    if f(a) * f(m) <= 0: b = m
    else: a = m
xi = (a + b) / 2
check("3a xi solves e^xi = 2 xi + 1 to 1e-45", abs(f(xi)) < D("1e-45"), f"xi = {xi:.12f}")
L = D(2) / D(3)
ok = all(abs(xs[k] - xi) <= L**k * abs(xs[0] - xi) for k in range(41))
check("3b |x_k - xi| <= (2/3)^k |x_0 - xi| for k = 0..40", ok)
Lbad = D("0.3")
check("3c control: with L = 0.3 the bound fails somewhere (test is not vacuous)", not all(abs(xs[k] - xi) <= Lbad**k * abs(xs[0] - xi) for k in range(41)))
ratio = abs(xs[41 - 1] - xi) / abs(xs[40 - 1] - xi)
check("3d the observed per-step error ratio is about g'(xi), well below 2/3", abs(ratio - D(2)/(2*xi + 1)) < D("1e-3"), f"observed {ratio:.5f}, g'(xi) = {D(2)/(2*xi+1):.5f}")

# 4  |x|: Lipschitz constant 1, unequal one-sided slopes at 0
quots = [Fraction(abs(Fraction(k, 1000)) - 0, Fraction(k, 1000)) for k in (-1000, -10, -1, 1, 10, 1000)]
check("4a |x| has difference quotients -1 and +1 at 0 (not differentiable)", min(quots) == -1 and max(quots) == 1)
pts = [Fraction(k, 7) for k in range(-30, 31)]
check("4b |x| satisfies |g(x)-g(y)| <= 1*|x-y| on a grid", all(abs(abs(p) - abs(q)) <= abs(p - q) for p in pts for q in pts))

# 5  control: identity has L = 1, every point is fixed, so no unique fixed point
gid = lambda t: t
fixed = [Fraction(k, 10) for k in range(10, 21) if gid(Fraction(k, 10)) == Fraction(k, 10)]
lip = max(abs(gid(p) - gid(q)) / abs(p - q) for p in fixed for q in fixed if p != q)
check("5  control: g(x) = x on [1,2] has Lipschitz ratio exactly 1 and every sampled point fixed (no uniqueness at L = 1)", lip == 1 and len(fixed) == 11)

# 6  control: sqrt has no Lipschitz constant on [0,1]
qs = [(D(10) ** -k).sqrt() / (D(10) ** -k) for k in range(1, 12)]
check("6  control: sqrt(x) on [0,1] has difference quotients at 0 that grow without bound", qs[-1] > 3 * qs[0] > 9 and all(qs[i+1] > qs[i] for i in range(len(qs)-1)), f"{qs[0]:.2f} .. {qs[-1]:.0f}")

print()
if fails: print("FAILED:", ", ".join(fails)); sys.exit(1)
print("All checks passed. They reproduce the source's worked example; they do not prove the theorem.")
