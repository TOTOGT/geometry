/-
  StabilityRadius.lean
  Principia Orthogona · Volume II · Contact Realization
  The two quantities called mu, and the constant epsilon_0 = 1/3 that nothing derives.

  WHY THIS FILE EXISTS, STATED FIRST.
  -----------------------------------
  On 2026-09-19 an audit of the base layer found that `mu` names two different
  objects in this corpus, four lines apart in PrincipiaVol1.lean, and that
  Proposition 4.4 of Book II computes epsilon_0 = 1/3 from a quantity it never
  derives. Neither is a mistake in the arithmetic. Both are unstated hypotheses
  sitting inside expressions that read like derivations -- rule R20.

  This file makes the dependency machine-visible. It does NOT prove
  epsilon_0 = 1/3. It proves epsilon_0 = 1/3 IF AND ONLY IF the Hessian bound
  is 2, which is the honest content of Proposition 4.4 as currently written.

  WHAT IS PROVED HERE
  -------------------
    §1  the cubic potential and its Morse data: V''(1) = 6, so -V''(1)/2 = -3
    §2  the normal-form radial coefficient DECREASES to -2 and never attains it
    §3  the two are different functions of different arguments
    §4  epsilon_0 as a function of the Hessian bound S, and the two values
          S = 2  ->  epsilon_0 = 1/3   (what Prop 4.4 uses)
          S = 6  ->  epsilon_0 = 1/7   (what V''(1) would give)
    §5  tau * epsilon_0 = 2/3  holds exactly when S = 2

  WHAT IS NOT PROVED HERE
  -----------------------
  That S = 2. Nothing in this corpus derives it. Book II's V in
  `sup ||Hess V||` is a stochastic Lyapunov function (Theorem 3.2:
  L V <= -cV + kappa_noise ||sigma||^2, kappa_noise = (1/2) sup ||Hess V||),
  while PrincipiaVol1's V is the cubic potential q^3 - 3q. They are different
  functions wearing the same letter. Until one page says which V carries the
  bound and where 2 comes from, epsilon_0 = 1/3 is an input.

  STATUS: not built on the desk that wrote it. CI is the judge.
-/
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Analysis.SpecialFunctions.Pow.NNRpow

namespace PrincipiaOrthogona.VolII

open Real

/-! ## §1  The cubic potential, and the Morse quantity -/

/-- The potential of PrincipiaVol1.lean. -/
noncomputable def V (q : ℝ) : ℝ := q ^ 3 - 3 * q
/-- Its first derivative. -/
noncomputable def V' (q : ℝ) : ℝ := 3 * q ^ 2 - 3
/-- Its second derivative. -/
noncomputable def V'' (q : ℝ) : ℝ := 6 * q

theorem V'_at_one : V' 1 = 0 := by unfold V'; norm_num

theorem V''_at_one : V'' 1 = 6 := by unfold V''; norm_num

/-- The Morse quantity at the critical point. This is `mu_canonical`, and it is
    **minus three**. -/
theorem morse_quantity_at_one : -(V'' 1) / 2 = -3 := by
  rw [V''_at_one]; norm_num

/-- `V` has a second critical point, and the Morse quantity there is `+3`. The
    sign is carried by the critical point, not by the system. -/
theorem V'_at_neg_one : V' (-1) = 0 := by unfold V'; norm_num

theorem morse_quantity_at_neg_one : -(V'' (-1)) / 2 = 3 := by
  unfold V''; norm_num

/-! ## §2  The normal-form radial coefficient

Proposition 4.3 of Book II gives the radial equation

    rho' = -2 (1 - exp (-z)) rho + O(rho^2)

so the coefficient is a **function of z**, not a constant. -/

/-- The radial coefficient of the contact normal form. -/
noncomputable def radialCoeff (z : ℝ) : ℝ := -2 * (1 - exp (-z))

/-- At `z = 0` the coefficient vanishes: on the contact hypersurface there is no
    radial contraction at all. -/
theorem radialCoeff_at_zero : radialCoeff 0 = 0 := by
  unfold radialCoeff; simp

/-- For every finite `z`, the coefficient is **strictly greater than −2**. The
    value −2 is a limit and is never attained. -/
theorem radialCoeff_gt_neg_two (z : ℝ) : -2 < radialCoeff z := by
  unfold radialCoeff
  have h : 0 < exp (-z) := exp_pos _
  nlinarith

/-- The coefficient is `0` at `z = 0` and falls toward `-2`; it is strictly
    negative for `z > 0`, so the flow does contract. -/
theorem radialCoeff_neg_of_pos {z : ℝ} (hz : 0 < z) : radialCoeff z < 0 := by
  unfold radialCoeff
  have h : exp (-z) < 1 := by
    rw [exp_lt_one_iff]; linarith
  nlinarith

/-! ## §3  The two quantities are different

`morse_quantity_at_one` is `-3`, a number. `radialCoeff` is a function of `z`
bounded strictly below by `-2`. No value of `z` makes them equal. -/

theorem morse_ne_radialCoeff (z : ℝ) : radialCoeff z ≠ -(V'' 1) / 2 := by
  rw [morse_quantity_at_one]
  have := radialCoeff_gt_neg_two z
  intro h; rw [h] at this; norm_num at this

/-! ## §4  The stability radius, as a function of what it depends on

Proposition 4.4 of Book II reads

    epsilon_0 = |mu_max| / (2 (1 + sup_Gamma ||Hess V||))

With `|mu_max| = 2` this is a function of the Hessian bound alone. -/

/-- The stability radius as Proposition 4.4 defines it, with `S` the Hessian
    bound left as an argument rather than silently fixed. -/
noncomputable def epsilon0 (S : ℝ) : ℝ := 2 / (2 * (1 + S))

/-- **The value Proposition 4.4 actually uses.** -/
theorem epsilon0_at_two : epsilon0 2 = 1 / 3 := by
  unfold epsilon0; norm_num

/-- **The value `V''(1) = 6` would give**, if the `V` of Proposition 4.4 were
    the cubic potential of §1. It is not `1/3`. -/
theorem epsilon0_at_six : epsilon0 6 = 1 / 7 := by
  unfold epsilon0; norm_num

/-- And `1/3` pins `S` uniquely: there is no other Hessian bound consistent with
    the published constant. -/
theorem epsilon0_eq_third_iff {S : ℝ} (hS : 1 + S ≠ 0) :
    epsilon0 S = 1 / 3 ↔ S = 2 := by
  unfold epsilon0
  constructor
  · intro h
    field_simp at h
    linarith
  · rintro rfl; norm_num

/-! ## §5  Noise tolerance

`noiseTolerance` in PrincipiaVol1.lean proves `tau * stabilityRadius = 2/3`
from `stabilityRadius := 1/3`, which is a definition. Here the same product is
computed from `S`, so the dependence is visible. -/

/-- The canonical `tau`. -/
noncomputable def tau : ℝ := 2

theorem noiseTolerance_iff {S : ℝ} (hS : 1 + S ≠ 0) :
    tau * epsilon0 S = 2 / 3 ↔ S = 2 := by
  unfold tau
  constructor
  · intro h
    have : epsilon0 S = 1 / 3 := by linarith
    exact (epsilon0_eq_third_iff hS).mp this
  · rintro rfl
    rw [epsilon0_at_two]; norm_num

/-- Book II's Theorem 3.2 sets `kappa_noise = (1/2) sup ||Hess V||`. Under the
    same `S = 2` that Proposition 4.4 needs, `kappa_noise = 1`, and then
    `tau = sqrt (c / kappa_noise) = 2` forces `c = 4`. Recorded as an
    implication, not as a fact: `c = 4` appears nowhere in the corpus. -/
noncomputable def kappaNoise (S : ℝ) : ℝ := S / 2

theorem kappaNoise_at_two : kappaNoise 2 = 1 := by unfold kappaNoise; norm_num

theorem c_forced_of_tau_two {c : ℝ} (hc : 0 ≤ c)
    (h : Real.sqrt (c / kappaNoise 2) = 2) : c = 4 := by
  rw [kappaNoise_at_two] at h
  have hdiv : c / 1 = c := by ring
  rw [hdiv] at h
  have h4 : c = 2 ^ 2 := by
    have := congrArg (fun x : ℝ => x ^ 2) h
    simpa [Real.sq_sqrt hc] using this
  linarith [h4]

end PrincipiaOrthogona.VolII
