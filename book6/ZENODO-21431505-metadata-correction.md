# Zenodo record 10.5281/zenodo.21431505 — metadata correction

**Record:** *Transamerican smoke: mixed-layer collapse and the locus of order-dependence
in surface exposure: The July 2026 Canadian wildfire episode over New York*
**Published:** 18 July 2026 · v1.0 · Preprint · CC BY 4.0
**URL:** <https://zenodo.org/records/21431505>

**Status: DRAFT — NOT DEPOSITED.** Per the house rule, a correction to a published
Zenodo record is the author's call. This file is the text to paste; nothing has been
submitted to Zenodo from this repository.

---

## Why

The record carries the phantom *series DOI* in two places. `10.5281/zenodo.19117399`
is **Vol I's concept DOI** — it is not a series DOI, and a concept DOI resolves to
whichever version was deposited most recently, so it pins nothing even for Vol I.

This is the same defect tracked in `CLAUDE.md` ("Blast radius of the phantom series
DOI"), but here it has escaped the repository into published metadata, where a reader
meets it first and where OpenAIRE has already indexed the `IsPartOf` relation.

**There is no series-level DOI.** The series-wide pointer is the Zenodo community.

---

## Field 1 — Description

### Current (first line of the abstract block)

```
FIFA World Cup 2026™ - Principia Orthogona Series GROSSI 2026
DOI (series): 10.5281/zenodo.19117399
Companion chapter:
```

### Replace with

```
Principia Orthogona Series · GROSSI 2026
Series: Zenodo community — Principia Orthogona
https://zenodo.org/communities/principia-orthogona
(There is no series-level DOI. 10.5281/zenodo.19117399 is Vol I's concept DOI
and was previously shown here in error.)
Companion chapter:
```

Everything from **"WEBPAGE: Transamerican smoke…"** onward is correct and should be
left exactly as it is — including the link to
`https://totogt.github.io/geometry/book5/chV-saturn-smoke.html`, which resolves and
is reciprocal.

The `FIFA World Cup 2026™` string appears to be stray and unrelated to the paper.
Recommend deleting it, but that is a separate editorial decision and not part of the
defect being corrected here.

---

## Field 2 — Related works

### Current

| Relation | Type | Identifier |
|---|---|---|
| Is part of | Preprint | `10.5281/zenodo.19117399` (DOI) |

### Replace with — option A (preferred)

Delete the `Is part of` relation entirely, and add:

| Relation | Type | Identifier |
|---|---|---|
| Is published in | Other | `https://zenodo.org/communities/principia-orthogona` (URL) |

Zenodo community membership is the correct mechanism for "belongs to this series";
a DOI relation is not, because the series has no DOI.

### Replace with — option B (if a DOI relation is required by a downstream system)

| Relation | Type | Identifier |
|---|---|---|
| Is supplement to | Publication | `10.5281/zenodo.19117400` (DOI) |

`19117400` is Vol I's **v1 founding deposit** — a fixed, frozen version rather than a
concept DOI. It is defensible as "the deposit this series began from," but it is *not*
a parent record, so `Is supplement to` is more accurate than `Is part of`.

**Do not** use `19117399` in any relation. It is a concept DOI: the target moves on
every new Vol I deposit, so the relation silently changes meaning over time.

---

## Field 3 — Communities

The record currently shows no community membership. If it is intended to sit in the
series, add it to **Principia Orthogona** —
<https://zenodo.org/communities/principia-orthogona>.

This also matters for the count: the community is described elsewhere in the corpus as
holding 6 records, and deposits that were never added to it are invisible to anyone
browsing the series.

---

## Unchanged — verified correct, do not edit

- Title, authors, ORCID `0009-0000-6496-2186`, affiliation G6 LLC
- Publisher `G6 LLC - Newark, NJ 07104`, licence CC BY 4.0, resource type Preprint
- Files: `smoke_transamerican_v1.pdf` / `.tex`, `SmokeBox.lean`
- The `Continues` / `Is supplement to` / `Is variant form of` GitHub relations
- The entire scientific abstract from "Between 13 and 19 July 2026…" onward

---

## After depositing

Zenodo edits to metadata do not mint a new DOI, so `10.5281/zenodo.21431505` stays
valid and no citation elsewhere needs updating. Record the correction in `CLAUDE.md`
under the phantom-DOI ledger, noting that the blast radius included published
metadata and not only repository files.

*Drafted 2026-08-12 · checked against the Zenodo record the same day.*
