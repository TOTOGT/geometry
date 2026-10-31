#!/usr/bin/env python3
"""Book XXIV, Chapter 2 -- checks behind "Superposition: what linear means".

A. EXACT (Fractions): one RK4 step of x' = A x with rational A and step h is
   a fixed matrix M = I + hA + (hA)^2/2 + (hA)^3/6 + (hA)^4/24, so stepping
   is additive and homogeneous.  Checked over 20 steps for random rational
   p, q, c.  Control: the same step with a cubic term added must FAIL.
B. EXACT (floats only for sin, but a single evaluation): the scaling
   counterexample of Proposition 4.  For theta'' = -sin(theta), a solution
   with theta(0)=pi/2, theta'(0)=0 has (2 theta)''(0) = -2 sin(pi/2) = -2,
   while -sin(2 theta(0)) = -sin(pi) ~ 0.  So 2*theta is not a solution.
C. NUMERICAL (floats): the plate's integrator, reproduced here.  For each
   linear preset the superposition gap max_t |x_{p+q} - x_p - x_q| over
   0<=t<=8 is at rounding level; for the pendulum it is large.  Control:
   a linear system with a small quadratic term added must show a gap.
This script does not run the page's JavaScript; it reproduces the same
integrator and checks the mathematics the page states.
"""
from fractions import Fraction as F
import math, random, sys

random.seed(20261031)
fails = 0
def check(name, ok):
    global fails
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok:
        fails += 1

# ---------- A ----------
A = [[F(-1, 5), F(1)], [F(-1), F(-1, 5)]]
h = F(1, 10)
def matmul(X, Y):
    return [[sum(X[i][k] * Y[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def madd(X, Y): return [[X[i][j] + Y[i][j] for j in range(2)] for i in range(2)]
def mscale(c, X): return [[c * X[i][j] for j in range(2)] for i in range(2)]
I2 = [[F(1), F(0)], [F(0), F(1)]]
hA = mscale(h, A)
hA2 = matmul(hA, hA); hA3 = matmul(hA2, hA); hA4 = matmul(hA3, hA)
M = madd(madd(madd(madd(I2, hA), mscale(F(1, 2), hA2)), mscale(F(1, 6), hA3)), mscale(F(1, 24), hA4))
def apply(Mx, v): return [Mx[0][0]*v[0] + Mx[0][1]*v[1], Mx[1][0]*v[0] + Mx[1][1]*v[1]]

def rk4_lin(f, v, h):
    k1 = f(v)
    k2 = f([v[0] + h/2*k1[0], v[1] + h/2*k1[1]])
    k3 = f([v[0] + h/2*k2[0], v[1] + h/2*k2[1]])
    k4 = f([v[0] + h*k3[0], v[1] + h*k3[1]])
    return [v[i] + h/6*(k1[i] + 2*k2[i] + 2*k3[i] + k4[i]) for i in range(2)]
flin = lambda v: [A[0][0]*v[0] + A[0][1]*v[1], A[1][0]*v[0] + A[1][1]*v[1]]
fnon = lambda v: [A[0][0]*v[0] + A[0][1]*v[1] + v[0]**3, A[1][0]*v[0] + A[1][1]*v[1]]

def rnd(): return F(random.randint(-9, 9), random.randint(1, 5))
ok_step = True; ok_hom = True; ok_add = True
for _ in range(6):
    p = [rnd(), rnd()]; q = [rnd(), rnd()]; c = rnd()
    P, Q, S, C = p[:], q[:], [p[0]+q[0], p[1]+q[1]], [c*p[0], c*p[1]]
    for _ in range(20):
        P = rk4_lin(flin, P, h); Q = rk4_lin(flin, Q, h)
        S = rk4_lin(flin, S, h); C = rk4_lin(flin, C, h)
    if S != [P[0]+Q[0], P[1]+Q[1]]: ok_add = False
    if C != [c*P[0], c*P[1]]: ok_hom = False
    if rk4_lin(flin, p, h) != apply(M, p): ok_step = False
check("A: RK4 on linear A is the matrix M (exact), 6 random p", ok_step)
check("A: additive over 20 steps, exact rationals", ok_add)
check("A: homogeneous over 20 steps, exact rationals", ok_hom)
brk = False
for _ in range(6):
    p = [rnd(), rnd()]; q = [rnd(), rnd()]
    P, Q, S = p[:], q[:], [p[0]+q[0], p[1]+q[1]]
    for _ in range(1):
        P = rk4_lin(fnon, P, h); Q = rk4_lin(fnon, Q, h); S = rk4_lin(fnon, S, h)
    if S != [P[0]+Q[0], P[1]+Q[1]]: brk = True
check("A control: with a cubic term, additivity FAILS (must)", brk)

# ---------- B ----------
second = -2 * math.sin(math.pi / 2)
needed = -math.sin(2 * (math.pi / 2))
check(f"B: (2θ)''(0) = {second:.3g} but -sin(2θ(0)) = {needed:.3g}: scaling is not a solution",
      abs(second - needed) > 1.9)
x0 = math.pi / 2
lin = lambda x: -x
check("B control: the same test on the linear right-hand side -x passes (2*f(x0) == f(2*x0))",
      abs(2 * lin(x0) - lin(2 * x0)) < 1e-15)

# ---------- C ----------
def rk4(f, v, h):
    k1 = f(v)
    k2 = f((v[0]+h/2*k1[0], v[1]+h/2*k1[1]))
    k3 = f((v[0]+h/2*k2[0], v[1]+h/2*k2[1]))
    k4 = f((v[0]+h*k3[0], v[1]+h*k3[1]))
    return (v[0]+h/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0]), v[1]+h/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1]))
SYS = {
    "spiral sink": lambda v: (-0.2*v[0] + v[1], -v[0] - 0.2*v[1]),
    "saddle":      lambda v: (v[0], -v[1]),
    "center":      lambda v: (v[1], -v[0]),
    "pendulum":    lambda v: (v[1], -math.sin(v[0])),
    "linear+0.1x^2 (control)": lambda v: (-0.2*v[0] + v[1] + 0.1*v[0]**2, -v[0] - 0.2*v[1]),
}
def gap(f, p, q, T=8.0, dt=0.02):
    a, b, c = p, q, (p[0]+q[0], p[1]+q[1]); g = 0.0
    for _ in range(int(T/dt)):
        a, b, c = rk4(f, a, dt), rk4(f, b, dt), rk4(f, c, dt)
        g = max(g, math.hypot(c[0]-a[0]-b[0], c[1]-a[1]-b[1]))
    return g
p, q = (1.0, 0.0), (0.5, 0.5)
res = {k: gap(f, p, q) for k, f in SYS.items()}
for k, v in res.items():
    print(f"      gap[{k}] = {v:.3e}")
for k in ("spiral sink", "saddle", "center"):
    check(f"C: {k}: gap at rounding level (< 1e-9)", res[k] < 1e-9)
check("C: pendulum: gap is large (> 0.1)", res["pendulum"] > 0.1)
check("C control: linear + small quadratic term shows a gap (> 1e-3)",
      res["linear+0.1x^2 (control)"] > 1e-3)

print("\nALL CHECKS PASSED" if not fails else f"\n{fails} CHECK(S) FAILED")
sys.exit(1 if fails else 0)
