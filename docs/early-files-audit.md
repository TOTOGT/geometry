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
