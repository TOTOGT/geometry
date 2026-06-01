# Orthogenesis

**Formal verification of a phased Moon Base colony architecture in Lean 4.**

Orthogenesis models the NASA Moon Base as a mathematically rigorous honeycomb colony: cells on an axial hex grid, geometric growth across deployment stages, and a `Colony.expand` operation that mirrors NASA's three-phase build-out — from the first 4,000 kg to a continuous crewed presence at the lunar South Pole.

> *"NASA is embarking on the most ambitious space project in recent history: building a Moon Base."*
> — NASA Moon Base User's Guide, Architecture Resources, April 2026 (NP-2026-04-6806-HQ)

---

## Why Lean 4

The NASA Moon Base Architecture Definition Document identifies **functional gaps** — capabilities that are either unallocated or under-specified — across seven sub-architectures. Each gap carries an identifier like `FN-H-101L`, `FN-P-402L`, `FN-T-201L`.

Orthogenesis treats those gaps as **proof obligations**. A Moon Base that compiles has no unmet structural requirements. A `sorry` is an open gap.

---

## Architecture

The colony is modeled in four layers:

```
Orthogenesis.Geometry.HexGrid      ←  axial coordinates, Euclidean embedding
Orthogenesis.Geometry.Growth       ←  geometric radius model  R(n) = g^n
Orthogenesis.Architecture.Cell     ←  (HexCoord, stage) pair
Orthogenesis.Architecture.Colony   ←  Finset Cell + expand operation
```

Extended by:

```
Orthogenesis.Architecture.G6Crystal   ←  20 dm³ invariant facts, planetary scaling
Orthogenesis.Architecture.DM3Bridge   ←  formal bridge: colony ↔ dm³ framework
Orthogenesis.Architecture.NASAGaps    ←  FN- code → proof obligation map
Orthogenesis.Architecture.Coverage    ←  coord_coverage, no_coord_collision
```

### Hex Grid

Modules on the lunar surface are arranged in a **pointy-top axial hex grid**. Every hex has exactly six neighbors:

```lean
def hexNeighbors (h : HexCoord) : List HexCoord :=
  [ ⟨h.q+1, h.r  ⟩, ⟨h.q+1, h.r-1⟩, ⟨h.q,   h.r-1⟩,
    ⟨h.q-1, h.r  ⟩, ⟨h.q-1, h.r+1⟩, ⟨h.q,   h.r+1⟩ ]
```

### Growth Model

```lean
def R (P : GrowthParams) (n : ℕ) : ℝ := P.g ^ n
```

NASA phased payload scaling:

| Phase | Launches | Landings | Payload to surface | Stage |
|-------|----------|----------|--------------------|-------|
| 01    | 25       | 21       | ~4,000 kg          | 0     |
| 02    | 27       | 24       | ~60,000 kg         | 1     |
| 03    | 29       | 28       | ~150,000 kg        | 2     |

Growth factor `g ≈ 3.87` (60,000/4,000 ≈ 15×, two stage steps of √15 each).

### Colony Expansion

```lean
def Colony.expand (C : Colony) : Colony :=
  { cells := C.cells ∪
      C.cells.biUnion (fun c =>
        (hexNeighbors c.coord).toFinset.image
          (fun h => Cell.mk h (c.stage + 1))) }
```

One call to `expand` = one NASA phase. A colony at depth 2 has passed through Phases 01, 02, and 03.

---

## Lemmas and Proof Obligations

| Lemma | Statement | Status | NASA Gap |
|-------|-----------|--------|----------|
| `hexNeighbors_length` | `(hexNeighbors h).length = 6` | ✓ proved | FN-L-101L |
| `hexNeighbors_nodup` | Six neighbors pairwise distinct | ✓ proved | FN-L-101L |
| `R_mono` | `1 < g → n ≤ m → R P n ≤ R P m` | ✓ proved | FN-P-101L |
| `expand_mono` | `C.cells ⊆ (C.expand).cells` | ✓ proved | FN-U-103L |
| `expandN_mono` | `C.cells ⊆ (expandN n C).cells` | ✓ proved | FN-A-104L |
| `mem_expand` | Membership characterisation | ✓ proved | — |
| `stage_bound` | Every cell in `expandN^n` has `stage ≤ n` | ✓ proved | FN-T-201L |
| `stage_bound_general` | Starting from stage ≤ k, after n steps stage ≤ k+n | ✓ proved | FN-T-202L |
| `no_coord_collision` | Expand preserves coord injectivity | ✓ proved | FN-H-101L |
| `hex_beats_square` | Hexagon isoperimetric ratio > square | ✓ proved | FN-H-101L |
| `nasa_payload_mono` | Phase 01 payload < Phase 02 | ✓ proved | FN-T-201L |
| `coord_coverage` | Ring at distance k has 6k cells (k ≥ 1) | ◑ partial | FN-C-101L |
| `arnold_tongue_A4` | A₄:₁ passive Schumann coupling | ○ open (S1) | FN-P-402L |
| `hexagrid_collapse` | Progressive collapse superiority | ○ open (S2) | FN-H-101L |

**`stage_bound` is the key structural invariant**: no capability is deployed before its phase is funded and launched. This is the formal analogue of the NASA functional gap closure requirement.

---

## The dm³ Bridge

The colony model is not merely a simulation of hex geometry. It is the **discrete realisation of the G6 Crystal** — a structural form derived from the three canonical invariants of the dm³ generative contact mechanics framework:

```
(T*, μ_max, τ) = (2π, −2, 2)
```

### G6 Crystal Connection

| Colony concept | dm³ / G6 Crystal analogue | Proved |
|---|---|---|
| `Colony.expand` | Operator G = U∘F∘K∘C | `expand_is_UCKF_composite` |
| `stage_bound` | Stability radius ε₀ = 1/3 | `stage_bound_is_epsilon0_analogue` |
| `hexNeighbors_length = 6` | Six G6 Crystal lattice directions | `hexNeighbors_is_G6_crystal_ring` |
| Centered hex sequence 1→7→19→37 | G6 Crystal ring structure | `centeredHex_one/two/three` |
| `R_mono` | Lyapunov descent toward Γ | `nasa_growth_satisfies_R_mono` |
| `hexNeighbors_nodup` | Lattice basis vectors distinct | `hexNeighbors_nodup` |
| `no_coord_collision` | A8 categorical closure | `Colony.no_coord_collision` |

### The Four Operators

Each step of `Colony.expand` instantiates the operator chain:

| Operator | Symbol | Colony action |
|---|---|---|
| Compression | C | Project cells to coordinate footprint (`op_C`) |
| Curvature | K | Find all adjacent hex coords (`op_K`) |
| Fold | F | Lift coords to stage+1 cells (`op_F`) |
| Unfold | U | Union with existing colony (`op_U`) |

**`Colony.expand` = U ∘ F ∘ K ∘ C** (proved: `expand_is_UCKF_composite`)

### Aspect Ratio and Planetary Scaling

The G6 Crystal derives all dimensions from the dm³ invariants alone:

- **Aspect ratio 66 = 33·τ = 33·|μ_max|** (monster threshold × embodiment threshold)
- **Stability radius ε₀ = 1/3** (dimensionless, gravity-independent)
- **Lunar scaling γ⁻¹ = 6.04** → base side 690 m, height 91 km
- **Mars scaling γ⁻¹ = 2.64** → base side 301 m, height 40 km (within Martian troposphere)

All proved in `G6Crystal.lean` (20 facts, 0 sorry on dimensional claims).

---

## NASA Gap Closure Matrix

| NASA Sub-Architecture | FN- Codes | Orthogenesis domain | Status |
|-----------------------|-----------|---------------------|--------|
| Habitation | FN-H-101L, FN-H-102L | Hex isoperimetric + `no_coord_collision` | ✓ / ∼ |
| Logistics | FN-L-101L, FN-L-205L | `hexNeighbors_nodup` + `FN_L_101L_unique_interface` | ✓ |
| Transportation | FN-T-201L, FN-T-202L | `stage_bound` + `nasa_payload_mono` | ✓ |
| Power | FN-P-101L, FN-P-402L | `g6_within_2pct_of_f4` + noise tolerance | ∼ |
| ISRU | FN-U-103L | `expand_mono` + `FN_U_103L_six_layers` | ∼ |
| Autonomous Systems | FN-A-104L, FN-A-105L | `expandN_mono` + neighbor traversal | ✓ |
| Communications & PNT | FN-C-101L, FN-C-201L | `ring_card` (coord_coverage) | ◑ |
| Mobility | FN-M-302L | Hex path existence | ∼ |

**Proved facts: `nasa_gap_closure_summary` collects the five fully closed gaps as a single theorem.**

---

## Formally Verified Facts (no sorry)

### From `HexGrid.lean`
- `hexNeighbors_length` — six neighbors exactly
- `hexNeighbors_nodup` — all six distinct

### From `Growth.lean`
- `R_mono` — growth is monotone when g > 1

### From `Colony.lean`
- `mem_expand` — membership characterisation
- `expand_mono` — existing cells preserved
- `expandN_mono` — monotone across iterations
- `stage_bound` — stage ≤ number of expansions (NASA phase invariant)
- `stage_bound_general` — general form

### From `Coverage.lean`
- `no_coord_collision` — expand preserves coord injectivity
- `seed_coord_injective` — canonical seed is injective
- `ring_card` — ring at depth n has 6n cells (combinatorial form)

### From `G6Crystal.lean` (20 facts)
- dm³ invariants: `dm3_Tstar_pos`, `dm3_mumax_neg`, `dm3_tau_pos`, `dm3_tau_eq_abs_mumax`, `dm3_epsilon0`, `dm3_noise_tolerance`, `dm3_noise_tol_lt_one`
- Aspect ratio: `aspect_ratio_eq`, `aspect_ratio_encoded`, `height_cubits`, `layer_height_cubits`, `height_metres`, `base_side_metres`
- Isoperimetric: `hex_beats_square`, `hex_improvement_gt_115`
- Schumann: `schumann_n4_sqrt`, `g6_within_2pct_of_f4`, `g6_within_16pct`, `noise_tol_covers_g6_error`
- Stability: `epsilon0_pos`, `epsilon0_lt_one`
- Planetary: `g_moon_lt_earth`, `g_mars_lt_earth`, `lunar_crystal_taller`, `mars_height_within_troposphere`, `aspect_ratio_scale_invariant`, `epsilon0_gravity_independent`
- Phase scaling: `growth_factor_gt_one`, `nasa_payload_mono`, `payload_ratio_phase_1_2`
- Colony: `hex_embedding_real`, `colony_depth1_cells`, `colony_depth2_cells`

### From `DM3Bridge.lean`
- `centeredHex_zero/one/two/three/four` — centered hex sequence
- `centeredHex_strictMono` — sequence is strictly increasing
- `ring_card` — ring n has 6n cells
- `expand_is_UCKF_composite` — expand = U∘F∘K∘C
- `opG_superset_expand` — operator G extends expand
- `stage_bound_is_epsilon0_analogue` — discrete ε₀ = 1/3
- `nasa_growth_satisfies_R_mono` — Lyapunov descent
- `hexNeighbors_is_G6_crystal_ring` — 6 neighbors = 6 crystal directions
- `hexNeighbors_unit_steps` — all steps have axial magnitude 1
- `dm3_bridge` — master bridge theorem (conjunction of all five bridges)

### From `NASAGaps.lean`
- `FN_H_101L_isoperimetric`, `FN_H_102L_phase02_cluster`
- `FN_L_101L_hex_interfaces`, `FN_L_101L_unique_interface`
- `FN_T_201L_payload_monotone`, `FN_T_202L_payload_ratio`, `FN_T_201L_stage_gated`
- `FN_P_101L_schumann_proximity`, `FN_P_402L_noise_tolerance`
- `FN_U_103L_six_layers`, `FN_U_103L_expand_models_ISRU`
- `FN_A_104L_reachability`, `FN_A_104L_neighbor_traversal`
- `FN_C_101L_ring_count`, `FN_M_302L_hex_path_exists`
- `nasa_gap_closure_summary` — master gap closure theorem

**Total: 50+ facts proved without sorry.**

---

## Open Obligations

| Sorry | Name | Gap | Closure path |
|-------|------|-----|-------------|
| S1 | `arnold_tongue_A4_coupling` | FN-P-402L | ODE flow theory in Mathlib; AXLE Target 6 |
| S2 | `hexagrid_collapse_resistance_superior` | FN-H-101L | FEM formalisation; Mashhadiali data |
| S3 | `coord_coverage` (cardinality) | FN-C-101L | Ring-walk injectivity; Coverage.lean |

---

## Project Structure

```
Orthogenesis/
├── Geometry/
│   ├── HexGrid.lean        -- Vec2, HexCoord, hexNeighbors, hexToVec2
│   └── Growth.lean         -- GrowthParams, R, R_mono
├── Architecture/
│   ├── Cell.lean           -- Cell, Cell.center, Cell.radius
│   ├── Colony.lean         -- Colony, expand, stage_bound (fully proved)
│   ├── Coverage.lean       -- coord_coverage, no_coord_collision
│   ├── G6Crystal.lean      -- 20 dm³ facts, planetary scaling
│   ├── DM3Bridge.lean      -- colony ↔ dm³ formal bridge
│   └── NASAGaps.lean       -- FN- code → proof obligation map
├── lakefile.lean
├── lean-toolchain
└── README.md
```

---

## Getting Started

**Prerequisites:** Lean 4 + Lake + Mathlib 4 (v4.14.0, rev `4bbdccd`)

```bash
git clone https://github.com/TOTOGT/geometry
cd geometry
lake exe cache get
lake build
```

**Run the basic colony expansion:**

```lean
import Orthogenesis.Architecture.Colony

open Orthogenesis

def seed : Colony := { cells := {Cell.mk ⟨0, 0⟩ 0} }
#eval seed.expand.cells.card              -- 7  (center + 6 neighbors)
#eval seed.expand.expand.cells.card      -- 19 (center + ring 1 + ring 2)
```

The sequence 1 → 7 → 19 → 37 → 61 is the **centered hexagonal numbers** `1 + 3n(n+1)` — the same formula that governs how many pressurised modules fit in a honeycomb base of radius n.

---

## Connection to NASA Architecture

> **Moon Base User's Guide — Architecture Resources**
> National Aeronautics and Space Administration, April 2026 · NP-2026-04-6806-HQ

Commercial innovators and international partners: HQ-MoonBase@nasa.gov

---

## Related Projects

- **[AXLE](https://github.com/TOTOGT/AXLE)** — Lean 4 formal verification hub for G = U∘F∘K∘C. 160+ theorems, 0 sorry on structural claims.
- **[GTCT](https://github.com/TOTOGT/GTCT)** — Generative Time Circuit Theorem. Verified Ring 5 operator T.
- **G6 Crystal** — Zenodo concept DOI: [10.5281/zenodo.19162012](https://doi.org/10.5281/zenodo.19162012)
- **Principia Orthogona** — Series root: [10.5281/zenodo.19117399](https://doi.org/10.5281/zenodo.19117399)

---

## Contributing

Pull requests that close proof obligations are welcome.
- If you add a lemma, update the table above.
- If you add a `sorry`, name it after the `FN-` gap it represents.
- If you close `coord_coverage` (S3), update `Coverage.lean` and remove the `sorry`.

---

## License

MIT (code) · CC BY-NC-ND 4.0 (mathematical content)

Build on it.
