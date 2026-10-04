#!/usr/bin/env python3
"""
nyc_flood_map.py -- the instrument behind Book IV, Chapter 9b (the flood-line map).

What it does (a "bathtub" inundation, and nothing more):
  1. reads two USGS 3DEP 1 arc-second DEM tiles (n41w075, n41w074),
  2. cuts the map window  -74.30..-73.70 E, 40.45..40.95 N  at 1 arc-second,
  3. for each water level L (metres, NAVD88) marks every cell with elevation <= L
     that is 4-connected to the open sea (a seed cell in the Atlantic off Coney Island),
  4. writes the numbers (results.json) and, with --write, the picture assets
     (base image, nested increment masks, contour paths, elevation grid) into the
     marked generated block of book4/ch09b-flood-lines.html.

What it does NOT do: storm dynamics, tides, waves, rain, drainage, groundwater, sea walls,
pumps, subsidence, or any change of the land. A cell below L but not connected to the sea
is reported separately ("below level, not connected") and is never drawn as flooded.

Inputs that are READ from sources (see SOURCES): NOAA 2022 Table 2.2 and 2.5 (Northeast),
NOAA CO-OPS datums for The Battery 8518750 (MHHW, NAVD88, recorded maximum).
Inputs that are NOT read from the DEM file: the vertical datum (USGS 3DEP documents NAVD88
for the contiguous US; the GeoTIFF carries only NAD83 horizontal keys).

Usage:
  python3 tools/nyc_flood_map.py --report                  # numbers only, writes results.json
  python3 tools/nyc_flood_map.py --write                   # numbers + assets into the chapter
  python3 tools/nyc_flood_map.py --dem-dir DIR --preview P # also write a PNG preview
Requires: numpy, scipy, tifffile, imagecodecs, scikit-image, Pillow
"""
import argparse, base64, gzip, io, json, os, re, sys
import numpy as np

# ---------------------------------------------------------------- inputs (read from sources)
SOURCES = {
  "noaa_2022": "Sweet et al. 2022, Global and Regional Sea Level Rise Scenarios for the United States "
               "(NOAA Technical Report NOS 01), section 2.0 Future Mean Sea Level: Table 2.2 (2050, regional) "
               "and Table 2.5 (2100, 2150, regional); relative to a year-2000 baseline; READ in full from the PDF.",
  "coops_battery": "NOAA CO-OPS station 8518750 (The Battery) datums, epoch 1983-2001, metres; "
                   "READ (JSON pasted by the user from the CO-OPS metadata API).",
}
# Table 2.2, Northeast, median, metres rel. to 2000: Low, Int-Low, Int, Int-High, High
NE_2050 = {"Low": 0.36, "Int-Low": 0.40, "Int": 0.43, "Int-High": 0.49, "High": 0.54}
# Table 2.5, Northeast, median
NE_2100 = {"Low": 0.6, "Int-Low": 0.8, "Int": 1.3, "Int-High": 1.6, "High": 2.1}
NE_2150 = {"Low": 0.9, "Int-Low": 1.3, "Int": 2.3, "Int-High": 2.7, "High": 3.7}
# CO-OPS datums, The Battery, metres above station datum
BATTERY = {"MHHW": 2.543, "NAVD88": 1.848, "MLLW": 1.002, "max": 5.282}   # max = 2012-10-30 (Sandy)

CENTRAL, HIGHEND = "Int", "High"
YEARS = (2050, 2150)

def mhhw_above_navd88():
    return round(BATTERY["MHHW"] - BATTERY["NAVD88"], 3)

def sandy_peak_navd88():
    return round(BATTERY["max"] - BATTERY["NAVD88"], 3)

def levels():
    """Water levels in metres NAVD88. Order within a year is nested: tide-central < tide-high <
    storm-central < storm-high (asserted by the verify script, not assumed)."""
    base = mhhw_above_navd88(); sandy = sandy_peak_navd88()
    rise = {2050: NE_2050, 2150: NE_2150}
    out = {"today": base, "sandy_2012": sandy}
    for y in YEARS:
        c, h = rise[y][CENTRAL], rise[y][HIGHEND]
        out[f"{y}_central"] = round(base + c, 3)
        out[f"{y}_high"] = round(base + h, 3)
        out[f"{y}_storm_central"] = round(sandy + c, 3)
        out[f"{y}_storm_high"] = round(sandy + h, 3)
    return out

# ---------------------------------------------------------------- geometry
LON0, LON1, LAT0, LAT1 = -74.30, -73.70, 40.45, 40.95
PX = 1 / 3600.0
TILES = (("USGS_1_n41w075.tif", -75.00166666698243), ("USGS_1_n41w074.tif", -74.00166666718229))
TILE_LAT0 = 41.00166666678416
SEED = (-73.97, 40.50)          # Atlantic off Coney Island; asserted <= MHHW baseline at load

def m_per_deg(lat):
    p = np.radians(lat)
    mlat = 111132.92 - 559.82 * np.cos(2 * p) + 1.175 * np.cos(4 * p)
    mlon = 111412.84 * np.cos(p) - 93.5 * np.cos(3 * p)
    return mlat, mlon

W = int(round((LON1 - LON0) / PX)); H = int(round((LAT1 - LAT0) / PX))
def ij(lon, lat):
    return int((LAT1 - lat) / PX), int((lon - LON0) / PX)

PLACES_PT = {"Newark Liberty airport": "Aeroporto de Newark Liberty", "Newark Penn Station": "Estação Newark Penn",
  "Harrison (Red Bull Arena)": "Harrison (Red Bull Arena)", "Belleville (town centre)": "Belleville (centro)",
  "Hoboken (terminal)": "Hoboken (terminal)", "Lower Manhattan (Battery Park)": "Baixo Manhattan (Battery Park)",
  "Staten Island (St. George)": "Staten Island (St. George)", "LaGuardia airport": "Aeroporto LaGuardia",
  "JFK airport": "Aeroporto JFK", "Coney Island": "Coney Island"}
PLACES = [  # typed from memory, +/- ~100 m; NOT geocoded. Used for orientation, not for claims about parcels.
  ("Newark Liberty airport", -74.1745, 40.6895),
  ("Newark Penn Station", -74.1646, 40.7347),
  ("Harrison (Red Bull Arena)", -74.1503, 40.7367),
  ("Belleville (town centre)", -74.1503, 40.7940),
  ("Hoboken (terminal)", -74.0292, 40.7357),
  ("Lower Manhattan (Battery Park)", -74.0170, 40.7033),
  ("Staten Island (St. George)", -74.0735, 40.6437),
  ("LaGuardia airport", -73.8740, 40.7769),
  ("JFK airport", -73.7781, 40.6413),
  ("Coney Island", -73.9707, 40.5755),
]

def load_mosaic(dem_dir):
    import tifffile
    M = np.full((H, W), np.nan, np.float32)
    lons = LON0 + (np.arange(W) + 0.5) * PX
    lats = LAT1 - (np.arange(H) + 0.5) * PX
    used = 0
    for fn, lon0 in TILES:
        a = tifffile.imread(os.path.join(dem_dir, fn)).astype(np.float32)
        a[a < -1e5] = np.nan
        jj = np.floor((lons - lon0) / PX).astype(int); ii = np.floor((TILE_LAT0 - lats) / PX).astype(int)
        cols = np.where((jj >= 0) & (jj < a.shape[1]))[0]; rows = np.where((ii >= 0) & (ii < a.shape[0]))[0]
        if len(cols) == 0 or len(rows) == 0:
            continue
        sub = a[np.ix_(ii[rows], jj[cols])]
        cur = M[np.ix_(rows, cols)]
        M[np.ix_(rows, cols)] = np.where(np.isnan(cur), sub, cur)
        used += 1
    if used != 2:
        raise SystemExit("expected both tiles to contribute; used %d" % used)
    return M

# ---------------------------------------------------------------- the one algorithm
def connected_flood(dem, level, seed_ij):
    """Cells with dem <= level that are 4-connected to the seed cell. Raises if the seed itself is
    above the level (a seed on dry land would silently return nothing -- an empty check is not a pass)."""
    from scipy import ndimage as ndi
    if np.isnan(dem[seed_ij]) or dem[seed_ij] > level:
        raise ValueError("seed cell is above the water level (%.3f > %.3f)" % (dem[seed_ij], level))
    lab, _ = ndi.label(np.nan_to_num(dem, nan=1e9) <= level)   # default structure = 4-connectivity
    return lab == lab[seed_ij]

def below_level(dem, level):
    return np.nan_to_num(dem, nan=1e9) <= level

def cell_area_km2(mask):
    rows = np.where(mask.any(axis=1))[0]
    if rows.size == 0:
        return 0.0
    lat = LAT1 - (np.arange(H) + 0.5) * PX
    mlat, mlon = m_per_deg(lat)
    per_row = mask.sum(axis=1) * (mlat * PX) * (mlon * PX)
    return float(per_row.sum() / 1e6)

# ---------------------------------------------------------------- results
def compute(dem):
    seed = ij(*SEED)
    lv = levels()
    if not dem[seed] <= lv["today"]:
        raise SystemExit("seed not at/below baseline MHHW")
    floods = {k: connected_flood(dem, v, seed) for k, v in lv.items()}
    res = {"generated_by": "tools/nyc_flood_map.py", "window": [LON0, LAT0, LON1, LAT1],
           "grid": [W, H], "pixel_arcsec": 1, "seed": {"lonlat": SEED, "elevation_m": float(dem[seed])},
           "sources": SOURCES, "inputs": {"NE_2050": NE_2050, "NE_2100": NE_2100, "NE_2150": NE_2150, "battery": BATTERY},
           "mhhw_above_navd88_m": mhhw_above_navd88(), "sandy_peak_navd88_m": sandy_peak_navd88(), "levels_navd88_m": lv}
    base_area = cell_area_km2(floods["today"])
    res["area_km2"] = {k: round(cell_area_km2(m), 1) for k, m in floods.items()}
    res["added_over_today_km2"] = {k: round(cell_area_km2(m) - base_area, 1) for k, m in floods.items() if k != "today"}
    res["below_not_connected_km2"] = {k: round(cell_area_km2(below_level(dem, v) & ~floods[k]) - 0.0, 1)
                                      for k, v in lv.items()}
    places = []
    for name, lo, la in PLACES:
        i, j = ij(lo, la); nb = dem[max(i-1,0):i+2, max(j-1,0):j+2]
        row = {"name": name, "lonlat": [lo, la], "elev_m": round(float(dem[i, j]), 2),
               "elev_3x3_min_m": round(float(np.nanmin(nb)), 2), "elev_3x3_max_m": round(float(np.nanmax(nb)), 2)}
        for k in lv:
            row["flooded_" + k] = bool(floods[k][i, j])
            row["below_" + k] = bool(dem[i, j] <= lv[k])
        places.append(row)
    res["places"] = places
    return res, floods

# ---------------------------------------------------------------- picture assets
def png_bytes(img):
    b = io.BytesIO(); img.save(b, "PNG", optimize=True); return b.getvalue()

def b64(b): return base64.b64encode(b).decode("ascii")

def hillshade(dem):
    lat = LAT1 - (np.arange(H) + 0.5) * PX
    mlat, mlon = m_per_deg(lat)
    dy = mlat * PX; dx = (mlon * PX)[:, None]
    z = np.nan_to_num(dem, nan=0.0)
    gy, gx = np.gradient(z, float(dy.mean()))
    gx = np.gradient(z, axis=1) / dx
    az, alt = np.radians(315), np.radians(40)
    slope = np.arctan(np.hypot(gx, gy) * 2.0)           # vertical exaggeration 2
    aspect = np.arctan2(gy, -gx)
    hs = np.sin(alt) * np.cos(slope) + np.cos(alt) * np.sin(slope) * np.cos(az - aspect)
    return np.clip(hs, 0, 1)

def make_assets(dem, floods, lv):
    from PIL import Image
    from skimage import measure
    sea0 = floods["today"]
    hs = hillshade(dem)
    base = np.zeros((H, W, 3), np.float32)
    land = np.array([0.93, 0.91, 0.86], np.float32)
    shade = (0.62 + 0.38 * hs)[..., None]
    base[:] = land * shade
    hi = np.clip((np.nan_to_num(dem, nan=0) - 6.0) / 60.0, 0, 1)[..., None]      # gently darken high ground
    base = base * (1 - 0.18 * hi) + np.array([0.55, 0.62, 0.5], np.float32) * 0.18 * hi * shade
    base[sea0] = np.array([0.69, 0.80, 0.89])
    base_img = Image.fromarray((np.clip(base, 0, 1) * 255).astype(np.uint8), "RGB")
    bj = io.BytesIO(); base_img.save(bj, "JPEG", quality=70, optimize=True)
    assets = {"w": W, "h": H, "window": [LON0, LAT0, LON1, LAT1], "base": "data:image/jpeg;base64," + b64(bj.getvalue()),
              "levels": lv, "years": {}}
    palette = {"tide_central": (36, 99, 168, 150), "tide_high": (226, 140, 36, 150),
               "storm_central": (200, 70, 110, 120), "storm_high": (232, 150, 170, 110)}
    for y in YEARS:
        spec = [("tide_central", f"{y}_central", "today"),
                ("tide_high", f"{y}_high", f"{y}_central"),
                ("storm_central", f"{y}_storm_central", f"{y}_central"),
                ("storm_high", f"{y}_storm_high", f"{y}_high")]
        layers = []
        for name, key, over in spec:
            inc = floods[key] & ~floods[over]
            r, g, b, a = palette[name]
            rgba = np.zeros((H, W, 4), np.uint8); rgba[inc] = (r, g, b, a)
            im = Image.fromarray(rgba, "RGBA")
            layers.append({"name": name, "level_m": lv[key], "over": over, "png": "data:image/png;base64," + b64(png_bytes(im)),
                           "path": contour_path(floods[key], measure)})
        assets["years"][str(y)] = layers
    # elevation grid for the click read-out: 3x block mean, decimetres, int16, gzip
    k = 3; hh, ww = H // k, W // k
    z = np.nan_to_num(dem[:hh*k, :ww*k], nan=0.0).reshape(hh, k, ww, k).mean(axis=(1, 3))
    wfrac = floods["today"][:hh*k, :ww*k].reshape(hh, k, ww, k).mean(axis=(1, 3))
    z10 = np.clip(np.round(z * 10), -299, 4000).astype(np.int16)
    z10[wfrac > 0.5] = -300            # sentinel: open water at today's MHHW (the page says "water", not "0.0 m")
    assets["elev"] = {"w": ww, "h": hh, "k": k, "unit_dm": True,
                      "gz_b64": b64(gzip.compress(z10.tobytes(), 9, mtime=0))}
    assets["today_path"] = contour_path(floods["today"], measure)
    assets["sandy_path"] = contour_path(floods["sandy_2012"], measure)
    off = {"Newark Penn Station": (-14, -6, "end"), "Harrison (Red Bull Arena)": (14, 34, "start"),
           "Hoboken (terminal)": (14, -8, "start"), "Lower Manhattan (Battery Park)": (14, 30, "start")}
    assets["places"] = [{"name": n, "x": round((lo - LON0) / PX, 1), "y": round((LAT1 - la) / PX, 1),
                         "dx": off.get(n, (14, 9, "start"))[0], "dy": off.get(n, (14, 9, "start"))[1],
                         "anchor": off.get(n, (14, 9, "start"))[2]} for n, lo, la in PLACES]
    return assets

def contour_path(mask, measure, tol=1.2, min_len=18):
    cs = measure.find_contours(np.pad(mask.astype(np.float32), 1), 0.5)
    parts = []
    for c in cs:
        c = measure.approximate_polygon(c, tol)
        if len(c) < 4 or len(c) < min_len // 6:
            continue
        if max(np.ptp(c[:, 0]), np.ptp(c[:, 1])) < 8:
            continue
        pts = [(int(round(x - 1)), int(round(y - 1))) for y, x in c]     # (row,col)->(x,y), undo pad
        d = "M%d %d" % pts[0]; px_, py_ = pts[0]
        for x, y in pts[1:]:
            d += "l%d %d" % (x - px_, y - py_); px_, py_ = x, y
        parts.append(d + "z")
    return "".join(parts)

def _markers(name):
    return ("<!-- BEGIN %s (generated by tools/nyc_flood_map.py --write; do not edit) -->" % name, "<!-- END %s -->" % name)

def write_block(chapter, name, content):
    B, E = _markers(name)
    s = open(chapter, encoding="utf-8").read()
    if B not in s or E not in s:
        raise SystemExit("chapter lacks the BEGIN/END %s markers" % name)
    block = B + "\n" + content + "\n" + E
    s = re.sub(re.escape(B) + r".*?" + re.escape(E), lambda m: block, s, flags=re.S)
    open(chapter, "w", encoding="utf-8").write(s)

FT = 3.28084
def ft(m): return "%.1f" % (m * FT)

LEVEL_ROWS = [  # key, EN label, PT label, rise-table (year) or None
  ("today", "Today: mean higher high water", "Hoje: preamar média mais alta", None),
  ("sandy_2012", "Sandy, 30 Oct 2012: recorded peak at The Battery", "Sandy, 30 out 2012: pico registrado em The Battery", None),
  ("2050_central", "2050, central (NOAA Intermediate)", "2050, central (Intermediário da NOAA)", 2050),
  ("2050_high", "2050, high-end (NOAA High)", "2050, cenário alto (Alto da NOAA)", 2050),
  ("2150_central", "2150, central (NOAA Intermediate)", "2150, central (Intermediário da NOAA)", 2150),
  ("2150_high", "2150, high-end (NOAA High)", "2150, cenário alto (Alto da NOAA)", 2150),
  ("2050_storm_central", "2050 central + a Sandy-sized storm", "2050 central + uma tempestade do tamanho da Sandy", 2050),
  ("2050_storm_high", "2050 high-end + a Sandy-sized storm", "2050 alto + uma tempestade do tamanho da Sandy", 2050),
  ("2150_storm_central", "2150 central + a Sandy-sized storm", "2150 central + uma tempestade do tamanho da Sandy", 2150),
  ("2150_storm_high", "2150 high-end + a Sandy-sized storm", "2150 alto + uma tempestade do tamanho da Sandy", 2150),
]

def numbers_html(res):
    lv = res["levels_navd88_m"]; add = res["added_over_today_km2"]; inp = res["inputs"]
    rise = {2050: inp["NE_2050"], 2150: inp["NE_2150"]}
    def risev(key):
        if "central" in key: return rise[int(key[:4])]["Int"]
        if "high" in key: return rise[int(key[:4])]["High"]
        return None
    o = ['<table class="dtab" id="tab-levels"><thead><tr>'
         '<th><span data-l="en">Line</span><span data-l="pt">Linha</span></th>'
         '<th><span data-l="en">Sea-level rise since 2000 (m)</span><span data-l="pt">Elevação do mar desde 2000 (m)</span></th>'
         '<th><span data-l="en">Water level, NAVD88 (m / ft)</span><span data-l="pt">Nível da água, NAVD88 (m / pés)</span></th>'
         '<th><span data-l="en">Land added to the water (km&sup2;)</span><span data-l="pt">Terra coberta além de hoje (km&sup2;)</span></th>'
         '</tr></thead><tbody>']
    for key, en, pt, yr in LEVEL_ROWS:
        r = risev(key) if yr else None
        o.append('<tr><td><span data-l="en">%s</span><span data-l="pt">%s</span></td><td>%s</td><td>%.3f / %s</td><td>%s</td></tr>' % (
            en, pt, ("%.2f" % r) if r is not None else "&mdash;", lv[key], ft(lv[key]),
            ("%.1f" % add[key]) if key in add else "&mdash;"))
    o.append('</tbody></table>')
    cols = [("sandy_2012", "Sandy 2012", "Sandy 2012"), ("2050_central", "2050 c", "2050 c"), ("2050_high", "2050 h", "2050 a"),
            ("2150_central", "2150 c", "2150 c"), ("2150_high", "2150 h", "2150 a"),
            ("2050_storm_central", "2050 c+S", "2050 c+S"), ("2050_storm_high", "2050 h+S", "2050 a+S"),
            ("2150_storm_central", "2150 c+S", "2150 c+S"), ("2150_storm_high", "2150 h+S", "2150 a+S")]
    o.append('<table class="dtab" id="tab-places"><thead><tr><th><span data-l="en">Place (approximate position)</span><span data-l="pt">Lugar (posi&ccedil;&atilde;o aproximada)</span></th>'
             '<th><span data-l="en">Ground (m / ft)</span><span data-l="pt">Terreno (m / p&eacute;s)</span></th>' +
             "".join('<th><span data-l="en">%s</span><span data-l="pt">%s</span></th>' % (e, p) for _, e, p in cols) + '</tr></thead><tbody>')
    for pl in res["places"]:
        cells = []
        for k, _, _ in cols:
            cells.append("&#9679;" if pl["flooded_" + k] else ("&#9676;" if pl["below_" + k] else "&middot;"))
        o.append('<tr><td><span data-l="en">%s</span><span data-l="pt">%s</span></td><td>%.1f / %s</td>%s</tr>' % (
            pl["name"], PLACES_PT.get(pl["name"], pl["name"]), pl["elev_m"], ft(pl["elev_m"]),
            "".join("<td>%s</td>" % c for c in cells)))
    o.append('</tbody></table>')
    return "\n".join(o)

def main():
    here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
    ap = argparse.ArgumentParser()
    ap.add_argument("--dem-dir", default=os.path.expanduser("~/Downloads"))
    ap.add_argument("--results", default=os.path.join(root, "book4", "ch09b-flood-lines.results.json"))
    ap.add_argument("--chapter", default=os.path.join(root, "book4", "ch09b-flood-lines.html"))
    ap.add_argument("--report", action="store_true"); ap.add_argument("--write", action="store_true")
    ap.add_argument("--preview")
    a = ap.parse_args()
    dem = load_mosaic(a.dem_dir)
    assert dem.shape == (H, W) and np.isnan(dem).mean() < 0.01
    res, floods = compute(dem)
    json.dump(res, open(a.results, "w"), indent=1, sort_keys=True)
    print("levels (m NAVD88):", json.dumps(res["levels_navd88_m"]))
    print("added over today (km2):", json.dumps(res["added_over_today_km2"]))
    for p in res["places"]:
        print("%-34s elev %6.2f  " % (p["name"], p["elev_m"]) + " ".join(
            ("F" if p["flooded_" + k] else ("b" if p["below_" + k] else ".")) for k in res["levels_navd88_m"]))
    if a.write or a.preview:
        assets = make_assets(dem, floods, res["levels_navd88_m"])
        sz = {k: len(json.dumps(v)) for k, v in assets.items() if k != "years"}
        print("asset sizes (chars):", sz, {y: sum(len(l["png"]) + len(l["path"]) for l in L) for y, L in assets["years"].items()})
        if a.write:
            write_block(a.chapter, "flood-data", "<script>window.FLOOD=" + json.dumps(assets, separators=(",", ":")) + ";</script>")
            write_block(a.chapter, "flood-numbers", numbers_html(res)); print("wrote blocks into", a.chapter)
        if a.preview:
            from PIL import Image
            def dec(u): return Image.open(io.BytesIO(base64.b64decode(u.split(",", 1)[1])))
            im = dec(assets["base"]).convert("RGBA")
            for L in assets["years"]["2150"]:
                im = Image.alpha_composite(im, dec(L["png"]).convert("RGBA"))
            im.convert("RGB").resize((W // 2, H // 2)).save(a.preview)
    return 0

if __name__ == "__main__":
    sys.exit(main())
