#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book11/ch03-verify.py -- every number on book11/ch03-zero.html. Run first (R24).

    python3 book11/ch03-verify.py

  [1] Bundling.lean §2: without a length rule, zero gives one number many names
  [2] §3: the digits of a numeral are the remainders of repeated division
  [3] §4: bijective base ten (digits 1..10, no zero) -- every number 1..100,000 has
      exactly one name, at any length
  [4] what the missing zero costs: carrying, and the digit that is not a remainder
  [HONESTY]
Standard library only.
"""
import itertools, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
val = lambda b, ds: sum(d * b**i for i, d in enumerate(ds))
src = open(os.path.join(ROOT, "book11/Bundling.lean"), encoding="utf-8").read()
for name in ("high_zero", "two_names", "low_digit_is_remainder", "bijective_unique"):
    check(f"Bundling.lean states {name}", f"theorem {name}" in src)

print("[1] zero on the high end")
names3 = [ds for L in range(1, 5) for ds in itertools.product(range(10), repeat=L) if val(10, ds) == 3]
print(f"     digit lists of length 1..4 naming 3: {names3}")
check("3 has four names at lengths 1-4: 3, 03, 003, 0003", len(names3) == 4)

print("[2] digits are remainders")
def digits(n, b):
    out = []
    while n: out.append(n % b); n //= b
    return out or [0]
for n in (273, 2026, 60):
    print(f"     {n}: remainders on dividing by 10, lowest first {digits(n, 10)}; by 60 {digits(n, 60)}")
check("273 -> [3, 7, 2]", digits(273, 10) == [3, 7, 2])
check("every n < 10^5: its standard digits read back to n", all(val(10, digits(n, 10)) == n for n in range(100000)))

print("[3] bijective base ten, no zero")
def bij(n, b):
    out = []
    while n:
        d = n % b or b
        out.append(d); n = (n - d) // b
    return out
names = {}
for L in range(1, 6):
    for ds in itertools.product(range(1, 11), repeat=L):
        names.setdefault(val(10, ds), []).append(ds)
upto = 100000
multi = [n for n in range(1, upto + 1) if len(names.get(n, [])) > 1]
missing = [n for n in range(1, upto + 1) if n not in names]
check("no number 1..100,000 has two zero-free names (lengths 1-5 enumerated)", not multi, f"{len(names):,} names")
check("and none is missing: every number 1..100,000 has one", not missing)
check("the greedy rule d = n mod 10, or 10 if that is 0, finds it", all(tuple(bij(n, 10)) == names[n][0] for n in range(1, upto + 1)))
print(f"     examples: 10 -> {bij(10,10)}, 20 -> {bij(20,10)}, 100 -> {bij(100,10)}, 2026 -> {bij(2026,10)}")

print("[4] what the missing zero costs")
check("in bijective base ten, the lowest digit of 20 is 10, which is not 20 mod 10", bij(20, 10)[0] == 10 and 20 % 10 == 0)
lens = [(n, len(digits(n, 10)), len(bij(n, 10))) for n in (9, 10, 99, 100, 1000)]
print("     n, standard length, zero-free length:", lens)
check("zero-free numerals are never longer, and sometimes shorter (100 is [10, 9], two digits)", all(z <= s for _, s, z in lens) and bij(100, 10) == [10, 9])

print("""
[HONESTY]
[1]-[3] brute-force the Lean theorems on small cases; the proofs are the Lean file.
Bijective numeration is standard mathematics, not this corpus's; no history of who
had a zero and when is claimed, because no source on it is held (wanted: Ifrah,
The Universal History of Numbers; or Menninger, Number Words and Number Symbols).
""")
print(f"{len(FAIL)} FAIL")
sys.exit(1 if FAIL else 0)
