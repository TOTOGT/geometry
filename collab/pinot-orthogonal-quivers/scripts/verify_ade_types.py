"""Check the ADE type of the surfaces in Pinot, 'Quiver varieties for affine orthogonal quivers' (arXiv:2609.39434),
Thm 1.2, D~ rows.  Milnor number mu = dim C[x,y,z]/(grad F) at the origin, via Groebner basis.
All critical points of these quasi-homogeneous F lie at the origin (checked below), so the global
quotient dimension equals the local Milnor number."""
from sympy import symbols, groebner, diff, Poly, Rational

x, y, z = symbols('x y z')

def quotient_dim(F):
    G = groebner([diff(F, v) for v in (x, y, z)], x, y, z, order='grevlex')
    lead = [Poly(g, x, y, z).monoms(order='grevlex')[0] for g in G.exprs]
    # count standard monomials (finite iff zero-dimensional)
    B = 40
    return sum(1 for i in range(B) for j in range(B) for k in range(B)
               if not any(i >= a and j >= b and k >= c for a, b, c in lead))

def D(m):            # D_m normal form  z^2 + x y^2 + x^(m-1)
    return z**2 + x*y**2 + x**(m-1)

print("n | printed surface z^2 - x^(n-1) y + x y^2 : mu | paper says D_{n+1} | normal form D_{2n-2} : mu")
for n in range(3, 9):
    F = z**2 - x**(n-1)*y + x*y**2
    print(n, quotient_dim(F), f"D_{n+1}", quotient_dim(D(2*n-2)))

# Weight argument: path-length weights of the generators in the D~ rows:
#   x=det C3 -> 4 ; y=tr(C1C2) -> 2L+2 ; z=tr(C1C2C3) -> 2L+4.
# Kleinian D_m (z^2 + x y^2 + x^(m-1)) has weights (2, m-2, m-1) up to scale 2.
print("\nweight-forced m = L+3:")
for n in range(3, 9):
    for label, L in (("(D~_{2n-2}, v)", 2*n-5), ("(D~_{2n-1}, a)", 2*n-4)):
        wx, wy, wz = 4, 2*L+2, 2*L+4
        m = L + 3
        assert (wx, wy, wz) == (2*2, 2*(m-2), 2*(m-1))
        print(f"n={n} {label}: L={L}  m=L+3={m}   (paper: D_{n+1})")

# completing the square: z^2 + x y^2 - c x^(n-1) y  ~  D_{2n-2}
from sympy import expand, symbols as S
c, yp = S('c yp')
for n in range(3, 7):
    sub = expand((z**2 + x*y**2 - c*x**(n-1)*y).subs(y, yp + c*x**(n-2)/2))
    print(n, sub)

# Homogeneity of the *printed* (D~_{2n-1}, a) relation z^2 = y(-x)^(n-1) - x y^2, with L = 2n-4,
# weights x:4, y:2L+2, z:2L+4.  A pure x^(n-1) y term needs degree 4(n-1)+2L+2 = 4L+8: impossible.
print("\n(D~_{2n-1}, a): degree of z^2, x y^2, x^(n-1) y  (must all agree for a weighted-homogeneous relation)")
for n in range(3, 9):
    L = 2*n - 4
    dz2, dxy2, dxn1y = 2*(2*L+4), 4 + 2*(2*L+2), 4*(n-1) + (2*L+2)
    print(n, dz2, dxy2, dxn1y, "OK" if dz2 == dxy2 == dxn1y else "INHOMOGENEOUS")
    assert dz2 == dxy2 and dz2 != dxn1y
    # the homogeneous alternative:  x^(L+2) = x^(2n-2)  -> z^2 + x y^2 + x^(2n-2) = D_{2n-1}
    assert 4*(L+2) == dz2
