/-
  book14/Polysemy.lean — the two counting rules of the IJL entry template, kernel-checked.
  Import-free (no Mathlib).  Principia Orthogona, Book XIV.  Pablo Nogueira Grossi, G6 LLC, 2026.

  The manuscript "Towards a Predictive Architecture for Dictionary Entry Design" (IJL v3)
  makes two rules that count senses. This file checks what each rule can and cannot do.
  The linguistic judgements are inputs; the kernel checks only the logic that follows.

  §1 Q3, the co-predication diagnostic: "readings that can co-occur in a single grammatical
     utterance are branches of one sense; readings that cannot are separate senses."
     For that to assign every reading to exactly one sense, co-predication must be
     transitive (`classes_force_transitive`). One non-transitive triple is enough to make
     Q3 assign no sense division at all (`three_readings_no_division`).

  §2 §3.3, "one fold produces two sense branches; two folds produce up to four".
     This holds for binary folds (`leaves_le_pow`). A binary fold of depth one always has
     exactly two branches (`depth_one_two`), so the paper's own three-qualia 'book'
     (three branches from one fold, §5.1) is not binary. The rule has to read
     "at least two", and the bound then fails.
-/
namespace Polysemy

/-! ## §1 The co-predication diagnostic -/

/-- If "same sense" is exactly co-predication, co-predication is transitive. -/
theorem classes_force_transitive {α β : Type} (R : α → α → Prop) (f : α → β)
    (h : ∀ x y, R x y ↔ f x = f y) : ∀ x y z, R x y → R y z → R x z :=
  fun x y z hxy hyz => (h x z).2 (((h x y).1 hxy).trans ((h y z).1 hyz))

/-- Three readings of one noun. -/
inductive Reading where
  | object | content | institution
  deriving DecidableEq

/-- A judgement table: object~content, content~institution, object≁institution.
    The table is an input (MODEL), to be tested on corpus data. It is the pattern
    reported for 'newspaper' in the dot-object literature. -/
def copred : Reading → Reading → Bool
  | .object, .institution => false
  | .institution, .object => false
  | _, _ => true

theorem copred_not_transitive :
    copred .object .content = true ∧ copred .content .institution = true ∧
    copred .object .institution = false := by decide

/-- Under such a table, Q3 assigns no sense division, into any set of senses. -/
theorem three_readings_no_division {β : Type} :
    ¬ ∃ f : Reading → β, ∀ x y, copred x y = true ↔ f x = f y := by
  intro ⟨f, h⟩
  have h1 := (h .object .content).1 (by decide)
  have h2 := (h .content .institution).1 (by decide)
  have h3 := (h .object .institution).2 (h1.trans h2)
  exact absurd h3 (by decide)

/-! ## §2 Fold depth and sense count -/

/-- A binary fold tree: a sense either stays (leaf) or folds into two branches. -/
inductive BTree where
  | leaf : BTree
  | node : BTree → BTree → BTree

def BTree.leaves : BTree → Nat
  | .leaf => 1
  | .node l r => l.leaves + r.leaves

def BTree.depth : BTree → Nat
  | .leaf => 0
  | .node l r => max l.depth r.depth + 1

/-- "k folds produce up to 2^k senses": true for binary folds. -/
theorem leaves_le_pow : ∀ t : BTree, t.leaves ≤ 2 ^ t.depth
  | .leaf => by simp [BTree.leaves, BTree.depth]
  | .node l r => by
      have hl := leaves_le_pow l
      have hr := leaves_le_pow r
      have h1 : 2 ^ l.depth ≤ 2 ^ (max l.depth r.depth) :=
        Nat.pow_le_pow_right (by decide) (Nat.le_max_left _ _)
      have h2 : 2 ^ r.depth ≤ 2 ^ (max l.depth r.depth) :=
        Nat.pow_le_pow_right (by decide) (Nat.le_max_right _ _)
      simp only [BTree.leaves, BTree.depth, Nat.pow_succ]
      omega

theorem depth_zero_leaf : ∀ t : BTree, t.depth = 0 → t.leaves = 1
  | .leaf, _ => rfl
  | .node _ _, h => by simp [BTree.depth] at h

/-- One binary fold yields exactly two senses. So a three-branch fold (the qualia of 'book')
    is not binary, and the paper's doubling rule does not cover it. -/
theorem depth_one_two : ∀ t : BTree, t.depth = 1 → t.leaves = 2
  | .leaf, h => by simp [BTree.depth] at h
  | .node l r, h => by
      have hm : max l.depth r.depth = 0 := by simp [BTree.depth] at h; omega
      have hl : l.depth = 0 := by have := Nat.le_max_left l.depth r.depth; omega
      have hr : r.depth = 0 := by have := Nat.le_max_right l.depth r.depth; omega
      simp [BTree.leaves, depth_zero_leaf l hl, depth_zero_leaf r hr]

end Polysemy

#print axioms Polysemy.classes_force_transitive
#print axioms Polysemy.copred_not_transitive
#print axioms Polysemy.three_readings_no_division
#print axioms Polysemy.leaves_le_pow
#print axioms Polysemy.depth_zero_leaf
#print axioms Polysemy.depth_one_two
