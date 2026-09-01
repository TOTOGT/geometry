# docs/ml-evidence — retained evidence of machine-assisted production

**These files are kept on purpose. Nothing here is scheduled for deletion.**

The corpus is produced with machine assistance, and the corpus publishes findings
about that production. A finding needs its artefact: when a page is corrected, the
superseded copy is the evidence that the correction happened and what it changed.
This folder is where those artefacts live.

Established 2026-09-01. Before that the same files sat in `_to_delete/`, which is
gitignored — so none of this had ever been in version control, and the folder name
said "delete" while the intent was "keep". Moving them here puts the evidence in git
history, where it can be cited and where it survives a cleared working tree.

## Rules

1. **Nothing here is live.** Every HTML file in this folder is superseded, stale,
   misplaced, or a backup. The live copy is elsewhere in the repo.
2. **The tooling skips this folder, deliberately.** `tools/build_indexes.py` does not
   index it (a superseded copy indexed as a live page is a false orphan) and
   `tools/audit.py` excludes it from both the link scan and the working-paper number
   index (`wp73` and `wp80` copies here must not collide with the live pages carrying
   those numbers). Both skips carry a comment pointing back at this README.
3. **Do not repair files here.** A dead link inside a superseded copy is part of the
   evidence. Fixing it destroys the record.
4. **Add, don't overwrite.** When a page is retired, move the old copy in under a name
   that says what it was and why it went, and add a line to the table below.
5. **Deletion is a separate decision.** If a cluster is ever genuinely finished with,
   it gets removed in its own commit that says what was removed and why — not swept
   into a cleanup.

## What is here

| Path | Files | What it documents |
|---|---|---|
| `superseded-copies/` | 18 | Retired duplicates: the root copy of `omega-point-index`, the stale `HVEH_index` homepage copy, the original three-document `omega-point-v2-draft`, seven `omega/` pages and eight `HVEH_proofs/` pages. The concatenated-documents defect that `tools/audit.py` was rewritten to catch (`<!DOCTYPE` counting, not tag balance) was found in this set. |
| `bak/` | 14 | Pre-edit backups from the Jun–Aug 2026 sweeps, flattened with their source path in the filename (`book4_ch07.html.bak` was `book4/ch07.html`). Includes `book6_policy_SITE_ERRATA.md.bak` and the crop-circle briefing `.tex`. These are the before-images for the corrections recorded in `docs/audit-log.md`. |
| `book4/` | 4 | Place-named Book IV chapters (`ch06b-elojo`, `ch07-newark`, `ch08-harrison`, `ch09-belleville`) as they stood before the surviving copies were reconciled. |
| `chIV/` | 3 | The `-fixed` variants of `chIV-correspondence`, `chIV-operators` and `chIV-recursion` — a repair pass kept beside its target rather than over it. |
| `AXLE-tools-verify-core/` | 3 | `probe_core.lean`, `run.sh`, `axioms.txt` from the AXLE verify-core probe. Kept because the axiom output is the artefact a published kernel-check count rests on. |
| `deposits-moved-to-GTCT-2026-08-30/` | 4 | The `rh-arithmetic-contact-v1` deposit staging set (`ZetaReflection.lean`, `verify_reflection_laws.py`, `METADATA.md`, `RH_arithmetic_contact_structure.md`) as it stood when the deposit work moved to the GTCT repo on 2026-08-30. |
| `stray-numeric-files/` | 5 | Zero-content files named `book6-1`, `book7-1`, `omega_1`, `HVEH_places_1`, `HVEH_proofs_1` — shell-redirect artefacts. Evidence of the mechanism, not of any claim. |
| `wp80-the-registry-and-the-kernel-superseded.html` | 1 | The superseded WP-80. The live page is `book6/wp80-the-theorem-and-the-reader.html`; this copy is what it replaced. |
| `wp73-dnls-d6-ring.html.SUPERSEDED` | 1 | Superseded WP-73; the live page is `book6/wp77-dnls-d6-ring.html`, i.e. the number moved as well as the content. |
| `_cajueiro-index-misplaced.html` | 1 | A Cajueiro index written to the wrong directory. |
| `audit-log.md.bak-2026-08-30` | 1 | `docs/audit-log.md` before the 2026-08-30 edits. |
| `OrthogonalWitness.lean.bak` | 1 | Pre-edit copy of the orthogonal-witness Lean file. |
| `AMonster/law-of-monsters-v2.html` | 1 | Superseded v2 of the Law of Monsters page. |
| `V4,` | 1 | Zero bytes. A shell typo — a `V4,` argument that became a filename. Kept because it is the smallest possible example of the class, and because the class is real: see `stray-numeric-files/`. |

Total 58 files.

## What is deliberately NOT here

`_to_delete/` still exists and stays gitignored. What remains in it is machine noise
with no evidentiary value: 23 stranded `HEAD.lock`/`index.lock` files, a `git-locks/`
and a `stale-git-locks/` folder, assorted `l.<timestamp>` fragments, `.DS_Store`, and
one redundant byte-identical copy of the set merged on 2026-09-01.

Those locks are not *entirely* without interest — they are the residue of running
`git status` and `git diff` across the desktop bridge, which takes `.git/index.lock`
and cannot release it, so the author's next `git add` fails with no visible cause.
That mechanism is already written down as a standing rule in `CLAUDE.md`
("Method rules that cost something to relearn"), which is the right home for it. The
lock files themselves add nothing the rule does not already say.
