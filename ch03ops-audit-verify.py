#!/usr/bin/env python3
"""ch03-operator-sequence audit (stdlib). Exit 0 = pass."""
import math,re,sys
bad=0
def ck(n,c):
    global bad; print(('PASS ' if c else 'FAIL ')+n); bad+=(not c)
# noncommuting yet invertible: rotation vs shear
R=lambda a:[[math.cos(a),-math.sin(a)],[math.sin(a),math.cos(a)]]
Sh=[[1,1],[0,1]]
mm=lambda A,B:[[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
A,B=mm(R(.5),Sh),mm(Sh,R(.5))
ck('rotation and shear do not commute',max(abs(A[i][j]-B[i][j]) for i in range(2) for j in range(2))>0.1)
det=lambda M:M[0][0]*M[1][1]-M[0][1]*M[1][0]
ck('both invertible',abs(det(R(.5)))>0.9 and abs(det(Sh))>0.9)
# d_f unit dependence
df=lambda mu,lam:1+math.log(abs(mu))/math.log(lam)
ck('d_f = 0.14 for 0.55/s, lam=2',abs(df(0.55,2)-0.137)<0.01)
ck('d_f = 6.0 for 33/min, lam=2',abs(df(33,2)-6.04)<0.01)
ck('d_f depends on the unit',abs(df(0.55,2)-df(33,2))>5)
t=re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',open('ch03-operator-sequence.html',encoding='utf-8').read()))
for g in ['Audit note (2026-10-25)','non-commutativity alone does not imply irreversibility','is proposed to enter the fractal dimension','dimensionally well-defined','Ch19Enzyme.lean']: ck('present: '+g,g in t)
ck('absent: enters the fractal dimension of the post-transition structure directly','enters the fractal dimension of the post-transition structure directly' not in t)
sys.exit(1 if bad else 0)
