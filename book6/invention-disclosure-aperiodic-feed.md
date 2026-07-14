# Invention Disclosure — Aperiodic Structured Nutrient Substrate

**Working draft for patent counsel. Not legal advice.** Claims below are illustrative skeletons to be reviewed, narrowed, and re-drafted by a registered patent attorney. See §7 (disclosure/priority) — public Zenodo/site/book disclosures have already started a clock.

**Inventor:** Pablo Nogueira Grossi · G6 LLC, Newark NJ · ORCID 0009-0000-6496-2186
**Related:** Book 6 · Ch DE-3 — [*Aperiodic Multiplying Media* (live chapter)](https://totogt.github.io/geometry/book6/ch-aperiodic-multiplying-media.html); Book 3 Ch η DNLS; companion criticality paper (Zenodo 10.5281/zenodo.20077205)

---

## 1. Field

Structured nutrient substrates, culture/fermentation media, animal feed, and bioreactor packings whose nutrient distribution is spatially ordered by an aperiodic (substitution) rule to control the growth-criticality (persistence/washout) threshold of a biological population.

## 2. The technical problem

Periodic or homogeneous nutrient substrates give a growth-criticality threshold that is fixed by composition alone and does not scale predictably from bench to plant. Cultures on lean or fluctuating feed drift toward washout with little design margin.

## 3. The invention (one sentence)

A nutrient substrate in which nutrient-bearing domains are arranged along a spatial axis by a **primitive substitution rule** of inflation order *n* (Fibonacci n=2, tribonacci n=3, …), so that the inflation eigenvalue λ_PF becomes a **design knob** setting the growth-criticality threshold — higher n raises the threshold, conferring robustness against nutrient fluctuation and making bioreactor criticality scale-covariant under inflation.

## 4. The unexpected effect (non-obviousness anchor)

The self-trapping / persistence threshold rises with n as a **difference in regime, not merely magnitude**: numerically λ_c(n) ≈ 0.958·Δ_n + 0.107 (r = 0.989), and a tribonacci ordering (η ≈ 1.8393 > φ ≈ 1.6180) holds a localized population together under leaner feed than a Fibonacci ordering of identical bulk composition. This surprising, structure-only advantage — same ingredients, different survival margin — is the §103 non-obviousness anchor.

---

## 5. Strongest asset — composition + method-of-use pair

### Independent composition claim

> **1.** A structured nutrient substrate for supporting biological growth, comprising a solid or gel matrix defining, along at least one spatial axis, a plurality of nutrient-bearing domains separated by interstitial transport regions, wherein the ordering of the nutrient-bearing domains along said axis follows a primitive substitution rule whose inflation matrix has a Perron–Frobenius eigenvalue λ_PF greater than 1, such that the local nutrient concentration profile along said axis is aperiodic and non-periodic with a characteristic domain-length ratio determined by said substitution rule.

Dependent narrowing:

> **2.** The substrate of claim 1, wherein the substitution rule is the tribonacci rule (a→ab, b→ac, c→a), so that λ_PF = η is the real root of x³ − x² − x − 1 = 0 in (1,2), η ≈ 1.8393.
>
> **3.** The substrate of claim 1, wherein the substitution rule is an n-bonacci rule with n ≥ 3, so that λ_PF > φ.
>
> **4.** The substrate of claim 1, wherein the nutrient-bearing domains have characteristic lengths between [X] and [Y] micrometres. *(fill from embodiment)*
>
> **5.** The substrate of claim 1, wherein the matrix comprises one of: a cross-linked hydrogel; an extruded feed pellet; an additively-manufactured (3D-printed) scaffold; a cast multilayer.
>
> **6.** The substrate of claim 1, **characterized in that** a mid-gap growth mode supported by the substrate has an inverse participation ratio at least K× that of a Fibonacci-ordered substrate of identical bulk composition. *(structural-functional limitation carrying the unexpected effect; set K ≈ 3.5–4 from data)*
>
> **7.** The substrate of claim 1, adapted as a scaffold for cultured animal cells for cultivated-meat production.

### Independent method-of-use claim

> **8.** A method of culturing a population of organisms, comprising: providing a structured nutrient substrate according to claim 1; inoculating the substrate with the organism; and maintaining culture conditions under which the population preferentially localizes onto the nutrient-bearing domains; wherein the inflation order *n* of the substitution rule is selected such that the persistence threshold of the population — the critical mean nutrient concentration, or critical patch contrast, below which the population washes out — is above a target value, thereby conferring robustness of the culture against fluctuation in nutrient supply.

Dependent:

> **9.** The method of claim 8, comprising selecting n = 3 rather than n = 2 to raise the persistence threshold.
>
> **10.** The method of claim 8, wherein the organism is a microbial fermentation strain, a probiotic culture, or a mammalian cell line.
>
> **11.** The method of claim 8, wherein selecting the inflation order *n* comprises **fabricating** the substrate with a physical domain sequence of inflation order *n*. *(ties the selection to a physical act — see §6)*

---

## 6. Keeping the design-method claims out of §101

A claim reciting "computing λ_PF" or "selecting n to maximize a threshold" as a standalone step is a bare mathematical/mental operation and is abstract under *Alice/Mayo*. The fix is to **never claim the calculation alone** — always fold the design choice into a physical transformation with a measurable structural result:

### Independent method-of-manufacture claim (§101-safe form of the "design method")

> **12.** A method of manufacturing a structured nutrient substrate, comprising: determining a spatial domain sequence from a primitive substitution rule of inflation order *n*; and **depositing nutrient material** to form nutrient-bearing domains physically arranged in said sequence along a spatial axis, by additive manufacturing, extrusion, or layer casting, such that the resulting substrate exhibits an aperiodic nutrient-concentration profile whose characteristic domain-length ratio is set by λ_PF.

Here "determining the sequence" is a limitation on the *physical deposition step and the resulting article*, not a standalone claim element — the claim rises or falls on making a real object. That is the pattern that survives §101.

### Optional QA/QC method (pairs with bomb calorimetry)

> **13.** A method of qualifying a feed or substrate, comprising: measuring a caloric density of the substrate by oxygen-bomb calorimetry; determining, by structural characterization, the inflation order *n* of the domain sequence; and accepting the substrate when both the caloric density and the inflation order meet specification. *(a two-parameter spec: energy + robustness margin)*

---

## 7. Enablement and priority — action items

- **Enablement (§112).** The nutrition embodiment is currently *predicted, untested*. Before a broad filing, add at least one prophetic example and, ideally, one fermentation/culture run showing the threshold shift between n = 2 and n = 3 substrates of equal bulk composition. This converts claim 6's K× limitation from assertion to demonstration.
- **Novelty search (§102).** Run prior-art on: aperiodic/Fibonacci/quasicrystal structuring of feed, hydrogels, and scaffolds; structured bioreactor packing; patterned nutrient release; cultivated-meat scaffold geometry.
- **Priority / disclosure (§102(b) + foreign absolute novelty).** The framework has been publicly disclosed (Zenodo preprints, totogt.github.io, Book 6 chapter). US: a one-year grace period runs from the first disclosure *of the product embodiment*. Most foreign jurisdictions: absolute novelty — prior self-disclosure may already bar. **Gather the exact first-publication date of any text describing the physical feed/substrate (not just the abstract math), and treat a provisional filing as time-sensitive.**

## 8. Commercial embodiments (ranked)

1. **Cultivated-meat scaffolds** — structured nutrient/oxygen scaffolds for cell-ag; strong IP frontier; direct adjacency to JBS/Friboi cultivated-meat interests.
2. **Precision-fermentation feedstocks** — robustness against feed fluctuation in industrial fermentation.
3. **Structured animal-feed pellets** — engineered nutrient-release profile with a robustness margin.
4. **Biofilm carriers / water treatment** — aperiodic carrier media for wastewater cultures.
