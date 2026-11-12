/-
  ReebWedge.lean  (2026-11-12)  --  run by the author 2026-11-12: `lake env lean` (v4.32.0), no errors;
  `#print axioms` on all three theorems = [propext, Classical.choice, Quot.sound], no sorryAx.
  Five earlier rounds failed against the compiler first (see docs/audit-log.md, 2026-11-12).

  PURPOSE. Close the last gap noted in ReebPullback.lean: `contactVol` was an explicit formula,
  not a Mathlib wedge product. This file compares it with Mathlib's shuffle-sum product
  `AlternatingMap.domCoprod` applied to the 1-form `omega p` and the 2-form `extDeriv omega p`.

  WHAT IS PROVED. `wedge12_eq_shuffle`: for any 1-form a and 2-form b on E3,
      wedge12 a b (u, v, w) = a(u) b(v, w) - a(v) b(u, w) + a(w) b(u, v)
  (the proof applies `MultilinearMap.domCoprod_alternization_eq` and sums the six permutations of
  Fin 1 ⊕ Fin 2 explicitly). `contactVol_eq_wedge12`: with a = omega p and b = extDeriv omega p
  (`dAlpha_eq_extDeriv`, ReebFlowExtDeriv.lean) this equals `contactVol p u v w`, for every p, u, v, w.
  `wedge12_frame`: (omega ^ extDeriv omega)(d_r, d_theta, d_z) = -2 r, i.e. alpha ^ d(alpha) =
  -2 r dr ^ dtheta ^ dz.

  NOT CLAIMED. Anything about r = 0 in the polar chart; anything beyond the 1-form ^ 2-form case;
  that this is Mathlib's *convention* for normalizing the wedge (it is the unnormalized shuffle
  sum; a different convention rescales both sides by a constant, which does not affect
  volume-preservation). `wedge12` is defined here, via `domCoprod` and `TensorProduct.lid`; it is
  not a Mathlib name.
-/

import Mathlib
import ReebFlowExtDeriv

open ReebFlowExt

namespace ReebWedge

/-- Wedge of a 1-form and a 2-form at a point, as a real number, using Mathlib's `domCoprod`
    (a tensor-valued shuffle sum) followed by the canonical iso ℝ ⊗ ℝ ≃ ℝ. -/
noncomputable def wedge12
    (a : ContinuousAlternatingMap ℝ E3 ℝ (Fin 1)) (b : ContinuousAlternatingMap ℝ E3 ℝ (Fin 2))
    (v : Fin 1 ⊕ Fin 2 → E3) : ℝ :=
  TensorProduct.lid ℝ ℝ
    (AlternatingMap.domCoprod a.toAlternatingMap b.toAlternatingMap v)

/-- The explicit 3-term shuffle formula, for any 1-form `a` and 2-form `b`. -/
theorem wedge12_eq_shuffle
    (a : ContinuousAlternatingMap ℝ E3 ℝ (Fin 1)) (b : ContinuousAlternatingMap ℝ E3 ℝ (Fin 2))
    (u v w : E3) :
    wedge12 a b (Sum.elim (fun _ => u) ![v, w])
      = a ![u] * b ![v, w] - a ![v] * b ![u, w] + a ![w] * b ![u, v] := by
  unfold wedge12
  -- Round 2 (diagnostic). Previous round showed `simp` leaves a sum over the quotient
  -- `Perm.ModSumCongr` of `Quotient.liftOn' ..` terms, which does not enumerate. New route:
  -- Mathlib's `MultilinearMap.domCoprod_alternization_eq` says
  --   alternatization (domCoprod a b) = (1! * 2!) • (a.domCoprod b),
  -- and `alternatization_apply` is a plain sum over `Perm (Fin 1 ⊕ Fin 2)` (6 terms).
  have key := MultilinearMap.domCoprod_alternization_eq a.toAlternatingMap b.toAlternatingMap
  have hv := congrArg (fun f => f (Sum.elim (fun _ => u) ![v, w])) key
  simp only [MultilinearMap.alternatization_apply, AlternatingMap.smul_apply] at hv
  -- Round 4. (Round 3 showed: `decide` enumerates the 6 perms, but a bare `simp` also unfolded
  -- the right-hand side `domCoprod` back into the opaque coset sum, and left `if i = 0 ..` inside
  -- lambdas.) Fixes: freeze the right-hand side as `D`; evaluate each summand with one generic lemma.
  generalize hD : (a.toAlternatingMap.domCoprod b.toAlternatingMap) (Sum.elim (fun _ => u) ![v, w]) = D
    at hv ⊢
  simp only [Fintype.card_fin, Nat.factorial_one, Nat.factorial_two, one_mul] at hv
  -- one generic evaluation lemma for a single summand
  have term_eq : ∀ σ : Equiv.Perm (Fin 1 ⊕ Fin 2),
      (MultilinearMap.domDomCongr σ
        (MultilinearMap.domCoprod (a.toAlternatingMap : MultilinearMap ℝ (fun _ : Fin 1 => E3) ℝ)
          (b.toAlternatingMap : MultilinearMap ℝ (fun _ : Fin 2 => E3) ℝ)))
        (Sum.elim (fun _ => u) ![v, w])
      = (a.toAlternatingMap ![Sum.elim (fun _ => u) ![v, w] (σ (Sum.inl 0))]) ⊗ₜ[ℝ]
        (b.toAlternatingMap ![Sum.elim (fun _ => u) ![v, w] (σ (Sum.inr 0)),
             Sum.elim (fun _ => u) ![v, w] (σ (Sum.inr 1))]) := by
    intro σ
    rw [MultilinearMap.domDomCongr_apply, MultilinearMap.domCoprod_apply]
    -- (Round 5) Round 4's `congr 2` tried to unify a MultilinearMap with a ContinuousAlternatingMap.
    -- Instead rewrite the two argument functions explicitly and close by `rfl`.
    have e1 : (fun i₁ : Fin 1 => Sum.elim (fun _ => u) ![v, w] (σ (Sum.inl i₁)))
        = ![Sum.elim (fun _ => u) ![v, w] (σ (Sum.inl 0))] := by
      funext i; fin_cases i; rfl
    have e2 : (fun i₂ : Fin 2 => Sum.elim (fun _ => u) ![v, w] (σ (Sum.inr i₂)))
        = ![Sum.elim (fun _ => u) ![v, w] (σ (Sum.inr 0)),
            Sum.elim (fun _ => u) ![v, w] (σ (Sum.inr 1))] := by
      funext i; fin_cases i <;> rfl
    rw [e1, e2]
    rfl
  -- antisymmetry of b on two arguments
  have hbswap : ∀ x y : E3, b ![y, x] = - b ![x, y] := by
    intro x y
    have h := b.toAlternatingMap.map_swap (v := ![x, y]) (i := 0) (j := 1) (by decide)
    have e : (![x, y] ∘ Equiv.swap (0 : Fin 2) 1) = ![y, x] := by
      funext i; fin_cases i <;> simp
    rw [e] at h
    exact h
  -- list the 6 permutations (identity, 3 transpositions, 2 three-cycles)
  have huniv : (Finset.univ : Finset (Equiv.Perm (Fin 1 ⊕ Fin 2))) =
      {1, Equiv.swap (Sum.inl 0) (Sum.inr 0), Equiv.swap (Sum.inl 0) (Sum.inr 1),
       Equiv.swap (Sum.inr 0) (Sum.inr 1),
       Equiv.swap (Sum.inl 0) (Sum.inr 0) * Equiv.swap (Sum.inr 0) (Sum.inr 1),
       Equiv.swap (Sum.inr 0) (Sum.inr 1) * Equiv.swap (Sum.inl 0) (Sum.inr 0)} := by
    decide
  rw [huniv] at hv
  simp (config := {decide := true}) only [Finset.sum_insert, Finset.mem_insert,
    Finset.mem_singleton, Finset.sum_singleton] at hv
  simp only [term_eq] at hv
  simp [Equiv.Perm.sign_mul, Equiv.Perm.sign_swap', Equiv.swap_apply_def] at hv
  -- (Round 6) hv : six tensor terms = 2 * D. Apply lid, use antisymmetry of b, close by linarith.
  rw [two_mul] at hv
  have h2 := congrArg (TensorProduct.lid ℝ ℝ) hv
  simp only [map_add, map_neg, TensorProduct.lid_tmul, smul_eq_mul] at h2
  rw [hbswap u v, hbswap v w, hbswap u w] at h2
  linarith

/-- **`contactVol` is Mathlib's wedge `omega ∧ extDeriv omega`** (1-form ∧ 2-form, shuffle-sum
    convention), at every point of the model R^3 with coordinates (r, theta, z). -/
theorem contactVol_eq_wedge12 (p u v w : E3) :
    wedge12 (omega p) (extDeriv omega p) (Sum.elim (fun _ => u) ![v, w])
      = contactVol p u v w := by
  rw [wedge12_eq_shuffle]
  have h1 : ∀ x : E3, omega p ![x] = alphaCat p x := fun x => by
    simpa using omega_apply p ![x]
  have h2 : ∀ x y : E3, extDeriv omega p ![x, y] = dAlpha p x y := fun x y =>
    (dAlpha_eq_extDeriv p x y).symm
  rw [h1, h1, h1, h2, h2, h2]
  unfold contactVol
  ring

/-- Frame value: `(omega ∧ extDeriv omega)(d_r, d_theta, d_z) = -2 r`. -/
theorem wedge12_frame (p : E3) :
    wedge12 (omega p) (extDeriv omega p)
        (Sum.elim (fun _ => ((1 : ℝ), (0 : ℝ), (0 : ℝ))) ![((0 : ℝ), (1 : ℝ), (0 : ℝ)), ((0 : ℝ), (0 : ℝ), (1 : ℝ))])
      = -2 * p.1 := by
  rw [contactVol_eq_wedge12]
  exact contactVol_frame p

end ReebWedge

#print axioms ReebWedge.wedge12_eq_shuffle
#print axioms ReebWedge.contactVol_eq_wedge12
#print axioms ReebWedge.wedge12_frame
