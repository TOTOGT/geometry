"""Inner basin boundary r*(z0) of the dm3 ODE, by bisection (DOP853, rtol 1e-12, atol 1e-14).
rdot = r(1-r^2)+2(r-1)e^{-z},  zdot = r^2-2(r-1)^2 e^{-z}.  'Converged' = no escape below r=1e-3 and |r(60)-1|<1e-3.
Produces the numbers quoted in book4 (r*=0.775941 at z0=0) and the z0 dependence. Numerically computed, not certified."""
import numpy as np
from scipy.integrate import solve_ivp
def f(t,y):
    r,z=y; e=np.exp(-z); return [r*(1-r*r)+2*(r-1)*e, r*r-2*(r-1)**2*e]
def conv(r0,z0,T=60):
    ev=lambda t,y:y[0]-1e-3; ev.terminal=True; ev.direction=-1
    s=solve_ivp(f,[0,T],[r0,z0],method="DOP853",rtol=1e-12,atol=1e-14,events=ev)
    return s.status!=1 and abs(s.y[0,-1]-1)<1e-3
for z0 in (0.0,0.01,0.05,0.5):
    lo,hi=0.3,0.95
    for _ in range(45):
        m=(lo+hi)/2
        if conv(m,z0): hi=m
        else: lo=m
    print(f"z0={z0}: r*={hi:.6f}")
