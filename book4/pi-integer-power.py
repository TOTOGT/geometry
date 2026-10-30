#!/usr/bin/env python3
"""pi-integer-power.py — attack 1 for book4/pi.html: is m^pi ever a whole number?

For each integer m in [2, M] this encloses m^pi in a rigorous interval (mpmath interval
arithmetic) and checks that the interval lies strictly inside (n, n+1) for some integer n.
If it does, m^pi is certified NOT an integer. If an interval ever contains an integer the
script says UNDECIDED (more precision needed); it never claims an integer hit.

    python3 book4/pi-integer-power.py [M]        (default M = 10000)

This proves the statement only for the m checked. It says nothing about larger m.
"""
import sys
from mpmath import mp, iv, floor, mpf

M = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
mp.dps = 80
iv.dps = 80
PI = iv.pi            # rigorous enclosure of pi
undecided = []
closest = []          # (distance of enclosure midpoint to nearest integer, m)
for m in range(2, M + 1):
    x = iv.mpf(m) ** PI
    lo, hi = mpf(x.a), mpf(x.b)   # enclosure of m^pi
    n = int(floor(lo))
    ok = (lo > n) and (hi < n + 1)
    if not ok:
        undecided.append(m)
        continue
    mid = (lo + hi) / 2           # plain mpf
    d = min(mid - n, n + 1 - mid)
    closest.append((d, m, n, mid))
closest.sort()
print(f"checked m = 2..{M}")
print(f"certified non-integer: {len(closest)}   undecided: {len(undecided)}")
if undecided:
    print("undecided m:", undecided[:20])
print("nearest to a whole number (distance, m, floor, m^pi):")
for d, m, n, mid in closest[:10]:
    print(f"  m={m:6d}  dist={float(d):.3e}  floor={n}  m^pi={mp.nstr(mid, 22)}")
# sanity: the two hand brackets in the chapter
for m, lo_b, hi_b in ((2, 8, 9), (3, 31, 32)):
    x = iv.mpf(m) ** PI
    print(f"hand bracket m={m}: {lo_b} < {mp.nstr(x.a,15)} .. {mp.nstr(x.b,15)} < {hi_b}: {lo_b < x.a and x.b < hi_b}")
