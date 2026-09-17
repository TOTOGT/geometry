/-
  VolXI_K0_Floor.lean
  Principia Orthogona · Volume XI · K-Theory and Index Theory
  The floor, stated against Mathlib v4.32.0.

  STATUS, STATED FIRST AND PLAINLY.
  ---------------------------------
  FIRST COMPILED 2026-09-17 against the vendored Mathlib at commit 81a5d257c8
  (toolchain leanprover/lean4:v4.32.0) -- the exact commit this file was written
  against, confirmed by `git log` in .lake/packages/mathlib. It did NOT
  elaborate. Seven errors, all `unknownIdentifier`, all one cause: the API was
  read correctly and namespaced wrongly. `GrothendieckGroup` is
  `Algebra.GrothendieckGroup`. Adding `open Algebra` is the fix.

  That is the good failure mode. The file claimed Mathlib has the pieces and
  named them; the compiler agreed the pieces exist and disagreed about where.
  WP-82's "Mathlib has no K-theory" survives as a statement about naming, which
  is what §3 already said.

  ONE `sorry` REMAINS and is declared below. Until it is discharged this file
  does not clear WP-82's bar -- `#print axioms` will report `sorryAx` and that
  is the honest reading.

  The superseded status note follows, kept because it was the claim under test:
  This file had NOT been compiled. It was written against the Mathlib source
  read at commit 81a5d257c8 (toolchain leanprover/lean4:v4.32.0) on
  2026-09-17, but no Lean toolchain was reachable from the machine that wrote
  it. Until someone runs

      lake env lean book6/lean/VolXI_K0_Floor.lean

  and it elaborates, this is a draft and not evidence. WP-82's admissibility
  bar for Volume XI is "a Lean file that elaborates clean against a pinned
  Mathlib and reports its axioms." This file does not yet clear it. It exists
  so that the distance to clearing it is known rather than guessed.

  WHAT WP-82 SAID, AND WHAT IS ACTUALLY THERE.
  --------------------------------------------
  WP-82 records: "Mathlib has no K-theory, so Volume XI cannot have a
  machine-checked core." Re-measured 2026-09-17, that is true of the name and
  overstates the obstacle. Mathlib has no `KTheory/` directory and zero files
  containing `K_0`. It does have, all machine-checked already:

    * `Mathlib/GroupTheory/MonoidLocalization/GrothendieckGroup.lean`
      (Best & Dillies, 2025) -- `GrothendieckGroup M := Localization (⊤ : Submonoid M)`,
      `instCommGroup`, and `lift : (M →* G) ≃ (GrothendieckGroup M →* G)`,
      which is the universal property and is the whole content of group
      completion. This is the K₀ construction.
    * `Mathlib/RingTheory/ClassGroup.lean` -- `ClassGroup R` for a Dedekind domain.
    * `Mathlib/NumberTheory/NumberField/ClassNumber.lean` -- `classNumber`,
      `classNumber_pos`, `classNumber_ne_zero`, `classNumber_eq_one_iff`,
      with positivity proved from `Fintype.card`, so finiteness of the class
      group is established rather than assumed.

  So the missing pieces for K₀(O_K) ≅ ℤ × Cl(K) (Weibel, K-book ch. I-II) are:
  the monoid of iso classes of finitely generated projective modules under ⊕,
  and the structure theorem. A definition and a bridge lemma. Not a field.
-/

import Mathlib

namespace PrincipiaOrthogona.VolXI

open Function
open Algebra          -- GrothendieckGroup lives in the `Algebra` namespace, not at
                      -- the root. This was the whole of the 2026-09-17 error list:
                      -- seven errors, one missing `open`.

set_option autoImplicit false
-- Mathlib turns autoImplicit off for exactly the reason it bit here. With it ON,
-- an unknown identifier becomes a silently bound implicit variable, so
-- `GrothendieckGroup M` reported "Function expected at GrothendieckGroup / but
-- this term has type ?m.1" instead of "unknown identifier". The diagnosis was
-- buried one layer down. Off, the first error names the real fault.

/-! ### §1 · Instrument check

If these three do not elaborate, the rest of the file is not worth reading,
because it means the API was misread. Each is a restatement of something
Mathlib already proves, and each should close by `inferInstance` or `exact?`. -/

/-- The Grothendieck group of a commutative monoid is a commutative group.
    Mathlib: `GrothendieckGroup.instCommGroup`. -/
example (M : Type*) [CommMonoid M] : CommGroup (GrothendieckGroup M) := inferInstance

/-- The universal property, as an equivalence of hom-sets.
    Mathlib: `GrothendieckGroup.lift`. -/
noncomputable example (M G : Type*) [CommMonoid M] [CommGroup G] :
    (M →* G) ≃ (GrothendieckGroup M →* G) :=
  GrothendieckGroup.lift

/-- For a cancellative monoid the inclusion is injective.
    Mathlib: `GrothendieckGroup.of_injective`. -/
example (M : Type*) [CommMonoid M] [IsCancelMul M] :
    Injective (GrothendieckGroup.of (M := M)) :=
  GrothendieckGroup.of_injective

/-! ### §2 · K₀ of a field, which is the first theorem Volume XI owes

Over a field every finitely generated module is free, and two are isomorphic
iff their ranks agree. So the monoid of iso classes under ⊕ is `(ℕ, +)`, and
K₀ of a field is the group completion of `(ℕ, +)`, which is `ℤ`.

The statement below is the second half only -- the group completion of the
naturals -- because the first half needs the projective-module monoid, which
is exactly what Mathlib does not yet have. Stating this separately is the
point: it isolates what is missing.

`AddGrothendieckGroup` is the `to_additive` name of `GrothendieckGroup`. -/

/-- **K₀ of a field, second half.** The Grothendieck group of `(ℕ, +)` is `ℤ`.
    This is where Volume XI's first theorem bottoms out. -/
theorem addGrothendieckGroup_nat_equiv_int :
    Nonempty (AddGrothendieckGroup ℕ ≃+ ℤ) := by
  sorry
  -- HONEST SORRY. The intended proof: `ℤ` is a commutative group, `Nat.cast`
  -- is an `AddMonoidHom ℕ →+ ℤ`, so `AddGrothendieckGroup.lift` supplies a
  -- hom `AddGrothendieckGroup ℕ →+ ℤ`. Injectivity comes from `ℕ` being
  -- cancellative; surjectivity from every integer being a difference of
  -- naturals. Each step is available; assembling them was not attempted here
  -- because the file could not be compiled to check the assembly.

/-! ### §3 · The arithmetic side, which Mathlib already holds -/

/-- The class number of a number field is positive.
    Mathlib: `NumberField.classNumber_pos`. -/
example (K : Type*) [Field K] [NumberField K] : 0 < NumberField.classNumber K :=
  NumberField.classNumber_pos K

/-- Class number one is exactly principality of the ring of integers.
    Mathlib: `NumberField.classNumber_eq_one_iff`. -/
example (K : Type*) [Field K] [NumberField K] :
    NumberField.classNumber K = 1 ↔ IsPrincipalIdealRing (NumberField.RingOfIntegers K) :=
  NumberField.classNumber_eq_one_iff

/-! ### §4 · The bridge Volume XI actually needs

This is the statement, with no attempt at a proof. It is recorded as a target
so the volume's obligation is written down rather than described.

For `R` a Dedekind domain, K₀(R) ≅ ℤ × Pic(R); for `R = 𝓞 K` the ring of
integers of a number field, Pic(𝓞 K) = ClassGroup (𝓞 K).

To state it at all, `K₀` must first be defined, which requires the monoid

    P(R) := (iso classes of f.g. projective R-modules, ⊕, 0)

and that monoid does not exist in Mathlib. Constructing it is the real work of
Volume XI, and it is a quotient-type construction with the usual universe and
decidability friction, not a deep theorem. -/

/-- **The target.** Not stated in Lean because `K₀` is undefined. Recorded in
prose so that the obligation is explicit:

    `K₀ (𝓞 K) ≃+ ℤ × Additive (ClassGroup (𝓞 K))`

Everything on the right-hand side exists and is machine-checked today.
Everything on the left-hand side has to be built. -/
def volXI_obligation : String :=
  "K₀(𝓞 K) ≃+ ℤ × Additive (ClassGroup (𝓞 K)) -- RHS exists in Mathlib; LHS does not"

/-! ### §5 · What this file establishes if it elaborates

1. The Grothendieck group construction and its universal property are present
   and usable. WP-82's "no K-theory" is a statement about naming.
2. The class group, class number, finiteness, and the principality criterion
   are present and usable.
3. Exactly two things are missing: the projective-module monoid P(R), and the
   structure theorem. Both are named above.

And if it does not elaborate, it establishes that the API was misread, which
is also worth knowing and is why the file says so at the top. -/

#print axioms addGrothendieckGroup_nat_equiv_int

end PrincipiaOrthogona.VolXI
