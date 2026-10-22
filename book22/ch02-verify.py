#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book22/ch02-verify.py -- every figure on book22/ch02-facts-and-findings.html. Run first (R24).
    python3 book22/ch02-verify.py
Standard library only. The figures below were copied by hand on 2026-10-22 from what a fetch tool returned
for each source URL. A fetch tool summarizes the page; it is not a reading of the page image or the PDF.
So this script proves the PAGE matches those recorded figures, not that the figures match the sources.
  [1] each recorded figure appears on the page
  [2] each finding F1..F8 has English and Portuguese text
  [3] the status box (fetched, not independently read) is present
  [4] a changed figure and a removed finding are both caught (control)
  [HONESTY] what this does not establish
"""
import re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def plain(t): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t))

# (finding, string that must appear, source it was copied from)
FIGURES = [
 ("F1", "5.6 percent", "NY Fed, 2026:Q2 Quarterly Highlights"),
 ("F1", "42 percent", "NY Fed, 2026:Q2 Quarterly Highlights"),
 ("F2", "1.8", "BLS, doctoral unemployment rate 2025"),
 ("F2", "2.8", "BLS, bachelor's unemployment rate 2025"),
 ("F2", "3.4", "BLS, all workers unemployment rate 2025"),
 ("F2", "1,578", "BLS, bachelor's median weekly earnings 2025"),
 ("F2", "1,268", "BLS, all workers median weekly earnings 2025"),
 ("F3", "9.65", "Bertrand & Mullainathan, AER 2004, Table 1"),
 ("F3", "6.45", "Bertrand & Mullainathan, AER 2004, Table 1"),
 ("F3", "3.20", "Bertrand & Mullainathan, AER 2004, Table 1"),
 ("F3", "4,870", "Bertrand & Mullainathan, AER 2004, Tables 1 and 3"),
 ("F4", "3.0 cents", "IZA DP 18239, willingness to pay, math"),
 ("F4", "7.2 cents", "IZA DP 18239, willingness to pay, verbal"),
 ("F4", "1,472", "IZA DP 18239, employers"),
 ("F5", "14%", "IZA DP 7725, gain for very popular American names"),
 ("F5", "1930", "IZA DP 7725, naturalized by 1930"),
 ("F6", "257.655", "Michigan Compiled Laws"),
 ("F6", "5263", "Michigan House Bill 5263, 2000"),
 ("F7", "11,488", "Wikipedia, Ulcinj, town population 2023 census"),
 ("F7", "21,395", "Wikipedia, Ulcinj, municipality 2023 census"),
 ("F7", "67.38%", "Wikipedia, Ulcinj, Albanian mother tongue, town"),
 ("F7", "74.44%", "Wikipedia, Ulcinj, Albanian mother tongue, municipality"),
 ("F7", "Ulqini", "Wiktionary, Ulqin, definite form"),
 ("F7", "Gheg", "Wikipedia, Albanians in Montenegro"),
 ("F8", "14183", "govinfo, DCPD-202500187, Executive Order 14183"),
 ("F8", "January 27, 2025", "govinfo, DCPD-202500187, date signed"),
 ("F8", "4(a)(1)", "govinfo, EO 14183 Sec. 4(a)(1), pronouns"),
 ("F8", "4(c)", "govinfo, EO 14183 Sec. 4(c), facilities"),
 ("F8", "extraordinary operational necessity", "govinfo, EO 14183 Sec. 4(c)"),
 ("F8", "June 1, 2026", "FindLaw and Military Times, D.C. Circuit in Talbott"),
 ("F8", "2 to 1", "Gender Justice League tracker, Sept 2026"),
 ("F8", "June 30, 2026", "Gender Justice League tracker, class certification"),
 ("F8", "4,240", "Military Times citing AP; tracker"),
 ("F8", "August 28, 2026", "Gender Justice League tracker, DOJ request to the Supreme Court"),
 ("F8", "October 20, 2025", "Gender Justice League tracker, Shilling argued"),
 ("F8", "November 3, 2026", "Gender Justice League tracker, Shilling trial"),
 ("F8", "May 2025", "Gender Justice League tracker, Supreme Court stay in Shilling"),
]
FINDINGS = ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8"]

def missing(text):
    p = plain(text)
    return [f"{f}:{s}" for f, s, _ in FIGURES if s not in p]
def findings_ok(text):
    got = {}
    for m in re.finditer(r'<div class="sec" data-n="([^"]+)">(.*?</div>)\s*</div>\s*(?=<div class="sec"|<!--end-secs-->)', text, re.S):
        body = m.group(2)
        en = re.search(r'<div lang="en">(.*?)</div>', body, re.S)
        pt = re.search(r'<div lang="pt">(.*?)</div>', body, re.S)
        got[m.group(1)] = bool(en and plain(en.group(1)).strip()) and bool(pt and plain(pt.group(1)).strip())
    return list(got) == FINDINGS and all(got.values())

p = HERE / "ch02-facts-and-findings.html"
if p.exists():
    t = p.read_text(encoding="utf-8")
else:
    t = ""; check("ch02 exists", False)
print("[1] figures on the page")
miss = missing(t) if t else [f for f, _, _ in FIGURES]
check(f"all {len(FIGURES)} recorded figures are on the page", not miss, ", ".join(miss))
print("[2] findings")
check("F1..F8 each have English and Portuguese text", bool(t) and findings_ok(t))
print("[3] status box")
check("page says the figures were fetched, not independently read", "not independently read" in plain(t))
print("[3b] F8 labels")
def f8_labels(text):
    q = plain(text)
    return ("Not verified" in q and "could not be fetched" in q and "published by a plaintiff" in q
            and "after the September 2026 tracker were not searched" in q and "the author" in q)
check("F8 says what was not verified, who published the tracker, and what was not searched", bool(t) and f8_labels(t))
check("control: the 'not verified' label removed is caught", bool(t) and not f8_labels(t.replace("Not verified", "")))
print("[4] controls")
check("control: a changed figure (9.65 -> 9.56) is caught", bool(t) and bool(missing(t.replace("9.65", "9.56"))))
d = re.sub(r'<div class="sec" data-n="F4">', '<div class="sec" data-n="F4x">', t, count=1) if t else ""
check("control: a renamed finding is caught", bool(t) and not findings_ok(d))
print("[HONESTY] Figures were taken from a fetch tool's summary of each page, not from the typeset papers or the BLS/NY Fed")
print("  pages themselves. The page matches these records; the records are not yet checked against the sources.")
print("\nFAILED: " + ", ".join(FAIL) if FAIL else "\nALL PASS")
sys.exit(1 if FAIL else 0)
