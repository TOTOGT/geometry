/-
Volume XVIII — chapters 2, 3 and 4. What the chain-rule chapters computed in Python,
stated and checked by the kernel.

  §1  The corpus's operators C₃ and K₃, copied verbatim from
      AMonster/dm3_operators.lean (that file is not in a build target; the copy is
      checked for drift by book18/ch02-verify.py). Chapter 2's finding:
      C₃ ∘ K₃ = C₃ exactly, and K₃ ∘ C₃ is C₃ shifted by a constant — so the two
      orders differ as maps but have the same derivative everywhere.
  §2  Chapter 3's finding: C₃ does not depend on the input z at all, which is why
      backpropagation through the generator returns ∂/∂z = 0.
  §3  Chapter 4: Euler's rule "higher differentials vanish" as an algebra. In any
      commutative ring with ε·ε = 0, (a + bε)^(n+1) = a^(n+1) + (n+1)·a^n·b·ε.
      With a = p and b = dp this is d(p^(n+1)) = (n+1) p^n dp — the chain rule
      Euler used without stating (Katz, in Bradley & Sandifer 2007, p. 224).

Toolchain: the repository pin, leanprover/lean4:v4.32.0 with Mathlib v4.32.0.
-/
import Mathlib

namespace Book18

/-- A state (r, θ, z), as in AMonster/dm3_operators.lean. -/
abbrev State := ℝ × ℝ × ℝ

/-- **C₃** — Contact constraint (verbatim from AMonster/dm3_operators.lean). -/
def C₃ : State → State
  | (r, θ, _) => (r, θ, r ^ 2 * θ)

/-- **K₃** — Reeb kinetics (verbatim from AMonster/dm3_operators.lean). -/
def K₃ : State → State
  | (r, θ, z) => (r, θ, z + 1)

/-! ## §1  The non-commutation the derivative cannot see -/

/-- Constraint after kinetics is just constraint: C₃ overwrites the z that K₃ shifted. -/
theorem C₃_comp_K₃ : C₃ ∘ K₃ = C₃ := by
  funext ⟨r, θ, z⟩
  rfl

/-- Kinetics after constraint is constraint plus a constant. -/
theorem K₃_comp_C₃ : K₃ ∘ C₃ = fun s => C₃ s + ((0 : ℝ), (0 : ℝ), (1 : ℝ)) := by
  funext ⟨r, θ, z⟩
  simp [C₃, K₃]

/-- The two orders differ as maps (AMonster's `C₃_K₃_noncommutative`)… -/
theorem orders_differ : C₃ ∘ K₃ ≠ K₃ ∘ C₃ := by
  intro h
  have := congrFun h (1, 1, 0)
  simp [C₃, K₃] at this

/-- …but have the same derivative at every point. -/
theorem same_derivative (s : State) :
    fderiv ℝ (C₃ ∘ K₃) s = fderiv ℝ (K₃ ∘ C₃) s := by
  rw [C₃_comp_K₃, K₃_comp_C₃, fderiv_add_const]

/-! ## §2  The input z cannot matter -/

/-- C₃ ignores its third coordinate, so no gradient flows back to z. -/
theorem C₃_ignores_z (r θ z z' : ℝ) : C₃ (r, θ, z) = C₃ (r, θ, z') := rfl

/-! ## §3  Euler's algebra: ε² = 0 -/

/-- In a commutative ring where ε² = 0, powers expand to first order only. -/
theorem dual_pow {R : Type*} [CommRing R] (ε a b : R) (hε : ε * ε = 0) (n : ℕ) :
    (a + b * ε) ^ (n + 1) = a ^ (n + 1) + ((n : R) + 1) * a ^ n * b * ε := by
  induction n with
  | zero => simp
  | succ k ih =>
    rw [pow_succ, ih]
    push_cast
    linear_combination ((k : R) + 1) * a ^ k * b ^ 2 * hε

end Book18

#print axioms Book18.C₃_comp_K₃
#print axioms Book18.K₃_comp_C₃
#print axioms Book18.orders_differ
#print axioms Book18.same_derivative
#print axioms Book18.C₃_ignores_z
#print axioms Book18.dual_pow
