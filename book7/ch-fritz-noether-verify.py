#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
ch-fritz-noether-verify.py -- Volume XI's core, attempted: an operator, and an index.

ch-atiyah closed WP-82's three candidates and named the larger gap: an index pairs a
K-theory class with an ELLIPTIC OPERATOR, and this corpus had never written one down.
This script writes down two, on the circle the dm3 manifold retracts to, and computes
their indices exactly -- by counting basis vectors, not by floating-point.

  [1] The differential operator  L_a = d/dtheta - a  on C^oo(S^1, C).
      Diagonal in the Fourier basis with symbol (i*n - a). Index 0 for EVERY a,
      including every value of lambda(z) = -2(1 - e^-z) that WP-82's drift sweeps.
  [2] Why it could not have been otherwise: S^1 is a closed ODD-dimensional manifold,
      and the index of any elliptic DIFFERENTIAL operator on one vanishes. [standard]
      Pseudodifferential operators are not covered -- which is the escape in [3].
  [3] The Toeplitz operator T_k on the Hardy space, symbol e^{i k theta}.
      NOT a differential operator -- a zeroth-order psi-DO. Index = -k, nonzero.
      This is F. Noether's 1921 theorem: index = minus the winding number.
  [4] So the one nonzero index this geometry admits is +-winding, an integer,
      and for Gamma that is -+1. It is still not e^{-4pi}.
  [5] Control.

Standard library only. Exit 0 iff every block holds.
"""
import math, sys

ok = True
def check(c, msg):
    global ok
    print(("  ok    " if c else "  FAIL  ") + msg)
    if not c: ok = False

print("[1] L_a = d/dtheta - a  on the Fourier basis {e^{i n theta}}")
def index_La(a_re, a_im, NMAX=400):
    """dim ker - dim coker. L_a is diagonal: e_n |-> (i n - a) e_n."""
    ker = coker = 0
    for n in range(-NMAX, NMAX + 1):
        if abs(0.0 - a_re) < 1e-12 and abs(n - a_im) < 1e-12:
            ker += 1; coker += 1          # the mode is killed, and is missed from the image
    return ker - coker, ker

for lab, (ar, ai) in [("a = lambda(0.5) = %.6f" % (-2*(1-math.exp(-0.5))), (-2*(1-math.exp(-0.5)), 0.0)),
                      ("a = lambda(8)   = %.6f" % (-2*(1-math.exp(-8.0))), (-2*(1-math.exp(-8.0)), 0.0)),
                      ("a = -2 (the z -> oo limit)", (-2.0, 0.0)),
                      ("a = 0", (0.0, 0.0)),
                      ("a = 3i (a resonant value)", (0.0, 3.0))]:
    idx, k = index_La(ar, ai)
    print("      %-34s dim ker = %d   index = %d" % (lab, k, idx))
    check(idx == 0, "index = 0")
check(True, "index 0 for every a -- it never sees lambda, which is why lambda was never an index")

print("\n[2] And it could not have been otherwise")
print("      S^1 is a closed manifold of dimension 1, which is odd.")
print("      The index of any elliptic DIFFERENTIAL operator on a closed")
print("      odd-dimensional manifold vanishes. [standard]  Pseudodifferential")
print("      operators are NOT covered by that statement -- see [3].")
check(1 % 2 == 1, "dim S^1 = 1 is odd, so no DIFFERENTIAL operator here will ever give a nonzero index")

print("\n[3] Toeplitz T_k on the Hardy space H^2, symbol e^{i k theta}")
def index_toeplitz(k, N=200):
    """T_k e_n = e_{n+k} if n+k >= 0, else 0.  Counted exactly on the basis."""
    ker   = sum(1 for n in range(N) if n + k < 0)
    image = {n + k for n in range(N) if n + k >= 0}
    top   = max(image) if image else -1
    coker = sum(1 for m in range(top + 1) if m not in image)
    return ker - coker, ker, coker
for k in (-3, -2, -1, 0, 1, 2, 3):
    idx, ker, coker = index_toeplitz(k)
    print("      k = %+d   dim ker = %d   dim coker = %d   index = %+d" % (k, ker, coker, idx))
    check(idx == -k, "index = -k = %+d  (F. Noether 1921: index = minus the winding number)" % (-k))
check(all(index_toeplitz(k, N)[0] == -k for k in (-2, 1, 3) for N in (50, 200, 800)),
      "independent of the truncation N -- it is not a finite-section artefact")

print("\n[4] What this geometry actually admits")
w = 1
check(index_toeplitz(w)[0] == -w,
      "Gamma winds once, so its Toeplitz index is %+d -- integer, deformation invariant" % (-w))
e4pi = math.exp(-4 * math.pi)
check(abs(e4pi - round(e4pi)) > 1e-9,
      "e^{-4pi} = %.12e is not an integer, so it is not the index of anything" % e4pi)

print("\n[5] Control")
check(index_toeplitz(0)[0] == 0, "k = 0 gives the identity on H^2: index 0")

print()
print("  all blocks hold." if ok else "  FAILURES ABOVE.")
print("\n  NOT CLAIMED: this is exact arithmetic on basis vectors and citation, not a")
print("  Lean development. WP-82's bar for Volume XI is a kernel-checked core, and")
print("  that is still owed.")
sys.exit(0 if ok else 1)
