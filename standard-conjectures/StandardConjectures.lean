import Mathlib

/-!
# Linear-algebra core of Milne, "Grothendieck's standard conjecture of Lefschetz
type over finite fields" (arXiv:2011.06563), §6 and §4.

This file does NOT prove any standard conjecture. It proves three
purely algebraic steps used in those arguments, with no `sorry`:

* `finrank_eq_of_perfect_pairing`   : a nondegenerate pairing forces equal dimension
                                      (Prop. 6.1: D(X) gives dim AH^i = dim AH^(d-i)).
* `injective_is_surjective_of_pairing` : with L injective, equal dimension makes L bijective
                                      (Prop. 6.1: D(X) => A(X,L)).
* `left_inverse_of_nilpotent_defect`  : if beta∘alpha = 1 + n with n nilpotent, then
                                      alpha has a left inverse (Prop. 6.6).

Everything geometric (Weil cohomology, algebraic cycles, motives) is NOT
formalised here; Mathlib does not yet contain it.
-/

open Module

section Pairing

variable {K V W : Type*} [Field K] [AddCommGroup V] [Module K V]
  [AddCommGroup W] [Module K W] [FiniteDimensional K V] [FiniteDimensional K W]

theorem finrank_le_of_separatingLeft (B : V →ₗ[K] W →ₗ[K] K)
    (hB : ∀ x, (∀ y, B x y = 0) → x = 0) : finrank K V ≤ finrank K W := by
  have hinj : Function.Injective B := by
    rw [← LinearMap.ker_eq_bot, LinearMap.ker_eq_bot']
    intro x hx
    exact hB x (fun y => by simpa using LinearMap.congr_fun hx y)
  calc finrank K V ≤ finrank K (W →ₗ[K] K) := LinearMap.finrank_le_finrank_of_injective hinj
    _ = finrank K W := by
      have := Subspace.dual_finrank_eq (K := K) (V := W)
      simpa [Module.Dual] using this

/-- A nondegenerate pairing `V × W → K` of finite-dimensional spaces gives equal dimension. -/
theorem finrank_eq_of_perfect_pairing (B : V →ₗ[K] W →ₗ[K] K)
    (hL : ∀ x, (∀ y, B x y = 0) → x = 0) (hR : ∀ y, (∀ x, B x y = 0) → y = 0) :
    finrank K V = finrank K W :=
  le_antisymm (finrank_le_of_separatingLeft B hL)
    (finrank_le_of_separatingLeft B.flip (fun y hy => hR y (fun x => by simpa using hy x)))

/-- Prop. 6.1 core: injective `L` between spaces in perfect pairing is surjective. -/
theorem injective_is_surjective_of_pairing (B : V →ₗ[K] W →ₗ[K] K)
    (hL : ∀ x, (∀ y, B x y = 0) → x = 0) (hR : ∀ y, (∀ x, B x y = 0) → y = 0)
    (L : V →ₗ[K] W) (hinj : Function.Injective L) : Function.Surjective L :=
  (LinearMap.injective_iff_surjective_of_finrank_eq_finrank
    (finrank_eq_of_perfect_pairing B hL hR)).1 hinj

end Pairing

/-- Prop. 6.6 core: `β α = 1 + n` with `n` nilpotent gives `α` a left inverse. -/
theorem left_inverse_of_nilpotent_defect {R : Type*} [Ring R] (α β n : R)
    (h : β * α = 1 + n) (hn : IsNilpotent n) : ∃ γ : R, γ * α = 1 := by
  obtain ⟨u, hu⟩ : IsUnit (1 + n) := hn.isUnit_one_add
  refine ⟨↑u⁻¹ * β, ?_⟩
  rw [mul_assoc, h, ← hu]
  exact u.inv_mul
