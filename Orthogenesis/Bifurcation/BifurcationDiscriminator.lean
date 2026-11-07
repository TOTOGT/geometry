-- GATE-DECLARE: sorries = none
-- GATE-REASON: new file 2026-11-06 for the geometry pin (Lean v4.32.0, Mathlib v4.32.0).
-- UNTESTED until the author runs `lake env lean` on it. Written without a local toolchain.
/-
# BifurcationDiscriminator.lean — the F test of the G-chain table, as algebra

What this file is: the elementary algebra behind two discriminators between a fold
(saddle-node) and the smooth one-parameter bifurcations (transcritical, supercritical
pitchfork, and the Hopf radial equation, which has the pitchfork form). Everything is
one-dimensional and exact: no calculus, no limits, only polynomial identities.

  §1  Saddle-node  x' = μ − x².   Expanding about the stable fixed point √μ:
        f(√μ + h) = −2√μ·h − h².   The linear coefficient (the relaxation rate) is
        −2√μ: it vanishes like the SQUARE ROOT of the distance μ from the fold.
  §2  Transcritical x' = μx − x², and pitchfork/Hopf-radial x' = μx − x³.
        About the stable branch the linear coefficients are −μ and −2μ: they vanish
        LINEARLY in the distance from the bifurcation.
  §3  The discriminator: no constant K bounds the saddle-node rate by K·μ for all
        μ > 0 (`sn_rate_not_linear`), while the pitchfork/Hopf rate is bounded by 2μ
        (`pf_rate_linear`). A 1/2-power of the AMPLITUDE does not discriminate:
        the pitchfork branch also has amplitude √μ (`pf_fixed`).
  §4  The fold algebra of the toy model used in the table,
        x' = r x (1 − x/K) − m x/(h + x): the nonzero fixed points solve
        r(1 − x/K)(h + x) = m, and (1 − x/K)(h + x) = (K+h)²/(4K) − (x − (K−h)/2)²/K,
        so there is no nonzero fixed point once m > r(K+h)²/(4K) (`toy_no_fixed_above`),
        which is 121/40 = 3.025 for r = 1, K = 10, h = 1 (`toy_fold_value`).

What this file does NOT do:
  * It does not say any real system (circadian, neural, viral, cell-cycle, ocean) is
    or is not a fold. Membership of a real system in a normal-form class is an
    empirical claim and is not formalised here.
  * It says nothing about hysteresis, which needs the dynamics of a parameter sweep;
    only the rate exponent and the fixed-point algebra are proved.
  * It is one-dimensional and smooth. The fly-swarm map of BioSwarmCheck.lean is a
    discontinuous discrete map and is NOT covered; a faithful definition of C, K, F, U
    for that chain needs piecewise-smooth maps.
-/

import Mathlib

namespace Orthogenesis.Bifurcation

/-! ## Normal forms -/

/-- Saddle-node (fold): x' = μ − x². -/
def sn (μ x : ℝ) : ℝ := μ - x ^ 2

/-- Transcritical: x' = μx − x². -/
def tc (μ x : ℝ) : ℝ := μ * x - x ^ 2

/-- Supercritical pitchfork; also the Hopf radial equation ṙ = λr − r³. -/
def pf (μ x : ℝ) : ℝ := μ * x - x ^ 3

/-! ## §1 Saddle-node: rate −2√μ -/

theorem sn_fixed {μ : ℝ} (hμ : 0 ≤ μ) : sn μ (Real.sqrt μ) = 0 := by
  unfold sn
  rw [Real.sq_sqrt hμ]
  ring

/-- Exact expansion about the fixed point √μ: f(√μ + h) = −2√μ·h − h². -/
theorem sn_expand {μ : ℝ} (hμ : 0 ≤ μ) (h : ℝ) :
    sn μ (Real.sqrt μ + h) = -2 * Real.sqrt μ * h - h ^ 2 := by
  have hs : Real.sqrt μ ^ 2 = μ := Real.sq_sqrt hμ
  unfold sn
  linear_combination (-1 : ℝ) * hs

/-- The linear coefficient (relaxation rate) of the saddle-node about √μ. -/
noncomputable def snRate (μ : ℝ) : ℝ := -2 * Real.sqrt μ

/-! ## §2 Transcritical and pitchfork/Hopf: rates linear in μ -/

theorem tc_fixed (μ : ℝ) : tc μ μ = 0 := by
  unfold tc
  ring

/-- About the stable branch x = μ: f(μ + h) = −μ·h − h². -/
theorem tc_expand (μ h : ℝ) : tc μ (μ + h) = -μ * h - h ^ 2 := by
  unfold tc
  ring

def tcRate (μ : ℝ) : ℝ := -μ

theorem pf_fixed {μ : ℝ} (hμ : 0 ≤ μ) : pf μ (Real.sqrt μ) = 0 := by
  have hs : Real.sqrt μ ^ 2 = μ := Real.sq_sqrt hμ
  unfold pf
  linear_combination (-(Real.sqrt μ)) * hs

/-- About the stable branch x = √μ: f(√μ + h) = −2μ·h − 3√μ·h² − h³. -/
theorem pf_expand {μ : ℝ} (hμ : 0 ≤ μ) (h : ℝ) :
    pf μ (Real.sqrt μ + h) = -2 * μ * h - 3 * Real.sqrt μ * h ^ 2 - h ^ 3 := by
  have hs : Real.sqrt μ ^ 2 = μ := Real.sq_sqrt hμ
  unfold pf
  linear_combination (-(Real.sqrt μ + 3 * h)) * hs

def pfRate (μ : ℝ) : ℝ := -2 * μ

/-! ## §3 The discriminator -/

/-- No constant K bounds the saddle-node rate by K·μ for all μ > 0: the rate goes to
zero strictly slower than linearly. -/
theorem sn_rate_not_linear :
    ¬ ∃ K : ℝ, ∀ μ : ℝ, 0 < μ → |snRate μ| ≤ K * μ := by
  rintro ⟨K, hK⟩
  obtain ⟨t, htdef⟩ : ∃ t : ℝ, t = |K| + 1 := ⟨_, rfl⟩
  have ht : 0 < t := by rw [htdef]; positivity
  have hμ : 0 < 1 / t ^ 2 := by positivity
  have hs : Real.sqrt (1 / t ^ 2) = 1 / t := by
    rw [show (1 / t ^ 2 : ℝ) = (1 / t) ^ 2 by ring]
    exact Real.sqrt_sq (by positivity)
  have h := hK (1 / t ^ 2) hμ
  have e : |snRate (1 / t ^ 2)| = 2 / t := by
    unfold snRate
    rw [hs, show (-2 : ℝ) * (1 / t) = -(2 / t) by ring, abs_neg]
    exact abs_of_pos (by positivity)
  have h1 : K * (1 / t ^ 2) ≤ |K| * (1 / t ^ 2) :=
    mul_le_mul_of_nonneg_right (le_abs_self K) (by positivity)
  have h2 : |K| * (1 / t ^ 2) < t * (1 / t ^ 2) :=
    mul_lt_mul_of_pos_right (by linarith) (by positivity)
  have h2' : t * (1 / t ^ 2) = 1 / t := by
    field_simp
  have h3 : (1 : ℝ) / t < 2 / t := by
    rw [div_lt_div_iff_of_pos_right ht]
    norm_num
  rw [e] at h
  linarith

/-- The pitchfork/Hopf rate is bounded linearly: |−2μ| ≤ 2μ for μ > 0. -/
theorem pf_rate_linear : ∀ μ : ℝ, 0 < μ → |pfRate μ| ≤ 2 * μ := by
  intro μ hμ
  unfold pfRate
  rw [show (-2 : ℝ) * μ = -(2 * μ) by ring, abs_neg]
  exact le_of_eq (abs_of_pos (by positivity : (0 : ℝ) < 2 * μ))

/-- The transcritical rate is bounded linearly: |−μ| ≤ μ for μ > 0. -/
theorem tc_rate_linear : ∀ μ : ℝ, 0 < μ → |tcRate μ| ≤ μ := by
  intro μ hμ
  unfold tcRate
  rw [abs_neg]
  exact le_of_eq (abs_of_pos hμ)

/-! ## §4 The toy immune model: fold algebra -/

/-- (1 − x/K)(h + x) = (K+h)²/(4K) − (x − (K−h)/2)²/K. -/
theorem toy_peak {K h x : ℝ} (hK : K ≠ 0) :
    (1 - x / K) * (h + x) = (K + h) ^ 2 / (4 * K) - (x - (K - h) / 2) ^ 2 / K := by
  field_simp
  ring

/-- The maximum is attained at x = (K − h)/2. -/
theorem toy_peak_attained {K h : ℝ} (hK : K ≠ 0) :
    (1 - ((K - h) / 2) / K) * (h + (K - h) / 2) = (K + h) ^ 2 / (4 * K) := by
  rw [toy_peak hK]
  simp

/-- Above the peak value there is no fixed point with x ≠ 0 of the toy model:
r(1 − x/K)(h + x) ≠ m whenever m > r(K+h)²/(4K). -/
theorem toy_no_fixed_above {r K h x m : ℝ} (hr : 0 < r) (hK : 0 < K)
    (hm : r * ((K + h) ^ 2 / (4 * K)) < m) :
    r * ((1 - x / K) * (h + x)) ≠ m := by
  intro heq
  rw [toy_peak hK.ne'] at heq
  have hsq : 0 ≤ r * ((x - (K - h) / 2) ^ 2 / K) := by positivity
  have hexp : r * ((K + h) ^ 2 / (4 * K) - (x - (K - h) / 2) ^ 2 / K)
      = r * ((K + h) ^ 2 / (4 * K)) - r * ((x - (K - h) / 2) ^ 2 / K) := by ring
  linarith

/-- r = 1, K = 10, h = 1: the fold value is 121/40 = 3.025. -/
theorem toy_fold_value : (1 : ℝ) * ((10 + 1) ^ 2 / (4 * 10)) = 121 / 40 := by
  norm_num

end Orthogenesis.Bifurcation

#print axioms Orthogenesis.Bifurcation.sn_fixed
#print axioms Orthogenesis.Bifurcation.sn_expand
#print axioms Orthogenesis.Bifurcation.tc_fixed
#print axioms Orthogenesis.Bifurcation.tc_expand
#print axioms Orthogenesis.Bifurcation.pf_fixed
#print axioms Orthogenesis.Bifurcation.pf_expand
#print axioms Orthogenesis.Bifurcation.sn_rate_not_linear
#print axioms Orthogenesis.Bifurcation.pf_rate_linear
#print axioms Orthogenesis.Bifurcation.tc_rate_linear
#print axioms Orthogenesis.Bifurcation.toy_peak
#print axioms Orthogenesis.Bifurcation.toy_peak_attained
#print axioms Orthogenesis.Bifurcation.toy_no_fixed_above
#print axioms Orthogenesis.Bifurcation.toy_fold_value
