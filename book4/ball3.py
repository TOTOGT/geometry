import numpy as np, math, collections
from scipy.spatial import ConvexHull, SphericalVoronoi
phi=(1+5**0.5)/2
def icosa():
    V=[]
    for s1 in(1,-1):
        for s2 in(1,-1): V+=[(0,s1,s2*phi),(s1,s2*phi,0),(s1*phi,0,s2)]
    V=np.array(V,float); V/=np.linalg.norm(V,axis=1)[:,None]
    F=[]
    for t in ConvexHull(V).simplices:                     # orient CCW seen from outside
        A,B,C=V[t]
        if np.dot(np.cross(B-A,C-A),A)<0: t=[t[0],t[2],t[1]]
        F.append(list(t))
    return V,F
def sph_area(P):
    n=len(P); tot=0.
    for i in range(n):
        a,b,c=P[i-1],P[i],P[(i+1)%n]
        u=np.cross(b,a); v=np.cross(b,c); u/=np.linalg.norm(u); v/=np.linalg.norm(v)
        tot+=math.acos(max(-1,min(1,u@v)))
    return tot-(n-2)*math.pi
def geodesic(m,n):
    T=m*m+m*n+n*n
    w=np.array([math.cos(math.pi/3),math.sin(math.pi/3)])
    R=np.array([[.5,-math.sin(math.pi/3)],[math.sin(math.pi/3),.5]])
    z=np.array([float(m),0.])+n*w
    Mi=np.linalg.inv(np.array([z,R@z]).T)
    rng=range(-3*(m+n)-3,3*(m+n)+4); bary=[]
    for a in rng:
        for b in rng:
            p=np.array([float(a),0.])+b*w; vw=Mi@p; u=1-vw.sum()
            if u>=-1e-9 and vw[0]>=-1e-9 and vw[1]>=-1e-9: bary.append((u,vw[0],vw[1]))
    V,F=icosa(); pts=[]
    for f in F:
        A,B,C=V[f[0]],V[f[1]],V[f[2]]
        for u,v,x in bary:
            q=u*A+v*B+x*C; pts.append(q/np.linalg.norm(q))
    pts=np.array(pts); _,idx=np.unique(np.round(pts,6),axis=0,return_index=True)
    return pts[sorted(idx)],T
print(f"{'ball':>10}{'T':>5}{'balls':>7}{'5/6/other':>18}{'hex:pent':>10}{'max/min':>9}{'CV%':>7}{'round':>8}")
rows=[]
for m,n in [(1,0),(1,1),(2,0),(2,1),(3,0),(2,2),(3,1),(4,0),(3,2),(4,1),(3,3),(4,4),(5,5)]:
    G,T=geodesic(m,n)
    assert len(G)==10*T+2,(m,n,len(G),10*T+2)
    sv=SphericalVoronoi(G,1.0,np.zeros(3)); sv.sort_vertices_of_regions()
    S=np.array([len(r) for r in sv.regions])
    A=np.array([sph_area(sv.vertices[r]) for r in sv.regions])
    other={k:int(v) for k,v in collections.Counter(S).items() if k not in(5,6)}
    pen=A[S==5].mean(); hx=A[S==6].mean() if (S==6).any() else float('nan')
    ch=ConvexHull(sv.vertices); IQ=36*math.pi*ch.volume**2/ch.area**3
    tag='CHIRAL' if (m!=n and m and n) else ''
    print(f"  GP({m},{n}){T:>5}{len(G):>7}   {(S==5).sum():>3}/{(S==6).sum():>4}/{str(other) if other else '-':>5}"
          f"{hx/pen:>10.4f}{A.max()/A.min():>9.4f}{100*A.std()/A.mean():>7.2f}{IQ:>8.4f}  {tag}")
