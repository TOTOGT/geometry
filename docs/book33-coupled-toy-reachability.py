#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Book 33 planning: reachability in the coupled dm3 toy (epsilon = 2, Book 4 chapter 10):
    r' = r(1 - r^2) + 2 (r - 1) e^(-z),     z' = r^2 - 2 (r - 1)^2 e^(-z).
Question (Pablo, 2026-10-02): does anything lead from the cycle's side back to the repeller side, so that "the head
reaches the tail's end"? Method: classify forward orbits by start (r0, z0): converge to Gamma (r -> 1), or escape (r -> 0).
Both outcome sets are forward invariant by definition, so a start in one cannot reach the other; the live question is how
the two sets sit relative to Gamma, as a function of z0. Standard library only; RK4, fixed step."""
import math
def f(r, z):
    e = math.exp(min(-z, 700.0))
    return r * (1 - r * r) + 2 * (r - 1) * e, r * r - 2 * (r - 1) ** 2 * e
def run(r, z, T=40.0, dt=0.02):
    try:
        for _ in range(int(T / dt)):
            if r < 0.02: return 'escape'
            if r > 1e3 or z < -60 or r != r: return 'blowup'
            a1, b1 = f(r, z); a2, b2 = f(r + dt / 2 * a1, z + dt / 2 * b1)
            a3, b3 = f(r + dt / 2 * a2, z + dt / 2 * b2); a4, b4 = f(r + dt * a3, z + dt * b3)
            r += dt / 6 * (a1 + 2 * a2 + 2 * a3 + a4); z += dt / 6 * (b1 + 2 * b2 + 2 * b3 + b4)
    except (OverflowError, ValueError):
        return 'blowup'
    return 'converge' if abs(r - 1) < 1e-2 else f'other(r={r:.3f})'
def lower_edge(z0, lo=0.05, hi=1.0):
    """smallest r0 in (0.05, 1] that converges, by bisection, assuming escape below and converge above"""
    if run(hi, z0) != 'converge': return None
    if run(lo, z0) == 'converge': return lo
    for _ in range(40):
        mid = (lo + hi) / 2
        if run(mid, z0) == 'converge': hi = mid
        else: lo = mid
    return hi
def main():
    ok = True
    r0 = lower_edge(0.0)
    print(f'z0 = 0: inner boundary r* = {r0:.6f} (chapter value 0.77594058)'); ok &= abs(r0 - 0.77594058) < 1e-4
    print(' z0     inner boundary r*(z0)   start on Gamma (r0=1)   r0=1+-0.001')
    flags = []
    for z0 in [-4.0, -3.0, -2.5, -2.0, -1.5] + [i * 0.1 for i in range(-10, 21)]:
        e = lower_edge(z0)
        g = run(1.0, z0); n1, n2 = run(0.999, z0), run(1.001, z0)
        print(f' {z0:5.1f}   {"none" if e is None else f"{e:.6f}":>20}   {g:>20}   {n1}/{n2}')
        flags.append((z0, e, g, n1, n2))
    gamma_stays = all(g == 'converge' for _, _, g, _, _ in flags)
    near_escape = [z for z, e, g, a, b in flags if a != 'converge' or b != 'converge']
    print('orbits starting exactly on Gamma stay on Gamma for every z0 tested:', gamma_stays)
    print('z0 values where a start within 0.001 of Gamma does NOT converge (either side):', near_escape if near_escape else 'none')
    mx = max(e for _, e, _, _, _ in flags if e is not None)
    print(f'largest inner boundary over the z0 range: {mx:.4f} (displacement from Gamma {1 - mx:.4f})')
    edges = [(z, e) for z, e, *_ in flags if e is not None]
    mono = all(e1 >= e2 - 1e-9 for (z1, e1), (z2, e2) in zip(sorted(edges), sorted(edges)[1:]))
    pinch = [z for z, e, g, a, b in flags if a != 'converge' and b != 'converge']
    print('inner boundary is non-increasing in z0 over the scan (it rises toward 1 as z0 falls):', mono)
    print('z0 where BOTH sides of Gamma (r0 = 1 -+ 0.001) leave Gamma (basin pinched to the cycle):', pinch)
    # on Gamma itself z increases without bound: z' = 1 at r = 1, so the lift of Gamma never returns to an earlier z
    print('on Gamma, z\' = r^2 - 0 = 1 > 0: the lifted cycle is a helix in (angle, z), not a closed ring in the full state')
    ok &= mono and len(pinch) > 0
    print('ALL CHECKS PASSED' if ok and gamma_stays else 'CHECK FAILED')
main()
