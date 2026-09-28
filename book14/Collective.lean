/-
  book14/Collective.lean — collective predicates in the language of mathematics.
  Principia Orthogona, Book XIV ch 2. Pablo Nogueira Grossi, G6 LLC, 2026.

  Arambillete & de Groote (LENLS 21, 2025) open with a sophism:
    "Every set of prime numbers is a fortiori a set of coprime numbers. Therefore, every
     prime number is a coprime number."
  The first sentence is true, and the second is not even false: *coprime* is a relation
  between numbers, used collectively of a set ("these are coprime" = pairwise coprime).
  Read distributively, of one number, it is the statement that {n} is pairwise coprime.
  That holds vacuously for every n, including 4.

  The same trap sits in this series' own title word. *Orthogonal* is a binary relation, and
  "u, v, w are orthogonal" means pairwise. It cannot be read along a chain, because u ⊥ v
  and v ⊥ w do not give u ⊥ w. That is the non-transitivity Book XIV ch 3 found in
  co-predication.
-/
import Mathlib.Data.Nat.Prime.Basic
import Mathlib.Data.Set.Pairwise.Basic

namespace Collective

/-- The sophism's premise, which is true: any set of primes is pairwise coprime. -/
theorem primes_pairwise_coprime (s : Set ℕ) (h : ∀ p ∈ s, p.Prime) : s.Pairwise Nat.Coprime :=
  fun p hp q hq hpq => (Nat.coprime_primes (h p hp) (h q hq)).2 hpq

/-- The distributive reading collapses: a one-element set is pairwise anything, so under it
    every number is "a coprime number", including the composite 4. -/
theorem four_is_coprime_distributively :
    ({4} : Set ℕ).Pairwise Nat.Coprime ∧ ¬ Nat.Prime 4 :=
  ⟨Set.pairwise_singleton _ _, by decide⟩

/-- The collective reading is downward closed, and that is what makes the premise true:
    a subset of a pairwise-coprime set is pairwise coprime. -/
theorem collective_mono {s t : Set ℕ} (hst : s ⊆ t) (ht : t.Pairwise Nat.Coprime) :
    s.Pairwise Nat.Coprime := ht.mono hst

/-- Integer dot product on ℤ², enough to exhibit the trap. -/
def dot (u v : ℤ × ℤ) : ℤ := u.1 * v.1 + u.2 * v.2

/-- *Orthogonal* is not transitive: (1,0) ⊥ (0,1) and (0,1) ⊥ (2,0), but (1,0) · (2,0) = 2.
    So "u, v, w are orthogonal" must mean each pair, not a chain. -/
theorem orthogonal_not_transitive :
    dot (1, 0) (0, 1) = 0 ∧ dot (0, 1) (2, 0) = 0 ∧ dot (1, 0) (2, 0) ≠ 0 := by
  decide

end Collective

#print axioms Collective.primes_pairwise_coprime
#print axioms Collective.four_is_coprime_distributively
#print axioms Collective.collective_mono
#print axioms Collective.orthogonal_not_transitive
