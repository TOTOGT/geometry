#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book26/ch11-verify.py -- book26/ch11-the-books-they-manage.html: the NYSIF bond book from its own public documents.
  [1] sections S1..S6 in order   [2] labels present   [3] no network, storage or form code
  [4] the report's bond table reconciles from its own columns: book + gross gains + gross losses = market,
      per category and total, and the categories add to the totals; the maturity table adds to the same totals
  [5] the S2 table, cell by cell, equals the values computed from the report's figures
  [6] every figure quoted in prose equals its computed value
  [7] SOURCE: each typed figure re-read from the PDF page the chapter cites (needs pdftotext and the PDFs;
      prints SKIP, never PASS, when either is missing)
  [8] controls   [HONESTY]
Primary sources: NYSIF 2023 Annual Report (Workers' Compensation Fund statements: balance sheet p. 4,
Note 3 pp. 24-26); Investment Policy Statement as amended 18 November 2020; Board minutes 30 October 2025.
Figures are $ thousands. PDFs are looked for in $NYSIF_PDF_DIR, ~/Downloads and ~/Desktop/grants/nysif.
"""
import os, re, shutil, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
PAGE = HERE / "ch11-the-books-they-manage.html"
FAIL, SKIP = [], []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def skip(label, why):
    print(f"SKIP {label}  -- {why}"); SKIP.append(label)
def plain(t):
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    for a, b in (("&rsquo;", "'"), ("&ldquo;", '"'), ("&rdquo;", '"'), ("&amp;", "&"), ("&mdash;", "-"), ("&ndash;", "-"),
                 ("&middot;", "."), ("&nbsp;", " "), ("&minus;", "-"), ("&eacute;", "e")):
        t = t.replace(a, b)
    return re.sub(r"\s+", " ", t)

# ---- typed from the 2023 report, re-read against the PDF on 2026-10-28 -------------------------------
# Note 3 p. 24: category -> (book, gross gains, gross losses, market)
CAT = {"U.S. Government and government agency obligations": (5984174, 20827, -852445, 5152556),
       "States, territories, possessions and political subdivisions": (1343430, 4289, -188133, 1159586),
       "Corporate bonds and public utilities": (9237910, 75259, -499106, 8814063),
       "Mortgage-backed securities": (1911385, 6534, -52635, 1865284)}
TOTAL = (18476899, 106909, -1592319, 16991489)
MATURITY = {"Due in one year or less": (603861, 598738), "Due after one year through five years": (7597711, 7282560),
            "Due after five years through ten years": (2260634, 2122875), "Due after ten years": (8014693, 6987316)}
BS = {"Bonds": 18476899, "Common stocks": 1827205, "Cash, cash equivalents and short-term investments": 462690,
      "Total cash and invested assets": 21025079}                       # balance sheet p. 4
ON_LOAN, COLLATERAL = 238377, 250359                                   # p. 25
REALIZED_BONDS = -85325                                                # p. 26, net realized gains (losses) and impairments
RESERVE_DISCOUNT = 5                                                   # p. 9, percent, mandated by the Workers' Compensation Law
CITED = {"bond table": 24, "maturity table": 24, "securities lending": 25, "balance sheet": 4, "realized": 26, "reserve discount": 9}

def m(x): return f"{x/1000:,.1f}"
def sgn(x): return ("-" if x < 0 else "") + f"{abs(x)/1000:,.1f}"
def pct(a, b): return f"{a/b*100:.1f}"
def net(r): return r[1] + r[2]

def expected_rows():
    rows = []
    for k, r in CAT.items():
        rows.append([m(r[0]), m(r[3]), sgn(net(r)), sgn(net(r) / r[0] * 100 * 1000)])
    rows.append([m(TOTAL[0]), m(TOTAL[3]), sgn(net(TOTAL)), sgn(net(TOTAL) / TOTAL[0] * 100 * 1000)])
    return rows
def page_rows(t):
    tbl = re.search(r"<table>(.*?)</table>", t, re.S)
    if not tbl: return []
    out = []
    for tr in re.findall(r"<tr>(.*?)</tr>", tbl.group(1), re.S)[1:]:
        cells = [plain(c).strip().replace(" ", "") for c in re.findall(r'<td class="num">(.*?)</td>', tr, re.S)]
        out.append(cells)
    return out
def table_ok(t): return page_rows(t) == expected_rows()

def prose_expected():
    B, MK = TOTAL[0], TOTAL[3]; gap = B - MK
    long_gap = MATURITY["Due after ten years"][0] - MATURITY["Due after ten years"][1]
    short = MATURITY["Due in one year or less"]
    corp = CAT["Corporate bonds and public utilities"]; govt = CAT["U.S. Government and government agency obligations"]
    return {
        "$21.0 billion of cash and invested assets": f"${BS['Total cash and invested assets']/1e6:.1f} billion of cash and invested assets",
        "bonds $18.48 billion": f"${B/1e6:.2f} billion",
        "bonds 87.9 percent": f"{pct(B, BS['Total cash and invested assets'])} percent",
        "stocks $1.83 billion": f"${BS['Common stocks']/1e6:.2f} billion",
        "stocks 8.7 percent": f"({pct(BS['Common stocks'], BS['Total cash and invested assets'])} percent)",
        "cash $463 million": f"${BS['Cash, cash equivalents and short-term investments']/1e3:.0f} million",
        "cash 2.2 percent": f"({pct(BS['Cash, cash equivalents and short-term investments'], BS['Total cash and invested assets'])} percent)",
        "on loan $238.4 million": f"${ON_LOAN/1e3:.1f} million",
        "collateral $250.4 million": f"${COLLATERAL/1e3:.1f} million of collateral",
        "gap $1.49 billion": f"${gap/1e6:.2f} billion below its cost",
        "gap about 8 percent": f"about {gap/B*100:.0f} percent",
        "govt about 14 percent": f"about {-net(govt)/govt[0]*100:.0f} percent of book",
        "corporates about 4.6 percent": f"about {-net(corp)/corp[0]*100:.1f} percent",
        "long end $1.03 billion": f"${long_gap/1e6:.2f} billion below cost",
        "long end 69 percent": f"{long_gap/gap*100:.0f} percent of the whole gap",
        "realized $85.3 million": f"${-REALIZED_BONDS/1e3:.1f} million of net realized losses",
        "reserves discounted at 5 percent": f"{RESERVE_DISCOUNT} percent at which state law makes the Fund discount its claim reserves",
    }
def prose_ok(t):
    p = plain(t); return all(v in p for v in prose_expected().values())
def logic_claims():
    gap = TOTAL[0] - TOTAL[3]; corp = CAT["Corporate bonds and public utilities"]; s = MATURITY["Due in one year or less"]
    return {"corporates hold less than a third of the gap": -net(corp) / gap < 1/3,
            "bonds due within a year are within 1 percent of cost": (s[0] - s[1]) / s[0] < 0.01,
            "corporates are about half the bond book": abs(corp[0] / TOTAL[0] - 0.5) < 0.005,
            "corporate book agrees with the posting's 'more than $9 billion'": corp[0] > 9_000_000}

SECS = ["S1", "S2", "S3", "S4", "S5", "S6"]
LABELS = ["not a statement by the fund", "author's arithmetic", "the author's proposals, not the fund's plans",
          "the monitor does not exist yet", "the policy has moved since", "re-read against the pdfs", "not checked:",
          "that the author meets the posting's experience requirement", "how much of that loss is credit is not measured here"]
FORBIDDEN = ["fetch(", "XMLHttpRequest", "localStorage", "<form", "action="]
def secs_ok(t): return re.findall(r'<div class="sec" data-n="([^"]+)">', t) == SECS
def labels_ok(t):
    p = plain(t).lower(); return all(l in p for l in LABELS)
def safe_ok(t): return not any(f in t for f in FORBIDDEN)

# ---- [7] source ---------------------------------------------------------------------------------------
def pdf_dir():
    for d in (os.environ.get("NYSIF_PDF_DIR", ""), "~/Downloads", "~/Desktop/grants/nysif"):
        if d and (Path(d).expanduser() / "AR2023.pdf").exists(): return Path(d).expanduser()
    return None
def pdftext(path):
    r = subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""
def wcf_page(pages, printed):
    """first page of the Workers' Compensation Fund statements whose footer is the printed page number"""
    for p in pages:
        lines = [l.strip() for l in p.splitlines() if l.strip()]
        if lines and re.fullmatch(rf"-\s*{printed}\s*-", lines[-1]) and "WORKERS' COMPENSATION FUND" in p.replace("’", "'"):
            return p
    return ""
NUM = re.compile(r"\(?[\d,]{4,}\)?")
def nums(line): return [(-1 if n.startswith("(") else 1) * int(n.strip("()").replace(",", "")) for n in NUM.findall(line)]
def row(page, label):
    for l in page.splitlines():
        if label.lower() in l.lower().replace("—", "-") and nums(l): return nums(l)
    return []
def source_checks(pages, ips, boc):
    res = {}
    p24, p25, p26, p4 = (wcf_page(pages, n) for n in (CITED["bond table"], CITED["securities lending"], CITED["realized"], CITED["balance sheet"]))
    res["p. 24 found"] = bool(p24) and "NOTE 3" in p24
    for k, v in CAT.items(): res[f"p. 24 {k[:30]}"] = row(p24, k)[:4] == list(v)
    res["p. 24 Total bonds"] = row(p24, "Total bonds")[:4] == list(TOTAL)
    for k, v in MATURITY.items(): res[f"p. 24 maturity: {k}"] = row(p24, k)[:2] == list(v)
    res["p. 24 maturity columns read Amortized Cost, then Market Value"] = bool(re.search(r"Amortized\s+Market", p24)) and bool(re.search(r"Cost\s+Value", p24))
    res["p. 25 on loan and collateral"] = f"${ON_LOAN:,}" in p25 and f"${COLLATERAL:,}" in re.sub(r"\s+", " ", p25)
    res["p. 26 realized bonds"] = any(nums(l)[:1] == [REALIZED_BONDS] for l in p26.splitlines() if l.strip().startswith("Bonds"))
    res["p. 4 balance sheet"] = (row(p4, "Bonds-at NAIC carrying value")[:1] == [BS["Bonds"]] and row(p4, "Common stocks")[:1] == [BS["Common stocks"]]
                                 and row(p4, "Cash, cash equivalents and short-term investments")[:1] == [BS["Cash, cash equivalents and short-term investments"]]
                                 and row(p4, "Total cash and invested assets")[:1] == [BS["Total cash and invested assets"]])
    p9 = re.sub(r"\s+", " ", wcf_page(pages, CITED["reserve discount"]))
    res["p. 9 reserves discounted at 5% by law"] = f"discounts all loss and loss adjustment expense reserves at {RESERVE_DISCOUNT}%" in p9
    w = re.sub(r"\s+", " ", ips)
    for s in ["As amended by the Board of Commissioners on November 18, 2020", "Investment Grade Fixed 78% 85% 100% NYSIF Custom Benchmark",
              "High Yield 0% 4% 7%", "Public Equities 0% 5% 8%", "Alternatives 0% 4% 7%", "Cash 0% 2% 3% ICE BofAML 3-month T-Bill",
              "mid-single A/A2", "duration target of eight years +/- 1 year", "pay 75% of liabilities coming due in the next 365 days",
              "NYSIF may invest surplus funds in derivative instruments", "WCL § 87 (4) permits NYSIF to loan its securities"]:
        res[f"IPS: {s[:48]}"] = s in w
    b = re.sub(r"\s+", " ", boc)
    for s in ["dated December 18, 2024", "current market environment and risks", "review and adopt it once a year"]:
        res[f"minutes: {s}"] = s in b
    return res

def main():
    t = PAGE.read_text(encoding="utf-8") if PAGE.exists() else ""
    check("page exists", bool(t))
    if not t: print("\nFAILED: page absent"); sys.exit(1)
    print("[1-3] structure")
    check("sections S1..S6 in order", secs_ok(t))
    check("required labels present", labels_ok(t))
    check("no network, storage or form code", safe_ok(t))
    print("[4] the report's tables reconcile from their own columns")
    for k, r in CAT.items(): check(f"book + gains + losses = market: {k[:40]}", r[0] + r[1] + r[2] == r[3])
    check("book + gains + losses = market: Total bonds", TOTAL[0] + TOTAL[1] + TOTAL[2] == TOTAL[3])
    for i, name in enumerate(("book", "gross gains", "gross losses", "market")):
        check(f"categories add to the total ({name})", sum(r[i] for r in CAT.values()) == TOTAL[i])
    check("maturity table adds to the bond totals", (sum(a for a, _ in MATURITY.values()), sum(b for _, b in MATURITY.values())) == (TOTAL[0], TOTAL[3]))
    print("[5] the S2 table, cell by cell")
    check("table cells equal computed values, in position", table_ok(t), f"{sum(len(r) for r in expected_rows())} cells")
    print("[6] figures quoted in prose")
    p = plain(t)
    for k, v in prose_expected().items(): check(f"prose: {k}", v in p, v)
    for k, ok in logic_claims().items(): check(k, ok)
    print("UNCHECKED  posting figures in S1 ($179,150-$229,150; 27 Oct and 1 Dec 2026; more than $22 and $9 billion): the posting is not held here")
    print("[7] SOURCE: typed figures against the cited PDF pages")
    d = pdf_dir()
    if not shutil.which("pdftotext"): skip("source checks", "pdftotext not installed")
    elif not d: skip("source checks", "AR2023.pdf not found in $NYSIF_PDF_DIR, ~/Downloads or ~/Desktop/grants/nysif")
    else:
        pages = pdftext(d / "AR2023.pdf").split("\f")
        ips = pdftext(d / "IPS-2020.pdf") if (d / "IPS-2020.pdf").exists() else ""
        boc = pdftext(d / "BoC-2025-10-30.pdf") if (d / "BoC-2025-10-30.pdf").exists() else ""
        for k, ok in source_checks(pages, ips, boc).items():
            if (k.startswith("IPS") and not ips) or (k.startswith("minutes") and not boc): skip(k, "PDF not found")
            else: check(k, ok)
    print("[8] controls")
    ctl = []
    def control(name, damaged, fn):
        ok = fn(damaged); print(("PASS " if not ok else "FAIL ") + "control rejected: " + name)
        if ok: ctl.append(name)
    control("section removed", t.replace('data-n="S4"', 'data-n="X"'), secs_ok)
    control("label removed", re.sub(r"not a statement by the fund", "a statement", t, flags=re.I), labels_ok)
    control("corporate book value changed", t.replace("9,237.9", "9,337.9"), table_ok)
    control("two table cells swapped", t.replace("&minus;13.9", "TMP").replace("&minus;13.7", "&minus;13.9").replace("TMP", "&minus;13.7"), table_ok)
    control("prose figure changed", t.replace("$238.4 million", "$283.4 million"), prose_ok)
    control("form code pasted in", t + " <form ", safe_ok)
    if d and shutil.which("pdftotext"):
        pages = pdftext(d / "AR2023.pdf").split("\f")
        global CITED
        saved = dict(CITED); CITED["securities lending"] = 26
        bad = source_checks(pages, "", "")["p. 25 on loan and collateral"]; CITED = saved
        print(("PASS " if not bad else "FAIL ") + "control rejected: securities lending cited to p. 26 (the first version's citation)")
        if bad: ctl.append("wrong page")
        gone = source_checks([""], "", "")["p. 24 Total bonds"]
        print(("PASS " if not gone else "FAIL ") + "control rejected: empty PDF text")
        if gone: ctl.append("empty pdf")
    print("[HONESTY] Blocks 4 to 6 show that the figures typed into this script reconcile under the report's own "
          "arithmetic, and that the page prints exactly those figures in the right places. Block 7 re-reads each typed "
          "figure from the PDF page the chapter cites; it runs only where pdftotext and the PDFs are present, and prints "
          "SKIP otherwise, which is not a pass.")
    print("[HONESTY] Nothing here shows the Fund's holdings after 31 December 2023, the policy now in force (the 2020 "
          "version has been replaced), the credit-rating mix, how much of any loss is credit rather than rates, or the "
          "posting's details, which are printed but not checked against a held copy.")
    if FAIL or ctl:
        print(f"\nFAILED: {len(FAIL)} check(s), {len(ctl)} control(s) not rejected"); sys.exit(1)
    print(f"\nALL PASS" + (f" ({len(SKIP)} skipped: not a pass)" if SKIP else ""))
main()
