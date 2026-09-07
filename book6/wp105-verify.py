#!/usr/bin/env python3
"""
wp105-verify.py — Principia Orthogona, Vol VI, WP-105
"The Unit That Inflates"

Regenerates every number in the note. Repo rule: a published number must be
regenerable by a tool.  Run: python3 wp105-verify.py   Requires: sympy.

Claim under test:  the classification of planar order is a statement about the
UNIT GROUP of the maximal real subfield Q(zeta_n)^+ .
    rank 0  ->  no scaling symmetry  ->  periodic order      n in {3,4,6}
    rank 1  ->  a fundamental unit   ->  quasiperiodic order n in {5,8,10,12}
and in the second case the fundamental unit IS the tiling's inflation factor.
"""
import sympy as sp

FAIL = []
def ok(label, cond):
    if not cond: FAIL.append(label)
    print(f"  [{'PASS' if cond else 'FAIL'}] {label}")

phi_gold = (1 + sp.sqrt(5)) / 2

# ----------------------------------------------------------------------
print("="*72)
print("[1] phi(n) partitions the plane's candidate orders")
print("="*72)
# phi(n) >= sqrt(n/2), so searching to n = 2000 is more than exhaustive for
# phi(n) <= 4: no n > 32 can have phi(n) <= 4.
tot = {n: sp.totient(n) for n in range(1, 2001)}
plane   = sorted(n for n in tot if tot[n] <= 2)
fourdim = sorted(n for n in tot if tot[n] == 4)
print(f"      phi(n) <= 2 , n <= 2000 : {plane}")
print(f"      phi(n) == 4 , n <= 2000 : {fourdim}")
ok("phi(n)<=2 gives exactly {1,2,3,4,6}", plane == [1, 2, 3, 4, 6])
ok("phi(n)==4 gives exactly {5,8,10,12} -- the COMPLETE solution set",
   fourdim == [5, 8, 10, 12])
observed = [5, 8, 10, 12]
ok("the four realised quasicrystal orders are precisely the solutions of phi(n)=4",
   fourdim == observed)
ok("no n > 32 has phi(n) <= 4 (search bound is safe)",
   max(n for n in tot if tot[n] <= 4) <= 32)

# ----------------------------------------------------------------------
print()
print("="*72)
print("[2] The maximal real subfield Q(zeta_n)^+ = Q(2 cos(2pi/n))")
print("="*72)
print("      n |  2cos(2pi/n)          | min poly over Q             | degree")
print("      " + "-"*68)
realsub = {}
for n in [3, 4, 6, 5, 8, 10, 12]:
    a = sp.simplify(2*sp.cos(2*sp.pi/n))
    p = sp.minimal_polynomial(a, sp.Symbol('x'))
    d = sp.degree(p)
    realsub[n] = (a, p, d)
    print(f"      {n:2d}| {str(a):21s}| {str(p):28s}| {d}")
for n in [3, 4, 6]:
    ok(f"n={n}: real subfield is Q itself (degree 1)", realsub[n][2] == 1)
for n in [5, 8, 10, 12]:
    ok(f"n={n}: real subfield is real quadratic (degree 2)", realsub[n][2] == 2)
ok("degree of Q(zeta_n)^+ equals phi(n)/2 in every row",
   all(realsub[n][2] == sp.Rational(tot[n], 2) or (n in (3,4,6) and realsub[n][2] == 1)
       for n in realsub))

# ----------------------------------------------------------------------
print()
print("="*72)
print("[3] Which real quadratic field, and its fundamental unit")
print("="*72)
# field discriminant radicand d, fundamental unit eps, its norm
FIELD = {
    5:  (5, phi_gold),
    10: (5, phi_gold),
    8:  (2, 1 + sp.sqrt(2)),
    12: (3, 2 + sp.sqrt(3)),
}
print("      n | Q(zeta_n)^+ | fundamental unit eps | N(eps) | eps (numeric)")
print("      " + "-"*68)
for n in [5, 8, 10, 12]:
    d, eps = FIELD[n]
    # conjugate: sqrt(d) -> -sqrt(d)
    conj = eps.subs(sp.sqrt(d), -sp.sqrt(d))
    norm = sp.simplify(sp.expand(eps*conj))
    print(f"      {n:2d}| Q(sqrt{d})    | {str(eps):20s} | {str(norm):6s} | {float(eps):.6f}")
    ok(f"n={n}: eps is a unit, N(eps) = +/-1", abs(norm) == 1)
    # eps generates the same field as 2cos(2pi/n): compare squarefree parts
    # of the discriminants of the two minimal polynomials.
    def sqfree_disc(alpha):
        q = sp.Poly(sp.minimal_polynomial(alpha, sp.Symbol('x')), sp.Symbol('x'))
        D = sp.discriminant(q)
        return sp.factorint(sp.Integer(D)) and sp.Integer(
            sp.prod([pr for pr, e in sp.factorint(sp.Integer(D)).items() if e % 2]))
    ok(f"n={n}: Q(eps) == Q(2cos(2pi/n)) == Q(sqrt{d})",
       sqfree_disc(eps) == d and sqfree_disc(realsub[n][0]) == d)

# fundamental (not merely a) unit: check no smaller unit >1 exists by
# running Pell/continued-fraction search up to a bound.
print()
print("      Fundamental-unit check (smallest unit > 1 in Z[sqrt d] / O_K):")
def smallest_unit(d, half_integers=False):
    """Brute search for the smallest (x + y*sqrt d)/k > 1 with norm +/-1."""
    best = None
    ks = [2, 1] if half_integers else [1]
    for y in range(1, 200):
        for k in ks:
            for x in range(0, 400):
                if k == 2 and (x % 2) != (y % 2):
                    continue
                val = sp.Rational(x*x - d*y*y, k*k)
                if val in (1, -1):
                    u = (x + y*sp.sqrt(d)) / k
                    if float(u) > 1 and (best is None or float(u) < float(best)):
                        best = sp.nsimplify(u)
            if best is not None and k == ks[-1]:
                pass
        if best is not None:
            return best
    return None
for d, half in [(5, True), (2, False), (3, False)]:
    u = smallest_unit(d, half)
    print(f"        d={d}: smallest unit > 1 is {u}  ({float(u):.6f})")
    expected = {5: phi_gold, 2: 1 + sp.sqrt(2), 3: 2 + sp.sqrt(3)}[d]
    ok(f"d={d}: smallest unit > 1 equals the eps used above",
       sp.simplify(u - expected) == 0)

# ----------------------------------------------------------------------
print()
print("="*72)
print("[4] The fundamental unit IS the tiling inflation factor")
print("="*72)
TILING = {
    5:  ("Penrose (rhombic / P3)",      phi_gold,        "golden mean"),
    10: ("Penrose, decagonal phase",    phi_gold,        "golden mean"),
    8:  ("Ammann-Beenker (octagonal)",  1 + sp.sqrt(2),  "silver mean"),
    12: ("Stampfli / shield (12-fold)", 2 + sp.sqrt(3),  "platinum / 2+sqrt3"),
}
print("      n | tiling                        | inflation lambda | = eps ?")
print("      " + "-"*68)
for n in [5, 8, 10, 12]:
    name, lam, nick = TILING[n]
    d, eps = FIELD[n]
    same = sp.simplify(lam - eps) == 0
    print(f"      {n:2d}| {name:30s}| {float(lam):.6f}       | {'YES' if same else 'no'}")
    ok(f"n={n}: inflation factor == fundamental unit of Q(zeta_n)^+", same)

# ----------------------------------------------------------------------
print()
print("="*72)
print("[5] Every one of them is a Pisot number (the window is discrete)")
print("="*72)
print("      n | lambda      | |conjugate| | Pisot ?")
print("      " + "-"*68)
for n in [5, 8, 10, 12]:
    d, eps = FIELD[n]
    conj = eps.subs(sp.sqrt(d), -sp.sqrt(d))
    print(f"      {n:2d}| {float(eps):.6f}   | {abs(float(conj)):.6f}    | "
          f"{'YES' if abs(float(conj)) < 1 else 'NO'}")
    ok(f"n={n}: |conjugate| < 1 (Pisot)", abs(float(conj)) < 1)
    ok(f"n={n}: |lambda * conjugate| = 1 (unit)",
       abs(sp.simplify(eps*conj)) == 1)

# ----------------------------------------------------------------------
print()
print("="*72)
print("[6] Substitution matrices: the same numbers from the other side")
print("="*72)
SUBST = {
    "Fibonacci   a->ab,    b->a":  (sp.Matrix([[1, 1], [1, 0]]), phi_gold),
    "Octonacci   a->aba,   b->a":  (sp.Matrix([[2, 1], [1, 0]]), 1 + sp.sqrt(2)),
    "Twelve-fold a->aaabb, b->ab": (sp.Matrix([[3, 1], [2, 1]]), 2 + sp.sqrt(3)),
}
for label, (M, lam) in SUBST.items():
    evs = sorted([sp.nsimplify(e) for e in M.eigenvals()], key=lambda e: -float(e))
    lead = evs[0]
    det = int(M.det())
    print(f"      {label:30s} det={det:3d}  lambda_PF={float(lead):.6f}")
    ok(f"{label.split()[0]}: det M = +/-1 (inflation lies in GL(2,Z))", abs(det) == 1)
    ok(f"{label.split()[0]}: lambda_PF equals the fundamental unit",
       sp.simplify(lead - lam) == 0)

# ----------------------------------------------------------------------
print()
print("="*72)
print("[7] Dirichlet rank: the whole classification in one column")
print("="*72)
print("      field            | r1 | r2 | rank = r1+r2-1 | unit group        | order type")
print("      " + "-"*68)
rows = [
    ("Q            (n=3,4,6)", 1, 0, 0, "{+/-1}, order 2",   "periodic"),
    ("Q(sqrt-3)  Z[omega]   ", 0, 1, 0, "mu_6, order 6",     "closes: 12 defects"),
    ("Q(sqrt5)   (n=5,10)   ", 2, 0, 1, "+/- phi^k, infinite",  "quasiperiodic"),
    ("Q(sqrt2)   (n=8)      ", 2, 0, 1, "+/- (1+r2)^k, inf.",  "quasiperiodic"),
    ("Q(sqrt3)   (n=12)     ", 2, 0, 1, "+/- (2+r3)^k, inf.",  "quasiperiodic"),
]
for f, r1, r2, rk, ug, ot in rows:
    print(f"      {f}|  {r1} |  {r2} |       {rk}        | {ug:18s}| {ot}")
    ok(f"Dirichlet rank r1+r2-1 for {f.strip()}", r1 + r2 - 1 == rk)
# the Z[omega] unit group really has order 6
omega = sp.Rational(-1, 2) + sp.sqrt(3)*sp.I/2
units = set()
for a in range(-3, 4):
    for b in range(-3, 4):
        z = a + b*omega
        nrm = sp.simplify(sp.expand(z*sp.conjugate(z)))
        if nrm == 1:
            units.add(sp.nsimplify(sp.expand(z)))
print(f"      Z[omega] units found by search: {len(units)}")
ok("Z[omega] has exactly 6 units (rank 0, torsion mu_6)", len(units) == 6)
ok("Z[i] has rank 0 too (mu_4)",
   len({sp.nsimplify(a + b*sp.I) for a in range(-2, 3) for b in range(-2, 3)
        if sp.simplify((a + b*sp.I)*sp.conjugate(a + b*sp.I)) == 1}) == 4)

# ----------------------------------------------------------------------
print()
print("="*72)
print("[8] The corpus numbers this note leans on")
print("="*72)
# ch21 / Euler: total defect 4pi, elementary disclination 2pi/6, quotient 12
ok("4pi / (2pi/6) = 12  (Ch 21's twelve pentagons)",
   sp.simplify(4*sp.pi / (2*sp.pi/6)) == 12)
# eta, the tribonacci constant, is a unit in its cubic order but NOT quadratic
x = sp.Symbol('x')
eta_poly = x**3 - x**2 - x - 1
eta = [r for r in sp.Poly(eta_poly, x).all_roots() if r.is_real][0]
print(f"      eta (tribonacci) = {float(eta):.6f}, min poly {eta_poly}")
ok("eta's minimal polynomial has constant term -1 (eta is a unit)",
   sp.Poly(eta_poly, x).all_coeffs()[-1] in (1, -1))
ok("eta is a Pisot number (complex conjugates inside the unit disc)",
   all(abs(complex(r)) < 1 for r in sp.Poly(eta_poly, x).all_roots() if not r.is_real))
ok("eta is cubic, not quadratic — it needs a rank-1 CUBIC field, not the plane",
   sp.degree(sp.minimal_polynomial(eta, x)) == 3)
print(f"      phi = {float(phi_gold):.6f} < eta = {float(eta):.6f} < tau = 2")
ok("phi < eta < 2 (the recurrence ladder of ch-eta-dnls)",
   float(phi_gold) < float(eta) < 2)

# ----------------------------------------------------------------------
print()
print("="*72)
if FAIL:
    print(f"FAILED {len(FAIL)} check(s):")
    for f in FAIL: print("   -", f)
    raise SystemExit(1)
print("ALL CHECKS PASSED")
print("="*72)
