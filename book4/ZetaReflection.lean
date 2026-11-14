-- SPDX-License-Identifier: MIT
-- ============================================================================
/-
  Principia Orthogona · Book 4 · Chapter 12, §12.2
  THE VON MANGOLDT MOVE — how g transforms under the functional equation.

  §12.2 states Conjecture 12.1 and says what is needed: "understanding how the
  von Mangoldt coefficient g(σ,t) transforms under the functional equation — a
  computation that connects g(σ,t) to g(1−σ,t) via χ."  This file states the
  answer so a kernel can hold it, and marks exactly what is not yet proved.

  THE COEFFICIENTS.  For Re s > 1,  −ζ'/ζ(s) = Σ Λ(n) n^(−s), and splitting
  n^(−s) = n^(−σ)(cos(t log n) − i sin(t log n)) gives chapter 12's two
  coefficients as the real and imaginary parts of ONE meromorphic object:
      c(σ,t) = Re(−ζ'/ζ)        g(σ,t) = Im(ζ'/ζ)

  THE LAW.   ζ'/ζ(s) = χ'/χ(s) − ζ'/ζ(1−s), with c even in t and g odd in t,
  gives, on imaginary parts:
      g(σ,t) − g(1−σ,t) = Im[ χ'/χ(σ + it) ]
  Numerically confirmed 2026-08-30 to 30 digits at eight points
  (σ = 0.3, 0.5, 0.8, 1.1, 1.5, 2.3; t from 0.7 to 25), max deviation 8.8e-16.

  WHY THE CRITICAL LINE.  At σ = 1/2 the digamma arguments (1/4 + it/2) and
  (1/4 − it/2) are conjugates, so χ'/χ(1/2+it) is REAL and the right-hand side
  vanishes.  The constraint g(σ,t) = g(1−σ,t) therefore holds identically on
  the critical wall and nowhere else.  Not an analogy — an identity.

  WHAT THIS MEANS FOR CONJECTURE 12.1.  g is not carried to ±g by the
  reflection.  It is carried to itself plus a gamma-factor defect containing no
  Λ at all, so Φ*α = f·α with scalar f cannot hold off the critical line.  The
  provable statement is the graded one: the defect is explicit and vanishes on
  σ = 1/2.

  STATUS 2026-09-08.  Every theorem in this file is proved.  `Zlog_add_Zlog_one_sub`,
  admitted since 2026-08-30 and carried on a numerical check, is closed, and with it
  `reflection_law`, which was only ever waiting on that one input.  `--audit` reports
  no sorryAx anywhere.  The route, and the five runs and their corrections, are in
  `book4/ZetaFELogDeriv.lean`; the axiom report is
  `geometry/tools/verify-audit/2026-09-08/`.

  WHERE THIS LIVES.  Beside book4/ch12.html in the GTCT repo, which is Book 4's
  Lean home.  Deliberately NOT under GTCT/GCTC/ — that is the lean_lib the
  "Verify Lean proofs" workflow builds, and it pins mathlib v4.11.0, while this
  file needs v4.32.0 (`Gamma/Digamma.lean`,
  `LSeries_vonMangoldt_eq_deriv_riemannZeta_div`).  Putting it there today would
  fail lake build and turn the README badge red.  It moves into GCTC/ when that
  package is bumped to 4.32 — and it is a reason to bump it.

  HOW TO RUN:
      bash ~/Desktop/geometry/tools/leancheck.sh --audit \
           ~/Desktop/geometry/book4/ZetaReflection.lean
-/
-- ============================================================================

import Mathlib.NumberTheory.LSeries.RiemannZeta
import Mathlib.NumberTheory.LSeries.Dirichlet
import Mathlib.NumberTheory.Harmonic.ZetaAsymp
import Mathlib.Analysis.SpecialFunctions.Gamma.Digamma
import Mathlib.Analysis.SpecialFunctions.Gamma.Deligne
import Mathlib.Analysis.Calculus.LogDeriv
import Mathlib.Analysis.Calculus.Deriv.Star

namespace Book4.Ch12

open Complex ArithmeticFunction ComplexConjugate

/-- The logarithmic derivative of ζ. Both chapter-12 coefficients live here. -/
noncomputable def Zlog (s : ℂ) : ℂ := logDeriv riemannZeta s

/-- `c(σ,t)` of §11–12: the cosine coefficient. -/
noncomputable def cCoef (σ t : ℝ) : ℝ := (-Zlog ⟨σ, t⟩).re

/-- `g(σ,t)` of §11–12: the sine coefficient, the one §12.2 asks about. -/
noncomputable def gCoef (σ t : ℝ) : ℝ := (Zlog ⟨σ, t⟩).im

/-- `χ'/χ(s) = log π − ½ψ(s/2) − ½ψ((1−s)/2)`, the gamma-factor defect. -/
noncomputable def chiLog (s : ℂ) : ℂ :=
  (Real.log Real.pi : ℂ) - digamma (s / 2) / 2 - digamma ((1 - s) / 2) / 2

/-- The bridge to von Mangoldt: for `Re s > 1` the Λ-series IS `−ζ'/ζ`.
    This is Mathlib's, restated in `logDeriv` form; not new, but it is the
    step that makes `cCoef` and `gCoef` the chapter's coefficients rather
    than two arbitrary functions. -/
theorem lseries_vonMangoldt_eq_neg_Zlog {s : ℂ} (hs : 1 < s.re) :
    LSeries (fun n => (Λ n : ℂ)) s = -Zlog s := by
  simpa [Zlog, logDeriv_apply, neg_div] using
    LSeries_vonMangoldt_eq_deriv_riemannZeta_div hs


/-- ζ is conjugation-symmetric as a composite. -/
theorem zeta_conj_comp : (conj ∘ riemannZeta ∘ conj : ℂ → ℂ) = riemannZeta := by
  funext z
  simp only [Function.comp_apply, ← riemannZeta_conj, Complex.conj_conj]

/-- **PROVED 2026-08-30** · `ζ'/ζ` is conjugation-symmetric. -/
theorem Zlog_conj (s : ℂ) : Zlog (conj s) = conj (Zlog s) := by
  have hd : deriv (conj ∘ riemannZeta ∘ conj : ℂ → ℂ)
      = conj ∘ deriv riemannZeta ∘ conj := deriv_conj_conj
  rw [zeta_conj_comp] at hd
  have h1 : deriv riemannZeta (conj s) = conj (deriv riemannZeta s) := by
    have h := congrFun hd s
    simp only [Function.comp_apply] at h
    rw [h, Complex.conj_conj]
  simp only [Zlog, logDeriv_apply, h1, riemannZeta_conj, map_div₀]

/-- **PROVED 2026-08-30 · g is odd in t.**  The header states this; here it is
    checked. It is also the step that any short "route" to `reflection_law`
    will skip, and it is load-bearing: the functional equation relates
    `s = σ + it` to `1 − s = (1−σ) − it`, whereas the law is stated at
    `(1−σ) + it`. Odd parity in `t` is exactly what bridges the two. -/
theorem gCoef_odd_in_t (σ t : ℝ) : gCoef σ (-t) = - gCoef σ t := by
  have h : (⟨σ, -t⟩ : ℂ) = conj (⟨σ, t⟩ : ℂ) := by
    apply Complex.ext <;> simp
  simp only [gCoef, h, Zlog_conj, Complex.conj_im]

/-- **PROVED 2026-08-30 · c is even in t**, by the same symmetry. -/
theorem cCoef_even_in_t (σ t : ℝ) : cCoef σ (-t) = cCoef σ t := by
  have h : (⟨σ, -t⟩ : ℂ) = conj (⟨σ, t⟩ : ℂ) := by
    apply Complex.ext <;> simp
  simp only [cCoef, h, Zlog_conj, ← map_neg, Complex.conj_re]

/-! ### The functional equation, differentiated.

    Proved 2026-09-08.  Four steps; the route and the corrections it cost are
    recorded in `book4/ZetaFELogDeriv.lean`, the development file this came
    from.  Nothing below depends on anything outside Mathlib v4.32.0. -/

/-! ### Step 0 · what the hypotheses actually give -/

/-- `Gammaℝ s ≠ 0` is exactly the hypothesis, read through `Gammaℝ_eq_zero_iff`. -/
theorem Gammaℝ_ne_zero_of (s : ℂ) (hΓ : ∀ n : ℕ, s ≠ -(2 * n)) :
    Gammaℝ s ≠ 0 := by
  rw [Ne, Gammaℝ_eq_zero_iff]
  rintro ⟨n, hn⟩
  exact hΓ n hn

/-- `s ≠ 0` falls out of `hΓ` at `n = 0`.  This is the step that makes the
    four-hypothesis statement self-sufficient: nothing further has to be assumed
    to get differentiability. -/
theorem ne_zero_of (s : ℂ) (hΓ : ∀ n : ℕ, s ≠ -(2 * n)) : s ≠ 0 := by
  simpa using hΓ 0

/-- `Gammaℝ` is differentiable wherever it is nonzero, obtained by inverting the
    entire function `1/Gammaℝ` rather than through `Γ`'s own API. -/
theorem differentiableAt_Gammaℝ (s : ℂ) (h : Gammaℝ s ≠ 0) :
    DifferentiableAt ℂ Gammaℝ s := by
  have hinv : DifferentiableAt ℂ (fun z => (Gammaℝ z)⁻¹) s :=
    differentiable_Gammaℝ_inv s
  -- `Gammaℝ = ((Gammaℝ)⁻¹)⁻¹`, and the inner function is entire.
  have h2 : DifferentiableAt ℂ (fun z => ((Gammaℝ z)⁻¹)⁻¹) s :=
    hinv.inv (inv_ne_zero h)
  -- `simpa only [inv_inv]` and not bare `simpa`: an unrestricted simp set
  -- rewrote the hypothesis into a shape that no longer matched the goal.
  simpa only [inv_inv] using h2

/-! ### Step 1 · the logarithmic derivative of the archimedean factor -/

/-- **The reusable half.**  `logDeriv Gammaℝ s = −½ log π + ½ ψ(s/2)`.

    This is the piece that is worth offering to Mathlib on its own, independently
    of anything below: it is a statement about `Gammaℝ` and `digamma` alone, both
    of which are Mathlib's, and it is what one needs any time an archimedean
    factor is differentiated. -/
theorem logDeriv_Gammaℝ (s : ℂ) (hΓ : ∀ n : ℕ, s ≠ -(2 * n)) :
    logDeriv Gammaℝ s = -(Real.log Real.pi : ℂ) / 2 + digamma (s / 2) / 2 := by
  -- NOTE.  `HasDerivAt.logDeriv_Gamma` does NOT exist in Mathlib v4.32.0 -- it is
  -- in a later version.  The Γ half therefore goes through `logDeriv_comp` and
  -- `digamma_def` instead, which is one line longer and needs no future library.
  have hne : Gammaℝ s ≠ 0 := Gammaℝ_ne_zero_of s hΓ
  have hsplit : ((Real.pi : ℂ)) ^ (-s / 2) * Gamma (s / 2) ≠ 0 := by
    rw [← Gammaℝ_def]; exact hne
  obtain ⟨hA, hB⟩ := mul_ne_zero_iff.mp hsplit
  -- `s / 2 = -m` would say `s = -(2m)`, which is exactly what hΓ forbids.
  have hΓdiff : DifferentiableAt ℂ Gamma (s / 2) :=
    differentiableAt_Gamma _ (fun m h => hΓ m (by linear_combination 2 * h))
  have hg : DifferentiableAt ℂ (fun z : ℂ => z / 2) s := differentiableAt_id.div_const 2
  -- (a)  the archimedean power.  `HasDerivAt.const_cpow` gives
  --      d/dz π^(f z) = π^(f z) · log π · f'(z), and the π^(f s) cancels.
  have hd : HasDerivAt (fun z : ℂ => ((Real.pi : ℂ)) ^ (-z / 2))
      (((Real.pi : ℂ)) ^ (-s / 2) * Complex.log ((Real.pi : ℂ)) * (-(1 : ℂ) / 2)) s := by
    have h1 : HasDerivAt (fun z : ℂ => -z / 2) (-(1 : ℂ) / 2) s := by
      simpa using (hasDerivAt_neg s).div_const 2
    exact h1.const_cpow (Or.inl (by simp))
  have ha : logDeriv (fun z : ℂ => ((Real.pi : ℂ)) ^ (-z / 2)) s
      = -(Real.log Real.pi : ℂ) / 2 := by
    rw [logDeriv_apply, hd.deriv, ← Complex.ofReal_log Real.pi_pos.le]
    field_simp
  -- (b)  the Γ factor.  logDeriv (Γ ∘ (·/2)) s = logDeriv Γ (s/2) · (1/2), and
  --      `digamma` is by definition `logDeriv Gamma`.
  have hderiv2 : deriv (fun z : ℂ => z / 2) s = 1 / 2 := by
    simp [deriv_div_const]
  have hb : logDeriv (fun z : ℂ => Gamma (z / 2)) s = digamma (s / 2) / 2 := by
    have hcomp : (fun z : ℂ => Gamma (z / 2)) = Gamma ∘ (fun z : ℂ => z / 2) := rfl
    -- The type ascription is load-bearing.  Left to infer, `logDeriv_comp`
    -- decomposed the composite as g := (s / ·) at x := 2, which typechecks as a
    -- unification and is not the statement wanted.
    have h : logDeriv (Gamma ∘ fun z : ℂ => z / 2) s
        = logDeriv Gamma (s / 2) * deriv (fun z : ℂ => z / 2) s :=
      logDeriv_comp hΓdiff hg
    rw [hcomp, h, hderiv2, ← digamma_def]
    ring
  have hprod : Gammaℝ = fun z : ℂ => ((Real.pi : ℂ)) ^ (-z / 2) * Gamma (z / 2) :=
    funext Gammaℝ_def
  have hBdiff : DifferentiableAt ℂ (fun z : ℂ => Gamma (z / 2)) s := hΓdiff.comp s hg
  rw [hprod, logDeriv_mul (f := fun z : ℂ => ((Real.pi : ℂ)) ^ (-z / 2))
      (g := fun z : ℂ => Gamma (z / 2)) s hA hB hd.differentiableAt hBdiff, ha, hb]

/-! ### Step 2 · the completed zeta splits -/

/-- Near any `s ≠ 0`, `Λ` agrees with the product `Gammaℝ · ζ`, so its log
    derivative splits.  The equality is only needed on a neighbourhood, which is
    why `s ≠ 0` suffices. -/
theorem logDeriv_completedRiemannZeta (s : ℂ)
    (hΓ : ∀ n : ℕ, s ≠ -(2 * n)) (hζ : riemannZeta s ≠ 0) (hs1 : s ≠ 1) :
    logDeriv completedRiemannZeta s = logDeriv Gammaℝ s + Zlog s := by
  have hne : Gammaℝ s ≠ 0 := Gammaℝ_ne_zero_of s hΓ
  -- `Λ = Gammaℝ · ζ` is FALSE at the zeros of Gammaℝ — at z = -2 the right side
  -- vanishes and Λ(-2) = Λ(3) does not — so the identity is only available on a
  -- neighbourhood, and the neighbourhood has to be produced.  The set where
  -- Gammaℝ ≠ 0 is open because `1/Gammaℝ` is ENTIRE (`differentiable_Gammaℝ_inv`),
  -- so it is the preimage of an open set under a continuous map.  Going through
  -- the inverse avoids needing continuity of Gammaℝ itself, which is exactly what
  -- is not available at its poles.
  have hUopen : IsOpen {z : ℂ | Gammaℝ z ≠ 0} := by
    have hset : {z : ℂ | Gammaℝ z ≠ 0} = (fun z : ℂ => (Gammaℝ z)⁻¹) ⁻¹' {0}ᶜ := by
      ext z; simp [inv_eq_zero]
    rw [hset]
    exact isOpen_compl_singleton.preimage differentiable_Gammaℝ_inv.continuous
  have hev : completedRiemannZeta =ᶠ[nhds s] fun z : ℂ => Gammaℝ z * riemannZeta z := by
    filter_upwards [hUopen.mem_nhds hne] with z hz
    -- z ≠ 0 comes free: Gammaℝ 0 = 0, so the good set is already inside {0}ᶜ.
    have hz0 : z ≠ 0 := by
      rintro rfl
      exact hz (Gammaℝ_eq_zero_iff.mpr ⟨0, by simp⟩)
    rw [riemannZeta_def_of_ne_zero hz0]
    field_simp
  have hswap : logDeriv completedRiemannZeta s
      = logDeriv (fun z : ℂ => Gammaℝ z * riemannZeta z) s := by
    rw [logDeriv_apply, logDeriv_apply, hev.deriv_eq, hev.eq_of_nhds]
  rw [hswap, logDeriv_mul (f := Gammaℝ) (g := riemannZeta) s hne hζ
      (differentiableAt_Gammaℝ s hne) (differentiableAt_riemannZeta hs1)]
  rfl

/-! ### Step 3 · the reflection, which is the only step with content -/

/-- `Λ(1−s) = Λ(s)` differentiated.  The minus sign from `deriv_comp_const_sub`
    is the whole of the functional equation as it acts on log derivatives. -/
theorem logDeriv_completedRiemannZeta_add_one_sub (s : ℂ)
    (hΛ : completedRiemannZeta s ≠ 0) :
    logDeriv completedRiemannZeta s + logDeriv completedRiemannZeta (1 - s) = 0 := by
  have hfun : (fun z : ℂ => completedRiemannZeta (1 - z)) = completedRiemannZeta := by
    funext z; exact completedRiemannZeta_one_sub z
  have hderiv : deriv completedRiemannZeta s = -deriv completedRiemannZeta (1 - s) := by
    have h1 : deriv (fun z : ℂ => completedRiemannZeta (1 - z)) s
        = -deriv completedRiemannZeta (1 - s) := deriv_comp_const_sub _ _ _
    rw [hfun] at h1
    exact h1
  have hval : completedRiemannZeta (1 - s) = completedRiemannZeta s :=
    completedRiemannZeta_one_sub s
  -- After the rewrites the goal is `(-a) / c + a / c = 0`, with `a = deriv Λ (1-s)`
  -- and `c = Λ s`.  That is a ring identity in a field — division is multiplication
  -- by the formal inverse, so `(-a)·c⁻¹ + a·c⁻¹ = (-a + a)·c⁻¹ = 0` needs no
  -- side condition — and `ring` closes it.  Two earlier attempts did not:
  -- `field_simp` left it unsolved, and `div_add_div_same` is not a name in this
  -- Mathlib.  Reaching for a lemma by remembered name cost two runs; the identity
  -- was closed by the tactic that does not need a name.
  simp only [logDeriv_apply]
  rw [hderiv, hval]
  ring

/-- **PROVED 2026-09-08** (was ADMITTED) · the analytic input, no longer assumed.
    Off the zeros of ζ and the poles of the two Γ factors, the logarithmic
    derivative and its reflection sum to the gamma-factor defect.

    The proof is Λ(1−s) = Λ(s) differentiated: `logDeriv Λ s + logDeriv Λ (1−s) = 0`,
    then `logDeriv Λ = logDeriv Gammaℝ + logDeriv ζ`, then `logDeriv Gammaℝ` read off.
    The four hypotheses are exactly the side conditions the route needs and are also
    exactly sufficient — at `n = 0` they supply `s ≠ 0` and `s ≠ 1`, the two points
    where ζ and Λ are not differentiable, so nothing further is assumed.

    The numerical check that stood in place of this proof (30 digits, eight points,
    max deviation 8.8e-16) is retained in the header as a record and is no longer
    load-bearing. -/
theorem Zlog_add_Zlog_one_sub (s : ℂ)
    (hΓ  : ∀ n : ℕ, s ≠ -(2 * n))
    (hΓ' : ∀ n : ℕ, (1 - s) ≠ -(2 * n))
    (hζ  : riemannZeta s ≠ 0)
    (hζ' : riemannZeta (1 - s) ≠ 0) :
    Zlog s + Zlog (1 - s) = chiLog s := by
  -- s ≠ 0 from hΓ at n = 0; s ≠ 1 from hΓ' at n = 0.
  have hs0 : s ≠ 0 := ne_zero_of s hΓ
  have h1s0 : (1 - s) ≠ 0 := ne_zero_of (1 - s) hΓ'
  have hs1 : s ≠ 1 := fun h => h1s0 (by simp [h])
  have h1s1 : (1 - s) ≠ 1 := fun h => hs0 (by linear_combination -h)
  -- Λ s ≠ 0.  If it vanished, so would Λ s / Gammaℝ s, which is ζ s.
  have hΛ : completedRiemannZeta s ≠ 0 := by
    rw [riemannZeta_def_of_ne_zero hs0] at hζ
    exact fun h => hζ (by rw [h]; simp)
  -- the three steps
  have key := logDeriv_completedRiemannZeta_add_one_sub s hΛ
  rw [logDeriv_completedRiemannZeta s hΓ hζ hs1,
      logDeriv_completedRiemannZeta (1 - s) hΓ' hζ' h1s1,
      logDeriv_Gammaℝ s hΓ, logDeriv_Gammaℝ (1 - s) hΓ'] at key
  -- key : (-logπ/2 + ψ(s/2)/2 + Zlog s) + (-logπ/2 + ψ((1-s)/2)/2 + Zlog (1-s)) = 0
  rw [chiLog]
  linear_combination key

/-- **PROVED, from the one admitted input above** · the transformation law of
    §12.2. The reduction below is kernel-checked; the only thing it consumes is
    `Zlog_add_Zlog_one_sub`. The parity half is `gCoef_odd_in_t`, proved above,
    which is what bridges `1 − s = (1−σ) − it` to the law's `(1−σ) + it`.

    WHAT REMAINS, as of 2026-08-30. The parity half is proved above
    (`gCoef_odd_in_t`), so the only missing input is

        ζ'/ζ(s) + ζ'/ζ(1−s) = chiLog s                          (FE-log)

    Verified numerically to 30 digits at three interior points (mpmath,
    2026-08-30). Given it, the law is three lines:
      ζ'/ζ(σ+it) = chiLog(σ+it) − ζ'/ζ((1−σ) − it)     (FE-log)
      Im: g(σ,t) = Im chiLog(σ+it) − g(1−σ, −t)         (definition of g)
                 = Im chiLog(σ+it) + g(1−σ, t)          (gCoef_odd_in_t)

    ROUTE, and this is the part worth getting right. Do NOT go via Mathlib's
    `riemannZeta_one_sub`. That is the ASYMMETRIC equation

        ζ(1−s) = 2 (2π)^(−s) Γ(s) cos(πs/2) ζ(s)

    whose logarithmic derivative is −log(2π) + ψ(s) − (π/2)tan(πs/2), which is
    NOT `chiLog`. Getting from one to the other needs Legendre duplication and
    Euler reflection for Γ — a real grind, not a chain rule.

    Go instead via the SYMMETRIC equation, which Mathlib also has:

        `completedRiemannZeta_one_sub : Λ (1 − s) = Λ s`,  Λ(s) = π^(−s/2) Γ(s/2) ζ(s)

    Take `logDeriv` of both sides. With `logDeriv_mul` (twice) and
    `logDeriv_comp` for the `1 − s` chain rule,
        Λ'/Λ(s) = −½ log π + ½ψ(s/2) + ζ'/ζ(s)
    and Λ'/Λ(s) = −Λ'/Λ(1−s) rearranges directly into (FE-log). The side
    conditions are the non-vanishing needed by `logDeriv_mul`.

    CAREFUL with Γ. It is true classically that Γ never vanishes, but Mathlib
    encodes Γ's POLES as zeros: `Complex.Gamma_eq_zero_iff s : Γ s = 0 ↔ ∃ m : ℕ,
    s = −m`. So `Γ(s/2) ≠ 0` is NOT free here — it needs `s ∉ {0, −2, −4, …}`,
    and the hypothesis has to be carried. Harmless for this chapter, which lives
    in the critical strip, but it will not discharge itself.

    Full side conditions: `s ∉ {0, −2, −4, …}` and `(1−s) ∉ {0, −2, −4, …}` for
    the two Γ factors, and `ζ(s) ≠ 0`, `ζ(1−s) ≠ 0`. The identity is therefore
    stated off the zeros — which is where g is defined anyway. Nothing in it
    assumes WHERE the zeros are.

    WHY THE HYPOTHESES ARE IN THE SIGNATURE.  `Zlog = logDeriv riemannZeta`, so
    at a zero of ζ the division is by zero and Lean returns 0.  Stated for all
    real σ, t the identity would therefore be a claim about junk values at the
    zeros and the Γ-poles — and at a hypothetical zero off the critical line the
    left side degenerates to `0 - gCoef (1-σ) t` with nothing forcing that to
    vanish while the right side does not.  The statement's truth would then
    depend on where the zeros are, which is exactly what the paragraph above
    says it must not do.  The four hypotheses close that gap.

    NOTE the pole set.  Mathlib bundles `π^(-s/2) Γ(s/2)` as `Gammaℝ`, and
    `Gammaℝ_eq_zero_iff : Gammaℝ s = 0 ↔ ∃ n : ℕ, s = -(2 * n)` — the negative
    EVEN integers.  `∀ m : ℕ, s ≠ -m` would be strictly stronger than needed and
    would not match the iff.  `hΓ` at `n = 0` supplies `s ≠ 0` and `hΓ'` at
    `n = 0` supplies `s ≠ 1`, which are exactly what `differentiableAt_completedZeta`
    wants at both `s` and `1 - s`; no fifth hypothesis is required, and
    `Λ s ≠ 0` is derivable from `hζ` and `hΓ` rather than assumed.

    ROUTE CORRECTION.  The product form is NOT `completedRiemannZeta_eq` — that
    one is subtractive, `Λ s = Λ₀ s - 1/s - 1/(1-s)`.  Use
    `riemannZeta_def_of_ne_zero (hs : s ≠ 0) : ζ s = Λ s / Gammaℝ s`
    (Mathlib/NumberTheory/LSeries/RiemannZeta.lean:155), rearranged.

    DEPOSIT.  Zenodo v1 (10.5281/zenodo.22179684) carries this statement without
    the hypotheses.  The domain is narrower here, so the difference is called out
    in the v2 release notes. -/
theorem reflection_law (σ t : ℝ)
    (hΓ  : ∀ n : ℕ, (⟨σ, t⟩ : ℂ) ≠ -(2 * n))
    (hΓ' : ∀ n : ℕ, (1 - (⟨σ, t⟩ : ℂ)) ≠ -(2 * n))
    (hζ  : riemannZeta ⟨σ, t⟩ ≠ 0)
    (hζ' : riemannZeta (1 - (⟨σ, t⟩ : ℂ)) ≠ 0) :
    gCoef σ t - gCoef (1 - σ) t = (chiLog ⟨σ, t⟩).im := by
  have hsub : (1 : ℂ) - (⟨σ, t⟩ : ℂ) = (⟨1 - σ, -t⟩ : ℂ) := by
    apply Complex.ext <;> simp
  have hodd := gCoef_odd_in_t (1 - σ) t
  have hval : gCoef (1 - σ) (-t) = (Zlog (1 - (⟨σ, t⟩ : ℂ))).im := by
    simp only [gCoef, hsub]
  rw [hval] at hodd
  have hg2 : gCoef (1 - σ) t = -((Zlog (1 - (⟨σ, t⟩ : ℂ))).im) := by linarith
  have hkey := Zlog_add_Zlog_one_sub (⟨σ, t⟩ : ℂ) hΓ hΓ' hζ hζ'
  rw [hg2, sub_neg_eq_add]
  show (Zlog (⟨σ, t⟩ : ℂ)).im + (Zlog (1 - (⟨σ, t⟩ : ℂ))).im = (chiLog ⟨σ, t⟩).im
  rw [← Complex.add_im, hkey]

/-- Γ is conjugation-symmetric as a composite: `conj ∘ Γ ∘ conj = Γ`. -/
theorem Gamma_conj_comp : (conj ∘ Gamma ∘ conj : ℂ → ℂ) = Gamma := by
  funext z
  simp only [Function.comp_apply, ← Complex.Gamma_conj, Complex.conj_conj]

/-- **digamma is conjugation-symmetric**: `ψ(conj s) = conj (ψ s)`.
    From `Complex.Gamma_conj` and `deriv_conj_conj`; `digamma = logDeriv Γ`. -/
theorem digamma_conj (s : ℂ) : digamma (conj s) = conj (digamma s) := by
  have hd : deriv (conj ∘ Gamma ∘ conj : ℂ → ℂ) = conj ∘ deriv Gamma ∘ conj :=
    deriv_conj_conj
  rw [Gamma_conj_comp] at hd
  have h1 : deriv Gamma (conj s) = conj (deriv Gamma s) := by
    have h := congrFun hd s
    simp only [Function.comp_apply] at h
    rw [h, Complex.conj_conj]
  simp only [digamma_def, logDeriv_apply, h1, Complex.Gamma_conj, map_div₀]

/-- **The critical line, as a statement about conjugation.**  `1 − s = conj s`
    holds exactly on `σ = 1/2`.  This is the whole reason the reflection
    constraint degenerates there, stated on its own rather than buried inside a
    `normSq` expansion. -/
theorem one_sub_conj (t : ℝ) : (1 : ℂ) - ⟨1/2, t⟩ = conj (⟨1/2, t⟩ : ℂ) := by
  simp [Complex.ext_iff] <;> norm_num

/-- **PROVED 2026-08-30** (was ADMITTED) · why σ = 1/2 is distinguished: the
    gamma-factor defect is real there, so the reflection constraint holds
    identically on the critical wall.

    At `s = 1/2 + it` the two digamma arguments are complex conjugates —
    `s/2 = 1/4 + it/2` and `(1−s)/2 = 1/4 − it/2` — so by `digamma_conj`
    their sum is `2 Re ψ(s/2)`, real; and `log π` is real. Nothing about the
    zeros of ζ is used: this is Schwarz reflection for Γ and nothing more.

    `#print axioms` reports [propext, Classical.choice, Quot.sound]. -/
theorem chiLog_real_on_critical_line (t : ℝ) :
    (chiLog ⟨1/2, t⟩).im = 0 := by
  have hconj : (1 - (⟨1/2, t⟩ : ℂ)) / 2 = conj ((⟨1/2, t⟩ : ℂ) / 2) := by
    rw [map_div₀, Complex.conj_ofNat, one_sub_conj]
  rw [chiLog, hconj, digamma_conj]
  simp [Complex.sub_im, Complex.conj_im, Complex.ofReal_im]
  ring

/-- FIXTURE · deliberately vacuous. Its axiom report is indistinguishable from
    a real theorem's, which is why reading the statements is still required. -/
theorem vacuity_control : True := trivial

end Book4.Ch12

-- ============================================================================
-- NO #print axioms BLOCK HERE, DELIBERATELY.
--
-- `tools/leancheck.sh --audit` generates one `#print axioms` line per theorem
-- and appends it to a copy of this file.  A file that also carries its own
-- block gets probed twice, and the tool then reports double the declarations
-- and double the sorryAx hits — 8 and 4 instead of 4 and 2, measured
-- 2026-08-30.  An instrument must not count its own echo.
--
-- EXPECTED under `--audit`:  18 declarations, 0 trusting sorryAx.  Six theorems
-- were added on 2026-09-08 (Gammaℝ_ne_zero_of, ne_zero_of, differentiableAt_Gammaℝ,
-- logDeriv_Gammaℝ, logDeriv_completedRiemannZeta,
-- logDeriv_completedRiemannZeta_add_one_sub) and the two that trusted sorryAx —
-- Zlog_add_Zlog_one_sub and reflection_law — no longer do.  This count moves in
-- the SAME edit as any change to the declarations: an expectation that lags the
-- artifact is not a check, it is a second claim to audit.
-- `lseries_vonMangoldt_eq_neg_Zlog` must NOT appear; if it does, the bridge to
-- von Mangoldt has broken and nothing above means anything.  Likewise
-- `digamma_conj` and `gCoef_odd_in_t` must NOT appear: they are the load-bearing
-- inputs to what is proved.
-- ============================================================================
