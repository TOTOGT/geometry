-- GATE-DECLARE: sorries = none
-- GATE-REASON: kernel-checked 2026-09-15 under the v4.32.0 pin. 19 declarations,
-- none admitted, every one on the permitted three axioms except seven_eq_seven,
-- which depends on none. Report: tools/verify-audit/2026-09-15/.
/-
# DisasterTheory.lean
# ===================
# The Lean behind §5 of
#   https://totogt.github.io/geometry/chDis-disaster.html
# "Disaster Theory — A Contact-Geometric Unification of Catastrophe and Chaos"
# (Zenodo, doi:10.5281/zenodo.19117399).
#
# WHY THIS FILE IS HERE AND NOT IN AXLE
# -------------------------------------
# The chapter cited this file, and CatastropheF.lean and ChaosMu.lean, at
# github.com/TOTOGT/AXLE. None of the three has ever existed there: not in the
# working tree and not anywhere in that repository's history. The Lean source
# existed only inside the HTML that claimed it had been checked.
#
# It is placed under Orthogenesis/ rather than in AXLE because AXLE pins
# leanprover/lean4:v4.14.0, has no .lake and no workflow, so a file deposited
# there would be as uncheckable as one that does not exist. This repository
# pins v4.32.0 and builds. An address that resolves into a target is the only
# kind worth citing. AXLE/Disaster/README.md points here.
#
# WHAT CHANGED FROM THE PUBLISHED LISTING
# ---------------------------------------
# D2 as published read
#
#     theorem fold_at_eps0 :
#         deriv (fun x => whitney_fold (1/3) x) 0 = 0 := by
#       simp [whitney_fold]; ring
#
# and is false. The derivative of x³ + a·x is 3x² + a, which at a = 1/3, x = 0
# is 1/3, not 0. No tactic closes it, so the listing as published could not have
# compiled — an internal proof, independent of the missing file, that the
# "sorry-free, machine-checkable" banner above it was never earned.
#
# That is now a theorem here rather than a remark: `published_D2_is_false`
# carries the refutation in the kernel. `fold_at_zero_parameter` gives the
# statement D2 was reaching for — the fold of this unfolding is at a = 0 — and
# `no_critical_point_at_eps0` gives what is true at a = ε₀ = 1/3, which is the
# opposite of what D2 asserted and is what D3's own docstring already said.
#
# NAMES THAT EXCEED THEIR STATEMENTS
# ----------------------------------
# Of the fourteen entries as published, one (D1) is a definition and nine
# conclude arithmetic about numerals while their docstrings name structural
# results. D11 is the clearest: docstringed "bijection between catastrophes and
# operators" and proved (7 : ℕ) = 7 by rfl. Those are kept here verbatim,
# because they are true and cheap, but each docstring now says what its own
# theorem says. The structural claims are listed as open obligations at the end,
# where a reader can see that nothing has been proved about them.
#
# WHAT IS STILL NOT HERE
# ----------------------
# The Disaster Theorem. The four parts of it in §2 of the chapter are not
# formalised by these theorems and are not formalised by any file in any of
# these repositories. See the OPEN block at the end.
-/
import Mathlib.Tactic
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.Deriv.Add

namespace dm3.DisasterTheory

/-! ## Part I — the fold -/

/-- D1. Whitney A₂ normal form, one-parameter unfolding `x³ + a·x`. A
definition. It is not evidence of anything. -/
noncomputable def whitney_fold (a x : ℝ) : ℝ := x ^ 3 + a * x

/-- The derivative of the unfolding: `d/dx (x³ + a·x) = 3x² + a`. Everything
in Part I reads off this. -/
theorem whitney_fold_hasDerivAt (a x : ℝ) :
    HasDerivAt (fun y => whitney_fold a y) (3 * x ^ 2 + a) x := by
  have h1 : HasDerivAt (fun y : ℝ => y ^ 3) (3 * x ^ 2) x := by
    simpa using hasDerivAt_pow 3 x
  have h2 : HasDerivAt (fun y : ℝ => a * y) a x := by
    simpa using (hasDerivAt_id x).const_mul a
  simpa [whitney_fold, Pi.add_def] using HasDerivAt.add h1 h2

/-- The same, as an equation on `deriv`. -/
theorem whitney_fold_deriv (a x : ℝ) :
    deriv (fun y => whitney_fold a y) x = 3 * x ^ 2 + a :=
  (whitney_fold_hasDerivAt a x).deriv

/-- **D2 as published is false.** The chapter asserted
`deriv (fun x => whitney_fold (1/3) x) 0 = 0`. It is `1/3`. Kept as a theorem
rather than a comment: the refutation of a published claim belongs in the same
kernel as the claims that replaced it. -/
theorem published_D2_is_false :
    deriv (fun y => whitney_fold (1 / 3) y) 0 ≠ 0 := by
  rw [whitney_fold_deriv]; norm_num

/-- D2′. At `a = ε₀ = 1/3` the unfolding is strictly increasing everywhere, so
it has **no** critical point. This is the opposite of what the published D2
asserted, and is what D3's docstring already said. -/
theorem no_critical_point_at_eps0 (x : ℝ) :
    deriv (fun y => whitney_fold (1 / 3) y) x > 0 := by
  rw [whitney_fold_deriv]; positivity

/-- D2″. The statement D2 was reaching for: the fold of `x³ + a·x` sits at
`a = 0`, not at `a = ε₀`. -/
theorem fold_at_zero_parameter :
    deriv (fun y => whitney_fold 0 y) 0 = 0 := by
  rw [whitney_fold_deriv]; norm_num

/-- D3. `1/3 < a → 0 < 3a`. Arithmetic. The published docstring read
"f′(x) > 0 for a > 1/3", which is D3′ below, not this. -/
theorem fold_resolved_above_eps0 {a : ℝ} (ha : 1 / 3 < a) : 0 < 3 * a := by
  linarith

/-- D3′. The statement D3's docstring was making: above `ε₀` the unfolding is
strictly increasing everywhere, so no fold survives. -/
theorem no_critical_point_above_eps0 {a : ℝ} (ha : 1 / 3 < a) (x : ℝ) :
    deriv (fun y => whitney_fold a y) x > 0 := by
  rw [whitney_fold_deriv]
  have : (0 : ℝ) < a := by linarith
  positivity

/-- D4. `(2 : ℝ) > 1/3`. Arithmetic on two numerals. It is cited as "τ = 2 is
fold-free"; that reading is D3′ instantiated at `a = 2`, not this. -/
theorem tau_fold_free : (2 : ℝ) > 1 / 3 := by norm_num

/-! ## Part II — the exponent -/

/-- D5. `(-2 : ℝ) < 0`. Arithmetic. "μ_max = −2 implies stability" is a claim
about a Lyapunov spectrum; nothing here mentions one. -/
theorem mu_max_negative : (-2 : ℝ) < 0 := by norm_num

/-- D6. `exp (-2) < 1`. -/
theorem contraction_at_rate_neg2 : Real.exp (-2) < 1 :=
  Real.exp_lt_one_iff.mpr (by norm_num)

/-- D7. The five decimal literals `1.618 < 1.839 < 1.927 < 1.966 < 1.984 < 2`
are in increasing order. Arithmetic on numerals. It is cited as "the n-bonacci
cascade is strictly increasing toward τ"; that is a statement about the roots
of `xⁿ = xⁿ⁻¹ + ⋯ + 1` and is not proved here or anywhere in this repository. -/
theorem nbonacci_literals_increasing :
    (1.618 : ℝ) < 1.839 ∧ (1.839 : ℝ) < 1.927 ∧ (1.927 : ℝ) < 1.966 ∧
      (1.966 : ℝ) < 1.984 ∧ (1.984 : ℝ) < 2 := by
  norm_num

/-! ## Part III — the ordering -/

/-- D8. `1/3 < 1.618 < 2`. Arithmetic on numerals. -/
theorem disaster_order : (1 : ℝ) / 3 < 1.618 ∧ (1.618 : ℝ) < 2 := by norm_num

/-- D9. `1/3 < 1 < 2`. Arithmetic on numerals. -/
theorem chaos_between_fold_and_tau :
    (1 : ℝ) / 3 < 1 ∧ (1 : ℝ) < 2 := by norm_num

/-- D10. A positive quantity contracts under the factor `exp (-2)`. -/
theorem ladder_contraction (x : ℝ) (hx : 0 < x) : x * Real.exp (-2) < x := by
  nlinarith [Real.exp_pos (-2), contraction_at_rate_neg2]

/-- D11. `(7 : ℕ) = 7`. This is `rfl` and depends on no axioms at all. It was
published under the docstring "bijection between catastrophes and operators",
which it does not state. Thom's seven elementary catastrophes and the seven dm³
operators are both counted by hand; no map between them is defined here. Kept so
the numeral agreement is on the record as an observation, not as a theorem. -/
theorem seven_eq_seven : (7 : ℕ) = 7 := rfl

/-- D12. `0 < 1/3 < 1`. Arithmetic on numerals. -/
theorem eps0_in_unit_interval :
    (0 : ℝ) < 1 / 3 ∧ (1 : ℝ) / 3 < 1 := by norm_num

/-- D13. `(1/3) · exp (-2) < 1/3`. -/
theorem safe_ball_contracts : (1 : ℝ) / 3 * Real.exp (-2) < 1 / 3 := by
  have h : Real.exp (-2) < 1 := contraction_at_rate_neg2
  linarith

/-- D14. The four numeric side-conditions of the chapter's §2, conjoined. A
conjunction of arithmetic facts about numerals. It is not the Disaster Theorem
and does not imply it; see the OPEN block below. -/
theorem disaster_constants_consistent :
    (1 : ℝ) / 3 > 0 ∧ (-2 : ℝ) < 0 ∧ (2 : ℝ) > 1 / 3 ∧ Real.exp (-2) < 1 :=
  ⟨by norm_num, by norm_num, by norm_num, contraction_at_rate_neg2⟩

/-!
## OPEN — what the chapter claims and this file does not prove

Nothing below is stated as a Lean proposition, because stating it would mean
naming the objects, and the objects are not defined in this repository. Each is
an obligation, recorded so that its absence is visible at the same address as
the theorems.

1. **The Disaster Theorem, all four parts.** §2 of the chapter. Not formalised.
2. **Thom ↔ dm³.** A map from the seven elementary catastrophes to the seven
   dm³ operators, and a proof that it is a bijection. `seven_eq_seven` is not
   this and is not a step toward it.
3. **The n-bonacci cascade.** That the root of `xⁿ = xⁿ⁻¹ + ⋯ + 1` increases in
   `n` and converges to 2. `nbonacci_literals_increasing` compares five decimal
   approximations and says nothing about the roots. AXLE's
   `TribonacciRatioConvergence.lean` is the nearest existing work.
4. **μ_max = −2 as a Lyapunov exponent.** `mu_max_negative` proves `-2 < 0`.
   The claim that −2 is the universal chaos-exit exponent for dm³ systems is
   analytic and is not in any kernel.
5. **The contact-geometric unification.** No contact structure appears in this
   file.
-/

end dm3.DisasterTheory
