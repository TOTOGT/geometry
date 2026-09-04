# HANDOFF — 2026-08-30, end of session

Read this first. Everything below the next `---` is the standing house notes.

## The overnight job, if you are the session that runs it

**Nothing needs installing.** Mathlib v4.32.0 is built at
`~/Desktop/geometry/.lake` (7.8 GB, 8,650 `.olean`, manifest `81a5d257c8e4`).
Do **not** run `lake exe cache get` — six sessions did that and left 30 GB of
duplicate builds; five were deleted today. See CHECK BEFORE YOU BUILD below.

    bash ~/Desktop/geometry/tools/leancheck.sh --audit FILE.lean [FILE.lean ...]

`lake env lean` from the geometry project compiles a file **anywhere on disk**,
so GTCT and 3M files check here without their own Mathlib. Budget ~3–30 s per
file now that imports are narrowed; it was 576 s each when files said
`import Mathlib`.

**The gate is `#print axioms`, not a clean compile.** `--audit` appends the
probe and reports any declaration trusting `sorryAx` or `native_decide`. A file
can build, contain no `sorry`, and still be worthless — see §6 of
`~/Desktop/dnls/CLAUDE.md`.

**Run order, highest value first.** The scan behind this is in
`/tmp/leanscan.json` if it survives; regenerate it by comparing each `.lean`
file's prose claim against its comment-stripped body.

1. **The 17 files with zero `import` lines.** They have never been compiled by
   anything. Give each the narrowest import set that resolves it, then audit.
   `AXLE/CatGT/axle_togt_canonical.lean` is one of these and was the worst
   finding of the day — three of its nine axioms are refutable, so the file is
   inconsistent. Fixed today; the other 16 are untouched.
2. **The 168 `sorry`s across 158 unique files.** Triage before proving: this
   session found three GTCT theorems and three AXLE axioms that were *false*,
   not merely unproved. Instantiate a claim at a two-element type with constant
   maps before spending an hour on its proof.
3. **`dm3CriticalityPrinciple_extended.lean`** carries the same false `V_c`
   double-root claim corrected in `GTCTsorryFree.lean`. Same repair applies.
4. **AXLE is stranded on toolchain v4.14.0** and **3M has no `lean-toolchain`
   at all**, so neither can be checked against the build we have. Repinning
   both to v4.32.0 is the unblock, and it is a deliberate decision — ask first.

## RH preprint — where reflection_law stands (30 Aug, end of day)

`GTCT/book4/ZetaReflection.lean` went from two `sorry`s to one. Proved and
kernel-audited today, none of them touching the zeros of ζ:
`chiLog_real_on_critical_line`, `Zlog_conj`, `gCoef_odd_in_t`, `cCoef_even_in_t`.

`reflection_law` needs exactly one input: `ζ'/ζ(s) + ζ'/ζ(1−s) = chiLog s`,
verified to 30 digits (mpmath) at three interior points. Its docstring carries
the route. Two traps recorded there, both found by checking advice rather than
taking it:
  · Go via `completedRiemannZeta_one_sub` (Λ(1−s) = Λ(s)), **not**
    `riemannZeta_one_sub` — the latter is the asymmetric form with cos(πs/2),
    and converting it to `chiLog` costs Legendre duplication and Euler
    reflection.
  · **Mathlib encodes Γ's poles as zeros** (`Gamma_eq_zero_iff`), so
    `Γ(s/2) ≠ 0` is not free and must be carried as a hypothesis.

`deposits/rh-arithmetic-contact-v1/RELATED-WORK.md` holds the verified
bibliography — three citations right, two corrected — plus the claims rejected
in audit. `GEMINI-PROMPT.md` beside it asks for checkable things instead of
proof plans; use it rather than asking how to close the gap.

## dnls has Lean CI already written — merge it before rebuilding one

Found 30 Aug. `TOTOGT/dnls` has **0 open PRs**; what looks like open work is 16
stale remote branches. Five are one stacked lineage whose tip,
**`fix-lean-proof-errors`**, was written 13 July and never merged. It carries:

- `.github/workflows/verify-proofs.yml` — *"Verify Lean proofs (real kernel
  check)"*: runs `lake build` as the gate and scans for `sorry` from
  actually-compiled source. This is the discipline this session rebuilt by hand.
- `Pin mathlib to v4.32.0 tag` + `Align lean-toolchain with pinned mathlib`.

Meanwhile **`dnls/main` carries `lean-toolchain v4.32.0-rc1` against
`mathlib @ "master"`** — a release candidate against a moving target, the same
defect class as GTCT's unsatisfiable pin. The branch fixes it and **merges into
main with zero conflicts**.

    https://github.com/TOTOGT/dnls/compare/main...fix-lean-proof-errors?expand=1

**Do not write new Lean CI for this corpus before reading that workflow.** Merge
it, then adapt it for geometry and GTCT rather than starting over.

After it lands, nine branches are already contained in main and can be deleted
by ancestry (never by name): TOTOGT-patch-1/4/5/6/7,
feature/archive-rehomed-book3-files, feature/curate-repo-structure,
feature/dnls-foundations-lean, house-rules. The four remaining stacked branches
become contained too.

## State at handoff

- **Pushed:** GTCT, AXLE, geometry, 3M. All clean.
- **`dnls` is pushed** (the blocking ruleset was removed 30 Aug). Its §6
  "what counts as formally verified" sits on branch
  `add-verification-and-coi-statement` at `c2a394a` and still needs a PR into
  `main`: https://github.com/TOTOGT/dnls/compare/main...add-verification-and-coi-statement
  The same six rules are duplicated in this file, so nothing is blocked on it.
  Note `dnls` carries 16 remote branches, several looking abandoned — branch
  hygiene there has drifted and is worth a pass.
- **Book 4 is clean.** 50 HTML files, all `<div>` balanced, 0 missing tracked
  files, 0 dead links or anchors (the repo's remaining 17 dead links and 4 dead
  anchors are all outside book4). A font checker flagged `MathFallback` in
  `ch11-catgt.html` and `gomc-opus.html`; that is a **false positive** — it is a
  deliberate `@font-face` with `local()` sources and a `unicode-range` for Greek
  and math glyphs, working as designed. Do not "fix" it.
- One WIP commit preserves a previous session's book4 pricing edit (PayPal
  links removed). Unreviewed — confirm it was intended.
- Disk: 49 GB free, up from 26 GB. `tools/disk-survey.sh` finds the rest.

## Not started, deliberately

ISO 13485 / orthobiologics. G6 LLC is moving into life sciences with a medical
device. Pablo asked to defer the QMS write-up until the corpus is ready. When
it starts, the first question is regulatory classification — device vs
21 CFR 1271 §361 HCT/P vs §351 biologic — because ISO 13485 is the right
standard only for the first. Do not let dm³ become a design input or a
marketing claim without evidence behind it.

---

# CLAUDE.md — totogt.github.io/geometry repo

**Read the Read-first section below and stop.** Open a later section only when
you are about to touch the file it covers. Dated narrative for closed defects
and audits lives in `docs/audit-log.md`, not here.

This file primes Claude for the `~/geometry` working repo, which is the live HTML site
for the Principia Orthogona series at totogt.github.io/geometry.

Read `~/Desktop/dnls/CLAUDE.md` for the canonical house rules (filesystem map, repo table,
style guide, licensing, what agents must NOT do). This file adds geometry-specific notes.

---

## Attribution — it goes in the handoff, not in commit messages

**Set 2026-09-04 by Pablo. Applies to every session.**

Do **not** put `Co-Authored-By:`, `Claude-Session:`, `🤖 Generated with…` or any
equivalent trailer in a commit message. The books are the user's work. A tool
that helped does not get a byline on 717 commits.

Attribution belongs in **one place**: the handoff block, in the form already used
below —

    **From:** session `<session id>` · account `<account email>` · model `<model>`

The account email is the load-bearing field. Sessions run under different
accounts (`brodananda@gmail.com`, `sluhcdf@gmail.com`, others), and months later
the only way to find which conversation produced a given artifact is to know
which account held it. A commit trailer cannot answer that question; the handoff
block can.

**If a session is running out of context ("no gas"), write the handoff before
anything else.** A session that spends its last tokens on one more edit instead
of the handoff costs the next session more than the edit was worth.

**Existing trailers.** 31 commits carry `Co-Authored-By: Claude Opus 5` and 27
carry `Claude-Session:`, all from before this rule. They are left in place:
removing them rewrites every downstream SHA and breaks the commit links recorded
in `docs/audit-log.md`. The rule is forward-looking. Do not add more.

## HANDOFF — 2026-09-04 (OVERWRITE this block. Do not append. It reached 341 lines once by appending; dated narrative belongs in `docs/audit-log.md`.)

**From:** session `01DfPorRiUiwcVdUj5rYnWRj` · account `sluhcdf@gmail.com` · model `claude-opus-5`
**Ended:** 2026-09-04, ~90% of session budget, on the user's signal.
**Repos touched:** `~/Desktop/geometry` only. AXLE and vol1-proofs were read, never written.

### Shipped and pushed
`4a12732` WP-94 created · `93733d2` §8 AxiomProver · `10bbd7d` WP-95 + indexes ·
`2136d51` §10 Isabelle probe · `3dda315` licence conflicts · `d86dc76` attribution rule ·
`320d5fc` Book 4 ORCID.

### The WP-94 arc — read §9 and §10 before adding to it
The note now runs §1–§11 and **twice corrects itself**, which is the point of it.
§9 retracts the §5 claim that no shared unit exists for what sits outside a formal
artifact: `#print axioms` is that unit and always was. §10 widens it — Isabelle
ships `thm_oracles`, thirty years older, equally unquoted. So the finding is a
**norm that failed to form twice, independently**, not a missing standard.

`book6/wp94-coining-note.md` proposes `vouch`. **Three findings have now narrowed
it** and the next session should not quietly re-widen it: Anthropic's FLT axiom
disclosure, the two-system tooling, and Isabelle's incumbent noun `oracle`, which
is machine-checkable and in use. The honest position is that disclosure is the
recommendation and coinage is the weaker claim.

`tools/lexeme_census.py` is the instrument. Rerun it rather than quoting numbers:
one figure in this session moved 780 → 271 purely by stripping comments.

### Open, in priority order

**0. SEND THE AI FOR MATH FUND SEED APPLICATION. This is the priority, said so by
the user on the way out: "need that out the door, we need to work."**
Draft is `~/Documents/Claude/Projects/ai-for-math-seed-application.md`, 962 words,
$95,000 / 12 months, tools-and-infrastructure track. Seed grants are **rolling** —
no deadline to wait for, and the 2026 main round has already closed (abstracts were
due 30 March, decided August), so seed is the only live door and it is open today.
Apply through the fund page, **not** `renaissancephilanthropy.org/partner-with-us`,
which is for co-funders and institutions, not applicants. Contact for questions is
on the fund page.
Two things to clear first, both small and both blocking on their own terms:
`vol1-proofs` needs a LICENSE file (MIT, matching the SPDX headers already in its
sources), and the fund requires **all outputs open-access**, which the NC-ND prose
licence contradicts. Do not send it with the repository legally all-rights-reserved.

1. **SciENcv is mandatory from 1 Sept 2026** for the ROSES A.13 proposal (due
   **15 Oct**). No profile exists. Cannot be done the night before.
2. **Is the A.13 PI an NSPIRES AOR for G6 LLC?** If not, nobody can press submit.
   Five-minute check, and the classic 11:50 pm failure.
3. **A.13 duration and award ceiling still unverified.** Needs-and-Opportunities →
   Market Discovery → 1 year is an *inference* from the amendment's ordering, never
   read stated. The budget is built for 3 years and $432,000. If the inference is
   wrong, Years 2–3 ($298,000) come off.
4. `vol1-proofs` **has no LICENSE file** while its Lean sources carry SPDX MIT.
   It is the repository the AI for Math seed application leads with.
5. CC BY-NC-ND vs the AI for Math Fund's open-access requirement — unresolved.
6. Two handoff blocks exist: this one, and a stale 2026-08-30 block at **line 1**,
   above the file's own title. That is the append violation this header warns about,
   already recurred once. Not deleted here — another session's notes.

### Deliverables that live OUTSIDE this repo
`~/Documents/Claude/Projects/` holds the A.13 pack (PSD answers, Q26, Q29, DAPR
checklist, attachment plan, budget review, budget narrative, S/T/M draft, OSDMP +
references), the submission tracker, the Carina Hong note, and the AI for Math seed
application. `~/Downloads/G6LLC_NASA_Proposal_Enceladus_2026_ORCIDfix.docx` is the
Enceladus proposal with ORCID and email corrected.

**Lost with the session:** the IJL work built in the cloud container and never
committed — a full reference audit finding **Petersen & Potts wrong three ways**
(Erika not W., *Findings of EACL 2023* not SCiL, 490–511 not 212–222), Bond &
Rudnicka's page range, and a rewritten §8.4 against C/K/F/U. **Redo it before the
IJL manuscript goes anywhere.**

### Scheduled
A weekly task fires **Sundays 09:00 ET** testing David Grossi's writing-coach
prompts and appending to `book6/wp94-coach-compliance.md`. It commits nothing.

### Method notes worth keeping
- **Every negative claim got a search behind it, and three were wrong.** A frontier
  paper's parameter table was found inconsistent (A₁ and δ disagree between §9.2 and
  §9.3; the errors cancel, so the printed total is right). Two "suspicious"
  citations were verified genuine. One self-check counted comments as code.
- **`device_bash` cannot unlink `.git/*.lock`.** Every git call through the bridge
  strands a lock and blocks the user's own git. Inspect read-only; hand writes over.

## CANONICAL: all HTML lives in geometry (set 2026-08-30 by Pablo)

**`~/Desktop/geometry` is the canonical home for every HTML page in the corpus.**
No exceptions. New pages are created here. Other repos hold Lean, tooling, data,
notebooks and PDFs — not chapter HTML.

**Why this rule exists.** Sessions run under different accounts and do not share
memory. This file is the only channel between them, so a convention that is not
written here does not survive the session that invented it. Book 4 is the proof:
it exists in `geometry/book4/` (50 HTML files) and in `GTCT/book4/` (36), and as
measured 2026-08-30 **every single shared chapter differs** — with drift running
in *both* directions, so neither copy is simply newer:

```
ch07.html   geometry 35,207 B   GTCT 88,789 B     ← GTCT ahead
ch08.html   geometry 34,182 B   GTCT 75,060 B     ← GTCT ahead
ch02.html   geometry 47,867 B   GTCT 25,212 B     ← geometry ahead
ch12.html   geometry 35,138 B   GTCT 30,473 B     ← geometry ahead
```

Fourteen chapters exist only in geometry (`ch15-complex-turn`, `ch16`–`ch20`
lattices, `ch-hawking`, `ch06b`, `ch-build-2river`, `ch6-resonance`, …).

**How to consolidate — this is a reconciliation, not a copy.** A blind
`cp` in either direction is silent data loss. Per file: diff the two, merge the
later work in both directions, land the result in `geometry/`, and then replace
the non-canonical copy with a one-line pointer to the geometry URL — never leave
a second copy behind. Do this chapter by chapter, and record in
`docs/audit-log.md` which files were reconciled and which direction each carried.

**Until a page is reconciled, do not edit it in either repo.** Editing the
non-canonical copy widens the gap; editing only the canonical one loses whatever
the other side has. That is why the §12.2 correction is still unwritten.

**Corollary for Lean.** Lean files are the exception that proves the rule: they
belong with the project whose toolchain builds them. Book 4's Lean is GTCT's
(`GTCT/book4/`, and `GTCT/GTCT/GCTC/` once that package moves off mathlib
v4.11.0). HTML never follows the Lean; the Lean never follows the HTML.

## Read first: Lean and CI verification state

Updated **2026-08-25**. This section is the current answer. Do not re-derive it
from the tree; update it when a run changes it. Every number below was measured
on the date shown, not inherited from a header comment.

**What the green badge now covers.** `.github/workflows/verify-proofs.yml`
builds and then gates. `lakefile.lean` declares two default targets,
`lean_lib Orthogenesis` and `lean_lib SaturnHexagon`. The job runs
`tools/axiom_gate.py` three times — on 5 SaturnHexagon theorems, 12 NASAGaps,
14 G6Crystal — so **31 theorems in this repo are kernel-checked**, each
reporting `[propext, Classical.choice, Quot.sound]` and no `sorryAx`. Those
three gate steps are the only steps permitted to decide the job.

**What it still does not cover.** Green does not mean every `.lean` in the tree
compiled — root-level `NASAGaps.lean`, `Coverage.lean`, `CollatzDescent.lean`,
`FoldCentralCharge.lean`, `SmokeBox.lean` and `AMonster/*.lean` are in no
target and the job never touches them. Green does not mean the tree is
sorry-free. And green does not mean any theorem **asserts** anything — see the
vacuity gap below, which is the largest open hole in this repo's verification.

**The `sorry` inventory, measured 2026-08-25** (comments and docstrings
stripped; grep alone over-counts badly, because these files discuss `sorry` at
length in their headers):

| Where | Count | In a build target? |
|---|---|---|
| `Orthogenesis/Architecture/MagneticLattice.lean:240` | 1 | **yes** — M2 incommensurate aperiodicity, disclosed in-file |
| `Orthogenesis/Architecture/SeismicLattice.lean:211` | 1 | **yes** — Q2 response-spectrum detuning, disclosed in-file |
| `CollatzDescent.lean` | 2 | no target |
| `Coverage.lean` (ROOT copy) | 1 | no target |
| `AMonster/GenerativeWeave.lean` | 1 | no target |

Six total, two of them visible to the build. No document should say the package
is sorry-free.

`Orthogenesis/Architecture/Coverage.lean` is **clean and building** as of this
date, and `Orthogenesis.lean` imports it. The 2026-08-21 note recording
`hexRing_card` as admitted and `coord_coverage` as unproved described the root
copy and is superseded; the surviving `sorry` at `Coverage.lean:92` is in the
untargeted root file.

**How to count `sorry` correctly.** Lean writes ``declaration uses `sorry` ``
with **backticks**. A grep written `declaration uses 'sorry'` with straight
quotes matches nothing and prints `0`, which reads as clean. That false
negative was produced on 2026-08-25 and believed until the build log two lines
above it was read. Use `grep -c 'declaration uses'` with no quoting around
sorry, and cross-check against a comment-stripped source scan.

### The vacuity gap — the one instrument this repo does not have

`#print axioms` certifies that a proof establishes its stated proposition. It
has nothing to say about whether the proposition asserts anything. This corpus
has shipped four vacuous or near-vacuous claims that a kernel check passed:

- `g6_equals_schumann : g6_layer_count_nat = schumann_4th_harmonic_integer := rfl`
  — both sides are `def … := 33`. It is `33 = 33` and cannot fail. Withdrawn in
  Vol I V7. A kernel cannot check a claim about the ionosphere.
- `basin_asymmetry` was cited as machine-checking the Factor-of-3 gravitational
  decoherence prediction. It is `1/3 < 4/5`, an inequality between rationals.
- `NASAGaps.lean` carried `: True := trivial` and `∀ x ∈ S, x ∈ S := id`.
  Deleted 2026-08. The second shape is the one a `: True` sweep misses.
- `UnfoldOp.stable_branch` is satisfied by `n = 0` for every map on every type,
  so "Theorem D (stability)" has no content beyond Φ-decrease.

**A working detector exists and is not in this repo.** `vacuity.lean` in the
Vol I bundle defines `#vacuity_scan` (flags trivially inhabited conclusions:
`True`, `∃ _, True`, and conjunctions of those, after `whnf` — so it sees
through definitions, which a grep for the token `True` cannot) and
`#unused_param_scan` (Prop-definitions that never mention an explicit
argument — true of every subject). It ships with `vacuity_fixtures.lean`,
five deliberate vacuous specimens and one honest control, so the instrument is
checked before its verdict counts. It runs in `vol1-proofs` and returned
`flagged=0` over 82 theorems.

The scan is prefix-driven, so porting it here is a probe file plus one CI step:
`#vacuity_scan "Orthogenesis."`. Until that runs, **this repo's 31 theorems are
kernel-checked and unverified for content**, and `nasa_gap_closure_summary` —
a summary theorem in the file that carried the two tautologies — is where to
point it first.

### Cross-repo verification tally, 2026-08-25

| Repo | Kernel-checked under a green gate | Vacuity-scanned |
|---|---|---|
| `vol1-proofs` | **82** (PrincipiaVol1 58 + AutophagyDm3 24) | **yes — 0 flagged** |
| `geometry` (this repo) | **31** (SaturnHexagon 5 + NASAGaps 12 + G6Crystal 14) | no |
| `io` | **16** (Theorem53 + CatGT) | no |
| **Total** | **129** | **82** |

The defensible public claim is **82 real, 129 kernel-checked**. Saying 129 real
would be the same overclaim the corpus has already corrected four times.

`io` runs "Verify proofs" on every push to `main` — 57 green runs as of this
date — and is where Theorem 5.3 is kernel-checked in a small repo. `vol1-proofs`
gained a real gate on 2026-08-24; before that its only workflow was
`pages-build-deployment`, which compiles no Lean, so the Vol I deposit's
published reproduction recipe (`git clone`, `bash tools/run.sh`) produced
`no configuration file with a supported extension` for as long as V7 had been
public.

**Traps.**

- Several files exist both at the repo root and under
  `Orthogenesis/Architecture/` (`NASAGaps.lean`, `Coverage.lean`). Only the
  latter are built. Edits to a root copy never reach CI, and the two copies
  have already diverged — the root `Coverage.lean` still carries a `sorry` the
  built copy does not.
- A `.lean` file that is not a build target is checked by nothing, however
  green the badge. `SaturnHexagon.lean` sat outside every target for a month
  while its own header asserted it had been kernel-verified and three of its
  five theorems were admitted. Declaring it a target is what made a regression
  fail the job rather than pass unnoticed.
- Header comments are not evidence. Seven pages still cite Mathlib
  **v4.33.0-rc1** (`wp35`, `wp66`, `wp73` ×3, `research-status.html`) while
  `lean-toolchain` pins **v4.32.0**. Quote the run, not the header.
- `~/Desktop/orthogenesis` has `.lake/packages/mathlib` fetched and
  `~/Desktop/geometry` does not. Builds must run in a tree that has mathlib, or
  in CI.
- **Do not run `git` through the Cowork device bridge.** It cannot delete
  files, so `git status` leaves a `.git/index.lock` that the bridge cannot
  remove and that blocks every later git command in that clone. This happened
  in `geometry` (three times) and in `io-clone` (once).
- **Read `git log --oneline -1` before generating any file for a repo, not
  after.** On 2026-08-25 a correction was built against a `vol1-proofs` HEAD
  that was one commit stale and would have left `AutophagyDm3_v2.lean` in the
  tree with no target building it — the `SaturnHexagon` failure, regenerated.
  It was caught only because an unrelated `git rm` failed.

### Audit tooling — what each tool can and cannot see

`tools/audit.py` checks **structure** (tags balance, files close, internal
links and anchors resolve). `tools/claims.py` checks **assertion** (a DOI
quoted beside a title resolves to that title; withdrawn claims are gone; status
claims have not decayed). The split is deliberate and documented in each file.

Changes landed 2026-08-25:

- `audit.py` **rule 6**, WP numbering: `wp_number_collision` (scoped
  per-directory — cross-directory pairs like the `wp56` book6/book7 case are
  legitimate), `wp_self_mismatch` (filename number against footer self-claim),
  and `wp_above_max` (informational; `book7/ch-hamilton.html`'s two references
  to WP81 are a deliberate forward reference to Vol VIII, not a defect).
- `claims.py` **`DOI-MALFORMED`**: any `href` on `doi.org` whose path is not
  `10.\d{4,9}/\S+`. Origin: the 2026-08-18 "series DOI" sweep replaced the link
  **text** and left the **target**, producing
  `href="https://doi.org/Zenodo community"` in `wp35`, `wp36` and `wp37` — live
  for six days and shipped inside a Zenodo deposit. Invisible to both auditors:
  `audit.py` skips external URLs by design, and `claims.py`'s DOI rules work by
  resolving an identifier, so the one input they cannot handle is an identifier
  too broken to be one. A validator that dereferences needs a well-formedness
  gate in front of it.
- `claims.py` **negative-cache fix**: `.doi-cache.json` persisted failures, so
  a record queried before publication was cached as a permanent 404 and the
  live record was reported dead forever. Failures are no longer written and a
  cached error no longer short-circuits a fresh lookup. Two poisoned entries
  purged. A failed lookup is a fact about one moment on one network; only a
  success is a fact about the world.
- `claims.py` cannot reach the Zenodo API from the Cowork device bridge (egress
  403). Run it `--offline` there.

Open audit findings: one genuine `wp_number_collision` (`wp30-how-to-audit` and
`wp30-the-missing-anchor`, same directory), one `dead_anchor`
(`book4/ladder-polynomials.html:442` → `ch11.html#correction-m1`, which does not
exist), and one `dead_link` inside `.lake/packages/` that is vendored and should
probably be excluded by adding `.lake` to `SKIP_DIRS`.

**The general rule this section exists to enforce.** An audit's coverage is not
the set of things it checks. It is that set, less the seams between its tools,
less everything outside the tree they read. Both subtractions are invisible from
inside: a clean run reports what the tools examined and says nothing about what
no tool was positioned to examine. `book6/wp78-the-seam-and-the-boundary.html`
is the write-up.

**Working economy.** This file is long. Read this section, then only the
section covering the file you are about to touch. Do not page a whole Actions
log — read the failing step. Prefer targeted reads to whole-file reads.

---

## Series ISBN & format map

**Canonical source: `~/Desktop/MATHS for life/isbn_metadata.json`.** It is the only copy
that carries `bowker_status`, so it is the only copy that can tell you whether a number is
*registered* or merely *reserved*. Do not restate the numbers anywhere else. The table that
used to sit here drifted out of sync with the registry and put an **unallocated reserve
number** into 87 book6 footers and 19 other files as though it were a real one. Read the JSON.

| ISBN | Allocated to | Bowker status |
|------|--------------|---------------|
| 979-8-9954416-0-1 | Complete Completeness · G5 · Paperback | **REGISTERED** |
| 979-8-9954416-6-3 | Book 3 · Mini-Beast · eBook PDF | INCOMPLETE — **register now**, only actively distributed product |
| 979-8-9954416-1-8 | Complete Completeness · G5 · eBook | INCOMPLETE — HOLD |
| 979-8-9954416-4-9 | Complete Completeness · G5 · Hardback (≤666pp) | INCOMPLETE — HOLD |
| 2-5 · 3-2 · **5-6** · 7-0 · **8-7** · 9-4 | **unallocated reserve — no group, no format** | INCOMPLETE — HOLD |

**Critical rules:**
- Book 3 (Vol III, The Mini-Beast) is **eBook only**. Never add a print ISBN to it.
  Never list it as available in print. It is a living document, updated as the pilot expands.
- **A volume without its own registered ISBN gets no ISBN line at all.** There is no such
  thing as a "fallback ISBN" — that instruction was wrong and is withdrawn. Point at the
  Zenodo community instead. Vols II, IV, VI and VII have no allocation of their own; do not
  borrow one from a volume that does.
- **Print ISBNs are reserved, not active.** The registry's own note: *"Print ISBNs reserved —
  paper books not for sale until further notice."* A print ISBN in a web footer advertises a
  product that does not exist. Do not add one.
- **10.5281/zenodo.19117399 is Vol I's *concept* DOI — it is NOT a series DOI.**
  Corrected 2026-08-01, checked against the Zenodo API. A concept DOI resolves to
  whichever version was deposited most recently: today it lands on Vol I v6,
  10.5281/zenodo.21146416 (2026-07-02). Citing it for anything other than Vol I
  sends the reader to the wrong document; citing it *for* Vol I pins nothing,
  because the target moves on every deposit.
  This line previously read "Series root DOI — use this for cross-volume
  citations." That instruction is what put a phantom citation into the JOMO
  game-theory pack and kept it there from June to August. Do not restore it.
- **Cross-volume / series-wide pointer:** the Zenodo community
  <https://zenodo.org/communities/principia-orthogona> — "Principia Orthogona —
  Generative Contact Mechanics", public, 6 records. **There is no series-level
  DOI.** If you need one thing to point at for the series as a whole, point at
  the community, or at the Opus Map (`book4/living-book.html`).
- **Vol I DOIs:** concept 10.5281/zenodo.19117399 · v1 (first deposit)
  10.5281/zenodo.19117400, 2026-03-17 · current v6 10.5281/zenodo.21146416,
  2026-07-02.
- **10.5281/zenodo.19117400 is real, valid, and checked against the Zenodo API
  (2026-08-02).** It is Vol I's v1 deposit and it is genuinely the origin
  point of the project: it bundles the first four Principia Orthogona / GCM
  papers (Vol I "Mathematics of Generative Transitions," Vol II "Contact
  Realization," "Generative Contact Mechanics," and "The dm3 Operator" toy
  model). If a page ever wants to point students at *where the series
  started*, this is the correct DOI for that purpose — cite it explicitly as
  the origin/founding deposit. What it is **not** is Book 3's DOI: it has
  nothing about the Mini-Beast, the D1–D4 domains, or the pilot. Book 3 has no
  standalone deposit yet (see `minibeast-pilot.html` fix, 2026-08-02, below).
  **The four founding papers do now also have their own later deposits — but
  none of the four is a clean substitute for "the origin," each for a
  different reason, checked against the Zenodo API 2026-08-02:**
  - Vol I: concept 10.5281/zenodo.19117399 → currently v6
    10.5281/zenodo.21146416 (July 2026). Heavily revised since v1 — new
    theorems, closed proofs, changed assumptions. Citing this today gets the
    *current* Vol I text, not the original.
  - Vol II ("Contact Realization"): 10.5281/zenodo.19379473. Clean, single
    version, April 2026 — the one paper of the four with an unambiguous
    standalone DOI.
  - "Generative Contact Mechanics": concept 10.5281/zenodo.19122167 →
    currently v2 10.5281/zenodo.20230610. v2's file list oddly re-bundles
    *all four* original PDFs again (same md5s as the v1 bundle) — looks like
    an accidental re-upload on the author's end, not a clean single-paper
    citation. Needs a Zenodo-side cleanup by the author before it's citable
    as "just this paper"; not something to fix from this repo.
  - "The dm3 Operator" toy model: 10.5281/zenodo.19379385. Clean, single
    version, April 2026.

  **Rule:** for "where the series started," cite 19117400 alone — it is the
  only one of these that is actually frozen at the origin state. Do not
  substitute the four individual DOIs above for that purpose; two of them no
  longer represent what was originally there.
- **Positional Dominance / network games has its own concept DOI** —
  10.5281/zenodo.21013065 → v1 10.5281/zenodo.21013066 (June 2026),
  v2 10.5281/zenodo.21753025 (August 2026). **Cite v2.** v1's analytical
  threshold is superseded; see `book6/wp38-positional-dominance.html`.
- **Rule:** cite a *version* DOI whenever the claim depends on what the text
  actually says. Cite a *concept* DOI only when you explicitly mean "whatever is
  current", and say so in the citation. Never label a concept DOI as the series.

### Blast radius of the phantom series DOI — FOOTERS CLOSED 2026-08-12, BODIES OPEN

**The 127 figure was wrong, and wrong in the direction that matters.** It came
from grepping one pattern (`10.5281/zenodo.19117399`). Measured properly on
2026-08-12 — both Vol I numbers, all three URL spellings — the real count is:

| Measure | Files |
|---|---|
| Carry a Vol I DOI (`19117399` **or** `19117400`) | **225** |
| …with it inside a `<footer>` | **189** — *repaired 2026-08-12* |
| …with it only in the page body | 36 — **still open** |
| …in both footer and body | 57 (bodies still open) |
| Labelled "Series DOI" / "Zenodo series" (Tier A) | 6 in footers |

**Three spellings, not one.** The undercount happened because the DOI appears as
`10.5281/zenodo.19117399`, as `zenodo.org/records/19117400`, and as a bare
`19117399` inside an anchor. Any future sweep must match all three, plus the
`zenodo.org/doi/…` path form — see the failure note below.

**Footers are done.** In a footer the number reads as *that page's own* DOI,
which is wrong by construction regardless of the page's subject, so the repair
is mechanical and was automated: 189 files, 181 anchors + 6 Tier-A labels + 6
bare mentions, all → the community URL. Verified: 0 Vol I DOIs remain in any
footer; every file diffed against HEAD for new defects.

**Bodies are NOT done — 93 files.** An in-body mention may legitimately discuss
Vol I. Those need the file opened and judged per the Tier rules below. Do not
automate that pass.

**Failure worth remembering:** the first sweep pattern missed
`https://zenodo.org/doi/10.5281/zenodo.19117399`, so the bare-mention rule fired
*inside the href attribute* and nested an `<a>` tag within a URL in
`dm3-course-landing.html` and `dm3-courses-101-102-103.html`. Caught by the
markup check, repaired the same pass. When rewriting URLs by regex, always match
the anchor first and never let a fallback rule run inside an attribute.

**It also escaped the repository.** Zenodo record `10.5281/zenodo.21431505`
carries `DOI (series): 10.5281/zenodo.19117399` in its Description *and* an
`Is part of` relation pointing at it — and OpenAIRE has indexed that relation.
Correction drafted at `book6/ZENODO-metadata-corrections.md`; **not
deposited**, per rule 4.

Repair, when it is done, is per-file and minimal:

- Tier A → the community URL `https://zenodo.org/communities/principia-orthogona`,
  or drop the line. Never "Series DOI".
- Tier B → the DOI of the work the page is actually about; if the page has no
  deposit, the community URL.
- Tier C → keep, but add "(concept DOI — resolves to the current version of
  Vol I)", or pin to a version DOI if the surrounding claim depends on the text.

**Settled so far:** `AXLE → GameTheory_Full_Pack.html` and
`AXLE → NetworkGamesJOMO/GameTheory_Full_Pack.html` (hero + footer + both
reference notices, 2026-08-01) · `geometry → GameTheory_Full_Pack.html`
(2026-08-02) · `book6/wp38-positional-dominance.html` footer (2026-08-01) ·
this file. All three copies of the pack now agree. Everything else is untouched.
`minibeast-pilot.html` footer (2026-08-02, not a tiered case above but same
mechanism: it cited `10.5281/zenodo.19117400`, checked against the Zenodo API
and confirmed to be Vol I's v1 deposit, not Book 3's — swapped for the
community URL since Book 3 has no deposit of its own. See the DOI note above.

### SECOND FAILURE MODE — mis-correction into a phantom *absence* (found 2026-08-02)

The grep for `19117399` does **not** find every affected file, because a file can
be "corrected" out of the phantom DOI and into a worse claim. The root copy of
the pack had already been edited by someone, and both reference entries read:

> *No standalone Zenodo record found under this title.*

**False.** The record exists — v1 `10.5281/zenodo.21013066`, v2
`10.5281/zenodo.21753025`, concept `10.5281/zenodo.21013065`. Checked against
the Zenodo API. Entry (2026b) went further: "not yet deposited, or not yet
written." It is neither; it is the ADDENDUM inside the parent record and carries
the parent's DOI.

The mechanism: searching on `19117399` lands on Vol. I, so the checker concluded
*the paper was never deposited* rather than *this DOI belongs to another work*.
**A phantom citation produced a phantom absence.** The correction inverted the
error instead of resolving it, and removed the searchable string on its way out.

Consequences for the rescan:

- Add to the sweep: `No standalone Zenodo record`, `no Zenodo record found`,
  `not yet deposited`, `not yet written`, `phantom-DOI`, `treat .* as unsourced`.
- A file with **zero** occurrences of `19117399` is not thereby clean.
- Before writing "no record exists" anywhere, query the Zenodo API for the
  *title*, not the DOI. Absence of a deposit is a positive claim and needs the
  same evidence as a citation.
- That edit was **uncommitted** in the working tree, so `git grep` on HEAD would
  not have found it either. Sweep the working tree, not just the committed tree.

Two files assert absence or unsourcedness elsewhere and have **not** been read:
`book6/wp30-how-to-audit.html`, `research-status.html`. `[OPEN]`

### WP-38 — open items carried forward (2026-08-02)

1. **Two broken formulas** remain in Figures 1–3 (`data-mjx-error="Misplaced &"`
   — matplotlib mathtext choking on a literal `&`). No generator exists for those
   three; Figure 4's is now committed as `book6/wp38-fig4.py` and is the pattern
   to follow. Verify any figure edit by rasterising the SVG **as embedded in the
   page**, not the standalone file — the 2026-08-02 breakage was in the embed
   (unnamespaced `clip-path="url(#…)"`), and the standalone file was fine.
2. **Otium is in two places at once** — §9 of WP-38 *and* a separate file in the
   unpublished deposit. Resolve before publishing `10.5281/zenodo.21752834`.
3. **c_K discrepancy `[OPEN]`** — inverting σ* = 0.33 through the corrected
   structural model gives c_K = 0.669, hence b = 44.6, against v2's b = 1.208.
   A factor of ~37. This is v2 §3.3's own identification test run from the
   structural side, and it does not come out clean. Do not describe either
   record as calibrated until it is resolved.

   **Diagnostic computed 2026-08-07** (Python, scipy.stats.norm, reproducible).
   Calibration used: δ = 0.985, γ = 0.55, κ = √(2/π), A_V = β(1−γ)κ = 3.051,
   σ̄ = 0.33, K determined by Kβσ̄·g(0.72) = 1.1577 (from the page's own text).
   All three expressions for the structural parameters agree:

   | Quantity | From crossing | From Π_J″ | V2 deposit | Factor |
   |----------|--------------|-----------|-----------|--------|
   | c_K      | 0.6577       | 0.6689    | 0.01812   | ×36    |
   | b = c_K/(1−δ) | 43.85   | 44.59     | 1.208     | ×36    |
   | a = b/σ*²    | 402.6    | 409.5     | 11.09     | ×37    |

   The structural inversion is self-consistent: √(b/a) = 0.327 ≈ 0.33 ✓.
   The discrepancy is not a rounding artifact — it is structural.

   **What v2's b = 1.208 implies for the model.**  With c_K_v2 = 0.01812:
   ΔΠ(σ̄) = Kβσ̄·g(0.72) − c_K_v2 − Π_V(σ̄) = 1.1577 − 0.0181 − 0.5 = +0.640 > 0.
   J already dominates V at the saturation point. There is no crossing at or above
   σ̄. Condition C' (which requires c_K ≥ 0.6577 for the root to lie in [σ̄, ∞))
   is violated. The threshold σ* = 0.33 must therefore fall *below* σ̄, in the
   regime where Π_V is quadratic (not affine) and uniqueness is [OPEN] (the paper
   states this explicitly in Proposition 1′). This is not internally inconsistent
   — it just means the paper's own uniqueness proof does not cover the calibrated
   case, and the quantitative results (σ* = 1/3 and related claims) rest on
   numerical simulations, not the proved theorem.

   **Resolution path.**  Two tasks remain before calling either record calibrated:
   (a) Obtain an independent empirical estimate of c_K (annual carry cost as a
   fraction of asset value) for the five events studied. If c_K ≈ 0.02 (≈ 2%/yr,
   consistent with pipeline O&amp;M or storage insurance at market rates), the
   structural model needs its below-saturation Π_V formula to produce a unique
   threshold, and the uniqueness proof gap must be closed. If c_K ≈ 0.66 (≈ 66%
   of a period's asset value), the structural model already has σ* at σ̄ and no
   gap. The factor of 37 in the parameter implies the two interpretations are not
   close; one must be wrong.
   (b) Identify where v2's quadratic coefficient a ≈ 11 came from. Structural
   gives a ≈ 409; if v2 evaluated Π_J″ at the wrong σ (e.g. σ ≈ 1.5 where
   Π_J″ ≈ 0.167 and a ≈ 11), that would explain the discrepancy. Check the v2
   Zenodo deposit (10.5281/zenodo.21013066) §3.3 for the explicit computation.

**Upstream:** `~/Desktop/dnls/CLAUDE.md` is named here as the canonical house
rules and was not reachable in the session that opened this entry. If it carries
the same "Series root DOI" line, it is the real source and must be corrected
there too, or this defect returns.

### KNOWN DEFECT: Neimark–Sacker row overclaims "proved" — REPAIRED 2026-08-07

**The false claim:** `vol2-toymodel.html` Theorem C and `vol2-contact.html` Proposition 5.1
assert that the dm³ toy model undergoes a Neimark–Sacker (A₂) bifurcation at detuning
|Δ| = Δ*, and label this "proved ✓ · full Lean 4 verification."

**Why it is false:** The dm³ ODE (r, θ, z) linearised around the attractor Γ = {r=1}
gives a triangular 2×2 Jacobian J(z) = [[-2(1−e^{−z}), 0], [2, 0]] with eigenvalues
λ₁ = −2(1−e^{−z}) and λ₂ = 0 — both real at every z. Verified by direct computation
(Python, 2026-08-07). A Neimark–Sacker bifurcation requires a complex-conjugate
eigenvalue pair crossing the unit circle (discrete) or imaginary axis (continuous);
that structure is absent from the 3-equation system. No Lean file for this claim exists.

**Salvageable part:** The table note "Rank-1, 2nd angular direction" and the detuning
parameter Δ = ω₂ − 1 correctly point at the DNLS extension. The NS mechanism is the
modulational instability (MI) of the DNLS plane-wave solution, onset at
λ_c = −2J/|A|², with BdG spectrum ω²(q) = ε(q)·[ε(q) + 2λ|A|²], ε(q) = 2J(1−cos q).
The Jordan wall ω²=0 at ε(q*) = −2λ|A|² is the Krein-signature flip. This is
mathematically correct but requires DNLS, not the bare dm³ ODE.

**Repair (done 2026-08-07):**
- `vol2-toymodel.html`: NS table row tagged [MODEL]; closing paragraph corrected —
  "full Lean 4 verification" removed, [OPEN] added for the NS row specifically.
- `vol2-contact.html` (root + `book2/` copy): "proved ✓" badge qualified with
  "[MODEL] pending DNLS extension"; Proposition 5.1 box reworded; correction notice added.
- This CLAUDE.md entry.

**Status:** `[OPEN]` — the NS/A₂ correspondence remains unproved for the bare dm³ system.
The correct proof target is the DNLS MI threshold; no Lean file yet exists for it.

### KNOWN DEFECT: the root-language conflation — REPAIRED 2026-08-12 (WP-61)

**A second costume for the WP-24 defect.** WP-24 refuted `q³ − 3q = (q−1)²(q+2)`
(false by a constant, +2). It fixed the file it was pointed at. It did not ask
whether the *habit* — using "double root", "degenerate" and "critical point"
interchangeably — had spread. It had.

**The false claims, and the true forms.** All checked with SymPy, symbolic:

| Claim as written | Status | True form |
|---|---|---|
| `V(q) = q³ − 3q` has a **double root at q = 1** | **FALSE** — V₃(1) = −2; roots are 0, ±√3 | `c = 3` is the unique coefficient with a **critical point** at q = 1. The double root belongs to `V − V(1) = V + 2 = (q−1)²(q+2)` |
| `V_φ = q³ − φq` has a **degenerate double root** at `q* = √(φ/3)` | **FALSE twice** — q* is not a root (V_φ(q*) = −0.792) and is non-degenerate (V″ = 4.41) | q* is a **non-degenerate critical point**, and q* ≠ 1, so φ is subcritical |
| η is the only n-bonacci constant giving that root | **FALSE** — no ρ_n equals 3; they increase to τ = 2 | the correspondence is **rank n = 3 ↔ coefficient c = 3**, integer to integer. `[OPEN]` whether that is more than small-integer coincidence |
| `μ_max = −½ V″(1)·ε₀²`, and Vieta "product of roots = −2" | **FALSE** — the formula gives −1/3; the Vieta line is numerology | the correct linearisation `d/dr[r(1−r²)]\|₁ = −2` was already one line above. Both removed |

**Key point, worth internalising:** a double root of `V − V(1)` at a critical
point is *automatic* at every non-degenerate critical point of every cubic. It is
not evidence of anything special about c = 3. What is special about c = 3 is the
**location**, q = 1. `V″(1) = 6 ≠ 0` is the Whitney A₁ condition — non-degeneracy
is the whole content, and "degenerate" asserts its opposite.

**Refinement surfaced by the repair:** `∂ṙ/∂r|_{r=1} = −2 + 2e^{−z}`, and `ż = 1`
on Γ, so `e^{−z} → 0`. **μ_max = −2 is the asymptotic transverse rate along Γ**,
exact as z → ∞, not at finite z. The word "exactly" now carries that qualifier.

**Files repaired (2026-08-12):** `ch-recurrence-ladder.html` (5 claims + 4 residual
phrasings) · `chapters-pi-phi-mu-eta-delta-sigma-omega.html` (3 + 2) ·
`ch-eta-dnls.html` (1). Each carries a dated CORRECTION NOTICE. **No conclusion was
lost** — φ stays subcritical, c* = 3 stays the unique threshold, μ_max stays −2,
the A₁ fold stays an A₁ fold.

**Already correct, left alone:** `ch-recurrence-ladder.html`'s glossary
(`V(q) + 2 = (q−1)²(q+2)`, with the +2 on the left) and Theorem μ.1 — both had been
hand-repaired earlier. **Theorem C.1 was correct all along**: it states
`V(1) = −2, V′(1) = 0, V″(1) = 6 ≠ 0`, which is precisely A₁. Only the prose
around it drifted toward sounding stronger.

**`[OPEN]` — flagged by signature, NOT yet read:** `chEps-gronwall.html`,
`chRho-spectral.html`, `chH-collatz.html`, `chE-gtct.html`. A grep hit is not a
finding; do not report these as defects until someone opens them.

**New rule for the audit method:** when a claim borrows a technical term from a
neighbouring field, check the term against *that field's* meaning, not against the
surrounding argument. An argument can be internally consistent and still use a word
that means something else to everyone who owns it. Sweep for the vocabulary of the
*strongest* nearby claim: `degenerate`, `double root`, `singular`, `exact`,
`canonical`, `unique`.

**Why it was found:** asking how a reader of combinatorial Hodge theory would see
the ladder chapters. Written up as `book7/ch-huh.html` (Scientist Gallery) and
`book6/wp61-root-language-sweep.html`. Established there, and worth keeping: the
n-bonacci polynomials are **provably not** matroid characteristic polynomials
(χ_M(1) = 0 for any matroid; p_n(1) = 1 − n ≠ 0), and their coefficient
log-concavity is degenerate (|coeffs| ≡ 1, inequality saturated). The adjacency is
real; the overlap is not. Do not claim otherwise in either direction.

### KNOWN DEFECT: the Vol IV footer block copied into Book 7 — REPAIRED 2026-08-12

Book 7's chapter footers were built by copying a Book 4 footer wholesale. The copy carried
three wrong facts at once, and they travelled together because nobody read the block, only
duplicated it:

| Line in the footer | What was wrong |
|---|---|
| `Principia Orthogona · Vol IV · GTCT T1 · Edição IMPA` | Book 7 is **Vol VII**. Wrong volume on 5 chapters. |
| `ISBN 979-8-9954416-8-7` | An **unallocated reserve** number (see the registry above). It is not Vol IV's and never was; `Bowker_ISBN_Registration_Guide.md` and `3M_README.md` label it "IMPA Edition · Hardback" aspirationally, but `isbn_metadata.json` has it on HOLD with no group and no format. Entered the repo 2026-06-03 in commit `24ea940`. |
| `doi:10.5281/zenodo.19117399` | Vol I's **concept** DOI — the Tier B defect already open above. 15 Book 7 files. |

Five of those footers additionally labelled it **"Series DOI"** (Tier A — the exact phrasing
that propagated into the JOMO pack). `ch-hawking.html` cited `19117400` instead, which is
Vol I's v1 founding deposit — right that it is a real DOI, wrong that it is Hawking's.

**Also found and fixed:** `ch-symplectic.html` and `ch-tropical.html` had a Python **list
repr of the chapter body** dumped into the footer's title slot (`Vol VII · ['<div class=...`)
— a generator bug, rendering as visible garbage on the live site.

**Repair (done 2026-08-12):** all 16 Book 7 footers now carry `Vol VII · The Scientist
Gallery` and point at the Zenodo community rather than any DOI. No ISBN line — Vol VII has
neither a deposit nor an allocation. The `ISBN fallback 979-8-9954416-5-6` line was removed
from `ch-huh.html` for the same reason.

**Still open:** book6's 87 footers and the other 18 files still carry `979-8-9954416-5-6`
labelled as the "G5 Complete Completeness eBook ISBN". Per the registry, G5's eBook is
`979-8-9954416-1-8`; `5-6` is unallocated. Not swept — same rule as the commutator ledger,
the count is a grep and not an audit.

**Second pass, same day — the defect was not confined to `<footer>`.** Sweeping whole files
rather than footer blocks found the same three errors in hero strips, chapter-header bylines,
figure captions and a Lean code comment. Repaired: `ch-lattes`, `ch-tatiana`, `ch-thoreau`
(hero strips citing `19117399` as the page's own DOI) · `the-scientists` (×2, `979-8-9954416-6-3`
labelled **"Series ISBN"** — it is Book 3's eBook ISBN, there is no series ISBN) ·
`ch-dirac`, `ch-faraday`, `ch-hawking` (chapter-header bylines; `ch-faraday` also inside a
Lean comment) · `ch-lattes` figure caption pinned to Vol I v6 `10.5281/zenodo.21146416`
instead of the concept DOI · `ch-huh` prose, which still asserted the now-withdrawn
"Vol VII uses the Vol VI eBook ISBN 5-6 as fallback" rule.

**Deliberately left alone:** `book7/jacobian-verification.html` and
`book7/wp59-dark-matter-lensing.html` both cite `19117399` *explicitly labelled as the
concept DOI* and give the current version DOI alongside. That is the prescribed form, not
a defect. A grep hit is not a finding — open the file.

**Migrated chapters keep their lineage.** `ch-ada`, `ch-curie`, `chcurie`, `ch-dirac` and
`ch-hawking` began life as Book 4 chapters and moved into Book 7 when the biographies became
their own book. Their hero strips now read `Vol VII · Scientist Gallery · originalmente
Vol IV, submetido ao IMPA` — where it lives now, and where it came from. The `Vol IV` nav
links (`../book4/index.html`) and the "GTCT Vol IV, Ch 5" citations are **correct** and must
not be swept; they genuinely point at Book 4.

### KNOWN DEFECT: two Book 7 chapters shipped empty — REPAIRED 2026-08-12

`ch-symplectic.html` and `ch-tropical.html` rendered as **blank chapters** on the live site:
h1, nav and footer only, zero body. The generator swapped two arguments — the chapter title
was iterated character-per-line into the body slot (20 lines each reading `G`, `e`, `o`, …),
and the body, a Python list of five HTML block strings, was `str()`-dumped into the
`<span class="ch-nav-mid">` slot and into the footer's title slot.

Recovered by `ast.literal_eval` on the list literal (escaping resolves to single-backslash
LaTeX, matching working siblings such as `ch-connes`), then writing each part back where it
belonged. Both pages now carry their two bilingual sections, section strips, theorem blocks
and pull quote; markup balanced, verified. **If any other chapter's body looks short, check
for a `['<div` in a nav or footer slot before assuming the content was never written.**

**Also completed 2026-08-12:** the nine Book 7 files that had no `<footer>` at all
(`ch-cross-staff-and-ledger`, `ch-keplers-correspondents`, `ch-levi`, `ch-metchnikoff`,
`ch-pasteur`, `tutor-card-ada/curie/dirac`, `ulam-dual`) were given one. Book 6 and Book 7
are now at 87/87 and 52/52.


### KNOWN DEFECT: the Alterna name collision — RECORDED 2026-08-12

**A third costume for the 5.3 mechanism — this time a *name*, not a number, and the
false version came from outside.**

`Alterna` = **WP-02**, `10.5281/zenodo.20710023`, *"Alternating Forms Vanish Beyond
Dimension: A Mechanized Proof in Lean 4 with Application to Contact Integrability"*,
deposited 16 June 2026. Verified against the Zenodo record 2026-08-12. Chapter now at
`book6/wp02-alterna.html` — it previously had four inbound citations and **no page**,
which is what let the name be filled with something else.

| | Alterna (yours) | The impostor |
|---|---|---|
| Field | multilinear algebra | 2-adic number theory |
| Statement | alternating *m*-linear map on rank-*n* module ≡ 0 when *m* > *n* | ∇ₖ v₂(3x+1) vanishes on alternating dyadic classes |
| Status | **closed**, Lean 4, 12 lines, 0 sorry | **false** — its non-vanishing claim fails ∀ k ≥ 3 |

The impostor was produced by an external LLM asked about this corpus. Its Claim A holds;
its Claim B is false because by its own argument `v₂ = 1` on *both* residue classes.
The salvageable true fact is elementary: **λ₃(x) = 1 ⟺ x ≡ 3 (mod 4)**, density ½ among
odds — one mod-4 condition, no scale hierarchy.

**Repaired in the same pass:** `ch15-complex-turn.html` Theorem 15.2 carried a stale
`sorry` (Alterna had closed it two months earlier) **and** two corollaries that are false
on parity — `(T_Γ M, J|_Γ)` as a complex vector bundle (rank 3, odd) and Γ as a complex
submanifold (dim 1, odd). A *J*-invariant subspace is even-dimensional: `v, Jv`
independent ⟹ dim ≥ 2. The vanishing is true; Newlander–Nirenberg does not follow from it.

**Level 2 is where the mathematics is.** The deposit closes level 1 of a three-level
integrability tower. Level 2 is `N_J` on the rank-2 contact distribution `ξ = ker α`,
where `m = n = 2` and the inequality `m > n` **fails** — the dimension count is silent
there and a real computation is needed. `[OPEN]`.

**Rule added:** a claim can be hijacked by *name* as well as by number. When an external
tool returns something bearing a corpus term, check the object, not the label — and
prefer giving every deposited result its own page, because an unhoused DOI is an
invitation.

## Hardback constraint

The **Complete Completeness hardback** (G5 print, ISBN 979-8-9954416-4-9) must stay
at **666 pages maximum** when sent to print. This is a structural target, not a soft limit.
666 = 6 × 111, resonant with the hexanacci/g6 threshold and the 111 Hz sacred frequency.
Any new content added to G5 must be measured against this constraint before inclusion.

## Site structure

- `geometry/` root = Book 3 (G3) chapters, prelude, overture, portals
- `geometry/book4/` = Book 4 (G4) chapters + G5 student edition + living-book.html
- Ring nav: G3 · Part I/II/III/IV → G4 → G5 (injected as `.po-ring-strip` after `</nav>`)
- Spiral map: `book4/living-book.html` — the G1–G5 hub
- Standard typography: follow `prelude.html` (Georgia 18px, line-height 1.75, #e8e4d8)

## File indexes — generated, never hand-maintained

`master-index.html` + `index-<folder>.html` (16 pages, repo root) are produced by
`tools/build_indexes.py` from a filesystem crawl. **Re-run it after adding or moving any
page**; do not hand-edit the output.

```bash
python3 tools/build_indexes.py     # 630 files, 74 orphaned as of 2026-08-12
```

An index that says *"this file is orphaned"* is a positive claim someone will act on, so it
gets the same treatment as any other derived fact here: recomputed, not remembered. The
first hand-generated version was already stale on delivery (missing `ch-huh.html` and
`wp59-root-language-sweep.html`) and had a **13% error rate on the orphan tag** — 10 of 76
wrong. Four failure modes, all now handled in the crawler and all worth knowing because they
recur in any link checker written for this repo:

1. **The generated indexes must be excluded as link sources.** `master-index.html` links to
   every file; count it and the orphan column reads zero forever.
2. **Resolve by path, not basename.** `ch-tatiana.html` and `ch6-resonance.html` each exist
   twice (root *and* a subfolder). Basename matching credits links to the wrong copy — it
   marked `ch-tatiana.html` linked and `book7/ch-tatiana.html`'s inbound links vanished.
3. **Site-absolute hrefs count.** `ch07-four-orbits.html` is linked as
   `/geometry/ch07-four-orbits.html` and was reported orphaned.
4. **Some nav is built in JavaScript.** `.html` literals inside `<script>` are real links
   (`omega/trinity-father.html`, `wk02-compression.html`, `wk06-threshold.html`).

Titles are unescaped from `<title>` and re-escaped exactly once; the original double-escaped
them, rendering a literal `&middot;` on every affected row.

## Duplicate pages — declared, or a finding

Added 2026-08-25. **Run `python3 tools/duplicates.py` before creating any page,
and after moving one.**

### The cause, stated plainly

Sessions run out of context and continue on another account. The next session
does not always see what the previous one left, or it continues and writes into
a different folder. Nothing looks wrong when it happens — two copies of a page
behave identically until somebody edits one. After that the corpus has two
answers and no record of which is current, and neither page mentions the other.

`book7/ch-curie.html` and `book7/chcurie.html` reached **516 lines apart** that
way. Same title. One linked from the Book 7 hub, series-hub and `ch-ada`; the
other from `master-index`, `ch-pasteur` and `ch-metchnikoff`. The newer copy
decomposed a `sorry` the older left opaque — γ = 1 → γ = 6/5 (U→C→K→F) →
γ ≈ 1.24 — so which text a reader got depended on which page they arrived from.
Merged 2026-08-25; `chcurie.html` is now a redirect that records why.

The sweep that found it found **32 more**. The whole `HVEH/` ↔ `book4/` chapter
set — `ch02`, `ch06b`, `ch07`, `ch08`, `ch09`, `chHALO`, `ch-build-2river` — is
one directory copied once with both copies edited since; five of the seven have
drifted apart.

### What this file already said, and why it was not enough

The **File indexes** section above records that `ch-tatiana.html` and
`ch6-resonance.html` each exist twice and instructs the crawler to *"resolve by
path, not basename."* That is a workaround for the duplication, not a fix, and
it made the crawler correct while leaving the corpus wrong. **What NOT to do**
separately forbids merging `ch7-topological-orthogenesis.html` and
`ch8-nested-infinities.html`, which are intentional alternate editions.

So both facts were known and neither was actionable: nothing prevented a new
duplicate, and nothing distinguished an intended pair from an accident. Reading
the two rules together, a future session could conclude either that duplication
is normal here or that it is forbidden, and both readings are wrong.

### The rule

**One page, one home, unless the pair is declared.** Declared groups live in
`tools/duplicate_ledger.txt`, append-only with a reason, in the same style as
`KNOWN_PLACEHOLDERS.txt`. `tools/duplicates.py` fails on any undeclared group.

Adding a line to the ledger is a decision that **both copies are maintained**.
If that is not true, merge and leave a redirect — the Curie shape. A redirect
stub is not counted as a copy, because it has no paragraphs of its own.

Before creating a page, check that its title is not already taken. Before
moving one, check what links to the old path. Both are one command.

### Before trusting the similarity number

The first version of this sweep used 8-gram shingles across the whole document.
It reported **2%** similarity for two files that are **100%** identical
paragraph for paragraph. Written up as it stood, sixteen pure duplicates would
have been presented as unrelated pages that happen to share a title, and every
one of them would have been left in place.

It was caught only because the Curie pair had already been compared by hand, so
there was a known answer to check the metric against. `duplicates.py` therefore
runs `--self-test` on four synthetic cases with hand-computed answers *before*
it reports anything, and refuses to continue if the metric is wrong.

**An instrument with no known-answer case is not known to work.** That is the
same rule the axiom gate, the conclusion scan and `vendor_check.py` follow, and
this is the fourth place it has paid for itself.

### The churn this doctrine causes, and the limit on it

"Recomputed, not remembered" is the right rule and it has a failure mode that
produces the very drift it exists to prevent.

Verification is cheap for a **claim** and expensive for an **instrument**. A
session that will not trust a recorded count and recomputes it costs a command.
A session that will not trust a recorded *tool* and rebuilds it costs a second
tool — and now there are two, they will diverge, and neither knows about the
other. The doctrine, read carelessly, licenses exactly that.

Both halves have to be said, because only one of them was:

- **Claims are recomputed, never inherited.** Counts, statuses, link validity,
  sorry totals, theorem totals, "fixed" — every one of these decays, and a
  figure in prose is a claim about a moment, not about the world.
- **Instruments are reused, never rebuilt.** An instrument is checked against
  its fixtures. If it passes, use it. If it fails, fix *it* — do not write a
  second one beside it. Before writing any tool, grep `tools/` for one that
  already does the job.

Two specimens from 2026-08-25, both the assistant's:

- Asked whether any Prop-definition ignores an argument, it wrote a textual
  regex scanner — which over-matched, reported `V` as taking 37 explicit
  arguments including one named `-2`, and answered a question that
  `#unused_param_scan` already answered correctly. A broken second instrument
  built next to a working first one, while explaining why not to.
- It generated a corrected `lakefile.toml`, `probe.lean` and `run.sh` for
  `vol1-proofs` against a HEAD one commit stale, and nearly committed a
  configuration that would have left `AutophagyDm3_v2.lean` in the tree with no
  target building it. Caught by an unrelated `git rm` failing, not by judgment.

The cheap guard for the second: **`git log --oneline -1` before generating any
file for a repository, not after.** The cheap guard for the first: search before
you build.

### Working through the backlog

The 32 groups split three ways, and only the third needs judgment:

- **Pure duplicates (≥ 90 %)** — identical content, two or three homes. Pick
  the home matching the naming convention, redirect the others, repoint
  inbound links, regenerate indexes.
- **Diverged (40–90 %)** — real edits on both sides. Compare paragraph sets,
  establish which is the refinement, merge as with Curie.
- **Same title, different content** — the title is wrong on one of them, not
  the file. Retitle rather than merge.

Do not batch these. Each is a decision about which text is current, and the
Curie case shows the answer is not always the larger file or the newer mtime.

## Threshold, not scale — the guard on fold language

Added 2026-08-26. **The shared structure is the threshold, not the scale.**

Fold, criticality and threshold language is the most portable vocabulary in this
corpus and therefore the easiest to misread. The misreading is always the same:
a reader takes a claim that two systems share a *shape* and hears a claim that
one supplies the *mechanism* for the other.

The true claim, stated once so it can be cited rather than re-derived:

- Near a critical point, susceptibility to the **parameters** of the governing
  equations diverges. Arbitrarily small parameter changes produce qualitatively
  different outcomes. This is the definition of criticality, not a metaphor.
- A system driven slowly to a threshold and then crossing it irreversibly has
  the same *shape* whether the driver is a detuning laser, a decade of glacial
  melt, or a curvature accumulating toward κ*. Shape, not substrate.
- Irreversibility has an address: the second-order line is reversible, and the
  **tricritical point is where it stops being so** — past it the transition is
  first order and hysteretic. If F is about irreversible rank loss, the
  tricritical point is its analogue, not the ordinary critical point.

Stated as three clauses, which is the form to use because the guard is then part of the
claim rather than an appendix to it:

- **Scale-invariant** — at the critical point, technically: power-law correlations, no characteristic
  length. This is why a conformal description can emerge.
- **Domain-agnostic** — by universality, and for a reason: a universality class is fixed by symmetry
  and dimension, not by constituents. The 2D Ising class contains a magnet, a liquid–gas critical
  point, and a chain of nineteen strontium atoms.
- **Predictive of the universal data only** — ratios, exponents, central charges, degeneracies.
  Silent by construction on every scale: where the transition sits, how fast anything moves, how big
  anything is. **A claim of this kind that appears to predict a scale is either fitting it or has
  smuggled in a substrate.**

This is the standard universal / non-universal distinction of critical phenomena, not a coinage.
WP-79's filter is that distinction applied to our own quantities.

Two things that must travel with it, every time:

1. **The sensitivity is to parameters, not to states.** In a quantum system,
   unitary evolution preserves the overlap between two states exactly; there is
   no exponential state-to-state divergence of the classical-chaos kind. What is
   exquisitely sensitive is the dependence on the Hamiltonian's knobs. "Tiny
   changes" is true of parameter space and false of state space.
2. **It is a property of sitting at criticality, not of being quantum, small,
   or fundamental.** Off the critical point susceptibility is finite and small
   perturbations do small things. Generic systems are not at their critical
   points, which is why the world is mostly stable.

**Never claim, and never let a page imply, that the quantum scale supplies the
mechanism at the geological, biological or civilisational one.** A glacier fails
from accumulated stress under a warming trend — classical, slow, and with a
threshold. The threshold is the shared object. Nothing crosses the scale gap,
and the argument does not need it to.

Live exposure, surveyed 2026-08-26: `ch-belousov-zhabotinsky.html` carries the
heading "From Quantum to Cosmic — Complex Systems at Every Scale" over a quoted
programme note. The quote is defensible as written — ordered behaviour *is* found
at all scales — but the heading invites the mechanistic reading, and the guard is
now stated on the page. Fifteen further files use "at every scale"; most are
about self-similarity of a mathematical object, which is a different and correct
claim. Re-survey with:

    grep -rn -i "at every scale\|from quantum to\|across all scales" --include="*.html" .

---

## What NOT to do

- Do not hand-edit `master-index.html` or `index-*.html` — regenerate them
- Do not add a print ISBN to Book 3 / Vol III pages
- Do not create a `book5/` directory without user instruction
- Do not merge or deduplicate the shadow pages (ch7-topological-orthogenesis.html,
  ch8-nested-infinities.html) — they are intentional alternate editions, and they
  are declared as such in `tools/duplicate_ledger.txt`
- Do not create a page without running `python3 tools/duplicates.py` first — 32
  undeclared duplicate groups exist as of 2026-08-25 and the mechanism that made
  them (a session continuing on another account, in another folder) is still live
- Do not write a new tool when `tools/` has one for the job. Claims are recomputed;
  instruments are reused. Rebuilding an instrument is how a second one appears
- Do not mark AXLE theorems as "✓ Lean 4" without the "(under SH)" caveat
  if they depend on the Structural Hypothesis (SH)
- Do not use Cormorant Garamond in book4 pages — it has no math glyph coverage
- Do not let fold/criticality language imply a scale bridge. The shared structure
  is the threshold, not the scale — see the guard section above

---

# KNOWN DEFECT: the false commutator lemma (opened 2026-07-18)

**A single false lemma has propagated across the series, the Zenodo deposits, and
at least one Lean file.** It is not a typo — it is a load-bearing derivation that
several chapters and papers rest on. If you are working anywhere in this repo and
you encounter an operator-order argument, read this section before touching it.

## The false claim, stated exactly

> Let `K` = multiplication by a Heaviside/indicator gate `θ(η* − η)` (a 0/1 mask),
> and `F` = the **pointwise** fold `F[ψ] = ψ + λ|ψ|²ψ` (a Nemytskii operator).
> Then `[K,F] ≠ 0`, the commutator being a boundary term `∝ δ(η − η*)`.

**This is false.** `K` and `F` commute *exactly*, everywhere, for every state.
There is no boundary term, no distributional subtlety, nothing "left to the
distributional-calculus literature." The δ does not exist.

**Proof (general, one line each way).** Let `K` be multiplication by an indicator
`χ` and `F` be any pointwise map `f` with `f(0) = 0` — true here since
`0 + λ·0 = 0`. Then `K(F(ψ)) = χ·f(ψ)` and `F(K(ψ)) = f(χψ)`. Where `χ = 1`
both equal `f(ψ)`; where `χ = 0` both equal `0`. Equal everywhere. ∎

Equivalently, in the finite setting where it is machine-checked: for a 0/1 gate
`g`, `(g·v)³ = g³v³ = g·v³` because `g³ = g` on `{0,1}`. A gate and a pointwise
map both act sitewise, so their order cannot matter.

**Kernel-checked** in `TOTOGT/io` → `zeolite_operator_order/ZeoliteCommutation.lean`
(Lean v4.33, `#print axioms` clean — `[propext, Classical.choice, Quot.sound]`,
no `sorryAx`):

- `gate_commutes` — the gate commutes with the pointwise fold, for every state
- `coupling_not_commute` — inter-site coupling does NOT commute with the on-site fold
- `gate_fold_not_commute` — the gate does NOT commute with `F = coupling ∘ onsite`

## How to recognise it in the wild

The derivations that carry this defect share a tell: **they derive that the two
compositions are equal, then assert the δ anyway.** Two examples already found:

- `book4/chIV-orthogonality.html` Lemma 5.3 — step 2 gives
  `KFψ = θ(ψ + λ|ψ|²ψ)`; step 3, via `θ² = θ`, gives `FKψ = θ(ψ + λ|ψ|²ψ)`.
  Identical. Step 4 introduces the δ from nowhere.
- `ALGEBRAIC_PROOFS_D1_RIBOSWITCH.md` — writes, in the text,
  *"This appears to vanish — but the issue is the region η ∈ (η*, 1]"*,
  and then produces the δ. It noticed, and argued past it.

Grep patterns that surface candidates:

```bash
grep -ril "λ|ψ|²ψ" .                       # the pointwise fold
grep -ril "δ(η − η\*)\|δ(r − r_"           # the asserted boundary term
grep -ril "θ² = θ\|θ³\|idempotent"         # the step that proves equality
grep -ril "\[K,F\]\|\[K, F\]\|commutator lemma"
```

## How it propagated: the 5.3 collision

**Two different statements share the number 5.3, and that is the whole mechanism.**

- **Vol I §5.3, `vol1-mathematics.html` — TRUE, and the root.**
  *"Theorem 5.3 · Non-Commutativity: The operators C, K, F, U do not commute;
  the sequence is order-dependent."* Chain-level, no mechanism asserted. This is
  the claim kernel-verified in `TOTOGT/io` →
  `PrincipiaOrthogona1/Theorem53NonCommutativity.lean`. **Leave it alone.**
- **`book4/chIV-orthogonality.html` Lemma 5.3 — FALSE, and the injection point.**
  Same number, different claim: it "upgrades" the true abstract statement into a
  specific mechanism (gate acting on a pointwise fold, δ boundary term). That
  upgrade is invalid.

Downstream chapters citing "5.3" could mean either. Those that took the abstract
statement are fine; those that took the mechanism inherited a false lemma. **When
fixing, always check which 5.3 a file is citing.**

## Status ledger — file clusters. UPDATE THIS as files are settled

### Cluster 0 — ROOT, clean. Do not touch.
| File | Why |
|---|---|
| `vol1-mathematics.html` (+ `book1/`, `_archive/…-REMOTE` copies) | States chain-level 5.3 only. True, kernel-verified. |
| `TOTOGT/io` → `Theorem53NonCommutativity.lean` | Existential over chains; exhibits an order-dependent AND a commuting instance. Clean axioms. |

### Cluster 1 — CARRIERS. Confirmed false, must be repaired.
| File | Location | Fixed? |
|---|---|---|
| `book4/chIV-orthogonality.html` | Lemma 5.3 — was "Distributional Commutator", **injection point** | **YES — 2026-07-18.** Restated as "Locus of Non-Commutativity" (2 parts), correction notice added, proof steps 4–5 replaced, summary-table row fixed. Steps 1–3 untouched (were correct). |
| `ALGEBRAIC_PROOFS_D1_RIBOSWITCH.md` | §D1 derivation (D1 domain) | **YES — 2026-07-20.** This is the file that *noticed* the commutator vanished ("This appears to vanish — but…") and argued past it with a δ from d/dη θ. Correction notice added; the δ argument replaced with the real coupling: non-local aptamer/SD base-pairing (F_pair moves amplitude between distant nucleotides). Statement corrected to `[K, F_pair] ≠ 0`. Summary checklist row fixed. Downstream D1-T2…T6 unaffected. |
| `ch18-zeolite-noncommutativity.html` | §18.2 (D2 domain) | **YES — 2026-07-20.** Only the *imported* δ formula was false; **Theorem 18.1 itself is sound and unchanged.** Its gate `K = θ(η* − d(ψ))` is threshold-**state-dependent** and F changes `d(ψ)` — a gate whose argument the fold rewrites genuinely fails to commute. The δ was never doing the work. Correction notice added; the invocation replaced with the correct grounding. |
| `ALGEBRAIC_PROOFS_CH7_CRYSTALLINE_RETURN.md` | Ch7-T1 Step 5 (Saturn hexagon / D₆) | **YES — 2026-07-20.** Step 5's false radial-gate claim replaced by the correct 3-part statement; 5 new theorems kernel-verified in `SaturnHexagon.lean` (Lean v4.14.0, axioms clean) including the D₆-specific `rot_commutes_coupling` and `hex_coupling_uniform`. Steps 1–4 and the D₆ conclusion untouched. |
| `zeolite_operator_selectivity_v2.tex` (in `TOTOGT/io`) | Theorem 1 | **YES → v3, 2026-07-18** |

**Cluster 1 is concentrated in Book 3 (The Mini-Beast) — its D1–D4 domain
chapters lean on this as their central claim.** Book 3 is eBook-only and an
explicitly living document (see ISBN map above), so it can be revised without a
print run. That makes it the cheapest cluster to repair and the most urgent, since
it is the one that presents the lemma as the book's spine.

### Cluster 2 — **VERIFIED 2026-07-29. ch19 and ch20 CLEAN, no edit needed. research-status.html has two housekeeping defects (not the δ).**

- **`ch19-enzyme-noncommutativity.html` (D3) — CLEAN.** Theorem 19.1's gate is
  `Kψ = θ(c* − |c(ψ) − c_bound|)ψ` — threshold-**state-dependent**, and F changes
  `c(ψ)`. Same structurally sound form as the repaired Theorem 18.1: a gate whose
  argument the fold rewrites. No δ asserted anywhere; cites the abstract Vol I §5
  statement only. The chapter even states outright that "Theorem 5.3 does not
  require K and F to act on separable structures."
  **Watch item, not a defect:** its fold is written `Fψ = ψ + λ·R(ψ)`, which has
  the *same shape* as the false pointwise fold. It is sound only because `R(ψ)`
  is a conformational operator acting non-locally, not `|ψ|²ψ`. If a later pass
  ever "simplifies" R to a pointwise map, this chapter becomes a carrier. Leave
  R symbolic.
- **`ch20-saf-noncommutativity.html` (D4) — CLEAN, and stronger than the ledger
  assumed.** It does not inherit a mechanism; it sharpens the claim into a
  controllability statement — if K and F are co-located with no separation in
  space, time, or catalyst identity, `[K,F]` is not merely nonzero but
  *uncontrolled*. The worry that D4 chains through D2 is resolved: ch18's
  Theorem 18.1 was itself found sound, so the chain rests on nothing false.
- **`research-status.html` — two defects, both housekeeping.**
  1. It cites `ALGEBRAIC_PROOFS_ALL_7_THEOREMS.md §4.4` as the paper of record for
     the MAIN selectivity theorem — the file Cluster 1b marks *delete, do not
     edit*. Deleting it as instructed would leave a dangling citation here and in
     `ALGEBRAIC_PROOFS_CH7_CRYSTALLINE_RETURN.md`. **Repoint both to
     `TOTOGT/io → OPERATOR_ORDER_DERIVATIONS_AND_STATUS.md` before deleting.**
  2. Its Theorem 5.3 row describes the Lean status as "1 disclosed sorry —
     `CatGT_PROOFS_COMPLETE.lean` — NonCommutativity, **boundary-discontinuity**".
     That lemma name is a possible δ residue in the Lean layer. The file lives in
     `TOTOGT/io`, not this repo, so it was **not** inspected — `[OPEN]`, check it
     there before citing this row.

### Cluster 2 original note — cite chain-level 5.3 only; probably fine, verify once each.
`ch19-enzyme-noncommutativity.html` (D3) · `ch20-saf-noncommutativity.html` (D4) ·
`research-status.html`

These quote the *abstract* statement ("the operators do not commute") rather than
the δ mechanism, so they may need no change at all — but each one's argument
should be read once to confirm it does not silently rely on the gate/pointwise
version. D4 in particular chains D3's K,F to D2's K,F, and D2 (ch18) is a carrier.

### Cluster 3 — TRIAGE. **SETTLED 2026-07-18 — all three CLEAN.**
- `AMonster/dm3_operators.lean` — `C₃ ∘ C₃ = C₃`, a genuine projection
  idempotency, Lean-checkable. Unrelated to the gate/fold commutator.
- `book6/ch03-explicit-Ai-matrices.html` — E₈ Lie-algebra commutators
  `[A_i, A_j]` and `P² = P`. Different mathematical context entirely.
- `omega/ch-resonance.html` — `R² = R` for the resonance projector. Standard.

None reproduces the derivation. Projections *are* idempotent; that fact is not
the defect. The defect is only ever: gate + **pointwise** fold → asserted δ.

### Cluster 1b — CARRIERS FOUND ON THE SECOND PASS (2026-07-20)
The first sweep grepped for the literal string `λ|ψ|²ψ` and therefore missed
files that assert the δ using different notation. A signature-based rescan
(δ boundary term, in any notation) surfaced these. **None repaired yet.**

| File | Note |
|---|---|
| `ALGEBRAIC_PROOFS_ALL_7_THEOREMS.md` | **Stale duplicate**, superseded in `TOTOGT/io` by `OPERATOR_ORDER_DERIVATIONS_AND_STATUS.md`. The earlier note here said "delete, do not edit." **DECISION 2026-07-29 (author, explicit): do NOT delete.** The file stays. Consequence: the citations to it from `research-status.html` and `ALGEBRAIC_PROOFS_CH7_CRYSTALLINE_RETURN.md` are no longer dangling-reference risks and need no repointing. But the file **still carries the false δ** and is still superseded, so it must not be cited as the paper of record going forward, and anyone reading it needs to know. **DONE 2026-07-29:** correction notice added at the head — retained-but-superseded, "DO NOT CITE", pointing to `OPERATOR_ORDER_DERIVATIONS_AND_STATUS.md`; Theorem 1's `✓` replaced with a dated `✗ WITHDRAWN` naming the DNLS `J` hopping term as the recoverable route and flagging that Theorems 4 and 7 chain through it; the self-awarded "10/10" and the 9/10→10/10 sentence neutralised. |
| `HVEH/distribution-theory.html` + `HVEH/proofs/distribution-theory.html` | **YES — 2026-07-29.** Both paths repaired (byte-identical, md5 `5c126293`). This one is *not* the commutator error — the distributional identity `d/dr H(r−r*) = δ(r−r*)` here is **true**. The defect was three inferences drawn from it: (i) the page claimed the δ "is not an artifact of the model" when it is precisely an artifact of the assumed discontinuity (smooth the shear layer to width ℓ and you get a bounded bump of height ~1/ℓ, no δ); (ii) it called δ an energy density, never derived; (iii) it claimed thermodynamic one-wayness "without invoking entropy" — impossible, since distributional differentiation is time-symmetric. **Engineering conclusion survives on different grounds:** hysteresis via the subcritical fold (Proof III's territory), with the shutdown-vs-startup setpoint gap now tagged `[OPEN]` and flagged as requiring measurement on a physical basin. Claims retagged `[VERIFIED — textbook]` / `[MODEL]` / `[OPEN]`. **Note the new failure mode: a true lemma with false inferences hung off it.** The signature grep for an asserted δ will not catch this class — scan also for "proves irreversibility", "without invoking entropy", and "not an artifact". |
| `HVEH/ch06b.html` | **YES — 2026-07-29.** Only the Proof II summary card was affected ("Differentiating the gate H(r − r*) yields an unavoidable δ(r − r*) boundary term: the transition is one-way"). Retitled "Sharp-interface idealization" and restated to match the repaired Proof II page. Tagged `[MODEL]`. Proof I and III–VII cards untouched. |
| `book4/ch06b.html` + `book4/ch06b-elojo.html` | **ALREADY REPAIRED — 2026-07-26** (this ledger row was stale; corrected 2026-07-29 after verification). Both paths byte-identical, md5 `c96aa1cf`. Proof II card retitled "Transport term, not a gate derivative", `[MODEL]`-tagged, with a dated correction note in the Synthesis section attributing order-dependence to the advective vortex-transport term inside F. **Consistency note:** that repair and the 2026-07-29 Proof II repair are compatible but emphasize different mechanisms — advective transport is what makes `[K,F] ≠ 0` (order-dependence); the subcritical fold is what makes the transition hysteretic (path-dependence); viscous dissipation is what makes it thermodynamically irreversible. Three distinct claims that the original conflated into one δ. Keep them distinct when editing either file. |

So ~5 unique documents remain, not 70.

### Cluster 1c — PROOF I. Found by the Cluster 4 sweep, 2026-07-29. **REPAIRED, 11 files.**

**The first two repair passes fixed Proof II and left Proof I asserting the same
thing in words.** `HVEH/operator-algebra.html` said the commutator is "nonzero,
*localizing at the fold point*" — a commutator concentrated at one radius is the
δ(r − r*) claim with the symbol removed, which is exactly why the signature grep
never caught it. The page used "proof"/"provable" 18 times and contained **no
derivation at all**: no KFψ/FKψ expansion, no steps (violating rules 1 and 3).

Worse, its K is *fixed* geometry — sills and vanes, a static mask. A static gate
composed with a pointwise map commutes exactly (`gate_commutes`), so as written
the page asserted the false lemma outright.

**Conclusion survives; the reason was wrong.** F is advective — vortex tightening
moves vorticity *between* radii, so F is not sitewise and a static radial gate
genuinely fails to commute with it (`coupling_not_commute`). Same mechanism the
2026-07-26 book4 note identified. The repaired page now shows the one-line
commuting argument for the pointwise case, then the transport argument for why the
real F escapes it, tagged `[MODEL]` for the continuum claim with thresholds `[OPEN]`.

Files corrected (all 11, HTML verified): `HVEH/operator-algebra.html` +
`HVEH/proofs/operator-algebra.html` (identical source, md5 `0c5b00aa`) ·
`HVEH/index.html` · `HVEH/proofs/index.html` · `HVEH/ch06b.html` · `HVEH/ch08.html` ·
`book4/index.html` · `book4/ch06b.html` · `book4/ch06b-elojo.html` ·
`book4/ch08.html` · `book4/ch08-harrison.html`.

**Lesson for the ledger: repair the whole proof family, not the named file.** The
defect migrated to the adjacent proof and to code comments (`// Proof I —
commutator localises at the fold` inside `.eq` blocks in three ch08 files). Add to
the rescan: `locali[sz]\w* at the fold`, and check summary cards and code comments,
not just prose.

### Cluster 4 — BACKGROUND. Swept 2026-07-29: 79 files touch the vocabulary. Tier A = 10, **zero unaccounted**; Tier B = 0; Tier C = 21 (Proof I family now repaired); Tier D = 48 vocabulary-only, matching the estimate below.
No fold, no gate, no δ, no commutator citation. Expected clean. Sweep last, and
only to confirm.

### How to rescan (use the SIGNATURE, not the vocabulary)
The first sweep undercounted because it matched one literal glyph string. Scan
for the *asserted boundary term* in any notation, then tier:

```bash
grep -rlE 'δ\(\s*[ηr]\s*[−-]\s*[ηr]' . --include=*.html --include=*.md --include=*.tex
```

Tier A = δ asserted · B = pointwise fold + gate/commutator · C = cites `[K,F]`
or "the commutator lemma" · D = vocabulary only. Expect false positives in A
from this file and from any *repaired* file, since corrections quote the claim
they retire — check whether the match sits inside a correction notice before
treating it as a carrier.

**The true count of affected published records is not yet established.** Do not
write a number into any document until each file has been opened. Overstating the
blast radius is the same error as overstating a proof.

## NOT affected — do not "fix" these

- **`PrincipiaOrthogona1/Theorem53NonCommutativity.lean`** (in `TOTOGT/io`) is a
  *different claim wearing a similar number*. It is existential over chains —
  it exhibits an order-dependent instance **and** a commuting instance on the same
  manifold — and it is kernel-verified clean. The false thing is the prose
  Lemma 5.3, not the Lean Theorem 5.3. Keep these separate when communicating,
  or you will spread alarm about a theorem that is fine.
- Chain-level order-dependence in general is **true**. What is false is the
  specific claim that a *gate acting on a pointwise fold* generates it.

## The correct repair

**Do not delete the conclusions — repair the derivation.** In every domain checked
so far, the genuine coupling already exists in the physics; it was simply left out
of the operator definition:

| Domain | The coupling that was omitted from `F` |
|---|---|
| Zeolite selectivity | the `J` hopping term of the DNLS equation |
| Saturn hexagon / D₆ | the `r⁶cos(6θ)` angular term in the Hamiltonian |
| Riboswitch | non-local base-pairing along the chain |

The repair is: **let `F` carry its coupling term** — `F = F_coupling ∘ F_onsite`,
not the pointwise map alone. Then `[K,F] ≠ 0` becomes *provable* instead of
asserted, and the downstream conclusions (D₆ stability, riboswitch switching,
ZSM-5/MCM-22 divergence) most likely survive intact. What dies is the derivation,
not the result.

Order-dependence is carried by whichever operator **moves amplitude between
sites** — never by a gate acting pointwise. That sentence is the whole content of
the defect, and it is the sentence to put in each correction.

See `TOTOGT/io/zeolite_operator_order/OPERATOR_ORDER_DERIVATIONS_AND_STATUS.md`
for a worked example of a corrected document.

## Rules for anyone fixing these

1. **Kernel-check before writing "proved."** No claim moves to VERIFIED without
   either green CI or a paste into a real Lean kernel that you watched come back
   clean. Fluent prose is not evidence — that is what produced this defect.
2. **Tag every claim** `[VERIFIED]` / `[MODEL]` / `[SIMULATION]` / `[OPEN]`, and
   never let a claim drift between tags.
3. **No document scores its own rigor.** No "10/10", no `∎` on a sketch.
4. **A correction to a published Zenodo record is the author's call.** Draft it,
   show it, do not deposit it. Amending a DOI is not a routine edit.
6. **Never wholesale-replace a working file** to fix this. Minimal edit to the
   specific lemma, then update the ledger above in the same session.
7. **Update this ledger** when you settle a file — mark it fixed, or move it out
   of triage. A future session will trust this table; leaving it stale recreates
   the original problem in a new place.
7. **A caveat may only be removed by the same edit that verifies the thing it
   hedges — never as tidying.** This is the corpus's most frequent failure mode,
   observed four separate times on 2026-07-18/20:
   - zeolite Theorem 1: "left to the distributional-calculus literature" deleted,
     the false δ asserted in its place;
   - Ch M: a Nobel date stated flatly, off by 26 years;
   - the wildfire toxicity multiplier: a coarse-fraction result silently
     transferred to PM2.5;
   - the Maya reference: "(volume/issue to confirm)" removed while an
     unconfirmed volume/issue was added.

   In each case the original author *knew* something was uncertain and said so,
   and a later pass cleaned up the flag instead of resolving the uncertainty.
   If you cannot verify it, leave the hedge exactly where it is.

---

# OPEN TODO: Book 3's ISBN is on pages that are not Book 3 (opened 2026-08-17)

**Not swept. Do not sweep it in passing.** Logged here so it is settled deliberately,
the way the DOI cluster was, rather than by a confident pass over 76 files. The last
confident ISBN pass is the one that put an unallocated reserve number into 87 book6
footers and 19 other files as though it were real; that is the failure this entry exists
to avoid repeating.

## Measured 2026-08-17 (all spellings: hyphenated, unhyphenated, loose-hyphen regex)

| Measure | Files |
|---|---|
| HTML files carrying `979-8-9954416-6-3` | **76** |
| …using the unhyphenated form `9798995441663` | 0 — only one spelling is in use |
| …on Book 3 / Vol III pages, where it is **correct** | 41 |
| …on other pages, **needs review** | **35** |
| …explicitly labelled "Series ISBN" | **3** — wrong by construction |
| …inside a `<footer>` | 54 |
| …body-only | 22 |

`979-8-9954416-6-3` is **Book 3 · Mini-Beast · eBook PDF**. It is not a series number.
On a page belonging to any other volume it asserts an allocation that does not exist,
and the rule above is unambiguous: *a volume without its own registered ISBN gets no
ISBN line at all — do not borrow one from a volume that does.*

## Already settled

- `book6/on-publication.html` — **fixed 2026-08-17.** Footer read `Series ISBN
  979-8-9954416-6-3` on a Vol VI page whose own provenance notice states Vol VI has no
  ISBN allocation. Line removed; footer now points at the Zenodo community only. The
  same edit removed `10.5281/zenodo.19117399 (series root)` from the hero, per the
  standing instruction not to restore that label.

## Still open in book6

- `book6/wp02-alterna.html`

Settled since: `book6/index.html` — **fixed 2026-08-17.** Carried it twice, in the
hero strip and the footer, both labelled "Series ISBN", three lines above the notice
stating Vol VI has no allocation. Both removed; 0 occurrences remain in the file.

## The repair, when it is taken up

1. Classify before editing. A Book 3 / Vol III page keeps the number — 41 of the 76 are
   legitimate and must not be touched. Automated removal would strip Book 3's only
   registered-in-progress identifier from its own pages.
2. On any non-Book-3 page, delete the ISBN line entirely. Do not substitute another
   volume's number, and do not invent a "series ISBN" — there isn't one. Point at
   <https://zenodo.org/communities/principia-orthogona>.
3. The 3 files labelled "Series ISBN" are the highest priority regardless of volume:
   the label is false even where the number is right.
4. Update this ledger in the same session, per rule 6.

---

# OPEN TODO: `book6/on-publication.html` — remaining content review (opened 2026-08-17)

Three defects fixed 2026-08-17; the rest of the page is unreviewed. Fixed:

- **§7 pull-quote asserted that a wrong argument will not compile.** False, and refuted
  by the corpus's own work: `AXLE/CatGT/CatGT_Main.lean` documents four theorems that
  compiled while being vacuously true (`: True`, `: 1 = 1`, `: ∃ shape, True`) and were
  replaced. Compilation certifies validity *given the statement*; it cannot certify that
  the statement says what was meant. Rewritten to state the three-way distinction —
  kernel-checked, sorry-free, non-vacuous — which is the same split the theorem registry
  at `sluing.github.io/neuro/SBM/1080.html` already publishes as Tier 1 / 2 / 3.
- **§6 scored its own rigor** ("a strictly higher standard than single-blind review"),
  against house rule 3. Now scoped: stronger for the formalised fragment, merely open for
  the cross-domain synthesis, laminin work and therapeutic corridors, which are stated as
  remaining unrefereed.
- **§5 listed Einstein and Shannon as precedents for self-publication.** Both were
  journal-published — *Annalen der Physik* 1905 and the *Bell System Technical Journal*
  1948 — and Ramanujan published conventionally besides circulating notebooks. Only
  Perelman withheld outright. Corrected in place per rule 5 rather than cut, with the
  narrower shared claim stated explicitly.

- **§2 claimed `polylaminin` as this corpus's coinage.** It is not. Polylaminin is
  Tatiana Coelho-Sampaio's (UFRJ), published in *The FASEB Journal* in 2010 — Menezes et
  al., *"Polylaminin, a polymeric form of laminin, promotes regeneration after spinal cord
  injury"*, PMID 20643907 — sixteen years before this page listed it among terms that "do
  not appear in prior literature". Corrected with explicit attribution: the contact-geometric
  reading is new, the molecule and its name are not. **Check the rest of the corpus for the
  same pattern** — any term listed as a neologism that belongs to another researcher is the
  most damaging class of error on these pages, because it is both false and discourteous.
- **§6 wrongly listed the laminin work as unrefereed** (my error, introduced earlier the
  same day while fixing rule-3 self-scoring). The polylaminin science is published and
  regulator-reviewed: FASEB J 2010, Front. Vet. Sci. 2025 (doi:10.3389/fvets.2025.1592687),
  and ANVISA authorised a Phase I trial in January 2026. Only the dm³ reading laid over it
  is unrefereed. **Rule for this corpus: never describe externally published collaborator
  or third-party science as unrefereed in order to sound modest about our own layer.**
  Scope the modesty to the layer we actually added.


# OPEN DEFECT: polilaminina claims across the corpus (opened + partly fixed 2026-08-17)

**A preprint result was labelled as ANVISA trial data.** `vol3-minibeast.html` and
`book3/index.html` both read *"ANVISA Phase I clinical data (January 2026): 6 of 8
patients…"*. That conflates two different things: the 6-of-8 figure is a **2024 pre-trial
pilot**, reported as a medRxiv preprint (10.1101/2024.02.19.24301010) and **not
peer-reviewed**; ANVISA's Phase I is a **5-patient** safety trial authorised January 2026
that has **not reported**. Both fixed, tagged `[PRELIMINARY — not peer-reviewed]`.

**Status, checked 2026-08-17.** Polilaminina is **not registered or approved** in Brazil.
It is simultaneously reaching patients: 33 authorised under ANVISA's *Programa de Uso
Compassivo* (sponsor Cristália donating doses) against 59 judicial decisions as of
11 March 2026, later reported at 38; HUOP Paraná among the administering hospitals.
**No law or regulation was changed** — ANVISA says so explicitly. Compassionate use is
the pathway that exists *because* a product is unapproved; citing it as evidence of
approval inverts its meaning.

**Precedent to keep straight.** Congress *did* once pass such a law, for a different
compound: Lei 13.269/2016 authorised fosfoetanolamina sintética without ANVISA
registration. AMB challenged it (ADI 5501); the STF suspended it 19 May 2016 and later
ruled it unconstitutional — safety review is ANVISA's technical competence, not
Congress's by abstract statute — and trials found no benefit. There is no such law for
polilaminina. Do not let the two stories merge.

**Rule.** Any clinical claim on these pages carries its evidence tier in the sentence:
peer-reviewed / preprint / trial-authorised / compassionate-use. A regulatory verb
("approved", "authorised", "registered") without its object is a defect.

## Still to review on that page

1. **§2's central claim is untested.** "The words exist because the framework required
   them" is asserted, not shown. One worked example — a term that cannot be expressed in
   existing vocabulary without a paragraph of circumlocution — would carry the section.
   Without it the paragraph asks the reader for exactly the trust it says reviewers
   withhold.
2. **§4's "five and thirty years" is unsourced.** Either cite the bibliometrics or mark
   it `[MODEL]` per rule 2.
3. **§5 still leads with Perelman.** Accurate, but it is the comparison most likely to
   make a hostile reader file the corpus under the failure mode the author already guards
   against. Worth deciding deliberately, not by inertia.
4. **§3 lists scope but not competence.** It says no reviewer pool spans the material; it
   does not say who *has* checked which parts. A short "what has been externally checked,
   and by whom or by what" line would answer the obvious question.

# OPEN TODO: maths and remaining defects, book6 (opened 2026-08-17)

Not started — logged so it is scoped rather than swept.

- **4 dead links remain in `book6/`** after the 2026-08-17 sweep (9 were repaired: 3
  wrong-path cross-volume links to `book7/`, 1 rename, 2 planned-chapter navs disabled,
  3 misc). The 4 survivors point at files that exist nowhere on disk and need a decision,
  not a redirect: `heat-equation/heat_equation_monograph.pdf`
  (`ch-elliptic-poisson-foundations.html`), `../../AXLE/HeatEquation_Step1.lean` and
  `../../AXLE/HelixToyModel.lean` (`index.html`),
  `../applications/stjohns-meco/aula-index.html` (`wp63-chladni-realia-build.html`).
- **`ch04-why-proofs.html` and `ch05-self-organization.html` are badged Planned in the
  index but were linked from chapter navs** — now rendered as disabled spans marked
  "planned". If either gets written, restore the anchors.
- The false commutator lemma ledger above is unaffected by any of this work; nothing in
  this session touched an operator-order argument.

---

# OPEN: terminology audit — two more claimed coinages that are not (2026-08-18)

Ran the sweep flagged after the polylaminin finding. Only `book6/on-publication.html` §2
makes an explicit "these terms do not appear in prior literature" claim, so the exposure is
narrower than feared — but the list was wrong twice more.

- **`knacci` is not a coinage.** *k-nacci* is standing terminology in the
  generalised-Fibonacci literature — *"On some combinations of k-nacci numbers"* (Chaos,
  Solitons & Fractals, 2016), *"The k-nacci triangle and applications"* (Cogent
  Mathematics, 2017). **Open question for the author:** is the object here the same as
  theirs? If yes, adopt their notation and cite them. If no, the difference has to be
  stated, because a reader in that field will otherwise assume the literature was missed.
- **`dm³` collides with SI.** dm³ is the cubic decimetre — a litre. Every chemist and
  physicist reads it that way first. Not fatal, but it is the author's job to
  disambiguate on first use in each document, not the reader's to infer.
- `Principia Orthogona` and the `η weighting` stand.

§2 rewritten to disclose both rather than assert novelty. Note the irony the section now
carries deliberately: §2's argument is that referees *wrongly* suspect invented jargon —
but a referee who knows the k-nacci literature would have been right, and the page cannot
make that argument while committing the error.

**Rule.** Before any term is listed as novel, search it. A claimed coinage that turns out
to be someone else's published term costs more credibility than the term ever bought.

---

# OPEN TODO: the theorem registry undercounts the repo (opened 2026-08-18)

The published registry at `sluing.github.io/neuro/SBM/1080.html` states three tiers:
**1,165** statements formally written (Tier 3), **1,004** sorry-free in source (Tier 2),
**30** individually kernel-audited (Tier 1), with 62 axiom declarations and 383 sorry
tokens disclosed corpus-wide.

A raw scan of `~/Desktop/AXLE` on 2026-08-17 found **122 `.lean` files** (excluding
`.lake/`) carrying **~1,340 `theorem` / `lemma` declarations** — roughly **175 more than
Tier 3 claims**.

**Do not "fix" the registry to 1,340.** The discrepancy has at least four innocent
explanations and they must be separated before any number moves:

1. **Duplicates.** `AutophagyDm3.lean` and `AutophagyDm3_v2.lean`, `AXLE.lean` /
   `AXLE_v5_1.lean` / `AXLE_v6.lean`, `Main_v6.lean` (51 decls, identical count to
   `AXLE_v6.lean`) — versioned copies of the same material almost certainly double-count.
2. **Comment and docstring hits.** The scan matched line-initial `theorem` / `lemma`; any
   inside `/-! -/` blocks or summary tables inflate it.
3. **Scope.** The registry may deliberately cover only the published corpus, excluding
   scratch directories, `geometry-backup-jul5/`, `cajulina/`, `orthogenesis/` etc.
4. **Placeholders.** `theorem X : True := by trivial` counts as a declaration and is
   exactly the class already documented as corrected in `CatGT_Main.lean`. These should
   **not** appear in Tier 3 at all.

**The task is reconciliation, not recounting.** Produce a per-file table — path, decl
count, sorry count, axiom count, whether it is a version-duplicate of another file — and
diff it against the registry's own basis. If Tier 3 is genuinely low, raise it *with* the
file list that justifies it. If the scan was loose, record the correct methodology in the
registry so the next scan agrees.

The registry's credibility comes from being conservative and auditable. A number that
moved once without a published basis is worth less than a smaller number that never has.

---

# OPEN — Book IV carries unallocated ISBNs on products offered for sale (2026-08-18)

Book IV was checked on the assumption it would be clean. Links are clean — **zero dead links
across all 66 files**, no links to non-canonical copies, and no stranded-anchor defect (the two
files the detector flags have a generic `a` rule, so their nav anchors are styled). `index.html`
is a deliberate redirect stub to `contents.html`, which is why the naive per-book orphan audit
once reported "50 orphans of 51".

The ISBNs are not clean. **Nothing was edited** — see the verification gap below.

## Storefront: three products priced and linked to Gumroad under numbers not allocated to them

Identical blocks in `book4/ch02.html` and `book4/ch10.html`:

| product as advertised | ISBN shown | price | status in the table above |
|---|---|---|---|
| Operator Framework — "Series foundation" | 979-8-9954416-2-5 | **$47 · Buy on Gumroad** | **unallocated reserve — no group, no format** |
| Applications Across Domains — "g₃₃ = 33" | 979-8-9954416-4-9 | **$47 · Buy on Gumroad** | G5 **Hardback** — INCOMPLETE, HOLD |
| Complete Completeness | 979-8-9954416-5-6 | **$47 · Buy on Gumroad** | **unallocated reserve** |

The rule above is written for footers: *"A print ISBN in a web footer advertises a product that
does not exist."* This is not a footer. It is a price and a buy button, and two of the three
numbers have no group and no format assigned at all.

## Citations and footers

- `ch02.html`, `ch10.html`: *"Principia Orthogona, Vol. I … ISBN 979-8-9954416-2-5"* — Vol I has
  no allocation, and 2-5 is unallocated reserve.
- `ch02.html`, `ch10.html`: *"Principia Orthogona, Vol. II … ISBN 979-8-9954416-4-9"* — that
  number is G5 Hardback, not Vol II.
- `hub.html`: *"ISBN 979-8-9954416-5-6 (G5 eBook · Complete Completeness)"* — G5 eBook is
  **1-8**. So this is an unallocated number *labelled as a different, allocated format*.
- Vol IV footers carry **979-8-9954416-8-7** in four files (`ch-hawking.html`,
  `ch15-complex-turn.html`, `chIV-axioms.html`, `chIV-field.html`) — unallocated reserve, and
  Vol IV has no allocation of its own.
- `chE-gtct.html` carries Book 3's **979-8-9954416-6-3** on a GTCT page.

## Why nothing was edited

**The canonical registry is not reachable.** This file names
`~/Desktop/MATHS for life/isbn_metadata.json` as *"the only copy that carries `bowker_status`,
so it is the only copy that can tell you whether a number is registered or merely reserved"* —
and there is no `MATHS for life` folder in the mounted Desktop, and no `isbn*metadata*` or
`*bowker*` file anywhere under the mount. So the only available source is the table at the top
of this file, which this file itself records as having **drifted out of sync once already**,
putting an unallocated reserve number into 87 book6 footers.

Correcting a footer on that basis would be reasonable. Removing an ISBN from a page that
prices a product and links to Gumroad is not something to do from a source known to have been
wrong before. **This needs the registry, or the author.** If the numbers are right and the
table is stale, the table is what should change.

# ISBN registry read at last — Book IV corrected, and the registry itself has two bugs (2026-08-18)

**The path in this file is wrong.** The registry is not at `~/Desktop/MATHS for life/`. It is at
**`~/Documents/Claude/Projects/MATHS for life/isbn_metadata.json`**, alongside
`Bowker_ISBN_Registration_Guide.md` and `isbn_registration.py`. Correct the path above before
the next session repeats the hunt.

## The registry confirms every Book IV finding

Verbatim `action` fields for the numbers Book IV was using:

| ISBN | bowker_status | registry says it is for |
|---|---|---|
| 979-8-9954416-2-5 | INCOMPLETE — HOLD | *"Reserve for Vol VI or 40-language edition."* |
| 979-8-9954416-4-9 | INCOMPLETE — HOLD | G5 **Hardback**, print — *"Activate on print."* 666 pp max |
| 979-8-9954416-5-6 | INCOMPLETE — HOLD | *"Reserve for first major translation or Vol II."* |
| 979-8-9954416-8-7 | INCOMPLETE — HOLD | *"Free."* — assigned to nothing |
| 979-8-9954416-6-3 | INCOMPLETE — **register now** | Book 3 · Mini-Beast · eBook PDF, $19.99 |
| 979-8-9954416-0-1 | **REGISTERED** | G5 Paperback — *"Print. NOT for sale until further notice."* |

And the file's own header: *"Only complete/register an ISBN when the product is live and being
distributed. Everything marked HOLD stays INCOMPLETE in Bowker until needed."*

**Fixed: 10 ISBN lines removed** from citations and footers across nine files —
`ch02`, `ch10` (Vol I cited with 2-5, Vol II with 4-9), `hub` (5-6 labelled "G5 eBook" when G5
eBook is 1-8), `chTau-tartaruga` (5-6), `chE-gtct` (Book 3's 6-3 on a GTCT page), and
`ch-hawking`, `ch15-complex-turn`, `chIV-axioms`, `chIV-field` (8-7, assigned to nothing).
Per the rule above, a volume without its own registered ISBN gets **no ISBN line**, not a
borrowed one. *(`chIV-field.html` has a stray `</div>` — pre-existing, confirmed in `HEAD`.)*

## Two bugs in the registry itself — fix upstream or this recurs

1. **`979-8-9954416-1-8` carries `format_note: "All-encompassing eBook. Default ISBN for any
   volume without its own."`** This is the withdrawn fallback-ISBN instruction, still live in
   the canonical source. It is almost certainly **the upstream origin of the borrowed-ISBN
   defect** — the one that put an unallocated number into 87 book6 footers and 19 other files.
   Every downstream correction made in this repo is undone the moment someone consults the
   registry and follows that note. It should be deleted there, not just contradicted here.
2. **`979-8-9954416-6-3` carries `distribution: "Gumroad · Zenodo doi:10.5281/zenodo.19117400"`.**
   That DOI is Vol I's v1 founding deposit, established on 2026-08-02; Book 3 has no standalone
   deposit at all. The registry is asserting a Zenodo record for Book 3 that is a different
   volume's.

## OPEN — the storefront

`book4/ch02.html` and `book4/ch10.html` still price three products at **$47 with Buy on
Gumroad** under **2-5**, **4-9** and **5-6** — all three `INCOMPLETE — HOLD` in Bowker, i.e.
not registered to anything, and 4-9 is a print ISBN whose own note reads *"Activate on print"*
against a registry header saying paper books are not for sale.

Untouched deliberately. If those products are genuinely for sale the fix is to **register
ISBNs for them**, not to strip the numbers off the page; if they are not for sale, the price
and the buy button are the problem, not the ISBN. Either way it is a commercial decision.


---

Dated narrative for closed defects and audits moved to `docs/audit-log.md`
on 2026-08-21. Nothing was changed, only relocated. Open items stayed here.

## Session 2026-08-25
- WP-Preemie added to AXLE/AULA/day-by-day/ — dm3 prematurity mapping, four bio domains
- Anchor: AutophagyDm3_v2.lean, 24 theorems, no sorry, no True conclusions
- Open Lean: [LEAN-NEEDED-1] surfactant CRNT deficiency, [LEAN-NEEDED-2] thymic selection
- to_delete/ policy: errors are evidence, nothing deleted directly

---

# RULE (2026-08-27): every declaration named in prose must resolve, at the path cited

Three findings in one week had the same shape: a claim about Lean written from
intention rather than from the artifact.

- `vol2-toymodel.html` carried Lean badges naming declarations absent from the repo.
- `tools/verify-dm3/probe_dm3.lean` named thirteen `ToyModel` declarations without
  importing the module.
- `PrincipiaOrthogona_v2/VolumeTwo.lean` was in no lakefile target, so six
  declaration names survived into a published paper without ever being elaborated.

Each got a local repair. None produced a check, because the rule that covers all
three was nowhere written down. It is this:

**Before a declaration name appears in prose — an HTML badge, a paper, a README, a
probe file, a commit message — resolve it. Open the file at the path cited and see
the name. If the file is not in a lakefile target, say so beside the claim, because
an unelaborated declaration is a name, not a theorem.**

Corollaries, each of which has already cost a correction:

- **Compilation is not verification.** `sorry` is a warning. Run `#print axioms`.
- **`#print axioms` emits info, not an error.** A `sorryAx` scrolls past inside a
  build that reports success. The gate is `tools/axiom_gate.py`, not the build.
- **Sorry-free is not proved.** `theorem X : True := by trivial` is sorry-free and
  vacuous; a biconditional proved from assumptions on both sides is sorry-free and
  empty. Both have been found in this corpus and are recorded in `docs/audit-log.md`.
- **A hand run proves the file on the day it is run and nothing afterwards.**
  Declare the target, or the next regression is silent.

## What NOT to do

Do not repair the individual page and move on. That is what produced three
instances of one defect. Repair the page, then ask what check would have caught it,
and write that check into `tools/`.

---

# RULE (2026-08-27): a published number must be produced by a tool in `tools/`

A number on a public page is a claim. If no script in `tools/` regenerates it, a
reader cannot check it and neither can the next session — and the number drifts
from whatever it once described without anything failing.

**Every corpus-wide figure that appears on a public page must name the tool that
computes it and the date it was last run.** If the tool does not exist, write it
before the number ships. Existing instances:

| figure | tool |
|---|---|
| theorem / declaration counts | `tools/theorem_census.py` |
| kernel-checked declaration counts | `tools/verify-*/run.sh` + `tools/axiom_gate.py` |
| probe / gate / README count agreement | `tools/probe_consistency.py` |
| word counts | `tools/wordcount_scan.py` |
| the corpus root set itself | `tools/corpus_roots.txt` |

## What counts as the corpus (added 2026-08-27)

A corpus-wide number is undefined until the root set is. This was the live defect:
`theorem_census.py` was first run over `~/Desktop/geometry ~/Desktop/AXLE` and its
output reported as a corpus census. Two of eleven repositories is not the corpus,
and the missing nine are why that run found 32 `axiom` declarations against the
registry's 62.

Scanning wider is not the fix either. `~/Downloads` holds `files (27)`,
`files (28)`, `files (39)` — repeated copies of the same declarations.
`~/Desktop/geometry-backup-jul5` and `~/Desktop/files 4.12.2026` are second
checkouts of `TOTOGT/geometry` and `TOTOGT/AXLE`. A scan of everything on disk is
not a wider net, it is a broken one: it counts the same theorem four times and
calls the result growth.

**The corpus is one checkout per distinct git remote, git-tracked `.lean` files
only.** The root set lives in `tools/corpus_roots.txt`, with every excluded path
listed there beside the reason it is excluded. Untracked files are drafts — in
`geometry` alone, `_to_delete/`, `V4,` and `vol2-v5/` hold 19 declarations that no
published number may include. Tracked files under `.lake/` or `lake-packages/` are
vendored dependencies and are excluded too: they are someone else's theorems.

    python3 tools/theorem_census.py --corpus --tracked

Run of 2026-08-27 — 11 repositories, 254 files:

| | raw | grouped |
|---|---|---|
| declarations written | 2628 | 1856 |
| sorry-free | 2365 | 1676 |
| admitted (`sorry` in body) | 263 | 180 |

53 `axiom` declarations. Read down one column; a raw figure and a grouped figure
are not comparable, and the tool now prints them as two columns for that reason.

**None of these six numbers is publishable yet, and the reason is written here so
the next session does not publish one anyway.** Grouping keys on the basename with
any `_vN` suffix stripped, discarding the directory, so it collapses files that
merely share a name in different directories — `AXLE.lean` appears four times in
one group. The grouped column is therefore a lower bound, not a count. The raw
column double-counts genuine version siblings (`AXLE.lean`, `AXLE_v5_1.lean`,
`AXLE_v6.lean`, `AXLE_V8.lean` are four tracked files in one repository). The true
figure is bracketed by 1856 and 2628 and is not yet known.

The registry publishes 1165 / 1004 / 30. That gap against 2628 is the reconciliation
opened in the 2026-08-18 TODO, still open. One lead: counting tracked files
*including* those under `.lake/` raises the axiom count from 53 to 61, against the
registry's 62 — which suggests the registry's scan reached into vendored trees this
rule excludes. Confirm that before moving any number.

The counting vocabulary is not interchangeable, and the three words below have been
used as synonyms on public pages when they name three different quantities:

- **written** — a `theorem` or `lemma` declaration exists. Says nothing about proof.
- **sorry-free** — no `sorry` in the proof body. Still says nothing about content:
  see the vacuity findings above.
- **kernel-audited** — `#print axioms` run on that named declaration, reporting
  only `[propext, Classical.choice, Quot.sound]`. This is the only one of the three
  that is evidence, and it is always the smallest number.

"Proved" belongs to the third column only. A page that puts a first-column number
under the word "Proved" is overclaiming by two full steps, whatever the arithmetic.

## What NOT to do

Do not raise a published number to match a fresh scan. The task is reconciliation:
produce the per-file basis (`tools/theorem_census.py --table`), diff it against the
number's stated basis, and move the number only with the file list that justifies
it. A number that moved once without a published basis is worth less than a smaller
number that never has.

Do not pass a directory tree to `theorem_census.py` and report the result as a
corpus figure. Without `--corpus --tracked` it counts whatever you point it at,
second checkouts and `~/Downloads` copies included. If a root belongs in the
corpus, add it to `tools/corpus_roots.txt` with its remote — and re-run the census
and diff before shipping, because adding a root changes every published total.

Do not quote a raw figure and a grouped figure in the same sentence. Before
2026-08-27 this tool printed "after grouping: 1009" four lines above "sorry-free:
1493" — a grouped total above a raw one, a pair that cannot both describe the same
corpus, and 1493 was on its way to a public page.

Do not treat "reach more places" as the fix for a number that is too low. The
registry undercounts and the disk overcounts; the work in between is naming the
corpus, not widening the scan.

---

# THE REPO MAP AND THE VERIFICATION LEDGER (mapped 2026-08-27)

Read this before counting anything, citing a declaration, or quoting a total.
The corpus is **thirteen repositories**, not one, and the same file exists in
several of them at different vintages. Three different CatGT counts were given in
a single session — 227, 36, 19 — purely by reading three different copies. The
repo of record decides the number.

## Repositories, by reference count across the corpus

| repo | .lean | decls | sorry-free | admitted | axiom decls | CI | Tier 1 audited |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| `TOTOGT/AXLE` | 127 | 1407 | 1235 | 172 | 32 | **none** | 19 |
| `TOTOGT/geometry` | 38 | 306 | 301 | 5 | 0 | uncommitted | 32 |
| `TOTOGT/vol1-proofs` | 7 | 140 | 140 | 0 | 0 | **gated + vacuity** | **82** |
| `TOTOGT/GTCT` | 32 | 148 | 122 | 26 | 20 | badge, ungated | 24 |
| `TOTOGT/io` | 3 | 19 | 19 | 0 | 0 | ungated | 14 |
| `TOTOGT/dnls` | 4 | 152 | 109 | 43 | 0 | none | 0 |
| `TOTOGT/3M` | 6 | 58 | 54 | 4 | 0 | none | 0 |
| `TOTOGT/book3-starter` | 3 | 4 | 4 | 0 | 0 | none | 0 |
| `TOTOGT/DM3-lab` | — | — | — | — | — | ? | ? |
| `TOTOGT/maths`, `Collatz`, `Atratores`, `reporting-layer` | — | — | — | — | — | ? | ? |

Counts from `tools/theorem_census.py`, 2026-08-27. `DM3-lab` is the third
most-referenced repo in the corpus (318 links) and has never been measured.

## Tier 1 — kernel-audited: 173

| source | n | evidence |
| --- | ---: | --- |
| `vol1-proofs/tools/axioms.txt` | **82** | PrincipiaVol1 58 + AutophagyDm3_v2 24; run 2026-08-25; 76 on the standard trio, 2 on `[propext, Quot.sound]`, 3 on `[propext]` alone; zero `sorryAx` |
| `geometry/tools/verify-dm3` + `verify-book8` | 32 | live `axioms.txt` |
| `GTCT/.github/badges/gctc-status.json` | 24 | CI badge, "24/24 proved", written 2026-08-01 |
| `AXLE/tools/verify-vol2` | 19 | live `axioms.txt` |
| `io/.github/workflows/verify-proofs.yml` | 16 | CatGT 9 + Theorem53/Zeolite 7, every push |

Not 51, and not 171: the io workflow probes 16, not 14 — `foldMap_not_odd` and
`exists_order_dependent` sit in a step that a first reading missed. A number quoted from one repo's reports is a fifth of the real figure.

## `vol1-proofs` is the reference implementation — do not rebuild it

`vol1-proofs/tools/run.sh` runs five stages: **gate self-test → build → probe →
axiom gate → vacuity scan**, the last with fixtures that must fire ("a silent
detector is worse than none"). It has `axiom_gate.py`, `test_axiom_gate.py`,
`counts.py`, `probe.lean` (82 declarations) and `vacuity.lean`. Its header states
the method better than anything else in the corpus:

> Neither `lake build` exiting 0 nor grepping for "sorry" can decide anything —
> a theorem can be sorry-free and vacuous. Only `#print axioms` sees both.

Before writing a verification tool anywhere in this corpus, read that directory.
`AXLE/tools/verify-core/` was built on 2026-08-27 to probe PrincipiaVol1 and
AutophagyDm3_v2 — which `vol1-proofs` had already been doing, gated, since the
25th. That is duplicated work, and the duplicate is the weaker one: it has no
vacuity stage.

## The gap the ledger has, in every repo but one

`#print axioms` emits **info, not an error**, and `lake build` succeeds whether or
not a proof is admitted. So printing axioms is not gating on them:

- `GTCT`: the axiom step ends `|| true`. The badge would go red because it parses
  `registry.csv`, but the job itself cannot fail on `sorryAx`.
- `io`: `lake env lean` exits 0 regardless, and nothing parses the output.
- `AXLE`: no CI at all, on any branch.
- `geometry`: `verify-proofs.yml` still uncommitted — the PAT lacks `workflow` scope.
- `vol1-proofs`: **gates correctly**, and additionally scans for vacuity.

Only the last one would actually fail if a proof were replaced by `sorry` tomorrow.

## Claims with no repo behind them

- **Jacobian.** `geometry/book7/jacobian-verification.html` carries the axiom line
  for `not_injective_despite_constant_jacobian` pasted into the page. No `.lean`
  file exists in any repo. It cannot be re-run.
- **Galois.** `AXLE/chGal-galois.html` carries
  `#print axioms Theorem_Galois -- expect sorryAx: this theorem is OPEN`.
  Correctly disclosed, contributes nothing, needs no repair.

## What NOT to do

Do not quote a corpus total from whichever repo happens to be open. Do not build a
verification tool before reading `vol1-proofs/tools/`. Do not count a file without
checking which repo holds its canonical copy — `Projects/io` is a stale non-git
working copy of `TOTOGT/io`, and `AXLE/CatGT/` holds six `Main_v*` versions that
do not exist in the io repo at all.

---

# RULE (2026-08-28): a mismatch is a defect only where something is distributed

The corpus is drafts. Everything in it is provisional until the verification machine
is finished, preprints are self-published and identified by their Zenodo DOI, and an
ISBN is only needed for a product that is actually being distributed. A draft that
disagrees with a registry, a plan, or another draft is not broken. It is a draft.

This rule exists because comparing provisional content against a canonical table and
reporting every difference as an error produces confident, well-evidenced findings
that are wrong. Three in one session:

- **"Complete Series — G¹ through G⁵ · Five volumes"** was read as an overclaim
  against a nine-volume series and renamed. It is the real title of a real 528-page
  bound product whose own title page reads *Principia Orthogona G¹–G⁵ · Complete
  Completeness Series*. The five-volume printed series and the nine-volume web series
  are two different objects; both counts are correct about their own object. Reverted.
- **The volume count** more generally. "Seven-volume", "five volumes" and "nine
  volumes" appear across the corpus and at least two of them name something specific.
  Before changing a count, establish what it counts.
- **ISBNs on a draft title page.** `Principia_Orthogona_Complete_v8.pdf` prints
  numbers the registry holds for other products. It is a draft; the numbers are not
  final; there is nothing to reconcile.

The same shape appears in the corpus's own history: a number that had been counted
was later declared wrong by a pass that believed it was doing a service.

## The test, before reporting any number or name as a defect

1. **Is it distributed?** Per `isbn_metadata.json`, exactly one product is:
   Book 3's eBook, `979-8-9954416-6-3`. Everything else is HOLD or draft.
2. **What does the number count?** Printed series, web series, framework, G-series
   and repository are five different denominators here.
3. **Is there a real artifact behind it?** Look for the PDF, the ISBN entry, the
   product page — before concluding a claim has nothing behind it.

## What NOT to do

Do not "fix" a draft into agreement with a plan. Do not chase ISBN registration,
listing copy, or volume counts — they are provisional by design. Work that improves
the verification machine is the priority; work that tidies drafts is not.

---

# OPEN — the machine: four of five checkers print without gating (2026-08-28)

This is the load-bearing item. `#print axioms` emits **info**, not an error, and
`lake build` exits 0 on an admitted proof, so printing axioms is not gating on them.

| repo | state | would a new `sorryAx` fail it? |
| --- | --- | --- |
| `vol1-proofs` | five stages: gate self-test, build, probe, axiom gate, vacuity scan with fixtures that must fire | **yes** |
| `GTCT` | probe list generated from source; axiom step ends `\|\| true` | no — the badge reddens, the job does not |
| `io` | `lake env lean` prints; nothing parses the output | no |
| `geometry` | gate written and tested; workflow file uncommitted (PAT lacks `workflow` scope) | not running |
| `AXLE` | gates exist as local scripts; no CI on any branch | no |

The repair is identical in each: parse the probe output, exit non-zero on `sorryAx`
or on any axiom outside the allowlist. `tools/axiom_gate.py` already does this and
has a self-test. This is a copy, not a design problem.

**A check that runs and cannot fail is worse than no check**, because it produces a
green mark a reader is entitled to believe.

---

# OPEN — `DM3-lab`: measured 2026-08-28. Real Lean, early Lean

Measured by cloning the repository and running `tools/theorem_census.py` on it:

| | raw | grouped |
| --- | ---: | ---: |
| `.lean` files | 49 | |
| declarations | 313 | 237 |
| sorry-free | 285 | 225 |
| admitted | 28 | 12 |
| **axiom declarations** | **134** | |

**Two things are true at once, and both matter.** The repository is early work — a
first pass, not a finished verification, and it should not be described as verified.
But the corpus's description of it is wrong in the other direction, and that is the
error worth fixing first, because it is on a reader-facing page.

**The description is wrong.** `book1/vol1-mathematics.html` lists Kakeya and the Tribonacci
growth rate among "complete mathematical arguments deposited in DM3-lab **without**
Lean 4 verification … proof sketches, not proof claims." Both have real Lean:

- `NS/Dm3Kakeya.lean` proves `finite_kakeya_thickened_positive_measure`, and its own
  header calls it *"First formally_verified pillar … a complete, zero-sorry result."*
- `Tribonacci.lean` carries `charpoly_C_eq_tribPoly`, `recurrence_holds`, `eta_root`,
  `eta_gt_one`, `eta_pos`, `tribonacci_growth_rate`.

That sentence needs the author's revision. It is the rarer failure: a page giving
away work that was done.

**The real qualifier is the axiom load, not absence of Lean.** 134 `axiom`
declarations — more than the rest of the measured corpus combined (52) — concentrated
in `NS/`: `Dm3Hodge` 18, `continuousDm3` 17, `Dm3Poincarev1.1` 16, `Dm3YangMills` 14,
`Dm3RH` 10, `Dm3Goldbach` + `Dm3GoldbachDeepened` 20. `Dm3Kakeya.lean` itself declares
`Kakeya_K`, `Kakeya_dirs`, `Kakeya_measurable`, `C_Kakeya`/`K_Kakeya`/`F_Kakeya`/
`U_Kakeya` and `Kakeya_preserves_contact`.

So "sorry-free" here means *sorry-free on top of declared assumptions*, which is a
different claim from the rest of the corpus and must not be summed with it. The
accurate description is neither "sketches, not proof claims" nor "verified": it is
**a first pass in Lean, resting on 134 declared axioms, never probed and never
version-pinned.** That sentence is defensible in both directions.
`#print axioms` settles it per declaration in one run, and `tools/axiom_gate.py`
refuses anything outside `[propext, Classical.choice, Quot.sound]` — so a probe would
immediately separate the theorems that stand alone from those resting on `NS/`'s
axioms. Nobody has run it.

**Blockers before it can be probed.** No `lean-toolchain`, so nothing is version-
pinned or reproducible. No `.github/workflows`. And `lakefile.toml` declares
`roots = ["Finite"]` against four case-differing `Finite.lean` copies — the same
case-sensitivity defect AXLE's lakefile header already records, invisible on macOS
and fatal on a Linux runner.

Order: pin a toolchain, see what builds, probe what builds, and report DM3-lab's
count in its own row — never folded into a corpus total, because its axiom base is
not the corpus's axiom base.

---

# OPEN — the audit tools run only by hand (2026-08-28)

`tools/theorem_census.py`, `tools/decl_resolve.py` and `tools/probe_consistency.py`
each found a real defect on their first run, and none of them is wired into any
pipeline. A citation that does not resolve, a count that has drifted, or a Lean file
outside every build target is currently found when someone thinks to look.

The sequence, in order of value: gate the four ungated checkers, measure `DM3-lab`,
then wire the census and the resolver in so a broken citation fails a build.

---

# PARTLY CLOSED — the theorem registry undercounts the repo (opened 2026-08-18)

Reconciliation done 2026-08-27/28. `tools/theorem_census.py` produces the per-file
basis the original entry asked for: comments stripped before matching, `example`
excluded, each `sorry` attributed to its own declaration, version-suffixed copies
grouped. `scripts/build_theorem_registry.py` now delegates to it instead of carrying
its own regex — the old one matched only line-initial `^(theorem|lemma)` and did not
strip comments, two errors in opposite directions, which is why its totals never
reconciled. Its publication date was also a hardcoded literal and is now `today()`.

Still open: the registry's Tier 1 reads from live `axioms.txt` files only, so it
misses runs recorded elsewhere — Volume I's 58, GTCT's CI badge, io's CI. Counted by
hand the total is **173**; the tool says less until it learns to read those sources.

---

# REFRAMED — Book IV and "unallocated ISBNs" (opened 2026-08-18, reframed 2026-08-28)

The original entry treated HOLD-status ISBNs appearing on pages as a defect on
products offered for sale. Under the rule above that is mostly not a defect: those
pages are self-published preprints carrying a Zenodo DOI, and the ISBNs are
provisional.

What survives, and it is one line: `isbn_metadata.json` marks
`979-8-9954416-6-3` (Book 3 eBook) **"INCOMPLETE — ACTION REQUIRED · Register this
now. Only actively distributed product."** That is the one place the distribution
test is met. It is an allocation decision for the author, not a repair for a tool.

---

# RULE (2026-08-28): never report absence from a single search

A failed search is evidence about the search. It is not evidence about the corpus.

The recurring failure in this project is not a session inventing something that does
not exist. It is a session declaring that something **does not exist** when it does,
and presenting the deletion or the correction as a service. That has cost real work:
a counted figure was declared wrong and replaced; a real product title was renamed as
an overclaim; a repository full of Lean was described as holding only sketches.

**Never write "there is no X", "X does not exist anywhere", or "this claim has
nothing behind it" on the strength of one search.** Write what is actually known:
*"I did not find X by <method>."* Then, before it goes in a file or a message, look
again by a differently-shaped method.

## Blind spots that produced false absences here, all in one session

| method | what it missed |
| --- | --- |
| `find -name 'AXLE_v8*'` | `AXLE_V8.lean` — case-sensitive glob. AXLE's own lakefile header already records this defect (`roots = ["Finite"]` vs `finite.lean`). |
| glob `*.lean` | `main/axle_v8.1` — Lean source with a version number where its extension should be. |
| `t.lstrip('./')` | `../impa-portal.html` became `impa-portal.html`. `lstrip` strips a character set, not a prefix. Produced 69 phantom dead links. |
| treating `/geometry/…` as a relative path | 55 phantom dead links across the root index and the student portal. Absolute paths resolve on the live site; `tools/audit.py` skips them for exactly this reason. |
| reading a page's description of a repository | `DM3-lab` — described in the corpus as sketches "without Lean 4 verification"; it holds 313 declarations and a `finite_kakeya_thickened_positive_measure` whose own header calls it a complete zero-sorry result. |
| reading whichever copy was open | CatGT counted at 227, then 36, then 19 — three checkouts of the same material. Only the one with the git remote is the number. |

## A second mechanism: over-reading a correct note past its scope

The table above is about failed searches. There is a quieter variant that needs no
search at all: **an accurate internal note is read as covering more than it says.**

On 2026-08-28 the `chLambda-polylaminin.html` line *"ANVISA Phase 1 approved 2025;
Phase 2 trials scheduled 2026"* was reported as having "nothing behind it" for the
Phase 2 clause. The basis given was this file's own polilaminina entry (2026-08-17),
which states: *"ANVISA's Phase I is a 5-patient safety trial authorised January 2026
that has not reported."* That sentence is correct and it is **only about Phase I**.
It was silently extended to Phase II, and the extension was attributed to the record.

Phase 2 is real: ANVISA's own release says advancing to Phases 2 and 3 depends on the
Phase 1 results, and Cristália has discussed a Phase 2 publicly with approval projected
within roughly two years. The accurate correction was narrower than the one offered —
"planned and conditional, no published start date", not "unsupported".

**A note is evidence for what it asserts and for nothing adjacent.** Before citing one
against a claim, check that its scope covers the claim. If it does not, the honest
statement is *"the record is silent on this"* — which is a reason to search, not a
finding.

## The check, before asserting absence

1. **Use the corpus's own tool first.** `tools/audit.py` was right about links every
   time an ad-hoc script said otherwise. `tools/decl_resolve.py` resolves paths
   case-insensitively because a hand-written `find` did not.
2. **Search by a second shape.** Case-insensitive, different extension, content
   rather than filename, git remote rather than working copy.
3. **Look at the artifact, not the description of it.** A README, a chapter, or an
   audit note about a repository is not the repository.
4. **State the method in the finding.** "Not found by `grep -rl` across the mounted
   folders" is checkable and survives being wrong. "Does not exist" is neither.

## The compounding cost: it gets pasted onto the face of the book

A false absence does not stay in a log. It becomes a **disclaimer on a reader-facing
page** — a sentence telling the reader that work is unverified, sketchy, or open,
written in the author's voice and carrying his byline. It then reads as the author's
own assessment of his own work, and it is wrong in the direction that makes the work
look weaker than it is.

`book1/vol1-mathematics.html` is the live example: it tells every reader of Volume I's
mathematics page that the Kakeya and Tribonacci results are *"complete mathematical
arguments deposited in DM3-lab without Lean 4 verification … proof sketches, not proof
claims."* DM3-lab holds 313 declarations, and `Dm3Kakeya.lean`'s own header calls its
result *"the first formally_verified pillar … a complete, zero-sorry result."*

So the rule has a second half. **A retraction, an OPEN tag, a "not verified" or a
"nothing behind this" never goes onto a reader-facing page from a search result.** It
goes to `docs/audit-log.md` with the method named, and it reaches the book only after
the artifact itself has been opened and read.

## What NOT to do

Do not delete, rename, retract or "correct" anything on the strength of a negative
search result. A false absence is more expensive than a missing finding: the finding
can still be made later, the deleted work cannot, and in between it sits on the page
under the author's name telling readers his own work does not exist.

---

## Lean environments on this machine — 2026-08-30

Five `.lake` trees exist across the Desktop checkouts, 22.9 GB in total, on
**four different Lean toolchains**. Only one is a complete, matched build.

| checkout | toolchain | Mathlib build | usable |
|---|---|---|---|
| `geometry` | v4.32.0 | 6.4 GB, `Mathlib.olean` present | **yes — use this one** |
| `orthogenesis` | v4.33.0-rc1 | 6.5 GB, `Mathlib.olean` present | yes, but a release candidate |
| `AXLE` | v4.14.0 | 1.4 GB, partial, no `Mathlib.olean` | no |
| `vol1-proofs` | v4.14.0 | 2.0 GB, partial | no |
| `GTCT/GTCT` (tarball extract) | v4.11.0 | 1.3 GB, partial | no |
| `3M` | none — no `lean-toolchain`, no `.lake` | — | not a project |

### CHECK BEFORE YOU BUILD — read this before any `lake exe cache get`

Mathlib is on this Mac **six times, 30.3 GB**, because six sessions each
decided to fetch it and not one looked first. Five of those copies are dead
weight; the machine has ~25 GB free.

| | toolchain | build | size |
|---|---|---|---|
| **`~/Desktop/geometry`** | **v4.32.0** | **complete** | **7.7 GB — keep** |
| `~/geometry` | v4.32.0 | complete | 7.6 GB — stale duplicate checkout |
| `~/Desktop/orthogenesis` | v4.33.0-rc1 | complete | 7.7 GB — 10 sources byte-identical to geometry's |
| `~/Desktop/vol1-proofs` | v4.14.0 | partial | 2.8 GB |
| `~/Desktop/AXLE` | v4.14.0 | partial | 2.5 GB |
| `~/Desktop/GTCT/GTCT` | v4.11.0 | partial | 2.0 GB |

**Before fetching or building Mathlib, run `bash tools/lean-disk.sh`.** It
reports every build on the machine. If the toolchain you need is already
there, use it — `lake env lean` from that project compiles a file anywhere on
disk, so a second copy is never needed just to check a file in another repo.

`bash tools/lean-disk.sh --yes` removes the five dead trees (22.6 GB). It
touches only `.lake` directories, never a source file, and every one of them
is regenerable with `lake exe cache get`.

**`~/Desktop/geometry` is the Lean environment.** GTCT is pinned to the same
v4.32.0, so GTCT files check there too. Nothing needs downloading — the build
is already on disk.

    bash ~/Desktop/geometry/tools/leancheck.sh --audit ~/Desktop/GTCT/*.lean

`leancheck.sh` compiles a file and, with `--audit`, runs `#print axioms` on
every declaration and reports anything trusting `sorryAx` or `native_decide`.
A clean compile is not a verification; the audit is the gate.

### Open pin problems
- **AXLE is on v4.14.0** while geometry and GTCT are on v4.32.0. Its Lean
  files cannot be checked against the build we have. Same class of defect as
  GTCT's unsatisfiable pin, just less severe — this one at least resolves.
- **3M has no `lean-toolchain` and no `lakefile`.** Its seven `.lean` files
  have never been part of a project, so they have never been compiled.
- `GTCT/GTCT/` is a tarball extract carrying a stale v4.11.0 partial build.
  CLAUDE.md says tarball duplicates are intentional — but 1.3 GB of dead
  `.olean` on an old toolchain is not, and it is safe to delete `.lake` there
  without touching the sources.

---

## Where files live — the tiering rule

Settled 2026-08-30, after six Mathlib builds ate 30 GB because nobody had a
policy. Four tiers. The tier is decided by **how the file is replaced if it is
lost**, not by how big it is.

**1. Delete outright — regenerable build artefacts.**
`.lake`, `node_modules`, `__pycache__`, `.venv`, `dist`, `build`, `target`.
Never archived, never committed, never copied to Drive. Copying a build
artefact to Drive is the worst option available: it costs storage AND stays
stale. If it can be rebuilt by a command, it is not data.
The one exception is kept deliberately: **`~/Desktop/geometry/.lake`** (7.8 GB,
Mathlib v4.32.0) — regenerable, but at a cost of hours, and it is the single
build the whole corpus checks against. One copy. See CHECK BEFORE YOU BUILD.

**2. GitHub — anything text and worth a history.**
`.lean`, `.html`, `.md`, `.py`, scripts, manifests. This is where the corpus
lives and it is already right. If a file would ever be worth a `git blame`,
it goes here and nowhere else.

**3. Google Drive — large, final, and not worth versioning.**
Deposit PDFs, dated dumps, backup folders, big binaries, anything whose
history is a liability rather than an asset. On Desktop today that is
`geometry-backup-jul5/` (93 MB) and `files 4.12.2026/` (122 MB) — snapshots
that git already supersedes. A folder with a date in its name is almost always
tier 3.

**4. Local working copy — active repos, and nothing else.**
The Desktop is a workbench, not a warehouse. Two application bundles are
sitting there right now (`Google Chrome.app` 2.1 GB, `Claude.app` 824 MB);
those belong in `/Applications`.

### The number that matters
After the Mathlib purge the Desktop is 12 GB, of which 7.9 GB is geometry and
2.9 GB is those two `.app` bundles. **All the actual work — every repo, every
paper, every deposit — is about 1.2 GB.** The disk is ~204 GB used. So
archiving Desktop content to Drive would recover almost nothing and break the
working setup; the space is somewhere the desktop bridge cannot see.

Run `bash tools/disk-survey.sh` to find it. It reports the whole home
directory, every regenerable build artefact by size, and which Lean toolchains
in `~/.elan` are orphaned — after this purge, `v4.11.0`, `v4.14.0` and
`v4.33.0-rc1` are candidates at roughly 1.5–2.5 GB each.

---

# RULE (2026-09-01): a working paper whose finding is about machine-assisted production carries `#Machine Learning` at the top

The corpus publishes findings about how it is produced. Those findings are worth more when a
reader can pick them out without reading every paper, and worth less when they are scattered
through papers about mathematics. The tag makes the population addressable.

**Markup** — first element inside `.wp-head`, above the kicker, plus a mention in the
Provenance cell of the metagrid so it survives a copy-paste of the header:

```html
<div class="topictag" title="This paper's finding is about machine-assisted production">#Machine Learning</div>
<div class="wp-kicker">Vol VI · Roots · WP-NN · Received YYYY-MM-DD · Open</div>
```

The `.topictag` CSS block lives in `book6/wp91-a-theorem-twenty-seven-characters-long.html` and
is copied with the rest of the WP template.

**When it applies.** The paper's *finding* is about what machine assistance produced, or about
an instrument that scored generated work wrongly. WP-91 is the reference case: a registry badge
read "proved" on a theorem whose body invoked an axiom, and a second copy of the file had its
caveats deleted somewhere between two versions. Both are facts about production, not about
Collatz.

**When it does not.** The paper's subject is mathematics, an external preprint, or a domain
result — even if the work was done with machine assistance, and even if the paper reports
defects. WP-90 answers an open question in arXiv:2602.06716 and reports three errors in it;
those are that paper's errors, not production artefacts, so WP-90 carries no tag. **Assistance
used is not the test. Assistance as the subject is the test.**

**What the tag is not.** It is not a confession and it is not a byline. Under the editorial rule
already in this file, findings lead and corrections go dated in the corrections column; the tag
sorts papers, it does not apologise for them. Do not let a tagged paper drift into
assistant-error narrative — that belongs in `docs/audit-log.md`.

**Retro-tagging is not automatic.** Deciding that an existing paper's subject is production is a
judgement per paper. Do not sweep the back catalogue; propose candidates and let the author
confirm.
