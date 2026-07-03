# Book 4 · Higher Dimensions Arc — Style & Consistency Audit

Reference: **ch10.html** (house style). Audited 2026-06-11 against the live site.
Scope: ch00–ch09 (ch02 already revamped; ch10 is the standard).

## Style census

Five different templates are currently live in one arc:

| Template | Chapters | Markers |
|---|---|---|
| **House (target)** | ch10, ch02 (new) | Running head, author/meta card, abstract, numbered Contents, sidenotes, dark sim section, series grid, citation footer |
| A — "Book 4 nav" | ch00, ch03 | ⚜ BOOK 4 ⚜ nav bar, kicker "Book 4 · Chapter N · Dimension Ladder", task+Copy block, minimal footer |
| B — "Hub nav hero" | ch01, ch04, ch05, ch06 | "Principia Orthogona · Book 4" strip nav, big hero with "↓ scroll", same body conventions as A |
| C — Book 3 "Mini-Beast" | ch07, ch09 | Book 3 ⚜ nav, Week/CEFR badges, Student Portal prompts, Crystal Map widget — **Book 3 template, not Book 4** |
| D — One-off | ch08 | Own nav ("G6" mark), GoFundMe/eBay footer links |

**Recommendation:** migrate A and B chapters to house style directly (content maps cleanly: hero → chapter-open card; §x.y → §N + Contents; def/theorem callouts → .env boxes; interactive widgets → dark sim section; task → exercise box). ch07/ch08/ch09 need an editorial decision first (see below) — they are different *kinds* of chapters, not just differently styled.

---

## Per-chapter findings

### ch00 — Student Edition
- Style A. No abstract/meta card/contents.
- **Stale chapter plan** (old 15-chapter numbering):
  - "does the attractor persist? (Yes — Chapter 11)" → **Chapter 4** (Thm 4.2)
  - "Chapter 12 lives here" (5D jet space) → **Chapter 5**
  - "Chapter 13 onward" (5D+t) → **Chapter 6**
  - "Chapters 0 → 15" (Pass 1) → 0 → 10 (or current count)
  - "By Chapter 10, you will be reading geometry in six dimensions" — ch10 is the dm³ paper (3D); 6D is ch06.
- **Ladder section skips the 2D+t rung** — cards jump 1D → 3D → 4D → 5D → 5D+t. Ch 2 (the chapter you just revamped) is missing from its own ladder.
- **Ch 1 described as "The ODE — ẋ = f(x)"** but the live ch01 is *The Fermion Seed* (ψ² = 0). The ladder card and the nav label "Ch 1 · The ODE as a 1-Dimensional Story" describe a chapter that no longer exists.

### ch01 — The Fermion Seed
- Style B.
- "T … Chapter 13 onward" → **Chapter 6**; §1.8 "Chapters 2 through 13" → 2 through 6 (or 10).
- Math flags: `f(ψ) = aψ + bψ†` introduces ψ† never defined (single-generator Grassmann algebra Λ(ψ) has no ψ†); "occupied (ψ = 1)" is loose for an odd variable. Remark 1.2: braid group B₃ needs three strands, but the text derives the braid from *two* objects ("path taken and path not taken").
- Introduces the **5-operator chain C→K→F→U→T**, while ch02/ch10 and the series branding use the 4-operator G = U∘F∘K∘C. See cross-cutting item 2.

### ch03 — Contact 3-Manifold + S³
- Style A — closest in substance to ch10; easiest house-style migration; it even has the same sim concept (r–z portrait + 3D helix).
- "the radial ODE from Chapter 1" — stale: Chapter 1 is now the fermion seed, not r(1−r²).
- **r\* value conflict:** ch03 says r\* ≈ 0.8; ch10 body says r\* ≈ 0.80 but ch10's figure label reads **r\* ≈ 0.8123**, and the **index card for ch10 says r\* ≈ 0.776**. Four claims, three values. Pick one (presumably the current DOP853 number) and propagate.
- ch03 next-link calls ch04 "First Lift"; ch04 calls itself "The Hypercube"; the index calls it "The Tesseract". One name, please.
- Theorem 3.3 "locally contactomorphic to S³ near the attractor" is vacuous as stated (Darboux makes *everything* locally contactomorphic) — consider restating as: the attractor's neighbourhood geometry matches the Hopf/Reeb model on S³.

### ch04 — The Hypercube / Tesseract
- Style B. Title inconsistency (above).
- §4.5: `ẇ = s(r,θ,z,w)` uses *s* as both the symplectisation coordinate and an undefined function; System (4.1) is a sketch wearing theorem clothing — Theorem 4.2's "area = 2π ⇒ w-exponent bounded by −2" is asserted, not derived or cited. If it's numerical/heuristic, label it like ch10 labels its proof sketch ("numerical").
- ch00's pointer to this result still says Chapter 11 (see ch00).

### ch05 — OPERA SATOR · Jet Space
- Style B.
- **Math flag — Theorem 5.1 ("Lie's theorem"):** by **Bäcklund's theorem**, for n ≥ 2 *every* contact transformation of J¹(ℝ,ℝⁿ) is a prolonged point transformation — there are no "genuine" contact transformations mixing x, yᵢ, pᵢ non-trivially on J¹(ℝ,ℝ²). The exceptional case is n = 1. As stated, the theorem that sets up GTCT is false for the space the book works in. Either move to J¹(ℝ,ℝ) or reframe GTCT as point/Galilean symmetries.
- **Letter-count claim is wrong:** "every letter appears twice — except one N." Actual counts: N=1, S=P=2, A=T=O=R=E=4. The true (and better) statement: under 180° rotation every *cell* pairs with its mirror cell; the centre cell is the unique fixed cell. Keep the N-as-fixed-point idea, fix the arithmetic.
- "the fixed point was x\* = 1, the fermion occupation number" (Ch 1) — stale old-Ch1 reference again; the live ch01 has no x\* = 1.

### ch06 — 666 · The 111 Square
- Style B.
- **Nav break:** footer/next goes to *Contents*, but ch07 exists. Restore Ch 6 → Ch 7 sequence (decision on ch07's status first, see below).
- **Math flag — the φ_v "✓":** d(y₁+vt) − (p₁+v)dx = dy₁ − p₁dx **+ v(dt − dx)**. The check only passes if t ≡ x. Either define the boost along the base coordinate (y₁ → y₁ + vx) or state the dt = dx convention.
- Theorem 6.1's invariant count "6·5/2 + 1 = 16" is unsourced and sits next to a "primary invariant = magic constant" claim that is analogy, not theorem. Consider downgrading to a Remark, matching ch10's honesty conventions (it marks open items as AXLE Issues).
- **GTCT expansion conflict:** here (and ch00/ch05) GTCT = *Galilean Contact Transformations*; the index/hub says GTCT = *Generative Temporal Contact Theory*. Both can coexist only if stated once, deliberately.

### ch07 — The Crystalline Return
- **Wrong template entirely**: Book 3 Mini-Beast nav whose links point at the geometry root, several to files that don't exist there (ch06.html…ch10.html — root uses ch6-resonance.html etc.). Crystal Map widget says "Book 4" but is the Book 3 component.
- **Broken prev-link:** "← Chapter 6 · Resonant" → `book4/ch6-resonance.html` (Book 3 file path inside book4 — 404). Should be `ch06.html`.
- **Boilerplate from Book 3:** ISBN 979-8-9954416-1-8 and Zenodo 10.5281/zenodo.14765680 don't match Vol IV (979-8-9954416-8-7 / 19117400).
- Content is a different register (Saturn hexagon → Monster group → galactic merger → pedagogy). Factual spot-checks pass (Monster order, 196,883/196,884, Borcherds 1992/Fields 1998, n-bonacci ratios and terms, Andromeda 110 km/s), with nits: the Saturn hexagon was identified in Voyager data by Godfrey in **1988** (Voyager flybys 1980–81); Classification "proved 1983" is the announcement — the quasithin gap closed in 2004.
- **Decision needed:** does ch07 belong to the Higher Dimensions arc (then re-theme into house style, big job) or to the Extended/popular tier (then label it as such and fix only nav/boilerplate)?

### ch08 — The Axiomatic Turn
- One-off template; GoFundMe/eBay footer; Book 3 ISBN again.
- **Broken next-links:** header "Ch. 9 →" goes to `geometry/ch9-phi.html` (Book 3); footer "Ch 9 · φ →" goes to `book4/ch9-phi.html` (no such file — it's `ch09.html`).
- Content (Letter to the Pope, Foulques→Clement IV→Grossi heraldry, 229 Ballantine Pkwy) is editorial/personal rather than mathematical. Historical flags if you keep it: Clement IV (Gui Foucois) was the son of a Provençal jurist — describing him as a *descendant of Foulques V* is genealogically unsupported; "only pope ever to have been a practising lawyer" is hard to defend. AXLE proof-state language here ("G⁶ threshold … sorry") is good and matches ch10's honesty convention.
- Same decision as ch07: arc chapter (restyle) or special file (relabel + fix links)?

### ch09 — φ · The Subcritical Approach
- **Book 3 template wholesale** (Week 11 · CEFR C1→D1, Student Portal prompts, Crystal Map) with Book 3 root nav, partly broken (same ch06–ch10 root links as ch07). This page is essentially Book 3's ch9-phi with the footer pointed at book4.
- **Mislabeled next-link:** "Chapter 10: Lyapunov →" → `book4/ch10.html`. Book 4's ch10 is *Helical Attractors*; Lyapunov is Book 3's ch10. Fix the label.
- Sportal link → `book4/Sportal.html` (file lives at geometry root — likely 404).
- Math checks pass (φ digits, golden angle 137.508°, under/overshoot alternation, error table).
- Decision: if the arc keeps a φ chapter, it should be rewritten in house style with the index's promised content ("fold frozen at q\* < 1"); currently it's a writing-course chapter.

---

## Cross-cutting issues (fix once, propagate everywhere)

1. **r\*** : 0.776 (index) vs 0.80 (ch03, ch10 §6) vs 0.8123 (ch10 figure). One number.
2. **Operator chain arity**: 4 ops (G = U∘F∘K∘C — ch02, ch10, series branding) vs 5 ops (C→K→F→U→T — ch01, ch05–ch06). If T is real, the brand formula should say so once ("G closes to G·T in 6D"), not vary silently.
3. **GTCT expansion**: Generative Temporal Contact Theory (hub/index) vs Galilean Contact Transformations (ch00, ch05, ch06). Also ch10's Lean block says "GCTC" (namespace GCTC) — typo for GTCT.
4. **Chapter 1 identity**: ch00, ch03, ch05 still reference the old "Ch 1 = radial ODE, x\* = 1". Live ch01 is the Fermion Seed. (My ch02 revamp keeps "Chapter 1 gave us ẋ = f(x)" from your original text — if ch01 stays fermionic, that opener should become "Chapter 1 gave us the seed; the first ODE…" Tell me and I'll adjust.)
5. **Ch 4 name**: First Lift vs Tesseract vs Hypercube.
6. **Stale numbering** (Ch 11/12/13/15) in ch00 and ch01.
7. **Footer identity block**: ch07/ch08 carry Book 3 ISBN + old DOI; everything in book4 should carry Vol IV (979-8-9954416-8-7, doi 10.5281/zenodo.19117400) like ch10.
8. **Nav chain integrity**: ch06→Contents (should be ch07), ch07's prev 404, ch08's next 404/mislabel, ch09's next mislabeled, ch07/ch09 top navs point at non-existent root files.

## Suggested order of work

1. Decide ch07/ch08/ch09 status (arc vs extended tier) and the canonical r\*, GTCT expansion, chain arity, Ch-4 name.
2. Mechanical fixes everywhere: links, footers, stale chapter numbers (small diffs, no redesign).
3. House-style revamps in order of payoff: **ch03** (closest to ch10, shares the sim), then **ch01, ch04, ch05, ch06**, then **ch00** (template differs most but content is short), then ch07–ch09 per the tier decision.
