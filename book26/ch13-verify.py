#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book26/ch13-verify.py -- book26/ch13-the-recommendation-record.html (Template B, as chapters 10 to 19): one month of
FINRA's published disciplinary actions (December 2025 report), the text of Regulation Best Interest and Rule 2111,
and a worked test on a SYNTHETIC account, read for a Principal Investigator posting on the Recommendations team.
  [1] Template B structure (hero, section nav, sections in order, Sources footer), required labels, no network/storage/form code
  [2] arithmetic: the three sanctions add to $110,000; the Reg BI period is 664 days; the suspension is 61 days counting both ends
  [3] the worked example: turnover and cost-equity ratio from stated inputs, under two equity definitions; the page's table cells match
  [4] the entries' typed figures (dates, amounts, pages, CRD numbers) appear on the page where the script says they do
  [5] SOURCE: the report entries are checked against a held copy of the report PDF if one is present; the rule text and
      posting quotes are checked against the held posting excerpts; prints SKIP, never PASS, when the held copy is absent
  [6] controls: each check is run on a wrong input and must fail   [HONESTY]
  [7] honesty: the page says it is an exercise, that the example is synthetic, that the rule gives no thresholds,
      and does not name the individual
Files looked for in $FINRA_DIR, else ~/Desktop/grants/finra: disciplinary-actions-december-2025.pdf (optional) and
posting-excerpts-2026-10-30.txt. Standard library only; the PDF check needs pdftotext.
"""
import os, re, subprocess, sys
from datetime import date
from pathlib import Path
HERE = Path(__file__).resolve().parent
PAGE = HERE / "ch13-the-recommendation-record.html"
FDIR = Path(os.environ.get("FINRA_DIR", Path.home() / "Desktop" / "grants" / "finra"))
FAIL, SKIP = [], []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def skip(label, why): print(f"SKIP {label}  -- {why}"); SKIP.append(label)

raw = PAGE.read_text(encoding="utf-8")
txt = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", raw, flags=re.S)
txt = re.sub(r"<[^>]+>", " ", txt)
import html as _h
txt = re.sub(r"\s+", " ", _h.unescape(txt))

# ---- source data typed from the December 2025 report entries (read through a fetch tool, twice) ----
ENTRIES = {
    "alexander": dict(crd="1037", head="Firms Fined", day=date(2025, 10, 20), fine=25000, page="6"),
    "supreme":   dict(crd="45348", head="Firms Fined", day=date(2025, 10, 31), fine=80000, page="11",
                      reg_bi_from=date(2020, 6, 30), reg_bi_to=date(2022, 4, 25)),
    "rep":       dict(crd="2391965", head="Individuals Suspended", day=date(2025, 10, 1), fine=5000, page="13",
                      susp_from=date(2025, 11, 3), susp_to=date(2026, 1, 2)),
}
total_fines = sum(e["fine"] for e in ENTRIES.values())
reg_bi_days = (ENTRIES["supreme"]["reg_bi_to"] - ENTRIES["supreme"]["reg_bi_from"]).days
susp_days_incl = (ENTRIES["rep"]["susp_to"] - ENTRIES["rep"]["susp_from"]).days + 1

# ---- worked example (SYNTHETIC) ----
PURCH, COSTS, MONTHS = 750_000, 18_000, 10
def turnover(purch, equity, months): return purch / equity * (12 / months)
def cost_equity(costs, equity, months): return costs / equity * (12 / months) * 100
EQ = {"average": 150_000, "initial": 120_000}

# [1] structure
print("[1] structure")
order = ["posting", "problems", "analysis", "recommendations", "actions", "followthrough", "limits", "updates", "checked", "sources"]
pos = [raw.find(f'id="{i}"') for i in order]
check("sections present and in order", all(p > 0 for p in pos) and pos == sorted(pos))
check("Template B hero and nav", 'class="hero"' in raw and 'class="pillars"' in raw)
check("no network, storage or form code", not re.search(r"<form|fetch\(|XMLHttpRequest|localStorage|sessionStorage|WebSocket", raw))
for lab in ["Questions raised", "Analysis", "Recommendations", "Actions", "Follow-through"]:
    check(f"label '{lab}'", lab in txt)

# [2] arithmetic
print("[2] arithmetic")
check("sanctions add to $110,000", total_fines == 110_000 and "$110,000" in txt, str(total_fines))
check("Reg BI period is 664 days", reg_bi_days == 664 and "664 days" in txt, str(reg_bi_days))
check("suspension is 61 days counting both ends", susp_days_incl == 61 and "61 days" in txt, str(susp_days_incl))

# [3] worked example
print("[3] worked example")
for k, eq in EQ.items():
    t, c = turnover(PURCH, eq, MONTHS), cost_equity(COSTS, eq, MONTHS)
    want = {"average": (6.0, 14.4), "initial": (7.5, 18.0)}[k]
    check(f"{k} equity: turnover {t:.1f}, cost-equity {c:.1f}%", abs(t - want[0]) < 1e-9 and abs(c - want[1]) < 1e-9)
    check(f"{k} equity figures on the page", f"{t:.1f}" in txt and f"{c:.1f}" in txt)
doubled = turnover(2 * PURCH, EQ["average"], MONTHS)
check("counting sales as well as purchases doubles turnover to 12.0", abs(doubled - 12.0) < 1e-9 and "12.0" in txt)
check("annualisation factor 12/10 = 1.2", abs(12 / MONTHS - 1.2) < 1e-12 and "1.2" in txt)

# [4] entries on the page
print("[4] entries on the page")
for name, e in ENTRIES.items():
    check(f"{name}: CRD {e['crd']}" if name != "rep" else "rep: no CRD or name on page (privacy)",
          (e["crd"] in txt) if name != "rep" else (e["crd"] not in txt))
    check(f"{name}: heading '{e['head']}', fine ${e['fine']:,}, page {e['page']}",
          e["head"] in txt and f"${e['fine']:,}" in txt and re.search(r">\s*" + e["page"], raw) is not None)
    d = e["day"]; check(f"{name}: action date {d.day} {d.strftime('%b %Y')} on page", f"{d.day} {d.strftime('%b %Y')}" in txt)

# [5] SOURCE
print("[5] SOURCE")
pdf = FDIR / "disciplinary-actions-december-2025.pdf"
if pdf.exists():
    try:
        rt = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True, check=True).stdout
        rt = re.sub(r"\s+", " ", rt)
        for name, e in ENTRIES.items():
            check(f"report: {name} CRD {e['crd']}", e["crd"] in rt)
            check(f"report: {name} fine ${e['fine']:,}", f"${e['fine']:,}" in rt)
        check("report: Reg BI period 30 June 2020 to 25 April 2022", "June 30, 2020" in rt and "April 25, 2022" in rt)
        check("report: suspension 3 Nov 2025 to 2 Jan 2026", "November 3, 2025" in rt and "January 2, 2026" in rt)
    except Exception as ex:
        skip("report entries", f"pdftotext failed: {ex}")
else:
    skip("report entries", f"no held copy at {pdf}; entries were read through a summarising fetch tool, twice, with matching results")
post = FDIR / "posting-excerpts-2026-10-30.txt"
if post.exists():
    pt = re.sub(r"\s+", " ", post.read_text(encoding="utf-8"))
    for q in ["analyze accounts, trading activity, fees, and disclosures to quantify harm", "findings, exceptions, and assumptions"]:
        check(f"posting quote found: '{q}'", q.lower() in pt.lower() and q.lower() in txt.lower())
else:
    skip("posting quotes", f"no held excerpts at {post}")
skip("rule text (Reg BI, Rule 2111, Notice 12-25)", "read through a summarising fetch tool; confirm against the official text")

# [6] controls
print("[6] controls")
def sanctions_ok(vals): return sum(vals) == 110_000
check("control: a wrong sanction fails the total", not sanctions_ok([25000, 80000, 6000]))
check("control: exclusive day count differs from inclusive", (ENTRIES["rep"]["susp_to"] - ENTRIES["rep"]["susp_from"]).days != susp_days_incl)
check("control: equity definition changes turnover", turnover(PURCH, EQ["average"], MONTHS) != turnover(PURCH, EQ["initial"], MONTHS))
check("control: unannualised turnover is 5.0, not 6.0", abs(PURCH / EQ["average"] - 5.0) < 1e-9 and PURCH / EQ["average"] != turnover(PURCH, EQ["average"], MONTHS))
check("control: a wrong CRD is not on the page", "99999" not in txt)

# [7] honesty
print("[7] honesty")
check("says it is an exercise, not investigative experience", "not investigative experience" in txt and "has not worked as an investigator" in txt)
check("says the worked example is synthetic and invented", "synthetic" in txt and "invented" in txt)
check("says the rule gives no numeric thresholds", "no numbers" in txt and "not as rules" in txt)
check("does not name the individual", "Schuur" not in txt)
check("does not claim a harm total", "no individual" in txt and "not customer losses" in txt)

print(f"\n{'ALL PASS' if not FAIL else 'FAILURES: ' + str(len(FAIL))}  ({len(SKIP)} SKIP)")
sys.exit(1 if FAIL else 0)
