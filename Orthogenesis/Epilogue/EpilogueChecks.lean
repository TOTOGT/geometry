-- GATE-DECLARE: sorries = none
-- GATE-REASON: new file 2026-09-26 for the geometry pin (Lean v4.32.0, Mathlib v4.32.0).
-- UNTESTED until the author runs `lake build` on it.
/-
# EpilogueChecks.lean — Book 3, Ch 17 · Epilogue (ch17-epilogue.html)

  §1  17.1 says the reader converges "by the Banach Fixed-Point Theorem" and the
      coda says "what you converge to depends on the initial condition x₀". Both
      cannot hold: a contraction has at most one fixed point, so every seed ends
      at the same x*. Contrapositive proved here: a map with two distinct fixed
      points is not a contraction. (PedagogyDynamics.contraction_fixed_points_eq and
      all_seeds_same_limit already prove the direct form.) Different readers ending
      in different places is modelled by the fold's bistable window
      (FoldHysteresis.bistable), not by Banach.
  §2  Prompt 10.2 calls "the proportion of claims with direct evidence" a spectral
      radius and 17.2 says it "must be below 1". A proportion is at most 1 and
      equals 1 exactly when every claim has evidence, so the test fails for a
      fully evidenced paper.
  §3  "Converges in three drafts ⇒ L ≈ 0.5" fixes a tolerance of 1/8 without saying
      so (FixedPointConclusion.three_rounds_half). At L = 0.5, a 1% tolerance takes
      seven rounds.
-/

import Mathlib

namespace Orthogenesis.EpilogueChecks

/-! ## §1 Two fixed points rule out a contraction -/

theorem distinct_fixed_points_not_contracting {α : Type*} [MetricSpace α]
    {K : NNReal} {f : α → α} {a b : α}
    (ha : f a = a) (hb : f b = b) (hab : a ≠ b) : ¬ ContractingWith K f := by
  intro hf
  have h1 : dist a b ≤ (K : ℝ) * dist a b := by
    have := hf.2.dist_le_mul a b
    rwa [ha, hb] at this
  have hpos : 0 < dist a b := dist_pos.mpr hab
  have hK : (K : ℝ) < 1 := by exact_mod_cast hf.1
  nlinarith

/-! ## §2 A proportion is not a spectral-radius test -/

theorem evidence_ratio_le_one (k n : ℕ) (hk : k ≤ n) : (k : ℝ) / n ≤ 1 := by
  rcases Nat.eq_zero_or_pos n with rfl | hn
  · simp
  · rw [div_le_one (by exact_mod_cast hn)]
    exact_mod_cast hk

theorem full_evidence_ratio_eq_one (n : ℕ) (hn : 0 < n) : (n : ℝ) / n = 1 :=
  div_self (by exact_mod_cast hn.ne')

theorem full_evidence_fails_below_one (n : ℕ) (hn : 0 < n) : ¬ ((n : ℝ) / n < 1) := by
  rw [full_evidence_ratio_eq_one n hn]
  exact lt_irrefl 1

/-! ## §3 The draft count depends on the tolerance -/

theorem half_reaches_one_percent_in_seven :
    (0.01 : ℝ) < 0.5 ^ 6 ∧ (0.5 : ℝ) ^ 7 < 0.01 := by
  norm_num

end Orthogenesis.EpilogueChecks

/-! ## Axiom probe -/
#print axioms Orthogenesis.EpilogueChecks.distinct_fixed_points_not_contracting
#print axioms Orthogenesis.EpilogueChecks.evidence_ratio_le_one
#print axioms Orthogenesis.EpilogueChecks.full_evidence_ratio_eq_one
#print axioms Orthogenesis.EpilogueChecks.full_evidence_fails_below_one
#print axioms Orthogenesis.EpilogueChecks.half_reaches_one_percent_in_seven
