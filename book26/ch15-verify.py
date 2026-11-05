#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""book26/ch15-verify.py -- book26/ch15-a-fair-price-for-a-resource.html. Exact-fraction arithmetic on INVENTED firms.
[1] rent  [2] levy vs share  [3] dividend and incidence  [4] numbers found on the page  [5] controls  [6] honesty. Standard library only."""
import html as _h, re
from fractions import Fraction as F
from pathlib import Path
PAGE = Path(__file__).resolve().parent / "ch15-a-fair-price-for-a-resource.html"
FAIL = []
def check(l, ok, d=""):
    print(("PASS " if ok else "FAIL ") + l + (f"  -- {d}" if d else ""))
    if not ok: FAIL.append(l)
raw = PAGE.read_text(encoding="utf-8")
txt = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", raw, flags=re.S)
txt = re.sub(r"\s+", " ", _h.unescape(re.sub(r"<[^>]+>", " ", txt)))
rent = lambda R, C, K, r: R - C - r * K
r = F(1, 10); K = 200
A = rent(100, 60, K, r); B = rent(100, 78, K, r)
check("rent A = 20, rent B = 2", (A, B) == (20, 2), f"{A},{B}")
g = F(5, 100) * 100
check("levy 5% of revenue = 5 for both", g == 5)
check("levy is 25% of A's rent and 250% of B's", (g / A, g / B) == (F(1, 4), F(5, 2)))
check("A viable after levy (15), B not (-3)", (A - g, B - g) == (15, -3))
s = F(2, 5)
check("40% share: A pays 8, B pays 4/5; both keep rent above required return",
      (s * A, s * B) == (8, F(4, 5)) and ((1 - s) * A, (1 - s) * B) == (12, F(6, 5)))
check("cost saving of 1 keeps 1-s: 0.6 at s=40%, 0 at s=100%", (1 - s, 1 - F(1)) == (F(3, 5), 0))
T, N = 1_000_000_000, 20_000_000
check("equal dividend = 50 each", F(T, N) == 50)
v = [10, 30, 60]; T3 = 300
prop = [F(T3 * x, sum(v)) for x in v]
check("by value: 30, 90, 180; equal share 100; top/bottom = 6", prop == [30, 90, 180] and F(T3, 3) == 100 and prop[2] / prop[0] == 6)
th = F(1, 2)
check("incidence theta=0.5: firm 150, users 150, net transfer 150; theta=1 gives 0",
      (T3 * (1 - th), T3 * th, T3 * (1 - th)) == (150, 150, 150) and T3 * (1 - 1) == 0)
for x in ["20", "250%", "25%", "-3", "0.6", "1,000,000,000", "20,000,000", "180", "S6102", "A09112", "5% of gross income"]:
    check(f"page carries {x}", x.replace("-", "&minus;") in raw or x in txt or x in raw)
check("control: Firm B with cost 70 would survive the 5% levy", rent(100, 70, K, r) - g > 0)
check("control: share of 100% leaves no cost-cutting incentive but 40% does", (1 - F(1)) == 0 and (1 - s) > 0)
check("honesty: says every figure is invented", "invented" in txt)
check("honesty: says 31% to 83% was not traced", "not traced" in txt)
check("honesty: not tax or legal advice", "not tax or legal advice" in txt.lower())
print("ALL PASS" if not FAIL else f"FAILED: {len(FAIL)}")
raise SystemExit(1 if FAIL else 0)
