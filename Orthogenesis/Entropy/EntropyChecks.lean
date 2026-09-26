-- GATE-DECLARE: sorries = none
-- GATE-REASON: ch15 entropy — merging outcomes cannot raise entropy, binary Gibbs inequality, genome and V(D)J arithmetic checked.
/-
Orthogenesis/Entropy/EntropyChecks.lean — Book 3, ch15 (H — Entropy and the Compression Circle).

  §1  Merging two outcomes never raises entropy: p log p + q log q ≤ (p+q) log (p+q) for p, q ≥ 0.
      This is the step behind "a deterministic compression C gives H(C(X)) ≤ H(X)".
  §2  Binary Gibbs inequality: D_KL(P‖Q) ≥ 0 for two-outcome distributions — a paper's
      divergence from the field's prior is never negative.
  §3  Genome arithmetic: 6×10⁹ bp × 1.9 bits / 8 = 1.425×10⁹ bytes; the chapter's "~750 MB"
      is the haploid 3×10⁹ bp figure (7.125×10⁸ bytes).
  §4  V(D)J: 2^49 < 10^15 < 2^50, so log₂(10¹⁵) is just under 50 bits — the maximum, reached
      only if every sequence were equally likely.
-/
import Mathlib

namespace Orthogenesis.EntropyChecks

open Real

/-! ## §1  Merging outcomes cannot raise entropy -/

lemma mul_log_le_mul_log_add {p q : ℝ} (hp : 0 ≤ p) (hq : 0 ≤ q) :
    p * log p ≤ p * log (p + q) := by
  rcases eq_or_lt_of_le hp with h | h
  · subst h; simp
  · exact mul_le_mul_of_nonneg_left (log_le_log h (by linarith)) hp

theorem merge_no_entropy_gain {p q : ℝ} (hp : 0 ≤ p) (hq : 0 ≤ q) :
    p * log p + q * log q ≤ (p + q) * log (p + q) := by
  have h1 := mul_log_le_mul_log_add hp hq
  have h2 := mul_log_le_mul_log_add hq hp
  rw [add_comm q p] at h2
  calc p * log p + q * log q ≤ p * log (p + q) + q * log (p + q) := add_le_add h1 h2
    _ = (p + q) * log (p + q) := by ring

/-! ## §2  Binary Gibbs inequality -/

theorem kl_binary_nonneg {p q : ℝ} (hp : 0 < p) (hp1 : p < 1) (hq : 0 < q) (hq1 : q < 1) :
    0 ≤ p * log (p / q) + (1 - p) * log ((1 - p) / (1 - q)) := by
  have hp' : 0 < 1 - p := by linarith
  have hq' : 0 < 1 - q := by linarith
  have e1 : log (p / q) = - log (q / p) := by rw [← log_inv, inv_div]
  have e2 : log ((1 - p) / (1 - q)) = - log ((1 - q) / (1 - p)) := by rw [← log_inv, inv_div]
  have h1 : p * log (q / p) ≤ q - p := by
    have := mul_le_mul_of_nonneg_left (log_le_sub_one_of_pos (div_pos hq hp)) hp.le
    rw [mul_sub, mul_div_cancel₀ q hp.ne', mul_one] at this
    exact this
  have h2 : (1 - p) * log ((1 - q) / (1 - p)) ≤ (1 - q) - (1 - p) := by
    have := mul_le_mul_of_nonneg_left (log_le_sub_one_of_pos (div_pos hq' hp')) hp'.le
    rw [mul_sub, mul_div_cancel₀ (1 - q) hp'.ne', mul_one] at this
    exact this
  rw [e1, e2, mul_neg, mul_neg]
  linarith

/-! ## §3  Genome arithmetic -/

theorem genome_bytes :
    (6 * 10 ^ 9 * (19 / 10) / 8 : ℝ) = 1425 * 10 ^ 6 ∧
    (3 * 10 ^ 9 * (19 / 10) / 8 : ℝ) = 7125 * 10 ^ 5 := by
  constructor <;> norm_num

/-! ## §4  V(D)J repertoire bound -/

theorem vdj_bits : (2 : ℕ) ^ 49 < 10 ^ 15 ∧ (10 : ℕ) ^ 15 < 2 ^ 50 := by
  constructor <;> norm_num

end Orthogenesis.EntropyChecks

#print axioms Orthogenesis.EntropyChecks.merge_no_entropy_gain
#print axioms Orthogenesis.EntropyChecks.kl_binary_nonneg
#print axioms Orthogenesis.EntropyChecks.genome_bytes
#print axioms Orthogenesis.EntropyChecks.vdj_bits
