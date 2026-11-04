import Mathlib

/-
Book XXIV, chapter 8: inner products and the spectral theorem. Lean core.

STATUS: COMPILED 2026-11-04 by the author (`lake env lean book24/Ortho.lean 2>&1 | tee book24/ortho.axioms.txt`). All eight
theorems depend only on [propext, Classical.choice, Quot.sound]; no sorryAx. Two warnings remain and were left as they are:
`complement` uses a lemma now deprecated in favour of `Submodule.isCompl_orthogonal`, and one `simpa` could be a `simp`.
Fixes made against the compiler's real output: the inner-product and transpose notations were replaced by `@inner` and
`Matrix.transpose`, and `pythagoras` needed an `nlinarith` step because the Mathlib lemma states squares as products.
Compiling shows the statements are true as formal sentences; it does not show they say what the page says (read them).

The statements follow Lax, Linear Algebra and Its Applications (2nd ed.), Chapters 7 and 8 (scan page = printed + 17):
  schwarz                      p.79   |(u,v)| <= |u| |v|                                  Theorem 1
  triangle                     p.80   |u + v| <= |u| + |v|                                Theorem 3
  pythagoras                   p.80   (u,v) = 0 implies |u+v|^2 = |u|^2 + |v|^2
  complement                   p.82   X = Y + Y-perp, with Y and Y-perp complementary    Theorem 6 (finite dimension)
  eigen_equation               p.106  the 2x2 symmetric case: for two distinct roots l1, l2 of the characteristic
                                      polynomial, the vectors (b, l1 - a) and (b, l2 - a) are orthogonal
  eigenbasis_orthonormal       p.106  Theorem 4: a self-adjoint map on a finite-dimensional real inner product space
                                      has an orthonormal basis of eigenvectors, with real eigenvalues
  control_indefinite                  the form x1y1 - x2y2 violates Schwarz
  control_complex_symmetric_nilpotent the complex symmetric matrix [[1,i],[i,-1]] is symmetric, not zero, and squares to 0

WHAT THESE PROOFS ARE. Four are one-line calls to Mathlib (inner-product Schwarz, the triangle inequality, the
Pythagorean identity, the orthogonal complement, and the spectral theorem for symmetric maps). So once the file
compiles, it checks that Lax's statements, as formal sentences, are true; it does not re-derive his proofs.
`eigen_equation` is a short algebra proof by `linear_combination`, and the two controls are direct computations.

WHAT IT DOES NOT STATE. Gram-Schmidt, the projection formula P = A (A^T A)^-1 A^T, least squares, the Hessian test,
and the counts on the page. Those are checked by the script, not by Lean.
-/

namespace Book24Ip

theorem schwarz {V : Type*} [NormedAddCommGroup V] [InnerProductSpace ℝ V] (u v : V) :
    |@inner ℝ V _ u v| ≤ ‖u‖ * ‖v‖ :=
  abs_real_inner_le_norm u v

theorem triangle {V : Type*} [NormedAddCommGroup V] [InnerProductSpace ℝ V] (u v : V) :
    ‖u + v‖ ≤ ‖u‖ + ‖v‖ :=
  norm_add_le u v

theorem pythagoras {V : Type*} [NormedAddCommGroup V] [InnerProductSpace ℝ V] (u v : V)
    (h : @inner ℝ V _ u v = 0) :
    ‖u + v‖ ^ 2 = ‖u‖ ^ 2 + ‖v‖ ^ 2 := by
  have h2 := norm_add_sq_eq_norm_sq_add_norm_sq_real h
  nlinarith [h2]

theorem complement {V : Type*} [NormedAddCommGroup V] [InnerProductSpace ℝ V] [FiniteDimensional ℝ V]
    (K : Submodule ℝ V) : IsCompl K Kᗮ :=
  Submodule.isCompl_orthogonal_of_hasOrthogonalProjection

theorem eigen_equation (a b d l1 l2 : ℝ) (h : l1 ≠ l2)
    (h1 : l1 ^ 2 - (a + d) * l1 + (a * d - b ^ 2) = 0)
    (h2 : l2 ^ 2 - (a + d) * l2 + (a * d - b ^ 2) = 0) :
    b * b + (l1 - a) * (l2 - a) = 0 := by
  have hs : l1 + l2 = a + d := by
    have h3 : (l1 - l2) * (l1 + l2 - (a + d)) = 0 := by linear_combination h1 - h2
    rcases mul_eq_zero.1 h3 with h0 | h0
    · exact absurd (sub_eq_zero.1 h0) h
    · linarith
  have hp : l1 * l2 = a * d - b ^ 2 := by linear_combination (-1 : ℝ) * h1 + l1 * hs
  linear_combination hp - a * hs

theorem eigenbasis_orthonormal {V : Type*} [NormedAddCommGroup V] [InnerProductSpace ℝ V]
    [FiniteDimensional ℝ V] {n : ℕ} (hn : Module.finrank ℝ V = n)
    (T : V →ₗ[ℝ] V) (hT : T.IsSymmetric) :
    ∃ (b : OrthonormalBasis (Fin n) ℝ V) (μ : Fin n → ℝ), ∀ i, T (b i) = μ i • b i :=
  ⟨hT.eigenvectorBasis hn, hT.eigenvalues hn, fun i => by
    simpa using hT.apply_eigenvectorBasis hn i⟩

theorem control_indefinite : ∃ u v : Fin 2 → ℝ,
    (u 0 * v 0 - u 1 * v 1) ^ 2 > (u 0 * u 0 - u 1 * u 1) * (v 0 * v 0 - v 1 * v 1) :=
  ⟨![1, 0], ![2, 1], by norm_num⟩

theorem control_complex_symmetric_nilpotent :
    Matrix.transpose (!![(1 : ℂ), Complex.I; Complex.I, -1]) = !![(1 : ℂ), Complex.I; Complex.I, -1] ∧
    (!![(1 : ℂ), Complex.I; Complex.I, -1]) * (!![(1 : ℂ), Complex.I; Complex.I, -1]) = 0 ∧
    (!![(1 : ℂ), Complex.I; Complex.I, -1]) ≠ 0 := by
  refine ⟨?_, ?_, ?_⟩
  · ext i j
    fin_cases i <;> fin_cases j <;> simp
  · ext i j
    fin_cases i <;> fin_cases j <;> simp [Matrix.mul_apply, Fin.sum_univ_two]
  · intro h
    have h0 := congrFun (congrFun h 0) 0
    simp at h0

end Book24Ip

#print axioms Book24Ip.schwarz
#print axioms Book24Ip.triangle
#print axioms Book24Ip.pythagoras
#print axioms Book24Ip.complement
#print axioms Book24Ip.eigen_equation
#print axioms Book24Ip.eigenbasis_orthonormal
#print axioms Book24Ip.control_indefinite
#print axioms Book24Ip.control_complex_symmetric_nilpotent
