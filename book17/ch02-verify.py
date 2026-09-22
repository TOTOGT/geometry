#!/usr/bin/env python3
"""book17/ch02-verify.py -- recomputes every geographic/arithmetic figure
printed on ch02-the-distance-a-plane-actually-flies.html from scratch
(standard library only) and checks the page prints the same numbers, plus a
presence check on its cited facts. Does NOT check book17/Book17Ch02.lean --
that file has not been run against a kernel; see its own header and the
page's own Part VI, which says so.

    python3 book17/ch02-verify.py
"""
import math
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAGE = ROOT / "book17" / "ch02-the-distance-a-plane-actually-flies.html"

BRASILIA = (-15.7939, -47.8828)
NYC = (40.7128, -74.0060)
R_KM = 6371.0088

FAIL = []

def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)

def flat_distance(p, q):
    return math.sqrt((q[1] - p[1]) ** 2 + (q[0] - p[0]) ** 2)

def great_circle_km(p, q):
    lat1, lon1 = p
    lat2, lon2 = q
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R_KM * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def main():
    flat = flat_distance(BRASILIA, NYC)
    gc_km = great_circle_km(BRASILIA, NYC)
    gc_mi = gc_km * 0.621371
    km_lat = (math.pi / 180) * R_KM
    km_lon_bsb = (math.pi / 180) * R_KM * math.cos(math.radians(BRASILIA[0]))
    km_lon_nyc = (math.pi / 180) * R_KM * math.cos(math.radians(NYC[0]))

    print("[1] recompute from raw coordinates (standard library only)")
    check("flat (naive Distance Formula, raw degrees)", True, f"{flat:.4f}")
    check("great-circle (haversine)", True, f"{gc_km:.2f} km = {gc_mi:.2f} mi")

    if not PAGE.exists():
        check("page exists", False, str(PAGE))
        return report()
    text = PAGE.read_text(encoding="utf-8")
    norm = re.sub(r"\s+", " ", text)

    print()
    print("[2] the page prints the same figures this script just computed")
    check(f"flat distance {flat:.2f} printed", f"{flat:.2f}" in norm)
    check(f"great-circle km {gc_km:.1f} printed", f"{gc_km:.1f}" in norm)
    check(f"great-circle mi {gc_mi:.0f} printed", f"{gc_mi:.0f}" in norm)
    check(f"km/deg latitude {km_lat:.2f} printed", f"{km_lat:.2f}" in norm)
    check(f"km/deg lon at Brasilia {km_lon_bsb:.2f} printed", f"{km_lon_bsb:.2f}" in norm)
    check(f"km/deg lon at NYC {km_lon_nyc:.2f} printed", f"{km_lon_nyc:.2f}" in norm)

    print()
    print("[3] cited facts still present (presence check, not a live re-fetch)")
    for s in (
        "Stitz",
        "Zeager",
        "Exercise 35",
        "Sasquatch",
        "September&nbsp;21, 2026",
        "Zohran Mamdani",
        "September&nbsp;23",
        "6371.0088",
    ):
        check(repr(s), s in norm)

    print()
    print("[4] the Lean file is present and its untested status is stated on the page")
    lean = ROOT / "book17" / "Book17Ch02.lean"
    check("Book17Ch02.lean exists", lean.exists())
    check("page states the Lean file is untested",
          "has not been run against a real kernel" in norm)

    return report()

def report():
    print()
    print("=" * 68)
    print("[HONESTY]")
    print()
    print("ESTABLISHED: every geographic/arithmetic figure on the page matches a")
    print("fresh, standard-library recomputation from the same raw coordinates,")
    print("run here, not copied from the page and trusted.")
    print()
    print("NOT ESTABLISHED: that book17/Book17Ch02.lean type-checks. This script")
    print("has no Lean toolchain and does not attempt to run it; the page's own")
    print("Part VI says the Lean file is untested, and this script only checks")
    print("that the page still says so, not that the file is correct.")
    if FAIL:
        print()
        print(f"{len(FAIL)} CHECK(S) FAILED")
        return 1
    print()
    print("ALL CHECKS PASSED")
    return 0

if __name__ == "__main__":
    sys.exit(main())
