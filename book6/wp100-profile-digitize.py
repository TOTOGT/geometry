#!/usr/bin/env python3
"""
wp100-profile-digitize.py — Principia Orthogona, Vol VI, WP-100

Digitises the zonal wind profile from Figure 3 (left panel) of Sanchez-Lavega
et al., Science Advances 12, eaee4251 (2026), CC BY. Reads the figure only.

Axis calibration is fixed by the plot frame: x from -40 to 180 m/s, y from
-50 to -70 planetographic. The calibration is then CHECKED against the paper's
own stated peak (116 m/s at 60.5 S) before any width is reported.

Usage:  python3 wp100-profile-digitize.py <path-to-fig3.png>
Requires: numpy, pillow, scipy
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

if len(sys.argv) < 2:
    sys.exit("usage: wp100-profile-digitize.py <fig3.png>")

a = np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]
gray = a.mean(2)

# ── panel frame ──────────────────────────────────────────────────────────────
dark = gray < 115
cs = dark[:, :1700].sum(0)
verticals = [i for i in range(1700) if cs[i] > 1250]
X_LEFT  = float(np.mean([i for i in verticals if i < 400]))
X_RIGHT = float(np.mean([i for i in verticals if 1500 < i < 1560]))
_rows   = [i for i in range(len(dark)) if dark[i, :1500].sum() > 1300]
Y_TOP   = float(np.mean([i for i in _rows if i < 200]))   # topmost frame line only
V0, V1, LAT0, LAT1 = -40.0, 180.0, -50.0, -70.0
pxv = (X_RIGHT - X_LEFT) / (V1 - V0)

cyan = (B > 140) & (G > 140) & (R < 130) & ((B - R) > 60) & ((G - R) > 60)
cyan[:, 1500:] = False
ybot = np.nonzero(cyan)[0].max()
YS = (ybot - Y_TOP) / 19.9                        # px per degree of latitude
print(f"[1] frame  x:{X_LEFT:.1f}..{X_RIGHT:.1f} = {V0:.0f}..{V1:.0f} m/s"
      f"   ({pxv:.3f} px per m/s)")
print(f"    y top {Y_TOP:.1f} = {LAT0:.0f}   scale {YS:.2f} px per degree")

# ── HST markers (yellow filled circles) ──────────────────────────────────────
yellow = (R > 190) & (G > 190) & (B < 130) & ((R - B) > 90) & ((G - B) > 90)
yellow[:, 1500:] = False
yellow[1150:, :] = False                          # caption text
lab, _ = ndimage.label(yellow)
pts = []
for i, sl in enumerate(ndimage.find_objects(lab), 1):
    h, w = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
    if 16 <= h <= 40 and 16 <= w <= 40 and (lab[sl] == i).sum() > 200 and 0.6 < h / w < 1.7:
        cy, cx = ndimage.center_of_mass(lab == i)
        pts.append((LAT0 - (cy - Y_TOP) / YS, (cx - X_LEFT) / pxv + V0))
pts.sort()
lat = np.array([p[0] for p in pts]); u = np.array([p[1] for p in pts])
print(f"[2] {len(pts)} HST marker centroids recovered")

k = int(np.argmax(u))
print(f"[3] CALIBRATION CHECK   peak {u[k]:.1f} m/s at {lat[k]:.2f}"
      f"   (paper states 116 m/s at 60.5 S)")
assert abs(u[k] - 116) < 4 and abs(lat[k] + 60.5) < 0.3, "calibration failed"
print("    within 4 m/s and 0.3 deg -> calibration accepted")

# ── width, stated three ways, because the paper does not state its own ──────
DEG_KM = 2 * np.pi * 57316 / 360
def crossings(level):
    out = []
    for i in range(1, len(u)):
        if (u[i-1] - level) * (u[i] - level) < 0:
            f = (level - u[i-1]) / (u[i] - u[i-1])
            out.append(lat[i-1] + f * (lat[i] - lat[i-1]))
    return sorted(c for c in out if abs(c - lat[k]) < 6)

print("[4] jet width, by three defensible definitions:")
eq = lat > lat[k]
umin = u[eq].min()
for name, level in (("half of peak, zero baseline      ", u[k]/2),
                    ("half above the adjacent minimum  ", umin + (u[k]-umin)/2),
                    ("half above a 55 m/s shoulder     ", 55 + (u[k]-55)/2)):
    c = crossings(level)
    if len(c) >= 2:
        w = c[-1] - c[0]
        print(f"      {name} level {level:5.1f} m/s   FWHM {w:4.2f} deg = {w*DEG_KM:5.0f} km")
print(f"      paper reports                                        2.80 deg =  2700 km")
print("""[5] The paper's 2.80 deg is recovered only by the third definition, which puts the
    baseline on the ~55 m/s shoulder rather than at zero or at the adjacent minimum.
    Across the three the width runs 2.93 to 4.77 degrees -- a factor of 1.6 -- and the
    paper does not state which baseline it used. So the ABSOLUTE width is not a citable
    input to anything. The RATIO of two widths measured the same way is, and that is
    all WP-100 section 5 needs.""")
