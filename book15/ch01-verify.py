#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book15/ch01-verify.py -- every number on book15/ch01-hubs-and-spokes.html. Run first (R24).
    python3 book15/ch01-verify.py
Standard library only. No external source is used: the chapter is counting, derived here.
  [1] route counts: complete network n(n-1)/2 vs hub n-1, by brute-force enumeration for small n
  [2] segment counts: brute force over all ordered pairs, against 2(n-1)^2 (hub) and n(n-1) (direct)
  [3] load per route per direction, brute force, against d and (n-1)d
  [4] the toy flight model: n=50, d=4, s=150, and the smallest d where direct is no worse than hub
  [5] the page prints exactly these numbers
  [HONESTY] what this does not establish
"""
import itertools, math, re, sys
from pathlib import Path
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)

# model: cities 0..n-1, city 0 is the hub. d passengers per ordered pair per day.
def direct_routes(n): return {frozenset(p) for p in itertools.combinations(range(n), 2)}
def hub_routes(n): return {frozenset((0, i)) for i in range(1, n)}
def path_hub(a, b):
    if a == 0 or b == 0: return [(a, b)]
    return [(a, 0), (0, b)]

print("[1] route counts")
for n in range(2, 9):
    check(f"n={n}: direct {n*(n-1)//2}, hub {n-1}",
          len(direct_routes(n)) == n*(n-1)//2 and len(hub_routes(n)) == n-1)
print("  n=50:", 50*49//2, "direct routes vs", 49, "hub routes")

print("[2] segments flown per day by passengers (d=1 per ordered pair), brute force")
for n in range(2, 9):
    pairs = [(a, b) for a in range(n) for b in range(n) if a != b]
    seg_direct = len(pairs)
    seg_hub = sum(len(path_hub(a, b)) for a, b in pairs)
    check(f"n={n}: direct {n*(n-1)}, hub {2*(n-1)**2}", seg_direct == n*(n-1) and seg_hub == 2*(n-1)**2)
n = 50
print(f"  n=50: direct {n*(n-1)}, hub {2*(n-1)**2}, ratio hub/direct = {2*(n-1)**2/(n*(n-1)):.4f} = 2(n-1)/n")

print("[3] load on one route in one direction (passengers/day, d=1)")
for n in range(3, 9):
    load = {}
    for a in range(n):
        for b in range(n):
            if a != b:
                for seg in path_hub(a, b):
                    load[seg] = load.get(seg, 0) + 1
    out_spoke = load[(1, 0)]
    check(f"n={n}: spoke 1->hub carries {n-1} (direct route carries 1)", out_spoke == n-1)

print("[4] toy flight model: s seats per flight, one flight per direction per route per day at minimum")
n, d, s = 50, 4, 150
def flights_direct(n, d, s): return n*(n-1) * math.ceil(d/s)
def flights_hub(n, d, s): return 2*(n-1) * math.ceil((n-1)*d/s)
fd, fh = flights_direct(n, d, s), flights_hub(n, d, s)
print(f"  n={n}, d={d}, s={s}: direct {fd} flights/day (average load {d/s:.4f}); "
      f"hub {fh} flights/day (average load {(n-1)*d/(math.ceil((n-1)*d/s)*s):.4f})")
check("direct 2450 flights, hub 196 flights", fd == 2450 and fh == 196)
tie = next(dd for dd in range(1, 151) if flights_direct(n, dd, s) <= flights_hub(n, dd, s))
strict = next(dd for dd in range(1, 151) if flights_direct(n, dd, s) < flights_hub(n, dd, s))
print(f"  hub strictly fewer flights for d <= {tie-1}; tie (2450 each) for d = {tie}..{strict-1}; direct strictly fewer from d = {strict}")
print(f"  at d={tie-1}: direct {flights_direct(n,tie-1,s)} vs hub {flights_hub(n,tie-1,s)}; at d={strict-1}: {flights_direct(n,strict-1,s)} vs {flights_hub(n,strict-1,s)}; at d={strict}: {flights_direct(n,strict,s)} vs {flights_hub(n,strict,s)}")
check("hub wins to d=73, tie 74-76, direct wins from d=77", (tie, strict) == (74, 77) and flights_hub(n, 73, s) == 2352 and flights_hub(n, 77, s) == 2548)

print("[5] the page prints these numbers")
page = Path(__file__).resolve().parent / "ch01-hubs-and-spokes.html"
if page.exists():
    t = re.sub(r"<[^>]+>", " ", page.read_text(encoding="utf-8"))
    t = t.replace("&minus;", "-").replace("&nbsp;", " ")
    for needle in ["1,225", "49", "2,450", "4,802", "1.96", "196", "2,548", "2,352", "73", "74", "77"]:
        check(f"page contains {needle}", needle in t)
else:
    print("  page not found next to this script; skipped")

print("[HONESTY]")
print("  This is a counting model with uniform demand, one hub, and a stated minimum-frequency rule.")
print("  It uses no airline data and prices nothing: no fares, fuel, aircraft, slots, or connection time.")
print("  It does not show that any real carrier should use either network.")
sys.exit(1 if FAIL else 0)
