#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book14/ch10-verify.py -- every number on book14/ch10-where-counting-meets-chance.html. Run first (R24).
    python3 book14/ch10-verify.py [--downloads DIR]
  [1] counting is chance: two dice, by listing all 36 outcomes and by the formula
  [2] a chain (series): p^n, checked by exact fractions and by a seeded simulation; the 14-step coin flip
  [3] a swarm of checkers (parallel): 1-(1-q)^n, the binomial counts, and the shared blind spot
  [4] the Swarm Simulator (Nogueira Grossi 2026): shared intent is the chain law; the printed bound fails
      from a large start; how often depends on where you look
  [HONESTY]
"""
import itertools, os, random, re, sys
from fractions import Fraction as Fr
from math import comb, isclose
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)

print("[1] counting is chance")
sevens = sum(1 for a, b in itertools.product(range(1, 7), repeat=2) if a + b == 7)
check("two dice: 36 outcomes, 6 of them sum to 7, so chance 1/6", sevens == 6 and Fr(sevens, 36) == Fr(1, 6))
check("the multiplication principle: k^n paths (6 outcomes, 4 throws = 1296)", len(list(itertools.product(range(6), repeat=4))) == 6 ** 4 == 1296)
check("choosing: C(5,2) = 10 ways to pick which 2 of 5 checks catch an error",
      len(list(itertools.combinations(range(5), 2))) == comb(5, 2) == 10)

print("[2] a chain: every step must hold")
p = Fr(95, 100)
check("10 steps at 95%: p^10 = 0.5987", isclose(float(p ** 10), 0.5987, abs_tol=5e-5), f"{float(p**10):.6f}")
check("50 steps at 95%: p^50 = 0.0769", isclose(float(p ** 50), 0.0769, abs_tol=5e-5), f"{float(p**50):.6f}")
n = 1
while p ** n >= Fr(1, 2): n += 1
check("the first chain at 95% per step that is worse than a coin flip has 14 steps",
      n == 14 and p ** 13 > Fr(1, 2) > p ** 14, f"p^13={float(p**13):.4f}, p^14={float(p**14):.4f}")
need = 0.9 ** (1 / 50)
check("to be right 90% of the time over 50 steps each step must be right 99.79% of the time",
      isclose(need, 0.99790, abs_tol=5e-6), f"{need:.6f}")
random.seed(2026)
trials = 200000
hits = sum(all(random.random() < 0.95 for _ in range(10)) for _ in range(trials)) / trials
check("simulation (seed 2026, 200,000 chains of 10): about 0.599", isclose(hits, 0.5987, abs_tol=0.005), f"{hits:.4f}")

print("[3] a swarm of checkers: one is enough")
for q in (0.5, 0.7, 0.9):
    row = [1 - (1 - q) ** k for k in range(1, 6)]
    check(f"q={q}: detection 1-(1-q)^n, n=1..5 = {[round(x, 4) for x in row]}",
          all(isclose(x, y, abs_tol=1e-12) for x, y in zip(row, [sum(comb(k, r) * q ** r * (1 - q) ** (k - r) for r in range(1, k + 1)) for k in range(1, 6)])))
check("three checkers at 70% each all miss with chance 0.027", isclose(0.3 ** 3, 0.027, abs_tol=1e-12))
check("binomial: chances of exactly r of 5 catching sum to 1", isclose(sum(comb(5, r) * 0.7 ** r * 0.3 ** (5 - r) for r in range(6)), 1.0))
# shared blind spot: a fraction b of errors is invisible to every checker; the rest is caught with chance q each
b, q = 0.3, 0.7
lim = [(1 - b) * (1 - (1 - q) ** k) for k in (1, 3, 10, 100)]
check("with 30% of errors invisible to all checkers, detection never exceeds 70%: 0.49, 0.68, 0.70, 0.70",
      [round(x, 2) for x in lim] == [0.49, 0.68, 0.70, 0.70] and max(lim) < 0.7 + 1e-12, str([round(x, 4) for x in lim]))

print("[4] the Swarm Simulator (Definitions 3.1-3.4, Nogueira Grossi 2026)")
tq, aq, eta, drag, beta, reuse, avq, alpha = 0.65, 0.80, 0.20, 1.50, 0.10, 0.50, 0.22, 0.02
def step(s, t):
    I, C, M, F = s
    In = I * tq * aq * (1 - eta)
    return (In, C * In / (1 + drag), M * (1 + beta * reuse) * avq, 1 + alpha * t)
LI = tq * aq * (1 - eta); LC = LI / (1 + drag); LM = (1 + beta * reuse) * avq; L = LI + LC + LM
check("the printed constants: LI=0.4160, LC=0.1664, LM=0.2310, L=0.8134 < 1",
      [round(x, 4) for x in (LI, LC, LM, L)] == [0.4160, 0.1664, 0.2310, 0.8134])
s = (1.0, 1.0, 1.0, 0.0); traj = [s]
for t in range(1, 201):
    s = step(s, t); traj.append(s)
check("shared intent is a chain: I_t = I_0 * 0.416^t exactly, at t = 1, 10, 20, 60",
      all(isclose(traj[t][0], 0.416 ** t, rel_tol=1e-9) for t in (1, 10, 20, 60)))
check("so I_10 = 1.55e-4 and I_20 = 2.41e-8 (starting from 1)",
      isclose(traj[10][0], 1.5521e-4, rel_tol=1e-3) and isclose(traj[20][0], 2.4092e-8, rel_tol=1e-3))
check("I, C and M all decay to 0; the diffusion term does not settle: F = 3.0 at t=100, 5.0 at t=200",
      max(traj[200][:3]) < 1e-70 and isclose(traj[100][3], 3.0) and isclose(traj[200][3], 5.0))
def violates(X0, T=30):
    s = (*X0, 0.0); n0 = sum(X0)
    for t in range(1, T + 1):
        s = step(s, t)
        if sum(abs(x) for x in s[:3]) > L ** t * n0 + 1e-12: return True
    return False
check("the paper's three starts satisfy the printed bound ||X_t - X*|| <= L^t ||X_0 - X*||, X* = (0,0,0)",
      not any(violates(x) for x in [(2.0, 0.5, 1.5), (0.3, 1.8, 0.4), (1.5, 1.5, 0.8)]))
seq = []; s = (100.0, 10.0, 1.0, 0.0)
for t in range(1, 6):
    s = step(s, t); seq.append((round(sum(abs(x) for x in s[:3]), 1), round(L ** t * 111.0, 1)))
check("from (100, 10, 1) the bound fails at every step t = 1..5: size 208.2, 1169.2, 3324.2, 3976.5, 1981.4",
      [a for a, _ in seq] == [208.2, 1169.2, 3324.2, 3976.5, 1981.4] and all(a > b for a, b in seq), str(seq))
random.seed(2026)
def frac(hi, N=5000):
    return sum(violates((random.uniform(0, hi), random.uniform(0, hi), random.uniform(0, hi))) for _ in range(N)) / N
f3, f10, f100 = frac(3), frac(10), frac(100)
check("starts drawn from [0,3]^3 never break the bound (0%); from [0,10]^3 about 3%; from [0,100]^3 about 88%",
      f3 == 0 and 0.01 < f10 < 0.06 and f100 > 0.80, f"{f3:.4f}, {f10:.4f}, {f100:.4f}")
check("three passing tests are weak evidence: if 10% of starts fail, three random tests all pass with chance 0.729",
      isclose(0.9 ** 3, 0.729, abs_tol=1e-12))
D = None
for c in ("~/mnt/Downloads", "~/Downloads"):
    if "--downloads" in sys.argv: D = Path(sys.argv[sys.argv.index("--downloads") + 1]); break
    if Path(os.path.expanduser(c)).is_dir(): D = Path(os.path.expanduser(c)); break
sim = next(iter(sorted(D.glob("swarm_simulator*.py"))), None) if D else None
if sim:
    src = sim.read_text(encoding="utf-8").split("# ── Figure 1")[0]; ns = {}; exec(src, ns)
    P = ns["SwarmParams"](); ok = True; st = (1.0, 1.0, 1.0, 0.0); mine = (1.0, 1.0, 1.0, 0.0)
    for t in range(1, 61):
        st = ns["step"](st, P, t); mine = step(mine, t)
        ok &= all(isclose(a, b, rel_tol=1e-9, abs_tol=1e-300) for a, b in zip(st, mine))
    check(f"the author's swarm_simulator.py ({sim.name}) agrees with the Definitions above for 60 steps", ok)
else:
    print("NOTE swarm_simulator.py not found in Downloads; the cross-check with the author's code was skipped")

print("[5] the Lean")
lean = (ROOT / "book14/SwarmSimulatorV3.lean").read_text(encoding="utf-8")
rep = (ROOT / "book14/swarmsimulatorv3.axioms.txt").read_text(encoding="utf-8")
for t in ["orbit_nrm_le", "paper_bound", "step_lipschitz_ball", "fixed_point_zero", "two_clusters",
          "no_global_lipschitz", "diffuse_unbounded", "printed_bound_fails", "default_radius"]:
    check(f"SwarmSimulatorV3.lean proves {t}, and its axiom report lists only the permitted three",
          f"theorem {t}" in lean and f"#print axioms SwarmSimulatorV3.{t}" in lean
          and re.search(rf"SwarmSimulatorV3\.{t}' depends on axioms: \[propext, Classical\.choice, Quot\.sound\]", rep) is not None)
check("no sorry", "sorry" not in re.sub(r"/-.*?-/|--[^\n]*", "", lean, flags=re.S))
check("the printed default constants in the Lean file are the exact values 52/125, 2/5, 231/1000",
      all(x in lean for x in ("52 / 125", "2 / 5", "231 / 1000")))

print("[HONESTY]")
print("  The chain and swarm laws assume independent steps and independent checkers. Real errors are correlated,")
print("  and the 30%-blind-spot model is an illustration, not a measurement. The 95% per step figure is a chosen")
print("  example, not the accuracy of any system. The Swarm Simulator is checked as a program: Definitions 3.1-3.4")
print("  as printed in the March 2026 PDF, cross-checked with the author's code when it is present. Its theorems")
print("  are the author's; the open notes S1 and S4 already list the missing Lipschitz and induction proofs. The")
print("  failure of the printed bound from (100,10,1) is computed; a repair (a bounded region, or the triangular")
print("  I, C, M structure with F set aside) is a lead and is not proved here. The violation rates depend on the")
print("  ranges chosen. The Lean file proves the statements about the map; it does not prove the author's Theorems")
print("  5.1-5.3 as printed (one of them is false, and the file proves that). It was compiled in the cloud against")
print("  Lean 4.32.0 / Mathlib v4.32.0; run tools/leancheck.sh --audit book14/SwarmSimulatorV3.lean on the Mac to confirm.")
print("  The V3 deposit that carries it (with the revised paper) was published as version 3.0, doi:10.5281/zenodo.23027566, on 29 September 2026. The Wolfram quotation is checked by eye.")
print(f"\n{len(FAIL)} FAIL" + (": " + ", ".join(FAIL) if FAIL else ""))
sys.exit(1 if FAIL else 0)
