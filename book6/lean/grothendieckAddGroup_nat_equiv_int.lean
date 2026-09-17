/-
  grothendieckAddGroup_nat_equiv_int.lean
  Principia Orthogona · Volume XI · CANDIDATE, NOT A RESULT

  STATUS. This is an UNTESTED candidate for the one `sorry` in
  VolXI_K0_Floor.lean. It was written by an assistant that had no Lean
  toolchain to run it against, which is precisely the condition that produced
  seven name errors in the parent file on 2026-09-17. Treat every line as a
  guess until the compiler says otherwise.

  It is kept in its own file ON PURPOSE. VolXI_K0_Floor.lean currently
  elaborates clean with one declared sorry, and that state is worth more than
  an attempt at the sorry. Test here; integrate only after it passes.

      lake env lean book6/lean/grothendieckAddGroup_nat_equiv_int.lean

  WHAT IT CLAIMS. The Grothendieck group of (ℕ, +) is ℤ. That is the second
  half of "K₀ of a field is ℤ" — the half that does not need the
  projective-module monoid Mathlib lacks. See VolXI_K0_Floor.lean §2.

  THE ARGUMENT, in words, so a failure can be read against intent:
    · `lift` is the universal property: (ℕ →+ ℤ) ≃ (GrothendieckAddGroup ℕ →+ ℤ).
      Feed it `Nat.castAddMonoidHom ℤ` to get a hom out of the group completion.
    · Surjectivity: every integer is a difference of two naturals. This half
      should go through; `omega` closes the arithmetic.
    · Injectivity: ℕ is cancellative, so the inclusion is injective and nothing
      collapses. This half is the one expected to fail, most likely on the name
      `AddLocalization.mk_eq_zero_iff`, which has not been verified to exist.

  A failure here is informative and cheap. A wrong lemma name costs one grep of
  the built olean — which is how `GrothendieckAddGroup` itself was settled,
  after guessing from the naming convention had already cost two rounds.
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
  · rw [injective_iff_map_eq_zero]
    intro x hx
    induction x using AddLocalization.induction_on with
    | H p => simpa [GrothendieckAddGroup.lift_apply, AddLocalization.mk_eq_zero_iff]
               using hx
  · intro n
    obtain ⟨a, b, rfl⟩ : ∃ a b : ℕ, n = (a : ℤ) - b :=
      ⟨n.toNat, (-n).toNat, by omega⟩
    exact ⟨AddLocalization.mk a ⟨b, trivial⟩, by
      simp [GrothendieckAddGroup.lift_apply]⟩

#print axioms grothendieckAddGroup_nat_equiv_int

end PrincipiaOrthogona.VolXI
