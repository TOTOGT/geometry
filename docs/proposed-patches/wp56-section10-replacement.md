# Proposed replacement for book7/wp56 §10 (DRAFT for Pablo's review; page NOT edited)
Evidence: book7/wp56_audit_check.py (6 PASS, 1 hand note). Status labels follow the page's convention.

## §10 Common causal receivers, and what a merger adds

**What stays true [VERIFIED, SR].** "Now in Andromeda" has no frame-independent answer: events at spacelike separation have no invariant order, and a 5 km/h walk shifts the Andromeda simultaneity slice by about 0.012 yr (4 days). This is the Andromeda argument (Rietdijk 1966, Putnam 1967; popularised by Penrose 1989 — verify the original attribution before publication; the page's earlier "Penrose 1960" is likely wrong).

**Proposition 10.1 (common causal receiver) [PROVED, elementary].** Let A=(0,−d/2) and B=(0,d/2) in a Minkowski frame, M=(T,0). Then s²(A,B)=d²>0 for all time: A and B stay spacelike. s²(A,M)=s²(B,M)=−c²T²+d²/4, so for T>d/2c both A and B lie in the timelike past of M (null at T=d/2c). With d=2.537 Mly, d/2c=1.2685 Myr. No event pair changes causal type; M is simply a third event that both can reach.

**Definition 10.2 (integration time of an observer).** For an observer worldline γ with a stated proper-time origin (so both where reception occurs and whose clock measures it are fixed) and bounded histories H_A,H_B with an explicit cutoff: T_CI[γ;H_A,H_B] = inf{τ : H_A∪H_B ⊆ J⁻(γ(τ))}, +∞ if none. It depends on γ and on the cutoff of the histories, is coordinate-independent once they are fixed, and measures causal accessibility, not transmitted information.

**Proposition 10.3 (stationary receiver) [PROVED, elementary].** For compact H and a receiver at rest at y: T_CI(y)=max over (t,x)∈H of t+|x−y|/c. For two simultaneous point sources a midpoint receiver gives d/2c = 1.2685 Myr.

**Consequence.** A merger billions of years later cannot be the first common-receiver event. Sharing a bound system does not give its stars a frame-independent present, so the merger does not resolve the Andromeda argument; the simultaneity problem reappears for any remaining spatially separated pair. FRW cosmic time (comoving observers) is the physical slicing, already noted above.

**Merger, separately [MODEL, conditional].** Define T_merge by an explicit dynamical criterion and ask how coalescence changes the spread of reception delays among observers in the remnant. That is a research question, not a change of causal type. The merger itself is not assured: Sawala et al. (2025, Nature Astronomy) report roughly a 50% chance of no merger within 10 Gyr (press coverage read, paper not read), so the "4.5–5 Gyr" timing needs to be conditional.

**Literature [OPEN, narrowed].** Sheffer, "Andromeda's New Clothes: Revealing the Causality Hidden in the Paradox" (PhilSci Archive 19464; mp_arc 22-82 listed 18 Dec 2022; manuscript submission date reported as 13 Aug 2021, second-hand; journal publication not established; abstract read here, full text not accessible to this session) already gives the paradox a future-light-cone reading, so a general light-cone treatment is not new. Whether the observer-specific, history-cutoff formulation of T_CI adds anything beyond standard causal geometry, or whether it appears in the full Sheffer text, is undetermined.
