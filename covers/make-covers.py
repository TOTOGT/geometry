#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""covers/make-covers.py -- draws one series cover system for the G6 LLC catalogue. Each cover is an SVG, 400 x 600:
a series band, one mathematical figure COMPUTED from the book's subject, the title block, the author and the imprint.
The design is original; it follows the general convention of academic series covers and uses no publisher's marks.
    python3 make-covers.py [outdir]      writes cover-<id>.svg and covers.json (id, title, svg) """
import math, json, sys
from pathlib import Path
import numpy as np
W, H = 400, 600
INK = "#f3ead6"

def f(x): return f"{x:.1f}"
def poly(pts, close=False, **kw):
    d = "M" + " L".join(f"{f(x)},{f(y)}" for x, y in pts) + ("Z" if close else "")
    a = " ".join(f'{k.replace("_","-")}="{v}"' for k, v in kw.items())
    return f'<path d="{d}" {a}/>'
def fit(pts, box):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys); bx0, by0, bx1, by1 = box
    s = min((bx1 - bx0) / (x1 - x0 or 1), (by1 - by0) / (y1 - y0 or 1))
    ox = bx0 + ((bx1 - bx0) - s * (x1 - x0)) / 2; oy = by0 + ((by1 - by0) - s * (y1 - y0)) / 2
    return lambda p: (ox + s * (p[0] - x0), oy + s * (p[1] - y0)), s
BOX = (60, 112, 340, 372)

# ---------- figures (each returns svg fragments in the box BOX) ----------
def fig_contact():            # contact planes of alpha = dz - y dx at points (x, y, 0): span of (1,0,y) and (0,1,0)
    out = []; P = lambda x, y, z: (x + 0.5*y, -z*1.0 - 1.15*y)
    cells = []
    for gy in np.linspace(-2, 2, 5):
        for gx in np.linspace(-2.4, 2.4, 5):
            s_ = 0.34
            c = [(-s_, -s_), (s_, -s_), (s_, s_), (-s_, s_)]
            pts3 = [(gx + a_, gy + b_ * 0.55, a_ * gy) for a_, b_ in c]
            cells.append((gy, [P(*q) for q in pts3]))
    allp = [p for _, c in cells for p in c]; tr, _ = fit(allp, BOX)
    for gy, c in sorted(cells, key=lambda t: -t[0]):
        out.append(poly([tr(p) for p in c], close=True, fill=INK, fill_opacity=.18, stroke=INK, stroke_width=1.3))
    return out
def fig_jet():                # curve with its tangent lines (the 1-jet)
    xs = np.linspace(0, 2*math.pi, 200); fy = lambda x: math.sin(x) + 0.35*math.sin(2*x)
    dfy = lambda x: math.cos(x) + 0.7*math.cos(2*x)
    curve = [(x, -fy(x)) for x in xs]; tr, s = fit(curve + [(0, -1.6), (2*math.pi, 1.6)], BOX); out = []
    for x in np.linspace(0.2, 2*math.pi - 0.2, 11):
        h = 0.42; a = (x - h, -(fy(x) - h*dfy(x))); b = (x + h, -(fy(x) + h*dfy(x)))
        out.append(poly([tr(a), tr(b)], stroke=INK, stroke_width=1.3, stroke_opacity=.8, fill="none"))
        px, py = tr((x, -fy(x))); out.append(f'<circle cx="{f(px)}" cy="{f(py)}" r="2.6" fill="{INK}"/>')
    out.append(poly([tr(p) for p in curve], stroke=INK, stroke_width=2.4, fill="none"))
    return out
def fig_fold():               # four rooms, one normal form: x' = mu + x^2, equilibria x = +-sqrt(-mu), in a 2x2 grid
    out = []; cell = 120; gap = 20; x0, y0 = 60, 118
    for i in range(4):
        cx = x0 + (i % 2) * (cell + gap); cy = y0 + (i // 2) * (cell + gap)
        out.append(f'<rect x="{cx}" y="{cy}" width="{cell}" height="{cell}" fill="none" stroke="{INK}" stroke-opacity=".5"/>')
        mus = np.linspace(-1, 0, 60); top = [(cx + 14 + (m + 1) * (cell - 28), cy + cell/2 - math.sqrt(-m) * (cell/2 - 16)) for m in mus]
        bot = [(px, 2*(cy + cell/2) - py) for px, py in top]
        out.append(poly(top, stroke=INK, stroke_width=2.2, fill="none")); out.append(poly(bot, stroke=INK, stroke_width=2.2, stroke_dasharray="4 3", fill="none"))
        out.append(f'<circle cx="{f(top[-1][0])}" cy="{f(top[-1][1])}" r="3.4" fill="{INK}"/>')
    return out
def fig_koch():               # Koch snowflake, iteration 4 (boundary dimension log 4 / log 3 = 1.2619; no number is printed on the cover)
    def step(pts):
        res = []
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            dx, dy = (x2 - x1)/3, (y2 - y1)/3; a_ = (x1 + dx, y1 + dy); b_ = (x1 + 2*dx, y1 + 2*dy)
            c_ = (a_[0] + (dx*math.cos(-math.pi/3) - dy*math.sin(-math.pi/3)), a_[1] + (dx*math.sin(-math.pi/3) + dy*math.cos(-math.pi/3)))
            res += [(x1, y1), a_, c_, b_]
        res.append(pts[-1]); return res
    tri = [(0, 0), (1, 0), (0.5, -math.sqrt(3)/2), (0, 0)]
    p = tri
    for _ in range(4): p = step(p)
    tr, _ = fit(p, BOX); pp = [tr(q) for q in p]
    return [poly(pp, close=True, stroke=INK, stroke_width=1.5, fill=INK, fill_opacity=.14, stroke_linejoin="round")]
def fig_cobweb():             # fixed point of g(x) = cos x
    g = math.cos; xs = np.linspace(0, 1.2, 100); curve = [(x, g(x)) for x in xs]
    tr, _ = fit(curve + [(0, 0), (1.2, 1.2)], (70, 118, 330, 370)); out = []
    out.append(poly([tr((0, 0)), tr((1.2, 1.2))], stroke=INK, stroke_width=1.4, stroke_opacity=.7, fill="none"))
    out.append(poly([tr(p) for p in curve], stroke=INK, stroke_width=2.4, fill="none"))
    x = 0.12; pts = [tr((x, 0))]
    for _ in range(14):
        y = g(x); pts += [tr((x, y)), tr((y, y))]; x = y
    out.append(poly(pts, stroke=INK, stroke_width=1.1, stroke_opacity=.85, fill="none"))
    fx, fy = tr((0.7390851332, 0.7390851332)); out.append(f'<circle cx="{f(fx)}" cy="{f(fy)}" r="4.4" fill="{INK}"/>'); return out
def fig_hex():                # honeycomb
    out = []; r = 26; dx = r * math.sqrt(3); cx0, cy0 = 200, 242
    for row in range(-3, 4):
        for col in range(-3, 4):
            cx = cx0 + col * dx + (row % 2) * dx / 2; cy = cy0 + row * r * 1.5
            if (cx - cx0)**2 + (cy - cy0)**2 > 125**2: continue
            pts = [(cx + r*math.cos(math.pi/6 + k*math.pi/3), cy + r*math.sin(math.pi/6 + k*math.pi/3)) for k in range(6)]
            out.append(poly(pts, close=True, fill=INK, fill_opacity=.1, stroke=INK, stroke_width=1.3))
    pts = [(cx0 + r*math.cos(math.pi/6 + k*math.pi/3), cy0 + r*math.sin(math.pi/6 + k*math.pi/3)) for k in range(6)]
    out.append(poly(pts, close=True, fill=INK, fill_opacity=.5, stroke=INK, stroke_width=2)); return out
def fig_svd():                # unit circle and its image under A, with the singular directions
    A = np.array([[2.0, 1.2], [0.3, 0.9]]); U, S, Vt = np.linalg.svd(A)
    t = np.linspace(0, 2*math.pi, 200); circ = np.array([np.cos(t), np.sin(t)]); img = A @ circ
    pts = [tuple(p) for p in circ.T] + [tuple(p) for p in img.T]; tr, s = fit([(x, -y) for x, y in pts], BOX); out = []
    cc = [tr((x, -y)) for x, y in circ.T]; ee = [tr((x, -y)) for x, y in img.T]
    out.append(poly(cc, close=True, stroke=INK, stroke_width=1.6, stroke_opacity=.6, fill="none"))
    out.append(poly(ee, close=True, stroke=INK, stroke_width=2.6, fill=INK, fill_opacity=.12))
    for k in range(2):
        v = Vt[k]; u = U[:, k] * S[k]
        out.append(poly([tr((0, 0)), tr((v[0], -v[1]))], stroke=INK, stroke_width=1.4, stroke_opacity=.7, stroke_dasharray="3 3", fill="none"))
        out.append(poly([tr((0, 0)), tr((u[0], -u[1]))], stroke=INK, stroke_width=2.6, fill="none"))
    ox, oy = tr((0, 0)); out.append(f'<circle cx="{f(ox)}" cy="{f(oy)}" r="3.4" fill="{INK}"/>'); return out
def fig_bridge():             # cable (catenary) between two towers, with hangers and a deck, plus its reflection in water
    a = 1.0; xs = np.linspace(-1.5, 1.5, 120); cat = [(x, a*math.cosh(x/a)) for x in xs]
    tr, _ = fit([(x, -y) for x, y in cat] + [(-1.5, -3.2), (1.5, 1.0)], (62, 130, 338, 360)); out = []
    deck = tr((-1.5, 0.2))[1] + 120*0 ; ytop = tr((0, -a*math.cosh(0)))[1]
    ydeck = tr((0, -3.2*0 + 0))[1]
    ycat = [tr((x, -y)) for x, y in cat]; basey = max(p[1] for p in ycat) + 62
    out.append(poly([(62, basey), (338, basey)], stroke=INK, stroke_width=3, fill="none"))
    for x in np.linspace(-1.3, 1.3, 14):
        px, py = tr((x, -a*math.cosh(x/a))); out.append(poly([(px, py), (px, basey)], stroke=INK, stroke_width=1.1, stroke_opacity=.7, fill="none"))
    out.append(poly(ycat, stroke=INK, stroke_width=2.6, fill="none"))
    for sx in (-1.5, 1.5):
        px, py = tr((sx, -a*math.cosh(sx/a))); out.append(poly([(px, py - 14), (px, basey + 36)], stroke=INK, stroke_width=5, fill="none"))
    for k in range(5):
        y = basey + 18 + k*9; out.append(poly([(70 + k*6, y), (330 - k*6, y)], stroke=INK, stroke_width=1, stroke_opacity=.4 - k*.06, fill="none"))
    return out
def fig_attn():               # 8x8 attention weights: softmax(Q K^T / sqrt(d)) with fixed pseudo-random Q, K
    rng = np.random.default_rng(16); n, d = 8, 4; Q = rng.normal(size=(n, d)); K = rng.normal(size=(n, d))
    Z = Q @ K.T / math.sqrt(d); Z = np.where(np.tril(np.ones((n, n))) > 0, Z, -1e9); E = np.exp(Z - Z.max(1, keepdims=True)); Wt = E / E.sum(1, keepdims=True)
    out = []; cell = 33; x0, y0 = 68, 118
    for i in range(n):
        for j in range(n):
            if j <= i: out.append(f'<rect x="{x0 + j*cell}" y="{y0 + i*cell}" width="{cell - 2}" height="{cell - 2}" fill="{INK}" fill-opacity="{Wt[i, j]*.95 + .04:.3f}"/>')
            else: out.append(f'<rect x="{x0 + j*cell}" y="{y0 + i*cell}" width="{cell - 2}" height="{cell - 2}" fill="none" stroke="{INK}" stroke-opacity=".18"/>')
    return out


def piece(kind, x, y, h, fill):
    """King or queen, an original silhouette in a 20 x 40 box with its base on the bottom edge; (x, y) = top-left, h = height."""
    k = h / 40.0
    g = [f'<g transform="translate({f(x)},{f(y)}) scale({k:.4f})" fill="{fill}">']
    g.append('<path d="M2,40 L18,40 L17,36 L3,36 Z"/><path d="M5,36 L7,16 L13,16 L15,36 Z"/><rect x="5" y="13" width="10" height="3"/>')
    if kind == "king":
        g.append('<circle cx="10" cy="10.2" r="3.6"/><rect x="9.2" y="0" width="1.6" height="6.6"/><rect x="7.4" y="1.5" width="5.2" height="1.6"/>')
    else:
        g.append('<path d="M4.5,13 L2.6,3.6 L7,8.4 L10,2 L13,8.4 L17.4,3.6 L15.5,13 Z"/><circle cx="2.6" cy="2.6" r="1.4"/><circle cx="10" cy="1.2" r="1.4"/><circle cx="17.4" cy="2.6" r="1.4"/>')
    g.append('</g>'); return "".join(g)
def emblem(xr, y, h, fill):
    w = 20 * h / 40.0; gap = 6
    return piece("king", xr - 2*w - gap, y, h, fill) + piece("queen", xr - w, y, h, fill)

# ---------- covers ----------
COVERS = [
 dict(id="vol1", mark="VOLUME I", color="#1f3b63", fig=fig_contact, lines=["GOMC", "Science"], sub=["Contact geometry: the operator", "algebra and the fixed-point claim"]),
 dict(id="vol2", mark="VOLUME II", color="#2c5b4a", fig=fig_jet, lines=["TOGT"], sub=["Jet spaces and the structural levels"]),
 dict(id="vol3", mark="VOLUME III · BOOK 3", color="#8a3d2b", fig=fig_fold, lines=["The", "Mini-Beast"], sub=["Four rooms, one normal form"]),
 dict(id="vol4", mark="VOLUME IV", color="#4b3a6e", fig=fig_koch, lines=["GTCT", "Dimensional Theory"], sub=["The Γ attractor"]),
 dict(id="vol5", mark="VOLUME V", color="#8a6a1e", fig=fig_cobweb, lines=["Complete", "Completeness"], sub=["The Seed · G(S) = S"]),
 dict(id="vol6", mark="VOLUME VI", color="#33414f", fig=fig_hex, lines=["G6 Crystal", "Roots"], sub=["An open conjecture, stated as one"]),
 dict(id="book24", mark="BOOK XXIV", color="#1d5c63", fig=fig_svd, lines=["Linear Algebra", "for Graduate Study"], sub=["With the nonlinear half beside it"]),
 dict(id="book25", mark="BOOK XXV", color="#7b2236", fig=fig_bridge, lines=["Ponte", "Bridge"], sub=["Study and settling in Brazil"]),
 dict(id="book16", mark="BOOK XVI", color="#2b2b33", fig=fig_attn, lines=["LLMs Explained"], sub=["Tokens, embeddings, transformers", "and more"]),
]
def cover_svg(c, standalone=True):
    col = c["color"]; o = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Cover: {" ".join(c["lines"])}" font-family="Georgia, \'Iowan Old Style\', \'Palatino Linotype\', serif">')
    o.append(f'<rect width="{W}" height="{H}" fill="{col}"/>')
    o.append(f'<rect x="0" y="0" width="{W}" height="64" fill="#000" fill-opacity=".28"/>')
    o.append(f'<text x="28" y="30" fill="{INK}" font-size="13" letter-spacing="3.2">PRINCIPIA ORTHOGONA</text>')
    o.append(f'<text x="28" y="50" fill="{INK}" fill-opacity=".75" font-size="10.5" letter-spacing="2.4" font-family="ui-monospace, Menlo, Consolas, monospace">{c["mark"]}</text>')
    o.append(f'<rect x="28" y="92" width="{W-56}" height="1.2" fill="{INK}" fill-opacity=".5"/>')
    o += c["fig"]()
    y = 414; size = 34 if max(len(l) for l in c["lines"]) <= 15 else 30
    for l in c["lines"]:
        o.append(f'<text x="28" y="{y}" fill="{INK}" font-size="{size}" font-weight="400" letter-spacing="-.3">{l}</text>'); y += size + 6
    y += 4
    for l in c["sub"]:
        o.append(f'<text x="28" y="{y}" fill="{INK}" fill-opacity=".82" font-size="15" font-style="italic">{l}</text>'); y += 21
    o.append(f'<rect x="28" y="542" width="{W-56}" height="1.2" fill="{INK}" fill-opacity=".5"/>')
    o.append(f'<text x="28" y="566" fill="{INK}" font-size="14" letter-spacing=".6">Pablo Nogueira Grossi</text>')
    o.append(f'<text x="28" y="585" fill="{INK}" fill-opacity=".8" font-size="10.5" letter-spacing="2.4" font-family="ui-monospace, Menlo, Consolas, monospace">G6 LLC</text>')
    o.append(emblem(W - 28, 551, 38, INK))
    o.append('</svg>'); return "".join(o)

if __name__ == "__main__":
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "."); out.mkdir(parents=True, exist_ok=True)
    meta = []
    for c in COVERS:
        s = cover_svg(c); (out / f"cover-{c['id']}.svg").write_text(s, encoding="utf-8"); meta.append(dict(id=c["id"], mark=c["mark"], title=" ".join(c["lines"]), svg=s))
    (out / "covers.json").write_text(json.dumps(meta), encoding="utf-8"); print("wrote", len(meta), "covers to", out)
