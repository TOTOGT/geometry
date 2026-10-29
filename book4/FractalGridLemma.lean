/-!
# FractalGridLemma — grid lemma for the 45° tent curve (book4/fractals.html §3)

Mathlib-free: core Lean 4 only, so it can be checked with
    lean book4/FractalGridLemma.lean
and cannot drift with a Mathlib bump.

STATUS: compiled by the author on Lean v4.32.0 with no errors and no sorry (2026-10-29).
`#print axioms` on even_level_no_crossing: propext, Classical.choice, Quot.sound.

## What this file claims (and what it does not)

The 45° tent curve refines a piece with direction `u` into four pieces with directions
`u·ω, u·ω, u·ω̄, u·ω̄` (ω = e^{iπ/4}). Doing this twice, a piece of direction `u`
becomes the sixteen unit steps `refine2 u` below (hand derivation: ω² = i, ω·ω̄ = 1,
ω̄² = −i), at grid spacing 1/8 of the parent.

PROVED HERE (if it compiles):
1. `allUnit_steps`   — at every even level 2m, every step of `steps m` is a unit lattice step.
2. `total_steps`     — the steps of `steps m` add up to (8^m, 0)  (the endpoint is right).
3. `unit_edges_no_cross` — two unit lattice edges never properly cross (integer orientation test).
4. `even_level_no_crossing` — hence no two edges of the level-2m polygon properly cross.

NOT PROVED HERE:
* That `refine2` really is two applications of the tent refinement. That is the hand
  computation above, and `fractals-grid-lemma.py` checks it numerically; Lean does not see it.
* The odd levels (the "tent" argument in the chapter).
* Anything about the limit curve or the open-set condition.
-/

namespace FractalGrid

abbrev V := Int × Int

/-- A unit lattice step. -/
def UnitStep (v : V) : Prop :=
  (v.1 = 1 ∧ v.2 = 0) ∨ (v.1 = 0 ∧ v.2 = 1) ∨ (v.1 = -1 ∧ v.2 = 0) ∨ (v.1 = 0 ∧ v.2 = -1)

/-- Rotation by +90°, i.e. multiplication by i. -/
def rot (v : V) : V := (-v.2, v.1)

/-- Negation, i.e. multiplication by −1. -/
def neg (v : V) : V := (-v.1, -v.2)

/-- Two refinement steps of a piece with direction `u`: sixteen unit steps.
    From ω² = i and ω·ω̄ = 1:  NE piece → [iu, iu, u, u], SE piece → [u, u, −iu, −iu]. -/
def refine2 (u : V) : List V :=
  [rot u, rot u, u, u, rot u, rot u, u, u,
   u, u, neg (rot u), neg (rot u), u, u, neg (rot u), neg (rot u)]

def refineList : List V → List V
  | [] => []
  | u :: l => refine2 u ++ refineList l

/-- Direction lists of the even levels: `steps m` is level 2m, in units of grid spacing 8^(-m). -/
def steps : Nat → List V
  | 0 => [(1, 0)]
  | m + 1 => refineList (steps m)

def AllUnit : List V → Prop
  | [] => True
  | v :: l => UnitStep v ∧ AllUnit l

theorem unit_rot {v : V} (h : UnitStep v) : UnitStep (rot v) := by
  simp only [UnitStep, rot] at *
  omega

theorem unit_neg {v : V} (h : UnitStep v) : UnitStep (neg v) := by
  simp only [UnitStep, neg] at *
  omega

theorem allUnit_refine2 {u : V} (hu : UnitStep u) : AllUnit (refine2 u) := by
  have h1 := unit_rot hu
  have h2 := unit_neg (unit_rot hu)
  simp only [refine2, AllUnit]
  exact ⟨h1, h1, hu, hu, h1, h1, hu, hu, hu, hu, h2, h2, hu, hu, h2, h2, trivial⟩

theorem allUnit_append : ∀ (a b : List V), AllUnit a → AllUnit b → AllUnit (a ++ b)
  | [], b, _, hb => by simpa using hb
  | v :: a, b, ha, hb => by
      simp only [AllUnit] at ha
      simp only [List.cons_append, AllUnit]
      exact ⟨ha.1, allUnit_append a b ha.2 hb⟩

theorem allUnit_refineList : ∀ (l : List V), AllUnit l → AllUnit (refineList l)
  | [], _ => by simp [refineList, AllUnit]
  | u :: l, h => by
      simp only [AllUnit] at h
      simp only [refineList]
      exact allUnit_append _ _ (allUnit_refine2 h.1) (allUnit_refineList l h.2)

theorem allUnit_steps : ∀ m : Nat, AllUnit (steps m)
  | 0 => by
      show UnitStep (1, 0) ∧ AllUnit []
      exact ⟨Or.inl ⟨rfl, rfl⟩, trivial⟩
  | m + 1 => by
      simp only [steps]
      exact allUnit_refineList _ (allUnit_steps m)

/-! ## Edges and the integer crossing test -/

/-- Twice the signed area of the triangle p q r. -/
def orient (p1 p2 q1 q2 r1 r2 : Int) : Int := (q1 - p1) * (r2 - p2) - (q2 - p2) * (r1 - p1)

/-- Proper crossing of segment ab and segment cd: each segment's endpoints lie strictly on opposite
    sides of the other's line. Touching at an endpoint or overlapping collinearly is NOT a proper crossing. -/
def Cross (a1 a2 b1 b2 c1 c2 d1 d2 : Int) : Prop :=
  ((orient a1 a2 b1 b2 c1 c2 < 0 ∧ 0 < orient a1 a2 b1 b2 d1 d2) ∨
   (0 < orient a1 a2 b1 b2 c1 c2 ∧ orient a1 a2 b1 b2 d1 d2 < 0)) ∧
  ((orient c1 c2 d1 d2 a1 a2 < 0 ∧ 0 < orient c1 c2 d1 d2 b1 b2) ∨
   (0 < orient c1 c2 d1 d2 a1 a2 ∧ orient c1 c2 d1 d2 b1 b2 < 0))

/-- Two unit lattice edges never properly cross. -/
theorem unit_edges_no_cross (a1 a2 c1 c2 u1 u2 v1 v2 : Int)
    (hu : (u1 = 1 ∧ u2 = 0) ∨ (u1 = 0 ∧ u2 = 1) ∨ (u1 = -1 ∧ u2 = 0) ∨ (u1 = 0 ∧ u2 = -1))
    (hv : (v1 = 1 ∧ v2 = 0) ∨ (v1 = 0 ∧ v2 = 1) ∨ (v1 = -1 ∧ v2 = 0) ∨ (v1 = 0 ∧ v2 = -1)) :
    ¬ Cross a1 a2 (a1 + u1) (a2 + u2) c1 c2 (c1 + v1) (c2 + v2) := by
  intro h
  unfold Cross orient at h
  rcases hu with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ <;>
  rcases hv with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ <;>
  omega

/-- The edges (start, start + step) of the path that starts at `p` and takes the given steps. -/
def edgesFrom : V → List V → List (V × V)
  | _, [] => []
  | p, v :: l => (p, (p.1 + v.1, p.2 + v.2)) :: edgesFrom (p.1 + v.1, p.2 + v.2) l

theorem edges_unit : ∀ (l : List V) (p : V), AllUnit l → ∀ e ∈ edgesFrom p l,
    ∃ (a u : V), UnitStep u ∧ e = (a, (a.1 + u.1, a.2 + u.2)) := by
  intro l
  induction l with
  | nil => intro p _ e he; simp [edgesFrom] at he
  | cons v l ih =>
    intro p h e he
    simp only [AllUnit] at h
    simp only [edgesFrom] at he
    rcases List.mem_cons.mp he with h1 | h1
    · exact ⟨p, v, h.1, h1⟩
    · exact ih _ h.2 e h1

/-- MAIN RESULT (even levels): no two edges of the level-2m polygon properly cross. -/
theorem even_level_no_crossing (m : Nat) (e₁ e₂ : V × V)
    (h₁ : e₁ ∈ edgesFrom (0, 0) (steps m)) (h₂ : e₂ ∈ edgesFrom (0, 0) (steps m)) :
    ¬ Cross e₁.1.1 e₁.1.2 e₁.2.1 e₁.2.2 e₂.1.1 e₂.1.2 e₂.2.1 e₂.2.2 := by
  obtain ⟨a, u, hu, rfl⟩ := edges_unit _ _ (allUnit_steps m) e₁ h₁
  obtain ⟨c, v, hv, rfl⟩ := edges_unit _ _ (allUnit_steps m) e₂ h₂
  exact unit_edges_no_cross a.1 a.2 c.1 c.2 u.1 u.2 v.1 v.2 hu hv

/-! ## Endpoint: the steps add up to (8^m, 0) -/

def total : List V → V
  | [] => (0, 0)
  | v :: l => (v.1 + (total l).1, v.2 + (total l).2)

def pow8 : Nat → Int
  | 0 => 1
  | n + 1 => 8 * pow8 n

theorem total_append : ∀ (a b : List V),
    total (a ++ b) = ((total a).1 + (total b).1, (total a).2 + (total b).2)
  | [], b => by simp [total]
  | v :: a, b => by
      simp only [List.cons_append, total]
      rw [total_append a b]
      simp only [Prod.mk.injEq]
      constructor <;> omega

theorem total_refine2 (u : V) : total (refine2 u) = (8 * u.1, 8 * u.2) := by
  simp only [refine2, total, rot, neg, Prod.mk.injEq]
  constructor <;> omega

theorem total_refineList : ∀ l : List V,
    total (refineList l) = (8 * (total l).1, 8 * (total l).2)
  | [] => by simp [refineList, total]
  | u :: l => by
      simp only [refineList]
      rw [total_append, total_refine2, total_refineList l]
      simp only [total, Prod.mk.injEq]
      constructor <;> omega

theorem total_steps : ∀ m : Nat, total (steps m) = (pow8 m, 0)
  | 0 => by simp [steps, total, pow8]
  | m + 1 => by
      simp only [steps]
      rw [total_refineList, total_steps m]
      simp [pow8]

end FractalGrid

#print axioms FractalGrid.even_level_no_crossing
#print axioms FractalGrid.total_steps
