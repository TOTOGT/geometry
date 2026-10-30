# Fast exact touch counter for the 45-degree tent curve, by vertex hashing (book4/fractals.html).
# Counts pairs of non-adjacent edges (index difference >= 2) that share a vertex. It does NOT see
# (pairs sharing both endpoints are counted once). It does NOT see a vertex lying in the interior of another edge (a T-junction); that is why its output is checked
# against the all-pairs integer counter (fractals-touch-count.py) for every level that counter reaches.
# Usage: python3 fractals-touch-fast.py MAXLEVEL
import numpy as np, sys, time
G=[(0,0),(1,1),(2,2),(3,1),(4,0)]
def build(n):
    x=np.array([0,1],dtype=np.int64); y=np.array([0,0],dtype=np.int64)
    for _ in range(n):
        dx=np.diff(x); dy=np.diff(y)
        X=np.zeros((len(dx),4),dtype=np.int64);Y=np.zeros((len(dx),4),dtype=np.int64)
        for k in range(4):
            gx,gy=G[k]
            X[:,k]=4*x[:-1]+gx*dx-gy*dy
            Y[:,k]=4*y[:-1]+gx*dy+gy*dx
        x=np.append(X.reshape(-1),4*x[-1]); y=np.append(Y.reshape(-1),4*y[-1])
    return x,y
def touches(x,y):
    n=len(x)-1                      # edges 0..n-1, edge e joins vertex e and e+1
    key=x*(1<<31)+(y+(1<<30))       # exact: |coords| < 2^30 for levels <= 12
    pid=np.unique(key,return_inverse=True)[1].astype(np.int64)
    eidx=np.concatenate([np.arange(n),np.arange(n)])
    p=np.concatenate([pid[:-1],pid[1:]])
    o=np.lexsort((eidx,p)); p=p[o]; e=eidx[o]
    total=0; d=1
    while True:
        if d>=len(p): break
        same=p[:-d]==p[d:]
        if not same.any(): break
        total+=int((same&((e[d:]-e[:-d])>=2)).sum())
        d+=1
    # pairs of edges that share BOTH endpoints (the same segment traversed twice) were counted twice
    a=pid[:-1]; b=pid[1:]
    lo=np.minimum(a,b); hi=np.maximum(a,b)
    ek=lo*(int(pid.max())+1)+hi
    o2=np.lexsort((np.arange(n),ek)); ek=ek[o2]; ei=np.arange(n)[o2]
    dup=0; d=1
    while d<len(ek):
        same=ek[:-d]==ek[d:]
        if not same.any(): break
        dup+=int((same&((ei[d:]-ei[:-d])>=2)).sum()); d+=1
    return total-dup
for n in range(1,int(sys.argv[1])+1):
    t0=time.time(); x,y=build(n); print(n,touches(x,y),f"{time.time()-t0:.1f}s",flush=True)
