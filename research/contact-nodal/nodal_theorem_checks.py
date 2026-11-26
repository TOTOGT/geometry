"""Checks accompanying the standalone quartic nodal theorem (NODAL-THEOREM.md).
(1) symbolic: with f(i)=0 and a=0 the degree-4 part forced by (E),(P),(S) is exactly c40*(x^4-6x^2v^2+v^4)=c40*Re(x+iv)^4  (for mu != 10)
(2) harmonic classification: homogeneous harmonic polys of degree k in 2 variables = span{Re w^k, Im w^k}; evenness in x and
    the sigma-differential -Id leave exactly alpha*Re w^k with k even  (symbolic for k<=8)
(3) numeric: for the truncated family (a=0) f = c40*Re w^4 + degree-5 part + degree-6 remainder (random remainder), the zero set on circles of radius rho
    has exactly 2k=8 sign changes -> 4 curves, with root angles within O(rho) of pi/8 + j*pi/4."""
import sympy as sp, numpy as np
x,v=sp.symbols('x v',real=True); mu,c40,c41=sp.symbols('mu c40 c41'); w=x+sp.I*v
# (1) reuse degree-4/5 output of nodal_taylor.py family (N=5)
d4=(-7*c40*mu*v**4+12*c40*mu*v**2*x**2+3*c40*mu*x**4-30*c40*v**4+180*c40*v**2*x**2-30*c40*x**4-c41*mu*v**4+3*c41*mu*v**2*x**2)/(3*(mu-10))
d5=v*(14*c40*mu*v**4-50*c40*mu*v**2*x**2+2*c41*mu*v**4-11*c41*mu*v**2*x**2+3*c41*mu*x**4-6*c41*v**4+60*c41*v**2*x**2-30*c41*x**4)/(3*(mu-10))
res=sp.simplify(d4.subs(c41,-10*c40)-c40*sp.re(sp.expand(w**4)))
print("(1) degree-4 with a=0 minus c40*Re w^4 =",res,"  PASS" if res==0 else "  FAIL")
print("    degree-5 with a=0:",sp.factor(sp.simplify(d5.subs(c41,-10*c40))))
# (2) classification, k<=8
ok=True
for k in range(1,9):
    a_,b_=sp.symbols('a_ b_'); P=a_*sp.re(sp.expand(w**k))+b_*sp.im(sp.expand(w**k))
    harm=sp.simplify(sp.diff(P,x,2)+sp.diff(P,v,2))==0
    ev=sp.expand(P.subs(x,-x)-P); sol_ev=sp.solve(sp.Poly(ev,x,v).coeffs(),[a_,b_],dict=True)
    # sigma: w->-w at leading order: P(-w)=P(w)
    ev2=sp.expand(P.subs({x:-x,v:-v})-P); sol_s=sp.solve(sp.Poly(ev2,x,v).coeffs(),[a_,b_],dict=True) if ev2!=0 else [{}]
    allowed = (k%2==0)
    both=(sol_ev and sol_ev[0].get(b_,None)==0) if k%2==0 else (sol_ev and sol_ev[0].get(a_,None)==0)
    # after evenness for odd k the survivor beta*Im w^k is odd under w->-w, so killed by sigma
    surv_s = (P.subs({a_:1,b_:0}).subs({x:-x,v:-v})-P.subs({a_:1,b_:0})==0) if k%2==0 else (P.subs({a_:0,b_:1}).subs({x:-x,v:-v})-P.subs({a_:0,b_:1})==0)
    ok&= bool(harm and both and (surv_s==allowed))
    print(f"(2) k={k}: harmonic={harm}, even-in-x keeps {'Re' if k%2==0 else 'Im'} w^k, survives w->-w: {surv_s}")
print("(2)","PASS" if ok else "FAIL")
# (3) numeric sign-change count
rng=np.random.default_rng(1); passed=True
for trial in range(5):
    c=rng.normal(); m=-(0.25+rng.uniform(1,300)**2)   # mu = -(1/4+t^2) critical line
    f4=lambda X,V: c*(X**4-6*X**2*V**2+V**4)
    r5=rng.normal(size=3); r6=rng.normal(size=4)
    def f(X,V,rho):
        d5=sum(r5[i]*X**(5-i)*V**i for i in range(3)) ; d6=sum(r6[i]*X**(6-i)*V**i for i in range(4))
        return f4(X,V)+d5+d6
    for rho in (0.05,0.01):
        th=np.linspace(0,2*np.pi,20001)[:-1]; X=rho*np.cos(th); V=rho*np.sin(th)
        val=f(X,V,rho); sc=np.sum(np.sign(val)!=np.sign(np.roll(val,-1)))
        roots=th[np.where(np.sign(val)!=np.sign(np.roll(val,-1)))[0]]
        dev=max(min(abs(((t-(np.pi/8+j*np.pi/4))+np.pi)%(2*np.pi)-np.pi) for j in range(8)) for t in roots)
        passed&=(sc==8)
        print(f"(3) trial {trial} rho={rho}: sign changes={sc} (expected 8), max angle deviation from pi/8+j pi/4 = {dev:.3f} rad")
print("(3)","PASS" if passed else "FAIL")
