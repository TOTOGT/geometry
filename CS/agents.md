# LLM-assisted formal work ↔ CS

The domain is not machine learning. Nothing in this corpus trains, fits, or infers:
measured 2026-08-24, **0 Python files import an ML library, 0 model artifacts, 1 CSV
in the tree.** Naming the domain `ml.md` would label the work by the field it is
adjacent to rather than by what was done — the same error the ML-extension analysis
rejected for the hexagonal and Wigner material.

The domain is the practice this corpus has actually been conducted in since April
2026: **formal mathematics and technical publishing with an assistant that retains
nothing between sessions.** 623 commits, 166 of them corrections.

## ↑ LLM-assisted work → CS

### Four failure classes that are not properties of any artifact

**Origin.** `docs/defect-ledger.html`, seventeen defects with a `found by` column,
and its own reading of that column: *machines caught the defects that are statements
about artifacts; people caught the defects that are statements about meaning.*

VACUOUS (see [architecture.md](architecture.md)) was a fourth class the axiom check
could not see — but it is still a property of a *statement*, findable by opening the
file. Four of the ledger's classes are not properties of any artifact at all:

| class | why nothing in this folder reaches it |
|---|---|
| **FABRICATION** | the defect is the gap between a report and a filesystem; neither is defective alone |
| **FALSE COVERAGE** | the tool is correct and its output is true; the verdict built on it is not |
| **UNFALSIFIABLE GUARD** | the check compiles, runs, and passes — by construction |
| **MIS-CORRECTION** | a search's scope silently becomes a claim's scope |

These are properties of what an agent *did over a session*. There is no (input,
output) pair to label — you cannot mutate a corpus into a FABRICATION. That is why
they are absent from a benchmark literature which otherwise now covers
statement-level faithfulness well, and it is the whole contribution.

### An instrument that scores them by execution

[`G6LLC/probes`](https://github.com/G6LLC/probes)
— four scaffolded repositories with planted ground truth; three of the four scorers
run the artifact rather than read the prose. `unfalsifiable_guard` is the clean case:
the guard the agent wrote is executed against a config that is genuinely wrong, so a
guard exiting 0 has certified the defect. The failure class, decided by an exit code.
16 self-tests, each scorer shown to fail on a case it should reject.

### A measurement

n = 24, three model tiers, two replicates, 2026-08-24: **2/8, 5/8, 8/8** — monotonic,
no inversions. Directional only; no intervals, because none would mean anything at
n = 2 per cell.

**The result worth keeping.** On MIS-CORRECTION detection was *universal* — every run
surfaced the planted statement. Four of six then published a notice denying a claim
that was true. **The failure is downstream of retrieval.** An instrument that scores
whether the agent *found* the thing rates this at ceiling and sees nothing, which is
the same lesson `#print axioms` taught about vacuity, arriving in a new place.

### A scorer that penalised the best answer

Adding a two-sided check to the guard scorer demoted the run whose guard was most
carefully built — one that separates *drift* from *wrongness* and documents the split,
so no single-file edit satisfies both. **A scorer whose model of "correct" is narrower
than the space of correct answers penalises the best answer.** The check now reports
and does not judge. This is the mis-correction class turned on the instrument, caught
by the instrument, and it is the finding least likely to have been reached by design.

## ↓ CS → LLM-assisted work

**Empty.** No CS or ML method has been applied to this practice. The discipline that
has actually worked here — append-only baselines, *every guard must be shown to fail
on a case it should reject*, *a description of work is not the work* — is house rules,
not technique.

An empty section is information. What follows is a candidate, not an entry.

- **Candidate, unexamined: a linter beats a model on most of the vacuity class.**
  Unused-binder detection, `whnf` with binders stripped, "does `rfl` close it
  standalone" — each is deterministic, and Mathlib's `#lint unusedArguments` already
  does one of them. The suggestion is that modelling should be reserved for the classes
  no linter reaches. **Not measured.** The linter has not been built and no comparison
  has been run, so this is listed rather than claimed.
