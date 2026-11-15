"""ch09 Proof VI replacement attempt (2026-11-14).  TOY MODEL - read before citing.

The book never defines K (curvature gate) and F (fold amplifier) as operators on a state space
(open item: operators C/K/F/U are not defined on L2(X_cat)).  So no simulation can 'confirm' the
book's operators.  This script fixes ONE explicit minimal encoding of ch8's verbal picture
('state x = vortex coherence; fold; K locks geometry; F amplifies') and reports what it gives,
whatever that is.  Nothing here is tuned to reach 0.94.

Model (Euler-Maruyama):  dx = (-x^3 + (a(t)-1) x + g(t)) dt + sigma dW
  K = ramp the gate g from 0 to G (breaks the x -> -x symmetry toward x>0)
  F = ramp the amplification a from 0 to A  (a>1: the x=0 state becomes unstable)
  correct order:  K over [0,T1], then F over [T1,2*T1]
  wrong order  :  F over [0,T1], then K over [T1,2*T1]
  P_ON = fraction of N paths with x(T) > 0.5 at T = 4*T1 (coherent = positive branch)
Everything is explicit below; integers/seeds fixed so the run reproduces exactly.
Inflow strength level = A in {1.5, 2.0, 3.0}. (No mapping to 10/50/100-yr storms is claimed.)"""
import numpy as np
SIGMA, G, T1, DT, N = 0.3, 0.2, 10.0, 0.001, 2000
def ramp(t,t0,t1,top): return top*min(max((t-t0)/(t1-t0),0.0),1.0)
def run(order, A, seed):
    rng=np.random.default_rng(seed); x=np.zeros(N); T=4*T1; n=int(T/DT)
    for i in range(n):
        t=i*DT
        if order=="KF": g=ramp(t,0,T1,G); a=ramp(t,T1,2*T1,A)
        else:           a=ramp(t,0,T1,A); g=ramp(t,T1,2*T1,G)
        x+=(-x**3+(a-1)*x+g)*DT+SIGMA*np.sqrt(DT)*rng.standard_normal(N)
    return float(np.mean(x>0.5))
if __name__=="__main__":
    print("A   P_ON(K then F)   P_ON(F then K)")
    for A in (1.5,2.0,3.0):
        print(f"{A:3.1f}  {run('KF',A,12345):.3f}            {run('FK',A,12345):.3f}")
