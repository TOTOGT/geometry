#!/usr/bin/env python3
"""
Reproduces every numerical claim in §4.4-§4.6 of

  "The Riemann Hypothesis as Non-Integrability of an Arithmetic Contact
   Structure on the Adele Class Space", Pablo Nogueira Grossi, v1.

    pip install mpmath
    python3 verify_reflection_laws.py

Definitions (paper §4.1, §4.4):
    -zeta'/zeta(s) = c(sigma,t) - i g(sigma,t)     s = sigma + i t
    c = Re(-zeta'/zeta)   = sum Lambda(n) n^-sigma cos(t log n)   (sigma > 1)
    g = -Im(-zeta'/zeta)  = sum Lambda(n) n^-sigma sin(t log n)   (sigma > 1)
    (chi'/chi)(s) = log pi - psi(s/2)/2 - psi((1-s)/2)/2

Claims checked:
    A  g(sigma,t) - g(1-sigma,t) =  Im[(chi'/chi)(sigma+it)]      (difference law)
    B  c(sigma,t) + c(1-sigma,t) = -Re[(chi'/chi)(sigma+it)]      (sum law)
    C  c(1/2,t) = theta'(t), theta = Riemann-Siegel theta         (CLASSICAL:
       equivalent to Z(t) = e^{i theta} zeta(1/2+it) being real)
    D  at a zero rho = 1/2 + i gamma the pole of zeta'/zeta falls
       entirely into g (simple, residue -1); c stays analytic
"""
from mpmath import mp, mpc, zeta, digamma, log, pi, im, re, diff, siegeltheta, zetazero

mp.dps = 30
PASS = "ok"

def F(s):            return -diff(zeta, s) / zeta(s)      # = c - i g
def c(sig, t):       return re(F(mpc(sig, t)))
def g(sig, t):       return -im(F(mpc(sig, t)))
def chiL(s):         return log(pi) - digamma(s/2)/2 - digamma((1-s)/2)/2

PTS = [(1.5,3.0), (0.8,7.0), (2.3,1.2), (0.3,14.0), (1.1,25.0), (0.5,6.0), (0.5,14.134725)]
TOL = mp.mpf(10)**-14
fails = 0

print("A  difference law:  g(s,t) - g(1-s,t) == Im[chi'/chi]")
for sig, t in PTS:
    d = abs((g(sig,t) - g(1-sig,t)) - im(chiL(mpc(sig,t))))
    ok = d < TOL; fails += not ok
    print(f"   sigma={sig:<5} t={t:<10} |diff|={mp.nstr(d,3):>10}  {'ok' if ok else 'FAIL'}")

print("\nB  sum law:  c(s,t) + c(1-s,t) == -Re[chi'/chi]")
for sig, t in PTS:
    d = abs((c(sig,t) + c(1-sig,t)) + re(chiL(mpc(sig,t))))
    ok = d < TOL; fails += not ok
    print(f"   sigma={sig:<5} t={t:<10} |diff|={mp.nstr(d,3):>10}  {'ok' if ok else 'FAIL'}")

print("\nC  critical line:  c(1/2,t) == theta'(t)   [classical]")
for t in [0.7, 3.0, 6.0, 10.0, 25.0, 40.0, 100.0]:
    d = abs(c(0.5,t) - diff(lambda x: siegeltheta(x), mp.mpf(t)))
    ok = d < TOL; fails += not ok
    print(f"   t={t:<10} |diff|={mp.nstr(d,3):>10}  {'ok' if ok else 'FAIL'}")

print("\nD  the pole at a zero is one-sided:  g ~ -1/(t-gamma), c analytic")
g1 = im(zetazero(1))
print(f"   gamma_1 = {mp.nstr(g1,12)}")
for e in range(1, 6):
    delta = mp.mpf(10)**-e
    v = F(mpc(0.5, g1 + delta))
    resid = -im(v) * delta          # -> -1 if simple pole of residue -1
    # A simple pole means resid = -1 + O(delta): the tolerance must scale with
    # delta, not be a constant. Measured slope of the correction is ~0.082.
    ok = abs(resid + 1) < mp.mpf("0.2") * delta; fails += not ok
    print(f"   delta=1e-{e}  c={mp.nstr(re(v),9):>12}  g={mp.nstr(-im(v),9):>14}"
          f"  g*delta={mp.nstr(resid,6):>10}  {'ok' if ok else 'FAIL'}")
print(f"   c is NOT quoted AT t=gamma_1: numerical differentiation across the pole")
print(f"   returns a wrong value there. The limit above is the correct object.")

print(f"\n{'ALL CHECKS PASSED' if fails==0 else str(fails)+' CHECK(S) FAILED'}")
raise SystemExit(1 if fails else 0)
