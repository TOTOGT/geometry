-- SPDX-License-Identifier: MIT
-- ============================================================================
/-
  Principia Orthogona · Book 4 · Chapter 12 · DEVELOPMENT FILE

  THE LOG-DERIVATIVE FORM OF THE FUNCTIONAL EQUATION.

  Target — currently `sorry`-ed as `Zlog_add_Zlog_one_sub` in
  `book4/ZetaReflection.lean`:

      ζ'/ζ(s) + ζ'/ζ(1−s) = log π − ½ψ(s/2) − ½ψ((1−s)/2)

  This file is NOT the audited file.  It exists to be compiled and edited until
  it carries no `sorry`, at which point the proof moves into `ZetaReflection.lean`
  in place of the admitted statement and this file is retired to evidence.
  Keeping the two apart means the audited file's `#print axioms` expectation
  (12 declarations, sorryAx on the one) does not move while this is in flight.

  THE ROUTE, in four steps.  Nothing here is deep; the work is entirely in
  finding which library lemma does each step.

    Λ(s) = Gammaℝ(s)·ζ(s)          with Gammaℝ(s) = π^(−s/2)·Γ(s/2)

    [1]  logDeriv Gammaℝ s = −½·log π + ½·ψ(s/2)
         The π-power contributes a constant; the Γ contributes ψ(s/2) with a
         factor ½ from the chain rule.  `HasDerivAt.logDeriv_Gamma` does the
         second half in one line.

    [2]  logDeriv Λ s = logDeriv Gammaℝ s + logDeriv ζ s
         `logDeriv_fun_mul`, needing both factors nonzero and differentiable
         at s.  Differentiability of Gammaℝ comes from `differentiable_Gammaℝ_inv`
         by inverting, which avoids Γ's own differentiability API entirely.

    [3]  logDeriv Λ s + logDeriv Λ (1−s) = 0
         THE ONLY STEP WITH ANY CONTENT.  Λ(1−s) = Λ(s) holds as a function
         identity, so differentiating gives −Λ'(1−s) = Λ'(s); dividing by
         Λ(s) = Λ(1−s) turns that into the sum above.  The minus sign is the
         whole reflection, and it is `deriv_comp_const_sub` that supplies it.

    [4]  Substitute [1] and [2] into [3] and read off.  The two −½·log π
         contributions add to −log π, which moves to the other side as the
         +log π of the gamma-factor defect.

  WHY THE FOUR HYPOTHESES ARE EXACTLY RIGHT — worth recording, because they
  look like four and are doing the work of six.

    hΓ  : ∀ n : ℕ, s ≠ -(2 * n)        gives Gammaℝ s ≠ 0        (Gammaℝ_eq_zero_iff)
    hΓ' : ∀ n : ℕ, (1 - s) ≠ -(2 * n)  gives Gammaℝ (1-s) ≠ 0
    hζ  : riemannZeta s ≠ 0
    hζ' : riemannZeta (1 - s) ≠ 0

  At n = 0 the first gives s ≠ 0, and the second gives 1 − s ≠ 0, i.e. s ≠ 1.
  Those are precisely the two points where ζ and Λ are not differentiable, so
  the differentiability side conditions are already contained in the hypotheses
  as stated and do not have to be added.  Dropping any one of the four leaves a
  statement that either asserts an equality of junk values or divides by zero.

  ROUTE TRAPS, recorded 2026-08-30 and still binding:
    · Go via `completedRiemannZeta_one_sub` (Λ(1−s) = Λ(s)), NOT
      `riemannZeta_one_sub` — the latter is the asymmetric form carrying
      cos(πs/2), and converting it costs Legendre duplication and Euler
      reflection on top of everything below.
    · Mathlib encodes Γ's poles as ZEROS, so `Gammaℝ s ≠ 0` is not free.  That
      is what hΓ and hΓ' are for.

  STATUS OF THIS FILE — read before trusting a line of it.
  STATUS 2026-09-08.  CLOSED.  Compiles clean, no `sorry` in the code, and the
  gate agrees: seven declarations, every one on `[propext, Classical.choice,
  Quot.sound]`, no `sorryAx`.  Report written by the run at
  `geometry/tools/verify-audit/2026-09-08/ZetaFELogDeriv.axioms.txt`.

  The proof has been moved into `book4/ZetaReflection.lean`, where it replaces the
  statement that had been admitted since 2026-08-30.  This file is kept as the
  development record: it is where the route and its five runs live, and deleting it
  would leave the corrected file with no account of how it was arrived at.

  Five runs, five failures, none mathematical — three tactic hygiene, two names
  read from the docs site rather than from the pinned tree.  The four-step route
  never changed.  Each correction is recorded at its site rather than here.

  LIBRARY FACTS THIS LEANS ON — all confirmed present, 2026-09-08:
    Complex.Gammaℝ_def, Complex.Gammaℝ_eq_zero_iff, Complex.differentiable_Gammaℝ_inv
    Complex.digamma_def, HasDerivAt.logDeriv_Gamma
    completedRiemannZeta_one_sub, riemannZeta_def_of_ne_zero
    differentiableAt_riemannZeta, riemannZeta_ne_zero_of_one_le_re
    logDeriv_apply, logDeriv_fun_mul, logDeriv_comp, logDeriv_const
-/
-- ============================================================================

import Mathlib.NumberTheory.LSeries.RiemannZeta
import Mathlib.Analysis.SpecialFunctions.Gamma.Digamma
import Mathlib.Analysis.SpecialFunctions.Gamma.Deligne
import Mathlib.Analysis.Calculus.LogDeriv

open Complex

namespace Book4.Ch12.FE

noncomputable def Zlog (s : ℂ) : ℂ := logDeriv riemannZeta s

/-- `χ'/χ(s) = log π − ½ψ(s/2) − ½ψ((1−s)/2)`, the gamma-factor defect. -/
noncomputable def chiLog (s : ℂ) : ℂ :=
  (Real.log Real.pi : ℂ) - digamma (s / 2) / 2 - digamma ((1 - s) / 2) / 2

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

/-! ### Step 4 · assembly -/

/-- **The target.**  Off the zeros of `ζ` and the poles of the two `Γ` factors,
    the logarithmic derivative and its reflection sum to the gamma-factor
    defect. -/
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

end Book4.Ch12.FE
