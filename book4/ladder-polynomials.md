# The Ladder Polynomials

Working note · 23 August 2026 · computations reproducible from the code at the end

Addresses the open item in WP44 §2, Prediction 3 — the claim that the n-bonacci
ladder is the exit sequence, "deferred to a companion paper" pending a connection
between the ADE classification and the dm³ operator chain. This note does not
supply that connection. It supplies two exact results and one honest boundary.

---

## 1. The family collapses to a single one-parameter polynomial

The n-bonacci characteristic polynomial is

    q_n(x) = x^n − x^(n−1) − … − x − 1

Multiplying by (x − 1) telescopes the whole tail:

    (x − 1)·q_n(x) = x^(n+1) − 2x^n + 1

Verified symbolically for n = 2…8. Each q_n is irreducible over ℚ (checked, same range).

So the entire ladder — φ, tribonacci, tetranacci, pentanacci, hexanacci, on up — is
one polynomial family:

    **p_n(x) = x^(n+1) − 2x^n + 1**

and the 2 in the middle coefficient is not put there. It is what the telescoping leaves.
τ = 2 is visible in the polynomial before any root is computed.

## 2. The gap to τ = 2 is exactly the root's own reciprocal power

Let r_n be the root of p_n in (1, 2), and write r = 2 − ε. Then

    r^(n+1) − 2r^n + 1 = r^n(r − 2) + 1 = −ε·r^n + 1 = 0

so

    **2 − r_n = r_n^(−n)**

exactly — not asymptotically. The distance from the n-th rung to the limit is the
reciprocal of that same rung raised to its own index. Self-referential, and closed form.

Verified to 50 significant digits for n = 2…20.

| n | r_n | 2 − r_n | r_n^(−n) | 2^(−n) |
|---|---|---|---|---|
| 2 | 1.6180339887498948 | 0.381966011250 | 0.381966011250 | 0.25 |
| 3 | 1.8392867552141611 | 0.160713244786 | 0.160713244786 | 0.125 |
| 4 | 1.9275619754829253 | 0.072438024517 | 0.072438024517 | 0.0625 |
| 5 | 1.9659482366454853 | 0.034051763354 | 0.034051763354 | 0.03125 |
| 6 | 1.9835828434243263 | 0.016417156576 | 0.016417156576 | 0.015625 |
| 8 | 1.9960311797354146 | 0.003968820265 | 0.003968820265 | 0.00390625 |
| 12 | 1.9997555009373175 | 0.000244499063 | 0.000244499063 | 0.000244140625 |
| 20 | 1.9999990463165885 | 9.53683411e−7 | 9.53683411e−7 | 9.5367432e−7 |

Since ε = r^(−n) and r → 2, the convergence is geometric with ratio → ½:
log₂(2 − r_n) / (−n) runs 0.694, 0.879, 0.947, 0.975, 0.988 … → 1.

**Consequence for WP44 Prediction 2.** That paper states the maximum Lyapunov exponent
"scales with the distance from τ = 2 in the n-bonacci sequence." That distance now has
a closed form, so the prediction is quantitative rather than qualitative: whatever the
scaling law is, its argument is r_n^(−n). This is the number to fit against. `[MODEL]`

Also: every r_n is a **Pisot number** — all conjugates strictly inside the unit disc
(checked n = 2…12; max conjugate modulus rises 0.618 → 0.980, never reaching 1).

## 3. Where τ = 2 comes from, independently

2 is not a constant chosen to make the ladder terminate. It is the threshold of a
classification theorem that has nothing to do with recurrences:

> A connected simply-laced graph has adjacency spectral radius **< 2** exactly when it
> is a finite ADE Dynkin diagram, and **= 2** exactly when it is affine (extended) ADE.

Checked numerically:

| Diagram | ρ | | Affine | ρ |
|---|---|---|---|---|
| A₅ | 1.732050807569 | | Ã₃ (3-cycle) | 2.000000000000 |
| A₁₂ | 1.941883634852 | | Ã₆ (6-cycle) | 2.000000000000 |
| D₆ | 1.902113032590 | | D̃₄ (4-leg star) | 2.000000000000 |
| E₆ | 1.931851652578 | | Ẽ₈ | 2.000000000000 |
| E₇ | 1.969615506024 | | | |
| E₈ | 1.989043790737 | | | |

Two independent families accumulate at 2 from below: the Pisot side (dynamics, the
recurrence ladder) and the Coxeter side (classification, ρ = 2cos(π/h)). Both stop
there for structural reasons of their own.

## 4. The one place they touch — and where they part

**φ = 2cos(π/5) = 1.6180339887498948…**, verified to 30 digits, and 5 is the Coxeter
number of A₄. So the bottom rung of the ladder *is* an ADE spectral radius: ρ(A₄) = φ.

Nothing above it is. Solving h = π / arccos(r_n / 2) for the higher rungs:

| n | h | integer? |
|---|---|---|
| 3 | 7.783448 | no |
| 4 | 11.637159 | no |
| **5** | **17.000510** | **no — near miss, 5.1 × 10⁻⁴ off** |
| 6 | 24.502104 | no |
| 7 | 35.033998 | no |
| 8 | 49.859430 | no |

An exhaustive scan over n < 40 against h < 60 returns exactly one coincidence: (n, h) = (2, 5).

This is expected, and the reason is worth stating because it closes off a whole class
of hoped-for identities. The ladder roots are Pisot: conjugates inside the unit disc.
The numbers 2cos(π/h) are totally real with all conjugates in [−2, 2]. The families are
essentially disjoint, and φ is the accident where a number manages to be both.

**The n = 5 near-miss is flagged deliberately.** h = 17.000510 is the kind of number that
becomes a false claim if nobody computes the next three digits. It is not 17.

## 5. What this does and does not establish

- `[VERIFIED]` The single-polynomial collapse, its irreducibility over the tested range,
  the exact gap identity 2 − r_n = r_n^(−n), the Pisot property, the ADE/affine spectral
  threshold at 2, and φ = 2cos(π/5) = ρ(A₄).
- `[MODEL]` That the shared accumulation at 2 is structurally meaningful rather than a
  coincidence of two families that both happen to live in (1, 2).
- `[OPEN]` The McKay correspondence connecting ADE to the dm³ operator chain. **Nothing
  here supplies it.** What this note does is make the target precise: any such
  correspondence must explain why one family is Pisot and the other is not, and why they
  meet only at φ. That is a sharper question than WP44 was able to ask, and a
  correspondence that cannot answer it is not the right one.

---

## Reproduce

```python
# 1 and 2
import sympy as sp
from mpmath import mp, mpf, findroot
x = sp.symbols('x'); mp.dps = 50
for n in range(2, 9):
    q = x**n - sum(x**k for k in range(n))
    assert sp.simplify(sp.expand((x-1)*q) - (x**(n+1) - 2*x**n + 1)) == 0
    assert q.as_poly().is_irreducible
for n in range(2, 21):
    r = findroot(lambda z: z**(n+1) - 2*z**n + 1, mpf('1.9') if n > 4 else mpf('1.6'))
    assert abs((2 - r) - r**(-n)) < mpf('1e-40')

# 3 and 4
import numpy as np
rho = lambda A: max(abs(np.linalg.eigvalsh(A)))
def path(n):
    A = np.zeros((n, n))
    for i in range(n-1): A[i, i+1] = A[i+1, i] = 1
    return A
assert abs(rho(path(4)) - (1 + 5**0.5)/2) < 1e-12          # rho(A_4) = phi
for n in range(3, 9):
    r = max(np.roots([1.0] + [-1.0]*n).real)
    h = np.pi / np.arccos(r/2)
    assert abs(h - round(h)) > 1e-6                          # no further coincidences
```

---

# 6. One level up — the Galois group of each rung

`chGal-galois.html` §§1–3 frames this ("when the group is the full symmetric group Sₙ,
the rung has no hidden structure: no subfield, no partial symmetry"). Here are the groups.

## Discriminants

| n | disc qₙ | factored |
|---|---|---|
| 2 | 5 | 5 |
| 3 | −44 | −2²·11 |
| 4 | −563 | −563 (prime) |
| 5 | 9584 | 2⁴·599 |
| 6 | 205937 | 205937 (prime) |
| 7 | −5390272 | −2⁶·84223 |
| 8 | −167398247 | −1319·126913 |
| 9 | 6042477824 | 2⁸·17·487·2851 |
| 10 | 249317139869 | 7·35616734267 |

No discriminant is a perfect square in ℚ, so no rung lies in Aₙ. Every Galois group
contains an odd permutation, at every level of the ladder.

## The groups

| n | Gal(qₙ) | \|G\| | n! | status |
|---|---|---|---|---|
| 2 | C₂ | 2 | 2 | proved (sympy) |
| 3 | S₃ | 6 | 6 | proved (sympy) |
| 4 | S₄ | 24 | 24 | proved (sympy) |
| 5 | S₅ | 120 | 120 | proved (sympy) |
| 6 | S₆ | 720 | 720 | proved (sympy) |
| 7 | S₇ | 5040 | 5040 | proved — Jordan, see below |
| 8 | S₈ (evidence) | — | 40320 | **not proved** |
| 9, 10 | Sₙ (evidence) | — | — | **not proved** |

**n = 7 is rigorous.** q₇ is irreducible, so the group is transitive; 7 is prime, so a
transitive group of degree 7 is primitive; Frobenius sampling over p < 4000 returns a
transposition type [2,1,1,1,1,1]; and a primitive group containing a transposition is Sₙ
(Jordan). No sampling assumption enters — one transposition suffices.

**n = 8 is evidence, and the honest word is evidence.** The transposition type
[2,1,1,1,1,1,1] does occur — first at **p = 17921**, after 2,052 usable primes, against an
expected density C(8,2)/8! ≈ 0.000694, i.e. one in ~1,440. The earlier scan to p < 4000
found none, which was not evidence of absence: it was under-sampling, and reporting it as
absence would have been a false negative dressed as a result. 21 of the 22 cycle types of
S₈ have now appeared. But 8 is not prime, so transitivity does not give primitivity, and
Jordan does not apply. **Gal(q₈) = S₈ is not established here.**

n = 9 and n = 10: irreducible, n-cycles present, 24/30 and 34/42 cycle types seen, no
transposition found in the range searched. Same status, weaker sampling.

## What this says about the ladder

Maximal Galois group means **no hidden structure**: no proper subfield, no partial
symmetry, no relation among conjugate roots beyond the ones every polynomial has. The
ladder is, at every rung above the first, as generic as an algebraic number can be.

Which isolates **n = 2 twice over**, by two independent measures:

- it is the only rung with a small Galois group (C₂ — abelian, and the field ℚ(√5));
- it is the only rung whose root is an ADE spectral radius (φ = 2cos(π/5) = ρ(A₄), §4).

The bottom rung is special in the classification sense *and* in the arithmetic sense, and
nothing above it is special in either. Two unrelated tests, one exception, the same rung.
`[OPEN]` Whether that is one fact or two is not settled here, and it is the sharpest
question this note produced.

## Reproduce

```python
import sympy as sp
x = sp.symbols('x')
for n in range(2, 7):
    q = sp.Poly(x**n - sum(x**k for k in range(n)), x)
    print(n, sp.galois_group(q)[0].order(), sp.factorial(n))

# the n=8 transposition
n, target = 8, sorted([2] + [1]*6)
q = sp.Poly(x**n - sum(x**k for k in range(n)), x)
D = sp.discriminant(q.as_expr(), x)
for p in sp.primerange(3, 60000):
    if D % p == 0: continue
    t = sorted(int(sp.Poly(f, x).degree())
               for f, _ in sp.factor_list(q.as_expr(), modulus=p)[1])
    if t == target:
        print("transposition at p =", p); break     # -> 17921
```
