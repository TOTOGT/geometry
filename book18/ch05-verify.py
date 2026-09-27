#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book18/ch05-verify.py -- every number on book18/ch05-off-the-line.html. Run first (R24).

    python3 book18/ch05-verify.py [--downloads DIR]

  [1] Loomis & Sternberg §10.6: the divergence theorem (p. 421)
  [2] Hubble flow v = H r: divergence 3H, and flux through a sphere = 3H x volume, by quadrature
  [3] Planck 2018 VI inputs, read off the paper; Hubble time, volume growth, doubling times
  [4] the visible universe: particle horizon and last-scattering distance, integrated
  [5] the moving boundary: the visible volume grows faster than the comoving flow, by c/(H0 D)
  [HONESTY]
"""
import math, os, re, subprocess, sys
from pathlib import Path
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def dl():
    if "--downloads" in sys.argv: return Path(sys.argv[sys.argv.index("--downloads") + 1])
    for c in ("~/mnt/Downloads", "~/Downloads"):
        p = Path(os.path.expanduser(c))
        if p.is_dir(): return p
DL = dl()
flat = lambda s: re.sub(r"\s+", " ", s)
txt = lambda n: subprocess.run(["pdftotext", "-layout", str(DL / n), "-"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, timeout=170).stdout.split("\f")

print("[1] Loomis & Sternberg")
L = txt("Advanced_Calculus.pdf")
l421 = flat(L[432])
check("p.421: §10.6, 'Theorem 6.1 (The divergence theorem)'", "10.6 THE DIVERGENCE THEOREM 421" in l421 and "(The divergence theorem)" in l421)
check("p.423: the version with a Riemann metric, volume density dV and outward unit normal n", "volume density" in flat(L[434]) and "points out of D" in flat(L[434]))

print("[2] the Hubble flow v = H r")
H = 1.0
v = lambda x, y, z: (H * x, H * y, H * z)
e = 1e-5; p0 = (0.3, -0.7, 1.1)
div = sum((v(*[p0[k] + (e if k == i else 0) for k in range(3)])[i] - v(*[p0[k] - (e if k == i else 0) for k in range(3)])[i]) / (2 * e) for i in range(3))
check("div v = 3H at a sample point", abs(div - 3 * H) < 1e-9, f"{div:.9f}")
R, n = 2.0, 400
flux = 0.0
for i in range(n):                                       # midpoint rule over the sphere
    th = (i + 0.5) * math.pi / n
    for j in range(2 * n):
        ph = (j + 0.5) * math.pi / n
        nx, ny, nz = math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph), math.cos(th)
        vx, vy, vz = v(R * nx, R * ny, R * nz)
        flux += (vx * nx + vy * ny + vz * nz) * R * R * math.sin(th) * (math.pi / n) ** 2
vol = 4 / 3 * math.pi * R ** 3
check("flux out of a sphere of radius 2 = (div v) x volume = 3H x 4/3 pi R^3", abs(flux - 3 * H * vol) / (3 * H * vol) < 1e-4, f"{flux:.5f} vs {3*H*vol:.5f}")

print("[3] Planck 2018 VI")
P = txt("Planck 2018 results. VI. Cosmological parameters.pdf")
p14, p15, p16 = flat(P[13]), flat(P[14]), flat(P[15])
check("p.15 Table 1: H0 = 67.36 +/- 0.54", "67.36 ± 0.54" in p15)
check("p.15 Table 1: Omega_m h^2 = 0.1430", "0.1430 ± 0.0011" in p15)
check("p.14 fn 14: T0 = 2.7255 K", "T 0 = 2.7255K" in p14)
check("p.16 Table 2: z* = 1089.92", "1089.92 ± 0.25" in p16)
H0, omh2, T0, zs = 67.36, 0.1430, 2.7255, 1089.92
Mpc, c, yr, Gyr = 3.0856775814913673e22, 299792458.0, 3.15576e7, 3.15576e16
ly = c * yr
Hs = H0 * 1e3 / Mpc
tH = 1 / Hs / Gyr
print(f"     Hubble time 1/H0 = {tH:.2f} Gyr; Hubble radius c/H0 = {c/Hs/ly/1e9:.2f} billion light-years")
per_year = 3 * Hs * yr
print(f"     comoving volume grows by 3 H0 = {per_year:.3e} of itself per year")
print(f"     at today's rate: volume doubles in ln2/(3H0) = {math.log(2)/(3*Hs)/Gyr:.2f} Gyr; distances in ln2/H0 = {math.log(2)/Hs/Gyr:.2f} Gyr")
check("volume doubling time at today's rate is between 3 and 4 billion years", 3 < math.log(2) / (3 * Hs) / Gyr < 4)

print("[4] the visible universe (flat LCDM from these inputs)")
h = H0 / 100; om = omh2 / h**2
orad = 2.469e-5 * (T0 / 2.7255)**4 * (1 + 0.2271 * 3.046) / h**2
ol = 1 - om - orad
E = lambda z: math.sqrt(om * (1+z)**3 + orad * (1+z)**4 + ol)
def comoving(z1, z2, n=400000):                           # c * int dz/H over ln(1+z)
    lo, hi = math.log(1 + z1), math.log(1 + z2); dx = (hi - lo) / n; s = 0.0
    for k in range(n):
        x = lo + (k + 0.5) * dx; zz = math.exp(x) - 1
        s += dx * (1 + zz) / E(zz)
    return c / Hs * s                                     # metres
D_hor = comoving(0, 1e9); D_ls = comoving(0, zs)
print(f"     particle horizon, comoving radius: {D_hor/ly/1e9:.1f} billion light-years ({D_hor/Mpc/1e3:.2f} Gpc)")
print(f"     last-scattering sphere, comoving radius: {D_ls/ly/1e9:.1f} billion light-years")
check("the visible universe is about 46 billion light-years in radius", 45 < D_hor / ly / 1e9 < 47.5)
check("the bright wall sits within 2% of the horizon", 0.97 < D_ls / D_hor < 1.0, f"{D_ls/D_hor:.4f}")

print("[5] the moving boundary")
ratio = c / (Hs * D_hor)
print(f"     dV/dt = 3 H0 V  +  4 pi D^2 c ;   second term / first = c/(H0 D) = {ratio:.3f}")
check("the horizon's own motion adds about 30% to the visible volume's growth", 0.28 < ratio < 0.33)
Vvis = 4 / 3 * math.pi * D_hor**3
grow = (3 * Hs * Vvis + 4 * math.pi * D_hor**2 * c) * yr / ly**3
print(f"     the visible universe gains {grow:.2e} cubic light-years per year")

print("""
[HONESTY]
[1] matches text in the ledgered Loomis & Sternberg. [2] is a quadrature check of the
theorem on one field, not a proof. [3]-[5] read five numbers off Planck 2018 VI and
integrate flat LCDM with them (radiation from T0 with N_eff = 3.046 and the standard
2.469e-5 photon density coefficient, which is not read from the paper). The 46-billion-
light-year horizon and the 30% boundary term are this script's integrals, not quotations.
'Doubling time at today's rate' holds H fixed; H is falling, so the true doubling is slower.
""")
print(f"{len(FAIL)} FAIL")
sys.exit(1 if FAIL else 0)
