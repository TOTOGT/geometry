-- GATE-DECLARE: sorries = none
-- GATE-REASON: new file 2026-09-25 for the geometry pin (Lean v4.32.0, Mathlib v4.32.0).
-- UNTESTED until the author runs `lake build` on it.
/-
# AxiomaticTurn.lean — Book 3, Chapter 8 · The Axiomatic Turn (taught path 34,
# ch8-axiomatic.html; the same page serves the Cajueiro edition)

§8.5 quotes a Lean theorem `dm3_universality` from `AXLE/Lexicon/dm3_operators.lean`:
from a well-founded order it concludes that the dynamics has a fixed point, by
`WellFounded.has_min`. As of 2026-09-25 that file and that theorem exist in
neither TOTOGT/AXLE nor TOTOGT/geometry, and the statement is false:

  §1  (ℕ, <) is well-founded, and x ↦ x + 1 has no fixed point. Well-foundedness
      gives MINIMAL ELEMENTS of nonempty sets (`has_min`), not fixed points of maps.
  §2  What is true, with the missing hypothesis supplied:
      – a map on ℕ that never increases (f x ≤ x) has a fixed point, reached by
        iterating — well-foundedness stops the descent;
      – a monotone map on a complete lattice has a least fixed point
        (Knaster–Tarski).
      The Collatz map fails the first hypothesis at once (3 ↦ 10), which is why
      no such one-line argument reaches Collatz.

Not formalised: Gödel's theorems (not in Mathlib), the "Gödel–dm³ Compatibility
Theorem" (for any effectively generated chain S → S′ → S″ …, the union is again
a consistent recursively enumerable theory and is itself incomplete, so "the
chain captures all of mathematics" does not hold), and the historical claims.
-/

import Mathlib

namespace Orthogenesis.AxiomaticTurn

/-! ## §1 Well-foundedness does not give fixed points -/

theorem wf_without_fixed_point :
    WellFounded ((· < ·) : ℕ → ℕ → Prop) ∧ ¬ ∃ x : ℕ, x + 1 = x :=
  ⟨wellFounded_lt, fun ⟨x, hx⟩ => by omega⟩

/-! ## §2 What is true -/

/-- A map on ℕ that never increases has a fixed point. -/
theorem nonincreasing_has_fixed_point (f : ℕ → ℕ) (hf : ∀ x, f x ≤ x) (x : ℕ) :
    ∃ y, f y = y := by
  induction x using Nat.strong_induction_on with
  | _ x ih =>
    by_cases h : f x = x
    · exact ⟨x, h⟩
    · exact ih (f x) (lt_of_le_of_ne (hf x) h)

/-- Knaster–Tarski: a monotone map on a complete lattice fixes its least fixed point. -/
theorem knaster_tarski {α : Type*} [CompleteLattice α] (f : α →o α) :
    f (OrderHom.lfp f) = OrderHom.lfp f :=
  OrderHom.map_lfp f

/-- The Collatz map. -/
def collatz (n : ℕ) : ℕ := if n % 2 = 0 then n / 2 else 3 * n + 1

/-- It increases at 3, so the non-increasing argument does not apply. -/
theorem collatz_increases : collatz 3 = 10 ∧ 3 < collatz 3 := by
  decide

end Orthogenesis.AxiomaticTurn

/-! ## Axiom probe -/
#print axioms Orthogenesis.AxiomaticTurn.wf_without_fixed_point
#print axioms Orthogenesis.AxiomaticTurn.nonincreasing_has_fixed_point
#print axioms Orthogenesis.AxiomaticTurn.knaster_tarski
#print axioms Orthogenesis.AxiomaticTurn.collatz_increases
