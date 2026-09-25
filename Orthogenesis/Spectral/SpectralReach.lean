-- GATE-DECLARE: sorries = none
-- GATE-REASON: new file 2026-09-25 for the geometry pin (Lean v4.32.0, Mathlib v4.32.0).
-- UNTESTED until the author runs `lake build` on it.
/-
# SpectralReach.lean — Book 3, Week 11 · Spectral Radius (taught path 36,
# ch11-spectral.html; the same page serves the Cajueiro edition)

  §1  "ρ = 1: the system neither grows nor collapses" fails for the shear
      (x, y) ↦ (x + y, y): its only eigenvalue is 1, yet it sends (0, 1) to
      (n, 1) after n steps — unbounded, linear growth.
  §2  "ρ > 1: iterations Aⁿx → ∞" holds only for x with a component along an
      expanding direction: (x, y) ↦ (2x, y/2) has ρ = 2 and sends (0, 1) to
      (0, (1/2)ⁿ) → 0.
  §3  Herd immunity. With a fraction p immune, the reproduction number is
      (1 − p)·R₀, which is below 1 exactly when p > 1 − 1/R₀. For the chapter's
      values: R₀ = 2.5 needs 60%; measles at R₀ = 12–18 needs about 92–94%.
  §4  "Like the Fibonacci sequence approaching φ … without crossing it": the
      ratios of consecutive Fibonacci numbers alternate around φ —
      2/1 > φ, 3/2 < φ, 5/3 > φ — they cross it at every step.

Not formalised: Theorem 11.1 (a definition of a well-pitched Discussion, not a
theorem), the ρ values assigned to claim types, and the R₀ estimates themselves.
-/

import Mathlib

namespace Orthogenesis.SpectralReach

/-! ## §1 The shear: ρ = 1, unbounded growth -/

def shear (p : ℝ × ℝ) : ℝ × ℝ := (p.1 + p.2, p.2)

/-- The shear's only eigenvalue is 1. -/
theorem shear_eigen {p : ℝ × ℝ} {c : ℝ} (hp : p ≠ 0) (h : shear p = c • p) : c = 1 := by
  obtain ⟨x, y⟩ := p
  simp only [shear, Prod.smul_mk, smul_eq_mul, Prod.mk.injEq] at h
  obtain ⟨h1, h2⟩ := h
  by_cases hy : y = 0
  · subst hy
    have hx : x ≠ 0 := by
      intro hx; apply hp; simp [hx]
    have : x * (c - 1) = 0 := by linarith
    rcases mul_eq_zero.1 this with h | h
    · exact absurd h hx
    · linarith
  · have : y * (c - 1) = 0 := by linarith
    rcases mul_eq_zero.1 this with h | h
    · exact absurd h hy
    · linarith

theorem shear_iter (n : ℕ) : shear^[n] (0, 1) = ((n : ℝ), 1) := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [Function.iterate_succ_apply', ih]
    simp [shear]

theorem shear_unbounded (M : ℝ) : ∃ n : ℕ, M < (shear^[n] (0, 1)).1 := by
  obtain ⟨n, hn⟩ := exists_nat_gt M
  exact ⟨n, by rw [shear_iter]; exact hn⟩

/-! ## §2 ρ = 2, yet some orbits decay -/

noncomputable def stretch (p : ℝ × ℝ) : ℝ × ℝ := (2 * p.1, p.2 / 2)

theorem stretch_iter (n : ℕ) : stretch^[n] (0, 1) = (0, (1 / 2 : ℝ) ^ n) := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [Function.iterate_succ_apply', ih]
    ext
    · simp [stretch]
    · simp only [stretch]
      ring

/-! ## §3 Herd immunity -/

theorem herd_threshold {R₀ p : ℝ} (hR : 0 < R₀) : (1 - p) * R₀ < 1 ↔ 1 - 1 / R₀ < p := by
  constructor
  · intro h
    have : 1 - p < 1 / R₀ := by rw [lt_div_iff₀ hR]; linarith
    linarith
  · intro h
    have : 1 - p < 1 / R₀ := by linarith
    rw [lt_div_iff₀ hR] at this
    linarith

theorem herd_values :
    1 - 1 / (2.5 : ℝ) = 0.6 ∧ (0.91 : ℝ) < 1 - 1 / 12 ∧ (1 : ℝ) - 1 / 18 < 0.95 := by
  norm_num

/-! ## §4 Fibonacci ratios alternate around φ -/

noncomputable def phi : ℝ := (1 + Real.sqrt 5) / 2

theorem fib_ratios_alternate : (3 / 2 : ℝ) < phi ∧ phi < 5 / 3 ∧ (5 / 3 : ℝ) < 2 / 1 := by
  have h := Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 5)
  have hs := Real.sqrt_nonneg 5
  unfold phi
  refine ⟨?_, ?_, by norm_num⟩ <;> nlinarith

end Orthogenesis.SpectralReach

/-! ## Axiom probe -/
#print axioms Orthogenesis.SpectralReach.shear_eigen
#print axioms Orthogenesis.SpectralReach.shear_iter
#print axioms Orthogenesis.SpectralReach.shear_unbounded
#print axioms Orthogenesis.SpectralReach.stretch_iter
#print axioms Orthogenesis.SpectralReach.herd_threshold
#print axioms Orthogenesis.SpectralReach.herd_values
#print axioms Orthogenesis.SpectralReach.fib_ratios_alternate
