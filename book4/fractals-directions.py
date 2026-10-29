# Counts distinct segment direction vectors of the tent curve at rational tan(theta)=p/q, exact integers.
# Usage: python3 fractals-directions.py   (book4/fractals.html, section 3)
import numpy as np, math, time, sys
from math import gcd
def build(p,q,n):
    G=[(0,0),(q,p),(2*q,2*p),(3*q,p),(4*q,0)]; S=4*q
    x=np.array([0,1],dtype=np.int64); y=np.array([0,0],dtype=np.int64)
    for _ in range(n):
        dx=np.diff(x); dy=np.diff(y)
        X=np.zeros((len(dx),4),dtype=np.int64); Y=np.zeros((len(dx),4),dtype=np.int64)
        for k in range(4):
            gx,gy=G[k]
            X[:,k]=S*x[:-1]+gx*dx-gy*dy; Y[:,k]=S*y[:-1]+gx*dy+gy*dx
        x=np.append(X.reshape(-1),S*x[-1]); y=np.append(Y.reshape(-1),S*y[-1])
    return x,y
print("distinct segment directions (exact, from integer vectors) at levels 1..5")
for p,q in [(1,3),(1,2),(3,4),(1,1),(4,3),(2,1)]:
    out=[]
    for n in range(1,6):
        x,y=build(p,q,n); dx=np.diff(x); dy=np.diff(y)
        g=np.gcd(np.abs(dx),np.abs(dy)); g[g==0]=1
        out.append(len(set(zip((dx//g).tolist(),(dy//g).tolist()))))
    print(f"tan={p}/{q}: {out}")
