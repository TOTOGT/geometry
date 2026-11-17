#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""odd_perfect_check.py: the producing tool (R12) for every number on
book7/ch-odd-perfect.html and book7/ch-euclid.html.

What it computes, with integer arithmetic only:
  1. s(n) = sum of the proper divisors of n, for every n in 1..LIMIT (a sieve), and the
     perfect numbers found (s(n) = n, n > 0), split into even and odd.
  2. For p = 2..31: M = 2^p - 1, whether M is prime (trial division), its full factorisation
     when composite, N = 2^(p-1) * M, and (only while N <= BRUTE_MAX) a brute-force check
     that N is perfect by summing proper divisors with a square-root loop.
  3. The Lucas-Lehmer test for odd prime p, compared with trial division. p = 2 is handled
     explicitly: the test starts at s_0 = 4 and is defined for odd p only, and M = 3 is prime.
  4. Edge cases for the divisor-sum routine: 1, a prime, an odd square (9, 25), an even square (36).

It does NOT prove anything about odd perfect numbers: a finite search through LIMIT says nothing
about n > LIMIT. The page states the interval and the count; this script prints the same.

    python3 tools/odd_perfect_check.py                 human-readable report
    python3 tools/odd_perfect_check.py --json          the numbers the page embeds
    python3 tools/odd_perfect_check.py --limit 100000  a different search interval
"""
import json, sys

LIMIT = 999_999
BRUTE_MAX = 10 ** 10
P_MAX = 31

def proper_sum(n):
    """Sum of proper divisors of n (divisors < n), by a square-root loop.
    The square root of a perfect square is added once, not twice."""
    if n < 2:
        return 0
    total = 1
    d = 2
    while d * d <= n:
        if n % d == 0:
            total += d
            e = n // d
            if e != d:
                total += e
        d += 1
    return total

def sieve_proper_sums(limit):
    s = [0] * (limit + 1)
    for d in range(1, limit // 2 + 1):
        for m in range(2 * d, limit + 1, d):
            s[m] += d
    return s

def factorise(n):
    f, d = [], 2
    while d * d <= n:
        while n % d == 0:
            f.append(d); n //= d
        d += 1
    if n > 1:
        f.append(n)
    return f

def is_prime(n):
    return n > 1 and factorise(n) == [n]

def lucas_lehmer(p):
    """True iff 2^p - 1 is prime, for odd prime p. p = 2 is handled by the caller."""
    m = (1 << p) - 1
    s = 4
    for _ in range(p - 2):
        s = (s * s - 2) % m
    return s == 0

def compute(limit=LIMIT):
    out = {"limit": limit}
    s = sieve_proper_sums(limit)
    perfect = [n for n in range(1, limit + 1) if s[n] == n]
    out["perfect_found"] = perfect
    out["odd_perfect_found"] = [n for n in perfect if n % 2 == 1]
    out["odd_candidates"] = len(range(1, limit + 1, 2))
    # routine cross-check: sqrt-loop vs sieve on the whole interval up to 5000
    k = min(limit, 5000)
    out["routine_agrees_to"] = k if all(proper_sum(n) == s[n] for n in range(1, k + 1)) else 0
    rows = []
    for p in range(2, P_MAX + 1):
        M = (1 << p) - 1
        row = {"p": p, "p_prime": is_prime(p), "M": M, "M_prime": is_prime(M)}
        if not row["M_prime"]:
            row["factors"] = factorise(M)
        N = (1 << (p - 1)) * M
        row["N"] = N
        if row["M_prime"]:
            row["brute_checked"] = N <= BRUTE_MAX
            if N <= BRUTE_MAX:
                row["N_perfect_brute"] = (proper_sum(N) == N)
        if row["p_prime"]:
            row["lucas_lehmer"] = True if p == 2 else lucas_lehmer(p)
            row["ll_agrees"] = (row["lucas_lehmer"] == row["M_prime"])
        rows.append(row)
    out["mersenne"] = rows
    out["edges"] = {str(n): proper_sum(n) for n in (1, 2, 6, 9, 25, 28, 36, 496)}
    return out

def main():
    limit = LIMIT
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])
    out = compute(limit)
    if "--json" in sys.argv:
        print(json.dumps(out, sort_keys=True))
        return 0
    fails = []
    def check(ok, msg):
        print("    %s  %s" % ("PASS" if ok else "FAIL", msg))
        if not ok: fails.append(msg)
    print("Perfect numbers in 1..%d: %s" % (limit, out["perfect_found"]))
    print("Odd candidates tested: %d positive odd integers from 1 through %d" % (out["odd_candidates"], limit))
    print("Odd perfect numbers found: %s" % (out["odd_perfect_found"] or "none (0 hits)"))
    print("\n  p   2^p-1        prime?  N = 2^(p-1)(2^p-1)   perfect (brute force)   LL")
    for r in out["mersenne"]:
        if not r["p_prime"]:
            continue
        pf = r.get("N_perfect_brute")
        print("%3d  %-12d %-6s  %-20d  %-22s  %s" % (
            r["p"], r["M"], r["M_prime"], r["N"],
            ("yes" if pf else "NO") if pf is not None else ("n/a (not prime)" if not r["M_prime"] else "not brute-forced"),
            "prime" if r.get("lucas_lehmer") else "composite"))
        if not r["M_prime"]:
            print("       2^%d - 1 = %s" % (r["p"], " x ".join(map(str, r["factors"]))))
    print("\nChecks")
    check(out["perfect_found"][:4] == [6, 28, 496, 8128] or limit < 8128, "the first perfect numbers found are 6, 28, 496, 8128 (within the interval)")
    check(out["odd_perfect_found"] == [], "no odd perfect number in 1..%d" % limit)
    check(out["routine_agrees_to"] == min(limit, 5000), "square-root-loop divisor sum agrees with the sieve for n <= 5000")
    e = out["edges"]
    check(e["1"] == 0, "s(1) = 0, so 1 is not perfect")
    check(e["9"] == 4 and e["25"] == 6, "odd squares count the square root once: s(9) = 1 + 3 = 4, s(25) = 1 + 5 = 6")
    check(e["36"] == 55, "even square: s(36) = 1+2+3+4+6+9+12+18 = 55")
    check(e["6"] == 6 and e["28"] == 28 and e["496"] == 496, "s(6) = 6, s(28) = 28, s(496) = 496")
    m = {r["p"]: r for r in out["mersenne"]}
    check(m[11]["M"] == 2047 and m[11]["factors"] == [23, 89], "2^11 - 1 = 2047 = 23 x 89")
    check(m[11]["p_prime"] and not m[11]["M_prime"], "11 is prime but 2^11 - 1 is not")
    check(all(r["ll_agrees"] for r in out["mersenne"] if r["p_prime"]), "Lucas-Lehmer agrees with trial division for every prime p <= %d" % P_MAX)
    check([r["p"] for r in out["mersenne"] if r["M_prime"]] == [2, 3, 5, 7, 13, 17, 19, 31],
          "Mersenne exponents up to 31 are 2, 3, 5, 7, 13, 17, 19, 31")
    check(all(r["N_perfect_brute"] for r in out["mersenne"] if r.get("brute_checked")),
          "every Euclid number with N <= 10^10 is perfect by brute-force divisor sum")
    # control: a number that is NOT perfect must fail the same test
    check(proper_sum(2 ** 10 * 2047) != 2 ** 10 * 2047, "control: 2^10 x 2047 (composite Mersenne factor) is NOT perfect")
    print("\n%s" % ("ALL PASS" if not fails else "FAILED: %d" % len(fails)))
    return 1 if fails else 0

if __name__ == "__main__":
    sys.exit(main())
