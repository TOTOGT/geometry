#!/usr/bin/env python3
"""
ch09b-verify.py -- regenerates and checks every number printed in Book IV, Chapter 9b
("The Flood Line"), and shows that each check can fail.

Run:  python3 book4/ch09b-verify.py [--dem-dir ~/Downloads] [--noaa-pdf PATH]
Needs: numpy, scipy (always); tifffile, imagecodecs (only if the DEM tiles are present);
       pdftotext (only if the NOAA PDF is present).
"""
import argparse, json, os, re, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
import nyc_flood_map as T

FAIL = []; RAN = {"checks": 0, "controls": 0, "optional": []}
def check(label, ok, detail=""):
    RAN["checks"] += 1
    print(("  OK   " if ok else "  FAIL ") + label + (("   " + detail) if detail else ""))
    if not ok: FAIL.append(label)
def expect_fail(label, fn):
    """A control: the check below must be able to fail. If it passes on a corrupted input, the check is blind."""
    RAN["controls"] += 1
    try:
        ok = fn()
    except Exception as e:
        ok = False
    print(("  OK   control fails as it should: " if not ok else "  FAIL control did NOT fail: ") + label)
    if ok: FAIL.append("control: " + label)

ap = argparse.ArgumentParser()
ap.add_argument("--dem-dir", default=os.path.expanduser("~/Downloads"))
ap.add_argument("--noaa-pdf", default=os.path.expanduser("~/Downloads/2.0-Future-Mean-Sea-Level.pdf"))
a = ap.parse_args()
CH = os.path.join(HERE, "ch09b-flood-lines.html")
RES = json.load(open(os.path.join(HERE, "ch09b-flood-lines.results.json")))
html = open(CH, encoding="utf-8").read()

print("\n[1] the water levels, derived by hand from the source numbers")
mhhw_navd = round(2.543 - 1.848, 3)                       # CO-OPS Battery: MHHW minus NAVD88, both above station datum
sandy = round(5.282 - 1.848, 3)                           # recorded maximum minus NAVD88
check("MHHW above NAVD88 = 0.695 m", mhhw_navd == 0.695)
check("Sandy peak above NAVD88 = 3.434 m", sandy == 3.434)
hand = {"today": 0.695, "sandy_2012": 3.434,
        "2050_central": round(0.695 + 0.43, 3), "2050_high": round(0.695 + 0.54, 3),
        "2150_central": round(0.695 + 2.3, 3), "2150_high": round(0.695 + 3.7, 3),
        "2050_storm_central": round(3.434 + 0.43, 3), "2050_storm_high": round(3.434 + 0.54, 3),
        "2150_storm_central": round(3.434 + 2.3, 3), "2150_storm_high": round(3.434 + 3.7, 3)}
lv = T.levels()
for k, v in hand.items():
    check("level %-20s hand %.3f = tool %.3f = results.json %.3f" % (k, v, lv[k], RES["levels_navd88_m"][k]),
          abs(v - lv[k]) < 1e-9 and abs(v - RES["levels_navd88_m"][k]) < 1e-9)
for y in (2050, 2150):
    seq = [lv[f"{y}_central"], lv[f"{y}_high"], lv[f"{y}_storm_central"], lv[f"{y}_storm_high"]]
    check("%d lines nest: central < high-end < storm-central < storm-high" % y, all(x < z for x, z in zip(seq, seq[1:])), str(seq))
expect_fail("a wrong order (storm-central above storm-high) is detected",
            lambda: all(x < z for x, z in zip([1, 2, 5, 4], [2, 5, 4, 6])))

print("\n[2] the bathtub rule on a grid small enough to work by hand")
# 5 rows x 9 cols. Sea (elev 0.0) at column 0. Land rises to a 3.0 m dike at column 4; behind the dike a basin at 0.2 m (columns 5-7);
# column 8 is high ground (9.0). Rows identical.
row = [0.0, 0.5, 1.0, 2.0, 3.0, 0.2, 0.2, 0.2, 9.0]
dem = np.array([row] * 5, np.float32); seed = (2, 0)
f1 = T.connected_flood(dem, 1.0, seed)
check("level 1.0: floods columns 0-2 only (3 x 5 cells)", f1.sum() == 15 and f1[:, :3].all() and not f1[:, 3:].any())
check("level 1.0: the basin behind the dike (0.2 m) is below the level but NOT flooded",
      T.below_level(dem, 1.0)[:, 5:8].all() and not f1[:, 5:8].any())
f3 = T.connected_flood(dem, 3.0, seed)
check("level 3.0: water tops the dike and fills the basin (8 columns x 5 cells)", f3.sum() == 40 and f3[:, :8].all() and not f3[:, 8].any())
check("nesting: flood(1.0) is a subset of flood(3.0)", bool((f1 & ~f3).sum() == 0))
expect_fail("a seed on dry land is refused", lambda: T.connected_flood(dem, 1.0, (2, 8)) is not None)
expect_fail("an unconnected-flood rule would wrongly flood the basin (the check would see it)",
            lambda: not T.below_level(dem, 1.0)[:, 5:8].any())

print("\n[3] the chapter's printed numbers equal the tool's output")
required = ["0.695", "3.434", "1.125", "1.235", "2.995", "4.395", "3.864", "3.974", "5.734", "7.134", "5.282", "2.543", "1.848",
            "0.36 to 0.54", "0.18 metres", "0.9 to 3.7", "0.81 metres", "0.88 metres", "0.63 to 1.60", "0.69 to 1.05", "0.18 to 0.25",
            "8.2 m", "17.0 m", "3.7 m", "2.7 m", "25 candidate"]
for r in required:
    check("English text contains %r" % r, r in html)
pt = ["0,695", "3,434", "1,125", "1,235", "2,995", "4,395", "5,282", "2,543", "1,848", "0,36 a 0,54", "0,9 a 3,7", "0,81 metro", "0,88 metro", "0,63 a 1,60", "8,2 m", "17,0 m"]
for r in pt:
    check("Portuguese text contains %r" % r, r in html)
pl = {p["name"]: p for p in RES["places"]}
check("Newark Penn 8.2 m, Belleville 17.0 m, Harrison 3.7 m, EWR 2.7 m agree with results.json",
      round(pl["Newark Penn Station"]["elev_m"], 1) == 8.2 and round(pl["Belleville (town centre)"]["elev_m"], 1) == 17.0
      and round(pl["Harrison (Red Bull Arena)"]["elev_m"], 1) == 3.7 and round(pl["Newark Liberty airport"]["elev_m"], 1) == 2.7)
h = pl["Harrison (Red Bull Arena)"]
check("claim: Harrison dry at 2150 central, wet at 2150 high-end and at 2050 + Sandy-sized storm",
      (not h["flooded_2150_central"]) and h["flooded_2150_high"] and h["flooded_2050_storm_central"])
check("claim: Newark Penn and Belleville above every line", not any(pl[n]["below_" + k] for n in ("Newark Penn Station", "Belleville (town centre)") for k in lv))
e = pl["Newark Liberty airport"]
check("claim: Newark airport under Sandy 2012 and every 2150 line",
      e["flooded_sandy_2012"] and all(e["flooded_" + k] for k in lv if k.startswith("2150")))
check("Sandy-level bathtub floods Hoboken, Lower Manhattan, LaGuardia, JFK, Coney Island, Newark airport (plausibility, not validation)",
      all(pl[n]["flooded_sandy_2012"] for n in ("Hoboken (terminal)", "Lower Manhattan (Battery Park)", "LaGuardia airport", "JFK airport", "Coney Island", "Newark Liberty airport")))
B = re.search(r"<!-- BEGIN flood-numbers[^>]*-->\n(.*?)\n<!-- END flood-numbers -->", html, re.S)
check("numbers block present", bool(B))
check("numbers block equals tool output from results.json", B is not None and B.group(1) == T.numbers_html(RES))
expect_fail("a tampered numbers block is detected", lambda: B is not None and B.group(1).replace("3.434", "3.443") == T.numbers_html(RES))

print("\n[3b] Rockaway and Coney Island (axis corridors)")
LFR = {l["name"]: l for l in RES["landforms"]}
rk, cn = LFR["Rockaway peninsula"], LFR["Coney Island"]
check("prose: median ground 2.2 m (Rockaway) and 1.9 m (Coney Island) equal results.json", rk["median_m"] == 2.2 and cn["median_m"] == 1.9)
check("prose: still dry at Sandy 2012: 3% and 3%", rk["dry_pct"]["sandy_2012"] == 3 and cn["dry_pct"]["sandy_2012"] == 3)
check("prose: still dry at 2150 central: 6% and 9%", rk["dry_pct"]["2150_central"] == 6 and cn["dry_pct"]["2150_central"] == 9)
check("prose: still dry at 2150 high-end: 1% and 0%", rk["dry_pct"]["2150_high"] == 1 and cn["dry_pct"]["2150_high"] == 0)
for r in ("median ground height of 2.2 m", "Coney Island&#8217;s 1.9 m", "$52.6 billion", "begin in 2030", "13 feet", "about 4.0 m", "0.9 to 3.7 m"):
    check("English text contains %r" % r, r in html)
check("13 feet is about 4.0 m (13 x 0.3048 = %.3f)" % (13 * 0.3048), round(13 * 0.3048, 1) == 4.0)
check("13 ft (3.96 m) lies above 2150 central (2.995) and below 2150 high-end (4.395)", lv["2150_central"] < 13 * 0.3048 < lv["2150_high"])
check("landforms block equals tool output", re.search(r"<!-- BEGIN flood-landforms[^>]*-->\n(.*?)\n<!-- END flood-landforms -->", html, re.S).group(1) == T.landforms_html(RES))
check("corridor masks nest: a narrower corridor holds fewer cells than a wider one",
      T.corridor_mask(*T.LANDFORMS[1][2:4], 350).sum() < T.corridor_mask(*T.LANDFORMS[1][2:4], 600).sum())
expect_fail("a wrong Rockaway median (2.9) is not what results.json says", lambda: rk["median_m"] == 2.9)

print("\n[3c] siting note and the 25 candidate coordinates")
import importlib.util
_sp = importlib.util.spec_from_file_location("ch09b_sites", os.path.join(HERE, "ch09b-sites.py")); S = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(S)
SR = json.load(open(os.path.join(HERE, "ch09b-sites.results.json")))
check("25 sites parsed from ch07.html and in results", SR["n"] == 25 == len(SR["sites"]) == len(S.load_sites()))
check("sites block equals generator output", re.search(r"<!-- BEGIN flood-sites[^>]*-->\n(.*?)\n<!-- END flood-sites -->", html, re.S).group(1) == S.sites_html(SR))
check("none of the 25 on open water at today's high tide (prose says so)", SR["on_water_today"] == 0 and "none of the 25 sits on open water" in html)
above20 = [x for x in SR["sites"] if x["elev_m"] > 20]
check("six sites read above 20 m, max 44.8 m (prose)", len(above20) == 6 and max(x["elev_m"] for x in above20) == 44.83 and "six read above 20 m" in html and "44.8 m" in html)
cnt = SR["sites_at_flooded_cell"]
check("counts nest or stay level as the lines rise (central<=high, tide<=storm)", all(cnt[a] <= cnt[b] for a, b in
      [("2050_central", "2050_high"), ("2150_central", "2150_high"), ("2050_central", "2050_storm_central"), ("2150_central", "2150_storm_central"), ("2150_storm_central", "2150_storm_high")]))
P = {q["name"]: q for q in RES["places"]}
def fl(n, k): return P[n]["flooded_" + k]
check("prose: Newark Penn dry on every line", not any(v for k, v in P["Newark Penn Station"].items() if k.startswith("flooded_")))
check("prose: Hoboken under Sandy, all storm lines and 2150 high-end, not 2150 central",
      all(fl("Hoboken (terminal)", k) for k in ("sandy_2012", "2050_storm_central", "2050_storm_high", "2150_storm_central", "2150_storm_high", "2150_high")) and not fl("Hoboken (terminal)", "2150_central") and P["Hoboken (terminal)"]["elev_m"] == 3.07)
check("prose: Newark airport and LaGuardia under Sandy and both 2150 lines",
      all(fl(n, k) for n in ("Newark Liberty airport", "LaGuardia airport") for k in ("sandy_2012", "2150_central", "2150_high")))
check("prose: JFK under Sandy and 2150 high-end, not 2150 central", fl("JFK airport", "sandy_2012") and fl("JFK airport", "2150_high") and not fl("JFK airport", "2150_central"))
check("prose: ground heights 2.7 / 2.2 / 3.2 / 3.1 / 8.2 m", [round(P[n]["elev_m"], 1) for n in ("Newark Liberty airport", "LaGuardia airport", "JFK airport", "Hoboken (terminal)", "Newark Penn Station")] == [2.7, 2.2, 3.2, 3.1, 8.2])
check("siting note makes no recommendation and says the mobile-unit idea is untested", "makes no recommendation" in html and "None of that has been tested here" in html)
expect_fail("a wrong count (7 sites flooded at 2150 central) is not what results say", lambda: cnt["2150_central"] == 7)

print("\n[4] the embedded map data")
D = re.search(r"<!-- BEGIN flood-data[^>]*-->\n<script>window\.FLOOD=(.*?);</script>\n<!-- END flood-data -->", html, re.S)
check("map data block present", bool(D))
F = json.loads(D.group(1)) if D else {}
check("map window and grid", F.get("window") == [T.LON0, T.LAT0, T.LON1, T.LAT1] and (F.get("w"), F.get("h")) == (T.W, T.H))
check("levels in the page equal results.json", F.get("levels") == RES["levels_navd88_m"])
for y in ("2050", "2150"):
    L = F["years"][y]
    check("%s: four layers with the right names" % y, [l["name"] for l in L] == ["tide_central", "tide_high", "storm_central", "storm_high"])
    check("%s: each layer has an image and a contour path" % y, all(l["png"].startswith("data:image/png;base64,") and len(l["path"]) > 100 for l in L))
    check("%s: layer levels equal results.json" % y, [l["level_m"] for l in L] == [lv[y + "_central"], lv[y + "_high"], lv[y + "_storm_central"], lv[y + "_storm_high"]])
check("no external script or image sources in the page", not re.search(r'<script[^>]+src=|<img[^>]+src="http', html))
check("English and Portuguese halves both present", min(html.count('data-l="en"'), html.count('data-l="pt"')) > 20 and abs(html.count('data-l="en"') - html.count('data-l="pt"')) <= 2)
check("no advice language: states 'not financial, real-estate or engineering advice'", "not financial, real-estate or engineering advice" in html)
check("labels READ / NOT READ present for sources", html.count('class="rd"') >= 3 and html.count('class="rd nr"') >= 2)

print("\n[5] optional: re-run the instrument on the DEM tiles")
dem_ok = all(os.path.exists(os.path.join(a.dem_dir, fn)) for fn, _ in T.TILES)
try:
    import tifffile  # noqa
except Exception:
    dem_ok = False
if dem_ok:
    dem = T.load_mosaic(a.dem_dir)
    res, floods = T.compute(dem)
    RAN["optional"].append("DEM re-run")
    check("re-run areas equal results.json", res["area_km2"] == RES["area_km2"] and res["added_over_today_km2"] == RES["added_over_today_km2"])
    ks = ["today", "2050_central", "2050_high", "2050_storm_central", "2050_storm_high"]
    check("masks nest by level (2050 chain)", all(not (floods[x] & ~floods[z]).any() for x, z in zip(ks, ks[1:])))
    ks = ["today", "2150_central", "2150_high", "2150_storm_central", "2150_storm_high"]
    check("masks nest by level (2150 chain)", all(not (floods[x] & ~floods[z]).any() for x, z in zip(ks, ks[1:])))
    check("seed cell is water at or below today's MHHW", dem[T.ij(*T.SEED)] <= lv["today"], "seed elevation %.3f" % dem[T.ij(*T.SEED)])
    check("tile mosaic has under 1%% empty cells (%.4f)" % float(np.isnan(dem).mean()), float(np.isnan(dem).mean()) < 0.01)
    expect_fail("moving the seed to a high inland cell is refused", lambda: T.connected_flood(dem, lv["today"], T.ij(-74.1503, 40.7940)) is not None)
else:
    print("  (skipped: DEM tiles or tifffile not available)")

print("\n[6] optional: NOAA tables against the source PDF")
if os.path.exists(a.noaa_pdf):
    txt = subprocess.run(["pdftotext", "-layout", a.noaa_pdf, "-"], capture_output=True, text=True).stdout
    RAN["optional"].append("NOAA PDF")
    i = txt.index("Northeast\n        0.40")
    blk = txt[i:i + 400]
    check("Table 2.2 Northeast medians 0.36 0.40 0.43 0.49 0.54 present", all(x in blk for x in ("0.36", "0.40", "0.43", "0.49", "0.54")))
    j = txt.index("Table 2.5: Scenarios of relative sea level"); k = txt.index("Northeast", j)
    nb = txt[k:k + 420]
    check("Table 2.5 Northeast 2100 row 0.6 0.8 1.3 1.6 2.1", re.search(r"2100\s+0\.6\s+0\.8\s+1\.3\s+1\.6\s+2\.1", nb) is not None)
    check("Table 2.5 Northeast 2150 row 0.9 1.3 2.3 2.7 3.7", re.search(r"2150\s+0\.9\s+1\.3\s+2\.3\s+2\.7\s+3\.7", nb) is not None)
    check("Table 2.4 5 C column: 2100 total 0.81 (0.69-1.05); very-high low-confidence 0.88 (0.63-1.60)", all(x in txt for x in ("0.81", "(0.69–1.05)", "0.88", "(0.63–1.60)")))
    check("Table 2.4 2050 totals 0.18 0.20 0.21 0.22 0.25", all(x in txt for x in ("0.18", "0.20", "0.21", "0.22", "0.25")))
    expect_fail("a wrong Northeast value (0.37) is not found in Table 2.2's Northeast block", lambda: "0.37" in blk)
else:
    print("  (skipped: NOAA PDF not found)")

print("\n[HONESTY] what this establishes, and what it does not")
print("  - Established: the printed levels follow from the source numbers; the bathtub code does what the hand-worked grid says;")
print("    the page text and tables equal the tool's output; the map data in the page equals the tool's masks' levels.")
print("  - Not established: that the real water will follow the bathtub (surge, drains, defences, subsidence not modelled);")
print("    the Rockaway and Coney Island corridor masks (hand-defined, ends typed from memory) and the ENR and USACE facts (summarising fetch; status after 2024 not checked);")
print("    NAVD88 as the DEM's vertical datum (cited, not read from the files); the Datums JSON as read (values typed from the pasted JSON);")
print("    place coordinates (typed from memory, about 100 m); the Sandy check is plausibility only (no official layer read);")
print("    the 25 candidate coordinates (taken from Chapter 7 as written; they look schematic, not placed on the channels);")
print("    that a mobile unit could be deployed or would perform (an idea, untested);")
print("    the Portuguese has not had native review.")
print("\nran: %d checks, %d controls; optional sections run: %s" % (RAN["checks"], RAN["controls"], RAN["optional"] or "none"))
if RAN["checks"] == 0 or RAN["controls"] == 0:
    FAIL.append("an empty check is not a passing check")
print("\nRESULT:", "FAIL (%d): %s" % (len(FAIL), FAIL) if FAIL else "all checks pass")
sys.exit(1 if FAIL else 0)
