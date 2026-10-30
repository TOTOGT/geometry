import Mathlib

/-!
# LatticeDensity — lattice dimensions log N / log m are dense in [0, 4]
(book4/pi.html §3, "the lattice trap")

STATUS: NOT YET COMPILED. Written against Mathlib names recalled from memory; the author runs
`lake env lean book4/LatticeDensity.lean` and errors are fixed against what the compiler says.

CLAIMS, if it compiles:
1. `lattice_error`   — for real d with 0 < d ≤ 4 and m ≥ 2 with x = m^d ≥ 2, N := ⌊x⌋ satisfies
      1 ≤ N ≤ m^4   and   0 ≤ d − log N / log m ≤ log 2 / log m.
   (The cruder of the two bounds on the page; the sharper 2/(x log m) is proved by hand there and
   only checked numerically in lattice-density-check.py, not in Lean.)
2. `lattice_dense`   — hence for every d ∈ (0, 4] and ε > 0 there are naturals m ≥ 2, N with
      1 ≤ N ≤ m^4 and |log N / log m − d| < ε.
   So the lattice dimensions {log N / log m : 1 ≤ N ≤ m^4} are dense in (0, 4], and in particular
   infinitely many distinct values lie in every interval.

NOT CLAIMED: that a lattice set with these N pieces has Hausdorff dimension log N / log m (that is
the quoted theorem for self-similar sets with the open set condition; here the pieces are distinct
cells of an m-grid in [0,1]^4, so the open set condition holds, but that is not formalised); nothing
about hitting π exactly.
-/

open Real

lemma floor_two_le (x : ℝ) (hx : 2 ≤ x) :
    x / 2 ≤ (⌊x⌋₊ : ℝ) ∧ (⌊x⌋₊ : ℝ) ≤ x := by
  have h1 : (⌊x⌋₊ : ℝ) ≤ x := Nat.floor_le (by linarith)
  have h2 : x < (⌊x⌋₊ : ℝ) + 1 := Nat.lt_floor_add_one x
  exact ⟨by linarith, h1⟩

theorem lattice_error (d : ℝ) (_hd : 0 < d) (hd4 : d ≤ 4) (m : ℕ) (hm : 2 ≤ m)
    (hx : 2 ≤ (m : ℝ) ^ d) :
    1 ≤ ⌊(m : ℝ) ^ d⌋₊ ∧ ⌊(m : ℝ) ^ d⌋₊ ≤ m ^ 4 ∧
    0 ≤ d - Real.log (⌊(m : ℝ) ^ d⌋₊) / Real.log m ∧
    d - Real.log (⌊(m : ℝ) ^ d⌋₊) / Real.log m ≤ Real.log 2 / Real.log m := by
  set x : ℝ := (m : ℝ) ^ d with hxdef
  have hm1 : (1 : ℝ) < m := by exact_mod_cast hm
  have hmpos : (0 : ℝ) < m := by linarith
  have hlogm : 0 < Real.log m := Real.log_pos hm1
  obtain ⟨hlo, hhi⟩ := floor_two_le x hx
  have hNreal : (1 : ℝ) ≤ (⌊x⌋₊ : ℝ) := by linarith
  have hNpos : (0 : ℝ) < (⌊x⌋₊ : ℝ) := by linarith
  refine ⟨?_, ?_, ?_, ?_⟩
  · exact_mod_cast hNreal
  · have h4 : x ≤ (m : ℝ) ^ (4 : ℝ) :=
      Real.rpow_le_rpow_of_exponent_le hm1.le hd4
    have h5 : (m : ℝ) ^ (4 : ℝ) = (m : ℝ) ^ (4 : ℕ) := by
      exact_mod_cast Real.rpow_natCast (m : ℝ) 4
    have : (⌊x⌋₊ : ℝ) ≤ (m : ℝ) ^ (4 : ℕ) :=
      calc (⌊x⌋₊ : ℝ) ≤ x := hhi
        _ ≤ (m : ℝ) ^ (4 : ℝ) := h4
        _ = (m : ℝ) ^ (4 : ℕ) := h5
    exact_mod_cast this
  · have hlx : Real.log x = d * Real.log m := by
      rw [hxdef, Real.log_rpow hmpos]
    have : Real.log (⌊x⌋₊ : ℝ) ≤ Real.log x := Real.log_le_log hNpos hhi
    rw [sub_nonneg, div_le_iff₀ hlogm]
    nlinarith
  · have hlx : Real.log x = d * Real.log m := by
      rw [hxdef, Real.log_rpow hmpos]
    have hx0 : 0 < x := by linarith
    have h1 : Real.log (x / 2) ≤ Real.log (⌊x⌋₊ : ℝ) :=
      Real.log_le_log (by linarith) hlo
    rw [Real.log_div hx0.ne' (by norm_num)] at h1
    have : d - Real.log (⌊x⌋₊ : ℝ) / Real.log m
        = (d * Real.log m - Real.log (⌊x⌋₊ : ℝ)) / Real.log m := by
      field_simp
    rw [this]
    apply div_le_div_of_nonneg_right _ hlogm.le
    linarith

theorem lattice_dense (d ε : ℝ) (hd : 0 < d) (hd4 : d ≤ 4) (hε : 0 < ε) :
    ∃ m N : ℕ, 2 ≤ m ∧ 1 ≤ N ∧ N ≤ m ^ 4 ∧ |Real.log N / Real.log m - d| < ε := by
  -- choose m with log m > max (log 2 / ε) (log 2 / d)
  set t : ℝ := Real.log 2 / min ε d + 1 with ht
  have hmin : 0 < min ε d := lt_min hε hd
  have hlog2 : 0 < Real.log 2 := Real.log_pos (by norm_num)
  have htpos : 0 < t := by positivity
  set m : ℕ := ⌈Real.exp t⌉₊ with hmdef
  have hmge : Real.exp t ≤ (m : ℝ) := Nat.le_ceil _
  have hm2 : 2 ≤ m := by
    have : (1 : ℝ) < Real.exp t := by rw [← Real.exp_zero]; exact Real.exp_lt_exp.mpr htpos
    have h2 : (1 : ℝ) < (m : ℝ) := lt_of_lt_of_le this hmge
    have : 1 < m := by exact_mod_cast h2
    omega
  have hmpos : (0 : ℝ) < m := by
    have : (1 : ℝ) < m := by exact_mod_cast hm2
    linarith
  have hlogm : t ≤ Real.log m := by
    have := Real.log_le_log (Real.exp_pos t) hmge
    rwa [Real.log_exp] at this
  have hA : Real.log 2 / min ε d < Real.log m := by
    have : Real.log 2 / min ε d < t := by rw [ht]; linarith
    linarith
  have hlm : 0 < Real.log m := by linarith
  have hmε : Real.log 2 / Real.log m < ε := by
    rw [div_lt_iff₀ hlm]
    have h1 : Real.log 2 < min ε d * Real.log m := by
      have := (div_lt_iff₀ hmin).mp hA
      linarith
    have h2 : min ε d * Real.log m ≤ ε * Real.log m :=
      mul_le_mul_of_nonneg_right (min_le_left _ _) hlm.le
    linarith
  have hx : 2 ≤ (m : ℝ) ^ d := by
    have h1 : Real.log 2 < d * Real.log m := by
      have h3 : Real.log 2 < min ε d * Real.log m := by
        have := (div_lt_iff₀ hmin).mp hA
        linarith
      have h4 : min ε d * Real.log m ≤ d * Real.log m :=
        mul_le_mul_of_nonneg_right (min_le_right _ _) hlm.le
      linarith
    have h5 : (m : ℝ) ^ d = Real.exp (d * Real.log m) := by
      rw [Real.rpow_def_of_pos hmpos]; ring_nf
    rw [h5]
    have : Real.exp (Real.log 2) ≤ Real.exp (d * Real.log m) :=
      Real.exp_le_exp.mpr h1.le
    rwa [Real.exp_log (by norm_num)] at this
  obtain ⟨h1, h2, h3, h4⟩ := lattice_error d hd hd4 m hm2 hx
  refine ⟨m, ⌊(m : ℝ) ^ d⌋₊, hm2, h1, h2, ?_⟩
  rw [abs_sub_comm, abs_of_nonneg h3]
  linarith

#print axioms lattice_error
#print axioms lattice_dense
