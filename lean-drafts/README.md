# lean-drafts: DRAFT, status per file

Files in this folder are drafts written 2026-11-26 without a Lean toolchain. They are not part of the default build and do not affect the other workflows. The workflow `verify-lean-drafts.yml` compiles them on every push and reports the declaration-specific axiom list for each theorem. Until that workflow is green and the statements have been read against their names, nothing here is formally verified.

| File | Content | Status until CI is green |
|---|---|---|
| ContactJacobian.lean | T1 real determinant of multiplication by a complex number; T1 derivative form; T2 contact coefficient and its nondegeneracy at simple zeros (coefficient level only, no differential forms); T5 energy dissipation under positive-semidefinite mobility (operator form); T3 harmonic quadratic and quartic at coefficient level | Specification, uncompiled |
| LegalPossibility.lean | Admissible and accessible trajectories in a procedural system, accessible implies admissible, resource monotonicity under an explicit assumption, remedy reachability, and the eight Hohfeld positions with correlatives and opposites | Specification, uncompiled |
| legal_transition_demo.py | Deterministic Python example: a legally available remedy that cannot be reached for lack of money, a non-monotone means-tested case, and a deadline case. Toy numbers, not law, not data | Numerical, passes its own assertions |

Known limits. The Laplacian coefficients in ContactJacobian.lean are computed by hand and not tied to Mathlib's Laplacian. The matrix form of positive-semidefinite mobility is not bridged. The statements about legal positions are about a constructed model and do not establish substantive law. Nothing in this folder is advice about any legal situation.
