/-
  Codifying the Cosmos — Maya Calendar Mathematics in Lean 4
  Principia Orthogona · Vol VI · Pablo Nogueira Grossi · G6 LLC · 2026

  STATUS: The arithmetic below is independently verified (Python `math.lcm`,
          exact-integer). The Lean proofs are written to be sound but have
          NOT yet been run through the kernel (compilation deferred until
          Mathlib build resources are available). Do not cite as machine-checked
          until `lake build` passes.

  The four-cycle grand alignment is lcm(260,365,584,780) = 113,880 days
  = 6 Calendar Rounds = 312 years. Because 780 = 3 × 260, adjoining Mars to
  the Tzolk'in/Haab'/Venus window (37,960 days) only multiplies it by 3.
-/
import Mathlib.Data.ZMod.Basic
import Mathlib.Algebra.GCDMonoid.Basic

namespace Maya

/-- The four periods Sak Tahn Waax co-indexed (in days). -/
def tzolkin : ℕ := 260   -- ritual round (13 × 20)
def haab    : ℕ := 365   -- vague solar year
def venus   : ℕ := 584   -- Venus synodic period
def mars    : ℕ := 780   -- Mars synodic period  (= 3 × 260)

/-- Alignment windows, built as nested least common multiples. -/
def calendarRound : ℕ := Nat.lcm tzolkin haab          -- Tzolk'in + Haab'
def venusSolar    : ℕ := Nat.lcm haab venus            -- Haab' + Venus
def cosmicAlign   : ℕ := Nat.lcm calendarRound venus   -- + Venus
def grandAlign    : ℕ := Nat.lcm cosmicAlign mars      -- + Mars

/- ── Scalar values (`rfl` forces compile-time kernel evaluation) ── -/
theorem calendarRound_eq : calendarRound = 18980  := by rfl   -- 52 years
theorem venusSolar_eq    : venusSolar    = 2920   := by rfl   -- 8 years, 5 Venus
theorem cosmicAlign_eq   : cosmicAlign   = 37960  := by rfl   -- 104 years
theorem grandAlign_eq    : grandAlign    = 113880 := by rfl   -- 312 years

/-- The three-cycle window is exactly two Calendar Rounds. -/
theorem cosmic_two_rounds : cosmicAlign = 2 * calendarRound := by rfl
/-- Adding Mars multiplies the window by exactly three: six Calendar Rounds. -/
theorem grand_six_rounds  : grandAlign  = 6 * calendarRound := by rfl

/-- The elegant fact the draft missed: because `780 = 3 · 260`, Mars is three
    Tzolk'in rounds, so adjoining it to a system that already contains the
    Tzolk'in contributes only a factor of 3. -/
theorem mars_is_three_tzolkin : mars = 3 * tzolkin := by rfl
theorem grand_is_triple_cosmic : grandAlign = 3 * cosmicAlign := by rfl

/-- Tzolk'in–Mars absorption: any day count that resets Mars also resets the
    Tzolk'in, since 260 ∣ 780. -/
theorem tzolkin_mars_absorption (d : ℕ) (h : (d : ZMod mars) = 0) :
    (d : ZMod tzolkin) = 0 := by
  have dvd_mars : mars ∣ d := (ZMod.natCast_zmod_eq_zero_iff_dvd d mars).mp h
  have factor   : tzolkin ∣ mars := by decide          -- 260 ∣ 780
  exact (ZMod.natCast_zmod_eq_zero_iff_dvd d tzolkin).mpr (dvd_trans factor dvd_mars)

/-- Grand alignment: any day count that simultaneously returns the Tzolk'in,
    Haab', Venus and Mars cycles to their origin is a multiple of 113,880 days. -/
theorem grand_alignment (d : ℕ)
    (h1 : (d : ZMod tzolkin) = 0) (h2 : (d : ZMod haab) = 0)
    (h3 : (d : ZMod venus)   = 0) (h4 : (d : ZMod mars) = 0) :
    113880 ∣ d := by
  have dt : tzolkin ∣ d := (ZMod.natCast_zmod_eq_zero_iff_dvd d tzolkin).mp h1
  have dh : haab    ∣ d := (ZMod.natCast_zmod_eq_zero_iff_dvd d haab).mp h2
  have dv : venus   ∣ d := (ZMod.natCast_zmod_eq_zero_iff_dvd d venus).mp h3
  have dm : mars    ∣ d := (ZMod.natCast_zmod_eq_zero_iff_dvd d mars).mp h4
  have dcr : calendarRound ∣ d := Nat.lcm_dvd dt dh
  have dca : cosmicAlign   ∣ d := Nat.lcm_dvd dcr dv
  have dga : grandAlign    ∣ d := Nat.lcm_dvd dca dm
  rwa [grandAlign_eq] at dga

end Maya
