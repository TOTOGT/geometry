# CLAUDE.md — totogt.github.io/geometry repo

This file primes Claude for the `~/geometry` working repo, which is the live HTML site
for the Principia Orthogona series at totogt.github.io/geometry.

Read `~/Desktop/dnls/CLAUDE.md` for the canonical house rules (filesystem map, repo table,
style guide, licensing, what agents must NOT do). This file adds geometry-specific notes.

---

## Series ISBN & format map

| Volume | Title | Format | ISBN |
|--------|-------|--------|------|
| G1 · Vol I | GOMC Science | Print + eBook | 979-8-9954416-0-1 (print) · 979-8-9954416-1-8 (eBook) |
| G2 · Vol II | TOGT | Print + eBook | — |
| G3 · Vol III | The Mini-Beast | **eBook ONLY** | 979-8-9954416-6-3 (eBook PDF) |
| G4 · Vol IV | GTCT Dimensional Theory | — (no ISBN yet) | use G5 eBook ISBN as fallback |
| G5 · Vol V | Complete Completeness · The Seed | Print + eBook | 979-8-9954416-0-1 (paperback, registered) · 979-8-9954416-1-8 (eBook) · 979-8-9954416-4-9 (hardback ≤666pp, reserved) |

**Critical rules:**
- Book 3 (Vol III, The Mini-Beast) is **eBook only**. Never add a print ISBN to it.
  Never list it as available in print. It is a living document, updated as the pilot expands.
- If a volume does not have its own ISBN assigned yet (e.g. Vol VI), use the
  **G5 Complete Completeness eBook ISBN 979-8-9954416-5-6** as the canonical fallback.
  G5 is all-encompassing — it adds what comes out by default.
- Series root DOI: **10.5281/zenodo.19117399** — use this for cross-volume citations.
- Vol I individual DOI: 10.5281/zenodo.19117400

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

## What NOT to do

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
| `ALGEBRAIC_PROOFS_D1_RIBOSWITCH.md` | §D1 derivation (D1 domain) | NO |
| `ch18-zeolite-noncommutativity.html` | §18.2 Thm 18.1 (D2 domain) — states the δ formula as *"the Mini-Beast's central commutator, applied across every domain so far in this book"* | NO |
| `ALGEBRAIC_PROOFS_CH7_CRYSTALLINE_RETURN.md` | Ch7-T1 Step 5 (Saturn hexagon / D₆) | **YES — 2026-07-20.** Step 5's false radial-gate claim replaced by the correct 3-part statement; 5 new theorems kernel-verified in `SaturnHexagon.lean` (Lean v4.14.0, axioms clean) including the D₆-specific `rot_commutes_coupling` and `hex_coupling_uniform`. Steps 1–4 and the D₆ conclusion untouched. |
| `zeolite_operator_selectivity_v2.tex` (in `TOTOGT/io`) | Theorem 1 | **YES → v3, 2026-07-18** |

**Cluster 1 is concentrated in Book 3 (The Mini-Beast) — its D1–D4 domain
chapters lean on this as their central claim.** Book 3 is eBook-only and an
explicitly living document (see ISBN map above), so it can be revised without a
print run. That makes it the cheapest cluster to repair and the most urgent, since
it is the one that presents the lemma as the book's spine.

### Cluster 2 — INHERITORS. Cite chain-level 5.3 only; probably fine, verify once each.
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
| `ALGEBRAIC_PROOFS_ALL_7_THEOREMS.md` | **Stale duplicate.** Superseded in `TOTOGT/io` by `OPERATOR_ORDER_DERIVATIONS_AND_STATUS.md`. Per the no-duplicates rule: **delete, do not edit.** |
| `HVEH/distribution-theory.html` + `HVEH/proofs/distribution-theory.html` | Same content, two paths — one repair, applied twice |
| `HVEH/ch06b.html` | asserts the δ |
| `book4/ch06b.html` + `book4/ch06b-elojo.html` | Same content, two paths |

So ~5 unique documents remain, not 70.

### Cluster 4 — BACKGROUND. 47 files match non-commutativity vocabulary only.
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
