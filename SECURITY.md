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
| S1 | `arnold_tongue_A4_coupling` | Open — requires ODE flow theory in Mathlib |
| S2 | `hexagrid_collapse_resistance_superior` | Open — requires FEM formalisation |
| S3 | `coord_coverage` | Open — ring-walk cardinality, tracked in `Coverage.lean` |

No `sorry` is hidden. The claim "0 sorry on structural claims" means the
load-bearing theorems (`stage_bound`, `expand_mono`, `hex_beats_square`,
`no_coord_collision`, `nasa_gap_closure_summary`) are all fully proved.

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
grossiatwork@gmail.com · ORCID: 0009-0000-6496-2186
GitHub: https://github.com/TOTOGT
