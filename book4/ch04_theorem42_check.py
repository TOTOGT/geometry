"""ch04 check (2026-11-14): what System (3.1)/(4.1) and alpha = dz - r^2 dtheta actually give.
Prints (1) the w-independent facts that ARE derivable, (2) why the w-exponent is undetermined.
Exit 0 if all derivable checks hold."""
import sympy as sp
r,th,z,t=sp.symbols('r theta z t',positive=True)
rdot=r*(1-r**2)+2*(r-1)*sp.exp(-z)
# (a) linearisation in r at r=1
lam=sp.simplify(sp.diff(rdot,r).subs(r,1)); print("d(rdot)/dr at r=1 =",lam)
assert sp.simplify(lam-(2*sp.exp(-z)-2))==0
print("  -> exponent in r is 2e^{-z}-2 : in (-2,0] for z>=0 ; equals -2 only as z->inf")
# (b) Reeb field of alpha = dz - r^2 dtheta is d_z (alpha(d_z)=1, no dz in d alpha). The attractor at r=1:
# zdot = r^2 = 1, thetadot = 1 -> orbit tangent T = d_theta + d_z, a HELIX z = z0 + theta, not a closed curve.
Ttheta,Tz=1,1; alpha_T=Tz-1**2*Ttheta
print("alpha(T) along r=1 orbit =",alpha_T,"-> orbit is Legendrian, not a Reeb orbit; z=z0 constant is NOT invariant (zdot=1)")
assert alpha_T==0
# (c) contour integral and disk area
loop=sp.integrate(-1*1,(th,0,2*sp.pi)); print("oint_gamma alpha =",loop)
area=sp.integrate(sp.integrate(2*r,(r,0,1)),(th,0,2*sp.pi)); print("|int_D d alpha| over r<=1 =",area)
assert area==2*sp.pi and abs(loop)==2*sp.pi
print("  -> area 2*pi is just |oint alpha| = 2*pi*r^2 at r=1 (Stokes); it is the theta-period times r^2, not a Lyapunov quantity")
print("wdot = s(r,theta,z,w) is unspecified in the chapter -> w-exponent undetermined")
print("ALL DERIVABLE CHECKS PASSED")
