-- GATE-DECLARE: sorries = none
-- GATE-REASON: chH Collatz — the T5 skeleton's conjecture is trivially provable; its implication is Collatz itself; orbit "mean contraction" telescopes; c = 1 also contracts; odd multiples of 3 are transient.
/-
Orthogenesis/Collatz/CollatzChecks.lean — Book 3, Chapter H (Collatz as dm³ Corollary).

  §1  The AXLE Target 5 skeleton. Its structure `DiscreteDM3System` records a carrier type, a
      negative number and a natural number, and nothing about the Collatz map. So its
      "conjecture" `collatz_is_dm3` is provable in a few lines, and the hypothesis of
      `collatz_convergence_from_dm3` is always satisfiable: that theorem, as stated, is the
      Collatz conjecture itself, with no reduction achieved.
  §2  The two-step log-ratios along any positive sequence telescope:
      Σ log(x(j+1)/x j) = log(x N) − log(x 0). For an orbit that reaches 1, the average is fixed
      by the starting value and the orbit's length, not by a universal constant. (Running the
      chapter's own code gives −0.047 for n₀ = 27 and −0.052 for n₀ = 837799, not −0.2901 and
      −0.2878.)
  §3  In the shortcut heuristic the average factor is c/4; among odd c it is below 1 exactly for
      c = 1 and c = 3 — so "only c = 3 contracts" holds only among odd c ≥ 3.
  §4  3 never divides (3n+1)/2^k: once an odd orbit leaves the multiples of 3 it never returns.
-/
import Mathlib

namespace Orthogenesis.CollatzChecks

/-! ## §1  The Target 5 skeleton carries no Collatz content -/

structure DiscreteDM3System where
  carrier : Type
  mean_contraction : ℝ
  contraction_neg : mean_contraction < 0
  triad_coeff : ℕ

theorem collatz_is_dm3_trivial :
    ∃ sys : DiscreteDM3System, sys.carrier = ℕ ∧
      sys.mean_contraction = Real.log (3 / 4) ∧ sys.triad_coeff = 3 :=
  ⟨⟨ℕ, Real.log (3 / 4), Real.log_neg (by norm_num) (by norm_num), 3⟩, rfl, rfl, rfl⟩

theorem skeleton_hypothesis_holds : ∃ sys : DiscreteDM3System, sys.carrier = ℕ :=
  let ⟨sys, h, _⟩ := collatz_is_dm3_trivial; ⟨sys, h⟩

/-- With the hypothesis always true, "hypothesis → P" is just P. -/
theorem skeleton_implication_is_the_conjecture (P : Prop) :
    ((∃ sys : DiscreteDM3System, sys.carrier = ℕ) → P) ↔ P :=
  ⟨fun h => h skeleton_hypothesis_holds, fun p _ => p⟩

/-! ## §2  Orbit log-ratios telescope -/

theorem log_ratios_telescope (x : ℕ → ℝ) (hx : ∀ j, 0 < x j) (N : ℕ) :
    ∑ j ∈ Finset.range N, Real.log (x (j + 1) / x j) = Real.log (x N) - Real.log (x 0) := by
  have h : ∀ j, Real.log (x (j + 1) / x j) = Real.log (x (j + 1)) - Real.log (x j) :=
    fun j => Real.log_div (hx (j + 1)).ne' (hx j).ne'
  simp_rw [h]
  exact Finset.sum_range_sub (fun j => Real.log (x j)) N

/-! ## §3  Which odd multipliers contract on average -/

theorem odd_contracting_multipliers (c : ℕ) (hc : Odd c) :
    (c : ℝ) / 4 < 1 ↔ c = 1 ∨ c = 3 := by
  constructor
  · intro h
    have h4 : (c : ℝ) < 4 := by linarith
    have : c < 4 := by exact_mod_cast h4
    obtain ⟨k, rfl⟩ := hc
    omega
  · rintro (rfl | rfl) <;> norm_num

/-! ## §4  Odd multiples of 3 are transient -/

theorem odd_succ_not_mult_three (n k : ℕ) (h : 2 ^ k ∣ 3 * n + 1) :
    ¬ 3 ∣ (3 * n + 1) / 2 ^ k := by
  intro h3
  have e : 2 ^ k * ((3 * n + 1) / 2 ^ k) = 3 * n + 1 := Nat.mul_div_cancel' h
  have : 3 ∣ 3 * n + 1 := by rw [← e]; exact Dvd.dvd.mul_left h3 _
  omega

end Orthogenesis.CollatzChecks

#print axioms Orthogenesis.CollatzChecks.collatz_is_dm3_trivial
#print axioms Orthogenesis.CollatzChecks.skeleton_implication_is_the_conjecture
#print axioms Orthogenesis.CollatzChecks.log_ratios_telescope
#print axioms Orthogenesis.CollatzChecks.odd_contracting_multipliers
#print axioms Orthogenesis.CollatzChecks.odd_succ_not_mult_three
