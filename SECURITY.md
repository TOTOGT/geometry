# Security Policy

## Supported Versions

Orthogenesis is a **Lean 4 formal verification library**, not executable software.
There are no network services, authentication systems, or user-facing binaries.
The security model is therefore different from a typical software project.

| Component | Version | Supported |
|-----------|---------|-----------|
| Lean 4 toolchain | `leanprover/lean4:v4.14.0` | ✅ Current |
| Mathlib4 | `v4.14.0` (rev `4bbdccd`) | ✅ Pinned in `lake-manifest.json` |
| Orthogenesis library | `main` branch | ✅ Active development |
| Older Mathlib revisions | `< v4.14.0` | ❌ Not tested |

The pinned Mathlib revision in `lake-manifest.json` is the single source of truth
for reproducibility. All theorems are verified against that exact revision.

## What "Security" Means Here

For a formal verification library, the relevant threats are:

**1. Proof soundness**
A `sorry` in the codebase is an unverified axiom — the formal equivalent of a
security vulnerability. Every `sorry` is tracked by name in the
[proof status table](./README.md#lemmas-and-proof-obligations) with its NASA gap
code and documented closure path. The current open obligations are:

| ID | Name | Status |
|----|------|--------|
| M2 | `heliSpin_incommensurate_aperiodic` (`MagneticLattice.lean:240`) | Open — needs irrationality of q/2π and a Weyl equidistribution argument |
| Q2 | `detune_from_ground_period` (`SeismicLattice.lean:211`) | Open — needs a damped forced-oscillator response model |

Those two are the only admitted declarations inside a `lake build` target. Four
more sit in files that are in no target — `CollatzDescent.lean` (2), the root
copy of `Coverage.lean` (1), `AMonster/GenerativeWeave.lean` (1) — and the build
never reads them. Six in total; the package is not sorry-free and no document
should say that it is.

No `sorry` is hidden. `stage_bound`, `expand_mono`, `expandN_mono`,
`hex_beats_square`, `coord_coverage`, `no_coord_collision` and
`nasa_gap_closure_summary` are proved, and the CI axiom gate
(`tools/axiom_gate.py`) reports `[propext, Classical.choice, Quot.sound]` with
no `sorryAx` for every theorem it covers. A kernel check certifies that a proof
establishes its stated proposition; it says nothing about whether the
proposition asserts anything, which is a separate audit.

<sub>Corrections, 2026-08-21, amended 2026-09-11. The earlier S1/S2/S3 table
named none of the repository's admitted declarations. S2 read
`: True := trivial` and was deleted on 2026-08-21; S3 `coord_coverage` was
proved; `no_coord_collision` was false as stated and now carries the separation
hypothesis it requires. S1 `arnold_tongue_A4_coupling` was reported deleted on
2026-08-21 and was not: it read `∀ δ : ℝ, ‖δ‖ < noise_tolerance → True`, a
conclusion of `True` behind an implication, which the vacuity scan's
`: True := trivial` pattern does not match. It was deleted on 2026-09-11 with
G6Crystal §4, and `verify-proofs.yml` now scans for the implication form as
well. The lesson is the one this section already states: a kernel check
certifies that a proof establishes its proposition, not that the proposition
asserts anything — and a textual scan certifies only the shapes it was written
to look for.</sub>

**2. Dependency integrity**
The Mathlib revision is pinned. Do not update `lake-manifest.json` without
re-running `lake build` and confirming all theorems still compile.

**3. Axiom transparency**
The only axioms used beyond Lean 4's kernel are those inherited from Mathlib4.
No custom axioms have been added. Verified with:
```
lake exe cache get && lake build
grep -r "axiom " Orthogenesis/
```

## Reporting a Vulnerability

**If you find a `sorry`-free proof of a false theorem** (i.e., a soundness issue
in the Lean 4 kernel or Mathlib), this is a critical issue affecting the entire
Lean ecosystem. Report it to:

- The Lean 4 core team: https://github.com/leanprover/lean4/security
- The Mathlib4 maintainers: https://github.com/leanprover-community/mathlib4/security

**If you find an error in an Orthogenesis proof** (a theorem that claims to be
proved but whose proof is incorrect or relies on a hidden gap), open an issue
at https://github.com/TOTOGT/geometry/issues with the label `proof-error`.
Include the theorem name, the file, and a description of the gap.
You can expect a response within 7 days.

**If you find a `sorry` that is not listed in the tracking table**, open an issue
immediately. Undisclosed `sorry`s are treated as the equivalent of a security
vulnerability in this project.

## Contact

Pablo Nogueira Grossi · G6 LLC · Newark, NJ
g6llc@proton.me · ORCID: 0009-0000-6496-2186
GitHub: https://github.com/TOTOGT
