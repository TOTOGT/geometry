# CLAUDE.md — totogt.github.io/geometry repo

This file primes Claude for the `~/geometry` working repo, which is the live HTML site
for the Principia Orthogona series at totogt.github.io/geometry.

Read `~/Desktop/dnls/CLAUDE.md` for the canonical house rules (filesystem map, repo table,
style guide, licensing, what agents must NOT do). This file adds geometry-specific notes.

---

---

## Handoff — read first, update last

> **Branch:** `verify-hardening`
> **Uncommitted:** none *(update this before your session ends)*
> **Open — next action, one web-editor trip:** two changes to `.github/workflows/verify-proofs.yml`. The PAT has no `workflow` scope, so both must go through github.com.
> &nbsp;&nbsp;1. **Axiom allowlist.** The gate greps for `sorryAx` only, so `FN_H_102L_phase02_cluster` passes while resting on `native_decide` — compiled code, not the kernel — inside a step named "Kernel axiom check". Permit `propext`, `Classical.choice`, `Quot.sound`; fail on anything else.
> &nbsp;&nbsp;2. **Wire `tools/terms.py --check`** in beside the vacuity scan.
> **Open — later pass:** `TERMS.md`'s 148-term baseline includes author affiliations, language tags and standard field acronyms caught by the pattern. Pruning them is cosmetic; the check works regardless.
> **Queued (2026-08-22):** V7 — L3 and cognitive limits on Lⁿ. ELTJ lexicography piece — needs the PDF and the author's angle.
> **Closed 2026-08-22:** WP71 §7's HRP figures, verified row by row against the retained specimen at `book6/sources/`. WP73 §8 and WP02 §5 written. `CLAUDE.md` split. A Google AI Overview attributed "Harmonic Resonance Bands (HRB)" and a "Log-Psi Recurrence Operator" to this corpus; neither term occurs in it, and `tools/terms.py` exists because of that.

Overwrite this block; do not append to it. The house rule that governs it is
`~/Desktop/dnls/CLAUDE.md` §9.

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


---

## Where the history went

Closed entries — `FIXED`, `RESOLVED`, `CORRECTION`, completed sweeps — live in
**[CLAUDE-ARCHIVE.md](CLAUDE-ARCHIVE.md)**. Do not read it at session start. Read it when
you need the provenance of one specific repair, and read only that section.

This file carries the rules, the open items, and the open residue of closed entries.
The split exists because this file is loaded in full at the start of every session, on
every account, and 40% of it was history that no arriving session needs.

### Archived sections

- FIXED: `book6/index.html` was hiding 16 finished pages (2026-08-17)
- FIXED: repo-wide link audit (2026-08-18)
- FIXED: §4's unsourced interval (2026-08-18)
- FIXED: `book1/index.html` was two documents in one file (2026-08-18)
- FIXED: `book1/vol2-dashboard.html` is not a dashboard (2026-08-18)
- RESOLVED: "V4" and "v6" — v6 is the current Volume I deposit
- Reachability audit, redone properly (2026-08-18)
- Orphan cleanup (2026-08-18)
- FIXED: Chapter 7 (Topological Orthogenesis) — the anyon identification (2026-08-18)
- FIXED: the map/point confusion, swept (2026-08-18)
- FIXED: `19117399` mislabelled as a series DOI (2026-08-18)
- Book II (2026-08-18)
- Book III (2026-08-18)
- ISBN registry read at last — Book IV corrected, and the registry itself has two bugs (2026-08-18)
- CORRECTION: the unit-distance exponent is 1.014, not 10⁻³⁸ (2026-08-18)
- Book V and Book III (2026-08-18)
- Storefronts relabelled as preprints (2026-08-18)
- "Edição IMPA" renamed to "Edição Brasil" (2026-08-18)
- IMPA: submitted, declined, and what they actually asked for (2026-08-18)
- RESOLVED (stale ledger entry): WP-38's "two broken formulas" (2026-08-18)
- Licensing: the IMPA claim was a mis-statement, and it exposed a real split (Aug 2026)
- The ten books audited clean — and `tools/audit.py` now exists (Aug 2026)
- The root audited clean — 614 files, whole repo (2026-08-20)

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


---

# Open items carried forward

Each of these is the unfinished part of an entry whose main body is in `CLAUDE-ARCHIVE.md`.

## FIXED: repo-wide link audit (2026-08-18)

*Context: `CLAUDE-ARCHIVE.md` → FIXED: repo-wide link audit (2026-08-18)*

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

## FIXED: `book1/index.html` was two documents in one file (2026-08-18)

*Context: `CLAUDE-ARCHIVE.md` → FIXED: `book1/index.html` was two documents in one file (2026-08-18)*

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


## RESOLVED: "V4" and "v6" — v6 is the current Volume I deposit

*Context: `CLAUDE-ARCHIVE.md` → RESOLVED: "V4" and "v6" — v6 is the current Volume I deposit*

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

## Reachability audit, redone properly (2026-08-18)

*Context: `CLAUDE-ARCHIVE.md` → Reachability audit, redone properly (2026-08-18)*

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

## Orphan cleanup (2026-08-18)

*Context: `CLAUDE-ARCHIVE.md` → Orphan cleanup (2026-08-18)*

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

## FIXED: `19117399` mislabelled as a series DOI (2026-08-18)

*Context: `CLAUDE-ARCHIVE.md` → FIXED: `19117399` mislabelled as a series DOI (2026-08-18)*

## Still open

- **The 26 formal citations.** In a reference list the string is not a label but an assertion
  that the cited work lives at that DOI, and it does not — a reader resolving it gets Vol I v6.
  These need the correct version DOI per work, or the Zenodo community link where the referent
  really is the series. Not done here.
- **`collatz-engineering_1.html` has a stray `</p>`.** Pre-existing — confirmed present in
  `HEAD` before this change — not introduced by the sweep.

## Book II (2026-08-18)

*Context: `CLAUDE-ARCHIVE.md` → Book II (2026-08-18)*

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

## Book III (2026-08-18)

*Context: `CLAUDE-ARCHIVE.md` → Book III (2026-08-18)*

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

## ISBN registry read at last — Book IV corrected, and the registry itself has two bugs (2026-08-18)

*Context: `CLAUDE-ARCHIVE.md` → ISBN registry read at last — Book IV corrected, and the registry itself has two bugs (2026-08-18)*

## OPEN — the storefront

`book4/ch02.html` and `book4/ch10.html` still price three products at **$47 with Buy on
Gumroad** under **2-5**, **4-9** and **5-6** — all three `INCOMPLETE — HOLD` in Bowker, i.e.
not registered to anything, and 4-9 is a print ISBN whose own note reads *"Activate on print"*
against a registry header saying paper books are not for sale.

Untouched deliberately. If those products are genuinely for sale the fix is to **register
ISBNs for them**, not to strip the numbers off the page; if they are not for sale, the price
and the buy button are the problem, not the ISBN. Either way it is a commercial decision.

## Storefronts relabelled as preprints (2026-08-18)

*Context: `CLAUDE-ARCHIVE.md` → Storefronts relabelled as preprints (2026-08-18)*

## OPEN — an IMPA claim to check before it matters

`book4/ch02.html`'s Vol G⁴ card reads *"GTCT T1 — The IMPA Edition … Submitted to IMPA."*
Separately, **"Edição IMPA" / "IMPA Edition" appears 209 times across 45 files**, and no
affiliation disclaimer was found anywhere in the corpus.

IMPA is a real institution with its own imprint. Used at that volume, the phrase reads as an
imprint credit rather than a description of intent or of a course edition. If the work has not
been published or endorsed by IMPA, this is the kind of thing that is cheap to correct now and
expensive later — precisely if a genuine IMPA submission is ever made. Worth one deliberate
decision about the wording, not 45 separate ones.

## RESOLVED (stale ledger entry): WP-38's "two broken formulas" (2026-08-18)

*Context: `CLAUDE-ARCHIVE.md` → RESOLVED (stale ledger entry): WP-38's "two broken formulas" (2026-08-18)*

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

## Licensing: the IMPA claim was a mis-statement, and it exposed a real split (Aug 2026)

*Context: `CLAUDE-ARCHIVE.md` → Licensing: the IMPA claim was a mis-statement, and it exposed a real split (Aug 2026)*

## Still open

`19501831` (Polylaminin) is deposited **`mit-license`** — an MIT-licensed *paper*, alongside a
`cc-by-nc-nd-4.0` sibling record (`20230633`) of the same title. One work, two deposits, two
incompatible licences. Nothing in this repo asserts either, so nothing was changed; it needs a
Zenodo-side decision by the author (rule 4).

## The ten books audited clean — and `tools/audit.py` now exists (Aug 2026)

*Context: `CLAUDE-ARCHIVE.md` → The ten books audited clean — and `tools/audit.py` now exists (Aug 2026)*

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

## The root audited clean — 614 files, whole repo (2026-08-20)

*Context: `CLAUDE-ARCHIVE.md` → The root audited clean — 614 files, whole repo (2026-08-20)*

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
