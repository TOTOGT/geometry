-- GATE-DECLARE: sorries = none
-- GATE-REASON: ported from AXLE and kernel-checked 2026-09-15 under the v4.32.0
-- pin. T1 as written in AXLE is false over all of ℝ; the refutation and the
-- corrected domain-restricted statement are both here.
/-
# TripleChamber.lean — ported into a build target
# ================================================
# Origin: AXLE/TripleChamber.lean (June 2026; no Zenodo deposit — the DOI it
# cited, 10.5281/zenodo.20682934, is TOGT V1, a different work),
# written against leanprover/lean4:v4.14.0. AXLE has no `.lake` and no
# workflow, so no version of that file has ever been elaborated by CI. It is
# cited as "formally verified" by chF-catastrophe.html §1.
#
# Ported here because it is the one file of the Disaster cluster that exists,
# and because the ETF Connect working paper (book6/wp121) leans on T1 and T5.
# A paper should not lean on a file nothing compiles.
#
# WHAT THE PORT FOUND
# -------------------
# 1. `λ_triple` no longer parses: `λ` is the lambda token. Renamed `lam_triple`.
#    Cosmetic, but it means the file could not have been elaborated under any
#    toolchain after the rename — which is consistent with its never having been.
#
# 2. **T1 is false as stated.** It claimed
#
#        StrictAnti (fun κ => λ_triple A γ κ)
#
#    over all of ℝ. With A = γ = 1 take κ₁ = -3, κ₂ = -2: the denominator
#    (1 + κ)² is 4 and 1, so the function rises from 1/4 to 1. Strict antitonicity
#    fails on the whole line because 1 + γκ changes sign, and blows up at
#    κ = -1/γ. The physical content — larger coupling lowers the mode — needs
#    κ ≥ 0, which every application assumes and no statement recorded.
#    `published_T1_is_false` refutes it; `triple_chamber_strictAntiOn_nonneg`
#    is the corrected statement. T4 is restated on the same domain.
#
# 3. T5 and T9 needed new proofs under the current Mathlib. The statements are
#    unchanged.
#
# The other six theorems port unchanged and are true as written.
-/
import Mathlib.Tactic
import Mathlib.Analysis.SpecialFunctions.Pow.Real

open Real

namespace dm3.TripleChamber

/-! ## §0 Constants -/

/-- dm³ stability radius ε₀ = 1/3 -/
noncomputable def ε₀ : ℝ := 1 / 3

/-- First coupling (inner ↔ ionospheric transition) = ε₀ -/
noncomputable def κ₁₂ : ℝ := ε₀

/-- Second coupling (ionospheric ↔ plasmaspheric) = ε₀² -/
noncomputable def κ₂₃ : ℝ := ε₀ ^ 2

/-- Triple-chamber eigenvalue `λ(κ) = A / (1 + γ·κ)²`, with `h` absorbed into
`A`. Renamed from `λ_triple`, which no longer parses. -/
noncomputable def lam_triple (A γ κ : ℝ) : ℝ := A / (1 + γ * κ) ^ 2

/-! ## §1 Monotonicity in the coupling -/

/-- **T1 as written in AXLE is false.** It asserted `StrictAnti` over all of ℝ.
Counterexample at `A = γ = 1`, `κ₁ = -3 < κ₂ = -2`. -/
theorem published_T1_is_false : ¬ StrictAnti (fun κ => lam_triple 1 1 κ) := by
  intro h
  have := h (show (-3 : ℝ) < -2 by norm_num)
  simp [lam_triple] at this
  norm_num at this

/-- T1′. The corrected statement: on `κ ≥ 0` the mode is strictly antitone in
the coupling. Larger coupling lowers the resonance. This is the domain every
application of T1 silently assumed. -/
theorem triple_chamber_strictAntiOn_nonneg {A γ : ℝ} (hA : 0 < A) (hγ : 0 < γ) :
    StrictAntiOn (fun κ => lam_triple A γ κ) (Set.Ici 0) := by
  intro a ha b hb hab
  simp only [Set.mem_Ici] at ha hb
  simp only [lam_triple]
  have pa : (0 : ℝ) < 1 + γ * a := by nlinarith
  have pb : (0 : ℝ) < 1 + γ * b := by nlinarith
  have h1 : (0 : ℝ) < (1 + γ * a) ^ 2 := by positivity
  have hlt : 1 + γ * a < 1 + γ * b := by nlinarith
  have h2 : (1 + γ * a) ^ 2 < (1 + γ * b) ^ 2 := by nlinarith [pa, pb, hlt]
  exact div_lt_div_of_pos_left hA h1 h2

/-- T2. The coupling perturbation is non-negative. -/
theorem triple_perturbation_nonneg {k₁₂ k₂₃ A₁₂ A₂₃ : ℝ}
    (h12 : 0 ≤ k₁₂) (h23 : 0 ≤ k₂₃) (hA12 : 0 ≤ A₁₂) (hA23 : 0 ≤ A₂₃) :
    0 ≤ k₁₂ * A₁₂ + k₂₃ * A₂₃ := by
  positivity

/-! ## §2 Coupled-mode ordering -/

/-- T3. Stronger aperture coupling lowers the global fundamental eigenvalue. -/
theorem triple_coupled_eigenvalue_decreases {lam₀ κ A : ℝ}
    (hlam : 0 < lam₀) (hκ : 0 < κ) (hA : 0 < A) : lam₀ - κ * A < lam₀ := by
  linarith [mul_pos hκ hA]

/-- T4. Restated on `κ ≥ 0`, the domain T1′ establishes. -/
theorem triple_dm3_curvature_lowers_all_modes {A γ κ₁ κ₂ : ℝ}
    (hA : 0 < A) (hγ : 0 < γ) (hκ : 0 ≤ κ₁) (hlt : κ₁ < κ₂) :
    lam_triple A γ κ₂ < lam_triple A γ κ₁ :=
  triple_chamber_strictAntiOn_nonneg hA hγ hκ (le_of_lt (lt_of_le_of_lt hκ hlt)) hlt

/-! ## §3 Mode splitting -/

/-- T5. The split modes `ω± = ω₀·√(1 ± κδ)` bracket the uncoupled mode `ω₀`
whenever `κδ < 1`. Coupling does not damp the mode; it splits it in two, one
below and one above. -/
theorem triple_mode_splitting_brackets {ω₀ κ δ : ℝ}
    (hω : 0 < ω₀) (hκ : 0 < κ) (hδ : 0 < δ) (hbound : κ * δ < 1) :
    ω₀ * sqrt (1 - κ * δ) < ω₀ ∧ ω₀ < ω₀ * sqrt (1 + κ * δ) := by
  have hkd : 0 < κ * δ := mul_pos hκ hδ
  constructor
  · have h : sqrt (1 - κ * δ) < 1 := by
      have : sqrt (1 - κ * δ) < sqrt 1 :=
        Real.sqrt_lt_sqrt (by linarith) (by linarith)
      simpa using this
    nlinarith [Real.sqrt_nonneg (1 - κ * δ)]
  · have h : (1 : ℝ) < sqrt (1 + κ * δ) := by
      have : sqrt 1 < sqrt (1 + κ * δ) :=
        Real.sqrt_lt_sqrt (by norm_num) (by linarith)
      simpa using this
    nlinarith

/-! ## §4 Degeneracy limit -/

/-- T6. At zero coupling the system collapses to the uncoupled mode. -/
theorem triple_degenerate_at_zero_coupling {A γ : ℝ} (hA : 0 < A) (hγ : 0 < γ) :
    lam_triple A γ 0 = A := by
  simp [lam_triple]

/-! ## §5 Bessel ratio -/

/-- T7. Ratio of the first two Bessel zeros. -/
noncomputable def bessel_ratio : ℝ := 7.016 / 3.832

theorem bessel_ratio_def : bessel_ratio = 7.016 / 3.832 := rfl

/-- T8. The ratio lies in `(1.8, 1.9)`, the interval containing the tribonacci
constant η ≈ 1.8393. That the ratio lies in an interval containing η is not a
statement that it equals η, and nothing here defines η. -/
theorem bessel_ratio_in_tribonacci_interval :
    (1.8 : ℝ) < bessel_ratio ∧ bessel_ratio < 1.9 := by
  constructor <;> norm_num [bessel_ratio]

/-! ## §6 Canonical couplings -/

/-- T9. `κ₂₃ = κ₁₂²`. -/
theorem canonical_coupling_ladder : κ₂₃ = κ₁₂ ^ 2 := by
  simp [κ₁₂, κ₂₃, ε₀]

/-!
## OPEN

1. **That κ₁₂ = ε₀.** `κ₁₂` is *defined* to be `ε₀` here. That the physical
   inner-to-transition coupling takes that value is an empirical claim and is
   not in this file. chF-catastrophe.html §1 reads the definition as a result.
2. **That the plasmapause is a Whitney A₁ fold.** Asserted in the header; no
   fold appears in any statement.
3. **η and the Bessel ratio.** T8 places a decimal in an interval. Whether
   `j'₀,₂ / j'₀,₁` is η, or near it for a reason, is untouched.
-/

end dm3.TripleChamber
