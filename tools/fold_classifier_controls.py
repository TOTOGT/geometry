#!/usr/bin/env python3
# fold_classifier_controls.py -- 2026-11-06. Runs the F test of the G-chain table (rate exponent near each
# critical value AND hysteresis in a quasi-static control sweep) on 3 positive and 5 control systems.
# Written and first run in a cloud sandbox (scipy); NOT yet run on the author's machine.
# Positive: bistable cubic, subcritical pitchfork, toy immune model. Controls: transcritical, supercritical
# pitchfork, Hopf radial, linear damped, diffusion. Findings are in the project doc
# claude/STATUS-g-chain-controls-run-2026-11-06.md. This script does not classify any real system.
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy.integrate import solve_ivp

# ---- generic 1-D classifier: x' = f(x, mu) on x in [xlo, xhi] ----
def roots(f, mu, xlo, xhi, n=4001):
    xs = np.linspace(xlo, xhi, n); v = np.array([f(x, mu) for x in xs]); out = []
    for i in range(n - 1):
        if v[i] == 0: out.append(xs[i])
        elif v[i] * v[i + 1] < 0: out.append(brentq(lambda x: f(x, mu), xs[i], xs[i + 1], xtol=1e-14))
    return out
def dfdx(f, x, mu, e=1e-6): return (f(x + e, mu) - f(x - e, mu)) / (2 * e)
def slowest_stable_rate(f, mu, xlo, xhi):
    r = [-dfdx(f, x, mu) for x in roots(f, mu, xlo, xhi)]; r = [q for q in r if q > 0]
    return min(r) if r else np.inf
def find_critical(f, xlo, xhi, mulo, muhi, ngrid=401):
    mus = np.linspace(mulo, muhi, ngrid); s = np.array([slowest_stable_rate(f, m, xlo, xhi) for m in mus])
    cands = [i for i in range(1, ngrid - 1) if s[i] <= s[i - 1] and s[i] <= s[i + 1] and np.isfinite(s[i])]
    # also boundaries of finite region (fold ends)
    for i in range(ngrid - 1):
        if np.isfinite(s[i]) != np.isfinite(s[i + 1]): cands.append(i if np.isfinite(s[i]) else i + 1)
    crit = []
    for i in sorted(set(cands)):
        a, b = mus[max(i - 1, 0)], mus[min(i + 1, ngrid - 1)]
        res = minimize_scalar(lambda m: slowest_stable_rate(f, m, xlo, xhi), bounds=(a, b), method='bounded', options={'xatol': 1e-12})
        if np.isfinite(res.fun) and res.fun < 5e-3 and not any(abs(res.x - c) < 1e-3 for c in crit): crit.append(res.x)
    return crit
def exponent(f, xlo, xhi, mu_c):
    d = np.logspace(-4, -2, 9); pts = []
    for sgn in (+1, -1):
        r = [slowest_stable_rate(f, mu_c + sgn * x, xlo, xhi) for x in d]
        if all(np.isfinite(r)) and all(q > 0 for q in r):
            slope = np.polyfit(np.log(d), np.log(r), 1)[0]; pts.append((sgn, round(slope, 3)))
    return pts
def hysteresis_width(f, xlo, xhi, mulo, muhi, n=61):
    mus = np.linspace(mulo, muhi, n)
    def settle(x0, m):
        s = solve_ivp(lambda t, y: [f(float(np.clip(y[0], xlo, xhi)), m)], [0, 400], [float(np.clip(x0, xlo, xhi))], method='LSODA', rtol=1e-9, atol=1e-12)
        return float(np.clip(s.y[0, -1], xlo, xhi))
    x = 0.5 * xhi; up = []
    for m in mus: x = settle(x + 1e-6, m); up.append(x)
    dn = []
    for m in mus[::-1]: x = settle(x + 1e-6, m); dn.append(x)
    dn = dn[::-1]; return float(np.max(np.abs(np.array(up) - np.array(dn))))
def classify(name, f, xlo, xhi, mulo, muhi):
    crit = find_critical(f, xlo, xhi, mulo, muhi)
    exps = {round(c, 6): exponent(f, xlo, xhi, c) for c in crit}
    hw = hysteresis_width(f, xlo, xhi, mulo, muhi)
    half = any(abs(sl - 0.5) < 0.1 for e in exps.values() for _, sl in e)
    verdict = "F PRESENT" if (hw > 1e-2 and half) else "F absent"
    print(f"{name:34s} hyst={hw:7.4f}  critical points/exponents={exps}  -> {verdict}")
    return verdict

K, hh, r = 10., 1., 1.
cases = [
 ("POS: bistable cubic x'=mu+x-x^3",   lambda x, m: m + x - x**3,              -3, 3, -1.0, 1.0),
 ("POS: subcritical pitchfork",        lambda x, m: m*x + x**3 - x**5,         -2, 2, -0.5, 0.5),
 ("POS: toy immune (r=1,K=10,h=1)",    lambda x, m: r*x*(1-x/K) - m*x/(hh+x),   0, 12, 0.4, 3.6),
 ("CTL: transcritical x'=mu x - x^2",  lambda x, m: m*x - x**2,                -3, 3, -1.0, 1.0),
 ("CTL: supercritical pitchfork",      lambda x, m: m*x - x**3,                -2, 2, -1.0, 1.0),
 ("CTL: Hopf radial r'=lam r - r^3",   lambda x, m: m*x - x**3,                 0, 2, -1.0, 1.0),
 ("CTL: linear damped x'=-x+mu",       lambda x, m: -x + m,                    -3, 3, -1.0, 1.0),
]
out = {}
for c in cases: out[c[0]] = classify(*c)

# diffusion control: u_t = D u_xx, u(0)=mu, u(1)=0 -> rates independent of mu, no bifurcation, no hysteresis
n = 60; D = 1.0; h = 1.0 / (n + 1)
A = (np.diag(-2*np.ones(n)) + np.diag(np.ones(n-1), 1) + np.diag(np.ones(n-1), -1)) * D / h**2
w = np.linalg.eigvalsh(A); rates = -w
print(f"{'CTL: diffusion (u_t=D u_xx)':34s} slowest rate={rates.min():.4f} (D*pi^2={np.pi**2:.4f}), independent of mu; no critical point; no hysteresis -> F absent")

print("\nSummary:")
for k, v in out.items(): print(f"  {v:10s} {k}")
