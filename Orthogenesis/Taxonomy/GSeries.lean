-- GATE-DECLARE: sorries = none
-- GATE-REASON: g-series taxonomy. Ordinal skeleton and cycle classification proved; the index-33 claim is a named Prop, never a sorry; two GCTC Chain.lean axioms refuted.
/-
Orthogenesis/Taxonomy/GSeries.lean — the g-series regime taxonomy, stated honestly.

Sources: GTCT-2026-001 Definitions 2.1–2.2 and Remarks 2.3–2.4; GCTC.Operators.Chain
(GTCT/GTCT/GCTC/Operators/Chain.lean, "UPDATED 2026-04-25").

What is proved here:
  §1  Five labels, an injective index map (0,2,6,33,64), strictly increasing.
  §2  A total classification ℕ → GRegime (cycle count ↦ highest regime reached), reading the
      indices as cycle thresholds, as GCTC's `GSeries.cycles` does. Partition, maximality and
      monotonicity are proved.
  §3  The arithmetic behind the labels: ⌈log₂(3!)·4⌉ = 11, 3·11 = 33, 2^6 = 64. Arithmetic only.
      Remark 2.3 calls 33 a heuristic, and nothing here makes it more than one.
  §4  In GCTC, the contracting-case theorem holds with 33 replaced by any N. The 33 is decorative.
  §5  GCTC `poincare_collatz` (general, axiom) is false: a counterexample chain on ℝ, U∘F∘K∘C = (x ↦ 2x).
  §6  GCTC `inner_basin_is_asymmetric` (axiom) is false for every input: its conclusion negates a
      tautology.
  §7  The index-33 claim as a named Prop about a given system. It holds for some systems and fails
      for others, so it is neither vacuous nor a theorem.

What is NOT formalised: the Definition 2.2 criteria ("two-operator closure, F active",
"limit cycle Γ entered", …). They need C, K, F, U as operators on a defined state space,
and no such objects exist yet. The criteria stay prose, in the constructor docstrings.

On ℝ, GCTC's `dist` and `‖·‖` are both |x - y|. §4–§6 use that form directly.
-/
import Mathlib
import Orthogenesis.Matrix.CajueiroPrinciple

namespace Orthogenesis.GSeries

/-! ## §1  Labels and ordinal index -/

/-- GTCT Definition 2.1: ordinal regime labels g0 < g2 < g6 < g33 < g64. -/
inductive GRegime
  /-- Seed: a single operator application. -/
  | g0
  /-- Compositional: two-operator closure, F active. -/
  | g2
  /-- Cycle-scale: full G-cycle closure, limit cycle Γ entered. -/
  | g6
  /-- Soft equilibrium: heuristic index ⌈log₂(3!)·4⌉·3 = 33 (Remark 2.3: conjecture). -/
  | g33
  /-- Phase threshold: 2^6 = 64 operator-state combinations. -/
  | g64
  deriving DecidableEq, Repr

def GRegime.index : GRegime → ℕ
  | .g0 => 0
  | .g2 => 2
  | .g6 => 6
  | .g33 => 33
  | .g64 => 64

theorem index_injective : Function.Injective GRegime.index := by
  intro a b h
  cases a <;> cases b <;> first | rfl | exact absurd h (by decide)

theorem index_chain :
    GRegime.g0.index < GRegime.g2.index ∧ GRegime.g2.index < GRegime.g6.index ∧
    GRegime.g6.index < GRegime.g33.index ∧ GRegime.g33.index < GRegime.g64.index := by
  decide

/-! ## §2  Classification of cycle counts -/

/-- Highest regime whose index does not exceed `n`. -/
def regimeOf (n : ℕ) : GRegime :=
  if 64 ≤ n then .g64 else if 33 ≤ n then .g33 else if 6 ≤ n then .g6
  else if 2 ≤ n then .g2 else .g0

theorem regimeOf_index (r : GRegime) : regimeOf r.index = r := by
  cases r <;> decide

theorem index_regimeOf_le (n : ℕ) : (regimeOf n).index ≤ n := by
  unfold regimeOf
  split_ifs <;> simp only [GRegime.index] <;> omega

theorem regimeOf_maximal (n : ℕ) (r : GRegime) (h : r.index ≤ n) :
    r.index ≤ (regimeOf n).index := by
  cases r <;> unfold regimeOf <;> split_ifs <;> simp only [GRegime.index] at * <;> omega

theorem regimeOf_mono {m n : ℕ} (h : m ≤ n) : (regimeOf m).index ≤ (regimeOf n).index :=
  regimeOf_maximal n _ (le_trans (index_regimeOf_le m) h)

/-- Partition: every cycle count lands in exactly one regime, characterised by
    "index reached, and no higher index reached". -/
theorem regimeOf_eq_iff (n : ℕ) (r : GRegime) :
    regimeOf n = r ↔ r.index ≤ n ∧ ∀ s : GRegime, s.index ≤ n → s.index ≤ r.index := by
  constructor
  · rintro rfl
    exact ⟨index_regimeOf_le n, fun s hs => regimeOf_maximal n s hs⟩
  · rintro ⟨h1, h2⟩
    apply index_injective
    exact le_antisymm (h2 _ (index_regimeOf_le n)) (regimeOf_maximal n r h1)

/-! ## §3  Arithmetic of the labels -/

theorem g33_arith : ⌈Real.logb 2 ((Nat.factorial 3 : ℕ) : ℝ) * 4⌉₊ * 3 = 33 := by
  have h : ((Nat.factorial 3 : ℕ) : ℝ) = 6 := by norm_num [Nat.factorial]
  rw [h, Orthogenesis.CajueiroPrinciple.nmin_eq_eleven]

theorem g64_arith : 2 ^ 6 = 64 := by norm_num

/-! ## §4  The contracting case does not single out 33 -/

lemma step_bound (f : ℝ → ℝ) (k : ℝ) (hk0 : 0 ≤ k)
    (hf : ∀ a b, |f a - f b| ≤ k * |a - b|) (x : ℝ) (n : ℕ) :
    |f^[n] x - f^[n + 1] x| ≤ k ^ n * |x - f x| := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [Function.iterate_succ_apply' f n x, Function.iterate_succ_apply' f (n + 1) x]
    calc |f (f^[n] x) - f (f^[n + 1] x)| ≤ k * |f^[n] x - f^[n + 1] x| := hf _ _
      _ ≤ k * (k ^ n * |x - f x|) := mul_le_mul_of_nonneg_left ih hk0
      _ = k ^ (n + 1) * |x - f x| := by ring

/-- GCTC `poincare_collatz_contracting`, with 33 replaced by an arbitrary `N` and 0.8 by an
    arbitrary `ε > 0`. It is the same theorem for every threshold, so it gives 33 no role. -/
theorem contracting_any_threshold (f : ℝ → ℝ) (k : ℝ) (hk0 : 0 ≤ k) (hk1 : k < 1)
    (hf : ∀ a b, |f a - f b| ≤ k * |a - b|) (x ε : ℝ) (hε : 0 < ε) (N : ℕ) :
    ∃ n, N ≤ n ∧ |f^[n] x - f^[n + 1] x| < ε := by
  by_cases hd : |x - f x| = 0
  · refine ⟨N, le_refl _, ?_⟩
    have hb := step_bound f k hk0 hf x N
    rw [hd, mul_zero] at hb
    linarith
  · have hd_pos : 0 < |x - f x| := lt_of_le_of_ne (abs_nonneg _) (Ne.symm hd)
    obtain ⟨M, hM⟩ := exists_pow_lt_of_lt_one (div_pos hε hd_pos) hk1
    refine ⟨max N M, le_max_left _ _, ?_⟩
    have hle : k ^ (max N M) ≤ k ^ M := pow_le_pow_of_le_one hk0 hk1.le (le_max_right _ _)
    calc |f^[max N M] x - f^[max N M + 1] x| ≤ k ^ (max N M) * |x - f x| :=
          step_bound f k hk0 hf x _
      _ ≤ k ^ M * |x - f x| := mul_le_mul_of_nonneg_right hle (abs_nonneg _)
      _ < ε / |x - f x| * |x - f x| := mul_lt_mul_of_pos_right hM hd_pos
      _ = ε := by field_simp

/-! ## §5  GCTC `poincare_collatz` (general) is false -/

/-- GCTC `Compressor` fields on ℝ. -/
def IsCompressor (f : ℝ → ℝ) : Prop :=
  ∃ k : ℝ, k < 1 ∧ 0 ≤ k ∧ ∀ x y, |f x - f y| ≤ k * |x - y|
/-- GCTC `Thresholder` field (idempotence). -/
def IsThresholder (f : ℝ → ℝ) : Prop := ∀ x, f (f x) = f x
/-- GCTC `Folder` field. -/
def IsFolder (f : ℝ → ℝ) : Prop := ∃ a : ℝ, ∀ x, |f x - a| < |x - a| ∨ x = a
/-- GCTC `Unfolder` field. -/
def IsUnfolder (f : ℝ → ℝ) : Prop := ∃ s : ℝ, ∀ x, |f x - s| > |x - s| ∨ x = s

/-- Body of GCTC `axiom poincare_collatz`, with GCTC's r_star = 0.8. -/
def PoincareCollatzGeneral : Prop :=
  ∀ C K F U : ℝ → ℝ, IsCompressor C → IsThresholder K → IsFolder F → IsUnfolder U →
    ∀ x : ℝ, ∃ n : ℕ, 33 ≤ n ∧ |(U ∘ F ∘ K ∘ C)^[n] x - (U ∘ F ∘ K ∘ C)^[n + 1] x| < 0.8

lemma iter_double (n : ℕ) : (fun x : ℝ => 2 * x)^[n] 1 = 2 ^ n := by
  induction n with
  | zero => simp
  | succ n ih => rw [Function.iterate_succ_apply', ih, pow_succ]; ring

lemma double_step_large (n : ℕ) :
    ¬ |(fun x : ℝ => 2 * x)^[n] 1 - (fun x : ℝ => 2 * x)^[n + 1] 1| < 0.8 := by
  rw [iter_double, iter_double]
  have h1 : (1 : ℝ) ≤ 2 ^ n := one_le_pow₀ (by norm_num)
  rw [show (2 : ℝ) ^ n - 2 ^ (n + 1) = -(2 ^ n) by ring, abs_neg,
    abs_of_pos (by positivity : (0 : ℝ) < 2 ^ n)]
  have h08 : (0.8 : ℝ) < 1 := by norm_num
  intro hlt
  linarith

theorem poincareCollatzGeneral_false : ¬ PoincareCollatzGeneral := by
  intro h
  have hC : IsCompressor (fun x => x / 2) :=
    ⟨1 / 2, by norm_num, by norm_num, fun x y => le_of_eq (by
      rw [show x / 2 - y / 2 = (1 / 2) * (x - y) by ring, abs_mul,
        abs_of_pos (by norm_num : (0 : ℝ) < 1 / 2)])⟩
  have hK : IsThresholder id := fun _ => rfl
  have hF : IsFolder (fun x => x / 2) := ⟨0, fun x => by
    by_cases hx : x = 0
    · exact Or.inr hx
    · left
      have hp : 0 < |x| := abs_pos.mpr hx
      rw [sub_zero, sub_zero, abs_div, abs_two]
      linarith⟩
  have hU : IsUnfolder (fun x => 8 * x) := ⟨0, fun x => by
    by_cases hx : x = 0
    · exact Or.inr hx
    · left
      have hp : 0 < |x| := abs_pos.mpr hx
      rw [sub_zero, sub_zero, abs_mul, abs_of_pos (by norm_num : (0 : ℝ) < 8)]
      linarith⟩
  obtain ⟨n, -, hn⟩ := h _ _ _ _ hC hK hF hU 1
  have hG : ((fun x : ℝ => 8 * x) ∘ (fun x : ℝ => x / 2) ∘ id ∘ (fun x : ℝ => x / 2))
      = fun x : ℝ => 2 * x := by
    funext x
    simp only [Function.comp_apply, id_eq]
    ring
  rw [hG] at hn
  exact double_step_large n hn

/-! ## §6  GCTC `inner_basin_is_asymmetric` is false -/

/-- Body of GCTC `axiom inner_basin_is_asymmetric`, with r_star = 0.8. -/
def InnerBasinAxiom : Prop :=
  ∀ r₀ : ℝ, r₀ < 0.8 → ∃ T : ℝ, 0 < T ∧
    ∀ z : ℝ → ℝ, (∀ t, 0 ≤ t → z t < 0) → ¬ (∀ t, 0 ≤ t → t < T → True)

theorem innerBasinAxiom_false : ¬ InnerBasinAxiom := by
  intro h
  obtain ⟨T, -, hT⟩ := h 0 (by norm_num)
  exact hT (fun _ => -1) (fun _ _ => by norm_num) (fun _ _ _ => trivial)

/-! ## §7  The index-33 claim, stated and not proved -/

/-- The index-33 claim for a given discrete system `f`, start `x` and basin radius `r`:
    from cycle 33 on, every consecutive step stays inside `r`. The author uses 33 (and 64)
    as teaching indices, not derived values (2026-09-25). This Prop is the template for
    anyone who claims 33 for a specific system; no such system is formalised here. -/
def Index33Conjecture (f : ℝ → ℝ) (r x : ℝ) : Prop :=
  ∀ n, 33 ≤ n → |f^[n] x - f^[n + 1] x| < r

/-- It holds for some systems … -/
theorem index33_holds_id : Index33Conjecture id 0.8 1 := fun n _ => by
  norm_num [Function.iterate_id]

/-- … and fails for others. So it is not a theorem for every system. -/
theorem index33_fails_double : ¬ Index33Conjecture (fun x => 2 * x) 0.8 1 :=
  fun h => double_step_large 33 (h 33 le_rfl)

end Orthogenesis.GSeries

#print axioms Orthogenesis.GSeries.index_injective
#print axioms Orthogenesis.GSeries.regimeOf_eq_iff
#print axioms Orthogenesis.GSeries.g33_arith
#print axioms Orthogenesis.GSeries.contracting_any_threshold
#print axioms Orthogenesis.GSeries.poincareCollatzGeneral_false
#print axioms Orthogenesis.GSeries.innerBasinAxiom_false
#print axioms Orthogenesis.GSeries.index33_fails_double
