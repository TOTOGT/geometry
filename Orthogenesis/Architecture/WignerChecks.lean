-- Orthogenesis/Architecture/WignerChecks.lean
-- Audit checks for Chapter W (chW-wigner.html, wigner-fractal.html) against
-- Orthogenesis/Architecture/G6Crystal.lean.
--
-- GATE-DECLARE: sorries = none
-- GATE-REASON: every statement here is a rational-arithmetic bound, or a
--   sqrt/pi bound discharged against Real.sq_sqrt and Real.pi_gt_d4 /
--   Real.pi_lt_d4.  No analysis, no ODE theory, no appeal to an unproved
--   physical model.  No theorem concludes `True`; no theorem has an unused
--   hypothesis.  UNTESTED: written without a local toolchain.
--
-- WHY THIS FILE EXISTS.  G6Crystal.lean asserts in prose that the G6 form
-- couples to "the Schumann n=4 resonance at 33.516 Hz", and backs it with
-- three theorems (Facts 16-18) that compare the integer 33 to the literal
-- 33.516.  This file checks that prose against measured values and against
-- what a p:q lock means.  The verdict is negative on four counts.  It also
-- pins the two things the companion page gets right, so the correction is
-- not mistaken for a wholesale retraction.
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
is, to within 0.2%, the number Chapter W labels n=4.  So the two chapters
disagree with each other, not merely with the outside literature.

The ideal lossless
cavity gives f_n = (c / 2*pi*R_E) * sqrt (n(n+1)), whose n = 1 value is
~ 10.6 Hz; the measured fundamental is ~26% lower because finite
ionospheric conductivity slows propagation in the cavity.

Chapter W's vocabulary box lists 7.83 (n=1), 14.3 (n=2), 20.8 (n=3) and
then 33.516 (n=4).  The first three are measured values; 33.516 is the
*ideal* n=4 eigenvalue.  The list mixes two conventions, and the number it
labels n=4 is not the n=4 mode under either of them. -/

/-- Measured Schumann fundamental. -/
def f1_obs : ℝ := 7.83

/-- Measured Schumann n=4 mode. -/
def f4_obs : ℝ := 26.6

/-- Measured Schumann n=5 mode. -/
def f5_obs : ℝ := 32.7

/-- The frequency Chapter W and `G6Crystal.lean` call "Schumann n=4". -/
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
cannot be 4.28.  Chapter W writes "7.83 Hz x 4.28, where 4.28 is the
rotation number of the Arnold tongue A4:1"; a 4:1 lock of a 7.83 Hz driver
responds at exactly 31.32 Hz, and no integer lock of 7.83 Hz reaches
33.516 Hz at all. -/

/-- Response frequency of a p:1 lock to a driver at `f_drive`. -/
def lockFreq (f_drive : ℝ) (p : ℕ) : ℝ := f_drive * p

theorem lock_four_to_one : lockFreq f1_obs 4 = 31.32 := by
  unfold lockFreq f1_obs; norm_num

/-- No p:1 lock of the measured fundamental produces the claimed frequency. -/
theorem no_integer_lock_reaches_claimed_f4 (p : ℕ) :
    lockFreq f1_obs p ≠ f4_claimed := by
  unfold lockFreq f1_obs f4_claimed
  intro h
  rcases le_or_lt p 4 with hp | hp
  · have hpr : (p : ℝ) ≤ 4 := by exact_mod_cast hp
    nlinarith
  · have hp5 : 5 ≤ p := hp
    have hpr : (5 : ℝ) ≤ (p : ℝ) := by exact_mod_cast hp5
    nlinarith

/-- The multiplier the chapter needs falls strictly between the 4:1 and 5:1
    locks, so it lies in no p:1 tongue. -/
theorem required_multiplier_strictly_between_locks :
    lockFreq f1_obs 4 < f4_claimed ∧ f4_claimed < lockFreq f1_obs 5 := by
  unfold lockFreq f1_obs f4_claimed
  constructor <;> norm_num

/-! ## §3  Facts 16-18 of `G6Crystal.lean` do not select 33

`g6_within_2pct_of_f4` proves |33 - 33.516| / 33.516 < 2/100.  That is a
true statement about two numerals.  It is not evidence for 33, because the
same band admits every real in [32.85, 34.18] -- 34 among them, and 34 has
no role anywhere in the framework.  A test an adjacent integer also passes
carries no information about the integer it was written for.

Separately: 33 is dimensionless in `G6Crystal.lean` (it is simultaneously
g6_int, the conjectured Euler characteristic, a cubit count of 33,000, and
3 x 11), while 33.516 is in hertz.  Fact 16 compares the two directly.
Units before data: that comparison has no physical content, whatever its
numeric value. -/

theorem thirtythree_in_band :
    |(33 : ℝ) - f4_claimed| < 2 / 100 * f4_claimed := by
  unfold f4_claimed
  rw [abs_of_nonpos (by norm_num)]
  norm_num

theorem thirtyfour_also_in_band :
    |(34 : ℝ) - f4_claimed| < 2 / 100 * f4_claimed := by
  unfold f4_claimed
  rw [abs_of_nonneg (by norm_num)]
  norm_num

/-- The 2% band is a whole interval, not a selection. -/
theorem band_2pct_admits_an_interval (m : ℝ)
    (hlo : 32.85 ≤ m) (hhi : m ≤ 34.18) :
    |m - f4_claimed| < 2 / 100 * f4_claimed := by
  unfold f4_claimed
  have h : |m - (33.516 : ℝ)| < 0.67032 := by
    rw [abs_lt]
    constructor <;> linarith
  calc |m - (33.516 : ℝ)| < 0.67032 := h
    _ = 2 / 100 * 33.516 := by norm_num

/-! ## §4  Saturn's hexagon is not a 66:1 tower

Cassini places the hexagonal wavenumber-6 boundary near 78 deg N,
~29,000 km across.  Fletcher et al. (Nat. Commun. 9:3564, 2018) trace it
over a vertical range of ~300 km, from the 2-3 bar troposphere into the
stratosphere.  Height/width ~ 0.01.  Chapter W's claim that Saturn's
hexagon has "an aspect ratio matching the G6 crystal" (66) is wrong by
more than three orders of magnitude, and in the wrong direction: the
feature is flat, not slender. -/

def saturn_width_km : ℝ := 29000
def saturn_height_km : ℝ := 300

theorem saturn_hexagon_is_flat :
    saturn_height_km < saturn_width_km / 90 := by
  unfold saturn_height_km saturn_width_km; norm_num

/-- Even inflated a thousandfold, the measured aspect ratio stays below 66. -/
theorem saturn_aspect_off_by_three_orders :
    1000 * saturn_height_km < 66 * saturn_width_km := by
  unfold saturn_height_km saturn_width_km; norm_num

/-! ## §5  Section 3 of `G6Crystal.lean`: the hexagon is not the optimum

Its section docstring says "A/P^2 is maximised for the regular hexagon
among all regular n-gons".  That is false.  For a regular n-gon,
A/P^2 = cot(pi/n) / (4n), which is strictly increasing in n and tends to
1/(4*pi).  The two theorems in that section prove only hexagon > square,
which is true and stays true.  The general claim in the docstring is not,
and the octagon is a one-line counterexample.

The correct optimality statement for hexagons is Hales' honeycomb theorem
(1999): least total perimeter among *tilings* of the plane, not largest
A/P^2 for a single cell.  Those are different claims, and the tiling one
is the one the architecture argument actually wants. -/

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

/-! ## §6  `arnold_tongue_A4_coupling` is vacuous, and the gate cannot see it

`G6Crystal.lean`'s header lists three sorries (S1 Arnold tongue, S2
hexagrid collapse, S3 coord coverage).  S1 and S2 are not sorries.  They are

    theorem arnold_tongue_A4_coupling :
        forall d : Real, ‖d‖ < noise_tolerance -> True
    theorem hexagrid_collapse_resistance_superior : True

both discharged by `trivial`.  The file therefore reports zero sorries and
`#print axioms` shows no `sorryAx`, while the two open obligations its own
header discloses are invisible to the kernel.  This is the failure mode
this project has caught three times before: a theorem whose name promises
more than its statement says.  A gate that counts sorries does not catch
it; reading the statement does.

Nothing in this file replaces S1.  A real Arnold-tongue statement needs
Poincare-map and rotation-number theory Mathlib does not yet carry.  What
§2 establishes is narrower and still load-bearing: whatever that theory
turns out to say, it cannot deliver 33.516 Hz from a 7.83 Hz driver at any
p:1 lock.  S1 should be restated as an honest `sorry` on a proposition that
says something, or deleted. -/

/-! ## §7  What the companion page gets right

`wigner-fractal.html` puts the 2D Wigner crystallisation threshold at
r_s* ~ 30-40.  That band contains both standing quantum Monte Carlo
estimates: Tanatar & Ceperley (PRB 39:5005, 1989) give r_s ~ 37 +/- 5, and
Drummond & Needs (PRL 102:126402, 2009) give r_s = 31(1).  The triangular
lattice as the 2D ground state is Bonsall & Maradudin (PRB 15:1959, 1977).
Both are correctly reported, and the page's B-field slider raises the
effective r_s -- the right direction, since Landau quantisation suppresses
kinetic energy and so favours the crystal.

The order of the transition is genuinely open: Drummond & Needs note it has
been argued the 2D fluid-to-crystal transition cannot be first order, and
do not settle it.  So the page's fold (continuous, soft-mode) picture is a
modelling choice, not a derived fact, and should be labelled as one. -/

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
#print axioms no_integer_lock_reaches_claimed_f4
#print axioms thirtyfour_also_in_band
#print axioms band_2pct_admits_an_interval
#print axioms saturn_aspect_off_by_three_orders
#print axioms octagon_beats_hexagon
#print axioms disc_beats_hexagon
#print axioms page_band_contains_drummond

end Orthogenesis.WignerChecks
