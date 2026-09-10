# Lean v4.32.0 ledger — geometry, measured 2026-09-10

Produced by `tools/toolchain_ledger.py`. Toolchain pinned: `leanprover/lean4:v4.32.0`.

Nothing here is compiled by this tool. Each row reports whether a gate report already on disk names this file's declarations, and **what those declarations rest on**. Axiom reports are parsed by `tools/axiom_gate.py`, which holds the allowlist and rejoins Lean's wrapped output.

**157 of 351 tracked declarations in this repo have a kernel record** — 28 of them resting on no axiom at all, 129 within the permitted three (`propext`, `Classical.choice`, `Quot.sound`), 3 outside them. 0 explicit `axiom` declarations in this repo — an axiom is not a proof.

| file | decls | audited | `axiom` | rests on | status | report | dated |
|---|---:|---:|---:|---|---|---|---|
| `Orthogenesis/Architecture/MagneticLattice.lean` | 20 | 17 | 0 | 3 axiom-free · 14 standard · **1 untrusted** | UNTRUSTED AXIOM | `geometry/tools/verify-audit/2026-09-09/MagneticLattice.axioms.txt` | 2026-09-10 |
| `Orthogenesis/Architecture/SeismicLattice.lean` | 17 | 14 | 0 | 2 axiom-free · 12 standard · **1 untrusted** | UNTRUSTED AXIOM | `geometry/tools/verify-audit/2026-09-09/SeismicLattice.axioms.txt` | 2026-09-10 |
| `docs/ml-evidence/deposits-moved-to-GTCT-2026-08-30/rh-arithmetic-contact-v1/ZetaReflection.lean` | 4 | 2 | 0 | 1 axiom-free · 1 standard · **1 untrusted** | UNTRUSTED AXIOM | `geometry/tools/verify-audit/2026-09-09/ZetaReflection.axioms.txt` | 2026-09-10 |
| `ChladniPolygon.lean` | 4 | 4 | 0 | 4 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-09/ChladniPolygon.axioms.txt` | 2026-09-10 |
| `CycleCoupling.lean` | 4 | 4 | 0 | 1 axiom-free · 3 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-09/CycleCoupling.axioms.txt` | 2026-09-10 |
| `NbonacciLadder.lean` | 13 | 13 | 0 | 1 axiom-free · 12 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-09/NbonacciLadder.axioms.txt` | 2026-09-10 |
| `Orthogenesis/Architecture/AcousticLattice.lean` | 11 | 9 | 0 | 3 axiom-free · 6 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-09/AcousticLattice.axioms.txt` | 2026-09-10 |
| `Orthogenesis/Architecture/G6Crystal.lean` | 38 | 14 | 0 | 3 axiom-free · 11 standard | kernel-audited | `geometry/tools/verify-dm3/axioms.txt` | 2026-08-26 |
| `Orthogenesis/Architecture/ToyModel.lean` | 14 | 12 | 0 | 12 standard | kernel-audited | `geometry/tools/verify-dm3/axioms.txt` | 2026-08-26 |
| `PolarPolygonCommonRefinement.lean` | 15 | 15 | 0 | 5 axiom-free · 10 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-09/PolarPolygonCommonRefinement.axioms.txt` | 2026-09-10 |
| `PolarTriadClosure.lean` | 9 | 9 | 0 | 5 axiom-free · 4 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-09/PolarTriadClosure.axioms.txt` | 2026-09-10 |
| `SaturnHexagon.lean` | 5 | 5 | 0 | 5 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-09/SaturnHexagon.axioms.txt` | 2026-09-10 |
| `SmokeBox.lean` | 5 | 5 | 0 | 5 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-09/SmokeBox.axioms.txt` | 2026-09-10 |
| `SpiralReturnObstruction.lean` | 5 | 5 | 0 | 1 axiom-free · 4 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-09/SpiralReturnObstruction.axioms.txt` | 2026-09-10 |
| `TripleAlphaDm3.lean` | 6 | 6 | 0 | 1 axiom-free · 5 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-09/TripleAlphaDm3.axioms.txt` | 2026-09-10 |
| `book4/ZetaScratch.lean` | 5 | 2 | 0 | 2 standard | kernel-audited | `geometry/tools/verify-audit/2026-09-08/ZetaReflection.axioms.txt` | 2026-09-08 |
| `book8/OrthogonalWitness.lean` | 4 | 4 | 0 | 4 standard | kernel-audited | `geometry/tools/verify-book8/axioms.txt` | 2026-08-27 |
| `vol2-v5/deposit/VolumeTwo.lean` | 19 | 17 | 0 | 2 axiom-free · 15 standard | kernel-audited | `AXLE/tools/verify-vol2/axioms.txt` | 2026-08-27 |
| `Orthogenesis.lean` | 0 | 0 | 0 | — | declared, no gate | `—` | — |
| `Orthogenesis/Architecture/Coverage.lean` | 6 | 0 | 0 | — | declared, no gate | `—` | — |
| `Orthogenesis/Architecture/DM3Bridge.lean` | 14 | 0 | 0 | — | declared, no gate | `—` | — |
| `Orthogenesis/Architecture/NASAGaps.lean` | 12 | 0 | 0 | — | declared, no gate | `—` | — |
| `Orthogenesis/Geometry/Cell.lean` | 0 | 0 | 0 | — | declared, no gate | `—` | — |
| `Orthogenesis/Geometry/Colony.lean` | 4 | 0 | 0 | — | declared, no gate | `—` | — |
| `Orthogenesis/Geometry/Growth.lean` | 1 | 0 | 0 | — | declared, no gate | `—` | — |
| `Orthogenesis/Geometry/HexGrid.lean` | 2 | 0 | 0 | — | declared, no gate | `—` | — |
| `Orthogenesis/Geometry/Main.lean` | 0 | 0 | 0 | — | declared, no gate | `—` | — |
| `AMonster/GenerativeWeave.lean` | 20 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `AMonster/dm3_operators.lean` | 13 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `CardiacHopfReduction.lean` | 4 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `CollatzDescent.lean` | 15 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `Coverage.lean` | 6 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `FoldCentralCharge.lean` | 10 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `Growth.lean` | 1 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `HexGrid.lean` | 2 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `LadderBound.lean` | 6 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `NASAGaps.lean` | 12 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `book6/MayaCalendar.lean` | 10 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `book6/ReactionDiffusionFold.lean` | 3 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `book8/TurnaroundUniverse.lean` | 6 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `docs/ml-evidence/AXLE-tools-verify-core/probe_core.lean` | 0 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `lakefile.lean` | 0 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `tools/conclusion_scan.lean` | 0 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `tools/conclusion_scan_fixtures.lean` | 6 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `tools/verify-book8/probe_book8.lean` | 0 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |
| `tools/verify-dm3/probe_dm3.lean` | 0 | 0 | 0 | — | OUTSIDE EVERY TARGET | `—` | — |

## Axiom profile across every gate report in the corpus

| declarations | rests on |
|---:|---|
| 223 | `Classical.choice, Quot.sound, propext` |
| 52 | `(none — axiom-free)` |
| 49 | `Quot.sound, propext` |
| 32 | `propext` |
| 12 | `Classical.choice, Quot.sound, propext, sorryAx` |
| 4 | `sorryAx` |

An axiom-free proof is the strongest result `#print axioms` can report, and a checker that counts only the `depends on axioms:` form cannot see it (WP-73 §6). Both forms are counted here.

## Report lines that did not parse

A line announcing axioms in a shape the gate cannot read is a finding, never a silent skip.

- `geometry/tools/verify-audit/2026-09-09/Bhaskara.axioms.txt` — `'Bhaskara.brahmagupta'' depends on axioms: [propext, Quot.sound]`
- `geometry/tools/verify-audit/2026-09-09/Bhaskara.axioms.txt` — `'Bhaskara.brahmagupta'' depends on axioms: [propext, Quot.sound]`

`OUTSIDE EVERY TARGET` is the row to act on first: `lake build` never touches that file, so it can stop compiling and nothing will say so. `UNTRUSTED AXIOM` outranks it — a declaration resting on `sorryAx`, `Lean.ofReduceBool` or a `native_decide` axiom is disclosed, not audited.

Dates are file timestamps on the reports, not environment records. This ledger cannot tell STALE from still-true; `CS/verify-stamp` is the instrument that binds the triple.
