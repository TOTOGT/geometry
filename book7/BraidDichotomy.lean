import Mathlib

/-!
# Abelian or non-abelian: a dichotomy for braid generators

STATUS (2026-11-11): WRITTEN, NOT YET COMPILED (no Lean on the machine that wrote it).
Run by `.github/workflows/jacobian-lean.yml`. Not evidence until that run is green (R22).

Content: classical group theory, not a new result. If two elements a, b of a group satisfy the
braid relation aba = bab and also commute, then a = b. Hence for any family of "braid
generators" σ_0, ..., σ_{n-2} in a group G, either all of them are equal (an abelian anyon
model: one statistics phase) or some adjacent pair fails to commute (a non-abelian model).
In a commutative target group (for example U(1), the pointed braided case where every fusion
space is one-dimensional) only the first branch can occur.

Not formalised: braided fusion categories, R-symbols, the coherence field Ω of
ch7-topological-orthogenesis.html, and clause (3) of its Theorem 7.1.
-/

namespace BraidDichotomy

/-- Braid relation plus commutation forces equality. -/
theorem eq_of_braid_of_commute {G : Type*} [Group G] {a b : G}
    (hbraid : a * b * a = b * a * b) (hcomm : a * b = b * a) : a = b := by
  have h1 : a * a * b = a * b * b := by
    calc a * a * b = a * (a * b) := mul_assoc a a b
      _ = a * (b * a) := by rw [hcomm]
      _ = a * b * a := (mul_assoc a b a).symm
      _ = b * a * b := hbraid
      _ = a * b * b := by rw [← hcomm]
  have h2 : a * a = a * b := mul_right_cancel h1
  exact mul_left_cancel h2

/-- If adjacent generators commute, all generators coincide with the first. -/
theorem all_equal_of_adjacent_commute {G : Type*} [Group G] (n : ℕ) (σ : ℕ → G)
    (hbraid : ∀ i, i + 1 < n → σ i * σ (i + 1) * σ i = σ (i + 1) * σ i * σ (i + 1))
    (hcomm : ∀ i, i + 1 < n → σ i * σ (i + 1) = σ (i + 1) * σ i) :
    ∀ k, k < n → σ k = σ 0 := by
  intro k
  induction k with
  | zero => intro _; rfl
  | succ k ih =>
    intro hk
    have h1 : σ k = σ (k + 1) := eq_of_braid_of_commute (hbraid k hk) (hcomm k hk)
    rw [← h1]
    exact ih (Nat.lt_of_succ_lt hk)

/-- The dichotomy: either one common generator (abelian) or a non-commuting adjacent pair. -/
theorem abelian_or_noncommuting {G : Type*} [Group G] (n : ℕ) (σ : ℕ → G)
    (hbraid : ∀ i, i + 1 < n → σ i * σ (i + 1) * σ i = σ (i + 1) * σ i * σ (i + 1)) :
    (∀ k, k < n → σ k = σ 0) ∨ ∃ i, i + 1 < n ∧ σ i * σ (i + 1) ≠ σ (i + 1) * σ i := by
  by_cases h : ∀ i, i + 1 < n → σ i * σ (i + 1) = σ (i + 1) * σ i
  · exact Or.inl (all_equal_of_adjacent_commute n σ hbraid h)
  · right
    push_neg at h
    exact h

/-- In a commutative target (phases, the pointed case) only the abelian branch occurs. -/
theorem commutative_target_all_equal {G : Type*} [CommGroup G] (n : ℕ) (σ : ℕ → G)
    (hbraid : ∀ i, i + 1 < n → σ i * σ (i + 1) * σ i = σ (i + 1) * σ i * σ (i + 1)) :
    ∀ k, k < n → σ k = σ 0 :=
  all_equal_of_adjacent_commute n σ hbraid (fun _ _ => mul_comm _ _)

/-- The second branch is inhabited: two adjacent transpositions in S₃ satisfy the braid relation
and do not commute. -/
theorem noncommuting_example :
    ((Equiv.swap (0 : Fin 3) 1) * (Equiv.swap 1 2) * (Equiv.swap 0 1) =
      (Equiv.swap 1 2) * (Equiv.swap 0 1) * (Equiv.swap 1 2)) ∧
    ((Equiv.swap (0 : Fin 3) 1) * (Equiv.swap 1 2) ≠ (Equiv.swap 1 2) * (Equiv.swap 0 1)) := by
  constructor <;> decide

end BraidDichotomy

#print axioms BraidDichotomy.abelian_or_noncommuting
#print axioms BraidDichotomy.commutative_target_all_equal
#print axioms BraidDichotomy.noncommuting_example
