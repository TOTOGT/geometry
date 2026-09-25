-- GATE-DECLARE: sorries = none
-- GATE-REASON: new file 2026-09-25 for the geometry pin (Lean v4.32.0, Mathlib v4.32.0).
-- UNTESTED until the author runs `lake build` on it.
/-
# NeuralOscillations.lean — Book 3, Chapter 4 · Neural Oscillations (taught path 30,
# ch4-neural.html; the same page serves the Cajueiro edition)

The neural room (NeuralDynamics.lean, chapters 16–19) checks the dm³ neural
parameters. This file checks chapter 4's own mathematics.

  §1  The Hopf normal form ż = (λ + iω)z − |z|²z. Its energy identity
      Re(z̄ ż) = λ|z|² − |z|⁴ gives the radial equation ṙ = λr − r³. For λ ≤ 0
      every r > 0 decays; for λ > 0 the circle r = √λ is a cycle, attracting
      from inside and outside. The critical value is λ* = 0, and AT λ* there is
      no cycle of positive radius: the amplitude √λ grows from zero as λ passes
      λ*. The phase equation is θ̇ = ω for every λ — the bifurcation does not
      select a frequency, so "40 Hz" is an input to the model, not an output.
  §2  Theorem 4.1's coherence C = |⟨e^{i(φ₁−φ₂)}⟩| (the phase-locking value)
      lies in [0, 1]. It equals 1 for ANY constant phase difference —
      anti-phase (δ = π) included — so C = 1 means phase-locked, not "firing in
      phase". Two samples at differences 0 and π give C = 0.
  §3  Arithmetic in the text: 40 Hz for 45 minutes is 108,000 cycles, and one
      40 Hz cycle lasts 25 ms.

Not formalised: the information bound in Theorem 4.1 (the data-processing
inequality does not by itself give a bound in terms of C), K* itself, and the
theta-gamma biology.
-/

import Mathlib

namespace Orthogenesis.NeuralOscillations

open Complex

/-! ## §1 The Hopf normal form -/

/-- Re(z̄ ż) = λ|z|² − |z|⁴ for ż = (λ + iω)z − |z|²z, i.e. d|z|²/dt = 2(λ|z|² − |z|⁴). -/
theorem hopf_energy (lam ω : ℝ) (z : ℂ) :
    ((starRingEnd ℂ) z * (((lam : ℂ) + (ω : ℂ) * I) * z - (normSq z : ℂ) * z)).re
      = lam * normSq z - normSq z ^ 2 := by
  simp only [mul_re, mul_im, sub_re, sub_im, add_re, add_im, conj_re, conj_im,
    ofReal_re, ofReal_im, I_re, I_im, normSq_apply]
  ring

/-- ṙ = λr − r³. -/
def radial (lam r : ℝ) : ℝ := lam * r - r ^ 3

/-- λ ≤ 0: every oscillation decays. -/
theorem radial_decay {lam r : ℝ} (hl : lam ≤ 0) (hr : 0 < r) : radial lam r < 0 := by
  unfold radial
  nlinarith [mul_nonpos_of_nonpos_of_nonneg hl hr.le, pow_pos hr 3]

/-- λ ≥ 0: r = √λ is a cycle. -/
theorem radial_cycle {lam : ℝ} (hl : 0 ≤ lam) : radial lam (Real.sqrt lam) = 0 := by
  have h := Real.sq_sqrt hl
  unfold radial
  rw [show Real.sqrt lam ^ 3 = Real.sqrt lam ^ 2 * Real.sqrt lam by ring, h]
  ring

/-- Inside the cycle the amplitude grows. -/
theorem radial_grows_inside {lam r : ℝ} (hl : 0 < lam) (hr0 : 0 < r)
    (hrs : r < Real.sqrt lam) : 0 < radial lam r := by
  have h := Real.sq_sqrt hl.le
  have hr2 : r ^ 2 < lam := by
    nlinarith [mul_pos (sub_pos.2 hrs) (by linarith : 0 < Real.sqrt lam + r)]
  unfold radial
  nlinarith [mul_pos hr0 (sub_pos.2 hr2)]

/-- Outside the cycle it decays: the cycle attracts from both sides. -/
theorem radial_decays_outside {lam r : ℝ} (hl : 0 ≤ lam) (hrs : Real.sqrt lam < r) :
    radial lam r < 0 := by
  have h := Real.sq_sqrt hl
  have hs := Real.sqrt_nonneg lam
  have hr0 : 0 < r := lt_of_le_of_lt hs hrs
  have hr2 : lam < r ^ 2 := by
    nlinarith [mul_pos (sub_pos.2 hrs) (by linarith : 0 < r + Real.sqrt lam)]
  unfold radial
  nlinarith [mul_pos hr0 (sub_pos.2 hr2)]

/-- At the critical value λ* = 0 the only cycle radius is 0. -/
theorem no_cycle_at_critical {r : ℝ} (hr : radial 0 r = 0) : r = 0 := by
  unfold radial at hr
  have h3 : r ^ 3 = 0 := by linarith
  exact (pow_eq_zero_iff (by norm_num)).1 h3

/-! ## §2 The phase-locking value -/

/-- C = |(1/n) Σ e^{i δ_k}| for phase differences δ_k. -/
noncomputable def plv {n : ℕ} (d : Fin n → ℝ) : ℝ :=
  ‖(n : ℂ)⁻¹ * ∑ k, exp ((d k : ℂ) * I)‖

theorem plv_le_one {n : ℕ} (hn : 0 < n) (d : Fin n → ℝ) : plv d ≤ 1 := by
  unfold plv
  rw [norm_mul, norm_inv, Complex.norm_natCast]
  have hsum : ‖∑ k, exp ((d k : ℂ) * I)‖ ≤ n := by
    calc ‖∑ k, exp ((d k : ℂ) * I)‖ ≤ ∑ k : Fin n, ‖exp ((d k : ℂ) * I)‖ :=
          norm_sum_le _ _
      _ = n := by simp [Complex.norm_exp_ofReal_mul_I]
  have hn' : (0 : ℝ) < n := by exact_mod_cast hn
  rw [inv_mul_le_iff₀ hn']
  linarith

/-- Any constant phase difference — in phase or not — gives C = 1. -/
theorem plv_const {n : ℕ} (hn : 0 < n) (δ : ℝ) : plv (fun _ : Fin n => δ) = 1 := by
  unfold plv
  have hn' : (n : ℂ) ≠ 0 := by exact_mod_cast hn.ne'
  simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
  rw [← mul_assoc, inv_mul_cancel₀ hn', one_mul, Complex.norm_exp_ofReal_mul_I]

/-- Anti-phase locking (δ = π at every sample) is fully coherent. -/
theorem plv_antiphase_locked : plv (fun _ : Fin 1 => Real.pi) = 1 :=
  plv_const (by norm_num) Real.pi

/-- Samples at differences 0 and π cancel: C = 0. -/
theorem plv_cancel : plv ![(0 : ℝ), Real.pi] = 0 := by
  unfold plv
  simp [Fin.sum_univ_two, Complex.exp_pi_mul_I]

/-! ## §3 Arithmetic in the text -/

theorem gamma_cycles_45min : (40 : ℝ) * (45 * 60) = 108000 := by norm_num

theorem gamma_period_25ms : (1 : ℝ) / 40 = 0.025 := by norm_num

end Orthogenesis.NeuralOscillations

/-! ## Axiom probe -/
#print axioms Orthogenesis.NeuralOscillations.hopf_energy
#print axioms Orthogenesis.NeuralOscillations.radial_decay
#print axioms Orthogenesis.NeuralOscillations.radial_cycle
#print axioms Orthogenesis.NeuralOscillations.radial_grows_inside
#print axioms Orthogenesis.NeuralOscillations.radial_decays_outside
#print axioms Orthogenesis.NeuralOscillations.no_cycle_at_critical
#print axioms Orthogenesis.NeuralOscillations.plv_le_one
#print axioms Orthogenesis.NeuralOscillations.plv_const
#print axioms Orthogenesis.NeuralOscillations.plv_antiphase_locked
#print axioms Orthogenesis.NeuralOscillations.plv_cancel
#print axioms Orthogenesis.NeuralOscillations.gamma_cycles_45min
#print axioms Orthogenesis.NeuralOscillations.gamma_period_25ms
