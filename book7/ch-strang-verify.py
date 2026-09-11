#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ch-strang-verify.py — companion to book7/ch-strang.html.

Five blocks, standard library only. The chapter's one computation is the
symmetric matrix under the hex grid; this script does it, and then does the
one thing Orthogenesis/Geometry/HexForm.lean explicitly does NOT prove.

  [1] Q(q,r) = q^2 + qr + r^2 as a symmetric matrix: eigenvalues, trace,
      determinant, and the discriminant relation det = -disc/4.
  [2] The embedding induces Q. |hexToVec2(q,r)|^2 = Q(q,r) over a lattice box.
  [3] The six neighbours all sit at Q = 1.
  [4] AND THEY ARE THE ONLY ONES. HexForm.lean proves the six neighbours have
      Q = 1 and says in its header that it does not prove they are the only
      vectors with Q = 1 — the kissing number of the A2 lattice. This block
      establishes it by exhaustion over a box, which is evidence, not proof.
  [5] Positive definiteness by exhaustion, and the minimum of Q off the origin.

Run:  python3 ch-strang-verify.py

Principia Orthogona - Vol VII - G6 LLC - CC BY-NC-ND 4.0
"""
import math, sys
FAIL = []
def check(label, ok, detail=""):
    print(f"    {'PASS' if ok else 'FAIL'}  {label}" + (f"   {detail}" if detail else ""))
    if not ok: FAIL.append(label)
    return ok

def Q(q, r):
    return q*q + q*r + r*r

print("\n[1] The symmetric matrix")
a, bb, cc = 1.0, 1.0, 1.0          # a q^2 + b q r + c r^2
M = ((a, bb/2), (bb/2, cc))
tr = M[0][0] + M[1][1]
det = M[0][0]*M[1][1] - M[0][1]*M[1][0]
disc_sqrt = math.sqrt(tr*tr - 4*det)
lam1, lam2 = (tr + disc_sqrt)/2, (tr - disc_sqrt)/2
discriminant = bb*bb - 4*a*cc
print(f"    M                        = [[{M[0][0]}, {M[0][1]}], [{M[1][0]}, {M[1][1]}]]")
print(f"    trace, det               = {tr}, {det}")
print(f"    eigenvalues              = {lam1}, {lam2}")
print(f"    discriminant b^2-4ac     = {discriminant}")
check("eigenvalues are 3/2 and 1/2", abs(lam1-1.5) < 1e-15 and abs(lam2-0.5) < 1e-15)
check("determinant is 3/4", abs(det - 0.75) < 1e-15)
check("both eigenvalues positive, so the form is positive definite", lam1 > 0 and lam2 > 0)
check("discriminant is -3", abs(discriminant + 3.0) < 1e-15)
check("det(M) = -discriminant/4", abs(det - (-discriminant/4.0)) < 1e-15)

print("\n[2] The embedding induces Q")
N = 40
worst = 0.0
for q in range(-N, N+1):
    for r in range(-N, N+1):
        x = q + r/2.0
        y = (math.sqrt(3.0)/2.0) * r
        worst = max(worst, abs(x*x + y*y - Q(q, r)))
print(f"    box                      = [-{N},{N}]^2  ({(2*N+1)**2} lattice points)")
print(f"    max |  |v|^2 - Q(q,r)  | = {worst:.3e}")
check("hexToVec2 norm^2 equals Q on every point of the box", worst < 1e-9)

print("\n[3] The six neighbours")
neigh = [(1,0), (1,-1), (0,-1), (-1,0), (-1,1), (0,1)]
for (dq, dr) in neigh:
    check(f"Q({dq:2d},{dr:2d}) == 1", Q(dq, dr) == 1)

print("\n[4] Kissing number — the step the Lean file declines")
ones = [(q, r) for q in range(-N, N+1) for r in range(-N, N+1) if Q(q, r) == 1]
print(f"    solutions of Q = 1 in the box = {len(ones)}")
print(f"    they are                      = {sorted(ones)}")
check("there are exactly six", len(ones) == 6)
check("they are exactly the hexNeighbors offsets", sorted(ones) == sorted(neigh))

print("\n[5] Positive definiteness by exhaustion")
vals = [Q(q, r) for q in range(-N, N+1) for r in range(-N, N+1) if (q, r) != (0, 0)]
print(f"    min Q over nonzero points     = {min(vals)}")
check("Q is strictly positive off the origin", min(vals) > 0)
check("the minimum is 1", min(vals) == 1)
check("Q(0,0) = 0", Q(0, 0) == 0)

print("""
[HONESTY] What this script establishes, and what it does not.

  ESTABLISHED. The matrix arithmetic exactly. Blocks [2], [4] and [5] are
  exhaustions over a finite box: strong evidence, and not proof. Block [4] in
  particular is the statement HexForm.lean's header declines — that the six
  neighbours are the ONLY vectors of norm one — and a box search cannot
  establish it for all integers. The honest reading is that the Lean file
  proves the six are there and this script gives reason to believe nothing
  else is.

  NOT ESTABLISHED. The eigenvalue computation is not in the Lean file and is
  not under the kernel; the chapter says so. Nothing here identifies Q with
  the Eisenstein integers as a ring, or with the A2 root lattice as a lattice;
  the quadratic forms agree and that is all that is checked.
""")
print(f"{'ALL CHECKS PASSED' if not FAIL else 'FAILED: ' + ', '.join(FAIL)}")
sys.exit(1 if FAIL else 0)
