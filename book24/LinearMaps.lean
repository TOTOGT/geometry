import Mathlib

/-
Book XXIV, chapter 5: linear maps. Lean core.

STATUS: first compile by the author (2026-11-04): 6 of 7 theorems clean, no sorryAx. corollaryA failed:
`simp [hk] at h4` made no progress (line 72), so it depended on sorryAx. The fix (prove the kernel's
finrank is 0 with `simp [hk]`, the pattern corollaryB already used, then `omega`) is in the file below
and has NOT been recompiled. linearmaps.axioms.txt still holds the real failing report; do not
overwrite it until the author reruns. To rerun:
  lake env lean book24/LinearMaps.lean 2>&1 | tee book24/linearmaps.axioms.txt

The statements follow Lax, Linear Algebra and Its Applications (2nd ed.), Chapter 3, pp.19-22:
  theorem1a, theorem1b       Theorem 1 (p.20): the image of a subspace is a subspace; the inverse image
                             of a subspace is a subspace
  theorem2                   Theorem 2 (p.20): dim N_T + dim R_T = dim X
  corollaryA                 Corollary A (p.21): dim U < dim X  =>  T x = 0 for some x != 0
  corollaryB                 Corollary B (p.21): dim U = dim X and T x = 0 only for x = 0  =>  R_T = U
  control_corollaryB_needs_trivial_kernel
                             a control: same dimensions, nonzero kernel, and the range is NOT all of U
  interpolation              Application 1 (p.22): n distinct points, any prescribed values are taken by a
                             polynomial of degree less than n

WHAT THESE PROOFS ARE. theorem1a/1b are the definitions of Mathlib's Submodule.map and Submodule.comap;
theorem2 is Mathlib's rank-nullity theorem; corollaryA and corollaryB are derived from theorem2 here, as Lax
derives them; interpolation uses corollary B's idea (injective + equal dimension => surjective) through
Mathlib's lemma. So this file checks that Lax's statements, as formal sentences over any field K, are true.
It does not re-derive his quotient-space proof of Theorem 2.

WHAT IT DOES NOT STATE.
  - Application 2 (averages over disjoint intervals), Application 3 (the Laplace lattice equations), the
    transpose theorems (p.27), similarity (p.29), projections (p.30).
  - The Jacobian as the linear map that best fits a nonlinear one: the page shows it by exact example, and
    the differential is treated in Book XVIII chapter 8, not here.
  - Linear independence and spanning are Mathlib's; the statements are for modules over a field.

NAMES MOST LIKELY TO NEED A FIX AGAINST THE REAL COMPILER (flagged in advance, not known to fail):
  LinearMap.finrank_range_add_finrank_ker, Submodule.exists_mem_ne_zero_of_ne_bot, LinearMap.ker_eq_bot',
  Submodule.eq_top_of_finrank_eq, LinearMap.injective_iff_surjective_of_finrank_eq_finrank,
  Polynomial.degreeLTEquiv, Polynomial.leval, Polynomial.eq_zero_of_natDegree_lt_card_of_eval_eq_zero,
  Polynomial.natDegree_lt_iff_degree_lt, LinearMap.single, and the `simp` steps in the control.

Toolchain: repository pin, leanprover/lean4:v4.32.0 with Mathlib v4.32.0.
-/

namespace Book24LM

variable {K V W : Type*} [Field K] [AddCommGroup V] [Module K V] [AddCommGroup W] [Module K W]

/-- Theorem 1(a): the image of a subspace under a linear map is a subspace. -/
theorem theorem1a (T : V →ₗ[K] W) (S : Submodule K V) :
    ∃ S' : Submodule K W, (S' : Set W) = T '' (S : Set V) :=
  ⟨S.map T, rfl⟩

/-- Theorem 1(b): the inverse image of a subspace is a subspace. -/
theorem theorem1b (T : V →ₗ[K] W) (S' : Submodule K W) :
    ∃ S : Submodule K V, (S : Set V) = T ⁻¹' (S' : Set W) :=
  ⟨S'.comap T, rfl⟩

/-- Theorem 2: dim of the nullspace plus dim of the range is dim of the domain. -/
theorem theorem2 [FiniteDimensional K V] (T : V →ₗ[K] W) :
    Module.finrank K (LinearMap.ker T) + Module.finrank K (LinearMap.range T) =
      Module.finrank K V := by
  have h := LinearMap.finrank_range_add_finrank_ker T
  omega

/-- Corollary A: if dim U < dim X, some nonzero vector is sent to 0. -/
theorem corollaryA [FiniteDimensional K V] [FiniteDimensional K W] (T : V →ₗ[K] W)
    (h : Module.finrank K W < Module.finrank K V) : ∃ x : V, x ≠ 0 ∧ T x = 0 := by
  have h2 := theorem2 T
  have h3 : Module.finrank K (LinearMap.range T) ≤ Module.finrank K W := Submodule.finrank_le _
  have h4 : 0 < Module.finrank K (LinearMap.ker T) := by omega
  have h5 : LinearMap.ker T ≠ ⊥ := by
    intro hk
    have h6 : Module.finrank K (LinearMap.ker T) = 0 := by simp [hk]
    omega
  obtain ⟨x, hx, hx0⟩ := Submodule.exists_mem_ne_zero_of_ne_bot h5
  exact ⟨x, hx0, hx⟩

/-- Corollary B: dim U = dim X, and T x = 0 only for x = 0; then the range is all of U. -/
theorem corollaryB [FiniteDimensional K V] [FiniteDimensional K W] (T : V →ₗ[K] W)
    (h : Module.finrank K W = Module.finrank K V) (hker : ∀ x : V, T x = 0 → x = 0) :
    LinearMap.range T = ⊤ := by
  have h2 := theorem2 T
  have hk : LinearMap.ker T = ⊥ := LinearMap.ker_eq_bot'.2 hker
  have h6 : Module.finrank K (LinearMap.ker T) = 0 := by simp [hk]
  have h7 : Module.finrank K (LinearMap.range T) = Module.finrank K W := by omega
  exact Submodule.eq_top_of_finrank_eq h7

/-- Control: without "T x = 0 only for x = 0", Corollary B fails. The map (x, y) -> (x, 0) of the
rational plane has equal dimensions, a nonzero kernel, and a range that is not the whole plane. -/
theorem control_corollaryB_needs_trivial_kernel :
    ∃ T : (Fin 2 → ℚ) →ₗ[ℚ] (Fin 2 → ℚ),
      (∃ x : Fin 2 → ℚ, x ≠ 0 ∧ T x = 0) ∧ ¬ Function.Surjective T := by
  refine ⟨(LinearMap.single ℚ (fun _ : Fin 2 => ℚ) 0).comp (LinearMap.proj 0), ?_, ?_⟩
  · refine ⟨Pi.single 1 1, ?_, ?_⟩
    · intro h
      have := congrFun h 1
      simp at this
    · ext i
      fin_cases i <;> simp
  · intro hs
    obtain ⟨x, hx⟩ := hs (Pi.single 1 1)
    have := congrFun hx 1
    simp at this

/-- Application 1: for n distinct points s_1..s_n of a field, the values of a polynomial of degree
less than n at those points can be prescribed arbitrarily. -/
theorem interpolation {n : ℕ} (s : Fin n → K) (hs : Function.Injective s) (u : Fin n → K) :
    ∃ p : Polynomial K, p.degree < n ∧ ∀ i, p.eval (s i) = u i := by
  classical
  let T : Polynomial.degreeLT K n →ₗ[K] (Fin n → K) :=
    LinearMap.pi fun i => (Polynomial.leval (s i)).comp (Polynomial.degreeLT K n).subtype
  haveI : FiniteDimensional K (Polynomial.degreeLT K n) :=
    LinearEquiv.finiteDimensional (Polynomial.degreeLTEquiv K n).symm
  have hfin : Module.finrank K (Polynomial.degreeLT K n) = Module.finrank K (Fin n → K) :=
    (Polynomial.degreeLTEquiv K n).finrank_eq
  have hinj : Function.Injective T := by
    rw [← LinearMap.ker_eq_bot, LinearMap.ker_eq_bot']
    intro p hp
    have h0 : ∀ i, (p : Polynomial K).eval (s i) = 0 := fun i => by
      have := congrFun hp i
      simpa [T] using this
    have hp' : (p : Polynomial K) = 0 := by
      by_contra hz
      have hdeg := Polynomial.mem_degreeLT.1 p.2
      have hnat : (p : Polynomial K).natDegree < n :=
        (Polynomial.natDegree_lt_iff_degree_lt hz).2 hdeg
      exact hz (Polynomial.eq_zero_of_natDegree_lt_card_of_eval_eq_zero (p : Polynomial K) hs h0
        (by simpa using hnat))
    exact Subtype.ext hp'
  have hsurj : Function.Surjective T :=
    (LinearMap.injective_iff_surjective_of_finrank_eq_finrank hfin).1 hinj
  obtain ⟨p, hp⟩ := hsurj u
  refine ⟨p, Polynomial.mem_degreeLT.1 p.2, fun i => ?_⟩
  have := congrFun hp i
  simpa [T] using this

#print axioms theorem1a
#print axioms theorem1b
#print axioms theorem2
#print axioms corollaryA
#print axioms corollaryB
#print axioms control_corollaryB_needs_trivial_kernel
#print axioms interpolation

end Book24LM
