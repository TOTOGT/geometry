#!/usr/bin/env python3
"""helix-ndim-check.py -- numerical check (NOT a proof) of whether the dm^3 attractor
carries over from n=1 (Book 4 Ch 3, System 3.1) to n copies in R^(2n+1).

n=1 is System (3.1) exactly as printed in ch03.html:
    r'     = r(1-r^2) + 2(r-1)e^{-z}
    theta' = 1
    z'     = r^2 - 2(r-1)^2 e^{-z}

n>1 is OUR OWN CONSTRUCTION (ch03 defines only n=1).  For contact form
alpha = dz - sum_i r_i^2 dtheta_i, with theta_i' = w_i, keep the n=1 form per copy and
share the single z (coupling e^{-z}):
    r_i'     = r_i(1-r_i^2) + 2(r_i-1)e^{-z}
    theta_i' = w_i
    z'       = sum_i w_i [ r_i^2 - 2(r_i-1)^2 e^{-z} ]
so alpha(gamma') = z' - sum r_i^2 w_i = -2 e^{-z} sum w_i (r_i-1)^2, which vanishes on r_i=1
(the Legendrian torus-helix).  For n=1, w=1 this is exactly System (3.1).
Other generalisations exist; this is one choice, labelled as such.

Reports: convergence, late-time rate of max|r_i-1| (n=1 linearisation is -2+2e^{-z}),
Legendrian defect, and bisected inner basin boundaries.  Integrator: scipy DOP853.
"""
import numpy as np
from scipy.integrate import solve_ivp

def make_rhs(w):
    w = np.asarray(w, float); n = len(w)
    def rhs(t, y):
        r = y[:n]; z = y[2*n]
        e = np.exp(-z)
        dr = r*(1-r**2) + 2*(r-1)*e
        dth = w
        dz = np.sum(w*(r**2 - 2*(r-1)**2*e))
        return np.concatenate([dr, dth, [dz]])
    return rhs

def run(w, r0, z0=0.0, T=40.0, rtol=1e-12, atol=1e-14):
    w = np.asarray(w, float); n = len(w)
    y0 = np.concatenate([r0, np.zeros(n), [z0]])
    def dead(t, y): return np.min(y[:n]) - 0.02       # an r_i collapsing toward 0 => diverged inward
    dead.terminal = True; dead.direction = -1
    def blow(t, y): return 50.0 - np.max(np.abs(y[:n]))
    blow.terminal = True
    sol = solve_ivp(make_rhs(w), (0, T), y0, method='DOP853', rtol=rtol, atol=atol,
                    events=[dead, blow], dense_output=False, max_step=0.05)
    return sol, n

def converged(sol, n, tol=1e-6):
    return sol.status == 0 and np.max(np.abs(sol.y[:n, -1] - 1)) < tol

def late_rate(sol, n, lo=1e-3, hi=1e-8):
    d = np.max(np.abs(sol.y[:n] - 1), axis=0)
    m = (d < lo) & (d > hi)
    if m.sum() < 10: return None
    t = sol.t[m]; return np.polyfit(t, np.log(d[m]), 1)[0], sol.y[2*n][m].min()

def defect(sol, n, w, final=True):
    """|alpha(gamma')| = 2 e^{-z} sum w_i (r_i-1)^2; at t=0 it is O(1), the claim is it -> 0."""
    r = sol.y[:n]; z = sol.y[2*n]; e = np.exp(-z)
    d = 2*e*np.sum(np.asarray(w)[:, None]*(r-1)**2, axis=0)
    return d[-1] if final else np.max(d)

def bisect(w, direction, lo=0.05, hi=1.0, it=40):
    """scale r0 = 1 - s*direction, s in (0,1): find the smallest s still converging.
    returns boundary s* (r0 = 1 - s*dir)."""
    w = np.asarray(w, float); n = len(w)
    d = np.asarray(direction, float)
    good, bad = 0.0, 0.98
    sol, _ = run(w, 1 - bad*d)
    if converged(sol, n): return None   # nothing diverges along this ray
    for _ in range(it):
        mid = 0.5*(good+bad)
        sol, _ = run(w, 1 - mid*d, T=60)
        if converged(sol, n): good = mid
        else: bad = mid
    return 0.5*(good+bad)

if __name__ == '__main__':
    rng = np.random.default_rng(7)
    print("== n=1 baseline (System 3.1 exactly) ==")
    for r0 in [1.5, 1.2, 0.9, 0.8, 0.7]:
        sol, n = run([1.0], [r0])
        lr = late_rate(sol, n)
        print(f" r0={r0}: converged={converged(sol, n)}  final|r-1|={abs(sol.y[0,-1]-1):.2e}"
              f"  late rate={lr[0]:.4f}" if lr else f" r0={r0}: converged={converged(sol, n)} (no late-rate window; status {sol.status})")
    s = bisect([1.0], [1.0])
    print(f" inner basin boundary r* (z0=0) ~ {1 - s:.6f}   (Ch 3 prose: ~0.776)")

    cases = {
        'n=2 w=(1,sqrt2) incommensurate': [1.0, np.sqrt(2)],
        'n=2 w=(1,1) commensurate': [1.0, 1.0],
        'n=3 w=(1,sqrt2,sqrt3)': [1.0, np.sqrt(2), np.sqrt(3)],
    }
    for name, w in cases.items():
        n = len(w)
        print(f"\n== {name} ==")
        ok = 0; rates = []; dm = 0.0; trials = 200
        for _ in range(trials):
            r0 = rng.uniform(1.0, 1.8, n)              # outer: every r_i(0) > 1
            sol, _ = run(w, r0, T=40)
            if converged(sol, n):
                ok += 1; dm = max(dm, defect(sol, n, w))
                lr = late_rate(sol, n)
                if lr: rates.append(lr[0])
        print(f" outer starts (all r_i(0) in (1,1.8)): {ok}/{trials} converged to r_i=1")
        if rates: print(f" late rate of max|r_i-1|: mean {np.mean(rates):.4f}, min {min(rates):.4f}, max {max(rates):.4f}"
                        f"   (n=1 linear prediction -> -2)")
        print(f" Legendrian defect |alpha(gamma')| at t=40, worst over runs: {dm:.2e}")
        ok2 = 0
        for _ in range(200):
            r0 = rng.uniform(0.85, 1.8, n)             # mixed: some inside (>=0.85), some outside
            sol, _ = run(w, r0, T=40)
            ok2 += converged(sol, n)
        print(f" mixed starts r_i(0) in (0.85,1.8): {ok2}/200 converged")
        # basin along the diagonal and along one-coordinate-inside rays
        sd = bisect(w, np.ones(n))
        print(f" inner boundary on diagonal r_i=s: s* ~ {1 - sd:.6f}" if sd is not None else " diagonal: no divergence found")
        e0 = np.zeros(n); e0[0] = 1.0
        s0 = bisect(w, e0)
        print(f" inner boundary dropping only r_1 (others =1): r_1* ~ {1 - s0:.6f}" if s0 is not None else " one-coordinate: no divergence found")
