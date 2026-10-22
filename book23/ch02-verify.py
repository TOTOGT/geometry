#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book23/ch02-verify.py -- the intervals on book23/ch02-what-an-hour-was.html. Run first (R24).
    python3 book23/ch02-verify.py
Standard library only. Recomputes every interval from the dates; the dates come from the sources named on the page.
  [1] each interval, in days and in hours, is recomputed and found on the page
  [2] the two small-hour figures are on the page
  [3] controls: a changed date and a changed hour count are caught
  [HONESTY] what this does not establish
"""
import re, sys
from datetime import date
from pathlib import Path
HERE = Path(__file__).resolve().parent
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def plain(t): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t))
INTERVALS = [
 ("I1", date(2020,7,16), date(2021,1,14)), ("I2", date(2020,9,9), date(2021,1,14)),
 ("I3", date(2020,12,27), date(2021,1,14)), ("I4", date(2020,12,28), date(2021,1,3)),
 ("I5", date(2021,1,4), date(2021,1,14)), ("I6", date(2021,1,8), date(2021,1,14)),
 ("I7", date(2021,1,14), date(2021,1,26)),
]
def fmt(n): return f"{n:,}"
def expected(iv): return [(k, (b-a).days, (b-a).days*24) for k, a, b in iv]
def rows_missing(text, exp):
    p = plain(text); out = []
    for k, d, h in exp:
        if not re.search(rf'data-i="{k}"[^>]*>.*?{fmt(d)}.*?{fmt(h)}', text, re.S) and not (fmt(d) in p and fmt(h) in p):
            out.append(k)
    return out
def row_ok(text, exp):
    for k, d, h in exp:
        m = re.search(rf'<tr data-i="{k}">(.*?)</tr>', text, re.S)
        if not m or fmt(d) not in plain(m.group(1)) or fmt(h) not in plain(m.group(1)): return False
    return True
p = HERE / "ch02-what-an-hour-was.html"
t = p.read_text(encoding="utf-8") if p.exists() else ""
if not t: check("ch02 exists", False)
exp = expected(INTERVALS)
print("[1] intervals"); check("all seven rows show the recomputed days and hours", bool(t) and row_ok(t, exp))
print("[2] small hours")
pt = plain(t)
check("the four-hour and 500-reais figures are on the page", "about four hours" in pt and "500 reais" in pt)
print("[3] controls")
bad_dates = [("I1", date(2020,7,17), date(2021,1,14))] + INTERVALS[1:]
check("control: a changed date is caught", bool(t) and not row_ok(t, expected(bad_dates)))
bad_h = [(k, d, h+24) for k, d, h in exp]
check("control: a changed hour count is caught", bool(t) and not row_ok(t, bad_h))
print("[HONESTY] The arithmetic is exact. Whether each date is right is the sources' question: some conflict, and the page says so.")
print("  Nothing here counts deaths or estimates harm per hour.")
print("\nFAILED: " + ", ".join(FAIL) if FAIL else "\nALL PASS")
sys.exit(1 if FAIL else 0)
