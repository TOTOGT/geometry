import Mathlib

open Complex

namespace DomainCheck

/-!
Does the Gammaℝ-route functional equation admit integers that
`logDeriv_riemannZeta_one_sub` excludes?

That theorem assumes  `hs : ∀ n : ℤ, s ≠ n`  — every integer is out.
The Gammaℝ route assumes only the poles of its own digamma terms:
  hΓ  : ∀ n : ℕ, s ≠ -(2 * n)        -- poles of digamma (s/2)
  hΓ' : ∀ n : ℕ, (1 - s) ≠ -(2 * n)  -- poles of digamma ((1-s)/2)

Claim: s = -1 and s = 2 satisfy hΓ and hΓ', and fail hs.
-/

-- hΓ at s = -1.  Also hΓ' at s = 2, since 1 - 2 = -1.
theorem hG_neg_one : ∀ n : ℕ, (-1 : ℂ) ≠ -(2 * n) := by
  intro n h
  rw [neg_inj] at h
  have : (1 : ℕ) = 2 * n := by exact_mod_cast h
  omega

-- hΓ' at s = -1 (1 - (-1) = 2).  Also hΓ at s = 2.
theorem hG_two : ∀ n : ℕ, (2 : ℂ) ≠ -(2 * n) := by
  intro n h
  have : (2 : ℤ) = -(2 * n) := by exact_mod_cast h
  omega

-- and both points are excluded by the merged theorem's hypothesis
theorem hs_fails_at_neg_one : ¬ (∀ n : ℤ, (-1 : ℂ) ≠ n) :=
  fun h => h (-1) (by norm_num)

theorem hs_fails_at_two : ¬ (∀ n : ℤ, (2 : ℂ) ≠ n) :=
  fun h => h 2 (by norm_num)

-- the zeta side conditions at those points
theorem zeta_two_ne_zero : riemannZeta 2 ≠ 0 :=
  riemannZeta_ne_zero_of_one_lt_re (by norm_num)

end DomainCheck
