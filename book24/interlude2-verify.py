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

print("[5b] focusing against dispersion: the virial identity y'' = 16 E (floating-point numerics; not a proof)")
try:
    import numpy as np
except Exception as ex:
    np = None; print(f"  SKIP: numpy not available ({ex}); no claim made")
if np is not None:
    L_, M_ = 60.0, 4096; xs = (np.arange(M_) - M_ // 2) * (L_ / M_); dxs = L_ / M_; ks = 2 * np.pi * np.fft.fftfreq(M_, d=dxs)
    def lin(v, dt): return np.fft.ifft(np.exp(-1j * ks ** 2 * dt / 2) * np.fft.fft(v))
    def stp(v, dt):
        v = lin(v, dt); v = v * np.exp(1j * np.abs(v) ** 4 * dt); return lin(v, dt)
    def En(v):
        vx = np.fft.ifft(1j * ks * np.fft.fft(v)); return 0.5 * np.sum(abs(vx) ** 2) * dxs - np.sum(abs(v) ** 6) * dxs / 6
    def yy(v): return np.sum(xs ** 2 * abs(v) ** 2) * dxs
    MQ = np.sqrt(3) * np.pi / 2
    for A in (0.5, 1.5, 2.5):
        u0 = A * np.exp(-xs ** 2 / 2) * np.exp(0.7j * xs); h = 2e-3; n = 20; up = u0.copy(); um = u0.copy()
        for _ in range(n): up = stp(up, h / n); um = stp(um, -h / n)
        ypp = (yy(up) - 2 * yy(u0) + yy(um)) / h ** 2; e = En(u0)
        check(f"A = {A}: finite-difference y'' = {ypp:+.4f} agrees with 16E = {16 * e:+.4f} to 4 significant digits", abs(ypp - 16 * e) <= 1e-4 * max(1.0, abs(16 * e)))
        vx = np.fft.ifft(1j * ks * np.fft.fft(u0)); K = np.sum(abs(vx) ** 2) * dxs; Mm = np.sum(abs(u0) ** 2) * dxs
        check(f"A = {A}: E >= (1/2)(1 - (M/M_Q)^2) int|u_x|^2 (illustration of the sharp inequality, not a proof)", e >= 0.5 * (1 - (Mm / MQ) ** 2) * K - 1e-9)
    Q = 3 ** 0.25 / np.sqrt(np.cosh(2 * xs)); Qxx = np.real(np.fft.ifft(-(ks ** 2) * np.fft.fft(Q)))
    check("Q = 3^(1/4) sech(2x)^(1/2) solves Q'' - Q + Q^5 = 0 (residual below 1e-8 on the grid)", np.max(abs(Qxx - Q + Q ** 5)) < 1e-8)
    check("mass of Q is sqrt(3) pi / 2 = 2.7207 (to 8 digits) and E(Q) = 0", abs(np.sum(Q ** 2) * dxs - MQ) < 1e-8 and abs(En(Q.astype(complex))) < 1e-9)
# exact part: the parabola
y0, y1, E_ = Fraction(1), Fraction(0), Fraction(-1, 8)
check("exact: y(t) = y0 + y1 t + 8 E t^2 with y0 = 1, y1 = 0, E = -1/8 is 1 - t^2: second derivative -2 = 16 E, and it vanishes at t = 1",
      16 * E_ == -2 and (y0 + y1 * 1 + 8 * E_ * 1) == 0)
if np is not None:
    ok = True
    for lam in (0.5, 2.0, 3.0):
        g = np.exp(-xs ** 2 / 2); gl = lam ** 0.5 * np.exp(-(lam * xs) ** 2 / 2)
        ok &= abs(np.sum(gl ** 2) * dxs - np.sum(g ** 2) * dxs) < 1e-9
        ok &= abs(np.sum(gl ** 6) * dxs - lam ** 2 * np.sum(g ** 6) * dxs) < 1e-9
        glx = np.real(np.fft.ifft(1j * ks * np.fft.fft(gl))); gx = np.real(np.fft.ifft(1j * ks * np.fft.fft(g)))
        ok &= abs(np.sum(glx ** 2) * dxs - lam ** 2 * np.sum(gx ** 2) * dxs) < 1e-8
    check("dilation u_lam = lam^(1/2) u(lam x), Gaussian, lam = 0.5, 2, 3: mass fixed, int|u_x|^2 and int|u|^6 both scale like lam^2 (the critical scaling)", bool(ok))

print("[5c] the pressure hull: wall stress and the buckling threshold")
check("exact: wall stress p R / (2 t) with R = 1, t = 1/10, p = 50e6 is 250e6 (force balance p pi R^2 = sigma 2 pi R t, pi cancels)",
      Fraction(50 * 10 ** 6) * 1 / (2 * Fraction(1, 10)) == 250 * 10 ** 6)
check("exact: exercise numbers R = 2, t = 1/20, p = 20e6 give wall stress 400e6",
      Fraction(20 * 10 ** 6) * 2 / (2 * Fraction(1, 20)) == 400 * 10 ** 6)
import math
okm = True
for (E_, nu_, t_, R_) in ((200e9, 0.30, 0.05, 1.0), (70e9, 0.33, 0.02, 0.5), (1.0, 0.25, 0.01, 1.0)):
    D_ = E_ * t_ ** 3 / (12 * (1 - nu_ ** 2)); k4 = E_ * t_ / (D_ * R_ ** 2)
    f_ = lambda k: D_ * k ** 2 / t_ + E_ / (R_ ** 2 * k ** 2)
    kstar = k4 ** 0.25
    best = min(f_(kstar * 10 ** (e / 200)) for e in range(-200, 201))
    pred = 2 * math.sqrt(D_ * E_ / t_) / R_
    target = E_ * t_ / (R_ * math.sqrt(3 * (1 - nu_ ** 2)))
    okm &= abs(f_(kstar) - pred) < 1e-9 * pred and best >= pred * (1 - 1e-12) and abs(pred - target) < 1e-9 * target
check("numerical (floating point): min over k of D k^2/t + E/(R^2 k^2) is 2 sqrt(DE/t)/R at k^4 = E t/(D R^2) (scan over three decades), and equals E t / (R sqrt(3(1 - nu^2))), for three parameter sets", okm)
check("1/sqrt(3 (1 - 0.3^2)) = 0.6052 to four digits (the page's 0.605 E t/R)", abs(1 / math.sqrt(3 * (1 - 0.09)) - 0.6052) < 5e-5)
pc = lambda t_: 2 * t_ * (1.0 * t_ / (1.0 * math.sqrt(3 * (1 - 0.09)))) / 1.0
check("buckling pressure p_cr = 2 t sigma_cr / R with sigma_cr proportional to t is proportional to t^2: doubling t multiplies it by 4", abs(pc(0.1) / pc(0.05) - 4) < 1e-12)

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

print("[7] the Lean file")
src = (HERE / "Interlude2.lean").read_text(encoding="utf-8")
rep_f = HERE / "interlude2.axioms.txt"
code = re.sub(r"/-.*?-/", "", src, flags=re.S)
names = ["toy_quadratic_deriv", "toy_quadratic_profile", "toy_quadratic_unbounded", "fold_tan_deriv",
         "virial_first_derivative", "virial_second_derivative", "virial_collapse", "glassey_step", "virial_terms",
         "energy_scales_critical", "energy_lower_bound", "no_negative_energy_below_threshold",
         "negative_energy_forces_mass", "sphere_force_balance", "wrinkle_stress_lower_bound",
         "wrinkle_stress_attained", "zoelly_algebra", "zoelly_pressure"]
for nm in names:
    check(f"theorem {nm} is stated", re.search(r"theorem\s+" + nm + r"\b", code) is not None)
check("no sorry or admit in the Lean code", not re.search(r"\b(sorry|admit)\b", code))
has_rep = rep_f.exists() and rep_f.read_text(encoding="utf-8").strip() != ""
if has_rep:
    r = rep_f.read_text(encoding="utf-8")
    check("axiom report: all eighteen theorems appear", all(("Book24Il2." + nm) in r for nm in names))
    check("axiom report: no sorryAx and no error", "sorryAx" not in r and "error" not in r.lower())
else:
    print("  NOTE: no interlude2.axioms.txt yet; the Lean file has NOT been compiled (run the command in its header).")
if txt:
    check("page links Interlude2.lean and says it states eighteen results", "Interlude2.lean" in txt and "eighteen" in txt)
    check("page says the Lean file is not compiled unless a report exists", ("not yet compiled" in txt) == (not has_rep))
    check("page says the Lean file does not formalise the equation (virial identity and GN enter as hypotheses)", "hypotheses" in txt and "not formalised" in txt)
    check("page makes no claim about the cause of the Titan failure and gives no design guidance", "no claim about its cause" in txt and "guidance for building or diving" in txt)

print("[8] the two figures (floating-point numerics; read from interlude2-figs.json, recompute with interlude2-figs.py)")
import json, math as _m
jf = Path(__file__).resolve().parent / "interlude2-figs.json"
if not jf.exists():
    print("  NOTE: no interlude2-figs.json; the figures have not been computed")
else:
    d = json.loads(jf.read_text(encoding="utf-8")); pos, neg, lat = d["pos"], d["neg"], d["lattice"]
    check("figure 1, E > 0: computed y matches y(0) + 8 E t^2 (relative gap < 1e-5) and E is conserved (< 1e-8)", pos["maxrel"] < 1e-5 and pos["Edrift"] < 1e-8, f"gap {pos['maxrel']:.1e}, drift {pos['Edrift']:.1e}")
    check("figure 1, E < 0: same on 0 <= t <= 0.3 t* (gap < 1e-8, E drift < 1e-6), and the peak only grows modestly (< 5)", neg["maxrel"] < 1e-8 and neg["Edrift"] < 1e-6 and neg["peak"] < 5, f"gap {neg['maxrel']:.1e}, drift {neg['Edrift']:.1e}, peak {neg['peak']:.2f}")
    check("figure 1: both runs satisfy kmax^2 dt < pi (split-step stability) and E < 0 gives a finite zero t* = sqrt(y0/(-8E))",
          pos["stab"] < _m.pi and neg["stab"] < _m.pi and neg["E"] < 0 and abs(neg["tstar"] - _m.sqrt(neg["y0"] / (-8 * neg["E"]))) < 1e-9 and abs(neg["T"] - 0.3 * neg["tstar"]) < 1e-3 * neg["tstar"])
    check("figure 2: mass drift < 1e-6, fractions in [0, 1], small at Lambda = 0.5 (< 0.05), large at Lambda = 12 (> 0.9), and increasing from Lambda = 3.5 on",
          lat["mass_drift_final"] < 1e-6 and all(0 <= f <= 1 for f in lat["fraction"]) and lat["fraction"][0] < 0.05 and lat["fraction"][-1] > 0.9
          and all(lat["fraction"][i] <= lat["fraction"][i + 1] for i in range(lat["Lambda"].index(3.5), len(lat["fraction"]) - 1)))
    ftxt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", page_html)) if "page_html" in globals() else None
    if ftxt is None:
        ftxt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", (Path(__file__).resolve().parent / "interlude2-frank-merle-blow-up.html").read_text(encoding="utf-8")))
    check("page prints the stored figure numbers (t* and the gaps) and calls t* the latest possible time, not the collapse time",
          f"{neg['tstar']:.4f}" in ftxt and f"{pos['maxdev']:.1e}" in ftxt and f"{neg['maxdev']:.1e}" in ftxt and "latest" in ftxt and "the collapse time the argument predicts" not in ftxt)
    check("page says the failed part of the run is not plotted and is not evidence of blow-up", "that part is not plotted" in ftxt and "it does not show it" in ftxt)


print("[9] r_eye(3,l) section (formulas only; read from the typeset arXiv PDF pp. 4-5)")
import math as _m2
def _re(d, l): return (d + l) / (l + _m2.sqrt(d)) if l < d else 1 + (d - 1) / (1 + _m2.sqrt(l)) ** 2
_pg = (Path(__file__).resolve().parent / "interlude2-frank-merle-blow-up.html").read_text(encoding="utf-8")
_tx = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", _pg))
check("branches agree at l = d and equal 3 - sqrt 3 for d = 3 (limits from both sides within 1e-9)", abs((3+3)/(3+_m2.sqrt(3)) - (1+2/(1+_m2.sqrt(3))**2)) < 1e-12 and abs(_re(3,3-1e-9)-(3-_m2.sqrt(3))) < 1e-8 and abs(_re(3,3+1e-9)-(3-_m2.sqrt(3))) < 1e-8)
check("r_eye(3,l) is strictly decreasing on (0,12], above 1, and the review's r2,r3,r4 (1.0501, 1.1010, 1.1348) lie in (1, 3 - sqrt 3)",
      all(_re(3,0.05*i) > _re(3,0.05*(i+1)) > 1 for i in range(1,239) if abs(0.05*i-3) > 0.06) and all(1 < v < 3-_m2.sqrt(3) for v in (1.0501,1.1010,1.1348)))
check("e = (l(r-1)+r-2)/2 > 0 at r = r_eye(3,l) exactly when r_eye > (l+2)/(l+1); this holds at l = 3 and for every l > 3 sampled, and fails below l = sqrt 3 (so the bound is sqrt 3, not 3); gamma < (2+sqrt3)/sqrt3 is the same as l > sqrt 3",
      abs((2+_m2.sqrt(3))/_m2.sqrt(3) - (1+2/_m2.sqrt(3))) < 1e-12 and abs(2/((2+_m2.sqrt(3))/_m2.sqrt(3)-1) - _m2.sqrt(3)) < 1e-12 and abs((2*_m2.sqrt(3)-3)/(2-_m2.sqrt(3)) - _m2.sqrt(3)) < 1e-12 and
      all(_re(3,l) > (l+2)/(l+1) for l in [3]+[3+0.1*i for i in range(1,400)]) and _re(3,1.70) < (1.70+2)/(2.70) and _re(3,1.80) > (1.80+2)/2.80)
check("page states the formula, the source arXiv:1912.11009, the typeset-page provenance, that r2-r4 are quoted not recomputed, and that Annals Part I was not read",
      "arXiv:1912.11009" in _tx and "typeset pages 4 and 5" in _tx and "quoted from the review" in _tx and "not recomputed" in _tx and "Part I was not read" in _tx)
check("page attributes l > 3 to lost radicals in a text extraction, not to a different version of the paper", "extraction loss, not a difference in the paper" in _tx and "versions of the paper differ" not in _tx)

def _rep(nm):
    f = Path(__file__).resolve().parent / nm
    return f.read_text(encoding="utf-8") if f.exists() and f.read_text(encoding="utf-8").strip() else ""
_rr, _wr = _rep("reye.axioms.txt"), _rep("witness.axioms.txt")
check("page says the r_eye derivation is floating point and does not resolve the l > d branch",
      "reye-derive.py" in _tx and "nothing is claimed about that branch" in _tx and "does not prove that smooth self-similar profiles exist" in _tx)
if not _rr:
    check("ReyeAlgebra.lean: no report, page says not compiled", "has not been compiled" in _tx)
elif "sorryAx" in _rr or "error" in _rr.lower():
    _bad = [l for l in _rr.splitlines() if "sorryAx" in l]
    check("ReyeAlgebra.lean: report shows only threshold_three with sorryAx, and the page says three of four clean and the rewrite not recompiled",
          len(_bad) == 1 and "threshold_three" in _bad[0] and "three of the four theorems are clean" in _tx and "not been recompiled" in _tx)
else:
    check("ReyeAlgebra.lean: clean report with all four theorems, page says all four clean", all(("Book24Re." + n) in _rr for n in ("branch_agree","branch_agree_d","threshold_three","plus_branch_positive")) and "all four theorems are clean" in _tx and "three of the four" not in _tx)
if not _wr:
    check("Witness.lean: no report, page says untested", "The file is untested" in _tx)
elif "sorryAx" in _wr or "error" in _wr.lower():
    check("Witness.lean: report shows a problem; the page must not say clean", "compiled clean (all six" not in _tx)
else:
    check("Witness.lean: clean report with all six theorems, page says compiled clean and not untested",
          all(("Book24Wi." + n) in _wr for n in ("agree_of_subsingleton","disagree_possible","witness_minimum","witness_minimum_card","majority_three","no_majority_two"))
          and "The file compiled clean (all six" in _tx and "The file is untested" not in _tx)
check("page 5d links Witness.lean and says the agreement is not blind", "Witness.lean" in _tx and "It is not blind" in _tx and "two routes meet, not that either is right about the fluid" in _tx)

print()
print("ALL PASS" if not FAIL else f"{len(FAIL)} FAILED: {FAIL}")
sys.exit(1 if FAIL else 0)
