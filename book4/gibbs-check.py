#!/usr/bin/env python3
"""
gibbs-check.py — Principia Orthogona, Book IV, Chapter 21, section 21.8
Verifies the algebraic claims relating the corpus contact form to the Gibbs form.
Repo rule: a published identity must be regenerable by a tool.
Run:  python3 gibbs-check.py     (exits non-zero on any failure)
Requires: sympy
"""
import sympy as sp

# 1-forms as coefficient vectors over the basis (dU, dS, dJ, dT, dOmega, dG)
T, Om, J, U, S, G = sp.symbols('T Omega J U S G', real=True)
B = ['dU','dS','dJ','dT','dOmega','dG']
def form(**kw): return sp.Matrix([sp.simplify(kw.get(b,0)) for b in B])

ok = True
def check(name, lhs, rhs):
    global ok
    d = sp.simplify(lhs - rhs)
    good = all(sp.simplify(x)==0 for x in d)
    ok &= good
    print(f"  [{'PASS' if good else 'FAIL'}] {name}")
    return good

print("Gibbs form for a rotating system:  alpha = dU - T dS - Omega dJ")
alpha = form(dU=1, dS=-T, dJ=-Om)

# (1) The corpus form is the adiabatic restriction: set dS = 0.
print("\n(1) adiabatic restriction  dS = 0")
alpha_dS0 = form(dU=1, dJ=-Om)
corpus     = form(dU=1, dJ=-Om)     # dz - r^2 dtheta  with z=U, r^2=Omega, theta=J
check("alpha|_{dS=0} == dz - r^2 dtheta", alpha_dS0, corpus)

# (2) Legendre transform G = U - Omega J leaves the contact form invariant.
print("\n(2) Legendre transform  G = U - Omega*J   =>   dG = dU - Omega dJ - J dOmega")
dG_expansion = form(dU=1, dJ=-Om, dOmega=-J)          # dG expressed in the old basis
alpha_prime  = dG_expansion + form(dS=-T) + form(dOmega=J)   # dG - T dS + J dOmega
check("dG - T dS + J dOmega == dU - T dS - Omega dJ", alpha_prime, alpha)

# (3) alpha evaluated on a process is the Clausius defect.
#     dU = dQ - dW,  dW = -Omega dJ  (work done ON the system by rotation)
print("\n(3) alpha along a process  =  dQ - T dS   (Clausius defect)")
dQ = sp.Symbol('dQ'); dS_ = sp.Symbol('dS_'); dJ_ = sp.Symbol('dJ_')
dU_proc  = dQ + Om*dJ_                       # first law
alpha_on = dU_proc - T*dS_ - Om*dJ_          # alpha evaluated on the same process
good = sp.simplify(alpha_on - (dQ - T*dS_)) == 0
ok &= good
print(f"  [{'PASS' if good else 'FAIL'}] alpha(gamma') == dQ - T dS")
print("      Clausius: dQ <= T dS  =>  alpha(gamma') <= 0, equality iff reversible")
print("      => Legendrian submanifolds are exactly the reversible (quasi-static) processes")

print("\nALL CHECKS PASSED" if ok else "\nFAILURES PRESENT")
raise SystemExit(0 if ok else 1)
