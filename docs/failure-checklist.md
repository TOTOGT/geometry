# Failure checklist for the Principia Orthogona corpus

Set 2026-11-08 at the author's request. Every chapter review, new chapter, and Lean file runs against this list. Each item is a failure that has actually happened in this corpus; the "where" column is the evidence, recorded in `docs/audit-log.md` and `docs/ml-evidence/reviews/2026-11-08-process-review-open-claims.md`.

| # | Check | Failure it prevents | Where it happened | What to do |
|---|---|---|---|---|
| 1 | Is a g-label (g⁰, g², g⁶, g³³, g⁶⁴) used as a count, bound or constant? | Arithmetic about a label read as dynamics | "33 cycles to stability", "g⁶ = 33", "after 64 applications of G", Θ = g₃₃ + N×M | g-labels name stages (g-series.html). A number needs a defined system and a derivation. Worklist: `docs/g-series-taxonomy-inventory-2026-11-08.md` |
| 2 | Are the operators C, K, F, U actual maps on a stated space? | Names treated as constraints on the composite | C = x/2, K = x, F = x/2, U = 8x meet the component conditions, yet G = 2x; Vol I 5.1's Lean assumes non-expansiveness | One concrete system; prove L_U·L_F·L_K·L_C < 1; then d(Gⁿx, x*) ≤ Lⁿ/(1−L)·d(x, Gx) gives a tolerance-dependent count |
| 3 | Does the claim concern motion, and is there a trajectory theorem? | Equilibrium geometry standing in for dynamics | FoldHysteresis "landing at −2"; "stays on its branch"; at a = 2, q(0) = 1 stays at 1 | Prove existence and convergence for the flow; treat ramps separately |
| 4 | Does "proved"/"verified" sit on a definition, `rfl`, or a `True` conclusion, or on assumptions containing the conclusion? | Tautologies presented as results | `g6_is_33 := rfl`; Vol II Theorem A (`True`), Theorem B; "8 Verified Constants" | Relabel as definition; declare in `Orthogenesis/Architecture/KNOWN_PLACEHOLDERS.txt`; restate before proving |
| 5 | Has anyone looked for a counterexample, and do the hypotheses hold for the actual vector field? | Statements false as written | FiniteBranching (U not connected); ch10 "all r(0) > 1 converge"; Whitney fold where both equilibria are saddles; "irreversible F" | Try to break the statement first; check each hypothesis against the equations |
| 6 | Does the Lean statement say what the page sentence says? | Compiles ≠ proves what it says | ExistenceWellPosedness (toy Banach) vs Vol I 5.1; old Reeb theorem about a scalar potential | Read the declaration against the claim it backs, every badge |
| 7 | Does every cited declaration exist? | Phantom verification | `nodal-sets.html` (3 missing), `chA-autophagy.html` (9 of 10) | Badge links to the declaration; run `tools/proved_labels.py` |
| 8 | Can each check in the verify script fail? | Scripts that pass anything | A finance check that could not fail; one passing with swapped cells | Add a control with a corrupted input that must be rejected |
| 9 | Is every citation and number traced to a primary source? | Unsupported facts | 114 GPa; wrong names and year; Frost strain figures in the bone report | Verify or remove |
| 10 | Is a theorem-shaped statement proved, sketched, or bare? | Theorem-shaped prose | 81-statement triage (30 no proof, 20 unchecked); Structural Theorems 5.2, 5.4 | Prove, narrow, or retire; say which on the page |
| 11 | Is an "open problem" stated precisely? | Items marked open before being stated | The softening limit (closed in one file, FoldSoftening.lean) | State the theorem first; many close or narrow |
| 12 | Does a cross-domain claim carry a derivation? | Unifying claims by resemblance | Coherence Bridge rows; "g = 33 across physics, biology, linguistics"; "Complete Completeness" | Derive it, or label "shared functional form, not shared invariant" |
| 13 | Is every limit stated with its normalisation and space? | Wrong limits | Vol II: unnormalised e^{−βz} has mass 1/β → 0 | State domain, normalisation, test functions; e.g. βe^{−βz}1_{z≥0} → δ₀ |
| 14 | Site hygiene: one document per file, no orphans, no stale copies | Broken or invisible pages | AXLE lessons index (two documents in one file); orphans; duplicate pairs | `tools/audit.py`; `python3 tools/build_indexes.py` after any change |

Working rules that go with it (from the same sessions):
- Hand-derive first; write the Lean; say "untested" until the author's build passes on the final rebased revision (pull, build, then push).
- Work only in `~/Desktop/geometry`; `~/geometry` is a stale clone.
- No inline `#` comments in shell commands given to the author (zsh passes them as arguments).
