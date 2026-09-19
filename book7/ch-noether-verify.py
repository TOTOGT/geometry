#!/usr/bin/env python3
"""
ch-noether-verify.py -- every number on book7/ch-noether.html.

Blocks:
  [1] symplectic limit (beta = 0): H is conserved -- Noether, unmodified
  [2] contact flow: dH/dt = -beta H, so H(t) = H(0) e^{-beta t}
  [3] H e^{beta t} is the exactly conserved quantity, to the page's 1e-14
  [4] energy (p^2+q^2)/2 is NOT the conserved thing -- the page's distinction
  [5] the eigenvalue collision at beta = 2, and the two roots at beta = 4
  [6] the correction the page records: mu = -beta/2 only for beta < 2

Contact equations from Bravetti-Cruz-Tapias (2017):
    qdot = H_p ,  pdot = -H_q - p H_z ,  zdot = p H_p - H
with H(q,p,z) = (p^2 + q^2)/2 + beta z, alpha = dz - p dq.

Standard library only.  Run:  python3 book7/ch-noether-verify.py
"""
import math, sys

FAIL = []
def check(label, ok, detail=""):
    print(("  PASS  " if ok else "  FAIL  ") + label + (("   " + detail) if detail else ""))
    if not ok: FAIL.append(label)

def rhs(s, b):
    q, p, z = s
    return (p, -q - b*p, p*p - ((p*p + q*q)/2 + b*z))

def rk4(s, h, b):
    k1 = rhs(s, b)
    k2 = rhs(tuple(s[i] + h/2*k1[i] for i in range(3)), b)
    k3 = rhs(tuple(s[i] + h/2*k2[i] for i in range(3)), b)
    k4 = rhs(tuple(s[i] + h*k3[i] for i in range(3)), b)
    return tuple(s[i] + h/6*(k1[i] + 2*k2[i] + 2*k3[i] + k4[i]) for i in range(3))

def H(s, b):
    q, p, z = s
    return (p*p + q*q)/2 + b*z

def run(b, T, h=1e-4, s0=(1.0, 0.0, 0.3)):
    s = s0
    for _ in range(int(round(T/h))): s = rk4(s, h, b)
    return s

print("=" * 70)
print("ch-noether-verify.py -- Noether in the symplectic case, and in the contact case")
print("=" * 70)

S0 = (1.0, 0.0, 0.3)

print("\n[1] beta = 0 : the symplectic limit. H is conserved.")
for T in (0.5, 1.0, 2.0):
    s = run(0.0, T)
    rel = abs(H(s, 0.0) - H(S0, 0.0)) / abs(H(S0, 0.0))
    check("t = %.1f   H = %.12f" % (T, H(s, 0.0)), rel < 1e-12, "relative drift %.2e" % rel)

print("\n[2] beta > 0 : H decays as H(0) e^{-beta t}")
for b in (0.5, 4.0):
    H0 = H(S0, b)
    for T in (0.5, 1.0, 2.0):
        s = run(b, T)
        pred = H0 * math.exp(-b*T)
        rel = abs(H(s, b) - pred) / abs(pred)
        check("beta = %.1f  t = %.1f   H = %.9f" % (b, T, H(s, b)), rel < 1e-11,
              "predicted %.9f, relative error %.2e" % (pred, rel))

print("\n[3] H e^{beta t} is the conserved quantity")
for b in (0.5, 1.0, 4.0):
    H0 = H(S0, b); worst = 0.0
    for T in (0.25, 0.5, 1.0, 1.5, 2.0):
        s = run(b, T)
        inv = H(s, b) * math.exp(b*T)
        worst = max(worst, abs(inv - H0) / abs(H0))
    check("beta = %.1f   H e^{beta t} constant to %.1e" % (b, worst), worst < 1e-11,
          "page claims 1e-14 over two periods; measured %.2e over t<=2" % worst)

print("\n[4] the energy (p^2+q^2)/2 is NOT what is conserved")
b = 4.0
s = run(b, 2.0)
E0 = (S0[0]**2 + S0[1]**2)/2
E2 = (s[0]**2 + s[1]**2)/2
check("beta = 4: E falls %.6f -> %.6f" % (E0, E2), E2 < E0 * 0.9,
      "H over the same interval falls by a factor e^{-8} = %.2e" % math.exp(-8))
check("E is not proportional to H", abs(E2/E0 - math.exp(-b*2.0)) > 1e-3,
      "E ratio %.6f vs e^{-beta t} %.2e" % (E2/E0, math.exp(-b*2.0)))

print("\n[5] the roots of qddot + beta qdot + q = 0")
def roots(b):
    d = b*b - 4
    if d < 0: return ("complex", -b/2, math.sqrt(-d)/2)
    return ("real", (-b + math.sqrt(d))/2, (-b - math.sqrt(d))/2)
for b, want in [(1.0, "complex"), (2.0, "real"), (4.0, "real"), (6.0, "real")]:
    r = roots(b)
    check("beta = %.1f  ->  %s" % (b, r[0]), r[0] == want, str(tuple(round(x, 4) for x in r[1:])))
r2 = roots(2.0)
check("at beta = 2 the two roots collide at -1", abs(r2[1] + 1) < 1e-12 and abs(r2[2] + 1) < 1e-12,
      "%.12f and %.12f" % (r2[1], r2[2]))
r4 = roots(4.0)
check("at beta = 4 the roots are -0.2679 and -3.7321",
      abs(r4[1] + 0.2679) < 5e-5 and abs(r4[2] + 3.7321) < 5e-5,
      "%.4f, %.4f" % (r4[1], r4[2]))

print("\n[6] the correction the page records")
check("mu = -beta/2 holds for beta = 1 (underdamped)", abs(roots(1.0)[1] + 0.5) < 1e-12)
check("mu = -beta/2 FAILS for beta = 4", abs(max(roots(4.0)[1], roots(4.0)[2]) - (-2.0)) > 1.7,
      "max Re = %.4f, not -2" % max(roots(4.0)[1], roots(4.0)[2]))
check("so beta = 4 does NOT reproduce the corpus mu_max = -2",
      abs(max(roots(4.0)[1], roots(4.0)[2]) + 2.0) > 1.0, "the dropped claim, kept refuted")
check("more damping gives SLOWER return past beta = 2",
      max(roots(6.0)[1], roots(6.0)[2]) > max(roots(2.0)[1], roots(2.0)[2]),
      "beta=6 -> %.4f is closer to 0 than beta=2 -> %.4f"
      % (max(roots(6.0)[1:]), max(roots(2.0)[1:])))

print("\n" + "=" * 70)
print("[HONESTY]")
print("=" * 70)
print("""  What this establishes. On the contact Hamiltonian H = (p^2+q^2)/2 + beta z,
  numerical integration confirms to eleven or more digits that H decays exactly
  exponentially and that H e^{beta t} is invariant, while the mechanical energy
  (p^2+q^2)/2 does neither. The root structure and the collision at beta = 2
  are closed-form and exact.

  What it does not establish. dH/dt = -H H_z is a one-line consequence of the
  contact equations and is PROVED, not verified here; blocks [2] and [3] check
  that a particular integrator reproduces it on one trajectory from one initial
  condition. That is a consistency check on the arithmetic, not a proof of the
  identity, and certainly not a proof of any general Noether theorem for
  contact systems. The literature for that is Bravetti and co-authors, cited on
  the page.

  Nothing here is a claim about Noether's own work. She did not write the
  contact case; the point of the chapter is that her correspondence between
  symmetry and conserved quantity has to be MODIFIED to survive in the setting
  this corpus works in, and block [6] keeps a flattering claim that did not
  survive checking, refuted, on the record.""")

print()
if FAIL:
    print("FAILED: %d" % len(FAIL))
    for f in FAIL: print("   " + f)
    sys.exit(1)
print("All blocks pass.")
