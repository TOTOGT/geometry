#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book18/ch02-verify.py -- every number on book18/ch02-the-rule-itself.html. Run first (R24).

    python3 book18/ch02-verify.py [--downloads DIR]

  [1] the three held statements, verbatim: Knill Unit 10, Deisenroth (5.48) p.148,
      Loomis & Sternberg Theorem 6.2 p.143-144
  [2] the rule checked numerically on two maps of the plane, both orders
  [3] the gap in the cancellation proof: g(x) = x^2 sin(1/x) returns H = 0 infinitely often
  [4] the corpus's own chain, AMonster/dm3_operators.lean: Jacobians of C3, K3, F3, U3,
      the Jacobian of G3 as their product, and which non-commutations the derivative sees
  [HONESTY]
"""
import math, os, re, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def dl():
    if "--downloads" in sys.argv: return Path(sys.argv[sys.argv.index("--downloads") + 1])
    for c in ("~/mnt/Downloads", "~/Downloads"):
        p = Path(os.path.expanduser(c))
        if p.is_dir(): return p
DL = dl()
def pages(n):
    try: return subprocess.run(["pdftotext", "-layout", str(DL / n), "-"], capture_output=True, text=True, timeout=150).stdout.split("\f")
    except Exception: return None
flat = lambda s: re.sub(r"\s+", " ", s)

print("[1] the held statements")
K = pages("math1a_2021.pdf")
if K:
    k = flat(K[40])
    check("Knill, Unit 10: 'Unit 10: Chain rule' and the pain rule", "Unit 10: Chain rule" in k and "pain rule" in k)
    check("Knill's sketch divides by H and lets H -> 0", "we also have H → 0" in k)
D = pages("MATHEMATICS FOR MACHINE LEARNING.pdf")
if D:
    d = flat(D[153])
    check("Deisenroth p.148: chain rule (5.48)", d.strip().startswith("148") and "Chain rule:" in d)
    check("Deisenroth p.148 margin: 'not mathematically correct since the partial derivative is not a fraction'", all(x in d for x in ("This is only an", "intuition, but not", "mathematically", "correct since the", "partial derivative is", "not a fraction")))
L = pages("Advanced_Calculus.pdf")
if L:
    a, b = flat(L[154]), flat(L[155])
    check("Loomis & Sternberg Theorem 6.2 (p.143): the composite-function rule", "Theorem 6.2" in a and "composite-function rule" in a)
    check("its proof (p.144) never divides: it ends in dG_F(a) o dF_a", b.strip().startswith("144") and "dGF(a) 0 dFa" in b)

print("[2] two maps of the plane")
f = lambda v: (v[0] ** 2 - v[1], math.sin(v[0] * v[1]))
g = lambda v: (v[0] + 2 * v[1], v[0] * v[1] ** 2)
def jac(h, v, e=1e-6):
    cols = []
    for j in range(2):
        vp = list(v); vm = list(v); vp[j] += e; vm[j] -= e
        cols.append([(a - b) / (2 * e) for a, b in zip(h(vp), h(vm))])
    return [[cols[j][i] for j in range(2)] for i in range(2)]
mul = lambda A, B: [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
diff = lambda A, B: max(abs(A[i][j] - B[i][j]) for i in range(len(A)) for j in range(len(A[0])))
x = (0.7, -0.4)
fg = lambda v: f(g(v)); gf = lambda v: g(f(v))
check("d(f o g) at x = df at g(x) times dg at x", diff(jac(fg, x), mul(jac(f, g(x)), jac(g, x))) < 1e-6)
check("d(g o f) at x = dg at f(x) times df at x", diff(jac(gf, x), mul(jac(g, f(x)), jac(f, x))) < 1e-6)
gap = diff(jac(fg, x), jac(gf, x))
check("the two orders have different derivatives", gap > 0.1, f"max entry gap {gap:.3f}")

print("[3] the division in the cancellation proof")
gg = lambda t: t * t * math.sin(1 / t) if t else 0.0
zs = [gg(1 / (k * math.pi)) for k in range(1, 6)]
check("H = g(h) - g(0) is zero (to machine precision) at h = 1/(k pi), k = 1..5", all(abs(z) < 1e-15 for z in zs), str([f"{z:.1e}" for z in zs]))
F = lambda u: math.exp(u)
num = [(F(gg(h)) - F(gg(0))) / h for h in (1e-3, 1e-4, 1e-5)]
check("yet d/dx exp(g(x)) at 0 = exp(0) * g'(0) = 0, as the rule says", all(abs(v) < 2e-3 for v in num), str([f"{v:.1e}" for v in num]))

print("[4] the corpus's chain: AMonster/dm3_operators.lean")
src = (ROOT / "AMonster/dm3_operators.lean").read_text(encoding="utf-8")
check("the file defines G3 = U3 o F3 o K3 o C3", "U₃ r₀ ∘ F₃ κ ∘ K₃ ∘ C₃" in src)
check("C3: (r, th, z) -> (r, th, r^2 th)", "| (r, θ, _) => (r, θ, r ^ 2 * θ)" in src)
check("K3: z -> z + 1", "| (r, θ, z) => (r, θ, z + 1)" in src)
check("F3: r -> r below kappa, 2 kappa - r above", "(if r ≤ κ then r else 2 * κ - r, θ, z)" in src)
check("U3: r -> r0 + (r - r0) e^-1", "(r₀ + (r - r₀) * exp (-1), θ, z)" in src)
kap, r0 = 1.5, 1.0
C = lambda s: (s[0], s[1], s[0] ** 2 * s[1])
Kf = lambda s: (s[0], s[1], s[2] + 1)
Fo = lambda s: (s[0] if s[0] <= kap else 2 * kap - s[0], s[1], s[2])
U = lambda s: (r0 + (s[0] - r0) * math.exp(-1), s[1], s[2])
def J3(h, v, e=1e-6):
    cols = []
    for j in range(3):
        vp = list(v); vm = list(v); vp[j] += e; vm[j] -= e
        cols.append([(a - b) / (2 * e) for a, b in zip(h(vp), h(vm))])
    return [[cols[j][i] for j in range(3)] for i in range(3)]
G = lambda s: U(Fo(Kf(C(s))))
for s in ((1.0, 1.0, 0.0), (2.0, 0.5, 0.3)):
    s1 = C(s); s2 = Kf(s1); s3 = Fo(s2)
    prod = mul(J3(U, s3), mul(J3(Fo, s2), mul(J3(Kf, s1), J3(C, s))))
    check(f"at s = {s}: dG3 = dU3 dF3 dK3 dC3", diff(J3(G, s), prod) < 1e-5, f"dF3 radial = {J3(Fo, s2)[0][0]:+.0f}")
s = (1.0, 1.0, 0.0)
ck, kc = (lambda v: C(Kf(v))), (lambda v: Kf(C(v)))
check("C3 o K3 != K3 o C3 at (1,1,0), as the file proves", ck(s) != kc(s), f"{ck(s)} vs {kc(s)}")
check("but d(C3 o K3) = d(K3 o C3) everywhere sampled: dK3 = I and dC3 ignores z",
      all(diff(J3(ck, v), J3(kc, v)) < 1e-6 for v in ((1, 1, 0), (0.3, -2, 5), (2, 0.1, -1))))
cu, uc = (lambda v: C(U(v))), (lambda v: U(C(v)))
gapCU = diff(J3(cu, s), J3(uc, s))
check("d(C3 o U3) != d(U3 o C3): this non-commutation the derivative does see", gapCU > 0.1, f"gap {gapCU:.3f}")
lo = J3(Fo, (kap - 1e-3, 0, 0))[0][0]; hi = J3(Fo, (kap + 1e-3, 0, 0))[0][0]
check("F3 has slope +1 below kappa and -1 above: not differentiable at r = kappa", abs(lo - 1) < 1e-6 and abs(hi + 1) < 1e-6, f"{lo:+.3f}, {hi:+.3f}")

print("""
[HONESTY]
[1] finds sentences in text layers. [2]-[4] check the rule by central differences
(h = 1e-6), which is Deisenroth's own gradient check (p. 149), not a proof; the proof
is Loomis & Sternberg's. [4] reads the operator definitions from the Lean file and
re-implements them in Python at kappa = 1.5, r0 = 1; the Lean file proves the maps
differ, and nothing in it states or proves a derivative. The finding that dC3 and dK3
commute although C3 and K3 do not is computed here at three points and follows from
the definitions (dK3 = I, C3 independent of z); it is not a kernel-checked theorem.
""")
print(f"{len(FAIL)} FAIL")
sys.exit(1 if FAIL else 0)
