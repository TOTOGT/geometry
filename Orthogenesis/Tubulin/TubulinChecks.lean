-- GATE-DECLARE: sorries = none
-- GATE-REASON: chT tubulin — units check on κ*, β = 0.382 is φ⁻² not φ⁻¹, P1 seam stagger is lattice geometry, P2's law has no knee.
/-
Orthogenesis/Tubulin/TubulinChecks.lean — Book 3, Chapter T (Tubulin as Computronium).

What the chapter's numbers do and do not support.
  §1  κ* = 2.81 nm⁻¹ exceeds the GDP-protofilament curvature (12° per 8 nm dimer = π/120 nm⁻¹)
      by more than a factor of 100. A curvature of 2.81 nm⁻¹ is a radius of about 0.36 nm,
      smaller than one tubulin monomer.
  §2  β = 0.382 is φ⁻² = 1 − φ⁻¹, not φ⁻¹ (= 0.618…).
  §3  P1's 0.92 nm is the stagger between neighbouring protofilaments in a 13-protofilament,
      3-start lattice: 3·d/13 with monomer spacing d between 4.0 and 4.1 nm lands in (0.92, 0.96).
      It follows from lattice geometry, with no contact form involved.
  §4  P2's law k = A·exp(c(κ − κ*)) has log k affine in κ: a straight line on a log plot, with
      no knee. It cannot produce the "sharp crossover" P2 predicts.
-/
import Mathlib

namespace Orthogenesis.TubulinChecks

/-! ## §1  Units: κ* against the real protofilament curvature -/

/-- GDP protofilament curvature: 12° (= π/15 rad) per 8 nm dimer, in nm⁻¹. -/
noncomputable def kappaGDP : ℝ := Real.pi / 15 / 8

theorem kappa_star_over_hundredfold : 100 * kappaGDP < 281 / 100 := by
  have h : Real.pi < 315 / 100 := by
    have := Real.pi_lt_d2; norm_num at this ⊢; linarith
  unfold kappaGDP; linarith

theorem kappa_star_radius : (1 : ℝ) / (281 / 100) < 4 / 10 := by norm_num

/-! ## §2  β = 0.382 is φ⁻², not φ⁻¹ -/

noncomputable def phi : ℝ := (1 + Real.sqrt 5) / 2

lemma sqrt5_sq : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)

lemma sqrt5_lo : (2236 : ℝ) / 1000 < Real.sqrt 5 := (Real.lt_sqrt (by norm_num)).mpr (by norm_num)

lemma sqrt5_hi : Real.sqrt 5 < 22361 / 10000 := (Real.sqrt_lt' (by norm_num)).mpr (by norm_num)

theorem phi_inv : phi⁻¹ = (Real.sqrt 5 - 1) / 2 :=
  inv_eq_of_mul_eq_one_right (by unfold phi; linear_combination sqrt5_sq / 4)

theorem phi_inv_sq : phi⁻¹ ^ 2 = (3 - Real.sqrt 5) / 2 := by
  rw [phi_inv]; linear_combination sqrt5_sq / 4

theorem beta_matches_phi_inv_sq : 3819 / 10000 < phi⁻¹ ^ 2 ∧ phi⁻¹ ^ 2 < 382 / 1000 := by
  rw [phi_inv_sq]; constructor <;> linarith [sqrt5_lo, sqrt5_hi]

theorem beta_is_not_phi_inv : 382 / 1000 + 23 / 100 < phi⁻¹ := by
  rw [phi_inv]; linarith [sqrt5_lo]

/-! ## §3  P1 is lattice geometry -/

theorem seam_stagger (d : ℝ) (h1 : 4 ≤ d) (h2 : d ≤ 41 / 10) :
    92 / 100 < 3 * d / 13 ∧ 3 * d / 13 < 96 / 100 := by
  constructor <;> linarith

/-! ## §4  P2's law has no knee -/

theorem log_rate_affine (A c κs κ : ℝ) (hA : 0 < A) :
    Real.log (A * Real.exp (c * (κ - κs))) = Real.log A + c * (κ - κs) := by
  rw [Real.log_mul (ne_of_gt hA) (Real.exp_ne_zero _), Real.log_exp]

end Orthogenesis.TubulinChecks

#print axioms Orthogenesis.TubulinChecks.kappa_star_over_hundredfold
#print axioms Orthogenesis.TubulinChecks.phi_inv_sq
#print axioms Orthogenesis.TubulinChecks.beta_matches_phi_inv_sq
#print axioms Orthogenesis.TubulinChecks.beta_is_not_phi_inv
#print axioms Orthogenesis.TubulinChecks.seam_stagger
#print axioms Orthogenesis.TubulinChecks.log_rate_affine
