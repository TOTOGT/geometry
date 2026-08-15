# WP-64 · The Recorder

### Displacement occurs at specification, not at automation — a first-person case from investment banking, 2006–2009

**Pablo Nogueira Grossi** — G6 LLC, Newark, NJ · ORCID 0009-0000-6496-2186 · g6llc@proton.me
**Working paper · version 1** · 2026 · CC BY 4.0
Labour-side companion to *The Response Gap* ([10.5281/zenodo.21752834](https://doi.org/10.5281/zenodo.21752834))

*Epistemic-status note — the discipline this corpus proposes and practises. Claims are marked `[documented]` (first-hand or public record), `[modeled]` (within a stated model), `[prospective]` (testable forward claim), or `[open]` (unresolved, flagged rather than asserted). The author was the operator in the case described and states below exactly which parts of it he can support.*

---

## Abstract

The dominant account of technological displacement locates the causal moment at **automation**: a system becomes capable enough to perform a task, and the humans performing it are released. This paper argues from a first-person case that the account is late by one step. **The displacing act is specification** — the moment heterogeneous professional output is rendered into a stable, repeatable sequence. Once that has happened, the function is already eliminated in principle; building the machine is a downstream engineering exercise of comparatively trivial cost `[modeled]`.

The case is unusual in one respect that the literature cannot manufacture: the author performed the specification, was rewarded for it with the mandate to generalise it, and was subsequently released along with the function `[documented]`. Studies of displacement typically draw on one of two populations — those who designed the automation, whose incentives run toward describing it as value creation, or those displaced by it, who were not present when the design decision was made. This account is from a single person occupying both positions, with an incentive structure that runs against overstatement.

The paper isolates three claims. First, that **the specification was a transcription rather than a design** — the automation was produced with a macro recorder, meaning the work was already algorithmic and merely unwritten. Second, that displacement **propagated through merit**: the individual who optimised locally was promoted into the role that generalised the optimisation, so the eliminating decision was made by the highest performer rather than imposed by management. Third, that this yields a **leading indicator** better than task-routineness measures: the function at risk is the one where a high performer has recently been given a mandate to standardise output across teams `[prospective]`.

A note on scale: the tools in this case were primitive. What follows is therefore a **lower bound** on the phenomenon, observed with a keystroke recorder in 2007. Systems that can infer a procedure from examples rather than requiring it to be recorded extend the exposed class from *work that is repeatable* to *work that is inferable*, which is very much larger.

---

## 1 · The case

Between 2006 and 2009 the author was an analyst in Relationship Management and Securities Finance at a global investment bank, latterly subject-matter expert for an internal client-intelligence platform.

The assigned work was the production of performance-attribution reporting for large corporate clients: analyses of an entire market that identified where a client's performance had come from, and why. The instrument was a spreadsheet. **The reporting cycle took approximately one month of full-time labour per iteration** `[documented]`.

**What the work actually consisted of, however, was reading contracts.** Attribution requires knowing the terms under which value was shared, and those terms were frequently **piecewise**: above one threshold, a stated percentage payout; above a further threshold, a different payout entirely `[documented]`. Such a schedule is a step function. It has **discontinuities**, and near a boundary an arbitrarily small change in measured performance produces a large change in what is owed.

The finding, repeated contract after contract, was that **the signatories did not understand the mathematics of what they had agreed to** `[documented]`. The document reads as a schedule of proportionate sharing. It behaves as a cliff. Nothing is concealed — the thresholds are written down — but their consequences are not legible to a reader without the relevant training, and the party that drafted the schedule chose where the boundaries sat.

The author consequently rewrote contracts on the basis of those findings, and advised counterparties on how such contracts should be written `[documented]`.

⚠️ **This is the origin of the corpus and it should be stated plainly.** The line of work published in 2026 as *The Response Gap* — a threshold parameter, set by one party, governing an irreversible consequence, undisclosed in its behaviour to the party it acts upon, and correctable by requiring the formula be published — is not a new research interest. It is the same object this author was paid to find, one contract at a time, between 2006 and 2009. §8.1 of that paper argues for published liquidation formulas. That argument was first made across a desk to corporate treasurers who had signed a step function believing it was a slope.

The author automated it using the spreadsheet application's macro recorder — a facility that captures a user's actions and emits them as executable code. **Building the automation took approximately one month.** Thereafter the same reports were produced by pressing a button `[documented]`.

**And then it was done again.** This is the part that matters most and the part most easily lost in the retelling. The first automation was not the event. It was the first instance of a campaign that ran for **years** — repeated month over month, relationship manager by relationship manager, client by client, report by report, each one a separate act of transcription `[documented]`.

Four features of that history carry the paper.

**The payback period was one iteration.** One month of labour to eliminate one month of recurring labour. Every subsequent cycle was pure return. That is not a marginal efficiency; it is a step change with break-even inside a single period — which is precisely why no approval process governs it. **The decision is small enough for one person to take alone**, and it was taken alone, hundreds of times.

**The automation was recorded, not written.** The load-bearing detail. The author did not analyse the task, decompose it, and design a program to replicate it. **He pressed record and did his job.** The resulting code was a transcript.

**The increments were individually invisible.** No single act in that campaign was large enough to warrant review. Each was one analyst improving one report for one client — the most unremarkable thing that happens in an office. There was never a proposal, never a business case, never a meeting at which the elimination of a function was on the agenda, because at no point did anyone hold a unit of work large enough to be *called* that. **The aggregate was the specification of an entire professional function. The aggregate was never on anyone's desk** `[modeled]`.

**And the outcome was promotion.** Not for one macro — for having, after years, become the only person who understood the logic across the whole book. The SME role was not a reward for building a tool. **It was the institution recognising that the author had become the specification**, and asking him to write it down for everyone `[documented]`.

## 2 · What the recorder proves

A macro recorder cannot capture judgement. It captures a sequence of operations. If a recording reproduces the output, then **the output was a function of a stable sequence**, and any judgement in the work had already been exercised — upstream, once, in selecting that sequence — and was thereafter being *replayed* rather than exercised.

This gives the paper its central claim in its strongest form:

> **The work was already a program. It had simply never been written down, and a person was serving as its interpreter.**

The month of analyst labour per cycle was not the cost of thinking. It was the **runtime cost of executing a program on human hardware** `[modeled]`.

On this reading, the function did not become automatable in the month the macro was recorded. It had been automatable for as long as the sequence had been stable. What the recorder did was not eliminate the work — it **revealed that the work had already been eliminated in principle** and was being performed anyway, because nobody had transcribed it.

The corollary is a diagnostic, and it is uncomfortable:

> **If your work can be captured by a recorder, it has already been specified. The automation is a formality and its timing is arbitrary.**

## 3 · Displacement propagates through merit

The standard policy frame treats automation as a decision taken by management and imposed on labour. Protective instruments — consultation requirements, notice periods, redundancy process — are built on that assumption.

**This case does not fit it, and the misfit is structural rather than incidental** `[modeled]`.

No manager decided to eliminate the function. The sequence ran:

1. An individual optimises his own output. Local, unilateral, unremarkable.
2. That individual becomes measurably the fastest performer in the group.
3. The organisation does the single most reasonable thing available to it: it identifies the fastest performer and asks him to make everyone else work that way.
4. That mandate is a **promotion**, and it is the standardisation step.
5. Standardisation renders the function machine-producible across the group.
6. The function contracts. The author is released with it `[documented]`.

Every step is individually correct and locally rewarded. No party acts in bad faith. **The eliminating decision was taken by the highest-performing worker and scaled by the organisation's ordinary reward mechanism** — which means it cannot be regulated by constraining management, because management did not do it.

It also means the person best positioned to foresee the outcome is structurally the least likely to. From inside, the trajectory is not visible as a trajectory. It is a series of promotions.

⚠️ **What this paper does not claim.** The author cannot establish the aggregate effect on headcount, and does not attempt to. The relevant period includes the global financial crisis, which cut analyst populations across every institution for reasons wholly unrelated to any platform. Any attempt to attribute a share of reductions to this mechanism would be unidentified, and the corpus's own standard forbids it `[open]`. What is claimed is the **mechanism**, from inside it, by the person who operated it.

## 4 · The prediction

The operational value of the argument is that it relocates the leading indicator.

Task-routineness measures — the standard instrument for estimating automation exposure — score a function on how repetitive its constituent tasks appear. This case suggests they measure the wrong object, and measure it too late. Routineness is a property of the work; **specification is an event**, and it is observable.

> **`[prospective]`** — Within a firm, the function most exposed to near-term automation is not the one scoring highest on task routineness, but the one in which a single high performer has **recently been granted a mandate to standardise output across teams**. Standardisation mandates should predict subsequent headcount reduction in that function better than routineness scores do, and with a shorter lead.

This is testable on ordinary organisational data — internal role changes, process-harmonisation initiatives, template-consolidation projects — against subsequent headcount by function. It requires no access to model capabilities and no assumption about them. It predicts from the *organisation's* behaviour rather than the *technology's*.

A second, sharper form:

> **`[prospective]`** — The interval between a standardisation mandate and the contraction of the standardised function is shorter than the interval between a capability threshold being crossed and the same contraction. If so, firms are not waiting for technology; they are waiting for specification.

### 4.1 · Why no threshold was ever crossed in view

The campaign described in §1 has a property that ought to trouble anyone designing oversight for this class of change: **it has no reviewable unit.**

Governance operates on decisions of a certain size. A proposal to eliminate a function is reviewable. A budget line is reviewable. A system procurement is reviewable. **A single analyst deciding to record a macro for one client's monthly report is none of those things**, and no reasonable process would make it one — the review would cost more than the act.

Run that act several hundred times over several years and the function is specified out of existence, without a single reviewable decision having occurred anywhere in the sequence `[modeled]`.

This is the response-gap structure transposed. In credit, the borrower has no window in which to act because irreversibility arrives faster than response. Here, the *institution* has no window in which to deliberate, because **no individual increment is large enough to trigger deliberation**, and the aggregate never appears as an object at all. In both cases the harm is not concealed. It is **sub-threshold**, and the threshold was never set.

> **`[prospective]`** — Functions eliminated through accumulated local optimisation should show **no identifiable decision point** in organisational records, while functions eliminated by procurement or restructuring should. If so, the absence of a decision record is itself a signature of this mechanism, and is empirically detectable.

## 5 · Why the case is a lower bound

The tools here were a spreadsheet and a keystroke recorder, in 2007.

A recorder requires the sequence to be **stable and demonstrable**: the operator must be able to perform it once, identically, on command. That is a strong constraint, and it excludes a great deal of professional work that varies case to case even when its underlying logic does not.

Systems that infer a procedure from examples do not carry that constraint. They do not need the sequence to be stable, only **recoverable from instances**. That extends the exposed class from *work that can be recorded* to *work that can be inferred* — and the second set contains the first.

So this case should be read as the phenomenon in its most primitive available form. The mechanism is the same. **The filter has been removed.**

## 5A · The threshold is invisible from inside the range where it does not bind

There is a further fact about the contracts of §1, and it is the most consequential observation in this paper.

**The piecewise structure only became evident during the crisis** `[documented]`.

The reason is structural rather than accidental. In ordinary conditions the measured performance on which these schedules operate clusters within a single band. One payout regime applies, continuously, for years. **No boundary is approached, so no boundary is experienced** — and a step function that is never evaluated near a step is indistinguishable, from the inside, from a straight line.

The thresholds were not hidden. They were written into the documents. They were simply **never load-bearing** until the distribution moved, and when it moved it moved into the tail, where the second regime fired and the parties discovered what they had agreed to.

This generalises, and the generalisation is the closing claim of the paper:

> **A bounded parameter is unobservable from within the range in which it does not bind.**

Every threshold in this corpus has this property. A site's carrying capacity is not visible while visitation stays below it. An aviation-fuel constraint is not visible while demand is small. A population's persistence threshold is not visible while feed is abundant. **Δt in a credit contract is not visible while collateral stays comfortable.** In every case the parameter is fully specified, fully in force, and completely undetectable by observation — until the moment it binds, at which point it has already acted `[modeled]`.

**The governance consequence is severe.** It means *experience cannot discover thresholds*, because experience is drawn from the regime in which they do not bind. Every year of incident-free operation is evidence about the interior of the range and no evidence whatever about the boundary. An institution with twenty years of clean history and an undisclosed step function has twenty years of data that is silent on the only question that matters.

There are exactly two remedies, and both appear in the companion paper's §8:

1. **Publish the formula** (§8.1), so the boundary can be located without reaching it.
2. **Derive the boundary rather than observe it** — which is the case for formal verification, and the reason this author's method is what it is. A proof establishes where a discontinuity lies without requiring the system to be driven into it.

That is why *verify, don't trust* is not a temperament. **Trust is calibrated on the interior. The damage is at the edge.**

### 5A.1 · At the fold, the contract stopped being a contract

The observation above understates the failure, and the understatement should be corrected because the true version is the point of the paper.

When the crisis drove outcomes past the boundary, the difficulty was not that the parties had misunderstood which payout regime would apply. **It was that the contract did not specify one** `[documented]`. Beyond the fold there was no rule — not an unfavourable rule, not a surprising rule. **No rule.**

Formally: the agreement was a **partial function**. It was defined over the domain its drafters had imagined and undefined outside it, and the distribution moved outside it. At the fold the map is not locally invertible — the observed state is consistent with several allocations and determines none of them. Given what had happened, **who was owed what percentage of what was not derivable from the document** `[documented]`.

The consequence follows immediately and is the reason this matters beyond one desk in one bank:

> **When specification fails at the boundary, the allocation is decided by whoever is standing in the gap, and the contract supplies the appearance of legitimacy while doing none of the work.**

The default occupant of that gap is the stronger party. More counsel, more capital, more capacity to wait — the ambiguity resolves in its favour without anything being breached, because there was nothing left to breach `[modeled]`. That is the sharpest form of the mechanism the companion paper describes in credit: there the borrower has a window too short to act in; here the parties have **no rule to act under**, at precisely the moment the amounts are largest.

### 5A.2 · What actually happened in the gap

The author is obliged to report that in this case it did not go that way, and the exception is more instructive than the rule.

**The gap was filled by an analyst.**

Asked what the split should be where the document did not say, the author recommended that it fall **in favour of the client, against the bank's immediate interest**, on the following ground: the client had placed assets in the institution's custody to be managed, and the institution therefore stood in a **fiduciary** relation to them. Where the agreement was silent, the silence should be resolved in favour of the party whose assets they were `[documented]`.

**The executives agreed** — and complained that they now had to be lawyers `[documented]`.

Three things follow, and they matter more than the anecdote.

**First, the correction to the rule above.** Power does not decide at a fold because power is entitled to; it decides because it is usually the only thing present. A void is filled by whoever occupies it and by whatever principle they bring into it. When a person with no bargaining power at all supplies a principle — and it is a *recognised* principle, load-bearing in law — it can hold, even against the interest of the party that could have overruled it `[documented]`. **The mechanism is not "the strong take." It is "the unspecified is taken by the present."** Those differ, and the difference is the entire space in which governance can act.

**Second, the complaint is the governance failure stated by its victims.** *"We have to be lawyers now"* is exactly right and should not be read as grumbling. When a contract goes undefined at the boundary, the drafting burden does not disappear — it is transferred, in real time, under crisis conditions, onto people who are not drafters and did not agree to draft. The specification work was not avoided by leaving the fold unwritten. **It was deferred to the worst possible moment and assigned to the worst-placed people** `[modeled]`.

**Third, why the fold was there at all.** The contracts had been written from the perspective of a single agent's exposure — the risk *to the bank* — on the implicit view that this was where risk presented. They did not model the client's risk, nor other stakeholders'. The document was therefore complete over the region where the bank's exposure was the binding constraint, and undefined where it was not `[modeled]`. This yields a general and testable claim:

> **`[prospective]`** — Agreements drafted from a single party's risk model will be undefined precisely in the states where another party's risk binds. Contract incompleteness should therefore concentrate not in rare states generally, but in **states adverse to the counterparty and neutral to the drafter** — a distribution distinguishable from mere failure of imagination.

If that holds, incompleteness is not simply an artefact of bounded foresight. **It is shaped by whose exposure the drafter was modelling**, which makes it an object of governance rather than an accident.

### 5A.3 · The resolution was ungoverned too

One further property of the episode deserves recording, because it is the sub-threshold failure of §4.1 recurring one level up.

**The decisions taken at the fold did not go to a vote** `[documented]`. There was no committee, no formal determination, no minuted process by which the institution decided how silence in a client agreement should be resolved. A recommendation was made and executives agreed with it.

So the failure compounds. The contract was undefined at the boundary — and **the procedure for resolving an undefined contract was also undefined.** The gap was filled, correctly as it happens, but by an informal act that produced no record of who decided, on what authority, or on what principle.

The consequences are structural rather than personal:

- **No reviewability.** A decision that was never formally taken cannot be audited, appealed, or examined afterwards for consistency with how comparable cases were handled.
- **No precedent.** The fiduciary reasoning that resolved this instance was not written into anything. The next fold, in another book, under other people, starts from nothing — and may be occupied by someone bringing a different principle, or none.
- **No visibility of variance.** If some folds were resolved on fiduciary grounds and others on commercial ones, the institution has no way to know, because neither kind generated a record.

> **The specification failure is therefore two-layered: the agreement is silent at the boundary, and the institution is silent about how it breaks that silence.** The second gap is the more tractable of the two — a firm cannot foresee every state, but it can certainly specify *how it will decide when it has not foreseen one* `[modeled]`.

That is a governance instrument that does not currently exist in the companion paper's §8, and it should. Call it a **fifth corrective: a disclosed resolution rule for undefined states** — naming, in advance, who decides, under what standard, and with what record, when an agreement turns out not to cover the situation. It costs nothing to draft in calm conditions, and it is unwritable in a crisis.

Note what this does to the epistemics of the whole arrangement. During the years when the contract appeared to be governing, it was governing. The parties' confidence was **correctly calibrated to their evidence.** The document was doing exactly what they believed it was doing. Its failure was not latent misbehaviour waiting to be discovered — the failure did not exist yet. **It was created by the arrival of a state the document did not cover**, and it arrived at the worst possible moment, because the states a drafter fails to imagine are systematically the extreme ones.

⚠️ *A terminological note. The word used here — the **fold** — is not borrowed for effect. It is the object: a surface turning back on itself such that the solution is locally non-unique or undefined, which is what a payout schedule does at an unspecified boundary. This author has treated folds formally elsewhere in this corpus (Book 6; Whitney A₁ classification; the catastrophe-manifold line). The mathematics came later. **The object was met first, across a table, in 2008.***

## 6 · The attribution, one layer down

*The Response Gap* argues that a loss caused by a structural condition is routinely attributed to the person the condition acted upon, and that the attribution survives because the condition is not measured.

The same operation is visible here, in the language.

**"He automated himself out of a job"** is the sentence available for this case. It locates the cause in an individual and reads as a wry observation about personal miscalculation. It is also the industry's account of the whole phenomenon in miniature: cause assigned to the person, mechanism unnamed.

The mechanism was a specification event, taken locally, rewarded institutionally, and scaled by an ordinary promotion. Nobody at any point crossed a line, and nobody was watching the threshold — because the threshold had not been written down either.

That is the same failure the companion paper identifies in credit: **the harm's unmeasurability is not incidental to it. It is the condition on which it persists.**

---

## 6A · On magnitude, and why this paper declines to state one

A paper describing a mechanism of this kind invites the question of what it is worth, and the temptation to answer it with a large number should be resisted. This section records why.

**The direct transfer is not the cost, and it largely nets out.** Value reallocated at a fold is not destroyed; it accrues to the counterparty and compounds in their hands rather than the other's. Summing realised transfers across a class of contracts therefore measures redistribution, not loss, and overstates the social cost by roughly the whole of it.

**Crisis-cost aggregates cannot be routed through this mechanism.** Published estimates of what a financial crisis cost exist and are large. Attributing any share of them to contract incompleteness at the boundary requires an identification strategy this paper does not have and does not pretend to. **The companion paper spends its §6 refusing exactly this move for the response gap** — realised loss cannot be assigned to a mechanism merely because the mechanism was present — and the refusal binds here with equal force `[open]`.

**And §5A forbids the estimate on its own terms.** A quantity that manifests only beyond a threshold cannot be estimated from a regime that has not crossed one. This author has a single tail observation. To extrapolate a magnitude from it would be to occupy precisely the epistemic position of the executives in §5A.1 — confident about a boundary from evidence drawn entirely from the interior. The paper cannot make that error in its own voice while identifying it as the central failure in others'.

**What can be said about magnitude is this**, and it is a statement about *direction and channel* rather than size:

> `[modeled]` The realised transfer understates the cost, because the transfer is redistributive and largely nets out. What does not net out is the **premium subsequently priced into every agreement in the class**, once incompleteness at the boundary is understood to be systematic — wider spreads, shorter tenors, heavier collateral, more counsel, and transactions that do not occur. That cost falls on contracts that never fold, accrues for as long as the incompleteness is unrepaired, and appears in no accounting of the events that revealed it.

This inverts the usual policy arithmetic in a way worth stating plainly. The correctives — publishing formulas, bounding response times, disclosing epistemic status, and the resolution rule of §5A.3 — are conventionally weighed against the losses of the events they would have prevented. **On the argument above they should be weighed against the standing premium on everything drafted afterwards**, which is larger, permanent, and borne by parties who were never near a fold. Drafting a resolution rule in calm conditions costs a lawyer's afternoon. Not having one is priced into the entire book, indefinitely `[modeled]`.

## 6B · Why procurement is governed and interpretation is not

An institution that will not let a manager engage a supplier without three competing quotations will let a small number of senior people resolve, informally and without record, a question whose consequences exceed that engagement by orders of magnitude. §5A.3 records one such instance. The asymmetry is not hypocrisy and it is worth stating precisely, because the explanation determines the remedy.

**Oversight attaches to legibility, not to consequence.** A procurement is legible: it has a price, a vendor, a date, a comparison class, and it fits on a form. A resolution at a fold has none of these. It has no unit, no tender, no natural register, and no obvious moment at which it becomes a *decision* rather than a conversation. Controls therefore bind on the *shape* of an act rather than its stakes — and the acts least resembling a purchase order attract the least scrutiny irrespective of what turns on them.

The consequence is systematic and inverts what governance is for:

> **Scrutiny is highest where a decision is routine enough to have a template, and lowest where it is novel enough to lack one.** Novelty is also the condition under which error is most likely and precedent least available `[modeled]`.

This is §4.1 and §5A.3 restated as a general property. There, no increment was large enough to review and no resolution was formal enough to record. Here: **nothing in the control apparatus is triggered by an act that does not resemble the acts the apparatus was built around.**

### 6B.1 · What a committee would have to demand

The obvious remedy — refer such decisions to a committee — is insufficient on its own, and the insufficiency is instructive. **Adding signatories to an unspecified decision does not specify it.** It distributes responsibility for an arbitrary determination across more people, which improves the record and the politics while leaving the epistemics untouched. Most governance reform fails at exactly this point: it adds process without adding anything checkable.

What would make such a committee more than ceremonial is a **decidable question it is obliged to ask.** The verification discipline supplies one, and it is narrower than it first appears.

⚠️ **A contract's *fairness* is not formally checkable.** Neither is the choice of principle at a fold — the fiduciary reasoning of §5A.2 is a normative judgement and no proof system will adjudicate it. Claiming otherwise would be the overreach this corpus exists to avoid.

**A contract's *totality* is checkable.** Whether a payout function is defined over the whole domain the parties are exposed to is a decidable property, not a matter of opinion. It requires only that the schedule be stated as a function and the exposure be stated as a domain — after which coverage either holds or a gap can be exhibited. This is the ordinary totality obligation a proof assistant imposes on any definition by cases, and it is the exact failure of §5A.1: a partial function presented as a complete agreement.

> **The sixth corrective: a totality obligation.** Before execution, the party drafting a threshold-bearing agreement should be required to state the payout as a function, state the exposure as a domain, and demonstrate that the function is defined across it — or name explicitly the states it does not cover and the rule that governs them (§5A.3). The committee's question is not *is this fair*, which it cannot answer, but *is this total*, which it can.

The virtues are practical rather than theoretical. The obligation is **cheap in calm conditions** and impossible in a crisis. It **produces an artefact** — a stated domain — which is reviewable in a way a conversation is not. It is **falsifiable by counterexample**: a single unhandled state defeats it, and exhibiting one requires no authority, only attention. And it makes the failure of 2008 a *finding* rather than a surprise, since a totality check performed at drafting would have returned the gap that the crisis later returned at far greater cost `[modeled]`.

This is the sense in which *verify, don't trust* generalises beyond mathematics. **It does not mean subjecting judgement to proof. It means never letting an unstated domain pass as a complete specification.**

### 6B.2 · The question had no owner

The natural objection is that these agreements were drafted by specialists, and that coverage was therefore somebody's job. The record suggests otherwise, and the reason is structural rather than a failure of diligence.

**The specialists present were lawyers, and legal training addresses text.** Whether language is ambiguous, whether terms are defined, whether obligations are enforceable, whether a clause survives challenge — these are demanding questions and they were competently handled. **None of them is the question whether a piecewise function is total over the reachable state space.** That is a property of the object the document describes, not of the document, and no amount of drafting skill surfaces it.

So the question fell between two professions and was owned by neither. The legal side could reasonably assume the commercial side had characterised the exposure; the commercial side could reasonably assume the legal side had confirmed the instrument was complete. **Both assumptions were held in good faith and neither was anyone's stated responsibility** `[modeled]`.

This explains the complaint recorded in §5A.2 — *"we have to be lawyers now"* — and shows it to be the wrong inference drawn at the right moment. More legal attention would not have helped. What the fold revealed was not a defect in the drafting but **a question that had never been assigned.**

It also explains the observational position from which the defect was visible. The author was neither drafting nor negotiating these agreements. He was performing attribution, which requires **evaluating** the function on realised states in order to produce a number `[documented]`.

> **A coverage gap is visible from the position that must compute the outcome, and invisible from every position upstream of it.** Drafting requires only that the text be defensible; negotiation requires only that the terms be acceptable. **Evaluation is the first step at which the function must actually return a value** — and therefore the first at which its failure to do so is discovered.

The governance implication is narrow and cheap: the totality obligation of §6B.1 should be discharged by whoever will have to **evaluate** the instrument, not by whoever drafts it — and it should be discharged **before execution rather than at the first hard case**, which is the only difference between a finding and a crisis.

## 7 · Open questions

- Aggregate headcount effect, unidentifiable from this case and not claimed `[open]`.
- Whether the specification-to-contraction interval is empirically shorter than the capability-to-contraction interval `[prospective]`.
- Whether firms with formal process-harmonisation programmes show earlier functional contraction than matched firms without, controlling for technology adoption `[open]`.
- Whether the merit-propagation mechanism is visible in promotion records — specifically, whether the individual granted a standardisation mandate is disproportionately likely to be released within the following two cycles `[open]`. This is the most personally interesting question and the author cannot answer it from *n* = 1.
- Whether any protective instrument can address a decision taken by the highest-performing worker rather than by management `[open]`.

---

## Companion works

- **The Response Gap** — [10.5281/zenodo.21752834](https://doi.org/10.5281/zenodo.21752834). The credit-side argument: Δt as an undisclosed, optimisable, bounded parameter.
- **The Forced Urgency Gap** (WP-32) — non-identification of preference under latent liquidity constraint.
- **Algorithmic Urgency** — Book 6, WP-56. https://totogt.github.io/geometry/book6/wp56-algorithmic-urgency.html

---

## Copyright and licence

© 2026 Pablo Nogueira Grossi. G6 LLC, Newark, New Jersey, USA.
Licensed **CC BY 4.0** — https://creativecommons.org/licenses/by/4.0/
ORCID [0009-0000-6496-2186](https://orcid.org/0009-0000-6496-2186) · Code and formalisation: https://github.com/TOTOGT

---

## ⚠️ Author's note before deposit — decide these two

**1. Naming.** This draft says *"a global investment bank"* and *"an internal client-intelligence platform"* rather than naming either. That is deliberate and I would keep it. The argument loses nothing — the mechanism is the subject and the employer is incidental — and naming a former employer alongside a claim about headcount reduction invites a dispute you have no reason to invite. Your CV already carries the institution; the paper does not need to.

**2. The one factual check only you can make.** I have written the reporting cycle as *"approximately one month of full-time labour"* and the build as *"approximately one month."* If those are estimates rather than records, keep the word *approximately*. If you can date the build, say so — a dated build with a stated payback period is far stronger evidence and costs nothing to include.
