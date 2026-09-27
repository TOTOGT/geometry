#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book20/ch03-verify.py -- every number on book20/ch03-what-to-expect.html. Run first (R24).

    python3 book20/ch03-verify.py [--downloads DIR]

  [1] Evans & Rosenthal ch 3: the definition (p. 130) and the opening examples
  [2] Example 3.1.12-13 (p. 133-134): St. Petersburg, and the truncated game's value
  [3] a threshold decision: expected cost against the false-alarm rate; the minimum is
      not at zero error of either kind
  [4] the same decision under this corpus's own costs, as a parameter sweep
  [HONESTY]
"""
import math, os, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def dl():
    if "--downloads" in sys.argv: return Path(sys.argv[sys.argv.index("--downloads") + 1])
    for c in ("~/mnt/Downloads", "~/Downloads"):
        p = Path(os.path.expanduser(c))
        if p.is_dir(): return p
DL = dl()
ER = "Probability and Statistics- The Science of Uncertainty.pdf"
try:
    T = subprocess.run(["pdftotext", "-layout", str(DL / ER), "-"], capture_output=True, text=True, timeout=120).stdout.split("\f")
except Exception:
    T = None

print("[1] definition and opening examples")
check("E X for X in {0,10} equally likely = 5", 0*.5 + 10*.5 == 5)
check("E Y for Y=6 w.p. 1/3, 15 w.p. 2/3 = 12", abs(6/3 + 15*2/3 - 12) < 1e-12)
if T:
    check("chapter 3 opens on printed p. 129 (pdf 143)", "Chapter 3" in T[142] and "129" in T[142])
    check("the fair-price reading is in the text, with its limit flagged to Example 3.1.12", "fair gambling" in T[142] and "Example 3.1.12" in T[142])

print("[2] St. Petersburg")
partial = [sum(2**z * 0.5**(z+1) for z in range(N)) for N in (10, 20, 30)]
check("each term contributes 1/2 cent, so the sum diverges", partial == [5.0, 10.0, 15.0], str(partial))
cap = 30
trunc = sum(2**min(cap, z) * 0.5**(z+1) for z in range(cap+1)) + 2**cap * 0.5**(cap+1)
check("award capped at 2^30 cents: expected value 16 cents", abs(trunc - 16) < 1e-9, f"{trunc} cents")
print(f"     2^30 cents = ${2**30/100:,.2f}")
if T:
    check("Example 3.1.12 is on printed p. 133 (pdf 147)", "EXAMPLE 3.1.12 The St. Petersburg Paradox" in T[146])
    check("Example 3.1.13 caps the award at 2^30 cents", "Truncated" in T[147] or "Truncated" in T[146])

print("[3] a threshold decision")
Phi = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))
d, prev = 2.0, 0.10          # signal shifted by 2 sd; 10% of cases are real
cFA, cMISS = 1.0, 5.0        # a miss costs five times a false alarm
def cost(t):
    fa = 1 - Phi(t)          # noise above threshold
    miss = Phi(t - d)        # signal below threshold
    return (1 - prev) * fa * cFA + prev * miss * cMISS, fa, miss
grid = [i / 1000 for i in range(-3000, 6001)]
best = min(grid, key=lambda t: cost(t)[0])
c, fa, miss = cost(best)
exact = d / 2 + math.log(((1 - prev) * cFA) / (prev * cMISS)) / d
check("grid optimum matches the closed form t* = d/2 + ln[(1-p)cFA/(p cMISS)]/d", abs(best - exact) < 1e-3, f"t* = {exact:.3f}")
print(f"     at t*: false-alarm rate {fa:.3f}, miss rate {miss:.3f}, expected cost {c:.4f}")
c0, fa0, m0 = cost(-3.0)     # never miss: flag almost everything
c1, fa1, m1 = cost(6.0)      # never false-alarm: flag almost nothing
print(f"     flag everything: false alarms {fa0:.3f}, misses {m0:.4f}, cost {c0:.4f}")
print(f"     flag nothing:    false alarms {fa1:.1e}, misses {m1:.3f}, cost {c1:.4f}")
check("neither error rate is zero at the optimum", fa > 0.01 and miss > 0.01)
check("the optimum beats both extremes by at least a factor of two", c < c0 / 2 and c < c1 / 2, f"{c:.3f} vs {c0:.3f}, {c1:.3f}")

print("[4] the corpus's scanners: the same trade, swept over the cost ratio")
sweep = []
for ratio in (1, 5, 20, 100):
    t = d / 2 + math.log((1 - prev) / (prev * ratio)) / d
    _, fa, miss = cost(t)
    sweep.append((fa, miss))
    print(f"     miss costs {ratio:>3}x a false alarm: t* = {t:+.2f}  false alarms {fa:.3f}  misses {miss:.3f}")
check("as misses get dearer the optimal false-alarm rate rises", all(a[0] < b[0] for a, b in zip(sweep, sweep[1:])))
check("and at every ratio both error rates stay strictly inside (0.01, 0.99)", all(0.01 < x < 0.99 for pair in sweep for x in pair))

print("""
[HONESTY]
[1]-[2] recompute the textbook's arithmetic. [3] is a model chosen for illustration:
a two-normal signal-detection problem with separation 2, prevalence 10% and a 5:1 cost
ratio. The numbers are not measurements of anything; the shape -- an interior optimum
-- holds for any continuous pair of overlapping distributions and any positive costs.
[4] is a parameter sweep of the same model, not a measurement of this corpus's
scanners, whose error rates have not been measured.
""")
print(f"{len(FAIL)} FAIL")
sys.exit(1 if FAIL else 0)
