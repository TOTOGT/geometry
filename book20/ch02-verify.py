#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book20/ch02-verify.py -- every number on book20/ch02-many-tries-one-winner.html.
Run before the page was written (R24). The two cases were named on book20/index.html
before this script existed; the observable for each was fixed there too: how many
constants and combinations were available to match, and the chance of a match at the
stated tolerance if nothing but that search were at work.

    python3 book20/ch02-verify.py [--downloads DIR]

  [1] Evans & Rosenthal Example 9.3.1: 1 - 0.95^n, and the text's own figures
  [2] case A, g6_equals_schumann: what the theorem checks; the search space; the chance
  [3] case A, propagation: which distributed pages still print it
  [4] case B, the 666-page limit: how many limits could have been read as resonant
  [HONESTY]
"""
import os, re, subprocess, sys
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
ER = "Probability and Statistics- The Science of Uncertainty.pdf"

print("[1] Evans & Rosenthal, Example 9.3.1 (pp. 509-510)")
for n, printed in ((10, .40), (20, .64), (100, .99)):
    v = 1 - .95 ** n
    check(f"n = {n}: 1 - 0.95^n = {v:.3f}, text prints {printed}", round(v, 2) == printed)
try:
    t = subprocess.run(["pdftotext", "-layout", str(DL / ER), "-"], capture_output=True, text=True, timeout=120).stdout.split("\f")
    p = t[522] + t[523]
    check("section 9.3 is on pdf page 523 = printed 509", "9.3 The Problem with Multiple Checks" in t[522])
    check("the cure is stated: decide on the checks before observing the data", "before actually observing the data" in p)
except Exception as e:
    print("SKIP E&R text", e)

print("[2] case A: g6_equals_schumann")
g = [int(x) for x in re.findall(r"\|\s*\.g\d+\s*=>\s*(\d+)", (ROOT / "Orthogenesis/Taxonomy/GSeries.lean").read_text())]
check("the g-series is {0, 2, 6, 33, 64}", g == [0, 2, 6, 33, 64], str(g))
page = (ROOT / "book5/chV-constants.html").read_text(encoding="utf-8")
plain = re.sub(r"<[^>]+>", "", page)
check("book5/chV-constants.html prints the theorem as := rfl", re.search(r"theorem g6_equals_schumann :\s*g6_layer_count = schumann_4th_harmonic_integer := rfl", plain) is not None)
m = re.search(r"f_4 \\approx 33\{,\}8", page)
check("the page's own target: f4 ~ 33.8 Hz, matched to its integer part 33", bool(m))
led = (ROOT / "docs/audit-log.md").read_text(encoding="utf-8")
check("the ledger: both sides are definitions equal to 33 (33 = 33)", "It is `33 = 33`" in led)
f4, bins = 33.8, 34            # modes f1..f4 lie at or below f4; integer bins 1..34
k = 4                          # "fourth" harmonic: at least four modes were on offer
hits = [x for x in g if 1 <= x <= bins]
p1 = len(hits) / bins
pk = 1 - (1 - p1) ** k
print(f"     g-series values with an integer bin at or below f4: {hits}")
print(f"     one mode, uniform over the {bins} bins: P(match) = {len(hits)}/{bins} = {p1:.3f}")
print(f"     any of {k} modes:                     P(match) = {pk:.3f}")
check("chance of some g-value matching some mode's integer part is about 1 in 3", 0.28 < pk < 0.34, f"{pk:.3f}")
lean = (ROOT / "Orthogenesis/Architecture/G6Crystal.lean").read_text()
check("G6Crystal.lean §4 records the withdrawal, 2026-09-11", "WITHDRAWN 2026-09-11" in lean)

print("[3] case A: did the withdrawal reach the pages a reader sees?")
G = ["git", "--no-optional-locks", "-C", str(ROOT)]
files = subprocess.run(G + ["grep", "-l", "g6_equals_schumann"], capture_output=True, text=True).stdout.split()
pub = [f for f in files if f.endswith(".html") and not f.startswith("docs/") and not f.startswith("book20/")]
print(f"     tracked files naming it: {len(files)}; published chapter pages among them: {pub}")
for f in pub:
    s = (ROOT / f).read_text(encoding="utf-8")
    flagged = "po-correction-ch20-02" in s
    check(f"{f} carries a correction pointing here", flagged)

print("[4] case B: the hardback's 666-page limit")
cm = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
check("CLAUDE.md: 666 is the printer's limit for this edition", "printer's limit for this edition" in cm)
check("CLAUDE.md keeps the retired 'resonant' gloss on record as history", "666 = 6 × 111,\nresonant" in cm or "666 = 6 × 111, resonant" in cm)
rep = [int(str(d) * w) for w in (2, 3) for d in range(1, 10)]          # 11..99, 111..999
gs = [2, 6, 33, 64]
lo, hi = 400, 800
readable = sorted({s * r for s in gs for r in rep if lo <= s * r <= hi} | {r for r in rep if lo <= r <= hi})
print(f"     page limits in [{lo},{hi}] writable as (g-value x repdigit) or a repdigit: {len(readable)}")
print(f"     {readable}")
print(f"     share of limits in that range: {len(readable)}/{hi-lo+1} = {len(readable)/(hi-lo+1):.3f}")
check("666 is among them", 666 in readable)
check("other editions can change it", "other editions" in cm)

print("""
[HONESTY]
[1] recomputes a textbook formula. [2] assumes each mode's integer part is equally
likely to be any of 1..34; that is a model of 'nothing but the search at work', chosen
before running, and the Schumann frequencies themselves are not held -- the only
physical value used is the one the page prints. The number k = 4 is read off the word
'fourth'; with more modes on offer the chance only rises. [4]'s families (the g-series,
repdigits) are the ones the corpus itself invokes; a reader with other favourite
numbers would find more. Neither case is judged true or false here: [2] shows the
theorem checks 33 = 33, and [4] shows a printer's limit that was later given a meaning.
""")
print(f"{len(FAIL)} FAIL")
sys.exit(1 if FAIL else 0)
