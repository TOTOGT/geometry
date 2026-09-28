/-
  book28/IndexTwoWays.lean — one number, counted from the analytic side.
  Principia Orthogona, Book XXVIII ch 7. Pablo Nogueira Grossi, G6 LLC, 2026.

  Dugger (§27, Table 27.2 and Prop. 27.4) computes the Euler characteristic of the line bundle
  O(k) on complex projective space CPⁿ from its sheaf cohomology:
      χ(CPⁿ; O(k)) = dim S^k(ℂ^{n+1})                 for k ≥ 0,
                   = 0                                 for −n ≤ k < 0,
                   = (−1)ⁿ dim S^{−k−(n+1)}(ℂ^{n+1})   for k < −n,
  where S^d(ℂ^{n+1}) is the space of homogeneous polynomials of degree d in n+1 variables,
  and shows that all three cases are the single binomial coefficient C(n+k, n).

  This file proves the counting fact under those formulas: the number of monomials of degree d
  in n+1 variables is C(n+d, n), and the binomial polynomial (k+1)(k+2)…(k+n)/n! vanishes on
  −n ≤ k < 0, as the middle case says. Its topological side, the residue computation of the Todd
  number, is checked numerically by book28/ch07-verify.py and not proved here.

  WHAT IS NOT HERE: no sheaf, no cohomology group, no Todd class, no index theorem.
-/
import Mathlib.Data.Sym.Card
import Mathlib.Data.Nat.Choose.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Data.Fintype.Card

namespace IndexTwoWays

/-- The number of monomials of degree d in n+1 variables is C(n+d, n): dim S^d(ℂ^{n+1}). -/
theorem card_monomials (n d : ℕ) : Fintype.card (Sym (Fin (n + 1)) d) = (n + d).choose n := by
  rw [Sym.card_sym_eq_choose]
  simp [Nat.add_comm]
  rw [Nat.choose_symm_add]

/-- Dugger's middle case: C(n+k, n) is zero for −n ≤ k < 0, read with k = −j, 1 ≤ j ≤ n. -/
theorem choose_zero_between (n j : ℕ) (hj : 1 ≤ j) (hjn : j ≤ n) : (n - j).choose n = 0 := by
  apply Nat.choose_eq_zero_of_lt; omega

/-- n = 1: χ(CP¹; O(k)) = k + 1 for k ≥ 0, the Riemann–Roch count of ch 4 with g = 0. -/
theorem P1_count (k : ℕ) : Fintype.card (Sym (Fin 2) k) = k + 1 := by
  have := card_monomials 1 k
  simpa [Nat.choose_one_right, Nat.add_comm] using this

end IndexTwoWays

#print axioms IndexTwoWays.card_monomials
#print axioms IndexTwoWays.choose_zero_between
#print axioms IndexTwoWays.P1_count
