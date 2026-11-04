#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book24/ch07-verify.py -- every check behind book24/ch07-eigenvalues.html. Run first.

    python3 book24/ch07-verify.py

Checks over finite fields are exhaustive within the stated bounds; the rest use exact rational arithmetic or
exact integers. Nothing here proves a theorem for all fields; the proofs are on the page.

  [1] Lax's Example 1, A = [[3,2],[1,4]]: characteristic polynomial a^2 - 7a + 10, eigenvalues 2 and 5,
      eigenvectors, A = P D P^-1 exactly, A^10 = P D^10 P^-1 exactly, A^1024 has 716 digits (Lax: "> 10^700")
  [2] the characteristic polynomial: a is an eigenvalue exactly when det(aI - A) = 0 (every 2x2 over F_3, F_5,
      every 3x3 over F_2); the coefficients of det(tI - A) for 200 random integer 3x3 and 200 random 4x4 matrices:
      monic, t^(n-1) coefficient = -trace, constant term = (-1)^n det
  [3] eigenvectors of distinct eigenvalues are independent: every 2x2 over F_5 and every 3x3 over F_3; the
      Fibonacci example in exact arithmetic over Q(sqrt 5)
  [4] the 2x2 classification by the discriminant (a-d)^2 + 4bc over the 2401 integer matrices with entries in
      -3..3; repeated eigenvalue and not scalar means one independent eigenvector; the rotation control
  [5] polynomials in A: Cayley-Hamilton (every 2x2 with entries -3..3, 200 random 3x3), the inverse formula,
      the spectral mapping example; controls
  [6] the held text: Lax, Linear Algebra and Its Applications, 2nd ed., Chapter 6, pp.59-68
      (printed page = pdf page - 17)
  [7] the Lean file: the seven statements are present, none uses sorry, and the axiom report (if it exists yet)
      shows no sorryAx
  [8] the page: the counts and figures printed on the page equal the ones computed here
"""
import itertools, os, random, re, subprocess, sys
from fractions import Fraction
from pathlib import Path

FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  [{detail}]" if detail else ""))
    if not ok: FAIL.append(label)

HERE = Path(__file__).resolve().parent

# ---- tools ---------------------------------------------------------------------------------------
def mul(A, B, p=None):
    n, m, q = len(A), len(B), len(B[0])
    R = [[sum(A[i][k] * B[k][j] for k in range(m)) for j in range(q)] for i in range(n)]
    return [[x % p for x in r] for r in R] if p else R
def ident(n): return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
def madd(A, B): return [[x + y for x, y in zip(r, s)] for r, s in zip(A, B)]
def mscale(c, A): return [[c * x for x in r] for r in A]
def tr(A): return sum(A[i][i] for i in range(len(A)))
def minor(A, i, j): return [r[:j] + r[j + 1:] for k, r in enumerate(A) if k != i]
def det(A):
    n = len(A)
    if n == 1: return A[0][0]
    return sum((-1) ** j * A[0][j] * det(minor(A, 0, j)) for j in range(n))
def detmod(A, p): return det(A) % p
def mpow(A, e):
    R = ident(len(A))
    B = [r[:] for r in A]
    while e:
        if e & 1: R = mul(R, B)
        B = mul(B, B); e >>= 1
    return R
def charpoly(A):
    """coefficients c[0..n] of det(tI - A) (c[n] = 1), exact, by interpolation at t = 0..n."""
    n = len(A)
    xs = list(range(n + 1))
    ys = [det([[(t if i == j else 0) - A[i][j] for j in range(n)] for i in range(n)]) for t in xs]
    # solve Vandermonde exactly (Lagrange to coefficients)
    coef = [Fraction(0)] * (n + 1)
    for i, xi in enumerate(xs):
        num = [Fraction(1)]
        den = Fraction(1)
        for j, xj in enumerate(xs):
            if j == i: continue
            num = [Fraction(0)] + num
            for k in range(len(num) - 1): num[k] -= xj * num[k + 1]
            den *= (xi - xj)
        for k in range(len(num)): coef[k] += ys[i] * num[k] / den
    return coef
def polyat(c, A):
    """sum c[k] A^k as a matrix"""
    n = len(A); R = [[Fraction(0)] * n for _ in range(n)]; P = ident(n)
    for k in range(len(c)):
        R = madd(R, mscale(c[k], P)); P = mul(P, A)
    return R
def allmats(p, n):
    for t in itertools.product(range(p), repeat=n * n):
        yield [list(t[i * n:(i + 1) * n]) for i in range(n)]
def matvec(A, v, p): return tuple(sum(a * x for a, x in zip(r, v)) % p for r in A)
def eigvecs(A, a, p):
    n = len(A)
    return [v for v in itertools.product(range(p), repeat=n)
            if any(v) and matvec(A, v, p) == tuple(a * x % p for x in v)]
def rank_q(A):
    A = [[Fraction(x) for x in r] for r in A]; rk = 0; rows, cols = len(A), len(A[0])
    for c in range(cols):
        pv = next((r for r in range(rk, rows) if A[r][c] != 0), None)
        if pv is None: continue
        A[rk], A[pv] = A[pv], A[rk]
        A[rk] = [x / A[rk][c] for x in A[rk]]
        for r in range(rows):
            if r != rk and A[r][c] != 0:
                f = A[r][c]; A[r] = [x - f * y for x, y in zip(A[r], A[rk])]
        rk += 1
    return rk
def inv_q(P):
    n = len(P); M = [[Fraction(x) for x in P[i]] + [Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    for c in range(n):
        pv = next(r for r in range(c, n) if M[r][c] != 0); M[c], M[pv] = M[pv], M[c]
        M[c] = [x / M[c][c] for x in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]; M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [r[n:] for r in M]

print("[1] Lax's Example 1")
A1 = [[3, 2], [1, 4]]
cp = charpoly(A1)
check("characteristic polynomial of [[3,2],[1,4]] is a^2 - 7a + 10", cp == [10, -7, 1], str(cp))
check("a = 2 and a = 5 are roots, and nothing else in -50..50", [a for a in range(-50, 51) if a * a - 7 * a + 10 == 0] == [2, 5])
h1, h2 = (2, -1), (1, 1)
check("A (2,-1) = 2 (2,-1)", [sum(A1[i][j] * h1[j] for j in range(2)) for i in range(2)] == [2 * x for x in h1])
check("A (1,1) = 5 (1,1)", [sum(A1[i][j] * h2[j] for j in range(2)) for i in range(2)] == [5 * x for x in h2])
P = [[2, 1], [-1, 1]]; D = [[2, 0], [0, 5]]
check("det P = 3, so the two eigenvectors are independent", det(P) == 3)
Pi = inv_q(P)
check("A = P D P^-1 exactly", mul(mul(P, D), Pi) == [[Fraction(x) for x in r] for r in A1])
check("A^10 = P D^10 P^-1 exactly", mul(mul(P, mpow(D, 10)), Pi) == [[Fraction(x) for x in r] for r in mpow(A1, 10)])
big = mpow(A1, 1024)
check("A^1024 has 716 digits in every entry (Lax: 'greater than 10^700')", all(len(str(x)) == 716 for r in big for x in r))
check("trace 7 = 2 + 5 and det 10 = 2 x 5", tr(A1) == 7 and det(A1) == 10)

print("[2] the characteristic polynomial")
for p, n in ((3, 2), (5, 2), (2, 3)):
    mats = list(allmats(p, n)); bad = 0
    for A in mats:
        for a in range(p):
            M = [[(a if i == j else 0) - A[i][j] for j in range(n)] for i in range(n)]
            has = len(eigvecs(A, a, p)) > 0
            if has != (detmod(M, p) == 0): bad += 1
    check(f"F_{p}, {n}x{n}: a is an eigenvalue exactly when det(aI - A) = 0, all {len(mats)} matrices, all a", bad == 0, f"{bad} failures")
random.seed(24007)
for n in (3, 4):
    ok = True
    for _ in range(200):
        A = [[random.randint(-4, 4) for _ in range(n)] for _ in range(n)]
        c = charpoly(A)
        if not (c[n] == 1 and c[n - 1] == -tr(A) and c[0] == (-1) ** n * det(A)): ok = False
    check(f"200 random integer {n}x{n}: det(tI - A) is monic, t^{n-1} coefficient = -trace, constant term = (-1)^{n} det", ok)
check("control: a matrix with a zero eigenvalue is singular ([[1,2],[2,4]]: roots 0 and 5, det 0)",
      charpoly([[1, 2], [2, 4]]) == [0, -5, 1] and det([[1, 2], [2, 4]]) == 0)

print("[3] eigenvectors of distinct eigenvalues")
for p, n in ((5, 2), (3, 3)):
    mats = list(allmats(p, n)); bad = 0; withtwo = 0
    for A in mats:
        ev = {a: eigvecs(A, a, p) for a in range(p)}
        vals = [a for a in range(p) if ev[a]]
        if len(vals) >= 2: withtwo += 1
        for k in (2, 3):
            if k > n: continue
            for combo in itertools.combinations(vals, k):
                for vs in itertools.product(*[ev[a][:6] for a in combo]):
                    if k == n and detmod([list(c) for c in zip(*vs)], p) == 0: bad += 1
                    if k < n:  # pairs in 3 dimensions: independent iff not proportional
                        u, v = vs
                        if any(all((c * x - y) % p == 0 for x, y in zip(u, v)) for c in range(1, p)): bad += 1
    check(f"F_{p}, {n}x{n}: eigenvectors of distinct eigenvalues are independent, {len(mats)} matrices ({withtwo} with two or more eigenvalues)", bad == 0, f"{bad} failures")
# Fibonacci in Q(sqrt 5): numbers x + y sqrt5 as pairs of Fractions
def qm(u, v): return (u[0] * v[0] + 5 * u[1] * v[1], u[0] * v[1] + u[1] * v[0])
def qsub(u, v): return (u[0] - v[0], u[1] - v[1])
def qpow(u, e):
    r = (Fraction(1), Fraction(0))
    for _ in range(e): r = qm(r, u)
    return r
phi = (Fraction(1, 2), Fraction(1, 2)); psi = (Fraction(1, 2), Fraction(-1, 2))
F = [0, 1]
for _ in range(80): F.append(F[-1] + F[-2])
check("phi and psi are the roots of a^2 - a - 1 (exact)", qsub(qm(phi, phi), phi) == (1, 0) and qsub(qm(psi, psi), psi) == (1, 0))
ok = True
for k in range(0, 61):
    d = qsub(qpow(phi, k), qpow(psi, k))   # = F_k sqrt5, i.e. (0, F_k)
    if d != (0, Fraction(F[k])): ok = False
check("Binet: phi^n - psi^n = F_n sqrt 5 exactly, n = 0..60", ok)
A2 = [[1, 1], [1, 0]]
check("[[1,1],[1,0]]^n = [[F_{n+1},F_n],[F_n,F_{n-1}]], n = 1..60", all(mpow(A2, k) == [[F[k + 1], F[k]], [F[k], F[k - 1]]] for k in range(1, 61)))
from decimal import Decimal, getcontext
getcontext().prec = 60
s5 = Decimal(5).sqrt(); ph = (1 + s5) / 2
check("F_n is the integer nearest phi^n / sqrt 5 for n = 0..60 (error below 1/2; bound 1/sqrt 5 < 1/2 because 1/5 < 1/4)",
      all(abs(Decimal(F[k]) - ph ** k / s5) < Decimal("0.5") for k in range(61)) and Fraction(1, 5) < Fraction(1, 4))
check("Lax Exercise 1: F_32 = 2178309", F[32] == 2178309)

print("[4] the 2x2 classification")
R7 = range(-3, 4); pos = zero = neg = scal = 0; badrk = 0; badcp = 0
for a, b, c, d in itertools.product(R7, repeat=4):
    disc = (a - d) ** 2 + 4 * b * c
    if charpoly([[a, b], [c, d]]) != [a * d - b * c, -(a + d), 1]: badcp += 1
    if disc > 0: pos += 1
    elif disc < 0: neg += 1
    else:
        zero += 1
        lam = Fraction(a + d, 2)
        M = [[Fraction(a) - lam, Fraction(b)], [Fraction(c), Fraction(d) - lam]]
        r = rank_q(M)
        if b == 0 and c == 0:
            scal += 1
            if r != 0: badrk += 1
        elif r != 1:
            badrk += 1
check("characteristic polynomial of [[a,b],[c,d]] is t^2 - (a+d)t + (ad - bc), all 2401", badcp == 0)
check("counts over entries -3..3: discriminant > 0: 1632, = 0: 127, < 0: 642 (sum 2401)", (pos, zero, neg) == (1632, 127, 642), f"{pos},{zero},{neg}")
check("repeated eigenvalue: 7 scalar matrices, 120 not scalar, and A - lambda I has rank 0 resp. 1 (one independent eigenvector)", scal == 7 and zero - scal == 120 and badrk == 0)
check("rotation [[0,-1],[1,0]]: discriminant -4 < 0, no real eigenvalue", (0 - 0) ** 2 + 4 * (-1) * 1 == -4)
rot = [[0, -1], [1, 0]]
check("control: the rotation has no eigenvector over F_3 (t^2 + 1 has no root there) but has eigenvectors over F_5 (roots 2 and 3)",
      all(not eigvecs(rot, a, 3) for a in range(3)) and sorted(a for a in range(5) if eigvecs(rot, a, 5)) == [2, 3])
check("control: [[1,1],[0,1]] has the double eigenvalue 1 and only the line of (1,0): nullity of A - I is 1",
      charpoly([[1, 1], [0, 1]]) == [1, -2, 1] and rank_q([[0, 1], [0, 0]]) == 1)

print("[5] polynomials in A")
ok = True
for a, b, c, d in itertools.product(R7, repeat=4):
    A = [[a, b], [c, d]]; T = a + d; Dt = a * d - b * c
    Z = madd(madd(mul(A, A), mscale(-T, A)), mscale(Dt, ident(2)))
    if Z != [[0, 0], [0, 0]]: ok = False
check("Cayley-Hamilton for 2x2: A^2 - T A + D I = 0 for all 2401 matrices with entries -3..3", ok)
random.seed(24017); ok = True
for _ in range(200):
    A = [[random.randint(-4, 4) for _ in range(3)] for _ in range(3)]
    Z = polyat(charpoly(A), A)
    if any(x != 0 for r in Z for x in r): ok = False
check("Cayley-Hamilton: p_A(A) = 0 for 200 random integer 3x3 matrices (exact)", ok)
ok = True; cnt = 0
for a, b, c, d in itertools.product(R7, repeat=4):
    A = [[a, b], [c, d]]; Dt = a * d - b * c
    if Dt == 0: continue
    cnt += 1
    Ai = [[Fraction((a + d) * (i == j) - A[i][j], Dt) for j in range(2)] for i in range(2)]
    if mul(A, Ai) != ident(2): ok = False
check(f"inverse from Cayley-Hamilton: A^-1 = (T I - A)/D for the {cnt} matrices with D != 0", ok)
q = lambda M: madd(madd(mul(M, M), mscale(-3, M)), ident(2))
Q = q(A1)
check("spectral mapping, q(x) = x^2 - 3x + 1 on [[3,2],[1,4]]: eigenvalues of q(A) are q(2) = -1 and q(5) = 11 (trace 10, det -11)",
      tr(Q) == 10 and det(Q) == -11 and charpoly(Q) == [-11, -10, 1])
check("q(A) h = q(a) h for the eigenvectors: q(A)(2,-1) = -(2,-1) and q(A)(1,1) = 11 (1,1)",
      [sum(Q[i][j] * h1[j] for j in range(2)) for i in range(2)] == [-x for x in h1] and [sum(Q[i][j] * h2[j] for j in range(2)) for i in range(2)] == [11 * x for x in h2])
Zc = madd(mul(A1, A1), mscale(-7, A1))
check("control: dropping the constant term of the characteristic polynomial leaves A^2 - 7A = -10 I, not 0", Zc == mscale(-10, ident(2)))
check("control: A + A = 2A has characteristic polynomial t^2 - 14t + 40, roots 4 and 10, twice those of A",
      charpoly(madd(A1, A1)) == [40, -14, 1] and [t for t in range(-50, 51) if t * t - 14 * t + 40 == 0] == [4, 10])

print("[6] the held text: Lax pp.59-68 (printed page = pdf page - 17)")
flat = lambda t: re.sub(r"\s+", " ", t).lower()
pdf = None
for c in ("~/Downloads", "~/mnt/Downloads", "."):
    qd = Path(os.path.expanduser(c)) / "lax.pdf"
    if qd.is_file(): pdf = qd; break
if pdf is None:
    print("  SKIP: lax.pdf not found (no claim made)")
else:
    pages = None
    try:
        pages = subprocess.run(["pdftotext", "-layout", "-f", "76", "-l", "85", str(pdf), "-"], capture_output=True, text=True, timeout=200, check=True).stdout.split("\f")
    except Exception:
        try:
            from pypdf import PdfReader
            rd = PdfReader(str(pdf)); pages = [rd.pages[i].extract_text() or "" for i in range(75, 85)]
        except Exception as ex:
            print(f"  SKIP: cannot read lax.pdf ({ex})")
    if pages:
        pg = lambda n: flat(pages[n + 17 - 76])
        check("p.59: Spectral Theory; eigenvector and eigenvalue defined", "spectral theory" in pg(59) and "eigenvector" in pg(59) and "eigenvalue" in pg(59))
        check("p.60: every matrix has at least one eigenvalue; equation (8), det(aI - A) = 0", "at least one eigenvalue" in pg(60) and "det" in pg(60))
        check("p.61: characteristic polynomial named; Example 1 with roots 2 and 5", "characteristic polynomial" in pg(61) and "example i" in pg(61).replace("example 1", "example i") and "10" in pg(61))
        check("p.62-63: the Fibonacci example", "fibonacci" in pg(62))
        check("p.64: Theorem 1 (distinct eigenvalues, independent eigenvectors) and Theorem 2", "theorem 1" in pg(64) and "linearly independent" in pg(64) and "theorem 2" in pg(64))
        check("p.65: Theorem 3, sum of eigenvalues = trace, product = determinant", "theorem 3" in pg(65) and "tr a" in pg(65))
        check("p.66: Theorem 4, the spectral mapping theorem", "spectral mapping theorem" in pg(66) and "theorem 4" in pg(66))
        check("p.67: Theorem 5 (Cayley-Hamilton)", "cayley" in pg(67) and "theorem 5" in pg(67))
        check("p.68: Example 4, the matrix with a double eigenvalue and one eigenvector", "example 4" in pg(68))
print("  OCR note: lax.pdf is a scan; these checks match short phrases and may miss a page the scan garbled.")

print("[7] the Lean file")
src = (HERE / "Eigen.lean").read_text(encoding="utf-8")
rep = HERE / "eigen.axioms.txt"
code = re.sub(r"/-.*?-/", "", src, flags=re.S)
names = ["eigen_iff_det_zero", "power_eigen", "trace_eq_sum_eigenvalues", "det_eq_prod_eigenvalues",
         "cayley_hamilton", "eigenvectors_distinct_independent", "control_rotation_no_real_eigenvalue"]
for nm in names:
    check(f"theorem {nm} is stated", re.search(r"theorem\s+" + nm + r"\b", code) is not None)
check("no sorry or admit in the Lean code", not re.search(r"\b(sorry|admit)\b", code))
if rep.exists() and rep.read_text(encoding="utf-8").strip():
    r = rep.read_text(encoding="utf-8")
    check("axiom report: all seven theorems appear", all(("Book24Ev." + nm) in r for nm in names))
    check("axiom report: no sorryAx and no error", "sorryAx" not in r and "error" not in r.lower())
else:
    print("  NOTE: no eigen.axioms.txt yet; the Lean file has NOT been compiled (run the command in its header).")

print("[8] the page")
page = HERE / "ch07-eigenvalues.html"
if page.exists():
    txt = re.sub(r"<[^>]+>", " ", page.read_text(encoding="utf-8")); txt = re.sub(r"\s+", " ", txt)
    check("page prints the three counts 1,632, 127 and 642", all(s in txt for s in ("1,632", "127", "642")))
    check("page prints 716 digits and F32 = 2,178,309", "716 digits" in txt and "2,178,309" in txt)
    check("page states the Lean file is not compiled unless a report exists", ("not yet compiled" in txt) == (not (rep.exists() and rep.read_text(encoding="utf-8").strip())))
else:
    print("  SKIP: page not found")

print()
print("ALL PASS" if not FAIL else f"{len(FAIL)} FAILED: {FAIL}")
sys.exit(1 if FAIL else 0)
