#!/usr/bin/env python3
"""
wp100-figure-measure.py — Principia Orthogona, Vol VI, WP-100

Measures the decagon's latitude directly from Figure 1 of Sanchez-Lavega et al.,
Science Advances 12, eaee4251 (2026), which is CC BY. Nothing here reads the
paper's text; the figure alone is the input.

  1. locate the red dashed circle  -> 80 S by the figure caption
  2. locate the cyan dashed circles -> 70 S and 50 S
  3. show the polar projection is linear in colatitude, and get px/degree
  4. sample brightness on circles of constant latitude and find the radius at
     which the 10-fold Fourier component is largest

Usage:  python3 wp100-figure-measure.py <path-to-fig1.png>
Requires: numpy, pillow
"""
import sys
import numpy as np
from PIL import Image

if len(sys.argv) < 2:
    sys.exit("usage: wp100-figure-measure.py <fig1.png>")

a = np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float)
R, G, B = a[..., 0], a[..., 1], a[..., 2]
gray = a.mean(2)
colored = (np.abs(R-G) > 25) | (np.abs(G-B) > 25) | (np.abs(R-B) > 25)
cyan = (B > 150) & (G > 150) & (R < 120) & ((B-R) > 80)
red  = (R > 150) & (G < 110) & (B < 110) & ((R-G) > 70)
H, W = gray.shape

def fit_circle(x, y):
    A = np.c_[2*x, 2*y, np.ones(len(x))]
    c, *_ = np.linalg.lstsq(A, x**2 + y**2, rcond=None)
    return c[0], c[1], np.sqrt(c[2] + c[0]**2 + c[1]**2)

# top-right panel of Fig. 1 (F763M, 29 Aug 2025)
y0, y1 = int(0.18*H), int(0.50*H)
m = red.copy(); m[:y0] = False; m[y1:] = False
ys, xs = np.nonzero(m)
cx, cy, r80 = fit_circle(xs.astype(float), ys.astype(float))
print(f"[1] red dashed circle  centre=({cx:.1f},{cy:.1f})  r={r80:.1f} px   = 80 S per caption")

mc = cyan.copy(); mc[:y0] = False; mc[y1:] = False
cys, cxs = np.nonzero(mc)
rad = np.hypot(cxs-cx, cys-cy)
hist, edges = np.histogram(rad, bins=140)
peaks = [0.5*(edges[i]+edges[i+1]) for i in range(1, len(hist)-1)
         if hist[i] > 300 and hist[i] >= hist[i-1] and hist[i] >= hist[i+1]]
print(f"[2] cyan dashed circles at radii {[round(p,1) for p in peaks]} px")

print("[3] linear-in-colatitude test:")
scale = r80 / 10.0
for lat, meas in [(80.0, r80)] + list(zip([70.0, 50.0], sorted(peaks))):
    co = 90 - lat
    print(f"      {lat:4.0f} S  colat {co:4.0f}   {meas:7.1f} px   {meas/co:7.3f} px/deg"
          f"   residual vs 80S scale: {100*(meas/co-scale)/scale:+5.2f} %")
print(f"      adopted scale {scale:.3f} px per degree of colatitude")

print("[4] 10-fold Fourier amplitude versus latitude:")
th = np.linspace(0, 2*np.pi, 1440, endpoint=False)
def comp(colat, m_):
    r = colat*scale
    xi = np.clip((cx+r*np.cos(th)).astype(int), 0, W-1)
    yi = np.clip((cy+r*np.sin(th)).astype(int), 0, H-1)
    v = gray[yi, xi].copy(); bad = colored[yi, xi]
    good = ~bad
    if good.sum() < 0.6*len(v): return 0.0, 0.0
    idx = np.arange(len(v))
    v = np.interp(idx, idx[good], v[good]) - np.interp(idx, idx[good], v[good]).mean()
    F = np.fft.rfft(v)/len(v)*2
    return abs(F[m_]), v.std()

best = (0.0, None)
for colat in np.arange(15.0, 40.0, 0.25):          # 75 S .. 50 S, away from the mask
    a10, rms = comp(colat, 10)
    if rms > 15:  continue                          # skip mask edges and bright rims
    a6, _ = comp(colat, 6); a5, _ = comp(colat, 5)
    if a10 > best[0] and a10 > 2.5*max(a6, a5):
        best = (a10, colat)
lat_meas = 90 - best[1]
print(f"      peak 10-fold amplitude {best[0]:.2f} at colatitude {best[1]:.2f}")
print(f"      => decagon latitude measured from the figure: {lat_meas:.2f} S")
print(f"      paper states 63.0 +/- 0.4 S            difference: {lat_meas-63.0:+.2f} deg")
