/-
  LadderRung.lean — the bracketing lemma that LadderBound.lean assumes.

  STATUS (2026-11-15): COMPILES in the recorded environments; correspondence with
  Chapter 26 NOT YET REVIEWED.  Compilation and the axiom gate say only that these three
  statements are proved in Lean; they do not say the statements are what the chapter claims.

  History.  First written 2026-11-15 in a container with no Lean toolchain (DRAFT, NOT
  COMPILED).  The first committed version did not compile: two `rwa` steps failed (lines
  68 and 71) and two theorems carried sorryAx.  Two proof steps were then changed
  (`rwa` -> `rw` then `linarith`); no theorem statement changed.
  Recorded run: Lean 4.32.0, Mathlib 81a5d257c8e410db227a6665ed08f64fea08e997, Linux
  x86_64, exit 0, all three theorems on [propext, Classical.choice, Quot.sound],
  tools/axiom_gate.py ... 3 prints OK.  Record: tools/verify-audit/2026-11-15/RECORD.md.

  Checks.  `lean_lib LadderRung` is a default target in lakefile.lean, and the CI step
  "Kernel axiom check on the Ladder files" runs tools/verify-ladder/run.sh (compile,
  gate 3, probe through the target, pin check).  This header does not record that the CI
  step has passed; its result is the authority.  Re-run locally:
      bash tools/verify-ladder/run.sh
  Not run on the author's machine as of this note.

  WHAT THIS ADDS.  LadderBound.lean takes the bracket
      c/(n+1) ≤ f ≤ c/n,  1 ≤ n
  as a HYPOTHESIS.  Chapter 26's claim "every target 0 < f ≤ c lies on some
  rung bracket, and the nearer rung is within f²/(2(c−f))" needs the existence
  of such an n.  This file proves it, with n = ⌊c/f⌋.

  Theorems (3):
    * `ladder_bracket`        — 0<f, f≤c ⇒ ∃ n:ℕ, 1≤n ∧ c/(n+1) ≤ f ∧ f ≤ c/n
    * `ladder_nearest_rung`   — 0<c, 0<f<c ⇒ ∃ N:ℕ, 1≤N ∧ |c/N − f| ≤ f²/(2(c−f))
    * `ladder_nearest_rung_rel` — the same, relative form |c/N − f|/f ≤ f/(2(c−f))

  NOT PROVED: that any particular framework's ladder is wrong.  See
  LadderBound.lean, WHAT IS NOT HERE.  The case f = c is a rung (N = 1) and is
  excluded from the quantitative form only because c − f = 0 there.
-/
import Mathlib

open Nat

/-- Existence of the bracketing rung index. -/
theorem ladder_bracket {c f : ℝ} (hf : 0 < f) (hfc : f ≤ c) :
    ∃ n : ℕ, 1 ≤ n ∧ c / ((n : ℝ) + 1) ≤ f ∧ f ≤ c / (n : ℝ) := by
  have hc : 0 < c := lt_of_lt_of_le hf hfc
  have hr : (1 : ℝ) ≤ c / f := by
    rw [le_div_iff₀ hf]; linarith
  refine ⟨⌊c / f⌋₊, ?_, ?_, ?_⟩
  · exact Nat.le_floor (by simpa using hr)
  · -- c/f < ⌊c/f⌋₊ + 1, so c < (n+1) f
    have h1 : c / f < (⌊c / f⌋₊ : ℝ) + 1 := Nat.lt_floor_add_one (c / f)
    have h2 : c < ((⌊c / f⌋₊ : ℝ) + 1) * f := by
      rw [div_lt_iff₀ hf] at h1; exact h1
    have hpos : (0 : ℝ) < (⌊c / f⌋₊ : ℝ) + 1 := by positivity
    rw [div_le_iff₀ hpos]; nlinarith
  · -- ⌊c/f⌋₊ ≤ c/f, so n f ≤ c
    have hn1 : 1 ≤ ⌊c / f⌋₊ := Nat.le_floor (by simpa using hr)
    have hnpos : (0 : ℝ) < (⌊c / f⌋₊ : ℝ) := by
      exact_mod_cast hn1
    have h1 : (⌊c / f⌋₊ : ℝ) ≤ c / f := Nat.floor_le (by positivity)
    have h2 : (⌊c / f⌋₊ : ℝ) * f ≤ c := by
      rw [le_div_iff₀ hf] at h1; exact h1
    rw [le_div_iff₀ hnpos]; nlinarith

/-- Nearest rung, absolute error f²/(2(c−f)). -/
theorem ladder_nearest_rung {c f : ℝ} (hc : 0 < c) (hf : 0 < f) (hfc : f < c) :
    ∃ N : ℕ, 1 ≤ N ∧ |c / (N : ℝ) - f| ≤ f ^ 2 / (2 * (c - f)) := by
  obtain ⟨n, hn1, hlo, hhi⟩ := ladder_bracket hf hfc.le
  have hn : (0 : ℝ) < n := by exact_mod_cast hn1
  have hn1' : (0 : ℝ) < (n : ℝ) + 1 := by positivity
  have hcf : 0 < c - f := by linarith
  -- (n+1) f ≥ c, from the lower bracket
  have hlo' : c ≤ ((n : ℝ) + 1) * f := by
    rw [div_le_iff₀ hn1'] at hlo
    linarith
  -- n f ≤ c, from the upper bracket
  have hhi' : (n : ℝ) * f ≤ c := by
    rw [le_div_iff₀ hn] at hhi
    linarith
  -- key bound: c/(n(n+1)) / 2 ≤ f²/(2(c−f))
  have key : c / (2 * ((n : ℝ) * ((n : ℝ) + 1))) ≤ f ^ 2 / (2 * (c - f)) := by
    rw [div_le_div_iff₀ (by positivity) (by positivity)]
    -- c * (2(c−f)) ≤ f² * (2 n (n+1)), using c ≤ (n+1) f and c − f ≤ n f
    have a : c - f ≤ (n : ℝ) * f := by linarith
    have b : c * (c - f) ≤ ((n : ℝ) + 1) * f * ((n : ℝ) * f) := by
      apply mul_le_mul hlo' a hcf.le (by positivity)
    nlinarith [b]
  -- half-gap
  have gap : c / (n : ℝ) - c / ((n : ℝ) + 1) = c / ((n : ℝ) * ((n : ℝ) + 1)) := by
    field_simp; ring
  by_cases h : f - c / ((n : ℝ) + 1) ≤ c / (n : ℝ) - f
  · refine ⟨n + 1, by omega, ?_⟩
    have hcast : ((n + 1 : ℕ) : ℝ) = (n : ℝ) + 1 := by push_cast; ring
    rw [hcast, abs_of_nonpos (by linarith)]
    have : c / (2 * ((n : ℝ) * ((n : ℝ) + 1))) = (c / (n : ℝ) - c / ((n : ℝ) + 1)) / 2 := by
      rw [gap]; field_simp
    linarith
  · refine ⟨n, hn1, ?_⟩
    rw [abs_of_nonneg (by linarith)]
    have : c / (2 * ((n : ℝ) * ((n : ℝ) + 1))) = (c / (n : ℝ) - c / ((n : ℝ) + 1)) / 2 := by
      rw [gap]; field_simp
    linarith

/-- Relative form, the reader-facing statement of Chapter 26. -/
theorem ladder_nearest_rung_rel {c f : ℝ} (hc : 0 < c) (hf : 0 < f) (hfc : f < c) :
    ∃ N : ℕ, 1 ≤ N ∧ |c / (N : ℝ) - f| / f ≤ f / (2 * (c - f)) := by
  obtain ⟨N, hN, h⟩ := ladder_nearest_rung hc hf hfc
  refine ⟨N, hN, ?_⟩
  rw [div_le_iff₀ hf]
  calc |c / (N : ℝ) - f| ≤ f ^ 2 / (2 * (c - f)) := h
    _ = f / (2 * (c - f)) * f := by ring

#print axioms ladder_bracket
#print axioms ladder_nearest_rung
#print axioms ladder_nearest_rung_rel
