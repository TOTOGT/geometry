#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book21/ch02-verify.py -- every number on book21/ch02-topological-conjugacy.html. Run first (R24).

    python3 book21/ch02-verify.py [--downloads DIR]

  [1] Strogatz (2018) p.156: "topologically equivalent", defined; the Strogatz file's hash
  [2] an explicit homeomorphism taking the corpus's immune spiral (mu = -0.44) to its
      market spiral (mu = -0.67): built, and the conjugacy equation checked
  [3] the same construction taking a spiral to a NODE: topology cannot tell them apart
  [4] why no linear map does this: h is not differentiable in both directions at 0
  [HONESTY]
"""
import cmath, hashlib, math, os, re, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
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
ST = "Nonlinear_Dynamics_and_Chaos_2018_Steven_H._Strogatz.pdf"
flat = lambda s: re.sub(r"\s+", " ", s)

print("[1] Strogatz")
try:
    h = hashlib.sha256((DL / ST).read_bytes()).hexdigest()
    check("the file is the ledgered printing (sha256 e4c3681c...)", h.startswith("e4c3681c"))
    P = subprocess.run(["pdftotext", "-layout", str(DL / ST), "-"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, timeout=170).stdout.split("\f")
    p156 = flat(P[170])
    check("pdf page 171 is printed p.156 (footer '156 PHASE PLANE')", "156 PHASE PLANE" in p156)
    check("p.156: 'topologically equivalent' means a homeomorphism mapping trajectories onto trajectories", "there is a homeomorphism" in p156 and "trajectories map onto trajectories" in p156)
    check("p.156: 'Bending and warping are allowed, but not ripping'", "Bending and warping are allowed, but not ripping" in p156)
except Exception as e:
    print("SKIP Strogatz", e)

print("[2] immune (mu = -0.44) to market (mu = -0.67), book21/Spiral.lean")
src = (ROOT / "book21/Spiral.lean").read_text(encoding="utf-8")
check("Spiral.lean: spiral mu omega = [[mu, -omega], [omega, mu]]", "!![μ, -ω; ω, μ]" in src)
check("Spiral.lean: immune_is_not_market uses -0.44 and -0.67", "spiral (-0.44) ω" in src and "spiral (-0.67) ω'" in src)
def flow(mu, om):                       # the flow of spiral(mu, om) on complex numbers z = x + iy
    return lambda z, t: z * cmath.exp(complex(mu, om) * t)
def conj(mu, om, mu2, om2):             # h: send the point that crosses |z| = 1 at time -t to the one that does so for the target
    def h(z):
        if z == 0: return 0j
        r, th = abs(z), cmath.phase(z)
        t = math.log(r) / mu                          # z = phi_t(y) with |y| = 1
        y = cmath.exp(1j * (th - om * t))
        return y * cmath.exp(complex(mu2, om2) * t)
    return h
mu, om, mu2, om2 = -0.44, 1.0, -0.67, 1.7
phi, psi, h = flow(mu, om), flow(mu2, om2), conj(mu, om, mu2, om2)
pts = [complex(a, b) for a in (-2, -0.3, 0.7, 3) for b in (-1.5, 0.2, 2.5)]
err = max(abs(h(phi(z, s)) - psi(h(z), s)) for z in pts for s in (-3, -0.5, 0.8, 4))
check("h(phi_s(z)) = psi_s(h(z)) on 12 points x 4 times", err < 1e-9, f"max error {err:.1e}")
hinv = conj(mu2, om2, mu, om)
err2 = max(abs(hinv(h(z)) - z) for z in pts)
check("h has a continuous inverse of the same form", err2 < 1e-9, f"{err2:.1e}")
check("h(0) = 0 and h is continuous there: |h(z)| = |z|^(0.67/0.44)", abs(abs(h(1e-6 + 0j)) - (1e-6) ** (mu2 / mu)) < 1e-15)

print("[3] a spiral to a node")
A = ((-1.0, 0.0), (0.0, -2.0))
def nflow(v, t): return (v[0] * math.exp(-t), v[1] * math.exp(-2 * t))
def ncross(v):                          # the time t with |nflow(v, -t)| = 1, i.e. v = nflow(y, t), |y| = 1
    lo, hi = -60.0, 60.0
    f = lambda t: math.hypot(*nflow(v, -t)) - 1
    for _ in range(200):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if f(m) < 0 else (lo, m)
    return (lo + hi) / 2
def h_ns(v):                            # node -> spiral(mu, om)
    if v == (0.0, 0.0): return 0j
    t = ncross(v); y = nflow(v, -t)
    return complex(*y) * cmath.exp(complex(mu, om) * t)
vpts = [(a, b) for a in (-2.0, 0.4, 1.5) for b in (-1.0, 0.3, 2.0)]
err3 = max(abs(h_ns(nflow(v, s)) - phi(h_ns(v), s)) for v in vpts for s in (-1.0, 0.5, 2.0))
check("a node and a spiral sink are topologically conjugate: the same equation holds", err3 < 1e-8, f"max error {err3:.1e}")
check("the node's matrix has real eigenvalues -1, -2: no rotation at all", A[0][1] == A[1][0] == 0)

print("[4] why no linear map does this")
for eps in (1e-2, 1e-4, 1e-6):
    q = abs(hinv(complex(eps, 0))) / eps
    print(f"     |h^-1(z)| / |z| at |z| = {eps:.0e}: {q:.3e}")
check("|h^-1(z)|/|z| -> infinity as z -> 0: the inverse is not differentiable at the fixed point",
      abs(hinv(complex(1e-6, 0))) / 1e-6 > 100)

print("[5] the general theorem, now held: Hirsch, Smale & Devaney (2013) §4.2, pp. 65-68")
try:
    Q = subprocess.run(["pdftotext", "-layout", str(DL / 'Smale, Stephen T_Devaney, Robert L - Differential equations, dynamical systems, and an introduction to chaos (2012_2013, Elsevier, Academic Press).pdf'), "-"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, timeout=170).stdout.split("\f")
    q65, q66, q67, q68 = (flat(Q[i]) for i in (79, 80, 81, 82))
    check("p.65: (topologically) conjugate, defined by phi_B(t, h(X0)) = h(phi_A(t, X0))", q65.strip().startswith("4.2 Dynamical Classification 65") and "(topologically) conjugate" in q65)
    check("p.66: the theorem -- hyperbolic 2x2 systems are conjugate iff they have the same number of eigenvalues with negative real part",
          "are conjugate if and only if each matrix has the same number of eigenvalues with negative real part" in q66)
    check("p.66: 'a system with a spiral sink is conjugate to a system with a (real) sink. Of course!'", "a spiral sink is conjugate to a system with a (real) sink. Of course!" in q66)
    check("p.66: h is not differentiable at the origin -- 'the reason we require h to be only a homeomorphism'", "the reason we require h to be only a homeomorphism" in q66)
    check("pp.67-68: the proof is the crossing-time construction through the unit circle S1", "each nonzero solution of X 0 = AX crosses S1 exactly" in q68 or "crosses S1 exactly once" in q68)
except Exception as e:
    print("SKIP HSD", e)

print("""
[HONESTY]
[2]-[3] build conjugacies by the standard crossing-time construction and check the
conjugacy equation numerically at sample points; that is evidence, not a proof. The
general theorem is Hirsch, Smale & Devaney's (p.66, proof pp.67-68, [5]); [2]-[3]
are instances of their construction, run. The omegas (1.0, 1.7)
are free choices: the Lean file quantifies over them, and the construction works for any.
""")
print(f"{len(FAIL)} FAIL")
sys.exit(1 if FAIL else 0)
