/-
  book14/TypesDecide.lean — one symbol, two laws: the type decides.
  Principia Orthogona, Book XIV ch 9. Pablo Nogueira Grossi, G6 LLC, 2026.

  Ganesalingam (2013; as reviewed by Aberdein 2017) observes that "the syntax of mathematics
  is type-dependent". I❤LA (Li, Kamil, Jacobson, Gingold 2021) compiles juxtaposition "to the
  appropriate multiplication … depending on the types of the operands". Lean does the same:
  `*` is one symbol, and the elaborator picks its meaning from the types (Book XIX ch 3).

  Here that is exhibited as a difference in *laws*: on ℕ the symbol commutes, and on 2×2
  integer matrices it does not. A reader who knows the symbol but not the type cannot know
  whether a * b = b * a may be used.
-/
import Mathlib.Data.Matrix.Mul
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Algebra.BigOperators.Fin

namespace TypesDecide

/-- On ℕ, `*` commutes. -/
theorem nat_mul_comm (a b : ℕ) : a * b = b * a := Nat.mul_comm a b

/-- The two matrices of the counterexample. -/
def A : Matrix (Fin 2) (Fin 2) ℤ := !![0, 1; 0, 0]
def B : Matrix (Fin 2) (Fin 2) ℤ := !![0, 0; 1, 0]

/-- On 2×2 integer matrices the same symbol does not commute: AB and BA differ in their
    top-left entry (1 against 0). -/
theorem matrix_mul_not_comm : A * B ≠ B * A := by
  intro h
  have := congrFun (congrFun h 0) 0
  simp [A, B, Matrix.mul_apply, Fin.sum_univ_two] at this

end TypesDecide

#print axioms TypesDecide.nat_mul_comm
#print axioms TypesDecide.matrix_mul_not_comm
