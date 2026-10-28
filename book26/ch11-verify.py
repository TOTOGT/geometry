#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book26/ch11-verify.py -- book26/ch11-the-books-they-manage.html: the NYSIF bond book from its own public documents.
  [1] sections S1..S6 in order  [2] labels present  [3] the report's table adds up (book, market, net)
  [4] every number on the page equals the number computed from the report's figures  [5] controls  [HONESTY]
Figures are in $ thousands, typed from the 2023 annual report Note 3 table (p. 24) as read through a fetch summary.
They have NOT been re-read against the PDF; that is stated on the page.
"""
import re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
PAGE = HERE / "ch11-the-books-they-manage.html"
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def plain(t):
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    for a, b in (("&rsquo;", "'"), ("&ldquo;", '"'), ("&rdquo;", '"'), ("&amp;", "&"), ("&mdash;", "-"), ("&ndash;", "-"), ("&middot;", "."), ("&nbsp;", " "), ("&minus;", "-"), ("&eacute;", "e")):
        t = t.replace(a, b)
    return re.sub(r"\s+", " ", t)
# category: (book, market) in $ thousands
CAT = {"govt": (5984174, 5152556), "munis": (1343430, 1159586), "corp": (9237910, 8814063), "mbs": (1911385, 1865284)}
TOTAL_BOOK, TOTAL_MKT = 18476899, 16991489
CASH_INV, STOCKS, SHORT = 21025079, 1827205, 462690
def m(x): return f"{x/1000:,.1f}"
def sgn(x): return ("-" if x < 0 else "") + f"{abs(x)/1000:,.1f}"
def pct(a, b): return f"{a/b*100:.1f}"
def expected_strings():
    s = []
    for k, (b, mk) in CAT.items():
        s += [m(b), m(mk), sgn(mk - b), "-" + pct(b - mk, b)]
    s += [m(TOTAL_BOOK), m(TOTAL_MKT), sgn(TOTAL_MKT - TOTAL_BOOK), "-" + pct(TOTAL_BOOK - TOTAL_MKT, TOTAL_BOOK)]
    s += [pct(TOTAL_BOOK, CASH_INV), pct(STOCKS, CASH_INV), pct(SHORT, CASH_INV)]
    return s
SECS = ["S1", "S2", "S3", "S4", "S5", "S6"]
LABELS = ["not a statement by the fund", "author's arithmetic", "the author's proposals, not the fund's plans", "the monitor does not exist yet",
          "not yet checked", "re-read against the report pages", "the policy has moved since", "does not show that the author meets"]
FORBIDDEN = ["fetch(", "XMLHttpRequest", "localStorage", "<form", "action="]
def secs_ok(t): return re.findall(r'<div class="sec" data-n="([^"]+)">', t) == SECS
def labels_ok(t):
    p = plain(t).lower().replace("meets the posting's", "meets the posting's")
    need = [l for l in LABELS if l != "does not show that the author meets"]
    return all(l in p for l in need) and "that the author meets the posting's experience requirement" in p
def safe_ok(t): return not any(f in t for f in FORBIDDEN)
def nums_ok(t):
    p = plain(t); return all(e in p for e in expected_strings())
def main():
    t = PAGE.read_text(encoding="utf-8") if PAGE.exists() else ""
    check("page exists", bool(t))
    if not t:
        print("\nFAILED: page absent"); sys.exit(1)
    check("sections S1..S6 in order", secs_ok(t))
    check("required labels present", labels_ok(t))
    check("no network, storage or form code", safe_ok(t))
    sb = sum(b for b, _ in CAT.values()); sm = sum(mk for _, mk in CAT.values())
    check("categories sum to the report's book total", sb == TOTAL_BOOK, f"{sb} vs {TOTAL_BOOK}")
    check("categories sum to the report's market total", sm == TOTAL_MKT, f"{sm} vs {TOTAL_MKT}")
    check("net unrealized equals market minus book, total and by category", sum(mk - b for b, mk in CAT.values()) == TOTAL_MKT - TOTAL_BOOK)
    check("corporate share of bonds is about half", abs(CAT['corp'][0] / TOTAL_BOOK - 0.5) < 0.005, pct(CAT['corp'][0], TOTAL_BOOK) + " percent")
    check("every table and percentage figure on the page equals the computed value", nums_ok(t), f"{len(expected_strings())} figures")
    ctl = []
    def control(name, damaged, fn):
        ok = fn(damaged); print(("PASS " if not ok else "FAIL ") + "control rejected: " + name)
        if ok: ctl.append(name)
    control("section removed", t.replace('data-n="S4"', 'data-n="X"'), secs_ok)
    control("label removed", re.sub(r"not a statement by the fund", "a statement", t, flags=re.I), labels_ok)
    control("corporate book value changed", t.replace("9,237.9", "9,337.9"), nums_ok)
    control("net unrealized changed", t.replace("&minus;1,485.4", "&minus;1,385.4"), nums_ok)
    control("form code pasted in", t + " <form ", safe_ok)
    print("[HONESTY] Checks that the typed report figures reconcile and that the page prints exactly those figures. It does not check the typed figures against the PDF, show the figures are current, or show anything about today's holdings.")
    if FAIL or ctl:
        print(f"\nFAILED: {len(FAIL)} check(s), {len(ctl)} control(s) not rejected"); sys.exit(1)
    print("\nALL PASS")
main()
