# Drafting memo — the three open questions

**Companion to:** *No Gauge on the Tank* (concept paper, draft 0.1)
**For:** legislative counsel · **From:** Pablo Nogueira Grossi, G6 LLC
**Draft 0.1 · not legal advice**

Answering, with reasons, the three questions a drafter must settle:
define the unit · set audit rules · penalize overage traps.

---

## Scope answers (asked and answered)

**Sector.** Subscription services that impose a usage limit the buyer cannot
observe. Written for AI/LLM subscriptions because that is where the gauge is
missing today, but drafted technology-neutrally so it does not need reopening
when the product changes. Cloud, API, and "unlimited*" plans fall in naturally.

**The first unfair cost to fix.** *Forced duplicate provisioning.* A buyer who
cannot see remaining capacity buys a second and third subscription to survive a
cutoff mid-task. That is the transfer: the buyer pays 2–3× for one workload, and
the seller's revenue rises precisely because the gauge is absent. Everything
below is aimed at that one harm.

---

## Q1 · Define the unit — **do not legislate the unit**

The instinct is to pick one: tokens, minutes, requests, gigabytes. Resist it.

**Why not.** (a) It freezes technology — a token-denominated statute is obsolete
when billing moves to something else, and the sector re-prices constantly.
(b) It favors incumbents, who can shape the standard-setting. (c) It is not what
weights-and-measures law does: the law does not require gasoline be sold in
gallons rather than liters. It requires that **whatever unit is declared, the
device measures it accurately and displays it to the buyer.**

**The rule instead — declare, stabilize, reconcile:**

1. **Declare.** The seller names its unit and publishes what consumes it.
2. **Composite units must decompose.** If usage depends on several factors
   (input vs output, model tier, feature), publish the conversion. "Messages"
   that silently cost different amounts is the abuse this closes.
3. **Stability.** The declared unit is fixed for the billing period. Changing
   the unit, the limit, or the accounting mid-period is a price change and
   triggers notice.
4. **Reconcilable.** A subscriber can obtain a record sufficient to add up to
   the charge. This is the actual anti-fraud provision: an unreconcilable meter
   is not a meter.

**Drafting note.** Add a *no-evasion* clause: renaming or re-partitioning the
unit does not restart or defeat the disclosure obligation. Without it, a seller
switches from "messages" to "credits" and claims a fresh start.

---

## Q2 · Set audit rules — **inspection, not pre-approval**

Do **not** create a new certifying body or a licensure gate. It is slow, it is
capturable, and it hands incumbents a moat. Weights and measures does not
pre-approve a gas station; it **inspects the pump** and can condemn it.

**Three tiers, in ascending cost:**

| Tier | Who | Trigger |
|---|---|---|
| 1 · Attestation | An officer of the seller certifies annually that the displayed meter reflects the enforced meter | Always |
| 2 · Verification | Independent examination of meter accuracy, at the seller's expense | On credible complaint, or above a subscriber/revenue threshold |
| 3 · Condemnation | The limit becomes unenforceable until the meter is corrected (see Q3) | Verified material discrepancy |

**The specific thing to audit** is narrow and testable: *does the number shown to
the subscriber match the number used to enforce the limit?* Not model internals,
not infrastructure. One question, mechanically checkable, no trade secrets.

**Where to house it.** New Jersey already runs weights-and-measures inspection.
Two workable homes: extend that office's authority to digital metering, or place
enforcement with the Division of Consumer Affairs under existing
unlawful-practice authority. Counsel should pick; the concept paper assumes the
latter for speed.

**Attestation is the cheap deterrent.** A named officer signing that the gauge is
honest changes internal behaviour long before any inspector arrives — the
Sarbanes–Oxley lesson. It costs a compliant seller almost nothing.

---

## Q3 · Penalize overage traps — **the meter-enforceability rule**

This is the strongest provision in the bill and the one that directly reaches
forced duplicate provisioning. Do not lead with fines. Lead with this:

> **An undisclosed limit is unenforceable.**
> A provider may not enforce a usage limit — by throttling, suspending,
> degrading, or charging for excess — unless the meter and the advance notice
> required by this act were provided.

Why this is better than a penalty schedule:

- **Self-executing.** No agency action needed; it is a defense the buyer already
  holds, and a risk the seller's own counsel will price.
- **Proportionate.** A seller that shows the gauge is untouched. Only the seller
  hiding the meter loses the ability to enforce against it.
- **Aligned to the harm.** It removes the *benefit* of hiding the gauge rather
  than taxing it. A fine is a cost of doing business; unenforceability is not.

**Companion clauses:**

- **No multi-account substitution.** A provider may not require, or design its
  service so as to effectively require, a single subscriber to hold multiple
  subscriptions to obtain capacity that could be sold and disclosed as one.
  *(This is the duplicate-provisioning harm named directly.)*
- **No mid-task termination without signal.** Where the service supports
  sessions or long-running work, the advance signal must precede the cutoff by
  enough to conclude or export work in progress.
- **No forfeiture without disclosure.** Unused prepaid capacity may not silently
  expire absent clear prior disclosure of the expiry.
- **Private right / small claims.** Statutory minimum damages set at a multiple
  of the period fee keeps small claims viable without inviting mass litigation.
  Counsel should set the multiple; treble under an existing consumer-fraud act
  may already suffice.

---

## The drafting trap to avoid: B2B exclusion

Most affected users here are **sole proprietors, small firms, and professionals**
— exactly the population many consumer-protection statutes exclude as
"commercial." If the bill rides on a consumer-protection act without adjustment,
it may not cover the people it is written for.

Two fixes, either acceptable:
1. Define the protected class to include small business below a threshold
   (employees or revenue), as several state statutes already do; or
2. Ground the duty in metering itself — a disclosure duty owed by anyone who
   sells by measured quantity, irrespective of the buyer's status. This is the
   weights-and-measures posture and is cleaner.

**Also anticipate:** arbitration clauses and class waivers in provider terms.
A non-waiver clause ("the rights under this act may not be waived by contract")
is standard and should be included, or the whole act is drafted around by the
terms of service it aims to regulate.

---

## What is still genuinely open

- The subscriber/revenue threshold for Tier 2 verification. `[OPEN]`
- The advance-notice threshold — one signal or two, at what percentage.
  Telecom practice suggests two. `[OPEN]`
- Preemption exposure: whether a state metering-disclosure duty is vulnerable to
  a dormant Commerce Clause or federal-preemption challenge. Requires counsel.
  The procurement phase avoids this question entirely. `[OPEN]`
- Statutory damages multiple. `[OPEN]`

## Recommended filing order

1. **Procurement standard** — adoptable now by any agency, no statute, no
   preemption question, creates the first compliance examples.
2. **State bill** — grounded in metering, non-waivable, with the
   meter-enforceability rule as § 1 rather than buried.
3. **Interstate** — follow the weights-and-measures convergence path rather than
   seeking federal preemption of state rules.

---

*CC BY 4.0 · © 2026 Pablo Nogueira Grossi — G6 LLC · Newark, NJ ·
g6llc@proton.me · Companion to doi:10.5281/zenodo.21561819*
