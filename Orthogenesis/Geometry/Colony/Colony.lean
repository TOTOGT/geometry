import Orthogenesis.Architecture.Cell
import Mathlib.Data.Finset.Basic

namespace Orthogenesis

/-- A honeycomb colony: finite set of structural cells. -/
structure Colony where
  cells : Finset Cell
deriving Repr

/-- Insert a new cell into the colony. -/
def Colony.insert (C : Colony) (c : Cell) : Colony :=
  { cells := C.cells.insert c }

/-- Expand the colony by adding all neighbors of all existing cells. -/
def Colony.expand (C : Colony) : Colony :=
  let newCells :=
    C.cells.fold
      (fun acc c =>
        let neigh := hexNeighbors c.coord
        let stage := c.stage + 1
        let new := neigh.map (fun h => Cell.mk h stage)
        acc ∪ new.toFinset)
      ∅
  { cells := C.cells ∪ newCells }

end Orthogenesis
