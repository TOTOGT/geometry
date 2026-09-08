/-
  LadderBound.lean — Theorem 26.1, the one-parameter ladder.

  WHY THIS FILE EXISTS.  Book 4, Chapter 26 states a negative test: a proposed
  selection rule earns the name only if it can FORBID something.  The worked
  counter-case is a "ladder" of allowed values with a single free integer
  parameter,

      L_c = { c / N : N ∈ ℤ⁺ },

  as used by frameworks that report a measured frequency "lying on the ladder"
  and treat the fit as evidence.  The chapter's claim is that such a family
  excludes nothing in the regime where the claims are made, because its rungs
  are dense there relative to the target.  That claim is arithmetic, it is
  short, and there is no reason for it to rest on a numerical sweep.  So it is
  proved here.

  WHAT IS PROVED.  Fix c > 0 and a target f bracketed by two consecutive rungs,

      c/(n+1) ≤ f ≤ c/n     with 1 ≤ n.

  * `gap_eq`            — the gap between the rungs is c / (n(n+1)).
  * `half_gap`          — a point in an interval is within half its width of an
                          endpoint.
  * `ladder_abs_error`  — the nearer rung is within c / (2n(n+1)) of f.
  * `ladder_rel_error`  — **Theorem 26.1**: the RELATIVE error is at most
                          1/(2n).
  * `ladder_rel_error_of_lt` — the reader-facing form: at most f / (2(c−f)),
                          which is ≈ f/(2c) for f ≪ c.

  The last line is the content.  As f/c → 0 the bound → 0, so the ladder matches
  every target to arbitrary relative precision and forbids nothing.  A fit to it
  therefore carries no information — which is not a complaint about anyone's
  arithmetic but an observation that the family could not have failed.

  WHAT IS NOT HERE.  Nothing about whether any particular framework's ladder is
  wrong.  A family that cannot fail is not thereby false; it is unfalsifiable,
  which is a different and weaker charge.  The positive counterpart — a count
  with no free parameter that DOES return zero — is Chapter 25's
  W(T) = d₁(T) − d₂(T), and is not formalised here.

  VERIFICATION STATUS — 2026-09-08.  NOT YET RUN.
  (First draft had a wrong hypothesis in `ladder_rel_error_of_lt`: it derived
   n*f ≤ c from the upper bracket when the goal needs c ≤ (n+1)*f from the
   lower one. Found by re-deriving on paper, before any run. Corrected here.)

      cd ~/Desktop/geometry && lake env lean LadderBound.lean

  Expected: no output (Lean is silent on success), then the axiom report from
  the `#print axioms` lines at the foot of the file, which should list only
  [propext, Classical.choice, Quot.sound] for all five theorems.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic

namespace LadderBound

/-- The gap between consecutive rungs `c/n` and `c/(n+1)` of the ladder. -/
theorem gap_eq (c : ℝ) {n : ℝ} (hn : 0 < n) :
    c / n - c / (n + 1) = c / (n * (n + 1)) := by
  have h1 : n ≠ 0 := ne_of_gt hn
  have h2 : n + 1 ≠ 0 := by positivity
  field_simp
  ring

/-- A point of an interval lies within half the interval's width of one end. -/
theorem half_gap {a b x : ℝ} (hax : a ≤ x) (hxb : x ≤ b) :
    min (x - a) (b - x) ≤ (b - a) / 2 := by
  rcases le_total (x - a) (b - x) with h | h
  · rw [min_eq_left h]; linarith
  · rw [min_eq_right h]; linarith

/-- The nearer of the two bracketing rungs is within half a gap of the target. -/
theorem ladder_abs_error {c f n : ℝ} (hc : 0 < c) (hn : 0 < n)
    (hlo : c / (n + 1) ≤ f) (hhi : f ≤ c / n) :
    min (c / n - f) (f - c / (n + 1)) ≤ c / (2 * (n * (n + 1))) := by
  have h := half_gap hlo hhi
  have hg : c / n - c / (n + 1) = c / (n * (n + 1)) := gap_eq c hn
  have : min (f - c / (n + 1)) (c / n - f) ≤ (c / n - c / (n + 1)) / 2 := h
  rw [min_comm] at this
  rw [hg] at this
  calc min (c / n - f) (f - c / (n + 1))
      ≤ c / (n * (n + 1)) / 2 := this
    _ = c / (2 * (n * (n + 1))) := by ring

/-- **Theorem 26.1.**  For a target bracketed by rungs `n` and `n+1`, the
relative error of the nearer rung is at most `1 / (2n)`. -/
theorem ladder_rel_error {c f n : ℝ} (hc : 0 < c) (hn : 0 < n)
    (hlo : c / (n + 1) ≤ f) (hhi : f ≤ c / n) :
    min (c / n - f) (f - c / (n + 1)) / f ≤ 1 / (2 * n) := by
  have hn1 : (0:ℝ) < n + 1 := by linarith
  have hcn1 : 0 < c / (n + 1) := div_pos hc hn1
  have hf : 0 < f := lt_of_lt_of_le hcn1 hlo
  have habs := ladder_abs_error hc hn hlo hhi
  -- from  c/(n+1) ≤ f  we get  c ≤ f * (n+1)
  have hc_le : c ≤ f * (n + 1) := by
    rw [div_le_iff hn1] at hlo
    linarith
  have step : c / (2 * (n * (n + 1))) / f ≤ 1 / (2 * n) := by
    rw [div_div, div_le_div_iff (by positivity) (by positivity)]
    nlinarith [hc_le, hn, hf]
  calc min (c / n - f) (f - c / (n + 1)) / f
      ≤ c / (2 * (n * (n + 1))) / f := by gcongr
    _ ≤ 1 / (2 * n) := step

/-- Reader-facing form.  If the target sits strictly below `c`, the relative
error is at most `f / (2 (c − f))`, which tends to `0` as `f / c → 0`. -/
theorem ladder_rel_error_of_lt {c f n : ℝ} (hc : 0 < c) (hn : 0 < n)
    (hlo : c / (n + 1) ≤ f) (hhi : f ≤ c / n) (hfc : f < c) :
    min (c / n - f) (f - c / (n + 1)) / f ≤ f / (2 * (c - f)) := by
  have hn1 : (0:ℝ) < n + 1 := by linarith
  have hcn1 : 0 < c / (n + 1) := div_pos hc hn1
  have hf : 0 < f := lt_of_lt_of_le hcn1 hlo
  have hcf : 0 < c - f := by linarith
  have main := ladder_rel_error hc hn hlo hhi
  -- The goal cross-multiplies to  c - f ≤ n * f,  i.e.  c ≤ (n+1) * f,
  -- which is `hlo` with its denominator cleared.  (An earlier draft derived
  -- `n * f ≤ c` from `hhi` instead — the wrong direction, and unusable here.)
  have hc_le : c ≤ f * (n + 1) := by
    rw [div_le_iff hn1] at hlo
    linarith
  have : (1:ℝ) / (2 * n) ≤ f / (2 * (c - f)) := by
    rw [div_le_div_iff (by positivity) (by positivity)]
    nlinarith [hc_le, hf, hn, hcf]
  linarith [main, this]

/-- The corollary the chapter states: as the target falls away from `c`, the
bound collapses, so the ladder excludes nothing. -/
theorem ladder_forbids_nothing {c f n : ℝ} (hc : 0 < c) (hn : 0 < n)
    (hlo : c / (n + 1) ≤ f) (hhi : f ≤ c / n) (hfc : 2 * f ≤ c) :
    min (c / n - f) (f - c / (n + 1)) / f ≤ f / c := by
  have hn1 : (0:ℝ) < n + 1 := by linarith
  have hf : 0 < f := lt_of_lt_of_le (div_pos hc hn1) hlo
  have hfc' : f < c := by linarith
  have h := ladder_rel_error_of_lt hc hn hlo hhi hfc'
  have hcf : 0 < c - f := by linarith
  have : f / (2 * (c - f)) ≤ f / c := by
    rw [div_le_div_iff (by positivity) hc]
    nlinarith [hf, hfc, hcf]
  linarith

#print axioms gap_eq
#print axioms half_gap
#print axioms ladder_abs_error
#print axioms ladder_rel_error
#print axioms ladder_rel_error_of_lt
#print axioms ladder_forbids_nothing

end LadderBound
