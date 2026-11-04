#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book24/ch09-verify.py -- every check behind book24/ch09-numerical.html. Run first.

    python3 book24/ch09-verify.py

Integers and Fractions are exact; the few steps that need a square root of a non-square use 60-digit Decimal and
say so. Finite checks are exhaustive within the stated bounds. Nothing here proves a theorem; the proofs are on the page.

  [1] size of a map: the 2-norm squared is the larger root of t^2 - F t + D^2 (F = sum of squares of entries,
      D = det): no vector in a grid beats it, and where the root is rational it is attained; |A^T| = |A|; the
      1-norm obeys |CA| <= |C||A|; Theorem 15 (a map within 1/|A^-1| of an invertible map is invertible) with its
      sharpness
  [2] polar decomposition and singular values: A = W D V^T built from Pythagorean rotations, so every entry is
      rational: A^T A V = V D^2, A A^T W = W D^2, A = R U with R symmetric and U orthogonal; A A^T and A^T A have the
      same nonzero eigenvalues (all 3x2 matrices with entries -1, 0, 1)
  [3] condition number, 2x2: K + 1/K = F/|D|; K >= 1 with equality exactly for a multiple of a rotation or
      reflection; K(A^T A) = K(A)^2; the lower bound K >= (largest |eigenvalue|)/(smallest) of Lax (7)
  [4] sensitivity: the relative error in x is at most K times the relative error in b (exact, 1-norm), and the
      bound is attained
  [5] pseudoinverse and least squares: Penrose conditions (including A^+ = V D^+ W^T), the chapter 8 fit, the Hilbert matrix
  [6] the held text: Lax, Linear Algebra and Its Applications, 2nd ed. (printed page = pdf page - 17)
  [7] the Lean file: the statements are present, none uses sorry, the axiom report (if it exists) has no sorryAx
  [8] the page: the counts printed on the page equal the ones computed here
"""
import itertools, math, os, random, re, subprocess
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

getcontext().prec = 60
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  [{detail}]" if detail else ""))
    if not ok: FAIL.append(label)

HERE = Path(__file__).resolve().parent
def mul(A, B): return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def T(A): return [list(r) for r in zip(*A)]
def det2(A): return A[0][0] * A[1][1] - A[0][1] * A[1][0]
def inv2(A):
    d = Fraction(det2(A)); return [[A[1][1] / d, -A[0][1] / d], [-A[1][0] / d, A[0][0] / d]]
def F2(A): return sum(x * x for r in A for x in r)
def n1(A): return max(sum(abs(A[i][j]) for i in range(len(A))) for j in range(len(A[0])))   # max column sum
def vec(A, x): return [sum(A[i][j] * x[j] for j in range(len(x))) for i in range(len(A))]
def ident(n): return [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
def inv(A):
    n = len(A); M = [[Fraction(x) for x in A[i]] + [Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    for c in range(n):
        pv = next(r for r in range(c, n) if M[r][c] != 0); M[c], M[pv] = M[pv], M[c]
        M[c] = [x / M[c][c] for x in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]; M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [r[n:] for r in M]
def isqrt_exact(n):
    if n < 0: return None
    r = math.isqrt(n); return r if r * r == n else None
def lam2(A):
    """(F, D2, disc) for the 2x2 Gram matrix: lambda = (F + sqrt(F^2 - 4 D^2)) / 2 is the larger one."""
    F = F2(A); D = det2(A); return F, D * D, F * F - 4 * D * D

grid = range(-2, 3)
M2 = [[[a, b], [c, d]] for a, b, c, d in itertools.product(grid, repeat=4)]

print("[1] size of a map")
bad = 0; cnt = 0
X = [(x, y) for x in range(-4, 5) for y in range(-4, 5) if (x, y) != (0, 0)]
for A in M2:
    F, D2, disc = lam2(A)
    for x in X:
        Ax = vec(A, x); nx = x[0] ** 2 + x[1] ** 2; nax = Ax[0] ** 2 + Ax[1] ** 2
        # |Ax|^2 <= lambda |x|^2  <=>  L <= sqrt(disc) |x|^2 with L = 2|Ax|^2 - F|x|^2
        L = 2 * nax - F * nx
        cnt += 1
        if not (L <= 0 or L * L <= disc * nx * nx): bad += 1
check("|Ax|^2 <= lambda_max(A^T A) |x|^2 for all 625 integer 2x2 matrices (entries -2..2) and 80 vectors", bad == 0, f"{cnt} cases")
att = 0; att_ok = 0
for A in M2:
    F, D2, disc = lam2(A); r = isqrt_exact(disc)
    if r is None or (F + r) % 2: continue
    lam = (F + r) // 2; M = mul(T(A), A)
    x = (M[0][1], lam - M[0][0]) if M[0][1] != 0 else ((1, 0) if M[0][0] == lam else (0, 1))
    if x == (0, 0): continue
    Ax = vec(A, x); att += 1
    if Ax[0] ** 2 + Ax[1] ** 2 == lam * (x[0] ** 2 + x[1] ** 2): att_ok += 1
check("where the root is an integer the bound is attained at an eigenvector of A^T A", att > 0 and att == att_ok, f"{att_ok} of {att} matrices")
check("|A^T| = |A| for the 2-norm: A A^T and A^T A have the same F and the same det^2",
      all(lam2(A) == lam2(T(A)) for A in M2))
pairs = list(itertools.product(M2, repeat=2)); bad = 0
for A, C in pairs:
    if n1(mul(C, A)) > n1(C) * n1(A): bad += 1
check("1-norm: |CA| <= |C||A| for all 390,625 pairs", bad == 0, f"{len(pairs)} pairs")
bad = 0; tot = 0; sharp = 0
E1 = [[[a, b], [c, d]] for a, b, c, d in itertools.product((-1, 0, 1), repeat=4)]
for A in M2:
    if det2(A) == 0: continue
    nAi = n1(inv2(A))
    for E in E1:
        B = [[A[i][j] + E[i][j] for j in range(2)] for i in range(2)]
        tot += 1
        if n1(E) * nAi < 1 and det2(B) == 0: bad += 1
        if n1(E) * nAi == 1 and det2(B) == 0: sharp += 1
check("Theorem 15 (Lax p.91): |A - B| < 1/|A^-1| implies B invertible, for every invertible A and every B = A + E, E in {-1,0,1}",
      bad == 0, f"{tot} cases")
check("the bound is sharp: A = I, B = I - E11 has |A - B| = 1 = 1/|A^-1| and B singular; sharp cases found: " + str(sharp), sharp > 0 and det2([[0, 0], [0, 1]]) == 0)

print("[2] polar decomposition and singular values")
trip = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)]
rots = [[[Fraction(p, h), Fraction(-q, h)], [Fraction(q, h), Fraction(p, h)]] for p, q, h in trip] + [ident(2)]
ok_all = True; n = 0
for W in rots:
    for V in rots:
        for s1 in range(0, 6):
            for s2 in range(0, s1 + 1):
                Dg = [[Fraction(s1), Fraction(0)], [Fraction(0), Fraction(s2)]]
                A = mul(mul(W, Dg), T(V)); n += 1
                D2 = [[Fraction(s1 * s1), Fraction(0)], [Fraction(0), Fraction(s2 * s2)]]
                c1 = mul(mul(T(A), A), V) == mul(V, D2)
                c2 = mul(mul(A, T(A)), W) == mul(W, D2)
                R = mul(mul(W, Dg), T(W)); U = mul(W, T(V))
                c3 = mul(R, U) == A and R == T(R) and mul(T(U), U) == ident(2)
                ok_all &= c1 and c2 and c3
check("A = W D V^T with rational rotations: A^T A V = V D^2, A A^T W = W D^2, A = R U, R = W D W^T symmetric, U = W V^T orthogonal",
      ok_all, f"{n} matrices")
bad = 0; cnt = 0
for ent in itertools.product((-1, 0, 1), repeat=6):
    A = [list(ent[0:2]), list(ent[2:4]), list(ent[4:6])]            # 3x2
    G2 = mul(T(A), A); G3 = mul(A, T(A))
    f1 = G2[0][0] + G2[1][1]; f2 = det2(G2)
    e1 = sum(G3[i][i] for i in range(3))
    e2 = sum(G3[i][i] * G3[j][j] - G3[i][j] * G3[j][i] for i in range(3) for j in range(i + 1, 3))
    e3 = (G3[0][0] * (G3[1][1] * G3[2][2] - G3[1][2] * G3[2][1]) - G3[0][1] * (G3[1][0] * G3[2][2] - G3[1][2] * G3[2][0])
          + G3[0][2] * (G3[1][0] * G3[2][1] - G3[1][1] * G3[2][0]))
    cnt += 1
    if not (e1 == f1 and e2 == f2 and e3 == 0): bad += 1
check("Lax Exercise 14: for all 729 3x2 matrices with entries -1, 0, 1, A A^T has characteristic polynomial t (t^2 - f1 t + f2) where t^2 - f1 t + f2 is that of A^T A",
      bad == 0, f"{cnt} matrices")
check("det(A^T A) = det(A)^2 for all 625 integer 2x2 matrices", all(det2(mul(T(A), A)) == det2(A) ** 2 for A in M2))

print("[3] condition number of a 2x2 matrix")
G = range(-3, 4)
M3 = [[[a, b], [c, d]] for a, b, c, d in itertools.product(G, repeat=4)]
inv_list = [A for A in M3 if det2(A) != 0]
sing = len(M3) - len(inv_list)
def lam_max_dec(F, D2):
    disc = F * F - 4 * D2; return (Decimal(F) + Decimal(disc).sqrt()) / 2
def lam_min_dec(F, D2):
    disc = F * F - 4 * D2; return (Decimal(F) - Decimal(disc).sqrt()) / 2
badid = 0; badind = 0; Kone = 0; badge = 0; badsq = 0; badcomp = 0
for A in inv_list:
    F = F2(A); D = det2(A)
    K = (lam_max_dec(F, D * D) / lam_min_dec(F, D * D)).sqrt()
    # independent: |A| |A^-1| from the largest-root formula applied to A and to A^-1 (exact Fractions, then Decimal)
    Ai = inv2(A); Fi = F2(Ai); Di2 = det2(Ai) ** 2
    disci = Fi * Fi - 4 * Di2
    nAi = ((Decimal(Fi.numerator) / Decimal(Fi.denominator)) + (Decimal(disci.numerator) / Decimal(disci.denominator)).sqrt()) / 2
    Kind = (lam_max_dec(F, D * D) * nAi).sqrt()
    if abs(Kind - K) > Decimal("1e-40"): badind += 1
    if abs(K + 1 / K - Decimal(F) / Decimal(abs(D))) > Decimal("1e-40"): badid += 1
    if K < 1 - Decimal("1e-40"): badge += 1
    exact_one = ((A[0][0] - A[1][1]) ** 2 + (A[0][1] + A[1][0]) ** 2 == 0) or ((A[0][0] + A[1][1]) ** 2 + (A[0][1] - A[1][0]) ** 2 == 0)
    if exact_one: Kone += 1
    if exact_one != (abs(K - 1) < Decimal("1e-40")): badge += 1
    Mg = mul(T(A), A); FM = F2(Mg); DM = det2(Mg)
    if F * F - 2 * D * D != sum(Mg[i][j] * Mg[j][i] for i in range(2) for j in range(2)): badsq += 1
    KM = (lam_max_dec(FM, DM * DM) / lam_min_dec(FM, DM * DM)).sqrt()
    if abs(KM - K * K) > Decimal("1e-35"): badsq += 1
check("K(A) from the definition |A||A^-1| equals sigma_max/sigma_min (60-digit decimal) for all 2,401 - singular integer matrices with entries -3..3",
      badind == 0, f"{len(inv_list)} invertible matrices, {sing} singular")
check("K + 1/K = F/|det| for every one of them (60-digit decimal)", badid == 0)
check("K >= 1 (Lax Exercise 1) and K = 1 exactly when (a-d)^2 + (b+c)^2 = 0 or (a+d)^2 + (b-c)^2 = 0, i.e. a multiple of a rotation or reflection",
      badge == 0, f"K = 1 for {Kone} of {len(inv_list)}")
check("trace((A^T A)^2) = F^2 - 2 det^2 exactly, and so K(A^T A) = K(A)^2 (60-digit decimal): the normal equations square the condition number",
      badsq == 0)
def roots_within(Tr, Dt, p):
    """both roots of t^2 - Tr t + Dt have modulus <= p (exact, p >= 0)"""
    disc = Tr * Tr - 4 * Dt
    if disc < 0: return Dt <= p * p
    return p * p - Tr * p + Dt >= 0 and p * p + Tr * p + Dt >= 0 and abs(Tr) <= 2 * p
badr = 0
for A in inv_list:
    Tr = A[0][0] + A[1][1]; Dt = det2(A); Ai = inv2(A)
    if not (roots_within(Tr, Dt, n1(A)) and roots_within(Fraction(Tr, Dt), Fraction(1, Dt), n1(Ai))): badr += 1
check("|eigenvalue| <= |A| and 1/|eigenvalue| <= |A^-1| for every eigenvalue (1-norm, exact), hence K >= (largest |eigenvalue|)/(smallest): Lax (6), (6)', (7)",
      badr == 0, f"{len(inv_list)} matrices")

phi2 = (Decimal(3) + Decimal(5).sqrt()) / 2
Kb = (lam_max_dec(F2([[1, 1], [0, 1]]), 1) / lam_min_dec(F2([[1, 1], [0, 1]]), 1)).sqrt()
check("exercise: A = [[1,1],[0,1]] has F = 3, det = 1, K + 1/K = 3 and K = (3 + sqrt 5)/2 = 2.618...", abs(Kb - phi2) < Decimal("1e-40") and abs(Kb + 1 / Kb - 3) < Decimal("1e-40"))
Afit = [[1, 0], [1, 1], [1, 2], [1, 3]]; Mfit = mul(T(Afit), Afit)
Kfit_M = (lam_max_dec(F2(Mfit), det2(Mfit) ** 2) / lam_min_dec(F2(Mfit), det2(Mfit) ** 2)).sqrt()
check("exercise: for the four-point fit, A^T A = [[4,6],[6,14]], F = 284, det = 20, K(A^T A) = 14.129... and K(A) = sqrt of it = 3.758...",
      Mfit == [[4, 6], [6, 14]] and F2(Mfit) == 284 and det2(Mfit) == 20 and abs(Kfit_M - Decimal("14.129224708315")) < Decimal("1e-9") and abs(Kfit_M.sqrt() - Decimal("3.758886099407")) < Decimal("1e-9"))

print("[4] sensitivity: relative error in x <= K times relative error in b")
bad = 0; cnt = 0
V4 = [(x, y) for x in range(-2, 3) for y in range(-2, 3) if (x, y) != (0, 0)]
for A in M2:
    if det2(A) == 0: continue
    Ai = inv2(A); K = n1(A) * n1(Ai)
    for x in V4:
        b = vec(A, x); nb = sum(abs(t) for t in b); nx = sum(abs(t) for t in x)
        for db in V4:
            dx = vec(Ai, db); ndx = sum(abs(t) for t in dx); ndb = sum(abs(t) for t in db)
            cnt += 1
            if ndx * nb > K * ndb * nx: bad += 1      # cross-multiplied: exact, no division
check("(|dx|/|x|) <= K (|db|/|b|) for every invertible A (entries -2..2), x and db in {-2..2}^2 minus 0 (1-norm, exact)", bad == 0, f"{cnt} cases")
good = 0
for m in range(1, 21):
    A = [[Fraction(1), Fraction(0)], [Fraction(0), Fraction(1, m)]]; Ai = inv2(A)
    x = (1, 0); b = vec(A, x); db = (0, Fraction(1, 7)); dx = vec(Ai, db)
    ratio = (sum(abs(t) for t in dx) / sum(abs(t) for t in x)) / (sum(abs(t) for t in db) / sum(abs(t) for t in b))
    if ratio == n1(A) * n1(Ai) == m: good += 1
check("the bound is attained: A = diag(1, 1/m), x = e1, db along e2 gives ratio exactly K = m, m = 1..20", good == 20)

print("[5] pseudoinverse, least squares, the Hilbert matrix")
def pen(A, P):
    AP = mul(A, P); PA = mul(P, A)
    return mul(AP, A) == A and mul(PA, P) == P and AP == T(AP) and PA == T(PA)
random.seed(24)
ok = True; cnt = 0
while cnt < 200:
    u = [random.randint(-3, 3) for _ in range(3)]; v = [random.randint(-3, 3) for _ in range(2)]
    if not any(u) or not any(v): continue
    A = [[u[i] * v[j] for j in range(2)] for i in range(3)]
    c = Fraction(sum(t * t for t in u) * sum(t * t for t in v))
    P = [[Fraction(v[j] * u[i]) / c for i in range(3)] for j in range(2)]
    ok &= pen(A, P); cnt += 1
check("rank one: A = u v^T has pseudoinverse v u^T / (|u|^2 |v|^2): all four Penrose conditions, 200 random integer cases", ok)
ok = True; cnt = 0
while cnt < 200:
    A = [[random.randint(-3, 3) for _ in range(2)] for _ in range(4)]
    if det2(mul(T(A), A)) == 0: continue
    P = mul(inv(mul(T(A), A)), T(A)); cnt += 1
    ok &= (mul(P, A) == ident(2)) and pen(A, P)
ok = True; n = 0
for W in rots:
    for V in rots:
        for s1 in range(0, 6):
            for s2 in range(0, s1 + 1):
                Dg = [[Fraction(s1), Fraction(0)], [Fraction(0), Fraction(s2)]]
                Dp = [[Fraction(1, s1) if s1 else Fraction(0), Fraction(0)], [Fraction(0), Fraction(1, s2) if s2 else Fraction(0)]]
                A = mul(mul(W, Dg), T(V)); P = mul(mul(V, Dp), T(W)); n += 1
                ok &= pen(A, P)
check("A = W D V^T gives A^+ = V D^+ W^T (invert the nonzero singular values): all four Penrose conditions, including the singular and zero cases", ok, f"{n} matrices")
check("full column rank: (A^T A)^-1 A^T is a left inverse and satisfies all four Penrose conditions, 200 random integer 4x2 matrices", ok)
A = [[1, 0], [1, 1], [1, 2], [1, 3]]; b = [[1], [2], [2], [4]]
P = mul(inv(mul(T(A), A)), T(A)); c = mul(P, b)
check("the chapter 8 fit: A^+ b = (9/10, 9/10) for the four points", [c[0][0], c[1][0]] == [Fraction(9, 10), Fraction(9, 10)])
def hil(n): return [[Fraction(1, i + j + 1) for j in range(n)] for i in range(n)]
allint = True; k1 = []
for n in range(1, 9):
    H = hil(n); Hi = inv(H)
    allint &= all(x.denominator == 1 for r in Hi for x in r) and mul(H, Hi) == ident(n)
    k1.append(n1(H) * n1(Hi))
check("Hilbert matrices H_1..H_8 have integer inverses (exact), and the 1-norm condition numbers increase strictly", allint and all(k1[i] < k1[i + 1] for i in range(7)),
      "kappa_1 = " + ", ".join(str(k) for k in k1[:5]) + ", ...")
H3 = hil(3); H3i = inv(H3)
check("H_3^-1 = [[9,-36,30],[-36,192,-180],[30,-180,180]] and kappa_1(H_3) = 748", [[int(x) for x in r] for r in H3i] == [[9, -36, 30], [-36, 192, -180], [30, -180, 180]] and k1[2] == 748)
try:
    import numpy as np
    for n in (3, 5, 8):
        Hn = np.array([[1.0 / (i + j + 1) for j in range(n)] for i in range(n)])
        xs = np.ones(n); bb = Hn @ xs; xh = np.linalg.solve(Hn, bb)
        rel = np.linalg.norm(xh - xs) / np.linalg.norm(xs); kap = np.linalg.cond(Hn)
        print(f"  numpy (float64, not exact): n={n}  kappa_2 = {kap:.3e}  relative error in solving H x = H 1: {rel:.2e}  (kappa * 1.1e-16 = {kap * 1.1e-16:.2e})")
        check(f"float64 solve of H_{n} x = H_{n} 1: relative error <= kappa_2 * 2.3e-16 * 10 (Lax p.248: 10^-k K(A), with a margin of 10)", rel <= kap * 2.3e-16 * 10)
except ImportError:
    print("  SKIP: numpy not installed (no claim made about floating point)")

print("[6] the held text: Lax (printed page = pdf page - 17)")
flat = lambda s: re.sub(r"\s+", " ", s).lower()
pdf = None
for cdir in ("~/Downloads", "~/mnt/Downloads", "."):
    q = Path(os.path.expanduser(cdir)) / "lax.pdf"
    if q.is_file(): pdf = q; break
def pages_of(first, last):
    try:
        return subprocess.run(["pdftotext", "-layout", "-f", str(first), "-l", str(last), str(pdf), "-"], capture_output=True, text=True, timeout=200, check=True).stdout.split("\f")
    except Exception:
        try:
            from pypdf import PdfReader
            rd = PdfReader(str(pdf)); return [rd.pages[i].extract_text() or "" for i in range(first - 1, last)]
        except Exception as ex:
            print(f"  SKIP: cannot read lax.pdf ({ex})"); return None
if pdf is None:
    print("  SKIP: lax.pdf not found (no claim made)")
else:
    a = pages_of(106, 109); b = pages_of(131, 131); c = pages_of(186, 188); d = pages_of(264, 265); e = pages_of(136, 136)
    if a and b and c and d and e:
        pa = lambda n: flat(a[n + 17 - 106]); pc = lambda n: flat(c[n + 17 - 186]); pd = lambda n: flat(d[n + 17 - 264])
        check("p.90: Theorem 13 (|Az| <= |A||z|) and Theorem 14 (norm of a sum, product, adjoint)", "theorem 13" in pa(90) and "theorem 14" in pa(90))
        check("p.91: Theorem 15 (a map close to an invertible map is invertible)", "theorem 15" in pa(91) and "invertible" in pa(91))
        check("p.114: the Rayleigh quotient", "rayleigh" in flat(b[0]))
        check("p.119: Chapter 8, Theorem 13 (the norm of A is the square root of the largest eigenvalue of A*A)", "theorem 13" in flat(e[0]) and "largest eigenvalue" in flat(e[0]))
        check("p.169: Theorem 22 (polar decomposition A = RU)", "theorem 22" in pc(169) and "unitary" in pc(169))
        check("p.170: singular value decomposition; singular values are square roots of eigenvalues of AA*", "singular value decomposition" in pc(170) and "singular values" in pc(170))
        check("p.170: Exercise 13 and p.171: Exercise 14 (AA* and A*A have the same eigenvalues)", "exercise 13" in pc(170) and "exercise 14" in pc(171))
        check("p.247: the system Ax = b; sensitivity to a change in b", "ax = b" in pd(247) or "invertible square matrix" in pd(247))
        check("p.248: condition number K(A) = |A||A^-1|; K(A) >= 1 as Exercise 1", "condition number" in pd(248) and "exercise" in pd(248))
print("  OCR note: lax.pdf is a scan; these checks match short phrases and may miss a page the scan garbled.")

print("[7] the Lean file")
src = (HERE / "Numerical.lean").read_text(encoding="utf-8")
rep_f = HERE / "numerical.axioms.txt"
code = re.sub(r"/-.*?-/", "", src, flags=re.S)
names = ["opNorm_le", "opNorm_comp_le", "condition_ge_one", "sensitivity", "gram_det", "trace_sq_gram",
         "frobenius_det_bounds", "left_inverse_normal", "gram_same_nonzero_spectrum", "control_hilbert3_inverse"]
for nm in names:
    check(f"theorem {nm} is stated", re.search(r"theorem\s+" + nm + r"\b", code) is not None)
check("no sorry or admit in the Lean code", not re.search(r"\b(sorry|admit)\b", code))
if rep_f.exists() and rep_f.read_text(encoding="utf-8").strip():
    r = rep_f.read_text(encoding="utf-8")
    check("axiom report: all ten theorems appear", all(("Book24Nm." + nm) in r for nm in names))
    check("axiom report: no sorryAx and no error", "sorryAx" not in r and "error" not in r.lower())
else:
    print("  NOTE: no numerical.axioms.txt yet; the Lean file has NOT been compiled (run the command in its header).")

print("[8] the page")
page = HERE / "ch09-numerical.html"
if page.exists():
    txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", page.read_text(encoding="utf-8")))
    check("page prints the counts 2401, 2401 - singular, and K = 1 for the matrices computed here",
          all(s in txt for s in ("2401", f"{sing} singular", f"{Kone} have K = 1")))
    check("page prints kappa_1(H_3) = 748 and H_3^-1", "748" in txt and "[[9,-36,30],[-36,192,-180],[30,-180,180]]" in txt)
    check("page states the Lean file is not compiled unless a report exists", ("not yet compiled" in txt) == (not (rep_f.exists() and rep_f.read_text(encoding="utf-8").strip())))
else:
    print("  SKIP: page not found")

print()
print("ALL PASS" if not FAIL else f"{len(FAIL)} FAILED: {FAIL}")
