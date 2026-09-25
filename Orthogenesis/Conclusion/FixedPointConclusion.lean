-- GATE-DECLARE: sorries = none
-- GATE-REASON: new file 2026-09-25 for the geometry pin (Lean v4.32.0, Mathlib v4.32.0).
-- UNTESTED until the author runs `lake build` on it.
/-
# FixedPointConclusion.lean — Book 3, Week 12 · Fixed Point (taught path 37,
# ch12-conclusion.html; the same page serves the Cajueiro edition)

  §1  Theorem 12.1 (Banach), as stated, is Mathlib's: a contraction with
      constant K < 1 on a nonempty complete metric space has a fixed point x*,
      the iterates converge to it, and d(xₙ, x*) ≤ d(x₀, x₁)·Kⁿ/(1 − K); and
      d(x₀, x*) ≤ d(x₀, x₁)/(1 − K) — §4's "small first revision ⇒ already near
      x*" is exactly this bound.
  §2  "L ≥ 1: no fixed point / no convergence" is not what Banach says. L ≥ 1
      only removes the guarantee. x ↦ 1.2x has L = 1.2 and a unique fixed point
      (0), which repels; the identity has L = 1 and every point fixed.
  §3  The chapter's numbers: at L = 0.5, three steps leave 1/8 of the error; at
      L = 0.9, reaching 1% takes 44 steps (0.9⁴³ > 0.01 > 0.9⁴⁴).

PedagogyDynamics.lean (chapter 6) already proves that convergence is only in
the limit (after 14 steps the distance is |1 − k|¹⁴·d ≠ 0) and that a
contraction has one fixed point for every seed.

Not formalised: the homeostatic L values (no source), and Theorem 12.2, a
definition of a finished Conclusion.
-/

import Mathlib

namespace Orthogenesis.FixedPointConclusion

open NNReal

/-! ## §1 Banach with the chapter's error bound -/

variable {α : Type*} [MetricSpace α] [Nonempty α] [CompleteSpace α] {K : ℝ≥0} {f : α → α}

theorem banach_fixed (hf : ContractingWith K f) :
    Function.IsFixedPt f (ContractingWith.fixedPoint f hf) :=
  hf.fixedPoint_isFixedPt

theorem banach_error_bound (hf : ContractingWith K f) (x : α) (n : ℕ) :
    dist (f^[n] x) (ContractingWith.fixedPoint f hf) ≤ dist x (f x) * (K : ℝ) ^ n / (1 - K) :=
  hf.apriori_dist_iterate_fixedPoint_le x n

/-- §4: the distance from the first draft to x* is at most (first revision)/(1 − K). -/
theorem first_revision_bound (hf : ContractingWith K f) (x : α) :
    dist x (ContractingWith.fixedPoint f hf) ≤ dist x (f x) / (1 - K) :=
  hf.dist_fixedPoint_le x

/-! ## §2 L ≥ 1 does not mean "no fixed point" -/

/-- x ↦ 1.2x has exactly one fixed point, 0. -/
theorem expanding_has_fixed_point (x : ℝ) : (1.2 : ℝ) * x = x ↔ x = 0 := by
  constructor
  · intro h; linarith
  · intro h; subst h; ring

/-- The identity (L = 1) fixes every point. -/
theorem identity_all_fixed (x : ℝ) : Function.IsFixedPt (id : ℝ → ℝ) x := rfl

/-! ## §3 The chapter's numbers -/

theorem three_rounds_half : (0.5 : ℝ) ^ 3 = 0.125 := by norm_num

theorem slow_contraction_44 : (0.01 : ℝ) < 0.9 ^ 43 ∧ (0.9 : ℝ) ^ 44 < 0.01 := by
  norm_num

end Orthogenesis.FixedPointConclusion

/-! ## Axiom probe -/
#print axioms Orthogenesis.FixedPointConclusion.banach_fixed
#print axioms Orthogenesis.FixedPointConclusion.banach_error_bound
#print axioms Orthogenesis.FixedPointConclusion.first_revision_bound
#print axioms Orthogenesis.FixedPointConclusion.expanding_has_fixed_point
#print axioms Orthogenesis.FixedPointConclusion.identity_all_fixed
#print axioms Orthogenesis.FixedPointConclusion.three_rounds_half
#print axioms Orthogenesis.FixedPointConclusion.slow_contraction_44
