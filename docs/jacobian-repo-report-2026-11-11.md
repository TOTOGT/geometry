# TOTOGT/jacobian: issues found, 2026-11-11 (report only; the repo was not changed)

Repo as read: HEAD `a6c5ef4` (2026-07-24), written in the week of Alpoge's announcement (19-20 July 2026).

## 1. The repo has no counterexample
`JacobianCounterexample.lean` is byte-identical to `SpectralDiagonalBound.lean`: a spectral-radius bound on matrix diagonals with two `sorry`s. No polynomial map F, no determinant, no collision appears in any file. README calls it "Counterexample polynomial map formulation". It is not. The Lean cited on `book7/jacobian-verification.html` does not exist here either (CLAUDE.md already recorded: "No .lean file exists in any repo").

## 2. CI is red, one cause
`DualDerivations.lean:35` `split_ifs` fails ("no if-then-else conditions to split") in `jacobian_mul_inverse_eq_one`. All other files build with warnings. Proposed fix, **untested** (no Lean here), kept out of the repo as asked:

```lean
  rw [Matrix.mul_smul, Matrix.mul_adjugate, hdet]
  have h_coeff : (C (-1 / 2 : Q) * C (-2 : Q) : R) = 1 := by
    rw [← map_mul]; norm_num
  rw [smul_smul, h_coeff, one_smul]
```
in place of the `rw [← smul_assoc]` ... `split_ifs` block.

## 3. Other defects
- `lean-toolchain` pins v4.32.1; `[[require]] mathlib` is unpinned, so Lake pulls Mathlib master and auto-switches to v4.36.0-rc2 (seen in the CI log). The build passes only by that accident, and will drift. No `lake-manifest.json` is committed.
- `verify.yml` runs `lake exe cache get` and `lake build` twice and ends with `lake update`; the second pair is redundant.
- `README.md` is pasted chat text, opens "Out with the Jacobian", and its registry marks `dualDerivation_apply_F` as `[PROVED]` while CI fails on the lemma it depends on.
- `Poisson.lean`: `standardPoissonBracket` is `sorry`. `Dixmier.lean`: one `sorry`; both are drafts.
- `DualDerivations` hypothesis `det J = C(-2)` matches the counterexample's determinant, but the module proves only that J times its adjugate-scaled inverse is 1. It does not touch injectivity.

## 4. Local commits in ~/Desktop/jacobian (NOT pushed; the repo is unchanged on GitHub)
`79ccf6c` (DualDerivations fix) and `3a4ab43` (StandardConjectures.lean + lakefile edit). The second would make CI depend on an uncompiled file. Do not push unless you decide to. To discard both: `cd ~/Desktop/jacobian && git reset --hard a6c5ef4`.

## 5. Geometry-side consequence (fixed, see audit-log 2026-11-11)
`book7/jacobian-verification.html` printed a map that is not the counterexample (det = 4x(1+xy)^6, no collision). A correction box is on the page; `book7/jacobian-verification-verify.py` re-runs the check against Gao, arXiv:2608.00222, Thm 3.3.
