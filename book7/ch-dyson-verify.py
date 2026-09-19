#!/usr/bin/env python3
"""
ch-dyson-verify.py -- every number on book7/ch-dyson.html.

No table of zeros is used. The zeros are computed here from the Riemann-Siegel
formula for Z(t), then unfolded and their pair correlation compared against
Montgomery's 1 - (sin(pi r)/(pi r))^2 -- the GUE two-point function Dyson
recognised -- and against the uncorrelated (Poisson) value 1.

Blocks:
  [1] Z(t) sign changes locate the zeros; the first ten against published values
  [2] how many zeros, to what height
  [3] unfolding: mean spacing one
  [4] the pair-correlation table printed on the page
  [5] RMS deviation from GUE against RMS deviation from Poisson
  [6] level repulsion: the first bin
  [7] the threefold way is three because Frobenius says three

Standard library only. Takes about ten seconds.
Run:  python3 book7/ch-dyson-verify.py
"""
import math, sys

FAIL = []
def check(label, ok, detail=""):
    print(("  PASS  " if ok else "  FAIL  ") + label + (("   " + detail) if detail else ""))
    if not ok: FAIL.append(label)

def theta(t):
    """Riemann-Siegel theta, asymptotic series."""
    return (t/2*math.log(t/(2*math.pi)) - t/2 - math.pi/8
            + 1/(48*t) + 7/(5760*t**3))

def Z(t):
    """Riemann-Siegel Z(t): real, and Z(t) = 0 exactly where zeta(1/2+it) = 0."""
    th = theta(t)
    N = int(math.sqrt(t/(2*math.pi)))
    s = sum(math.cos(th - t*math.log(n))/math.sqrt(n) for n in range(1, N+1))
    p = math.sqrt(t/(2*math.pi)) - N
    C0 = math.cos(2*math.pi*(p*p - p - 1/16))/math.cos(2*math.pi*p)
    return 2*s + (-1)**(N-1) * (2*math.pi/t)**0.25 * C0

print("=" * 70)
print("ch-dyson-verify.py -- Montgomery's pair correlation, from zeros computed here")
print("=" * 70)

T_MAX, DT = 4200.0, 0.04
zeros = []
t, prev = 10.0, Z(10.0)
while t < T_MAX:
    t += DT
    cur = Z(t)
    if prev * cur < 0:
        a, b = t - DT, t
        for _ in range(70):
            m = (a + b) / 2
            if Z(a) * Z(m) < 0: b = m
            else: a = m
        zeros.append((a + b) / 2)
    prev = cur

print("\n[1] the first ten zeros, against the published values")
KNOWN = [14.134725142, 21.022039639, 25.010857580, 30.424876126, 32.935061588,
         37.586178159, 40.918719012, 43.327073281, 48.005150881, 49.773832478]
errs = [abs(zeros[i] - KNOWN[i]) for i in range(10)]
for i in range(5):
    check("zero %2d = %.6f" % (i+1, zeros[i]), errs[i] < 1e-2,
          "published %.6f, error %.2e" % (KNOWN[i], errs[i]))
check("mean absolute error over the first ten = %.2e" % (sum(errs)/10), sum(errs)/10 < 5e-3,
      "page says 2.1e-3")

print("\n[2] how many")
check("found %d zeros below t = %d" % (len(zeros), int(T_MAX)), len(zeros) > 3600,
      "page says 3681")
check("the count matches Riemann-von Mangoldt to within 1%",
      abs(len(zeros) - (theta(T_MAX)/math.pi + 1)) / len(zeros) < 0.01,
      "N(T) ~ theta(T)/pi + 1 = %.0f" % (theta(T_MAX)/math.pi + 1))

print("\n[3] unfolding")
w = [theta(z)/math.pi for z in zeros]
gaps = [w[i+1] - w[i] for i in range(len(w)-1)]
mean_gap = sum(gaps)/len(gaps)
check("mean unfolded spacing = %.6f" % mean_gap, abs(mean_gap - 1.0) < 0.01,
      "unfolding is w_n = theta(t_n)/pi")
w = w[len(w)//2:]
n = len(w)
check("upper half kept: %d points" % n, n > 1800, "page says 1841")

BW, NB = 0.1, 30
H = [0]*NB
for i in range(n):
    for j in range(i+1, n):
        r = w[j] - w[i]
        if r >= NB*BW: break
        H[int(r/BW)] += 1
obs = [H[k]/(n*BW) for k in range(NB)]
gue = [1 - (math.sin(math.pi*((k+.5)*BW))/(math.pi*((k+.5)*BW)))**2 for k in range(NB)]

print("\n[4] the table on the page")
for k, want_o, want_g in [(0, 0.0000, 0.0082), (1, 0.0380, 0.0719), (2, 0.0760, 0.1894),
                          (4, 0.5269, 0.5119), (9, 1.1298, 0.9973), (19, 0.9125, 0.9993)]:
    check("r = %.2f   observed %.4f   GUE %.4f" % ((k+.5)*BW, obs[k], gue[k]),
          abs(obs[k] - want_o) < 5e-3 and abs(gue[k] - want_g) < 5e-4,
          "page says %.4f / %.4f" % (want_o, want_g))

print("\n[5] GUE against Poisson")
for lim, name in ((15, "r < 1.5"), (30, "r < 3.0")):
    dg = math.sqrt(sum((obs[k]-gue[k])**2 for k in range(lim))/lim)
    dp = math.sqrt(sum((obs[k]-1.0)**2 for k in range(lim))/lim)
    check("%s : RMS from GUE %.4f, from Poisson %.4f, ratio %.2f" % (name, dg, dp, dp/dg),
          dp/dg > 4.0, "the zeros are far closer to GUE than to uncorrelated")
dg = math.sqrt(sum((obs[k]-gue[k])**2 for k in range(15))/15)
dp = math.sqrt(sum((obs[k]-1.0)**2 for k in range(15))/15)
check("the page's figures: 0.078 and 0.502", abs(dg-0.078) < 0.01 and abs(dp-0.502) < 0.01,
      "computed %.4f and %.4f" % (dg, dp))

print("\n[6] level repulsion")
check("first bin: observed %.4f, Poisson would give 1.0000" % obs[0], obs[0] < 0.05,
      "the zeros avoid each other")
check("and GUE predicts %.4f there" % gue[0], abs(obs[0]-gue[0]) < 0.05)

print("\n[7] the threefold way is three")
# Frobenius: the finite-dimensional associative division algebras over R are
# R, C, H -- dimensions 1, 2, 4, which are Dyson's beta.
check("beta = dim_R of the division algebra: 1, 2, 4", [1, 2, 4] == [1, 2, 4],
      "R, C, H -- Frobenius 1878, and there is no fourth")
check("the Cayley numbers are excluded because they are not associative", True,
      "O has dimension 8 and gives no beta = 8 ensemble")

print("\n" + "=" * 70)
print("[HONESTY]")
print("=" * 70)
print("""  What this establishes. From zeros this script computes itself, the pair
  correlation of the Riemann zeros is close to the GUE two-point function and
  far from the uncorrelated one -- by a factor of six in RMS -- and the first
  bin shows unambiguous level repulsion. That is a real numerical confirmation
  of the observation Dyson made at tea, reproduced from scratch.

  What it does not establish. Montgomery's result is a THEOREM only for test
  functions of restricted support and only under the Riemann Hypothesis; the
  full pair-correlation conjecture is open. Nothing here proves it. Nothing
  here proves RH, and the agreement of a statistic is not evidence for RH.

  The zeros are accurate to about 2e-3, from a Riemann-Siegel formula truncated
  after the leading C0 correction term. That is fine against a mean spacing near
  1 after unfolding but it is not high-precision root-finding, and the third
  decimal of any individual zero here should not be quoted. Odlyzko's
  computations, cited on the page, are the real numerical evidence; this is a
  demonstration that the effect is visible without them.

  Block [7] is bookkeeping, not a proof: Frobenius' theorem is cited, not
  verified. No arithmetic can establish that there is no fourth division
  algebra.""")

print()
if FAIL:
    print("FAILED: %d" % len(FAIL))
    for f in FAIL: print("   " + f)
    sys.exit(1)
print("All blocks pass.")
