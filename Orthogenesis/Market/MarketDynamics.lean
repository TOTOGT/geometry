-- GATE-DECLARE: sorries = none
-- GATE-REASON: new file 2026-09-25 for the geometry pin (Lean v4.32.0,
-- Mathlib v4.32.0). Author's first build 2026-09-25: one error (a `ring` with no goal
-- left after `field_simp`), removed. Rebuild 2026-09-25: 12/12 on standard axioms, no warnings.
/-
# MarketDynamics.lean — market dynamics in Book 3 (The Mini-Beast)
# ================================================================
# Source chapters (taught path 13–16): ch04-markets.html (Definition 4.1,
# Assumption 4.2, Theorems 4.3–4.4, Falsifiability 4.5, the 2010 case study),
# ch13-market-metric.html, ch14-market-threshold.html,
# ch15-market-transition.html. Builds on Orthogenesis/Plasma/PlasmaRoom.lean.
#
#   §1  Theorem 4.4's parameters (μ_max, ω, β) = (−0.67, 0.28, 2.4): the
#       transverse rate is negative for z > 0 and tends to −0.67.
#   §2  Fold time τ_fold = π/ω: at ω = 0.28 rad/day it lies in (11.2, 11.25)
#       days, matching the chapter's "≈ 11.2 days". The intraday ω is not
#       pinned by the chapters, so the 22-minute figure is not checked here.
#   §3  d_f. The chapters say d_f is set by μ_max and the compression ratio λ,
#       as in the plasma room, but state no λ. With the plasma room's printed
#       λ = 0.6, d_f = 1 + log 0.67 / log 0.6 ≈ 1.78 lies in the printed band
#       (1.7, 1.9). (The same λ with the plasma μ_max = −0.42 gives d_f > 2.)
#   §4  Theorem 4.3's spectrum α(q) = d_f + (q − 1)·τ(q)/q is not the standard
#       multifractal relation α = dτ/dq: for a monofractal, τ(q) = (q − 1)D,
#       the standard α is the constant D while the chapter's formula varies
#       with q (d_f at q = 1, d_f + D/2 at q = 2).
#   §5  Definition 4.1: the Fisher quadratic form E[(s·v)²] is ≥ 0 — the
#       Fisher metric is positive semidefinite by construction (unlike the
#       plasma room's Hessian-as-metric at a saddle). The chapters' units
#       argument holds: ds² is dimensionless, so its curvature — and the band
#       0.12–0.18 — is unit-free. Lean does not check units; this is a note.
#   §6  ch14's backtest proxy κ = |σ''| / |σ'| is a different quantity: under
#       a change of time unit t ↦ c·t it scales by c. Its threshold band
#       therefore depends on the time unit (per minute vs per day: ×1440).
#   §7  Falsifiability 4.5(3): a decay envelope e^{μ t} with μ < 0 halves at
#       t = ln 2 / |μ|; for μ_max = −0.67 that is ≈ 1.03 in the (unstated)
#       time unit of μ_max.
#
# Not formalised: the TAQ / Binance / options data, the event timings, and
# the liquidity functional L itself. Assumption 4.2 has the same shape as
# the plasma room's: read as "Morse except at the fold, at crash onset",
# PlasmaRoom's `fold_generic_morse` is the relevant statement.
-/

import Orthogenesis.Plasma.PlasmaRoom

namespace Orthogenesis.MarketDynamics

open Real Filter Topology Orthogenesis.Plasma

/-! ## §1 Theorem 4.4 parameters -/

/-- Theorem 4.4: μ_max = −0.67, ω = 0.28 rad/day, β = 2.4. -/
noncomputable def market : DM3Params := ⟨-0.67, 0.28, 2.4⟩

theorem market_omega : market.omega = 0.28 := rfl

theorem market_inFamily : InFamily market := by
  refine ⟨?_, ?_, ?_⟩ <;> norm_num [market]

theorem market_transverseRate_neg {z : ℝ} (hz : 0 < z) :
    transverseRate market z < 0 :=
  transverseRate_neg market (by norm_num [market]) (by norm_num [market]) hz

theorem market_transverseRate_tendsto :
    Tendsto (transverseRate market) atTop (𝓝 (-0.67)) := by
  have := transverseRate_tendsto market (by norm_num [market])
  simpa [market] using this

/-! ## §2 Fold time -/

/-- τ_fold = π / ω. -/
noncomputable def foldTime (ω : ℝ) : ℝ := π / ω

/-- At ω = 0.28 rad/day the fold time lies in (11.2, 11.25) days. -/
theorem market_foldTime_bounds : 11.2 < foldTime 0.28 ∧ foldTime 0.28 < 11.25 := by
  have h1 := Real.pi_gt_d2
  have h2 := Real.pi_lt_d2
  unfold foldTime
  constructor
  · rw [lt_div_iff₀ (by norm_num)]
    linarith
  · rw [div_lt_iff₀ (by norm_num)]
    linarith

/-! ## §3 Fractal dimension with the plasma room's λ -/

/-- With λ = 0.6 (the plasma room's printed compression ratio; the market
    chapters state none), d_f(−0.67, 0.6) lies in the printed band (1.7, 1.9). -/
theorem market_fractalDim_in_band :
    1.7 < fractalDim (-0.67) 0.6 ∧ fractalDim (-0.67) 0.6 < 1.9 := by
  have habs : |(-0.67 : ℝ)| = 0.67 := by rw [abs_of_neg (by norm_num)]; norm_num
  have hL : Real.log 0.6 < 0 := Real.log_neg (by norm_num) (by norm_num)
  -- 0.6⁹ < 0.67¹⁰  ⟹  9·log 0.6 < 10·log 0.67
  have hA : 9 * Real.log 0.6 < 10 * Real.log 0.67 := by
    have h := Real.log_lt_log (by positivity : (0 : ℝ) < 0.6 ^ 9)
      (by norm_num : (0.6 : ℝ) ^ 9 < 0.67 ^ 10)
    rw [Real.log_pow, Real.log_pow] at h
    push_cast at h
    linarith
  -- 0.67¹⁰ < 0.6⁷  ⟹  10·log 0.67 < 7·log 0.6
  have hB : 10 * Real.log 0.67 < 7 * Real.log 0.6 := by
    have h := Real.log_lt_log (by positivity : (0 : ℝ) < 0.67 ^ 10)
      (by norm_num : (0.67 : ℝ) ^ 10 < 0.6 ^ 7)
    rw [Real.log_pow, Real.log_pow] at h
    push_cast at h
    linarith
  unfold fractalDim
  rw [habs]
  constructor
  · have : 0.7 < Real.log 0.67 / Real.log 0.6 := by
      rw [lt_div_iff_of_neg hL]
      linarith
    linarith
  · have : Real.log 0.67 / Real.log 0.6 < 0.9 := by
      rw [div_lt_iff_of_neg hL]
      linarith
    linarith

/-! ## §4 Theorem 4.3's spectrum formula -/

/-- The chapter's formula α(q) = d_f + (q − 1)·τ(q)/q. -/
noncomputable def chapterAlpha (df : ℝ) (tau : ℝ → ℝ) (q : ℝ) : ℝ :=
  df + (q - 1) * tau q / q

theorem chapterAlpha_one (df : ℝ) (tau : ℝ → ℝ) : chapterAlpha df tau 1 = df := by
  simp [chapterAlpha]

/-- For a monofractal τ(q) = (q − 1)·D with D ≠ 0, the chapter's α varies with q. -/
theorem chapterAlpha_monofractal_varies (df D : ℝ) (hD : D ≠ 0) :
    chapterAlpha df (fun q => (q - 1) * D) 2 ≠ chapterAlpha df (fun q => (q - 1) * D) 1 := by
  intro h
  simp only [chapterAlpha] at h
  ring_nf at h
  apply hD
  linarith

/-- The standard relation α = dτ/dq gives the constant D for the same monofractal. -/
theorem monofractal_legendre_alpha (D q : ℝ) :
    HasDerivAt (fun q : ℝ => (q - 1) * D) D q := by
  have := ((hasDerivAt_id q).sub_const 1).mul_const D
  simpa using this

/-! ## §5 Definition 4.1: the Fisher form is positive semidefinite -/

/-- Fisher quadratic form of a finite family with probabilities p and scores s:
    v ↦ E[(s · v)²] = Σ_k p_k (Σ_i s_{k i} v_i)², i.e. vᵀ E[s sᵀ] v. -/
def fisherForm {K n : Type*} [Fintype K] [Fintype n] (p : K → ℝ) (s : K → n → ℝ)
    (v : n → ℝ) : ℝ :=
  ∑ k, p k * (∑ i, s k i * v i) ^ 2

theorem fisherForm_nonneg {K n : Type*} [Fintype K] [Fintype n] (p : K → ℝ)
    (hp : ∀ k, 0 ≤ p k) (s : K → n → ℝ) (v : n → ℝ) : 0 ≤ fisherForm p s v :=
  Finset.sum_nonneg (fun k _ => mul_nonneg (hp k) (sq_nonneg _))

/-! ## §6 The backtest curvature proxy depends on the time unit -/

/-- ch14's proxy κ = |σ''| / |σ'|, from the first and second time derivatives. -/
noncomputable def curvProxy (d1 d2 : ℝ) : ℝ := |d2| / |d1|

/-- Under t ↦ c·t the derivatives scale as σ' ↦ c·σ', σ'' ↦ c²·σ'', and the
    proxy scales by c: its band depends on the time unit. -/
theorem curvProxy_rescale {c : ℝ} (hc : 0 < c) (d1 d2 : ℝ) (hd1 : d1 ≠ 0) :
    curvProxy (c * d1) (c ^ 2 * d2) = c * curvProxy d1 d2 := by
  have h1 : |d1| ≠ 0 := abs_ne_zero.mpr hd1
  unfold curvProxy
  rw [abs_mul, abs_mul, abs_of_pos hc, abs_of_pos (by positivity : 0 < c ^ 2)]
  field_simp

/-! ## §7 Half-life of the decay envelope -/

/-- Half-life ln 2 / |μ| of the envelope e^{μ t}. -/
noncomputable def halfLife (mu : ℝ) : ℝ := Real.log 2 / |mu|

theorem exp_halfLife {mu : ℝ} (hmu : mu < 0) : Real.exp (mu * halfLife mu) = 1 / 2 := by
  have hne : mu ≠ 0 := hmu.ne
  unfold halfLife
  rw [abs_of_neg hmu]
  have h : mu * (Real.log 2 / -mu) = -Real.log 2 := by
    field_simp
  rw [h, Real.exp_neg, Real.exp_log (by norm_num)]
  norm_num

end Orthogenesis.MarketDynamics

/-! ## Axiom probe -/
#print axioms Orthogenesis.MarketDynamics.market_omega
#print axioms Orthogenesis.MarketDynamics.market_inFamily
#print axioms Orthogenesis.MarketDynamics.market_transverseRate_neg
#print axioms Orthogenesis.MarketDynamics.market_transverseRate_tendsto
#print axioms Orthogenesis.MarketDynamics.market_foldTime_bounds
#print axioms Orthogenesis.MarketDynamics.market_fractalDim_in_band
#print axioms Orthogenesis.MarketDynamics.chapterAlpha_one
#print axioms Orthogenesis.MarketDynamics.chapterAlpha_monofractal_varies
#print axioms Orthogenesis.MarketDynamics.monofractal_legendre_alpha
#print axioms Orthogenesis.MarketDynamics.fisherForm_nonneg
#print axioms Orthogenesis.MarketDynamics.curvProxy_rescale
#print axioms Orthogenesis.MarketDynamics.exp_halfLife
