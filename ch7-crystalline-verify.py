#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ch7-crystalline-verify.py — companion to ch7-crystalline.html (Book 3, chapter 33).

The chapter prints thirteen numbers to three or more decimals and a table of
k-nacci sequences. All of it is exactly computable, and none of it had a script.

This one does not take the numbers from a transcription. It **reads them out of the
page** and recomputes them, so a later edit to the page is checked rather than
assumed. Five blocks.

  [1] The limit ratios. eta_k is the root in (1,2) of x^(k+1) - 2x^k + 1 = 0,
      which is the characteristic equation of the k-nacci recurrence with the
      spurious root x = 1 divided out. Bisected to 1e-15 and compared against
      every ratio the page prints, at the page's own precision.
  [2] The sequences. Each row's first ten terms, regenerated from the recurrence
      with the page's own seed, and compared term by term.
  [3] eta_k is strictly increasing in k and bounded above by 2, so the
      "infinity-bonacci = 2.00000" row is a limit and not a member.
  [4] Where hexanacci leaves the powers of two, which the chapter draws attention
      to. The departure is at the eighth term and the script says which.
  [5] The widget's short forms against the table's long ones.

Requires: nothing but the standard library.
Run:  python3 ch7-crystalline-verify.py

Principia Orthogona - Book 3 - G6 LLC - CC BY-NC-ND 4.0
"""

import html as H
import re
import sys
from pathlib import Path

PAGE = Path(__file__).resolve().parent / "ch7-crystalline.html"
FAIL = []


def check(label, ok, detail=""):
    print(f"    {'PASS' if ok else 'FAIL'}  {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def text_of(p: Path) -> str:
    s = p.read_text(encoding="utf-8")
    s = re.sub(r"<script.*?</script>|<style.*?</style>", "", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"[ \t]+", " ", H.unescape(s))


def eta(k: int, tol=1e-15) -> float:
    """Root in (1,2) of x^(k+1) - 2x^k + 1."""
    f = lambda x: x ** (k + 1) - 2 * x ** k + 1
    lo, hi = 1.0 + 1e-12, 2.0
    assert f(lo) > 0 > f(hi) or f(lo) < 0 < f(hi), "bracket does not straddle"
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if (f(lo) < 0) == (f(mid) < 0):
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)


def knacci(k: int, n: int) -> list[int]:
    """First n terms, seeded 1,1 then each term the sum of the last k."""
    seq = [1, 1]
    while len(seq) < n:
        seq.append(sum(seq[-k:]))
    return seq[:n]


NAMES = {2: "Fibonacci", 3: "Tribonacci", 4: "Tetranacci",
         5: "Pentanacci", 6: "Hexanacci"}


def block1(txt):
    print("\n[1] LIMIT RATIOS  eta_k, root in (1,2) of x^(k+1) - 2x^k + 1 = 0")
    print("    Every ratio the page prints, checked at the page's own precision.\n")
    rows = re.findall(r"(\d)\s+(Fibonacci|Tribonacci|Tetranacci|Pentanacci|Hexanacci)\s+(\d\.\d+)", txt)
    print(f"      {'k':>2} {'name':<11} {'page':>10} {'computed':>18} {'agrees to':>10}")
    print("      " + "-" * 56)
    ok = True
    for ks, name, printed in rows:
        k = int(ks)
        e = eta(k)
        dp = len(printed.split(".")[1])
        agree = f"{e:.{dp}f}" == printed
        print(f"      {k:>2} {name:<11} {printed:>10} {e:>18.12f} {dp:>7} dp {'' if agree else '  <-- NO'}")
        ok &= agree
    check(f"all {len(rows)} table ratios reproduce", ok and len(rows) >= 5,
          f"{len(rows)} rows parsed from the page")
    return ok


def block2(txt):
    print("\n[2] SEQUENCES  first ten terms, regenerated from the recurrence")
    # The Hexanacci row carries a "✦" between its ratio and its sequence. The
    # first version of this pattern did not allow it, parsed four rows instead
    # of five, and reported a failure that was the parser's, not the page's.
    rows = re.findall(
        r"(Fibonacci|Tribonacci|Tetranacci|Pentanacci|Hexanacci)\s+\d\.\d+…?\s*[^\d]*?((?:\d+,){9}\d+)",
        txt)
    inv = {v: k for k, v in NAMES.items()}
    ok = True
    for name, csv in rows:
        k = inv[name]
        page = [int(x) for x in csv.split(",")]
        mine = knacci(k, 10)
        good = page == mine
        print(f"      {name:<11} k={k}  page {csv}")
        if not good:
            print(f"      {'':<11}       mine {','.join(map(str, mine))}")
        ok &= good
    check(f"all {len(rows)} sequences regenerate term by term", ok and len(rows) == 5,
          f"{len(rows)} rows parsed — the count is asserted, so a row that stops\n                                        matching fails instead of quietly shrinking the check")
    return ok


def block3():
    print("\n[3] MONOTONE AND BOUNDED  eta_k increases in k, and 2 is the limit")
    es = [(k, eta(k)) for k in range(2, 13)]
    for k, e in es[:6]:
        print(f"      eta_{k:<2} = {e:.12f}")
    print(f"      eta_12 = {es[-1][1]:.12f}")
    ok1 = check("strictly increasing in k", all(a[1] < b[1] for a, b in zip(es, es[1:])))
    ok2 = check("bounded above by 2", all(e < 2 for _, e in es))
    ok3 = check("approaches 2 (eta_12 within 1e-3)", 2 - es[-1][1] < 1e-3,
                f"2 - eta_12 = {2 - es[-1][1]:.3e}")
    print("\n      So the page's 'infinity-bonacci  2.00000' row is the limit, not a")
    print("      member of the family: no finite k attains it.")
    return ok1 and ok2 and ok3


def block4(txt):
    print("\n[4] WHERE HEXANACCI LEAVES THE POWERS OF TWO")
    seq = knacci(6, 10)
    pw = [1] + [2 ** i for i in range(9)]
    first = next(i for i, (a, b) in enumerate(zip(seq, pw)) if a != b)
    print(f"      hexanacci   {seq}")
    print(f"      1,2,4,8,... {pw}")
    print(f"      first disagreement at index {first} (term {first + 1}): "
          f"{seq[first]} vs {pw[first]}")
    ok1 = check("the first seven terms agree with doubling", seq[:7] == pw[:7])
    ok2 = check("the eighth term is 63, not 64", seq[7] == 63 and pw[7] == 64)
    print("\n      The recurrence sums the last six terms, so it can only match")
    print("      doubling while fewer than six terms exist to sum. 63 = 64 - 1 is")
    print("      the missing seventh predecessor.")
    return ok1 and ok2


def block5(txt):
    print("\n[5] THE WIDGET'S SHORT FORMS AGAINST THE TABLE'S LONG ONES")
    short = dict(re.findall(r"(\d)-bonacci · φ=(\d\.\d+)", txt))
    ok = True
    for ks, printed in sorted(short.items()):
        k = int(ks)
        e = eta(k)
        dp = len(printed.split(".")[1])
        agree = f"{e:.{dp}f}" == printed
        print(f"      {k}-bonacci widget {printed:>7}   eta_{k} = {e:.12f}   {'ok' if agree else 'NO'}")
        ok &= agree
    check(f"all {len(short)} widget ratios round correctly", ok and len(short) >= 6,
          f"{len(short)} parsed")
    return ok


def main():
    print(__doc__.split("Requires:")[0].rstrip())
    print("=" * 70)
    if not PAGE.exists():
        print(f"\nFAIL: {PAGE.name} not found")
        return 1
    txt = text_of(PAGE)
    block1(txt); block2(txt); block3(); block4(txt); block5(txt)
    print("\n" + "=" * 70)
    if FAIL:
        print(f"\n{len(FAIL)} CHECK(S) FAILED:")
        for f in FAIL:
            print("   -", f)
        return 1
    print("\nALL CHECKS PASSED   (5 blocks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
