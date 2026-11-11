/-
  ReebUnique.lean  (2026-11-11)  --  built clean by the author under Lean v4.32.0 (geometry,
  `lake env lean catgt/lean/ReebUnique.lean`): all four theorems depend on
  [propext, Classical.choice, Quot.sound]; lint warnings only (unused fallback branches of the
  `first | ...` block in `alpha_line_deriv`).  An earlier draft had two `simp` errors in
  `dAlpha_eq`; this revision replaced that proof.  NOT yet built under the v4.14.0 pin of io.

  PURPOSE. Two uniqueness statements that were missing from the Reeb files.

  (1) `reebOrbit_unique`: every curve gamma : R -> R^3 with gamma' = reebR at every time and
      gamma 0 = (r0, th0, z0) equals `reebOrbit r0 th0 z0`.  So `reebOrbit` is THE integral
      curve through its base point, not merely one of them.  Proof is ODE-free: gamma t - t.R has
      derivative 0 everywhere, hence is constant.  (reebR is a constant field in this chart.)

  (2) `reeb_unique`: in the (r, theta, z) chart, at a point with r > 0, the only vector v with
      alphaCat p v = 1 and dAlpha p v w = 0 for all w is reebR.  Uses the explicit formula
      `dAlpha_eq`: dAlpha p u w = 2 r (w_r u_th - u_r w_th).

  CHART CAVEAT, NOT A GEOMETRIC ONE.  In polar coordinates dAlpha = -2 r dr^dtheta vanishes at
  r = 0, so (2) needs r > 0 in this chart.  In Cartesian coordinates r dr^dtheta = dx^dy and the
  form is nonvanishing at the origin; the r > 0 hypothesis is the polar Jacobian, not a
  limitation of the contact structure.  Do not cite it as one.

  NOT CLAIMED.  Completeness or smoothness of the flow beyond what ReebFlow.lean proves;
  uniqueness for a non-constant field; anything at r = 0 in the polar chart; any statement
  about Mathlib's `extDeriv` or pullback (those are ReebFlowExtDeriv.lean and a later step).
-/

import Mathlib
import CatGT_Main
import ReebFlow
import ReebBridge

/-- Any curve with velocity `reebR` everywhere and the right starting point is `reebOrbit`. -/
theorem reebOrbit_unique (γ : ℝ → ℝ × ℝ × ℝ)
    (hγ : ∀ t, HasDerivAt γ reebR t) (r₀ θ₀ z₀ : ℝ)
    (h0 : γ 0 = (r₀, θ₀, z₀)) (t : ℝ) :
    γ t = reebOrbit r₀ θ₀ z₀ t := by
  have hg : ∀ s : ℝ, HasDerivAt (fun x : ℝ => γ x - x • reebR) 0 s := by
    intro s
    have h := (hγ s).sub ((hasDerivAt_id s).smul_const reebR)
    exact h.congr_deriv (by simp)
  have key := is_const_of_deriv_eq_zero (fun s => (hg s).differentiableAt)
    (fun s => (hg s).deriv) t 0
  simp only [zero_smul, sub_zero] at key
  rw [h0] at key
  rw [reebOrbit_eq_reebFlow]
  exact eq_add_of_sub_eq key

/-- Derivative of `s ↦ alphaCat (p + s•u) w` at 0: only the r-coordinate of the base point
    moves, and alphaCat is `w_z - r² w_θ`. -/
theorem alpha_line_deriv (p u w : ℝ × ℝ × ℝ) :
    HasDerivAt (fun s : ℝ => ReebFlow.alphaCat (p + s • u) w)
      (-(2 * p.1 * u.1 * w.2.1)) 0 := by
  have hfun : (fun s : ℝ => ReebFlow.alphaCat (p + s • u) w)
      = fun s : ℝ => w.2.2 - (p.1 + s * u.1) ^ 2 * w.2.1 := by
    funext s
    simp [ReebFlow.alphaCat]
  rw [hfun]
  have hl : HasDerivAt (fun s : ℝ => p.1 + s * u.1) u.1 0 := by
    simpa using ((hasDerivAt_id (0 : ℝ)).mul_const u.1).const_add p.1
  have h2 := ((hl.pow 2).mul_const w.2.1).const_sub w.2.2
  refine h2.congr_deriv ?_
  first
    | (simp; ring)
    | simp
    | ring
    | (norm_num; ring)
    | norm_num

/-- Explicit formula for `ReebFlow.dAlpha` in the (r, theta, z) chart. -/
theorem dAlpha_eq (p u w : ℝ × ℝ × ℝ) :
    ReebFlow.dAlpha p u w = 2 * p.1 * (w.1 * u.2.1 - u.1 * w.2.1) := by
  unfold ReebFlow.dAlpha
  rw [(alpha_line_deriv p u w).deriv, (alpha_line_deriv p w u).deriv]
  ring

/-- At r > 0 (polar-chart hypothesis), `reebR` is the only vector with `alpha(v) = 1` and
    `i_v d(alpha) = 0`. -/
theorem reeb_unique (p v : ℝ × ℝ × ℝ) (hp : 0 < p.1)
    (h1 : ReebFlow.alphaCat p v = 1)
    (h2 : ∀ w, ReebFlow.dAlpha p v w = 0) : v = reebR := by
  obtain ⟨a, b, c⟩ := v
  have hA := h2 (0, 1, 0)
  have hB := h2 (1, 0, 0)
  rw [dAlpha_eq] at hA hB
  simp only at hA hB
  have ha : a = 0 := by
    have h : p.1 * a = 0 := by linarith
    rcases mul_eq_zero.mp h with h | h
    · exact absurd h hp.ne'
    · exact h
  have hb : b = 0 := by
    have h : p.1 * b = 0 := by linarith
    rcases mul_eq_zero.mp h with h | h
    · exact absurd h hp.ne'
    · exact h
  have hc : c = 1 := by
    simp only [ReebFlow.alphaCat] at h1
    rw [hb] at h1
    linarith
  rw [ha, hb, hc]
  rfl

#print axioms reebOrbit_unique
#print axioms alpha_line_deriv
#print axioms dAlpha_eq
#print axioms reeb_unique
