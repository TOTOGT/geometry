/-
  VolXI_K0_Floor.lean
  Principia Orthogona · Volume XI · K-Theory and Index Theory
  The floor, stated against Mathlib v4.32.0.

  STATUS, STATED FIRST AND PLAINLY.
  ---------------------------------
  NO SORRY, 2026-09-18, against the vendored Mathlib at commit 81a5d257c8
  (toolchain leanprover/lean4:v4.32.0). Zero errors, zero warnings, and the
  axiom report reads:

      'PrincipiaOrthogona.VolXI.grothendieckAddGroup_nat_equiv_int'
          depends on axioms: [propext, Classical.choice, Quot.sound]

  All three are Lean's and Mathlib's own; none is sorryAx. Every declaration in
  this file type-checks, which means §1, §2 and §3 are no longer claims about
  Mathlib's API -- they are uses of it.

  It took three rounds and both faults were names, not mathematics:
    round 1, seven errors -- `GrothendieckGroup` is `Algebra.GrothendieckGroup`
    round 2, one error    -- the to_additive name is `GrothendieckAddGroup`;
                             to_additive rewrites the token "Group" into
                             "AddGroup" in place, it does not prefix
    round 3, clean, one sorry.
  The sorry then took three further candidates, and §2 records why the first two
  failed -- the fault was `sec`, a choice function, and then the decision to
  build a map at all.

  WHAT THIS SETTLES. WP-82 recorded "Mathlib has no K-theory, so Volume XI
  cannot have a machine-checked core." The first half is true of the NAME and
  the second half does not follow. This file uses the group completion, its
  universal property, the class group, the class number and its positivity, and
  the compiler accepts all of it. Volume XI's obstacle was never a missing
  theory. It was a missing definition and a bridge lemma, and §2 names both.

  WP-82'S BAR asks for a file that elaborates clean AND reports its axioms
  without sorryAx. Both halves are now met. What is still absent upstream is the
  projective-module monoid, so §2 proves the second half of "K₀ of a field is ℤ"
  and states the first half as the thing Mathlib does not yet have. That is a
  gap in Mathlib, not a gap in this file.

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

`GrothendieckAddGroup` is the `to_additive` name of `GrothendieckGroup`.
`to_additive` rewrites the token "Group" into "AddGroup" IN PLACE; it does not
prefix the whole identifier. So the name is Grothendieck-Add-Group and not
Add-Grothendieck-Group, which is what this file assumed and what the second
compile rejected. Settled by grepping the built olean, since to_additive
generates the declaration at elaboration time and it appears nowhere in the
Mathlib source: one hit for the right spelling, zero for the wrong one. -/

/-- The cast `ℕ → ℤ`, certified as a localization map at `⊤`.

This is the whole content of "ℤ is the group completion of ℕ", and it is three
conditions, not a construction: you may add any natural number and stay
invertible, every integer is a difference of two naturals, and nothing is
collapsed by the cast. Mathlib supplies the isomorphism once those hold. -/
def natCastLocalizationMap : AddSubmonoid.LocalizationMap (⊤ : AddSubmonoid ℕ) ℤ where
  toFun n := (n : ℤ)
  map_add' a b := by push_cast; ring
  isLocalizationMap :=
    { map_addUnits := fun _ => AddGroup.isAddUnit _
      surj := fun z =>
        ⟨⟨z.toNat, ⟨(-z).toNat, AddSubmonoid.mem_top _⟩⟩, by
          show z + (((-z).toNat : ℕ) : ℤ) = ((z.toNat : ℕ) : ℤ)
          omega⟩
      exists_of_eq := fun {x y} h =>
        ⟨⟨0, AddSubmonoid.mem_top _⟩, by
          have hxy : (x : ℤ) = (y : ℤ) := h
          show (0 : ℕ) + x = 0 + y
          omega⟩ }

/-- **K₀ of a field, second half.** The Grothendieck group of `(ℕ, +)` is `ℤ`.
    This is where Volume XI's first theorem bottoms out. -/
theorem grothendieckAddGroup_nat_equiv_int :
    Nonempty (GrothendieckAddGroup ℕ ≃+ ℤ) :=
  ⟨AddLocalization.addEquivOfQuotient natCastLocalizationMap⟩

/-  HOW THIS WAS FOUND, AND WHAT THE FAILURES COST.
    -----------------------------------------------
    Three candidates. The first two are the same idea and both are wrong in the
    same way; the third abandons the idea.

    Candidates 1 and 2 built the map `GrothendieckAddGroup.lift
    (Nat.castAddMonoidHom ℤ)` and tried to prove it bijective by hand.

      Candidate 1 died on `lift_apply`, which states `lift f x` through
      `(monoidOf ⊤).sec x` -- and `sec` is a CHOICE FUNCTION. It picks a
      representative out of an equivalence class and does not reduce. Rewriting
      with it turns a goal about `mk a b` into a goal about an arbitrary
      representative and strands it there. Both branches, injectivity and
      surjectivity, died identically; the header of that attempt had predicted
      surjectivity would go through, and it did not. The lemma name that was
      also wrong (`AddLocalization.mk_eq_zero_iff`, which does not exist) was
      noise. `sec` was the fault.

      Candidate 2 routed around `sec` with `lift_mk'_spec`
      (MonoidLocalization/Maps.lean:143), which states the lift without ever
      mentioning a representative. That is the right lemma. It still carries the
      full weight of proving a hand-built map bijective.

    Candidate 3, above, builds no map. `Localization.mulEquivOfQuotient`
    (Maps.lean:615, `@[to_additive]`) already takes a localization map to an
    isomorphism, and `GrothendieckAddGroup M` is an `abbrev` for
    `AddLocalization (⊤ : AddSubmonoid M)` -- reducibly the same type. So the
    theorem was never about building anything. It was about recognising that the
    cast satisfies a definition Mathlib already knows what to do with, and all
    three obligations are arithmetic `omega` can see.

    The lesson is the one the first two candidates were too busy to notice:
    when a universal property is available, constructing the map by hand is
    work you have chosen, not work the theorem requires.

    Compiled 2026-09-18, leanprover/lean4:v4.32.0, Mathlib at 81a5d257c8.
    Axiom report: [propext, Classical.choice, Quot.sound]. `Classical.choice`
    is expected -- `addEquivOfQuotient` is noncomputable and the localization is
    a quotient -- and belongs to Mathlib's construction, not to this argument.
    The separate candidates are kept, unedited, in book6/lean/VolXI_attempt.lean
    and book6/lean/VolXI_candidate3.lean. -/

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

#print axioms grothendieckAddGroup_nat_equiv_int

end PrincipiaOrthogona.VolXI
