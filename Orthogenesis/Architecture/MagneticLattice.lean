-- GATE-DECLARE: sorries = Orthogenesis.Magnetism.heliSpin_incommensurate_aperiodic
-- GATE-REASON: M2 in the repository README's Open Obligations table. Needs irrationality of q/2pi plus a Weyl equidistribution argument.
/-
# MagneticLattice.lean
# =====================
# Formal bridge between magnetic crystallography (Shubnikov / magnetic
# space-group symmetry, time-reversal 1', collinear and helical spin
# order) and the dm³ contact framework of the Principia Orthogona series.
#
# Companion to the site chapter
#   Book 4, Ch 17 · "The Magnetic Lattice"
#   https://totogt.github.io/geometry/book4/ch17-magnetic-lattice.html
#
# This file sits beside G6Crystal.lean and DM3Bridge.lean and follows the
# same discipline: sorry-free where the mathematics is elementary, with the
# genuinely hard obligations left as *named, disclosed* placeholders rather
# than hidden or axiomatised away.
#
# CENTRAL BRIDGE (proved, no sorry)
# ---------------------------------
#   Every helimagnetic spin  Sₙ = (cos nq, sin nq)  has unit length, i.e.
#   lies on the unit circle {r = 1} of the spin plane, and a helimagnet whose
#   pitch closes after p sites (p·q = 2π) is exactly p-periodic.
#   [Corrected 2026-11-14: earlier text here said this "lies on the dm³ limit
#   cycle" and that a helimagnet "is, literally, the dm³ helical attractor".
#   What is proved is the identity cos² + sin² = 1 for a vector defined as
#   (cos nq, sin nq), and the 2π-periodicity of cos and sin.  This file
#   contains no dm³ vector field, flow or attraction; the match of the unit
#   circle with Γ = {r = 1}, of q with θ̇ = 1 and of 2π with T* is an
#   analogy of notation, not a theorem here.]
#
# What is proved here WITHOUT sorry
# ----------------------------------
#  · The Shubnikov census sums correctly: 230 + 230 + 1191 = 1651 magnetic
#    (Shubnikov) space groups; 32 + 32 + 58 = 122 magnetic point groups.
#  · Time-reversal 1' is an involution whose only fixed point is the zero
#    (paramagnetic / grey-group) moment; ordered magnets break 1'.
#  · Collinear order: the ferromagnet has period 1, the antiferromagnet
#    period 2 with a neutral magnetic cell — doubling the chemical cell.
#  · Helical spins have unit length (the unit circle {r=1} of the spin plane);
#    the ferromagnet is the zero-pitch helix; a pitch closing after p sites
#    (p·q = 2π) gives p-periodicity.
#  · Arithmetic on two constants defined in this file, mu_max := −2 < 0 and
#    T_star := 2π > 0 (mirrored from G6Crystal).  These are not statements
#    about the dm³ system.
#  · A capstone `magnetic_bridge` bundling the proved correspondence.
#
# What is NOT claimed (named open obligations)
# ---------------------------------------------
#  M1  Kramers degeneracy T² = −1 for spin-½ (needs the projective / SU(2)
#      representation of time reversal, not the ℤ-model used here).
#  M2  Incommensurate helimagnet is aperiodic and equidistributes on Γ
#      (needs Weyl equidistribution / irrationality of q/2π).  Stated as a
#      real proposition and left as an explicit `sorry`.
#  M3  Neutron magnetic structure-factor selection rule (needs the Fourier
#      transform of the moment density; scattering theory).
#
# None of the proved facts depends on the Structural Hypothesis (SH);
# none carries the "(under SH)" caveat.
#
# Toolchain: Lean 4 + Mathlib (v4.14.0, as G6Crystal.lean)
# Zenodo concept DOI: 10.5281/zenodo.19162012
# GitHub: https://github.com/TOTOGT/geometry
# ORCID:  0009-0000-6496-2186
-/
import Mathlib.Tactic

namespace Orthogenesis.Magnetism

open Real

-- ─────────────────────────────────────────────────────────────────────────────
-- §1  The Shubnikov census
--     230 space groups → 1651 magnetic space groups (Belov–Neronova–Smirnova):
--     type I (colourless) 230 + type II (grey) 230 + type III/IV (b-w) 1191.
-- ─────────────────────────────────────────────────────────────────────────────

/-- The 230 ordinary crystallographic space groups. -/
def n_space_groups : ℕ := 230

/-- The 1651 Shubnikov (magnetic) space groups. -/
def n_magnetic_space_groups : ℕ := 1651

/-- The 122 magnetic point groups (Heesch–Shubnikov). -/
def n_magnetic_point_groups : ℕ := 122

-- ── Fact 1 ──────────────────────────────────────────────────────────────────
/-- The magnetic space-group census sums correctly:
    230 (colourless) + 230 (grey) + 1191 (black-white) = 1651. -/
theorem shubnikov_census : 230 + 230 + 1191 = n_magnetic_space_groups := by
  unfold n_magnetic_space_groups; norm_num

-- ── Fact 2 ──────────────────────────────────────────────────────────────────
/-- The magnetic point-group census: 32 + 32 + 58 = 122. -/
theorem magnetic_point_census : 32 + 32 + 58 = n_magnetic_point_groups := by
  unfold n_magnetic_point_groups; norm_num

-- ── Fact 3 ──────────────────────────────────────────────────────────────────
/-- The grey (type II) groups number exactly the 230 ordinary space groups:
    each colourless group paired with the pure time-reversal 1'. -/
theorem grey_groups_eq_space_groups : (230 : ℕ) = n_space_groups := rfl

-- ── Fact 4 ──────────────────────────────────────────────────────────────────
/-- Admitting magnetic order more than septuples the symmetry census. -/
theorem magnetic_exceeds_ordinary :
    n_space_groups < n_magnetic_space_groups := by
  unfold n_space_groups n_magnetic_space_groups; norm_num

-- ─────────────────────────────────────────────────────────────────────────────
-- §2  Time reversal 1'
--     The primed generator flips a moment.  (Analogy, not proved here: the
--     dm³ temporal operator under t ↦ −t reverses a vector field, whereas 1'
--     is an antiunitary operation on spin states; no map between them is
--     constructed in this file.)
-- ─────────────────────────────────────────────────────────────────────────────

/-- Time reversal acting on a (scalar) magnetic moment: 1' : s ↦ −s. -/
def timeReversal (s : ℤ) : ℤ := -s

-- ── Fact 5 ──────────────────────────────────────────────────────────────────
/-- 1' is an involution: applying time reversal twice is the identity. -/
theorem tr_involution (s : ℤ) : timeReversal (timeReversal s) = s := by
  simp [timeReversal]

-- ── Fact 6 ──────────────────────────────────────────────────────────────────
/-- The only time-reversal-invariant moment is zero: the paramagnetic /
    grey-group fixed point. Ordered magnets break 1' (black-white groups). -/
theorem tr_fixed_iff_zero (s : ℤ) : timeReversal s = s ↔ s = 0 := by
  unfold timeReversal; omega

-- ─────────────────────────────────────────────────────────────────────────────
-- §3  Collinear order — ferromagnet vs antiferromagnet
-- ─────────────────────────────────────────────────────────────────────────────

/-- Ferromagnetic sublattice: every site carries the same moment +1. -/
def ferroSpin (_ : ℕ) : ℤ := 1

/-- Antiferromagnetic sublattice: alternating ±1 by site parity. -/
def afmSpin (i : ℕ) : ℤ := (-1) ^ i

-- ── Fact 7 ──────────────────────────────────────────────────────────────────
/-- The ferromagnet has magnetic period 1 — its cell equals the chemical cell. -/
theorem ferro_period_one (i : ℕ) : ferroSpin (i + 1) = ferroSpin i := rfl

-- ── Fact 8 ──────────────────────────────────────────────────────────────────
/-- The antiferromagnet has magnetic period 2: the magnetic cell doubles the
    chemical cell — the discrete "unit-cell doubling" of AFM order. -/
theorem afm_period_two (i : ℕ) : afmSpin (i + 2) = afmSpin i := by
  simp only [afmSpin, pow_add]; ring

-- ── Fact 9 ──────────────────────────────────────────────────────────────────
/-- Antiferromagnetic order flips the moment site to site. -/
theorem afm_flips (i : ℕ) : afmSpin (i + 1) = - afmSpin i := by
  simp only [afmSpin, pow_succ]; ring

-- ── Fact 10 ─────────────────────────────────────────────────────────────────
/-- The two-site antiferromagnetic cell is neutral: net moment 0.
    This is why X-rays (blind to the ±1 alternation) see no extra periodicity
    while neutrons do. -/
theorem afm_cell_neutral : afmSpin 0 + afmSpin 1 = 0 := by norm_num [afmSpin]

-- ── Fact 11 ─────────────────────────────────────────────────────────────────
/-- The ferromagnetic cell carries a net moment (here 2 over two sites). -/
theorem ferro_cell_moment : ferroSpin 0 + ferroSpin 1 = 2 := by norm_num [ferroSpin]

-- ─────────────────────────────────────────────────────────────────────────────
-- §4  Helical order — the unit circle of the spin plane
--     Sₙ = (cos nq, sin nq).  The match with the dm³ limit cycle is notation.
-- ─────────────────────────────────────────────────────────────────────────────

/-- A helimagnetic spin at site `n` with pitch angle `q`. -/
noncomputable def heliSpin (q : ℝ) (n : ℤ) : ℝ × ℝ :=
  (Real.cos ((n : ℝ) * q), Real.sin ((n : ℝ) * q))

-- ── Fact 12 ─────────────────────────────────────────────────────────────────
/-- **Unit length of a helimagnetic spin.** ‖Sₙ‖² = cos²(nq) + sin²(nq) = 1,
    so every spin lies on the unit circle {r = 1} of the spin plane.  This is
    the Pythagorean identity for a vector defined as (cos nq, sin nq); it is
    unit length by definition.  It is NOT a statement about the dm³ limit
    cycle Γ or about attraction: this file has no dm³ dynamics.  (The name
    `heliSpin_on_limit_cycle` is kept so that the audit receipt and page
    references still resolve.) -/
theorem heliSpin_on_limit_cycle (q : ℝ) (n : ℤ) :
    (heliSpin q n).1 ^ 2 + (heliSpin q n).2 ^ 2 = 1 := by
  simp only [heliSpin]
  exact Real.cos_sq_add_sin_sq _

-- ── Fact 13 ─────────────────────────────────────────────────────────────────
/-- The ferromagnet is the zero-pitch helix: all spins parallel to (1,0).
    Ferromagnetism is the q → 0 degeneration of the helical family. -/
theorem ferromagnet_is_zero_pitch (n : ℤ) : heliSpin 0 n = (1, 0) := by
  simp [heliSpin]

-- ── Fact 14 ─────────────────────────────────────────────────────────────────
/-- **Commensurate lock.** If the pitch closes after `p` sites — i.e. `p·q = 2π`
    — the helimagnet is exactly `p`-periodic.  The proof is the 2π-periodicity
    of cos and sin; `T* = 2π` is the same number, and no dm³ period enters the
    argument. -/
theorem heliSpin_period (q : ℝ) (n p : ℤ) (h : (p : ℝ) * q = 2 * Real.pi) :
    heliSpin q (n + p) = heliSpin q n := by
  simp only [heliSpin, Int.cast_add, add_mul, h]
  rw [Real.cos_add_two_pi, Real.sin_add_two_pi]

-- ─────────────────────────────────────────────────────────────────────────────
-- §5  dm³ invariant anchors (mirrored from G6Crystal.lean)
-- ─────────────────────────────────────────────────────────────────────────────

/-- The constant −2.  In the dm³ system the radial exponent at r = 1 is
    2·e^(−z) − 2, which tends to −2 only as z → ∞ (it is 0 at z = 0); this
    definition records the limiting value as a bare real number and is not
    connected to the vector field here.  Under t ↦ −t the exponents of a flow
    change sign; the identification of that with the magnetic 1' is an
    analogy, not proved in this file. -/
def mu_max : ℝ := -2

/-- The constant 2π (the dm³ period T* is 2π; the definition is just the real
    number 2π). -/
noncomputable def T_star : ℝ := 2 * Real.pi

-- ── Fact 15 ─────────────────────────────────────────────────────────────────
theorem mu_max_neg : mu_max < 0 := by unfold mu_max; norm_num

-- ── Fact 16 ─────────────────────────────────────────────────────────────────
theorem T_star_pos : 0 < T_star := by unfold T_star; positivity

-- ─────────────────────────────────────────────────────────────────────────────
-- §6  The Magnetic Bridge Theorem — proved core in one proposition
-- ─────────────────────────────────────────────────────────────────────────────

/-- **Magnetic Bridge Theorem.** The machine-checked core of the
    magnetism ↔ dm³ correspondence:

    (a) helimagnetic spins live on Γ = {r = 1};
    (b) the ferromagnet is the zero-pitch helix;
    (c) a pitch closing after `p` sites (p·q = T* = 2π) gives `p`-periodicity;
    (d) time reversal 1' is an involution fixing only the zero moment;
    (e) the antiferromagnetic cell is neutral and period-2. -/
theorem magnetic_bridge :
    (∀ q : ℝ, ∀ n : ℤ, (heliSpin q n).1 ^ 2 + (heliSpin q n).2 ^ 2 = 1) ∧
    (∀ n : ℤ, heliSpin 0 n = (1, 0)) ∧
    (∀ q : ℝ, ∀ n p : ℤ, (p : ℝ) * q = 2 * Real.pi →
        heliSpin q (n + p) = heliSpin q n) ∧
    (∀ s : ℤ, timeReversal (timeReversal s) = s ∧ (timeReversal s = s ↔ s = 0)) ∧
    (afmSpin 0 + afmSpin 1 = 0 ∧ ∀ i, afmSpin (i + 2) = afmSpin i) :=
  ⟨heliSpin_on_limit_cycle,
   ferromagnet_is_zero_pitch,
   fun q n p h => heliSpin_period q n p h,
   fun s => ⟨tr_involution s, tr_fixed_iff_zero s⟩,
   ⟨afm_cell_neutral, afm_period_two⟩⟩

-- ─────────────────────────────────────────────────────────────────────────────
-- §7  Open obligations (named, disclosed)
-- ─────────────────────────────────────────────────────────────────────────────

/-- **M2 (OPEN).** If the pitch is incommensurate — `q / 2π` irrational —
    then no nonzero period exists: the helimagnet is aperiodic (and, in the
    full statement, equidistributes on Γ by Weyl's theorem). The proposition
    is stated honestly and left as an explicit `sorry`; closing it requires
    the irrationality of `q/(2π)` and an equidistribution argument. -/
theorem heliSpin_incommensurate_aperiodic
    (q : ℝ) (hirr : Irrational (q / (2 * Real.pi))) (p : ℤ) (hp : p ≠ 0) :
    ∃ n : ℤ, heliSpin q (n + p) ≠ heliSpin q n := by
  sorry

/-- **M1 (OPEN).** Kramers degeneracy: for a spin-½ system time reversal
    squares to −1 (T² = −1), forcing double degeneracy of every level. The
    faithful statement needs the projective/SU(2) representation of time
    reversal, outside the scalar ℤ-model of §2. Tracked as an open obligation;
    the substantive content is the antiunitary T with T² = −𝟙. -/
theorem kramers_degeneracy_placeholder :
    ∀ s : ℤ, timeReversal (timeReversal s) = s := tr_involution
-- Note: the scalar model gives T² = +1; the true spin-½ claim T² = −1 is the
-- open obligation and is NOT captured by the ℤ-model above.

/-- **M3 (OPEN).** Neutron magnetic structure-factor selection rule: the
    magnetic Bragg intensity is |F_M(k)|² with F_M the Fourier transform of
    the moment density, vanishing where the chemical-cell periodicity alone
    would predict a peak. Requires scattering theory; not formalised here. -/
theorem neutron_selection_rule_placeholder : True := trivial
-- Note: the statement is literally `True`; the axiom receipt for this name
-- reads "no axioms" and certifies nothing about neutron scattering.

/-!
## Summary of verified facts (no sorry)

  shubnikov_census            230+230+1191 = 1651 magnetic space groups   ✓
  magnetic_point_census       32+32+58 = 122 magnetic point groups        ✓
  magnetic_exceeds_ordinary   230 < 1651                                  ✓
  tr_involution               1' ∘ 1' = id                                ✓
  tr_fixed_iff_zero           1'-invariant ⟺ zero moment (paramagnet)     ✓
  ferro_period_one            ferromagnet period 1                        ✓
  afm_period_two              antiferromagnet period 2 (cell doubling)    ✓
  afm_flips                   AFM flips site to site                      ✓
  afm_cell_neutral            AFM cell net moment 0                       ✓
  heliSpin_on_limit_cycle     helical spins have unit length (cos²+sin²=1) ✓
  ferromagnet_is_zero_pitch   ferromagnet = zero-pitch helix              ✓
  heliSpin_period             p·q = 2π ⟹ p-periodic                       ✓
  mu_max_neg, T_star_pos      −2 < 0 and 0 < 2π for two defined constants ✓
  magnetic_bridge             proved core, bundled                        ✓

Open, disclosed:  M1 Kramers T²=−1 · M2 incommensurate aperiodicity (sorry)
                  · M3 neutron structure-factor selection rule.
-/

end Orthogenesis.Magnetism
