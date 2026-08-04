# WP-38 · Mathematical supplement

**Repairing Proposition 1′, closing Theorem 1(ii), and locating the invariant**

Pablo Nogueira Grossi · G6 LLC · 2026-08-01
Supplement to *Positional Dominance under Non-Contestability* (WP-38, DOI 10.5281/zenodo.21752834)
Builds on Grossi (2026a) v2, DOI 10.5281/zenodo.21753025

Claims tagged `[VERIFIED]` (closed form, checked) · `[MODEL]` (proved within the
model) · `[SIMULATION]` (numeric only) · `[OPEN]`.

---

## 0. Summary of what is new here

1. The divergence step of Proposition 1′ is **false as drafted** and repaired by
   restoring β to J's benefit term. `[VERIFIED]`
2. Restoring β **simultaneously dissolves** the unit inconsistency that v2 recorded
   as its "discarded observation". One edit closes two defects. `[VERIFIED]`
3. Existence gets an exact, interpretable condition, and the option value gets a
   closed form under Gaussian shocks. `[MODEL]`
4. **Theorem 1(ii) is closed in closed form.** WP-38 asserts only that some critical
   hazard λ̄ ∈ (0,1) exists. It is
   $$\bar\lambda \;=\; \frac{1-\delta}{\delta}\left(\frac{A_J}{A_V}-1\right)$$
   and in v2's normalisation it collapses to `λ̄ = ((1−δ)/δ)·γ/(1−γ)`. `[VERIFIED]`
5. **λ̄ contains no β, no τ, no c_K, no κ.** σ* is calibration-bound; λ̄ is not.
   If the corpus wants a transferable constant, this is where to look — not at
   σ* ≈ 1/3. `[VERIFIED]`
6. Corollary 1's four signs are proved by the implicit function theorem and
   confirmed numerically. `[MODEL]` + `[SIMULATION]`
7. c_K is **identified** by σ*, and the implied value is ~37× the ansatz-implied b.
   A live discrepancy that the calibration must resolve. `[OPEN]`
8. HODL is the model's cleanest instance, and "not your keys, not your coins" is
   literally the statement λ > 0. It supplies a **sixth event class** — λ-jumps —
   which is the sign-mirror of the five λ-collapses. `[MODEL]`

---

## 1. The repair

### 1.1 What is wrong

`positional-dominance-formal-section.md` §1 sets

$$\pi_J(q;X) = (|X|-\tau)|q| - c_K, \qquad \pi_V(v;X) = \beta(1-\gamma)\min(v,1)|X| - \tfrac12 v^2 .$$

β appears on V's side and not on J's. Three consequences:

**(a) The asymptotic slopes reverse.** For symmetric atomless `F` with `E|ξ| = κ`,

$$\mathbb E[(\sigma|\xi|-\tau)^+] \;=\; \kappa\sigma - \tau + o(1), \qquad \sigma\to\infty,$$

so `Π_J` is convex but **asymptotically affine**, slope `Kκ`. Against `Π_V`'s slope
`β(1−γ)κ` this gives `1.196` versus `3.051` under the paper's own calibration
(β = 8.5, γ = 0.55, K = 1.5, κ = √(2/π) = 0.79789). Hence `ΔV → −∞` and **no
threshold exists at all**. `[VERIFIED]`

Numerically, ΔΠ at σ = 0.33, 1, 2, 5, 10, 25, 50, 100:
`−0.51, −2.53, −5.10, −11.30, −20.81, −48.77, −95.18, −187.92` — negative and
falling throughout. `[SIMULATION]`

**(b) "Grows superlinearly" is false** independently of (a). A call's value is
convex but asymptotically linear in the scale parameter. The conclusion cannot rest
on superlinearity; it must rest on the slope gap.

**(c) Dimensions do not match.** J's benefit is `$/bbl × bbl`; V's is `$/bbl × $/bbl`.

### 1.2 The corrected primitive

$$\boxed{\;\pi_J(q;X) = \big(\beta|X|-\tau\big)^+|q| - c_K\;}$$

so that

$$\Pi_J(\sigma) = K\,\mathbb E\big[(\beta\sigma|\xi|-\tau)^+\big] - c_K
\;\xrightarrow[\sigma\to\infty]{}\; K(\beta\kappa\sigma-\tau),$$

which is exactly v2's Lemma 3.4 form `Π_J ∼ βκσ − τK`. The two documents now agree.
`[MODEL]`

### 1.3 Closed form under Gaussian shocks `[VERIFIED]`

For `ξ ~ N(0,1)`, write `a ≡ τ/(βσ)` and

$$g(a) \;\equiv\; \mathbb E\big[(|\xi|-a)^+\big] \;=\; 2\varphi(a) - 2a\,Q(a), \qquad Q = 1-\Phi .$$

Then

$$\Pi_J(\sigma) \;=\; K\beta\sigma\, g\!\left(\frac{\tau}{\beta\sigma}\right) - c_K .$$

Checks: `g(0) = 2φ(0) = √(2/π) = κ` ✓ (verified to machine precision);
`g′(a) = −2Q(a)`, so `g(a) = κ − a + O(a²)` and `Kβσg(τ/βσ) = Kβκσ − Kτ + O(1/σ)`,
recovering §1.2 exactly.

---

## 2. Existence, exactly

> **Theorem A (existence).** `[MODEL]`
> Let `A_J`, `A_V` be the asymptotic slopes of `Π_J`, `Π_V` in σ. Under
> non-contestability, `ΔΠ(0) = −c_K < 0`, and `σ*` with `ΔΠ(σ*) = 0` exists iff
> $$A_J > A_V .$$
> In v2's normalisation (J's benefit coefficient β at `k = K/K̄ = 1`, V's `β(1−γ)`)
> this is `β > β(1−γ)`, i.e. **γ > 0** — v2's Lemma 3.4 condition, recovered.
> In WP-38's normalisation (J's coefficient `K`) it is **K > 1 − γ**, i.e.
> `1.5 > 0.45` ✓.

**Normalisation conflict, must be reconciled.** v2 writes J's benefit with `K/K̄`
(dimensionless, `= 1` at the optimum); WP-38's formal section writes it with `K`
(MMbbl/d). The existence condition, and every number downstream, depends on which
is meant. This is an editorial decision, not a mathematical one — but it must be
made before deposit, because the two give different λ̄ (§4). `[OPEN]`

---

## 3. Uniqueness, and where it is still open

`Π_V` is quadratic on `[0, σ̄]` and affine above, with
`σ̄ = 1/(β(1−γ)κ) = 0.327664`. At `σ̄` the branches meet and `Π_V(σ̄) = ½` exactly,
since `β(1−γ)κσ̄ = 1` by construction. `[VERIFIED]`

Above `σ̄`: `Π_J` strictly convex, `Π_V` affine ⟹ `ΔΠ` strictly convex, negative
somewhere, divergent ⟹ **exactly one root**. This is WP-38's argument and it is
sound in that region. `[MODEL]`

Below `σ̄` both are convex, so convex-minus-convex gives nothing. The analogue of
v2's condition (C):

> **Condition (C′).** `[VERIFIED]` No root below saturation iff
> $$K\beta\bar\sigma\,g\!\left(\frac{\tau}{\beta\bar\sigma}\right) - c_K \;\le\; \tfrac12,
> \qquad\text{i.e.}\qquad c_K \;\ge\; 0.65766$$
> under the calibration (the gross option value at `σ̄` is `1.15766`).

> **Observation.** `[SIMULATION]` Scanning `c_K ∈ {0, 0.018, 0.1, 0.3, 0.5, 0.669,
> 0.9, 1.5}` the root is **unique in every case**, including the five where it lies
> below `σ̄` and (C′) fails. The model appears better behaved than the proof
> establishes.

> **Open.** `[OPEN]` Uniqueness on `(0, σ̄)` when (C′) fails. A sufficient route:
> `Π_J − Π_V` has a strictly increasing derivative wherever `Π_J′ > Π_V′` at the
> first crossing — i.e. single-crossing rather than convexity. Not attempted here.
> Do not upgrade the `[SIMULATION]` tag without it.

---

## 4. Theorem 1(ii) in closed form — the main new result

WP-38 states only: *"there exists `λ̄ ∈ (0,1)` such that for `λ > λ̄` no finite σ*
exists."* It can be computed.

Under hazard λ, `W_J = Π_J/(1-\delta(1-\lambda))` while `W_V = Π_V/(1-\delta)`.
Write `ρ(λ) = (1−δ)/(1−δ+δλ) ∈ (0,1]`, so `(1−δ)ΔW_λ = ρ(λ)Π_J − Π_V`. A threshold
exists iff the slope condition survives the discount: `ρ(λ)A_J > A_V`. Solving,

> **Theorem C.** `[VERIFIED]`
> $$\boxed{\;\bar\lambda \;=\; \frac{1-\delta}{\delta}\left(\frac{A_J}{A_V}-1\right)\;}$$
> and in v2's normalisation, where `A_J/A_V = 1/(1-\gamma)`,
> $$\bar\lambda \;=\; \frac{1-\delta}{\delta}\cdot\frac{\gamma}{1-\gamma}.$$

**Numbers.** `[VERIFIED]`

| Normalisation | `A_J/A_V` | λ̄ per month | annualised |
|---|---|---|---|
| v2 (`A_J = β`) | 2.222 | **0.018613** | 20.2% |
| WP-38 (`A_J = K`) | 3.333 | **0.035533** | 35.2% |

Independent numerical confirmation, by bisecting on `sup_σ [ρ(λ)Π_J − Π_V] = 0`
over a 8,000-point σ grid: `0.035513` against the closed form's `0.035533` —
agreement to **0.056%**. `[SIMULATION]`

### 4.1 Why this matters more than σ*

**λ̄ contains no β, no τ, no c_K, no κ.** Price impact, transport cost, carrying
cost and shock dispersion all cancel. λ̄ depends only on the discount factor and the
information/capacity ratio. `[VERIFIED]`

This is the direct answer to §7.2 of WP-38 and §6.2 of v2. Those sections withdraw
σ* ≈ 1/3 as an invariant because the sensitivity table moves it over [0.24, 0.43] —
correctly, since σ* is denominated in the units of a particular bottleneck. **λ̄ is
not.** It is a pure number in (0,1), comparable across a pipeline, an exchange and a
job. If there is a transferable constant in this family, the search should move here.

Whether λ̄ takes any distinguished value is open and should not be asserted. What is
established is only that λ̄ is the dimensionless object and σ* is not.

### 4.2 The patience result

$$\frac{\partial\bar\lambda}{\partial\delta} = -\frac{1}{\delta^2}\left(\frac{A_J}{A_V}-1\right) < 0 . \qquad \texttt{[VERIFIED]}$$

| δ | 0.90 | 0.95 | 0.985 | 0.999 |
|---|---|---|---|---|
| λ̄ | 0.1358 | 0.0643 | 0.0186 | 0.0012 |

**The more patient the positional player, the less preemption risk the strategy can
absorb.** This is counterintuitive and it is not an artifact: as `δ → 1`, J's value
is divided by `1−δ+δλ → λ` while V's is divided by `1−δ → 0`, so the ratio collapses
for any `λ > 0`. Patience amplifies the damage of hazard rather than buffering it.

Practical reading: a long-horizon holder needs *more* security than a short-horizon
one, not less. At δ = 0.999 the position must be secure to 99.88% per period.

---

## 5. Corollary 1, proved

At a crossing from below, `∂ΔΠ/∂σ > 0`, so by the implicit function theorem
`sign(∂σ*/∂θ) = −sign(∂ΔΠ/∂θ)`. `[MODEL]`

| θ | `∂ΔΠ/∂θ` | sign `∂σ*/∂θ` | numeric (+5% shock) |
|---|---|---|---|
| `c_K` | `−1` | **+** | +0.00686 ✓ |
| `K` | `βσ g(τ/βσ) > 0` | **−** | −0.01133 ✓ |
| `τ` | `−K·P(βσ\|ξ\|>τ) < 0` | **+** | +0.01475 ✓ |
| `γ` | `+βκσ > 0` | **−** | −0.01165 ✓ |

All four of Corollary 1's asserted signs hold, now with derivations rather than
assertions. `[MODEL]` + `[SIMULATION]`

---

## 6. Identification of c_K — an open discrepancy

With the corrected `Π_J`, σ* is a strictly increasing function of `c_K`: `[SIMULATION]`

| `c_K` | 0.018 | 0.10 | 0.30 | 0.50 | **0.669** | 1.00 | 2.00 |
|---|---|---|---|---|---|---|---|
| σ* | 0.1647 | 0.1956 | 0.2495 | 0.2944 | **0.3300** | 0.3940 | 0.5627 |

So **c_K is identified by σ***. Inverting at the reported σ* = 0.33 gives

$$c_K = 0.66893 \quad\Longrightarrow\quad b = c_K/(1-\delta) = 44.6 .$$

v2 reports `b = 1.208` (back-solved from v1's analytical root 0.665). The structural
model and the ansatz therefore disagree about the carrying cost by a factor of ~37.
`[OPEN]`

Three possibilities, and the calibration must choose: (i) the ansatz coefficients
`a, b` are not the structural ones and should not be quoted as such; (ii) `c_K` is
genuinely of order 0.67 in these units and v2's `b` is an artifact of the superseded
root; (iii) the normalisation conflict of §2 accounts for it. **This is v2 §3.3's
identification test, run from the structural side, and it does not come out clean.**
It should be resolved before either record is treated as calibrated.

Note also that at `c_K = 0.669` the root sits at `σ* = 0.3300` against
`σ̄ = 0.32766` — the threshold and the saturation point nearly coincide. Whether
that is mechanism or coincidence is unresolved; §7 argues it is not the 1/3
coincidence v2 discarded.

---

## 7. The unit inconsistency v2 recorded, dissolved

v2 records a "discarded observation": `σ̄ = [β(1−γ)κS]⁻¹ = 0.3277` at `S = 1`, an
inviting explanation for the threshold sitting near a third — killed because `S = 1`
is inconsistent with `τ = 2`, requiring a six-sigma shock before J could trade.

**Restoring β to J's payoff removes the inconsistency.** With
`Π_J = K·E[(βσ|ξ| − τ)⁺] − c_K`, the strike ratio at σ = 0.33 is

$$a = \frac{\tau}{\beta\sigma} = \frac{2}{8.5\times0.33} = 0.7181,$$

so exercise requires `|ξ| > 0.72`, which has probability 0.47. **The option is
live.** β now plays the scale role on *both* sides, where before it appeared only in
V's saturation. `[VERIFIED]`

This does not resurrect the numerological reading — `σ̄` still moves with β, γ and κ,
so it is no more a constant than σ*. What it does is remove the *reason* v2 gave for
discarding it, which means the near-coincidence `σ* ≈ σ̄` in §6 needs a proper
explanation rather than a dismissal. `[OPEN]`

---

## 8. HODL

The model's cleanest instance outside pipelines, and the one that makes λ observable.

| Model object | Midstream | HODL |
|---|---|---|
| position `h` | hub ownership | the coins |
| `λ` | preemption hazard | **custody risk** — the rate at which the position is lost while inactive |
| `σ` | spread volatility | asset volatility |
| `c_K` | tankage, O&M, insurance | custody cost, opportunity cost of capital |
| `v` | speed investment | active trading effort |
| saturation `min(v,1)` | latency floor | the point past which more screen time buys no edge |

**"Not your keys, not your coins" is the statement λ > 0.** Self-custody is an
attempt to set `λ = 0` by construction; exchange custody accepts `λ > 0` in exchange
for convenience. The model says this is not a preference but a regime switch: below
λ̄ the passive holder strictly dominates the active trader above σ*; above λ̄ **no
volatility whatever makes holding dominant.**

With v2's normalisation, `λ̄ = 1.86%` per period — annualised ~20%. `[VERIFIED]`
Whether real custody arrangements sit above or below that is an empirical question
with an available answer: exchange failure, freeze and haircut histories give a
per-period hazard directly. Mt. Gox, QuadrigaCX, Celsius and FTX are realised draws.
Estimating λ from that record is the natural companion to §8 of WP-38. `[OPEN]`

**Do not transfer σ* to crypto.** σ* = [0.30, 0.36] is a midstream calibration in
units of β, τ and c_K specific to a pipeline. Quoting it against BTC volatility
without re-estimating those three is exactly the error §7.2 retires. What transfers
is the structure — `A_J > A_V` for existence, `λ < λ̄` for the regime — because λ̄ is
dimensionless and σ* is not.

### 8.1 A sixth event class: λ-jumps

WP-38's five events are all cases where **λ collapses to zero** — flights grounded,
tankage committed, wellheads frozen, canal drafted down, stock cornered. Every one
tests the same sign.

The HODL reading supplies the mirror: events where **λ jumps up** on an
otherwise-unchanged position. Custody freezes, exchange halts, withdrawal
suspensions, capital controls, asset seizure. The model predicts the *opposite*
sign — `∂W_J/∂σ` should fall discontinuously, and holders should shift toward
participation, not away.

This is a stronger test than adding a sixth λ-collapse. Five events sharing one sign
can be explained by any theory that makes bottlenecks valuable; a sixth with the
**reverse** sign, generated by the same parameter moving the other way, cannot.
Event 5 (LME nickel, trades cancelled) already sits on this boundary — WP-38 calls
it a boundary case, and under this reading it is better classified as the first
λ-jump: the exchange restored contestability by fiat. `[MODEL]`

---

## 9. Ledger

| # | Claim | Tag |
|---|---|---|
| 1 | Drafted Prop 1′ divergence fails; ΔΠ → −∞ under the calibration | `[VERIFIED]` |
| 2 | `E[(σ\|ξ\|−τ)⁺] = κσ − τ + o(1)`; convex, asymptotically affine | `[VERIFIED]` |
| 3 | `Π_J = Kβσ·g(τ/βσ) − c_K`, `g(a) = 2φ(a) − 2aQ(a)`, `g(0) = κ` | `[VERIFIED]` |
| 4 | Existence ⟺ `A_J > A_V` (⟺ γ > 0 in v2's normalisation) | `[MODEL]` |
| 5 | `Π_V(σ̄) = ½` exactly; condition (C′) `c_K ≥ 0.65766` | `[VERIFIED]` |
| 6 | Uniqueness above σ̄ | `[MODEL]` |
| 7 | Uniqueness below σ̄ when (C′) fails | `[OPEN]` |
| 8 | `λ̄ = ((1−δ)/δ)(A_J/A_V − 1)`; matches numerics to 0.056% | `[VERIFIED]` |
| 9 | λ̄ independent of β, τ, c_K, κ | `[VERIFIED]` |
| 10 | `∂λ̄/∂δ < 0` — patience reduces hazard tolerance | `[VERIFIED]` |
| 11 | Corollary 1's four signs | `[MODEL]` |
| 12 | `c_K = 0.669` implied by σ* = 0.33; vs v2's `b = 1.208` | `[OPEN]` |
| 13 | β on both sides dissolves v2's S-inconsistency | `[VERIFIED]` |
| 14 | `σ* ≈ σ̄` at the identified `c_K` — mechanism or coincidence | `[OPEN]` |
| 15 | HODL mapping; λ estimable from custody-failure records | `[MODEL]` / `[OPEN]` |
| 16 | λ-jump events as the sign-mirror test | `[MODEL]` |
| 17 | Normalisation conflict `K` vs `K/K̄` between v2 and WP-38 | `[OPEN]` |

No claim above is machine-checked in Lean. Nothing here should be marked
`✓ Lean 4`. Numerics: `ξ ~ N(0,1)`, 4×10⁶ draws for the Monte-Carlo checks,
closed-form Gaussian elsewhere; β = 8.5, τ = 2.0, K = K̄ = 1.5, γ = 0.55, δ = 0.985.
