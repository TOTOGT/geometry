#!/usr/bin/env python3
"""ch05_audit_check.py -- read-only checks of Chapter 5 beyond the Sator letter count (audit 2026-11-15). Complements ch05_sator_count_check.py."""
import sys, itertools, numpy as np, sympy as sp
bad = 0
def ck(n, ok):
    global bad; bad += (not ok); print(('PASS ' if ok else 'FAIL ') + n)
w = ['SATOR', 'AREPO', 'TENET', 'OPERA', 'ROTAS']
ck('only TENET is a palindrome (SATOR<->ROTAS, AREPO<->OPERA)', [x for x in w if x == x[::-1]] == ['TENET'] and w[0] == w[4][::-1] and w[1] == w[3][::-1])
g = [list(r) for r in w]
T = [[g[j][i] for j in range(5)] for i in range(5)]
R180 = [[g[4-i][4-j] for j in range(5)] for i in range(5)]
R90 = [[g[4-j][i] for j in range(5)] for i in range(5)]
AT = [[g[4-j][4-i] for j in range(5)] for i in range(5)]
ck('square invariant under transpose, 180 rotation, anti-transpose', T == g and R180 == g and AT == g)
ck('square is NOT invariant under a 90 degree rotation (symmetry group is the Klein four-group, order 4)', R90 != g)
diag_fixed = [(i, i, g[i][i]) for i in range(5)]
ck('cells fixed by transpose alone are the whole diagonal S,R,N,R,S; only the centre is fixed by the whole group', ''.join(c for _, _, c in diag_fixed) == 'SRNRS')
# page: "reads identically ... and as a torus (wraps)": test cyclic shifts of rows
shifts = [k for k in range(1, 5) if all(g[i][(j+k) % 5] == g[i][j] for i in range(5) for j in range(5))]
ck('"reads the same as a torus (wraps)" has no support: no nontrivial cyclic column shift preserves the grid', shifts == [])
# Cartan distribution rank
a1 = sp.Matrix([[ -sp.Symbol('p1'), 1, 0, 0, 0]]); a2 = sp.Matrix([[ -sp.Symbol('p2'), 0, 1, 0, 0]])
A = sp.Matrix.vstack(a1, a2)
ck('ker(alpha1) ∩ ker(alpha2) on J^1(R,R^2) has dimension 5-2 = 3 (rank 3 on a 5-manifold = codimension 2, not the rank-4 hyperplane field a contact structure needs)', A.rank() == 2 and 5-A.rank() == 3)
# dm3 manifold -> J^1(R,R): alpha = dz - r^2 dtheta with (x,y,p) = (theta, z, r^2)
r, th, z = sp.symbols('r theta z', positive=True)
print('INFO substitution (x,y,p)=(theta,z,r^2) turns dy - p dx into dz - r^2 dtheta (identity by inspection, not a test)')
print('NOTE hand argument, not computed: that substitution is a contactomorphism of {r>0, theta real} onto the open subset {p>0} of J^1(R,R), not onto all of J^1(R,R); "contactomorphic to J^1(R,R)" holds only locally / onto that subset (and not if theta is an angle mod 2pi).')
# z as independent variable: zdot = r^2 - 2 (r-1)^2 e^{-z} can be <= 0
rr, zz = np.meshgrid(np.linspace(0.05, 2, 400), np.linspace(-3, 3, 400))
zd = rr**2 - 2*(rr-1)**2*np.exp(-zz)
ck('zdot = r^2 - 2(r-1)^2 e^{-z} takes both signs on the sampled region, so it vanishes on a hypersurface: z is a local independent variable only where zdot != 0 and p2 = 1/zdot is undefined at zdot = 0', (zd > 0).any() and (zd < 0).any())
ck('on r=1: zdot = 1, p1 = 0, p2 = 1 (the attractor curve prolongs to a Legendrian curve in J^1)', sp.simplify((r**2 - 2*(r-1)**2*sp.exp(-z)).subs(r, 1)) == 1)
print('NOTE hand argument, not computed: Theorem 5.1 (Backlund) is classical (Olver); not re-derived here (as the page says). The page cites "Chapter 23, §23.6–22.7": the second number is a typo for 23.7; ch23 has sections 23.6 and 23.7 (not re-audited for this claim here).')
sys.exit(1 if bad else 0)
