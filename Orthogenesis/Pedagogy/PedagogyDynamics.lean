-- GATE-DECLARE: sorries = none
-- GATE-REASON: new file 2026-09-25 for the geometry pin (Lean v4.32.0, Mathlib v4.32.0).
-- Author's build 2026-09-25: 9/9 on standard axioms, first try, no warnings.
/-
# PedagogyDynamics.lean — Book 3, Ch 6 (Pedagogy: CEFR → TO/TOGT), "Why This Program Works"
# ==========================================================================================
# ch06-pedagogy.html rests the 14-week program on three mathematical claims. This file
# checks each against what the mathematics gives.
#
#   §1  "Convergence guaranteed: G is a contraction (Banach)." Banach gives convergence in
#       the limit. For the linear contraction r ↦ r* + (1 − k)(r − r*) the distance after n
#       steps is exactly |1 − k|ⁿ·|r₀ − r*|, so after 14 steps it is still non-zero unless
#       the start was already the fixed point: "will reach the fixed point" does not hold in
#       finite time.
#   §2  "Each student's fixed point Γ* is unique because each begins with a different seed."
#       A contraction has exactly one fixed point, and every starting point converges to that
#       same point (Banach). Individual fixed points require a different G per student.
#   §3  "Because G is non-commutative, the learner cannot return to an earlier phase."
#       Non-commutativity does not imply irreversibility: x ↦ x + 1 and x ↦ 2x are both
#       bijective and do not commute. Irreversibility needs G to be non-injective.
#
# Not formalised: the CEFR–TOGT correspondence table, the week plan and the one-year recall
# prediction (empirical, teaching design). G itself is not defined anywhere in the Lean.
-/

import Mathlib

namespace Orthogenesis.PedagogyDynamics

open Filter Topology

/-! ## §1 Convergence is in the limit, not in 14 steps -/

/-- The linear contraction toward s with gain k: r ↦ s + (1 − k)(r − s). -/
def relax (k s r : ℝ) : ℝ := s + (1 - k) * (r - s)

theorem relax_dist (k s x y : ℝ) : |relax k s x - relax k s y| = |1 - k| * |x - y| := by
  unfold relax
  rw [show s + (1 - k) * (x - s) - (s + (1 - k) * (y - s)) = (1 - k) * (x - y) by ring, abs_mul]

theorem relax_iter (k s r : ℝ) (n : ℕ) :
    (relax k s)^[n] r - s = (1 - k) ^ n * (r - s) := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [Function.iterate_succ_apply']
    simp only [relax]
    rw [show s + (1 - k) * ((relax k s)^[n] r - s) - s = (1 - k) * ((relax k s)^[n] r - s) by ring,
      ih]
    ring

/-- After fourteen steps the learner is not at the fixed point, unless k = 1 (a single-step
    jump) or the start was already there. -/
theorem fourteen_steps_not_at_fixed_point {k s r : ℝ} (hk : k ≠ 1) (hr : r ≠ s) :
    (relax k s)^[14] r ≠ s := by
  intro h
  have e := relax_iter k s r 14
  rw [h, sub_self] at e
  have h1 : (1 - k) ^ 14 ≠ 0 := pow_ne_zero _ (sub_ne_zero.mpr (Ne.symm hk))
  have h2 : r - s ≠ 0 := sub_ne_zero.mpr hr
  exact (mul_ne_zero h1 h2) e.symm

/-! ## §2 A contraction has one fixed point, shared by every seed -/

/-- Any two fixed points of a contraction coincide. -/
theorem contraction_fixed_points_eq {α : Type*} [MetricSpace α] {K : NNReal} {f : α → α}
    (hf : ContractingWith K f) {a b : α} (ha : Function.IsFixedPt f a)
    (hb : Function.IsFixedPt f b) : a = b :=
  hf.fixedPoint_unique' ha hb

/-- Every seed converges to the same fixed point. -/
theorem all_seeds_same_limit {α : Type*} [MetricSpace α] [CompleteSpace α] [Nonempty α]
    {K : NNReal} {f : α → α} (hf : ContractingWith K f) (x y : α) :
    Tendsto (fun n => f^[n] x) atTop (𝓝 (ContractingWith.fixedPoint f hf)) ∧
      Tendsto (fun n => f^[n] y) atTop (𝓝 (ContractingWith.fixedPoint f hf)) :=
  ⟨hf.tendsto_iterate_fixedPoint x, hf.tendsto_iterate_fixedPoint y⟩

/-! ## §3 Non-commutative does not mean irreversible -/

def shift (x : ℝ) : ℝ := x + 1
def dbl (x : ℝ) : ℝ := 2 * x

theorem shift_bijective : Function.Bijective shift :=
  ⟨fun a b h => by unfold shift at h; linarith, fun y => ⟨y - 1, by unfold shift; ring⟩⟩

theorem dbl_bijective : Function.Bijective dbl :=
  ⟨fun a b h => by unfold dbl at h; linarith, fun y => ⟨y / 2, by unfold dbl; ring⟩⟩

theorem shift_dbl_not_commute : shift ∘ dbl ≠ dbl ∘ shift := by
  intro h
  have := congrFun h 0
  simp only [Function.comp, shift, dbl] at this
  norm_num at this

/-- Two invertible maps that do not commute: order matters, yet every step can be undone. -/
theorem noncommutative_not_irreversible :
    ∃ f g : ℝ → ℝ, Function.Bijective f ∧ Function.Bijective g ∧ f ∘ g ≠ g ∘ f :=
  ⟨shift, dbl, shift_bijective, dbl_bijective, shift_dbl_not_commute⟩

end Orthogenesis.PedagogyDynamics

/-! ## Axiom probe -/
#print axioms Orthogenesis.PedagogyDynamics.relax_dist
#print axioms Orthogenesis.PedagogyDynamics.relax_iter
#print axioms Orthogenesis.PedagogyDynamics.fourteen_steps_not_at_fixed_point
#print axioms Orthogenesis.PedagogyDynamics.contraction_fixed_points_eq
#print axioms Orthogenesis.PedagogyDynamics.all_seeds_same_limit
#print axioms Orthogenesis.PedagogyDynamics.shift_bijective
#print axioms Orthogenesis.PedagogyDynamics.dbl_bijective
#print axioms Orthogenesis.PedagogyDynamics.shift_dbl_not_commute
#print axioms Orthogenesis.PedagogyDynamics.noncommutative_not_irreversible
