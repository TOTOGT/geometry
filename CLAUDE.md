# CLAUDE.md — totogt.github.io/geometry repo

This file primes Claude for the `~/geometry` working repo, which is the live HTML site
for the Principia Orthogona series at totogt.github.io/geometry.

Read `~/Desktop/dnls/CLAUDE.md` for the canonical house rules (filesystem map, repo table,
style guide, licensing, what agents must NOT do). This file adds geometry-specific notes.

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

## What NOT to do

- Do not hand-edit `master-index.html` or `index-*.html` — regenerate them
- Do not add a print ISBN to Book 3 / Vol III pages
- Do not create a `book5/` directory without user instruction
- Do not merge or deduplicate the shadow pages (ch7-topological-orthogenesis.html,
  ch8-nested-infinities.html) — they are intentional alternate editions
- Do not mark AXLE theorems as "✓ Lean 4" without the "(under SH)" caveat
  if they depend on the Structural Hypothesis (SH)
- Do not use Cormorant Garamond in book4 pages — it has no math glyph coverage

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
5. **Never wholesale-replace a working file** to fix this. Minimal edit to the
   specific lemma, then update the ledger above in the same session.
6. **Update this ledger** when you settle a file — mark it fixed, or move it out
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
