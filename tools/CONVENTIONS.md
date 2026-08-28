# tools/ — naming and duplication conventions

Written 2026-08-25, after the word "vacuity" came to name three different
instruments in this repository and the same scanner logic appeared in four
files with two spellings inside an hour.

---

## 1. Name the mechanism, not the property

A property is what you are chasing. A mechanism is what the file does. Two
different mechanisms chasing the same property **must not share a name**, and
the failure that rule prevents is specific and has already happened here twice
in one day: a textual check standing in for a semantic one, and being believed.

On 2026-08-25 this repository had a CI step called **"Vacuity scan"** that
greps for the literal string `: True := trivial` in one directory and diffs the
result against a declared ledger. It is a good check. It is complete for what
exists today. It is **not** a vacuity scan — it cannot see `: True := by
trivial`, cannot see `∃ _, True`, cannot see a conclusion that *reduces* to
`True` through a definition, and does not read `SaturnHexagon.lean` or
`Orthogenesis/Geometry/` at all. Calling it one invited exactly the substitution
it should have prevented.

| Role suffix | Meaning | Example |
|---|---|---|
| `_gate` | decides a job; may fail the build | `axiom_gate.py` |
| `_scan` | reports findings; gates only where a step says so | `conclusion_scan.lean` |
| `_ledger` | a declared baseline that actual state is diffed against | `placeholder_ledger.txt` |
| `_fixtures` | specimens that prove the instrument fires | `conclusion_scan_fixtures.lean` |

**A file doing the same job carries the same name in every repository** —
`geometry`, `vol1-proofs`, `io`. If two repos disagree about what to call the
same instrument, at least one of them will end up with two of it.

### Current names and their targets

| Now | Target | Status |
|---|---|---|
| `tools/vacuity.lean` | `tools/conclusion_scan.lean` | **done** — never wired into CI, so free |
| `tools/vacuity_fixtures.lean` | `tools/conclusion_scan_fixtures.lean` | **done** |
| `tools/test_axiom_gate.py` | `tools/axiom_gate_fixtures.py` | deferred — referenced by CI here, by `run.sh` and CI in `vol1-proofs` |
| `Orthogenesis/Architecture/KNOWN_PLACEHOLDERS.txt` | `tools/placeholder_ledger.txt` | deferred — one `BASE=` line in `verify-proofs.yml` |
| CI step "Vacuity scan (declared placeholders vs actual)" | "Placeholder ledger (declared vs actual)" | deferred — cosmetic, do with the rename |

Deferred renames are deferred because they touch CI in more than one
repository, not because they are optional. Do each in one commit per repo.

### Added 2026-08-28

| File | Role | Note |
|---|---|---|
| `tools/declaration_scan.py` | `_scan` | resolves names used in prose against tracked sources across the corpus |
| `tools/declaration_scan_fixtures.py` | `_fixtures` | |
| `tools/textual_conclusion_scan.py` | `_scan` | **textual**; `conclusion_scan.lean` is the semantic instrument and is authoritative |
| `tools/textual_conclusion_scan_fixtures.py` | `_fixtures` | |
| `tools/corpus_roots.txt` | root set | one checkout per remote; see the corpus rule in `CLAUDE.md` |

`textual_conclusion_scan.py` is deliberately **not** named `conclusion_scan.py`.
Two mechanisms chasing the same property must not share a name (§1), and these
two differ exactly where it matters: the Lean scan reduces with `whnf` and sees
`∀ x ∈ S, x ∈ S := id`; the textual one cannot, and says so in its header. What
the textual one has is reach — it does not need the file to elaborate, so it
covers the ~2600 declarations in this corpus that no build currently touches.
Find candidates with the textual scan; confirm with the Lean one where the file
builds.

It was written on 2026-08-28 without noticing `conclusion_scan.lean` already
existed, which is the duplication this document exists to prevent. It is kept
because the reach is real, not because it was needed.

---

## 2. Every instrument is checked before its verdict counts

A gate that has never rejected anything is not known to work. Each `_gate` and
each `_scan` ships a `_fixtures` file carrying specimens it must catch and at
least one control it must not, and the fixtures run **before** the instrument's
verdict is read — step 0, not step last.

Three things this has already caught:

- `axiom_gate.py` failed **open** on Lean's wrapped output in its earlier form:
  continuation lines were dropped before the `sorryAx` test and the bracket
  regex never matched, so an admitted theorem returned GREEN. Demonstrated on a
  fixture, not argued.
- The Volume I fixtures once carried `import Mathlib`, silently failed to
  elaborate, and produced zero findings. The caller read that as clean. **A
  detector that did not run looks exactly like a detector that found nothing.**
  A fixtures file must depend on as little as possible, so it can test the
  instrument even when the corpus is broken.
- `vendor_check.py`, below, passed with **zero files hashed** in its first
  draft — it printed a summary and returned 0. Found by its own negative test,
  fixed in the same hour.

The general form: **an empty check is not a passing check.** Any instrument
that can examine nothing must fail when it examines nothing, and must report
the count it examined so a caller can assert it.

---

## 3. Duplicated logic carries a marked block and a digest

Some duplication is correct. `conclusion_scan_fixtures.lean` restates the
scanner rather than importing it, precisely so it elaborates when the corpus
does not — that is what makes it a test of the instrument. The problem is not
the copy. The problem is that a copy drifts silently.

Duplicated logic is wrapped in explicit markers:

```lean
-- BEGIN SHARED BLOCK conclusion_scan_core -- see tools/vendor_manifest.json
...
-- END SHARED BLOCK conclusion_scan_core
```

`tools/vendor_manifest.json` records, per instrument: what it is, which repo is
canonical, every copy, the shared-block name, and one sha256 of the
comment-stripped block. `tools/vendor_check.py` recomputes and fails on any
difference.

Comments are excluded from the hash on purpose — a vendored copy **should**
carry its own header saying where it came from and what it is scoped to. What
must not differ is the logic.

**Canonical home for shared instruments is `geometry/tools/`.** Other
repositories vendor from here and record the same digest in their own manifest.

To change a shared instrument: edit the canonical copy, re-vendor every copy,
run `--update`, **read the diff**, commit. Never run `--update` to silence a
difference you have not explained — that converts a detector into a rubber
stamp, which is this repository's most-repeated defect wearing new clothes.

---

## 4. Every rule carries the incident that caused it

Each tool's docstring records the defect that produced it: `claims.py` names
the CatGT DOI misattribution and the `doi.org/Zenodo community` sweep;
`axiom_gate.py` names CI run #245; `audit.py` names the unaudited repo root;
`vendor_check.py` names the four-copy drift.

A rule without its origin is a rule a future maintainer deletes as noise, and
the deletion looks like cleanup.

---

## 5. What no instrument here can see

Stated so it is not rediscovered a fourth time.

- **Everything outside the tree.** `audit.py` and `claims.py` read HTML in the
  working tree. Zenodo deposit metadata, GitHub repository descriptions, and
  the three sibling sites off-domain are not in it. The phantom series-DOI
  relation reproduced into a published record on 2026-08-24, six days after the
  sweep that "fixed" it, because the deposit form is outside the audited
  boundary. Any claim that something is fixed is scoped to the tree and must
  say so.
- **The seam between two correct scopes.** `audit.py` skips external URLs by
  design; `claims.py` resolves identifiers, so it cannot handle one too broken
  to be an identifier. `href="https://doi.org/Zenodo community"` was invisible
  to both for six days. A validator that works by dereferencing needs a
  well-formedness gate in front of it.
- **A `.lean` file in no build target.** Checked by nothing, however green the
  badge. `SaturnHexagon.lean` sat outside every target for a month while its
  header asserted it was kernel-verified and three of five theorems were
  admitted.
- **Whether a theorem asserts anything.** `#print axioms` certifies that a proof
  establishes its proposition and says nothing about the proposition.
  `conclusion_scan.lean` covers part of this — trivially inhabited conclusions.
  It does **not** detect unsatisfiable hypotheses, which is the other thing
  "vacuous" means. Report it as what it checks.
