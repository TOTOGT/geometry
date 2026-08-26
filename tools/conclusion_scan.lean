/-
  tools/vacuity.lean — the check `#print axioms` cannot make.

  The kernel certifies that a proof establishes its stated proposition. It has
  nothing to say about whether the proposition asserts anything.

  WHY THIS REPO NEEDS IT. Four vacuous or near-vacuous claims have shipped from
  this corpus and passed a kernel check:

    · `g6_equals_schumann : g6_layer_count_nat = schumann_4th_harmonic_integer
      := rfl` — both sides are `def … := 33`. It is `33 = 33` and cannot fail.
      A kernel cannot check a claim about the ionosphere.
    · `basin_asymmetry` was cited as machine-checking the Factor-of-3
      gravitational-decoherence prediction. It is `1/3 < 4/5`.
    · NASAGaps.lean carried `: True := trivial` and `∀ x ∈ S, x ∈ S := id`.
      The second shape is the one a `: True` sweep misses.
    · `UnfoldOp.stable_branch` is satisfied by `n = 0` for every map on every
      type, so "Theorem D (stability)" has no content beyond Φ-decrease.

  As of 2026-08-25 this repository's 31 gated theorems are kernel-checked and
  unverified for content. This file closes that.

  SCOPE — state it as what it checks, never as "not vacuous" in general.
  `#vacuity_scan` and `#vacuity_names` detect trivially inhabited CONCLUSIONS:
  `True`, `∃ _, True`, and conjunctions of those, after `whnf`. Reducing with
  `whnf` is the point — it sees through a definition that unfolds to `True`,
  which a grep for the token `True` cannot. They do NOT detect unsatisfiable
  HYPOTHESES, which is the other thing "vacuous" can mean.
  `#unused_param_scan` detects Prop-definitions that never mention an explicit
  argument, which are true of every subject.

  TWO SCANNERS, BECAUSE OF A NAMESPACE. The G6Crystal and NASAGaps theorems
  live under `Orthogenesis.` and a prefix scan reaches them. SaturnHexagon.lean
  declares its five theorems at top level with no namespace, so no prefix
  isolates them from Mathlib. `#vacuity_names` takes them explicitly, and
  reports MISSING loudly for any name it cannot find — a typo that silently
  scans zero theorems is exactly the failure this file exists to prevent.

  PORTED 2026-08-25 from the Volume I bundle, which runs at Lean v4.14.0. This
  repository pins v4.32.0. The metaprogramming API used here is stable across
  that range as far as I can tell, but that is an expectation, not a check —
  tools/vacuity_fixtures.lean is the check, and it must be run first.
-/
import Lean
import Orthogenesis
import SaturnHexagon
open Lean Elab Command Meta

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

/-- Scan every theorem whose full name starts with the given prefix. -/
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

/-- Scan an explicit list of theorems. For declarations with no namespace.
    A name that is absent, or is not a theorem, is reported and NOT counted
    as scanned, so the caller can assert `scanned=` the number it asked for. -/
elab "#vacuity_names " ids:ident+ : command => do
  let env ← getEnv
  let mut flagged := 0
  let mut total := 0
  let mut missing := 0
  for id in ids do
    let name := id.getId
    match env.find? name with
    | some (.thmInfo ti) =>
        total := total + 1
        let vac ← liftTermElabM <| MetaM.run' (isTriviallyInhabited ti.type)
        if vac then
          flagged := flagged + 1
          logInfo m!"VACUOUS: {name}"
    | some _ =>
        missing := missing + 1
        logInfo m!"NOT-A-THEOREM: {name}"
    | none =>
        missing := missing + 1
        logInfo m!"MISSING: {name}"
  logInfo m!"SCAN-SUMMARY kind=trivial-conclusion-named scanned={total} flagged={flagged} missing={missing}"

/-- Prop-definitions that never mention one of their explicit arguments. -/
elab "#unused_param_scan " pfx:str : command => do
  let env ← getEnv
  let prefixStr := pfx.getString
  let mut flagged := 0
  let mut total := 0
  for (name, info) in env.constants.toList do
    unless name.isInternal do
    if (name.toString).startsWith prefixStr then
      match info with
      | .defnInfo di =>
          let isProp ← liftTermElabM <| MetaM.run' do
            forallTelescopeReducing di.type fun _ b => return (← whnf b).isProp
          if isProp then
            total := total + 1
            let bad ← liftTermElabM <| MetaM.run' do
              lambdaTelescope di.value fun args body => do
                let mut miss := #[]
                for a in args do
                  let d ← a.fvarId!.getDecl
                  if d.binderInfo.isExplicit && !(body.containsFVar a.fvarId!) then
                    miss := miss.push d.userName
                return miss
            if bad.size > 0 then
              flagged := flagged + 1
              logInfo m!"IGNORES-ITS-ARGUMENT: {name} never mentions {bad}"
      | _ => pure ()
  logInfo m!"SCAN-SUMMARY kind=unused-arg prefix={prefixStr} scanned={total} flagged={flagged}"

-- The 26 gated theorems under a namespace.
#vacuity_scan "Orthogenesis."

-- The 5 SaturnHexagon theorems, which have none. These are the same five the
-- axiom gate probes; if a name here goes MISSING the two checks have drifted.
#vacuity_names gate_commutes_onsite angCoupling_not_commute rot_commutes_coupling hex_rotation_invariant hex_coupling_uniform

#unused_param_scan "Orthogenesis."
