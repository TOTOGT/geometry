import Mathlib

/-!
# GCM V2, corrected toy model: what these three theorems say

STATUS: UNTESTED (written 2026-11-02, no local toolchain); the author compiles it.

The model is  r' = (μ/2)(r - 1/r),  θ' = ω₀,  z' = μ z - ω₀  with  α = dz - (r²-1) dθ.
Read each statement for what it says, not what its name promises:

* `toy_r2_solution` : u(t) = 1 + a·e^{μt} satisfies u' = μ(u-1). With u = r² this is the exact
  solution r²(t) = 1 + (r₀²-1)e^{μt}. It does NOT mention r, only the function u.
* `toy_z_solution`  : z(t) = ω₀/μ + (z₀-ω₀/μ)e^{μt} satisfies z' = μ z - ω₀ (needs μ ≠ 0).
* `toy_dtheta_coefficient` : the ONE polynomial identity  -2r·((μ/2)(r-1/r)) = -μ(r²-1), i.e. the
  dθ-coefficient of L_Xα equals μ times the dθ-coefficient of α. It is not the Lie derivative
  (that is checked in gcm-v2/gcm-v2-partII-verify.py, check C2, in sympy, not Lean).
-/

open Real

theorem toy_r2_solution (μ a t : ℝ) :
    HasDerivAt (fun s : ℝ => 1 + a * Real.exp (μ * s)) (μ * ((1 + a * Real.exp (μ * t)) - 1)) t := by
  have h : HasDerivAt (fun s : ℝ => 1 + a * Real.exp (μ * s)) (a * (Real.exp (μ * t) * μ)) t := by
    have := ((((hasDerivAt_id t).const_mul μ).exp).const_mul a).const_add 1
    simpa using this
  refine h.congr_deriv ?_
  ring

theorem toy_z_solution (μ ω z0 t : ℝ) (hμ : μ ≠ 0) :
    HasDerivAt (fun s : ℝ => ω / μ + (z0 - ω / μ) * Real.exp (μ * s))
      (μ * (ω / μ + (z0 - ω / μ) * Real.exp (μ * t)) - ω) t := by
  have h : HasDerivAt (fun s : ℝ => ω / μ + (z0 - ω / μ) * Real.exp (μ * s))
      ((z0 - ω / μ) * (Real.exp (μ * t) * μ)) t := by
    have := ((((hasDerivAt_id t).const_mul μ).exp).const_mul (z0 - ω / μ)).const_add (ω / μ)
    simpa using this
  have hk : μ * (ω / μ) = ω := by field_simp
  refine h.congr_deriv ?_
  first
    | linear_combination (-1 : ℝ) * hk
    | linear_combination hk

theorem toy_dtheta_coefficient (μ r : ℝ) (hr : r ≠ 0) :
    -2 * r * ((μ / 2) * (r - 1 / r)) = -μ * (r ^ 2 - 1) := by
  have hk : r * (1 / r) = 1 := by field_simp
  linear_combination μ * hk
