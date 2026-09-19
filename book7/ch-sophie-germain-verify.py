#!/usr/bin/env python3
"""
ch-sophie-germain-verify.py -- every number on book7/ch-sophie-germain.html.

Blocks:
  [1] the first twenty Germain primes, as printed
  [2] the three counts: 190 below 10^4, 1171 below 10^5, 7746 below 10^6
  [3] Germain's Case 1 criterion, tested by exhaustion in a finite box
  [4] the non-trivial degenerate pairs m^2+n^2 for the square plate
  [5] degeneracy gives a one-parameter family of nodal curves, not one figure

Standard library only.  Run:  python3 book7/ch-sophie-germain-verify.py
"""
import sys
from collections import defaultdict

FAIL = []
def check(label, ok, detail=""):
    print(("  PASS  " if ok else "  FAIL  ") + label + (("   " + detail) if detail else ""))
    if not ok: FAIL.append(label)

def sieve(n):
    s = bytearray([1]) * (n + 1); s[0] = s[1] = 0
    i = 2
    while i * i <= n:
        if s[i]: s[i*i::i] = bytearray(len(s[i*i::i]))
        i += 1
    return s

LIM = 2 * 10**6 + 10
S = sieve(LIM)

print("=" * 70)
print("ch-sophie-germain-verify.py")
print("=" * 70)

print("\n[1] the first twenty Germain primes")
G = [p for p in range(2, 400) if S[p] and S[2*p+1]][:20]
WANT = [2, 3, 5, 11, 23, 29, 41, 53, 83, 89, 113, 131, 173, 179, 191, 233, 239, 251, 281, 293]
check("list matches the page", G == WANT, str(G))

print("\n[2] counting functions")
for N, want in [(10**4, 190), (10**5, 1171), (10**6, 7746)]:
    got = sum(1 for p in range(2, N) if S[p] and S[2*p+1])
    check("Germain primes below 10^%d" % len(str(N-1)), got == want,
          "got %d, page says %d" % (got, want))

print("\n[3] Case 1 of Fermat under Germain's criterion, by exhaustion")
print("      for each Germain prime p, search x,y,z in [1,B] with p not dividing xyz")
B = 120
for p in [3, 5, 11, 23]:
    bad = None
    pw = {v: pow(v, p, 0) for v in ()}     # placeholder, exact arithmetic below
    for x in range(1, B + 1):
        if x % p == 0: continue
        xp = x ** p
        for y in range(x, B + 1):
            if y % p == 0: continue
            s = xp + y ** p
            # integer p-th root of s
            lo, hi = 1, B * 2
            while lo < hi:
                mid = (lo + hi) // 2
                if mid ** p < s: lo = mid + 1
                else: hi = mid
            if lo ** p == s and lo % p != 0:
                bad = (x, y, lo); break
        if bad: break
    check("p = %2d  (2p+1 = %2d, prime)  no solution with p!|xyz in [1,%d]"
          % (p, 2*p+1, B), bad is None, "" if bad is None else "FOUND %s" % (bad,))

print("\n[4] non-trivial degeneracies of the simply supported square plate")
d = defaultdict(set)
for m in range(1, 12):
    for n in range(1, 12):
        d[m*m + n*n].add(tuple(sorted((m, n))))
deg = [(k, sorted(v)) for k, v in sorted(d.items()) if len(v) > 1]
PAGE = {50: [(1, 7), (5, 5)], 65: [(1, 8), (4, 7)], 85: [(2, 9), (6, 7)],
        125: [(2, 11), (5, 10)], 130: [(3, 11), (7, 9)]}
for k, want in sorted(PAGE.items()):
    got = dict(deg).get(k)
    check("m^2+n^2 = %3d  <-  %s" % (k, want), got == want, "computed %s" % (got,))
check("the page lists every non-trivial degeneracy with m,n <= 11",
      sorted(PAGE) == [k for k, _ in deg], "computed keys %s" % [k for k, _ in deg])

print("\n[5] a degenerate eigenvalue is a FAMILY, not a figure")
import math
def w(m, n, x, y): return math.sin(m*math.pi*x) * math.sin(n*math.pi*y)
# every combination cos(t) phi1 + sin(t) phi2 solves the same eigenproblem:
# check the Rayleigh quotient (m^2+n^2 is shared) by verifying the two modes
# have equal eigenvalue, hence any combination does.
check("(1,7) and (5,5) share the eigenvalue", 1*1+7*7 == 5*5+5*5, "both 50")
# the nodal SET genuinely differs with t: sample the zero sets
def nodal_count(t, N=400):
    c, s = math.cos(t), math.sin(t)
    prev = None; crossings = 0
    for i in range(N + 1):
        x = i / N
        v = c * w(1, 7, x, 0.5) + s * w(5, 5, x, 0.5)
        if prev is not None and prev * v < 0: crossings += 1
        prev = v
    return crossings
counts = {round(t, 3): nodal_count(t) for t in [0.0, 0.4, 0.8, 1.2, math.pi/2]}
check("the nodal set on the mid-line changes with t", len(set(counts.values())) > 1,
      "crossings by t: %s" % counts)

print("\n" + "=" * 70)
print("[HONESTY]")
print("=" * 70)
print("""  What this establishes. The Germain prime list and the three counting
  figures are exact. The degeneracies of the simply supported square plate are
  exact facts about sums of two squares, and block [4] confirms the page lists
  all of them within its stated range. Block [5] shows the nodal set of a
  degenerate pair genuinely varies with the mixing angle, so "a family of
  figures, not a figure" is measured and not asserted.

  What it does not establish. Block [3] is an exhaustion over x, y <= 120 for
  four small Germain primes. That is EVIDENCE FOR Germain's theorem and in no
  sense a proof of it; the theorem is Germain's and its proof is hers, not a
  search. Nothing here re-proves Fermat's Last Theorem or any case of it.

  Block [5] samples one horizontal line of the square and counts sign changes.
  Different nodal sets certainly imply different figures; equal counts on one
  line would not have implied the figures were the same. The test is sound in
  the direction it is used and not in the other.

  The plate model is the simply supported square, which has closed-form modes.
  Chladni's plates were free at the edge and driven by a bow, and their exact
  spectrum is not this one. The degeneracy phenomenon is general; these
  particular integers are not Chladni's.""")

print()
if FAIL:
    print("FAILED: %d" % len(FAIL))
    for f in FAIL: print("   " + f)
    sys.exit(1)
print("All blocks pass.")
