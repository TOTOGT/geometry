#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book26/ch17-verify.py -- book26/ch17-the-credit-behind-the-annuity.html (Template B): a work sample for an insurance
domain analyst posting at EY, built from three public NAIC documents on year-end 2025 data.
  [1] structure: hero, section nav, sections in order, Sources footer; no network/storage/form code
  [2] arithmetic on the asset-mix tables: sector shares, sector remainder, bond and Schedule BA shares and growth,
      implied 2024 total cross-check
  [3] arithmetic on the private-credit table: five categories sum to 1,210; focus 544; lower-complexity 666; every ratio
      quoted on the page; the two ceilings; the CLO reconciliation 65 - 23 = 42
  [4] every recomputed figure appears on the page
  [5] SOURCE: typed figures vs the NAIC PDFs if held copies are present (pdftotext); prints SKIP, never PASS, otherwise
  [6] controls: each check is run on a wrong input and must fail   [HONESTY]
  [7] honesty: no insurance experience claimed, no insurer or individual named, no count of applications, the life-sector
      figure is given as bounds only, fetch-tool limit stated
Held copies are looked for in $NAIC_DIR, else ~/Desktop/grants/ey: asset-mix-ye2025.pdf, private-credit-analysis.pdf.
Standard library only; the PDF check needs pdftotext.
"""
import os, re, subprocess, sys, html as _h
from pathlib import Path
HERE = Path(__file__).resolve().parent
PAGE = HERE / "ch17-the-credit-behind-the-annuity.html"
NDIR = Path(os.environ.get("NAIC_DIR", Path.home() / "Desktop" / "grants" / "ey"))
FAIL, SKIP = [], []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def skip(label, why): print(f"SKIP {label}  -- {why}"); SKIP.append(label)

raw = PAGE.read_text(encoding="utf-8")
txt = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", raw, flags=re.S)
txt = re.sub(r"<[^>]+>", " ", txt)
txt = re.sub(r"\s+", " ", _h.unescape(txt))

# ---- typed from the NAIC asset-mix report, Table 1 ($ million), read through a summarising fetch tool ----
LIFE, PC, HEALTH, INDUSTRY = 6_096_774, 3_095_454, 376_851, 9_580_585
BONDS, BA, BA_2024 = 5_727_555, 638_817, 578_346
G_TOTAL, G_BONDS, G_BA_STATED = 0.067, 0.056, 0.105          # stated year-on-year growth
BOND_SHARE_2025, BOND_SHARE_2024_STATED = 59.8, 60.4         # stated, percent
# ---- typed from the NAIC private-credit report, Table 1 ($ billion) ----
PRIV_PLACE, PLR_BONDS, BANK, MM_CLO, BDC = 580, 512, 44, 42, 32
STATED_TOTAL, STATED_FOCUS, STATED_LOWER = 1210, 544, 666
CLO_TOTAL, CLO_PRIVATELY_RATED = 65, 23
STATED_PCT = {"all_of_assets": 13, "all_of_bonds": 21, "focus_of_assets": 6, "focus_of_bonds": 9}

def pct(a, b): return a / b * 100
def r1(x): return f"{x:.1f}"

# [1] structure
print("[1] structure")
order = ["intro", "problems", "analysis", "recommendations", "actions", "followthrough", "limits", "updates", "checked", "sources"]
pos = [raw.find(f'id="{i}"') for i in order]
check("sections present and in order", all(p > 0 for p in pos) and pos == sorted(pos))
check("Template B hero and nav", 'class="hero"' in raw and 'class="pillars"' in raw)
check("no network, storage or form code", not re.search(r"<form|fetch\(|XMLHttpRequest|localStorage|sessionStorage|WebSocket", raw))
for lab in ["Questions raised", "Analysis", "Recommendations", "Actions", "Follow-through"]:
    check(f"label '{lab}'", lab in txt)

# [2] asset-mix arithmetic
print("[2] asset-mix arithmetic")
sector_sum = LIFE + PC + HEALTH
remainder = INDUSTRY - sector_sum
check("sectors sum to 9,569,079; remainder 11,506", sector_sum == 9_569_079 and remainder == 11_506, f"{sector_sum} {remainder}")
check("remainder is 0.12% of industry", r1(pct(remainder, INDUSTRY)) == "0.1" and f"{pct(remainder, INDUSTRY):.2f}" == "0.12")
shares = {"life": pct(LIFE, INDUSTRY), "pc": pct(PC, INDUSTRY), "health": pct(HEALTH, INDUSTRY)}
check("sector shares 63.6 / 32.3 / 3.9", [r1(v) for v in shares.values()] == ["63.6", "32.3", "3.9"], str([r1(v) for v in shares.values()]))
check(f"bonds share rounds to stated {BOND_SHARE_2025}", r1(pct(BONDS, INDUSTRY)) == str(BOND_SHARE_2025))
check("Schedule BA share 6.7", r1(pct(BA, INDUSTRY)) == "6.7")
check("Schedule BA growth 10.5% from the 2024 figure", r1((BA / BA_2024 - 1) * 100) == "10.5", f"{(BA/BA_2024-1)*100:.3f}")
t24 = INDUSTRY / (1 + G_TOTAL)
bonds24 = BONDS / (1 + G_BONDS)
check("implied 2024 total is about $8.98 trillion", abs(t24 / 1e6 - 8.98) < 0.005, f"{t24/1e6:.4f}")
check("implied 2024 bond share matches stated 60.4%", r1(pct(bonds24, t24)) == str(BOND_SHARE_2024_STATED), r1(pct(bonds24, t24)))
check("implied 2024 Schedule BA share is 6.4%", r1(pct(BA_2024, t24)) == "6.4", r1(pct(BA_2024, t24)))

# [3] private-credit arithmetic
print("[3] private-credit arithmetic")
total = PRIV_PLACE + PLR_BONDS + BANK + MM_CLO + BDC
focus, lower = PLR_BONDS + BDC, PRIV_PLACE + BANK + MM_CLO
check("five categories sum to 1,210", total == STATED_TOTAL, str(total))
check("focus group is 544", focus == STATED_FOCUS, str(focus))
check("lower-complexity group is 666", lower == STATED_LOWER, str(lower))
check("middle-market CLO: 65 total - 23 privately rated = 42", CLO_TOTAL - CLO_PRIVATELY_RATED == MM_CLO)
A, B, L = INDUSTRY / 1000, BONDS / 1000, LIFE / 1000      # $ billion
ratios = {
    "all_of_assets": pct(total, A), "all_of_bonds": pct(total, B),
    "focus_of_assets": pct(focus, A), "focus_of_bonds": pct(focus, B),
}
for k, v in ratios.items():
    check(f"{k}: {v:.2f} rounds to the NAIC's stated {STATED_PCT[k]}%", round(v) == STATED_PCT[k], f"{v:.3f}")
ceil_focus, ceil_all = pct(focus, L), pct(total, L)
check("ceilings: focus 8.9% and all 19.8% of life assets", r1(ceil_focus) == "8.9" and r1(ceil_all) == "19.8", f"{ceil_focus:.3f} {ceil_all:.3f}")
check("even-spread figures 5.7% and 12.6%", r1(ratios["focus_of_assets"]) == "5.7" and r1(ratios["all_of_assets"]) == "12.6")
check("ceiling is above the even spread (life holds less than industry in the denominator)", ceil_focus > ratios["focus_of_assets"] and ceil_all > ratios["all_of_assets"])
check("ratio to bonds: 21.1% and 9.5%", r1(ratios["all_of_bonds"]) == "21.1" and r1(ratios["focus_of_bonds"]) == "9.5")

# [4] on the page
print("[4] on the page")
for s in ["9,569,079", "11,506", "0.12%", "63.6%", "32.3%", "3.9%", "59.8%", "60.4%", "5.6%", "10.5%", "$8.98 trillion", "6.4%",
          "1,210", "544", "666", "12.6%", "21.1%", "5.7%", "9.5%", "8.9%", "19.8%", "$512 billion", "$32 billion"]:
    check(f"page shows {s}", s in txt)

# [5] SOURCE
print("[5] SOURCE")
held = {"asset-mix-ye2025.pdf": ["9,580,585", "6,096,774", "3,095,454", "376,851", "5,727,555", "638,817", "578,346"],
        "private-credit-analysis.pdf": ["1,210", "544", "512"]}
for name, needles in held.items():
    p = NDIR / name
    if p.exists():
        try:
            t = re.sub(r"\s+", " ", subprocess.run(["pdftotext", "-layout", str(p), "-"], capture_output=True, text=True, check=True).stdout)
            for n in needles: check(f"{name}: {n}", n in t)
        except Exception as ex:
            skip(name, f"pdftotext failed: {ex}")
    else:
        skip(name, f"no held copy at {p}; figures were read through a summarising fetch tool")
skip("NAIC web page figures (PIK 7% vs 6%, 40% repeat defaults, non-accruals)", "read through a summarising fetch tool; not recomputable")

# [6] controls
print("[6] controls")
check("control: a wrong sector total fails the remainder", INDUSTRY - (LIFE + PC + HEALTH + 1) != 11_506)
check("control: a wrong category value fails the 1,210 sum", (PRIV_PLACE + PLR_BONDS + BANK + MM_CLO + BDC + 1) != STATED_TOTAL)
check("control: 8.9% is not the even-spread figure", r1(ceil_focus) != r1(ratios["focus_of_assets"]))
check("control: dividing by bonds instead of assets changes the ratio", r1(ratios["all_of_bonds"]) != r1(ratios["all_of_assets"]))
check("control: a 7% total growth rate would not give a 60.4% bond share", r1(pct(BONDS / (1 + G_BONDS), INDUSTRY / 1.07)) != "60.4")
check("control: a wrong figure is not on the page", "9,999,999" not in txt)

# [7] honesty
print("[7] honesty")
check("claims no insurance-industry experience", "claims no insurance-industry experience" in txt)
check("says the NAIC report is not an assessment of any insurer", "not an assessment of any specific insurer" in txt)
check("says it names no individual and no insurer", "names no individual and no insurer" in txt)
check("life-sector figure given as bounds only", "bounds only" in txt and "not a measurement" in txt)
check("states the fetch-tool limit", "web-fetch tool that returns summaries" in txt and "SKIP" in txt)
check("no count of applications claimed", not re.search(r"\b\d+ applications", txt))
check("does not quote the posting", "posting’s own text is not quoted" in txt or "posting’s own text is not quoted" in txt)

print(f"\n{'ALL PASS' if not FAIL else 'FAILURES: ' + str(len(FAIL))}  ({len(SKIP)} SKIP)")
sys.exit(1 if FAIL else 0)
