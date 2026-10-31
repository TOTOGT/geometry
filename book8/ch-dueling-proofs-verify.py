#!/usr/bin/env python3
"""
ch-dueling-proofs-verify.py -- what can be computed about the three results
reported by Scientific American on 27 Oct 2026 (Kakeya, Yang-Mills existence,
ETH). Nothing here checks any of the three proofs.

A. Date arithmetic on the reported timeline.
B. The Millennium count as printed in the article, which does not add up
   on its face. Recorded as a question, not a finding.
C. WHAT "REFUTING ETH" REQUIRES. ETH: 3-SAT needs 2^(delta*n) time for some
   delta>0. A running time c^n with 1<c<2 is faster than 2^n and is STILL
   exponential, so it does not refute ETH; refuting ETH needs 2^(o(n)). Shown
   numerically: log2(T)/n stays constant for c^n and tends to 0 for 2^sqrt(n).
   This is why "a tiny bit faster than exponential" cannot by itself be read as
   a refutation. What was actually proved is not in the source.
NOT COMPUTED: the chapter's remark that Kakeya concerns dimension, not volume,
   is standard background stated in prose. Nothing in this script checks it.

Run:  python3 book8/ch-dueling-proofs-verify.py
"""
import datetime as dt, math
FAIL = []
def check(n, c, note=""):
    print("  [%s] %s" % ("SHOWN" if c else "FAIL ", n))
    if note: print("        " + note)
    if not c: FAIL.append(n)
def control(n, c):
    print("  [%s] control: %s" % ("OK   " if not c else "BLIND", n))
    if c: FAIL.append("blind control: " + n)

print("A. Timeline as reported")
art, drop, first = dt.date(2026,10,27), dt.date(2026,10,26), dt.date(2026,10,6)
check("article dated 27 Oct says 'yesterday': the drop is 26 Oct", (art-dt.timedelta(days=1)) == drop)
check("6 Oct release to 26 Oct drop = 20 days ('a few weeks')", (drop-first).days == 20)
control("20 days is not 20 weeks", (drop-first).days == 140)

found, anth, oai = dt.date(2026,10,16), dt.date(2026,10,27), dt.date(2026,10,26)
check("Anthropic preprint (27 Oct) is one day after the OpenAI preprint it cites (26 Oct)", (anth-oai).days == 1)
control("same-day posting would contradict 'one day after'", (anth-oai).days == 0)
check("core algorithm reportedly found 16 Oct, 11 days before posting", (anth-found).days == 11)

print("\nB. Millennium Prize Problems as printed")
SET, SOLVED_KNOWN = 7, 1
print("  [NOTE ] article: 'one of seven set by Clay in 2000' and 'five ... remain open'.")
print("          7 - 1 solved (Poincare, Perelman, accepted) = %d open, not 5." % (SET-SOLVED_KNOWN))
check("7 - 1 = 6", SET - SOLVED_KNOWN == 6)
print("          Five open would mean one further problem counted as resolved. The source")
print("          does not say which. Either the article counts a disputed claim as resolved")
print("          or one of its figures is off; this book does not decide.")

print("\nC. What refuting ETH requires")
def rate(logT, n): return logT / n
ns = [10**3, 10**4, 10**5, 10**6]
c = 1.31                                  # illustrative base below 2, not a cited bound
r_c   = [rate(n*math.log2(c), n) for n in ns]
r_sub = [rate(math.sqrt(n), n) for n in ns]
print("  n          log2(T)/n for c^n (c=1.31)   log2(T)/n for 2^sqrt(n)")
for n, a, b in zip(ns, r_c, r_sub): print("  %-10d %-28.5f %-.5f" % (n, a, b))
check("c^n with c<2: log2(T)/n is constant (still exponential)", max(r_c)-min(r_c) < 1e-12)
check("c^n is faster than 2^n for every n (c<2)", all(math.log2(c) < 1 for _ in ns))
check("2^sqrt(n): log2(T)/n decreases toward 0", all(r_sub[i] > r_sub[i+1] for i in range(len(r_sub)-1)) and r_sub[-1] < 0.002)
control("c^n must NOT tend to 0 (if it did, c^n would refute ETH)", r_c[-1] < 0.002)

print()
if FAIL: print("FAILED:", FAIL); raise SystemExit(1)
print("ALL CHECKS SHOWN. No proof of Kakeya, Yang-Mills existence or ETH was examined.")
