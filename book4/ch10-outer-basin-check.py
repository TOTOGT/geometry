#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Book 4 chapter 10, "Helical attractor (outer basin)": the statement reads "for all initial conditions with r(0) > 1 ...
r(t) -> 1". This script tests it on the chapter's own system (epsilon = 2):
    r' = r(1 - r^2) + 2 (r - 1) e^(-z),   z' = r^2 - 2 (r - 1)^2 e^(-z).
For each r(0) > 1 it finds the smallest z(0) from which the orbit converges to r = 1 (bisection, RK4, fixed step), and for
z(0) = 0 the largest r(0) that still converges. Blow-up means z falls without bound in finite time while r grows.
Cross-checked outside this script with scipy DOP853 and Radau (adaptive steps collapse at the same starts)."""
import math
def f(r, z):
    e = math.exp(min(-z, 700.0))
    return r * (1 - r * r) + 2 * (r - 1) * e, r * r - 2 * (r - 1) ** 2 * e
def conv(r, z, T=60.0, dt=0.01):
    try:
        for _ in range(int(T / dt)):
            if r > 1e3 or z < -60 or r != r: return False
            a1, b1 = f(r, z); a2, b2 = f(r + dt / 2 * a1, z + dt / 2 * b1)
            a3, b3 = f(r + dt / 2 * a2, z + dt / 2 * b2); a4, b4 = f(r + dt * a3, z + dt * b3)
            r += dt / 6 * (a1 + 2 * a2 + 2 * a3 + a4); z += dt / 6 * (b1 + 2 * b2 + 2 * b3 + b4)
    except (OverflowError, ValueError):
        return False
    return abs(r - 1) < 1e-2
def zmin(r0, lo=-6.0, hi=0.0):
    if not conv(r0, hi): return None
    if conv(r0, lo): return lo
    for _ in range(30):
        mid = (lo + hi) / 2
        if conv(r0, mid): hi = mid
        else: lo = mid
    return hi
def rmax_at_zero(lo=3.0, hi=40.0):
    if not conv(lo, 0.0) or conv(hi, 0.0): return None
    for _ in range(30):
        mid = (lo + hi) / 2
        if conv(mid, 0.0): lo = mid
        else: hi = mid
    return lo
def main():
    print(' r(0)    smallest z(0) from which the orbit converges')
    rows = []
    for r0 in (1.001, 1.01, 1.1, 1.5, 2.0, 3.0, 5.0):
        z = zmin(r0); rows.append((r0, z)); print(f' {r0:6.3f}   {z:8.4f}')
    rm = rmax_at_zero(); print(f'at z(0) = 0 the largest r(0) that converges: {rm:.4f}')
    counter = [(1.5, -2.0), (2.0, -1.0), (1.001, -3.0), (8.0, 0.0), (10.0, 0.0)]
    bad = [(r, z) for r, z in counter if not conv(r, z)]
    print('starts with r(0) > 1 that do NOT converge (statement as written has no z(0) or r(0) bound):', bad)
    chapter_ok = all(conv(r, 0.0) for r in (1.001, 1.5, 2.0, 3.0))
    print('the chapter\'s numerical evidence (z(0) = 0, r(0) up to 3.0) reproduces:', chapter_ok)
    print('ALL CHECKS PASSED' if chapter_ok and len(bad) == len(counter) and rm and 5 < rm < 10 else 'CHECK FAILED')
main()
