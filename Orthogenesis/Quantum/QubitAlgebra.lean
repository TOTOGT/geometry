import Mathlib

-- GATE-DECLARE: sorries = none
-- GATE-REASON: Pauli algebra, a Clifford conjugation, and the inner-product core of
--   no-cloning, stated over explicit 2x2 complex matrices and an abstract inner-product
--   space. UNTESTED when written: no toolchain in the session that wrote it. The author
--   runs `lake build Orthogenesis.Quantum.QubitAlgebra`; errors get fixed against the
--   compiler's actual output. NOT yet imported from Orthogenesis.lean (add the import in
--   the commit that follows a clean build).
--
-- What each theorem actually says (read these, not just the names):
--   * pauli_*       : the Pauli matrices square to 1, satisfy XY = iZ, YZ = iX, ZX = iY,
--                     and X, Z anticommute. These are identities between explicit
--                     matrices, proved entrywise. Not vacuous: change a sign in the
--                     definition of Y and `X_mul_Y` fails.
--   * clifford_conj : (X+Z) X (X+Z) = 2 Z. This is the Hadamard conjugation H X H = Z
--                     with the 1/sqrt 2 factors multiplied out (2 = (sqrt 2)^2), so no
--                     real square roots are needed.
--   * clone_overlap : c = c^2 over the complex numbers forces c = 0 or c = 1.
--   * no_cloning    : if a linear isometry U sends pair φ b to pair φ φ and pair ψ b to
--                     pair ψ ψ, where `pair` has the tensor-product inner product and b is
--                     a unit vector, then ⟪φ,ψ⟫ = 0 or 1. The hypothesis `hpair` is
--                     exactly the defining property of the tensor product's inner
--                     product, and it is satisfied by the Kronecker product (checked
--                     numerically in quantum-maths/qm1-verify.py, not in Lean). This is
--                     the abstract no-cloning argument; it does not construct a tensor
--                     product inside Lean.
--   Not claimed: that these matrices are unitary (stated in the page and the checker, not
--   here), or anything about the Bloch sphere.

open Matrix Complex

namespace Orthogenesis.Quantum

def X : Matrix (Fin 2) (Fin 2) ℂ := !![0, 1; 1, 0]
def Y : Matrix (Fin 2) (Fin 2) ℂ := !![0, -I; I, 0]
def Z : Matrix (Fin 2) (Fin 2) ℂ := !![1, 0; 0, -1]

theorem pauli_X_sq : X * X = 1 := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [X, Matrix.mul_apply, Fin.sum_univ_two]

theorem pauli_Y_sq : Y * Y = 1 := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [Y, Matrix.mul_apply, Fin.sum_univ_two]

theorem pauli_Z_sq : Z * Z = 1 := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [Z, Matrix.mul_apply, Fin.sum_univ_two]

theorem X_mul_Y : X * Y = I • Z := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [X, Y, Z, Matrix.mul_apply, Fin.sum_univ_two]

theorem Y_mul_Z : Y * Z = I • X := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [X, Y, Z, Matrix.mul_apply, Fin.sum_univ_two]

theorem Z_mul_X : Z * X = I • Y := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [X, Y, Z, Matrix.mul_apply, Fin.sum_univ_two]

theorem pauli_XZ_anticomm : X * Z = -(Z * X) := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [X, Z, Matrix.mul_apply, Fin.sum_univ_two]

theorem clifford_conj : (X + Z) * X * (X + Z) = (2 : ℂ) • Z := by
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [X, Z, Matrix.mul_apply, Fin.sum_univ_two] <;> norm_num

theorem clone_overlap (c : ℂ) (h : c = c ^ 2) : c = 0 ∨ c = 1 := by
  have h0 : c * (c - 1) = 0 := by linear_combination (-1 : ℂ) * h
  rcases mul_eq_zero.mp h0 with h1 | h1
  · exact Or.inl h1
  · exact Or.inr (sub_eq_zero.mp h1)

theorem no_cloning {V E : Type*}
    [NormedAddCommGroup V] [InnerProductSpace ℂ V]
    [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    (pair : V → V → E)
    (hpair : ∀ a b c d, inner ℂ (pair a b) (pair c d) = inner ℂ a c * inner ℂ b d)
    (U : E →ₗᵢ[ℂ] E) (b : V) (hb : ‖b‖ = 1) (φ ψ : V)
    (hφ : U (pair φ b) = pair φ φ) (hψ : U (pair ψ b) = pair ψ ψ) :
    inner ℂ φ ψ = 0 ∨ inner ℂ φ ψ = 1 := by
  have h1 : inner ℂ (U (pair φ b)) (U (pair ψ b)) = inner ℂ φ ψ := by
    rw [LinearIsometry.inner_map_map, hpair, inner_self_eq_norm_sq_to_K, hb]
    simp
  have h2 : inner ℂ (pair φ φ) (pair ψ ψ) = (inner ℂ φ ψ) ^ 2 := by
    rw [hpair]; ring
  rw [hφ, hψ, h2] at h1
  exact clone_overlap _ h1.symm

end Orthogenesis.Quantum

#print axioms Orthogenesis.Quantum.pauli_X_sq
#print axioms Orthogenesis.Quantum.pauli_Y_sq
#print axioms Orthogenesis.Quantum.pauli_Z_sq
#print axioms Orthogenesis.Quantum.X_mul_Y
#print axioms Orthogenesis.Quantum.Y_mul_Z
#print axioms Orthogenesis.Quantum.Z_mul_X
#print axioms Orthogenesis.Quantum.pauli_XZ_anticomm
#print axioms Orthogenesis.Quantum.clifford_conj
#print axioms Orthogenesis.Quantum.clone_overlap
#print axioms Orthogenesis.Quantum.no_cloning
