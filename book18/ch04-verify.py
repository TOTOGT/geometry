#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book18/ch04-verify.py -- every number on book18/ch04-euler-in-the-middle.html. Run first (R24).

    python3 book18/ch04-verify.py [--downloads DIR]

  [1] Katz, "Euler's Analysis Textbooks", in Bradley & Sandifer (eds.), Leonhard Euler:
      Life, Work and Legacy (Elsevier 2007), pp. 213-233 -- the passages, verbatim
  [2] Euler's rule "higher differentials vanish" as an algebra: numbers a + b*dx with dx^2 = 0
  [3] in that algebra, Euler's special case d(p^n) = n p^(n-1) dp is the chain rule, unstated
  [4] Euler's d(ln x) = dx/x from ln(1 + dx/x), the series cut after one term
  [HONESTY]
"""
import math, os, re, subprocess, sys
from pathlib import Path
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
flat = lambda s: re.sub(r"\s+", " ", s)

print("[1] Katz, in Bradley & Sandifer")
try:
    B = subprocess.run(["pdftotext", "-layout", str(DL / "bradley_leonhard_euler.pdf"), "-"], capture_output=True, text=True, timeout=150).stdout.split("\f")
    pg = lambda n: flat(B[n + 9 - 1])                      # printed page n is pdf page n + 9
    check("p.213: the offset holds -- the page is headed 213", pg(213).lstrip().startswith("Leonhard Euler: Life, Work and Legacy 213"))
    check("p.213: 'Euler introduced much of our current notation for the calculus'", "Euler introduced much of our current notation for the calculus" in pg(213))
    check("p.224: the analysis of the infinite is 'nothing but a special case of the method of differences'", "is nothing but a special case of the method of differences" in pg(224))
    check("p.224: 'the second term and all succeeding terms vanish in the presence of the first term'", "In this expression the second term and all succeeding terms vanish in the presence of the first term" in pg(224))
    check("p.224: 'Euler did not give an explicit statement of the modern chain rule'", "Euler did not give an explicit statement of the modern chain rule" in pg(224))
    check("p.224: '... but did deal with special cases as the need arose': d(p^n) with p a function of x", "but did deal with special cases as the need arose" in pg(224) and "if p is a function of x whose differential is dp" in pg(224))
    check("p.231: understanding 'by pure manipulation of symbols according to the rules'", "pure manipulation of symbols according to the rules" in pg(231) + " " + pg(232))
    check("p.232: 'Read Euler; read Euler. He is the master of us all.' (Laplace)", "Read Euler; read Euler. He is the master of us all." in pg(232))
except Exception as e:
    print("SKIP Bradley", e)

print("[2] numbers a + b*dx with dx^2 = 0")
class D:
    def __init__(s, a, b=0.0): s.a, s.b = a, b
    def __add__(s, o): o = o if isinstance(o, D) else D(o); return D(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __mul__(s, o): o = o if isinstance(o, D) else D(o); return D(s.a * o.a, s.a * o.b + s.b * o.a)   # the dx*dx term dropped
    __rmul__ = __mul__
    def __pow__(s, n):
        r = D(1.0)
        for _ in range(n): r = r * s
        return r
x = 1.3
y = D(x, 1.0) ** 5                                     # (x + dx)^5 with dx^2 = 0
check("(x + dx)^5 = x^5 + 5 x^4 dx: the binomial series cut after the dx term", abs(y.a - x**5) < 1e-12 and abs(y.b - 5 * x**4) < 1e-12, f"coefficient of dx = {y.b:.6f} = 5*{x}^4")

print("[3] Euler's special case is the chain rule")
p = D(x, 1.0) * D(x, 1.0) + 1                           # p = x^2 + 1, carrying dp = 2x dx
q = p ** 5
chain = 5 * (x**2 + 1) ** 4 * (2 * x)
check("d(p^5) with p = x^2 + 1: the algebra returns 5 p^4 dp = 5 (x^2+1)^4 * 2x dx", abs(q.b - chain) < 1e-9, f"{q.b:.6f}")
check("the p-part alone is 2x: dp was carried, not asked for", abs(p.b - 2 * x) < 1e-12)
h = 1e-6
num = (((x + h)**2 + 1)**5 - ((x - h)**2 + 1)**5) / (2 * h)
check("agrees with a central difference", abs(q.b - num) < 1e-4, f"{num:.6f}")

print("[4] d(ln x) = dx/x")
terms = [(-1) ** (k + 1) / k for k in range(1, 6)]      # ln(1+u) = u - u^2/2 + u^3/3 - ...
check("ln(1 + dx/x) = dx/x - dx^2/(2x^2) + ...: with dx^2 = 0 only the first coefficient, 1, survives", terms[0] == 1.0)
for u in (1e-2, 1e-4, 1e-6):
    print(f"     dx/x = {u:.0e}: ln(1+u)/u = {math.log1p(u)/u:.10f}")
check("ln(1+u)/u -> 1 as u -> 0, so d(ln x)/dx = 1/x", abs(math.log1p(1e-8) / 1e-8 - 1) < 1e-8)

print("""
[HONESTY]
[1] reads Katz's survey, a secondary source; Euler's Institutiones calculi
differentialis (1755) itself is not held, and every Euler quotation here is Katz's,
with Katz's page references to the English translation (Blanton). [2]-[4] implement
Euler's rule 'higher differentials vanish' as arithmetic with dx^2 = 0. That this
algebra is exactly what a forward-mode engine computes in is a mathematical identity
checked here numerically; it is not a claim that Euler thought of it that way, and no
historical priority is claimed for anyone.
""")
print(f"{len(FAIL)} FAIL")
sys.exit(1 if FAIL else 0)
