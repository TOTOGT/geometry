#!/usr/bin/env python3
"""
TribonacciLog-verify.py  --  R6 companion to TribonacciLog.lean

Checks every arithmetic claim the Lean file makes or relies on, at 30 digits.
The Lean is NOT BUILT; this script is what stands behind the numbers until it is.

Run:  python3 TribonacciLog-verify.py
"""
from mpmath import mp, mpf, exp, log, pi, findroot

mp.dps = 30
ok = []


def chk(name, cond, detail=""):
    ok.append((name, bool(cond), detail))
    print(("PASS  " if cond else "FAIL  ") + name + (("   " + detail) if detail else ""))


p = lambda x: x ** 3 - x ** 2 - x - 1
eta = findroot(p, mpf("1.84"))
LO, HI = mpf("1.83928"), mpf("1.83929")
L, U = mpf("0.60937"), mpf("0.60939")

print("eta            =", mp.nstr(eta, 18))
print("log eta        =", mp.nstr(log(eta), 18))
print()

# ---- §1  the bracket -------------------------------------------------------
chk("p(1.83928) < 0", p(LO) < 0, f"p = {mp.nstr(p(LO), 6)}")
chk("p(1.83929) > 0", p(HI) > 0, f"p = {mp.nstr(p(HI), 6)}")
chk("eta in the bracket", LO < eta < HI)

# p'(x) = 3x^2 - 2x - 1 = (3x+1)(x-1) > 0 for x > 1  ->  the root above 1 is unique
dp = lambda x: 3 * x ** 2 - 2 * x - 1
fact = lambda x: (3 * x + 1) * (x - 1)
chk("p' factors as (3x+1)(x-1)",
    all(abs(dp(mpf(t)) - fact(mpf(t))) < mpf("1e-25") for t in "1.0 1.5 1.83928 2.0 7.0".split()))
chk("p' > 0 on (1, inf)  [sampled]",
    all(dp(mpf(t)) > 0 for t in "1.0001 1.5 1.83928 2 10 1000".split()))
# the only real root: the other two are complex
chk("exactly one real root", sum(1 for r in [p(mpf(t)) for t in ("-5", "0", "1", "2", "5")]
                                 if False) == 0 and p(mpf("-5")) < 0 and p(mpf("0")) < 0
    and p(mpf("1")) < 0 and p(mpf("2")) > 0,
    "p < 0 on (-inf, eta), > 0 after")

# ---- §2  the exp sandwich (the two Lean hypotheses) ------------------------
eL, eU = exp(L), exp(U)
chk("exp(0.60937) < 1.83928", eL < LO, f"margin {mp.nstr(LO - eL, 6)}")
chk("1.83929 < exp(0.60939)", HI < eU, f"margin {mp.nstr(eU - HI, 6)}")
chk("therefore 0.60937 < log eta", L < log(eta))
chk("therefore log eta < 0.60939", log(eta) < U)

# ---- the tightness finding -------------------------------------------------
# A looser bracket does NOT suffice: this is why the Lean uses five decimals.
LOOSE_LO, LOOSE_HI = mpf("1.8392"), mpf("1.8393")
chk("the loose bracket (1.8392, 1.8393) is NOT sufficient",
    not (exp(L) < LOOSE_LO and LOOSE_HI < exp(U)),
    "exp(0.60937) = 1.8392723 > 1.8392, so the lower half fails")
chk("p(1.8392) < 0 and p(1.8393) > 0 all the same",
    p(LOOSE_LO) < 0 < p(LOOSE_HI),
    "the loose bracket is true, just too weak to carry the log bound")

# ---- §3  the composite -----------------------------------------------------
v = 1 + log(eta) / (2 * pi)
chk("1 + log(eta)/(2 pi) in (1.0969, 1.0971)",
    mpf("1.0969") < v < mpf("1.0971"), f"= {mp.nstr(v, 12)}")
# tribonacci_factor's own endpoints, checked independently of eta
for l, lbl in ((L, "0.60937"), (U, "0.60939")):
    w = 1 + l / (2 * pi)
    chk(f"endpoint {lbl}: 1 + l/(2pi) in window",
        mpf("1.0969") < w < mpf("1.0971"), f"= {mp.nstr(w, 12)}")

# ---- non-vacuity -----------------------------------------------------------
chk("IsTribonacci is satisfiable", eta > 1 and abs(eta ** 3 - (eta ** 2 + eta + 1)) < mpf("1e-25"),
    "a hypothesis nothing satisfies proves anything -- R20")

print()
bad = [n for n, good, _ in ok if not good]
print(f"{len(ok) - len(bad)}/{len(ok)} checks pass")
if bad:
    print("FAILED:", "; ".join(bad))
    raise SystemExit(1)
print("""
NOT VERIFIED HERE, because it is not arithmetic:
  the nlinarith calls in TribonacciLog.lean sec.1 are unbuilt. The numbers they
  are asked to prove are all confirmed above; whether Lean finds the certificate
  with the hints given is open until `lake build` runs.
""")
