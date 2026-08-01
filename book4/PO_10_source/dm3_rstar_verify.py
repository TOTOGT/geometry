#!/usr/bin/env python3
"""
dm3 inner-basin threshold r* — independent verification.

System (PO_10 abstract, eq. 1):
    r' = r(1 - r^2) + eps*(r-1)*exp(-z)
    th' = 1
    z' = r^2 - eps*(r-1)^2*exp(-z)

FINDING: eps and z0 enter only through lambda = eps*exp(-z0).
    lambda = 2  ->  r* = 0.775941   (eps=2, z0=0)      <- the 0.77594059 in the corpus
    lambda = 1  ->  r* = 0.572235   (eps=2, z0=log 2)  <- the abstract's stated hypothesis
The value 0.80 printed in PO_10_Pablo_Grossi.pdf matches no lambda in play.

Run: python3 dm3_rstar_verify.py
"""
import numpy as np
from scipy.integrate import solve_ivp


def rhs(eps):
    def f(t, s):
        r, th, z = s
        e = np.exp(-z)
        return [r * (1 - r * r) + eps * (r - 1) * e,
                1.0,
                r * r - eps * (r - 1) ** 2 * e]
    return f


def converges(r0, z0, eps, T=40.0):
    ev = lambda t, s: s[0] - 1e-6
    ev.terminal, ev.direction = True, -1
    sol = solve_ivp(rhs(eps), (0, T), [r0, 0.0, z0], method='DOP853',
                    rtol=1e-10, atol=1e-12, events=ev)
    return sol.t_events[0].size == 0 and abs(sol.y[0, -1] - 1) < 1e-6


def rstar(z0, eps, iters=55):
    lo, hi = 0.001, 1.0
    if converges(lo, z0, eps):
        return None
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if converges(mid, z0, eps):
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


if __name__ == '__main__':
    print("scaling law: r* depends on (eps, z0) only through lambda = eps*exp(-z0)\n")
    print(" lambda    r*          spread over (eps=1,2,4)")
    for lam in (0.5, 1.0, 2.0, 3.0):
        vals = [rstar(np.log(eps / lam), eps) for eps in (1.0, 2.0, 4.0)]
        print(f" {lam:5.2f}    {vals[0]:.6f}    {max(vals) - min(vals):.1e}")

    print("\nagainst the two circulating values:")
    print(f"  corpus 0.77594059  ->  lambda=2, i.e. eps=2 with z0=0     : {rstar(0.0, 2.0):.8f}")
    print(f"  abstract z(0)>=log2 ->  lambda=1, i.e. eps=2 with z0=log2 : {rstar(np.log(2), 2.0):.8f}")
    print("  PDF 0.80            ->  matches no lambda in play")
