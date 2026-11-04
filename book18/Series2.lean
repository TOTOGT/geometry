import Mathlib

/-
Volume XVIII — chapter 7, second Lean file: the ratio test, the alternating series test, Abel's lemma.

STATUS: UNTESTED. Written without a Lean toolchain; not compiled by anyone. Until the author runs it
and saves the output as series2.axioms.txt, nothing in this file counts as checked. To run:
  lake env lean book18/Series2.lean 2>&1 | tee book18/series2.axioms.txt

Series.lean is compiled and is not touched. This file is standalone: it re-declares ConvergesTo and
partialSum (same definitions, its own namespace Book18Series2) so that nothing in Series.lean changes.

What it states, in the textbook's epsilon-N form:
  convergesTo_iff             the definition agrees with Mathlib's Tendsto (fidelity check, as in Series.lean)
  dominated_by_geometric      |a n| <= C r^n, 0 < r < 1  =>  the series of |a n| and the series of a n converge
  terms_tend_to_zero          the partial sums converge  =>  the terms tend to 0
  ratio_test_converges        a n never 0, |a(n+1)|/|a n| -> L, L < 1  =>  absolute and ordinary convergence
  ratio_test_diverges         the same ratio, L > 1  =>  the series does not converge
  alternating_series_test     b antitone, b -> 0  =>  the series of (-1)^n b n converges
  control_alternating_needs_limit_zero
                              b = 1 is antitone, and the series of (-1)^n does NOT converge: "b -> 0" is used
  power_series_abel           |a n x0^n| <= M for all n and |x| < |x0|  =>  the series of a n x^n converges
  exp_series_converges_of_ne_zero
                              for x != 0 the series of x^n / n! converges (ratio test with ratio |x|/(n+1))

WHAT THESE PROOFS ARE. dominated_by_geometric, alternating_series_test and the convergence half of
the others lean on Mathlib (Summable, HasSum, Antitone.tendsto_alternating_series_of_tendsto_zero).
This file checks that the textbook statements are true as formal sentences. It does not reproduce a
textbook's own proof of the ratio test line for line.

WHAT IT DOES NOT STATE.
  - The root test, the radius of convergence as a definition, Taylor's theorem.
  - The cases L = 1 in the ratio test (inconclusive; the page shows harmonic and 1/(n+1)^2 by script).
  - Conditional convergence results beyond the alternating series test.

NAMES MOST LIKELY TO NEED A FIX AGAINST THE REAL COMPILER (flagged in advance, not known to fail):
  Summable.of_nonneg_of_le, summable_geometric_of_lt_one, Summable.of_norm, HasSum.tendsto_sum_nat,
  tendsto_add_atTop_nat, div_lt_iff₀, div_le_iff₀, one_lt_div, div_lt_one, pow_le_pow_left₀,
  tendsto_const_div_atTop_nhds_zero_nat, Antitone.tendsto_alternating_series_of_tendsto_zero,
  the final `field_simp` steps, and `simp` closing the control.

Toolchain: repository pin, leanprover/lean4:v4.32.0 with Mathlib v4.32.0.
-/

namespace Book18Series2

open Filter Topology

/-- The textbook definition: s n gets and stays within e of L. -/
def ConvergesTo (s : ℕ → ℝ) (L : ℝ) : Prop :=
  ∀ ε > 0, ∃ N : ℕ, ∀ n ≥ N, |s n - L| < ε

/-- The n-th partial sum a 0 + ... + a (n-1). -/
def partialSum (a : ℕ → ℝ) : ℕ → ℝ := fun n => ∑ i ∈ Finset.range n, a i

/-- The epsilon-N definition is Mathlib's `Tendsto`. -/
theorem convergesTo_iff (s : ℕ → ℝ) (L : ℝ) :
    ConvergesTo s L ↔ Tendsto s atTop (𝓝 L) := by
  rw [Metric.tendsto_atTop]
  simp only [ConvergesTo, Real.dist_eq]

/-- A series dominated by a convergent geometric series converges, absolutely and ordinarily. -/
theorem dominated_by_geometric (a : ℕ → ℝ) (C r : ℝ) (hr0 : 0 < r) (hr1 : r < 1)
    (h : ∀ n, |a n| ≤ C * r ^ n) :
    (∃ S, ConvergesTo (partialSum (fun n => |a n|)) S) ∧ (∃ T, ConvergesTo (partialSum a) T) := by
  have hs : Summable (fun n => |a n|) :=
    Summable.of_nonneg_of_le (fun n => abs_nonneg _) h
      ((summable_geometric_of_lt_one hr0.le hr1).mul_left C)
  have hs' : Summable a := Summable.of_norm (by simpa [Real.norm_eq_abs] using hs)
  refine ⟨⟨_, (convergesTo_iff _ _).2 hs.hasSum.tendsto_sum_nat⟩,
    ⟨_, (convergesTo_iff _ _).2 hs'.hasSum.tendsto_sum_nat⟩⟩

/-- If the partial sums converge, the terms tend to 0. -/
theorem terms_tend_to_zero (a : ℕ → ℝ) (T : ℝ) (h : ConvergesTo (partialSum a) T) :
    ConvergesTo a 0 := by
  rw [convergesTo_iff] at h ⊢
  have h1 : Tendsto (fun n => partialSum a (n + 1)) atTop (𝓝 T) :=
    h.comp (tendsto_add_atTop_nat 1)
  have h2 := h1.sub h
  rw [sub_self] at h2
  refine h2.congr (fun n => ?_)
  simp [partialSum, Finset.sum_range_succ]

/-- Ratio test, convergence half: ratios tend to L < 1. -/
theorem ratio_test_converges (a : ℕ → ℝ) (L : ℝ) (hne : ∀ n, a n ≠ 0)
    (hL : ConvergesTo (fun n => |a (n + 1)| / |a n|) L) (hlt : L < 1) :
    (∃ S, ConvergesTo (partialSum (fun n => |a n|)) S) ∧ (∃ T, ConvergesTo (partialSum a) T) := by
  obtain ⟨r, hr0, hr1, hLr⟩ : ∃ r : ℝ, 0 < r ∧ r < 1 ∧ L < r :=
    ⟨max ((L + 1) / 2) (1 / 2), lt_max_of_lt_right (by norm_num),
      max_lt (by linarith) (by norm_num), lt_max_of_lt_left (by linarith)⟩
  obtain ⟨N, hN⟩ := hL (r - L) (by linarith)
  have hrat : ∀ n ≥ N, |a (n + 1)| < r * |a n| := by
    intro n hn
    have h3 : |a (n + 1)| / |a n| - L < r - L := (abs_lt.1 (hN n hn)).2
    have h4 : |a (n + 1)| / |a n| < r := by linarith
    have := (div_lt_iff₀ (abs_pos.2 (hne n))).1 h4
    linarith
  have hk : ∀ k : ℕ, |a (N + k)| ≤ |a N| * r ^ k := by
    intro k
    induction k with
    | zero => simp
    | succ k ih =>
      have h5 := hrat (N + k) (by omega)
      calc |a (N + (k + 1))| = |a (N + k + 1)| := rfl
        _ ≤ r * |a (N + k)| := h5.le
        _ ≤ r * (|a N| * r ^ k) := mul_le_mul_of_nonneg_left ih hr0.le
        _ = |a N| * r ^ (k + 1) := by ring
  obtain ⟨C, hC, hCN⟩ : ∃ C : ℝ, (∀ n ≤ N, |a n| / r ^ n ≤ C) ∧ |a N| / r ^ N ≤ C := by
    have hsum : ∀ n ≤ N, |a n| / r ^ n ≤ ∑ i ∈ Finset.range (N + 1), |a i| / r ^ i := by
      intro n hn
      exact Finset.single_le_sum (f := fun i => |a i| / r ^ i)
        (fun i _ => div_nonneg (abs_nonneg _) (pow_pos hr0 i).le)
        (Finset.mem_range.2 (by omega))
    exact ⟨_, hsum, hsum N le_rfl⟩
  have hbound : ∀ n, |a n| ≤ C * r ^ n := by
    intro n
    by_cases hn : n ≤ N
    · have hmem := hC n hn
      rw [div_le_iff₀ (pow_pos hr0 n)] at hmem
      exact hmem
    · obtain ⟨k, rfl⟩ : ∃ k, n = N + k := ⟨n - N, by omega⟩
      have hr0' : r ≠ 0 := hr0.ne'
      have e : |a N| * r ^ k = (|a N| / r ^ N) * r ^ (N + k) := by
        rw [pow_add]
        field_simp
      calc |a (N + k)| ≤ |a N| * r ^ k := hk k
        _ = (|a N| / r ^ N) * r ^ (N + k) := e
        _ ≤ C * r ^ (N + k) := mul_le_mul_of_nonneg_right hCN (pow_pos hr0 _).le
  exact dominated_by_geometric a C r hr0 hr1 hbound

/-- Ratio test, divergence half: ratios tend to L > 1. -/
theorem ratio_test_diverges (a : ℕ → ℝ) (L : ℝ) (hne : ∀ n, a n ≠ 0)
    (hL : ConvergesTo (fun n => |a (n + 1)| / |a n|) L) (hgt : 1 < L) :
    ¬ ∃ T, ConvergesTo (partialSum a) T := by
  rintro ⟨T, hT⟩
  obtain ⟨N, hN⟩ := hL (L - 1) (by linarith)
  have hstep : ∀ n ≥ N, |a n| < |a (n + 1)| := by
    intro n hn
    have h3 : -(L - 1) < |a (n + 1)| / |a n| - L := (abs_lt.1 (hN n hn)).1
    have h4 : 1 < |a (n + 1)| / |a n| := by linarith
    exact (one_lt_div (abs_pos.2 (hne n))).1 h4
  have hmono : ∀ k : ℕ, |a N| ≤ |a (N + k)| := by
    intro k
    induction k with
    | zero => simp
    | succ k ih => exact ih.trans (hstep (N + k) (by omega)).le
  have h0 := terms_tend_to_zero a T hT
  obtain ⟨M, hM⟩ := h0 (|a N|) (abs_pos.2 (hne N))
  have h6 := hM (max N M) (le_max_right _ _)
  have h5 := hmono (max N M - N)
  rw [show N + (max N M - N) = max N M by omega] at h5
  rw [sub_zero] at h6
  linarith

/-- Alternating series test. -/
theorem alternating_series_test (b : ℕ → ℝ) (hanti : Antitone b) (hb0 : ConvergesTo b 0) :
    ∃ T, ConvergesTo (partialSum (fun n => (-1) ^ n * b n)) T := by
  obtain ⟨l, hl⟩ := hanti.tendsto_alternating_series_of_tendsto_zero ((convergesTo_iff _ _).1 hb0)
  exact ⟨l, (convergesTo_iff _ _).2 hl⟩

/-- Control: "b tends to 0" is used. b = 1 is antitone, yet the series of (-1)^n does not converge. -/
theorem control_alternating_needs_limit_zero :
    Antitone (fun _ : ℕ => (1 : ℝ)) ∧
      ¬ ∃ T, ConvergesTo (partialSum (fun n => (-1 : ℝ) ^ n * 1)) T := by
  refine ⟨antitone_const, ?_⟩
  rintro ⟨T, hT⟩
  obtain ⟨N, hN⟩ := terms_tend_to_zero _ T hT 1 one_pos
  have h := hN N le_rfl
  simp at h

/-- Abel's lemma: bounded at x0 implies convergent for every |x| < |x0|. -/
theorem power_series_abel (a : ℕ → ℝ) (x0 x M : ℝ) (hM : ∀ n, |a n * x0 ^ n| ≤ M)
    (hx : |x| < |x0|) : ∃ T, ConvergesTo (partialSum (fun n => a n * x ^ n)) T := by
  have hx0 : x0 ≠ 0 := by
    intro h
    rw [h, abs_zero] at hx
    exact absurd hx (not_lt.2 (abs_nonneg x))
  have hq0 : 0 ≤ |x| / |x0| := div_nonneg (abs_nonneg _) (abs_nonneg _)
  have hq1 : |x| / |x0| < 1 := (div_lt_one (abs_pos.2 hx0)).2 hx
  obtain ⟨r, hqr, hr0, hr1⟩ : ∃ r : ℝ, |x| / |x0| ≤ r ∧ 0 < r ∧ r < 1 :=
    ⟨max (|x| / |x0|) (1 / 2), le_max_left _ _, lt_max_of_lt_right (by norm_num),
      max_lt hq1 (by norm_num)⟩
  have hdom : ∀ n, |a n * x ^ n| ≤ M * r ^ n := by
    intro n
    have e : |a n * x ^ n| = |a n * x0 ^ n| * (|x| / |x0|) ^ n := by
      rw [abs_mul, abs_mul, abs_pow, abs_pow, div_pow]
      have : |x0| ^ n ≠ 0 := pow_ne_zero n (abs_ne_zero.2 hx0)
      field_simp
    rw [e]
    exact mul_le_mul (hM n) (pow_le_pow_left₀ hq0 hqr n) (pow_nonneg hq0 n)
      ((abs_nonneg _).trans (hM n))
  exact (dominated_by_geometric _ M r hr0 hr1 hdom).2

/-- The exponential series converges for x != 0: ratio |x|/(n+1) tends to 0. -/
theorem exp_series_converges_of_ne_zero (x : ℝ) (hx : x ≠ 0) :
    ∃ T, ConvergesTo (partialSum (fun n : ℕ => x ^ n / (n.factorial : ℝ))) T := by
  have hne : ∀ n : ℕ, x ^ n / (n.factorial : ℝ) ≠ 0 := fun n =>
    div_ne_zero (pow_ne_zero n hx) (Nat.cast_ne_zero.2 (Nat.factorial_ne_zero n))
  have hlim : Tendsto (fun n : ℕ => |x| / ((n : ℝ) + 1)) atTop (𝓝 0) := by
    have h := (tendsto_const_div_atTop_nhds_zero_nat |x|).comp (tendsto_add_atTop_nat 1)
    refine h.congr (fun n => ?_)
    simp
  have hratio : ∀ n : ℕ, |x ^ (n + 1) / ((n + 1).factorial : ℝ)| / |x ^ n / (n.factorial : ℝ)|
      = |x| / ((n : ℝ) + 1) := by
    intro n
    have hx' : |x| ≠ 0 := abs_ne_zero.2 hx
    have hf : (n.factorial : ℝ) ≠ 0 := Nat.cast_ne_zero.2 (Nat.factorial_ne_zero n)
    have hn1 : ((n : ℝ) + 1) ≠ 0 := by positivity
    rw [abs_div, abs_div, abs_pow, abs_pow, Nat.factorial_succ]
    simp only [Nat.cast_mul, Nat.cast_add, Nat.cast_one, Nat.abs_cast]
    field_simp
  have hL : ConvergesTo (fun n : ℕ => |x ^ (n + 1) / ((n + 1).factorial : ℝ)| /
      |x ^ n / (n.factorial : ℝ)|) 0 :=
    (convergesTo_iff _ _).2 (hlim.congr (fun n => (hratio n).symm))
  exact (ratio_test_converges (fun n : ℕ => x ^ n / (n.factorial : ℝ)) 0 hne hL
    (by norm_num)).2

#print axioms dominated_by_geometric
#print axioms terms_tend_to_zero
#print axioms ratio_test_converges
#print axioms ratio_test_diverges
#print axioms alternating_series_test
#print axioms control_alternating_needs_limit_zero
#print axioms power_series_abel
#print axioms exp_series_converges_of_ne_zero

end Book18Series2
