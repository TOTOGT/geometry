#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""book16/ch02-verify.py -- every number on book16/ch02-embedding-geometry.html. Run first.   python3 book16/ch02-verify.py
Standard library only (a small Jacobi eigenvalue routine is included). Written 2026-11-19, UNRUN BY ANYONE BUT THE AUTHOR OF THIS FILE until you run it.

  [1] the month ring: circulant kernel f(d)=exp(-dc/2.5); Fourier vectors are eigenvectors (max error); eigenvalues lambda_k;
      Gram matrix of the eigen-embedding reproduces C; centered top-2 principal components form an equal-radius circle in
      calendar order (circular score 1); the UNcentered top-2 do not (score printed, a failed first attempt kept on the page)
  [2] open ends: Toeplitz exp(-|i-j|/6), N=30: top eigenvalues; sign changes of the first six eigenvectors are 0..5; whether the
      first centered axis is monotone in year order (a negative result if false)
  [3] the ablation toy (seed 7, then seeds 1..20): month-month entries zeroed, top-6 eigendirections, circular score by number S of seasonal words
  [4] the page: prints these numbers; says the paper was only partly read; says nothing was run on a real corpus; no Lean file; does not claim
      that large models have no world model
QUOTED, NOT CHECKED: everything about the paper itself (arXiv:2602.15029v3). NOT A SOURCE FOR: any real corpus, any trained model."""
import math, cmath, re, sys, html as H
from pathlib import Path
HERE=Path(__file__).resolve().parent
fails=[]
def check(ok,msg):
    print('    %s  %s'%('PASS' if ok else 'FAIL',msg))
    if not ok: fails.append(msg)
def head(n,t): print('\n'+'='*70+'\n  [%s]  %s\n'%(n,t)+'='*70)
import math, cmath
def jacobi(A, tol=1e-12, maxsweep=100):
    n=len(A); A=[r[:] for r in A]; V=[[1.0 if i==j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(maxsweep):
        off=sum(A[i][j]**2 for i in range(n) for j in range(i+1,n))
        if off<tol: break
        for p in range(n-1):
            for q in range(p+1,n):
                if abs(A[p][q])<1e-300: continue
                th=(A[q][q]-A[p][p])/(2*A[p][q]); t=(1 if th>=0 else -1)/(abs(th)+math.sqrt(th*th+1))
                c=1/math.sqrt(t*t+1); s=t*c
                for k in range(n):
                    akp,akq=A[k][p],A[k][q]; A[k][p]=c*akp-s*akq; A[k][q]=s*akp+c*akq
                for k in range(n):
                    apk,aqk=A[p][k],A[q][k]; A[p][k]=c*apk-s*aqk; A[q][k]=s*apk+c*aqk
                for k in range(n):
                    vkp,vkq=V[k][p],V[k][q]; V[k][p]=c*vkp-s*vkq; V[k][q]=s*vkp+c*vkq
    w=[A[i][i] for i in range(n)]
    order=sorted(range(n),key=lambda i:-w[i])
    return [w[i] for i in order],[[V[k][i] for k in range(n)] for i in order]  # eigvals desc, eigvecs as rows
class LCG:
    def __init__(s,seed): s.x=seed
    def u(s): s.x=(1103515245*s.x+12345)%2**31; return s.x/2**31
def circ_corr(theta):  # best over reflection of |mean exp(i(theta_m - 2 pi m/12))|
    n=len(theta); best=0
    for sgn in (1,-1):
        z=sum(cmath.exp(1j*(theta[m]-sgn*2*math.pi*m/n)) for m in range(n))/n
        best=max(best,abs(z))
    return best
def pca2(rows):
    n=len(rows); d=len(rows[0]); mu=[sum(r[j] for r in rows)/n for j in range(d)]
    X=[[r[j]-mu[j] for j in range(d)] for r in rows]
    C=[[sum(X[i][a]*X[i][b] for i in range(n))/n for b in range(d)] for a in range(d)]
    w,V=jacobi(C)
    return [[sum(X[i][j]*V[c][j] for j in range(d)) for c in (0,1)] for i in range(n)],w

head(1,'the month ring')
n=12; sigma=2.5
f=lambda d: math.exp(-min(d%n,(-d)%n)/sigma)
C=[[f(i-j) for j in range(n)] for i in range(n)]
lam=[sum(f(d)*math.cos(2*math.pi*k*d/n) for d in range(n)) for k in range(n)]
err=0
for k in range(n):
    v=[cmath.exp(2j*math.pi*k*j/n) for j in range(n)]
    Cv=[sum(C[i][j]*v[j] for j in range(n)) for i in range(n)]
    err=max(err,max(abs(Cv[i]-lam[k]*v[i]) for i in range(n)))
print('    max |C v_k - lambda_k v_k| = %.2e'%err); check(err<1e-12,'Fourier vectors are eigenvectors, error < 1e-12')
print('    lambda_0..6 =',[round(x,4) for x in lam[:7]]); check(min(lam)>0,'all eigenvalues positive (so a real embedding W with W W^T = C exists)')
w,V=jacobi(C)
W=[[math.sqrt(max(w[c],0))*V[c][i] for c in range(n)] for i in range(n)]
g=max(abs(sum(W[i][c]*W[j][c] for c in range(n))-C[i][j]) for i in range(n) for j in range(n))
print('    max Gram error %.2e'%g); check(g<1e-7,'W W^T reproduces C to < 1e-7')
P,pw=pca2(W)
rad=[math.hypot(*p) for p in P]; th=[math.atan2(p[1],p[0]) for p in P]
spread=max(rad)-min(rad); print('    radius spread %.2e, top PCA variances %.4f %.4f, third %.4f'%(spread,pw[0],pw[1],pw[2]))
check(spread<1e-7,'all twelve months at equal radius (spread < 1e-7)')
check(abs(pw[0]-pw[1])<1e-9,'top two principal variances equal (cos and sin share one eigenvalue)')
d=[(th[(m+1)%n]-th[m])%(2*math.pi) for m in range(n)]
sgn=1 if d[0]<math.pi else -1
steps=[(x if sgn==1 else 2*math.pi-x) for x in d]
check(max(abs(s-2*math.pi/12) for s in steps)<1e-6,'consecutive months are 30 degrees apart, in calendar order')
check(circ_corr(th)>1-1e-9,'circular score = 1')
E2=[[math.sqrt(w[c])*V[c][i] for c in range(2)] for i in range(n)]
Ru=circ_corr([math.atan2(e[1],e[0]) for e in E2]); print('    uncentered top-2 circular score %.3f'%Ru)
check(Ru<0.5,'uncentered top-2 components do NOT form the circle (the failed first attempt on the page)')

head(2,'open ends (Toeplitz)')
N=30; s=6.0
K=[[math.exp(-abs(i-j)/s) for j in range(N)] for i in range(N)]
wo,Vo=jacobi(K); sch=lambda v: sum(1 for a,b in zip(v,v[1:]) if a*b<0)
sc=[sch(Vo[c]) for c in range(6)]; print('    top eigenvalues',[round(x,3) for x in wo[:6]],' sign changes',sc)
check(sc==[0,1,2,3,4,5],'first six eigenvectors have 0,1,2,3,4,5 sign changes')
Wo=[[math.sqrt(max(wo[c],0))*Vo[c][i] for c in range(N)] for i in range(N)]
Po,_=pca2(Wo); ax1=[p[0] for p in Po]
mono=all(a<b for a,b in zip(ax1,ax1[1:])) or all(a>b for a,b in zip(ax1,ax1[1:]))
print('    first centered axis monotone in year order:',mono)
check(mono is False,'NEGATIVE RESULT stands: the first centered axis is not monotone (page says so; if this becomes True, edit the page)')

head(3,'the ablation toy')
def toy(S,B=20,seed=7,noise=0.05,d=6,ablate=True):
    r=LCG(seed); nn=12
    ph=[2*math.pi*m/12 for m in range(nn)]+[2*math.pi*r.u() for _ in range(S)]
    amp=[1.0]*nn+[0.6+0.8*r.u() for _ in range(S)]
    Vn=nn+S+B; M=[[0.0]*Vn for _ in range(Vn)]
    for i in range(Vn):
        for j in range(i,Vn):
            v=amp[i]*amp[j]*math.cos(ph[i]-ph[j]) if (i<nn+S and j<nn+S) else 0.0
            v+=noise*(r.u()-0.5); M[i][j]=M[j][i]=v
    if ablate:
        for i in range(nn):
            for j in range(nn): M[i][j]=0.0
    wv,Vv=jacobi(M); idx=sorted(range(Vn),key=lambda i:-abs(wv[i]))[:d]
    Wm=[[math.sqrt(abs(wv[c]))*Vv[c][i] for c in idx] for i in range(nn)]
    Pm,_=pca2(Wm); return circ_corr([math.atan2(p[1],p[0]) for p in Pm])
Ss=(0,1,2,3,5,10,40); tab=[(S,toy(S),toy(S,ablate=False)) for S in Ss]
for S,a,b in tab: print('    S=%2d  ablated %.3f   not ablated %.3f'%(S,a,b))
check(tab[0][1]<0.5,'S=0: no circle once month-month entries are removed')
check(tab[1][1]<0.8,'S=1: one seasonal word cannot fix a circle (months fall on a line)')
check(all(a>0.99 for S,a,b in tab if S>=2),'S>=2: circle recovered (score > 0.99) at seed 7')
check(all(b>0.999 for S,a,b in tab),'nothing removed: score ~ 1 for every S')
sweep={S:[toy(S,seed=sd) for sd in range(1,21)] for S in (1,2,3,5,10)}
for S,v in sweep.items(): print('    S=%2d  min %.3f  median %.3f  >=0.95: %d of 20'%(S,min(v),sorted(v)[10],sum(x>=0.95 for x in v)))
check(sum(x>=0.95 for x in sweep[1])==0 and all(sum(x>=0.95 for x in sweep[S])==20 for S in (2,3,5,10)),'over 20 seeds: S=1 never reaches 0.95, S>=2 always does')

head(4,'the page')
pg=HERE/'ch02-embedding-geometry.html'
if not pg.exists(): print('    SKIP  page not found beside this script')
else:
    txt=H.unescape(re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',re.sub(r'<style>.*?</style>|<script>.*?</script>','',pg.read_text(encoding='utf-8'),flags=re.S))))
    for k in range(7): check('%.4f'%lam[k] in txt,'page shows lambda_%d = %.4f'%(k,lam[k]))
    check('%.4f'%pw[0] in txt and '%.4f'%pw[2] in txt,'page shows PCA variances %.4f and %.4f'%(pw[0],pw[2]))
    check('%.3f'%Ru in txt,'page shows the uncentered score %.3f'%Ru)
    check(', '.join('%.3f'%x for x in wo[:6]) in txt,'page shows the six open-end eigenvalues')
    for S,a,b in tab: check('%.3f'%a in txt and '%.3f'%b in txt,'page shows the S=%d row'%S)
    for S,v in sweep.items(): check('%.3f'%min(v) in txt and '%.3f'%sorted(v)[10] in txt,'page shows the S=%d sweep row'%S)
    check('negative result' in txt.lower() and 'false' in txt,'page states the monotone test came out false')
    check('real corpus' in txt and 'no Lean file' in txt,'page says nothing was run on a real corpus and that there is no Lean file')
    check('does not show that large models build no internal world model' in txt,'page does not claim large models have no world model')
    check('2602.15029' in txt,'page cites arXiv:2602.15029')
    idx=(HERE/'index.html'); 
    if idx.exists(): check('ch02-embedding-geometry.html' in idx.read_text(encoding='utf-8'),'Book XVI contents lists this chapter')
print('\n%s'%('ALL CHECKS PASSED' if not fails else 'FAILED: %d'%len(fails)))
sys.exit(1 if fails else 0)
