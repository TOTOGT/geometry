/-
  book28/InfinityMinusInfinity.lean — the index, from linear algebra to the shift.
  Principia Orthogona, Book XXVIII ch 2. Pablo Nogueira Grossi, G6 LLC, 2026.

  Zois, "18 Lectures on K-Theory" (arXiv:1008.1346), Part II, Lecture 1, opens analytic
  K-theory with the question "what is infinity minus infinity?". For a linear map
  T : V₀ → V₁ between finite-dimensional spaces, his Theorem 1 (Linear Algebra) gives

      [V₀] − [V₁] = [Ker T] − [coker T].

  In infinite dimensions the left side is ∞ − ∞ and the right side can still be a number.
  This file uses Mathlib's `LinearMap.index` (Oliver Nash, 2026), whose sign convention,
  dim ker − dim coker, is Zois' Definition 5, and proves:

  * the finite-dimensional theorem, and that every endomorphism of a finite-dimensional
    space has index 0 — the reason a square matrix can never have the shift's index;
  * that the ch 1 counts for the shifts of book28/ShiftIndex.lean *are* Mathlib's index;
  * Zois' "basic property" Ind(T₀T₁) = Ind T₀ + Ind T₁, on the shifts;
  * that Sₖ ∘ Bₖ has index 0 and is still not the identity: index 0 does not mean invertible.

  WHAT IS NOT HERE: no norm, no Hilbert space, no compact operator, no Toeplitz operator.
  Everything is on the finitely supported sequences ℕ →₀ F, as in ch 1.
-/
import ShiftIndex
import Mathlib.Algebra.Module.LinearMap.Index

open Module LinearMap

namespace InfinityMinusInfinity

section FiniteDim
variable {k M N : Type*} [Field k] [AddCommGroup M] [AddCommGroup N] [Module k M] [Module k N]

/-- Zois, Part II Lecture 1, Theorem 1 (Linear Algebra): [Ker T] − [coker T] = [V₀] − [V₁]. -/
theorem zois_theorem1 (T : M →ₗ[k] N) [FiniteDimensional k M] [FiniteDimensional k N] :
    T.index = finrank k M - finrank k N :=
  index_eq_of_finiteDimensional

/-- In finite dimensions every endomorphism has index 0: a square matrix cannot be the shift. -/
theorem endo_index_zero (T : M →ₗ[k] M) [FiniteDimensional k M] : T.index = 0 := by
  rw [index_eq_of_finiteDimensional]; simp

end FiniteDim

variable (F : Type) [Field F]

instance (k : ℕ) : FiniteDimensional F (ker (shift F k)) := by
  rw [ker_shift]; infer_instance
instance (k : ℕ) : FiniteDimensional F (V F ⧸ range (shift F k)) :=
  LinearEquiv.finiteDimensional (cokerEquiv F k).symm
instance (k : ℕ) : FiniteDimensional F (ker (bshift F k)) :=
  LinearEquiv.finiteDimensional (kerBshiftEquiv F k).symm
instance (k : ℕ) : FiniteDimensional F (V F ⧸ range (bshift F k)) := by
  rw [range_bshift]; infer_instance

/-- The ch 1 count for Sₖ is Mathlib's index. Zois' example U (e₀ ↦ e₁ ↦ e₂ …) is S₁. -/
theorem shift_index_eq (k : ℕ) : (shift F k).index = -k := shift_index F k

/-- The ch 1 count for Bₖ is Mathlib's index. -/
theorem bshift_index_eq (k : ℕ) : (bshift F k).index = k := bshift_index F k

/-- Bₖ ∘ Sₖ = id, and the indices add: k + (−k) = 0 = Ind id. -/
theorem bshift_shift_index (k : ℕ) :
    ((bshift F k).comp (shift F k)).index = (bshift F k).index + (shift F k).index := by
  rw [index_comp]

/-- The other order: Sₖ ∘ Bₖ also has index (−k) + k = 0 … -/
theorem shift_bshift_index (k : ℕ) : ((shift F k).comp (bshift F k)).index = 0 := by
  rw [index_comp, shift_index_eq, bshift_index_eq]; simp

/-- … and yet it is not the identity when k ≥ 1: it kills e₀. Index 0 is not invertibility. -/
theorem shift_bshift_ne_id (k : ℕ) (hk : 0 < k) :
    (shift F k).comp (bshift F k) ≠ LinearMap.id := by
  intro h
  have h0 := congrArg (fun g => g (Finsupp.single 0 1) 0) h
  have hb : bshift F k (Finsupp.single 0 1) = 0 := by
    ext n
    simp [bshift, Finsupp.single_apply]
    omega
  simp [hb] at h0

end InfinityMinusInfinity

#print axioms InfinityMinusInfinity.zois_theorem1
#print axioms InfinityMinusInfinity.endo_index_zero
#print axioms InfinityMinusInfinity.shift_index_eq
#print axioms InfinityMinusInfinity.bshift_index_eq
#print axioms InfinityMinusInfinity.bshift_shift_index
#print axioms InfinityMinusInfinity.shift_bshift_index
#print axioms InfinityMinusInfinity.shift_bshift_ne_id
