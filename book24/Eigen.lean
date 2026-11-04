import Mathlib

/-
Book XXIV, chapter 7: eigenvalues and eigenvectors. Lean core.

STATUS: COMPILED on the author's machine, 2026-11-04. It was written without a toolchain. The first compile found
one unknown lemma name (Matrix.smul_mulVec_assoc, in eigen_iff_det_zero); the fix was recompiled with
`lake env lean book24/Eigen.lean 2>&1 | tee book24/eigen.axioms.txt`. The report lists all seven theorems, each
depending only on [propext, Classical.choice, Quot.sound], and no sorryAx. The only remaining output is linter
warnings about unused fallback tactics in eigen_iff_det_zero.

The statements follow Lax, Linear Algebra and Its Applications (2nd ed.), Chapter 6 (scan page = printed + 17):
  eigen_iff_det_zero                p.60-61  a is an eigenvalue of A exactly when det(aI - A) = 0 (over a field)
  power_eigen                       p.59     if A h = a h then A^N h = a^N h
  trace_eq_sum_eigenvalues          p.65     Theorem 3: the sum of the eigenvalues (roots of the characteristic
                                             polynomial, with multiplicity) is the trace   [over C]
  det_eq_prod_eigenvalues           p.65     Theorem 3: their product is the determinant   [over C]
  cayley_hamilton                   p.67     Theorem 5: p_A(A) = 0
  eigenvectors_distinct_independent p.64     Theorem 1: eigenvectors of distinct eigenvalues are independent
  control_rotation_no_real_eigenvalue        a control: the rotation [[0,-1],[1,0]] has no real eigenvector

WHAT THESE PROOFS ARE. The first two are short proofs from Mathlib lemmas about matrices and vectors. The next
four call Mathlib's own theorems (Matrix.trace_eq_sum_roots_charpoly_of_splits, Matrix.det_eq_prod_roots_charpoly_of_splits,
Matrix.aeval_self_charpoly, Module.End.eigenvectors_linearIndependent). So the file would check that Lax's
statements, as formal sentences, are true; it would not re-derive his proofs. The control is by direct computation.

WHAT IT DOES NOT STATE. The existence of an eigenvalue over C by the powers argument (Lax p.60), the Fibonacci
formula, the discriminant classification of 2x2 matrices, the spectral mapping theorem, and the counts on the page.
-/

open Matrix

namespace Book24Ev

theorem eigen_iff_det_zero {K : Type*} [Field K] {n : ℕ} (A : Matrix (Fin n) (Fin n) K) (a : K) :
    (∃ v : Fin n → K, v ≠ 0 ∧ A.mulVec v = a • v) ↔ ((a • (1 : Matrix (Fin n) (Fin n) K)) - A).det = 0 := by
  have key : ∀ v : Fin n → K, A.mulVec v = a • v ↔ ((a • (1 : Matrix (Fin n) (Fin n) K)) - A).mulVec v = 0 := by
    intro v
    have h1 : (a • (1 : Matrix (Fin n) (Fin n) K)).mulVec v = a • v := by
      first
      | simp [Matrix.smul_mulVec]
      | simp [Matrix.smul_mulVec_assoc]
      | (ext i; simp [Matrix.mulVec, dotProduct, Matrix.one_apply, mul_comm])
    rw [Matrix.sub_mulVec, h1, sub_eq_zero]
    exact eq_comm
  simp_rw [key]
  exact Matrix.exists_mulVec_eq_zero_iff

theorem power_eigen {K : Type*} [CommRing K] {n : ℕ} (A : Matrix (Fin n) (Fin n) K) (a : K)
    (v : Fin n → K) (h : A.mulVec v = a • v) (N : ℕ) :
    (A ^ N).mulVec v = a ^ N • v := by
  induction N with
  | zero => simp
  | succ k ih =>
    rw [pow_succ, ← Matrix.mulVec_mulVec, h, Matrix.mulVec_smul, ih, smul_smul, pow_succ']

theorem trace_eq_sum_eigenvalues {n : ℕ} (A : Matrix (Fin n) (Fin n) ℂ) :
    A.trace = A.charpoly.roots.sum :=
  Matrix.trace_eq_sum_roots_charpoly_of_splits (IsAlgClosed.splits _)

theorem det_eq_prod_eigenvalues {n : ℕ} (A : Matrix (Fin n) (Fin n) ℂ) :
    A.det = A.charpoly.roots.prod :=
  Matrix.det_eq_prod_roots_charpoly_of_splits (IsAlgClosed.splits _)

theorem cayley_hamilton {K : Type*} [CommRing K] {n : ℕ} (A : Matrix (Fin n) (Fin n) K) :
    Polynomial.aeval A A.charpoly = 0 :=
  Matrix.aeval_self_charpoly A

theorem eigenvectors_distinct_independent {K V : Type*} [Field K] [AddCommGroup V] [Module K V]
    (f : Module.End K V) (μs : Set K) (xs : μs → V)
    (h : ∀ μ : μs, f.HasEigenvector μ (xs μ)) :
    LinearIndependent K xs :=
  Module.End.eigenvectors_linearIndependent f μs xs h

theorem control_rotation_no_real_eigenvalue (a : ℝ) :
    ¬ ∃ v : Fin 2 → ℝ, v ≠ 0 ∧ (!![(0 : ℝ), -1; 1, 0]).mulVec v = a • v := by
  intro hv
  have h := (eigen_iff_det_zero (!![(0 : ℝ), -1; 1, 0]) a).1 hv
  simp [Matrix.det_fin_two] at h
  nlinarith [sq_nonneg a]

end Book24Ev

#print axioms Book24Ev.eigen_iff_det_zero
#print axioms Book24Ev.power_eigen
#print axioms Book24Ev.trace_eq_sum_eigenvalues
#print axioms Book24Ev.det_eq_prod_eigenvalues
#print axioms Book24Ev.cayley_hamilton
#print axioms Book24Ev.eigenvectors_distinct_independent
#print axioms Book24Ev.control_rotation_no_real_eigenvalue
