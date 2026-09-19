/-
  ToeplitzIndex.lean — the combinatorial core of Volume XI's index.

  WHAT THIS IS. book7/ch-fritz-noether computes the index of the Toeplitz operator
  T_k on the Hardy space H², symbol e^{ikθ}, by counting basis vectors, and gets
  ind(T_k) = -k. This file formalises that count.

  SCOPE, STATED BEFORE THE THEOREMS. The Hardy space has an orthonormal basis
  indexed by ℕ, and T_k acts on it by n ↦ n + k when n + k ≥ 0 and kills the basis
  vector otherwise. That action is the object formalised here, as a map
  ℕ → Option ℕ. What is proved is that its kernel and cokernel are the finite sets
  the chapter claims, and that their difference is -k.

  What is NOT formalised, and is not claimed: that T_k is bounded, that it is
  Fredholm, that the index is a homotopy invariant, or F. Noether's theorem that
  the index equals minus the winding number of the symbol. Those are the analytic
  content. This file is the arithmetic underneath them, and it is exactly what the
  verify script counted.

  Lean core only — no Mathlib. `#print axioms` at the end is the verdict.

  KERNEL-CHECKED 2026-09-19, Lean v4.33.0-rc1, no imports. Seven declarations:
  none admitted; `#print axioms` reports only [propext, Classical.choice,
  Quot.sound] or a subset for each.
-/

namespace VolXI

/-- The Toeplitz operator with symbol `e^{ikθ}`, on the Hardy basis indexed by `ℕ`:
the basis vector `n` goes to `n + k` when that is still a basis index, and is
killed otherwise. -/
def toeplitz (k : Int) (n : Nat) : Option Nat :=
  if 0 ≤ (n : Int) + k then some ((n : Int) + k).toNat else none

/-- **The kernel.** A basis vector is killed exactly when `k` pushes it below zero. -/
theorem mem_ker (k : Int) (n : Nat) : toeplitz k n = none ↔ (n : Int) + k < 0 := by
  unfold toeplitz
  split <;> rename_i h <;> simp <;> omega

/-- **The cokernel.** A basis index is missed exactly when it sits below `k`. -/
theorem mem_coker (k : Int) (m : Nat) :
    (∀ n : Nat, toeplitz k n ≠ some m) ↔ (m : Int) < k := by
  constructor
  · intro h
    refine Decidable.byContradiction (fun hc => ?_)
    have hn := h ((m : Int) - k).toNat
    unfold toeplitz at hn
    rw [if_pos (by omega)] at hn
    exact hn (congrArg some (by omega))
  · intro h n hn
    unfold toeplitz at hn
    split at hn <;> rename_i hp
    · have : ((n : Int) + k).toNat = m := Option.some.inj hn
      omega
    · simp at hn

/-- Number of killed basis vectors. -/
def kerCount (k : Int) : Nat := if k < 0 then (-k).toNat else 0

/-- Number of missed basis indices. -/
def cokerCount (k : Int) : Nat := if 0 ≤ k then k.toNat else 0

/-- `kerCount` counts exactly the `n` the kernel characterisation admits. -/
theorem kerCount_spec (k : Int) (n : Nat) :
    ((n : Int) + k < 0) ↔ n < kerCount k := by
  unfold kerCount; split <;> omega

/-- `cokerCount` counts exactly the `m` the cokernel characterisation admits. -/
theorem cokerCount_spec (k : Int) (m : Nat) :
    ((m : Int) < k) ↔ m < cokerCount k := by
  unfold cokerCount; split <;> omega

/-- **The index.** `dim ker − dim coker = −k`, for every `k`. -/
theorem toeplitz_index (k : Int) :
    (kerCount k : Int) - (cokerCount k : Int) = -k := by
  unfold kerCount cokerCount; split <;> split <;> omega

/-- The case the chapter uses: `Γ` winds once, so the index is `−1`. -/
theorem index_of_winding_one :
    (kerCount 1 : Int) - (cokerCount 1 : Int) = -1 := toeplitz_index 1

/-- And the differential operator's answer, for contrast: the zero symbol has
index `0`. The chapter's point is that `d/dθ − a` gives `0` for *every* `a`; here
only the corresponding Toeplitz statement is formalised. -/
theorem index_of_winding_zero :
    (kerCount 0 : Int) - (cokerCount 0 : Int) = 0 := toeplitz_index 0

end VolXI

#print axioms VolXI.mem_ker
#print axioms VolXI.mem_coker
#print axioms VolXI.kerCount_spec
#print axioms VolXI.cokerCount_spec
#print axioms VolXI.toeplitz_index
#print axioms VolXI.index_of_winding_one
#print axioms VolXI.index_of_winding_zero
