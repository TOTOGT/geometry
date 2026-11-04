#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book24/ch06-verify.py -- every check behind book24/ch06-matrices-determinants.html. Run first.

    python3 book24/ch06-verify.py

Checks over finite fields are exhaustive within the stated bounds (every matrix, every pair), so a PASS is a
statement about the whole finite family, not a sample. Nothing here proves a theorem for all fields; the proofs
are on the page.

  [1] product = composition: every pair of 2x2 matrices over F_2 and F_3 and of 3x3 over F_2, on every vector
  [2] rank: row rank = column rank for every 2x3, 3x2 (F_2, F_3) and 3x3 (F_2) matrix; rank agrees with the
      size of the range, |range| = p^rank (the link to chapter 5)
  [3] Gaussian elimination in exact rational arithmetic: the worked 3x3 system (one row swap), a zero-pivot
      control, a singular system and an inconsistent one
  [4] determinants: the Leibniz formula equals cofactor expansion (random integer 4x4, fixed seed); det(BA) =
      det A det B for every pair of 2x2 over F_2, F_3, F_5 and 3x3 over F_2; a matrix is invertible exactly
      when det != 0 (brute-force search for an inverse); the number of invertible matrices equals
      prod (p^n - p^i); a row swap changes the sign; determinant is not additive
  [5] Cramer's rule and the cofactor inverse, exact over Q, on the worked example
  [6] trace: tr(AB) = tr(BA) for every pair of 3x3 over F_2; similar matrices share determinant and trace
      (all P, all A, 2x2 over F_3); controls
  [7] the held text: Lax, Linear Algebra and Its Applications, 2nd ed., Chapters 3 (pp.27-28), 4 and 5, pp.32-57
      (printed page = pdf page - 17)
  [8] the Lean file: the nine statements are present, none uses sorry, and the axiom report (if it exists yet)
      shows no sorryAx
"""
import itertools, os, random, re, subprocess, sys
from fractions import Fraction
from pathlib import Path

FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  [{detail}]" if detail else ""))
    if not ok: FAIL.append(label)

# ---- matrix tools --------------------------------------------------------------------------------
def mul(A,B,p=None):
    n,m,q=len(A),len(B),len(B[0])
    R=[[sum(A[i][k]*B[k][j] for k in range(m)) for j in range(q)] for i in range(n)]
    return [[x%p for x in r] for r in R] if p else R
def sign(perm):
    s=1;perm=list(perm)
    for i in range(len(perm)):
        while perm[i]!=i:
            j=perm[i];perm[i],perm[j]=perm[j],perm[i];s=-s
    return s
def det_leibniz(A,p=None):
    n=len(A);t=0
    for pm in itertools.permutations(range(n)):
        pr=sign(pm)
        for i in range(n): pr*=A[i][pm[i]]
        t+=pr
    return t%p if p else t
def rref_rank(A,p):
    A=[r[:] for r in A];rk=0;rows,cols=len(A),len(A[0])
    for c in range(cols):
        pv=next((r for r in range(rk,rows) if A[r][c]%p),None)
        if pv is None: continue
        A[rk],A[pv]=A[pv],A[rk];inv=pow(A[rk][c],-1,p)
        A[rk]=[x*inv%p for x in A[rk]]
        for r in range(rows):
            if r!=rk and A[r][c]%p:
                f=A[r][c];A[r]=[(x-f*y)%p for x,y in zip(A[r],A[rk])]
        rk+=1
    return rk
def gauss_solve(A,b):
    n=len(A);M=[[Fraction(x) for x in A[i]]+[Fraction(b[i])] for i in range(n)];swaps=0
    for c in range(n):
        pv=next((r for r in range(c,n) if M[r][c]!=0),None)
        if pv is None: return None
        if pv!=c: M[c],M[pv]=M[pv],M[c];swaps+=1
        M[c]=[x/M[c][c] for x in M[c]]
        for r in range(n):
            if r!=c and M[r][c]!=0:
                f=M[r][c];M[r]=[x-f*y for x,y in zip(M[r],M[c])]
    return [M[i][n] for i in range(n)],swaps
def minor(A,i,j): return [r[:j]+r[j+1:] for k,r in enumerate(A) if k!=i]
def det_cof(A):
    n=len(A)
    if n==1: return A[0][0]
    return sum((-1)**j*A[0][j]*det_cof(minor(A,0,j)) for j in range(n))
def allmats(p,n,m):
    for t in itertools.product(range(p),repeat=n*m):
        yield [list(t[i*m:(i+1)*m]) for i in range(n)]

HERE = Path(__file__).resolve().parent
def matvec(A, v, p): return tuple(sum(a * x for a, x in zip(r, v)) % p for r in A)
def ident(n): return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
def tr(A): return sum(A[i][i] for i in range(len(A)))

print("[1] product = composition")
for p, n in ((2, 2), (3, 2), (2, 3)):
    mats = list(allmats(p, n, n)); vecs = list(itertools.product(range(p), repeat=n)); bad = 0
    for A in mats:
        for B in mats:
            AB = mul(A, B, p)
            for v in vecs:
                if matvec(AB, v, p) != matvec(A, matvec(B, v, p), p): bad += 1
    check(f"F_{p}, {n}x{n}: (AB)v = A(Bv) for all {len(mats)**2} pairs and all {len(vecs)} vectors", bad == 0, f"{bad} failures")
A0, B0 = [[1, 1], [0, 1]], [[1, 0], [1, 1]]
check("control: AB != BA over F_3 (the product is not commutative)", mul(A0, B0, 3) != mul(B0, A0, 3), f"{mul(A0,B0,3)} vs {mul(B0,A0,3)}")

print("[2] rank")
def range_size(A, p):
    n, m = len(A), len(A[0]); return len({matvec(A, v, p) for v in itertools.product(range(p), repeat=m)})
for p, n, m in ((2, 2, 3), (2, 3, 2), (3, 2, 3), (3, 3, 2), (2, 3, 3)):
    cnt = 0; bad = 0; bad2 = 0
    for A in allmats(p, n, m):
        At = [list(c) for c in zip(*A)]; r = rref_rank(A, p); cnt += 1
        if r != rref_rank(At, p): bad += 1
        if range_size(A, p) != p ** r: bad2 += 1
    check(f"F_{p}, {n}x{m}: row rank = column rank and |range| = p^rank for all {cnt} matrices", bad == 0 and bad2 == 0, f"{bad}, {bad2} failures")
check("control: over F_2 the all-ones 2x2 has rank 1, the identity rank 2", rref_rank([[1, 1], [1, 1]], 2) == 1 and rref_rank(ident(2), 2) == 2)

print("[3] Gaussian elimination, exact")
A1 = [[0, 2, 1], [1, 1, 1], [2, 1, 3]]; b1 = [4, 6, 11]
x, sw = gauss_solve(A1, b1)
check("worked system: x = (11/3, 5/3, 2/3) with one row swap", x == [Fraction(11, 3), Fraction(5, 3), Fraction(2, 3)] and sw == 1, f"{x}, swaps {sw}")
check("worked system: A x = b by substitution", [sum(Fraction(A1[i][j]) * x[j] for j in range(3)) for i in range(3)] == [Fraction(v) for v in b1])
x2, _ = gauss_solve(A1, [5, 6, 13])
check("second right-hand side (5, 6, 13): x = (7/3, 4/3, 7/3), same elimination", x2 == [Fraction(7, 3), Fraction(4, 3), Fraction(7, 3)])
check("control: [[0,1],[1,1]] has a zero first pivot and still solves, by one swap", gauss_solve([[0, 1], [1, 1]], [1, 2]) == ([Fraction(1), Fraction(1)], 1))
check("control: [[1,2],[2,4]] is singular (elimination reports no unique solution)", gauss_solve([[1, 2], [2, 4]], [1, 2]) is None)
check("rank of [[1,2],[2,4]] is 1: [1,2] is consistent and [1,3] is not (augmented rank 2)",
      rref_rank([[1, 2], [2, 4]], 10007) == 1 and rref_rank([[1, 2, 1], [2, 4, 2]], 10007) == 1 and rref_rank([[1, 2, 1], [2, 4, 3]], 10007) == 2)

print("[4] determinants")
random.seed(24006)
ok = True
for _ in range(200):
    M = [[random.randint(-5, 5) for _ in range(4)] for _ in range(4)]
    if det_leibniz(M) != det_cof(M): ok = False
check("Leibniz formula = cofactor expansion on 200 random integer 4x4 matrices", ok)
check("det of the worked matrix is -3", det_leibniz(A1) == -3 and det_cof(A1) == -3)
for p, n in ((2, 2), (3, 2), (5, 2), (2, 3)):
    mats = list(allmats(p, n, n)); D = {tuple(map(tuple, M)): det_leibniz(M, p) for M in mats}; bad = 0
    for A in mats:
        dA = D[tuple(map(tuple, A))]
        for B in mats:
            if D[tuple(map(tuple, mul(B, A, p)))] != dA * D[tuple(map(tuple, B))] % p: bad += 1
    check(f"F_{p}, {n}x{n}: det(BA) = det A det B for all {len(mats)**2} pairs", bad == 0, f"{bad} failures")
for p, n in ((2, 2), (3, 2), (2, 3)):
    mats = list(allmats(p, n, n)); I = ident(n)
    invertible = {tuple(map(tuple, A)) for A in mats for B in mats if mul(A, B, p) == I}
    nz = {tuple(map(tuple, A)) for A in mats if det_leibniz(A, p) != 0}
    check(f"F_{p}, {n}x{n}: has an inverse exactly when det != 0 ({len(nz)} such matrices)", invertible == nz)
    want = 1
    for i in range(n): want *= p ** n - p ** i
    check(f"F_{p}, {n}x{n}: number of invertible matrices = prod (p^n - p^i) = {want}", len(nz) == want, str(len(nz)))
want33 = (27 - 1) * (27 - 3) * (27 - 9)
n33 = sum(1 for A in allmats(3, 3, 3) if det_leibniz(A, 3) != 0)
check(f"F_3, 3x3: number of matrices with det != 0 = {want33}", n33 == want33, str(n33))
S = [[1, 2], [3, 4]]; S2 = [S[1], S[0]]
check("a row swap changes the sign of det (over Z, [[1,2],[3,4]] has det -2)", det_leibniz(S) == -2 and det_leibniz(S2) == 2)
I2 = ident(2); twoI = [[2, 0], [0, 2]]
check("control: det is not additive, det(I + I) = 4 but det I + det I = 2", det_leibniz(twoI) == 4 and det_leibniz(I2) * 2 == 2)
check("control: det(AB) != det A + det B in general (A = B = I over Q)", det_leibniz(mul(I2, I2)) != det_leibniz(I2) + det_leibniz(I2))

print("[5] Cramer's rule and the cofactor inverse")
d = det_cof(A1)
cr = [Fraction(det_cof([[b1[i] if c == k else A1[i][c] for c in range(3)] for i in range(3)]), d) for k in range(3)]
check("Cramer: x_k = det(A with column k replaced by b) / det A matches elimination", cr == x, str(cr))
adj = [[(-1) ** (i + j) * det_cof(minor(A1, j, i)) for j in range(3)] for i in range(3)]
check("cofactor inverse: A adj(A) = det A . I, adj(A) = [[2,-5,1],[-1,-2,1],[-1,4,-2]]",
      mul(A1, adj) == [[d if i == j else 0 for j in range(3)] for i in range(3)] and adj == [[2, -5, 1], [-1, -2, 1], [-1, 4, -2]])
Ainv = [[Fraction(adj[i][j], d) for j in range(3)] for i in range(3)]
check("A^-1 = adj(A)/det A, and A^-1 b = x", mul(A1, Ainv) == ident(3) and [sum(Ainv[i][j] * b1[j] for j in range(3)) for i in range(3)] == x)
check("control: Cramer fails to apply when det = 0 (the singular matrix)", det_cof([[1, 2], [2, 4]]) == 0)

print("[6] trace")
mats = list(allmats(2, 3, 3)); bad = 0
for A in mats:
    for B in mats:
        if tr(mul(A, B, 2)) % 2 != tr(mul(B, A, 2)) % 2: bad += 1
check(f"F_2, 3x3: tr(AB) = tr(BA) for all {len(mats)**2} pairs", bad == 0, f"{bad} failures")
p = 3; mats = list(allmats(p, 2, 2)); GL = [P for P in mats if det_leibniz(P, p) != 0]; bad = 0
def inv2(P):
    d_ = pow(det_leibniz(P, p), -1, p); return [[P[1][1] * d_ % p, -P[0][1] * d_ % p], [-P[1][0] * d_ % p, P[0][0] * d_ % p]]
for P in GL:
    Pi = inv2(P)
    assert mul(P, Pi, p) == ident(2)
    for A in mats:
        C = mul(mul(P, A, p), Pi, p)
        if det_leibniz(C, p) != det_leibniz(A, p) or tr(C) % p != tr(A) % p: bad += 1
check(f"F_3, 2x2: P A P^-1 has the same det and trace as A for all {len(GL)} P and all {len(mats)} A", bad == 0, f"{bad} failures")
check("control: tr(AB) != tr A tr B (A = B = I over Z: 2 vs 4)", tr(mul(I2, I2)) == 2 and tr(I2) * tr(I2) == 4)
J = [[1, 1], [0, 1]]
conj_of_I = {tuple(map(tuple, mul(mul(P, ident(2), p), inv2(P), p))) for P in GL}
check("control: det and trace do not determine similarity: I and [[1,1],[0,1]] share det 1 and trace 2 over F_3, yet every conjugate of I is I",
      det_leibniz(I2, p) == det_leibniz(J, p) and tr(I2) % p == tr(J) % p and conj_of_I == {((1, 0), (0, 1))} and tuple(map(tuple, J)) not in conj_of_I)

print("[7] the held text: Lax pp.32-57 (printed page = pdf page - 17)")
flat = lambda t: re.sub(r"\s+", " ", t).lower()
pdf = None
for c in ("~/Downloads", "~/mnt/Downloads", "."):
    q = Path(os.path.expanduser(c)) / "lax.pdf"
    if q.is_file(): pdf = q; break
if pdf is None:
    print("  SKIP: lax.pdf not found (no claim made)")
else:
    pages = None
    try:
        pages = subprocess.run(["pdftotext", "-layout", "-f", "44", "-l", "74", str(pdf), "-"], capture_output=True, text=True, timeout=200, check=True).stdout.split("\f")
    except Exception:
        try:
            from pypdf import PdfReader
            rd = PdfReader(str(pdf)); pages = [rd.pages[i].extract_text() or "" for i in range(43, 74)]
        except Exception as ex:
            print(f"  SKIP: cannot read lax.pdf ({ex})")
    if pages:
        pg = lambda n: flat(pages[n + 17 - 44])
        check("p.27: Theorem 6 (dim of range of T = dim of range of its transpose)", "theorem 6" in pg(27))
        check("p.28: the remark that Theorem 6 is the abstract version of column rank = row rank", "column rank and row rank" in pg(28))
        check("p.32: Chapter 4, Matrices", "chapter 4" in pg(32) and "matrices" in pg(32))
        check("p.35: Rule of matrix multiplication", "rule of matrix multiplication" in pg(35))
        check("p.39: Gaussian elimination", "gauss" in pg(39))
        check("p.44: Chapter 5, Determinant and Trace", "chapter 5" in pg(44) and "determinant and trace" in pg(44))
        check("p.49: Theorem 2, det(BA) = det A det B", "theorem 2" in pg(49) and "det a det b" in pg(49).replace("det(ba) =", ""))
        check("p.51: Corollary 3 (invertible iff det != 0) and the multiplicative property", "corollary 3" in pg(51) and "multiplicative" in pg(51))
        check("p.54: Cramer's rule and Theorem 7 (the inverse by cofactors)", "cramer" in pg(54) and "theorem 7" in pg(54))
        check("p.55: trace and Theorem 8, tr(AB) = tr(BA)", "trace" in pg(55) and "theorem 8" in pg(55))
        check("p.56: Theorem 9, similar matrices have the same determinant and trace", "theorem 9" in pg(56) and "similar matrices" in pg(56))
print("  OCR note: lax.pdf is a scan; these checks match short phrases and may miss a page the scan garbled.")

print("[8] the Lean file")
src = (HERE / "MatricesDet.lean").read_text(encoding="utf-8")
rep = HERE / "matricesdet.axioms.txt"
code = re.sub(r"/-.*?-/", "", src, flags=re.S)
names = ["product_is_composition", "det_product", "invertible_iff_det_ne_zero", "rank_transpose_eq", "cramer_solves",
         "trace_comm", "similar_det", "control_singular", "control_det_not_linear"]
for nm in names:
    check(f"theorem {nm} is stated", re.search(r"theorem\s+" + nm + r"\b", code) is not None)
check("no sorry or admit in the Lean code", not re.search(r"\b(sorry|admit)\b", code))
if rep.exists():
    r = rep.read_text(encoding="utf-8")
    check("axiom report: all nine theorems appear", all(("Book24MD." + nm) in r for nm in names))
    check("axiom report: no sorryAx", "sorryAx" not in r and "error" not in r.lower())
else:
    print("  NOTE: no matricesdet.axioms.txt yet; the Lean file has NOT been compiled (run the command in its header).")

print()
print("ALL PASS" if not FAIL else f"{len(FAIL)} FAILED: {FAIL}")
sys.exit(1 if FAIL else 0)
