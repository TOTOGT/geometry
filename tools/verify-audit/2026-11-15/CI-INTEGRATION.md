# Ladder files: repository integration and CI step (2026-11-15)

Follows RECORD.md (same directory). RECORD.md covered a scratch project; this note covers the repository configuration. It is a record of what was changed and what was run, and of what has NOT yet run.

## Changes
- `LadderRung.lean`: proposed patch applied (two `rwa` steps -> `rw` + `linarith`; no statement changed); header status rewritten to the recorded facts (compiles in the recorded environments; correspondence with Chapter 26 not reviewed; CI result not recorded; not run on the author's machine). SHA-256 after: aa5c28d7c139940ac2bab81363fb61d256bd6a254cbed7383038adbfd5a92075.
- `lakefile.lean`: `lean_lib LadderBound` and `lean_lib LadderRung`, both `@[default_target]`, so the existing `lake build` step compiles them; comments about LadderBound being outside every target revised. SHA-256 after: 4ca5e535aabbe7840d6e05f7b77a5505e653c048198f2fd0669960202b3363de.
- `.gitignore`: `lake-manifest.json` no longer ignored; the manifest used for the recorded compiles is to be committed (SHA-256 8e19b34f0a72c85e55e077d5f89004c38a7907eaeacbd545eb035dee80787f8e; Mathlib rev 81a5d257c8e410db227a6665ed08f64fea08e997).
- New `tools/verify-ladder/`: `run.sh` (the one script, run locally and by CI), `check_pins.py`, `pins.txt` (expected toolchain and Mathlib rev), `probe_ladder.lean` (9 `#print axioms` through the library targets).
- `.github/workflows/verify-proofs.yml`: new steps "Kernel axiom check on the Ladder files (LadderBound, LadderRung)" (runs `tools/verify-ladder/run.sh`) and "Keep the Ladder logs" (`actions/upload-artifact@v4`, `if: always()`), placed before the CatGT step. The existing `lake update` step is unchanged.

## What run.sh does
Runs every step even after a failure, writes each exit status to `status.tsv`, and exits non-zero if any failed: (1) pins: `lean-toolchain`, committed `lake-manifest.json` and the resolved `.lake/packages/mathlib` HEAD against `pins.txt`; (2) `lake build LadderBound LadderRung`; (3) `lake env lean LadderBound.lean` and `tools/axiom_gate.py ... 6`; (4) `lake env lean LadderRung.lean` and gate `... 3`; (5) `lake env lean tools/verify-ladder/probe_ladder.lean` and gate `... 9`.

## Run recorded here (a simulation of the repository configuration, not CI)
Cloud container, Lean 4.32.0 (commit 8c9756b2), Linux x86_64, with the real `lakefile.lean`, `lake-manifest.json`, `lean-toolchain`, `LadderBound.lean`, `LadderRung.lean`, `tools/axiom_gate.py` and `tools/verify-ladder/*` from the working tree, and the Mathlib build from `lake exe cache get`. Not a git checkout (the `commit:` line is empty); the other files of the repository, including the other `lean_lib` sources, were absent, so `lake build` was limited to the two targets. Result: all eight steps exit 0 (`ladder-run.status.tsv`), gate OK for 6, 3 and 9 theorems, pins match; `lake build` completed (8658 jobs) with the same three axioms reported by the build itself.
Controls on `check_pins.py`: altered Mathlib rev in `pins.txt` -> exit 1 (manifest and resolved checkout both flagged); altered toolchain -> exit 1; restored -> exit 0. The committed (unpatched) `LadderRung.lean` was already shown in RECORD.md to fail compilation and the gate (exit 1); the full `run.sh` was not re-run against it.

## Not established
- CI has not run these steps. Whether the job passes on GitHub is unknown until it does; this note does not claim it.
- The existing step `lake update` runs before the Ladder step in CI and can move packages; `run.sh`'s pin check is what would catch a moved Mathlib revision. It does not fail on drift in the other packages (plausible, aesop, batteries, ...), which are recorded in the manifest only.
- A full-repository `lake build` with every target was not run here.
- Statements versus Chapter 26: not reviewed here (pending).
- Mac run: not done.
