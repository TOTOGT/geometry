#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book26/nielsen-lepton-table.py -- the lepton-mass formula of a third-party preprint (chapter 8, C12), written as one
table: each constant with its expression, then the formula's outputs against PDG 2024/2025 values, then the
size of each correction term. Needs mpmath. No network.     python3 book26/nielsen-lepton-table.py
SOURCE OF THE FORMULAS: the preprint's own Appendix A script (TUFT_Verification.py), lines for sections 1-3,
transcribed by hand because the PDF text lost its indentation. The check at the end confirms the transcription:
the paper's script prints "e +0.22%, mu +0.24%, tau +0.23% (uniform scale offset)" and ratio deviations of
+0.002% (mu/e) and -0.006% (tau/mu). This script reproduces those.
NOT VERIFIED: the PDG reference masses are taken from the preprint's own table of references (m_tau = 1776.93(9),
the 2024 value it carries), not re-fetched.
"""
import sys
from mpmath import mp, mpf, pi, sqrt, exp, log, zeta
mp.dps = 40
FAIL = []
def must(label, ok):
    print(("PASS " if ok else "FAIL ") + label)
    if not ok: FAIL.append(label)
z3, z5 = zeta(3), zeta(5)
alpha = (9/(8*pi**4))*(pi**5/1920)**(mpf(1)/4)
v = mpf("246220")
kappa = exp(z3/(24*pi**2))/(4*pi**2)
Lam = sqrt(2*pi)*v*kappa**6
a3 = 6*sqrt(2)*exp(z3/(24*pi**2))
s3 = z3/(4*pi**2)
beta = z5/(8*pi**4)
tau = {1: mpf(1), 2: mpf(1), 3: mpf(3)**(1/(3 - s3*sqrt(2)))}
print("--- constants (expression : value)")
for name, expr, val in [
    ("alpha", "(9/(8 pi^4)) (pi^5/1920)^(1/4)", alpha),
    ("v (MeV)", "246220, the one empirical input", v),
    ("kappa", "exp(zeta3/(24 pi^2))/(4 pi^2)", kappa),
    ("Lambda_Hopf (MeV)", "sqrt(2 pi) v kappa^6", Lam),
    ("a", "6 sqrt2 exp(zeta3/(24 pi^2))", a3),
    ("sigma3", "zeta3/(4 pi^2)", s3),
    ("beta", "zeta5/(8 pi^4)", beta),
    ("tau_K(3)", "3^(1/(3 - sigma3 sqrt2))  [trefoil, 'Dubois regularization' in the paper's comment]", tau[3])]:
    print(f"{name:<20} {expr:<62} {mp.nstr(val, 12)}")
print("discrete choices in the formula: shell level n=1,2,3 (the paper's knot assignment), the exponent terms below, the trefoil regularization")
PDG = {1: (mpf("0.51099895069"), mpf("1.6e-10")), 2: (mpf("105.6583755"), mpf("0.0000023")), 3: (mpf("1776.93"), mpf("0.09"))}
def mass(n, drop=None):
    e = a3*n - z3*n**2
    if drop != "beta": e += beta*n*(n+1)/2
    if drop != "alpha": e += n*alpha/6
    if drop != "tau": e += s3*log(tau[n])
    return Lam*(n+1)*exp(e)
print("--- outputs against PDG (relative deviation, pull in sigma)")
m = {n: mass(n) for n in (1, 2, 3)}
dev = {}
for n, nm in ((1, "e"), (2, "mu"), (3, "tau")):
    r, u = PDG[n]; dev[n] = (m[n]-r)/r
    print(f"m_{nm:<4} {mp.nstr(m[n], 10):>14} MeV   PDG {mp.nstr(r, 10)}   dev {mp.nstr(dev[n]*100, 4)} %   pull {mp.nstr((m[n]-r)/u, 4)} sigma")
rme = (m[2]/m[1])/(PDG[2][0]/PDG[1][0]) - 1
rtm = (m[3]/m[2])/(PDG[3][0]/PDG[2][0]) - 1
print(f"ratio mu/e dev {mp.nstr(rme*100, 4)} %   ratio tau/mu dev {mp.nstr(rtm*100, 4)} %")
print("--- size of each correction term (relative change in each mass if the term is removed, %)")
for term in ("beta", "alpha", "tau"):
    print(f"drop {term:<6}", [mp.nstr((mass(n, term)-m[n])/m[n]*100, 3) for n in (1, 2, 3)])
print("--- checks")
must("1/alpha is 137.0361 to six figures (the paper says 137.036)", abs(1/alpha - mpf("137.036")) < mpf("0.0005"))
must("transcription reproduces the paper's printed deviations: e +0.22%, mu +0.24%, tau +0.23% (to 0.02 points)",
     all(abs(dev[n]*100 - t) < mpf("0.02") for n, t in ((1, mpf("0.22")), (2, mpf("0.24")), (3, mpf("0.23")))))
must("... and its printed ratio deviations: mu/e +0.002%, tau/mu -0.006% (to 0.001 points)",
     abs(rme*100 - mpf("0.002")) < mpf("0.001") and abs(rtm*100 + mpf("0.006")) < mpf("0.001"))
must("the electron mass is more than 10^6 sigma from PDG, the muon more than 10^5, the tau more than 40",
     abs((m[1]-PDG[1][0])/PDG[1][1]) > 10**6 and abs((m[2]-PDG[2][0])/PDG[2][1]) > 10**5 and abs((m[3]-PDG[3][0])/PDG[3][1]) > 40)
print("[HONESTY] The abstract says the charged lepton masses are within PDG uncertainties. The paper's own script prints a uniform 0.23% offset, which this reproduces; the ratios agree to 0.002-0.006% only after one mass is used as the anchor. That is a one-parameter fit to the electron, with a five-term exponent. It does not show the terms were chosen after the data, only that the paper does not say they were chosen before.")
sys.exit(1 if FAIL else 0)
