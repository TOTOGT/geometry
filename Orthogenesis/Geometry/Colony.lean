import Orthogenesis.Geometry.Cell
import Mathlib.Data.Finset.Basic

namespace Orthogenesis

/-- A honeycomb colony: finite set of structural cells. -/
structure Colony where
  cells : Finset Cell

/-- Insert a new cell into the colony. -/
def Colony.insert (C : Colony) (c : Cell) : Colony :=
      { cells := _root_.insert c C.cells }

/-- Expand the colony by adding all neighbors of all existing cells. -/
def Colony.expand (C : Colony) : Colony :=
    let expandOne (c : Cell) : Finset Cell :=
    let neigh := hexNeighbors c.coord
    let stage := c.stage + 1
    (neigh.map (fun h => Cell.mk h stage)).toFinset
  let newCells := C.cells.fold (· ∪ ·) ∅ expandOne
  { cells := C.cells ∪ newCells }
end Orthogenesis
