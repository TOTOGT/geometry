#!/usr/bin/env python3
"""pi-verify.py — checks behind book4/pi.html (Chapter 3½).
    python3 book4/pi-verify.py
Everything here is arithmetic or a count; none of it proves the dimension theorems quoted on the page.
"""
import math
from fractions import Fraction

PI = math.pi
s = PI - 3
print("1. the construction")
r = 2 ** (-1 / s)
print(f"   s = pi-3 = {s:.10f}")
print(f"   r = 2^(-1/s) = {r:.10f}   (1/r = {1/r:.4f})")
print(f"   similarity dim of the 2-piece Cantor set = log2/log(1/r) = {math.log(2)/math.log(1/r):.12f}  (s = {s:.12f})")
print(f"   Moran sum 2*r^s = {2*r**s:.12f}  (must be 1)")
print(f"   pieces [0,r] and [1-r,1] are disjoint iff r < 1/2: r = {r:.6f} -> {r < 0.5}")
print(f"   times R^3: dimension s + 3 = {s+3:.12f} vs pi = {PI:.12f}; container R^4 needs dim <= 4: {s+3 <= 4}")

print("\n2. the lattice route: equal ratios 1/m, N pieces kept out of m^4 cells of the unit 4-cube")
print("   d = log N / log m, any integer N <= m^4. Closest to pi for each m (N = round(m^pi), capped at m^4):")
best = []
for m in range(2, 61):
    N = min(round(m ** PI), m ** 4)
    d = math.log(N) / math.log(m)
    best.append((abs(d - PI), m, N, d))
best.sort()
for err, m, N, d in best[:8]:
    print(f"   m={m:3d}  N={N:9d}  d={d:.6f}  error {err:.2e}")
print("   -> lattice sets come as close to pi as you like with enough pieces, but each is a rational-log value;")
print("      whether log N / log m can equal pi exactly (m^pi an integer) is not settled by this check.")

print("\n3. box counting on the level-k Cantor set C_s (scale between levels shows the lacunary wobble)")
K = 6
# level-k intervals have length r^k, 2^k of them; left endpoints by recursion
pts = [0.0]
for k in range(K):
    step = (1 - r) * r ** k
    pts = pts + [p + step for p in pts]
length = r ** K
def boxes(eps):
    return len({math.floor(p / eps) for p in pts} | {math.floor((p + length) / eps) for p in pts})
rows = []
for j in range(1, 11):
    eps = 10.0 ** (-j)
    if eps < length * 2: break
    n = boxes(eps)
    rows.append((eps, n))
    print(f"   eps=1e-{j:<2d} boxes={n:4d}  log N/log(1/eps)={math.log(n)/math.log(1/eps):.4f}")
# slope between level-aligned scales is exact s; between decades it wobbles
xs = [math.log(1/e) for e, n in rows]; ys = [math.log(n) for e, n in rows]
mx = sum(xs)/len(xs); my = sum(ys)/len(ys)
slope = sum((x-mx)*(y-my) for x, y in zip(xs, ys)) / sum((x-mx)**2 for x in xs)
print(f"   regression slope over these decades = {slope:.4f}  (target s = {s:.4f}; finite range, a wobbly estimate)")
for k in range(0, K+1):
    n = 2 ** k; e = r ** k
    print(f"   level {k}: eps=r^{k}={e:.3e} N={n:3d} exact log N/log(1/eps)={math.log(n)/math.log(1/e) if k else 0:.6f}")

print("\n4. other target dimensions d in (3,4): s = d-3, r = 2^(-1/s)")
for d in (3.1, 3.25, 3.5, PI, 3.9):
    ss = d - 3
    rr = 2 ** (-1 / ss)
    print(f"   d={d:.5f}  s={ss:.5f}  r={rr:.6g}  disjoint(r<1/2)={rr < 0.5}")
print("\n5. plane analogue C_s x R (container R^2): dimension 1+s =", f"{1+s:.6f}")
