#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book24/reye-derive.py -- derives, from the compressible Euler equations alone, the numbers the MRRS papers use,
and compares them with the formula r_eye(d,l) of arXiv:1912.11009v2 eq. (1.4). Floating point; needs sympy, numpy.

Radial isentropic Euler in d dimensions, with sound speed c, alpha = (gamma-1)/2:
    c_t + u c_r + alpha c (u_r + (d-1) u / r) = 0,      u_t + u u_r + c c_r / alpha = 0.
Self-similar ansatz with speed r:  u = tau^(1/r - 1) U(xi), c = tau^(1/r - 1) C(xi), xi = x / tau^(1/r), tau = T - t.
With P = U/xi, Q = C/xi and y = ln xi the ODE is autonomous:
    (1+rP)(P+P_y) + (r/alpha) Q (Q+Q_y) + (r-1) P = 0
    r alpha Q (P+P_y) + (1+rP)(Q+Q_y) + (r-1) Q + r alpha (d-1) Q P = 0.
It is singular where Delta = (1+rP)^2 - r^2 Q^2 = 0 (the sonic locus). Desingularised (multiply by Delta), the sonic
points are zeros of (N1, N2); k = ratio of the two eigenvalues of the Jacobian there.

CHECKS (asserted):  (1) for gamma = 5/3, d = 3 the ratio is 2, 3, 4 at r = 11-3 sqrt 11, 6-2 sqrt 6, (43-5 sqrt 43)/9
(the closed forms quoted in arXiv:2301.10101); (2) for l < d the smaller eigenvalue at one sonic point goes to 0
linearly as r -> r_*(d,l) from below (checked for (d,l) = (3,0.5), (3,1), (3,2), (2,1), (4,2)).
NOT CHECKED: the branch l > d. The sonic-point root finding is noisy there and the eigenvalue behaviour near r_+ was
not resolved; nothing is claimed about r_+ from this script. Nothing here proves existence of smooth profiles.
"""
import math, sympy as sp, numpy as np
P, Q, r, al, d = sp.symbols('P Q r alpha d', real=True); PY, QY = sp.symbols('PY QY')
e1 = (1 + r*P)*(P + PY) + (r/al)*Q*(Q + QY) + (r - 1)*P
e2 = r*al*Q*(P + PY) + (1 + r*P)*(Q + QY) + (r - 1)*Q + r*al*(d - 1)*Q*P
sol = sp.solve([e1, e2], [PY, QY], dict=True)[0]
Delta = sp.simplify((1 + r*P)**2 - r**2*Q**2)
N1 = sp.simplify(sol[PY]*Delta); N2 = sp.simplify(sol[QY]*Delta)
Jm = sp.Matrix([N1, N2]).jacobian([P, Q])
fJ = sp.lambdify((P, Q, r, al, d), Jm)
poly = sp.Poly(sp.expand(sp.simplify(N1.subs(Q, (1 + r*P)/r))), P)
coeffs = [sp.lambdify((r, al, d), c) for c in poly.all_coeffs()]

def points(rv, g, dv=3):
    a = (g - 1)/2; out = []
    for Pv in np.roots([c(rv, a, dv) for c in coeffs]):
        if abs(Pv.imag) > 1e-10: continue
        Pv = Pv.real; Qv = (1 + rv*Pv)/rv
        if Qv > 0: out.append((Pv, Qv))
    return sorted(out)

def eigs(rv, g, w, dv=3):
    Pv, Qv = points(rv, g, dv)[w]
    return np.linalg.eigvals(np.array(fJ(Pv, Qv, rv, (g - 1)/2, dv), dtype=float)).real

def r_eye(dv, l):
    return (dv + l)/(l + math.sqrt(dv)) if l < dv else 1 + (dv - 1)/(1 + math.sqrt(l))**2

FAIL = []
def check(name, ok, extra=""):
    print(("PASS " if ok else "FAIL ") + name + (f"  [{extra}]" if extra else ""))
    if not ok: FAIL.append(name)

print("[1] gamma = 5/3, d = 3: eigenvalue ratio at the sonic points at the review's r_j")
for j, rv in ((2, 11 - 3*math.sqrt(11)), (3, 6 - 2*math.sqrt(6)), (4, (43 - 5*math.sqrt(43))/9)):
    ratios = []
    for w in range(len(points(rv, 5/3))):
        e = eigs(rv, 5/3, w)
        if min(e) > 0: ratios.append(max(e)/min(e))
    check(f"ratio = {j} at r_{j} = {rv:.6f} (two sonic points with both eigenvalues > 0)", len(ratios) >= 1 and all(abs(x - j) < 1e-6 for x in ratios), f"ratios {[round(x, 9) for x in ratios]}")

print("[2] l < d: the smaller eigenvalue vanishes at r_* (linear in r_* - r)")
for dv, l in ((3, 0.5), (3, 1.0), (3, 2.0), (2, 1.0), (4, 2.0)):
    g = 1 + 2/l; rt = r_eye(dv, l); best = []
    for eps in (1e-3, 1e-4, 1e-5):
        pts = points(rt - eps, g, dv); m = min(np.abs(eigs(rt - eps, g, w, dv)).min() for w in range(len(pts)))
        best.append(m/eps)
    s3, s4, s5 = best   # slope = smallest |eig| / (r_* - r); an O(eps) correction is expected, so the gaps shrink about 10x per decade
    check(f"(d,l)=({dv},{l}): smallest |eig| = slope * (r_* - r) with slope -> a positive constant (gaps between slopes shrink >= 5x per decade, limit > 0.5), so the eigenvalue has a simple zero at r_*",
          abs(s4 - s5) < 0.2*abs(s3 - s4) and s5 > 0.5 and abs(s4 - s5) < 0.02*s5, f"slopes {[round(x, 4) for x in best]}")
print()
print("ALL PASS" if not FAIL else f"{len(FAIL)} FAILED: {FAIL}")
raise SystemExit(1 if FAIL else 0)
