#!/usr/bin/env python3
"""ch21 audit evidence (read-only). Checks: Loeschian set, chirality criterion, vertex types, alpha^dalpha."""
import itertools, collections, sympy as sp
F=[]
def ck(ok,m):
    print('[%s] %s'%('PASS' if ok else 'FAIL',m)); 
    if not ok: F.append(m)
# 1 Loeschian numbers up to 100 and non-members
L=sorted({m*m+m*n+n*n for m in range(0,12) for n in range(0,12)}-{0})
L100=[t for t in L if t<=100]
print('T<=100:',L100)
non=[t for t in range(1,16) if t not in L]
ck(non==[2,5,6,8,10,11,14,15],'non-members <=15 = %s'%non)
ck(2 not in L and 5 not in L,'T=2 and T=5 not Loeschian (22 and 52 sites impossible)')
# 21.3: T<=216 sites => T<=21
ck([t for t in L if 10*t+2<=216]==[1,3,4,7,9,12,13,16,19,21],'ex 21.3 T list')
# chirality: GP(m,n) chiral iff m!=n, m*n!=0
chir=[(m,n) for m in range(0,6) for n in range(0,m+1) if (m,n)!=(0,0) and n!=0 and m!=n]
print('chiral (m>=n) with m<=5:',chir)
ck((2,1) in chir and (3,1) in chir and (3,2) in chir and (4,1) in chir,'page chiral rows chiral')
# 'chirality <=> p splits': GP(7,0) achiral, T=49, 7 splits in Z[w]
ck((7,0) not in chir and 7%3==1,'GP(7,0) achiral though 7 = 1 mod 3 splits')
# 2 vertex types of class I geodesic via face lattice: count for T=1 (icosa) and T=4 via Euler: all verts deg5 or 6; (5,5,5) means faces around a hexagon-vertex
# build Goldberg dual = geodesic: triangulated sphere; Goldberg vertex = triangle of geodesic; type = degrees of its 3 corners
import numpy as np
def geod_triangles(m,n):
    phi=(1+5**.5)/2
    V=[(-1,phi,0),(1,phi,0),(-1,-phi,0),(1,-phi,0),(0,-1,phi),(0,1,phi),(0,-1,-phi),(0,1,-phi),(phi,0,-1),(phi,0,1),(-phi,0,-1),(-phi,0,1)]
    V=np.array(V,float); V/=np.linalg.norm(V[0])
    # edges
    d=np.linalg.norm(V[:,None]-V[None],axis=2); e=d[d>0].min()
    Fc=[(i,j,k) for i,j,k in itertools.combinations(range(12),3) if abs(d[i,j]-e)<1e-9 and abs(d[j,k]-e)<1e-9 and abs(d[i,k]-e)<1e-9]
    assert len(Fc)==20
    pts={};tri=set()
    def key(p): return tuple(np.round(p/np.linalg.norm(p),7))
    def idx(p):
        k=key(p)
        if k not in pts: pts[k]=len(pts)
        return pts[k]
    for (i,j,k) in Fc:
        A,B,C=V[i],V[j],V[k]
        if np.dot(np.cross(B-A,C-A),A+B+C)<0: B,C=C,B
        u=(B-A)/(m+n)*1.0; w=(C-A)/(m+n)*1.0
        # Eisenstein basis e1=(m,n), e2 rotated 60: use barycentric lattice vectors
        # lattice vector a=(m,n): a = m*u0 + n*w0 with u0=(B-A)/(m+n)? use standard: grid in triangle with basis p=(B-A)/(m+n)... build via triangle ABC in plane coords
        # planar coords: A=(0,0), B=(1,0), C=(.5,sqrt3/2); Eisenstein triangle with vertices 0, m+n w?, handled below
        # class vertices of big triangle: 0, z=(m+n*w)?? use z=m+n*w, w=e^{i pi/3}; vertices 0, z, z*w
        w6=complex(.5,3**.5/2); z=m+n*w6
        P=[0,z,z*w6]
        # all lattice pts a+b*w6 inside closed triangle
        M=np.array([[P[1].real,P[2].real],[P[1].imag,P[2].imag]])
        Mi=np.linalg.inv(M)
        loc={}
        R=m+n+2
        for a in range(-R,R+1):
            for b in range(-R,R+1):
                q=a+b*w6; l=Mi@np.array([q.real,q.imag])
                if l[0]>=-1e-9 and l[1]>=-1e-9 and l[0]+l[1]<=1+1e-9:
                    s=1-l[0]-l[1]; X=s*A+l[0]*B+l[1]*C
                    loc[(a,b)]=idx(X)
        for (a,b),i0 in loc.items():
            for (da,db,ea,eb) in [(1,0,0,1),(0,1,-1,1)]:
                p1=(a+da,b+db);p2=(a+ea,b+eb)
                # triangles (a,b),(a+1,b),(a,b+1) and (a+1,b),(a,b+1),(a+1,b+1)
            for t in [((a,b),(a+1,b),(a,b+1)),((a+1,b),(a,b+1),(a+1,b+1))]:
                if all(x in loc for x in t): tri.add(frozenset(loc[x] for x in t))
    return pts,tri
import ast, numpy as _np
from scipy.spatial import ConvexHull
import os; src=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'ball3.py')).read(); tree=ast.parse(src)
pre=[]
for nd in tree.body:
    if isinstance(nd,ast.For): break
    pre.append(nd)
ns={'np':_np}
exec(compile(ast.Module(body=pre,type_ignores=[]),'ball3','exec'),ns)
for (m,n,T) in [(1,0,1),(1,1,3),(2,0,4),(2,1,7),(3,0,9),(2,2,12)]:
    G,TT=ns['geodesic'](m,n); G=_np.asarray(G)
    ck(TT==T and len(G)==10*T+2,'GP(%d,%d): T=%d sites=%d'%(m,n,TT,len(G)))
    h=ConvexHull(G); tri=h.simplices
    nb=collections.defaultdict(set)
    for t in tri:
        for a in t:
            for b in t:
                if a!=b: nb[a].add(b)
    dg={v:len(s) for v,s in nb.items()}
    types=collections.Counter(tuple(sorted(dg[v] for v in t)) for t in tri)
    print('   vertex types:',dict(types))
    ck(len(tri)==20*T,'GP(%d,%d): 20T=%d vertices of the Goldberg polyhedron'%(m,n,20*T))
    if T==3: ck(set(types)=={(5,6,6)},'T=3 every vertex is (5,6,6)')
    else: ck(set(types)!={(5,6,6)},'T=%d is not uniformly (5,6,6)'%T)
# 3 contact form
z,r,th=sp.symbols('z r theta',real=True)
alpha=sp.Matrix([1,0,-r**2]); X=[z,r,th]
def d1(a): # exterior derivative coefficients
    return sp.Matrix(3,3,lambda i,j: sp.diff(a[j],X[i])-sp.diff(a[i],X[j]))
da=d1(alpha)
# alpha^dalpha coefficient on dz^dr^dtheta = a_z*da_rt - a_r*da_zt + a_t*da_zr
c=alpha[0]*da[1,2]-alpha[1]*da[0,2]+alpha[2]*da[0,1]
print('alpha^dalpha coeff of dz dr dtheta =',sp.simplify(c))
ck(sp.simplify(c+2*r)==0,'alpha^dalpha = -2r dz^dr^dtheta in polar coordinates (r is the polar Jacobian; contact on all of R^3 in Cartesian form, see ch22_audit_check.py)')
raise SystemExit(1 if F else 0)
