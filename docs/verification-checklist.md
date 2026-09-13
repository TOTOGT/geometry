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

### Implementation

`tools/verdict_table.py` writes rung 2 (`verdicts.tsv`) from artifacts already on
disk; it never invokes Lean. `tools/verdict_summary.py` writes rung 3, diffing
against the most recent earlier table. Neither reads `run.log`.

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
answer* — never of a scan.

Two tests, and a paragraph must pass both.

**Compression.** Could this paragraph be regenerated from rung 3 alone? If not, it
is resting on something nobody can check.

**Descent.** Does it carry the address of the data it was compressed from? Routine
operation never reads downward — but *every artifact must publish the way down*,
or it is checkable only by its author, which is the first failure wearing better
clothes. Compression without a path back is not a summary; it is a claim.

#### An address is a triple, not a name

`(path, sha256, date)`. A name is not an address: a corpus with three copies of a
file under one basename can cite a declaration accurately and still point at the
wrong object, and a link to a file that has since changed is not a citation of the
thing that was checked. The sha is what makes the reference survive the file.

#### What each artifact must carry

| In the artifact | The link it must publish |
|---|---|
| "machine-checked" | the gate file: declaration, project, file `(path, sha, date)`, toolchain pin, axiom manifest |
| a number, constant, or figure | the verification script and the block inside it that recomputes it, plus the command to run it |
| a measurement taken from elsewhere | the source deposit and its DOI, and whether this work re-derived it or took it as given |
| a dataset or micrograph | where to obtain it, licence, and the accession or figure number |
| an open obligation | the declaration name, the file, and the closure path |
| the environment | the toolchain and library versions, pinned, so the run can be reconstructed |

This is the same disclosure standard §6 of the interstitium chapter asks of the
formal-verification movement. It applies here first, or asking it of anyone else is
rhetoric.

---

## I · Make the report refer to a definite object

| # | Step | Status | Where |
|---|------|--------|-------|
| 1 | Every report line carries project root and toolchain, not the basename | done | `tools/verdict_table.py` derives both from the resolved source path and flags `AMBIGUOUS` when a basename has several copies |
| 2 | Anything this environment cannot verify gets one `NOT-VERIFIABLE` line with the reason — frozen deposits, archives, `to_delete/`, lakefiles, and any root declaring a different toolchain | open | `tools/corpus_roots.txt` has no toolchain column |
| 3 | Deduplicate by sha256, never by basename; report mirrors as identical-to | partial | every row carries its sha; mirror collapsing not yet done |

Step 2 is the large one. Only `geometry` has a built Mathlib; every other root on
disk declares a toolchain it cannot currently meet, so elaborating those files
against `geometry`'s toolchain measures nothing.

## II · Make the verdict mean something

| # | Step | Status | Where |
|---|------|--------|-------|
| 4 | `#print axioms` per declaration, compared against the permitted set; the gate is the verdict, never a grep | done | `tools/axiom_gate.py` |
| 5 | Tactics that are not kernel checks are named as such | done | gate prints the `native_decide` / `Lean.ofReduceBool` line |
| 6 | Declared obligations matched against actual ones; declared-and-present is `PASS-AS-DECLARED`, undeclared-and-present is the only red | done | `tools/verdict_table.py` reads `GATE-DECLARE: sorries = …` (preferred, named) or the incumbent `EXPECTED under \`--audit\`` counts; absence of both is `UNDECLARED-STATUS`, never a guess |
| 7 | Declaration count asserted: expected *n*, found *n* | done | `COUNT-MISMATCH`; the parser handles names ending in a prime and rejoins axiom lists that `#print axioms` wraps across lines |

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

---

## Stage IV has an ancestry, and it is not ours

Nothing in this document is new. Akṣapāda Gautama's *Nyāya Sūtra* already
carries the whole apparatus, and carries it better specified than the version
assembled here this week.

Priority is not the claim and is not needed. The core of the text is placed
around the 2nd century BCE and the redaction that survives is often put several
centuries later; on either dating Aristotle's *Organon* is earlier, and the
debate tradition Nyāya codifies is older than either text. What matters is that
the two traditions are independent, and that Nyāya **kept three things the Greek
form discarded as redundant** — the three this document spent a week
rediscovering.

**1. The worked instance travels with the rule.** The Greek syllogism is premises
and conclusion. Nyāya's inference has five members: the claim (*pratijñā*), the
reason (*hetu*), **the general rule together with an example** (*udāharaṇa*), its
application to the case (*upanaya*), and the conclusion (*nigamana*). The third
member exists so that an argument establishes not only validity but factual
anchoring — the rule must be shown holding *somewhere*, in a case a listener can
check. That is rung 4's descent test, stated two thousand years earlier: an
argument carries the address of its evidence, not merely its form.

**2. Failure is enumerated, not narrated.** *Nigrahasthāna* — points of defeat —
is one of the sixteen categories of the system, and *hetvābhāsa* names five ways a
reason can merely appear to be one: inconclusive, contradictory, counterbalanced,
unproven, and mistimed. A catalogued taxonomy of how argument fails, built into
the framework rather than accumulated by accident afterwards. That is stage IV,
and Nyāya did not need to be wrong in public for years first to get it.

**3. Warrant has a closed set of kinds.** The four *pramāṇa* — perception,
inference, comparison, and testimony — are kinds of knowing, not degrees of
confidence, and testimony is admitted as its own bounded source with its own
conditions rather than smuggled in as weak perception. Our verdict set is a
*pramāṇa* taxonomy and should be read as one: a kernel record and a page's
assertion are different **kinds** of warrant, not the same warrant at different
strengths. Confusing the two is the defect this whole document exists to prevent,
and it is the one Nyāya ruled out by construction.

### Two axes, and we inherited one

The convergence is the first half of the point: two traditions, out of contact,
both isolate inference as a thing with parts, both name the ways a reason fails,
both build an apparatus for adjudicating a claim in public. That is the grammar
reappearing.

The second half is that they then developed **different axes**, and it is worth
being exact about which, because the asymmetry is not a matter of one side being
cleverer.

*Where the Greek line went further.* Aristotle's schematic letters — *A belongs to
all B* — abstract form from content, and that single move is what eventually made
logic mechanisable. The Stoics added propositional connectives and their inference
schemes. Nyāya's inference deliberately stays attached to content: the
*udāharaṇa* is required *because* content matters, which is a strength for
adjudication and an obstacle to formalisation. The line that runs to Frege, to
Mathlib and to a Lean kernel is the Greek one, and it is not an accident that it
is.

*Where Nyāya went further.* On the question of when instances license a general
claim, Greek *epagōgē* is thin and the problem stays open until Sextus and then
Hume; Nyāya built *vyāpti* into a theory, with *upādhi* — the limiting condition
that silently defeats a concomitance — as a named object to be searched for before
the inference is granted. And the syllogistic stayed substantially unchanged from
Aristotle to the nineteenth century, while the Indian tradition kept developing:
Gaṅgeś́a's *Tattvacintāmaṇi* and the Navya-Nyāya after him built a technical
language for relations and for negation of relational complexes that Ingalls and
Matilal both argued is more expressive than the syllogism ever became.

**And the instrument we use inherited the Greek axis only.** A Lean kernel is
form abstracted from content, executed perfectly. Every defect this document
catalogues lives on the other axis: whether the theorem says what was meant,
whether a name claims more than its proof, whether a sweep holding one parameter
fixed has established a concomitance or merely confirmed itself, whether
"machine-checked" on a page and a gate record are the same kind of warrant. Those
are *upādhi* questions and *pramāṇa* questions. The compiler cannot be blamed for
being silent about them; it descends from the tradition that set them aside in
order to become a compiler.

So the checklist is not an eccentric addition to formal verification. It is the
half of the apparatus that formalisation left behind on its way to being
mechanical, arriving late and under-specified, and the useful move is to go
read the tradition that kept it rather than to keep deriving it from failures.

### Derived, not transmitted — and the third instance is this repository

Neither system was copied from the other and neither was learned. Each was
**derived**, from the same first principles, by people addressing the same
problem: how does a claim earn assent, and how does it fail.

The differences are the evidence. Transmission produces the same decomposition
in local vocabulary. What is actually there is two systems that agree completely
on *what the problem is* — inference has parts, reasons fail in nameable ways,
warrant comes in kinds — and disagree on how to cut it: five members against two
premises, an epistemology of *pramāṇa* against a theory of formal validity, the
worked instance kept against the worked instance discarded. That is the signature
of convergent derivation. Copying does not produce disagreement at the joints
while producing agreement about where the joints are.

Which changes what the observation is worth. A parallel is a curiosity. Two
independent derivations mean the apparatus is a property of **the problem** — of
inference held up to scrutiny — and not of a culture, a language, or a period.

And there is a third instance, which is the reason to write this down here rather
than in a history: **this repository derived it again, this month, from a night of
Lean failures.** Nobody consulted Akṣapāda. The twelve steps came out of a report
that named a frozen deposit as if it were a live file, a parser that dropped a
declaration whose name ended in a prime, a wrapped axiom list hiding a `sorryAx`,
and a sweep that varied one axis of a two-axis claim. From those, and only those,
came: keep the worked instance with the rule; name the ways a reason fails;
distinguish kinds of warrant. Three of Nyāya's central commitments, reached
backwards from broken output.

Two independent derivations across two millennia are suggestive. A third, whose
provenance is documented commit by commit in `docs/audit-log.md` and can be
audited by anyone who doubts it, is a different kind of evidence — because the
usual objection to any such parallel is that transmission cannot be excluded, and
here it can. The derivation is in the history of this repository.

The practical consequence is the one worth acting on: stop deriving it from
failures. *Vyāpti* — invariable concomitance, and *upādhi*, the limiting condition
that defeats it — is precisely the question of when a sweep over instances
licenses a general claim, which is step 10 and is currently answered by hand. That
work has been done. Read it before rediscovering it a fourth time.

---

## Building it: what exists, what is missing

Measured 2026-09-13: **96 pages** in this corpus assert a verification claim
(*machine-checked*, *kernel-checked*, *verified symbolically*, *independently
verified*). **47** verification scripts recompute what they accompany. The verdict
table covers **45** Lean files. Nine defect classes are in use, all applied by hand.

| Nyāya part | What it does | What exists here | What is missing |
|---|---|---|---|
| *pratijñā* | the claim, stated as a claim | the sentence on the page | claims are prose inside HTML; there is no registry in which a claim is an object with an id |
| *hetu* | the reason offered for it | declaration name, gate record, `verdicts.tsv` | present for Lean, absent for most of the 96; nothing links claim to reason mechanically |
| *udāharaṇa* | the rule **and** a checkable worked instance | 47 verification scripts; the address triple | not required. A page may assert and cite nothing, and nothing notices |
| *upanaya* | *this case is of that kind* | — | nothing states that a given file instantiates the rule its page cites. This is where the frozen-deposit confusion lived |
| *nigamana* | concluded, and marked as concluded | the published sentence | a page does not distinguish *claimed* from *established*; both are prose |
| *pramāṇa* | a closed set of **kinds** of warrant | closed verdict set, for gate outcomes only | no warrant-kind on a published claim. "Machine-checked" and "independently verified numerically" are different *pramāṇa* and are written as though they were one thing at two strengths |
| *hetvābhāsa* | named types of merely-apparent reason | 9 defect classes in `audit-log.md` | no mapping to the five, no detection of any of them |
| *nigrahasthāna* | procedural defeat in adjudication | checklist stage III | entirely manual |
| *vyāpti* / *upādhi* | when instances license the general claim, and the condition that silently defeats it | — | **the largest gap.** Step 10, wholly by hand. This is the WP-84 defect: a sweep over nine values of *N* at fixed *k*, confirming itself |

### The five, mapped

The nine classes already in use are the five *hetvābhāsa*, plus two that are not
fallacies of reason at all. The correspondence was not designed:

| *hetvābhāsa* | Reason that only looks like one | Our class |
|---|---|---|
| *savyabhicāra* | strays — holds also where the conclusion does not | `OVER-GENERALISED` |
| *viruddha* | contradicts what it is offered to prove | `FALSE` |
| *prakaraṇasama* | counterbalanced by an equal opposing reason | `UNTRUSTED` |
| *sādhyasama* | itself unproved; assumes the thing | `VACUOUS`, and any theorem resting on `sorryAx` |
| *kālātīta* | mistimed — offered after its moment has passed | `STALE` |

`MISMATCH`, `MISATTRIBUTED` and `MISFRAMED` are not defects of reason; they are
*nigrahasthāna*, failures of the adjudication rather than of the argument.
Keeping them in one list obscures that, and is why a night's report could not
separate a broken proof from a broken reader.

### What to build, in order

1. **`tools/claim_table.py` — the claim registry.** One row per asserted claim
   across the 96 pages: page, claim id, warrant kind, *hetu* (declaration, or
   script and block), address triple, gate verdict, date. This one artifact
   supplies *pratijñā*, *hetu*, *upanaya* and *nigamana* together, and makes step
   11 mechanical instead of a grep.
2. **Warrant kind as a closed set** — the *pramāṇa* field, five values, each with
   its own required address: `kernel` (gate record), `recomputed` (script and
   block), `measured` (instrument and dataset), `cited` (deposit and DOI, and
   whether re-derived), `argued` (no address, and must say so). A page that
   cannot name its kind has not made a claim.
3. **`tools/sweep_audit.py` — the *upādhi* check.** For a claim quantified over
   parameters, verify the accompanying script varied *every* one. Nine agreeing
   points along a single axis is not a concomitance. This is the only genuinely
   new instrument on the list, and the one that would have caught WP-84 with
   nobody reading the sweep.
4. **Split the ledger** into reasons and procedures, per the table above.

Items 1, 2 and 4 are bookkeeping the corpus already half-does. Item 3 is the part
nobody here has built, and the part Nyāya spent centuries on.
