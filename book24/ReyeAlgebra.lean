import Mathlib

/-
Book XXIV, Interlude 2: the algebra of the limiting blow-up speed r_eye (Merle, Raphael, Rodnianski, Szeftel,
arXiv:1912.11009v2, eq. (1.4), (1.8), (1.16); read on the typeset pages 4 and 5).

STATUS: COMPILED 2026-11-04, ALL FOUR CLEAN. The report reye.axioms.txt lists all four theorems with axioms
[propext, Classical.choice, Quot.sound] only and no sorryAx. History: the first run failed on `threshold_three`
because `div_lt_div_iff` is no longer a Mathlib name; the rewrite (fractions cleared with `field_simp`, then linear
arithmetic) compiled. The report also holds two deprecation warnings for `push_neg` (newer Mathlib prefers `push Not`);
they are not errors.

WHAT IT STATES (real-number algebra only):
  branch_agree / branch_agree_d   the two branches r_* and r_+ of r_eye are equal at l = d, for every d > 0
                                  (value 2 sqrt d / (sqrt d + 1); 3 - sqrt 3 for d = 3)
  threshold_three                 for l > 0:  (2+l)/(1+l) < (3+l)/(l+sqrt 3)  iff  sqrt 3 < l   (eq. (1.8), d = 3)
  plus_branch_positive            for t = sqrt l > 0, t != 1:  (2+t^2)/(1+t^2) < 1 + 2/(1+t)^2   (the r_+ branch, d = 3)

WHAT IT DOES NOT STATE. The compressible Euler equations, the self-similar ODE, the sonic point, the existence of
smooth self-similar profiles, the eigenvalue ratio k(r), the blow-up theorem. Those are the content of the papers
and are not formalised here. The derivation of r_eye from the ODE is checked numerically, not in Lean
(see book24/reye-derive.py), and only for the branch l < d.
-/

namespace Book24Re

theorem branch_agree (s : ℝ) (hs : 0 < s) :
    (s ^ 2 + s ^ 2) / (s ^ 2 + s) = 1 + (s ^ 2 - 1) / (1 + s) ^ 2 := by
  have h1 : s ^ 2 + s ≠ 0 := by positivity
  have h2 : (1 + s) ^ 2 ≠ 0 := by positivity
  field_simp
  ring

theorem branch_agree_d (d : ℝ) (hd : 0 < d) :
    (d + d) / (d + Real.sqrt d) = 1 + (d - 1) / (1 + Real.sqrt d) ^ 2 := by
  have h := branch_agree (Real.sqrt d) (Real.sqrt_pos.2 hd)
  rwa [Real.sq_sqrt hd.le] at h

theorem threshold_three (l : ℝ) (hl : 0 < l) :
    (2 + l) / (1 + l) < (3 + l) / (l + Real.sqrt 3) ↔ Real.sqrt 3 < l := by
  have hs2 : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have hs0 : 0 < Real.sqrt 3 := Real.sqrt_pos.2 (by norm_num)
  have hs4 : Real.sqrt 3 < 2 := by nlinarith
  have hpos1 : 0 < 1 + l := by linarith
  have hpos2 : 0 < l + Real.sqrt 3 := by linarith
  have hne1 : (1 + l) ≠ 0 := hpos1.ne'
  have hne2 : (l + Real.sqrt 3) ≠ 0 := hpos2.ne'
  have hx : (2 + l) / (1 + l) * (1 + l) = 2 + l := by field_simp
  have hy : (3 + l) / (l + Real.sqrt 3) * (l + Real.sqrt 3) = 3 + l := by field_simp
  generalize (2 + l) / (1 + l) = x at hx ⊢
  generalize (3 + l) / (l + Real.sqrt 3) = y at hy ⊢
  have key : (3 + l) * (1 + l) - (2 + l) * (l + Real.sqrt 3)
      = (2 - Real.sqrt 3) * (l - Real.sqrt 3) := by
    linear_combination (-1 : ℝ) * hs2
  have hid : (y - x) * ((1 + l) * (l + Real.sqrt 3))
      = (3 + l) * (1 + l) - (2 + l) * (l + Real.sqrt 3) := by
    linear_combination (1 + l) * hy - (l + Real.sqrt 3) * hx
  have hD : 0 < (1 + l) * (l + Real.sqrt 3) := mul_pos hpos1 hpos2
  constructor
  · intro h
    have h1 : 0 < (y - x) * ((1 + l) * (l + Real.sqrt 3)) := mul_pos (sub_pos.2 h) hD
    by_contra hc
    push_neg at hc
    nlinarith [mul_nonneg (sub_nonneg.2 hs4.le) (sub_nonneg.2 hc)]
  · intro h
    by_contra hc
    push_neg at hc
    nlinarith [mul_nonneg (sub_nonneg.2 hc) hD.le, mul_pos (sub_pos.2 hs4) (sub_pos.2 h)]

theorem plus_branch_positive (t : ℝ) (ht : 0 < t) (h1 : t ≠ 1) :
    (2 + t ^ 2) / (1 + t ^ 2) < 1 + 2 / (1 + t) ^ 2 := by
  have hne : t - 1 ≠ 0 := sub_ne_zero.2 h1
  have e : 1 + 2 / (1 + t) ^ 2 - (2 + t ^ 2) / (1 + t ^ 2)
      = (t - 1) ^ 2 / ((1 + t) ^ 2 * (1 + t ^ 2)) := by
    have a : (1 + t) ^ 2 ≠ 0 := by positivity
    have b : 1 + t ^ 2 ≠ 0 := by positivity
    field_simp
    ring
  have : 0 < (t - 1) ^ 2 / ((1 + t) ^ 2 * (1 + t ^ 2)) := by positivity
  linarith

end Book24Re

#print axioms Book24Re.branch_agree
#print axioms Book24Re.branch_agree_d
#print axioms Book24Re.threshold_three
#print axioms Book24Re.plus_branch_positive
