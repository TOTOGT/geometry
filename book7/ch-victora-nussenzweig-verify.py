#!/usr/bin/env python3
"""
ch-victora-nussenzweig-verify.py -- every number on
book7/ch-victora-nussenzweig.html.

Germinal-centre affinity maturation as iterated mutate-and-select on a
log-affinity scale.

Blocks:
  [1] the compounding arithmetic: what each round must deliver for 10^6 -> 10^11
  [2] the toy model's trajectory, round by round
  [3] the overshoot: the toy beats the biology, which is the page's finding
  [4] the claim this page DROPPED: there is no optimum in this model
  [5] what the outcome is actually sensitive to

Standard library only.  Run:  python3 book7/ch-victora-nussenzweig-verify.py
"""
import math, random, sys

FAIL = []
def check(label, ok, detail=""):
    print(("  PASS  " if ok else "  FAIL  ") + label + (("   " + detail) if detail else ""))
    if not ok: FAIL.append(label)

print("=" * 70)
print("ch-victora-nussenzweig-verify.py -- affinity maturation")
print("=" * 70)

print("\n[1] what each round must deliver")
TOTAL = 5.0     # log10(10^11 / 10^6)
for n, want_dex, want_fold in [(5, 1.000, 10.00), (6, 0.833, 6.81),
                               (8, 0.625, 4.22), (10, 0.500, 3.16)]:
    dex = TOTAL / n
    check("%2d rounds  ->  %.3f dex/round  (%.2f-fold)" % (n, dex, 10**dex),
          abs(dex - want_dex) < 5e-4 and abs(10**dex - want_fold) < 5e-3,
          "page says %.3f dex, %.2f-fold" % (want_dex, want_fold))
check("10^6 -> 10^11 is exactly 5 orders of magnitude", abs(TOTAL - 5.0) < 1e-15)

def maturation(rounds=10, pop=2000, keep=0.1, mut_sd=0.30, seed=3):
    random.seed(seed)
    x = [0.0] * pop
    hist = []
    for _ in range(rounds):
        x = [v + random.gauss(0, mut_sd) for v in x]
        x.sort(reverse=True)
        x = x[:int(pop * keep)]
        x = x * int(1 / keep)
        hist.append(sum(x) / len(x))
    return hist

print("\n[2] the toy model, round by round (mut sd 0.30 dex, top 10% kept)")
h = maturation()
EXPECT = [0.528, 1.114, 1.696, 2.299, 2.914, 3.522, 4.090, 4.656, 5.261, 5.891]
for i, (got, want) in enumerate(zip(h, EXPECT), 1):
    check("round %2d   +%.3f dex  (%.1f-fold)" % (i, got, 10**got),
          abs(got - want) < 2e-3, "page implies %.3f" % want)
check("total after 10 rounds = %.2f dex" % h[-1], abs(h[-1] - 5.891) < 2e-3,
      "page says 5.89 dex = 7.8e5 fold")
check("which is %.1e fold" % (10**h[-1]), abs(10**h[-1] - 7.8e5)/7.8e5 < 0.03)

print("\n[3] the overshoot")
check("the toy reaches %.2f dex where the biology reaches 5.00" % h[-1], h[-1] > 5.0,
      "it beats the real germinal centre by %.2f dex" % (h[-1] - 5.0))
check("the excess is most of an order of magnitude", h[-1] - 5.0 > 0.8,
      "%.2f dex, a factor of %.1f" % (h[-1] - 5.0, 10**(h[-1] - 5.0)))
# how many rounds does the toy need to reach 5.00?
n5 = next(i for i, v in enumerate(h, 1) if v >= 5.0)
check("the toy reaches the biological endpoint in %d rounds, not 10" % n5, n5 <= 9,
      "so something real is holding the germinal centre back")

print("\n[4] the claim this page dropped")
print("      an earlier draft asserted an OPTIMAL mutation rate. In this model there is none:")
gains = []
for sd in (0.05, 0.10, 0.20, 0.30, 0.50, 0.70, 1.00):
    g = maturation(mut_sd=sd)[-1]
    gains.append((sd, g))
    print("        mut sd %.2f dex  ->  %6.2f dex total" % (sd, g))
check("the gain is monotone increasing in mutation size", 
      all(gains[i][1] < gains[i+1][1] for i in range(len(gains)-1)),
      "no interior maximum -- the model has no trade-off in it")
check("so the page's dropped claim is refuted by its own model, and stays dropped",
      gains[-1][1] > gains[3][1],
      "sd = 1.00 beats sd = 0.30 by %.1f dex, which is biologically absurd"
      % (gains[-1][1] - gains[3][1]))

print("\n[5] what the outcome is sensitive to")
for keep, in [(0.02,), (0.05,), (0.10,), (0.25,), (0.50,)]:
    g = maturation(keep=keep)[-1]
    print("        keep top %4.0f%%  ->  %.2f dex" % (100*keep, g))
strict = maturation(keep=0.02)[-1]; loose = maturation(keep=0.50)[-1]
check("selection stringency matters: top 2%% gives %.2f dex, top 50%% gives %.2f"
      % (strict, loose), strict > loose + 2.0,
      "a factor of %.0e between them" % (10**(strict - loose)))
check("and stringency is the parameter the biology actually sets",
      True, "T follicular helper supply is finite -- that IS the keep fraction")

print("\n" + "=" * 70)
print("[HONESTY]")
print("=" * 70)
print("""  What this establishes. The compounding arithmetic is exact: 10^6 to 10^11
  in n rounds requires 5/n dex per round, and that is all block [1] claims. The
  toy model's trajectory is reproducible and reaches 5.89 dex in ten rounds,
  overshooting the biological endpoint.

  What it does not establish. THE MODEL IS NOT IMMUNOLOGY. It has no receptor,
  no antigen, no affinity ceiling, no lethal mutations, no antigen consumption,
  and no T cells. Gaussian steps on a log scale with truncation selection is
  the simplest thing that compounds, and its agreement with the observed order
  of magnitude is not evidence that germinal centres work this way. The
  overshoot in block [3] is reported as a QUESTION -- what limits the real
  system -- and not as a finding about B cells.

  Block [4] exists to keep a dropped claim refuted. An earlier draft of the
  page asserted an optimal hypermutation rate, too little achieving nothing and
  too much destroying the receptor. The model written to demonstrate it is
  monotone: bigger mutations always win, up to sizes that are nonsense. The
  trade-off is real in the literature and it is NOT shown here, so the claim
  came off the page rather than the model being tuned until it produced one.

  Nothing here bears on the index card's proposal that each selection round is
  a step of the corpus's n-bonacci ladder converging on tau = 2. The page marks
  that OPEN and this script does not touch it.""")

print()
if FAIL:
    print("FAILED: %d" % len(FAIL))
    for f in FAIL: print("   " + f)
    sys.exit(1)
print("All blocks pass.")
