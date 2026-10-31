#!/usr/bin/env python3
"""Book XXIV, Interlude 1 -- "When to linearize, and when it lies".

Every number in the chapter is printed here.  Four blocks:
 1. Strogatz Example 6.3.2, x' = -y + a x (x^2+y^2), y' = x + a y (x^2+y^2):
    the polar form r' = a r^3, theta' = 1 is checked symbolically-by-sampling
    (exact rationals), and the case a = -1 is integrated with RK4 against the
    closed form r(t) = r0 / sqrt(1 + 2 r0^2 t).  The linearization (pure
    rotation) keeps r constant, so it is wrong about the kind of fixed point.
 2. A hyperbolic sink, the damped pendulum: linearizing works for small
    amplitude, degrades as amplitude grows, and misses other sinks entirely
    once the start is past theta = pi.
 3. The saddle-node x' = r + x^2: the eigenvalue 2x* at the stable branch
    goes to zero with r and is exactly zero at the fold.
 4. The horizon formula T* = (1/lam) ln(Dmax/d0) and the rate mix-up that
    book (Orthogenesis/Lyapunov/LyapunovHorizon.lean) records.
Each block has a control that must FAIL.  Lean is not run here.
"""
from fractions import Fraction as F
import math, random, sys

fails = 0
def check(name, ok):
    global fails
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok: fails += 1
random.seed(31)

# ---------------- 1 ----------------
def ex632(a):
    return lambda x, y: (-y + a*x*(x*x+y*y), x + a*y*(x*x+y*y))
# polar identities, exact: r r' = x x' + y y' = a r^4 ; theta' r^2 = x y' - y x' = r^2
ok = True
for _ in range(200):
    x, y, a = F(random.randint(-9, 9), 3), F(random.randint(-9, 9), 3), F(random.randint(-4, 4), 2)
    if x == 0 and y == 0: continue
    r2 = x*x + y*y
    xp, yp = -y + a*x*r2, x + a*y*r2
    if x*xp + y*yp != a*r2*r2: ok = False
    if x*yp - y*xp != r2: ok = False
check("1: x x' + y y' = a r^4 and x y' - y x' = r^2 (exact), so r' = a r^3, theta' = 1", ok)
bad = False
for _ in range(50):
    x, y = F(random.randint(1, 9), 3), F(random.randint(1, 9), 3)
    r2 = x*x + y*y; a = F(1, 2)
    xp, yp = -y + a*x*r2, x + a*y*r2
    if x*xp + y*yp == a*r2*r2 + 1: bad = True      # a wrong identity must not hold
check("1 control: a wrong identity (a r^4 + 1) never holds", not bad)

def rk4(f, v, h):
    k1 = f(*v); k2 = f(v[0]+h/2*k1[0], v[1]+h/2*k1[1])
    k3 = f(v[0]+h/2*k2[0], v[1]+h/2*k2[1]); k4 = f(v[0]+h*k3[0], v[1]+h*k3[1])
    return (v[0]+h/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0]), v[1]+h/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1]))
def radius_at(f, v, T, h=1/40):
    for _ in range(int(round(T/h))): v = rk4(f, v, h)
    return math.hypot(*v)
rows = []
for T in (10, 100, 1000):
    r_true = radius_at(ex632(-1.0), (1.0, 0.0), T)
    r_lin = radius_at(lambda x, y: (-y, x), (1.0, 0.0), T)
    r_cf = 1/math.sqrt(1 + 2*T)
    rows.append((T, r_true, r_cf, r_lin))
    print(f"      t={T:5d}  integrated r={r_true:.6f}  closed form={r_cf:.6f}  linearization r={r_lin:.6f}")
check("1: integrated r matches the closed form 1/sqrt(1+2t) (rel err < 1e-5)",
      all(abs(a-b)/b < 1e-5 for _, a, b, _ in rows))
check("1: the linearization keeps r = 1 (a center), while the true r has fallen", 
      all(abs(l-1) < 1e-6 for *_, l in rows) and rows[-1][1] < 0.03)
check("1 control: the wrong closed form 1/(1+2t) disagrees with the integration",
      any(abs(a - 1/(1+2*T))/a > 1e-2 for T, a, _, _ in rows))
t_1e3 = (1e6 - 1)/2
print(f"      time for r to reach 1e-3: {t_1e3:,.1f} (closed form); hyperbolic mu=-0.44: {math.log(1e3)/0.44:.1f}")
check("1: marginal case takes > 30,000x longer than the mu=-0.44 sink to reach 1e-3",
      t_1e3 / (math.log(1e3)/0.44) > 30000)
# blow-up for a>0
a = 1.0; r0 = 0.5; tblow = 1/(2*a*r0*r0)
r_near = radius_at(ex632(a), (r0, 0.0), tblow*0.9, h=1/400)
check(f"1: a=+1, r0=0.5 blows up at t=1/(2 a r0^2)={tblow:.1f}: r(0.9 t*) already > 1.5",
      r_near > 1.5)

# ---------------- 2 ----------------
def pend(c):
    return lambda x, y: (y, -math.sin(x) - c*y)
def lin(c):
    return lambda x, y: (y, -x - c*y)
print("      damped pendulum c=0.2, start (eps,0), T=20: radius nonlinear vs linear")
ratios = []
for eps in (0.05, 0.5, 1.5, 2.5):
    rn = radius_at(pend(0.2), (eps, 0.0), 20, h=1/100)
    rl = radius_at(lin(0.2), (eps, 0.0), 20, h=1/100)
    ratios.append(abs(rn - rl)/rl)
    print(f"        eps={eps:4.2f}  nonlinear r={rn:.4g}  linear r={rl:.4g}  rel diff={ratios[-1]:.3g}")
check("2: relative difference grows with starting amplitude", ratios == sorted(ratios))
check("2: at eps=0.05 the relative difference is below 1%", ratios[0] < 0.01)
check("2 control: at eps=2.5 it is above 10% (linearizing is NOT safe there)", ratios[-1] > 0.10)

# global failure: the damped pendulum has other sinks (theta = 2 pi, ...); the linearization has one
def final_theta(f, th0, T=80, h=1/100):
    v = (th0, 0.0)
    for _ in range(int(round(T/h))): v = rk4(f, v, h)
    return v[0]
f3, f35 = final_theta(pend(0.2), 3.0), final_theta(pend(0.2), 3.5)
l35 = final_theta(lin(0.2), 3.5)
print(f"      start theta=3.0 settles at {f3:.4f}; start theta=3.5 settles at {f35:.4f} (2 pi = {2*math.pi:.4f}); linearization from 3.5 settles at {l35:.4f}")
check("2: from theta0 = 3.0 the pendulum settles near 0", abs(f3) < 1e-2)
check("2: from theta0 = 3.5 it settles near 2 pi, a different sink", abs(f35 - 2*math.pi) < 1e-2)
check("2 control: the linearization from 3.5 goes to 0, so it misses that sink", abs(l35) < 1e-2)

# ---------------- 3 ----------------
ok3 = True
for r in (-1.0, -0.01, -0.0001):
    xs = -math.sqrt(-r); eig = 2*xs
    num = ((r + (xs+1e-6)**2) - (r + (xs-1e-6)**2))/2e-6      # finite-difference f'(x*)
    print(f"      r={r:9.4f}  x*={xs:9.4f}  eigenvalue 2x*={eig:8.4f}")
    if abs(num - eig) > 1e-6: ok3 = False
check("3: eigenvalue 2x* matches a finite-difference derivative at r=-1, -0.01, -0.0001", ok3)
check("3: at the fold (r=0, x*=0) the eigenvalue is exactly 0", 2*(-math.sqrt(0.0)) == 0)
check("3 control: a wrong formula (x*) does NOT match the finite difference",
      abs(((-1.0 + (1+1e-6)**2) - (-1.0 + (1-1e-6)**2))/2e-6 - (-1.0)) > 1)  # x*=-1 vs f'=-2... sign test

# ---------------- 4 ----------------
d0, Dmax, lam = 1e-3, 1.0, 0.9
Tstar = math.log(Dmax/d0)/lam
check(f"4: T* = (1/lam) ln(Dmax/d0) = {Tstar:.3f} gives d0*exp(lam*T*) = Dmax",
      abs(d0*math.exp(lam*Tstar) - Dmax) < 1e-9)
g09 = math.exp(0.9*10); g2 = 2.0**10
print(f"      ten days at lam=0.9: e^9 = {g09:.0f}; at doubling daily: 2^10 = {g2:.0f}; ratio {g09/g2:.2f}")
check("4: e^9 > 8000 > 1024 (the two rates differ by a factor of about 8 over ten days)",
      g09 > 8000 > g2 and 7.5 < g09/g2 < 8.5)
check("4 control: with lam = ln 2 the ten-day growth is exactly 2^10",
      abs(math.exp(math.log(2)*10) - 1024) < 1e-9)

print("\nALL CHECKS PASSED" if not fails else f"\n{fails} CHECK(S) FAILED")
sys.exit(1 if fails else 0)
