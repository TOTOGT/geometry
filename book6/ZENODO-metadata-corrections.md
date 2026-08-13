# Zenodo metadata corrections — DRAFTS, NOT DEPOSITED

Two live records carry the phantom series DOI. Neither has been amended;
amending a published record is the author's call (house rule 4).

| Record | Title | Defects |
|---|---|---|
| `10.5281/zenodo.21431505` | Transamerican smoke | series DOI ×2 |
| `10.5281/zenodo.20710023` | Alternating Forms Vanish Beyond Dimension (Alterna) | series DOI ×2, wrong ISBN |

---

## Record 1 — 10.5281/zenodo.21431505

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

## Verified 2026-08-12 from the record page — this record has BOTH DOIs

| DOI | Kind | Resolves to |
|---|---|---|
| `10.5281/zenodo.21431504` | **concept** | always the latest version |
| `10.5281/zenodo.21431505` | **version** (v1.0, 18 Jul 2026) | this text, frozen |

This was not visible from the metadata block alone; it appears on the record page as
*"Cite all versions? You can cite all versions by using the DOI 10.5281/zenodo.21431504."*

**Consequence — the repository citation is correct.** `book5/chV-saturn-smoke.html`
cites `21431505`, the **version** DOI. That is the right choice under the house rule:
cite a version DOI whenever the claim depends on what the text actually says. Do not
"upgrade" it to the concept DOI; that would repeat the `19117399` mistake in miniature.

Record both numbers in `CLAUDE.md` so a later pass does not treat `21431504` as
unknown, or mistake it for a second deposit.

**Zenodo's own suggested citation** (APA, from the record page), for reference:

> Nogueira Grossi, P. (2026). *Transamerican smoke: mixed-layer collapse and the locus
> of order-dependence in surface exposure: The July 2026 Canadian wildfire episode over
> New York* (Version 1.0). G6 LLC - Newark, NJ 07104.
> https://doi.org/10.5281/zenodo.21431505

The ABNT (NBR 6023) form of the same record, for the Vol V reference list:

> NOGUEIRA GROSSI, Pablo. **Transamerican smoke**: mixed-layer collapse and the locus of
> order-dependence in surface exposure: the July 2026 Canadian wildfire episode over New
> York. Versão 1.0. Newark: G6 LLC, 2026. Preprint. DOI: 10.5281/zenodo.21431505.
> Disponível em: https://doi.org/10.5281/zenodo.21431505. Acesso em: 12 ago. 2026.

Also noted from the record page: **Citations — "No citations found"**, and the record
is indexed in OpenAIRE. The OpenAIRE index carries the `IsPartOf` relation below, which
is the reason the phantom-DOI correction matters beyond Zenodo itself.

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


---

## Record 2 — 10.5281/zenodo.20710023 (Alterna)

**Record:** *Alternating Forms Vanish Beyond Dimension: A Mechanized Proof in Lean 4
with Application to Contact Integrability*
**Published:** 16 June 2026 · v1.0 · Preprint · CC BY 4.0 · G6 LLC
**URL:** <https://zenodo.org/records/20710023>
**Verified against the record:** 2026-08-12
**Chapter:** `book6/wp02-alterna.html`

### Defect 1 — the phantom series DOI, again

Two places, same as record 1:

- **Description**, final paragraph: `Series root: 10.5281/zenodo.19117399.`
- **Related works**: `Is part of → Preprint: 10.5281/zenodo.19117399 (DOI)`

`19117399` is Vol I's **concept** DOI. There is no series-level DOI. Replace the
Description line with the community URL, and drop or retarget the relation exactly as
set out for record 1 above.

**This is the second live deposit carrying it.** The blast radius recorded in
`CLAUDE.md` is therefore not confined to the repository — it reaches published,
OpenAIRE-indexed metadata on at least two records. Any deposit made from a template
containing that line should be checked before the next upload.

### Defect 2 — wrong ISBN

Description: `Part of the Principia Orthogona series (ISBN 979-8-9954416-6-3).`

`979-8-9954416-6-3` is **Book 3's eBook ISBN** (Vol III, The Mini-Beast). This is a
**Vol VI** working paper. Per the corrected registry, Vol VI has no ISBN allocation
of its own, and a volume without a registered ISBN gets no ISBN line at all.

**Replace with:** delete the ISBN clause. Keep `Part of the Principia Orthogona series`
and point at the community.

### Suggested replacement for the Description tail

```
Part of the Principia Orthogona series.
Series: Zenodo community — Principia Orthogona
https://zenodo.org/communities/principia-orthogona
(There is no series-level DOI, and Vol VI has no ISBN allocation.)
AXLE formal verification: github.com/TOTOGT/AXLE.
```

### Unchanged — verified correct, do not edit

- Title, author, ORCID `0009-0000-6496-2186`, G6 LLC, CC BY 4.0, resource type Preprint
- The entire abstract through *"...identifies precisely what the deeper levels require."*
  That sentence is the paper's own honest scoping and should be preserved verbatim —
  it is what distinguishes the deposit from the overclaim that grew around it in `ch15`.
- File `alternating_vanishing_paper_v2.pdf`, md5 `191b5e6796834ed2948613065ed0290f`

### Note for the record's own good

The deposit closes **level 1** of a three-level integrability tower. Level 2
($N_J$ on the rank-2 contact distribution $\xi = \ker\alpha$) is **not** reachable by
the same dimension count — there $m = n = 2$ and the inequality $m > n$ fails. If a
future version of this paper is deposited, saying so explicitly in the abstract would
prevent the parity overclaim that `ch15` accumulated and that was corrected 2026-08-12.
