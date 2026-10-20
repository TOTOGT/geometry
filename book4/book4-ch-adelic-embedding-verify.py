"""Checks for Book 4, Ch 14A (GTCT-Adelic Embedding Conjecture), editor's note 2026-10-19.

Check 1 (Obligation 2): the formal statement phi*(g) = r^2 needs g >= 0, since r is real.
  g(sigma, t) = -Im(zeta'/zeta(sigma + i t)). The check FAILS the obligation if g < 0
  at any sampled point. On sigma = 1/2, g = Z'/Z (Hardy Z), which runs from +inf to -inf
  between consecutive zeros, so negative values are expected there.

Check 2 (Obligation 3): the commutator of two finite square matrices has trace 0,
  so it can never equal c * I with c != 0. A "scalar commutator = -6" on a 3-site
  ring must therefore mean one entry, or the commutator applied to a particular state.

Checks 3-6 (added 2026-10-19 with the correction in rh-paper.html section 4.9):
  3. dt g changes sign for sigma > 1/2, including sigma > 1 where zeta has no zeros.
  4. On sigma = 1/2, the xi version keeps one sign (first Laguerre inequality).
  5. Re(xi'/xi) > 0 for Re s > 1/2 on a grid (Lagarias 1999: equivalent to RH).
  6. Each local factor g_p is periodic with mean zero, so dt g_p changes sign too.

Requires: mpmath, numpy.  Run: python3 book4-ch-adelic-embedding-verify.py
"""
import mpmath as mp
import numpy as np

mp.mp.dps = 20


def g(sigma, t):
    s = mp.mpc(sigma, t)
    return -mp.im(mp.zeta(s, derivative=1) / mp.zeta(s))


def check_obligation2(sigmas=(0.5, 0.7, 2.0), t_max=60.0, step=0.05):
    ts = [k * step for k in range(2, int(t_max / step) + 1)]
    results = {}
    for sigma in sigmas:
        vals = [g(sigma, t) for t in ts]
        neg = sum(1 for v in vals if v < 0)
        results[sigma] = (neg, len(vals), float(min(vals)), float(max(vals)))
        print(f"sigma={sigma}: g<0 at {neg}/{len(vals)} samples, t in [{ts[0]:.2f},{t_max}]; "
              f"min={float(min(vals)):.2f} max={float(max(vals)):.2f}")
    return results


def check_trace_zero(trials=1000, n=3, seed=0):
    rng = np.random.default_rng(seed)
    worst = 0.0
    for _ in range(trials):
        a, b = rng.standard_normal((n, n)), rng.standard_normal((n, n))
        worst = max(worst, abs(np.trace(a @ b - b @ a)))
    print(f"max |trace([A,B])| over {trials} random {n}x{n} pairs: {worst:.2e}")
    # tr(c I) = n c, so [A,B] = -6 I would need trace -18 on a 3-site ring
    print(f"trace needed for [A,B] = -6*I on {n} sites: {-6 * n}")
    return worst


def xi_logderiv(s):
    """xi'/xi for xi(s) = 1/2 s(s-1) pi^(-s/2) Gamma(s/2) zeta(s)."""
    return (1 / s + 1 / (s - 1) - mp.log(mp.pi) / 2 + mp.digamma(s / 2) / 2
            + mp.zeta(s, derivative=1) / mp.zeta(s))


def _dt(f, sigma, t, h=mp.mpf("1e-6")):
    return (f(sigma, t + h) - f(sigma, t - h)) / (2 * h)


def sign_changes(vals):
    return sum(1 for a, b in zip(vals, vals[1:]) if (a > 0) != (b > 0))


def check_dtg_sign_changes(sigmas=(0.6, 0.75, 1.0, 2.0, 3.0), t_max=60.0, step=0.05):
    """Check 3: dt g changes sign at sigma > 1/2, including sigma > 1 (no zeros of zeta there)."""
    ts = [0.1 + k * step for k in range(int((t_max - 0.1) / step))]
    out = {}
    for sigma in sigmas:
        v = [_dt(g, sigma, t) for t in ts]
        out[sigma] = sign_changes(v)
        print(f"sigma={sigma}: {out[sigma]} sign changes of dt g")
    return out


def check_xi_on_line(t_max=60.0, step=0.05, avoid=0.03):
    """Check 4: on sigma = 1/2, dt(-Im xi'/xi) keeps one sign (first Laguerre inequality)."""
    zeros = [float(mp.zetazero(k).imag) for k in range(1, 20) if mp.zetazero(k).imag < t_max + 1]
    gx = lambda sigma, t: -mp.im(xi_logderiv(mp.mpc(sigma, t)))
    ts = [0.1 + k * step for k in range(int((t_max - 0.1) / step))
          if min(abs(0.1 + k * step - z) for z in zeros) > avoid]
    v = [_dt(gx, 0.5, t) for t in ts]
    n_pos = sum(1 for x in v if x > 0)
    print(f"sigma=1/2, xi version: {sign_changes(v)} sign changes, positive at {n_pos}/{len(v)}")
    return n_pos


def check_lagarias(sigmas=(0.51, 0.6, 0.75, 1.0, 2.0), t_max=60.0, step=0.25):
    """Check 5: Re(xi'/xi) > 0 for Re s > 1/2 (Lagarias 1999, equivalent to RH) on this grid."""
    ts = [0.1 + k * step for k in range(int((t_max - 0.1) / step))]
    worst = min(float(min(mp.re(xi_logderiv(mp.mpc(s, t))) for t in ts)) for s in sigmas)
    print(f"min Re(xi'/xi) over grid: {worst:.4g}")
    return worst


def check_prime_factors(primes=(2, 3, 5, 7), sigmas=(0.5, 0.75, 2.0)):
    """Check 6: each Euler-product local factor g_p is periodic in t (period 2 pi / log p)
    with mean zero, so dt g_p also changes sign. A prime-by-prime version of the
    non-vanishing condition therefore fails for every p, at every sigma."""
    for p in primes:
        lp = mp.log(p)
        for sigma in sigmas:
            gp = lambda s, t: lp * p ** (-s) * mp.sin(t * lp) / (1 - 2 * p ** (-s) * mp.cos(t * lp) + p ** (-2 * s))
            period = 2 * mp.pi / lp
            ts = [period * k / 400 for k in range(401)]
            v = [_dt(gp, sigma, t) for t in ts]
            mean = mp.quad(lambda t: gp(sigma, t), [0, period]) / period
            print(f"p={p} sigma={sigma}: {sign_changes(v)} sign changes of dt g_p per period, "
                  f"mean of g_p = {float(mean):.1e}")


if __name__ == "__main__":
    print("Check 1: Obligation 2, phi*(g) = r^2 requires g >= 0")
    res = check_obligation2()
    any_negative = any(r[0] > 0 for r in res.values())
    print("Obligation 2 as worded:", "FAILS (g takes negative values)" if any_negative
          else "not refuted on this grid")
    print()
    print("Check 2: a finite commutator cannot be a nonzero scalar")
    worst = check_trace_zero()
    assert worst < 1e-9, "trace identity violated: numerical problem"
    print("Confirmed: [A,B] = c*I forces c = 0 for finite matrices.")
    print()
    print("Check 3: dt g changes sign off the critical line, including sigma > 1")
    ch = check_dtg_sign_changes()
    assert ch[2.0] > 0 and ch[3.0] > 0, "expected sign changes for sigma > 1"
    print("'alpha ^ d alpha != 0 everywhere' fails where zeta has no zeros: not equivalent to RH.")
    print()
    print("Check 4: Laguerre-type condition on the critical line, using xi")
    check_xi_on_line()
    print()
    print("Check 5: Lagarias criterion Re(xi'/xi) > 0 for Re s > 1/2")
    check_lagarias()
    print()
    print("Check 6: Euler-product local factors g_p")
    check_prime_factors()
