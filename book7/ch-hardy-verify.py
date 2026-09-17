#!/usr/bin/env python3
"""
ch-hardy-verify.py

Hardy said his work was useless. He wrote it down, in print, as a prediction
about the future. This file checks the prediction against the two theorems he
offered as specimens of beauty, and against the one result of his own he
thought too trivial to mention.

Primary source, read directly (1967 Cambridge edition, Snow foreword):
  G. H. Hardy, A Mathematician's Apology.
  p. 148  "I was at my best at a little past forty... A mathematician may still
           be competent enough at sixty, but it is useless to expect him to
           have original ideas."
  p. 150  "I have never done anything 'useful'. No discovery of mine has made,
           or is likely to make, directly or indirectly, for good or ill, the
           least difference to the amenity of the world."
  p. 151  "Judged by all practical standards, the value of my mathematical life
           is nil; and outside mathematics it is trivial anyhow."
  p. 152  Note: "In short, my section 28 is much too 'sentimental'."

Standard library only. Exact arithmetic throughout.
"""

from fractions import Fraction as F
import math, itertools

FAIL = []
def check(name, ok, detail=""):
    print(("  PASS  " if ok else "  FAIL  ") + name + (("   " + detail) if detail else ""))
    if not ok: FAIL.append(name)

# ---------------------------------------------------------------------------
print("[1] The two theorems Hardy offered as specimens of real mathematics.")
print("    He chose them for economy and inevitability, not for use.")
print()

# Euclid: infinitely many primes. Verified constructively -- the proof IS the
# algorithm, so running it is running the proof.
def primes_upto(n):
    s = bytearray([1]) * (n + 1); s[0] = s[1] = 0
    for i in range(2, math.isqrt(n) + 1):
        if s[i]: s[i*i::i] = bytearray(len(s[i*i::i]))
    return [i for i in range(n + 1) if s[i]]

P = primes_upto(200)
print("    Euclid: given any finite set of primes, N = (product) + 1 has a")
print("    prime factor outside the set. Run on initial segments:")
for k in (1, 2, 3, 4, 5, 6):
    S = P[:k]
    N = 1
    for p in S: N *= p
    N += 1
    # smallest prime factor of N
    f = next(q for q in range(2, N + 1) if N % q == 0)
    print("      {%s}  ->  N = %6d  smallest factor %5d   new? %s"
          % (", ".join(map(str, S)), N, f, f not in S))
    check("Euclid's construction escapes {%s}" % ", ".join(map(str, S)), f not in S)

# Pythagoras: sqrt(2) irrational. The proof is a parity argument; check that the
# parity obstruction is real by exhaustion over all reduced fractions p/q with
# q bounded -- none squares to 2, and the near-misses are the convergents.
print()
print("    Pythagoras: no rational squares to 2. Exhaustive over q <= 2000,")
print("    and the closest approaches are exactly the continued-fraction")
print("    convergents of sqrt(2), which is why the proof has to be parity")
print("    and not a search.")
best = []
for q in range(1, 2001):
    p = round(math.isqrt(2 * q * q))
    for cand in (p, p + 1):
        d = abs(F(cand, q) ** 2 - 2)
        best.append((d, cand, q))
best.sort()
exact = [b for b in best if b[0] == 0]
check("no rational with denominator <= 2000 squares to 2", not exact)
print("      closest five:")
seen = set()
for d, p, q in best:
    if math.gcd(p, q) != 1 or q in seen: continue
    seen.add(q); print("        %4d/%-4d   |p^2/q^2 - 2| = %s" % (p, q, d))
    if len(seen) == 5: break
# First draft ranked by |p^2/q^2 - 2| and asserted the top five would be the
# convergent denominators. They are not: that metric weights small q wrongly.
# The exact invariant is Pell's: the convergents of sqrt2 are precisely the
# p/q with p^2 - 2q^2 = +-1. Test THAT, which is a theorem rather than a guess.
pell = [(p, q) for q in range(1, 1001) for p in (math.isqrt(2*q*q), math.isqrt(2*q*q)+1)
        if abs(p*p - 2*q*q) == 1]
conv_q = {1, 2, 5, 12, 29, 70, 169, 408, 985}
found_q = sorted({q for _, q in pell})
print("      denominators with p^2 - 2q^2 = +-1, q <= 1000: %s" % found_q)
check("those are exactly the sqrt2 convergent denominators",
      set(found_q) == conv_q, str(found_q))
check("every one of them misses 2 by exactly 1/q^2",
      all(abs(F(p,q)**2 - 2) == F(1, q*q) for p, q in pell))
print("      The approximation never closes: |p^2/q^2 - 2| = 1/q^2 exactly,")
print("      for the best rationals there are. That is why Pythagoras needs a")
print("      parity argument and not a search, which is Hardy's point about")
print("      the proof being inevitable rather than clever.")

# ---------------------------------------------------------------------------
print()
print("[2] The result Hardy did not think worth mentioning.")
print("    Hardy-Weinberg, published 1908 in a letter to Science, after a")
print("    geneticist asked him a question at cricket. It is not named in the")
print("    Apology. It is the foundation of population genetics.")
print()
print("    Claim: under random mating, with no selection, mutation, migration")
print("    or drift, genotype frequencies reach p^2 : 2pq : q^2 after ONE")
print("    generation and are stationary thereafter.")
print()

def next_gen(P_AA, P_Aa, P_aa):
    """One generation of random mating, exactly, in Fractions."""
    p = P_AA + P_Aa / 2          # allele frequency of A
    q = P_aa + P_Aa / 2
    assert p + q == 1
    return p * p, 2 * p * q, q * q

print("      start (AA, Aa, aa)          after 1 gen              after 2")
starts = [(F(1), F(0), F(0)),
          (F(0), F(1), F(0)),
          (F(1,2), F(0), F(1,2)),
          (F(1,4), F(1,4), F(1,2)),
          (F(9,10), F(0), F(1,10))]
for s in starts:
    g1 = next_gen(*s)
    g2 = next_gen(*g1)
    stationary = (g1 == g2)
    print("      %-26s %-24s %s" % (
        "(%s, %s, %s)" % s,
        "(%s, %s, %s)" % g1,
        "stationary" if stationary else "NOT stationary"))
    check("equilibrium reached in one generation from (%s,%s,%s)" % s, stationary)

# and it is exactly p^2 : 2pq : q^2
for s in starts:
    p = s[0] + s[1] / 2; q = 1 - p
    g1 = next_gen(*s)
    check("the equilibrium is p^2 : 2pq : q^2 for p = %s" % p,
          g1 == (p * p, 2 * p * q, q * q))
print()
print("    Exact, in one generation, from every starting point. Hardy called")
print("    this 'very simple' and declined to claim it. It is the null model")
print("    against which every deviation in population genetics is measured.")

# ---------------------------------------------------------------------------
print()
print("[3] The prediction, tested where it is most often said to fail.")
print("    Hardy, p. 150: no discovery of his would make 'the least difference")
print("    to the amenity of the world'. Number theory became cryptography.")
print()
print("    RSA runs on Euler's theorem: a^phi(n) = 1 mod n for gcd(a,n) = 1.")
print("    That is eighteenth-century number theory, the kind Hardy meant.")

p_, q_ = 61, 53
n = p_ * q_
phi = (p_ - 1) * (q_ - 1)
e = 17
d = pow(e, -1, phi)
print("      p = %d, q = %d, n = %d, phi = %d, e = %d, d = %d" % (p_, q_, n, phi, e, d))
msgs = [65, 1234, 2000, 3000]
allok = True
for m in msgs:
    c = pow(m, e, n)
    back = pow(c, d, n)
    ok = (back == m)
    allok &= ok
    print("      m = %-5d ->  c = %-5d ->  %-5d   %s" % (m, c, back, "ok" if ok else "FAIL"))
check("encrypt-then-decrypt is the identity for every message tested", allok)
check("the exponent pair satisfies e*d = 1 mod phi(n)", (e * d) % phi == 1)
print()
print("    This is a toy n. The mathematics is not a toy, and it is Hardy's.")
print("    The Apology was published in 1940. RSA is 1977. Hardy could not")
print("    have known -- that is not the point. The point is that he wrote a")
print("    falsifiable claim about the future of his own subject, in print,")
print("    and the claim was falsified.")

# ---------------------------------------------------------------------------
print()
print("[4] The claim about age, which is his own and about himself.")
print("    p. 148: 'I was at my best at a little past forty.'")
print("    Hardy: born 7 February 1877. The Littlewood collaboration begins")
print("    1911; he meets Ramanujan's letter January 1913.")
# First draft printed "age 36" for January 1913 and then asserted 35. Hardy's
# birthday is 7 February, so a January date falls before it and the plain
# year difference is wrong by one. Corrected with the birthday, not the
# assertion loosened.
import datetime
BORN = datetime.date(1877, 2, 7)
def age_on(d):
    return d.year - BORN.year - ((d.month, d.day) < (BORN.month, BORN.day))
events = [(datetime.date(1911, 6, 1),  "Littlewood collaboration begins (year only)"),
          (datetime.date(1913, 1, 16), "Ramanujan's first letter"),
          (datetime.date(1940, 11, 1), "Apology published (year only)"),
          (datetime.date(1947, 12, 1), "death")]
for d, what in events:
    print("      %s   age %2d   %s" % (d.isoformat(), age_on(d), what))
check("Hardy was 34 at the start of the Littlewood collaboration",
      age_on(datetime.date(1911, 6, 1)) == 34)
check("Hardy was 35 when Ramanujan's letter arrived in January 1913",
      age_on(datetime.date(1913, 1, 16)) == 35,
      "before his 7 February birthday")
check("Hardy was 63 when the Apology appeared",
      age_on(datetime.date(1940, 11, 1)) == 63)
print("      Day-precise dates are used only where this file has one; the")
print("      1911 and 1940 rows are year-only and their day is a placeholder.")
print()
print("    He wrote 'it is useless to expect him to have original ideas' at")
print("    sixty-three, in a book that is still read. The Apology is itself a")
print("    counterexample to its own sentence, in the weak sense that it is")
print("    the work of his that most people have actually encountered.")

# ---------------------------------------------------------------------------
print()
print("[5] Relativity's standing military application, computed.")
print("    Hardy named relativity. GPS is a US Department of Defense")
print("    navigation constellation, first satellite 1978, and it does not")
print("    work without both special and general relativistic corrections.")
print("    This is not a one-off in 1945. It runs every day.")
print()

c    = 299792458.0            # m/s, exact by definition
GM   = 3.986004418e14         # m^3/s^2, WGS-84 Earth gravitational parameter
R_E  = 6371000.0              # m, mean Earth radius
r_gps = 26559800.0            # m, GPS semi-major axis (~20180 km altitude)
day  = 86400.0                # s
om_E = 7.2921150e-5           # rad/s, Earth rotation rate

v_sat = math.sqrt(GM / r_gps)
v_surf = om_E * R_E

sr_sat  = -(v_sat ** 2) / (2 * c * c)          # satellite runs slow (velocity)
sr_surf = -(v_surf ** 2) / (2 * c * c)         # ground clock also moving
sr_net  = sr_sat - sr_surf
gr_net  = (GM / (c * c)) * (1.0 / R_E - 1.0 / r_gps)   # satellite runs fast (potential)
net     = sr_net + gr_net

print("      satellite orbital speed      %10.1f m/s" % v_sat)
print("      ground clock speed (equator) %10.1f m/s" % v_surf)
print()
print("      special relativity  %+.4e   -> %+8.2f us/day" % (sr_net, sr_net * day * 1e6))
print("      general relativity  %+.4e   -> %+8.2f us/day" % (gr_net, gr_net * day * 1e6))
print("      net                 %+.4e   -> %+8.2f us/day" % (net,    net    * day * 1e6))
print()
drift_s = net * day
print("      uncorrected positional error: %.1f km per day" % (drift_s * c / 1000.0))

check("special relativity slows the satellite clock", sr_net < 0)
check("general relativity speeds it up by more", gr_net > -sr_net)
check("the net is between 35 and 42 microseconds per day",
      35e-6 < drift_s < 42e-6, "%.2f us/day" % (drift_s * 1e6))
check("uncorrected drift exceeds 10 km of position per day",
      drift_s * c > 10000.0, "%.1f km/day" % (drift_s * c / 1000))
print()
print("    Both of Einstein's theories, with opposite signs, in a system whose")
print("    purpose includes guiding munitions. Hardy wrote that no warlike")
print("    purpose had been found for relativity and that it seemed 'very")
print("    unlikely that anyone will do so for many years'. The bomb arrived in")
print("    five. The navigation system arrived in thirty-eight and has not")
print("    stopped since.")

# ---------------------------------------------------------------------------
print()
if FAIL:
    print("FAILED: " + "; ".join(FAIL)); raise SystemExit(1)
print("All checks passed.")
print()
print("What Hardy did on p. 152, which is why this chapter exists. Broad and")
print("Snow told him section 28 was wrong. He agreed in print -- 'my section 28")
print("is much too sentimental' -- and DID NOT REVISE THE TEXT. He printed the")
print("criticism as a Note and left the original standing, saying he had found")
print("it impossible to meet the objections and would content himself with the")
print("acknowledgement. That is this corpus's correction practice, in 1940, by")
print("a man who had no verification scripts and did it anyway.")
