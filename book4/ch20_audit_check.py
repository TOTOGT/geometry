#!/usr/bin/env python3
"""Audit evidence for book4/ch20-defect-lattice.html Result 20.2 (2026-11-15). Read-only.

Model (the page's): N independent defects, each with a Burgers vector drawn uniformly from the
lattice translation set (square: 4 vectors, triangular: 6). The coarse-grained torsion in a cell
is their sum S_N. The m-fold anisotropy of S_N is measured here, EXACTLY (no sampling), as
  A_m(N) = |E[S^m]| / E[|S|^m]            (m = 4 square, m = 6 triangular),
the amplitude of the m-th angular harmonic of the sum weighted by |S|^m. Two further exact
definitions are reported: B_m(N) = |E[exp(i m arg S)]| (angular distribution, S != 0) and
the fixed-radius density anisotropy of the characteristic function phi^N is analysed by hand in the page.
Exact: S_N is a lattice random walk; its law is obtained by convolution on Z[i] (square) / Z[w] (hex).
"""
import numpy as np, math, sys
def walk(steps, N):
    # law of S_N by repeated convolution on a dict of integer coordinates
    law = {(0, 0): 1.0}
    for _ in range(N):
        new = {}
        for (x, y), p in law.items():
            for dx, dy in steps:
                k = (x + dx, y + dy); new[k] = new.get(k, 0.0) + p / len(steps)
        law = new
    return law
SQ = [(1, 0), (-1, 0), (0, 1), (0, -1)]
# hexagonal: coordinates in basis a1 = 1, a2 = w = e^{i pi/3}; steps are the six unit vectors
HX = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
def embed_sq(k): return complex(k[0], k[1])
def embed_hx(k): return k[0] + k[1] * complex(0.5, math.sqrt(3) / 2)
def measures(law, emb, m):
    num = 0j; den = 0.0; ang = 0j; w = 0.0
    for k, p in law.items():
        z = emb(k)
        if abs(z) < 1e-12: continue
        num += p * z ** m; den += p * abs(z) ** m
        ang += p * (z / abs(z)) ** m; w += p
    return abs(num) / den, abs(ang) / w
def slope(Ns, ys):
    return np.polyfit(np.log(Ns), np.log(ys), 1)[0]
res = {}
for name, steps, emb, m in (("square", SQ, embed_sq, 4), ("triangular", HX, embed_hx, 6)):
    Ns = [1, 2, 4, 8, 16, 24, 32, 48, 64, 96, 128]
    A = []; B = []
    law = {(0, 0): 1.0}; cur = 0
    for N in Ns:
        law = walk(steps, N - cur) if cur == 0 else None
        cur = N
    # recompute incrementally for speed
    law = {(0, 0): 1.0}; done = 0; A = []; B = []
    for N in Ns:
        for _ in range(N - done):
            new = {}
            for (x, y), p in law.items():
                for dx, dy in steps:
                    k = (x + dx, y + dy); new[k] = new.get(k, 0.0) + p / len(steps)
            law = new
        done = N
        a, b = measures(law, emb, m); A.append(a); B.append(b)
    tail = [i for i, N in enumerate(Ns) if N >= 16]
    sa = slope([Ns[i] for i in tail], [A[i] for i in tail]); sb = slope([Ns[i] for i in tail], [B[i] for i in tail])
    print("%-10s m=%d  A_m(1)=%.3f  A_m(N=16,32,64,128)=%s" % (name, m, A[0], ", ".join("%.3e" % A[Ns.index(n)] for n in (16, 32, 64, 128))))
    print("           tail exponent (N>=16): A_m -> %.3f   B_m (angular distribution) -> %.3f" % (sa, sb))
    res[name] = (sa, sb)
ok_sq = abs(res["square"][0] + 1) < 0.1
ok_hx = abs(res["triangular"][0] + 2) < 0.15
print("PASS square: A_4 ~ N^-1 (exponent %.3f), as the page states" % res["square"][0] if ok_sq else "FAIL square exponent %.3f" % res["square"][0])
print("PASS triangular: A_6 ~ N^-2 (exponent %.3f), NOT N^-1 as the page's table states" % res["triangular"][0] if ok_hx else "FAIL triangular exponent %.3f" % res["triangular"][0])
# hand argument check: hexagonal phi has no quartic anisotropy
th = np.linspace(0, math.pi, 7)
quartic = [sum(math.cos(4 * (t - j * math.pi / 3)) for j in range(3)) for t in th]
print("PASS hex quartic term is isotropic: sum_j cos(4(theta - j*60deg)) = %s" % np.round(quartic, 12) if max(abs(np.array(quartic))) < 1e-12 else "FAIL hex quartic")
sex = [sum(math.cos(6 * (t - j * math.pi / 3)) for j in range(3)) for t in th]
print("     hex sextic term is anisotropic: sum_j cos(6(theta - j*60deg)) = %s" % np.round(sex, 3))
sys.exit(0 if (ok_sq and ok_hx) else 1)
