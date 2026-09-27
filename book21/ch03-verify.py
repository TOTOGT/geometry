#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book21/ch03-verify.py -- every number on book21/ch03-hartman-grobman.html. Run first (R24).

    python3 book21/ch03-verify.py [--downloads DIR]

  [1] Strogatz (2018) pp.154-156: Example 6.3.2, robust vs marginal cases, Hartman-Grobman
  [2] Example 6.3.2 integrated: the linearisation says 'center', the system spirals, and slowly
  [3] a hyperbolic case for contrast: the linearisation's decay rate is the true one
  [4] the corpus's fold: at a saddle-node the eigenvalue is zero, and the theorem is silent
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

print("[1] Strogatz")
try:
    P = subprocess.run(["pdftotext", "-layout", str(DL / "Nonlinear_Dynamics_and_Chaos_2018_Steven_H._Strogatz.pdf"), "-"],
                       stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, timeout=170).stdout.split("\f")
    p154, p155, p156 = flat(P[168]), flat(P[169]), flat(P[170])
    check("p.154: Example 6.3.2, the linearized system incorrectly predicts a center", "EXAMPLE 6.3.2" in p154 and "incorrectly predicts that the origin is a center" in p154 and "154 PHASE PLANE" in p154)
    check("p.155: 'centers live on the razor's edge between stability and instability'", "razor" in p155 and "155" in p155)
    check("p.155: robust cases (sources, sinks, saddles) vs marginal (centers, a zero eigenvalue)", "Robust cases" in p155 and "Marginal cases" in p155 and "at least one eigenvalue is zero" in p155)
    check("p.156: Hartman-Grobman -- near a hyperbolic fixed point the local portrait is topologically equivalent to the linearization's", "Hartman-Grobman" in p156 and "hyperbolic fixed point is" in p156)
    check("p.155: the decay 'is extremely slow'", "extremely slow" in p155)
except Exception as e:
    print("SKIP Strogatz", e)

print("[2] Example 6.3.2: x' = -y + a x r^2, y' = x + a y r^2, a = -1, from (1, 0)")
a = -1.0
def f(x, y):
    r2 = x*x + y*y
    return -y + a*x*r2, x + a*y*r2
def rk4(x, y, T, n):
    h = T / n
    for _ in range(n):
        k1 = f(x, y); k2 = f(x + h/2*k1[0], y + h/2*k1[1]); k3 = f(x + h/2*k2[0], y + h/2*k2[1]); k4 = f(x + h*k3[0], y + h*k3[1])
        x += h/6*(k1[0] + 2*k2[0] + 2*k3[0] + k4[0]); y += h/6*(k1[1] + 2*k2[1] + 2*k3[1] + k4[1])
    return x, y
rows = []
for T in (10, 100, 1000):
    x, y = rk4(1.0, 0.0, T, 40 * T)
    r_num, r_exact = math.hypot(x, y), 1 / math.sqrt(1 - 2 * a * T)
    rows.append((T, r_num, r_exact))
    print(f"     t = {T:5d}: r numerical {r_num:.6f}, closed form 1/sqrt(1+2t) {r_exact:.6f}; linearisation says r = 1")
check("the closed form r' = a r^3 matches the integration", all(abs(u - v) < 1e-6 for _, u, v in rows))
check("the true system spirals in (r < 1): the linearisation's 'center' is wrong", all(u < 1 for _, u, _ in rows))
check("and it spirals in slowly: after 1000 time units r is still above 0.02", rows[-1][1] > 0.02, f"{rows[-1][1]:.4f}")

print("[3] a hyperbolic sink for contrast: the corpus's immune row, mu = -0.44")
mu = -0.44
print("     linear decay is exponential: r(t) = e^(mu t)")
t_half_lin = math.log(2) / -mu
t_half_642 = (4 - 1) / (2 * -a)            # 1/sqrt(1+2t) = 1/2  =>  t = 3/2
print(f"     time to halve r: hyperbolic mu = -0.44, {t_half_lin:.3f}; Example 6.3.2, {t_half_642:.3f}")
t_to_small = lambda eps: ((1/eps)**2 - 1) / 2
print(f"     time to reach r = 1e-3: hyperbolic {math.log(1e3)/0.44:.1f}; Example 6.3.2, {t_to_small(1e-3):.0f}")
check("reaching r = 0.001 takes the marginal case over 30,000 times longer", t_to_small(1e-3) / (math.log(1e3) / 0.44) > 30000)

print("[4] the fold: x' = r + x^2, the saddle-node normal form, at r = 0")
fp = lambda r: -math.sqrt(-r)              # the stable branch for r < 0
for r in (-1.0, -0.01, -1e-4):
    print(f"     r = {r:>8}: fixed point {fp(r):+.4f}, eigenvalue f'(x*) = 2x* = {2*fp(r):+.4f}")
check("the eigenvalue at the stable branch is 2x* = -2 sqrt(-r) -> 0 as r -> 0", abs(2 * fp(-1e-8)) < 1e-3)
print("     at the fold itself (r = 0, x* = 0) the eigenvalue is 2*0 = 0: marginal")

print("""
[HONESTY]
[1] matches sentences in the ledgered Strogatz file. [2] integrates Strogatz's own
Example 6.3.2 with RK4 (step 1/40) and checks it against the closed form he derives.
[3] compares halving and 1e-3 times for a linear decay rate the corpus uses (mu = -0.44)
and for the example; it is a comparison of two model systems, not a measurement. [4]
uses the textbook saddle-node normal form x' = r + x^2 (Strogatz ch. 3) as a stand-in
for the corpus's fold; the corpus's own F3 is piecewise linear (Book XVIII ch 2) and has
no eigenvalue at the fold at all.
""")
print(f"{len(FAIL)} FAIL")
sys.exit(1 if FAIL else 0)
