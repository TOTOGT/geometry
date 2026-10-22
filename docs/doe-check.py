#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
docs/doe-check.py -- checks a design matrix returned by ANOTHER model (e.g. Gemini) before anyone uses it.
    python3 docs/doe-check.py design.csv [--runs N] [--centres N] [--strength2]
    python3 docs/doe-check.py --selftest
The matrix is a CSV with a header row of factor names and coded levels -1,0,1. It checks what a matrix can be checked for:
  [1] shape and levels: every cell in {-1,0,1}; no blank rows; no duplicate rows except centre runs
  [2] run count and centre count equal what the answer CLAIMS (--runs, --centres)
  [3] balance: each factor uses each of its levels equally often, excluding centre rows
  [4] strength-2 orthogonality (--strength2): for every pair of columns, each of the 9 level pairs occurs equally often,
      excluding centre rows. This is what 'orthogonal main effects' means for a 3-level array.
It does NOT check resolution or aliasing claims in prose, power, or that levels are physically sensible.
Hand-derivable example (selftest): 27 runs from three free columns a,b,c over GF(3) and columns a, b, c, a+b, a+2b (mod 3)
(levels 0,1,2 mapped to -1,0,1). Any two of these linear forms are independent, so every pair is a strength-2 array;
the matrix has 27 runs, 9 occurrences of each level per column, and 3 of each level pair.
"""
import csv, io, sys, itertools
from collections import Counter

def load(text):
    rows = [r for r in csv.reader(io.StringIO(text.strip())) if r]
    head, data = rows[0], rows[1:]
    return head, [[int(x) for x in r] for r in data]

def check(head, data, runs=None, centres=None, strength2=False):
    out = []
    ok = lambda name, good, detail="": out.append((name, bool(good), detail))
    k = len(head)
    ok("every row has one cell per factor", all(len(r) == k for r in data))
    if not all(len(r) == k for r in data): return out
    ok("levels are all in {-1,0,1}", all(x in (-1, 0, 1) for r in data for x in r))
    cen = [r for r in data if all(x == 0 for x in r)]
    non = [r for r in data if not all(x == 0 for x in r)]
    dup = [t for t, c in Counter(map(tuple, non)).items() if c > 1]
    ok("no duplicate non-centre runs", not dup, str(dup[:2]))
    if runs is not None: ok("run count equals the claimed %d" % runs, len(data) == runs, "got %d" % len(data))
    if centres is not None: ok("centre count equals the claimed %d" % centres, len(cen) == centres, "got %d" % len(cen))
    for j, name in enumerate(head):
        c = Counter(r[j] for r in non)
        ok("balance of %s over non-centre runs" % name, len(set(c.values())) == 1 and len(c) >= 2, str(dict(c)))
    if strength2:
        for a, b in itertools.combinations(range(k), 2):
            c = Counter((r[a], r[b]) for r in non)
            levels = sorted({r[a] for r in non}), sorted({r[b] for r in non})
            full = len(c) == len(levels[0]) * len(levels[1]) and len(set(c.values())) == 1
            ok("pair %s,%s: every level pair equally often" % (head[a], head[b]), full, str(dict(c)))
    return out

def selftest_matrix():
    rows = []
    for a, b, c in itertools.product(range(3), repeat=3):
        cols = [a, b, c, (a + b) % 3, (a + 2 * b) % 3]
        rows.append([x - 1 for x in cols])
    return ["T", "WHSV", "PEtOH", "SiAl", "Water"], rows

def selftest():
    head, data = selftest_matrix()
    good = check(head, data, runs=27, centres=0, strength2=True)
    allok = all(g for _, g, _ in good)
    print(("PASS " if allok else "FAIL ") + "reference 27-run matrix passes all checks (%d checks)" % len(good))
    bad = []
    d1 = [r[:] for r in data]; d1[0][0] = 5
    bad.append(("a level outside {-1,0,1}", check(head, d1, runs=27, centres=0, strength2=True)))
    d2 = [r[:] for r in data]; d2[1] = d2[0][:]
    bad.append(("a duplicated run", check(head, d2, runs=27, centres=0, strength2=True)))
    d3 = [r[:] for r in data]; assert d3[0][3] != d3[9][3]; d3[0][3], d3[9][3] = d3[9][3], d3[0][3]
    bad.append(("two cells swapped (breaks pair structure)", check(head, d3, runs=27, centres=0, strength2=True)))
    bad.append(("wrong claimed run count", check(head, data, runs=28, centres=0, strength2=True)))
    d5 = [r[:] for r in data[:-1]]
    bad.append(("a run deleted", check(head, d5, runs=27, centres=0, strength2=True)))
    fails = 0
    for name, res in bad:
        rejected = not all(g for _, g, _ in res)
        print(("PASS " if rejected else "FAIL ") + "control rejected: " + name)
        fails += (not rejected)
    return 0 if allok and not fails else 1

if __name__ == "__main__":
    args = sys.argv[1:]
    if "--selftest" in args: sys.exit(selftest())
    if not args: print(__doc__); sys.exit(2)
    def opt(n):
        return int(args[args.index(n) + 1]) if n in args else None
    head, data = load(open(args[0]).read())
    res = check(head, data, opt("--runs"), opt("--centres"), "--strength2" in args)
    for n, g, d in res: print(("PASS " if g else "FAIL ") + n + (("  -- " + d) if (d and not g) else ""))
    print("[HONESTY] Resolution, aliasing, power and physical sense of levels are NOT checked.")
    sys.exit(0 if all(g for _, g, _ in res) else 1)
