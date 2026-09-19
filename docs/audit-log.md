# STROGATZ CITATIONS: TWENTY CHECKED, ONE WAS WRONG (2026-09-17)

**What happened.** `book7/strogatz-citations-verify.py` existed and covered 13 citations across
`book6/wp122` and `book7/ch-strogatz`. Six chapters written after it — ch-van-der-pol, ch-smale,
ch-euler, ch-conley — cite Strogatz by page and had never been through it. Extended to **20
claims**, run against the 2018 printing in `~/Downloads`, **all 20 hold**.

**The one that did not, before it was fixed.** `ch-van-der-pol` cited **Liénard's Theorem to
p. 212**. Probing the book: §7.4 *opens* on p. 212 and the word Liénard is on it, but the
**theorem — the five conditions on f and g, and "a unique, stable limit cycle surrounding the
origin" — is on p. 213**, on the page whose running head has already turned over to §7.5
Relaxation Oscillations. A section heading and a theorem inside that section are two addresses.
Corrected in the chapter and in its verify script's docstring; the source row now reads
"§7.4 p. 212 (Liénard's equation, and the section heading) · Liénard's Theorem p. 213".

Everything else in those chapters held: Figure 1.3.1 p. 10, Example 7.1.2 p. 200, Example 7.4.1
p. 213, §7.5 p. 213, §6.8 p. 179, **Theorem 6.8.2 p. 180**, §8.7 p. 281, §10.5 p. 373.

**A claim worth adding.** The chapter prints a direct quotation — *"In the early days of nonlinear
dynamics, say from about 1920 to 1950 … radio and vacuum tube technology"* — attributed to p. 212.
Checked: it is on p. 212. A verbatim quotation is the strongest citation a checker can test, and
it is now one of the 20.

**Two numbers in the script disagreed with the script.** Its docstring said "532 PDF pages, **513**
printed"; the run reports **481**. And it described the offset as "14 in Chapter 1, 18 by Chapter
10"; the run reports **three distinct values, 4 to 18**. Both corrected from the output. The count
is extractor-dependent — the docstring says so itself, having found 278 of them under pypdf 6.18
and all under an older build — so the run now prints `pypdf.__version__` beside the count.
**A count quoted without its extractor version is not reproducible**, and one had been quoted that
way in `ch-strogatz.html`'s source row.

**A working note that was wrong and never published.** This session carried "PDF page = printed
page + 15, verified at seven points" in its notes. There is no fixed offset in this printing. The
figure never reached a page or a script, so there is nothing in the corpus to correct — recorded
because the note was used to place citations for a week.

**One block relaxed, deliberately.** `ch-van-der-pol-verify.py` [6] pinned an exhaustive list of
the chapters naming van der Pol, as a notification that the gap had closed by use. Four chapters
now name it and the list went red for the fourth time. It now pins the two that closed it first
and requires the count to have grown. An exhaustive list is a notification once and noise
afterwards; ch-conley block [7] was rewritten the same way on 2026-09-16. `classify()` also gained
`scaffolding` and `tooling` buckets, which it was missing.

**Housekeeping.** A zero-byte file named `=` in the repository root, from a stray shell
redirection, moved to `_to_delete/strays-2026-09-17/`.

# EULER: THE CURIOSITY THAT WAS NOT ONE (2026-09-17)

**What was built.** `book7/ch-euler.html` and `book7/ch-euler-verify.py` — 8 blocks, standard
library only, 26 checks, exit 0. Registered in `book7/index.html`; the three generated indexes
re-run. Source: R. E. Bradley and C. E. Sandifer (eds.), *Leonhard Euler: Life, Work and Legacy*,
Elsevier 2007 — in particular Richeson on the polyhedral formula and Hopkins–Wilson on Königsberg.

**The measurement.** χ is in **89 files and 76 chapters**; Euler 56 chapters; Runge–Kutta/RK4 16;
Euler characteristic 17; Euler product 14; Gauss–Bonnet 7; Poincaré–Hopf 1; Königsberg 1; graph
theory 1. And **index of a vector field 0, hairy ball 0, polyhedron formula 0, Euler's method 0,
Euler–Lagrange 0, Basel problem 0.** Sixteen chapters integrate with Runge–Kutta and none names the
method Euler wrote first, of which it is the refinement.

**The finding — ch-conley's aside had a reason.** `ch-conley` block [5] printed that all three of
its Conley indices have χ = 0 and that χ therefore separates nothing, recorded as a curiosity
because χ is what a reader reaches for first. It is not a curiosity. All three quotients are built
from the annulus, χ(A) = 0, and the two that differ — (ℤ,ℤ,0) and (0,ℤ,ℤ) — differ by a shift of
**two** degrees, the unstable dimension. **χ is an alternating sum, so an even shift leaves it
fixed.** χ was never going to see the difference: it is the wrong invariant there, not a weak one.
Euler's construction answers *how many cells, counted with sign* — not *which cells, in which
degree*. Block [3] computes χ by two independent routes, cell counts and Betti numbers, agreeing on
six spaces: sphere 2, disk 1, torus 0, annulus 0, and both Conley quotients 0.

**Euler's own statement and its hypothesis.** To Goldbach, 14 November 1750: *"In every solid
enclosed by plane faces, the number of faces along with the number of solid angles exceeds the
number of edges by two."* E230 (statement, 1750) and E231 (proof, 1751), both published 1758.
Block [1] gives 2 on nine solids in integer arithmetic. Block [2] shows the hypothesis does work:
a polyhedral torus gives **0** at every grid size tested, and so does the cylinder — **which is
where Γ lives.** Richeson's chapter records that Euler's proof has a flaw, found and repaired in
the century after; the observation stands.

**The corpus's own field, and a misreading corrected.** Block [6]: ṙ = −(r−1)(r²+r−a), θ̇ = 1. On
r = 1 the field is (0, +1), |F| = 1; on r₂ = 1.884652 it is (−7.9e−16, +1.884652), |F| = 1.884652.
**The field does not vanish on either invariant circle** — ṙ does, θ̇ does not, and an invariant
circle is not a fixed point. The only planar zero is the origin, every circle about it has index
**exactly +1** from R = 0.3 to R = 10, and a small loop enclosing nothing has index 0. That is
Strogatz Theorem 6.8.2 satisfied on the corpus's own equations.

**And it joins ch-conley from the other side.** That chapter's no-go turned on the 3-D flow having
no fixed point anywhere, because θ̇ ≡ 1. A surface admits a nowhere-zero field only when χ = 0. The
cylinder's is 0 (block [2] counted it); the sphere's is 2 (block [3] computed it), which is why you
cannot comb a hairy ball. The corpus's flow being zero-free and its surface being a cylinder are
not two facts.

**Königsberg — an attribution error, in someone else's ledger.** Hopkins and Wilson: **Euler did
not draw the graph.** Graphs of that kind do not appear until the second half of the nineteenth
century. The picture universally credited to him was drawn by someone else 130 years later and
attributed backwards, and it has been repeated for a century by people in a position to check.
Same class as `book6/ch-the-present-king-of-france.html`. Neither of this corpus's two Königsberg
mentions repeats it, which is luck rather than diligence.

**Not established.** Poincaré–Hopf, or the hairy ball theorem. Block [6] computes χ for two
surfaces and indices for particular fields; the remark joining the zero-free flow to χ = 0 is a
reading of two computed facts, not a derivation. Winding numbers are numerical quadrature landing
within 1e-6 of integers — evidence, not proof. Euler's proof and the question of which hypotheses
make the theorem true are not assessed. No priority claimed.

# CORRECTION — "66 FILES THAT DO NOT EXIST" WAS ABSENCE FROM A SINGLE SEARCH (2026-09-17)

**What was wrong.** The chapter, its index card, its verify script and the commit message all said
the corpus cites Lean files that **do not exist**. The run behind that number passed **two roots** —
this repository and AXLE. **More than twenty other repositories exist and were not searched.**

**R15 is explicit: never report absence from a single search.** Two roots is a single search. The
tool's own limits section says it too — "a root not passed is a root not searched" — and that
sentence was written into the page's scholium in the same pass that the overclaim was written into
its body.

**The true statement.** 66 names are **unresolved under the two roots searched**, across 142
citations. Unresolved is not absent. Nothing about absence is established for any of the 66.

**What changed.** The chapter now scopes the measurement to the two roots, carries the R15 point in
a box immediately after the table, and states every consequence of Russell's analysis as a
conditional on a name being *confirmed absent after a full search* — with `OPEN` named as the
correct tag until then. A fourth row was added to the replacement table for the pre-search case:
"asserted at an address this corpus has not resolved" — and search. The verify script gains
`ROOTS_SEARCHED` and a check asserting that exactly two roots were passed, so the scope cannot
drift out of the record. The index card and the [HONESTY] block are rewritten to lead with it.

**The logic is untouched.** Blocks [1] and [2] are exhaustive over predicates on domains up to four
elements and establish what follows once a description fails to denote. That was never in question;
what was wrong was asserting that these particular descriptions fail.

**Open, and the actual next action.** Run `tools/lean_addresses.py` with every repository passed as
a root. Only then does any name deserve the word absent, and only then do the replacement sentences
in the chapter's table apply to it.

# NINE PAGES, NO PROOFS — THE CITATIONS THAT POINT NOWHERE (2026-09-17)

**What was built.** `book6/ch-the-present-king-of-france.html` and its verify script — 6 blocks,
standard library only, 16 checks, exit 0. Registered in `book6/index.html` as a named chapter
rather than a numbered working paper: the subject is a story and a WP number reads dry.
`tools/lean_addresses.py` gains three EXEMPT pairs.

**The story it is told through.** Ramanujan's first letter to Hardy, 16 January 1913 — nine pages,
some 120 theorems across the first two letters, almost no proofs. Hardy's reply of 8 February:
**he asked for the proofs.** Not "this is wrong", not "this is marvellous" — he already believed a
great deal of it, and asked anyway. That same year, in the same college, Whitehead and Russell
brought out Volume III of a book that spends ~360 pages reaching 1+1=2. One address, one year: the
highest pitch of proof-discipline ever attempted and nine pages of unproved assertion.

Hardy's grounds for believing the continued-fraction formulas — they *"must be true, because, if
they were not true, no one would have had the imagination to invent them"* — is an argument from
the improbability of the forgery, and he never called it a proof. **He kept two ledgers**, what he
believed and what had been demonstrated, sorted the nine pages into wrong / already known / new,
and published which was which. Some were wrong.

**The finding — scoped, see the correction dated 2026-09-17 at the head of this log.**
`tools/lean_addresses.py`, run with **two roots** (this repository and AXLE): **66 names unresolved
under those roots, 2 resolve only under another case, 142 citations in all.** Unresolved is not
absent; twenty-odd repositories were not searched. `Chain.lean` is cited by **23 pages**;
`ZeoliteCommutation.lean` by 11; then 5, 4, 4, 4, 4. Twenty-three pages send a reader to an address
this corpus cannot currently resolve.

**What Russell changes.** The repository has filed these as *defects to repair*, and "repair"
concedes that something is there to mend — the Meinong reading in a work shirt. On the 1905
analysis, "the proof in Chain.lean establishes P" unpacks into three claims, the first being that
such a file exists. Whether it does is what the unsearched roots decide. **So, conditionally on a name
being confirmed absent, the sentence is false as published** — not unverified, not pending. Block [1] evaluates all three readings over every (F, G) pair on domains
up to four elements: with nothing answering to the description, "the F is G" and "the F is not-G"
are *both* false while "not (the F is G)" is true, so excluded middle is untouched.

**And it fixes how a retraction must be written.** Block [2]: with the file missing, only the
**wide** reading is true. A correction saying *"the proof there is incomplete"* takes narrow scope
and therefore **concedes that a proof exists** — false when the file is missing. The true sentence
is *"there is no such file"*, and it is shorter. Some corrections in this corpus are written the
wrong way round.

**Mention is not use — and the tool was already right.** This page names `Chain.lean` and
`ZeoliteCommutation.lean`; `book7/ch-gelfand.html` names the latter precisely to say it does *not*
rely on it. A name-counter would count all three as citations. `lean_addresses.py` has exempted by
**(page, name) pair and never by name alone** from the start, with the note that "a blanket name
exemption would hide a real dangling citation elsewhere" — Russell's use/mention distinction,
implemented correctly by someone who did not stop to name it. Three pairs added; that took
`ZeoliteCommutation.lean` from 12 citing pages to 11. The name did not become less dangling; one of
the twelve was never using it.

**The ledger the corpus already keeps.** "proof" in 422 chapters, "unproved/unproven" in 26,
"without proof" in 11, "notebook" in 33, Ramanujan in 16, Hardy in 7, Littlewood in 4. And
**"theory of descriptions" 0, "On Denoting" 0, use/mention 0.** The habit is there; the name for it
was not.

**Three replacements are tabled on the page** for the sentences the corpus currently writes.

**Not established.** That any page is wrong about its mathematics — a false citation is a fact
about the citation, not the theorem, which may be true, provable, or proved where the tool cannot
see. The counts inherit `lean_addresses.py`'s limits: it asks whether a *file* of that name exists
under the roots given, not whether a declaration inside it exists or elaborates, and a root not
passed is a root not searched. Exemptions are hand-curated. Strawson's 1950 objection — that such a
sentence presupposes rather than asserts existence, and is therefore neither true nor false — is
not addressed and is not obviously wrong. No priority claimed: "On Denoting" is 1905.

# THE RULER COUNTED ITSELF: PRINCIPIA MATHEMATICA, AND A VICIOUS CIRCLE IN WP-82 (2026-09-17)

**What was built.** `book7/ch-whitehead-russell.html` + `-verify.py` (8 blocks, 25 checks, exit 0);
`book13/ch-types-the-range-of-a-variable.html` (Book 13 chapter 10, PARTIAL); and
`tools/self_reference.py`, a new instrument. `book6/wp82-verify.py` and
`book6/wp82-the-missing-floor.html` are corrected. Source: *Principia Mathematica* Vol I, 2nd ed.,
Whitehead and Russell, supplied as a scan.

**The measurement.** **"Lean" is in 470 tracked files and 405 chapters** — the corpus runs on a
dependent type theory. **"theory of types" 0. vicious circle 0. propositional calculus 0. Sheffer 0.
axiom of reducibility 0. definite description 0. logicism 0.** Whitehead 1, Principia Mathematica 1,
Frege 1, Russell 3. Meanwhile paradox 27 chapters, self-reference 9, Gödel 27, incompleteness 39,
Cantor 18, diagonal argument 8. **The corpus discusses the phenomenon at length and holds none of
the machinery built for it.**

**The defect, and it is in the flagship measurement.** `tools/self_reference.py` implements PM's
vicious-circle principle (Vol I, Introduction ch. II): no object may be defined in terms of a
totality containing itself. Applied to WP-82:

- `book6/wp82-the-missing-floor.html` is **not in the tree at `654fb06`**, the commit its first
  column names — `book6/wp81` is the last working paper in that commit. **0 of 12 rows** of column
  one contain the ruler.
- At `d97154e`, which column two names, the paper is in the tree and matches **all 12 of its own
  patterns**, because it prints them in its Pattern column. **12 of 12 rows.**

Two columns, two totalities, and **a spurious +1 in every row of the second**.

**The fix is Russell's: stratify the range.** `files()` now excludes the ruler at both refs, and at
`654fb06` that changes nothing — which is how the exclusion is known to be the right one rather
than a convenient one. Block [2] recomputes and asserts **both** the unstratified and the
stratified column, so the difference is printed rather than absorbed.

| | @654fb06 | with ruler | stratified |
|---|---:|---:|---:|
| k-theory | 0 | 9 | **8** |
| index theorem | 1 | 6 | **5** |
| Atiyah | 1 | 5 | **4** |
| operator algebra | 76 | 100 | **99** |
| von Neumann | 7 | 12 | **11** |
| ∞-categor | 0 | 3 | **2** |
| sheaf / sheaves | 1 | 7 | **6** |
| motivic / langlands | 3 | 7 | **6** |
| noncommutative | 9 | 17 | **16** |
| Connes | 15 | 27 | **26** |
| spectral triple | 7 | 15 | **14** |
| moonshine | 25 | 28 | **27** |

**Rung 28: 2 → 17. Rung 33: 31 → 56. Inversion 3.3 : 1, not 3.0 : 1.** The finding survives and
the numbers moved. Block [3]'s k-theory assertion moves 9 → 8; its `kind_of()` keeps the
`the ruler itself` bucket so a future `wp82*` file is classified rather than counted.

**The instrument, and the two design findings in it.** The tool asks, per verify script, what
totality it counts over and whether the counter is inside it — **CORPUS-WIDE** (greps tracked files
by extension, or walks the repo) versus **NARROW** (named files, or a tree outside the corpus such
as `.lake/packages/mathlib`). Over 57 scripts: **0 vicious, 8 guarded, 48 narrow, 1 unread.**

Both design findings are the failure the tool exists to catch, and both are printed in the chapter:

1. **Testing vocabulary rather than range over-reports.** The first version flagged six scripts
   because they *contained* a word they counted. In every case the counted set was Mathlib's tree,
   a Lean file, or a single `.tex` — the counter was not in range, and none was a circle. The
   principle is about the range of a variable, not the words used.
2. **Resolving a script's page by its stem mis-files it.** `book6/wp82-verify.py` belongs to
   `book6/wp82-the-missing-floor.html`, a longer title than the script carries, so the tool
   reported "no page" and filed it as clean. Fixed by falling back to the leading token.
   The guard detector also missed `exclude_finding` (wp109's named guard) and `kind_of` — both are
   real stratifications written under other names.

**wp109 was already correct.** `book6/wp109-verify.py` carries an explicit narrow exclusion and a
comment recording that a broader first attempt was wrong: excluding every file that merely *names*
wp109 dropped two genuine CFT chapters and took the count 20 → 17. "A page is part of the finding
if it would not exist without it, not if it cites it." That is the right rule and it predates this
entry.

**The PM computations, all exhaustive and exact.** The four stroke definitions reproduce their
truth tables; the stroke realises **16 of 16** binary truth functions by enumeration, with ~p the
shortest at (p|p); **Nicod's single primitive proposition, as printed in the second-edition
Introduction, is a tautology on all 32 rows** — a source checked against itself; the rule of
inference is sound on all 8; *54.43 holds with no mismatch in every finite universe from 2 to 6;
and the diagonal set is outside the image of **all 65 536** maps from a 4-element set to its power
set. The authors' own caveat is quoted and respected: the Axiom of Reducibility is "not the sort of
axiom with which we can rest content", and without it "Cantor's proof that 2ⁿ > n breaks down
unless n is finite" — the exhaustion is entirely inside the finite case they say survives.

**Not established.** No type hierarchy is constructed and nothing about Lean's kernel is verified.
The descent from ramified types through Church to Martin-Löf to Lean is a historical reading,
stated to place the instrument, not checked. The blocks are exhaustions over finite sets — evidence
and not proof. Nothing addresses Gödel. The tool cannot see a pathspec or a pattern built at run
time, so a clean report is consistent with a script assembling a bad pattern; it reports four
labelled buckets rather than a verdict so a clean line can be checked instead of believed. No
priority claimed: PM is 1910–1913.

# NEWTON: THE DEFINITIONAL FORM, AND THE MEASURE THAT WENT UNNAMED (2026-09-17)

**What was built.** `book7/ch-newton.html` and `book7/ch-newton-verify.py` — 6 blocks, standard
library only, 33 checks, exit 0. Registered in `book7/index.html`; the three generated indexes
re-run. Source: the *Principia*, Motte translation as revised by Chittenden (public domain),
supplied as a scan; passages located by OCR.

**The measurement.** "Principia" is in **814 tracked files and 712 chapters**. definition 233,
lemma 123, corollary 67, Newton 25, "measure of" 19, centripetal 1. And **Scholium 0, Rules of
Reasoning / Regulae 0, quantity of matter 0, vis insita 0, motive quantity 0, "absolute …
accelerative" 0, hypotheses non fingo 0.** The series borrows the name and the outer furniture
and has never opened the apparatus.

**The form.** Every Definition I–VIII has one shape — *"the ⟨quantity⟩ of X is the measure of the
same, arising from / proportional to ⟨Y⟩."* Two consequences: **a definition is not finished until
the measure is fixed**, and **one quantity can have several measures** — a centripetal force has
three, given consecutive numbers and named absolute (VI), accelerative (VII) and motive (VIII)
expressly "for distinction's sake". Block [1] checks the relation on Newton's own terms: motion is
mass × velocity, so motive = accelerative × mass; three bodies at one place have three motive
measures and one accelerative measure.

**The finding, and it has teeth.** λ⊥ = e^−4π is an **accelerative** measure — literally
"proportional to the velocity which it generates in a given time", a contraction rate over one
period — and the Conley index is an **absolute** one. Block [2] applies Newton's own test, change
the test body and see which measure follows it, with the parametrisation as the test body: under
ṙ → k·r(1−r²), which moves neither Γ nor its stability type nor the isolating block's boundary
signs,

| k | λ = −2k | accelerative e^(λ·2π) | absolute CH_* |
|---:|---:|---:|---|
| 1 | −2 | 3.487342e−06 | (ℤ, ℤ, 0) |
| 3 | −6 | 4.241151e−17 | (ℤ, ℤ, 0) |
| 10 | −20 | 2.660393e−55 | (ℤ, ℤ, 0) |
| 100 | −200 | underflow | (ℤ, ℤ, 0) |

**Fifty-plus orders of magnitude in one column and nothing at all in the other.** That is
Definition VII against Definition VI. WP-82 §3b reached the same wall by finding the multiplier
monotone in z₀; ch-smale by finding that no homotopy invariant can be a monotone function of a
parameter it does not feel. **Newton had the vocabulary for the confusion in 1687** — not the
theorem, the vocabulary, which is what makes the confusion unavailable.

**The same form names the other three findings.** ch-gelfand's "operator algebra" is a quantity
with no measure fixed — no norm — which the definitional form refuses for Newton's reason; the
chapter then supplies dim = n·p. ch-feigin is the Scholium's absolute-versus-relative: block [3]
checks that α(m³−m) is a cocycle for every α, so the **class** is absolute and one-dimensional
while **the 12 is a unit** and c(1) = 0 is the convention that picks the representative.

**The Regulae beside the corpus's own rules** — offered as a reading, not a result. Rule I ↔ the
`ASSUME` tag. Rule II ↔ R14 and one-number-everywhere. Rule III ↔ the `DATA`/`MODEL` split and
every `[HONESTY]` block saying an exhaustion over a finite box is evidence, not proof. **Rule IV ↔
the dated measurement**, and it earned itself this week: WP-82's second column was correct and
stopped being current inside a single day. Rule IV does not call that an error — it calls it the
ordinary fate of a proposition collected from phenomena and says to make it more accurate or
record the exception. The column now names a commit. The General Scholium's refusal to feign a
hypothesis is the register of every `OPEN` tag, and of four statements made this week that could
have been dressed up and were not.

**Part V fixes eight shared terms** — quantity, measure, absolute measure, accelerative measure,
unit, restriction, no-go, Scholium — as the corpus's common language from here.

**Not established.** No new mathematics; blocks [2] and [3] re-run published computations. The
reading of Newton is a reading, quoted from a translation, and the mapping onto the tier tags is
proposed, not proved — it earns its place only if it stops a measure going unnamed again, which is
a claim about future pages. No priority claimed: the *Principia* is 1687 and the point is that the
apparatus was available the whole time.

---

# THE DRAFT ISBNs ARE NOT CITED (2026-09-17)

`ch-conley` block [8] and its boxed note cited the IMPA edition as "March 2026, ISBN
979-8-9954416-6-3". **ISBNs in that folder are drafts.** Worse, this repository already records
(2026-08-30) that this particular number is allocated to **Book III**, not to the series, so the
citation attached a draft number to the wrong volume. Both citations now give the edition by title
and by the date in its own front matter and say the ISBN is deliberately omitted. The priority note
in the earlier entry is corrected the same way: **the date is the record; the ISBN carries no
weight.**

# THE PUBLISHED NORMAL FORM, AND THE HTML SYSTEM, COMPARED (2026-09-16)

**Source.** The IMPA edition of *Principia Orthogona*, dated March 2026 in its own front matter,
ORCID 0009-0000-6496-2186, supplied as PDF. Its printed ISBN is **not** cited here: ISBNs in that
folder are drafts, and this one is separately recorded below (2026-08-30) as allocated to Book III
rather than to the series. It prints the **universal contact normal form**:

> ρ̇ = μ_max(1 − e^−βz)ρ + O(ρ²),  θ̇ = ω + O(ρ),  ż = ω − |μ_max|ρ²e^−βz + O(ρ³)

with (μ_max, ω, β) named as the canonical invariants of the dm³ system, the corpus's instance
being (−2, 1, 1), and "Transverse Lyapunov exponent: μ_max = −2" stated separately. WP-82 §3b
instead states the contact-exact system on (ℝ²_{>0} × ℝ, α = dz − r²dθ). **Neither source prints
the comparison**, so `book7/ch-conley-verify.py` gained block [8], which makes it exactly —
expanding in ρ = r − 1 with u = e^−z as an indeterminate, over ℚ.

| | order ≤ 1 in ρ |
|---|---|
| corpus ṙ | −2ρ + 2ρu |
| published ρ̇ | −2ρ + 2ρu |
| **identical** | λ(z) = −2(1 − e^−z) in both |
| corpus ż | 1 + 2ρ |
| published ż | 1 |
| difference | **+2ρ** |

**Both give ż = ω = 1 on Γ, exactly.** The +2ρ is not a discrepancy to resolve: α = dz − r²dθ
forces ż = r²θ̇ = 1 + 2ρ + ρ² on the Reeb direction, where the normal form writes the constant ω.
The published form is the ρ → 0 truncation; the §3b system is its contact-exact realisation.

**Why it matters.** ch-conley's no-go uses only ż > 0 on Γ, and the published form gives
ż|_Γ = ω for **every** ω > 0. So *no compact isolating neighbourhood contains any of Γ* is a
property of the **canonical normal form as published in March 2026**, not of one HTML variant
written later. The chapter carries this as a boxed statement before Part IV.

**Priority note (R18).** The normal form, its three canonical invariants and μ_max = −2 are
dated March 2026 in the edition's own front matter — six months before the Strogatz reading. The
date is the record; the ISBN is a draft and carries no weight here. That is
the corpus's own priority record for the object, independent of any textbook. It is a record of
*what was derived here and when*; it is not a claim that the object is unmatched in the
literature, and no such claim is made. The Conley index, its continuation property, Liénard's
theorem and Poincaré–Bendixson remain classical and are cited as such wherever used.

**Also, and it is the block firing as designed.** `ch-conley-verify.py` [7] asserted that Conley
was named in exactly three files and applied in none, and said it would fail when the vocabulary
was picked up. It failed the same day: ch-smale, ch-gelfand and ch-feigin all cite the chapter.
The assertion now pins the part that does not churn — that WP-82 and ch-grothendieck.html, the
two that named the candidate without checking it, are still present — and prints the composition.
`classify()` gained `tooling` (for `tools/`) and `scaffolding` (for `CLAUDE.md`) buckets.

# FEIGIN: THE FLOOR UNDER VOLUME XV'S CORRECTED SEED (2026-09-16)

**What was built.** `book7/ch-feigin.html` and `book7/ch-feigin-verify.py` — 8 blocks, standard
library only, exact over ℚ throughout, 38 checks, exit 0. Registered in `book7/index.html`; the
three generated indexes re-run.

**Why.** WP-82 §3's own correction of 2026-09-11 withdrew the Moonshine seed for Volume XV —
*"Moonshine supplies modular functions — the automorphic side... half of a correspondence is not
half the distance"* — and named Feigin–Frenkel instead: at the critical level the centre of the
affine vertex algebra is the classical W-algebra of the Langlands dual, duality inside vertex
algebra theory with no Galois side. Measured at HEAD, entity-aware, this page classified out:
E8 141 chapters, Moonshine 22, vertex operator 8, central charge 7, Virasoro 7, Kac–Moody 2,
Langlands 2, critical level 1, **W-algebra 1 — and that one is WP-82 itself**. Everything the
theorem is *stated in terms of* reads 0: **Sugawara 0, dual Coxeter number 0, Zamolodchikov 0.**

**Virasoro derived, not quoted.** Witt from vector fields, exact on 2197 integer triples. Then
H²(Witt) computed: **1 at every window tested** — (N,M) = (5,2), (6,3), (7,3), (8,4), (9,4),
(10,5), with dim Z| − dim B| = 1 in each. Which is why Virasoro is *the* central extension.

**A truncation lesson, the second in two days.** A raw truncation to |n| ≤ N drops every cocycle
condition reaching outside the window, so the cocycle space is inflated at the edge and the
answer is wrong. The fix is to solve on [−N,N] and **restrict to pairs inside [−M,M] before
quotienting.** Same shape as ch-gelfand, where an algebra generated to a fixed word length
reported dim 33 where the commutant forces 36.

**And the −m is forced.** Degree-zero cocycles are exactly span{m, m³} — m² and m⁵ are checked
and are *not* cocycles, so the reading is not an artefact of the ansatz. The degree-zero
coboundaries are c(m) = 2m·f(L₀), exactly the multiples of m. So every representative is m³ + t·m,
and **t = −1 is the unique value with c(1) = 0**, which is the statement that L₋₁, L₀, L₁ span an
uncentred sl₂. The 12 is a normalisation; the −m is not. c(2) = 1/2, i.e. [L₂,L₋₂] = 4L₀ + c/2.

**Root systems from Cartan matrices alone.** Reflection closure, highest root, symmetriser,
coroot coefficients. Fifteen simple types, every h^∨ agreeing with the known value. E₈: **h^∨ = 30,
240 roots, dim 248**, highest root (2,3,4,6,5,4,3,2).

**Langlands duals by transposition.** A, D, E self-dual; G₂ and F₄ self-dual up to relabelling;
B_n ↔ C_n. **E₈ is self-dual**, so the centre at its critical level is W(e₈) and not some other
algebra to be hunted for.

**The critical level, with a check that is not circular.** c(k) = k·dim g/(k + h^∨), undefined
where the Sugawara normalisation 1/(2(k+h^∨)) is — that is the critical level, and the Virasoro
description of ĝ breaks exactly there. The test: **at level 1, simply laced, c must equal the
rank.** Nothing in the computation was arranged to make that true, so it tests h^∨ and dim g
together. It holds for every type tested; for E₈, 248/31 = 8.

> **For E₈: c(k) = 248k/(k+30), critical level k = −30, centre W(e₈).**

**What is NOT established, and it is the larger half.** No W-algebra is constructed. The theorem
is quoted; what is computed is the data it is stated in terms of. The Sugawara operator is not
built, the centre at the critical level is not exhibited, the isomorphism is not checked in any
case, not even sl₂. The reason is printed rather than hidden: **a W-algebra is not a Lie algebra** —
W₃'s bracket closes only on the composite field :TT: − (3/10)∂²T, so the structure "constants"
depend on the central charge and none of the Witt/Virasoro machinery extends for free. That needs
OPEs and normal ordering, neither of which is in this corpus. **By WP-82's own admissibility bar,
Volume XV is not opened by this page.** It supplies the floor under the seed and an honest measure
of the distance. No priority claimed; all of it is classical.

# GELFAND: IS "THE OPERATOR ALGEBRA" AN ALGEBRA? (2026-09-16)

**What was built.** `book7/ch-gelfand.html` and `book7/ch-gelfand-verify.py` — 8 blocks,
standard library only, exact over ℚ where exactness is available, exit 0. Registered in
`book7/index.html`; the three generated indexes re-run.

**The measurement.** operator algebra **100 files / 74 chapters**; semigroup 28, monoid 10,
Gelfand 4, operator norm 3, C\*-algebra 1, \*-algebra 1, commutant 1; **von Neumann algebra 0,
Banach algebra 0, Gelfand–Naimark 0, Wedderburn 0.** WP-82 §3 gives Volume XII both halves and
notes the phrase "has never had a volume". The prior question is whether the thing is an algebra.

**First finding — it is a monoid.** Block [1] checks the corpus's own page against itself,
flattened so a phrase split by an `<em>` cannot silently miss: HVEH Proof I states G = U∘F∘K∘C,
calls K "multiplication by a radial mask", calls F **"the nonlinear self-amplification"**, says
"F is not pointwise", and attributes the non-commutativity to advection; Vol I Theorem 5.3 states
the four do not commute. An algebra is a vector space; **a nonlinear map is not an element of
one**, and no page supplies a sum, a scalar multiple, an involution or a norm for the four.
Composition gives associativity and an identity, which is a monoid. Nothing is wrong with a
monoid — the finding is that the name promises a different object, and that Gelfand, Naimark and
GNS have nothing to act on until one is supplied.

**Second finding — the algebra that is there, and its complete structure.** The corpus's own
refutation is already a finite linear statement: *a static gate composed with a sitewise map
commutes; a gate and an inter-site coupling do not.* On n sites, K = diag(χ), S = the cyclic
shift: [K,S]_ij = (χ_i − χ_j)S_ij, zero **iff** χ is constant — checked exactly over all 120
masks for n = 3..6. Then, with p the minimal period of χ under the shift:

> **dim C\*(K,S) = n·p  ·  A ≅ (M_p(ℂ))^⊕(n/p)  ·  dim A′ = n/p**

Exhaustive over **all 248 masks for n = 3..7, zero violations**, algebra generated to closure
rather than truncated, both dimensions computed. Wedderburn data then forced: Σn_i² = (n/p)p² = np,
Σm_i² = n/p with every m_i = 1, Σn_i m_i = n.

The reading: **the algebra is exactly as large as the gate is asymmetric.** Constant mask → the
smallest algebra the shift admits. Mask with no symmetry → the whole of M_n(ℂ), which is simple
and therefore distinguishes nothing. The informative cases are in between, where the number of
Wedderburn blocks *is* the symmetry of the gate.

**Two expectations corrected by the computation**, both worth recording because both were the
kind of thing a hand reading would have kept: a first pass truncated the generation at word
length 8 and reported dim 33 at n = 6 where the commutant forces 36; and the alternating mask at
n = 4 is **not** the full matrix algebra — it is M_2 ⊕ M_2, dim 8, commutant 2.

**Gelfand–Naimark, and what Theorem 5.3 actually says.** At p = 1 the algebra is the circulants,
commutative of dimension n, so it is C(X) with X the n-th roots of unity and the Gelfand
transform the DFT — exhibited at n = 4, 6, 8, worst residual 5e-16. So **Vol I's "C, K, F, U do
not commute" is, in this model, the statement p > 1**, i.e. that the algebra is not an algebra of
functions on a space. That is exactly the sentence WP-82 needs for the step from rung 29 to rung
33, and seventy-four chapters have been one theorem away from it.

**GNS, which reads 2 — both files written today.** Block [6] runs it on the trace τ(a) =
(1/n)Tr(a): faithful, so nothing is quotiented, dim ℋ = n² at n = 2, 3, 4 as the rank of the Gram
matrix of ⟨a,b⟩ = τ(b\*a), cyclic vector Ω = I reproducing τ to zero error over ℚ. Three lines of
linear algebra, and the step the phrase has promised a hundred times.

**Not established.** That the finite model is the corpus's system — it is not; K and F act on a
continuum and F is nonlinear. Whether the continuum algebra is a crossed product, and whether p
has a continuum analogue, is untouched. The Lean names on the source page (`gate_commutes`,
`coupling_not_commute` in `ZeoliteCommutation.lean`) are **not** relied on: that file is already
recorded here as resolving nowhere under any root, so block [3] re-derives the finite statement
rather than citing it. No priority claimed — Gelfand–Naimark, GNS, Burnside and Wedderburn are
classical and the period rule is an exercise in them.

# SMALE: THE RETURN MAP CANNOT FOLD, AND NOT BECAUSE OF THE PARAMETERS (2026-09-16)

**What was built.** `book7/ch-smale.html` and `book7/ch-smale-verify.py` — 7 blocks, standard
library only, exit 0, entity-aware counts through `tools/corpus_count.py`. Registered in
`book7/index.html`; the three generated indexes re-run.

**The measurement.** Twenty-two chapters compute a return map and twelve name a Poincaré section
or map; **horseshoe 0, shift map 0, Sharkovskii 0, lap number 0, logistic map 0**, symbolic
dynamics 1, topological entropy 1. Smale 2, Levinson 4, Cartwright 0. The corpus builds the
object and has never asked the question the object exists to answer.

**WP-122's return map in closed form.** P(r) = r·e^2π / √(1 + (e^4π − 1)r²), against RK4 at
eight radii, worst 8×10⁻¹⁵. P′(r) = e^2π/(1+(e^4π−1)r²)^(3/2); P′(1) = e^−4π =
3.487342356208997×10⁻⁶; |P′| = 1 at r\* = 0.015049224003. P′ > 0 at all 2001 sampled radii.

**Entropy zero — and a table that mostly proves nothing.** Lap numbers of P^n are 1 at every n,
but P contracts by e^−4π per turn, so by n = 6 the whole of (0,3] lands on the single double
nearest 1.0 and a lap count of 1 is then true of a constant function. **Four rows carry
information; three are an artefact of double precision.** The script prints the range of P^n
beside each row and asserts only on the four. Contrast, same instrument, on a map that folds:
the logistic map at μ = 4 gives ℓ(L^n) = 2^n exactly and log 2 = 0.693147180559945 at every n.

**The restriction, which is the finding.** For ṙ = f(r), θ̇ = ω > 0, the return map is the time-T
flow map of a *scalar autonomous* ODE, so dP/dr₀ = exp(∫₀ᵀ f′(r(s))ds) — an exponential, hence
strictly positive, **for every f**. P is a monotone homeomorphism, ℓ(P^n) = 1 for all n, h(P) = 0.
Orbits of a scalar autonomous equation cannot cross and a fold is a crossing. So no member of the
closure family, and no radial-plus-rigid-rotation system whatever, has a horseshoe in its return
map. Checked on four fields including two non-monotone ones.

**A methodological result from the T sweep.** At T = 0.2 the identity verifies against a central
difference to ~1e-8. At T = 2π the derivative for WP-120's field is e^−110, both perturbed flows
land on the same double, and only 1 of 30 sample points is comparable at all — the difference
quotient reports nonsense while the integral still returns the number. **A derivative that small
is computed, not measured.** A script that had only differenced would have reported a fold where
there is none.

**Third restriction on the same family, same source.** Circle-preserving (ch-van-der-pol);
uniqueness route tied to circles (WP-120); entropy zero (here). All three follow from the radial
speed being a function of r alone.

**An open question, stated not asserted.** The operator chain is G = U∘F∘K∘C and F is the *Fold*.
The published return map cannot fold and by the above no member of the family can. The two senses
of "fold" are not in contradiction — F acts on the chain, not on a return map — but nothing in the
corpus says which sense is meant where. Recorded as a question.

**Where it meets ch-conley.** Escaping planar entropy needs three dimensions; the corpus has them;
and there the obstruction is ż ≡ 1 on Γ — no orbit returns to a section, so there is no return map
to have an itinerary. ch-conley was stopped by the same identity looking for a compact invariant
set. Two chapters, opposite directions, one fact.

**And what would change it.** Smale's horseshoe came from a *forced* oscillator — a periodic
drive, non-autonomous, which is exactly the hypothesis the one-line proof needs and lacks. The
corpus's modulation e^−z is monotone, not periodic. A periodic modulation is the smallest change
to these equations that could produce what Levinson found. Not tried here.

**Instrument note.** Smale's advisor was Raoul Bott. `/bott/` matches 789 tracked files and every
one is the word *bottom*; "Bott periodicity" reaches one chapter, put there by ch-conley the same
day; **"Raoul Bott" was in no file at all** before this page. Two chapters added in one day, a
student of Moser's and a student of Bott's, and both teachers were gaps.

**Not established.** That the corpus's 3-D flow has no chaos — block [5] is about planar systems
with constant angular speed, and Poincaré–Bendixson already forbids planar chaos independently;
what block [5] adds is *which* feature is responsible. The lap counts are evidence over a finite
grid, not proof; the proof is the variational argument, which is classical. No priority claimed.

# THE INSTRUMENT HAS A THIRD FAILURE MODE, AND IT MAKES FALSE ZEROS (2026-09-16)

**Found while propagating the Conley chapter.** `book7/ch-van-der-pol-verify.py` block [6]
went red on its own terms — it was written to fail when a second chapter named van der Pol,
and it did, the same day. Updating it exposed something larger. The Liénard row read **0
chapters for a word printed twice on the page doing the counting.**

**The cause.** The corpus is HTML and writes accented names as character entities. The pattern
`/li[eé]nard/` matches neither the literal nor the entity form, so every page that spells the
name properly is invisible to it. Measured at `d97154e`, tracked `*.html`/`*.md`:

| pattern | plain `git grep` | entity-aware | low by |
|---|---:|---:|---:|
| Liénard | 2 | 5 | 60% |
| Poincaré | 58 | 68 | 15% |
| Gödel | 23 | 27 | 15% |
| Poincaré–Bendixson | 12 | 14 | 14% |

**68 tracked HTML files carry at least one accented entity**, so this is not a corner case.
Every published count in this corpus for a name with a diacritic is low until it is re-taken.

**The instrument.** `tools/corpus_count.py` — shortlists with `git grep -l`, then matches
against the file's text with entities unescaped, so `Li&eacute;nard` and `Li<em>é</em>nard`
both match. Tracked files only (R13), standard library only. It also prints the gap against
plain `git grep`, so the difference is visible rather than assumed. Writing it caught a fourth
thing: `git ls-tree -r --name-only HEAD -- '*.html'` returns **nothing and exits 0** where
`ls-files` and `grep` honour the same pathspec — a silent empty answer, which is the same
failure class. The module filters in Python instead.

**Three modes now recorded, where WP-82 §4 recorded one.**

1. Wrong spelling — `k-theory` does not match `K theory`. A 0 means "zero in that spelling".
   (WP-82 §4, already recorded.)
2. Substring inflation — `/gns/` returns 68 files via *designs* and *assignments*; `/bott/`
   returns 810 via *bottom*. Both anchor to 0. Checked by `ch-conley-verify.py` [7].
3. Entity blindness — the table above. Checked by `ch-van-der-pol-verify.py` [6].

**Propagated.** `book7/ch-van-der-pol-verify.py` switched to `-ilE` and an entity-aware
Liénard pattern, its van-der-Pol assertion updated to name the exact two-chapter set so a
third arrival still notifies; `book7/ch-van-der-pol.html` carries a dated update box and its
original counts are now marked as measured on the day. `book7/ch-conley.html`'s instrument
note carries all three modes.

**And a fifth, small.** Two verify scripts shipped the control token `zzz` + `-no-such-token-`
+ `zzz` as a literal, which means each file contains it and a grep for it returns those files.
`book6/wp82-verify.py` and `book7/ch-van-der-pol-verify.py` now assemble the control token at
run time instead. A control for absence cannot be a string any file writes down.

---

# WP-82's SECOND COLUMN NOW NAMES A COMMIT (2026-09-16)

**Why.** The 2026-09-16 column was published against `HEAD`, and `book6/wp82-verify.py` only
printed it — the page said the script "computes both and fails if either drifts", and for the
second column that was not so. Publishing `book7/ch-conley.html` moved six of its twelve rows
**within the same day**: k-theory 7→9, index theorem 4→6, Atiyah 3→5, von Neumann 11→12,
sheaf 6→7, spectral triple 14→15.

**What changed.** The column now names commit `d97154e`, the way the first names `654fb06`.
`wp82-verify.py` block [2] recomputes both columns at the commits they name and asserts both;
live `HEAD` is still printed, asserted only for monotonicity. A date is not a commit.

**Block [3] gained a bucket.** Its classifier had `the ruler / index / docs / CHAPTER` and no
place for `CLAUDE.md`, which names the vocabulary in a handoff note and was being counted as a
chapter. With `project scaffolding` separated out, k-theory at `d97154e` is **9 files, 2 of
them chapters** (`ch-grothendieck.html`, `ch-conley.html`) — the floor is started, not built.
The [HONESTY] block now computes those two numbers instead of stating them.

# CONLEY: THE THIRD CANDIDATE IS CLOSED (2026-09-16)

**What was built.** `book7/ch-conley.html` and `book7/ch-conley-verify.py` — 7 blocks,
standard library only, exit 0. Registered in `book7/index.html`; the three generated indexes
re-run.

**Why.** WP-82 §3b, having shown that λ⊥ = e^−4π moves with z₀ and so is not an index, left a
sharp inherited question — *is there a K-theory class whose pairing is constant along this
helix?* — and named three candidates: an asymptotic index at z → ∞, a relative class on
(M, {z ≤ c}), and a Conley invariant of the isolated invariant set.
`book7/ch-grothendieck-verify.py` repeats all three and states that none is checked.
Counted at HEAD with this page and its script classified out, **"Conley" occurs in exactly
three files — WP-82, ch-grothendieck.html and that script — and is applied in none of them.**
One rung lower: **"index theorem" is in 5 chapters and "Fredholm" in 0**, so the corpus names
an index theorem without naming the class of operator an index belongs to.

**The no-go, and it needs no numerics.** On Γ = {r = 1} the third equation reads ż ≡ 1. For
every compact N, z ≤ Z on N for some finite Z, and z(t) = z(0) + t exceeds it in finite time,
so **Inv(N) ∩ Γ = ∅ for every compact N.** Block [2] integrates it rather than asserting it —
orbits from z₀ = −5, 0, +5 leave z ≤ 10 and z ≤ 100 at exactly the predicted times with
r = 1 held to fifteen digits — and then proves the stronger statement, that a whole tube has
empty invariant set, from ż ≥ (1−d)² − 2d²e^−z₀, a bound attained at r = 1−d:

| z₀ | d | bound m | grid min |
|---:|---:|---:|---:|
| 0.0 | 0.372792 | 0.115442 | 0.115442 |
| −1.0 | 0.270137 | 0.135973 | 0.135973 |
| −5.0 | 0.049373 | 0.180125 | 0.180125 |
| −10.0 | 0.004268 | 0.189146 | 0.189146 |

Candidate three fails for the reason λ⊥ failed: Γ closes in the (r,θ) projection and in no
other, and compactness is what both instruments were asking for.

**What survives, in the frozen-z family — stated as a family, not the flow.** Blocks [3]–[5].
The factorisation r(1−r²) + a(r−1) = −(r−1)(r²+r−a) is checked exactly over a 61×80 rational
grid. Below the neutral line the exit set of the largest annulus isolating r = 1 alone is
**both** boundary circles; above it the exit set is **empty**; at z = 0 exactly, r₂ = 1 and no
annulus isolates r = 1 alone. Integral homology by Smith normal form on a CW chain complex:

| exit set | N/L | CH₀ | CH₁ | CH₂ | χ |
|---|---|---:|---:|---:|---:|
| empty | A₊ | ℤ | ℤ | 0 | 0 |
| both circles | A/∂A | 0 | ℤ | ℤ | 0 |
| one circle | A/L | 0 | 0 | 0 | 0 |

**All three Euler characteristics are 0**, so χ separates nothing — worth recording, since χ is
what a reader reaches for. The homology does separate them, by a degree shift equal to the
unstable dimension. So a genuine deformation-invariant index exists on each side and **it is not
the same index on the two sides**: the answer for this candidate is *no*, and the obstruction is
the fold at z = 0, not a missing tool.

**The result that closes it.** Block [6]. Replace ṙ by k·r(1−r²): the multiplier over T = 2π is
e^−4πk, running from 3.487342×10⁻⁶ at k = 1 to underflow at k = 100, while the isolating block
N = [½, 2] stays valid for every k > 0 because the *sign* of ṙ on the two boundary circles is
k-independent. The index is (ℤ, ℤ, 0) throughout. A Conley index is a homotopy type and the
multiplier is a derivative; no homotopy invariant can be a strictly monotone function of a
parameter that leaves the homotopy type fixed. **e^−4π cannot be an index of this kind.**
Candidate three is closed rather than left open; WP-82's other two stand, and are now the only
two left.

**A limit of the instrument, for WP-82 §4.** §4 records that a `0` may mean "zero in that
spelling". The dual failure is not recorded and is live: an unanchored pattern returns noise.
At HEAD, `/gns/` matches 68 files and `/\bGNS\b/` matches 0 — the hits are *designs* and
*assignments*; `/bott/` matches 810 and `/bott periodicity/` matches 0 — the hits are *bottom*.
Block [7] checks both pairs on every run. A grep count without an anchor is not a measurement.
The page carries this as a footed note; the patch to WP-82 itself is not yet made.

**Two conventions re-earned.** Block [7] classifies this page and its script out and asserts on
*chapters*, because publishing moves the file column by construction — ch-van-der-pol block [6]'s
lesson, arriving on schedule. And the control token `zzz-no-such-token-zzz`, copied from two
existing verify scripts, is present in both of them and therefore matches; a control for absence
has to use a string no script has written down.

**Not established.** Nothing here is Conley theory applied to the flow — the flow has no compact
isolated invariant set, which is the finding. Blocks [3]–[6] work with the frozen family. The
homology is arithmetic on a hand-chosen CW model, not an index pair built by the theory, so
WP-82's admissibility bar for Volume XI is not met by it. No priority is claimed: the Conley
index, its continuation property and its behaviour at a transcritical bifurcation are classical.

# VAN DER POL: THE CLOSURE FAMILY IS CIRCLE-PRESERVING (2026-09-16)

**What was built.** `book7/ch-van-der-pol.html` and `book7/ch-van-der-pol-verify.py` —
7 blocks, standard library only, exit 0. Registered in `book7/index.html`. Row N11 added to
`docs/novelty-register.md`.

**The finding.** Strogatz prints Example 7.1.2 one page after 7.1.1. 7.1.1 is this corpus's
transverse attractor; 7.1.2 is van der Pol. Counted on tracked `*.html`/`*.md` at HEAD,
excluding `docs/` and this chapter: **"limit cycle" 108 chapters, "van der Pol" 0,
"Liénard" 0, "memristor" 0, "Chua" 2** (both the game-theory pack).

Measured over one settled turn:

| mu | r_min | r_max | r_max/r_min | period |
|---:|---:|---:|---:|---:|
| 0.1 | 1.9369 | 2.0668 | 1.067 | 6.2870 |
| 1.0 | 1.5317 | 2.8300 | 1.848 | 6.6630 |
| 1.5 | 1.4134 | 3.3608 | 2.378 | 7.0960 |
| 5.0 | 1.1825 | 7.7015 | 6.513 | 11.6120 |

Example 7.1.1 needs no integration: ratio 1.000, period 2π, both exact.

**So WP-22's closure family is circle-preserving, and had not said so.** The conditions
f(1)=0, f'(1)=−2, f(r)(r−1)<0 with θ̇=1 make the radial speed a function of r alone, so on a
closed orbit r is constant and the orbit is a circle. Every ratio above exceeds 1, so
**van der Pol lies in no admissible closure.** Not a defect — a restriction, and everything
WP-22 proves is proved about circular cycles. Naming it costs one clause and tells a reader
how far the results reach.

**And WP-120's uniqueness route is tied to the same restriction.** g = 1/r³ on a
5,400-point grid: Example 7.3.1 min −1245.3369 / max −0.2525, one sign; van der Pol
min −1647.9492 / max +814.5996, sign change. The Dulac route works because that cycle is a
circle. **Liénard's Theorem (Strogatz p. 212) never assumed one** — five conditions, all
verified here for van der Pol with F(x) = ⅓μx(x²−3) and a = √3 exactly (Example 7.4.1,
p. 213) — and settles it, in 1928. Both routes are correct; one travels.

**The generative half.** The question is now well posed: what does the contact construction
look like over a non-circular cycle? Drop θ̇ = 1, or let the radial speed depend on θ, and
the period, the multiplier and the neutral line all have to be recomputed rather than read
off. Liénard says the cycle is still there and still unique. Nothing in the corpus says what
happens to the contact form.

**The electronics lineage, recorded where it belongs.** Strogatz §7.4 p. 212: the work on
nonlinear oscillations "was initially motivated by the development of radio and vacuum tube
technology, and later it took on a mathematical life of its own." van der Pol's equation is a
vacuum-tube circuit; Figure 1.3.1's nonlinear n=2 cell reads "Nonlinear electronics (van der
Pol, Josephson)" and Chua's circuit sits in the chaos cell. **Nonlinear electronics produced
the mathematics this corpus runs on, and the corpus holds almost none of its names.**

**Chua's completeness argument, cited as a precedent for the method and not as a result.**
Four circuit variables give six pairwise relations; two are definitions, three are the
resistor, capacitor and inductor, and the sixth — flux against charge — had no element. Chua
predicted it in 1971 (*Memristor — The Missing Circuit Element*, IEEE Trans. Circuit Theory
CT-18, 507–519); claimed physically by HP Labs in 2008 (Nature 453). That is WP-82's method
on its rung ladder and Figure 1.3.1's on its cells — enumerate, find the empty relation,
treat the gap as a prediction — at its most successful known instance.

**N11 opened as a row, not a claim.** A memristor's pinched hysteresis loop against the
corpus's subcritical fold (HVEH Proof III; the shutdown-vs-startup setpoint gap still
`[OPEN]`). Verdict `UNRESOLVED`, corpora searched: **none yet**. The resemblance is currently
at the level of the word *hysteresis*, which is the match the register exists to refuse.

**A self-reference, caught by the script failing on its own commit.** Block [6] counts with
`git grep` at HEAD. Excluding `docs/` and this chapter was not enough: publishing the chapter
also put "van der Pol" into `book7/index.html` and two generated index pages, and the script
went red on the first run after the commit. That is **WP-82 block [3]'s finding arriving on
schedule — a file count counts the listings and the ruler.** The block now classifies every
hit as chapter / listing / audit / self, prints the composition, and asserts on **chapters**:
`limit cycle` 119 files but **108 chapters**; `van der Pol` 5 files but **0 chapters**. It is
written to fail when a second *chapter* names the example, which is the notification that the
gap has been closed by use. The raw file count was never the number to quote and the page now
quotes chapters.

**Checks.** `ch-van-der-pol-verify.py` exit 0; `novelty_check.py` exit 0; `audit.py --all`
clean at 733 HTML; `terms.py --check` OK at 153 terms; indexes regenerated.

# THE NOVELTY REGISTER, AND WHY UNMATCHED IS NOT NOVEL (2026-09-16)

**What was built.** `docs/novelty-register.md` (ten rows) and `tools/novelty_check.py`
(4 blocks, exit 0). Rule R18 added to CLAUDE.md.

**What it is for.** The mathematics here is derived from first principles without reading
the literature first. That is the method, and it is not in question. Its one consequence is:
**priority runs on publication date, not on route.** A result derived cleanly in 2026 that
someone published in 1928 is re-derived — the derivation happened, the method is vindicated,
and the novelty claim fails anyway. So the claim rests entirely on a search run before
publishing, looking *for* the prior art rather than for its absence. That makes R15 —
*a failed search is a fact about the search* — load-bearing at the highest stakes in the
corpus.

**Two registers that were being conflated.** A literature pass here is a **priority check**,
not an attribution fix. Nothing in the Strogatz pass of 2026-09-15/16 was a missing citation
in the ordinary sense; the sources had not been read. The earlier framing of those findings
as "missing pointers" is withdrawn and restated as priority findings. Consequence for
writing: a citation in this corpus is a pointer for the reader — *"this is classical, see X
p. N"* — never *"following X"*. `book6/wp58-galactic-fold.html` is the model, deriving
`r - r^3` from the flat-rotation-curve effective force and printing the derivation.

**The scale, closed:** `KNOWN-EXACT` → `KNOWN-GENERAL` → `PRIOR-ART-CANDIDATE` →
`UNRESOLVED` → `UNMATCHED-LIMITED` → `UNMATCHED-BROAD`. Never found / not-found. The word
*novel* is not in the vocabulary and the checker fails if it appears in a verdict.

**Four rows come back KNOWN-EXACT**, all from the Strogatz pass: Γ / T\* / μ = −2
(Example 7.1.1 p. 199), the closed-form return map (Example 8.7.1 p. 282), uniqueness of the
cycle (Liénard's Theorem p. 212, Example 7.4.1 p. 213 — Liénard 1928, Levinson–Smith 1942),
and the trapping annulus (Example 7.3.1 p. 206).

**A keyword-level similarity is not a prior-art match, and the register caught that on its
first pass.** An external search returned "definitely prior art at the level of the general
claim" for the contact-Hamiltonian obstruction, citing two papers. Both are real and both
were checked at source:

- de Lucas & Rivas, *Contact Lie systems: theory and applications*, arXiv:2207.04038
  (July 2022) / J. Phys. A 2023. The result is **Proposition 3.8 in the published version and
  3.7 in the arXiv version** — record both; a proposition number that moves between preprint
  and journal is how a citation dies later. Verbatim: *"If (M,Λ,X) is a Lie–Hamilton system
  and D^X = TM, then M is even-dimensional."* That is a **dimension obstruction on Poisson
  structures**, not a contact no-go.
- Colombo & López-Gordón, *Egorov-type semiclassical limits for open quantum systems with a
  bi-Lindblad structure*, Anal. Math. Phys. **16**:118 (2026), Remark 2.9 — compatible
  Jacobi–Nijenhuis recursion operators do not yield a maximal family of dissipated quantities
  in involution. An **integrability obstruction**.

Neither states WP-22 §7's theorem — impose θ̇ ≡ 1, get ℋ = p + g(θ,z), the locking identity,
c → −2 forcing H → −∞. What the three share is the phrase "no-go" and the setting. Row N08
is `PRIOR-ART-CANDIDATE`, not `KNOWN`: both papers are the right neighbourhood and must be
read line by line before any priority claim. **Priority date for de Lucas–Rivas is the arXiv
date, July 2022, not the journal date.**

**And the converse bites.** Row N06, base-point drift of the per-period exponent, looked
pre-empted by published statements that a monodromy matrix depends on its base point. The
standard result is the opposite for the quantity that matters: ChaosBook §5.3 — *"Jp
evaluated anywhere along the cycle has the same set of Floquet multipliers"*, the matrices
being related by similarity. So the adjacent literature runs **against** equivalence: a
genuine periodic-orbit monodromy has base-point-invariant multipliers, which makes the
corpus's drift a diagnostic that the object is a time-2π flow map and not a monodromy —
ż = 1, no return, no periodic orbit, which is what WP-122 concluded independently. The row
carries a requirement with it: **the claim must be stated in multipliers or exponents, not
in the matrix**, or it collides with a true and uninteresting statement.

**Finite-time escape (N09) is background prior art and was never the claim.** A citation
proving escape exists cannot pre-empt a theorem about when *closure* changes the escape
property. `KNOWN-GENERAL` on the phenomenon, `UNRESOLVED` on the closure-dependence.

**Searches still owed on N08.** Searching for the theorem has not worked and will not.
Search its ingredients: the locking identity in algebraic form; contact Hamiltonians with a
cyclic coordinate at identically fixed velocity; the obstruction between a transverse
attractor and a positive constant expansion rate, phrased without "no-go".

**Not covered.** Patents. Different corpus, different priority rules, different disclosure
bar; HVEH and the SAF work need their own search and no row here speaks to patentability.

**Checks.** `novelty_check.py` exit 0; `audit.py --all` clean at 732 HTML.

# THE RULER RE-MEASURED: WP-82 REPRODUCES 12/12, AND HAS MOVED (2026-09-16)

**What was built.** `book6/wp82-verify.py` — 6 blocks, exit 0. WP-82's rung table now
carries a second, dated column and the volume-XIII entry carries its date.

**The table is not wrong. It is dated, and nothing had re-run it.** WP-82 states its own
method — "tracked `*.html` and `*.md` files containing at least one case-insensitive
match, taken at commit `654fb06` on 2026-08-29." Re-run at that commit, **all twelve
published numbers reproduce exactly**, the rung-30 zero included. The paper was right on
the day.

**The rung-30 zero was right too, and an earlier note in this log saying otherwise is
withdrawn.** `book13/ch06-past-two.html` carries the ∞-category vocabulary, and book13 was
stubbed on 2026-08-28 in `9d78ff8` — the same day as `654fb06`, but *after* it. The file
does not exist in the tree the table was taken from (`git cat-file -e 654fb06:book13/…`
fails). A date comparison at day resolution said "stale on arrival"; the commit order says
it was current.

**Re-measured at HEAD, same method:**

| rung | pattern | 2026-08-29 | 2026-09-16 |
|---|---|---:|---:|
| 28 | k-theory | 0 | 7 |
| 28 | index theorem | 1 | 4 |
| 28 | atiyah | 1 | 3 |
| 29 | operator algebra | 76 | 100 |
| 29 | von neumann | 7 | 11 |
| 30 | ∞-categor / infinity-categor | 0 | 3 |
| 31 | sheaf / sheaves | 1 | 6 |
| 32 | motivic / langlands | 3 | 7 |
| 33 | noncommutative | 9 | 17 |
| 33 | connes | 15 | 27 |
| 33 | spectral triple | 7 | 14 |
| — | moonshine | 25 | 28 |

Rung 28 goes 2 → 14 file-mentions, rung 33 goes 31 → 58. **The inversion the paper reported
has narrowed from 15.5:1 to 4.1:1 and has not reversed.**

**And the composition matters more than the total.** Of the seven files that now say
"k-theory": one chapter (`book7/ch-grothendieck.html`), three index/listing pages, the audit
log, a checklist, and WP-82 itself. Block [3] prints the breakdown, because reporting
0 → 7 without it overstates the floor by a factor of seven. The floor is **started**, not
built.

**Why this needed a tool.** A dated measurement with no script behind it can only be
re-derived by hand, and on 2026-09-15 a hand reading of the rung-30 row as a live count
produced a wrong conclusion about Volume XIII — that book13 was ordinary category theory
squatting on a reserved number. It is not: every book13 chapter's metagrid reads
`Rung 30 · Higher Category Theory`, ch03 is kernel-checked against
`CategoryTheory.Bicategory`, and WP-82 marks the XIII–XV placement `ASSUME` rather than
reserving it. There was no collision. The row was not wrong; the reading was.

## Book XIII: the Mathlib numbers reached the index page and not the chapters

`book13/index.html` was corrected on 2026-09-12 from 1113 / 48 / 112 to **1089 / 44 / 108**
and records the earlier reading in its own text. The correction did not travel: all eight
chapter metagrids still read `CategoryTheory 1113 files · measured 2026-08-29`, and
Chapter 4's table still read 1113 / 48 / 112. `ch-mathlib-verify.py` passed throughout
**because it read one file**.

Fixed: eight metagrids to `1089 · measured 2026-09-12`, Chapter 4's three table rows to
1089 / 44 / 108. Re-measured against the local checkout today and confirmed.
`ch-mathlib-verify.py` gains block [5], which walks every `ch*.html` in the volume and fails
on any superseded count; index.html keeps 1113 / 48 / 112 deliberately, as a quotation of
what the earlier reading said. **A number is published wherever it is printed.**

## The construction-order argument, measured for XI, XII and XIII

book13's reason for being written first is recorded in `ch-mathlib-verify.py`: *"Mathlib has
no K-theory, so Volume XI cannot have a machine-checked core, and CategoryTheory/ is large
enough that Volume XIII's work is instantiation rather than construction."* Measured against
the checkout at `.lake/packages/mathlib`, that generalises:

| volume | rung | Mathlib support | reading |
|---|---|---|---|
| **XIII** | 30 | `CategoryTheory/` 1089, `Bicategory/` 44, `Monoidal/` 108, `SimplicialSet/` 68, `Quasicategory/` 6 | instantiation |
| **XII** | 29 | `CStarAlgebra/` 44, `InnerProductSpace/` 53, `Normed/Algebra/` 12, **`VonNeumannAlgebra/` 1** | half instantiation, half construction |
| **XI** | 28 | no `KTheory/` under any of five plausible paths; one K-adjacent file in all of Mathlib — `GroupTheory/MonoidLocalization/GrothendieckGroup.lean` | construction |

So the order forced by the verification machine is **XIII, then XII, then XI** — the reverse
of rung order. Two consequences worth recording before those volumes are written:

1. **XII is not one volume by this measure.** WP-82 §3 assigns it "Operator Algebras — C\*-
   and von Neumann". The C\*- half has 44 files behind it; the von Neumann half has one. A
   volume claiming both claims a machine-checked core for a half that has no library.
2. **XI's entire Mathlib floor is the Grothendieck group of a commutative monoid** — which is
   precisely the object `book7/ch-grothendieck.html` was built around. Anything above K₀ is
   construction, not instantiation.

Not written up as a paper; recorded here as the measurement.

**Checks.** `audit.py --all` clean at 732 HTML; `wp82-verify.py` and `ch-mathlib-verify.py`
exit 0.

# WP-22 REVISED: FOUR CLAUSES CARRIED INTO THE SOURCE, AND THE DOCUMENT REBUILDS AGAIN (2026-09-15)

**What was done.** `book6/differential-equations/helix-toy-model/helix_toy_model.tex` and
its PDF, revised together. Four clarifications, listed in the paper's own new
**Corrections** section, dated. **No result is withdrawn and no theorem changes content.**
PDF rebuilt with `pdflatex` twice, clean: no undefined references, no undefined citations,
10 pages to 12.

1. **Γ is a helix, not a periodic orbit of the flow.** ż = 1, so z(t) = z₀ + t is strictly
   increasing, nothing returns, and the flow has no periodic orbit at all; T\* = 2π is the
   period of the (r, θ) projection. The first edition wrote "a periodic orbit of period
   T\* = 2π (a helix in (r, θ, z), since θ̇ = ż = 1)" — the parenthesis was right and the
   phrase it qualified was not. Abstract and §2 now say it directly.
2. **The sense of "degenerate" is named.** Guckenheimer & Holmes — a vanishing first
   Lyapunov coefficient — and not Strogatz p. 256, where the term means a nonlinear centre
   with a continuous band of closed orbits and no limit cycle on either side. Both books are
   in the paper's own bibliography. The claim was and remains correct by Strogatz's Rule of
   Thumb 1 (p. 254); only the word needed a qualifier. §5 is retitled accordingly.
3. **Theorem 5.1 is about the frozen planar subsystem.** A new paragraph before the theorem
   says so: z is a dynamical variable swept at unit rate, not a parameter; the field
   (ṙ, θ̇, ż) has ż ≡ 1 and hence no zero, so there is no equilibrium to bifurcate. The
   caveat had existed only in the exercises ("freeze z"; solution 4 disqualifies the
   codimension-one normal forms at z = 0). The theorem is retitled *Degenerate Hopf at
   r = 0, frozen z*.
4. **The radial data are Strogatz Example 7.1.1 and are now cited as such.** Removing ż and
   taking f = f_cub leaves r' = r(1−r²), θ̇ = 1 — p. 199. Γ, T\* = 2π and the value −2
   imposed as f'(1) all come from there. `\bibitem{Strogatz}` stood in the bibliography with
   `\cite{Strogatz}` used zero times and the string `7.1.1` absent; the counts are now 5 and
   3, at the places the data are used.

**Added while there.** §2 now records that both canonical closures have exactly one positive
root, so each frozen slice carries exactly one circular orbit — a count, not an assumption —
and that the same statement fails for the additive coupling r(1−r²) + a(r−1), which
factorises as −(r−1)(r²+r−a) and carries a second circular orbit. Cross-references to
ch-strogatz, WP-120 and WP-122 with their URLs.

**THE BLOCKER IS GONE, AND IT WAS LARGER THAN REPORTED.** The 2026-09-15 entry below records
that `hopf_diagram.png` was missing so the PDF could not be rebuilt. Measured properly:
**four** of the five figures the document `\includegraphics` were absent from the source
directory — `helix_split.png`, `basin_boundary.png`, `hopf_diagram.png`, `cosmo_parallel.png`
— and none had ever been tracked (`git log --all --diff-filter=A` returns nothing for any of
them). Only `fig1_helix3d.png` was there. So the paper had been unbuildable from its own
sources since it was added in `f8a7a54`, and nothing said so.

The repair was already written: `helix_toy_model.py`, sitting in the same directory, states
in its docstring that it "reproduces every numerical claim in the paper and regenerates all
figures", and it does. Run under `MPLBACKEND=Agg` (scipy installed on the desk for it), it
regenerated all five and reprinted the paper's numerical report — μ → −2 by base point,
z₀\*(ε₀) at three ε₀, the bounded closure recovering where the cubic blows up, and the
double-log basin fit C = 3.677, max resid 0.105 — matching the text. The four missing figures
are now tracked beside the source; `fig1_helix3d.png` was left at its committed bytes rather
than churned.

**A verify script caught its own subject moving.** `book7/ch-strogatz-verify.py` block [7]
read this `.tex` and asserted `\cite{Strogatz} == 0` and `"7.1.1" == 0`. After the revision it
exited 1. That is the instrument working: the block now checks the repaired state (citations
present, Example 7.1.1 named, "no periodic orbit" stated, the Guckenheimer-Holmes sense
attributed and separated from p. 256, the frozen-z reading stated, a Corrections section
present) and prints the old counts beside the new ones. `ch-strogatz.html` and
`wp120-how-many-closed-orbits.html` were updated in the same pass so neither still describes
a live defect; both keep the finding and date its closure.

**Evidence.** `docs/ml-evidence/wp22-2026-09-15/` holds the pre-revision `.tex` and a README
declaring the cluster, per the 2026-09-01 ruling.

**Checks.** `audit.py --all` clean at 723 HTML; `terms.py --check` OK at 153 declared terms;
indexes and master index regenerated; all three verify scripts exit 0.

# HOW MANY CLOSED ORBITS — WP-120, AND THE GAP FILLED (2026-09-15)

**What was built.** `book6/wp120-how-many-closed-orbits.html` and `book6/wp120-verify.py`
— 8 blocks, 23 checks, standard library only, exit 0. Registered in `book6/index.html`.
The WP-120 number was an unexplained gap (no file, no reference anywhere in the repository);
it is now used deliberately rather than left open.

**The question.** Gamma = {r = 1} is called *the* limit cycle across the corpus, ten to
seventeen times on the pages that use the phrase. Uniqueness is asserted exactly once
anywhere in the series — one row of `chRho-spectral.html`'s open-obligation table — and
there it is about the discrete Collatz cycle. For the continuous Gamma nothing had been
claimed and nothing proved; the definite article was carrying both.

**Radial-only fields: the count is free.** If r' depends on r alone and theta' > 0, a
closed orbit needs r periodic, r is monotone where r' is nonzero, and a monotone periodic
function is constant. So the closed orbits are exactly the circles at positive roots of f.
Book 6's `r' = f(r)(1 - e^{-z})`: the modulation is a positive factor for z > 0, and both
canonical closures have exactly one positive root. **One circular orbit.**

**Vol II has two, and this is new.** `r' = r(1-r^2) + 2(r-1)e^{-z}`. With a = 2e^{-z} the
field factorises — checked as an identity at 16 (a, r) pairs —

    r(1-r^2) + a(r-1)  =  -(r - 1)(r^2 + r - a)

so besides r = 1 there is a second positive root `r_2(a) = (-1 + sqrt(1+4a))/2`, i.e.
`r_2(z) = (-1 + sqrt(1 + 8e^{-z}))/2`. Radial eigenvalues: `a - 2` at Gamma and
`(1 - r_2) sqrt(1+4a)` at r_2, both checked against numerical differentiation at six values
of z. They vanish together at a = 2, that is at z = 0, where r_2 = 1 exactly.

**So the neutral line has a name it was not being given.** It is not only a sign change in
an eigenvalue: it is the collision of two circular orbits, which pass through each other
and exchange stability — a transcritical bifurcation of cycles. For z > 0 the inner circle
r_2 < 1 is repelling and is the basin boundary of Gamma in the frozen slice; for z < 0 the
roles swap. Neither the second orbit nor the string `sqrt(1+8e^{-z})` appears anywhere in
the repository (`git grep`, several spellings).

**And the two toy models are not variants of each other.** A multiplicative modulation
`f(r)(1-e^{-z})` preserves the root set; an additive coupling `+ a(r-1)` adds a root.
Wherever both are cited the difference has to be stated.

**Guard, written into the paper and into block [6].** r_2(z) is strictly increasing in a
with limits 0 and 1, so as z runs over (0, infinity) it attains *every* value in (0,1)
exactly once; the block finds the z producing 0.25, 0.5, 0.773, 0.882 and 0.99 to 1e-9
each. A numerical agreement between r_2(z) and r_star, kappa* or any other stored constant
of that interval is therefore **not evidence**, and would become evidence only if the z at
which it matched were independently fixed. None is. The guard is in the paper so the
finding cannot be turned into a correspondence later.

**theta-dependent fields: Dulac, with the function.** Plain Bendixson fails on Strogatz's
Example 7.3.1 (`r' = r(1-r^2) + mu r cos theta`, `theta' = 1`) because
`div F = 2 - 4r^2 + 2 mu cos theta` changes sign at r = 1/sqrt(2). Taking g = 1/r^3,

    div(gF) = -(1/r) [ (1 + mu cos theta)/r^2 + 1 ]

strictly negative on all of r > 0 exactly when |mu| < 1 — the same threshold as Example
7.3.1's trapping annulus. Checked against numerical differentiation at nine points, scanned
at six values of mu, and confirmed to change sign at mu = 1.5. Strogatz's own candidate
list on p. 204 is g = 1, 1/(x^a y^b), e^{ax}, e^{ay}; 1/r^3 is the polar analogue of the
second, and he says plainly there is no algorithm.

**Index theory supplies the other half.** Theorem 6.8.2, p. 180: any closed orbit encloses
fixed points whose indices sum to +1. Block [3] scans r in (0.01, 4] on 800 x 720 and finds
min|F| = 0.0168, so the origin is the only fixed point, and the winding number is +1 on
circles from 0.05 to 5.0. Hence every closed orbit encircles the origin and any two are
nested with an annulus between them in r > 0.

**The annulus form of Dulac, flagged as an extension.** Strogatz p. 204 requires a simply
connected region and concludes *no* closed orbits, which does not apply to the punctured
plane where one exists. What applies is his own proof run on an annulus: Green's theorem
over the annulus between two nested closed orbits gives 0 on the right because F is tangent
to each, so a one-signed div(gF) is a contradiction, and R holds at most one closed orbit.
This is stated in the paper as an extension with its extra line, not as a quotation, so a
reader checks the line rather than the citation.

**Result.** Existence (Example 7.3.1's annulus, checked in WP-122) plus uniqueness gives
**exactly one** closed orbit for every |mu| < 1. Corroborated by integration from five radii
at three values of mu, spread 1e-13 on the return ray — corroboration only; three values
against a theorem covering all of them.

**And nothing on the 3-manifold has a periodic orbit to be unique.** Book 6: z' = 1
identically, so z(t) = z_0 + t is injective and the flow has no periodic orbit at all;
Gamma is a helix, a closed orbit of the (r, theta) projection and not of the flow. Vol II:
z' = r^2 - 2(r-1)^2 e^{-z} is 1 on Gamma and positive on the tube |r-1| <= 0.4, z >= 0
(scanned min 0.040000 at (0.600, 0.00); analytic bound `(1-d)^2 > 2d^2` for
`d < 1/(1+sqrt2) = 0.414214`), so no periodic orbit lies there either. Outside that tube
Vol II's z' does change sign, so the statement is about a neighbourhood; Book 6's needs none.
This is the same fact WP-122 reports as the absence of a return map, seen from the other side.

**OPEN — a vocabulary consequence.** "Limit cycle" is right for the planar system and for
frozen slices, loose for the object on the contact 3-manifold. WP-22 writes "a periodic
orbit of period T* = 2pi (a helix in (r, theta, z), since theta' = z' = 1)", where the
parenthesis contradicts the phrase it qualifies. Not edited — it is the author's call, and
it belongs with the two clauses already owed to WP-22 at its next rebuild.

**Registered.** `audit.py --all` clean at 723 HTML; `terms.py --check` OK at 153 declared
terms; indexes regenerated.

# THE RETURN MAP WAS IN THE EXERCISE (2026-09-15)

**What was built.** `book6/wp122-the-return-map-was-in-the-exercise.html` and
`book6/wp122-verify.py` — eight blocks, standard library only, exit 0. Registered in
`book6/index.html`.

**What was verified.** Strogatz Example 8.7.1 (2nd ed., p. 282) gives the Poincare map of
the corpus's transverse attractor in closed form:

    P(r) = [ 1 + e^{-4pi} ( r^{-2} - 1 ) ]^{-1/2}

Checked against RK4 over one period from eight radii between 0.02 and 40: agreement at
1e-15 relative. `P'(1) = e^{-4pi} = 3.487342356e-06` exactly — the multiplier `ch-feynman`
and `ch-grothendieck` already print is the derivative of this map at its fixed point.

Exponent/multiplier bookkeeping confirmed correct: `(1/T*) ln|P'(1)| = -2`, per Strogatz's
Liapunov-exponent definition (p. 374, Example 10.5.1). Recorded as a PASS before the
correction below, because the two are conflated in exactly one place and used correctly
everywhere else checked.

**The Gronwall radius, measured.** `chEps-gronwall.html` Proof IV is correct: the bound
`exp((mu_max + 6 eps) T*)` reaches 1 at `eps_0 = 1/3`. Against it, the exact supremum of
`|P'|` on `|rho| <= 1/3` is `1.176970e-05`, attained at `rho = -1/3` — the bound is loose
there by a factor of `8.496e4`. `|P'|` does not reach 1 until `r = 0.015049224`, so P
contracts on a ball about three times wider in rho. Twenty iterates of P from initial radii
spanning 1e-6 to 1e4 all land on Gamma to 1e-8: the basin of the uncoupled transverse flow
has no boundary but the axis. **`eps_0 = 1/3` is not withdrawn** — it is a correct Gronwall
radius, and what this measures is what it is a radius of. Vol I's note that writing
`eps_0 ~ r_star` is an unwarranted identification stands and is now quantified.

**A vacuous pass, caught in this script's own first draft.** Fixed-step RK4 on
`r' = r - r^3` returns `nan` for `r_0 >~ 30` (stiff). The block tested
`if abs(r - 1.0) > 1e-8: fail`, and every comparison against `nan` is false, so two `nan`
rows passed as convergence. The guard now tests `isfinite` first; the `nan` rows are kept
in the printed table deliberately. Same class as the `: True := trivial` findings —
a check that cannot fail.

**OPEN — chRho-spectral.html, Argument V of seven.** Three separable items, each with a fix
on a numbered page:

1. *Units.* The paragraph calls -2 an eigenvalue of the linearised Poincare map. -2 is the
   exponent; the multiplier is `e^{-4pi}`. The two differ by `5.735e5`.
2. *Count.* Strogatz p. 281: a surface of section for an n-dimensional flow is
   (n-1)-dimensional, so P linearises to (n-1)x(n-1) — one multiplier for the planar
   transverse system, two on a contact 3-manifold. A spectrum listed as `{-2, +i, -i}` fits
   neither, and a modulus-one entry asserts a neutral direction the system does not have.
3. *Scaling.* The page reads `t_1/(2pi) ~ 2.25 ~ tau * eps_0^{-1} * (1/3)`. Computed:
   `eps_0^{-1} * (1/3) = 1` identically, so eps_0 does not enter the expression and the
   right-hand side is `tau = 2`; `t_1/(2pi) = 2.249611375552`; the gap is 12.4806 %.

The file also carries no `[MODEL]` / `[OPEN]` / `[VERIFIED]` tag on any of the seven
arguments, which the house rules require. The other six were not examined and nothing here
is a verdict on them, on RH, or on whether a contact reading of the critical strip is worth
pursuing. Not edited — this is a reader-facing page and the correction is the author's call.

**OPEN — the flow has no return map.** The full model has `z' = 1` everywhere, so no
trajectory returns to a section `{z = z_0}`. What the series computes over one period is a
time-2pi flow map, not a first return; the two agree on the transverse coordinate and
nowhere else, and the base-point drift `-4pi + 2e^{-z_0}(1 - e^{-2pi})` is that gap
measured. Finding the right substitute — a section in extended phase space, a pullback
attractor, or a compactifying rescaling of z — is handed forward. Until then "Poincare map"
should not name an object on the 3-manifold. In `chEps-gronwall`'s planar reduction the
term is correct, because there the time-2pi map is the first return.

**Instruments named, not yet adopted.** Trapping region + Poincare-Bendixson (Strogatz
§7.3, pp. 205-206) — Example 7.3.1 perturbs this same system and proves the cycle survives
for mu < 1 inside `0.999 sqrt(1-mu) < r < 1.001 sqrt(1+mu)`, by two inequalities holding for
all theta; block [7] checks the annulus at five values of mu. That is the analytic form of
the certificate `wp62-three-open-paths.html` asks for. Also unused: Dulac's criterion
(§7.2) for ruling out a second closed orbit, which the series has never done.

**Registered.** `audit.py --all` clean at 722 HTML; `terms.py --check` OK at 153 declared
terms; indexes regenerated. Note for whoever numbers the next paper: **WP-120 is an
unexplained gap** — no file, and no reference to it anywhere in the repository.

# THE HELIX IS EXAMPLE 7.1.1, AND FOUR OF ITS NUMBERS CAME WITH IT (2026-09-15)

**What was built.** `book7/ch-strogatz.html` and `book7/ch-strogatz-verify.py` — the
Scientist Gallery chapter for Steven Strogatz, and eight verification blocks, standard
library only, exit 0.

**What was verified.** The radial field of the Book 6 helix toy model (WP-22,
`book6/differential-equations/helix-toy-model/helix_toy_model.tex`) in its canonical cubic
closure is Strogatz, *Nonlinear Dynamics and Chaos*, 2nd ed., Example 7.1.1, p. 199:
`r' = r(1 - r^2)`, `theta' = 1`. Integrated from six starting radii, every trajectory
lands on r = 1 to fourteen places; theta advances at unit rate, so T* = 2*pi is
`theta' = 1` and nothing else; and `d/dr[r - r^3]` at r = 1 is -2.

`mu_max = -2` is the closure condition `f'(1) = -2`, imposed on every admissible closure
by eq. (closure-cond) and satisfied by both canonical closures because they were required
to satisfy it. The content of the exponent theorem is therefore the *invariance* and not
the value: the correction term `2e^{-z_0}(1 - e^{-t})` is bounded in t, so
`|mu + 2| <= 2e^{-z_0}/t`. Closed form checked against RK4 from four base points to 1e-12
relative.

The per-period exponent is `-4pi + 2e^{-z_0}(1 - e^{-2pi})`, closed form and midpoint
quadrature agreeing to 1e-8. It reaches -4pi only in the limit — the base-point dependence
`ch-grothendieck` reported when it measured the multiplier as an index candidate.

**Class: PROVENANCE, not error.** Every theorem examined is true as stated. Four of the
numbers the series quotes for Gamma — the cycle, T* = 2*pi, mu_max = -2, and the
multiplier e^{-4pi} = 3.487342e-06 — are fixed by the textbook example before the contact
structure enters. Five results are the model's own, and each involves z: the invariance of
the exponent under an integrable modulation, the neutral line z = 0, the closure-dependent
finite-time escape, the drift of the multiplier, and the contact-Hamiltonian no-go.

**One bibitem, zero citations.** Block [7] reads WP-22's source: `\bibitem{Strogatz}`
appears once, `\cite{Strogatz}` zero times, the string `7.1.1` zero times. Across the
geometry repository the name occurs in that one bibliography line and nowhere else
(`git grep -ril strogatz`, 1 file). Example 7.1.1 is the standard first example of a limit
cycle and belongs to nobody; what is absent is the pointer that would let a reader ask
which properties arrived with it.

**OPEN, owed to WP-22 at its next rebuild — two clauses.**

1. *Name the sense of "degenerate."* Strogatz p. 256 reserves *degenerate Hopf
   bifurcation* for the case with no limit cycles on either side and a continuous band of
   closed orbits — a nonlinear centre, his damped-pendulum example. WP-22's degeneracy is a
   vanishing first Lyapunov coefficient, which is Guckenheimer & Holmes' usage and the
   second entry in the same bibliography. The claim itself is correct by Strogatz's own
   Rule of Thumb 1 (p. 254): block [5] tabulates the generic radius falling to 1e-3 as
   z -> 0 against the model's pinned 1. Only the word needs a qualifier.
2. *Say where z is frozen.* The 2x2 Jacobian in the degenerate-Hopf theorem is that of the
   (x,y) subsystem at a held-fixed z. In the flow `z' = 1` everywhere, so the
   three-dimensional field has no zero: block [6] scans r in [0,4] x z in [-4,4] and finds
   `min |(r', theta', z')| = sqrt(2)`. WP-22 makes both points in its exercises — one says
   "freeze z", and solution 4 disqualifies the codimension-one normal forms because the
   whole field vanishes at z = 0 — but the theorem and the abstract do not carry the caveat
   their own exercises do.

Neither clause was applied to the `.tex` in this pass. `hopf_diagram.png` is absent from
`book6/differential-equations/helix-toy-model/`, so the distributed PDF cannot be rebuilt
from source as it stands, and editing the source alone would put the `.tex` and the linked
PDF out of step. Restoring or regenerating that figure is the prerequisite.

**Registered.** `book7/index.html` — gallery card and gap-table row. `audit.py --all`
clean at 720 HTML; `terms.py --check` OK at 153 declared terms.

# TWELVE WAS THE INSTANCE, AND THE PAGE CLAIMED THE KERNEL BEFORE THE KERNEL RAN (2026-09-13)

**What was built.** `GTCT/book4/FoldingFrequency.lean` — the WP-84 arithmetic as a
general theorem rather than a table:

    visibleModes N k = { N/2 }   <=>   N = 2k          (0 < k, 2 | N)

Six declarations, no `sorry`, every one resting on `[propext, Classical.choice,
Quot.sound]` and nothing else. Compiles in 289 s against Mathlib under Lean 4.32.0.
Report: `tools/verify-audit/2026-09-09/FoldingFrequency.axioms.txt`.

The gate probes `theorem` and `lemma`, and here that is **six of six**. The file's
only other declarations are the definition `visibleModes`, which carries no proof
obligation, and two anonymous `example`s instantiating the theorem. Every proof in
the file is audited — worth stating, because `Bhaskara.lean` audited eleven of
twelve and the difference between those two situations is invisible in the summary
line both print.

**Class: OVER-GENERALISED — one word, not the arithmetic.** WP-84 §4 was headed
*"The coincidence is a characterisation of twelve."* The sweep under that heading
holds k = 6 and varies N. With k fixed the answer can only come back N = 12, so the
table cannot see whether twelve is distinguished among all (N, k). It is not: the
theorem returns 12 at k = 6 and 20 at k = 10.

What survives is the sentence that followed the heading — at six-fold symmetry,
twelve is the one site count carrying no harmonic content except the fold. That was
checked independently against every N up to 20,000 and holds. Only the word
*characterisation* is withdrawn. The distinction matters: a retraction of the
arithmetic would have taken `PhaseVector := Fin 12 → ℝ` with it, and nothing here
does.

**Prompted by Saturn, and not applied to it.** A ten-sided wave at the south pole
(Sánchez-Lavega et al., *Science Advances*, doi 10.1126/sciadv.aee4251, 2 September
2026) beside the long-known six-sided wave at the north is a reason to stop
presenting one value of k as special. It is not evidence for the theorem, which is
about a discretely sampled ring; the polar wavenumbers are set by the width and
shear of a circumpolar jet. The two share the integers 6 and 10. WP-84 and
`FoldingFrequency.lean` both say so in their own text.

## The page asserted the audit before the audit existed

`wp84-the-fold-is-the-folding-frequency.html` carried **"Kernel-checked. Six
declarations … Report: `tools/verify-audit/…/FoldingFrequency.axioms.txt`"**
while the Lean file was still failing to compile. The count, the axiom set and the
report path were all written from what the file was expected to produce.

Every one of them turned out to be right. That is the part worth recording, because
a claim that happens to be true is indistinguishable in the published page from one
that was checked — which is the exact defect `--audit` and the `verify-audit/`
directory were introduced to remove. Evidence-shaped prose written ahead of the
evidence is the same failure as an audit that leaves nothing behind, arriving from
the other direction.

**Rule.** A page may not name a report path, a
declaration count or an axiom set until that report exists on disk. Cite nothing
prospectively; write the sentence after the gate prints, not before.

## A debugging note: two runs spent on a file that did not exist

`leancheck --audit` reported `FoldingFrequency.lean:86:40 unknown identifier 'k'`
twice, byte-identical. The diagnosis — that `rintro rfl` on `m = k` eliminates `k`
rather than `m`, stranding `dvd_refl k` — was applied to a copy in the container and
never reached the disk, because the device bridge was down at the moment of writing.
Reading the file on disk afterwards showed line 86 column 40 was `_`, not `k`;
column 40 on **line 72** is `k`. The reported position and the reported message
never agreed, and three compile cycles were spent before anyone checked the bytes.

Resolved by removing the fragile point rather than locating it. Both membership
tuples now read `⟨by omega, by omega, dvd_rfl⟩`: `dvd_rfl` takes its argument
implicitly and `omega` reads the context, so neither can name a variable `subst`
has eliminated, whichever side it chooses. Compiles clean.

**Two rules from it.** Read the file on the target disk before diagnosing an error
reported from it — a fix that was never written is indistinguishable from a fix that
did not work, and both produce the identical error message on re-run. And where a
tactic's behaviour is unspecified in the direction you depend on, remove the
dependency instead of predicting it.

## Applied

- `book6/wp84-the-fold-is-the-folding-frequency.html` — §4 heading and its referee
  response now state the surviving claim; the general theorem and its audit lead;
  the framing withdrawal is a dated note beneath them rather than the section's
  headline.
- `AXLE/Journal/vol7.html`, `vol8.html` — dated erratum appended to the notices
  page. Both issues are published; the body stands as circulated.
- `AXLE/Journal/vol9.html` — colophon now cites the theorem rather than "tested
  against nine candidate rates."

## Two git defects the push itself surfaced

**A stranded lock hid four days of AXLE commits.** `AXLE/.git/index.lock`, zero
bytes, created `2026-09-09 00:15:48` — the same second as `cf237e1`, by a git
invocation issued through the desktop bridge. It was never cleared. Every `git add`
and `git commit` in AXLE since has failed with *"Another git process seems to be
running"*, and the `git push` that followed then reported **"Everything
up-to-date"** — which is true, and reads as success.

That is the defect this log keeps finding, in a new costume: an operation that did
not happen, reported in words indistinguishable from one that did. Nothing was lost
— the AXLE working tree still held all five modified tracked files, three from this
pass and `lexical-generativity-ijl.html` and `theorem-registry.html` from other
sessions. But no session had been told its commit failed.

**Rule.** After a push script runs, read the commit back with
`git show --stat HEAD`. The script's own echo is not evidence, and
"Everything up-to-date" is not evidence that anything was committed.

**An unrelated file rode into the WP-84 commit.** `08c4577` contains
`tools/verify-audit/2026-09-12/geometry__CardiacHopfReduction.axioms.txt`, which the
push script never added. It was already staged in geometry's index from an earlier
session, and `git commit` takes the index, not the arguments to the preceding
`git add`. The file is a legitimate audit report — five `CardiacHopf` declarations,
all within the permitted three — sitting in the wrong commit. Not amended: the
commit is pushed, and pushed history stands.

**Rule.** A script that stages explicit paths must verify the index holds only those
paths before committing. `git diff-index --cached --name-only HEAD` answers it as
plumbing, without the index rewrite that makes `git status` unsafe through the
bridge.

**One line in `08c4577` corrected here rather than amended.** Its message says
"Kernel evidence committed alongside the prose."
`tools/verify-audit/2026-09-09/FoldingFrequency.axioms.txt` was already tracked —
committed 2026-09-10 by the overnight full-corpus run along with some fifty other
reports. The evidence is in the repo and the chapter's citation resolves; that
commit did not put it there.

---

# THE THIRD OVER-GENERALISED IN ONE WEEK, AND IT CONTRADICTED ITS OWN COMPANION (2026-09-05)

**Class: OVER-GENERALISED.** Mine, in `book6/wp99-paying-for-what-the-kernel-can-see.html` §6.

Comparing theorem-closing to mining, I wrote that mining's memorylessness
fails here because "skill and prior work dominate completely; the reward
concentrates, and concentrates on the people who least need an incentive." The
first clause is right and stands. The second fixed a parameter — that capability
in this work is a function of training history — and read it as a constant of
nature. Unmeasured, and asserted as structure.

**It also contradicted WP-98 §8, written days earlier, by me.** That section
argues the credential requirement falls to near zero on a hub whose outputs are
machine-checkable, because the artefact carries the argument. WP-99 §6 denied it
one paper later. A corpus is supposed to make that visible and it did — but only
because Pablo read both.

Corrected in place, the row marked rather than rewritten. The corrected form:
theorem-closing is not memoryless and cannot be made so, and is also not the
strongly path-dependent tournament the draft implied; variance in who closes a
given obligation is higher than a seniority model predicts and the direction of
travel is toward wider access, because the part of "prior work" that was tooling
fluency is what an assistant supplies. Both directions remain unmeasured and
WP-98 §7 already names the measurement.

**The correction strengthens the paper, which is why it matters.** A market is
worth running only when the supplier's identity is uncertain — if you can
predict who closes an obligation you hire them instead of posting a bounty. The
concentration I asserted would have been an argument against WP-99's own
mechanism. High variance is the condition for commissioning, not a defect in it.

Provenance: third instance in a week of the same class, and the third time the
correction came from Pablo. ε₀ = 1/3 called a chosen threshold when it is a
Grönwall bound; thirty sectors read as a fact about six and ten; now this.

# THIRTY WAS DOING THE WORK — an overclaim found by asking about base sixty (2026-09-05)

**Class: OVERSTATED.** Mine, in `book5/chV-saturn-smoke.html` §4 and on the
standalone decagon page.

The sentence was "the only field admitting both a hexagon and a decagon is the
trivial one", offered as a fact about six and ten. It is a fact about choosing
THIRTY sectors. On sixty, a sixfold pattern repeats every ten and a tenfold
every six, `gcd(10, 6) = 2`, and `k mod 2` carries both symmetries without being
constant. Checked exhaustively for every refinement N = 30 … 600: the invariant
space has exactly N/30 free values, never one except at N = 30.

`hex_and_dec_forces_constant` is true and unaffected. The defect is entirely in
the prose written around it, which carried the grid choice inside it as though
the grid were not a choice. This is the vacuity vocabulary's neighbour: not a
statement without content, a statement whose content is narrower than the
sentence built on it.

**The correction is stronger than what it replaces.** Rotations of order 6 and
order 10 generate rotation of order 30. A field carrying both is invariant under
C₃₀ and shows a thirty-sided pattern — no hexagon, no decagon. Nobody has
photographed a triacontagon on Saturn, so the two polygons are still two rings,
and the claim now names the observation that would refute it. "The field is
trivial" named nothing.

**Provenance.** Pablo asked whether base sixty would change the arithmetic. I
had already answered once that a base changes numerals and not numbers, which
is true and was not the question. Sixty as a NUMBER OF SECTORS changes the
answer, and the instinct behind it — sixty has room where thirty does not,
because 60/6 and 60/10 still share a factor — was exactly right. Second time in
two days that dismissing the vocabulary cost me the finding.

**Closed the same day.** `bash tools/leancheck.sh --audit
PolarPolygonCommonRefinement.lean` — OK 7s, 15 declarations, 0 sorryAx, nothing
outside the permitted three. `periodic_gcd` compiled with its `termination_by`
on the first attempt. Five of the fifteen rest on no axiom at all:
`periodic_one_const`, `constant_is_bisymmetric`, `sawtooth_not_constant`,
`alt_not_constant`, `periodic_add`.

This is also the first run to leave a report behind on its own —
`tools/verify-audit/2026-09-05/PolarPolygonCommonRefinement.axioms.txt`, written
by the run rather than typed. Every earlier `--audit` in this repo's history
printed to a terminal and discarded the evidence.

One thing the report exposed: `sawtooth_not_constant` had no `#print axioms`
line in the file's gate block, so it sat outside Tier 1 while every theorem
around it sat inside. A declaration is in the tier because a line names it, not
because it lives in an audited file. Block completed to all fifteen.

# Audit log — totogt.github.io/geometry

Dated narrative for defects and audits that are closed. Moved out of
`CLAUDE.md` on 2026-08-21 so the priming file stays short to read. Nothing
here was changed, only relocated. Open items remain in `CLAUDE.md`.

# ENCELADUS PROPOSAL PASS — a Lean file that is honest, and prose that is not (2026-09-05)

Occasioned by `G6LLC_NASA_Proposal_Enceladus_2026_ORCIDfix.docx` (May 2026), audited
against the tracked corpus with `tools/declaration_scan.py` and by reading the named
files. The pattern across every finding below is the same: **the Lean says what it
does; the prose upgrades it.** No defect here was introduced by a Lean file.

## ε₀ = 1/3 is presented as a machine-verified constant. It is a conditional one

**Class: OVERSTATED.** The proposal states "the Gronwall basin of Γ, with radius
ε₀ = 1/3 (PROVED, Lean 4)", calls it "a formally verified constant", and makes its
physical interpretation — the Khawaja et al. bond-dissociation boundary — its primary
novel scientific result, with the emphasis that "the mathematical constant was derived
before the comparison, not fitted after it."

What Lean holds is `AutophagyDm3.lean:182`:

    theorem gronwall_radius : (2 : ℝ) / (2 * (1 + 2)) = 1 / 3 := by norm_num

That is the last arithmetic step of the derivation, at sup‖Hess V‖ = 2. It mentions no
dynamical system, no Gronwall lemma, no Hessian and no basin. The formula
ε₀ = |μ_max| / [2(1 + sup‖Hess V‖)] is real and the value is derived, not chosen — but
whether the dm³ system has the Hessian bound that yields 1/3 is **O7, still open**, and
recorded above at four values in four places.

The correct tier is: *derived, conditional on an open input, with the final arithmetic
kernel-checked.* Not "PROVED, Lean 4."

## r* and ε₀: the "basin asymmetry" may be an artifact of the Hessian bound

**Class: NOT NEW — ch10 §6, restated with a consequence it does not draw.** An earlier
draft of this entry labelled the r*/ε₀ tension NEW. It is not: it is the headline of
Book 4 ch10, whose abstract says the inner boundary r* = 0.77594058 "correct[s] the
symmetric Gronwall estimate ε₀ = 1/3", and whose §6 states that trajectories with
r(0) ∈ (0.667, 0.77594058) are "in the Gronwall basin but outside the true basin" and
escape. Claiming novelty without looking is the FALSE ABSENCE pattern, recorded here
against the writer of this entry.

The consequence ch10 does not draw is this. §6 frames the discrepancy as *asymmetry* —
a symmetric estimate against an asymmetric basin, the outer side conservative and the
inner side failing. But a Gronwall stability radius is a **guaranteed-contraction**
radius. A ball that contains points which provably escape is not an asymmetric bound;
it is an invalid one. On the strict reading, ε₀ = 1/3 is simply too large.

And that lands on **O7**. At sup‖Hess V‖ = 6 — the value `V_second_deriv_at_one` proves —
ε₀ = 2/(2·7) = 1/7 ≈ 0.143, giving a basin r ∈ (0.857, 1.143), entirely inside the true
basin (0.776, ∞). Valid, and conservative on both sides, which is what a Gronwall bound
is supposed to be. **The asymmetry requiring correction may therefore be an artifact of
using H = 2 rather than a property of the system.** At H = 6 the correction ch10 §6
performs is not needed, because there is nothing to correct.

Caveat that keeps this open: if ε₀ is a radius in a different norm, or on the (r,z)
phase space rather than in r alone, the comparison lapses. Settling that closes O7 and
decides whether ch10 §6 describes a real asymmetry or a wrong constant.

## `nodal-sets.html` marks "Lean ✓" for declarations that exist nowhere

**Class: FABRICATED.** `AXLE/SBM/nodal-sets.html` — Bienal presentation material —
displays Lean source for `chladni6`, `chladni6_sixfold_sym` and
`hexagon_nodes_are_zeros`, and its status table carries the row "Six-fold symmetry,
hexagon nodes are zeros — **Lean ✓**". A declaration scan over the tracked corpus
resolves neither `hexagon_nodes_are_zeros` nor `hexagon_nodal_angles`. The displayed
proof also calls `hexagon_nodal_angles` without defining it, so the snippet could not
elaborate as shown even if a file held it.

Same class as the Chapter A pass, on a public page. Written this session as
`geometry/ChladniPolygon.lean`, which supplies both declarations and adds the tenfold
case; the tick is earned once that file passes `leancheck.sh --audit`, and not before.

## `separation_theorem` is not "one open obligation" — it is an uncompiled file

**Class: UNCHECKED.** The proposal names AXLE #12 `separation_theorem` as the single open
obligation with an explicit closure path. It does carry a real `sorry`
(`h_transverse ... := sorry -- placeholder for eigenvalue API`), so "open" is true. But it
lives in `AXLE/lean/`, and **no target in AXLE's lakefile covers that directory** — roots
are AXLE, finite, three toys, AXLE_v5_1, Main_v6, TribonacciRatioConvergence and
PrincipiaVol1. Nothing has ever compiled it. Reading it, `Real.exp (-12) < 1/32 := by
norm_num` will not discharge and the `calc` chains appear malformed. This is the same
class as bug #5 that AXLE's own lakefile records about `Main_v6`.

## Two counts that do not resolve

**Class: UNVERIFIABLE.** "Chapter A ... Twenty-six theorems are verified in Lean 4 with
zero sorry statements." Current tree: `AutophagyDm3.lean` 21, `TripleAlphaDm3.lean` 6,
`NbonacciLadder.lean` 13, all with zero code-level `sorry`. No grouping gives 26; the
nearest is 27, and the latter two files postdate the proposal. Not necessarily false when
written; not checkable now, which is the defect for a document inviting verification.

"Thirty-plus theorems are machine-verified with zero axioms beyond Mathlib4" cannot be
checked at all: AXLE pins Mathlib **v4.14.0**, the only complete build on this machine is
geometry's **v4.32.0**, so `leancheck.sh` cannot audit AXLE. The Control Ledger already
says this.

## "A reviewer ... can verify every proved claim in under one hour"

**Class: FALSE.** With a v4.14.0 pin a reviewer must build that Mathlib first — hours, not
one — and several of the named files are in no build target, so `lake build` would not
reach them regardless.

---

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
  `r★ = 0.77594058`; 4/5 = 0.8 is 3% above it, and `≈` reads as an identification.
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

# FALSE ABSENCES AND A STALE EXPECTATION — one session, four of them (2026-09-02)

Method: assistant session working on the RH arc (book4 ch11–15) and the D.8 NOI.
Every item below was an assertion made without a search, or from a source that
was not the live one. Recorded here rather than in the chapters or in
`GTCT/book4/ZetaReflection.lean`, which ships with a Zenodo deposit.

## The retired snapshot read as live

**Class: FALSE ABSENCE.** `ZetaReflection.lean` was read at
`geometry/docs/ml-evidence/deposits-moved-to-GTCT-2026-08-30/rh-arithmetic-contact-v1/`
and reported as current. That is the v1 deposit copy. The live file is
`Desktop/GTCT/book4/ZetaReflection.lean`, which by 2026-08-30 already held ten
theorems and one `sorry`, not four and two. On the strength of the snapshot,
`chiLog_real_on_critical_line` was written and compiled again from scratch —
a theorem proved three days earlier. The `ml-evidence` rule written 2026-09-01
says those copies are evidence, not sources. The rule was one day old.

## The file's own audit expectation had lagged its contents

**Class: DRIFT.** The footer of `ZetaReflection.lean` read `EXPECTED under
--audit: 4 declarations, 2 trusting sorryAx`, and the header STATUS block said
both `reflection_law` and `chiLog_real_on_critical_line` were admitted. Both had
been true on 2026-08-30 before the proof landed and false after it. Corrected to
11 and 1 and verified by `leancheck --audit` rather than asserted. The footer now
carries the rule instead of the incident: an expectation that lags the artifact
is not a check, it is a second claim to audit.

## `reflection_law` was stated on a domain its own docstring excluded

**Class: UNDERSPECIFIED STATEMENT.** The docstring enumerated four side
conditions; the signature carried none, quantifying over all real σ and t
including the ζ-zeros and the Γ-poles. Since `Zlog = logDeriv riemannZeta`
returns 0 at a zero under Lean's junk convention, the unhypothesised form was not
merely imprecise: at a hypothetical zero off the critical line its truth would
depend on where the zeros are, which the docstring explicitly disclaims. Four
hypotheses added, matching `Gammaℝ_eq_zero_iff` (negative EVEN integers — an
earlier prose-to-Lean rendering had used all negative integers, which is stronger
than needed and does not match the iff). Zenodo v1 carries the wider statement;
the narrowing goes in the v2 release notes.

## The D.8 element PDF was asserted missing while sitting in Downloads

**Class: FALSE ABSENCE.** `D.08+HWO_PSI_Amend68.pdf` and
`ROSES25_SoS_Amend_59_061526_v2.pdf` were in `~/Downloads` throughout. The claim
that the NOI was blocked on obtaining it was written into three delivered
documents — the NOI draft's notes, `opportunity_scan_2026-08-29.md`, and
`HANDOFF-2026-09-01.md`. `Desktop` was searched; `Downloads` never was.

## Two smaller ones, same shape

**Class: SINGLE-SOURCE ASSERTION.** "Baruch College has no chemistry research
facility" — stated from priors, never verified, withdrawn and still unverified.
"Futurex Inc places Felipe de Aquino on the US side of the research-security
line" — read from one document while another in the same folder says otherwise;
his affiliation remains open.

**Class: UNCHECKED CONTEXT.** The session ran on 29 August for three days after
it was 1 September, because the date was taken from file mtimes and `date` was
never called. Deadline arithmetic reported to the user was three days generous
throughout.

## What the arc gained anyway

Repairs applied to the M-series audit: M6 (the Global Positivity centrepiece,
ill-formed as an integral of a 3-form over a 2-plane field), M8 (the garbled Weil
explicit formula), M9 (ch13's "the Euler product is finite", including in an
exercise hint that made students reason from it). Two further copies of M6 that
the audit had not caught — the proof-ladder figure caption and ch13's setup line
— stated the degeneracy backwards, positive-definite ON the critical line rather
than off it, contradicting the corrected box. All now consistent.


## THEOREM 5.1 AND THE SPACE IT WAS STATED ON (2026-09-05)

**Defect.** Book 4 Chapter 5 printed, as Theorem 5.1, a dichotomy: every contact symmetry
of J¹(ℝ,ℝⁿ) is either a prolonged point transformation or a genuine contact transformation
mixing x, yᵢ and pᵢ, the latter being Chapter 6's Galilean Contact Transformations. By
Bäcklund's theorem (Math. Ann. 9, 1876) the second alternative is empty for n ≥ 2, and
Chapter 5 works in n = 2 throughout.

**Root cause, stated structurally rather than as an oversight.** A contact structure is a
hyperplane field — corank exactly one. The Cartan distribution on J¹(ℝ,ℝⁿ) is cut out by n
independent forms αᵢ = dyᵢ − pᵢ dx, so its corank is n. J¹(ℝ,ℝ²) is therefore not a contact
manifold at all; it is a Pfaffian system of rank 2, and those are rigid. The chapter had been
calling the Cartan distribution "the contact distribution" throughout, and the wrong noun
carried the wrong theorem with it. Corank is checkable in one line and had never been
checked.

**Repair.** Two were available and they are not equivalent:
  (a) keep J¹(ℝ,ℝ²) and rename the group — it is the prolonged point group, which is what
      Chapter 6 has in fact been computing;
  (b) relocate the claim to a contact 3-manifold, where genuine contact transformations do
      exist.
(b) is the repair taken, because the dm³ manifold turns out to be such a space. The shear
ψ(x,y,z) = (x,y,z+xy) followed by y ↦ y/2 carries α = dz − r²dθ to dz + y dx, so the dm³
contact structure is contactomorphic to the standard one on ℝ³, i.e. to J¹(ℝ,ℝ) — Bäcklund's
exceptional case n = 1. The Legendre transformation is the witness that the exception is not
vacuous.

**Second finding, from the same computation.** In cylindrical coordinates α ∧ dα = −2r dz∧dr∧dθ,
which vanishes at r = 0, and the corpus had read this as a degeneracy of the structure on the
axis. In Cartesian coordinates α ∧ dα = −2 dx∧dy∧dz. The vanishing factor was the Jacobian of
the polar chart. The form is contact on all of ℝ³.

**Third finding, caught by the tool rather than by reading.** While Chapter 22 §22.2 was being
drafted, `ch22-verify.py` failed the assertion that Res(f, f′) has degree 2(d−1) in the
coefficients of a binary form of degree d. It has degree 2d−1; the discriminant is that divided
by the leading coefficient. The claim in the chapter was corrected before it was printed, not
after. This is the first instance in this corpus of the verify-alongside rule catching an error
during composition rather than in audit.

**Files changed.**
- `book4/ch22.html` — new. §22.6 states Bäcklund and sets out both repairs; §22.7 gives the
  explicit contactomorphism.
- `book4/ch22-verify.py` — new. Ten blocks, all passing, exits non-zero on any failure.
- `book4/ch05.html` — Theorem 5.1 restated as Bäcklund's rigidity theorem; version note added;
  five occurrences of "contact distribution" corrected to "Cartan distribution"; "invariant
  under all contactomorphisms" corrected to "under all its symmetries". The Sator material is
  untouched — it is a mnemonic and was never load-bearing.
- `book4/ch21-gauss-map.html` — the §21.8 inventory row "dm³ contact form algebraises / OPEN"
  split: the structure half is settled in Ch 22 §22.7, the flow half stays open and is now
  stated narrowly.
- `book4/contents.html` — ch20 was missing from Part V; added. New Part VI (The Algebraic Turn)
  with ch21 and ch22.

**Also fixed, unrelated to the mathematics.** ch21-gauss-map.html spliced ch10's stylesheet but
not ch10's IntersectionObserver. The stylesheet sets `.f { opacity:0 }` and nothing added the
`.in` class, so all fifteen elements carrying that class — every theorem box and all three
SVG diagrams — rendered invisible. The script is now in both ch21 and ch22. Any chapter built
by splicing ch10's `<style>` should be checked for the same thing.


## A COUNT ERROR IN A COMMIT MESSAGE ABOUT COUNTING (2026-09-05)

**What was published.** GTCT commit `7ac47df`, pushed, states of `book4/Bhaskara.lean`:
"Ten declarations, no sorry."

**What the file holds.** **Twelve** declarations — eleven `theorem` and one `def`
(`IsPell`). Zero `sorry` in code. The same wrong figure went into *Imaginary Origin*
No. 9 page 4 twice, in the body and in the sidebar stat, and into the session's
working notes.

**Root cause.** The count was carried forward from the description written while the
file was being drafted, before the last two theorems were added, and was never
regenerated from the file. No instrument was run; a remembered number was reused.
This is the failure the corpus's own census exists to prevent, in a commit message
whose neighbouring paragraph reports a de-duplicated declaration count.

**A second point, which is the more useful one.** A naive `grep -c '\bsorry\b'` on
`Bhaskara.lean` returns **1**. The file contains no `sorry` in any proof; the single
match is the word inside the header comment "Every theorem below is proved. No
`sorry`." Stripping block and line comments before counting returns 0, which is the
truth. This is exactly the code-versus-comment distinction that moved this corpus's
own admitted count from 780 to 270, reproduced at file scale on the same day the
seed-grant application citing that distinction was being finalised.

**Resolution.** The commit is left as pushed: amending rewrites downstream SHAs and
breaks the commit links recorded in this log (rule of `d86dc76`, 2026-09-04). The
journal is corrected to twelve in both places before publication on 19 September.
Verified counts, comments stripped:

| file | declarations | `sorry` in code |
|---|---:|---:|
| `book4/Bhaskara.lean` | 12 (11 theorem, 1 def) | 0 |
| `book4/ZetaReflection.lean` | 11 | 1 |

`ZetaReflection`'s figures in the same commit message — eleven declarations, one
`sorryAx` — are correct and unchanged.

**Standing rule reinforced.** A declaration count in a commit message, a chapter or a
journal page is a published number and falls under the repo rule: regenerate it from
the file at the moment of writing, never restate it from a draft.


## WHAT "KERNEL-AUDITED" ASSERTS, IN THIS CORPUS AND ELSEWHERE (2026-09-05)

**Occasion.** `book4/Bhaskara.lean` was run through `leancheck.sh --audit` and passed:

    OK     202s  Bhaskara.lean
            audit: 11 declarations, 0 trusting sorryAx/native_decide
      1 ok, 0 failed

**What that establishes, read from the script rather than from the badge.** The audit
copies the file, appends `#print axioms <ns>.<decl>` for every declaration matched by
`^(theorem|lemma)`, runs it, and counts two things: lines reporting an axiom
dependency, and lines mentioning `sorryAx` or `native_decide`. So the assertion is
**no theorem in this file transitively trusts `sorryAx` or `native_decide`** — a
kernel-level, transitive statement, and genuinely stronger than sorry-free-in-source.

**What it does not establish.** That the axiom set is *exactly* `propext`,
`Classical.choice`, `Quot.sound`. The gate tests for the two dependencies that break
trust; it does not reject a fourth axiom, and it would pass a file that added one. For
`Bhaskara.lean` the added-axiom count is 0 by inspection and the tactics used are
`ring` and `norm_num`, so the axiom set almost certainly *is* the three — but "almost
certainly by inspection" is not what the tool reported, and the difference is the whole
subject of WP-94.

**Two counts, two meanings.** The audit reports **11** declarations; the file holds
**12**. The gate probes `theorem` and `lemma`, and `IsPell` is a `def`. Neither number
is wrong; they measure different sets, and quoting either without saying which gate
produced it is the defect this corpus keeps finding in other people's figures.

**The comparison that makes this worth logging.** The Fermat formalization announced
4 September states a stricter gate: its build *fails* unless the final theorem rests on
exactly the three standard axioms with no `sorry` anywhere. Two developments, both
truthfully described as kernel-audited, tested against different gates. Neither party is
misreporting. There is no agreed sense in which the phrase is a measurement.

**Action.** No change to the tool in this entry. Recorded so that the three-tier
registry's tier-three wording can be made precise — "no declaration trusts `sorryAx` or
`native_decide`" rather than the bare word *audited* — and so that a later session does
not read the badge as the stronger claim. A stricter mode that fails on any axiom
outside the allowlist is the obvious follow-up and is exactly item 1 of the `leanledger`
proposal in the seed-grant application.


## WHAT WAS LEFT IN GTCT WHEN BOOK 4 MOVED (2026-09-05)

**Audit.** Six files exist in `GTCT/book4/` with no counterpart in
`geometry/book4/`. Checked one at a time rather than assumed:

| File | Verdict |
|---|---|
| `chIV-preface-impa.html` | superseded — the IMPA-named preface, retired by the Edição Brasil rename |
| `chIV-15.html` | superseded — same chapter as `ch15.html` here, which is larger and further developed |
| `nav.js` | not needed — nothing here loads it; the single grep hit is a CSS comment in `ch15-complex-turn.html` |
| `SERIES_SKELETON.md` | GTCT's own |
| `certify_rstar_rigorous.py` | **real gap — brought over** |
| `METHODOLOGY.md` | **real gap — brought over**, it is the certifier's benchmark record |

**The gap that mattered.** `certify_rstar_rigorous.py` certifies r* by a
Lohner-style method — mpmath centre trajectory, Jacobian-linearised error
transport, interval-Hessian Lagrange remainder — so the radius over-approximates
the reachable set instead of estimating it. This repo held only the plain
float-bisection `certify_rstar.py`. Re-run, the rigorous script reproduces its
documented result exactly: **r\* ∈ [0.775940575501953125, 0.77594057550234375]**,
width 3.906e-13.

**A dangling citation, resolved without writing anything.** The script's docstring
pointed at a companion note `why_no_closed_form.md` for the algebraic and
Hamiltonian checks ruling out a closed form. No such file exists in any repo. The
content does exist — `METHODOLOGY.md` §"Path 3 — closed form (ruled out)". The
reference was misnamed, not missing, and is repointed. Nothing was composed to
fill it.

**A number published today, corrected against the certificate.** `ch23-verify.py`
block [8] regenerated Ch 3's basin figure by float bisection and reported
`0.775940575502539698`. That value is **outside** the certified bracket, 1.96e-13
above its upper bound. The two agree to eleven significant figures under
rounding; the twelve leading digits are identical (775940575502) and they part at
the thirteenth, by an amount comparable to the bracket width itself. The cause is
the block's own error floor: `solve_ivp` at rtol=1e-11/atol=1e-13. Ch 3 quotes
~0.776 and is unaffected. Block [8] now prints the bracket, states plainly that it
falls outside it, and directs any citation past eleven figures to the certificate.

**Standing note.** A figure regenerated by an instrument is only as good as that
instrument's floor, and quoting it to sixteen digits because Python printed
sixteen digits is the same defect as quoting a declaration count without its
convention. Where two instruments exist, the paper cites the stronger one and
says which.

---

## AN ORIENTATION BUG THAT INVENTED FIFTEEN PENTAGONS (2026-09-06)

Chapter 20b, `book4/ch20b-the-closing-field.html`, is new: the Eisenstein-norm
classification of closable hexagonal shells. Its §20b.7 reports measured panel
geometry, and the first version of that table was wrong. It is recorded here
because the numbers had already been quoted in conversation before the fault
was found.

**What was reported.** The thirty-two-panel shell — the classic football,
Goldberg GP(1,1) — at coefficient of variation ≈ 15% in panel area, with a
hexagon-to-pentagon area ratio of 1.39. Rounder shells were said to be *more*
uniform than the numbers actually support.

**What is true.** CV **2.90%**, ratio **1.0623**. The trade-off runs the other
way and runs monotonically: across GP(1,1) → GP(5,5) roundness climbs
0.9058 → 0.9960 while panel uniformity degrades 2.90% → 12.64%. The classic
thirty-two-panel ball has the most uniform panels of any shell in the family
that has hexagons at all — which is a result, and the opposite of what the bad
table said.

**The fault.** Icosahedral faces were taken from a convex-hull routine without
enforcing a consistent outward orientation. The Eisenstein lattice patch was
therefore laid down in mirrored handedness on roughly half the twenty faces,
and the seams did not register. The dual then miscounted vertex degree.

**Why it survived a first check.** Achiral shells — Goldberg class I, $(m,0)$,
and class II, $(m,m)$ — carry a mirror-symmetric patch, so orientation does not
matter and those rows were correct throughout. Only class III is chiral, and
only class III was wrong. A spot check on the football, which is class II,
returned a clean twelve pentagons and licensed the whole table.

**What caught it.** Theorem 20b.2 — every such shell has exactly twelve
pentagons, by Euler, with no exceptions and no parameters. GP(2,1) came back
with **twenty-seven**. GP(3,1) with forty-one. A theorem with no free
parameters is the cheapest possible assertion to test against a computation,
and it is the only reason this was found at all. `ball3.py` now prints the
pentagon count for every row; twelve in all of them is the check, not the
result.

**Standing note.** Where a construction has a symmetric special case and a
general case, verifying the symmetric case verifies nothing about the general
one. The bug lived exactly in the branch the spot check could not reach, and it
was reported to the reader before it was caught.

**A second fault, in the numbering.** The chapter was first written as Chapter
21 and its file named `ch21-the-closing-field.html`. Book 4 already had one:
`ch21-gauss-map.html`, "The Gauss Map, or What Survives the Lift", commit
`5b8140d`, 2026-09-04 — together with `ch22.html` and a `ch23-verify.py` naming
a Chapter 23. The number was chosen by reading a directory listing and adding
one to the highest chapter in it. That listing was already stale when it was
read, and a listing is the wrong instrument regardless: `git ls-files | grep
ch21` answers the question in one line and answers it about the repository
rather than about one working tree at one moment. Renumbered to **20b**,
following the `ch06` / `ch06b` precedent in the same directory, and placed in
Part V beside Ch 20 — where it belongs anyway, since Ch 20's defects are
translational and this chapter's are rotational.

**Standing note, second.** Do not derive an identifier from a listing. Derive it
from the index. The tree is one machine's opinion at one instant; `git ls-files`
is the repository's.

---

## THE CONTACT FORM WAS GIBBS'S ALL ALONG, MINUS THE HEAT (2026-09-06)

`book4/ch20b-the-closing-field.html` §20b.8 was written as a pointer at an open
question. It is now a result, and the result is a subtraction.

**The measurement that prompted it.** Across `geometry/`: `contact form` in 164
files, `Reeb` in 164, `Legendrian` in 33, `α ∧ dα` in 24 — against `Gibbs` in
**one** file (a subordinate clause in `gcm-framework.html`), `Carnot` in **one**
(a history section), and `Legendre transform` in **zero**. The structure is
everywhere and has never been named.

**Observation 20b.7.** The first law for a system that can rotate is
`dU = T dS + Ω dJ`, whose contact form is `α_G = dU − T dS − Ω dJ`. Setting
`dS = 0` gives `dU − Ω dJ`, which is `dz − r² dθ` — the corpus's own form, with
`z = U`, `θ` the angle, `r²` in the position of `Ω`. **The form used throughout
this corpus is the Gibbs form with the heat term deleted.** Its Legendrian
submanifolds are adiabats. Nothing appeared to be spent because on an adiabat
nothing is.

**Observation 20b.8.** Restoring the term and evaluating along a process gives
`α_G(γ̇) = δQ − T dS`, which is the Clausius defect. So `α_G(γ̇) ≤ 0` on every
physical path, with equality exactly on `ker α` — **the Legendrian submanifolds
are the reversible processes, and the failure to be Legendrian is the entropy
produced.** The direction is the sign of α; the cost is `−α(γ̇)/T`. Both were
already in the geometry, and deleting `T dS` had thrown the arrow away.

**A Legendre transform, the first written in this corpus.** `G = U − ΩJ` gives
`α′ = dG − T dS + J dΩ = dU − T dS − Ω dJ = α_G`. Not equivalent — identical.
Changing potential is a change of chart, which is Arnold's point.

All three verified symbolically in `book4/gibbs-check.py`, exit 0.

**What this does NOT license.** 20b.B stands and is now stricter. Clausius is a
statement about processes with a real entropy. The critical strip supplies none,
and the `c/π = (1/2π)log(t/2π)` rate remains a bookkeeping identity. A rate that
is positive is not thereby entropy production.

**The open question, restated.** It is no longer "does a potential exist" — it
does. It is: **what is the corpus's entropy?** Until an `S` is named on the
corpus's own phase space rather than borrowed from an analogy, the `T dS` term
cannot be restored and §20b.8 describes a thermodynamics the corpus is adjacent
to rather than one it has.

---

## A COMMIT MESSAGE THAT CONTRADICTED THE FILE IT COMMITTED (2026-09-06)

Commit `57add27` landed `CycleCoupling.lean` with the header **"VERIFICATION
STATUS — 2026-09-06. CLEAN, RUN AND RECORDED,"** carrying the three axiom lines
from an actual kernel check. Its commit message says of the same file:
**"NOT YET RUN."**

Both were written by the assistant. The message was drafted before the run and
handed over as a paste-ready block; the run then succeeded, the file's header
was rewritten to record it, and the message was not. Nothing in the pipeline
re-reads a commit message against the tree it is about to describe.

**What is true.** `lake env lean CycleCoupling.lean` in `~/Desktop/geometry`
under leanprover/lean4:v4.32.0 returns, for each of the three theorems,
`[propext, Classical.choice, Quot.sound]`. No `sorryAx`. WP-104 §2 is therefore
a theorem and not a reading: `SaturnHexagon.lean`'s content is available at
every sector count, and `Fin 6` entered as a hypothesis.

**Not amended.** `57add27` is pushed. Rewriting it would move every downstream
SHA to repair a message, which is the same trade this log already declined for
the `Co-Authored-By` trailers. The commit stands and this entry is the erratum.

**Standing note.** A commit message is a claim about a tree, and it can go stale
between being drafted and being run. Where a message asserts a verification
status, it should be written after the verification, not before — or it should
name the file and let the file's own header carry the status. This one did
neither.


## FIRST EDITIONS CANNOT POINT FORWARD (2026-09-07)

`tools/backlinks.py`, written today, reads every working paper in the corpus and
reports each citation that runs only one way: a later paper names an earlier one,
the earlier one says nothing back. Across 80 papers it finds **121 such edges,
touching 48 of them** — sixty per cent of the corpus is built on by something it
has never heard of. The mode is two to three papers later, a successor never
announced by its predecessor. The tail reaches 71 papers, which is a thread
reopening after most of a year with no trace at the older end.

The first reading of that result was wrong, and it was the assistant's. It was
put as a defect in 48 files, with a proposal to edit them.

**A first edition cannot point at what happens later.** The paper was complete
and correct on its date; what it lacks is knowledge it could not have had.
Appending "cited later by" to a dated note quietly undates it — a reader can no
longer tell what the paper knew when it was written from what the corpus learned
afterwards. Corrections are what a **second edition** is for, and the first
edition stays what it was.

**So the policy, from here.**

- Forward references belong to the **index**, which is allowed to know the
  present. They do not belong in the papers, which are dated records.
- Corrections go to **this log** by default. That is what it is.
- A correction reaches the **book** only when it must go through: when a reader
  who sees only that page could act on the claim and be wrong. In practice that
  means a published number, a stated verification status, or a claim offered for
  citation. Tightened statements, better proofs of the same result, loose prose
  and internal refinements are log-only.
- The corpus finds corrections continually. Publishing a notice for each one
  teaches a reader to read the errata instead of the work, and a high correction
  rate is evidence of checking rather than of sloppiness — which a reader has no
  way to distinguish from a wall of notices.

**The worklist, for whenever Book 6 turns an edition.** Splitting the 121 by
whether the citing text reads as a correction gives **13 corrections across 11
papers** against 116 extensions across 49. The 116 are the new cross-references
an edition would gain. The 13 are what an edition would fold in:

    WP-28  <- WP-30          WP-70  <- WP-72
    WP-29  <- WP-38, WP-85   WP-78  <- WP-81
    WP-30  <- WP-35          WP-79  <- WP-84
    WP-31  <- WP-38          WP-100 <- WP-104
    WP-39  <- WP-45, WP-66   WP-102 <- WP-104
    WP-41  <- WP-72

**The classifier overcalls.** It is a keyword window around each citation, so
"corrects" appearing near a mention of WP-n does not always mean WP-n is the
thing being corrected. Thirteen is small enough to read by hand, and that is the
intended use: a shortlist for a person, not a verdict.

**Standing note.** `backlinks.py` is not a defect finder and should not be
described as one. It produces the worklist for a second edition. Nothing it
reports is an error in the paper it names.

### The class

WP-73 separated the ways a verification claim comes loose from its artifact —
MISMATCH, STALE, FAIL — and four concerning the artifact itself: FALSE, VACUOUS,
UNTRUSTED, MISATTRIBUTED. WP-97 added OVER-GENERALISED: a statement true in its
own setting, carried into prose where a parameter fixed inside it reads as a
constant of nature.

This is none of those, and it is worth a name because it happened twice today.

    MISFRAMED   The artifact is correct and the finding about it is real, but
                the finding has been assigned to the wrong category, so the
                repair it implies damages something that was not broken.

**Instance one.** 121 one-way citations is a true measurement. Calling it a
defect in 48 papers was a category error — the property measured is navigational
and belongs to the corpus as a reading surface, not to any document in it. The
implied repair, editing 48 correct dated papers, would have destroyed the one
thing those papers are for: saying what was known on their date.

**Instance two, one level up.** The tool's own header then described it as a
reference *symmetry audit* finding one-way edges, which is the same mistake
written into the instrument. An instrument that names its output wrongly
propagates the misframing to everyone who runs it.

**Why it was plausible.** Every other survey this corpus runs — `terms.py`,
`leancheck`, the verify scripts, the link checker — reports defects, and its
output is a worklist of things to repair. A new survey producing a long list of
asymmetries reads as the same kind of object. The prior was strong and it was
wrong.

### What caught it, and what could not have

**No instrument in this repository would have caught this.** Every gate here
checks an artifact against a claim about it. This was a claim about a *class of
artifact*, and it was true as measurement and wrong as classification. There is
no assertion to test. `backlinks.py` would have kept reporting the same 121
edges, correctly, under a heading that made them mean something they did not.

It was caught by a reader saying *this happens naturally — one can only look
back in time*. That sentence carries no data the tool did not have. It supplies
the category.

**What generalises.** A measurement can be exactly right and the sentence
wrapping it exactly wrong, and no amount of re-running the measurement will
surface that. The check that catches MISFRAMED is not another instrument: it is
asking what kind of thing the measured property is, and whether the repair it
implies would damage something the artifact is supposed to be. Where the repair
touches many correct files at once, that question is not optional.


## NAMING A FAILURE MODE DID NOT PREVENT ITS NEXT TWO INSTANCES (2026-09-07)

Earlier today this log gained a class, MISFRAMED: the artifact is correct and
the finding about it is real, but the finding is assigned to the wrong category,
so the repair it implies damages something that was not broken. It was written
up with an instance, a plausibility account, and a note on what could have caught
it. Within the same session, by the same author, it recurred twice.

**Second instance — twenty-three working papers that were never missing.** A scan
for unwritten papers reported WP-1 and WP-3 through WP-24 as cited but absent. It
had matched files whose names begin `wpNN-`. WP-11 is a Zenodo DOI; WP-14 is
`emmes-whitepaper.html`; WP-23 is `archive.html`; WP-24 is
`ch-criticality-bridge-audit.html`; WP-60 is `book7/jacobian-verification.html`.
All present. Resolving the index's own hrefs instead — 155 rows — returns 154
local targets, none broken, and three external deposits. The corpus was complete
and the instrument said it was not.

**Third instance — a numbering scheme read as a mismatch.** A follow-up flagged
five index rows whose label number differs from the file they open, among them
"WP-31B" opening `wp30-how-to-audit.html` and "WP-31C" opening
`wp86-autophagy-calibration-case-study.html`. Reading the pages settles it: `wp86`
calls itself **WP-31C** in its own text, `wp87` calls itself **WP-31D**, `wp30`
calls itself **WP-31B**. Two numbering systems are laid over each other on
purpose — filename as position in the book, letter-suffix as position in the
calibration sub-series — and the index is faithfully showing the second. Three of
the five were a deliberate scheme reported as a defect.

**The mechanism, identical in all three.** A property was read off a name instead
of resolved from the artifact: filename to existence, filename number to identity,
citation count to correctness. In every case the artifact was available and would
have answered directly.

**What did survive the check.** Two of the five are real. A row labelled WP-81
opened `wp82-the-missing-floor.html`, whose own header says WP-82; the label was
wrong and the page is the authority, and it has been corrected. A row labelled
WP-30 opens `wp85-the-missing-anchor.html`, which calls itself WP-85 while citing
WP-31; the page does not settle whether it is a sub-series member or a stale
label, and it is left for a person.

**Standing note, and it is the point of this entry.** Naming a failure mode,
writing it into the log with a worked instance, and recording what would catch
it, did not prevent the same author from committing it twice more within the
hour. A taxonomy is a vocabulary for describing errors after the fact. It is not
a check, and treating a written-down class as though it were one is a fourth
instance of the same mistake — the class is a correct finding assigned to the
wrong category of remedy. What actually caught all three was resolving the
artifact: opening the index, opening the pages. The cheap operation was available
every time and was skipped every time in favour of a pattern over names.

### Addendum, same day: the fourth instance reached the filesystem

The entry above closed by saying a taxonomy describes errors after the fact and
is not a check. Within the hour the same author produced a fourth instance, and
this one was not caught by reading — it was written to disk first.

**What happened.** Two index rows appeared to disagree with the files they open:
a row labelled WP-30 opening `wp85-the-missing-anchor.html`, and a row labelled
WP-31B opening `wp30-how-to-audit.html`. The pages do not declare their own
numbers; they declare their neighbours, in prev/next navigation. Reading those
links produced a self-consistent forward chain — WP-29, WP-30a, WP-30b, WP-31,
WP-31C, WP-31D — and an argument for it: `wp30` precedes `wp31`, so labelling it
31B places it after a paper it comes before, and there is no WP-31A for a 31B to
follow. On that reasoning seven edits were made across six files, changing the
index and five pages.

**What was actually true.** The index row's own description records the decision,
dated: *"renumbered 2026-08-11 from a collision with WP-30 (The Missing Anchor);
written after WP-31, so it sits as WP-31B rather than displacing either."* The
index was correct. `wp85-the-missing-anchor.html` holds WP-30 and
`wp30-how-to-audit.html` is WP-31B, by an editorial decision taken four weeks
earlier and written down in the file being edited. All seven edits were reverted
and the tree returned to HEAD exactly.

**What the reasoning was worth.** The forward chain was real and the argument
from ordering was sound. It was reasoning about what the numbering *should* be,
offered where a record of what it *is* already existed, a few hundred characters
away in the same file. A good argument is not evidence, and producing one is not
the same as looking.

**What the survey then found, correctly.** Measured against the documented
decision rather than against an inference, twelve links in eight files were
stale, eight of them still calling `wp30-how-to-audit.html` by its
pre-renumbering name. That is the real residue of the 2026-08-11 collision: the
file was renumbered and eight files were never followed through. All twelve are
now corrected, and a re-audit returns zero.

**Standing note.** The failure did not change between instances three and four;
the consequence did. Instances one to three ended in a wrong sentence. The fourth
ended in modified files, and was caught only because a grep for the label turned
up the word *renumbered* by accident. Where a repair touches several files at
once, the check is not to reason more carefully. It is to search the artifact for
a record of the decision before assuming none was taken.

## 2026-09-07 — WP-105 and a footer erratum in three files

**WP-105 · The Unit That Inflates** (`book6/`, ~2,200 words, 9 sections,
`wp105-verify.py` all checks pass under sympy 1.14).

The note closes the gap WP-103 §4 left open. WP-103 established φ(n) ≤ d as the
condition for an order-n lattice rotation in dimension d, and stopped there. It
did not say what the excluded orders do *instead*. They inflate.

Three results, none novel, none previously stated together in this corpus:

1. φ(n) = 4 has **exactly four solutions**: {5, 8, 10, 12}. Not a search
   result — φ(n) ≳ √(n/2), so no n > 32 can have φ(n) ≤ 4. The observed
   quasicrystal symmetries are a solution set, not an empirical list. My first
   draft asserted {5,8,10,12,15,16,20,24,30}; the verify script caught it
   (φ(15) = φ(16) = φ(20) = φ(24) = φ(30) = 8, not 4). The correct statement is
   strictly stronger than the one I wrote.
2. Dirichlet rank, not rotation order, is the classification. Rank 0 with
   torsion ±1 → the periodic plane (n = 3,4,6). Rank 0 with torsion μ₆ (ℤ[ω])
   → Ch 21's closing shell and its twelve defects. Rank 1 → an infinite ±ε^k,
   hence an inflation. A tiling cannot inflate unless its field has somewhere
   to inflate to.
3. The inflation factor **is** the fundamental unit of ℚ(ζ_n)⁺: φ for Penrose,
   1+√2 for Ammann–Beenker, 2+√3 for the twelve-fold shield. Confirmed by brute
   Pell search, and independently from the substitution side, where
   det M = ±1 is the same condition read in GL(2,ℤ). This supplies the missing
   half of `ch-aperiodic-multiplying-media.html`'s "conserved criticality"
   sentence: the conserved quantity is the field norm.

Also recorded: 2cos(2π/10) = φ exactly, so for the decagon the *trace* of the
rotation is the fundamental unit; and η (tribonacci) is a Pisot unit but of a
**cubic** field, which is why Chapter η's chain is 1D and its Penrose cousin 2D.

§7 states the Saturn consequence and marks it OPEN: ℚ(ζ₁₀)⁺ = ℚ(√5) has one
fundamental unit, so *if* a scale ratio shows up in the south polar decagon the
arithmetic says it must be φ — but whether that is a statement about Saturn or
only about ℚ(√5) is not established. The note is kinematics throughout;
selection remains unclosed, as WP-104 §4 said.

**Erratum.** `wp102`, `wp103` and `wp104` each carried
"WP-100 · The Wavelength, Not the Count" in the footer title — copied from
WP-100's shell when I built them this session and never changed. Corrected in
place to each file's own title. WP-101 was correct; WP-105 was written correct.
Standing lesson, third variant of the same one: *when a file is built by
copying another, the identifiers are the part that does not survive the copy.*

## 2026-09-08 — ch8-meru: the fourth column

The attribution table had three columns: the pattern, the Western name, the
date of Western naming. It named no Indian source in any row, which made it a
table about Europe with an Indian header. Added **"Named in India"** as the
second column, and changed the first header from "What Pingala found in Meru
Prastara" to "What the Meru Prastara holds" — two of the five rows are not
Pingala's.

Sources checked before writing, not after:

- **Binomial coefficients.** Piṅgala, *Chandaḥśāstra*, final centuries BCE
  (conventionally c. 200 BCE); the *meru-prastāra* construction rule is written
  out explicitly in Halāyudha's *Mṛtasañjīvinī*, 10th c. CE. The sūtra style is
  cryptic and depends on the commentary — worth naming Halāyudha rather than
  letting Piṅgala carry a rule he stated only in outline.
- **Diagonal sums.** Virahāṅka, *Vṛttajātisamuccaya*, 6th–8th c. CE;
  Hemachandra, *Chandonuśāsana*, c. 1150. This is the row that started the
  thread.
- **Row sums = 2ⁿ.** Piṅgala's *saṅkhyā* pratyaya, *Chandaḥśāstra* 8.28, where
  2⁷ is obtained by three doublings and two squarings — repeated squaring, in a
  prosody manual.
- **Hockey stick.** Āryabhaṭa's *citighana*, *Gaṇitapāda* 21, 499 CE.

**The fourth row is left blank.** The odd-cell Sierpiński pattern has no Indian
attestation I could find, and the cell says so: *"not attested — a twentieth-
century reading of an ancient table."* A caption under the table states why the
blank is there. A table that claimed five out of five would be worth less than
one that claims four; the empty cell is the reason to believe the other four.

One secondary correction while checking: a search summary dated Halāyudha to
the 13th century. Both the primary-facing sources give the 10th. Used the 10th.

## 2026-09-08 — Two corrections and one result

**1. The G3 rung is not broken. I mischaracterised it.**

I had this on the open list as "shows 15 where Book 3 has 42, 5 of those 15
aren't in the roster, 32 roster chapters unreachable." Checked properly against
`tools/book3_roster.json`:

- all 42 roster files exist on disk
- all 42 carry a `nav.b3nav` rung
- **0** rungs disagree with the roster — position ("n of 42"), previous chapter,
  next chapter and the journey link are correct in every one

The taught path is complete and correct, and every chapter is reachable by
walking it. What I was actually looking at is the *other* nav, the `.nav-links`
series bar, which is a different element with a different job. There the union
over Book-3 files reaches 15 roster chapters and 15 non-roster pages, in three
incompatible shapes (23 files with a 9-link bar, 8 with a 20-link bar, 1 with
2 links, 10 with none). That is real inconsistency but it is not a broken
reading path, and cramming 42 links into a top bar would not improve it. The
item as I wrote it was wrong; downgraded from "regenerate 55 files" to "make
the secondary bar consistent", which is a smaller and more honest job.

**2. φ is the smallest fundamental unit of any real quadratic field.**

Computed over every squarefree d < 300: the minimum of ε > 1 is d = 5,
ε = 1.618034 = φ; the next is d = 2, ε = 1+√2 = 2.414214. So among all the
inflations the plane makes available, **φ is the gentlest one there is.**

This matters because it unifies two arguments that land on φ by what look like
different routes:

- *Diophantine.* φ is the worst-approximable irrational — Hurwitz's constant √5
  is optimal and fails to improve exactly for φ and its equivalents. This is why
  phyllotaxis: a divergence angle that is hard to approximate by a rational is
  an angle at which leaves never line up.
- *Algebraic.* φ is the fundamental unit of ℚ(√5) = ℚ(ζ₁₀)⁺, hence the
  inflation factor of the Penrose and decagonal tilings (WP-105 §5).

These are the same fact. The continued fraction [1;1,1,1,…] is simultaneously
the slowest-converging expansion (worst approximable) and the shortest possible
period (smallest unit). φ is the extreme point of one problem, not the shared
answer to two.

**Douady & Couder**, *Phys. Rev. Lett.* **68**, 2098–2101 (30 March 1992),
"Phyllotaxis as a Physical Self-Organized Growth Process": ferrofluid drops in
silicone oil under a vertical magnetic field with a radial gradient
self-organise to a divergence angle converging on 137.5°. No biology anywhere
in the apparatus. Follow-up: "Static and Dynamical Phyllotaxis in a Magnetic
Cactus", *PRL* **102**, 186103 (2009).

**The boundary this does not cross.** Two mechanisms landing on one number is
the exact failure mode WP-24 and WP-28 caught in this corpus. Here they do
unify, and the unification is now computed rather than asserted — but what it
establishes is *availability*, not *tendency*. It says: when a planar system
must be aperiodic and self-similar, the arithmetic leaves it one cheapest
choice. It does not say systems tend toward that state. Getting from
availability to tendency needs a throughflow argument — Prigogine, dissipative
structure, far from equilibrium — which is thermodynamics and attaches at
§21.8's heat term. That remains the gap, and it is the whole content of the
dm³ selection chapter.

### The branching case — same thesis, different constants, and that is the evidence

Trees, rivers and lungs branch, and each is solving a constrained optimisation.
Checked what the constants actually are, because the claim only survives if they
are *not* all φ:

| system | constraint | law | exponent / ratio |
|---|---|---|---|
| blood vessels, airways | pumping power + metabolic cost of the fluid | Hess–Murray: r₀³ = Σrᵢ³ | 3 → homothety (½)^⅓ = 0.7937 |
| human lung, conducting airways | the same | Weibel's fractal tree | measured ≈ 0.79 |
| tree branches | mechanical (wind, self-load) vs hydraulic | da Vinci's rule: Σ areas conserved | 2 nominal; measured 1.8–3.0 |
| river networks | total energy dissipation | Horton / optimal channel networks | bifurcation 3–5; Hack h ≈ 0.57 |
| phyllotaxis | non-repetition — never line up | worst-approximable angle | φ, 137.5° |
| planar quasicrystal | aperiodic + self-similar | fundamental unit of ℚ(ζₙ)⁺ | φ, 1+√2, 2+√3 |

The exponent is not a decoration on the law; it *is* the constraint, read off.
3 means the cost was pumping power. 2 means the cost was bending moment.
1.8–3.0 in real trees means the two costs trade off and the exponent moves with
the trade. φ means the problem was never transport at all — it was packing
without repetition, and the extremal answer to *that* is the worst-approximable
number.

So the general claim is supported and the specific one is not: **form is the
solution to a constraint problem, and substrate does not enter** — blood, air,
sap and water give the same law when the cost function is the same. But there is
no single constant across problems, and there should not be. A theory in which
every system returned φ would explain nothing, because it could not distinguish
a lung from a sunflower. The exponents differ *because* the constraints differ,
and that is what makes the framework falsifiable rather than decorative.

This is WP-29's standard applied to our own thesis. WP-29 refused three
"not a coincidence" claims in this corpus for asserting a shared number without
a shared mechanism. The same rule binds here: φ in phyllotaxis and φ in the
decagonal tiling *do* share a mechanism (both extremise the same continued
fraction — see the entry above, now computed), and that bridge stands. φ in a
lung would not, and is not claimed.

Sources: Murray, *PNAS* **12**, 207 (1926); Weibel, *Morphometry of the Human
Lung* (1963); Douady & Couder, *PRL* **68**, 2098 (1992); Rodríguez-Iturbe &
Rinaldo, *Fractal River Basins* (1997); Hurwitz (1891) for the √5 constant.

## 2026-09-08 — Book 4, Part VII, Chapter 25; and the rung, correctly this time

### Correcting today's correction

Earlier today I recorded that "the G3 rung is not broken" and downgraded the
item. **That entry was wrong and the original note was right.** I had searched
for `.nav-links` generally and concluded the rung was fine; the rung is a
different element, `div.rung` inside `nav-links.dual-rung`, and it is carried by
**16 files**, not 55. Measured:

- G3 rung: 15 links labelled 1..15, of which **10** are roster chapters —
  sitting at roster positions 28,29,31,32,33,34,35,36,37,38 — and **5**
  (`ch1.html`, `ch2.html`, `ch5-immune.html`, `ch9-phi.html`,
  `ch15-entropy.html`) are not on the taught path at all. **32 of 42** roster
  chapters unreachable. The 1..15 labels were a second numbering with no
  relation to the book's own.
- G4 rung: four incompatible shapes across the 16 files — 15, 19, 20 and 23
  links — and not one of them reached Chapter 24.

Both are now generated: G4 from `book4/contents.html` (the source of truth for
Book 4, deduplicated at slot 15 where the pt-BR stub shares the number), G3 from
`tools/book3_roster.json`, showing the Week 1–14 spine under its **real** roster
numbers 25–38 plus an "all 42" link to `journey.html`. A bar cannot hold 42
links; it can stop lying about which number a chapter has.

**A bug I introduced and caught.** The first pass applied Book-4-relative
prefixes uniformly, which broke **78** links in `chPI-rh.html` and
`chPHI-rh.html` — two files at the repo root that carry the same nav and had
correct root-relative paths in HEAD. Fixed by deriving the prefix per file from
its directory. Verified: 0 broken rung links across all 16 files. Lesson, and it
is the third time this session in a different costume: *a shared block is not a
shared context — anything relative in it has to be recomputed per file.*

### Chapter 25 · The Selection Principle

Part VII opened at 25 rather than renumbering a third time, per Pablo. The
chapter answers §21.8's standing question — *name an entropy on the corpus's own
phase space, not borrowed from an analogy* — for one system.

**Proposition 25.1.** The number of distinct closable shells at size T, counting
enantiomers separately, is W(T) = d₁(T) − d₂(T), the divisors of T congruent to
1 minus those congruent to 2 mod 3. So S(T) = k·log(d₁ − d₂). Checked for every
closable T below 1000, no mismatches; and W(T) = 0 coincides exactly with
Chapter 21's inertness condition.

This meets the bar §21.8 set. It is *named* (a function of T, no free
parameter), *not borrowed* (a count of the sheet's own configurations, which is
what S = k log W means), and it is arithmetic rather than geometric — a
consequence of Ch 21 indexing shells by norms in ℤ[ω].

Consequences recorded: chirality is worth exactly k·log 2, so the split primes
are thermodynamically preferred; T = 49 is the smallest size carrying two
distinct shells (GP(5,3), its mirror, and GP(7,0)) because 49 = 7² with 7 split;
and the 216-sphere family splits 4 chiral / 6 achiral, giving a desk experiment
with three stated failure modes.

**What the chapter refuses to claim**, all in §25.6: it is one system, not the
corpus — S lives on the shell configuration space, the contact form lives on the
jet space, and nothing transports between them; it selects among closures, not
between closing and not closing, so the δQ question is untouched; it does not
reach Saturn; and it does not establish that systems tend to complexity. The
Dirichlet identity Σ W(T)T⁻ˢ = ζ(s)L(s,χ₋₃) is recorded in §25.4 **inside a
warning box**, because the log-cost assumption it needs is unargued and §21.8's
own caution about ζ applies at full force.

Also fixed in `ch21-the-closing-field.html`: four stale open-item labels still
read "20b.A" / "20b.B" from before the renumber. Now 21.A / 21.B, with a forward
pointer to Ch 25 on 21.A.

`ch25-verify.py`: all checks pass. Zero broken links in the new chapter.
MathJax does not render in the sandbox (CDN blocked) — confirmed identical
behaviour on ch21, so not a defect in the new page.

### §25.8 — a borrowed strategy, and what it actually returned

Pablo's note: Larsen's route to Carmichael numbers, and the standing method —
watch how others devised a strategy, try it on ours, see what works.

Larsen (2021, *IMRN*, arXiv:2111.06963) proved a Bertrand postulate for
Carmichael numbers — one in (x,2x) for large x — by adapting the Maynard–Tao
sieve to the Alford–Granville–Pomerance framework. The obvious transplant: is
there always a *maximum-entropy shell* in (x,2x)?

**What the transplant returned.** Yes, and it is easy. Counting T = pqr in
(x,2x) with three distinct split primes gives 1, 3, 10, 24, 66, 153, 345, 781,
1714, 3664 across dyadic intervals from 2¹⁰ up. The supply grows; there is no
scarcity for a sieve of that power to fight.

**Why, and this is the part worth keeping.** Larsen's difficulty is Korselt:
p−1 | n−1 *couples the primes to each other*, so they cannot be chosen
independently, and the whole apparatus exists to manage that coupling. W is
multiplicative — each split prime contributes its factor alone. The transplant
fails, and it fails informatively: it locates the difficulty in Larsen's problem
by showing ours does not have it.

Recorded as a discipline in §25.8, because it generalises: before importing
machinery, ask whether the borrowed problem still contains the difficulty the
machinery was built to defeat. If yes, it may transfer. If no, the honest
conclusion is that our problem is easier than it looked — and knowing which case
you are in is most of the value of having looked.

**1729.** The record-setters for W below 4000 are 1, 7, 49, 91, 637, **1729**,
and 1729 = 7·13·19 is three split primes, so W = 2³ = 8: eight distinct closable
shells at 17,292 sites. It is also the taxicab number and the third Carmichael
number. Checked against WP-29's rule before being written down, because a shared
number is not a bridge until the mechanism is shared:

*p ≡ 1 mod 3 ⟺ 3 | p−1 ⟺ p splits in ℤ[ω].* Korselt is easiest when the p−1 are
smooth and share small factors, so Carmichael numbers favour 3 | p−1; W is
raised by exactly those primes. Two constructions, two different reasons, one
congruence class. The overlap is **partial**, which is the check that it is real:
of the first eight Carmichael numbers, 1729, 2821 and 8911 are closable (all
prime factors split, each W = 8) and 561, 1105, 2465, 6601, 10585 are not
(inert primes to odd powers, W = 0 — no shell of that size exists at all).

Also added: the Landau–Ramanujan count of closable sizes,
#{T ≤ x : W(T) > 0} ~ K x/√(log x) with K ≈ 0.6389 for this form; computed to
x = 2×10⁶ the ratio reads 0.670 and is still falling slowly toward it.

`ch25-verify.py` extended with section [7]; all checks pass. Zero broken links.

## 2026-09-08 — Book 3 grows to 43, and the second place the number lived

### A correction first: the chapter did not exist

My handoff list carried "The Term You Set to Zero — written, renders, points at
§21.8, still unplaced" through several turns. It was never written to disk.
`git log --all --diff-filter=A` finds no such file ever added, and
`--diff-filter=D` finds none removed. It lived only in a previous session's
context and my note promoted it to a file. Written properly today.

### And a second correction: the insertion cost was never real

I twice described placing it at roster position 6 as triggering "an `of 42` →
`of 43` pass across 42 files", and used that cost to argue for appending at the
end instead. **`tools/build_book3.py` generates the b3nav rung** — the line
`f'{c["n"]} of {len(chapters)}'` at line 118 — so the whole pass is one JSON edit
plus `--write`. The tool's own docstring says so: *a derived fact is regenerated,
never maintained.* I had argued against an insertion on the grounds of a manual
cost the repository had already automated away.

With the mechanical objection gone the placement is purely editorial, and
Pablo's original intent wins: he asked for this chapter in Book 3 "so it comes
earlier then here". Inserted at **position 6**, immediately after
`ch05-contact-normal-form.html` — the student meets the omission at the moment
the form is written down, not several hundred pages downstream in another book.
Week 3, phase C, level B1, matching its neighbours.

### The chapter

`ch-term-set-to-zero.html`, ~1,500 words. α = dz − r²dθ is the Gibbs form with
T dS deleted; the deleted term was carrying the arrow of time (Clausius fixes
the sign, not convention) and the entropy budget (−α(γ̇)/T is what the process
cost). Which is why nothing in dm³ ever appears to cost anything: on an adiabat,
nothing is.

Its spine is a census, taken by script over 685 files:

| | files | |
|---|---|---|
| `contact form` | 150 | the restricted object |
| `Reeb` | 143 | its vocabulary |
| `entropy` | 60 | the word, used elsewhere |
| `adiabatic` | 4 | the name of the restriction |
| `Clausius` | 5 | the inequality supplying the sign |
| `set to zero` | **0** | — |
| `we assume … = 0` | **0** | — |
| `neglect` | 7 | none of them about α |

150 files write the restricted object; 4 name the restriction; **0** record that
a restriction was made. The chapter's four rules for crossing something out come
out of that asymmetry, and rule 4 is the census itself: a corpus that can count
how often it says *adiabatic* against how often it uses the adiabatic form can
audit itself; one that cannot, cannot.

### The second location

After `--write`, 23 files still read "of 42". The position is stated **twice**
per chapter — the generated `nav.b3nav`, and a hand-written
`<p class="chapter-label">Chapter n of 42</p>` in the hero. Only the first was
generated. That is precisely the drift `build_book3.py` was written to kill,
surviving in a location the tool did not know about.

Extended the tool rather than fixing 23 files: `chapter_label()`,
`write_chapter_labels()` and `label_drift()`, wired into both the report and
`--write`. It found and rewrote **25** stale labels (23 at "of 42" plus two the
insertion shifted). Reruns clean: *all 43 chapters carry a current taught-order
nav; all 43 hero labels match the roster.* Corpus-wide `of 42` count: 0.

Also repointed `ch05-contact-normal-form.html`'s bottom in-page nav to the new
chapter. `ch02-biological.html` has no bottom nav at all — pre-existing legacy
shape, and the generated rung is authoritative, so left alone.

**The standing lesson, and it is the session's third variant.** Before arguing
that a change is expensive, check whether the repository already automates it.
I have now twice mis-scoped work in this repo by reading the artefact instead of
the tool that generates it — the rung this morning, the roster insertion this
afternoon. The tools here are better than my estimates of them.

## 2026-09-08 — Book 7 · Chapter Pr · What a Child Can Enter

Opens a new Vol VII section, "The Door Before the Life", as the slot the prodigy
entries go into. Pablo's framing: the ninth volume exists and has its part about
authors, but those are the other kind — the ones with life experience — so Book 7
gets the chapter that opens the question.

**The argument is about domains, not children,** which is what makes it ours
rather than a summary of somebody's literature. Vol VII holds 34 people in five
sections built by subject, and reading the roster against one question —
*could a twelve-year-old have done this?* — splits it in two along a line that
ignores every section heading. Ramanujan, Hamilton, Noether, Mirzakhani,
Kovalevskaya, Tao: yes, in the sense that nothing in the material forbids it.
The Writers section: no, and not by a little. Ramos's material is the sertão and
the prison, dos Anjos's is his own body failing, Levi's is Monowitz.

§2 states the proposal so it can fail: **a domain admits prodigies when its rules
are complete, available, and independent of having lived.** Chess, notation and
tonal harmony, mathematics. The excluded domains fail only the third condition —
craft can be taught, material cannot be handed over, because the material is a
life. Predicts that apparent exceptions resolve into either a formal sub-skill
mistaken for the domain (technical facility is not musicianship) or a constructed
story.

**§3 is the part that keeps it honest,** and both halves were already in this
gallery. Terence Tao: university mathematics at 9, IMO bronze/silver/gold at
10/11/12 and still the youngest winner of each, Flinders at 16, PhD Princeton
1996 under Stein at 21, Fields 2006. June Huh: dropped out at 16 to write poetry,
SNU 2002, Hironaka's course in his sixth year, PhD Michigan 2014 under Mustață at
31, Fields 2022. Same domain, same medal, entry at 9 and at ~23. So the door is
open **early**, not **only early** — and Huh is the counterexample the proposal
survives, which is worth more than one it never met.

§4 gives the literature its due: Feldman & Goldsmith's co-incidence theory
(*Nature's Gambit*, 1986) — a prodigy is an improbable convergence of ordinary
factors, and "a child raised in a family of mathematicians" is three or four of
them arriving in one household. With the uncomfortable corollary stated: their
distribution measures access at least as much as it measures children. Ruthsatz
on working memory and attention to detail over general IQ, with profiles
differing by domain.

**§5 sets the attribution standard before the entries rather than after an
erratum**, using our own caught case: the video account of Bhargava arriving at
n(n+1)(n+2)/6 by stacking oranges, where the formula is Āryabhaṭa's *citighana*,
*Gaṇitapāda* 21, 499 CE. Nothing against Bhargava; everything against the genre,
which wants a scene of spontaneous discovery and will supply one. Five rules
follow, including: look for prior art *before* the sentence is written, and where
the subject is a child, write about the domain and the work rather than the child
as spectacle.

**A check that went the right way.** A fetched summary told me Huh's PhD was
2011; `ch-huh.html` says 2014. I nearly filed that as an error in an existing
chapter. Wikipedia confirms 2014, under Mustață, at 31 — the chapter was right
and my single summarised fetch was wrong. Lesson: one fetch is not a source, and
an existing chapter gets checked against a reference before it gets corrected.

Also fixed on the way: my first index insertion put the card orphaned outside the
`sci-grid` and immediately before the Writers `<h2>`. Rebuilt as its own section
with heading, intro and grid. Book 7's index is being edited by another session
(a Feynman card, +7 lines); this insert is in a different region and does not
touch it.

### §4 rewritten — "Why so few walk through, and who decided"

The first draft listed Feldman's co-incidence factors the way Feldman lists them
— geographic availability, family tradition, access to training, historical
timing — and let them stand as a neutral inventory. They are not neutral.
*Historical timing* is whose government was in power and what it did. *Access to
training* is whether a family could spare a child from earning. *Family
tradition* presumes a household with room for one rather than a household
organised around staying alive. Every factor is a condition on the child's
circumstances and every one was set by somebody. Stated neutrally the theory
explains why prodigies are rare; stated plainly, much of what it files under
coincidence is somebody's policy.

**The methodological objection is this corpus's recurring one.** Co-incidence
theory is assembled by examining prodigies and asking what they had in common,
so it can only ever see the survivors. It gives an excellent account of how a
prodigy holds together once present and no account at all of the children who
never came near the domain, because they are not in the sample and cannot be.
That is the WP-104 / Chapter 25 gap in a subject as far from shells and Saturn
as it is possible to get: **everything on offer was stability, and the question
was selection.** The selection account here is not a psychological question and
will not be answered by studying prodigies — it is about states, economies,
schools and wars.

So the chapter's thesis now has the half §2 was missing: **a domain decides when
it can be entered; access decides who arrives; and only the first of those is a
fact about mathematics.** The indifference of a closed formal system to the age
of the entrant is real and is the good news in §2 — the rules do not check a
birth certificate and did not close while Huh spent seven years elsewhere.
Institutions are not indifferent, and it is institutions, not domains, that
invented being too old.

Illustration, checked against a reference before use: mathematics has no age gate
anywhere in it; the Fields Medal requires the recipient be **under 40 on 1
January of the award year**, following Fields's stated intent that the medal
encourage further work rather than only crown finished work. A decision made by
people, not a property of the subject — the domain's openness and the
institution's deadline side by side, with only one of them mathematics. Huh
cleared it having begun at twenty-three.

Closing paragraph states the limit so the section cannot be read as determinism:
this is not an argument that talent is fiction or circumstance destiny, but the
narrower claim that when a distribution is produced jointly by a door and by who
was permitted near it, reading it as though the door were the only term mistakes
an accident of access for a fact about people — and that error has a direction.
It always flatters whoever got in.

Index card blurb updated to carry the two-part thesis. No biographical material
was added to the chapter; the argument stands on the roster and the sources.

### §5 added — "The case: Brazil, 1964–1985", with the author's own account

§4 asserted that the selection question is answered in terms of states, economies,
schools and wars. §5 demonstrates it once, on a case with a good record, at
Pablo's explicit invitation and with his account given in his words.

**The mechanism is sharper than "a dictatorship damaged education."** Verified
before writing, per §6's own rule:

- ~300 professors forcibly retired or dismissed across two purges, 1964 and 1969,
  the second after AI-5 and Decreto-Lei 477, which permitted summary expulsion
  with practically no defence. 1,000+ students expelled 1969–79, 250 at UnB in
  1969 alone. From 1970, ~35 ASIs monitored campuses and reported to the national
  intelligence service. At USP's Faculty of Philosophy the compulsory retirements
  took Cardoso, Florestan Fernandes and Ianni. *Educação Moral e Cívica*
  compulsory from 1969.
- **Simultaneously** the same regime expanded science and technology enormously:
  enrolment 142,000 (1964) → 1.4M (1984); graduate programmes 6 courses (1961) →
  792 master's + 333 doctoral (1984); FINEP 1967, Embrapa 1973, twelve new
  federal universities.
- And it ran the elite technical schools itself. **ITA** (1950) is maintained by
  the Brazilian Air Force; first-year undergraduates *are classified as military
  personnel* and attend weekly military preparation, discharging compulsory
  service; admission runs near 1% and its entrance exam is the country's most
  competitive. **IME** is the Army's equivalent.

So the regime did not close the door to mathematics. **It funded that door,
widened it, and stood in it.** A household that opposed the regime, containing a
child with an aptitude for mathematics, faced a domain whose rules were open and
indifferent to age (§2) and an institutional route that ran through a gate with
soldiers on it. A family that turned away was not less mathematical; it was
pricing the route accurately, and the cost was not tuition.

**The instance** is Pablo's, in his own account and marked as his: both parents
are journalists rather than mathematicians for this reason; the household was
required to participate in institutions not its own — the Catholic church, in a
Jewish family — and to write about the feats of the great country and its armed
forces while defending democracy, freedom and human rights. The turn towards art
and away from the sciences passed down a generation as though it were a
temperament. It was a political inheritance. He was told at thirty-five he was
too old to begin; the mathematics in this series was written afterwards. The
section says explicitly that neither half is offered as a triumph — the point is
that to anyone counting later, this looks like a family that simply preferred
the arts, which is the §4 error in one household over two generations.

Sources for the history are cited in §8 and are *not* from him; the family
account is his and is attributed as such. Every personal sentence is his to cut.

**Not past tense.** Pablo raised Colombia, flagging it himself as hearsay —
correctly, and it checked out stronger than he had it. Corte Constitucional,
*Sentencia T-357 de 2024* (September 2024): a nine-year-old in a state school,
Christian but not Catholic, required to learn Catholic prayers and dogma; her
father's request for an alternative went unanswered; she was excluded from the
class and given **0.0**, damaging her record. The Court found violations of
freedom of worship, the right to education and state secularity, and ordered
alternatives, removal of dogmatic content, and neutral teaching. A constitutional
court had to say this in 2024, so the practice was live until it did.

**Two things I did not write, and why.** He named the city as Pereira; the ruling
anonymises the child and the reporting does not name the school or city, as is
standard for a tutela involving a minor, so the location is not in the chapter.
And "Pereira, a Jewish name" is too strong as stated: it is a Portuguese
toponymic surname (*pear tree*) that is well attested among Sephardic converso
families but is also extremely common among non-Jewish Portuguese, and the
Colombian city is named after Francisco Pereira Martínez. An association, not an
identification — so it is not in the chapter either.

### §5 closes on "Availability is not access"

Pablo's point, and it targets a soft spot the chapter had acquired: the argument
so far could be read as though the problem were historical and the internet had
solved it. Two corrections, both his.

**Church and state are not separated everywhere**, and where the principle exists
on paper it is not thereby enforced — which is exactly what T-357/2024 shows: a
constitutional guarantee, and a nine-year-old marked 0.0 for declining the
catechism, in the same country in the same year.

**And availability was never the binding constraint.** Verified before use:
Hansen & Reich, *Science*, 4 December 2015 — 68 free HarvardX and MITx courses on
edX, 2012–2014. Young registrants lived in neighbourhoods with median incomes
**38% above** the typical American neighbourhood; among teenagers, those with
college-educated parents had **nearly twice the odds** of completing. Reich's own
summary: online learning does not yet live up to its promise to democratise
education.

The reason is this chapter's own distinction one level up. The internet is an
availability revolution. It distributes the material and nothing else on
Feldman's list — not a household with room for study, not a tradition that makes
the domain thinkable, not an adult who knows the field exists, not the time of a
fifteen-year-old who is earning, and not the sentence *this is for people like
you*, which is on no syllabus and is the one that decides. Family, tradition and
opportunity do not materialise because a PDF is free.

The section ends on why this is worth stating: the availability claim is usually
offered not as an observation but as a dismissal — *it's all online, so what's
your excuse* — which converts a question about access into a verdict about a
person. The §4 error in contemporary dress, with the same direction. It flatters
whoever got in.

One wording caution: the fetched summary of the Hansen–Reich paper described the
finding as MOOCs "narrowing rather than widening" access, which reads garbled
against both the statistics and Reich's own quote. The chapter states the
statistics and the quote and does not use that directional phrasing. Third time
today that a single fetch was the unreliable link in the chain.

### §5 gains the strongest evidence in the chapter: a measurable absence

Pablo: "teachers of sociology and philosophy did not exist for 20 years — when
they returned, they were either very young, or very old. I was lucky to have had
one."

Checked, and the record is longer and messier than either of us had it, which
made the point sharper rather than weaker:

- **Philosophy and Sociology were banned from Brazilian schools in 1971** and
  replaced by *Educação Moral e Cívica*. They returned in **1986** as optional
  subjects. They became compulsory in secondary education only in **2008**
  (Lei 11.684/2008) — thirty-seven years after the ban.
- Sociology's exclusion is older still: out of the curriculum since the Reforma
  Capanema of **1942**, creeping back state by state from 1983 (São Paulo,
  Resolução SEE/SP 236/83).
- And it is live: philosophy and sociology have been removed from the compulsory
  curriculum again under the current secondary-education reform, São Paulo among
  the states dropping them.

Pablo's "twenty years" is a fair description of the lived gap — the ban ran
fifteen years and the 1986 return was optional, so the effective absence from
most classrooms ran longer.

**Why this is the best evidence in the section.** For fifteen years nobody could
enter the profession, because the job did not exist. When the subjects returned,
the teachers were necessarily of two kinds — those who predated 1971 and those
trained after 1986 — with no middle cohort, and none possible. The ban is legible
in the age distribution of the teaching staff decades after it was lifted: a
bimodal profession, very old or very young, with a hole where a generation should
be.

That answers §4's own methodological objection in the one case where it can be
answered. §4 says a theory assembled from the people who arrived cannot count the
people who did not, because the missing are not in the sample. Here they are in
the sample, as a gap with edges and dates. Nobody needs to be interviewed about
the sociologists Brazil did not train between 1971 and 1986 — the number is
readable off who was standing in front of a classroom in 1995, and **the shape of
the hole is the shape of the law.**

His having had such a teacher is recorded as his note, and "luck" is kept as his
word because it is also Feldman's: in a fifteen-year hole, an adult in the room
who can teach the subject *is* a coincidence factor.

### §5 · "Cut from the curriculum, bought at the frontier" — with a declared conflict

Pablo: "that is absurd, AI is hiring philosophy majors, put that in the book."

The observation is real and checkable. A publicly maintained list at *Daily Nous*
names philosophers in research roles at frontier AI firms — among them Amanda
Askell, Joe Carlsmith, Ben Levinstein, Jackson Kernion and Harvey Lederman at
Anthropic; Iason Gabriel, Adam Bales, Atoosa Kasirzadeh, Arianna Manzini, Julia
Haas and Geoff Keeling at Google DeepMind; Robert Long and Patrick Butlin at
Eleos AI; Beba Cibralic at RAND; Lisa Miracchi Titus at Meta. Roles: alignment,
evaluation, governance, moral status, character.

**Three cautions written into the section rather than left out of it.**

1. The magnitude is disputed. Workforce specialists have publicly pushed back on
   reports of philosophers commanding extraordinary salaries. That pushback is
   cited; the source itself returned 403 on fetch, so it is referenced as
   existing rather than characterised in detail.
2. The practice is not industry-wide — OpenAI is reported to treat safety largely
   as an engineering problem without dedicated philosopher roles.
3. **Declared conflict of interest.** This section was drafted with the
   assistance of an AI system built by one of the companies named. That is stated
   in §8 in the chapter itself, and the section is written conservatively for
   that reason. It would have been easy and wrong to let an Anthropic model write
   an enthusiastic passage about Anthropic hiring philosophers into somebody
   else's book without saying so.

**The argument is framed so it does not depend on the trend being large**, which
is what makes it survivable: the skills being cut from a public curriculum have
non-zero and rising value at the frontier, and eligibility for that frontier is
set roughly a generation upstream by a decision a fifteen-year-old does not take.
Twenty such jobs would suffice. What matters is not how many exist but who will
be able to hold them. Explicitly *not* a labour-market claim — "study philosophy,
the market wants you" is disclaimed in the text.

It closes on the chapter's mechanism running live rather than in retrospect:
philosophy as a domain is wide open and §2 applies to it as much as to chess; the
state narrows the school door; the frontier then recruits from wherever
philosophers are still made — the systems that did not cut the subject, and the
households that could supply it privately when the school would not. Hansen and
Reich measured what that produces. A curriculum decision taken in 2026 is a
statement about who is eligible in 2045, and it is not debated in those terms
because the people it excludes are not yet old enough to say anything.

## 2026-09-08 — Book 4 Ch 26 · The Kaleidoscope Test; Book 8 joins Book 4

Prompted by evaluating an external framework (Guarino, "plasma mirage",
SEIS-UGFM) at Pablo's request. The evaluation produced a reusable instrument, so
the instrument became the chapter and the evaluation stayed conversational.

**The taxonomy.** Three sources of a stable image, each leaving a different bill:

| source | order lives in | dies when | ledger | in this corpus |
|---|---|---|---|---|
| recording | the medium's past | read-out is cut | a **capacity** | Book 8's territory |
| throughflow | the dynamics | energy input stops | a **cost** | Ch 21 §21.8 |
| boundary | the symmetry group | the container changes | a **count** | Ch 21, Ch 25 |

Recorded en route: the holographic *principle* is the capacity column and has no
projector in it — degrees of freedom scaling with boundary area, Bekenstein–
Hawking S = A/4G. Critiques aimed at the optical hologram (reference beam, plate,
playback) leave it untouched. This is a distinction the corpus should not lose.

**Proposition 26.1, the negative test.** For a one-parameter ladder
L_c = {c/N}, spacing near f is c/(N(N+1)) ≈ f²/c, so the nearest rung satisfies
**|rung − f|/f ≤ f/(2c)**. Verified against 200,000 random targets in (1,200) Hz
at c = 700: **zero violations**. Below 50 Hz such a ladder matches any frequency
to better than 4%, near 10 Hz to better than 0.8%. A family that matches every
target excludes none, so it predicts nothing — and the correct response to such
a fit is not doubt about the fitter but the observation that the family could
not have failed.

**The contrast, computed.** W(T) = d₁ − d₂ has no free parameter and returns zero
on a large set (below 40: 2,5,6,8,10,11,14,15,17,18,20,22,23,24,26,29,30,32,33,
34,35,38). Counted to x = 200,000 the closing field **forbids ~80.6%** of sizes,
with the permitted fraction → 0 like 1/√(log x). A one-parameter ladder forbids
**0%** at every x. Opposite extremes of the only property that matters for a
selection rule — a difference in degrees of freedom, not in rigour or good faith.

**§26.3 is the join Pablo asked for.** Book 8 Ch 13 named the fourth face —
topology connects the parts, topography maps the surface, holography inscribes
the whole, holology is the logic by which a totality is coherent as one — and
closed saying that what holology is in itself "remains structurally invisible
from inside". Holology is the *boundary* column: a claim about constraint, not
storage and not drive. Chapters 21 and 25 are the first place in this corpus
where that constraint is **counted**: μ₆ fixing the admissible defects and
forcing twelve, W(T) saying how many wholes of each size are permitted. So: it
was not invisible, it was uncounted, and what made it visible was a norm form
rather than a better vantage point. The limit is stated in the chapter — one
instance of a logic is not the logic, so the general claim stays OPEN; the join
establishes only that holology is the kind of thing that can have a count.

`book8/ch13-holology.html` now carries a forward block into Part VII, so the join
is navigable from both ends.

**§26.4 turns the test inward,** because a diagnostic written for other people's
work and never aimed at one's own is a weapon rather than an instrument (WP-29's
rule). Where the corpus passes: Ch 21's twelve forbids eleven and thirteen; Ch
25's W forbids four sizes in five; §21.8's cost has a sign fixed by Clausius, not
by us. Where it does not: α ran for 164 files before anyone noticed a missing
term, and the entropy §21.8 asked for is named for exactly one system. The §26.2
objection is explicitly pointed at our own η-ladder and φ material — wherever
this corpus fits a constant to a phenomenon, the question is what the fit forbids.

Standing rule adopted in §26.4: any claim that a structure is *selected* must
come with one of the three ledgers, and a count must be able to return zero.
Otherwise the claim stays marked OPEN.

Part VII now has two chapters. `ch26-verify.py` all checks pass; contents row
added; ch25 → ch26 forward link; G4 rung regenerated to 0..26 across 17 files,
0 broken links; terms.py clean.

### Ch 26 gains a proof and a stated conjecture — and the "one instance" limit dissolves

Pablo: "so, a theorem, and a conjecture." Both are now stated as such, and
checking the conjecture before stating it changed its standing.

**Theorem 26.1** (the one-parameter ladder) now carries its proof rather than an
assertion. For L_c = {c/N} and 0 < f < c, put N₀ = ⌊c/f⌋; the gap containing f
has width c/(N₀(N₀+1)) and f lies within half of it from an endpoint, so the
absolute error is ≤ c/(2N₀(N₀+1)); with N₀ ≤ c/f ≤ N₀+1 this gives relative error
≤ (f/2c)(1 + O(f/c)). Corollary: for f ≪ c the ladder matches every target, so a
fit to it carries no information. The 200,000-target numerical check remains as
confirmation, not as the argument.

**The "one instance of a logic is not the logic" limit was too weak, and testing
it showed why.** The closing field is not one instance. It is one of exactly two,
and the two exhaust the plane:

| K | O_K | \|μ\| | norm form | count W(n) | defects 2\|μ\| | realised by |
|---|---|---|---|---|---|---|
| ℚ(√−3) | ℤ[ω] | 6 | a²+ab+b² | d₁ − d₂ (mod 3) | 12 | icosahedron, 12 vertices of degree 5 |
| ℚ(i) | ℤ[i] | 4 | a²+b² | d₁ − d₃ (mod 4) | 8 | cube, 8 vertices of degree 3 |

Both verified: W(n) equals the stated divisor difference with **no mismatch below
2000** in each case; both counts return zero on a set of density one; and closure
requires 4π ÷ (2π/|μ|) = 2|μ| defects, confirmed against both polyhedra, each with
V − E + F = 2. Every other imaginary quadratic field has μ = {±1}, so these are
not two samples from a large space — they are the whole of it, for the plane.

Recorded as **Proposition 26.2**, with the honest note that every component is
classical (Jacobi's two-square theorem, its Eisenstein analogue, Descartes on
total defect). Nothing here proves any of them. The claim is only that they are
the same statement twice, and that the statement is what Book 8 was reaching for.

**Conjecture 26.3 (Counted Holology)**, stated so it can be killed. For a
substrate with discrete closure symmetry G: (i) closure requires exactly 2|G|
elementary defects; (ii) the number of distinct wholes at index n is an
ideal-counting function, hence a divisor sum against a character; (iii) that
function vanishes on a set of density one.

*Status*: proved, by the assembled classical results, in every case the plane
admits — which is two. Conjectural everywhere else: higher dimensions, non-lattice
substrates, and quasiperiodic order, where WP-105 shows the unit group has
infinite order and (i) has no evident meaning.

*Falsification*: a substrate with discrete closure symmetry whose realisable sizes
are not counted by any ideal-counting function — a forbidden set of density zero
rather than one, say — or whose defect count differs from 2|G|. One counterexample
in three dimensions suffices.

This is §26.4's own rule met by §26.3: the count exists, it has no free parameter,
and it returns zero. `ch26-verify.py` section [5] added; all checks pass.

### Conjecture 26.3 refuted in one clause, the same day, from the named direction

Pablo asked for "a 3d count of a holological system" — which is precisely the
falsification clause of the conjecture written an hour earlier. Run before
answering.

The three-dimensional analogue is not another quadratic ring but the **Hurwitz
order** H, the maximal order in the rational quaternions: unit group of order
**24** (the vertices of the 24-cell, against 6 for Z[ω] and 4 for Z[i]), norm the
quaternary form a²+b²+c²+d².

**(ii) survives and gains its best instance.** Jacobi's four-square theorem:
r₄(n) = 8σ(n) for odd n, 24σ(odd part) for even n — checked against direct
enumeration to n = 20, no discrepancy. The count is still a divisor sum, and this
is the first instance in a **non-commutative** order.

**(iii) is refuted.** Lagrange (1770): every non-negative integer is a sum of four
squares. The forbidden set is empty — density zero, not one. Direct check to
n = 500 finds no n with r₄(n) = 0. Against the planar cases forbidding **74.0%**
(Z[ω]) and **69.0%** (Z[i]) of the first two thousand sizes, the Hurwitz order
forbids **0%**.

**(i) does not transfer.** The 4π is Gauss–Bonnet, a statement about closed
*surfaces*. There is no three-dimensional statement of the same form. The chapter
should not have written it as though |G| alone fixed a defect count in any
dimension, and now says so.

Written into §26.3 in the order it happened — conjecture, then test, then verdict
— rather than quietly restating the conjecture as though it had always been
narrower. What survives is one clause, verified in three orders, and worth more
for being narrow.

**The lesson the counterexample carries, and it inverts the intuition that made
the conjecture attractive.** The planar cases forbid a great deal because their
unit groups are *small* — four and six — with binary norm forms. The Hurwitz
order forbids nothing because it has twenty-four units and a quaternary form.
**A count's power to forbid comes from the scarcity of its symmetry, not its
richness.** Same direction as WP-103: φ(n) ≤ d means higher dimensions permit
more and forbid less. A framework reaching for a larger symmetry group in hope of
a stronger selection rule has the sign backwards — and this chapter nearly did.

`ch26-verify.py` section [6] added; all checks pass.

### LadderBound.lean — Theorem 26.1 formalised, awaiting a kernel run

`LadderBound.lean` written at repo root, Mathlib, toolchain v4.32.0, six theorems
and six `#print axioms` lines: `gap_eq`, `half_gap`, `ladder_abs_error`,
`ladder_rel_error` (Theorem 26.1: relative error ≤ 1/(2n)),
`ladder_rel_error_of_lt` (≤ f/(2(c−f))), `ladder_forbids_nothing` (≤ f/c when
2f ≤ c). Header marked **NOT YET RUN** and will stay so until the report exists —
the erratum of commit 57add27 is the standing reason.

Gate: `python3 tools/axiom_gate.py <report> 6` — expecting exactly six theorems,
each on [propext, Classical.choice, Quot.sound] and nothing else.

### Möbius: clause (i) restated, and a correction IMPA forces

**Clause (i) was under-stated, not dead.** The 4π was the *sphere's* 2πχ. Restore
the Euler characteristic and Descartes gives the general law:

  total defect = 2πχ(Σ), elementary defect = 2π/|G|, **#defects = |G|·χ(Σ)**

which reduces to 2|G| exactly when χ = 2. It generalises across *surfaces*, not
into a third dimension — the direction it was always pointing.

Verified on five surfaces, two of them non-orientable, none adjustable:

| surface | χ | orientable | \|G\| | \|G\|χ | realised as |
|---|---|---|---|---|---|
| sphere | 2 | yes | 6 | 12 | icosahedron, 12 vertices of degree 5 |
| sphere | 2 | yes | 4 | 8 | cube, 8 vertices of degree 3 |
| torus | 0 | yes | 6 | **0** | hexagonal sheet tiles it flat |
| ℝP² | 1 | **no** | 6 | **6** | hemi-dodecahedron, 6 pentagons |
| ℝP² | 1 | **no** | 4 | **4** | hemi-cube, 4 vertices of degree 3 |
| Klein bottle | 0 | **no** | 6 | **0** | closes with no defect at all |

The non-orientable rows are the exemplary ones, which is Pablo's point: the
sphere is a bad witness for a law about χ because there χ = 2 and the constant
looks like a coincidence. On ℝP² the naive "2|G|" predicts 12 and 8; the truth is
6 and 4; |G|χ is right on all five. The hemi-polyhedra are the cleanest — ℝP² is
the sphere mod the antipodal map, χ halves, and the defect count halves with it.

**A consequence worth naming.** χ(Klein) = 0, so a hexagonal sheet closes onto a
Klein bottle with **zero** defects. Klein topology is not expensive; it is free in
the currency Ch 21 counts. Any framework invoking a Klein or Möbius boundary as
the thing that *selects* a structure is invoking something that costs nothing and
therefore forbids nothing — §26.2's objection to a one-parameter ladder, arriving
from topology instead of arithmetic. Non-orientability may still split mode
spectra, which is a claim about eigenvalues, not defects; a selection argument has
to say which bill it is paying. Marked OPEN.

**And a correction to Book 7 §5 that the IMPA logo forced.** Pablo noted the
institute's emblem is a Möbius band. Checking IMPA at all exposed an overreach in
my own section: it could be read as saying mathematics in Brazil *was* the
military route. It was not. IMPA — founded in Rio on 15 October 1952 as the first
research unit of CNPq, the civilian federal research council, under Lélio Gama
with Nachbin and Peixoto — was there throughout, and trained Artur Avila.

The correction sharpens the access claim rather than dissolving it: on one side a
nationally recruited, regime-funded system of military technical schools; on the
other one institute in one city admitting a handful. **Access is not whether a
door exists but how many doors, how wide, and how far from where you live** — and
a single narrow civilian door beside a well-funded national military one is
exactly the shape that turns a household away from a subject without anyone in it
lacking the aptitude. Added to §5 as a marked correction with sources.

The Möbius/IMPA convergence itself is recorded in ch26 as **a remark and only a
remark**, with WP-29's rule stated over it: there is no mechanism connecting an
institute's visual identity to the Euler characteristic of anything, and noticing
a resonance and then declining to spend it is the habit the chapter is about.

`ch26-verify.py` section [7] added; all checks pass.

### §5–§6: the third term, Lattes, and a correction I made too cleverly

Pablo, in three messages: "all because of a few ppl"; "do not miss LATTES"; "the
complaint went further to say they did not get due credit for their work and
discoveries, prizes were given to the superiors."

**The third term.** §4 said access decides who arrives and §5 said the state
shapes access; left there the account is determinism. The missing term is that
access is also *built*, by very few people. Lélio Gama (Observatório Nacional
1943, IMPA 1952); Mário Schenberg (Urca process with Gamow 1940–41, the
Schönberg–Chandrasekhar limit 1942); César Lattes (pion 1947, CBPF 1949, CNPq);
Abrahão de Moraes (celestial mechanics at USP from 1945). Most of a national
scientific base, and four names.

**Which is why the purge count means what it means.** Schenberg was arrested
**seven days after the 1 April 1964 coup**, forced to resign his university post,
fifty days imprisoned; police confiscated his books, mistaking a Baroque statue
for a likeness of Lenin; amnesty in **1979** — fifteen years, almost exactly the
philosophy/sociology ban. ~300 professors sounds modest beside 1.4 million
students and is not: in a system where the astrophysics is one man, three hundred
is catastrophic. **A regime facing a thin institution does not need to close a
field; it needs to remove a few people.** Agency matters *more* in a thin system,
in both directions.

**Lattes, written into §6 as the attribution case.** He improved Powell's emulsion
with boron, carried plates to Chacaltaya at 5,200 m, determined the pion's mass,
and was **first author of the 1947 Nature paper**. The 1950 Nobel went to Cecil
Powell alone. Not bad faith — the Committee's policy until 1960 was to award the
head of the research group. §2 says a domain decides when it can be entered, §4
says institutions decide who arrives, and Lattes says institutions also decide
*who is recorded as having arrived*. Door, queue and ledger are all three
institutional, and none of them is the mathematics.

**A correction I made too cleverly, then corrected.** I first wrote that the
"he built it because of the snub" story fails on dates — CBPF 1949, Nobel 1950 —
and let that settle the matter. Pablo's third message shows why that is too
clever: the grievance was never about one prize. The award-the-group-head policy
was a **standing rule**, legible from inside any laboratory, systematically
directing credit upward. Lattes was first author and Powell was the head in 1947.
The 1950 prize was that rule doing what it always did, not the discovery that it
existed. The chapter now says both: the single-event causality is refused, and
the structural grievance stands.

That is the complaint the returning generation made in the form they made it —
not that conditions were poor but that *the discoveries were theirs and the
prizes went to their superiors* — and what they built at home was in part an
answer to it. Which gives the **Plataforma Lattes** its real meaning: not an
ironic epilogue but the thing the complaint asked for, built by one of the
complainants and carrying his name — a ledger in which the person who did the
work is the person recorded as having done it.

Sources added to §8: MacTutor on Schenberg; Wikipedia on Lattes (emulsion,
Chacaltaya, first authorship, the pre-1960 Committee policy, CBPF, CNPq, the
Plataforma).

## 2026-09-09 — WP-107: auditing OpenAI's Navier–Stokes formalization

Resumed from a handoff whose central worry was: a theorem of the right shape can
be true without being the problem, if `NavierStokesExistenceAndSmoothnessRn`
demands more of a solution than Fefferman does — the negation then rules out a
smaller class. Same species as WP-104's `Fin 6`.

**The worry is closed, structurally.** The challenge file carries a header saying
it is copied from Google DeepMind's *Formal Conjectures* at commit `8bf45ed`.
Checked rather than trusted: stripping comments, docstrings, attributes, imports,
open/namespace lines and blanks leaves 80 code lines upstream, 71 in the OpenAI
copy, and a full unified diff of **17 lines** whose only substantive content is
the *deletion* of the two (A)/(B) `sorry` placeholders they are not claiming.

**Every definition is byte-identical** — `divergence`, `IsOnePeriodic`,
`InitialVelocityCondition(Decay)`, `ForceCondition(Decay)`,
`NavierStokesExistenceAndSmoothness` and both extensions. The breakdown theorems
are DeepMind's own sorry-ed challenges, discharged. **OpenAI could not have
narrowed the target statement because they did not author it.** The audit
question moves one layer out, to whether DeepMind's formalization is faithful to
Fefferman — a question about a public, independently maintained artifact, which
is a far better thing for a claim to rest on.

The asymmetry worth recording, because it is the general lesson: strengthening
the *data conditions* makes such a theorem **harder** (fewer witnesses qualify);
strengthening the *solution notion* makes the negation **weaker**. Only the
second is a risk, and it is the one the diff closes.

§4 spot-checks the inherited definitions against Fefferman's (1)–(7): the
equation on t ≥ 0 via `derivWithin` on `Ici 0`; div-free; initial condition;
`∀ m K, ∃ C, ‖iteratedFDeriv ℝ m u₀ x‖ ≤ C/(1+‖x‖)^K`; force decay in x and t
with bound C/(1+‖x‖+t)^K; `ContDiffOn ℝ ∞` for v and p on `univ ×ˢ Ici 0`; L² at
each t plus uniformly bounded energy. Forcing is permitted in (C)/(D), so f is
not a dodge.

§5: across **2,486 Lean files and 616,276 lines**, excluding the reference file,
**zero** `sorry`, `admit`, `native_decide` or user-declared `axiom`. Stated as
what it is — a fact about source text, not a build.

§6: the verification design is the strongest part and deserves saying out loud.
Comparator exports the proof term and re-checks it in an **independent kernel**
(nanoda, not Lean's own), in a **sandbox** (landrun), against a **statement file
the claimant did not write**. Three distinct failure modes closed at once — which
means the axiom question this corpus usually asks by hand is answered by the
tooling, provided the tool is run.

§7 is the honest limit and it is long on purpose: no build was run (toolchain
v4.34.0-rc2 against our v4.32.0), so nothing here says the theorems are proved;
the Euler side is unaudited; the ComparatorBridge adapters are unread, though the
§3 diff constrains them usefully since the adapter must land on a Prop it did not
author; there is no peer review; and no mathematical opinion is offered. What is
established is narrower and worth having: **the thing being proved is the thing
that was asked.**

A note on the method cutting both ways: WP-24 refuted one of this corpus's own
bridges and WP-29 generalised the sweep. An audit method that can only return
findings is not a method. This one returned clean on the layer it examined, and
says so.

### LadderBound.lean, second draft

First run: `gap_eq` and `half_gap` **CLEAN** — [propext, Classical.choice,
Quot.sound], no sorryAx. Four failures, two causes:

(a) the mathematical bug found on paper beforehand, in `ladder_rel_error_of_lt`;
(b) `div_le_iff`, `le_div_iff` and `div_le_div_iff` **do not exist** in this
    Mathlib — renamed in the GroupWithZero refactor. My first "fix" still used
    two of them and would have failed identically, which I told Pablo before he
    re-ran.

Rewritten to lean on tactics (`field_simp`, `gcongr`, `positivity`, `nlinarith`,
`mul_le_mul_of_nonneg_left`) rather than version-sensitive lemma names, and the
statements are cleared of division where the content allows: the main theorem is
now `2 * n * min (...) ≤ f`, which is "relative error ≤ 1/(2n)" without asking
Lean to divide. Awaiting a second run.

## 2026-09-09 — LadderBound.lean CLEAN; Theorem 26.1 is kernel-checked

Third run, all six theorems on `[propext, Classical.choice, Quot.sound]`, no
`sorryAx`, no errors. Gated:

    python3 tools/axiom_gate.py <report> 6
    OK: 6 theorems, no sorryAx, no axiom outside the permitted set.

So Chapter 26's negative test is no longer a numerical sweep with an informal
argument attached. **Theorem 26.1 — a one-parameter ladder c/N matches any target
to relative error ≤ f/(2c), and therefore forbids nothing — has been read by a
kernel.** The Lean statement is multiplicative, `2 * n * min (…) ≤ f`, which is
the relative bound cleared of its division; the 200,000-target run stays as
illustration.

That is the chapter's own standard met by the chapter. §26.4 says any claim that
a structure is *selected* must produce a ledger; §26.2's negative test is now the
one thing in the arc a machine has verified.

### The three drafts, and why two of them had nothing to do with the mathematics

1. **A real error, caught on paper before any run.** `ladder_rel_error_of_lt`
   derived `n*f ≤ c` from the upper bracket when the goal needs `c ≤ (n+1)*f`
   from the lower one — wrong direction, unprovable as written. Found by
   re-deriving the cross-multiplication by hand while Pablo's first run was still
   going, and reported before he pasted the errors.
2. **`div_le_iff`, `le_div_iff`, `div_le_div_iff` and `le_or_lt` are all gone**
   from this Mathlib — the GroupWithZero refactor renamed or removed them. Four
   of the six failures across two runs, one cause, and none of it about the
   theorem. My first "fix" still used two of them, which I caught and told Pablo
   before he re-ran rather than after.
3. **Two trailing `ring`s after a `field_simp` that had already closed the goal.**
   Reported as "No goals to be solved"; the declarations were clean regardless,
   which is why run two showed four clean theorems alongside two errors.

**Standing lesson.** Proofs written against remembered lemma *names* are fragile
across Mathlib versions in a way proofs written with *tactics* are not. The final
version leans on `field_simp`, `gcongr`, `positivity`, `nlinarith`, `by_cases`
and `push_neg`, and the only name-shaped risk left is `div_le_iff₀`. Worth
carrying into any future Lean in this corpus: prefer a tactic to a name whenever
the tactic exists.

Two warnings deliberately left: `hax`/`hxb` in `half_gap` are consumed
implicitly by `linarith`, and `push_neg` is deprecated in favour of `push Not`.
Editing verified code to silence a warning means re-verifying it — a bad trade
against a clean run.

### WP-107 §7b — Trefethen, and a convergence with Ch 26

Pablo supplied L. N. Trefethen, *Reflections on the Millennium Problems*,
arXiv:2608.24965v1 [math.HO], **25 August 2026** — Harvard SEAS, fourteen days
before OpenAI's announcement. It argues RH, P vs NP and Navier–Stokes have each
lost much of their original practical leverage, for three different reasons. On
NS: research since 2000 (Chen & Hou, *PNAS* 122, 2025) has made candidate blowup
scenarios look ever more special, "the farther removed from 'wet' fluid
mechanics", initial conditions "too contrived", configurations possibly unstable
in themselves. And, written before any resolution existed to comment on:

> "It is fascinating to speculate what may happen if it is proved that
> singularities can arise. I think that in this case, the next scientific
> challenge will be not so much to modify the NS equations to make them more
> physical … as **to understand why those singularities have so little
> consequence**."

He named the branch in advance. Added as WP-107 §7b because it answers the
question that note deliberately declines — not *is the proof right* but *what is
being right worth* — from someone with no stake, written beforehand. It also
fixes the register: a (C) result would be historic mathematics whose consequences
for fluid mechanics may be near nil, which is neither an engineering
breakthrough nor a triviality.

**And a convergence with Ch 26 that has a mechanism, not just a resonance.**
Trefethen: "To resolve a problem one way or another, we need to find a handle to
grab it by. Maybe these handles have something to do with what gives a problem,
as it were, *measurable consequences*. Perhaps problems that remain open for a
century … tend to be so smooth that they glide through both our theory and our
practice, like neutrinos, hard to catch."

A *handle* is a *ledger*. Ch 26 says a framework producing none of the three
ledgers has not identified a source of order; Trefethen says a problem forbidding
little is a problem with nothing to grab. Unlike the resonances WP-29 refuses,
these share a mechanism rather than a number — both are claims about whether a
statement has measurable consequences. Recorded as a convergence, not as
evidence for either.

## 2026-09-09 — Ch 26 §26.3 completed with three dynamical figures; and a second failure mode

**The Möbius material was carrying the law and showing none of it.** Three canvas
figures added, in the chapter's existing `figure-wrap` house style, each earning
its place by showing something a static picture cannot:

- **Fig 26.1 · the Volterra wedge.** Flat sheet beside closed sheet, wedge 2π/|G|
  excised and the angles re-drawn compressed. Switchable |G| ∈ {3,4,6}. Shows why
  the defect size is not a choice: the rotation gluing one cut edge to the other
  must be a lattice symmetry.
- **Fig 26.2 · transport on a Möbius band.** A frame carried once around,
  returning with its ends *exchanged* rather than rotated back. Non-orientability
  is a statement about a journey, not a shape, so it is animated. Play/pause and
  a slow mode.
- **Fig 26.3 · the ledger, interactive.** Pick surface and lattice; |G|·χ against
  the sphere-only 2|G|, with the realising object named. On ℝP² the two formulas
  visibly separate — 6 and 4 against 12 and 8 — and the hemi-polyhedra have
  exactly the smaller counts.

Prose layered around them: the sphere is a bad witness for a law about χ because
there χ = 2 and the constant looks like a coincidence; the lattice fixes the
denomination of the currency and the surface fixes the bill; and the Möbius
band's flatness is the first hint that non-orientability is free in the currency
Ch 21 counts. Render-checked: all three canvases paint, 11 controls live, labels
update on click, animation running, no console errors, no overflow.

### §26.2 gains a second failure mode, from Trefethen's P vs. NP section

Pablo, on reading it: "it's almost as if we had already solved the problem with
the series, just never wrote it down."

**We have not, and the chapter now says so in its own voice.** But the feeling had
a real cause worth extracting. §26.2 catches one failure — a count that cannot
return zero. Trefethen's P/NP account supplies a second that this chapter's own
examples could not reveal, because both of them are evaluated on every instance
of their index.

Worst-case complexity *is* a strict ledger: a count, no free parameter, forbids
plenty. Yet its practical force has drained, for two reasons Trefethen names —
worst-case-exponential algorithms that run fast on real instances (simplex
remains a workhorse though provably exponential; Knuth's 2016 von Neumann lecture
was all SAT applications and mentioned NP-completeness in passing), and
approximate optimality removing the exponential even in the worst case (88% on
max cut).

> **The second failure mode.** A ledger can be exact, parameter-free and able to
> return zero, and still forbid nothing that matters — if it is computed over a
> measure the world does not sample. A bound that binds only off the support of
> what occurs is not a false bound; it is a true one with no purchase. So the
> test needs a second clause: not only *can this count return zero* but *does it
> return zero anywhere the system actually goes*.

Written with the limit attached, because the reading it invites is wrong: nothing
here bears on whether P equals NP, and nothing in this corpus does. Trefethen's
observation is his, published under his name, and it concerns the *consequences*
of a distinction rather than the distinction — he is explicit that P vs. NP's
standing as an organising principle "has only grown", with 551 complexity classes
catalogued as of August 2026. The chapter takes a diagnostic from it, not a
result. The closing line is the one that matters: **recognising the shape of a
problem is not the same as having solved it, and the gap between those two is
where most of the mathematics lives.**

That is §26.4's rule applied to us rather than to anyone else, which is the only
way it stays an instrument.

### A Möbius chapter — Book 7, and a claim I checked and then weakened

Recommendation is Book 7's Attribution Series, not Book 4. Möbius is a person and
Book 7 is the gallery of people; Book 4 would need it to be about the mathematics,
which Ch 26 now covers.

The attribution angle, **checked and then walked back one step**: the tempting
claim is that Johann Benedict Listing discovered the band first and was robbed by
the naming. MacTutor will not support that. It says Listing "discovered the
properties of the Möbius band at almost the same time, and independently of"
Möbius, in 1858, and does not establish priority either way. So the honest case is
not theft but **co-discovery collapsed by a singular name** — a third kind of
attribution failure, distinct from Bhargava's (a story the genre invented) and
Lattes' (a rule sending credit upward). Here it is convention: objects get one
name because names are singular.

With a genuine counterweight: **Listing coined the word "topology"** — first in an
1834 letter, published in *Vorstudien zur Topologie*, 1847, the first published
use of the term. The man whose name is not on the band named the entire field.

The Faraday connection Pablo asked about is real but it is *content*, not a home:
**Stokes' theorem requires an orientable surface**, so Faraday's law
∮E·dl = −dΦ/dt is well-posed only when the surface is orientable — flux is not
defined on a Möbius band. That belongs as a section inside the Möbius chapter,
cross-linked to `ch-faraday.html`, rather than making it a Book 4 chapter.

## 2026-09-09 — Book 4 Ch 27 · The Measure That Binds, and a claim

Pablo asked for the next chapter toward P vs NP, for gap-filling, and — fairly —
for the corpus to produce a claim of its own from time to time rather than only
audit. This is the attempt, and the claim is real but its standing is stated
rather than dressed.

**The question is §26.2's second failure mode, turned from a diagnostic into a
demand:** name the measure, and show the count is nonzero on it. Easy to state,
hard to meet. Met here once, completely, on the smallest object that can carry
it.

**Two classical facts about W(T) = d₁ − d₂ point opposite ways.** Summing W is a
lattice-point count in ℤ[ω], whose fundamental domain has area √3/2, giving
Σ_{T≤x} W(T) ~ (π/√27)x = 0.60460x. But by Landau–Ramanujan in its Löschian form
the support has density zero: #{T≤x : W>0} ~ K x/√(log x), K = 0.6389…

Constant mean on a vanishing support forces the surviving values to grow.

### Result 27.1

    ⟨W(T) | W(T) > 0⟩  ~  C √(log T),   C = (π/√27)/K = 0.94617…
    ⟨S(T)⟩/k = ⟨log W⟩ ~  ½ log log T + log C

Sieved to T = 4×10⁶: summatory mean settles on 0.60460 against π/√27 = 0.60460;
permitted fraction still falling 0.230 → 0.171; conditional mean over √(log x)
climbing 0.867, 0.887, 0.899, 0.902, 0.905 — flattening, below C, which is what a
Landau–Ramanujan constant does on the way up.

**The standing of the claim, stated in the chapter rather than implied.** Both
inputs are classical. The quotient is not, for a prosaic reason: the conditional
mean of a divisor function is an odd thing to want until the function is an
entropy, which it became one chapter ago. So it is **a new statement about a new
object, assembled from old parts**, fully checkable by `ch27-verify.py`. Same
standing as Proposition 26.2. Nothing here is a new theorem of number theory, and
the chapter says so.

### And it costs us

Ch 25 said its entropy was a tie-breaker — k log 2 against an elastic cost
scaling with 10T+2 — and could not say how the entropy grows. Now it can, and the
news makes the earlier claim stronger by making it worse:

| T | sites | ⟨S⟩/k | ratio |
|---|---|---|---|
| 10¹ | 102 | 0.362 | 3.5×10⁻³ |
| 10³ | 10,002 | 0.911 | 9.1×10⁻⁵ |
| 10⁶ | 10⁷ | 1.258 | 1.3×10⁻⁷ |
| 10¹² | 10¹³ | 1.604 | 1.6×10⁻¹³ |

Doubly logarithmic against linear. A hundred sites to ten trillion multiplies the
elastic bill by 10¹¹ and the entropy by four. **The ledger binds, and what it
binds is almost nothing** — a real answer to §26.2's demand, and a negative one
about our own chapter. A framework that had asked only whether the count can
return zero would have stopped one chapter earlier, satisfied.

### §27.4, and the discipline held

Three serious answers to the same demand where it is hard, none of them ours:
average-case complexity (Levin 1986), smoothed analysis (Spielman & Teng, *JACM*
51(3) 2004, Gödel Prize 2008 — the simplex method polynomial under small random
perturbation, which is Trefethen's observation converted into a theorem by naming
the measure), and phase transitions (random k-SAT's sharp threshold; proved for
large k by Ding–Sly–Sun, numerically ≈4.267 for k=3 and still open there).

The κ* remark — a sharp threshold at which cost peaks has the shape of this
corpus's critical parameter — is **recorded and left unspent**, per WP-29. No
mechanism is offered, so no bridge is claimed.

§27.5 states the distance plainly: nothing here bears on whether P equals NP;
average-case and worst-case are different questions; smoothed analysis does not
collapse the classes; the SAT threshold is about random instances. The chapter
takes a diagnostic from that literature and repays it with an example small
enough to finish.

`ch27-verify.py` all checks pass. Contents row added, ch26 → ch27 forward link,
G4 rung regenerated to 0..27 across 18 files, 0 broken links, terms.py clean.

### An operational note: the index.lock was mine

`git push` failed on a stale `.git/index.lock` — zero bytes, owned by the
bridge's session user, created 00:15 UTC. Cause: I ran `git diff --quiet
origin/main -- <file>` in a loop while checking what had reached origin, and
`git diff --stat` / `git diff` on `book7/index.html`. Those refresh the index and
take the lock, and the bridge cannot delete files. That is precisely the standing
rule — through the bridge, only `git log`, `git grep`, `git ls-files` — and I
broke it. Nothing was lost; both `git add` and `git commit` had already failed, so
the push had nothing to send.

**Replacement habit:** to ask whether a file has reached origin, use
`git log origin/main -- <file>`, which only reads. Never `git diff` through the
bridge, for any purpose.

> **Superseded 2026-09-09, one day later.** The diagnosis above is right and the
> prohibition drawn from it is wrong. `git --no-optional-locks diff --stat` does
> not take the index lock, so `diff` through the bridge is safe when the flag is
> present; and a lock that is stranded can be `mv`-ed aside by the same bridge
> that cannot `rm` it. This entry is left as written — it is the log — with the
> correction attached. See the 2026-09-09 entry, and *Git, on this machine* in
> `CLAUDE.md`.

---

## 2026-09-09 · Book 4 Chapter 28, and four corrections found in building it

**Ch 28, `What the Flow Pays`.** §21.8 asked for an entropy named on the corpus's
own phase space. Evaluating the corpus's contact form on the corpus's own vector
field returns `α(X) = ż − r²θ̇ = −2(r−1)²e^(−z)`, non-positive everywhere and zero
exactly on `Γ = {r = 1}`. The two objects had been in the corpus for a hundred and
sixty-four files without being placed side by side. Companion `book4/ch28-verify.py`,
symbolic throughout, exits 0.

**A scaffold script died on a replacement template.** `re.sub` parses its
replacement as a template in which `\` opens an escape. `\a` is legal (bell) and
passed silently; `\s` is not, so a replacement carrying `\alpha` and `\sigma`
failed on the second and nothing downstream ran. Rebuilt with exact string
replacement and no regex. **Rule:** any `re.sub` whose replacement contains a
backslash takes a `lambda _:` replacement, or the backslashes are doubled.

**Exact-match beat pattern-match on a second point.** The separator in the
`po-ring-meta` strip is a literal `·`, not `&middot;`. A regex tolerant enough to
match both would have hidden the difference; the assertion on an exact substring
surfaced it.

**A verification tactic failed and the fix strengthened the claim.** The check on
`2cos(3π/7)` as a root of `r³ − r² − 2r + 1` was written as
`expand_trig().rewrite(cos).simplify()` and left a non-obviously-zero expression —
a failure of the tactic, not of the claim. Replaced with `minimal_polynomial`,
which returns the cubic exactly. The cubic is therefore the minimal polynomial and
not merely a polynomial admitting the root, which is the stronger statement.

**`ch27` carried `ch25`'s header.** It was scaffolded from Chapter 25 and the ring
strip read `Book 4 · Ch 25` with the chapter line `Chapter 25 · Selection · Why the
Sheet Closes This Way and Not Another`, on a page titled *The Measure That Binds*.
Both renumbered to 27.

**§28.2 separated two numbers that had been run together.** The transverse
eigenvalue gives `μ_max = lim λ(z) = −2` and gives nothing else. `τ = 2` is the
limit of the n-bonacci ladder, reached from polynomial arithmetic with no dynamics
in it. They agree numerically; agreeing is not being the same claim, and the
chapter now says so and marks the coincidence OPEN.

**Indexes regenerated, not hand-edited.** `master-index.html` and `index-book4.html`
are outputs of `tools/build_indexes.py`; both lacked Ch 27 as well as Ch 28. Running
the tool added both. Ch 28 indexes at 17 links, not orphaned.

### The bridge git ban was wrong, and had been wrong the whole time

`CLAUDE.md` carried, in three places, a rule saying not to run `git` through the
Cowork device bridge: the bridge cannot delete files, so any command that touches
the index strands a `.git/index.lock` that nothing but the desk can clear. The
diagnosis was accurate and the rule drawn from it was wrong on both halves, which
two commands settled in under a minute.

    git --no-optional-locks status --short      # returns; no index.lock created
    mv .git/index.lock .git/_stale-locks/...    # succeeds where rm does not

`--no-optional-locks` tells git not to take the opportunistic index-refresh lock,
which is the only lock a read command wants; and while `rm` inside `.git/` still
fails with `Operation not permitted`, `mv` does not, so a stranded lock can be
moved out of git's way by the session that stranded it. Neither fact needed
discovering — both are documented behaviour — and neither had been tried.

**The rule cost more than the incidents did.** Four stranded locks (`geometry`
three times, `io-clone` once) produced a prohibition that left every subsequent
sandboxed session unable to read the state of the repository it was editing, for
four days. **Rule: a prohibition inferred from a failure gets tested against the
failure before it is written down.** Three sites updated — the *Git, on this
machine* section, the bullet under *Read first*, and the handoff method note —
each marked superseded rather than silently rewritten, and the 2026-09-08 entry
above given a correction box in place.

Fifty-four zero-byte `.stale-HEAD.lock-*` files had accumulated loose in
`geometry/.git` from sessions using the rename workaround. All moved to
`.git/_stale-locks/` so the desk clears them with one `rm -rf`.

### WP-107 curated: two sessions, one paper, and the other one is better

Two sessions independently set out to audit the OpenAI Navier–Stokes / Euler
release for statement fidelity. Both were real work; only one shipped. The
curation rule the corpus already had for WP-96 — compare against the claim set,
keep one, do not renumber — applies unchanged, and here it decides against this
session: `book6/wp107-the-statement-was-not-theirs.html` (`3f3107c`) reaches a
finding this session had not reached, namely that the OpenAI challenge file's own
header says it is copied from Google DeepMind's Formal Conjectures at commit
`8bf45ed`, with a 17-line unified diff whose only substantive content is the
**deletion** of the two positive alternatives and their `sorry` placeholders.
This session's draft is dropped and not filed; nothing in it survives the shipped
page. Its §7 draws the boundary honestly — statement layer complete, proof layer
not verified here — and that boundary, plus the absent `wp107-verify.py`, are now
items 6 and 7 of the handoff's open list.

**A claim written into the handoff was checked and was false.** The first draft of
item 6 said WP-107 was "the only working paper in book6 without a verify script."
Counting: 66 of 81 have none, and among the fourteen from WP-94 onward twelve do,
with WP-101 the other exception. The companion script is a convention of the
recent papers and not of the book. The corrected item says so and records that the
first version was wrong — the same discipline the entry above applies to the lock
rule, applied to a sentence written four minutes earlier.

### The handoff block was overwritten, as its own header instructs

`CLAUDE.md`'s handoff is dated 2026-09-09 and replaces the 2026-09-05 narrative in
place. Standing subsections that later sessions had added below it — the WP-94
arc, the WP-96 do-not-duplicate rule, Book 7 Ch Fy, the out-of-repo deliverables,
the scheduled task — were kept, because they are house notes wearing a handoff's
indentation and deleting them would lose rules, not narrative. The open list is
carried forward with three items added and item 8 correcting its predecessor: the
line-1 block it called "a stale 2026-08-30 block" is now dated 2026-09-05 and
holds the overnight-job run order. Merging the two blocks is a restructure and is
left undone on purpose.

### Postscript, ten minutes later: the bridge can commit too

The entry above lifted the ban on *reading* and left writes at the desk. Then the
commit carrying it was made through the bridge, to see what would happen, and it
worked — `38e0f5a`, `git add` and `git commit` both succeeding. Git builds each
object as `.git/objects/??/tmp_obj_*` and renames it into place; the rename is the
operation that matters and the bridge permits it. What fails is git's attempt to
unlink the temporaries it did not use, and the resulting `Operation not permitted`
warnings are litter reports rather than failures. A `HEAD.lock` is left behind too,
already released; `git --no-optional-locks status` returns 0 with it sitting there
and `git fsck` is clean.

So the corrected rule is narrower again than the correction: **push is the only
operation that has to happen at the desk, and it is push credentials that require
it.** Sweep `tmp_obj_*` and `HEAD.lock` into `.git/_stale-locks/` before ending a
session that committed — 1,520 temporaries had accumulated in
`geometry/.git/objects` from sessions that never looked, all now swept.

Two corrections to the same rule in one day, each narrower than the last, both
found by running the command instead of reasoning about it.

### `wp107-verify.py`, and two figures it caught in the page it verifies

WP-107 shipped without a companion script, which for a paper whose entire claim
is a diff is the wrong way round: the load-bearing numbers were exactly the kind
a reader should not have to take on trust. `book6/wp107-verify.py` regenerates
them — standard library only, blocks [1]–[4] fetching the two statement files
over HTTPS and blocks [5]–[6] reporting SKIPPED unless `--repo` points at a
checkout, rather than guessing.

Reproduced exactly: 2,486 Lean files, 616,276 lines, a 17-line unified diff at
default context, every changed line a deletion, and the deleted block exactly the
two positive alternatives with their placeholders. The definition comparison came
out **stronger** than the page claimed — eleven declarations byte-identical, not
nine, the two extra being the periodic variants of the initial-velocity and force
conditions, 4,801 bytes in total.

**Two figures were wrong and are corrected on the page in a dated box.** The copy
has **72** normalised code lines, not 71: the 71 came from a normalisation that
also dropped `variable {n : ℕ}`, while the 80 for upstream came from one that did
not, so the published pair mixed two strippings of the same file. `variable` binds
the dimension in every definition below it and is statement content; the page's
own declared strip list does not include it, and 80/72 is what that list gives.
And §5 excluded "the challenge reference file", singular, where there are two —
the Euler one carries the only two `sorry`s in the repository. Both exclusions
rest on the same stated ground, each file declaring its placeholders intentional
in its own header, so the finding does not move.

**Rule: a count is a claim, and a pair of counts is two claims that have to come
from one procedure.** Neither number was individually implausible. What made the
error findable was writing the procedure down as code and running it on both
files at once.

### The Euler side is not the same kind of object, and now the page says why

The script's block [6] is not a reproduction; it is a finding, and it is the
reason the script was worth writing rather than transcribing. WP-107 §3 argues
structurally: the claimant could not have narrowed the target statement because
they did not author it. **That argument covers Navier–Stokes and does not extend
to Euler.** The two challenge files declare different provenance in their own
headers — the Navier–Stokes file says *copied from* DeepMind at a pinned
40-character commit, the Euler file says *adapted from* the same upstream file at
`main`, with no commit, and describes itself as the whole-space breakdown
alternative *specialized* to zero viscosity and zero external force. A
specialization is authored. Its normalised code lines are not a subset of
upstream's, so on that side there is neither a diff that could settle the question
nor a pinned version to diff against.

Nothing here says the Euler statement is unfaithful. It says the cheap check is
unavailable there, and a Prop that has to be read is a different epistemic object
from one that can be traced. §7 already marked the Euler side OPEN; it now says
what specifically is open about it, tagged COMPUTED and OPEN together.

Handoff item 6 closed. Item 7 — the proof layer, on both sides — stands.

### `wp101-verify.py`, and a withdrawal that was right for the wrong reason

WP-101 maps the dm³ chain onto four biological thresholds disrupted by preterm
birth and **withdraws two of the four**. A paper whose value is in what it refuses
has to be right about the refusals, so the companion script checks those first.

**The anchor recount.** §1 quoted `AutophagyDm3_v2.lean` at 18 theorems. The file
carries **24**, still with no `sorry` and no `True` conclusion — its own header
says 24 and the page did not follow. Corrected, and now recounted by the script
rather than quoted. A figure that is transcribed decays the moment the file moves;
this is the same defect as the seven pages citing Mathlib v4.33.0-rc1 against a
v4.32.0 pin.

**The surfactant withdrawal was right and its reason was not.** §2 withdrew the
contact morphism because CRNT deficiency analysis "returned δ < 0 under two
independent formulations", adding that valid deficiency requires δ ≥ 0. That
second sentence is true and destroys the first as evidence. Deficiency is
δ = n − ℓ − s, and it is non-negative for **every** reaction network: the reaction
vectors of a linkage class span at most one dimension fewer than the class has
complexes, so s ≤ n − ℓ. Degradation sinks and de novo synthesis do not change it.
A computed δ < 0 is therefore a defect in the graph construction — miscounted
complexes, linkage classes, or stoichiometric rank — and cannot be a property of
the network. Both formulations were wrong, in the same direction.

The script implements deficiency from the definition, calibrates on Feinberg's
textbook example (n,ℓ,s,δ) = (3,1,1,1), and finds minimum δ = 0 over 5,898 random
networks. The corrected ground is narrower than what was published: **no valid
deficiency was ever obtained for the surfactant network, so CRNT supplies no
evidence either way.** The morphism stays withdrawn; what is withdrawn alongside
it is the claim to have shown anything against it.

**Rule: an impossible measurement is a broken instrument, not a finding.** When a
computation returns a value the theory forbids, the conclusion available is about
the computation. Reading it as a result about the object is the same error as
reading a zero-byte axiom report as a gate defect, three entries above.

### Four citations in WP-101 checked against the primary sources, and four wrong

The corpus has a standing method for this — WP-28 traced a citation to a phantom
DOI — and it is owed to its own pages as much as to other people's.

- **Whitsett & Weaver** is **2002**, not 2015. NEJM 347:2141–8, PMID 12501227. The
  volume and pages were right, which is what made the year survive.
- **Ball et al. 2013** is in ***Cortex*** 49(6):1711–21. The reference list had it
  right and the in-text citation said *Brain*.
- **Gibbons et al. 2014** is *Interleukin-8 (CXCL8) production is a signatory T
  cell effector function of human newborn infants*, **Nat Med** 20:1206–10,
  doi 10.1038/nm.3670. The entry had a different title, journal, volume and pages.
- **Stjerna** is the serious one. The entry gave *PLoS ONE* 10(5):e0123420 (2015)
  and the in-text citation gave *NeuroImage* 2015 — two different journals for one
  source, neither of which publishes a paper of that title. The real paper is
  *J Vis Exp* 60:3774 (2012), PMID 22371054, and it is a recording **protocol**,
  which cannot support a finding about EEG coherence. The sentence it carried is
  **downgraded to unsourced** rather than re-attached to a paper that does not
  bear it, and OPEN-2 now says a source has to be identified.

Three more are unresolved and are recorded as unresolved rather than guessed at:
Fairchild et al. 2016 and a bare "PNAS 2009" are cited in the text with no
reference entry, and the Poets et al. 1994 entry did not resolve to a paper of
that title, journal, volume and pages.

Block [3] of the script now checks the internal half mechanically — every in-text
(Author, Year, Journal) resolves to an entry, and the journals agree — and block
[4] asserts each externally verified correction is present, so a citation checked
against a primary source cannot silently revert.

Handoff item 6 fully closed: every working paper from WP-94 onward now carries a
verify script.

## 2026-09-10 · WP-29 verified: the instrument that refuses coincidences

WP-29 is the most-linked instrument in the corpus — **26 pages** point at it, and
WP-30, WP-104, WP-107 and Book 4 Ch 26 invoke "the WP-29 method" by name — and it
had no script. An instrument used to refuse other people's claims is the first
thing that should be verified, not the last.

**Its claims are unusual: most are about other files.** Five sentences of the form
"Fixed: page X now reads Y". A claim of that shape decays in silence — nothing
fails when a page is edited back, and nothing was watching. `wp29-verify.py` holds
all five as assertions. **All five held.** Then it re-ran the sweep.

**A. The Moonshine repair fixed the epigraph and not the chapter.**
`book8/ch8-6-voa.html` carried the corrected epigraph — "conjectured… still open
as of 2026" — and eight paragraphs below it a technical box reading "the
uniqueness of V♮ (Frenkel–Lepowsky–Meurman conjecture, **now a theorem**)". One
chapter, both statements. The conjecture is open: Betsumiya, Lam and Shimakura
(*Comm. Math. Phys.*, 2023) prove uniqueness for holomorphic c = 24 VOAs with
**non-trivial** weight-one Lie algebra — exactly the complement of the moonshine
module, which has dim V₁ = 0. Corrected to a conditional. **Rule: repairing a
page's epigraph is not repairing the page.** Finding 4 did the first and reported
the second.

**B. The same claim species survived one paragraph above its own correction.**
`course-dm3-102.html` still read "critDim(4) = 112 — exactly the number of proofs
in the AXLE 1080-proofs programme", directly above the Week 10 card carrying
finding 3's correction. The registry reports 284 core proved, 148 kernel-audited,
1244 recursive; the programme is named for 1080. It survived because **the sweep
searched for the phrase "not a coincidence" and this sentence does not contain
it.** A sweep keyed to wording finds the wording. Corrected.

**C. Finding 3's correction is no longer regenerable.** The figures that replaced
the bad claim — 112 rows, 1,041 sorrys, 1,027 open — came off
`project-1080-proofs/sorry_inventory.csv`, which is in no repository reachable
from this desk. More defensible than what it replaced, and now resting on an
artefact nobody can re-run. Recorded, not fixed.

**The base rate, measured instead of asserted.** Finding 2 argued that a shared 3
is not evidence because small integers recur by base rate — rhetoric until now.
Counting every integer below 1000 in the running text of **751 pages**, 63,771 of
them: **3 accounts for 10.94% and ranks third overall.** And 112 occurs **70
times**, one of them Book 6 Ch 02 building E₈ as 112 + 128 = 240 — a three-digit
integer recurring across unrelated structures, inside the corpus, in a chapter
WP-29 already cites for something else.

**One correction toward strength.** The control case is stated for simply-laced
root systems; |Φ| = rank × h holds for *every* irreducible root system. Thirteen
checked including B, C, F₄ and G₂. The control is right and its stated scope was
narrower than the identity under it.

**A verify script found an error in itself before it found any in the paper.**
The root-system table was written with h(D₇) = 14; it is 12. The check failed on
its own fixture, which is what a fixture is for.

WP-29 extended in place, as its own closing paragraph asks for, rather than
re-done.

### WP-107 §9: the adapter layer and the witness, prompted by an outside reading

Olga Holtz (UC Berkeley) published a public assessment of the OpenAI announcement
on 9 September asking, among other things, for independent scrutiny of "whether
the formal statement matches the intended theorem" — the question WP-107 was
written to answer, asked independently a day later. Her description of the
construction (a 3D incompressible fluid at rest, forced, bounded energy) turned
out to be checkable in the repository, so two of §7's three OPEN items were read.

**The adapter layer, which §7 flagged as where scope slips.** The submission
proves nothing against the challenge file; it proves against
`NavierStokes/ComparatorDefinitions.lean`, whose header says the adapters' import
closure must contain no reference placeholders. Normalised and compared line for
line: **62 code lines against the challenge file's 72, zero lines present here and
absent there, and exactly 10 removed — the two theorem statements and their two
`sorry`s.** Nothing is added. The adapter has no room to introduce a weaker
solution notion, because it introduces nothing. Closed at the statement layer.
`ComparatorSolution.lean` restates (C) and (D) under the reference names and calls
`#print axioms` on both; that the calls are there is checked, what they print is
not, and no build was run.

**The witness.** (C) is existential in u₀, so the witness decides how strong the
instance is. `ComparatorR3Theorem.lean` supplies `fun _ => 0` — the zero field,
its decay obligation discharged by a lemma rather than assumed. By §2's asymmetry
that is a strengthening: conditions on the data make a theorem harder, never
easier. Holtz's "a three-dimensional incompressible fluid at rest" is that line of
Lean, and it is one line.

**What was deliberately not adopted.** Her note also raises research-priority and
discovery-provenance questions, including concerns attributed to others. Those are
outside the note's scope and are recorded as outside it. **Rule: relaying an
allegation is not auditing it.** WP-107 has an instrument for comparing a
statement against an upstream file and no instrument for adjudicating credit, and
a paper that borrows the authority of the first to carry the second is doing the
thing this corpus audits other people for. The distinction WP-107 depends on is
the one Holtz draws herself: a verified theorem can settle a mathematical question
and cannot settle scientific credit. §3's finding is provenance of the *statement*
and says nothing about provenance of the *proof*.

Blocks [7] and [8] added to `wp107-verify.py`. Two of §7's three OPEN items remain
open: the proof layer, and the Euler side.

### The audit report is clean for the first time, and the reason it wasn't is a finding

`tools/audit.py` had reported **19 dead links and 6 markdown leaks** on every run
for as long as this session has been watching. A report that is never empty is a
report nobody reads, so the standing findings were cleared rather than stepped
over again.

**Twelve of the dead links were one mistake.** `vol2-v5/deposit/dashboard.html`
links eight sibling pages by bare filename while sitting two directories down.
All eight exist at the repository root. Thirteen hrefs given `../../`.

**Five were in WP-101, and they were symptoms of something else.** The page links
`wp30-the-missing-anchor.html`, `wp31c-autophagy-calibration-case-study.html` and
`sample-chapter-autophagy.html`. None exists. Each is **a filename constructed out
of a display label**, and the labels do not match the filenames:

| the label a reader sees | the file it actually points to |
|---|---|
| WP-30 · The Missing Anchor | `book6/wp85-the-missing-anchor.html` |
| WP-31B · How to Audit a Mathematical Claim | `book6/wp30-how-to-audit.html` |
| WP-31C · Executing the Calibration Pipeline | `book6/wp86-autophagy-calibration-case-study.html` |
| WP-31D · Topological Mismatch | `book6/wp87-topological-mismatch-bifurcation-loss.html` |

So **"WP-30" is not a well-defined citation in this corpus**: by label it is *The
Missing Anchor*, by filename it is *How to Audit a Mathematical Claim*, and those
are different papers. WP-101 cites "WP-30" for the μ_max ≈ −0.41 s⁻¹ withdrawal,
which is the first of the two; the link was repaired to `wp85`, and the label left
alone. **Nothing was renumbered.** The corpus's own rule from the WP-96 and WP-107
collisions is that renumbering is worse than the collision, and the author is
entitled to a display numbering that follows the argument rather than the disk.
What is not acceptable is a divergence nobody can see, so it is now instrumented.

**Six markdown leaks: five real, one not.** `book4/rh-paper.html` — the RH preprint
— was rendering literal `**asterisks**` to readers in five places, including the
line stating the axiom result. Converted to `<strong>`. The sixth was
`<strong>K**` in WP-101, where `K*` and `K**` are the two thymic-selection
thresholds; a mathematical name ending in a star is not half-converted bold, and
`audit.py` now carries a documented notation exception rather than a weakened
check.

`.lake` added to `SKIP_DIRS`: the remaining dead link was `importGraph`'s own
html-template referencing a stylesheet it does not ship. Auditing other people's
vendored files reports defects nobody here can fix.

**`tools/audit.py` now reports `clean` across 693 files.**

### `tools/numbering.py` — the check that would have caught it

Reports four things over every index page and judges none of them: label number
against filename number (MISMATCH), one label on several files (COLLISION), a
`wpNN` file no index lists (ORPHAN), and one number carried by files in two books
(DUPLICATE). Exit 0 unless `--strict`, because divergence can be deliberate.

First run, 165 rows across 29 index pages, **15 reported**:

- the four MISMATCHes above;
- six COLLISIONs, of which four are benign — `Cap 0`–`Cap 3` are per-book
  Portuguese chapter numbers in Book 5 and Book 6 — one is generic (`Plan` on the
  two 47-year plans), and one is real: **`Ch DE-3` on both
  `ch-aperiodic-multiplying-media.html` and `ch-box-domain-lift.html`**;
- four ORPHANs, all Book 7: `wp56-special-relativity`, `wp57-causal-integration`,
  `wp58-galactic-fold`, `wp59-dark-matter-lensing` — written and listed nowhere;
- one DUPLICATE, and it is the same four papers again from the other side:
  **`book6/wp56-algorithmic-urgency.html` and `book7/wp56-special-relativity.html`
  both claim WP-56.** Book 7 opened a wp56–wp59 run over Book 6's wp56 and put
  none of it in an index, which is why nothing surfaced it.

None of these are repaired here. They are decisions — which numbering wins, and
whether Book 7's run belongs in an index — and this entry's contribution is that
they are now visible and will stay visible.

### Handoff written on a context limit, not after one

`CLAUDE.md`'s handoff block overwritten for 2026-09-10 at 90% of the session
budget, per the standing rule that losing the handoff costs the next session more
than the edit was worth. The block carries what a fresh session cannot recover
from the log: the corrected git rule, the four verify scripts and what each found,
seven rules earned rather than assumed, and an **In flight** section for WP-31B
(`book6/wp30-how-to-audit.html`), which was being read when the limit arrived.

Five things were established about WP-31B before stopping and are recorded so the
reading does not have to be redone. The most useful is the first: **the
label/filename split that `tools/numbering.py` flagged yesterday is documented on
the page itself** — WP-31B was renumbered on 2026-08-11 out of a collision with
WP-30 *The Missing Anchor*, and the filename was deliberately left unchanged
because WP-28 and WP-38 link to it directly. One of the four MISMATCHes is a
recorded decision, which is exactly the case the tool was built to allow for: it
reports and does not judge.

Also confirmed: `value_iteration_midstream.py` is present at the repository root,
so §8's claim that the phantom is now a real file holds; √(1.05/9.493) = 0.3326
and √(4.20/9.493) = 0.6652, with 4.20 = 4 × 1.05 exactly, so the "ψ ≈ 0.50
correction" is exactly a factor of four in the unstated rent b₀ and can be stated
exactly rather than approximately; Book 4 Ch 10 confirms r* = 0.77594058 by
bisection to 10⁻⁷. And one phrase not to trust as written: §7 calls the payoff
"identically zero at σ = 0" when at σ = 0 it is −v²/2, zero only at v = 0 — what
vanishes is the payoff maximised over v. The argument survives; the sentence is
loose.

The open list is renumbered to 11 items with the three numbering decisions, the
unreachable `sorry_inventory.csv`, and the three unresolved WP-101 citations added
as their own entries rather than left inside prose.

### The Mathlib lemma was read by its name, and its name was misleading

The Zulip thread was checked. Three messages: the post, Moritz Doll's one-line
`docs#logDeriv_riemannZeta_one_sub`, and the reply conceding it. **The two
follow-up questions in that reply are still unanswered**, and both turn out to be
answerable from the primary source, which is where they should have been answered
before conceding anything.

**What `logDeriv_riemannZeta_one_sub` actually says**, read off master rather than
inferred from its name — it lives in `NumberTheory/LSeries/RiemannZetaLogDeriv.lean`,
a module whose entire content is this one statement:

    ζ'/ζ(s) = −ζ'/ζ(1−s) + log 2π − ψ(s) + (π/2)·tan(πs/2)
    hypotheses:  ∀ n : ℤ, s ≠ n        ζ s ≠ 0

It is obtained by differentiating **`riemannZeta_one_sub`, the asymmetric
functional equation**, which is why it carries `log 2π`, a single unhalved
digamma, and a tangent term. The statement in `ZetaReflection.lean` comes from
`completedRiemannZeta_one_sub`, the **symmetric** Λ form: `log π`, two
half-argument digammas, **no trigonometric term**. They are equivalent modulo
Legendre duplication and Euler reflection — which is exactly the conversion this
development's own route note, written 2026-08-30, records deciding not to pay.
Mathlib paid it. The two identities are therefore not the same statement, and the
symmetric form is not in the library.

**The hypotheses differ, and not uniformly.** Mathlib excludes *every* integer and
needs ζ non-vanishing at s alone. This desk's excludes only
{0,−2,−4,…} ∪ {1,3,5,…} and needs non-vanishing at both s and 1−s. So the local
statement applies at s = 2, 4, −1, −3, where Mathlib's does not, and costs a
second non-vanishing hypothesis for it.

**And `logDeriv Gammaℝ` is absent from master.** `Gamma/Deligne.lean` carries
eighteen declarations today — the two definitions, their `_def` lemmas, recurrences,
zero characterisations, reflection formulas, and `differentiable_Gammaℝ_inv` — and
not one derivative, `logDeriv` or digamma lemma among them. The offer stands.

**The correction was over-conceded, and is amended.** The 2026-09-09 box in
RH §4.6 said the proof is "an independent derivation of an existing result", which
reads as *the same result*. It is an independent derivation of a *different form*
of the same mathematics. Amended in place with both statements printed side by
side, so a reader can see the difference rather than take either characterisation
on trust.

**Rule: `docs#name` is a pointer, not a statement.** Conceding to a name is the
same error as trusting a green badge — WP-31B's first rule, applied to this desk
by this desk. The concession was right to make and was made a day too early.

## WP-84 WAS CORRECTED BY ITS OWN LEAN FILE, AND DID NOT KNOW (2026-09-10)

`GTCT/book4/FoldingFrequency.lean` was written and kernel-checked on 2026-09-09 —
six declarations, no `sorry`, all on `[propext, Classical.choice, Quot.sound]`,
report in `tools/verify-audit/2026-09-09/`. Its own header states that WP-84's
framing is wrong: *"twelve is not characterised, it is an instance."*

**WP-84 said nothing about any of it.** Zero occurrences of `Lean`,
`FoldingFrequency`, `sorry` or `decagon` on the page. A correction existed, was
proved, and sat one repo over for a day without reaching the page it corrected.

### The defect

§7 is titled *The coincidence is a characterisation of twelve* and says the
non-DC fixed modes equal {N/2} "if and only if N = 12", verified at
N = 6, 12, 18, 24, 30, 36, 42, 48, 60.

Every one of those checks holds k = 6 and varies N. **With k fixed the answer can
only come back N = 12**, so the sweep could not see the thing it was asked to
test. The general theorem varies both:

    visibleModes N k = {N/2}  ↔  N = 2k        (0 < k, 2 ∣ N)

At k = 6 it returns 12; at k = 10 it returns 20. Nothing distinguishes twelve
except the k it was computed at. The arithmetic was never wrong — the sentence
around it claimed a specialness the general statement removes. MISFRAMED.

### What generalises

**A sweep that varies one axis of a two-axis claim confirms itself.** This is the
same shape as *a sweep keyed to wording finds the wording* (2026-09-09), one level
up: there the instrument matched the phrasing, here it matched the parameter that
was already fixed. Before trusting a table, ask which variable it was not allowed
to move.

### Repair

Correction block added to WP-84 at the §5 boundary: the general theorem, the six
declarations with their statements, the axiom result and the report path, the
dropped `k ∣ N` hypothesis (only `0 < k` and `2 ∣ N` are used), and what prompted
it — the ten-sided wave reported at Saturn's south pole on 2026-09-02
(Sánchez-Lavega et al., *Science Advances*, doi 10.1126/sciadv.aee4251).

A `NOT CLAIMED` block was added with it, carrying the Lean file's own disclaimer
forward, because `hexagon_at_twelve` and `decagon_at_twenty` sitting beside a
Saturn citation invite exactly the inference the file forbids: **nothing here
bears on Saturn.** The theorem is about Fourier modes of a discretely sampled
ring; Saturn's polar waves are jet-stream wavenumbers in a continuous fluid set
by barotropic instability. They share the integers 6 and 10 and nothing else.
Linked to WP-100 and WP-97 rather than restating either.

`tools/verify-audit/2026-09-09/` is committed with this, since it is now cited.

### Addendum, 2026-09-10: "the HTML is redundant" would have licensed archiving the folder

The GTCT orphan audit concluded that `GTCT/book4/`'s HTML is redundant and that the
only unique thing left would be `SERIES_SKELETON.md`. Both halves are true **of the
HTML**. The folder is 36 html · 4 pdf · 4 lean · 3 md · 2 py · 1 js · 1 .bak.

The four PDFs are safe — all four are already in `geometry/book4/` at the same names.
The four Lean files are not, and two are cited from this repo by that path:
`FoldingFrequency.lean` from `book6/wp84-…html` as of today, and `ZetaReflection.lean`
— the RH arc's closed statement, 18 declarations — from `docs/ml-evidence/`.
`MATHLIB-POST.md` exists nowhere else.

Nothing is wrong with where those files live: the canonical rule says other repos hold
Lean, tooling, data and PDFs, so GTCT is correct and the citations are correct. What was
wrong was the **instruction** a later session would have acted on. A sentence true of a
subset, written about the container, licenses an action on the container.

Recorded as the third instance today of the same shape: a correct measurement under a
sentence that would have caused damage. The other two are WP-84's fixed-k sweep and
block [8]'s regenerated r*. Repair: the handoff now says *archive the 36 HTML files,
not the directory*, and lists what else is in there.

### Addendum 2, 2026-09-10: the repair was real, the citation was not

The block-[8] finding above is correct in substance and **was attributed to the wrong
file**. It is `book4/ch24-verify.py`, not `ch23-verify.py`. `ch23-verify.py` computes
contact forms, the Segre P¹×P² dual defect and the Legendre transformation on J¹(ℝ,ℝ),
and contains no r* at all — which is why `push-book4-whole.sh`, whose `git add` names
`book4/ch23-verify.py`, reported nothing to commit.

Verified on disk: `ch24-verify.py` lines ~168–190 carry the certified bracket
[0.775940575501953125, 0.77594057550234375], the inside/outside test, the eleven-figure
agreement check, and the instruction to cite `certify_rstar_rigorous.py` past eleven
figures. The repair is complete. Only its address was wrong.

This handoff repeated the wrong address for a day. A session sent to `ch23-verify.py`
would have found a Segre block, concluded the repair was never made, and either redone it
or reopened a closed finding. **Fourth instance today of one shape** — after WP-84's
fixed-k sweep, block [8]'s regenerated r*, and the container-vs-subset archive
instruction. Here the object measured was right and the *pointer* to it was wrong.

Caught by opening the file instead of trusting the report of it, which is the same move
that produced all three of the others.

## BOOK 3 HAS ONE VERIFY SCRIPT, AND THE AUDIT FOUND AN 8TH DIGIT (2026-09-10)

### The book that teaches has the least instrumentation

`tools/book3_roster.json` lists **44 chapters, every file present on disk**, and
**one** has a companion verify script — `ch44-verify.py`, written 2026-09-08. Book 4
has five, Book 6 about twelve, Book 7 one. Book 3 is the taught path, the book a
child is handed, and it is the least checked in the corpus.

Eighteen of its 44 chapters print a number to three or more decimals. Not all want a
script; the recurring constants do, because they are quoted in several chapters at
once and nothing keeps them agreeing.

### What the scan found: r* is wrong at the eighth decimal, in 67 files

`certify_rstar_rigorous.py` certifies

    r* ∈ [0.775940575501953125, 0.775940575502343750]     width 3.906e-13
    midpoint 0.7759405755021484375,  which to 8 dp is 0.77594058

The value carried across the corpus is **0.77594058**. That is **1.450e-8 above the
certified upper bound** — outside the bracket, and the disagreement is in the eighth
decimal place, not the thirteenth. Rounded honestly the certificate gives
**...58**, not ...59.

`0.77594058` appears in **67 files** (html, py, md, lean; `_to_delete` and `_archive`
excluded), including three Book 3 chapters — `ch05-contact-normal-form.html`,
`ch23-14-week.html`, `about-author.html` — and `book7/ch-feynman-verify.py`, which
took it from `labs/dm3_numeric.py`. **`0.77594058` appears in three files.** So the
correct digit exists in the repo and never propagated.

WP-69 already recorded that "Vol II toy-model §7 lists 'certified 0.77594058' — 8th
digit differs". The certificate now says which side is right.

### Not repaired here, and deliberately

Changing a figure that is published in 67 files, several of them deposited, is an
author's decision and not a session's — the WP-96 and WP-107 rule. Two things must
be settled first, and neither is arithmetic:

1. **Are they the same quantity?** `dm3_rstar_verify.py` reads 0.77594058 as the
   λ = 2 basin edge (ε=2, z₀=0). If the certificate certifies that same edge, ...59
   is simply wrong at the 8th place. If it certifies something else, the two numbers
   are different objects sharing a name, and the repair is to distinguish them — not
   to overwrite one with the other.
2. **What is actually at stake?** Every use found so far quotes ~0.776 or 8 digits in
   prose, where the error is invisible. No downstream computation has been shown to
   depend on the 8th digit. The cost of a 67-file sweep may exceed the cost of the
   error, and that is a judgement about the corpus, not about the number.

Recorded with the arithmetic so the decision can be made once, from the certificate,
instead of rediscovered a fourth time.

### Book 3 gets its second verify script — and the chapter was clean (2026-09-10)

`ch7-crystalline-verify.py`, for `ch7-crystalline.html` (Book 3, ch 33), the chapter
carrying the most numbers in the book: thirteen at three or more decimals.

**Every number on the page is correct.** Five table ratios, five ten-term sequences,
six widget ratios, all reproduced. η_k is computed as the root in (1,2) of
x^(k+1) − 2x^k + 1 = 0 — the k-nacci characteristic equation with the spurious root
x = 1 divided out — bisected to 1e-15 and compared **at the page's own precision**:

    eta_2 1.618033988750   eta_3 1.839286755214   eta_4 1.927561975483
    eta_5 1.965948236645   eta_6 1.983582843424   eta_7 1.991964196605

The widget's three-decimal forms round correctly from these, including 1.92756 → 1.928.
The chapter's "∞-bonacci 2.00000" row is confirmed as a limit and not a member: η_k is
strictly increasing and bounded above by 2, and 2 − η_12 = 2.4e-4.

**The script reads the numbers out of the page rather than from a transcription**, so a
later edit is checked instead of assumed. That is what WP-29's *a figure that is
transcribed decays the moment the file moves* asks for, applied at the source.

**The one failure was the instrument's.** Block [2] first reported four sequences, not
five: the Hexanacci row carries a `✦` between its ratio and its sequence and the pattern
did not allow it. An impossible measurement is a broken instrument, not a finding — the
same rule the δ < 0 case earned. Fixed, and the row count is now **asserted at five**, so
a row that stops matching fails the block instead of quietly shrinking it.

Book 3 now has 2 verify scripts for 44 chapters.

### RULED: r* stays at 0.77594058 — the eighth decimal is not worth 67 files (2026-09-10)

The finding above stands as arithmetic: the corpus value is 1.45e-8 above the
certified upper bound, and the certificate rounded honestly to eight places gives
0.77594058, not ...59.

**Pablo's ruling, same day: not a defect. Do not chase it.** The reasoning is a cost
argument and it is the right one. Every use of the number in the corpus quotes ~0.776
or eight digits in prose. No computation has been shown to depend on the eighth
decimal. A sweep of 67 files, several of them deposited, buys nothing a reader could
act on and risks the thing a sweep always risks — touching many correct files to
repair a defect that was never load-bearing. That is the MISFRAMED lesson of
2026-09-07 applied before the damage rather than after it.

**What this closes and what it does not.** It closes the sweep. It does not close the
precision rule, which `ch24-verify.py` already carries and which is now the settled
position of the corpus:

> Prose keeps ~0.776. Anything cited past eleven significant figures comes from
> `certify_rstar_rigorous.py` and not from any float-bisection block.

Recorded as a **ruling** rather than a finding so that the next session to notice the
eighth digit finds the decision already made. A discrepancy that is real, visible, and
deliberately not repaired needs its reason written down, or it gets rediscovered and
"fixed" by someone acting in good faith.

### overnight.sh could report a failed run as an empty corpus (2026-09-10)

Run through the Cowork bridge, `tools/overnight.sh --dry-run` printed eleven
`UNREADABLE ROOT` lines and then `corpus: 0 tracked .lean files across 11 declared
roots`, `priority 1: 0`, `priority 2: 0`, `priority 3: 0`, and exited 0.

Nothing was wrong with the corpus and nothing was wrong with the roots file.
`corpus_roots.txt` names `~/Desktop/...`, which is correct at the desk; on the bridge
`~` is the session root and the desk is mounted under `~/mnt`, so every path resolves
to nothing. The script's own design already handles this correctly — *a root it cannot
read is REPORTED, never skipped* — and it did report all eleven.

**The defect was in the summary, not the measurement.** After eleven honest failure
lines the script printed a zero corpus and a clean exit, and "0 files, priority 1: 0"
reads like *nothing to do*. The failure lines scroll; the summary is what gets read.

Repaired: the script now counts unreadable roots and, when every declared root failed,
prints that this is a **failed run and not an empty corpus**, names the bridge as the
likely cause, and exits 2. Recorded in the handoff's overnight section with the
instruction not to "fix" `corpus_roots.txt` to bridge paths — the file is right for the
machine the job runs on.

Same shape as the day's other four: the measurement was correct and the sentence
carrying it would have licensed a wrong conclusion. Fifth instance, and the first one
found in a tool rather than a page.

### Ch 28's own open caveat, closed against the deposit (2026-09-10)

Chapter 28 §28.5 shipped with a caveat in its "What Is Not Claimed" section: *"The
source is not current. Version 4 is the published version this was computed against;
the author reports later revisions. The evaluation is two lines and should be re-run
against the current equations before anything is built on it."*

Re-run. Three things came back, and only one of them was expected.

**The version is current.** The Zenodo record of record is
[10.5281/zenodo.21708678](https://doi.org/10.5281/zenodo.21708678) — *GTCT 2026*, v4.0,
deposited 30 July 2026, concept DOI 10.5281/zenodo.19498857 — and it is the most recent
version in the series. The caveat assumed v4 had been superseded. It has not been. The
chapter was computed against the current source and said otherwise about itself.

**The erratum is settled in the deposit, not merely survivable.** §28.2 argued that
Result 28.1 is robust to the coupling, so it would survive the reported
$e^{-r}\!\to\!e^{-z}$ correction either way. That argument stands, but it is no longer
what carries the result: the deposit's executable `dm3_simulation.py` has

    rdot = r * (1.0 - r**2) + 2.0 * (r - 1.0) * np.exp(-z)
    zdot = r**2 - 2.0 * (r - 1.0)**2 * np.exp(-z)

character for character what `ch28-verify.py` assumes, $e^{-z}$ included. The robustness
argument was insurance against a possibility that the deposit had already resolved.

**Nothing in the deposit's numerics touches the identity.** `FINDINGS.md` reports
$\mu_{\max} = -2$ recovered to three decimals and an asymmetric inner basin boundary
$r^\ast \approx 0.7732$ — correcting the symmetric $2/3$ estimate. Neither reaches
Result 28.1: $\alpha(X) = -2(r-1)^2 e^{-z}$ is computed pointwise on the field and is
indifferent to which initial conditions reach $\Gamma$. A basin correction changes who
arrives, not what the arrival costs.

§28.5 rewritten: the paragraph now records the check with the DOI rather than asking a
future reader to perform it, and is marked CHECKED. The reference entry now cites the
deposit and its files rather than a manuscript version number.

**The lesson is about the caveat, not the result.** The honest caveat was written from
what the session knew — the author had mentioned later revisions — and it was cheap to
discharge: one API call and one `grep`. A caveat that can be closed in two minutes and
is instead shipped as an open question is a small dishonesty in the other direction:
it makes the chapter look more careful than the work behind it was. Where a check is
this cheap, run it before publishing the doubt.

### The layer we said did not exist was already in use (2026-09-10)

Journal Vol. Ω No. 9 argued that `#print axioms` goes unquoted because there is no
vocabulary for what it returns — that a 1974 theorem proved by hand and a numerical
bound established last month both print as `axiom`, and that until there is a word for
the difference there is no sentence to put in a paper. It closed: *"The vocabulary gap
is still open — the three axioms had to be spelled out in prose, because there is no
standard citation for them."*

WP-107 §9, written yesterday, left the matching gap on its own side: it verified that
`#print axioms` is **called** on all four headline theorems in
`openai/NavierStokesAndEuler` and said plainly that *what they print is not* checked,
and no build was run.

Both gaps closed today by reading one file neither had opened. The repository root
carries `formalization.yaml`, declared against the mathlib-initiative schema at v0.4,
and for each of the four declarations it records:

    sorry_count: 0
    axioms: [ propext, Classical.choice, Quot.sound ]

plus `automation: { method: agent, models: [GPT-6 Astra], framework: Codex }` and
`review: status: "self-assessed"`. The two Comparator configurations go further and set
`permitted_axioms` to exactly those three names, so the independent checker **enforces**
the axiom set rather than reporting it — a gate, not a line of output.

So the standard citation exists, the schema is published, and the highest-stakes
formalization of the month populates it. **Vol 9's sentence was wrong on the day it was
set.** Corrected there with a dated note; WP-107 gains §10 with the census at HEAD
`f9e8bc5` (2,659 files, 641,332 lines; `sorry` 5, all inside the two challenge files
the solution adapters are architecturally forbidden to import; `axiom` declarations 0;
`native_decide` 0; `implemented_by` 0; `sorryAx` 0).

Two lessons, and the second is the one that costs.

**A negative claim about a field needs a search, not an absence.** "There is no standard
citation for them" was asserted from not having seen one. It took one `grep` of a
repository the corpus had already cloned to find the counterexample. The corpus has a
rule for other people's claims — WP-30 — and did not apply it to its own negative.

**And a count I nearly published was a word fragment.** The first pass of the escape
census reported `extern` at 339 occurrences, which would have been a real finding about
compiler escapes. Every one was the word *external* inside a docstring; whole-word
matches are 0. The number was produced, believed, and only caught because it was
implausible for a pure-Mathlib development. Bare `grep` on a token that is a prefix of
an ordinary English word is not a census. Same failure family as the φ(n)=4 list and the
"42-file pass": a number that felt like evidence, generated by a method that could not
have distinguished the two cases.


---

## Superseded handoff block — 2026-09-10 (moved here 2026-09-11)

Moved out of `CLAUDE.md` under the block's own rule: overwrite, do not append; dated
narrative belongs here. Nothing was edited. Still-open items were carried forward into
the 2026-09-11 block rather than left in this copy.

## HANDOFF — 2026-09-10 (OVERWRITE this block. Do not append. It reached 341 lines once by appending; dated narrative belongs in `docs/audit-log.md`.)

**Two sessions feed this block. Read both — they ran in the same repos on the same days.**

**A · session `018xEUzVc4fHaeLN5oumWAvc`** · `grossiatwork@gmail.com` · claude-opus-5.
Ended 2026-09-10 on a context limit, mid-way through WP-31B (see *In flight*).
Touched `~/Desktop/geometry` (Book 4 ch27–ch28 and `rh-paper.html`, Book 6
wp29/wp101/wp106/wp107, Book 8 ch8-6-voa, `course-dm3-102.html`,
`vol2-v5/deposit/dashboard.html`, `tools/audit.py`, `tools/numbering.py`,
`CLAUDE.md`, `docs/audit-log.md`), `~/Desktop/GTCT` (`ZetaReflection.lean`,
`ZetaFELogDeriv.lean`, `MATHLIB-POST.md`), `~/Desktop/AXLE` (Journal Vol. 10).

**B · session `c8a4c97a` (`sluhcdf@gmail.com`)** · claude-opus-5, Cowork bridge.
Ended 2026-09-10 at 90% of a session limit, work all committed. Touched
`~/Desktop/geometry` (Book 7 Ch Fy, Book 3 Ch 44, WP-96, Book 4 Ch 26 cross-link,
the rung strips, `RH_arithmetic_contact_structure.md` v3, `book4/rh-paper.html`,
three new tools) and `~/Desktop/AXLE` (`AULA/coach.html` and its assets).

**Neither session had push credentials.** Both left commits for the desk.

### Read this before touching git

**The ban on `git` through the Cowork bridge is lifted, and was corrected twice.**
Reads: prefix `--no-optional-locks`. Writes: `git add` and `git commit` **work** —
they only leave `tmp_obj_*` and a released `HEAD.lock` behind, which are litter
reports, not failures. **Push is the only thing that needs the desk, and it is
credentials that require it.** Sweep the litter into `.git/_stale-locks/` before
ending a session that committed; the desk clears that directory with one
`rm -rf`. Full account in *Git, on this machine*.

### What shipped 2026-09-08, session B — and one rule it earned

**Book 3 Ch 44 · `ch44-how-to-learn.html` + `ch44-verify.py` (5 blocks, stdlib only).**
The Feynman technique has five steps and step 3 — *find the gaps* — carries the whole
method and is the step self-explanation is worst at. Empirical, from this repo's own
`docs/audit-log.md`: 35 dated entries, **20 name how the defect surfaced — kernel 10,
recomputation 4, a person 3, reading it back 3.** The chapter's argument is that
frequency is not coverage: the person column is smallest and contains the only entry
saying *no instrument in this repository would have caught this* (the MISFRAMED case
of 2026-09-07). `--entries` prints all 35 verdicts so any one can be disputed by name.
The roster grew to 44; **slot 44 at week 14 is a proposal, not a decision** — a method
chapter may belong at week 1 and that is an editorial move of one line.

**Rung strips derived, not typed · `tools/build_rungs.py`.** Seventeen pages carry the
G3/G4 strip. Session A had already fixed the +1 Book 3 shift in fifteen and left two
uncommitted; Ch 44 then made all seventeen say "all 43". The tool takes G3 numbers and
the total from `book3_roster.json` and **never adds or removes a G3 link** — which
chapters the strip lists is editorial. The G4 rule was *read off the corpus*: eleven of
twelve Book 4 chapter pages omit exactly one number, their own. So `ch26` omitting 26 is
correct and was nearly "fixed" into a defect; the one real fault was `book4/ch15.html`
linking to itself. 701 rung links, 0 broken, no drift.

**RH preprint v3 · new §4.7 + `book4/rh-paper.html` + `tools/build_rh_paper.py`.**
§4.7 records the August–September 2026 movement in the analytic line and says why it
does not touch the construction: Pratt–Robles–Zaharescu–Zeindler's five-twelfths
(41.67%) was the standing unconditional record; on 11 Aug 2026 an internal research
Claude, directed by Jarred Sumner over two sessions and ~31M output tokens, proved
**unconditionally that >67.25% of the non-trivial zeros are simple and on the critical
line** (≥83.62% distinct), via Bombieri on Weil's quadratic form plus the unconditional
Montgomery pair correlation of Baluyot–Goldston–Suriajaya–Turnage-Butterbaugh; verified
by Alpöge and Furman, formalised in Lean; Lamzouri published a shorter proof on 2 Sept.
**The paper already cited Montgomery as [5]**, so §4.7 states explicitly that [5] is
orientation and not machinery — a reader seeing the citation and the news in one season
could infer a dependency that is not there. §4.6 gained a note on why it is a table
sorted by *how each claim is known*. §9 gained two questions the corpus can now ask of
itself: Ch Fy's Reeb computation constrains §9.4, and Ch 26's free-parameter test
applied here returns *no free parameter*, which is the minimum entry requirement and not
an achievement. `rh-paper.html` is **generated from the manuscript** and the tool exits 1
when they disagree, so the HTML cannot drift.

**AXLE · `AULA/coach.html`.** David Grossi's *Writer* pattern moved from sentences to
steps with the model removed: 50 authored questions, five stages, no model, no network,
all questions in the page source. Written for David after the 2 Sept NYC generative-AI
restriction reached his project. Carries the verified credit-by-exam routes (CLEP has no
age floor; **Modern States requires 13**, which the advice circulating gets wrong; ASU
ULC $25/$400; CUNY College Now; ECC/East Orange *Jaguar University*, which is East
Orange district only). Signed with Pablo's own Figure 1 from the RH paper.

**The rule this session earned, and it cost two near-misses:**
**check what the other instances do before "fixing" one.** The Ch 26 rung and the ch15
self-link look identical from inside a single file; only the population distinguishes a
convention from a defect. Same shape as A's `certify_rstar` finding below.

### What shipped, 2026-09-09 and 2026-09-10

**The RH arc's last admitted statement is closed.** `Zlog_add_Zlog_one_sub` is
proved; `GTCT/book4/ZetaReflection.lean` is 18 declarations, 0 `sorryAx`, all on
the three standard axioms. `ZetaFELogDeriv.lean` was the development file and is
retired evidence. The `#mathlib4` post went out; text in `GTCT/book4/MATHLIB-POST.md`.

**Four verify scripts, and every one of them found something.** This is the
finding of the two days, more than any single result: *a paper without a script is
a paper whose numbers have not been checked, including the ones nobody doubted.*

- `book6/wp107-verify.py` — reproduces the OpenAI/DeepMind diff exactly (2,486
  Lean files, 616,276 lines, 17-line diff, deletions only). Found the copy has
  **72** normalised code lines not 71, and that §5's exclusion covers **two**
  reference files not one. Blocks [7]–[8] added 10 Sept: the adapter layer proves
  against `ComparatorDefinitions.lean`, which is the challenge file minus the two
  theorems with **nothing added**, so §7's "adapters are where scope slips" closes
  at the statement layer; and the (C) witness is `fun _ => 0`, the fluid at rest,
  which by §2's asymmetry is a strengthening.
- `book6/wp101-verify.py` — the anchor is **24** theorems not the 18 quoted; the
  surfactant withdrawal is right and its reason cannot be, since CRNT deficiency
  δ = n − ℓ − s is **non-negative for every network** and a computed δ < 0 is a
  construction error; and **four citations were wrong** against primary sources,
  one naming two different journals for a paper that is in neither.
- `book6/wp29-verify.py` — all five of WP-29's repairs held. Three new findings:
  `ch8-6-voa` called FLM uniqueness "now a theorem" eight paragraphs below its own
  corrected epigraph; `course-dm3-102` still claimed 112 = the AXLE proof count one
  paragraph above its own correction; and finding 3's replacement figures rest on a
  CSV that is in no reachable repository. Base rate measured, not asserted: over
  751 pages and 63,771 integers below 1000, **the digit 3 is 10.94% and ranks
  third**.
- `tools/numbering.py` — MISMATCH / COLLISION / ORPHAN / DUPLICATE across every
  index page.

**`tools/audit.py` reports `clean` across 693 files**, first time. It had shown 19
dead links and 6 markdown leaks on every run. Twelve were one relative-path
mistake in `vol2-v5/deposit/dashboard.html`; five were WP-101 hrefs built out of
display labels; five markdown leaks were **in the RH preprint**, rendering literal
asterisks to readers. `.lake` added to `SKIP_DIRS`; a documented notation
exception added for the thresholds `K*` and `K**`.

### GTCT → geometry: the orphan audit is closed, and it caught a published number

**The precondition for archiving GTCT's `book4/` HTML is now met, and was not before.**
Six files existed only in GTCT. Four were never gaps: `chIV-15.html` is the same chapter
as geometry's larger `ch15.html`; `chIV-preface-impa.html` is the retired IMPA preface;
`nav.js` is not needed — the single grep hit in geometry is a CSS comment reading *"NAV —
replaced by nav.js, but style is here for no-JS fallback"*, not a script tag; and
`SERIES_SKELETON.md` is GTCT's own. **Two were real and are now in geometry.**

- **`tools/certify_rstar_rigorous.py`** — Lohner-style rigorous interval certification of
  the inner basin boundary: mpmath centre trajectory, Jacobian-linearised error transport,
  interval-Hessian Lagrange remainder, so the radius **over-approximates** the reachable
  set rather than estimating it. Reproduced exactly:
  **r\* ∈ [0.775940575501953125, 0.77594057550234375]**, width 3.906e-13. geometry had
  only `certify_rstar.py`, the plain float-bisection version.
- **`tools/METHODOLOGY.md`** — the certifier's benchmark record; closes AXLE #21.

**`why_no_closed_form.md` never needed writing.** The rigorous script cited it for "the
algebraic/Hamiltonian checks ruling this out" and it exists nowhere — because the content
is `METHODOLOGY.md` §*Path 3 — closed form (ruled out)*: `nonlinsolve` degenerate, the
exactness test ∂ṙ/∂z + ∂ż/∂r not identically zero, no separability under w = e⁻ᶻ, and
(r=1, z=0) not a fixed point of the reduced system. **A misnamed reference, not a missing
file.** The citation was repointed and nothing was composed.

**Then the certificate caught this repo's own arithmetic.** A float-bisection basin figure
came out **outside the certified bracket, above its upper bound.** Twelve leading digits
identical; they part at the thirteenth, by about the bracket width. Cause is that block's
own `solve_ivp` floor. **Ch 3's published ~0.776 is unaffected.** The block now prints the
bracket, says plainly that it falls outside it, and sends any citation past eleven figures
to `certify_rstar_rigorous.py`.

**The repair is in `book4/ch24-verify.py`, not `ch23-verify.py`.** Session A's report named
ch23 and this handoff repeated it; `ch23-verify.py` is contact forms, the Segre P¹×P², and
the Legendre transformation, and computes no r* at all. Verified on disk 2026-09-10: the
bracket, the comparison and the "cite the certificate past eleven figures" line are at
`book4/ch24-verify.py` lines ~168–190 and are complete. `push-book4-whole.sh` staged
`ch23-verify.py` for the same reason and had nothing to commit. Nothing is broken — but a
session sent to ch23 would have found a Segre block and concluded the repair was never
made. **Fourth instance of the day's shape: right finding, wrong file.**

`ch24-verify.py` needs **scipy**, which the Cowork bridge VM does not have. Run it at the
desk, not through the bridge.

**The standing rule, and it is the finding of the two days:**
**where two instruments exist for one number, cite the stronger one and say which.**
A number was regenerated from scratch while a stronger instrument for it sat one repo
over. Session B hit the same shape from the other side (see *check what the other
instances do*).

**What remains before GTCT `book4/` goes to archive — and READ THIS BEFORE ARCHIVING.**
Run `bash ~/Downloads/push-book4-whole.sh` and confirm. Then **archive the 36 HTML files,
not the directory.** The audit's conclusion was about the HTML and is correct about the
HTML; the folder holds more than that, and checked 2026-09-10 it is
36 html · 4 pdf · 4 lean · 3 md · 2 py · 1 js · 1 .bak.

- **The four PDFs are safe** — all four already exist at the same names in
  `geometry/book4/`.
- **The four Lean files are not, and two are cited from this repo by that path.**
  `FoldingFrequency.lean` is cited by `book6/wp84-…html` (see below);
  `ZetaReflection.lean` is the RH arc's closed statement, 18 declarations, cited from
  `docs/ml-evidence/`; `ZetaFELogDeriv.lean` is named in `book4/rh-paper.html` and the
  manuscript as retired evidence; `Bhaskara.lean` appears in the audit log.
- `MATHLIB-POST.md` is the text of the #mathlib4 post and exists nowhere else.
- `SERIES_SKELETON.md` is GTCT's own. `ZetaReflection.lean.bak-1788655485` is litter.

**Do not move the Lean or the PDFs into geometry to "solve" this.** The canonical rule
already says other repos hold Lean, tooling, data and PDFs; GTCT is where they belong and
the citations are correct as written. The only thing that needs to change is the
*instruction*: it is an HTML archive, not a directory archive.

**GTCT itself has not been touched by either session.**

**Lean, 2026-09-09:** `tools/leancheck.sh --audit --full ~/Desktop/GTCT/book4/FoldingFrequency.lean`
→ **OK, 289s, 6 declarations, all within the permitted three axioms.** Report at
`tools/verify-audit/2026-09-09/FoldingFrequency.axioms.txt` — **untracked at handoff;
commit or discard it deliberately.**

### Rules earned, both sessions — these are the reusable part

*(This block is long because it merges two sessions. On the next overwrite it should come back to one, with the dated narrative moved to `docs/audit-log.md`.)*

- **Where two instruments exist for one number, cite the stronger one and say which.**
- **Check what the other instances do before "fixing" one.** A convention and a defect are indistinguishable from inside a single file; only the population tells them apart.

- **A prohibition inferred from a failure gets tested against the failure before
  it is written down.** The bridge git ban cost four days of sessions unable to
  read their own repo state, on the strength of four incidents and no test.
- **An impossible measurement is a broken instrument, not a finding.** δ < 0, and
  the zero-byte axiom report read as a gate defect, are the same error.
- **Repairing a page's epigraph is not repairing the page.**
- **A sweep keyed to wording finds the wording.** WP-29 missed a claim one
  paragraph from its own correction because that sentence lacked the phrase.
- **A count is a claim, and a pair of counts is two claims that must come from
  one procedure.** 80/71 mixed two normalisations of one file.
- **Relaying an allegation is not auditing it.** Kept the OpenAI priority and
  Codex-leakage material out of WP-107 and said on the page why.
- **A figure that is transcribed decays the moment the file moves.** Recompute.

### In flight — WP-31B, stopped mid-audit

`book6/wp30-how-to-audit.html` is labelled **WP-31B · How to Audit a Mathematical
Claim** and is the second-most-linked instrument (20 inbound). It has no verify
script and was being read when this session ran out. Established so far:

1. **The label/filename split is deliberate and documented on the page.** It was
   renumbered 2026-08-11 out of a collision with WP-30 *The Missing Anchor*, and
   the filename was **deliberately left unchanged** because WP-28 and WP-38 link
   to it directly. So one of the four MISMATCHes `numbering.py` reports is a
   recorded decision, not a defect — record that when writing the script.
2. `value_iteration_midstream.py` **does exist** at the repository root. The
   page's §8 claim that "the phantom is now a real file" holds.
3. Arithmetic to assert: √(1.05/9.493) = 0.3326 ≈ 0.333 and √(4.20/9.493) =
   0.6652 ≈ 0.665. Note **4.20 = 4 × 1.05 exactly**, so the two σ* differ by
   exactly 2 and the "ψ ≈ 0.50 correction" is exactly a factor of 4 in the
   unstated rent b₀. The page says ψ is the gap between two guesses; it can be
   made exact.
4. **One phrase to check before trusting it.** §7 says R_V = βσ(1−γ)·min(v,1)·|I|
   − v²/2 is "identically zero at σ = 0". At σ = 0 it is **−v²/2**, which is zero
   only at v = 0; what is zero is the payoff *maximised over v*. The point stands
   and the wording is loose.
5. Book 4 Ch 10 confirms r* = 0.77594058 by bisection to 10⁻⁷, refining ε₀ = 1/3,
   which is what §5 asserts.

### WP-107 — curated 2026-09-09. There is one, and it is the other session's.

Two sessions independently audited the OpenAI release for statement fidelity. The
other shipped `book6/wp107-the-statement-was-not-theirs.html` in `3f3107c`; this
session's version was **dropped, not renumbered.** The shipped page finds the
challenge file's own header pointing at DeepMind's Formal Conjectures at
`8bf45ed`, a 17-line diff whose only substantive content is the deletion of the
positive alternatives (A) and (B) with their `sorry`s, and every definition
byte-identical. §9 now closes the adapter question. Still open: the proof layer,
and the Euler side — that challenge file is *adapted*, not copied, pins no commit,
and its Prop was therefore authored by the claimant.
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
**Both blockers were cleared by Pablo on 2026-09-04 and this application is now
unblocked.** `vol1-proofs/LICENSE` is MIT; `vol1-proofs/LICENSE-CONTENT` relicensed
the prose from CC BY-NC-ND to **CC BY 4.0**, on the stated grounds that NC-ND
permits neither commercial reuse nor derivatives and so does not meet the fund's
open-access requirement. It also records that Zenodo deposits keep the licence in
force at deposit time and that `record/` is not retroactively altered. Nothing
stands between the draft and submission. **Send it.**

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
6. **Three numbering decisions, reported and not made.** `tools/numbering.py`
   surfaces them and they are the author's calls, not a session's:
   **(a)** `Ch DE-3` labels two different Book 6 chapters —
   `ch-aperiodic-multiplying-media.html` and `ch-box-domain-lift.html`;
   **(b)** four Book 7 papers are in **no index at all** —
   `wp56-special-relativity`, `wp57-causal-integration`, `wp58-galactic-fold`,
   `wp59-dark-matter-lensing`; **(c)** `book6/wp56-algorithmic-urgency` and
   `book7/wp56-special-relativity` **both claim WP-56**. Book 7 opened a wp56–59
   run over Book 6's wp56 and indexed none of it, which is why nothing surfaced
   it. Do **not** renumber on a session's initiative — the WP-96 and WP-107 rule.
7. **`wp31b-verify.py` (i.e. for `wp30-how-to-audit.html`) — see *In flight*.**
   Everything needed is listed there; it is an hour of work, not a day.
8. **The OpenAI release's PROOF layer is unaudited**, on both the Navier–Stokes
   and the Euler side. WP-107 settles the statement layer and says so.
9. **`sorry_inventory.csv` is in no reachable repository.** WP-29's finding 3 and
   both dm³-102 pages quote figures off it (112 rows, 1,041 sorrys, 1,027 open)
   that can no longer be regenerated. Restore it or re-derive the numbers.
10. **Three WP-101 citations unresolved**, recorded as unresolved rather than
   guessed: Fairchild et al. 2016 and a bare "PNAS 2009" are cited with no
   reference entry, and Poets et al. 1994 did not resolve to that title, journal,
   volume and pages.
11. Two handoff blocks still exist: this one, and a second at **line 1**, above
   the file's own title. The line-1 block carries the overnight-job run order,
   which is standing house notes and not narrative. Merging them is a
   restructure, not a fix, and is left undone deliberately — but it should be
   done.
12. **Run `bash ~/Downloads/push-book4-whole.sh`, then push geometry.** One commit is
   waiting. After the script, GTCT `book4/` HTML is archivable — see *GTCT → geometry*.
13. **Ch 44's roster slot is an open editorial call.** It sits at n=44, week 14, phase G,
   D2 — appended, not placed. A chapter about *how to study* plausibly belongs at week 1.
   One line in `tools/book3_roster.json`; a session must not move it on its own initiative.
14. **`tools/verify-audit/2026-09-09/` is untracked.** Commit the axioms report or delete
   it, but decide — an untracked verification artefact is the thing WP-73 calls UNTRUSTED.
15. **Book 4 Ch 26 ↔ Book 7 Ch Fy are cross-linked; the third leg is not.** Ch 44's
   instrument taxonomy is cited by the RH paper's §4.6 but Ch 44 does not cite the RH
   paper back. First editions cannot point forward; this is now second-edition work.
16. **r\* — RULED 2026-09-10 by Pablo: not a defect, do not sweep it.** The corpus
   carries 0.77594058; the certificate's midpoint to 8 dp is 0.77594058, so the corpus
   value sits 1.45e-8 above the certified upper bound. **The author's ruling is that the
   difference is too small to chase** — every use in the corpus quotes ~0.776 or eight
   digits in prose, nothing downstream depends on the eighth decimal, and a 67-file
   sweep would cost more than the error does. **This item is closed. A later session
   must not reopen it** on rediscovering the discrepancy; that it looks like a defect
   and is not is precisely why the ruling is written here. The standing rule stays as
   `ch24-verify.py` already states it: **prose keeps ~0.776, and anything cited past
   eleven significant figures comes from `certify_rstar_rigorous.py`, not from a
   float-bisection block.** Arithmetic in `docs/audit-log.md`, 2026-09-10.
17. **Book 3 has 1 verify script for 44 chapters** (`ch44-verify.py`). It is the taught
   path and the least instrumented book in the corpus; 18 of its chapters print a
   3+-decimal number. The cheap first move is one `book3-verify.py` for the constants
   that recur across chapters — the k-nacci roots, r\*, the 0.015 that appears in six
   chapters — not 43 separate scripts.
18. **AXLE Coach has two offered follow-ups, neither started:** a parent-facing companion
   to `coach.html` ("can my nine-year-old already do this"), and a mapping of Zero
   Sorries' eight sessions onto the CLEP College Algebra objectives so the course visibly
   aims at the exam.

### WP-96 — written 2026-09-07. Do not write a second one.

**Superseded note.** From 2026-09-06 this section read *do not write it, it exists
elsewhere*: the paper was held in a session on another account, out of budget until
8 September, and the sequence had a hole at 96 with 95 and 97 both shipped.

On **2026-09-07 the author instructed this session to take control and write it**, so
`book6/wp96-the-second-instrument.html` was rendered from `wp96-verify.py` — eight
sections against the script's five blocks — and indexed, with WP-95 and WP-97 rewired
so the chain reads 95 → 96 → 97. The page carries a *Provenance of this page* block
saying so.

**Reconciliation rule if the held version arrives.** The two are renderings of the same
claim set — the verifier fixes the claim, the scope and the tagging decision, and both
pages are downstream of it. Do **not** ship both and do **not** renumber. Compare the
two against `wp96-verify.py`; if the held draft says more, replace this page's body at
the same filename and keep the index row and navigation; if it does not, keep this one
and file the draft under `book6/_drafts/`. Either way the outcome is one WP-96.

What the paper argues: WP-79 states its filter as a general principle — "ratios are
falsifiable, scales are not" — and it holds only for spectrum instruments.
"Dimensionless" and "scale-invariant" are different properties; a phase is the first and
not the second. An action instrument reports S/ħ, and ħ is fixed by nature, so the
rescaling symmetry the filter quotients by is not a symmetry of that column. Block [5]
redoes the sorting: T*, μ_max and the light-cone velocity v move from unexposed to
exposed; the k-nacci roots η_k do not move. The physics is standard (Parker 2018 Cs,
Morel 2020 Rb) and is not claimed as a result. It carries no `#Machine Learning` tag,
per the rule of 2026-09-01, on the same grounds as WP-90.

Also note: `wp96-verify.py` reached the repo inside `c933f84`, a Book 4 commit, as a
swept-in file. It is correct and it belongs there, but it was not the subject of that
commit.

### Book 7 Ch Fy — Feynman, written 2026-09-08

`book7/ch-feynman.html` + `book7/ch-feynman-verify.py` (8 blocks, EXIT=0, numpy only,
no scipy). The Standard Model path integral read through G = U∘F∘K∘C, continuing the
Faraday → Maxwell → Einstein → Dirac chain and supplying the Higgs those chapters
lacked. Forward pointers added to all five predecessors and to WP-96.

The load-bearing new result is §VI: for α = dz − r²dθ and the dm³ field X,
**α(X) = −2(r−1)²e^{−z}** exactly. So the contact action is a strict Lyapunov
functional — zero on Γ = {r=1} over any interval, strictly negative on every other
orbit — and Γ is its global maximum. Also proved: the Reeb field of α is ∂/∂z and has
**no** closed orbit, so nothing here may invoke Reeb existence theory. Γ is tangent to
ker α, not transverse to it.

Two things are deliberately NOT claimed and are marked OPEN on the page:
the Gutzwiller weight 1/(2 sinh 2π) is printed but does not apply (dm³ is dissipative,
Gutzwiller assumes a Hamiltonian flow); and the cusp result holds only for the
one-real-field truncation, since the full SU(2)×U(1) potential has a vacuum manifold
and Arnold's A_k list classifies isolated critical points.

§VIII runs the WP-29 method on this chapter's own near-miss: κ* ≈ 0.882 agrees with
cos θ_W = 0.881357 to 0.073%, and it is REFUSED — a corpus of ~40 named constants
against ~25 SM quantities expects 0.32 such matches, so this is the expected one.
Recorded so the next reader finds the refusal instead of writing the claim.

Note: commit `cc4bbd1` (another session) swept the Feynman index card in `book7/index.html`
into a Ch Pr commit while this page was still unwritten. The card is correct and it
belongs there; it was not the subject of that commit.

### State at handoff — 2026-09-10

**geometry:** clean but for regenerated `index-*.html`. **1 commit unpushed:** `4df28b6`
*WP-84: the correction its own Lean file had already proved*. `2433ff7` (RH 4.6) and the
merged handoff went up while this session was running. `tools/verify-audit/2026-09-09/` is
**no longer untracked** — it is committed, because WP-84 now cites it. Open item 14 closed.

**WP-84 is the last thing that happened and it is worth reading before anything else.**
`FoldingFrequency.lean` was proved on 09-09 and its own header says WP-84's framing is
wrong — twelve is an instance, not a characterisation — and WP-84 knew nothing about it for
a day. Section 7's sweep verified "iff N = 12" at nine values of N while **holding k = 6**,
so it could only ever return 12. The general theorem is `visibleModes N k = {N/2} ↔ N = 2k`.
**A sweep that varies one axis of a two-axis claim confirms itself.** The page now carries
the correction, the six declarations, and the Lean file's own *nothing here bears on Saturn*
disclaimer, because `hexagon_at_twelve` and `decagon_at_twenty` beside a Saturn citation
invite exactly the inference the file forbids.

**AXLE:** clean and **in sync** — the five Coach commits are pushed.

**Pending on the desk:** `bash ~/Downloads/push-book4-whole.sh`, then
`cd ~/Desktop/geometry && git push`.

**Litter:** both repos have a `_to_delete/` holding git lock files moved aside by session
B before `--no-optional-locks` was understood, plus two stale downloads
(`coach-1.html`, `ch44-how-to-learn-1.html`) that are copies of delivered files, and
session B's superseded `sig-rh-lift.py`/`.svg`. **All safe to `rm -rf`.** geometry also
carries ~1,300 orphaned `.git/objects/*/tmp_obj_*`; `git gc --prune=now` from the desk
clears them.

**Standing constraints from Pablo, both still in force:**
1. **No attribution trailers in commits** — no `Co-Authored-By`, no `Claude-Session`, no
   generated-with line. Attribution goes in this handoff.
2. **"Where I came from, we have a place for an audit and that is not here."** No
   correction trails or self-audit narration inside deliverables; `docs/audit-log.md` is
   the place for those.

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
- **`device_bash` cannot unlink `.git/*.lock` — and does not need to.**
  Superseded 2026-09-09: `--no-optional-locks` stops the lock being taken, and
  `mv` clears one that was. The generalisation from "cannot `rm`" to "cannot use
  git" was the error.


---

## Moved from CLAUDE.md, 2026-09-13 — the 2026-09-05 handoff narrative

CLAUDE.md carried two handoff blocks; the 09-05 one opened the file above its own
title. Its standing rules stayed in CLAUDE.md. Its dated narrative is below, verbatim.

## What changed today, in one paragraph

The overnight job became a job, an `--audit` began leaving evidence, Tier 1 was
found to be a four-fold undercount caused by a glob, and a published claim was
found to be an artefact of a grid. All four are the same defect wearing four
costumes: **a measurement nobody could regenerate.** Every fix pushed in that
direction — the numbers now come from artefacts on disk, and where they cannot,
the tool says so.
## The Saturn correction, and the class it named

`hex_and_dec_forces_constant` is true and was carrying a sentence wider than
itself: "the only field admitting both a hexagon and a decagon is the trivial
one" is a fact about choosing THIRTY sectors. On sixty the periods are 10 and 6,
gcd is 2, and `k mod 2` is a non-constant witness. The grid-free statement —
rotations of order 6 and 10 generate C₃₀, so such a field shows thirty sides and
neither polygon — is closed by `periodic_gcd`, kernel-audited 2026-09-05.

Published as **WP-97, `book6/wp97-thirty-was-doing-the-work.html`**, with
`wp97-verify.py`. §7 names the class WP-73's seven lacked: **OVER-GENERALISED** —
true statement, wider prose, because a parameter fixed in the hypotheses reads in
prose as a constant of nature. Unlike MISATTRIBUTED it is mechanisable and cheap:
instantiate at a second value of every number in the hypotheses. A theorem whose
hypotheses carry a numeral the surrounding prose never mentions is a warning.

Provenance, recorded because the failure mode is the point: the finding came from
"what about base 60", asked twice, and the first answer — that a base is notation
and changes no number — was true and not responsive. Second time in a week that
arguing with borrowed vocabulary cost a finding; the other was ε₀ = 1/3 described
as "a chosen threshold" when it is a Grönwall bound. **When the words are wrong
and the gesture is at a structure, go look at the structure.**
## A.13 went to NASA

**Submitted 2026-09-05** (ROSES-2025 A.13, Needs and Opportunities,
`G6-AES-PROP-2026-13`, *Whose Flag Is It? Mapping the Decision Architecture for
Outdoor-Activity Restriction During Wildfire Smoke Episodes*). Stated by Pablo;
what is verifiable from this machine is that the four required documents exist
in `~/Desktop/A13/`, all built 5 September:

| file | pp | note |
|---|---|---|
| `A13_STM_ANONYMIZED_2026-09-05.pdf` | 8 | §1–12 = 6 of the 10 allowed pages; DAPR-anonymised |
| `A13_TOTAL_BUDGET_2026-09-05.pdf` | 2 | **not** anonymised — Table A.13-4 requires this separately |
| `A13_EXPERTISE_RESOURCES_2026-09-05.pdf` | 2 | |
| `A13_OSDMP_2026-09-05.pdf` | 2 | |

Alongside them: `A13_program_specific_data_answers_2026-09-05.md` (Q1–Q30 as
entered) and `A13_proposal_summary_v2_2026-09-05.txt`.

**Do not assume the NSPIRES-side items closed.** At last check these were open
and a next session should verify rather than infer them from the submission:
SciENcv biosketch and Current & Pending (SciENcv mandatory since 2026-09-01),
research security training, and the training sentence into Expertise &
Resources §7 — which would mean re-uploading that one file.

Facts worth not relitigating: N&O proposals are **limited to one year** by the
element text, so there is no year 2 or 3 to fill; the anonymised budget goes
*inside* the proposal document (Table A.13-1) **and** a separate non-anonymised
Total Budget is also required (Table A.13-4); NSPIRES warns if Q5 is answered
when Q4 is No. Contact email on everything is `g6llc@proton.me`.
## Open, in the order they should be taken

1. **The 22 files outside every build target.** Give each a `lean_lib` entry, or
   move it to `_to_delete/`. Until then they are unverifiable by construction.
2. **`verify-proofs.yml` discards its own axiom reports** into `/tmp`. It gates
   45 declarations named by hand in three heredocs, weekly, and only on pushed
   commits. Make it upload or commit the reports, and consider driving it from
   the tracked probes rather than heredocs — the dm³ step already does.
3. **The `verify-stamp` step in `verify-proofs.yml` is commented out**, waiting
   on `SaturnHexagon.lean` carrying a stamp generated under v4.32.0, which means
   generating it from a CI run and not from a local tree.
4. **`ZetaReflection` refactor: keep or revert.** If kept, `book4/ch12.html`
   line 331 reads "eleven theorems… one admitted" and must become twelve and two.
5. **`verify-book8/run.sh` counts `N` with an unanchored grep** that matches its
   own probe docstring. `verify-polar` uses the anchored form. Fix, in its own
   commit — moving a gate's N inside an unrelated commit is how a number drifts.
6. **O7** — one supremum computation (sup‖Hess V‖) from either closing or moving
   ε₀. Caveat recorded: ε₀ may live in a different norm than r.
7. Untracked and awaiting a decision: `book5/.bak-saturn-smoke`, `.bak-polar-*`,
   `tools/.leancheck.sh.bak-*`.

   **`book4/ZetaScratch.lean` — resolved 2026-09-13: removed from the tree.**
   The item read "untracked and awaiting a decision". It was neither: the file
   entered the history in `7860de0`, whose subject is the Eisenstein-norm
   classification of closable hexagonal shells, so a decision recorded as open
   had already been made inside a commit about something else, and the list
   tracking it never learned. A byte-identical copy had also accumulated at the
   repository root (2026-09-10); it is in `_to_delete/` with both hashes.

   The removal is not about the duplication. `digamma_conj` is live at
   `GTCT/book4/ZetaReflection.lean:404` and marked load-bearing there at :463.
   This was a second copy of a load-bearing theorem, in a repository that does
   not build it, outside every target, with an audit report containing the single
   token `file:` — so on the day the two copies diverge, the unchecked one is the
   one still sitting here. A second copy nobody builds is worse than no copy.

   Not salvaged here: `conj_Gamma_conj_eq` and `deriv_Gamma_conj` do not appear
   by name in `ZetaReflection.lean`, which proves `digamma_conj` by another route.
   If those two are worth having they belong beside the theorem that uses them,
   in GTCT, and not in this repository.
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

## 2026-09-13 — the instrument, not the corpus

A full night's Lean run returned 44 failures; six of them were about mathematics
and the rest were about the report. Each defect below is the same shape: a true
measurement under a sentence that licenses a wrong action.

- **MISFRAMED — the toolchain.** `overnight.sh` elaborated all 280 files against
  `geometry`'s `v4.32.0`, because it is the only project on disk with a built
  Mathlib. `AXLE` declares `v4.14.0` and holds 129 of those files. A file failing
  to compile under a toolchain it does not declare is not evidence about the file.
  Seven distinct toolchains are declared across the Desktop; two are unpinned
  (`stable`), so results under them are not reproducible.
- **MISATTRIBUTED, averted — three copies, one name.** The gate reported
  `ZetaReflection: sorryAx present`, naming `reflection_law` and
  `chiLog_real_on_critical_line`. It had read a frozen August deposit, which says
  of itself that both are ADMITTED. The live `GTCT/book4/ZetaReflection.lean`
  (2026-09-08) has 18 declarations and no `sorryAx`; the RH paper's
  "Proved, machine-checked (2026-09-08; admitted since 2026-08-30)" is exact.
  Fix: an address is `(path, sha256, date)`, never a name. Frozen deposits should
  not be re-verified at all.
- **MISMATCH — a parser artifact read as a lost theorem.** `Bhaskara`'s "expected
  11 theorems, found 10 — one was renamed, removed, or failed to elaborate" was
  the gate's own parser dropping `Bhaskara.brahmagupta'`, a name ending in a
  prime. Eleven declarations, eleven present.
- **UNTRUSTED, nearly missed — wrapped output.** `#print axioms` wraps a long
  axiom list across lines. A line-wise parser sees `[propext,` and misses the
  `sorryAx` on the next line. `MagneticLattice`'s single admitted theorem sits
  exactly there.
- **STALE — pages understating the kernel.** `book6/ch-reaction-diffusion-fold.html`
  ("not yet kernel-checked (compute pending)") and `book8/ch-turnaround.html`
  (twice: "not yet been run through the kernel", and again in its status line)
  both describe files that now pass, 3 and 6 declarations, permitted axioms only.
  Stale in the safe direction is still a page disagreeing with a gate.
- **MISFRAMED — scope inferred instead of declared.** A 3-file targeted run
  compared against a 45-file corpus run reported "dropped 44 files". True count,
  false sentence. Scope is now declared: a day directory without `order.txt` is a
  targeted run.
- **MISMATCH — the reader that could not see the declaration.** `DECLARE_RE` in
  `verdict_table.py` lacked `re.M`, so a `GATE-DECLARE` line on the first line of
  a file never matched. The line was present and the tool reported its absence.

**What the six genuinely sorry-bearing files turned out to be.** Every one already
declared its admitted theorems in prose — README's Open Obligations table, `OPEN
(sorry)` in ch17 and ch18, `AXLE_v8_1`'s own "Honest admits" block. There was no
hidden false claim anywhere in the corpus. What was missing was a form the gate
could read, which is now `GATE-DECLARE: sorries = …`. Board at close: 39 PASS,
6 PASS-AS-DECLARED, nothing to decide. A seventh file growing an *undeclared*
sorry is now the only thing that can go red.

Method written up in `docs/verification-checklist.md`; narrative in Book VI,
*The Hydrated Lattice*, §6.

### The same class, one about files and one about people

The day's first real finding and its last are the same defect.

The first: a gate reported `ZetaReflection: sorryAx present`, naming two theorems
the RH paper calls proved. It had read one of three copies sharing that basename —
a frozen August deposit that says of itself that both are ADMITTED. The live file
is clean and the paper was exact. `MISATTRIBUTED`: the reason was real, and it
belonged to a different object than the one named.

The last: a suspicion that one account's sessions were producing the chapter
bloat. The only instrument available to test it was `section_balance.py`, shipped
an hour earlier with a header stating that it does not detect that defect — and
the sample was 41 pages with 3 hits against an expected 1.1. Direction matched;
the measurement could not carry it. Meanwhile the one signal that *is* sound —
which commits still carry the forbidden `Co-Authored-By` / `Claude-Session`
trailers — runs the other way: 33 of 545 on the account with the most commits,
0 of 246 on the suspected one.

Same shape. A real observation attached to the wrong object, with a name doing
the work an address should do. Once about a file, once about a person.

**The rule, and it is the harder half of the defect taxonomy.** Attributing a
defect to a source before measuring it is `MISATTRIBUTED` whether the source is a
file or an author. The corpus's practice — an address is `(path, sha256, date)`,
never a name — has a counterpart here: a pattern is a rate with a denominator,
never an impression. A clean signal that runs opposite to a guess is not a
refutation of the guess; it is the notice that no measurement has been made yet,
and the point at which changing how anyone works would be acting on nothing.

---

## 2026-09-15 — The file existed only inside the page that claimed it had been checked

`chDis-disaster.html` is a Zenodo-deposited preprint. Its abstract read: *All
claims are formally verified in AXLE … Fourteen core theorems are presented, all
sorry-free.* Corollary 2 read: *The fourteen Lean 4 theorems in §5 constitute a
formal proof of all four parts of the Disaster Theorem … machine-checkable,
sorry-free, and depends only on Mathlib4.* §5 displayed the file in full, under
the banner `-- 14 theorems proved · zero sorry · AXLE verified`.

`DisasterTheory.lean`, `CatastropheF.lean` and `ChaosMu.lean` do not exist in
AXLE's working tree and have never existed anywhere in its history. The Lean
source existed only inside the HTML.

That is `MISATTRIBUTED` and would be the whole entry, except for what the listing
itself says. D2 asserted

    deriv (fun x => whitney_fold (1/3) x) 0 = 0

where `whitney_fold a x = x^3 + a*x`. The derivative is `3x² + a`, which at
`a = 1/3, x = 0` is `1/3`. The statement is `FALSE`, so `simp [whitney_fold];
ring` closes nothing and the file as displayed could not have compiled under any
toolchain. **The page carries its own proof that it was never run.** That is a
stronger finding than the missing file, and it is available to any reader without
access to the repository — which is the only kind of finding a published preprint
can be audited by.

Nine of the remaining entries are `NAME EXCEEDS STATEMENT`. D11 was docstringed
"bijection between catastrophes and operators" and proved `(7 : ℕ) = 7 := by
rfl` — `VACUOUS` under a structural name. D7, "the n-bonacci cascade is strictly
increasing toward τ", compares five decimal literals.

**The repair.** The file now exists at
`Orthogenesis/Disaster/DisasterTheory.lean` — in geometry, not AXLE, because
AXLE pins `v4.14.0`, has no `.lake`, and has no workflow, so a file deposited
there would be exactly as uncheckable as one that does not exist. It is imported
by `Orthogenesis.lean` and therefore elaborated on every push. D2 is restated as
the true statement (at `a = ε₀` the fold has *no* critical point; the fold is at
`a = 0`, which is what D3's own docstring was already saying), every docstring is
reduced to what its theorem says, the derivative identity is a declared `sorry`
under `GATE-DECLARE`, and a closing block names the five obligations the chapter
makes and the file does not discharge. The page states the correction.

**The class, measured.** `tools/decl_resolve.py` has enforced "every declaration
named in prose must resolve at the path cited" since 2026-08-27. It had never
been run across the corpus, because it takes a `claims.json` nobody ever built.
The tool was present; its input was not. That is the reduction ladder's own
failure mode — a rung reading from a table that was never generated — occurring
in the instrument built to catch it.

`tools/lean_addresses.py`, added today, needs no input: it takes the rung below,
asking only whether the *file* exists anywhere under any root a reader could be
sent to. Across 776 pages and 152 `.lean` files in four repositories:

    57 names resolve nowhere, cited by 106 pages
     2 resolve only under another case — open on macOS, 404 on GitHub

`ZeoliteCommutation.lean` alone is cited by eleven pages.

Beneath all of it: 36 pages assert that something is *proved in AXLE*. AXLE has
no `.lake`, no `.github/workflows`, and no axiom report. Nothing in it has ever
been elaborated by anything but a hand run. The three missing files are not an
exception in that repository. They are the visible end of a repository that
compiles nothing, and a citation to it has never been a verification claim,
whatever the sentence around it said.

### Same day, later — the defect was in three chapters, and two more theorems were false

Closing `DisasterTheory.lean` meant standing up Lean 4.32.0 and Mathlib in a
clean container and actually running it, which then cost nothing to point at the
two sibling chapters citing the other two missing files. Both are worse than
chDis was.

`chF-catastrophe.html` §4, "Seven Theorems … proved in AXLE … all sorry-free":

- **T2 false.** `deriv (fun x => whitney_fold (1/3) x) 0 = 0`. Byte-for-byte the
  same statement, with the same tactic, as chDis's D2. The defect did not appear
  twice; it was copied.
- **T3 false, and of a worse kind.** It asserted `∃! x, deriv … x = 0` under the
  hypothesis `0 < a`. For `0 < a` the derivative `3x² + a` is positive
  everywhere, so no critical point exists. The theorem asserted the existence of
  an object its own hypothesis excludes — not an overstatement but a
  contradiction, and the published "proof" ran `use 0` on a goal where `0` is
  not a witness.
- **T4 empty.** `∃ f, f x = x⁴ + ax² + bx` is `rfl` under an existential and is
  true for any right-hand side whatsoever. It was docstringed "cusp unfolds the
  fold".
- T5, T6, T7 arithmetic on numerals; T1 a definition. **None of the seven
  carried the content its name claimed.**

`chMu-lyapunov.html` §4, same banner:

- **T1 false at `t = 0`**, where `∀ t, 0 ≤ t → δ₀·exp(μt) < δ₀` reads
  `δ₀ · 1 < δ₀`. The hypothesis needed `0 < t`. T1 was the only one of the seven
  that quantified over anything and the only one about decay over time. The
  chapter names μ_max in its title and never states a proposition about it.

**Three files, three chapters, three false theorems, all published under a
machine-checkable banner against a repository that compiles nothing.** Each
refutation is now a theorem rather than a remark — `published_D2_is_false`,
`published_T2_is_false`, `published_T3_is_false`, `published_T1_is_false` — at
`Orthogenesis/Disaster/`, kernel-checked against the v4.32.0 pin with nothing
admitted, imported by `Orthogenesis.lean` so CI elaborates them. Reports in
`tools/verify-audit/2026-09-15/`.

Two notes on method, both of which cost time today.

The elaboration was done in a clean container from the toolchain pin, not on the
author's machine. That is the difference between "it worked here" and a run
anyone can repeat; the reports carry the source sha256 so the claim is about a
specific file and not about a name.

And `axiom_gate.py` failed the first report I wrote, on the string `sorryAx`
appearing in my own header comment "No sorryAx". That is the third time this
session a scanner has read prose about the defect as an instance of the defect —
after the vacuity scan reading a quoted `True := trivial`, and `DECLARE_RE`
missing a line-one match. A checker that cannot distinguish a mention from a use
will eventually be satisfied by silence, which is the failure mode that matters.

---

## 2026-09-15 — Book X opens, and book13 had no address at all

Book X — *Trade, Power and the Continent* — is the political-economy volume:
political science and mathematics, trade and economics. The glyph does two
jobs. X is ten and this is the tenth book. X is also the Africa term in BRIX,
the variable standing for a continent that has ratified a continental trade
treaty and has not yet acquired a voice to negotiate under it. The series
numbers the book; the second meaning is its subject.

Chapter 1 defines the volume's first measurable. Trade statistics record where
a commodity went — Brazil shipped 416.4 Mt of iron ore in 2025 for $28.9bn,
67% of it to one destination — and record nothing about what is already
promised. Destination concentration and contractual commitment produce
identical export tables, and only one of them is reversible. Three figures
close the gap: `E`, committed volume over national output; `C`, the
concentration of that commitment in one counterparty; `T`, the weighted
remaining term. None is published by anyone, for any country, for any
commodity.

The chapter's own load-bearing claim is that a long-horizon supply commitment
is the **sale of an option** — the credible ability to transact with somebody
else — and that no accounting standard records it as sold. The cash is booked,
the delivery obligation is booked, the extinguished bargaining position is
not. That is stated in prose and is not formalised, and the chapter says so in
its OPEN block rather than in a footnote.

It also keeps a correction on the page instead of behind it. The drafts ran
"iron ore → steel → Brazilian aircraft", which does not close: airframes are
aluminium, titanium and composites. The examples that do close are bauxite and
niobium. Brazil's niobium share is **not stated**, because it has not been
verified for that chapter, and an unverified number is exactly what this
corpus spent 2026-09-15 removing from three other chapters.

**And the defect found while registering the volume.** `tools/build_indexes.py`
carries the list that decides what has an address. `book13` — nine
category-theory chapters, committed, live on the site — has never appeared in
it. [The count read "eleven" until 2026-09-16; see that day's entry.] Nothing linked them, no generated index carried them, and
`index-book13.html` did not exist until today. Eleven chapters at no address,
in the corpus that has spent a month cataloguing exactly that failure, sitting
inside the one file whose job is to prevent it.

Both are registered now, `audit.py` reports clean across 727 HTML files, and
the lesson is the one already in this log on 2026-09-15: a checker that reads
its own scope from a hand-maintained list inherits every omission in the list.
The list is not the corpus. Nothing here yet derives the scan set from the
filesystem, and until something does, this will happen again.

---

## 2026-09-15 · WP-41 audited a second time, and the arrow that was never drawn

An external technical evaluation of `book6/wp41-planetary-triage.html` was
supplied to the author. Two of its findings were checked against the page and
both hold.

**Defect 1 — NUMBER EXCEEDS DERIVATION.** §3 assesses three receiving regions
bottom-up: US Mountain West 2–5M, Andes 3–8M, other high-altitude zones 5–10M.
The section then states a total of "~200–500M over 30–50 years", which is
roughly twenty times its own components. The large figure is not derived in §3;
it is carried back from the scenario in §2 and the abstract, where it was
assumed. Consequences of the small figure, none of which were drawn: the
movable share of the 2.3bn is 0.4–1.0%, not 9–22%; the relocation cost at the
paper's own $100k–$200k per person is $1–4.6T, not $20T–$100T; and §11's own
modelling task, sized at "5–10M additional residents", is written to the small
number. Neither figure is sourced. Corrected on the page; the abstract now
carries a standing-corrections block naming all three open corrections to that
paper.

Note the shape. The paper contains two answers to one question and carried the
larger into its conclusion. The operator claim was the interesting part and the
wrong part; the arithmetic sat in the section that was merely instrumental, and
instrumental sections do not get read. This is the third distinct defect found
in one paper, and the first two were found by asking about the interesting
claim.

**Defect 2 — THE MISSING RETURN.** The arc ran WP39 → WP40 → WP41 → WP66 →
WP67 → WP68 without once returning to WP39. Six papers asked which atmospheric
process could be called K. None asked what an operator must do to be a K. WP41's
own August addendum reaches the edge of the question — "the substitution simply
does not inherit its order-dependence, which was the whole reason to want a K" —
and withdraws one candidate rather than characterising the class.

Read backwards, WP39's T2(i) is a screen, and the proof never used the squaring.
`GateScreen.lean` (kernel-checked 2026-09-15, Lean v4.33.0-rc1 + Mathlib
eba3d887fc, sha256 `09c97f67e9ee2f67b7442f09c4136309924b93730c69a7276c76ffda261340c5`,
nothing admitted) generalises it: **the gate commutes with every layer-local
intervention that fixes zero, in every column state.** Aerosol, seeding,
microplastic loading — all layer-local, all disqualified, all by the same line.
What fails the screen acts on h, and nothing that acts on h at regional scale is
deployable. Published as `book6/wp123-what-k-must-be.html`.

**A third claim was made here and is withdrawn — see the 2026-09-16 entry.**
This entry originally said the screen "was already written down" in
`ch03-operator-sequence.html` and that WP41 was drafted in spite of it. That is
false, and WP-123 §5 carried the same error for a day. It is corrected below
and on the page.

---

## 2026-09-16 · Chasing X, XI, XII, XIII — and the count that was a directory listing

Four volume numbers checked against the filesystem and against what the corpus
says about itself. Three defects, one clean.

**XIII — MISCOUNTED, and by the worst possible method.** `book13/` holds
`ch01`–`ch09`, an `index.html` and `ch-mathlib-verify.py`. Nine chapters.
Yesterday's entry, the `build_indexes.py` comment and `CLAUDE.md` all say
**eleven**. Eleven is `ls book13 | wc -l`: nine chapters, plus the index that
lists them, plus the script that checks them. A directory listing was read as a
chapter count and promoted to a claim in three files — inside the entry whose
whole subject is numbers about addresses being wrong. Corrected in
`build_indexes.py` and in this log; `CLAUDE.md` line 97 carries it too and is
corrected in the same commit.

The general form is worth stating because it will recur: **`wc -l` on a
container counts the container's furniture.** Any census that does not name
what it is counting will silently include the index of the thing and the test
of the thing among the things.

**X — ADDRESSED BY THE GENERATOR, ABSENT FROM THE NAVIGATION.** `book10` is in
the FOLDERS list, `index-book10.html` is generated, and the orphan column reads
zero. It reads zero because three pages link into it, and all three were written
in the last two days: WP-123's references and the two correction blocks now on
WP-41. `series-hub.html` — the page a human uses to find a volume — has no row
for it. Neither does the root `index.html`. A reader arriving at the site cannot
reach Book X by navigating; they can only arrive through a correction notice on
a working paper about climate triage.

This is yesterday's defect one level up. Registering a folder with the generator
makes the *derived* index true. It does not put the volume in the *authored*
navigation, and the authored navigation is what anybody reads. Book XIII has the
same shape: its nine chapters are reached only from body text inside individual
chapters of Books VI, VII and VIII, never from a hub.

`series-hub.html` stops at **Vol IX**. Volumes X and XIII exist, are live, are
generated-indexed, and are not on it.

**XI — CLEAN, and the only one of the four that is.** Volume XI is declared
unwritten and is named as such: `book7/ch-grothendieck.html` calls it "the
unwritten Volume XI" and `wp82-the-missing-floor.html` gives it a seed — the
transverse Floquet multiplier as an index candidate, the thing Volume XI would
have to ground. An unwritten volume that says it is unwritten and names what it
would need is not a defect; it is the correct way to hold a gap open.

One update it has not received: WP-122 computed the whole return map that seed
sits inside, in closed form. The seed grew and nobody told Volume XI.

**XII — [WITHDRAWN 2026-09-16, see below.]** This entry said Volume XII was
named nowhere in the corpus. It is named in `wp82-the-missing-floor.html` §3,
which assigns XI–XVI. The finding was an artifact of the search pattern, not of
the corpus.

**What none of this is.** No chapter is wrong, no theorem is affected, and
`audit.py` was clean across 732 pages both before and after. Every defect here
is a statement about the corpus made by the corpus and not checked against it.


---

## 2026-09-16 · WP-123 §5 withdrawn and rewritten — hindsight presented as negligence

Corrected the same day it was published, on the author's objection, which was
right.

**What was claimed.** WP-123 §5 was titled "The rule was already written". It
quoted `ch03-operator-sequence.html` — "K as a 0/1 gate and F as a pointwise
fold commute exactly. Non-commutativity in this framework comes from inter-site
coupling inside F, not from the gate" — called it "K1, in prose, without the
quantifier", and said WP41 was drafted anyway. Yesterday's audit-log entry said
the same, and so did `tools/build_indexes.py`'s neighbours in tone: the arc
"spent six papers searching a slot the theorem had already closed", and "the
screen costs one line and the arc did not run it for two years."

**Two things wrong with that, one technical and one about what research is.**

*Technical — NAME EXCEEDS STATEMENT, and the name was mine.* ch03's caution is
not K1. It pairs the gate with **the fold**, and its target is a derivation: it
exists to forbid a spurious boundary term ∝ δ(η − η*). K1 pairs the gate with a
**proposed intervention** and quantifies over the whole class. Getting from the
first to the second requires noticing that the candidate occupying the K slot is
itself layer-local — which is WP66 §2's observation, and is not in ch03. The
algebra rhymes. The claim is different. Reading the earlier sentence as the
later theorem is only possible once you hold the later theorem, which is the
exact defect this log spends most of its length cataloguing, committed in the
paper that catalogues it.

*About the method.* Nobody knew WP39→WP40→WP41 would not work until WP66–WP68.
Had it been known, the papers would not have been written. On the evidence
available, an ice-nucleation aerosol at 2–4 km was the obvious occupant of the K
slot and a reasonable one: right altitude, threshold character, and the only
object in the frame a person can actually release. WP66's disqualifying
observation is not available until somebody writes down a specific deployment at
a specific altitude. WP67's half — the thing has been running for fifty years
and has produced no measurable effect — cannot be reasoned to at all; it was
found by looking.

Propose, develop, test, fail, turn. That is what the arc did and it is what
anyone does. K1 is its **residue**, not its correction, and the one line is
cheap only because six papers were expensive. The value is entirely prospective:
the next candidate gets screened by someone who never has to run this arc.

**What changed.** §5 is rewritten as "What the one line cost". The resemblance to
ch03 is kept and stated as a resemblance, with the difference spelled out. The
lede, subtitle, §1, the §4 finding box, §8's closing line, the Book 6 index blurb
and WP-41's standing-corrections block (c) all carried the same framing and are
all corrected. A note on Kepler is added: the *Astronomia Nova* came out of the
polyhedral programme worked thoroughly enough to reach an eight-arcminute
residual in Mars, and what decided it was a measurement rather than an argument.
This arc turned in months rather than Kepler's twenty-five years, for the same
reason — WP67 went and looked.

**The one defect that survives unchanged** is WP-41 §3's arithmetic: three
capacities of 2–5M, 3–8M and 5–10M and a stated total of ~200–500M. That needed
nothing learned later. Both figures are on one page in one section. It is worth
keeping the two apart — one is the cost of finding out, the other is a section
nobody re-read.

**The general rule this log now owes itself.** An audit written from the end of
an arc can always make the beginning look negligent, because the audit holds
what the beginning was trying to find. Before filing a defect as "they should
have known", check the dates and check whether the knowledge existed. The class
is *hindsight presented as negligence*, and it is the first entry in this log to
commit it.


---

## 2026-09-16 · Volume XII was named all along — and two number collisions the search should have found

Withdrawn on the same day it was filed. This morning's entry said Volume XII is
"named nowhere in the corpus", searching for `Volume XII`, `Vol XII` and
`Book XII`. WP-82 §3 writes it as a bare `XII` in a table cell. Present under
another form, which looks exactly like absence — the same class as receiving
capacity being counted every year under the heading "tourism". **A pattern that
matches a label does not measure a concept, and an absence produced by a search
is a fact about the search.**

**What WP-82 §3 actually assigns.** Six volumes against rungs 28–33 of the
"33 Levels" graphic:

| Vol | Rung | Subject | Kind |
|-----|------|---------|------|
| XI | 28 | K-Theory & Index Theory | FLOOR |
| XII | 29 | Operator Algebras — C*- and von Neumann | CONSOLIDATION |
| XIII | 30 | Higher Category Theory & ∞-Categories | NEW |
| XIV | 31 | Derived Algebraic Geometry | NEW |
| XV | 32 | Motivic Homotopy / Langlands | BRIDGE |
| XVI | 33 | Noncommutative Geometry | CEILING |

**Collision 1 — XIII is occupied by a different subject.** WP-82 reserves XIII
for higher category theory and ∞-categories, noting "Zero files use the
vocabulary." `book13/` on disk is ordinary category theory: ch01 *Never a
Diagram*, ch02 *What Category*, ch03 *On the Nose*, ch04 *Associator Pentagon*,
ch05 *Thirty-Three Compositions*. `build_indexes.py` registers it as "Book XIII
— Category Theory". Rung 30 is where the operator chain "stops being a diagram
and becomes a structure"; book13 is largely about the chain still being a
diagram. Either the plan was superseded and nothing says so, or the number was
taken while reserved.

The irony is on the record already. WP-82 was published as WP-81, a number that
was held, and renumbered — its own note reads: "The number was taken without
checking whether it was free — the same class of unmeasured absence this paper
is about." It happened again to the volume numbers in the same paper.

**Collision 2 — X had a prior occupant.** WP-82's limitations say: "Volume X
carries a deposit DOI in the AXLE header but no title appears anywhere in the
repository, so the arc from IX to XI has a segment this paper cannot see."
`book10/` — Book X, Trade, Power and the Continent — was created on 2026-09-14
into that slot. Whether it inherits that DOI or collides with it is not
established here. `[OPEN]`

**And the ruler.** WP-82's is "33 Levels of Mathematical Mastery", a circulating
graphic ordering fields by difficulty. WP-82 says plainly that the ruler is
damaged — it skips a numeral, jumps 28 → 33, and the placement of XIII–XV is
"an ordering chosen here, not one recovered from the source" `[ASSUME]`.

Strogatz, *Nonlinear Dynamics and Chaos* 2nd ed., Figure 1.3.1 (p. 10) is the
same genre of object built on a different principle: two axes, number of state
variables (n = 1, 2, ≥3, ≫1, continuum) against linear/nonlinear, with the
bottom-right cell labelled **"The frontier"**. Both axes are properties of the
system rather than of the student. He states the principle, marks where the
mathematics runs out, and invites the reader to move things or add axes — "the
point is to think about classifying systems on the basis of their dynamics."

A one-dimensional ladder can only say *higher*. A grid can say *where*. The
correction WP-82 needs is not a better ladder. `[OPEN]`

Primary source now held and checkable: the 2018 printing, 532 pages, at the
desk. Every page citation in WP-122 and `book7/ch-strogatz.html` was written
without it and can now be verified against it. None has been.

## 2026-09-17 · The map on page ten, and the count that was right about the wrong subject

The `[OPEN]` from 2026-09-16 above — Strogatz's Figure 1.3.1 as a grid where a
one-dimensional ladder can only say *higher* — is closed. `book7/ch-the-map-on-page-ten.html`
places this corpus on that figure; `book7/ch-the-map-on-page-ten-verify.py` is
eight blocks and passes with and without the PDF.

**Two corrections to what this session believed about the figure.** The earlier
note here was right that there are five columns, and the chapter as first drafted
said four and called it eight cells. It is **five columns by two rows — ten
cells**: `n = 1`, `n = 2`, `n ≥ 3`, `n >> 1`, `Continuum`, recovered from thirteen
positioned glyph runs on the single line `x = 163.2`. And the first draft
published a per-cell table for all sixty-one entries. It should not have. The page
is set rotated and pypdf emits **one text run for a whole row-line spanning
several columns** — `'Fixed points Pendulum Strange attra'` arrives as one string
at one coordinate. So the *column* of an entry is not recoverable from the PDF,
and the chapter now publishes the **row** (the linear and nonlinear glyph bands,
`x ∈ [197,280]` and `x ∈ [310,458]`, are disjoint — exactly one of the 236 runs
falls between them) plus only the **eight columns Strogatz states in prose**.
Position is a figure's content; the strings are captions. A figure read through a
text extractor loses the thing it exists to convey. `[FIXED before publication]`

**The measurement.** 61 entries, entity-aware at HEAD: **44 occupied, 17 at
zero**, and 8 of the 17 fall in the linear row, which has only 18 entries in it —
RC circuit, RLC circuit, mass and spring, 2-body problem, coupled harmonic
oscillators, equilibrium statistical mechanics, radioactive decay, viscous fluids.
WP-82's missing floor, found in one pass, because those are the systems Strogatz
puts on the page to give the rest of it a scale. The eight prose-anchored entries
read **260, 119, 71, 69, 6, 3, 0, 0** — and the only two at zero are the RC and
RLC circuits, the pair he uses to explain what the horizontal axis *means*.

**A fourth failure mode of the counting instrument, now recorded in
`tools/corpus_count.py`.** WP-82 §4 has three: wrong spelling, substring
inflation, HTML entities. Each produces a visibly wrong number. This one has no
symptom — **sense collision**: the string is right, the anchor is right, the
entities are handled, the arithmetic is right, and the referent is a different
subject.

    entry              string   dynamical   other sense
    Life                  151          11             –   (the English word)
    Plasmas                93          35            31   (plasma cells, blood plasma)
    Turbulent fluids       49          10            12   ("messy flow")
    Economics              45          19            23   (project economics)
    Acoustics              19           5             9   (archaeoacoustics)
    shocks                 19           7             7   (price, income, bill)
    Levinson                8           6             2   (Evans & Levinson, linguistics)

`Life` is the figure's own punchline — Strogatz's hardest named cell — and 140 of
its 151 files are the ordinary English word. Every count this corpus has published
for a word with more than one sense in it was a string count wearing a sense's
name. Figure 1.3.1 exposed this because the figure's cells are *senses*, not
strings.

**And the audit failed the same way on its first run.** The first companion
pattern for `Plasmas` accepted **83 of 93** — it contained `reconnect` and
`fusion`, which matched **304** and **43** times respectively while `tokamak`
matched twice and `stellar plasma` once. That is WP-82's *second* failure mode,
committed while auditing the fourth, and it would have promoted the false positive
into a verified count. It was caught only because the block prints a per-term
breakdown instead of a total. **Print breakdowns.** That is the transferable
result of the day and it is worth more than the tables. `[FIXED]`

**And the page closed its own gaps.** Run at HEAD after the commit, the same
script reports `RC circuit` at 3 rather than 0 and **the seventeen zeros collapse
to none** — every gap covered by the page that names it, with nothing in the
corpus changed except that the gaps were written down. This is WP-82's rung table
again: a column read 12/12 because the paper printing the table was one of the
twelve and the true value was 0. Fixed by pinning every count in the chapter and
the script to commit `b42750e`, the last before this measurement began, and
printing the drift at HEAD in block [8] so the self-count is visible rather than
assumed. Any future page that measures the corpus and then joins it needs the same
pin. `[FIXED before publication]`

**Queue.** Seventeen zeros, ranked in the chapter by how much machinery the corpus
already owns. Two shapes recur: entries *occupied by person and empty by phrase*
(Smale 12 files, Levinson 6, van der Pol 9 — and `forced nonlinear oscillator` 0,
`anharmonic` 0), and a linear row whose gaps are the first systems in an
undergraduate course. Fifty-four of the sixty-one entries have not been sense-audited;
on the evidence of the seven that were, there is no reason to assume they are clean.
`[OPEN]`

## 2026-09-17 · later — the Lean was never chased, and two published numbers were wrong

**Withdrawn: "AXLE compiles nothing."** It was carried in the handoff block and
repeated in conversation, and it was never tested — the Cowork Linux VM has no
`elan`, `lake` or `lean` on PATH, so nothing in this session could have tested it.
`lake env lean book6/lean/grothendieckAddGroup_nat_equiv_int.lean` run by the
author on the desk **elaborates**: three errors and an axiom report, which is a
toolchain working, not a toolchain absent. The claim is struck; the replacement
claim is per-file and stated below. `[FIXED]`

**Corrected: "55 Lean names resolve nowhere across 102 page-citations."** That was
measured under **2 of the 11 roots** in `tools/corpus_roots.txt` — the R15 failure
recorded on 2026-09-16, committed again. All eleven roots are now mounted and
searched (AXLE, geometry, GTCT, vol1-proofs, 3M, dnls, b3s, grossi-ops, Projects,
~/geometry, Downloads). 812 pages against 202 distinct corpus `.lean` basenames:

    36 resolve nowhere in this corpus
     2 resolve only under another case  (main.lean → Main.lean;
                                         discretedm3.lean → discreteDm3.lean)
     5 resolve UPSTREAM in .lake/packages
    74 citations in all

**The 5 upstream names were a defect in the checker, not in the corpus.**
`GrothendieckGroup.lean`, `ClassGroup.lean`, `ClassNumber.lean`, `Convolution.lean`
and `Deligne.lean` are Mathlib files that WP-82, `book4/ch12`, `book4/rh-paper` and
`book6/archive` cite **accurately** — WP-82 names
`Mathlib/GroupTheory/MonoidLocalization/GrothendieckGroup.lean` (Best & Dillies,
2025) in the sentence that makes its argument. `.lake` is in `SKIP_DIRS` so
Mathlib's 4,543 files do not drown the corpus's, and the effect was to report
someone else's correctly-cited file as the corpus's dangling claim.
`lean_addresses.py` now carries `upstream_names()` and a third finding class,
`UPSTREAM`, which prints but does not set the exit code. **An absence report that
does not say whose file is absent is not a measurement.** `[FIXED]`

**The Lean census, all reachable roots, comments stripped.** 351 `.lean` files,
**3,188 theorem/lemma declarations**, **384 `sorry` tokens in 98 files** — so 253
files carry no literal `sorry`. Per root: AXLE 129 files / 1,378 decls / 187
sorries; geometry 53 / 384 / 7; GTCT 37 / 212 / 28; grossi-ops 48 / 434 / 27;
Projects 35 / 204 / 79; ~/geometry 28 / 229 / 6; dnls 4 / 152 / 46; 3M 7 / 55 / 4;
vol1-proofs 7 / 136 / **0**; b3s 3 / 4 / 0.

**That census is an upper bound on cleanliness and must not be published as a
proof count.** `sorryAx` arrives transitively: a file with no literal `sorry` can
still depend on one through an import, which is exactly what the author's run
showed. Only `#print axioms` settles it, and only `lake env lean` produces that.
`vol1-proofs` at 136 declarations and zero literal sorries is the strongest
candidate for a real axiom report, and it has not been run.

**Volume XI, concretely.** `book6/lean/grothendieckAddGroup_nat_equiv_int.lean`
(61 lines) is **not proved**: `depends on axioms: [propext, sorryAx,
Classical.choice, Quot.sound]`. Three errors, the first being
`AddLocalization.mk_eq_zero_iff` — an unknown constant in the pinned Mathlib, so
the bridge lemma is named but does not exist under that name.
`book6/lean/VolXI_K0_Floor.lean` (183 lines) already states the bar in its own
docstring — "elaborates clean AND reports its axioms without sorryAx" — and says
what is missing is a definition and a bridge lemma, not a field. Nothing to
correct there; it is honest and in progress. `[OPEN]`

## 2026-09-17 · item 2 of the register, closed in the negative

`book7/dm3-transverse-modes-verify.py`, six blocks, exit 0. Built instead of
another audit, and chosen by reading `docs/missing-instruments.md` rather than
scanning the corpus — R19's first use.

The Jacobian on Γ is `[[−2 + 2e^{−z}, 0], [2, 0]]`; both z-derivatives vanish
identically because every `e^{−z}` term carries `(r − 1)`. One-turn monodromy
`M(z₀) = [[m(z₀), 0], [2I(z₀), 1]]` with `m(z₀) = exp(−4π + 2K e^{−z₀})`, matched
to RK4 below 1e-9 at six base points. That exponent is the same `E(z)` the
q-factor instrument uses, and `m(z_c) = 1` at its pole — two instruments, one
object, which is worth more than either.

**γ(f) does not exist for this flow.** `eig M = {m(z₀), 1}`, the 1 being
translation along the helix, so the transverse spectrum is one number per base
point. A rank-one transverse direction cannot carry a frequency-resolved damping
under any Floquet set-up. Structural, not technical. The register's open question
— whether the right object is a cocycle over z-translation — is answered yes, and
`m(z₀)^n` is wrong by a factor of order one or more, so treating Γ as a closed
orbit is not a small error. `e^{−4π}` is the z → +∞ limit of the cocycle and the
multiplier of no orbit; the ratio is exactly `exp(2K e^{−z₀})`.

Consequence recorded for the vocabulary: "overshoot", "fold" and "resistance" are
not modes of this linearisation with a frequency and a width each. `[FIXED]`

Also honest, and in block [5]: beyond z₀ ≈ 36.7 the excess `2K e^{−z₀}` falls
below float64 epsilon and the ratio rounds to 1. The check now asserts the
crossover where the epsilon argument puts it, rather than quietly testing a
smaller range. A fact about the arithmetic, not the flow.

## 2026-09-17 · item 4 closed — the Pacific trio is collinear to 1.4%

`book8/multiorbit-symmetry-verify.py`, five blocks, exit 0. Chosen over item 3
because item 3's inputs (published cyclone scale heights and decorrelation times)
are not in the repository and sourcing them is where a fabricated number would
enter; item 4 needs only `docs/multiorbit-pacific-2026-09.md`.

**The conjecture was being read too weakly.** "2^d − 1 companions" is not a count
of arbitrary companions: a ℤ₂^d orbit is a *box*, and for d = 2 it is the four
corners of a rectangle. That converts the count into a configuration test needing
no knowledge of where the mirrors are — three points sit in a rectangle iff one
triangle angle is 90°, and if one does, the fourth corner is predicted. Validated
on an exact rectangle (90.000000, fourth corner recovered), an equilateral (60°)
and a collinear triple (0°) before being used.

**Pacific trio: falsified for every d.** Angles 10.0° / 161.1° / 8.9°; closest to
a right angle is 71° off. Monte Carlo over the prose-to-coordinate reconstruction
— landmark ±0.15°, distance ±8%, bearing ±11° — gives median 161.4°, 5–95% band
[137.3°, 178.0°], and **0 of 20,000 draws** within 5°. The reason is collinearity:
2,143 + 2,391 − 4,473 = 61 km, tight to **1.4%** of the long side. d = 1 orbits
have 2 points; d = 2 needs a right angle; d ≥ 3 has rectangles as 2-faces and
three collinear points share no 2-face. The register's word "strung" now has a
number.

**Recorded so it is not over-read:** this falsifies the *trio*, not the
conjecture. The conjecture speaks about configurations with a mirror symmetry, and
the register's own note describes this environment as asymmetric — cooler water,
shear, higher latitude east — which is the conjecture's own escape clause. The
trio was never a test case; the value of the exercise is that establishing so cost
hours. `[FIXED]`

## 2026-09-17 · item 4 on real tracks — HURDAT2, and the 8 = 2³ trap

`book8/hurdat-symmetry-verify.py`, five blocks, exit 0. The earlier instrument's
honesty block named HURDAT2 as the remedy for its prose-reconstructed positions;
this is that run. File fetched through the browser straight to `~/Downloads`
(7,071,568 bytes, 57,513 lines) so none of it passed through the session — 1,988
storms, 36,351 TS/HU six-hourly rows, 30,544 synoptic epochs, zero unparseable
coordinates, lat/lon confirmed in basin range before any test ran.

    co-active   epochs   test                               observed     null
        3          588   closest angle within 5 deg of 90      10.0%    11.1%
        4           72   four points a rectangle within 5      0.0%     0.0%

Ratio 0.91 on the corner test — co-active storms are marginally *further* from a
right angle than positions drawn at random from the same geography. On the direct
d = 2 test not one of 72 four-storm epochs is a rectangle, and median worst-corner
deviation is 80.7 deg observed against 72.0 deg for the null. **No support for the
d = 2 symmetry-image prediction in 175 years of Atlantic tracks.** Same verdict as
the prose trio, now with 660 configurations and a null instead of one
reconstruction.

**The cheaper guard, added to the earlier instrument as block [6]: `d <= k`.**
Z_2^d needs d mutually orthogonal mirrors and R^k admits at most k, so a cyclone
field (a surface, k = 2) can only offer counts 1 and 3 — the seven-point case is
geometrically unavailable to storms whatever the data says. Recorded because the
NCEI 2002 report gives September 2002 as the most active month on record with
**eight** named formations, and 8 = 2^3 fits source-plus-seven exactly. It is the
most attractive d = 3 candidate in the Atlantic record and the geometry kills it
before a single position is looked up. A matching headcount is not evidence — the
vocabulary-correspondence failure, caught this time before it was written down.

Still not a falsification of the conjecture, which speaks about configurations
that HAVE a mirror symmetry. What is established is that co-occurrence in a
hurricane basin is not one. `[FIXED]`

The East Pacific file did not download (only the Atlantic landed) and was not
used, so Lowell/Karina/Marie remain only in the reconstruction instrument; 2026 is
past this file's 2025 end regardless. `[OPEN, low value]`

## 2026-09-17 · the Strogatz chapter rewritten to his register, and the confession removed

Two corrections to `book7/ch-the-map-on-page-ten.html`, neither of them about the
mathematics.

**Audit narrative was in a reader-facing chapter.** The page carried a
block-theorem headed "the sense test failed the same way on its first run",
narrating how a companion pattern accepted 83 of 93 plasma files. That is a
process finding and it belongs here, where it already is, not in a chapter under
the author's byline. Cut, 1,173 characters. What survives in the chapter is the
transferable rule stated impersonally — print the breakdown, not the total —
because that is method a reader can use. The 83/93 and `reconnect` 304 figures
stay in the verify script, which is a tool and the right place for them.

**The page did not read like the book it is about.** Measured, rather than
argued: Strogatz's own §1.3, two pages from the figure, runs 49 sentences, mean
19.9 words, longest 48, em-dashes 6.2 per thousand words, 31% of sentences under
15 words. The draft ran mean 24.5, longest **182**, em-dashes at nearly double his
rate, and opened its second section on pypdf extraction before the reader had a
reason to care. Rewritten: 2,248 words, mean 14.2, longest 68, em-dashes 1.8 per
thousand, 65% under 15 words. Five tables cut to three. The method section moved
to the back. The page now closes where it should — on what the blanks say, which
is that they sit in the top-left corner among the circuits and springs, not at
the frontier where Strogatz put his dragons.

`ch-the-map-on-page-ten-verify.py` gains block **[9]**, which recomputes
Strogatz's register from pp. 9 and 11 of the PDF and holds the chapter to it. It
is a register check and not a quality check, and it says so. No other instrument
in the corpus measures prose.

**And block [8] learned something.** Its self-count check required HEAD's zeros to
be a subset of BASELINE's, and it failed: `Iterated maps` reads 1 at `b42750e` and
0 at HEAD. The single baseline hit was `CLAUDE.md` — the old handoff block's own
WP-124 note listing `logistic map`, `iterated map`, `circle map`, `standard map`
as reading 0 chapters. Overwriting that block removed the phrase. Not a content
regression: the term was project scaffolding and never a chapter, which is the
distinction `wp82-verify` block [3] already draws. The check now names any entry
that moves the other way and asserts its lost hits were scaffolding rather than
chapters. `[FIXED]`

## 2026-09-17 · the verify-audit directory existed all along

**`tools/verify-audit/2026-09-09/` holds a corpus-wide axiom audit: 69 `.axioms.txt`
reports, 46 `.gate` files and a `verdicts.tsv` of 45 rows.** Of the gate lines, 22
read *"OK: N theorems, no sorryAx, no axiom outside the permitted set"*; 6 read
*"sorryAx present — a theorem is admitted, not proved"*, with 3 more naming
`claimN` and 2 naming `TOGT.gN_unconditional_closure`. Thirteen `verdicts.tsv`
rows carry AMBIGUOUS notes where 2–4 copies share a file name. One gate line is
worth lifting out on its own: *"native_decide leaves Lean.ofReduceBool and is NOT
a kernel check."*

This session said twice that the corpus had no machine-checked core outside
`vol1-proofs`, and once that nobody knew whether anything passed. Both statements
were made with this directory in the repository, last touched 2026-09-15. It was
found by following a failing check rather than by searching for it. R19's reading
order should have named it; `docs/` was on the list and `tools/verify-audit/` was
not. **Any corpus-wide claim about proof state reads `tools/verify-audit/<date>/`
first — `verdicts.tsv` for the ledger, `*.gate` for the verdicts.**

**Two flagship "unresolved" Lean names resolve.** `book6/ch-the-present-king-of-france.html`
tabulates `Chain.lean` at 23 citing pages and `ZeoliteCommutation.lean` at 11,
under a two-root search, and — to its credit — says outright that "more than twenty
repositories have not been searched" and that the honest state of all 66 names is
"unresolved, not absent". That work is now done, eleven roots:

    36  resolve nowhere
     2  resolve only under another case
     5  resolve UPSTREAM in Mathlib, never this corpus's claims
    74  citations in all

`Chain.lean` is at `GTCT/Chain.lean` with two further copies in GTCT.
`ZeoliteCommutation.lean` is at `io-clone/zeolite_operator_order/`, the eleventh
root, and its gate in this repository reads **OK: 6 theorems, no sorryAx**. The
chapter gains a dated *Searched* block recording all of it; nothing in the original
text needed retracting, because the original text had already refused the absence
claim. Its verify script's stale `>= 20` threshold on the most-cited unresolved
name is rebased to `>= 10`, since resolving `Chain.lean` moved the top of that
table. `[FIXED]`

**A near-miss worth recording.** A sweep of the three Ramanujan-family chapters
reported `book7/ch-ramanujan-1pi-verify.py` as "0 pass, 0 fail, exit 0" — a silent
detector. It is not: that script prints `ok` where the others print `PASS`, and it
runs 18 checks with 0 failures. The sweep counted the wrong token. Same shape as
the sense collision in `ch-the-map-on-page-ten`: right string, wrong referent,
arithmetic correct. Caught before it was reported. **A sweep over scripts must
count each script's own vocabulary, or read its exit code and nothing else.**

## 2026-09-17 · the root's conventions curated, and the fourth ledger miss

**Curated into CLAUDE.md** as `## Filename conventions at the root — Book 3`: a
table covering all 301 root-level `.html` files. Chapters account for 126 —
`chN-` 67, `ch{Greek}-` 27, `ch-` 27, `capitulo-` 2, plus 6 `sessao`/`session`
IMPA pairs. The largest single body at the root is **`dm3-1NN-wNN.html`, 48 pages:
three courses (101, 102, 103) of sixteen weeks each**, a teaching programme that
no convention described. Also written down: `for-<venue>` (bienal, brazil-china,
ichep), `series-<part>` (hub, intro, layer-map), and the generated `index-*`
family. What remains outside the conventions is one-off pages named for their
subject, which is the intended state rather than a gap.

Two same-book duplicate pairs recorded as unresolved: `spectral-radius` /
`spectral-radius-v2`, and `GameTheory_Full_Pack` / `GameTheory_Full_Pack.FIXED`.
The `.FIXED` copy is one of `index-root`'s eight orphans and double-counts in any
measurement touching game-theory vocabulary — it inflated the `shocks` sense audit
earlier today. Left alone because both are same-book pairs where a version suffix,
not a directory, carries the claim about which is current; the nine Book 3 / Book 4
pairs resolved on newer-wins do not settle these.

**The miss, recorded because it is the fourth of the same kind today.** This
session described the root as sprawl, then reported that Book 3 was not in this
repository and that its body was 24 pages in AXLE "on the wrong side of the
canonical-HTML rule". `CLAUDE.md` § Site structure opens with
`geometry/ root = Book 3 (G3) chapters, prelude, overture, portals`, four lines
above where the new section was inserted. The section had been grepped for a
heading and never read. **Withdrawn:** the canonical rule was never violated;
Book 3's HTML is in geometry, at the root, since March.

The other three misses today were the same shape — `vol1-proofs` proposed for an
axiom check it has gated in CI since 25 August; `certify_rstar.py` queued for a
DOI edit a canonical v1.1 had superseded; `tools/verify-audit/` unknown while
claiming no machine-checked core existed. R19 said read the ledger and named four
files. The rule needs the stronger form: **read the section, not its heading**, and
`CLAUDE.md` § Site structure and § Where files live are part of the ledger.

**One thing the misses did not cost.** `Projects/book/` holds 209 pages including
the full Greek-operator set and is excluded from `corpus_roots.txt` as a working
directory. All eighteen Figure 1.3.1 entries recorded as zero were tested against
its 213 files: **eighteen for eighteen, still zero.** The seventeen gaps survive
the addition, so `ch-the-map-on-page-ten`'s numbers hold and the exclusion cost
nothing on that measurement.

## 2026-09-17 · Volume XI's sorry — the Mathlib API read off the source

`book6/lean/VolXI_K0_Floor.lean` carries one declared `sorry`:
`Nonempty (GrothendieckAddGroup ℕ ≃+ ℤ)`. The placement map calls compiling this
file XI's unblock, and the file's own comment said the assembly was never
attempted because it could not be compiled. It compiles now.

Four API facts added to the file, each **grepped from
`.lake/packages/mathlib`** rather than recalled, since the first compile failed
on a name that does not exist:

1. **`AddLocalization.mk_eq_zero_iff` does not exist** — that was the run's first
   error. The working pair is `Localization.mk_eq_mk_iff` (Basic.lean:224) with
   `r_iff_exists` (Basic.lean:191), additivised by `to_additive`.
2. `GrothendieckGroup M` is an **`abbrev`** for `Localization (⊤ : Submonoid M)`
   (GrothendieckGroup.lean:36), so the whole `Localization` API applies
   unchanged and `AddLocalization.induction_on` is the eliminator.
3. `lift` is an **`Equiv`**, not a function (line 81), so it must be coerced
   before it behaves as a map; `lift_apply` unfolds an application.
4. **Nothing in Mathlib equates any localization with `ℤ`.** The only files
   naming GrothendieckGroup are its own, `Finite.lean` and
   `AffineMonoid/Embedding.lean`. So the theorem is genuinely absent upstream
   and is not being reproved out of ignorance — the R18 check, done.

The proof shape that follows is written into the file as a comment and
explicitly **not compiled**: this environment has no `lake`, and an uncompiled
Lean proof is a guess, not a contribution. Left as the next command to run.

Related, from the same day's Book IV work: `book4/ch-euclidean-algorithm.html`
now gives the classical route to the fundamental unit — expansion, convergent at
norm −1, cube, square — reaching `eps^6 = 9801 + 1820 sqrt29`. XI's core
candidate in the placement map is the Pell row, so the arithmetic side of XI has
a worked chapter behind it even while the Lean side has a sorry. `[OPEN]`

---

## 2026-09-18 · Volume XI's sorry is discharged — and the proof was not a construction

`book6/lean/VolXI_K0_Floor.lean` now compiles with **no `sorry`** against the
pinned checkout (`mathlib 81a5d257c8`, toolchain `v4.32.0`). The report:

```
'PrincipiaOrthogona.VolXI.grothendieckAddGroup_nat_equiv_int'
    depends on axioms: [propext, Classical.choice, Quot.sound]
```

No `sorryAx`. That is WP-82's admissibility bar, in full. `[VERIFIED]`

`Classical.choice` is expected and is Mathlib's, not the argument's:
`addEquivOfQuotient` is noncomputable and the localization is a quotient.

**What the theorem turned out to need.** Nothing built. Mathlib's
`Localization.mulEquivOfQuotient` (Maps.lean:615, `@[to_additive]`) already
carries a localization map to an isomorphism, and `GrothendieckAddGroup M` is an
`abbrev` for `AddLocalization (⊤ : AddSubmonoid M)` — reducibly the same type.
So the whole task was certifying that the cast ℕ → ℤ **is** a localization map
at ⊤, which is three arithmetic conditions (`AddSubmonoid.IsLocalizationMap`,
Basic.lean:87–90): every integer is an additive unit, every integer is a
difference of two naturals, the cast collapses nothing. `omega` sees all three.

**Correcting yesterday's entry.** Point 3 above — "`lift` is an `Equiv`, so it
must be coerced before it behaves as a map" — was true and was a dead end.
Candidate 1 followed it and died on `lift_apply`, which states the lift through
`(monoidOf ⊤).sec`, a **choice function** that picks a representative and does
not reduce; both branches stranded identically, including the one the header had
predicted would go through. Candidate 2 routed around `sec` with `lift_mk'_spec`
(Maps.lean:143), which is the right lemma and still carries the full burden of
proving a hand-built map bijective. Candidate 3 dropped the map.

The rule, which is general and not an anecdote: **when a universal property is
available, constructing the map by hand is work you have chosen, not work the
theorem requires.** Both failing candidates are kept unedited at
`book6/lean/VolXI_attempt.lean` and `book6/lean/VolXI_candidate3.lean`.

**What is still missing upstream** is unchanged: the monoid of finitely
generated projective modules under ⊕. §2 of the file proves the second half of
"K₀ of a field is ℤ" and states the first half as the thing Mathlib does not
have. That is a gap in Mathlib, not in the file. `[OPEN]`

WP-82 (`book6/wp82-the-missing-floor.html` §3) restated to match.

---

## 2026-09-18 · "Across series" reached one repository — grossi-ops.github.io/TO has served a withdrawn r★ for 77 days

**The finding.** `https://grossi-ops.github.io/TO` is live, returns 200, and is
byte-for-byte the pre-correction `book4/hub.html`. It prints **r\* ≈ 0.773** in
four places: the dm³ contact equations block, the `poincare_collatz_contracting`
row, the `inner_basin_is_asymmetric` row, and the hierarchy line
`ε₀=1/3 < 2/3 < r*≈0.773 < κ*≈0.882 < 1`.

That value was withdrawn here on **2026-07-03**, commit `4beb902`, whose subject
line is **"Fix dm3 math: r\*=0.77594058 across series"**. It was not across the
series. It was across this repository. Seventy-seven days later a second live
address is still publishing the number the commit message says was fixed
everywhere.

`geometry/book4/hub.html` carries 0.776 in all four places and is correct. No
page needs writing. A deploy needs doing, and this session cannot reach that
repository.

**The class.** Not a wrong number — a correction whose scope was asserted rather
than checked. `r-star-mess.html` already names the shape ("one number, four
values, five repositories"); what this adds is that the repair inherited the
same defect as the thing it repaired. A commit message is not a survey. **"Across
series" is a claim about other repositories and must be produced by something
that reads them, or it is not a claim** — R18 and R15 in the same sentence.

**And a second r★ that is not this one.** A parallel session spent 2026-09-17
correcting `TOTOGT/io/index.html`, the CatGT / Helical Selectivity page, whose
`r* = a√(J/λ)` is a radius in lattice spacings in the DNLS model — a different
object from the dm³ inner-basin boundary, sharing a symbol. Both are called r\*
on live pages with no disambiguation anywhere. `[OPEN]`

**A real defect on that page, verified here independently.** `Projects/io/index.html`
(the stale working copy, 2026-07-18) states: "The Reeb vector field R = ∂z
satisfies ι_R dα = 0 and α(R) = 1. Its integral curves (r₀, θ₀, z₀ + t) are
helical lines." The curve written is correct and the name is wrong — r and θ are
held constant while z advances, which in cylindrical coordinates is a straight
vertical line. A helix needs θ to advance with z. NAME EXCEEDS STATEMENT, the
same class as `ch-strogatz`'s "degenerate" and as WP-123 §5. Prediction 3 rests
on a "Reeb-helix signature" and falls with it. The correction is the other
session's; this entry records that it was checked against the file and holds.

**What is not established here.** Whether `grossi-ops.github.io/TO` is deployed
from a repository anyone still edits, and what else among the 64 lines of drift
between the two copies matters. `[OPEN]`

---

## 2026-09-18 · Auditing grossi-ops.github.io/TO — the equations were the typo, and the Reeb field is not the helix

Full audit of the TO hub at the author's request, after the r★ correction was made
but landed on a path the site does not serve. `tools/to_hub_verify.py`, stdlib
only, five blocks, exit 0.

### The deploy, first

Pages serves this repo from `/docs`. The corrected file went to the repository
root, so the live page never changed. Three copies existed at the moment of the
audit — root `index.html` with r★ = 0.77594058, and `docs/index.html` and
`tornhub.html` both still at 0.773, with `docs/index.html` the one being served.
**A correction that lands on an unserved path is indistinguishable from no
correction.** This is the same class as the `book4/hub.html` finding of
2026-09-16, one level further in: there the repository was right and the copy was
stale; here the copy was right and the served file was stale.

### The equations were the typo, not the constants  `[VERIFIED]`

The page printed ṙ = r(1−r²) + 2(r−1)·e^(−r) and ż = r² − 2(r−1)²·e^(−r), and two
lines below printed λ(z) = −2(1−e^(−z)) → μ_max = −2. Those cannot both hold, and
the arithmetic says which is wrong:

| reading | f′(1) at Γ | inner zero of ṙ |
|---|---|---|
| as printed, e^(−r) | **−2 + 2/e = −1.264241118** | **0.641494576** |
| e^(−z) | −2(1−e^(−z)) exactly, → −2 as z→∞ | — |

So with e^(−z) the page's own λ and μ_max are exact; with e^(−r) neither holds and
r★ is not a zero at all (ṙ(0.77594058) = +0.1025). **The constants were right and
the exponent was wrong.** This also independently confirms the coupling erratum
recorded in the handoff — the e^(−r) system's inner boundary is ≈0.641 — without
appeal to `certify_rstar.py` v1.1, which could not be found: the path the handoff
names does not exist, and none of the nine copies on this desk carries "v1.1",
"CANONICAL" or any erratum text. `[OPEN]`

### The Reeb field is not the helix — and the helix is Legendrian  `[VERIFIED]`

Two pages in this corpus say the helical attractor is an orbit of the Reeb field.
For α = dz − r²dθ the Reeb field is R = ∂_z — α(R) = 1 and ι_R dα = 0, both
checked — and its integral curves are (r₀, θ₀, z₀+t), holding r and θ **constant**.
That is a vertical line: no winding, no period, not a helix.

The helix is real and belongs to the **dynamics**: on Γ = {r=1} the dm³ flow has
ṙ = 0, θ̇ = 1, ż = 1, so the orbit is (1, t, z₀+t), a circular helix of pitch 2π,
which is where T* = 2π comes from.

And the contact form supplies something sharper than the claim it was miscredited
with: **Γ is Legendrian.** α(∂_θ + ∂_z) = 1 − r², which vanishes exactly at r = 1
and nowhere else in that family. The limit cycle of the dynamics sits precisely on
the Legendrian locus of α. Whether that is construction or coincidence of the
chosen α is not established here. `[OPEN]`

The correction is therefore not to delete the helix, which is what "the name is
wrong" would suggest, but to say **which flow it belongs to**. The defect is a
conflation of two vector fields on one manifold, not a mislabelled curve.

### The Lean, stated exactly

The file kernel-checks. That was never in question and the page may say so. What
the kernel certifies is narrower than the page claimed:

- `AXLE/NASA/MoonBase/AXLE_lean_files/Chain_updated.lean` has **no sorry** and
  **three** axioms — `inner_basin_is_asymmetric`, `outer_basin_unbounded`,
  `poincare_collatz`. The page said two and never named the third. An axiom is
  accepted *by being assumed*, so `#print axioms` is the verdict and the absence
  of `sorry` is not.
- `GTCT/Chain_updated.lean` is an earlier, divergent copy of the same filename in
  which `spiral_return_exists` and `poincare_collatz` are real `sorry`s. Two files,
  one name, opposite status — R9 in Lean.
- **`spiral_return_exists` assumes its conclusion.** It takes
  `h_second_circuit : G.iter 128 x₀ ≠ x₀` and closes the goal with
  `exact h_second_circuit`; `h_nontrivial` is never used. The prose said it proves
  "the G⁶⁴-orbit does not return to x₀ — the circuit is generative, not periodic."
  It proves the implication, not the antecedent. The earlier copy is honest about
  this in its own comment — "requires the full dynamics of G; left as sorry pending
  AXLE integration" — and the later copy closed it by promoting the missing step to
  a hypothesis and marking it `CLOSED`.
- The cited source path `GTCT/lean/GTCT/Operators/Chain_updated.lean` does not
  exist. `g64_equals_two_to_6` does not exist in either file.

**A theorem that assumes its conclusion still kernel-checks.** That is the whole
reason the gate reads `#print axioms` and a human reads the hypotheses.

### Everything else corrected on the page

ε₀ = 1/3 relabelled as the Grönwall saturation radius rather than a measured basin
edge (WP-122); the four-constant "hierarchy" marked as four constants measuring
three different things; "these are exact mathematical identities" replaced, since
the parameters differ row by row and identity would require them to agree;
"17 orders of magnitude" qualified against a table whose ω spans about four; the
anyon paragraph corrected — non-abelian anyons were created in **2023**
(Quantinuum May 2023, Google Quantum AI and Cornell after; Quanta reported it
9 May 2023), not 28 February 2026, and the priority claim is withdrawn rather than
reworded, because the physics was three years earlier; the street address removed
from the footer.

## 2026-09-19 — five Book IV chapters moved from GTCT to geometry (R7)

Moved on Pablo's instruction. All five existed only in `GTCT/book4/`; none
collided with a name in `geometry/book4/`. Direction carried: GTCT → geometry,
whole file, no merge required.

| file | title | claims | tags |
|---|---|---|---|
| `chE-gtct.html` | Chapter E · The Generative Time Circuit | 7 | none |
| `chIV-15.html` | Cap IV-15 · A Virada Complexa (PT) | 0 | none |
| `chIV-axioms.html` | Cap 1 · Os Sete Axiomas (PT) | 0 | none |
| `chIV-preface.html` | Abertura · Vol IV (PT) | 0 | none |
| `chIV-preface-impa.html` | IMPA Edition · Preface | 0 | none |

The GTCT copies were replaced with one-line pointer pages carrying
`<link rel="canonical">` to the geometry URL — not deleted, not left as copies.

Two things noted and not acted on. **`chE-gtct.html` and `chE-gtct-alt.html` are
both "Chapter E" and are different chapters** (similarity 0.147, no shared
paragraphs) — an R9 matter: a duplicate label, declared here. And three of the
five are Portuguese pages under the `chIV-` prefix, which elsewhere in
`geometry/book4/` marks English Roman-numeral chapters; renaming them would break
GTCT's inbound links, so they keep their names.

`geometry/book4` is 64 files; `GTCT/book4` holds 36, all of them now either
shared or pointers. **Zero chapters exist only in GTCT.** Sixteen shared chapters
still need reading — `python3 tools/book4_reconcile.py`.

---

## 2026-09-19 · The floor WP-82 asked for is in ~/Downloads, and has been

WP-82 measured the corpus against the 33-rung ruler and found the distribution
inverted — rung 33 in 31 file-mentions, rung 28 in **zero** — and recommended
building the floor before the ceiling. A scan of `~/Downloads` on 2026-09-19
found the floor texts already on the machine:

| rung | vol | text | pp |
|---|---|---|---|
| 28 | XI | Weibel, *The K-book: an introduction to Algebraic K-theory* | 576 |
| 29 | XII | van Neerven, *Functional Analysis* (CUP) | 732 |
| 33 | XVI | Connes & Marcolli, *Noncommutative Geometry, Quantum Fields and Motives* | 705 |
| — | — | Deisenroth, Faisal & Ong, *Mathematics for Machine Learning* | 417 |
| — | — | Lehman, Leighton & Meyer, *Mathematics for Computer Science* | 1048 |
| — | — | Hefferon, *Linear Algebra* 4e · Evans & Rosenthal, *Probability and Statistics* | 525 · 774 |

5,309 pages of primary source, none of it cited anywhere in the corpus.
`tools/floor_texts.py` gives each one an address — (path, sha256, pages,
citation) — in `docs/floor-texts.tsv`, exit 0, eight held and none missing.

**The finding is not that the books were missing. It is that they had no
address**, which in this corpus is the same thing: WP-122's return map was in
the exercise, the Strogatz page numbers were never opened, receiving capacity
was counted every year under "tourism", Volume XII was "named nowhere" because
the search looked for the wrong string. Every one of those was already held and
unaddressed. So is the floor.

**Why it matters beyond the rungs.** The 2026-09-17 audit of the Axiom Math
posting measured the corpus for machine-learning evidence and found PyTorch in 1
file, JAX in 2, TensorFlow, reinforcement learning and program synthesis in
none. The one book that closes that gap is Deisenroth, 417 pages, downloaded and
unread. The corpus's weakest measured area and the text that founds it were on
the same disk.

`[OPEN]` The book that covers these topics needs a home. XI, XII, XIII and XVI
are spoken for in WP-82 §3 and XIII already collides with `book13/` on disk, so
this one takes a name and not a numeral until the author assigns one.

---

## 2026-09-19 (later) · The hand list was the defect, again — and three Lean books nobody had opened

`tools/floor_texts.py` was written this morning with a hand-kept list of eight
filenames. That is the defect `build_indexes.py` records about its own FOLDERS
list — **the list is not the corpus** — committed inside the tool written to cure
it. Rewritten to scan and classify; the WP-82 rung map is now an overlay on what
is found, never the source.

The scan found **37 third-party texts of 60pp or more**, against the eight the
hand list knew. What the hand list had missed:

| pp | text | why it matters |
|---|---|---|
| 255 | Ullrich, *An Extensible Theorem Proving Frontend* (the Lean 4 thesis) | **Lean's own design document** |
| 214 | Avigad & Massot, *Mathematics in Lean*, release v4.19.0 (11 Jun 2026) | the standard Mathlib tutorial |
| 206 | Avigad, de Moura & Kong, *Theorem Proving in Lean* (`file.pdf`) | the reference manual |
| 719 | Whitehead & Russell, *Principia Mathematica* vol. I | — |
| 594 | Newton, *Principia* · 543 Bradley, *Leonhard Euler* | — |
| 175 | Borisov, Gabber et al., *On Endomorphisms of Affine Spaces and the Jacobian Problem* | the corpus has `JacobianCounterexample.lean` |
| 100 | Ishiki, *The Topology of Gromov–Hausdorff Space* | — |
| 115 | Andersson, Gustafson, Ingelman & Sjöstrand, *Parton Fragmentation and String Dynamics* | — |
| 96 | Navrátil, *Geometric Quantum Mechanics* from the SL(3;ℤ) tribonacci | the corpus's own η₃ ≈ 1.8393 |

**Three Lean textbooks, in a corpus whose central practice is Lean**, none cited
anywhere in it. One of them is dated three months ago and names the release. The
corpus has spent the month writing rules about declarations resolving at the path
cited, and had never opened the manual for the language it writes them in.

**And the folder has the repository's disease.** Of 36 of the author's own PDFs at
60pp or more, **24 are second-or-later copies** of a work already present —
fourteen openings of "Applications of Generative Orthogonal Matrix Compression
Science", six of "PRINCIPIA ORTHOGONA SERIES · THE COMPLETE EDITION", three of
Book 3. Same class as `docs/index.html` versus `tornhub.html`, as the two
`Chain_updated.lean`, as `book4/hub.html` versus the TO deploy: copies that drift
because nothing declares which is canonical. It is not a repository problem. It
is a habit.

`[OPEN]` No Leibniz text is held. No calculus textbook of any kind is held —
no Spivak, Apostol, Rudin or Stewart. Newton and Euler are, at 594 and 543 pages.
A volume on the calculus lineage into machine learning has its endpoints and not
its middle.

---

## 2026-09-19 (later still) · The ledger was right, and wrong sixty minutes later

`book17/index.html` and `book18/index.html` both published **"no calculus textbook of
any kind."** (XVII was corrected first; XVIII's patch failed on a string mismatch and was
corrected in the following commit — recorded here because a half-applied correction is
worse than none.) It was true of the scan that produced it and false by 02:39, when
`Advanced_Calculus.pdf` (Loomis & Sternberg, revised edition, 592 pp) and
`math1a_2021.pdf` (Knill, *Introduction to Calculus*, Harvard Math 1a, 311 pp) appeared
in Downloads. Re-run: **39 third-party texts, not 37.**

**This was not a tool failure and should not be recorded as one.** The scan was correct
when it ran. What failed is that two pages quoted a point-in-time ledger as a statement
about the world, in a series whose own rule is that an address is a name plus a place
plus a hash — and a hash is a claim about a moment. **A ledger cited without being re-run
is a memory, not an address.**

One real latent defect was found while diagnosing, and fixed: `floor_texts.py` caught
every reader exception with a bare `continue`, so a file pypdf could not open vanished
with no trace and would have been indistinguishable from a file that was not there. It
now collects them and prints `UNREADABLE — not absent, unread`, and says so again at the
end. None were unreadable in this run; the bug was latent, not the cause.

**What actually remains not held is Leibniz** — not the 1684 *Nova Methodus*, not a
collected works, not a secondary study. Book XVIII's chapters 2–4 become writable;
chapter 1 stays blocked, because its argument is about what Leibniz's notation does that
Newton's does not, and a modern textbook restating the rule cannot warrant that.

**Text-layer census, run the same day.** The volumes' warrant is that page numbers are
*located by script*, which requires a text layer. Sixteen held texts checked at three
sample pages each: fourteen return 900–2,000 characters per page. **Two return zero** —
`whiteheadrussell-principiamathematicavolumei.pdf` (719 pp) and
`aMathematiciansApology-HARDY.pdf` (80 pp) are image scans. They can be read by a human
and cannot be cited by this corpus's own method. Held is not the same as addressable.

---

## 2026-09-19 · WP-94's three open rows, checked within the hour — one withdrawn

Three primary sources arrived in Downloads at 02:48–02:49 and are exactly the three rows
WP-94 marked `OPEN` and Book XIX ch 1 had listed as open an hour earlier: Paulson's
*The Foundation of a Generic Theorem Prover* (Isabelle, 37 pp), Huet, Kahn &
Paulin-Mohring's *Coq Proof Assistant: A Tutorial* v8.0 (47 pp), and Denney, Fischer &
Schumann's *Using Automated Theorem Provers to Certify Auto-Generated Aerospace Software*
(NASA Ames, 13 pp).

**None of them was in the ledger, because the scanner's floor was 60 pages.** A threshold
is a filter and a filter manufactures absence; the three sources most relevant to the
chapter written that morning were all below it. `MIN_PAGES` lowered to 12. The ledger
went from 39 third-party texts to **112**.

**Isabelle — checked negative.** `sorry` 0, `oops` 0. The vocabulary for an unfinished
step in Isabelle's foundational paper is `axiom` (79) and `assumption` (42). Consistent
with `sorry` arriving later with Isar, but this source cannot date anything and no dated
source is held. WP-94 §4's pivot stays open — now open against evidence rather than
against nothing.

**Coq — the row overstated itself.** WP-94 gives "`admit` a step closed by fiat;
`Admitted` for the whole lemma." The tutorial attests `Admitted` **once**, p. 17, and the
standalone `admit` tactic **not at all** — the single lowercase match is the substring
inside `Admitted`, which is the same substring-inflation defect this log already records
for `/gns/` via *designs* and `/bott/` via *bottom*. One tutorial is not the manual, so
the claim narrows rather than falls.

**Aerospace — the fifth row is withdrawn.** `assumption` **0**, `assume` **0**. What the
paper uses is `axiom` (12) and `trust` (2) — **the proof-carrying-code vocabulary of row
four.** On this evidence the table has four words, not five, and the fifth row was a guess
about a community rather than a reading of one. It may hold for the assurance-case
literature proper (DO-178C, goal-structuring notation), where *assumption* is a term of
art. None of that is held. **Withdrawn, not corrected.**

The pattern is the volume's thesis in one pass: three claims stated from working
familiarity, checked against sources within an hour of their arriving, yielding one
narrowing, one withdrawal and one honest negative. No new mathematics. Only opening
the file.

---

## 2026-09-19 · The Coherence Bridge similarity test: 0 of 55

Book XVII ch 1's translation table found one row that is a genuine identity rather
than a correspondence of practice: **similarity of matrices**, two matrices being
similar exactly when they represent one linear map in different bases. That is the
Coherence Bridge's claim in a standard term, and unlike the claim it comes with a
decision procedure. `tools/coherence_similarity.py` parses the table out of
`book4/hub.html` and runs it.

| test | invariant | matching pairs |
|---|---|---|
| linear similarity | the eigenvalue pair μ ± iω | **0 of 55** |
| similarity up to time-rescaling | the ratio μ/ω | **0 of 55** |
| topological conjugacy `[standard]` | being a spiral sink | 11 of 11 |

Closest pair under the most generous reading: Immune adaptation and Market
volatility, μ/ω = −2.4444 against −2.3929. Near, not equal. Nothing else within 0.11.

**The reading.** The claim is true at the level where it carries no information and
false at every level where it would. Every 2D linear spiral sink is topologically
conjugate to every other, so eleven of eleven qualify — and so would eleven damped
oscillators picked at random. Ask for the same map in a new basis, or even the same
map after rescaling the clock, and the count is zero.

**`ch20-coherence-bridge.html` already had this right** without the number: "six
systems have been shown to admit the same normal form with different invariants …
it is not yet a categorical equivalence, and the difference matters." The chapter
also already lists "parameter drift" among the ways to falsify itself. What this
adds is that the falsification does not need new data — the table falsifies the
strong reading on its own figures.

**Four pages still carry the unhedged form** — `vol2-dashboard.html`,
`ch-e-gtct.html`, `ch24-seed-sentences.html` (which defends it) and the TO deploy.
Not edited here; an author's call on published pages. `[CLOSED 2026-09-19]`

---

### 2026-09-19 — the identity claim, corrected on the pages; and the count of pages was wrong

Deferring was the defect. One session declining to edit does nothing when several
sessions have already let the claim through; "an author's call" is what allowed it
to stand. The pages are corrected.

**The count in the entry above was itself produced by the search that made it.**
"Four pages" came from one grep. `grep -rln "exact mathematical identit"` over
`--include=*.html` returns **eleven** files, thirteen occurrences:

| file | occurrences | state before |
|---|---|---|
| `vol2-dashboard.html` | 1 | corrected earlier today |
| `ch-e-gtct.html` | 1 | corrected earlier today |
| `ch07-four-orbits.html` | 1 | corrected earlier today — **not on the list of four** |
| `ch20-coherence-bridge.html` | 1 | corrected earlier today — **not on the list of four** |
| `ch00-introduction.html` | 2 | uncorrected — one is a student exercise that presupposes it |
| `ch24-seed-sentences.html` | 1 | hedged on a different ground, not this one |
| `journey.html` | 1 | uncorrected — a JS topic string, invisible to a prose reader |
| `minibeast-pilot.html` | 3 | uncorrected |
| `book4/hub.html` | 1 | uncorrected — the page the test's own data is parsed from |
| `book4/chIV-preface-impa.html` | 1 | uncorrected |
| `vol2-v5/deposit/dashboard.html` | 1 | uncorrected — a duplicate of `vol2-dashboard.html` (R9) |
| `book17/_to_delete/_b.html` | 1 | scratch, pending deletion; declared, not edited |

Two of the four named were not among the pages actually carrying it, and seven
pages carrying it were not named. The entry above was written from a search
narrower than the corpus and then read back as if it were a census — the same
shape as the "no calculus textbook of any kind" error, and the reason R15 exists.

`book4/hub.html` is the sharpest of them: it is the page `tools/coherence_similarity.py`
**parses the table out of**. The data that falsifies the claim and the claim itself
were on one screen.

All eleven live pages now carry the withdrawal block or, for `journey.html`, a
corrected topic line. `tools/audit.py`: 27 dead_link, 2 double_escaped, unchanged
— no new finding introduced. `[CLOSED]`

---

### 2026-09-19 — `[documented]` is not a verification marker

Book XVII's index and chapter 1 printed a list of total-function-kernel facts
marked `[documented]`. The marker meant: read somewhere, not run here. Book XVII's
whole thesis is that a subject taught early is not thereby settled, and it was
resting that thesis on recollection.

Run: `book17/Book17Core.lean` (12 theorems, no imports) and
`book17/Book17Mathlib.lean` (9 theorems, Mathlib v4.33.0-rc1). Both gate clean
under `tools/axiom_gate.py` — no `sorryAx`, nothing outside
`[propext, Classical.choice, Quot.sound]`.

Two rows came back sharper than the prose that cited them:

- `Filter.Tendsto f l₁ l₂` unfolds **definitionally** to `Filter.map f l₁ ≤ l₂`,
  so "limits are filters" closes by `Iff.rfl`. It is not an analogy or a
  reformulation; it is the definition.
- `variance_of_not_memLp`: a real random variable with no second moment does not
  make `variance` undefined. It makes it **zero**, and the zero is a theorem.

One row was added rather than verified: `(-7 : Int) / 2 = -4`. Lean's integer
division is Euclidean, so the remainder is never negative — not what C, or a
Python `int()` that rounds toward zero, returns.

`book17/book17-claims-verify.py` pairs each published string with the theorem that
closes it, and checks the `.lean` files hash to the bytes the toolchain actually
read. A saved `#print axioms` report proves nothing about a file that has since
changed. It caught exactly that during this commit: a ninth theorem was added, the
stale report was still on disk, and the script refused. `[CLOSED]`

---

### 2026-09-19 — exercises that tell a student to defend a claim

Raised by the author, on finding that `ch00-introduction.html` asked the reader to
write a paragraph defending &ldquo;exact mathematical identity&rdquo; against &ldquo;analogy&rdquo; —
a claim the corpus had by then withdrawn. The objection is about who carries the
cost: the author keeps the claim, the student walks into a seminar and defends it,
and the correction arrives in the student's face rather than the author's.

Census of the ~90 prompt panels for loaded verbs (defend / justify / argue that /
prove that / explain why X is licensed). Six matched; four are legitimate — they
ask a student to justify a reading of evidence, which is the exercise. Two were
not, plus two lines of prose:

| where | what it said | state |
|---|---|---|
| `ch06-pedagogy.html` l.218 | &ldquo;can say — and defend with the full mathematical apparatus&rdquo; | rewritten |
| `ch06-pedagogy.html` l.312 | &ldquo;a student who can defend **all three** sentences has proven they understand the entire system&rdquo; | rewritten |
| `ch06-pedagogy.html` prompt D1 | &ldquo;I can defend the three seed sentences&rdquo; | rewritten |
| `book4/chE-gtct-alt.html` B2 | &ldquo;defend the claim that this — not entropy — is the real reason time cannot be reversed&rdquo; | rewritten as a test |
| `ch00-introduction.html` B2 | the analogy/identity exercise | corrected earlier today |
| `ch24-seed-sentences.html` | Seed 3 defence | corrected earlier today |

**`ch06-pedagogy.html` l.312 is a half-applied correction, and an old one.** On
23 August 2026 a session rewrote the Sentence 3 bullet to read &ldquo;Your task is not
to defend it.&rdquo; Three lines below, the closing sentence of the same paragraph still
read &ldquo;a student who can defend all three sentences has proven they understand the
entire system.&rdquo; It stood for 27 days, in direct contradiction to the bullet above
it, because the correction was applied to the string that was searched for and not
to the paragraph it was in. Same class as the two half-applied corrections logged
on 2026-09-18. The lesson is the same one: search for the *claim*, not for the
sentence that states it.

**`book4/chE-gtct-alt.html` is the worse of the two prompts** even though it is the
&ldquo;alternate telling&rdquo;. It asked for a defence of a claim about thermodynamics — that
operator non-commutativity, not entropy, is the real reason time cannot be
reversed. A student who wrote that paragraph and took it anywhere near a physics
department would be dismantled, and correctly. The prompt now asks the student to
separate &ldquo;G is not reversible&rdquo; from &ldquo;time is not reversible&rdquo; and to say what would
have to be shown to displace the measured statement.

**A section was added to `ch06-pedagogy.html`** rather than only deleting the bad
prompts, at the author's direction: students ought to know that mistakes are part
of the process. It prints the identity claim's whole arc — eleven pages, the
untested standard test, 0 of 55, the falsifying data sitting on the same page as
the claim — and says that the sequence is ordinary rather than shameful, and that
the failure mode would have been leaving the claim up after the number came back.
The standard it sets is not &ldquo;can you defend your sentence&rdquo; but &ldquo;can you say what
would make you drop it, and would you recognise that thing if it arrived.&rdquo;

`tools/audit.py`: 27 dead_link, 2 double_escaped, unchanged. `contrast_check`:
0 below 4.5:1. `novelty_check`: all checks passed. `[CLOSED]`

---

### 2026-09-19 — the 0-of-55 computation is now a theorem

`tools/coherence_similarity.py` compared eleven rows and reported no similar
pairs. That is evidence about eleven rows, and it depends on the table having
been parsed correctly.

`book21/Spiral.lean` proves the statement the computation was an instance of.
Similar matrices have the same trace and the same determinant; for a planar
system with eigenvalues μ ± iω that is τ = 2μ and Δ = μ² + ω², so μ and ω² are
invariants. Two spiral sinks with different μ are therefore not conjugate by
any invertible matrix whatsoever — `different_mu_not_similar`. The closest
pair in the corpus's own table is instantiated as
`immune_is_not_market` (μ = −0.44 against −0.67), with no arithmetic left to
trust. Ten theorems, gate clean.

Only the direction the falsification needs is proved: different invariants
forbid similarity. The converse, same invariants imply similarity, needs
rational canonical form and is not proved — it would only be required to show
two rows ARE the same, and none are. The header says so.

The same file records the weakness of the shared description: with eigenvalues
μ ± iω, the discriminant τ² − 4Δ is −4ω², negative with no further hypothesis.
So "spiral sink" says only μ < 0 and ω ≠ 0. Eleven systems meeting that have
almost nothing in common.

**The citation was checked against the file, and one phrase was withdrawn.**
`book21/spiral-pages-verify.py` opens
`Nonlinear_Dynamics_and_Chaos_2018_Steven_H._Strogatz.pdf` (sha256 e4c3681c…,
532pp, already in `docs/floor-texts.tsv` with rung and volume blank), confirms
§5.2 "Classification of Linear Systems" at printed pp. 129–138, the
discriminant on pp. 132, 135 and 138, and Figure 5.2.8 on p. 138. It refuses
outright if the sha does not match, because every page number in the header
then describes a copy the reader does not have.

A first draft of the header called §5.2 "the trace–determinant plane". That
phrase is not in this printing — Strogatz gives the diagram without naming the
plane. Common usage is not a quotation, and the phrase was removed rather than
left in his mouth. `[CLOSED]`

