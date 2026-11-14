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
  [5] the dm3 row test
  [6] K as feedback strength (curvature), constant K => no F, critical duration T_c: is bone recovery, as fitted, a spiral sink?
  [7] negative controls: corrupted inputs that the checks must reject
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


print("[6] K as the feedback strength (curvature of the restoring potential), and the F test on the mechanostat loop")
# loop: h' = -r (h - hstar(L)); V = (r/2)(h - hstar)^2 so V'' = r = K, whatever L is
r_fn = math.log(2) / 211.0
hE, hc, eps0 = 1.0, 0.9, 1.0
def h_t(L, t): hs = L / eps0; return hs + (hE - hs) * math.exp(-r_fn * t)
check("K = V'' = r = ln2/211 = 0.003285 per day at the femoral neck", abs(r_fn - 0.003285) < 1e-6, f"{r_fn:.6f}")
rates = []
for L in (0.95, 0.9, 0.85, 0.5, 0.1):
    d = 1e-6                                 # numerical rate of approach: -d ln|h - h*| / dt
    hs = L / eps0
    lam = -(math.log(abs(h_t(L, 100 + d) - hs)) - math.log(abs(h_t(L, 100) - hs))) / d
    rates.append(lam)
check("the measured relaxation rate equals r at every loading (no critical slowing; exponent 0, not 1/2)", all(abs(x - r_fn) < 1e-7 for x in rates), str([round(x, 6) for x in rates]))
check("so F is absent as modelled: the rate does not vanish toward any loading", max(rates) - min(rates) < 1e-7)
for L in (0.89, 0.85, 0.8, 0.7):
    hs = L / eps0
    Tc = math.log((hE - hs) / (hc - hs)) / r_fn
    check(f"T_c at loading {L}: h(T_c) = h_c", abs(h_t(L, Tc) - hc) < 1e-9, f"T_c = {Tc:.1f} d = {Tc/211:.3f} half-times")
check("T_c grows without bound as loading approaches L_c = eps0*h_c = 0.9 (loading 0.89999 -> over 10 half-times)", math.log((hE - 0.89999) / (hc - 0.89999)) / r_fn / 211 > 10)
check("pelvis K / femoral neck K = 211/97 = 2.175 (sourced half-times)", abs((math.log(2)/97) / r_fn - 211/97) < 1e-9)
check("constant K gives a proportional residue: doubling the landing loss doubles the 12-month deficit", abs((2*6.8*0.5**(365/211)) / (6.8*0.5**(365/211)) - 2) < 1e-12)

print("[7] negative controls: each check above must be able to fail. A corrupted input is fed to the same test and must be REJECTED")
def rejects(label, ok):
    """PASS only if the corrupted case fails the check it is aimed at."""
    check("control: " + label, not ok)
# (a) the pelvis/femoral-neck ratio test must reject a wrong half-time (pelvis 211 instead of 97)
rejects("pelvis K / femoral neck K test rejects a wrong pelvis half-time (211)", abs((math.log(2)/211) / r_fn - 211/97) < 1e-9)
# (b) the no-critical-slowing test must reject a loop whose rate falls toward L_c = 0.9
def rate_bad(L, t=100.0, d=1e-6):
    rr = r_fn * max(0.9 - L, 1e-3)           # corrupted loop: K shrinks as loading approaches 0.9
    hs = L / eps0
    f = lambda tt: hs + (hE - hs) * math.exp(-rr * tt)
    return -(math.log(abs(f(t + d) - hs)) - math.log(abs(f(t) - hs))) / d
bad_rates = [rate_bad(L) for L in (0.5, 0.8, 0.85, 0.89)]
rejects("F-absent test rejects a loop whose rate vanishes toward L_c", max(bad_rates) - min(bad_rates) < 1e-7)
# (c) the sign test must reject a wrong-signed rate
rejects("'all five mu negative' test rejects a flipped sign", all(-m < 0 for m in mu.values()))
# (d) the proportional-residue test must reject a residue that grows faster than the loss
rejects("proportional-residue test rejects a residue quadratic in the loss", abs(((2*6.8)**2 * 0.5**(365/211)) / (6.8**2 * 0.5**(365/211)) - 2) < 1e-12)
# (e) T_c must reject a wrong closed form (log of the inverted ratio)
Tc_ok = math.log((hE - 0.8/eps0) / (hc - 0.8/eps0)) / r_fn
Tc_bad = math.log((hc - 0.8/eps0) / (hE - 0.8/eps0)) / r_fn
rejects("h(T_c) = h_c test rejects an inverted T_c formula", abs(h_t(0.8, Tc_bad) - hc) < 1e-9)
check("control sanity: the correct T_c is accepted by the same test", abs(h_t(0.8, Tc_ok) - hc) < 1e-9)

print("[HONESTY]")
print("  Source numbers are typed from one 2006 NASA manuscript and one 2022 abstract; the 2006 manuscript predates ARED (installed 2008).")
print("  The half-times are the source's own fits; this script does not refit raw data (none held).")
print("  Section [3] compares femoral-neck DXA to tibia HR-pQCT: different bones, methods and crews. It is a consistency check, not a test.")
print("  Section [6] is the mechanostat toy loop (assumptions: one slow variable, h* = L/eps0, a critical thickness h_c); it is not fitted to data.")
print("  Nothing here tests kappa*, a fold, or hysteresis in bone: the data held cannot.")
print("\nFAIL: %d" % len(FAIL) if FAIL else "\nALL PASS")
sys.exit(1 if FAIL else 0)
