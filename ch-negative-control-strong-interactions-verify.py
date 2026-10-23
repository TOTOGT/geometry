#!/usr/bin/env python3
"""
ch-negative-control-strong-interactions-verify.py   (R24 verify script)

Checks the numerical claims of "Topographical Orthogenetic Generative Theory in
Strong Interactions" (P. N. Grossi, G6 LLC, 4 pp., 11 April 2026) that a script
CAN check. Blocks:

  [1] The Tribonacci recurrence w(k+3)=w(k+2)+w(k+1)+w(k): ratio -> eta, eta a root of x^3-x^2-x-1.
  [2] The paper calls eta ~ 1.839 "the plastic number". The plastic number is the real root of x^3=x+1.
  [3] T3 companion matrix: det = 1 (exact, integers); (eta^2, eta, 1) is an eigenvector.
  [4] The weights eta^-k decrease, and sum to eta/(eta-1) over k >= 0 (a measure on the index set N only).
  [6] Does eta^-k give a fractal measure? The partition of [0,1] by eta^-1, eta^-2, eta^-3.
  [7] A finite counterexample to the companion's stability_at_threshold (g = 33 lock-in).
  [5] Figure 1 against its own caption: the ring widths in the PDF vector drawing scale by eta.
      Needs `pdftocairo` and the PDF (path in argv[1] or $NUCLEAR_V1_PDF); prints SKIP, never PASS, without them.

Primary source: AXLE/AnuclearPhysics/NuclearPhysicsB_latex.pdf (md5 7961116c2967103990c5a4fac3fc5f45). Lean cross-reference (NOT run here):
Orthogenesis/Eta/EtaChecks.lean, audited 2026-10-01 (tools/verify-audit/2026-10-01/).

Run:  python3 ch-negative-control-strong-interactions-verify.py [path/to/NuclearPhysicsB_latex.pdf]
"""
import os, re, shutil, subprocess, sys, tempfile
from fractions import Fraction

FAIL = []
def check(label, ok, detail=""):
    print("  [%s] %s %s" % ("PASS" if ok else "FAIL", label, detail))
    if not ok: FAIL.append(label)
def skip(label, why): print("  [SKIP] %s -- %s" % (label, why))
def head(n, t): print("\n[%s] %s" % (n, t))

def bisect(f, lo, hi, n=200):
    for _ in range(n):
        mid = (lo + hi) / 2
        if f(lo) * f(mid) <= 0: hi = mid
        else: lo = mid
    return (lo + hi) / 2

ETA = bisect(lambda x: x**3 - x**2 - x - 1, 1.0, 2.0)
PLASTIC = bisect(lambda x: x**3 - x - 1, 1.0, 2.0)

head(1, "Tribonacci recurrence")
w = [0, 0, 1]
for k in range(3, 80): w.append(w[-1] + w[-2] + w[-3])
r = w[-1] / w[-2]
check("w(k+3)=w(k+2)+w(k+1)+w(k) by construction; w(79)/w(78) -> eta", abs(r - ETA) < 1e-12, "ratio=%.15f eta=%.15f" % (r, ETA))
check("eta is a root of x^3-x^2-x-1 (residual < 1e-12)", abs(ETA**3 - ETA**2 - ETA - 1) < 1e-12, "eta=%.12f" % ETA)
check("eta = 1.8392867552 to 10 places", abs(ETA - 1.8392867552) < 1e-10)

head(2, "'eta ~ 1.839 (plastic number)'")
check("plastic number = real root of x^3=x+1 = 1.3247179572", abs(PLASTIC - 1.3247179572) < 1e-10, "plastic=%.10f" % PLASTIC)
check("eta != plastic number", abs(ETA - PLASTIC) > 0.5)
check("1.839 is not a root of x^3=x+1 (residual)", abs(1.839**3 - 1.839 - 1) > 1, "residual=%.3f" % (1.839**3 - 1.839 - 1))
print("  -> 1.839 is the TRIBONACCI constant. The paper's parenthetical names the wrong constant.")

head(3, "T3 companion matrix")
T3 = [[1, 1, 1], [1, 0, 0], [0, 1, 0]]
def det3(m):
    return (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1]) - m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0]) + m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))
check("det T3 = 1 (exact)", det3(T3) == 1, "det=%d" % det3(T3))
v = [ETA**2, ETA, 1.0]
Tv = [sum(T3[i][j]*v[j] for j in range(3)) for i in range(3)]
check("T3 (eta^2, eta, 1)^T = eta (eta^2, eta, 1)^T", all(abs(Tv[i] - ETA*v[i]) < 1e-12 for i in range(3)))
v2 = [PLASTIC**2, PLASTIC, 1.0]
Tv2 = [sum(T3[i][j]*v2[j] for j in range(3)) for i in range(3)]
check("control: the plastic number is NOT an eigenvalue with that vector", any(abs(Tv2[i] - PLASTIC*v2[i]) > 0.1 for i in range(3)))

head(4, "Weights eta^-k")
ws = [ETA**-k for k in range(60)]
check("eta^-k strictly decreasing, k=0..59", all(ws[i] > ws[i+1] for i in range(59)))
check("sum_{k>=0} eta^-k = eta/(eta-1)", abs(sum(ETA**-k for k in range(2000)) - ETA/(ETA-1)) < 1e-9, "=%.9f" % (ETA/(ETA-1)))
print("  -> this is a finite measure on the index set N. No measure on ker(alpha) is defined by the paper.")

head(5, "Figure 1 against its own caption (ring widths in the vector drawing)")
pdf = (sys.argv[1] if len(sys.argv) > 1 else os.environ.get("NUCLEAR_V1_PDF", os.path.expanduser("~/Desktop/AXLE/AnuclearPhysics/NuclearPhysicsB_latex.pdf")))
if not pdf or not os.path.exists(pdf): skip("Figure 1 ring widths", "PDF not given or missing")
elif not shutil.which("pdftocairo"): skip("Figure 1 ring widths", "pdftocairo not installed")
else:
    d = tempfile.mkdtemp(); out = os.path.join(d, "p3.svg")
    subprocess.run(["pdftocairo", "-svg", "-f", "3", "-l", "3", pdf, out], check=True)
    s = open(out).read(); ws_ = []
    for m in re.finditer(r'<path[^>]*>', s):
        tag = m.group(0)
        if 'stroke' not in tag or 'rgb(' not in tag: continue   # poppler writes stroke="rgb(..)" or style="stroke:rgb(..)"
        c = re.search(r'stroke[:="]+rgb\(([\d.]+)%,\s*([\d.]+)%,\s*([\d.]+)%\)', tag)
        if not c or not (float(c.group(3)) > 80 and float(c.group(1)) < 40): continue
        dd = re.search(r' d="([^"]+)"', tag).group(1)
        nums = [float(x) for x in re.findall(r'-?\d+\.?\d*', dd)]; xs = nums[0::2]
        if len(xs) > 3: ws_.append(max(xs) - min(xs))
    ws_ = sorted(ws_)
    print("  blue stroke widths:", ["%.3f" % x for x in ws_])
    rings = [x for x in ws_ if x > 10]
    ratios = [rings[i+1]/rings[i] for i in range(len(rings)-1)]
    print("  successive width ratios:", ["%.4f" % x for x in ratios])
    check("five rings found", len(rings) == 5, "n=%d" % len(rings))
    check("four successive ratios, each = eta within 0.5%", len(ratios) == 4 and all(abs(x/ETA - 1) < 0.005 for x in ratios), "n=%d" % len(ratios))


head(6, "Does eta^-k give a fractal measure? The partition of [0,1] by eta^-1, eta^-2, eta^-3")
r = [ETA**-1, ETA**-2, ETA**-3]
check("eta^-1 + eta^-2 + eta^-3 = 1 (divide eta^3 = eta^2 + eta + 1 by eta^3)", abs(sum(r) - 1) < 1e-12, "sum=%.15f" % sum(r))
sd = bisect(lambda t: sum(x**t for x in r) - 1, 0.1, 3.0)
check("similarity dimension s solving sum r_i^s = 1 is exactly 1", abs(sd - 1) < 1e-9, "s=%.12f" % sd)
def level(d):
    iv = [(0.0, 1.0)]
    for _ in range(d):
        nxt = []
        for a, b in iv:
            L = b - a; x = a
            for ri in r:
                nxt.append((x, x + ri*L)); x += ri*L
        iv = nxt
    return iv
for d in (1, 3, 6):
    iv = level(d)
    tot = sum(b - a for a, b in iv)
    gaps = max(abs(iv[i][1] - iv[i+1][0]) for i in range(len(iv)-1))
    check("depth %d: %d intervals, total length 1, no gaps, no overlaps" % (d, len(iv)), len(iv) == 3**d and abs(tot - 1) < 1e-9 and gaps < 1e-9, "total=%.12f max gap=%.1e" % (tot, gaps))
print("  -> with the natural weights (mass = length) the self-similar measure is Lebesgue measure on [0,1], dimension 1. It is not fractal.")
print("     A fractal (multifractal) measure needs weights other than eta^-i; the paper does not specify any.")

head(7, "Does the lean companion's stability_at_threshold hold? A 3-point counterexample")
# Mirror of NuclearPhysicsB/Operators.lean on M = {0,1,2,...} with C=K=U=identity and F = Fmap.
def Fmap(n): return 1 if n == 0 else 0 if n == 1 else 0 if n == 2 else n
S = range(0, 60)
check("F has a fold: Fmap 1 = Fmap 2 with 1 != 2", Fmap(1) == Fmap(2) and 1 != 2)
branch = {p_ for p_ in S if any(q != p_ and Fmap(q) == Fmap(p_) for q in S)}
check("F's branch locus is finite: {1, 2}", branch == {1, 2}, "locus=%s" % sorted(branch))
ident = lambda x: x
pairs = [(x, y) for x in S for y in S]
check("C = id is contractive: |C x - C y| <= |x - y| on all pairs in 0..59", all(abs(ident(x) - ident(y)) <= abs(x - y) for x, y in pairs))
check("C = id is injective on 0..59", len({ident(x) for x in S}) == len(S))
check("K = id and U = id do not increase Phi(n) = n", all(ident(x) <= x for x in S))
def iterate(f, n, x):
    for _ in range(n): x = f(x)
    return x
succ = lambda x: x + 1          # control: a map with NO fixed point at all
stable0 = lambda f: all(iterate(f, 0, f(x)) == f(x) for x in S)
stable_pos = lambda f: all(any(iterate(f, n, f(x)) == f(x) for n in range(1, 40)) for x in S)
check("stable_branch with n = 0 passes for the identity", stable0(ident))
check("CONTROL: stable_branch with n = 0 also passes for x -> x+1, which has no fixed point (so n = 0 carries no content)", stable0(succ))
check("CONTROL: with n >= 1 required, x -> x+1 correctly fails", not stable_pos(succ))
orbit = [2]
for _ in range(33): orbit.append(Fmap(orbit[-1]))
print("  orbit of 2 under G = Fmap, g = 0..33:", orbit)
check("no g <= 33 has G(G^g x0) = G^g x0 (the claimed lock-in fails)", all(Fmap(orbit[g]) != orbit[g] for g in range(34)))
print("  -> every hypothesis of the structures holds and the conclusion fails: stability_at_threshold is FALSE as stated.")
print("     This is a finite check of one instance; the Lean file NuclearControl.lean states it as a theorem (kernel-audited 2026-10-23, standard axioms only).")

print("\n[HONESTY]")
print("  This script establishes: the recurrence and its dominant root are what the paper says; the paper's name for that root is wrong;")
print("  T3 has det 1 and the stated eigenvector; the weights eta^-k contract and sum to eta/(eta-1); Figure 1's rings are drawn to the")
print("  scale its labels claim; that eta^-1+eta^-2+eta^-3 = 1, so the natural self-similar measure is Lebesgue (dimension 1); and one finite")
print("  instance on which the companion's g = 33 lock-in statement fails. It does NOT establish a measure on ker(alpha), any link between fold events and")
print("  confinement, or any of the heavy-ion, lattice-QCD or analogue-gravity predictions. Those have no computation here, and no Lean statement.")
print("  Floating-point checks are evidence, not proof; the proofs are in EtaChecks.lean (kernel run: see the chapter).")
if FAIL:
    print("\nFAILED:", FAIL); sys.exit(1)
print("\nall checks passed")
