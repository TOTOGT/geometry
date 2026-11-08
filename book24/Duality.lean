import Mathlib

/-
Book XXIV, chapter 10: duality, bilinear forms, tensor products. Lean core.

STATUS: NOT COMPILED. Written 2026-11-08 without a Lean toolchain. Lemma names were read from the pinned Mathlib
(Mathlib/LinearAlgebra/Dual/{Basis,Lemmas,Defs}.lean, Mathlib/LinearAlgebra/Matrix/Kronecker.lean); signatures were not
type-checked. Run, from the repo root:
    lake env lean book24/Duality.lean > book24/duality.axioms.txt 2>&1
and report the output; errors are fixed against what the compiler says, not guessed.

The statements follow Lax, Linear Algebra and Its Applications (2nd ed.), Chapter 2 (scan page = printed + 17):
  dual_basis_apply          p.15 (Exercise 6(c))   the dual basis: l_i(e_j) = delta_ij        Mathlib: Basis.toDual_apply
  annihilator_dim           p.15-16 Theorem 4      dim Y + dim Y^perp = dim X                 Mathlib: Subspace.finrank_add_finrank_dualAnnihilator_eq
  annihilator_annihilator   p.16 Theorem 5         Y^perp perp = Y                            Mathlib: Subspace.dualAnnihilator_dualCoannihilator_eq
  dualMap_apply             p.15 (the pairing)     (T^t l)(x) = l(T x)                        Mathlib: LinearMap.dualMap_apply
  kronecker_det                                    det(A (x) B) = det(A)^n det(B)^m           Mathlib: Matrix.det_kronecker
  simpson_exact_two, simpson_fails_four            Exercise 4: Simpson weights 1/3, 4/3, 1/3 are exact on t^0, t^2 and not on t^4
  gauss3_exact_four, gauss3_fails_six              Exercise 4(iii): weights 5/9, 8/9, 5/9 at a^2 = 3/5 are exact up to t^4 and fail at t^6
  congruence_not_trace                             the trace is not a congruence invariant (G = I, P = diag(2, 1))

WHAT THESE PROOFS ARE. The first five are one-line calls to Mathlib: once the file compiles it records that Mathlib's
theorem has the shape the page quotes; it does not re-derive Lax's proofs. The last five are exact rational arithmetic written
out by hand (the even powers of the nodes +-a are written as powers of a^2 = 3/5, so no square root appears); they restate
what ch10-verify.py computes. The Sylvester law, the weights for general a, the tensor product's universal property and
the 'pure tensor iff det = 0' count are not stated in Lean.
-/

open Module
open scoped Kronecker

namespace Book24Dual

/-- The dual basis of a basis `b` satisfies `l_i(e_j) = delta_ij` (Mathlib's `Basis.toDual_apply`). -/
theorem dual_basis_apply {ι K V : Type*} [Field K] [AddCommGroup V] [Module K V] [DecidableEq ι] [Finite ι]
    (b : Basis ι K V) (i j : ι) : b.toDual (b i) (b j) = if i = j then 1 else 0 :=
  b.toDual_apply i j

/-- Theorem 4 (Lax p.15-16): `dim Y + dim Y^perp = dim X`. -/
theorem annihilator_dim {K V : Type*} [Field K] [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    (W : Subspace K V) :
    finrank K W + finrank K W.dualAnnihilator = finrank K V :=
  Subspace.finrank_add_finrank_dualAnnihilator_eq W

/-- Theorem 5 (Lax p.16): `Y^perp perp = Y`, with the double dual identified with `V`. -/
theorem annihilator_annihilator {K V : Type*} [Field K] [AddCommGroup V] [Module K V]
    (W : Subspace K V) :
    W.dualAnnihilator.dualCoannihilator = W :=
  Subspace.dualAnnihilator_dualCoannihilator_eq

/-- The dual (transpose) map: `(T^t l)(x) = l(T x)`. -/
theorem dualMap_apply {K V U : Type*} [Field K] [AddCommGroup V] [Module K V] [AddCommGroup U] [Module K U]
    (f : V →ₗ[K] U) (g : Dual K U) (x : V) : f.dualMap g x = g (f x) :=
  LinearMap.dualMap_apply f g x

/-- `det (A (x) B) = det A ^ n * det B ^ m` for `A` of size `m` and `B` of size `n`. -/
theorem kronecker_det {m n R : Type*} [Fintype m] [Fintype n] [DecidableEq m] [DecidableEq n] [CommRing R]
    (A : Matrix m m R) (B : Matrix n n R) :
    (A ⊗ₖ B).det = A.det ^ Fintype.card n * B.det ^ Fintype.card m :=
  Matrix.det_kronecker A B

/-- Simpson's weights on the nodes -1, 0, 1 are exact on 1 and t^2 (integrals 2 and 2/3). -/
theorem simpson_exact_two :
    ((1 / 3 : ℚ) + 4 / 3 + 1 / 3 = 2) ∧
    ((1 / 3 : ℚ) * (-1) ^ 2 + 4 / 3 * 0 ^ 2 + 1 / 3 * 1 ^ 2 = 2 / 3) := by
  constructor <;> norm_num

/-- ... and fail on t^4 (rule 2/3, integral 2/5). -/
theorem simpson_fails_four :
    (1 / 3 : ℚ) * (-1) ^ 4 + 4 / 3 * 0 ^ 4 + 1 / 3 * 1 ^ 4 ≠ 2 / 5 := by
  norm_num

/-- The weights 5/9, 8/9, 5/9 on the nodes -a, 0, a with a^2 = 3/5 are exact on 1, t^2 and t^4. The even powers of the
nodes appear as 3/5 and (3/5)^2. -/
theorem gauss3_exact_four :
    ((5 / 9 : ℚ) + 8 / 9 + 5 / 9 = 2) ∧
    (2 * (5 / 9 : ℚ) * (3 / 5) = 2 / 3) ∧
    (2 * (5 / 9 : ℚ) * (3 / 5) ^ 2 = 2 / 5) := by
  refine ⟨?_, ?_, ?_⟩ <;> norm_num

/-- ... and fail at t^6 (rule 6/25, integral 2/7). -/
theorem gauss3_fails_six :
    2 * (5 / 9 : ℚ) * (3 / 5) ^ 3 ≠ 2 / 7 := by
  norm_num

/-- The trace is not a congruence invariant: for `G = I` and `P = diag(2, 1)` the trace of `P^T G P` is 5, not 2. -/
theorem congruence_not_trace :
    Matrix.trace ((!![2, 0; 0, 1] : Matrix (Fin 2) (Fin 2) ℚ)ᵀ * (1 : Matrix (Fin 2) (Fin 2) ℚ) *
      (!![2, 0; 0, 1] : Matrix (Fin 2) (Fin 2) ℚ)) ≠ Matrix.trace (1 : Matrix (Fin 2) (Fin 2) ℚ) := by
  first
    | (simp [Matrix.trace_fin_two, Matrix.mul_fin_two]; norm_num; done)
    | (norm_num [Matrix.trace, Matrix.mul_apply, Fin.sum_univ_two]; done)
    | (rw [Matrix.trace_fin_two, Matrix.trace_fin_two, Matrix.mul_fin_two, Matrix.mul_fin_two]; norm_num; done)

#print axioms Book24Dual.dual_basis_apply
#print axioms Book24Dual.annihilator_dim
#print axioms Book24Dual.annihilator_annihilator
#print axioms Book24Dual.dualMap_apply
#print axioms Book24Dual.kronecker_det
#print axioms Book24Dual.simpson_exact_two
#print axioms Book24Dual.simpson_fails_four
#print axioms Book24Dual.gauss3_exact_four
#print axioms Book24Dual.gauss3_fails_six
#print axioms Book24Dual.congruence_not_trace

end Book24Dual
