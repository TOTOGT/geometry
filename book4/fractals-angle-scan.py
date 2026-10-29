# Exact-integer crossing/touch scan of the tent family at rational tan(theta)=p/q (book4/fractals.html section 3).
# Usage: python3 fractals-angle-scan.py   (about 1-2 minutes). Columns per level: (proper crossings, point touches, collinear overlaps).
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
def analyze(x,y):
    n=len(x)-1; ax,ay,bx,by=x[:-1],y[:-1],x[1:],y[1:]
    proper=0; pt=0; col=0
    sg=np.sign
    for i in range(n-2):
        j=np.arange(i+2,n); cx,cy,dx,dy=ax[j],ay[j],bx[j],by[j]
        o=lambda px,py,qx,qy,rx,ry: sg((qx-px)*(ry-py)-(qy-py)*(rx-px))
        o1=o(ax[i],ay[i],bx[i],by[i],cx,cy);o2=o(ax[i],ay[i],bx[i],by[i],dx,dy)
        o3=o(cx,cy,dx,dy,ax[i],ay[i]);o4=o(cx,cy,dx,dy,bx[i],by[i])
        proper+=int(((o1*o2<0)&(o3*o4<0)).sum())
        on=lambda px,py,qx,qy,rx,ry:(np.minimum(px,qx)<=rx)&(rx<=np.maximum(px,qx))&(np.minimum(py,qy)<=ry)&(ry<=np.maximum(py,qy))
        t=((o1==0)&on(ax[i],ay[i],bx[i],by[i],cx,cy))|((o2==0)&on(ax[i],ay[i],bx[i],by[i],dx,dy))|((o3==0)&on(cx,cy,dx,dy,ax[i],ay[i]))|((o4==0)&on(cx,cy,dx,dy,bx[i],by[i]))
        c=t&(o1==0)&(o2==0); col+=int(c.sum()); pt+=int((t&~c).sum())
    return proper,pt,col
cands=[(1,4),(1,3),(1,2),(2,3),(3,4),(1,1),(4,3),(3,2),(2,1)]
print("tan=p/q  theta   d=log4/log(4cos)   [per level: (proper, point-touch, collinear)]")
for p,q in cands:
    th=math.degrees(math.atan2(p,q)); c=4*q/math.hypot(p,q)
    d=math.log(4)/math.log(c) if c>1 else float('nan')
    maxn=1
    while (4*q)**(maxn+1)<=2e8 and maxn<6: maxn+=1
    res=[analyze(*build(p,q,n)) for n in range(1,maxn+1)]
    print(f"{p}/{q} {th:6.2f}  d={d:7.4f}  {res}",flush=True)
