Orthogenesis
Formal verification of a phased Moon Base colony architecture in Lean 4.
Orthogenesis models the NASA Moon Base as a mathematically rigorous honeycomb colony: cells on an axial hex grid, geometric growth across deployment stages, and a Colony.expand operation that mirrors NASA's three-phase build-out — from the first 4,000 kg to a continuous crewed presence at the lunar South Pole.

"NASA is embarking on the most ambitious space project in recent history: building a Moon Base."
— NASA Moon Base User's Guide, Architecture Resources, April 2026


Why Lean 4
The NASA Moon Base Architecture Definition Document identifies functional gaps — capabilities that are either unallocated or under-specified — across seven sub-architectures (Autonomous Systems, Communications & PNT, Habitation, Logistics, Mobility, Power, Transportation). Each gap carries an identifier like FN-A-104 L, FN-P-402 L, FN-T-201 L.
Orthogenesis treats those gaps as proof obligations. A Moon Base that compiles has no unmet structural requirements. A sorry is an open gap.

Architecture
The colony is modeled in four layers:
Orthogenesis.Geometry.HexGrid      ←  axial coordinates, Euclidean embedding
Orthogenesis.Geometry.Growth       ←  geometric radius model  R(n) = g^n
Orthogenesis.Architecture.Cell     ←  (HexCoord, stage) pair
Orthogenesis.Architecture.Colony   ←  Finset Cell + expand operation
Hex Grid
Modules on the lunar surface are arranged in a pointy-top axial hex grid — the same honeycomb geometry used in pressurized habitat clusters, ISRU pad layouts, and mobility staging areas. Every hex has exactly six neighbors:
leandef hexNeighbors (h : HexCoord) : List HexCoord :=
  [ ⟨h.q+1, h.r  ⟩, ⟨h.q+1, h.r-1⟩, ⟨h.q,   h.r-1⟩,
    ⟨h.q-1, h.r  ⟩, ⟨h.q-1, h.r+1⟩, ⟨h.q,   h.r+1⟩ ]
The Euclidean embedding maps axial (q, r) to ℝ²:
x = q + r/2
y = (√3 / 2) · r
Growth Model
Each cell carries a stage that indexes into a geometric growth sequence. The structural radius at stage n is:
leandef R (P : GrowthParams) (n : ℕ) : ℝ := P.g ^ n
This matches NASA's phased payload scaling:
PhaseLaunchesLandingsPayload to surfaceStage012521~4,000 kg0022724~60,000 kg1032928~150,000 kg2
Growth factor g ≈ 3.87 fits the Phase 01 → Phase 02 transition (60,000 / 4,000 ≈ 15×, two stage steps of √15 ≈ 3.87 each).
Colony Expansion
Colony.expand adds all six hex neighbors of every existing cell, advancing each to the next stage:
leandef Colony.expand (C : Colony) : Colony :=
  let newCells :=
    C.cells.fold
      (fun acc c =>
        let neigh := hexNeighbors c.coord
        let stage := c.stage + 1
        let new := neigh.map (fun h => Cell.mk h stage)
        acc ∪ new.toFinset)
      ∅
  { cells := C.cells ∪ newCells }
One call to expand = one NASA phase. A colony at depth 2 has passed through Phases 01, 02, and 03.

Lemmas and Proof Obligations
LemmaStatementStatushexNeighbors_length(hexNeighbors h).length = 6✓ provedR_mono1 < g → n ≤ m → R P n ≤ R P m✓ provedexpand_monoC.cells ⊆ (C.expand).cells◑ in progressstage_boundEvery cell in expand^n has stage ≤ n◯ opencoord_coverageRing at distance k has 6k cells for k ≥ 1◯ openno_coord_collisionWell-formed colonies have unique coords◯ open
stage_bound is the key structural invariant: it ensures no capability is deployed before its phase is funded and launched. This is the formal analogue of the NASA functional gap closure requirement.

Project Structure
Orthogenesis/
├── Geometry/
│   ├── HexGrid.lean        -- Vec2, HexCoord, hexNeighbors, hexToVec2
│   └── Growth.lean         -- GrowthParams, R, R_mono
├── Architecture/
│   ├── Cell.lean           -- Cell, Cell.center, Cell.radius
│   └── Colony.lean         -- Colony, Colony.insert, Colony.expand
├── lakefile.lean
└── README.md

Getting Started
Prerequisites: Lean 4 + Lake + Mathlib 4
bashgit clone https://github.com/TOTOGT/Orthogenesis
cd Orthogenesis
lake update
lake build
Run the basic colony expansion:
leanimport Orthogenesis.Architecture.Colony

open Orthogenesis

def seed : Colony := { cells := {Cell.mk ⟨0, 0⟩ 0} }
#eval seed.expand.cells.card        -- 7  (center + 6 neighbors)
#eval seed.expand.expand.cells.card -- 19 (center + ring 1 + ring 2)
The sequence 1 → 7 → 19 → 37 → 61 … is the centered hexagonal numbers 1 + 3n(n+1) — the same formula that governs how many pressurized modules fit in a honeycomb base of radius n.

Connection to NASA Architecture
This project formally models the architecture resources described in:

Moon Base User's Guide — Architecture Resources
National Aeronautics and Space Administration, April 2026
NP-2026-04-6806-HQ
nasa.gov/architecture

The seven Phase 01 functional gap categories map directly to proof domains:
NASA Sub-ArchitectureFN- CodesOrthogenesis domainAutonomous Systems & RoboticsFN-A-104 L … FN-M-501 LColony.expand reachabilityCommunications & PNTFN-C-101 L … FN-C-201 LCoord coverage lemmasHabitationFN-H-101 L … FN-H-201 LCell occupancy invariantsLogisticsFN-L-101 L … FN-L-205 LStage-gated insertionMobilityFN-M-302 L … FN-U-103 LNeighbor traversal proofsPowerFN-P-101 L … FN-P-402 LGrowth monotonicityTransportation (Cargo)FN-T-201 L … FN-T-202 LGrowthParams payload bounds
The architecture-driven technology gaps (#0xxx) and data gaps (DN-xxx-L) in the NASA document correspond to sorry-marked lemmas in this repo. Closing a sorry closes a gap.

Name
Orthogenesis (from Greek orthos — straight, genesis — origin): directed growth toward a fixed goal. The colony expands outward in every direction simultaneously, but each cell knows its stage, its position, and the radius it must fill. The fixed point is a permanent human presence on the Moon.
This naming is intentional. Orthogenesis in biology was the (now abandoned) idea that evolution has a direction. Here it does: Gⁿ(x₀) → x*.

Related Projects

AXLE — Lean 4 formal verification hub for the G=U∘F∘K∘C operator chain
DM3-lab — Research writing and Book 3: The Mini-Beast
book3-starter — Classroom template for writing-for-research courses


Contributing
NASA's Moon Base program is explicitly designed for commercial innovators and international partners (contact: HQ-MoonBase@nasa.gov). Orthogenesis follows the same open model.
Pull requests that close proof obligations are welcome. If you add a lemma, update the table above. If you add a sorry, name it after the FN- gap it represents.

License
MIT. Build on it.
