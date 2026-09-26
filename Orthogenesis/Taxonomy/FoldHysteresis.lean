-- GATE-DECLARE: sorries = none
-- GATE-REASON: fold and hysteresis of the cusp slice W = q⁴/4 − 3q²/2 + a·q; branch lifetimes, jump landing, bistable window, all proved.
/-
Orthogenesis/Taxonomy/FoldHysteresis.lean — the phase transition and its irreversible residue.

The family W_a(q) = q⁴/4 − 3q²/2 + a·q (Thom's cusp at b = −3). Equilibria: W′ = q³ − 3q + a = 0.
The curve q³ − 3q is PrincipiaVol1's V(q), read as the equilibrium curve rather than the potential:
its facts V′(1) = 0, V″(1) = 6, V(1) = −2 are exactly the fold conditions W″ = 0, W‴ ≠ 0, W′ = 0
at (q, a) = (1, 2).

Proved:
  §1  W′, W″, W‴ are the actual derivatives (HasDerivAt), not free definitions.
  §2  Folds at (1, 2) and (−1, −2): W′ = W″ = 0, W‴ ≠ 0.
  §3  The jump: at a = 2 the equilibria are exactly q = 1 (the fold) and q = −2, and q = −2 is stable.
  §4  Branch lifetimes: a stable equilibrium with q > 1 exists iff a < 2; one with q < −1 exists iff a > −2.
  §5  Past the fold nothing is left nearby: for a > 2 there is no equilibrium with q ≥ −2;
      for a < −2 none with q ≤ 2.
  §6  The residue: for −2 < a < 2 both stable equilibria coexist (bistable window).

Reading §4–§6 as history dependence ("the system stays on its branch until that branch ends") is the
quasi-static assumption. The gradient flow itself is not formalised here. Nothing in this file
fixes 33, 64 or any other count; the counts in the g-series are teaching indices.
-/
import Mathlib

namespace Orthogenesis.FoldHysteresis

noncomputable def W (a q : ℝ) : ℝ := q ^ 4 / 4 - 3 * q ^ 2 / 2 + a * q
def dW (a q : ℝ) : ℝ := q ^ 3 - 3 * q + a
def d2W (q : ℝ) : ℝ := 3 * q ^ 2 - 3
def d3W (q : ℝ) : ℝ := 6 * q

/-! ## §1  The derivatives are real -/

theorem hasDerivAt_W (a q : ℝ) : HasDerivAt (W a) (dW a q) q := by
  have h := (((hasDerivAt_pow 4 q).div_const 4).sub
    (((hasDerivAt_pow 2 q).const_mul 3).div_const 2)).add ((hasDerivAt_id' q).const_mul a)
  refine h.congr_deriv ?_
  unfold dW
  norm_num <;> ring

theorem hasDerivAt_dW (a q : ℝ) : HasDerivAt (dW a) (d2W q) q := by
  have h := ((hasDerivAt_pow 3 q).sub ((hasDerivAt_id' q).const_mul 3)).add_const a
  refine h.congr_deriv ?_
  unfold d2W
  norm_num <;> ring

theorem hasDerivAt_d2W (q : ℝ) : HasDerivAt d2W (d3W q) q := by
  have h := ((hasDerivAt_pow 2 q).const_mul 3).sub_const 3
  refine h.congr_deriv ?_
  unfold d3W
  norm_num <;> ring

/-! ## §2  The two folds -/

theorem fold_right : dW 2 1 = 0 ∧ d2W 1 = 0 ∧ d3W 1 ≠ 0 := by
  unfold dW d2W d3W; norm_num

theorem fold_left : dW (-2) (-1) = 0 ∧ d2W (-1) = 0 ∧ d3W (-1) ≠ 0 := by
  unfold dW d2W d3W; norm_num

/-! ## §3  The jump at a = 2 -/

theorem equilibria_at_fold (q : ℝ) : dW 2 q = 0 ↔ q = 1 ∨ q = -2 := by
  unfold dW
  constructor
  · intro h
    have hf : (q - 1) ^ 2 * (q + 2) = 0 := by linear_combination h
    rcases mul_eq_zero.mp hf with h1 | h2
    · left; linarith [pow_eq_zero_iff (two_ne_zero) |>.mp h1]
    · right; linarith
  · rintro (rfl | rfl) <;> norm_num

theorem landing_stable : 0 < d2W (-2) := by unfold d2W; norm_num

/-! ## §4  Branch lifetimes -/

theorem right_stable {q : ℝ} (hq : 1 < q) : 0 < d2W q := by unfold d2W; nlinarith

theorem left_stable {q : ℝ} (hq : q < -1) : 0 < d2W q := by unfold d2W; nlinarith

theorem right_branch_iff (a : ℝ) : (∃ q, 1 < q ∧ dW a q = 0) ↔ a < 2 := by
  constructor
  · rintro ⟨q, hq, h⟩
    unfold dW at h
    nlinarith [mul_pos (pow_pos (sub_pos.mpr hq) 2) (by linarith : (0 : ℝ) < q + 2)]
  · intro ha
    have hA : 0 ≤ |a| := abs_nonneg a
    have hB : -a ≤ |a| := neg_le_abs a
    have hM1 : (1 : ℝ) ≤ 2 + |a| := by linarith
    have hcont : ContinuousOn (fun q : ℝ => q ^ 3 - 3 * q + a) (Set.Icc 1 (2 + |a|)) :=
      (by fun_prop : Continuous fun q : ℝ => q ^ 3 - 3 * q + a).continuousOn
    have h0 : (0 : ℝ) ∈ Set.Icc ((fun q : ℝ => q ^ 3 - 3 * q + a) 1)
        ((fun q : ℝ => q ^ 3 - 3 * q + a) (2 + |a|)) := by
      constructor
      · show (1 : ℝ) ^ 3 - 3 * 1 + a ≤ 0
        norm_num
        linarith
      · show (0 : ℝ) ≤ (2 + |a|) ^ 3 - 3 * (2 + |a|) + a
        have hP : (0 : ℝ) ≤ (2 + |a|) * ((2 + |a|) ^ 2 - 4) :=
          mul_nonneg (by linarith) (by nlinarith [sq_nonneg |a|])
        nlinarith [hP]
    obtain ⟨q, hq, hq0⟩ := intermediate_value_Icc hM1 hcont h0
    refine ⟨q, ?_, hq0⟩
    rcases eq_or_lt_of_le hq.1 with h | h
    · subst h
      have h1 : (1 : ℝ) ^ 3 - 3 * 1 + a = 0 := hq0
      norm_num at h1
      linarith
    · exact h

lemma dW_neg (a q : ℝ) : dW a (-q) = -dW (-a) q := by unfold dW; ring

theorem left_branch_iff (a : ℝ) : (∃ q, q < -1 ∧ dW a q = 0) ↔ -2 < a := by
  constructor
  · rintro ⟨q, hq, h⟩
    have h' : dW (-a) (-q) = 0 := by
      have := dW_neg a (-q)
      rw [neg_neg] at this
      rw [this] at h
      exact neg_eq_zero.mp h
    have := (right_branch_iff (-a)).mp ⟨-q, by linarith, h'⟩
    linarith
  · intro ha
    obtain ⟨p, hp, h⟩ := (right_branch_iff (-a)).mpr (by linarith)
    refine ⟨-p, by linarith, ?_⟩
    rw [dW_neg, h, neg_zero]

/-! ## §5  Past the fold -/

theorem nothing_near_past_right_fold {a : ℝ} (ha : 2 < a) (q : ℝ) (hq : -2 ≤ q) :
    dW a q ≠ 0 := by
  unfold dW
  intro h
  nlinarith [mul_nonneg (sq_nonneg (q - 1)) (by linarith : (0 : ℝ) ≤ q + 2)]

theorem nothing_near_past_left_fold {a : ℝ} (ha : a < -2) (q : ℝ) (hq : q ≤ 2) :
    dW a q ≠ 0 := by
  unfold dW
  intro h
  nlinarith [mul_nonneg (sq_nonneg (q + 1)) (by linarith : (0 : ℝ) ≤ 2 - q)]

/-! ## §6  The residue: bistable window -/

theorem bistable {a : ℝ} (h1 : -2 < a) (h2 : a < 2) :
    ∃ q₁ q₂, q₁ < -1 ∧ 1 < q₂ ∧ dW a q₁ = 0 ∧ dW a q₂ = 0 ∧ 0 < d2W q₁ ∧ 0 < d2W q₂ := by
  obtain ⟨q₁, hq₁, e₁⟩ := (left_branch_iff a).mpr h1
  obtain ⟨q₂, hq₂, e₂⟩ := (right_branch_iff a).mpr h2
  exact ⟨q₁, q₂, hq₁, hq₂, e₁, e₂, left_stable hq₁, right_stable hq₂⟩

end Orthogenesis.FoldHysteresis

#print axioms Orthogenesis.FoldHysteresis.hasDerivAt_W
#print axioms Orthogenesis.FoldHysteresis.fold_right
#print axioms Orthogenesis.FoldHysteresis.equilibria_at_fold
#print axioms Orthogenesis.FoldHysteresis.right_branch_iff
#print axioms Orthogenesis.FoldHysteresis.left_branch_iff
#print axioms Orthogenesis.FoldHysteresis.nothing_near_past_right_fold
#print axioms Orthogenesis.FoldHysteresis.bistable
