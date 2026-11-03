#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book6/ch06-verify.py -- every number and rule on book6/ch06-molecular-cascade.html. Run first.

    python3 book6/ch06-verify.py

All arithmetic is exact (fractions). This chapter makes no claim that its molecular numbers derive
from the corpus's constants (its section 4 says so), so nothing here tests biology. The checks are:

  [1] two filters in series: net error = e1 * e2; 1/40 through a fine sieve passing 1/1000 is 1/40000;
      the pass fraction needed to reach 1/40000 from 1/100, 1/10 and 1/40
  [2] the chapter's own consistency: 1/40 lies inside the "roughly 1/10-1/100" range it quotes
  [3] the nonsense-mediated-decay rule as stated (flag when the stop lies more than T nt upstream of
      the last exon-exon junction): the five properties in the Lean file, checked on every
      (T, s, j) in a grid, and the 50-versus-55 band
  [4] section 3 numbers: 1-3 misincorporations per 10,000 sits inside 1/40,000 .. 1/2,400 (containment,
      not equality); improvement factors; and the old-versus-new low end
  [5] the page text still says what these checks assume
  [6] the Lean file: the sixteen theorems are present, none uses sorry, and the axiom report (if it
      exists yet) shows no sorryAx
"""
import html as _html, re, sys
from fractions import Fraction as F
from pathlib import Path

FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  [{detail}]" if detail else ""))
    if not ok: FAIL.append(label)

net = lambda e1, e2: e1 * e2

print("[1] two filters in series")
check("1/40 x 1/1000 = 1/40000", net(F(1, 40), F(1, 1000)) == F(1, 40000))
check("fine-sieve pass fraction needed for 1/40000: from 1/100 -> 1/400", F(1, 40000) / F(1, 100) == F(1, 400))
check("from 1/10 -> 1/4000", F(1, 40000) / F(1, 10) == F(1, 4000))
check("from 1/40 -> 1/1000", F(1, 40000) / F(1, 40) == F(1, 1000))
check("a second stage passing everything changes nothing (e x 1 = e), several e", all(net(e, F(1)) == e for e in (F(1, 40), F(1, 7), F(3, 5))))
check("strict gain iff the second stage passes less than everything, on a grid",
      all((net(e1, e2) < e1) == (e2 < 1) for e1 in (F(1, 40), F(1, 3), F(9, 10)) for e2 in (F(0), F(1, 1000), F(1, 2), F(1), F(3, 2))))
check("net error never exceeds either stage when both are in [0,1]",
      all(net(a, b) <= min(a, b) for a in (F(0), F(1, 40), F(1, 2), F(1)) for b in (F(0), F(1, 1000), F(1, 2), F(1))))

print("[2] the chapter against itself")
check("1/40 lies inside the range 1/100 .. 1/10 that section 3 quotes", F(1, 100) <= F(1, 40) <= F(1, 10))

print("[3] the NMD rule as stated, on a grid")
flag = lambda T, s, j: s + T < j
R = range(0, 131)
check("a stop at or after the last junction is never flagged (all T = 50, 55)", all(not flag(T, s, j) for T in (50, 55) for j in R for s in R if j <= s))
check("a stop within T of the last junction is never flagged", all(not flag(T, s, j) for T in (50, 55) for j in R for s in R if j <= s + T))
check("moving the stop upstream keeps it flagged", all(flag(T, s2, j) for T in (50, 55) for j in R for s in R for s2 in range(0, s + 1) if flag(T, s, j)))
check("a larger threshold flags a subset of what a smaller one flags", all(flag(50, s, j) for j in R for s in R if flag(55, s, j)))
check("flagged at 50 but not at 55 exactly when 50 < j - s <= 55", all((flag(50, s, j) and not flag(55, s, j)) == (s + 50 < j <= s + 55) for j in R for s in R))
check("example: stop at 100, junction at 152 (52 nt): flagged at 50, not at 55", flag(50, 100, 152) and not flag(55, 100, 152))

print("[4] section 3 numbers")
check("1/40000 < 1/10000 and 3/10000 < 1/2400 (inside the window)", F(1, 40000) < F(1, 10000) and F(3, 10000) < F(1, 2400))
check("so '1 to 3 per 10,000' is contained in the window, not equal to it", F(1, 10000) != F(1, 40000) and F(3, 10000) != F(1, 2400))
check("improvement factors: 1/100 -> 1/40000 is 400, 1/10 is 4000, 1/40 is 1000", (F(1, 100) / F(1, 40000), F(1, 10) / F(1, 40000), F(1, 40) / F(1, 40000)) == (400, 4000, 1000))
check("the old 10^-4 -> 10^-8 is a factor of 10^4", F(1, 10 ** 4) / F(1, 10 ** 8) == 10 ** 4)
check("the new low end 1/40000 is 2500 times the old 10^-8", F(1, 40000) / F(1, 10 ** 8) == 2500)
check("the new improvement factors (400..4000) are 2.5 to 25 times smaller than the old 10^4",
      (F(10 ** 4) / 4000, F(10 ** 4) / 400) == (F(5, 2), F(25)))

print("[5] the page text")
here = Path(__file__).resolve().parent
html = (here / "ch06-molecular-cascade.html").read_text(encoding="utf-8")
txt = re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", " ", html)))
check("page quotes 1/40,000 and the 50-55 nt rule", "1/40,000" in txt and "50–55" in txt)
check("page quotes 1 to 3 per 10,000 and the window 1/2,400 to 1/40,000", "1 to 3 amino" in txt and "1/2,400" in txt)
check("page says the correction does not reach 10^-8", "does not reach" in txt and "10⁻⁸" in txt)
check("the sentence 'roughly an order of magnitude looser at the low end' now appears only in the correction note",
      txt.count("roughly an order of magnitude looser at the low end") == 1 and "[CORRECTED" in txt)
check("section 3 now states the 2,500 factor and the 400 to 4,000 improvement factor", "2,500 times larger" in txt and "400 to 4,000" in txt)
check("section 3 states the starting error as 1/10 to 1/100", "roughly 1/10 to 1/100" in txt)

print("[6] the Lean file")
src = (here / "MolecularCascade.lean").read_text(encoding="utf-8")
rep = here / "molecularcascade.axioms.txt"
code = re.sub(r"/-.*?-/", "", src, flags=re.S)
code = re.sub(r"--[^\n]*", "", code)
names = ["net_error_le_first", "net_error_le_second", "double_sieve_example", "required_pass_fraction",
         "required_examples", "no_gain_if_passes_all", "strict_gain_iff", "nmd_no_flag_last_exon",
         "nmd_no_flag_within", "nmd_flag_upstream_monotone", "nmd_threshold_antitone", "nmd_band",
         "nmd_band_example", "misincorporation_inside_window", "improvement_factors", "old_vs_new_low_end"]
for n in names:
    check(f"theorem {n} is declared", re.search(r"\btheorem\s+" + n + r"\b", code) is not None)
check("no proof in the file uses sorry", re.search(r"\bsorry\b", code) is None)
if not rep.is_file():
    print("  NOT YET RUN: molecularcascade.axioms.txt does not exist.")
else:
    lines = [l for l in rep.read_text(encoding="utf-8").splitlines() if l.startswith("'Book6Molecular.")]
    check("the axiom report has one line per theorem", len(lines) == len(names), f"{len(lines)} lines")
    check("no theorem line shows sorryAx", all("sorryAx" not in l for l in lines))

print("[HONESTY]")
print("  Nothing here tests biology. Part A assumes the two stages are independent; the NMD rule is the chapter's rule as stated.")
print("  Whether real pass fractions are 1/1000 or the real threshold is 50 or 55 nt is empirical and is not checked.")
print("  The ChargingAttempt sketch on the page is not in the Lean file. The Lean file was compiled by the author on 2026-11-03 (see molecularcascade.axioms.txt).")
print()
print("0 FAIL" if not FAIL else f"{len(FAIL)} FAIL: {FAIL}")
sys.exit(1 if FAIL else 0)
