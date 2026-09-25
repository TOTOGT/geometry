-- GATE-DECLARE: sorries = none
-- GATE-REASON: new file 2026-09-25 for the geometry pin (Lean v4.32.0, Mathlib v4.32.0).
-- UNTESTED until the author runs `lake build` on it.
/-
# PythagoreanComma.lean — Book 3, D2 · Evolutionary Epistemology and the Limits
# of Formalism (taught path 43, ch-d2-academic.html)

The chapter separates what is "created and checkable" from what is held as
[FAITH]. This file checks the one exact number it commits to.

  §1  The tetractys: 1 + 2 + 3 + 4 = 10.
  §2  The Pythagorean comma. Twelve perfect fifths exceed seven octaves by
      (3/2)¹² / 2⁷ = 3¹²/2¹⁹ = 531441/524288, as printed, and that interval is
      between 23.2 and 23.7 cents (the chapter: ≈ 23.46).

The chapter's other checkable statements concern the AXLE roadmap. One of them
disagrees with AXLE itself: the chapter says Issue 6, χ(H*(X⁶)) = 33, is
"verified computationally for n ≤ 5"; in AXLE/CatGT/G6Conjecture.lean the space
X_G6 is not yet defined (its definition is a placeholder, and the file notes
that every downstream statement is vacuous until it is), and the n ≤ 5 range is
itself stated without proof. That is a note, not a theorem here.
-/

import Mathlib

namespace Orthogenesis.PythagoreanComma

open Real

/-! ## §1 The tetractys -/

theorem tetractys : 1 + 2 + 3 + 4 = 10 := rfl

/-! ## §2 The comma -/

theorem comma_ratio : ((3 : ℚ) / 2) ^ 12 / 2 ^ 7 = 531441 / 524288 ∧
    (3 : ℚ) ^ 12 / 2 ^ 19 = 531441 / 524288 := by
  norm_num

/-- The comma in cents: 1200 · log₂(531441/524288). -/
noncomputable def commaCents : ℝ := 1200 * Real.log (531441 / 524288) / Real.log 2

theorem commaCents_bounds : 23.2 < commaCents ∧ commaCents < 23.7 := by
  have hr : (0 : ℝ) < 531441 / 524288 := by norm_num
  have hu := Real.log_le_sub_one_of_pos hr
  have hl := Real.one_sub_inv_le_log_of_pos hr
  have h2l := Real.log_two_gt_d9
  have h2u := Real.log_two_lt_d9
  have hl2 : 0 < Real.log 2 := by linarith
  unfold commaCents
  constructor
  · rw [lt_div_iff₀ hl2]
    norm_num at hl ⊢
    nlinarith
  · rw [div_lt_iff₀ hl2]
    norm_num at hu ⊢
    nlinarith

end Orthogenesis.PythagoreanComma

/-! ## Axiom probe -/
#print axioms Orthogenesis.PythagoreanComma.tetractys
#print axioms Orthogenesis.PythagoreanComma.comma_ratio
#print axioms Orthogenesis.PythagoreanComma.commaCents_bounds
