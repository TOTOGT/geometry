import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic

/-!
# ChladniPolygon.lean

The standing-wave patterns behind `AXLE/SBM/nodal-sets.html`, and Saturn's two
polar polygons.

## Why this file exists

`nodal-sets.html` displays Lean source for `chladni6`, `chladni6_sixfold_sym`
and `hexagon_nodes_are_zeros`, and its status table marks the row
"Six-fold symmetry, hexagon nodes are zeros" as **Lean ✓**. As of 2026-09-06 a
declaration scan over the tracked corpus resolved neither
`hexagon_nodes_are_zeros` nor `hexagon_nodal_angles`: the source was shown on
the page but lived in no file, so nothing had ever elaborated it, and the tick
in that table asserted a check that could not have happened. The page's proof
also calls `hexagon_nodal_angles` without defining it.

This file supplies what the page displays, so the names resolve and the tick
can be earned. It also carries the tenfold case, which the page predates.

## Saturn, and what the mathematics does and does not say

Saturn's north polar jet carries a sixfold pattern, stable across more than
forty years. On 2 September 2026 a tenfold pattern at the south pole was
reported from Hubble OPAL imagery — the first regular polygonal jet seen in the
southern hemisphere, and unlike the hexagon it is strengthening rather than
steady.

`chladni6` and `chladni10` are the angular standing waves whose nodal sets have
those symmetries. Nothing here claims Saturn's jets *are* these functions: a
polar jet is a fluid instability, not a vibrating plate, and the honest
statement is that both share a wavenumber. What is proved is the geometry of the
nodal set at each wavenumber, and nothing beyond it.

For what the pair *cannot* be, see `PolarPolygonCommonRefinement.lean`: a field
carrying both symmetries at once is constant, so the hexagon and the decagon are
not two symmetries of one field.
-/

namespace ChladniPolygon

open Real

/-- Angular standing wave of wavenumber 6. Its nodal set `{f = 0}` is the six
    lines of the hexagonal pattern. -/
noncomputable def chladni6 (θ : ℝ) : ℝ := cos (6 * θ)

/-- The six nodal angles of `chladni6`, offset by `π/12` so they fall between
    the antinodes. -/
noncomputable def hexagon_nodal_angles (i : Fin 6) : ℝ :=
  (i.val : ℝ) * (π / 6) + π / 12

/-- **Sixfold symmetry**: rotation by `π/3` leaves the pattern unchanged. -/
theorem chladni6_sixfold_sym (θ : ℝ) : chladni6 (θ + π / 3) = chladni6 θ := by
  unfold chladni6
  have h : 6 * (θ + π / 3) = 6 * θ + 2 * π := by ring
  rw [h, Real.cos_add_two_pi]

/-- **Each nodal angle is a zero.** This is the declaration the Bienal page
    displays and marks Lean ✓. -/
theorem hexagon_nodes_are_zeros (i : Fin 6) :
    chladni6 (hexagon_nodal_angles i) = 0 := by
  unfold chladni6 hexagon_nodal_angles
  have h : 6 * ((i.val : ℝ) * (π / 6) + π / 12) = (i.val : ℝ) * π + π / 2 := by
    ring
  rw [h, Real.cos_add, Real.cos_pi_div_two, Real.sin_pi_div_two]
  simp [Real.sin_nat_mul_pi]

/-! ## The tenfold case

Reported at Saturn's south pole on 2 September 2026. The same three statements,
at wavenumber 10.
-/

/-- Angular standing wave of wavenumber 10. -/
noncomputable def chladni10 (θ : ℝ) : ℝ := cos (10 * θ)

/-- The ten nodal angles of `chladni10`. -/
noncomputable def decagon_nodal_angles (i : Fin 10) : ℝ :=
  (i.val : ℝ) * (π / 10) + π / 20

/-- **Tenfold symmetry**: rotation by `π/5` leaves the pattern unchanged. -/
theorem chladni10_tenfold_sym (θ : ℝ) : chladni10 (θ + π / 5) = chladni10 θ := by
  unfold chladni10
  have h : 10 * (θ + π / 5) = 10 * θ + 2 * π := by ring
  rw [h, Real.cos_add_two_pi]

/-- **Each nodal angle is a zero**, tenfold case. -/
theorem decagon_nodes_are_zeros (i : Fin 10) :
    chladni10 (decagon_nodal_angles i) = 0 := by
  unfold chladni10 decagon_nodal_angles
  have h : 10 * ((i.val : ℝ) * (π / 10) + π / 20) = (i.val : ℝ) * π + π / 2 := by
    ring
  rw [h, Real.cos_add, Real.cos_pi_div_two, Real.sin_pi_div_two]
  simp [Real.sin_nat_mul_pi]

-- Kernel gate.
#print axioms chladni6_sixfold_sym
#print axioms hexagon_nodes_are_zeros
#print axioms chladni10_tenfold_sym
#print axioms decagon_nodes_are_zeros

end ChladniPolygon
