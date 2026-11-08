# Process review, 2026-11-08: claims marked "open" before they were stated

Supplied by the author (Pablo Nogueira Grossi) in a Claude Cowork session on 2026-11-08 and
kept here verbatim as evidence. The reviewer model is not named in the paste. The review read
`GSeries.lean`, `FoldHysteresis.lean`, `FoldScaling.lean` and Volume II, and says it cannot attribute
passages to Claude without edit history.

Spot-checked on receipt (Claude, same day): item 1's counterexample composes to G(x) = 2x
(Lipschitz product 1/2 · 1 · 1/2 · 8 = 2); item 2's a-priori bound is the standard Banach estimate;
item 3's algebra re-derived by hand and with sympy (δ = x²(3+x), W″ = 3x(2+x), ratio → 2√3);
item 4's test is right (q = 1 is an equilibrium at a = 2, so q(t) ≡ 1); item 5: ∫₀^∞ e^{−βz} dz = 1/β → 0,
and βe^{−βz}1_{z≥0} → δ₀. Items 6 and 7 not checked beyond reading.
Action taken the same day: item 1 of the work order (the softening limit) written as
`Orthogenesis/Taxonomy/FoldSoftening.lean`, not yet kernel-checked.

---

**The main failure is that several claims were marked "open" before their mathematical statements were made precise. Some are genuine proof tasks; others are false as stated, already resolved, or only definitions dressed as results.**

I read the current `GSeries.lean`, `FoldHysteresis.lean`, `FoldScaling.lean`, and the relevant sections of Volume II. I cannot attribute individual passages to Claude without their edit history. But these are concrete failures in the assisted development process—and concrete ways to close them.

**1. The G-chain's operators still lack a common mathematical specification**

GSeries.lean explicitly says the substantive stage criteria remain prose: the required operators on a defined state space have not been supplied for that formalization.

The file also gives a decisive counterexample to the old general convergence claim:
C(x)=x/2, K(x)=x, F(x)=x/2, U(x)=8x.
These meet the encoded component conditions, yet G(x)=2x, which expands.

**Where the process failed:** assigning useful names to individual operators was treated as sufficient to constrain their composition.

**Closure path:** choose one concrete state space and actual maps. If the goal is convergence, prove that they preserve a complete domain and establish, for example, L_U L_F L_K L_C < 1. That gives a genuine contraction theorem. If the intended G is not contractive, specify a different mechanism and prove that mechanism.

**Completion criterion:** one instantiated G-chain with a theorem about its trajectories, beyond the ordering of its labels.

---

**2. The "33 cycles" problem is ready to close by replacement**

The same file already proves that the contracting argument works with any lower index N. It also demonstrates that the index-33 property holds for some systems and fails for others.

**Where the process failed:** arithmetic about a label became a claim about dynamics.

**Closure path:** retain 33 as a teaching label, then supply a system-dependent accuracy bound. For a contraction with 0<L<1,
d(Gⁿx, x*) ≤ Lⁿ/(1−L) · d(x, Gx).
This gives an explicit iteration count once the initial displacement and tolerance are specified.

**Completion criterion:** remove universal cycle guarantees and prove a tolerance-dependent bound for the chosen model. This is not a frontier open problem.

---

**3. The fold's "softening" limit can be closed immediately**

FoldHysteresis.lean establishes the equilibrium branches and derivatives. The canonical page still lists the limiting softening statement as absent from the formalization.

For the upper branch, write q=1+x, x>0, and δ=2−a. The equilibrium equation gives exactly δ=x²(3+x).
The restoring rate is k=W_qq=3x(2+x).
Therefore k/√δ = 3(2+x)/√(3+x) → 2√3.
For the specified gradient dynamics, the linear relaxation time consequently satisfies τ_lin ~ 1/(2√(3δ)).

**Where the process stalled:** an elementary branch calculation was left as an open formalization task.

**Closure path:** prove the branch limit and this ratio limit in Lean. FoldScaling.lean already supplies related normal-form results.

**Completion criterion:** an explicit asymptotic theorem with its constant, not just "recovery slows."

---

**4. Equilibrium geometry has been allowed to stand in for transition dynamics**

FoldHysteresis.lean explicitly states that the gradient flow is not formalized. Its "landing" result establishes a stable equilibrium at −2; that alone does not establish a trajectory arriving there.

There is an especially useful test: a=2, q(0)=1 ⟹ q(t)=1. At the exact fold, this initial condition does not spontaneously jump.

**Closure path, in manageable steps:**
1. For fixed a>2, prove global forward existence and convergence to the unique equilibrium q₋(a)<−2.
2. Prove q₋(a)→−2 as a↓2.
3. Only then introduce a specified ramp a(t) and study tracking, departure and delay.

**Completion criterion:** separate the already-established equilibrium diagram from a proved statement about motion. Finite-rate hysteresis is a further theorem.

---

**5. Volume II's contact-limit theorem needs a corrected limit before a proof**

Volume II describes the full contact-realization theorem as a placeholder with conclusion `True`. It also refers to distributional convergence of e^{−βz} to a step-like object.

**Where the process failed:** neither a placeholder theorem nor pointwise decay establishes an impulse limit.

For example, on z≥0, the unnormalized exponential has mass ∫₀^∞ e^{−βz} dz = 1/β → 0.
A possible replacement is the normalized kernel K_β(z)=βe^{−βz}1_{z≥0}, whose distributional limit is a Dirac mass.

**Closure path:** specify the intended limit, domain, normalization and test-function space. Prove that scalar limit first. Then derive the claimed momentum jump from the actual equations, including how a trajectory crosses the layer.

**Completion criterion:** a correctly stated regularization theorem. The normalized kernel is a proposed repair, not proof that the existing dm³ Hamiltonian produces the claimed jump.

---

**6. Threshold equivalence should first become a one-way quantitative theorem**

Volume II acknowledges that its formal equivalence is trivial under the encoded assumptions: negativity of the Lyapunov parameter is already supplied.

The displayed estimate 𝓛V ≤ −cV + Kσ² can, under suitable global hypotheses, yield
E V_t ≤ e^{−ct} E V_0 + (Kσ²/c)(1−e^{−ct}).
That is a useful noise-dependent bound. It does not establish a universal equivalence with a geometric fold, or an exact noise threshold.

**Closure path:** prove this bound for a specified SDE and Lyapunov function. Define the desired tolerance or exit probability. Treat the geometric converse as a separate claim requiring separate assumptions.

**Completion criterion:** a nontrivial theorem connecting measured quantities, with assumptions that do not already contain its conclusion.

---

**7. Close the ledger on results we have already settled**

The Chapter 10 contact obstruction, including λ*, and the attracting-tube contact realization should now be recorded as resolved at the mathematical level, subject to the repository's implementation checks. The original-form contact claim and "irreversible F" argument are refuted or withdrawn—not perpetually open.

Likewise, neural superiority is an empirical hypothesis. The named Hopf model can have its own fully resolved local bifurcation analysis without establishing a general neuronal theory.

**The best work order for Claude is:**

| Priority | Task | Why |
|---|---|---|
| 1 | Formalize the softening limit | Small, exact, and directly supports the g-series |
| 2 | Prove frozen-control gradient convergence | Turns equilibrium geometry into dynamics |
| 3 | Instantiate one G-chain and derive an iteration bound | Gives the operator framework mathematical content |
| 4 | Repair and prove the regularization limit | Resolves a foundational ambiguity |
| 5 | Prove a specified stochastic stability bound | Produces a useful result without an unsupported equivalence |

The instruction I would give Claude is: **"Take one row. State the exact theorem, identify its existing dependencies, and finish with a proof, a counterexample, or a precisely narrowed replacement. A clean Lean build is required for formalization, but also explain why the theorem's statement establishes the advertised claim."**
