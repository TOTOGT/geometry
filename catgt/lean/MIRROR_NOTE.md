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
in `lakefile.lean` (default target). That stanza has not yet been exercised with
`lake build CatGT`; run it once. The dnls mirror is still not a build target.
