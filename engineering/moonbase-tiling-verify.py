#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""moonbase-tiling-verify.py -- companion to the 2026-10-13 audit-log entry "Moon Base Architecture claim (B9)" and the geometric
result that replaced the ">90% crew dose" Prediction 1 in the Overleaf Mars chapter. Written 2026-10-13 (R24).
CHECKED here: partition wall length per unit floor area for equal-area cells that tile the plane, regular triangle / square / hexagon,
(a) by closed form, (b) by counting unique edges in a finite patch (independent of the closed form). The first run of (b) FAILED because
the patch was not normalised to unit cell area (a bug in the check, not in the closed form); fixed the same day, and left on record here.
NOT checked: the honeycomb theorem itself (Hales, Discrete Comput. Geom. 25 (2001) 1-22) -- cited, not proved or read here;
mass saving (wall MASS depends on loads, joints, curvature; nothing here says mass scales with length); anything about radiation
(a layout shape does not shield; shielding is mass thickness over the crew); pressurized 3-D habitats (this is a plane tiling)."""
import math, sys
fails=[]
def check(ok,msg):
    print('    %s  %s'%('PASS' if ok else 'FAIL',msg))
    if not ok: fails.append(msg)
def head(n,t): print('\n'+'='*72+'\n  [%s]  %s\n'%(n,t)+'='*72)

head(1,'closed form: wall length per unit area, shared walls counted once')
# regular n-gon, side s, area A = n s^2 /(4 tan(pi/n)). Each wall is shared by 2 cells, so unique wall per cell = n s /2.
def wall_per_area(n):
    A1=n/(4*math.tan(math.pi/n))          # area for s=1
    s=1/math.sqrt(A1)                     # side for unit area
    return n*s/2
W={n:wall_per_area(n) for n in (3,4,6)}
for n,name in ((3,'triangle'),(4,'square'),(6,'hexagon')):
    print('    %-8s unique wall per unit area = %.4f   (without halving: %.4f)'%(name,W[n],2*W[n]))
check(abs(2*W[6]-3.7224)<5e-4,'hexagon 3.722 (unhalved)')
check(abs(2*W[4]-4.0)<1e-12,'square 4.000 (unhalved)')
check(abs(2*W[3]-4.5590)<5e-4,'triangle 4.559 (unhalved)')
r_sq=W[6]/W[4]; r_tr=W[6]/W[3]
print('    hexagon / square = %.4f  -> %.1f%% less ; hexagon / triangle = %.4f -> %.1f%% less'%(r_sq,100*(1-r_sq),r_tr,100*(1-r_tr)))
check(abs(100*(1-r_sq)-6.9)<0.1,'about 7% less than squares (6.9%)')
check(abs(100*(1-r_tr)-18.4)<0.1,'about 18% less than triangles (18.4%)')
check(abs(r_tr-math.sqrt(2/3))<1e-12,'hexagon/triangle ratio is exactly sqrt(2/3)')

head(2,'independent: count unique edges in a finite patch of each tiling')
def patch(kind,N=40):
    edges=set(); cells=0
    def key(p): return (round(p[0],6),round(p[1],6))
    def add(a,b):
        a,b=key(a),key(b); edges.add((a,b) if a<=b else (b,a))
    if kind==4:
        for i in range(N):
            for j in range(N):
                P=[(i,j),(i+1,j),(i+1,j+1),(i,j+1)]; cells+=1
                for k in range(4): add(P[k],P[(k+1)%4])
        side=1.0; area=N*N
    elif kind==3:
        for i in range(N):
            for j in range(N):
                a=(i+0.5*j,j*math.sqrt(3)/2); b=(a[0]+1,a[1]); c=(a[0]+0.5,a[1]+math.sqrt(3)/2); d=(a[0]+1.5,c[1])
                for T in ((a,b,c),(b,d,c)):
                    cells+=1
                    for k in range(3): add(T[k],T[(k+1)%3])
        side=1.0; area=cells*math.sqrt(3)/4
    else:
        s=1.0
        for q in range(N):
            for r in range(N):
                cx=s*math.sqrt(3)*(q+r/2); cy=s*1.5*r
                P=[(cx+s*math.cos(math.pi/6+k*math.pi/3),cy+s*math.sin(math.pi/6+k*math.pi/3)) for k in range(6)]; cells+=1
                for k in range(6): add(P[k],P[(k+1)%6])
        side=s; area=cells*3*math.sqrt(3)/2*s*s
    # wall/area scales as 1/side, so normalise to unit CELL area: multiply by sqrt(cell area at this side)
    return len(edges)*side/area*math.sqrt(area/cells)
for n,name in ((3,'triangle'),(4,'square'),(6,'hexagon')):
    v=patch(n); print('    %-8s patch: unique wall per unit area = %.4f (closed form %.4f; patch includes boundary walls)'%(name,v,W[n]))
    check(abs(v-W[n])/W[n]<0.06,'%s patch within 6%% of closed form (boundary effect shrinks as 1/N)'%name)
pv={n:patch(n,80) for n in (3,4,6)}
check(pv[6]<pv[4]<pv[3],'ordering hexagon < square < triangle holds in the large patch')

head(3,'what the polygon formula says if tiling is NOT required (why the audit rejected "isoperimetric optimum among regular polygons")')
for n in (3,4,5,6,8,12):
    print('    n=%2d  perimeter^2/area = %.4f'%(n,4*n*math.tan(math.pi/n)))
check(4*12*math.tan(math.pi/12)<4*6*math.tan(math.pi/6),'the 12-gon beats the hexagon on perimeter^2/area, but only n=3,4,6 tile the plane')
check(abs(4*6*math.tan(math.pi/6)-13.856)<5e-3 and abs(4*12*math.tan(math.pi/12)-12.861)<5e-3,'13.856 (hexagon) and 12.86 (12-gon) as in the audit-log entry')

print('\nRESULT: %s'%('ALL PASS' if not fails else '%d FAIL'%len(fails)))
sys.exit(1 if fails else 0)
