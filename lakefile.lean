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
