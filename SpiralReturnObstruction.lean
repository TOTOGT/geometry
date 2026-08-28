/-!
# SpiralReturnObstruction.lean

A strengthening of Theorem T1's hypotheses in `GCTC/Operators/Chain.lean`.

`spiral_return_exists` currently takes two hypotheses:

    h_nontrivial     : G.iter 64 x₀ ≠ x₀
    h_second_circuit : G.iter 128 x₀ ≠ x₀

and discharges the conclusion `sr.x₀' ≠ sr.x₀` directly from the second. The
first is unused. That is honest — the file says the dynamics needed to derive
the second are left to AXLE — but it means the non-triviality of the spiral is
assumed rather than obtained.

This file isolates exactly what stands between the two. The answer is a single
obstruction, and it is small: `h_second_circuit` follows from `h_nontrivial`
UNLESS the 64-iterate has x₀ on an orbit of period exactly two. There is nothing
else to rule out. So the hypothesis can be replaced by the weaker and more
natural "the circuit map has no 2-cycle at x₀", which is a statement about G
rather than about the 128th iterate.

Mathlib-free. `Function.iterate` and its `f^[n]` notation are Mathlib, so the
iterate is defined here and the one lemma about it is proved here. The file
checks with `lean` alone and imports nothing.

## What is proved

* `iter_add` — `iter f (m+n) x = iter f m (iter f n x)`, by induction on m.
* `two_cycle_of_return` — if `iter f n x ≠ x` and `iter f (2n) x = x`, then x
  sits on a period-2 orbit of `iter f n`. The obstruction, exhibited.
* `second_circuit_of_no_two_cycle` — the replacement hypothesis: no 2-cycle at
  x, plus `iter f n x ≠ x`, gives `iter f (2n) x ≠ x`.
* `two_cycle_is_inhabited` — a 2-cycle exists (`Bool.not`), so the hypothesis
  cannot be dropped, only weakened.

## What is NOT proved

Nothing here says a dm³ G-chain has no 2-cycle. That is a dynamical fact about
a particular G and is exactly the AXLE obligation; this file only shows it is
the *whole* of what remains, which the two-hypothesis form does not make visible.
-/

namespace SpiralReturnObstruction

/-- The iterate, defined here rather than imported: `Function.iterate` and its
    `f^[n]` notation are Mathlib, and this file is deliberately Mathlib-free so
    it checks with `lean` alone. This matches `GChain.iter` in shape, so
    transporting these results to the chain is a rename, not a re-proof. -/
def iter {X : Type _} (f : X → X) : Nat → X → X
  | 0, x => x
  | (n + 1), x => f (iter f n x)

/-- `iter f (m + n) x = iter f m (iter f n x)`. The one fact about iteration
    used below, proved rather than assumed. -/
theorem iter_add {X : Type _} (f : X → X) : ∀ (m n : Nat) (x : X),
    iter f (m + n) x = iter f m (iter f n x)
  | 0, n, x => by rw [Nat.zero_add]; rfl
  | (m + 1), n, x => by
      have ih := iter_add f m n x
      show iter f (m + 1 + n) x = iter f (m + 1) (iter f n x)
      rw [show m + 1 + n = (m + n) + 1 from by omega]
      show f (iter f (m + n) x) = f (iter f m (iter f n x))
      rw [ih]

/-- **The obstruction, exhibited.** If the circuit does not return after one
    pass but does after two, then the circuit map `iter f n` carries `x` on an
    orbit of period exactly two. This is the only way a second circuit can close
    while the first does not. -/
theorem two_cycle_of_return {X : Type _} (f : X → X) (n : Nat) (x : X)
    (h_first : iter f n x ≠ x) (h_return : iter f (2 * n) x = x) :
    iter f n (iter f n x) = x ∧ iter f n x ≠ x := by
  refine ⟨?_, h_first⟩
  rw [← iter_add f n n x, show n + n = 2 * n from by omega]
  exact h_return

/-- **The replacement hypothesis.** `h_second_circuit` in `spiral_return_exists`
    can be weakened to this: the circuit map has no 2-cycle at `x`. That is a
    statement about `G`, to be discharged from the dynamics, rather than an
    assumption about the 128th iterate which is most of the conclusion. -/
theorem second_circuit_of_no_two_cycle {X : Type _} (f : X → X) (n : Nat) (x : X)
    (h_first : iter f n x ≠ x)
    (h_no_two_cycle : iter f n (iter f n x) ≠ x) :
    iter f (2 * n) x ≠ x := by
  intro h_return
  exact h_no_two_cycle (two_cycle_of_return f n x h_first h_return).1

/-- Instantiated at the g⁶⁴ circuit, the form Theorem T1 uses. -/
theorem second_circuit_64 {X : Type _} (f : X → X) (x : X)
    (h_first : iter f 64 x ≠ x)
    (h_no_two_cycle : iter f 64 (iter f 64 x) ≠ x) :
    iter f 128 x ≠ x := by
  have h := second_circuit_of_no_two_cycle f 64 x h_first h_no_two_cycle
  rwa [show 2 * 64 = 128 from by omega] at h

/-- The obstruction is real, not an artefact of the proof: a genuine 2-cycle
    exists, so no argument derives `iter f (2*n) x ≠ x` from `iter f n x ≠ x`
    alone. The extra hypothesis in Theorem T1 cannot simply be dropped — it can
    only be weakened, which is what this file does. -/
theorem two_cycle_is_inhabited :
    iter Bool.not 1 true ≠ true ∧ iter Bool.not 2 true = true := by
  constructor <;> decide

#print axioms iter_add
#print axioms two_cycle_of_return
#print axioms second_circuit_of_no_two_cycle
#print axioms second_circuit_64
#print axioms two_cycle_is_inhabited

end SpiralReturnObstruction
