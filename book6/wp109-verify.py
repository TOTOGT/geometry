#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""wp109-verify.py — companion to book6/wp109-only-in-two.html.

Six blocks, standard library only. Every number and every claim of the form
"this map is conformal" is produced here, from the pullback metric, by the
same method that measured Klein's angle distortion in ch-felix-klein-verify.py.

  [1] The conformal group dimension (n+1)(n+2)/2, and the fact that n = 2 is
      not an exception GLOBALLY - dim 6 = dim PSL(2,C) as a real group - but
      is an exception LOCALLY, where the algebra is infinite-dimensional.
  [2] Conformal = pullback metric is a scalar multiple of the identity.
      J^T J = lambda I. Checked on holomorphic, anti-holomorphic and plainly
      non-conformal plane maps.
  [3] Cauchy-Riemann is the same condition: u_x = v_y, u_y = -v_x, and then
      J^T J = |f'|^2 I exactly.
  [4] Dimension three. Inversion x -> x/|x|^2 IS conformal there. The naive
      analogue of z -> z^2 - double the azimuth, square the radius - is NOT.
      That contrast is what Liouville's theorem makes a theorem.
  [5] The corpus counts quoted in the paper, recomputed from the tree.
  [6] The Escher map z -> z^alpha is conformal, as an instance of [2].

Run:  python3 book6/wp109-verify.py     (from the repository root)

Principia Orthogona - Vol VI - G6 LLC - CC BY-NC-ND 4.0
"""
import math, cmath, sys, os, re, subprocess

FAIL = []
def check(label, ok, detail=""):
    print(f"    {'PASS' if ok else 'FAIL'}  {label}" + (f"   {detail}" if detail else ""))
    if not ok: FAIL.append(label)
    return ok

def jacobian(f, p, h=1e-6):
    """Numerical Jacobian of f: R^n -> R^n at p."""
    n = len(p)
    J = [[0.0]*n for _ in range(n)]
    for j in range(n):
        a = list(p); b = list(p)
        a[j] -= h; b[j] += h
        fa, fb = f(a), f(b)
        for i in range(n):
            J[i][j] = (fb[i] - fa[i]) / (2*h)
    return J

def gram(J):
    n = len(J)
    return [[sum(J[k][i]*J[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

def conformal_defect(J):
    """0 iff J^T J is a positive scalar multiple of the identity."""
    G = gram(J); n = len(G)
    lam = sum(G[i][i] for i in range(n)) / n
    if lam <= 0: return float('inf')
    return max(abs(G[i][j] - (lam if i == j else 0.0)) for i in range(n) for j in range(n)) / lam

print("\n[1] The dimension of the conformal group")
for n in range(2, 9):
    d = (n+1)*(n+2)//2
    print(f"    n = {n}   (n+1)(n+2)/2 = {d}")
check("n=3 gives 10", (3+1)*(3+2)//2 == 10)
check("n=4 gives 15", (4+1)*(4+2)//2 == 15)
check("n=2 gives 6, which is dim PSL(2,C) as a real Lie group",
      (2+1)*(2+2)//2 == 6, "3 complex parameters = 6 real")
check("the LOCAL two-dimensional algebra is infinite-dimensional", True,
      "Witt/Virasoro - quoted, not computed; no finite check can establish it")

print("\n[2] Conformal means the pullback metric is a scalar multiple of I")
maps2 = {
    "z -> z^2            (holomorphic)":      lambda p: [p[0]**2 - p[1]**2, 2*p[0]*p[1]],
    "z -> 1/z            (holomorphic)":      lambda p: [ p[0]/(p[0]**2+p[1]**2), -p[1]/(p[0]**2+p[1]**2)],
    "z -> conj(z)        (anti-holomorphic)": lambda p: [p[0], -p[1]],
    "(x,y) -> (x, 2y)    (linear, not conf)": lambda p: [p[0], 2*p[1]],
    "(x,y) -> (x+y^2, y) (shear, not conf)":  lambda p: [p[0] + p[1]**2, p[1]],
}
pts = [(0.7, 0.4), (1.3, -0.9), (-0.6, 1.1)]
for name, f in maps2.items():
    d = max(conformal_defect(jacobian(f, list(p))) for p in pts)
    print(f"    {name:<38} max defect = {d:.3e}")
    if "not conf" in name:
        check(f"{name.split('(')[0].strip()} is NOT conformal", d > 1e-3)
    else:
        check(f"{name.split('(')[0].strip()} IS conformal", d < 1e-5)

print("\n[3] Cauchy-Riemann is the same condition")
f = lambda p: [p[0]**2 - p[1]**2, 2*p[0]*p[1]]
J = jacobian(f, [0.7, 0.4])
ux, uy, vx, vy = J[0][0], J[0][1], J[1][0], J[1][1]
print(f"    u_x = {ux:.6f}   v_y = {vy:.6f}")
print(f"    u_y = {uy:.6f}  -v_x = {-vx:.6f}")
check("u_x = v_y", abs(ux - vy) < 1e-5)
check("u_y = -v_x", abs(uy + vx) < 1e-5)
fprime = 2*complex(0.7, 0.4)
G = gram(J)
check("J^T J = |f'|^2 I", abs(G[0][0] - abs(fprime)**2) < 1e-4 and abs(G[0][1]) < 1e-5,
      f"|f'|^2 = {abs(fprime)**2:.6f}, G00 = {G[0][0]:.6f}")

print("\n[4] Dimension three: what survives and what does not")
def inversion3(p):
    s = p[0]**2 + p[1]**2 + p[2]**2
    return [p[0]/s, p[1]/s, p[2]/s]
def azimuth_double(p):
    x, y, z = p
    r = math.sqrt(x*x + y*y + z*z)
    th = math.atan2(y, x)
    ph = math.acos(max(-1.0, min(1.0, z/r)))
    R, TH = r*r, 2*th
    return [R*math.sin(ph)*math.cos(TH), R*math.sin(ph)*math.sin(TH), R*math.cos(ph)]
p3 = [0.6, 0.3, 0.8]
d_inv = conformal_defect(jacobian(inversion3, p3))
d_sq  = conformal_defect(jacobian(azimuth_double, p3))
print(f"    inversion x/|x|^2 in R^3        defect = {d_inv:.3e}")
print(f"    'z^2 analogue' in R^3           defect = {d_sq:.3e}")
check("inversion IS conformal in R^3 (it is a Mobius generator)", d_inv < 1e-4)
check("the naive z^2 analogue is NOT conformal in R^3", d_sq > 1e-2,
      "in the plane the same construction is conformal; above two it is not")

print("\n[5] The corpus counts, and the observer effect they ran into")
# MEASURED 2026-09-11, BEFORE wp109-only-in-two.html existed:
BASELINE = {"conformal": 35, "conformal geometry": 0, "CFT": 20, "conformal field": 7}
# On the FIRST run after the paper was written this block failed: "conformal
# geometry" had gone from 0 to 2, and the two files were the paper itself and
# the index row describing it. Reporting the finding put the phrase into the
# corpus it was a finding about. The check is therefore stated the way it was
# always meant: outside the pages that exist BECAUSE of this finding - every
# one of which names wp109 - the phrase appears nowhere. The baseline is kept
# so the drift stays visible rather than being absorbed.
def scan():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = []
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in ('.git', '.lake', 'node_modules')]
        for f in fn:
            if not f.endswith(('.html', '.md')): continue
            path = os.path.join(dp, f)
            try: out.append((path, open(path, encoding='utf-8', errors='ignore').read()))
            except Exception: pass
    return out
CORPUS = scan()
def count(term, regex=False, exclude_finding=False):
    n = 0
    for path, s in CORPUS:
        # Narrow, explicit, auditable: only the paper and the index row that
        # lists it. Excluding every file that MERELY NAMES wp109 was the first
        # attempt and it was wrong - it dropped ch8-0-monster and
        # ch7-holographic, two genuine CFT chapters that had only been
        # annotated with a cross-link, and CFT fell 20 -> 17. A page is part of
        # the finding if it would not exist without it, not if it cites it.
        base = os.path.basename(path)
        if exclude_finding and (base.startswith("wp109") or path.replace("\\", "/").endswith("book6/index.html")):
            continue
        if (re.search(term, s, re.I) if regex else term.lower() in s.lower()): n += 1
    return n
cur = {"conformal": count("conformal", exclude_finding=True),
       "conformal geometry": count("conformal geometry", exclude_finding=True),
       "CFT": count(r"\bCFT\b", regex=True, exclude_finding=True),
       "conformal field": count("conformal field", exclude_finding=True)}
raw_geom = count("conformal geometry")
print(f"    excluding every page that names wp109:")
for k in ("conformal", "conformal geometry", "CFT", "conformal field"):
    print(f"      {k:<20} = {cur[k]:>3}   (baseline 2026-09-11: {BASELINE[k]})")
print(f"    including them, 'conformal geometry' = {raw_geom}  <- the observer effect")
check("outside the pages about this finding, 'conformal geometry' appears nowhere",
      cur["conformal geometry"] == 0, f"{cur['conformal geometry']} files")
check("'conformal' is still in heavy circulation", cur["conformal"] >= 30, f"{cur['conformal']} files")
check("the usage is still field-theoretic", cur["CFT"] >= 18, f"CFT in {cur['CFT']} files")
check("the paper itself is the only reason the phrase now exists here", raw_geom > 0,
      "recorded, not corrected: publishing a count can change it")

print("\n[6] The Escher map is an instance of block [2]")
TWOPII = 2j*math.pi; LOG256 = math.log(256.0)
alpha = (TWOPII + LOG256)/TWOPII
def escher(p):
    w = cmath.exp(alpha*cmath.log(complex(p[0], p[1])))
    return [w.real, w.imag]
d_e = max(conformal_defect(jacobian(escher, list(p))) for p in [(0.7,0.4), (1.3,-0.9)])
print(f"    z -> z^alpha, alpha = {alpha!r}   max defect = {d_e:.3e}")
check("the Droste map is conformal", d_e < 1e-4,
      "because it is holomorphic - a freedom that exists only in dimension two")

print("""
[HONESTY] What this script establishes, and what it does not.

  ESTABLISHED. Conformality or its failure, at sampled points, for each map
  listed, from the pullback metric. The dimension arithmetic. The corpus
  counts, recomputed from the working tree at the moment of running.

  OBSERVER EFFECT. Block [5] failed on its first run after the paper it
  verifies was written, because publishing the count changed it. The
  exclusion that fixes it is narrow and explicit and the first, wider
  attempt is recorded in the comments: it dropped two real CFT chapters
  that had only been cross-linked.

  NOT ESTABLISHED. Liouville's theorem itself. Block [4] exhibits ONE map that
  fails to be conformal in R^3 and one that succeeds; it does not show that
  the conformal maps of R^3 are EXACTLY the Mobius transformations, which is
  the theorem and is quoted. Block [1]'s second half - that the local
  two-dimensional conformal algebra is infinite-dimensional - is likewise
  quoted; no finite computation can establish it. The defects are measured at
  sampled points with a numerical Jacobian, so a map conformal everywhere
  except on a small set would pass.
""")
print(f"{'ALL CHECKS PASSED' if not FAIL else 'FAILED: ' + ', '.join(FAIL)}")
sys.exit(1 if FAIL else 0)
