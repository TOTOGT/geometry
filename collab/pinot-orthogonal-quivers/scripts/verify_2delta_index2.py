"""Ring-level consistency of Conjecture C (2-delta surfaces are quotients of the classical Kleinian surface by an involution).
Classical A_{m-1}: C^2/Z_m = {XY = Z^m}, X=u^m, Y=v^m, Z=uv.
 iota_1 : (X,Y,Z) -> (-X,-Y,Z)  [induced by the generator of Z_{2m} > Z_m]   invariants P=X^2, R=Y^2, Z :  P R = Z^{2m}  => A_{2m-1}
 iota_2 : (X,Y,Z) -> (Y, X, -Z) [induced by j in BD_{4m} > Z_m, m even]     invariants s=X+Y, w=Z^2, t=Z(X-Y):
                                                       t^2 = w s^2 - 4 w^{m/2+1}   => D_{m/2+2}
Rows: (A~_{2n-2},v-a,-1,2delta): m=2n-1, iota_1 -> A_{4n-3}  ; (A~_{2n-1},a-a,(+,-),2delta): m=2n, iota_1 -> A_{4n-1} ;
      (A~_{2n-1},c,2delta): m=2n, iota_2 -> D_{n+2}.  All three match Pinot's Theorem 1.2."""
import sympy as sp
u, v = sp.symbols('u v')
for m in range(2, 12):
    z2m = sp.exp(sp.I*sp.pi/m)                       # generator of Z_{2m}: u -> z u, v -> z^-1 v
    X, Y, Z = u**m, v**m, u*v
    act = lambda f: sp.expand(f.subs({u: z2m*u, v: v/z2m}, simultaneous=True))
    assert sp.simplify(act(X) + X) == 0 and sp.simplify(act(Y) + Y) == 0 and sp.simplify(act(Z) - Z) == 0
    assert sp.expand(X**2 * Y**2 - Z**(2*m)) == 0
    if m % 2 == 0:
        n = m // 2
        jact = lambda f: sp.expand(f.subs({u: -v, v: u}, simultaneous=True))   # j in SU(2)
        assert sp.expand(jact(X) - Y) == 0 and sp.expand(jact(Y) - X) == 0 and sp.expand(jact(Z) + Z) == 0
        s_, w_, t_ = X + Y, Z**2, Z*(X - Y)
        assert sp.expand(t_**2 - (w_*s_**2 - 4*w_**(n + 1))) == 0
print("iota_1: A_{m-1} / iota_1 = A_{2m-1} relation holds, m=2..11; iota_2: A_{2n-1} / iota_2 = D_{n+2} relation holds, n=1..5")
for n in range(2, 7):
    print(f"n={n}: (A~_{2*n-2},v-a,-1,2d): Z_{2*n-1} < Z_{4*n-2} -> A_{4*n-3};  (A~_{2*n-1},a-a,(+,-),2d): Z_{2*n} < Z_{4*n} -> A_{4*n-1};"
          f"  (A~_{2*n-1},c,2d): Z_{2*n} < BD_{4*n} -> D_{n+2}")
