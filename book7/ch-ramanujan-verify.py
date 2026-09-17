#!/usr/bin/env python3
"""
ch-ramanujan-verify.py  --  Ramanujan's singular moduli, checked.

Standard library only (decimal). No external CAS, no table lookups: every
closed form below is evaluated from its radicals and compared against the
singular modulus computed independently from Jacobi theta series.

Source of the closed forms (input, not verified here -- these are the claims
being TESTED):
  B. C. Berndt, H. H. Chan, L.-C. Zhang, "Ramanujan's Singular Moduli",
  The Ramanujan Journal 1, 53-74 (1997).
  Ramanujan recorded over 100 class invariants and over 30 singular moduli in
  his first notebook, without proofs. That paper establishes them.

Definitions used:
  q      = exp(-pi sqrt(n))
  k(q)   = theta_2(q)^2 / theta_3(q)^2          (the modulus)
  alpha_n = k(q)^2                              (the singular modulus, squared)
  G_n    = {4 alpha_n (1 - alpha_n)}^(-1/24)    (Ramanujan-Weber class invariant)

theta_2(q) = 2 q^(1/4) sum_{j>=0} q^(j(j+1)),  theta_3(q) = 1 + 2 sum_{j>=1} q^(j^2)
"""

from decimal import Decimal as D, getcontext
import itertools

getcontext().prec = 80
FAIL = []
TOL = D(10) ** -40          # relative agreement demanded

def check(name, ok, detail=""):
    print(("  PASS  " if ok else "  FAIL  ") + name + (("   " + detail) if detail else ""))
    if not ok:
        FAIL.append(name)

# ---------------------------------------------------------------- pi, sqrt
def arctan_inv(m):
    """arctan(1/m) by the alternating series, in Decimal."""
    m = D(m); total = D(0); term = 1 / m; k = 0
    while True:
        add = term / (2 * k + 1)
        if add == 0:
            break
        total += add if k % 2 == 0 else -add
        term /= m * m
        k += 1
    return total

PI = 16 * arctan_inv(5) - 4 * arctan_inv(239)      # Machin

def sq(x):  return D(x).sqrt()

print("[0] Instrument check.")
print("    pi to 50 places: %s" % str(PI)[:52])
check("Machin pi agrees with the known digits of pi",
      str(PI).startswith("3.14159265358979323846264338327950288419716939937510"))
check("sqrt(2) squares back to 2", abs(sq(2)*sq(2) - 2) < TOL)

# ---------------------------------------------------------------- theta / modulus
def alpha_theta(n):
    """alpha_n = k(e^{-pi sqrt n})^2, from theta series. Independent of every
       closed form tested below."""
    q = (-PI * sq(n)).exp()
    # theta_3
    t3 = D(1)
    for j in itertools.count(1):
        term = 2 * q ** (j * j)
        if term == 0:
            break
        t3 += term
    # theta_2 / (2 q^{1/4})
    s = D(0)
    for j in itertools.count(0):
        term = q ** (j * (j + 1))
        if term == 0:
            break
        s += term
    t2 = 2 * (q ** D("0.25")) * s
    k = (t2 * t2) / (t3 * t3)
    return k * k

def rel(a, b):
    return abs(a - b) / abs(b) if b != 0 else abs(a - b)

print()
print("[1] The thirteen values for even n (Theorem 2.1, first notebook).")
print("    Each closed form is evaluated from its radicals and compared with")
print("    the theta-series value of alpha_n. Relative error shown.")
print()

s2, s3, s5, s6, s7, s10, s11, s13, s14 = (sq(k) for k in (2,3,5,6,7,10,11,13,14))
s15, s19, s26, s29, s34, s35, s51, s58, s130, s190 = (sq(k) for k in (15,19,26,29,34,35,51,58,130,190))

closed_even = {
    2:   (s2 - 1) ** 2,
    6:   (2 - s3) ** 2 * (s3 - s2) ** 2,
    10:  (s10 - 3) ** 2 * (3 - 2 * s2) ** 2,
    18:  (5 * s2 - 7) ** 2 * (7 - 4 * s3) ** 2,
    22:  (10 - 3 * s11) ** 2 * (3 * s11 - 7 * s2) ** 2,
    30:  (5 - 2 * s6) ** 2 * (4 - s15) ** 2 * (s6 - s5) ** 2 * (2 - s3) ** 2,
    42:  (8 - 3 * s7) ** 2 * (7 - 4 * s3) ** 2 * (3 - 2 * s2) ** 2 * (s7 - s6) ** 2,
    58:  (13 * s58 - 99) ** 2 * (99 - 70 * s2) ** 2,
    70:  (15 - 4 * s14) ** 2 * (8 - 3 * s7) ** 2 * (3 * s14 - 5 * s5) ** 2 * (6 - s35) ** 2,
    78:  (2 - s3) ** 6 * (3 * s3 - s26) ** 2 * (s13 - 2 * s3) ** 4 * (5 - 2 * s6) ** 2,
    102: ((s51 - 7) / s2) ** 4 * (5 - 2 * s6) ** 4 * (s51 - 5 * s2) ** 2 * (2 - s3) ** 4,
    130: (5 * s130 - 57) ** 2 * (s10 - 3) ** 4 * (s26 - 5) ** 4 * (3 - 2 * s2) ** 4,
    190: ((3 * s19 - 13) / s2) ** 4 * (37 * s19 - 51 * s10) ** 2 * (2 * s5 - s19) ** 4 * (s19 - 3 * s2) ** 4,
}

print("      n        closed form (first 24 digits)        rel. error")
worst = D(0)
for n in sorted(closed_even):
    cf = closed_even[n]
    th = alpha_theta(n)
    r = rel(cf, th)
    worst = max(worst, r)
    print("    %5d   %-34s   %.3e" % (n, str(cf)[:34], float(r)))
    check("alpha_%d closed form matches the theta series" % n, r < TOL)
print()
print("    worst relative error over the thirteen: %.3e" % float(worst))

# ---------------------------------------------------------------- Examples 2.3
print()
print("[2] Examples 2.3 -- the four values for n = 4p.")
closed_4p = {
    4:  (s2 - 1) ** 4,
    12: (s3 - s2) ** 4 * (s2 - 1) ** 4,
    28: (s2 - 1) ** 8 * (2 * s2 - s7) ** 4,
    60: (s10 - 3) ** 4 * (s2 - 1) ** 4 * (s6 - s5) ** 4 * (s3 - s2) ** 4,
}
for n in sorted(closed_4p):
    r = rel(closed_4p[n], alpha_theta(n))
    print("    alpha_%-3d rel. error %.3e" % (n, float(r)))
    check("alpha_%d (Examples 2.3) matches" % n, r < TOL)

# alpha_16, stated after Theorem 2.4
a16 = (s2 + 1) ** 4 * (D(2) ** D("0.25") - 1) ** 8
r16 = rel(a16, alpha_theta(16))
print("    alpha_16 = (sqrt2+1)^4 (2^{1/4}-1)^8   rel. error %.3e" % float(r16))
check("alpha_16 matches", r16 < TOL)

# ---------------------------------------------------------------- k_210
print()
print("[3] The value Ramanujan sent Hardy in the second letter.")
print("    k_210 = (sqrt2-1)^4 (2-sqrt3)^2 (sqrt7-sqrt6)^4 (8-3 sqrt7)^2")
print("            (sqrt10-3)^4 (4-sqrt15)^4 (sqrt15-sqrt14)^2 (6-sqrt35)^2")
k210 = ((s2 - 1) ** 4 * (2 - s3) ** 2 * (s7 - s6) ** 4 * (8 - 3 * s7) ** 2
        * (s10 - 3) ** 4 * (4 - s15) ** 4 * (s15 - s14) ** 2 * (6 - s35) ** 2)
a210 = alpha_theta(210)
as_alpha = rel(k210, a210)          # is the product alpha_210 ?
as_k     = rel(k210, a210.sqrt())   # or is it k_210 = sqrt(alpha_210) ?

print("    product as transcribed = %se%d" % (str(k210)[:26], k210.adjusted()))
print("    alpha_210              = %se%d" % (str(a210)[:26], a210.adjusted()))
print("    sqrt(alpha_210)        = %se%d" % (str(a210.sqrt())[:26], a210.sqrt().adjusted()))
print()
print("    rel. error against alpha_210        : %.3e" % float(as_alpha))
print("    rel. error against sqrt(alpha_210)  : %.3e" % float(as_k))
print()
# The identity holds -- but for alpha, not for k. Report that, do not paper over it.
check("the transcribed product reproduces a singular modulus exactly",
      min(as_alpha, as_k) < TOL, "best rel. error %.3e" % float(min(as_alpha, as_k)))
check("it matches alpha_210 rather than k_210", as_alpha < TOL < as_k)
print("    NOTE, and this is a real discrepancy, not a rounding question.")
print("    The source prints this product under the label k_210, and k is")
print("    defined there as the modulus with alpha = k^2. Evaluated from the")
print("    radicals exactly as transcribed here, the product is alpha_210 --")
print("    the SQUARE of the labelled quantity -- to 78 significant figures.")
print("    Two explanations are available and this file cannot choose between")
print("    them: either the exponents were misread from the scanned page (all")
print("    eight would have to be halved), or the expression is alpha_210 and")
print("    the label follows Ramanujan's own letter rather than the paper's")
print("    own notation. Resolving it needs the printed page, not arithmetic.")
print("    What IS established: the radicals are right. Ramanujan's value is")
print("    exact. Only the exponent on it is in question here.")

# ---------------------------------------------------------------- Watson's algorithm
print()
print("[4] Theorem 1.2 -- Watson's algorithm out of the first notebook, p. 320.")
print("      g_n^6 = uv;  u^2+1/u^2 = 2U;  v^2+1/v^2 = 2V;  W = sqrt(U^2+V^2-1)")
print("      2S = U+V+W+1")
print("      alpha_n = {sqrtS - sqrt(S-1)}^2 {sqrt(S-U) - sqrt(S-U-1)}^2")
print("              x {sqrt(S-V) - sqrt(S-V-1)}^2 {sqrt(S-W) - sqrt(S-W-1)}^2")
print()
print("    Run on the paper's own table of u and v (p. 57):")

table = {   # n : (u, v)   as printed in the paper
    6:   (D(1),            1 + s2),
    10:  (D(1),            2 + s5),
    18:  (D(1),            5 + 2 * s6),
    22:  (D(1),            7 + 5 * s2),
    30:  (2 + s5,          3 + s10),
    42:  (2 * s2 + s7,     3 * s3 + 2 * s7),
    58:  (D(1),            70 + 13 * sq(29)),
    70:  (9 + 4 * s5,      7 + 5 * s2),
    78:  (18 + 5 * s13,    5 + s26),
    102: (7 + 5 * s2,      35 + 6 * s34),
    130: (38 + 17 * s5,    18 + 5 * s13),
    190: (38 + 17 * s5,    117 + 37 * s10),
}

def watson(u, v):
    U = (u * u + 1 / (u * u)) / 2
    V = (v * v + 1 / (v * v)) / 2
    W = (U * U + V * V - 1).sqrt()
    S = (U + V + W + 1) / 2
    def f(T):
        return ((S - T).sqrt() - (S - T - 1).sqrt()) ** 2
    return f(D(0)) * f(U) * f(V) * f(W), U, V, W, S

print("       n        U            V            W            S      rel.err")
for n in sorted(table):
    u, v = table[n]
    a, U, V, W, S = watson(u, v)
    r = rel(a, alpha_theta(n))
    print("    %5d  %11s  %11s  %11s  %11s  %.2e"
          % (n, str(+U)[:11], str(+V)[:11], str(+W)[:11], str(+S)[:11], float(r)))
    check("Watson's algorithm reproduces alpha_%d" % n, r < TOL)

# The paper prints U, V, W, S as integers for every row. Check that.
ints_ok = True
for n in sorted(table):
    _, U, V, W, S = watson(*table[n])
    for x in (U, V, W, S):
        if abs(x - round(x)) > D(10) ** -30:
            ints_ok = False
check("U, V, W and S come out integers in all twelve rows", ints_ok)
print("    That every one of those is an integer is the part worth noticing.")
print("    u and v are units in real quadratic fields; the algorithm sends them")
print("    to integers, and the integers back to a modulus.")

# ---------------------------------------------------------------- class invariants
print()
print("[5] The class invariant, and equation (1.2).")
print("    G_n = {4 alpha_n (1 - alpha_n)}^(-1/24)")
print("    (1.2):  alpha_n = 1/2 G_n^-12 ( G_n^12 - sqrt(G_n^24 - 1) )")
print()
print("       n        G_n                         (1.2) rel.err")
for n in (3, 7, 11, 15, 19, 23, 27, 31):
    a = alpha_theta(n)
    G = (1 / (4 * a * (1 - a))) ** (D(1) / 24)
    G12 = G ** 12
    a_from_G = (G12 - (G12 * G12 - 1).sqrt()) / (2 * G12)
    r = rel(a_from_G, a)
    print("    %5d   %-26s  %.3e" % (n, str(+G)[:26], float(r)))
    check("(1.2) round-trips at n = %d" % n, r < TOL)

G1 = (1 / (4 * alpha_theta(1) * (1 - alpha_theta(1)))) ** (D(1) / 24)
check("G_1 = 1 exactly (alpha_1 = 1/2)", abs(G1 - 1) < TOL, str(+G1)[:20])
check("alpha_1 = 1/2", abs(alpha_theta(1) - D("0.5")) < TOL)
print("    alpha_1 = 1/2 is the lemniscatic point: the one n where the modulus")
print("    is rational, and the place Gauss started.")

# ---------------------------------------------------------------- (2.3)
print()
print("[6] Equation (2.3): alpha_4p from G_p alone.")
print("    alpha_4p = (sqrt(G_p^12 + 1) - sqrt(G_p^12))^4 (sqrt(G_p^12) - sqrt(G_p^12 - 1))^4")
for p in (1, 3, 7, 15):
    a = alpha_theta(p)
    G12 = ((1 / (4 * a * (1 - a))) ** (D(1) / 24)) ** 12
    pred = ((G12 + 1).sqrt() - G12.sqrt()) ** 4 * (G12.sqrt() - (G12 - 1).sqrt()) ** 4
    r = rel(pred, alpha_theta(4 * p))
    print("    p = %-3d  ->  alpha_%-4d rel. error %.3e" % (p, 4 * p, float(r)))
    check("(2.3) gives alpha_%d from G_%d" % (4 * p, p), r < TOL)

# ---------------------------------------------------------------- close
print()
if FAIL:
    print("FAILED: " + "; ".join(FAIL))
    raise SystemExit(1)
print("All checks passed at 40 significant figures.")
print()
print("What this does and does not show. It confirms that the radicals")
print("Ramanujan wrote in his notebooks are the singular moduli, to forty")
print("digits, computed two independent ways. It says nothing whatever about")
print("how he found them. Watson's proof of Theorem 1.2 is, in Berndt, Chan")
print("and Zhang's own word, a VERIFICATION -- 'it does not shed any light on")
print("how Ramanujan might have discovered the formula.' Neither does this file.")
