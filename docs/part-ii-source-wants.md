# Part II · what the floor needs, and what is not on this machine

*Measured 2026-09-17 against `~/Downloads` (471 PDFs) and the volume table in
`book6/wp82-the-missing-floor.html`.*

---

## What is here, and which volume it serves

| Source in Downloads | Serves |
|---|---|
| `newtonprincipia.pdf` | Vol I–II lineage; the *Principia* the series is named against |
| `whiteheadrussell-principiamathematicavolumei.pdf` | Already load-bearing — WP-82's own self-reference correction cites Vol I, Introduction ch. II |
| `bradley_leonhard_euler.pdf` | Euler chapter, Vol VII |
| `Nonlinear_Dynamics_and_Chaos_2018_Steven_H._Strogatz.pdf` | Strogatz chapter, Vol VII; the dynamical spine of Vol II |
| `Helical Attractors Contact Manifolds.pdf` | This project's own dm³ study — a source *for* the corpus, not a source *to* the corpus |
| Ramanujan's Singular Moduli (Berndt, Chan & Zhang) | Done — Vol VII §VI–VII, 2026-09-17 |

## What is not here

**Rungs 28 through 33 have no books behind them at all.** A keyword scan of all
471 filenames for *k-theory, Atiyah, Singer, index theorem, Connes,
noncommutative, operator algebra, C\*, von Neumann, Murphy, Blackadar, Lurie,
higher topos, ∞-categor, derived algebraic, Toën, Weibel, homological,
Langlands, motivic, vertex algebra, W-algebra, Feigin, Frenkel, Virasoro,
moonshine, Milnor, Rosenberg, spin geometry* returns **one** hit, and it is
this corpus's own `spectral-radius.html`.

The measurement in WP-82 said the series stands on rung 33 without rung 28.
The bookshelf says the same thing independently.

---

## Volume XI · K-Theory and Index Theory — FLOOR

**Free, verified, download today:**

- **Weibel, *The K-book: An Introduction to Algebraic K-theory*** —
  `sites.math.rutgers.edu/~weibel/Kbook/Kbook.pdf`. The author's own page hosts
  the full text. This is the floor text; there is no reason not to have it.

**Must be obtained:**

- Atiyah, *K-Theory* (Benjamin 1967 / Westview) — the topological side.
- Milnor, *Introduction to Algebraic K-theory* (Annals Studies 72) — K₀, K₁, K₂
  at the length the corpus actually needs.
- Booss-Bavnbek & Bleecker, *Topology and Analysis: The Atiyah–Singer Index
  Formula and Gauge-Theoretic Physics* — the index theorem stated for people who
  came from analysis, which is where this corpus came from.
- Lawson & Michelsohn, *Spin Geometry* — if the Dirac-operator route is taken.

**The structural obstacle, already recorded.** `book13/ch-mathlib-verify.py`
notes that Mathlib has no K-theory. WP-82's admissibility bar requires each of
XI–XVI to have a machine-checked core "or it is a reading list with a DOI on
it." **Volume XI therefore cannot clear its own bar with Mathlib as it stands.**
That is the single hardest fact in Part II and it is not a book problem. Either
the core is built from scratch, or the bar is restated for XI in public.

## Volume XII · Operator Algebras — CONSOLIDATION

**Must be obtained — nothing here is free:**

- Murphy, *C\*-Algebras and Operator Theory* — the standard entry.
- Blackadar, *K-Theory for Operator Algebras* (MSRI 5) — **the bridge between XI
  and XII**, and the book that would let the two volumes be written as one arc.
- Davidson, *C\*-Algebras by Example* (Fields Monographs 6).
- Takesaki, *Theory of Operator Algebras I* — reference, not reading.

## Volume XIII · Higher Category Theory — NEW (volume exists on disk)

**Free, believed hosted by the authors — confirm before relying:**

- Lurie, *Higher Topos Theory* and *Higher Algebra* — the author's own site.
- Riehl, *Category Theory in Context* and *Categorical Homotopy Theory*.

The Lean core for XIII is Mathlib's `CategoryTheory/`, which WP-82 already
identifies as large enough that the work is instantiation rather than
construction. XIII is the volume that can actually clear the bar.

## Volume XIV · Derived Algebraic Geometry — NEW

**Free, believed available — confirm:**

- Toën & Vezzosi, *Homotopical Algebraic Geometry I & II* — arXiv.
- Gaitsgory & Rozenblyum, *A Study in Derived Algebraic Geometry* — author page.

**Must be obtained:** Weibel, *An Introduction to Homological Algebra* (CUP) —
different book from the K-book, same author, and the prerequisite for both.

## Volume XV · The W-algebra route — BRIDGE

WP-82's 2026-09-11 correction replaced the Langlands seed with vertex algebras:
Feigin–Frenkel, z(ĝ) ≅ W(ᴸg). The corpus has 7 files using "vertex operator",
5 using "Virasoro", **0 using "W-algebra"**, and `book7/ch-feigin.html` already
exists.

**Free, believed hosted by the author — confirm:**

- Frenkel, *Langlands Correspondence for Loop Groups* — Berkeley page.

**Must be obtained:**

- Frenkel & Ben-Zvi, *Vertex Algebras and Algebraic Curves* (AMS Surveys 88).
- Arakawa's survey papers on W-algebras (arXiv — free, and the shortest route in).

## Volume XVI · Noncommutative Geometry — CEILING

**Free, verified, download today:**

- **Connes & Marcolli, *Noncommutative Geometry, Quantum Fields and Motives*** —
  `alainconnes.org/wp-content/uploads/bookwebfinal-2.pdf`. Hosted by Connes.

**Must be obtained:**

- Connes, *Noncommutative Geometry* (Academic Press 1994) — the 1994 book is the
  one the corpus's 31 file-mentions are actually gesturing at. Internet Archive
  has a lending copy; it is not a free PDF.
- Gracia-Bondía, Várilly & Figueroa, *Elements of Noncommutative Geometry*.
- Khalkhali, *Basic Noncommutative Geometry* (EMS) — the short one.

---

## The two to fetch first

Weibel's K-book and the Connes–Marcolli volume. Both are free, both are hosted
by their authors, and between them they are the floor and the ceiling of Part II.
Everything else on this list can wait behind them.

## The one to decide first

Whether Volume XI is written without a Lean core and says so, or waits. WP-82
set that bar in public. Nothing on this list changes it.
