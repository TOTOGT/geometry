# Audit: book7/ch-hawking.html (2026-11-20)

Audit record and proposed repair only. No manuscript page, generator, Lean file or sealed artifact was edited. Source of comparison: S. W. Hawking and G. F. R. Ellis, *The Large Scale Structure of Space-Time* (CUP 1973), text extracted with pdftotext from the author's copy; §8.2 read in full for the two singularity theorems. Nothing from the book is reproduced beyond the hypotheses of the two theorems, paraphrased.

## 1. What the book says (section 8.2)
- Theorem 1 (Penrose, 1965): space-time cannot be null geodesically complete if (1) R_ab K^a K^b >= 0 for all null K; (2) there is a non-compact Cauchy surface; (3) there is a closed trapped surface.
- Theorem 2 (Hawking and Penrose, 1970): space-time is not timelike and null geodesically complete if (1) R_ab K^a K^b >= 0 for every non-spacelike K; (2) the generic condition holds; (3) the chronology condition holds; (4) one of: a compact achronal set without edge, a closed trapped surface, or a point whose null geodesics (all past, or all future) start to reconverge.
- Proof method in both: conjugate points from focusing (Raychaudhuri-type propositions in section 4.4), then a contradiction with compactness of a boundary set. The conclusion is that at least one inextendible geodesic is incomplete.

## 2. Findings
F1 (changes a mathematical statement). Theorem H.1 is not a statement of either theorem. It takes "globally hyperbolic" and "strong energy condition (timelike vectors)" with "compact trapped surface" and concludes incompleteness. Missing: the non-compact Cauchy surface of Theorem 1, or the generic and chronology conditions of Theorem 2. In the book's Theorem 2 global hyperbolicity is not assumed at all. Also the null-vector condition in Theorem 1 is weaker than the strong energy condition as the chapter states it.

F2 (changes a mathematical statement). "The singularity theorems are instantiations of Banach's fixed point theorem" and "the singularity is the unique fixed point x* with G(x*) = x*" are not supported by the book. The proofs use focusing and a compactness contradiction. The theorems give incompleteness of some geodesic, not a point, not a location, not uniqueness. No contraction mapping or metric space on which G contracts is written down in the chapter.

F3 (provenance label). The closing Lean-style comment block says "3 identificacoes estruturais verificadas" with check marks. There is no Lean file or script behind them; the page's own Gold Standard box shows "(i) reproducible: no script or Lean file". "Verified" there should read "stated" until a file exists.

F4 (machine labels). docs/claims.tsv ch-hawking#5 is labelled `proved`, but the sentence it comes from is the page's own "Status: Conjecture. Not proved. Not refuted." That is a negation read as a positive (substring "proved"). #1 is labelled `proved` from "Hawking ... proved this" (Hawking's result, not the chapter's). #3 is labelled `proved` from Theorem H.1, which per F1/F2 is a reading, not a proof. Only #3 needs a human decision; #1 and #5 are classifier artifacts. The classifier itself (tools/claims.py) is not edited here.

F5 (count conflict). Section III says AXLE v6.1 "marks this problem as one of nine open sorrys". Book V chapter 3 is titled "The 9 Closed Sorrys". Both cannot describe the same nine without a stated change of status. Not resolved here; no registry file was read.

F6 (quote provenance). The English quotation attributed to the "BBC Reith Lectures, 2016" is not traced to a source on the page. The Portuguese rendering differs from the English. Needs a primary source or removal; I did not locate one.

F7 (age). "Hawking was 29 when he proved this": by my recollection he was born 8 January 1942 and the Hawking-Penrose paper appeared in January 1970, so 27 or 28. Unverified from the book; check before keeping.

F8 (language). "Theorem H.2" (Hawking radiation = fold F, Unruh effect = K, pair creation = F) and "Theorem H.3" (no-boundary = fixed point) are identifications, as the chapter's own WP70 addendum says for the constants. Neither is derived. The 1974 temperature formula and the 2004 bet with Preskill, the Page 1993 and Maldacena 1997 references are standard and not contradicted here; the 1973 book predates all of them and cannot support them. "As M goes to 0 the black hole explodes" extrapolates the formula past its validity (the formula diverges).

## 3. What survives
The Section III treatment of the information problem is already labelled a conjecture with a named missing lemma and is the most careful part. The WP70 addendum correctly withdraws the constant-matching. The irreducible-mass / area-theorem comparison named there is the connection that needs no constant to coincide.

## 4. Proposed repair (not applied)
See docs/proposed-patches/ch-hawking-h1-replacement.md. Summary: restate H.1 with the book's two theorems, relabel Theorems H.1-H.3 as "Reading H.n (the author's identification, not a theorem)", change "verificadas" to "enunciadas", resolve F5-F7 against sources, and leave the classifier row for #3 to the author.

## 5. Not done
Section 8 beyond 8.2 and the black-hole chapters were not read for this audit. Sources for F5, F6 were not located. tools/claims.py and docs/claims.tsv were not regenerated.
