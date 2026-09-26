-- GATE-DECLARE: sorries = none
-- GATE-REASON: ch16 scale — Murray's law gives similarity dimension exactly 3; shrew-to-whale span is under 8 orders; the scale table's ratios.
/-
Orthogenesis/Scale/ScaleChecks.lean — Book 3, ch16 (Scale Invariance).

  §1  Murray's law with two daughters, each scaled by 2^(−1/3), satisfies Moran's equation
      2·r^D = 1 at D = 3: the self-similar tree is exactly space-filling, not 2.97.
  §2  Shrew (2 g) to blue whale (10⁸ g) spans 10⁸/2 = 5×10⁷, between 10⁷ and 10⁸ —
      under eight orders of magnitude, not ten.
  §3  The chapter's scale table, from its own word counts: abstract 50/5000 = 1/100,
      introduction 500/5000 = 1/10, paragraph 100/5000 = 1/50 — not 10⁻⁴, 10⁻², 10¹.
-/
import Mathlib

namespace Orthogenesis.ScaleChecks

theorem murray_moran_dim_three : 2 * ((2 : ℝ) ^ (-(1 : ℝ) / 3)) ^ (3 : ℝ) = 1 := by
  rw [← Real.rpow_mul (by norm_num), show -(1 : ℝ) / 3 * 3 = -1 by norm_num, Real.rpow_neg_one]
  norm_num

theorem shrew_to_whale_span : (10 : ℝ) ^ 7 < 10 ^ 8 / 2 ∧ (10 : ℝ) ^ 8 / 2 < 10 ^ 8 := by
  constructor <;> norm_num

theorem scale_table_ratios :
    (50 : ℝ) / 5000 = 1 / 100 ∧ (500 : ℝ) / 5000 = 1 / 10 ∧ (100 : ℝ) / 5000 = 1 / 50 := by
  refine ⟨?_, ?_, ?_⟩ <;> norm_num

end Orthogenesis.ScaleChecks

#print axioms Orthogenesis.ScaleChecks.murray_moran_dim_three
#print axioms Orthogenesis.ScaleChecks.shrew_to_whale_span
#print axioms Orthogenesis.ScaleChecks.scale_table_ratios
