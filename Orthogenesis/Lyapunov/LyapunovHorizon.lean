-- GATE-DECLARE: sorries = none
-- GATE-REASON: new file 2026-09-25 for the geometry pin (Lean v4.32.0, Mathlib v4.32.0).
-- UNTESTED until the author runs `lake build` on it.
/-
# LyapunovHorizon.lean — Book 3, Week 10 · Lyapunov Stability (taught path 35,
# ch10-lyapunov.html; the same page serves the Cajueiro edition)

A separation growing at rate λ is δ(t) = δ₀·e^{λt}.

  §1  The horizon formula T* = (1/λ)·ln(Δ_max/Δ₀) is right: δ(T*) = Δ_max.
      The doubling time is ln 2 / λ.
  §2  The weather paragraph mixes two rates. λ ≈ 0.9 per day gives a doubling
      time of ln 2 / 0.9 ≈ 0.77 days and a ten-day growth factor e⁹ > 8000;
      "doubles roughly every day … 2¹⁰ = 1024" is the rate λ = ln 2 ≈ 0.69 per
      day. The two statements differ by a factor of about 8 over ten days.
      (0.906 is also the leading Lyapunov exponent of the Lorenz-63 model in
      its own dimensionless time; reading it as "per day" needs a conversion
      the chapter does not give.)

Not formalised: the heart-rate exponents (no units or source given), and
Theorem 10.1, which is a definition of robustness rather than a theorem.
-/

import Mathlib

namespace Orthogenesis.LyapunovHorizon

open Real

/-- δ(t) = δ₀ e^{λt}. -/
noncomputable def sep (δ₀ lam t : ℝ) : ℝ := δ₀ * exp (lam * t)

/-- §1: the horizon T* = (1/λ) ln(Δ_max/Δ₀) is reached exactly. -/
theorem horizon_spec {δ₀ Δ lam : ℝ} (h0 : 0 < δ₀) (hΔ : 0 < Δ) (hl : lam ≠ 0) :
    sep δ₀ lam ((1 / lam) * Real.log (Δ / δ₀)) = Δ := by
  unfold sep
  rw [show lam * ((1 / lam) * Real.log (Δ / δ₀)) = Real.log (Δ / δ₀) by field_simp,
    Real.exp_log (div_pos hΔ h0)]
  field_simp [h0.ne']

/-- The doubling time is ln 2 / λ. -/
theorem doubling_time (δ₀ : ℝ) {lam : ℝ} (hl : lam ≠ 0) :
    sep δ₀ lam (Real.log 2 / lam) = 2 * δ₀ := by
  unfold sep
  rw [show lam * (Real.log 2 / lam) = Real.log 2 by field_simp,
    Real.exp_log (by norm_num)]
  ring

/-- §2: at λ = 0.9 per day, ten days multiply an error by e⁹ > 8000, not 1024. -/
theorem ten_days_at_0_9 : (1024 : ℝ) < 8000 ∧ (8000 : ℝ) < exp (0.9 * 10) := by
  refine ⟨by norm_num, ?_⟩
  have h := Real.exp_one_gt_d9
  have h9 : exp (0.9 * 10) = exp 1 ^ 9 := by
    rw [← Real.exp_nat_mul]
    norm_num
  rw [h9]
  have hp : (2.7182818283 : ℝ) ^ 9 < exp 1 ^ 9 := by gcongr
  have hn : (8000 : ℝ) < 2.7182818283 ^ 9 := by norm_num
  linarith

/-- Doubling once a day is λ = ln 2, and ln 2 < 0.7 < 0.9. -/
theorem daily_doubling_rate : Real.log 2 < 0.7 := by
  have := Real.log_two_lt_d9
  linarith

end Orthogenesis.LyapunovHorizon

/-! ## Axiom probe -/
#print axioms Orthogenesis.LyapunovHorizon.horizon_spec
#print axioms Orthogenesis.LyapunovHorizon.doubling_time
#print axioms Orthogenesis.LyapunovHorizon.ten_days_at_0_9
#print axioms Orthogenesis.LyapunovHorizon.daily_doubling_rate
