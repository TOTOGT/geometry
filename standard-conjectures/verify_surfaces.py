#!/usr/bin/env python3
"""X = T x S, product of two smooth projective surfaces, h = H_T + H_S.
Product-generated codim-2 classes: z = a*[pt_T] + omega + b*[pt_S], omega in NS(T) (x) NS(S).
Hand derivation (Hodge index on each surface: NS = Q.H + P, P negative definite):
  primitive  <=>  a = -H_T^2 c,  b = -H_S^2 c,  omega = c H_T(x)H_S + omega',  omega' in P_T (x) P_S
  deg(z^2) = 2ab + <omega,omega> = 3 c^2 H_T^2 H_S^2 + <omega',omega'>,
  and <.,.> on P_T (x) P_S is a product of two negative definite forms, hence positive definite.
This script checks the claim exactly (rational arithmetic) on generic Gram matrices, in a NON-orthogonal
basis, and runs two negative controls. It checks the product-generated part ONLY.
"""
import sympy as sp, itertools
def gram(h2, Q, M):
    """NS Gram in basis M*(H, P-basis): block diag(h2, -Q) conjugated by an invertible rational M."""
    k = Q.shape[0]
    G0 = sp.diag(sp.Matrix([[h2]]), -Q)
    G0 = sp.Matrix(sp.BlockDiagMatrix(sp.Matrix([[h2]]), -Q))
    return M.T*G0*M, M  # basis vectors e_i = M-columns combos
def run(name, hT2, QT, MT, hS2, QS, MS, pos_ok=True):
    GT = sp.Matrix(sp.BlockDiagMatrix(sp.Matrix([[hT2]]), -QT)); GT = MT.T*GT*MT
    GS = sp.Matrix(sp.BlockDiagMatrix(sp.Matrix([[hS2]]), -QS)); GS = MS.T*GS*MS
    rT, rS = GT.shape[0], GS.shape[0]
    # H_T in the new basis: old basis vector 0 = M^{-1} column 0 expressed in new coords
    hT = MT.inv()[:,0]; hS = MS.inv()[:,0]
    # sanity: H_T.H_T = hT2
    assert (hT.T*GT*hT)[0] == hT2 and (hS.T*GS*hS)[0] == hS2
    # unknowns: a, b, W (rT x rS)
    W = sp.Matrix(rT, rS, sp.symbols('w0:%d' % (rT*rS)))
    a, b = sp.symbols('a b')
    # contraction with H_T on T factor -> vector in NS(S) coords; plus a*H_S
    c1 = (hT.T*GT*W) + a*hS.T          # 1 x rS  (a*pt_T (x) H_S + (H_T.omega))
    c2 = (W*GS*hS) + b*hT              # rT x 1  (b*H_T (x) pt_S + (omega . H_S))
    eqs = list(c1) + list(c2)
    unk = [a, b] + list(W)
    A, _ = sp.linear_eq_to_matrix(eqs, unk)
    ns = A.nullspace()
    dim_expected = 1 + (rT-1)*(rS-1)
    ok_dim = (len(ns) == dim_expected)
    def deg2(vec_u, vec_v):
        au, bu = vec_u[0], vec_u[1]; Wu = sp.Matrix(rT, rS, list(vec_u[2:]))
        av, bv = vec_v[0], vec_v[1]; Wv = sp.Matrix(rT, rS, list(vec_v[2:]))
        # <z,z'> = a b' + a' b + <omega,omega'>
        return au*bv + av*bu + (Wu.T*GT*Wv*GS).trace()
    Gm = sp.Matrix(len(ns), len(ns), lambda i, j: deg2(ns[i], ns[j]))
    # positive definite <=> all leading principal minors > 0
    minors = [Gm[:k,:k].det() for k in range(1, len(ns)+1)]
    posdef = bool(all(m > 0 for m in minors))
    L, D = Gm.LDLdecomposition()
    cert = bool((L*D*L.T - Gm).is_zero_matrix and all(D[i, i] > 0 for i in range(D.shape[0])) and all(L[i, i] == 1 for i in range(L.shape[0])))
    print(('PASS ' if cert else 'FAIL ') + '   certificate: Gram = L D L^T, L unit lower triangular rational, D = %s all > 0' % [D[i, i] for i in range(D.shape[0])])
    ok_dim = ok_dim and cert
    print(('PASS ' if (ok_dim and posdef == pos_ok) else 'FAIL ') +
          '%-34s rho=(%d,%d) dim primitive=%d (expected %d) pos.def=%s (expected %s)' %
          (name, rT, rS, len(ns), dim_expected, posdef, pos_ok))
    return ok_dim and posdef == pos_ok
I = sp.Integer
res = []
# 1. rho = 1,1: reproduces the P2xP2 value 3 H_T^2 H_S^2 (single primitive class)
res.append(run('rho=(1,1) P2xP2-type', 1, sp.zeros(0,0), sp.eye(1), 1, sp.zeros(0,0), sp.eye(1)))
# 2. rho=(3,3), generic non-orthogonal rational bases
QT = sp.Matrix([[2,1],[1,3]]); QS = sp.Matrix([[5,2],[2,1]])
MT = sp.Matrix([[1,2,0],[0,1,3],[1,0,1]]); MS = sp.Matrix([[2,0,1],[1,1,0],[0,3,1]])
res.append(run('rho=(3,3) generic basis', 4, QT, MT, 6, QS, MS))
# 3. rho=(2,4)
QT2 = sp.Matrix([[3]]); QS2 = sp.Matrix([[2,1,0],[1,2,1],[0,1,2]])
MT2 = sp.Matrix([[1,1],[0,1]]); MS2 = sp.Matrix([[1,0,0,1],[0,1,0,0],[0,0,1,2],[1,0,0,1]]).inv() if False else sp.Matrix([[1,0,0,0],[1,1,0,0],[0,1,1,0],[0,0,1,1]])
res.append(run('rho=(2,4)', 3, QT2, MT2, 2, QS2, MS2))
# NEGATIVE CONTROLS: the Hodge index input matters.
# 4. S with a positive definite NS (violates Hodge index): positivity should be able to fail.
def run_bad():
    hT2, hS2 = 1, 1
    GT = sp.diag(hT2, -2); GS = sp.diag(hS2, +3)        # P_S positive: NOT allowed by Hodge index
    rT, rS = 2, 2
    hT = sp.Matrix([1,0]); hS = sp.Matrix([1,0])
    W = sp.Matrix(rT, rS, sp.symbols('v0:4')); a, b = sp.symbols('a b')
    eqs = list(hT.T*GT*W + a*hS.T) + list(W*GS*hS + b*hT)
    A, _ = sp.linear_eq_to_matrix(eqs, [a,b]+list(W)); ns = A.nullspace()
    Gm = sp.Matrix(len(ns), len(ns), lambda i,j: ns[i][0]*ns[j][1]+ns[j][0]*ns[i][1] + (sp.Matrix(2,2,list(ns[i][2:])).T*GT*sp.Matrix(2,2,list(ns[j][2:]))*GS).trace())
    posdef = all(Gm[:k,:k].det() > 0 for k in range(1, len(ns)+1))
    print(('PASS ' if not posdef else 'FAIL ') + 'control: P_S positive (Hodge index violated) -> positivity fails: pos.def=%s' % posdef)
    return not posdef
res.append(run_bad())
# 5. control: drop primitivity, the full product-generated form is indefinite
G = sp.Matrix([[0,0,1],[0,1,0],[1,0,0]])  # a,omega,b with rho=1: 2ab + c^2 H_T^2H_S^2 pattern, (a,omega,b)
ev = [sp.Matrix([1,0,-1]), sp.Matrix([0,1,0])]
v1 = (ev[0].T*G*ev[0])[0]; v2 = (ev[1].T*G*ev[1])[0]
print(('PASS ' if (v1 < 0 < v2) else 'FAIL ') + 'control: unrestricted form takes both signs (%s, %s)' % (v1, v2))
res.append(v1 < 0 < v2)
res = [bool(r) for r in res]
print('%d/%d checks passed' % (sum(res), len(res)))
raise SystemExit(0 if all(res) else 1)
