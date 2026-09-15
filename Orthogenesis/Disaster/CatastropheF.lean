-- GATE-DECLARE: sorries = none
-- GATE-REASON: kernel-checked 2026-09-15 under the v4.32.0 pin. Two of the
-- seven theorems this file replaces were false; both refutations are theorems
-- here rather than remarks. Report: tools/verify-audit/2026-09-15/.
/-
# CatastropheF.lean
# =================
# The Lean behind §4 of
#   https://totogt.github.io/geometry/chF-catastrophe.html
# "F · Catastrophe Theory — the Whitney fold at ε₀".
#
# The chapter cited `CatastropheF.lean` at github.com/TOTOGT/AXLE from its
# publication until 2026-09-15. No file of that name has ever existed there.
# It is placed here, in geometry, for the reason given in DisasterTheory.lean:
# AXLE pins v4.14.0, has no .lake and no workflow, so nothing deposited there is
# checked by anything. AXLE/Disaster/README.md points here.
#
# THE TWO FALSE THEOREMS
# ----------------------
# T2 as published:
#
#     theorem fold_singularity_at_eps0 :
#         deriv (fun x => whitney_fold (1/3) x) 0 = 0
#
# The derivative is 3x² + a, which at a = 1/3, x = 0 is 1/3. False — the same
# statement, with the same tactic, that chDis-disaster.html published as D2.
#
# T3 as published:
#
#     theorem fold_unique_critical_point {a : ℝ} (ha : 0 < a) :
#         ∃! x : ℝ, deriv (fun t => whitney_fold a t) x = 0
#
# For a > 0 the derivative 3x² + a is strictly positive everywhere, so there is
# no critical point at all. The theorem does not merely overstate: it asserts
# the existence of an object the hypothesis excludes. Both are refuted below
# and replaced by the statements they were reaching for.
#
# WHAT THE REMAINING FIVE ARE
# ---------------------------
# T1 is a definition (reused from DisasterTheory.lean rather than redeclared).
# T4 concludes `∃ f, f x = x⁴ + a·x² + b·x`, which is `rfl` under an existential
# and says nothing about unfolding. T5, T6 and T7 are arithmetic on numerals.
# None of the seven carried the content its name claimed.
-/
import Orthogenesis.Disaster.DisasterTheory

namespace dm3.CatastropheF

open dm3.DisasterTheory

/-- **T2 as published is false.** Same statement and same tactic as the D2 of
chDis-disaster.html; the defect travelled between chapters. -/
theorem published_T2_is_false :
    deriv (fun x => whitney_fold (1 / 3) x) 0 ≠ 0 := by
  rw [whitney_fold_deriv]; norm_num

/-- **T3 as published is false.** It asserted a unique critical point for
`a > 0`. There is none: `3x² + a > 0` everywhere. -/
theorem published_T3_is_false {a : ℝ} (ha : 0 < a) :
    ¬ ∃ x : ℝ, deriv (fun t => whitney_fold a t) x = 0 := by
  rintro ⟨x, hx⟩
  rw [whitney_fold_deriv] at hx
  nlinarith [sq_nonneg x]

/-- T3′. What is true above `a = 0`: the unfolding is strictly increasing, so
the fold is resolved and no critical point survives. -/
theorem no_critical_point_of_pos {a : ℝ} (ha : 0 < a) (x : ℝ) :
    deriv (fun t => whitney_fold a t) x > 0 := by
  rw [whitney_fold_deriv]; positivity

/-- T2′. The fold of this unfolding sits at `a = 0`, and `a = 0` is the only
parameter at which it has a degenerate critical point. -/
theorem fold_exactly_at_zero {a : ℝ} :
    (∃ x : ℝ, deriv (fun t => whitney_fold a t) x = 0) ↔ a ≤ 0 := by
  constructor
  · rintro ⟨x, hx⟩
    rw [whitney_fold_deriv] at hx
    nlinarith [sq_nonneg x]
  · intro ha
    refine ⟨Real.sqrt (-a / 3), ?_⟩
    rw [whitney_fold_deriv, Real.sq_sqrt (by linarith : (0:ℝ) ≤ -a / 3)]
    ring

/-- T4 as published. True, and empty: `∃ f, f x = e` is `rfl` under an
existential for any expression `e`. It states nothing about unfolding, about
the cusp, or about the fold. Kept so that the shape is on the record. -/
theorem cusp_unfolds_fold_as_published (a b x : ℝ) :
    ∃ f : ℝ → ℝ, f x = x ^ 4 + a * x ^ 2 + b * x :=
  ⟨fun x => x ^ 4 + a * x ^ 2 + b * x, rfl⟩

/-- T5. `1 < 2 < 3 < 4`. Arithmetic on numerals. It is cited as "the A-series
unfolds: fold (A₁) < cusp (A₂) in codimension"; no codimension is defined. -/
theorem a_series_codim_increases : (1 : ℕ) < 2 ∧ 2 < 3 ∧ 3 < 4 := by norm_num

/-- T6. `1/3 < a → 0 < 3a`. Arithmetic. -/
theorem fold_resolved_above_eps0 {a : ℝ} (ha : 1 / 3 < a) : 0 < 3 * a := by
  linarith

/-- T7. `2 > 1/3 + 1/9 + 1/27 + 1/81`. Arithmetic on numerals. It is cited as
"τ = 2 is fold-free: the A-series unfolding is complete at τ"; completeness of
an unfolding is not stated here. -/
theorem tau_is_fold_free : (2 : ℝ) > 1 / 3 + 1 / 9 + 1 / 27 + 1 / 81 := by
  norm_num

/-!
## OPEN

1. **The A-series as an unfolding sequence.** That A₁ ⊂ A₂ ⊂ A₃ ⊂ A₄ is a chain
   of versal unfoldings of increasing codimension. T5 compares four numerals.
2. **κ₁₂ = ε₀ = 1/3 as the fold parameter.** `TripleChamber.lean` in AXLE
   defines `κ₁₂ := ε₀` and proves the triple-chamber eigenvalue is antitone in
   κ. That is a resonance statement, not a statement that the fold sits at κ₁₂,
   and AXLE compiles nothing.
3. **The seven catastrophes.** Thom's classification is cited, not formalised.
-/

end dm3.CatastropheF
