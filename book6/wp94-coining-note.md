# Proposing a term with the census instrument
**Method note · the gap identified in WP-94 §8, the apparatus from the IJL paper, the measurement from `tools/lexeme_census.py`**

---

## 1. What a corpus census can and cannot decide

A census cannot tell you what a word should *mean*. It can decide three things that usually get decided
by taste:

1. **Collision.** Whether the string is already carrying load in the discourse. A term that must be
   disambiguated from its own existing use is dead on arrival.
2. **Paradigm availability.** Whether the community already inflects words of this kind — WP-94 §2
   established that this one does, and that it selects between two individuation strategies (`sorry`
   pluralises and counts; `grammar` takes a modifier and almost never pluralises).
3. **Derivational reach.** Whether the proposed term supports the derivations the existing term
   actually shows. `sorry` is attested with `-free` (135 tokens) and `zero-` (50). A replacement that
   cannot do that is a narrower word than the one it joins.

What it cannot do is settle attestation *in the target community*. This corpus is one author's. That
limit is stated again in §6.

## 2. The requirement, derived rather than assumed

From WP-94 §8 and the OpenAI comparison, the object needing a name is:

> **a step in a formal development that is established by a proof outside the formal system, and is
> entered as an assumption because the verifier cannot read that proof.**

Four existing terms fail, each in a stateable way:

| Term | Why it fails |
|---|---|
| `sorry` | asserts the step is *unfinished*. It is finished, elsewhere. |
| `axiom` | asserts it will *never* be checked. It has been checked, elsewhere. |
| `admit` | asserts it is granted by *fiat*. It is granted by *citation*. |
| `hypothesis` | asserts the conclusion is *conditional*. It is not, mathematically — only formally. |

The required grammatical profile follows from what speakers need to do:

- **count it** — "three ___ remain" (numeral + noun; `sorry` does this 905 times in the corpus)
- **enumerate and discharge it** — "close off these ___" (definite plural)
- **point it at a source** — "a ___ on Deligne" (relational complement: *on* / *for* / *against*)
- **use it as a verb and a participle** — the existing keywords are all first-person speech acts
- **negate it as a quality** — `___-free`, `zero-___`, on the `sorry-free` model

That is a **token** noun with a relational slot and a verbal base — not a type noun.

## 3. Collision measurement

`python3 tools/lexeme_census.py import:imports cite:cites ...` over 3,214,612 words.

| Candidate | per M | verdict |
|---|---|---|
| `cite` | 512.7 | **dead** — bibliographic sense saturates it |
| `bridge` | 486.2 | **dead** — carries the Ponte Nova argument |
| `import` | 436.8 | **dead** — Lean/Python `import` |
| `hypothesis` | 282.5 | **dead** — and it is the word already being misused |
| `assumption` | 208.1 | **dead** — 202 plurals in place |
| `stub` | 159.0 | **dead** — 80 plurals, 33 numeral+, already a full count paradigm elsewhere |
| `certificate` | 59.4 | **taken** — both papers use it for the object that *is* verified |
| `warrant` | 47.6 | crowded — mostly the verb "to warrant" |
| `proxy` | 17.4 | light |
| `debt` | 14.3 | light — but WP-94 already uses debt as the *frame* for `sorry` |
| `voucher` | 4.0 | near-free |
| `receipt` | 2.2 | near-free |
| `attestation` | 1.9 | near-free — and **4 plurals in 6 tokens**, already countable |
| `surrogate` | 0.9 | near-free |
| `deferral` | 0.6 | near-free |
| **`lien`** | **0.0** | **free** |
| **`escrow`** | **0.0** | **free** |
| **`consignment`** | **0.0** | **free** |

## 4. Two finalists, and the trade they represent

### `lien` — the better semantic fit

A lien is *a claim registered against an asset held elsewhere, discharged when the obligation settles.*
That is exactly the relation: the formal development registers a claim against a proof it does not
hold. Zero collision. Supports every required form — *three liens remain*, *a lien on Deligne*,
*lien-free* (already idiomatic in its home domain), *zero-lien*.

Its weakness is register. `sorry`, `admit`, `oops` are short, first-person, faintly absurd — they are
**speech acts by the author to the reader**. `lien` is a term of art from conveyancing. It describes
the situation from outside rather than saying anything.

### `vouch` — the better register fit

The existing keywords are all speech acts: `sorry` apologises, `admit` concedes, `oops` abandons,
`axiom` declares. The missing act is *I attest that this is proved, elsewhere* — and the one-syllable
English verb for that is **vouch**.

- keyword: `vouch [BI17]`
- count noun: *a vouch*, *three vouches remain*
- participle: *a vouched lemma* — matching `sorried`, which WP-94 found attested in Tao's PFR project
- negation: *vouch-free*, *zero-vouch*, on the attested `sorry-free` / `zero-sorry` model
- relational: *vouch for*, which is the ordinary English government of the verb

Corpus collision 0.0 per million for `vouch` as a bare verb in this corpus; `voucher` at 4.0 is the
nearest neighbour and is a different lemma.

### Recommendation

**`vouch`.** The semantic argument favours `lien`, and the semantic argument is not the one that
decides adoption. IEC 60906-1 was the better plug and lost to installed base; a term that is right and
unspeakable loses to a term that is approximate and sayable. The register of this vocabulary is
established — short, verbal, first-person — and a proposal that ignores it is proposing to a community
that does not talk that way.

Keep `lien` in the paper as the gloss: *a vouch is a lien against a proof held elsewhere.*

## 5. The entry, built on the operator chain

Applying C → K → F → U from the IJL manuscript to a term being *coined* rather than *described* —
which is the same apparatus run in the other direction.

**C — the compressed core.** *A step whose proof exists outside the checker.* Minimal, context-neutral,
and everything below derives from it. Note what it excludes: it says nothing about whether the step is
true, only about where its proof lives.

**K — licensed constructions, and one blocked.**

| Licensed | Example |
|---|---|
| numeral + N | *two vouches remain* |
| definite plural + discharge verb | *close off these vouches* |
| relational *for* | *vouch for the Kloosterman bound* |
| participial modifier | *a vouched lemma* |
| privative compound | *vouch-free*, *zero-vouch* |

**Blocked:** \**vouch* as a bare mass noun — \**there is much vouch in this file*. The corpus shows this
community's gap-words are count nouns without exception; a mass reading would be a different concept.

**F — how many senses the entry needs.** Two branches, and they co-predicate, so one entry:
(i) the keyword written in the source; (ii) the obligation it records. *This file has three vouches, and
two of them are on the same paper* — the first clause counts occurrences, the second counts
obligations, in one grammatical utterance. One headword, two senses.

**U — contextual licensing.** A vouch is only well-formed **with a resolvable citation attached.** A
vouch with no source is not a vouch; it is a `sorry`. That condition is the whole content of the term,
and it is what the usage note must carry.

## 6. What this has not established

- **No attestation in the target community.** Everything above is measured against one author's corpus.
  Whether `vouch` collides in mathlib, Isabelle, Coq or the avionics literature is unmeasured, and it is
  the measurement that matters most.
- **The corpora that would settle it** are a mathlib Zulip dump, the Isabelle mailing list, and the
  formal-methods arXiv listings. None has been assembled.
- **No claim that a term is needed rather than a convention.** It is possible the right fix is not a new
  keyword but a required citation field on the existing ones — `sorry (cf. [BI17])`. That is a cheaper
  proposal and it should be costed before a new word is argued for.
