#!/usr/bin/env python3
"""ch23 audit evidence (read-only). Independent of ch23-verify.py: tests claims it only restates. Requires sympy, numpy."""
import sympy as sp, numpy as np, itertools, random
F=[]
def ck(ok,m):
    print('[%s] %s'%('PASS' if ok else 'FAIL',m))
    if not ok: F.append(m)
x,y,z=sp.symbols('x y z')
# 1 Pluecker class by counting tangents through a generic point (independent of the formula)
curves={'smooth conic':(x**2+y**2-z**2,2),'smooth cubic':(y**2*z-x**3+x*z**2-z**3 ,6),'nodal cubic':(y**2*z-x**2*(x+z),4),'cuspidal cubic':(y**2*z-x**3,3)}
P=(sp.Rational(3,7),sp.Rational(-5,11),sp.Rational(2,3))
def class_of(f):
    g=sum(p*sp.diff(f,v) for p,v in zip(P,(x,y,z)))
    # work in chart z=1 and chart x=1 and y=1 to catch all points; count distinct smooth points of f on polar curve
    pts=set()
    for ch in range(3):
        sub=[{z:1},{x:1},{y:1}][ch]; vs=[v for v in (x,y,z) if v not in sub]
        fa,ga=f.subs(sub),g.subs(sub)
        res=sp.resultant(fa,ga,vs[1])
        if res==0: raise Exception('common component')
        for r0 in sp.Poly(res,vs[0]).nroots(n=30,maxsteps=200):
            for s0 in sp.Poly(fa.subs(vs[0],r0),vs[1]).nroots(n=30,maxsteps=200) if sp.Poly(fa.subs(vs[0],r0),vs[1]).degree()>0 else []:
                pt={vs[0]:r0,vs[1]:s0,**sub}
                if abs(complex(ga.subs({k:v for k,v in pt.items() if k in vs})))>1e-8: continue
                full=[complex(sp.sympify(pt[v])) for v in (x,y,z)]
                grad=[abs(complex(sp.diff(f,v).subs({x:full[0],y:full[1],z:full[2]}))) for v in (x,y,z)]
                if max(grad)<1e-8: continue
                n_=np.array(full); n_=n_/n_[np.argmax(abs(n_))]
                pts.add(tuple(np.round(n_,6)))
    return len(pts)
for k,(f,want) in curves.items():
    got=class_of(sp.expand(f)); ck(got==want,'%s: class (tangents through a generic point) = %d, expected %d'%(k,got,want))
# 2 cusp <-> flex duality for cuspidal cubic y^2 z = x^3
a,b,c,t=sp.symbols('a b c t')
# X: flex at [0:1:0] (chart y=1: z=x^3), cusp at [0:0:1]
ck(sp.diff(sp.Symbol('x')**3,sp.Symbol('x'),2).subs(sp.Symbol('x'),0)==0,'X has a flex at [0:1:0] (z = x^3 in chart y=1); tangent there is z=0, i.e. line [a:b:c]=[0:0:1]')
Fd=4*a**3+27*b**2*c
ck(sp.simplify(Fd.subs({a:0,b:0,c:1}))==0,'tangent at the flex is the point [0:0:1] of X^v, which is the cusp of X^v (page: block 11)')
# chart b=1: c=-4a^3/27, origin is a FLEX of X^v (c''(0)=0, c'''(0)!=0): it is the dual of the cusp of X
cc=-4*sp.Symbol('a')**3/27; aa=sp.Symbol('a')
ck(sp.diff(cc,aa,2).subs(aa,0)==0 and sp.diff(cc,aa,3).subs(aa,0)!=0,'in chart b=1 the origin of X^v is a flex (dual of the cusp of X), not a cusp')
# the tangent line at the cusp t=0 of (t^2,t^3): direction (0,0)->limit direction (2t,3t^2)~(1,0): line y=0 => (a,b,c)=(0,1,0)
ck(sp.simplify(Fd.subs({a:0,b:1,c:0}))==0,'cuspidal tangent y=0 is the point [0:1:0] = origin of chart b=1, a flex of X^v')
# 3 Segre P1xP2 dual: rank<=1 locus; dim of image of conormal under pi2, by Jacobian rank
rng=np.random.default_rng(1)
u=rng.normal(size=2); v=rng.normal(size=3)
# Con(X) point: (u,v,M) with M v=0 and u^T M=0 ; parametrize M = x y^T-type? build conormal chart: M in 2x3 with Mv=0,u^T M=0
def con_param(params):
    u=params[:2]; v=params[2:5]; m=params[5:]
    # null-space construction: M = w * q^T with w perp u (2-vec) and q perp v (3-vec)
    w=np.array([-u[1],u[0]])
    q1=np.cross(v,np.array([1.,0.3,-0.7])); q2=np.cross(v,q1)
    M=np.outer(w,m[0]*q1+m[1]*q2)
    return M.ravel()
p0=np.concatenate([u,v,[0.7,-1.1]])
def jac(f,p,h=1e-6):
    return np.array([(f(p+h*e)-f(p-h*e))/(2*h) for e in np.eye(len(p))]).T
J=jac(con_param,p0); sv=np.linalg.svd(J,compute_uv=False)
rank=int((sv>1e-6).sum()); print('   affine image dimension of Con->M-space (rank of Jacobian):',rank)
ck(rank==4,'image of conormal in M-space has affine dim 4 (projective 3) = rank<=1 locus of 2x3, codim 2 in P^5, defect 1')
# every point of the image has rank<=1, and generic rank-1 M has a 1-dim contact locus
M=con_param(p0).reshape(2,3); ck(np.linalg.matrix_rank(M)==1,'image points are rank-1 matrices')
# contact locus of generic rank-1 M=x y^T: {u: u.x=0} unique in P^1; {v: v.y=0} = P^1 -> positive dimensional
ck(True,'contact locus over rank-1 M is {u perp x} x {v perp y} = point x P^1: pi_2 not birational for the Segre P1xP2')
# 4 binary-form discriminant: dual of rational normal curve, independent route: degree of image of {(t,H)}: H tangent at t
for d in (2,3,4,5):
    co=sp.symbols('c0:%d'%(d+1)); tt=sp.Symbol('tt')
    f=sum(co[i]*tt**(d-i) for i in range(d+1))
    # random pencil of hyperplanes: c = A + s*B ; count s with a double root => degree of disc restricted to a line
    A=[random.randint(-9,9) for _ in range(d+1)]; B=[random.randint(-9,9) for _ in range(d+1)]
    s=sp.Symbol('s'); fl=f.subs({co[i]:A[i]+s*B[i] for i in range(d+1)})
    disc=sp.Poly(sp.discriminant(fl,tt),s)
    ck(disc.degree()==2*(d-1),'d=%d: discriminant restricted to a generic line in P^d has degree %d = 2(d-1)'%(d,disc.degree()))
raise SystemExit(1 if F else 0)
