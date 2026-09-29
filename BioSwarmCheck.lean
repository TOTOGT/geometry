/-
  BioSwarmCheck.lean -- what the fruit-fly toy model's operator pipeline actually does.
  Model: Nogueira Grossi, "Biological Transitions as Multi-Agent Realisations of the Generative
  Operator Pipeline ... A Fruit-Fly Connectome Toy Model", V2 (Zenodo 10.5281/zenodo.20128568).

  One agent state is a pair (x, y). The stages, as in multi_orbit_bioswarm.py:
    C  keep the larger coordinate, zero the other          (ties go to x)
    K  add b * sgn to each coordinate, clip to [-1, 1]      (sgn 0 = +1, as numpy's sign(s + 1e-12))
    F  (1 - α) s + α n                                      (n = the neighbour's state)
    U  s / |s|                                              (s ≠ 0)

  Proved:
    C_jumps            C sends (1, 999/1000) and (999/1000, 1), which are 1/500 apart in ℓ¹, to points 2 apart:
                       C is not continuous, so G has no Lipschitz constant for any α
    U_norm             every output of U with s ≠ 0 has x² + y² = 1
    four_fixed_points  at α = 0 (where the paper's formula gives L = 1/2) the one-agent map has four distinct fixed points
-/
import Mathlib

namespace BioSwarmCheck

noncomputable section

def C (s : ℝ × ℝ) : ℝ × ℝ := if |s.2| ≤ |s.1| then (s.1, 0) else (0, s.2)

def sgn (x : ℝ) : ℝ := if 0 ≤ x then 1 else -1

def clip (x : ℝ) : ℝ := max (-1) (min 1 x)

def K (b : ℝ) (s : ℝ × ℝ) : ℝ × ℝ := (clip (s.1 + b * sgn s.1), clip (s.2 + b * sgn s.2))

def F (α : ℝ) (s n : ℝ × ℝ) : ℝ × ℝ := ((1 - α) * s.1 + α * n.1, (1 - α) * s.2 + α * n.2)

def nrm (s : ℝ × ℝ) : ℝ := Real.sqrt (s.1 ^ 2 + s.2 ^ 2)

def U (s : ℝ × ℝ) : ℝ × ℝ := (s.1 / nrm s, s.2 / nrm s)

/-- One application of G = U ∘ F ∘ K ∘ C, with bias b = 1/10. -/
def G (α : ℝ) (s n : ℝ × ℝ) : ℝ × ℝ := U (F α (K (1 / 10) (C s)) n)

def l1 (s t : ℝ × ℝ) : ℝ := |s.1 - t.1| + |s.2 - t.2|

theorem C_jumps :
    l1 (1, 999 / 1000) (999 / 1000, 1) = 1 / 500 ∧
    l1 (C (1, 999 / 1000)) (C (999 / 1000, 1)) = 2 := by
  refine ⟨?_, ?_⟩
  · simp only [l1]; norm_num [abs_of_pos, abs_of_neg]
  · simp only [C, l1]
    norm_num [abs_of_pos]

theorem U_norm (s : ℝ × ℝ) (hs : s ≠ 0) : (U s).1 ^ 2 + (U s).2 ^ 2 = 1 := by
  have hpos : 0 < s.1 ^ 2 + s.2 ^ 2 := by
    rcases s with ⟨a, b⟩
    by_contra h
    have h1 : a ^ 2 + b ^ 2 = 0 := le_antisymm (not_lt.mp h) (by positivity)
    have ha : a = 0 := by nlinarith [sq_nonneg a, sq_nonneg b]
    have hb : b = 0 := by nlinarith [sq_nonneg a, sq_nonneg b]
    exact hs (by simp [ha, hb])
  have hn : 0 < nrm s := Real.sqrt_pos.mpr hpos
  have hsq : nrm s ^ 2 = s.1 ^ 2 + s.2 ^ 2 := Real.sq_sqrt hpos.le
  simp only [U, div_pow]
  rw [← add_div, ← hsq]
  exact div_self (by positivity)

/-- r = √(101/100), the length of (1, 1/10). -/
def r : ℝ := Real.sqrt (101 / 100)

lemma r_pos : 0 < r := Real.sqrt_pos.mpr (by norm_num)
lemma r_sq : r ^ 2 = 101 / 100 := Real.sq_sqrt (by norm_num)
lemma r_ge_one : 1 ≤ r := by
  rw [show (1 : ℝ) = Real.sqrt 1 by simp]; exact Real.sqrt_le_sqrt (by norm_num)
lemma r_le : r ≤ 11 / 10 := by
  rw [show (11 / 10 : ℝ) = Real.sqrt ((11 / 10) ^ 2) by rw [Real.sqrt_sq]; norm_num]
  exact Real.sqrt_le_sqrt (by norm_num)
lemma inv_r_ge : 9 / 10 ≤ 1 / r := by
  rw [le_div_iff₀ r_pos]; nlinarith [r_le]
lemma inv_r_le : 1 / r ≤ 1 := by
  rw [div_le_iff₀ r_pos]; linarith [r_ge_one]

lemma nrm_pair (p q : ℝ) (h : p ^ 2 + q ^ 2 = 101 / 100) : nrm (p, q) = r := by
  simp only [nrm, r, h]

/-- The four fixed points: (±1, 1/10)/r rotated through the four axis directions. -/
def P1 : ℝ × ℝ := (1 / r, (1 / 10) / r)
def P2 : ℝ × ℝ := (-1 / r, (1 / 10) / r)
def P3 : ℝ × ℝ := ((1 / 10) / r, 1 / r)
def P4 : ℝ × ℝ := ((1 / 10) / r, -1 / r)

lemma clip_of_ge (x : ℝ) (h : 1 ≤ x) : clip x = 1 := by
  simp [clip, min_eq_left h]
lemma clip_of_le (x : ℝ) (h : x ≤ -1) : clip x = -1 := by
  simp only [clip]; rw [min_eq_right (by linarith)]; exact max_eq_left h
lemma clip_mid (x : ℝ) (h1 : -1 ≤ x) (h2 : x ≤ 1) : clip x = x := by
  simp [clip, min_eq_right h2, max_eq_right h1]

theorem fixed_P1 : G 0 P1 P1 = P1 := by
  have hr := r_pos; have a := inv_r_ge; have b := inv_r_le
  have hC : C P1 = (1 / r, 0) := by
    simp only [C, P1]
    rw [if_pos]
    rw [abs_of_pos (by positivity), abs_of_pos (by positivity)]
    rw [div_le_div_iff_of_pos_right hr]; norm_num
  have hK : K (1 / 10) (1 / r, 0) = (1, 1 / 10) := by
    simp only [K, sgn]
    rw [if_pos (by positivity), if_pos le_rfl]
    rw [clip_of_ge _ (by linarith), clip_mid _ (by norm_num) (by norm_num)]
    norm_num
  simp only [G, hC, hK, F, U]
  norm_num
  rw [nrm_pair 1 (1 / 10) (by norm_num)]
  try simp [P1]

theorem fixed_P2 : G 0 P2 P2 = P2 := by
  have hr := r_pos; have a := inv_r_ge; have b := inv_r_le
  have hC : C P2 = (-1 / r, 0) := by
    simp only [C, P2]
    rw [if_pos]
    have e1 : |(-1 : ℝ) / r| = 1 / r := by rw [abs_div, abs_neg, abs_one, abs_of_pos hr]
    have e2 : |(1 / 10 : ℝ) / r| = (1 / 10) / r := abs_of_pos (by positivity)
    rw [e1, e2, div_le_div_iff_of_pos_right hr]; norm_num
  have hK : K (1 / 10) (-1 / r, 0) = (-1, 1 / 10) := by
    have hneg : -1 / r < 0 := div_neg_of_neg_of_pos (by norm_num) hr
    simp only [K, sgn]
    rw [if_neg (not_le.mpr hneg), if_pos le_rfl]
    have : -1 / r = -(1 / r) := by ring
    rw [clip_of_le _ (by rw [this]; linarith), clip_mid _ (by norm_num) (by norm_num)]
    norm_num
  simp only [G, hC, hK, F, U]
  norm_num
  rw [nrm_pair (-1) (1 / 10) (by norm_num)]
  try simp [P2]
  try ring

theorem fixed_P3 : G 0 P3 P3 = P3 := by
  have hr := r_pos; have a := inv_r_ge; have b := inv_r_le
  have hC : C P3 = (0, 1 / r) := by
    simp only [C, P3]
    rw [if_neg]
    rw [abs_of_pos (by positivity), abs_of_pos (by positivity)]
    rw [not_le, div_lt_div_iff_of_pos_right hr]; norm_num
  have hK : K (1 / 10) (0, 1 / r) = (1 / 10, 1) := by
    simp only [K, sgn]
    rw [if_pos le_rfl, if_pos (by positivity)]
    rw [clip_mid (0 + 1 / 10 * 1) (by norm_num) (by norm_num), clip_of_ge _ (by linarith)]
    norm_num
  simp only [G, hC, hK, F, U]
  norm_num
  rw [nrm_pair (1 / 10) 1 (by norm_num)]
  try simp [P3]

theorem fixed_P4 : G 0 P4 P4 = P4 := by
  have hr := r_pos; have a := inv_r_ge; have b := inv_r_le
  have hC : C P4 = (0, -1 / r) := by
    simp only [C, P4]
    rw [if_neg]
    have e1 : |(-1 : ℝ) / r| = 1 / r := by rw [abs_div, abs_neg, abs_one, abs_of_pos hr]
    have e2 : |(1 / 10 : ℝ) / r| = (1 / 10) / r := abs_of_pos (by positivity)
    rw [e1, e2, not_le, div_lt_div_iff_of_pos_right hr]; norm_num
  have hK : K (1 / 10) (0, -1 / r) = (1 / 10, -1) := by
    have hneg : -1 / r < 0 := div_neg_of_neg_of_pos (by norm_num) hr
    simp only [K, sgn]
    rw [if_pos le_rfl, if_neg (not_le.mpr hneg)]
    have : -1 / r = -(1 / r) := by ring
    rw [clip_mid (0 + 1 / 10 * 1) (by norm_num) (by norm_num), clip_of_le _ (by rw [this]; linarith)]
    norm_num
  simp only [G, hC, hK, F, U]
  norm_num
  rw [nrm_pair (1 / 10) (-1) (by norm_num)]
  try simp [P4]
  try ring

theorem four_fixed_points :
    G 0 P1 P1 = P1 ∧ G 0 P2 P2 = P2 ∧ G 0 P3 P3 = P3 ∧ G 0 P4 P4 = P4 ∧
    P1 ≠ P2 ∧ P1 ≠ P3 ∧ P1 ≠ P4 ∧ P2 ≠ P3 ∧ P2 ≠ P4 ∧ P3 ≠ P4 := by
  have hr := r_pos
  have h1 : (1 : ℝ) / r ≠ -1 / r := by
    intro h; have := (div_left_inj' hr.ne').mp h; norm_num at this
  have h2 : (1 : ℝ) / r ≠ (1 / 10) / r := by
    intro h; have := (div_left_inj' hr.ne').mp h; norm_num at this
  have h3 : (-1 : ℝ) / r ≠ (1 / 10) / r := by
    intro h; have := (div_left_inj' hr.ne').mp h; norm_num at this
  have h4 : (1 / 10 : ℝ) / r ≠ -1 / r := by
    intro h; have := (div_left_inj' hr.ne').mp h; norm_num at this
  have h5 : (1 : ℝ) / r ≠ -1 / r := h1
  refine ⟨fixed_P1, fixed_P2, fixed_P3, fixed_P4,
    fun h => h1 (congrArg Prod.fst h), fun h => h2 (congrArg Prod.fst h),
    fun h => h2 (congrArg Prod.fst h), fun h => h3 (congrArg Prod.fst h),
    fun h => h3 (congrArg Prod.fst h), fun h => h5 (congrArg Prod.snd h)⟩

end

end BioSwarmCheck

#print axioms BioSwarmCheck.C_jumps
#print axioms BioSwarmCheck.U_norm
#print axioms BioSwarmCheck.four_fixed_points
