-- GATE-DECLARE: sorries = none
-- GATE-REASON: new file 2026-09-29 for the geometry pin (Lean v4.32.0, Mathlib v4.32.0).
-- UNTESTED until the author runs `lake build` on it.
/-
# EtaChecks.lean — Book 3, Chapter η (ch-eta-dnls.html)

  Builds on `Orthogenesis.Tribonacci` (Hawking/TribonacciLog.lean), which defines η
  by its cubic and brackets it. This file checks what Chapter η says about η.

  §1  What the page's Lean block SHOULD have said. It prints
        `⟨1.839287, by norm_num, by native_decide, ...⟩`
      as the proof that η exists with tribPoly.eval η = 0. 1.839287 is a six-place
      decimal, not a root (its residual in x³−x²−x−1 is +1.34×10⁻⁶), so that
      conjunct is false at that witness, and `native_decide` would in any case add
      `Lean.ofReduceBool` to the axiom list, against the page's "no axioms beyond
      Mathlib". The real file, AXLE/TribonacciMeasure.lean, does not do this (it
      defines η by `Classical.choose`). Proved here, from the cubic alone: η exists,
      η > 1, and (η⁻¹)ᵏ is strictly decreasing.
  §2  The page's §η.3 arithmetic is right, and it defeats the page's headline. For
      V(q) = q³ − c·q, q = 1 is critical iff c = 3, non-degenerate (V″(1) = 6),
      V(1) = −2, and V + 2 = (q−1)²(q+2). All proved. But η ≠ 3 (η < 1.83929), so at
      c = η the point q = 1 is NOT critical. "The only n-bonacci root that sits
      exactly at c* = 3" is false as a statement about values: the only thing equal
      to 3 is the NUMBER OF TERMS, n = 3.
  §3  No n-bonacci root reaches 3, or 2: every root above 1 of xⁿ = Σ_{k<n} xᵏ is
      below 2. The ladder converges to 2 from below and no rung is at the fold.
  §4  "The two 26s": D_crit(13) = 2·(13−1)+2 is 2·13 for every argument, so the
      second 26 is the number 13 doubled; and trib(7) = 13 under the A000073
      indexing the page must be using (stated here, since it is convention-bound).
  §5  T₃ has determinant 1, and (η², η, 1) is an eigenvector with eigenvalue η iff
      η is Tribonacci. Its membership in SL(3,ℤ) is a fact about integer matrices;
      Sp(2g,ℤ) lives on ℤ^{2g}, so a 3×3 matrix is not in any of them.

  NOT formalised, and not claimed: anything about the DNLS chain, the IPR, "four
  times more robust", or the self-trapping thresholds. The DNLS result is
  numerical. Nothing in this file, or in AXLE/TribonacciMeasure.lean, is a
  statement about a chain, so η⁻ᵏ contracting is not a "load-bearing lemma" for it.
-/

import Mathlib
import Orthogenesis.Hawking.TribonacciLog

namespace Orthogenesis.EtaChecks

open Orthogenesis.Tribonacci

/-! ## §1 η exists and its weights contract -/

theorem eta_inv_pow_strictAnti {η : ℝ} (h : IsTribonacci η) :
    StrictAnti (fun k : ℕ => (η⁻¹) ^ k) := by
  have hpos : 0 < η := tribonacci_pos h
  obtain ⟨h1, _⟩ := h
  have ha : 0 < η⁻¹ := inv_pos.mpr hpos
  have hmul : η⁻¹ * η = 1 := inv_mul_cancel₀ hpos.ne'
  have hlt : η⁻¹ < 1 := by nlinarith [mul_pos ha (sub_pos.mpr h1)]
  apply strictAnti_nat_of_succ_lt
  intro k
  show (η⁻¹) ^ (k + 1) < (η⁻¹) ^ k
  have hk : 0 < (η⁻¹) ^ k := pow_pos ha k
  have hp := mul_pos hk (sub_pos.mpr hlt)
  rw [pow_succ]
  nlinarith [hp]

/-- The statement the page's `eta_gt_one` block was meant to prove, with a real
    witness: η exists, η > 1, η is a root of x³−x²−x−1, the weights contract. -/
theorem eta_exists_and_contracts :
    ∃ η : ℝ, 1 < η ∧ η ^ 3 = η ^ 2 + η + 1 ∧
      StrictAnti (fun k : ℕ => (η⁻¹) ^ k) := by
  obtain ⟨η, hη⟩ := isTribonacci_nonvacuous
  have h := hη
  obtain ⟨h1, h2⟩ := h
  exact ⟨η, h1, h2, eta_inv_pow_strictAnti hη⟩

/-- 1.839287 is not a root, so the page's literal witness cannot satisfy its own
    conjunct. (Residual +1.339…×10⁻⁶ > 0.) -/
theorem page_witness_not_a_root : (1.839287 : ℝ) ^ 3 - 1.839287 ^ 2 - 1.839287 - 1 ≠ 0 := by
  norm_num

/-! ## §2 The fold at c* = 3, and why η is not at it -/

theorem V_at_one : (1 : ℝ) ^ 3 - 3 * 1 = -2 := by norm_num

theorem V_shift_double_root (q : ℝ) : q ^ 3 - 3 * q + 2 = (q - 1) ^ 2 * (q + 2) := by ring

theorem V_hasDerivAt (c q : ℝ) :
    HasDerivAt (fun q : ℝ => q ^ 3 - c * q) (3 * q ^ 2 - c) q := by
  have h := (hasDerivAt_pow 3 q).sub ((hasDerivAt_id' q).const_mul c)
  refine h.congr_deriv ?_
  norm_num

theorem V_critical_at_one_iff (c : ℝ) : 3 * (1 : ℝ) ^ 2 - c = 0 ↔ c = 3 := by
  constructor <;> intro h <;> linarith

theorem V_nondegenerate : (6 : ℝ) * 1 ≠ 0 := by norm_num

theorem eta_ne_three {η : ℝ} (h : IsTribonacci η) : η ≠ 3 := by
  have hl := tribonacci_lt h
  intro h3
  rw [h3] at hl
  norm_num at hl

/-- At c = η the point q = 1 is NOT a critical point of q³ − c·q. -/
theorem not_critical_at_eta {η : ℝ} (h : IsTribonacci η) :
    3 * (1 : ℝ) ^ 2 - η ≠ 0 := fun h0 =>
  eta_ne_three h ((V_critical_at_one_iff η).mp h0)

/-! ## §3 No n-bonacci root reaches 2, let alone 3 -/

theorem nbonacci_three_iff (x : ℝ) :
    x ^ 3 = ∑ k ∈ Finset.range 3, x ^ k ↔ x ^ 3 = x ^ 2 + x + 1 := by
  simp only [Finset.sum_range_succ, Finset.sum_range_zero, pow_zero, pow_one, zero_add]
  constructor <;> intro h <;> linarith

theorem nbonacci_root_lt_two {n : ℕ} {x : ℝ} (hx : 1 < x)
    (h : x ^ n = ∑ k ∈ Finset.range n, x ^ k) : x < 2 := by
  have hg := geom_sum_mul x n
  rw [← h] at hg
  have hpos : 0 < x ^ n := pow_pos (by linarith) n
  by_contra hge
  push Not at hge
  nlinarith [hpos, hg, hge]

/-! ## §4 The two 26s -/

/-- The page's D_crit(n) = 2(n−1)+2 is 2n. -/
theorem dcrit_eq_two_mul (n : ℝ) : 2 * (n - 1) + 2 = 2 * n := by ring

theorem dcrit_thirteen : 2 * ((13 : ℝ) - 1) + 2 = 26 := by norm_num

/-- Tribonacci numbers, OEIS A000073 indexing: 0, 0, 1, 1, 2, 4, 7, 13, ... -/
def trib : ℕ → ℕ
  | 0 => 0
  | 1 => 0
  | 2 => 1
  | n + 3 => trib (n + 2) + trib (n + 1) + trib n

theorem trib_seven : trib 7 = 13 := by decide

/-- Under the OTHER common indexing (1, 1, 2, 4, 7, 13, ...) 13 sits at position 6,
    not 7, so "trib(7) = 13" is convention-bound and the page should say which. -/
theorem trib_six : trib 6 = 7 := by decide

/-! ## §5 The companion matrix -/

def T3 : Matrix (Fin 3) (Fin 3) ℝ := !![1, 1, 1; 1, 0, 0; 0, 1, 0]

theorem T3_det : T3.det = 1 := by
  simp [T3, Matrix.det_fin_three]

theorem T3_eigen_iff (η : ℝ) :
    T3.mulVec ![η ^ 2, η, 1] = η • ![η ^ 2, η, 1] ↔ η ^ 3 = η ^ 2 + η + 1 := by
  constructor
  · intro h
    have h0 := congrFun h 0
    simp [T3, Matrix.mulVec, dotProduct, Fin.sum_univ_three] at h0
    nlinarith [h0]
  · intro h
    funext i
    fin_cases i <;> simp [T3, Matrix.mulVec, dotProduct, Fin.sum_univ_three] <;>
      nlinarith [h]

end Orthogenesis.EtaChecks

/-! ## Axiom probe -/
#print axioms Orthogenesis.EtaChecks.eta_inv_pow_strictAnti
#print axioms Orthogenesis.EtaChecks.eta_exists_and_contracts
#print axioms Orthogenesis.EtaChecks.page_witness_not_a_root
#print axioms Orthogenesis.EtaChecks.V_hasDerivAt
#print axioms Orthogenesis.EtaChecks.V_critical_at_one_iff
#print axioms Orthogenesis.EtaChecks.eta_ne_three
#print axioms Orthogenesis.EtaChecks.not_critical_at_eta
#print axioms Orthogenesis.EtaChecks.nbonacci_three_iff
#print axioms Orthogenesis.EtaChecks.nbonacci_root_lt_two
#print axioms Orthogenesis.EtaChecks.dcrit_eq_two_mul
#print axioms Orthogenesis.EtaChecks.trib_seven
#print axioms Orthogenesis.EtaChecks.T3_det
#print axioms Orthogenesis.EtaChecks.T3_eigen_iff
