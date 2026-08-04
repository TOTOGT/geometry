# WP-38 deposit — 10.5281/zenodo.21752834

Reserved DOI: **10.5281/zenodo.21752834** · Title: *Positional Dominance under Non-Contestability*

---

## A. Blockers — fix in the files BEFORE publishing

Zenodo: "File addition, removal or modification are not allowed after you have
published your upload." Everything below is baked in permanently at publish.

### A1. The HTML footer still carries the phantom series DOI

`book6/wp38-positional-dominance.html` line ~footer:

```html
Series DOI <a href="https://doi.org/10.5281/zenodo.19117399">…</a>
```

`19117399` is Vol I's **concept** DOI, not a series DOI. Publishing this bakes the
exact defect we spent today removing from the JOMO pack into an immutable record.

Replace with either:

```html
Series <a href="https://zenodo.org/communities/principia-orthogona">Principia Orthogona</a>
```

or drop the line — series membership is better expressed by submitting the record
to the community (see §B, "Communities").

### A2. `otium-jomo-generalization.md` mis-cites its own record

Header line 5 and the final reference both read:

> *Companion note. Extends Grossi (2026a), DOI 10.5281/zenodo.21752834.*

Two problems. `21752834` is **this record's own DOI** — the note is inside the
thing it claims to extend. And "Grossi (2026a)" denotes the network-games paper
everywhere else in the corpus (`21013066` v1 / `21753025` v2), so the label points
at one work and the DOI at another.

Correct to:

> *Companion note. Generalizes Theorem 1 of the present working paper
> (WP-38, DOI 10.5281/zenodo.21752834), which builds on Grossi (2026a) v2,
> DOI 10.5281/zenodo.21753025.*

### A3. `positional-dominance-formal-section.md` — Proposition 1′ does not go through

**The divergence step is false under the pack's own calibration.** §1 defines

```
π_J(q; X) = (|X| − τ)|q| − c_K          ← no β
π_V(v; X) = β(1−γ) min(v,1)|X| − v²/2   ← β present
```

β was dropped from J's benefit term. Consequences:

1. **Asymptotic slopes reverse.** `E[(σ|ξ|−τ)⁺]` is convex but *asymptotically
   affine*, → `σκ − τ`. So J's slope is `Kκ = 1.196` against V's
   `β(1−γ)κ = 3.051`. ΔV → **−∞**, not +∞, and no σ* exists.
   Checked numerically (4M draws, standard normal, κ = 0.7976, K = 1.5,
   β = 8.5, γ = 0.55, τ = 2): ΔV is negative and falling at every σ from
   0.33 to 100 — −0.51, −2.53, −5.10, −11.3, −20.8, −48.8, −95.2, −187.9.
2. **"Grows superlinearly" is wrong** even with β restored. A call's value is
   convex but asymptotically linear. The conclusion must rest on the *slope gap*,
   not on superlinearity.
3. Dimensions don't match either: J's benefit is `$/bbl × bbl`, V's is
   `$/bbl × $/bbl`.

**Fix:** restore β to J's benefit, as v2 has it (Lemma 3.4: `Π_J ∼ βκσ − τK`,
`Π_V ∼ β(1−γ)κσ − ½`, slope gap `βκγ > 0`). Then divergence holds — `Kβκ = 10.17`
vs `3.05` — and Proposition 1′ stands. Restate the divergence step as:

> Both payoffs are asymptotically affine in σ; J's slope exceeds V's by βκγ > 0,
> which is strictly positive precisely when γ > 0. Hence ΔV → +∞.

This is the same failure mode as the v1 defect being corrected: a sign/divergence
step asserted rather than checked. Worth catching before it is deposited.

---

## B. Form values

| Field | Value |
|---|---|
| Communities | **principia-orthogona** — submit the record here; this is the series link, not a DOI |
| Resource type | Publication → **Working paper** if the dropdown offers it (the paper self-describes as "Working paper · v1.0"); otherwise Preprint |
| DOI | 10.5281/zenodo.21752834 (reserved) |
| Title | Positional Dominance under Non-Contestability |
| Subtitle (into description) | Why the waiter beats the racer — and the one condition that decides it |
| Publication date | 2026-08-01 |
| Authors | Nogueira Grossi, Pablo — G6 LLC — ORCID 0009-0000-6496-2186 |
| Version | 1.0 |
| Language | eng |
| Publisher | G6 LLC |
| License | CC BY 4.0 |

### Keywords and subjects

```
positional dominance; non-contestability; preemption hazard; real options;
option exercise games; Markov perfect equilibrium; stochastic games;
market microstructure; high-frequency trading; volatility threshold;
chokepoint rents; energy midstream; Cushing; Panama Canal;
JEL C73; JEL D43; JEL G13; JEL L95
```

### Alternate identifiers

| Identifier | Scheme |
|---|---|
| https://totogt.github.io/geometry/book6/wp38-positional-dominance.html | URL |

### Related works

| Relation | Identifier | Scheme | Resource type |
|---|---|---|---|
| continues | 10.5281/zenodo.21753025 | DOI | Publication / Preprint |
| references | 10.5281/zenodo.21013066 | DOI | Publication / Preprint |
| is part of | https://zenodo.org/communities/principia-orthogona | URL | — |

Notes on the choices:

- **continues → 21753025 (v2)** — the paper builds on v2 and does not retract it.
- **references → 21013066 (v1)** — the record whose Proposition 1 is replaced.
  Deliberately *not* `obsoletes`: WP-38 supersedes one proposition, not the paper.
  Claiming `obsoletes` would overstate exactly the way the corrected text warns against.
- **Do not add 10.5281/zenodo.19117399 in any relation.** It is Vol I's concept DOI.
- If the two-work bundling in §C is resolved by splitting, add
  `isSupplementedBy → <Otium DOI>` here and `isSupplementTo → 21752834` there.

### References (paste into the References field, one per line)

```
Aquilina, M., Budish, E., & O'Neill, P. (2022). Quantifying the high-frequency trading arms race. Quarterly Journal of Economics, 137(1).
Budish, E., Cramton, P., & Shim, J. (2015). The high-frequency trading arms race: frequent batch auctions as a market design response. Quarterly Journal of Economics, 130(4), 1547-1621.
Dixit, A. K., & Pindyck, R. S. (1994). Investment under Uncertainty. Princeton University Press.
Fernandez-Perez, A., Fuertes, A.-M., & Miffre, J. (2021). The negative pricing of the May 2020 WTI contract.
Grenadier, S. R. (2002). Option exercise games: an application to the equilibrium investment strategies of firms. Review of Financial Studies, 15.
Huisman, K. J. M. (2001). Technology Investment: A Game Theoretic Real Options Approach. Kluwer.
Joskow, P., & Tirole, J. (2000). Transmission rights and market power on electric power networks. RAND Journal of Economics, 31.
Kyle, A. S. (1985). Continuous auctions and insider trading. Econometrica, 53.
Veblen, T. (1899). The Theory of the Leisure Class.
```

---

## C. Open question — two works, one record

The upload bundles two distinct works:

- `positional-dominance-paper.html` — WP-38, the formal result
- `otium-jomo-generalization.md` — the Otium note, which generalizes Theorem 1
  out of markets entirely (FOMO/JOMO, *otium/negotium*, wu wei, Sabbath,
  attention platforms as λ-inflation)

Bundled, the Otium note has no DOI of its own, cannot be cited independently, and
inherits WP-38's title and JEL codes — which do not describe it. It is a different
literature and a different audience.

If it is meant to be **WP-39**, deposit it separately with its own reserved DOI and
link the two with `isSupplementTo` / `isSupplementedBy`. If it is meant as an
appendix to WP-38, retitle the record to signal that it contains both, and say so
in the description.

Unresolved — needs your call before publishing.

---

## D. Description (paste as HTML into the Description field)

```html
<p><strong>Why the waiter beats the racer — and the one condition that decides it.</strong></p>

<p>Standard results in option-exercise games hold that competition erodes, and in
the limit dissipates, the option value of waiting. This paper identifies the single
condition under which that mechanism operates, and shows that where the condition
fails, volatility does the opposite of what the literature predicts.</p>

<p>A hub is <em>contestable</em> if some action available to the rival transfers
ownership, and <em>non-contestable</em> if none does; equivalently, the preemption
hazard &lambda; is zero. The positional player's payoff is a call on the spread
struck at transport cost, hence convex in volatility; the velocity player's is
affine once the latency cap binds. Convex minus affine, negative at the origin by
the carrying cost of position, gives a unique threshold &sigma;*. Theorem 1 shows
that preemption risk erodes the sensitivity of the positional advantage to
volatility, that above a critical hazard no threshold exists at all, and that at
&lambda; = 0 the full option value accrues to the position holder.</p>

<p><strong>The empirical claim is an interaction, not a level.</strong> Every model
predicts prices rise when supply breaks. This one predicts the <em>slope</em> of
positional returns against volatility jumps discontinuously when contestability
collapses. The proposed event set — COMEX&ndash;London gold (March 2020), the
negative WTI May contract (April 2020), Winter Storm Uri (February 2021), the
Panama Canal drought (2023&ndash;2026), and LME nickel (March 2022) — is chosen so
that every trigger is exogenous, the assets are unrelated, and two events have
opposite price signs while sharing one mechanism.</p>

<p><strong>Corrections carried by this paper.</strong> It replaces Proposition 1 of
Grossi (2026a) v1 (DOI 10.5281/zenodo.21013066), whose intercept was justified on
the ground that the velocity player earns positive rents at zero volatility — false
under the tabled payoffs, since volatility multiplies the benefit term for both
players. The correct source of the intercept is the capitalised fixed cost of
holding position. That correction is now also carried by v2
(DOI 10.5281/zenodo.21753025), on which this paper builds. Corollary 1 makes
&sigma;* an explicit function of carry, capacity, transport friction and
information, so it is a property of a particular bottleneck rather than a constant:
the cross-domain 1/3 invariance claim is withdrawn as evidence and retained only as
an open question.</p>

<p>Independent working paper; not peer-reviewed. Figures generated from model
primitives. Event magnitudes are reported from public sources and have not been
independently re-estimated.</p>

<p>Series: <a href="https://zenodo.org/communities/principia-orthogona">Principia
Orthogona</a> &middot; Vol VI &middot; Roots &middot; WP-38.
HTML edition: <a href="https://totogt.github.io/geometry/book6/wp38-positional-dominance.html">totogt.github.io/geometry/book6/wp38-positional-dominance.html</a></p>
```
