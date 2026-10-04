#!/usr/bin/env python3
"""ch05-contact-normal-form-verify.py -- R29 three-point audit, page 2 (2026-10-03).

Blocks (each states a claim the page makes, or a claim the audit adds):
 [1] exact: zdot at r=1 is 1 for every z, so Gamma is a helix, not a closed orbit (symbolic, no numerics)
 [2] exact: the normal-form radial coefficient mu(1-exp(-b z)) is negative only for z>0 when mu<0
 [3] numeric: page says "symmetric ball of guaranteed convergence |r-1|<1/3"; test it at z(0)=0
 [4] control: the same test must PASS at a z(0) where the ball does lie in the basin (else the checker cannot detect convergence)
 [5] cited, not re-derived (R19): r*(z0=0) = 0.77594058, docs/definitions.md B(Gamma) row

Needs scipy (DOP853). Standard library otherwise.
"""
import math, sys
from scipy.integrate import solve_ivp

FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + ("  " + detail if detail else ""))
    if not ok: FAIL.append(label)

def rhs(t, y):
    r, z = y
    e = math.exp(-z)
    return [r*(1 - r*r) + 2*(r - 1)*e, r*r - 2*(r - 1)**2*e]

def converges(r0, z0, T=80.0):
    blow = lambda t, y: abs(y[0]) - 1e6
    blow.terminal = True
    s = solve_ivp(rhs, [0, T], [r0, z0], method="DOP853", rtol=1e-13, atol=1e-15, events=[blow])
    r, z = s.y[0, -1], s.y[1, -1]
    return s.t[-1] >= T and abs(r - 1) < 1e-6 and z > 0

# [1] zdot at r=1 : r^2 - 2(r-1)^2 e^{-z} = 1 - 0 = 1, for every z
vals = [rhs(0, [1.0, z])[1] for z in (-3, -1, 0, 1, 5, 20)]
check("[1] zdot = 1 on r=1 for all z (Gamma is a helix, z advances; no closed orbit)", all(v == 1.0 for v in vals), str(vals))
check("[1] rdot = 0 on r=1 (so r=1 is invariant, as the page says)", all(rhs(0, [1.0, z])[0] == 0.0 for z in (-3, 0, 5)))

# [2] radial coefficient of the normal form, mu=-1, beta=2
mu, b = -1.0, 2.0
coef = lambda z: mu*(1 - math.exp(-b*z))
check("[2] coefficient < 0 (contracts) for z>0", coef(0.5) < 0 and coef(2.0) < 0)
check("[2] coefficient > 0 (EXPANDS) for z<0 although mu<0", coef(-0.5) > 0, f"coef(-0.5)={coef(-0.5):.4f}")

# [3] symmetric ball (2/3,4/3) at z(0)=0
rs = [2/3 + k*(2/3)/200 for k in range(1, 200)]
bad = [r for r in rs if not converges(r, 0.0)]
check("[3] page claim 'ball |r-1|<1/3 guaranteed convergence' is REFUTED at z(0)=0 (PASS = counterexamples found)",
      bool(bad), f"{len(bad)} of {len(rs)} start points in (2/3,4/3) do not converge, r in [{min(bad):.4f},{max(bad):.4f}]" if bad else "no counterexample found")

# [4] control: at z(0)=2 the inner side of the ball converges, so the checker can say PASS
rs2 = [2/3 + k*(1/3)/100 for k in range(0, 101)]          # inner half (2/3,1]
check("[4] control: inner half of the ball converges at z(0)=2", all(converges(r, 2.0) for r in rs2))
check("[4] control: a start well outside any basin does not converge (r=0.05, z(0)=0)", not converges(0.05, 0.0))

# [5] cited
print("NOTE [5] r*(z(0)=0)=0.77594058 is DECIDED/checked in docs/definitions.md (B(Gamma) row); cited, not re-derived (R19).")

print("\n[HONESTY] Block [1], [2] are exact. Blocks [3], [4] are numerical (DOP853, rtol 1e-13) on a grid of start points: evidence, not proof.")
print("[HONESTY] This script shows the page's wording 'guaranteed' and 'limit cycle' do not hold as stated; it does not say what the right wording is (author's call, R28).")
print("[HONESTY] The Lean files the page cites are not named by path, so the vacuity check (point 1) could not be run on them; see docs/audit-log.md.")
sys.exit(1 if FAIL else 0)
