#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""r2_bound_check.py: producing tool for the figures on portfolio/euler-verification-example.html.
Checks r2(u) <= 4 * prod_{q = 1 mod 4, q^e || u} (e+1) for 1 <= u <= N by brute force,
where r2(u) = #{(a,b) in Z^2 : a^2+b^2 = u}. A finite sanity check, NOT a proof.
Usage: python3 tools/r2_bound_check.py [N]   (default 20000)"""
import math, sys
N = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
def mq(u):
    m, q = 1, 2
    while q * q <= u:
        e = 0
        while u % q == 0:
            u //= q; e += 1
        if e and q % 4 == 1: m *= e + 1
        q += 1
    if u > 1 and u % 4 == 1: m *= 2
    return m
viol = tight = 0
for u in range(1, N + 1):
    r = math.isqrt(u); c = 0
    for a in range(-r, r + 1):
        b2 = u - a * a; b = math.isqrt(b2)
        if b * b == b2: c += 1 if b == 0 else 2
    if c > 4 * mq(u): viol += 1
    if c == 4 * mq(u): tight += 1
print(f"u <= {N}: violations {viol}, equality (tight) in {tight}")
