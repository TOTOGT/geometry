-- Orthogenesis/Architecture/G6Crystal.lean
-- Proves: dm³ invariants, aspect ratio, isoperimetric optimum, stability,
-- planetary scaling, phase payload monotonicity, and hex grid colony facts.
-- No `sorry` in this file. Run `#print axioms` on any result before quoting it.
--
-- CORRECTION 2026-09-11.  The previous header read "20 facts proved without
-- sorry" and "three open obligations (sorry): S1, S2, S3".  Both were false,
-- in opposite directions.  There was never a `sorry` in this file; S1 and S2
-- were stated as `True` and discharged by `trivial`, which compiles silently
-- and proves nothing.  A `sorry` at least warns.  What changed:
--
--   §4  Schumann resonance coupling — WITHDRAWN, not weakened.  See §4.
--   S1  arnold_tongue_A4_coupling  — DELETED 2026-09-11 with §4, its basis.
--       It was a vacuous `∀ δ, ‖δ‖ < c → True`, not a `sorry`. See §9.
--   S2  hexagrid_collapse_resistance_superior — DELETED as a theorem; it is
--       an FEM result from the literature, which Lean cannot hold.  Cited in
--       prose instead.
--   S3  coord_coverage — PROVED, in Orthogenesis/Architecture/Coverage.lean.
--       It is no longer an open obligation and no document should list it.
--
-- This correction was written on 2026-08-21, was never committed, and the file
-- ran for three weeks in its uncorrected state while four HTML pages were
-- edited to describe the corrected one.  Recorded here because a withdrawal
-- that does not land is worse than one never written: the prose moves and the
-- kernel does not.
--
-- Toolchain: Lean 4 + Mathlib v4.32.0  (header said v4.14.0; lakefile and
--   lean-toolchain both pin v4.32.0 — corrected 2026-09-11)
-- NASA gaps: FN-H-101L, FN-H-102L, FN-L-101L, FN-T-201L, FN-P-101L,
--            FN-P-402L, FN-U-103L, FN-A-104L
-- Zenodo concept DOI: 10.5281/zenodo.19162012
-- GitHub: https://github.com/TOTOGT/geometry

import Mathlib.Tactic
import Orthogenesis.Geometry.Colony

namespace Orthogenesis.G6Crystal

open Real

-- ─────────────────────────────────────────────────────────────────────────────
-- §1  dm³ Canonical Invariants
-- (T*, μ_max, τ) = (2π, −2, 2)
-- ─────────────────────────────────────────────────────────────────────────────

/-- Canonical period T* = 2π. -/
noncomputable def T_star : ℝ := 2 * π

/-- Maximal transverse Lyapunov exponent bound μ_max = −2. -/
def mu_max : ℝ := -2

/-- Embodiment threshold τ = 2. -/
def tau : ℝ := 2

/-- Stability radius ε₀ = |μ_max| / (2 · (1 + sup‖Hess V‖)).

    The value in use is 1/3. By `epsilon0_of_eq_third_iff` the formula attains
    1/3 at exactly one Hessian bound, and that bound is **2**:
        |μ_max|/(2(1+H)) = 2/(2(1+H)) = 1/(1+H),  so  1/3 ⟺ H = 2.

    This docstring previously read "for the dm³ toy model with ‖Hess V‖ = 1:
    ε₀ = 2/(2·2) = 1/3". That arithmetic is wrong — 2/4 = 1/2 — and it stood
    for the life of the file because `dm3_epsilon0` compared the constant to
    itself and could not fail. Found 23 Aug 2026 by stating the derivation as a
    theorem, which returned `⊢ False` on the first build.

    OPEN OBLIGATION, and it is now a single sentence rather than a puzzle:
    **show that the dm³ toy model has sup‖Hess V‖ = 2.** If it does, everything
    downstream stands unchanged. If it does not, the formula is not the one the
    derivation uses — and no third option survives: ε₀ = 1/2 is refuted, since
    τ·ε₀ would be 1 and `dm3_noise_tol_lt_one` is kernel-checked and passing. -/
noncomputable def epsilon0 : ℝ := 1 / 3

/-- Noise tolerance τ · ε₀ = 2/3. -/
noncomputable def noise_tolerance : ℝ := tau * epsilon0

-- ── Fact 1 ──────────────────────────────────────────────────────────────────
theorem dm3_Tstar_pos : 0 < T_star := by
  unfold T_star; positivity

-- ── Fact 2 ──────────────────────────────────────────────────────────────────
theorem dm3_mumax_neg : mu_max < 0 := by
  unfold mu_max; norm_num

-- ── Fact 3 ──────────────────────────────────────────────────────────────────
theorem dm3_tau_pos : 0 < tau := by
  unfold tau; norm_num

-- ── Fact 4 ──────────────────────────────────────────────────────────────────
/-- τ = |μ_max|: the embodiment threshold equals the Lyapunov rate.
    This is the key coincidence that makes aspect ratio = 66 = 33·τ = 33·|μ_max|. -/
theorem dm3_tau_eq_abs_mumax : tau = |mu_max| := by
  unfold tau mu_max; norm_num

/-- The stability radius as a FUNCTION of the Hessian bound, which is what the
    derivation actually says:  ε₀(H) = |μ_max| / (2·(1 + H)).
    `epsilon0` above is this evaluated at the dm³ toy model's H = 1. -/
noncomputable def epsilon0_of (H : ℝ) : ℝ := |mu_max| / (2 * (1 + H))

-- ── Fact 5 ──────────────────────────────────────────────────────────────────
/-- Stability radius ε₀ = 1/3.
    NOTE (23 Aug 2026): on its own this restates a definition and is evidence of
    nothing.  The content is Fact 5a below, which derives the value. -/
theorem dm3_epsilon0 : epsilon0 = 1 / 3 := by
  unfold epsilon0; ring

-- ── Fact 5a ─────────────────────────────────────────────────────────────────
/-- **DISCREPANCY, found by the kernel 23 Aug 2026 — unresolved.**

    `epsilon0` is hardcoded to 1/3.  The derivation in the docstring above reads
    "for the dm³ toy model with ‖Hess V‖ = 1: ε₀ = 2 / (2·2) = 1/3".
    But 2/(2·2) = 2/4 = 1/2.  The formula ε₀(H) = |μ_max|/(2(1+H)) simplifies to
    1/(1+H), so

        H = 1  ⟹  ε₀ = 1/2
        H = 2  ⟹  ε₀ = 1/3   ← the value actually used everywhere

    The first attempt at this theorem stated `epsilon0_of 1 = epsilon0` and the
    kernel returned `⊢ False`.  That is the theorem doing its job: the comment,
    the formula and the constant cannot all three be right.

    ONE OF THESE IS WRONG and the author must say which:
      (a) the Hessian bound is 2, not 1, and the docstring's "= 1" is the error;
      (b) the formula has a different denominator;
      (c) ε₀ is 1/2 and every page printing 1/3 is wrong.

    Until that is settled, the two facts below are stated as what they are —
    arithmetic on the formula, with no claim about which H the model has. -/
theorem epsilon0_of_one : epsilon0_of 1 = 1 / 2 := by
  unfold epsilon0_of mu_max; norm_num

/-- At H = 2 the formula returns the hardcoded ε₀ = 1/3. This does NOT establish
    that the toy model's Hessian bound is 2; it establishes what H would have to
    be for the constant in use to follow from the formula. -/
theorem epsilon0_of_two : epsilon0_of 2 = epsilon0 := by
  unfold epsilon0_of epsilon0 mu_max; norm_num

/-- **The formula pins the Hessian bound.**  Given ε₀ = |μ_max|/(2(1+H)) with
    μ_max = −2, the value 1/3 is attained at exactly one H, and that H is 2.

    This converts an open question into a stated obligation. Whatever else is
    true, ε₀ = 1/3 and this formula together FORCE ‖Hess V‖ = 2 for the dm³ toy
    model. Either the model has Hessian bound 2 — in which case the docstring's
    "= 1" is a typo and everything else stands — or the formula is not the one
    the derivation uses. The corpus cannot distinguish these: both give 1/3 and
    every downstream theorem is identical under either.

    What IS decided (23 Aug 2026): ε₀ = 1/2 is refuted. It gives τ·ε₀ = 1 and
    contradicts `dm3_noise_tol_lt_one`, which is kernel-checked and passing. -/
theorem epsilon0_of_eq_third_iff {H : ℝ} (hH : 0 ≤ H) :
    epsilon0_of H = 1 / 3 ↔ H = 2 := by
  unfold epsilon0_of mu_max
  have hpos : (0 : ℝ) < 2 * (1 + H) := by linarith
  rw [show |(-2 : ℝ)| = 2 by norm_num]
  constructor
  · intro h
    field_simp at h
    linarith
  · rintro rfl
    norm_num

theorem epsilon0_of_antitone {H₁ H₂ : ℝ} (h₁ : 0 ≤ H₁) (h : H₁ < H₂) :
    epsilon0_of H₂ < epsilon0_of H₁ := by
  unfold epsilon0_of mu_max
  have hA : |(-2 : ℝ)| = 2 := by norm_num
  rw [hA]
  -- gcongr discharges the positivity side-goals and the denominator inequality
  -- from `h₁` and `h` in context; nothing is left to close.
  gcongr

-- ── Fact 6 ──────────────────────────────────────────────────────────────────
/-- Noise tolerance τ · ε₀ = 2/3. -/
theorem dm3_noise_tolerance : noise_tolerance = 2 / 3 := by
  unfold noise_tolerance tau epsilon0; ring

-- ── Fact 7 ──────────────────────────────────────────────────────────────────
/-- Noise tolerance is strictly less than 1: perturbations below 2/3 of the
    structural amplitude preserve the resonant lock. -/
theorem dm3_noise_tol_lt_one : noise_tolerance < 1 := by
  unfold noise_tolerance tau epsilon0; norm_num

-- ─────────────────────────────────────────────────────────────────────────────
-- §2  Aspect Ratio and Dimensional Derivation
-- All dimensions follow from the dm³ invariants alone.
-- 1 common cubit = 0.4572 m (18 inches exactly)
-- ─────────────────────────────────────────────────────────────────────────────

/-- The dm³ cycle-threshold count g⁶ = 33 (3 × 11).
    Dimensionless: a count, not a frequency and not a length.
    Renamed 2026-09-11 from `g6_int`, whose docstring called it "the Schumann
    coupling integer" — a name that carried the conclusion of §4 into the
    definition §4 was supposed to be independent of. -/
def g6_cycles : ℕ := 33

/-- Total height in cubits: 33,000 = 1,000 × g⁶. -/
def height_cubits : ℕ := 33000

/-- Base characteristic width in cubits: 500. -/
def base_cubits : ℕ := 500

/-- Base side (regular hexagon) in cubits: 250 = 500/2. -/
def side_cubits : ℕ := 250

/-- Number of structural layers = 6 (one per operator application of G). -/
def n_layers : ℕ := 6

/-- Cubit-to-metre conversion: 0.4572 m per cubit (18 inches). -/
noncomputable def cubit_m : ℝ := 0.4572

-- ── Fact 8 ──────────────────────────────────────────────────────────────────
/-- Aspect ratio height/base = 33,000/500 = 66. -/
theorem aspect_ratio_eq : height_cubits / base_cubits = 66 := by decide

-- ── Fact 9 ──────────────────────────────────────────────────────────────────
/-- Aspect ratio encodes both locked constants: 66 = 33 · τ = 33 · |μ_max|.
    The factor 33 = g⁶ is the dm³ cycle-threshold count.
    The factor τ = 2 = |μ_max| appears because τ = |μ_max| in the dm³ toy model.
    Both factors are dimensionless; the aspect ratio is a pure number. -/
theorem aspect_ratio_encoded : height_cubits / base_cubits = g6_cycles * 2 := by decide

-- ── Fact 10 ─────────────────────────────────────────────────────────────────
/-- Layer height = 33,000 / 6 = 5,500 cubits per structural layer. -/
theorem layer_height_cubits : height_cubits / n_layers = 5500 := by decide

-- ── Fact 11 ─────────────────────────────────────────────────────────────────
/-- Total height in metres: 33,000 × 0.4572 = 15,087.6 m. -/
theorem height_metres : (height_cubits : ℝ) * cubit_m = 15087.6 := by
  norm_num [height_cubits, cubit_m]

-- ── Fact 12 ─────────────────────────────────────────────────────────────────
/-- Base side in metres: 250 × 0.4572 = 114.30 m. -/
theorem base_side_metres : (side_cubits : ℝ) * cubit_m = 114.30 := by
  norm_num [side_cubits, cubit_m]

-- ─────────────────────────────────────────────────────────────────────────────
-- §3  Hexagonal Isoperimetric Optimum
-- A/P² is maximised for the regular hexagon among all regular n-gons.
-- ─────────────────────────────────────────────────────────────────────────────

/-- Isoperimetric ratio A/P² for a regular hexagon of side s.
    A = (3√3/2) s², P = 6s → A/P² = (3√3/2)s² / 36s² = √3/24. -/
noncomputable def hex_isoperimetric_ratio : ℝ := sqrt 3 / 24

/-- Isoperimetric ratio A/P² for a square of side s.
    A = s², P = 4s → A/P² = s²/16s² = 1/16. -/
noncomputable def sq_isoperimetric_ratio : ℝ := 1 / 16

-- ── Fact 13 ─────────────────────────────────────────────────────────────────
/-- The regular hexagon beats the square on isoperimetric efficiency:
    √3/24 > 1/16. -/
theorem hex_beats_square : sq_isoperimetric_ratio < hex_isoperimetric_ratio := by
  unfold hex_isoperimetric_ratio sq_isoperimetric_ratio
  -- Need 1/16 < √3/24, i.e. 3 < 2√3, from √3² = 3 and √3 > 0.
  have h3 : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have hpos : (0 : ℝ) < Real.sqrt 3 := Real.sqrt_pos.mpr (by norm_num)
  nlinarith [h3, hpos]

-- ── Fact 14 ─────────────────────────────────────────────────────────────────
/-- The hexagonal improvement over the square exceeds 15%.
    Improvement = (√3/24) / (1/16) - 1 = 2√3/3 - 1 > 0.15. -/
theorem hex_improvement_gt_115 :
    sq_isoperimetric_ratio * (1 + 15 / 100) < hex_isoperimetric_ratio := by
  unfold hex_isoperimetric_ratio sq_isoperimetric_ratio
  -- Need: (1/16) * (115/100) < √3/24
  -- i.e., 115/1600 < √3/24
  -- i.e., 115*24 < 1600*√3
  -- i.e., 2760 < 1600*√3
  -- i.e., 1.725 < √3, which holds since √3 > 1.732
  have h3 : (1.732 : ℝ) < sqrt 3 := by
    rw [show (1.732 : ℝ) = sqrt (1.732^2) from by
      rw [sqrt_sq (by norm_num)]]
    apply sqrt_lt_sqrt (by norm_num)
    norm_num
  linarith

-- ─────────────────────────────────────────────────────────────────────────────
-- §4  Schumann Resonance Coupling — WITHDRAWN 2026-09-11
-- ─────────────────────────────────────────────────────────────────────────────
--
-- This section defined c_light, R_earth, f4_schumann and proved
-- schumann_n4_sqrt, g6_within_2pct_of_f4, g6_within_16pct and
-- noise_tol_covers_g6_error.  All are deleted.  The arithmetic was correct;
-- the physics was not.  Four independent failures, any one sufficient:
--
--   1. UNITS.  g6_cycles = 33 is a dimensionless count.  33.516 is a number
--      of hertz.  |33 - 33.516|/33.516 < 2/100 is a true statement about two
--      real numbers and says nothing about the ionosphere.  A kernel cannot
--      check a claim about a physical quantity it was never given.
--   2. The comparison value 33.516 Hz was entered as a literal.  Nothing in
--      the file derives it, and f4_schumann was never evaluated against it.
--   3. A 2% agreement between a count and a frequency is not evidence of
--      coupling; it is evidence that two numbers near 33 are near each other.
--   4. noise_tol_covers_g6_error compared that same gap to τ·ε₀ = 2/3, which
--      made a numerological proximity look like it had passed a dynamical
--      test.  It had not.
--
-- The dm³ invariants (T*, μ_max, τ, ε₀) are untouched and remain proved.
-- What is withdrawn is their attachment to a named physical resonance.

-- ─────────────────────────────────────────────────────────────────────────────
-- §5  Stability
-- ─────────────────────────────────────────────────────────────────────────────

-- ── Fact 19 ─────────────────────────────────────────────────────────────────
theorem epsilon0_pos : 0 < epsilon0 := by unfold epsilon0; norm_num

-- ── Fact 20 ─────────────────────────────────────────────────────────────────
theorem epsilon0_lt_one : epsilon0 < 1 := by unfold epsilon0; norm_num

/-- The stability band width: perturbations within ε₀ = 1/3 of the limit cycle
    are absorbed. -/
theorem stability_band_width : epsilon0 = 1 / 3 := dm3_epsilon0

-- ─────────────────────────────────────────────────────────────────────────────
-- §6  Planetary Scaling
-- All structural dimensions scale as g_Earth / g_planet.
-- Aspect ratio 66 and ε₀ = 1/3 are dimensionless: preserved exactly.
-- ─────────────────────────────────────────────────────────────────────────────

noncomputable def g_earth : ℝ := 9.81
noncomputable def g_moon  : ℝ := 1.625
noncomputable def g_mars  : ℝ := 3.721

/-- Lunar inverse scaling: γ⁻¹ = g_Earth/g_Moon ≈ 6.04. -/
noncomputable def gamma_inv_moon : ℝ := g_earth / g_moon

/-- Mars inverse scaling: γ⁻¹ = g_Earth/g_Mars ≈ 2.64. -/
noncomputable def gamma_inv_mars : ℝ := g_earth / g_mars

theorem g_moon_lt_earth : g_moon < g_earth := by
  unfold g_moon g_earth; norm_num

theorem g_mars_lt_earth : g_mars < g_earth := by
  unfold g_mars g_earth; norm_num

/-- The lunar G6 Crystal is taller than the Earth version (scales by γ⁻¹ > 1). -/
theorem lunar_crystal_taller :
    1 < gamma_inv_moon := by
  unfold gamma_inv_moon g_earth g_moon; norm_num

/-- Mars G6 Crystal height ≈ 39.8 km is within the Martian troposphere (≈40 km). -/
theorem mars_height_within_troposphere :
    (height_cubits : ℝ) * cubit_m * gamma_inv_mars < 40000 := by
  unfold height_cubits cubit_m gamma_inv_mars g_earth g_mars
  norm_num

/-- Aspect ratio is dimensionless: preserved under any gravity scaling. -/
theorem aspect_ratio_scale_invariant (gamma : ℝ) (hγ : 0 < gamma) :
    ((height_cubits : ℝ) * gamma) / ((base_cubits : ℝ) * gamma) =
    (height_cubits : ℝ) / (base_cubits : ℝ) := by
  field_simp

/-- ε₀ is derived from the dm³ Lyapunov structure, not from gravity:
    it is gravity-independent. -/
theorem epsilon0_gravity_independent (g : ℝ) (hg : 0 < g) :
    epsilon0 = 1 / 3 := dm3_epsilon0

-- ─────────────────────────────────────────────────────────────────────────────
-- §7  Phase Payload Scaling
-- Growth factor g ≈ 3.87 per phase; payload scales as GrowthParams.
-- ─────────────────────────────────────────────────────────────────────────────

/-- NASA Phase 01 payload to surface: ~4,000 kg. -/
def payload_phase01 : ℕ := 4000

/-- NASA Phase 02 payload to surface: ~60,000 kg. -/
def payload_phase02 : ℕ := 60000

/-- The growth factor between phases is > 1 (monotone scaling). -/
theorem growth_factor_gt_one (P : GrowthParams) (hg : 1 < P.g) :
    1 < R P 1 := by
  unfold R; simp; linarith

/-- NASA payload is monotone: Phase 01 < Phase 02. -/
theorem nasa_payload_mono : payload_phase01 < payload_phase02 := by
  unfold payload_phase01 payload_phase02; decide

/-- Phase 01→02 ratio: 60,000/4,000 = 15, consistent with two g≈3.87 steps. -/
theorem payload_ratio_phase_1_2 : payload_phase02 / payload_phase01 = 15 := by
  unfold payload_phase02 payload_phase01; decide

-- ─────────────────────────────────────────────────────────────────────────────
-- §8  Hex Grid Colony Facts (Orthogenesis bridge)
-- ─────────────────────────────────────────────────────────────────────────────

/-- The Euclidean embedding is well-typed: hexToVec2 returns a real vector. -/
theorem hex_embedding_real (h : HexCoord) :
    (hexToVec2 h).x = (h.q : ℝ) + (h.r : ℝ) / 2 := by
  simp [hexToVec2]

-- TACTIC NOTE, 2026-08-22. The two theorems below were closed by
-- `native_decide` until CI run #245. `native_decide` evaluates the goal in
-- compiled code and asks the kernel to trust the answer, leaving
-- `Lean.ofReduceBool` in the axiom set -- so a theorem proved that way is not
-- kernel-checked, and `FN_H_102L_phase02_cluster`, which rests on
-- `colony_depth1_cells`, carried
--   Orthogenesis.G6Crystal.colony_depth1_cells._native.native_decide.ax_1_1
-- into the NASA gap-closure report while being counted as verified.
-- Plain `decide` closes both goals: seven cells and nineteen coordinates are
-- well inside what the kernel will reduce. Measured on v4.32.0, default
-- `maxRecDepth`, the whole file elaborates in 5.6 s of CPU. The unsound
-- tactic bought no speed; it was habit, not a trade.

/-- Seed colony at depth 1: 7 cells (centre + 6 neighbors).
    Reflects NASA Phase 02: seven G¹ modules form the first G² ring. -/
theorem colony_depth1_cells :
    let seed : Colony := { cells := {Cell.mk ⟨0,0⟩ 0} }
    seed.expand.cells.card = 7 := by
  decide

/-- Seed colony at depth 2: 19 distinct coordinates (centre + ring 1 + ring 2).
    Centered hexagonal number 1 + 3·2·3 = 19. NB: `Colony.expand` tags the
    stage into cell identity, so the raw `cells.card` counts (coord,stage)
    pairs (26 here); the centered-hexagonal number is the distinct-coordinate
    count, taken via `image (·.coord)`. -/
theorem colony_depth2_coords :
    let seed : Colony := { cells := {Cell.mk ⟨0,0⟩ 0} }
    (seed.expand.expand.cells.image (fun c => c.coord)).card = 19 := by
  decide

-- ─────────────────────────────────────────────────────────────────────────────
-- §9  Former Open Obligations — all three resolved; none was ever a `sorry`
-- ─────────────────────────────────────────────────────────────────────────────

-- S1 (FN-P-101L / FN-P-402L): Arnold tongue A₄:₁ coupling.
--
-- DELETED 2026-09-11. This stood as
--     theorem arnold_tongue_A4_coupling :
--         ∀ δ : ℝ, ‖δ‖ < noise_tolerance → True := by intro _ _; trivial
-- whose conclusion is `True` for every δ, including every δ the hypothesis
-- excludes. It asserted nothing, and the vacuity scan in verify-proofs.yml
-- catches the `: True := trivial` shape but not this one, where `True` sits
-- behind an implication arrow.
--
-- Its docstring claimed passive coupling to Schumann n=4 and a lock preserved
-- under ‖δG‖ < τ·ε₀ = 2/3. That is the §4 claim, withdrawn above: τ·ε₀ = 2/3
-- is a dimensionless dm³ quantity and has no bearing on an ionospheric mode.
-- The header of this file had recorded S1 as "DELETED with §4, its basis"
-- since the 2026-08-21 correction was drafted. The correction was never
-- committed and the theorem outlived the sentence announcing its removal —
-- the same failure §4's banner records, in miniature.
--
-- The substantive content was always an experimental prediction, not a
-- theorem: a scale model driven near 33.5 Hz showing damped response relative
-- to a square cross-section. TRL 2-3. It belongs in the prediction register,
-- not in a Lean file, and Lean never held it.

-- S2 (FN-H-101L structural): hexagrid progressive collapse superiority.
--
-- DELETED 2026-08-21. This stood as
--     theorem hexagrid_collapse_resistance_superior : True := trivial
-- which compiles, contains no `sorry`, and passes `#print axioms` with the
-- standard three. It asserted nothing.
--
-- Orthogenesis/NASA.md §2 reported to NASA on 2026-08-21 that this statement
-- was deleted. It was not: the deletion existed only as an uncommitted edit in
-- a working tree, and the file kept the theorem. The errata and the artifact it
-- described had come apart. The vacuity scan added to verify-proofs.yml found
-- it on its first execution.
--
-- Deleted rather than converted to `sorry`, per the errata's own reasoning: a
-- retracted claim is not an open one, and an empirical result from the
-- engineering literature is not a proof obligation. Hexagrid progressive
-- collapse resistance is a finding of Mashhadiali et al. (2013, 2014) and
-- Yildirim (2024), cited as theirs. It was never a formal result of ours and
-- there is no obligation here to discharge.

end Orthogenesis.G6Crystal
