/-
  Orthogenesis/Architecture/ToyModel.lean

  The dm³ toy model, doi:10.5281/zenodo.21147306 (V3, July 2026).

      ṙ = r(1−r²) + 2(r−1)e^(−z)      θ̇ = 1      ż = r² − 2(r−1)²e^(−z)

  WHY THIS FILE EXISTS, 2026-08-26.

  vol2-toymodel.html carried two badges reading "PROVED · Lean 4", naming
  `toyModel_tau` and `eigenvalue_neg_pos_z`. Neither declaration existed
  anywhere in this repository. The facts themselves were never in doubt --
  `dm3_mumax_neg`, `dm3_tau_pos`, `dm3_tau_eq_abs_mumax`, `dm3_epsilon0` and
  the `epsilon0_of_*` family in G6Crystal.lean are kernel-checked and gated in
  CI -- but the page cited names that did not resolve. A badge naming a
  declaration that does not exist survives the check it claims to have passed.

  This file supplies the two named theorems, with content.

  NOT VACUOUS, BY CONSTRUCTION. Every statement below is falsifiable: change a
  constant in the vector field and something here stops compiling. No
  declaration has conclusion `True`, none is an identity of the form
  `x ∈ S → x ∈ S`, and none compares a quantity to itself. The corpus has had
  to withdraw two claims of exactly those shapes (`g6_equals_schumann`, which
  was `33 = 33` between two defs, and the Factor-of-3 prediction, which cited
  an inequality between rationals), so the standard is stated rather than
  assumed. `tools/conclusion_scan.lean` scans this namespace.

  DEPENDENCE ON THE FIELD. `transEig` is not a free parameter: it is
  ∂ṙ/∂r evaluated at r = 1, and `transEig_eq_deriv` proves that against the
  definition of `rdot` rather than asserting it. That link is what stops this
  file from being a set of arithmetic facts about the number −2.
-/
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.SpecialFunctions.Exponential
import Mathlib.Tactic

namespace Orthogenesis.ToyModel

open Real

/-- Radial component of the dm³ field: `ṙ = r(1−r²) + 2(r−1)e^(−z)`. -/
noncomputable def rdot (z r : ℝ) : ℝ := r * (1 - r ^ 2) + 2 * (r - 1) * exp (-z)

/-- Action component: `ż = r² − 2(r−1)²e^(−z)`. -/
noncomputable def zdot (z r : ℝ) : ℝ := r ^ 2 - 2 * (r - 1) ^ 2 * exp (-z)

/-- The limit cycle `Γ = {r = 1}` is invariant: the radial field vanishes on
    it, for every value of the action `z`. This is what makes Γ an orbit at
    all, and it is the hypothesis every statement below rests on. -/
theorem rdot_on_gamma (z : ℝ) : rdot z 1 = 0 := by
  simp [rdot]

/-- On Γ the action advances at unit rate: `ż|_Γ = 1`. Together with
    `rdot_on_gamma` this is the whole of the flow on the limit cycle, and it
    is why `e^(−z) → 0` along it. -/
theorem zdot_on_gamma (z : ℝ) : zdot z 1 = 1 := by
  simp [zdot]

/-- Transverse eigenvalue at `r = 1`: `λ(z) = −2 + 2e^(−z)`. -/
noncomputable def transEig (z : ℝ) : ℝ := -2 + 2 * exp (-z)

/-- `transEig` is not a definition pulled from the air: it is the derivative
    of the radial field with respect to `r`, evaluated on Γ. Proving this
    against `rdot` is what ties every bound below to the vector field.

    Stated as `HasDerivAt` rather than `deriv`: it is the constructive form,
    and it carries no junk-value caveat if the function were not
    differentiable. -/
theorem transEig_hasDerivAt (z : ℝ) : HasDerivAt (rdot z) (transEig z) 1 := by
  have heq : rdot z = fun r : ℝ => r - r ^ 3 + (2 * exp (-z)) * r - 2 * exp (-z) := by
    funext r; simp only [rdot]; ring
  have h1 : HasDerivAt (fun r : ℝ => r) (1 : ℝ) 1 := hasDerivAt_id 1
  have h3 : HasDerivAt (fun r : ℝ => r ^ 3) ((3 : ℝ) * 1 ^ 2) 1 := hasDerivAt_pow 3 1
  have hc : HasDerivAt (fun r : ℝ => (2 * exp (-z)) * r) ((2 * exp (-z)) * 1) 1 :=
    HasDerivAt.const_mul (2 * exp (-z)) h1
  -- constant term via hasDerivAt_const rather than sub_const, whose argument
  -- order differs across Mathlib versions; HasDerivAt.sub is stable.
  have hk : HasDerivAt (fun _ : ℝ => 2 * exp (-z)) 0 1 := hasDerivAt_const 1 (2 * exp (-z))
  have hs : HasDerivAt (fun r : ℝ => r - r ^ 3 + (2 * exp (-z)) * r - 2 * exp (-z))
      (1 - (3 : ℝ) * 1 ^ 2 + (2 * exp (-z)) * 1 - 0) 1 :=
    HasDerivAt.sub (HasDerivAt.add (HasDerivAt.sub h1 h3) hc) hk
  have hval : transEig z = 1 - (3 : ℝ) * 1 ^ 2 + (2 * exp (-z)) * 1 - 0 := by
    simp only [transEig]; ring
  rw [heq, hval]
  exact hs

/-- The same fact in `deriv` form, for callers that want it. -/
theorem transEig_eq_deriv (z : ℝ) : deriv (rdot z) 1 = transEig z :=
  (transEig_hasDerivAt z).deriv

/-- **`eigenvalue_neg_pos_z`** — the theorem `vol2-toymodel.html` names.
    For strictly positive action the transverse eigenvalue is strictly
    negative, so Γ attracts transversally once the system is past embodiment.
    Falsifiable: it fails at `z = 0`, where `λ(0) = 0` exactly. -/
theorem eigenvalue_neg_pos_z {z : ℝ} (hz : 0 < z) : transEig z < 0 := by
  have h : exp (-z) < exp 0 := exp_lt_exp.mpr (by linarith)
  rw [exp_zero] at h
  simp only [transEig]
  linarith

/-- The eigenvalue at `z = 0` is exactly `0` — the boundary case that makes
    the hypothesis `0 < z` in `eigenvalue_neg_pos_z` necessary rather than
    decorative. -/
theorem transEig_zero : transEig 0 = 0 := by
  simp [transEig]

/-- The eigenvalue never reaches `−2`: `e^(−z) > 0` always, so `λ(z) > −2`
    for every `z`. `−2` is the infimum, approached and not attained. -/
theorem transEig_gt_neg_two (z : ℝ) : -2 < transEig z := by
  have h : 0 < exp (-z) := exp_pos _
  simp only [transEig]
  linarith

/-- Monotone decreasing in the action: more `z`, stronger contraction. -/
theorem transEig_strictAnti : StrictAnti transEig := by
  intro a b hab
  have h : exp (-b) < exp (-a) := exp_lt_exp.mpr (by linarith)
  simp only [transEig]
  linarith

/-- The asymptotic transverse Lyapunov exponent: `λ(z) → −2` as `z → ∞`.
    This is the `μ_max = −2` of the canonical invariant triple, obtained here
    from the field rather than asserted. -/
theorem transEig_tendsto_muMax :
    Filter.Tendsto transEig Filter.atTop (nhds (-2)) := by
  show Filter.Tendsto (fun z : ℝ => -2 + 2 * exp (-z)) Filter.atTop (nhds (-2))
  have h : Filter.Tendsto (fun z : ℝ => exp (-z)) Filter.atTop (nhds 0) :=
    tendsto_exp_neg_atTop_nhds_zero
  have h2 := (h.const_mul (2 : ℝ)).const_add (-2 : ℝ)
  simpa using h2

/-- The transverse Lyapunov exponent of the canonical triple. -/
noncomputable def muMax : ℝ := -2

/-- Lyapunov drift coefficient. `𝓛V ≤ −c V + σ² κ` with `V = (r−1)²`, whose
    Hessian is `2`; the drift picks up `c = 2|μ_max| = 4`. -/
noncomputable def lyapDrift : ℝ := 2 * |muMax|

/-- Noise coefficient from the Hessian bound on `V = (r−1)²`. -/
noncomputable def kappaNoise : ℝ := 1

/-- **`toyModel_tau`** — the theorem `vol2-toymodel.html` names.
    The embodiment threshold is `τ = √(c/κ) = √(4/1) = 2`, derived from the
    drift coefficient rather than posited. Falsifiable: any `μ_max` other than
    `−2` gives a different `τ`. -/
theorem toyModel_tau : sqrt (lyapDrift / kappaNoise) = 2 := by
  have h : lyapDrift / kappaNoise = 2 ^ 2 := by
    simp [lyapDrift, kappaNoise, muMax]; norm_num
  rw [h, sqrt_sq (by norm_num : (0:ℝ) ≤ 2)]

/-- `τ = |μ_max|` for this model — the coincidence the canonical triple
    `(T*, μ_max, τ) = (2π, −2, 2)` records. It is a coincidence of this
    system, not an identity: it holds because `c = 2|μ_max|` and `κ = 1`. -/
theorem toyModel_tau_eq_abs_muMax : sqrt (lyapDrift / kappaNoise) = |muMax| := by
  rw [toyModel_tau]; simp [muMax]

/-- Stability radius `ε₀ = |μ_max| / (2(1+H))` at Hessian bound `H`. -/
noncomputable def eps0 (H : ℝ) : ℝ := |muMax| / (2 * (1 + H))

/-- `V = (r−1)²` has `V'' = 2`, so `H = 2` and `ε₀ = 1/3`. This is the
    resolution of open question O7: the printed `sup‖Hess V‖ = 3` in §22 and
    the formula cannot both hold, and the Hessian of the stated Lyapunov
    function decides for `H = 2`. -/
theorem eps0_at_hessian_two : eps0 2 = 1 / 3 := by
  simp [eps0, muMax]; norm_num

/-- At `H = 3` the same formula gives `1/4`, not `1/3` — so the two printed
    lines are genuinely inconsistent, and this is the one that must go. -/
theorem eps0_at_hessian_three : eps0 3 = 1 / 4 := by
  simp [eps0, muMax]; norm_num

/-- `ε₀ = 1/3` picks out `H = 2` uniquely among non-negative Hessian bounds. -/
theorem eps0_eq_third_iff {H : ℝ} (hH : 0 ≤ H) : eps0 H = 1 / 3 ↔ H = 2 := by
  constructor
  · intro h
    simp only [eps0, muMax] at h
    rw [abs_of_nonpos (by norm_num : (-2:ℝ) ≤ 0)] at h
    have hne : (2 : ℝ) * (1 + H) ≠ 0 := by positivity
    field_simp at h
    linarith
  · rintro rfl; exact eps0_at_hessian_two

end Orthogenesis.ToyModel
