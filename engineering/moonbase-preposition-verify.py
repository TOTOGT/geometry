#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""moonbase-preposition-verify.py -- companion to engineering/beltdraulic-paper.html section 11 (resources in place before arrival).
Written 2026-09-30 (R24). NOTHING here is sourced data on actuator reliability. ASSUMED: N actuators, per-actuator MTBF, the
unattended interval T. Standard constants (not read here): Earth-Moon mean distance 384,400 km, c = 299,792.458 km/s.
Question: with no crew and no repair for T, how many spares (or how much redundancy) must be delivered first?"""
import math, sys
fails=[]
def check(ok,msg):
    print('    %s  %s'%('PASS' if ok else 'FAIL',msg))
    if not ok: fails.append(msg)
def head(n,t): print('\n'+'='*72+'\n  [%s]  %s\n'%(n,t)+'='*72)

head(1,'no redundancy: P(no failure) = exp(-N T / MTBF)   [N, MTBF, T ASSUMED]')
T=8766.0   # one year of unattended hours
for N,mtbf in ((100,1e5),(1000,1e5),(1000,1e6)):
    mu=N*T/mtbf
    print('    N=%5d, MTBF=%.0e h, T=%.0f h: expected failures mu = %.2f ; P(none) = %.3e'%(N,mtbf,T,mu,math.exp(-mu)))
mu=1000*T/1e5
check(abs(mu-87.66)<1e-6,'N=1000, MTBF 1e5 h, one year: mu = 87.66 expected failures')
check(math.exp(-mu)<1e-30,'P(no failure) is below 1e-30: without spares the warehouse does not arrive intact')

head(2,'with s spares: P(failures <= s) = exp(-mu) * sum_{k<=s} mu^k / k!   (Poisson: the 1/k! series again)')
def cdf(s,mu):
    t=math.exp(-mu); tot=t
    for k in range(1,s+1):
        t*=mu/k; tot+=t
    return tot
def need(mu,p):
    s=0
    while cdf(s,mu)<p: s+=1
    return s
print('    mu=87.66 (N=1000): spares s needed for P(covered) >= p')
for p in (0.9,0.99,0.999,0.99999):
    s=need(mu,p); print('      p=%-8g  s=%3d   (%.1f%% of N ; mu + z*sqrt(mu) with mu=%.1f, sqrt=%.2f)'%(p,s,100*s/1000,mu,math.sqrt(mu)))
check(need(mu,0.999)>mu,'spares needed for 0.999 exceed the mean number of failures (%d > %.1f)'%(need(mu,0.999),mu))
check(abs(cdf(200,mu)-1)<1e-12,'the Poisson sum reaches 1')
print('    the requirement is mu + a few sqrt(mu): spares scale with the expected failures, NOT with N alone; halving the failure rate roughly halves mu.')

head(3,'the price of spares, in Earth-orbit mass  (K = 5.09..6.66 kg LEO per kg landed, from moonbase-warehouse-verify.py)')
K0,K1=5.09,6.66
for mtbf in (1e5,2e5):
    mu2=1000*T/mtbf; s=need(mu2,0.999)
    print('    MTBF %.0e h: mu=%.1f, spares for 0.999 = %d ; extra mass = %d x unit mass, i.e. %.1f%% of the fleet; in LEO %.0f-%.0f unit-masses'%(mtbf,mu2,s,s,100*s/1000,s*K0,s*K1))
print('    doubling MTBF (a simpler, fluid-free actuator with fewer failure modes, IF true) removes about half the spares: a mass gain that comes from reliability, not from efficiency.')
check(need(1000*T/2e5,0.999)<need(1000*T/1e5,0.999)*0.65,'doubling MTBF cuts the spares for 0.999 by more than a third')

head(4,'remote operation from Earth')
d=384400.0; c=299792.458
print('    one-way light time = %.3f s ; round trip = %.3f s (standard constants, not read here)'%(d/c,2*d/c))
check(abs(d/c-1.282)<1e-3,'one-way 1.282 s')
print('    so teleoperation has a 2.6 s loop: a warehouse that must be built and maintained before arrival needs on-site autonomy for anything faster.')
print('\n'+('FAIL: %d'%len(fails) if fails else 'all checks passed')); sys.exit(1 if fails else 0)
