# verify-book8

One command, run from anywhere in the repo:

```bash
bash tools/verify-book8/run.sh
```

It does exactly what CI does, in the same order:

1. `lake build OrthogonalWitness` — compiles `book8/OrthogonalWitness.lean`.
   **Compilation is not verification.** A theorem proved with `sorry` compiles
   with a *warning*, not an error, so a green build here means nothing on its own.
   Note also that `#print axioms` emits **info**, not an error: a `sorryAx` would
   scroll past inside a build that still reports success. Step 3 is what refuses.
2. `lake env lean probe_book8.lean` — asks the **kernel** which axioms each of the
   4 named theorems actually depends on.
3. `python3 tools/axiom_gate.py axioms.txt 4` — fails if any theorem reports
   `sorryAx`, if any axiom falls outside the allowlist, or if the **count** is not
   4. The count matters: without it, a theorem quietly dropped from the probe
   would shrink the check instead of failing it.

First kernel run: 2026-08-27, `leanprover/lean4:v4.32.0`. All four on
`[propext, Classical.choice, Quot.sound]`.

## What is checked

| group | theorems |
|---|---|
| hyperboloid constraint / proper time | `on_hyperboloid`, `proper_time` |
| the throat | `radius_has_throat`, `throat_value` |

## What those four actually say

Read the count as four *names*, not four independent facts.

- `on_hyperboloid` and `proper_time` are the same Mathlib fact,
  `cosh² − sinh² = 1`, in two dresses — the first multiplied by ℓ², the second
  negated. Both are named because the chapter cites both.
- `on_hyperboloid` states the **ω-reduced** constraint: `‖ω‖² = 1` is substituted
  by hand into the statement rather than carried as a hypothesis, so the theorem
  is an identity in two real variables. No metric, manifold, pullback or normal
  bundle appears anywhere in the file.
- `radius_has_throat` is stated for `0 ≤ ℓ`. At ℓ = 0 it is true but empty, since
  Lean's `τ / 0 = 0` gives `a 0 τ = 0 ≤ 0`. The geometry needs `0 < ℓ`. The
  hypothesis does real work in the proof, so this is a weak statement, not a
  vacuous one.
- `throat_value` is `cosh 0 = 1`.

None of the four is vacuous in the gate's sense: no `True`, no unsatisfiable
hypothesis, no conclusion independent of its hypotheses.

## What is NOT checked, on purpose

- **The tensor pullback** — the step that would make "induced metric" a proved
  phrase rather than a docstring phrase. It is verified in sympy (exact symbolic,
  zero difference matrix) and that is a different tool making a different claim.
  It is not in the kernel and no Lean declaration for it exists to name.
- **Leg 2, the epistemic claim** (Tarski's undefinability; Frauchiger–Renner;
  Local Friendliness). A logical result, not a geometric one. Conflating the +1
  dimension with the +1 meta-level is the error the chapter exists to prevent.
- **`witness_codimension`.** `5 - 4 = 1` on ℕ literals closes by `rfl` whether or
  not anything about normal bundles holds, and truncated subtraction makes
  statements of that shape true for reasons unrelated to geometry. It is recorded
  as a comment in the header, where a remark belongs.

Cite these four as what they are: the scalar identities the embedding must
satisfy, machine-checked. Not the embedding theorem.
