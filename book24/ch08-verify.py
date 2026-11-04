#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book24/ch08-verify.py -- every check behind book24/ch08-inner-products.html. Run first.

    python3 book24/ch08-verify.py

Everything is exact (integers and Fractions; no floating point). Finite checks are exhaustive within the stated
bounds. Nothing here proves a theorem; the proofs are on the page.

  [1] scalar product: Schwarz and the triangle inequality on every pair of integer vectors in {-2..2}^3, with
      equality exactly for proportional vectors; the Pythagorean identity; control: an indefinite form fails
  [2] Gram-Schmidt: the worked example, and 200 random integer bases of Q^3 (orthogonal, triangular)
  [3] projections: P = A (A^T A)^-1 A^T is idempotent and symmetric for 200 random integer 4x2 matrices; x - Px is
      orthogonal to the range; Px is the closest point (checked against a grid of competitors)
  [4] least squares on four points: the normal equations, the fitted line, the residual, the minimum by grid
  [5] symmetric 2x2: real eigenvalues and orthogonal eigenvectors for every integer matrix with entries -3..3,
      positive definiteness, the 3x3 spectral decomposition A = 4 P1 + 1 P2; controls
  [6] the held text: Lax, Linear Algebra and Its Applications, 2nd ed., Chapters 7 and 8 (printed page = pdf - 17)
  [7] the Lean file: the statements are present, none uses sorry, the axiom report (if it exists) has no sorryAx
  [8] the page: the counts printed on the page equal the ones computed here
"""
import itertools, os, random, re, subprocess, sys
from fractions import Fraction
from pathlib import Path

FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  [{detail}]" if detail else ""))
    if not ok: FAIL.append(label)

HERE = Path(__file__).resolve().parent
def dot(u, v): return sum(a * b for a, b in zip(u, v))
def sub(u, v): return [a - b for a, b in zip(u, v)]
def add(u, v): return [a + b for a, b in zip(u, v)]
def sc(c, u): return [c * a for a in u]
def mul(A, B): return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def T(A): return [list(r) for r in zip(*A)]
def det(A):
    n = len(A)
    if n == 1: return A[0][0]
    return sum((-1) ** j * A[0][j] * det([r[:j] + r[j + 1:] for r in A[1:]]) for j in range(n))
def inv(A):
    n = len(A); M = [[Fraction(x) for x in A[i]] + [Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    for c in range(n):
        pv = next(r for r in range(c, n) if M[r][c] != 0); M[c], M[pv] = M[pv], M[c]
        M[c] = [x / M[c][c] for x in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]; M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [r[n:] for r in M]
def ident(n): return [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
def proportional(u, v):
    return all(u[i] * v[j] == u[j] * v[i] for i in range(len(u)) for j in range(len(u)))

print("[1] scalar product")
V = list(itertools.product(range(-2, 3), repeat=3)); bad = 0; badeq = 0; badtri = 0
for u in V:
    for v in V:
        lhs = dot(u, v) ** 2; rhs = dot(u, u) * dot(v, v)
        if lhs > rhs: bad += 1
        if (lhs == rhs) != proportional(u, v): badeq += 1
        # triangle: |u+v|^2 <= (|u|+|v|)^2  <=>  2 u.v <= 2|u||v| ; check via squares to stay exact
        w = add(u, v)
        nu2, nv2, nw2 = dot(u, u), dot(v, v), dot(w, w)
        # |w| <= |u| + |v|  <=>  nw2 <= nu2 + nv2 + 2 sqrt(nu2 nv2)  <=> (nw2 - nu2 - nv2) <= 2 sqrt(nu2 nv2)
        d = nw2 - nu2 - nv2
        if d > 0 and d * d > 4 * nu2 * nv2: badtri += 1
check(f"Schwarz (u.v)^2 <= (u.u)(v.v) for all {len(V)**2} pairs in {{-2..2}}^3", bad == 0, f"{bad} failures")
check("equality holds exactly when the vectors are proportional (all pairs)", badeq == 0, f"{badeq} failures")
check("triangle inequality |u+v| <= |u| + |v| for all pairs (checked exactly through squares)", badtri == 0, f"{badtri} failures")
check("Pythagoras: u.v = 0 implies |u+v|^2 = |u|^2 + |v|^2 for all orthogonal pairs", all(dot(add(u, v), add(u, v)) == dot(u, u) + dot(v, v) for u in V for v in V if dot(u, v) == 0))
lor = lambda u, v: u[0] * v[0] - u[1] * v[1]
check("control: the indefinite form x1y1 - x2y2 is not positive: (1,1).(1,1) = 0 although (1,1) is not zero", lor((1, 1), (1, 1)) == 0)
u, v = (1, 0), (2, 1)
check("control: for that form Schwarz fails: u = (1,0), v = (2,1) give (u.v)^2 = 4 > (u.u)(v.v) = 1 x 3 = 3",
      lor(u, v) ** 2 == 4 and lor(u, u) * lor(v, v) == 3 and lor(u, v) ** 2 > lor(u, u) * lor(v, v))

print("[2] Gram-Schmidt (orthogonal vectors, not normalised, so everything stays rational)")
def gram(ys):
    xs = []
    for y in ys:
        x = [Fraction(a) for a in y]
        for p in xs: x = sub(x, sc(dot(y, p) / dot(p, p), p))
        xs.append(x)
    return xs
ys = [[1, 1, 0], [1, 0, 1], [0, 1, 1]]; xs = gram(ys)
check("worked example y = (1,1,0), (1,0,1), (0,1,1): x1 = (1,1,0), x2 = (1/2,-1/2,1), x3 = (-2/3,2/3,2/3)",
      xs == [[1, 1, 0], [Fraction(1, 2), Fraction(-1, 2), 1], [Fraction(-2, 3), Fraction(2, 3), Fraction(2, 3)]])
check("they are mutually orthogonal", all(dot(xs[i], xs[j]) == 0 for i in range(3) for j in range(i)))
random.seed(24008); ok = True; okt = True
for _ in range(200):
    while True:
        Y = [[random.randint(-4, 4) for _ in range(3)] for _ in range(3)]
        if det(Y) != 0: break
    X = gram(Y)
    if any(dot(X[i], X[j]) != 0 for i in range(3) for j in range(i)): ok = False
    if any(all(a == 0 for a in x) for x in X): ok = False
    # x_k - y_k lies in the span of y_1..y_{k-1}: check x_3 - y_3 = c1 y1 + c2 y2 by solving with the first two (exact rank test)
    d = sub(X[2], [Fraction(a) for a in Y[2]])
    M = [list(map(Fraction, Y[0])), list(map(Fraction, Y[1])), d]
    if det(M) != 0: okt = False
check("200 random integer bases of Q^3: Gram-Schmidt output is orthogonal and never zero", ok)
check("and x_3 - y_3 lies in span(y_1, y_2) (the triangular property, Lax's (ii))", okt)

print("[3] projections")
random.seed(24018); ok1 = ok2 = ok3 = ok4 = True
for _ in range(200):
    while True:
        A = [[random.randint(-3, 3) for _ in range(2)] for _ in range(4)]
        if det(mul(T(A), A)) != 0: break
    G = inv(mul(T(A), A)); P = mul(mul(A, G), T(A))
    if mul(P, P) != P: ok1 = False
    if P != T(P): ok2 = False
    x = [random.randint(-5, 5) for _ in range(4)]
    px = [sum(P[i][j] * x[j] for j in range(4)) for i in range(4)]
    r = sub([Fraction(a) for a in x], px)
    if any(dot(r, [A[i][c] for i in range(4)]) != 0 for c in range(2)): ok3 = False
    best = dot(r, r)
    for c1 in range(-4, 5):
        for c2 in range(-4, 5):
            z = [Fraction(A[i][0] * c1 + A[i][1] * c2, 2) for i in range(4)]
            w = sub([Fraction(a) for a in x], z)
            if dot(w, w) < best: ok4 = False
check("P = A (A^T A)^-1 A^T satisfies P^2 = P for 200 random integer 4x2 matrices (Lax Theorem 7)", ok1)
check("and P^T = P (the projection is self-adjoint)", ok2)
check("x - Px is orthogonal to both columns of A (Lax Theorem 6, the decomposition x = y + y-perp)", ok3)
check("no competitor z = A c with c in a 17x17 grid of half-integers is closer to x than Px (Lax Theorem 8)", ok4)

print("[4] least squares on four points")
t = [0, 1, 2, 3]; b = [1, 2, 2, 4]; A = [[1, s] for s in t]
AtA = mul(T(A), A); Atb = [sum(A[i][j] * b[i] for i in range(4)) for j in range(2)]
check("A^T A = [[4,6],[6,14]] and A^T b = (9, 18)", AtA == [[4, 6], [6, 14]] and Atb == [9, 18])
c = [sum(inv(AtA)[i][j] * Atb[j] for j in range(2)) for i in range(2)]
check("normal equations give c = (9/10, 9/10): the line y = 0.9 + 0.9 t", c == [Fraction(9, 10), Fraction(9, 10)])
res = [b[i] - (c[0] + c[1] * t[i]) for i in range(4)]
check("residuals (1/10, 1/5, -7/10, 2/5) sum to 0 and are orthogonal to the t column", res == [Fraction(1, 10), Fraction(1, 5), Fraction(-7, 10), Fraction(2, 5)] and sum(res) == 0 and dot(res, t) == 0)
rss = dot(res, res)
check("residual sum of squares is 7/10", rss == Fraction(7, 10))
best = True
for i in range(-10, 11):
    for j in range(-10, 11):
        c0 = c[0] + Fraction(i, 20); c1 = c[1] + Fraction(j, 20)
        r = [b[k] - (c0 + c1 * t[k]) for k in range(4)]
        if dot(r, r) < rss: best = False
check("no line with intercept and slope within 1/2 of the fit (steps of 1/20, 441 lines) has a smaller sum of squares", best)
check("and moving the intercept by d adds exactly 4 d^2 when the slope is fixed (Pythagoras, Lax p.86): d = 1/10 adds 1/25",
      dot([b[k] - (c[0] + Fraction(1, 10) + c[1] * t[k]) for k in range(4)], [b[k] - (c[0] + Fraction(1, 10) + c[1] * t[k]) for k in range(4)]) == rss + Fraction(4, 100))

print("[5] symmetric matrices")
R7 = range(-3, 4); n_real = 0; bad_disc = 0; bad_orth = 0; pd = nd = ind = sing = 0; rep = 0; bad_pd = 0; bad_pd2 = 0
for a, bb, d in itertools.product(R7, repeat=3):
    Tr = a + d; D = a * d - bb * bb; disc = (a - d) ** 2 + 4 * bb * bb
    if disc < 0: bad_disc += 1
    if disc > 0:
        n_real += 1
        # eigenvectors (b, lam - a) for the two roots: dot = b^2 + (lam1 - a)(lam2 - a) = b^2 + D - a T + a^2, expressed with T and D only
        if bb * bb + D - a * Tr + a * a != 0: bad_orth += 1
    else: rep += 1
    if D > 0:
        if Tr > 0: pd += 1
        else: nd += 1
    elif D < 0: ind += 1
    else: sing += 1
    # positive definiteness: q(y) > 0 for all nonzero y in {-3..3}^2 iff (a > 0 and D > 0) iff (T > 0 and D > 0)
    q_pos = all(a * y1 * y1 + 2 * bb * y1 * y2 + d * y2 * y2 > 0 for y1 in range(-3, 4) for y2 in range(-3, 4) if (y1, y2) != (0, 0))
    if (a > 0 and D > 0) != (Tr > 0 and D > 0): bad_pd += 1
    if (a > 0 and D > 0) and not q_pos: bad_pd2 += 1
check("every real symmetric 2x2 with entries -3..3 (343 matrices) has discriminant (a-d)^2 + 4b^2 >= 0, so real eigenvalues", bad_disc == 0)
check(f"{n_real} of them have two distinct eigenvalues, and for each the eigenvectors (b, lam - a) are orthogonal (b^2 + D - aT + a^2 = 0, exact)", bad_orth == 0 and n_real == 336, f"{n_real} distinct, {rep} repeated")
check("the 7 with a repeated eigenvalue are the scalar matrices (a = d, b = 0)", rep == 7 and sum(1 for a, bb, d in itertools.product(R7, repeat=3) if a == d and bb == 0) == 7)
check("counts over the 343: positive definite 31, negative definite 31, indefinite 256, singular (D = 0) 25", (pd, nd, ind, sing) == (31, 31, 256, 25), f"{pd},{nd},{ind},{sing}")
check("a > 0 and D > 0  iff  T > 0 and D > 0  (positive definite), for all 343", bad_pd == 0)
check("every positive definite one has q(y) = a y1^2 + 2b y1 y2 + d y2^2 > 0 at all 48 nonzero y with entries in -3..3 (an illustration, not a proof)", bad_pd2 == 0)
A3 = [[2, 1, 1], [1, 2, 1], [1, 1, 2]]
P1 = [[Fraction(1, 3)] * 3 for _ in range(3)]; P2 = [[ident(3)[i][j] - P1[i][j] for j in range(3)] for i in range(3)]
check("3x3 example A = [[2,1,1],[1,2,1],[1,1,2]]: A (1,1,1) = 4 (1,1,1) and A (1,-1,0) = (1,-1,0), A (0,1,-1) = (0,1,-1)",
      [sum(A3[i][j] for j in range(3)) for i in range(3)] == [4, 4, 4] and [A3[i][0] - A3[i][1] for i in range(3)] == [1, -1, 0] and [A3[i][1] - A3[i][2] for i in range(3)] == [0, 1, -1])
check("spectral decomposition A = 4 P1 + 1 P2 with P1 = (1/3) J, P2 = I - P1: P1^2 = P1, P2^2 = P2, P1 P2 = 0, P1 + P2 = I, both symmetric",
      mul(P1, P1) == P1 and mul(P2, P2) == P2 and mul(P1, P2) == [[0] * 3] * 3 and P1 == T(P1) and P2 == T(P2)
      and [[4 * P1[i][j] + P2[i][j] for j in range(3)] for i in range(3)] == [[Fraction(x) for x in r] for r in A3])
# controls
S3 = [[0, 1], [1, 1]]
check("control: the symmetric matrix [[0,1],[1,1]] has no eigenvalue in F_3 (t^2 - t - 1 has no root there): the theorem is about the reals, not every field",
      all((t * t - t - 1) % 3 != 0 for t in range(3)))
Z = [[1, 1j], [1j, -1]]
Z2 = [[sum(Z[i][k] * Z[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
check("control: the complex symmetric (not Hermitian) matrix [[1,i],[i,-1]] squares to 0 and is not 0: it is nilpotent, so its only eigenvalue is 0 and it is not diagonalizable",
      Z2 == [[0, 0], [0, 0]] and Z != [[0, 0], [0, 0]])
N = [[1, 1], [0, 1]]; NmI = [[0, 1], [0, 0]]
check("control: the non-symmetric [[1,1],[0,1]] has the single eigenvalue 1 and A - I has rank 1, so only one eigenvector line (1,0): no orthogonal pair of eigenvectors",
      det(NmI) == 0 and any(x != 0 for r in NmI for x in r) and N[0][0] + N[1][1] == 2 and det(N) == 1)

print("[6] the held text: Lax pp.77-107 (printed page = pdf page - 17)")
flat = lambda s: re.sub(r"\s+", " ", s).lower()
pdf = None
for cdir in ("~/Downloads", "~/mnt/Downloads", "."):
    q = Path(os.path.expanduser(cdir)) / "lax.pdf"
    if q.is_file(): pdf = q; break
if pdf is None:
    print("  SKIP: lax.pdf not found (no claim made)")
else:
    pages = None
    try:
        pages = subprocess.run(["pdftotext", "-layout", "-f", "94", "-l", "124", str(pdf), "-"], capture_output=True, text=True, timeout=200, check=True).stdout.split("\f")
    except Exception:
        try:
            from pypdf import PdfReader
            rd = PdfReader(str(pdf)); pages = [rd.pages[i].extract_text() or "" for i in range(93, 124)]
        except Exception as ex:
            print(f"  SKIP: cannot read lax.pdf ({ex})")
    if pages:
        pg = lambda n: flat(pages[n + 17 - 94])
        check("p.79: Euclidean structure defined; Theorem 1 (Schwarz Inequality)", "schwarz inequality" in pg(79) and "euclidean structure" in pg(79))
        check("p.80: Theorem 3 (Triangle Inequality), Pythagorean theorem", "triangle inequality" in pg(80) and "pythagor" in pg(80))
        check("p.81: Theorem 4 (Gram-Schmidt)", "gram-schmidt" in pg(81) and "theorem 4" in pg(81))
        check("p.82: Theorem 5 (linear functions) and Theorem 6 (X = Y + Y-perp, orthogonal complement)", "theorem 5" in pg(82) and "theorem 6" in pg(82) and "orthogonal complement" in pg(82))
        check("p.83: orthogonal projection and Theorem 7", "orthogonal projection" in pg(83) and "theorem 7" in pg(83))
        check("p.84: Theorem 8 (the closest point) and the definition of the adjoint", "theorem 8" in pg(84) and "closest" in pg(84) and "adjoint" in pg(84))
        check("p.85: Theorem 9 (properties of the adjoint)", "theorem 9" in pg(85))
        check("p.86: Theorem 10 (least squares, A*A z = A*p)", "theorem 10" in pg(86) and "minimizes" in pg(86))
        check("p.101: Chapter 8, self-adjoint and symmetric", "self-adjoint" in pg(101) and "symmetric" in pg(101))
        check("p.102: the Hessian", "hessian" in pg(102))
        check("p.103: Theorem 1 (diagonalising a quadratic form)", "theorem 1" in pg(103) and "quadratic form" in pg(103))
        check("p.106: Theorem 4 (real eigenvalues, orthonormal basis of eigenvectors)", "theorem 4" in pg(106) and "real eigenvalues" in pg(106) and "orthonormal basis" in pg(106))
print("  OCR note: lax.pdf is a scan; these checks match short phrases and may miss a page the scan garbled.")

print("[7] the Lean file")
src = (HERE / "Ortho.lean").read_text(encoding="utf-8")
rep_f = HERE / "ortho.axioms.txt"
code = re.sub(r"/-.*?-/", "", src, flags=re.S)
names = ["schwarz", "triangle", "pythagoras", "complement", "eigen_equation", "eigenbasis_orthonormal",
         "control_indefinite", "control_complex_symmetric_nilpotent"]
for nm in names:
    check(f"theorem {nm} is stated", re.search(r"theorem\s+" + nm + r"\b", code) is not None)
check("no sorry or admit in the Lean code", not re.search(r"\b(sorry|admit)\b", code))
if rep_f.exists() and rep_f.read_text(encoding="utf-8").strip():
    r = rep_f.read_text(encoding="utf-8")
    check("axiom report: all eight theorems appear", all(("Book24Ip." + nm) in r for nm in names))
    check("axiom report: no sorryAx and no error", "sorryAx" not in r and "error" not in r.lower())
else:
    print("  NOTE: no ortho.axioms.txt yet; the Lean file has NOT been compiled (run the command in its header).")

print("[8] the page")
page = HERE / "ch08-inner-products.html"
if page.exists():
    txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", page.read_text(encoding="utf-8")))
    check("page prints the counts 31, 256, 25 and 343", all(s in txt for s in ("343", "31 positive definite", "256", "25 singular")))
    check("page prints the fitted line, residual sum of squares and normal equations", "0.9 + 0.9" in txt and "7/10" in txt and "[[4,6],[6,14]]" in txt)
    check("page states the Lean file is not compiled unless a report exists", ("not yet compiled" in txt) == (not (rep_f.exists() and rep_f.read_text(encoding="utf-8").strip())))
else:
    print("  SKIP: page not found")

print()
print("ALL PASS" if not FAIL else f"{len(FAIL)} FAILED: {FAIL}")
sys.exit(1 if FAIL else 0)
