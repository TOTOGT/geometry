# Lean v4.32.0 ledger — geometry, measured 2026-09-06

Produced by `tools/toolchain_ledger.py`. Toolchain pinned: `leanprover/lean4:v4.32.0`.

Nothing here is compiled by this tool. Each row reports whether a gate report already on disk names this file's declarations, and **what those declarations rest on**. Axiom reports are parsed by `tools/axiom_gate.py`, which holds the allowlist and rejoins Lean's wrapped output.

**30 of 330 tracked declarations in this repo have a kernel record** — 3 of them resting on no axiom at all, 27 within the permitted three (`propext`, `Classical.choice`, `Quot.sound`), 0 outside them. 0 explicit `axiom` declarations in this repo — an axiom is not a proof.

| file | decls | audited | `axiom` | rests on | status | report | dated |
|---|---:|---:|---:|---|---|---|---|
| `Orthogenesis/Architecture/G6Crystal.lean` | 38 | 14 | 0 | 3 axiom-free · 11 standard | kernel-audited | `geometry/tools/verify-dm3/axioms.txt` | 2026-08-26 |
| `Orthogenesis/Architecture/ToyModel.lean` | 14 | 12 | 0 | 12 standard | kernel-audited | `geometry/tools/verify-dm3/axioms.txt` | 2026-08-26 |
| `book8/OrthogonalWitness.lean` | 4 | 4 | 0 | 4 standard | kernel-audited | `geometry/tools/verify-book8/axioms.txt` | 2026-08-27 |
| `vol2-v5/deposit/VolumeTwo.lean` | 19 | 0 | 0 | — | ambiguous name | `—` | — |
| `ChladniPolygon.lean` | 4 | 0 | 0 | — | declared, no gate | `—` | — |
| `Orthogenesis.lean` | 0 | 0 | 0 | — | declared, no gate | `—` | — |
| `Orthogenesis/Architecture/AcousticLattice.lean` | 11 | 0 | 0 | — | declared, no gate | `—` | — |
| `Orthogenesis/Architecture/Coverage.lean` | 6 | 0 | 0 | — | declared, no gate | `—` | — |
| `Orthogenesis/Architecture/DM3Bridge.lean` | 14 | 0 | 0 | — | declared, no gate | `—` | — |
| `Orthogenesis/Architecture/MagneticLattice.lean` | 20 | 0 | 0 | — | declared, no gate | `—` | — |
| `Orthogenesis/Architecture/NASAGaps.lean` | 12 | 0 | 0 | — | declared, no gate | `—` | — |
| `Orthogenesis/Architecture/SeismicLattice.lean` | 17 | 0 | 0 | — | declared, no gate | `—` | — |
| `Orthogenesis/Geometry/Cell.lean` | 0 | 0 | 0 | — | declared, no gate | `—` | — |
| `Orthogenesis/Geometry/Colony.lean` | 4 | 0 | 0 | — | declared, no gate | `—` | — |
| `Orthogenesis/Geometry/Growth.lean` | 1 | 0 | 0 | — | declared, no gate | `—` | — |
| `Orthogenesis/Geometry/HexGrid.lean` | 2 | 0 | 0 | — | declared, no gate | `—` | — |
| `Orthogenesis/Geometry/Main.lean` | 0 | 0 | 0 | — | declared, no gate | `—` | — |
| `PolarPolygonCommonRefinement.lean` | 7 | 0 | 0 | — | declared, no gate | `—` | — |
| `PolarTriadClosure.lean` | 9 | 0 | 0 | — | declared, no gate | `—` | — |
| `SaturnHexagon.lean` | 5 | 0 | 0 | — | declared, no gate | `—` | — |
| `TripleAlphaDm3.lean` | 6 | 0 | 0 | — | declared, no gate | `—` | — |
| `AMonster/GenerativeWeave.lean` | 20 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `AMonster/dm3_operators.lean` | 13 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `CardiacHopfReduction.lean` | 4 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `CollatzDescent.lean` | 15 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `Coverage.lean` | 5 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `FoldCentralCharge.lean` | 10 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `Growth.lean` | 1 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `HexGrid.lean` | 1 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `NASAGaps.lean` | 16 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `NbonacciLadder.lean` | 13 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `SmokeBox.lean` | 5 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `SpiralReturnObstruction.lean` | 5 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `book6/MayaCalendar.lean` | 10 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `book6/ReactionDiffusionFold.lean` | 3 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `book8/TurnaroundUniverse.lean` | 6 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `docs/ml-evidence/AXLE-tools-verify-core/probe_core.lean` | 0 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `docs/ml-evidence/deposits-moved-to-GTCT-2026-08-30/rh-arithmetic-contact-v1/ZetaReflection.lean` | 4 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `lakefile.lean` | 0 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `tools/conclusion_scan.lean` | 0 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `tools/conclusion_scan_fixtures.lean` | 6 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `tools/verify-book8/probe_book8.lean` | 0 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `tools/verify-dm3/probe_dm3.lean` | 0 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |

## Axiom profile across every gate report in the corpus

| declarations | rests on |
|---:|---|
| 29 | `Classical.choice, Quot.sound, propext` |
| 3 | `(none — axiom-free)` |

An axiom-free proof is the strongest result `#print axioms` can report, and a checker that counts only the `depends on axioms:` form cannot see it (WP-73 §6). Both forms are counted here.

`OUTSIDE EVERY TARGET` is the row to act on first: `lake build` never touches that file, so it can stop compiling and nothing will say so. `UNTRUSTED AXIOM` outranks it — a declaration resting on `sorryAx`, `Lean.ofReduceBool` or a `native_decide` axiom is disclosed, not audited.

Dates are file timestamps on the reports, not environment records. This ledger cannot tell STALE from still-true; `CS/verify-stamp` is the instrument that binds the triple.
