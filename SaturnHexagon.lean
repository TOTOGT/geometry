/-
  Saturn's north-polar hexagon — the D6 fixed point, finite six-sextant model.
  Companion to ALGEBRAIC_PROOFS_CH7 (Crystalline Return), Theorem Ch7-T1, Step 5.

  WHY THIS FILE EXISTS. An earlier version of Ch7-T1 Step 5 asserted that a
  radial gate fails to commute with a POINTWISE fold. That is false, and is the
  same defect corrected across the corpus (see ~/geometry/CLAUDE.md, KNOWN
  DEFECT: the false commutator lemma). Here we establish the correct statement
  for the finite six-sextant (D6 / wavenumber-6) model, and add results the
  zeolite and smoke instances do not have: the sixfold rotation is a symmetry of
  the angular coupling, and the uniform hexagon is its invariant configuration.

  State: amplitude over six angular sextants theta_k = k*pi/3, k = 0..5,
  as `Fin 6 -> R`.

  NOTE ON STYLE: operators are defined by explicit pattern match on `Fin 6`
  rather than `![...]` vector notation. Mathlib's Matrix.cons_val simp lemmas
  do not chain to index 5 on a Fin 6 literal, so the vector form leaves
  unsolved goals; pattern matching reduces definitionally at every index.

  KERNEL-VERIFIED 2026-07-20 on the author's machine, Lean v4.14.0 + Mathlib
  (~/Desktop/orthogenesis tree). All five theorems: 0 sorry, and
  `#print axioms` = [propext, Classical.choice, Quot.sound] for each.
  No sorryAx.

  Provenance: the first draft of this file used `![...]` vector notation and
  reported sorryAx on all five theorems — Mathlib's Matrix.cons_val simp lemmas
  do not chain to index 5 on a Fin 6 literal, so every proof silently failed
  into `sorry`. The kernel caught it; the pattern-match form below is the one
  that came back clean.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-- Angular coupling: the cos(6θ)-type term. Each sextant receives from its two
    cyclic neighbours — this is the operator that moves amplitude BETWEEN
    sextants, and it is what carries order-dependence. -/
def angCoupling (v : Fin 6 → ℝ) : Fin 6 → ℝ
  | 0 => v 5 + v 1
  | 1 => v 0 + v 2
  | 2 => v 1 + v 3
  | 3 => v 2 + v 4
  | 4 => v 3 + v 5
  | 5 => v 4 + v 0

/-- Pointwise on-site nonlinearity (the λ|ψ|²ψ term; real cube). -/
def onsite (v : Fin 6 → ℝ) : Fin 6 → ℝ := fun i => (v i) ^ 3

/-- Radial gate: a 0/1 mask acting POINTWISE (sitewise) on the sextants. -/
def gate (v : Fin 6 → ℝ) : Fin 6 → ℝ
  | 0 => v 0
  | 1 => 0
  | 2 => v 2
  | 3 => 0
  | 4 => v 4
  | 5 => 0

/-- Sixfold rotation R : θ ↦ θ + π/3, i.e. cyclic shift of the sextants. -/
def rot (v : Fin 6 → ℝ) : Fin 6 → ℝ
  | 0 => v 5
  | 1 => v 0
  | 2 => v 1
  | 3 => v 2
  | 4 => v 3
  | 5 => v 4

/-- The uniform hexagon: equal amplitude in all six sextants. -/
def hex (c : ℝ) : Fin 6 → ℝ := fun _ => c

/-- A test state, deliberately not D6-symmetric. -/
def probe : Fin 6 → ℝ
  | 0 => 2
  | 1 => 1
  | 2 => 0
  | 3 => 1
  | 4 => 0
  | 5 => 1

-- ============================================================
-- (i) the radial gate commutes exactly with the pointwise fold
-- ============================================================

/-- **The radial gate commutes with the pointwise fold, for every state.**
This is the corrected claim: the gate is NOT the source of order-dependence. -/
theorem gate_commutes_onsite (v : Fin 6 → ℝ) : gate (onsite v) = onsite (gate v) := by
  funext i
  fin_cases i <;> norm_num [gate, onsite]

-- ============================================================
-- (ii) the angular coupling does NOT commute with the fold
-- ============================================================

/-- **Angular coupling does NOT commute with the on-site nonlinearity.**
At sextant 0 the neighbours hold 1 and 1: cube-then-sum gives 1³+1³ = 2,
sum-then-cube gives (1+1)³ = 8. Order-dependence lives here. -/
theorem angCoupling_not_commute :
    angCoupling (onsite probe) ≠ onsite (angCoupling probe) := by
  intro h
  have h0 := congrFun h 0
  norm_num [angCoupling, onsite, probe] at h0

-- ============================================================
-- (iii) D6 symmetry — results specific to the hexagon
-- ============================================================

/-- **The sixfold rotation commutes with the angular coupling.**
This is the D6 symmetry of the mechanism, with no analogue in the zeolite or
atmospheric instances of the same operator algebra. -/
theorem rot_commutes_coupling (v : Fin 6 → ℝ) :
    rot (angCoupling v) = angCoupling (rot v) := by
  funext i
  fin_cases i <;> simp [rot, angCoupling] <;> ring

/-- **The uniform hexagon is invariant under the sixfold rotation.** -/
theorem hex_rotation_invariant (c : ℝ) : rot (hex c) = hex c := by
  funext i
  fin_cases i <;> simp [rot, hex]

/-- **The uniform hexagon is preserved in form by the angular coupling:**
each sextant receives exactly `2c` from its two neighbours, so the output is
again uniform — the sixfold symmetry is not broken by the coupling. -/
theorem hex_coupling_uniform (c : ℝ) : angCoupling (hex c) = hex (2 * c) := by
  funext i
  fin_cases i <;> simp [angCoupling, hex]

#print axioms gate_commutes_onsite
#print axioms angCoupling_not_commute
#print axioms rot_commutes_coupling
#print axioms hex_rotation_invariant
#print axioms hex_coupling_uniform
