# Revision plan — "The Immune System as a Maintenance Engine"
Applying Henry Cohn, *Advice for amateur mathematicians on writing and publishing papers* (cohn.mit.edu/advice).

**Framing.** Cohn's through-line: separate yourself from cranks by (a) modest checkable contributions, (b) standard language, (c) real literature engagement, (d) clear non-bragging introductions, (e) outside feedback. This paper is already the *right kind* of paper for that — an applied domain paper with falsifiable predictions, not a Millennium-problem claim. The fixes below are about presentation, not direction.

---

### 1. Develop a track record — make this paper stand ALONE
Cohn: appear-from-nowhere famous-problem claims get ignored; build a record of serious, uncontroversial contributions.
- **Issue:** the paper inherits the series umbrella (links to a Poincaré "correspondence," Collatz, Navier-Stokes, the Monster). A referee who follows those links pattern-matches to crank — regardless of this paper's merits.
- **Fix:** cut the grand-unification cross-links from the body; cite only what *this* paper uses. Let the checkable claims carry it: autophagy-as-fold, the μ=−2 Lean result, the three predictions. The umbrella story lives elsewhere, clearly labeled.

### 2. Use standard terminology — the single biggest fixable problem
Cohn: don't invent terminology/notation; if you must, relate it to the standard.
- **Issue:** heavy private vocabulary ("dm³ operator chain," "generative transition," "commitment operator K," "g-series," "GTCT," "temporal operator 𝓔"). A geometer or immunologist can't parse it.
- **Fix:** add an explicit translation table and use standard names in the prose:
  | Coined term | Standard term to map to |
  |---|---|
  | Fold operator \(F\) | Whitney \(A_1\) fold / fold catastrophe (Thom, Arnold) |
  | The G-chain | piecewise-smooth / impulsive (hybrid) dynamical system with resets |
  | Contact manifold, Reeb flow | standard contact geometry (Geiges) |
  | \(\mu_{\max}\) "contraction rate" | Lyapunov exponent (post-fold Floquet) |
  | Commitment \(K\), compression \(C\), unfolding \(U\) | define against existing concepts; **where no standard analogue exists, say so plainly** rather than implying one |
  Rename or gloss so a reader fluent in dynamical systems follows without learning a private dialect.

### 3. Search the literature (MathSciNet analogue)
Cohn: if you're not searching, you have no idea what's out there.
- **Issue:** the paper cites biology headlines (*Nature*, *Cell*) but not the mathematical-modeling literature it competes with.
- **Fix:** engage and position against — mathematical immunology (Perelson; Nowak & May, *Virus Dynamics*); singularity/catastrophe theory (Thom; Arnold; Golubitsky–Guillemin); impulsive/hybrid dynamical systems; and the existing **ODE bistability models of mTOR/AMPK/autophagy** (a large systems-biology literature). Replace the blanket "no linear ODE framework can encode these distinctions" with a specific, cited statement of what prior models do and where non-commutativity actually adds something.

### 4. Clear, non-bragging introduction
Cohn: explain what it's on, what it relates to, why care, techniques — implicitly; don't exaggerate.
- **Issue:** the abstract asserts ("No linear ODE framework can encode…"; disease mappings stated flatly as fact).
- **Fix:** soften proclamations to proposals; state the relation to existing models; cut superlatives; lead with the concrete checkable results, not the grand claim. (This is the same discipline as the webpage's conjecture tags.)

### 5. Format & conventions
Cohn: one-paragraph abstract; don't force a theory paper into a generic "science-paper" mold; theory papers usually skip a "conclusions" section.
- **Issue:** the abstract is several dense paragraphs.
- **Fix:** compress to one tight paragraph — problem, proposal, the one verified result (μ=−2), the three predictions. This is genuinely cross-disciplinary, so a hybrid format is defensible; just keep it disciplined.

### 6. Get feedback — and don't imply endorsement
Cohn: get friends/collaborators to read and *criticize*; referees aren't for this.
- **Issue:** the paper cites the Hidalgo/Yale group's work. Citing ≠ endorsement — the framing must not imply those researchers back the dm³ mapping.
- **Fix:** get one real immunologist and one real dynamical-systems mathematician to attack it ("where is this wrong/unclear?"). Add a line making explicit that cited authors' experimental work is used descriptively and implies no endorsement of the framework.

### 7. Professional submission / journal fit
Cohn: choose a journal that publishes papers like yours; no double submission.
- **Issue (the hard one):** no single journal referees both contact geometry and innate immunity.
- **Options:** (a) keep it a clearly-labeled **preprint/perspective** (Zenodo is fine — but call it a hypothesis, not a "result"); (b) **split** into a rigorous math note (the μ=−2 stability, properly framed, to a dynamical-systems venue) and a **hypothesis/perspective** for a theoretical-biology journal (*J. Theor. Biol.*, *Bull. Math. Biol.*); (c) if kept whole, target a **mathematical-biology** journal and adopt its conventions.

---

### Bottom line
This is the right kind of paper to build the track record Cohn describes — modest, applied, falsifiable — *provided* it (1) stands alone without the grand-unification baggage, (2) translates its private vocabulary into standard terms, (3) engages the real modeling literature, (4) states proposals not proclamations, and (5) is read by a real immunologist and a real mathematician before it's called anything more than a preprint.
