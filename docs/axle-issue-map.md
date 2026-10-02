# AXLE issue numbers, checked against GitHub

Checked 2026-09-15 against `github.com/TOTOGT/AXLE`. GitHub numbers issues and
pull requests in one sequence, so a number used by a PR can never become an issue.

| # | what it actually is | title | state |
|---|---|---|---|
| 6  | issue | Prove `closurePoints_stationary` without regularity hypothesis — full club filter for all limit ordinals | closed |
| 12 | issue | O1: `separation_theorem` — eigenvalue API gap (Mathlib.LinearAlgebra.Matrix.Spectrum) | open |
| 13 | issue | AutophagyDm3 — Mather C∞ stability (Ob.2) and Poincaré–Bendixson (Ob.3) | open |
| 14 | issue | O3: Theorem T1 — full ODE Grönwall integration (z(t) monotonicity) | open |
| 15 | issue | "Update code" — a pasted trading-platform page, unrelated to this corpus | open |
| 16 | **discussion** | Bot scans buys, sells | open |
| 17 | **pull request** | Rename AULA screenshot to UcedaSchool… | closed |
| 18 | **pull request** | Rename screenshot to QRcode.png | merged |
| 19 | **pull request** | feat: Principia Orthogona G⁶ — full operator triad + five codex chapters | merged |
| 20 | **pull request** | Add README for crop circles geometric analysis report | closed |

## Corrections applied 2026-09-15

* **Theorem T1 / entropy monotonicity** was cited as AXLE #15. #15 is the trading
  page. T1 is #14, whose title names it exactly. Corrected in `book1/vol1-mathematics.html`.
* **AutophagyDm3, Ob.2 (Mather)** was cited as AXLE #14. Ob.2 is #13, whose title
  names it exactly. Corrected in `book7/Polylaminin.html` and `chA-autophagy.html`.
* **#19 and #20** are pull requests. `book4/ch14.html` cited them as issues for the
  Baker non-integrability obligation and for stating the Global Positivity Theorem
  in Lean. Neither issue exists and neither number can be reused. The obligations
  are real; the citations now name them without a number.

## Second pass, 2026-09-15 — the rest, curated

Every remaining citation was read against the statement beside it.

**Renumbered, because the real title names the obligation exactly.**

* `GameTheory_Full_Pack.html` and `.FIXED.html`: the Grönwall card and the
  Poincaré–Bendixson card were **swapped** — #13 and #14 each carried the other's
  obligation. Corrected to #14 and #13. The χ(H*(X⁶)) = 33 separation-theorem
  card cited #15, the trading page; the separation theorem is **#12**.
  Issue #6 was correct and is unchanged.
* `book8/ch2-event-horizon.html`: seven references to #13 for a Grönwall bound
  that "never closed in Lean". Grönwall is **#14**.

**Number removed, because the obligation has no issue.** Five cards in
GameTheory (#16–#20 as cited) point at a discussion and four pull requests;
`book8/ch6-quantum.html` cited #14 for kernel dimension; `ch-recurrence-ladder.html`
cited #13 for the asymmetric inner boundary. All now state the obligation and say
it is not yet filed. Drafts are in `docs/axle-issues-to-file.md`.

**Left alone deliberately.** `docs/ml-evidence/book4/ch09-belleville.html` cites
#14, #15 and #16. It is an ml-evidence snapshot, and the rule written 2026-09-01
is that those copies are evidence, not sources. Correcting it would destroy the
record of what was published.

## Filed 2026-09-15 — the nine now have numbers

Opened as #26–#34 from `tools/file-axle-issues.sh` (and its no-install twin,
`docs/file-axle-issues.html`). Confirmed at the source at two points, #30 and
#34, before the numbers were written back.

| # | obligation | source | cited in |
|---|---|---|---|
| 26 | Regeneration loop invariant after g₆ cycles — transfinite | `regeneration_loop_invariant.lean` | GameTheory (both) |
| 27 | Floquet multipliers for the spiral return map | `Main_v6.lean` | GameTheory (both) |
| 28 | IPR_trib > IPR_fib — formal bound | `SwarmSimulator.lean` | GameTheory (both) |
| 29 | Spectral measure of the transfer operator at a Whitney fold | `FoldEvents.lean` | GameTheory (both) |
| 30 | LCH construction for Legendrian action positivity | `MarketThreshold.lean` | GameTheory (both) |
| 31 | Kernel dimension from contact topology | — | `book8/ch6-quantum.html` |
| 32 | O7 — asymmetric inner boundary vs the symmetric Grönwall bound | `PrincipiaVol1.lean` | `ch-recurrence-ladder.html` |
| 33 | Global Positivity Theorem as a Lean proposition | — | `book4/ch14.html` |
| 34 | Non-integrability from Baker's theorem | — | `book4/ch14.html` |

Every "not yet filed" wording in the corpus has been replaced with its number.

## Rule

A number in this corpus is a citation. Before writing one, check it here or at
the source. Numbers are not reassigned by renumbering the corpus: if an
obligation has no issue, state the obligation and leave the number out.

## Filed 2026-10-01: ten more, #35-#44

Opened from `docs/axle-issues-to-file-2.html`. Live open list checked the same day: 13 open before these (#12-#15, #26-#34).
Confirmed against the live GitHub list in the author's browser on 2026-10-01: titles of #35-#44 match this table, in this order.

| # | obligation | cited in |
|---|---|---|
| 35 | `kappa_lipschitz`: Lipschitz bound on the dm3 coupling term | book4 ch10, chE-gtct-alt, ch-eta-dnls, dm3-lab-index, Book 3 sessions 2-3, livro3-brasil |
| 36 | Outer basin: convergence domain (z(0) hypothesis) | book4 ch10, ch09; HVEH ch09 |
| 37 | `inner_basin_escape`, null-causality route | book8 index, ch5, notes |
| 38 | `jackknife_correspondence` | book8 ch3, notes |
| 39 | `Matrix.minnorm` missing from Mathlib | book4 chIV-orthogonality |
| 40 | `P_ON (wrongOrder drv) = 0` | book4 ch09; HVEH ch09 |
| 41 | No homotopy between gamma_K and gamma_F | book4 ch09; HVEH ch09 |
| 42 | `g_arith`: connect to Mathlib vonMangoldt | book4 ch11, chpt11, chpt14 |
| 43 | Digamma cancellation, critical line | book4 chpt12, chpt14 |
| 44 | p-adic local coefficient definition | book4 chpt13, chpt14 |

Re-cited without a new number: independence of {log p} now cites #34; Global Positivity cites #33; Gronwall cites #14; Mather and Poincare-Bendixson cite #13 (poa_research, GameTheory).
#21 is a real, closed issue ("r* ≈ 0.77594 at arbitrary Lean 4 precision"), so `book4/METHODOLOGY.md` keeps citing it. The p-adic coefficient obligation that `chpt13.md` and `chpt14.md` had cited as #21 is now #44.

All 30 issues, checked live 2026-10-01: 23 open (#12-#15, #26-#44), 7 closed (#1, #3, #4, #5, #6, #10, #21). Every other number from #1 to #25 (#2, #7-#9, #11, #16-#20, #22-#25) is a pull request or discussion, not an issue.

## Resolved 2026-10-01, second pass

* Basin asymmetry (`inner_basin_is_asymmetric`, `thm_gronwall_asymmetry`, r* certificate), formerly cited as #13 on ten pages, now cites **#32** (O7). Chosen because #32's title names the asymmetric inner boundary against the symmetric Gronwall bound. Reversible if you would rather file it separately. #13 stays on the Mather and Poincare-Bendixson citations (poa_research, GameTheory, book7 Polylaminin).
* `book8/ch2-event-horizon.html`: the `inner_basin_escape` citations now cite **#37**. The last sentence ("the bound never closed in Lean") now cites #32 as well (2026-10-02): it is about the inner-basin Gronwall bound, which is the asymmetry obligation, not T1 (#14, Gronwall integration).
* `P_ON (correctOrder drv) > 0`, "discretisation bound": number removed; drafted as round 3 in `docs/axle-issues-to-file-3.html` (file it, or close as a duplicate of #14 if T1 covers it).
* "Proved" outer-basin wording in `book4/chpt12.md` and the Lean comment in `book4/ch10.html` corrected.

## Still open

* Issue #6, reconciled 2026-10-01 against the Lean. Four files carry `closurePoints_stationary` and they do not agree.
  * `PrincipiaOrthogona1/PrincipiaVol1.lean` (V7): hypothesis `Cardinal.aleph0 < α.cof`, the correct one. Built and kernel-checked at Lean/Mathlib v4.14.0, 0 sorry. This is the real proof of the regular case.
  * `lean/Main.lean`, the file commit a1f11b9 changed ("closes #6"): hypothesis `omega < α.card.ord` (uncountable cardinality, not cofinality). Its lemma `sup_lt_of_regular` is false as stated (α = ω₁+ω, s n = ω₁+n); the theorem is false for the same α. The 2026-09-09 audit: 59 errors against current Mathlib.
  * `AXLE_v8_1.lean` `closurePoints_stationary_regular`: hypothesis `α.card.ord = α` (initial ordinal, not regular). False for α = ω_ω, so its "honest admit #5" cannot be filled.
  * `CatGT/MahloClosure.lean` and `lean/Ordinal/MahloClosure.lean`: carry `g6_unconditional_closure` with a sorry and the comment "closes the final sorry in the Collatz–dm³ bridge".
  The counterexamples (a club of successor ordinals cofinal in α, plus α) are machine-checked: `ClosurePointsCheck.lean` at the geometry root compiles under Lean 4.32.0 / Mathlib v4.32.0 with zero errors, zero sorry and only `propext`, `Classical.choice`, `Quot.sound`. It proves both hypotheses insufficient, the regularity-free goal false, and the corrected theorem (`ℵ₀ < α.cof`) true. `AXLE_v8_1.lean` (working tree, not committed in the AXLE repo) was patched with the corrected hypothesis and that proof and recompiles with five sorries instead of six; its GATE-DECLARE line was updated. The goal in #6's title, regularity-free, is also false for cof α = ω by the same construction, so the pages that call "Issue 6" an open boundary describe a statement that cannot be proved as written. `TOGT.g6_unconditional_closure` (finite 33-step crystal saturation) is a separate statement the pages also label "Issue 6". Three issues are drafted in `docs/axle-issues-to-file-3.html` (with the `correctOrder` one, four in all); once filed, the pages get the numbers.
* `docs/claims.tsv` is a scraped table; regenerating it today would churn about 11,000 lines for reasons unrelated to citations, so it was not regenerated.
* GitHub housekeeping: close or relabel #15; retitle #12 and #34.

## GitHub titles (owner edit; the browser session offered no Edit option)

* #12: "O1: separation_theorem — restate with the Tr(M⁶) hypothesis (deposited form is false; not an eigenvalue-API gap)". Basis: `docs/defect-ledger.html`, 24 Aug.
* #34: "Linear independence of {log p} over ℚ and non-integrability of α_arith (elementary, by unique factorisation; not Baker)". Basis: `book4/ch11.html`.
* #15: unrelated page; close as not planned if you agree.

## Filed 2026-10-01: round 3, #45-#48 (confirmed live)

| # | obligation | written onto |
|---|---|---|
| 45 | `P_ON (correctOrder drv) > 0`, discretisation bound | book4/ch09, HVEH/ch09 |
| 46 | `closurePoints_stationary` stated with a false hypothesis (`lean/Main.lean`, `AXLE_v8_1.lean`); fixed and compiled | no page cites it yet |
| 47 | Regularity-free `closurePoints_stationary` is false when cof α = ω | GameTheory_Full_Pack |
| 48 | `g6_unconditional_closure`: ∃ m ≤ 33, crystal saturated and eigenmode locked | GameTheory_Full_Pack, ch-ocio |

#6 stays closed: it holds for cof α > ω (`PrincipiaVol1`, #46's fix).

### "Issue 6" is three different things in the corpus (found while writing #47 and #48 back)

1. Cardinal regularity in `MahloClosure.lean` / `closurePoints_stationary`: now #6 (closed), #46, #47; and `g6_unconditional_closure`: #48. Pages updated: GameTheory_Full_Pack, ch-ocio (code comments and the two sorry labels).
2. The G⁶ conjecture χ(H*(X⁶)) = 33 for all n, labelled "Issue 6" on about twenty pages: book5 (chV-g6, chV-sorrys, chV-axle, index), book6 (chVI-conjecture, g6-crystal, chVI-planetary, index, wp29), book1/vol2-dashboard, vol2-contact, book7/ch-huh, ch-d2-academic, ch24, chH-collatz, spectral-radius-v2, trilogy-sale, g6-opus-map. GameTheory maps the χ = 33 separation theorem to #12; chVI-conjecture records it "REFUTED for closed orientable manifolds 2026-08-21". Which issue carries it (#12, restated?) is an author decision; not changed.
3. Smoothness regularity (α is C∞ and α∧dα ≠ 0) in `AMonster/monsterlaw.html` ("prove the hyper-Mahlo fixed-point result without the regularity hypothesis"), echoed in `ch-ocio.html` (Axiom 9, topic chip) and `ch3c-econophysics.html`. Different from sense 1: the cofinality counterexample does not touch it, and no issue carries it. Not changed.
