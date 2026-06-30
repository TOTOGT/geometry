# Series Audit — Promises vs Delivery
**Date:** 2026-06-30  
**Scope:** series-hub.html vol cards vs actual book folder contents + promised chapters not yet built

---

## CURRENT MISMATCHES (need fixing now or soon)

### Vol VI card — WRONG/INCOMPLETE
- **Series-hub says:** "Explicit Operators — E₈ Dynkin = G-chain · 240 roots · Sorry-free Aᵢ matrices" · status "Planned" / "In development" · NO link to book6/
- **book6/ actually is:** "G⁶ · Vol VI · Roots — io, not oi · J² = -id · E₈ · 12 bio-domain proofs · Self-organization · IP & transport tech · 23 chapters" · LIVE
- **Fix:** Update Vol VI card → status Live, title "Roots — io, not oi", link to book6/index.html
- **Gap:** The "23 chapters" in book6/index.html are mostly root-level files linked as ../fileName.html — they live in Book 3 (geometry root) not in book6/. Need decision: move them into book6/ or keep as cross-volume links?

### Vol V card — FIXED today
- Was: ℍ→𝕆 / Dimensional Theory / links to book4/ch01.html
- Now: G⁵ / The Seed — Complete Completeness / links to book5/index.html ✓

### Book 5 card missing chapter links
- Vol V card only shows: book5/index.html + book5/chV-sorrys.html
- **Existing chapters not linked from series-hub:**
  - book5/ch00.html — Preâmbulo (the seed proof)
  - book5/chV-preface.html — Prefácio
  - book5/chV-banach.html — Banach Fixed-Point Theorem
  - book5/chV-constants.html — 8 Verified Constants
  - book5/chV-g6.html — O Horizonte Aberto (G⁶ conjecture)
  - book5/chV-axle.html — AXLE Engine
  - book5/chV-seed.html — The Seed

### "Dimensional Theory / ℍ→𝕆" — ORPHANED
- This was the OLD Vol V description (quaternionic/octonionic dm³, non-commutative/non-associative turn)
- Source: GTCT_Vol5_v8_FinalSubmission.docx
- No book folder exists for it
- It's now GONE from the series-hub after Vol V fix
- Decision needed: does it become a "Bridge" card between V and VI? Or an additional volume?

---

## PROMISES IN BOOK FOLDERS NOT YET DELIVERED

### book6/index.html — 23 Chapters Promised, ~6 Exist
book6/index.html lists these chapters as links. Most resolve to root-level or external files:
- ✓ hidden-track-punk-edu.html (in book6/)
- ✓ g6-crystal.html (in book6/)
- ✓ on-publication.html (in book6/)
- ✓ doi links (Zenodo — external)
- ✓ ../chPHI-rh.html (root-level, exists)
- ✓ ../chPI-rh.html (root-level, exists)
- ✓ ../vol2-toymodel.html (root-level, exists)
- ✓ ../spectral-radius-v2.html (root-level, exists)
- ✓ ../Enceladus.html (root-level, exists)
- ✓ ../gcm-framework.html (root-level, exists)
- ✓ ../law3m-brief.html (root-level, exists)
- ✓ ../../banking-butterfly-preprint.html (root-level, one level up, exists)
- ✓ ../emmes-whitepaper.html (root-level, exists)
- ✗ ../../AXLE/GameTheory_Full_Pack.html — MISSING (out of geometry folder)
- ✗ ../../AXLE/lexical-generativity-ijl.html — MISSING (out of geometry folder)

**Chapters PROMISED in book6/index.html description but NOT YET BUILT:**
"12 bio-domain proofs" → none exist yet in book6/ as dedicated HTML chapters
These would need new files: chVI-biology-1 through chVI-biology-12 (or equivalent)

### book7/index.html — 13 Scientists Added as Stubs Today
Stubs created (basic, need prose): ch-noether, ch-dyson, ch-mirzakhani, ch-kovalevskaya,
ch-katherine-johnson, ch-turing, ch-hopfield, ch-waddington, ch-victora-nussenzweig,
ch-klein-thymus, ch-mitchison-kirschner, ch-bak, ch-thom

Full chapters (with real prose): ch-ada, ch-curie, ch-dirac, ch-escher, ch-faraday,
ch-hawking, ch-lattes, ch-ramanujan, ch-tatiana, ch-thoreau

### book8/index.html — Chapters promised that may be stubs
Need to verify: ch10-thermodynamics, ch11-cymatic, ch12-container, ch13-holology are
built but may be stubs.

---

## VOL CARD DESCRIPTION vs ACTUAL CONTENT — FULL TABLE

| Vol | Badge | Card Title | Card Status | Actual Folder | Actual Status | Match? |
|-----|-------|-----------|------------|---------------|---------------|--------|
| I | ℝ | GOMC — Operator Algebra | Published | vol1-mathematics.html + gomc-opus.html | ✓ | OK |
| II | ℝ² | TOGT — Contact Geometry | Published | vol2-contact.html | ✓ | OK |
| III | ℝ³ | The Mini-Beast | Living | geometry root (index.html) | ✓ | OK |
| IV | ℂ | GTCT — Formal Theory | Published | book4/ | ✓ | OK |
| V | G⁵ | The Seed | Live | book5/ | ✓ | FIXED |
| Bridge | log | Logs Segment | Planned | NONE | planned | OK (gap noted) |
| VI | E₈ | Explicit Operators | Planned | book6/ EXISTS | LIVE | ⚠ WRONG |
| VII | M | Scientist Gallery | Live | book7/ | ✓ | OK |
| VIII | 𝕄 | The Monster | Live | book8/ | ✓ | OK |
| IX | Ω | Omega Point | Live | omega/ | ✓ | OK |
| — | ℍ→𝕆 | Dimensional Theory | — | NONE | ORPHANED | ⚠ NEEDS DECISION |

---

## CHAPTERS TO BUILD (to make promises whole)

### HIGH PRIORITY
1. **Vol VI card** — fix series-hub to say Live, link book6/index.html
2. **ℍ→𝕆 Dimensional Theory bridge** — decide: add as a "Bridge V→VI" card? or new Vol?
3. **12 bio-domain chapters for book6** — the E₈ × biology instantiation chapters (book6/chVI-biology-*.html)

### MEDIUM PRIORITY  
4. **Book 5 card** — add all 7 chapter links to the series-hub Vol V card
5. **book7 stubs → prose** — 13 scientist stubs need real content (Noether, Turing, Hopfield etc.)
6. **book6/chVI-axle6.html** — was referenced in g6-crystal.html broken links, still needs creating

### LOW PRIORITY
7. **AXLE/GameTheory_Full_Pack.html** — referenced in book6 but lives outside geometry/
8. **AXLE/lexical-generativity-ijl.html** — same

---

## AUDIT TRAIL
- Link audit June 30: 233 broken → 21 remaining (HVEH + book/ separate projects + 1 PT version)
- Theorem count convergence June 30: 160+ → 1,080 (Project 1080, June 22 2026)
- Book 5 stale sorry count June 30: 9 → 0
- Vol V series-hub card June 30: wrong book → corrected
