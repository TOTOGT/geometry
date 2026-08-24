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
   12 named theorems actually depends on. This is the step that can see a
   `sorry`, because an admitted proof reports `sorryAx`.
3. `python3 tools/axiom_gate.py axioms.txt 12` — fails if any theorem reports
   `sorryAx`, if any axiom falls outside the allowlist, or if the **count** is
   not 12. The count matters: without it, a theorem quietly dropped from the
   probe would shrink the check instead of failing it.

## What is checked

| group | theorems |
|---|---|
| canonical invariants | `dm3_Tstar_pos`, `dm3_mumax_neg`, `dm3_tau_pos`, `dm3_tau_eq_abs_mumax` |
| stability radius | `dm3_epsilon0`, **`dm3_epsilon0_derived`**, **`epsilon0_of_antitone`**, `dm3_noise_tolerance`, `dm3_noise_tol_lt_one` |
| dimensional derivation | `aspect_ratio_eq`, `aspect_ratio_encoded`, `layer_height_cubits` |

The two in bold were written 23 Aug 2026 and **have never been compiled.**
`dm3_epsilon0_derived` puts the derivation ε₀(H) = |μ_max| / (2(1+H)) under the
kernel — before it, `dm3_epsilon0` restated a definition and was evidence of
nothing. `epsilon0_of_antitone` says a stiffer potential gives a narrower
stability band; its proof uses `div_lt_div_iff` and `abs_two` and is the most
likely thing here to need a tactic fix on first run.

## What is NOT checked, on purpose

G6Crystal.lean's three open obligations — S1 Arnold tongue, S2 hexgrid collapse
superiority, S3 `coord_coverage` — are not named in the probe. Naming them would
fail the job for being honest. The gate exists to punish quiet admission, not
disclosure.
