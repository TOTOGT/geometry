# Exact integer touch/crossing counter for the 45-degree tent curve (book4/fractals.html, section 5).
# Usage: python3 fractals-touch-count.py N   (levels 1..N; level 8 takes about 40 s)
# Output per level: (proper crossings, point touches, collinear overlaps) between non-adjacent pieces.
import numpy as np, sys, time
# integer Gaussian-rational build: coordinates scaled by 4^n
G=[(0,0),(1,1),(2,2),(3,1),(4,0)]  # generator * 4
def build(n):
    # work with complex ints scaled: each level coordinates scaled by 4 more
    x=np.array([0,1],dtype=np.int64); y=np.array([0,0],dtype=np.int64); sc=1
    for _ in range(n):
        dx=np.diff(x); dy=np.diff(y)
        nx=[];ny=[]
        X=np.zeros((len(dx),4),dtype=np.int64);Y=np.zeros((len(dx),4),dtype=np.int64)
        for k in range(4):
            gx,gy=G[k]
            X[:,k]=4*x[:-1]+gx*dx-gy*dy
            Y[:,k]=4*y[:-1]+gx*dy+gy*dx
        x=np.append(X.reshape(-1),4*x[-1]); y=np.append(Y.reshape(-1),4*y[-1]); sc*=4
    return x,y
def analyze(x,y):
    n=len(x)-1
    ax,ay,bx,by=x[:-1],y[:-1],x[1:],y[1:]
    proper=0; touch_pt=0; touch_col=0
    for i in range(n-2):
        j=np.arange(i+2,n)
        cx,cy,dx,dy=ax[j],ay[j],bx[j],by[j]
        def o(px,py,qx,qy,rx,ry): return np.sign((qx-px)*(ry-py)-(qy-py)*(rx-px))
        o1=o(ax[i],ay[i],bx[i],by[i],cx,cy); o2=o(ax[i],ay[i],bx[i],by[i],dx,dy)
        o3=o(cx,cy,dx,dy,ax[i],ay[i]); o4=o(cx,cy,dx,dy,bx[i],by[i])
        pr=(o1*o2<0)&(o3*o4<0); proper+=int(pr.sum())
        def on(px,py,qx,qy,rx,ry): return (np.minimum(px,qx)<=rx)&(rx<=np.maximum(px,qx))&(np.minimum(py,qy)<=ry)&(ry<=np.maximum(py,qy))
        t=((o1==0)&on(ax[i],ay[i],bx[i],by[i],cx,cy))|((o2==0)&on(ax[i],ay[i],bx[i],by[i],dx,dy))|((o3==0)&on(cx,cy,dx,dy,ax[i],ay[i]))|((o4==0)&on(cx,cy,dx,dy,bx[i],by[i]))
        col=t&(o1==0)&(o2==0)
        touch_col+=int(col.sum()); touch_pt+=int((t&~col).sum())
    return proper,touch_pt,touch_col
for n in range(1,int(sys.argv[1])+1):
    t0=time.time(); r=analyze(*build(n)); print(n,r,f"{time.time()-t0:.0f}s",flush=True)
