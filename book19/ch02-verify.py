#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book19/ch02-verify.py -- every number on book19/ch02-the-idioms-axle-reinvented.html. Run first (R24).
    python3 book19/ch02-verify.py [--downloads DIR]
  [1] the tactic census: how often each tactic OPENS a line of Lean, in this repository's
      tracked .lean files and in the code of Mathematics in Lean (v4.19.0, 214 pp)
  [2] tactics MIL teaches that the corpus never uses, and the reverse
  [3] the three native_decide and the sorry lines: where they are, and whether any
      is in a file a build target compiles
  [HONESTY]
"""
import os, re, subprocess, sys
from collections import Counter
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
TACS = ["have","rw","simp","norm_num","linarith","exact","unfold","intro","omega","ring","rfl","nlinarith","decide",
        "constructor","show","refine","obtain","rintro","positivity","rcases","field_simp","apply","subst",
        "linear_combination","calc","induction","funext","cases","push_cast","ext","gcongr","use","by_contra",
        "push_neg","contrapose","convert","specialize","exact?","apply?","tauto","abel","norm_cast","bound",
        "sorry","native_decide","aesop","congr","interval_cases","exfalso","ring_nf","set","norm_num at"]
LEAD = re.compile(r"^\s*(?:·\s*|<;>\s*|\|\s*)?([a-z_?]+)")
def census(text):
    c = Counter()
    for line in text.splitlines():
        m = LEAD.match(line)
        if m and m.group(1) in TACS: c[m.group(1)] += 1
    return c

print("[1] the census")
files = [f for f in subprocess.run(["git", "--no-optional-locks", "-C", str(ROOT), "ls-files", "*.lean"],
         capture_output=True, text=True).stdout.split() if ".lake" not in f]
src = {}
for f in files:
    t = (ROOT / f).read_text(encoding="utf-8", errors="ignore")
    t = re.sub(r"/-.*?-/", "", t, flags=re.S); t = re.sub(r"--[^\n]*", "", t)
    src[f] = t
C = census("\n".join(src.values()))
mil = subprocess.run(["pdftotext", "-layout", str(DL / "mathematics_in_lean.pdf"), "-"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True).stdout
M = census(mil)
print(f"     {len(files)} tracked .lean files; line-opening tactics: corpus {sum(C.values()):,}, MIL {sum(M.values()):,}")
tc, tm = sum(C.values()), sum(M.values())
for t in sorted(set(C) | set(M), key=lambda t: -(C[t] + M[t])):
    print(f"     {t:18} corpus {C[t]:5} ({100*C[t]/tc:5.1f}%)   MIL {M[t]:4} ({100*M[t]/tm:5.1f}%)")
check("110 tracked .lean files outside .lake", len(files) == 110, str(len(files)))

print("[2] the gaps")
never_used = sorted(t for t in M if M[t] >= 5 and C[t] == 0)
never_taught = sorted(t for t in C if C[t] >= 5 and M[t] == 0)
print("     MIL opens >= 5 lines with, corpus never:", never_used)
print("     corpus opens >= 5 lines with, MIL never:", never_taught)
share = lambda X, ts: sum(X[t] for t in ts) / sum(X.values())
auto = ["norm_num", "linarith", "nlinarith", "omega", "decide", "positivity", "simp"]
print(f"     share of lines opened by a decision procedure ({', '.join(auto)}): corpus {100*share(C, auto):.1f}%, MIL {100*share(M, auto):.1f}%")
check("the corpus leans on decision procedures more than MIL does", share(C, auto) > share(M, auto))

print("[3] native_decide and sorry")
nd = [f for f, t in src.items() if re.search(r"\bnative_decide\b", t)]
so = [f for f, t in src.items() if re.search(r"(?<![\w])sorry(?![\w])", t)]
print("     native_decide in:", nd)
print("     sorry in:", so)
lake = (ROOT / "lakefile.lean").read_text(encoding="utf-8")
check("native_decide appears only in CollatzDescent.lean, which no lean_lib declares", nd == ["CollatzDescent.lean"] and "lean_lib CollatzDescent" not in lake)
ml = (ROOT / "Orthogenesis/Architecture/MagneticLattice.lean").read_text(encoding="utf-8")
gw = (ROOT / "AMonster/GenerativeWeave.lean").read_text(encoding="utf-8")
check("the sorry in MagneticLattice (a default target) is disclosed in its own header", "left as an explicit `sorry`" in ml)
check("the sorry in GenerativeWeave is disclosed at the line", "The sorry below marks exactly this gap" in gw)

print("""
[HONESTY]
The census counts lines that OPEN with a tactic name (after indentation, a bullet, <;> or |),
in both sources, so English uses of 'use' or 'show' in MIL's prose are not counted. It
still counts tactic names inside MIL's exercises, which are Lean too. MIL is a teaching
text and this corpus is research code; different shares are expected and are not by
themselves defects. [3] lists files; whether a listed file is compiled by a build target
is read by eye against lakefile.lean on the page, not decided here.
""")
print(f"{len(FAIL)} FAIL")
sys.exit(1 if FAIL else 0)
