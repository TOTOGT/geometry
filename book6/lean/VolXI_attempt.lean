/-
  VolXI_attempt.lean -- discharge the sorry in VolXI_K0_Floor.lean §2.
  Goal:  Nonempty (GrothendieckAddGroup ℕ ≃+ ℤ)

  Run:   lake env lean book6/lean/VolXI_attempt.lean

  NOT COMPILED BY ITS AUTHOR -- no lake in that environment. Names were read
  off .lake/packages/mathlib, not recalled:
    Localization.mk_eq_mk_iff                     Basic.lean:224
    Localization.r_iff_exists                     Basic.lean:191
    Localization.induction_on / induction_on₂     Basic.lean:293 / 314
    Submonoid.LocalizationMap.lift_mk'_spec       Maps.lean:143
    Algebra.GrothendieckGroup.lift (an Equiv)     GrothendieckGroup.lean:81
  If a name is wrong the fix is one `exact?`, and §3 below says where.
-/
import Mathlib

open Algebra

namespace PrincipiaOrthogona.VolXI

noncomputable abbrev F : GrothendieckAddGroup ℕ →+ ℤ :=
  GrothendieckAddGroup.lift (Nat.castAddMonoidHom ℤ)

/-! ### §1 · the computation lemma -/

-- The whole proof rests on this. `lift_mk'_spec` states
--   lift hg (mk' x y) = v  ↔  g x = g y + v
-- which avoids `sec` entirely.
theorem F_mk (a b : ℕ) :
    F (AddLocalization.mk a ⟨b, trivial⟩) = (a : ℤ) - (b : ℤ) := by
  rw [AddLocalization.mk_eq_monoidOf_mk']
  rw [(AddLocalization.addMonoidOf (⊤ : AddSubmonoid ℕ)).lift_mk'_spec]
  push_cast
  ring

/-! ### §2 · the equivalence -/

theorem grothendieckAddGroup_nat_equiv_int :
    Nonempty (GrothendieckAddGroup ℕ ≃+ ℤ) := by
  classical
  refine ⟨AddEquiv.ofBijective F ⟨?_, ?_⟩⟩
  · -- injective
    intro x y hxy
    induction x using AddLocalization.induction_on with
    | H p =>
    induction y using AddLocalization.induction_on with
    | H q =>
    obtain ⟨a, b, -⟩ := p
    obtain ⟨c, d, -⟩ := q
    rw [show (⟨b, _⟩ : (⊤ : AddSubmonoid ℕ)) = ⟨b, trivial⟩ from rfl] at hxy ⊢
    rw [show (⟨d, _⟩ : (⊤ : AddSubmonoid ℕ)) = ⟨d, trivial⟩ from rfl] at hxy ⊢
    rw [F_mk, F_mk] at hxy
    rw [AddLocalization.mk_eq_mk_iff, AddLocalization.r_iff_exists]
    exact ⟨⟨0, trivial⟩, by simpa using by omega⟩
  · -- surjective
    intro z
    refine ⟨AddLocalization.mk z.toNat ⟨(-z).toNat, trivial⟩, ?_⟩
    rw [F_mk]
    omega

end PrincipiaOrthogona.VolXI

#print axioms PrincipiaOrthogona.VolXI.grothendieckAddGroup_nat_equiv_int
