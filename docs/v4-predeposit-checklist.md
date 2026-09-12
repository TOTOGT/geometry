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

---

# Second pass — 2026-09-12

Added after integrating the dm³ flow rather than reading it. Everything below is
reproducible by `book7/ch-grothendieck-verify.py`, blocks [3], [4] and [4b],
standard library only.

## 10. FAIL — n_H ≈ 3.64. The formula gives 3.628.

**Item 9 asked the right question and this answers it: the provenance passes.**
`ALGEBRAIC_PROOFS_CH7_CRYSTALLINE_RETURN.md`, Step 4, derives the Hill
coefficient as `n = |μ_max|·π/√3 = 2·π/√3`. So μ_max = −2 is genuinely in it, as
the factor 2, and no Lean declaration is cited in support. The sentence "derived
from μ_max = −2, not fitted" is fine as physics. **No action on item 9.**

**The numeral is another matter.** `2π/√3 = 3.6275987285…`, which is 3.628, or
3.63 to two decimals. **3.64 is wrong by 0.0124.** The source document states
both: Statement (c) says "≈ 3.64", Step 4 of its own proof says "≈ 3.628". A
referee who divides will get 3.628.

It has propagated: `ch18-zeolite-noncommutativity.html` ("n ≈ 3.64 ± 0.4"), the
HVEH proof copies under `docs/ml-evidence/`, and the deposit abstract.

Nothing depends on the difference — the corroborating measurement is
Coelho-Sampaio's laminin–integrin `n ≈ 3.6`, which 3.628 matches at least as well.
**Do:** print the number the formula gives. Fix Statement (c) to agree with Step 4,
then sweep.

## 11. FAIL — μ_max = −2 is listed among the canonical invariants, and it is a limit

**As written:** "The canonical invariants (T\* = 2π, μ_max = −2, τ = 2) … are
closed form".

**What checking finds.** The transverse eigenvalue on Γ = {r = 1} is, exactly,

```
λ(z) = ∂_r ṙ |_{r=1} = 1 − 3 + 2e^{−z} = −2(1 − e^{−z})
```

confirmed to fourteen digits. It equals −2 **only as z → ∞**. At z = 0 it is
exactly 0 — the neutral height Volume II already names. So μ_max = −2 is the
asymptotic rate, not a value the system takes.

**This is the ε₀ defect again, with the same term responsible.** The correction
notice of 2026-08-12 on `chEps-gronwall.html` withdrew the word *basin* for
exactly this reason: the seven ε₀ proofs are correct for the reduced ODE obtained
in the limit z → ∞ where e^{−z} → 0, and the full system's coupling
`2(r−1)e^{−z}` is sign-aware. That correction has already reached this abstract —
it now says "outer stability radius", not "basin". μ_max has not had its turn.

**And the consequence is larger than a word.** On Γ the third equation reads
`ż = 1`. Γ closes in (r, θ) and in no other projection: **it is a helix**. So the
monodromy of one turn does not integrate a constant:

```
∫₀^{2π} λ(z₀+t) dt  =  −4π + 2e^{−z₀}(1 − e^{−2π})
```

RK4 on the variational equation agrees with that to 4×10⁻¹² at nine heights.

| z₀ | multiplier | ÷ e^(−4π) |
|---:|---|---:|
| 0 | 2.567×10⁻⁵ | **7.36** |
| 1 | 7.268×10⁻⁶ | 2.08 |
| 5 | 3.535×10⁻⁶ | 1.014 |
| → ∞ | 3.487×10⁻⁶ | 1 |

`e^{−4π}` is the limit, not the value. **Do:** state μ_max = −2 and T\* = 2π as
invariants *of the z → ∞ reduced system*, exactly as ε₀ = 1/3 now is. Part IV
consumes μ_max twice — the Hill coefficient, and
`v₂ ∝ ε_part·exp(−|μ̂_max| τ_hydro)` — so the paper should say which regime the
prediction is made in. If the intended regime is asymptotic, the fix is one clause
and nothing else changes.

## 12. WHAT SURVIVES — an invariant that does not move

Worth adding rather than only correcting. The multiplier drifts over eight orders
of magnitude; the **fixed-point index of the return map** does not. For an
isolated fixed point with P′(1) = m ≠ 1 it is `sign(1 − m)`, and here:

```
z_c = ln((1 − e^{−2π})/2π) = −1.839746254986…
```

is the single height at which m = 1 exactly. Above it the index is **+1**, below
it **−1**, and it is undefined only at z_c itself. Integer, locally constant,
jumping only at degeneracy — which is what an index is, and what `e^{−4π}` is not.
This also says the flow has exactly one bifurcation in the base point, in closed
form, which the corpus did not previously record.

Volume XI's inherited question sharpens accordingly: *is there a K-theory class
whose pairing is this index?* Not checked, not ruled out. See
`book7/ch-grothendieck.html` and `book6/wp82-the-missing-floor.html` §3b.

## 13. PRE-EMPT — the Tribonacci near-coincidence, killed before deposit

This paper is titled *Seven Proofs of the Tribonacci Constant*. Item 12 introduces
a new constant into the same system, and:

```
|z_c| = 1.839746254986…
η     = 1.839286755214…     (root of x³ = x² + x + 1)
```

They agree to two decimal places and differ by **4.6×10⁻⁴**. In a corpus where η
appears in every volume, someone will notice, and the paper should have noticed
first.

**It is a coincidence.** η satisfies its minimal polynomial to 2.2×10⁻¹⁶; z_c
misses it by **2.5×10⁻³**. η is algebraic of degree 3; z_c is a logarithm of
`(1 − e^{−2π})/2π`. They have no shared construction. **Do:** if z_c enters V4 at
all, state the separation in the same paragraph that introduces it. A near-miss
disclosed by the author is data; the same near-miss found by a referee is the
whole review.

## Passing checks, second pass

* `λ(z) = −2(1 − e^{−z})` matches ∂_r ṙ at r = 1 to 1.4×10⁻¹⁴ — Volume II §4.3 is
  exactly right about the eigenvalue.
* Γ = {r = 1} is genuinely invariant: the radial field vanishes at every height.
* `α ∧ dα = −2r dr∧dθ∧dz ≠ 0` for every r > 0.
* T\* = 2π is correct as the θ-period, which is the only period Γ has.
* Item 9's `n_H` provenance: **passes**, as above. No Lean is cited for it.

---

## Re-measurements of first-pass items, 2026-09-12

**Item 4 — RESOLVED.** `certify_rstar_rigorous.py` is now tracked in two
repositories, `geometry/book4/` and `GTCT/book4/`. The deposit's headline
numerical claim has a producing script under version control. Close it.

**Item on `r*`'s last digit — DEFERRED by decision, 2026-09-12. Do not re-raise.**
Author's call: too small a difference to chase. Recorded here with its size so
that a later pass does not spend the same hour rediscovering it.

The gap is **1.45×10⁻⁸ absolute, 1.87×10⁻⁸ relative** — `0.77594059` against a
certified midpoint of `0.775940575502…`. Nothing in the corpus turns on it: the
ordering the paper actually uses, `ε₀ = 1/3 < 2/3 < r* < κ* = √(7/9)`, holds for
both values with margins of 0.109 and 0.106, seven orders of magnitude larger than
the disagreement. No prediction, no Lean statement and no figure resolves to eight
decimal places. A 133-file sweep to change a digit no argument reads is cost
without a result.

**What remains true, and is the part worth keeping in view.** The count went from
131 to 133, only 4 files carry the certified digit, and the `CLAUDE.md:46` line
the first pass quoted — "canonical r\* is now 0.77594059, not the 0.776 the audit
names" — is no longer in `CLAUDE.md`. The defect is deferred; the *mechanism* is
not, because it is the one this whole checklist is about: a note telling the next
session about a known gap was removed while the gap stayed. If `r*` is ever
restated to more than 8 decimal places, or cited in a context where 10⁻⁸ matters,
this item reopens and the sweep is unavoidable — so the certified interval, not
the rounded digit, is what any new citation should use.

**Superseded first-pass text, kept for the record:** The first pass counted 131 files carrying `0.77594059` against a
certified `0.77594058…`. Today it is **133**, and only **4** files carry the
certified digit. The `CLAUDE.md:46` line the first pass quoted — "canonical r\*
is now 0.77594059, not the 0.776 the audit names" — is **no longer in
`CLAUDE.md`**. So the note that told the next session about the problem is gone
and the 133 files are not. That is the worse of the two possible outcomes: the
checklist said "fix `CLAUDE.md` first, since it is what the next session reads",
and what happened is that `CLAUDE.md` stopped saying it.

**Item 10 scope.** `3.64` appears in 24 files; **22** of them are Hill-coefficient
context. `3.628` appears in 2, one of which is this checklist. Note `D1` states it
as `n ≈ 3.64.00 ± 0.05` in one line and `3.64 ± 0.4` elsewhere — the tolerance
differs by a factor of eight between two statements of one prediction, and
`3.64.00` is not a number.

---

## 14. FAIL — τ = 2 is the same limit as μ_max = −2, and Volume II writes the arrow itself

**As written:** "The canonical invariants (T\* = 2π, μ_max = −2, τ = 2) … are
closed form."

**What checking finds.** Volume II §4.4, in the sentence that produces τ:

> Generator: `LV = −4V(1 − e^{−z}) + σ²`, giving **c → 4**, `κ_noise = 1`, `τ = 2`.

The arrow is in the source. `c → 4` is a limit as `z → ∞`, for the same reason
λ(z) → −2 is, and `τ = √(c/κ_noise)` is therefore 2 in that limit and smaller
below it. Two of the three "canonical invariants" are asymptotic values, and the
same section of Volume II that states them also states the neutral height
`λ(0) = 0` that proves they are not attained everywhere.

**Do:** one clause, covering both. "T\* = 2π is exact; μ_max = −2 and τ = 2 are
the asymptotic values of the reduced z → ∞ system" — the phrasing ε₀ = 1/3 already
received on 2026-08-12, applied to the two constants that did not get it.

## 15. FAIL — the `rfl` sweep item 9 asked for, run. Five more, and the withdrawn one is a build target.

Item 9 said: "grep V4's Lean citations for `rfl` before deposit." Done.

| declaration | statement after unfolding | file |
|---|---|---|
| `tau_is_two : tau = 2 := rfl` | `2 = 2` | `AXLE_v6.lean:555` |
| `g6_is_33 : g6 = 33 := rfl` | `33 = 33` | `AXLE_v6.lean:554` |
| `g6_is_minimum_monster : g6 = 33 := rfl` | `33 = 33` | `AXLE_v6.lean:561` |
| `g64_is_kether_orthogon : g64 = 64 := rfl` | `64 = 64` | `AXLE_v6.lean:562` |
| `g6_equals_schumann := rfl` | `33 = 33` | **18 files** |

with `def g6 : ℕ := 33`, `def tau : ℕ := 2`, `def g64 : ℕ := 64` immediately above.

**`tau_is_two` is the one that matters**, because τ = 2 is in the abstract as a
canonical invariant and this is the only declaration whose name says it is proved.
It proves nothing: τ is *defined* to be 2. `g6_is_minimum_monster` is worse in the
other direction — the name asserts something about the Monster and the statement
is `33 = 33`.

**And `g6_equals_schumann` was withdrawn from the paper, not from the build.** It
is in 18 files, and two of them — `AXLE_v5_1` and `Main_v6` — are explicit
`[[lean_lib]]` roots in `lakefile.toml`. Lake compiles it. A withdrawal that
reaches the prose and not the artifact leaves the artifact citable.

**Do:** delete them, or rename to what they are (`g6_def : g6 = 33 := rfl` is
honest; `g6_is_minimum_monster` is not). Nothing in the paper may cite any of them.

## 16. The sweep needs to cover `decide` and `norm_num`, not only `rfl`

Two lines below `tau_is_two`:

```lean
theorem det_M_equals_64 : tau ^ 6 = 64 := by decide
theorem tau_embodiment  : tau ^ 6 = 2 ^ 6 := by decide
```

These are `2^6 = 64` and `64 = 64`. Same defect, different tactic, and a grep for
`rfl` misses both — while `det_M_equals_64` carries a name asserting a
determinant. Volume II §4.4 also says the threshold values are "Verified by
`norm_num` in Lean 4"; `norm_num` on chosen numerals verifies arithmetic, not that
the numerals are the system's.

**Do:** sweep `rfl`, `decide`, `norm_num` and `simp` alike, under one test —
*could this statement be false if the framework were wrong?* If not, it is not
evidence for the framework.

## 17. RECOMMENDATION — what to do with the K-theory material in V4

**The finding goes in. The programme stays out.**

*In*, because item 11 is not optional: μ_max = −2 must be re-scoped in V4 whatever
else happens, and a correction that cannot say what *is* invariant invites the
obvious question. Item 12 answers it in two lines and a closed form, so the
invariants table gains `z_c = ln((1 − e^{−2π})/2π)` and the index `sign(1 − m)`
beside T\*, ε₀, κ\* and r\*. That converts a withdrawal into a result, in the part
of the paper where closed-form constants already live, and costs a paragraph.
Item 13 travels with it, in the same paragraph, for the reason given there.

*Out*, because K-theory is not this paper. The title has four parts and none is
rung 28; WP-82 says in its own header that it contains no formal results and that
the measurement is the contribution; and the index question is a question — three
untested candidates and no class exhibited. Adding a fifth part to a deposit that
still carries items 1, 2, 5, 7, 8 and 15 unresolved is how a deposit slips a
season. The material has a home already: `book6/wp82-the-missing-floor.html` §3b
and `book7/ch-grothendieck.html`, both in the corpus and both citable. One
sentence of further work in V4 is the right size — *whether a K-theory class pairs
to this index is open, and is Volume XI's first obligation* — and no more.

---

## CORRECTION to items 11 and 14 — 2026-09-12, same day, after reading the deposited source

Items 11 and 14 accused the paper of treating asymptotic values as exact. **That
accusation is wrong and is withdrawn.** It was written from the abstract and from
the Volume II HTML without opening `TOGTnuclearPhysicsB_v3_triplealpha.tex`. The
paper does the drift correctly, in full, and says so.

The Proposition on the local SDE gives the fundamental solution of exactly the
moving-rate problem:

```
Φ(t) = exp( ∫₀ᵗ −2(1 − e^{−s}) ds ) = e² e^{−2t} e^{−2e^{−t}}
```

and its proof states, in the paper's own words, *"at large t the decay rate
−2(1 − e^{−t}) → −2 = μ_max exactly."* The arrow is there. The
time-inhomogeneous SDE is written as time-inhomogeneous. The convergence is
reported numerically — `Var/κ = 0.50455` at t = 5, `0.50003` at t = 10, `0.500000`
by t = 15.

**And the "finding" of item 11 is that Proposition, rederived.** Evaluating the
paper's own Φ at one turn:

```
Φ(2π) = 2.567210665029×10⁻⁵      ← the paper's formula
        2.567210665029×10⁻⁵      ← "7.36 × e^{−4π}" from item 11
        agreement: 3.4×10⁻²¹
```

They are the same number. The variance integral reproduces the paper's three
printed values to every digit. So item 11 did not find a defect; it independently
confirmed a Proposition already in the deposit, and then reported the confirmation
as though it were a correction. That is the precise failure this checklist exists
to catch, committed by the checklist.

**What actually survives, stated at its real size:**

1. **An abstract/body mismatch, and nothing more.** The body marks μ_max = −2 and
   c → 4 as limits; the abstract says "the canonical invariants (T\* = 2π,
   μ_max = −2, τ = 2) … are closed form". One phrase in the abstract does not
   carry a distinction the body makes carefully. That is worth one clause and is
   not a FAIL. Items 11 and 14 are **downgraded to NOTE**.

2. **z_c and the index are still new.** The paper integrates Φ from t = 0. It does
   not ask where the one-turn monodromy crosses 1, and
   `z_c = ln((1 − e^{−2π})/2π) = −1.839746254986` does not appear in it, nor does
   the observation that `sign(1 − m)` is locally constant with a single
   degeneracy. Item 12 stands, and item 13's η separation travels with it.

3. **Item 17's recommendation is unchanged** and is now better supported: the
   paper's dynamics need no correction, so the only reason to touch that section
   in V4 is to add z_c — a small addition to a correct section, rather than a
   repair.

## On the g-series tag — no conjecture is owed

Remark 22.3 cites `(T: nextLevel_layer_count_gt)` for "the g-series taxonomy
identifies g = 33 as the first index at which G exhibits lock-in", and declares
the nuclear-multiplicity correspondence analogical with no derivation offered.

`nextLevel_layer_count_gt` proves `r.layer_count < (nextLevel r).layer_count`,
where `nextLevel` adds 33. Unfolded, it is `n < n + 33` — true for any positive
increment, and carrying no information about 33.

**Under the taxonomy reading that is the right lemma, not a misattribution.** A
taxonomy is a classification with an indexing, and what one machine-checks about
an indexing is that it is well-formed: that the levels strictly increase, so the
ordering is sound and no level collides with another. That is what this theorem
says and all it needs to say. g = 33 is where the taxonomy *places* lock-in; it is
a label, not a prediction, and a label owes no derivation. The remark already
refuses the one claim that would owe one — the nuclear correspondence — and marks
it as a modelling target.

Contrast with `g6_is_minimum_monster : g6 = 33 := rfl` in item 15. The difference
is not the proof, which is equally trivial in both; it is the **name**. A
well-formedness lemma named for well-formedness is honest bookkeeping. The same
triviality named for the Monster asserts, in the only part a reader skims, a
result no one has. Item 15 stands on that ground and not on the triviality.
