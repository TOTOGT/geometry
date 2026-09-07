#!/usr/bin/env python3
"""
wp102-verify.py — Principia Orthogona, Vol VI, WP-102
"What the Limb Allowed"

Regenerates every computed number in the note. Repo rule: a published number
must be regenerable by a tool.

Run:  python3 wp102-verify.py        (exits non-zero on any failure)
Requires: sympy.  Network optional (--live re-queries JPL Horizons).

Inputs used and their provenance:
  IAU 2015 Saturn spheroid              a = 60268 km, c = 54364 km
  Saturn System III rotation            10h 33m 38s
  Sanchez-Lavega et al., Sci. Adv. 12, eaee4251 (2026):
      decagon at 63.0 S planetographic, drift 2.5 m/s, vertex libration 32 d
  Hexagon latitude 78.5 N planetographic (WP-100 §2)
  JPL Horizons PDObsLat for Saturn, 1 July of each year (cached below; --live re-queries)
"""
import math, sys
import sympy as sp

A_KM, C_KM = 60268.0, 54364.0
a, c = A_KM*1e3, C_KM*1e3
OMEGA = 2*math.pi/(10*3600 + 33*60 + 38)
FEATURE_G = -63.0
HEX_G     =  78.5
MU_CUT    = 0.20

# JPL Horizons, target 699, location 500@399, quantity 14 (PDObsLat), 1 July each year
PDOBSLAT = {2018:31.01, 2019:28.91, 2020:25.51, 2021:20.92, 2022:15.36, 2023:9.09,
            2024:2.40, 2025:-4.41, 2026:-11.03, 2027:-17.13, 2028:-22.47,
            2029:-26.75, 2030:-29.82, 2031:-31.51, 2032:-31.74}

FAIL = []
def check(label, got, want, tol):
    ok = abs(got-want) <= tol
    if not ok: FAIL.append(label)
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}: {got:.4f} (expected {want} +/- {tol})")

def g2c(g):  return math.degrees(math.atan((C_KM/A_KM)**2 * math.tan(math.radians(g))))
def axis_R(g):
    pc = math.radians(g2c(g)); return 1/math.sqrt(1/a**2 + math.tan(pc)**2/c**2)

print("="*72); print("[1] Embedding dimension phi(n): which rotation orders a lattice can carry")
for n, want in [(5,4),(6,2),(7,6),(8,4),(10,4),(11,10),(12,4),(13,12),(30,8)]:
    p = int(sp.totient(n)); tag = "plane -> periodic crystal" if p<=2 else f"needs {p}D -> cut-and-project"
    print(f"      n={n:>2}  phi={p:>2}  {tag}")
    if p != want: FAIL.append(f"phi({n})")
print("      realised quasicrystal orders {5,8,10,12} are exactly the n with phi(n)=4:",
      sorted(n for n in range(3,40) if sp.totient(n)==4))
check("lcm(6,10) — the group a sixfold AND tenfold field must carry", float(sp.lcm(6,10)), 30, 0)
check("phi(30) — the price of thirty, in dimensions", float(sp.totient(30)), 8, 0)

print("="*72); print("[2] WP-100 geometry reproduced")
RN, RS = axis_R(HEX_G), axis_R(FEATURE_G*-1)
lamN, lamS = 2*math.pi*RN/6, 2*math.pi*RS/10
check("hexagon axis radius (km)",  RN/1e3, 13260, 30)
check("decagon axis radius (km)",  RS/1e3, 29641, 30)
check("lambda_6 (km)",            lamN/1e3, 13886, 30)
check("lambda_10 (km)",           lamS/1e3, 18624, 30)

print("="*72); print("[3] The two clocks of the decagon")
C_ring = 2*math.pi*RS
T_side = (C_ring/10)/2.5/86400
check("drift by one wavelength (days)", T_side, 86.22, 0.1)
ratio = T_side/32.0
check("ratio to the 32 d vertex libration", ratio, 2.6944, 0.01)
# LOWEST-denominator rational inside 0.5% -- the commensurability question, not the closest fit
best = next(((n, d) for d in range(1, 40) for n in [round(ratio*d)] if abs(ratio - n/d) < 0.005), None)
print(f"      lowest-denominator rational inside 0.5%: {best[0]}/{best[1]} = {best[0]/best[1]:.4f}")
if best[1] < 10: FAIL.append("clocks: unexpectedly low-order commensurability")
print("      a denominator of 13 before 0.5% is not a resonance -> motion on a 2-torus")
print("      CONDITIONAL: the paper's uncertainties on 2.5 m/s and 32 d are not in hand.")

print("="*72); print("[4] Pole-to-pole NH — a consistency check, NOT evidence (see WP-100 sec 7)")
fN = 2*OMEGA*math.sin(math.radians(g2c(HEX_G)))
fS = 2*OMEGA*math.sin(math.radians(g2c(-FEATURE_G)))
resid = (lamN/lamS)/(fS/fN)
check("observed lambda_N/lambda_S",           lamN/lamS, 0.7456, 0.002)
check("Coriolis-only prediction f_S/f_N",     fS/fN,     0.8736, 0.002)
check("residual (NH)_N/(NH)_S",               resid,     0.8534, 0.002)
m_new = 2*math.pi*RS/(lamS*resid)
check("m if the south adopts the north's NH", m_new,     11.72,  0.05)
print("      m=11 needs -9.1%, m=12 needs -16.7%; measured residual is -14.7%.")
print("      The 2% gap is smaller than any error bar available: 11 and 12 are NOT separated.")
print("      This assumes a selection law. WP-100 sec 7 quotes the paper's own shallow-water")
print("      result that wavenumber is inherited from the forcing. Demoted accordingly.")

print("="*72); print("[5] The archival window — what the limb actually allowed")
if '--live' in sys.argv:
    from astroquery.jplhorizons import Horizons
    for yr in PDOBSLAT:
        e = Horizons(id='699', id_type='majorbody', location='500@399',
                     epochs={'start':f'{yr}-07-01','stop':f'{yr}-07-02','step':'1d'}).ephemerides(quantities='14')
        PDOBSLAT[yr] = round(float(e['PDObsLat'][0]), 2)
    print("      (re-queried JPL Horizons live)")
print(f"      {'year':>5} {'PDObsLat(g)':>12} {'sub-obs(c)':>11} {'S limit(g)':>11} {'mu':>8}  usable")
usable = []
for yr in sorted(PDOBSLAT):
    g = PDOBSLAT[yr]; cen = g2c(g)
    limit = cen - 90.0
    mu = max(math.cos(math.radians(FEATURE_G - cen)), 0.0)
    v = 'YES' if mu >= MU_CUT else ('marginal' if mu >= 0.15 else 'no')
    if v == 'YES': usable.append(yr)
    print(f"      {yr:>5} {g:>11.2f} {cen:>11.2f} {limit:>11.2f} {mu:>8.4f}  {v}")
check("mu at 63S in 2018", max(math.cos(math.radians(FEATURE_G-g2c(PDOBSLAT[2018]))),0), 0.0164, 0.002)
check("mu at 63S in 2022", max(math.cos(math.radians(FEATURE_G-g2c(PDOBSLAT[2022]))),0), 0.2486, 0.002)
check("mu at 63S in 2032", max(math.cos(math.radians(FEATURE_G-g2c(PDOBSLAT[2032]))),0), 0.8061, 0.002)
gap = [y for y in usable if y < 2023]
print(f"      first year with mu >= {MU_CUT}: {usable[0]}")
print(f"      untouched usable epochs before the paper's 2023 baseline: {gap}")
if gap != [2022]: FAIL.append("archival gap is not exactly [2022]")
print("      THE GAP IS ONE YEAR, NOT FIVE. 2018-2020 sit at mu = 0.016-0.101 -- above the")
print("      limb, but edge-on. 2021 is marginal at 0.169. The paper beginning at 2023 is")
print("      very nearly when the geometry became usable, not an oversight.")

print("="*72)
print("ALL CHECKS PASSED" if not FAIL else f"FAILURES: {FAIL}")
raise SystemExit(0 if not FAIL else 1)
