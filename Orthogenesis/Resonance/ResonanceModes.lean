-- GATE-DECLARE: sorries = none
-- GATE-REASON: new file 2026-09-25 for the geometry pin (Lean v4.32.0, Mathlib v4.32.0).
-- UNTESTED until the author runs `lake build` on it.
/-
# ResonanceModes.lean — Book 3, Chapter 6 · Resonance (taught path 32,
# ch6-resonance.html; the same page serves the Cajueiro edition)

  §1  Schumann. c / 2πR with c = 3·10⁸ m/s, R = 6.371·10⁶ m lies in (7.47, 7.50) Hz,
      and the ideal fundamental (c / 2πR)·√2 lies in (10.5, 10.7) Hz: the
      chapter's 7.49 and 10.6 check. (The observed 7.83 Hz is ~26% below the
      ideal value, the top of the chapter's "18–26%".)
  §2  Chladni modes on the unit square, ψ_nm(x, y) = sin(nπx)·sin(mπy).
      Mode (1,1) has NO interior nodal line (it is positive inside the square),
      so it is not "a single cross"; the cross is mode (2,2) (nodal lines
      x = 1/2 and y = 1/2, four squares). Modes (1,2) and (2,1) have the same
      frequency (1² + 2² = 2² + 1²), and their difference vanishes on the whole
      diagonal y = x while their sum does not: one frequency, two different
      patterns. So the pattern is not "the unique solution … at that frequency".
  §3  Theorem 6.1. Rescaling one shape preserves its nodal pattern, but a square
      plate and a spherical shell are different shapes with different spectra:
      the sphere's first two frequencies are in ratio √(2·3/(1·2)) = √3, the
      square's √(5/2). They are not one family.

Not formalised: the Laplacian eigenvalue computation itself (standard), the
free-edge boundary condition of real Chladni plates (these ψ are the
simply-supported / membrane modes), Bloch waves (travelling, not standing, away
from the zone boundary), and the EEG claims.
-/

import Mathlib

namespace Orthogenesis.ResonanceModes

open Real

/-! ## §1 Schumann resonance -/

/-- c / 2πR in Hz. -/
noncomputable def schumannBase : ℝ := 3e8 / (2 * π * 6.371e6)

theorem schumannBase_bounds : 7.47 < schumannBase ∧ schumannBase < 7.5 := by
  have h1 := Real.pi_gt_d2
  have h2 := Real.pi_lt_d2
  have hd : 0 < 2 * π * 6.371e6 := by positivity
  unfold schumannBase
  constructor
  · rw [lt_div_iff₀ hd]
    nlinarith
  · rw [div_lt_iff₀ hd]
    nlinarith

theorem sqrt_two_bounds : 1.414 < Real.sqrt 2 ∧ Real.sqrt 2 < 1.415 := by
  have h := Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)
  have hs := Real.sqrt_nonneg 2
  constructor <;> nlinarith

/-- Ideal (lossless) fundamental (c / 2πR)·√(1·2) ∈ (10.5, 10.7) Hz. -/
theorem schumann_ideal_f1 :
    10.5 < schumannBase * Real.sqrt 2 ∧ schumannBase * Real.sqrt 2 < 10.7 := by
  obtain ⟨b1, b2⟩ := schumannBase_bounds
  obtain ⟨s1, s2⟩ := sqrt_two_bounds
  constructor <;> nlinarith

/-! ## §2 Chladni modes on the unit square -/

/-- ψ_nm(x, y) = sin(nπx) sin(mπy). -/
noncomputable def psi (n m : ℕ) (x y : ℝ) : ℝ := Real.sin (n * π * x) * Real.sin (m * π * y)

/-- Mode (1,1) is positive inside the square: no interior nodal line. -/
theorem psi11_pos {x y : ℝ} (hx0 : 0 < x) (hx1 : x < 1) (hy0 : 0 < y) (hy1 : y < 1) :
    0 < psi 1 1 x y := by
  simp only [psi, Nat.cast_one, one_mul]
  exact mul_pos
    (Real.sin_pos_of_pos_of_lt_pi (mul_pos pi_pos hx0) (mul_lt_of_lt_one_right pi_pos hx1))
    (Real.sin_pos_of_pos_of_lt_pi (mul_pos pi_pos hy0) (mul_lt_of_lt_one_right pi_pos hy1))

/-- Mode (2,2) vanishes on x = 1/2 (and, by symmetry, on y = 1/2): the cross. -/
theorem psi22_cross (y : ℝ) : psi 2 2 (1 / 2) y = 0 := by
  simp only [psi]
  rw [show ((2 : ℕ) : ℝ) * π * (1 / 2) = π by push_cast; ring, Real.sin_pi, zero_mul]

/-- The difference of the degenerate modes (1,2), (2,1) vanishes on the diagonal … -/
theorem psi_diff_diagonal (x : ℝ) : psi 1 2 x x - psi 2 1 x x = 0 := by
  simp only [psi]
  ring

/-- … but their sum does not. -/
theorem psi_sum_off_diagonal : 0 < psi 1 2 (1 / 4) (1 / 4) + psi 2 1 (1 / 4) (1 / 4) := by
  simp only [psi]
  rw [show ((1 : ℕ) : ℝ) * π * (1 / 4) = π / 4 by push_cast; ring,
    show ((2 : ℕ) : ℝ) * π * (1 / 4) = π / 2 by push_cast; ring, Real.sin_pi_div_two]
  have h := Real.sin_pos_of_pos_of_lt_pi (by positivity : 0 < π / 4)
    (by linarith [Real.pi_pos] : π / 4 < π)
  simp only [mul_one, one_mul]
  linarith

/-! ## §3 Different shapes, different spectra -/

/-- Sphere: f₂/f₁ = √3. Square: f₁₂/f₁₁ = √(5/2). -/
theorem spectra_differ : Real.sqrt 3 ≠ Real.sqrt (5 / 2) := by
  intro h
  rw [Real.sqrt_inj (by norm_num) (by norm_num)] at h
  norm_num at h

end Orthogenesis.ResonanceModes

/-! ## Axiom probe -/
#print axioms Orthogenesis.ResonanceModes.schumannBase_bounds
#print axioms Orthogenesis.ResonanceModes.sqrt_two_bounds
#print axioms Orthogenesis.ResonanceModes.schumann_ideal_f1
#print axioms Orthogenesis.ResonanceModes.psi11_pos
#print axioms Orthogenesis.ResonanceModes.psi22_cross
#print axioms Orthogenesis.ResonanceModes.psi_diff_diagonal
#print axioms Orthogenesis.ResonanceModes.psi_sum_off_diagonal
#print axioms Orthogenesis.ResonanceModes.spectra_differ
