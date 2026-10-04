#!/usr/bin/env python3
"""photochem-laser-verify.py -- checks behind book7/photochem-laser.html (2026-10-04).

Source for every "book p." note: K. K. Rohatgi-Mukherjee, Fundamentals of Photochemistry (revised ed.),
Ch.10 sec. 10.4 "Lasers in photochemical kinetics", pp.317-321 (Fig. 10.12 values read from the page scan).
Book statements are CITED; the rate-equation models, derivations and controls are ours. numpy only.

Blocks
 [1] two levels: the most that can be lifted is one half (equal degeneracy), and inversion is never reached
 [2] three-level scheme (ruby, Fig. 10.12): threshold pump rate per ion = about k21
 [3] four-level scheme: threshold set by the thermal population of the lower laser level
 [4] ruby numbers read from Fig. 10.12 and p.317: photon energy, lifetimes, what a long pump pulse loses
 [5] frequency doubling: 694 -> 347 nm, and what "about 20 % efficiency" means in photons
 [6] power density: can the p.317 figure of 1e19 W/cm^2 come from the pulse that page is describing?
 [7] page check
Controls are lines that must reject a wrong value; they print PASS when the wrong value is rejected.
"""
import math, os, re, sys, html as _html
import numpy as np

FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + ("  " + detail if detail else ""))
    if not ok: FAIL.append(label)

h, c, NA, kB, eV = 6.62607015e-34, 299792458.0, 6.02214076e23, 1.380649e-23, 1.602176634e-19

# [1] ------------------------------------------------------------------------------
def two_level(W, A, g1, g2):
    # dN2/dt = W N1 - W (g1/g2) N2 - A N2 = 0 with N1 + N2 = 1
    N2 = W / (W + W * g1 / g2 + A)
    return N2, 1 - N2
Ws = np.logspace(0, 12, 25)
fr = [two_level(W, 1e8, 1, 1)[0] for W in Ws]
check("[1] equal degeneracy: the upper-level fraction rises with pump rate but stays below 1/2 for every pump rate tried", all(f < 0.5 for f in fr) and fr[-1] > 0.499, f"max {max(fr):.6f}")
inv = [(two_level(W, 1e8, 2, 3)[0] * 2 - two_level(W, 1e8, 2, 3)[1] * 3) for W in Ws]   # N2*g1 - N1*g2 (g1=2,g2=3)
check("[1] with degeneracies 2 and 3 the upper fraction can pass 1/2 (limit 3/5) but N2/g2 > N1/g1 is still never reached", two_level(1e12, 1e8, 2, 3)[0] > 0.55 and all(v < 0 for v in inv))
check("[1] control: the claim 'a two-level system can be inverted at high pump' is REJECTED", not any(v > 0 for v in inv))

# [2] ------------------------------------------------------------------------------
def three(W, k21, k32):
    # levels 1,2,3 ; pump 1<->3 at W ; 3->2 at k32 ; 2->1 at k21 ; N = 1
    # steady state: dN3: W N1 - (W + k32) N3 = 0 ; dN2: k32 N3 - k21 N2 = 0 ; sum = 1
    A = np.array([[W, 0, -(W + k32)], [0, -k21, k32], [1, 1, 1]], dtype=float)
    b = np.array([0, 0, 1.0])
    N1, N2, N3 = np.linalg.solve(A, b)
    return N1, N2, N3
k21, k32 = 2e2, 1e9                                              # k21 = 2e2 /s from Fig. 10.12; k32 ASSUMED fast
def threshold3():
    lo, hi = 1e-3, 1e8
    for _ in range(200):
        mid = math.sqrt(lo * hi); N1, N2, _ = three(mid, k21, k32)
        lo, hi = (mid, hi) if N2 < N1 else (lo, mid)
    return math.sqrt(lo * hi)
W3 = threshold3(); W3_formula = k21 * k32 / (k32 - k21)
print(f"   three-level threshold pump rate per ion: {W3:.4f} /s   (k21 k32/(k32-k21) = {W3_formula:.4f})")
check("[2] numerical threshold equals k21 k32/(k32-k21)", abs(W3 / W3_formula - 1) < 1e-6)
check("[2] threshold is 200 /s to three figures: one pump quantum per ion per 5 ms", abs(W3 - 200.0) < 0.05, f"{W3:.3f}")
check("[2] at half the threshold the upper level is NOT ahead; at twice it is", three(W3 / 2, k21, k32)[1] < three(W3 / 2, k21, k32)[0] and three(2 * W3, k21, k32)[1] > three(2 * W3, k21, k32)[0])
check("[2] control: a threshold ten times k21 (2000 /s) is REJECTED", not abs(W3 / 2000.0 - 1) < 0.05)

# [3] ------------------------------------------------------------------------------
def four(W, ku, kl, kpu, x):
    # states: g, l (lower laser), u (upper laser), p (pump) ; thermal up-rate g->l = kl*exp(-x), x = dE/kT
    # dp: W g - (W + kpu) p = 0 ; du: kpu p - ku u = 0 ; dl: ku u + kl e^-x g - kl l = 0 ; sum = 1
    A = np.array([[W, 0, 0, -(W + kpu)],            # dp
                  [0, 0, -ku, kpu],                 # du
                  [kl * math.exp(-x), -kl, ku, 0],  # dl
                  [1, 1, 1, 1]], dtype=float)
    b = np.array([0, 0, 0, 1.0])
    g, l, u, p = np.linalg.solve(A, b)
    return g, l, u, p
ku, kl, kpu = 2e2, 1e9, 1e9
dE, T = 0.20, 300.0                                              # ASSUMED lower-level gap 0.2 eV, room temperature
x = dE * eV / (kB * T)
def threshold4():
    lo, hi = 1e-8, 1e8
    for _ in range(300):
        mid = math.sqrt(lo * hi); g, l, u, p = four(mid, ku, kl, kpu, x)
        lo, hi = (mid, hi) if u < l else (lo, mid)
    return math.sqrt(lo * hi)
W4 = threshold4()
print(f"   dE/kT = {x:.3f}; four-level threshold = {W4:.4f} /s;  ratio three/four = {W3/W4:.0f};  e^x = {math.exp(x):.0f}")
check("[3] four-level threshold is about k_u e^-x (within 1 %)", abs(W4 / (ku * math.exp(-x)) - 1) < 0.01)
check("[3] four-level threshold = 0.087 /s", abs(W4 - 0.087) < 0.0005, f"{W4:.4f}")
check("[3] ratio of three-level to four-level thresholds = 2.3e3 for these assumptions", abs(W3 / W4 / 2300 - 1) < 0.03, f"{W3/W4:.0f}")
g, l, u, p = four(1e3, ku, kl / 1e7, kpu, x)      # lower level that empties SLOWER than the upper one decays: ku > kl
check("[3] control: if the lower level empties more slowly than the upper decays (k_l < k_u) no pump rate inverts it",
      all(four(W, 2e2, 20.0, kpu, x)[2] < four(W, 2e2, 20.0, kpu, x)[1] for W in (1e1, 1e3, 1e5, 1e7)))

# [4] ------------------------------------------------------------------------------
lam = 694.3e-9
Ephot = h * c / lam
tau_E = 1 / 2e2; tau_F = 1 / 3e6
kept_1ms = math.exp(-2e2 * 1e-3); kept_50ms = math.exp(-2e2 * 50e-3)
stored = 0.5 * NA * Ephot / 1e3
print(f"   694.3 nm photon {Ephot/eV:.3f} eV ; 2E lifetime {tau_E*1e3:.1f} ms ; 4F2 fluorescence lifetime {tau_F*1e6:.3f} us ; kept after 1 ms {kept_1ms:.3f}, after 50 ms {kept_50ms:.2e}")
check("[4] ruby laser photon = 1.786 eV", abs(Ephot / eV - 1.786) < 0.001, f"{Ephot/eV:.4f}")
check("[4] 2E lifetime from k = 2e2 /s is 5.0 ms; 4F2 fluorescence lifetime from 3e6 /s is 0.333 us", abs(tau_E * 1e3 - 5.0) < 1e-9 and abs(tau_F * 1e6 - 0.3333) < 1e-3)
check("[4] after a 1 ms pump pulse 82 % of what reached 2E is still there", abs(kept_1ms - 0.819) < 0.001, f"{kept_1ms:.3f}")
check("[4] least energy stored to invert one mole of Cr(III): half the ions at the laser photon energy = 86.1 kJ", abs(stored - 86.1) < 0.1, f"{stored:.1f} kJ")
check("[4] control: after a 50 ms pump pulse more than 80 % would remain -- REJECTED", not kept_50ms > 0.8)

# [5] ------------------------------------------------------------------------------
lam2 = lam / 2
photon_ratio = (0.20 * 1.0 / (h * c / lam2)) / (1.0 / (h * c / lam))
print(f"   second harmonic {lam2*1e9:.2f} nm ({h*c/lam2/eV:.3f} eV); 20 % of the ENERGY is {photon_ratio*100:.0f} % of the PHOTONS")
check("[5] 694.3 nm doubled = 347.15 nm (book p.319: 694 -> 347 nm)", abs(lam2 * 1e9 - 347.15) < 0.005)
check("[5] 20 % energy efficiency = 10 % of the photons (each product photon takes two)", abs(photon_ratio - 0.10) < 1e-12)
check("[5] outside the book: a fundamental near 1060 nm quadrupled gives 265 nm (the book's Nd-glass figure)", abs(1060 / 4 - 265) < 0.01)
check("[5] control: one doubling of 1060 nm (530 nm) is NOT 265 nm", not abs(1060 / 2 - 265) < 1)

# [6] ------------------------------------------------------------------------------
area = (lam * 100) ** 2                                         # (lambda in cm)^2, order-of-magnitude diffraction-limited spot
P_q = 1.0 / 10e-9                                                # 1 J in 10 ns (book p.319: several joules, nanosecond)
P_ml = 1e13                                                      # upper end of book p.320 for mode-locked pulses
I_q = P_q / area; I_ml = P_ml / area
need = 1e19 * area
print(f"   spot area ~ lambda^2 = {area:.2e} cm^2 ; Q-switched 1 J / 10 ns = {P_q:.0e} W -> {I_q:.1e} W/cm^2 ; 1e19 W/cm^2 needs {need:.1e} W ; mode-locked 1e13 W -> {I_ml:.1e} W/cm^2")
check("[6] Q-switched pulse (1 J, 10 ns) at a lambda^2 spot reaches about 2e16 W/cm^2", abs(I_q / 2.1e16 - 1) < 0.05, f"{I_q:.2e}")
check("[6] 1e19 W/cm^2 at that spot needs about 4.8e10 W, which is 480 times that pulse", abs(need / 4.8e10 - 1) < 0.02 and abs(need / P_q / 480 - 1) < 0.02, f"{need:.2e} W, x{need/P_q:.0f}")
check("[6] the book's own mode-locked upper figure (1e13 W) would reach about 2e21 W/cm^2, so p.317's 1e19 is consistent with p.320 but not with a Q-switched nanosecond pulse", I_ml > 1e19 > I_q)
check("[6] control: at a 1 mm^2 spot (not focused) the same Q-switched pulse gives only 1e10 W/cm^2, which does NOT reach 1e19 -- confirms the spot size is the assumption that matters",
      abs(P_q / 1e-2 - 1e10) < 1e8 and not P_q / 1e-2 >= 1e19)

# [7] ------------------------------------------------------------------------------
here = os.path.dirname(os.path.abspath(__file__))
page = os.path.join(here, "photochem-laser.html")
if os.path.exists(page):
    txt = open(page, encoding="utf-8").read()
    txt = re.sub(r"<!--po-([a-z]+)-->.*?<!--/po-\1-->", "", txt, flags=re.S)
    txt = _html.unescape(re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>", " ", txt, flags=re.S))
    need_s = ["200 /s", "0.087 /s", "2.3e3", "1.786 eV", "5.0 ms", "0.333 µs", "82 %", "86.1 kJ", "347.15 nm", "10 % of the photons",
              "2e16", "4.8e10", "480 times", "2e21", "1e10"]
    for s in need_s:
        check(f"[7] page prints {s!r}", s in txt)
    check("[7] control: a number this script never produced is absent from the page", "999.9" not in txt)
else:
    print("SKIP [7] page not found beside this script")

print("\n[HONESTY] Blocks [1]-[3] are OUR rate-equation models: the book describes inversion qualitatively (p.317-318) and says a four-level scheme needs 'much less pump power'; the thresholds, k32 = 1e9 /s, kl = 1e9 /s and the 0.2 eV lower-level gap are ASSUMED, not from the book.")
print("[HONESTY] Block [4] k values are read from the Fig. 10.12 caption on the page scan (k_f = 3e6 /s, k_e = 2e2 /s); they are not independently confirmed. Pump-lamp efficiency is not modelled.")
print("[HONESTY] Block [6] is an order-of-magnitude consistency check with a lambda^2 spot, not a laser design; it does not say the book is wrong, only which pulse type its 1e19 W/cm^2 can belong to.")
print("[HONESTY] The 1060 nm fundamental in block [5] is outside the book (the pages read do not state it). The book's Fig. 10.14 labels the doubling crystal NH4H2PO4 while its text says KDP; this page does not resolve that.")
sys.exit(1 if FAIL else 0)
