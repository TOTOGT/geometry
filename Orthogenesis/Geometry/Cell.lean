import Orthogenesis.Geometry.HexGrid
import Orthogenesis.Geometry.Growth

namespace Orthogenesis

/-- A structural cell in the honeycomb. -/
structure Cell where
  coord : HexCoord
  stage : ℕ
deriving Repr, DecidableEq

/-- Center of the cell in ℝ². -/
def Cell.center (c : Cell) : Vec2 :=
  hexToVec2 c.coord

/-- Structural radius of the cell at its stage. -/
def Cell.radius (P : GrowthParams) (c : Cell) : ℝ :=
  R P c.stage

end Orthogenesis

