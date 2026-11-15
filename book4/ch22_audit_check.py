#!/usr/bin/env python3
"""ch22 audit evidence (read-only). Requires sympy."""
import sympy as sp
F=[]
def ck(ok,m):
    print('[%s] %s'%('PASS' if ok else 'FAIL',m))
    if not ok: F.append(m)
# 1 contact form in Cartesian coordinates: alpha = dz - (x dy - y dx)
x,y,z=sp.symbols('x y z',real=True); X=[x,y,z]
a=sp.Matrix([y,-x,1])          # dz - r^2 dtheta = dz - (x dy - y dx)
da=sp.Matrix(3,3,lambda i,j: sp.diff(a[j],X[i])-sp.diff(a[i],X[j]))
c=a[0]*da[1,2]-a[1]*da[0,2]+a[2]*da[0,1]
print('alpha^dalpha coeff of dx dy dz (Cartesian):',sp.simplify(c))
ck(sp.simplify(c)==-2 or sp.simplify(c)==2,'alpha^dalpha is a nonzero constant multiple of dx^dy^dz: contact on all of R^3 incl. r=0')
# polar picture: dx^dy = r dr^dtheta, so -2 dz^dx^dy = -2r dz^dr^dtheta (r=0 is a coordinate singularity)
# 2 torus of revolution: int K dA = 0 (R=2, r=1)
u,v=sp.symbols('u v',real=True); R,r=2,1
P=sp.Matrix([(R+r*sp.cos(v))*sp.cos(u),(R+r*sp.cos(v))*sp.sin(u),r*sp.sin(v)])
Pu,Pv=P.diff(u),P.diff(v); N=Pu.cross(Pv); n=sp.simplify(N.norm()); N=N/n
E,Fm,G=Pu.dot(Pu),Pu.dot(Pv),Pv.dot(Pv)
L,M,Nn=P.diff(u,2).dot(N),P.diff(u).diff(v).dot(N),P.diff(v,2).dot(N)
K=sp.simplify((L*Nn-M**2)/(E*G-Fm**2)); dA=sp.simplify(sp.sqrt(E*G-Fm**2))
I=sp.integrate(sp.simplify(K*dA),(u,0,2*sp.pi),(v,0,2*sp.pi))
print('K=',K,' int K dA =',sp.simplify(I)); ck(sp.simplify(I)==0,'torus: int K dA = 0 (Gauss-Bonnet, chi=0)')
# 3 cylinder (page 22.2 example, K=0): Gauss map N=(cos t, sin t, 0) has rank 1 everywhere -> degenerate, not a fold
t,h=sp.symbols('t h',real=True); Nc=sp.Matrix([sp.cos(t),sp.sin(t),0])
J=sp.Matrix.hstack(Nc.diff(t),Nc.diff(h)); ck(J.rank()==1,'cylinder: dN has rank 1 everywhere (det dN=0 on the whole surface, no fold curve)')
# 4 sphere: K=det dN = 1/R^2 check
th,ph,Rr=sp.symbols('theta phi R',positive=True)
S=Rr*sp.Matrix([sp.sin(th)*sp.cos(ph),sp.sin(th)*sp.sin(ph),sp.cos(th)]); Ns=S/Rr
Ju=sp.Matrix.hstack(Ns.diff(th),Ns.diff(ph)); Jx=sp.Matrix.hstack(S.diff(th),S.diff(ph))
# dN = (1/R) Id on tangent plane => det = 1/R^2
ck(sp.simplify(Ns.diff(th)-S.diff(th)/Rr).norm()==0 and sp.simplify(Ns.diff(ph)-S.diff(ph)/Rr).norm()==0,'sphere: dN = (1/R) dX on the tangent plane => det dN = 1/R^2 = K')
# 5 dimension count: conormal vs graph of tangent-space map, X^k in P^n
for n_,k in [(2,1),(3,1),(3,2),(4,2)]:
    con=n_-1; graph=k
    print('  P^%d, dim X=%d: dim Con(X)=%d, dim graph of tangent-space map=%d'%(n_,k,con,graph))
ck([(n_,k) for n_,k in [(2,1),(3,1),(3,2),(4,2)] if n_-1==k]==[(2,1),(3,2)],'dim Con(X)=n-1 equals dim X (graph of gamma) only for hypersurfaces; fails for (P^3,curve), (P^4,surface)')
raise SystemExit(1 if F else 0)
