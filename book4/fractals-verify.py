#!/usr/bin/env python3
"""Verifier for book4/fractals.html (the 4/3 chapter).
Checks, numerically, what the chapter states:
  1. generator pieces have length r = 2^(-3/2), N = 4  ->  d = log N / log(1/r) = 4/3
  2. level-n length = (N r)^n = sqrt(2)^n
  3. no proper self-crossings through level 5 (finite check only, NOT a proof for the limit)
  4. box-counting slope (noisy; calibrated against the Koch curve, whose d = log4/log3 = 1.2619)
Run:  python3 fractals-verify.py
"""
import numpy as np, math

def refine(pts, gen):
    z = pts[:, 0] + 1j * pts[:, 1]
    g = gen[:, 0] + 1j * gen[:, 1]
    out = []
    for a, b in zip(z[:-1], z[1:]):
        out.extend(a + g[:-1] * (b - a))
    out.append(z[-1])
    out = np.array(out)
    return np.c_[out.real, out.imag]

def build(gen, n):
    pts = np.array([[0.0, 0.0], [1.0, 0.0]])
    for _ in range(n):
        pts = refine(pts, gen)
    return pts

TENT = np.array([[0, 0], [.25, .25], [.5, .5], [.75, .25], [1, 0]], float)
KOCH = np.array([[0, 0], [1/3, 0], [.5, math.sqrt(3)/6], [2/3, 0], [1, 0]], float)

def seglens(p): return np.hypot(*np.diff(p, axis=0).T)

def crossings(p):
    a, b = p[:-1], p[1:]
    n = len(a); bad = 0
    def orient(u, v, w): return (v[..., 0]-u[..., 0])*(w[..., 1]-u[..., 1]) - (v[..., 1]-u[..., 1])*(w[..., 0]-u[..., 0])
    for i in range(n):
        j = np.arange(i + 2, n)
        if len(j) == 0: continue
        o1 = orient(a[i], b[i], a[j]); o2 = orient(a[i], b[i], b[j])
        o3 = orient(a[j], b[j], a[i]); o4 = orient(a[j], b[j], b[i])
        e = 1e-12
        bad += int(np.sum((o1*o2 < -e*e) & (o3*o4 < -e*e)))
    return bad

def boxslope(p, eps_list, per=6):
    t = np.linspace(0, 1, per, endpoint=False)
    a, b = p[:-1], p[1:]
    pts = (a[:, None, :] * (1 - t)[None, :, None] + b[:, None, :] * t[None, :, None]).reshape(-1, 2)
    pts = np.vstack([pts, p[-1]])
    N = []
    for e in eps_list:
        N.append(len(set(map(tuple, np.floor(pts / e).astype(np.int64)))))
    s = np.polyfit(np.log(1 / np.array(eps_list)), np.log(N), 1)[0]
    return N, s

r = 2 ** -1.5; N = 4
print("1. similarity dimension")
print("   piece lengths of generator:", np.round(seglens(TENT), 6), " 2^-1.5 =", round(r, 6))
print("   d = log4/log(1/r) =", math.log(N) / math.log(1 / r), " (4/3 =", 4/3, ")")
print("2. length per level (exact sqrt2^n vs measured)")
for n in range(0, 7):
    L = seglens(build(TENT, n)).sum()
    print(f"   n={n}: measured {L:.6f}  sqrt2^n {math.sqrt(2)**n:.6f}")
print("3. proper self-crossings (finite check)")
for n in range(1, 6):
    print(f"   level {n}: {crossings(build(TENT, n))}")
print("4. box counting (noisy; compare to calibration)")
pk = build(KOCH, 7)
Nk, sk = boxslope(pk, [3.0**-k for k in range(2, 6)])
print(f"   Koch  (true {math.log(4)/math.log(3):.4f}): slope {sk:.4f}  counts {Nk}")
pt = build(TENT, 8)
Nt, st = boxslope(pt, [r**k for k in range(3, 8)])
print(f"   Tent  (true {4/3:.4f}): slope {st:.4f}  counts {Nt}  (boxes of side r^k, k=3..7)")
print("5. similarity dimensions of objects between dimension 1 and 2 (exact: log N / log(1/r))")
zoo=[("Koch curve",4,3),("2-D Cantor dust (4 squares, ratio 1/3)",4,3),("Minkowski sausage curve (8 pieces, ratio 1/4)",8,4),("Sierpinski triangle",3,2),("Sierpinski carpet",8,3)]
for name,Nn,inv in zoo:
    print(f"   {name}: N={Nn}, 1/r={inv}  d={math.log(Nn)/math.log(inv):.4f}")
print("   tent family r = 1/(4 cos(theta)), N=4, d = log4/log(4cos(theta)); upper bound where pieces overlap:")
for th in (0,15,30,45,55):
    print(f"   theta={th:2d} deg: 4cos={4*math.cos(math.radians(th)):.4f}  d={math.log(4)/math.log(4*math.cos(math.radians(th))):.4f}")
print("Interpretation: (1),(2) are exact algebra; (3) holds through level 5 only; (4) is a sanity check, not a measurement of the limit.")
