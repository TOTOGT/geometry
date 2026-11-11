#!/usr/bin/env python3
"""Projected (-2)-chain on T x S. e_i = E_i - (H.E_i/H^2) H.
Checks, in exact rational arithmetic:
 1. -(e_i.e_j) = C_m + u u^T/d  (Gram of projected chain, from E_i.E_j = -C_ij)
 2. deg(z^2) = tr(Z^T K_T Z K_S) equals the four-term sum of squares, for random Z
 3. D^T D = C_m, D injective (rank m)
 4. K_T (x) K_S has an LDL^T certificate with D > 0
 5. negative control: d <= 0 (Hodge-index violated) can destroy definiteness"""
import sympy as sp, random, sys
random.seed(7)
ok=[]
def chk(n,c):
    ok.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n)
def cartan(m): return sp.Matrix(m,m,lambda i,j: 2 if i==j else (-1 if abs(i-j)==1 else 0))
def Dm(m):
    D=sp.zeros(m+1,m)
    for j in range(m):
        D[j,j]=1; D[j+1,j]=-1
    return D
def ldl_pos(M):
    n=M.shape[0]; A=sp.Matrix(M)
    for k in range(n):
        if A[k,k]<=0: return False
        for i in range(k+1,n):
            f=A[i,k]/A[k,k]
            for j in range(k,n): A[i,j]-=f*A[k,j]
    return True
def rq(): return sp.Rational(random.randint(1,9),random.randint(1,5))
for m,n in ((1,1),(2,3),(3,3),(4,2),(5,4)):
    C,Cn=cartan(m),cartan(n)
    u=sp.Matrix([rq() for _ in range(m)]); v=sp.Matrix([rq() for _ in range(n)])
    dT,dS=rq()+1,rq()+1
    # 1: Gram of e_i via bilinearity, E_i.E_j=-C_ij, H.E_i=u_i, H.H=dT
    G=sp.Matrix(m,m,lambda i,j: -C[i,j]-u[i]*u[j]/dT)  # e_i.e_j expanded
    K_T=C+u*u.T/dT; K_S=Cn+v*v.T/dS
    chk(f'A{m}: -(e_i.e_j) = C + uu^T/d', -G==K_T)
    D,Dn=Dm(m),Dm(n)
    chk(f'A{m},A{n}: D^T D = C and rank m,n', D.T*D==C and Dn.T*Dn==Cn and D.rank()==m and Dn.rank()==n)
    Z=sp.Matrix(m,n,lambda i,j: sp.Rational(random.randint(-6,6),random.randint(1,4)))
    lhs=(Z.T*K_T*Z*K_S).trace()
    N=lambda M: sum(x*x for x in M)
    rhs=N(D*Z*Dn.T)+N(u.T*Z*Dn.T)/dT+N(D*Z*v)/dS+((u.T*Z*v)[0])**2/(dT*dS)
    chk(f'A{m}xA{n}: deg(z^2) = four-term sum of squares', lhs==rhs)
    # deg(z^2) as quadratic form of Kronecker product on vec(Z)
    from sympy.physics.quantum import TensorProduct as TP
    zvec=sp.Matrix([Z[i,j] for i in range(m) for j in range(n)])
    chk(f'A{m}xA{n}: Kronecker form agrees', (zvec.T*sp.kronecker_product(K_T,K_S)*zvec)[0]==lhs)
    chk(f'A{m}xA{n}: LDL certificate for K_T (x) K_S, D>0', ldl_pos(sp.kronecker_product(K_T,K_S)))
# negative control: d<0 with large u makes K indefinite
C=cartan(2); u=sp.Matrix([5,5]); K=C+u*u.T/sp.Rational(-1)
chk('control: d<0 gives a non-definite K', not ldl_pos(K))
print('%d/%d checks passed'%(sum(ok),len(ok))); sys.exit(0 if all(ok) else 1)
