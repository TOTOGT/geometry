-- Orthogenesis/Geometry/GaussBonnet.lean
--
-- Discrete Gauss-Bonnet: the total angle defect of a triangulated closed
-- surface is 2*pi*chi, with chi = V - E + F.
--
-- Candidate machine-checked core for Volume XI (rung 28, Index Theory), the
-- FLOOR volume named in WP-82 and not yet written.  Gauss-Bonnet is the first
-- and oldest index theorem: a local quantity, integrated, returns a global
-- topological invariant.  The discrete form needs no differential geometry at
-- all -- it is the Euclidean angle sum plus one counting identity.
--
-- WHAT THIS ESTABLISHES
--   total_defect            : sum of defects = 2*pi*V - pi*F.  Exchange of
--                             summation order and the Euclidean angle sum.
--   discrete_gauss_bonnet   : with 3F = 2E, that equals 2*pi*(V - E + F).
--   tetra_gauss_bonnet      : a non-vacuous instance.  The tetrahedron has
--                             V=4, E=6, F=4, chi=2, and total defect 4*pi.
--
-- WHAT IT DOES NOT ESTABLISH
--   * 3F = 2E is a HYPOTHESIS, not a theorem.  It encodes "every face is a
--     triangle and every edge borders exactly two faces".  Deriving it needs a
--     simplicial complex and an orientability condition, neither of which is
--     built here.
--   * No surface is constructed.  `Triangulation` is a structure; a vacuous
--     instance (empty faces, empty vertices) satisfies it.  That is why
--     `tetra` is included and why `tetra_gauss_bonnet` is part of the claim
--     rather than an illustration of it.  A theorem with no witness is the
--     vacuity failure this corpus has recorded four times.
--   * chi is taken as the integer V - E + F, not as an independently defined
--     topological invariant.  Identifying the two is the content of the real
--     theorem and is not attempted here.
--
-- Toolchain: Lean 4 + Mathlib, pinned by lean-toolchain.
-- Axiom report: pending first CI run.  Until it is pasted below with the run
-- number, this file is a claim and not a verification.

import Mathlib

namespace Orthogenesis.GaussBonnet

open Finset

variable {ι κ : Type*}

/-- A triangulated closed surface, recorded only as far as the angle
    bookkeeping needs it: a finite set of faces, a finite set of vertices, and
    the interior angle of each face at each vertex, taken to be `0` when the
    vertex does not belong to the face. -/
structure Triangulation (faces : Finset ι) (verts : Finset κ) where
  /-- `θ f v` is the interior angle of face `f` at vertex `v`. -/
  θ : ι → κ → ℝ
  /-- Every face is a Euclidean triangle: its interior angles sum to `π`. -/
  face_angle_sum : ∀ f ∈ faces, ∑ v ∈ verts, θ f v = Real.pi

namespace Triangulation

variable {faces : Finset ι} {verts : Finset κ} (T : Triangulation faces verts)

/-- The angle defect at a vertex: a full turn, minus the angles meeting there.
    On a flat patch the defect is zero; curvature is what the angles fail to
    close by. -/
noncomputable def defect (v : κ) : ℝ := 2 * Real.pi - ∑ f ∈ faces, T.θ f v

/-- Summing the defect over every vertex gives `2πV − πF`.

    This is exchange of summation order and nothing else: each face
    contributes exactly `π` to the total angle sum, whichever vertices it
    contributes it at. -/
theorem total_defect :
    ∑ v ∈ verts, T.defect v
      = 2 * Real.pi * verts.card - Real.pi * faces.card := by
  classical
  have hswap : ∑ v ∈ verts, ∑ f ∈ faces, T.θ f v
             = ∑ f ∈ faces, ∑ v ∈ verts, T.θ f v := Finset.sum_comm
  have hface : ∑ f ∈ faces, ∑ v ∈ verts, T.θ f v = faces.card * Real.pi := by
    rw [Finset.sum_congr rfl T.face_angle_sum, Finset.sum_const, nsmul_eq_mul]
  have hsplit : ∑ v ∈ verts, T.defect v
              = (∑ v ∈ verts, (2 * Real.pi)) - ∑ v ∈ verts, ∑ f ∈ faces, T.θ f v := by
    simp only [defect, Finset.sum_sub_distrib]
  rw [hsplit, hswap, hface, Finset.sum_const, nsmul_eq_mul]
  ring

/-- **Discrete Gauss–Bonnet.**  If every face is a triangle and every edge is
    shared by exactly two faces — the counting identity `3F = 2E` — then the
    total angle defect is `2π·χ`, with `χ = V − E + F`.

    The Euler characteristic is taken in `ℝ` on the right-hand side so that no
    truncated `ℕ` subtraction can occur. -/
theorem discrete_gauss_bonnet (edges : ℕ) (hTri : 3 * faces.card = 2 * edges) :
    ∑ v ∈ verts, T.defect v
      = 2 * Real.pi * ((verts.card : ℝ) - edges + faces.card) := by
  have key : (3 : ℝ) * faces.card = 2 * edges := by exact_mod_cast hTri
  rw [total_defect]
  linear_combination (-Real.pi) * key

end Triangulation

/-- The regular tetrahedron, as a non-vacuity witness. Four vertices, four
    faces, each face the complement of one vertex, three equilateral triangles
    meeting at every vertex. -/
noncomputable def tetra : Triangulation (Finset.univ : Finset (Fin 4)) (Finset.univ : Finset (Fin 4)) where
  θ f v := if v = f then 0 else Real.pi / 3
  face_angle_sum := by
    intro f _
    fin_cases f <;> simp [Fin.sum_univ_four] <;> ring

/-- The tetrahedron has `χ = 4 − 6 + 4 = 2` and total defect `4π = 2π·χ`.
    Each vertex carries three angles of `π/3`, so each defect is `2π − π = π`,
    and there are four of them. -/
theorem tetra_gauss_bonnet :
    ∑ v ∈ (Finset.univ : Finset (Fin 4)), tetra.defect v = 4 * Real.pi := by
  have h := tetra.discrete_gauss_bonnet 6 (by decide)
  simp only [Finset.card_univ, Fintype.card_fin] at h
  rw [h]
  ring

end Orthogenesis.GaussBonnet
