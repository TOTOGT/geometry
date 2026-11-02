#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gcm-theorems-AD-audit.py -- audit of statements on gcm-framework.html (Theorems A-D, Def 3.1, section 4). Written 2026-11-02.
RECOMPUTED here (sympy, hand-derived first): (1) the page's identity for alpha ^ (d alpha)^n; (2) whether the Theorem C 'normal form'
vector field, and the section-4 version of it, is a contact vector field of alpha = dz - rho^2 dtheta; (3) the dimension count behind
Definition 3.1 (alpha_12 = alpha_1 + alpha_2); (4) a counterexample to tau_12 <= min(tau_1, tau_2) under Definition 3.1 with the natural
single-system tau = |mu|/kappa; (5) the epsilon_0 = 1/3 arithmetic.
NOT DONE: no proof of A(i), A(iii), Prop 6.1 or the iff in Theorem B was found on the page, so none is checked; nothing is formalized.
SCOPE: audits what the page states; does not edit the page. 'Contact' tests assume alpha_normal = dz - rho^2 dtheta (Axioms 5-6), because the
Theorem C statement never defines alpha_normal -- itself a finding."""
import itertools, sys
import sympy as sp
fails=[]
def check(ok,msg,detail=''):
    print('    %s  %s%s'%('PASS' if ok else 'FAIL',msg,('  -- '+detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def info(msg): print('    INFO  '+msg)
def head(n,t): print('\n'+'='*70+'\n  [%s]  %s\n'%(n,t)+'='*70)

# ---- tiny exterior algebra: a form is {sorted index tuple: coeff}
def wedge(a,b):
    out={}
    for ia,ca in a.items():
        for ib,cb in b.items():
            if set(ia)&set(ib): continue
            idx=ia+ib; perm=sorted(range(len(idx)),key=lambda k:idx[k])
            # sign of permutation
            sgn=1; seen=[False]*len(idx)
            for i in range(len(idx)):
                if not seen[i]:
                    j=i; L=0
                    while not seen[j]: seen[j]=True; j=perm[j]; L+=1
                    if L%2==0: sgn=-sgn
            key=tuple(sorted(idx)); out[key]=sp.simplify(out.get(key,0)+sgn*ca*cb)
    return {k:v for k,v in out.items() if v!=0}
def d(form,xs):
    out={}
    for idx,c in form.items():
        for k,x in enumerate(xs):
            if k in idx: continue
            t=wedge({(k,):sp.diff(c,x)},{idx:1})
            for kk,vv in t.items(): out[kk]=sp.simplify(out.get(kk,0)+vv)
    return {k:v for k,v in out.items() if v!=0}

head(1,'the page: alpha ^ (d alpha)^n = (-1)^{n(n+1)/2} lambda ^ omega^n  (section 4)')
# n = 1: M = R^2 (x,y), lambda = (x dy - y dx)/2, omega = d lambda = dx^dy;  M-hat = R^3 (x,y,z)
x,y,z=sp.symbols('x y z'); X=[x,y,z]
lam={(1,):x/2,(0,):-y/2}; alpha={(2,):1}
for k,v in lam.items(): alpha[k]=-v
da=d(alpha,X); a_da=wedge(alpha,da); lam_om=wedge(lam,d(lam,X))
print('    n=1: alpha^dalpha =',a_da,'   lambda^omega =',lam_om)
check(a_da=={(0,1,2):-1},'alpha^dalpha = -dx^dy^dz (nonzero, as a contact form should)')
check(lam_om=={},'lambda^omega is identically 0 on M-hat: it is a 3-form pulled back from a 2-manifold')
check(not (lam_om!={}),'the page\'s right-hand side (-1)^{n(n+1)/2} lambda^omega^n therefore equals 0, not a nonzero volume form')
# n = 2: M = R^4
x1,y1,x2,y2,z2=sp.symbols('x1 y1 x2 y2 z2'); X4=[x1,y1,x2,y2,z2]
lam4={(1,):x1/2,(0,):-y1/2,(3,):x2/2,(2,):-y2/2}; al4={(4,):1}
for k,v in lam4.items(): al4[k]=-v
dal=d(al4,X4); vol=wedge(al4,wedge(dal,dal)); om=d(lam4,X4); lam_om2=wedge(lam4,wedge(om,om))
check(lam_om2=={},'n=2: lambda^omega^2 is identically 0 on M-hat as well')
omn=wedge(om,om); dz_om=wedge({(4,):1},omn)
check(vol==({k:sp.simplify(((-1)**2)*v) for k,v in dz_om.items()}),'n=2: alpha^(dalpha)^2 = (-1)^n dz ^ omega^n')
info('correct identity: alpha ^ (d alpha)^n = (-1)^n dz ^ omega^n (n=1,2 checked; general n follows by the same expansion)')

head(2,"Theorem C 'normal form' vs contact vector fields of alpha = dz - rho^2 dtheta  (coordinates rho, theta, z)")
r,t,zz,mu,w,b=sp.symbols('rho theta z mu omega beta',real=True); C=[r,t,zz]
al={(2,):1,(1,):-r**2}
dal=d(al,C)                                   # -2 rho drho^dtheta
def lie(Xv):
    # L_X alpha = i_X d alpha + d(i_X alpha), as coefficient vectors on (drho,dtheta,dz)
    s=sp.simplify(Xv[2]-r**2*Xv[1])           # i_X alpha
    ds=[sp.diff(s,c) for c in C]
    # d alpha = -2 rho drho^dtheta ; i_X (drho^dtheta) = X^rho dtheta - X^theta drho
    ix=[2*r*Xv[1], -2*r*Xv[0], 0]
    return [sp.simplify(ds[i]+ix[i]) for i in range(3)]
def is_contact(Xv):
    L=lie(Xv); a=[0,-r**2,1]
    cr=[sp.simplify(L[1]*a[2]-L[2]*a[1]),sp.simplify(L[2]*a[0]-L[0]*a[2]),sp.simplify(L[0]*a[1]-L[1]*a[0])]
    return all(c==0 for c in cr),L
absmu=sp.Symbol('m',positive=True)
fields={
 'control: Reeb field d_z':[0,0,1],
 'control: d_theta':[0,1,0],
 'control: rho d_rho + 2 z d_z (dilation, L alpha = 2 alpha)':[r,0,2*zz],
 'Theorem C field (rho_dot=-m(1-e^{-bz})rho, theta_dot=w, z_dot=w)':[-absmu*(1-sp.exp(-b*zz))*r,w,w],
 'section-4 field (z_dot = w - m rho^2 e^{-bz}), leading terms':[-absmu*(1-sp.exp(-b*zz))*r,w,w-absmu*r**2*sp.exp(-b*zz)],
}
res={}
for name,Xv in fields.items():
    ok,L=is_contact(Xv); res[name]=ok; print('    %s -> contact: %s ; L_X alpha = %s'%(name,ok,L))
check(res['control: Reeb field d_z'] and res['control: d_theta'] and res['control: rho d_rho + 2 z d_z (dilation, L alpha = 2 alpha)'],'the test accepts the three known contact fields (controls)')
check(not res[list(fields)[3]],"Theorem C's field is NOT a contact vector field of dz - rho^2 dtheta (L_X alpha has no dz part, so f=0, but it is not 0)")
check(not res[list(fields)[4]],"the section-4 version (with the z_dot correction) is NOT a contact vector field of dz - rho^2 dtheta either")
info('hand check: L_X alpha for the Theorem C field is -2 rho rho_dot dtheta, which is a multiple of alpha only if rho*rho_dot = 0')
info('so no contact Hamiltonian H generates either field for this alpha; the statement needs a different alpha_normal, which the theorem never defines')

head(3,'Definition 3.1: alpha_12 = alpha_1 + alpha_2')
for n1,n2 in ((1,1),(1,2),(2,3)):
    dim=(2*n1+1)+(2*n2+1)
    top=2*(n1+n2)+3   # degree of (alpha)^(d alpha)^k with k=(dim-1)/2 would need dim odd
    print('    M-hat_1 x M-hat_2 with n1=%d,n2=%d: dimension %d (even)'%(n1,n2,dim))
    check(dim%2==0,'dimension %d is even, so no contact form exists on it (a contact manifold is odd-dimensional)'%dim)
info('the page says X_12 lives on M_1 x M_2 (bases, dimension 2n1+2n2, even) but alpha_i lives on M_i x R; the sum alpha_1+alpha_2 is not defined there')
info('a single-z version (dz - lambda_1 - lambda_2 on (M_1 x M_2) x R) would be contact, but that is a different definition from the stated one')

head(4,'Theorem B: tau_12 <= min(tau_1, tau_2), with tau_12 = sqrt(mu1^2+mu2^2)/max(kappa1,kappa2) (Definition 3.1)')
import math
def tau(m,k): return abs(m)/k            # natural single-system analogue (mu2 -> 0 recovers it); ASSUMPTION
for m1,k1,m2,k2 in ((1,1,1,1),(2,1,1,1),(1,2,1,2)):
    t12=math.sqrt(m1**2+m2**2)/max(k1,k2); mn=min(tau(m1,k1),tau(m2,k2))
    print('    mu=(%g,%g) kappa=(%g,%g): tau_12=%.4f, min(tau)=%.4f'%(m1,m2,k1,k2,t12,mn))
check(math.sqrt(2)/1>1,'mu=(1,1), kappa=(1,1): tau_12 = sqrt2 > min(tau_1,tau_2) = 1: the stated inequality fails')
info('depends on the assumption tau_i = |mu_i|/kappa_i; the page does not define tau_i for one system in Theorem B (Vol II uses sqrt(c/kappa) -- log 2026-09-30, a different formula)')
info('the "equality iff g-orthogonal Lyapunov functions" clause has no proof on the page and no formula connecting g-orthogonality to tau')

head(5,'Theorem D arithmetic and statement type')
check(sp.Rational(2,2*(1+2))==sp.Rational(1,3),'toy model: 2 / (2*(1+2)) = 1/3')
info("'the operator algebra (G,U,F,K,C) is C^1-structurally stable' is a category error: structural stability is a property of a vector field or flow, not of an algebra")
info('the page gives no derivation of epsilon_0; Prop 6.1 states a bound with the same factor and no proof; log 2026-09-30 already found the inner/outer basin mismatch')

head(6,'Theorem C classification clause (not computed)')
info("'(mu,omega,beta) are contact invariants that classify the local contact geometry up to contact diffeomorphism': by the standard neighbourhood theorem")
info('for transverse (and Legendrian) curves in contact 3-manifolds (Geiges, An Introduction to Contact Topology; from memory, to confirm), the germ of the')
info("contact structure near the curve is standard, so it cannot carry parameters like mu or beta. These are invariants of the vector field xi, not of alpha.")

print('\nALL PASS (every check above passed; INFO lines are findings or open items)' if not fails else '\nFAILED: %d'%len(fails)); sys.exit(1 if fails else 0)
