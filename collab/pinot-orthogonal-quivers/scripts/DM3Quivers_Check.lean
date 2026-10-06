/-
  DM3Quivers_Check.lean  --  kernel-checked arithmetic skeleton of the corrections in
  "Contact links of orthogonal quiver varieties" (draft v0.1), concerning Pinot, arXiv:2609.39434.

  WHAT THIS FILE CHECKS (Lean 4 core only, no Mathlib):
    * the weight bookkeeping behind the D~ rows of Pinot's Thm 1.2 (degrees of z^2, x y^2, x^(L+2), x^(n-1) y);
    * the Milnor-Orlik numerator identity giving mu = L+3;
    * where the printed index D_{n+1} agrees with the corrected index;
    * the group orders |Gamma| of the table, and the orbifold Euler-characteristic identity
      chi(B) = 2/|Gamma-bar| for the Seifert bases of S^3/Gamma (cross-multiplied, in N).

  WHAT IT DOES *NOT* CHECK:
    * Pinot's Remark 2.15 at zeta = 0 (that M_d is the sigma-fixed locus of the classical quiver variety).
      That is a statement in algebraic geometry, far outside this file; Nakajima (arXiv:2510.13007) treats
      only the smooth, generic-zeta case.  Conjecture 3.5 of the draft depends on it and stays unproved.
    * That the surface is Kleinian / weighted-homogeneous with the stated generators (hypotheses of Prop 3.2).
-/
namespace DM3Quivers

/-- path-length weights of the generators x = det C3, y = tr(C1C2), z = tr(C1C2C3) -/
def wx : Nat := 4
def wy (L : Nat) : Nat := 2 * L + 2
def wz (L : Nat) : Nat := 2 * L + 4
/-- common degree of z^2 and x y^2 -/
def deg (L : Nat) : Nat := 4 * L + 8

theorem z2_degree  (L : Nat) : 2 * wz L = deg L := by unfold wz deg; omega
theorem xy2_degree (L : Nat) : wx + 2 * wy L = deg L := by unfold wx wy deg; omega
/-- the homogeneous pure-x term is x^(L+2) -/
theorem xpow_degree (L : Nat) : (L + 2) * wx = deg L := by unfold wx deg; omega

/-- row (D~_{2n-2}, v), L = 2n-5: the printed term x^(n-1) y IS homogeneous -/
theorem v_row_homogeneous (n : Nat) (h : 3 ≤ n) :
    (n - 1) * wx + wy (2 * n - 5) = deg (2 * n - 5) := by
  unfold wx wy deg; omega

/-- row (D~_{2n-1}, a), L = 2n-4: the printed term x^(n-1) y misses the degree by exactly 2 -/
theorem a_row_printed_defect (n : Nat) (h : 3 ≤ n) :
    (n - 1) * wx + wy (2 * n - 4) + 2 = deg (2 * n - 4) := by
  unfold wx wy deg; omega

theorem a_row_printed_inhomogeneous (n : Nat) (h : 3 ≤ n) :
    (n - 1) * wx + wy (2 * n - 4) ≠ deg (2 * n - 4) := by
  unfold wx wy deg; omega

/-- ... while x^(L+2) = x^(2n-2) has the right degree in that row -/
theorem a_row_corrected_homogeneous (n : Nat) (h : 3 ≤ n) :
    (2 * n - 2) * wx = deg (2 * n - 4) := by
  unfold wx deg; omega

/-- the relation actually found numerically in row (D~_{2n-1}, a) contains z x^(n-1): homogeneous -/
theorem a_row_zx_term_homogeneous (n : Nat) (h : 3 ≤ n) :
    (n - 1) * wx + wz (2 * n - 4) = deg (2 * n - 4) := by
  unfold wx wz deg; omega

/-- Milnor-Orlik: mu = prod (d/w_i - 1) = (L+3).  Cross-multiplied in N:
    (d-w_x)(d-w_y)(d-w_z) = (L+3) * w_x w_y w_z . -/
theorem milnor_orlik_numerator (L : Nat) :
    (deg L - wx) * (deg L - wy L) * (deg L - wz L) = (L + 3) * (wx * wy L * wz L) := by
  have h1 : deg L - wx = 4 * L + 4 := by unfold deg wx; omega
  have h2 : deg L - wy L = 2 * L + 6 := by unfold deg wy; omega
  have h3 : deg L - wz L = 2 * L + 4 := by unfold deg wz; omega
  rw [h1, h2, h3]; unfold wx wy wz; grind

/-- Kleinian type index forced by the weights, in each D~ row -/
theorem v_row_type (n : Nat) (h : 3 ≤ n) : (2 * n - 5) + 3 = 2 * n - 2 := by omega
theorem a_row_type (n : Nat) (h : 3 ≤ n) : (2 * n - 4) + 3 = 2 * n - 1 := by omega

/-- the printed index D_{n+1} agrees with the corrected one only at n = 3 (row v) ... -/
theorem v_row_printed_agrees_iff (n : Nat) (h : 3 ≤ n) : n + 1 = 2 * n - 2 ↔ n = 3 := by omega
/-- ... and never for n >= 3 (row a) -/
theorem a_row_printed_never_agrees (n : Nat) (h : 3 ≤ n) : n + 1 ≠ 2 * n - 1 := by omega

/-! ### group orders: |BD| of D_m is 4(m-2) -/
def bdOrder (m : Nat) : Nat := 4 * (m - 2)
theorem order_v_row (n : Nat) (h : 3 ≤ n) : bdOrder (2 * n - 2) = 8 * (n - 2) := by unfold bdOrder; omega
theorem order_a_row (n : Nat) (h : 3 ≤ n) : bdOrder (2 * n - 1) = 4 * (2 * n - 3) := by unfold bdOrder; omega
theorem order_c_row (n : Nat) (h : 1 ≤ n) : bdOrder (n + 2) = 4 * n := by unfold bdOrder; omega
theorem order_Q8 : bdOrder 4 = 8 := by decide

/-! ### Seifert bases of S^3/Gamma: chi_orb(B) = 2/|Gamma-bar|, cross-multiplied.
   chi(S^2(a,b)) * ab = a + b ;  chi(S^2(a,b,c)) * abc = (bc+ac+ab) - abc.
   Claim  chi = 2/g   <=>   g * (chi * abc) = 2 * abc. -/
/-- cyclic, m odd: base S^2(m,m), |Gamma-bar| = m -/
theorem seifert_cyclic_odd (m : Nat) : m * (m + m) = 2 * (m * m) := by grind
/-- cyclic, m = 2j even: base S^2(j,j), |Gamma-bar| = j -/
theorem seifert_cyclic_even (j : Nat) : j * (j + j) = 2 * (j * j) := by grind
/-- binary dihedral of order 4k: base S^2(2,2,k), |Gamma-bar| = 2k;
    (bc+ac+ab) - abc = 4 for (a,b,c) = (2,2,k) -/
theorem seifert_prism (k : Nat) : (2 * k + 2 * k + 4) = 4 * k + 4 ∧
    2 * k * 4 = 2 * (2 * 2 * k) := by
  constructor <;> grind

end DM3Quivers

#print axioms DM3Quivers.milnor_orlik_numerator
#print axioms DM3Quivers.a_row_printed_inhomogeneous
#print axioms DM3Quivers.seifert_prism
