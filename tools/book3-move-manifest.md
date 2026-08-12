# Book 3 — root → `book3/` move manifest

**Status: PROPOSAL. Nothing has been moved.** Generated 2026-08-12.

## The blocking finding: this repo has three different answers to "what is Book 3"

| source | what it is | root files listed |
|---|---|---:|
| `chapters-diagram.html` | titled **"All Chapters · Book 3: The Mini-Beast"** | 102 |
| `journey.html` | **"Student Journey Map · Book 3 · 42 chapters"** | 53 |
| marker grep | `Book 3`/`Vol III`/`Mini-Beast` in the first 4 KB | 85 |

**All three agree on 16 files.** The union of the two hand-built rosters is
130 — nearly half of root's 283 files.

Neither roster can arbitrate, because each is demonstrably incomplete:

- `journey.html` names **28 files that "All Chapters" omits**, including
  `ch03-operator-sequence.html`, `ch04-kappa-star.html`, `ch05-contact-normal-form.html`
  — core operator chapters. So "All Chapters" is not all chapters.
- `journey.html`'s own title says **42 chapters**; it references 53. The count is
  a stale derived fact, the same failure mode as the ISBN table and the Vol IV footer.
- The grep catches any Book 4 or Book 6 page that merely *cites* Book 3.

**Recommendation: fix the roster before moving anything.** A move keyed to a list that is
itself wrong will scatter Book 3 across two folders and leave the rosters pointing at dead
paths — strictly worse than the current state. Decide the roster, write it down once, then
move.

## Cost, once the roster is settled

| | 3-source core | union of rosters |
|---|---:|---:|
| files moved | 16 | 130 |
| internal links to rewrite | 291 | 1174 |
| absolute `totogt.github.io/…` cites broken | 10 | 26 |

The external cost cannot be measured from inside the repo. Book 3 is the **only actively
distributed product** (`isbn_metadata.json`: 979-8-9954416-6-3, "register now"). Its eBook
and any shared link point at current root URLs; moving 404s them unless redirect stubs stay.

`CLAUDE.md` documents the present layout as deliberate — *"`geometry/` root = Book 3 (G3)
chapters, prelude, overture, portals"* — so that line must change in the same commit.

Legend: **D** = in chapters-diagram · **J** = in journey · **G** = matched the grep.

## Tier A — all three sources (16) · move with confidence

| file | in | inbound | title |
|---|---|---:|---|
| `ch00-student-edition.html` | DJG | 3 | Ch 0 · Student Edition — How to Read This Book · Principia Orthogona B |
| `ch01-dm3-framework.html` | DJG | 6 | Ch. 1 — The dm³ Framework: A Review | The Mini-Beast |
| `ch02-biological.html` | DJG | 5 | Ch. 2 — Biological Instantiations | The Mini-Beast |
| `ch03-plasma.html` | DJG | 4 | Ch 3: Plasma-Sheet Reconnection — The Mini-Beast |
| `ch04-markets.html` | DJG | 7 | Ch 4: Market Volatility Manifolds — The Mini-Beast |
| `ch06-pedagogy.html` | DJG | 4 | Chapter 6: Pedagogy — The Mini-Beast: Principia Orthogona Book 3 |
| `ch10-lyapunov.html` | DJG | 25 | Chapter 10 — Lyapunov | Book 3: The Mini-Beast |
| `ch11-spectral.html` | DJG | 23 | Ch11 · Spectral Radius — The Reach of Unfolding · Book 3 |
| `ch12-conclusion.html` | DJG | 21 | Ch12 · Fixed Point — The Conclusion as Attractor · Book 3 |
| `ch13-revision.html` | DJG | 15 | Ch13 · The Nirvana Machine — Revision as Annealing · Book 3 |
| `ch14-axle.html` | DJG | 20 | Ch14 · AXLE — The Sorry-Free Paper · Book 3 |
| `ch2-allostatic.html` | DJG | 4 | Ch.2 · Allostatic Load · Book 3: The Mini-Beast · G6 LLC |
| `ch3-circadian.html` | DJG | 30 | Chapter 3 — Circadian Regulation | Book 3: The Mini-Beast |
| `ch4-neural.html` | DJG | 27 | Chapter 4 — Neural Oscillations | Book 3: The Mini-Beast |
| `ch6-resonance.html` | DJG | 25 | Chapter 6 — Resonance | Book 3: The Mini-Beast |
| `chPI-recurrence.html` | DJG | 72 | Greek Series: The Recurrence Ladder — The Mini-Beast: Principia Orthog |

## Tier B — both rosters, grep missed (9) · almost certainly Book 3

| file | in | inbound | title |
|---|---|---:|---|
| `ch-d2-academic.html` | DJ | 9 | Chapter D2 · Evolutionary Epistemology and the Limits of Formalism · P |
| `ch01-one-equation.html` | DJ | 4 | Chapter 1 — One Shape, Three Origins | Principia Orthogona |
| `ch1-seed.html` | DJ | 6 | Chapter 1 — One Shape, Many Infinities | Principia Orthogona |
| `ch7-crystalline.html` | DJ | 30 | Chapter 7 · The Crystalline Return · Principia Orthogona |
| `ch8-axiomatic.html` | DJ | 19 | Chapter 8 · The Axiomatic Turn · Principia Orthogona |
| `chDelta-tetranacci.html` | DJ | 17 | Δ · Tetranacci | dm³ — The Recurrence Ladder |
| `chEta-tribonacci.html` | DJ | 23 | η · Tribonacci | dm³ — The Recurrence Ladder |
| `chOmega-hexabonacci.html` | DJ | 76 | Ω · Hexabonacci | dm³ — The Recurrence Ladder |
| `chSigma-pentanacci.html` | DJ | 15 | Σ · Pentanacci | dm³ — The Recurrence Ladder |

## Tier C — diagram + grep, off the journey path (29)

| file | in | inbound | title |
|---|---|---:|---|
| `capitulo-e-gtct-pt.html` | DG | 2 | Capítulo E · O Circuito Temporal Generativo — O Mini-Beast · Principia |
| `capitulo-e-gtct.html` | DG | 4 | Capítulo E · O Circuito Temporal Generativo — O Mini-Beast · Principia |
| `ch-e-gtct.html` | DG | 9 | Chapter E · The Generative Time Circuit — The Mini-Beast · Principia O |
| `ch-t-tubulin.html` | DG | 1 | Chapter T · Tubulin as Computronium · Principia Orthogona |
| `ch-t-tubulina.html` | DG | 3 | Chapter T · Tubulin as Computronium · Principia Orthogona |
| `ch00-introduction.html` | DG | 3 | Ch. 0 — Introduction: One Equation, Many Rooms | The Mini-Beast |
| `ch1.html` | DG | 28 | Chapter 1 — The Cajueiro Principle | Book 3: The Mini-Beast |
| `ch15-entropy.html` | DG | 17 | Ch15 · H — Entropy and the Compression Circle · Book 3 |
| `ch16-scale.html` | DG | 5 | Ch 16 · Scale Invariance — Book 3: The Mini-Beast |
| `ch17-epilogue.html` | DG | 10 | Ch 17 · Epilogue — Book 3: The Mini-Beast |
| `ch2.html` | DG | 22 | Chapter 2 — Generative Matrix | Book 3: The Mini-Beast |
| `ch5-immune.html` | DG | 36 | Chapter 5 — Immune Adaptation | Book 3: The Mini-Beast |
| `ch6-resonant.html` | DG | 6 | Chapter 6 · The Resonant Chamber · Book 3 |
| `ch7-topological-orthogenesis.html` | DG | 10 | Chapter 7 — Topological Orthogenesis | Book 3: The Mini-Beast |
| `ch8-nested-infinities.html` | DG | 9 | Chapter 8 — Nested Infinities | Book 3: The Mini-Beast |
| `ch9-phi.html` | DG | 92 | Chapter 9 — φ · The Subcritical Approach | Book 3: The Mini-Beast |
| `chE-gtct.html` | DG | 15 | Chapter E · The Generative Time Circuit — The Mini-Beast · Principia O |
| `chLambda-polylaminin.html` | DG | 20 | Chapter Λ · Protein Shape Transformations — The Mini-Beast · Principia |
| `chT-tubulin.html` | DG | 89 | Chapter T · Tubulin as Computronium · Principia Orthogona |
| `chW-wigner.html` | DG | 34 | Chapter W: The Wigner Crystal — The Mini-Beast: Principia Orthogona Bo |
| `chapters-pi-phi-mu-eta-delta-sigma-omega.html` | DG | 3 | Principia Orthogona · Book 3 · Chapters π φ μ η Δ Σ Ω |
| `fractal-index.html` | DG | 1 | dm³ Generative Attractor — Principia Orthogona |
| `labyrinth.html` | DG | 1 | The Labyrinth · Principia Orthogona · Book 3 |
| `livro3-brasil.html` | DG | 4 | The Mini-Beast · Livro 3 · Principia Orthogona · Para o Brasil |
| `minibeast-pilot.html` | DG | 1 | The Mini-Beast · Principia Orthogona · Book 3 |
| `prelude.html` | DG | 14 | Prelude | Book 3: The Mini-Beast |
| `spectral-radius-v2.html` | DG | 4 | Spectral Radius Asymptotics — Transfer Operator · Book 3 Collatz Suppl |
| `spectral-radius.html` | DG | 8 | Spectral Radius Asymptotics — Transfer Operator · Book 3 Collatz Suppl |
| `wigner-fractal.html` | DG | 2 | Wigner Crystal — dm³ Fold Diagram · Book 3 |

## Tier D — diagram only (48) · review

| file | in | inbound | title |
|---|---|---:|---|
| `229-ballantine.html` | D | 0 | 229 Ballantine · Newark Wellness Soundworks · G6 LLC |
| `GTCT_V_Student_Edition.html` | D | 0 | Principia Orthogona V — Student Edition | Edição do Estudante |
| `Sportal.html` | D | 0 | Student Portal — Principia Orthogona · A1 → D2 |
| `access-required.html` | D | 0 | Chapter Access · dm³ Research Lab |
| `berimbau_cymatics.html` | D | 0 | Berimbau Machine — Cymatics | GTCT Volume V |
| `ch-d2-parashurama.html` | D | 0 | Chapter D2 · The Paraśurāma Hinge · Philosophy of Internal Transformat |
| `ch01-cajueiro.html` | D | 0 | We Perceive the Unfolding First — The Cajueiro Principle | English for |
| `ch02-reading.html` | D | 0 | Compressing the Abstract — Scientific Reading at the Threshold | Engli |
| `ch03-sources.html` | D | 0 | Source Mapping — Citations, DOIs, and the Literature Chain | English f |
| `ch04-milestone1.html` | D | 0 | Paper 1 — Your First Zenodo Publication | English for Researchers |
| `ch05-neural-coherence.html` | D | 0 | Chapter 5: Neural Coherence | dm³ |
| `ch05-oscillations.html` | D | 0 | Chapter 5: Neural Oscillations | English for Researchers C1→D2 |
| `ch06-argument.html` | D | 0 | Chapter 6: Argument Architecture | English for Researchers C1→D2 |
| `ch07-bridge.html` | D | 0 | Chapter 7: Bridge | dm³ |
| `ch7-circuito-completo.html` | D | 0 | Capítulo 7: Circuito Completo | dm³ |
| `ch7-complete-circuit.html` | D | 0 | Chapter 7: Complete Circuit | dm³ |
| `ch8-meru.html` | D | 0 | Chapter 8 · The Mountain and the Serpent · Principia Orthogona |
| `chMu-lyapunov.html` | D | 0 | μ · Chaos Theory | dm³ — The Lyapunov Operator |
| `chPsi-quantum-mind.html` | D | 0 | Ch Ψ · Quantum Gravity · Mind · dm³ |
| `chRho-spectral.html` | D | 0 | ρ · Spectral Radius · Collatz · RH Surgery — Principia Orthogona |
| `course-16weeks.html` | D | 0 | English for Researchers — C1 to D2 · 16-Week Program |
| `dm3-lab-index.html` | D | 0 | Helical Attractors on Contact 3-Manifolds · Principia Orthogona Vol. I |
| `g6-drone-machine.html` | D | 0 | G6 Drone Machine · Newark Wellness Soundworks |
| `guru-puja.html` | D | 0 | Pratyaksha Pada Puja · Sri Brodananda · Principia Orthogona · G6 LLC |
| `hal-saflieni-resonance.html` | D | 0 | Ħal Saflieni Temple Resonance · Newark Wellness Soundworks |
| `helical-attractor.html` | D | 0 | Redirecting... |
| `hypogeum_temple_resonance.html` | D | 0 | Ħal Saflieni Temple Resonance · Newark Wellness Soundworks |
| `impa-portal.html` | D | 0 | dm³ Soundworks · Chladni · Sacred Resonance · G6 LLC |
| `newark-wellness.html` | D | 0 | Newark Wellness Center · G6 LLC · Forest Hill |
| `om-machine.html` | D | 0 | Om Machine · Newark Wellness Soundworks |
| `portal.html` | D | 0 | Student Portal — Principia Orthogona · A1 → D2 |
| `pranayama-machine.html` | D | 0 | Pranayama Machine · Newark Wellness Soundworks |
| `series-layer-map.html` | D | 0 | Series Layer Map · Principia Orthogona · G6 LLC |
| `sessao1-geometria-contato.html` | D | 0 | Sessão S1 · Geometria de Contato & o Sistema dm³ · Mini-Curso Vol. IV |
| `sessao2-teorema-bacia.html` | D | 0 | Sessão S2 · Teorema 2.1 & a Bacia Assimétrica · Mini-Curso Vol. IV |
| `sessao3-esqueleto-lean.html` | D | 0 | Sessão S3 · Esqueleto Lean 4 & AXLE Issue #12 · Mini-Curso Vol. IV |
| `session1-contact-geometry.html` | D | 0 | Redirecting... |
| `session2-theorem-basin.html` | D | 0 | Redirecting... |
| `session3-lean-skeleton.html` | D | 0 | Redirecting... |
| `sim-lyapunov.html` | D | 0 | Lyapunov Exponent — Syracuse Return Map |
| `sim-stormmanifold.html` | D | 0 | StormManifold — AXLE SIM |
| `sim.html` | D | 0 | AXLE Simulator — Operator Mode |
| `soham-machine.html` | D | 0 | So-Haṃ Machine · Newark Wellness Soundworks |
| `sri-yantra-sakti-machine.html` | D | 0 | Śrī Yantra Śakti Machine · Newark Wellness Soundworks |
| `swarnakarshana-bhairava-machine.html` | D | 0 | Swarnakarshana Bhairava Machine · Newark Wellness Soundworks |
| `trilogy-sale.html` | D | 0 | Principia Orthogona — Pre‑Print Trilogy · Direct from the Author |
| `wellness-soundworks.html` | D | 0 | Newark Wellness Soundworks · G6 LLC |
| `yuga6.html` | D | 0 | Yuga 6 · Yoga-ESL · The Origin · Principia Orthogona · G6 LLC |

## Tier E — journey only, absent from "All Chapters" (28) · roster gap

These are the files that prove "All Chapters" is incomplete. Fix the roster here first.

| file | in | inbound | title |
|---|---|---:|---|
| `about-author.html` | JG | 2 | About the Author | Book 3: The Mini-Beast | Principia Orthogona |
| `about-series.html` | JG | 1 | About the Series | Book 3: The Mini-Beast | Principia Orthogona |
| `ch-eta-dnls.html` | JG | 16 | Chapter η · Tribonacci as Critical Constant · Principia Orthogona |
| `ch03-operator-sequence.html` | JG | 1 | The Operator Sequence | Book 3: The Mini-Beast | Principia Orthogona |
| `ch04-kappa-star.html` | JG | 2 | The Critical Curvature Threshold κ* | Book 3: The Mini-Beast | Princip |
| `ch05-contact-normal-form.html` | JG | 1 | The dm³ System & Contact Normal Form | Book 3: The Mini-Beast | Princi |
| `ch07-four-orbits.html` | JG | 0 | The Four Biological Orbits | Book 3: The Mini-Beast | Principia Orthog |
| `ch09-plasma-metric.html` | JG | 1 | Plasma · The Manifold and Metric | Book 3: The Mini-Beast | Principia  |
| `ch10-plasma-xpoint.html` | JG | 2 | Plasma · Critical Curvature at the X-Point | Book 3: The Mini-Beast |  |
| `ch11-plasma-transition.html` | JG | 1 | Plasma · The Generative Transition | Book 3: The Mini-Beast | Principi |
| `ch13-market-metric.html` | JG | 1 | Market · The Manifold and Metric | Book 3: The Mini-Beast | Principia  |
| `ch14-market-threshold.html` | JG | 2 | Market · Critical Volatility Threshold | Book 3: The Mini-Beast | Prin |
| `ch15-market-transition.html` | JG | 2 | Market · The Generative Transition | Book 3: The Mini-Beast | Principi |
| `ch16-neural.html` | JG | 2 | Neural Embedding Geometry | Book 3: The Mini-Beast | Principia Orthogo |
| `ch17-neural-metric.html` | JG | 2 | Neural · The Manifold and Metric | Book 3: The Mini-Beast | Principia  |
| `ch18-neural-curvature.html` | JG | 2 | Neural · Critical Curvature in Phase Space | Book 3: The Mini-Beast |  |
| `ch19-neural-transition.html` | JG | 2 | Neural · The Generative Transition | Book 3: The Mini-Beast | Principi |
| `ch20-coherence-bridge.html` | JG | 1 | The Coherence Bridge Theorem | Book 3: The Mini-Beast | Principia Orth |
| `ch22-correspondence.html` | JG | 1 | The Correspondence | Book 3: The Mini-Beast | Principia Orthogona |
| `ch23-14-week.html` | JG | 2 | The 14-Week Structure | Book 3: The Mini-Beast | Principia Orthogona |
| `ch24-seed-sentences.html` | JG | 1 | The Three Seed Sentences | Book 3: The Mini-Beast | Principia Orthogon |
| `ch41-first-publication.html` | JG | 1 | After Pass 3 · Your First Publication | Book 3: The Mini-Beast | Princ |
| `chH-collatz.html` | JG | 11 | Ch.H · Collatz as dm³ Corollary · Book 3: The Mini-Beast · G6 LLC |
| `course-dm3-101.html` | J | 51 | dm³ 101 — Foundations · Principia Orthogona |
| `course-dm3-102.html` | J | 70 | dm³ 102 — Middle Operators · Principia Orthogona |
| `course-dm3-103.html` | J | 53 | dm³ 103 — The Omega Point · Principia Orthogona |
| `wk02-compression.html` | JG | 0 | Week 2 · Compression | Book 3: The Mini-Beast | Principia Orthogona |
| `wk06-threshold.html` | JG | 0 | Week 6 · Threshold Crossing | Book 3: The Mini-Beast | Principia Ortho |

## Tier F — grep only, on no roster (15) · expect false positives

| file | in | inbound | title |
|---|---|---:|---|
| `ch-flame.html` | G | 3 | Chapter Flame: The Geometry of Fire — The Mini-Beast: Principia Orthog |
| `ch-ocio.html` | G | 9 | Ch. Ocio · The Law of Monsters · Book 3: The Mini-Beast · G6 LLC |
| `ch-recurrence-ladder.html` | G | 3 | Principia Orthogona · Book 3 · Chapters π φ μ η Δ Σ Ω |
| `ch18-zeolite-noncommutativity.html` | G | 4 | Ch 18 · Non-Commutativity — Zeolite to the Stars — Book 3: The Mini-Be |
| `ch19-enzyme-noncommutativity.html` | G | 3 | Ch 19 · Non-Commutativity — The Active Site Remembers Order — Book 3:  |
| `ch20-saf-noncommutativity.html` | G | 2 | Ch 20 · Non-Commutativity — The Bridge Domain — Book 3: The Mini-Beast |
| `ch3c-econophysics.html` | G | 12 | Chapter 3c · The Circadian Trader · Book 3: The Mini-Beast · Principia |
| `ch6b-cardiac.html` | G | 3 | Chapter 6b — Cardiac | Book 3: The Mini-Beast |
| `ch7-kitagawa.html` | G | 1 | Chapter 7: Susumu Kitagawa — From Beauty to Molecular Design · Book 3 |
| `chapters-diagram.html` | G | 61 | All Chapters · Book 3: The Mini-Beast · Principia Orthogona |
| `classroom-index.html` | G | 3 | Book 3 Classroom · The Mini-Beast · Principia Orthogona |
| `journey.html` | G | 12 | Student Journey Map · Book 3: The Mini-Beast · 42 chapters · 6 passes  |
| `living-book.html` | G | 300 | Principia Orthogona · Book 3 · Living Book |
| `overture.html` | G | 3 | Overture · Principia Orthogona · Vol. III · G6 LLC |
| `vol3-minibeast.html` | G | 4 | The Mini-Beast · Vol III · Principia Orthogona |

## Procedure, once you cut the list

1. Correct `chapters-diagram.html` and `journey.html` so they agree, and fix journey's
   "42 chapters" title to the real count.
2. `git mv` the approved files to `book3/`.
3. Rewrite internal links by **path resolution, never basename** — `ch6-resonance.html`
   and `ch-tatiana.html` each exist twice (see `CLAUDE.md`).
4. Leave a redirect stub at each old root path so the eBook and external links survive.
5. Rewrite the affected absolute `totogt.github.io/geometry/…` citations.
6. Update `CLAUDE.md`'s site-structure section in the same commit.
7. Re-run `python3 tools/build_indexes.py`; confirm orphans did not rise.
8. Spot-check moved pages render, then push.

Steps 2–7 are mechanical and scriptable. Step 1 is editorial and step 2's list is yours.
