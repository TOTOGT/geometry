import Mathlib

/-
Book XXIV, chapter 9: the numerical side (norms, singular values, conditioning). Lean core.

STATUS: COMPILED 2026-11-04, NINE OF TEN CLEAN. The first run (output in numerical.axioms.txt) accepted the first nine
theorems with axioms [propext, Classical.choice, Quot.sound] only, and failed on `control_hilbert3_inverse`: the `simp`
step left `![9, -36, 30] 2` and the `vecCons ... 2` terms unevaluated, so nine goals stayed open and the theorem
carries sorryAx. The proof of that one theorem has since been replaced (a `first` over `Matrix.mul_fin_three` and a
`simp` with `Matrix.vecHead`/`Matrix.vecTail`); the replacement has NOT been compiled. Two lint warnings in the first run
say the fallback alternatives in `opNorm_comp_le` and `gram_same_nonzero_spectrum` never ran: the first alternative
worked in both, so the fallbacks are harmless and can be dropped. Recompile with
`lake env lean book24/Numerical.lean 2>&1 | tee book24/numerical.axioms.txt` and read the real output.

The statements follow Lax, Linear Algebra and Its Applications (2nd ed.), Chapters 7, 10 and 17 (scan page = printed + 17):
  opNorm_le                    p.90   |Az| <= |A| |z|                                    Theorem 13 (33)
  opNorm_comp_le               p.90   |CA| <= |C| |A|                                    Theorem 14 (36)
  condition_ge_one             p.248  K(A) = |A| |A^-1| >= 1                             Exercise 1
  sensitivity                  p.247  |dx| |b| <= K |db| |x|  (Lax (4)' and (5), with the division cleared)
  gram_det                     p.170  det(A^T A) = det(A)^2   (the product of the squared singular values)
  trace_sq_gram                       trace((A^T A)^2) = F^2 - 2 det^2 for a 2x2 matrix, written out in the entries;
                                      this is why K(A^T A) = K(A)^2 in the 2x2 case
  frobenius_det_bounds                F - 2 det = (a-d)^2 + (b+c)^2 and F + 2 det = (a+d)^2 + (b-c)^2, so F >= 2|det|
  left_inverse_normal                 (A^T A)^-1 A^T is a left inverse of A when A^T A is invertible
  gram_same_nonzero_spectrum   p.171  Exercise 14: A A^T and A^T A have the same nonzero eigenvalues, as charpolys
  control_hilbert3_inverse            the Hilbert matrix H_3 has the integer inverse the page prints

WHAT THESE PROOFS ARE. Most are one-line calls to Mathlib or short algebra (`ring`, `nlinarith`). So once the file
compiles, it checks that these statements, as formal sentences, are true; it does not re-derive Lax's proofs, and it
does not state the singular value decomposition or the polar decomposition (Mathlib's versions are not used here).

WHAT IT DOES NOT STATE. The existence of the singular value decomposition, the formula |A|_2^2 = largest eigenvalue
of A^T A, the equality K(A) = sigma_max / sigma_min, and everything about floating point. Those are checked by the
script on exact families, not by Lean.
-/

open Matrix Polynomial

namespace Book24Nm

theorem opNorm_le {E F : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    [NormedAddCommGroup F] [NormedSpace ℝ F] (A : E →L[ℝ] F) (z : E) :
    ‖A z‖ ≤ ‖A‖ * ‖z‖ :=
  A.le_opNorm z

theorem opNorm_comp_le {E F G : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    [NormedAddCommGroup F] [NormedSpace ℝ F] [NormedAddCommGroup G] [NormedSpace ℝ G]
    (C : F →L[ℝ] G) (A : E →L[ℝ] F) :
    ‖C.comp A‖ ≤ ‖C‖ * ‖A‖ := by
  first
  | exact C.opNorm_comp_le A
  | exact C.op_norm_comp_le A

theorem condition_ge_one {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] [Nontrivial E]
    (A B : E →L[ℝ] E) (hBA : B.comp A = ContinuousLinearMap.id ℝ E) :
    1 ≤ ‖A‖ * ‖B‖ := by
  have h := opNorm_comp_le B A
  rw [hBA, ContinuousLinearMap.norm_id] at h
  rw [mul_comm]
  exact h

theorem sensitivity {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (A B : E →L[ℝ] E) (hBA : ∀ y, B (A y) = y) (x dx : E) :
    ‖dx‖ * ‖A x‖ ≤ (‖A‖ * ‖B‖) * (‖A dx‖ * ‖x‖) := by
  have h1 : ‖dx‖ ≤ ‖B‖ * ‖A dx‖ := by
    calc ‖dx‖ = ‖B (A dx)‖ := by rw [hBA]
      _ ≤ ‖B‖ * ‖A dx‖ := B.le_opNorm _
  have h2 : ‖A x‖ ≤ ‖A‖ * ‖x‖ := A.le_opNorm x
  calc ‖dx‖ * ‖A x‖ ≤ (‖B‖ * ‖A dx‖) * (‖A‖ * ‖x‖) :=
        mul_le_mul h1 h2 (norm_nonneg _) (by positivity)
    _ = (‖A‖ * ‖B‖) * (‖A dx‖ * ‖x‖) := by ring

theorem gram_det {m : Type*} [Fintype m] [DecidableEq m] {R : Type*} [CommRing R]
    (A : Matrix m m R) : (Aᵀ * A).det = A.det ^ 2 := by
  rw [Matrix.det_mul, Matrix.det_transpose, sq]

theorem trace_sq_gram (a b c d : ℝ) :
    (a ^ 2 + c ^ 2) ^ 2 + 2 * (a * b + c * d) ^ 2 + (b ^ 2 + d ^ 2) ^ 2
      = (a ^ 2 + b ^ 2 + c ^ 2 + d ^ 2) ^ 2 - 2 * (a * d - b * c) ^ 2 := by
  ring

theorem frobenius_det_bounds (a b c d : ℝ) :
    a ^ 2 + b ^ 2 + c ^ 2 + d ^ 2 - 2 * (a * d - b * c) = (a - d) ^ 2 + (b + c) ^ 2 ∧
    a ^ 2 + b ^ 2 + c ^ 2 + d ^ 2 + 2 * (a * d - b * c) = (a + d) ^ 2 + (b - c) ^ 2 ∧
    2 * |a * d - b * c| ≤ a ^ 2 + b ^ 2 + c ^ 2 + d ^ 2 := by
  refine ⟨by ring, by ring, ?_⟩
  have h1 : 0 ≤ (a - d) ^ 2 + (b + c) ^ 2 := by positivity
  have h2 : 0 ≤ (a + d) ^ 2 + (b - c) ^ 2 := by positivity
  rcases abs_cases (a * d - b * c) with ⟨h, _⟩ | ⟨h, _⟩ <;> rw [h] <;> nlinarith [h1, h2]

theorem left_inverse_normal {m n : Type*} [Fintype m] [Fintype n] [DecidableEq n]
    (A : Matrix m n ℝ) (h : IsUnit (Aᵀ * A).det) :
    ((Aᵀ * A)⁻¹ * Aᵀ) * A = 1 := by
  rw [Matrix.mul_assoc]
  exact Matrix.nonsing_inv_mul _ h

theorem gram_same_nonzero_spectrum {m n : Type*} [Fintype m] [Fintype n] [DecidableEq m] [DecidableEq n]
    (M : Matrix m n ℝ) :
    (X : ℝ[X]) ^ Fintype.card m * (Mᵀ * M).charpoly = X ^ Fintype.card n * (M * Mᵀ).charpoly := by
  first
  | exact Matrix.charpoly_mul_comm' Mᵀ M
  | exact (Matrix.charpoly_mul_comm' M Mᵀ).symm

theorem control_hilbert3_inverse :
    (!![(9 : ℚ), -36, 30; -36, 192, -180; 30, -180, 180]) *
      (!![(1 : ℚ), 1 / 2, 1 / 3; 1 / 2, 1 / 3, 1 / 4; 1 / 3, 1 / 4, 1 / 5]) = 1 := by
  first
  | (rw [Matrix.mul_fin_three]; norm_num [Matrix.one_fin_three])
  | (ext i j
     fin_cases i <;> fin_cases j <;>
       simp [Matrix.mul_apply, Fin.sum_univ_three, Matrix.vecHead, Matrix.vecTail] <;> norm_num)

end Book24Nm

#print axioms Book24Nm.opNorm_le
#print axioms Book24Nm.opNorm_comp_le
#print axioms Book24Nm.condition_ge_one
#print axioms Book24Nm.sensitivity
#print axioms Book24Nm.gram_det
#print axioms Book24Nm.trace_sq_gram
#print axioms Book24Nm.frobenius_det_bounds
#print axioms Book24Nm.left_inverse_normal
#print axioms Book24Nm.gram_same_nonzero_spectrum
#print axioms Book24Nm.control_hilbert3_inverse
