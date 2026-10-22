#!/usr/bin/env python3
"""Numeric cross-check for NbonacciLimit.lean (2026-10-22).
Checks, for k=2..40, the facts the Lean file claims, using exact rational
bisection (Fraction). This is NOT a proof; it is a sanity check that the
statements are not false. The Lean file is UNTESTED until run by Pablo.
Facts: root eta in (3/2, 2); eta^k*(2-eta)=1 (to tolerance); 2-eta <= (2/3)^k;
gap shrinks with k. Control: a damaged claim (2-eta <= (1/2)^k) must be rejected.
"""
import sys
from fractions import Fraction as F

def f(x, k):            # x^k (2-x) - 1
    return x**k * (2 - x) - 1

def root(k, steps=200):
    lo, hi = F(3, 2), F(2)          # f(3/2)>0, f(2)=-1<0
    assert f(lo, k) > 0 and f(hi, k) < 0
    for _ in range(steps):
        mid = (lo + hi) / 2
        if f(mid, k) > 0: lo = mid
        else: hi = mid
    return lo

def check(bound_base):
    prev_gap = None
    for k in range(2, 41):
        e = root(k)
        gap = 2 - e
        if not (F(3, 2) < e < 2): return f"k={k}: root outside (3/2,2)"
        if abs(f(e, k)) > F(1, 10**30): return f"k={k}: equation residual too big"
        if gap > bound_base**k: return f"k={k}: gap {float(gap):.3e} > bound {float(bound_base**k):.3e}"
        if prev_gap is not None and gap >= prev_gap: return f"k={k}: gap not shrinking"
        prev_gap = gap
    return None

real = check(F(2, 3))
ctrl = check(F(1, 2))        # false claim; must be rejected
print("claim 2-eta<=(2/3)^k, k=2..40:", "OK" if real is None else "FAIL " + real)
print("negative control (2-eta<=(1/2)^k):", "rejected as it must be" if ctrl else "NOT rejected -> check is blind")
print("eta_2..eta_6 =", [round(float(root(k)), 4) for k in range(2, 7)])
sys.exit(0 if (real is None and ctrl) else 1)
