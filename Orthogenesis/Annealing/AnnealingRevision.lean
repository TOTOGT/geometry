-- GATE-DECLARE: sorries = none
-- GATE-REASON: new file 2026-09-25 for the geometry pin (Lean v4.32.0, Mathlib v4.32.0).
-- UNTESTED until the author runs `lake build` on it.
/-
# AnnealingRevision.lean — Book 3, Week 13 · Revision · Nirvana Machine
# (taught path 38, ch13-revision.html; the same page serves the Cajueiro edition)

  §1  The Metropolis rule. An uphill move (ΔE > 0) is accepted with probability
      e^{−βΔE}, which lies in (0, 1], falls as β grows, and tends to 0 as β → ∞.
      A move with ΔE = 0 is accepted with probability 1 at every β — so at
      T = 0 sideways moves are still accepted, not "only downhill".
  §2  The energy E(θ) = ‖θ − x*‖² + V(θ). Its minimum is x* only if V does not
      tilt it there. In one dimension, with V(θ) = cθ and c ≠ 0, the point
      x* − c/2 has lower energy than x* itself: the error potential moves the
      minimum.
  §3  The learning rate. For E(θ) = (θ − x*)², one step θ ↦ θ − η·E′(θ) multiplies
      the distance to x* by (1 − 2η). It shrinks exactly when 0 < η < 1, flips
      sign (overshoots) for 1/2 < η < 1, and grows for η > 1 — the chapter's
      three cases, quantified.

Not formalised: that simulated annealing finds the global minimum (true in
probability only under a logarithmically slow cooling schedule — Hajek 1988 —
not for the fast schedules used in practice); the protein-folding claims; and
Theorem 13.1, a definition whose fourth condition (β → ∞) is a property of the
schedule, not a test on the paper.
-/

import Mathlib

namespace Orthogenesis.AnnealingRevision

open Real Filter Topology

/-! ## §1 The Metropolis acceptance probability -/

/-- P(accept an uphill move) = e^{−βΔE}. -/
noncomputable def acceptProb (β ΔE : ℝ) : ℝ := exp (-(β * ΔE))

theorem acceptProb_pos (β ΔE : ℝ) : 0 < acceptProb β ΔE := exp_pos _

theorem acceptProb_le_one {β ΔE : ℝ} (hβ : 0 ≤ β) (hE : 0 ≤ ΔE) : acceptProb β ΔE ≤ 1 := by
  unfold acceptProb
  rw [exp_le_one_iff]
  nlinarith [mul_nonneg hβ hE]

/-- Colder (larger β) means fewer uphill moves. -/
theorem acceptProb_strictAnti {ΔE : ℝ} (hE : 0 < ΔE) {β₁ β₂ : ℝ} (h : β₁ < β₂) :
    acceptProb β₂ ΔE < acceptProb β₁ ΔE := by
  unfold acceptProb
  rw [exp_lt_exp]
  nlinarith [mul_lt_mul_of_pos_right h hE]

/-- As β → ∞ an uphill move is (almost) never accepted. -/
theorem acceptProb_tendsto_zero {ΔE : ℝ} (hE : 0 < ΔE) :
    Tendsto (fun β => acceptProb β ΔE) atTop (𝓝 0) := by
  have h1 : Tendsto (fun β : ℝ => β * ΔE) atTop atTop := tendsto_id.atTop_mul_const hE
  exact Real.tendsto_exp_atBot.comp (tendsto_neg_atTop_atBot.comp h1)

/-- A sideways move is always accepted, at every temperature. -/
theorem acceptProb_flat (β : ℝ) : acceptProb β 0 = 1 := by
  simp [acceptProb]

/-! ## §2 The error potential moves the minimum -/

/-- E(θ) = (θ − a)² + cθ. -/
def energy (a c θ : ℝ) : ℝ := (θ - a) ^ 2 + c * θ

theorem minimum_moves {a c : ℝ} (hc : c ≠ 0) : energy a c (a - c / 2) < energy a c a := by
  unfold energy
  have : 0 < c ^ 2 := by positivity
  nlinarith

/-! ## §3 The learning rate -/

/-- One gradient step on (θ − a)² multiplies the distance to a by (1 − 2η). -/
theorem gradient_step (a η θ : ℝ) : (θ - η * (2 * (θ - a))) - a = (1 - 2 * η) * (θ - a) := by
  ring

/-- The step contracts exactly when 0 < η < 1. -/
theorem step_contracts_iff (η : ℝ) : |1 - 2 * η| < 1 ↔ 0 < η ∧ η < 1 := by
  rw [abs_lt]
  constructor
  · rintro ⟨h1, h2⟩; exact ⟨by linarith, by linarith⟩
  · rintro ⟨h1, h2⟩; exact ⟨by linarith, by linarith⟩

end Orthogenesis.AnnealingRevision

/-! ## Axiom probe -/
#print axioms Orthogenesis.AnnealingRevision.acceptProb_pos
#print axioms Orthogenesis.AnnealingRevision.acceptProb_le_one
#print axioms Orthogenesis.AnnealingRevision.acceptProb_strictAnti
#print axioms Orthogenesis.AnnealingRevision.acceptProb_tendsto_zero
#print axioms Orthogenesis.AnnealingRevision.acceptProb_flat
#print axioms Orthogenesis.AnnealingRevision.minimum_moves
#print axioms Orthogenesis.AnnealingRevision.gradient_step
#print axioms Orthogenesis.AnnealingRevision.step_contracts_iff
