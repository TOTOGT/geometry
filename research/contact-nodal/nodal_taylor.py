"""Exact local Taylor expansion of f(x+iy)=E*(z,s) at z=i, from three structural facts only:
 (E) y^2 (f_xx+f_yy) = mu f,  mu=s(s-1)   (Laplace eigen-equation, any complex s)
 (P) f(-x,y)=f(x,y)                        (evenness)
 (S) f(sigma z)=f(z), sigma(z)=-1/z        (fixes i)
Unknowns: Taylor coeffs c[j,k] of x^j v^k, v=y-1, total degree<=N. Assumption: f real-analytic at i
(true: eigenfunction of an elliptic operator with analytic coefficients). Asked: constraint on coefficients
when f(i)=c00=0. No numerical input, no zeta input: holds for ANY joint eigenfunction, hence cannot locate zeros."""
import sympy as sp
x,v,mu=sp.symbols("x v mu"); N=int(__import__("sys").argv[1]) if len(__import__("sys").argv)>1 else 5
cs={(j,k):sp.Symbol(f'c{j}{k}') for j in range(N+1) for k in range(N+1-j)}
f=sum(c*x**j*v**k for (j,k),c in cs.items())
def trunc(e,n=N):
    e=sp.expand(e); P=sp.Poly(e,x,v)
    return sum(co*x**a*v**b for (a,b),co in P.terms() if a+b<=n)
eqs=[]
# (E)
E=sp.expand((1+v)**2*(sp.diff(f,x,2)+sp.diff(f,v,2))-mu*f)
P=sp.Poly(E,x,v); eqs+=[co for (a,b),co in P.terms() if a+b<=N-2]
# (P)
eqs+=[cs[(j,k)] for (j,k) in cs if j%2==1]
# (S): X=-x/r2, Y=(1+v)/r2, r2=x^2+(1+v)^2 ; series to order N
r2=x**2+(1+v)**2
t=sp.symbols('t')
def ser(e):  # series in scaling t of rational fn
    return sp.series(e.subs({x:t*x,v:t*v}),t,0,N+1).removeO().subs(t,1)
X=ser(-x/r2); V=ser((1+v)/r2-1)
fs=sum(c*X**j*V**k for (j,k),c in cs.items())
fs=sp.expand(fs.subs({}) )
# truncate to total degree N in (x,v)
Pd=sp.Poly(fs-f,x,v); eqs+=[co for (a,b),co in Pd.terms() if a+b<=N]
sol=sp.solve(eqs+[cs[(0,0)]],list(cs.values()),dict=True)[0]
fz=sp.expand(f.subs(sol))
free=sorted(fz.free_symbols-{x,v,mu},key=str)
print("free parameters when f(i)=0:",free)
for d in range(0,N+1):
    print(f"degree {d}:", sp.factor(sum(t for t in sp.Add.make_args(fz) if sp.Poly(t,x,v).total_degree()==d)) if d>0 else 0)
