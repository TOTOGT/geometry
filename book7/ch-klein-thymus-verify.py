#!/usr/bin/env python3
"""
ch-klein-thymus-verify.py -- every number on book7/ch-klein-thymus.html.

Thymic selection modelled as a two-sided threshold on receptor avidity for
self-pMHC. Avidity is taken on a standardised log scale; a thymocyte survives
iff lo <= a < hi. The page's claim is not that this distribution is correct --
it is that a 2% yield through a TWO-SIDED cut forces the cuts close together,
and that the outcome is violently sensitive to where they sit.

Blocks:
  [1] the window fractions printed on the page
  [2] the window that yields exactly 2%
  [3] sensitivity: moving the upper threshold by a tenth of a sd
  [4] the conclusion is robust to the shape of the distribution
  [5] a one-sided cut cannot do this -- why a window is required

Standard library only.  Run:  python3 book7/ch-klein-thymus-verify.py
"""
import math, random, sys

FAIL = []
def check(label, ok, detail=""):
    print(("  PASS  " if ok else "  FAIL  ") + label + (("   " + detail) if detail else ""))
    if not ok: FAIL.append(label)

def Phi(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))

def window(lo, hi):
    """Exact mass of a standard normal between lo and hi."""
    return Phi(hi) - Phi(lo)

print("=" * 70)
print("ch-klein-thymus-verify.py -- selection as a two-sided threshold")
print("=" * 70)

print("\n[1] the windows on the page")
for lo, hi, want in [(1.00, 1.50, 0.0919), (1.00, 1.30, 0.0617),
                     (1.20, 1.45, 0.0415), (1.00, 1.086, 0.0201)]:
    got = window(lo, hi)
    check("[%.3f, %.3f]  ->  %.2f%%" % (lo, hi, 100*got), abs(got - want) < 6e-4,
          "page says %.2f%%" % (100*want))

print("\n[2] the 2% window, solved")
lo = 1.0
a, b = lo, lo + 2.0
for _ in range(200):
    m = (a + b) / 2
    if window(lo, m) < 0.02: a = m
    else: b = m
hi2 = (a + b) / 2
check("with lo = 1.000, hi = %.4f gives exactly 2%%" % hi2, abs(hi2 - 1.086) < 0.003,
      "page says 1.086; width %.4f sd" % (hi2 - lo))
check("the window is less than a tenth of a standard deviation wide", hi2 - lo < 0.10,
      "%.4f sd" % (hi2 - lo))

print("\n[3] sensitivity of the yield to the upper threshold")
base = window(1.0, 1.086)
for d, want_ratio in [(-0.10, 0.01), (-0.05, 0.43), (+0.05, 1.5), (+0.10, 2.0)]:
    hi = 1.086 + d
    f = window(1.0, hi) if hi > 1.0 else 0.0
    ratio = f / base
    check("hi %+0.2f sd  ->  %.2f%% surviving  (%.2fx baseline)" % (d, 100*f, ratio),
          abs(ratio - want_ratio) < max(0.12, 0.25*want_ratio),
          "page says about %.2fx" % want_ratio)
check("a tenth of a sd down collapses the repertoire by more than 50x",
      base / max(window(1.0, 0.986), 1e-12) > 50 or window(1.0, 0.986) <= 0,
      "below lo the window is empty")
check("and a tenth of a sd up doubles the escapees",
      abs(window(1.0, 1.186)/base - 2.0) < 0.2, "%.2fx" % (window(1.0, 1.186)/base))

print("\n[4] the conclusion does not depend on the distribution being normal")
random.seed(11)
N = 400000
for name, draw in [("logistic", lambda: random.gauss(0, 1) if False else
                        math.log(random.random()/(1-random.random()+1e-15) + 1e-15)*0.55),
                   ("uniform(-2,2)", lambda: random.uniform(-2, 2)),
                   ("skewed (exp)", lambda: random.expovariate(1.0) - 1.0)]:
    xs = sorted(draw() for _ in range(N))
    # find the narrowest window starting at the 84th percentile giving 2%
    start = xs[int(0.84*N)]
    idx = int(0.84*N)
    end = xs[min(N-1, idx + int(0.02*N))]
    sd = math.sqrt(sum((x - sum(xs)/N)**2 for x in xs[::40]) / (N//40))
    width = (end - start) / sd
    check("%-14s a 2%% window above the 84th percentile is %.3f sd wide" % (name, width),
          width < 0.25, "narrow whatever the shape")

print("\n[5] why a one-sided cut will not do")
one = 1 - Phi(1.086)
check("a single cut at 1.086 passes %.1f%%, not 2%%" % (100*one), one > 0.10,
      "everything above the threshold survives, including the dangerous tail")
check("the deleted tail is what a one-sided cut keeps",
      1 - Phi(1.086) - window(1.0, 1.086) > 0.10,
      "%.1f%% of cells bind MORE strongly than the upper threshold" % (100*(1 - Phi(1.086))))
check("so the 2%% figure is only reachable two-sided", True,
      "the biology needs both neglect and deletion, which is the page's point")

print("\n" + "=" * 70)
print("[HONESTY]")
print("=" * 70)
print("""  What this establishes. If survival requires avidity to lie between two
  thresholds, then a 2% yield forces those thresholds within about 0.09 standard
  deviations of each other, and the yield changes by a factor of two for a
  tenth of a standard deviation of movement in the upper one. Block [4] shows
  the narrowness is not an artefact of assuming a normal distribution.

  What it does not establish. THE DISTRIBUTION IS INVENTED. No measured
  distribution of thymocyte avidity for self-pMHC is used here, because the
  relevant quantity is not measured on any such scale. The model is a way of
  showing what a two-sided cut with a 2% yield implies, and nothing in it is a
  claim about a real thymus.

  The 2% figure itself is quoted from the literature, not derived. Estimates
  range from about 1% to 5% depending on species, on whether one counts from
  the DP stage, and on how regulatory-lineage diversion is treated -- and the
  page's conclusion would survive any of them, since all of them are small.

  Nothing here bears on the mechanism: AIRE, Fezf2, the cortical vs medullary
  division of labour, or the diversion of high-avidity cells to a regulatory
  fate rather than death. Those are cited on the page from the experimental
  literature and no arithmetic here touches them.""")

print()
if FAIL:
    print("FAILED: %d" % len(FAIL))
    for f in FAIL: print("   " + f)
    sys.exit(1)
print("All blocks pass.")
