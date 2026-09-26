-- GATE-DECLARE: sorries = none
-- GATE-REASON: new file 2026-09-26 for the geometry pin (Lean v4.32.0, Mathlib v4.32.0).
-- UNTESTED until the author runs `lake build` on it.
/-
# HawkingConstants.lean — Book 7 Ch H (ch-hawking.html) and Book 8 Ch 10
# (book8/ch10-thermodynamics.html): which constant-matchings are content.

  §1  Ch H identifies τ = 2 inside 8π = 4πτ. Proved: the identity holds, and
      4π·t = 8π forces t = 2 — so exhibiting τ = 2 is solving for t, not
      evidence that dm³'s τ is the 2 in the Bekenstein–Hawking factor.
  §2  Ch H identifies ε* = 1/3 inside S = A/4 = (A·ε*)/(4/3). Proved: it holds
      for EVERY area A, so no measurement could disagree with it; and the same
      move works with any nonzero constant in place of 1/3, so the appearance
      of ε* is not evidence for ε*. This is WP70 §5's point, checked.
  §3  What survives in Ch H needs no constant to coincide: the irreducible mass
      M_irr = √(A/16π) is monotone in horizon area, so the area theorem makes
      it a Lyapunov function for the flow. Proved as monotonicity.
  §4  Book 8 Ch 10 states T_H^contact = T_H^classical·(1 + ln η/2π) ≈ 1.097·T_H,
      η the Tribonacci constant, and calls the 9.7% shift universal and
      observable. The arithmetic is confirmed here to the stated precision.
      The arithmetic is all that is confirmed: this file does not derive the
      correction, and the chapter does not either — "the Tribonacci weight of
      the contact form" is the insertion §2 shows to be unconstraining. A
      universal shift in the temperature of every black hole is a physical
      claim and needs a derivation, not a matching factor.
-/

import Mathlib

namespace Orthogenesis.HawkingConstants

open Real

/-! ## §1 The 8π = 4πτ match is solving for τ -/

theorem eight_pi_eq_four_pi_two : 8 * π = 4 * π * 2 := by ring

theorem four_pi_mul_eq_eight_pi_iff (t : ℝ) : 4 * π * t = 8 * π ↔ t = 2 := by
  have hπ : π ≠ 0 := Real.pi_ne_zero
  constructor
  · intro h
    field_simp at h
    linarith
  · rintro rfl; ring

/-! ## §2 The ε* identity holds for every area, and for every constant -/

theorem epsilon_identity (A : ℝ) : (A * (1 / 3)) / (4 / 3) = A / 4 := by ring

theorem any_constant_inserts (A c : ℝ) (hc : c ≠ 0) : (A * c) / (4 * c) = A / 4 := by
  field_simp

/-! ## §3 What survives: the irreducible mass is monotone in area -/

noncomputable def irrMass (A : ℝ) : ℝ := Real.sqrt (A / (16 * π))

theorem irrMass_mono {A B : ℝ} (h : A ≤ B) : irrMass A ≤ irrMass B := by
  unfold irrMass
  apply Real.sqrt_le_sqrt
  have h16 : (0 : ℝ) < 16 * π := by positivity
  exact div_le_div_of_nonneg_right h h16.le

theorem irrMass_nonneg (A : ℝ) : 0 ≤ irrMass A := Real.sqrt_nonneg _

/-! ## §4 Book 8 Ch 10's Tribonacci factor: the arithmetic only -/

/-- The Tribonacci constant, to the precision the chapter uses. -/
def etaApprox : ℝ := 1.8392867552

/-- 1 + (ln η)/(2π) ≈ 1.097, as the chapter states. Checked to 3 decimals
    against ln η ≈ 0.6093778, which is the value this bound assumes. -/
theorem tribonacci_factor (l : ℝ) (hl : 0.60937 < l ∧ l < 0.60939) :
    1.0969 < 1 + l / (2 * π) ∧ 1 + l / (2 * π) < 1.0971 := by
  obtain ⟨h1, h2⟩ := hl
  have hpl : (3.1415 : ℝ) < π := Real.pi_gt_d4
  have hpu : π < 3.1416 := Real.pi_lt_d4
  have hp : (0 : ℝ) < 2 * π := by positivity
  have hqm : (l / (2 * π)) * (2 * π) = l := by
    field_simp
  have hqpos : 0 < l / (2 * π) := div_pos (by linarith) hp
  constructor
  · nlinarith [hqm, hqpos, hpl, hpu, h1, h2]
  · nlinarith [hqm, hqpos, hpl, hpu, h1, h2]

end Orthogenesis.HawkingConstants

/-! ## Axiom probe -/
#print axioms Orthogenesis.HawkingConstants.eight_pi_eq_four_pi_two
#print axioms Orthogenesis.HawkingConstants.four_pi_mul_eq_eight_pi_iff
#print axioms Orthogenesis.HawkingConstants.epsilon_identity
#print axioms Orthogenesis.HawkingConstants.any_constant_inserts
#print axioms Orthogenesis.HawkingConstants.irrMass_mono
#print axioms Orthogenesis.HawkingConstants.irrMass_nonneg
#print axioms Orthogenesis.HawkingConstants.tribonacci_factor
