# Lean v4.32.0 ledger — geometry, measured 2026-09-25

Produced by `tools/toolchain_ledger.py`. Toolchain pinned: `leanprover/lean4:v4.32.0`.

Nothing here is compiled by this tool. Each row reports whether a gate report already on disk names this file's declarations, and **what those declarations rest on**. Axiom reports are parsed by `tools/axiom_gate.py`, which holds the allowlist and rejoins Lean's wrapped output.

**375 of 657 tracked declarations in this repo have a kernel record** — 34 of them resting on no axiom at all, 341 within the permitted three (`propext`, `Classical.choice`, `Quot.sound`), 3 outside them. 0 explicit `axiom` declarations in this repo — an axiom is not a proof.

| file | decls | audited | `axiom` | rests on | status | report | dated |
|---|---:|---:|---:|---|---|---|---|
| `Orthogenesis/Architecture/MagneticLattice.lean` | 20 | 17 | 0 | 3 axiom-free · 14 standard · **1 untrusted** | UNTRUSTED AXIOM | `geometry/tools/verify-audit/2026-09-09/MagneticLattice.axioms.txt` | 2026-09-09 |
| `docs/ml-evidence/deposits-moved-to-GTCT-2026-08-30/rh-arithmetic-contact-v1/ZetaReflection.lean` | 4 | 2 | 0 | 1 axiom-free · 1 standard · **2 untrusted** | UNTRUSTED AXIOM | `geometry/tools/verify-audit/2026-09-09/ZetaReflection.axioms.txt` | 2026-09-09 |
| `CardiacHopfReduction.lean` | 5 | 5 | 0 | 5 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-12/geometry__CardiacHopfReduction.axioms.txt` | 2026-09-12 |
| `ChladniPolygon.lean` | 4 | 4 | 0 | 4 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-09/ChladniPolygon.axioms.txt` | 2026-09-10 |
| `CycleCoupling.lean` | 4 | 4 | 0 | 1 axiom-free · 3 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-09/CycleCoupling.axioms.txt` | 2026-09-10 |
| `NbonacciLadder.lean` | 13 | 13 | 0 | 1 axiom-free · 12 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-09/NbonacciLadder.axioms.txt` | 2026-09-09 |
| `Orthogenesis/Architecture/AcousticLattice.lean` | 9 | 7 | 0 | 1 axiom-free · 6 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-14/geometry__Orthogenesis__Architecture__AcousticLattice.axioms.txt` | 2026-09-14 |
| `Orthogenesis/Architecture/G6Crystal.lean` | 33 | 14 | 0 | 3 axiom-free · 11 standard | kernel-audited | `geometry/tools/verify-dm3/axioms.txt` | 2026-08-26 |
| `Orthogenesis/Architecture/SeismicLattice.lean` | 17 | 15 | 0 | 1 axiom-free · 14 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-14/geometry__Orthogenesis__Architecture__SeismicLattice.axioms.txt` | 2026-09-14 |
| `Orthogenesis/Architecture/ToyModel.lean` | 14 | 12 | 0 | 12 standard | kernel-audited | `geometry/tools/verify-dm3/axioms.txt` | 2026-08-26 |
| `Orthogenesis/Bridge/CoherenceBridge.lean` | 10 | 10 | 0 | 10 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-25/geometry__Orthogenesis__Bridge__CoherenceBridge.axioms.txt` | 2026-09-25 |
| `Orthogenesis/Disaster/CatastropheF.lean` | 8 | 7 | 0 | 7 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-15/geometry__Orthogenesis__Disaster__CatastropheF.axioms.txt` | 2026-09-15 |
| `Orthogenesis/Disaster/ChaosMu.lean` | 9 | 7 | 0 | 7 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-15/geometry__Orthogenesis__Disaster__ChaosMu.axioms.txt` | 2026-09-15 |
| `Orthogenesis/Disaster/DisasterTheory.lean` | 18 | 16 | 0 | 1 axiom-free · 15 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-15/geometry__Orthogenesis__Disaster__DisasterTheory.axioms.txt` | 2026-09-15 |
| `Orthogenesis/Figure8/A1Node.lean` | 27 | 27 | 0 | 27 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-25/geometry__Orthogenesis__Figure8__A1Node.axioms.txt` | 2026-09-25 |
| `Orthogenesis/Figure8/Analemma.lean` | 15 | 15 | 0 | 15 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-25/geometry__Orthogenesis__Figure8__Analemma.axioms.txt` | 2026-09-25 |
| `Orthogenesis/Figure8/BernoulliLemniscate.lean` | 20 | 19 | 0 | 19 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-25/geometry__Orthogenesis__Figure8__BernoulliLemniscate.axioms.txt` | 2026-09-25 |
| `Orthogenesis/Figure8/GeronoLemniscate.lean` | 16 | 15 | 0 | 15 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-25/geometry__Orthogenesis__Figure8__GeronoLemniscate.axioms.txt` | 2026-09-25 |
| `Orthogenesis/Figure8/LunarAnalemma.lean` | 16 | 16 | 0 | 16 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-25/geometry__Orthogenesis__Figure8__LunarAnalemma.axioms.txt` | 2026-09-25 |
| `Orthogenesis/Market/MarketDynamics.lean` | 12 | 12 | 0 | 12 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-25/geometry__Orthogenesis__Market__MarketDynamics.axioms.txt` | 2026-09-25 |
| `Orthogenesis/Neural/NeuralDynamics.lean` | 12 | 12 | 0 | 12 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-25/geometry__Orthogenesis__Neural__NeuralDynamics.axioms.txt` | 2026-09-25 |
| `Orthogenesis/Plasma/PlasmaRoom.lean` | 27 | 27 | 0 | 27 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-25/geometry__Orthogenesis__Plasma__PlasmaRoom.axioms.txt` | 2026-09-25 |
| `Orthogenesis/Resonance/TripleChamber.lean` | 10 | 9 | 0 | 9 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-15/geometry__Orthogenesis__Resonance__TripleChamber.axioms.txt` | 2026-09-15 |
| `PolarPolygonCommonRefinement.lean` | 15 | 15 | 0 | 5 axiom-free · 10 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-09/PolarPolygonCommonRefinement.axioms.txt` | 2026-09-09 |
| `PolarTriadClosure.lean` | 9 | 9 | 0 | 5 axiom-free · 4 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-09/PolarTriadClosure.axioms.txt` | 2026-09-09 |
| `ReactionDiffusionFold.lean` | 3 | 3 | 0 | 3 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-13/geometry__ReactionDiffusionFold.axioms.txt` | 2026-09-13 |
| `SaturnHexagon.lean` | 5 | 5 | 0 | 5 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-09/SaturnHexagon.axioms.txt` | 2026-09-09 |
| `SmokeBox.lean` | 5 | 4 | 0 | 4 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-09/SmokeBox.axioms.txt` | 2026-09-10 |
| `SpiralReturnObstruction.lean` | 5 | 5 | 0 | 1 axiom-free · 4 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-09/SpiralReturnObstruction.axioms.txt` | 2026-09-09 |
| `TripleAlphaDm3.lean` | 6 | 6 | 0 | 1 axiom-free · 5 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-09/TripleAlphaDm3.axioms.txt` | 2026-09-09 |
| `book6/MayaCalendar.lean` | 10 | 10 | 0 | 8 axiom-free · 2 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-13/geometry__book6__MayaCalendar.axioms.txt` | 2026-09-13 |
| `book8/OrthogonalWitness.lean` | 4 | 4 | 0 | 4 standard | kernel-audited | `geometry/tools/verify-book8/axioms.txt` | 2026-08-27 |
| `book8/TurnaroundUniverse.lean` | 6 | 6 | 0 | 6 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-13/geometry__TurnaroundUniverse.axioms.txt` | 2026-09-13 |
| `catgt/lean/CatGT_Main.lean` | 23 | 9 | 0 | 9 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-09/CatGT_Main.axioms.txt` | 2026-09-09 |
| `vol2-v5/deposit/VolumeTwo.lean` | 19 | 14 | 0 | 2 axiom-free · 12 standard | kernel-audited | `AXLE/tools/verify-vol2/axioms.txt` | 2026-09-24 |
| `GateScreen.lean` | 5 | 0 | 0 | — | ambiguous name | `—` | — |
| `Orthogenesis.lean` | 0 | 0 | 0 | — | declared, no gate | `—` | — |
| `Orthogenesis/Architecture/Coverage.lean` | 6 | 0 | 0 | — | declared, no gate | `—` | — |
| `Orthogenesis/Architecture/DM3Bridge.lean` | 14 | 0 | 0 | — | declared, no gate | `—` | — |
| `Orthogenesis/Architecture/NASAGaps.lean` | 12 | 0 | 0 | — | declared, no gate | `—` | — |
| `Orthogenesis/Geometry/Cell.lean` | 0 | 0 | 0 | — | declared, no gate | `—` | — |
| `Orthogenesis/Geometry/Colony.lean` | 4 | 0 | 0 | — | declared, no gate | `—` | — |
| `Orthogenesis/Geometry/GaussBonnet.lean` | 3 | 0 | 0 | — | declared, no gate | `—` | — |
| `Orthogenesis/Geometry/Growth.lean` | 1 | 0 | 0 | — | declared, no gate | `—` | — |
| `Orthogenesis/Geometry/HexForm.lean` | 5 | 0 | 0 | — | declared, no gate | `—` | — |
| `Orthogenesis/Geometry/HexGrid.lean` | 2 | 0 | 0 | — | declared, no gate | `—` | — |
| `Orthogenesis/Geometry/Main.lean` | 0 | 0 | 0 | — | declared, no gate | `—` | — |
| `AMonster/GenerativeWeave.lean` | 20 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `AMonster/dm3_operators.lean` | 13 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `CollatzDescent.lean` | 15 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `DomainCheck.lean` | 5 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `FoldCentralCharge.lean` | 10 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `LadderBound.lean` | 6 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `NASAGaps.lean` | 0 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `ToeplitzIndex.lean` | 7 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `book11/Numerals.lean` | 9 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `book12/Counting.lean` | 11 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `book17/Book17Ch02.lean` | 3 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `book17/Book17Core.lean` | 12 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `book17/Book17Mathlib.lean` | 9 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `book2/lean/StabilityRadius.lean` | 15 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `book21/Spiral.lean` | 10 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `book28/ShiftIndex.lean` | 16 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `book6/lean/VolXI_K0_Floor.lean` | 1 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `book6/lean/VolXI_attempt.lean` | 2 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `book6/lean/VolXI_candidate3.lean` | 1 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `book6/lean/grothendieckAddGroup_nat_equiv_int.lean` | 1 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `docs/ml-evidence/AXLE-tools-verify-core/probe_core.lean` | 0 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `lakefile.lean` | 0 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `tools/conclusion_scan.lean` | 0 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `tools/conclusion_scan_fixtures.lean` | 6 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `tools/verify-book8/probe_book8.lean` | 0 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `tools/verify-catgt/probe_catgt.lean` | 0 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `tools/verify-dm3/probe_dm3.lean` | 0 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `tools/verify-gaussbonnet/probe_gb.lean` | 0 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |

## Axiom profile across every gate report in the corpus

| declarations | rests on |
|---:|---|
| 436 | `Classical.choice, Quot.sound, propext` |
| 61 | `(none — axiom-free)` |
| 50 | `Quot.sound, propext` |
| 33 | `propext` |
| 12 | `Classical.choice, Quot.sound, propext, sorryAx` |
| 4 | `sorryAx` |

An axiom-free proof is the strongest result `#print axioms` can report, and a checker that counts only the `depends on axioms:` form cannot see it (WP-73 §6). Both forms are counted here.

`OUTSIDE EVERY TARGET` is the row to act on first: `lake build` never touches that file, so it can stop compiling and nothing will say so. `UNTRUSTED AXIOM` outranks it — a declaration resting on `sorryAx`, `Lean.ofReduceBool` or a `native_decide` axiom is disclosed, not audited.

Dates are file timestamps on the reports, not environment records. This ledger cannot tell STALE from still-true; `CS/verify-stamp` is the instrument that binds the triple.
