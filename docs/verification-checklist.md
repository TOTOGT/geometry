# Verification checklist

The order is the content. Each stage exists to make the next one mean something;
run them out of order and the later checks compare true statements against the
wrong object.

Narrative version: Book VI, *The Hydrated Lattice*, §6.

Status column: `done` — implemented and running. `partial` — implemented for some
roots or some cases. `open` — not implemented.

## Stage 0 · The reduction ladder

Information is what a reader can hold. Data is what a machine crunches. The two
must not meet, and the cost of confusing them is paid in attention and in error.

Each rung below is produced from the one beneath it **by a program**. Nothing
reads downward. If a question can only be answered by reading a lower rung, the
rung above it is missing a field — that is the bug, and it is fixed by adding
the field, never by reading the log.

| Rung | What it is | Size | Read by |
|------|-----------|------|---------|
| 0 · Data | `run.log`, elaboration output, stack traces | unbounded | nothing; kept on disk, addressed by path |
| 1 · Records | one gate file per declaration set | ~30 lines each | programs |
| 2 · Table | one row per file | ~280 rows | programs; scanned by a person |
| 3 · Information | the summary | under ~20 lines | a person, or a model |
| 4 · Artifacts | audit entry, index and README updates, chapter revisions, Lean repairs | as needed | readers |

### Rung 2 — the table

One row per file, fixed fields, no prose:

```
project  path  sha256[:12]  toolchain  verdict  declared_sorries  actual_sorries  declarations  seconds
```

`verdict` is closed: `PASS` · `PASS-AS-DECLARED` · `UNDECLARED-SORRY` ·
`AXIOM-VIOLATION` · `COUNT-MISMATCH` · `FAIL` · `NOT-VERIFIABLE`.

### Rung 3 — the summary, and the delta rule

**A run's information content is its delta.** A file that passed yesterday and
passes today contributes nothing and must not be printed. The summary is:

1. counts per verdict class, one line;
2. every row whose verdict or sha changed since the last run;
3. every row requiring a decision that a program cannot make.

A clean night is three lines. A night with one new undeclared sorry is four, and
the fourth is the one that matters. A summary that grows with the corpus is not a
summary, and a report that prints 44 failures which are all the same fact has
moved data into a place where only information belongs.

### The price of a probe

Every test is charged, and the charge does not scale with how much you learn from
it. Two consequences, and the second is the one that gets forgotten.

**A probe that cannot surprise you is not a test.** Write both outcomes down
before running it, and what each one settles. If you cannot name the result that
would change your mind, the run is reassurance, and it is billed at the same rate
as evidence. This is the same discipline the chapters apply to a claim, turned on
the instrument.

**A long input is not read evenly.** The end is answered; the middle is skimmed.
That is a property of the reader and not a defect in the writing, and it cannot be
argued with — a corpus handed over whole buys one paragraph's worth of attention,
spent wherever the text happens to stop. So:

- **One decision per summary, and it goes last.** Counts first, delta second, the
  question needing a human at the bottom, where attention actually lands.
- **Two decisions are two summaries.** Concatenated, the second is the one that
  gets answered and the first is the one you will believe was considered.
- **What must survive belongs on disk, not in a conversation.** Anything carried
  forward only in context is being carried at falling resolution, and the fall is
  invisible from inside. This directory exists for that reason and not for
  tidiness.

### The consequence for authoring

Rung 4 is where writing happens, and it is the only rung where it happens. Reports,
Lean repairs, HTML, index and README updates are all *downstream of a computed
answer* — never of a scan. The practical test: if a paragraph could not be
regenerated from rung 3 alone, it is resting on something nobody can check.

---

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
