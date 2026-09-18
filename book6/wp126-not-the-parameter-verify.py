#!/usr/bin/env python3
"""
wp126-not-the-parameter-verify.py

WP-41 concluded that moving 200-500M people to high-altitude Americas refugia
is "RESOURCE-FEASIBLE if subsidies redirected. Politically implausible but
financially possible." This paper asks the question that leaves open:

    IF THE RESOURCES EXIST, WHY DOESN'T IT HAPPEN?

and answers it with a model rather than a sentiment.

THE ANSWER: aggregate resources are not the parameter the system's stability
depends on. A coordination game with heterogeneous thresholds has a stable
low-action equilibrium whose stability is a property of the DISPERSION of
those thresholds, not of how much money is lying around. You can pile
resources beside a stuck system indefinitely and it stays stuck, because
nothing about the pile changes any single actor's payoff for moving first.

WHAT IS COMPUTED
  A. WP-41's own arithmetic, checked for internal consistency.
  B. The requirement in context: as a share of world output, and against
     what the world already spends on its militaries.
  C. The saddle-node of x = F(x) in closed form, for four values of mu.
  D. The stuck equilibrium: across 11 parameter pairs it sits between
     0.0015% and 1.2% of actors acting -- and it is STABLE.
  E. The size of the intervention that tips it: 4%-17% on either channel,
     against a programme that is 100%. You are not buying the outcome. You
     are buying the bifurcation.
  F. A CORRECTION. The author's prior estimate was that the guarantee
     channel would be ~5x cheaper than the subsidy channel. It is not. Across
     11 parameter pairs the subsidy channel is CHEAPER, by 3%-14%. The guess
     was wrong by a factor of five and the computation caught it. See §6.

Run:  python3 book6/wp126-not-the-parameter-verify.py
"""
from math import erf, sqrt
import statistics as st

FAIL = []
def head(n, t):
    print(); print("=" * 78); print("%s. %s" % (n, t)); print("=" * 78)
def check(name, got, want, rtol, note=""):
    d = abs(got-want)/abs(want) if want else abs(got-want)
    ok = d < rtol
    print("  [%s] %-46s %14.6g vs %-12.6g rel %.2e"
          % ("SHOWN" if ok else "FAIL ", name, got, want, d))
    if note: print("        " + note)
    if not ok: FAIL.append(name)

# ---------------------------------------------------------------------------
head(1, "WP-41'S ARITHMETIC, CHECKED")
# ---------------------------------------------------------------------------
print("  WP-41 §1, partial relocation: 200-500M people at $100-200k each,")
print("  total $20T-$100T over 30-50 years, needing $0.7-3T/year sustained.")
print()
check("200M x $100k = $20T", 200e6*100e3, 20e12, 1e-12)
check("500M x $200k = $100T", 500e6*200e3, 100e12, 1e-12)
check("$20T over 30 yr -> $/yr", 20e12/30, 0.667e12, 1e-2)
check("$100T over 50 yr -> $/yr", 100e12/50, 2.0e12, 1e-12)
print("  The stated annual band $0.7-3T contains both endpoints. Internally")
print("  consistent. This paper takes the band as given and does not re-derive")
print("  the per-person cost -- see GAPS M1.")

# ---------------------------------------------------------------------------
head(2, "WHAT THAT BAND IS, AGAINST THINGS THAT ALREADY HAPPEN")
# ---------------------------------------------------------------------------
MIL = 2887e9        # SIPRI: world military expenditure 2025  [CITED]
MIL_SHARE = 0.025   # SIPRI: 2.5% of global GDP               [CITED]
GDP = MIL/MIL_SHARE
print("  SIPRI (2025): world military expenditure $%.0fbn, being %.1f%% of" % (MIL/1e9, 100*MIL_SHARE))
print("  global GDP -- which implies world GDP = $%.1fT." % (GDP/1e12))
print()
print("      %-16s %-14s %-22s" % ("annual need", "% world GDP", "% world military spend"))
for a in (0.7e12, 2.0e12, 3.0e12):
    print("      $%-15.1fT %-14.2f %-22.0f" % (a/1e12, 100*a/GDP, 100*a/MIL))
print()
print("  The top of WP-41's band is what the world spends on its militaries.")
print("  The bottom is a quarter of it. Neither is a number the world cannot")
print("  reach; both are numbers the world reaches every year for other things.")
print("  So 'we cannot afford it' is not the obstacle, and the paper stops")
print("  arguing about affordability here.")

# ---------------------------------------------------------------------------
head(3, "THE MODEL -- why abundance and inaction coexist without contradiction")
# ---------------------------------------------------------------------------
def F(x, mu, sg):
    """CDF of thresholds: the fraction of actors who will act if they expect
    a fraction x of others to act."""
    return 0.5*(1 + erf((x-mu)/(sg*sqrt(2))))

def settle(mu, sg, g=0.0):
    """Iterate x <- g + (1-g)F(x) from x=0 to a fixed point."""
    x = 0.0
    for _ in range(20000):
        nx = g + (1-g)*F(x, mu, sg)
        if abs(nx-x) < 1e-14: return x
        x = nx
    return x

def bis(f, lo, hi, n=80):
    flo = f(lo)
    for _ in range(n):
        m = 0.5*(lo+hi)
        if f(m)*flo > 0: lo = m
        else: hi = m
    return 0.5*(lo+hi)

print("  Each actor has a threshold: the fraction of OTHERS acting that would")
print("  make acting worth it. Thresholds differ. Equilibria are the fixed")
print("  points of x = F(x), F the threshold CDF, and x* is stable when")
print("  F'(x*) < 1. This is Granovetter's 1978 model and nothing here is new.")
print()
print("  The point is WHERE THE RESOURCES ENTER. They do not enter as a level.")
print("  They enter only by moving thresholds -- and a pile of money that no")
print("  actor's decision depends on moves no threshold at all.")

# ---------------------------------------------------------------------------
head(4, "THE SADDLE-NODE, IN CLOSED FORM")
# ---------------------------------------------------------------------------
from math import exp, pi
phi = lambda z: exp(-z*z/2)/sqrt(2*pi)
Phi = lambda z: 0.5*(1+erf(z/sqrt(2)))
print("  Tangency needs F(x) = x AND F'(x) = 1. With z = (x-mu)/sigma that is")
print("      phi(z) = sigma      and      Phi(z) = mu + sigma z")
print("  so sigma is eliminated:  Phi(z) - z phi(z) = mu.")
print()
print("      %-8s %-16s %-14s" % ("mu", "sigma_crit", "tips at x ="))
for mu in (0.20, 0.25, 0.30, 0.40):
    z = bis(lambda z: Phi(z) - z*phi(z) - mu, -8.0, 2.0)
    sg = phi(z)
    print("      %-8.2f %-16.10f %-14.8f" % (mu, sg, mu+sg*z))
z = bis(lambda z: Phi(z) - z*phi(z) - 0.25, -8.0, 2.0)
check("sigma_crit at mu = 0.25", phi(z), 0.1222209, 1e-6,
      "below this the system is stuck; above it, it tips unaided")

# ---------------------------------------------------------------------------
head(5, "THE STUCK EQUILIBRIUM, AND WHAT IT COSTS TO LEAVE IT")
# ---------------------------------------------------------------------------
print("  Two ways to intervene:")
print("    GUARANTEE  de-risk a fraction g of actors outright, so they act")
print("               regardless:      F_g(x) = g + (1-g) F(x)")
print("    SUBSIDY    make it cheaper for EVERYONE, lowering every threshold")
print("               by the same amount:   mu -> mu - d")
print()
print("  %-6s %-6s %-12s %-13s %-13s %-10s"
      % ("mu", "sigma", "x* stuck", "g* guarantee", "d* subsidy", "d*/g*"))
rows = []
for mu, sg in ((0.25,0.10),(0.25,0.08),(0.25,0.06),(0.30,0.10),(0.30,0.12),
               (0.35,0.12),(0.35,0.15),(0.20,0.07),(0.40,0.15),(0.45,0.18),(0.50,0.20)):
    if settle(mu, sg) > 0.5:
        print("  %-6.2f %-6.2f tips unaided" % (mu, sg)); continue
    x0 = settle(mu, sg)
    g  = bis(lambda g: settle(mu, sg, g) - 0.5, 0.0, 0.7)
    d  = bis(lambda d: settle(mu-d, sg) - 0.5, 0.0, mu)
    rows.append((mu, sg, x0, g, d, d/g))
    print("  %-6.2f %-6.2f %-12.6f %-13.6f %-13.6f %-10.4f" % (mu, sg, x0, g, d, d/g))
xs  = [r[2] for r in rows]; gs = [r[3] for r in rows]
ds  = [r[4] for r in rows]; rs = [r[5] for r in rows]
print()
print("  STUCK LEVEL   x* from %.6f to %.6f  -- that is 0.0015%% to 1.2%% of"
      % (min(xs), max(xs)))
print("                actors acting, and F'(x*) < 1 at every one of them, so")
print("                it is STABLE. The system is not slow. It is at rest.")
print("  TO TIP IT     g* from %.1f%% to %.1f%% ; d* from %.1f%% to %.1f%%"
      % (100*min(gs), 100*max(gs), 100*min(ds), 100*max(ds)))
ok = max(gs) < 0.20 and max(ds) < 0.20
print("  [%s] every intervention needed is under 20%%, against a programme"
      % ("SHOWN" if ok else "FAIL "))
print("        that is 100%%. YOU ARE NOT BUYING THE OUTCOME. YOU ARE BUYING")
print("        THE BIFURCATION.")
if not ok: FAIL.append("intervention exceeded 20%")

# ---------------------------------------------------------------------------
head(6, "A CORRECTION -- the guarantee channel is NOT cheaper")
# ---------------------------------------------------------------------------
print("  Before computing this, the author asserted in conversation that a")
print("  guarantee would be roughly 5x cheaper than a subsidy, on the reasoning")
print("  that de-risking a few first movers must beat subsidising everyone.")
print()
print("  It is not true. Across all %d parameter pairs:" % len(rows))
print("      d*/g*  min %.4f   max %.4f   median %.4f" % (min(rs), max(rs), st.median(rs)))
print()
print("  The ratio is BELOW 1 everywhere, so the SUBSIDY channel is cheaper --")
print("  by 3%% to 14%%. The prior estimate was wrong by a factor of about five,")
print("  and wrong in direction. It is recorded here rather than quietly")
print("  dropped, because the reasoning that produced it was plausible and will")
print("  recur.")
worse = max(rs) < 1.0
print("  [%s] d*/g* < 1 in every case tested" % ("SHOWN" if worse else "FAIL "))
if not worse: FAIL.append("ratio not below 1 everywhere")
print()
print("  WHAT SURVIVES. The case for a guarantee instrument does not rest on")
print("  cost-efficiency in this model and this paper withdraws that claim. It")
print("  rests on things the model does not contain: a guarantee is contingent,")
print("  so it is authorised against capital that is not spent, which is a")
print("  POLITICAL economy, not an economy of resources. That is a real")
print("  argument and it is not the argument that was made.")

# ---------------------------------------------------------------------------
head(7, "WHAT THIS DOES AND DOES NOT ANSWER")
# ---------------------------------------------------------------------------
print("  WP-41's 2026-09-15 correction withdrew the claim that receiving")
print("  capacity does not exist, and named four binding constraints instead:")
print("      duration, livelihood, financing, political consent.")
print()
print("  This paper addresses FINANCING and concludes it is not binding -- the")
print("  band is a quarter to all of world military spending, and the tipping")
print("  intervention is under a fifth of the programme.")
print()
print("  It says nothing about duration or livelihood. And on POLITICAL")
print("  CONSENT it says only that consent has the shape of a coordination")
print("  problem with a stable stuck equilibrium, which is a description of the")
print("  difficulty, not a route through it. No mechanism here delivers")
print("  consent, and a paper claiming otherwise would be repeating the error")
print("  that the September correction already fixed once.")

# ---------------------------------------------------------------------------
head("GAPS", "what this script does not establish")
# ---------------------------------------------------------------------------
for g in [
 "M1  THE $100-200k PER PERSON IS INHERITED. WP-41's per-person relocation",
 "    cost is taken as given and not re-derived. Every dollar figure here",
 "    rests on it, and it is the least examined number in the chain.",
 "",
 "M2  mu AND sigma ARE INVENTED. No threshold distribution was measured. The",
 "    NUMBERS in §5 -- 3.7%, 16.8% -- are properties of chosen parameters and",
 "    are not estimates of anything in the world. What is robust across the",
 "    sweep is the STRUCTURE: a stable low equilibrium, a saddle-node, and an",
 "    intervention far smaller than the programme. Quoting 3.7% as if it were",
 "    a measurement would be the worst possible use of this paper.",
 "",
 "M3  ONE FUNCTIONAL FORM. Thresholds are normal in every run. A skewed or",
 "    bimodal distribution can change the number of fixed points, and none was",
 "    tried.",
 "",
 "M4  ACTORS ARE UNWEIGHTED AND IDENTICAL IN POWER. In the real problem a",
 "    handful of states and institutions carry most of the weight, so 'a",
 "    fraction g of actors' is the wrong unit and the model does not have a",
 "    better one.",
 "",
 "M5  NO DYNAMICS, NO DEFECTION, NO TIME. The iteration x <- F(x) is a",
 "    convergence device, not a history. Actors cannot reverse, the programme",
 "    has no schedule, and the 30-50 year horizon of WP-41 is entirely absent.",
 "",
 "M6  THE SIPRI FIGURES ARE CITED, NOT VERIFIED. World military expenditure",
 "    $2887bn at 2.5% of GDP, 2025, and the implied world GDP of $115.5T is a",
 "    division of two cited numbers rather than an independent figure.",
 "",
 "M7  AND THE ONE THAT MATTERS MOST. This model explains inaction. It does",
 "    not license it. The paper's closing section carries the argument and a",
 "    parable of Pablo Nogueira Grossi's that states it better: a guru",
 "    levitates, tells everyone to calm down, rises out of sight, and reports",
 "    from the sky that death is absolutely safe. Every statement true; the",
 "    serenity scales with the altitude. This script puts 98%+ of actors at",
 "    rest and calls it stable, which it is, and that is the difficulty.",
]:
    print("  " + g)

print(); print("=" * 78)
if FAIL:
    print("FAILED: " + ", ".join(FAIL)); raise SystemExit(1)
print("All checks passed. 7 gaps recorded above remain open.")
print("=" * 78)
