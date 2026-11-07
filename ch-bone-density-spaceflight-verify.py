#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""ch-bone-density-spaceflight-verify.py -- every number computed on ch-bone-density-spaceflight.html (Book 3). Run first (R24).
    python3 ch-bone-density-spaceflight-verify.py
Inputs are the SOURCE NUMBERS below (typed from the sources named in the chapter; the sources are reported, not
re-measured). Everything else is arithmetic on them.
  [1] loss rate implied by the 2006 DXA numbers
  [2] recovery as a one-variable relaxation: mu = -ln2 / half-time, with the confidence range
  [3] what that relaxation predicts at 12 months, against the 2022 tibia deficits (different bone, different method)
  [4] the 4-half-life statement
  [5] the dm3 row test: is bone recovery, as fitted, a spiral sink?
  [HONESTY]
"""
import math, sys
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)

# Sibonga et al. (NASA manuscript dated 2006, 45 crew, mean flight 173 +/- 24 d): loss at landing % and 50% recovery time (days) with 95% CI
SIB = {  # site: (loss%, hl, hl_lo, hl_hi)
    "femoral neck": (6.8, 211, 129, 346),
    "trochanter":   (7.8, 255, 173, 377),
    "pelvis":       (7.7,  97,  56, 168),
    "lumbar spine": (4.9, 151,  72, 315),
    "calcaneus":    (2.9, 163,  67, 395),
}
FLIGHT_D = 173.0; DAYS_PER_MONTH = 30.4375
# Gabel et al. 2022 abstract: 17 astronauts, HR-pQCT tibia; at 12 months deficits 0.9-2.1 % ; 9 of 17 not fully recovered total BMD
GABEL_LO, GABEL_HI, GABEL_N, GABEL_NOT = 0.9, 2.1, 17, 9

print("[1] loss rate implied by the 2006 DXA numbers")
months = FLIGHT_D / DAYS_PER_MONTH
r = SIB["femoral neck"][0] / months
check("173 days is 5.68 months", abs(months - 5.68) < 0.01, f"{months:.3f}")
check("femoral neck 6.8 % over the mean flight is about 1.2 % per month if loss accrues evenly", abs(r - 1.2) < 0.01, f"{r:.3f} %/month")
r65 = 6.5 / months
check("with the 6.5 % printed in the Figure 1 caption instead, about 1.14 % per month", abs(r65 - 1.144) < 0.01, f"{r65:.3f}")
check("both sit inside the '1 to 2 percent per month' that the 2012 NASA article states for earlier crews", 1 <= r <= 2 and 1 <= r65 <= 2)

print("[2] recovery as relaxation: mu = -ln2 / half-time (per day), range from the 95% CI")
mu = {}
for site, (loss, hl, lo, hi) in SIB.items():
    m = -math.log(2) / hl; mlo = -math.log(2) / lo; mhi = -math.log(2) / hi
    mu[site] = m
    print(f"      {site:13s} HL {hl:4d} d  mu = {m:+.5f} /day  = {m*DAYS_PER_MONTH:+.4f} /month   range [{mlo:+.5f}, {mhi:+.5f}] /day")
check("femoral neck mu = -0.003285 per day", abs(mu["femoral neck"] + 0.003285) < 1e-6, f"{mu['femoral neck']:.6f}")
check("all five mu are negative (recovery relaxes toward preflight)", all(m < 0 for m in mu.values()))
check("pelvis relaxes about 2.2 times faster than the femoral neck (point estimates)", abs(mu["pelvis"] / mu["femoral neck"] - 211 / 97) < 1e-9, f"{211/97:.3f}")
check("the confidence ranges are wide: femoral neck half-time 129-346 d spans a factor of 2.7", abs(346 / 129 - 2.68) < 0.01, f"{346/129:.3f}")

print("[3] predicted deficit one year after return (exponential model) against the 2022 tibia deficits")
for site, (loss, hl, lo, hi) in SIB.items():
    res = loss * 0.5 ** (365.0 / hl)
    print(f"      {site:13s} {loss:4.1f} % at landing -> {res:5.2f} % below preflight at 365 d")
res_fn = 6.8 * 0.5 ** (365 / 211)
check("femoral neck: about 2.06 % still below preflight at 12 months", abs(res_fn - 2.06) < 0.01, f"{res_fn:.3f}")
res_all = {s: v[0] * 0.5 ** (365.0 / v[1]) for s, v in SIB.items()}
check("pelvis (HL 97 d) is nearly back at 12 months, under 1 %", res_all["pelvis"] < 1.0, f"{res_all['pelvis']:.2f}")
check("predicted 12-month deficits span 0.57-2.89 %, largest at the trochanter and femoral neck (the two longest half-times)", abs(min(res_all.values())-0.57)<0.01 and abs(max(res_all.values())-2.89)<0.01 and max(res_all, key=res_all.get)=="trochanter", str({k: round(v,2) for k,v in res_all.items()}))
inside = [k for k,v in res_all.items() if GABEL_LO <= v <= GABEL_HI]
check("two of the five predicted deficits (femoral neck 2.05, lumbar spine 0.92) fall inside the Gabel 12-month tibia range 0.9-2.1 % -- order-of-magnitude agreement only", sorted(inside)==["femoral neck","lumbar spine"], str(inside))
check("9 of 17 is 52.9 %", abs(GABEL_NOT / GABEL_N - 0.5294) < 1e-3, f"{GABEL_NOT/GABEL_N:.4f}")

print("[4] the 4-half-life statement")
four = max(v[1] for v in SIB.values()) * 4 / DAYS_PER_MONTH
check("4 half-lives restore 15/16 of the loss", abs((1 - 0.5 ** 4) - 15 / 16) < 1e-12)
check("with the slowest point-estimate half-time (255 d) that is 33.5 months, inside the stated 36", abs(four - 33.5) < 0.1 and four <= 36, f"{four:.2f} months")
four_hi = 346 * 4 / DAYS_PER_MONTH
check("with the upper end of the widest CI (346 d) it is 45 months, beyond 36", abs(four_hi - 45.5) < 0.2, f"{four_hi:.1f} months")

print("[5] the dm3 row test")
# A scalar relaxation x' = mu x has the single real eigenvalue mu: no complex pair, omega = 0.
omega = 0.0
check("fitted bone recovery has one real eigenvalue, so omega = 0 and it is NOT a spiral sink (needs mu<0 and omega>0)", not (mu["femoral neck"] < 0 and omega > 0))
check("its damping per cycle exp(2 pi mu/omega) is undefined (no cycle)", omega == 0)
check("a 12-month residual of about 30 % of the landing loss follows from a single 211-day half-time with no fold or memory", abs(0.5 ** (365 / 211) - 0.3015) < 1e-3, f"{0.5**(365/211):.4f}")

print("[HONESTY]")
print("  Source numbers are typed from one 2006 NASA manuscript and one 2022 abstract; the 2006 manuscript predates ARED (installed 2008).")
print("  The half-times are the source's own fits; this script does not refit raw data (none held).")
print("  Section [3] compares femoral-neck DXA to tibia HR-pQCT: different bones, methods and crews. It is a consistency check, not a test.")
print("  Nothing here tests kappa*, a fold, or hysteresis in bone: the data held cannot.")
print("\nFAIL: %d" % len(FAIL) if FAIL else "\nALL PASS")
sys.exit(1 if FAIL else 0)
