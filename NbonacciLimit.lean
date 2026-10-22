-- GATE-DECLARE: sorries = none
-- GATE-REASON: new file 2026-10-22 for the geometry pin (Lean v4.32.0, Mathlib).
-- COMPILED by the author 2026-10-22 (Lean v4.32.0, Mathlib), including `exists_seq_tendsto_two`: no errors, no sorry, two `push_neg` deprecation warnings (lines 62, 83); axioms for all seven #print lines: propext, Classical.choice, Quot.sound.
/-
# NbonacciLimit.lean

Companion to `NbonacciLadder.lean`. That file bounds integer sequences by 2^n and says, in its own
header, that "that η_k is the root of x^k = x^{k-1} + … + 1, and that η_k → 2, are analytic
statements this file does not make." This file makes them.

## What is proved (once it compiles)

For the characteristic equation `x^k = x^(k-1) + … + x + 1`, written `IsNbonacciRoot k x`:

* `root_eq`       — any root satisfies `x^k * (2 - x) = 1`.
* `root_lt_two`   — any root `x > 1` has `x < 2`.
* `root_gt_three_halves` — for `k ≥ 2`, any root `x > 1` has `x > 3/2`.
* `gap_le`        — for `k ≥ 2`, any root `x > 1` has `2 - x ≤ (2/3)^k`.
* `root_exists`   — for `k ≥ 2` a root exists, with `3/2 < x < 2`.
* `tendsto_two`   — ANY sequence of roots `η k > 1` (k ≥ 2) converges to 2.

So each rung of the ladder is below 2, the rungs climb toward 2, and the gap is at most (2/3)^k.
The bound is a supremum that is never attained: no largest rung, but a least upper bound.

## The derivation (by hand)

Sum the geometric series: (x^k - 1)/(x - 1) = x^(k-1) + … + 1. The equation x^k = that sum becomes
x^k (x - 1) = x^k - 1, that is x^k (2 - x) = 1. Hence 2 - x = x^(-k) > 0.
For k ≥ 2 and x > 1, the sum is at least 1 + x > 2, so x^k > 2 and 2 - x < 1/2, so x > 3/2.
Then x^k ≥ (3/2)^k and 2 - x = 1/x^k ≤ (2/3)^k → 0.
Existence: f(x) = x^k (2 - x) - 1 has f(3/2) = (3/2)^k / 2 - 1 > 0 for k ≥ 2 (since (3/2)^2 = 9/4 > 2)
and f(2) = -1 < 0, so the intermediate value theorem gives a root in [3/2, 2], not at either end.

## What is NOT proved here

* Uniqueness of the root in (1, 2), and that the roots increase with k. Neither is needed for the limit:
  `tendsto_two` holds for every choice of roots greater than 1.
* Anything about physical systems realising the recurrence. That identification is chapter prose.
-/

import Mathlib

namespace NbonacciLimit

/-- The characteristic equation of the k-term recurrence: `x^k = x^(k-1) + … + x + 1`. -/
def IsNbonacciRoot (k : ℕ) (x : ℝ) : Prop := x ^ k = ∑ i ∈ Finset.range k, x ^ i

/-- `charFn k x = x^k (2 - x) - 1`; its roots in (1, 2) are exactly the n-bonacci constants. -/
def charFn (k : ℕ) (x : ℝ) : ℝ := x ^ k * (2 - x) - 1

theorem root_eq (k : ℕ) (x : ℝ) (h : IsNbonacciRoot k x) : x ^ k * (2 - x) = 1 := by
  have hg : (∑ i ∈ Finset.range k, x ^ i) * (x - 1) = x ^ k - 1 := geom_sum_mul x k
  have h' : x ^ k = ∑ i ∈ Finset.range k, x ^ i := h
  rw [← h'] at hg
  linear_combination (-1 : ℝ) * hg

theorem root_lt_two (k : ℕ) (x : ℝ) (hx : 1 < x) (h : IsNbonacciRoot k x) : x < 2 := by
  have h1 := root_eq k x h
  have hp : 0 < x ^ k := pow_pos (by linarith) k
  by_contra hc
  push_neg at hc
  nlinarith [mul_nonneg hp.le (sub_nonneg.mpr hc)]

theorem sum_ge (x : ℝ) (hx : 0 < x) : ∀ k : ℕ, 2 ≤ k → 1 + x ≤ ∑ i ∈ Finset.range k, x ^ i := by
  intro k hk
  induction k, hk using Nat.le_induction with
  | base => simp [Finset.sum_range_succ]
  | succ n hn ih =>
      rw [Finset.sum_range_succ]
      have : 0 < x ^ n := pow_pos hx n
      linarith

theorem root_gt_three_halves (k : ℕ) (hk : 2 ≤ k) (x : ℝ) (hx : 1 < x) (h : IsNbonacciRoot k x) :
    3 / 2 < x := by
  have h1 := root_eq k x h
  have hp : 0 < x ^ k := pow_pos (by linarith) k
  have hbig : 2 < x ^ k := by
    have h' : x ^ k = ∑ i ∈ Finset.range k, x ^ i := h
    have := sum_ge x (by linarith) k hk
    linarith
  by_contra hc
  push_neg at hc
  nlinarith [mul_nonneg hp.le (sub_nonneg.mpr hc)]

theorem three_halves_pow_le (x : ℝ) (hx : 3 / 2 ≤ x) : ∀ n : ℕ, (3 / 2 : ℝ) ^ n ≤ x ^ n
  | 0 => by simp
  | n + 1 => by
      have ih := three_halves_pow_le x hx n
      have h0 : (0 : ℝ) ≤ (3 / 2) ^ n := by positivity
      have hx0 : (0 : ℝ) ≤ x := by linarith
      rw [pow_succ, pow_succ]
      nlinarith [mul_nonneg (sub_nonneg.mpr ih) hx0, mul_nonneg h0 (sub_nonneg.mpr hx)]

theorem gap_le (k : ℕ) (hk : 2 ≤ k) (x : ℝ) (hx : 1 < x) (h : IsNbonacciRoot k x) :
    2 - x ≤ (2 / 3 : ℝ) ^ k := by
  have h1 := root_eq k x h
  have h32 := root_gt_three_halves k hk x hx h
  have hlt := root_lt_two k x hx h
  have hpow := three_halves_pow_le x h32.le k
  have hpos : (0 : ℝ) < (3 / 2) ^ k := by positivity
  have h2x : (0 : ℝ) ≤ 2 - x := by linarith
  have hmul : (2 - x) * (3 / 2 : ℝ) ^ k ≤ 1 := by
    nlinarith [mul_le_mul_of_nonneg_left hpow h2x]
  have hone : (2 / 3 : ℝ) ^ k * (3 / 2) ^ k = 1 := by
    rw [← mul_pow]; norm_num
  exact le_of_mul_le_mul_right (by rw [hone]; exact hmul) hpos

theorem nine_fourths_le (n : ℕ) (hn : 2 ≤ n) : (9 / 4 : ℝ) ≤ (3 / 2) ^ n := by
  induction n, hn using Nat.le_induction with
  | base => norm_num
  | succ m hm ih =>
      rw [pow_succ]
      nlinarith [ih]

theorem charFn_continuous (k : ℕ) : Continuous (charFn k) := by
  unfold charFn
  fun_prop

theorem root_exists (k : ℕ) (hk : 2 ≤ k) : ∃ x : ℝ, 3 / 2 < x ∧ x < 2 ∧ IsNbonacciRoot k x := by
  have hf2 : charFn k 2 = -1 := by simp [charFn]
  have hf32 : 0 < charFn k (3 / 2) := by
    unfold charFn
    nlinarith [nine_fourths_le k hk]
  have hmem : (0 : ℝ) ∈ Set.Icc (charFn k 2) (charFn k (3 / 2)) :=
    ⟨by rw [hf2]; norm_num, hf32.le⟩
  obtain ⟨c, hc, hfc⟩ :=
    intermediate_value_Icc' (by norm_num : (3 / 2 : ℝ) ≤ 2) (charFn_continuous k).continuousOn hmem
  have hfc' : c ^ k * (2 - c) = 1 := by
    unfold charFn at hfc
    linarith
  have hc2 : c < 2 := by
    rcases hc.2.lt_or_eq with h | h
    · exact h
    · exfalso
      rw [h] at hfc'
      norm_num at hfc'
  have hc32 : 3 / 2 < c := by
    rcases hc.1.lt_or_eq with h | h
    · exact h
    · exfalso
      have h94 := nine_fourths_le k hk
      rw [← h] at hfc'
      nlinarith [h94]
  refine ⟨c, hc32, hc2, ?_⟩
  have hg : (∑ i ∈ Finset.range k, c ^ i) * (c - 1) = c ^ k - 1 := geom_sum_mul c k
  have hne : c - 1 ≠ 0 := ne_of_gt (by linarith)
  have e : c ^ k * (c - 1) = c ^ k - 1 := by
    linear_combination (-1 : ℝ) * hfc'
  have hsum : (∑ i ∈ Finset.range k, c ^ i) = c ^ k := mul_right_cancel₀ hne (hg.trans e.symm)
  exact hsum.symm

theorem tendsto_two (η : ℕ → ℝ) (h : ∀ k, 2 ≤ k → 1 < η k ∧ IsNbonacciRoot k (η k)) :
    Filter.Tendsto η Filter.atTop (nhds 2) := by
  have hg : ∀ k, 2 ≤ k → ‖η k - 2‖ ≤ (2 / 3 : ℝ) ^ k := by
    intro k hk
    obtain ⟨h1, h2⟩ := h k hk
    have hlt := root_lt_two k (η k) h1 h2
    have hgap := gap_le k hk (η k) h1 h2
    rw [Real.norm_eq_abs, abs_sub_comm, abs_of_nonneg (by linarith)]
    exact hgap
  have hlim : Filter.Tendsto (fun k : ℕ => (2 / 3 : ℝ) ^ k) Filter.atTop (nhds 0) :=
    tendsto_pow_atTop_nhds_zero_of_lt_one (by norm_num) (by norm_num)
  have h0 : Filter.Tendsto (fun k => η k - 2) Filter.atTop (nhds 0) := by
    apply squeeze_zero_norm' _ hlim
    filter_upwards [Filter.eventually_ge_atTop 2] with k hk
    exact hg k hk
  have h2 := h0.add_const 2
  simpa using h2

/-- Non-vacuity: the hypothesis of `tendsto_two` is satisfiable. There is a sequence that, for every `k ≥ 2`, picks a root
of the k-th characteristic equation greater than 1 (by `root_exists`), and that sequence tends to 2. -/
theorem exists_seq_tendsto_two :
    ∃ η : ℕ → ℝ, (∀ k, 2 ≤ k → 1 < η k ∧ IsNbonacciRoot k (η k)) ∧ Filter.Tendsto η Filter.atTop (nhds 2) := by
  have key : ∀ k : ℕ, ∃ x : ℝ, 2 ≤ k → (3 / 2 < x ∧ x < 2 ∧ IsNbonacciRoot k x) := by
    intro k
    by_cases hk : 2 ≤ k
    · obtain ⟨x, hx⟩ := root_exists k hk
      exact ⟨x, fun _ => hx⟩
    · exact ⟨0, fun h => absurd h hk⟩
  choose η hη using key
  have h : ∀ k, 2 ≤ k → 1 < η k ∧ IsNbonacciRoot k (η k) := by
    intro k hk
    obtain ⟨h1, _, h3⟩ := hη k hk
    exact ⟨by linarith, h3⟩
  exact ⟨η, h, tendsto_two η h⟩

end NbonacciLimit

#print axioms NbonacciLimit.root_eq
#print axioms NbonacciLimit.root_lt_two
#print axioms NbonacciLimit.root_gt_three_halves
#print axioms NbonacciLimit.gap_le
#print axioms NbonacciLimit.root_exists
#print axioms NbonacciLimit.tendsto_two
#print axioms NbonacciLimit.exists_seq_tendsto_two
