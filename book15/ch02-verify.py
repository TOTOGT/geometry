#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book15/ch02-verify.py -- every number on book15/ch02-what-the-count-leaves-out.html. Run first (R24).
    python3 book15/ch02-verify.py
Standard library only. No external source and no emission figures are used: the cost weights are symbols.
  [1] S_hub - S_direct = (n-1)(n-2)d, brute force over all ordered pairs
  [2] the break-even weight rho*(d) = (F_direct - F_hub) / ((n-1)(n-2)d): the hub is cheaper iff rho < rho*,
      checked against direct cost comparison on a grid of d and exact rational rho
  [3] the table on the page
  [4] where the movements land: flights touching the busiest airport
  [5] the page prints these numbers
  [HONESTY] what this does not establish
"""
import itertools, math, re, sys
from fractions import Fraction
from pathlib import Path
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)

def F_direct(n, d, s): return n*(n-1) * math.ceil(Fraction(d, s))
def F_hub(n, d, s):    return 2*(n-1) * math.ceil(Fraction((n-1)*d, s))
def S_direct(n, d):    return n*(n-1)*d
def S_hub(n, d):       return 2*(n-1)**2*d
def cost(F, S, alpha, beta): return alpha*F + beta*S
def rho_star(n, d, s):
    return Fraction(F_direct(n, d, s) - F_hub(n, d, s), (n-1)*(n-2)*d)

print("[1] extra passenger-segments of the hub, brute force (d=1)")
for n in range(3, 9):
    segs = lambda a, b: 1 if (a == 0 or b == 0) else 2
    extra = sum(segs(a, b) - 1 for a in range(n) for b in range(n) if a != b)
    check(f"n={n}: extra segments {(n-1)*(n-2)}", extra == (n-1)*(n-2))

print("[2] hub cheaper iff rho < rho*(d), where rho = beta/alpha (flights per passenger-segment)")
n, s = 50, 150
bad = 0; tested = 0
for d in range(1, 151):
    rs = rho_star(n, d, s)
    for k in range(-3, 4):
        for rho in (rs + Fraction(k, 997), Fraction(k, 3), Fraction(1, 100), Fraction(1, 1000), Fraction(0)):
            if rho < 0: continue
            tested += 1
            hub_cheaper = cost(F_hub(n,d,s), S_hub(n,d), 1, rho) < cost(F_direct(n,d,s), S_direct(n,d), 1, rho)
            pred = (F_direct(n,d,s) > F_hub(n,d,s)) and (rho < rs)
            if hub_cheaper != pred: bad += 1
check(f"{tested} (d, rho) cases agree with the closed form", bad == 0, f"{bad} disagreements")

print("[3] table, n=50, s=150")
rows = [1, 4, 20, 50, 73, 74, 77]
for d in rows:
    fd, fh = F_direct(n,d,s), F_hub(n,d,s)
    rs = rho_star(n, d, s)
    print(f"  d={d}: F_direct={fd}, F_hub={fh}, S_direct={S_direct(n,d)}, S_hub={S_hub(n,d)}, rho*={float(rs):.4f}" if fd > fh else
          f"  d={d}: F_direct={fd}, F_hub={fh}, S_direct={S_direct(n,d)}, S_hub={S_hub(n,d)}, hub never cheaper (rho* <= 0)")
check("d=4 : rho* = 2254/9408", rho_star(n, 4, s) == Fraction(2254, 9408))
check("d=73: rho* = 98/171696", rho_star(n, 73, s) == Fraction(98, 171696))
check("d=74: F tie, hub never cheaper", F_direct(n,74,s) == F_hub(n,74,s))
check("d=77: direct has fewer flights and fewer segments", F_direct(n,77,s) < F_hub(n,77,s) and S_direct(n,77) < S_hub(n,77))

print("[4] flights touching the busiest airport per day")
for d in (4, 20, 73):
    hub_airport = F_hub(n, d, s)              # every hub flight has the hub at one end
    direct_airport = 2*(n-1) * math.ceil(Fraction(d, s))   # each city: n-1 departures + n-1 arrivals
    print(f"  d={d}: hub airport {hub_airport}, each airport in the direct network {direct_airport}")
check("d=4: 196 at the hub vs 98 per airport", F_hub(n,4,s) == 196 and 2*(n-1)*math.ceil(Fraction(4,s)) == 98)
check("d=73: 2352 at the hub vs 98 per airport", F_hub(n,73,s) == 2352)

print("[5] the page prints these numbers")
page = Path(__file__).resolve().parent / "ch02-what-the-count-leaves-out.html"
if page.exists():
    t = re.sub(r"<[^>]+>", " ", page.read_text(encoding="utf-8")).replace("&minus;", "-")
    for needle in ["2,254", "9,408", "0.2396", "0.0006", "98", "196", "2,352", "(n-1)(n-2)d"]:
        check(f"page contains {needle}", needle in t)
else:
    print("  page not found next to this script; skipped")

print("[HONESTY]")
print("  alpha and beta are symbols for any per-flight and per-passenger-segment cost in one common unit.")
print("  No emission figure, fuel burn, noise level or exposure is used or implied; the chapter does not say which weight is larger.")
print("  Uniform demand, one hub, whole aircraft and a daily minimum frequency are assumed, as in chapter 1.")
sys.exit(1 if FAIL else 0)
