-- GATE-DECLARE: sorries = none
-- GATE-REASON: ch-ocio — iteration need not settle; the displayed "ceiling" formula is Cantor's theorem; GenerativeWeave's 66 ≠ 6·11 is false.
/-
Orthogenesis/Ocio/OcioChecks.lean — Book 3, Chapter Ocio (The Law of Monsters).

  §1  "Lawful iteration must ascend to a fixed point" is not a theorem: x ↦ 2x never settles
      from 1, although it has a fixed point (0). Fixed points are guaranteed under contraction
      (Banach; see Orthogenesis/Conclusion/FixedPointConclusion.lean), not in general.
  §2  The displayed ceiling formula, |P(κ)| > κ¹, is Cantor's theorem: κ¹ = κ, and
      |P(A)| = 2^|A| > |A| for every set A, finite or infinite. It says nothing about GCH.
  §3  AMonster/GenerativeWeave.lean states `lvlHyperMahlo ≠ lvlMinMonster * 11`, i.e.
      66 ≠ 6 · 11. That is false. The file sits outside every build target, so it was never
      compiled; there, "hyper-Mahlo" is the natural number 66.
-/
import Mathlib
import Orthogenesis.Taxonomy.GSeries

namespace Orthogenesis.OcioChecks

/-! ## §1  Iteration need not settle -/

theorem doubling_never_settles (n : ℕ) :
    (fun x : ℝ => 2 * x)^[n] 1 ≠ (fun x : ℝ => 2 * x)^[n + 1] 1 := by
  rw [Orthogenesis.GSeries.iter_double, Orthogenesis.GSeries.iter_double, pow_succ]
  intro h
  linarith [pow_pos (two_pos : (0 : ℝ) < 2) n]

/-! ## §2  The "ceiling" formula is Cantor's theorem -/

theorem ceiling_formula_is_cantor (κ : Cardinal) : κ ^ (1 : Cardinal) < 2 ^ κ := by
  rw [Cardinal.power_one]; exact Cardinal.cantor κ

theorem powerset_exceeds_every_set (A : Type*) :
    Cardinal.mk A ^ (1 : Cardinal) < Cardinal.mk (Set A) := by
  rw [Cardinal.mk_set, Cardinal.power_one]; exact Cardinal.cantor _

/-! ## §3  The GenerativeWeave statement is false -/

theorem hyperMahlo_label_is_six_times_eleven : ¬ ((66 : ℕ) ≠ 6 * 11) := by decide

end Orthogenesis.OcioChecks

#print axioms Orthogenesis.OcioChecks.doubling_never_settles
#print axioms Orthogenesis.OcioChecks.ceiling_formula_is_cantor
#print axioms Orthogenesis.OcioChecks.powerset_exceeds_every_set
#print axioms Orthogenesis.OcioChecks.hyperMahlo_label_is_six_times_eleven
