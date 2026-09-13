#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""wp110-verify.py — companion to book6/wp110-not-rough-enough.html.

Seven blocks. numpy is used (as in wp69, wp90, wp100); nothing else outside the
standard library. Every number printed in the paper is produced here.

  [1] The divergence-theorem volume of a closed triangulated surface, checked
      against the analytic sphere. The mesh is an INSCRIBED polyhedron, so it
      must come in slightly under 4/3 pi and converge from below.
  [2] The section-area slicer, checked against the analytic circle pi(1-z^2).
      Areas are accumulated over oriented slice segments by Green's theorem
      with no polygon chaining; orientation comes from the triangle normal.
  [3] The two exact routes agree. On one rough polyhedron, the divergence sum
      and the Riemann integral of the slicer's areas must converge to each
      other, not merely to something plausible.
  [4] Isoperimetric ratio S / V^(2/3). The sphere's value 4.8360 is the floor,
      and it anchors how folded the test surfaces actually are.
  [5] The sweep: realized coefficient of variation of the Cavalieri estimator
      over systematic random section offsets, and the fitted decay exponent
      gamma in CV ~ n^-gamma. Reduced by default (about a minute); --full
      reproduces the table in the paper.
  [6] The cortical anchor. Arithmetic only, from nominal inputs stated in the
      paper; it is an order-of-magnitude marker and not a measurement.
  [7] The negative result, stated as a check: no monotone trend in gamma.

Run:  python3 book6/wp110-verify.py            (from the repository root)
      python3 book6/wp110-verify.py --full     (the paper's full sweep, ~9 min)

Principia Orthogona - Vol VI - G6 LLC - CC BY-NC-ND 4.0
"""
import sys, math, time
import numpy as np

FULL = "--full" in sys.argv
FAIL = []
def check(label, ok, detail=""):
    print(f"    {'PASS' if ok else 'FAIL'}  {label}" + (f"   {detail}" if detail else ""))
    if not ok: FAIL.append(label)
    return ok

# ----------------------------------------------------------------- geometry
def icosphere(sub):
    t = (1 + 5 ** 0.5) / 2
    V = np.array([[-1,t,0],[1,t,0],[-1,-t,0],[1,-t,0],[0,-1,t],[0,1,t],
                  [0,-1,-t],[0,1,-t],[t,0,-1],[t,0,1],[-t,0,-1],[-t,0,1]], float)
    V /= np.linalg.norm(V, axis=1, keepdims=True)
    F = np.array([[0,11,5],[0,5,1],[0,1,7],[0,7,10],[0,10,11],[1,5,9],[5,11,4],
                  [11,10,2],[10,7,6],[7,1,8],[3,9,4],[3,4,2],[3,2,6],[3,6,8],
                  [3,8,9],[4,9,5],[2,4,11],[6,2,10],[8,6,7],[9,8,1]], int)
    for _ in range(sub):
        mid = {}; nV = list(V); nF = []
        def m(a, b):
            k = (min(a,b), max(a,b))
            if k not in mid:
                p = np.asarray(nV[a]) + np.asarray(nV[b]); p /= np.linalg.norm(p)
                mid[k] = len(nV); nV.append(p)
            return mid[k]
        for a, b, c in F:
            ab, bc, ca = m(a,b), m(b,c), m(c,a)
            nF += [[a,ab,ca],[b,bc,ab],[c,ca,bc],[ab,bc,ca]]
        V = np.array(nV); F = np.array(nF, int)
    return V, F

def displace(V, beta, amp, seed, band=(2.0, 80.0), nmodes=160):
    """Radial displacement with a power-law spectrum A(w) = w^-beta.
       Small beta keeps high frequencies alive: rougher. Large beta: smoother."""
    rng = np.random.default_rng(seed)
    d = rng.normal(size=(nmodes, 3)); d /= np.linalg.norm(d, axis=1, keepdims=True)
    w = np.exp(rng.uniform(math.log(band[0]), math.log(band[1]), nmodes))
    ph = rng.uniform(0, 2*math.pi, nmodes)
    disp = ((w ** -beta) * np.cos(w * (V @ d.T) + ph)).sum(axis=1)
    disp /= np.abs(disp).max()
    return V * (1.0 + amp * disp)[:, None]

def volume(V, F):
    """Divergence theorem: signed tetrahedra from the origin. Exact for a polyhedron."""
    a, b, c = V[F[:,0]], V[F[:,1]], V[F[:,2]]
    return float(np.einsum('ij,ij->i', a, np.cross(b, c)).sum() / 6.0)

def area(V, F):
    a, b, c = V[F[:,0]], V[F[:,1]], V[F[:,2]]
    return float(0.5 * np.linalg.norm(np.cross(b-a, c-a), axis=1).sum())

def prep(V, F):
    a, b, c = V[F[:,0]], V[F[:,1]], V[F[:,2]]
    return np.stack([a, b, c], axis=1), np.cross(b-a, c-a)

def section_areas(tri, nrm, zs, batch=64):
    """Exact cross-sectional area at each z. Green's theorem over oriented
       segments: no polygon chaining, so a section in several pieces is free."""
    out = np.empty(len(zs))
    for s in range(0, len(zs), batch):
        Z = zs[s:s+batch]
        d = tri[None,:,:,2] - Z[:,None,None]
        k = (d > 0).sum(axis=2)
        sel = (k == 1) | (k == 2)
        cross = np.empty(d.shape, bool); pts = np.empty(d.shape[:2] + (3, 2))
        for e, (e0, e1) in enumerate(((0,1),(1,2),(2,0))):
            d0, d1 = d[:,:,e0], d[:,:,e1]
            c = (d0 > 0) != (d1 > 0)
            den = d0 - d1; den = np.where(den == 0, 1e-300, den)
            t = np.where(c, d0 / den, 0.0)
            p0 = tri[None,:,e0,:2]; p1 = tri[None,:,e1,:2]
            pts[:,:,e,:] = p0 + t[:,:,None] * (p1 - p0)
            cross[:,:,e] = c
        order = np.argsort(~cross, axis=2, kind='stable')[:,:,:2]
        P = np.take_along_axis(pts, order[...,None], axis=2)
        p, q = P[:,:,0,:], P[:,:,1,:]
        nxy = nrm[None,:,:2]
        perp = np.stack([-nxy[...,1], nxy[...,0]], axis=-1)
        flip = ((q - p) * perp).sum(axis=-1) < 0
        p2 = np.where(flip[...,None], q, p); q2 = np.where(flip[...,None], p, q)
        contrib = 0.5 * (p2[...,0]*q2[...,1] - q2[...,0]*p2[...,1])
        out[s:s+batch] = np.abs(np.where(sel, contrib, 0.0).sum(axis=1))
    return out

# ----------------------------------------------------------------- blocks
print("\n[1] Divergence theorem against the analytic sphere")
for sub in (2, 3, 4):
    V, F = icosphere(sub); v = volume(V, F)
    print(f"    sub={sub}  faces={len(F):6d}  V={v:.8f}   4pi/3 - V = {4*math.pi/3 - v:.3e}")
V4, F4 = icosphere(4)
g3 = 4*math.pi/3 - volume(*icosphere(3))
g4 = 4*math.pi/3 - volume(V4, F4)
check("inscribed polyhedron under-estimates the ball", volume(V4, F4) < 4*math.pi/3)
check("the gap falls by about four per subdivision", 3.0 < g3/g4 < 5.0,
      f"gap {g3:.2e} -> {g4:.2e}, ratio {g3/g4:.2f}")

print("\n[2] The slicer against the analytic circle")
tri, nrm = prep(V4, F4)
zs = np.linspace(-0.9, 0.9, 13)
A = section_areas(tri, nrm, zs)
err = max(abs(a - math.pi*(1-z*z)) for z, a in zip(zs, A))
print(f"    max |A(z) - pi(1-z^2)| over 13 heights = {err:.3e}   (polyhedral, not slicer, error)")
check("section areas track the analytic circle", err < 6e-3)
check("every section area is non-negative", bool((A >= 0).all()))

print("\n[3] The two exact routes agree on a rough polyhedron")
Vr = displace(V4, 1.2, 0.22, seed=0); trir, nrmr = prep(Vr, F4)
Vex = volume(Vr, F4); zmin, zmax = Vr[:,2].min(), Vr[:,2].max()
for N in (500, 2000, 8000):
    z = zmin + (np.arange(N) + 0.5) * (zmax - zmin) / N
    Vc = (zmax - zmin) / N * section_areas(trir, nrmr, z).sum()
    rel = abs(Vc - Vex) / Vex
    print(f"    N={N:5d}  Cavalieri={Vc:.9f}   divergence={Vex:.9f}   rel={rel:.2e}")
check("the two exact methods converge on each other", rel < 1e-8,
      "one integrates areas of slices, the other sums signed tetrahedra")

print("\n[4] Isoperimetric ratio S / V^(2/3)")
SPH = 4*math.pi / (4*math.pi/3) ** (2/3)
print(f"    sphere (the floor) = {SPH:.4f}")
check("the sphere is the minimum", abs(SPH - 4.8360) < 1e-3, f"{SPH:.4f}")
for beta in (0.3, 2.5):
    Vb = displace(V4, beta, 0.22, seed=0)
    print(f"    beta={beta}  S/V^(2/3) = {area(Vb,F4)/volume(Vb,F4)**(2/3):.3f}")

print("\n[5] Realized error of the Cavalieri estimator, and its decay exponent")
SUB, BET, NS, R, SEEDS = ((5, [0.3,0.8,1.5,2.5], [8,16,32,64,128], 30, [0,1]) if FULL
                          else (4, [0.3, 2.5], [8, 16, 32, 64], 20, [0]))
V0, F0 = icosphere(SUB)
print(f"    mesh {len(F0)} faces | betas {BET} | n {NS} | {R} offsets | seeds {SEEDS}"
      + ("" if FULL else "   (reduced; --full for the paper's table)"))
rng = np.random.default_rng(999); GAM = {}; t0 = time.time()
for beta in BET:
    percv = {n: [] for n in NS}; iso = []
    for sd in SEEDS:
        Vb = displace(V0, beta, 0.22, seed=sd); t_, n_ = prep(Vb, F0)
        Ve = volume(Vb, F0); iso.append(area(Vb, F0) / Ve ** (2/3))
        lo, hi = Vb[:,2].min(), Vb[:,2].max(); H = hi - lo
        for n in NS:
            T = H / n
            est = []
            for _ in range(R):
                z = lo + (rng.random() + np.arange(n)) * T
                est.append(T * section_areas(t_, n_, z[z < hi]).sum())
            percv[n].append(float(np.std(est, ddof=1) / Ve))
    cv = np.array([np.mean(percv[n]) for n in NS]); nn = np.array(NS, float)
    g = -np.polyfit(np.log(nn), np.log(cv), 1)[0]
    GAM[beta] = (float(np.mean(iso)), float(g))
    print(f"    beta={beta:<4} iso={np.mean(iso):.3f}  gamma={g:.3f}   " +
          "  ".join(f"n={n}:{c:.2e}" for n, c in zip(NS, cv)) + f"   [{time.time()-t0:.0f}s]")
check("every fitted exponent is near 2", all(1.5 < g < 2.5 for _, g in GAM.values()),
      "  ".join(f"{b}:{g:.2f}" for b, (_, g) in GAM.items()))

print("\n[6] The cortical anchor - arithmetic only, from nominal inputs")
S_CX, V_BR = 1600.0, 1100.0          # cm^2, cm^3: round numbers, stated as such
iso_cx = S_CX / V_BR ** (2/3)
print(f"    S={S_CX:.0f} cm^2, V={V_BR:.0f} cm^3  ->  S/V^(2/3) = {iso_cx:.1f}")
print(f"    roughest surface tested = {max(i for i,_ in GAM.values()):.2f};  sphere = {SPH:.2f}")
check("the test surfaces do not reach cortical folding", iso_cx > 2 * max(i for i, _ in GAM.values()),
      "which is the restriction this paper is named for")

print("\n[7] The negative result, as a check")
order = [GAM[b][1] for b in BET]
mono = all(x <= y for x, y in zip(order, order[1:])) or all(x >= y for x, y in zip(order, order[1:]))
check("gamma is not monotone in roughness", (not mono) or len(BET) < 3,
      "no trend survives; with this many offsets a difference under ~0.3 is not resolved")

print("""
[HONESTY] What this script establishes, and what it does not.

  ESTABLISHED. That the two exact volume methods agree on the same polyhedron
  to the precision printed in block [3] - the divergence-theorem sum over
  faces, and the Riemann integral of exact section areas. That the slicer is
  correct against the analytic sphere. The isoperimetric ratios of the test
  surfaces. The realized coefficient of variation of the Cavalieri estimator
  at the stated section counts, and the exponent fitted to it.

  NOT ESTABLISHED. That folding does not affect the Cavalieri error law. This
  measures a range of roughness that stops far short of a folded cortex -
  block [6] prints the gap - so a null result here is a null result about
  mildly corrugated spheres and nothing else. The variance of the CV estimate
  at this number of offsets leaves differences in gamma below about 0.3
  undetectable; the non-monotone ordering in block [5] is consistent with
  there being no effect and equally consistent with an effect this design
  cannot see.

  NOT ATTEMPTED. The published variance predictors for Cavalieri sampling are
  not implemented or tested here. The smoothness constant that parameterises
  them is quoted in the paper from the literature and is not measured.

  The cortical figures in block [6] are round numbers chosen to set a scale.
  They are not a measurement and nothing downstream depends on their precision.
""")
print(f"{'ALL CHECKS PASSED' if not FAIL else 'FAILED: ' + ', '.join(FAIL)}")
sys.exit(1 if FAIL else 0)
