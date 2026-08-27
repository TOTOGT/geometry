# verify-dm3

One command, run from anywhere in the repo:

```bash
bash tools/verify-dm3/run.sh
```

It does exactly what CI does, in the same order:

1. `lake build` — compiles `Orthogenesis`. **Compilation is not verification.**
   A theorem proved with `sorry` compiles with a *warning*, not an error, so a
   green build here means nothing on its own.
2. `lake env lean probe_dm3.lean` — asks the **kernel** which axioms each of the
   28 named theorems actually depends on. This is the step that can see a
   `sorry`, because an admitted proof reports `sorryAx`.
3. `python3 tools/axiom_gate.py axioms.txt 28` — fails if any theorem reports
   `sorryAx`, if any axiom falls outside the allowlist, or if the **count** is
   not 28. The count matters: without it, a theorem quietly dropped from the
   probe would shrink the check instead of failing it.

## What is checked

28 theorems across two files. The authoritative list is the probe itself —
`grep -c '#print axioms' tools/verify-dm3/probe_dm3.lean` must equal the `N` in
`run.sh`, and this table must match both.

### `Orthogenesis.G6Crystal` — 14

| group | theorems |
|---|---|
| canonical invariants | `dm3_Tstar_pos`, `dm3_mumax_neg`, `dm3_tau_pos`, `dm3_tau_eq_abs_mumax` |
| stability radius | `dm3_epsilon0`, `epsilon0_of_one`, `epsilon0_of_two`, `epsilon0_of_eq_third_iff`, `epsilon0_of_antitone`, `dm3_noise_tolerance`, `dm3_noise_tol_lt_one` |
| dimensional derivation | `aspect_ratio_eq`, `aspect_ratio_encoded`, `layer_height_cubits` |

`epsilon0_of_antitone` is the load-bearing one: a stiffer potential gives a
narrower stability band. `dm3_epsilon0` on its own restates a definition and is
evidence of nothing; it is named so a change to it fails the count.

### `Orthogenesis.ToyModel` — 14, added 2026-08-26

| group | theorems |
|---|---|
| flow on the curve | `rdot_on_gamma`, `zdot_on_gamma` |
| transverse eigenvalue | `transEig_hasDerivAt`, `transEig_eq_deriv`, `eigenvalue_neg_pos_z`, `transEig_zero`, `transEig_gt_neg_two`, `transEig_strictAnti`, `transEig_tendsto_muMax` |
| τ and ε₀ | `toyModel_tau`, `toyModel_tau_eq_abs_muMax`, `eps0_at_hessian_two`, `eps0_at_hessian_three`, `eps0_eq_third_iff` |

`rdot_on_gamma` and `zdot_on_gamma` are the two `vol2-toymodel.html` cites on its
Lean badges; the rest are the facts those two rest on, named so that the badge
cannot survive a change underneath it.

## What is NOT checked, on purpose

G6Crystal.lean's three open obligations — S1 Arnold tongue, S2 hexgrid collapse
superiority, S3 `coord_coverage` — are not named in the probe. Naming them would
fail the job for being honest. The gate exists to punish quiet admission, not
disclosure.
