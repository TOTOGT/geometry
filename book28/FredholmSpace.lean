/-
  book28/FredholmSpace.lean — Atiyah's two inequalities, and every integer is an index.
  Principia Orthogona, Book XXVIII ch 5. Pablo Nogueira Grossi, G6 LLC, 2026.

  Atiyah, K-Theory (1967), Appendix "The space of Fredholm operators", p. 154:
      dim Ker TS ≤ dim Ker T + dim Ker S,   dim Coker TS ≤ dim Coker T + dim Coker S,
  "and so TS is again a Fredholm operator". The first inequality is proved here for any
  linear maps, in the cardinal-valued `Module.rank`, so no finiteness has to be assumed
  and none is smuggled in. The shifts of ch 1 then give every integer as an index: the
  algebraic shadow of Atiyah's note that for X a point "the connected components of 𝔉
  are determined by an integer: this is in fact the index".

  WHAT IS NOT HERE: no norm, no topology on the operators, no components, no K(X).
-/
import ShiftIndex
import Mathlib.Algebra.Module.LinearMap.Index

open Module LinearMap

namespace FredholmSpace

universe u
variable {k : Type u} {M N P : Type u} [Field k] [AddCommGroup M] [AddCommGroup N]
  [AddCommGroup P] [Module k M] [Module k N] [Module k P]

/-- Atiyah p. 154: dim Ker TS ≤ dim Ker T + dim Ker S (as cardinals, no finiteness assumed). -/
theorem rank_ker_comp_le (S : M →ₗ[k] N) (T : N →ₗ[k] P) :
    Module.rank k (ker (T ∘ₗ S)) ≤ Module.rank k (ker T) + Module.rank k (ker S) := by
  let r : ker (T ∘ₗ S) →ₗ[k] ker T :=
    S.restrict (p := ker (T ∘ₗ S)) (q := ker T) (fun x hx => by simpa [mem_ker] using hx)
  let j : ker r →ₗ[k] ker S :=
    { toFun := fun x => ⟨x.1.1, by
        have := x.2; simp only [mem_ker, r, restrict_apply] at this
        simpa [mem_ker] using congrArg Subtype.val this⟩
      map_add' := fun _ _ => rfl
      map_smul' := fun _ _ => rfl }
  have hj : Function.Injective j := by
    intro a b h
    have h' : ((j a : ker S) : M) = ((j b : ker S) : M) := congrArg Subtype.val h
    exact Subtype.ext (Subtype.ext h')
  have h1 := r.rank_range_add_rank_ker
  have h2 : Module.rank k (range r) ≤ Module.rank k (ker T) := Submodule.rank_le _
  have h3 : Module.rank k (ker r) ≤ Module.rank k (ker S) := rank_le_of_injective j hj
  rw [← h1]; exact add_le_add h2 h3

variable (F : Type) [Field F]

/-- Every integer is the index of an operator on ℕ →₀ F: −k from the shift Sₖ, +k from Bₖ. -/
theorem every_integer_is_an_index (n : ℤ) : ∃ T : V F →ₗ[F] V F,
    (finrank F (ker T) : ℤ) - (finrank F (V F ⧸ range T) : ℤ) = n := by
  rcases Int.eq_nat_or_neg n with ⟨m, rfl | rfl⟩
  · exact ⟨bshift F m, bshift_index F m⟩
  · exact ⟨shift F m, shift_index F m⟩

end FredholmSpace

#print axioms FredholmSpace.rank_ker_comp_le
#print axioms FredholmSpace.every_integer_is_an_index
