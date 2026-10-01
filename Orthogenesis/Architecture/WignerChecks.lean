-- Orthogenesis/Architecture/WignerChecks.lean
-- Checks for Chapter W (chW-wigner.html, wigner-fractal.html) against
-- Orthogenesis/Architecture/G6Crystal.lean.
--
-- GATE-DECLARE: sorries = none
-- GATE-REASON: every statement here is a rational-arithmetic bound, or a
--   sqrt/pi bound discharged against Real.sq_sqrt and Real.pi_gt_d4 /
--   Real.pi_lt_d4.  No analysis, no ODE theory, no appeal to an unproved
--   physical model.  No theorem concludes `True`; no theorem has an unused
--   hypothesis.  Author's lake build 2026-10-01 (Lean 4.32.0 / Mathlib):
--   14/14, zero warnings, all 10 probes on [propext, Classical.choice,
--   Quot.sound], no sorryAx.
--
-- SCOPE.  G6Crystal.lean already withdrew its §4 Schumann section on
-- 2026-09-11, and deleted the vacuous S1/S2 with it, for the right reasons
-- (units; 33.516 entered as a literal nothing derives; f4_schumann never
-- evaluated against it).  None of that is reopened here.  This file does
-- three things that withdrawal left undone:
--
--   §1-2  Give the withdrawal positive content.  "33.516 is not derived"
--         is weaker than "33.516 is not the n=4 mode, the measured mode is
--         ~26.6 Hz, and no p:1 lock of 7.83 Hz can reach 33.516."  The
--         chapter page still asserts the withdrawn claims three weeks on,
--         so the numbers that refute them are worth pinning in the kernel
--         rather than only in a comment.
--   §3    Saturn's hexagon: the chapter's aspect-ratio claim was never part
--         of §4 and so survived its withdrawal.  It is false independently.
--   §4    §3 of G6Crystal.lean still carries a false section docstring.
--         This is a live defect, not a historical one.
--   §5    What wigner-fractal.html gets right, pinned so the chapter's
--         correction is not mistaken for a retraction of the physics.
--
-- Toolchain: Lean 4 + Mathlib
-- Chapter: chW-wigner.html, wigner-fractal.html (Book 3)

import Mathlib

namespace Orthogenesis.WignerChecks

open Real

/-! ## §1  Schumann modes: measured values vs the ideal-cavity formula

Measured Earth-ionosphere modes, as tabulated by this project's own
`ch-schumann-dual.html` section 8: f1 ~ 7.83, f2 ~ 14.1, f3 ~ 20.3,
f4 ~ 26.6, f5 ~ 32.7 Hz.  (Wikipedia's summary gives 26.3 and 32.5; both
sit inside the literature spread, and the results below hold on either.)
That same page computes f5 ~ 33.58 Hz from its dual-cavity model -- which
is, to within 0.2%, the number chW-wigner.html labels n=4.  So the two
chapters disagree with each other, not merely with outside literature.

The ideal lossless cavity gives f_n = (c / 2*pi*R_E) * sqrt (n(n+1)), whose
n = 1 value is ~10.6 Hz; the measured fundamental is ~26% lower because
finite ionospheric conductivity slows propagation in the cavity.  The
chapter's vocabulary box lists 7.83 (n=1), 14.3 (n=2), 20.8 (n=3) -- all
measured -- and then 33.516 (n=4), which is the ideal value.  Two
conventions in one list, and the number it labels n=4 is the n=4 mode
under neither. -/

/-- Measured Schumann fundamental. -/
def f1_obs : ℝ := 7.83

/-- Measured Schumann n=4 mode. -/
def f4_obs : ℝ := 26.6

/-- Measured Schumann n=5 mode. -/
def f5_obs : ℝ := 32.7

/-- The frequency chW-wigner.html calls "Schumann n=4". -/
def f4_claimed : ℝ := 33.516

/-- The claimed frequency overshoots the measured n=4 mode by 26% (the bound
    is stated at 20% so it holds on the 26.3 Hz figure too). -/
theorem claimed_f4_exceeds_observed_n4 :
    20 / 100 * f4_obs < f4_claimed - f4_obs := by
  unfold f4_obs f4_claimed; norm_num

/-- It sits within 4% of the measured n=5 mode instead. -/
theorem claimed_f4_within_4pct_of_observed_n5 :
    0 < f4_claimed - f5_obs ∧ f4_claimed - f5_obs < 4 / 100 * f5_obs := by
  unfold f4_claimed f5_obs
  constructor <;> norm_num

/-- And it is strictly closer to the measured n=5 mode than to n=4.
    Both gaps are positive, so these differences are the distances. -/
theorem claimed_f4_closer_to_n5_than_n4 :
    0 < f4_claimed - f5_obs ∧ f4_claimed - f5_obs < f4_claimed - f4_obs := by
  unfold f4_claimed f5_obs f4_obs
  constructor <;> norm_num

/-- The ideal-cavity formula fixes the ratio f4/f1 = sqrt 20 / sqrt 2 = sqrt 10.
    Applied to the *measured* fundamental it predicts ~24.8 Hz, not 33.516. -/
theorem ideal_f4_from_measured_f1 :
    24 < f1_obs * sqrt 10 ∧ f1_obs * sqrt 10 < 25 := by
  unfold f1_obs
  have h10 : sqrt 10 ^ 2 = 10 := Real.sq_sqrt (by norm_num)
  have hpos : (0 : ℝ) < sqrt 10 := Real.sqrt_pos.mpr (by norm_num)
  constructor
  · nlinarith [h10, hpos]
  · nlinarith [h10, hpos]

/-- So the claimed value is not the ideal n=4 built on the measured
    fundamental either.  It is the ideal n=4 built on the ideal fundamental
    (~10.6 Hz).  Mixing the measured f1 with the ideal f4 is the error. -/
theorem claimed_f4_above_ideal_from_measured_f1 :
    f1_obs * sqrt 10 < f4_claimed := by
  unfold f1_obs f4_claimed
  have h10 : sqrt 10 ^ 2 = 10 := Real.sq_sqrt (by norm_num)
  have hpos : (0 : ℝ) < sqrt 10 := Real.sqrt_pos.mpr (by norm_num)
  nlinarith [h10, hpos]

/-! ## §2  A 4:1 lock has rotation number exactly 4

An Arnold tongue A_{p:q} is by definition the parameter region on which the
rotation number is *locked* at the rational p/q.  A locked rotation number
cannot be 4.28.  chW-wigner.html writes "7.83 Hz x 4.28, where 4.28 is the
rotation number of the Arnold tongue A4:1"; a 4:1 lock of a 7.83 Hz driver
responds at exactly 31.32 Hz, and no integer lock of 7.83 Hz reaches
33.516 Hz at all.

This is independent of whether Mathlib can state Arnold tongues.  It is a
constraint on what any such statement could conclude. -/

/-- Response frequency of a p:1 lock to a driver at `f_drive`. -/
def lockFreq (f_drive : ℝ) (p : ℕ) : ℝ := f_drive * p

theorem lock_four_to_one : lockFreq f1_obs 4 = 31.32 := by
  unfold lockFreq f1_obs; norm_num

/-- No p:1 lock of the measured fundamental produces the claimed frequency. -/
theorem no_integer_lock_reaches_claimed_f4 (p : ℕ) :
    lockFreq f1_obs p ≠ f4_claimed := by
  unfold lockFreq f1_obs f4_claimed
  intro h
  rcases Nat.lt_or_ge p 5 with hp | hp
  · have h4 : p ≤ 4 := by omega
    have hpr : (p : ℝ) ≤ 4 := by exact_mod_cast h4
    linarith
  · have hpr : (5 : ℝ) ≤ (p : ℝ) := by exact_mod_cast hp
    linarith

/-- The multiplier the chapter needs falls strictly between the 4:1 and 5:1
    locks, so it lies in no p:1 tongue. -/
theorem required_multiplier_strictly_between_locks :
    lockFreq f1_obs 4 < f4_claimed ∧ f4_claimed < lockFreq f1_obs 5 := by
  unfold lockFreq f1_obs f4_claimed
  constructor <;> norm_num

/-! ## §3  Saturn's hexagon is not a 66:1 tower

chW-wigner.html calls Saturn's north polar vortex "an empirical certificate"
with "an aspect ratio matching the G6 crystal" (66).  That claim sat in the
Collatz section, not in §4, so the 2026-09-11 withdrawal did not reach it.

Cassini places the hexagonal wavenumber-6 boundary near 78 deg N,
~29,000 km across.  Fletcher et al. (Nat. Commun. 9:3564, 2018) trace it
over a vertical range of ~300 km, from the 2-3 bar troposphere into the
stratosphere.  Height/width ~ 0.01: wrong by more than three orders of
magnitude, and in the wrong direction -- the feature is flat, not slender. -/

def saturn_width_km : ℝ := 29000
def saturn_height_km : ℝ := 300

theorem saturn_hexagon_is_flat :
    saturn_height_km < saturn_width_km / 90 := by
  unfold saturn_height_km saturn_width_km; norm_num

/-- Even inflated a thousandfold, the measured aspect ratio stays below 66. -/
theorem saturn_aspect_off_by_three_orders :
    1000 * saturn_height_km < 66 * saturn_width_km := by
  unfold saturn_height_km saturn_width_km; norm_num

/-! ## §4  LIVE DEFECT: section 3 of `G6Crystal.lean` has a false docstring

Its section header still reads

    -- §3  Hexagonal Isoperimetric Optimum
    -- A/P² is maximised for the regular hexagon among all regular n-gons.

That is false.  For a regular n-gon, A/P^2 = cot(pi/n) / (4n), which is
strictly increasing in n and tends to 1/(4*pi).  The two theorems under
that header -- `hex_beats_square` and `hex_improvement_gt_115` -- prove only
hexagon > square, which is true and stays true.  The general claim above
them is not, and the octagon is a one-line counterexample.

The correct optimality statement for hexagons is Hales' honeycomb theorem
(1999): least total perimeter among *tilings* of the plane, not largest
A/P^2 for a single cell.  Those are different claims, and the tiling one is
the one the architecture argument actually wants.

Fixing the docstring is a comment-only change with no logic change, but it
is left to the author rather than done here, since it decides what §3 is
claiming to be about. -/

/-- A/P^2 for a regular hexagon: (3*sqrt 3/2)s^2 / 36 s^2 = sqrt 3 / 24. -/
noncomputable def hexRatio : ℝ := sqrt 3 / 24

/-- A/P^2 for a regular octagon: cot(pi/8) / 32 = (1 + sqrt 2) / 32. -/
noncomputable def octRatio : ℝ := (1 + sqrt 2) / 32

theorem octagon_beats_hexagon : hexRatio < octRatio := by
  unfold hexRatio octRatio
  have h3 : sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have h2 : sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have p3 : (0 : ℝ) < sqrt 3 := Real.sqrt_pos.mpr (by norm_num)
  have p2 : (0 : ℝ) < sqrt 2 := Real.sqrt_pos.mpr (by norm_num)
  have h3u : sqrt 3 < 1.7321 := by nlinarith [h3, p3]
  have h2l : (1.4142 : ℝ) < sqrt 2 := by nlinarith [h2, p2]
  linarith

/-- The disc beats the hexagon too: hexRatio * (4*pi) < 1, i.e. sqrt 3/24 < 1/(4*pi). -/
theorem disc_beats_hexagon : hexRatio * (4 * π) < 1 := by
  unfold hexRatio
  have h3 : sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have p3 : (0 : ℝ) < sqrt 3 := Real.sqrt_pos.mpr (by norm_num)
  have h3u : sqrt 3 < 1.7321 := by nlinarith [h3, p3]
  have hpu : π < 3.1416 := Real.pi_lt_d4
  have hpp : (0 : ℝ) < π := Real.pi_pos
  nlinarith [h3u, hpu, hpp, p3]

/-! ## §5  What the companion page gets right

`wigner-fractal.html` puts the 2D Wigner crystallisation threshold at
r_s* ~ 30-40.  That band contains both standing quantum Monte Carlo
estimates: Tanatar & Ceperley (PRB 39:5005, 1989) give r_s ~ 37 ± 5, and
Drummond & Needs (PRL 102:126402, 2009) give r_s = 31(1).  The triangular
lattice as the 2D ground state is Bonsall & Maradudin (PRB 15:1959, 1977).
Both are correctly reported, and the page's B-field control raises the
effective r_s -- the right direction, since Landau quantisation suppresses
kinetic energy and so favours the crystal.

The order of the transition is genuinely open: Drummond & Needs note it has
been argued the 2D fluid-to-crystal transition cannot be first order, and
do not settle it.  So that page's fold (continuous, soft-mode) picture is a
modelling choice, not a derived fact, and is labelled as one. -/

def rs_star_lo : ℝ := 30
def rs_star_hi : ℝ := 40
def rs_tanatar : ℝ := 37
def rs_drummond : ℝ := 31

theorem page_band_contains_tanatar :
    rs_star_lo ≤ rs_tanatar ∧ rs_tanatar ≤ rs_star_hi := by
  unfold rs_star_lo rs_star_hi rs_tanatar
  constructor <;> norm_num

theorem page_band_contains_drummond :
    rs_star_lo ≤ rs_drummond ∧ rs_drummond ≤ rs_star_hi := by
  unfold rs_star_lo rs_star_hi rs_drummond
  constructor <;> norm_num

-- ── Axiom probes ────────────────────────────────────────────────────────────
#print axioms claimed_f4_exceeds_observed_n4
#print axioms claimed_f4_closer_to_n5_than_n4
#print axioms ideal_f4_from_measured_f1
#print axioms claimed_f4_above_ideal_from_measured_f1
#print axioms no_integer_lock_reaches_claimed_f4
#print axioms required_multiplier_strictly_between_locks
#print axioms saturn_aspect_off_by_three_orders
#print axioms octagon_beats_hexagon
#print axioms disc_beats_hexagon
#print axioms page_band_contains_drummond

end Orthogenesis.WignerChecks
