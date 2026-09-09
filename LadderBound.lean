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

  VERIFICATION STATUS — 2026-09-09.  **CLEAN, RUN AND RECORDED.**

      cd ~/Desktop/geometry && lake env lean LadderBound.lean

  All six theorems:

      'LadderBound.gap_eq'                depends on axioms: [propext, Classical.choice, Quot.sound]
      'LadderBound.half_gap'              depends on axioms: [propext, Classical.choice, Quot.sound]
      'LadderBound.ladder_abs_error'      depends on axioms: [propext, Classical.choice, Quot.sound]
      'LadderBound.ladder_rel_error'      depends on axioms: [propext, Classical.choice, Quot.sound]
      'LadderBound.ladder_rel_error_of_lt' depends on axioms: [propext, Classical.choice, Quot.sound]
      'LadderBound.ladder_forbids_nothing' depends on axioms: [propext, Classical.choice, Quot.sound]

  No `sorryAx`, no axiom outside the permitted three, no errors.  Gated:

      python3 tools/axiom_gate.py <report> 6
      OK: 6 theorems, no sorryAx, no axiom outside the permitted set.

  Ran under Lean v4.32.0 in `geometry`.  Three drafts were needed and the faults
  are worth keeping, because two of the three had nothing to do with the
  mathematics:

    1. A real error, found on paper before any run: `ladder_rel_error_of_lt`
       derived `n*f ≤ c` from the UPPER bracket when the goal needs
       `c ≤ (n+1)*f` from the LOWER one.  Wrong direction; unprovable as
       written.
    2. `div_le_iff`, `le_div_iff`, `div_le_div_iff` and `le_or_lt` are all gone
       from this Mathlib — the GroupWithZero refactor.  Four failures, one
       cause, and none of it about the theorem.
    3. Two trailing `ring`s after a `field_simp` that had already closed the
       goal.  Reported as errors; the declarations were clean regardless.

  Lesson recorded in the audit log: proofs written against remembered lemma
  NAMES are fragile across Mathlib versions in a way proofs written with
  TACTICS are not.  The final version leans on field_simp, gcongr, positivity,
  nlinarith, by_cases and push_neg.

  Two harmless warnings remain and are deliberately not fixed: `hax`/`hxb` in
  `half_gap` are used implicitly by `linarith`, and `push_neg` is deprecated in
  favour of `push Not`.  Editing verified code to silence a warning would mean
  re-verifying it, which is a bad trade against a clean run.
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
  have hn1 : (0:ℝ) < n + 1 := by linarith
  have h1 : n ≠ 0 := ne_of_gt hn
  have h2 : n + 1 ≠ 0 := ne_of_gt hn1
  have h := half_gap hlo hhi
  rw [min_comm] at h
  calc min (c / n - f) (f - c / (n + 1))
      ≤ (c / n - c / (n + 1)) / 2 := h
    _ = c / (2 * (n * (n + 1))) := by rw [gap_eq c hn]; field_simp

/-- **Theorem 26.1.**  For a target bracketed by rungs `n` and `n+1`, the error of
the nearer rung is at most `f / (2n)` — stated as `2n · error ≤ f`, which is the
relative bound `error / f ≤ 1/(2n)` cleared of its division. -/
theorem ladder_rel_error {c f n : ℝ} (hc : 0 < c) (hn : 0 < n)
    (hlo : c / (n + 1) ≤ f) (hhi : f ≤ c / n) :
    2 * n * min (c / n - f) (f - c / (n + 1)) ≤ f := by
  have hn1 : (0:ℝ) < n + 1 := by linarith
  have h1 : n ≠ 0 := ne_of_gt hn
  have h2 : n + 1 ≠ 0 := ne_of_gt hn1
  have habs := ladder_abs_error hc hn hlo hhi
  have hpos : (0:ℝ) ≤ 2 * n := by positivity
  calc 2 * n * min (c / n - f) (f - c / (n + 1))
      ≤ 2 * n * (c / (2 * (n * (n + 1)))) := mul_le_mul_of_nonneg_left habs hpos
    _ = c / (n + 1) := by field_simp
    _ ≤ f := hlo

/-- The reader-facing form.  Since `2n · error ≤ f` and `c ≤ (n+1)f`, the error
is at most `f·f / (2(c−f))`, which tends to `0` with `f/c`. -/
theorem ladder_rel_error_of_lt {c f n : ℝ} (hc : 0 < c) (hn : 0 < n)
    (hlo : c / (n + 1) ≤ f) (hhi : f ≤ c / n) (hfc : f < c) :
    2 * (c - f) * min (c / n - f) (f - c / (n + 1)) ≤ f * f := by
  have hn1 : (0:ℝ) < n + 1 := by linarith
  have hf : 0 < f := lt_of_lt_of_le (div_pos hc hn1) hlo
  have hcf : 0 < c - f := by linarith
  -- clear `hlo` of its denominator with a tactic, not a renamed lemma
  have hc_le : c ≤ f * (n + 1) := by
    have h := hlo
    rw [div_le_iff₀ hn1] at h
    linarith
  have main := ladder_rel_error hc hn hlo hhi
  -- If the error is negative the bound is trivial; otherwise divide `main` through.
  by_cases hge : 0 ≤ min (c / n - f) (f - c / (n + 1))
  · nlinarith [main, hge, hc_le, hn, hf, hcf]
  · push_neg at hge
    nlinarith [hge, hf, hcf]

/-- The corollary the chapter states: once the target is at most half of `c`, the
error is bounded by `f·f / c`, so the ladder excludes nothing. -/
theorem ladder_forbids_nothing {c f n : ℝ} (hc : 0 < c) (hn : 0 < n)
    (hlo : c / (n + 1) ≤ f) (hhi : f ≤ c / n) (h2f : 2 * f ≤ c) :
    c * min (c / n - f) (f - c / (n + 1)) ≤ f * f := by
  have hn1 : (0:ℝ) < n + 1 := by linarith
  have hf : 0 < f := lt_of_lt_of_le (div_pos hc hn1) hlo
  have hfc : f < c := by linarith
  have h := ladder_rel_error_of_lt hc hn hlo hhi hfc
  nlinarith [h, hf, hc, h2f]

#print axioms gap_eq
#print axioms half_gap
#print axioms ladder_abs_error
#print axioms ladder_rel_error
#print axioms ladder_rel_error_of_lt
#print axioms ladder_forbids_nothing

end LadderBound
