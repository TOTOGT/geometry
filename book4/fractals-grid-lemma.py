# Checks the two structural facts used in the 45-degree no-crossing argument (book4/fractals.html, section 3).
# Exact integers. Level n coordinates are scaled by 4^n.
#  (E) even level n=2m: every segment is a unit edge of the square grid of spacing l=8^(-m), axis-parallel.
#  (O) odd level n=2m+1: every segment lies on a leg of a 'tent' over a grid edge of the level-2m grid,
#      i.e. along a cell diagonal between a grid corner and the cell centre.
import numpy as np
G=[(0,0),(1,1),(2,2),(3,1),(4,0)]
def build(n):
    x=np.array([0,1],dtype=np.int64); y=np.array([0,0],dtype=np.int64)
    for _ in range(n):
        dx=np.diff(x); dy=np.diff(y)
        X=np.zeros((len(dx),4),dtype=np.int64); Y=np.zeros((len(dx),4),dtype=np.int64)
        for k in range(4):
            gx,gy=G[k]; X[:,k]=4*x[:-1]+gx*dx-gy*dy; Y[:,k]=4*y[:-1]+gx*dy+gy*dx
        x=np.append(X.reshape(-1),4*x[-1]); y=np.append(Y.reshape(-1),4*y[-1])
    return x,y
ok=True
for n in range(0,9):
    x,y=build(n); S=4**n
    if n%2==0:
        m=n//2; l=S//(8**m) if S%(8**m)==0 else None
        dx=np.diff(x); dy=np.diff(y)
        good=(l is not None) and np.all(x%l==0) and np.all(y%l==0) and np.all((np.abs(dx)==l)&(dy==0)|(np.abs(dy)==l)&(dx==0))
        print(f"level {n}: unit grid edges of spacing 8^-{m}: {bool(good)}")
    else:
        m=(n-1)//2; l=S//(8**m)           # grid spacing of the parent even level, in these units
        dx=np.diff(x); dy=np.diff(y)
        good=np.all(np.abs(dx)==np.abs(dy))   # all diagonal
        # nearest grid corner c of each endpoint pair: segment must lie in [corner, centre] of a cell
        mx=(x[:-1]+x[1:]); my=(y[:-1]+y[1:])  # twice the midpoint
        # corner = round(midpoint / l) * l  ; need |x-cx|=|y-cy|<=l/2 for both endpoints
        cx=np.rint(mx/(2*l)).astype(np.int64)*l; cy=np.rint(my/(2*l)).astype(np.int64)*l
        inleg=np.all((np.abs(x[:-1]-cx)==np.abs(y[:-1]-cy))&(np.abs(x[1:]-cx)==np.abs(y[1:]-cy))&(2*np.abs(x[:-1]-cx)<=l)&(2*np.abs(x[1:]-cx)<=l))
        print(f"level {n}: all diagonal: {bool(good)}; every segment on a corner-to-centre leg: {bool(inleg)}")
