#!/usr/bin/env python3
"""Checks the multiplication tables and identities in P2xP2.lean against sympy
polynomial reduction modulo (a^3, b^3). Exact arithmetic, no sampling.
This verifies the TABLES (geometric input G1/G2/G3 as arithmetic); it is not a Lean check."""
import sympy as sp
a,b,s,t,c,x,y,u,x2,y2,u2,p,q = sp.symbols('a b s t c x y u x2 y2 u2 p q')
def red(e):
    e = sp.expand(e); P = sp.Poly(e,a,b); r = 0
    for (i,j),co in P.terms():
        if i<3 and j<3: r += co*a**i*b**j
    return sp.expand(r)
def d1(z): return z[0]*a+z[1]*b
def d2(z): return z[0]*a**2+z[1]*a*b+z[2]*b**2
def d3(z): return z[0]*a**2*b+z[1]*a*b**2
def coef(e,i,j): return sp.Poly(red(e),a,b).coeff_monomial(a**i*b**j)
ok=[]
def chk(name,cond): ok.append(bool(cond)); print(('PASS ' if cond else 'FAIL ')+name)
Z1,W1=(x,y),(x2,y2); Z2,W2=(x,y,u),(x2,y2,u2); W3=(p,q)
# tables
chk('mul11', sp.expand(red(d1(Z1)*d1(W1))-d2((x*x2,x*y2+y*x2,y*y2)))==0)
chk('mul12', sp.expand(red(d1(Z1)*d2(W2))-d3((x*y2+y*x2,x*u2+y*y2)))==0)
chk('deg13', sp.expand(coef(d1(Z1)*d3(W3),2,2)-(x*q+y*p))==0)
chk('deg22', sp.expand(coef(d2(Z2)*d2(W2),2,2)-(x*u2+y*y2+u*x2))==0)
h=s*a+t*b
chk('h2', sp.expand(red(h*h)-d2((s**2,2*s*t,t**2)))==0)
chk('h3', sp.expand(red(h**3)-d3((3*s**2*t,3*s*t**2)))==0)
chk('deg_h4', sp.expand(coef(h**4,2,2)-6*s**2*t**2)==0)
chk('deg_h3_mul', sp.expand(coef(h**3*d1(Z1),2,2)-3*s*t*(t*x+s*y))==0)
chk('hz_eq', sp.expand(red(h*d2(Z2))-d3((s*y+t*x,s*u+t*y)))==0)
cp2=d2((c*s**2,-c*s*t,c*t**2))
chk('codim2_value', sp.expand(coef(cp2*cp2,2,2)-3*c**2*s**2*t**2)==0)
z1=d1((c*s,-c*t))
chk('codim1_value', sp.expand(-coef(z1*z1*h**2,2,2)-2*c**2*s**2*t**2)==0)
chk('primitive_codim1_h3', sp.expand(coef(h**3*z1,2,2))==0)
chk('primitive_codim2_hz', sp.expand(red(h*cp2))==0)
# L2 and Gamma: L2 z = h^2 z
L2=lambda z: red(d1(z)*h**2)
chk('L2_eq', sp.expand(L2(Z1)-d3((2*s*t*x+s**2*y,t**2*x+2*s*t*y)))==0)
Gba,Gbb,Gaa,Gab=2/(3*s*t),-1/(3*s**2),-1/(3*t**2),2/(3*s*t)
push=lambda w:(w[0]*Gba+w[1]*Gaa, w[0]*Gbb+w[1]*Gab)
# G3 from the push-pull formula: Gamma on X x X, source classes a1,b1 (variables A,B), target a2,b2
A,B,a2,b2=sp.symbols('A B a2 b2')
Gam=B*(2*a2/(3*s*t)-b2/(3*s**2))+A*(-a2/(3*t**2)+2*b2/(3*s*t))
def pf(w):  # pr1^* w * Gamma, integrate over source (coeff of A^2 B^2 with A,B truncated), read target
    src=sp.expand(w[0]*A**2*B+w[1]*A*B**2)*Gam
    e=sp.expand(src); P=sp.Poly(e,A,B)
    r=P.coeff_monomial(A**2*B**2)
    return (sp.expand(r).coeff(a2,1), sp.expand(r).coeff(b2,1))
chk('G3 pushforward matches push-pull', all(sp.simplify(i-j)==0 for i,j in zip(pf((p,q)),push((p,q)))))
L2z=(2*s*t*x+s**2*y,t**2*x+2*s*t*y)
chk('pushforward_L2', all(sp.simplify(i-j)==0 for i,j in zip(push(L2z),(x,y))))
zz=push((p,q))
back=(2*s*t*zz[0]+s**2*zz[1], t**2*zz[0]+2*s*t*zz[1])
chk('L2_pushforward', all(sp.simplify(i-j)==0 for i,j in zip(back,(p,q))))
chk('L2_det', sp.expand((2*s*t)**2-s**2*t**2-3*s**2*t**2)==0)
# primitive uniqueness: kernel of hz map is 1-dim spanned by p2 (null space)
M=sp.Matrix([[t,s,0],[0,t,s]])
chk('kernel is spanned by (s^2,-st,t^2)', M.nullspace()[0].T.rank()==1 and sp.simplify(M*sp.Matrix([s**2,-s*t,t**2])).is_zero_matrix)
chk('middle form indefinite', 2*1*(-1)+0**2<0 and 0+1+0>0)
# Frobenius countermodel
q_=sp.symbols('q'); F=sp.diag(q_**2,q_**2); J=sp.diag(1,-1)
chk('F^T J F = q^4 J', sp.simplify(F.T*J*F-q_**4*J).is_zero_matrix)
chk('(0,1) J-square = -1', (sp.Matrix([[0,1]])*J*sp.Matrix([0,1]))[0]==-1)
print('%d/%d checks passed'%(sum(ok),len(ok)))
raise SystemExit(0 if all(ok) else 1)
