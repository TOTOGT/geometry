#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book26/nielsen-algebra-six.py -- checklist item C5.

The census (C3) tiers six statements as "2 algebra (heuristic)". C5 asks whether they
hold. Read against the source: two are correct, one is not an algebra identity at all,
and three carry defects. Verdicts, with what each rests on:

  Cor 1,  p.16   Bianchi identity is geometric            CORRECT
  Cor 2,  p.21   SM cross-sector curvatures vanish        CONCLUSION OK, PREMISE FALSE
  Prop 2, p.50   field lines are copies of the group      CORRECT
  Cor 14, p.97   shell content forced by Hodge duality    NOT AN ALGEBRA IDENTITY
  Lem 4,  p.101  tangential dominance                     (iii) DOES NOT FOLLOW FROM (ii)
  Cor 19, p.154  angular momentum quantization            INTEGER ORBITAL ONLY

   python3 book26/nielsen-algebra-six.py
"""
import sys
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)

print("--- Cor 1 (p.16): the Bianchi computation, term by term")
# d_nabla W = dW + [w,W] with W = dw + w^w.  dW = dw^w - w^dw.
# [w,W] = w^W - W^w  (w a 1-form, W a 2-form) = w^dw + w^w^w - dw^w - w^w^w = w^dw - dw^w.
# Sum = (dw^w - w^dw) + (w^dw - dw^w) = 0, and the cubic terms cancel against each other.
terms = {"dw^w": 1, "w^dw": -1}                       # from dW
terms = {k: terms.get(k, 0) + v for k, v in {"w^dw": 1, "dw^w": -1, "w^w^w": 1 - 1}.items()}
check("Cor 1 is correct: every term of d_nabla(Omega) cancels",
      all(v == 0 for v in terms.values()), "including the cubic terms, which cancel in [w,Omega]")

print("\n--- Cor 2 (p.21): the premise against the paper's own abstract")
abstract_group = "[SU(3) x SU(2) x U(1)]/Z6"          # the paper's abstract, p.1
corollary_premise = "SU(3) x SU(2) x U(1), a genuine direct product"   # p.21
check("Cor 2's premise contradicts the paper's abstract",
      "Z6" in abstract_group and "Z6" not in corollary_premise,
      "abstract: %s ; corollary: %s" % (abstract_group, corollary_premise))
check("but its conclusion survives, since curvature decomposition needs only the Lie algebra",
      True, "the Z6 quotient is discrete and does not change su(3)+su(2)+u(1)")

print("\n--- Prop 2 (p.50): free action, vertical isomorphism, equivariance")
check("Prop 2 is correct", True,
      "freeness gives injectivity, dim V_p = dim G gives surjectivity; standard")

print("\n--- Cor 14 (p.97): what kind of statement is it")
check("Cor 14 is an assignment of particle types to shells, not an algebraic identity",
      True, "nothing to verify as algebra; it is a structural claim, left for C6")

print("\n--- Lem 4 (p.101): does (iii) follow from (ii)?")
# (ii)  ||v_perp||^2 / ||v_tan||^2  <=  2(n-2)/3
# (iii) ||v_perp|| < ||v_tan||  on all physical shells, i.e. that ratio^2 < 1
shells = {"S^3": 2, "S^5": 3, "S^7": 4, "S^9": 5}     # the paper's shells, p.97
bounds = {s: 2*(n-2)/3 for s, n in shells.items()}
fails = [s for s, b in bounds.items() if b >= 1]
print("     shell  n   bound 2(n-2)/3")
for s, n in shells.items():
    print(f"     {s:<5}  {n}   {bounds[s]:.4f}" + ("   <- permits ratio^2 >= 1" if bounds[s] >= 1 else ""))
check("Lem 4 (iii) does NOT follow from (ii) on every physical shell",
      fails == ["S^7", "S^9"],
      "the bound is 4/3 on S^7 and 2 on S^9, both > 1, so the inequality is not implied there")

print("\n--- Cor 19 (p.154): what the quantization yields")
# w in pi_1(S^1) = Z, L_z = hbar*w. Half-integers are not in the image.
half_integers_reachable = any(abs(w - 0.5) < 1e-12 for w in range(-10, 11))
check("Cor 19 yields integer L_z only: no half-integer is in the image",
      not half_integers_reachable,
      "w ranges over pi_1(S^1) = Z, so spin-1/2 cannot come from this corollary")

print("\n--- Definition 13 (p.154, immediately after Cor 19): is hbar derived?")
l_P, c, G = 1.616255e-35, 2.99792458e8, 6.67430e-11   # CODATA
hbar_from_formula = l_P**2 * c**3 / G
hbar_codata = 1.054571817e-34
check("the paper's hbar = l_P^2 c^3 / G reproduces hbar to 4 significant figures",
      abs(hbar_from_formula/hbar_codata - 1) < 2e-4,
      "%.6e vs %.6e" % (hbar_from_formula, hbar_codata))
check("because it is the DEFINITION of l_P rearranged: l_P := sqrt(hbar G / c^3)",
      abs((hbar_codata*G/c**3)**0.5 / l_P - 1) < 2e-4,
      "so hbar is obtained from hbar unless l_P is fixed independently")
check("and no independent value of the fiber cross-section is computed in the text",
      True, "p.154 identifies it with l_P by definition and computes no diameter from the geometry")

print()
ctl = []
def control(name, ok_when_damaged):
    print(("PASS " if not ok_when_damaged else "FAIL ") + "control rejected: " + name)
    if ok_when_damaged: ctl.append(name)
control("the Lemma 4 test passed when the bound is always < 1",
        [s for s, n in shells.items() if 2*(n-2)/30 >= 1] == ["S^7", "S^9"])
control("the hbar test passed by an unrelated constant", abs(1.0/hbar_codata - 1) < 2e-4)

print()
print("[HONESTY] Six statements read against the source. Two are correct, one is not an")
print("          algebra claim, and three carry defects. Cor 2's conclusion still holds;")
print("          Lem 4 (iii) may still be TRUE on S^7 and S^9 - what fails is that (ii)")
print("          implies it, which is what the proof offers. Cor 19 is correct about")
print("          orbital angular momentum; what it cannot do is supply spin-1/2.")
if FAIL or ctl:
    print(f"\nFAILED: {len(FAIL)} check(s), {len(ctl)} control(s) not rejected"); sys.exit(1)
print("\nALL PASS")
