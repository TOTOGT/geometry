/-
  ReebPullback.lean  (2026-11-11)  --  built clean by the author under Lean/Mathlib v4.32.0
  (geometry, `lake env lean catgt/lean/ReebPullback.lean`, first run): all six declarations
  depend on [propext, Classical.choice, Quot.sound]; no warnings or errors in the output seen.
  NOT buildable under the v4.14.0 pin of the io repo (that Mathlib has no `extDeriv`).

  PURPOSE. Restate "the Reeb flow preserves alpha and d(alpha)" with Mathlib's own pullback and
  exterior derivative, not the hand formulas of ReebFlow.lean.

  Mathlib's pullback of a form `ω : F → F [⋀^Fin n]→L[𝕜] G` along `f : E → F` is
      x ↦ (ω (f x)).compContinuousLinearMap (fderiv 𝕜 f x)
  (this is exactly the expression in `extDeriv_pullback`, Analysis/Calculus/DifferentialForm/Basic).
  With `omega` the Mathlib 1-form of `alpha_cat` (ReebFlowExtDeriv.lean):

    (1) `reebFlow_pullback_omega`:   phi_t^* omega = omega.
    (2) `reebFlow_preserves_extDeriv_omega`:   phi_t^* (extDeriv omega) = extDeriv omega, i.e. the
        flow preserves d(alpha) as a Mathlib 2-form.  Proof: Mathlib's `extDeriv_pullback`
        (d commutes with pullback) applied to (1).  The only inputs are (1), smoothness of the
        affine map `reebFlow t`, and `omega_differentiableAt`.
    (3) `reeb_interior_extDeriv`:   extDeriv omega p ![reebR, w] = 0 for all w (i_R d(alpha) = 0),
        via the bridge `ReebFlowExt.dAlpha_eq_extDeriv` and the fact that the `dAlpha` and
        `alphaCat` copies in ReebFlow and ReebFlowExt are definitionally equal.

  WHAT THIS DOES NOT DO.  The contact volume alpha ∧ d(alpha) is still not compared with a Mathlib
  wedge product; `contactVol` is the explicit formula.  Nothing here uses polar-chart degeneracy:
  `omega` is a form on the model space R^3 with coordinates (r, theta, z), and every statement
  holds at every point of that model, including r = 0 (the polar chart is not at issue because the
  statements are about the coordinate expression, not about the Cartesian manifold).
-/

import Mathlib
import ReebFlow
import ReebFlowExtDeriv

/-- The `alphaCat` copies agree (definitionally; stated so `exact` has an anchor). -/
theorem alphaCat_copies (p v : ℝ × ℝ × ℝ) :
    ReebFlowExt.alphaCat p v = ReebFlow.alphaCat p v := rfl

/-- The `dAlpha` copies agree (definitionally). -/
theorem dAlpha_copies (p u w : ℝ × ℝ × ℝ) :
    ReebFlowExt.dAlpha p u w = ReebFlow.dAlpha p u w := rfl

/-- **(1)** The Reeb flow pulls the Mathlib 1-form `omega` back to itself. -/
theorem reebFlow_pullback_omega (t : ℝ) :
    (fun x : ℝ × ℝ × ℝ =>
      (ReebFlowExt.omega (ReebFlow.reebFlow t x)).compContinuousLinearMap
        (fderiv ℝ (ReebFlow.reebFlow t) x)) = ReebFlowExt.omega := by
  funext x
  rw [ReebFlow.reebFlow_fderiv]
  ext v
  rw [ContinuousAlternatingMap.compContinuousLinearMap_apply]
  simp [ReebFlowExt.omega_apply, ReebFlowExt.alphaCat, ReebFlow.reebFlow, ReebFlow.reebR]

/-- `reebFlow t` is smooth (it is translation). -/
theorem reebFlow_contDiffAt (t : ℝ) (x : ℝ × ℝ × ℝ) :
    ContDiffAt ℝ 2 (ReebFlow.reebFlow t) x := by
  show ContDiffAt ℝ 2 (fun p : ℝ × ℝ × ℝ => p + t • ReebFlow.reebR) x
  exact (contDiff_id.add contDiff_const).contDiffAt

/-- **(2)** The Reeb flow preserves `d(alpha)` as a Mathlib 2-form: the pullback of
    `extDeriv omega` along `reebFlow t` is `extDeriv omega`. -/
theorem reebFlow_preserves_extDeriv_omega (t : ℝ) (x : ℝ × ℝ × ℝ) :
    (extDeriv ReebFlowExt.omega (ReebFlow.reebFlow t x)).compContinuousLinearMap
        (fderiv ℝ (ReebFlow.reebFlow t) x)
      = extDeriv ReebFlowExt.omega x := by
  have h := extDeriv_pullback (𝕜 := ℝ) (r := 2) (ω := ReebFlowExt.omega)
    (f := ReebFlow.reebFlow t) (x := x)
    (ReebFlowExt.omega_differentiableAt _) (reebFlow_contDiffAt t x) (by simp)
  rw [reebFlow_pullback_omega t] at h
  exact h.symm

/-- **(3)** `i_R d(alpha) = 0`, with `d` Mathlib's exterior derivative. -/
theorem reeb_interior_extDeriv (p w : ℝ × ℝ × ℝ) :
    extDeriv ReebFlowExt.omega p ![ReebFlow.reebR, w] = 0 := by
  rw [← ReebFlowExt.dAlpha_eq_extDeriv]
  exact ReebFlow.reeb_interior_dAlpha p w

#print axioms alphaCat_copies
#print axioms dAlpha_copies
#print axioms reebFlow_pullback_omega
#print axioms reebFlow_contDiffAt
#print axioms reebFlow_preserves_extDeriv_omega
#print axioms reeb_interior_extDeriv
