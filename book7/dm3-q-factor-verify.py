#!/usr/bin/env python3
"""
dm3-q-factor-verify.py  --  the quality factor the corpus never computed.

Standard library only. Everything here is arithmetic on objects already
established in this corpus; nothing is imported from outside it.

Established elsewhere and used as input:
  * dm3 toy model on M = R^2_{>0} x R, alpha = dz - r^2 dtheta.
  * Gamma = {r = 1} is a HELIX, not a closed orbit: zdot = 1 on Gamma.
    (book7/ch-grothendieck.html, block [4])
  * One-turn (T* = 2 pi) monodromy exponent of the transverse direction:
        E(z0) = -4 pi + 2 exp(-z0) (1 - exp(-2 pi))
  * z_c = ln( (1 - exp(-2 pi)) / (2 pi) ) = -1.839746254986, the height at
    which E changes sign.  (docs/v4-predeposit-checklist.md, item 12)

What is NEW here is one division. The corpus has computed decay RATES
everywhere and has never once divided one by its period. Doing so turns a
sign change into a pole, and gives the flow a quantity acoustics has had
since Sabine: a quality factor.
"""

import math

PI   = math.pi
K    = 1.0 - math.exp(-2.0 * PI)          # 1 - e^{-2pi}
Z_C  = math.log(K / (2.0 * PI))
FAIL = []

def check(name, ok, detail=""):
    print(("  PASS  " if ok else "  FAIL  ") + name + (("   " + detail) if detail else ""))
    if not ok:
        FAIL.append(name)

def E(z):
    "one-turn monodromy exponent of the transverse direction"
    return -4.0 * PI + 2.0 * math.exp(-z) * K

# ----------------------------------------------------------------------------
print("[1] z_c is not a sign change. It is a pole.")
print("    Logarithmic decrement per turn: Lambda(z) = |E(z)|.")
print("    Quality factor of a decaying oscillator: Q = pi / Lambda.")
print()
# Written first as 0.9981345 from memory and wrong in the sixth digit; the
# machine value is 0.998132557. Corrected rather than the tolerance widened.
check("K = 1 - e^{-2pi} is 0.998132557", abs(K - 0.998132557) < 1e-9, "%.9f" % K)
check("z_c = -1.839746254986", abs(Z_C - (-1.839746254986)) < 1e-11, "%.12f" % Z_C)
check("E(z_c) vanishes to machine precision", abs(E(Z_C)) < 1e-12, "%.3e" % abs(E(Z_C)))
print()
print("    Exactly: E(z) = 0  <=>  2 e^{-z} K = 4 pi  <=>  e^{-z} = 2 pi / K")
print("                        <=>  z = ln( K / (2 pi) ) = z_c.")
print("    So Lambda(z_c) = 0 and Q(z_c) is infinite. Not large. Infinite.")

def Q(z):
    L = abs(E(z))
    return math.inf if L == 0.0 else PI / L

print()
print("        z            E(z)         Lambda          Q         regime")
for z in (-4.0, -3.0, -2.2453, Z_C, -1.1466, 0.0, 1.0, 5.0, 20.0):
    q = Q(z)
    reg = ("growing" if E(z) > 0 else "decaying")
    reg += (", underdamped" if q > 0.5 else ", overdamped")
    print("  %9.4f  %13.6f  %11.6f  %9.4f   %s"
          % (z, E(z), abs(E(z)), q, reg))

check("below z_c the exponent is positive (amplifying)", E(Z_C - 0.5) > 0, "%.4f" % E(Z_C-0.5))
check("above z_c the exponent is negative (decaying)",  E(Z_C + 0.5) < 0, "%.4f" % E(Z_C+0.5))

# ----------------------------------------------------------------------------
print()
print("[2] The resonance band has width exactly ln 3.")
print("    Underdamped means Q > 1/2, i.e. Lambda < 2 pi, i.e. |E| < 2 pi:")
print("        -2pi < -4pi + 2 K e^{-z} < 2pi")
print("          pi/K  <   e^{-z}   <  3 pi/K")
print("    so z runs from -ln(3 pi / K) to -ln(pi / K), and the width is")
print("        ln(3 pi / K) - ln(pi / K) = ln 3,")
print("    with K cancelling. The band width does not depend on the model's")
print("    only constant. It is ln 3 and it could not have been anything else.")
print()
z_lo = -math.log(3.0 * PI / K)
z_hi = -math.log(PI / K)
width = z_hi - z_lo
print("    band: z in (%.6f, %.6f),  width = %.12f,  ln 3 = %.12f"
      % (z_lo, z_hi, width, math.log(3.0)))
check("the underdamped band width is exactly ln 3",
      abs(width - math.log(3.0)) < 1e-14, "%.3e off" % abs(width - math.log(3.0)))
check("Q exceeds 1/2 strictly inside the band and not outside",
      Q(z_lo + 1e-9) > 0.5 and Q(z_hi - 1e-9) > 0.5
      and Q(z_lo - 1e-6) < 0.5 and Q(z_hi + 1e-6) < 0.5)
check("z_c lies inside the band", z_lo < Z_C < z_hi,
      "%.4f < %.4f < %.4f" % (z_lo, Z_C, z_hi))

print()
print("    z_c is NOT the midpoint in z. It is the midpoint in e^{-z}, which is")
print("    the coordinate the flow actually moves in:")
mid_u = 0.5 * (PI / K + 3.0 * PI / K)
print("      e^{-z_lo} = %.6f,  e^{-z_hi} = %.6f,  midpoint = %.6f"
      % (math.exp(-z_lo), math.exp(-z_hi), mid_u))
print("      e^{-z_c}  = %.6f" % math.exp(-Z_C))
check("z_c is the exact midpoint of the band in e^{-z}",
      abs(math.exp(-Z_C) - mid_u) < 1e-12, "%.3e off" % abs(math.exp(-Z_C) - mid_u))
check("the band is 2 pi / K wide in e^{-z}",
      abs((3*PI/K - PI/K) - 2*PI/K) < 1e-12)

# ----------------------------------------------------------------------------
print()
print("[3] Everywhere else, dm3 does not ring at all.")
Q_inf = PI / (4.0 * PI)
print("    As z -> +infinity, E -> -4 pi and Q -> pi/(4 pi) = 1/4 exactly.")
check("the asymptotic quality factor is exactly 1/4",
      abs(Q_inf - 0.25) < 1e-15, "%.15f" % Q_inf)
check("Q at z = 20 has already reached 1/4 to 10 digits",
      abs(Q(20.0) - 0.25) < 1e-10, "%.12f" % Q(20.0))
amp = math.exp(-4.0 * PI)
print("    Amplitude ratio over one full turn at large z: e^{-4pi} = %.6e" % amp)
print("    That is a factor of %.0f. The transverse direction is gone before" % (1.0/amp))
print("    the helix has finished a single revolution.")
check("one turn at large z costs more than five orders of magnitude",
      amp < 1e-5, "%.3e" % amp)
print()
print("    Q = 1/4 is a formal number: the pi/Lambda formula means something only")
print("    when Lambda is small, and Lambda = 4 pi is not small. The honest reading")
print("    is not 'a bad oscillator'. It is 'not an oscillator'. Above the band")
print("    there is no ringing mode to speak of, and the only place in the whole")
print("    flow where the lightly-damped formula is even valid is the band itself.")
print("    Which is exactly where Q blows up.")

# ----------------------------------------------------------------------------
print()
print("[4] What this says next to a room.")
LN10 = math.log(10.0)
def Qroom(f, T): return PI * f * T / (3.0 * LN10)
q_hyp = Qroom(63.0, 14.62)
print("    Hal Saflieni Hypogeum, 63 Hz band (Till, T20 = 14.62 s):  Q = %.1f" % q_hyp)
print("    dm3 helix, asymptotic:                                    Q = %.2f" % Q_inf)
print("    ratio: %.3e" % (q_hyp / Q_inf))
check("a neolithic tomb outperforms the corpus's flagship orbit by 1000x",
      q_hyp / Q_inf > 1000.0, "%.0fx" % (q_hyp / Q_inf))
print()
print("    And the structural echo, which is the point of computing this at all:")
print("      In the Hypogeum, Q is FLAT across the two lowest octaves (419, 416)")
print("      because the loss per cycle is set by the boundary and nothing else.")
print("      In dm3, Q is FLAT at 1/4 for all large z, because -4 pi is the")
print("      z-independent part of the exponent -- the geometry -- and the")
print("      2 e^{-z} K part, the state-dependent part, has died away.")
print("      Same split, same signature: a constant loss per cycle is a boundary.")
print()
print("      The echea condition -- internal loss exactly equal to radiation loss,")
print("      which is where a resonator's absorption cross-section is maximal --")
print("      is Lambda = 0 read in the other direction. Critical coupling and z_c")
print("      are the same condition written in two vocabularies.")

# ----------------------------------------------------------------------------
print()
if FAIL:
    print("FAILED: " + "; ".join(FAIL))
    raise SystemExit(1)
print("All checks passed.")
print("New here: Q(z), the ln 3 band width, and z_c as a pole rather than a sign.")
print("Everything else was already in the corpus and had simply never been divided")
print("by its period.")
