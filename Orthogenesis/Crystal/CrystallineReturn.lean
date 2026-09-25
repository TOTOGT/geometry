-- GATE-DECLARE: sorries = none
-- GATE-REASON: new file 2026-09-25 for the geometry pin (Lean v4.32.0, Mathlib v4.32.0).
-- UNTESTED until the author runs `lake build` on it.
/-
# CrystallineReturn.lean — Book 3, Chapter 7 · The Crystalline Return (taught path 33,
# ch7-crystalline.html; the same page serves the Cajueiro edition)

Companions already kernel-audited in this repo: NbonacciLadder.lean (every
n-bonacci term is < 2^k) and SaturnHexagon.lean (the six-sextant D₆ model).

  §1  The n-bonacci table. The first ten terms printed for n = 2…6 are exactly
      right, and each printed limit ratio (1.6180…, 1.8392…, 1.9275…, 1.9659…,
      1.9835…) is within 10⁻⁴ of a root of xⁿ − xⁿ⁻¹ − … − 1 (sign change).
  §2  The honeycomb. For one unit of area, the squared perimeters of the three
      regular tilings are 12√3 (triangle), 16 (square), 8√3 (hexagon): the
      hexagon is the smallest — the elementary case behind Hales' theorem.
  §3  D₆ has 12 elements, as stated.
  §4  The Monster. The printed order equals 2⁴⁶·3²⁰·5⁹·7⁶·11²·13³·17·19·23·29·31·41·47·59·71,
      and the moonshine identities 196884 = 1 + 196883 and
      21493760 = 1 + 196883 + 21296876 hold.

Not formalisable here, and corrected in the chapter note instead: the Collatz
conjecture is not a Millennium Prize Problem (the seven are Birch–Swinnerton-Dyer,
Hodge, Navier–Stokes, P vs NP, Poincaré, Riemann, Yang–Mills), and no argument
is given that one proof would settle Collatz, BSD and Navier–Stokes together.
-/

import Mathlib

namespace Orthogenesis.CrystallineReturn

/-! ## §1 The n-bonacci table -/

/-- Append the sum of the last n terms. -/
def nbStep (n : ℕ) (l : List ℕ) : List ℕ := l ++ [(l.reverse.take n).sum]

/-- The first k terms of the n-bonacci sequence starting from 1. -/
def nbList (n k : ℕ) : List ℕ := (nbStep n)^[k - 1] [1]

theorem fibonacci_row : nbList 2 10 = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55] := by decide
theorem tribonacci_row : nbList 3 10 = [1, 1, 2, 4, 7, 13, 24, 44, 81, 149] := by decide
theorem tetranacci_row : nbList 4 10 = [1, 1, 2, 4, 8, 15, 29, 56, 108, 208] := by decide
theorem pentanacci_row : nbList 5 10 = [1, 1, 2, 4, 8, 16, 31, 61, 120, 236] := by decide
theorem hexanacci_row : nbList 6 10 = [1, 1, 2, 4, 8, 16, 32, 63, 125, 248] := by decide

/-- p_n(x) = xⁿ − (xⁿ⁻¹ + … + 1). -/
def pn (n : ℕ) (x : ℚ) : ℚ := x ^ n - ∑ k ∈ Finset.range n, x ^ k

theorem root2_bracket : pn 2 1.6180 < 0 ∧ 0 < pn 2 1.6181 := by
  constructor <;> norm_num [pn, Finset.sum_range_succ]
theorem root3_bracket : pn 3 1.8392 < 0 ∧ 0 < pn 3 1.8393 := by
  constructor <;> norm_num [pn, Finset.sum_range_succ]
theorem root4_bracket : pn 4 1.9275 < 0 ∧ 0 < pn 4 1.9276 := by
  constructor <;> norm_num [pn, Finset.sum_range_succ]
theorem root5_bracket : pn 5 1.9659 < 0 ∧ 0 < pn 5 1.9660 := by
  constructor <;> norm_num [pn, Finset.sum_range_succ]
theorem root6_bracket : pn 6 1.9835 < 0 ∧ 0 < pn 6 1.9836 := by
  constructor <;> norm_num [pn, Finset.sum_range_succ]

/-! ## §2 The honeycomb: squared perimeter per unit area -/

theorem hexagon_least_perimeter :
    8 * Real.sqrt 3 < 16 ∧ (16 : ℝ) < 12 * Real.sqrt 3 := by
  have h := Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 3)
  have hs := Real.sqrt_nonneg 3
  constructor <;> nlinarith

/-! ## §3 D₆ -/

theorem dihedral6_card : Fintype.card (DihedralGroup 6) = 12 := by
  simp [DihedralGroup.card]

/-! ## §4 The Monster -/

theorem monster_order :
    (2 ^ 46 * 3 ^ 20 * 5 ^ 9 * 7 ^ 6 * 11 ^ 2 * 13 ^ 3 * 17 * 19 * 23 * 29 * 31 * 41 * 47
      * 59 * 71 : ℕ) = 808017424794512875886459904961710757005754368000000000 := by
  norm_num

theorem moonshine_first : (196884 : ℕ) = 1 + 196883 := by norm_num

theorem moonshine_second : (21493760 : ℕ) = 1 + 196883 + 21296876 := by norm_num

end Orthogenesis.CrystallineReturn

/-! ## Axiom probe -/
#print axioms Orthogenesis.CrystallineReturn.fibonacci_row
#print axioms Orthogenesis.CrystallineReturn.tribonacci_row
#print axioms Orthogenesis.CrystallineReturn.tetranacci_row
#print axioms Orthogenesis.CrystallineReturn.pentanacci_row
#print axioms Orthogenesis.CrystallineReturn.hexanacci_row
#print axioms Orthogenesis.CrystallineReturn.root2_bracket
#print axioms Orthogenesis.CrystallineReturn.root3_bracket
#print axioms Orthogenesis.CrystallineReturn.root4_bracket
#print axioms Orthogenesis.CrystallineReturn.root5_bracket
#print axioms Orthogenesis.CrystallineReturn.root6_bracket
#print axioms Orthogenesis.CrystallineReturn.hexagon_least_perimeter
#print axioms Orthogenesis.CrystallineReturn.dihedral6_card
#print axioms Orthogenesis.CrystallineReturn.monster_order
#print axioms Orthogenesis.CrystallineReturn.moonshine_first
#print axioms Orthogenesis.CrystallineReturn.moonshine_second
