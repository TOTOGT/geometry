namespace Orthogenesis

/-- 2D vector for geometric embedding. -/
structure Vec2 where
  x : ℝ
  y : ℝ
deriving Repr, DecidableEq

/-- Axial hex coordinates (q, r). -/
structure HexCoord where
  q : ℤ
  r : ℤ
deriving Repr, DecidableEq

/-- Six axial neighbors (pointy-top hex grid). -/
def hexNeighbors (h : HexCoord) : List HexCoord :=
  [ ⟨h.q+1, h.r  ⟩,
    ⟨h.q+1, h.r-1⟩,
    ⟨h.q,   h.r-1⟩,
    ⟨h.q-1, h.r  ⟩,
    ⟨h.q-1, h.r+1⟩,
    ⟨h.q,   h.r+1⟩ ]

/-- Axial → Euclidean embedding (standard). -/
def hexToVec2 (h : HexCoord) : Vec2 :=
  let x : ℝ := (h.q : ℝ) + (h.r : ℝ) / 2
  let y : ℝ := (Real.sqrt 3 / 2) * (h.r : ℝ)
  ⟨x, y⟩

end Orthogenesis
