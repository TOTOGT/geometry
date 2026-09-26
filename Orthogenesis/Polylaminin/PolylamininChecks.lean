-- GATE-DECLARE: sorries = none
-- GATE-REASON: chΛ polylaminin — Prediction 1 depends on the chosen working concentration; Prediction 2's bound sits between T* and 1.2·T*.
/-
Orthogenesis/Polylaminin/PolylamininChecks.lean — Book 3, Chapter Λ (Protein Shape Transformations).

  §1  Prediction 1 sets the critical concentration at one third of "the maximum working
      concentration". Two protocols with different working concentrations then predict different
      thresholds for the same protein: the prediction depends on a lab's choice, not on laminin.
  §2  Prediction 2 bounds recovery by T*·log 3. Since 1 < log 3 < 1.2, the bound lies strictly
      between T* and 1.2·T*: its content is the assumed cycle length T* (26 weeks), stretched by
      less than a fifth.
-/
import Mathlib

namespace Orthogenesis.PolylamininChecks

/-! ## §1  Prediction 1 depends on the protocol -/

theorem p1_threshold_depends_on_protocol {c₁ c₂ : ℝ} (h : c₁ ≠ c₂) : c₁ / 3 ≠ c₂ / 3 := by
  intro h'; apply h; linarith

/-! ## §2  Prediction 2 restates T* -/

lemma one_lt_log_three : 1 < Real.log 3 := by
  rw [Real.lt_log_iff_exp_lt (by norm_num)]
  have := Real.exp_one_lt_d9
  norm_num at this ⊢
  linarith

lemma log_three_lt : Real.log 3 < 6 / 5 := by
  have h2 := Real.log_two_lt_d9
  have h32 : Real.log (3 / 2) ≤ 3 / 2 - 1 := Real.log_le_sub_one_of_pos (by norm_num)
  have e : Real.log 3 = Real.log 2 + Real.log (3 / 2) := by
    rw [← Real.log_mul (by norm_num) (by norm_num)]; norm_num
  norm_num at h2
  linarith

theorem p2_bound_between {T : ℝ} (hT : 0 < T) : T < T * Real.log 3 ∧ T * Real.log 3 < 6 / 5 * T := by
  constructor
  · nlinarith [one_lt_log_three]
  · nlinarith [log_three_lt]

end Orthogenesis.PolylamininChecks

#print axioms Orthogenesis.PolylamininChecks.p1_threshold_depends_on_protocol
#print axioms Orthogenesis.PolylamininChecks.one_lt_log_three
#print axioms Orthogenesis.PolylamininChecks.p2_bound_between
