/-
  GateScreen.lean — WP39's Theorem T2(i), read backwards as a screen.

  WP39 (Book 6) proves, on a three-layer atmospheric column, that a 0/1 lid
  commutes with a specific pointwise loss (squaring) and does NOT commute with
  vertical transport. The arc WP40–WP41–WP66–WP67 then ran forward from that
  result, asking which atmospheric process could be called K.

  This file asks the backward question. The proof of T2(i) never uses the
  squaring. What it uses is that the loss acts inside each layer separately and
  sends an empty layer to an empty layer. So T2(i) generalises to a screen:

    NO layer-local intervention is a gate.

  and the screen is decidable by inspection of the candidate's type.

  SCOPE DISCIPLINE. These are theorems about a box model, not claims about the
  atmosphere. Nothing here says an intervention is ineffective. It says an
  intervention of this shape cannot carry order-dependence with respect to the
  lid, and therefore cannot be argued for from WP39.

  KERNEL-CHECKED 2026-09-15, Lean v4.33.0-rc1 + Mathlib rev eba3d887fc. All five
  theorems: no goals left admitted; `#print axioms` = [propext, Classical.choice,
  Quot.sound] for each.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Data.Fin.VecNotation
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.NormNum

/-- A three-layer column: 0 = surface, 1 = mid, 2 = aloft. -/
abbrev Column := Fin 3 → ℝ

/-- The gate. A 0/1 lid sealing off the layer aloft (WP39 §3). -/
def lid (v : Column) : Column := ![v 0, v 1, 0]

/-- Vertical transport: moves amplitude BETWEEN adjacent layers. -/
def transport (v : Column) : Column := ![v 1, v 0 + v 2, v 1]

/-- A **layer-local** intervention: one real function applied inside each layer,
with no term coupling one layer to another. Every aerosol, seeding, phase or
loss process the arc proposed has this shape. -/
def layerLocal (f : ℝ → ℝ) (v : Column) : Column := fun i => f (v i)

/-- **The screen.** The gate commutes with *every* layer-local intervention that
fixes zero — identically, in every column state, not approximately and not
generically. WP39's T2(i) is the case `f = (· ^ 2)`. -/
theorem lid_commutes_layerLocal (f : ℝ → ℝ) (hf : f 0 = 0) (v : Column) :
    lid (layerLocal f v) = layerLocal f (lid v) := by
  funext i
  fin_cases i <;> simp [lid, layerLocal, hf]

/-- WP39's T2(i) recovered as a corollary: nothing in it depended on squaring. -/
theorem lid_commutes_onsite (v : Column) :
    lid (fun i => (v i) ^ 2) = (fun i => (lid v i) ^ 2) :=
  lid_commutes_layerLocal (· ^ 2) (by norm_num) v

/-- **The screen, contrapositive — the form a referee can run.** An operator that
fails to commute with the gate at even one column state cannot be written as a
layer-local map fixing zero. Equivalently: if a candidate intervention acts
inside layers, it is not a gate, and no amount of deployment detail will make it
one. -/
theorem not_layerLocal_of_not_commutes (g : Column → Column)
    (h : ∃ v, lid (g v) ≠ g (lid v)) :
    ¬ ∃ f : ℝ → ℝ, f 0 = 0 ∧ ∀ v, g v = layerLocal f v := by
  rintro ⟨f, hf, hg⟩
  obtain ⟨v, hv⟩ := h
  exact hv (by rw [hg, hg]; exact lid_commutes_layerLocal f hf v)

/-- Test column: smoke present at all three levels. -/
def plume : Column := ![2, 1, 1]

/-- The screen is not vacuous: transport fails it. -/
theorem transport_not_commutes_lid : lid (transport plume) ≠ transport (lid plume) := by
  intro h
  have h1 := congrFun h 1
  simp [lid, transport, plume] at h1

/-- **What survives the screen moves amplitude between layers.** Transport is not
layer-local — which is the whole content of the finding, since the atmospheric
objects that move amplitude between layers (subsidence, frontal passage, the
boundary-layer cap) are the ones no one can deploy. -/
theorem transport_not_layerLocal :
    ¬ ∃ f : ℝ → ℝ, f 0 = 0 ∧ ∀ v, transport v = layerLocal f v :=
  not_layerLocal_of_not_commutes transport ⟨plume, transport_not_commutes_lid⟩

#print axioms lid_commutes_layerLocal
#print axioms lid_commutes_onsite
#print axioms not_layerLocal_of_not_commutes
#print axioms transport_not_commutes_lid
#print axioms transport_not_layerLocal
