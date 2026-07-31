# Site errata — pages not included in this session's corrected files

The corrected `index.html` (deploy to `/GTCT/`, `/GTCT/book4/ch10.html`, and
`geometry/book4/ch10`) already contains all ch10 fixes. The following pages
need the same corrections applied by find/replace. Series-DOI ruling applied
throughout: cite **10.5281/zenodo.19117399** (always resolves to latest).

## book4 hub (`/GTCT/book4/index.html`)

| Find | Replace |
|---|---|
| `r*≈0.773 basin` (Ch 10 blurb) | `r*≈0.77594 basin (certified)` |
| `doi:10.5281/zenodo.19117400` | `doi:10.5281/zenodo.19117399` |
| `0 Sorry in Chain.lean` (stats strip) | `0 sorrys in Chain_updated.lean (registry copy)` |

## Higher-Dimensions Ch 3 (`/GTCT/book4/ch03.html`)

| Find | Replace |
|---|---|
| `r* ≈ 0.8` (all instances: Theorem 3.2, §3.4 box, Fig 3.1 caption, summary) | `r* ≈ 0.77594` |
| `the true boundary is r* ≈ 0.8` | `the true boundary is r* = 0.77594059 (certified by bisection, tol 1e-7)` |
| footer `doi.org/10.5281/zenodo.19117400` | `doi.org/10.5281/zenodo.19117399` |

Note: ch03 prints the dm³ ODE with `e^{-z}` — already correct there.

## Vol IV theory chapters (`chIV-*.html`, footers)

| Find | Replace |
|---|---|
| `doi:10.5281/zenodo.19117400` (footer of every chIV page) | `doi:10.5281/zenodo.19117399` |

## Vol IV Ch 6 — Recursion (`chIV-recursion.html`)

No change to √(5/9) — it is the **correct, derived** chain contraction
(κ²_chain ≤ (2/3)² + (1/3)² = 5/9 from σ_min ≥ 2/3 and ‖u_i w_iᵀ‖ ≤ 1/3).
Optionally add: "κ_chain here is distinct from the dm³ basin marker
κ* = √(7/9) ≈ 0.882 used in Ch 10; the two cannot coincide since
√(5/9) < r* = 0.77594."

## GTCT repo (`github.com/TOTOGT/GTCT`)

1. **`Chain_updated.lean` at repo root is the stale 2026-04-18 draft**
   (2 sorrys, `r_star := 0.8`). Replace with the registry-indexed copy from
   `AXLE:NASA/MoonBase/AXLE_lean_files/Chain_updated.lean`, and update its
   constant to `r_star : ℝ := 0.77594059`.
2. Repo **About/description** cites "(Version 2) … zenodo.20360288" — update
   to Version 4, DOI 10.5281/zenodo.21708678 (or series 19117399).
3. `FINDINGS.md` still documents r* ≈ 0.773 → update to 0.77594059.
4. `dm3_simulation.py` — verify coupling term is `e^{-z}` before shipping in
   the V4 deposit.

## ISBNs

Per ruling: ISBNs are draft placeholders for now; collisions
(979-8-9954416-6-3 listed as both Vol III and Vol V) left as-is, no action.
