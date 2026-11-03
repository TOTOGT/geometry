/-
Volume XVIII — chapter 7 (planned): sequences and series. Lean core.

STATUS: compiled clean by the author, no sorryAx (report: series.axioms.txt). It was first written
without a toolchain and fixed against the real compiler output. To rerun:
  lake env lean book18/Series.lean

What it states, in the textbook's own epsilon-N form (not as a Mathlib `Tendsto`, so the
statement can be read against the book):

  ConvergesTo s L          :  forall e > 0, exists N, forall n >= N, |s n - L| < e
  partialSum a n           :  a 0 + ... + a (n-1)

  §0  convergesTo_iff        the definition above agrees with Mathlib's Tendsto. This is the
                             fidelity check: it says the definition means what it should.
  §1  geom_partial_sum       r^0 + ... + r^(n-1) = (r^n - 1)/(r - 1) for r != 1
      geom_series_converges  |r| < 1  =>  the partial sums converge to 1/(1 - r)
  §2  bounded_monotone_converges
                             a monotone sequence bounded above converges
  §3  nonneg_series_bounded_converges
                             nonnegative terms with bounded partial sums: the series converges
  §4  comparison_test        0 <= a n <= b n and the b-partial-sums bounded => a converges
  §5  controls               (i) the bound hypothesis in §3 can fail (constant 1);
                             (ii) the geometric theorem gives 2 for r = 1/2.

Not here yet: ratio test, alternating series test, power series, Taylor. Each needs its own
statement read against the textbook before it is trusted.

Reminder of the project rule: compiling is not the same as proving what it says. Read §0 and
the statements, not the names.

Toolchain: repository pin, leanprover/lean4:v4.32.0 with Mathlib v4.32.0.
-/
import Mathlib

namespace Book18Series

open Filter Topology

/-- The textbook definition: s n gets and stays within e of L. -/
def ConvergesTo (s : ℕ → ℝ) (L : ℝ) : Prop :=
  ∀ ε > 0, ∃ N : ℕ, ∀ n ≥ N, |s n - L| < ε

/-- The n-th partial sum a 0 + ... + a (n-1). -/
def partialSum (a : ℕ → ℝ) : ℕ → ℝ := fun n => ∑ i ∈ Finset.range n, a i

/-- §0. The epsilon-N definition is Mathlib's `Tendsto`. -/
theorem convergesTo_iff (s : ℕ → ℝ) (L : ℝ) :
    ConvergesTo s L ↔ Tendsto s atTop (𝓝 L) := by
  rw [Metric.tendsto_atTop]
  simp only [ConvergesTo, Real.dist_eq]

/-- §1. The finite geometric sum. -/
theorem geom_partial_sum (r : ℝ) (hr : r ≠ 1) (n : ℕ) :
    partialSum (fun i => r ^ i) n = (r ^ n - 1) / (r - 1) := by
  simp only [partialSum]
  exact geom_sum_eq hr n

/-- §1. The geometric series converges to 1/(1 - r) when |r| < 1. -/
theorem geom_series_converges (r : ℝ) (hr : |r| < 1) :
    ConvergesTo (partialSum (fun i => r ^ i)) (1 / (1 - r)) := by
  rw [convergesTo_iff]
  have h := (hasSum_geometric_of_abs_lt_one hr).tendsto_sum_nat
  rw [one_div]
  exact h

/-- §2. Monotone and bounded above implies convergent. -/
theorem bounded_monotone_converges (s : ℕ → ℝ) (hm : Monotone s)
    (hb : ∃ M, ∀ n, s n ≤ M) : ∃ L, ConvergesTo s L := by
  obtain ⟨M, hM⟩ := hb
  refine ⟨⨆ n, s n, ?_⟩
  rw [convergesTo_iff]
  exact tendsto_atTop_ciSup hm ⟨M, by rintro _ ⟨n, rfl⟩; exact hM n⟩

/-- §3. Nonnegative terms, partial sums bounded: the series converges. -/
theorem nonneg_series_bounded_converges (a : ℕ → ℝ) (ha : ∀ n, 0 ≤ a n)
    (hb : ∃ M, ∀ n, partialSum a n ≤ M) : ∃ L, ConvergesTo (partialSum a) L := by
  refine bounded_monotone_converges (partialSum a) ?_ hb
  apply monotone_nat_of_le_succ
  intro n
  simp only [partialSum, Finset.sum_range_succ]
  linarith [ha n]

/-- §4. The comparison test. -/
theorem comparison_test (a b : ℕ → ℝ) (ha : ∀ n, 0 ≤ a n) (hab : ∀ n, a n ≤ b n)
    (hb : ∃ M, ∀ n, partialSum b n ≤ M) : ∃ L, ConvergesTo (partialSum a) L := by
  obtain ⟨M, hM⟩ := hb
  refine nonneg_series_bounded_converges a ha ⟨M, fun n => ?_⟩
  calc partialSum a n ≤ partialSum b n := by
        simp only [partialSum]
        exact Finset.sum_le_sum (fun i _ => hab i)
    _ ≤ M := hM n

/-- §5 control (i). The boundedness hypothesis is not automatic: the partial sums of the
constant sequence 1 are unbounded, so §3 does not apply to it. -/
theorem control_constant_unbounded : ¬ ∃ M : ℝ, ∀ n, partialSum (fun _ => (1 : ℝ)) n ≤ M := by
  rintro ⟨M, hM⟩
  obtain ⟨n, hn⟩ := exists_nat_gt M
  have h := hM n
  simp only [partialSum, Finset.sum_const, Finset.card_range, nsmul_eq_mul, mul_one] at h
  linarith

/-- §5 control (ii). With r = 1/2 the theorem's limit is 2. -/
theorem control_half_geometric : ConvergesTo (partialSum (fun i => (1 / 2 : ℝ) ^ i)) 2 := by
  have h := geom_series_converges (1 / 2 : ℝ) (by norm_num [abs_of_pos])
  have e : (1 : ℝ) / (1 - 1 / 2) = 2 := by norm_num
  rw [e] at h
  exact h

#print axioms convergesTo_iff
#print axioms geom_partial_sum
#print axioms geom_series_converges
#print axioms bounded_monotone_converges
#print axioms nonneg_series_bounded_converges
#print axioms comparison_test
#print axioms control_constant_unbounded
#print axioms control_half_geometric

end Book18Series
