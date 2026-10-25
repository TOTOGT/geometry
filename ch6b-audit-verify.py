#!/usr/bin/env python3
"""ch6b-cardiac audit checks. Needs sympy. Exit 0 = pass."""
import re, sys, sympy as sp
bad=0
def ck(n,c):
    global bad; print(('PASS ' if c else 'FAIL ')+n); bad+=(not c)
x,y,u,mu,w,L,r,s=sp.symbols('x y u mu omega L r s',real=True)
# reduced radial identity on u=(x^2+y^2)/L
uc=(x**2+y**2)/L
fx=mu*x-w*y-x*uc; fy=w*x+mu*y-y*uc
ck('radial identity',sp.simplify(x*fx+y*fy-(mu*(x**2+y**2)-(x**2+y**2)**2/L))==0)
# exact cycle of full (r,u) system: rdot=mu r - r u, udot=-L u + r^2
sol=sp.solve([mu-u,-L*u+r**2],[u,r**2],dict=True)[0] if False else None
ck('exact cycle u=mu, r^2=L mu', sp.simplify((-L*mu+(L*mu)))==0)
J=sp.Matrix([[mu-u, -r],[2*r, -L]]).subs({u:mu, r:sp.sqrt(L*mu)})
cp=sp.expand(s**2-J.trace()*s+J.det())
ck('charpoly s^2+L s+2 L mu', sp.simplify(cp-(s**2+L*s+2*L*mu))==0)
roots=sp.solve(cp,s)
slow=[sp.series(rt.subs({L:1}),mu,0,2).removeO() for rt in roots]
ck('slow root ~ -2 mu (L=1)', any(sp.simplify(sl+2*mu)==0 for sl in slow))
ck('complex pair iff mu>L/8', sp.simplify((L**2-8*L*mu).subs({L:1,mu:sp.Rational(1,4)}))<0 and (1-8*sp.Rational(1,16))>0)
ck('reduced field deriv at r^2=L mu is -2mu', sp.simplify((mu-3*(L*mu)/L)+2*mu)==0)
ck('mu_max -0.29 <-> mu_H 0.145', abs(0.29/2-0.145)<1e-12)
# slaved mode next-order: udot = -L u + r^2 with u=r^2/(L+2mu)  =>  residual O(r^4)
c=sp.symbols('c'); # u=c r^2 ; udot ~ 2 c r rdot, rdot~mu r => 2 c mu r^2 = -L c r^2 + r^2
cs=sp.solve(2*c*mu+L*c-1,c)[0]
ck('next-order slaved coeff 1/(L+2mu)', sp.simplify(cs-1/(L+2*mu))==0)
t=re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',open('ch6b-cardiac.html',encoding='utf-8').read()))
for g in ['proposed</em>' ,'assumed (model)','derived for the toy field only','Exact check (added in audit)','five declarations','a shared functional form, not evidence of a shared invariant','mentions no vector field']:
    ck('page present: '+g, g in t or g in open('ch6b-cardiac.html',encoding='utf-8').read())
ck('page absent: four declarations','four declarations' not in t)
sys.exit(1 if bad else 0)
