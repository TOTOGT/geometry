#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dm3_numeric.py — high-precision reproducer for the dm3 contact system.

    r' = r(1 - r^2) + 2(r - 1) e^{-z}
    th' = 1
    z' = r^2 - 2(r - 1)^2 e^{-z}

on M = R^2_+ x R, with contact form alpha = dz - r^2 dtheta.

Three things, in order:

  (1) TABLE 1 — five initial radii integrated with DOP853 at rtol = 1e-10,
      each fitted for the asymptotic transverse rate mu from log|r - 1|.
      Prediction: mu -> -2.

  (2) BASIN SCAN — bisection on r(0) for the inner boundary r*.
      Corpus value r* ~ 0.77594059. Grönwall's symmetric ball |rho| < 1/3
      would put the boundary at 0.667; it does not. The ball is a strict
      SUBSET of the basin and the basin is NOT symmetric about r = 1.

  (3) HONESTY BLOCK — what this script does and does not establish.

Requires: numpy, scipy.  Run: python3 dm3_numeric.py

Principia Orthogona - dm3 Lab - G6 LLC - CC BY-NC-ND 4.0
"""

import numpy as np
from scipy.integrate import solve_ivp

RTOL, ATOL = 1e-10, 1e-12
TMAX = 40.0


def field(t, y):
    r, th, z = y
    e = np.exp(-z)
    return [r * (1.0 - r * r) + 2.0 * (r - 1.0) * e,
            1.0,
            r * r - 2.0 * (r - 1.0) ** 2 * e]


def run(r0, z0=0.0, tmax=TMAX, rtol=RTOL):
    """Integrate from (r0, 0, z0). Returns the solution object."""
    return solve_ivp(field, (0.0, tmax), [r0, 0.0, z0],
                     method="DOP853", rtol=rtol, atol=ATOL, dense_output=True)


def converges(r0, z0=0.0, tol=1e-6):
    """Did this orbit reach the attractor Gamma = {r = 1}?"""
    s = run(r0, z0)
    if not s.success:
        return False
    rf = s.y[0, -1]
    return np.isfinite(rf) and abs(rf - 1.0) < tol


def mu_fit(r0, z0=0.0, hi=1e-5, lo=1e-9):
    """Asymptotic transverse rate: slope of log|r - 1|, fitted in a window
    chosen ADAPTIVELY rather than by a fixed time interval.

    The linearisation is
        d/dr [ r(1-r^2) + 2(r-1)e^{-z} ] |_{r=1} = -2 + 2 e^{-z},
    and z' -> 1 on Gamma, so e^{-z} -> 0 and mu -> -2 only ASYMPTOTICALLY.

    Two ways to get this wrong, and a fixed window hits one or the other
    depending on r0:
      - fit too EARLY and you measure the transient, while e^{-z} is still
        contributing and the true local rate is nowhere near -2;
      - fit too LATE and |r - 1| has reached the integrator's noise floor,
        where log of it is pure numerical junk and the fitted slope goes
        POSITIVE. An earlier version of this script used a fixed window
        (15, 30) and reported mu ~ +0.05 for exactly that reason.
        Corrected 2026-08-13.

    NOTE THE FLOOR IS NOT MACHINE EPSILON. At rtol=1e-10, atol=1e-12 the
    orbit from r0 = 0.8 sits at |r - 1| ~ 1e-10 to 1e-13 from t ~ 16
    onward, jittering in SIGN — that is accumulated integration error, six
    orders of magnitude above 2^-52. It is the same floor that stops this
    script from establishing the 8th digit of r*, and seeing it here is
    the cheapest way to understand why AXLE Issue #13 is open.

    So: keep the FIRST CONTIGUOUS run of samples with |r - 1| in [lo, hi]
    — past the transient, well above the floor — and fit only those.
    """
    s = run(r0, z0)
    t = np.linspace(0.0, TMAX, 8000)
    d = np.abs(s.sol(t)[0] - 1.0)
    idx = np.where((d < hi) & (d > lo))[0]
    if idx.size < 50:
        return np.nan, np.nan, (np.nan, np.nan)
    brk = np.where(np.diff(idx) > 1)[0]      # discard any later noise island
    if brk.size:
        idx = idx[:brk[0] + 1]
    tt, dd = t[idx], np.log(d[idx])
    slope, icept = np.polyfit(tt, dd, 1)
    resid = float(np.std(dd - (slope * tt + icept)))
    return slope, resid, (tt[0], tt[-1])


def bisect_basin(lo=0.5, hi=0.95, iters=60, z0=0.0):
    """Inner basin edge by bisection on the converges() predicate."""
    assert not converges(lo) and converges(hi), "bracket does not straddle r*"
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if converges(mid, z0):
            hi = mid
        else:
            lo = mid
    return lo, hi


if __name__ == "__main__":
    print(__doc__.split("Requires:")[0].rstrip())
    print("=" * 66)

    print("\nTABLE 1 - asymptotic transverse rate  (DOP853, rtol=%g)\n" % RTOL)
    print(f"  {'r(0)':>8} {'r(T)':>14} {'mu fitted':>12} {'resid':>9} {'fit window':>14}  status")
    print("  " + "-" * 74)
    for r0 in (0.80, 0.90, 1.00, 1.10, 1.50):
        s = run(r0)
        mu, res, win = mu_fit(r0)
        ok = "converged" if abs(s.y[0, -1] - 1.0) < 1e-6 else "DIVERGED"
        if r0 == 1.0:
            mus, rss, ws = "  (on Gamma)", "        -", "             -"
        else:
            mus, rss = f"{mu:12.6f}", f"{res:9.2e}"
            ws = f"  t={win[0]:5.2f}-{win[1]:5.2f}"
        print(f"  {r0:8.2f} {s.y[0,-1]:14.10f} {mus} {rss} {ws}  {ok}")
    print("\n  prediction: mu -> -2 as z -> infinity.  [MODEL, numerical]")
    print("  residuals ~1e-2 or below mean the decay really is a clean")
    print("  exponential over the fitted window, not a fitted curve.")

    print("\nBASIN SCAN - inner boundary r*\n")
    lo, hi = bisect_basin()
    print(f"  bracket   : [{lo:.10f}, {hi:.10f}]   width {hi-lo:.2e}")
    print(f"  r* approx : {0.5*(lo+hi):.8f}")
    print(f"  corpus    : 0.77594059")
    print(f"  Gronwall  : 1 - 1/3 = 0.66666667   (symmetric ball, conservative)")
    print(f"  outer edge: none - the basin is unbounded above r = 1")
    print("\n  The symmetric eps0 = 1/3 ball is a strict SUBSET of the basin.")
    print("  The basin is NOT symmetric about r = 1. That asymmetry is the")
    print("  pedagogical point of Session S2.")

    print("\n" + "=" * 66)
    print("""WHAT THIS ESTABLISHES, AND WHAT IT DOES NOT

  [MODEL]  mu -> -2 asymptotically. Fitted, not proved. The exact
           statement d/dr|_{r=1} = -2 + 2e^{-z} is elementary calculus;
           the LIMIT is what the fit illustrates.

  [OPEN]   r* is located, NOT bounded. This is a bisection on a numerical
           integrator: every evaluation carries truncation and rounding
           error that is ESTIMATED, not ENCLOSED. Digits beyond ~7 are not
           established by this script and should not be quoted from it.
           AXLE Issue #13.

  To convert "located" into "bounded" you need either validated interval
  integration (CAPD, Arb) or a sum-of-squares Lyapunov certificate. The
  field polynomialises under w = e^{-z} > 0:

      r' = -r^3 + 2 r w + r - 2 w
      w' = 2 r^2 w^2 - r^2 w - 4 r w^2 + 2 w^2

  which SOSTOOLS / SumOfSquares.jl accept unmodified. See Book 6, WP-62.
""")
