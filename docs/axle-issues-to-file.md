# Obligations with no issue — drafts to file

Nine obligations are cited in the corpus against numbers that are pull requests,
a discussion, or an unrelated issue. Those numbers cannot be reused: GitHub
numbers issues and PRs in one sequence. Each obligation below is real and needs
its own issue; the corpus now states them without a number until one exists.

File them from a machine with `gh` authenticated:

```
cd ~/Desktop/AXLE
gh issue create --title "<title>" --body "<body>"
```

Then record the number in `docs/axle-issue-map.md` and write it back into the
page named under **cited in**.

---

**1. Regeneration loop invariant after g₆ cycles (full transfinite)**
Source: `regeneration_loop_invariant.lean` · cited in `GameTheory_Full_Pack.html`
The invariant is proved for finite cycle counts. The transfinite case is open.

**2. Floquet multiplier analysis for spiral return**
Source: `Main_v6.lean` · cited in `GameTheory_Full_Pack.html`
Multipliers of the return map on the spiral section; stability of the closed orbit.

**3. IPR_trib > IPR_fib formal bound**
Source: `SwarmSimulator.lean` · cited in `GameTheory_Full_Pack.html`
Inverse participation ratio, Tribonacci against Fibonacci. Numerics support it;
no formal bound exists.

**4. Spectral measure theory for fold maps**
Source: `FoldEvents.lean` · cited in `GameTheory_Full_Pack.html`
Spectral measure of the transfer operator at a Whitney fold.

**5. LCH construction for Legendrian action positivity**
Source: `MarketThreshold.lean` · cited in `GameTheory_Full_Pack.html`
Legendrian contact homology; the positivity of the action functional.

**6. Kernel dimension from contact topology**
Cited in `book8/ch6-quantum.html`, which carries a proof outline and marks it
CONJECTURE.

**7. The asymmetric inner boundary**
Cited in `ch-recurrence-ladder.html`. ε₀ = |μmax|/(2(1+sup‖Hess V‖)) is the
symmetric Grönwall bound; the numerical inner boundary r★ ≈ 0.776 is asymmetric
and is numerical input rather than a theorem. This is obligation **O7** in
`PrincipiaOrthogona1/PrincipiaVol1.lean`, which states the three-way
disagreement and says deciding it is a question about the Hessian bound, not
about Lean.

**8. Global Positivity Theorem as a Lean proposition**
Cited in `book4/ch14.html`. Not a `sorry` and not an axiom — a precise
`theorem GPT : ...` with hypotheses stated correctly, so the distance between
what is proved and what is needed becomes measurable.

**9. Non-integrability from Baker's theorem**
Cited in `book4/ch14.html`, Ch 11 rung. α_arith ∧ dα_arith ≠ 0 on a dense set of
t, via Q-linear independence of {log p}.
