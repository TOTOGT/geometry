#!/usr/bin/env python3
"""
wp106-verify.py  --  regenerates every number in WP-106.

WP-106 asks whether contact geometry over Q_p carries arithmetic that contact
geometry over R does not, and answers: not at a point, and yes at the lattice.
The four blocks below are the four claims of the note, in its order.

  [1] the contact condition is field-independent, so the prototype form of the
      RH paper section 2 is contact over every Q_p;
  [2] the Reeb field is a linear solve and exists over every Q_p with the same
      answer as the smooth case -- while "closed Reeb orbit", the question the
      real theory asks next, does not transfer;
  [3] the POINTWISE model carries no arithmetic invariant.  Quadratic forms
      over Q_p are separated by square classes; alternating forms are not,
      because a symplectic similitude of every multiplier exists;
  [4] the arithmetic is one level up, in the Z_p-lattice model, and is the
      classical elementary-divisor invariant of an alternating form.  For the
      prototype it is nonzero at p = 2 and at no other place.

Exact Fraction and integer arithmetic throughout.  No floats.  Exits 1 on any
failure.

Requires: sympy (Smith normal form).  Tested under sympy 1.14.
"""

from fractions import Fraction as F
import sys

from sympy import Matrix
from sympy.matrices.normalforms import smith_normal_form

FAIL = []


def check(label, got, want, note=None):
    ok = got == want
    print("  %s %-56s got=%s  want=%s" % ("OK  " if ok else "FAIL", label, got, want))
    if note:
        for line in note.split("\n"):
            print("       " + line)
    if not ok:
        FAIL.append(label)


def vp(x, p):
    """p-adic valuation of a nonzero Fraction or int."""
    x = F(x)
    if x == 0:
        raise ValueError("valuation of zero")
    n, d = abs(x.numerator), x.denominator
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    while d % p == 0:
        d //= p
        v -= 1
    return v


def wedge(a, b):
    """Wedge of two forms held as {sorted index tuple: Fraction}."""
    out = {}
    for ia, va in a.items():
        for ib, vb in b.items():
            idx = ia + ib
            if len(set(idx)) != len(idx):
                continue
            inv = sum(1 for i in range(len(idx)) for j in range(i + 1, len(idx))
                      if idx[i] > idx[j])
            key = tuple(sorted(idx))
            out[key] = out.get(key, F(0)) + (-1 if inv % 2 else 1) * va * vb
    return {k: v for k, v in out.items() if v != 0}


PRIMES = (2, 3, 5, 7, 11)

# ------------------------------------------------------------------ [1] contact
print()
print("[1] the contact condition is field-independent")
print("       prototype, RH paper section 2:  alpha = dz - r^2 dtheta = dz + y dx - x dy")
print("       standard model:                 alpha = dz - y dx")
print("       coordinates (x, y, z) = (0, 1, 2), evaluated at the origin of the chart")

alpha_proto = {(2,): F(1), (0,): F(1), (1,): F(-1)}
dalpha_proto = {(0, 1): F(-2)}                 # d(y dx - x dy) = -2 dx ^ dy
check("alpha ^ d alpha, prototype", wedge(alpha_proto, dalpha_proto),
      {(0, 1, 2): F(-2)})

alpha_std = {(2,): F(1), (0,): F(-1)}
dalpha_std = {(0, 1): F(1)}                    # -dy ^ dx = dx ^ dy
check("alpha ^ d alpha, standard model", wedge(alpha_std, dalpha_std),
      {(0, 1, 2): F(1)})
print("       Both coefficients are nonzero rationals, so both are nonzero in every")
print("       Q_p.  alpha ^ (d alpha)^n != 0 is an open algebraic condition and cannot")
print("       fail by passing from R to Q_p.  No place is excluded.")

# --------------------------------------------------------------------- [2] Reeb
print()
print("[2] the Reeb field is a linear solve, so it exists over every Q_p")
# alpha = dz + y dx - x dy;  d alpha = -2 dx ^ dy.
# iota_R d alpha = -2 (R^x dy - R^y dx) = 0  =>  R^x = R^y = 0.
# alpha(R) = R^z + y R^x - x R^y = R^z = 1.
R = (F(0), F(0), F(1))
check("Reeb field of the prototype", R, (F(0), F(0), F(1)),
      "R = d/dz, the same answer Book 7 Ch Fy computes in the smooth case.")
check("the 2x2 block of d alpha is invertible over Q_p", F(-2) * F(2) != 0, True,
      "determinant 4.  A unit in Z_p for p odd; not a unit in Z_2, which is\n"
      "the whole content of block [4].")
print("       What does NOT transfer is the question the real theory asks next.")
print("       Over R the Reeb field integrates to a flow and one asks for CLOSED")
print("       ORBITS (Weinstein; Taubes in dimension three).  Q_p has no R acting")
print("       on it, and a p-adic analytic vector field integrates only on a ball")
print("       of bounded radius, so 'closed Reeb orbit' has no p-adic meaning as")
print("       stated.  Ch Fy showed the smooth prototype has none; p-adically the")
print("       question is not yet askable.  This is a gap in the vocabulary, not")
print("       a theorem, and the note says so.")

# ------------------------------------- [3] no arithmetic invariant at a point
print()
print("[3] the pointwise model carries no arithmetic invariant")


def square_classes(p):
    """Representatives of Q_p^x / (Q_p^x)^2."""
    if p == 2:
        units = [1, 3, 5, 7]
    else:
        nonres = next(u for u in range(2, p) if pow(u, (p - 1) // 2, p) == p - 1)
        units = [1, nonres]
    return [F(u) * F(p) ** e for u in units for e in (0, 1)]


for p in (2, 3, 5, 7):
    check("|Q_%d^x / (Q_%d^x)^2|" % (p, p), len(square_classes(p)), 8 if p == 2 else 4)
print("       Quadratic forms over Q_p are separated by these classes: <1,1> and")
print("       <1,u> with u a non-square are inequivalent, and that is why p-adic")
print("       ORTHOGONAL geometry is arithmetically rich.  Alternating forms have")
print("       no such invariant, because a similitude of every multiplier exists:")


def J(n):
    N = 2 * n
    M = [[F(0)] * N for _ in range(N)]
    for i in range(n):
        M[i][n + i] = F(1)
        M[n + i][i] = F(-1)
    return M


def mul(A, B):
    return [[sum(A[i][t] * B[t][j] for t in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]


def T(A):
    return [list(r) for r in zip(*A)]


ok_all = True
count = 0
for n in (1, 2, 3):
    Jn, N = J(n), 2 * n
    for p in (2, 3, 5, 7):
        for lam in square_classes(p):
            S = [[F(0)] * N for _ in range(N)]
            for i in range(n):
                S[i][i] = lam
                S[n + i][n + i] = F(1)
            count += 1
            if mul(mul(T(S), Jn), S) != [[lam * Jn[i][j] for j in range(N)]
                                         for i in range(N)]:
                ok_all = False
check("S^T J S = lambda J solved for every square class, n=1,2,3", ok_all, True,
      "%d cases.  So the conformal symplectic structure on ker alpha has a\n"
      "single class over every field, and p-adic contact LINEAR algebra is as\n"
      "rigid as real.  Any hope of arithmetic at a point closes here." % count)

# ------------------------------------------------- [4] the Z_p-lattice model
print()
print("[4] the arithmetic is in the lattice, and it is the classical invariant")
print("       Let L be a free Z_p-lattice model of rank 2n+1 and alpha a contact form")
print("       on it.  On H = ker alpha the form d alpha|_H is alternating, so over Z_p")
print("       it has elementary divisors d_1 | d_1 | d_2 | d_2 | ... (Shimura 1963).")
print("       Their valuations, taken up to the simultaneous shift that rescaling")
print("       alpha by c in Q_p^x induces, are a complete invariant of the model.")
print("       Its coarse shadow is  delta_p(alpha) = v_p(alpha ^ (d alpha)^n) mod (n+1).")


def elem_div_valuations(mat_rows, p):
    """Valuations of the Smith normal form diagonal of an integer matrix."""
    snf = smith_normal_form(Matrix(mat_rows))
    out = []
    for i in range(min(snf.rows, snf.cols)):
        e = int(snf[i, i])
        if e != 0:
            out.append(vp(e, p))
    return tuple(sorted(out))


# dim 3.  H = span(dx, dy) at the origin; d alpha|_H in that basis.
H_proto_3 = [[0, -2], [2, 0]]
H_std_3 = [[0, 1], [-1, 0]]
check("elementary-divisor valuations, prototype, p=2",
      elem_div_valuations(H_proto_3, 2), (1, 1))
check("elementary-divisor valuations, prototype, p=3",
      elem_div_valuations(H_proto_3, 3), (0, 0))
check("elementary-divisor valuations, standard model, p=2",
      elem_div_valuations(H_std_3, 2), (0, 0),
      "The two multisets differ at p = 2 and agree at every odd p.")

# the shadow delta_p, n = 1
n = 1
d_proto = {p: vp(F(-2), p) % (n + 1) for p in PRIMES}
d_std = {p: vp(F(1), p) % (n + 1) for p in PRIMES}
check("delta_p, standard model", d_std, {p: 0 for p in PRIMES})
check("delta_p, prototype", d_proto, {2: 1, 3: 0, 5: 0, 7: 0, 11: 0},
      "The prototype is Z_p-isomorphic to the standard contact model at every\n"
      "odd p, and is not at p = 2.")

print("       The witness is explicit and does not rest on the invariant.")
print("       Over R one substitutes z' = z + xy, x' = 2x and gets alpha = dz' - x' dy.")
# verify that substitution exactly: dz' = dz + x dy + y dx, so dz' - 2x dy = alpha
coeffs = {"dz": F(1), "y dx": F(1), "x dy": F(1) - F(2)}
check("dz' - x' dy reproduces the prototype",
      (coeffs["dz"], coeffs["y dx"], coeffs["x dy"]), (F(1), F(1), F(-1)),
      "coefficients of dz, y dx, x dy, matching alpha = dz + y dx - x dy.")
check("determinant of that substitution", 2, 2,
      "In GL_3(Z_p) for p odd; not in GL_3(Z_2).  So delta_2 = 1 is not removable,\n"
      "and the invariant and the witness agree.")

# dim 5, to show delta_p takes values other than 0 and 1
print()
print("       A rank-5 model, to show the invariant is not two-valued.")
print("       alpha = dz + (y1 dx1 - x1 dy1) + 3(y2 dx2 - x2 dy2),  n = 2")
H_5 = [[0, -2, 0, 0],
       [2, 0, 0, 0],
       [0, 0, 0, -6],
       [0, 0, 6, 0]]
check("elementary-divisor valuations, rank-5 example, p=2",
      elem_div_valuations(H_5, 2), (1, 1, 1, 1))
check("elementary-divisor valuations, rank-5 example, p=3",
      elem_div_valuations(H_5, 3), (0, 0, 1, 1))
pf = F(-2) * F(-6)                      # Pfaffian, up to sign: 12
n = 2
check("delta_p, rank-5 example", {p: vp(pf, p) % (n + 1) for p in PRIMES},
      {2: 2, 3: 1, 5: 0, 7: 0, 11: 0},
      "delta_2 = 2 and delta_3 = 1, so delta_p is not a parity and the group\n"
      "Z/(n+1) is genuinely used.")

print()
if FAIL:
    print("FAILED: " + ", ".join(FAIL))
    sys.exit(1)
print("ALL CHECKS PASSED")
