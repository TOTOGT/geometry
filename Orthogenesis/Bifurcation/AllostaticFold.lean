-- GATE-DECLARE: sorries = none
-- GATE-REASON: new file 2026-11-06 for the geometry pin (Lean v4.32.0, Mathlib v4.32.0).
-- UNTESTED until the author runs `lake env lean` on it. Written without a local toolchain.
/-
# AllostaticFold.lean — exact algebra behind the allostatic accumulation toy model

Model (project doc claude/MODEL-allostatic-accumulation-fold-2026-11-06.md):

    dx/dt = s − k·x + b·x²/(1 + x²)         (x = load, s = stress, k = recovery, b = feedback)

Equilibria satisfy  s = S(x) := k·x − b·x²/(1 + x²).

What is proved here (all exact, no numerics):

  §1  The factorisation  S(x) = x·(k·x² − b·x + k)/(1 + x²)   (`allo_factor`).
  §2  Irreversibility threshold: S takes a negative value at some x > 0 exactly when
      b > 2k (`allo_neg_iff`), and S ≥ 0 on x ≥ 0 when b ≤ 2k (`allo_nonneg_of_le`).
  §3  The exact case k = 1, b = 3: the zero-stress equilibria are x = 0 and the roots
      (3 ± √5)/2 of x² − 3x + 1; the larger is stable and the smaller unstable, read
      from the derivative formula `alloSp` (`high_state_stable`, `middle_state_unstable`).
  §4  `alloS_hasDerivAt`: the formula `alloSp` really is the derivative of `alloS`
      (so "stable" in §3 means f' = −S' < 0 for the model's right-hand side f = s − S).
  §5  Sign pattern of S' at 0, 1, 2 (+, −, +): S rises, falls, rises.

What this file does NOT do:
  * It does not locate the folds (x ≈ 0.17731 and 1.36416, s ≈ 0.08587 and −0.58723 for
    k = 1, b = 3); those come from a numerical root solve, and are not proved here.
  * §2 says S is negative somewhere iff b > 2k. That the minimum of S over x ≥ 0 is the
    upper fold, and that the high-load state therefore persists for every s ≥ 0, uses
    calculus (a minimum of S exists and is a fold) that is not formalised here.
  * It does not prove the rate exponent 1/2 at this model's fold; the generic saddle-node
    expansion is in BifurcationDiscriminator.lean (`sn_expand`, `sn_rate_not_linear`).
  * It does not prove hysteresis or the pulse-duration result; those are from simulation.
  * It does not say anything about real allostatic load. The positive-feedback term is
    an assumption of the toy model.
-/

import Mathlib

namespace Orthogenesis.Bifurcation

/-- Equilibrium stress for load x, general parameters: s = S(x). -/
noncomputable def alloSgen (k b x : ℝ) : ℝ := k * x - b * x ^ 2 / (1 + x ^ 2)

/-- The exact case k = 1, b = 3. -/
noncomputable def alloS (x : ℝ) : ℝ := alloSgen 1 3 x

/-- Claimed derivative of `alloS`: 1 − 6x/(1+x²)². -/
noncomputable def alloSp (x : ℝ) : ℝ := 1 - 6 * x / (1 + x ^ 2) ^ 2

-- §1 ---------------------------------------------------------------------------

theorem allo_factor (k b x : ℝ) :
    alloSgen k b x = x * (k * x ^ 2 - b * x + k) / (1 + x ^ 2) := by
  have h : (1 + x ^ 2) ≠ 0 := by positivity
  unfold alloSgen
  field_simp
  ring

-- §2 ---------------------------------------------------------------------------

/-- S is negative somewhere on x > 0 exactly when b > 2k (for k > 0). -/
theorem allo_neg_iff (k b : ℝ) (hk : 0 < k) :
    (∃ x : ℝ, 0 < x ∧ alloSgen k b x < 0) ↔ 2 * k < b := by
  constructor
  · rintro ⟨x, hx, hS⟩
    rw [allo_factor] at hS
    have hpos : 0 < 1 + x ^ 2 := by positivity
    have hnum : x * (k * x ^ 2 - b * x + k) < 0 := by
      by_contra hcon
      push Not at hcon
      have : 0 ≤ x * (k * x ^ 2 - b * x + k) / (1 + x ^ 2) := div_nonneg hcon hpos.le
      linarith
    have hq : k * x ^ 2 - b * x + k < 0 := by
      by_contra hcon
      push Not at hcon
      have : 0 ≤ x * (k * x ^ 2 - b * x + k) := mul_nonneg hx.le hcon
      linarith
    by_contra hb
    push Not at hb
    have h1 : b * x ≤ 2 * k * x := by nlinarith
    have h2 : 0 ≤ k * (x - 1) ^ 2 := mul_nonneg hk.le (sq_nonneg _)
    nlinarith
  · intro hb
    refine ⟨1, one_pos, ?_⟩
    rw [allo_factor]
    have : (1 : ℝ) * (k * 1 ^ 2 - b * 1 + k) = 2 * k - b := by ring
    rw [this]
    apply div_neg_of_neg_of_pos
    · linarith
    · norm_num

/-- If b ≤ 2k then S ≥ 0 for every x ≥ 0. -/
theorem allo_nonneg_of_le (k b : ℝ) (hk : 0 < k) (hb : b ≤ 2 * k) {x : ℝ} (hx : 0 ≤ x) :
    0 ≤ alloSgen k b x := by
  rw [allo_factor]
  apply div_nonneg
  · apply mul_nonneg hx
    have h1 : b * x ≤ 2 * k * x := by nlinarith
    have h2 : 0 ≤ k * (x - 1) ^ 2 := mul_nonneg hk.le (sq_nonneg _)
    nlinarith
  · positivity

-- §3 ---------------------------------------------------------------------------

/-- For k = 1, b = 3: zero-stress equilibria are x = 0 or a root of x² − 3x + 1. -/
theorem alloS_zero_iff (x : ℝ) : alloS x = 0 ↔ x = 0 ∨ x ^ 2 - 3 * x + 1 = 0 := by
  unfold alloS
  rw [allo_factor]
  have h : (1 + x ^ 2) ≠ 0 := by positivity
  rw [div_eq_zero_iff, mul_eq_zero]
  constructor
  · rintro ((h0 | h0) | h0)
    · exact Or.inl h0
    · right; linarith
    · exact absurd h0 h
  · rintro (h0 | h0)
    · exact Or.inl (Or.inl h0)
    · exact Or.inl (Or.inr (by linarith))

private theorem sqrt5_sq : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)

private theorem sqrt5_gt_two : 2 < Real.sqrt 5 := by
  have h5 := sqrt5_sq
  have hs : 0 ≤ Real.sqrt 5 := Real.sqrt_nonneg 5
  nlinarith

/-- (3 + √5)/2 solves x² − 3x + 1 = 0. -/
theorem quad_plus : ((3 + Real.sqrt 5) / 2) ^ 2 - 3 * ((3 + Real.sqrt 5) / 2) + 1 = 0 := by
  linear_combination (1 / 4 : ℝ) * sqrt5_sq

/-- (3 − √5)/2 solves x² − 3x + 1 = 0. -/
theorem quad_minus : ((3 - Real.sqrt 5) / 2) ^ 2 - 3 * ((3 - Real.sqrt 5) / 2) + 1 = 0 := by
  linear_combination (1 / 4 : ℝ) * sqrt5_sq

/-- The high-load zero-stress equilibrium is a zero of S with S' > 0, i.e. f' = −S' < 0
    for f = s − S: stable. -/
theorem high_state_stable :
    alloS ((3 + Real.sqrt 5) / 2) = 0 ∧ 0 < alloSp ((3 + Real.sqrt 5) / 2) := by
  set x : ℝ := (3 + Real.sqrt 5) / 2 with hxdef
  have hq : x ^ 2 - 3 * x + 1 = 0 := quad_plus
  refine ⟨(alloS_zero_iff x).2 (Or.inr hq), ?_⟩
  have hx : 5 / 2 < x := by
    have := sqrt5_gt_two
    rw [hxdef]; linarith
  have h1 : 1 + x ^ 2 = 3 * x := by linarith
  unfold alloSp
  rw [h1]
  have hxpos : 0 < x := by linarith
  have : 6 * x / (3 * x) ^ 2 < 1 := by
    rw [div_lt_one (by positivity)]
    nlinarith [mul_pos hxpos hxpos, hx]
  linarith

/-- The smaller nonzero zero-stress equilibrium has S' < 0, i.e. f' > 0: unstable. -/
theorem middle_state_unstable :
    alloS ((3 - Real.sqrt 5) / 2) = 0 ∧ alloSp ((3 - Real.sqrt 5) / 2) < 0 := by
  set x : ℝ := (3 - Real.sqrt 5) / 2 with hxdef
  have hq : x ^ 2 - 3 * x + 1 = 0 := quad_minus
  refine ⟨(alloS_zero_iff x).2 (Or.inr hq), ?_⟩
  have hx : 0 < x := by
    have h5 := sqrt5_sq
    have hs : 0 ≤ Real.sqrt 5 := Real.sqrt_nonneg 5
    have : Real.sqrt 5 < 3 := by nlinarith
    rw [hxdef]; linarith
  have hx2 : x < 2 / 3 := by
    have := sqrt5_gt_two
    rw [hxdef]; linarith
  have h1 : 1 + x ^ 2 = 3 * x := by linarith
  unfold alloSp
  rw [h1]
  have : 1 < 6 * x / (3 * x) ^ 2 := by
    rw [one_lt_div (by positivity)]
    nlinarith [mul_pos hx (sub_pos.2 hx2)]
  linarith

-- §4 ---------------------------------------------------------------------------

/-- `alloSp` is the derivative of `alloS`. -/
theorem alloS_hasDerivAt (x : ℝ) : HasDerivAt alloS (alloSp x) x := by
  have hd : (1 + x ^ 2) ≠ 0 := by positivity
  have a : HasDerivAt (fun y : ℝ => 3 * y ^ 2) (3 * (2 * x)) x := by
    simpa using (hasDerivAt_pow 2 x).const_mul 3
  have c : HasDerivAt (fun y : ℝ => 1 + y ^ 2) (2 * x) x := by
    simpa using (hasDerivAt_pow 2 x).const_add 1
  have h1 : HasDerivAt (fun y : ℝ => 3 * y ^ 2 / (1 + y ^ 2))
      ((3 * (2 * x) * (1 + x ^ 2) - 3 * x ^ 2 * (2 * x)) / (1 + x ^ 2) ^ 2) x := a.div c hd
  have h2 : HasDerivAt (fun y : ℝ => y - 3 * y ^ 2 / (1 + y ^ 2))
      (1 - (3 * (2 * x) * (1 + x ^ 2) - 3 * x ^ 2 * (2 * x)) / (1 + x ^ 2) ^ 2) x :=
    (hasDerivAt_id' x).sub h1
  have h3 : alloS = fun y : ℝ => y - 3 * y ^ 2 / (1 + y ^ 2) := by
    funext y
    simp [alloS, alloSgen]
  rw [h3]
  refine h2.congr_deriv ?_
  unfold alloSp
  field_simp
  ring

-- §5 ---------------------------------------------------------------------------

/-- Sign pattern of S': + at 0, − at 1, + at 2. -/
theorem alloSp_signs : 0 < alloSp 0 ∧ alloSp 1 < 0 ∧ 0 < alloSp 2 := by
  unfold alloSp
  refine ⟨?_, ?_, ?_⟩ <;> norm_num

end Orthogenesis.Bifurcation

#print axioms Orthogenesis.Bifurcation.allo_factor
#print axioms Orthogenesis.Bifurcation.allo_neg_iff
#print axioms Orthogenesis.Bifurcation.allo_nonneg_of_le
#print axioms Orthogenesis.Bifurcation.alloS_zero_iff
#print axioms Orthogenesis.Bifurcation.quad_plus
#print axioms Orthogenesis.Bifurcation.quad_minus
#print axioms Orthogenesis.Bifurcation.high_state_stable
#print axioms Orthogenesis.Bifurcation.middle_state_unstable
#print axioms Orthogenesis.Bifurcation.alloS_hasDerivAt
#print axioms Orthogenesis.Bifurcation.alloSp_signs
