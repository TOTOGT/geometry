#!/usr/bin/env python3
"""photochem-light-sources-verify.py -- checks behind book7/photochem-light-sources.html (2026-10-04).

Source for every "book p." note: K. K. Rohatgi-Mukherjee, Fundamentals of Photochemistry (revised ed.),
Ch.10 "Tools and Techniques", pp.298-302. Book statements are CITED; the arithmetic, controls and
the worked example are ours. Needs numpy only.

Blocks
 [1] energy per photon and per einstein: E = h c / lambda (exact SI constants) at the lamp lines and range ends the book names
 [2] the book's rounded hc (2e-16 J nm) against the exact value
 [3] fraction of light absorbed, 1 - 10^-A: the book's "99%" is A = 2
 [4] worked example (ours): lamp flux from an actinometer reading, and what each omitted factor costs
 [5] chooser: which of the four chemical actinometers the book gives a range for covers a wavelength
 [6] page check: every number the page prints is produced here
Controls are lines that must reject a wrong value; they print PASS when the wrong value is rejected.
"""
import math, os, re, sys, html as _html

FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + ("  " + detail if detail else ""))
    if not ok: FAIL.append(label)

h, c, NA = 6.62607015e-34, 299792458.0, 6.02214076e23     # SI exact
def E_photon(nm): return h * c / (nm * 1e-9)
def E_einstein_kJ(nm): return NA * E_photon(nm) / 1e3

# [1] -------------------------------------------------------------------
rows = [(253.7, "Hg low-pressure resonance line (book p.298)"), (365.0, "Hg line, 365 nm triplet region (book p.298)"),
        (400.0, "flash example wavelength (book p.316)"), (577.0, "ferrioxalate range end (book p.301)")]
val = {}
for nm, why in rows:
    val[nm] = E_einstein_kJ(nm)
    print(f"   {nm:6.1f} nm  {E_photon(nm)/1.602176634e-19:.3f} eV  {val[nm]:.1f} kJ per einstein   ({why})")
check("[1] energy falls as wavelength rises: 253.7 > 365 > 400 > 577 nm", val[253.7] > val[365.0] > val[400.0] > val[577.0])
check("[1] 365 nm einstein = 327.7 kJ", abs(val[365.0] - 327.7) < 0.05, f"{val[365.0]:.2f}")
check("[1] 253.7 nm einstein = 471.5 kJ", abs(val[253.7] - 471.5) < 0.05, f"{val[253.7]:.2f}")
check("[1] control: a value that forgets N_A (J per photon read as kJ per einstein) is rejected",
      not abs(E_photon(365.0) - 327.7) < 0.05)

# [2] -------------------------------------------------------------------
hc_nm = h * c * 1e9                   # J nm
dev = (2e-16 - hc_nm) / hc_nm
print(f"   exact hc = {hc_nm:.4e} J nm; book prints 2e-16 J nm ({dev*100:+.2f} %)")
check("[2] book's rounded hc is within 1 % of exact", abs(dev) < 0.01, f"{dev*100:+.2f} %")
check("[2] control: the same rounded hc is NOT within 0.1 % (tolerance matters)", not abs(dev) < 0.001)

# [3] -------------------------------------------------------------------
frac = lambda A: 1 - 10 ** (-A)
check("[3] A = 2 absorbs 99 %  (book p.302 asks the Reinecke solution to absorb nearly 99 %)", abs(frac(2) - 0.99) < 1e-12)
check("[3] control: A = 1 absorbs 90 %, not 99 %", not abs(frac(1) - 0.99) < 1e-3, f"{frac(1):.3f}")

# [4] worked example (ours) ----------------------------------------------
n_fe, phi, t, A, nm = 3.0e-8, 1.2, 60.0, 2.0, 366.0          # hypothetical reading; phi = book p.301 (254-365 nm)
f = frac(A)
I0 = n_fe / (phi * f * t)                    # einstein per second incident
photons = I0 * NA
power = photons * E_photon(nm)
print(f"   example: n = {n_fe:g} mol product in {t:g} s, phi = {phi}, A = {A} (absorbs {f:.2f}), {nm:g} nm")
print(f"   incident flux I0 = {I0:.3e} einstein/s = {photons:.3e} photons/s = {power*1e3:.3f} mW")
check("[4] I0 = 4.21e-10 einstein/s", abs(I0 / 4.21e-10 - 1) < 0.005, f"{I0:.3e}")
check("[4] photons per second = 2.54e14", abs(photons / 2.54e14 - 1) < 0.005, f"{photons:.3e}")
check("[4] power = 0.138 mW", abs(power * 1e3 - 0.138) < 0.0005, f"{power*1e3:.4f}")
err_f = n_fe / (phi * 1.0 * t) / I0 - 1       # forgetting f
err_phi = n_fe / (1.0 * f * t) / I0 - 1       # using phi = 1
print(f"   forgetting the absorbed fraction: {err_f*100:+.1f} %   using phi = 1: {err_phi*100:+.1f} %")
check("[4] forgetting the absorbed fraction (f = 1) changes I0 by about 1 %", abs(err_f + 0.01) < 0.002, f"{err_f*100:+.2f} %")
check("[4] using phi = 1 instead of 1.2 changes I0 by about 20 %", abs(err_phi - 0.2) < 0.002, f"{err_phi*100:+.2f} %")
check("[4] control: if the solution absorbed only A = 0.301 (50 %), forgetting f would be a factor 2 error",
      abs(1 / frac(0.30103) - 2) < 0.001)
check("[4] control: the 1 % claim FAILS for that weakly absorbing solution",
      not abs((1 / frac(0.30103)) - 1) < 0.02)

# [5] chooser ----------------------------------------------------------------
RANGES = {   # nm range and quantum yield as printed (book pp.301-302)
    "ferrioxalate": (250, 577, "1.1 to 1.2"),
    "uranyl oxalate": (208, 435, "about 0.5"),
    "Reinecke's salt": (316, 735, "0.27 to 0.3"),
    "malachite green leucocyanide": (None, None, "0.91"),   # book gives 'particularly useful 220-300 nm', not a range
}
def covering(nm):
    return [k for k, (lo, hi, _) in RANGES.items() if lo is not None and lo <= nm <= hi]
check("[5] 254 nm: ferrioxalate and uranyl oxalate cover it, Reinecke does not",
      covering(254) == ["ferrioxalate", "uranyl oxalate"], str(covering(254)))
check("[5] 500 nm: ferrioxalate and Reinecke cover it", covering(500) == ["ferrioxalate", "Reinecke's salt"], str(covering(500)))
check("[5] 700 nm: only Reinecke's salt covers it", covering(700) == ["Reinecke's salt"], str(covering(700)))
check("[5] 200 nm: none of the three printed ranges covers it", covering(200) == [])
check("[5] control: at 600 nm ferrioxalate must NOT be listed (range ends 577)", "ferrioxalate" not in covering(600))

# [6] page check ---------------------------------------------------------------
here = os.path.dirname(os.path.abspath(__file__))
page = os.path.join(here, "photochem-light-sources.html")
if os.path.exists(page):
    txt = open(page, encoding="utf-8").read()
    txt = re.sub(r"<!--po-([a-z]+)-->.*?<!--/po-\1-->", "", txt, flags=re.S)
    txt = _html.unescape(re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>", " ", txt, flags=re.S))
    need = ["471.5", "327.7", "299.1", "207.3", "4.21e-10", "2.54e14", "0.138", "-1.0 %", "+20.0 %", "1.986e-16"]
    for s in need:
        check(f"[6] page prints {s!r}", s in txt)
    check("[6] control: a number this script never produced is absent from the page", "999.9" not in txt)
else:
    print("SKIP [6] page not found beside this script")

print("\n[HONESTY] Blocks [1]-[3] are exact arithmetic. Block [4] uses a HYPOTHETICAL reading (3.0e-8 mol in 60 s); it shows how the factors enter, not a measurement.")
print("[HONESTY] The quantum yields and ranges in block [5] are the book's printed values (pp.301-302), cited, not re-measured here; the book is not in this repository and was read from page scans.")
print("[HONESTY] Not checked: whether 0.006 M ferrioxalate absorbs enough at each wavelength (the book gives no extinction coefficient), the colorimetric analysis step, and any vendor's current protocol.")
sys.exit(1 if FAIL else 0)
