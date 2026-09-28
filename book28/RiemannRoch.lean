/-
  book28/RiemannRoch.lean — the even case, on the sphere: ℓ(d·∞) = d + 1 on CP¹.
  Principia Orthogona, Book XXVIII ch 4. Pablo Nogueira Grossi, G6 LLC, 2026.

  Riemann–Roch for a curve of genus g: ℓ(D) − ℓ(K − D) = deg D − g + 1 (Dugger, Thm 28.16).
  Blackadar (Ex. 24.1.2(b)) reads it as the Atiyah–Singer index of ∂̄ on a Riemann surface,
  the even-dimensional companion of the Toeplitz index in ch 3.

  On CP¹ (g = 0) with D = d·∞, the meromorphic functions with at most a pole of order d at ∞
  are the polynomials of degree ≤ d. This file proves that space has dimension d + 1, which is
  deg D − g + 1 with g = 0, and ℓ(K − D) = 0 because deg(K − D) = −2 − d < 0.

  WHAT IS NOT HERE: no Riemann surface, no divisor, no sheaf cohomology. Mathlib has none of
  the three for curves; the identification of L(d·∞) with polynomials of degree ≤ d is the
  classical one (Dugger §28) and is stated, not proved.
-/
import Mathlib.RingTheory.Polynomial.Basic
import Mathlib.LinearAlgebra.Dimension.Constructions

open Polynomial Module

namespace RiemannRoch

/-- The polynomials of degree < n form a space of dimension n. -/
theorem finrank_degreeLT (F : Type*) [Field F] (n : ℕ) :
    finrank F (degreeLT F n) = n := by
  rw [(degreeLTEquiv F n).finrank_eq]; simp

/-- ℓ(d·∞) on CP¹ is d + 1 = deg D − g + 1 with g = 0. -/
theorem ell_P1 (F : Type*) [Field F] (d : ℕ) :
    (finrank F (degreeLT F (d + 1)) : ℤ) = (d : ℤ) - 0 + 1 := by
  rw [finrank_degreeLT]; push_cast; ring

end RiemannRoch

#print axioms RiemannRoch.finrank_degreeLT
#print axioms RiemannRoch.ell_P1
