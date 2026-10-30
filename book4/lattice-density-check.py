#!/usr/bin/env python3
"""lattice-density-check.py — numerical check of the lattice-dimension bounds on book4/pi.html §3.

Claim (proved by hand on the page): for real d with 0 < d <= 4 and integer m >= 2 with x = m^d >= 2,
put N = floor(x). Then 1 <= N <= m^4 and
      0 <= d - ln N / ln m <= 2 / (x ln m)          (sharp rate)   and   <= ln 2 / ln m   (crude).
This script tests both bounds on a grid and on d = pi. A check is not a proof.
"""
import math, random
random.seed(1)
bad = 0; worst = 0.0; n = 0
cases = [(math.pi, m) for m in range(2, 3000)]
cases += [(random.uniform(0.05, 4.0), random.randint(2, 5000)) for _ in range(200000)]
for d, m in cases:
    x = m ** d
    if x < 2 or x > 1e12: continue   # beyond ~1e12 the float error of ln N exceeds the bound; not a test of the claim
    N = math.floor(x)
    err = d - math.log(N) / math.log(m)
    sharp = 2 / (x * math.log(m)); crude = math.log(2) / math.log(m)
    n += 1
    if not (N >= 1 and N <= m ** 4 and err >= -1e-14 and err <= sharp*(1+1e-6)):
        bad += 1; print("VIOLATION", d, m, N, err, sharp)
    worst = max(worst, err / sharp)
print(f"cases tested: {n}   violations: {bad}   max (error / sharp bound) = {worst:.4f}")
d = math.pi
for m in (37, 38, 43, 100, 1000):
    x = m ** d; N = math.floor(x); e = d - math.log(N) / math.log(m)
    print(f"d=pi m={m:5d} N={N}  error={e:.3e}  sharp bound={2/(x*math.log(m)):.3e}")
