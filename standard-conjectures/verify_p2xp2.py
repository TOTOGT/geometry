#!/usr/bin/env python3
"""Exact algebra for a classical standard-conjecture benchmark.

X = P^2 x P^2, h = s*a + t*b, s,t positive rational.
Requires SymPy. No floating-point sampling, finite-field point counting,
Lean verification, or general-conjecture proof is claimed.
The geometric input CH*(X)_Q = Q[a,b]/(a^3,b^3) is documented in the note.
"""
import sympy as S

a, b, A, B = S.symbols("a b A B")
s, t = S.symbols("s t", positive=True)
checks = 0


def require(label, condition):
    global checks
    if not condition:
        raise RuntimeError("FAIL: " + label)
    checks += 1
    print("PASS:", label)


def zero(expr):
    return S.simplify(expr) == 0


def truncate(expr, variables=(a, b)):
    """Reduce independently in each factor of the projective-space ring."""
    poly = S.Poly(S.expand(expr), *variables)
    return S.expand(sum(
        coefficient * S.prod(v**e for v, e in zip(variables, powers))
        for powers, coefficient in poly.terms() if all(e <= 2 for e in powers)
    ))


def degree(expr):
    return S.expand(expr).coeff(a, 2).coeff(b, 2)


def vector(expr, basis):
    poly = S.Poly(truncate(expr), a, b)
    return S.Matrix([poly.coeff_monomial(monomial) for monomial in basis])


def same_matrix(left, right):
    return left.shape == right.shape and all(zero(x) for x in left-right)


h = s*a+t*b
p1 = s*a-t*b
p2 = s**2*a**2-s*t*a*b+t**2*b**2
require("primitive codimension 1: h^3 p1 = 0", zero(truncate(h**3*p1)))
require("primitive codimension 2: h p2 = 0", zero(truncate(h*p2)))

L3 = S.Matrix([[degree(h**3*a), degree(h**3*b)]])
L1 = S.Matrix.hstack(*(vector(h*m, [a*a*b, a*b*b]) for m in [a*a, a*b, b*b]))
require("codimension-1 primitive space has dimension 1", L3.rank() == 1)
require("codimension-2 primitive space has dimension 1", L1.rank() == 2)
require("p1 nonzero", not zero(p1))
require("p2 nonzero", not zero(p2))

values = [degree(h**4), -degree(h**2*p1**2), degree(p2**2)]
for r, (actual, expected) in enumerate(zip(values, [6*s*s*t*t, 2*s*s*t*t, 3*s*s*t*t])):
    require(f"signed primitive pairing in codimension {r}", zero(actual-expected))
    require(f"pairing coefficient positive for s,t > 0, codimension {r}", expected.is_positive is True)

M = S.Matrix.hstack(*(vector(h*h*m, [a*a*b, a*b*b]) for m in [a, b]))
require("L^2 matrix", same_matrix(M, S.Matrix([[2*s*t, s*s], [t*t, 2*s*t]])))
require("L^2 determinant = 3 s^2 t^2", zero(M.det()-3*s*s*t*t))
N = S.Matrix([[2/(3*s*t), -1/(3*t*t)], [-1/(3*s*s), 2/(3*s*t)]])
require("inverse matrix, both compositions", same_matrix(N*M, S.eye(2)) and same_matrix(M*N, S.eye(2)))

# Lowercase coordinates are on the source X; uppercase on the target X.
correspondence = b*(2*A/(3*s*t)-B/(3*s*s)) + a*(-A/(3*t*t)+2*B/(3*s*t))


def act(cycle, z):
    product = truncate(cycle*z, (a, b, A, B))
    pushed = S.expand(product).coeff(a, 2).coeff(b, 2)
    return pushed.subs({A: a, B: b}, simultaneous=True)


action = S.Matrix.hstack(*(vector(act(correspondence, z), [a, b]) for z in [a*a*b, a*b*b]))
require("explicit algebraic correspondence realizes N", same_matrix(action, N))
for i, z in enumerate([a, b]):
    require(f"correspondence after L^2 on basis element {i}", zero(act(correspondence, truncate(h*h*z))-z))
for i, z in enumerate([a*a*b, a*b*b]):
    require(f"L^2 after correspondence on basis element {i}", zero(truncate(h*h*act(correspondence, z))-z))
require("codimension-0 correspondence inverts L^4", zero(act(1/(6*s*s*t*t), truncate(h**4))-1))

gram = S.Matrix([[degree(x*y) for y in [a*a, a*b, b*b]] for x in [a*a, a*b, b*b]])
require("full middle pairing has signature (2,1)", gram.eigenvals() == {S.Integer(1): 2, S.Integer(-1): 1})

# A negative control: correct Frobenius weights do not force positive pairing.
q = S.symbols("q", positive=True)
F = q*q*S.eye(2)
J = S.diag(1, -1)
require("weight-four scalar Frobenius preserves an indefinite pairing up to q^4", same_matrix(F.T*J*F, q**4*J))
require("negative direction survives Frobenius compatibility", (S.Matrix([[0,1]])*J*S.Matrix([0,1]))[0] == -1)

print(f"\n{checks} exact checks passed; no skipped checks.")
print("Known P^2 x P^2 benchmark only. General standard conjectures NOT proved.")
