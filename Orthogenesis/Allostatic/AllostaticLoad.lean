-- GATE-DECLARE: sorries = none
-- GATE-REASON: new file 2026-09-25 for the geometry pin (Lean v4.32.0, Mathlib v4.32.0).
-- UNTESTED until the author runs `lake build` on it.
/-
# AllostaticLoad.lean — Book 3, Chapter 2 (taught path 28, ch2-allostatic.html)

What the chapter claims, and what is checked here:

  §1  The load index λ = Σ wᵢ sᵢ with binary sᵢ: non-negative for non-negative
      weights, bounded by Σ wᵢ, monotone in the set of flagged systems, and —
      with unit weights — exactly the number of flagged systems ("the total count
      of systems pushed past their range").
  §2  "λ is the radial coordinate r approaching the limit cycle Γ … As λ grows,
      V grows", with V = (r − 1)². V grows exactly when the distance |r − 1| to Γ
      grows (`V_lt_iff`). So on the approach to Γ, V falls; V grows with r only
      for r ≥ 1, where r moves away from Γ. The two sentences cannot both hold.
  §3  "When V exceeds ε₀ = 1/3, the stability radius is breached." ε₀ is a
      radius, |r − 1| < ε₀ (Book 4, Ch 10). V is a squared distance: the breach
      is V > ε₀² = 1/9 (`breach_iff`). Testing V > 1/3 misses breaches — r = 3/2
      is outside the radius while V = 1/4 < 1/3.

Not formalised: the biomarker thresholds, the weights, κ* = 35 in the widget
(which sums graded 0–10 scores, not binary sᵢ), and the basin itself (Book 4,
Ch 10: the symmetric radius 1/3 is a Grönwall estimate; the inner boundary is
r* ≈ 0.776, and every r(0) > 1 converges).
-/

import Mathlib

namespace Orthogenesis.Allostatic

open Finset

/-! ## §1 The load index -/

/-- sᵢ ∈ {0, 1}. -/
def indicator (b : Bool) : ℝ := if b then 1 else 0

/-- λ = Σ wᵢ sᵢ. -/
def load {ι : Type*} [Fintype ι] (w : ι → ℝ) (s : ι → Bool) : ℝ :=
  ∑ i, w i * indicator (s i)

variable {ι : Type*} [Fintype ι]

theorem load_nonneg (w : ι → ℝ) (hw : ∀ i, 0 ≤ w i) (s : ι → Bool) :
    0 ≤ load w s :=
  Finset.sum_nonneg fun i _ => mul_nonneg (hw i) (by unfold indicator; split_ifs <;> norm_num)

theorem load_le_total (w : ι → ℝ) (hw : ∀ i, 0 ≤ w i) (s : ι → Bool) :
    load w s ≤ ∑ i, w i :=
  Finset.sum_le_sum fun i _ => by
    unfold indicator
    split_ifs
    · simp
    · simp [hw i]

/-- Flagging more systems never lowers the load. -/
theorem load_mono (w : ι → ℝ) (hw : ∀ i, 0 ≤ w i) {s s' : ι → Bool}
    (h : ∀ i, s i = true → s' i = true) : load w s ≤ load w s' :=
  Finset.sum_le_sum fun i _ => by
    unfold indicator
    cases hs : s i
    · cases h' : s' i <;> simp [hw i]
    · simp [h i hs]

/-- With unit weights the load is the number of flagged systems. -/
theorem load_unit (s : ι → Bool) :
    load (fun _ => (1 : ℝ)) s = ((univ.filter fun i => s i = true).card : ℝ) := by
  simp only [load, indicator, one_mul]
  rw [Finset.sum_boole]

/-! ## §2 V = (r − 1)² grows exactly when the distance to Γ grows -/

/-- The chapter's Lyapunov function. -/
def V (r : ℝ) : ℝ := (r - 1) ^ 2

theorem V_lt_iff (r₁ r₂ : ℝ) : V r₁ < V r₂ ↔ |r₁ - 1| < |r₂ - 1| := by
  unfold V
  exact sq_lt_sq

/-- Approaching Γ from below (r growing up to 1), V falls. -/
theorem V_strictAntiOn : StrictAntiOn V (Set.Iic 1) := by
  intro a ha b hb hab
  simp only [Set.mem_Iic] at ha hb
  unfold V
  nlinarith [mul_pos (sub_pos.2 hab) (by linarith : (0 : ℝ) < 2 - a - b)]

/-- V grows with r only for r ≥ 1, where r moves away from Γ. -/
theorem V_strictMonoOn : StrictMonoOn V (Set.Ici 1) := by
  intro a ha b hb hab
  simp only [Set.mem_Ici] at ha hb
  unfold V
  nlinarith [mul_pos (sub_pos.2 hab) (by linarith : (0 : ℝ) < a + b - 2)]

/-! ## §3 The threshold compares a squared distance with a radius -/

/-- The stability radius ε₀ = 1/3 (Book 4, Ch 10: |r − 1| < ε₀). -/
noncomputable def eps0 : ℝ := 1 / 3

/-- Leaving the ball of radius ε is V > ε², not V > ε. -/
theorem breach_iff {ε : ℝ} (hε : 0 ≤ ε) (r : ℝ) : ε < |r - 1| ↔ ε ^ 2 < V r := by
  unfold V
  rw [sq_lt_sq, abs_of_nonneg hε]

/-- The chapter's test V > 1/3 misses a breach: r = 3/2 lies outside the radius
    1/3, but V(3/2) = 1/4 < 1/3. -/
theorem chapter_test_misses_breach : eps0 < |(3 / 2 : ℝ) - 1| ∧ V (3 / 2) < eps0 := by
  unfold eps0
  constructor
  · rw [abs_of_pos (by norm_num)]
    norm_num
  · norm_num [V]

end Orthogenesis.Allostatic

/-! ## Axiom probe -/
#print axioms Orthogenesis.Allostatic.load_nonneg
#print axioms Orthogenesis.Allostatic.load_le_total
#print axioms Orthogenesis.Allostatic.load_mono
#print axioms Orthogenesis.Allostatic.load_unit
#print axioms Orthogenesis.Allostatic.V_lt_iff
#print axioms Orthogenesis.Allostatic.V_strictAntiOn
#print axioms Orthogenesis.Allostatic.V_strictMonoOn
#print axioms Orthogenesis.Allostatic.breach_iff
#print axioms Orthogenesis.Allostatic.chapter_test_misses_breach
