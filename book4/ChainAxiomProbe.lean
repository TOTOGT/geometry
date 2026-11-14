/-
ChainAxiomProbe.lean  (2026-11-14, book4 audit; UNTESTED: written by hand, never run)

Question: are the axioms declared in the registered Chain_updated.lean
(AXLE/NASA/MoonBase/AXLE_lean_files, byte-identical to GTCT/GTCT/GCTC/Operators/Chain.lean)
consistent with the definitions they sit on?

Self-contained: the structures below are copied from GCTC/Operators/{Compress,Threshold,Fold,Unfold}.lean
and Chain.lean, and the axioms and r_star are copied verbatim. Only Mathlib is imported.

Expected if the hand derivation is right: this file compiles, and BOTH
  inner_basin_axiom_gives_false  and  poincare_axiom_gives_false
are accepted, i.e. each axiom, as stated, proves False. If either theorem fails to compile,
read the error: it may be a proof-script slip here, not evidence that the axiom is consistent.

Run (from anywhere):
  bash ~/Desktop/geometry/tools/leancheck.sh --audit ~/Desktop/geometry/book4/ChainAxiomProbe.lean
The audit WILL report the declared axioms (that is the point of this file).
-/
import Mathlib

namespace GCTC

structure Compressor (X : Type*) [SeminormedAddCommGroup X] where
  apply    : X → X
  ratio    : ℝ
  ratio_lt : ratio < 1
  ratio_nn : 0 ≤ ratio
  lipschitz : ∀ x y : X, ‖apply x - apply y‖ ≤ ratio * ‖x - y‖

structure Thresholder (X : Type*) where
  apply    : X → X
  cutoff   : ℝ
  idem     : ∀ x, apply (apply x) = apply x

structure Folder (X : Type*) [MetricSpace X] where
  apply     : X → X
  attractor : X
  contracts : ∀ x : X, dist (apply x) attractor < dist x attractor ∨
                        x = attractor

structure Unfolder (X : Type*) [MetricSpace X] where
  apply  : X → X
  seed   : X
  expands : ∀ x : X, dist (apply x) seed > dist x seed ∨ x = seed

structure GChain (X : Type*) [MetricSpace X] [SeminormedAddCommGroup X] where
  C : Compressor X
  K : Thresholder X
  F : Folder    X
  U : Unfolder  X

def GChain.apply {X : Type*} [MetricSpace X] [SeminormedAddCommGroup X]
    (G : GChain X) (x : X) : X :=
  G.U.apply (G.F.apply (G.K.apply (G.C.apply x)))

def GChain.iter {X : Type*} [MetricSpace X] [SeminormedAddCommGroup X]
    (G : GChain X) (n : ℕ) (x : X) : X :=
  G.apply^[n] x

@[simp] lemma GChain.iter_zero {X} [MetricSpace X] [SeminormedAddCommGroup X]
    (G : GChain X) (x : X) : G.iter 0 x = x := rfl

@[simp] lemma GChain.iter_succ {X} [MetricSpace X] [SeminormedAddCommGroup X]
    (G : GChain X) (n : ℕ) (x : X) : G.iter (n + 1) x = G.apply (G.iter n x) := by
  simp only [GChain.iter, Function.iterate_succ', Function.comp_apply]

inductive GSeries : Type
  | g0  : GSeries
  | g2  : GSeries
  | g6  : GSeries
  | g33 : GSeries
  | g64 : GSeries

def GSeries.cycles : GSeries → ℕ
  | .g0  => 0
  | .g2  => 2
  | .g6  => 6
  | .g33 => 33
  | .g64 => 64

-- copied verbatim from Chain_updated.lean --------------------------------------------------
noncomputable def r_star : ℝ := 0.8
lemma r_star_lt_one : r_star < 1 := by unfold r_star; norm_num
lemma r_star_pos : 0 < r_star := by unfold r_star; norm_num

axiom inner_basin_is_asymmetric :
  ∀ (r₀ : ℝ), r₀ < r_star → ∃ (T : ℝ), 0 < T ∧
    ∀ (z : ℝ → ℝ), (∀ t, 0 ≤ t → z t < 0) →
    ¬ (∀ t, 0 ≤ t → t < T → True)

axiom outer_basin_unbounded :
  ∀ (M : ℝ), ∃ (r₀ : ℝ), M < r₀ ∧ True

axiom poincare_collatz
    {X : Type*} [MetricSpace X] [SeminormedAddCommGroup X]
    (G : GChain X) (x : X) :
    ∃ n : ℕ, n ≥ GSeries.cycles .g33 ∧
      dist (G.iter n x) (G.iter (n + 1) x) < r_star
-- end of verbatim copy ---------------------------------------------------------------------

/-- Hand derivation: r₀ = 0 < r_star and z ≡ -1 satisfy the hypotheses, and the conclusion
    negates a statement that holds for every T. -/
theorem inner_basin_axiom_gives_false : False := by
  obtain ⟨T, _, h⟩ := inner_basin_is_asymmetric 0 r_star_pos
  exact h (fun _ => -1) (fun t _ => by norm_num) (fun _ _ _ => trivial)

/-- outer_basin_unbounded is true, so declaring it an axiom is unnecessary (it is provable). -/
theorem outer_basin_is_provable : ∀ (M : ℝ), ∃ (r₀ : ℝ), M < r₀ ∧ True :=
  fun M => ⟨M + 1, by linarith, trivial⟩

-- A GChain on ℝ whose composite is x ↦ 2x: C halves, K is the identity, F halves toward 0,
-- U multiplies by 8 away from 0. Every structure field below is satisfied.
noncomputable def halfC : Compressor ℝ where
  apply := fun x => x / 2
  ratio := 1 / 2
  ratio_lt := by norm_num
  ratio_nn := by norm_num
  lipschitz := by
    intro x y
    show ‖x / 2 - y / 2‖ ≤ 1 / 2 * ‖x - y‖
    have h : x / 2 - y / 2 = (x - y) / 2 := by ring
    rw [h, Real.norm_eq_abs, Real.norm_eq_abs, abs_div, abs_of_pos (by norm_num : (0:ℝ) < 2)]
    linarith

def idK : Thresholder ℝ where
  apply := fun x => x
  cutoff := 0
  idem := fun _ => rfl

noncomputable def halfF : Folder ℝ where
  apply := fun x => x / 2
  attractor := 0
  contracts := by
    intro x
    by_cases hx : x = 0
    · exact Or.inr hx
    · left
      show dist (x / 2) 0 < dist x 0
      have hpos : 0 < |x| := abs_pos.mpr hx
      rw [Real.dist_eq, Real.dist_eq, sub_zero, sub_zero, abs_div,
        abs_of_pos (by norm_num : (0:ℝ) < 2)]
      linarith

def eightU : Unfolder ℝ where
  apply := fun x => 8 * x
  seed := 0
  expands := by
    intro x
    by_cases hx : x = 0
    · exact Or.inr hx
    · left
      show dist (8 * x) 0 > dist x 0
      have hpos : 0 < |x| := abs_pos.mpr hx
      rw [gt_iff_lt, Real.dist_eq, Real.dist_eq, sub_zero, sub_zero, abs_mul,
        abs_of_pos (by norm_num : (0:ℝ) < 8)]
      linarith

noncomputable def Gdouble : GChain ℝ := ⟨halfC, idK, halfF, eightU⟩

theorem Gdouble_apply (x : ℝ) : Gdouble.apply x = 2 * x := by
  show 8 * (x / 2 / 2) = 2 * x
  ring

theorem Gdouble_iter (n : ℕ) : Gdouble.iter n 1 = 2 ^ n := by
  induction n with
  | zero => simp
  | succ n ih => rw [GChain.iter_succ, ih, Gdouble_apply]; ring

/-- Hand derivation: along Gdouble from x = 1 the consecutive distance is 2^n ≥ 1 > r_star. -/
theorem poincare_axiom_gives_false : False := by
  obtain ⟨n, _, h⟩ := poincare_collatz Gdouble (1 : ℝ)
  rw [Gdouble_iter n, Gdouble_iter (n + 1), Real.dist_eq] at h
  have h2 : (1 : ℝ) ≤ 2 ^ n := by exact_mod_cast Nat.one_le_two_pow
  have e : (2 : ℝ) ^ n - 2 ^ (n + 1) = -(2 ^ n) := by ring
  rw [e, abs_neg, abs_of_pos (by linarith)] at h
  linarith [r_star_lt_one]

#print axioms inner_basin_axiom_gives_false
#print axioms poincare_axiom_gives_false
#print axioms outer_basin_is_provable

end GCTC
