# HANDOFF — Key Register, the letter U (2026-09-29). NOT FIXED. For the session that owns tools/key_register.py.

**Status: I could not settle HANDOFF item 4, and I do not think it can be settled inside the register.**
The register counts *glosses* ("U — Unfolding"). The series also *defines* U, in four places, and the
definitions disagree with each other. Deciding what to do with union / universal / unification before
the author picks among the definitions would mean editing Book XIV ch3/ch4 to fit a guess.
Everything below is reproduced by `python3 book14/key-register-u-check.py` (part 2 prints the quotes).

## What the corpus itself says U is
1. **Volume I** (`book1/vol1-mathematics.html`), Definition 3.4: *the unfolding operator* U : X_F → X, gradient flow to a local minimum. U = Unfolding.
2. **GCM paper page** (`gcm-framework.html`), one section, two operators: the table row "Unfolding U: ∇Φ-flow", then "the U-operator is the unification map between two dm³ systems (Theorem B)", **Definition 3.1 — Unification Operator**, X₁₂ = U(X₁,X₂), α₁₂ = α₁+α₂, τ₁₂ = √(μ₁²+μ₂²)/max(κ₁,κ₂).
3. **Omega gallery** (`omega/ch-fourfold.html`), **Definition 5.4 — Union**: the same X₁₂, α₁₂ and the same τ₁₂ formula. The page's own table says "U-operator (unification, Def. 3.1) = Union". It says Omega "takes this exact algebra … and reads it in a register" of theology.
4. **GCM Institutional Edition (2025)**, Appendix A (`~/Downloads/GCM-Institutional-Edition.docx`): g = metric operator, L = Lie derivative, R = Reeb vector field, **U = Unfolding operator** ("the stability operator"), B = boundary operator.
5. **Book 3 (Mini-Beast)** (`prelude.html`, `ch1.html`): U = "Universal — the same structure at every scale". `prelude.html` carries its own audit note: the page "defines six … U as 'Universal / scale-invariance'; other chapters use U for Unfolding, and the chapter method uses U for the residue test (hysteresis). **One set of definitions needs to be chosen.**" and closes "These are the author's decisions." So this is a known, open, author-owned conflict, not a stray.

## What follows for the four options recorded in the audit log (A–D)
- **union and unification are one operator by the corpus's own definitions** (items 2 and 3: same Definition, same formula). The register files them as two senses (a "second key set" homonym and a "stray"). The three unification pages (`ch7-crystalline`, `ch8-axiomatic`, `ch8-meru`) use it in exactly that sense (competing cells joined; galaxy merger; self and consumed; lineages joined). **Folding unification under unfolding (option C) is contradicted by the definitions.** The chain rule cannot see this because no page happens to use both words.
- **universal is not a stray either.** It is the Book 3 reading in item 5, and its own page says the choice belongs to the author. Two more Book 3 wordings of it are invisible to the register: `chapter-zero.html` ("U (Scale)"), `ch7-topological-orthogenesis.html` ("U = the scale-invariant braid-group structure"); `ch6-resonance.html` says "the recognition of the same structure at different scales" beside a legend that says "U Unfolding". A residue/hysteresis reading (`ch5-immune`, `chT-tubulin`, `chPsi-latent-capacity`) is invisible too.
- **The register's "three senses" is partly an artefact of `SENSES` in tools/key_register.py**, a hard-coded whitelist (unfolding, union, universal, unification). Any other gloss word is dropped silently. So "U has three senses" (ch4) and the 68/10/3/3 counts describe the whitelist as much as the corpus.
- **ch4 §3 says the Institutional Edition's U "is the Unfolding operator, which agrees with the majority".** True (item 4). But the same g/L/R/U letters mean different things in item 2/3 (g = expansion semigroup/Genesis, L = Lie-bracket/Logos, R = resonance selector/Resonance, U = unification/Union) than in item 4 (metric, Lie derivative, Reeb, unfolding). ch4 does not say so, and "the Omega chain G–L–R–U" is therefore not the Institutional Edition's g–L–R–U.

## Not for a session to decide
Which definition of U is canonical for Book 3, and whether Omega/GCM-page g–L–R–U and the Institutional Edition's g–L–R–U are meant to be the same algebra, are the author's calls (R9). Until then: do not change SENSES, ch3, ch4 or any page's U wording.
A possible mismatch I did not check mathematically: Def 3.1/5.4 give τ₁₂ = √(μ₁²+μ₂²)/max(κ₁,κ₂), while the Trinity pages state the Theorem of Union as τ₁₂ ≤ min(τ₁,τ₂).

## What was and was not read (so nobody assumes more)
Read in full: Book XIV ch3 and ch4 (text). Read in paragraph context: the six pages behind the extra glosses (`ch1`, `prelude`, `ch6-resonance`, `ch7-crystalline`, `ch8-axiomatic`, `ch8-meru`). Read at the definition: Vol I Def 3.4; `gcm-framework.html` §3; `omega/ch-fourfold.html` Def 5.4; the GCM docx Appendix A.
**Not read:** Volume II, the Lean files' docstrings, `omega/ch-union.html`, and the ~260 other pages carrying the Book 3 banner (only their U wordings were pattern-searched, not read). The answer could still be in one of them.

## Suggested next steps for the owning session
1. Ask the author the two questions above; record the answers in claims.tsv.
2. Only then decide whether key_register.py should be driven by definitions (a small table of "U as defined at X") rather than a gloss whitelist.
3. Rerun ch03/ch04-verify after any change (R24); ch4's "U is three" line and the figure depend on it.
