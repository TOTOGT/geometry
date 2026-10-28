#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book26/ch11-verify.py -- book26/ch11-the-books-they-manage.html (version 3, Template B as chapters 10 to 19): the NYSIF bond book at
31 December 2025, and seven years of realized gains and losses, from the Fund's own reports and the
Department of Financial Services' reports on examination.
  [1] Template B structure (hero, section nav, sections in order, Sources footer), required labels, no network/storage/form code
  [2] the 2025 report reconciles from its own columns: book + (fair minus book) = fair per category,
      categories and maturities add to the totals; NAIC designation amounts reproduce their printed percentages
  [3] seven years: each year's realized table is covered by its stock and bond lines to within $0.3M
  [4] both tables on the page, cell by cell
  [5] every figure quoted in prose equals its computed value   [6] every comparative claim, computed
  [7] SOURCE: each typed figure re-read from its report (2025 figures from the cited page; 2019-2025 from
      the 2020-2025 reports, each year in both reports that print it); prints SKIP, never PASS, without
      pdftotext or the PDFs
  [8] controls   [HONESTY]
PDFs looked for in $NYSIF_PDF_DIR, ~/Downloads and ~/Desktop/grants/nysif, named AR2020.pdf ... AR2025.pdf,
IPS-2020.pdf, BoC-2025-10-30.pdf, DFS-exam-2014.pdf, DFS-exam-2019.pdf. Figures are $ thousands unless noted.
"""
import os, re, shutil, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
PAGE = HERE / "ch11-the-books-they-manage.html"
FAIL, SKIP = [], []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def skip(label, why): print(f"SKIP {label}  -- {why}"); SKIP.append(label)
def plain(t):
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", t, flags=re.S); t = re.sub(r"<[^>]+>", " ", t)
    for a, b in (("&rsquo;", "'"), ("&ldquo;", '"'), ("&rdquo;", '"'), ("&amp;", "&"), ("&mdash;", "-"), ("&ndash;", "-"),
                 ("&middot;", "."), ("&nbsp;", " "), ("&minus;", "-"), ("&eacute;", "e"), ("&divide;", "/")):
        t = t.replace(a, b)
    return re.sub(r"\s+", " ", t)

# ---- typed from the PDFs, re-read 2026-10-28 ----------------------------------------------------------
BS25 = {"bonds": 19466090, "stocks": 2421510, "cash": 945387, "total": 23394667}                     # 2025 p. 4
BOND25 = [("U.S. Government obligations", 3599240, -744682, 2854558), ("All other governments", 54339, -6890, 47449),
          ("Municipal bonds", 1295323, -136627, 1158696), ("Corporate bonds", 9515465, -237004, 9278461),
          ("Bank loans", 460756, 2460, 463216), ("Asset-backed securities", 4540967, -106337, 4434630)]   # 2025 p. 24
BOND25_TOTAL = (19466090, -1229080, 18237010)
MAT25 = [("Due in one year or less", 977008, 970633), ("Due after one year through five years", 7480939, 7410018),
         ("Due after five years through ten years", 2780021, 2795421), ("Due after ten years", 8228122, 7060938)]  # p. 25
LEND25 = (509666, 521935)                                                                            # p. 26
NAIC25 = [17742803827, 876792672, 768585076, 78934941, 4194038, 0]       # p. 46, dollars (scanned page)
NAIC25_PRINTED_PCT = [70.895, 3.503, 3.071, 0.315, 0.017]                 # p. 46, percent of admitted assets
ADMITTED25 = 25026921168                                                  # p. 46, dollars
TOP25 = {"Freddie Mac": 1042547372, "Fannie Mae": 765236653}              # p. 46, dollars
YEARS = [2019, 2020, 2021, 2022, 2023, 2024, 2025]
REAL_STOCKS = [42797, 307690, 208897, -22664, 141535, 249126, 86864]
REAL_BONDS  = [154223, 253656, 38261, -30859, -85325, -43353, -14978]
REAL_TOTAL  = [196965, 561294, 247197, -53755, 56224, 205795, 71894]
STOCKS_BS   = [1849910, 1842300, 2051036, 1636782, 1827205, 2057268, 2421510]
CASH_INV    = [19017037, 19782545, 20566185, 20372828, 21025079, 22447840, 23394667]
BONDS_BS    = [16292127, 17269891, 17798893, 18121860, 18476899, 18975313, 19466090]
INC_BONDS   = [520734, 497038, 468999, 485220, 575900, 657836, 715173]
PROCEEDS    = [6826580, 6606699, 5248921, 3253651, 3496010, 3569252, 3988314]
ACQUIRED    = [7079379, 6861774, 5541621, 3841961, 3699723, 4124452, 4632943]
OPS_CASH    = [642793, 235249, 338024, 386432, 447690, 627683, 606755]
DFS_1014_REALIZED, DFS_1519_REALIZED = 1136677570, 957422517             # dollars
DFS_YIELDS = [4.1, 3.8, 3.4, 3.0, 2.8]                                    # 2010-2014, DFS 2014 report
RESERVE_DISCOUNT = 5
CITED25 = {"balance sheet": 4, "bond table": 24, "maturity table": 25, "securities lending": 26, "lending agent": 27, "reserve discount": 9, "rates note": 29}
QUOTE_RATES = "primarily impacted by a change in interest rates after the purchase date"
QUOTE_WASH = "may be sold at a loss and repurchased within 30 days of the sale date to enhance WCF"

def M(x): return f"{x/1000:,.1f}"
def S(x): return ("-" if x < 0 else "") + f"{abs(x)/1000:,.1f}"
def P(x): return ("-" if x < 0 else "") + f"{abs(x):.1f}"
share = [s / c * 100 for s, c in zip(STOCKS_BS, CASH_INV)]
yld = [i / b * 100 for i, b in zip(INC_BONDS, BONDS_BS)]
turn = [p / b * 100 for p, b in zip(PROCEEDS, BONDS_BS)]

SECS = ["posting", "books", "rules", "numbers", "money", "monitor", "limits", "updates", "checked"]
LABELS = ["not a statement by the fund", "the author's arithmetic", "the author's proposals, not the fund's plans",
          "the monitor does not exist yet", "the policy has moved since", "not checked:",
          "that the author meets the posting's experience requirement", "how much of that is credit is not measured here",
          "that is an inference from the filings, not something they state", "this is a question, not a finding of a breach",
          "describes what the fund allows, not what it did", "not a recommendation to hedge", "are not directly comparable",
          "which bonds were sold, when and why"]
FORBIDDEN = ["fetch(", "XMLHttpRequest", "localStorage", "<form", "action="]
def secs_ok(t): return re.findall(r'<section id="([^"]+)">', t) == SECS
def template_ok(t):
    return all(k in t for k in ("Template B", '<header class="hero">', '<nav class="pillars"', '<footer id="sources">', '<div class="chapnav">', "family=Cinzel"))
def labels_ok(t): p = plain(t).lower(); return all(l in p for l in LABELS)
def safe_ok(t): return not any(f in t for f in FORBIDDEN)
def tables(t):
    out = []
    for tb in re.findall(r"<table>(.*?)</table>", t, re.S):
        out.append([[plain(c).strip().replace(" ", "") for c in re.findall(r'<td class="num">(.*?)</td>', tr, re.S)]
                    for tr in re.findall(r"<tr>(.*?)</tr>", tb, re.S)[1:]])
    return [x for x in out if any(x)]          # the two number tables; the Updates table has no number cells
def exp_s2():
    r = [[M(b), M(f), S(d), P(d / b * 100)] for _, b, d, f in BOND25]
    b, d, f = BOND25_TOTAL; return r + [[M(b), M(f), S(d), P(d / b * 100)]]
def exp_s5(): return [[S(a), S(b), f"{c:.1f}", f"{d:.2f}", f"{e:.0f}"] for a, b, c, d, e in zip(REAL_STOCKS, REAL_BONDS, share, yld, turn)]
def tables_ok(t):
    tb = tables(t); return len(tb) == 2 and tb[0] == exp_s2() and tb[1] == exp_s5()
def years_ok(t):
    tb = [x for x in re.findall(r"<table>(.*?)</table>", t, re.S) if 'class="num"' in x]
    return len(tb) == 2 and [int(y) for y in re.findall(r"<tr><td>(\d{4})</td>", tb[1])] == YEARS

def prose_expected():
    B = BS25; book, dfv, _ = BOND25_TOTAL; gap = -dfv; c = {n: (b, d) for n, b, d, _ in BOND25}
    pb = lambda n: -c[n][1] / c[n][0] * 100
    tot = sum(NAIC25); below = sum(NAIC25[2:]); lg = MAT25[3][1] - MAT25[3][2]; mid = MAT25[2][2] - MAT25[2][1]
    up, dn = sum(REAL_BONDS[:3]), sum(REAL_BONDS[3:])
    return {
      "cash and invested": f"${B['total']/1e6:.1f} billion of cash and invested assets",
      "bonds share": f"${B['bonds']/1e6:.2f} billion of that, or {B['bonds']/B['total']*100:.1f} percent",
      "stocks share": f"${B['stocks']/1e6:.2f} billion ({B['stocks']/B['total']*100:.1f} percent)",
      "cash share": f"${B['cash']/1e3:.0f} million ({B['cash']/B['total']*100:.1f} percent)",
      "corporates": f"Corporate bonds were ${c['Corporate bonds'][0]/1e6:.2f} billion, {c['Corporate bonds'][0]/book*100:.0f} percent of the bond book",
      "NAIC 1 and 2": f"{NAIC25[0]/tot*100:.1f} percent of the bonds carry the top NAIC designation and {NAIC25[1]/tot*100:.1f} percent the second",
      "below IG": f"${below/1e6:,.1f} million, {below/tot*100:.1f} percent, is below investment grade",
      "NAIC difference": f"add to ${(tot - B['bonds']*1000)/1e6:.1f} million more than the balance-sheet bond figure",
      "Freddie Mac": f"Freddie Mac (${TOP25['Freddie Mac']/1e6:,.1f} million)", "Fannie Mae": f"Fannie Mae (${TOP25['Fannie Mae']/1e6:,.1f} million)",
      "lending": f"${LEND25[0]/1e3:.1f} million of securities on loan, supported by ${LEND25[1]/1e3:.1f} million of collateral",
      "gap": f"${gap/1e6:.2f} billion below its book value, about {gap/book*100:.1f} percent",
      "govt": f"were about {pb('U.S. Government obligations'):.0f} percent below book", "munis": f"municipal bonds about {pb('Municipal bonds'):.0f} percent",
      "corp pct": f"corporate bonds {pb('Corporate bonds'):.1f} percent", "abs pct": f"asset-backed securities {pb('Asset-backed securities'):.1f} percent",
      "long end": f"${lg/1e6:.2f} billion below book, {lg/gap*100:.0f} percent of the whole gap",
      "5-10 above book": f"${mid/1e3:.1f} million above book",
      "stock gains": f"six of the seven years, ${sum(REAL_STOCKS)/1e6:.2f} billion in all",
      "DFS realized": f"${DFS_1014_REALIZED/1e9:.2f} billion over 2010 to 2014 and ${DFS_1519_REALIZED/1e6:,.0f} million over 2015 to 2019",
      "stock share range": f"between {min(share):.1f} and {max(share):.1f} percent of cash and invested assets",
      "bond gains 2019-21": f"net gains of ${up/1e3:,.1f} million over 2019 to 2021", "bond losses 2022-25": f"net losses of ${-dn/1e3:,.1f} million over 2022 to 2025",
      "shrinking": f"{S(REAL_BONDS[4])}, {S(REAL_BONDS[5])} and {S(REAL_BONDS[6])} million",
      "net buyer": f"by ${min(a - p for a, p in zip(ACQUIRED, PROCEEDS))/1e3:,.1f} million at the least",
      "yield rise": f"from {yld[3]:.2f} percent in 2022 to {yld[6]:.2f} percent in 2025",
      "turnover": f"from {turn[0]:.0f} percent of the bond book in 2019 to about {sum(turn[3:])/4:.0f} percent from 2022",
      "DFS yields": f"lists {', '.join(f'{v:.1f}' for v in DFS_YIELDS[:-1])} and {DFS_YIELDS[-1]:.1f} percent for 2010 to 2014",
      "ratio range": f"between {min(yld):.2f} and {max(yld):.2f} percent through 2025",
      "reserve discount": f"discount all its claim reserves at a fixed {RESERVE_DISCOUNT} percent",
      "lending agent": "its lending agent is JPMorgan Chase",
      "rates quote": QUOTE_RATES, "wash quote": QUOTE_WASH.replace("WCF", "WCF's yield")[:-len("WCF's yield")] + "WCF's yield",
    }
def prose_ok(t): p = plain(t); return all(v in p for v in prose_expected().values())
def stats_expected():
    B = BS25; tot = sum(NAIC25); up, dn = sum(REAL_BONDS[:3]), sum(REAL_BONDS[3:])
    return [f"${B['total']/1e6:.1f}B", f"{B['bonds']/B['total']*100:.1f}%", f"{B['stocks']/B['total']*100:.1f}% in common stocks",
            f"{B['cash']/B['total']*100:.1f}% in cash", f"${-BOND25_TOTAL[1]/1e6:.2f}B", f"{sum(NAIC25[2:])/tot*100:.1f}%",
            f"${sum(REAL_STOCKS)/1e6:.2f}B", f"-${-dn/1e3:,.1f}M", f"+${up/1e3:,.1f}M", "7 of 7", f"{min(yld):.2f}-{max(yld):.2f}%"]
def stats_ok(t):
    blocks = " ".join(plain(b) for b in re.findall(r'<div class="stats">(.*?)</div>\s*</div>', t, re.S))
    return all(v in blocks for v in stats_expected())
def claims():
    gap = -BOND25_TOTAL[1]; corp = dict((n, d) for n, _, d, _ in BOND25)["Corporate bonds"]; s = MAT25[0]; m = MAT25[2]
    return {"stocks show gains in six of seven years": sum(x > 0 for x in REAL_STOCKS) == 6,
            "corporates hold less than a quarter of the 2025 gap": -corp / gap < 0.25,
            "bonds due within a year are within 1 percent of book": (s[1] - s[2]) / s[1] < 0.01,
            "bonds due in five to ten years are above book": m[2] > m[1],
            "realized bond results positive 2019-2021, negative 2022-2025": all(x > 0 for x in REAL_BONDS[:3]) and all(x < 0 for x in REAL_BONDS[3:]),
            "bond losses shrink each year from 2023": REAL_BONDS[4] < REAL_BONDS[5] < REAL_BONDS[6] < 0,
            "operating cash positive every year": all(x > 0 for x in OPS_CASH),
            "net buyer of investments every year": all(a > p for a, p in zip(ACQUIRED, PROCEEDS)),
            "stock share above the 2020 target (5%) and maximum (8%) every year": all(x > 8 for x in share),
            "bond income over book below the 5% reserve rate every year": all(x < RESERVE_DISCOUNT for x in yld),
            "turnover from 2022 is about half of 2019's": 0.4 < (sum(turn[3:]) / 4) / turn[0] < 0.6,
            "corporate book agrees with the posting's 'more than $9 billion'": dict((n, b) for n, b, _, _ in BOND25)["Corporate bonds"] > 9_000_000}

# ---- [7] source -----------------------------------------------------------------------------------------
def pdf_dir():
    for d in (os.environ.get("NYSIF_PDF_DIR", ""), "~/Downloads", "~/Desktop/grants/nysif"):
        if d and (Path(d).expanduser() / "AR2025.pdf").exists(): return Path(d).expanduser()
def pdftext(path):
    if not path.exists(): return ""
    r = subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True, text=True); return r.stdout
def nums(line):
    return [(-1 if n.startswith("(") else 1) * int(n.strip("() ").replace(",", "")) for n in re.findall(r"\(\s*[\d,]{2,}\s*\)|\d{1,3}(?:,\d{3})+|\d{4,}", line)]
def wcf(pages):
    end = next((i for i, p in enumerate(pages) if i > 30 and "DISABILITY BENEFITS FUND" in p and "Statutory Basis" in p), len(pages))
    return pages[:end]
def wcf_page(pages, printed):
    for p in wcf(pages):
        L = [l.strip() for l in p.splitlines() if l.strip()]
        if L and re.fullmatch(rf"-\s*{printed}\s*-", L[-1]): return p
    return ""
def row(page, label, n=2):
    for l in page.splitlines():
        if re.search(label, l.replace("—", "-"), re.I) and len(nums(l)) >= n: return nums(l)
    return []
def find(pages, anchor, label):
    for p in wcf(pages):
        L = p.splitlines(); k = next((i for i, l in enumerate(L) if re.search(anchor, l, re.I)), None)
        if k is None: continue
        for l in L[k:]:
            if re.search(label, l, re.I) and len(nums(l)) >= 2: return nums(l)[-2:]
    return None
FIELDS = {"REAL_BONDS": (r"Net realized capital gains (\(losses\) )?on investments", r"^\s*Bonds"),
          "REAL_STOCKS": (r"Net realized capital gains (\(losses\) )?on investments", r"^\s*Stocks"),
          "REAL_TOTAL": (r"Net realized capital gains (\(losses\) )?on investments", r"^\s*Net realized capital gains(?!\s+(\(losses\)\s+)?on)"),
          "STOCKS_BS": (r"Admitted assets", r"^\s*Common stocks"), "CASH_INV": (r"Admitted assets", r"Total cash and invested assets"),
          "BONDS_BS": (r"Admitted assets", r"^\s*Bonds"), "INC_BONDS": (r"Net investment income earned consists", r"^\s*Bonds"),
          "PROCEEDS": (r"Cash flows from investments", r"Proceeds from investments sold"),
          "ACQUIRED": (r"Cash flows from investments", r"Cost of investments acquired"),
          "OPS_CASH": (r"Cash flows from operations", r"Net cash (provided by|from) operations")}
def source_checks(d, cited=None):
    cited = cited or CITED25; res = {}
    ar = {y: pdftext(d / f"AR{y}.pdf").split("\f") for y in range(2020, 2026)}
    p25 = ar[2025]
    pg = {k: wcf_page(p25, v) for k, v in cited.items()}
    bs = pg["balance sheet"]
    res["2025 p. 4: bonds, stocks, cash, total"] = (row(bs, r"Bonds-at NAIC")[:1] == [BS25["bonds"]] and row(bs, r"^\s*Common stocks")[:1] == [BS25["stocks"]]
        and row(bs, r"Cash, cash equivalents")[:1] == [BS25["cash"]] and row(bs, r"Total cash and invested")[:1] == [BS25["total"]])
    for n, b, dd, f in BOND25: res[f"2025 p. 24: {n}"] = row(pg["bond table"], rf"^\s*{re.escape(n)}\s", 3)[:3] == [b, dd, f]
    res["2025 p. 24: Total bonds"] = row(pg["bond table"], r"^\s*Total bonds", 3)[:3] == list(BOND25_TOTAL)
    for n, a, f in MAT25: res[f"2025 p. 25: {n}"] = row(pg["maturity table"], re.escape(n))[:2] == [a, f]
    lp = re.sub(r"\s+", " ", pg["securities lending"])
    res["2025 p. 26: on loan and collateral"] = f"${LEND25[0]:,}" in lp and f"${LEND25[1]:,}" in lp
    res["2025 p. 27: lending agreement is with JPMorgan Chase"] = "security lending agreement is with JPMorgan Chase" in re.sub(r"\s+", " ", pg["lending agent"]).replace("\u2019", "'")
    res["2025 p. 9: reserves discounted at 5% by law"] = f"reserves at {RESERVE_DISCOUNT}%" in re.sub(r"\s+", " ", pg["reserve discount"])
    res["2025 p. 29: the Fund's note on rates"] = QUOTE_RATES in re.sub(r"\s+", " ", pg["rates note"])
    res["2025: income-tax exemption"] = "exempt from federal and state income taxes" in re.sub(r"\s+", " ", " ".join(wcf(p25)))
    res["2025: 2024 figures 'are not directly comparable'"] = "are not directly comparable" in re.sub(r"\s+", " ", " ".join(wcf(p25)))
    for y in range(2020, 2026):
        w = re.sub(r"\s+", " ", " ".join(wcf(ar[y]))).replace("’", "'")
        res[f"{y} report: the wash-sale sentence"] = QUOTE_WASH in w
        if y <= 2024: res[f"{y} report: no additional other-than-temporary impairments"] = "no additional other-than-temporary impairments" in w
        for f, (a, lab) in FIELDS.items():
            v = find(ar[y], a, lab); i = YEARS.index(y)
            sign = -1 if f == "ACQUIRED" else 1          # the cash flow statement prints purchases as an outflow, in parentheses
            res[f"{y} report: {f} {y} and {y-1}"] = v == [sign * globals()[f][i], sign * globals()[f][i - 1]]
    d14, d19 = (re.sub(r"\s+", " ", pdftext(d / f)) for f in ("DFS-exam-2014.pdf", "DFS-exam-2019.pdf"))
    res["DFS 2014: yield 'has not exceeded five percent'"] = "has not exceeded five percent during the examination period" in d14
    res["DFS 2014: yields 2010-2014"] = all(f"{y} {v:.1f}%" in d14 for y, v in zip(range(2010, 2015), DFS_YIELDS))
    res["DFS 2014: net realized gain 2010-2014"] = f"Net realized capital gain {DFS_1014_REALIZED:,}" in d14
    res["DFS 2019: net realized gain 2015-2019"] = f"Net realized capital gain {DFS_1519_REALIZED:,}" in d19
    ips = re.sub(r"\s+", " ", pdftext(d / "IPS-2020.pdf")); boc = re.sub(r"\s+", " ", pdftext(d / "BoC-2025-10-30.pdf"))
    for s in ["As amended by the Board of Commissioners on November 18, 2020", "Investment Grade Fixed 78% 85% 100% NYSIF Custom Benchmark",
              "High Yield 0% 4% 7%", "Public Equities 0% 5% 8%", "Alternatives 0% 4% 7%", "Cash 0% 2% 3% ICE BofAML 3-month T-Bill",
              "mid-single A/A2", "duration target of eight years +/- 1 year", "pay 75% of liabilities coming due in the next 365 days"]:
        res[f"IPS: {s[:46]}"] = s in ips
    for s in ["dated December 18, 2024", "current market environment and risks", "review and adopt it once a year"]: res[f"minutes: {s}"] = s in boc
    return res

def main():
    t = PAGE.read_text(encoding="utf-8") if PAGE.exists() else ""
    check("page exists", bool(t))
    if not t: print("\nFAILED: page absent"); sys.exit(1)
    print("[1] structure"); check("Template B: hero, section nav, Sources footer, chapter nav, Cinzel/Garamond", template_ok(t)); check("sections in order: " + ", ".join(SECS), secs_ok(t)); check("required labels present", labels_ok(t)); check("no network, storage or form code", safe_ok(t))
    print("[2] the 2025 report reconciles from its own columns")
    for n, b, d, f in BOND25: check(f"book + (fair minus book) = fair: {n}", b + d == f)
    for i, nm in enumerate(("book", "fair minus book", "fair")): check(f"categories add to the total ({nm})", sum((b, d, f)[i] for _, b, d, f in BOND25) == BOND25_TOTAL[(0, 1, 2)[i]])
    check("maturity table adds to the bond totals", (sum(a for _, a, _ in MAT25), sum(f for *_, f in MAT25)) == (BOND25_TOTAL[0], BOND25_TOTAL[2]))
    check("NAIC amounts reproduce the printed percentages of admitted assets (scanned page read correctly)",
          all(round(n / ADMITTED25 * 100, 3) == p for n, p in zip(NAIC25, NAIC25_PRINTED_PCT)))
    print("[3] seven years"); [check(f"{y}: stock and bond lines cover the realized total to within $0.3M", abs(T - s - b) < 300) for y, s, b, T in zip(YEARS, REAL_STOCKS, REAL_BONDS, REAL_TOTAL)]
    print("[4] tables, cell by cell"); check("S2 table equals computed values", tables_ok(t), "28 cells"); check("S5 table equals computed values, years in order", tables_ok(t) and years_ok(t), "35 cells")
    print("[5] figures quoted in prose"); p = plain(t)
    for k, v in prose_expected().items(): check(f"prose: {k}", v in p, v[:90])
    check("stat panels equal computed values", stats_ok(t), f"{len(stats_expected())} figures")
    c10 = (HERE / "ch10-four-pillars-one-mission.html"); fact = "securities finance at JPMorgan Chase (2005 to 2008)"
    if c10.exists(): check("author aside: the JPMorgan Chase dates match chapter 10 word for word", fact in plain(c10.read_text(encoding="utf-8")) and fact in plain(t))
    else: skip("author aside against chapter 10", "ch10 not beside the page")
    print("[6] comparative claims"); [check(k, ok) for k, ok in claims().items()]
    print("UNCHECKED  posting figures in S1 ($179,150-$229,150; 27 Oct and 1 Dec 2026; more than $22 and $9 billion): the posting is not held here")
    print("[7] SOURCE")
    d = pdf_dir()
    if not shutil.which("pdftotext"): skip("source checks", "pdftotext not installed")
    elif not d: skip("source checks", "AR2025.pdf not found in $NYSIF_PDF_DIR, ~/Downloads or ~/Desktop/grants/nysif")
    else:
        for k, ok in source_checks(d).items(): check(k, ok)
        skip("2025 p. 46 NAIC designations and largest exposures", "scanned page with no text layer; checked in [2] against its own printed percentages")
    print("[8] controls"); ctl = []
    def control(name, damaged, fn):
        ok = fn(damaged); print(("PASS " if not ok else "FAIL ") + "control rejected: " + name)
        if ok: ctl.append(name)
    control("section removed", t.replace('<section id="money">', '<section id="x">'), secs_ok)
    control("chapter 1-9 layout swapped in", t.replace('<header class="hero">', '<div class="wp-head">'), template_ok)
    control("stat panel figure changed", t.replace(">7 of 7<", ">6 of 7<"), stats_ok)
    control("label removed", t.replace("not a recommendation to hedge", "a recommendation"), labels_ok)
    control("S2 cell changed", t.replace(">9,515.5<", ">9,551.5<"), tables_ok)
    control("S5 cells swapped (2023 and 2024 stock gains)", t.replace(">141.5<", ">TMP<").replace(">249.1<", ">141.5<").replace(">TMP<", ">249.1<"), tables_ok)
    control("prose figure changed", t.replace("$509.7 million", "$590.7 million"), prose_ok)
    control("form code pasted in", t + " <form ", safe_ok)
    if d and shutil.which("pdftotext"):
        bad = source_checks(d, dict(CITED25, **{"securities lending": 25}))["2025 p. 26: on loan and collateral"]
        print(("PASS " if not bad else "FAIL ") + "control rejected: 2025 securities lending cited to p. 25")
        if bad: ctl.append("wrong page")
        keep = REAL_STOCKS[:]; REAL_STOCKS[4] = 141536
        bad = source_checks(d)["2023 report: REAL_STOCKS 2023 and 2022"]; REAL_STOCKS[:] = keep
        print(("PASS " if not bad else "FAIL ") + "control rejected: 2023 stock gain typed $1K off")
        if bad: ctl.append("typed figure")
    print("[HONESTY] Blocks 2 to 6 show that the figures typed into this script reconcile under each report's own arithmetic, "
          "that the page prints exactly those figures in the right cells, and that each comparative sentence holds for them. "
          "Block 7 re-reads each typed figure from its report, the 2025 ones from the page the chapter cites and each year's "
          "figures from both reports that print them; it prints SKIP where pdftotext or the PDFs are missing, which is not a pass. "
          "The scanned page of NAIC designations is checked only against its own printed percentages.")
    print("[HONESTY] Nothing here shows which bonds were sold or why: the reasons in S5 are fitted to the filings, not read "
          "from them, apart from the Fund's 'may be sold ... to enhance yield' sentence. It does not show holdings after "
          "31 December 2025, the policy now in force, the rate and credit split of any loss, or the posting's details.")
    if FAIL or ctl: print(f"\nFAILED: {len(FAIL)} check(s), {len(ctl)} control(s) not rejected"); sys.exit(1)
    print("\nALL PASS" + (f" ({len(SKIP)} skipped: not a pass)" if SKIP else ""))
main()
