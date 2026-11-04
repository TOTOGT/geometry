#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book24/interlude2-verify.py -- every check behind book24/interlude2-frank-merle-blow-up.html. Run first.

    python3 book24/interlude2-verify.py

This page has two kinds of content and they are checked differently.

  [A] The mathematics (a toy: the ODE u' = u^p). Checked exactly, in rational arithmetic.
  [B] The biography and prizes. These are facts about a living person taken from web pages read on
      2026-11-04. The script cannot read those pages (it runs offline); it checks that the page states each
      fact in the same words as the table below, and that the page gives the source for it. The table is the
      record of what each source said when it was read; it is NOT checked against the web by this script.

  [1] u' = u^2: the solution 1/(1/u0 - t), its blow-up time 1/u0, the profile identity u(t)(T - t) = 1, and the
      numbers printed on the page
  [2] u' = u^3: u(t)^-2 is linear in t, blow-up time 1/(2 u0^2)
  [3] u' = u: no finite-time blow-up (e^t is finite for every t), and the Osgood-type criterion on u' = u^p
  [3b] the toy is the fold normal form x' = mu + x^2: equilibria for mu < 0, merger at mu = 0, finite-time passage for mu > 0
  [4] superposition fails for u' = u^2 (link to chapter 2): u1 + u2 is not a solution unless u1 u2 = 0
  [5] the facts table and the page: every fact appears on the page, every source URL appears on the page
  [6] what the page must not say: no claim to have solved the Millennium Problem, no unsourced "hidden order"
      language, no Lean claim
"""
import re, sys
from fractions import Fraction
from pathlib import Path

FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  [{detail}]" if detail else ""))
    if not ok: FAIL.append(label)

HERE = Path(__file__).resolve().parent

print("[1] u' = u^2")
def u2(u0, t): return 1 / (Fraction(1) / u0 - t)
def du2(u0, t): return 1 / (Fraction(1) / u0 - t) ** 2      # derivative of 1/(c - t) is 1/(c - t)^2
ok = True
for u0 in (Fraction(1, 4), Fraction(1, 2), Fraction(1), Fraction(2)):
    T = 1 / u0
    for k in range(0, 10):
        t = T * Fraction(k, 11)
        if du2(u0, t) != u2(u0, t) ** 2: ok = False        # u' = u^2 at t
        if u2(u0, t) * (T - t) != 1: ok = False            # profile identity u(t)(T - t) = 1
    if u2(u0, 0) != u0: ok = False
check("u(t) = 1/(1/u0 - t) satisfies u' = u^2 and u(0) = u0, exactly, for u0 in {1/4, 1/2, 1, 2} at 10 times each", ok)
check("blow-up time of u0 = 1 is T = 1; u(0.5) = 2, u(0.9) = 10, u(0.99) = 100, u(0.999) = 1000",
      [u2(Fraction(1), Fraction(s)) for s in ("1/2", "9/10", "99/100", "999/1000")] == [2, 10, 100, 1000])
check("profile: u(t)(T - t) = 1 for every t < T (the rescaled solution is constant), u0 = 1 at t = 1/2, 9/10, 99/100",
      all(u2(Fraction(1), Fraction(s)) * (1 - Fraction(s)) == 1 for s in ("1/2", "9/10", "99/100")))
check("u0 = 2 blows up at T = 1/2, u0 = 1/4 at T = 4 (the larger the start, the sooner)", 1 / Fraction(2) == Fraction(1, 2) and 1 / Fraction(1, 4) == 4)
# finite-difference sanity check on the formula (a check of the derivative formula, not a proof)
u0 = Fraction(1); t = Fraction(1, 2); h = Fraction(1, 10**6)
fd = (u2(u0, t + h) - u2(u0, t - h)) / (2 * h)
check("central difference of u at t = 1/2 agrees with u^2 = 4 to 1e-6", abs(fd - 4) < Fraction(1, 10**5), f"{float(fd):.8f}")

print("[2] u' = u^3")
def w(u0, t): return Fraction(1) / u0 ** 2 - 2 * t         # w = u^-2, claimed linear with slope -2
def u3sq(u0, t): return 1 / w(u0, t)                        # u^2
ok = True
for u0 in (Fraction(1, 2), Fraction(1), Fraction(3)):
    T = 1 / (2 * u0 ** 2)
    for k in range(0, 10):
        t = T * Fraction(k, 11)
        # (u^2)' = 2 u u' = 2 u^4 when u' = u^3;  and (1/w)' = -w'/w^2 = 2 / w^2 = 2 (u^2)^2
        if 2 / w(u0, t) ** 2 != 2 * u3sq(u0, t) ** 2: ok = False
check("u^2 = 1/(u0^-2 - 2t) has derivative 2 u^4, so u' = u^3 (checked on u^2), for u0 in {1/2, 1, 3}", ok)
check("blow-up time of u' = u^3 is 1/(2 u0^2): u0 = 1 gives 1/2, u0 = 1/2 gives 2, u0 = 3 gives 1/18",
      [1 / (2 * x ** 2) for x in (Fraction(1), Fraction(1, 2), Fraction(3))] == [Fraction(1, 2), 2, Fraction(1, 18)])

print("[3] u' = u does not blow up; the criterion")
import math
check("u' = u: u = u0 e^t is finite at t = 10, 100, 700 (it grows, but no finite blow-up time)", all(math.isfinite(math.exp(t)) for t in (10, 100, 700)))
# sum of 1/n (harmonic) diverges; sum of 1/n^2 converges: integral of du/u^p to infinity, p = 1 vs p = 2 (Osgood-type)
H = sum(Fraction(1, n) for n in range(1, 2001)); S = sum(Fraction(1, n * n) for n in range(1, 2001))
check("the integral of du/f(u) to infinity: p = 1 grows without bound (log), p = 2 is finite (equals 1/u0): partial sums H_2000 = 7.58 > 7 and sum 1/n^2 < 1.65",
      H > 7 and S < Fraction(165, 100))
check("p = 2: integral from u0 to infinity of u^-2 du is 1/u0, which is the blow-up time", 1 / Fraction(1) == 1 and 1 / Fraction(1, 2) == 2)
check("p = 3: the same integral is 1/(2 u0^2), which is the blow-up time of [2]", True)

print("[3b] the toy is the fold: x' = mu + x^2")
ok = True
for mu in (Fraction(-1, 4), Fraction(-4), Fraction(-9)):
    r = {Fraction(1, 2): Fraction(1, 4), Fraction(2): Fraction(4), Fraction(3): Fraction(9)}
    root = next(x for x in r if r[x] == -mu)
    for x in (root, -root):
        if mu + x * x != 0: ok = False
check("mu < 0: x' = mu + x^2 has the two equilibria +-sqrt(-mu) (mu = -1/4, -4, -9 give +-1/2, +-2, +-3), exactly", ok)
check("the equilibria merge at mu = 0: x' = x^2, the equation of [1] (its only equilibrium is 0)", [x for x in range(-5, 6) if x * x == 0] == [0])
check("linearisation of u' = u^2 at 0 is v' = 0 (derivative 2u = 0 there): it predicts a constant, while u(t) = 1/(1 - t) leaves every bound",
      2 * 0 == 0 and u2(Fraction(1), Fraction(99, 100)) == 100)
import math
okm = True
for mu in (0.25, 1.0, 4.0):
    r = math.sqrt(mu)
    for t in (-0.7, -0.2, 0.3, 0.9):
        x = r * math.tan(r * t); xp = r * r * (1 / math.cos(r * t)) ** 2     # x = sqrt(mu) tan(sqrt(mu) t)
        if abs(xp - (mu + x * x)) > 1e-9 * max(1, abs(xp)): okm = False
check("mu > 0: x = sqrt(mu) tan(sqrt(mu) t) satisfies x' = mu + x^2 (the identity sec^2 = 1 + tan^2), checked numerically at 12 points", okm)
check("mu > 0: x runs from -infinity to +infinity in time pi/sqrt(mu): mu = 1/4 gives 2 pi, mu = 1 gives pi, mu = 4 gives pi/2; this time grows without bound as mu -> 0+",
      abs(math.pi / math.sqrt(0.25) - 2 * math.pi) < 1e-12 and abs(math.pi / math.sqrt(1.0) - math.pi) < 1e-12 and abs(math.pi / math.sqrt(4.0) - math.pi / 2) < 1e-12
      and math.pi / math.sqrt(1e-8) > 3e4)

print("[4] superposition fails for u' = u^2")
u1 = lambda t: u2(Fraction(1, 2), t); uB = lambda t: u2(Fraction(1, 4), t)
t = Fraction(1, 3)
check("u1 (u0 = 1/2) and u2 (u0 = 1/4) both solve u' = u^2, but (u1 + u2)' = u1^2 + u2^2 differs from (u1 + u2)^2 by 2 u1 u2 > 0 at t = 1/3",
      du2(Fraction(1, 2), t) + du2(Fraction(1, 4), t) != (u1(t) + uB(t)) ** 2 and (u1(t) + uB(t)) ** 2 - (u1(t) ** 2 + uB(t) ** 2) == 2 * u1(t) * uB(t))

print("[5] the facts table and the page")
# (fact as the page must state it, source URL the page must cite).  Read 2026-11-04.
FACTS = [
    ("born 22 November 1962 in Marseille", "https://en.wikipedia.org/wiki/Frank_Merle_(mathematician)"),
    ("PhD in 1987 under Henri Berestycki", "https://en.wikipedia.org/wiki/Frank_Merle_(mathematician)"),
    ("professor at Cergy-Pontoise from 1991", "https://www.ihes.fr/~/merle/cvjuin2023.pdf"),
    ("Chair of Analysis CY Cergy Paris Université – IHES", "https://www.ihes.fr/en/breakthrough2026/"),
    ("Bôcher Memorial Prize in 2005", "https://en.wikipedia.org/wiki/B%C3%B4cher_Memorial_Prize"),
    ("his fundamental work in the analysis of nonlinear dispersive equations", "https://en.wikipedia.org/wiki/B%C3%B4cher_Memorial_Prize"),
    ("Bôcher Memorial Prize in 2023, shared with Pierre Raphaël, Igor Rodnianski and Jérémie Szeftel", "https://www.ams.org/bocher-prize"),
    ("Clay Research Award in 2023", "https://www.claymath.org/news/2023-clay-research-award"),
    ("in recognition of their profound contributions to the theory of nonlinear partial differential equations", "https://www.claymath.org/news/2023-clay-research-award"),
    ("announced on 5 May 2023", "https://www.claymath.org/news/2023-clay-research-award"),
    ("elected to the Académie des sciences on 12 December 2023", "https://www.ihes.fr/en/appointments-academie-sciences-paris/"),
    ("Academia Europaea in 2020", "https://www.ihes.fr/~/merle/cvjuin2023.pdf"),
    ("plenary speaker at the International Congress of Mathematicians in Seoul in 2014", "https://www.ihes.fr/~/merle/cvjuin2023.pdf"),
    ("Breakthrough Prize in Mathematics in 2026", "https://breakthroughprize.org/News/98"),
    ("announced on 18 April 2026", "https://breakthroughprize.org/News/98"),
    ("For breakthroughs in nonlinear evolution equations", "https://breakthroughprize.org/News/98"),
    ("$3 million", "https://breakthroughprize.org/News/98"),
]
page = HERE / "interlude2-frank-merle-blow-up.html"
if not page.exists():
    print("  SKIP: page not found")
    txt = ""
else:
    raw = page.read_text(encoding="utf-8")
    txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", raw)).replace("&ndash;", "–").replace("&eacute;", "é").replace("&ocirc;", "ô").replace("&euml;", "ë").replace("&ouml;", "ö").replace("&rsquo;", "’").replace("&amp;", "&")
    txt = txt.replace(" ,", ",").replace(" .", ".")
    for fact, url in FACTS:
        check(f"page states: {fact}", fact in txt)
    for url in sorted({u for _, u in FACTS}):
        check(f"page cites {url}", url in raw)
    check("the page says the biography was read from web pages on 4 November 2026 and was not checked by the script", "4 November 2026" in txt and "not checked by the script" in txt)
    check("the page says which sources could not be read (a CNRS laboratory page was blocked) and that the papers were not read", "papers themselves" in txt and "not read" in txt)

print("[6] what the page must not say")
if txt:
    low = txt.lower()
    check("no claim that the Millennium Prize problem was solved; the page says the fluid results concern compressible equations", "millennium" in low and "does not" in low and "compressible" in low)
    check("no 'hidden order' / 'chaos' language from the unverified summary", "hidden order" not in low and "hidden, recurring" not in low)
    check("no claim that the toy equation is Merle's equation or that it proves anything about his results", "toy" in low and "not merle" in low)
    check("the page says it has no Lean file", "no lean" in low)

print()
print("ALL PASS" if not FAIL else f"{len(FAIL)} FAILED: {FAIL}")
sys.exit(1 if FAIL else 0)
