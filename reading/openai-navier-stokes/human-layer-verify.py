#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
human-layer-verify.py -- verify script for reading/openai-navier-stokes/human-layer.html (R6, R24).

The page adds the explanatory layer the preprint leaves out. Its toy models are classical and
are NOT the paper's construction; this script checks that each toy is what the page says it is.

Blocks:
  [1] waves carry momentum: for w = a cos(k.x) with a perpendicular to k, the space average of
      w (x) w is a a^T / 2 -- a rank-one, positive semi-definite stress (numerical quadrature)
  [2] why two families and a cone: squared amplitudes are >= 0, so two families with flux
      directions v1, v2 reach exactly the cone {c1 v1 + c2 v2 : c1, c2 >= 0}; a target outside it
      needs a negative weight
  [3] Kelvin's shearing wave is an exact Navier-Stokes solution: on the shear u = (S y, 0), the
      vorticity w' = A(t) cos(kx x + ky(t) y), ky(t) = ky0 - S kx t, A(t) = A0 exp(-nu int |k|^2),
      satisfies the full 2-D vorticity equation, nonlinear term included (sympy)
  [4] it grows, then decays: energy ~ A(t)^2 / |k(t)|^2 rises while the shear turns the wave
      toward kx (|k| falls) and then falls once |k| grows and viscosity dominates; the page's
      default parameters give the peak time and gain printed here
  [5] the speeds are faster than diffusion allows: the parabolic (critical) speed scale is
      l_r / tau ~ tau^(-1/2); the swirl tau^(-1/2-h) exceeds it by tau^(-h) = Re_theta
  [6] the dependency map names results that exist in the paper (needs --pdf PATH; else SKIP)

Usage:  python3 human-layer-verify.py [--pdf PATH]
"""
import math, re, subprocess, sys
from fractions import Fraction as F

FAIL, SKIP = [], []
def check(label, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {label}" + (f"  ({detail})" if detail else ""))
    if not ok: FAIL.append(label)
def skip(label, why):
    print(f"  SKIP  {label}  ({why})"); SKIP.append(label)

print("[1] a wave's averaged momentum flux")
k = (3, -2, 5)
a = (2.0, 3.0, 0.0)                       # a . k = 6 - 6 + 0 = 0
assert sum(x * y for x, y in zip(a, k)) == 0
N = 24; acc = [[0.0] * 3 for _ in range(3)]
for i in range(N):
    for j in range(N):
        for l in range(N):
            x = (2 * math.pi * i / N, 2 * math.pi * j / N, 2 * math.pi * l / N)
            c = math.cos(sum(kk * xx for kk, xx in zip(k, x)))
            for p in range(3):
                for q in range(3):
                    acc[p][q] += a[p] * a[q] * c * c
acc = [[v / N**3 for v in row] for row in acc]
want = [[a[p] * a[q] / 2 for q in range(3)] for p in range(3)]
err = max(abs(acc[p][q] - want[p][q]) for p in range(3) for q in range(3))
check("<w (x) w> = a a^T / 2 over a period", err < 1e-12, f"max error {err:.1e}")
check("the wave itself averages to zero", abs(sum(math.cos(sum(kk * 2 * math.pi * ii / N for kk, ii in zip(k, (i, j, l))))
      for i in range(N) for j in range(N) for l in range(N)) / N**3) < 1e-12)
check("the stress is positive semi-definite: x^T <w (x) w> x = (a.x)^2 / 2 >= 0", all(
      sum(x[p] * acc[p][q] * x[q] for p in range(3) for q in range(3)) >= -1e-12
      for x in [(1, 0, 0), (0, 1, 0), (1, -1, 2), (-3, 1, 1)]))

print("[2] two families and the cone")
v1, v2 = (1.0, 0.25), (0.3, 1.0)           # illustrative flux directions (r-theta, r-z) per unit squared amplitude
def weights(T):
    det = v1[0] * v2[1] - v2[0] * v1[1]
    return ((T[0] * v2[1] - v2[0] * T[1]) / det, (v1[0] * T[1] - T[0] * v1[1]) / det)
inside, outside = (1.0, 1.0), (1.0, -0.5)
ci, co = weights(inside), weights(outside)
check("a target inside the cone has two positive weights", ci[0] > 0 and ci[1] > 0, f"c = ({ci[0]:.3f}, {ci[1]:.3f})")
check("a target outside needs a negative weight, i.e. a negative squared amplitude", min(co) < 0, f"c = ({co[0]:.3f}, {co[1]:.3f})")
check("one family alone reaches only a ray (two stress components need two families)",
      abs(weights((2 * v1[0], 2 * v1[1]))[1]) < 1e-12)

print("[3] Kelvin's shearing wave solves the 2-D Navier-Stokes vorticity equation exactly")
try:
    import sympy as sp
    x, y, t = sp.symbols("x y t", real=True)
    S, nu, kx, ky0, A0 = sp.symbols("S nu k_x k_y0 A_0", positive=True)
    ky = ky0 - S * kx * t
    A = A0 * sp.exp(-nu * sp.integrate(kx**2 + (ky0 - S * kx * sp.Symbol("s"))**2, (sp.Symbol("s"), 0, t)))
    wp = A * sp.cos(kx * x + ky * y)                       # perturbation vorticity
    psi = -wp / (kx**2 + ky**2)                             # streamfunction: lap psi = w'
    up, vp = sp.diff(psi, y), -sp.diff(psi, x)              # u = (psi_y, -psi_x)
    U, V = S * y + up, vp                                   # full velocity
    W = -S + wp                                             # full vorticity (background -S)
    lap = lambda f: sp.diff(f, x, 2) + sp.diff(f, y, 2)
    resid = sp.diff(W, t) + U * sp.diff(W, x) + V * sp.diff(W, y) - nu * lap(W)
    check("w_t + u.grad w = nu lap w, with the nonlinear term included", sp.simplify(resid) == 0)
    check("lap psi = w' (the velocity is the one this vorticity induces)", sp.simplify(lap(psi) - wp) == 0)
except ImportError:
    skip("Kelvin mode", "sympy not installed")

print("[4] growth then decay (page defaults: kx = 1, S = 1, ky0 = 8, nu = 0.002)")
def energy(tt, ky0=8.0, nu=0.002, kx=1.0, S=1.0):
    ky = ky0 - S * kx * tt
    integ = kx**2 * tt + (ky0**2 * tt - S * kx * ky0 * tt**2 + (S * kx)**2 * tt**3 / 3)
    return math.exp(-2 * nu * integ) / (kx**2 + ky**2)
ts = [i * 0.01 for i in range(0, 3001)]
Es = [energy(tt) for tt in ts]
imax = max(range(len(Es)), key=Es.__getitem__)
gain = Es[imax] / Es[0]
check("energy first rises", Es[100] > Es[0])
check("then falls below its starting value", Es[-1] < Es[0])
print(f"        peak at t = {ts[imax]:.2f} (inviscid peak would be t = ky0/(S kx) = 8.00), gain x{gain:.1f}")
check("inviscid gain would be |k0|^2/kx^2 = 65; viscosity lowers it", 1 < gain < 65, f"gain {gain:.1f}")
check("the peak comes just before the wave is aligned with kx (ky = 0 at t = 8)", 7.0 < ts[imax] <= 8.0)

print("[5] faster than diffusion allows")
for h in (F(1, 200), F(1, 101)):
    crit = F(1, 2) - 1                    # l_r / tau = tau^(1/2) / tau
    swirl = -(F(1, 2) + h)
    check(f"h = {h}: swirl / critical speed = tau^({swirl - crit}) = tau^(-h) = Re_theta", swirl - crit == -h)

print("[6] the dependency map against the paper")
labels = ["Theorem 1.1", "Theorem 3.1", "Theorem 4.6", "Lemma 4.5", "Proposition 5.5", "Lemma 7.4",
          "Proposition 7.5", "Lemma 7.7", "Proposition 9.6", "Proposition 9.9", "Proposition 10.1",
          "Lemma 10.3", "Lemma 10.4", "Lemma 10.5", "Corollary 10.6", "Proposition C.3", "Proposition B.2",
          "Proposition A.4", "Proposition 9.5", "Lemma 10.2"]
if "--pdf" in sys.argv:
    txt = subprocess.run(["pdftotext", "-layout", sys.argv[sys.argv.index("--pdf") + 1], "-"],
                         capture_output=True, text=True).stdout
    flat = re.sub(r"\s+", " ", txt)
    missing = [l for l in labels if l not in flat]
    check(f"all {len(labels)} results named on the page occur in the paper", not missing, f"missing: {missing}")
else:
    skip("dependency labels", "pass --pdf PATH to the paper")

print("""
[HONESTY]
What this establishes: the page's toy models are correct as stated. A plane wave's averaged
flux is a positive rank-one stress; two families reach exactly a cone; Kelvin's shearing wave
is an exact viscous solution whose energy grows and then decays as the page shows; the swirl
exceeds the parabolic speed scale by tau^(-h); and the results the dependency map names exist.

What it does not establish: that the toys are how the paper's construction works in detail.
Kelvin's wave lives on plane shear; the paper's pulses live on a rotating, axially sheared
vortex and are amplified partly by the centrifugal mechanism, which this toy omits. The flux
directions in block [2] are illustrative numbers, not the paper's. The page's account of how
the construction might have been found is our reconstruction, not the authors' account.""")
print(f"\n{len(FAIL)} FAIL, {len(SKIP)} SKIP")
sys.exit(1 if FAIL else 0)
