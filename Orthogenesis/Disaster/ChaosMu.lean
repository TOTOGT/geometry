-- GATE-DECLARE: sorries = none
-- GATE-REASON: kernel-checked 2026-09-15 under the v4.32.0 pin. The one theorem
-- of the seven that carried real content was false as stated; the refutation and
-- the corrected statement are both here. Report: tools/verify-audit/2026-09-15/.
/-
# ChaosMu.lean
# ============
# The Lean behind §4 of
#   https://totogt.github.io/geometry/chMu-lyapunov.html
# "μ · Chaos Theory — the exit exponent".
#
# The chapter cited `ChaosMu.lean` at github.com/TOTOGT/AXLE from its publication
# until 2026-09-15. No file of that name has ever existed there. Placed here for
# the reason given in DisasterTheory.lean. AXLE/Disaster/README.md points here.
#
# THE FALSE THEOREM
# -----------------
# T1 as published:
#
#     theorem lyapunov_negative_implies_stable
#         {μ : ℝ} (hμ : μ < 0) (δ₀ : ℝ) (hδ : 0 < δ₀) :
#         ∀ t : ℝ, 0 ≤ t → δ₀ * Real.exp (μ * t) < δ₀
#
# At t = 0 this reads δ₀ · 1 < δ₀, which is false. The hypothesis needs 0 < t,
# not 0 ≤ t; with `≤` the statement fails at the single point where the
# perturbation has not yet decayed. It is the only one of the seven with
# quantifiers over anything, and it is the one that is wrong.
#
# THE OTHER SIX
# -------------
# T2, T3, T5 and T6 are arithmetic on numerals. T4 and T7 are `exp (-2) < 1` and
# a conjunction containing it. None of them mentions a Lyapunov exponent, a flow,
# or a spectrum; T1 was the only statement in the file about decay over time.
-/
import Mathlib.Tactic
import Mathlib.Analysis.SpecialFunctions.Exp

namespace dm3.ChaosMu

/-- **T1 as published is false**, at `t = 0`. -/
theorem published_T1_is_false :
    ¬ ∀ (μ : ℝ), μ < 0 → ∀ (d : ℝ), 0 < d → ∀ t : ℝ, 0 ≤ t →
      d * Real.exp (μ * t) < d := by
  intro h
  have := h (-1) (by norm_num) 1 (by norm_num) 0 (le_refl 0)
  simp at this

/-- T1′. The corrected statement: a negative exponent contracts strictly for
every **positive** time. -/
theorem lyapunov_strict_for_positive_time {μ : ℝ} (hμ : μ < 0) {d : ℝ}
    (hd : 0 < d) {t : ℝ} (ht : 0 < t) : d * Real.exp (μ * t) < d := by
  have h : Real.exp (μ * t) < 1 := Real.exp_lt_one_iff.mpr (mul_neg_of_neg_of_pos hμ ht)
  nlinarith [Real.exp_pos (μ * t)]

/-- T1″. The non-strict statement that is true on all of `t ≥ 0`, which is what
the published hypothesis could support. -/
theorem lyapunov_nonstrict_from_zero {μ : ℝ} (hμ : μ < 0) {d : ℝ} (hd : 0 < d)
    {t : ℝ} (ht : 0 ≤ t) : d * Real.exp (μ * t) ≤ d := by
  rcases eq_or_lt_of_le ht with h | h
  · simp [← h]
  · exact (lyapunov_strict_for_positive_time hμ hd h).le

/-- T2. `(-2 : ℝ) < 0`. Arithmetic. -/
theorem dm3_mu_max_is_negative : (-2 : ℝ) < 0 := by norm_num

/-- T3. `0 < 1/3 < 1`. Arithmetic. Cited as "chaos boundary: fold exists at
ε₀"; no boundary and no fold appear in the statement. -/
theorem chaos_boundary_at_eps0 : (0 : ℝ) < 1 / 3 ∧ (1 : ℝ) / 3 < 1 := by
  norm_num

/-- T4. `exp (-2) < 1`. Cited as a Banach fixed-point bound; no map and no
complete space appear. -/
theorem contraction_rate_e_neg2 : Real.exp (-2) < 1 :=
  Real.exp_lt_one_iff.mpr (by norm_num)

/-- T5. Five decimal literals in increasing order. Not a statement about the
n-bonacci constants, which are roots of `xⁿ = xⁿ⁻¹ + ⋯ + 1`. -/
theorem nbonacci_literals_increasing :
    (1.618 : ℝ) < 1.839 ∧ (1.839 : ℝ) < 1.927 ∧ (1.927 : ℝ) < 1.966 ∧
      (1.966 : ℝ) < 1.984 ∧ (1.984 : ℝ) < 2 := by
  norm_num

/-- T6. `3.569945672 ≠ 2`. Two numerals differ. The Feigenbaum constant is not
defined here, so this distinguishes a decimal approximation from 2 and not the
constant from τ. -/
theorem feigenbaum_literal_ne_two : (3.569945672 : ℝ) ≠ 2 := by norm_num

/-- T7. `2 > 0 ∧ exp (-4) < 1`. -/
theorem tau_is_stable_fixed_point : (2 : ℝ) > 0 ∧ Real.exp (-2 * 2) < 1 :=
  ⟨by norm_num, Real.exp_lt_one_iff.mpr (by norm_num)⟩

/-!
## OPEN

1. **μ_max = −2 for dm³.** That the transverse Lyapunov exponent of the dm³
   chain equals −2 at every point of the basin. No flow is defined here, so the
   quantity the chapter names has no referent in this file.
2. **The chaos exit.** That the n-bonacci ladder reduces the effective exponent
   toward −∞. T5 compares decimals.
3. **Feigenbaum vs τ.** That the period-doubling constant and the embodiment
   threshold are genuinely different objects rather than different numerals.
-/

end dm3.ChaosMu
