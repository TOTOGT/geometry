# Audit of the early (model-3 era) Book 2 files

Scope: the LaTeX sources in the author's Downloads folder dated March 2026 (main.tex, main_fixed.tex, main-2.tex, main-2-fixed*.tex, master_book*.tex, book321.tex, MASTER.tex, chapter 09 mars.tex, completePrincipia.tex). The author reports that most model-3 work had hallucinations. This page records the first pass; the script `engineering/early-files-audit-verify.py` reproduces every computed line.

## Method
R24: a script runs before any sentence is written. External facts were read from the publisher page or Crossref on 2026-09-30 and are marked CITED. Nothing here chooses a canonical figure (R9).

## Findings so far
1. **Lai (2026) author names.** The paper is real (Nature, "Bulk hexagonal diamond", DOI resolves) but none of the 12 given names in the `Lai2026` entry of main.tex match the Nature page (surnames do). Real list: Shoulong Lai, Xigui Yang, Jiuyang Shi, Shijie Liu, Ying Guo, Longbin Yan, Jinhao Zang, Zhuangfei Zhang, Qiuhan Jia, Jian Sun, Shaobo Cheng, Chongxin Shan.
2. **"Yang et al., Nature 2026".** Yang et al. is Nature 644:370-375 (2025), "Synthesis of bulk hexagonal diamond". The 2026 paper is Lai et al. My own 2026-09-29 patch carried the wrong year; corrected in main-2-fixed.tex and main-2-fixed-2.tex on 2026-09-30.
3. **114 GPa Vickers hardness.** Not found in either paper as read (both pages say only "slightly higher" than cubic diamond in the accessible text). UNCONFIRMED.
4. **Other references checked and correct:** Dorkenwald 2024 (Nature 634:124-138), Pospisil 2024 (Nature 634:201-209; main.tex keys it Dorkenwald2024b, a label error), Demirtas-Kim-McAllister-Moritz (PRL 124(21) 211603, 2020), Gukov-Vafa-Witten (NPB 584 (2000) 69; seen in ADS and ScienceDirect listings, the Crossref fetch was rate-limited).
5. **Tower height.** Three figures: 15,087.6 / 39,788 (chapter 09 mars.tex), 15,080 / 39,808 (main.tex, main-2.tex), 15,114 / 39,900 (my patch from the stated 229 m apothem). 15,087.6 = 66 x 228.6 m exactly (228.6 m = 750 ft) and 39,788 = 15,087.6 / (3.72/9.81); the 39,808 is 15,087.6 / 0.379. 15,080/66 = 228.48 matches neither apothem. **OPEN: which apothem is canonical (228.6 m or 229 m).**
6. **Bibliographies of master_book_FINAL_v2.tex and completePrincipia.tex.** 13 keys are defined more than once (Arnold x3, Bravetti2017 x3, ...), and Paper1 is called "submitted to J. Geom. Mech." in one bibliography and "Chapter 2 of this volume" in another; Paper1 and Paper2 share one Zenodo DOI (10.5281/zenodo.19117400).

## Not yet audited
Theorem-by-theorem triage of the 78 theorem environments in master_book (which are proved, which asserted); the numerical claims in chapters 8-10 of Book 2; main-2.tex (largest, unpatched); the PDFs.

## Theorem triage of master_book_FINAL_v2.tex (2026-09-30)
Script: `engineering/master-book-theorem-triage.py`; per-statement table: `docs/master-book-theorem-triage.tsv`. The script classifies what is on the page, not whether an argument is correct.

- 81 theorem-like statements (29 theorems, 42 propositions, 3 lemmas, 4 corollaries, 3 conjectures). By page features: 30 have no proof on the page, 7 have only a "Proof sketch", 10 have a one-line proof, 14 have a proof that defers to a citation or another result, 20 have a proof that looks complete (and is not yet checked). None was classed hand-waved by keyword.
- **The five "Structural Theorems" (lines 744-765) have no proof in this file, and the file is out of date against Volume I.** Found by a second, differently-shaped search (per the 2026-08-28 rule, one search is not evidence of absence): `book1/vol1-mathematics.html` carries the same five with status labels, and `book1/verification-registry.html` lists `ExistenceWellPosedness.lean` and `FiniteBranching.lean` (Vol. I sections 4 and 5; Finite Branching "honestly incomplete", with `sorry` in some lemmas). The current Volume I page has CORRECTED two of them: Non-Commutativity now reads "some orderings are order-dependent; the universal reading is false (corrected 2026-09-18)", and Irreducibility is marked "SHOWN - existential only". The early master_book still states both in the stronger, universal form. So the early file contains claims the author has since withdrawn; the corrections were not propagated back.
- Theorems A-D are restated in three places (introduction of the Paper1 chapter, the Paper2 appendix and later parts), with the same label. Proofs named "Proof of Theorem~\ref{thm:A}" sit in the later parts, so the copy at line 1427 has none of its own; it is counted as unproved here even though a proof of the same statement exists elsewhere. Propositions used inside those proofs (for example prop:portrait) are also counted as having none.
- Five statements are conjectures or corollaries about other claims with no proof (conj:global, conj:torus, conj:L1, cor:false); these are labelled as such in the book and are not findings.
- Not checked: whether the 20 full-looking proofs are correct, and whether the 14 that defer point to a cited result that says what is claimed.

## Which count is which (2026-09-30)
There is no single unified theorem count; three different things are being counted.
1. **Lean declarations** (`tools/theorem_census.py`, run on this checkout): 1,045 raw / 1,031 grouped, 3 with `sorry`, 0 axioms, 126 .lean files. This counts declarations with bodies, machine-checked where the file is in a lakefile target; it is not a count of mathematical results.
2. **The theorem registry** (AXLE, Tier 1 from `axioms.txt` files): CLAUDE.md records a by-hand total of 173 and says the tool reports less until it reads the other run records (Volume I's 58, GTCT's CI badge, io's CI). `--corpus --tracked` could not run from this session (it needs the author's local checkouts).
3. **Statements written in TeX** (this audit): 81 theorem-like statements in master_book_FINAL_v2.tex, not machine-checked. Some of these restate one another (Theorems A-D appear three times) and some have Lean counterparts.
The master index lists pages and numbered claims per page, a fourth unit. A unified figure needs a mapping table from TeX statement to Lean declaration to registry row; none exists yet.
