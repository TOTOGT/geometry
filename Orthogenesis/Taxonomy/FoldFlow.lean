-- GATE-DECLARE: sorries = none
-- GATE-REASON: motion in time for the scalar fold W = q⁴/4 − 3q²/2 + a·q: global exponential convergence above the fold, and a solution started at the fold point at a = 2 stays there.
/-
Orthogenesis/Taxonomy/FoldFlow.lean — gradient flow q' = −dW/dq on the fold, as TRAJECTORY statements.

Written 2026-11-08 without a Lean toolchain; every lemma name was read from the pinned Mathlib
(rev 81a5d257c8, Lean v4.32.0). Compiled on the author's Mac the same day with `lake env lean`: no errors,
all six #print axioms report only [propext, Classical.choice, Quot.sound]. (One unused-tactic note on a
`beta_reduce`, since removed; that edit is not re-run.)

Setting. f(q) = q³ − 3q + a = dW/dq. A "solution" is a function q : ℝ → ℝ with
  hq : ∀ t, 0 ≤ t → HasDerivAt q (−f(q t)) t.
Existence of a solution is NOT proved here; both theorems are about any function that is one.

T1 (a > 2). f has exactly one real root qs, and qs < −2. For every solution,
  |q t − qs| ≤ |q 0 − qs| · exp(−c t),   c = 3(qs² − 4)/4 > 0,   and q t → qs.
Proof: f(q) = (q − qs)·g(q), g(q) = q² + qs·q + qs² − 3 ≥ c; V(t) = e^{2ct}(q t − qs)² has V' ≤ 0.
CAUTION on c: c → 0 as a → 2⁺ (qs → −2). That is an artefact of one global constant. The true local
rate at qs is f'(qs) = 3qs² − 3 → 9. The slow passage near q = 1 (the ghost of the fold) is not
captured by this bound and is NOT proved here (it is target T3, a lower bound on passage time).

T2 (a = 2). If q 0 = 1 then q t = 1 for all t ≥ 0. Proof by the Gronwall inequality in Mathlib on
y = q − 1, y' = −y²(y + 3), with the Lipschitz-type bound |y'| ≤ M(M+3)|y| on the compact [0, T].
No uniqueness theorem for ODEs is used. Control: q ≡ 1 is a solution (`const_one_is_solution`),
so the hypothesis is satisfiable and the theorem is not vacuous.

NOT proved: existence of solutions; T3 (passage-time lower bound π/(2√(3ε)) as ε = a−2 → 0⁺);
T4 (a < 2, convergence to the right branch from q 0 ≥ 1); any statement for a < 2 other than none;
that 1/W'' is a relaxation time at a < 2 (T1 is at a > 2, a different regime).
-/
import Mathlib

namespace Orthogenesis.Taxonomy.FoldFlow

open Set Filter Topology Real

/-- `f(q) = q³ − 3q + a`, the derivative of the double-well potential in `q`. -/
def foldF (a q : ℝ) : ℝ := q ^ 3 - 3 * q + a

/-! ## T1  above the fold -/

/-- For `a > 2` there is a real root `qs < -2` of `foldF a`. -/
theorem root_exists {a : ℝ} (ha : 2 < a) : ∃ qs : ℝ, qs < -2 ∧ foldF a qs = 0 := by
  have hcont : ContinuousOn (foldF a) (Icc (-(a + 2)) (-2)) := by
    have : Continuous (foldF a) := by unfold foldF; fun_prop
    exact this.continuousOn
  have hle : -(a + 2) ≤ (-2 : ℝ) := by linarith
  have hlo : foldF a (-(a + 2)) < 0 := by
    have h1 : 0 < (a + 2) ^ 2 - 4 := by nlinarith
    have h2 := mul_pos (show (0 : ℝ) < a + 2 by linarith) h1
    unfold foldF
    nlinarith [h2]
  have hhi : 0 < foldF a (-2) := by unfold foldF; nlinarith
  obtain ⟨qs, ⟨_, hqs2⟩, hz⟩ :=
    intermediate_value_Icc hle hcont
      (show (0 : ℝ) ∈ Icc (foldF a (-(a + 2))) (foldF a (-2)) from ⟨hlo.le, hhi.le⟩)
  refine ⟨qs, lt_of_le_of_ne hqs2 ?_, hz⟩
  rintro rfl
  exact absurd hz hhi.ne'

/-- Factorisation through a root. -/
theorem foldF_factor {a qs : ℝ} (h : foldF a qs = 0) (q : ℝ) :
    foldF a q = (q - qs) * (q ^ 2 + q * qs + qs ^ 2 - 3) := by
  unfold foldF at h ⊢
  linear_combination h

/-- The cofactor is bounded below by a positive constant when `qs < -2`. -/
theorem cofactor_lower {qs : ℝ} (q : ℝ) :
    3 * (qs ^ 2 - 4) / 4 ≤ q ^ 2 + q * qs + qs ^ 2 - 3 := by
  nlinarith [sq_nonneg (q + qs / 2)]

theorem rate_pos {qs : ℝ} (h : qs < -2) : 0 < 3 * (qs ^ 2 - 4) / 4 := by
  nlinarith [mul_pos (show (0 : ℝ) < -2 - qs by linarith) (show (0 : ℝ) < 2 - qs by linarith)]

/-- The root is unique. -/
theorem root_unique {a qs : ℝ} (hqs : qs < -2) (h : foldF a qs = 0) {r : ℝ}
    (hr : foldF a r = 0) : r = qs := by
  have hfac := foldF_factor h r
  have hpos : 0 < r ^ 2 + r * qs + qs ^ 2 - 3 :=
    lt_of_lt_of_le (rate_pos hqs) (cofactor_lower r)
  rw [hr] at hfac
  have : (r - qs) * (r ^ 2 + r * qs + qs ^ 2 - 3) = 0 := hfac.symm
  rcases mul_eq_zero.1 this with h1 | h1
  · linarith
  · linarith

/-- Core estimate: along any solution, `exp(2ct)·(q t − qs)²` does not increase. -/
theorem lyapunov_antitone {a qs : ℝ} (_hqs : qs < -2) (h : foldF a qs = 0) {q : ℝ → ℝ}
    (hq : ∀ t, 0 ≤ t → HasDerivAt q (-(foldF a (q t))) t) :
    ∀ t, 0 ≤ t →
      Real.exp (2 * (3 * (qs ^ 2 - 4) / 4) * t) * ((q t - qs) * (q t - qs))
        ≤ (q 0 - qs) * (q 0 - qs) := by
  set c : ℝ := 3 * (qs ^ 2 - 4) / 4 with hc
  set V : ℝ → ℝ := fun t => Real.exp (2 * c * t) * ((q t - qs) * (q t - qs)) with hV
  have hv : ∀ t, 0 ≤ t → HasDerivAt V
      (Real.exp (2 * c * t) * (2 * c) * ((q t - qs) * (q t - qs))
        + Real.exp (2 * c * t) *
          (-(foldF a (q t)) * (q t - qs) + (q t - qs) * (-(foldF a (q t))))) t := by
    intro t ht
    have hu : HasDerivAt (fun s => (q s - qs) * (q s - qs))
        (-(foldF a (q t)) * (q t - qs) + (q t - qs) * (-(foldF a (q t)))) t :=
      ((hq t ht).sub_const qs).mul ((hq t ht).sub_const qs)
    have h1 : HasDerivAt (fun s => Real.exp (2 * c * s)) (Real.exp (2 * c * t) * (2 * c)) t := by
      have := ((hasDerivAt_id' t).const_mul (2 * c)).exp
      exact this.congr_deriv (by ring)
    exact h1.mul hu
  have hnonpos : ∀ t, 0 ≤ t →
      Real.exp (2 * c * t) * (2 * c) * ((q t - qs) * (q t - qs))
        + Real.exp (2 * c * t) *
          (-(foldF a (q t)) * (q t - qs) + (q t - qs) * (-(foldF a (q t)))) ≤ 0 := by
    intro t _
    have hfac := foldF_factor h (q t)
    have hg := cofactor_lower (qs := qs) (q t)
    have key : 2 * c * ((q t - qs) * (q t - qs))
        + (-(foldF a (q t)) * (q t - qs) + (q t - qs) * (-(foldF a (q t)))) ≤ 0 := by
      rw [hfac]
      nlinarith [mul_nonneg (mul_self_nonneg (q t - qs)) (sub_nonneg.2 hg)]
    have : Real.exp (2 * c * t) * (2 * c) * ((q t - qs) * (q t - qs))
        + Real.exp (2 * c * t) *
          (-(foldF a (q t)) * (q t - qs) + (q t - qs) * (-(foldF a (q t))))
        = Real.exp (2 * c * t) *
          (2 * c * ((q t - qs) * (q t - qs))
            + (-(foldF a (q t)) * (q t - qs) + (q t - qs) * (-(foldF a (q t))))) := by ring
    rw [this]
    exact mul_nonpos_iff.2 (Or.inl ⟨(Real.exp_pos _).le, key⟩)
  have hcont : ContinuousOn V (Ici 0) := fun t ht =>
    (hv t ht).continuousAt.continuousWithinAt
  have hdiff : DifferentiableOn ℝ V (interior (Ici (0 : ℝ))) := by
    intro t ht
    rw [interior_Ici] at ht
    exact (hv t (le_of_lt ht)).differentiableAt.differentiableWithinAt
  have hder : ∀ t ∈ interior (Ici (0 : ℝ)), deriv V t ≤ 0 := by
    intro t ht
    rw [interior_Ici] at ht
    rw [(hv t (le_of_lt ht)).deriv]
    exact hnonpos t (le_of_lt ht)
  have hanti := antitoneOn_of_deriv_nonpos (convex_Ici 0) hcont hdiff hder
  intro t ht
  have h2 := hanti (Set.mem_Ici.2 le_rfl) (Set.mem_Ici.2 ht) ht
  simp only [hV, mul_zero, Real.exp_zero, one_mul] at h2
  exact h2

/-- **T1.** Above the fold (`a > 2`) the flow has a unique equilibrium `qs < -2`, and every solution
converges to it exponentially, at the rate `c = 3(qs² − 4)/4`. -/
theorem flow_converges_above_fold {a : ℝ} (ha : 2 < a) :
    ∃ qs : ℝ, qs < -2 ∧ foldF a qs = 0 ∧ (∀ r, foldF a r = 0 → r = qs) ∧
      ∀ q : ℝ → ℝ, (∀ t, 0 ≤ t → HasDerivAt q (-(foldF a (q t))) t) →
        (∀ t, 0 ≤ t →
          |q t - qs| ≤ |q 0 - qs| * Real.exp (-(3 * (qs ^ 2 - 4) / 4 * t))) ∧
        Tendsto q atTop (𝓝 qs) := by
  obtain ⟨qs, hqs, hz⟩ := root_exists ha
  refine ⟨qs, hqs, hz, fun r hr => root_unique hqs hz hr, ?_⟩
  intro q hq
  set c : ℝ := 3 * (qs ^ 2 - 4) / 4 with hc
  have hcpos : 0 < c := rate_pos hqs
  have hbound : ∀ t, 0 ≤ t → |q t - qs| ≤ |q 0 - qs| * Real.exp (-(c * t)) := by
    intro t ht
    have hV := lyapunov_antitone hqs hz hq t ht
    have e1 : Real.exp (-(2 * c * t)) * Real.exp (2 * c * t) = 1 := by
      rw [← Real.exp_add]; simp
    have hu : (q t - qs) * (q t - qs)
        ≤ Real.exp (-(2 * c * t)) * ((q 0 - qs) * (q 0 - qs)) := by
      calc (q t - qs) * (q t - qs)
          = (Real.exp (-(2 * c * t)) * Real.exp (2 * c * t)) * ((q t - qs) * (q t - qs)) := by
            rw [e1, one_mul]
        _ = Real.exp (-(2 * c * t)) *
              (Real.exp (2 * c * t) * ((q t - qs) * (q t - qs))) := by ring
        _ ≤ Real.exp (-(2 * c * t)) * ((q 0 - qs) * (q 0 - qs)) :=
            mul_le_mul_of_nonneg_left hV (Real.exp_pos _).le
    have e2 : Real.exp (-(c * t)) ^ 2 = Real.exp (-(2 * c * t)) := by
      rw [sq, ← Real.exp_add]; congr 1; ring
    have hsq : (q t - qs) ^ 2 ≤ (|q 0 - qs| * Real.exp (-(c * t))) ^ 2 := by
      rw [mul_pow, sq_abs, e2]
      nlinarith [hu]
    have hnn : 0 ≤ |q 0 - qs| * Real.exp (-(c * t)) :=
      mul_nonneg (abs_nonneg _) (Real.exp_pos _).le
    exact abs_le.2 (abs_le_of_sq_le_sq' hsq hnn)
  refine ⟨hbound, ?_⟩
  have hexp : Tendsto (fun t : ℝ => Real.exp (-(c * t))) atTop (𝓝 0) :=
    Real.tendsto_exp_neg_atTop_nhds_zero.comp (tendsto_id.const_mul_atTop hcpos)
  have hK : Tendsto (fun t : ℝ => |q 0 - qs| * Real.exp (-(c * t))) atTop (𝓝 0) := by
    simpa using hexp.const_mul (|q 0 - qs|)
  have h0 : Tendsto (fun t => q t - qs) atTop (𝓝 0) := by
    refine squeeze_zero_norm' ?_ hK
    filter_upwards [eventually_ge_atTop (0 : ℝ)] with t ht
    rw [Real.norm_eq_abs]
    exact hbound t ht
  exact tendsto_sub_nhds_zero_iff.1 h0

/-! ## T2  at the fold, a = 2 -/

/-- At `a = 2`: `f(q) = (q − 1)²(q + 2)`. -/
theorem foldF_two (q : ℝ) : foldF 2 q = (q - 1) ^ 2 * (q + 2) := by
  unfold foldF; ring

/-- Control: the constant function `1` is a solution at `a = 2`, so T2 is not vacuous. -/
theorem const_one_is_solution :
    ∀ t : ℝ, 0 ≤ t → HasDerivAt (fun _ : ℝ => (1 : ℝ)) (-(foldF 2 ((fun _ : ℝ => (1 : ℝ)) t))) t := by
  intro t _
  have : -(foldF 2 ((fun _ : ℝ => (1 : ℝ)) t)) = 0 := by
    norm_num [foldF]
  rw [this]
  exact hasDerivAt_const t 1

/-- **T2.** At `a = 2`, a solution that starts at the fold point `q = 1` stays there for all `t ≥ 0`. -/
theorem flow_fixed_at_fold {q : ℝ → ℝ}
    (hq : ∀ t, 0 ≤ t → HasDerivAt q (-(foldF 2 (q t))) t) (h0 : q 0 = 1) :
    ∀ t, 0 ≤ t → q t = 1 := by
  intro T hT
  have hcont : ContinuousOn (fun s => q s - 1) (Icc 0 T) := fun s hs =>
    ((hq s hs.1).continuousAt.sub continuousAt_const).continuousWithinAt
  obtain ⟨M, hM⟩ := isCompact_Icc.exists_bound_of_continuousOn hcont
  have hM0 : 0 ≤ M := le_trans (norm_nonneg _) (hM 0 ⟨le_rfl, hT⟩)
  have key := norm_le_gronwallBound_of_norm_deriv_right_le
    (f := fun s => q s - 1) (f' := fun s => -(foldF 2 (q s))) (δ := 0) (K := M * (M + 3)) (ε := 0)
    (a := 0) (b := T) hcont
    (fun x hx => ((hq x hx.1).sub_const 1).hasDerivWithinAt)
    (by simp [h0])
    (by
      intro x hx
      have hxI : x ∈ Icc 0 T := ⟨hx.1, hx.2.le⟩
      have hy : |q x - 1| ≤ M := by simpa [Real.norm_eq_abs] using hM x hxI
      have h3 : |q x - 1 + 3| ≤ M + 3 := by
        calc |q x - 1 + 3| ≤ |q x - 1| + |(3 : ℝ)| := abs_add_le _ _
          _ ≤ M + 3 := by norm_num; linarith
      have hf : foldF 2 (q x) = (q x - 1) ^ 2 * (q x - 1 + 3) := by
        rw [foldF_two]; ring
      rw [Real.norm_eq_abs, Real.norm_eq_abs, abs_neg, hf, abs_mul, abs_pow]
      have e : |q x - 1| ^ 2 * |q x - 1 + 3| = |q x - 1| * (|q x - 1| * |q x - 1 + 3|) := by ring
      rw [e]
      have : |q x - 1| * |q x - 1 + 3| ≤ M * (M + 3) :=
        mul_le_mul hy h3 (abs_nonneg _) hM0
      nlinarith [mul_nonneg (abs_nonneg (q x - 1)) (sub_nonneg.2 this)])
  have := key T ⟨hT, le_rfl⟩
  rw [gronwallBound_ε0_δ0, Real.norm_eq_abs] at this
  have h := abs_nonneg (q T - 1)
  have : |q T - 1| = 0 := le_antisymm this h
  linarith [abs_eq_zero.1 this]

#print axioms Orthogenesis.Taxonomy.FoldFlow.root_exists
#print axioms Orthogenesis.Taxonomy.FoldFlow.root_unique
#print axioms Orthogenesis.Taxonomy.FoldFlow.lyapunov_antitone
#print axioms Orthogenesis.Taxonomy.FoldFlow.flow_converges_above_fold
#print axioms Orthogenesis.Taxonomy.FoldFlow.const_one_is_solution
#print axioms Orthogenesis.Taxonomy.FoldFlow.flow_fixed_at_fold

end Orthogenesis.Taxonomy.FoldFlow
