#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book12/ch03-verify.py -- every number on book12/ch03-division.html. Run first (R24).
    python3 book12/ch03-verify.py
  [1] Carrying.lean §2: (quotient, remainder) unique, by brute force
  [2] §3: long division's running remainder ends at the true remainder, all divisors 1..30
  [3] casting out nines, and what it cannot see: a swap of two digits
  [HONESTY]
Standard library only.
"""
import os, random, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
src = open(os.path.join(ROOT, "book12/Carrying.lean"), encoding="utf-8").read()
for n in ("quot_rem_unique", "remH_correct", "nines"):
    check(f"Carrying.lean states {n}", f"theorem {n}" in src)

print("[1] one quotient, one remainder")
ok = all(len([(q, r) for q in range(n + 1) for r in range(b) if b * q + r == n]) == 1 for b in range(1, 13) for n in range(200))
check("for every n < 200 and b = 1..12, exactly one pair (q, r) with r < b", ok)
print("     17 shared among 5: 3 each, 2 left over -- 5*3 + 2 = 17")

print("[2] long division's running remainder")
def remH(d, n):
    r = 0
    for ch in str(n): r = (10 * r + int(ch)) % d
    return r
check("equals n % d for every n < 20,000 and d = 1..30", all(remH(d, n) == n % d for d in range(1, 31) for n in range(20000)))
print(f"     2026 on division by 7: running remainders", end=" ")
r = 0; trail = []
for ch in "2026": r = (10 * r + int(ch)) % 7; trail.append(r)
print(trail, "->", 2026 % 7)

print("[3] casting out nines")
ds = lambda n: sum(int(c) for c in str(n))
check("n and its digit sum agree mod 9, every n < 100,000", all(n % 9 == ds(n) % 9 for n in range(100000)))
random.seed(12)
caught9 = caught11 = trials = 0
for _ in range(20000):
    n = random.randrange(10**5, 10**7); s = list(str(n))
    i = random.randrange(len(s) - 1)
    if s[i] == s[i + 1]: continue
    s[i], s[i + 1] = s[i + 1], s[i]; m = int("".join(s)); trials += 1
    caught9 += (m % 9 != n % 9); caught11 += (m % 11 != n % 11)
print(f"     {trials:,} numbers with two neighbouring digits swapped: nines caught {caught9}, elevens caught {caught11}")
check("casting out nines never catches a swap of two digits", caught9 == 0)
check("the check by eleven catches every neighbouring swap of different digits", caught11 == trials)

print("""
[HONESTY]
[1]-[2] brute-force the Lean theorems on small ranges; the proofs are Carrying.lean.
[3]'s swap test uses 20,000 random 6-7 digit numbers, seed 12; that nines miss every
swap is a theorem (a swap does not change the digit sum), the sample only illustrates it.
""")
print(f"{len(FAIL)} FAIL")
sys.exit(1 if FAIL else 0)
