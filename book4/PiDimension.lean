import Mathlib

/-!
# PiDimension — the algebra behind book4/pi.html (Chapter 3½)

STATUS: compiled by the author on Lean v4.32.0 with Mathlib, no errors and no sorry (2026-10-30).
`#print axioms` on moran, ratio_lt_half, box_count and box_count_pi: propext, Classical.choice,
Quot.sound. (An earlier run failed in `box_count` at a `rw`; that step was rewritten.)

Transcendence of π plays no role. The construction only uses that π is a real number with
3 < π < 4 (Mathlib: `Real.pi_gt_three`, and an upper bound), so s = π − 3 lies in (0, 1).

## What this file claims, if it compiles
1. `moran`        — for s > 0, the two-piece ratio r = 2^(−1/s) satisfies 2 · r^s = 1.
2. `ratio_lt_half`— for 0 < s < 1, r < 1/2, so the two pieces [0,r] and [1−r,1] are disjoint.
3. `box_count`    — for every level k, with ε = r^k:  2^k · (ε⁻¹)^3 = (ε⁻¹)^(3+s).
   This is the box-counting identity of the chapter: the cover count of C × [0,1]^3 at scale ε
   is exactly ε^(−(3+s)).
4. `box_count_pi` — the same with 3 + s = π, for s = π − 3.

## What it does NOT claim
* That the Hausdorff dimension of C × [0,1]^3 equals π. Mathlib's Hausdorff dimension of a
  product with the needed hypotheses is not used here; the step from box count to Hausdorff
  dimension is the standard theorem quoted in the chapter, not formalised.
* That the count N(ε) is the minimal cover number of the set; the file proves the algebraic
  identity for the count 2^k · ε⁻³ that the chapter's argument uses.
* Anything about the lattice route.
-/

open Real

noncomputable section

/-- The ratio of the two-piece Cantor set whose similarity dimension is `s`. -/
def ratio (s : ℝ) : ℝ := (2 : ℝ) ^ (-(1 / s))

lemma ratio_pos (s : ℝ) : 0 < ratio s :=
  Real.rpow_pos_of_pos (by norm_num) _

lemma ratio_rpow (s : ℝ) (hs : 0 < s) : (ratio s) ^ s = 1 / 2 := by
  unfold ratio
  rw [← Real.rpow_mul (by norm_num : (0 : ℝ) ≤ 2)]
  have h : -(1 / s) * s = -1 := by field_simp
  rw [h, Real.rpow_neg_one]
  norm_num

/-- Similarity equation: 2 · r^s = 1. -/
theorem moran (s : ℝ) (hs : 0 < s) : 2 * (ratio s) ^ s = 1 := by
  rw [ratio_rpow s hs]; norm_num

/-- For 0 < s < 1 the ratio is below 1/2, so the two pieces are disjoint. -/
theorem ratio_lt_half (s : ℝ) (hs : 0 < s) (hs1 : s < 1) : ratio s < 1 / 2 := by
  unfold ratio
  have h1 : 1 < 1 / s := by
    rw [lt_div_iff₀ hs]; linarith
  have h2 : -(1 / s) < -1 := by linarith
  have h3 : (2 : ℝ) ^ (-(1 / s)) < (2 : ℝ) ^ (-1 : ℝ) :=
    Real.rpow_lt_rpow_of_exponent_lt (by norm_num) h2
  rw [Real.rpow_neg_one] at h3
  simpa using h3

/-- 2^k = (ε⁻¹)^s for ε = r^k, using 2 = r^(−s). -/
lemma two_pow_eq (s : ℝ) (hs : 0 < s) (k : ℕ) :
    (2 : ℝ) ^ k = (((ratio s) ^ k)⁻¹) ^ s := by
  have hr : 0 ≤ ratio s := (ratio_pos s).le
  have hrk : 0 ≤ (ratio s) ^ k := pow_nonneg hr k
  rw [Real.inv_rpow hrk]
  have h : ((ratio s) ^ k) ^ s = ((ratio s) ^ s) ^ k := by
    rw [← Real.rpow_natCast (ratio s) k, ← Real.rpow_mul hr,
        mul_comm, Real.rpow_mul hr, Real.rpow_natCast]
  rw [h, ratio_rpow s hs]
  rw [one_div, inv_pow, inv_inv]

/-- Box-count identity: 2^k · (ε⁻¹)^3 = (ε⁻¹)^(3+s) with ε = r^k. -/
theorem box_count (s : ℝ) (hs : 0 < s) (k : ℕ) :
    (2 : ℝ) ^ k * (((ratio s) ^ k)⁻¹) ^ (3 : ℕ)
      = (((ratio s) ^ k)⁻¹) ^ ((3 : ℝ) + s) := by
  have hpos : 0 < ((ratio s) ^ k)⁻¹ := inv_pos.mpr (pow_pos (ratio_pos s) k)
  have h3 : (((ratio s) ^ k)⁻¹) ^ (3 : ℝ) = (((ratio s) ^ k)⁻¹) ^ (3 : ℕ) := by
    exact_mod_cast Real.rpow_natCast (((ratio s) ^ k)⁻¹) 3
  rw [Real.rpow_add hpos, h3, two_pow_eq s hs k]
  ring

/-- The same with 3 + s = π, for s = π − 3. -/
theorem box_count_pi (k : ℕ) (hs : 0 < Real.pi - 3) :
    (2 : ℝ) ^ k * (((ratio (Real.pi - 3)) ^ k)⁻¹) ^ (3 : ℕ)
      = (((ratio (Real.pi - 3)) ^ k)⁻¹) ^ Real.pi := by
  have h := box_count (Real.pi - 3) hs k
  have e : (3 : ℝ) + (Real.pi - 3) = Real.pi := by ring
  rwa [e] at h

theorem pi_sub_three_pos : 0 < Real.pi - 3 := by
  have := Real.pi_gt_three
  linarith

#print axioms moran
#print axioms ratio_lt_half
#print axioms box_count
#print axioms box_count_pi

end
