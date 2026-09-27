-- GATE-DECLARE: sorries = none
-- GATE-REASON: foundational to Orthogenesis.Geometry, compiled as part of the
-- Orthogenesis root since before this repo's per-file audit convention existed
-- (lake build has always reached it); no tools/leancheck.sh --audit report was
-- ever produced against it by name until now.
import Mathlib.Tactic

namespace Orthogenesis

/-- 2D vector for geometric embedding. -/
structure Vec2 where
  x : ℝ
  y : ℝ

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
noncomputable def hexToVec2 (h : HexCoord) : Vec2 :=
  let x : ℝ := (h.q : ℝ) + (h.r : ℝ) / 2
  let y : ℝ := (Real.sqrt 3 / 2) * (h.r : ℝ)
  ⟨x, y⟩

/-- The six-neighbour list always has length 6 — the six-fold ring. -/
theorem hexNeighbors_length (h : HexCoord) : (hexNeighbors h).length = 6 := rfl

/-- The six axial neighbour directions are pairwise distinct. -/
theorem hexNeighbors_nodup (h : HexCoord) : (hexNeighbors h).Nodup := by
  simp [hexNeighbors, HexCoord.mk.injEq] <;> omega

end Orthogenesis
