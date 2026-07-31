# The Forced Urgency Gap — Pilot Audit Scope

**Jurisdictions: Newark, NJ + New York, NY · G6 LLC · July 2026 · Draft 0.1**

## Thesis (one paragraph)

Corporate landlords, banks, insurers, and transaction platforms extract value
from urban residents through a shared mechanism: they convert *time pressure*
into price. The household that must close this week, insure by renewal date,
rent by the first of the month, or sell before payday accepts worse terms than
the institution that can wait. The Forced Urgency Gap (FUG) is the measurable
spread between the price the urgent party gets and the price the patient party
gets. Fix the root — the asymmetry of urgency — and the rest of the tree takes
care of itself. This pilot makes the gap measurable for two cities.

## Why Newark + NYC first

Newark is home turf, an MGI (guaranteed-income pilot) city, and the national
extreme case: the Rutgers CLiME *Who Owns Newark?* study found **~47% of
1–4-unit residential sales (2017–2020) went to institutional buyers — the
highest rate in the nation**, tripled from under 20% in 2010. NYC is the
adjacent data-rich contrast case: Local Law 18 (2023) produced a natural
experiment in STR removal, and its open-data infrastructure (ACRIS deeds,
HPD, evictions data) is the best in the country. One extreme case + one
data-rich case = a defensible method paper.

## The four channels of the index

Each channel gets a per-city score from public data. No procurement needed
for the prototype.

**1. Ownership concentration (the landlord channel).**
Share of residential sales and stock held by institutional/LLC buyers.
Data: Essex County deed records; NJ property tax lists (public); NYC ACRIS +
PLUTO; Rutgers CLiME baseline for Newark. Metric: institutional share of
sales, LLC share of rental stock, median hold time.

**2. Displacement velocity (the eviction channel).**
Eviction filings per 1,000 renter households and filing-to-judgment speed —
urgency weaponized as legal tempo. Data: Eviction Lab (Princeton), NJ courts,
NYC OCA filings via open data. Metric: filings rate, serial-filing share
(same landlord refiling as rent-collection tactic).

**3. Risk repricing (the bank/insurer channel).**
Insurance non-renewals, premium growth vs. income growth, branch/lending
deserts. Data: NAIC/state DOBI complaint and non-renewal data, HMDA lending
data by tract, FDIC branch locations. Metric: premium-to-income delta,
non-renewal rate, denial-rate spread by tract.

**4. Platform extraction (the intermediation channel).**
Every transaction that used to be peer-to-peer now passes through a
fee-taking platform: Airbnb (host ~3% + guest ~14%), delivery apps (15–30%
of restaurant revenue), Facebook Marketplace (selling fees), payment apps.
Housing sub-channel: STR conversion of long-term stock. Data: Inside Airbnb
(free per-city listing scrapes; NYC covered — includes the LL18 before/after),
platform fee schedules (public), NYC STR registration data. Metric: estimated
annual fee dollars extracted per capita + housing units lost to STR.
*Note: platform presence is global (Airbnb: 150k+ cities), which is what
makes the index exportable — the 450×n path runs through this channel.*

## Composite

FUG score = weighted composite of the four channel scores, normalized so a
city can be compared to itself over time and to peer cities. Weighting is the
methodological contribution of the paper — candidate approach: weight by
estimated dollars extracted per household per year, so the index reads in
dollars, not abstractions. A city official should be able to say: "the
Forced Urgency Gap costs the median Newark renter household $X/year."

## Deliverables (pilot)

1. **Method paper**: *The Forced Urgency Gap: A Measurable Index* — Zenodo
   DOI, open method (CC), Newark + NYC as worked examples.
2. **Two city scorecards**: 4-page audit per city, all four channels, in
   dollars.
3. **Reproducible pipeline**: Python + open data, published (the same
   paper → DOI → code → verification pattern as the Principia corpus).

## Four-week plan

Week 1 — Data pull: CLiME baseline, Eviction Lab, Inside Airbnb NYC, ACRIS
sample, NJ DOBI insurance data. Week 2 — Channel metrics computed; draft
weighting. Week 3 — Scorecards + method paper draft. Week 4 — Review, DOI
deposit, one-pagers for the two natural first readers: Newark's Mayor's
Office (housing/EDC) and NYC Comptroller's office (which already publishes
institutional-ownership research).

## Who buys this (after the pilot exists)

Not sold as "equity consulting" — sold as a **cost-of-living diagnostic**:
what does forced urgency cost your median household per year, and which lever
(deed, docket, premium, platform fee) is cheapest to pull. First distribution
through networks, not RFPs: MGI (Newark is a member), GARE convenings,
What Works Cities. The RFP route opens once two published scorecards exist as
past performance.

## Anchor facts (verified this session)

- Newark institutional-buyer share of 1–4-unit sales, 2017–2020: **~47%**,
  highest in the U.S.; ~2,500 homes; up from <20% in 2010. (Rutgers CLiME,
  *Who Owns Newark?*, Troutt & Nelson, May 2022.)
- Airbnb operates in **150,000+ cities, ~220 countries**; 8M+ active
  listings — the extraction mechanism is structural, not local.
- NYC Local Law 18 (Sept 2023) removed the large majority of short-term
  listings — the before/after is a free natural experiment sitting in
  Inside Airbnb's archives.

---
*G6 LLC · Newark NJ · g6llc@proton.me · draft for discussion — not yet a
public document.*
