# Architecture ↔ CS

## ↑ Architecture → CS

### A fourth class: VACUOUS — the check passes and means nothing

**Origin.** `Orthogenesis/Architecture/` formalises lattice claims for acoustic,
magnetic, seismic and crystal structures. Measured 2026-08-21:

| file | lines | theorems | defs | `sorry` |
|---|---|---|---|---|
| `AcousticLattice.lean` | 192 | 11 | 5 | 3 |
| `DM3Bridge.lean` | 224 | 14 | 6 | 0 |
| `G6Crystal.lean` | 364 | 29 | 20 | 11 |
| `MagneticLattice.lean` | 283 | 20 | 9 | 8 |
| `SeismicLattice.lean` | 225 | 17 | 5 | 6 |
| **total** | **1288** | **91** | **45** | **28** |

Six of those 91 are live placeholders of the form `: True := trivial`:

```
AcousticLattice.lean:166   full_diffraction_spectrum_placeholder
AcousticLattice.lean:171   intentionality_placeholder
AcousticLattice.lean:175   quetzal_match_placeholder
MagneticLattice.lean:259   neutron_selection_rule_placeholder
SeismicLattice.lean:187    hexagrid_collapse_superior_placeholder
SeismicLattice.lean:194    crack_tortuosity_placeholder
```

**Finding.** These are a *fourth* failure class, and the instrument built for
the first three cannot see it.

MISMATCH, STALE and FAIL all concern whether a **proof** still supports a
statement. VACUOUS concerns whether the **statement says anything**. A theorem
`: True := trivial` compiles cleanly, depends on no axioms beyond the standard
three, contains no `sorry`, and reports exactly what a real theorem reports.
`#print axioms` is the wrong instrument by construction: it asks what a proof
rests on, and a trivially true statement rests on nothing. The check passes,
truthfully, and certifies nothing.

| | question asked | detects |
|---|---|---|
| MISMATCH | is this the artifact that was checked? | hash |
| STALE | is this the environment it was checked in? | probe |
| FAIL | does the check still pass? | re-run |
| **VACUOUS** | **does the statement have content?** | **nothing yet** |
| **FALSE** | **is the statement true at all?** | **elaboration, and only if a build target reaches the file** |

**Why it survives here.** The Architecture library *is* in a build target —
`lean_lib Orthogenesis`, imported by `Orthogenesis.lean` — so `lake build`
compiles all 91 theorems on every push. But the CI axiom probe names only the
five `SaturnHexagon` theorems. None of the 91 is axiom-checked, and even if all
91 were, the six placeholders would pass.

So the corpus contains two distinct blind spots stacked: theorems outside the
probe, and theorems the probe cannot judge even when aimed at them.

**Detection sketch, not built.** A statement-level check: reject a `theorem`
whose type is `True`, or whose type is an implication from a hypothesis to
itself, or which quantifies over nothing and asserts a decidable closed
proposition already reducible by `decide`. Textual grep finds the obvious
shapes — that is how these six were found — but a real check has to work on the
*elaborated type*, not the source text, or it will miss anything written
indirectly and flag anything mentioned in a comment.

**Open.** The six placeholders are unresolved. Each should become a real
statement or be deleted; leaving them is the corpus asserting 91 theorems while
85 are load-bearing. Deleting them is not a decision this file can make.

### A fifth class: MISATTRIBUTED — the statement is proved, the claim credited to it is not

**Origin.** CI run #238 (`8855044`, branch `verify-hardening`) is green:
seventeen theorems probed by name, no `sorryAx`, vacuity baseline matching the
file. Twelve of the seventeen are in `Orthogenesis/Architecture/NASAGaps.lean`,
which indexes each theorem against a NASA Moon Base functional gap code. The
green says nothing about whether a theorem answers the gap it is filed under, so
the twelve statements were read against their gap codes on 2026-08-22.

(`NASAGaps.lean` and `Coverage.lean` entered the build on 2026-08-21 and are not
in the measured table above.)

| theorem | what the statement proves | what it is filed as |
|---|---|---|
| `FN_A_104L_reachability` | `C₀.cells ⊆ (expandN n C₀).cells` — the seed cells survive n steps | "every cell in `expandN n C₀` is reachable from C₀ in exactly n steps" — the converse inclusion |
| `FN_L_101L_unique_interface` | `h₂ ∈ N(h₁) → h₁ ∈ N(h₂)` — adjacency is symmetric | "any two neighbouring cells share exactly one interface face" |
| `FN_U_103L_six_layers` | `n_layers = 6`, by `decide` on a literal | "each completed layer contains sufficient processed regolith to seed one additional module" |
| `FN_U_103L_expand_models_ISRU` | `C.cells ⊆ C.expand.cells` — monotonicity, true of `expand` by construction | "one expand = one ISRU cycle" |
| `FN_T_202L_payload_ratio` | `payload_phase02 / payload_phase01 = 15` in ℕ, so any true ratio in [15, 16) satisfies it | confirmation that g² ≈ 14.98 |

Every one is true. Every one is proved. Each reports the standard three axioms.
None supports the sentence recorded against it. `FN_A_104L_reachability` is also
re-exported into `nasa_gap_closure_summary`, so the mislabel travels into the
machine-readable table a reader is pointed at.

**Finding.** VACUOUS asks whether a statement says anything. MISATTRIBUTED
concerns a statement that says something real and is credited with something
else. The defect is in neither half: the Lean is correct, the prose is a
coherent claim, and the error is only in the join between them. That is why no
layer reports it — every layer is examining one side.

| | question asked | detects |
|---|---|---|
| MISMATCH | is this the artifact that was checked? | hash |
| STALE | is this the environment it was checked in? | probe |
| FAIL | does the check still pass? | re-run |
| VACUOUS | does the statement have content? | nothing yet |
| FALSE | is the statement true at all? | elaboration, and only if a build target reaches the file |
| **MISATTRIBUTED** | **does the statement support the claim made from it?** | **nothing, and nothing can** |
| **UNTRUSTED** | **does the proof rest on the kernel?** | **an axiom allowlist — mechanisable, not mechanised** |

**The class was stated here before it was named.** `NASAGaps.lean` §POWER,
2026-08-21, reopening two gaps that had been answered by re-exporting true
theorems about unrelated quantities: *"re-exporting a true statement under a gap
code does not address the gap"* — it makes the gap table look answered. Two
further theorems were deleted the same day as `x ∈ S → x ∈ S := id`. That sweep
was this class being found by hand, one instance at a time, without a name; the
five above are what the same reading finds when it is run to completion.

**Why no instrument in this folder can decide it.** MISMATCH, STALE and FAIL are
mechanical — both sides of each comparison are machine-readable. VACUOUS is
partly mechanical: the elaborated type is a formal object, so a checker can
reject `True` and self-implication. MISATTRIBUTED is the first class where one
side of the comparison is a natural-language sentence. Deciding it means
deciding whether a Lean proposition entails an English claim, which is not a
decision procedure and will not become one. This is the ceiling of the
verification stack and should be stated as a ceiling: **the stack can certify
that a proof supports a statement, and can never certify that a statement
supports a claim.** Everything above that line is review.

**Detection sketch, not built.** What is mechanisable is the bookkeeping, not
the judgement. Require every theorem cited in a claims table to carry a
machine-readable claim identifier; require every claim identifier in the prose
to resolve to exactly one theorem; fail on either side unmatched. That catches
drift — a renamed theorem, a gap code whose theorem was deleted, a theorem
quietly repointed at a second gap — and catches nothing about whether the
pairing was ever warranted. This is the same instrument `ROUTINE.md` lists as
*not yet built* under "a document linter", and this entry fixes its ceiling in
advance: it can enforce that a link exists and that a person signed it, never
that the link is warranted.

The residual judgement has an honest form, and it is a three-column table —
statement as written, what it strictly licenses, what is claimed from it. The
gap between columns two and three is the audit. It has to be signed, because a
person is the only thing that can produce it.

**Open.** The five above are unrepaired; each is a rename, a restatement, or a
reopening, and which one is an authorial call. The sixth row is also live:
`FN_H_102L_phase02_cluster` depends on
`G6Crystal.colony_depth1_cells._native.native_decide.ax_1_1`, so one of the
twelve is checked by compiled code rather than by the kernel, in a step named
"Kernel axiom check". The gate greps for `sorryAx` and cannot see it. An
allowlist over `propext`, `Classical.choice` and `Quot.sound` is a two-line
change and closes UNTRUSTED for good.

---

## ↓ CS → Architecture

*(nothing filled)*

- **Candidate, unexamined.** `SeismicLattice.lean` and `G6Crystal.lean` make
  comparative claims about hexagonal grids under collapse. Whether any is in a
  state where a machine check would mean something has not been assessed — and
  the two `hexagrid_collapse` placeholders suggest the comparative claim is
  currently asserted rather than proved.
- **Candidate, unexamined.** `AcousticLattice.lean` carries an
  `intentionality_placeholder`. Whatever it is meant to state, a claim about
  intentionality is not the kind of thing a lattice formalisation can settle,
  and it should be looked at before it acquires a proof-shaped wrapper.
