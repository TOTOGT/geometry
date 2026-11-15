# LadderBound.lean and LadderRung.lean: compilation and axiom reports (2026-11-15)

Scope: what these two compiles establish, and what they do not. Recorded by an audit session; nothing here was run by CI.

## Environment (one run, one machine)
- Repository commit: a0e7592e30fa148fb9263829ac4ed234f67f39e0 (local main; contains 6aaee037/e0fbdcd4/5cb25a3c; not yet pushed when run). Files were copied from the working tree; both `.lean` files, `lakefile.lean`, `lean-toolchain` and `tools/axiom_gate.py` are byte-identical to HEAD.
- File SHA-256: LadderBound.lean 29f1cd94397bc9c08bc73a726f7e318c34a009b4d1141ce0d26e8f83d516400e; LadderRung.lean (committed) e110c0ff72f6f9f12ef883d06157f3fa537000bf72e71de430ed939b14ae8ce6; LadderRung.lean (with proposed patch) 6b2db662172f58abdf28b8b05477bee9c1f954b6624743ae69e8b420a0baf33d; axiom_gate.py 9ba06ddb8a340c073337d8ad4c40a1a205aedc1d50d2636009b7a4b62fddb7e2.
- Toolchain: `lean-toolchain` = leanprover/lean4:v4.32.0. Installed with elan 4.2.4; `lake env lean --version` = Lean 4.32.0, x86_64-unknown-linux-gnu, commit 8c9756b28d64dab099da31a4c09229a9e6a2ef35, Release. Linux 6.18.44 x86_64. Not the author's Mac (arm64, darwin).
- Dependencies: Mathlib at rev 81a5d257c8e410db227a6665ed08f64fea08e997 (tag v4.32.0, from `lake-manifest.json`); plausible e12c1910, LeanSearchClient c5d5b8fe, importGraph 7e9612bf, proofwidgets 6e311e2a, aesop a7dbf0c6, Qq 38d591e7, batteries 023ce7d6, Cli 88679d08. Mathlib build artifacts came from `lake exe cache get` (8639 files). CAVEAT: `lake-manifest.json` is listed in .gitignore and is not in the repository; the committed `lakefile.lean` pins only the tag "v4.32.0". The pins above are from the local manifest; a fresh CI resolve is assumed, not shown, to give the same revisions.
- Build setup: a scratch Lake project with the repository's `lean-toolchain` and `lake-manifest.json` and a minimal `lakefile.lean` (`package geometry`, `require mathlib` at the same tag). The repository's own lakefile, with its many other libraries, was not used.

## Commands and exit statuses
1. `lake env lean LadderBound.lean > LadderBound.out 2> LadderBound.err` : exit 0; stderr empty; 7 s. Report: LadderBound.axioms.txt. Two unused-variable linter warnings (half_gap, hax and hxb) and one deprecation warning (`push_neg`, line 151) in stdout; no errors.
   `python3 tools/axiom_gate.py LadderBound.out 6` : exit 0, "OK: 6 theorems, no sorryAx, no axiom outside the permitted set."
2. `lake env lean LadderRung.lean` (file as committed) : exit 1. Two errors, lines 68 and 71: `assumption` failed after `rwa`, because `div_le_iff₀` leaves `c ≤ f * (n + 1)` while the goal is `c ≤ (n + 1) * f` (and the same ordering issue at `f * n ≤ c`). Report: LadderRung.committed.axioms.txt; `ladder_nearest_rung` and `ladder_nearest_rung_rel` depend on sorryAx (the failed steps are elaborated as sorry); `ladder_bracket` does not.
   `python3 tools/axiom_gate.py LadderRung.out 3` : exit 1 (sorryAx in two theorems).
3. `lake env lean LadderRung.lean` with docs/proposed-patches/LadderRung-compile-fix.patch applied (each `rwa` replaced by `rw ...` then `linarith`; two lines changed, no statement changed) : exit 0; stderr and stdout otherwise empty. Report: LadderRung.fixed.axioms.txt; all three theorems depend on exactly [propext, Classical.choice, Quot.sound].
   `python3 tools/axiom_gate.py LadderRung.fixed.out 3` : exit 0, "OK: 3 theorems, no sorryAx, no axiom outside the permitted set."

## What this establishes
- LadderBound.lean (six theorems, as committed) type-checks in the recorded environment with only the three standard axioms.
- LadderRung.lean as committed does NOT compile; with the proposed two-line patch it type-checks with only the three standard axioms. The committed file and its DRAFT/NOT COMPILED header were not changed by this audit; the patch is a proposal.

## What it does not establish
- CI: neither file is in any build target or workflow. No `lean_lib` root names them (lakefile.lean mentions LadderBound only in comments), `.github/workflows/verify-proofs.yml` has no step for either, and no .lean file imports either. A green general `lake build` therefore says nothing about them; it counts only once a target or probe-plus-gate step for them exists.
- A run on the author's machine, or any run other than the one above.
- That the theorems say what Chapter 26 prose says: the statements were not re-read against the prose in this record. LadderBound still takes the bracket as a hypothesis; LadderRung supplies its existence. Neither proves that any particular framework's ladder is wrong (see the file headers).
- Mathlib revisions in a fresh CI environment (manifest not tracked).

## To make it routine (not done here)
Add the two files as targets or a probe step in verify-proofs.yml with `tools/axiom_gate.py ... 6` and `... 3`, and track `lake-manifest.json` or state the Mathlib rev in the workflow.
