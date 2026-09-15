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

## Rule

A number in this corpus is a citation. Before writing one, check it here or at
the source. Numbers are not reassigned by renumbering the corpus: if an
obligation has no issue, state the obligation and leave the number out.
