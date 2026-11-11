# Evaluation of the earlier Claude session's Jacobian work (repo, Lean, WP60 page)

Date: 2026-11-11. Evaluator: Claude Sonnet 5.5. Scope: `TOTOGT/jacobian` at HEAD a6c5ef4 (2026-07-24), `book7/jacobian-verification.html` (WP60) with its PDF, and the Lean printed on it. The producing session is not identified in any file read.

**Method and limits.** Nothing was compiled: no Lean on this machine, and the Mathlib source was not reachable (GitHub access to that repo was refused), so every Lean finding is from reading, tagged R (read) below. Findings tagged **RAN** were executed (sympy, exact arithmetic) and are in `book7/jacobian-verification-verify.py`. Findings tagged **LOG** come from the CI log of run #52 on 2026-11-11. A finding tagged "unconfirmed" is a suspicion, not a defect.

## A. WP60 page (book7/jacobian-verification.html, PDF, Zenodo 10.5281/zenodo.21514514)

| # | Finding | Basis | Severity |
|---|---|---|---|
| A1 | The printed map (F2 = -(1+xy)^4, F3 = x) is not the counterexample: det Jac = 4x(1+xy)^6; the three points map to (0,0,-2), (111,-81,-2), (18315/4,-6561,-2). Theorems 2.1, 2.2 false as printed. | RAN | Critical |
| A2 | "Zero sorry, kernel-verified", the `#print axioms` block and the "expected output: zero errors, zero warnings" describe a build that cannot have run on this map. CLAUDE.md already records that no .lean file exists in any repo. | RAN + R | Critical |
| A3 | Section 3.4 corollary proof `h (by linarith [...])` asks `linarith` to prove an equality of triples (the hypothesis `h` needs `f p1 = f p2`). As printed it would not elaborate. | R | High |
| A4 | Section 3.6 narrates a `map_ofNat` looping-simp difficulty "during formalization". Nothing was formalized against this map, so the account is invented or from a different file. | R + A1 | High |
| A5 | Imports `Mathlib.RingTheory.MvPolynomial.Basic` / `...Pderiv`; the jacobian repo (which built) uses `Mathlib.Algebra.MvPolynomial.PDeriv` and `...Basic`. Printed paths unconfirmed. | R, unconfirmed | Medium |
| A6 | Attribution "L. Alpoge and Claude Fable 5, A Counterexample ..., Preprint, 2025" and "Alpoge-Fable 2025": no source read supports the title, the co-authorship or the year. Sources read: Gao, arXiv:2608.00222 (manuscript dated 31 Jul 2026, announcement 19 Jul; Fable 5 credited with assisting Gao); AFP entry (announcement 20 Jul 2026). | R (fetch) | High |
| A7 | Remark 4.1 / section 4.2. **Partly confirmed 2026-11-11** from the ADS abstract of arXiv:math/0512171 (Belov-Kanel, Kontsevich), Bavula arXiv:math/0512250 and Wikipedia: JC_2n implies DC_n (BKK; Bavula gives a shorter proof), and the opposite implication DC implies JC is called well-known; together they give *stable* equivalence, not JC_2n <=> DC_n at fixed n as the page writes. The page's "DC_n <=> PC_n" appears in none of the three sources (no Poisson conjecture mentioned). The remark's conclusion (a dimension-3 counterexample says nothing about DC) conflicts with DC_n implying JC_n: if that implication holds at the same n, a counterexample at n = 3 refutes DC_3. The index of the easy direction is not stated in the text read (Wikipedia's extraction was garbled), so the exact range for DC is unconfirmed. Papers themselves not read; Tsuchimoto 2005 not reached. | read via fetch summaries | High |
| A8 | The ledger marks "F is not injective ... VERIFIED, Lean 4". Verified only for a different map, by sympy, today. | A1 | Critical |
| A9 | Section 1 history: "In 2025". Wrong; July 2026. | R (fetch) | Medium |
| A10 | Title "An Independent Lean 4 Verification": no Lean artefact exists; AFP (Isabelle/HOL) is the independent formal check I found. | R | High |
| A11 | Gold Standard box on the page says "no script or Lean file" (generated, stale as of the new verify script). | R | Low |
| A12 | The Zenodo deposit and PDF almost certainly carry the same wrong map (PDF text confirms F2 = -(1+xy)^4). The deposit itself was not opened. | R | Critical if distributed |

Downstream: `claims.tsv` rows 1400-1406 tag the page `conjecture`; `book7/wp58-galactic-fold.html`, `wp59-dark-matter-lensing.html` and `index-book7.html` only carry generated link boxes naming it; `book4/rh-paper.html` mentions "Alpoge and Furman" on a different (RH) topic, unrelated and not examined.

## B. TOTOGT/jacobian (Lean and workflow)

| # | File | Finding | Basis |
|---|---|---|---|
| B1 | JacobianCounterexample.lean | Byte-identical to SpectralDiagonalBound.lean (spectral-radius bound, two `sorry`). Contains no map, determinant or collision. README calls it "Counterexample polynomial map formulation". | RAN (diff) |
| B2 | SpectralDiagonalBound.lean | Both theorems are `sorry`. Labelled `[CONJECTURAL]`; the statement (diagonal of a Hermitian matrix is bounded by the largest |eigenvalue|) is textbook and true, so the label is wrong: it is an unproved lemma. Unrelated to the Jacobian problem. | R |
| B3 | DualDerivations.lean | `jacobian_mul_inverse_eq_one`: statement correct, proof fails at `split_ifs` (the one CI error). The inverse is defined with a hard-coded factor -1/2 and dimension 3, so it is an "inverse" only under det = -2; the name hides that. The file imports `JacobianCounterexample`, i.e. the unrelated sorry file, for no reason. Does not touch injectivity, so it is not evidence about the conjecture. | LOG + R |
| B4 | DualDerivations.lean | `dualDerivation_apply_F` (delta_ij identity) is mathematically correct by hand; its proof was never confirmed (CI fails earlier in the file). README marks it `[PROVED]`. | R |
| B5 | Poisson.lean | `standardPoissonBracket` is `sorry` as a data definition. `standardPoissonBracket_is_valid` states only `Nonempty (PoissonBracket ...)`, which the zero bracket satisfies; its docstring claims the standard bracket satisfies the axioms. Too weak by design (R20 shape). | R |
| B6 | Poisson.lean | `PoissonConjecture m pb` quantifies over any bracket `pb`. For the zero bracket every algebra endomorphism is Poisson, and x -> 0 on a polynomial ring is not bijective, so the proposition is false for m >= 1 as defined. It states the right conjecture only if `pb` is fixed to the standard bracket, which is not required. A stray glyph ("y-tetragram") sits in the docstring. | R |
| B7 | Dixmier.lean | `WeylAlgebra` as `Algebra.adjoin` of multiplication and partial-derivative operators on the polynomial ring is a sound model of A_n in characteristic 0. `DixmierConjecture` (every endomorphism bijective) is the right statement. `pderiv_mulX_comm` is `sorry`, though the identity is true and elementary. Only the commutation relation is stated; no theorem relates the file to the Jacobian map. | R |
| B8 | lakefile / toolchain | Mathlib requirement unpinned, no lake-manifest.json committed; lean-toolchain v4.32.1 vs Mathlib master v4.36.0-rc2 (Lake auto-switched in CI). Build passes by accident of drift. | LOG |
| B9 | verify.yml | `cache get` and `lake build` each run twice; ends with `lake update` and an `ls`, which tests nothing. No `sorry` gate: a build with `sorry` is a green check with warnings (it is green on the files that have them). | R + LOG |
| B10 | README.md | Pasted chat text including a prompt-style draft; "Out with the Jacobian"; the registry statuses (`[PROVED]`, `[CONJECTURAL]`, `[PROVE-ME]`) were not produced by any tool. | R |

Lean `sorry` count at HEAD: SpectralDiagonalBound 2, JacobianCounterexample 2 (duplicate), Poisson 2, Dixmier 1, DualDerivations 0. (LOG: warnings "declaration uses sorry" at Poisson 28:18, 33:8; Dixmier 40:8.)

## C. What stands

- The *arithmetic* of the Alpoge counterexample as printed in Gao Thm 3.3: det = -2 and the three-point collision, re-derived by sympy today. A formal check by other authors exists (AFP). Neither is this corpus's Lean.
- The elementary identities in DualDerivations (statement level) and Dixmier's commutation relation are correct as mathematics.
- WP60's section 1 framing of the conjecture and the claim JC remains open for n = 2 match the AFP abstract ("no claim about dimension two").

## D. Not examined

The Zenodo deposit; any other Claude session's output not in these two repos; Gao's paper beyond the fetch summary (formulas were re-derived by running them, not read from the PDF); the Belov-Kanel-Kontsevich and Tsuchimoto statements (A7).
