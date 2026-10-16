#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book15/ch03-verify.py -- every number on book15/ch03-thirty-days.html. Run first (R24).
    python3 book15/ch03-verify.py
Standard library only. The rule counted is CLT art. 134 par. 1 as stated by a secondary source
(barbieriadvogados.com, read 2026-10-16): up to three periods, one of at least 14 calendar days,
each other of at least 5. The statute text itself has NOT been read; check it before citing.
  [1] ordered splits of an entitlement of D days, by brute force
  [2] closed forms for D = 30 (inclusion-exclusion), against the brute force
  [3] the four entitlements of art. 130 (30, 24, 18, 12 days)
  [4] person-days and the even-spread share of covered workers on vacation on a given day
  [5] the page prints these numbers
  [HONESTY] what this does not establish
"""
import itertools, re, sys
from math import comb
from pathlib import Path
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)

def splits(D, k):
    """ordered k-tuples of positive ints summing to D, each >= 5, at least one >= 14"""
    out = []
    def rec(prefix, left, parts):
        if parts == 1:
            if left >= 5: out.append(tuple(prefix) + (left,))
            return
        for x in range(5, left - 5 * (parts - 1) + 1):
            rec(prefix + [x], left - x, parts - 1)
    rec([], D, k)
    if k == 1: return out            # unsplit: the 14-day minimum applies only when the vacation is split
    return [t for t in out if max(t) >= 14]
def count(D): return {k: len(splits(D, k)) for k in (1, 2, 3)}

print("[1] brute force, D = 30")
c30 = count(30)
print("  one period:", c30[1], " two periods:", c30[2], " three periods:", c30[3], " total:", sum(c30.values()))
check("30 days: 1 + 21 + 84 = 106", (c30[1], c30[2], c30[3]) == (1, 21, 84) and sum(c30.values()) == 106)

print("[2] closed form for three periods, D = 30")
# each part >= 5: subtract 5 from each, sum 15 over 3 parts; at least one part >= 14 means not all parts <= 13, i.e. not all reduced parts <= 8
all_ge5 = comb(15 + 2, 2)                                   # 136
all_le13 = comb(17, 2) - 3 * comb(17 - 9, 2) + 3 * comb(max(17 - 18, 0), 2)  # inclusion-exclusion, last term 0
print(f"  each part >= 5: {all_ge5}; of those with every part <= 13: {all_le13}; so {all_ge5 - all_le13}")
check("84 = 136 - 52", all_ge5 == 136 and all_le13 == 52 and all_ge5 - all_le13 == 84 == c30[3])
check("two periods: parts 5..25, one of them >= 15 >= 14 always, so 21", c30[2] == 21 == 25 - 5 + 1)

print("[3] entitlements of art. 130")
for D in (30, 24, 18, 12):
    c = count(D)
    print(f"  {D} days: one {c[1]}, two {c[2]}, three {c[3]}, total {sum(c.values())}")
check("24 days: 1 + 12 + 3 = 16 (three periods only as 14+5+5 in some order)", count(24) == {1: 1, 2: 12, 3: 3})
check("18 days: only the unsplit period", count(18) == {1: 1, 2: 0, 3: 0})
check("12 days: only the unsplit period", count(12) == {1: 1, 2: 0, 3: 0})

print("[4] person-days and share on vacation, even spread over a 365-day year")
share = 30 / 365
print(f"  one covered worker with 30 days: 30 person-days a year; on any one day, on average {share:.4f} of covered workers on vacation (30/365)")
check("30/365 = 0.0822", round(share, 4) == 0.0822)
print(f"  if everyone's vacation were in one 30-day month: share on that month's days = 1.0000, a factor of {365/30:.2f} over the even spread")
check("peak factor 365/30 = 12.17", round(365/30, 2) == 12.17)

print("[5] the page prints these numbers")
page = Path(__file__).resolve().parent / "ch03-thirty-days.html"
if page.exists():
    t = re.sub(r"<[^>]+>", " ", page.read_text(encoding="utf-8"))
    for needle in ["106", "84", "21", "136", "52", "0.0822", "12.17", "16"]:
        check(f"page contains {needle}", needle in t)
else:
    print("  page not found next to this script; skipped")

print("[HONESTY]")
print("  This counts legal ways to split an entitlement. It does not say how many people hold one, when they take it,")
print("  whether they travel, or what they spend. No population, survey or tourism figure is used.")
print("  The rule is taken from a secondary source; the statute text has not been read.")
sys.exit(1 if FAIL else 0)
