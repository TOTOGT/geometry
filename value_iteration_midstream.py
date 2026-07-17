#!/usr/bin/env python3
"""
value_iteration_midstream.py  —  fresh reconstruction (Principia Orthogona, G6 LLC)

Rebuilds the midstream network-game threshold sigma* referenced in
GameTheory_Full_Pack.html ("The 1/3 Invariant"). The original script was cited but
not present in the repo; this is a clean, fully-documented FRESH build — a new
derivation with every assumption stated, not a claimed reproduction of the original.

MODEL (two-player, infinite horizon, discount delta; Table 1 parameters).
  State: imbalance i, AR(1) with volatility sigma:   i' = phi*i + sigma*eps.
  Payoffs, per period, from the paper's stated forms plus ONE piece the page leaves
  off (V's zero-volatility rent b0 — see note):
     J (positional):  K* = Kbar   ->  pi_J = beta*sigma*|i|
        E[pi_J] = a * sigma^2  with a pinned by the imbalance dynamics (option value).
     V (velocity):    v* static-optimal, plus a baseline speed rent b0:
        pi_V = b0 + 0.5*(beta*sigma*(1-gamma)*|i|)^2
  Crossing:  E[pi_J] = E[pi_V]   ->   a*sigma*^2 (+ tiny) = b0   ->   sigma* = sqrt(b0/a).

KEY HONEST FINDING.
  a is DETERMINED by the stated dynamics (a ~= 9.49 for phi=0.7).
  b0 is NOT on the page: R_V as written is identically 0 at sigma=0, yet the analytical
  result needs "V earns rent at sigma=0" (b>0). So sigma* is a ONE-PARAMETER FAMILY in b0.
     sigma* = 1/3    <=>  b0 ~= 1.05
     sigma* = 0.665  <=>  b0 ~= 4.20
  Neither number is derivable from what is written; b0 (V's baseline speed rent) must be
  measured. The paper's "correction factor psi ~= 0.50" is just the ratio between two
  different b0 guesses, narrated after the fact.

Run:  python3 value_iteration_midstream.py
"""
import numpy as np, math

BETA, GAMMA, PHI, DELTA = 8.5, 0.55, 0.7, 0.985   # Table 1 (Kbar cancels; delta unused in the crossing)
_erf = np.vectorize(math.erf)
def _ncdf(x): return 0.5 * (1.0 + _erf(x / math.sqrt(2.0)))

def stationary(sigma, n=41, m=3.5):
    """Tauchen discretization of i' = phi*i + sigma*eps; returns grid and stationary dist."""
    s = sigma / math.sqrt(1 - PHI**2)
    xs = np.linspace(-m*s, m*s, n); step = xs[1] - xs[0]
    P = np.zeros((n, n))
    for j in range(n):
        mu = PHI * xs[j]
        P[j, 0]  = _ncdf((xs[0]  - mu + step/2) / sigma)
        P[j, -1] = 1 - _ncdf((xs[-1] - mu - step/2) / sigma)
        for k in range(1, n-1):
            P[j, k] = _ncdf((xs[k] - mu + step/2)/sigma) - _ncdf((xs[k] - mu - step/2)/sigma)
    w = np.ones(n) / n
    for _ in range(3000): w = w @ P
    return xs, w / w.sum()

def E_piJ(sigma):
    xs, w = stationary(sigma); return BETA * sigma * np.sum(w * np.abs(xs))

def E_piV_sigma_term(sigma):
    xs, w = stationary(sigma); return 0.5 * np.sum(w * (BETA*sigma*(1-GAMMA)*np.abs(xs))**2)

def option_value_coeff():
    """a := E[pi_J]/sigma^2  (constant in sigma -> J is genuinely convex in volatility)."""
    return E_piJ(0.30) / 0.30**2

def sigma_star(b0, a=None):
    a = a if a is not None else option_value_coeff()
    return math.sqrt(max(b0, 0.0) / a)

if __name__ == "__main__":
    print("E[pi_J] = a * sigma^2  (a should be constant across sigma):")
    for sg in (0.2, 0.3, 0.4, 0.5):
        print(f"  sigma={sg}:  E[pi_J]={E_piJ(sg):.4f}  a={E_piJ(sg)/sg**2:.3f}  E[piV_sigma]={E_piV_sigma_term(sg):.4f}")
    a = option_value_coeff()
    print(f"\noption-value coefficient  a = {a:.2f}  (pinned by the stated AR(1) dynamics)")
    print("crossing:  sigma* = sqrt(b0 / a),  b0 = V's sigma=0 rent (NOT on the page)")
    for tgt in (1/3, 0.665):
        print(f"  sigma* = {tgt:.3f}  <=>  b0 = {a*tgt**2:.2f}")
    print("\nVerdict: sigma* is a one-parameter family in b0; '1/3' and '0.665' are two points on it.")
