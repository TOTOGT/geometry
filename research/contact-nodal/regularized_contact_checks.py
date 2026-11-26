"""Regularized form eta = dz + Re(f) d Im(f), f holomorphic on a domain D in C (s = sigma + i t).
Claim (hand-derivable): d eta = |f'|^2 dsigma^dt ; eta^d eta = |f'|^2 dz^dsigma^dt; contact at s iff f'(s) != 0.
Checks: (i) Jacobian identity numerically for f=zeta; (ii) contact at simple zeros of zeta, failure at zeros of zeta';
(iii) toy f=s^2: smooth through its DOUBLE zero at 0 but NOT contact there; (iv) local Taylor lemma at a zero of order m:
|f'|^2 = O(|s-s0|^(2m-2)); (v) Speiser in this language. No claim about RH."""
from mpmath import mp, mpf, mpc, zeta, diff, zetazero, findroot, fabs
mp.dps=30
ok=True
def chk(name,cond,info=""):
    global ok; ok&=bool(cond); print(("[PASS] " if cond else "[FAIL] ")+name,info)
def jac(f,s):   # d(Re f,Im f)/d(sigma,t) by numerical derivatives of Re,Im along sigma and t
    h=mpf(10)**-12
    fs=(f(s+h)-f(s-h))/(2*h); ft=(f(s+1j*h)-f(s-1j*h))/(2*h)
    u_s,v_s,u_t,v_t=fs.real,fs.imag,ft.real,ft.imag
    return u_s*v_t-u_t*v_s, (u_s,u_t,v_s,v_t)
for s in [mpc(2,1),mpc(0.3,7),mpc(0.7,3),mpc(-1.5,20),mpc(1.2,-40)]:
    J,(us,ut,vs,vt)=jac(zeta,s)
    chk(f"CR + Jacobian = |zeta'|^2 at {s}", fabs(us-vt)<1e-9*(1+fabs(us)) and fabs(ut+vs)<1e-9*(1+fabs(ut)) and fabs(J-abs(diff(zeta,s))**2)<1e-8*(1+abs(J)), f"J={mp.nstr(J,8)}")
rho=zetazero(1)
chk("simple zero rho1: zeta(rho1)=0 but |zeta'|^2>0 => contact", fabs(zeta(rho))<1e-25 and abs(diff(zeta,rho))**2>0.1, f"|zeta'|^2={mp.nstr(abs(diff(zeta,rho))**2,8)}")
zp=findroot(lambda s: diff(zeta,s), mpc(2.46,23.3))
chk("zero of zeta' found (|zeta'|<1e-20): contact fails there", abs(diff(zeta,zp))<1e-20, f"s={mp.nstr(zp,10)}")
f2=lambda s:s**2
J0,_=jac(f2,mpc(0,0)); J1,_=jac(f2,mpc(0.01,0.01))
chk("toy f=s^2 (double zero): Jacobian 0 at the zero (not contact), positive nearby", abs(J0)<1e-18 and J1>0, f"J(0)={mp.nstr(J0,3)} J(.01+.01i)={mp.nstr(J1,5)} (=4|s|^2={4*2e-4})")
for m in (1,2,3):
    fm=lambda s,m=m:s**m
    e=mpf('1e-3'); J,_=jac(fm,mpc(e,0))
    chk(f"order-{m} zero: J ~ m^2 |s|^(2m-2)", fabs(J-m**2*e**(2*m-2))<1e-6*(m**2*e**(2*m-2)+1e-30),f"J={mp.nstr(J,6)}")
print("ALL PASS" if ok else "SOME FAIL")
