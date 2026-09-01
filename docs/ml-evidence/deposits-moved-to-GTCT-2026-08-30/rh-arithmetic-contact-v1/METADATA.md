# Zenodo deposit — metadata to paste

**Reserved DOI:** 10.5281/zenodo.22179684 · **Version:** v1 · **Prepared:** 2026-08-30

---

## Upload type
Publication → **Preprint**

## Title
The Riemann Hypothesis as Non-Integrability of an Arithmetic Contact Structure on the Adele Class Space

## Authors
Pablo Nogueira Grossi · G6 LLC, Newark, New Jersey, USA · ORCID 0009-0000-6496-2186

## Publication date
2026-08-30

## Description
> We reformulate the Riemann Hypothesis (RH) as a non-vanishing condition on a globally
> defined arithmetic contact 3-form on the adele class space 𝔸_ℚ/ℚ^×. Starting from the
> classical 2D+t contact-geometry prototype of *Principia Orthogona* (Book 4, Chapter 2), we
> lift the Riemann zeta function to an extended arithmetic phase space, construct an explicit
> contact 1-form α_arith whose twisting coefficient is the von Mangoldt–Dirichlet series (or
> its meromorphic continuation), and decompose it into local contact forms α_v at each place
> of ℚ. The non-integrability condition α ∧ dα ≠ 0 — automatic in the smooth ODE setting —
> becomes, in the arithmetic setting, equivalent to a global positivity statement on the
> action of the idele class group on ker α. We compare this condition to Weil's explicit
> formula criterion, Connes' spectral-triple approach, and the function-field case where RH
> is proved, identifying where the final rung would need to sit.
>
> We further establish two reflection laws for the form's coefficients under the functional
> equation: g(σ,t) − g(1−σ,t) = Im[(χ′/χ)(σ+it)] and c(σ,t) + c(1−σ,t) = −Re[(χ′/χ)(σ+it)],
> verified numerically to 30 significant digits. On the critical line the second collapses to
> c(½,t) = ϑ′(t), the Riemann–Siegel theta derivative — a classical identity, equivalent to
> Z(t) being real-valued, credited as such — which identifies the d𝑈̃ coefficient of α_arith
> on the critical wall with the density of the Riemann–von Mangoldt counting formula. We show
> the pole of ζ′/ζ at each zero falls entirely into the d𝑉̃ component while the d𝑈̃ component
> remains analytic, and we refute the conjecture that the functional equation acts as a
> contactomorphism of α_arith, replacing it with a graded statement.
>
> **RH itself is untouched.** §4.6 gives a status-of-claims table separating what is proved,
> what is machine-checked in Lean 4, what is classical, and what is numerical only. The
> contribution is a translation dictionary between contact geometry and arithmetic.

## Version
v1

## Language
eng

## Keywords
Riemann Hypothesis · contact geometry · adele class space · von Mangoldt function ·
Riemann–Siegel theta function · Weil explicit formula · Connes spectral triple ·
p-adic differential forms · Lean 4 · formal verification · Principia Orthogona

## Subjects (MSC 2020)
- 11M26 — Nonreal zeros of ζ(s) and L(s, χ); Riemann and other hypotheses
- 53D10 — Contact manifolds, general
- 11R56 — Adèle rings and groups
- 81Q10 — Selfadjoint operator theory in quantum mechanics

## License
**Recommended: Creative Commons Attribution 4.0 International (CC BY 4.0)** — the standard
for preprints and the one that maximises citation and reuse.
⚠️ Note the corpus is inconsistent here: *Imaginary Origin* uses CC BY-NC-ND 4.0 and the Lean
files carry MIT. A preprint under NC-ND cannot be built on, which for a "translation
dictionary intended for researchers" works against the stated purpose. Pablo's call.

## Related identifiers
- **is supplemented by** — https://github.com/TOTOGT/geometry (repository)
- **is supplemented by** — https://github.com/TOTOGT/GTCT (Lean sources, `book4/ZetaReflection.lean`)
- **is part of** — https://totogt.github.io/geometry/book4/ch11.html (Book 4 Ch 11, public 2026-06-09)
- **is part of** — https://totogt.github.io/geometry/book4/ch12.html (Book 4 Ch 12, public 2026-06-09)

## Communities
Principia Orthogona

## Additional notes
Preprint, not peer reviewed. Numerical claims are reproducible by the included script
`verify_reflection_laws.py` (requires mpmath; runs in ~2 minutes; exits non-zero on any
failure). The Lean file `ZetaReflection.lean` compiles against Mathlib v4.32.0; one lemma is
proved and two statements are explicitly admitted — the file's header says which.

---

## Files in this deposit

| File | What it is |
|---|---|
| `RH_arithmetic_contact_structure.md` | The manuscript, 383 lines |
| `ZetaReflection.lean` | Lean 4 / Mathlib v4.32.0. `lseries_vonMangoldt_eq_neg_Zlog` **proved** on `[propext, Classical.choice, Quot.sound]`; `reflection_law` and `chiLog_real_on_critical_line` **admitted** (`sorryAx`) |
| `verify_reflection_laws.py` | Reproduces all four numerical claims of §4.4–§4.6. Last run 2026-08-30: **ALL CHECKS PASSED** |
| `METADATA.md` | This file — do not upload |

## Before publishing, check
- [ ] License decided (CC BY 4.0 recommended over the corpus's usual NC-ND)
- [ ] `python3 verify_reflection_laws.py` exits 0 on your machine
- [ ] `bash ~/Desktop/geometry/tools/leancheck.sh --audit ZetaReflection.lean` reports
      4 declarations, 2 trusting sorryAx
- [ ] ORCID and affiliation correct
- [ ] The DOI in the manuscript header matches the record being published
