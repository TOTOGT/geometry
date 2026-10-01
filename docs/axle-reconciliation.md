# AXLE issues: reconciliation of corpus citations (2026-10-01)

Basis: `docs/axle-issue-map.md` (GitHub `TOTOGT/AXLE`, checked 2026-09-15). On 2026-10-01 you pasted the live open list: 13 open (#12, #13, #14, #15, #26-#34), 7 closed.
Nothing open sits above #34 and nothing open sits at #21-#25. The 7 closed issues were not listed, so
which numbers they hold (beyond #6) is unverified. GitHub numbers issues and pull requests in one
sequence, so a PR number can never become an issue.

## 1. What GitHub says each number is

| # | kind | what it is | state |
|---|---|---|---|
| 6 | issue | `closurePoints_stationary`, club filter at limit ordinals | closed |
| 12 | issue | O1 `separation_theorem`, eigenvalue API gap (`docs/defect-ledger.html`: the theorem was false, not unfinished) | open |
| 13 | issue | AutophagyDm3: Mather stability (Ob.2) and Poincare-Bendixson (Ob.3) | open |
| 14 | issue | O3 Theorem T1, full ODE Gronwall integration (z(t) monotonicity) | open |
| 15 | issue | unrelated pasted trading page | open |
| 16 | discussion | bot scans buys, sells | open |
| 17-20 | pull requests | screenshots, README, G6 chapters, crop circles | closed/merged |
| 21-25 | not open issues | pull requests or closed items; not in the map | ? |
| 26-34 | issues | filed 2026-09-15 (regeneration invariant, Floquet, IPR, fold spectral measure, LCH, kernel dimension, O7 asymmetric inner boundary, Global Positivity statement, non-integrability) | open |

## 2. Where the live corpus still disagrees (found 2026-10-01)

The 2026-09-15 passes fixed the pages they listed. These were not on that list.

| cited as | what the page means | real issue | action |
|---|---|---|---|
| #12 (about 25 pages: book4 ch10, chE-gtct-alt, ch-eta-dnls, dm3-lab-index, Book 3 sessao2/3, index pages, livro3-brasil, claims.tsv) | `kappa_lipschitz`, Lipschitz bound on the coupling | #12 is `separation_theorem` | new issue 1 |
| #12 (book8 ch3-singularity, book8 notes) | `jackknife_correspondence`, C4 to C3 fold | none | new issue 4 |
| #12-#17 "six remaining gaps" (book4 ch6b, ch9; HVEH ch6b, ch9; claims.tsv) | a block of six | #15 unrelated, #16 discussion, #17 PR | replace by a list of the real ones |
| #13 (book1 vol2-dashboard, vol2-contact, chTau-tartaruga, book4 ch10, wp61, wp62, claims.tsv) | `inner_basin_is_asymmetric` / `thm_gronwall_asymmetry` | closest is #32 (O7); #13 is Mather and PB | author decision (R9): re-cite to #32 or file separately |
| #13 / #14 (book8 index, ch5, ch2, notes) | `inner_basin_escape`; ch2 says #14, ch5 and notes say #13 | neither | new issue 3 |
| #13 (GameTheory 710, 718) | Gronwall contraction | #14 | re-cite |
| #14 (poa_research) | Mather step and Poincare-Bendixson | #13 | re-cite |
| #14 (book4 ch9, HVEH ch9, "discretisation bound") | `P_ON(correctOrder) > 0` | unclear: may be T1 (#14) | author decision |
| #15 (claims.tsv rows for vol1) | Theorem T1 | #14 (page already fixed) | regenerate claims.tsv |
| #15 (book4 chIV-orthogonality, 8 places) | `Matrix.minnorm` Mathlib gap | #15 is a trading page | new issue 5 |
| #15 (ch9) | `P_ON(wrongOrder) = 0` | same | new issue 6 |
| #16 (ch9) | no homotopy gamma_K to gamma_F | #16 is a discussion | new issue 7 |
| #16, #18 (claims.tsv rows 80, 81, 115, 116) | regeneration invariant, IPR | #26, #28 (pages fixed) | regenerate claims.tsv |
| #18 (book4 ch11, chpt11, chpt14) | `g_arith` / vonMangoldt | PR | new issue 8 |
| #19 (book4 ch11, chpt11, RH audit) | independence of {log p}, now elementary | PR; filed as #34 under the title "Baker" | retitle #34, re-cite |
| #20 (chpt12, chpt14, claims.tsv 3318, MahloClosure block) | three meanings: digamma critical line, Global Positivity, "closes" in the Mahlo block | PR | new issue 9; re-cite Global Positivity to #33 |
| #21 (chpt13, chpt14 and METHODOLOGY) | p-adic coefficient, and also `certify_rstar_rigorous.py` | not an open issue | new issue 10 |
| #22 (chpt13, chpt14) | Global Positivity = RH itself | not an open issue; #33 states it | re-cite to #33 |
| #6 (GameTheory MahloClosure, ContactHomology) | "last sorry in the Collatz bridge", shown OPEN | #6 is closed on GitHub | state mismatch: page or issue wrong |

## 3. Actions only you can take on GitHub

Close or relabel #15 (unrelated page). Retitle #12 to match what the defect ledger says. Retitle #34 (the chapter now says the independence is elementary, not Baker). Optionally look at the closed list to see which numbers the 7 closed issues hold.

## 4. New issues to file

Ten, with prefilled titles and bodies: open `docs/axle-issues-to-file-2.html` and click each link, then Submit. Nothing above needs checking first: none of the ten is already open. Record each number in `docs/axle-issue-map.md` and write it back to its pages. Per the map's own rule, pages cite a number only after it exists.

## 5. Side effect on today's Book 4 correction

The ch10 correction note and theorem box name #12 for the full nonlinear result. Under this table that should read "the kappa_lipschitz and outer-basin-domain issues (new 1 and 2, not yet filed)".
