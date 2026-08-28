import Lake
open Lake DSL

package geometry

require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "v4.32.0"

@[default_target]
lean_lib Orthogenesis

/-
  SaturnHexagon.lean sits at the repository root and was NOT a build target
  before 2026-08-21. Nothing in CI compiled it, while its own header asserted
  it had been kernel-verified. Declaring it a default target is what makes a
  regression fail the job rather than pass unnoticed.

  The other root-level .lean files (CardiacHopfReduction, CollatzDescent,
  Coverage, FoldCentralCharge, Growth, HexGrid, NASAGaps, SmokeBox) are still
  outside every target. That is a known gap, not an endorsement: no claim
  resting on them should be treated as checked.
-/
@[default_target]
lean_lib SaturnHexagon

/-
  book8/OrthogonalWitness.lean kernel-checked by hand on 2026-08-27 (all four
  theorems on [propext, Classical.choice, Quot.sound]). A hand run proves the file
  on the day it is run and nothing afterwards, which is the same gap SaturnHexagon
  had. Declaring the target is what makes a later regression fail the job.
-/
@[default_target]
lean_lib OrthogonalWitness where
  srcDir := "book8"

/-
  TripleAlphaDm3.lean is the Lean behind chA-autophagy.html, which calls it
  "Mathlib-free" and "kernel-checked". Both are true and now checkable: the file
  has zero imports, so it elaborates with the bare `lean` binary in about a second
  and cannot drift with a Mathlib bump. It was nonetheless outside every target
  until 2026-08-27, which is the one thing that could have let it rot unnoticed.
-/
@[default_target]
lean_lib TripleAlphaDm3
