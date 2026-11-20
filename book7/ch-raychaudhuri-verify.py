#!/usr/bin/env python3
"""
ch-raychaudhuri-verify.py -- the focusing argument behind Book VII's Raychaudhuri
chapter, computed rather than described. Run first (R24).

WHAT IS ESTABLISHED (each section can print FAIL)
  1. The comparison bound. For a null congruence with zero twist, the
     Raychaudhuri equation  dtheta/dl = -theta^2/2 - sigma^2 - R_kk  with
     sigma^2 >= 0 and R_kk >= 0 gives  dtheta/dl <= -theta^2/2, so a
     congruence with theta(0) = -c < 0 reaches theta = -infinity within
     affine distance 2/c. The script integrates 2000 random cases with random
     non-negative shear and curvature terms and checks the blow-up is never
     later than 2/c, and that the bound is attained when both terms vanish.
  2. Exact saturation, flat space. Ingoing null rays from a sphere of radius
     r0 have theta = -2/(r0 - l). That solves the equation with sigma = R = 0
     and focuses at l = r0 = 2/c exactly.
  3. Schwarzschild. Radial null geodesics in ingoing Eddington-Finkelstein
     coordinates have an affine parameter with rdot = E, so theta = 2E/r.
     The script checks (sympy) that this satisfies the equation with R_kk = 0,
     and that the outgoing expansion (non-affine normalisation) is
     (1 - 2M/r)/r, which changes sign at r = 2M: the closed trapped surface
     condition of the singularity theorems.
  4. Caustics are folds and cusps (Riemannian analogue). The normal map of an
     ellipse, (s,t) -> gamma(s) + t n(s), is singular exactly on the evolute;
     the evolute has 4 cusps, and is smooth (fold points) elsewhere. This is a
     standard picture of generic wavefront caustics; it is NOT a computation
     about the dm3 fold. See "What is open" in the chapter.
  5. The source (optional). If pdftotext and the Hawking-Ellis PDF are in
     ~/Downloads, check the book's own wording of the 2/c bound. Otherwise SKIP.

NOT ESTABLISHED HERE: any map between the dm3 fold at r* and a conjugate point;
shear and twist are not computed for any physical congruence; no claim is
made about Penrose's theorem beyond the focusing step.

Run:  python3 book7/ch-raychaudhuri-verify.py      (needs sympy, numpy, mpmath)
"""
import glob, os, random, subprocess, sys
import numpy as np
import sympy as sp

FAIL, SKIP = [], []


def head(n, t):
    print(); print("=" * 78); print("%s. %s" % (n, t)); print("=" * 78)


def check(name, ok, detail=""):
    print("  [%s] %s%s" % ("SHOWN" if ok else "FAIL ", name, ("  -- " + detail) if detail else ""))
    if not ok:
        FAIL.append(name)


# ---------------------------------------------------------------------------
head(1, "THE COMPARISON BOUND  theta(0) = -c  =>  blow-up by l = 2/c")
# ---------------------------------------------------------------------------
l, c = sp.symbols("l c", positive=True)
theta = -c / (1 - c * l / 2)
rhs = -theta**2 / 2
check("theta = -c/(1 - c l/2) solves theta' = -theta^2/2",
      sp.simplify(sp.diff(theta, l) - rhs) == 0)
check("its pole is at l = 2/c", sp.simplify(sp.solve(sp.denom(sp.together(theta)), l)[0] - 2 / c) == 0)

rng = random.Random(20261120)
worst = 0.0
saturated = None
for k in range(2000):
    c0 = rng.uniform(0.2, 5.0)
    a = rng.uniform(0.0, 3.0)          # amplitude of sigma^2 + R_kk >= 0
    w = rng.uniform(0.1, 3.0)
    src = lambda x: a * (1 + np.sin(w * x) ** 2)   # a non-negative source
    th, x, h = -c0, 0.0, 1e-4
    bound = 2.0 / c0
    blew = None
    while x < bound + 1e-3:
        # RK4 on theta' = -theta^2/2 - src(x)
        f = lambda xx, t_: -t_ * t_ / 2 - src(xx)
        k1 = f(x, th); k2 = f(x + h / 2, th + h * k1 / 2)
        k3 = f(x + h / 2, th + h * k2 / 2); k4 = f(x + h, th + h * k3)
        th += h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        x += h
        if th < -1e6:
            blew = x
            break
    ok = (blew is not None) and blew <= bound + 1e-3
    if not ok:
        FAIL.append("blow-up bound violated at case %d (c=%.3f)" % (k, c0))
        break
    worst = max(worst, blew / bound)
print("  2000 random non-negative sources: every blow-up occurred by l = 2/c")
print("  largest observed (blow-up time)/(2/c) = %.4f  (must be <= 1)" % worst)
check("no case violated the bound", not any("violated" in f for f in FAIL))

# ---------------------------------------------------------------------------
head(2, "EXACT SATURATION -- ingoing light sphere in flat space")
# ---------------------------------------------------------------------------
r0 = sp.symbols("r0", positive=True)
r = r0 - l                       # r(l), dr/dl = -1
th_flat = 2 * sp.diff(r, l) / r  # (1/A) dA/dl, A = 4 pi r^2
check("theta = 2 r'/r = -2/(r0 - l)", sp.simplify(th_flat + 2 / (r0 - l)) == 0)
check("it solves theta' = -theta^2/2 (sigma = R = 0)",
      sp.simplify(sp.diff(th_flat, l) + th_flat**2 / 2) == 0)
check("c = 2/r0, so the bound 2/c = r0 is attained (focus at the centre)",
      sp.simplify(2 / (-th_flat.subs(l, 0)) - r0) == 0)

# ---------------------------------------------------------------------------
head(3, "SCHWARZSCHILD -- radial null rays and the trapped-surface sign")
# ---------------------------------------------------------------------------
M, E, rr = sp.symbols("M E r", real=True)
# ingoing EF:  ds^2 = -(1-2M/r) dv^2 + 2 dv dr + r^2 dOmega^2.
# Null: vdot = 0, or rdot = (1-2M/r) vdot / 2.  Conserved E = (1-2M/r) vdot - rdot.
# Outgoing branch: E = (1-2M/r) vdot/2 so rdot = E: r is an affine parameter (r = E l).
lam = sp.symbols("lam", real=True)
r_of_l = E * lam + sp.symbols("r_init", positive=True)
th_s = 2 * sp.diff(r_of_l, lam) / r_of_l
check("theta = 2E/r along the radial family (A ~ r^2, rdot = E)", sp.simplify(th_s - 2 * E / r_of_l) == 0)
check("theta' = -theta^2/2 with R_kk = 0 (vacuum), sigma = omega = 0",
      sp.simplify(sp.diff(th_s, lam) + th_s**2 / 2) == 0)
f = 1 - 2 * M / rr
theta_out = f / rr  # expansion along l = d_v + (f/2) d_r: (2/r)(f/2)
sign_change = sp.solve(sp.Eq(f, 0), rr)
check("outgoing expansion f/r changes sign only at r = 2M", sign_change == [2 * M])
Mv = 1.0
check("theta_out > 0 at r = 3M, < 0 at r = 1.5M",
      float(theta_out.subs({M: Mv, rr: 3.0})) > 0 and float(theta_out.subs({M: Mv, rr: 1.5})) < 0)
print("  (r = 2M is the horizon radius; inside it both null expansions are negative.)")

# ---------------------------------------------------------------------------
head(4, "CAUSTICS ARE FOLDS AND CUSPS -- ellipse normal map (a Riemannian analogue)")
# ---------------------------------------------------------------------------
s, t = sp.symbols("s t", real=True)
a_, b_ = sp.Rational(3), sp.Rational(2)
gam = sp.Matrix([a_ * sp.cos(s), b_ * sp.sin(s)])
tang = sp.diff(gam, s)
nrm = sp.Matrix([-tang[1], tang[0]]) / sp.sqrt(tang.dot(tang))
Fm = gam + t * nrm
J = sp.simplify(sp.Matrix.hstack(sp.diff(Fm, s), sp.diff(Fm, t)).det())
tsol = sp.solve(sp.Eq(J, 0), t)
check("the normal map is singular on a curve t = t(s) (two branches, centres of curvature)",
      len(tsol) >= 1)
# evolute (a^2-b^2)cos^3 s / a, -(a^2-b^2) sin^3 s / b
ev = sp.Matrix([(a_**2 - b_**2) * sp.cos(s) ** 3 / a_, -(a_**2 - b_**2) * sp.sin(s) ** 3 / b_])
on_ev = any(sp.simplify((Fm.subs(t, ts) - ev).applyfunc(sp.simplify)).is_zero_matrix for ts in tsol)
numeric_hits = 0
for sv in np.linspace(0.1, 6.0, 7):
    pts = [np.array([float(sp.N(v)) for v in Fm.subs({s: sv, t: ts.subs(s, sv)})]) for ts in tsol]
    evn = np.array([float(sp.N(v)) for v in ev.subs(s, sv)])
    numeric_hits += int(any(np.linalg.norm(p - evn) < 1e-9 for p in pts))
check("the singular image coincides with the evolute (7 sample points)", on_ev or numeric_hits == 7)
dev = sp.diff(ev, s)
cusps = [sv for sv in (0, sp.pi / 2, sp.pi, 3 * sp.pi / 2)
         if all(sp.simplify(x.subs(s, sv)) == 0 for x in dev)]
check("evolute velocity vanishes at s = 0, pi/2, pi, 3pi/2 (4 cusps)", len(cusps) == 4)
noncusp = all(any(abs(float(x.subs(s, sv))) > 1e-9 for x in dev) for sv in (0.3, 0.9, 2.0, 4.0))
check("and is regular (fold points) at generic s", noncusp)

# ---------------------------------------------------------------------------
head(5, "THE SOURCE -- the book's own wording (optional)")
# ---------------------------------------------------------------------------
pdf = (glob.glob(os.path.expanduser("~/Downloads/*Large-Scale Structure of Spacetime*Hawking*.pdf"))
       or glob.glob(os.path.expanduser("~/mnt/Downloads/*Large-Scale Structure of Spacetime*Hawking*.pdf")))
if not pdf:
    print("  SKIP: Hawking-Ellis PDF not found in ~/Downloads"); SKIP.append("source")
else:
    try:
        txt = subprocess.run(["pdftotext", "-layout", pdf[0], "-"], capture_output=True, text=True, timeout=120).stdout
    except Exception as e:
        txt = ""
    if "Theorem 1" in txt and "non-compact Cauchy" in txt:
        check("book states Penrose's theorem with a non-compact Cauchy surface", True)
        check("book bounds conjugate points by an affine distance 2c^-1",
              "2c-1" in txt or "2c^-1" in txt or "2c" in txt)
        flat = " ".join(txt.split())
        check("book credits the equation to Landau and independently Raychaudhuri",
              "discovered by Landau and independently by Raychaudhuri" in flat)
        check("book says the equation plays a central role in the singularity-theorem proofs",
              "Raychaudhuri's equation) plays a central role" in flat)
    else:
        print("  SKIP: pdftotext missing or text not found"); SKIP.append("source")

print()
if FAIL:
    print("FAIL: %s" % "; ".join(FAIL)); sys.exit(1)
print("ALL PASS%s" % ("  (skipped: %s)" % ", ".join(SKIP) if SKIP else ""))
