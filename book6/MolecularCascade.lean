import Mathlib

/-
Book VI, chapter 6: The Molecular Cascade. Lean core.

STATUS: COMPILED by the author on 2026-11-03 (no errors; one push_neg deprecation warning at the
time; no sorryAx; output in molecularcascade.axioms.txt). Header text only edited since. To run:
  lake env lean book6/MolecularCascade.lean

WHAT THIS FILE IS. The chapter's own section 4 says it makes no claim that any rate constant,
threshold or structure derives from the corpus's constants. So this file does not formalise biology.
It formalises only the arithmetic and the decision rule that the chapter states in words:

  Part A  two filters in series (the double sieve), as a product of pass fractions
            net_error_le_first / _le_second   a filter that passes at most everything never raises the error
            double_sieve_example              1/40 through a fine sieve passing 1/1000 gives 1/40000
            required_pass_fraction            the fine-sieve pass fraction needed to reach a target
            required_examples                 1/400 from 1/100, 1/4000 from 1/10, 1/1000 from 1/40
            strict_gain_iff                   a strict improvement happens exactly when the fine
                                              sieve passes less than everything (the control)
  Part B  the nonsense-mediated-decay rule as the chapter states it: a stop codon at position s is
          flagged when it lies more than T nucleotides upstream of the last exon-exon junction at j
            nmd_no_flag_last_exon, nmd_no_flag_within, nmd_flag_upstream_monotone,
            nmd_threshold_antitone, nmd_band (the 50-versus-55 band), nmd_band_example
  Part C  the chapter's section 3 numbers, exactly
            misincorporation_inside_window    1-3 per 10,000 sits inside 1/40,000 .. 1/2,400
            improvement_factors               400, 4000, 1000 and the old 10^4
            old_vs_new_low_end                the new low end is 2500 times the old 10^-8

WHAT IT DOES NOT PROVE. Nothing about any real enzyme, ribosome or transcript: whether the true
pass fractions are 1/1000, whether the true NMD threshold is 50 or 55, and the ChargingAttempt
sketch in the chapter (not in this file) are empirical or unformalised. Part A assumes the two
stages are independent and multiplicative; that is a modelling assumption, not a theorem about
aminoacyl-tRNA synthetases.
-/

namespace Book6Molecular

/-! ### Part A: two filters in series -/

/-- Net error of two stages in series: e₁ is the error after the first sieve (the fraction wrongly
accepted), e₂ is the fraction of those the second sieve fails to remove. Independence is assumed. -/
def netError (e₁ e₂ : ℚ) : ℚ := e₁ * e₂

theorem net_error_le_first {e₁ e₂ : ℚ} (h₁ : 0 ≤ e₁) (h₂ : e₂ ≤ 1) : netError e₁ e₂ ≤ e₁ := by
  unfold netError
  nlinarith [mul_nonneg h₁ (sub_nonneg.2 h₂)]

theorem net_error_le_second {e₁ e₂ : ℚ} (h₁ : e₁ ≤ 1) (h₂ : 0 ≤ e₂) : netError e₁ e₂ ≤ e₂ := by
  unfold netError
  nlinarith [mul_nonneg h₂ (sub_nonneg.2 h₁)]

/-- The chapter's headline figures as arithmetic: a coarse error of 1/40 and a fine sieve that lets
through 1/1000 of what slips past give 1/40000. -/
theorem double_sieve_example : netError (1 / 40) (1 / 1000) = 1 / 40000 := by
  unfold netError
  norm_num

/-- If the net error is t and the first-sieve error is e₁ ≠ 0, the second stage passes t / e₁. -/
theorem required_pass_fraction {e₁ e₂ t : ℚ} (h : e₁ ≠ 0) (hm : netError e₁ e₂ = t) :
    e₂ = t / e₁ := by
  unfold netError at hm
  rw [← hm, mul_comm, mul_div_assoc, div_self h, mul_one]

theorem required_examples :
    (1 / 40000 : ℚ) / (1 / 100) = 1 / 400 ∧ (1 / 40000 : ℚ) / (1 / 10) = 1 / 4000 ∧
      (1 / 40000 : ℚ) / (1 / 40) = 1 / 1000 := by
  refine ⟨?_, ?_, ?_⟩ <;> norm_num

/-- Control: a second stage that passes everything changes nothing. -/
theorem no_gain_if_passes_all (e : ℚ) : netError e 1 = e := by
  unfold netError
  ring

/-- Control: for a positive first-stage error, the second stage helps strictly exactly when it
passes strictly less than everything. -/
theorem strict_gain_iff {e₁ e₂ : ℚ} (h : 0 < e₁) : netError e₁ e₂ < e₁ ↔ e₂ < 1 := by
  unfold netError
  constructor
  · intro hlt
    by_contra hc
    push_neg at hc
    nlinarith [mul_nonneg h.le (sub_nonneg.2 hc)]
  · intro h2
    nlinarith [mul_pos h (sub_pos.2 h2)]

/-! ### Part B: the nonsense-mediated-decay rule as stated in the chapter -/

/-- A stop codon at position `s` is flagged when it lies more than `T` nucleotides upstream of the
last exon-exon junction at position `j`. Positions are nucleotide counts along the transcript.
This is the chapter's rule as stated, as a model; it is not a claim about the cell. -/
def nmdFlag (T s j : ℕ) : Prop := s + T < j

theorem nmd_no_flag_last_exon {T s j : ℕ} (h : j ≤ s) : ¬ nmdFlag T s j := by
  unfold nmdFlag
  omega

theorem nmd_no_flag_within {T s j : ℕ} (h : j ≤ s + T) : ¬ nmdFlag T s j := by
  unfold nmdFlag
  omega

theorem nmd_flag_upstream_monotone {T s s' j : ℕ} (h : nmdFlag T s j) (hs : s' ≤ s) :
    nmdFlag T s' j := by
  unfold nmdFlag at *
  omega

theorem nmd_threshold_antitone {T T' s j : ℕ} (hT : T ≤ T') (h : nmdFlag T' s j) :
    nmdFlag T s j := by
  unfold nmdFlag at *
  omega

/-- The chapter says "50-55". Under the rule as stated, the positions flagged at 50 but not at 55
are exactly those between 50 and 55 nucleotides upstream. -/
theorem nmd_band {s j : ℕ} :
    (nmdFlag 50 s j ∧ ¬ nmdFlag 55 s j) ↔ (s + 50 < j ∧ j ≤ s + 55) := by
  unfold nmdFlag
  constructor <;> intro h <;> omega

theorem nmd_band_example : nmdFlag 50 100 152 ∧ ¬ nmdFlag 55 100 152 := by
  unfold nmdFlag
  omega

/-! ### Part C: the chapter's section 3 numbers, exactly -/

/-- 1 to 3 misincorporations per 10,000 lies strictly inside the window 1/40,000 .. 1/2,400. It is
containment, not equality: neither endpoint of the window equals an endpoint of 1..3 per 10,000. -/
theorem misincorporation_inside_window :
    (1 / 40000 : ℚ) < 1 / 10000 ∧ (3 / 10000 : ℚ) < 1 / 2400 := by
  refine ⟨?_, ?_⟩ <;> norm_num

theorem improvement_factors :
    (1 / 100 : ℚ) / (1 / 40000) = 400 ∧ (1 / 10 : ℚ) / (1 / 40000) = 4000 ∧
      (1 / 40 : ℚ) / (1 / 40000) = 1000 ∧ (1 / 10 ^ 4 : ℚ) / (1 / 10 ^ 8) = 10 ^ 4 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> norm_num

/-- The new low end 1/40,000 is 2500 times the old 10^-8: not "an order of magnitude looser". -/
theorem old_vs_new_low_end : (1 / 40000 : ℚ) / (1 / 10 ^ 8) = 2500 := by
  norm_num

#print axioms net_error_le_first
#print axioms net_error_le_second
#print axioms double_sieve_example
#print axioms required_pass_fraction
#print axioms required_examples
#print axioms no_gain_if_passes_all
#print axioms strict_gain_iff
#print axioms nmd_no_flag_last_exon
#print axioms nmd_no_flag_within
#print axioms nmd_flag_upstream_monotone
#print axioms nmd_threshold_antitone
#print axioms nmd_band
#print axioms nmd_band_example
#print axioms misincorporation_inside_window
#print axioms improvement_factors
#print axioms old_vs_new_low_end

end Book6Molecular
