-- GATE-DECLARE: sorries = none
-- GATE-REASON: new file 2026-09-25 for the geometry pin (Lean v4.32.0, Mathlib v4.32.0).
-- Author's build 2026-09-25: OK.
/-
# CoherenceBridge.lean — Book 3, Ch 20 (Theorem 5.4, the Coherence Bridge)
# ========================================================================
# ch20-coherence-bridge.html states that six dm³ systems are "objects in the same
# category, related by explicit contact morphisms", and records (2026-09-19) that
# the identity claim is withdrawn: near Γ each room is the 2×2 linear system with
# eigenvalues μ ± iω, and no two rows of the table are similar, even up to
# rescaling the clock. This file proves that withdrawal from the chapter's own model.
#
#   §1  The model matrix A(μ, ω) = [[μ, −ω], [ω, μ]]: trace 2μ, det μ² + ω².
#   §2  Similarity P⁻¹AP preserves trace and determinant, so rows with different μ are
#       not similar.
#   §3  Similarity up to rescaling the clock (A ↦ c·A, c > 0) preserves μ/ω.
#   §4  The table. All six rows are spiral sinks (the shared functional form). Their
#       μ values and their μ/ω ratios are each strictly increasing in a fixed order,
#       hence pairwise distinct: no two rows are similar, with or without rescaling.
#
# Not formalised: a category of rooms or contact morphisms between them (none is
# defined anywhere in the Lean), and the fact that all 2D linear spiral sinks are
# topologically conjugate (true, not in Mathlib) — which is why sharing that property
# says little.
-/

import Orthogenesis.Neural.NeuralDynamics
import Mathlib

namespace Orthogenesis.CoherenceBridge

open Real Orthogenesis.Plasma Orthogenesis.MarketDynamics Orthogenesis.NeuralDynamics

/-! ## §1 The linear model near Γ -/

/-- Linear part with eigenvalues μ ± iω. -/
def linMat (μ ω : ℝ) : Matrix (Fin 2) (Fin 2) ℝ := !![μ, -ω; ω, μ]

theorem linMat_trace (μ ω : ℝ) : (linMat μ ω).trace = 2 * μ := by
  simp [linMat, Matrix.trace_fin_two, two_mul]

theorem linMat_det (μ ω : ℝ) : (linMat μ ω).det = μ ^ 2 + ω ^ 2 := by
  rw [linMat, Matrix.det_fin_two_of]
  ring

/-! ## §2 Similarity invariants -/

theorem trace_conj {M P : Matrix (Fin 2) (Fin 2) ℝ} (hP : IsUnit P.det) :
    (P⁻¹ * M * P).trace = M.trace := by
  rw [Matrix.trace_mul_comm, ← Matrix.mul_assoc, Matrix.mul_nonsing_inv P hP, Matrix.one_mul]

theorem det_conj {M P : Matrix (Fin 2) (Fin 2) ℝ} (hP : IsUnit P.det) :
    (P⁻¹ * M * P).det = M.det := by
  have h : P.det ≠ 0 := hP.ne_zero
  rw [Matrix.det_mul, Matrix.det_mul, Matrix.det_nonsing_inv, Ring.inverse_eq_inv',
    mul_comm (P.det)⁻¹ M.det, mul_assoc, inv_mul_cancel₀ h, mul_one]

/-- Rows with different μ are not similar. -/
theorem not_similar_of_mu_ne {μ₁ ω₁ μ₂ ω₂ : ℝ} (h : μ₁ ≠ μ₂) :
    ¬ ∃ P : Matrix (Fin 2) (Fin 2) ℝ, IsUnit P.det ∧ P⁻¹ * linMat μ₁ ω₁ * P = linMat μ₂ ω₂ := by
  rintro ⟨P, hP, hs⟩
  have ht := congrArg Matrix.trace hs
  rw [trace_conj hP, linMat_trace, linMat_trace] at ht
  exact h (by linarith)

/-! ## §3 Similarity up to rescaling the clock preserves μ/ω -/

theorem ratio_of_rescaled_similar {μ₁ ω₁ μ₂ ω₂ : ℝ} (hω₁ : 0 < ω₁) (hω₂ : 0 < ω₂)
    (h : ∃ c : ℝ, 0 < c ∧ ∃ P : Matrix (Fin 2) (Fin 2) ℝ,
      IsUnit P.det ∧ P⁻¹ * (c • linMat μ₁ ω₁) * P = linMat μ₂ ω₂) :
    μ₁ / ω₁ = μ₂ / ω₂ := by
  obtain ⟨c, hc, P, hP, hs⟩ := h
  have ht := congrArg Matrix.trace hs
  have hd := congrArg Matrix.det hs
  rw [trace_conj hP, Matrix.trace_smul, linMat_trace, linMat_trace, smul_eq_mul] at ht
  rw [det_conj hP, Matrix.det_smul, linMat_det, linMat_det] at hd
  simp only [Fintype.card_fin] at hd
  have hμ : μ₂ = c * μ₁ := by linarith
  have hpos : 0 < c * ω₁ := mul_pos hc hω₁
  have h2 : ω₂ ^ 2 = (c * ω₁) ^ 2 := by
    rw [hμ] at hd
    nlinarith
  have hω : ω₂ = c * ω₁ := by
    nlinarith [sq_nonneg (ω₂ - c * ω₁), sq_nonneg (ω₂ + c * ω₁)]
  rw [hμ, hω, mul_div_mul_left _ _ hc.ne']

/-! ## §4 The table of Theorem 5.4 -/

/-- HPA stress: μ = −0.38 s⁻¹, ω = 0.21 rad/s, β = 1.9. -/
noncomputable def hpa : DM3Params := ⟨-0.38, 0.21, 1.9⟩
/-- Circadian clock: μ = −0.29 s⁻¹, ω = 2π/86400 rad/s, β = 1.6. -/
noncomputable def circadian : DM3Params := ⟨-0.29, 2 * π / 86400, 1.6⟩
/-- Immune adaptation: μ = −0.44 s⁻¹, ω = 0.18 rad/s, β = 2.0. -/
noncomputable def immune : DM3Params := ⟨-0.44, 0.18, 2.0⟩

/-- Spiral sink: trace < 0, det > 0, trace² < 4·det. -/
def IsSpiralSink (p : DM3Params) : Prop :=
  (linMat p.mu p.omega).trace < 0 ∧ 0 < (linMat p.mu p.omega).det ∧
    (linMat p.mu p.omega).trace ^ 2 < 4 * (linMat p.mu p.omega).det

theorem spiral_sink_of {p : DM3Params} (hμ : p.mu < 0) (hω : p.omega ≠ 0) : IsSpiralSink p := by
  unfold IsSpiralSink
  rw [linMat_trace, linMat_det]
  have hω2 : 0 < p.omega ^ 2 := lt_of_le_of_ne (sq_nonneg _) (Ne.symm (pow_ne_zero 2 hω))
  refine ⟨by linarith, by nlinarith [sq_nonneg p.mu], by nlinarith⟩

/-- All six rows are spiral sinks — the shared functional form, and all they share. -/
theorem all_rows_spiral_sinks :
    IsSpiralSink hpa ∧ IsSpiralSink neural ∧ IsSpiralSink circadian ∧
      IsSpiralSink immune ∧ IsSpiralSink plasma ∧ IsSpiralSink market := by
  have hc : (0 : ℝ) < 2 * π / 86400 := by positivity
  refine ⟨spiral_sink_of (by norm_num [hpa]) (by norm_num [hpa]),
    spiral_sink_of (by norm_num [neural]) (by norm_num [neural]),
    spiral_sink_of (by norm_num [circadian]) (by simpa [circadian] using hc.ne'),
    spiral_sink_of (by norm_num [immune]) (by norm_num [immune]),
    spiral_sink_of (by norm_num [plasma]) (by norm_num [plasma]),
    spiral_sink_of (by norm_num [market]) (by norm_num [market])⟩

/-- The six μ values are strictly increasing in this order, hence pairwise distinct:
    by `not_similar_of_mu_ne`, no two rows are similar. -/
theorem mu_chain :
    market.mu < neural.mu ∧ neural.mu < immune.mu ∧ immune.mu < plasma.mu ∧
      plasma.mu < hpa.mu ∧ hpa.mu < circadian.mu := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;> norm_num [market, neural, immune, plasma, hpa, circadian]

/-- The six ratios μ/ω are strictly increasing in this order (circadian ≈ −3988,
    plasma −28, immune −2.444, market −2.393, HPA −1.810, neural −1.222), hence pairwise
    distinct: by `ratio_of_rescaled_similar`, no two rows are similar even after
    rescaling the clock. Immune against market is the nearest pair. -/
theorem ratio_chain :
    circadian.mu / circadian.omega < plasma.mu / plasma.omega ∧
      plasma.mu / plasma.omega < immune.mu / immune.omega ∧
      immune.mu / immune.omega < market.mu / market.omega ∧
      market.mu / market.omega < hpa.mu / hpa.omega ∧
      hpa.mu / hpa.omega < neural.mu / neural.omega := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · show (-0.29 : ℝ) / (2 * π / 86400) < -0.42 / 0.015
    have h28 : (-0.42 : ℝ) / 0.015 = -28 := by norm_num
    rw [h28, div_lt_iff₀ (by positivity)]
    have := Real.pi_lt_d2
    linarith
  · show (-0.42 : ℝ) / 0.015 < -0.44 / 0.18
    norm_num
  · show (-0.44 : ℝ) / 0.18 < -0.67 / 0.28
    norm_num
  · show (-0.67 : ℝ) / 0.28 < -0.38 / 0.21
    norm_num
  · show (-0.38 : ℝ) / 0.21 < -0.55 / 0.45
    norm_num

end Orthogenesis.CoherenceBridge

/-! ## Axiom probe -/
#print axioms Orthogenesis.CoherenceBridge.linMat_trace
#print axioms Orthogenesis.CoherenceBridge.linMat_det
#print axioms Orthogenesis.CoherenceBridge.trace_conj
#print axioms Orthogenesis.CoherenceBridge.det_conj
#print axioms Orthogenesis.CoherenceBridge.not_similar_of_mu_ne
#print axioms Orthogenesis.CoherenceBridge.ratio_of_rescaled_similar
#print axioms Orthogenesis.CoherenceBridge.spiral_sink_of
#print axioms Orthogenesis.CoherenceBridge.all_rows_spiral_sinks
#print axioms Orthogenesis.CoherenceBridge.mu_chain
#print axioms Orthogenesis.CoherenceBridge.ratio_chain
