#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book26/ch12-verify.py -- book26/ch12-from-problem-to-plan.html (Template B, as chapters 10 to 19): the Sanar
Wellness Institute's Forms 990 for 2021, 2022 and 2024 (with 2023 from the 2024 return's prior-year columns),
read as problems found, analysis, recommendations, actions and follow-through for the Operations Specialist posting.
  [1] Template B structure (hero, section nav, sections in order, Sources footer), required labels, no network/storage/form code
  [2] the returns reconcile under their own arithmetic: revenue less expenses, assets less liabilities, net assets
      carried forward, balance-sheet lines adding to total assets and liabilities, Part I line 15 against Part IX,
      and the 2024 Part IX columns against their printed totals
  [3] the three tables on the page, cell by cell
  [4] every figure quoted in prose, and the stat panels, equal their computed values
  [5] every comparative claim, computed
  [6] SOURCE: each typed figure found on the labelled line of its page's OCR text (the returns are image-only
      scans), and each posting quote found in the held copy of the posting; prints SKIP, never PASS, when the
      OCR text or the held copy is absent
  [7] controls   [HONESTY]
Files looked for in $SANAR_DIR, else ~/Desktop/grants/sanar: ocr/<year>-p<NN>.txt (tesseract 300 dpi, --psm 6, of
990-<year>-irs.pdf) and posting-2026-10-28.txt. Figures are dollars.
"""
import os, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
PAGE = HERE / "ch12-from-problem-to-plan.html"
FAIL, SKIP = [], []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def skip(label, why): print(f"SKIP {label}  -- {why}"); SKIP.append(label)
def plain(t):
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", t, flags=re.S); t = re.sub(r"<[^>]+>", " ", t)
    for a, b in (("&rsquo;", "'"), ("&lsquo;", "'"), ("&ldquo;", '"'), ("&rdquo;", '"'), ("&amp;", "&"), ("&mdash;", "-"),
                 ("&ndash;", "-"), ("&middot;", "."), ("&nbsp;", " "), ("&minus;", "-"), ("&rarr;", "->")):
        t = t.replace(a, b)
    return re.sub(r"\s+", " ", t)

# ---- typed from the page images of the returns, 28 October 2026 ---------------------------------------------
YEARS = [2021, 2022, 2023, 2024]
REVENUE  = {2021: 954698, 2022: 771448, 2023: 973599, 2024: 1127926}
EXPENSES = {2021: 761486, 2022: 766039, 2023: 1019590, 2024: 1054626}
PAY      = {2021: 550924, 2022: 592980, 2023: 820358, 2024: 888773}
PRIOR_PAY_2021, PRIOR_REV_2021, PRIOR_EXP_2021 = 448540, 643523, 578137          # 2021 return, prior-year column (2020)
GOV      = {2021: 562538, 2022: 492281, 2024: 840082}
EMPLOYEES = {2021: 6, 2022: 11, 2024: 12}
PROGRAM_REV = {2021: 163111, 2022: 109317, 2023: 215511, 2024: 169744}
AR       = {2021: 78598, 2022: 102936, 2023: 161941, 2024: 202662}
CASH     = {2021: 246290, 2022: 232085, 2023: 51409, 2024: 139297}
SAVINGS  = {2021: 0, 2022: 0, 2023: 78558, 2024: 132986}
ASSETS   = {2020: 241988, 2021: 413742, 2022: 382554, 2023: 298655, 2024: 569412}
LIAB     = {2020: 110062, 2021: 88604, 2022: 52007, 2023: 14099, 2024: 211556}
NET      = {2021: 325138, 2022: 330547, 2023: 284556, 2024: 357856}                # Part X line 32
SURPLUS  = {2021: 193212, 2022: 5409, 2024: 73300}                                 # Part XI line 3
OTHER_ASSET_LINES = {2021: [83596, 5258], 2022: [45189, 2344], 2023: [3217, 3530], 2024: [89235, 5232]}  # PP&E, prepaid, other
LIAB_LINES = {2021: [6250, 82354], 2022: [7641, 44366], 2023: [14099], 2024: [3423, 118000, 90133]}
DEFERRED_2024 = 118000
BASIS = {2021: "Cash", 2022: "Accrual", 2024: "Accrual"}
AUDITED = {2021: "No", 2022: "Yes", 2024: "Yes"}
SINGLE_AUDIT = {2021: "No", 2022: "No", 2024: "No"}
COMMITTEE = {2022: "No", 2024: "No"}
PART9 = [("5", 208000, 208000, 0), ("7", 533767, 517471, 16296), ("9", 147006, 142772, 4234), ("11g", 21319, 20676, 643),
         ("13", 30385, 29723, 662), ("17", 17968, 17955, 13), ("20", 7016, 7016, 0), ("22", 40474, 40474, 0),
         ("23", 8010, 7167, 843), ("24a", 25396, 25396, 0), ("24b", 15285, 15285, 0)]
PART9_TOTAL = (1054626, 1031935, 22691, 0)
PP_REVENUE = {2015: 192735, 2025: 1275645}; PP_PROGRAM_2025 = 153439                 # ProPublica, secondary
OVC = [(2021, 600000), (2024, 800000)]; SA_OLD, SA_NEW = 750000, 1000000           # not held here
POSTING_QUOTES = ["see the 'big picture' of organizational operations to identify opportunities",
                  "Prepare financial statements and reporting monthly, federal/state grant financial reports and drawdowns",
                  "Prepare necessary paperwork for audits and grant reimbursement processes",
                  "Record day-to-day financial transactions in Quickbooks Online and pull regular reports for oversight",
                  "Coordinate employee payroll and grant payroll reconciliation using Sanar's contracted Kronos payroll system",
                  "Record necessary information into Salesforce records for grant reporting",
                  "Reporting to the Co-Chief Executive Officer", "Start Date: January 4, 2027", "Application Deadline: November 10, 2026",
                  "Salary: USD $60,000 / year", "Spanish speakers receive an additional $1,500", "People Administration (30%)",
                  "Bookkeeping and Finance Responsibilities (40%)", "Office Management and Program Support (20%)",
                  "Spanish, Portuguese, or Haitian Creole fluency", "including rent", "technology support", "Prestige"]
AUTHOR_WORDS = "Observation to diagnostics, diagnostics to uncover gaps, then use those gaps to derive solutions: I want to solve the same problems in my own work, with the tools that I have."

def D(x): return f"{x:,}"
def pc(a, b, n=1): return f"{a / b * 100:.{n}f}"
cash = {y: CASH[y] + SAVINGS[y] for y in YEARS}
months = {y: cash[y] / (EXPENSES[y] / 12) for y in YEARS}
arp = {y: AR[y] / REVENUE[y] * 100 for y in YEARS}
ard = {y: AR[y] / REVENUE[y] * 365 for y in YEARS}
payp = {y: PAY[y] / EXPENSES[y] * 100 for y in YEARS}
T, PG, MG, FR = PART9_TOTAL
ill = REVENUE[2024] * AR[2021] / REVENUE[2021]; freed = AR[2024] - ill

SECS = ["posting", "problems", "analysis", "recommendations", "actions", "followthrough", "limits", "updates", "checked"]
LABELS = ["not a statement by the institute", "the author's arithmetic", "the author's proposals, not the institute's plans",
          "this is a question, not a finding", "a question about classification, not an error", "not checked:",
          "secondary extraction", "were not checked against returns", "as an illustration only", "not a forecast",
          "the strongest opposing case", "that the author has run federal grant drawdowns", "the application does not claim it",
          "the 2023 return itself was not read", "read from the page image only", "cannot be read from the return",
          "nothing here shows that any figure is wrong", "is the co-ceos' decision", "does not claim the latter", "a measure that does not move is a finding too", "not visible from the returns"]
FORBIDDEN = ["fetch(", "XMLHttpRequest", "localStorage", "<form", "action="]
def secs_ok(t): return re.findall(r'<section id="([^"]+)">', t) == SECS
def template_ok(t):
    return all(k in t for k in ("Template B", '<header class="hero">', '<nav class="pillars"', '<footer id="sources">', '<div class="chapnav">', "family=Cinzel"))
def labels_ok(t): p = plain(t).lower(); return all(l in p for l in LABELS)
def safe_ok(t): return not any(f in t for f in FORBIDDEN)
def tables(t):
    out = []
    for tb in re.findall(r"<table>(.*?)</table>", t, re.S):
        rows = []
        for tr in re.findall(r"<tr>(.*?)</tr>", tb, re.S)[1:]:
            rows.append([plain(c).strip() for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)])
        out.append(rows)
    return out
DASH = "-"
def exp_t1():
    return [[str(y), D(REVENUE[y]), D(GOV[y]) if y in GOV else DASH, pc(GOV[y], REVENUE[y]) if y in GOV else DASH,
             str(EMPLOYEES[y]) if y in EMPLOYEES else DASH, f"{payp[y]:.1f}", D(AR[y]), D(cash[y]), BASIS.get(y, DASH), AUDITED.get(y, DASH)] for y in YEARS]
def exp_t2(): return [[str(y), f"{arp[y]:.1f}", f"{ard[y]:.0f}", f"{months[y]:.1f}"] for y in YEARS]
def exp_t3(): return [[l, D(a), D(b), D(c)] for l, a, b, c in PART9] + [["25", D(T), D(PG), D(MG)]]
def t3_cells(rows): return [[r[0]] + r[2:] for r in rows]
def exp_t5(): return [[f"{ard[2024]:.0f} days at the end of 2024"], [f"{months[2024]:.1f} months at the end of 2024"], [f"{pc(MG, T)} percent in 2024"]]
def tables_ok(t):
    tb = tables(t)
    fu = [[r[1]] for r in tb[4] if r[1] != "Not visible from the returns"] if len(tb) >= 5 else []
    return len(tb) >= 5 and tb[0] == exp_t1() and tb[1] == exp_t2() and t3_cells(tb[2]) == exp_t3() and fu == exp_t5()

def prose_expected():
    return {
      "posting salary and dates": "at $60,000 a year, with applications due 10 November 2026 and a start date of 4 January 2027",
      "posting split": "People Administration (30%), Bookkeeping and Finance Responsibilities (40%), Office Management and Program Support (20%)",
      "stipend": "the details line puts it at $1,500 for Spanish speakers",
      "posting quote: drawdowns": '"Prepare financial statements and reporting monthly, federal/state grant financial reports and drawdowns."',
      "posting quote: big picture": "\"see the 'big picture' of organizational operations to identify opportunities.\"",
      "author's words": AUTHOR_WORDS,
      "revenue 2021 and 2024": f"Revenue was ${D(REVENUE[2021])} in 2021 and ${D(REVENUE[2024])} in 2024",
      "grants by year": f"were ${D(GOV[2021])} in 2021, ${D(GOV[2022])} in 2022 and ${D(GOV[2024])} in 2024",
      "training fees": f"which were ${D(PROGRAM_REV[2023])} in 2023 and ${D(PROGRAM_REV[2024])} in 2024",
      "ProPublica span": f"${D(PP_REVENUE[2015])} in 2015, the first year after exemption, and ${D(PP_REVENUE[2025])} in 2025, about {PP_REVENUE[2025] / PP_REVENUE[2015]:.1f} times as much",
      "receivables growth": f"from ${D(AR[2021])} at the end of 2021 to ${D(AR[2024])} at the end of 2024, {AR[2024] / AR[2021]:.2f} times as much, while annual revenue grew {REVENUE[2024] / REVENUE[2021]:.2f} times",
      "receivables shares": ", ".join(f"{arp[y]:.1f}" for y in YEARS[:-1]) + f" and {arp[2024]:.1f} percent",
      "months 2021/22/24": f"{months[2021]:.1f} months of that year's expenses at the end of 2021, {months[2022]:.1f} at the end of 2022 and {months[2024]:.1f} at the end of 2024",
      "months 2023": f"they covered {months[2023]:.1f}",
      "deferred revenue": f"${D(DEFERRED_2024)} of deferred revenue",
      "Part IX split": f"puts ${D(PG)} of ${D(T)} in program services, {pc(PG, T)} percent, and ${D(MG)} in management and general, {pc(MG, T)} percent",
      "line 15 agreement": f"Salaries, officers' pay and benefits are ${D(208000 + 533767 + 147006)}, which agrees with Part I line 15",
      "zero lines": "payroll taxes (line 10), accounting (line 11c), information technology (line 14) and occupancy (line 16)",
      "thresholds": f"${D(SA_OLD)} of federal awards spent in a fiscal year beginning before 1 October 2024, and ${D(SA_NEW)} for fiscal years beginning on or after that date",
      "2024 grants vs threshold": f"so the ${D(SA_OLD)} threshold applied, and 2024 government grants were ${D(GOV[2024])}",
      "OVC awards": f"${D(OVC[0][1])} in fiscal year {OVC[0][0]} and ${D(OVC[1][1])} in fiscal year {OVC[1][0]}",
      "problem: receivables": f"They rose from {arp[2021]:.1f} to {arp[2024]:.1f} percent of the year's revenue",
      "problem: M&G": f"{pc(MG, T)} percent management and general, with zero on payroll taxes",
      "rec: pay": f"salaries and benefits are {payp[2024]:.1f} percent of expenses",
      "problem: buffer": f"Between {min(months.values()):.1f} and {max(months.values()):.1f} months of expenses at year end",
      "concentration": f"Government grants rose from {pc(GOV[2021], REVENUE[2021])} to {pc(GOV[2024], REVENUE[2024])} percent of revenue, while training fees fell from ${D(PROGRAM_REV[2023])} in 2023 to ${D(PROGRAM_REV[2024])} in 2024, and to ${D(PP_PROGRAM_2025)} in 2025",
      "plan threshold": f"against the ${D(SA_NEW)} single-audit threshold that applies from the 2025 fiscal year",
      "follow-through start": f"{ard[2024]:.0f} days at the end of 2024",
      "follow-through months": f"{months[2024]:.1f} months at the end of 2024",
      "illustration": f"about ${ill / 1e3:,.0f} thousand instead of ${D(AR[2024])}. The difference, about ${freed / 1e3:,.0f} thousand, is {freed / (EXPENSES[2024] / 12):.1f} months of 2024 expenses",
      "author aside": "usually about $100,000 a month or less, and hired its two other local managers",
    }
def prose_ok(t): p = plain(t); return all(v in p for v in prose_expected().values())
def stats_expected():
    return [f"${REVENUE[2024]/1e6:.2f}M", f"up {pc(REVENUE[2024] - REVENUE[2021], REVENUE[2021], 0)}% from 2021",
            f"{pc(GOV[2024], REVENUE[2024])}% of 2024 revenue", f"against {pc(GOV[2021], REVENUE[2021])}% in 2021",
            f"{EMPLOYEES[2021]} -> {EMPLOYEES[2024]}", f"{payp[2024]:.1f}%", f"{ard[2021]:.0f} -> {ard[2024]:.0f}",
            f"{months[2023]:.1f} months", f"{pc(MG, T)}% of 2024 expenses", "3 of 3"]
def stats_ok(t):
    blocks = " ".join(plain(b) for b in re.findall(r'<div class="stats">(.*?)</div>\s*</div>', t, re.S))
    return all(v in blocks for v in stats_expected())
def claims():
    return {"receivables rose as a share of revenue every year": all(arp[a] < arp[b] for a, b in zip(YEARS, YEARS[1:])),
            "receivables grew faster than revenue, 2021 to 2024": AR[2024] / AR[2021] > REVENUE[2024] / REVENUE[2021],
            "2023 is the cash low point": months[2023] == min(months.values()),
            "2023 expenses exceeded revenue": EXPENSES[2023] > REVENUE[2023],
            "cash covered about three months in the other years (3.0 to 4.0)": all(3 <= months[y] < 4 for y in (2021, 2022, 2024)),
            "government share rose 2021 to 2024": GOV[2024] / REVENUE[2024] > GOV[2022] / REVENUE[2022] > GOV[2021] / REVENUE[2021],
            "2024 government grants exceed the $750,000 threshold": GOV[2024] > SA_OLD,
            "all three returns answer No on line 3a": all(v == "No" for v in SINGLE_AUDIT.values()),
            "training fees fell 2023 to 2024 and again in 2025": PROGRAM_REV[2023] > PROGRAM_REV[2024] > PP_PROGRAM_2025,
            "pay share rose every year": all(payp[a] < payp[b] for a, b in zip(YEARS, YEARS[1:])),
            "M&G under 3 percent, fundraising nil": MG / T < 0.03 and FR == 0,
            "employees grew 6 to 12": (EMPLOYEES[2021], EMPLOYEES[2024]) == (6, 12),
            "the 2021 return was the cash-basis, unaudited one": BASIS[2021] == "Cash" and AUDITED[2021] == "No" and all(BASIS[y] == "Accrual" and AUDITED[y] == "Yes" for y in (2022, 2024))}

# ---- [6] source -----------------------------------------------------------------------------------------
def base():
    for d in (os.environ.get("SANAR_DIR", ""), "~/Desktop/grants/sanar"):
        if d and (Path(d).expanduser() / "ocr" / "2024-p01.txt").exists(): return Path(d).expanduser()
def nums(line): return [int(n.replace(",", "")) for n in re.findall(r"\d{1,3}(?:,\d{3})+|\d{4,}", line)]
def line(txt, label, n=1):
    for l in txt.splitlines():
        if re.search(label, l, re.I) and len(nums(l)) >= n: return nums(l)
    return []
def after(txt, label):
    L = txt.splitlines(); k = next((i for i, l in enumerate(L) if re.search(label, l, re.I)), None)
    return " ".join(L[k:k + 2]) if k is not None else ""
def source_checks(d, gov=None):
    gov = gov or GOV; r = {}
    rd = lambda y, p: (d / "ocr" / f"{y}-p{p:02d}.txt").read_text(errors="replace") if (d / "ocr" / f"{y}-p{p:02d}.txt").exists() else ""
    prior = {2021: (PRIOR_REV_2021, PRIOR_EXP_2021, PRIOR_PAY_2021), 2022: (REVENUE[2021], EXPENSES[2021], PAY[2021]), 2024: (REVENUE[2023], EXPENSES[2023], PAY[2023])}
    for y in (2021, 2022, 2024):
        p1, p9, p11, p12 = rd(y, 1), rd(y, 9), rd(y, 11), rd(y, 12)
        pr, pe, pp = prior[y]
        r[f"{y} p.1 line 12 revenue, prior and current"] = line(p1, r"Total revenue.add lines 8")[-2:] == [pr, REVENUE[y]]
        r[f"{y} p.1 line 18 expenses, prior and current"] = line(p1, r"Total expenses\. Add lines 13")[-2:] == [pe, EXPENSES[y]]
        r[f"{y} p.1 line 15 pay, prior and current"] = line(p1, r"Salaries, other compensation")[-2:] == [pp, PAY[y]]
        r[f"{y} p.1 line 9 program service revenue (current)"] = line(p1, r"Program service revenue")[-1:] == [PROGRAM_REV[y]]
        m = re.search(r"individuals employed.*?(\d+)\s*$", next((l for l in p1.splitlines() if "individuals employed" in l), ""))
        r[f"{y} p.1 line 5 employees"] = bool(m) and int(m.group(1)) == EMPLOYEES[y]
        r[f"{y} p.9 line 1e government grants"] = line(p9, r"Government grants")[-1:] == [gov[y]]
        r[f"{y} p.11 line 4 receivables, end of year"] = line(p11, r"Accounts receivable, net")[-1:] == [AR[y]]
        r[f"{y} p.11 line 1 cash, end of year"] = line(p11, r"Cash-non-interest")[-1:] == [CASH[y]]
        r[f"{y} p.11 line 16 total assets, begin and end"] = line(p11, r"Total assets\. Add lines")[-2:] == [ASSETS[y - 1], ASSETS[y]]
        r[f"{y} p.11 line 26 total liabilities, begin and end"] = line(p11, r"Total liabilities\. Add lines")[-2:] == [LIAB[y - 1], LIAB[y]]
        r[f"{y} p.12 Part XI totals"] = line(p12, r"^\s*1 Total revenue")[-1:] == [REVENUE[y]] and line(p12, r"^\s*2 Total expenses")[-1:] == [EXPENSES[y]]
        r[f"{y} p.12 line 2b audited: {AUDITED[y]}"] = re.search(r"audited by an independent accountant\?.*\b" + AUDITED[y] + r"\b", p12) is not None
        r[f"{y} p.12 line 3a single audit: {SINGLE_AUDIT[y]}"] = re.search(r"\b" + SINGLE_AUDIT[y] + r"\b", after(p12, r"^3a As a result of a federal award")) is not None
        if y in COMMITTEE: r[f"{y} p.12 line 2c committee: No"] = re.search(r"\bNo\b", after(p12, r"^c If .Yes,. to line 2a or 2b")) is not None
        if y in (2022, 2024): r[f"{y} p.12 line 1 accrual box marked"] = re.search(r"cash M Accrual", p12) is not None
    p11 = rd(2024, 11); p10 = rd(2024, 10)
    r["2024 p.11 line 2 savings, begin and end"] = line(p11, r"Savings and temporary")[-2:] == [SAVINGS[2023], SAVINGS[2024]]
    r["2024 p.11 line 4 receivables, begin"] = line(p11, r"Accounts receivable, net")[-2:] == [AR[2023], AR[2024]]
    r["2024 p.11 line 1 cash, begin"] = line(p11, r"Cash-non-interest")[-2:] == [CASH[2023], CASH[2024]]
    r["2024 p.11 line 19 deferred revenue"] = line(p11, r"Deferred ?revenue")[-1:] == [DEFERRED_2024]
    r["2024 p.11 line 32 net assets, begin and end"] = line(p11, r"Total ?net ?assets ?or ?fund")[-2:] == [NET[2023], NET[2024]]
    r["2024 p.10 line 5 officers (total, program)"] = line(p10, r"^5 Compensation of current officers")[-2:] == [208000, 208000]
    r["2024 p.10 line 11g other fees (three columns)"] = re.search(r"Other \(If line 11g.*\b21,319 20,676 643\b", p10) is not None
    return r
def posting_checks(d):
    f = d / "posting-2026-10-28.txt"
    if not f.exists(): return None
    txt = re.sub(r"\s+", " ", f.read_text(errors="replace")).replace("’", "'")
    return {f"posting: {q[:60]}": q in txt for q in POSTING_QUOTES}

def main():
    t = PAGE.read_text(encoding="utf-8") if PAGE.exists() else ""
    check("page exists", bool(t))
    if not t: print("\nFAILED: page absent"); sys.exit(1)
    print("[1] structure"); check("Template B: hero, section nav, Sources footer, chapter nav, Cinzel/Garamond", template_ok(t))
    check("sections in order: " + ", ".join(SECS), secs_ok(t)); check("required labels present", labels_ok(t)); check("no network, storage or form code", safe_ok(t))
    print("[2] the returns reconcile under their own arithmetic")
    for y in SURPLUS: check(f"{y}: revenue less expenses = Part XI line 3", REVENUE[y] - EXPENSES[y] == SURPLUS[y])
    for y in YEARS: check(f"{y}: assets less liabilities = net assets", ASSETS[y] - LIAB[y] == NET[y])
    for y in (2022, 2024): check(f"{y}: net assets carried forward plus the year's result", NET[y - 1] + SURPLUS[y] == NET[y])
    for y in YEARS: check(f"{y}: balance-sheet lines add to total assets", CASH[y] + SAVINGS[y] + AR[y] + sum(OTHER_ASSET_LINES[y]) == ASSETS[y])
    for y in YEARS: check(f"{y}: liability lines add to total liabilities", sum(LIAB_LINES[y]) == LIAB[y])
    check("2024 Part IX: total column adds to line 25", sum(a for _, a, _, _ in PART9) == T)
    check("2024 Part IX: program column adds to line 25", sum(b for _, _, b, _ in PART9) == PG)
    check("2024 Part IX: management column adds to line 25", sum(c for *_, c in PART9) == MG)
    check("2024 Part IX: each line's columns add to its total", all(a == b + c for _, a, b, c in PART9))
    check("2024 Part IX: program + management + fundraising = total", PG + MG + FR == T)
    check("2024 Part IX line 25 = Part I line 18", T == EXPENSES[2024])
    check("2024 Part IX lines 5 + 7 + 9 = Part I line 15", PART9[0][1] + PART9[1][1] + PART9[2][1] == PAY[2024])
    print("[3] tables, cell by cell"); check("observation, cash, Part IX and follow-through tables equal computed values", tables_ok(t), "40 + 16 + 48 + 3 cells")
    print("[4] figures quoted in prose"); p = plain(t)
    for k, v in prose_expected().items(): check(f"prose: {k}", v in p, v[:90])
    check("stat panels equal computed values", stats_ok(t), f"{len(stats_expected())} figures")
    print("[5] comparative claims"); [check(k, ok) for k, ok in claims().items()]
    print("UNCHECKED  OVC awards ($600,000 FY2021, $800,000 FY2024): read once through an automated reader, no held copy")
    print("UNCHECKED  single-audit thresholds ($750,000 / $1,000,000): Federal Audit Clearinghouse help page, not the regulation")
    print("UNCHECKED  ProPublica secondary figures (2015 and 2025 revenue, 2025 training fees)")
    print("UNCHECKED  author aside (branch operating-cost lines, hiring, school director): the author's own record, no document")
    print("[6] SOURCE")
    d = base()
    if not d: skip("source checks", "ocr/2024-p01.txt not found in $SANAR_DIR or ~/Desktop/grants/sanar")
    else:
        for k, ok in source_checks(d).items(): check(k, ok)
        pc_ = posting_checks(d)
        if pc_ is None: skip("posting quotes", "posting-2026-10-28.txt not found")
        else: [check(k, ok) for k, ok in pc_.items()]
        skip("2024 Part IX lines other than 5 and 11g", "OCR lost the columns; checked in [2] by their printed column totals")
        skip("2021 Part XII line 1 cash box", "OCR does not read the box; read from the page image")
    print("[7] controls"); ctl = []
    def control(name, damaged, fn):
        ok = fn(damaged); print(("PASS " if not ok else "FAIL ") + "control rejected: " + name)
        if ok: ctl.append(name)
    control("section removed", t.replace('<section id="recommendations">', '<section id="x">'), secs_ok)
    control("chapter 1-9 layout swapped in", t.replace('<header class="hero">', '<div class="wp-head">'), template_ok)
    control("stat panel figure changed", t.replace(">3 of 3<", ">2 of 3<"), stats_ok)
    control("label removed", t.replace("This is a question, not a finding", "This is a finding"), labels_ok)
    control("observation table cell changed", t.replace(">202,662<", ">206,262<", 1), tables_ok)
    control("Part IX cells swapped (lines 13 and 17 program)", t.replace(">29,723<", ">TMP<").replace(">17,955<", ">29,723<").replace(">TMP<", ">17,955<"), tables_ok)
    control("prose figure changed", t.replace("$840,082", "$804,082"), prose_ok)
    control("form code pasted in", t + " <form ", safe_ok)
    if d:
        bad = source_checks(d, {**GOV, 2024: 840028})["2024 p.9 line 1e government grants"]
        print(("PASS " if not bad else "FAIL ") + "control rejected: 2024 government grants typed with two digits swapped")
        if bad: ctl.append("typed figure")
    print("[HONESTY] Blocks 2 to 5 show that the figures typed into this script reconcile under each return's own arithmetic, "
          "that the page prints exactly those figures in the right cells, and that each comparative sentence holds for them. "
          "Block 6 finds each typed figure on the labelled line of its page's OCR text; the returns are scanned images, "
          "so OCR is a second reading of the same page, not an independent source. It prints SKIP where the OCR text or "
          "the held posting is absent, which is not a pass.")
    print("[HONESTY] Nothing here shows how much of the government money is federal, which grants the receivables "
          "belong to, what the audited statements or Schedule O say, or anything after 31 December 2024. The analysis "
          "is the author's reading of the returns, and the recommendations, actions and follow-through are his proposals, not the Institute's.")
    if FAIL or ctl: print(f"\nFAILED: {len(FAIL)} check(s), {len(ctl)} control(s) not rejected"); sys.exit(1)
    print("\nALL PASS" + (f" ({len(SKIP)} skipped: not a pass)" if SKIP else ""))
main()
