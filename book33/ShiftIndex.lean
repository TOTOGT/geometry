/-
Volume XXXIII — rung 33, the top of the floor ladder.

This is the ceiling the rest of the ladder is climbing toward, which is why it
is written first: a reader who skips to the end of the series lands here, and
should find the payload rather than a summary.

A note on where this file is NOT. `docs/math-placement-map.md` gives Volume XI
the role "the algebraic floor" and lists its subject as number fields, units,
class groups and K-theory. The shift index is none of those — it is an index
computation on a free module — so it does not belong to XI, and an earlier
draft of this file that claimed XI was wrong about its own address.

WHAT IS PROVED HERE

Let V = ℕ →₀ F be the finitely supported sequences over a field F: the free
F-module with basis e₀, e₁, e₂, …  The forward shift Sₖ sends eₙ to eₙ₊ₖ; the
backward shift Bₖ sends eₙ₊ₖ to eₙ and kills e₀ … eₖ₋₁.

    ind(Sₖ) = dim ker − dim coker = 0 − k = −k
    ind(Bₖ) = dim ker − dim coker = k − 0 = +k

Both are theorems below with actual kernels and cokernels — `LinearMap.ker`,
the quotient `V ⧸ LinearMap.range`, and `Module.finrank` — not a count kept by
hand. `bshift_comp_shift` records that Bₖ ∘ Sₖ = id, which is why one is
injective-not-surjective and the other surjective-not-injective.

WHAT IS NOT PROVED HERE, AND MUST NOT BE READ IN

This is the ALGEBRAIC index. There is no topology in this file: no norm, no
completion, no boundedness, no compactness, no Fredholm theory in the analytic
sense, and no Toeplitz operator on a Hardy space. F. Noether's 1921 theorem
— ind(T_f) = −winding(f) — is not formalised, and the agreement between
`ind(Sₖ) = −k` and the winding number of zᵏ is here an observation about two
numbers, not a proof that they are the same theorem.

What the file does establish is that the sign and the size are forced by linear
algebra alone, with no analysis involved: an operator with a one-sided inverse
on an infinite-dimensional space has an index, the index is not zero, and which
side the inverse is on decides the sign. That is the part of the story that a
reader can check with a basis and no limits.

Toolchain: Lean 4.33.0-rc1. Mathlib: tag v4.33.0-rc1.
-/
import Mathlib.LinearAlgebra.Finsupp.Defs
import Mathlib.LinearAlgebra.Isomorphisms
import Mathlib.LinearAlgebra.Dimension.Constructions
import Mathlib.LinearAlgebra.Dimension.Finite

open Finsupp LinearMap

variable (F : Type) [Field F]

abbrev V : Type := ℕ →₀ F

noncomputable def shift (k : ℕ) : V F →ₗ[F] V F := lmapDomain F F (· + k)

noncomputable def bshift (k : ℕ) : V F →ₗ[F] V F :=
  lcomapDomain (M := F) (R := F) (· + k) (add_left_injective k)

noncomputable def trunc (k : ℕ) : V F →ₗ[F] (Fin k →₀ F) :=
  lcomapDomain (M := F) (R := F) Fin.val Fin.val_injective

noncomputable def incl (k : ℕ) : (Fin k →₀ F) →ₗ[F] V F := lmapDomain F F Fin.val

theorem shift_apply (k n : ℕ) (f : V F) : shift F k f (n + k) = f n := by
  simp only [shift, lmapDomain_apply]
  exact mapDomain_apply (add_left_injective k) f n

theorem shift_injective (k : ℕ) : Function.Injective (shift F k) :=
  mapDomain_injective (add_left_injective k)

theorem ker_shift (k : ℕ) : ker (shift F k) = ⊥ :=
  ker_eq_bot.mpr (shift_injective F k)

theorem trunc_surjective (k : ℕ) : Function.Surjective (trunc F k) := by
  intro g
  exact ⟨mapDomain Fin.val g,
    leftInverse_lcomapDomain_mapDomain (R := F) (M := F) Fin.val Fin.val_injective g⟩

theorem ker_trunc (k : ℕ) : ker (trunc F k) = range (shift F k) := by
  ext f
  simp only [mem_ker, trunc, lcomapDomain_apply, mem_range]
  constructor
  · intro hf
    have hzero : ∀ m : ℕ, m < k → f m = 0 := by
      intro m hm
      have h := congrArg (fun g => g ⟨m, hm⟩) hf
      simpa [comapDomain_apply] using h
    refine ⟨comapDomain (· + k) f ((add_left_injective k).injOn), ?_⟩
    simp only [shift, lmapDomain_apply]
    refine mapDomain_comapDomain _ (add_left_injective k) f ?_
    intro n hn
    have hne : f n ≠ 0 := by simpa using (Finsupp.mem_support_iff.mp hn)
    have : k ≤ n := by
      by_contra hc
      exact hne (hzero n (Nat.lt_of_not_le hc))
    exact ⟨n - k, by show n - k + k = n; omega⟩
  · rintro ⟨g, rfl⟩
    ext i
    simp only [comapDomain_apply, Finsupp.coe_zero, Pi.zero_apply, shift, lmapDomain_apply]
    refine mapDomain_of_notMem_range _ _ ?_
    rintro ⟨m, hm⟩
    have hm' : m + k = (i : ℕ) := hm
    have hi : (i : ℕ) < k := i.isLt
    omega

noncomputable def cokerEquiv (k : ℕ) : (V F ⧸ range (shift F k)) ≃ₗ[F] (Fin k →₀ F) :=
  (Submodule.quotEquivOfEq _ _ (ker_trunc F k).symm).trans
    (quotKerEquivOfSurjective (trunc F k) (trunc_surjective F k))

theorem finrank_ker_shift (k : ℕ) : Module.finrank F (ker (shift F k)) = 0 := by
  rw [ker_shift]
  exact finrank_bot F (V F)

theorem finrank_coker_shift (k : ℕ) :
    Module.finrank F (V F ⧸ range (shift F k)) = k := by
  rw [(cokerEquiv F k).finrank_eq, Module.finrank_finsupp]
  simp

/-- **The index of the k-fold shift is −k.** -/
theorem shift_index (k : ℕ) :
    (Module.finrank F (ker (shift F k)) : ℤ)
      - (Module.finrank F (V F ⧸ range (shift F k)) : ℤ) = -k := by
  rw [finrank_ker_shift, finrank_coker_shift]
  simp

#print axioms shift_index

/-! ### The other sign -/

theorem bshift_comp_shift (k : ℕ) : (bshift F k).comp (shift F k) = LinearMap.id := by
  ext f n
  exact congrArg (fun g => g n)
    (leftInverse_lcomapDomain_mapDomain (R := F) (M := F) (· + k) (add_left_injective k) _)

theorem bshift_surjective (k : ℕ) : Function.Surjective (bshift F k) := by
  intro f
  refine ⟨shift F k f, ?_⟩
  exact leftInverse_lcomapDomain_mapDomain (R := F) (M := F) (· + k) (add_left_injective k) f

theorem range_bshift (k : ℕ) : range (bshift F k) = ⊤ :=
  range_eq_top.mpr (bshift_surjective F k)

theorem incl_injective (k : ℕ) : Function.Injective (incl F k) :=
  mapDomain_injective Fin.val_injective

theorem range_incl (k : ℕ) : range (incl F k) = ker (bshift F k) := by
  ext f
  simp only [mem_range, mem_ker, incl, lmapDomain_apply, bshift, lcomapDomain_apply]
  constructor
  · rintro ⟨g, rfl⟩
    ext n
    simp only [comapDomain_apply, Finsupp.coe_zero, Pi.zero_apply]
    refine mapDomain_of_notMem_range _ _ ?_
    rintro ⟨i, hi⟩
    have hi' : (i : ℕ) = n + k := hi
    have := i.isLt
    omega
  · intro hf
    have hzero : ∀ n : ℕ, k ≤ n → f n = 0 := by
      intro n hn
      have h := congrArg (fun g => g (n - k)) hf
      simp only [comapDomain_apply, Finsupp.coe_zero, Pi.zero_apply] at h
      have : n - k + k = n := by omega
      rwa [this] at h
    refine ⟨comapDomain Fin.val f Fin.val_injective.injOn, ?_⟩
    refine mapDomain_comapDomain _ Fin.val_injective f ?_
    intro n hn
    have hne : f n ≠ 0 := by simpa using (Finsupp.mem_support_iff.mp hn)
    have hlt : n < k := by
      by_contra hc
      exact hne (hzero n (Nat.le_of_not_lt hc))
    exact ⟨⟨n, hlt⟩, rfl⟩

noncomputable def kerBshiftEquiv (k : ℕ) : (ker (bshift F k)) ≃ₗ[F] (Fin k →₀ F) :=
  (LinearEquiv.ofEq _ _ (range_incl F k).symm).trans
    (LinearEquiv.ofInjective (incl F k) (incl_injective F k)).symm

theorem finrank_ker_bshift (k : ℕ) : Module.finrank F (ker (bshift F k)) = k := by
  rw [(kerBshiftEquiv F k).finrank_eq, Module.finrank_finsupp]
  simp

theorem finrank_coker_bshift (k : ℕ) :
    Module.finrank F (V F ⧸ range (bshift F k)) = 0 := by
  have : Subsingleton (V F ⧸ range (bshift F k)) := by
    rw [range_bshift]; infer_instance
  simpa using Module.finrank_eq_of_rank_eq (R := F) (M := V F ⧸ range (bshift F k))
    (rank_subsingleton' F _)

/-- **The index of the k-fold backward shift is +k.** -/
theorem bshift_index (k : ℕ) :
    (Module.finrank F (ker (bshift F k)) : ℤ)
      - (Module.finrank F (V F ⧸ range (bshift F k)) : ℤ) = k := by
  rw [finrank_ker_bshift, finrank_coker_bshift]
  simp

#print axioms shift_index
#print axioms bshift_index
#print axioms bshift_comp_shift
