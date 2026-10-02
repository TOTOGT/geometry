#!/usr/bin/env python3
"""
gibbs-check.py — Principia Orthogona, Book IV, Chapter 21, section 21.8
Verifies the algebraic claims relating the corpus contact form to the Gibbs form, and
checks the two statements about cost that the chapter text makes.

Run:  python3 gibbs-check.py     (exits non-zero on any failure)
Requires: sympy

Revised 2026-10-02 (audit of ch-term-set-to-zero, Book 3 page 1). What changed, and why:
  * The earlier check (1) compared `form(dU=1, dJ=-Om)` with an identical copy of itself and
    could not fail. It is replaced by a PULLBACK of the Gibbs form along an explicit dictionary map
    from the corpus coordinates (z, r, theta), with controls that a wrong dictionary must fail.
  * The earlier Legendre check typed dG by hand; dG is now differentiated by sympy.
  * The Clausius and "Legendrian = reversible" lines were `print` statements. They are now tests,
    and the second one is a test of a CORRECTED statement (see CHECKS 5 and 6).

What this file does NOT establish: that any physical system is described by the corpus form.
It checks algebra and two counterexamples to over-strong wording; nothing more.
"""
import sympy as sp
from fractions import Fraction

FAIL = []
def check(ok, msg):
    print('  [%s] %s' % ('PASS' if ok else 'FAIL', msg))
    if not ok: FAIL.append(msg)

# ------------------------------------------------------------ coordinates on the extended phase space
U, S, J, T, Om = sp.symbols('U S J T Omega', real=True)
X = [U, S, J, T, Om]                       # coordinates; a 1-form is its list of coefficients
alpha_G = [sp.Integer(1), -T, -Om, 0, 0]   # dU - T dS - Omega dJ

def pullback(form, phi, params):
    """Pull the 1-form `form` (coefficients over X) back along phi: params -> X."""
    sub = dict(zip(X, phi))
    return [sp.simplify(sum(sp.sympify(form[i]).subs(sub) * sp.diff(sp.sympify(phi[i]), p) for i in range(len(X)))) for p in params]

z, r, th, S0, T0 = sp.symbols('z r theta S0 T0', real=True)
corpus = [sp.Integer(1), sp.Integer(0), -r**2]       # dz - r^2 dtheta, written in ITS OWN coordinates (z, r, theta)

print('CHECK 1: the corpus form is the Gibbs form restricted to a constant-entropy hypersurface')
print('   dictionary: U = z, S = S0 (constant), J = theta, T = T0 (constant), Omega = r^2')
phi = [z, S0, th, T0, r**2]
pb = pullback(alpha_G, phi, [z, r, th])
check(all(sp.simplify(a - b) == 0 for a, b in zip(pb, corpus)), 'pullback of dU - T dS - Omega dJ equals dz - r^2 dtheta')
print('   control: a wrong dictionary must fail')
phi_bad = [z, S0, th, T0, r]                         # Omega = r instead of r^2
pb_bad = pullback(alpha_G, phi_bad, [z, r, th])
check(not all(sp.simplify(a - b) == 0 for a, b in zip(pb_bad, corpus)), 'with Omega = r the pullback is NOT dz - r^2 dtheta')
phi_bad2 = [z, S0, r**2, T0, th]                     # theta and r^2 swapped between the J and Omega slots
pb_bad2 = pullback(alpha_G, phi_bad2, [z, r, th])
check(not all(sp.simplify(a - b) == 0 for a, b in zip(pb_bad2, corpus)), 'with the J and Omega slots exchanged the pullback is NOT dz - r^2 dtheta')
print('   NOTE: this fixes the roles. theta takes the slot of J (the differentiated variable) and r^2 takes the slot of Omega.')
print('   It is a formal match of slots, not an identification of an angle with an angular momentum.')

print('\nCHECK 2: Legendre transform G = U - Omega*J leaves the contact form unchanged (dG differentiated, not typed)')
G = U - Om * J
dG = [sp.diff(G, x) for x in X]
alpha_prime = [dG[i] + [0, -T, 0, 0, J][i] for i in range(5)]    # dG - T dS + J dOmega
check(all(sp.simplify(a - b) == 0 for a, b in zip(alpha_prime, alpha_G)), 'dG - T dS + J dOmega == dU - T dS - Omega dJ')
alpha_prime_bad = [dG[i] + [0, +T, 0, 0, J][i] for i in range(5)]  # flip the sign of the T dS term
check(not all(sp.simplify(a - b) == 0 for a, b in zip(alpha_prime_bad, alpha_G)), 'control: flipping the sign of the T dS term breaks it')

print('\nCHECK 3: along a process, alpha_G(gamma-dot) = dQ - T dS  (first law dU = dQ + Omega dJ; algebra only)')
dQ, dS_, dJ_ = sp.symbols('dQ dS_ dJ_')
dU_proc = dQ + Om * dJ_
alpha_on = dU_proc * alpha_G[0] + dS_ * alpha_G[1] + dJ_ * alpha_G[2]
check(sp.simplify(alpha_on - (dQ - T * dS_)) == 0, 'alpha_G(gamma-dot) == dQ - T dS')

print('\nCHECK 4 (worked counterexample, exact arithmetic; it shows a wording fails, it does not test a model):')
print('   on the constant-entropy restriction alpha(gamma-dot) is the heat dQ, so dS = 0 is NOT free of cost')
# alpha = dU - Omega dJ = dQ. A path with dS = 0 and dQ < 0 (the system gives up heat) has entropy production
# dS - dQ/T = -dQ/T > 0 if Clausius holds with equality only for reversible processes.
T_ = Fraction(300)
for dq in (Fraction(-1), Fraction(-5, 2)):
    produced = Fraction(0) - dq / T_
    check(produced > 0, 'dS = 0, dQ = %s at T = 300: entropy produced = %s > 0 (so "on an adiabat nothing is spent" needs dQ = 0 too)' % (dq, produced))
check(Fraction(0) - Fraction(0) / T_ == 0, 'dS = 0 and dQ = 0 (reversible adiabatic, i.e. on a Legendrian leaf): entropy produced = 0')

print('\nCHECK 5 (worked counterexample, exact arithmetic): alpha_G = 0 does NOT imply the process is reversible overall')
# System in internal equilibrium at T1 receives heat dQ from a reservoir at T2 > T1.
# The system's own entropy change is dS = dQ/T1, so alpha_G = dQ - T1*dS = 0: the path is Legendrian.
T1, T2, dq = Fraction(300), Fraction(400), Fraction(1)
dS_sys = dq / T1
a_val = dq - T1 * dS_sys
produced_total = dS_sys - dq / T2                    # system entropy gain + reservoir entropy change (-dq/T2)
check(a_val == 0, 'T1 = 300, T2 = 400, dQ = 1: alpha_G = %s (the path is Legendrian)' % a_val)
check(produced_total == Fraction(1, 300) - Fraction(1, 400) and produced_total > 0, 'total entropy produced = dQ(1/T1 - 1/T2) = %s > 0 (the process is irreversible)' % produced_total)
T2b = T1
check((dS_sys - dq / T2b) == 0, 'control: with T2 = T1 the same path is reversible overall, total production 0')
print('   So: Legendrian = quasi-static for the SYSTEM. Reversible overall also needs no finite temperature difference with the')
print('   reservoir. Clausius\'s T is the reservoir (boundary) temperature, not a coordinate on the system\'s phase space.')
print('   -alpha_G/T is the system\'s internal entropy production only.')

print('\nCHECK 6: Clausius with the boundary temperature: dS >= dQ/T_boundary for the system (stated as input, not derived here)')
print('   (not checked: this is the second law, taken as given)')

print('\nALL CHECKS PASSED' if not FAIL else '\nFAILURES: %d' % len(FAIL))
raise SystemExit(1 if FAIL else 0)
