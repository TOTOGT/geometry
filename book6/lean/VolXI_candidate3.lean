/-
  VolXI_candidate3.lean -- discharge the sorry in VolXI_K0_Floor.lean §2.
  Goal:  Nonempty (GrothendieckAddGroup ℕ ≃+ ℤ)

  Run:   lake env lean book6/lean/VolXI_candidate3.lean

  WHY A THIRD CANDIDATE.  Candidates 1 and 2 both tried to prove the map
  `GrothendieckAddGroup.lift (Nat.castAddMonoidHom ℤ)` bijective.  Candidate 1
  died on `sec`, a choice function that does not reduce.  Candidate 2 routes
  around `sec` via `lift_mk'_spec`, which is the right lemma, but it still
  carries the burden of proving bijectivity by hand.

  This candidate does not build a map at all.  Mathlib already proves

      Localization.mulEquivOfQuotient (f : S.LocalizationMap N) : Localization S ≃* N
        -- Maps.lean:615, @[to_additive] ⇒ AddLocalization.addEquivOfQuotient

  and `GrothendieckAddGroup M` is by definition `AddLocalization (⊤ : AddSubmonoid M)`
  (GrothendieckGroup.lean:33, an `abbrev`, hence reducible).  So the entire task
  is to certify that `ℕ → ℤ` IS a localization map at ⊤ -- three obligations,
  each of which `omega` can see:

    map_addUnits  every integer is an additive unit          (AddGroup.isAddUnit)
    surj          every z : ℤ is a - b with a b : ℕ          (omega, via Int.toNat)
    exists_of_eq  Nat.cast : ℕ → ℤ is injective              (omega)

  Names read off .lake/packages/mathlib, not recalled:
    AddSubmonoid.LocalizationMap  (extends M →ₙ+ N)     Basic.lean:94, 121
    AddSubmonoid.IsLocalizationMap fields               Basic.lean:87-90
    AddLocalization.addEquivOfQuotient                  Maps.lean:615 (to_additive)
    AddGroup.isAddUnit                                  Units/Defs.lean:628
  The additive names were confirmed present in the built oleans, not guessed.

  NOT COMPILED BY ITS AUTHOR -- no lake in that environment.
-/
import Mathlib

open Algebra

namespace PrincipiaOrthogona.VolXI

/-! ### §1 · ℤ is the localization of ℕ at its top submonoid -/

/-- The cast `ℕ → ℤ`, certified as a localization map at `⊤`.  This is the whole
content of "ℤ is the Grothendieck group of ℕ": you may add any natural number,
subtraction is the inverse of that, and nothing is collapsed on the way. -/
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

/-! ### §2 · the equivalence -/

theorem grothendieckAddGroup_nat_equiv_int :
    Nonempty (GrothendieckAddGroup ℕ ≃+ ℤ) :=
  ⟨AddLocalization.addEquivOfQuotient natCastLocalizationMap⟩

/-! ### §3 · what the proof depends on

If the axiom report below names anything beyond `propext`, `Classical.choice`
and `Quot.sound`, the proof is not the one claimed.  `Classical.choice` IS
expected here: `addEquivOfQuotient` is noncomputable, and the localization is a
quotient.  That is a property of Mathlib's construction, not of this argument. -/

#print axioms grothendieckAddGroup_nat_equiv_int

/-! ### §4 · if something breaks

  (a) `natCastLocalizationMap` fails to elaborate as a structure instance:
      the parent is `M →ₙ+ N` (an AddHom, no zero).  If the field is named
      something other than `map_add'`, `#check @AddSubmonoid.LocalizationMap.mk`
      prints the signature.

  (b) `show ... ; omega` fails in `surj`: the coercion from `(⊤ : AddSubmonoid ℕ)`
      may not reduce as written.  Replace the `show` with `simp only
      [AddSubmonoid.coe_mk]` and rerun; if the goal still has a cast omega
      cannot see, `push_cast` before it.

  (c) `AddLocalization.addEquivOfQuotient` is not the additive name: run
      `open AddLocalization in #check @addEquivOfQuotient`.  The olean for
      Maps.lean carries 8 occurrences of that string, so it exists; the only
      question would be its namespace.

  (d) The `Nonempty` unifies but the abbrev does not: `GrothendieckAddGroup ℕ`
      is `AddLocalization (⊤ : AddSubmonoid ℕ)` by `abbrev`, so this is
      reducible-defeq.  `show Nonempty (AddLocalization (⊤ : AddSubmonoid ℕ) ≃+ ℤ)`
      forces it. -/

end PrincipiaOrthogona.VolXI
