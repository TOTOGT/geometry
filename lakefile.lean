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

  Revised 2026-09-11. Coverage.lean, Growth.lean and HexGrid.lean are no longer
  at the root: each was a stale ancestor of the copy under Orthogenesis/ (April
  or June, against August in the tree), nothing imported them, and the built
  copy is authoritative. NASAGaps.lean stays as a tombstone with no declarations
  -- see its header for why an emptied file is doing work there.

  Nine root-level .lean files are still outside every target, and they are not
  all in the same condition. The distinction this lakefile keeps making applies
  here too: a hand run proves a file on the day it is run and nothing afterwards.

    Hand-audited 2026-09-09, reports in tools/verify-audit/2026-09-09/ --
      CycleCoupling, NbonacciLadder, SmokeBox, SpiralReturnObstruction.
      Kernel-checked on that date against the v4.32.0 pin, with no undeclared
      vacuity (see Orthogenesis/Architecture/KNOWN_PLACEHOLDERS.txt for how a
      `True`-conclusion theorem is declared rather than left to pass silently).
      What they lack is not a check. It is a check that repeats.

    No audit report on record --
      CardiacHopfReduction, CollatzDescent (346 L), FoldCentralCharge,
      LadderBound (172 L), DomainCheck. Nothing is known either way about
      these, which is a different and weaker position than the four above.
      CollatzDescent and LadderBound carry the most unaudited mathematics in
      the repository.

  DomainCheck.lean elaborated clean under `lake env lean` on 2026-09-11 -- five
  theorems, no sorry, no warnings -- but has no .axioms.txt beside it and no
  target. It exists so a reader can re-run the domain result in Book 4 Ch 12
  against their own kernel, and a file nothing compiles cannot keep that
  promise. It is the cheapest of the five to close.
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

/-
  PolarTriadClosure.lean was hand-checked with the bare `lean` binary on
  2026-09-05 under v4.32.0, the repo pin: no sorry, axioms limited to propext
  and Quot.sound, which arrive through the induction on an inductive Prop.
  Like TripleAlphaDm3 it has zero imports, so it elaborates in about a second
  and cannot drift with a Mathlib bump. But a hand run proves the file on the
  day it is run and nothing afterwards — the same gap SaturnHexagon had.
  Declaring the target is what makes a later regression fail the job.
-/
@[default_target]
lean_lib PolarTriadClosure

/-
  PolarPolygonCommonRefinement.lean, same conditions: zero imports, hand-checked
  under v4.32.0 on 2026-09-05, no sorry, axioms propext and Quot.sound only.
  Declared here for the same reason as the others — a hand run dates from the
  day it was run.
-/
@[default_target]
lean_lib PolarPolygonCommonRefinement

/-
  ChladniPolygon.lean supplies the declarations `nodal-sets.html` displays and
  marks "Lean ✓" — which resolved nowhere until 2026-09-05 — and adds the tenfold
  case. Checked with `leancheck.sh --audit` on 2026-09-05: 4 theorems, 0 trusting
  sorryAx. It imports Mathlib, so unlike the other two polar files it cannot be
  run with the bare `lean` binary; the target is what keeps it checked.
-/
@[default_target]
lean_lib ChladniPolygon
