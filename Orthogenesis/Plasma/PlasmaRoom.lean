-- GATE-DECLARE: sorries = none
-- GATE-REASON: new file 2026-09-24 for the geometry pin (Lean v4.32.0,
-- Mathlib v4.32.0). Author's lake build 2026-09-24: 27/27 on standard axioms.
/-
# PlasmaRoom.lean — the plasma room of Book 3 (The Mini-Beast)
# ============================================================
# Source chapters (taught path 9–12): ch03-plasma.html (Definitions 3.1–3.3,
# Theorems 3.4–3.5, Falsifiability 3.6), ch09-plasma-metric.html,
# ch10-plasma-xpoint.html, ch11-plasma-transition.html.
#
# What is formalised here, and what is not:
#
#   §1  The dm³ contact normal form with the plasma parameters
#       (μ_max, ω, β) = (−0.42, 0.015, 1.8) of Theorem 3.5: the transverse
#       rate is negative for z > 0 and tends to μ_max; ρ = 0 is invariant.
#   §2  The fractal-dimension formula of Theorem 3.4,
#       d_f = 1 + log|μ_max| / log λ. It lies in (1, 2) exactly when
#       λ < |μ_max| < 1; with λ ≈ 0.6 > 0.42 it exceeds 2, so the printed
#       value 1.43 does not follow from the printed λ. The λ that does give
#       d_f = d is constructed (`lamFor`); for d = 1.43 it is ≈ 0.133
#       (computed, not proved here).
#   §3  X-point and fold (flux-function model). An X-point is a non-degenerate
#       saddle: for ψ = (x² − y²)/2 the Hessian has det −1. It is not a metric
#       (indefinite), which matters for Definition 3.1's g = Hess E. The rank
#       drop belongs to the fold ψ_a = x³/3 − a·x + y²/2: for a > 0 an X-point
#       (−√a, 0) and an O-point (√a, 0); for a < 0 none; at a = 0 they merge
#       with singular Hessian. Morse holds for every a ≠ 0, so Assumption 3.2
#       stays Morse once "the Hessian loses rank at the X-point" is replaced by
#       "the Hessian loses rank at the fold, at reconnection onset".
#   §4  Definition 3.3: focal curvature κ* = min(‖Π‖, √K_sec) — basic facts.
#       The km⁻¹ band 0.8–1.2 × 10⁻³ is a measurement claim; Lean cannot
#       check units or data.
#   §5  Theorem 3.5's parameters belong to the dm³ family (μ < 0, ω > 0,
#       β > 0). Shared functional form only: the cross-room identity claim of
#       the Coherence Bridge was withdrawn in ch20 on 2026-09-19.
#   §6  Falsifiability 3.6(2): an Alfvén-normalised rate v_in / v_A is ≥ 0,
#       so it is a different quantity from μ_max = −0.42 (a transverse
#       Lyapunov exponent) and the two are not expected to match. Which
#       quantity μ_max is here, and how it relates to Vol II's −2, is open;
#       Lean does not settle it.
#
# Not formalised: the MHD energy functional itself, the Cluster/MMS/PSP
# numbers, the 10¹⁵ J energy release, and the identification of plasma β
# (a pressure ratio) with the normal form's β (a z-coupling rate) — the
# chapters make that identification without a derivation.
-/

import Mathlib

namespace Orthogenesis.Plasma

open Real Filter Topology

/-! ## §1 Contact normal form with plasma parameters -/

/-- Parameters (μ_max, ω, β) of the dm³ contact normal form
    ρ̇ = μ(1 − e^{−βz})ρ,  θ̇ = ω,  ż = ω − |μ|ρ²e^{−βz}  (leading order). -/
structure DM3Params where
  mu : ℝ
  omega : ℝ
  beta : ℝ

/-- Theorem 3.5's plasma parameters: μ_max = −0.42, ω = 0.015 rad/s, β = 1.8. -/
noncomputable def plasma : DM3Params := ⟨-0.42, 0.015, 1.8⟩

/-- Transverse rate μ(1 − e^{−βz}) multiplying ρ in ρ̇. -/
noncomputable def transverseRate (p : DM3Params) (z : ℝ) : ℝ :=
  p.mu * (1 - Real.exp (-p.beta * z))

/-- Leading-order normal-form vector field in (ρ, θ, z) coordinates
    (θ̇ does not depend on the state at this order). -/
noncomputable def field (p : DM3Params) (ρ z : ℝ) : ℝ × ℝ × ℝ :=
  (transverseRate p z * ρ, p.omega, p.omega - |p.mu| * ρ ^ 2 * Real.exp (-p.beta * z))

/-- For μ < 0 and β > 0 the transverse rate is strictly negative at every z > 0:
    ρ is contracted there. -/
theorem transverseRate_neg (p : DM3Params) (hmu : p.mu < 0) (hbeta : 0 < p.beta)
    {z : ℝ} (hz : 0 < z) : transverseRate p z < 0 := by
  have hbz : -p.beta * z < 0 := by nlinarith
  have hexp : Real.exp (-p.beta * z) < 1 := by
    have := Real.exp_lt_exp.mpr hbz
    rwa [Real.exp_zero] at this
  unfold transverseRate
  exact mul_neg_of_neg_of_pos hmu (by linarith)

/-- The plasma instance: −0.42(1 − e^{−1.8z}) < 0 for every z > 0. -/
theorem plasma_transverseRate_neg {z : ℝ} (hz : 0 < z) :
    transverseRate plasma z < 0 :=
  transverseRate_neg plasma (by norm_num [plasma]) (by norm_num [plasma]) hz

/-- As z → ∞ the transverse rate tends to μ_max. -/
theorem transverseRate_tendsto (p : DM3Params) (hbeta : 0 < p.beta) :
    Tendsto (transverseRate p) atTop (𝓝 p.mu) := by
  have h1 : Tendsto (fun z : ℝ => p.beta * z) atTop atTop :=
    tendsto_id.const_mul_atTop hbeta
  have h2 : Tendsto (fun z : ℝ => Real.exp (-(p.beta * z))) atTop (𝓝 0) :=
    Real.tendsto_exp_neg_atTop_nhds_zero.comp h1
  have h3 : Tendsto (fun z : ℝ => p.mu * (1 - Real.exp (-(p.beta * z)))) atTop
      (𝓝 (p.mu * (1 - 0))) :=
    (tendsto_const_nhds.sub h2).const_mul p.mu
  rw [sub_zero, mul_one] at h3
  unfold transverseRate
  simpa only [neg_mul] using h3

/-- The plasma instance tends to −0.42. -/
theorem plasma_transverseRate_tendsto :
    Tendsto (transverseRate plasma) atTop (𝓝 (-0.42)) := by
  have := transverseRate_tendsto plasma (by norm_num [plasma])
  simpa [plasma] using this

/-- ρ = 0 is invariant: the ρ-component of the field vanishes there. -/
theorem rho_zero_invariant (p : DM3Params) (z : ℝ) : (field p 0 z).1 = 0 := by
  simp [field]

/-! ## §2 Theorem 3.4: the fractal-dimension formula -/

/-- d_f = 1 + log|μ| / log λ  (Theorem 3.4). -/
noncomputable def fractalDim (mu lam : ℝ) : ℝ := 1 + Real.log |mu| / Real.log lam

/-- If 0 < |μ| < λ < 1 then d_f > 2. -/
theorem fractalDim_gt_two {mu lam : ℝ} (hmu0 : 0 < |mu|) (hlt : |mu| < lam)
    (hlam1 : lam < 1) : 2 < fractalDim mu lam := by
  have hlam0 : 0 < lam := hmu0.trans hlt
  have hl : Real.log lam < 0 := Real.log_neg hlam0 hlam1
  have hm : Real.log |mu| < Real.log lam := Real.log_lt_log hmu0 hlt
  have hdiv : 1 < Real.log |mu| / Real.log lam := (one_lt_div_of_neg hl).mpr hm
  unfold fractalDim
  linarith

/-- If 0 < λ < |μ| < 1 then 1 < d_f < 2: the range of a fractal curve. -/
theorem fractalDim_mem_Ioo {mu lam : ℝ} (hlam0 : 0 < lam) (hlt : lam < |mu|)
    (hmu1 : |mu| < 1) : 1 < fractalDim mu lam ∧ fractalDim mu lam < 2 := by
  have hmu0 : 0 < |mu| := hlam0.trans hlt
  have hl : Real.log lam < 0 := Real.log_neg hlam0 (hlt.trans hmu1)
  have hm0 : Real.log |mu| < 0 := Real.log_neg hmu0 hmu1
  have hm : Real.log lam < Real.log |mu| := Real.log_lt_log hlam0 hlt
  constructor
  · have hpos : 0 < Real.log |mu| / Real.log lam := div_pos_of_neg_of_neg hm0 hl
    unfold fractalDim
    linarith
  · have hlt1 : Real.log |mu| / Real.log lam < 1 := (div_lt_one_of_neg hl).mpr hm
    unfold fractalDim
    linarith

/-- With the printed values μ_max = −0.42 and λ = 0.6, d_f > 2. -/
theorem plasma_fractalDim_gt_two : 2 < fractalDim (-0.42) 0.6 := by
  have habs : |(-0.42 : ℝ)| = 0.42 := by rw [abs_of_neg (by norm_num)]; norm_num
  apply fractalDim_gt_two
  · rw [habs]; norm_num
  · rw [habs]; norm_num
  · norm_num

/-- Hence the printed value d_f ≈ 1.43 does not follow from the printed λ = 0.6. -/
theorem plasma_fractalDim_ne_published : fractalDim (-0.42) 0.6 ≠ 1.43 := by
  intro h
  have := plasma_fractalDim_gt_two
  rw [h] at this
  norm_num at this

/-- The compression ratio that yields a prescribed dimension d:
    λ = exp(log|μ| / (d − 1)). -/
noncomputable def lamFor (mu d : ℝ) : ℝ := Real.exp (Real.log |mu| / (d - 1))

/-- `lamFor` does what it says: d_f(μ, lamFor μ d) = d whenever log|μ| ≠ 0, d ≠ 1.
    For μ = −0.42, d = 1.43 this λ is ≈ 0.133 (numerical, not proved here). -/
theorem fractalDim_lamFor {mu d : ℝ} (hlog : Real.log |mu| ≠ 0) (hd : d ≠ 1) :
    fractalDim mu (lamFor mu d) = d := by
  have hd' : d - 1 ≠ 0 := sub_ne_zero.mpr hd
  unfold fractalDim lamFor
  rw [Real.log_exp]
  field_simp
  ring

/-! ## §3 X-point, fold, and Assumption 3.2

Model computation in the flux function ψ of the reconnection plane (the standard
X-point picture). An X-point is a NON-degenerate saddle of ψ; the Hessian loses
rank only at the fold where a saddle (X-point) and an O-point merge and
annihilate — the onset of reconnection. So Assumption 3.2 can stay Morse: Morse
holds generically, and the fold is the codimension-one exception. Linking this
to the Hessian of E_MHD on the chapter's coordinates (B_z, ρ, T, J) is not done
here. -/

/-- A Hessian with det ≤ 0 is not positive definite, so it is not a Riemannian
    metric at that point (Definition 3.1 uses the Hessian as the metric). -/
theorem det_nonpos_not_posDef {n : Type*} [Fintype n] [DecidableEq n]
    (H : Matrix n n ℝ) (h : H.det ≤ 0) : ¬ H.PosDef := by
  intro hp
  have := hp.det_pos
  linarith

/-- Hessian of the X-point flux ψ = (x² − y²)/2. -/
def xpointHessian : Matrix (Fin 2) (Fin 2) ℝ := !![1, 0; 0, -1]

/-- Its determinant is −1: the X-point is a non-degenerate (Morse) saddle. -/
theorem xpointHessian_det : xpointHessian.det = -1 := by
  rw [xpointHessian, Matrix.det_fin_two_of]
  norm_num

theorem xpointHessian_nondegenerate : xpointHessian.det ≠ 0 := by
  rw [xpointHessian_det]
  norm_num

/-- Being indefinite, it is not a metric: Definition 3.1's g = Hess E fails to be
    Riemannian at a saddle. -/
theorem xpointHessian_not_posDef : ¬ xpointHessian.PosDef :=
  det_nonpos_not_posDef _ (by rw [xpointHessian_det]; norm_num)

/-- Gradient of the fold family ψ_a(x, y) = x³/3 − a·x + y²/2. -/
def foldGrad (a x y : ℝ) : ℝ × ℝ := (x ^ 2 - a, y)

/-- Hessian of the fold family at (x, y): diag(2x, 1). -/
def foldHessian (x : ℝ) : Matrix (Fin 2) (Fin 2) ℝ := !![2 * x, 0; 0, 1]

theorem foldHessian_det (x : ℝ) : (foldHessian x).det = 2 * x := by
  rw [foldHessian, Matrix.det_fin_two_of]
  ring

/-- For a > 0, (√a, 0) and (−√a, 0) are critical points. -/
theorem fold_critical_points {a : ℝ} (ha : 0 < a) :
    foldGrad a (Real.sqrt a) 0 = (0, 0) ∧ foldGrad a (-Real.sqrt a) 0 = (0, 0) := by
  have hs : Real.sqrt a ^ 2 = a := Real.sq_sqrt ha.le
  refine ⟨?_, ?_⟩
  · simp [foldGrad, hs]
  · simp [foldGrad, hs]

/-- For a > 0 the point (−√a, 0) is a non-degenerate saddle: the X-point. -/
theorem fold_xpoint_saddle {a : ℝ} (ha : 0 < a) :
    (foldHessian (-Real.sqrt a)).det < 0 := by
  rw [foldHessian_det]
  have := Real.sqrt_pos.mpr ha
  linarith

/-- For a > 0 the point (√a, 0) has positive-definite Hessian: the O-point. -/
theorem fold_opoint_posdet {a : ℝ} (ha : 0 < a) :
    0 < (foldHessian (Real.sqrt a)).det := by
  rw [foldHessian_det]
  have := Real.sqrt_pos.mpr ha
  linarith

/-- For a < 0 there are no critical points: the X–O pair has annihilated. -/
theorem fold_no_critical {a : ℝ} (ha : a < 0) (x y : ℝ) : foldGrad a x y ≠ (0, 0) := by
  intro h
  have h1 : x ^ 2 - a = 0 := congrArg Prod.fst h
  nlinarith [sq_nonneg x]

/-- At a = 0 the only critical point is the origin, and there the Hessian is
    singular: the fold. -/
theorem fold_degenerate_at_zero {x y : ℝ} (h : foldGrad 0 x y = (0, 0)) :
    x = 0 ∧ y = 0 ∧ (foldHessian x).det = 0 := by
  have h1 : x ^ 2 - 0 = 0 := congrArg Prod.fst h
  have h2 : y = 0 := congrArg Prod.snd h
  have hx : x = 0 := by
    have : x ^ 2 = 0 := by linarith
    exact (pow_eq_zero_iff two_ne_zero).mp this
  refine ⟨hx, h2, ?_⟩
  rw [foldHessian_det, hx]
  ring

/-- Assumption 3.2, consistent form: for every a ≠ 0 every critical point of ψ_a
    is non-degenerate. The rank drop happens only at a = 0. -/
theorem fold_generic_morse {a : ℝ} (ha : a ≠ 0) {x y : ℝ}
    (h : foldGrad a x y = (0, 0)) : (foldHessian x).det ≠ 0 := by
  have h1 : x ^ 2 - a = 0 := congrArg Prod.fst h
  rw [foldHessian_det]
  intro hx
  have hx0 : x = 0 := by linarith
  rw [hx0] at h1
  norm_num at h1
  exact ha (by linarith)

/-! ## §4 Definition 3.3: focal curvature -/

/-- κ* = min(‖Π‖, √K_sec), with ‖Π‖ the norm of the second fundamental form and
    K_sec the sectional curvature at the point. -/
noncomputable def focalCurvature (secondFF sectional : ℝ) : ℝ :=
  min secondFF (Real.sqrt sectional)

theorem focalCurvature_le_secondFF (a K : ℝ) : focalCurvature a K ≤ a := min_le_left _ _

theorem focalCurvature_le_sqrt (a K : ℝ) : focalCurvature a K ≤ Real.sqrt K :=
  min_le_right _ _

theorem focalCurvature_pos {a K : ℝ} (ha : 0 < a) (hK : 0 < K) :
    0 < focalCurvature a K :=
  lt_min ha (Real.sqrt_pos.mpr hK)

/-! ## §5 Membership of the dm³ family -/

/-- The sign conditions of a contracting dm³ normal form. -/
def InFamily (p : DM3Params) : Prop := p.mu < 0 ∧ 0 < p.omega ∧ 0 < p.beta

/-- Theorem 3.5's plasma parameters satisfy them. -/
theorem plasma_inFamily : InFamily plasma := by
  refine ⟨?_, ?_, ?_⟩ <;> norm_num [plasma]

/-! ## §6 Falsifiability 3.6(2): sign of a measured reconnection rate -/

/-- Alfvén-normalised reconnection rate R = v_in / v_A (inflow speed over
    Alfvén speed), the quantity reported by MMS event studies. -/
noncomputable def alfvenRate (vin vA : ℝ) : ℝ := vin / vA

theorem alfvenRate_nonneg {vin vA : ℝ} (hin : 0 ≤ vin) (hA : 0 < vA) :
    0 ≤ alfvenRate vin vA :=
  div_nonneg hin hA.le

/-- An Alfvén-normalised rate cannot equal μ_max = −0.42. So μ_max is the
    transverse (Lyapunov) exponent of the normal form, and testing prediction (2)
    against MMS rates requires a stated map from μ_max to the measured rate. -/
theorem alfvenRate_ne_plasma_mu {vin vA : ℝ} (hin : 0 ≤ vin) (hA : 0 < vA) :
    alfvenRate vin vA ≠ plasma.mu := by
  intro h
  have := alfvenRate_nonneg hin hA
  rw [h] at this
  norm_num [plasma] at this

end Orthogenesis.Plasma

/-! ## Axiom probe -/
#print axioms Orthogenesis.Plasma.transverseRate_neg
#print axioms Orthogenesis.Plasma.plasma_transverseRate_neg
#print axioms Orthogenesis.Plasma.transverseRate_tendsto
#print axioms Orthogenesis.Plasma.plasma_transverseRate_tendsto
#print axioms Orthogenesis.Plasma.rho_zero_invariant
#print axioms Orthogenesis.Plasma.fractalDim_gt_two
#print axioms Orthogenesis.Plasma.fractalDim_mem_Ioo
#print axioms Orthogenesis.Plasma.plasma_fractalDim_gt_two
#print axioms Orthogenesis.Plasma.plasma_fractalDim_ne_published
#print axioms Orthogenesis.Plasma.fractalDim_lamFor
#print axioms Orthogenesis.Plasma.det_nonpos_not_posDef
#print axioms Orthogenesis.Plasma.xpointHessian_det
#print axioms Orthogenesis.Plasma.xpointHessian_nondegenerate
#print axioms Orthogenesis.Plasma.xpointHessian_not_posDef
#print axioms Orthogenesis.Plasma.foldHessian_det
#print axioms Orthogenesis.Plasma.fold_critical_points
#print axioms Orthogenesis.Plasma.fold_xpoint_saddle
#print axioms Orthogenesis.Plasma.fold_opoint_posdet
#print axioms Orthogenesis.Plasma.fold_no_critical
#print axioms Orthogenesis.Plasma.fold_degenerate_at_zero
#print axioms Orthogenesis.Plasma.fold_generic_morse
#print axioms Orthogenesis.Plasma.focalCurvature_le_secondFF
#print axioms Orthogenesis.Plasma.focalCurvature_le_sqrt
#print axioms Orthogenesis.Plasma.focalCurvature_pos
#print axioms Orthogenesis.Plasma.plasma_inFamily
#print axioms Orthogenesis.Plasma.alfvenRate_nonneg
#print axioms Orthogenesis.Plasma.alfvenRate_ne_plasma_mu
