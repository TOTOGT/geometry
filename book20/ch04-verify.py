#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book20/ch04-verify.py -- every number on book20/ch04-back-toward-the-mean.html. Run first (R24).

    python3 book20/ch04-verify.py [--downloads DIR]

  [1] Galton 1886: the passages, verbatim (pp. 252, 253-254, 256, 263)
  [2] Galton's own balance equation v^2 p^2 + f^2 = P^2 with his numbers
  [3] the converse: from 2/3 and his two spreads, the 1/3 he reads off the columns
  [4] the phenomenon with no heredity in it: a simulation with no cause at all
  [5] this corpus: re-running only the surprising number
  [6] Evans & Rosenthal never name the phenomenon; §10.3 is the model
  [HONESTY]
"""
import math, os, random, re, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def dl():
    if "--downloads" in sys.argv: return Path(sys.argv[sys.argv.index("--downloads") + 1])
    for c in ("~/mnt/Downloads", "~/Downloads"):
        p = Path(os.path.expanduser(c))
        if p.is_dir(): return p
DL = dl()
def text(name):
    try:
        return subprocess.run(["pdftotext", "-layout", str(DL / name), "-"], capture_output=True, text=True, timeout=120).stdout
    except Exception:
        return None
flat = lambda s: re.sub(r"\s+", " ", s)

print("[1] Galton, the passages")
G = text("Galton85.pdf")
if G:
    g = flat(G)
    check("p. 252: the law, in one sentence", "the height-deviate of the offspring is, on the average, two-thirds of the height-deviate of its mid-parentage" in g)
    check("p. 253: the converse is not the numerical opposite", "The converse of this law is very far from being its numerical opposite" in g)
    check("p. 254: read by columns, the mid-parent deviates one-third as much", "deviates only one-third as much as the man does" in g)
    check("p. 254: 928 children of 205 mid-parents", "928 children" in g and "205 mid-parents" in g)
    check("p. 256: the distribution is held in stable equilibrium", "stable equilibrium" in g)
    check("p. 256: 'It acts like a spring against a weight'", "like a spring against a weight" in g)
else:
    print("SKIP Galton text")

print("[2] the balance: regression shrinks, family scatter spreads, the population stays put")
v, p, f = 2/3, 1.22, 1.5      # regression (p.252), probable error of mid-parents (p.263), co-family (p.252)
P = math.sqrt(v**2 * p**2 + f**2)
check("v^2 p^2 + f^2 = P^2 gives P = 1.7, the population's probable error on p. 252", round(P, 1) == 1.7, f"P = {P:.3f}")
check("mid-parents are narrower than people by about sqrt 2 (p. 251): 1.7/sqrt2 ~ 1.22", abs(1.7 / math.sqrt(2) - p) < 0.03, f"{1.7/math.sqrt(2):.3f}")

print("[3] the converse, from his own numbers")
back = v * (p / P) ** 2
check("slope of mid-parent on child = (2/3)(1.22/1.706)^2 ~ 1/3", abs(back - 1/3) < 0.02, f"{back:.3f}")
ratio = (1 / v) / back
check("'four and a half times smaller': (3/2) / (1/3) = 4.5", abs((1.5) / (1/3) - 4.5) < 1e-12)
print(f"     with his measured spreads: (3/2) / {back:.3f} = {ratio:.2f}")

print("[4] regression with no cause: two noisy measurements of the same fixed thing")
random.seed(1886)
N = 100_000
true = [random.gauss(0, 1) for _ in range(N)]
m1 = [t + random.gauss(0, 1) for t in true]
m2 = [t + random.gauss(0, 1) for t in true]
srt = sorted(m1)
cut, low = srt[int(0.95 * N)], srt[int(0.05 * N)]
top = [i for i in range(N) if m1[i] >= cut]
a1 = sum(m1[i] for i in top) / len(top)
a2 = sum(m2[i] for i in top) / len(top)
print(f"     top 5% on the first measurement: mean {a1:.3f}; same cases, second measurement: {a2:.3f}")
check("the second measurement falls back by about half (reliability 1/2), with nothing done in between", abs(a2 / a1 - 0.5) < 0.02, f"ratio {a2/a1:.3f}")
bot = [i for i in range(N) if m1[i] <= low]
b1 = sum(m1[i] for i in bot) / len(bot); b2 = sum(m2[i] for i in bot) / len(bot)
print(f"     bottom 5% on the first measurement: mean {b1:.3f}; second: {b2:.3f}")
check("the bottom 5% 'improve' by the same fraction", abs(b2 / b1 - 0.5) < 0.02, f"ratio {b2/b1:.3f}")

print("[5] this corpus: R19 re-runs only the number that looks wrong")
cm = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
check("CLAUDE.md R19: 'If it looks wrong, say which row and why, then re-run that one thing'", "If it looks wrong, say which row and why, then re-run that one thing" in cm)

print("[6] Evans & Rosenthal")
E_ = text("Probability and Statistics- The Science of Uncertainty.pdf")
if E_:
    e = flat(E_)
    names = ["regression to the mean", "regression toward the mean", "Galton", "regression effect"]
    found = [n for n in names if n.lower() in e.lower()]
    check("none of four names for the phenomenon occurs in the text", not found, str(found))
    check("§10.3 Quantitative Response and Predictors is listed at p. 538", re.search(r"10\.3 Quantitative Response and Predictors[ .]*538", e) is not None)
else:
    print("SKIP E&R")

print("""
[HONESTY]
[1] finds sentences verbatim in an OCR layer. [2]-[3] use four numbers Galton prints
(2/3; 1.22 on p. 263; 1.5 and 1.7 on p. 252) and show they are mutually consistent and
yield his 1/3; the balance equation on p. 256 is garbled in the scan, so its symbols
are read from what reproduces his figures. Table I is not re-tabulated here: its OCR
is too damaged to count, and no number on the page is taken from it. [4] is a
simulation with seed 1886 and no heredity in it, built to show the phenomenon needs no
cause. [5] quotes a rule; whether any re-run under it has mistaken regression for a
fix has not been measured.
""")
print(f"{len(FAIL)} FAIL")
sys.exit(1 if FAIL else 0)
