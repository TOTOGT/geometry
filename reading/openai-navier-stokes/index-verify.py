#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
index-verify.py -- verify script for reading/openai-navier-stokes/index.html (R6, R24).

Primary source: OpenAI, "Finite time blowup for Navier-Stokes" (166 pp., PDF dated
8 Sep 2026, https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf).
Section and equation numbers below are the paper's.

The reading guide quotes scaling laws from Sections 2-3 of the paper. This script re-derives
each one from the paper's stated inputs (l_r ~ tau^(1/2), l_z ~ tau^(1/2-h), swirl and axial
speed ~ tau^(-1/2-h), radial speed O(tau^(-1/2)), 0 < h < 1/100) and prints every exponent the
page shows. It checks the arithmetic of the paper's sketch; it does not check the paper's proof.

Blocks:
  [1] core volume, energy and dissipation exponents; energy -> 0 and dissipation integrable iff h < 1/6
  [2] Reynolds numbers and the balance of rates (transport, radial diffusion, axial diffusion)
  [3] pulse scales: A_wave^2 matches the stress scale, A_wave^2/q^(1/2) matches the momentum rates
  [4] viscosity rescaling u_nu = sqrt(nu) u(x/sqrt(nu), t) maps solutions to solutions (symbolic, sympy;
      SKIP if sympy absent) and multiplies the energy by nu^(5/2)
  [5] the correction exponent sigma_j = 1/5 + j/10 (eq. after Prop. 9.6) and the similarity map
      tau = q(1 - eta^2), z = q^D eta is invertible for |eta| < 1 (d/dq > 0 iff h < 1/2)
  [6] the page's exponent table, for the default h = 1/200 used by its slider
  [7] optional: if the PDF text is supplied (--pdf PATH), the quoted sentences occur in it

Usage:  python3 index-verify.py [--pdf "FINITE TIME BLOWUP FOR NAVIER-STOKES.pdf"]
"""
import os, re, subprocess, sys
from fractions import Fraction as F

FAIL, SKIP = [], []
def check(label, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {label}" + (f"  ({detail})" if detail else ""))
    if not ok: FAIL.append(label)
def skip(label, why):
    print(f"  SKIP  {label}  ({why})"); SKIP.append(label)

# exponents of tau, as functions of h (exact rationals)
def scal(h):
    lr, lz = F(1, 2), F(1, 2) - h
    uth = -(F(1, 2) + h)          # swirl and axial speed
    ur = -F(1, 2)                 # radial speed (upper bound)
    vol = 2 * lr + lz             # = 3/2 - h
    E = vol + 2 * uth             # kinetic energy of the core
    D = vol + 2 * (uth - lr)      # integral of squared radial derivative
    return dict(lr=lr, lz=lz, uth=uth, ur=ur, vol=vol, E=E, D=D,
                Re_th=uth + lr, Re_r=ur + lr, adv_r=ur - lr, adv_z=uth - lz, diff_r=-2 * lr,
                diff_z=-2 * lz)

hs = [F(k, 1000) for k in range(1, 10)] + [F(1, 200), F(1, 101)]
print("[1] volume, energy, dissipation (paper Sec. 2.1 and 3.5)")
ok = all(scal(h)["vol"] == F(3, 2) - h and scal(h)["E"] == F(1, 2) - 3 * h and scal(h)["D"] == -F(1, 2) - 3 * h for h in hs)
check("core volume tau^(3/2-h), energy tau^(1/2-3h), dissipation tau^(-1/2-3h) for h in (0, 1/100)", ok)
check("energy exponent > 0 (energy -> 0) and dissipation exponent > -1 (integrable) for every h < 1/100",
      all(scal(h)["E"] > 0 and scal(h)["D"] > -1 for h in hs))
thr = [h for h in (F(k, 600) for k in range(1, 200)) if not (scal(h)["E"] > 0 and scal(h)["D"] > -1)]
check("both conditions fail first at h = 1/6 (the paper's 'Since h < 1/6')", min(thr) == F(1, 6), f"first failure at h = {min(thr)}")

print("[2] Reynolds numbers and rates (Sec. 2.1)")
h = F(1, 200); s = scal(h)
check("Re_theta = |u_theta| l_r / nu ~ tau^(-h) -> infinity", s["Re_th"] == -h)
check("Re_r = |u_r| l_r / nu = O(1)", s["Re_r"] == 0)
check("radial transport |u_r|/l_r, axial transport |u_z|/l_z, radial diffusion nu/l_r^2 all ~ tau^(-1)",
      s["adv_r"] == -1 and s["adv_z"] == -1 and s["diff_r"] == -1)
check("axial/radial diffusion = l_r^2/l_z^2 ~ tau^(2h) -> 0", (2 * s["lr"]) - (2 * s["lz"]) == 2 * h)

print("[3] pulse scales (Sec. 3.3), in powers of q ~ tau")
Aw, lw = -(F(1, 2) + h / 2), F(1, 2) + h / 2
check("A_wave^2 ~ q^(-1-h) equals |u_theta|/q^(1/2)", 2 * Aw == -1 - h == s["uth"] - F(1, 2))
check("A_wave^2 / q^(1/2) ~ q^(-3/2-h) equals the rate d/dt u_theta ~ q^(-A-1)", 2 * Aw - F(1, 2) == -(F(1, 2) + h) - 1)
# The paper's display reads A_wave / q^(-1/2-h) ~ l_wave / q^(1/2) ~ q^(h/2): two ratios, not a product.
# (A first draft of this block multiplied them and failed; the page was written after the fix, R24.)
check("A_wave / |u_theta| ~ q^(h/2) -> 0: waves are weak relative to the core speed", Aw - s["uth"] == h / 2)
check("l_wave / l_r ~ q^(h/2) -> 0: wavelengths are short relative to the core radius", lw - s["lr"] == h / 2)

print("[4] viscosity rescaling (Sec. 3)")
try:
    import sympy as sp
    x, y, z, t, nu = sp.symbols("x y z t nu", positive=True)
    X = (x, y, z); Xs = tuple(c / sp.sqrt(nu) for c in X)
    u = [sp.Function(f"u{i}") for i in range(3)]; p = sp.Function("p")
    U = [u[i](*X, t) for i in range(3)]; P = p(*X, t)
    res = [sp.diff(U[i], t) + sum(U[j] * sp.diff(U[i], X[j]) for j in range(3))
           - sum(sp.diff(U[i], X[j], 2) for j in range(3)) + sp.diff(P, X[i]) for i in range(3)]  # nu = 1
    Un = [sp.sqrt(nu) * u[i](*Xs, t) for i in range(3)]; Pn = nu * p(*Xs, t)
    resn = [sp.diff(Un[i], t) + sum(Un[j] * sp.diff(Un[i], X[j]) for j in range(3))
            - nu * sum(sp.diff(Un[i], X[j], 2) for j in range(3)) + sp.diff(Pn, X[i]) for i in range(3)]
    ok = all(sp.simplify(resn[i] - sp.sqrt(nu) * res[i].subs({x: Xs[0], y: Xs[1], z: Xs[2]}, simultaneous=True)) == 0 for i in range(3))
    check("residual of (u_nu, p_nu) at viscosity nu = sqrt(nu) x residual of (u, p) at viscosity 1, so f_nu = sqrt(nu) f(x/sqrt(nu), t)", ok)
    divn = sum(sp.diff(Un[i], X[i]) for i in range(3)); div = sum(sp.diff(U[i], X[i]) for i in range(3))
    check("divergence-free is preserved", sp.simplify(divn - div.subs({x: Xs[0], y: Xs[1], z: Xs[2]}, simultaneous=True)) == 0)
    check("energy scales by nu * nu^(3/2) = nu^(5/2) (finite stays finite)", sp.simplify(nu * nu**sp.Rational(3, 2) - nu**sp.Rational(5, 2)) == 0)
except ImportError:
    skip("viscosity rescaling", "sympy not installed")

print("[5] correction exponent and similarity map")
sig = [F(1, 5) + F(j, 10) for j in range(0, 60)]
check("sigma_0 = 1/5 and sigma_{j+1} = sigma_j + 1/10: sigma_j exceeds every N after 10N steps", sig[0] == F(1, 5) and all(sig[j + 1] - sig[j] == F(1, 10) for j in range(59)) and sig[50] > 5)
# d/dq (q - z^2 q^(2h)) at z = q^D eta equals 1 - 2h eta^2 (paper eq. after (3.2))
try:
    import sympy as sp
    q, eta, hh = sp.symbols("q eta h", positive=True)
    zz = q ** (sp.Rational(1, 2) - hh) * eta
    expr = sp.diff(q - sp.Symbol("Z")**2 * q**(2 * hh), q).subs(sp.Symbol("Z"), zz)
    check("d/dq (q - z^2 q^(2h)) = 1 - 2h eta^2 at z = q^D eta", sp.simplify(expr - (1 - 2 * hh * eta**2)) == 0)
except ImportError:
    skip("similarity map derivative", "sympy not installed")
check("1 - 2h eta^2 >= 1 - 2h > 0 on |eta| < 1 for 0 < h < 1/100, so q(z, tau) is unique", all(1 - 2 * hh_ > 0 for hh_ in hs))

print("[6] the page's exponent table at h = 1/200")
h = F(1, 200); s = scal(h)
table = [("core radius l_r", s["lr"]), ("core height l_z", s["lz"]), ("swirl and axial speed", s["uth"]),
         ("radial speed (bound)", s["ur"]), ("core volume", s["vol"]), ("core kinetic energy", s["E"]),
         ("core dissipation rate", s["D"]), ("Re_theta", s["Re_th"]), ("aspect ratio l_r/l_z", s["lr"] - s["lz"])]
for name, e in table:
    print(f"        {name:<26} tau^({float(e):+.4f})")
check("table has nine rows, as the page shows", len(table) == 9)

print("[7] quoted sentences against the PDF text")
if "--pdf" in sys.argv:
    path = sys.argv[sys.argv.index("--pdf") + 1]
    try:
        txt = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
        flat = re.sub(r"\s+", " ", txt).replace("\u2019", "'")   # typographic apostrophes
        for q in ["develops unbounded velocity in finite time while maintaining uniformly bounded kinetic energy",
                  "This establishes alternative (C) in the Millennium problem statement",
                  "oscillatory pulses generate a mean momentum flux that supplies the missing force on a collapsing background vortex",
                  "Since h < 1/6",
                  "the fluid's own motion supplies the missing momentum transport"]:
            check(f"quote present: '{q[:60]}...'", q in flat)
    except FileNotFoundError:
        skip("quote check", "pdftotext not installed")
else:
    skip("quote check", "pass --pdf PATH to the paper")

print("""
[HONESTY]
What this establishes: the exponent arithmetic of the paper's Sections 2-3 as quoted on the page
(volume, energy, dissipation, Reynolds numbers, rate balances, pulse scales), the viscosity
rescaling identity, the correction-exponent recursion, the invertibility of the similarity map,
and, with --pdf, that the sentences the page quotes from the paper are in it. (The Clay
Institute's words, quoted from press and Wikipedia, are not checked here.)

What it does not establish: anything about the proof itself. The existence of the profiles
(Sections 4, 5 and Appendices A-C), the admissible stress cone, the wave estimates (Section 7),
the convergence of the correction cycle (Section 9) and the smooth extension of the force
(Section 10) are not checked here. The paper is a preprint; as of this page's date it has not
completed peer review, and the Clay Institute has said it awaits that review.""")
print(f"\n{len(FAIL)} FAIL, {len(SKIP)} SKIP")
sys.exit(1 if FAIL else 0)
