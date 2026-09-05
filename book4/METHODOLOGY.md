# Rigorous certification of r* — methodology and benchmarks

Companion to `certify_rstar_rigorous.py`. Closes AXLE Issue #21.

## The question

The inner stability boundary r* (dm³ system, Theorem 10.3(v)) was previously
certified only by plain-float bisection (original `certify_rstar.py`), to
8 decimal places, with no rigorous error bound — i.e. not proved to the same
standard as `gronwall_radius` (ε₀ = 1/3), which is a closed-form algebraic
identity checkable by exact arithmetic.

Three paths were evaluated to close this gap:

## Path 3 — closed form (ruled out)

Checked and ruled out:
- Symbolic solve of the coupled fixed-point system (`sympy.nonlinsolve`):
  degenerate, no isolated closed-form root.
- Exactness / Hamiltonian structure check: `d(r_dot)/dz + d(z_dot)/dr` does
  **not** vanish identically (`2*(r*e^z - 3r + 3)*e^{-z} ≠ 0`), so the system
  is not Hamiltonian/exact — no conserved quantity of that form exists.
- Substitution `w = e^{-z}`: reduces to a quadratic in `w` but remains
  nonlinearly coupled to `r`; no separability found.
- `(r=1, z=0)` is **not** a fixed point of the reduced planar system
  (`ṙ=0` but `ż=1` there) — Γ is an asymptotic attracting set (`z→∞`), not
  a classical equilibrium, which rules out standard saddle-point/closed-form
  separatrix formulas.

**Conclusion: r* is a genuine transcendental threshold of a non-integrable
coupled system. No closed form found; this is not an oversight.**

## Path 2 — existence/uniqueness without exact value (partial)

- On the exact slice `z=0`: `ṙ(r,0) = -(r-1)²(r+2)`, strictly negative on
  `(0,1)` except the double root at `r=1`. So no 1-variable monotonicity
  argument on `r` alone can show existence/uniqueness of r* — convergence
  for `r₀ > r*` depends on the coupled `z`-growth decaying the `e^{-z}`
  term, a genuinely 2D effect.
- Numerical scan (150 points, `r0 ∈ [0.01, 1.5]`): exactly **one** transition
  from escape to converge — strong evidence the basin boundary is a single
  clean threshold, not a fractal/multi-component boundary.
- A full proof would need a 2D saddle/stable-manifold argument (shooting +
  IVT, or a Lyapunov-Chetaev-style instability theorem), which is real but
  separate work from the numerical certificate below. **Recorded as a
  companion open item, not required to close #21.**

## Path 1 — certified numerical interval (this is what closes #21)

### Naive interval RK4: measured failure

Direct substitution of interval arithmetic into RK4 (`mpmath.iv`) was
implemented and benchmarked:

| t   | interval box width (r) |
|-----|------------------------|
| 0   | 2.22e-16 (machine eps) |
| 4   | 6.06e-09               |
| 7   | 6.87e-06               |
| 10  | 5.47e-03               |
| ~10.5 | MemoryError / OverflowError even at 2000-bit working precision |

Independently verified this is a **wrapping-effect artifact**, not real
dynamical uncertainty: a true float-trajectory cloud with matched initial
spread shows the box is inflated by a factor of **~490,000× at t=7**
relative to the true reachable-set spread. More working precision does not
fix this — it is a method defect (axis-aligned re-boxing every step loses
the true, curved, shrinking-in-places shape of the reachable set).

### Linearized (Jacobian-transported) error, no rigorous remainder

Replacing per-step re-boxing with linear transport of the error radius via
the Jacobian (`Σ_new = (I + dt·J) Σ (I + dt·J)ᵀ`) closes almost all of the
gap: at t=7, radius = 7.5e-13 (vs. naive 6.9e-06 — a ~9,000,000× tightening),
consistent with the independently-measured true spread (1.4e-11). **Not
yet a certificate**: drops the nonlinear (Lagrange) remainder term, so it
is a very good estimate, not a proof.

### Full rigorous step (implemented in `certify_rstar_rigorous.py`)

Adds a genuine interval-enclosed second-order remainder: the Hessian of the
vector field is bounded via interval arithmetic *over the current error box*
(not just at a point), giving a Lagrange-form bound

```
|remainder_i| ≤ dt · ½ · ( |∂²fᵢ/∂r²|·rad_r² + |∂²fᵢ/∂z²|·rad_z²
                            + 2|∂²fᵢ/∂r∂z|·rad_r·rad_z )
```

added to the linearly-transported radius each step. This radius is now a
genuine upper bound on the true local error, not an estimate.

The float64-precision version of this scheme hit its own precision floor
(center trajectory computed in plain `numpy.float64`) at deep bisection
levels — diagnosed directly (starting radius 2.22e-16 already equals
`np.finfo(float64).eps`) and fixed by moving the center trajectory to
`mpmath` arbitrary precision (300 bits used here). This removed the floor;
certified radius continued shrinking cleanly to ~1e-51–1e-52 before the
run was capped for compute time, with no sign of a fundamental barrier.

### Result

```
r* ∈ [0.775940575501953125, 0.77594057550234375]
width: 3.906e-13
midpoint: 0.7759405755021484
```

Matches the paper's stated `r* ≈ 0.77594` to every quoted digit, and
extends it to **13 significant figures**, with each bisection step backed
by a certified error radius (printed alongside each result — see script
output), not a floating-point guess.

## What would still be needed for a Lean/AXLE formalization

This Python/mpmath implementation is a rigorous **reference algorithm**,
not yet a machine-checked proof. To port into AXLE:

1. Express the same three-part structure (center + linear transport +
   interval Hessian remainder) as Lean lemmas, likely built on
   `Mathlib.Analysis.SpecialFunctions.Exp` for rigorous `exp` bounds.
2. Mathlib does not currently ship a general Lohner/Taylor-model rigorous
   ODE integrator — this would need to be built from primitives (interval
   arithmetic + the mean-value/Lagrange remainder lemma), which is a real
   scope of work, not a wrapper.
3. For very long integrations, production tools (VNODE-LP, COSY) add
   automatic QR re-orthogonalization of the error ellipsoid each step to
   avoid slow degradation over many steps; not needed at the ~17,000–46,000
   step counts used here, but worth flagging if integration times grow.

## Files

- `certify_rstar_rigorous.py` — the rigorous certifier (replaces the
  plain-bisection `certify_rstar.py` as the citable methodology)
- `METHODOLOGY.md` — this document
