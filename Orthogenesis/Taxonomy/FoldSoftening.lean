-- GATE-DECLARE: sorries = none
-- GATE-REASON: softening at the right fold of W = q⁴/4 − 3q²/2 + a·q: along the stable branch q > 1, W″(q)/√(2 − a) → 2√3 as a → 2⁻.
/-
Orthogenesis/Taxonomy/FoldSoftening.lean — the g³³ stage ("soft equilibrium") as a stated limit.

Companion to FoldHysteresis.lean (same W, dW, d2W). g-series.html listed "the softening as a limit"
under "not proved". This file states and proves it with its constant.

Hand derivation (2026-11-08, checked symbolically with sympy before writing this file):
  Put q = 1 + x with x > 0 (the stable branch q > 1) and δ = 2 − a.
  dW a q = 0  ⇔  δ = x²(3 + x)                       (foldGap x)
  W″(q) = 3q² − 3 = 3x(2 + x)
  W″/√δ = 3x(2+x) / (x√(3+x)) = 3(2+x)/√(3+x)  →  6/√3 = 2√3   as x → 0⁺.
  Since δ ≥ 3x², δ → 0⁺ forces x → 0⁺, so the limit holds as a → 2⁻ on the branch,
  for every equilibrium with q > 1 (branch_complete: there is no other such equilibrium).

What this proves: the restoring stiffness W″ at the stable state vanishes like 2√(3δ).
What it does not prove: anything about motion. The gradient flow q̇ = −dW a q is NOT formalised here;
relaxation_time_x is about 1/W″, which is the linear relaxation time of that flow only once the flow
and its linearisation are stated. No count of cycles (33 or otherwise) follows from this file.
-/
import Mathlib
import Orthogenesis.Taxonomy.FoldHysteresis

namespace Orthogenesis.FoldSoftening

open Orthogenesis.FoldHysteresis Filter Topology

/-- Distance of the control below the right fold, as a function of the branch coordinate x = q − 1. -/
def foldGap (x : ℝ) : ℝ := x ^ 2 * (3 + x)

/-! ## §1  The branch, parametrised by x = q − 1 -/

theorem branch_equilibrium (x : ℝ) : dW (2 - foldGap x) (1 + x) = 0 := by
  unfold dW foldGap; ring

/-- Every equilibrium determines its control: 2 − a = foldGap (q − 1). -/
theorem branch_complete {a q : ℝ} (h : dW a q = 0) : 2 - a = foldGap (q - 1) := by
  unfold dW at h
  unfold foldGap
  linear_combination (-1 : ℝ) * h

theorem d2W_branch (x : ℝ) : d2W (1 + x) = 3 * x * (2 + x) := by
  unfold d2W; ring

theorem foldGap_pos {x : ℝ} (hx : 0 < x) : 0 < foldGap x := by
  unfold foldGap
  exact mul_pos (pow_pos hx 2) (by linarith)

theorem foldGap_ge {x : ℝ} (hx : 0 < x) : 3 * x ^ 2 ≤ foldGap x := by
  unfold foldGap
  nlinarith [pow_pos hx 3]

/-! ## §2  The ratio, in closed form -/

theorem ratio_eq {x : ℝ} (hx : 0 < x) :
    d2W (1 + x) / Real.sqrt (foldGap x) = 3 * (2 + x) / Real.sqrt (3 + x) := by
  have h3 : (0 : ℝ) < 3 + x := by linarith
  have hr : 0 < Real.sqrt (3 + x) := Real.sqrt_pos.mpr h3
  have hs : Real.sqrt (foldGap x) = x * Real.sqrt (3 + x) := by
    unfold foldGap
    rw [Real.sqrt_mul (sq_nonneg x), Real.sqrt_sq hx.le]
  rw [hs, d2W_branch, div_eq_div_iff (mul_pos hx hr).ne' hr.ne']
  ring

noncomputable def softRatio (x : ℝ) : ℝ := 3 * (2 + x) / Real.sqrt (3 + x)

theorem softRatio_zero : softRatio 0 = 2 * Real.sqrt 3 := by
  unfold softRatio
  have h : Real.sqrt 3 ≠ 0 := by positivity
  have h3 : (3 : ℝ) + 0 = 3 := by norm_num
  rw [h3, div_eq_iff h]
  nlinarith [Real.mul_self_sqrt (show (0 : ℝ) ≤ 3 by norm_num)]

theorem softRatio_continuousAt : ContinuousAt softRatio 0 := by
  have h1 : Continuous fun x : ℝ => 3 * (2 + x) :=
    continuous_const.mul (continuous_const.add continuous_id)
  have h2 : Continuous fun x : ℝ => Real.sqrt (3 + x) :=
    Real.continuous_sqrt.comp (continuous_const.add continuous_id)
  have h3 : Real.sqrt (3 + 0) ≠ 0 := by positivity
  exact h1.continuousAt.div h2.continuousAt h3

/-! ## §3  The softening limit -/

/-- Along the stable branch, W″/√(2 − a) → 2√3 as the branch coordinate x → 0⁺. -/
theorem softening_limit_x :
    Tendsto (fun x => d2W (1 + x) / Real.sqrt (foldGap x)) (𝓝[>] 0) (𝓝 (2 * Real.sqrt 3)) := by
  have hg : Tendsto softRatio (𝓝[>] 0) (𝓝 (2 * Real.sqrt 3)) := by
    rw [← softRatio_zero]
    exact softRatio_continuousAt.tendsto.mono_left nhdsWithin_le_nhds
  refine Tendsto.congr' ?_ hg
  filter_upwards [self_mem_nhdsWithin] with x hx
  exact (ratio_eq (Set.mem_Ioi.mp hx)).symm

/-- The same limit stated in the control: for every equilibrium q > 1 of W(·; a) with a close
enough below 2, W″(q)/√(2 − a) is within ε of 2√3. No parametrisation is assumed. -/
theorem softening_limit {ε : ℝ} (hε : 0 < ε) :
    ∃ η > 0, ∀ a q : ℝ, 1 < q → dW a q = 0 → 2 - a < η →
      |d2W q / Real.sqrt (2 - a) - 2 * Real.sqrt 3| < ε := by
  obtain ⟨ρ, hρ, hball⟩ := Metric.tendsto_nhdsWithin_nhds.mp softening_limit_x ε hε
  refine ⟨3 * ρ ^ 2, by positivity, ?_⟩
  intro a q hq heq hδ
  obtain ⟨x, rfl⟩ : ∃ x, q = 1 + x := ⟨q - 1, by ring⟩
  have hx : 0 < x := by linarith
  have hda : 2 - a = foldGap x := by
    have h0 := branch_complete heq
    have e : (1 + x - 1) = x := by ring
    rw [e] at h0
    exact h0
  have hxρ : x < ρ := by
    by_contra hc0
    have hc : ρ ≤ x := not_lt.mp hc0
    have hsq : ρ * ρ ≤ x * x := mul_le_mul hc hc hρ.le hx.le
    have hge := foldGap_ge hx
    nlinarith
  have hd : dist x 0 < ρ := by
    rw [Real.dist_eq, sub_zero, abs_of_pos hx]
    exact hxρ
  have key := hball (Set.mem_Ioi.mpr hx) hd
  rw [Real.dist_eq] at key
  rw [hda]
  exact key

/-- 1/W″ (the linear relaxation time, once the gradient flow is stated) scales as 1/(2√(3δ)):
√(2 − a)/W″ → (2√3)⁻¹ along the branch. -/
theorem relaxation_time_x :
    Tendsto (fun x => Real.sqrt (foldGap x) / d2W (1 + x)) (𝓝[>] 0)
      (𝓝 (2 * Real.sqrt 3)⁻¹) := by
  have h := softening_limit_x.inv₀ (by positivity : (2 * Real.sqrt 3) ≠ 0)
  simpa only [inv_div] using h

end Orthogenesis.FoldSoftening

#print axioms Orthogenesis.FoldSoftening.branch_complete
#print axioms Orthogenesis.FoldSoftening.ratio_eq
#print axioms Orthogenesis.FoldSoftening.softening_limit_x
#print axioms Orthogenesis.FoldSoftening.softening_limit
#print axioms Orthogenesis.FoldSoftening.relaxation_time_x
