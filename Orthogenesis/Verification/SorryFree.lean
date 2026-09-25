-- GATE-DECLARE: sorries = none
-- GATE-REASON: new file 2026-09-25 for the geometry pin (Lean v4.32.0, Mathlib v4.32.0).
-- UNTESTED until the author runs `lake build` on it.
/-
# SorryFree.lean — Book 3, Week 14 · Publication · AXLE (taught path 39,
# ch14-axle.html; the same page serves the Cajueiro edition)

  §1  The chapter's Curry–Howard example compiles as written (`myProof`).
      The §2 and §6 code blocks do not: they use undefined names
      (`evidence_set`, `overclaims`, `Claim`, `polII`, …) and an unproved placeholder;
      they are
      pseudocode in Lean syntax and should be labelled so.
  §2  DNA fidelity arithmetic: error rates 10⁻⁵, 10⁻⁷, 10⁻⁹ give 10⁴, 100 and 1
      errors per 10⁹ bases, as printed; for a 3·10⁹-base human genome the last
      stage leaves about 3, not 1.
  §3  Hopfield. With n irreversible steps the error is f₀ⁿ⁺¹, strictly smaller at
      every added step when 0 < f₀ < 1. The chapter's numbers do not fit
      together: Δε = 2–3 k_BT gives f₀ = e⁻³…e⁻² ≈ 0.05–0.14 (not 0.01–0.14),
      and then one proofreading step gives f₀² > 0.0016 — not "≈ 10⁻⁴". 10⁻⁴
      needs f₀ ≈ 0.01, i.e. Δε ≈ 4.6 k_BT.

Not formalised: the link drawn between the n-bonacci constants φₙ → 2 and
error rates (no derivation is given: the error falls by ~100× per rung while
φₙ moves by less than 0.3); Theorems 14.1 and 7.1 (definitions); and the
connectome figures (FlyWire, Nature 2024: about 139,000 neurons and 50 million
synapses — chapter 7 says 140,000, this chapter 130,000 and "2023").
-/

import Mathlib

namespace Orthogenesis.SorryFree

open Real

/-! ## §1 The chapter's Curry–Howard example -/

def MyProposition : Prop := ∀ n : ℕ, n + 0 = n

theorem myProof : MyProposition := fun n => Nat.add_zero n

/-! ## §2 DNA fidelity arithmetic -/

theorem errors_per_billion :
    (1e-5 : ℝ) * 1e9 = 1e4 ∧ (1e-7 : ℝ) * 1e9 = 100 ∧ (1e-9 : ℝ) * 1e9 = 1 := by
  norm_num

theorem errors_per_human_genome : (1e-9 : ℝ) * 3e9 = 3 := by norm_num

/-! ## §3 Kinetic proofreading -/

/-- Error after n irreversible proofreading steps: f₀ⁿ⁺¹. -/
def hopfieldError (f₀ : ℝ) (n : ℕ) : ℝ := f₀ ^ (n + 1)

theorem hopfield_step_improves {f₀ : ℝ} (h0 : 0 < f₀) (h1 : f₀ < 1) (n : ℕ) :
    hopfieldError f₀ (n + 1) < hopfieldError f₀ n := by
  unfold hopfieldError
  rw [pow_succ f₀ (n + 1)]
  exact mul_lt_of_lt_one_right (pow_pos h0 _) h1

/-- Δε = 2–3 k_BT gives f₀ between e⁻³ > 0.04 and e⁻² < 0.14. -/
theorem f0_range : (0.04 : ℝ) < exp (-3) ∧ exp (-2) < 0.14 := by
  have e1 := Real.exp_one_lt_d9
  have e2 := Real.exp_one_gt_d9
  have h3 : exp 3 = exp 1 ^ 3 := by rw [← Real.exp_nat_mul]; norm_num
  have h2 : exp 2 = exp 1 ^ 2 := by rw [← Real.exp_nat_mul]; norm_num
  have c3 : exp 1 ^ 3 < 20.2 := by
    calc exp 1 ^ 3 < (2.7182818286 : ℝ) ^ 3 := by gcongr
      _ < 20.2 := by norm_num
  have c2 : (7.38 : ℝ) < exp 1 ^ 2 := by
    calc (7.38 : ℝ) < (2.7182818283 : ℝ) ^ 2 := by norm_num
      _ < exp 1 ^ 2 := by gcongr
  have m3 : exp (-3) * exp 3 = 1 := by rw [← Real.exp_add]; norm_num
  have m2 : exp (-2) * exp 2 = 1 := by rw [← Real.exp_add]; norm_num
  have p3 := Real.exp_pos (-3)
  have p2 := Real.exp_pos (-2)
  have pE3 : 0 < exp 1 ^ 3 := by positivity
  have pE2 : 0 < exp 1 ^ 2 := by positivity
  rw [h3] at m3
  rw [h2] at m2
  constructor <;> nlinarith

/-- One proofreading step at Δε = 3 k_BT still leaves f₀² > 10⁻⁴. -/
theorem one_step_not_1e4 : (1e-4 : ℝ) < exp (-3) ^ 2 := by
  have := f0_range.1
  nlinarith

end Orthogenesis.SorryFree

/-! ## Axiom probe -/
#print axioms Orthogenesis.SorryFree.myProof
#print axioms Orthogenesis.SorryFree.errors_per_billion
#print axioms Orthogenesis.SorryFree.errors_per_human_genome
#print axioms Orthogenesis.SorryFree.hopfield_step_improves
#print axioms Orthogenesis.SorryFree.f0_range
#print axioms Orthogenesis.SorryFree.one_step_not_1e4
