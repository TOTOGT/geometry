# HVEH/cfd — the evaluator

Drafted 2026-08-25.

## Why this directory exists

`ch-build-2river.html` §8 names the rotor as "the one hard thing" — the only
non-catalogue item in the whole build — and says its geometry "must be derived
from the contact-geometric analysis ... **and validated by CFD before
fabrication**," calling that the critical-path item that sets the timeline.

`rotor_geometry.py` does the first half. It generates a blade surface from the
contact form α = dz − r²dθ, with the pitch law tan φ(r) = r that annihilates α
at each radius, and prints the three conditions a CFD pass must establish.

Nothing does the second half. This directory is the second half's skeleton.

## The shape being copied, and from whom

LEAP 71's Noyron generated a 5 kN LOX/kerosene engine from specification in
under two weeks, printed in CuCrZr by AMCM, hot-fired first try at Airborne
Engineering; the same approach later produced aerospike and orbital-class
methalox engines. What makes that work is not a model inventing a turbine. It
is three parts in a loop:

```
    generator  →  physics evaluator  →  score  →  iterate
```

HVEH has the generator and the score. It does not have the evaluator, and that
is the whole gap.

| Part | Status |
|---|---|
| Generator — `rotor_geometry.py` | **exists, runs** — 258,048 points at default resolution (32 × 64 × 21 × 2 surfaces × 3 blades), verified 2026-08-25 |
| Score — `gates.py` | **exists, fixtured** — 8/8 cases in `gates_fixtures.py` |
| Evaluator — CFD | **does not exist**. Outlined below and not run. |
| Sweep driver | does not exist |

The manufacturing axis is the one place HVEH is *easier* than the rocket case:
5083 aluminium on a 5-axis machine is a Newark-corridor shop, not metal AM with
a partner like Nikon SLM.

## What is verified here and what is not

**Verified.** `gates.py` computes three verdicts from extracted quantities, and
`gates_fixtures.py` proves it rejects — including three cases where a naive
checker returns clean while establishing nothing (no data at all; axial power
exactly zero, making the ratio undefined rather than infinite; zero upstream
swirl, making extraction unscoreable). Run `python3 gates_fixtures.py`.

**Not verified.** Everything below this line. No solver has been run. The
OpenFOAM structure is a plan, and a plan is not a result. When the first case
runs, this section is what gets rewritten — and it should be rewritten from the
run, not from the plan.

## The evaluator, outlined

Steady MRF (multiple reference frame) first; sliding mesh only if MRF proves
inadequate at these tip-speed ratios. `simpleFoam` or `pimpleFoam`,
incompressible, k-ω SST.

- **Domain.** Channel section around the rotor: 3–6 m wide per the Second River
  confluence, rotor diameter 1.2 m, inlet ≥ 5 D upstream, outlet ≥ 10 D down.
- **Inlet.** 0.3–1.0 m/s, the design range. Swirl must be *imposed* — the guide
  vane is what produces it, and a rotor evaluated in axial flow is being asked
  the wrong question.
- **Mesh.** `snappyHexMesh` from the STEP surface. The point cloud → NURBS →
  STEP path is in ch-build-2river §"CAM output"; the mesh needs the same STEP.
- **Extract, per case, into the JSON `gates.py` reads:** `torque_Nm`,
  `omega_rad_s`, `axial_force_N`, `U_axial_m_s`, `V_theta_upstream_m_s`,
  `V_theta_downstream_m_s`, `U_axial_core_min_normalised`.

Extraction is deliberately a separate step from scoring. The criteria should be
swappable without touching the solver and vice versa, and a change to either
should be visible in the diff of exactly one file.

**Mesh independence is not optional.** Three refinement levels, and the gate
values must converge. A single mesh that passes is not a pass; it is one mesh.

## The sweep

`rotor_geometry.py` already exposes the parameters worth sweeping:
`THETA_SWEEP`, `C_TIP`, `N_BLADES`, `N_RADIAL`/`N_THETA`/`N_CHORD` for
resolution, and the pitch law itself. The loop is: generate → mesh → solve →
extract → score → rank.

The AI leverage is here, and it is unglamorous: automating the sweep and the
post-processing, not inventing geometry. The geometry already follows from the
contact form. What is missing is the labour of evaluating a few hundred
candidates, which is exactly what a computational model absorbs.

## What passing all three gates does not mean

Cavitation. Fatigue under debris strike. Bearing loads. Biofouling. Silt.
Ice. A CFD pass sees none of these, and a hydrokinetic rotor in an urban river
fails in ways a rocket engine does not — a hot-fire is a short violent test,
and this machine has to survive years of a river being a river.

Passing all three gates means the hydrodynamics are worth taking to a flume.
That is all it means, and the verdict line in `gates.py` says so.
