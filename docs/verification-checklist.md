# Verification checklist

The order is the content. Each stage exists to make the next one mean something;
run them out of order and the later checks compare true statements against the
wrong object.

Narrative version: Book VI, *The Hydrated Lattice*, §6.

Status column: `done` — implemented and running. `partial` — implemented for some
roots or some cases. `open` — not implemented.

## I · Make the report refer to a definite object

| # | Step | Status | Where |
|---|------|--------|-------|
| 1 | Every report line carries project root and toolchain, not the basename | partial | `tools/leancheck.sh` writes `<project>__<file>` gates as of 2026-09-12; older reports do not |
| 2 | Anything this environment cannot verify gets one `NOT-VERIFIABLE` line with the reason — frozen deposits, archives, `to_delete/`, lakefiles, and any root declaring a different toolchain | open | `tools/corpus_roots.txt` has no toolchain column |
| 3 | Deduplicate by sha256, never by basename; report mirrors as identical-to | open | 280 paths, 163 distinct basenames |

Step 2 is the large one. Only `geometry` has a built Mathlib; every other root on
disk declares a toolchain it cannot currently meet, so elaborating those files
against `geometry`'s toolchain measures nothing.

## II · Make the verdict mean something

| # | Step | Status | Where |
|---|------|--------|-------|
| 4 | `#print axioms` per declaration, compared against the permitted set; the gate is the verdict, never a grep | done | `tools/axiom_gate.py` |
| 5 | Tactics that are not kernel checks are named as such | done | gate prints the `native_decide` / `Lean.ofReduceBool` line |
| 6 | Declared obligations matched against actual ones; declared-and-present is `PASS-AS-DECLARED`, undeclared-and-present is the only red | open | files already declare theirs in Status / Open Obligations blocks — the gate does not read them |
| 7 | Declaration count asserted: expected *n*, found *n* | partial | fires for some files; the parser mis-handles declaration names ending in a prime |

Step 6 is the one that changes what the nightly job is for. Six files currently
refuse the gate; every one of them declares its own sorries in prose, and every
page citing them says `OPEN (sorry)`. Until the gate reads the declaration, a
seventh file growing an *undeclared* sorry arrives indistinguishable from the six.

## III · Make the claim mean what the page says

| # | Step | Status |
|---|------|--------|
| 8 | Formal statement read back against the sentence citing it — do the quantifiers match the prose? | open, manual |
| 9 | The declaration name treated as a claim: *unconditional*, *every*, *iff*, *optimal*, a named constant | open, manual |
| 10 | Every free axis varied; a sweep holding one parameter fixed confirms itself | open, manual |
| 11 | Each published "machine-checked" traced to a gate file naming that declaration, in that copy, on that date | open |

No compiler performs any of these. Most of the corpus's recorded defects are here.

## IV · Make it a study rather than a chore

| # | Step | Status | Where |
|---|------|--------|-------|
| 12 | Every miss logged with a class and a date; corrections left standing in the text rather than withdrawn | done | `docs/audit-log.md` |

Classes: `MISMATCH`, `STALE`, `FAIL`, `FALSE`, `VACUOUS`, `UNTRUSTED`,
`MISATTRIBUTED`, `OVER-GENERALISED`, `MISFRAMED`.

One instance of any class is an anecdote. The count is the finding, and the count
is the only thing that can say what the instrument systematically misses.
