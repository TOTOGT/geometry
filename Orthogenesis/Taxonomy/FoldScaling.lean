-- GATE-DECLARE: sorries = none
-- GATE-REASON: why the fold is scale-agnostic — the normal form ẋ = μ + x² maps to itself under x ↦ bx, μ ↦ b²μ, t ↦ t/b; square-root law and recovery-rate scaling.
/-
Orthogenesis/Taxonomy/FoldScaling.lean — the fold has no preferred scale.

Near any fold the dynamics reduce to the normal form ẋ = μ + x². This file proves:
  §1  The vector field is covariant: (b²μ) + (bx)² = b²(μ + x²).
  §2  Solutions map to solutions: if x(t) solves ẋ = μ + x², then y(t) = b·x(bt) solves
      ẏ = b²μ + y². Rescaling space by b, the control by b² and time by 1/b gives the same
      equation back — the normal form is a fixed point of this rescaling, with the control a
      relevant direction of exponent 2.
  §3  Resting states exist iff μ ≤ 0, at x = ±√(−μ).
  §4  Square-root law: at distance d from the fold the states sit ±√d apart, and at distance
      b²d they sit b times farther: √(b²d) = b√d. The recovery rate at the stable state, 2√d,
      obeys the same law, so relaxation slows like 1/√d near the fold.
  (The passage time π/√r just past a fold is proved in Orthogenesis/Immune/CommitmentThreshold.)
These are the exponents shared across fields; where the fold sits, and in what units, are not.
-/
import Mathlib

namespace Orthogenesis.FoldScaling

/-! ## §1  Covariance of the field -/

theorem field_covariant (b μ x : ℝ) : b ^ 2 * μ + (b * x) ^ 2 = b ^ 2 * (μ + x ^ 2) := by ring

/-! ## §2  Solutions rescale to solutions -/

theorem rescale_solution (b μ : ℝ) (x : ℝ → ℝ) (hx : ∀ t, HasDerivAt x (μ + x t ^ 2) t) (t : ℝ) :
    HasDerivAt (fun s => b * x (b * s)) (b ^ 2 * μ + (b * x (b * t)) ^ 2) t := by
  have h1 : HasDerivAt (fun s => b * s) b t := by
    simpa using (hasDerivAt_id' t).const_mul b
  have h2 := ((hx (b * t)).comp t h1).const_mul b
  refine h2.congr_deriv ?_
  ring

/-! ## §3  Resting states -/

theorem rest_iff (μ : ℝ) : (∃ x : ℝ, μ + x ^ 2 = 0) ↔ μ ≤ 0 := by
  constructor
  · rintro ⟨x, hx⟩; nlinarith [sq_nonneg x]
  · intro h
    exact ⟨Real.sqrt (-μ), by rw [Real.sq_sqrt (by linarith)]; ring⟩

/-! ## §4  Square-root law -/

theorem sqrt_law {b d : ℝ} (hb : 0 ≤ b) :
    Real.sqrt (b ^ 2 * d) = b * Real.sqrt d := by
  rw [Real.sqrt_mul (sq_nonneg b), Real.sqrt_sq hb]

/-- At μ = −d the stable state is x = −√d, where the linearised field has slope 2x = −2√d. -/
theorem stable_state {d : ℝ} (hd : 0 < d) :
    -d + (-Real.sqrt d) ^ 2 = 0 ∧ 2 * (-Real.sqrt d) < 0 := by
  refine ⟨by rw [neg_sq, Real.sq_sqrt hd.le]; ring, ?_⟩
  have := Real.sqrt_pos.mpr hd; linarith

end Orthogenesis.FoldScaling

#print axioms Orthogenesis.FoldScaling.field_covariant
#print axioms Orthogenesis.FoldScaling.rescale_solution
#print axioms Orthogenesis.FoldScaling.rest_iff
#print axioms Orthogenesis.FoldScaling.sqrt_law
#print axioms Orthogenesis.FoldScaling.stable_state
