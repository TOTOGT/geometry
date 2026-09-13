-- probe_book8.lean — the Orthogonal Witness scalar core (Book 8).
-- Asks the Lean KERNEL which axioms each named theorem actually depends on.
-- A theorem proved with `sorry` reports sorryAx here even though it compiled
-- without error, which is the whole point: compilation is not verification.
--
-- WHAT IS NOT NAMED HERE, on purpose:
--   · the tensor pullback (dS₄ hyperboloid → FRW line element). That is a sympy
--     result, exact and symbolic, and it is NOT in the kernel. Naming a Lean
--     declaration for it would mean writing one, and none exists.
--   · Leg 2, the epistemic claim (Tarski; Frauchiger–Renner; Local Friendliness).
--     It is a logical result, not a geometric one, and belongs in the chapter.
--   · `witness_codimension`. `5 - 4 = 1` on ℕ literals closes by `rfl` whether or
--     not anything about normal bundles holds; truncated subtraction makes
--     statements of that shape true for reasons unrelated to geometry.

import OrthogonalWitness

-- §1 · the hyperboloid constraint and proper time.
-- These two are the SAME Mathlib fact, cosh² − sinh² = 1, in two dresses: the
-- first multiplied by ℓ², the second negated. Counted separately because the
-- paper cites both names; not independent evidence.
#print axioms OrthogonalWitness.on_hyperboloid
#print axioms OrthogonalWitness.proper_time

-- §2 · the throat (no singularity).
-- `radius_has_throat` is stated for 0 ≤ ℓ and is true-but-empty at ℓ = 0, since
-- Lean's τ / 0 = 0 gives a 0 τ = 0 ≤ 0. The geometry needs 0 < ℓ.
#print axioms OrthogonalWitness.radius_has_throat
#print axioms OrthogonalWitness.throat_value
