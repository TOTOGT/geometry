"""Independent numerical test of the symbolic Taylor family (nodal_taylor.py) on the REAL Eisenstein function
f(x+iy)=E*(z,1/2+i t1)=xi(2s)y^s+xi(2s-1)y^(1-s)+4 sqrt(y) sum n^(s-1/2) sigma_{1-2s}(n) K_{s-1/2}(2 pi n y) cos(2 pi n x), t1 = first zeta zero.
(here F(t1)=f(i) ~ 2Lambda_{Q(i)}(1/2+i t1)=0 up to the 10-digit t1, so c00 ~ 1e-10, treated as 0.)
Compares measured Taylor coefficients c_{jk}=d^j_x d^k_v f/(j!k!) with those predicted from (mu, a, c40)."""
from mpmath import mp, mpf, mpc, zeta, gamma, pi, besselk, cos, sqrt, diff, factorial, nstr, fabs
import sympy as sp, importlib.util, sys, io, contextlib
mp.dps=30
t1=mpf('14.134725141734693790457251983562')
s=mpf(1)/2+1j*t1; NN=14
def sig(n,a): return sum(mpf(d)**a for d in range(1,n+1) if n%d==0)
xi=lambda w: pi**(-w/2)*gamma(w/2)*zeta(w)
c0,c1=xi(2*s),xi(2*s-1)
co=[mpf(n)**(s-0.5)*sig(n,1-2*s) for n in range(1,NN+1)]
def f(x,v):
    y=1+v
    return c0*y**s+c1*y**(1-s)+4*sqrt(y)*sum(co[n-1]*besselk(s-0.5,2*pi*n*y)*cos(2*pi*n*x) for n in range(1,NN+1))
def c(j,k): return diff(f,(0,0),(j,k))/(factorial(j)*factorial(k)) if j+k>0 else f(0,0)
meas={(j,k):c(j,k) for j in range(0,5) for k in range(0,5-j)}
print("c00 (should be ~0):",nstr(meas[(0,0)],5))
# symbolic family
x,v,mu=sp.symbols('x v mu'); N=4
cs={(j,k):sp.Symbol(f'c{j}{k}') for j in range(N+1) for k in range(N+1-j)}
F=sum(cc*x**j*v**k for (j,k),cc in cs.items())
eqs=[]
E=sp.expand((1+v)**2*(sp.diff(F,x,2)+sp.diff(F,v,2))-mu*F); eqs+=[co_ for (a_,b_),co_ in sp.Poly(E,x,v).terms() if a_+b_<=N-2]
eqs+=[cs[(j,k)] for (j,k) in cs if j%2==1]
r2=x**2+(1+v)**2; t=sp.symbols('t')
ser=lambda e: sp.series(e.subs({x:t*x,v:t*v}),t,0,N+1).removeO().subs(t,1)
X=ser(-x/r2); V=ser((1+v)/r2-1)
Fs=sp.expand(sum(cc*X**j*V**k for (j,k),cc in cs.items()))
eqs+=[co_ for (a_,b_),co_ in sp.Poly(Fs-F,x,v).terms() if a_+b_<=N]
sol=sp.solve(eqs+[cs[(0,0)]],list(cs.values()),dict=True)[0]
mu_num=complex(s*(s-1)); 
free=[q for q in cs.values() if q not in sol]
print("free symbols:",free)
a_meas=2*meas[(2,0)]
# determine free params from measured c20 and c40
subs={mu:mu_num}
c20=sol[cs[(2,0)]]; c40=cs[(4,0)] if cs[(4,0)] not in sol else sol[cs[(4,0)]]
# solve the 2 free symbols from measured c20,c40
fs=[q for q in free if q!=cs[(0,0)]]
eq=[sp.Eq(sp.sympify(c20).subs(subs),complex(meas[(2,0)])), sp.Eq(sp.sympify(c40).subs(subs),complex(meas[(4,0)]))]
vals=sp.solve(eq,fs,dict=True)[0]
mx=0
for (j,k),cc in cs.items():
    if j+k==0: continue
    pred=complex(sp.sympify(sol.get(cc,cc)).subs(subs).subs(vals))
    m=complex(meas[(j,k)]); err=abs(pred-m)/(abs(m)+1e-8)
    if (j,k) not in [(2,0),(4,0)]: mx=max(mx,abs(pred-m)/(abs(meas[(2,0)])+abs(meas[(4,0)])))
    print(f"c{j}{k}: measured {m:.6e}   predicted {pred:.6e}")
print("max |pred-meas| / (|c20|+|c40|) over non-input coefficients:",mx)
print("RESULT:", "consistent" if mx<1e-6 else "MISMATCH")
