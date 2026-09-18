/-
  grothendieckAddGroup_nat_equiv_int.lean
  Principia Orthogona · Volume XI · CANDIDATE 2, STILL UNTESTED

  CANDIDATE 1 FAILED, 2026-09-17, and the failure was more useful than the
  lemma name it was blamed on. Three errors:

    · `AddLocalization.mk_eq_zero_iff` does not exist   (predicted)
    · injectivity stuck with `hx` reduced to a statement about
        ((AddLocalization.addMonoidOf ⊤).sec (mk p.1 p.2)).1 - ...
    · surjectivity stuck the SAME way                   (NOT predicted --
      candidate 1's header said this half should go through)

  THE DIAGNOSIS. `lift_apply` expresses `lift f x` through `sec`, which is a
  CHOICE FUNCTION. It picks a numerator/denominator pair out of an equivalence
  class and nothing about it reduces. Rewriting with `lift_apply` therefore
  turns a goal about `mk a b` into a goal about an arbitrary representative and
  strands it there. That is why `Classical.choice` appeared in candidate 1's
  axiom list. The wrong lemma name was noise; `sec` was the fault.

  WHAT MATHLIB SAYS TO DO INSTEAD, in its own docstring at
  MonoidLocalization/Basic.lean:54 -- "To reason about the localization as a
  quotient type, use `mk_eq_monoidOf_mk'` and associated ... hence gives you
  access to the results in the rest of the file."

  So: rewrite `mk` into `mk'` FIRST, then use `lift_mk'`, which computes.
  Verified to exist on disk:
    Localization.mk_eq_monoidOf_mk'_apply  (Basic.lean:731)
    Submonoid.LocalizationMap.lift_mk'     (Maps.lean:103)
    Localization.mk_eq_mk_iff              (Basic.lean:224)
    Localization.r_iff_exists              (Basic.lean:191)
  Their additive twins are to_additive-generated; the names below assume the
  usual AddLocalization / AddSubmonoid prefixes and ARE NOT VERIFIED.

  WHERE THIS ONE WILL PROBABLY DIE. The additive names, and whether
  `lift_mk'`'s right-hand side simplifies. If it dies on a name, grep the
  olean rather than guessing -- that is what settled GrothendieckAddGroup.

  A THIRD ROUTE, if this fails and is not worth another round: skip `lift`
  entirely. Define the map by `AddLocalization.liftOn` as (a, b) ↦ a - b,
  prove it respects `r` via `r_iff_exists`, give the inverse explicitly as
  n ↦ mk n.toNat (-n).toNat, and assemble with `AddEquiv.mk'`. Longer, but it
  never touches `sec`.

      lake env lean book6/lean/grothendieckAddGroup_nat_equiv_int.lean

  VolXI_K0_Floor.lean still elaborates clean with its one declared sorry. That
  state is not touched by anything in this file.
-/

import Mathlib

namespace PrincipiaOrthogona.VolXI

open Function
open Algebra

set_option autoImplicit false

theorem grothendieckAddGroup_nat_equiv_int :
    Nonempty (GrothendieckAddGroup ℕ ≃+ ℤ) := by
  refine ⟨AddEquiv.ofBijective
    (GrothendieckAddGroup.lift (Nat.castAddMonoidHom ℤ)) ⟨?_, ?_⟩⟩
  · -- injective: ℕ is cancellative, so nothing collapses.
    rw [injective_iff_map_eq_zero]
    intro x hx
    induction x using AddLocalization.induction_on with
    | H p =>
      rw [AddLocalization.mk_eq_addMonoidOf_mk'_apply] at hx ⊢
      rw [AddSubmonoid.LocalizationMap.lift_mk'] at hx
      simp only [Nat.castAddMonoidHom_apply] at hx
      -- hx : (p.1 : ℤ) - (p.2 : ℤ) = 0, so p.1 = p.2 in ℕ
      rw [← AddLocalization.mk_eq_addMonoidOf_mk'_apply,
          AddLocalization.mk_eq_mk_iff, AddLocalization.r_iff_exists]
      exact ⟨0, by omega⟩
  · -- surjective: every integer is a difference of two naturals.
    intro n
    obtain ⟨a, b, rfl⟩ : ∃ a b : ℕ, n = (a : ℤ) - b :=
      ⟨n.toNat, (-n).toNat, by omega⟩
    refine ⟨AddLocalization.mk a ⟨b, trivial⟩, ?_⟩
    rw [AddLocalization.mk_eq_addMonoidOf_mk'_apply,
        AddSubmonoid.LocalizationMap.lift_mk']
    simp

#print axioms grothendieckAddGroup_nat_equiv_int

end PrincipiaOrthogona.VolXI
