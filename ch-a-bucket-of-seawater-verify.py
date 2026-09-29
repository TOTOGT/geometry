#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""ch-a-bucket-of-seawater-verify.py -- every number on ch-a-bucket-of-seawater.html (Book 3). Run first (R24).
    python3 ch-a-bucket-of-seawater-verify.py
  [1] the bucket: viruses per bucket at the reported density, against the world's population
  [2] the fruit-fly toy model as it behaves (the author's own code, papers/multi-orbit-bioswarm/)
  [3] why the printed contraction could not hold: C jumps, four fixed points at alpha = 0, U fixes the norm
  [4] the link to Book XIV ch 10: fast settling, and the chain law
  [5] the Lean: BioSwarmCheck.lean
  [HONESTY]
"""
import csv, importlib.util, re, sys
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parent
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)

print("[1] the bucket")
per_ml = 10 ** 7            # typical surface seawater, as reported by Suttle (2005, 2007); not held
bucket_l = 10
people = 8.0e9              # world population passed 8 billion in November 2022 (UN)
v = per_ml * bucket_l * 1000
check("a 10-litre bucket at 10^7 viruses per mL holds 10^11 viruses", v == 10 ** 11)
check("that is 12.5 times the world's 8 billion people", abs(v / people - 12.5) < 1e-9, f"{v/people}")
check("even at 10^6 per mL (ten times fewer) the bucket still beats the population", 10 ** 6 * 10 * 1000 > people)

print("[2] the fruit-fly toy model, run from the author's code")
spec = importlib.util.spec_from_file_location("bio", ROOT / "papers/multi-orbit-bioswarm/multi_orbit_bioswarm.py")
bio = importlib.util.module_from_spec(spec); sys.modules["bio"] = bio; spec.loader.exec_module(bio)
import numpy as np
Cc, Kc, Fc, Uc = bio.C_compress, bio.K_clip, bio.F_fold, bio.U_unfold
def G(s, nb, a, b=0.1): return Uc(Fc(Kc(Cc(s), b), nb, a))
def run(N, a, T, seed):
    rng = np.random.default_rng(seed); S = [rng.uniform(-1, 1, 2) for _ in range(N)]; hist = [np.array(S)]
    for _ in range(T):
        S = [G(S[i], S[(i + 1) % N], a) for i in range(N)]; hist.append(np.array(S))
    return hist
def period(h):
    for p in range(1, 40):
        if np.abs(h[-1 - p] - h[-1]).max() < 1e-9: return p
    return None
rows = {}
for a in (0.0, 0.3, 0.41, 0.42, 0.45, 0.5, 0.6, 0.7, 0.9):
    ends = set(); pers = []
    for seed in range(40):
        h = run(8, a, 400, seed); ends.add(tuple(np.round(h[-1].ravel(), 4))); pers.append(period(h))
    rows[a] = (len(ends), Counter(pers))
    print(f"     alpha={a}: {len(ends)} distinct end states; periods {dict(rows[a][1])}")
check("weak coupling (alpha = 0, 0.3): every one of 40 starts settles to a fixed state, and all 40 differ",
      all(rows[a][0] == 40 and rows[a][1] == Counter({1: 40}) for a in (0.0, 0.3)))
check("alpha = 0.41: all 40 runs settle; alpha = 0.42: the first cycles (4 runs, period 24), 27 distinct end states",
      rows[0.41][1] == Counter({1: 40}) and rows[0.42][1].get(24, 0) == 4 and rows[0.42][0] == 27)
check("alpha = 0.45: cycles of period 16", rows[0.45][1].get(16, 0) > 0)
check("alpha = 0.5: most runs cycle (period 16 or 24), fewer than half settle",
      rows[0.5][1].get(1, 0) < 20 and rows[0.5][1].get(16, 0) > 0)
check("alpha >= 0.7: some runs neither settle nor repeat within 400 steps",
      rows[0.7][1].get(None, 0) > 0 and rows[0.9][1].get(None, 0) > 0)

print("[3] why the printed contraction could not hold")
x = np.array([1.0, 0.999]); y = np.array([0.999, 1.0]); nb = np.array([0.6, 0.8])
dx = np.abs(x - y).sum(); dG = np.abs(G(x, nb, 0.3) - G(y, nb, 0.3)).sum()
check("two inputs 0.002 apart go to outputs 1.32 apart at alpha = 0.3 (C jumps)", abs(dx - 0.002) < 1e-12 and abs(dG - 1.3203) < 1e-3, f"{dG:.4f}")
lim = set()
for s0 in [(1, 0), (-1, 0), (0, 1), (0, -1), (0.3, 0.2), (-0.2, 0.9), (0.1, -0.7), (-0.5, -0.4)]:
    s = np.array(s0, float)
    for _ in range(50): s = G(s, s, 0.0)
    lim.add(tuple(np.round(s, 6)))
check("at alpha = 0, where the paper's L(alpha) = 1/2 + |alpha| gives 0.5, one agent has 4 fixed points",
      len(lim) == 4 and all(abs(abs(p[0]) + abs(p[1]) - 1.1 / 1.01 ** 0.5) < 1e-5 for p in lim), str(sorted(lim)))
data = [(float(r["alpha"]), float(r["mean_norm_sq"])) for r in csv.DictReader(open(ROOT / "papers/multi-orbit-bioswarm/pitchfork_scan.csv"))]
vals = [m for _, m in data]
check("the pitchfork figure's data (80 couplings): every value lies in 0.9989-1.0010, a spread of 0.0021",
      len(data) == 80 and min(vals) > 0.9988 and max(vals) < 1.0011 and abs(max(vals) - min(vals) - 0.002144) < 1e-6)
S = run(12, 0.5, 6, 1)[-1]
check("without noise every state has |s|^2 = 1 exactly (U rescales it), so the plotted quantity cannot show a bifurcation",
      np.allclose((S ** 2).sum(1), 1.0, atol=1e-12))

print("[4] the link to Book XIV ch 10")
rat = []
for seed in range(200):
    h = run(8, 0.3, 60, seed); fin = h[-1]
    r0 = np.linalg.norm(h[0] - fin, axis=1).mean(); r6 = np.linalg.norm(h[6] - fin, axis=1).mean()
    rat.append(r6 / r0)
rat = np.array(rat)
check("at alpha = 0.3 six steps close the distance to each run's own end state to under 1.5% (the paper's bound was 27%)",
      rat.max() < 0.015, f"median {np.median(rat):.4f}, max {rat.max():.4f}")
check("going viral: with m = 0.231 (the Swarm Simulator default) a type shrinks to 4.3e-7 of its size in 10 steps; with m = 1.1 it grows 2.59-fold",
      abs(0.231 ** 10 - 4.3e-7) < 0.05e-7 and abs(1.1 ** 10 - 2.5937) < 1e-4, f"{0.231**10:.3e}, {1.1**10:.4f}")
check("the paper's six-step figure (4/5)^6 = 0.262144", abs((4 / 5) ** 6 - 0.262144) < 1e-12)

print("[5] the Lean: BioSwarmCheck.lean")
lean = (ROOT / "BioSwarmCheck.lean").read_text(encoding="utf-8")
rep = (ROOT / "bioswarmcheck.axioms.txt").read_text(encoding="utf-8")
for t in ("C_jumps", "U_norm", "four_fixed_points"):
    check(f"BioSwarmCheck.lean proves {t}, within the permitted three axioms",
          f"theorem {t}" in lean and re.search(rf"BioSwarmCheck\.{t}' depends on axioms: \[propext, Classical\.choice, Quot\.sound\]", rep) is not None)
check("no sorry", "sorry" not in re.sub(r"/-.*?-/|--[^\n]*", "", lean, flags=re.S))
v2 = (ROOT / "papers/multi-orbit-bioswarm/MultiOrbitBioSwarm_v2.lean").read_text(encoding="utf-8")
check("the V2 file defines L(alpha) = 1/2 + |alpha| and never derives it from G", "def lipschitzConst (α : ℝ) : ℝ := 1 / 2 + |α|" in v2)
check("the V2 file's 'obligations' contain no sorry: two conclude True, one uses an identity placeholder",
      "sorry" not in re.sub(r"/-.*?-/|--[^\n]*", "", v2, flags=re.S) and v2.count("True := by") == 2 and "-- identity placeholder" in v2)

print("[HONESTY]")
print("  The virus density (10^7 per mL) is Suttle's reported typical figure; the papers are not held (WANTED).")
print("  The lecture is the author's recollection of V. Racaniello's Columbia virology course (2020); no transcript is")
print("  held. The model is run from the author's own code; the attractor counts depend on N = 8, 40 seeds and 400")
print("  steps, and are a measurement of this toy model, not of any fly. The V2 reference [11] (Bhaskaran et al.,")
print("  J. Theor. Biol. 540, 111077, doi:10.1016/j.jtbi.2022.111077) returned 404 at doi.org on 2026-09-29 and was not")
print("  found by title search; that check needs a network and is not repeated here. BioSwarmCheck.lean was compiled in")
print("  the cloud (Lean 4.32.0 / Mathlib v4.32.0); run tools/leancheck.sh --audit BioSwarmCheck.lean on the Mac.")
print("  Its sgn(0) = +1 matches numpy's sign(s + 1e-12) except on (-1e-12, 0).")
print(f"\n{len(FAIL)} FAIL" + (": " + ", ".join(FAIL) if FAIL else ""))
sys.exit(1 if FAIL else 0)
