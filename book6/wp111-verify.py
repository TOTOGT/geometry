#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""wp111-verify.py — companion to book6/wp111-the-cardioid-is-the-locus.html.

Eight blocks, standard library only. Every number in the paper is produced here.

  [1] The multiplier of the fixed point of z -> z^2 + c, and the closed form of
      the curve on which it has modulus one.
  [2] The landmarks on that curve, against their exact values: the cusp at 1/4,
      the period-doubling root at -3/4, the 1/3 bulbs, the 1/4 bulb.
  [3] That crossing the curve is a bifurcation and not a coordinate artefact:
      the orbit is asymptotically fixed just inside and is not just outside.
  [4] That the bulb rooted at internal angle p/q carries an attracting cycle of
      period exactly q. This is the claim that makes the crossing a Hopf-type
      event with a rotation number, rather than a generic loss of stability.
  [5] The corpus's own continuous-time Hopf reduction, CardiacHopfReduction.lean,
      checked independently: rdot = mu r - r^3 / L on random states, the
      limit-cycle amplitude, and the sign that makes it supercritical.
  [6] Where the two part. For a smooth map the Neimark-Sacker picture depends on
      a nondegeneracy condition and nothing else. In the holomorphic case it
      depends on the ARITHMETIC of the rotation number: the Brjuno sum over the
      continued-fraction convergents converges for some irrationals and diverges
      for others that are arbitrarily close to them. That is computed here.
  [7] The cross-references resolve, at the paths the paper cites.

Run:  python3 book6/wp111-verify.py      (from the repository root)

Principia Orthogona - Vol VI - G6 LLC - CC BY-NC-ND 4.0
"""
import cmath, math, os, random, sys

FAIL = []
def check(label, ok, detail=""):
    print(f"    {'PASS' if ok else 'FAIL'}  {label}" + (f"   {detail}" if detail else ""))
    if not ok: FAIL.append(label)
    return ok

def c_of(theta):
    """The point of the main cardioid at internal angle theta."""
    z = cmath.exp(1j*theta)/2
    return z - z*z

print("\n[1] The multiplier, and the curve on which it has modulus one")
print("    z* = z*^2 + c  =>  lambda = 2 z*.   |lambda| = 1  =>  z* = e^{i t}/2")
print("    c(t) = z* - z*^2 = e^{i t}/2 - e^{2 i t}/4")
worst = 0.0
for k in range(400):
    t = 2*math.pi*k/400
    c = c_of(t); z = cmath.exp(1j*t)/2
    worst = max(worst, abs(abs(2*z) - 1.0), abs(z*z + c - z))
check("|lambda| = 1 and z* is fixed, all along the curve", worst < 1e-12,
      f"max deviation over 400 angles = {worst:.2e}")

print("\n[2] Landmarks, against exact values")
land = [("cusp, t = 0",           0.0,     complex(0.25, 0.0),  "saddle-node, lambda = +1"),
        ("period-2 root, t = pi", math.pi, complex(-0.75, 0.0), "period doubling, lambda = -1")]
for nm, t, exact, note in land:
    got = c_of(t)
    print(f"    {nm:24s} c = {got.real:+.12f}{got.imag:+.12f}i   exact {exact}")
    check(nm, abs(got - exact) < 1e-12, note or "")
# the 1/3 and 1/4 roots in closed form
c13 = c_of(2*math.pi/3); c14 = c_of(math.pi/2)
ex13 = complex(-0.125,  3*math.sqrt(3)/8)
ex14 = complex(0.25, 0.5)
print(f"    1/3 bulb, t = 2pi/3      c = {c13.real:+.12f}{c13.imag:+.12f}i   exact -1/8 + 3sqrt3/8 i")
check("the 1/3 bulb root is -1/8 + 3*sqrt(3)/8 i", abs(c13 - ex13) < 1e-12)
print(f"    1/4 bulb, t = pi/2       c = {c14.real:+.12f}{c14.imag:+.12f}i   exact 1/4 + 1/2 i")
check("the 1/4 bulb root is 1/4 + i/2", abs(c14 - ex14) < 1e-12)

print("\n[3] Crossing the curve is a bifurcation")
def settle(c, warm=6000, probe=1):
    z = 0j
    for _ in range(warm):
        z = z*z + c
        if abs(z) > 4: return float('inf'), z
    z0 = z
    for _ in range(probe): z = z*z + c
    return abs(z - z0), z
for t in (2*math.pi/3, math.pi/2, 1.0):
    base = c_of(t)
    din, _ = settle(base*0.99)
    dout, _ = settle(base*1.01)
    print(f"    t={t:.4f}   |z_{{n+1}}-z_n| inside = {din:.2e}    outside = {dout:.2e}")
    check(f"fixed point attracts inside, not outside (t={t:.3f})", din < 1e-9 < dout)

print("\n[4] The bulb at internal angle p/q carries a cycle of period q")
def cycle_period(c, warm=20000, maxq=24, tol=1e-7):
    z = 0j
    for _ in range(warm):
        z = z*z + c
        if abs(z) > 4: return None
    z0 = z; w = z
    for q in range(1, maxq+1):
        w = w*w + c
        if abs(w - z0) < tol: return q
    return None
for p, q in [(1,2), (1,3), (2,3), (1,4), (1,5), (2,5), (1,6), (3,7)]:
    root = c_of(2*math.pi*p/q)
    inside = root * 1.0 + (root/abs(root)) * 0.012      # a short step outward from the cusp side
    per = cycle_period(inside)
    print(f"    p/q = {p}/{q}:  root c = {root.real:+.9f}{root.imag:+.9f}i   period found = {per}")
    check(f"the {p}/{q} bulb has period {q}", per == q, f"got {per}")

print("\n[5] CardiacHopfReduction.lean, checked independently of the kernel")
print("    The file has been kernel-audited since 2026-09-12 (block [8] reads the")
print("    evidence). This block is kept because it checks something the kernel")
print("    does not: that the radial identity holds on states, numerically, by a")
print("    route that shares no code with the Lean proof.")
random.seed(11)
worst_r = 0.0
for _ in range(2000):
    mu = random.uniform(0.05, 2.0); L = random.uniform(0.3, 3.0); w = random.uniform(0.1, 3.0)
    r  = random.uniform(0.05, 1.5); th = random.uniform(0, 2*math.pi)
    x, y = r*math.cos(th), r*math.sin(th)
    u  = (x*x + y*y)/L
    fx = mu*x - w*y - x*u
    fy = w*x + mu*y - y*u
    rdot = (x*fx + y*fy)/r
    worst_r = max(worst_r, abs(rdot - (mu*r - r**3/L)))
check("rdot = mu r - r^3 / L, identically", worst_r < 1e-12, f"max residual {worst_r:.2e}")
for mu, L in [(0.7, 1.3), (1.5, 0.4), (0.2, 2.2)]:
    rs = math.sqrt(mu*L)
    print(f"    mu={mu:<4} L={L:<4} r* = sqrt(mu L) = {rs:.9f}   rdot(r*) = {mu*rs - rs**3/L:+.2e}"
          f"   d/dr = {mu - 3*rs*rs/L:+.6f}")
    check(f"r* is a zero and is attracting (mu={mu}, L={L})",
          abs(mu*rs - rs**3/L) < 1e-12 and abs((mu - 3*rs*rs/L) - (-2*mu)) < 1e-12,
          "derivative is exactly -2 mu, so supercritical for every mu > 0")
print("    the rotation frequency omega drops out of the radial equation entirely;")
print("    nothing in this reduction depends on whether omega is rational.")

print("\n[6] Where the holomorphic case parts from the smooth one")
print("    Both numbers below are DEFINED by their continued fractions, so the")
print("    convergents are exact integers and no floating point enters the q's.")

def convergents_from_cf(a):
    p0, q0, p1, q1 = 1, 0, a[0], 1
    out = [(p1, q1)]
    for k in a[1:]:
        p0, q0, p1, q1 = p1, q1, k*p1 + p0, k*q1 + q0
        out.append((p1, q1))
    return out

def brjuno_partials(a):
    cv = convergents_from_cf(a); s = 0.0; out = []
    for i in range(len(cv) - 1):
        q, qn = cv[i][1], cv[i+1][1]
        if q == 0: continue
        s += math.log(qn) / q; out.append(s)
    return out

# golden mean: [0; 1, 1, 1, ...]  -- the slowest-growing partial quotients there are
gold_cf = [0] + [1]*30
gt = brjuno_partials(gold_cf)
print("    golden mean  [0;1,1,1,...]")
print("      partial sums: " + ", ".join(f"{v:.4f}" for v in gt[:8]) + f"  ...  {gt[-1]:.6f}")

# a Brjuno-divergent number, built so each term is at least 1:
#   choose a_{n+1} >= exp(q_n), so log(q_{n+1})/q_n >= log(a_{n+1})/q_n >= 1.
div_cf = [0, 1]
while True:
    q = convergents_from_cf(div_cf)[-1][1]
    if q > 650: break          # beyond this exp(q) is not representable; three terms suffice
    div_cf.append(int(math.ceil(math.exp(q))))
lt = brjuno_partials(div_cf)
print("    divergent-by-construction  [0;1,a1,a2,...] with a_{n+1} = ceil(exp(q_n))")
print("      partial quotients: " + ", ".join(str(x) if x < 10**6 else f"{x:.3e}" for x in div_cf[:5]))
print("      partial sums: " + ", ".join(f"{v:.4f}" for v in lt))
check("the Brjuno sum stays bounded for the golden mean", gt[-1] < 5.0,
      f"{gt[-1]:.6f} after {len(gt)} terms, and the increments are falling geometrically")
incr = [b - a for a, b in zip(lt, lt[1:])]
print("      increments:   " + ", ".join(f"{v:.4f}" for v in incr))
check("every constructed term contributes at least 1", all(v >= 0.99 for v in incr),
      "the construction forces it: a_{n+1} >= exp(q_n) makes log(q_{n+1})/q_n >= 1, "
      "so the sum diverges by construction and not by observation")
print("    Nothing about the map changes between these two rotation numbers.")
print("    The classification of the fixed point does. That is the whole point:")
print("    for a smooth Neimark-Sacker it would not.")
cS = c_of(2*math.pi*(math.sqrt(5)-1)/2)
print(f"    c at the golden internal angle = {cS.real:+.9f}{cS.imag:+.9f}i")

print("\n[7] The cross-references resolve")
for rel in ["ch8-nested-infinities.html", "book8/ch8-9-nested-infinities.html",
            "ch1-seed.html", "cm-choreography.html", "dm3-101-w11.html",
            "ch-mandelbrot-fractals.html", "CardiacHopfReduction.lean",
            "book6/wp109-only-in-two.html", "book6/wp110-not-rough-enough.html"]:
    check(rel, os.path.exists(rel))

print("\n[8] The kernel evidence is on disk")
import glob
reps = sorted(glob.glob("tools/verify-audit/*/geometry__CardiacHopfReduction.axioms.txt"))
print(f"    reports found: {len(reps)}" + (f"   latest: {reps[-1]}" if reps else ""))
STD = "[propext, Classical.choice, Quot.sound]"
if reps:
    lines = [l for l in open(reps[-1]).read().splitlines() if l.startswith("'")]
    for l in lines: print("      " + l)
    check("at least the four original declarations are reported", len(lines) >= 4,
          f"{len(lines)} reported; the count rose to 5 on 2026-09-12 when "
          "radial_deriv_at_cycle was added, so this is a floor and not an equality")
    check("every reported declaration is inside the permitted three",
          all(STD in l or "does not depend on any axioms" in l for l in lines))
    for d in ("radial_reduction", "limit_cycle", "supercritical", "one_mode_no_saturation"):
        check(f"CardiacHopf.{d} is in the report", any(d in l for l in lines))
    if any("radial_deriv_at_cycle" in l for l in lines):
        check("CardiacHopf.radial_deriv_at_cycle is in the report", True,
              "the theorem that carries what `supercritical` is named for")
    else:
        print("      note: radial_deriv_at_cycle not in this report — it was added "
              "2026-09-12; re-audit to pick it up")
else:
    check("an axioms report for CardiacHopfReduction exists", False,
          "run tools/leancheck.sh --audit on it and commit the report")
print("    the file is audited and still untargeted: declaring it @[default_target]")
print("    is what would make this repeat rather than date from one afternoon.")

print("""
[HONESTY] What this script establishes, and what it does not.

  ESTABLISHED. That the main cardioid is exactly the set of c at which the
  fixed point of z^2 + c has a multiplier of modulus one, in closed form, to
  the precision printed. The landmark values. That the fixed point attracts
  inside the curve and does not outside, at the sampled angles. That the bulb
  rooted at internal angle p/q carries an attracting cycle of period q, for
  the eight rationals tested. That the radial reduction asserted in
  CardiacHopfReduction.lean is an identity, that its limit-cycle amplitude is
  sqrt(mu L), and that the derivative there is exactly -2 mu.

  NOT ESTABLISHED, AND QUOTED. Every dynamical statement about irrational
  rotation numbers. Block [6] computes the arithmetic - partial Brjuno sums -
  and nothing else. Whether a Siegel disk exists at a given irrational angle
  is Siegel's theorem, Brjuno's and Yoccoz's; none of it is proved or tested
  here, and no orbit is integrated at an irrational angle, because a finite
  orbit cannot distinguish a linearisable fixed point from one that is not.

  AUDITED BUT NOT TARGETED. CardiacHopfReduction.lean was compiled and audited
  on 2026-09-12 under the v4.32.0 pin: four declarations, all reporting
  [propext, Classical.choice, Quot.sound]. It is still outside every build
  target, so that result dates from the day it was run and a later regression
  would not fail the job.

  WHAT THE AXIOM GATE CANNOT SAY. CardiacHopf.supercritical is clean and proves
  0 < L -> -(1/L) < 0. Its statement mentions no vector field; the reading of
  -1/L as the first Lyapunov coefficient lives in its docstring. A gate that
  enumerates permitted axioms cannot report that a statement is weaker than its
  name, and neither vacuity scan can either, since the conclusion is an ordinary
  inequality and not True. Block [5] here computes the derivative at the limit
  cycle, which is the content the name claims.

  THE BULB PERIODS in block [4] are found by a numerical search with a fixed
  tolerance after a fixed warm-up. A cycle whose attraction is slower than the
  warm-up allows would be missed, and the step length into each bulb was chosen
  to work, not derived.
""")
print(f"{'ALL CHECKS PASSED' if not FAIL else 'FAILED: ' + ', '.join(FAIL)}")
sys.exit(1 if FAIL else 0)
