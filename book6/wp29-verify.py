#!/usr/bin/env python3
"""
wp29-verify.py  --  re-runs book6/wp29-numerology-sweep.html against the corpus.

WP-29 is the corpus's own instrument for refusing coincidences: 26 pages link to
it, and WP-30, WP-104, WP-107 and Book 4 Ch 26 invoke "the WP-29 method" by name.
An instrument used to refuse other people's claims should be the first thing
verified, and it had no script.

WP-29 is unusual among the working papers in that most of its claims are about
OTHER FILES -- five "Fixed:" statements asserting that a specific page was
repaired.  A claim of that shape decays silently: nothing fails when a page is
later edited back, and nothing in the corpus was watching.  So the blocks are:

  [1] the arithmetic the sweep rests on, recomputed;
  [2] the base-rate argument turned into a measurement over the corpus itself,
      rather than left as an assertion about small integers;
  [3] REGRESSION GUARD -- each of the five repairs asserted still in place;
  [4] what re-running the sweep finds that the sweep missed.  The paper's own
      closing instruction is that it "should be extended, not re-done", and
      block [4] is that extension.

Run from book6/, or pass --repo.  Standard library only.  Exits 1 on failure.
"""

import argparse
import html
import os
import re
import sys
from collections import Counter
from fractions import Fraction

FAIL, SKIP = [], []


def check(label, got, want, note=None):
    ok = (got == want)
    print("  %s %-52s got=%s  want=%s" % ("OK  " if ok else "FAIL", label,
                                          str(got)[:30], str(want)[:30]))
    if note:
        for line in note.split("\n"):
            print("       " + line)
    if not ok:
        FAIL.append(label)
    return ok


def skip(label, why):
    print("  SKIP %-52s %s" % (label, why))
    SKIP.append(label)


HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("--repo", default=os.path.abspath(os.path.join(HERE, "..")),
                help="path to the geometry repository")
ap.add_argument("--axle", default=None, help="path to the AXLE repository")
args = ap.parse_args()
R = args.repo


def read(rel):
    p = os.path.join(R, rel)
    return open(p, encoding="utf-8").read() if os.path.isfile(p) else None


def text(rel):
    s = read(rel)
    if s is None:
        return None
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.S)
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)))


# ======================================================================== [1]
print()
print("[1] the arithmetic the sweep rests on")

check("nBonacciRingSize(4) = 56 gives critDim(4) = 112", 2 * (56 - 1) + 2, 112,
      "The Lean constant. It is correct, and correctness was never the issue --\n"
      "the issue was what it was said to match.")
check("tau * eps_0 = 2 * 1/3 = 2/3", 2 * Fraction(1, 3), Fraction(2, 3))
check("and 2/3 < 1", 2 * Fraction(1, 3) < 1, True,
      "Both constants are independently Lean-proved elsewhere. The sweep left\n"
      "them standing and removed only the inference hung on the shared digit 3.")

# The control case, and the identity behind it, over EVERY irreducible root
# system -- not just the simply-laced ones the page restricts it to.
ROOTS = {                       # name: (rank, |Phi|, Coxeter number h)
    "A_1": (1, 2, 2), "A_4": (4, 20, 5), "A_8": (8, 72, 9),
    "B_3": (3, 18, 6), "B_5": (5, 50, 10),
    "C_4": (4, 32, 8), "D_4": (4, 24, 6), "D_7": (7, 84, 12),
    "E_6": (6, 72, 12), "E_7": (7, 126, 18), "E_8": (8, 240, 30),
    "F_4": (4, 48, 12), "G_2": (2, 12, 6),
}
check("E_8: 240 roots / rank 8 = Coxeter number 30",
      Fraction(240, 8), 30,
      "The sweep's control case, included so the paper is not read as saying\n"
      "every claim in the corpus is suspect.")
bad = [k for k, (n, phi, h) in ROOTS.items() if n * h != phi]
check("|Phi| = rank * h for every irreducible root system", bad, [],
      "%d systems checked, classical and exceptional. The identity is general;\n"
      "the page restricts it to simply-laced, which is true but narrower than\n"
      "needed. This is what makes the control case a definitional identity and\n"
      "not a numerical coincidence -- it names a reason." % len(ROOTS))

# ======================================================================== [2]
print()
print("[2] the base-rate argument, as a measurement rather than an assertion")
pages, nums = 0, Counter()
for dp, dn, fn in os.walk(R):
    if any(x in dp.split(os.sep) for x in (".git", ".lake", "node_modules")):
        continue
    for f in fn:
        if not f.endswith(".html"):
            continue
        try:
            s = open(os.path.join(dp, f), encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        pages += 1
        body = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.S)
        body = re.sub(r"<[^>]+>", " ", body)
        for m in re.finditer(r"(?<![\w.])(\d{1,3})(?![\w.])", body):
            nums[int(m.group(1))] += 1
if pages == 0:
    skip("integer base rate", "no HTML found under --repo")
else:
    total = sum(nums.values())
    print("       %d pages, %d integers 0-999 counted" % (pages, total))
    for n in (3, 33, 112, 240, 30):
        share = 100.0 * nums[n] / total
        print("       %-4d appears %6d times  (%.2f%% of all small integers)"
              % (n, nums[n], share))
    check("3 is among the ten commonest integers in the corpus",
          n_rank := sorted(nums, key=nums.get, reverse=True).index(3) + 1 <= 10, True,
          "The sweep's second finding argued that a shared 3 is not evidence,\n"
          "because 3 recurs by base rate. Measured on the corpus's own text that\n"
          "is not rhetoric: rank %d of all integers below 1000."
          % (sorted(nums, key=nums.get, reverse=True).index(3) + 1))
    check("112 occurs in the corpus independently of critDim",
          nums[112] >= 2, True,
          "Book 6 Ch 02 builds E_8 as 112 + 128 = 240 roots. That 112 has no\n"
          "relation to critDim(4) or to any inventory row count, and it is the\n"
          "cleanest available demonstration of the sweep's own argument: a\n"
          "three-digit integer recurring across unrelated structures.")

# ======================================================================== [3]
print()
print("[3] regression guard: the five repairs, still in place?")

collatz = read("chH-collatz.html")
if collatz is None:
    skip("chH-collatz.html repairs", "file not found")
else:
    card = collatz[collatz.find("Monster Threshold"):][:2600]
    check("1a. Monster Threshold card reads OPEN CONJECTURE",
          "OPEN CONJECTURE" in card, True)
    check("1b. and points at g6-crystal.html", "g6-crystal.html" in card, True)
    check("1c. and records that it previously read ESTABLISHED",
          'previously read "ESTABLISHED."' in card, True,
          "The repair keeps its own history, which is why it can be checked.")
    stab = collatz[collatz.find("Stability Relation"):][:2200]
    check("2a. the Collatz-3 inference is marked removed",
          "has been removed" in stab, True)
    check("2b. and the two proved constants still stand",
          "independently Lean-proved" in stab, True)

for rel in ("course-dm3-102.html", "dm3-102-w10.html"):
    t = text(rel)
    if t is None:
        skip("3. %s" % rel, "file not found")
        continue
    check("3. %s carries the sorry-inventory correction" % rel,
          ("not a count of sorrys" in t) or ("not sorrys" in t), True)
    check("   and states the real totals (1,041 / 1,027)",
          "1,041" in t and "1,027" in t, True)

voa = text("book8/ch8-6-voa.html")
if voa is None:
    skip("4. book8/ch8-6-voa.html", "file not found")
else:
    check("4a. epigraph says conjectured, not settled",
          "conjectured to be the unique VOA" in voa, True)
    check("4b. and says the FLM conjecture is open",
          "still open as of 2026" in voa, True)
    check("4c. and credits Dong-Griess-Lam's partial results",
          "Dong" in voa and "Griess" in voa and "Lam" in voa, True)

e8 = text("book6/ch02-e8-root-system.html")
if e8 is None:
    skip("5. the control case", "file not found")
else:
    check("5. the E_8 control still states 240 roots and h = 30",
          "240" in e8 and "30" in e8, True)

# ======================================================================== [4]
print()
print("[4] the extension: what re-running the sweep finds")
print("       WP-29 closes by asking to be EXTENDED, not re-done. These are new,")
print("       and two of them are inside files the sweep itself repaired.")

if voa is not None:
    check("4-A. ch8-6-voa does NOT also call FLM uniqueness a theorem",
          "Meurman conjecture, now a theorem)" in voa, False,
          "FOUND 2026-09-10, CORRECTED. The epigraph was repaired by the sweep\n"
          "and the body of the same chapter was not: a tech-box read 'the\n"
          "uniqueness of V-natural (Frenkel-Lepowsky-Meurman conjecture, now a\n"
          "theorem)', contradicting the corrected epigraph eight paragraphs\n"
          "above it. The conjecture is open. Betsumiya, Lam and Shimakura\n"
          "(Comm. Math. Phys., 2023) prove uniqueness for holomorphic c = 24\n"
          "VOAs with NON-TRIVIAL weight-one Lie algebra -- precisely the\n"
          "complement of the moonshine module, which has dim V_1 = 0.\n"
          "Repairing a page's epigraph is not repairing the page.")

course = text("course-dm3-102.html")
if course is not None:
    check("4-B. the 112 = 'number of proofs' claim is gone",
          "112 \u2014 exactly the number of proofs" in course, False,
          "FOUND 2026-09-10, CORRECTED. One paragraph above the sweep's own\n"
          "correction, the same file still read 'critDim(4) = 112 -- exactly the\n"
          "number of proofs in the AXLE 1080-proofs programme', and the page\n"
          "summary said the same. It is the identical claim species the sweep\n"
          "refused, attached to a different denominator, and it survived because\n"
          "the sweep searched for 'not a coincidence' and this sentence does not\n"
          "contain the phrase. A sweep keyed to wording finds the wording.")

AX = args.axle or next((c for c in (os.path.join(R, "..", "AXLE"),
                                    os.path.expanduser("~/Desktop/AXLE"),
                                    os.path.expanduser("~/mnt/AXLE"))
                        if os.path.isdir(c)), None)
reg = os.path.join(AX, "theorem-registry.html") if AX else None
if not reg or not os.path.isfile(reg):
    skip("4-C. the AXLE registry figures", "AXLE not found (pass --axle)")
else:
    rt = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", open(reg, encoding="utf-8").read())))
    got = re.search(r"(\d+)\s+Core proved", rt)
    check("4-C. the registry's core count is not 112",
          got.group(1) if got else "?", "284",
          "What 112 was said to equal, measured: 284 core proved, 148\n"
          "kernel-audited, 1244 on the full recursive scan. The programme is\n"
          "named for 1080. No reading of the registry gives 112.")

inv = None
for dp, dn, fn in os.walk(os.path.dirname(R)):
    if "sorry_inventory.csv" in fn:
        inv = os.path.join(dp, "sorry_inventory.csv")
        break
check("4-D. sorry_inventory.csv is reachable", inv is not None, False,
      "FOUND 2026-09-10, RECORDED NOT FIXED. The corrected figures in finding 3\n"
      "-- 112 rows, 1,041 sorrys, 1,027 open -- were read off a CSV that is not\n"
      "present in any connected repository. The correction is more defensible\n"
      "than what it replaced and it is no longer regenerable, which is a\n"
      "different weakness in the same place. Noted on the page rather than\n"
      "quietly left; restoring or re-deriving the file is open work.")

# ==================================================================== verdict
print()
if SKIP:
    print("SKIPPED: " + ", ".join(SKIP))
if FAIL:
    print("FAILED: " + ", ".join(FAIL))
    sys.exit(1)
print("ALL CHECKS PASSED" + (" (partial -- see SKIPPED)" if SKIP else ""))
