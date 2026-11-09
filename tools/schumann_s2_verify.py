#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
schumann_s2_verify.py -- arithmetic behind section 2 of ch-schumann-dual.html.

The page used to say f2/f1 ~ 14.1/7.83 ~ 1.827 is "within 0.7%" of eta.
14.1/7.83 is 1.8008, not 1.827; 1.827 is what 14.3 Hz gives (to rounding).
This script states the whole measured range and the gap to eta at each end,
and checks the page text against it. Standard library only.

    python3 tools/schumann_s2_verify.py
Exit 0 iff every check passes (the failing control must FAIL to count).
"""
import re, sys, pathlib

F1, F2_LO, F2_HI = 7.83, 14.1, 14.3          # Table 1 on the page
STD_F2 = 14.30                               # Table 1 "Standard" column
# eta: real root of t^3 = t^2 + t + 1, by bisection
lo, hi = 1.0, 2.0
for _ in range(200):
    mid = (lo + hi) / 2
    if mid**3 - mid**2 - mid - 1 < 0: lo = mid
    else: hi = mid
ETA = (lo + hi) / 2
SQRT3 = 3 ** 0.5

def gap(r, ref): return (ref - r) / ref * 100

r_lo, r_hi, r_std = F2_LO / F1, F2_HI / F1, STD_F2 / F1
res = []
def check(name, ok): res.append((name, ok)); print(("PASS " if ok else "FAIL ") + name)

print(f"eta        = {ETA:.6f}")
print(f"sqrt(3)    = {SQRT3:.6f}")
print(f"14.1/7.83  = {r_lo:.4f}   below eta by {gap(r_lo, ETA):.2f}%   above sqrt3 by {(r_lo-SQRT3)/SQRT3*100:.2f}%")
print(f"14.3/7.83  = {r_hi:.4f}   below eta by {gap(r_hi, ETA):.2f}%   above sqrt3 by {(r_hi-SQRT3)/SQRT3*100:.2f}%")
print(f"std 14.30/7.83 = {r_std:.4f}  (Table 1 'Standard' column; same as top of measured)")
print(f"7.83*eta   = {F1*ETA:.2f} Hz (outside 14.1-14.3 by {F1*ETA-F2_HI:.2f} to {F1*ETA-F2_LO:.2f} Hz)")

check("eta solves t^3=t^2+t+1", abs(ETA**3 - ETA**2 - ETA - 1) < 1e-12)
check("14.1/7.83 rounds to 1.801 (not 1.827)", round(r_lo, 3) == 1.801)
check("14.3/7.83 rounds to 1.826", round(r_hi, 3) == 1.826)
check("gap to eta at low end ~2.1%", abs(gap(r_lo, ETA) - 2.09) < 0.01)
check("gap to eta at high end ~0.7%", abs(gap(r_hi, ETA) - 0.71) < 0.01)
check("whole measured range is below eta", r_hi < ETA)
check("whole measured range is nearer eta than sqrt3", all(abs(r-ETA) < abs(r-SQRT3) for r in (r_lo, r_hi)))
check("'0.7%' holds only at the top of the range", gap(r_lo, ETA) > 0.7 + 1 and gap(r_hi, ETA) < 0.8)
check("Table 1 standard ratio is NOT sqrt3 (so sqrt3 is the ideal cavity, not Table 1)", abs(r_std - SQRT3) > 0.05)
check("eta*f1 = 14.40 lies outside the quoted 14.1-14.3", not (F2_LO <= F1*ETA <= F2_HI))
# failing control: the old claim must not pass
check("CONTROL: old claim 14.1/7.83 = 1.827 is rejected", abs(r_lo - 1.827) > 0.01)

page = pathlib.Path(__file__).resolve().parent.parent / "ch-schumann-dual.html"
txt = page.read_text(encoding="utf-8")
sec = txt[txt.index("The measured ratio is f₂/f₁"):txt.index("§3 — Ionospheric")]
check("PAGE: old '≈ 1.827 is within 0.7%' wording gone", "≈ 1.827 is within" not in sec)
check("PAGE: §2 states 1.80 and 1.83 ends", "1.80" in sec and "1.83" in sec)
check("PAGE: §2 states 2.1%", "2.1%" in sec)
check("PAGE: §2 does not claim a match to eta",  "first empirical signal" not in sec)
bad = [m for m in re.finditer(r"matches measured 14\.1", txt)]
check("PAGE: ladder note no longer says eta*f1 'matches measured'", not bad)

fails = [n for n, ok in res if not ok]
print(f"\n{len(res)-len(fails)}/{len(res)} pass")
sys.exit(1 if fails else 0)
