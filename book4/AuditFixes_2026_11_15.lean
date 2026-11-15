import Mathlib

/-!
# Audit fixes, 2026-11-15 (Book 4, chapters 18 and 19)

STATUS: COMPILED 2026-11-15 on the author's machine (`lake env lean`, repo pin Lean v4.32.0). Axiom report saved in
`book4/AuditFixes_2026_11_15.axioms.txt`: all five declarations depend only on propext / Classical.choice / Quot.sound
(the three Decidable-by-`decide` statements on propext and Quot.sound only), no sorryAx. The report was produced by the
author's run and pasted back; it has not been put through the repository's receipt gate.
A clean build and axiom report show that the statements below are proved, not that they express the prose claims;
see the notes on each declaration.

This file is NEW. It does not edit `Orthogenesis/Architecture/SeismicLattice.lean` or
`AcousticLattice.lean` (the ch18 footer carries a sha256 of the Seismic file; editing it would
invalidate that line and the 2026-09-14 receipt).

What each declaration establishes, and what it does not:

* `hex_no_straight_continuation`: at a vertex of the honeycomb with outgoing edge directions
  `d, d+2, d+4` (units of 60 degrees, `Fin 6`), the direction `d+3` (straight on from an arrival along
  the edge `d`) is not outgoing. This is the statement that separates the honeycomb from the square grid.
* `square_has_straight_continuation`: for the square grid (`Fin 4`, outgoing directions `d, d+1, d+2, d+3`)
  a straight continuation exists. Together with the previous one: the property is about the vertex
  direction sets, not about `d ≠ d+k` for the other edges.
* `old_form_does_not_separate`: the statement proved as `no_straight_continuation` in
  `SeismicLattice.lean` (`d ≠ d+2 ∧ d ≠ d+4` in `Fin 6`) holds in the same form for the square grid
  (`d ≠ d+1 ∧ d ≠ d+2 ∧ d ≠ d+3` in `Fin 4`), so it does not by itself express "no straight continuation".
* `norm_double_le`, `stair_delay_nondecreasing`: for point reflectors at `P + n • v` and a listener at
  the origin, the distance `‖P + n • v‖` has non-decreasing increments. The delay between successive
  echoes is `2 * (r (n+1) - r n) / c`, so this is the non-strict form of "the delay grows". The strict
  form needs the listener off the line through the reflectors (strict convexity along a non-radial
  line) and is NOT proved here. Not covered: extended tread/riser surfaces, separated source and
  listener, curved or non-uniform stairs, diffraction.
-/

namespace Orthogenesis.AuditFixes

/-- Honeycomb vertex: straight-on from an arrival along the edge `d` is not an outgoing direction. -/
theorem hex_no_straight_continuation :
    ∀ d : Fin 6, d + 3 ∉ ({d, d + 2, d + 4} : Finset (Fin 6)) := by
  decide

/-- Square-grid vertex: a straight continuation exists. -/
theorem square_has_straight_continuation :
    ∃ d : Fin 4, d + 2 ∈ ({d, d + 1, d + 2, d + 3} : Finset (Fin 4)) :=
  ⟨0, by decide⟩

/-- The form proved in `SeismicLattice.lean` holds for both vertex types, so it does not separate them. -/
theorem old_form_does_not_separate :
    (∀ d : Fin 6, d ≠ d + 2 ∧ d ≠ d + 4) ∧
    (∀ d : Fin 4, d ≠ d + 1 ∧ d ≠ d + 2 ∧ d ≠ d + 3) := by
  decide

/-- Triangle inequality in the form used for convexity of the norm along a line. -/
theorem norm_double_le {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] (x v : E) :
    2 * ‖x + v‖ ≤ ‖x‖ + ‖x + (2 : ℝ) • v‖ := by
  have h : (2 : ℝ) • (x + v) = x + (x + (2 : ℝ) • v) := by
    simp only [smul_add, two_smul]
    abel
  calc 2 * ‖x + v‖ = ‖(2 : ℝ) • (x + v)‖ := by
        rw [norm_smul, Real.norm_of_nonneg (by norm_num)]
    _ = ‖x + (x + (2 : ℝ) • v)‖ := by rw [h]
    _ ≤ ‖x‖ + ‖x + (2 : ℝ) • v‖ := norm_add_le _ _

/-- Distances from the listener (origin) to equally spaced reflectors `P + n • v` have non-decreasing
increments (non-strict). -/
theorem stair_delay_nondecreasing {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (P v : E) (n : ℕ) :
    ‖P + ((n : ℝ) + 1) • v‖ - ‖P + (n : ℝ) • v‖ ≤
      ‖P + ((n : ℝ) + 2) • v‖ - ‖P + ((n : ℝ) + 1) • v‖ := by
  have h := norm_double_le (P + (n : ℝ) • v) v
  have e1 : P + (n : ℝ) • v + v = P + ((n : ℝ) + 1) • v := by
    rw [add_smul, one_smul]
    abel
  have e2 : P + (n : ℝ) • v + (2 : ℝ) • v = P + ((n : ℝ) + 2) • v := by
    rw [add_smul]
    abel
  rw [e1, e2] at h
  linarith

end Orthogenesis.AuditFixes

#print axioms Orthogenesis.AuditFixes.hex_no_straight_continuation
#print axioms Orthogenesis.AuditFixes.square_has_straight_continuation
#print axioms Orthogenesis.AuditFixes.old_form_does_not_separate
#print axioms Orthogenesis.AuditFixes.norm_double_le
#print axioms Orthogenesis.AuditFixes.stair_delay_nondecreasing
