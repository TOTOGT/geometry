#!/usr/bin/env python3
"""X = P^3 x P^3, d = 6. CH(X)_Q = Q[a,b]/(a^4,b^4) = H^{2*}(X;Q) (cellular: Chow = cohomology, odd cohomology 0),
deg(a^3 b^3) = 1.  h = s a + t b with s,t > 0 rational.  Exact arithmetic throughout.

Claims checked, for EVERY primitive class (the whole space, not generators only):
  (i)   dim A^r = r+1 (r=0..3); L^{d-2r+1}: A^r -> A^{d-r+1} has kernel P^r of dimension 1 for r = 0..3
        (so the primitive space is one-dimensional in each codimension <= d/2 and a generator spans it);
  (ii)  rescaling a->s a, b->t b is a ring automorphism, so everything reduces to s = t = 1:
        (-1)^r deg(z^2 h^{d-2r}) = s^3 t^3 * V_r * c^2 for z = c * p_r(s,t), V_r computed at s=t=1;
  (iii) V_r > 0 for r = 0,1,2,3 (the signed Hodge-type inequality);
  (iv)  also checked directly with SYMBOLIC s,t as a cross-check.
"""
import sympy as sp
a, b, s, t, c = sp.symbols('a b s t c')
N = 4; d = 6
def red(e):
    P = sp.Poly(sp.expand(e), a, b); r = 0
    for (i, j), co in P.terms():
        if i < N and j < N: r += co*a**i*b**j
    return sp.expand(r)
def mons(r): return [a**i*b**(r-i) for i in range(0, r+1) if i < N and r-i < N]
def coords(e, r):
    P = sp.Poly(red(e), a, b); return [P.coeff_monomial(m) for m in mons(r)]
def deg(e): return sp.Poly(red(e), a, b).coeff_monomial(a**3*b**3)
ok = []
def chk(name, cond):
    cond = bool(cond); ok.append(cond); print(('PASS ' if cond else 'FAIL ') + name)
def primitive_space(r, hh):
    """kernel of multiplication by hh^(d-2r+1): A^r -> A^(d-r+1), as list of polynomials."""
    k = d - 2*r + 1; src = mons(r); tgt = mons(d-r+1)
    cols = [coords(red(hh**k*m), d-r+1) for m in src]
    M = sp.Matrix(len(tgt), len(src), lambda i, j: cols[j][i])
    ns = M.nullspace()
    return [sum(v[i]*src[i] for i in range(len(src))) for v in ns], M
# (i) dimensions, at generic symbolic s,t: kernel dimension from exact rank over Q(s,t)
h = s*a + t*b
gens = {}
for r in range(0, 4):
    chk('dim A^%d = %d' % (r, r+1), len(mons(r)) == r+1)
    ker, M = primitive_space(r, h)
    chk('r=%d: kernel of L^%d has dimension 1 (generic s,t)  [rank %d of %d columns]' % (r, d-2*r+1, M.rank(), M.shape[1]), len(ker) == 1)
    gens[r] = sp.factor(ker[0])
    # no degeneration for s,t > 0: dimension equals the s=t=1 value and the rescaling argument covers all s,t
for r in range(0, 4):
    ker1, _ = primitive_space(r, a + b)
    chk('r=%d: at s=t=1 kernel dim 1' % r, len(ker1) == 1)
# (ii)-(iii) values at s=t=1, then scaling
print('primitive generators at s=t=1:')
V = {}
for r in range(0, 4):
    p = sp.expand(primitive_space(r, a+b)[0][0]); 
    val = (-1)**r*deg(p**2*(a+b)**(d-2*r)); V[r] = val
    print('  p_%d = %s   (-1)^%d deg(p^2 h^%d) = %s' % (r, sp.factor(p), r, d-2*r, val))
    chk('V_%d > 0' % r, val > 0)
# (ii) scaling law: a->s a, b->t b automorphism gives deg(z(sa,tb)^2 (sa+tb)^(d-2r)) = s^3 t^3 deg(z^2 (a+b)^(d-2r))
for r in range(0, 4):
    p1 = sp.expand(primitive_space(r, a+b)[0][0])
    ps = sp.expand(p1.subs({a: s*a, b: t*b}, simultaneous=True))
    lhs = (-1)**r*deg(sp.expand(ps**2*(s*a+t*b)**(d-2*r)))
    chk('r=%d scaling: (-1)^r deg(z_s^2 h^%d) = s^3 t^3 V_%d, symbolic s,t' % (r, d-2*r, r), sp.simplify(lhs - s**3*t**3*V[r]) == 0)
    # and z_s is in the primitive space for h = s a + t b
    chk('r=%d z_s primitive for h = s a + t b (symbolic)' % r, red(sp.expand(ps*(s*a+t*b)**(d-2*r+1))) == 0)
print('%d/%d checks passed' % (sum(ok), len(ok)))
raise SystemExit(0 if all(ok) else 1)
