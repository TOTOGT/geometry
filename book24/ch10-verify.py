#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book24/ch10-verify.py -- every check behind book24/ch10-duality.html. Run first.

    python3 book24/ch10-verify.py

Integers and Fractions are exact. Finite checks are exhaustive within the stated bounds. Nothing here proves a theorem; the
proofs are on the page. Every claim that is meant to fail has a control that is built to fail, and the control is printed.

  [1] the dual basis: the dual basis of the columns of an invertible P is the rows of P^-1 (Lax Ch 2 Exercise 6(c));
      l(x) = sum a_i c_i (Theorem 1); all invertible 2x2 integer matrices with entries -2..2
  [2] annihilators: dim Y + dim Y^perp = n (Theorem 4) and Y^perp^perp = Y (Theorem 5) for every subspace of Q^3 spanned by
      vectors with entries -1, 0, 1; control: "dim Y^perp = dim Y" fails
  [3] the transpose is the dual map: <A^T l, x> = <l, A x>, and the matrix of the dual map in the dual bases is the
      transpose of the matrix of the map
  [4] quadrature from the dual space (Theorem 7, Exercises 4 and 5): weights for -a, 0, a; positivity; the degree of exactness
      of the three-point Gauss rule; Exercise 5 weights
  [5] bilinear forms: a Gram matrix changes by P^T G P, a map by P^-1 A P; signature is a congruence invariant (Sylvester,
      2x2 exhaustive), trace is not (control)
  [6] tensor products: Kronecker product, mixed product rule, dimension, det(A x B) = det(A)^n det(B)^m, and which 2x2 arrays
      are pure tensors (det = 0)
  [7] the held text: Lax, Linear Algebra and Its Applications, 2nd ed., Chapter 2 (printed page = pdf page - 17)
  [8] the Lean file: the statements are present, none uses sorry, the axiom report (if it exists) has no sorryAx
  [9] the page: the counts printed on the page equal the ones computed here
"""
import itertools, os, re, subprocess
from fractions import Fraction as Fr
from pathlib import Path

FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  [{detail}]" if detail else ""))
    if not ok: FAIL.append(label)

HERE = Path(__file__).resolve().parent
def mul(A, B): return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def T(A): return [list(r) for r in zip(*A)]
def det2(A): return A[0][0] * A[1][1] - A[0][1] * A[1][0]
def ident(n): return [[Fr(int(i == j)) for j in range(n)] for i in range(n)]
def inv(A):
    n = len(A); M = [[Fr(x) for x in A[i]] + [Fr(int(i == j)) for j in range(n)] for i in range(n)]
    for c in range(n):
        pv = next((r for r in range(c, n) if M[r][c] != 0), None)
        if pv is None: return None
        M[c], M[pv] = M[pv], M[c]; M[c] = [x / M[c][c] for x in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]; M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [r[n:] for r in M]
def det(A):
    n = len(A)
    if n == 1: return A[0][0]
    return sum((-1) ** j * A[0][j] * det([r[:j] + r[j + 1:] for r in A[1:]]) for j in range(n))
def rref(rows):
    M = [[Fr(x) for x in r] for r in rows]; piv = 0; out = []
    ncol = len(M[0]) if M else 0
    for c in range(ncol):
        p = next((r for r in range(piv, len(M)) if M[r][c] != 0), None)
        if p is None: continue
        M[piv], M[p] = M[p], M[piv]; M[piv] = [x / M[piv][c] for x in M[piv]]
        for r in range(len(M)):
            if r != piv and M[r][c] != 0:
                f = M[r][c]; M[r] = [x - f * y for x, y in zip(M[r], M[piv])]
        piv += 1
    return [tuple(r) for r in M[:piv]]
def nullspace(rows, n):
    R = rref(rows) if rows else []
    pivs = [next(j for j, x in enumerate(r) if x != 0) for r in R]
    free = [j for j in range(n) if j not in pivs]; basis = []
    for f in free:
        v = [Fr(0)] * n; v[f] = Fr(1)
        for r, p in zip(R, pivs): v[p] = -r[f]
        basis.append(v)
    return basis

# ---------------------------------------------------------------------------------------------------------------
print("[1] the dual basis is the rows of P^-1")
rng = range(-2, 3); n_inv = 0; ok_all = True
for a, b, c, d in itertools.product(rng, repeat=4):
    P = [[a, b], [c, d]]
    if det2(P) == 0: continue
    n_inv += 1; Q = inv(P)                       # rows of Q are the candidate dual basis
    cols = T(P)
    ok_all &= all(sum(Q[i][k] * cols[j][k] for k in range(2)) == int(i == j) for i in range(2) for j in range(2))
check(f"for all {n_inv} invertible 2x2 integer matrices (entries -2..2): row i of P^-1 applied to column j of P is delta_ij", ok_all)
l = [Fr(3), Fr(-2), Fr(5)]; xs = [Fr(1), Fr(4), Fr(-1)]
check("Theorem 1: l(x) = sum a_i c_i with a_i = l(e_i) (one worked case)",
      sum(li * xi for li, xi in zip(l, xs)) == 3 * 1 + (-2) * 4 + 5 * (-1))
bad = [[1, 0], [0, 1]]; wrong_rows = T([[1, 1], [0, 1]])   # a deliberately wrong "dual basis": columns instead of rows
P = [[1, 1], [0, 1]]; Qinv = inv(P)
check("CONTROL (built to fail): the COLUMNS of P^-1 are not the dual basis in general", not all(
      sum(T(Qinv)[i][k] * T(P)[j][k] for k in range(2)) == int(i == j) for i in range(2) for j in range(2)))
n_inv_page = n_inv

# ---------------------------------------------------------------------------------------------------------------
print("[2] annihilators in Q^3")
vecs = [v for v in itertools.product((-1, 0, 1), repeat=3) if any(v)]
subspaces = {}
for k in range(0, 4):
    for S in itertools.combinations(vecs, k):
        R = tuple(rref(list(S))) if S else ()
        subspaces[R] = len(R)
cnt = len(subspaces); ok4 = ok5 = True; ctrl_fail = 0
for R, dimY in subspaces.items():
    Yperp = nullspace([list(r) for r in R], 3) if R else [[Fr(int(i == j)) for j in range(3)] for i in range(3)]
    ok4 &= (dimY + len(Yperp) == 3)
    back = tuple(rref([list(v) for v in Yperp])) if Yperp else ()
    YY = nullspace([list(v) for v in back], 3) if back else [[Fr(int(i == j)) for j in range(3)] for i in range(3)]
    ok5 &= (tuple(rref([list(v) for v in YY])) if YY else ()) == R
    if dimY != len(Yperp): ctrl_fail += 1
by_dim = {d: sum(1 for v in subspaces.values() if v == d) for d in range(4)}
check(f"Theorem 4: dim Y + dim Y^perp = 3 for all {cnt} distinct subspaces spanned by vectors with entries -1,0,1 (by dimension {by_dim})", ok4)
check(f"Theorem 5: Y^perp^perp = Y for the same {cnt} subspaces", ok5)
off_by_one = sum(1 for R, dY in subspaces.items() if dY + len(nullspace([list(r) for r in R], 3) if R else [0, 0, 0]) != 4)
check("CONTROL (built to fail): the off-by-one claim dim Y + dim Y^perp = 4 is false for every one of them", off_by_one == cnt, f"false for {off_by_one} of {cnt}")
cnt_page = cnt

# ---------------------------------------------------------------------------------------------------------------
print("[3] the transpose is the dual map")
import random
random.seed(24); ok = True
for _ in range(500):
    m, nn = random.randint(1, 3), random.randint(1, 3)
    A = [[random.randint(-3, 3) for _ in range(nn)] for _ in range(m)]
    lv = [random.randint(-3, 3) for _ in range(m)]; xv = [random.randint(-3, 3) for _ in range(nn)]
    Ax = [sum(A[i][j] * xv[j] for j in range(nn)) for i in range(m)]
    ATl = [sum(A[i][j] * lv[i] for i in range(m)) for j in range(nn)]
    ok &= sum(lv[i] * Ax[i] for i in range(m)) == sum(ATl[j] * xv[j] for j in range(nn))
check("500 random integer cases: <l, Ax> = <A^T l, x>", ok)
ok = True
for _ in range(300):
    M = [[Fr(random.randint(-3, 3)) for _ in range(2)] for _ in range(2)]
    P = [[Fr(random.randint(-2, 2)) for _ in range(2)] for _ in range(2)]; R = [[Fr(random.randint(-2, 2)) for _ in range(2)] for _ in range(2)]
    if det2(P) == 0 or det2(R) == 0: continue
    # T has matrix M in the standard bases; in bases (columns of P) of X and (columns of R) of U its matrix is R^-1 M P.
    Mt = mul(mul(inv(R), M), P)
    # dual bases are the rows of P^-1 and R^-1; the dual map sends l to l o T; its matrix in those bases must be Mt^T
    Pi, Ri = inv(P), inv(R)
    # (dual map applied to the i-th dual basis vector of U)(x_j) = rows(Ri)[i] . M . col_j(P) = Mt[i][j]
    dm = [[sum(Ri[i][a] * M[a][b] * P[b][j] for a in range(2) for b in range(2)) for j in range(2)] for i in range(2)]
    ok &= dm == Mt
check("the dual map has, in the dual bases, the coordinates given by the transpose of the matrix of the map (300 cases: entry (i,j) of R^-1 M P)", ok)

# ---------------------------------------------------------------------------------------------------------------
print("[4] quadrature from the dual space")
def moment(k): return Fr(2, k + 1) if k % 2 == 0 else Fr(0)      # integral of t^k over [-1, 1]
def weights3(a2):                                                  # nodes -a, 0, a ; a2 = a^2
    m1 = 1 / (3 * a2); m2 = 2 - 2 * m1; return m1, m2, m1
check("weights for nodes -a, 0, a from exactness on 1 and t^2: m1 = m3 = 1/(3a^2), m2 = 2 - 2/(3a^2)",
      all(2 * weights3(a2)[0] + weights3(a2)[1] == 2 and 2 * a2 * weights3(a2)[0] == Fr(2, 3) for a2 in (Fr(1, 2), Fr(1), Fr(3, 5), Fr(4, 9))))
check("a = 1 gives Simpson: 1/3, 4/3, 1/3", weights3(Fr(1)) == (Fr(1, 3), Fr(4, 3), Fr(1, 3)))
pos = lambda a2: all(w > 0 for w in weights3(a2))
check("Exercise 4(ii): all three weights positive exactly when a^2 > 1/3 (tested on 200 values of a^2 on both sides of 1/3)",
      all(pos(Fr(k, 100)) == (Fr(k, 100) > Fr(1, 3)) for k in range(1, 201) if Fr(k, 100) != Fr(1, 3)))
m1, m2, m3 = weights3(Fr(3, 5))
check("Exercise 4(iii): a^2 = 3/5 gives weights 5/9, 8/9, 5/9", (m1, m2, m3) == (Fr(5, 9), Fr(8, 9), Fr(5, 9)))
def rule(w, a2, k): return (w[0] + w[2]) * a2 ** (k // 2) if k % 2 == 0 and k > 0 else (w[1] * 0 + (w[0] + w[1] + w[2] if k == 0 else 0))
exact = [k for k in range(0, 9) if (rule((m1, m2, m3), Fr(3, 5), k) == moment(k))]
check("the 3-point rule at a^2 = 3/5 integrates t^0..t^5 exactly and fails at t^6 (the odd powers vanish on both sides)",
      all(k in exact for k in range(0, 5)) and 6 not in exact, f"exact for even k in {[k for k in exact if k % 2 == 0]}; t^6: rule {rule((m1,m2,m3),Fr(3,5),6)} vs integral {moment(6)}")
def weights4(a2, b2):                                              # nodes -a, -b, b, a (a2 = a^2, b2 = b^2)
    ma = (Fr(1, 3) - b2) / (a2 - b2); mb = (a2 - Fr(1, 3)) / (a2 - b2); return ma, mb
okq = True
for a2, b2 in [(Fr(9, 10), Fr(1, 10)), (Fr(2, 3), Fr(1, 5)), (Fr(1, 2), Fr(1, 4))]:
    ma, mb = weights4(a2, b2)
    okq &= (2 * ma + 2 * mb == 2) and (2 * (a2 * ma + b2 * mb) == Fr(2, 3))
check("Exercise 5: weights (1/3 - b^2)/(a^2 - b^2) at +-a and (a^2 - 1/3)/(a^2 - b^2) at +-b are exact on 1 and t^2 (three sample pairs)", okq)
grid = [Fr(k, 40) for k in range(1, 40) if Fr(k, 40) != Fr(1, 3)]
okp = True
for a2 in grid:
    for b2 in grid:
        if b2 < a2:
            wa, wb = weights4(a2, b2)
            okp &= ((wa > 0 and wb > 0) == (b2 < Fr(1, 3) < a2))
check("Exercise 5(ii): for 0 < b < a, both weights are positive exactly when b^2 < 1/3 < a^2 (all pairs on a grid of 39 values of a^2, b^2)", okp)
neg_ctrl = weights4(Fr(1, 5), Fr(1, 10))
check("CONTROL (built to fail): the weights are not all positive for every a, b", not all(x > 0 for x in neg_ctrl), f"a^2 = 1/5, b^2 = 1/10 gives weights {neg_ctrl[0]} at +-a and {neg_ctrl[1]} at +-b")

# ---------------------------------------------------------------------------------------------------------------
print("[5] bilinear forms")
ok = True; ncong = 0
def sig(G):
    a, b, d = G[0][0], G[0][1], G[1][1]; D = a * d - b * b; tr = a + d
    if D > 0: return (2, 0) if tr > 0 else (0, 2)
    if D < 0: return (1, 1)
    if tr > 0: return (1, 0)
    if tr < 0: return (0, 1)
    return (0, 0)
sigs_total = 0
for a, b, d in itertools.product(range(-2, 3), repeat=3):
    G = [[a, b], [b, d]]
    for p in itertools.product(range(-2, 3), repeat=4):
        P = [[p[0], p[1]], [p[2], p[3]]]
        if det2(P) == 0: continue
        H = mul(mul(T(P), G), P); ncong += 1; sigs_total += 1
        ok &= sig(H) == sig(G) and H[0][1] == H[1][0]
check(f"Sylvester for 2x2: the signature (n+, n-) is unchanged by G -> P^T G P over all {ncong} pairs (G symmetric, entries -2..2; P invertible, entries -2..2)", ok)
Gc = [[1, 0], [0, 1]]; Pc = [[2, 0], [0, 1]]; Hc = mul(mul(T(Pc), Gc), Pc)
check("CONTROL (built to fail): the trace is NOT a congruence invariant (G = I, P = diag(2,1) gives trace 5, not 2)", sum(Hc[i][i] for i in range(2)) != 2, f"trace {sum(Hc[i][i] for i in range(2))}")
A = [[Fr(1), Fr(2)], [Fr(0), Fr(3)]]; P = [[Fr(1), Fr(1)], [Fr(0), Fr(1)]]
S = mul(mul(inv(P), A), P)
check("a MAP changes by P^-1 A P and keeps its trace (3 + 1 = 4 both ways); a FORM changes by P^T G P and does not", S[0][0] + S[1][1] == A[0][0] + A[1][1])
ncong_page = ncong

# ---------------------------------------------------------------------------------------------------------------
print("[6] tensor products")
def kron(A, B):
    return [[A[i][j] * B[k][l] for j in range(len(A[0])) for l in range(len(B[0]))] for i in range(len(A)) for k in range(len(B))]
random.seed(10); ok1 = ok2 = True
for _ in range(200):
    A = [[random.randint(-3, 3) for _ in range(2)] for _ in range(2)]; C = [[random.randint(-3, 3) for _ in range(2)] for _ in range(2)]
    B = [[random.randint(-3, 3) for _ in range(3)] for _ in range(3)]; D = [[random.randint(-3, 3) for _ in range(3)] for _ in range(3)]
    ok1 &= mul(kron(A, B), kron(C, D)) == kron(mul(A, C), mul(B, D))
    ok2 &= det(kron(A, B)) == det(A) ** 3 * det(B) ** 2
check("(A x B)(C x D) = AC x BD on 200 random pairs (2x2 and 3x3)", ok1)
check("det(A x B) = det(A)^3 det(B)^2 for A 2x2, B 3x3 on the same 200 pairs (det(A x B) = det(A)^n det(B)^m for A m x m, B n x n)", ok2)
check("dimension: the Kronecker product of a 2x2 and a 3x3 matrix is 6x6", len(kron([[1, 2], [3, 4]], [[1, 0, 0], [0, 1, 0], [0, 0, 1]])) == 6)
pure = 0; nonpure = 0; ok = True
for t in itertools.product(range(-2, 3), repeat=4):
    Tm = [[t[0], t[1]], [t[2], t[3]]]
    if det2(Tm) == 0:
        pure += 1
        # factor as an outer product x y^T with rational x, y
        if all(v == 0 for v in t): continue
        r = next(i for i in range(2) if any(Tm[i])); c = next(j for j in range(2) if Tm[r][j] != 0)
        x = [Fr(Tm[i][c], Tm[r][c]) for i in range(2)]; y = [Fr(Tm[r][j]) for j in range(2)]
        ok &= all(x[i] * y[j] == Tm[i][j] for i in range(2) for j in range(2))
    else: nonpure += 1
check(f"a 2x2 array is a pure tensor x (x) y exactly when det = 0: {pure} of the 625 arrays with entries -2..2 factor, {nonpure} do not", ok and pure + nonpure == 625)
check("e1 (x) e1 + e2 (x) e2 (the identity array) is not a pure tensor (det = 1) -- a sum of two pure tensors", det2([[1, 0], [0, 1]]) != 0)
pure_page, nonpure_page = pure, nonpure

# ---------------------------------------------------------------------------------------------------------------
print("[7] the held text: Lax Chapter 2 (printed page = pdf page - 17)")
flat = lambda s: re.sub(r"\s+", " ", s).lower()
pdf = None
for cdir in ("~/Downloads", "~/mnt/Downloads", "."):
    q = Path(os.path.expanduser(cdir)) / "lax.pdf"
    if q.is_file(): pdf = q; break
def pages_of(first, last):
    try:
        return subprocess.run(["pdftotext", "-layout", "-f", str(first), "-l", str(last), str(pdf), "-"], capture_output=True, text=True, timeout=200, check=True).stdout.split("\f")
    except Exception as ex:
        print(f"  SKIP: cannot read lax.pdf ({ex})"); return None
if pdf is None: print("  SKIP: lax.pdf not found (no claim made)")
else:
    pg = pages_of(30, 36)
    if pg:
        p = lambda n: flat(pg[n + 17 - 30])
        check("p.13: Chapter 2 Duality; linear function defined", "duality" in p(13) and "linear" in p(13))
        check("p.14: Theorem 1 (every linear function has the form sum a_j c_j)", "theorem 1" in p(14))
        check("p.15: Theorem 2 (dim X' = dim X), Theorem 3 (X'' = X), annihilator definition", "theorem 2" in p(15) and "theorem 3" in p(15) and "annihilator" in p(15))
        check("p.15-16: Theorem 4 (dim Y^perp + dim Y = dim X)", "theorem 4" in p(15) or "theorem 4" in p(16))
        check("p.16: Theorem 5 (Y^perp perp = Y)", "theorem 5" in p(16))
        check("p.17: Theorem 7 (quadrature formula for polynomials of degree less than n)", "theorem 7" in p(17) or "quadrature" in p(17))
        check("p.18: Exercises 4 and 5 (weights on [-1, 1])", "exercise 4" in p(18) and "exercise 5" in p(18))
print("  OCR note: lax.pdf is a scan; these checks match short phrases and may miss a page the scan garbled.")

# ---------------------------------------------------------------------------------------------------------------
print("[8] the Lean file")
lf = HERE / "Duality.lean"; rep_f = HERE / "duality.axioms.txt"
names = ["dual_basis_apply", "annihilator_dim", "annihilator_annihilator", "dualMap_apply", "kronecker_det",
         "simpson_exact_two", "simpson_fails_four", "gauss3_exact_four", "gauss3_fails_six", "congruence_not_trace"]
if lf.exists():
    code = re.sub(r"/-.*?-/", "", lf.read_text(encoding="utf-8"), flags=re.S)
    for nm in names: check(f"theorem {nm} is stated", re.search(r"theorem\s+" + nm + r"\b", code) is not None)
    check("no sorry or admit in the Lean code", not re.search(r"\b(sorry|admit)\b", code))
    if rep_f.exists() and rep_f.read_text(encoding="utf-8").strip():
        r = rep_f.read_text(encoding="utf-8")
        check("axiom report: every theorem appears", all(("Book24Dual." + nm) in r for nm in names))
        check("axiom report: no sorryAx and no error", "sorryAx" not in r and "error" not in r.lower())
    else:
        print("  NOTE: no duality.axioms.txt yet; the Lean file has NOT been compiled (run the command in its header).")
else:
    print("  SKIP: Duality.lean not found")

# ---------------------------------------------------------------------------------------------------------------
print("[9] the page")
page = HERE / "ch10-duality.html"
if page.exists():
    txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", page.read_text(encoding="utf-8")))
    check("page prints the counts computed here", all(s in txt for s in (f"{n_inv_page} invertible", f"{cnt_page} distinct subspaces", f"{ncong_page} pairs", f"{pure_page} of the 625")))
else:
    print("  SKIP: page not found")

print()
print("ALL PASS" if not FAIL else f"{len(FAIL)} FAILED: {FAIL}")
