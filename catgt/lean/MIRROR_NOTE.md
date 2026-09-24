# CatGT_Main.lean — mirror copy

This folder holds a MIRROR of `CatGT_Main.lean`. The canonical copy lives in
`TOTOGT/io` (local: `~/Desktop/io/CatGT/CatGT_Main.lean`), which pins Lean v4.14.0
and is what the paper cites. Edit the canonical copy first, then mirror the change here.

- Theorem statements must match the canonical copy exactly. Only proofs may differ, and
  only where a Lean/Mathlib bump forced it; mark each such line with `-- COMPAT: <reason>`.
- Check for drift (read-only): `bash ~/Desktop/Claude\ outputs/catgt-sync-check.sh`.
- This folder is NOT a build target until it is wired into the repo's `lakefile.lean`.
  Until then nothing compiles it automatically. A hand run proves the file on the day it is
  run and nothing afterwards. Suggested wiring:

  ```lean
  @[default_target]
  lean_lib CatGT where
    srcDir := "catgt/lean"
    roots := #[`CatGT_Main]
  ```

Status when copied (2026-09-20): compiled clean on Lean 4.32.0 / Mathlib v4.32.0 (owner's
`lake env lean`), 13/13 `#print axioms` on [propext, Classical.choice, Quot.sound]. Not yet
checked on v4.14.0 (io's CI pin).

Update (2026-09-20, late): in THIS repo (geometry) the folder is now wired as `lean_lib CatGT`
in `lakefile.lean` (default target). `lake build CatGT` was then run by the
owner (2026-09-20): completed, 8656 jobs, 13/13 `#print axioms` on [propext, Classical.choice,
Quot.sound], 5 unused-binder warnings, no errors. Still not checked on v4.14.0 (io's pin). The dnls
mirror is still not a build target.

Update (2026-09-21): CI (verify-proofs.yml) now gates the 13 theorems via
tools/verify-catgt/probe_catgt.lean -- sorryAx and non-standard axioms only.

Update (2026-09-23): checked on v4.14.0 (io's pin) — owner ran
`lake env lean ~/Desktop/io/CatGT/CatGT_Main.lean` from the local AXLE checkout
(Lean/Mathlib v4.14.0): no errors, 13/13 `#print axioms` on [propext, Classical.choice,
Quot.sound], 5 unused-binder warnings. Header comment updated in both copies (comment only,
copies still identical).

Update (2026-09-24): §4b (5 theorems, r* normalisation) and §4c (5 theorems, sech relation
derived from the continuum DNLS equation) added; 23 theorems. Owner's runs: v4.14.0 via the
AXLE checkout, no errors; v4.32.0 `lake build CatGT` completed (8656 jobs). The two
derivative proofs carry `-- COMPAT` lines: `h1.cosh`/`h1.sinh` and `congr_deriv` replace
`.comp`/`convert` because v4.32 returns Pi-form functions from `HasDerivAt.inv/div/mul`.
Copies byte-identical. CI gate (verify-proofs.yml) now expects 23.
