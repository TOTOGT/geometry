-- Orthogenesis/Architecture/Coverage.lean
--   · coord_coverage      -- the ring walk at radius k visits exactly 6k coords (k >= 1)
--   · no_coord_collision  -- Colony.expand preserves coordinate injectivity,
--                            under an explicit separation hypothesis (see §4)
--
-- Toolchain: Lean 4 + Mathlib, pinned by lean-toolchain (v4.32.0).
-- NASA gaps: FN-C-101 L (coord coverage), FN-H-101 L (no collision)
--
-- REWRITTEN 2026-08-21.  This file had never compiled.  An import of
-- `Mathlib.Data.Int.Order`, a module removed upstream, failed before the body
-- was ever elaborated, so nothing in it had been checked by the kernel.  Two
-- defects were sitting behind that failure:
--
--   1. `hexRing_card` ended in `sorry` in its successor case, so
--      `coord_coverage`, which is one call to it, was not proved.  The old
--      `hexRing` was a fold-based walk over an `Array` with `!` indexing,
--      which is not a shape any cardinality argument can get hold of.  It is
--      replaced below by the same walk written as an image of
--      `range 6 ×ˢ range k`, which is linear in k and t and therefore
--      provable.  The set of points is unchanged; only the presentation is.
--
--   2. `no_coord_collision` was FALSE as stated.  Counterexample: take
--      C.cells = {Cell.mk (0,0) 0, Cell.mk (1,0) 0}, which is
--      coordinate-injective with every cell at stage 0.  Expanding, (1,0) is
--      a neighbour of (0,0), so Cell.mk (1,0) 1 enters C.expand while
--      Cell.mk (1,0) 0 is already there: two distinct cells at one
--      coordinate.  The hypothesis that rules this out is separation -- no
--      cell sits on another cell's neighbour -- and it is now an explicit
--      argument rather than an unstated assumption.  The canonical seed
--      satisfies it, which is the case §5 needed.

import Orthogenesis.Geometry.Colony
import Mathlib.Data.Finset.Card
import Mathlib.Tactic

namespace Orthogenesis

-- ─────────────────────────────────────────────────────────────────────────────
-- §1  Axial distance and the ring walk
-- ─────────────────────────────────────────────────────────────────────────────

/-- Axial (cube) distance between two hex coordinates:
    max(|Δq|, |Δr|, |Δq+Δr|), equivalently (|Δq| + |Δr| + |Δq+Δr|) / 2. -/
def hexDist (a b : HexCoord) : ℕ :=
  let dq := (a.q - b.q).natAbs
  let dr := (a.r - b.r).natAbs
  let ds := (a.q + a.r - b.q - b.r).natAbs
  (dq + dr + ds) / 2

/-- Point `t` of side `s` of the ring walk of radius `k`.

    The six axial directions are those of `hexNeighbors`:
    d0 = (1,0), d1 = (1,-1), d2 = (0,-1), d3 = (-1,0), d4 = (-1,1), d5 = (0,1).
    Side `s` begins at the corner `k • d_{s+4 mod 6}` and takes `k` steps in
    direction `d_s`, so consecutive sides meet at corners and each corner is
    reached once, at `t = 0`.  Written out per side so that every coordinate
    is linear in `k` and `t`, which is what makes injectivity decidable. -/
def hexRingPoint (k t s : ℕ) : HexCoord :=
  let K : ℤ := (k : ℤ)
  let T : ℤ := (t : ℤ)
  match s with
  | 0 => ⟨-K + T, K⟩
  | 1 => ⟨T, K - T⟩
  | 2 => ⟨K, -T⟩
  | 3 => ⟨K - T, -K⟩
  | 4 => ⟨-T, -K + T⟩
  | _ => ⟨-K, T⟩

/-- The ring of radius `k` centred at the origin, as the image of the walk. -/
def hexRing (k : ℕ) : Finset HexCoord :=
  if k = 0 then {⟨0, 0⟩}
  else (Finset.range 6 ×ˢ Finset.range k).image
        (fun p : ℕ × ℕ => hexRingPoint k p.2 p.1)

-- ─────────────────────────────────────────────────────────────────────────────
-- §2  coord_coverage
-- ─────────────────────────────────────────────────────────────────────────────

/-- The ring walk of radius `k >= 1` visits exactly `6k` distinct coordinates.
    Six sides of `k` steps each, and no point is visited twice: within a side
    the step index determines the point, and across two different sides the
    only common points would be corners, which the bound `t < k` excludes. -/
lemma hexRing_card (k : ℕ) (hk : 1 ≤ k) : (hexRing k).card = 6 * k := by
  have hk0 : ¬ k = 0 := by omega
  rw [hexRing, if_neg hk0, Finset.card_image_of_injOn, Finset.card_product,
      Finset.card_range, Finset.card_range]
  rintro ⟨s₁, t₁⟩ h₁ ⟨s₂, t₂⟩ h₂ heq
  simp only [Finset.coe_product, Set.mem_prod, Finset.mem_coe,
    Finset.mem_range] at h₁ h₂
  obtain ⟨hs₁, ht₁⟩ := h₁
  obtain ⟨hs₂, ht₂⟩ := h₂
  interval_cases s₁ <;> interval_cases s₂ <;>
    simp_all [hexRingPoint, HexCoord.mk.injEq, Prod.mk.injEq] <;> omega

/-- **coord_coverage.**  For `k >= 1` the ring at axial distance `k` from the
    origin contains exactly `6k` distinct hex coordinates.

    NASA gap: FN-C-101 L (Communications & PNT -- coverage verification).
    dm³ connection: ring n has 6n vertices, matching centred-hexagonal growth
    1 + 3n(n+1). -/
theorem coord_coverage (k : ℕ) (hk : 1 ≤ k) :
    (hexRing k).card = 6 * k :=
  hexRing_card k hk

-- ─────────────────────────────────────────────────────────────────────────────
-- §3  Coordinate injectivity
-- ─────────────────────────────────────────────────────────────────────────────

/-- A colony is **coordinate-injective** if no two distinct cells share a coord.
    The formal analogue of: no two modules occupy the same pad. -/
def Colony.CoordInjective (C : Colony) : Prop :=
  ∀ c₁ ∈ C.cells, ∀ c₂ ∈ C.cells, c₁.coord = c₂.coord → c₁ = c₂

/-- A colony is **separated** if no cell sits on a neighbour of a cell.
    Expansion writes stage-(s+1) cells onto neighbour coordinates, so without
    this the new cells can land on top of existing ones -- see the header. -/
def Colony.Separated (C : Colony) : Prop :=
  ∀ c ∈ C.cells, ∀ d ∈ C.cells, c.coord ∉ hexNeighbors d.coord

-- ─────────────────────────────────────────────────────────────────────────────
-- §4  no_coord_collision
-- ─────────────────────────────────────────────────────────────────────────────

/-- **no_coord_collision.**  A coordinate-injective, stage-uniform, separated
    colony stays coordinate-injective under one expansion.

    Separation is doing real work here and is not a technicality: without it
    the statement is false, and the header gives a two-cell counterexample.

    NASA gap: FN-H-101 L (Habitation -- cell occupancy invariants). -/
theorem Colony.no_coord_collision (C : Colony)
    (hInj : C.CoordInjective)
    (hStage : ∀ c ∈ C.cells, c.stage = 0)
    (hSep : C.Separated) :
    (C.expand).CoordInjective := by
  intro c₁ hc₁ c₂ hc₂ hcoord
  rw [Colony.mem_expand] at hc₁ hc₂
  rcases hc₁ with hc₁old | ⟨p₁, hp₁, h₁, hh₁, rfl⟩
  · rcases hc₂ with hc₂old | ⟨p₂, hp₂, h₂, hh₂, rfl⟩
    · exact hInj c₁ hc₁old c₂ hc₂old hcoord
    · exact absurd (hcoord ▸ hh₂) (hSep c₁ hc₁old p₂ hp₂)
  · rcases hc₂ with hc₂old | ⟨p₂, hp₂, h₂, hh₂, rfl⟩
    · exact absurd (hcoord ▸ hh₁) (hSep c₂ hc₂old p₁ hp₁)
    · have e₁ : p₁.stage = 0 := hStage p₁ hp₁
      have e₂ : p₂.stage = 0 := hStage p₂ hp₂
      simp only [] at hcoord
      exact Cell.ext hcoord (by simp [e₁, e₂])

-- ─────────────────────────────────────────────────────────────────────────────
-- §5  The canonical seed
-- ─────────────────────────────────────────────────────────────────────────────

/-- The canonical seed colony (single cell at the origin, stage 0) is
    coordinate-injective. -/
lemma seed_coord_injective :
    Colony.CoordInjective { cells := {Cell.mk ⟨0,0⟩ 0} } := by
  intro c₁ hc₁ c₂ hc₂ _
  simp only [Finset.mem_singleton] at hc₁ hc₂
  rw [hc₁, hc₂]

/-- The canonical seed is separated: the origin is not one of its own six
    neighbours. -/
lemma seed_separated :
    Colony.Separated { cells := {Cell.mk ⟨0,0⟩ 0} } := by
  intro c hc d hd
  simp only [Finset.mem_singleton] at hc hd
  subst hc; subst hd
  simp [hexNeighbors, HexCoord.mk.injEq]

/-- After one expansion from the canonical seed, coordinate injectivity holds. -/
lemma seed_expand_coord_injective :
    Colony.CoordInjective ({ cells := {Cell.mk ⟨0,0⟩ 0} } : Colony).expand := by
  apply Colony.no_coord_collision
  · exact seed_coord_injective
  · intro c hc
    simp only [Finset.mem_singleton] at hc
    rw [hc]
  · exact seed_separated

end Orthogenesis
