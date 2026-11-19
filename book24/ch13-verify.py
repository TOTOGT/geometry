#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book24/ch13-verify.py -- every check behind book24/ch13-circulant-matrices.html. Run first.   python3 book24/ch13-verify.py
Standard library only. Written 2026-11-19; not run by anyone but its author until you run it. Nothing here proves a theorem; the proofs are on the page.

  [1] C_ij = c_((i-j) mod n): every integer circulant with entries -3..3 for n = 3 and n = 4 (343 and 2401 matrices, exhaustive) and 300
      pseudo-random ones for n = 5..12: the Fourier vector v_j = w^(jk), w = exp(2 pi i / n), is an eigenvector with eigenvalue
      lambda_k = sum_d c_d w^(-dk); worst error printed (tolerance 1e-9)
  [2] the cyclic shift S has the n distinct eigenvalues w^(-k) (n = 2..12): pairwise distances printed
  [3] normality: C C^T = C^T C exactly (integers) for all circulants in [1] with n = 3, 4; the 2-norm equals max |lambda_k| for 300 samples
      (largest eigenvalue of C^T C by a Jacobi sweep; tolerance 1e-9)
  [4] symmetric circulants have lambda_k = lambda_(n-k) (so the eigenspaces for 0<k<n/2 are two-dimensional: a cosine and a sine)
  [5] the ring of masses: c = (2,-1,0,..,0,-1) has lambda_k = 4 sin^2(pi k / n) for n = 3..12; the frequencies 2 sqrt(K/m) |sin(pi k/n)|
  [6] the month kernel of Book XVI, Chapter 2: f(d) = exp(-dc/2.5), n = 12; lambda_0..6; lambda_k decreasing for k = 1..6 (so k = 1 is the dominant non-constant mode)
  [7] a nonlinear example: the ring of n = 8 Kuramoto-type oscillators, thetadot_i = K [sin(theta_(i+1)-theta_i) + sin(theta_(i-1)-theta_i)]; the Jacobian at the
      synchronised state (all theta equal), by central differences, is the circulant (-2K, K, 0, .., 0, K); its eigenvalues are -4K sin^2(pi k/n)
  [8] the page: shows the numbers above, states the sign convention, says there is no Lean file, and does not claim a shared invariant
"""
import cmath, math, itertools, re, sys, html as H
from pathlib import Path
HERE=Path(__file__).resolve().parent
fails=[]
def check(ok,msg):
    print('    %s  %s'%('PASS' if ok else 'FAIL',msg))
    if not ok: fails.append(msg)
def head(n,t): print('\n'+'='*70+'\n  [%s]  %s\n'%(n,t)+'='*70)
def circ(c): n=len(c); return [[c[(i-j)%n] for j in range(n)] for i in range(n)]
def matvec(M,v): return [sum(M[i][j]*v[j] for j in range(len(v))) for i in range(len(M))]
def lam_formula(c,k):
    n=len(c); w=cmath.exp(2j*math.pi/n); return sum(c[d]*w**(-d*k) for d in range(n))
def worst_err(c):
    n=len(c); C=circ(c); w=cmath.exp(2j*math.pi/n); e=0
    for k in range(n):
        v=[w**(j*k) for j in range(n)]; lam=lam_formula(c,k)
        Cv=matvec(C,v); e=max(e,max(abs(Cv[i]-lam*v[i]) for i in range(n)))
    return e
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
head(1,'Fourier vectors are eigenvectors of every circulant')
worst=0; count=0
for n in (3,4):
    for c in itertools.product(range(-3,4),repeat=n):
        worst=max(worst,worst_err(list(c))); count+=1
r=LCG(11)
for t in range(300):
    n=5+int(r.u()*8); c=[int(r.u()*7)-3 for _ in range(n)]; worst=max(worst,worst_err(c)); count+=1
print('    %d circulants, worst error %.2e'%(count,worst)); check(count==343+2401+300 and worst<1e-9,'eigenvector relation holds for all %d (error < 1e-9)'%count)
head(2,'the shift has n distinct eigenvalues')
for n in range(2,13):
    ev=[cmath.exp(-2j*math.pi*k/n) for k in range(n)]
    dmin=min(abs(ev[a]-ev[b]) for a in range(n) for b in range(a+1,n))
    check(dmin>1e-3,'n=%d: smallest gap between the n eigenvalues %.4f > 0'%(n,dmin))
head(3,'normality and the norm')
ok=True
for n in (3,4):
    for c in itertools.product(range(-3,4),repeat=n):
        C=circ(list(c)); Ct=[[C[j][i] for j in range(n)] for i in range(n)]
        A=[[sum(C[i][k]*Ct[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
        B=[[sum(Ct[i][k]*C[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
        if A!=B: ok=False
check(ok,'C C^T = C^T C exactly for all 343 + 2401 integer circulants (n = 3, 4)')
r=LCG(5); wn=0
for t in range(300):
    n=5+int(r.u()*8); c=[r.u()*6-3 for _ in range(n)]; C=circ(c)
    G=[[sum(C[k][i]*C[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    ev,_=jacobi(G,tol=1e-26); nrm=math.sqrt(max(ev))
    rho=max(abs(lam_formula(c,k)) for k in range(n)); wn=max(wn,abs(nrm-rho))
print('    worst |norm - max|lambda|| over 300 random real circulants = %.2e'%wn); check(wn<1e-9,'2-norm = max |lambda_k| (tolerance 1e-9)')
head(4,'symmetric circulants: paired eigenvalues')
r=LCG(3); worst=0
for t in range(100):
    n=12; h=[r.u()*4-2 for _ in range(n//2+1)]
    c=[h[min(d,n-d)] for d in range(n)]
    for k in range(1,n): worst=max(worst,abs(lam_formula(c,k)-lam_formula(c,n-k)))
check(worst<1e-12,'lambda_k = lambda_(n-k) for 100 symmetric circulants with n = 12 (worst difference %.1e)'%worst)
head(5,'the ring of masses')
worst=0
for n in range(3,13):
    c=[0.0]*n; c[0]=2; c[1]=-1; c[n-1]=-1
    for k in range(n):
        lam=lam_formula(c,k); worst=max(worst,abs(lam-4*math.sin(math.pi*k/n)**2))
check(worst<1e-12,'eigenvalues of circ(2,-1,0,..,0,-1) are 4 sin^2(pi k/n), n = 3..12 (worst error %.1e)'%worst)
n=12; ringrows=[(k,4*math.sin(math.pi*k/n)**2,math.sin(math.pi*k/n)) for k in range(7)]
print('    n=12:',[(k,round(a,4),round(b,4)) for k,a,b in ringrows])
head(6,'the month kernel of Book XVI Chapter 2')
n=12; f=lambda d: math.exp(-min(d%n,(-d)%n)/2.5); c=[f(d) for d in range(n)]
lam=[lam_formula(c,k).real for k in range(n)]
print('    lambda_0..6 =',[round(x,4) for x in lam[:7]])
check(abs(lam[1]-2.0833)<5e-5 and abs(lam[0]-4.6069)<5e-5,'lambda_0 = 4.6069 and lambda_1 = 2.0833 (agrees with the Book XVI table)')
check(all(lam[k]>lam[k+1] for k in range(1,6)),'lambda_1 > lambda_2 > ... > lambda_6: the dominant non-constant mode is k = 1')
head(7,'a nonlinear ring linearises to a circulant')
n=8; K=1.0
def rhs(th): return [K*(math.sin(th[(i+1)%n]-th[i])+math.sin(th[(i-1)%n]-th[i])) for i in range(n)]
th0=[0.3]*n; hh=1e-6; J=[[0.0]*n for _ in range(n)]
for j in range(n):
    a=th0[:]; b=th0[:]; a[j]+=hh; b[j]-=hh; fa=rhs(a); fb=rhs(b)
    for i in range(n): J[i][j]=(fa[i]-fb[i])/(2*hh)
Jc=circ([-2*K,K]+[0.0]*(n-3)+[K]); e=max(abs(J[i][j]-Jc[i][j]) for i in range(n) for j in range(n))
check(e<1e-6,'Jacobian at the synchronised state equals circ(-2K,K,0,..,0,K) (max entry difference %.1e)'%e)
worst=max(abs(lam_formula([-2*K,K]+[0.0]*(n-3)+[K],k)+4*K*math.sin(math.pi*k/n)**2) for k in range(n)); check(worst<1e-12,'its eigenvalues are -4K sin^2(pi k/n)')
head(8,'the page')
pg=HERE/'ch13-circulant-matrices.html'
if not pg.exists(): print('    SKIP  page not found beside this script')
else:
    txt=H.unescape(re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',re.sub(r'<style>.*?</style>|<script>.*?</script>','',pg.read_text(encoding='utf-8'),flags=re.S))))
    for k,a,b in ringrows: check('%.4f'%a in txt or k==0,'page shows 4 sin^2(pi*%d/12) = %.4f'%(k,a))
    for k in range(7): check('%.4f'%lam[k] in txt,'page shows lambda_%d = %.4f'%(k,lam[k]))
    check('343' in txt and '2401' in txt,'page states the exhaustive counts')
    check('no Lean file' in txt,'page says there is no Lean file')
    check('shared invariant' in txt,'page labels the shared form as not a shared invariant')
    check('w^{-dk}' in txt.replace(' ','') or 'ω' in txt,'page states the eigenvalue convention')
    idx=(HERE/'index.html')
    if idx.exists(): check('ch13-circulant-matrices.html' in idx.read_text(encoding='utf-8'),'Book XXIV contents lists this chapter')
print('\n%s'%('ALL CHECKS PASSED' if not fails else 'FAILED: %d'%len(fails)))
sys.exit(1 if fails else 0)
