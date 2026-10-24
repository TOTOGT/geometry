import Mathlib

/-!
# ChEAudit.lean - companion to the 2026-10-24 audit of chE-gtct.html (Book 3, Extended Chapter E)

STATUS: UNTESTED. Written without a local Lean toolchain; run `lake env lean ChEAudit.lean`
and report the real output before treating any statement here as settled.

What each theorem establishes, and what it does not:

1. `boost_not_contraction` - the Galilean boost (x, v) |-> (x + v, v) is not a contraction
   (Lipschitz constant 1 on the fixed line v = 0). Says nothing about Conjecture 5 beyond
   "a pure boost is not the contraction of Theorem 3".
2. `eig_two_unbounded` - powers of 2 are unbounded: eigenvalue 2 is expanding.
3. `neg_two_decays` - powers of 1/2 tend to 0, i.e. the Book 4 Ch 10 rate mu = -2 for the flow
   corresponds to a per-unit-time factor exp(-2) < 1. Elementary, but it is the sign the page lacked.
4. `G_is_equiv` - a composite of four bijections is a bijection: non-commutativity and
   contraction do not by themselves make G irreversible.
5. `critDim_mono_of_hyp` / `critDim_gt_26_of_hyp` - the page's two lemmas, with the three
   axioms taken as HYPOTHESES on an arbitrary sequence `s`, so nothing is axiomatised.
   They are arithmetic about whatever `s` is. They do NOT say `s` is the 7th term of the
   n-bonacci recurrence (it is not under any convention tried; see chE-audit-verify.py A5).
-/

namespace ChEAudit

/-- Galilean boost on the (x, v) plane. -/
def boost (p : ℝ × ℝ) : ℝ × ℝ := (p.1 + p.2, p.2)

theorem boost_not_contraction :
    ¬ ∃ k : ℝ, k < 1 ∧ ∀ p q : ℝ × ℝ, dist (boost p) (boost q) ≤ k * dist p q := by
  rintro ⟨k, hk, h⟩
  have h1 := h (0, 0) (1, 0)
  have e1 : dist (boost (0, 0)) (boost (1, 0)) = 1 := by
    simp [boost, Prod.dist_eq, Real.dist_eq]
  have e2 : dist ((0 : ℝ), (0 : ℝ)) ((1 : ℝ), (0 : ℝ)) = 1 := by
    simp [Prod.dist_eq, Real.dist_eq]
  rw [e1, e2] at h1
  linarith

theorem eig_two_unbounded : ∀ M : ℝ, ∃ n : ℕ, M < (2 : ℝ) ^ n :=
  fun M => pow_unbounded_of_one_lt M (by norm_num)

theorem neg_two_decays :
    Filter.Tendsto (fun n : ℕ => Real.exp (-2) ^ n) Filter.atTop (nhds 0) :=
  tendsto_pow_atTop_nhds_zero_of_lt_one (Real.exp_pos _).le
    (by rw [Real.exp_lt_one]; norm_num)

/-- G = U ∘ F ∘ K ∘ C of four bijections is a bijection. -/
theorem G_is_equiv {α : Type*} (C K F U : α ≃ α) :
    ∃ H : α ≃ α, (H : α → α) = U ∘ F ∘ K ∘ C :=
  ⟨C.trans (K.trans (F.trans U)), by funext x; rfl⟩

/-- Order matters even for bijections of ℝ: x ↦ x + 1 and x ↦ 2x do not commute. -/
theorem noncomm_example :
    ((fun x : ℝ => 2 * x) ∘ (fun x : ℝ => x + 1)) 0 ≠
    ((fun x : ℝ => x + 1) ∘ (fun x : ℝ => 2 * x)) 0 := by
  norm_num

/-- critDim from a ring-size sequence `s`. -/
def critDim (s : ℕ → ℕ) (n : ℕ) : ℕ := 2 * (s n - 1) + 2

theorem critDim_mono_of_hyp (s : ℕ → ℕ) (h3 : s 3 = 13)
    (hmono : ∀ m n : ℕ, m < n → s m < s n) :
    ∀ m n : ℕ, 3 < m → m < n → critDim s m < critDim s n := by
  intro m n hm hmn
  have h1 := hmono m n hmn
  have h2 := hmono 3 m hm
  unfold critDim
  omega

theorem critDim_gt_26_of_hyp (s : ℕ → ℕ) (h3 : s 3 = 13) (h4 : s 4 = 56)
    (hmono : ∀ m n : ℕ, m < n → s m < s n) :
    ∀ n : ℕ, n > 3 → critDim s n > 26 := by
  intro n hn
  have h1 := hmono 3 n hn
  unfold critDim
  omega

end ChEAudit
