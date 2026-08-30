# Audit log — totogt.github.io/geometry

Dated narrative for defects and audits that are closed. Moved out of
`CLAUDE.md` on 2026-08-21 so the priming file stays short to read. Nothing
here was changed, only relocated. Open items remain in `CLAUDE.md`.

# CHAPTER A PASS — the chapter page cited nine declarations that do not exist (2026-08-28)

Found while preparing `chA-autophagy.html` and the Chapter A deposit. Method:
`tools/declaration_scan.py` over `tools/corpus_roots.txt` with `--tracked`, which is
new this session and exists because the declaration-resolver rule had no tool.

## Nine of the ten declarations named on the chapter page do not resolve

**Class: FABRICATED.** `chA-autophagy.html` named ten Lean declarations. One
resolves. The nine that do not:

`CellState`, `autophagy`, `autophagyThreshold`, `autophagy_fold_fires`,
`autophagy_lyapunov_stable`, `mtor`, `nutrient`, `sweet_parker_fold`,
`triple_alpha_fold`.

They were not merely named. §4 displayed a `lean-box` containing the full text of
`structure CellState`, `def autophagyThreshold` and `theorem autophagy_fold_fires`
— statement, hypotheses and tactic proof — for declarations that are in no file in
any of the eleven corpus repositories. A status table gave four of them a green
`closed · 0 sorry` badge. The page also attributed `triple_alpha_fold` to
`AutophagyDm3.lean`, a file which at that date contained no triple-alpha material
of any kind.

The file the page cited does exist and holds 27 declarations. None of them is
named anywhere on the page. `helical_selectivity` in `CatGT_Main.lean` is the one
name that resolves, and it resolves cleanly.

This is the sharpest instance so far of the class the 2026-08-24 pass called
MISATTRIBUTED, and worse in kind: there, true theorems were filed under claims
they did not support. Here the theorems do not exist, and a proof term was
rendered for one of them.

## AutophagyDm3.lean contains three vacuous theorems

**Class: VACUOUS.** `contactForm_nondeg_full`, `whitneyFold_from_kinase_data` and
`limitCycle_exists_auto` are each `: True := by trivial`. They are sorry-free,
which is exactly how they pass every count that keys on `sorry`.

The source is honest about them — each carries a `TODO (Issue #14)` and names the
scalar or algebraic content standing in for it. The defect is not in the file. It
is that "21 sorry-free theorems in `AutophagyDm3.lean`" is a true sentence that
overstates by three, and nothing downstream knew to subtract.

Substantive count for that file: 18.

## gronwall_radius — a third value for the Hessian bound, in a fourth place

Related to **O7**, still open. `AutophagyDm3.lean` proves

    theorem gronwall_radius : (2 : ℝ) / (2 * (1 + 2)) = 1 / 3 := by norm_num

which is the formula at sup‖Hess V‖ = 2. The docstring immediately above it reads
"With |μ_max| = 2 and sup‖Hess V‖ = 1", which would give 2/(2·(1+1)) = 1/2. And
`V_second_deriv_at_one`, eleven lines earlier in the same file, proves V″(1) = 6.

The 2026-08-24 pass recorded the naming sentence at H = 3 and the Lean at H = 2.
This is a third value, in a fourth location. ε₀ = 1/3 is load-bearing corpus-wide
and the theorem asserting it is arithmetically correct; what is not settled is
which Hessian bound is the right one to put in, and that remains physics, not Lean.

## What changed in the chapter, and what did not

Changed: §4 and §8 now cite only declarations that resolve, quoted verbatim from
source. The three placeholders appear in their own table as open obligations
against Issue #14, which is what the file says they are. §8's counts are per file
and separate theorems that carry content from placeholders that do not. The
closing paragraph no longer says the analogy is verified; it says the theorems are
and the identification is argued.

Not changed: the biology, the history, the mTOR account, and the claim that
autophagy and the triple-alpha process are the same fold. That claim is the
chapter's thesis. It is argued in prose, where a thesis belongs.

One word in §5. The display read "Same operator. Same proof. Different universe."
The two proofs now both exist and are not the same: `AutophagyDm3.lean` is real
analysis over Mathlib, `TripleAlphaDm3.lean` is Nat arithmetic with no dependency.
A referee who opens both finds different proofs, so the sentence was falsifiable
and false. It now reads "Same operator. Same threshold structure." The threshold
structure r* = √(J/λ) is what the display actually exhibits, and that much is
true.

## A refinement to the UNFALSIFIABLE GUARD class (2026-08-28)

The class was recorded from `g6_equals_schumann : g6_layer_count_nat =
schumann_4th_harmonic_integer := rfl`, and stated as: `rfl` between two
definitions the author chose. That statement is too wide, and applying it flags
`g33_stability_index : GSeries.cycles .g33 = 33 := rfl` in all three `Chain`
versions, which is not a defect.

`GSeries` is a five-constructor taxonomy — g0, g2, g6, g33, g64 — and `cycles`
assigns each a number. The theorem pins the mnemonic label to its numeral so the
two cannot drift apart. Both sides are internal to the formal system. It does the
job a fixture does, and its docstring says "by definition".

The Schumann case differs in one respect and it is the only one that matters:
`schumann_4th_harmonic_integer` **denotes a physical quantity**. The `rfl` made a
claim about the ionosphere look kernel-checked.

Corrected statement of the class: **`rfl` between two definitions is a defect
only when one of them denotes something outside the formal system.** The shape is
identical in both cases, no scanner can separate them, and a reader separates
them immediately. Any tool reporting this shape must report it as a candidate
for a human read, never as a finding.

## Added

`AXLE/TripleAlphaDm3.lean` — the three-body ladder, Mathlib-free, compiled under
Lean 4.14.0 with `EXIT=0`, no `sorry`, no `native_decide`. Per-declaration
`#print axioms` returns `[propext, Quot.sound]`, and nothing at all for
`tribo_rec`. Six theorems: positivity, the recurrence, η > φ and η < τ = 2 in
ordinal form, and the two-sided bracket. Wired into `lakefile.toml` as its own
`[[lean_lib]]` target, since a file that is no target's root is compiled by nothing.

It proves no physics and its header says so. The triple-alpha identification is a
modelling claim of the chapter prose, not a theorem of the file.

# EDITORIAL PASS on the Volume I V7 release — six more defects, three of them mine (2026-08-24)

The V7 release above was handed over, and then read again as an editor rather than
as its author. That second pass found more than the first, which is the point of it.

## The worst one is mine: V7 was built on the wrong ancestor

**Class: MIS-CORRECTION.** I based the V7 paper on
`AXLE/a.PolyLaminin/principia_vol1_v2_full.tex` — 1,168 lines, 18 pages, a V2-era
file. The real paper is `Downloads/files (34)/principia_vol1_v6.tex` — 2,322 lines,
**42 pages** — and its PDF is byte-identical (md5 `28cd9e46…`) to the
`principia_vol1_v5_FIXED.pdf` in the same tree. Three filenames, one document.

Consequence: I reported that *"the LaTeX source did not compile either; it
referenced three figures under names that exist nowhere, and the Perelman
correspondence figure is withdrawn."* **That was false.** The real source uses
`fig1_phase_portrait`, `fig6_operator_sequence`, `fig5_coherence_bridge`, all three
present in the deposit, and it compiles clean on the first pass. The figure was
never missing. The claim is withdrawn from `CHANGES_Vol1.md` and from the commit
record, and V7 is rebuilt from the correct source (47 pp).

**Rule.** Before correcting an artifact, establish which artifact is current. A
repository with `_v2_full`, `_v5_FIXED` and `_v6` in three directories does not
answer that by filename. Hash the PDFs; the deposit's own version history is the
authority, not the tree.

## The second is also mine: a sharpness claim that witnessed nothing

**Class: MIS-CORRECTION.** V7 shipped `separation_sharp_at_33 : Σ_{i<33} 1⁶ = 33`
and read it as proof that the hypothesis `n < 33` is load-bearing — explicitly, as
proof that it is "not an unfalsifiable guard."

It is not a witness for that. Its configuration has every `λᵢ = 1`, which violates
the theorem's own transverse hypothesis `|λᵢ| ≤ e⁻²` for `i ≠ 0`. Under the actual
hypothesis, at n = 33 the sixth-power trace is within 32/4096 of **1**, not 33.

Doing the arithmetic properly: the bound is `|Tr − 1| ≤ (n−1)·(1/4)⁶`, so the
conclusion survives to `n = 131072 = 32·4⁶`. `n < 33` is **sufficient and nowhere
near necessary**. It is inherited from the dm³ dimensional threshold, not forced by
this estimate. And it cannot simply be deleted either: with about 1.7·10⁷ transverse
directions each contracted to exactly `e⁻²`, the trace does exceed 33.

Both facts are now theorems — `spectral_trace_ne_33_upto` and
`separation_fails_in_high_dimension` — and the misread theorem is renamed
`coherent_directions_realise_33` with a docstring saying what it does and does not
show. A warning class the corpus already tracks was, in this instance, produced by
the person writing the warning.

## ε₀ = 1/3 does not close as printed — new obligation O7

**Class: FALSE.** The headline constant of Volume I. §22, Proof VII, reads:

> ε₀ = |μ_max| / [2(1 + sup‖Hess V‖)] = 2/(2·3) = 1/3, where sup‖Hess V‖ = |L₂| = 3.

Three statements. They cannot all hold.

| | value |
|---|---|
| formula at H = 3 | 2/(2·4) = **1/4** |
| printed arithmetic `2/(2·3)` | corresponds to 1 + H = 3, i.e. **H = 2** |
| the Lean line `2/(2*(1+2))` | **H = 2** |

So the formula and the Lean agree with each other, and the sentence that names the
constant disagrees with both. `epsilon0_of_eq_third_iff` proves the choice is
forced: for H ≥ 0, this formula yields 1/3 for exactly one Hessian bound, H = 2.

This is the same defect the ε₀ audit found in `G6Crystal.lean` in July, surfacing in
a second place. It is not decided here, because deciding it is a question about
which Hessian bound enters the Gronwall estimate — `V''(1) = 6`, `|L₂| = 3` — and
that is physics, not Lean. Logged as **O7** in the deposit and stated in the paper.
ε₀ = 1/3 is load-bearing corpus-wide; a constant reached by an argument that does
not close is worth knowing about.

## A physical prediction was reported as machine-checked

**Class: MISATTRIBUTED.** The Factor-of-3 Prediction — gravitational decoherence
satisfies τ_grav < τ_dec/3, a factor of 3 tighter than the Penrose bound — carried
the sentence *"This is machine-checked (Lean: `basin_asymmetry`: 1/3 < 4/5)."*

`basin_asymmetry` is an inequality between two rational numbers. It says nothing
about gravitational decoherence, and no kernel can check a physical prediction. This
is the NASAGaps defect again — true theorems filed under claims they do not support
— and it is the one class no machine can catch, because one side of the comparison
is a sentence in English. Withdrawn; the prediction stands as physical argument,
which is what it is.

## Two structure fields are weaker than their names

**Class: VACUOUS.** `UnfoldOp.stable_branch` reads
`∀ x, ∃ n, IsFixedPt (map^[n]) (map x)`. Take n = 0: `f^[0] = id`, and every point
is a fixed point of the identity. The field is satisfied by **every map on every
type**. "Theorem D (stability)" therefore has no content beyond Φ-decrease. The V6
file recorded this in a comment; V7 proves it, so it is a fact a reader can act on
rather than a remark that can be skipped.

**Class: MISMATCH.** `CompressionOp.contractive` reads `d(fx,fy) ≤ d(x,y)`. That is
*non-expansive*. The identity satisfies it — and `C_ex`, the deposit's own witness,
is exactly the identity. Assumption 3 should say "non-expansive"; a contraction
needs `≤ k·d(x,y)` with `k < 1`, which nothing here requires and nothing uses.

## And a guard that could not fail

**Class: UNFALSIFIABLE GUARD.** §12 ended with

```lean
def schumann_4th_harmonic_integer : ℕ := 33
theorem g6_equals_schumann : g6_layer_count_nat = schumann_4th_harmonic_integer := rfl
```

Both sides are definitions equal to 33. It is `33 = 33`. It was counted among the
machine-checked facts, and the ledger already records the Schumann identification
itself as only partly supported — four carriers claimed, two real. Withdrawn rather
than repaired: a kernel cannot check a claim about the ionosphere, and dressing an
empirical assertion as `rfl` makes it look verified. The claim moves to prose, where
it can be argued and challenged.

## Smaller, still real

- **`V(1) + 2 = (q−1)²(q+2)`** (§19). Left side a number, right side a function of
  q. The Lean is `V q + 2`. Typo, but in a displayed equation labelled
  "machine-checked".
- **`1/3 < 4/5 ≈ r*`.** The corpus's canonical inner boundary is
  `r★ = 0.77594059`; 4/5 = 0.8 is 3% above it, and `≈` reads as an identification.
  Both comparisons are now theorems, and the text says which number is numerical
  input rather than proved.
- **`10.5281/zenodo.19117400` given as the "series root"** in Data and Software
  Availability. It is the version DOI of Volume I V1 (17 March 2026). The concept
  DOI is `19117399`.
- **Counts.** §14 has 12 theorems, not 9; the header block carried two compensating
  errors that summed to the right total; the status table summed to 48 while
  claiming 49. Counts are now produced by `tools/counts.py` and never typed.

## Rules

**Compensating errors are the reason to compute totals rather than type them.**
Two wrong numbers that add to the right one survive every review that checks only
the sum.

**A second pass by the same author, in a different role, is worth its cost.** The
first pass fixed 81 compile errors and a false theorem, and shipped a false claim
about figures and a sharpness claim that witnessed nothing. Neither was caught by
being careful the first time. Both were caught by reading it back as an editor.

Final state: 58 theorems, 0 sorry, kernel-checked; paper 47 pp rebuilt from the
correct source; O7 opened.

---

# FIXED: the Volume I deposit's Lean had drifted off its own Mathlib pin (2026-08-24)

**Class: STALE — silent version drift, and the reason CI is not optional.**

`PrincipiaOrthogona1/PrincipiaVol1.lean` is the formal-verification artifact
attached to the Principia Orthogona Volume I deposit (10.5281/zenodo.19117400).
V3 through V6 described it as *"30+ facts proved, 1 sorry (clearly scoped), 0
axioms beyond Mathlib4."*

AXLE has no CI. Nothing in the repository re-runs that file. So the question
"does it still build against the revision the repo pins?" had not been asked.

A small repository was built to ask it — `vol1-proofs`, one file, pinned to
Lean v4.14.0 and Mathlib v4.14.0 rev 4bbdccd9c5f8, exactly what
`lake-manifest.json` names. AXLE is too large to build for one check; that is
why the small repos exist.

**Result: 81 errors.**

**The first diagnosis of that number was wrong, and is withdrawn.** I recorded
it as "the file had never been elaborated by Lean." The author's account is
that these files were run, repeatedly, and the error profile agrees with the
author and not with me:

| name used in the file | status at the pin | when it changed |
|---|---|---|
| `Ordinal.sup`, `Ordinal.lt_sup` | deprecated | 2024-08-27 |
| `Ordinal.IsLimit.add_right` | renamed `isLimit_add` | 2024-10-11 |
| `Set.finite_insert` | Mathlib-3 spelling of `Set.Finite.insert` | port-era |
| `pow_le_pow_left` | deprecated for `pow_le_pow_left₀` | 2024 |

Those are the names of a file written and run when they were current. Sorting
the 81: 23 proofs that no longer close, 20 missing instances, 15 type
mismatches, 8 unknown constants — that is Mathlib moving underneath working
code. Six parse errors and five consequent unknown-field errors are a later
hand-edit (three structure fields written on one line separated by `;`) that
was never rebuilt.

So the true finding is narrower than the one I filed, and more useful:

> **The deposit's pin was advanced past its own code, and nothing re-ran the
> build, so the drift was silent for four published versions.**

That is a tooling failure with a one-line fix, not a claim about anyone's care.
The file is now at the pin, and `vol1-proofs/tools/run.sh` re-runs it in one
command.

**Rule.** A pin is a claim, and like any claim it goes stale unless something
re-checks it. "Compiles under current Mathlib" is not checkable; "compiles
under rev 4bbdccd9c5f8" is — but only if someone, or something, runs it. Ship
the runner with the artifact.

**Second rule, learned the hard way here.** When a build fails, read the
failures before naming the cause. Deprecation dates are in the Mathlib source;
they distinguish "was never right" from "stopped being right", and those call
for completely different responses.

## The separation theorem: FALSE, not unfinished

The file's one advertised `sorry` sat in `separation_theorem`, attributed to a missing
Mathlib eigenvalue API and tracked as open obligation O1 / AXLE issue #12.

Do the math before assuming the label is right. The hypothesis is

```
IsDm3Stable M  :=  ∀ i ≠ 0, |M i i| ≤ exp (−2)
```

which constrains the transverse diagonal and says nothing whatever about `M 0 0`. So the
trace is unbounded. At `n = 1` there is no transverse direction at all, the hypothesis
holds vacuously, and the 1×1 matrix `(33)` has trace 33. **The deposited theorem is
false.** That refutation is now itself a proved theorem in the file
(`v6_separation_statement_is_false`) — the record is worth more than a silent fix.

No eigenvalue API would have closed it. What was missing was a hypothesis, not a lemma.

## And the sixth power had been dropped

Reading the ancestors rather than the label: Book 2 Theorem 12.2, `lean/main_v7.lean`
Part H, and `AXLE_v6.lean` Part H all state **Tr(M⁶) ≠ 33**. The deposit states
`M.trace ≠ 33`. The exponent was lost in transcription, leaving a hypothesis about `M`
and an argument about `M⁶` with nothing joining them.

The numbers say the same thing. The intended bound is `|Tr − 1| < 1` off at most 31
transverse directions:

| power | per-direction bound | 31 directions | `|Tr − 1| < 1`? |
|---|---|---|---|
| first | e⁻² ≈ 0.1353 | ≈ 4.195 | **no** |
| sixth | e⁻¹² ≈ 6.14·10⁻⁶ | ≈ 1.9·10⁻⁴ | yes, with room |

So the first-power form could never have been proved by the argument attached to it, and
the sixth-power form needs no eigenvalue API at all once the statement is made about a
diagonal matrix or about the eigenvalue list — which is where the spectral reduction has
already been performed.

## What V7 proves

49 theorems, 0 sorry, kernel-checked, no axiom beyond `propext` / `Classical.choice` /
`Quot.sound`. Nine of them are the new §9:

`exp_neg_two_le` (e⁻² ≤ 1/4, from `1 + 1 ≤ e` alone) · `exp_neg_twelve_le` ·
`transverse_sum_bound` (the step V6 admitted) · `spectral_trace_ne_33` ·
`separation_theorem` (diagonal, sixth power) · `separation_trace_first` (first power,
carrying the normalisation V6 omitted) · `separation_sharp_at_33` · 
`dm3_hypothesis_nonvacuous` · `v6_separation_statement_is_false`.

The last two are there on purpose. `separation_sharp_at_33` shows the dimension bound is
load-bearing — at n = 33 the sixth-power trace *is* 33 — so the hypothesis is not an
UNFALSIFIABLE GUARD. `dm3_hypothesis_nonvacuous` exhibits a witness, so the theorem is
not vacuously true. Both classes are on this ladder already; both checks now ship with
the theorem they guard.

The margin, once stated correctly, is not narrow. Under the hypotheses the sixth-power
trace lies within `31/4096` of 1. It misses 33 by more than 31. That gap **is** the
dimensional threshold: 33 units of trace need 33 coherent directions, and below 33
dimensions there are not 33 directions to be had.

## What was withdrawn

Every provenance line of the form *"Source: `X.lean` — 0 sorry"* has been removed from
the section banners. Those files have not been built either. The claim is restored per
file as each one goes green — not before.

The §14 banner read *"STATUS: NOT MACHINE-CHECKED beyond this file's own lake build in
CI."* There was no CI and no lake build. Those nine theorems are now genuinely checked.

## Rule

**A verification artifact that has never been built is not a weak claim, it is a costume.**
A false theorem can be refuted; an unbuilt file was never put in a form anything could
refuse, while wearing the word "verified" on the front. The check is one line. Ship the
runner with the artifact: `vol1-proofs/tools/run.sh` builds, probes every named theorem
with `#print axioms`, and refuses on `sorryAx` or on any axiom outside the allowlist. It
is 40 lines and it would have caught this in May.

**And: when a `sorry` carries a reason, the reason is a claim too.** O1 said "Mathlib
eigenvalue API." Four versions repeated it. It was wrong, and it was wrong in the
direction that makes it look like someone else's problem — an upstream gap, nothing to do
here, wait for Mathlib. Doing the math took an afternoon and the API was never involved.

**Still open:** AXLE has no CI at all. 1,165 formalized entries, nothing re-runs any of
them. This defect is what that costs.

---

# FIXED: `book6/index.html` was hiding 16 finished pages (2026-08-17)

Every other defect logged here is the corpus claiming more than it has. This one was the
reverse, and it cost more: **16 completed pages, 521 KB, were live on the site with no
link from the index at all.** Two more existed only as prose mentions with no chapter row.

Restored, with titles and descriptions taken from each file's own `<title>` and meta
description rather than invented:

- **The Portuguese Vol VI sequence** — `chVI-preface` (Cap 0), `chVI-conjecture` (Cap 1),
  `chVI-wigner` (Cap 2), `chVI-planetary` (Cap 3), plus `g6-crystal.html`. A complete
  reading path with no entrance. Cap 1 now carries "AXLE Issue 6 — aberta, não
  demonstrada" so the conjecture is not read as settled.
- **IP and commercial, 5 files** — `patent-city-doctrine`, the invention disclosure in
  English and Portuguese, and the `jbs47` / `esg47` twenty-year plans. Badged Tech / IP;
  both plans marked **prospective — a proposal, not an agreement**, since an unlabelled
  20-year plan naming a real company reads as a deal.
- **Nutrition, 3 files** — `ch-nutrient-spectrum` (72 KB) and `ch-nutrient-predictions`
  (71 KB), the two largest files in the volume, plus `wp-nutrient-spectroscopy`.
- **Biology, 2** — `ch-immune-maintenance`, `ch-multiagent-biological-transitions`.
- **Loose ends, 3** — `wp02-alterna`, `wp69-the-fold-is-a-coordinate`,
  `hidden-track-punk-edu`.

Also corrected on that page: the footer claimed *"Two stubs due: chDev-waddington.html ·
chIm-thymus.html"* — both are finished (25 KB and 22 KB); the stat tile read "25 Chapters
Planned" against 100 live rows; and the contents heading read "27 Chapters". Counts are
now 118 rows, heading and tile derived from the actual count.

**Rule.** An index is a claim about what exists. Audit it the same way as any other claim:
`set(files on disk) - set(files linked)` should be empty, and the count in the heading
should be computed, not typed. Both checks take one line and neither had ever been run.

---

# FIXED: repo-wide link audit (2026-08-18)

The earlier book6 audit only globbed `book6/*.html` and treated `/geometry/...` as a
filesystem path. Both were wrong: it missed `book6/differential-equations/` and
`book6/policy/` entirely, and it would have flagged every site-root-absolute link as dead.

**Correct method, for reuse.** Resolve `/geometry/X` against the repo root, everything else
against the linking file's directory; skip `http`, `mailto`, `javascript`, `data:`, `tel:`,
protocol-relative, and anything containing a JS template fragment (`${...}`, `' + t.card + '`)
— those are string concatenations, not hrefs.

**Result: 99 real dead links → 18.**

- **51 were pure path errors** — the file existed elsewhere under a unique name. Repaired
  with computed relative paths: HVEH chapters pointing at `book4/` siblings, `book1`–`book3`
  indexes pointing at root-level chapters, `hub.html` pointing at four `book4/` PDFs.
- **27 more were ambiguous by basename** and resolved by choosing the volume copy over the
  root stub: `living-book.html` → `book4/`, `vol1-mathematics.html` → `book1/`,
  `vol2-contact.html` → `book2/`, `vol2-dashboard.html` → `book1/`, `gomc-opus.html` →
  `book4/`. Plus `HVEH/proofs/index.html`, which had a doubled `proofs/` segment on seven
  links to files sitting beside it.
- **4 were the book6 survivors**: the heat-equation monograph exists at
  `book6/differential-equations/heat-equation/` (link assumed one level up); the two
  `../../AXLE/*.lean` links pointed outside the repo at files absent from AXLE too, now
  aimed at the repo root and titled as not-yet-deposited; `wp63`'s AULA link disabled since
  no `applications/` directory exists.

## The 18 that remain — authorial decisions, not path errors

No file of that name exists anywhere in the repo. Each needs either the file, or the link
removed:

`vitruvian-approximation.pdf` (4 pages) · `living-book.html` variants resolved but
`OMEGA_STATUS_AUDIT.md`, `docs/index.md` (×2), `ch6-cardiac.html`, `gomc-opus` resolved,
`banking-butterfly-preprint-pt.html`, `TribonacciEta.lean`, `course-16weeks-source.html`,
`impa-portal-patch.html`, `index-geometry-hub.html`, `journey-v1-backup.html`, `ch5.html`,
`maquinas.html`, `access-required_copy.html`, `aula-index.html` (book7/ch-huh),
`certify_rstar.py` and `PO_10_Pablo_Grossi.pdf` resolved to `book4/`.

`vitruvian-approximation.pdf` is the most linked of the true absences — four pages promise
it. Either deposit it or drop the four links.

# FIXED: §4's unsourced interval (2026-08-18)

`on-publication.html` §4 claimed *"between five and thirty years for a novel framework to
acquire enough secondary literature."* No source, and none findable. **Withdrawn.**

Replaced with the real bibliometrics, which support the shape but not the interval: Ke,
Ferrara, Radicchi & Flammini, *"Defining and identifying Sleeping Beauties in science"*,
PNAS 2015 (doi:10.1073/pnas.1424329112) — 22 million papers, and delayed recognition turns
out **not** to be a rare separable class but a continuous spectrum in both hibernation
length and awakening intensity, with early citation counts a poor proxy for impact. The
page now says the weaker, defensible thing and states that the old figure was withdrawn.

# FIXED: `book1/index.html` was two documents in one file (2026-08-18)

Found while extending the index-orphan audit past Book VI. `book1/index.html` (1,404
lines) contained **two complete HTML documents concatenated**, with the closing tags
interleaved:

- lines 1–328 — *Formal Verification Registry*, its own `<head>`, `<title>`, `<style>`,
  never closed;
- lines 329–1402 — *Principia Orthogona · Volume I · Version 4 · June 21, 2026*, a second
  `<!DOCTYPE>`, `<html>`, `<head>`, `<body>`, closed at 1402;
- lines 1403–1404 — the first document's `</body></html>`, arriving after the second
  document had already closed.

Consequence: **the first thing a reader of Book I saw was "None of this is machine-checked
yet."** That sentence is a true statement about five Lean files on 2026-07-03. It is not a
true statement about the corpus, and it sat above the Volume I text on the volume's own
front page. The second document's `<style>` also applied globally, so the registry half was
rendered in the wrong stylesheet.

**Fix — split, not rewrite. Both halves preserved verbatim:**

- `book1/verification-registry.html` (new) — the registry document, properly closed, plus
  one added banner marking it a superseded 2026-07-03 snapshot and pointing at the live
  three-tier registry. No counts were edited; the page still says what it said. Per rule 7
  the stale caveat was *added*, not removed.
- `book1/index.html` — now the Volume I V4 document alone.

Both files parse with zero unclosed tags, zero stray closers, zero duplicate ids, and the
class/CSS split is clean (`banner warn` lives only in the registry half, `toc-drawer` /
`nav-links` only in the Volume I half) — which is itself the evidence that the two
documents were never integrated.

## Nav defects fixed in the same pass

1. **Two `<a>` outside `.nav-links`.** `nav` is `display:flex; justify-content:space-between`
   and only `.nav-links a` is styled, so `Living Book` and `Series ↗` rendered as default
   blue underlined links, spaced apart from the rest of the bar. Moved inside the div.
   **This same stray-anchor pattern is present in `index.html` (root) and `book2/index.html`
   and is not yet fixed** — it looks like one botched append repeated across files.
2. **`../index.html` was labelled "Formal Verification Registry."** It is the series root.
   Relabelled *Principia Orthogona*.
3. **Book I's own index linked none of its own files.** Added `verification-registry.html`
   and `vol2-dashboard.html`.
4. **Nav "Zenodo" pointed at 10.5281/zenodo.19117400** — Vol I's *v1* deposit, which per the
   ISBN/DOI section above is the *origin* citation, not the current text. The page's own
   badge cites V4, 10.5281/zenodo.20784030; the nav now agrees with the page.

## OPEN — authorial call, not fixed

**CORRECTED 2026-08-18, same day.** The first version of this entry said "17 pages link the
Second Edition, none link V4." That was wrong — it came from grepping the substring `book1/`
and reading two different targets as one. Counted properly (paths resolved, `/geometry/`
prefix handled, `_archive` excluded), there are **three Volume I files**:

| file | edition | inbound links |
|---|---|---|
| `vol1-mathematics.html` (root) | **V4 · June 21, 2026** | **51** |
| `book1/vol1-mathematics.html` | Second Edition · April 2026 | 7 |
| `book1/index.html` | V4 · June 21, 2026 (copy) | 5 |

So V4 is not unreachable — the root copy is the most-linked page in the series. The stale
one is `book1/vol1-mathematics.html`, linked from `book2/index.html`,
`book2/vol2-contact.html`, `book3/index.html`, `book1/vol2-dashboard.html`,
`book4/logs-segment.html`, `index-book1.html`, `master-index.html`.

**Which Volume I is canonical?** The root copy, on link count. But the two V4 copies have
already drifted: the root copy hyperlinks reference [WP-02] to `book6/wp02-alterna.html`;
the `book1/index.html` copy leaves it as plain text. Splitting `book1/index.html` therefore
produced a **third** copy of V4 that was already one edit behind root.

**RESOLVED, author's decision, 2026-08-18:** `book1/index.html` is now **a real index — a
list of the volume's files — and the text of Volume I is read at the root copy.** There are
again only two Volume I texts: `vol1-mathematics.html` (V4, current) and
`book1/vol1-mathematics.html` (Second Edition, kept for the orthogenesis note). The index
lists every file in `book1/`, including the duplicates and the misnamed one, so nothing in
the directory is reachable only by guessing a URL.

V4 is **not** a superset, which is why the 7 stale links must not simply be repointed. The
Second Edition carries a `<details>` note **"A note on 'orthogenesis'"** — the disclaimer
separating *orthogonal genesis* from the dead nineteenth-century biological theory, citing
Waddington's canalisation — and **both V4 copies dropped it**. Repointing those 7 links
silently deletes that disclaimer from every path a reader can take. Either:
(a) V4 regains the orthogenesis note, then the 7 links repoint at `vol1-mathematics.html`; or
(b) `book1/vol1-mathematics.html` is explicitly labelled the archived Second Edition and the
    links stay as they are.

**Navs fixed 2026-08-18 (both Vol I files).** Stranded anchors moved inside `.nav-links`;
added `vol2-dashboard.html` and `book1/verification-registry.html`; the root V4 nav's Zenodo
link pointed at `19117400` (the v1 origin deposit) while the page's own badge cites
`20784030` — the nav now agrees with the page. The Second Edition's nav gained an explicit
`Vol I · V4 · June 2026 →` link, so the newer text is reachable from the older without
deciding which is canonical. Every nav target verified to exist; both files parse with zero
unclosed tags.

Also open: `book2/index.html` and `book2/vol2-contact.html` are **byte-identical** (69,403
bytes, `cmp` clean) — one is a copy of the other, and `book2`'s nav sends "← Vol I" to the
stale `book1/vol1-mathematics.html`.

14 `.bak` files are **tracked in git and published to GitHub Pages**, including
`book1/vol1-mathematics.html.bak`.

# FIXED: `book1/vol2-dashboard.html` is not a dashboard (2026-08-18)

Found while writing the new Book I index. **`book1/vol2-dashboard.html` (69,313 bytes) is the
Volume II text** — *Contact Realization of Generative Transitions, Version 2a* — under a
filename that promises a dashboard. It differs from root `vol2-contact.html` by four diff
lines, all of them relative paths. The **actual** interactive dashboard is root
`vol2-dashboard.html` (38,140 bytes, `<title>Principia Orthogona Vol. II — Interactive
Dashboard</title>`).

Consequence: **20 links whose visible label said "Dashboard", "Interactive Dashboard" or
"interactive dashboard →" opened the Volume II paper instead**, across `book2/index.html`,
`book2/vol2-contact.html`, `book3/index.html`, `book1/vol1-mathematics.html`,
`book1/verification-registry.html` and the file's own self-links.

**Fixed** by repointing at the real dashboard — but only where the anchor's own visible label
mentions a dashboard. Links that correctly describe the file as Volume II were left alone.
Two of those are in `index-book1.html` and `master-index.html`: the generated indexes label
the entry *"Principia Orthogona · Volume II · Contact Realization"* — accurate, because they
read the file's `<title>` — and their `<span class="path mono">book1/vol2-dashboard.html</span>`
sits **inside** the anchor text, so a naive label filter matches on the word "dashboard" in
the path and rewrites a link that was right. It did, on the first pass, and both files were
restored from `HEAD`. Any future sweep over anchor labels must strip `.path` spans first.

**Still open:** the file itself. `book1/vol2-dashboard.html` remains a fourth copy of the
Volume II text under a misleading name. Renaming it would break the two generated-index
entries and any external link. The new `book1/index.html` documents it in full rather than
hiding it. Author's call whether it is renamed, made a redirect, or removed.

# RESOLVED: "V4" and "v6" — v6 is the current Volume I deposit

Raised 2026-08-18. The site labels Volume I's current deposit **two different ways in two
different books**, and both call themselves current:

| label | DOI | date | where |
|---|---|---|---|
| **V4** (edition of the *text*) | 10.5281/zenodo.20784030 | text dated 21 June 2026 | `vol1-mathematics.html` (eyebrow, badge, nav, footer), `chRho-spectral.html`, `Enceladus.html` |
| **v6** (Zenodo's *deposit* counter) | 10.5281/zenodo.21146416 | 2 July 2026 | `book7/ch-lattes.html`, `book7/wp59-dark-matter-lensing.html`, `book7/jacobian-verification.html`, `GameTheory_Full_Pack.html`, and the ISBN/DOI section of this file |

These are not the same kind of number. "Version 4" is the author's edition of the text —
the page's own eyebrow reads *"Principia Orthogona · Volume I · Version 4 · June 21, 2026."*
"v6" is Zenodo's counter on the concept record, which increments on **every** deposit,
including metadata-only corrections. An edition and a deposit count drift apart by
construction.

**They cannot both be Vol I's current DOI.** Two readings fit the repo, and this session
could not tell them apart — Zenodo's API and record pages are robots-disallowed from the
tooling available here:

1. `20784030` is Zenodo v4, and two later deposits (v5, v6) exist — in which case the
   website's Volume I is **two deposits behind** the record, and 21146416 is correct.
2. The author's Version 4 text was deposited *as* v6 `21146416` — in which case
   `vol1-mathematics.html`'s own badge cites the **wrong DOI for the text on that page**,
   and `20784030` is an earlier deposit.

**Settle it by opening the concept DOI** <https://doi.org/10.5281/zenodo.19117399>, which
always resolves to the newest version, and reading the version badge and version-history
list on the record page. Then make the site say one thing. Do **not** guess and sweep: three
files carry one number and four carry the other, and picking wrong propagates a bad citation
into both halves.

**Related defect found in the same check.** `Enceladus.html` line 1038 cites Vol I as
*"...Zenodo 10.5281/zenodo.20784030 (2026). **ISBN 979-8-9954416-0-1**."* That ISBN is
allocated to **Complete Completeness · G5 · Paperback** (registered), not to Volume I.
Volume I has no allocation of its own, so per the rule above it gets **no ISBN line at all**.
This is the borrowed-ISBN defect again, in a file the August sweep did not reach.


## Ruling and repair (2026-08-18)

**Author's ruling: v6, `10.5281/zenodo.21146416`, is Volume I's last version.** The site now
says so.

The version ladder, reconstructed from the DOIs the pages themselves carry — this is what
settled the question, because the numbers form a clean sequence and Zenodo's counter tracks
the author's edition numbering rather than running independently of it:

| deposit | DOI | cited in |
|---|---|---|
| v1 · 17 Mar 2026 | 10.5281/zenodo.19117400 | `book1/vol1-mathematics.html` deposit table, and dozens of pages as the origin deposit |
| V3 | 10.5281/zenodo.20237688 | `Enceladus-zenodo.html` |
| V4 · text dated 21 Jun 2026 | 10.5281/zenodo.20784030 | `vol1-mathematics.html`, `chRho-spectral.html`, `Enceladus.html` |
| **v6 · 2 Jul 2026 — current** | **10.5281/zenodo.21146416** | `book7/ch-lattes.html`, `book7/wp59-dark-matter-lensing.html`, `book7/jacobian-verification.html`, `GameTheory_Full_Pack.html` |

**Fixed — 12 edits across 5 files.** Every place the HTML presented a Zenodo link as
*Volume I's record* now resolves to v6:

- `vol1-mathematics.html` — nav and footer point at v6. The hero badge is the one place that
  keeps both, because both are true and the distinction matters: *"This text (V4):
  20784030"* beside *"Current version (v6): 21146416"*.
- `chRho-spectral.html` — two "Zenodo V4" links → v6.
- `Enceladus.html`, `Enceladus-zenodo.html` — reference [2] and the footer cite Volume I as a
  work, so both take v6. `Enceladus-zenodo.html` had been three versions behind, still on V3.
- `book1/vol1-mathematics.html` (archived Second Edition) — its badge said flatly
  *"Zenodo 10.5281/zenodo.19117400"*, which reads as *this edition's* DOI and is not; it is
  the v1 origin deposit. Now labelled as such, with v6 named beside it.

**Borrowed ISBN removed in the same pass.** All four of those Volume I citations carried
**ISBN 979-8-9954416-0-1** — allocated to *Complete Completeness · G5 · Paperback*, not to
Volume I, which has no allocation and per the rule above gets no ISBN line at all.

## STILL OPEN after this repair

1. **The website's Volume I text is two deposits behind the archive.** The page is V4, dated
   21 June; the record is v6, dated 2 July. The badge now discloses this rather than hiding
   it, but disclosure is not a fix — either the v6 text is published to
   `vol1-mathematics.html`, or the page states what changed between V4 and v6. **Do not
   silently relabel the page "Version 6": no one has compared the two texts.**
2. **The G5 paperback ISBN is still attached to non-G5 material in 8 files** —
   `trilogy-sale.html` (×4), `GameTheory_Full_Pack.html`, `GameTheory_Full_Pack.FIXED.html`,
   `Sportal.html`, `classroom-index.html`, `impa-working-paper.html`, `newark-wellness.html`,
   `portal.html`. Each needs reading before editing: on a G5 page the number is correct.
3. **`19117399` is still presented as a "series DOI" in roughly sixty files.** It is Vol I's
   concept DOI; there is no series DOI. This is the defect the ISBN/DOI section at the top of
   this file already documents, and it is by far the largest remaining citation problem in
   the repo. It was not touched today.

# Reachability audit, redone properly (2026-08-18)

The per-book orphan counts from the first pass were wrong in the same way the Volume I
inbound-link count was wrong: they compared a directory's files against links **from that
directory's own index**. `book4/index.html` is a 1.7 KB stub that links only
`contents.html`, so the method reported *50 orphans of 51* for book4. Those 50 pages are
reachable — through `book4/contents.html` and `living-book.html`.

**Correct method: breadth-first reachability from `index.html`**, resolving by path, honouring
`/geometry/` site-absolute hrefs, and following `.html` literals inside `<script>` (audit
rule 4 above). Result:

| measure | reachable | unreachable |
|---|---|---|
| counting the generated indexes as link sources | 633 / 636 | 3 |
| **excluding them (audit rule 1)** | **577 / 636** | **59** (2.0 MB) |

**The gap between those two rows is the whole point, and it is a trap.** Adding one link to
`master-index.html` — which lists nearly every file — moves the headline number from 60 to 3
without navigating anyone anywhere. Audit rule 1 at the top of this file predicted exactly
this: *"count it and the orphan column reads zero forever."* It is now demonstrated. **The
honest figure is 59.** Any future report that quotes a number near zero without saying
whether generated indexes were excluded is measuring nothing.

## Fixed

1. **The generated-index system was an island.** `master-index.html` links all fifteen
   `index-*.html` files, and *nothing in the live site linked to `master-index.html`* — its
   fifteen inbound links all came from pages that were themselves unreachable. Root
   `index.html`'s nav now carries **All Files → `/geometry/master-index.html`**. This is
   worth doing on its own merits — the index was unusable — but see the trap above: it is
   not an orphan fix.
2. **Root `index.html` had the stranded-anchor defect too.** `Living Book` and `Series ↗`
   sat outside `.nav-links`. Verified from the CSS, not assumed: root `index.html` has
   `nav { display:flex }`, styles only `.nav-links a`, and has **no** global `a` rule and no
   `nav a` rule — so both rendered as default blue underlined links. Moved inside, and
   switched to `/geometry/` paths to match the rest of that nav.
3. **`omega/index.html` and `contact/index.html` were not indexes.** Both were stale copies
   of the site's **home page** — same title, *"O Princípio do Cajueiro · dm³ Soundworks"*,
   and within a kilobyte of root `index.html`'s size. So `/geometry/omega/` served the
   homepage instead of the Omega Point series, and this is what made the first audit report
   omega as "1 linked of 42": `omega/index.html` was never omega's index. The real one is
   `omega/omega-point-index.html`, and it is reachable.
   Both are now small redirect pages — meta-refresh plus `rel=canonical` plus a visible
   link, no JavaScript — `omega/` → `omega-point-index.html`, `contact/` → the home page
   (that directory contains nothing else).

   *Noted but not diagnosed:* the copies carry broken sentences against root — a bare `.`
   where root reads `Forest Hill.`, and *"the walk from this building to will be a public
   meditation trail"* where root reads *"to Forest Hill will be."* That looks like a
   find-and-replace that deleted a phrase, but the copies are **older** (3 Aug vs 12 Aug),
   so root filling the gaps is equally consistent. Do not repeat the damage theory as fact.

## Open

- **`_cajueiro-index-misplaced.html` is a third copy of the home page.** Left alone: it is
  not at a directory URL, so it misleads no one, and its filename already says what it is.
- **`master-index.html` is stale.** It does not list `course-hist201.html`,
  `hist201-development-proposal.html` or `tutor-deck.html`, added in `2cf3906` after the
  index was last generated. Whatever generates it needs re-running.
- **59 pages remain genuinely unreachable**, 39 of them at root. Known clusters: duplicate
  name-variants in `book4` (`ch06b-elojo` / `ch07-newark` / `ch08-harrison` /
  `ch09-belleville` / `ch6-resonance` beside the reachable `ch06b` / `ch07` / `ch09`), three
  copies of *The Law of Monsters* in `AMonster/` with no `index.html` at all, and
  `book3/index.html` — Book III's own index has no way in.

# Orphan cleanup (2026-08-18)

Starting point: 636 HTML files, **59 unreachable** by the corrected breadth-first audit
(generated indexes excluded as link sources, per audit rule 1). Of those 59, seventeen were
never real problems — fifteen `index-*.html` files that *are* reachable through
`master-index.html`, and the two redirect stubs written earlier the same day. **42 real
orphans.** After this pass: **7**, and every one of the 7 is a competing variant, not a
stranded page.

## Retired (moved to `_to_delete/`, staged as deletions)

- **`book4/ch06b-elojo.html`, `ch07-newark.html`, `ch08-harrison.html`,
  `ch09-belleville.html`** — visible text byte-identical to the reachable
  `book4/ch06b.html`, `ch07.html`, `ch08.html`, `ch09.html`.
- **`chIV-correspondence-fixed.html`, `chIV-operators-fixed.html`,
  `chIV-recursion-fixed.html`** — root duplicates of the reachable `book4/chIV-*.html`,
  differing by eleven or twelve lines. Worth recording *what* those lines were, because the
  filenames say the opposite of the truth: the `-fixed` copies carry the **stranded
  Living Book / Series anchors**, and `chIV-correspondence-fixed.html`'s nav marks
  `chIV-recursion.html` as the current page. The book4 copies are the correct ones.
- **`AMonster/law-of-monsters-v2.html`** — byte-identical to `AMonster/MonstersLaw.html`.
- **`_cajueiro-index-misplaced.html`** — a third stale copy of the home page; its filename
  already said so.
- **All 14 `.bak` files that were tracked in git** and therefore published to GitHub Pages,
  including `book6/policy/SITE_ERRATA.md.bak` and a `.tex.bak` under `book8/notes/`.

## Given a way in

26 pages that had no inbound link from anywhere reachable are now listed in a curated
section at the foot of `series-hub.html`, grouped as *Edição IMPA · Portuguese chapters*
(including `gtct-index.html`, the Vol IV index, which nobody could reach), *Teaching ·
HIST 201* (the syllabus, the tutor deck, the proposal, and the three `book7/tutor-card-*`
hologram tutors), *Newark · Soundworks · taking part*, *Volumes and chapters not listed
above* (including **`book3/index.html`** — Book III's own index had no way in), and
*Editions & templates*.

This is a curated section in the hub, **not** a link to the generated dump. The distinction
is the one recorded above: `master-index.html` makes the number go down without taking any
reader anywhere.

**Result: 627 files, 604 reachable, 7 real orphans.**

## The 7 that remain — each is a variant, and each is the author's call

Every one has a reachable counterpart, so linking it would put two versions of the same page
in front of readers, and retiring it would destroy the only copy of whichever differences it
holds. Nobody has compared the texts.

| orphan | bytes | reachable counterpart | bytes | diff lines |
|---|---|---|---|---|
| `ch-tatiana.html` | 50,083 | `book7/ch-tatiana.html` | 66,032 | 263 |
| `Enceladus-zenodo.html` | 71,609 | `Enceladus.html` | 67,696 | 305 |
| `AMonster/MonstersLaw.html` | 48,410 | `AMonster/monsterlaw.html` | 56,693 | 169 (mostly a larger SVG) |
| `book4/ch6-resonance.html` | 48,304 | `ch6-resonance.html` | 51,936 | 96 |
| `GameTheory_Full_Pack.FIXED.html` | 142,962 | `GameTheory_Full_Pack.html` | 143,339 | 38 |
| `omega/pitch-soundworks-clinic.html` | ~16 K | `pitch-soundworks-clinic.html` | ~16 K | 24 |
| `omega/omega-point-v2-draft.html` | 89 K | `omega/omega-point-index.html` | — | draft of |

Note the shape of the trap in row 5: the file **named** `.FIXED` is the one the site does not
serve. Same pattern as the `chIV-*-fixed.html` files retired above, where the `-fixed` name
was also wrong. Do not resolve any of these by filename.

# FIXED: Chapter 7 (Topological Orthogenesis) — the anyon identification (2026-08-18)

`ch7-topological-orthogenesis.html` asserted, in the body and again in Theorem 7.1, that
**G = U ∘ F ∘ K ∘ C *is* a braid-group element**. It is not, and the error was not in G.

Vol I §3 gives the operators real signatures — `C : X → X_C` a Lipschitz projection,
`K : X_C → X_C` a curvature flow with α(s) = λ(κ* − κ)₊ and κ* = 1/foc, `F : X_C → X_F` a
corank-1 fold, `U : X_F → X` gradient descent on a Morse functional Φ — so
**G : X → X type-checks perfectly.** What Chapter 7 did was throw those definitions away and
re-gloss the four operators as *a channel assignment, a move, topological protection,* and
*universality*: a map, an event, a property and a theorem. Composability died there, not in
Vol I. Any future chapter that re-reads the chain in a new domain must carry the §3
signatures with it, or it will reproduce this exact failure.

**Withdrawn, with reasons stated on the page:**

1. **&ldquo;The Yang–Baxter relation is K written in the language of topology.&rdquo;** It is one of the
   two defining relations of Bₙ. It holds for every braid at every strand count,
   unconditionally. K is defined *by* a threshold — α is identically zero until κ reaches κ*.
   A relation that always holds cannot be an operator that only fires above κ*.
2. **&ldquo;Below K, all braids are equivalent.&rdquo;** B₂ ≅ ℤ is infinite; two 2-strand braids with
   different winding are already inequivalent, with no threshold anywhere.
3. **&ldquo;K fires when the strand count and fusion rules become rich enough that
   non-commutativity enters.&rdquo;** Non-commutativity of Bₙ is a fact about n ≥ 3 — a property of
   the group. The chapter's own later sections use K as a per-move selection rule
   (Ω_after > Ω_before + K*). One symbol was doing two incompatible jobs; only the second
   usage is retained.
4. **&ldquo;G is the physical content of that fabric.&rdquo;** Not available on the definitions above.
   What survives: the order in which threshold-crossing moves are committed is not
   recoverable from any local slice — the one property the chain and the braid group
   demonstrably share.
5. **The □ on the proof sketch**, per rule 3.

**Corrected rather than withdrawn:**

- Clause (2) said no measurement on a proper subset determines β. The true statement is about
  *local operators* failing to distinguish the degenerate fusion states; subset fusion
  measurements do return partial information.
- Clause (3) is now marked `[OPEN]` with its debt written out: to make it a theorem, exhibit
  X, X_C, X_F, n(s), κ* and Φ for a configuration space of n anyons. None exists.
- The universality clause asserted Bₙ is universal for TQC. Universality is model-dependent:
  Fibonacci braiding is universal (Freedman–Larsen–Wang), **Ising braiding is not** — Clifford
  only. The theorem quantifies over non-abelian anyons generally, so the clause covers only
  the universal models, and Google's 2023 experiment used projective *Ising* anyons.
- The &ldquo;six elementary braid moves&rdquo; box called τᵢ and ωᵢ generators. They act trivially on
  π₁ of the configuration space and contribute nothing to the braid word. σᵢ₋₁ is also not a
  fifth generator — the generating set is {σ₁,…,σₙ₋₁}, size n−1.
- The falsification test now specifies **Fibonacci** hardware: an Ising machine failing to beat
  a gate-based one falsifies nothing.

**New section — engineered order versus emergent order.** Every non-abelian anyon experiment
to date (Google 2023, projective Ising on a superconducting processor; Quantinuum, trapped
ions; Fibonacci braiding, Nat. Phys. 2024) builds the braid by applying unitary gates chosen
by the experimenter. In those systems &ldquo;the order of operations is physically recorded&rdquo; is
true by construction and tests nothing. The control case is emergent order: FQHE, where
anyonic braiding statistics were observed directly at ν = 1/3 in 2020 (Fabry–Pérot
interferometry; anyon collider), with non-abelian order at ν = 5/2 still open — half-integer
thermal Hall in 2018, and hedged time-domain-braiding evidence as of 2026-08-13
(arXiv:2608.12897, whose own abstract calls the evidence elusive).

This is the same move Olimpia Lombardi objects to in quantum chemistry: molecular geometry is
inserted by clamping the nuclei under Born–Oppenheimer, then recovered and reported as found.
The engineered anyon experiments reproduce that pattern one level down; the FQHE does not.
**That asymmetry — two impositions and one control — is a paper, and it is not a refutation of
Lombardi but a question about where her argument's boundary lies.** Any such paper must meet
the obvious counter head-on: the FQHE invariant is also read in, through the choice of
Chern–Simons effective theory.

# FIXED: the map/point confusion, swept (2026-08-18)

Chapter 7's braid-group error turned out not to be isolated. Sweeping the corpus for claims of
the form *"G is <something>"* and *"… = G"* surfaced 93 candidate files; almost all are correct
(*"G is a contraction"*, *"x* = G(x*)"*, *"G is a contactomorphism"* — all statements about a
self-map, all fine). Three carried the same underlying confusion as Chapter 7: **G is a map on
X; a point of X is not a map, and a map is not a point.**

1. **`book5/chV-banach.html`** wrote the volume-convergence claim as
   **`G⁵ = G(G(G(G(G)))) = x*`**. Three errors stacked: `G(G(…))` feeds G to itself when its
   argument must be a point of X; `G⁵` is the fifth *iterate*, a map, not a nested application;
   and the whole thing is then set equal to `x*`, a point. Now
   `G^∘5 = G∘G∘G∘G∘G`, with `x* = limₙ G^∘n(v₀)`.
   The decisive detail: **§2 of that same page already states Banach correctly** —
   *"a sequência x₀, G(x₀), G(G(x₀)), …"* — so the page contradicted itself, and the correct
   form was sitting two sections away.

2. **`ch8-nested-infinities.html`** had `G(G(G(…))) = G∞` and *"The surreal construction is G
   applied to G."* Now `G^∘n(v₀) → G∞`, and *G applied to its own output — not to itself*,
   which is what the surreal-day construction actually describes and what the rest of that
   paragraph already says. Note `G ∘ G` elsewhere on the page was always correct, and
   `G(G∞) = G∞` is fine provided G∞ ∈ X.

3. **`ch6-resonance.html`** defined G correctly and then slid: *"G is the learner … G is the
   practitioner … G is what a person becomes."* **The practitioner is x*, not G.** The corpus
   writes x* = G(x*) everywhere; the person is the fixed point, G is the process that produces
   one. Also corrected: *"it is what the sequence produces"* — the sequence produces x*, not G.
   And *"Resonance is not a metaphor for learning. It is the physical instance of the same
   operator structure"* is now stated as a reading and tagged `[MODEL]`, per rule 2.

**The pattern worth remembering.** Every instance had the correct statement nearby — the same
page, sometimes the same paragraph. The error is not ignorance of the definitions; it is
prose drifting off them while the mathematics stays put a few lines away. When re-reading the
chain in any new domain, carry the Vol I §3 signatures into the passage rather than glossing
the operators in that domain's vocabulary.

**Not fixed, deliberately:** `book4/ch6-resonance.html` still carries the pre-fix text. It is
one of the seven competing variants awaiting the author's decision (see the variant table
above); editing an orphan copy of a page whose fate is undecided would make that decision
harder, not easier. `book6/wp55-the-fixed-point.html` uses **G for the Gödel sentence**, an
unrelated symbol; not an error, but the collision is worth knowing about before any future
sweep matches on `G is …`.

# FIXED: `19117399` mislabelled as a series DOI (2026-08-18)

Author's ruling: **keep every link, fix the label.** The DOI resolves to a real record —
Principia Orthogona Vol I — so this was mislabelling, not misdirection, and no `href` needed
to change.

Measured first, because "roughly sixty files" was wrong. **182 occurrences**: 81 in
nav/footer/badges, 75 in prose, 26 in formal citations. And **74 of the 106 occurrences in
running text carry no "series" word at all** — bare Zenodo links with no false claim attached.
The real defect was ~32 strings.

**23 labels changed across 16 files, plus 2 in `AMonster/monsterlaw.html`.** "Series DOI",
"Series Root", "Zenodo series", "DOI (series)" → **"Vol I concept DOI"** / **"Vol I on
Zenodo"**. Every `href` verified byte-identical before and after, per file, by assertion in
the edit script.

## Three exclusions the sweep would otherwise have damaged

This is the same near-miss as the `master-index` anchor-label sweep, and it is now the third
time this pattern has appeared. **A repo that documents its own defects will contain correct
prose that matches the defect's search pattern.**

1. **`wp38-zenodo-metadata.md` line 17** is a fenced code block quoting the defective HTML so
   it can be corrected. Rewriting it would have deleted the instruction.
2. **`HVEH/proofs/index.html`** already reads *"Vol I concept DOI, resolves to current Vol I —
   **no single series DOI**."* That phrase is the denial. The sweep would have produced "no
   single Vol I concept DOI" — the opposite of true.
3. **`about-series.html`, `book6/wp02-alterna.html`, `book6/ZENODO-metadata-corrections.md`,
   `book6/policy/SITE_ERRATA.md`** all quote the mislabel in order to report it.

Also skipped: `HVEH/index.html` and `book7/jacobian-verification.html`, which were already
correct, and `GameTheory_Full_Pack.FIXED.html` + `AMonster/MonstersLaw.html`, which are among
the seven competing variants awaiting a decision.

**Why the AMonster files needed a second pass.** The label there is split across two anchors
in different parts of the page — a nav chip reading `Series` at line 231, and a footer reading
`Root DOI:` at line 807. Flattened to text they look like one string, "Series Root DOI:". The
positional sweep also required the label to sit *before* the DOI, so an anchor whose text
follows its own `href` was invisible to it. Fixed by hand.

## Still open

- **The 26 formal citations.** In a reference list the string is not a label but an assertion
  that the cited work lives at that DOI, and it does not — a reader resolving it gets Vol I v6.
  These need the correct version DOI per work, or the Zenodo community link where the referent
  really is the series. Not done here.
- **`collatz-engineering_1.html` has a stray `</p>`.** Pre-existing — confirmed present in
  `HEAD` before this change — not introduced by the sweep.

# Book II (2026-08-18)

Same shape as Book I, and one new discrepancy that needs the author.

## Fixed

1. **`book2/index.html` was byte-identical to `book2/vol2-contact.html`** — the directory
   index was a second copy of the paper, not an index. Rewritten as a real Book II index on
   the same template as `book1/index.html`: the text, the companions (toy model, dashboard),
   and a full ledger of the directory. It points at **`../vol2-contact.html`**, the root copy,
   which carries 13 inbound links against `book2/vol2-contact.html`'s 5.
2. **Book II's copy pointed at the wrong Volume I.** Five links — nav, TOC drawer, reference
   [1], the bottom button and the footer — went to `book1/vol1-mathematics.html`, the **April
   Second Edition**, while the canonical root copy of the same page points at
   `vol1-mathematics.html`, the **V4**. The two copies of Volume II were sending readers to
   two different Volume I texts. Repointed to V4.
3. **Reference [1] cited Vol I at `19117400`** — the v1 origin deposit — in both copies. Now
   cites **`21146416`, v6, current**, per the ruling. The entry also now names Version 4
   explicitly and keeps a pointer to the Second Edition, because it remains the only copy
   carrying the note on &ldquo;orthogenesis&rdquo;; repointing the links without that pointer
   would have removed the disclaimer from Volume II's path entirely.
4. **Stranded nav anchors** in both copies. Verified from the CSS rather than assumed: neither
   file has a global `a` rule or a `nav a` rule, only `.nav-links a`, so `Living Book` and
   `Series ↗` were rendering as default blue underlined links. Moved inside.

All three files parse with zero unclosed tags, zero stray closers, no duplicate ids, no dead
links.

## OPEN — which DOI is Volume II's?

`vol2-contact.html` cites **`10.5281/zenodo.20755436`** seven times — hero badge, nav, footer —
for a page whose eyebrow reads *Version 2a · 2026*.

The ISBN/DOI section at the top of this file says something different: *"Vol II ('Contact
Realization'): 10.5281/zenodo.19379473. Clean, single version, April 2026 — the one paper of
the four with an unambiguous standalone DOI."*

Both cannot be right. Either a Version 2a was deposited after April and this file's note is
stale, or the page cites the wrong record. This is the same shape as the V4/v6 question
settled for Volume I on 2026-08-18, one volume over, and it was settled there in one sentence
by the author. **Do not guess:** `19379473` appears nowhere in `vol2-contact.html`, and
`20755436` appears nowhere in this file, so whichever is wrong has been wrong consistently and
a sweep would propagate it. Zenodo's API and record pages are robots-disallowed from the
tooling here; resolve it by opening the record.

# Book III (2026-08-18)

Two files: `index.html` and `vocab-seismic-geometry.html`.

## Fixed

1. **Wrong Volume I and Volume II targets, seven links.** `book3/index.html` sent four links to
   `book1/vol1-mathematics.html` (the April Second Edition) and three to
   `book2/vol2-contact.html` (the non-canonical copy). Repointed to `../vol1-mathematics.html`
   (V4) and `../vol2-contact.html` (13 inbound against book2's 5). This is the third volume
   index in a row carrying the same defect — books I, II and III all pointed backwards.
2. **`ISBN 979-8-9954416-6-3 (series)`, twice.** That number is allocated to **Book 3 ·
   Mini-Beast · eBook PDF** — it is not a series ISBN, and this file's own rule is that a
   volume without its own registered ISBN gets *no* ISBN line rather than a borrowed one.
   Labelling Book 3's number "(series)" is an invitation to stamp it on other volumes, which
   is exactly how the borrowed-ISBN defect spread the first time. Now reads
   `(Vol III · eBook)`. The number itself was correct and is unchanged.
3. **A nav chip reading `Series Zenodo` pointed at `10.5281/zenodo.19117399`** — Vol I's
   concept DOI, on a Book III page. Doubly wrong: it is not a series DOI, and Book 3 has no
   standalone deposit of its own. Repointed to the **Zenodo community**, which is the correct
   series-wide target per the ISBN/DOI section above. Note this one survived the 2026-08-18
   relabel sweep because the label is the anchor's *text*, which follows its `href` — the same
   blind spot that hid the AMonster labels.
4. **Stranded nav anchors** in `index.html`. In `vocab-seismic-geometry.html` the nav is a
   `<ul class="nav-links">`, so `Series ↗` was stranded outside the list rather than outside a
   div; wrapped in an `<li>` and moved inside, and a link to the Vol III index added, since
   that page previously offered no route to its own volume index.

*Detector note:* the stranded-anchor scan reported five stray anchors in
`vocab-seismic-geometry.html`. There is one. The scan slices after the last `</div>` in the
nav block, and that nav contains no `</div>` at all, so `rfind` returned −1 and it counted
nearly the whole block. Any future run of that check must handle the `<ul>`-based navs.

## Open

- **Two Book III hubs.** Root `vol3-minibeast.html` (38,803 bytes, 5 inbound) and
  `book3/index.html` (38,590, 2 inbound) are near-copies. The 111-line diff between them is
  **entirely link targets** — the drift *was* the wrong-Volume-I/II problem now fixed — plus
  one line, the `vocab-seismic-geometry.html` entry, which only the book3 copy carries. So
  they are the same page with different destinations, not two texts. Unlike Books I and II,
  `book3/index.html` was **not** replaced with a short index: the root copy is a hub rather
  than a paper, so there is no separate "text" for an index to point at, and collapsing them
  is an editorial decision about which filename the volume should live at.
- **`ch6-cardiac.html` is still dead** — linked from `book3/index.html`, no such file anywhere
  in the repo. Already on the dead-link list above; unchanged, since it needs either the file
  or a decision to drop the link.

## Staleness check across the volume set (2026-08-18)

Ran the obvious verification after the Book III pass: does anything still link to a
non-canonical copy? Eleven links did, in three files the volume work had not touched.

| file | links | was pointing at | now |
|---|---|---|---|
| `book1/vol2-dashboard.html` | 5 | `book1/vol1-mathematics.html` (2nd ed) | root `vol1-mathematics.html` (V4) |
| `book1/vol1-mathematics.html` | 5 | `book2/vol2-contact.html` | root `vol2-contact.html` |
| `book4/logs-segment.html` | 1 | `book1/vol1-mathematics.html` (2nd ed) | root `vol1-mathematics.html` (V4) |

The second row is the one worth noticing: the **archived Second Edition** was sending readers
on to the non-canonical Volume II. An archived page should still hand off to current
companions — being superseded is not a reason to strand the reader one level deeper.

**Six links to non-canonical copies remain, and all six are deliberate:** three ledger rows and
the &ldquo;kept for the record&rdquo; entry in `book1/index.html`, one ledger row in
`book2/index.html`, and the pointer inside reference [1] of both Volume II copies naming the
Second Edition as the only text carrying the orthogenesis note. Those must not be swept —
they exist precisely to describe the non-canonical files.

Book III itself is now clean: every link resolves to a canonical file, and the only dead link
is the pre-existing `ch6-cardiac.html`.

# CORRECTION: the unit-distance exponent is 1.014, not 10⁻³⁸ (2026-08-18)

`book7/ch-erdos.html` was written yesterday around the figure the nine-author *Remarks* note
computes explicitly, **1 + 6.24 × 10⁻³⁸**, and concluded that "the true growth rate is exactly
as unknown as it was in 1984." **That understated the result and is corrected.**

That figure is an illustration, not the theorem. The note picks *T* = {3,5,7,11,13,17} and
*S* = {101,∞} — its own words, *"as just one small example"* and *"for simplicity"* — and says
of the class-number bound it uses that it is *"not optimal but suffices."* Optimised, the same
construction does vastly better: **Will Sawin, *An explicit lower bound for the unit distance
problem*, arXiv:2605.20579, 20 May 2026, proves more than n^1.014.**

So the honest statement is: the lower bound moved from Erdős's n^(1+Ω(1/log log n)) to
n^1.014, the Spencer–Szemerédi–Trotter ceiling still sits at O(n^4/3) ≈ n^1.333, and the truth
between 1.014 and 1.333 is unknown. Sawin's paper is now cited in the chapter's references.

**And a check that failed.** I reported to the author that `book5/chV-erdos-machine.html` had
"zero mentions" of the unit distance result and was stale. It was not. That chapter is in
**Portuguese** — *"Problema das distâncias unitárias no plano (Erdős, 1946)"* — and it already
carried the correct δ = 0.014 and credited Sawin, while the English chapter I had just written
carried the weaker figure. The grep was English-only. **In a bilingual corpus, a
single-language search is not a search.** Any future staleness sweep must cover the Portuguese
terms too, or it will keep reporting the translated chapters as missing content they contain.

# Book V and Book III (2026-08-18)

**Book V is the cleanest volume audited.** Zero dead links across twelve files. `nav.js` builds
the nav in JavaScript for the whole volume and every one of its twelve chapter entries resolves
to a real file. Its single ISBN mention is not a defect but a *correction note*, in Portuguese,
recording that the fallback rule was withdrawn on 2026-08-12 and that 979-8-9954416-5-6 is
unallocated reserve — it must not be swept. Zenodo references are the community link and two
version DOIs (19162012, and 21431505 for the kernel-checked commutation work). Nothing changed.

**Book III: the author confirms the volume lives at the root file.** `book3/index.html` is now a
real index on the Book I/II template, pointing at `../vol3-minibeast.html` for the text and
keeping `vocab-seismic-geometry.html`, the Brazilian edition and the pilot. It was 38,615 bytes
of near-duplicate; it is now 8,945 bytes of index. The duplicate-hub question recorded above is
closed.

# Storefronts relabelled as preprints (2026-08-18)

Author's ruling, in his words: *"too early to be marketing it, books aren't ready"*, then
*"forthcoming is okay — anyone buying anything right now is buying preprints"*, and *"stale html
and pdfs"*. So the fix is honesty in the listing, not deletion of the listing.

**Changed in `book4/ch02.html`, `book4/ch10.html` and `livro3-brasil.html`:**

- The three unallocated/HOLD ISBNs (2-5, 4-9, 5-6) are gone from the product cards, replaced by
  **"Preprint · ISBN on publication"** / **"Pré-publicação · ISBN na publicação"**. A preprint
  does not carry the volume's ISBN, and these numbers were never allocated to these works.
  Book 3's own **6-3** stays on the Mini-Beast card — it is correct and that product is real.
- Each grid gained a line stating what a purchase actually delivers today: the working text,
  HTML and PDF, revised as the series revises; volumes forthcoming; ISBNs assigned on
  publication.
- `livro3-brasil.html`'s Vol G⁴ card cited **DOI 10.5281/zenodo.19117400** — Vol I's v1 deposit,
  not Vol IV's. Replaced with the Zenodo community link.
- Prices and Gumroad links left as they are. That was the instruction, and it is now accurate:
  the page says preprint and sells a preprint.

## What the Gumroad audit actually found

**Every Gumroad link in the corpus — 86 of them across 43 files — points at one product,
`/l/soundworks`**, under two different accounts (`g6llc.gumroad.com` and
`brodanova6.gumroad.com`). That includes the buttons labelled *"Buy Book 3 on Gumroad"*,
*"Comprar — $15"*, *"All volumes →"* and *"Complete Series"*. **The book-buy buttons do not lead
to books.** 38 links carry book-purchase language; 22 are membership/Soundworks; the rest are
bare "Gumroad".

Two accounts for one product is its own problem — pick one. Nothing outside the three
storefronts was touched, because most of those 43 files link the membership rather than a book.

## OPEN — an IMPA claim to check before it matters

`book4/ch02.html`'s Vol G⁴ card reads *"GTCT T1 — The IMPA Edition … Submitted to IMPA."*
Separately, **"Edição IMPA" / "IMPA Edition" appears 209 times across 45 files**, and no
affiliation disclaimer was found anywhere in the corpus.

IMPA is a real institution with its own imprint. Used at that volume, the phrase reads as an
imprint credit rather than a description of intent or of a course edition. If the work has not
been published or endorsed by IMPA, this is the kind of thing that is cheap to correct now and
expensive later — precisely if a genuine IMPA submission is ever made. Worth one deliberate
decision about the wording, not 45 separate ones.

# "Edição IMPA" renamed to "Edição Brasil" (2026-08-18)

Author's reason, in his words: *"we wannabe worthy of IMPA, MIT etc."* — which is an argument
for **not** wearing the name yet.

**163 occurrences renamed across 47 files.** `Edição IMPA` → `Edição Brasil`,
`IMPA Edition` → `Brazil Edition`, plus the `&ccedil;&atilde;` entity variant and the
`The IMPA Edition` form. Every `href` verified identical before and after, per file, and every
file's parse compared against `HEAD` — 53 files checked, zero deltas. Generated indexes
regenerated so their cached titles follow.

**Why the rename and not a disclaimer.** IMPA has its own imprint. As an *edition name* on the
volume, "Edição IMPA" reads as a publisher credit — the same grammatical slot as "Penguin
Edition". A disclaimer buried on one page does not undo a label repeated 163 times in titles,
footers and nav bars. "Edição Brasil" says what the edition actually is: the bilingual PT/EN
Brazilian edition of Vol IV, which is exactly how the surrounding text already describes it
(`· Edição Brasil · Bilíngue PT/EN · GTCT T1`).

**What was deliberately NOT changed: `Submetido ao IMPA` / `Submitted to IMPA`**, in 14 files
(`ch-curie`, `ch-dirac`, `ch-hawking`, `chIV-preface`, `HVEH/ch02`, four `book6` chapters, and
the four `book7` copies whose strips read *"originalmente Vol IV, submetido ao IMPA"*).

That distinction is the whole point. **An edition name claims who published it; "submitted to"
claims only what the author did.** The first is a credit that has to be earned; the second is a
fact about an action. It stands if it is true — and it should be checked, because it is the one
IMPA statement left in the corpus. If nothing was ever actually sent, it needs to go the same
way the edition name did.

Filenames are untouched: `impa-portal.html`, `impa-working-paper.html`, `impa-masters-phd.html`
keep their names, and `impa-masters-phd.html` is straightforwardly *about* studying at IMPA,
which is fine.

# IMPA: submitted, declined, and what they actually asked for (2026-08-18)

**The submission was real and IMPA replied.** Their answer, as the author reports it: it is not
the kind of book they publish, and what would work is **a book for a class they teach** —
matching their size, style and digestibility.

That is not a rejection of the mathematics. It is a format specification, and it is a usable one.

**17 stale labels cleared across 17 files.** Footer strips reading
`· Vol IV · Submetido ao IMPA · Newark NJ · 2026` (and the `Vol VI`, `G⁴`, and
`originalmente Vol IV, submetido ao IMPA` variants, plus a product card reading
*"Submitted to IMPA"*) implied a submission still under consideration. It has an outcome now,
so the clause is gone; the strips read `· Vol IV · Newark NJ · 2026`. **The claim was true when
written — it went stale, which is the defect class this whole audit has been chasing.** No
`href` changed; indexes regenerated.

## What IMPA's own catalogue says, for whoever picks this up

IMPA publishes through, among others: **Projeto Euclides**, **Coleção Matemática
Universitária**, **Coleção Matemática e Aplicações**, **Monografias do IMPA**, **Publicações
Matemáticas**, and the **Coleção Colóquios Brasileiros de Matemática**. Their publisher page
describes the works as arising from *"research, courses, seminars or scientific meetings."*

The series matching their feedback most exactly is the **Colóquio minicourse notes**: short
books written to accompany a course actually taught at the Colóquio Brasileiro de Matemática,
sized to be worked through in a week. **The 35th Colóquio ran 27 July – 1 August 2025 at IMPA,
and it is biennial — so the 36th falls in 2027**, which is the realistic target and leaves
enough lead time to write to the format rather than retrofit.

The corpus already has the raw material for exactly this shape — a one-week course with a
narrow spine, not a multi-volume framework. Contact `coloquio@impa.br` for the call and
deadlines; the 2025 cycle published its deadlines as a PDF in February of the event year.

**Do not restore any IMPA edition name or submission label on the strength of a future
submission.** Both were removed today for the same reason: a label has to describe something
that has already happened.

# RESOLVED (stale ledger entry): WP-38's "two broken formulas" (2026-08-18)

The triage list above states: *"**Two broken formulas** remain in Figures 1–3
(`data-mjx-error="Misplaced &"` — matplotlib mathtext choking on a literal `&`)."*

**They are not broken. They were fixed and the ledger was never updated.**

Both `data-mjx-error="Misplaced &"` occurrences in `book6/wp38-positional-dominance.html` sit
**inside HTML comments** (character ranges 474099–474901 and 483228–484006). They render
nothing. Immediately after each comment closes there is live SVG path data using embedded
DejaVu glyph outlines — `DejaVuSans-2202` (∂), `DejaVuSans-3e` (>), `DejaVuSerif-28` — i.e.
the mathematics is now drawn as vector outlines instead of being handed to MathJax. Whoever
fixed it commented out the failing render rather than deleting it, which is good practice and
left the search string behind.

**Repo-wide check: zero live `data-mjx-error` anywhere.** 638 HTML files scanned, comment-aware.
The only two occurrences are the commented pair above.

This is the ledger's own failure mode, described in rule 6 of "Rules for anyone fixing these":
*"a future session will trust this table; leaving it stale recreates the original problem in a
new place."* It cost this session a figure-rendering investigation to discover the work was
already done. **When a triage item is settled, strike it here in the same commit.**

## Book VI audit, same pass — clean

122 files. **Zero dead links. Zero links to non-canonical copies. Zero unstyled stranded nav
anchors.** Its three ISBN mentions are all *correction notes*, not defects, and must not be
swept: `g6-crystal.html` states in both languages that Vol VI has no allocation of its own and
that 979-8-9954416-5-6 is unallocated reserve and not a fallback; `wp02-alterna.html` records
that a Zenodo record wrongly claims Book 3's 979-8-9954416-6-3.

Still open for Book VI, unchanged and untouched here: the `c_K` discrepancy `[OPEN]` (inverting
σ* = 0.33 gives c_K = 0.669, b = 44.6 against v2's b = 1.208 — a factor of ~37); Otium existing
in both WP-38 §9 and a separate unpublished deposit; and WP-02's Zenodo metadata carrying the
wrong ISBN and a phantom series DOI, which is the author's call per rule 4.

## Sweep: Book VI and Book VII (Aug 2026)

Standard battery run over `book6/` (99 HTML) and `book7/` (52 HTML): dead links, non-canonical
copies, stranded anchors (CSS-verified), ISBN/DOI misuse, index integrity, HTML parse.

### Fixed

| File | Defect | Fix |
|---|---|---|
| `book6/index.html` | WP-13 row pointed at `../../banking-butterfly-preprint.html` → `totogt.github.io/banking-butterfly-preprint.html`, **404** | `../banking-butterfly-preprint.html` — the file is in *this* repo's root; one `../` too many. Five other files already link it correctly. |
| `book7/ch-huh.html` | `../applications/stjohns-meco/aula-index.html` — no `applications/` directory exists anywhere in the repo, and the only reference to it is this one link | Retargeted to `../../AXLE/AULA/103/dm3-courses-101-102-103.html` (AULA 101/102/103 course landing, tracked on AXLE `main`) — matches the row's own description, "the lesson programme itself — AULA 101 / 102 / 103 against CEFR" |
| `book6/ir-animal-nutrition.html` | 2 stray `</p>` (lines 218, 320) closing nothing inside `div.gate` — one EN, one PT | Removed |
| `book6/wp43-immediate-action.html` | Markdown `**` leaked into HTML: `<strong>Deploy ceilometer networks … in vulnerable regions.**` | `**` → `</strong>` |
| `book6/wp38-positional-dominance.html` | 3 `<b>` opened inside table cells, never closed before `</td>` (WTI settle, Waha peak, Panama slot auction) | `</b>` inserted before each `</td>` |
| `book6/1`, `book7/1` | 1-byte files named `1` — shell redirect artifacts (`> 1`) | Moved to `_to_delete/stray-numeric-files/` |

### Verified live, not defects

`book6/index.html` → `../../AXLE/GameTheory_Full_Pack.html` and `../../AXLE/lexical-generativity-ijl.html`
both resolve on the live site. Cross-repo links out of `geometry` into `AXLE` are legitimate;
the auditor flags them as "escapes repo" and that flag is not a finding by itself.

### Not fixed — needs a decision or lives in another repo

1. **`book6/wp65-the-oracle-outside.html` → `../../AXLE/chGal-galois.html` is 404 live.**
   The link is *correct*; the file is tracked in the AXLE repo but only on the branch
   `chapter-gal-galois`, which is 1 commit ahead of its remote and **never merged to `main`**.
   Pages serves `main`. Two of the chapter's links and one table row depend on it. Fix belongs
   in AXLE: merge the branch, or the three references stay dead.
2. **Same two ISBNs used across two volumes.** `979-8-9954416-5-6` appears in
   `book6/g6-crystal.html` and `book7/ch-huh.html`; `979-8-9954416-6-3` appears in
   `book6/wp02-alterna.html` and `book7/wp59-dark-matter-lensing.html`. This is the registry
   `1-8` "default ISBN for any volume without its own" note biting — an ISBN identifies one
   edition of one title, so a shared default is not a placeholder, it is a wrong identifier.
   Author's call.
3. **Six `.md` in `book6/` with no `.html` counterpart:** `COHN_revision_plan_immune.md`,
   `OPENING_NOTE.md`, `ZENODO-metadata-corrections.md`, `wp38-math-supplement.md`,
   `wp57-one-animal-four-operators.md`, `wp58-the-recorder.md`. The last two are numbered
   working papers with no published page — WP-57 and WP-58 exist only as source.

### Known-benign — do not re-flag

`book6/wp38-positional-dominance.html` reports duplicate ids (`figure_1`, `patch_1`, `axes_1`,
`matplotlib.axis_1`, `xtick_1`). Three matplotlib-emitted inline SVGs share structural `<g id=…>`
names. **Every `clipPath` id is unique** (matplotlib hashes those) and nothing references the
duplicated ids via `url(#…)`, so rendering is unaffected. Cosmetic only.

### Auditor caveat recorded

The reachability resolver reports a bare `href="../"` as dead. It is not: `os.path.join(".", "index.html")`
yields `./index.html`, which does not match the normalized `index.html` in the file set. Normalize
the joined path before the membership test, or `book7/index.html` and `book7/Polylaminin.html`
will be flagged on every future run.

## Sweep: HVEH, omega, AMonster, Orthogenesis (Aug 2026) — the series tail

Standard battery over `HVEH/` (26 HTML + 1 extensionless), `omega/` (43), `AMonster/` (2),
`Orthogenesis/` (1): dead links, non-canonical copies, stranded anchors, ISBN/DOI misuse,
index integrity, HTML parse. **Orthogenesis is clean.** The other three are not, and what they
have in common is duplicates: every real finding below is either a stale copy that a repair
pass missed, or a file nobody can reach.

### Fixed

| File | Defect | Fix |
|---|---|---|
| `HVEH/ch02.html` | **The fourth storefront.** Same product grid as `book4/ch02.html`, carrying the three unallocated/HOLD ISBNs (2-5, 4-9, 5-6) as though allocated. The 2026-08-18 storefront pass fixed three files and missed this one | `Preprint &middot; ISBN on publication` on all three cards, plus the same preprint-disclosure paragraph, byte-identical to `book4/ch02.html`. **It was the last storefront in the repo carrying those numbers** |
| `HVEH/ch02.html` | References [1] and [2] cite `ISBN 979-8-9954416-2-5` for Vol I and `979-8-9954416-4-9` for Vol II. 2-5 is unallocated reserve; **Vol II has no allocation at all** | Both ISBNs dropped. The DOIs stay — they are correct and were checked against the Zenodo API |
| 11 files in `HVEH/` | Provenance footer reads `Principia Orthogona &middot; Principia Orthogona &middot; HVEH` — the volume slot got filled with the series name. Every other section reads `Principia Orthogona &middot; Vol N &middot; <name>` | `Principia Orthogona &middot; HVEH`. HVEH is a project track, not a numbered volume |
| `HVEH/index.html`, `HVEH/proofs/index.html` | Punctuation debris left by the DOI relabel: `…20360288</a>;\n ), Five works…` — a semicolon before a closing paren, then a sentence starting mid-clause | Paren closed, sentence started. No link touched |
| `omega/space-of-possibility.html` | Footer asserts `ISBN 979-8-9954416-5-6` for Book Ω. 5-6 is unallocated reserve; Book Ω has no allocation | ISBN line dropped, Zenodo community link kept. This is the standing rule: *a volume without its own registered ISBN gets no ISBN line at all* |
| `omega/omega-point-index.html` | "Full Status Audit" button → `OMEGA_STATUS_AUDIT.md`. **That file has never existed in the repo's history** — not present, not deleted, never committed | Button removed. There is no honest substitute: `omega/SPINE-omega-point.md` is the book's editorial spine, not a status audit, and retargeting to it would be the same mislabel this audit exists to catch |
| `AMonster/MonstersLaw.html` | Two Tier-A phantom labels on Vol I's concept DOI — nav `<a …19117399>Series</a>` and footer `Root DOI: 10.5281/zenodo.19117399` | `Vol I on Zenodo` / `Vol I concept DOI: …`, matching the corrected `monsterlaw.html`. Commit `a7f22d6` ("Relabel 19117399: it is Vol I's concept DOI") fixed the lowercase copy and never saw this one |
| `omega/1`, `HVEH/places/1`, `HVEH/proofs/1` | 1-byte `> 1` shell-redirect artifacts, same class as `book6/1` and `book7/1` | Moved to `_to_delete/stray-numeric-files/` |

Every edited file was diffed against `HEAD` by parsed tag sequence and by sorted `href` set:
16 files, zero unintended href changes, zero title changes (so no index regeneration needed),
and the only structural deltas are the two tags added for the preprint paragraph and the one
anchor removed with the dead button.

### Verified live, not defects — do not re-flag

- **Every Zenodo DOI cited in these four sections resolves and matches its label**, checked
  against the API: `20561165` = *The Law of Monsters* · `20320693` = Vol I (a version under
  concept `19117399`) · `20360288` = GTCT · `20682934` = *Contact-Geometric Theory…* ·
  `21146416` = Vol I v6.
- `979-8-9954416-6-3` on both AMonster pages **is correct.** Both are labelled
  *Principia Orthogona · Vol. III · Chapter: Ocio*, and 6-3 is Book 3's own registered eBook
  ISBN. It is the one ISBN in this sweep that should stay.
- `HVEH/index.html` and `HVEH/proofs/index.html` label `19117399` as *"Vol I concept DOI …
  there is no single series DOI"*. Already Tier-C correct.

### Not fixed — needs a decision

1. **`HVEH/proofs/` is eight stale copies, and the hub links them instead of the maintained
   set.** `HVEH/{index,operator-algebra,distribution-theory,catastrophe-theory,contact-geometry,
   spectral-markov,numerical-constructive,information-geometry}.html` each exist twice, once at
   `HVEH/` and once at `HVEH/proofs/`. Commit `2ef1664` ("series-wide provenance footers:
   307/307") added footers to the `HVEH/` copies only — **the `proofs/` copies were invisible to
   it, so 307/307 was 307 of the files the pass could see.** `HVEH/index.html`'s own navigation
   points at `proofs/`, so a reader who lands on the hub gets the footerless set. Pick one
   location; the other should go.
2. **`omega/` carries seven orphaned stale copies of root pages** — `journey.html`,
   `omega-point-index.html`, `omega-point-sample-logos.html`, `pitch-soundworks-clinic.html`,
   `trinity.html`, `trinity-son.html`, `trinity-spirit.html`. **Nothing hand-links any of them**;
   they are reachable only through the generated indexes, which enumerate every file. The root
   copies are the ones `series-hub.html`, `chapters-diagram.html` and the trinity pages point at.
   One of the seven is actively embarrassing: **`omega/pitch-soundworks-clinic.html` has the site
   name blanked out of a capital-campaign pitch** in three places — *"A phased capital campaign
   for ."*, *"Acquire and stabilize ; basic build-out…"*, *"ending at ."* A find-and-replace
   removed "Forest Hill" and left the punctuation. The root copy is intact.
3. **There are two live Omega Point indexes and they got different halves of the repairs.**
   `omega-point-index.html` (25 KB, root) has no Gallery, no Ancient Transmission, no Status
   section; `omega/omega-point-index.html` (47 KB) has all three. The DOI-footer sweep
   (`2320bd0`) hit only the root copy; the provenance-footer pass (`2ef1664`) hit only the omega
   copy. Hand-written nav points at root; `omega/index.html`'s `<link rel="canonical">` and its
   meta-refresh point at the omega copy. Decide which is the volume, then delete the other —
   this is the clearest case in the repo of why two copies cost more than they save.
4. **Two pages' worth of unique content are buried in unreachable files.**
   - `omega/omega-point-v2-draft.html` is **three complete HTML documents concatenated** (three
     `<!DOCTYPE>`, three `<html>`, three `<body>`): two Omega Point index drafts with an
     unrelated page sandwiched between them — *"Clay Energy — an open archaeology of unread
     tablets"*, which **exists nowhere else in the repo**. Marked `data-orphan="1"`.
   - `HVEH/index` — **no file extension**, 51 KB, committed as "Create index", linked from
     nothing. Also two documents: *"Atratores — Pablo Nogueira Grossi"*, which **exists nowhere
     else in the repo**, and a stale copy of the G6 Opus Map. Pages will serve an extensionless
     file as a download, not a page.
5. **`AMonster/MonstersLaw.html` and `AMonster/monsterlaw.html` are divergent drafts** of the
   same chapter differing only in filename case — 48 KB vs 57 KB, 155 differing lines, different
   SVG geometry. The case difference is why the relabel pass found one and not the other; on a
   case-insensitive checkout they cannot both exist. Only `series-hub.html` hand-links either
   (it picks `monsterlaw.html`).
6. **`dm3-lab-index.html` (root) has an ISBN table** listing 2-5, 4-9 and 5-6 against G¹, G² and
   G⁵. Same unallocated numbers, same defect as the storefronts, different construct — left
   alone because it is outside this sweep's four sections.
7. **`impa-portal.html` is not an IMPA portal.** It is the *"Seven Sound Machines"* Soundworks
   page; its only two mentions of IMPA are links *out* to `AXLE/impa-portal.html`. **121 files in
   this repo link it, including the site root `index.html`.** The 2026-08-18 IMPA pass
   deliberately kept the filename on the grounds that the page was *about* IMPA. Nobody opened
   it. Same defect class as everything above — a label describing something that isn't there.
8. `AMonster/Files.md` is a pasted chat transcript, not a document.

### Auditor caveats recorded

- **`href="/geometry/…"` absolute paths are correct, not dead.** Pages serves this repo at
  `totogt.github.io/geometry/`, so the leading `/geometry/` is the site base. There are **896 of
  them and all 896 resolve.** Strip the `/geometry/` prefix before the membership test or
  `omega/pitch-soundworks-clinic.html` gets five false hits on every run.
- **Tag-balance checking does not catch concatenated documents** — each document is internally
  balanced, so the stack comes out clean. Count `<!DOCTYPE` per file instead; that is what found
  both buried pages above.
- **Counting `<!DOCTYPE` false-positives on doctypes inside JS template literals.**
  `impa-portal.html` reports two; the second is inside ``const html=`<!DOCTYPE html>…` `` — a
  page generator, not a defect. Check whether the match sits inside a backtick string.
- The `href="../"` normalization bug recorded in the Book VI/VII sweep is still unfixed and
  still produces false positives.

# The five open items from the HVEH/omega/AMonster sweep — closed (Aug 2026)

All five were worked in one pass. What follows is what changed, what was *wrong in the
previous entry*, and what is newly open.

## CORRECTION to the entry above: there IS an IMPA portal, on DM3-lab

The entry above says *"`impa-portal.html` is not an IMPA portal"* and implies none exists.
**That was half right and the missing half matters.** Checked live:

| URL | HTTP | Title |
|---|---|---|
| `totogt.github.io/DM3-lab/impa-portal.html` | 200 | **IMPA Edition — Purchase Portal · Principia Orthogona** (25 KB) |
| `totogt.github.io/AXLE/impa-portal.html` | 200 | dm³ Soundworks · Chladni · Sacred Resonance (272 KB) |
| `totogt.github.io/geometry/impa-portal.html` | 200 | dm³ Soundworks · Chladni · Sacred Resonance (272 KB) |

So the real purchase portal is alive on **DM3-lab**, and the AXLE and geometry copies were
**overwritten** at some point with the Seven Sound Machines page. Two of three copies clobbered,
and this repo's copy is one of them. Note also that the surviving real one still carries
*"IMPA Edition"* in its title — the edition name withdrawn here on 2026-08-18. That is another
repo; rule 4 applies.

**Do not "restore" geometry's copy from DM3-lab on the strength of this note.** Which page
should be this repo's store is the author's call. What was fixed is only the *labelling*.

## 1 · impa-portal labels — 117 rewrites, 0 hrefs touched

`geometry/impa-portal.html` does carry the purchase apparatus (4 Gumroad links, 5 PayPal links
including the exact `$213.24` eBook and `$263.36` hardcover amounts the storefronts quote), so
it functions as a purchase portal. Only the word IMPA was untrue.

- **84 anchor texts** on links to `impa-portal.html`: `IMPA Portal`→`Purchase Portal` (28) ·
  `IMPA`→`Purchase` (26) · `Portal IMPA →`→`Portal de Compras →` (21, all on `lang="pt"`
  Edição Brasil pages) · `⬡ AXLE Portal`→`⬡ Purchase Portal` (5) · plus 4 one-offs.
- **31 non-anchor labels**: `AXLE · IMPA Portal`, `via the IMPA portal`, `Open the IMPA portal`,
  the two `g6-opus-map.html` node labels, and 16 loose `IMPA Portal` strings.
- **2 individually judged**: `chapters-diagram.html`'s card title `IMPA Purchase Portal` →
  `Purchase Portal`; `livro3-brasil.html`'s `Portal IMPA (revisores)` → `Portal de Compras`.

**Deliberately not changed:** `chapters-diagram.html`'s *"IMPA Portal — Patch"* card. It names
the real file `_archive/impa-portal-patch.html`; it is a note about an artifact, not a claim
that a portal exists. And **every filename stays**, per the 2026-08-18 precedent.

**`⬡ AXLE Portal` was relabelled, not repointed.** There is no AXLE portal in this repo —
`portal.html` is the *Student* Portal. Relabelling states what the target is; repointing would
have been a guess about intent. If the intent was the AXLE site, that is a five-file change.

## 2 · omega/ — seven orphans retired, and a trap worth remembering

Retired to `_to_delete/superseded-copies/omega/`: `journey.html`,
`omega-point-sample-logos.html`, `pitch-soundworks-clinic.html`, `trinity.html`,
`trinity-son.html`, `trinity-spirit.html`, **and `trinity-father.html`** — the seventh turned up
during the work: it is byte-for-byte the same page as root `trinity.html` (same title *"The
Father — Genesis"*, same headings), just under a second filename. Root `trinity.html` **is** The
Father; the triptych was never missing a panel.

Before retiring, the one thing the omega copies had that root did not was carried over: the
three root `trinity*.html` files now read `Principia Orthogona · Vol IX · Omega Point` instead
of the generic `· totogt.github.io/geometry`.

**The trap, recorded because it nearly shipped:** the inbound-link check searched for
`href="omega/<file>"` and reported zero. It was wrong twice. `chapters-diagram.html` and
`series-hub.html` *did* link `omega/trinity.html` — caught by a second assertion. And 26 more
links inside `omega/` referenced the copies by **bare relative name** (`href="trinity.html"`),
which no `omega/`-prefixed pattern can match; those only surfaced when the auditor reported 32
new dead links *after* the move. All 26 were repointed to `../`.
**Before moving a file, resolve every link in the repo and check whether it lands on that file.
Do not pattern-match the path you expect callers to have written.**

## 3 · HVEH/proofs/ — the worst thing in the sweep

The eight `HVEH/proofs/` copies are gone; `HVEH/index.html`'s seven links now point at the
maintained set beside it. The seven proof pages were a clean call — `HVEH/` is a strict superset,
zero lines existed only in `proofs/`.

`HVEH/proofs/index.html` was **not** just a footer difference. It predates commit `ea2a64e`
("MODEL-tag engineering claims; retire expired grant/World Cup dates"), so the copy the hub
actually linked still said:

- *"reducing flood peaks by 20–50%"* — where the maintained copy says *"a modeled 20–50%
  flood-peak reduction … **[MODEL — not yet built.]**"*
- *"seven independent mathematical proofs **validating design claims**"* — vs *"proofs of the
  operator framework (model-level) … the engineering design targets are modeled, not yet
  validated by a built prototype"*
- *"The FIFA World Cup Jersey Fan Hub … **is open for 39 days** … Forecasters **flag active**
  flash flood risk"* — present tense, for a window that closed in July.

**A page written for grant reviewers was making unqualified engineering claims about an unbuilt
device, and it was the copy on the linked path.** This is the strongest argument in the repo for
the no-duplicates rule: the honesty pass ran, and landed on the copy nobody reads.

## 4 · The two buried pages — one real, one not

- **Clay Energy is real and is now published** as `omega/ch-clay-energy.html` — a complete essay
  (*"The tablets are already digitized. Almost no one has read them."*) on CDLI, ORACC, the
  Electronic Babylonian Library and ETCSL, with a five-step how-to. Verified 404 at every
  plausible URL beforehand, so nothing was being duplicated. Three of its four archive links
  return 200; ORACC's host could not be reached from the container, but `http://oracc.org/`
  301s to it, so the URL is canonical and only the scheme was stale (now `https`). It carries
  its own disclaimer — *"Not affiliated with CDLI, ORACC, the Electronic Babylonian Library, or
  the University of Oxford"* — which is the standard this repo is trying to hold. Linked from
  `omega/ch-here-comes-everybody.html` and from the Ancient Transmission section of the index.
- **Atratores was not buried content.** `HVEH/index` (extensionless, 51 KB) is a **stale copy of
  a live site's homepage**: `grossi-ops.github.io/Atratores/` returns 200 at 34.4 KB with 57
  working links, against the buried copy's 27.8 KB and 11 dead ones. Six of the seven files the
  buried copy "lost" are served fine over there. Nothing was rescued because nothing was lost —
  retired to `_to_delete/superseded-copies/`.
- `omega/omega-point-v2-draft.html` is now **one** document instead of three (the original is
  preserved in `_to_delete/superseded-copies/`). Of its two index drafts, the later was kept —
  identified by its carrying the `prov-add`/`prov-foot` CSS that `2ef1664` introduced.

## 5 · The two Omega Point indexes — merged, canonical is `omega/`

**The earlier claim that they "each got a different half of the repairs" was wrong on the DOI
half** — neither copy carries a Vol I DOI; both are clean. The real difference was content, and
neither was a superset:

- `omega/omega-point-index.html` had Gallery of Mathematical Mystics, The Ancient Transmission,
  and Transmission Status. Root had none of the three.
- Root had two chapter cards omega lacked: **Chapter Eleven · The Prevention Theorem** and
  **Chapter Twelve · The Inner Pharmacy**.

`omega/` wins: more content, sits with its 32 chapters, and every chapter reaches it through a
bare relative `href="omega-point-index.html"` — against five root-level pages for the other.
The two chapter cards were ported across (hrefs rebased), the section heading corrected from
**"Ten Chapters" to "Twelve Chapters"** — it listed twelve — and root `omega-point-index.html`
is now a redirect stub on the `omega/index.html` pattern, so the five root links and any
bookmark still land. The superseded root copy is in `_to_delete/superseded-copies/`.

## Verification

128 HTML paths in the diff (15 retired). **107 have an identical parsed tag sequence and an
identical href set** — the IMPA pass was pure label text, as intended. The six with real deltas
are all accounted for: five omega chapters at ±2 hrefs (the `../` repoint) and the v2 draft at
−476 tags (two documents removed). Auditor over all four sections: **zero dead links, zero parse
defects, zero duplicate ids.** Indexes regenerated: 624 files, HVEH 18/0 orphaned (was 26 with
duplicates).

## Newly open — residue the 2026-08-18 IMPA pass left behind

Relabelling the portal surfaced IMPA claims of a different kind. **None were touched**; each is
a claim about the institution, not about a link target, and each needs the author.

1. **`GTCT_V_Student_Edition.html` (and `book5/`): *"Licensed for educational use at IMPA and
   partner programs."*** That is a licensing claim. It is either true or it has to go.
2. **Edition names survived the rename.** `book6/index.html` still has *"IMPA Bilingual Edition"*
   and *"IMPA distribution companion to Vol IV"*; `book1/vol2-dashboard.html`,
   `book2/vol2-contact.html` and `vol2-contact.html` label Vol IV *"GTCT T1, IMPA"*.
3. **`book4/ch10.html` still says *"Submitted to IMPA."*** IMPA replied and declined; the pass
   that cleared 17 of these missed this one.
4. `book4/chIV-axioms.html` and `chIV-axioms.html`: *"IMPA / Bienal SBM 2026"* — a venue claim.
5. *"IMPA-style textbook"*, *"quarterly IMPA-style lectures"*, *"you will hear this even in IMPA
   seminars"* — descriptive, probably fine, listed for completeness.
6. **The `$199.99` Patron tier promises *"Complete print + eBook series, all volumes"*.** Print
   is not for sale ("Print ISBNs reserved — paper books not for sale until further notice").
   Only the *"via the IMPA portal"* clause was fixed; the print promise is a commercial decision.

Still open from the previous entry, unchanged: `AMonster/MonstersLaw.html` vs `monsterlaw.html`
(divergent case-differing drafts) and `dm3-lab-index.html`'s ISBN table.

# Licensing: the IMPA claim was a mis-statement, and it exposed a real split (Aug 2026)

**Author's clarification:** *"Licensed for educational use at IMPA and partner programs"* was
never a claim that IMPA licensed anything. He meant the work is openly licensed — MIT and
Creative Commons — so it can be used in teaching. The sentence said the opposite of what he
meant, and it was the only licensing statement on those two pages.

Fixed in `GTCT_V_Student_Edition.html` and `book5/GTCT_V_Student_Edition.html`:
**"Free for non-commercial educational use · CC BY-NC-ND 4.0"** — true under the licence, and it
preserves the intent (teach from it) that the original sentence was reaching for.

## There was no LICENSE file at all

The README promised *"MIT (code)"* and **nothing in the repository granted it.** Now:

- **`LICENSE`** — the MIT text, covering 27 `.lean`, 20 `.py`, 6 `.js`, 2 `.sh`.
- **`LICENSE-CONTENT`** — CC BY-NC-ND 4.0 for the written material, with the deposit exception
  below written down.
- README's `## License` section points at both.

## The 464/134 split was NOT drift — it mirrors the deposits

Before assuming the minority string was an error, every Zenodo record cited anywhere in the
corpus was queried for its actual `license` field. **The split is real:**

| Deposited licence | Records |
|---|---|
| `cc-by-nc-nd-4.0` | 26 — incl. Vol I (19117400, 20320693, 21146416), Vol II (19379473), GTCT (20360288), the dm³ Operator |
| `cc-by-4.0` | **25** — incl. The Law of Monsters (20561165), Positional Dominance (21013066, 21753025), Contact-Geometric Theory (20682934), Transamerican smoke (21431505), Gravitational Lensing, Nested Infinities |
| `mit-license` | 1 — Polylaminin (19501831) |

**A Zenodo licence cannot be narrowed after publication.** So "CC BY-NC-ND everywhere" is not
available as a fact about the 25 records already deposited CC BY 4.0, however the series is
labelled going forward. Writing `CC BY-NC-ND 4.0` onto a page that reports one of those deposits
would have manufactured 100+ false statements — the exact defect class this audit exists to
remove. **Check the deposit before normalising a licence string.**

## What the 46 both-licence files actually were

Not contradictions. The **provenance footer** states the licence of the *page as part of the
series*; the **deposit block** states the licence of the *paper the page reports*. Two different
objects. They are kept, and `LICENSE-CONTENT` now says so explicitly so a future pass does not
"fix" one into the other.

## What was changed

Each of the 123 files containing `CC BY 4.0` was classified by whether it cites a record actually
deposited under CC BY 4.0:

- **23 keep it** — every one sits beside a genuine `cc-by-4.0` deposit. Verified: after the pass,
  zero files carry `CC BY 4.0` without such a deposit.
- **100 corrected** (108 strings) — page footers of the form
  `© 2026 Pablo Nogueira Grossi · G6 LLC · Newark, New Jersey · CC BY 4.0` on chapters with no
  deposit of their own. These are the series default and now read `CC BY-NC-ND 4.0`. Ten of them
  sat directly beside Vol I's concept DOI, which is deposited NC-ND — those were flatly wrong.
- **0 unresolved.** Every DOI in every affected file had a checked licence.

Corpus now: **521 files CC BY-NC-ND 4.0 · 23 files CC BY 4.0**, and the 23 are justified.

## Still open

`19501831` (Polylaminin) is deposited **`mit-license`** — an MIT-licensed *paper*, alongside a
`cc-by-nc-nd-4.0` sibling record (`20230633`) of the same title. One work, two deposits, two
incompatible licences. Nothing in this repo asserts either, so nothing was changed; it needs a
Zenodo-side decision by the author (rule 4).

# The ten books audited clean — and `tools/audit.py` now exists (Aug 2026)

**311 HTML files across Vols I–IX plus HVEH. All ten report clean.**

The battery is no longer improvised per-session. It lives at **`tools/audit.py`**:

    python3 tools/audit.py book4 book8        # named targets
    python3 tools/audit.py --all --json       # everything, machine-readable

Its resolver rules each exist because a naive version lied to a previous session, and
the docstring says so. **Do not "simplify" them.**

| Rule | Why |
|---|---|
| Strip the `/geometry/` prefix | It is the Pages base path, not a repo path. ~900 links use it and all resolve; without this they all read dead |
| `href="../"` and bare dirs → `index.html` | Normalise before the membership test |
| Split fragments, then check ids in the target | A live file with a dead anchor is still a defect — that is how `#F3` and `#schwarzschild` were caught |
| **Count `<!DOCTYPE`, do not rely on tag balance** | Concatenated documents are each internally balanced, so the stack comes out clean. This is what found `HVEH/index` and `omega-point-v2-draft` |
| Ignore doctypes inside `<script>` | `impa-portal.html` emits a page from a backtick string |
| Ignore `**bold**` inside `<pre>`/`<code>` | Lean docstrings legitimately use markdown |

Three known-benign classes are now suppressed **in the tool**, not in a human's memory:
cross-repo `../../AXLE/` links; matplotlib-emitted duplicate SVG ids; and a flagged string
sitting inside its own correction note (an ISBN named *as* unallocated, or a claim quoted
in order to retract it). That last one matters — the auditor was flagging this file's own
corrections as defects.

## What the sweep fixed

| File | Defect | Note |
|---|---|---|
| **`book5/GTCT_V_Student_Edition.html`** and its **root copy** | **`<script/>` at line 1329** | The find of the sweep. HTML has no self-closing script: it opened an element that ran to the next `</script>` at line 2557, **swallowing 1,228 lines** — the whole of Level III's diagram and Levels IV–V. Half the Student Edition was not rendering, in both copies |
| `book8/ch01-anyonic-topology.html` | two `.math-block` divs unclosed (lines 532, 606) | cascaded, so `content-wrap` appeared unclosed too |
| `book4/ch15-complex-turn.html` | `<div class="chapter-body">` opened twice, closed once | duplicate opener removed |
| `book4/gomc-opus.html` | `.table-scroll` never closed | every sibling closes `</table></div>`; this one did not |
| `book4/chIV-field.html` | stray `</div>` with no opener | in a browser this closes the *parent* early — a real layout bug, not cosmetic. Note: the axiom pip rail runs 2–7; **pip 1 is missing** and was not invented |
| `book8/ch8-9-nested-infinities.html` | display math split a paragraph; second half never opened | `<p>` added |
| `book6/wp64-the-recorder.html` | `**` around a span in a pull-quote | → `<strong>` |
| `book8/ch3-singularity.html` | `ch1-darkmatter.html#F3` — no such id | fragment dropped |
| `book4/ch10.html` | *"Submitted to IMPA."* | survived the 17-file cleanup; IMPA declined |
| `book8/ch-orthogonal-witness.html`, `book8/ch-turnaround.html` | footers asserting ISBN 979-8-9954416-5-6 | Vol VIII has no allocation |
| `book8/ch8-3-galaxy-mergers.html` | *"will collide in 4.5 billion years"* | → *"were projected to collide"*; the van der Marel (2012) attribution stays |

**Deliberately not touched:** the ISBN correction notes in `book5/chV-seed`, `book6/g6-crystal`
and `book7/ch-huh`. Each says in its own words that 5-6 is unallocated reserve and not a
fallback. They are the fix, not the defect.

## OPEN — the root is the real backlog

The ten books are clean. **The 299 files at the repository root are not:**

| | |
|---|---|
| dead links | **79** |
| dead anchors | 18 |
| unclosed tags | 16 |
| stray closers | 4 |
| stale claims | 2 |

That is the largest unaudited surface in the repo and it contains the site's front door.
Nothing above touched it. Examples from the first page of output: `ch-tatiana.html` points at
two `figures/*.png` that do not exist; `chEta-tribonacci.html` points into
`Orthogenesis/Constants/` which does not exist; `chapters-diagram.html` links
`index-geometry-hub.html` and `journey-v1-backup.html`, neither of which exists;
`access-required.html` fails to close `<html>` and `<head>`.

---

# The root audited clean — 614 files, whole repo (2026-08-20)

The section above ("OPEN — the root is the real backlog") is now closed. `--all` audits
614 files and prints `clean`. Two commits did it: `3266a71` took the dead links and the
two files that were corrupt on upload; this pass took the parse defects, the anchors and
the ISBN claims.

## The auditor was lying about its own coverage

`--all` walked *directories only*. The 299 loose HTML files at the repo root — including
`index.html`, the site's front door — were never in scope unless someone typed
`python3 tools/audit.py *.html` by hand. Nobody did, for months.

That is now **rule 6** in `tools/audit.py`: `--all` = every directory **plus** every root
`.html`. The tool reports `… + 299 root files` so the coverage claim is visible in the
output, not buried in the argument parser. **A tool that under-reports its own scope is
worse than no tool** — it converts "unaudited" into "audited, clean".

## What the root was hiding

| file | defect | root cause |
|---|---|---|
| `gomc-opus.html` | 177 KB, **two whole documents** | see below |
| `ch7-topological-orthogenesis.html` | 22 headings nested one level too deep | a `<div class="math-block">` never closed; the `</div>` labelled `<!-- /content-wrap -->` was closing *it* |
| `ch-d2-academic.html` | a paragraph opener and a reference opener both lost | see below |
| `ch12-conclusion.html` | `div` unclosed to EOF | a `math-block` div closed with `</p>` |
| `collatz-engineering_1.html` | same `</p>`-for-`</div>`, **plus** every section id off by one | see below |
| `ch15-complex-turn.html` | duplicate `<div class="chapter-body">` opener | same defect already fixed in `book4/`; the root copy was missed |
| `ch4-neural.html` | 856 bytes of duplicated prompt block **after `</html>`** | tail of an aborted append |

### `gomc-opus.html` — the concatenation the DOCTYPE rule could not see

Rule 4 exists because tag balance cannot detect concatenated documents. This file defeated
rule 4 as well: the second document's `<!DOCTYPE htm` had been **eaten**, leaving `l>`
welded onto the end of a truncated table:

```
    </table></div>l>
<html lang="en">
```

One `<!DOCTYPE`, so the counter stayed quiet. What gave it away was two `<body>` tags.

The two copies were not old-and-new — they were **two different edit passes on two
different copies**. Document 1 had the nav bar and the orthogenesis note and was truncated
mid-table; document 2 had the provenance CSS and everything from §7 to `</html>`.
`book4/gomc-opus.html` turned out to be the correct merge of both, so the root file was
rebuilt from it plus document 1's nav. Verified content-complete first: document 1's
18-row bridge table is document 2's CatGT table, condensed — nothing was lost.

**Check for a second `<body>`, not just a second `<!DOCTYPE>`.**

### `ch-d2-academic.html` — one missing opener, 1,100 lines of consequence

A reference entry lost its `<div class="ref">` and author span, leaving an orphan tail:

```
    </div>
      2013. "Mindfulness-induced Changes in Gamma Band Activity." <em>Clinical
      Neurophysiology</em> 123(4): 700–710.
    </div>
```

That extra `</div>` closed `<div class="references">` early, which made the `</div>` at
line 1993 — the one labelled `<!-- /chapter -->` — read as stray, 250 lines away from the
actual defect. The entry was identifiable from the title and the citation and restored as
Berkovich-Ohana, Glicksohn & Goldstein; the year was also wrong (2013 → **2012**, PubMed
21940201).

Separately, a `<p>` opener and its first clause were lost around line 855, so the text
resumed mid-sentence at *"adaptation — morphological, behavioral…"*. The clause is
recoverable from this chapter's own abstract and is restored, **marked with an HTML
comment naming it a reconstruction**. Do not silently restore prose; say that you did.

Note also that those three paragraphs sit at the end of §1.3 (Bacon and cryptography) and
argue the daśāvatāra hinge, which §1.1 already covers more fully. They look like a
superseded draft that was never removed. **Left in place — that is an editorial call, not
an audit fix.**

### `collatz-engineering_1.html` — ids drift when you insert without renumbering

The Saturn Lean section was added later and given `id="s9-saturn"` instead of renumbering.
Everything after it kept its old number, so the TOC's `#s9` landed on §10's content,
`#s10` on §11's, and `#s12` on nothing. Renumbered to match the TOC. `#ack` and `#refs`
were also in the TOC; **neither section was ever written**, so the two promises were
removed rather than satisfied with invented content.

## ISBNs — two more instances of the rule already written above

`Book1.html` footer carried `979-8-9954416-5-6 (eBook · Complete Completeness G5)`, and
`dm3-lab-index.html`'s table assigned `2-5`, `4-9` and `5-6` to three volumes. Per
`isbn_metadata.json`: `2-5` and `5-6` are unallocated reserve (no group, no format) and
`4-9` is G5 *Hardback* on HOLD. All removed. The table now carries a note saying only
registered allocations are listed and pointing at the Zenodo community.

This is the fourth time the same reserve numbers have had to be pulled out of footers.
The rule is in "Series ISBN & format map" above: **no registered allocation → no ISBN line.**

## Anchors

`omega-point-index.html` at the root is a redirect stub with **no ids of its own** — a
fragment link to it silently drops the fragment. Four files were linking
`omega-point-index.html#chapters`; all now point at `omega/omega-point-index.html#…`.
**When you replace a page with a redirect, grep for inbound fragments.**

Also fixed: three `sessao*.html` footers linked "Série completa" at
`index.html#bibliography`, which never existed (→ `series-hub.html`); `gcm-framework.html`
promised `#sec3-g` in its TOC and never gave the paragraph the id; `vol1-mathematics.html`
pointed at `#references` when References is `#sec18`; `ch02-biological.html`'s "Next:
Chapter 3" was still the placeholder `href="#next"` (→ `ch03-plasma.html`).

## Cover art

`assets/book-cover.png` and `book-cover.jpg` do not exist and never have — there is no
cover image anywhere in the repo. Both `<img>` tags already had `onerror` handlers, so the
pages looked fine while linking at nothing. Replaced with a placeholder that says "cover
art not yet produced". **An `onerror` handler hides a broken link from the reader, not
from the audit — and hiding it from the reader is how it survives.**

## Verification

```
python3 tools/audit.py --all
614 html scanned in: … + 299 root files
  clean
python3 tools/build_indexes.py     # 625 files, 31 orphaned, 16 pages written
```

The 31 orphans are almost all `_archive/` (23) and are deliberate.

## Errata — 23–24 August 2026

Recorded here, not on the chapter pages. A book carrying its own correction
apparatus in the body text reads as unreliable to someone who has not been
following the work, and that cost is real: the reader does not distinguish
"this desk checks itself" from "this text is full of mistakes." The fixes are
in the pages. The account of them is here.

| date | file | what changed |
|---|---|---|
| 24 Aug 2026 | `ch6-resonant.html` | Correction history. 23 Aug 2026, first pass: this sentence read &ldquo;the separation theorem guarantees&rdquo; and was changed to &ldquo;separation conjecture&rdquo; with a note asserting that no statement of it existed anywhere in this corpus. That note was wrong &mdash; the statement exists in AXLE&rsquo;s Lean and the registry tracks its single open obligation; the search behind it covered only HTML. 24 Aug 2026: corrected to the text above. A mis-correction is a defect of the same family as the one it was trying to repair, and is recorded here rather than quietly reverted. |
| 24 Aug 2026 | `chLambda-polylaminin.html` | 24 Aug 2026: guarantees was too strong. The theorem carries one scoped sorry (h_transverse, an eigenvalue API gap, AXLE&nbsp;#12), so this chapter&rsquo;s conclusion inherits that obligation. |
| 24 Aug 2026 | `chLambda-polylaminin.html` | under review 24 Aug 2026 &mdash; the derivation ε₀ = |μ_max|/(2(1+H)) gives 1/2 at H = 1, not 1/3; see G6Crystal.lean |
| 23 Aug 2026 | `omega/ch-baudhayana.html` | Corrected 23 August 2026: this line previously printed the fraction as &ldquo;$\approx 1.41421356\ldots$&rdquo;, which is the decimal expansion of $\sqrt{2}$ itself, not of $577/408$ &mdash; and contradicted the five-decimal claim in the same sentence. |
| 23 Aug 2026 | `book4/ch13.html` | Convention fixed 23 Aug 2026. $c = p^{-s}$ with $s\in\mathbb{C}$ is a complex number, and $|c|_p$ has no meaning for it. Everything in this section is to be read in the formal setting: treat $c$ as a $p$-adic variable in the open unit disc of $\mathbb{C}_p$. The ultrametric identities below are correct there and only there. |
| 23 Aug 2026 | `book4/ch14.html` | attribution corrected 23 Aug 2026 &mdash; this line previously credited Bombieri&ndash;Hejhal, whose 1995 work is on zeros of linear combinations of L-functions, not pair correlation |
| 23 Aug 2026 | `book4/ch14.html` | corrected 23 Aug 2026: this sentence previously said the Euler product is finite. It is not &mdash; a curve over $\mathbb{F}_q$ has infinitely many closed points, and already $\mathbb{A}^1$ has infinitely many monic irreducibles. |
| 23 Aug 2026 | `book4/ch11.html` | corrected 23 Aug 2026: this passage previously quoted $\alpha = dy + x\,dx$ and claimed &ldquo;the key was non-integrability, $\alpha\wedge d\alpha \neq 0$&rdquo;. That is wrong twice over &mdash; $\alpha\wedge d\alpha$ is a 3-form and vanishes identically on a 2-plane, and $d(dy + x\,dx) = 0$ in any case. Non-integrability belongs to the 3-space prototype $\alpha = dy - y'\,dx$ on the 1-jet space $J^1(\mathbb{R},\mathbb{R})$, not to the oscillator certificate. |
| 23 Aug 2026 | `book4/ch11.html` | corrected 23 Aug 2026 &mdash; this previously called for Baker&ndash;W&uuml;stholz at ~80 lines; the argument is elementary and the issue is correspondingly smaller. |

### Not errata — live warnings that stay on the page

`book4/ch11.html` §11.5 and the inherited notices on ch12–14 are **not** in this
table and must not be moved here. There the body text is *still wrong* and has
not been rewritten: α_arith = dV − g dU does not annihilate the lifted curve, and
the chapter still prints it. A reader arriving at that page needs the warning
before the claim, not after it in a ledger. Those notices come off when the
log-zeta rewrite lands (audit item M1), and not before.


## M1 closed — 24 August 2026, and a class the ladder did not have

`book4/ch11–14`. The withdrawn kernel claim is repaired and the four withdrawal
notices are retired. Zero occurrences of the old form remain in the arc.

**What the defect actually was.** Not a wrong theorem. §11.3 defines
ζ(σ+it) = U + iV — the real and imaginary parts of ζ itself, which is the correct
picture for the trajectory and for Fig. 11.1. §11.5 then applied the
Cauchy–Riemann equations *to log ζ* while still writing U and V. Both statements
are individually true; they are about different coordinate systems wearing the
same two letters. The relation ∂ₜV = g·∂ₜU is false for ζ-coordinates and the
correct log-coordinate statement is (∂ₜŨ, ∂ₜṼ) = (−g, −c) with −ζ′/ζ = c − ig.

**The repair** names them apart: Ũ + iṼ = log ζ, kept strictly distinct from
(U,V); α_arith = c dŨ − g dṼ, verified in one line as c(−g) − g(−c) = 0; §11.6
carries the Wronskian W = c ∂ₜg − g ∂ₜc; a zero is a plunge Ũ → −∞ rather than an
axis crossing. ch12–14 updated in body text, in ch13's local factors, and in
ch14's inventory array — which held the false Cauchy–Riemann justification inside
a JavaScript string, where no prose read would have found it.

---

### New class · NOTATION COLLISION

> Two distinct objects share a symbol inside one document, and a statement true of
> one is asserted in the notation of the other. Every sentence is individually
> defensible. The document is wrong.

**Why the existing classes miss it.** It is not MISMATCH (nothing is filed under
the wrong claim), not STALE (nothing decayed), not FALSE in the ordinary sense
(each half is true where it belongs), and not VACUOUS (the statements have
content). It is a defect of *reference*, not of content.

**Why the instruments miss it.** A kernel cannot see it: each statement
type-checks in its own coordinate system, and nothing forces the two systems into
the same context where they would clash. `grep` cannot see it: the symbol is
spelled identically in both uses — that is the defect. It survives review because
a reviewer checking any single line finds it correct.

**How this one was found.** By reading the definition of the coordinates against
the use of the coordinates, four sections apart. That is the same instrument that
found the five MISATTRIBUTED theorems in NASAGaps: a person holding two parts of
the document in mind at once. Both classes are undecidable by machine for the same
reason — the failure is in the correspondence between a symbol and what it denotes,
and the denotation is not written down anywhere the machine can read it.

**Cheapest available guard.** Not a checker. A convention: *when a document changes
coordinate system, the new system gets new letters, in the sentence that introduces
it.* Ch 11 now does this. It costs one sentence and it makes the collision
impossible to write.

**Where the classes live.** Here, in the log. WP73 carries the four artifact-level
classes because those are the paper's subject. The rest — UNFALSIFIABLE GUARD,
MIS-CORRECTION, FABRICATION, NOTATION COLLISION — are recorded in this file and
not promoted to working papers. A series with a defect paper in it reads like a
series that needs one.


## ε₀ — tested rather than chosen, 24 August 2026

Three candidate resolutions were on the table. Two were eliminated by test, not
by preference.

**(c) ε₀ = 1/2 — REFUTED.** It gives τ·ε₀ = 1 exactly, contradicting
`dm3_noise_tol_lt_one : noise_tolerance < 1`, which is kernel-checked and
passing. That theorem is substantive, not decorative: it is the claim that
perturbations below 2/3 of the structural amplitude preserve the resonant lock.
At exactly 1 the claim dies. So (c) is not free — it costs a second theorem.

**(a) H = 2 and (b) a different formula — INDISTINGUISHABLE inside the corpus.**
Both give ε₀ = 1/3, both give noise tolerance 2/3, both clear the g⁶ relative
error of 0.0154. No downstream theorem separates them. The corpus cannot decide
this; only the source of the derivation can.

**What was done instead of choosing.** `epsilon0_of_eq_third_iff` proves
ε₀(H) = 1/3 ↔ H = 2 — an iff, so it cannot drift. The open question became a
stated obligation: *show the dm³ toy model has sup‖Hess V‖ = 2.* Kernel-checked
GREEN, 14 theorems, 24 Aug 2026.

The method is worth keeping separately from the result. When a defect admits
several repairs, propagate each through the existing theorems before picking one:
the corpus often eliminates options on its own, and what survives is either a
single answer or a well-posed question. Choosing first would have looked like
resolution and produced none.


## M13 closed — 24 August 2026 · E₈ is not a Cayley–Dickson rung

`series-hub.html` asserted *"G = U∘F∘K∘C IS the Dynkin diagram of E₈"* and
`vol3-minibeast.html` listed E₈ as a rung of the Cayley–Dickson ladder. The
audit (RH-arc item M13) had flagged both: E₈ is not in that sequence — the rung
after the octonions is the 32-dimensional trigintaduonions — and the chain has
four operators against the diagram's eight nodes, so the identity cannot hold
as written.

**What is true, and it is stronger than the compression.** The E₈ lattice *is*
the ring of integral octonions — Coxeter's octavian integers, 1946 — and that
ring has exactly 240 units, which are the E₈ roots. So E₈ does not sit *on* the
ladder; it sits *at* the octonionic rung, by a different construction.

Verified this session, independently of the corpus:

| quantity | value |
|---|---|
| det(Cartan E₈) | 1 |
| roots | 112 + 128 = **240** |
| rank | 8 = dim 𝕆 |
| Coxeter number h | 240/8 = **30** |
| ρ(Dynkin adjacency) | 2cos(π/30) = 1.989043790737 |

The last row is the one that connects to `docs/` → the ladder note: ρ(E₈) is the
**largest finite ADE spectral radius**, sitting just below the affine boundary at
2. That is what the corpus's standing line "the finite classification ends" means,
now with the number attached — and it is the same 2 the n-bonacci ladder
approaches from below.

**Lean targets, no new mathematics required:** `e8_roots_card = 240`,
`e8_coxeter : 240 / 8 = 30`, `e8_rank_eq_octonion_dim`, and
`e8_rho_lt_two : adjacencySpectralRadius E8dynkin < 2`.

**Method note.** The first instinct here was to call the claim wrong because no
Lean file mentioned Dynkin diagrams — the same bad inference that produced the
separation-theorem mis-correction the day before. Computing the E₈ invariants
first showed every number the corpus asserts about E₈ is correct; only the
*placement* was wrong. Absence of a proof file is not absence of a fact.


---

## 2026-08-26 · Volume II: the verification table described a file nobody built

`vol2-contact.html` was serving **Version 2a** while the deposit stood at V4
(doi:10.5281/zenodo.21148424, July 2026), and the V4 record's own "read it here"
link points at that page. So the canonical URL served the Contact Hopf value
γ* = e^(z₀) that V4 exists to correct, and claimed *"Inner basin formal proof
closed — Project 1080"* on the same page where the Open Problems section called
that obligation open. Its DOI badge read `20755436`, which is V3's.

**Appendix A named twelve declarations; six had never existed.** `thm_B_mu_iff_tau`
and `thm_C_A1_surjective` — both in the *proved* column — plus
`thm_gronwall_asymmetry`, `eigenvalue_limit_filter`, `thm_A_contact_realization`
and `thm_B_full_chain` return nothing anywhere in AXLE. The cited path
`AXLE/lean/VolumeTwo.lean` 404s; the file is at
`AXLE/PrincipiaOrthogona_v2/VolumeTwo.lean`, with a byte-identical second copy
under `NASA/MoonBase/AXLE_lean_files/`.

**Why it could drift that far: the file was in no lakefile target.** Nothing had
ever elaborated it. Its first build reported eight errors, three of them in
theorems the table listed as proved — including `eigenvalue_neg_pos_z`, whose
proof the page displayed verbatim as its worked example and which used
`Real.exp_lt_one_of_neg`, not a Mathlib constant. AXLE has no CI at all, which
is worth stating plainly: the repository the papers name as "the companion formal
verification repository" has never run an automated check.

Fixed in AXLE, verified at v4.14.0, 14/14 on
`[propext, Classical.choice, Quot.sound]`. Three findings the axiom gate cannot
see, and which the corrected table therefore states in words:

- **Theorem A's conclusion is `True`**, not a `sorry`. A `sorry` fails a kernel
  gate; `True := by trivial` passes one. The published row read `sorry ★★★★`.
- **Theorem B's biconditional is proved from assumptions on both sides** —
  `sys.mu_neg` is a field of `DM3System`, so `μ_max < 0` is assumed at
  declaration, and both branches discard the incoming hypothesis.
- **Theorem C is a surjection, not a bijection.** Four bifurcations onto three
  Whitney types, two-to-one on A₁. §5 states this correctly while the abstract,
  Theorem C and the Lean name all said "bijective."

Also withdrawn: integrability Levels 2d and 2d+t, whose "dΩ = 0" hypothesis was
`∀ X Y Z, (0:ℝ) = 0` — a tautology, so the axiom field asserted its own
conclusion. Recorded as OP4/OP5 rather than restated as `sorry`s, because
N_J needs Lie brackets of vector fields and cannot be written in a pointwise
model at all. Level 1 is genuinely proved and stands.

**Method note.** This is the third claim-about-Lean in two days written from
intention rather than from the artifact — after the `vol2-toymodel.html` badges
naming declarations absent from `geometry`, and `tools/verify-dm3/probe_dm3.lean`
naming thirteen ToyModel declarations without importing the module. Each got a
local repair; none produced a check. The rule that would have caught all three
does not exist in any CLAUDE.md: *every declaration named in prose must resolve,
at the path cited.*

---

## 2026-08-27 — Book 8 `OrthogonalWitness.lean`: first kernel run, and the count-drift guard

`book8/OrthogonalWitness.lean` had a STATUS header asserting sympy verification
and stating plainly that the Lean had never been through a kernel. That is the
honest version of the failure the entries above document, and it is what made
today cheap: nothing had to be withdrawn, only run.

**The run.** `lake env lean book8/OrthogonalWitness.lean` under
`leanprover/lean4:v4.32.0` — the toolchain this repository already pins, so no
second Mathlib and no cache download. All four theorems report
`[propext, Classical.choice, Quot.sound]`. No `sorryAx`. STATUS now records the
date, the pin, the command and the axiom line.

**What the four theorems are.** None is vacuous in the gate's sense — no `True`,
no unsatisfiable hypothesis, no conclusion independent of its hypotheses — but
four *names* are not four independent facts, and the file now says so in a SCOPE
block rather than leaving the reader to infer it:

- `on_hyperboloid` and `proper_time` are the same Mathlib fact,
  `cosh² − sinh² = 1`, multiplied by ℓ² in one and negated in the other.
- `on_hyperboloid` states the ω-reduced constraint: `‖ω‖² = 1` is substituted by
  hand into the statement rather than carried as a hypothesis. No metric,
  manifold, pullback or normal bundle appears anywhere in the file.
- `radius_has_throat` is stated for `0 ≤ ℓ` and is true-but-empty at ℓ = 0, since
  Lean's `τ / 0 = 0` gives `a 0 τ = 0 ≤ 0`. The geometry needs `0 < ℓ`.
- `throat_value` is `cosh 0 = 1`.

The tensor pullback — the step that would make "induced metric" a proved phrase
rather than a docstring phrase — is the sympy result and is **not** in the
kernel. `witness_codimension` (`5 - 4 = 1`) was demoted to a comment: truncated
subtraction on ℕ literals closes by `rfl` whether or not anything about normal
bundles holds, and stated beside three real analytic identities it invites the
reading that vocabulary matching means the theorem matches.

**The file was in no build target.** Same shape as `SaturnHexagon.lean` before
2026-08-21 and `PrincipiaOrthogona_v2/VolumeTwo.lean` before 2026-08-26: it
compiles when invoked by hand, and a hand run proves the file on the day it is
run and nothing afterwards. Declared as `lean_lib OrthogonalWitness` with
`srcDir := "book8"`. Eight root-level `.lean` files remain outside every target.

**The gate, and its limit.** `tools/verify-book8/` mirrors `verify-dm3`: build,
kernel probe, `axiom_gate.py` with a hardcoded count. Note that `#print axioms`
emits *info*, not an error — a `sorryAx` would scroll past inside a build that
still reports success — so the declared target catches a compile regression and
the gate catches an admission regression. They are two different checks.

**A check that produced a finding on its first run.** The hardcoded `N` in each
`run.sh` is deliberate: deriving it from the probe would let a theorem be
dropped without failing anything, which is the regression the gate exists to
catch. The cost of hardcoding is drift between three places — the probe's actual
`#print axioms` lines, `N=` in `run.sh`, and the README.
`tools/probe_consistency.py` refuses that drift (selftest 5/5; negative controls
catch a wrong `N` and an emptied probe; exit 2 on a zero scan, so it cannot
silently stop checking). It immediately found `tools/verify-dm3/README.md`
stating 12 theorems and gate count 12 while `run.sh` had been `N=28` since the
ToyModel additions of 2026-08-26. The README now lists all 28 by name.

**What it does not do.** `probe_consistency.py` guards counts, not claims. It
cannot tell you that `on_hyperboloid` and `proper_time` are one fact wearing two
names. That is prose in a README, and nothing enforces it — the same class of
gap as the declaration-resolver rule noted in the entry above, still unwritten.

**Open after today.** `.github/workflows/verify-proofs.yml` remains uncommitted
(PAT lacks `workflow` scope) and, when it lands, needs a verify-book8 step and a
`probe_consistency.py` step. AXLE has no CI at all, and `AXLE/tools/verify-vol2/`
now has the same three-file shape without the guard, which only walks
`geometry/tools/`.

Commits: `d203f4c` (kernel run + build target), `7047888` (gate + guard + README
count 12→28).

## WP-61 · The Root-Language Sweep — logged 30 August 2026, eighteen days after the fact

The sweep happened on **2026-08-12**. It never reached this log. Recording it now,
together with what it missed, because a correction that is not logged cannot be
checked for completeness — which is exactly how it came to be incomplete.

### The error
Several chapters asserted that the dm³ potential `V(q) = q³ − cq` **has a double
root at q = 1** when `c = 3`. False. `V₃(q) = q³ − 3q` has roots `0, ±√3`, and
`V₃(1) = −2`, so `q = 1` is not a root of it at all.

What is true, and what every downstream result actually uses: `c = 3` is the
unique coefficient for which `q = 1` is a **critical point** of `V_c`
(`V′_c(1) = 3 − c = 0 ⟺ c = 3`), and it is **non-degenerate**, since
`V″(1) = 6 ≠ 0` — the Whitney A₁ condition. The double root belongs to the
**shifted** potential `V(q) − V(1) = V(q) + 2 = (q−1)²(q+2)`, where it is
automatic at any non-degenerate critical point, not a special feature of `c = 3`.

The distinction is load-bearing: "double root", "degenerate" and "critical point"
are technical terms in singularity theory and in the combinatorial-Hodge-theory
literature this material sits beside. Conflating them is the same error WP-24
found and refuted.

### What WP-61 fixed on 2026-08-12
- `ch-recurrence-ladder.html` — correction notice added
- `chapters-pi-phi-mu-eta-delta-sigma-omega.html` — correction notice added
- `ch-eta-dnls.html` — correction notice added

### What it missed, found 2026-08-30
- **`ch-lambda-criticality.html`.** Worse than the others: besides the prose, it
  displayed a Lean theorem `fold_double_root_at_unity` asserting `V 1 = 0` **with
  a ✓ beside it**. No such theorem can have been checked, because the statement is
  false. Corrected, with a notice naming the eighteen-day gap.
- **`GTCTsorryFree.lean` in TOTOGT/GTCT.** Section 1 carried the identical false
  claim in Lean: `fold_factorization_c3`, `root_at_one` and `c_star_unique` were
  false statements, not unproved ones. The sweep never reached the formalization.
  Corrected 2026-08-30 with the operator `W_c q c = q³ − c·q + (c−1)`, which is
  the same shifted potential the HTML notice describes.
- **`dm3CriticalityPrinciple_extended.lean`** still carries it. Open.

### Not defects
- `chPI-recurrence.html` — the short Greek-series hub. Never made the claim; no
  notice needed.
- `book4/chpt11.md` — a diagnosis note *about* the error. Its own correction,
  `q³ − q² − q + 1 = (q−1)²(q+1)`, is a different cubic from the shifted potential
  but is itself correct; it is describing the general shape, not the framework's V.

### The lesson, and it is the second time this week
A sweep is only as good as its inventory. WP-61 swept HTML and stopped there; the
Lean files stating the same claim were never in scope, and one HTML page was
simply missed. The rule going in to `CLAUDE.md`: **a correction sweep must name
the file set it searched, and that set must include every format the claim appears
in — prose, Lean, and any registry or figure caption that quotes it.** A sweep
with an unstated scope cannot be audited, and this one was not.

---

## 2026-08-30 · Book 4 §12.1–§12.2: the reflection was the wrong map, and the open computation was classical

**Scope searched.** `book4/ch12.html` in `geometry` and in `GTCT` (the two copies), and
`GTCT/book4/ZetaReflection.lean`. Naming the set because the WP-61 lesson below says to.
Not searched, and therefore not claimed clean: ch11, ch13, ch14, and any figure caption
outside ch12 that restates the functional equation.

### Defect 1 — §12.1 stated the wrong involution
The page read: *"This reflects $s \mapsto 1-s$: the function at $\sigma + it$ equals (up to
$\chi$) the function at $(1-\sigma) + it$."* False. $s \mapsto 1-s$ carries $\sigma + it$ to
$(1-\sigma) - it$; the height changes sign. The $t$-preserving mirror the chapter actually
uses throughout — and the one Figure 12.1 draws — is $s \mapsto 1-\bar{s}$, the functional
equation composed with complex conjugation, legitimate only because $\zeta$ has real
coefficients. The figure was always right; the prose named the wrong map.

Consequence, and this is why it mattered rather than being a slip: **$s \mapsto 1-s$ fixes
only the single point $s = \tfrac{1}{2}$, not the critical line.** Conjecture 12.1 asserted a
fixed locus of "the plane $\sigma = \tfrac{1}{2}$" for an involution that does not have one.
The figure caption carried the same error and is corrected with it.

### Defect 2 — §12.2's "what's needed" was already known
The conjecture said the missing step was *"understanding how the von Mangoldt coefficient
$g(\sigma,t)$ transforms under the functional equation."* That computation is the logarithmic
derivative of $\zeta(s) = \chi(s)\zeta(1-s)$ and is classical. It gives

    g(σ,t) − g(1−σ,t) = Im[(χ'/χ)(σ+it)],
    (χ'/χ)(s) = log π − ½ψ(s/2) − ½ψ((1−s)/2)

Confirmed numerically to 30 digits at eight points (σ ∈ {0.3, 0.5, 0.8, 1.1, 1.5, 2.3};
t from 0.7 to 25), max deviation 8.8e-16 at one point, exact at the rest. On σ = ½ the digamma
arguments ¼ ± it/2 are conjugates, so χ'/χ is real there and the right side vanishes — checked
at five heights, `Im = 0.0` exactly.

### What that does to the conjecture
It weakens it, in the direction of being provable. $g$ is not carried to $\pm g$; it is carried
to itself plus a defect built from gamma factors and containing no $\Lambda$ at all, so no
scalar $f$ can give $\Phi^*\alpha = f\alpha$ off the critical line. Restated on the page as
**Conjecture 12.2**, graded: $\Phi^*\alpha - \alpha$ is an explicit gamma-factor 1-form
vanishing on $\sigma = \tfrac{1}{2}$. The old form is superseded, and the page says so in one
clause rather than carrying a notice.

### Formalisation
`GTCT/book4/ZetaReflection.lean`, pushed 2026-08-30. `lseries_vonMangoldt_eq_neg_Zlog` — that
$c$ and $g$ are the real and imaginary parts of $-\zeta'/\zeta$ — is **proved**, resting on
`[propext, Classical.choice, Quot.sound]`, verified by `tools/leancheck.sh --audit` against
Mathlib v4.32.0. `reflection_law` and `chiLog_real_on_critical_line` are **admitted**
(`sorryAx`). Numerically confirmed is not proved, and the file states this in its header.

### Where the notices went
Nowhere. Per `CLAUDE.md`, a chapter page carries the corrected statement, not the history of
having been wrong; this entry is the history. Book 4 is a draft for a publisher and the pages
are not the place for errata.

### Still open from this
- `GTCT/book4/ch12.html` still carries both defects. It is the non-canonical copy and, per the
  canonical-HTML rule set today, must be reduced to a pointer rather than edited in parallel.
- ch10's Key Constants sidebar still reads `ε₀ = 1/3 (Gronwall, outer)` after the commit that
  removed the Gronwall framing from the prose. Same shape as WP-61: a sweep that named prose
  as its scope and stopped there.

---

## 2026-08-30 · Book 4 sweep: correction notices off the chapter pages

**Why.** Pablo, this session: *"those are not the pages of the draft book — my publisher
won't like to see that there — we need that note in the log where that belongs."* A chapter
carries the corrected statement; this log carries the history.

**Scope searched.** All 50 `.html` files in `geometry/book4`, on the union of
`correction notice | corrected on | erratum | errata | this page was wrong | was incorrect |
previously stated | now corrected` plus `class="correction`. Not searched: the same chapters
as they exist in `GTCT/book4` (non-canonical, to be reduced to pointers), and Books 1–3, 5–8.

**Structural state at the same date, for the record.** 50 files: **0 parse errors, 0 dead
internal anchors, 0 broken local links.** 21 of 50 carry an "In Plain Terms" opener; 8 carry
an in-page contents list; 18 carry chapter-nav.

### Moved off the pages

**1. `ch10.html` — "Erratum (V4 sync)."** An earlier posting of §6 quoted λ₊ ≈ 1.1097 and
Δ ≈ 4.534. Direct evaluation of the Jacobian at (r_s, z_s) gives **λ₊ = 1.49148,
λ₋ = −0.24450, Δ = 3.01362**; the closed-form expressions in Theorems B.1–B.5 are unchanged
and verify to machine precision. The corrected discriminant is already stated in the proof
immediately above the removed block ("numerically ≈ 3.0136"), so the page loses no fact.

**2. `chIV-orthogonality.html` — "Correction notice (2026-07-18)."** Preserved in full because
it is the sharpest of the three: *the lemma previously asserted the opposite of what is true,
and the error propagated.* The earlier statement claimed
`[K, F]ψ = −λ|ψ(η*)|²ψ(η*)·δ(η − η*) ≠ 0` for K a Heaviside gate and F the **pointwise**
Nemytskii fold. False — a 0/1 gate commutes with a pointwise map *exactly*, for every state,
and the δ term does not exist. The lemma's own proof (steps 2–3) derives KFψ = FKψ; the old
step 4 introduced the δ from nowhere. The lemma now stands correctly on the page.
**Downstream chapters that inherited the false version are tracked in the repository ledger** —
that pointer was on the page and is carried here so it is not lost.

**3. `ch13.html` §13.4** — retitled from "The p-adic Boundary and a Correction" to "The p-adic
Boundary", and the paragraph narrating the error replaced by one that states what the
ultrametric inequality decides. Removed from the page: the attribution of the wrong claim to
"the Gemini conversation in Ch 11's development", and the aside that "the earlier wording
collided with that term". The mathematics is untouched: for |c|_p < 1, |1−c|_p = 1 throughout
the interior, so |(1−c)²|_p = 1 and |g_p|_p = |c|_p = p^(−σ) → 1, not 0; the boundary
|c|_p = 1 is a wall of poles of the local Euler factor, not a soft lock.

### Left in place, deliberately

`ladder-polynomials.html` carries a `.correction`-styled block, but it is not an erratum — it
is a provenance warning: *"Read this cold before citing it. Written in a single sitting at the
end of a long session. The computations are machine-checked and the code is printed; the
interpretations have not been reviewed by anyone."* That is a caveat about reliability, not a
record of a past error, and removing it would delete an honest signal rather than relocate a
history. **Flagged for Pablo's decision**, not acted on.

### A claim of mine, withdrawn

Earlier in this session I reported that ch10's sidebar label `ε₀ = 1/3 (Gronwall, outer)` was a
correction that "reached the prose and missed the sidebar", citing the commit *"Remove Gronwall
framing; relabel ε₀ as Lyapunov stability radius."* **That was wrong.** All six Book 4 files
mentioning Gronwall use the name correctly: ch04 lists it among the tools of the original proof;
ch09 and ch10 say r* was established *against* the symmetric Gronwall estimate, which is the
accurate history; ch10:292 states a true theorem; ch10:539 is the Lean declaration
`gronwall_outer`, which must not be renamed; hub.html records that the symmetric Gronwall ball
is wrong on the inner side. The commit in question corrected one page and never claimed a
corpus-wide sweep. I inferred a scope that was not asserted — the same error the WP-61 entry
above is about, committed while acting on it.

### Still open

- **Twelve Book 4 files claim Lean verification** — `ch-build-2river`, `ch-hawking`, `ch02`,
  `ch06`, `ch06b`, `ch08`, `ch09`, `ch10`, `ch11-catgt`, `ch11`, `ch12`, `ch13`. Each needs
  checking against what the kernel actually reports. This is where a ✓ on a false statement
  would live, and it has not been done.
- **Seven `chIV-*` files hold 170–250 words of prose each** — axioms, correspondence,
  emergence, field, operators, recursion, time. Placeholders carrying chapter names.
- `ch15.html` (223 words) and `ch15-complex-turn.html` (3,784) both claim chapter 15.

---

## 2026-08-30 · Book 4 §12.2: the open note answered — c is the Riemann–Siegel theta derivative

**Provenance.** The note left on the page an hour earlier read: *"What is needed: the
corresponding law for c(σ,t) and the d𝑈̃ component, and then the identification of the
resulting 1-form."* Pablo: *"there are notes in the book you left for me — we can try doing
that now."* This entry records what came out.

### Result 12.2
Taking real parts of ζ'/ζ(s) = χ'/χ(s) − ζ'/ζ(1−s), with c even in t:

    c(σ,t) + c(1−σ,t) = −Re[(χ'/χ)(σ+it)]

A **sum** law, where g obeys a **difference** law. Verified to 30 digits at seven points
(σ ∈ {0.3, 0.5, 0.8, 1.1, 1.5, 2.3}; t from 1.2 to 25).

On σ = ½ the two terms coincide and it collapses to a closed form:

    c(½,t) = ½[ Re ψ(¼ + it/2) − log π ]  =  ϑ'(t)

**ϑ is the Riemann–Siegel theta function.** Verified to 25 digits at t = 0.7, 3, 6, 10, 25,
40, 100 — agreement exact at four of the seven, ≤ 2.6e-26 at the rest.

### Why that matters, and it is not internal to the framework
The Riemann–von Mangoldt formula is N(T) = ϑ(T)/π + 1 + S(T). So the d𝑈̃ coefficient of
α_arith, restricted to the critical wall, **is the density of the zero-counting function**, and
its integral along the wall counts the zeros. Checked: ϑ(T)/π + 1 gives 1.378 / 9.423 / 29.002
against actual counts of 1 / 10 / 29 below T = 20 / 50 / 100, the gaps being S(T) as expected.
On that line the contact form is not *analogous* to classical analytic number theory; it is
classical analytic number theory in a different alphabet.

### The coefficients divide the labour completely
At a zero ρ = ½ + iγ, ζ'/ζ has a simple pole, and along the wall s − ρ = i(t−γ) is purely
imaginary — so the pole lands **entirely in g and not at all in c**. Measured:
g(½, γ₁+δ) = −10.076 / −100.08 / −1000.08 / −10000.08 / −100000.08 for δ = 1e-1 … 1e-5, a
simple pole of residue −1; c converges quietly to ϑ'(γ₁) = 0.4052744. So on the critical line
**c is prime-free, smooth, and counts; g carries every pole, one per zero.**

This gives §12.6's "each zero is a fold singularity" a precise and checkable form: the
singularity is a simple pole in the d𝑉̃ component, and the d𝑈̃ component is analytic across it.

⚠️ **One numerical trap, recorded so no one repeats it.** Evaluating c *exactly at* t = γ₁ by
numerical differentiation of ζ returns 0.342444, not 0.405274 — mpmath is differentiating
across a pole. The closed form is right and the limit from δ = 1e-5 confirms it to six digits.
**Do not quote the at-the-pole evaluation.**

### Status
All of the above is **numerical, not proved.** `GTCT/book4/ZetaReflection.lean` states Result
12.1 as `reflection_law` carrying `sorryAx`; Result 12.2 is not yet in the file at all. The
Mathlib pieces for the ϑ identification exist — `Complex.digamma` and
`riemannCompletedZeta_one_sub` — so it is formalisable, and it is a better first target than
Result 12.1 because it needs no contact geometry.

### Interpretation — deliberately left open
Pablo reads new mathematics toward applications first. Both readings are available here and
neither has been written into the chapter yet:
- **Applied.** c(½,t) has a closed form in gamma factors, so any numerical scheme working with
  α on the critical line can use ϑ'(t) instead of evaluating ζ'/ζ — which is expensive and
  unstable precisely where it matters, near the zeros. The singular part is isolated in one
  component with a known residue, which is the standard precondition for subtracting it off.
- **Pure.** The 1-form separates the counting function from the zeros into different
  components of the same object. If RH is "the critical line attracts", then whatever does the
  attracting is carried by g alone; c contributes nothing to it and is fully classical. That
  splits the conjecture along a seam that was not visible before it was written as a 1-form.

---

## 2026-08-30 · ch-lambda-criticality: the ✓ on a false statement, moved off the page

**Not my finding.** This was found and corrected on the page by another session earlier today,
under a different account, while repairing `GTCTsorryFree.lean` in TOTOGT/GTCT. It is recorded
here in full and removed from the chapter, per the rule that a draft-book page carries the
corrected statement and this log carries the history. Nothing below is new work; it is a
relocation.

### The defect
Chapter λ previously stated that the dm³ potential V(q) = q³ − 3q **has a double root at q = 1**,
and displayed a Lean theorem `fold_double_root_at_unity` asserting `V 1 = 0` — **with a ✓ beside
it.** Both were false. V₃(1) = −2, so q = 1 is not a root of V₃ at all, and no theorem asserting
`V 1 = 0` can have been kernel-checked. A tick mark on a false statement, on a live page.

### What is true, and is what the page now says
c = 3 is the unique coefficient for which q = 1 is a *critical point* of V_c
(V′_c(1) = 3 − c = 0 ⟺ c = 3), and it is *non-degenerate* since V″(1) = 6 ≠ 0 — precisely the
Whitney A₁ condition. The double root belongs to the *shifted* potential
V(q) − V(1) = V(q) + 2 = (q−1)²(q+2).

### Why the notice was eighteen days late
The same error was found and corrected on **2026-08-12** by the sweep published as
**WP-61 · The Root-Language Sweep**, which fixed Chapter π–Ω and Chapter η. **This page was
missed**, and so was the Lean: `GTCTsorryFree.lean` §1 carried the identical false claim in
formal form. The sweep reached neither. That is the WP-61 lesson twice over — a correction
sweep must name the file set it searched, and that set must span every format the claim appears
in, prose and Lean alike.

### How it surfaced today
Not by review. **CI caught it sideways.** `tools/terms.py`, the vocabulary guard, flagged
`PRECISION OF THE ROOT LANGUAGE (LATE)` — the notice's own heading — as an undeclared
expansion-plus-acronym, and failed run #341 on commit `f3979f5`. The guard was written to catch
confabulated vocabulary; it caught an erratum heading instead, and in doing so pointed at the
one chapter page still carrying a correction notice. An instrument finding something it was not
aimed at is worth recording as such.

### The other half of that CI failure
`Risk Reduction and Management Authority (NDRRMA)` from `book6/wp-86-rasuwa-lhende.html` was
also flagged. That one is a genuine external proper noun — Nepal's National Disaster Risk
Reduction and Management Authority — and is now declared in `TERMS.md` (line 116, between RCSR
and Saddle-node), which is what the baseline is for. Guard now reports: *149 declared terms, all
present; 2 disowned terms, mentioned only where declared.*

### Still open
`GTCTsorryFree.lean` was repaired in GTCT, but that repo's kernel check builds `GTCT/GCTC/` only
and root-level files are outside the build. The repair has therefore not been verified by CI —
only locally, by the session that made it.

---

## 2026-08-30 · The counter-example we had not written down: what the geometry does not determine

Pablo asked whether tonight's observation had been recorded anywhere. It had not — it existed
only in conversation. Recording it, because it bears on a live grant document.

### The observation
`HVEH/contact-geometry.html` states: *"The basin hierarchy ε₀=1/3 < r*≈0.776 < κ*≈0.882 < 1
demarcates three nested zones: the inner laminar core, the transition annulus, and the outer
turbulent boundary. **All three are determined by the contact geometry alone.**"* The same
sentence sits in `_to_delete/superseded-copies/HVEH_proofs/contact-geometry.html`.

Chapter 12 is a counter-example to that *style* of claim, from inside the same framework. There,
the distinguished locus is not picked out by the contact structure. It is picked out by the
**gamma factor**: the constraint g(σ,t) = g(1−σ,t) holds exactly where Im[χ'/χ(σ+it)] vanishes,
and that happens on σ = ½ because the two digamma arguments ¼ ± it/2 are complex conjugates
there. Nothing in α = c d𝑈̃ − g d𝑉̃ knows that. The wall is located by an analytic input from
outside the geometry, and the geometry then carries the consequence.

### Why it matters beyond the phrasing
If the arithmetic instance of this framework needs an external analytic input to locate its
distinguished set, the burden is on the hydrodynamic instance to show that its three zones do
**not**. They may not — ε₀, r* and κ* could well follow from the ODE and the contact condition
alone. But r* itself was obtained *numerically*, by bisection to 10⁻⁷, and ch10 records that a
closed form for it "remains an open analytic problem". A boundary whose value is only known by
bisection is not obviously "determined by the geometry alone" in the sense a reviewer will read.

### Recommended repair, not yet made
Either show the derivation, or weaken the sentence to what is defensible: the three zones are
*located within* the contact-geometric model, with r* determined numerically. On a $350,000
NJDEP Resilient NJ narrative the difference between those two sentences is the difference
between a claim that invites a proof request and one that does not.

### Status
Not acted on. `HVEH/contact-geometry.html` is unchanged; this is a flag for Pablo, not an edit.

---

## 2026-08-30 · The preprint was never deposited — updated to v2 and readied

`RH_arithmetic_contact_structure.md` — 326 lines, full abstract, MSC 11M26 / 53D10 / 11R56 /
81Q10, nine sections, two appendices, comparisons to Weil, Connes and the function-field case —
was committed **10 June 2026** (`f116d5e`, "Add files via upload") and **never touched again, and
never deposited.** It is the most complete statement of the arithmetic-contact framework in the
corpus and the only substantial piece carrying no DOI.

**Priority evidence that already exists:** `book4/ch11.html` and `ch12.html` public since
**9 June 2026**, manuscript since the 10th, all with git history. Public and timestamped, but
not citable.

**Literature check, 2026-08-30.** No prior work found formulating a contact form on the critical
strip with von Mangoldt coefficients, or asking whether the functional equation is a
contactomorphism. Nearest neighbours: a Gaussian–Perron prime-side defect comparing a smoothed
prime force with ζ'/ζ (2607.04316); an extension of the Riemann–Siegel Z function off the line
(2107.03191); spirals and curvature of ζ via Voronin universality (2306.00460). The framework
appears unoccupied. **The identity c(½,t) = ϑ'(t) is not** — it is equivalent to Z(t) being real
and is credited as such in the text.

**Updated to v2 today.** New §4.4 (the pole is one-sided, with proof and residue), §4.5 (both
reflection laws, the ϑ' corollary with its classical credit, and Proposition 4.6 refuting the
contactomorphism conjecture), §4.6 (status-of-claims table). Abstract's "No new theorem is
proved" replaced by a precise statement of what the revision adds. The manuscript used the
single-coefficient form α = dV − g dU; the new material is what justifies Book 4's
two-coefficient form, since "g → ∞" cannot say what stays finite.

**DOI reserved for v1: 10.5281/zenodo.22179684.** Not yet published — the deposit is pending and the DOI will not resolve until the record goes live. This is the first deposit of this manuscript; the v2 material described above is intended to go up with it, or as a second version.

## Errata belong here, not in the manuscript — 30 August 2026

Editorial rule, set by Pablo: **the book chapters are draft manuscript pages a
publisher will read. Correction notices do not belong on them.** The mathematics
on the page must be right; the story of how it came to be wrong belongs in this
log.

Three chapters still carried the red `CORRECTION NOTICE` banner from WP-61
(2026-08-12). Removed today, with the corrected mathematics left in place and
verified to stand on its own:

| page | banner | inline `[CORRECTED …]` | correct statement retained |
|---|---|---|---|
| `ch-recurrence-ladder.html` | removed | 1 removed | yes |
| `chapters-pi-phi-mu-eta-delta-sigma-omega.html` | removed | 1 removed | yes |
| `ch-eta-dnls.html` | removed | 1 removed | yes |
| `ch-lambda-criticality.html` | already swept | — | yes |

Each page was checked **before** the banner came off, because on a page whose
body had never been rewritten the banner would have been the only place the
true statement appeared — removing it would have silently reinstated the false
claim. All four bodies carry it independently: `q = 1` is a non-degenerate
critical point of `V₃`, not a root (`V₃(1) = −2`), and the double root belongs
to the shifted potential `V(q) + 2 = (q−1)²(q+2)`.

Corpus-wide check after the sweep: **zero pages assert the false form.**

### The rule
1. A correction is **published in this log**, with its date, its cause, and the
   file set it touched.
2. The chapter is **silently corrected** — the prose, the figures, and any Lean
   snippet quoted in it.
3. No errata banner on a manuscript page. A reader of the book should meet the
   mathematics, not the repair history. A reader of this log should be able to
   reconstruct every repair.

This is not the corpus hiding anything: the log is public, versioned, and named
from the repository root. It is the difference between a printed erratum slip
and a marked-up galley proof.

### Note on concurrent sessions
Another session was working this repository at the same time and had already
swept the banner from `ch-lambda-criticality.html` (commits `b38d5fd`,
`f3979f5` — "corrections logged, not posted", "notices swept into the log"),
while keeping the corrected `fold_critical_at_unity` /
`shifted_double_root_at_unity` snippet written earlier today. Verified before
touching anything; nothing of that session's work was overwritten.
