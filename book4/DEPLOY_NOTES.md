# Book 4 · Chapters 6½–9 — Deployment Notes

New files (in `Downloads/HVEH/`, alongside the seven-proofs pages):
`ch06b.html` · `ch07.html` · `ch08.html` · `ch09.html`

All four use the ch10 house style. Relative links assume these sit in the **same folder as the HVEH pages** (`index.html`, `operator-algebra.html` … `information-geometry.html`) **and** the Book 4 chapter files (`ch06.html`, `ch10.html`, `ch03.html`).

> Decision: the HVEH proof pages and the Book 4 chapter pages must live in one directory for the cross-links to resolve. If they currently live in `geometry/book4/` and `HVEH/` separately, either (a) copy the seven-proofs pages into `book4/`, or (b) copy ch06b–ch09 into the HVEH folder and adjust the `ch06.html`/`ch10.html`/`ch03.html` links to point at `book4/`. Pick one base and make the hrefs consistent before publishing.

## Arc that now exists
Ch 6 (666 · 5D+t) → **Ch 6½ El Ojo** → **Ch 7 Newark** → **Ch 8 Harrison** → **Ch 9 Belleville** → Ch 10 (proven dm³). Conjectural → proven, capped at 6D with a Vol V pointer.

## Edits needed in EXISTING files

### ch06.html (5D+t · 666)
- Footer/next-link currently → Contents. Change to **Ch 6½**: `<a href="ch06b.html">Ch 6½ · El Ojo →</a>`.

### book4 index.html / hub
- Replace the three recycled entries (Crystalline Return / Axiomatic Turn / φ) with:
  - Ch 6½ · El Ojo — The Mystery That Rotates → ch06b.html
  - Ch 7 · Map Newark — The Field and the Need → ch07.html
  - Ch 8 · Harrison — The Ordering Law Under Pressure → ch08.html
  - Ch 9 · Belleville — Verification and the Ladder's End → ch09.html
- Move the OLD ch07/ch08/ch09 (Book 3 Mini-Beast: Crystalline Return, Axiomatic Turn, φ) to the Book 3 root or an "Extended / Mini-Beast" section, under new filenames so they don't collide with the new ch07–09. They are Book 3 content (CEFR badges, Student Portal, Book 3 ISBN/DOI).

### r* = 0.773 (canonical — chosen)
Propagate everywhere; the new chapters already use 0.773. Fix:
- **ch10.html** body "r* ≈ 0.80" → 0.773; figure label "r* ≈ 0.8123" → 0.773; Lean `r_star := 0.80` → 0.773.
- **ch03.html** "r* ≈ 0.8" (×2) → 0.773.
- Anywhere the symmetric Gronwall 1/3 is described: keep ε₀ = 1/3 as the *outer* stability radius, r* ≈ 0.773 as the *inner* nonlinear boundary (the new chapters state it this way).

### Other cross-cutting (from the earlier audit, still open)
- GTCT expansion: pick one — index/hub say *Generative Temporal Contact Theory*; ch05/ch06 say *Galilean Contact Transformations*. ch10 Lean namespace says "GCTC" (typo for GTCT).
- Operator chain arity: 4-op G = U∘F∘K∘C (used in the new chapters) vs 5-op C→K→F→U→T (ch01/05/06). The new chapters use the 4-op form to match ch10 and the HVEH pages.
- ch00/ch01/ch03/ch05 still reference the old "Ch 1 = radial ODE / x*=1" and stale Ch 11/12/13/15 numbering — unchanged by this batch.

## What the new chapters deliberately do
- El Ojo framed as a **conjecture** (consistent-with, awaiting field measurement), not a claimed result — keeps the conjectural→proven honesty.
- Seven proofs introduced once in Ch 6½, then referenced by number in 7–9 (no duplication).
- Lean obligations in Ch 9 shown as honest `sorry` placeholders (AXLE Issues #14–#16), matching ch10's convention.
- Ladder explicitly capped at 6D with Vol V handoff (Ch 9 §7).
- Site data taken verbatim from `hveh_site_map_tricounty.html` (Newark 14, Belleville 8, Harrison 3 = 25).

## Not yet verified
Pixel rendering — logic was checked headlessly (markup balanced, JS syntax-valid, sim math runs), not visually. Open each in a browser to confirm the canvas sims (rotating-eye, tri-city map, commissioning fold) feel right before publishing.
