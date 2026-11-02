import Mathlib

/-!
# GCM V2, Part I: what the audit of the PDF actually established, stated in Lean

STATUS: compiled by the author 2026-11-02 (Lean v4.32.0 + Mathlib): no errors; the only output was two linter
warnings about an unused fallback tactic, which was then deleted (that deletion itself not re-run).
Read each statement for what it says, not what its name promises:

* `gronwall_equality_case` checks ONLY that the comparison function e^{-ct} m0 + (K/c)(1-e^{-ct})
  solves m' = -c m + K. It is the equality case behind the ultimate bound; it is NOT the
  stochastic theorem (no Ito, no expectation, no inequality).
* `winding_depends_on_primitive` shows two primitives of the same ω-coefficient give different
  W := 2π·f(1) in the radial toy. It does NOT formalise de Rham classes.
* `nonnormal_example` checks the characteristic polynomial of A = [[-1,10],[0,-1]] is (l+1)^2 and the
  quadratic form at (1,1) is 8 > 0. It does not formalise Floquet theory or d_g^2.
-/

open Real

theorem gronwall_equality_case (c K m0 t : ℝ) (hc : c ≠ 0) :
    HasDerivAt (fun s : ℝ => Real.exp (-c * s) * m0 + K / c * (1 - Real.exp (-c * s)))
      (-c * (Real.exp (-c * t) * m0 + K / c * (1 - Real.exp (-c * t))) + K) t := by
  have h1 : HasDerivAt (fun s : ℝ => Real.exp (-c * s)) (Real.exp (-c * t) * (-c)) t := by
    have := ((hasDerivAt_id t).const_mul (-c)).exp
    simpa using this
  have h2 := (h1.mul_const m0).add ((h1.const_sub 1).const_mul (K / c))
  have hk : c * (K / c) = K := by field_simp
  refine h2.congr_deriv ?_
  linear_combination hk

theorem winding_depends_on_primitive :
    ∃ f g : ℝ → ℝ, (∀ r, deriv f r = deriv g r) ∧ 2 * Real.pi * f 1 ≠ 2 * Real.pi * g 1 := by
  refine ⟨fun r => r ^ 2, fun r => r ^ 2 - 1, fun r => by simp, ?_⟩
  intro h
  norm_num [Real.pi_ne_zero] at h

theorem nonnormal_example :
    (∀ l : ℝ, (-1 - l) * (-1 - l) - 10 * 0 = (l + 1) ^ 2) ∧
    (0 : ℝ) < (1 * ((-1) * 1 + 10 * 1) + 1 * (0 * 1 + (-1) * 1)) := by
  refine ⟨fun l => by ring, by norm_num⟩
