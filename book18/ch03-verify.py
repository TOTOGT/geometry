#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book18/ch03-verify.py -- every number on book18/ch03-mechanising-it.html. Run first (R24).

    python3 book18/ch03-verify.py [--downloads DIR]

  [1] Deisenroth et al. §5.6 (pp. 159-164), verbatim
  [2] a reverse-mode engine in ~40 lines, run on their Example 5.14, against (5.110)
  [3] forward vs reverse: elementary operations to get a full gradient of f: R^n -> R
  [4] the engine run through the corpus's G3, against ch 2's Jacobian product
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

print("[1] the text")
try:
    D = subprocess.run(["pdftotext", "-layout", str(DL / "MATHEMATICS FOR MACHINE LEARNING.pdf"), "-"], capture_output=True, text=True, timeout=150).stdout.split("\f")
    p159, p162, p163, p164 = (flat(D[i]) for i in (164, 167, 168, 169))
    check("p.159: backpropagation credited to Kelley 1960, Bryson 1961, Dreyfus 1962, Rumelhart et al. 1986", all(x in p159 for x in ("Kelley, 1960; Bryson, 1961; Dreyfus,", "1962; Rumelhart et al., 1986)")))
    check("p.162: reverse mode, which is backpropagation, is significantly cheaper when inputs outnumber outputs", "reverse mode automatic differentia" in p162 and "significantly cheaper than the forward mode" in p162)
    check("p.163: the derivative costs about as much as the function", "of similar complexity as the computation of the function itself" in p163)
    check("p.164: (5.145) is the backpropagation of the gradient", "is the backpropagation of the gradient through the computation graph" in p164)
except Exception as e:
    print("SKIP text", e)

print("[2] a reverse-mode engine")
OPS = [0]
class V:
    def __init__(s, val, parents=()):
        s.val, s.parents, s.grad = val, parents, 0.0
        OPS[0] += 1
    def __add__(s, o): o = o if isinstance(o, V) else V(o); return V(s.val + o.val, ((s, 1.0), (o, 1.0)))
    __radd__ = __add__
    def __mul__(s, o): o = o if isinstance(o, V) else V(o); return V(s.val * o.val, ((s, o.val), (o, s.val)))
    __rmul__ = __mul__
    def __sub__(s, o): return s + (-1.0) * o
def exp(v): e = math.exp(v.val); return V(e, ((v, e),))
def cos(v): return V(math.cos(v.val), ((v, -math.sin(v.val)),))
def sqrt(v): r = math.sqrt(v.val); return V(r, ((v, 0.5 / r),))
def backward(out):
    order, seen, stack = [], set(), [(out, False)]
    while stack:                                   # iterative topological sort
        v, done = stack.pop()
        if done: order.append(v); continue
        if id(v) in seen: continue
        seen.add(id(v)); stack.append((v, True))
        for p, _ in v.parents: stack.append((p, False))
    out.grad = 1.0
    for v in reversed(order):
        for p, local in v.parents:
            p.grad += local * v.grad
            OPS[0] += 1
x0 = 0.5
x = V(x0); a = x * x; b = exp(a); c = a + b; d = sqrt(c); e = cos(c); f = d + e
backward(f)
closed = 2 * x0 * (1 / (2 * math.sqrt(x0**2 + math.exp(x0**2))) - math.sin(x0**2 + math.exp(x0**2))) * (1 + math.exp(x0**2))
F = lambda t: math.sqrt(t*t + math.exp(t*t)) + math.cos(t*t + math.exp(t*t))
fd = (F(x0 + 1e-6) - F(x0 - 1e-6)) / 2e-6
check("reverse mode at x = 0.5 matches the closed form (5.110)", abs(x.grad - closed) < 1e-12, f"{x.grad:.10f}")
check("and a central difference", abs(x.grad - fd) < 1e-7, f"{fd:.10f}")

print("[3] forward vs reverse on f(x) = sum_i sin(x_i) * x_{i+1}, f: R^n -> R")
def f_rev(xs):
    OPS[0] = 0
    vs = [V(t) for t in xs]
    s = V(0.0)
    for i in range(len(vs) - 1):
        s = s + V(math.sin(vs[i].val), ((vs[i], math.cos(vs[i].val)),)) * vs[i + 1]
    backward(s)
    return [v.grad for v in vs], OPS[0]
class Dual:
    def __init__(s, a, b): s.a, s.b = a, b; OPS[0] += 1
    def __add__(s, o): return Dual(s.a + o.a, s.b + o.b)
    def __mul__(s, o): return Dual(s.a * o.a, s.a * o.b + s.b * o.a)
def dsin(u): return Dual(math.sin(u.a), math.cos(u.a) * u.b)
def f_fwd(xs):
    OPS[0] = 0
    g = []
    for j in range(len(xs)):                     # one pass per input direction
        ds = [Dual(t, 1.0 if i == j else 0.0) for i, t in enumerate(xs)]
        s = Dual(0.0, 0.0)
        for i in range(len(ds) - 1):
            s = s + dsin(ds[i]) * ds[i + 1]
        g.append(s.b)
    return g, OPS[0]
rows = []
for n in (10, 100, 1000):
    xs = [0.1 * (i % 7) - 0.3 for i in range(n)]
    gr, cr = f_rev(xs); gf, cf = f_fwd(xs)
    rows.append((n, cf, cr))
    check(f"n = {n}: both modes give the same gradient", max(abs(u - w) for u, w in zip(gr, gf)) < 1e-12)
    print(f"     n = {n:5d}: forward {cf:>9,d} operations, reverse {cr:>7,d}, ratio {cf/cr:7.1f}")
check("forward grows like n^2, reverse like n: the ratio grows with n", rows[0][1]/rows[0][2] < rows[1][1]/rows[1][2] < rows[2][1]/rows[2][2])

print("[4] through the corpus's generator G3 (kappa = 1.5, r0 = 1)")
kap, r0 = 1.5, 1.0
def G3(r, th, z):
    z = r * r * th                                   # C3
    z = z + 1.0                                      # K3
    r = r if r.val <= kap else V(2 * kap) - r       # F3, branch taken at the value
    r = (r - r0) * math.exp(-1) + r0                 # U3
    return r, th, z
for s in ((1.0, 1.0, 0.0), (2.0, 0.5, 0.3)):
    r, th, z = V(s[0]), V(s[1]), V(s[2])
    R, T, Z = G3(r, th, z)
    loss = R * R + T * T + Z * Z
    backward(loss)
    grad = (r.grad, th.grad, z.grad)
    def Lnum(v):
        rr, tt, zz = v
        zz = rr*rr*tt + 1
        rr = rr if rr <= kap else 2*kap - rr
        rr = (rr - r0) * math.exp(-1) + r0
        return rr*rr + tt*tt + zz*zz
    num = []
    for j in range(3):
        vp = list(s); vm = list(s); vp[j] += 1e-6; vm[j] -= 1e-6
        num.append((Lnum(vp) - Lnum(vm)) / 2e-6)
    check(f"at {s}: backprop through U3 F3 K3 C3 = numerical gradient of |G3|^2", max(abs(a - b) for a, b in zip(grad, num)) < 1e-5, f"{tuple(round(g, 4) for g in grad)}")
    check(f"at {s}: the gradient in z is 0 -- C3 overwrites z, so the input z cannot matter", abs(grad[2]) < 1e-12)

print("""
[HONESTY]
[1] matches sentences in a text layer. [2]-[4] use an engine written for this page
(forty lines, standard library); it is the algorithm of Deisenroth's (5.143)-(5.145),
not a production system, and its operation counts count graph nodes and edge
updates, not machine instructions. The function in [3] was chosen to have one scalar
output and n inputs, the case where the text says reverse mode wins; with n outputs
and one input the comparison reverses. [4] differentiates the Python re-implementation
of the Lean definitions used in ch 2, away from the fold at r = kappa.
""")
print(f"{len(FAIL)} FAIL")
sys.exit(1 if FAIL else 0)
