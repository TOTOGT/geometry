#!/usr/bin/env python3
"""
ch-mirzakhani-verify.py -- every number on book7/ch-mirzakhani.html.

The Weil-Petersson volume polynomials are taken from the literature (Mirzakhani
2007; Do 2011, Table 1). This script does not derive them. What it does is check
them against EACH OTHER, using Do's identity

    dV_{g,n+1}/dL_{n+1} (L, 2 pi i) = 2 pi i (2g - 2 + n) V_{g,n}(L)

which relates volumes at different (g, n) and so cannot be satisfied by a
mistyped coefficient.

Blocks:
  [1] V_{0,4} -> V_{0,3}
  [2] V_{1,2} -> V_{1,1}, at several boundary lengths
  [3] V_{2,1} -> V_{2,0}, recovering 43 pi^6 / 2160
  [4] the /48 vs /24 convention for V_{1,1}, decided
  [5] the degree of each polynomial is 3g - 3 + n in the b_i^2
  [6] the numerical values quoted on the page

Standard library only.  Run:  python3 book7/ch-mirzakhani-verify.py
"""
import math, sys

FAIL = []
def check(label, ok, detail=""):
    print(("  PASS  " if ok else "  FAIL  ") + label + (("   " + detail) if detail else ""))
    if not ok: FAIL.append(label)

PI = math.pi
TPI = 2j * PI

V03 = lambda: 1.0
V11 = lambda b: (b*b + 4*PI**2) / 48
V04 = lambda b1, b2, b3, b4: 2*PI**2 + (b1*b1 + b2*b2 + b3*b3 + b4*b4)/2
V12 = lambda b1, b2: (4*PI**2 + b1*b1 + b2*b2) * (12*PI**2 + b1*b1 + b2*b2) / 192
V21 = lambda b: ((4*PI**2 + b*b) * (12*PI**2 + b*b)
                 * (6960*PI**4 + 384*PI**2*b*b + 5*b**4) / 2211840)
V20 = 43 * PI**6 / 2160

def ddx(f, x, h=1e-6):
    return (f(x + h) - f(x - h)) / (2*h)

print("=" * 70)
print("ch-mirzakhani-verify.py -- the volume polynomials, checked against each other")
print("=" * 70)

print("\n[1] Do's identity: V_{0,4} -> V_{0,3}   (g=0, n=3)")
for L in [(1.3, 0.7, 2.1), (0.0, 0.0, 0.0), (5.0, 0.1, 3.3)]:
    lhs = ddx(lambda x: V04(L[0], L[1], L[2], x), TPI)
    rhs = TPI * (2*0 - 2 + 3) * V03()
    check("L = %s   residual %.2e" % (str(L), abs(lhs - rhs)), abs(lhs - rhs) < 1e-9,
          "lhs %s" % lhs)

print("\n[2] Do's identity: V_{1,2} -> V_{1,1}   (g=1, n=1)")
for b in (0.0, 1.3, 2.7, 6.5):
    lhs = ddx(lambda x: V12(b, x), TPI)
    rhs = TPI * (2*1 - 2 + 1) * V11(b)
    check("b = %.1f   residual %.2e   (V_{1,1} = %.9f)" % (b, abs(lhs - rhs), V11(b).real
          if isinstance(V11(b), complex) else V11(b)), abs(lhs - rhs) < 1e-10)

print("\n[3] Do's identity: V_{2,1} -> V_{2,0}   (g=2, n=0)")
lhs = ddx(V21, TPI)
implied = lhs / (TPI * (2*2 - 2 + 0))
check("implied V_{2,0} = %.12f" % implied.real, abs(implied - V20) < 1e-9,
      "43 pi^6 / 2160 = %.12f, residual %.2e" % (V20, abs(implied - V20)))
check("and the imaginary part vanishes", abs(implied.imag) < 1e-9, "%.2e" % implied.imag)

print("\n[4] the /48 vs /24 convention")
b = 1.7
lhs = ddx(lambda x: V12(b, x), TPI)
r48 = abs(lhs - TPI * 1 * ((b*b + 4*PI**2)/48))
r24 = abs(lhs - TPI * 1 * ((b*b + 4*PI**2)/24))
check("with /48 the residual is %.2e" % r48, r48 < 1e-10)
check("with /24 the residual is %.2f" % r24, r24 > 1.0,
      "not a rounding difference -- a wrong answer")
check("the identity therefore selects /48", r48 < 1e-10 < 1.0 < r24)

print("\n[5] degrees: V_{g,n} has degree 3g-3+n in the b_i^2")
def deg_in_bsq(f, nvar, gn):
    # fit: evaluate at b^2 = t and difference until constant
    vals = [f(*( [math.sqrt(t)] * nvar )) for t in range(1, 12)]
    d = vals
    k = 0
    while len(d) > 1 and max(abs(x) for x in d) > 1e-6:
        d = [d[i+1] - d[i] for i in range(len(d)-1)]
        k += 1
        if k > 8: break
    return k - 1
for name, f, nvar, g, n in [("V_{1,1}", lambda b: V11(b), 1, 1, 1),
                            ("V_{0,4}", lambda *b: V04(*b), 4, 0, 4),
                            ("V_{1,2}", lambda *b: V12(*b), 2, 1, 2),
                            ("V_{2,1}", lambda b: V21(b), 1, 2, 1)]:
    want = 3*g - 3 + n
    got = deg_in_bsq(f, nvar, (g, n))
    check("%s has degree %d in b^2" % (name, got), got == want, "3g-3+n = %d" % want)

print("\n[6] the values printed on the page")
check("V_{1,1}(0) = pi^2/12 = 0.822467033424", abs(V11(0.0) - PI**2/12) < 1e-15,
      "%.12f" % V11(0.0))
check("V_{0,4}(0,0,0,0) = 2 pi^2 = 19.739208802179",
      abs(V04(0,0,0,0) - 2*PI**2) < 1e-12, "%.12f" % V04(0,0,0,0))
check("V_{2,0} = 43 pi^6/2160 = 19.138766353582", abs(V20 - 19.138766353582) < 1e-11,
      "%.12f" % V20)
check("V_{0,3} = 1", V03() == 1.0)

print("\n" + "=" * 70)
print("[HONESTY]")
print("=" * 70)
print("""  What this establishes. The five volume polynomials quoted on the page are
  mutually consistent under Do's identity, which relates volumes at DIFFERENT
  (g, n). A transcription error in any one coefficient would break the
  identity, so this is a real check on the page's numbers and not a tautology.
  Block [4] is the useful one: it decides, from the polynomials themselves,
  which of the two conventions in the literature for V_{1,1} the rest of the
  page is using.

  What it does not establish. The polynomials are QUOTED, not derived.
  Mirzakhani's recursion is not implemented here and nothing in this script
  proves any of the volumes from first principles. Do's identity is itself a
  theorem of Do's, cited, and is used here as a consistency relation.

  Nothing here touches the geodesic counting theorem. s_X(L) ~ c_X L^{6g-6+2n}
  is an asymptotic statement about a hyperbolic surface, not an arithmetic one,
  and no finite computation on these polynomials bears on it. The page states
  it with its citation and this script leaves it alone.

  Derivatives are central differences with h = 1e-6 evaluated in the complex
  plane, so the residuals near 1e-13 are the differencing error, not a
  measurement of how well the identity holds. The comparison that matters is
  between 1e-13 and 5.55 in block [4], and that gap is far outside any
  numerical artefact.""")

print()
if FAIL:
    print("FAILED: %d" % len(FAIL))
    for f in FAIL: print("   " + f)
    sys.exit(1)
print("All blocks pass.")
