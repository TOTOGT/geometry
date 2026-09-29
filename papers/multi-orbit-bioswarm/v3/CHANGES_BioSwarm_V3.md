# CHANGES — Fruit-Fly Connectome Toy Model, V2 → V3 (September 2026)

Author: Pablo Nogueira Grossi, G6 LLC.

## Why a V3
Running the V2 code and reading the V2 Lean file against the paper found:
1. **No Lipschitz constant.** C is discontinuous: (1, 0.999) and (0.999, 1), 0.002 apart, go to (1, 0) and (0, 1), 2 apart. In V2, L(α) = 1/2 + |α| is a Lean *definition*; the theorems about it are arithmetic about the definition and never mention G.
2. **No unique fixed point.** At α = 0 (V2's L = 1/2) one agent has four fixed points, (±1, 0.1)/√1.01 and (0.1, ±1)/√1.01.
3. **The pitchfork figure is constant by construction.** U rescales every state to length 1, so mean |s|² is 1 for every α; the plotted spread (0.0021) is the added noise.
4. **The V2 "sorry obligations" contain no sorry.** Two conclude `True`; the third holds because the swarm step is an identity placeholder.
5. **Reference [11] (Bhaskaran et al., J. Theor. Biol. 540, 111077, doi:10.1016/j.jtbi.2022.111077) is not registered at doi.org** and was not found by title. It is withdrawn and replaced by Zarzer et al. 2013 (doi:10.1186/1742-4682-10-65).

## What V3 measures (noise-free, N = 8, 40 starts, 400 steps)
- α ≤ 0.35: all 40 runs settle, to 40 different end states (multistable); at α = 0.3 each run is within 1.5% of its own end state after 6 steps.
- α = 0.42: first cycles (period 24). α = 0.5–0.65: more runs cycle than settle. α ≥ 0.7: some runs neither settle nor repeat within 400 steps; α = 0.95: none do.

## Files
| File | Change |
|------|--------|
| `multi_orbit_bioswarm_v3.tex`, `.pdf` | Revised paper, 5 pages. |
| `BioSwarmCheck.lean`, `bioswarmcheck.axioms.txt` | New Lean file: `C_jumps`, `U_norm`, `four_fixed_points`; 17 declarations audited, permitted three axioms, no sorry. Replaces `MultiOrbitBioSwarm.lean` (kept in the V2 record). |
| `multi_orbit_bioswarm.py` | V2 operators, unchanged. |
| `multi_orbit_bioswarm_v3.py` | New: attractor scan, figures, `--check` (11 checks). |
| `figures/` | `fig2_attractor_scan`, `fig3_settling` (new), `fig4_operator_diagram` (V2), `scan_v3.csv`. The V2 pitchfork figure and `pitchfork_scan.csv` are withdrawn. |
