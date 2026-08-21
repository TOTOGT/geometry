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

  VERIFICATION STATUS — 2026-08-21. CLEAN, RUN AND RECORDED.
  `lake env lean` on this file, in the ~/Desktop/orthogenesis tree
  (Lean v4.33.0-rc1 + Mathlib), reports for each of the five theorems:

    [propext, Classical.choice, Quot.sound]

  No sorryAx. No errors. Two linter warnings remain, both at line 136, in
  `rot_commutes_coupling`: the trailing `ring` there is dead, because `simp`
  closes every branch on its own. It is left in place so the diff against the
  earlier version stays readable.

  HOW IT GOT HERE. Two false starts, recorded because the failure mode is the
  subject of the accompanying note.

  (1) An earlier draft used `![...]` vector notation. Mathlib's Matrix.cons_val
      simp lemmas do not chain to index 5 on a Fin 6 literal, so every proof
      silently failed into `sorry` and all five theorems reported sorryAx. The
      pattern-match form below was adopted as the fix.

  (2) THE HEADER WAS PART TRUE. Resolved by running the 2026-07-20 copy under
      the toolchain it named. ~/Desktop/AXLE pins leanprover/lean4:v4.14.0 and
      carries a built Mathlib; `lake env lean` on that copy there returns
      exit=1 and:

        gate_commutes_onsite     [propext, Classical.choice, Quot.sound]
        angCoupling_not_commute  [propext, Classical.choice, Quot.sound]
        rot_commutes_coupling    [propext, Classical.choice, Quot.sound]
        hex_rotation_invariant   [propext, Classical.choice, Quot.sound]
        hex_coupling_uniform     [propext, sorryAx, Classical.choice, Quot.sound]

      with `c + c = 2 * c` unsolved in all six cases of hex_coupling_uniform.
      So under v4.14.0 four of the five were genuinely proved, and `fin_cases`
      worked — the six cases split. The header's "All five theorems: 0 sorry
      ... No sorryAx" was therefore inaccurate on the day it was written, but
      for ONE theorem, not three, and not because no verification took place.

      Three provenance classes inside one file, under one header:

        T2, T3          true when written, true now.
        T1, T4          true when written; DECAYED. Between v4.14.0 and
                        v4.33.0-rc1 Mathlib stopped supplying Fintype (Fin 6)
                        transitively through Mathlib.Data.Real.Basic, so
                        fin_cases lost its instance and the goals were
                        admitted. Nobody changed the file.
        T5              never proved in THIS copy. The sibling copy in
                        ~/Desktop/orthogenesis carried the `ring` that closes
                        c + c = 2 * c, and carried the header
                        "KERNEL-VERIFIED: <pending>". The copy without the
                        `ring` carried the claim. The claim and the code that
                        would justify it were in different files.

      OPEN: whether an all-five clean run ever existed, on the sibling copy
      that had the `ring`. Retained at
      ~/Desktop/_to_delete/SaturnHexagon.lean.from-orthogenesis-2026-08-21 and
      testable under AXLE. Until that is run, do not assert either that the
      2026-07-20 verification happened or that it did not.

      Superseded first reading, kept for the record: this header previously
      asserted that the fix was never confirmed and that no run had occurred.
      That was inferred from failing to find evidence, in a tree chosen because
      the header itself named it, and it was too strong. What replaces it is
      narrower and measured.

  (2, as originally written) The fix was never confirmed, and a header was
      written asserting
      "KERNEL-VERIFIED 2026-07-20 ... All five theorems: 0 sorry ... No
      sorryAx." That assertion is RETRACTED. It stood in ~/Desktop/geometry, a
      tree with no .lake directory, in which this file had never been compiled.
      The repo's CI builds only `lean_lib Orthogenesis`, which does not include
      this file, and its axiom probe covers six definitions and no theorems, so
      nothing in the pipeline contradicted it. The first real run, on
      2026-08-21, returned sorryAx on gate_commutes_onsite,
      hex_rotation_invariant and hex_coupling_uniform: `fin_cases` could not
      synthesize Fintype (Fin 6) under the imports then declared, and Lean's
      error recovery admitted the open goals.

  What closed the gap: the import of Mathlib.Data.Fintype.Fin, and the `ring`
  on line 148. Between (2) and now, the statements did not change and nothing
  about them became more true; only the evidence changed.

  SINGLE COPY. As of 2026-08-21 this is the only copy of this file. Two others
  existed — ~/Desktop/orthogenesis/SaturnHexagon.lean (header: "<pending>",
  `ring` present) and ~/Desktop/cajulina/SaturnHexagon.lean (byte-identical to
  the false-header version) — and have been retired to ~/Desktop/_to_delete/.
  Neither tree is under version control. This file, in the `geometry` repo, is
  canonical; edit nowhere else.

  LOCAL VERIFICATION PROCEDURE. The `geometry` repo has no .lake directory, so
  the check runs against the built Mathlib in ~/Desktop/orthogenesis, which is
  a toolchain and not a source of truth:

      cd ~/Desktop/orthogenesis
      cp ~/Desktop/geometry/SaturnHexagon.lean /tmp/SH_geom.lean
      lake env lean /tmp/SH_geom.lean

  TOOLCHAIN MISMATCH — OPEN. That procedure runs under leanprover/lean4
  v4.33.0-rc1 (orthogenesis/lean-toolchain). This repo pins v4.32.0
  (geometry/lean-toolchain), which is also what CI would use. The clean run
  recorded above is therefore evidence under v4.33.0-rc1 only. It has not been
  reproduced under the version this repo declares.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Mathlib.Data.Fintype.Fin  -- required: puts Fintype (Fin 6) in scope for fin_cases

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
  fin_cases i <;> simp [angCoupling, hex] <;> ring  -- `ring` closes c + c = 2 * c

#print axioms gate_commutes_onsite
#print axioms angCoupling_not_commute
#print axioms rot_commutes_coupling
#print axioms hex_rotation_invariant
#print axioms hex_coupling_uniform
