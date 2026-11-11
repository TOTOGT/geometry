import Mathlib

/-!
# P² × P²: the Hodge-type and inverse-Lefschetz calculations, and the Frobenius-only countermodel

STATUS: written without a Lean toolchain; compiled by CI run #3 of `.github/workflows/jacobian-lean.yml`
(manual, commit 45cdb1f, `set -o pipefail` on): no `sorry`; axiom reports for `hodge_codim1`, `hodge_codim2`,
`pushforward_L2`, `L2_pushforward`, `FrobeniusCountermodel.F_similitude` are [propext, Classical.choice,
Quot.sound] (Mathlib tactic infrastructure; not a constructive build). Non-default target; not on the main gate.

WHAT THIS FILE IS. Exact arithmetic in the truncated ring CH = ℚ[a,b]/(a³,b³), graded
pieces stored as coefficient records. It proves identities about those records.

WHAT THIS FILE IS NOT. It does not prove that CH(P²×P²)_ℚ is ℚ[a,b]/(a³,b³), that the
cycle class map is injective there, that the monomials are a basis, or that the pushforward
of a correspondence is the map `pushforward` below. Those are the GEOMETRIC INPUTS,
listed here and taken as given (Stacks 02TX for the first; the rest is the push-pull
formula Γ_*(z) = pr₂*(pr₁^* z · Γ) integrated over the source):

  (G1) CH(P²×P²)_ℚ = ℚ[a,b]/(a³,b³), deg(a²b²) = 1.
  (G2) The nine monomials aⁱbʲ (i,j<3) are a ℚ-basis, so a class is its coefficient record.
  (G3) The pushforward of a correspondence with source-by-target coefficients
       (b₁a₂, b₁b₂, a₁a₂, a₁b₂) acts on degree-3 classes as `pushforward`.

The multiplication tables below are the truncated products for a³ = b³ = 0. They are
checked against sympy polynomial reduction in `verify_lean_tables.py`, not in Lean.
No theorem here is a statement about an arbitrary variety, and none touches the
general standard conjectures.
-/

namespace P2xP2

/-- x·a + y·b -/
@[ext] structure D1 where
  x : ℚ
  y : ℚ

/-- x·a² + y·ab + u·b² -/
@[ext] structure D2 where
  x : ℚ
  y : ℚ
  u : ℚ

/-- p·a²b + q·ab² -/
@[ext] structure D3 where
  p : ℚ
  q : ℚ

/-- (xa+yb)(x'a+y'b) = xx'a² + (xy'+yx')ab + yy'b² -/
def mul11 (z w : D1) : D2 := ⟨z.x * w.x, z.x * w.y + z.y * w.x, z.y * w.y⟩

/-- (xa+yb)(x'a²+y'ab+u'b²): a·a²=0, a·ab=a²b, a·b²=ab², b·a²=a²b, b·ab=ab², b·b²=0 -/
def mul12 (z : D1) (w : D2) : D3 := ⟨z.x * w.y + z.y * w.x, z.x * w.u + z.y * w.y⟩

/-- degree of (xa+yb)(p a²b + q ab²) = xq + yp  (deg a²b² = 1) -/
def deg13 (z : D1) (w : D3) : ℚ := z.x * w.q + z.y * w.p

/-- degree of (x a²+y ab+u b²)(x'a²+y'ab+u'b²) = xu' + yy' + ux' -/
def deg22 (z w : D2) : ℚ := z.x * w.u + z.y * w.y + z.u * w.x

/-- The polarization h = s·a + t·b. -/
def h (s t : ℚ) : D1 := ⟨s, t⟩
def h2 (s t : ℚ) : D2 := mul11 (h s t) (h s t)
def h3 (s t : ℚ) : D3 := mul12 (h s t) (h2 s t)

/-- primitive generators -/
def p1 (s t : ℚ) : D1 := ⟨s, -t⟩
def p2 (s t : ℚ) : D2 := ⟨s ^ 2, -(s * t), t ^ 2⟩

section Powers
variable (s t : ℚ)

theorem h2_eq : h2 s t = ⟨s ^ 2, 2 * s * t, t ^ 2⟩ := by
  ext <;> simp only [h2, mul11, h] <;> ring

theorem h3_eq : h3 s t = ⟨3 * s ^ 2 * t, 3 * s * t ^ 2⟩ := by
  ext <;> simp only [h3, h2, mul12, mul11, h] <;> ring

/-- deg h⁴ = 6 s² t² -/
theorem deg_h4 : deg22 (h2 s t) (h2 s t) = 6 * s ^ 2 * t ^ 2 := by
  simp only [deg22, h2, mul11, h]; ring

end Powers

/-! ## Codimension 0 and 1 -/

theorem hodge_codim0 {s t : ℚ} (hs : 0 < s) (ht : 0 < t) :
    0 < deg22 (h2 s t) (h2 s t) := by
  rw [deg_h4]; positivity

/-- h³ · z = 3st(tx+sy) · a²b² -/
theorem deg_h3_mul (s t : ℚ) (z : D1) :
    deg13 z (h3 s t) = 3 * s * t * (t * z.x + s * z.y) := by
  simp only [deg13, h3, h2, mul12, mul11, h]; ring

/-- the primitive space in codimension 1 is spanned by p₁ = s·a − t·b -/
theorem primitive_codim1 {s t : ℚ} (hs : s ≠ 0) (ht : t ≠ 0) (z : D1)
    (hz : deg13 z (h3 s t) = 0) : ∃ c : ℚ, z = ⟨c * s, -(c * t)⟩ := by
  rw [deg_h3_mul] at hz
  have h1 : t * z.x + s * z.y = 0 := by
    rcases mul_eq_zero.mp hz with h | h
    · exfalso
      rcases mul_eq_zero.mp h with h | h
      · rcases mul_eq_zero.mp h with h | h
        · norm_num at h
        · exact hs h
      · exact ht h
    · exact h
  refine ⟨z.x / s, ?_⟩
  have hx : z.x = z.x / s * s := by field_simp
  ext
  · exact hx
  · apply mul_left_cancel₀ hs
    show s * z.y = s * -(z.x / s * t)
    linear_combination h1 - t * hx

/-- −deg(z² h²) for z = c·p₁ equals 2c²s²t² -/
theorem codim1_value (s t c : ℚ) :
    -deg22 (mul11 ⟨c * s, -(c * t)⟩ ⟨c * s, -(c * t)⟩) (h2 s t)
      = 2 * c ^ 2 * s ^ 2 * t ^ 2 := by
  simp only [deg22, mul11, h2, h]; ring

/-- Hodge-type positivity, codimension 1, every ample rational polarization s,t>0:
    −deg(z²h²) > 0 for nonzero primitive z. -/
theorem hodge_codim1 {s t : ℚ} (hs : 0 < s) (ht : 0 < t) (z : D1)
    (hz : deg13 z (h3 s t) = 0) (hne : z ≠ ⟨0, 0⟩) :
    0 < -deg22 (mul11 z z) (h2 s t) := by
  obtain ⟨c, rfl⟩ := primitive_codim1 hs.ne' ht.ne' z hz
  have hc : c ≠ 0 := by
    intro h0
    apply hne
    ext <;> simp [h0]
  rw [codim1_value]
  positivity

/-! ## Codimension 2 -/

theorem hz_eq (s t : ℚ) (z : D2) :
    mul12 (h s t) z = ⟨s * z.y + t * z.x, s * z.u + t * z.y⟩ := by
  ext <;> simp only [mul12, h] <;> ring

/-- the primitive space in codimension 2 is exactly ℚ·p₂, p₂ = s²a² − st·ab + t²b² -/
theorem primitive_codim2 {s t : ℚ} (hs : s ≠ 0) (z : D2)
    (hz : mul12 (h s t) z = ⟨0, 0⟩) :
    ∃ c : ℚ, z = ⟨c * s ^ 2, -(c * s * t), c * t ^ 2⟩ := by
  rw [hz_eq] at hz
  have h1 : s * z.y + t * z.x = 0 := congrArg D3.p hz
  have h2' : s * z.u + t * z.y = 0 := congrArg D3.q hz
  refine ⟨z.x / s ^ 2, ?_⟩
  set c := z.x / s ^ 2 with hc
  have hx : z.x = c * s ^ 2 := by rw [hc]; field_simp
  have hy : z.y = -(c * s * t) := by
    apply mul_left_cancel₀ hs
    linear_combination h1 - t * hx
  have hu : z.u = c * t ^ 2 := by
    apply mul_left_cancel₀ hs
    linear_combination h2' - t * hy
  ext
  · exact hx
  · exact hy
  · exact hu

/-- p₂² = 3 s² t² · a²b², hence (c·p₂)² = 3c²s²t² -/
theorem codim2_value (s t c : ℚ) :
    deg22 ⟨c * s ^ 2, -(c * s * t), c * t ^ 2⟩ ⟨c * s ^ 2, -(c * s * t), c * t ^ 2⟩
      = 3 * c ^ 2 * s ^ 2 * t ^ 2 := by
  simp only [deg22]; ring

/-- Hodge-type positivity, codimension 2 on P²×P², every ample rational h = s·a + t·b:
    deg(z²) > 0 for every nonzero primitive class z (h·z = 0). -/
theorem hodge_codim2 {s t : ℚ} (hs : 0 < s) (ht : 0 < t) (z : D2)
    (hz : mul12 (h s t) z = ⟨0, 0⟩) (hne : z ≠ ⟨0, 0, 0⟩) :
    0 < deg22 z z := by
  obtain ⟨c, rfl⟩ := primitive_codim2 hs.ne' z hz
  have hc : c ≠ 0 := by
    intro h0
    apply hne
    ext <;> simp [h0]
  rw [codim2_value]
  positivity

/-- The full middle form is NOT positive definite: it is indefinite. The primitive
    condition and the sign (−1)^r are essential. (Signature (2,1) in the note.) -/
theorem middle_form_indefinite :
    ∃ z : D2, deg22 z z < 0 := by
  refine ⟨⟨1, 0, -1⟩, ?_⟩
  simp only [deg22]; norm_num

theorem middle_form_not_all_negative :
    ∃ z : D2, 0 < deg22 z z := by
  refine ⟨⟨0, 1, 0⟩, ?_⟩
  simp only [deg22]; norm_num

/-! ## The explicit inverse of L² and its algebraic realization -/

/-- L² : H² → H⁶, z ↦ h²·z (coefficients in the bases (a,b) and (a²b, ab²)). -/
def L2 (s t : ℚ) (z : D1) : D3 := mul12 z (h2 s t)

theorem L2_eq (s t : ℚ) (z : D1) :
    L2 s t z = ⟨2 * s * t * z.x + s ^ 2 * z.y, t ^ 2 * z.x + 2 * s * t * z.y⟩ := by
  ext <;> simp only [L2, mul12, h2, mul11, h] <;> ring

/-- det of L² is 3s²t². -/
theorem L2_det (s t : ℚ) : (2 * s * t) * (2 * s * t) - s ^ 2 * t ^ 2 = 3 * s ^ 2 * t ^ 2 := by
  ring

/-- Coefficients of a codimension-2 correspondence on X × X:
    ba = coeff of b₁a₂, bb = b₁b₂, aa = a₁a₂, ab = a₁b₂. -/
structure Corr where
  ba : ℚ
  bb : ℚ
  aa : ℚ
  ab : ℚ

/-- Γ_*(p a²b + q ab²) with Γ_*(z) = pr₂*(pr₁^* z · Γ), integrating over the source:
    a²b·b₁ = a²b² (degree 1), ab²·a₁ = a²b² (degree 1), the other two products vanish.
    (Geometric input G3.) -/
def pushforward (G : Corr) (w : D3) : D1 :=
  ⟨w.p * G.ba + w.q * G.aa, w.p * G.bb + w.q * G.ab⟩

/-- Γ = b₁(2a₂/(3st) − b₂/(3s²)) + a₁(−a₂/(3t²) + 2b₂/(3st)). -/
def Gamma (s t : ℚ) : Corr :=
  ⟨2 / (3 * s * t), -1 / (3 * s ^ 2), -1 / (3 * t ^ 2), 2 / (3 * s * t)⟩

/-- Γ_*(a²b) = 2a/(3st) − b/(3s²), Γ_*(ab²) = −a/(3t²) + 2b/(3st): the columns of (L²)⁻¹. -/
theorem Gamma_columns {s t : ℚ} :
    pushforward (Gamma s t) ⟨1, 0⟩ = ⟨2 / (3 * s * t), -1 / (3 * s ^ 2)⟩ ∧
    pushforward (Gamma s t) ⟨0, 1⟩ = ⟨-1 / (3 * t ^ 2), 2 / (3 * s * t)⟩ := by
  constructor <;> ext <;> simp [pushforward, Gamma]

/-- Γ_* ∘ L² = id on H². -/
theorem pushforward_L2 {s t : ℚ} (hs : s ≠ 0) (ht : t ≠ 0) (z : D1) :
    pushforward (Gamma s t) (L2 s t z) = z := by
  rw [L2_eq]
  ext <;> simp only [pushforward, Gamma] <;> field_simp <;> ring

/-- L² ∘ Γ_* = id on H⁶. -/
theorem L2_pushforward {s t : ℚ} (hs : s ≠ 0) (ht : t ≠ 0) (w : D3) :
    L2 s t (pushforward (Gamma s t) w) = w := by
  rw [L2_eq]
  ext <;> simp only [pushforward, Gamma] <;> field_simp <;> ring

/-- L⁴ : H⁰ → H⁸ is multiplication by 6s²t²; its inverse is the scalar 1/(6s²t²),
    induced by the cycle (6s²t²)⁻¹ [X×X]. -/
theorem L4_inverse {s t : ℚ} (hs : s ≠ 0) (ht : t ≠ 0) (x : ℚ) :
    (1 / (6 * s ^ 2 * t ^ 2)) * ((6 * s ^ 2 * t ^ 2) * x) = x := by
  field_simp

end P2xP2

/-! ## The Frobenius-only deduction fails

F = q²·I has every eigenvalue of absolute value q² (the weight-four value) and satisfies
FᵀJF = q⁴J, yet J = diag(1,−1) is indefinite. This is a statement about 2×2 matrices only.
It is NOT claimed to arise from a variety and is NOT a counterexample to any standard
conjecture. It shows that "eigenvalue sizes + pairing similitude" cannot imply positivity.
-/

namespace FrobeniusCountermodel

def Fm (q : ℚ) : Matrix (Fin 2) (Fin 2) ℚ := !![q ^ 2, 0; 0, q ^ 2]
def Jm : Matrix (Fin 2) (Fin 2) ℚ := !![1, 0; 0, -1]

/-- F is the scalar q² times the identity: every eigenvalue is q². -/
theorem F_scalar (q : ℚ) : Fm q = (q ^ 2) • (1 : Matrix (Fin 2) (Fin 2) ℚ) := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [Fm]

/-- Fᵀ J F = q⁴ J -/
theorem F_similitude (q : ℚ) : Matrix.transpose (Fm q) * Jm * Fm q = (q ^ 4) • Jm := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Fm, Jm, Matrix.mul_apply, Fin.sum_univ_two] <;> ring

/-- (0,1) has J-square −1. -/
theorem J_indefinite :
    ∑ i : Fin 2, ∑ j : Fin 2, (![0, 1] : Fin 2 → ℚ) i * Jm i j * (![0, 1] : Fin 2 → ℚ) j = -1 := by
  simp [Fin.sum_univ_two, Jm]

/-- (1,0) has J-square +1: the form takes both signs. -/
theorem J_takes_both_signs :
    ∑ i : Fin 2, ∑ j : Fin 2, (![1, 0] : Fin 2 → ℚ) i * Jm i j * (![1, 0] : Fin 2 → ℚ) j = 1 := by
  simp [Fin.sum_univ_two, Jm]

end FrobeniusCountermodel

#print axioms P2xP2.hodge_codim2
#print axioms P2xP2.hodge_codim1
#print axioms P2xP2.pushforward_L2
#print axioms P2xP2.L2_pushforward
#print axioms FrobeniusCountermodel.F_similitude
