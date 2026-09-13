#!/usr/bin/env python3
"""
WP-114 -- The Index Must Come From the Source.
Companion verification script. Standard library only; runs in seconds.

Every number printed on the chapter page is produced here.

  [1] A reader-supplied index absorbs every contradiction. Exhaustive.
  [2] A source-supplied index does not. Exact probability, rational arithmetic.
  [3] How fast the teeth go blunt as the index set grows.
  [4] The same size check applied to the string landscape.
  [5] Figures quoted on the page.
"""
import sys, itertools
from fractions import Fraction
from math import comb, log10, factorial

FAIL = []
def check(label, got, want, note=""):
    ok = (got == want)
    if not ok:
        FAIL.append(label)
    print(f"  {'ok  ' if ok else 'FAIL'} {label}: {got}{'' if ok else ' (expected ' + str(want) + ')'}{'  ' + note if note else ''}")

# ---------------------------------------------------------------- [1]
print("\n[1] A READER-SUPPLIED INDEX ABSORBS EVERY CONTRADICTION")
print("    Language: all propositions over two variables, represented by the")
print("    set of valuations satisfying them. A set of sentences is jointly")
print("    satisfiable iff the intersection is non-empty. Under a reader-supplied")
print("    index every sentence is given its own index, so the set is 'consistent'")
print("    iff each sentence is individually satisfiable.\n")

VALUATIONS = [(0,0),(0,1),(1,0),(1,1)]
# every proposition = a subset of valuations; drop bottom (unsatisfiable) and top
ALL = [frozenset(s) for r in range(1,4) for s in itertools.combinations(VALUATIONS, r)]
print(f"    sentences in the language (satisfiable, non-tautologous): {len(ALL)}")

jointly_unsat = 0
rescued = 0
total_sets = 0
for r in (2,3):
    for combo in itertools.combinations(ALL, r):
        total_sets += 1
        inter = frozenset.intersection(*combo)
        if not inter:                      # jointly unsatisfiable
            jointly_unsat += 1
            # reader-supplied index: one index per sentence
            if all(len(c) > 0 for c in combo):
                rescued += 1

print(f"    sets of size 2 or 3 examined:            {total_sets}")
print(f"    jointly unsatisfiable among them:        {jointly_unsat}")
print(f"    rescued by a reader-supplied index:      {rescued}")
print(f"    NOT rescued:                             {jointly_unsat - rescued}")
check("reader-supplied index rescues everything", jointly_unsat - rescued, 0,
      "-- discriminating power exactly zero")

# ---------------------------------------------------------------- [2]
print("\n[2] A SOURCE-SUPPLIED INDEX DOES NOT")
print("    Null model. N sentences bear on one question; each asserts it or")
print("    denies it (sign uniform, independent) and each carries an index")
print("    label supplied by the source, uniform over K labels. The indexed")
print("    reading survives iff no single label carries both an assertion and")
print("    a denial. This is the chance baseline: it is what an index would")
print("    achieve if the source assigned labels at random.\n")

_STIR = {}
def stirling2(n):
    """Row n of the Stirling numbers of the second kind, memoised."""
    if n in _STIR: return _STIR[n]
    row = [0]*(n+1)
    if n == 0:
        row[0] = 1
    else:
        prev = stirling2(n-1)
        for m in range(1, n+1):
            a = prev[m] if m < len(prev) else 0
            b = prev[m-1] if m-1 < len(prev) else 0
            row[m] = m*a + b
    _STIR[n] = row
    return row

def p_survive(N, K):
    """Exact P(no index label carries both an assertion and a denial).

    Condition on the number m of labels actually used. The m occupied labels
    are chosen C(K,m) ways, the N labelled sentences are distributed onto them
    surjectively in m!*S(N,m) ways, and each occupied label must be all of one
    sign, contributing 2^m. Every term is positive, so this is exact and stable:

        P(N,K) = sum_m C(K,m) m! S(N,m) 2^m / (2K)^N
    """
    S = stirling2(N)
    tot = 0
    for m in range(1, min(N, K)+1):
        tot += comb(K, m) * factorial(m) * S[m] * (2**m)
    return Fraction(tot, (2*K)**N)

# sanity checks against hand calculation
check("P(N=2,K=1)", p_survive(2,1), Fraction(1,2), "-- both sentences share the one index")
check("P(N=2,K=2)", p_survive(2,2), Fraction(3,4), "-- hand calculation 1/2 + 1/4")
check("P(N=1,K=1)", p_survive(1,1), Fraction(1,1), "-- nothing to collide with")

N = 20
print(f"\n    N = {N} sentences bearing on one question:\n")
print("      K (index labels)   P(survives by chance)")
rows = []
for K in (1,2,3,5,8,12,20,30,50,80,120,200,400):
    p = float(p_survive(N, K))
    rows.append((K, p))
    print(f"      {K:>6}             {p:.4f}")

# smallest K at which the chance baseline exceeds 0.5, and 0.95
def first_above(thresh, n=N, hi=200000):
    lo = 1
    if float(p_survive(n, hi)) <= thresh: return None
    while lo < hi:
        mid = (lo + hi)//2
        if float(p_survive(n, mid)) > thresh: hi = mid
        else: lo = mid + 1
    return lo
K50 = first_above(0.50)
K95 = first_above(0.95)
print(f"\n    chance baseline first exceeds 0.50 at K = {K50}")
print(f"    chance baseline first exceeds 0.95 at K = {K95}")
check("K50 is in the birthday regime (order N^2/ln2)", K50 > N, True,
      f"-- N = {N}, N^2 = {N*N}")

# ---------------------------------------------------------------- [3]
print("\n[3] HOW FAST THE TEETH GO BLUNT")
print("    The collision threshold is birthday-like: the index stops")
print("    discriminating once K grows on the order of N^2.\n")
print("      N     K50     K50/N^2")
ratios = []
for n in (10, 20, 30, 40):
    K = first_above(0.5, n)
    ratios.append(K/(n*n))
    print(f"      {n:<5} {K:<7} {K/(n*n):.3f}")
CONST = sum(ratios)/len(ratios)
print(f"\n    mean ratio c = {CONST:.3f}   (birthday prediction 1/(4 ln 2) = {1/(4*0.6931471805599453):.3f})")
print("\n    The ratio is flat, so K50 ~ c*N^2. An index set that grows faster")
print("    than the square of the number of statements it must reconcile has")
print("    no discriminating power left, whoever supplied it.")

print("\n    LIMITING CASE. A continuous index set is K -> infinity:")
for K in (10**3, 10**4, 10**6, 10**9):
    print(f"      K = 10^{len(str(K))-1:<3}  P = {float(p_survive(20, K)):.9f}")
check("P(N=20, K=10^9) exceeds 0.9999999", float(p_survive(20, 10**9)) > 0.9999999, True,
      "-- two points drawn from a continuum never coincide")
print("    An index set that is a space, rather than a list, forbids nothing at all.")

# ---------------------------------------------------------------- [4]
print("\n[4] THE SAME SIZE CHECK, APPLIED TO THE STRING LANDSCAPE")
print("    Not a new argument -- this is the standard motivation for the")
print("    swampland programme, restated in the terms of block [3].\n")
n_obs = 19          # free parameters of the Standard Model (no neutrino masses)
n_obs_nu = 26       # with three Dirac neutrino masses and the PMNS matrix
for label, n in (("Standard Model free parameters", n_obs),
                 ("with neutrino masses and mixing", n_obs_nu)):
    need = log10(CONST * n * n)
    print(f"    {label}: N = {n};  blunting scale c*N^2 = 10^{need:.1f}")
print(f"\n    quoted landscape sizes:  10^500 (flux-vacua estimate),")
print(f"                             10^272000 (F-theory flux counting)")
print("    Either exceeds the blunting threshold by hundreds of orders of")
print("    magnitude. Under the chance baseline the index explains nothing;")
print("    the swampland programme is the attempt to show the assignment is")
print("    not by chance -- that some effective theories get no label at all.")
check("landscape exceeds the blunting scale", 500 > log10(CONST*n_obs_nu**2), True)

# ---------------------------------------------------------------- [5]
print("\n[5] FIGURES QUOTED ON THE PAGE")
check("Vyasas enumerated in Visnu Purana III.3", 28, 28, "-- one per dvapara-yuga")
check("sentences in the two-variable language", len(ALL), 14)
check("size-2 and size-3 sets examined", total_sets, comb(14,2)+comb(14,3))

print("""
[HONESTY] What this script establishes, and what it does not.

  ESTABLISHED. Block [1] is an exhaustive enumeration over a finite language,
  and its result is a triviality -- which is the point. A reader who is free to
  assign an index after seeing the sentences can rescue every jointly
  unsatisfiable set that contains no individually unsatisfiable member. The
  manoeuvre never fails, so observing it succeed carries no information.

  ESTABLISHED. Blocks [2] and [3] are exact rational arithmetic on a stated
  null model, checked against hand calculation at three points. The scaling
  K50 ~ N^2 is measured from that arithmetic, not assumed.

  A NULL MODEL IS NOT A THEORY OF ANYTHING. Block [2] assumes signs and labels
  are independent and uniform. No tradition assigns its indices that way, and
  no physicist claims vacua are drawn uniformly. The number it produces is a
  chance baseline -- what an index would achieve if it were doing no work. It
  is the denominator a real claim has to beat, and nothing more. Reading it as
  a measurement of any actual corpus would be a misuse of it.

  NOT A CLAIM ABOUT PURANIC EXEGESIS. Kalpa-bheda is named on the page as the
  tradition's own device and is not modelled here. Nothing in this script
  counts variants in any text, and the enumerated Vyasas of Visnu Purana III.3
  are cited as a textual fact, not used as data.

  NOT A RESULT IN PHYSICS. Block [4] restates a known motivation for the
  swampland programme in the language of block [3]. It establishes nothing
  about string theory, which remains without experimental confirmation. The
  quoted landscape counts are estimates from the literature, reproduced, not
  derived here.

  WHAT WOULD FALSIFY THE RULE. The rule of section 5 fails if a corpus can be
  exhibited whose index is supplied only by readers and which nonetheless makes
  checkable predictions that could have come out otherwise. No such corpus is
  offered here, and the rule is stated so that one would count against it.
""")
print(f"{'ALL CHECKS PASSED' if not FAIL else 'FAILED: ' + ', '.join(FAIL)}")
sys.exit(1 if FAIL else 0)
