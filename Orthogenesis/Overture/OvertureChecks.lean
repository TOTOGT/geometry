-- GATE-DECLARE: sorries = none
-- GATE-REASON: new file 2026-09-26 for the geometry pin (Lean v4.32.0, Mathlib v4.32.0).
-- UNTESTED until the author runs `lake build` on it.
/-
# OvertureChecks.lean — Book 3, Overture (overture.html)

  The overture's memoir is the author's account and is not checked here. Two
  mathematical claims are:

  §1  "g⁶ is the Mahlo cardinal arrived at from the operator side", and "four
      operators iterated to hyper-Mahlo". Every Mahlo cardinal is (strongly)
      inaccessible by definition, and no finite cardinal is inaccessible: an
      inaccessible cardinal exceeds every natural number (Mathlib,
      `Cardinal.IsInaccessible.nat_lt`). So neither 6 nor any finite iteration
      count is Mahlo. Whether a Mahlo cardinal exists at all cannot be proved in
      ZFC (if ZFC is consistent); see ch-ocio.html and OcioChecks.lean.
-/

import Mathlib

namespace Orthogenesis.OvertureChecks

/-- No finite cardinal is inaccessible (so none is Mahlo). -/
theorem finite_not_inaccessible (n : ℕ) : ¬ Cardinal.IsInaccessible (n : Cardinal) :=
  fun h => lt_irrefl _ (h.nat_lt n)

/-- In particular g⁶ = 6 is not inaccessible (so not Mahlo). -/
theorem six_not_inaccessible : ¬ Cardinal.IsInaccessible (6 : Cardinal) := by
  simpa using finite_not_inaccessible 6

end Orthogenesis.OvertureChecks

/-! ## Axiom probe -/
#print axioms Orthogenesis.OvertureChecks.finite_not_inaccessible
#print axioms Orthogenesis.OvertureChecks.six_not_inaccessible
