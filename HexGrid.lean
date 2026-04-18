-- HexGrid.lean
import Mathlib.Analysis.SpecialFunctions.Sqrt

namespace Orthogenesis

structure Vec2 where
  x : ℝ
  y : ℝ
deriving Repr, DecidableEq

structure HexCoord where
  q : ℤ
  r : ℤ
deriving Repr, DecidableEq, Hashable

def hexNeighbors (h : HexCoord) : List HexCoord :=
  [ ⟨h.q+1, h.r  ⟩, ⟨h.q+1, h.r-1⟩, ⟨h.q,   h.r-1⟩,
    ⟨h.q-1, h.r  ⟩, ⟨h.q-1, h.r+1⟩, ⟨h.q,   h.r+1⟩ ]

/-- Six neighbors, always exactly 6. -/
lemma hexNeighbors_length (h : HexCoord) : (hexNeighbors h).length = 6 := by
  simp [hexNeighbors]

def hexToVec2 (h : HexCoord) : Vec2 :=
  { x := (h.q : ℝ) + (h.r : ℝ) / 2
    y := Real.sqrt 3 / 2 * (h.r : ℝ) }

end Orthogenesis
