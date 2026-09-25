-- GATE-DECLARE: sorries = none
-- GATE-REASON: new file 2026-09-25 for the geometry pin (Lean v4.32.0, Mathlib v4.32.0).
-- Author's build 2026-09-25: 12/12 on standard axioms, first try, no warnings.
/-
# NeuralDynamics.lean — neural dynamics in Book 3 (The Mini-Beast)
# ================================================================
# Source chapters (taught path 17–20): ch16-neural.html, ch17-neural-metric.html,
# ch18-neural-curvature.html, ch19-neural-transition.html.
# Builds on Orthogenesis/Plasma/PlasmaRoom.lean and Orthogenesis/Market/MarketDynamics.lean.
#
#   §1  (μ_max, ω, β) = (−0.55 s⁻¹, 0.45 rad/s, 2.1): the transverse rate is negative
#       for z > 0 and tends to −0.55 (same dm³ family as the plasma and market rooms).
#   §2  Timescales carried by those numbers. Half-life ln 2/0.55 > 1 s, fold time
#       π/0.45 > 6.9 s. Both exceed the chapter's 50–200 ms window, so that window is
#       not derived from (μ_max, ω): it needs its own derivation (for instance, that
#       passage through the fold is faster than relaxation onto the new cycle).
#   §3  ch17's metric d = −log C. It is ≥ 0, zero only at C = 1, and unbounded as
#       C → 0 (independence is infinitely distant). It is not a metric: with real
#       correlations ρ₁₂ = ρ₂₃ = 0.9, ρ₁₃ = 0.7 (a positive-definite correlation matrix:
#       leading minors 1, 0.19, 0.024) and C = ρ², d₁₃ > d₁₂ + d₂₃. This confirms the
#       chapter's own caution: curvature computed from −log C is not curvature until
#       an embedding repairs the triangle inequality. d is dimensionless, so the κ*
#       band 0.25–0.35 passes the units-before-data rule.
#
# Not formalised: the coherence data, the 33 Hz question (the chapter itself flags it),
# the modality-invariance test of ch18, and ch19's claim that the four rooms are
# objects in one category related by contact morphisms — no such category or
# morphisms are defined anywhere in the Lean.
-/

import Orthogenesis.Market.MarketDynamics
import Mathlib

namespace Orthogenesis.NeuralDynamics

open Real Filter Topology Orthogenesis.Plasma Orthogenesis.MarketDynamics

/-! ## §1 Parameters -/

/-- μ_max = −0.55 s⁻¹, ω = 0.45 rad/s, β = 2.1 (ch16, ch19). -/
noncomputable def neural : DM3Params := ⟨-0.55, 0.45, 2.1⟩

theorem neural_inFamily : InFamily neural := by
  refine ⟨?_, ?_, ?_⟩ <;> norm_num [neural]

theorem neural_transverseRate_neg {z : ℝ} (hz : 0 < z) :
    transverseRate neural z < 0 :=
  transverseRate_neg neural (by norm_num [neural]) (by norm_num [neural]) hz

theorem neural_transverseRate_tendsto :
    Tendsto (transverseRate neural) atTop (𝓝 (-0.55)) := by
  have := transverseRate_tendsto neural (by norm_num [neural])
  simpa [neural] using this

/-! ## §2 Timescales carried by the normal form -/

/-- Half-life of the envelope e^{μt} at μ = −0.55 s⁻¹ exceeds one second. -/
theorem neural_halfLife_gt_one : 1 < halfLife (-0.55) := by
  have h := Real.log_two_gt_d9
  unfold halfLife
  rw [abs_of_neg (by norm_num : (-0.55 : ℝ) < 0), lt_div_iff₀ (by norm_num)]
  norm_num
  linarith

/-- Fold time π/ω at ω = 0.45 rad/s exceeds 6.9 seconds. -/
theorem neural_foldTime_gt : 6.9 < foldTime 0.45 := by
  have h := Real.pi_gt_d2
  unfold foldTime
  rw [lt_div_iff₀ (by norm_num)]
  linarith

/-- Both timescales exceed the chapter's 200 ms window. -/
theorem neural_timescales_exceed_window :
    (0.2 : ℝ) < halfLife (-0.55) ∧ (0.2 : ℝ) < foldTime 0.45 :=
  ⟨by linarith [neural_halfLife_gt_one], by linarith [neural_foldTime_gt]⟩

/-! ## §3 The coherence distance d = −log C -/

/-- ch17: d = −log C for a coherence C ∈ (0, 1]. -/
noncomputable def coherenceDist (C : ℝ) : ℝ := -Real.log C

theorem coherenceDist_nonneg {C : ℝ} (h0 : 0 < C) (h1 : C ≤ 1) : 0 ≤ coherenceDist C := by
  unfold coherenceDist
  have := Real.log_nonpos h0.le h1
  linarith

theorem coherenceDist_eq_zero_iff {C : ℝ} (h0 : 0 < C) : coherenceDist C = 0 ↔ C = 1 := by
  unfold coherenceDist
  constructor
  · intro h
    have hl : Real.log C = 0 := by linarith
    rcases Real.log_eq_zero.mp hl with h' | h' | h'
    · linarith
    · exact h'
    · linarith
  · rintro rfl
    simp

/-- Independence is infinitely distant: d exceeds every bound for small coherence. -/
theorem coherenceDist_unbounded (M : ℝ) :
    ∃ C : ℝ, 0 < C ∧ C < 1 ∧ M < coherenceDist C := by
  have hneg : -(|M| + 1) < 0 := by
    have := abs_nonneg M
    linarith
  refine ⟨Real.exp (-(|M| + 1)), Real.exp_pos _, ?_, ?_⟩
  · have := Real.exp_lt_exp.mpr hneg
    rwa [Real.exp_zero] at this
  · unfold coherenceDist
    rw [Real.log_exp]
    have := le_abs_self M
    linarith

/-- A real correlation matrix with ρ₁₂ = ρ₂₃ = 0.9, ρ₁₃ = 0.7. -/
def corr3 : Matrix (Fin 3) (Fin 3) ℝ := !![1, 0.9, 0.7; 0.9, 1, 0.9; 0.7, 0.9, 1]

/-- Its leading principal minors are 1, 0.19 and 0.024, all positive, so it is positive
    definite (Sylvester's criterion — stated, not invoked here): these correlations
    can occur. -/
theorem corr3_minors :
    (0 : ℝ) < 1 ∧ (0 : ℝ) < 1 * 1 - 0.9 * 0.9 ∧ 0 < corr3.det := by
  refine ⟨by norm_num, by norm_num, ?_⟩
  rw [corr3, Matrix.det_fin_three]
  simp
  norm_num

/-- With C = ρ², the three coherences are 0.81, 0.81 and 0.49. -/
theorem corr3_coherences :
    corr3 0 1 ^ 2 = 0.81 ∧ corr3 1 2 ^ 2 = 0.81 ∧ corr3 0 2 ^ 2 = 0.49 := by
  simp [corr3]
  norm_num

/-- −log C violates the triangle inequality at those coherences:
    d(0.49) ≈ 0.71 > d(0.81) + d(0.81) ≈ 0.42. -/
theorem coherenceDist_triangle_fails :
    coherenceDist 0.81 + coherenceDist 0.81 < coherenceDist 0.49 := by
  unfold coherenceDist
  have h : Real.log 0.49 < Real.log ((0.81 : ℝ) ^ 2) :=
    Real.log_lt_log (by norm_num) (by norm_num)
  rw [Real.log_pow] at h
  push_cast at h
  linarith

end Orthogenesis.NeuralDynamics

/-! ## Axiom probe -/
#print axioms Orthogenesis.NeuralDynamics.neural_inFamily
#print axioms Orthogenesis.NeuralDynamics.neural_transverseRate_neg
#print axioms Orthogenesis.NeuralDynamics.neural_transverseRate_tendsto
#print axioms Orthogenesis.NeuralDynamics.neural_halfLife_gt_one
#print axioms Orthogenesis.NeuralDynamics.neural_foldTime_gt
#print axioms Orthogenesis.NeuralDynamics.neural_timescales_exceed_window
#print axioms Orthogenesis.NeuralDynamics.coherenceDist_nonneg
#print axioms Orthogenesis.NeuralDynamics.coherenceDist_eq_zero_iff
#print axioms Orthogenesis.NeuralDynamics.coherenceDist_unbounded
#print axioms Orthogenesis.NeuralDynamics.corr3_minors
#print axioms Orthogenesis.NeuralDynamics.corr3_coherences
#print axioms Orthogenesis.NeuralDynamics.coherenceDist_triangle_fails
