/-
Book17Ch02.lean -- three small, self-contained facts about the squared
Euclidean distance function on ℝ², backing
book17/ch02-the-distance-a-plane-actually-flies.html.

UNTESTED: no Lean toolchain in the session that wrote this (2026-09-22),
same constraint noted throughout this corpus and its sibling catgt project.
`ring` and `positivity` are common enough tactics that these should close;
the exact Mathlib lemma name used for the third theorem (`Real.sq_sqrt`) is
this session's best recollection, not a confirmed one. Re-run against a real
kernel, fix whatever the compiler actually says, report the output -- do not
edit this comment to claim a run that has not happened.

    lake env lean book17/Book17Ch02.lean       # from a mathlib4 checkout
-/
import Mathlib.Data.Real.Sqrt

namespace Book17Ch02

/-- The squared straight-line distance between (x0,y0) and (x1,y1) in ℝ²,
as Equation 1.1 (Stitz & Zeager §1.1.3) computes it before the square root. -/
def distSq (x0 y0 x1 y1 : ℝ) : ℝ := (x1 - x0) ^ 2 + (y1 - y0) ^ 2

/-- Squared distance does not care which point is listed first -- swapping
P and Q negates each leg, and squaring erases the sign. -/
theorem distSq_symm (x0 y0 x1 y1 : ℝ) :
    distSq x0 y0 x1 y1 = distSq x1 y1 x0 y0 := by
  unfold distSq; ring

/-- Squared distance is never negative: a sum of two squares. -/
theorem distSq_nonneg (x0 y0 x1 y1 : ℝ) : 0 ≤ distSq x0 y0 x1 y1 := by
  unfold distSq; positivity

/-- Taking the square root of the squared distance and squaring the result
returns the original squared distance -- the fact the page's Part III leans
on implicitly whenever it moves between Equation 1.1's `d` and the `d²`
this file actually proves things about. -/
theorem sqrt_distSq_sq (x0 y0 x1 y1 : ℝ) :
    Real.sqrt (distSq x0 y0 x1 y1) ^ 2 = distSq x0 y0 x1 y1 :=
  Real.sq_sqrt (distSq_nonneg x0 y0 x1 y1)

end Book17Ch02
