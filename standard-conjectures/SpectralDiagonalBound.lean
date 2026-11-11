import Mathlib

/-!
# Diagonal entries of a normal matrix are bounded by its spectral radius

STATUS: UNCOMPILED DRAFT (no Lean toolchain where this was written). Not promoted (R22).
Built only by the manual workflow `jacobian-lean.yml`; read `#print axioms` from that run.

Statement (complex, finite square matrices):
  if `A` is normal and every `μ ∈ spectrum ℂ A` has `‖μ‖ ≤ r`, then `‖A i i‖ ≤ r` for all `i`.

Route (not the convex-hull route): for normal `A`, in the C*-algebra `Matrix n n ℂ` with the
l2 operator norm, `spectralRadius = ‖A‖` (`IsStarNormal.spectralRadius_eq_nnnorm`), and every
entry is at most the operator norm. The convex-hull statement (`A i i` lies in the convex hull
of the spectrum) is stronger and is NOT proved here. Schur–Horn is not used; for normal
matrices the convex-hull fact is the direct computation `A i i = Σ_k |U i k|² λ_k`.

Risk points for the first compile: (1) whether `CStarAlgebra (Matrix n n ℂ)` is found by
instance search under the scoped l2 instances; (2) the entry-vs-norm step via `mulVec`.
-/

open scoped Matrix Matrix.Norms.L2Operator

namespace SpectralDiagonalBound

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- Every entry is bounded by the l2 operator norm. -/
theorem entry_norm_le_opNorm (A : Matrix n n ℂ) (i j : n) : ‖A i j‖ ≤ ‖A‖ := by
  have h := Matrix.l2_opNorm_mulVec A (WithLp.toLp 2 (Pi.single j (1 : ℂ)))
  have hx : ‖(WithLp.toLp 2 (Pi.single j (1 : ℂ)) : EuclideanSpace ℂ n)‖ = 1 := by
    simpa using (PiLp.norm_single (p := 2) j (1 : ℂ))
  rw [hx, mul_one] at h
  have hc := PiLp.norm_apply_le ((EuclideanSpace.equiv n ℂ).symm
    (A.mulVec (WithLp.toLp 2 (Pi.single j (1 : ℂ))))) i
  refine le_trans ?_ (hc.trans h)
  simp [Matrix.mulVec, dotProduct, Pi.single_apply]

/-- Main statement: bound by any upper bound `r` of the moduli of the spectrum. -/
theorem diag_norm_le_of_spectrum_bound
    (A : Matrix n n ℂ) [IsStarNormal A] {r : NNReal}
    (hr : ∀ μ ∈ spectrum ℂ A, ‖μ‖₊ ≤ r) (i : n) : ‖A i i‖ ≤ r := by
  have hsr : spectralRadius ℂ A ≤ (r : ENNReal) :=
    iSup₂_le fun μ hμ => ENNReal.coe_le_coe.2 (hr μ hμ)
  have hnorm : ‖A‖₊ ≤ r := by
    have := IsStarNormal.spectralRadius_eq_nnnorm A
    rw [this] at hsr
    exact_mod_cast hsr
  exact (entry_norm_le_opNorm A i i).trans (by exact_mod_cast hnorm)

#print axioms entry_norm_le_opNorm
#print axioms diag_norm_le_of_spectrum_bound

end SpectralDiagonalBound
