#!/usr/bin/env python3
"""Run the 25 HVEH candidate coordinates (book4/ch07.html SITES) through tools/nyc_flood_map.py.
Same bathtub model, same levels. Siting question only: where does each coordinate sit relative to the lines.
Coordinates are the chapter's own, not geocoded; river outfalls sit on or beside open water by design, so
the point is read together with the nearest land (7x7 window, about +/-100 m).
  python3 book4/ch09b-sites.py --dem-dir ~/Downloads [--write]"""
import argparse, json, os, re, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
import nyc_flood_map as T

ORDER = ["today", "sandy_2012", "2050_central", "2050_high", "2050_storm_central", "2050_storm_high",
         "2150_central", "2150_high", "2150_storm_central", "2150_storm_high"]

def load_sites():
    src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ch07.html"), encoding="utf-8").read()
    pat = re.compile(r'\{id:(\d+),name:"([^"]*)",city:"([^"]*)",size:"([^"]*)",lat:([\d.]+),lng:(-[\d.]+)')
    rows = [dict(id=int(m[0]), name=m[1], city=m[2], size=m[3], lat=float(m[4]), lng=float(m[5])) for m in pat.findall(src)]
    assert len(rows) == 25, len(rows)
    return rows

LABEL = {"sandy_2012": ("Sandy 2012 peak", "Pico da Sandy 2012"), "2050_central": ("2050 central", "2050 central"),
         "2050_high": ("2050 high-end", "2050 alta"), "2050_storm_central": ("2050 central + Sandy-sized storm", "2050 central + tempestade tipo Sandy"),
         "2050_storm_high": ("2050 high-end + Sandy-sized storm", "2050 alta + tempestade tipo Sandy"), "2150_central": ("2150 central", "2150 central"),
         "2150_high": ("2150 high-end", "2150 alta"), "2150_storm_central": ("2150 central + Sandy-sized storm", "2150 central + tempestade tipo Sandy"),
         "2150_storm_high": ("2150 high-end + Sandy-sized storm", "2150 alta + tempestade tipo Sandy")}

def sites_html(doc):
    """Generated block: how many of the 25 candidate coordinates sit at a cell the bathtub floods, per line."""
    rows = ["<table class=\"dtab\" id=\"tab-sites\"><thead><tr><th><span data-l=\"en\">Line</span><span data-l=\"pt\">Linha</span></th>"
            "<th><span data-l=\"en\">Level (m, NAVD88)</span><span data-l=\"pt\">N&iacute;vel (m, NAVD88)</span></th>"
            "<th><span data-l=\"en\">Of 25 candidate coordinates, at a flooded cell</span><span data-l=\"pt\">Das 25 coordenadas candidatas, em c&eacute;lula alagada</span></th></tr></thead><tbody>"]
    for k in ORDER[1:]:
        rows.append("<tr><td><span data-l=\"en\">%s</span><span data-l=\"pt\">%s</span></td><td>%.3f</td><td>%d</td></tr>" %
                    (LABEL[k][0], LABEL[k][1], doc["levels_navd88_m"][k], doc["sites_at_flooded_cell"][k]))
    rows.append("</tbody></table>")
    return "\n".join(rows)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--dem-dir", required=True)
    ap.add_argument("--write", action="store_true"); a = ap.parse_args()
    dem = T.load_mosaic(os.path.expanduser(a.dem_dir)); res, fl = T.compute(dem); lv = T.levels()
    out = []
    for s in load_sites():
        i, j = T.ij(s["lng"], s["lat"])
        assert 0 <= i < T.H and 0 <= j < T.W, s
        win = (slice(max(i-3, 0), i+4), slice(max(j-3, 0), j+4))
        w = dem[win]; land = w[~fl["today"][win] & ~np.isnan(w)]
        r = dict(s); r["elev_m"] = round(float(dem[i, j]), 2); r["on_water_today"] = bool(fl["today"][i, j])
        r["nearest_land_min_m"] = round(float(land.min()), 2) if land.size else None
        r["nearest_land_median_m"] = round(float(np.median(land)), 2) if land.size else None
        r["flooded"] = {k: bool(fl[k][i, j]) for k in ORDER}
        r["land_flooded_share"] = {k: round(float((fl[k][win] & ~fl["today"][win]).sum() / max(land.size, 1)), 2) for k in ORDER if k != "today"}
        out.append(r)
    summ = {k: sum(r["flooded"][k] for r in out) for k in ORDER}
    summ_water = sum(r["on_water_today"] for r in out)
    doc = dict(generated_by="book4/ch09b-sites.py", levels_navd88_m=lv, n=len(out), on_water_today=summ_water,
               sites_at_flooded_cell=summ, sites=out)
    print("levels", {k: round(v, 3) for k, v in lv.items()})
    print("%-42s %-9s %5s %5s %5s  %s" % ("site", "city", "elev", "lmin", "lmed", "flooded at: " + ",".join(k.replace("_central","c").replace("_high","h").replace("_storm","s") for k in ORDER[1:])))
    for r in out:
        print("%-42s %-9s %5.2f %5s %5s  %s%s" % (r["name"][:42], r["city"], r["elev_m"], r["nearest_land_min_m"], r["nearest_land_median_m"],
              "".join("X" if r["flooded"][k] else "." for k in ORDER[1:]), "  [on water today]" if r["on_water_today"] else ""))
    print("count flooded per line:", summ, " on water today:", summ_water)
    if a.write:
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ch09b-sites.results.json")
        json.dump(doc, open(p, "w"), indent=1); print("wrote", p)
        T.write_block(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ch09b-flood-lines.html"), "flood-sites", sites_html(doc)); print("wrote flood-sites block")
if __name__ == "__main__":
    main()
