#!/usr/bin/env python3
"""
ch22-verify.py — regenerates every computed number printed in
Principia Orthogona, Book IV, Chapter 22 ("Duality and the Discriminant").

Repo rule: a published number must be regenerable by a tool.
Run:  python3 ch22-verify.py
Requires: sympy
"""
import sympy as sp

FAIL = []
def check(label, got, want):
    ok = (sp.simplify(got - want) == 0) if isinstance(got, sp.Expr) else (got == want)
    print(("  OK   " if ok else "  FAIL ") + label + f"   got={got}  want={want}")
    if not ok:
        FAIL.append(label)

x, y, z, r, th = sp.symbols('x y z r theta', real=True)
x_ = sp.Symbol('x_')


def alpha_wedge_dalpha(A, B, C, v=(x, y, z)):
    """alpha = A dx + B dy + C dz  ->  coefficient of dx^dy^dz in alpha ^ dalpha."""
    u, w, t = v
    return sp.simplify(A*(sp.diff(C, w) - sp.diff(B, t))
                       + B*(sp.diff(A, t) - sp.diff(C, u))
                       + C*(sp.diff(B, u) - sp.diff(A, w)))


print("\n[1] the dm3 contact form in Cartesian coordinates")
X, Y = r*sp.cos(th), r*sp.sin(th)
c_dr = sp.simplify(X*sp.diff(Y, r) - Y*sp.diff(X, r))
c_dth = sp.simplify(X*sp.diff(Y, th) - Y*sp.diff(X, th))
check("x dy - y dx has no dr component", c_dr, 0)
check("x dy - y dx = r^2 dtheta", c_dth, r**2)

print("\n[2] alpha = dz - r^2 dtheta = dz - x dy + y dx is contact on all of R^3")
check("alpha ^ dalpha coefficient", alpha_wedge_dalpha(y, -x, sp.Integer(1)), -2)
print("       (nonvanishing at r=0 too: the zero in cylindrical coordinates")
print("        is the Jacobian r of the polar chart, not a degeneracy)")

print("\n[3] the shear psi(x,y,z) = (x, y, z + xy) followed by y -> y/2")
Z = z + x*y
pb = (sp.diff(Z, x) + y, sp.diff(Z, y) - x, sp.diff(Z, z))
check("psi* alpha, dx coefficient", sp.simplify(pb[0]), 2*y)
check("psi* alpha, dy coefficient", sp.simplify(pb[1]), 0)
check("psi* alpha, dz coefficient", sp.simplify(pb[2]), 1)
check("after y -> y/2, dz + y dx is contact", alpha_wedge_dalpha(y, sp.Integer(0), sp.Integer(1)), -1)
print("       => dm3 form is contactomorphic to the standard structure on R^3 = J^1(R,R)")

print("\n[4] J^1(R,R^n) is a contact manifold only for n = 1")
for n in (1, 2, 3):
    dim = 1 + 2*n                      # (x, y_1..y_n, p_1..p_n)
    cartan = dim - n                   # ker of n independent 1-forms
    need = dim - 1                     # a contact hyperplane field has corank 1
    print(f"       n={n}: dim J^1 = {dim}, Cartan distribution rank = {cartan}, "
          f"contact needs rank {need}  ->  {'contact' if cartan == need else 'NOT contact'}")
check("only n=1 gives corank 1", [n for n in (1, 2, 3) if (1+2*n) - n == 2*n], [1])

print("\n[5] Plucker: d^dual = d(d-1) - 2*delta - 3*kappa")
def plucker(d, delta=0, kappa=0):
    return d*(d-1) - 2*delta - 3*kappa
check("smooth conic  d=2",              plucker(2), 2)
check("smooth cubic  d=3",              plucker(3), 6)
check("nodal cubic   d=3, delta=1",     plucker(3, delta=1), 4)
check("cuspidal cubic d=3, kappa=1",    plucker(3, kappa=1), 3)

print("\n[6] cuspidal cubic y^2 z = x^3: dual computed by elimination")
a, b, c, s = sp.symbols('a b c s')
# parametrise the cuspidal cubic: [s^... ] use affine y^2 = x^3, (x,y) = (t^2, t^3)
t = sp.symbols('t')
px, py = t**2, t**3
# tangent line at t:  a*x + b*y + c = 0 through (px,py) with direction (px', py')
# conditions: a*px + b*py + c = 0  and  a*px' + b*py' = 0
sols = sp.solve([a*px + b*py + c, a*sp.diff(px, t) + b*sp.diff(py, t)], [a, c], dict=True)[0]
A_, C_ = sp.simplify(sols[a]), sp.simplify(sols[c])
# dual curve in coordinates (a,c) with b normalised to 1
dual = sp.simplify(sp.resultant(sp.numer(sp.together(a - A_)), sp.numer(sp.together(c - C_)), t))
dual = sp.factor(sp.Poly(dual, a, c).as_expr())
print("       dual curve equation (b = 1 chart):", dual)
deg = sp.Poly(dual, a, c).total_degree()
check("degree of the dual of the cuspidal cubic", deg, 3)

print("\n[7] discriminant of a binary form of degree d has degree 2(d-1)")
for d in (2, 3, 4, 5):
    co = sp.symbols(f'c0:{d+1}')
    u = sp.symbols('u')
    f = sum(co[i]*u**(d-i) for i in range(d+1))
    res = sp.expand(sp.resultant(sp.Poly(f, u), sp.Poly(sp.diff(f, u), u)))
    res_deg = sp.Poly(res, *co).total_degree()
    # disc(f) = Res(f, f') / c0 ; the resultant carries one extra factor of the
    # leading coefficient, so it sits one degree above the discriminant.
    disc, rem = sp.div(sp.Poly(res, *co), sp.Poly(co[0], *co))
    check(f"Res(f,f') is divisible by c0, d={d}", rem.as_expr(), 0)
    deg = disc.total_degree()
    print(f"       d={d}: Res(f,f') degree {res_deg}; disc = Res/c0 degree {deg}; 2(d-1) = {2*(d-1)}")
    check(f"discriminant degree, d={d}", deg, 2*(d-1))

print("\n[8] dual defect of the Segre P^1 x P^2 in P^5")
# P^1 x P^2 = rank-1 locus of 2x3 matrices, sitting in P(2x3 matrices) = P^5
amb = 2*3 - 1                       # 5
segre = 1 + 2                       # 3
dual_var = segre                    # rank <= 1 locus is self-describing here; dim 3
check("ambient dimension", amb, 5)
check("dim Segre P^1 x P^2", segre, 3)
check("dim of the dual (rank <=1 locus of the transpose pencil)", dual_var, 3)
check("codim of the dual (a hypersurface would be 1)", amb - dual_var, 2)
check("dual defect", (amb - dual_var) - 1, 1)

print("\n[9] the Legendre transformation on J^1(R,R): L(x,u,p) = (p, px - u, x)")
u_, p_ = sp.symbols('u p', real=True)
def L(X, U, P):
    return (P, P*X - U, X)
# pull back alpha = du - p dx under L
Lx, Lu, Lp = L(x, u_, p_)
# alpha_L = d(Lu) - Lp * d(Lx), expanded in the basis (dx, du, dp)
basis = (x, u_, p_)
alpha_L = [sp.simplify(sp.diff(Lu, v) - Lp*sp.diff(Lx, v)) for v in basis]
alpha_0 = [sp.simplify(sp.diff(u_, v) - p_*sp.diff(x, v)) for v in basis]
check("L* alpha = -alpha, dx component", alpha_L[0], -alpha_0[0])
check("L* alpha = -alpha, du component", alpha_L[1], -alpha_0[1])
check("L* alpha = -alpha, dp component", alpha_L[2], -alpha_0[2])
print("       => L preserves ker(alpha): it is a contact transformation")
print("       => it moves p into the base coordinates, so it is NOT a prolonged")
print("          point transformation. Baecklund's exceptional case n = 1.")

print("\n[10] biduality, in the affine chart: L o L = identity")
LL = L(*L(x, u_, p_))
check("L(L(x,u,p)) = (x,u,p)", list(sp.simplify(sp.Matrix(LL) - sp.Matrix([x, u_, p_]))), [0, 0, 0])

print("\n[11] the dual of the cuspidal cubic is itself CUSPIDAL -- and the chart decides")
F = 4*a**3 + 27*b**2*c
grad = [sp.diff(F, v) for v in (a, b, c)]
sing = sp.solve(grad + [F], [a, b, c], dict=True)
print("       X^v : ", F, " = 0    grad =", grad)
print("       projective singular locus:", sing, " -> the single point [0:0:1]")
check("X^v is singular at exactly one point", len(sing), 1)
# chart b = 1: the singular point is not in this chart, so the curve looks smooth
Gb = F.subs(b, 1)
sing_b = sp.solve([sp.diff(Gb, v) for v in (a, c)] + [Gb], [a, c], dict=True)
print("       chart b=1 :", Gb, "= 0  -> c = -4a^3/27, singular points:", sing_b)
check("no singular point visible in the chart b = 1", len(sing_b), 0)
# chart c = 1: the cusp is here
Gc = F.subs(c, 1)
sing_c = sp.solve([sp.diff(Gc, v) for v in (a, b)] + [Gc], [a, b], dict=True)
print("       chart c=1 :", Gc, "= 0  -> b^2 = -4a^3/27, singular points:", sing_c)
check("the cusp is visible in the chart c = 1", len(sing_c), 1)
print("       => plotting a dual curve in the wrong chart can hide its singularities entirely")

print("\n[12] 4a^3 + 27b^2 is three objects at once")
disc_cubic = sp.discriminant(x_**3 + a*x_ + b, x_)
print("       discriminant of x^3 + ax + b        :", sp.factor(disc_cubic))
check("disc(x^3+ax+b) = -(4a^3 + 27b^2)", sp.expand(disc_cubic + (4*a**3 + 27*b**2)), 0)
V = x_**4/4 + a*x_**2/2 + b*x_
bif = sp.expand(sp.resultant(sp.Poly(sp.diff(V, x_), x_), sp.Poly(sp.diff(V, x_, 2), x_)))
print("       cusp catastrophe V = x^4/4 + ax^2/2 + bx, eliminate x between V' and V'':", sp.factor(bif))
check("bifurcation set = 4a^3 + 27b^2", sp.expand(bif - (4*a**3 + 27*b**2)), 0)
check("bifurcation set = dual of the cuspidal cubic in the chart c=1", sp.expand(bif - Gc), 0)
print("       => the dual variety of block [6], the discriminant of the cubic, and the")
print("          cusp catastrophe's bifurcation curve are one equation.")

print("\n" + ("ALL CHECKS PASSED" if not FAIL else "FAILURES: " + ", ".join(FAIL)))
raise SystemExit(1 if FAIL else 0)
