#!/usr/bin/env python3
"""photochem-spectrometer-verify.py -- checks behind book7/photochem-spectrometer.html (2026-10-04).

Source for every "book p." note: K. K. Rohatgi-Mukherjee, Fundamentals of Photochemistry (revised ed.),
Ch.10, pp.302-311 (emission spectra, quantum yields, lifetimes). Book statements are CITED; the
derivations, simulations and controls are ours. Needs numpy only.

Blocks
 [1] relative quantum yield (book Eq. 10.1): phi_s = phi_ref * (F_s/F_ref) * (f_ref/f_s), f = 1 - 10^-A
 [2] why the book asks for dilute solutions (OD about 0.03): the linear stand-in for f
 [3] phase shift: integrate dI/dt = -kI + k J(t) for sinusoidal J and read the phase and modulation off the result
 [4] phase angles at the book's frequency and lifetime range
 [5] delay from distance (Kerr-cell and Porter-Topp arrangements): t = d / c, and the round-trip factor 2
 [6] single-photon counting: why the count rate must be low (ours; the book says only "not too high")
 [7] lifetime bookkeeping: k_f = phi/tau, 1/tau = k_f + sum k_i (book Eqs. 10.2, 10.3)
 [8] spectra per wavelength vs per wavenumber: counts are conserved, the shape is not
 [9] page check
Controls are lines that must reject a wrong value; they print PASS when the wrong value is rejected.
"""
import math, os, re, sys, html as _html
import numpy as np

def trap(y, x):
    y = np.asarray(y); x = np.asarray(x)
    return float(np.sum((y[1:] + y[:-1]) * np.diff(x)) / 2)

FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + ("  " + detail if detail else ""))
    if not ok: FAIL.append(label)

f_abs = lambda A: 1 - 10 ** (-A)

# [1] --------------------------------------------------------------------------
def qy_sample(phi_ref, F_ratio, A_s, A_ref, exact=True):
    fr = (lambda A: f_abs(A)) if exact else (lambda A: A)
    return phi_ref * F_ratio * fr(A_ref) / fr(A_s)
phi_ref, Fr, A_s, A_ref = 0.50, 0.84, 0.030, 0.030      # HYPOTHETICAL standard and readings
phi_s = qy_sample(phi_ref, Fr, A_s, A_ref)
print(f"   example: phi_ref = {phi_ref} (hypothetical), F_s/F_ref = {Fr}, equal OD {A_s}  ->  phi_s = {phi_s:.3f}")
check("[1] equal absorbance and geometry: phi_s/phi_ref = F_s/F_ref (book Eq. 10.1)", abs(phi_s / phi_ref - Fr) < 1e-12)
check("[1] example phi_s = 0.420", abs(phi_s - 0.420) < 1e-9, f"{phi_s:.3f}")
check("[1] control: if the sample absorbs MORE than the standard, the same F ratio must give a LOWER phi_s",
      qy_sample(0.5, 0.84, 0.060, 0.030) < phi_s)

# [2] --------------------------------------------------------------------------
def lin_err(A_s, A_ref):
    ex = f_abs(A_ref) / f_abs(A_s); li = A_ref / A_s
    return (li / ex - 1) * 100
e_dil = lin_err(0.030, 0.045); e_conc = lin_err(0.30, 0.45)
print(f"   linear-in-OD correction error: ODs 0.030 vs 0.045: {e_dil:+.1f} %;  ODs 0.30 vs 0.45: {e_conc:+.1f} %")
check("[2] at OD 0.03-0.045 the linear correction is within 2 %", abs(e_dil) < 2.0, f"{e_dil:+.2f} %")
check("[2] at OD 0.30-0.45 it is off by more than 10 %", abs(e_conc) > 10.0, f"{e_conc:+.2f} %")
check("[2] control: the dilute-case 2 % bound must NOT hold at OD 0.3-0.45", not abs(e_conc) < 2.0)

# [3] phase shift by integration --------------------------------------------------
def simulate(nu, tau, steps=4000):
    k = 1.0 / tau; w = 2 * math.pi * nu; T = 1.0 / nu
    dt = T / steps; t = 0.0; I = 0.5
    J = lambda t: 0.5 + 0.5 * math.cos(w * t)               # a0/2 = 1/2, a1 = 1/2 (modulation of the exciting light = 1)
    rhs = lambda t, I: -k * I + k * J(t)
    settle = int(max(60 * tau, 8 * T) / dt)
    for _ in range(settle):
        k1 = rhs(t, I); k2 = rhs(t + dt / 2, I + dt * k1 / 2); k3 = rhs(t + dt / 2, I + dt * k2 / 2); k4 = rhs(t + dt, I + dt * k3)
        I += dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6; t += dt
    ts, Is = [], []
    for _ in range(steps):
        ts.append(t); Is.append(I)
        k1 = rhs(t, I); k2 = rhs(t + dt / 2, I + dt * k1 / 2); k3 = rhs(t + dt / 2, I + dt * k2 / 2); k4 = rhs(t + dt, I + dt * k3)
        I += dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6; t += dt
    ts, Is = np.array(ts), np.array(Is)
    M = np.column_stack([np.ones_like(ts), np.cos(w * ts), np.sin(w * ts)])
    c0, a, b = np.linalg.lstsq(M, Is, rcond=None)[0]
    theta = math.atan2(b, a)                                  # I ~ c0 + R cos(wt - theta)
    mod = math.hypot(a, b) / c0                               # AC/DC of the response; the exciting light has AC/DC = 1
    return theta, mod
cases = [(2e6, 1e-8), (20e6, 1e-8), (2e6, 1e-10), (20e6, 1e-10)]
sim = {}
for nu, tau in cases:
    th, m = simulate(nu, tau); sim[(nu, tau)] = (th, m)
    wt = 2 * math.pi * nu * tau
    print(f"   nu = {nu/1e6:4.0f} MHz  tau = {tau:.0e} s  w*tau = {wt:.4f}  simulated phase {math.degrees(th):8.4f} deg, modulation {m:.5f}   (atan(w tau) = {math.degrees(math.atan(wt)):8.4f}, cos = {math.cos(math.atan(wt)):.5f})")
ok_t = all(abs(math.tan(sim[k][0]) - 2 * math.pi * k[0] * k[1]) < 2e-3 * max(1.0, 2 * math.pi * k[0] * k[1]) + 1e-6 for k in cases)
check("[3] tan(theta) = 2 pi nu tau for all four (nu, tau)  (book Eq. 10.9/10.11)", ok_t)
ok_m = all(abs(sim[k][1] - 1 / math.sqrt(1 + (2 * math.pi * k[0] * k[1]) ** 2)) < 2e-3 for k in cases)
check("[3] modulation depth = 1/sqrt(1 + (w tau)^2) = cos(theta)  (the amplitude factor in Eq. 10.11)", ok_m)
wrong = lambda k: 1 / (2 * math.pi * k[0] * k[1])            # tan(theta) = 1/(w tau): the inverted form
check("[3] control: the inverted relation tan(theta) = 1/(w tau) is REJECTED by the simulation",
      not all(abs(math.tan(sim[k][0]) - wrong(k)) < 0.05 * wrong(k) for k in cases))

# [4] -------------------------------------------------------------------------------
ang = {k: math.degrees(math.atan(2 * math.pi * k[0] * k[1])) for k in cases}
check("[4] 2 MHz, 10 ns: 7.16 deg", abs(ang[(2e6, 1e-8)] - 7.16) < 0.01, f"{ang[(2e6,1e-8)]:.2f}")
check("[4] 20 MHz, 10 ns: 51.5 deg", abs(ang[(20e6, 1e-8)] - 51.5) < 0.05, f"{ang[(20e6,1e-8)]:.2f}")
check("[4] 20 MHz, 0.1 ns: 0.72 deg", abs(ang[(20e6, 1e-10)] - 0.72) < 0.005, f"{ang[(20e6,1e-10)]:.3f}")
check("[4] 2 MHz, 0.1 ns: 0.072 deg", abs(ang[(2e6, 1e-10)] - 0.072) < 0.0005, f"{ang[(2e6,1e-10)]:.4f}")
check("[4] control: no single frequency in 2-20 MHz gives a phase near 45 deg at BOTH 10 ns and 0.1 ns",
      not (30 < ang[(20e6, 1e-8)] < 60 and 30 < ang[(20e6, 1e-10)] < 60))

# [5] -------------------------------------------------------------------------------
c = 299792458.0
d_1ns = c * 1e-9
check("[5] 1 ns of light travel = 29.98 cm", abs(d_1ns * 100 - 29.98) < 0.01, f"{d_1ns*100:.2f} cm")
x = 0.15; delay = 2 * x / c
check("[5] a mirror 15 cm farther away adds a 1.00 ns round-trip delay (Porter-Topp style)", abs(delay * 1e9 - 1.00) < 0.005, f"{delay*1e9:.3f} ns")
check("[5] control: forgetting the round trip (x/c) gives 0.50 ns, which is REJECTED", not abs(x / c * 1e9 - 1.00) < 0.005)

# [6] pile-up --------------------------------------------------------------------------
def apparent_tau_ratio(p, n=200001):
    tau = 1.0
    t = np.linspace(0, 0.02, n)
    F = 1 - np.exp(-t / tau); f = np.exp(-t / tau) / tau
    h = f * np.exp(-p * F)                                        # first-photon histogram (ours)
    s = np.polyfit(t[:2001], np.log(h[:2001]), 1)[0]
    return -1 / s / tau
rat = {p: apparent_tau_ratio(p) for p in (0.0, 0.01, 0.05, 0.5)}
for p, r in rat.items(): print(f"   detection probability per flash {p:4.2f}: apparent early lifetime / true = {r:.4f}   (1/(1+p) = {1/(1+p):.4f})")
check("[6] early apparent lifetime = tau/(1+p) for p = 0, 0.01, 0.05, 0.5", all(abs(rat[p] - 1 / (1 + p)) < 2e-3 for p in rat))
check("[6] at p = 0.05 the lifetime reads 4.8 % short; at p = 0.01, 1.0 % short", abs((1 - rat[0.05]) * 100 - 4.76) < 0.1 and abs((1 - rat[0.01]) * 100 - 0.99) < 0.05)
check("[6] control: the claim 'no distortion at p = 0.5' is REJECTED", not abs(rat[0.5] - 1) < 0.05)

# [7] -------------------------------------------------------------------------------------
phi, tau = 0.30, 5e-9                                           # HYPOTHETICAL
kf = phi / tau; ksum = 1 / tau - kf; tau0 = 1 / kf
print(f"   hypothetical phi = {phi}, tau = {tau*1e9:g} ns -> k_f = {kf:.2e} /s, sum k_i = {ksum:.2e} /s, radiative lifetime 1/k_f = {tau0*1e9:.1f} ns")
check("[7] k_f = 6.0e7 /s", abs(kf / 6.0e7 - 1) < 1e-9)
check("[7] sum of the other rate constants = 1.4e8 /s", abs(ksum / 1.4e8 - 1) < 1e-9)
check("[7] radiative lifetime = 16.7 ns and phi = tau/tau_rad", abs(tau0 * 1e9 - 16.7) < 0.05 and abs(tau / tau0 - phi) < 1e-12)
check("[7] control: a measured tau LONGER than the radiative lifetime would give phi > 1, which is rejected", not (20e-9 / tau0 <= 1.0))

# [8] -------------------------------------------------------------------------------------
lam = np.linspace(300, 700, 400001); dl = lam[1] - lam[0]
n_lam = np.exp(-0.5 * ((lam - 450) / 20.0) ** 2)                # counts per nm, Gaussian in wavelength
nu = 1e7 / lam                                                   # cm^-1
n_nu = n_lam * lam ** 2 / 1e7                                    # counts per cm^-1: n(nu) = n(lam) |dlam/dnu|
area_lam = trap(n_lam, lam); area_nu = abs(trap(n_nu, nu))
peak_lam = lam[np.argmax(n_lam)]; peak_nu_as_nm = 1e7 / nu[np.argmax(n_nu)]
print(f"   area per nm = {area_lam:.3f}, area per cm^-1 = {area_nu:.3f}; peak at {peak_lam:.1f} nm per nm, at {peak_nu_as_nm:.1f} nm per wavenumber")
check("[8] counts are conserved under the change of variable (areas agree within 0.1 %)", abs(area_nu / area_lam - 1) < 1e-3)
check("[8] the peak moves: per-wavenumber maximum sits at a longer wavelength than per-wavelength maximum (+1.8 nm for this 20 nm-wide band at 450 nm)", abs((peak_nu_as_nm - peak_lam) - 1.8) < 0.05, f"{peak_nu_as_nm - peak_lam:+.1f} nm")
area_bad = abs(trap(n_lam, nu))
check("[8] control: integrating the per-nm spectrum over wavenumber without the Jacobian gives a different area, REJECTED", not abs(area_bad / area_lam - 1) < 1e-3)

# [9] -------------------------------------------------------------------------------------
here = os.path.dirname(os.path.abspath(__file__))
page = os.path.join(here, "photochem-spectrometer.html")
if os.path.exists(page):
    txt = open(page, encoding="utf-8").read()
    txt = re.sub(r"<!--po-([a-z]+)-->.*?<!--/po-\1-->", "", txt, flags=re.S)
    txt = _html.unescape(re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>", " ", txt, flags=re.S))
    need = ["0.420", "7.16", "51.5", "0.72", "0.072", "29.98", "1.00 ns", "4.8 %", "6.0e7", "1.4e8", "16.7 ns", "+1.8 nm"]
    # [2] numbers are rendered with sign; compute exact strings
    need += [f"{e_dil:+.1f} %", f"{e_conc:+.1f} %"]
    for s in need:
        check(f"[9] page prints {s!r}", s in txt)
    check("[9] control: a number this script never produced is absent from the page", "999.9" not in txt)
else:
    print("SKIP [9] page not found beside this script")

print("\n[HONESTY] Blocks [1], [2], [4], [5], [7] are exact arithmetic on stated inputs. Blocks [3], [6], [8] are numerical (RK4 / least squares / trapezoid): evidence, not proof.")
print("[HONESTY] phi_ref, the readings in [1] and the numbers in [7] are HYPOTHETICAL. The book names quinine sulphate in 0.1 N H2SO4 and anthracene in benzene as common standards (p.303) but the pages read here do not give a yield, so none is used.")
print("[HONESTY] Block [1] leaves out the refractive-index factor between solvents and re-absorption; the book flags re-absorption (p.304) and this page does not correct it. Block [6] is our derivation; the book only says the count rate should not be too high (p.308).")
print("[HONESTY] Not checked: the 2-20 MHz recommendation for 1e-8 to 1e-10 s (p.310) is cited; block [4] shows what phase it implies, not whether a given detector can resolve it.")
sys.exit(1 if FAIL else 0)
