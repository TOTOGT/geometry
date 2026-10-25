import Mathlib

/-!
# ChEKbonacci.lean - k-bonacci facts behind the ring-size question in chE-gtct.html

STATUS: UNTESTED. Written without a local Lean toolchain. Run `lake env lean ChEKbonacci.lean`
and send the real output; fix against what the compiler says, not by guessing.

Convention (Parks-Wills, arXiv:2208.01224, eq. 1.1): f_0 = 1, f_n = 0 for n < 0,
f_n = f_{n-1} + ... + f_{n-k}. Rank 3 runs 1,1,2,4,7,13,24 and rank 4 runs 1,1,2,4,8,15,29,56.

What is and is not claimed:
* PROVED here (finite, by `decide`): 13 = f^(3)_5, 56 = f^(4)_7, the 7th terms (index 6) are 24 and 29
  at ranks 3 and 4 (so the 7th term does NOT give 13 and 56), and the candidate ring size
  `ring k = f^(k)_(2k-1)` takes the values 3, 13, 56, 236, ... for k = 2..10.
* PROVED here (general): the closed form `M k = 2^(k-3) * (2^(k+1) - k)` is strictly increasing for
  k >= 3, and `2 * (M k - 1) + 2` is too.
* NOT proved here: that `ring k = M k` for ALL k >= 3. That identity is Parks-Wills Corollary 3.2
  specialised to n = 2k-1 (credit: Parks and Wills 2022, building on Dunkel 1925); only k = 3..10
  is checked below, and chE-audit-verify.py checks k = 3..40.
* NOT established: that `ring` is the intended definition. It fits two data points (13, 56) and
  gives 3, not 13, at k = 2, contradicting the docstring "Dcrit(2) = 26". Hypothesis only.
-/

namespace ChEKbonacci

/-- window k n = [f_n, f_{n-1}, ..., f_{n-k+1}] -/
def window (k : ℕ) : ℕ → List ℕ
  | 0 => 1 :: List.replicate (k - 1) 0
  | n + 1 => (window k n).sum :: (window k n).take (k - 1)

/-- k-bonacci number f^(k)_n (Parks-Wills convention). -/
def kb (k n : ℕ) : ℕ := (window k n).headD 0

theorem kb_3_5 : kb 3 5 = 13 := by decide
theorem kb_4_7 : kb 4 7 = 56 := by decide
theorem kb_2_6 : kb 2 6 = 13 := by decide

/-- The 7th term (index 6) is 24 at rank 3 and 29 at rank 4: not 13 and 56. -/
theorem seventh_term_rank3 : kb 3 6 = 24 := by decide
theorem seventh_term_rank4 : kb 4 6 = 29 := by decide

/-- For ranks 6..12 the 7th term has stopped changing (finite check, not a proof for all k). -/
theorem seventh_term_stabilises :
    (List.range' 6 7).all (fun k => kb k 6 == 32) = true := by decide

/-- Candidate ring size: the term at index 2k-1 of the rank-k sequence. HYPOTHESIS. -/
def ring (k : ℕ) : ℕ := kb k (2 * k - 1)

theorem ring_values :
    (List.range' 2 9).map ring = [3, 13, 56, 236, 976, 3984, 16128, 64960, 260864] := by decide

/-- Closed form (Parks-Wills Cor. 3.2 at n = 2k-1), valid for k >= 3. -/
def M (k : ℕ) : ℕ := 2 ^ (k - 3) * (2 ^ (k + 1) - k)

theorem ring_eq_M_small : (List.range' 3 8).all (fun k => ring k == M k) = true := by decide

theorem M_pos (k : ℕ) (hk : 3 ≤ k) : 0 < M k := by
  have h1 : k < 2 ^ k := Nat.lt_two_pow_self
  have h2 : 2 ^ (k + 1) = 2 * 2 ^ k := by ring
  unfold M
  exact Nat.mul_pos (by positivity) (by omega)

theorem key (q m : ℕ) (hq : m < q) :
    q * (16 * q - (m + 3)) < q * 2 * (32 * q - (m + 3 + 1)) := by
  have hpos : 0 < q := by omega
  have h : 16 * q - (m + 3) < 2 * (32 * q - (m + 3 + 1)) := by omega
  calc q * (16 * q - (m + 3)) < q * (2 * (32 * q - (m + 3 + 1))) :=
        mul_lt_mul_of_pos_left h hpos
    _ = q * 2 * (32 * q - (m + 3 + 1)) := by ring

theorem M_lt_succ (k : ℕ) (hk : 3 ≤ k) : M k < M (k + 1) := by
  obtain ⟨m, rfl⟩ : ∃ m, k = m + 3 := ⟨k - 3, by omega⟩
  have hq : m < 2 ^ m := Nat.lt_two_pow_self
  have e1 : 2 ^ (m + 3 + 1) = 16 * 2 ^ m := by ring
  have e2 : 2 ^ (m + 3 + 1 + 1) = 32 * 2 ^ m := by ring
  have h1 : m + 3 - 3 = m := by omega
  have h2 : m + 3 + 1 - 3 = m + 1 := by omega
  unfold M
  rw [h1, h2, e1, e2, pow_succ]
  exact key (2 ^ m) m hq

/-- critDim from the closed form. -/
def critDimM (k : ℕ) : ℕ := 2 * (M k - 1) + 2

theorem critDimM_3 : critDimM 3 = 26 := by decide
theorem critDimM_4 : critDimM 4 = 112 := by decide

theorem critDimM_lt_succ (k : ℕ) (hk : 3 ≤ k) : critDimM k < critDimM (k + 1) := by
  have a := M_lt_succ k hk
  have b := M_pos k hk
  unfold critDimM
  omega

end ChEKbonacci
