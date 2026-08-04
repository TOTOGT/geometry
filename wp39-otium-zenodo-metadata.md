# WP-39 deposit — Otium (new record, new DOI)

**Do not publish this inside `21752834`.** Start a *new* Zenodo upload, press
**Reserve DOI**, and put `otium-jomo-generalization.md` there alone. Remove it
from the WP-38 upload.

Why: bundled, the note has no citable identifier of its own, inherits WP-38's
title and JEL codes (C73/D43/G13/L95 — none of which describe it), and is
indexed under an energy-microstructure record although its literature is
leisure, labour precarity and platform design. It is a different audience.

---

## Form values

| Field | Value |
|---|---|
| Communities | principia-orthogona |
| Resource type | Publication → Working paper (else Preprint) |
| DOI | reserve a new one — call it `<WP39-DOI>` below |
| Title | Otium: Positional Dominance outside Markets |
| Additional title (subtitle) | A generalization of the non-contestability theorem |
| Publication date | 2026-08-01 |
| Authors | Nogueira Grossi, Pablo — G6 LLC — ORCID 0009-0000-6496-2186 |
| Version | 1.0 |
| Language | eng |
| Publisher | G6 LLC |
| License | CC BY 4.0 |

### Keywords

```
otium; negotium; JOMO; FOMO; attention economy; replaceability; preemption hazard;
positional goods; conspicuous leisure; real options; labour precarity;
platform design; engagement optimization; wu wei; Sabbath; Veblen
```

### Related works

| Relation | Identifier | Scheme |
|---|---|---|
| is supplement to | 10.5281/zenodo.21752834 | DOI |
| references | 10.5281/zenodo.21753025 | DOI |
| is part of | https://zenodo.org/communities/principia-orthogona | URL |

And on the **WP-38** record, add the mirror: `is supplemented by → <WP39-DOI>`.

### References

```
Budish, E., Cramton, P., & Shim, J. (2015). The high-frequency trading arms race. Quarterly Journal of Economics, 130(4).
Cicero. De Officiis.
Grenadier, S. R. (2002). Option exercise games. Review of Financial Studies, 15.
Laozi. Daodejing, ch. 37, 48.
Pieper, J. (1948). Leisure: The Basis of Culture.
Russell, B. (1932). In Praise of Idleness.
Seneca. De Otio.
Veblen, T. (1899). The Theory of the Leisure Class.
```

---

## Fix in the file before uploading

Line 5 and the closing reference both read:

> *Companion note. Extends Grossi (2026a), DOI 10.5281/zenodo.21752834.*

Wrong on both counts. `21752834` is WP-38, not Grossi (2026a) — that label denotes
the network-games paper (`21013066` v1 / `21753025` v2) everywhere else in the
corpus. Replace with:

> *Companion note. Generalizes Theorem 1 of WP-38, "Positional Dominance under
> Non-Contestability" (DOI 10.5281/zenodo.21752834), which builds on Grossi (2026a)
> v2 (DOI 10.5281/zenodo.21753025).*

And in the reference list, replace `Grossi (2026a), DOI 10.5281/zenodo.21752834`
with two entries:

```
Grossi, P. N. (2026a). Positional dominance in network games, v2. DOI 10.5281/zenodo.21753025.
Grossi, P. N. (2026). Positional dominance under non-contestability. WP-38. DOI 10.5281/zenodo.21752834.
```

---

## Description (paste as HTML)

```html
<p><strong>Otium is not the absence of strategy. It is the dominant strategy in a
specific regime, and the regime is defined by whether your position can be taken
while you are not looking.</strong></p>

<p>This note generalizes Theorem 1 of the companion working paper
(DOI 10.5281/zenodo.21752834) out of markets. Stripping the network game of its
commodity content leaves five objects: standing (a position one occupies),
replaceability &lambda; (the rate at which absence transfers standing to a rival),
turbulence &sigma; (dispersion in outcomes), carry (what the position costs to hold
while idle), and participation effort. The theorem's proof used none of the
commodity structure: it required only that effort face a saturating return, that
the position hold an option on turbulence, and that holding cost something. Those
conditions are met by a wide class of social and professional positions.</p>

<p><strong>Proposition A.</strong> FOMO is the correct response to &lambda; &gt; 0;
JOMO is the correct response to &lambda; = 0. Neither is a virtue; each is a
strategy, and each is wrong in the other's regime. The uncomfortable corollary is
that counsel to disengage is sound for the secure and harmful for the precarious,
while being dispensed, as a rule, by the former to the latter. The advice is not
false; it is unqualified, and the missing qualifier is &lambda;.</p>

<p><strong>Proposition B.</strong> An attention platform maximizes engagement not by
increasing the return to participation — which saturates — but by increasing
perceived replaceability. Feeds displaying what one missed, decaying follower
counts, streaks, activity indicators and absence-penalizing distribution are
&lambda;-inflation technologies. The countermeasure is not willpower but
establishing genuine non-contestability.</p>

<p>The note reads the classical vocabulary as the same partition: <em>negotium</em>
is literally <em>nec-otium</em>, business defined negatively as the absence of the
primary state; Cicero and Seneca treat <em>otium</em> as the condition under which
judgement becomes possible. Wu wei is a claim about regimes rather than a paradox,
and the Sabbath is the one mechanism in the set that manufactures &lambda; = 0 by
coordination rather than by ownership — which is why it required a law, and why it
erodes once observance becomes optional. Veblen (1899) saw the observable side
without the mechanism: conspicuous leisure signals status precisely because it
demonstrates that one's position is not contestable.</p>

<p>Three falsifiable predictions are stated: a cross-sectional one on engagement
elasticity by &lambda;, an interaction prediction on the slope of participation
against turbulence by regime, and an institutional one on the collapse of
coordinated abstention when enforcement becomes optional. The boundary condition
transfers from the market paper intact — &lambda; = 0 is never permanent, because
the institution that guarantees it can withdraw the guarantee.</p>
```
