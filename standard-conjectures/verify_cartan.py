#!/usr/bin/env python3
"""Cartan matrices, intersection graphs and the Kronecker products that appear in the T x S computation.
Exact rational arithmetic for definiteness (LDL^T certificates), numpy only for the eigenvalue formula.

Setting: curves E_i on a smooth projective surface with E_i^2 = -2 and E_i.E_j in {0,1} forming a Dynkin
graph G have intersection matrix -C(G), C(G) the Cartan matrix (Du Val / Artin; CITED, standard).
If H.E_i = 0 for all i then each E_i lies in H^perp, where the Hodge index theorem makes the form
negative semidefinite; for a Dynkin configuration it is negative DEFINITE (checked below by certificate).
On the product-generated part of T x S, the form on P_T (x) P_S restricted to two such configurations is
C(G_T) (x) C(G_S) (a Kronecker product of two positive definite matrices): positive definite, with
eigenvalues the products of the factors' eigenvalues.  For A_n: 4 sin^2(k pi / (2(n+1))).
"""
import sympy as sp, numpy as np, itertools, sys
ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(('PASS ' if cond else 'FAIL ') + name)
def cartan(edges, n):
    C = sp.zeros(n, n)
    for i in range(n): C[i, i] = 2
    for i, j in edges: C[i, j] = C[j, i] = -1
    return C
def A(n): return cartan([(i, i+1) for i in range(n-1)], n)
def D(n): return cartan([(i, i+1) for i in range(n-2)] + [(n-3, n-1)], n)
def E(n):
    e = [(i, i+1) for i in range(n-2)] + [(2, n-1)]
    return cartan(e, n)
def ldl_cert(M):
    try:
        L, Dg = M.LDLdecomposition()
    except Exception:          # sympy raises when M is not positive definite: no certificate exists
        return False
    return bool((L*Dg*L.T - M).is_zero_matrix and all(Dg[i, i] > 0 for i in range(M.shape[0])) and all(L[i, i] == 1 for i in range(M.shape[0])))
# 1. definiteness and determinants of the ADE Cartan matrices (rational certificates)
for n in range(1, 9):
    chk('A_%d Cartan: LDL certificate, det = %d' % (n, n+1), ldl_cert(A(n)) and A(n).det() == n+1)
for n in range(4, 9):
    chk('D_%d Cartan: LDL certificate, det = 4' % n, ldl_cert(D(n)) and D(n).det() == 4)
for n, dt in ((6, 3), (7, 2), (8, 1)):
    chk('E_%d Cartan: LDL certificate, det = %d' % (n, dt), ldl_cert(E(n)) and E(n).det() == dt)
# 2. negative control: the affine A~_2 (triangle) and A~_1 are only SEMI-definite, not definite
tri = cartan([(0, 1), (1, 2), (0, 2)], 3)
chk('control: affine A~_2 Cartan is singular (det 0): not definite', tri.det() == 0)
chk('control: a wrong graph (4-cycle with a chord weight) breaks definiteness', not ldl_cert(cartan([(0,1),(1,2),(2,3),(3,0),(0,2)], 4)))
# 3. eigenvalues of A_n Cartan = 4 sin^2(k pi / (2(n+1))); Kronecker eigenvalues are products
for n in range(1, 8):
    ev = np.sort(np.linalg.eigvalsh(np.array(A(n).tolist(), dtype=float)))
    th = np.sort([4*np.sin(k*np.pi/(2*(n+1)))**2 for k in range(1, n+1)])
    chk('A_%d eigenvalues = 4 sin^2(k pi/(2(n+1)))  (max err %.1e)' % (n, np.max(np.abs(ev-th))), np.max(np.abs(ev-th)) < 1e-12)
for m, n in ((2, 3), (3, 4), (4, 4), (5, 3)):
    K = sp.kronecker_product(A(m), A(n))
    chk('A_%d (x) A_%d Cartan: LDL certificate (positive definite), det = (%d)^%d (%d)^%d' % (m, n, m+1, n, n+1, m), ldl_cert(K) and K.det() == (m+1)**n*(n+1)**m)
    ev = np.sort(np.linalg.eigvalsh(np.array(K.tolist(), dtype=float)))
    th = np.sort([4*np.sin(i*np.pi/(2*(m+1)))**2*4*np.sin(j*np.pi/(2*(n+1)))**2 for i in range(1, m+1) for j in range(1, n+1)])
    chk('A_%d (x) A_%d eigenvalues = products (max err %.1e)' % (m, n, np.max(np.abs(ev-th))), np.max(np.abs(ev-th)) < 1e-11)
# 4. Milnor number of x y + z^(2n) (the A_{2n-1} surface of the Pinot table, type read from the page) = number of nodes 2n-1
x, y, z = sp.symbols('x y z')
def milnor(F):
    G = sp.groebner([sp.diff(F, v) for v in (x, y, z)], x, y, z, order='grevlex')
    lead = [sp.Poly(g, x, y, z).monoms(order='grevlex')[0] for g in G.exprs]
    B = 24
    return sum(1 for i in range(B) for j in range(B) for k in range(B) if not any(i >= a and j >= b and k >= c for a, b, c in lead))
for n in (2, 3, 4):
    chk('Milnor number of xy + z^%d = %d = rank of A_%d (nodes of the resolution graph)' % (2*n, 2*n-1, 2*n-1), milnor(x*y + z**(2*n)) == 2*n-1)
# D_m normal form z^2 + x y^2 + x^(m-1) has Milnor number m = rank D_m
for m in (4, 5, 6, 7):
    chk('Milnor number of z^2 + x y^2 + x^%d = %d = rank of D_%d' % (m-1, m, m), milnor(z**2 + x*y**2 + x**(m-1)) == m)
print('%d/%d checks passed' % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
