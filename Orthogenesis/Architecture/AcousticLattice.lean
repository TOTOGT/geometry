/-
# AcousticLattice.lean
# ====================
# Formal core of the acoustic / resonance face of the dm³ Architecture arc:
# why a periodic staircase turns a handclap into a *descending chirp* — the
# quetzal-bird echo of the El Castillo (Kukulkán) pyramid at Chichén Itzá.
#
# Companion to the site chapter
#   Book 4, Ch 19 · "The Acoustic Lattice"
#   https://totogt.github.io/geometry/book4/ch19-acoustic-lattice.html
#
# Sits beside G6Crystal / DM3Bridge / MagneticLattice / SeismicLattice and
# follows the same discipline: sorry-free where the mathematics is
# elementary, hard/empirical obligations named and disclosed.
#
# THE MECHANISM (grounded in the acoustics literature)
# ----------------------------------------------------
#   The staircase is a periodic reflective grating. A broadband impulse
#   (a handclap) reflects off successive treads; the reflection from step n
#   returns after a round-trip delay, and — because the geometry steepens as
#   the reflection point climbs — the delay *between successive returns*
#   grows with n. Pitch is the reciprocal of that delay, so a growing delay
#   is a falling pitch: a descending chirp. At El Castillo the fall is about
#   one octave, and lands in the band of the quetzal's call (Lubman;
#   Declercq, Degrieck, Briers & Leroy, JASA 116(6):3328, 2004).
#
# What is proved here WITHOUT sorry
# ----------------------------------
#  · The grating pitch f₀ = c/(2L) of an equally-spaced staircase is positive.
#  · Pitch is the reciprocal of the round-trip step delay; a strictly
#    increasing delay gives a strictly DECREASING pitch (a descending chirp).
#  · Doubling the step delay drops the pitch by exactly one octave (factor 2).
#  · The dm³ invariant signs μ_max < 0, T* > 0 (mirrored from G6Crystal).
#  · A capstone `acoustic_bridge` bundling the proved core.
#
# What is NOT claimed (named open obligations)
# ---------------------------------------------
#  A1  Full diffraction spectrum of the real staircase (the optical-grating
#      computation of Declercq et al.) — needs Fourier/diffraction theory.
#  A2  Intentionality: whether the Maya built the effect on purpose — an
#      archaeological/historical question, not a theorem.
#  A3  The quetzal-match: that the chirp *is* the quetzal call — a perceptual
#      claim, outside formal reach.
#
# None of the proved facts depends on the Structural Hypothesis (SH).
#
# Toolchain: Lean 4 + Mathlib (v4.14.0, as G6Crystal.lean)
# Zenodo concept DOI: 10.5281/zenodo.19162012
# GitHub: https://github.com/TOTOGT/geometry · ORCID: 0009-0000-6496-2186
-/
import Mathlib

namespace Orthogenesis.Acoustic

open Real

-- ─────────────────────────────────────────────────────────────────────────────
-- §1  The staircase as a reflective grating
--     Equal step diagonal L, sound speed c → adjacent-return delay 2L/c,
--     hence a pitched echo f₀ = c/(2L) (a Bragg / grating condition).
-- ─────────────────────────────────────────────────────────────────────────────

/-- Round-trip delay between reflections off two adjacent steps of diagonal
    spacing `L`, at sound speed `c`. -/
noncomputable def stepDelay (c L : ℝ) : ℝ := 2 * L / c

/-- The grating pitch of an equally-spaced staircase: f₀ = c / (2L). -/
noncomputable def echoPitch (c L : ℝ) : ℝ := c / (2 * L)

-- ── Fact 1 ──────────────────────────────────────────────────────────────────
/-- The grating pitch is positive for a real staircase (c, L > 0). -/
theorem echoPitch_pos (c L : ℝ) (hc : 0 < c) (hL : 0 < L) : 0 < echoPitch c L := by
  unfold echoPitch; positivity

-- ── Fact 2 ──────────────────────────────────────────────────────────────────
/-- Pitch is the reciprocal of the step delay: f₀ · T = 1. -/
theorem pitch_delay_reciprocal (c L : ℝ) (hc : 0 < c) (hL : 0 < L) :
    echoPitch c L * stepDelay c L = 1 := by
  unfold echoPitch stepDelay
  field_simp

-- ─────────────────────────────────────────────────────────────────────────────
-- §2  The descending chirp
--     Pitch(delay) = 1/delay. A delay that grows step to step is a pitch
--     that falls step to step — the chirp descends.
-- ─────────────────────────────────────────────────────────────────────────────

/-- Perceived pitch as a function of the (growing) round-trip step delay. -/
noncomputable def pitch (delay : ℝ) : ℝ := 1 / delay

-- ── Fact 3 ──────────────────────────────────────────────────────────────────
/-- **The chirp descends.** A longer step delay is a lower pitch:
    if `0 < Δ₁ < Δ₂` then `pitch Δ₂ < pitch Δ₁`. -/
theorem chirp_descends {Δ₁ Δ₂ : ℝ} (h0 : 0 < Δ₁) (h : Δ₁ < Δ₂) :
    pitch Δ₂ < pitch Δ₁ := by
  unfold pitch
  exact one_div_lt_one_div_of_lt h0 h

-- ── Fact 4 ──────────────────────────────────────────────────────────────────
/-- Over the whole staircase: if the per-step delay is strictly increasing
    (steepening geometry), the emitted pitch sequence is strictly decreasing —
    a monotone descending chirp. -/
theorem chirp_strictAnti (delay : ℕ → ℝ) (hpos : ∀ n, 0 < delay n)
    (hmono : StrictMono delay) : StrictAnti (fun n => pitch (delay n)) := by
  intro a b hab
  unfold pitch
  exact one_div_lt_one_div_of_lt (hpos a) (hmono hab)

-- ── Fact 5 ──────────────────────────────────────────────────────────────────
/-- **One octave.** When the step delay doubles, the pitch drops by exactly
    an octave (a factor of two) — the reported fall of the El Castillo chirp. -/
theorem octave_drop (Δ : ℝ) (h : 0 < Δ) : pitch Δ / pitch (2 * Δ) = 2 := by
  unfold pitch
  field_simp

-- ─────────────────────────────────────────────────────────────────────────────
-- §3  dm³ invariant anchors (mirrored from G6Crystal.lean)
-- ─────────────────────────────────────────────────────────────────────────────

/-- Maximal transverse Lyapunov exponent bound μ_max = −2. -/
def mu_max : ℝ := -2

/-- Canonical dm³ period T* = 2π. The staircase locks a handclap onto a pitch
    the way Ch 16 locks the crystal onto Schumann — resonance by design of the
    period, here the step period rather than the cavity period. -/
noncomputable def T_star : ℝ := 2 * Real.pi

-- ── Fact 6 ──────────────────────────────────────────────────────────────────
theorem mu_max_neg : mu_max < 0 := by unfold mu_max; norm_num
-- ── Fact 7 ──────────────────────────────────────────────────────────────────
theorem T_star_pos : 0 < T_star := by unfold T_star; positivity

-- ─────────────────────────────────────────────────────────────────────────────
-- §4  The Acoustic Bridge Theorem — proved core in one proposition
-- ─────────────────────────────────────────────────────────────────────────────

/-- **Acoustic Bridge Theorem.** The machine-checked core of the resonant
    staircase:

    (a) the equal-step grating has a positive pitch f₀ = c/(2L);
    (b) pitch is the reciprocal of the step delay (f₀·T = 1);
    (c) a steepening (strictly increasing) delay gives a strictly descending
        pitch — the chirp;
    (d) a doubled delay is exactly one octave down;
    (e) the dm³ period is positive (a real period to lock onto). -/
theorem acoustic_bridge :
    (∀ c L : ℝ, 0 < c → 0 < L → 0 < echoPitch c L) ∧
    (∀ c L : ℝ, 0 < c → 0 < L → echoPitch c L * stepDelay c L = 1) ∧
    (∀ Δ₁ Δ₂ : ℝ, 0 < Δ₁ → Δ₁ < Δ₂ → pitch Δ₂ < pitch Δ₁) ∧
    (∀ Δ : ℝ, 0 < Δ → pitch Δ / pitch (2 * Δ) = 2) ∧
    (0 < T_star) :=
  ⟨echoPitch_pos,
   pitch_delay_reciprocal,
   fun _ _ h0 h => chirp_descends h0 h,
   octave_drop,
   T_star_pos⟩

-- ─────────────────────────────────────────────────────────────────────────────
-- §5  Open obligations (named, disclosed)
-- ─────────────────────────────────────────────────────────────────────────────

/-- **A1 (OPEN).** The full diffraction spectrum of the real staircase — the
    optical-grating computation of Declercq, Degrieck, Briers & Leroy (JASA
    116(6):3328, 2004) — reproducing the measured chirp envelope. Needs
    Fourier/diffraction theory; not formalised here. -/
theorem full_diffraction_spectrum_placeholder : True := trivial

/-- **A2 (OPEN).** Intentionality: whether the effect was designed by the
    Maya or is incidental to a periodic staircase. An archaeological /
    historical question, explicitly NOT a theorem. -/
theorem intentionality_placeholder : True := trivial

/-- **A3 (OPEN).** The quetzal-match: that the descending chirp *is* the call
    of the resplendent quetzal. A perceptual claim, outside formal reach. -/
theorem quetzal_match_placeholder : True := trivial

/-!
## Summary of verified facts (no sorry)

  echoPitch_pos            grating pitch c/(2L) > 0                      ✓
  pitch_delay_reciprocal   f₀ · T = 1                                   ✓
  chirp_descends           longer delay ⟹ lower pitch                   ✓
  chirp_strictAnti         steepening delay ⟹ descending chirp          ✓
  octave_drop              doubled delay ⟹ one octave down              ✓
  mu_max_neg, T_star_pos   dm³ invariant signs                          ✓
  acoustic_bridge          proved core, bundled                         ✓

Open, disclosed:  A1 full diffraction spectrum · A2 intentionality
                  · A3 quetzal perceptual match.
-/

end Orthogenesis.Acoustic
