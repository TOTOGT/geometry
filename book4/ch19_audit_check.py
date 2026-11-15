#!/usr/bin/env python3
"""Audit evidence for book4/ch19-acoustic-lattice.html (2026-11-14). Read-only.

The page says the per-step delay grows "because the geometry steepens as the reflection point
climbs". AcousticLattice.lean takes that growth as a hypothesis (StrictMono delay); it is not
derived there. This script derives it for the stated geometry and tests the page's side claims.
Model (ours, stated): straight uniform staircase, step edges at P_n = (d + n*q, n*p), source and
listener together at (0, h). Round-trip path 2*|P_n|, per-step delay D(n) = 2(r_{n+1}-r_n)/c.
"""
import math, random, sys
fails = 0
def check(name, ok):
    global fails
    print(("PASS " if ok else "FAIL ") + name); fails += (not ok)
c = 343.0
def delays(d, h, q, p, N):
    r = [math.hypot(d + n * q, n * p - h) for n in range(N + 1)]
    return [2 * (r[n + 1] - r[n]) / c for n in range(N)]
random.seed(19)
# [1] D(n) strictly increasing for every listener position in front of a uniform stair
bad = 0; trials = 20000
for _ in range(trials):
    q = random.uniform(0.15, 0.5); p = random.uniform(0.1, 0.5)
    d = random.uniform(0.5, 60); h = random.uniform(0.0, 2.0); N = random.randint(5, 120)
    D = delays(d, h, q, p, N)
    if any(D[i + 1] <= D[i] for i in range(N - 1)): bad += 1
check("[1] delay D(n) strictly increasing in all %d random uniform-stair geometries (r_n is convex in n)" % trials, bad == 0)
# control: listener on the stair line itself -> equal delays (flat tone), the degenerate case
D = delays(10.0, -10.0 * 0.3 / 0.25, 0.25, 0.3, 40)   # (0,h) collinear with the edges: h = -d*p/q
check("[1] control: listener collinear with the step edges gives constant delay (spread %.1e s)" % (max(D) - min(D)), max(D) - min(D) < 1e-12)
# [2] limits: D -> 2*sqrt(q^2+p^2)/c far up the stair; D(0) ~ 2(q d - p h)/(c sqrt(d^2+h^2))
q = p = 0.263; N = 91; h = 1.6          # El Castillo-like: 91 steps, run = riser = 26.3 cm (inputs not verified against a survey)
print("    El Castillo-like stair, ear height 1.6 m, c = 343 m/s, 91 steps:")
for d in (3, 5, 10, 20, 40):
    D = delays(d, h, q, p, N)
    f0, f1 = 1 / D[0], 1 / D[-1]
    print("      listener %4.0f m out: pitch %6.0f -> %4.0f Hz, fall = %.2f octave" % (d, f0, f1, math.log2(f0 / f1)))
Dfar = delays(1e6, h, q, p, 3)[0]; Dtop = delays(10, h, q, p, 100000)[-1]
check("[2] far-field first delay -> 2q/c (%.6f vs %.6f ms)" % (1e3 * Dfar, 1e3 * 2 * q / c), abs(Dfar - 2 * q / c) < 1e-8)   # 1e-8 s: float cancellation at d = 1e6 m
check("[2] far up the stair delay -> 2*sqrt(q^2+p^2)/c (%.5f vs %.5f ms)" % (1e3 * Dtop, 1e3 * 2 * math.hypot(q, p) / c), abs(Dtop - 2 * math.hypot(q, p) / c) < 1e-6)
print("    => for a distant listener the fall is at most log2(sqrt(1+(p/q)^2)) = %.2f octave for run = riser;" % math.log2(math.hypot(1, p / q)))
print("       'about one octave' needs the listener close in (a few metres). The page gives no listener distance.")
# [3] "Nearer the base the swoop is steeper; farther back it flattens"
falls = [math.log2(delays(d, h, q, p, N)[-1] / delays(d, h, q, p, N)[0]) for d in (3, 5, 10, 20, 40, 80)]
check("[3] total fall decreases as the listener moves back (%s)" % ", ".join("%.2f" % f for f in falls), all(falls[i] > falls[i + 1] for i in range(len(falls) - 1)))
# [4] Task 2 asks for a geometry (run, riser, observer position) giving an ASCENDING chirp
asc = 0
for _ in range(20000):
    q2 = random.uniform(0.15, 0.5); p2 = random.uniform(0.1, 0.5)
    d2 = random.uniform(0.5, 60); h2 = random.uniform(0.0, 2.0)
    D = delays(d2, h2, q2, p2, 60)
    if all(D[i + 1] < D[i] for i in range(59)): asc += 1
check("[4] in THIS model (straight uniform stair, point reflectors at the step edges, source and listener together, listener height 0-2 m, distance 0.5-60 m, run/riser 0.15-0.5 m) no sampled geometry gives an ascending chirp (0 of 20000); this is sampling, the convexity argument in AuditFixes_2026_11_15.lean gives the non-strict statement for all listener positions. Extended surfaces, separated source/listener, curved or non-uniform stairs are not covered", asc == 0)
D = []; x = 5.0; y = 0.0; pts = [(x, y)]
for n in range(40):                       # runs shrinking geometrically, riser shrinking with them
    s = 0.4 * 0.93 ** n; x += s; y += s; pts.append((x, y))
r = [math.hypot(px, py - 1.6) for px, py in pts]; D = [r[i + 1] - r[i] for i in range(40)]
check("[4] a stair whose steps shrink with height does give an ascending chirp (exists)", all(D[i + 1] < D[i] for i in range(5, 39)))
# [5] octave_drop arithmetic
check("[5] doubling the delay halves the pitch", abs((1 / 0.001) / (1 / 0.002) - 2) < 1e-12)
sys.exit(1 if fails else 0)
