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
