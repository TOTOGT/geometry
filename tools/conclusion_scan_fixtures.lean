/-
  tools/vacuity_fixtures.lean — proof that the vacuity scan fires.

  A gate that has never rejected anything is not known to work. This file
  declares the shapes the scan must catch and asserts it catches them. If a
  future edit makes the scan silent, this file is what notices.

  EXPECTED:  scanned=6  flagged=5  — everything except `honest_content`.

  WHY THIS MATTERS MORE THAN IT LOOKS. In the Volume I bundle these fixtures
  once carried `import Mathlib`, the monolithic root module. On a cache miss it
  was never built, the file failed to elaborate, and the run produced zero
  VACUOUS lines. The caller read that as a clean detector when the detector had
  not run at all. **A detector that did not run looks exactly like a detector
  that found nothing.** The CI step for this file must therefore assert the
  SCAN-SUMMARY line is present and reads flagged=5, not merely that no VACUOUS
  line appeared.

  This copy deliberately imports nothing but `Lean` and uses only core `Nat`,
  so it elaborates even when Orthogenesis is broken. That is the point: it
  tests the INSTRUMENT, not the artifact. When it fails, the scanner is wrong;
  when tools/vacuity.lean fails, the corpus is.

  SCOPE. This detects trivially inhabited CONCLUSIONS -- True, ∃ _, True, and
  conjunctions of those. It does not detect unsatisfiable HYPOTHESES, which is
  the other thing "vacuous" can mean. Report it as what it checks.
-/
import Lean
open Lean Elab Command Meta

namespace VacuityFixture

/-- The `NASAGaps.lean` shape, deleted 2026-08: `… : True := trivial`. -/
theorem bare_true : True := by trivial

/-- True under real binders — the shape a conclusion-only reader misses. -/
theorem true_under_binders (n : Nat) (_h : n = n) : True := by trivial

/-- A real hypothesis and a vacuous conclusion: `∃ _, True`. -/
theorem exists_true (f : Nat → Nat) (_hf : f 0 = f 0) : ∃ _g : Nat → Nat, True :=
  ⟨id, trivial⟩

/-- Nested existentials, still vacuous. -/
theorem exists_exists_true : ∃ _a : Nat, ∃ _b : Nat, True := ⟨0, 0, trivial⟩

/-- A conjunction of two vacuities. -/
theorem and_of_trues : True ∧ ∃ _n : Nat, True := ⟨trivial, 0, trivial⟩

/-- NOT vacuous — the control. Must not be flagged. -/
theorem honest_content : (2 : Nat) + 2 = 4 := rfl

end VacuityFixture

-- BEGIN SHARED BLOCK conclusion_scan_core -- see tools/vendor_manifest.json
-- This block is duplicated by design: the fixtures file must elaborate even
-- when the corpus does not, so it restates the scanner rather than importing
-- it. tools/vendor_check.py hashes what lies between these markers in every
-- copy and fails the build if any copy differs. Edit the canonical copy only.
partial def isTriviallyInhabited (t : Expr) : MetaM Bool :=
  forallTelescopeReducing t fun _ body => do
    let body ← whnf body
    if body.isConstOf ``True then return true
    match body.getAppFnArgs with
    | (``Exists, #[_, p]) =>
        lambdaTelescope p fun _ inner => isTriviallyInhabited inner
    | (``And, #[a, b]) =>
        return (← isTriviallyInhabited a) && (← isTriviallyInhabited b)
    | _ => return false

elab "#vacuity_scan " pfx:str : command => do
  let env ← getEnv
  let prefixStr := pfx.getString
  let mut flagged := 0
  let mut total := 0
  for (name, info) in env.constants.toList do
    unless name.isInternal do
    if (name.toString).startsWith prefixStr then
      match info with
      | .thmInfo ti =>
          total := total + 1
          let vac ← liftTermElabM <| MetaM.run' (isTriviallyInhabited ti.type)
          if vac then
            flagged := flagged + 1
            logInfo m!"VACUOUS: {name}"
      | _ => pure ()
  logInfo m!"SCAN-SUMMARY kind=trivial-conclusion prefix={prefixStr} scanned={total} flagged={flagged}"
-- END SHARED BLOCK conclusion_scan_core

#vacuity_scan "VacuityFixture."
