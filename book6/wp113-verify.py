#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""wp113-verify.py — companion to book6/wp113-three-terms-in-a-fingernail.html.

Seven blocks. numpy only, as in wp110 and wp112. Every number in the paper is
produced here, and the three error terms are computed separately so that the
crossover table in the paper is an output rather than an assertion.

  [1] The change of variable. t -> x = v t, and back. The two rates and the
      ratio between them.
  [2] Term one, the write head. Keratinisation completes over a zone of width w,
      so the record is the true signal convolved with a kernel of width w/v in
      time. The transfer function of a box kernel is a sinc; its first zero and
      its half-power point are computed, not quoted.
  [3] Term two, the read. Segmental analysis is systematic sampling with an
      arbitrary start of a one-dimensional signal whose ends do not vanish.
      That is the p = 0 case of WP-112, so the error should fall as n^-1 and
      not n^-2. Measured here on the same Weierstrass construction.
  [4] Term three, the warp. v is unknown and slowly varying, so a dated event is
      displaced by an amount LINEAR in its distance from the matrix.
  [5] Which term dominates where. The crossover is computed from [2], [3], [4].
  [6] A two-site transit observation against published replacement times.
  [7] The cross-references resolve.

Run:  python3 book6/wp113-verify.py     (from the repository root, a few seconds)

Principia Orthogona - Vol VI - G6 LLC - CC BY-NC-ND 4.0
"""
import sys, math, os
import numpy as np

FAIL = []
def check(label, ok, detail=""):
    print(f"    {'PASS' if ok else 'FAIL'}  {label}" + (f"   {detail}" if detail else ""))
    if not ok: FAIL.append(label)
    return ok

# Nominal rates. Ranges commonly quoted in the clinical literature; the paper
# treats them as nominal and every consequence below is reported as a function
# of them rather than as a fixed number.
V_FINGER_MM_MONTH = 3.0      # 2.5 - 3.5
V_TOE_MM_MONTH    = 1.2      # 1.0 - 1.6
V_HAIR_MM_DAY     = 0.35     # 0.30 - 0.40

print("\n[1] The change of variable")
print("    The matrix writes the state at time t into the shaft at x = v t.")
print("    Reading back is t = x / v. That is the whole translation.")
print(f"    fingernail {V_FINGER_MM_MONTH} mm/month   toenail {V_TOE_MM_MONTH} mm/month"
      f"   scalp hair {V_HAIR_MM_DAY} mm/day = {V_HAIR_MM_DAY*30.44:.1f} mm/month")
ratio = V_FINGER_MM_MONTH / V_TOE_MM_MONTH
print(f"    finger : toe = {ratio:.2f}")
check("two sites in one body differ by about a factor of two",
      1.8 < ratio < 3.5, f"{ratio:.2f} — the exchange rate is not one number")

print("\n[2] Term one: the write head has width")
print("    Keratinisation completes over a zone of width w, so the shaft carries")
print("    the true signal convolved with a kernel of that width. In time the")
print("    kernel is w/v wide. For a box kernel the transfer function is")
print("        H(f) = sinc(pi f T),  T = w/v")
print("    first zero at f = 1/T, half power at f T = 0.4429 (solving sinc^2 = 1/2).")
# solve sinc^2(pi u) = 1/2 for u = f T
from bisect import bisect
def sinc2(u):
    if u == 0: return 1.0
    x = math.pi*u
    return (math.sin(x)/x)**2
lo, hi = 0.0, 1.0
for _ in range(200):
    mid = (lo+hi)/2
    if sinc2(mid) > 0.5: lo = mid
    else: hi = mid
u_half = (lo+hi)/2
print(f"    solved: f T at half power = {u_half:.4f}")
check("the half-power point is the classical 0.443", abs(u_half - 0.4429) < 2e-3,
      f"{u_half:.4f}, computed by bisection on sinc^2 = 1/2, not quoted")
print(f"    {'w (mm)':>8} {'T = w/v (days)':>16} {'shortest resolved period (days)':>34}")
for w in (1.0, 2.0, 3.0, 5.0):
    T = w / V_HAIR_MM_DAY
    print(f"    {w:8.1f} {T:16.1f} {1.0/(u_half/T):34.1f}")
w_nom = 2.0
T_nom = w_nom / V_HAIR_MM_DAY
P_min = 1.0/(u_half/T_nom)
print(f"    At the nominal w = {w_nom} mm: anything faster than a period of"
      f" {P_min:.0f} days is attenuated below half power.")
check("the write head alone imposes a limit of order a week or two",
      7 < P_min < 21, f"{P_min:.1f} days at w = {w_nom} mm")

print("\n[3] Term two: the read is a systematic sample, and it is the p = 0 case")
B, NT = 3, 26
def weier(H, seed):
    rng = np.random.default_rng(seed)
    ph = rng.uniform(0, 2*math.pi, NT)
    amp = (B ** (-H)) ** np.arange(NT); frq = (B ** np.arange(NT)) * math.pi
    def W(z):
        z = np.asarray(z, float)[..., None]
        return (amp*np.cos(frq*z + ph)).sum(axis=-1)
    zz = np.linspace(0, 1, 200001)
    return W, 0.9/np.abs(W(zz)).max()
NS = [17, 29, 53, 101, 199, 401, 797, 1601]
R, SEEDS = 300, [0, 1, 2, 3]
rng = np.random.default_rng(11)
print("    A hair cut into n segments from an arbitrary start, with the signal")
print("    not vanishing at either cut. WP-112 says p = 0, so gamma = 1.")
print(f"    {'H':>5} {'tail gamma':>11} {'r':>10}")
gs = []
for H in (0.5, 0.9):
    acc = np.zeros(len(NS))
    for sd in SEEDS:
        W, c = weier(H, sd)
        for i, n in enumerate(NS):
            u = rng.random(R)[:, None]
            z = (u + np.arange(n)[None, :]) / n
            e = (1.0 + c*W(z)).mean(axis=1)
            acc[i] += e.std(ddof=1)/e.mean()
    cv = acc/len(SEEDS); nn = np.array(NS, float)
    gt = -np.polyfit(np.log(nn[-5:]), np.log(cv[-5:]), 1)[0]
    rt = np.corrcoef(np.log(nn[-5:]), np.log(cv[-5:]))[0, 1]
    gs.append(gt)
    print(f"    {H:5.2f} {gt:11.3f} {rt:10.5f}")
check("the read term falls as 1/n, not 1/n^2", all(0.93 < g < 1.10 for g in gs),
      "inherited from WP-112 and re-measured on the time axis: a segmental series "
      "is a full power less precise than whole-organ intuition suggests")

print("\n[4] Term three: the warp displaces a date in proportion to its distance")
print("    If the true rate differs from the assumed rate by a factor (1+eps),")
print("    an event read at distance x is dated t = x/v_assumed instead of")
print("    x/v_true, an error of eps*t. Linear in t: the far end is worst.")
print(f"    {'eps':>7} " + " ".join(f"{m:>7d}mo" for m in (1, 3, 6, 12)))
for eps in (0.05, 0.10, 0.20):
    print(f"    {eps:7.0%} " + " ".join(f"{eps*m*30.44:8.1f}d" for m in (1, 3, 6, 12)))
check("a 20% rate error misdates a six-month-old event by over a month",
      0.20*6*30.44 > 30, f"{0.20*6*30.44:.0f} days")

print("\n[5] Which term dominates where")
print("    Read term: with 1 cm segments on a hair, one segment is one month, so")
print("    the read cannot resolve anything shorter than that however precise it is.")
seg_days = 10.0 / V_HAIR_MM_DAY
print(f"    1 cm segment at {V_HAIR_MM_DAY} mm/day = {seg_days:.1f} days per segment")
print()
print(f"    {'regime':<34} {'limit set by':<22} {'scale'}")
print(f"    {'-'*34} {'-'*22} {'-'*22}")
print(f"    {'events shorter than ~2 weeks':<34} {'the write head':<22} {P_min:.0f} days, irrecoverable")
print(f"    {'2 weeks to ~1 month':<34} {'the segment length':<22} {seg_days:.0f} days per cut")
print(f"    {'dating an event months back':<34} {'the warp':<22} {'eps x t, linear'}")
check("the write head and the segment length are within a factor of three",
      1/3 < P_min/seg_days < 3,
      f"{P_min:.0f} d against {seg_days:.0f} d — cutting finer than the write head "
      "buys resolution that is not in the record")

print("\n[6] A two-site transit observation against published replacement times")
obs = {"fingernail": 6.0, "toenail": 12.0}
lit = {"fingernail": (4.0, 6.0), "toenail": (12.0, 18.0)}
for site, months in obs.items():
    lo, hi = lit[site]
    inside = lo <= months <= hi
    print(f"    {site:<12} observed transit {months:4.1f} months   commonly quoted {lo:.0f}-{hi:.0f}")
    check(f"{site} transit is inside the quoted range", inside,
          "at the fast end" if months <= (lo+hi)/2 else "")
r_obs = obs["toenail"]/obs["fingernail"]
print(f"    observed toe:finger transit ratio = {r_obs:.2f}")
check("and the ratio matches the rate ratio from block [1]",
      abs(r_obs - ratio) < 1.2, f"{r_obs:.2f} against {ratio:.2f}")

print("\n[7] The cross-references resolve")
for rel in ["book6/wp112-the-ends-not-the-middle.html", "book6/wp112-verify.py",
            "book6/wp110-not-rough-enough.html", "book6/ch-aperiodic-multiplying-media.html"]:
    check(rel, os.path.exists(rel))

print("""
[HONESTY] What this script establishes, and what it does not.

  ESTABLISHED. The arithmetic of all three terms, from the stated nominal rates:
  the half-power point of a box write head, solved rather than quoted; the
  decay exponent of the read term, measured on the WP-112 construction and
  inherited from its p = 0 result; the linear growth of the warp term with the
  age of the event; and the crossover scales that follow.

  NOMINAL, NOT MEASURED. Every growth rate here is a commonly quoted clinical
  figure, and the width of the keratinisation zone most of all -- it is the
  least well pinned of the inputs and every consequence in block [2] is printed
  as a function of it for that reason. Nothing here measures a rate.

  A BOX IS A MODEL. The write head is treated as a box kernel because that is
  the conservative choice for a first cut: a smoother kernel cuts off sooner,
  so the resolution limit computed here is optimistic, not pessimistic.

  THE OBSERVATION IN BLOCK [6] IS N = 1. Two transit times, one subject, one
  year, reported retrospectively, with arrival at the free edge observed rather
  than distances measured. It is consistent with the published ranges and it
  calibrates nothing. A matrix injury can also perturb the very rate it marks,
  which is a confound the fluorochrome version of this measurement does not have.

  NOT ATTEMPTED. No published keratin chronology is reanalysed here, and the
  claim that the three terms are separable in practice is a claim about the
  model, not a demonstration on data.
""")
print(f"{'ALL CHECKS PASSED' if not FAIL else 'FAILED: ' + ', '.join(FAIL)}")
sys.exit(1 if FAIL else 0)
