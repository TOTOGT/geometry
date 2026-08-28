# V4 pre-deposit checklist — TOGT / Nuclear Physics B

Contact-Geometric Theory of Generative Transitions: Mathematical Foundations,
Contact Realization, Seven Proofs of the Tribonacci Constant, and Applications to
Nuclear Matter.

Draft: `zenodo.org/uploads/22135179`. Superseding V3, `10.5281/zenodo.21206925`
(5 July 2026). Concept DOI `10.5281/zenodo.20682933` still resolves to V3.

Checked 2026-08-28 against the V3 record text and the repositories in
`tools/corpus_roots.txt`. Every item below is a claim in the paper that a reader
could check; the ones marked FAIL are the ones that do not survive checking.
Items are ordered by what a referee would catch first.

---

## 1. FAIL — Theorem D is not a theorem

**As written:** under *Certified without sorry*, "Operator sequence: GenerativeOp
(Theorem A), UnfoldOp.stable_branch (Theorem D)".

**This is not a new finding.** `docs/audit-log.md:95`, in the 2026-08-24 editorial
pass on the Volume I V7 release, already classes it **VACUOUS** and gives the
argument in one line: take n = 0, `f^[0] = id`, every point is a fixed point of
the identity — so the field is satisfied by *every map on every type*. The log
also records that V7 proves the vacuity rather than only noting it in a comment.
It was found, written down, and the deposit still carries the claim. That gap
between the log and the deposit is the defect worth fixing, more than the field
itself.

**What checking finds:** `stable_branch` is a **structure field**, declared at
`AXLE/lean/main_v7.lean:133` and `AXLE/lean/Main_v5.lean:202` as

```lean
stable_branch : ∀ x, ∃ n : ℕ, Function.IsFixedPt (map^[n]) (map x)
```

It is a hypothesis carried by every `UnfoldOp`, not a result about one. Nothing
proves it; anything using an `UnfoldOp` assumes it. The repository says so itself,
in `AXLE/lean/NonCommutativity_instance.lean:102–106`:

> U := identity. decreases_Phi and stable_branch both hold trivially
> (stable_branch is in fact trivially true for *any* map, for any x…)
> **UnfoldOp.stable_branch constrains nothing.**

`AXLE/lean/regeneration_loop_invariant.lean:13` also carries
`:= sorry  -- from UnfoldOp.stable_branch after threshold`.

**Do:** remove it from the certified list. If Theorem D is to stay in the paper,
it needs a `theorem` that *discharges* the field for a named, non-trivial `U` —
the identity instance the repo already flags will not do, precisely because it
holds for any map.

## 2. FAIL — Theorem A is a definition

**As written:** "GenerativeOp (Theorem A)" under *Certified without sorry*.

**What checking finds:** `GenerativeOp` is a `def`, in 29 files across AXLE. A
definition cannot be sorry-free-in-the-sense-the-list-means; there is nothing to
prove.

**Do:** either cite the theorem *about* `GenerativeOp` that Theorem A actually is,
or move the name to a "definitions" line. Prose that calls a `def` a theorem is
the exact failure this list exists to prevent.

## 3. FAIL — "13 significant figures" is one digit too many

**As written:** "r\* ∈ [0.775940575501953125, 0.77594057550234375] (width
3.9×10⁻¹³, 13 significant figures)".

**What checking finds:** the width is right — 3.90625×10⁻¹³, which rounds to
3.9×10⁻¹³. The digit count is not. The two endpoints are

```
0.775940575501953125
0.775940575502343750
```

They agree through the 11th significant digit and diverge at the 12th. A width of
3.9×10⁻¹³ on a value near 0.776 determines roughly 12 significant digits, not 13.

**Do:** replace with "width 3.9×10⁻¹³; the endpoints agree to 11 significant
digits". A referee who subtracts the endpoints will do this subtraction.

## 4. FAIL — the producing script is not in any repository

**As written:** "New script `certify_rstar_rigorous.py` accompanies the deposit."

**What checking finds:** a `find` across every repository and working directory
reachable from this session returns exactly one `certify_rstar_rigorous.py`, in
`~/Downloads`. It is in no git repository, so it is in no corpus root, and nothing
versions it. The deposit's headline numerical claim has no producing script under
version control.

(The older `certify_rstar.py` — the superseded bisection script — is the opposite
problem: nine copies on disk, seven of them tracked, across AXLE ×3, geometry ×2,
GTCT and 3M. CLAUDE.md says seven locations; there are nine now.)

**Do:** move it into AXLE (or GTCT, beside the r\* section it certifies), commit
it, and cite the repository path in the paper alongside the deposit copy. This is
the repo's own reproducibility rule applied to its own most-cited number.

## 5. FAIL — the V3 record still describes V2

**As written, on the live V3 record:** a section headed "What V2 fixes", and
"Deposit contents: `TOGTnuclearPhysicsB_v2.pdf` — 42-page paper (this file)".

**What checking finds:** the file list on that record contains
`TOGTnuclearPhysicsB_v3_triplealpha.pdf` and
`TOGTnuclearPhysicsB_largeprint_figs (1).pdf`. There is no `_v2.pdf` in it. The
description says "this file" about a file that is not there.

Also in the published file list: `files (31).zip`. A download-folder name in a
deposit's permanent record.

**Do:** for V4, write a "What V3 fixes / What V4 fixes" section that matches the
files actually uploaded, and rename the zip to something that names its contents.

## 6. CHECK THE SCOPE — "48+ proved · 17 admits · 0 hidden sorries"

Not marked FAIL, because the numbers may be scoped to a named file set the
description does not state. But as a corpus figure they do not hold: a tracked
census of AXLE finds 1369 declarations, of which **158** have `sorry` in the
proof body. "17 admits" is not the repository's number.

"Proved" is also the kernel-audited word. Of the corpus, 30 declarations are
kernel-audited per the registry. Sorry-free is not proved — `True := by trivial`
is sorry-free.

**Do:** name the file set the 48/17/0 count is over, in the sentence that makes
the claim, or restate it as "48 sorry-free declarations in ⟨these files⟩".

## 7. FAIL — the second structure field, already logged and not yet in the paper

`docs/audit-log.md` (2026-08-24) classes `CompressionOp.contractive` as
**MISMATCH**. The field reads `d(fx,fy) ≤ d(x,y)`, which is *non-expansive*, not
contractive: a contraction needs `≤ k·d(x,y)` with `k < 1`. The identity satisfies
it — and `C_ex`, the deposit's own witness, is exactly the identity.

**Do:** Assumption 3 should say "non-expansive". If the paper's argument anywhere
needs an actual contraction, that step does not currently have one.

## 8. UNRESOLVED — ε₀ = 1/3 does not close as printed (obligation O7)

Logged 2026-08-24, still open. Three statements that cannot all hold: the formula
at H = 3 gives 2/(2·4) = 1/4; the printed arithmetic `2/(2·3)` corresponds to
H = 2; the Lean line `2/(2*(1+2))` is H = 2. The formula and the Lean agree; the
sentence naming the constant disagrees with both. `epsilon0_of_eq_third_iff`
proves 1/3 is forced for exactly one Hessian bound, H = 2.

The log is explicit that this is not decidable in Lean — it turns on which Hessian
bound enters the Gronwall estimate, `V''(1) = 6` or `|L₂| = 3`, which is physics.

**Why it matters for V4:** ε₀ = 1/3 is load-bearing corpus-wide, and this paper
states it among the closed-form invariants. A referee who follows the arithmetic
reaches the same three-way disagreement. Either close it or state O7 in the paper
as an open obligation, as the log says the deposit already does.

## 9. PRECEDENT — two defect classes to sweep V4 against before deposit

Both were found in the same pass and both are the kind that recur:

**MISATTRIBUTED.** The Factor-of-3 Prediction carried "This is machine-checked
(Lean: `basin_asymmetry`: 1/3 < 4/5)". `basin_asymmetry` is an inequality between
two rationals; it says nothing about gravitational decoherence. No kernel checks a
physical prediction. Withdrawn. **V4 contains at least one structurally identical
sentence to check**: "The Hill coefficient n_H ≈ 3.64 is derived from μ_max = −2,
not fitted." If any Lean declaration is cited in support of that, it is the same
defect; if none is, the sentence is fine as physics.

**UNFALSIFIABLE GUARD.** `theorem g6_equals_schumann : g6_layer_count_nat =
schumann_4th_harmonic_integer := rfl` — both sides definitionally 33. It is
`33 = 33`, and it was counted among the machine-checked facts. Withdrawn. Any
`:= rfl` between two definitions the author chose is this defect; grep V4's Lean
citations for `rfl` before deposit.

---

## Passing checks — no action

* Interval width 3.90625×10⁻¹³ matches the stated 3.9×10⁻¹³.
* κ\* = √(7/9) = 0.881917103688… matches the stated ≈0.8819.
* The ordering ε₀ = 1/3 < 2/3 < r\* < κ\* holds for the certified midpoint.
* The wrapping-effect account (naive interval arithmetic inflating error ~5×10⁵
  by t = 7, replaced by Jacobian transport plus interval-Hessian remainder) is
  internally consistent and reports a negative result, which is the right way to
  report it.
* Proofs 3 and 4 are disclosed as admits rather than counted among the seven as
  complete. The title says seven proofs; the body says five are Lean-ready. That
  is disclosed, not hidden.

---

## Two repository defects the paper depends on

Not in the paper, but they will contradict it after publication.

**`r*` is wrong in the 8th decimal, in 131 files.** `geometry/CLAUDE.md:46` reads
"canonical r\* is now 0.77594059, not the 0.776 the audit names". The deposit's
certified midpoint is `0.7759405755021484…`, which is `0.77594058` at 8 decimal
places — not `0.77594059`.

`0.77594059` appears in **131** files across `geometry`, `AXLE`, `GTCT` and `3M`
(`.html`, `.md`, `.py`, `.lean`). Every one of them disagrees in the last digit
with the interval the paper certifies. The correction that made the constant more
precise never propagated to the constant itself.

Fix `CLAUDE.md` first, since it is what the next session reads, then sweep the
131.

**The seven `certify_rstar.py` copies still cite the wrong DOI.** CLAUDE.md
records this as *Resolved 2026-07-30*: cite GTCT's own `10.5281/zenodo.20360288`,
not a series-level DOI, and "fix all 7 copies in the same edit". Checked today,
six reachable copies:

| copy | cites |
|---|---|
| `Desktop/3M/certify_rstar.py` | 19117399 |
| `Desktop/AXLE/AAlpha_Linkedin/certify_rstar.py` | 19117400 |
| `Desktop/AXLE/LAW3M/certify_rstar.py` | 19117399 |
| `Desktop/GTCT/book4/certify_rstar.py` | 19117400 |
| `Downloads/certify_rstar.py` | 19117400 |
| `Downloads/helical-contact-repo/certify_rstar.py` | 19117400 |

None cite 20360288. The edit was recorded as done and was not done — which is the
same class of defect as a published number with no producing script: a claim in
the record that nothing checks.

---

## New this pass

`AXLE/TripleAlphaDm3.lean` — the three-body ladder, Mathlib-free, compiled under
Lean 4.14.0 with `EXIT=0`, no `sorry`, no `native_decide`. `#print axioms` reports
`[propext, Quot.sound]` on five declarations and no axioms at all on `tribo_rec` —
fewer than the three standard kernel axioms, since nothing in it is classical.

It proves the ordinal form of φ < η < τ: each term strictly exceeds the sum of the
two before it, and every term past the first is strictly below 2ⁿ. The bound is
tight — `tribo n < 2^n` is false exactly at n = 0.

It proves no physics, and its header says so. If V4 cites it, cite it for the
bracket and not for the triple-alpha identification, which remains a modelling
claim of the prose.

Wired into `lakefile.toml` as its own `[[lean_lib]]` target, because a file that is
no target's root is compiled by nothing.

---

## What this pass can and cannot attest

Stating the boundary, because the difference between these two is the subject of
the whole checklist.

**Can attest.** `TripleAlphaDm3.lean` compiles: Lean 4.14.0, `EXIT=0`, no `sorry`,
`#print axioms` output read directly. Declaration resolution across all eleven
corpus repositories: whether a name exists, in a tracked file, as a `theorem` /
`def` / `axiom`, and whether `sorry` appears in its body. Arithmetic on the stated
constants. File and DOI inventory.

**Cannot attest.** That any Mathlib-dependent file in AXLE, GTCT, `vol1-proofs`
or CatGT elaborates. There is no Mathlib available to this session and no cache
reachable, so nothing in those files was built. Every statement here about them is
Tier 2 at best — the declaration exists and has no `sorry` in its body — and Tier 2
is exactly the level at which `stable_branch` looked fine for months.

The honest summary: today's file is the only one in this corpus that this session
watched a kernel accept.
