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

/-
  CardiacHopfReduction.lean is the Lean behind ch6b-cardiac.html. Audited by hand
  2026-09-12 under the v4.32.0 pin. A hand run dates from the day it was run;
  declaring the target is what makes a later regression fail the job.
  Caution recorded where the file enters CI: `supercritical` proves
  0 < L -> -(1/L) < 0 and mentions no vector field. `radial_deriv_at_cycle`
  carries the content its name claims.
-/
@[default_target]
lean_lib CardiacHopfReduction

/-
  ReactionDiffusionFold.lean is the Lean behind book6/ch-reaction-diffusion-fold.
  Audited 2026-09-13 with tools/leancheck.sh --audit under the v4.32.0 pin: three
  declarations, all on the permitted three axioms, report kept at
  tools/verify-audit/2026-09-13/. It carried a "NOT yet been run through the
  kernel" banner from 2026-09-10 until that run; the banner now records the run
  and the target is what keeps it true after today.

  The file proves the algebraic and spectral core only. Center-manifold existence
  and the O(a^5) feedback bound are invoked as standard results, not formalized,
  and the header says which is which -- the distinction the NAME EXCEEDS STATEMENT
  entry in docs/defect-ledger.html exists to keep visible.
-/
@[default_target]
lean_lib ReactionDiffusionFold

/-
  book8/TurnaroundUniverse.lean is the recollapsing closed-dust companion to
  OrthogonalWitness.lean, and sits beside it under the same srcDir. Audited
  2026-09-13 under the v4.32.0 pin: six declarations, all on the permitted three,
  report in tools/verify-audit/2026-09-13/.

  Its six theorems are about the cycloid a(eta) = R(1 - cos eta) -- non-negativity,
  the ceiling at eta = pi, the two zeros. That the cycloid SOLVES the closed-dust
  Friedmann first integral is a numeric result to ~1e-10 and is not in the kernel.
  Recorded here because the filename names a cosmology and the theorems name a
  curve, which is the NAME EXCEEDS STATEMENT shape; the header carries the same
  note where a reader of the file will meet it.
-/
@[default_target]
lean_lib TurnaroundUniverse where
  srcDir := "book8"

/-
  catgt/lean/CatGT_Main.lean is the Lean behind ch-catgt-zeolite.html and the V5 paper
  "The Self-Trapping Selectivity Principle". It is a MIRROR: the canonical copy is
  TOTOGT/io (CatGT/CatGT_Main.lean, pinned to v4.14.0); see catgt/lean/MIRROR_NOTE.md.
  Hand-run by the author 2026-09-20 under this repo's v4.32.0 pin: no errors, 13 theorems,
  all on [propext, Classical.choice, Quot.sound]. Declaring the target is what makes a later
  regression fail the job instead of passing unnoticed. Not yet built with `lake build CatGT`
  at the time this stanza was added -- run it once to confirm the target itself resolves.
-/
@[default_target]
lean_lib CatGT where
  srcDir := "catgt/lean"
  roots := #[`CatGT_Main]
