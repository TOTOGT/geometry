#!/usr/bin/env python3
"""
wp96-verify.py — regenerates every computed claim in
Principia Orthogona, Book VI, WP-96, "The Second Instrument".

Repo rule: a published number must be regenerable by a tool.

SCOPE. The physics here is standard and is not claimed as a result. What is
claimed is a correction to WP-79's own bookkeeping: its filter is stated as a
general principle ("ratios are falsifiable, scales are not") and is valid only
for spectrum instruments. The sorting is redone in block [5].

TAG. No `#Machine Learning` tag. Applying the rule of 2026-09-01: this paper's
finding is a domain result — which physical quantities an instrument class can
refute — occasioned by an external experiment. Machine assistance found it;
assistance used is not the test, assistance as the subject is. Same class as
WP-90, which reports defects in an external preprint and carries no tag either.
Run:  python3 wp96-verify.py     (exits non-zero on any failure)
Requires: sympy
"""
import sympy as sp

FAIL = []
def check(label, got, want):
    ok = (sp.simplify(got - want) == 0) if isinstance(got, sp.Expr) else (got == want)
    print(("  OK   " if ok else "  FAIL ") + label + f"   got={got}  want={want}")
    if not ok: FAIL.append(label)

a, b = sp.symbols('a b', positive=True)          # energy, time rescalings
E1, E2, T, hbar, mu, Ts = sp.symbols('E_1 E_2 T hbar mu T_star', positive=True)

print("\n[1] WP-79's filter is correct for the instrument it considered")
check("level ratio is invariant under E -> aE", sp.simplify((a*E1)/(a*E2)), E1/E2)
check("rate x period is invariant under t -> bt", sp.simplify((mu/b)*(b*Ts)), mu*Ts)

print("\n[2] a phase is dimensionless but NOT scale-invariant")
phase = E1*T/hbar
check("phase picks up the factor a", sp.simplify((a*E1)*T/hbar), a*phase)
print("       so 'dimensionless' and 'scale-invariant' are different properties,")
print("       and WP-79's filter tests the second while the eye reads the first.")

print("\n[3] the free-fall phase is dimensionless in SI base units")
from sympy.physics import units as u
from sympy.physics.units import kg, m as metre, s, J
dim = (kg * (metre/s**2) * metre * s) / (J*s)          # m g h T / hbar
check("[m g h T / hbar] = 1", sp.simplify(u.convert_to(dim, [kg, metre, s])), 1)
print("       every factor in it carries a scale; the quotient is still observable.")

print("\n[4] why: hbar is not a free parameter")
print("""       PROVENANCE. This is NOT a new observation about physics. It is the
       operating principle of atom interferometry as a metrology field: cold-atom
       gravimeters measure g ABSOLUTELY, and h/m recoil interferometry measures the
       fine structure constant (Parker et al. 2018, Cs; Morel et al. 2020, Rb).
       Those are absolute determinations of scales, by exactly this mechanism.
       Nothing below is offered to that community as news. The finding is internal:
       WP-79 ran its falsifiability audit against one instrument class and stated
       the conclusion without the qualifier.""")
print("""       A spectrum instrument reports E_n/E_m and every scale cancels.
       An action instrument reports S/hbar, and hbar is fixed by nature, so the
       rescaling symmetry WP-79 quotients by is BROKEN by the apparatus. That is
       the whole difference, and it is why an interferometer can refute a scale
       that no spectroscopy can touch.""")

print("\n[5] the sorting WP-79 performed, redone against two columns")
rows = [
    # name,                       ratio-exposed, action-exposed
    ("k-nacci roots eta_k",            False, False),   # theorems about polynomial roots
    ("level ratios (CFT data)",        True,  True ),
    ("mu_max * T*  (Floquet)",         True,  True ),
    ("T*  (period alone)",             False, True ),
    ("mu_max  (rate alone)",           False, True ),
    ("light-cone velocity v",          False, True ),
]
print("       %-28s %-14s %-14s" % ("quantity", "ratio instr.", "action instr."))
for n, r, p in rows:
    print("       %-28s %-14s %-14s" % (n, "exposed" if r else "—", "exposed" if p else "—"))
moved = [n for n, r, p in rows if p and not r]
check("quantities that move once the second column exists", len(moved), 3)
print("       moved:", ", ".join(moved))
print("""       The k-nacci roots do not move and cannot: they are theorems about roots
       of polynomials, exposed to no measurement of any kind. WP-79 said so and
       that verdict stands.""")

print("\n" + ("ALL CHECKS PASSED" if not FAIL else "FAILURES: " + ", ".join(FAIL)))
raise SystemExit(1 if FAIL else 0)
