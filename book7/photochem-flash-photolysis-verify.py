#!/usr/bin/env python3
"""photochem-flash-photolysis-verify.py -- checks behind book7/photochem-flash-photolysis.html (2026-10-04).

Source for every "book p." note: K. K. Rohatgi-Mukherjee, Fundamentals of Photochemistry (revised ed.),
Ch.10 sec. 10.3 "Techniques for study of transient species", pp.311-317 (numbers on pp.315-316 read from
the page scan). Book statements are CITED; the checks, simulations and controls are ours. numpy only.

Blocks
 [1] the 12 % in-band fraction at 6000 K (book p.315-316)
 [2] quanta from a 100 J flash, the concentration they make, and the book's rounding
 [3] the detection limit from Beer's law with a 3 % change (book p.316)
 [4] headroom between [2] and [3]
 [5] flash duration against lifetime: the printed sentence says the flash sets an UPPER limit; the simulation says LOWER
 [6] capacitor energy against the 20-2000 J and 0.5-20 kV the book gives
 [7] sector method: where 1/2 and 1/sqrt(2) come from, and why it needs second-order termination
 [8] page check
Controls are lines that must reject a wrong value; they print PASS when the wrong value is rejected.
"""
import math, os, re, sys, html as _html
import numpy as np

FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + ("  " + detail if detail else ""))
    if not ok: FAIL.append(label)

h, c, NA, kB = 6.62607015e-34, 299792458.0, 6.02214076e23, 1.380649e-23
def trap(y, x):
    y = np.asarray(y); x = np.asarray(x)
    return float(np.sum((y[1:] + y[:-1]) * np.diff(x)) / 2)

# [1] ------------------------------------------------------------------------------
def band_fraction(T, lo=350e-9, hi=450e-9):
    lam = np.logspace(math.log10(20e-9), math.log10(1e-3), 400001)       # 20 nm to 1 mm, log grid
    B = lam ** -5 / np.expm1(h * c / (lam * kB * T))                      # spectral radiance shape (energy per wavelength)
    tot = trap(B, lam)
    m = (lam >= lo) & (lam <= hi)
    return trap(B[m], lam[m]) / tot
f6000 = band_fraction(6000); f5000 = band_fraction(5000)
print(f"   share of blackbody ENERGY in 350-450 nm: {f6000*100:.1f} % at 6000 K, {f5000*100:.1f} % at 5000 K")
check("[1] 6000 K: 12.2 % of the energy lies in 350-450 nm (book: 12 %)", abs(f6000 * 100 - 12.2) < 0.15, f"{f6000*100:.2f} %")
check("[1] control: the book's 12 % is REJECTED at 5000 K (7.7 %)", not abs(f5000 * 100 - 12) < 0.5, f"{f5000*100:.2f} %")

# [2] ------------------------------------------------------------------------------
E_ph = h * c / 400e-9
q_exact = 100 * 0.12 / E_ph
q_book = 2.5e19
dev = (q_book / q_exact - 1) * 100
conc_book = q_book / NA / 0.020
conc_exact = q_exact / NA / 0.020
print(f"   quanta from 100 J: {q_exact:.3e} exact vs {q_book:.1e} printed ({dev:+.1f} %); in 20 mL: {conc_book:.3e} (from printed) / {conc_exact:.3e} mol/L")
check("[2] 100 J x 0.12 at 400 nm = 2.42e19 quanta", abs(q_exact / 2.42e19 - 1) < 0.002, f"{q_exact:.3e}")
check("[2] the printed 2.5e19 is 3.5 % above that (rounding, not an error that matters)", abs(dev - 3.5) < 0.1, f"{dev:+.2f} %")
check("[2] 2.5e19 quanta in 20 mL = 2.1e-3 mol/L (as printed)", abs(conc_book / 2.1e-3 - 1) < 0.02, f"{conc_book:.3e}")
check("[2] the exact count gives 2.0e-3 mol/L", abs(conc_exact / 2.0e-3 - 1) < 0.01, f"{conc_exact:.3e}")
check("[2] control: a 1 % tolerance REJECTS the printed 2.5e19", not abs(dev) < 1.0)

# [3] ------------------------------------------------------------------------------
eps, ell = 7e4, 20.0
C_lim = math.log10(100 / 97) / (eps * ell)
print(f"   detection limit C = log(100/97)/(eps l) = {C_lim:.3e} mol/L")
check("[3] detection limit = 9.4e-9 mol/L (book: about 1e-8)", abs(C_lim / 9.4e-9 - 1) < 0.01, f"{C_lim:.3e}")
check("[3] it is within a factor 1.1 of the book's 1e-8", 1 / 1.1 < C_lim / 1e-8 < 1.1)
check("[3] control: with eps = 7e3 (one digit lost) the limit would be 9.4e-8, so '1e-8' is REJECTED", not abs(math.log10(100 / 97) / (7e3 * ell) / 1e-8 - 1) < 0.2)

# [4] ------------------------------------------------------------------------------
ratio = 2.1e-3 / C_lim
eta_min = C_lim / 2.1e-3
print(f"   headroom 2.1e-3 / {C_lim:.2e} = {ratio:.2e} ; smallest overall efficiency that is still detectable = {eta_min:.2e}")
check("[4] headroom = 2.2e5 (about five orders of magnitude)", abs(ratio / 2.2e5 - 1) < 0.02, f"{ratio:.3e}")
ratio_exact = conc_exact / C_lim
check("[4] against the exact 2.0e-3 the headroom is 2.1e5", abs(ratio_exact / 2.1e5 - 1) < 0.02, f"{ratio_exact:.3e}")
check("[4] smallest efficiency still detectable = 4.5e-6", abs(eta_min / 4.5e-6 - 1) < 0.02, f"{eta_min:.3e}")
check("[4] control: an overall efficiency of 1e-7 would leave the triplet BELOW the limit", 1e-7 < eta_min)

# [5] ------------------------------------------------------------------------------
def visible_fraction(tau, w, n=200000):
    # lamp is a box of width w; transient forms at constant rate during it and decays with tau. Peak concentration
    # relative to the concentration if all of it formed instantaneously.
    t = np.linspace(0, w, n)
    kernel = np.exp(-(w - t) / tau)
    return trap(kernel, t) / w
w = 10e-6
vf = {tau: visible_fraction(tau, w) for tau in (1e-6, 10e-6, 100e-6)}
for tau, v in vf.items(): print(f"   flash width {w*1e6:g} us, lifetime {tau*1e6:g} us: peak is {v:.3f} of the instantaneous-flash peak (analytic (tau/w)(1-exp(-w/tau)))")
check("[5] w = 10 us: lifetimes 1, 10, 100 us give 0.100, 0.632, 0.952 of the full peak",
      abs(vf[1e-6] - 0.100) < 0.001 and abs(vf[10e-6] - 0.632) < 0.001 and abs(vf[100e-6] - 0.952) < 0.001)
check("[5] w = 10 us, lifetime 2 us: 0.199 of the full peak (quiz example)", abs(visible_fraction(2e-6, 10e-6) - 0.199) < 0.001, f"{visible_fraction(2e-6,10e-6):.4f}")
check("[5] the fraction rises monotonically with lifetime: SHORT lifetimes are what a long flash loses", vf[1e-6] < vf[10e-6] < vf[100e-6])
check("[5] a 100 us transient is seen at 95 % with a 10 us flash, so the printed 'upper limit' reading is REJECTED",
      not vf[100e-6] < 0.5)
check("[5] control: with a 100 us flash a 1 us transient is almost lost (1 %)", abs(visible_fraction(1e-6, 100e-6) - 0.010) < 0.001, f"{visible_fraction(1e-6,100e-6):.4f}")

# [6] ------------------------------------------------------------------------------
E_fig = 0.5 * 5e-6 * (20e3) ** 2
C_low = 2 * 20.0 / 500.0 ** 2
print(f"   Fig. 10.10B: 5 uF at 20 kV = {E_fig:.0f} J ; 20 J at 0.5 kV needs {C_low*1e6:.0f} µF")
check("[6] the figure's 5 uF at 20 kV stores 1000 J, inside the book's 20-2000 J", abs(E_fig - 1000) < 1e-9 and 20 <= E_fig <= 2000)
check("[6] the low end (20 J at 0.5 kV) needs 160 µF", abs(C_low * 1e6 - 160) < 1e-9)
check("[6] control: reading the voltage as 20 V would store 1 mJ, outside the range -- REJECTED", not (20 <= 0.5 * 5e-6 * 20.0 ** 2 <= 2000))

# [7] ------------------------------------------------------------------------------
def sector_ratio(period, k=1.0, Ia=1.0, order=2):
    # d[X]/dt = Ia(t) - k [X]^order, Ia(t) = Ia for the first half of each period and 0 for the second half.
    # Returns the cycle-averaged [X] divided by the continuous-light steady state. Total time >= 40 radical lifetimes.
    tau_rad = 1.0 / (order * k * (math.sqrt(Ia / k) ** (order - 1)))     # linearised relaxation time at the continuous steady state
    steps = 40 if period < tau_rad else 2000
    dt = period / steps
    Xss = math.sqrt(Ia / k) if order == 2 else Ia / k
    X = Xss
    ncyc = int(math.ceil(40 * tau_rad / period)) + 12
    t = 0.0; acc = 0.0; cnt = 0
    for cyc in range(ncyc):
        for i in range(steps):
            on = Ia if (i < steps // 2) else 0.0                           # constant over the step: boundaries fall on step edges
            f = lambda X: on - k * max(X, 0.0) ** order
            k1 = f(X); k2 = f(X + dt * k1 / 2); k3 = f(X + dt * k2 / 2); k4 = f(X + dt * k3)
            X += dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6
            if cyc >= ncyc - 10: acc += X; cnt += 1
    return (acc / cnt) / Xss
tau_r = 1.0 / (2 * 1.0 * 1.0)         # radical lifetime 1/(2 k [X]ss) for second-order termination, k = Ia = 1
slow = sector_ratio(200.0 * tau_r); fast = sector_ratio(0.002 * tau_r)
print(f"   second-order termination: relative mean radical level / rate, slow sector {slow:.4f}, fast sector {fast:.4f} ; 1/sqrt(2) = {1/math.sqrt(2):.4f}")
slow2 = sector_ratio(2000.0 * tau_r)
print(f"   slow sector at 2000 tau_r: {slow2:.4f}")
check("[7] slow sector: relative rate approaches 1/2 from ABOVE, and only slowly (0.533 at 200 tau_r, 0.506 at 2000 tau_r) because second-order decay in the dark is hyperbolic",
      0.5 < slow2 < slow < 0.55 and abs(slow - 0.533) < 0.002 and abs(slow2 - 0.506) < 0.001, f"{slow:.4f}, {slow2:.4f}")
check("[7] fast sector: relative rate = 1/sqrt(2) = 0.7071 (book p.314)", abs(fast - 1 / math.sqrt(2)) < 0.005, f"{fast:.4f}")
pers = [0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 20.0, 100.0]
curve = [sector_ratio(p * tau_r) for p in pers]
mid = 0.5 * (0.5 + 1 / math.sqrt(2))
j = next(i for i, v in enumerate(curve) if v <= mid)
lin = np.interp(mid, curve[::-1], np.log10(pers)[::-1])
print("   relative rate vs sector period / tau_r: " + ", ".join(f"{p:g}:{v:.3f}" for p, v in zip(pers, curve)))
print(f"   half-way level {mid:.4f} is crossed at a period of about {10**lin:.2f} tau_r (light period {10**lin/2:.2f} tau_r)")
check("[7] the curve falls monotonically from 0.707 (fast) to 0.5 (slow) as the sector slows", all(curve[i] >= curve[i + 1] - 1e-3 for i in range(len(curve) - 1)))
t90 = math.atanh(0.90) / 1.0 / tau_r; t99 = math.atanh(0.99) / 1.0 / tau_r     # X(t) = Xss tanh(k Xss t) for growth from zero; in units of tau_r = 1/(2 k Xss)
print(f"   growth from zero under light: 90 % of steady state after {t90:.2f} tau_r, 99 % after {t99:.2f} tau_r")
check("[7] growth from zero follows tanh: 90 % of steady state after 2.9 tau_r, 99 % after 5.3 tau_r", abs(t90 - 2.94) < 0.01 and abs(t99 - 5.30) < 0.01)
check("[7] the half-way crossing of the rate curve is at a light period of 16.1 tau_r, about three times the time to reach 99 % of steady state, so the inflection locates the lifetime only to within a model fit",
      abs(10 ** lin / 2 - 16.1) < 0.3 and 10 ** lin / 2 > 2.5 * t99, f"{10**lin/2:.2f} tau_r")
s1 = sector_ratio(200.0, order=1); f1 = sector_ratio(0.002, order=1)
print(f"   first-order termination: slow {s1:.4f}, fast {f1:.4f}")
check("[7] control: with FIRST-order termination fast and slow limits are both 1/2, so no 1/sqrt(2) step and no lifetime to read off",
      abs(s1 - 0.5) < 0.01 and abs(f1 - 0.5) < 0.01 and not abs(f1 - 1 / math.sqrt(2)) < 0.05)

# [8] ------------------------------------------------------------------------------
here = os.path.dirname(os.path.abspath(__file__))
page = os.path.join(here, "photochem-flash-photolysis.html")
if os.path.exists(page):
    txt = open(page, encoding="utf-8").read()
    txt = re.sub(r"<!--po-([a-z]+)-->.*?<!--/po-\1-->", "", txt, flags=re.S)
    txt = _html.unescape(re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>", " ", txt, flags=re.S))
    need_s = ["12.2 %", "7.7 %", "2.42e19", "2.5e19", "+3.5 %", "2.1e-3", "2.0e-3", "9.4e-9", "2.2e5", "2.1e5", "4.5e-6",
              "0.100", "0.199", "0.632", "0.952", "1000 J", "160 µF", "0.7071", "0.533", "0.506", "16.1", "2.9", "5.3"]
    for s in need_s:
        check(f"[8] page prints {s!r}", s in txt)
    check("[8] control: a number this script never produced is absent from the page", "999.9" not in txt)
else:
    print("SKIP [8] page not found beside this script")

print("\n[HONESTY] Blocks [1]-[4] and [6] are exact arithmetic. Block [5] and [7] are numerical (trapezoid / RK4): evidence, not proof.")
print("[HONESTY] Block [2] takes the book's premise that 100 J of lamp output is spread as a 6000 K blackbody and fully absorbed in 20 mL; it does not model electrical-to-light efficiency, quantum yield of the intermediate, or the sample's own absorption.")
print("[HONESTY] Block [5] is OUR reading of an apparent inversion on p.315: the page prints that the flash duration sets the 'upper limit' of detectable lifetimes. The simulation shows the flash width limits the SHORTEST resolvable lifetime. It does not say what limits the longest; the book is silent. The sentence is read from the page scan; if the scan misleads, block [5] still stands as a statement about physics.")
print("[HONESTY] The 5 uF and 20 kV in block [6] are read from Fig. 10.10B on the page scan. Block [7] uses a square-wave sector with equal light and dark periods; the book's general light-to-dark ratio is not explored.")
sys.exit(1 if FAIL else 0)
