from mpmath import mp, mpf, zeta, gamma, besselk, cos, pi, sqrt, diff, matrix, eigsy
import json
mp.dps=30
def sigma(k,a): return sum(mpf(d)**a for d in range(1,k+1) if k%d==0)
def E_series(x,y,s,K=40):
    s=mpf(s)
    t=2*zeta(2*s)*y**s + 2*sqrt(pi)*gamma(s-mpf(1)/2)*zeta(2*s-1)/gamma(s)*y**(1-s)
    S=0
    for k in range(1,K+1):
        S+= mpf(k)**(s-mpf(1)/2)*sigma(k,1-2*s)*besselk(s-mpf(1)/2,2*pi*k*y)*cos(2*pi*k*x)
    return t+ 8*pi**s/gamma(s)*sqrt(y)*S
def E_direct(x,y,s,M=400):
    t=mpf(0)
    for m in range(-M,M+1):
        for n in range(-M,M+1):
            if m==0 and n==0: continue
            t+= y**s/((m+n*x)**2+(n*y)**2)**s
    return t
if __name__=='__main__':
    for s in (2,3):
        a=E_series(mpf(0),mpf(1),s); b=E_direct(0,1,s,150)
        print(s,a,b,a-b)
