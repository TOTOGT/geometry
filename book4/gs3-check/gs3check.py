from mpmath import mp,mpf,mpc,gamma,zeta,pi,sqrt,quad,tanh,exp,inf,log,acosh,nsum,altzeta
mp.dps=30
Lam=lambda s:pi**(-s/2)*gamma(s/2)*zeta(s)
phi=lambda s:Lam(2*s-1)/Lam(2*s)
cf=lambda s:sqrt(pi)*gamma(s-mpf(1)/2)*zeta(2*s-1)/(gamma(s)*zeta(2*s))
for s in [mpc(.8,2.5),mpc(.6,-1.2),mpc(2.2,.7)]:
    print('phi',abs(phi(s)*phi(1-s)-1),abs(phi(s)-cf(s)))
# residue at s=1
eps=mpf(10)**-12;print('res',eps*phi(1+eps),3/pi)
# heat identity term
for t in [mpf('0.1'),mpf('0.03'),mpf('0.01')]:
    I=(1/12)*quad(lambda r:exp(-t*(mpf(1)/4+r*r))*r*tanh(pi*r),[0,5,50,inf])*2
    ap=(1/12)*(1/t-mpf(1)/12)*exp(-t/4)
    print('heat',t,I,ap,I-ap)
# geodesic
print('geod',2*log((3+sqrt(5))/2),2*acosh(mpf(3)/2))
# E*(i,s), E*(rho,s) vs direct lattice sum
import numpy as np
def Estar(x,y,s,R=600):
    tot=mpf(0)
    tot=0.0
    ms=np.arange(-R,R+1)
    for n in range(-R,R+1):
        a=ms+n*x;q=a*a+(n*y)**2;mask=(q>0)&(q<=R*R)
        tot+=np.sum(y**s*q[mask]**(-s))
    tot+=float(pi)*y**(s-1)*R**(2-2*s)/(s-1)
    return 0.5*float(pi**(-s)*gamma(s))*tot
def L4(s):return (mp.zeta(s,mpf(1)/4)-mp.zeta(s,mpf(3)/4))/4**s
def L3(s):return (mp.zeta(s,mpf(1)/3)-mp.zeta(s,mpf(2)/3))/3**s
s=2.5
print('Ei',Estar(0,1,s),2*pi**(-s)*gamma(s)*zeta(s)*L4(s))
print('Er',Estar(-.5,sqrt(3)/2,s),3*(sqrt(3)/(2*pi))**s*gamma(s)*zeta(s)*L3(s))
