#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
ch06c-verify.py -- ch06c-cantor-and-crossing-infinities.html (English for Researchers, outside the weekly plan).
  [1] sections S1..S9 present   [2] every local link resolves
  [3] the mathematics on the page recomputes: N->Z pairing, the diagonal example, 2^n table, no onto map X->P(X) for |X|<=4,
      string counts 3,9,27,81 (120), a listing of all strings by length then order, ages
  [4] the Lean file the page cites states Cantor's theorem and has no `sorry` (text check, NOT a kernel run)
  [5] biographical facts from sources: recorded, SKIP (not machine-checked)
  [6] controls: each check is shown to fail on a broken input (R24)
  [HONESTY] what this does not establish
"""
import re, sys, html as H, itertools
from pathlib import Path
HERE = Path(__file__).resolve().parent
PAGE = HERE / "ch06c-cantor-and-crossing-infinities.html"
fails, skips = [], []
def check(ok, msg, detail=""):
    print("    %s  %s%s" % ("PASS" if ok else "FAIL", msg, ("  -- " + detail) if (detail and not ok) else ""))
    if not ok: fails.append(msg)
def skip(msg): print("    SKIP  " + msg); skips.append(msg)
def head(n, t): print("\n" + "=" * 72 + "\n  [%s]  %s\n" % (n, t) + "=" * 72)
def plain(h):
    h = re.sub(r"<script.*?</script>|<style.*?</style>", "", h, flags=re.S)
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", h)))
N_TABLES = 8
SECS = ["S%d" % i for i in range(1, 10)]
def sections(h): return [x for x in SECS if 'id="%s"' % x in h]
def local_links(h): return [x for x in re.findall(r'href="([^"#]+)"', h) if not re.match(r"https?:|mailto:|/", x)]

def f(n): return (-n - 1) // 2 if n % 2 else n // 2      # the article's pairing, N from 0
def is_bijection_prefix(N):
    vals = [f(n) for n in range(N)]
    return len(set(vals)) == N and set(range(-(N // 2) + (1 if N % 2 == 0 else 0) - (0), 0)) <= set(vals)
def diag(rows):
    return [int(r[i]) for i, r in enumerate(rows)]
def flip(d): return [6 if x == 5 else 5 for x in d]
def differs_everywhere(rows, d): return all(rows[i][i] != str(d[i]) for i in range(len(rows)))
def has_onto(X, target_size_fn):
    """is there a function X -> P(X) onto? brute force. target = subsets of X as bitmasks."""
    n = len(X); P = range(2 ** n)
    for fn in itertools.product(P, repeat=n):
        if set(fn) == set(P): return True
    return False
def onto_identity_exists(n):                              # control: X -> X (not the power set) CAN be onto
    return any(set(fn) == set(range(n)) for fn in itertools.product(range(n), repeat=n))

html = PAGE.read_text(encoding="utf-8"); txt = plain(html)

head(1, "SECTIONS")
check(sections(html) == SECS, "sections S1..S9 all present")
check(len(re.findall(r'<table class="cmp">', html)) == N_TABLES, "%d tables" % N_TABLES)

head(2, "LOCAL LINKS RESOLVE")
ll = local_links(html); miss = [l for l in ll if not (HERE / l).exists()]
check(len(ll) >= 8 and not miss, "%d local links, none missing" % len(ll), ", ".join(miss))

head(3, "THE MATHEMATICS ON THE PAGE, RECOMPUTED")
row = [f(n) for n in range(9)]
check(row == [0, -1, 1, -2, 2, -3, 3, -4, 4], "f(0..8) = 0,-1,1,-2,2,-3,3,-4,4 as in the table", str(row))
check(f(9) == -5 and f(10) == 5 and f(199) == -100, "task 1: f(9) = -5, f(10) = 5, and n = 199 gives -100")
check(len({f(n) for n in range(2001)}) == 2001 and set(range(-1000, 1001)) <= {f(n) for n in range(2001)}, "f is one-to-one on 0..2000 and hits every integer from -1000 to 1000")
rows = ["31415", "27182", "57521", "41421", "14142"]
d = diag(rows); fl = flip(d)
check(d == [3, 7, 5, 2, 2] and fl == [5, 5, 6, 5, 5] and "0.55655" in txt, "diagonal 3,7,5,2,2 -> d = 0.55655, as printed")
check(differs_everywhere(rows, fl), "d differs from each listed number at its own diagonal place")
check(all(x not in (0, 9) for x in fl), "the 5-or-6 rule never produces 0 or 9")
check([2 ** n for n in range(6)] == [1, 2, 4, 8, 16, 32] and all(2 ** n > n for n in range(200)), "2^n table 1,2,4,8,16,32 and 2^n > n for n < 200")
for n in range(0, 5):
    check(not has_onto(range(n), None), "no function from a %d-set onto its power set (brute force over %d functions)" % (n, (2 ** n) ** n))
counts = [3 ** k for k in range(1, 5)]
check(counts == [3, 9, 27, 81] and sum(counts) == 120 and "120" in txt, "strings over 3 parts: 3, 9, 27, 81; total 120 up to length 4")
def listing(alpha, L):
    out = []
    for k in range(1, L + 1): out += ["".join(p) for p in itertools.product(alpha, repeat=k)]
    return out
lst = listing("abc", 5)
check(len(lst) == len(set(lst)) == sum(3 ** k for k in range(1, 6)), "listing by length, then order, gives every string up to length 5 exactly one place (%d strings)" % len(lst))
check(1845 + 44 == 1889 and 1918 - 1845 == 73, "Cantor was 44 when Wittgenstein was born (1889), if born 1845 (year arithmetic only; month ignored)")

head(4, "THE LEAN FILE THE PAGE CITES (text check only)")
lp = HERE / "Orthogenesis/NestedInfinities/EightChecks.lean"
lt = lp.read_text(encoding="utf-8") if lp.exists() else ""
nocomment = re.sub(r"--.*", "", lt)
check("theorem rung_is_strict" in lt and "Cardinal.cantor" in lt, "the file states rung_is_strict (a < 2 ^ a) from Cardinal.cantor")
check(not re.search(r"\bsorry\b", nocomment), "no `sorry` outside comments")
skip("the Lean file was not compiled by this script; a text check is not a kernel check")

head(5, "BIOGRAPHICAL FACTS FROM SOURCES")
for s in ["St Petri-Schule from about age 8 and the timetable (Sinkevich 2018)", "family left in 1856; leave request 4 May 1856 (Sinkevich)",
          "1869 census, 45.5 thousand Germans, <= 7% (Shaidurov & Osipov 2024)", "Acta Math. 2 (1883) French translations; Gerbaldi's Italian; Jourdain 1915 (Grattan-Guinness 1970; MacTutor)"]:
    skip(s + " -- read through a fetch tool on 2026-11-10, not machine-checked")
check("Marotte" in txt and "not confirmed" in txt, "the page states that Marotte's 1899 translation was not confirmed")
check("Jeremy" in txt and "surname" in txt and "licence were not recorded" in txt, "the page names the author as Jeremy and states that his surname, address and licence were not recorded")

head(6, "CONTROLS (each check must be able to fail)")
check(sections(html.replace('id="S5"', 'id="XX"')) != SECS, "control: a missing section is detected")
bad = html.replace('href="ch8-nested-infinities.html"', 'href="no-such-page-ch06c.html"')
check({l for l in local_links(bad) if not (HERE / l).exists()} == {"no-such-page-ch06c.html"}, "control: a broken link is detected")
check(not differs_everywhere(rows, [3, 7, 5, 2, 1]), "control: a 'diagonal' agreeing with r5 at place 5 is rejected")
check(onto_identity_exists(3) and not has_onto(range(3), None), "control: the brute-force search finds an onto map X->X for |X| = 3 but none X->P(X)")
check([(-n - 1) // 2 if n % 2 else n // 2 + 1 for n in range(9)] != row, "control: a wrong pairing gives a different row and is detected")
check(len({(n // 2) for n in range(10)}) != 10, "control: a non-injective rule is detected by the set-size test")
check(re.search(r"\bsorry\b", re.sub(r"--.*", "", "theorem t : True := by sorry")) is not None, "control: a `sorry` in code is detected")

print("\n[HONESTY] This script does not verify any theorem. It recomputes the arithmetic on the page, brute-forces the finite cases of Cantor's theorem (|X| <= 4),")
print("          checks that links resolve, and checks the Lean file's text. The biographical statements come from sources read by a fetch tool and are NOT checked here.")
print("          The proof in Part 4 is the standard one; it is on the page to be read, not verified by this script. Nothing here shows how children acquire language.")
print("\n%s  (%d skipped)" % ("all run checks passed." if not fails else "FAILED: %d" % len(fails), len(skips)))
sys.exit(1 if fails else 0)
