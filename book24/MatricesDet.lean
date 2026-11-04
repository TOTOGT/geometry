import Mathlib

/-
Book XXIV, chapter 6: matrices and determinants. Lean core.

STATUS: COMPILED on the author's machine, 2026-11-04. It was written without a toolchain; then
`lake env lean book24/MatricesDet.lean 2>&1 | tee book24/matricesdet.axioms.txt` was run. The report lists all nine
theorems, each depending only on [propext, Classical.choice, Quot.sound], and no sorryAx.

The statements follow Lax, Linear Algebra and Its Applications (2nd ed.), Chapters 4 and 5 (scan page = printed + 17):
  product_is_composition     p.35   the product of matrices is the matrix of the composed maps
  det_product                p.49   Theorem 2: det(BA) = det A det B
  invertible_iff_det_ne_zero p.51   Corollary 3 and its converse (over a field)
  rank_transpose_eq          p.27   row rank = column rank (Chapter 3, Theorem 6, with his remark on p.28)
  cramer_solves              p.54   Cramer's rule, in the form A (cramer A b) = det A . b
  trace_comm                 p.55   Theorem 8(b): tr(AB) = tr(BA)
  similar_det                p.56   Theorem 9 (determinant part): similar matrices have the same determinant
  control_singular           a control: [[1,2],[2,4]] has determinant 0 and is not invertible
  control_det_not_linear     a control: det(2 . 1) = 4 is not 2 det 1, so determinant is not a linear function

WHAT THESE PROOFS ARE. Most are one-line calls to Mathlib's own lemmas (Matrix.mulVec_mulVec, Matrix.det_mul,
Matrix.isUnit_iff_isUnit_det, Matrix.rank_transpose, Matrix.mulVec_cramer, Matrix.trace_mul_comm,
Matrix.det_conj). So this file would check that Lax's statements, as formal sentences, are true over the stated
rings and fields; it would not re-derive his proofs. The two controls are checked by direct computation.

WHAT IT DOES NOT STATE. Gaussian elimination, the Leibniz formula as a definition, the cofactor inverse
(Theorem 7), the volume interpretation of the determinant, and the finite-field counts on the page.
-/

open Matrix

namespace Book24MD

theorem product_is_composition {K : Type*} [CommRing K] {n m l : ℕ}
    (A : Matrix (Fin n) (Fin m) K) (B : Matrix (Fin m) (Fin l) K) (v : Fin l → K) :
    (A * B).mulVec v = A.mulVec (B.mulVec v) := by
  rw [Matrix.mulVec_mulVec]

theorem det_product {K : Type*} [CommRing K] {n : ℕ} (A B : Matrix (Fin n) (Fin n) K) :
    (B * A).det = A.det * B.det := by
  rw [Matrix.det_mul]; ring

theorem invertible_iff_det_ne_zero {K : Type*} [Field K] {n : ℕ} (A : Matrix (Fin n) (Fin n) K) :
    IsUnit A ↔ A.det ≠ 0 := by
  rw [Matrix.isUnit_iff_isUnit_det, isUnit_iff_ne_zero]

theorem rank_transpose_eq {K : Type*} [Field K] {n m : ℕ} (A : Matrix (Fin n) (Fin m) K) :
    Aᵀ.rank = A.rank :=
  Matrix.rank_transpose A

theorem cramer_solves {K : Type*} [CommRing K] {n : ℕ} (A : Matrix (Fin n) (Fin n) K) (b : Fin n → K) :
    A.mulVec (Matrix.cramer A b) = A.det • b :=
  Matrix.mulVec_cramer A b

theorem trace_comm {K : Type*} [CommRing K] {n m : ℕ}
    (A : Matrix (Fin n) (Fin m) K) (B : Matrix (Fin m) (Fin n) K) :
    (A * B).trace = (B * A).trace :=
  Matrix.trace_mul_comm A B

theorem similar_det {K : Type*} [Field K] {n : ℕ} (P A : Matrix (Fin n) (Fin n) K) (hP : P.det ≠ 0) :
    (P * A * P⁻¹).det = A.det :=
  Matrix.det_conj ((Matrix.isUnit_iff_isUnit_det P).2 (isUnit_iff_ne_zero.2 hP)) A

theorem control_singular : ¬ IsUnit (!![(1 : ℚ), 2; 2, 4]) := by
  intro h
  have h2 := (Matrix.isUnit_iff_isUnit_det _).1 h
  norm_num [Matrix.det_fin_two_of] at h2

theorem control_det_not_linear :
    (((2 : ℚ) • (1 : Matrix (Fin 2) (Fin 2) ℚ)).det) ≠ 2 * (1 : Matrix (Fin 2) (Fin 2) ℚ).det := by
  rw [Matrix.det_smul, Matrix.det_one]
  simp
  norm_num

end Book24MD

#print axioms Book24MD.product_is_composition
#print axioms Book24MD.det_product
#print axioms Book24MD.invertible_iff_det_ne_zero
#print axioms Book24MD.rank_transpose_eq
#print axioms Book24MD.cramer_solves
#print axioms Book24MD.trace_comm
#print axioms Book24MD.similar_det
#print axioms Book24MD.control_singular
#print axioms Book24MD.control_det_not_linear
