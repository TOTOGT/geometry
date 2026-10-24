#!/usr/bin/env python3
"""Verification table for hex-habitat.html (Built from Mars section; G6 LLC, 2026-10-23).

Usage:
  python3 BuiltFromMars_verify.py                  # offline checks + banned-claim scan of the section .md
  python3 BuiltFromMars_verify.py page.html ...    # also scan other files for banned claims
  python3 BuiltFromMars_verify.py --online         # also fetch each NASA page and look for each key string

Statuses:
  confirmed  = matched against the page text via a fetch on 2026-10-23
  derived    = arithmetic on confirmed figures (re-run below)
  secondary  = from a non-NASA source, labelled as such
  unconfirmed = not checked against a source; must not be used as fact
"""
import re, sys, math, os, urllib.request

MARS = "https://nssdc.gsfc.nasa.gov/planetary/factsheet/marsfact.html"
CHAL = "https://www.nasa.gov/news-release/teams-3d-print-planetary-habitats-awarded-700k-in-nasa-challenge/"
TOP5 = "https://www.nasa.gov/centers-and-facilities/marshall/top-five-teams-win-a-share-of-100000-in-virtual-modeling-stage-of-nasas-3d-printed-habitat-competition/"
MOX  = "https://www.nasa.gov/missions/mars-2020-perseverance/perseverance-rover/nasas-oxygen-generating-experiment-moxie-completes-mars-mission/"
ZOPH = "https://www.dezeen.com/2018/07/27/nasa-announces-winners-3d-habitat-centennial-challenge-competition-printed-habitat-mars/amp/"  # Dezeen, 27 Jul 2018 (secondary); replaced mymodernmet URL that returned 404
IAC19 = "https://ntrs.nasa.gov/api/citations/20190032473/downloads/20190032473.pdf"
ZIMG = "https://www.nasa.gov/wp-content/uploads/2019/04/p3l4_zopherus_4.png"
BVAD = "https://ntrs.nasa.gov/citations/20210024855"

# id, claim as used, source, key string expected on the page, status
ROWS = [
 ("G",        "Surface gravity 3.73 m/s2, 0.380 x Earth",          MARS, "3.73",          "confirmed"),
 ("G-RATIO",  "Gravity ratio 0.380",                               MARS, "0.380",         "confirmed"),
 ("P",        "Surface pressure 6.36 mb at mean radius",           MARS, "6.36 mb",       "confirmed"),
 ("P-PCT",    "Under 1% of Earth sea-level pressure",              "derived: 6.36 / 1013.25 (standard atmosphere)", None, "derived"),
 ("T-RANGE",  "Diurnal range -89 to -31 C (Viking 1 Lander site)", MARS, "-89 to -31",    "confirmed"),
 ("CO2",      "Atmosphere 95.1% CO2",                              MARS, "95.1%",         "confirmed"),
 ("N2",       "Nitrogen 2.59%",                                    MARS, "2.59%",         "confirmed"),
 ("AR",       "Argon 1.94%",                                       MARS, "1.94%",         "confirmed"),
 ("DAY",      "Solar day 24.6597 h (shown as 24.66)",              MARS, "24.6597",       "confirmed"),
 ("D-MIN",    "Minimum distance from Earth 54.6 million km",       MARS, "54.6",          "confirmed"),
 ("D-MAX",    "Maximum distance from Earth 401.4 million km",      MARS, "401.4",         "confirmed"),
 ("CH-SCALE", "Challenge structures were one-third scale",         CHAL, "one-third scale","confirmed"),
 ("CH-WIN",   "AI. SpaceFactory (New York) won first place",       CHAL, "SpaceFactory",  "confirmed"),
 ("CH-PRIZE", "First prize $500,000",                              CHAL, "$500,000",      "confirmed"),
 ("CH-DATE",  "Release dated May 4, 2019",                         CHAL, "2019",          "confirmed"),
 ("CH-MAT",   "Recyclables and materials found on deep-space destinations", CHAL, "deep-space destinations", "confirmed"),
 ("CH-TESTS", "Tested for material mix, leakage, durability, strength", CHAL, "leakage",  "confirmed"),
 ("CH-START", "Challenge began 2015, three phases",                CHAL, "2015",          "confirmed"),
 ("Z-RANK",   "Team Zopherus placed first, virtual stage, July 2018", TOP5, "Zopherus",   "confirmed"),
 ("Z-HEX",    "Zopherus design described as modular, hexagonal, printed by a lander from Martian materials (Dezeen)",   ZOPH, "hexagonal",     "secondary"),
 ("Z-IAC",    "NASA IAC 2019 paper: Zopherus lander encloses the printer (PDF; string check may fail on PDF text encoding)", IAC19, "Zopherus", "confirmed"),
 ("Z-IMG",    "NASA-hosted Zopherus rendering exists (description of the picture is our reading)", ZIMG, None, "confirmed-by-user"),
 ("MOX-TOT",  "MOXIE made 122 grams of oxygen",                    MOX,  "122 grams",     "confirmed"),
 ("MOX-RUNS", "16 runs",                                           MOX,  "16th",          "confirmed"),
 ("MOX-RATE", "Up to 12 grams per hour",                           MOX,  "12 grams of oxygen an hour", "confirmed"),
 ("MOX-PUR",  "98% purity or better",                              MOX,  "98%",           "confirmed"),
 ("MOX-FINAL","Final run Aug. 7; article dated Sept. 6, 2023 (year of run inferred from article date)", MOX, "Aug. 7", "confirmed"),
 ("O2-NEED",  "Crew oxygen need per person per day (BVAD Table 3-27)", BVAD, None,        "unconfirmed"),
]

BANNED = [  # claims cut on 2026-10-13; must not reappear
 (r"114\s*GPa", "114 GPa figure"),
 (r"20[,\s]?000[- ]year", "20,000-year theorem"),
 (r"33\.516", "33.516 Hz prediction"),
 (r"six[- ]cycle|6[- ]cycle", "six-cycle claim"),
 (r"CHAPEA", "CHAPEA prediction"),
]

def offline():
    fails = 0
    def check(name, cond, detail):
        nonlocal fails
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}: {detail}")
        fails += (not cond)
    print("Arithmetic checks")
    check("184 K -> C", round(184 - 273.15) == -89, f"{184-273.15:.2f} C")
    check("242 K -> C", round(242 - 273.15) == -31, f"{242-273.15:.2f} C")
    check("6.36 mb < 1% of 1013.25 mb", 6.36 / 1013.25 < 0.01, f"{100*6.36/1013.25:.3f}%")
    check("24.6597 h rounds to 24.66", round(24.6597, 2) == 24.66, "24.66")
    check("hex area coefficient", abs(3*math.sqrt(3)/2 - 2.598) < 5e-4, f"{3*math.sqrt(3)/2:.4f}")
    # 7-module flower: centre + 6 neighbours
    dirs = [(1,0),(1,-1),(0,-1),(-1,0),(-1,1),(0,1)]
    cells = {(0,0)} | set(dirs)
    pairs = sum((q+dq, r+dr) in cells for q, r in cells for dq, dr in dirs) // 2
    ext = 6*len(cells) - 2*pairs
    check("flower shared pairs = 12", pairs == 12, str(pairs))
    check("flower outside faces = 18 of 42", ext == 18, f"{ext} of {6*len(cells)}")
    check("outside-wall saving = 57%", round(100*(1 - ext/42)) == 57, f"{100*(1-ext/42):.1f}%")
    return fails

def scan(paths):
    hits = 0
    print("Banned-claim scan")
    for p in paths:
        try:
            txt = open(p, encoding="utf-8", errors="replace").read()
        except OSError as e:
            print(f"  [SKIP] {p}: {e}"); continue
        for pat, label in BANNED:
            for m in re.finditer(pat, txt, re.I):
                hits += 1
                print(f"  [FLAG] {os.path.basename(p)}: {label} -> ...{txt[max(0,m.start()-40):m.end()+40]!r}...")
        print(f"  scanned {os.path.basename(p)}")
    if not hits:
        print("  no banned claims found")
    return hits

def online():
    fails, cache = 0, {}
    print("Online source checks (exact-string search in raw page HTML)")
    for rid, claim, src, key, status in ROWS:
        if not key or not src.startswith("http"):
            print(f"  [----] {rid}: {status} ({claim})"); continue
        if src not in cache:
            try:
                req = urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0"})
                cache[src] = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
            except Exception as e:
                cache[src] = None; print(f"  [ERR ] could not fetch {src}: {e}")
        page = cache[src]
        if page is None:
            fails += 1; continue
        norm = re.sub(r"\s+", " ", page).replace("&nbsp;", " ").replace("&#8217;", "'")
        ok = key in norm
        fails += (not ok)
        print(f"  [{'PASS' if ok else 'FAIL'}] {rid}: '{key}' {'found' if ok else 'NOT found'} ({status})")
    return fails

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    files = [os.path.join(here, "hex-habitat.html")] + [a for a in sys.argv[1:] if not a.startswith("--")]
    print("Figure table")
    for rid, claim, src, key, status in ROWS:
        print(f"  {rid:<10} {status:<11} {claim}")
    f = offline() + scan(files)
    if "--online" in sys.argv:
        f += online()
    print(f"\n{'ALL CHECKS PASSED' if f == 0 else f'{f} check(s) failed or flagged'}")
    sys.exit(1 if f else 0)
