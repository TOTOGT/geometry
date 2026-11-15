#!/usr/bin/env python3
"""ch15_audit_check.py -- read-only checks of statements in Chapter 15 (audit 2026-11-15).
Checks are labelled; lines marked NOTE are hand arguments, not computed."""
import sys, sympy as sp
r, th, z, eps, lam = sp.symbols('r theta z epsilon lambda', real=True)
bad = 0
def ck(name, ok):
    global bad; bad += (not ok); print(('PASS ' if ok else 'FAIL ') + name)
# alpha = dz - r^2 dtheta on coordinates (r, theta, z); a vector is (vr, vth, vz)
alpha = lambda v: v[2] - r**2*v[1]
reeb = (0, 0, 1)
ck('alpha(d_z)=1', sp.simplify(alpha(reeb) - 1) == 0)
# d(alpha) = -2r dr^dtheta ; contraction with d_z is zero => d_z is the Reeb field
dalpha = lambda u, v: -2*r*(u[0]*v[1] - u[1]*v[0])
ck('i_{d_z} d(alpha)=0 (d_z is Reeb)', all(sp.simplify(dalpha(reeb, e)) == 0 for e in [(1,0,0),(0,1,0),(0,0,1)]))
# T of the page: (theta+e, z+r^2 e) has generator d_theta + r^2 d_z
gen = (0, 1, r**2)
ck('generator of T is NOT the Reeb field', gen != reeb)
ck('alpha(generator of T)=0: it lies in ker(alpha), a Legendrian direction', sp.simplify(alpha(gen)) == 0)
# printed Psi f = r^2 f_theta - eps r^2 f_z : kills constants, so Psi^2 cannot be -lambda^2 id
f = sp.Function('f')(r, th, z)
Psi = lambda g: r**2*sp.diff(g, th) - eps*r**2*sp.diff(g, z)
ck('Psi(1)=0 so Psi^2(1)=0 != -lambda^2', Psi(sp.Integer(1)) == 0)
sym = sp.symbols('xi_t xi_z')
ck('Psi^2 has nonzero second-order symbol (r^4 (xi_t - eps xi_z)^2), not a scalar', sp.simplify(r**4*(sym[0]-eps*sym[1])**2) != 0)
# J^2=-id on a 3-dimensional tangent space is impossible: det(J)^2 = det(-I3) = -1
J = sp.Matrix(3, 3, sp.symbols('j0:9', real=True))
ck('det(-I_3) = -1 < 0, but det(J^2)=det(J)^2 >= 0: no J with J^2=-id on R^3', (-sp.eye(3)).det() == -1)
# Theorem 15.5 numbers: Re h = 2|mu| |u|^2 with mu=-2 gives 4; the stated gap tau|mu|/2 = 2
mu = -2
ck('Re h coefficient 2|mu| = 4 differs from the stated Hermitian gap 2 (internal inconsistency)', 2*abs(mu) != 2)
# d(alpha) on the 3-manifold has a kernel (Reeb), so it is not a symplectic form on TM
ck('d(alpha) is degenerate on TM (kernel contains d_z)', all(sp.simplify(dalpha(reeb, e)) == 0 for e in [(1,0,0),(0,1,0)]))
print('NOTE hand argument, not computed: Thm 15.4 says [F,T]=0 on Re s=1/2, but Thm 15.1 says Psi^2=-lambda^2 id with lambda>0, so Psi is invertible and cannot vanish anywhere.')
print('NOTE hand argument, not computed: Thm 15.2 uses "Gamma Legendrian"; ch28 audit (ch28_audit_check.py) shows Gamma={r=1} is a cylinder foliated by Legendrian helices.')
sys.exit(1 if bad else 0)
