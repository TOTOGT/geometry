import Orthogenesis.Geometry.Cell
import Mathlib.Data.Finset.Basic

namespace Orthogenesis

/-- A honeycomb colony: finite set of structural cells. -/
structure Colony where
  cells : Finset Cell

/-- Insert a new cell into the colony. -/
def Colony.insert (C : Colony) (c : Cell) : Colony :=
  { cells := Insert.insert c C.cells }

/-- Expand the colony by adding all neighbors of all existing cells. -/
def Colony.expand (C : Colony) : Colony :=
  let expandOne (c : Cell) : Finset Cell :=
    let neigh := hexNeighbors c.coord
    let stage := c.stage + 1
    (neigh.map (fun h => Cell.mk h stage)).toFinset
  let newCells := C.cells.biUnion expandOne
  { cells := C.cells ∪ newCells }

/-- Iterated expansion: `expandN n` applies `expand` `n` times. -/
def Colony.expandN : ℕ → Colony → Colony
  | 0,     C => C
  | n + 1, C => (Colony.expandN n C).expand

/-- Membership in an expanded colony: a cell is either original, or a
    stage-(s+1) neighbour of some original cell. -/
theorem Colony.mem_expand {C : Colony} {x : Cell} :
    x ∈ C.expand.cells ↔
      x ∈ C.cells ∨ ∃ c ∈ C.cells, ∃ h ∈ hexNeighbors c.coord,
        x = Cell.mk h (c.stage + 1) := by
  unfold Colony.expand
  simp only [Finset.mem_union, Finset.mem_biUnion, List.mem_toFinset,
             List.mem_map]
  constructor
  · rintro (hx | ⟨c, hc, h, hh, hx⟩)
    · exact Or.inl hx
    · exact Or.inr ⟨c, hc, h, hh, hx.symm⟩
  · rintro (hx | ⟨c, hc, h, hh, hx⟩)
    · exact Or.inl hx
    · exact Or.inr ⟨c, hc, h, hh, hx.symm⟩

/-- Stage bound (discrete ε₀): from a stage-0 seed, `n` expansions keep every
    cell at stage ≤ n. -/
theorem Colony.stage_bound (C₀ : Colony) (h₀ : ∀ c ∈ C₀.cells, c.stage = 0) :
    ∀ n : ℕ, ∀ x ∈ (Colony.expandN n C₀).cells, x.stage ≤ n := by
  intro n
  induction n with
  | zero =>
    intro x hx
    simp only [Colony.expandN] at hx
    exact le_of_eq (h₀ x hx)
  | succ m ih =>
    intro x hx
    simp only [Colony.expandN] at hx
    rw [Colony.mem_expand] at hx
    rcases hx with hold | ⟨c, hc, _h, _hh, rfl⟩
    · exact le_trans (ih x hold) (Nat.le_succ m)
    · simpa using Nat.succ_le_succ (ih c hc)

end Orthogenesis
