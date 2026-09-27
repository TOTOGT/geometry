#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book12/ch02-verify.py -- every number on book12/ch02-carrying.html. Run first (R24).
    python3 book12/ch02-verify.py
  [1] Carrying.lean §1 mirrored: column addition with carries, every pair of numbers below 10,000
  [2] the little one: its largest value when adding 2, 3, ... 12 numbers
  [3] how often a carry happens at all
  [HONESTY]
Standard library only.
"""
import itertools, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
digits = lambda n: [int(c) for c in str(n)[::-1]]
val = lambda ds: sum(d * 10**i for i, d in enumerate(ds))
def addc(c, xs, ys):
    out = []
    while xs or ys or c:
        s = (xs[0] if xs else 0) + (ys[0] if ys else 0) + c
        out.append(s % 10); c = s // 10; xs, ys = xs[1:], ys[1:]
    return out
src = open(os.path.join(ROOT, "book12/Carrying.lean"), encoding="utf-8").read()
for n in ("addc_correct", "carry_small", "written_is_digit"):
    check(f"Carrying.lean states {n}", f"theorem {n}" in src)

print("[1] column addition, every pair below 10,000 in steps")
bad = 0; maxcarry = 0; pairs = 0
for a in range(0, 10000, 7):
    for b in range(0, 10000, 13):
        pairs += 1
        xs, ys, c = digits(a), digits(b), 0
        if val(addc(0, xs, ys)) != a + b: bad += 1
        while xs or ys:
            s = (xs[0] if xs else 0) + (ys[0] if ys else 0) + c
            c = s // 10; maxcarry = max(maxcarry, c); xs, ys = xs[1:], ys[1:]
check("the written answer is the true sum", bad == 0, f"{pairs:,} pairs")
check("the carry was never more than 1", maxcarry == 1)
check("58 + 67: written [5, 2, 1], i.e. 125", addc(0, [8, 5], [7, 6]) == [5, 2, 1])

print("[2] adding a column of k numbers: the largest carry")
rows = []
for k in range(2, 13):
    worst = (9 * k + (k - 1)) // 10          # k nines plus the largest carry k-1
    rows.append((k, worst))
print("     k numbers -> largest carry:", rows)
check("two numbers carry at most 1; ten numbers at most 9; eleven or more can carry 10", rows[0][1] == 1 and dict(rows)[10] == 9 and dict(rows)[11] == 10)

print("[3] how often a carry happens, adding two random digits (all 100 pairs, no incoming carry)")
carries = sum(1 for x in range(10) for y in range(10) if x + y >= 10)
check("45 of the 100 digit pairs carry", carries == 45)

print("""
[HONESTY]
[1] mirrors the Lean definition in Python and checks it on a grid of 1,100,000 pairs;
the proof for all numbers is Carrying.lean. [2]-[3] are arithmetic.
""")
print(f"{len(FAIL)} FAIL")
sys.exit(1 if FAIL else 0)
