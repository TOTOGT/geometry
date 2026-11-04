#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book24/interlude2-figs.py -- computes the data behind the two figures of interlude2-frank-merle-blow-up.html and writes
them as inline SVG into the page (between the markers FIGS-BEGIN and FIGS-END) and as interlude2-figs.json.

    python3 book24/interlude2-figs.py            # recompute; resumable: stops after about 140 s, run again until it says it wrote the figures
    python3 book24/interlude2-figs.py --from-json  # redraw from the stored JSON without recomputing

Floating-point numerics, not exact arithmetic. Needs numpy.

Figure 1. The virial identity y'' = 16 E for the critical 1D NLS  i u_t = -u_xx - |u|^4 u, with y = int x^2 |u|^2.
   Because E is conserved, y(t) is exactly the parabola y(0) + y'(0) t + 8 E t^2 for as long as the solution exists.
   Left: E > 0 (Gaussian, amplitude 0.5). Right: E < 0 (amplitude 2.5): the parabola reaches 0 at a finite time t*, the LATEST time the solution
   can exist (it may blow up earlier). The numerical points stop at 0.3 t*: past about 0.4 t* the solution has concentrated
   below one grid spacing and the run fails (energy not conserved), so nothing is claimed there. Strang split-step Fourier,
   with k_max^2 dt < pi for stability: left 1024 points on [-10, 10], dt = 1e-4; right 8192 points, dt = 1.5e-6.
Figure 2. The lattice (discrete NLS)  i u_n' = -J (u_{n+1} + u_{n-1} - 2 u_n) - lambda |u_n|^2 u_n  from one occupied site,
   J = 1, M = 1, lambda = Lambda J / M, N = 201 sites, RK4 with step 0.002 to t = 60. Plotted: the fraction of the mass on the
   initial site, averaged over t in [30, 60], against Lambda. Mass is conserved and |u_n|^2 <= M, so nothing blows up on
   a lattice; what changes with Lambda is whether the mass stays on the site (self-trapping) or spreads.
"""
import json, re, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
JS = HERE / "interlude2-figs.json"
PAGE = HERE / "interlude2-frank-merle-blow-up.html"

def fig1():
    def run_case(A, L, M, dt, T, nt):
        x = (np.arange(M) - M // 2) * (L / M); dx = L / M; k = 2 * np.pi * np.fft.fftfreq(M, d=dx)
        ph = np.exp(-1j * k ** 2 * dt / 2)
        def step(u):
            u = np.fft.ifft(ph * np.fft.fft(u)); u = u * np.exp(1j * np.abs(u) ** 4 * dt); return np.fft.ifft(ph * np.fft.fft(u))
        def E(u):
            ux = np.fft.ifft(1j * k * np.fft.fft(u)); return float(0.5 * np.sum(abs(ux) ** 2) * dx - np.sum(abs(u) ** 6) * dx / 6)
        def yy(u): return float(np.sum(x ** 2 * abs(u) ** 2) * dx)
        u = A * np.exp(-x ** 2 / 2) * np.exp(0.7j * x); e = E(u); y0 = yy(u)
        # y'(0) = 0: |u0|^2 is even, so the integral of x |u0|^2 vanishes (y' = 4 Im int x conj(u) u_x, and u_x = (-x + 0.7i) u here)
        steps_per = int(round(T / nt / dt)); ts = [0.0]; ys = [y0]; es = [e]; v = u.copy(); peak = float(np.max(abs(v)))
        for i in range(nt):
            for _ in range(steps_per): v = step(v)
            ts.append((i + 1) * steps_per * dt); ys.append(yy(v)); es.append(E(v)); peak = max(peak, float(np.max(abs(v))))
        par = [y0 + 8 * e * t * t for t in ts]
        return dict(A=A, E=e, y0=y0, mass=float(np.sum(abs(u) ** 2) * dx), T=ts[-1], t=ts, y=ys, parabola=par,
                    maxdev=float(max(abs(p - q) for p, q in zip(ys, par))), maxrel=float(max(abs(p - q) / q for p, q in zip(ys, par))),
                    Edrift=float(max(abs(q / e - 1) for q in es)), peak=peak, L=L, M=M, dt=dt, stab=float((np.pi / dx) ** 2 * dt))
    out = {}
    out["pos"] = run_case(0.5, 20.0, 1024, 1e-4, 1.0, 40); out["pos"]["tstar"] = None
    # E < 0: the parabola y(0) + 8 E t^2 reaches 0 at t*; the run covers 0 <= t <= 0.3 t* (beyond ~0.4 t* the solution has
    # concentrated below one grid spacing: the energy drifts and the run is not valid; not plotted)
    e_neg = None
    A = 2.5; xx = (np.arange(8192) - 4096) * (20.0 / 8192); kk = 2 * np.pi * np.fft.fftfreq(8192, d=20.0 / 8192)
    u0 = A * np.exp(-xx ** 2 / 2) * np.exp(0.7j * xx); ux = np.fft.ifft(1j * kk * np.fft.fft(u0))
    e_neg = float(0.5 * np.sum(abs(ux) ** 2) * (20.0 / 8192) - np.sum(abs(u0) ** 6) * (20.0 / 8192) / 6); y0n = float(np.sum(xx ** 2 * abs(u0) ** 2) * (20.0 / 8192))
    tstar = float(np.sqrt(y0n / (-8 * e_neg)))
    out["neg"] = run_case(2.5, 20.0, 8192, 1.5e-6, 0.3 * tstar, 24); out["neg"]["tstar"] = tstar
    for tag in ("pos", "neg"):
        d = out[tag]
        print(f"  figure 1 {tag}: A={d['A']} E={d['E']:+.4f} t*={d['tstar']} T={d['T']:.4f} max |y - parabola| = {d['maxdev']:.2e} (relative {d['maxrel']:.2e}); max |E/E0 - 1| = {d['Edrift']:.1e}; peak |u| = {d['peak']:.2f}; kmax^2 dt = {d['stab']:.2f} (< pi)")
    return out

def lattice_one(Lam):
    N = 201; Jc = 1.0; c = N // 2
    def rhs(u, lam): return -1j * (-Jc * (np.roll(u, 1) + np.roll(u, -1) - 2 * u) - lam * abs(u) ** 2 * u)
    def rk4(u, dt, lam):
        k1 = rhs(u, lam); k2 = rhs(u + dt / 2 * k1, lam); k3 = rhs(u + dt / 2 * k2, lam); k4 = rhs(u + dt * k3, lam)
        return u + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    lam = Lam * Jc; u = np.zeros(N, complex); u[c] = 1.0; acc = []
    for s in range(int(60 / 0.002)):
        u = rk4(u, 0.002, lam)
        if s * 0.002 >= 30 and s % 50 == 0: acc.append(abs(u[c]) ** 2)
    return float(np.mean(acc)), abs(float(np.sum(abs(u) ** 2)) - 1.0)

LAMBDAS = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 3.6, 3.7, 3.8, 3.9, 4, 4.5, 5, 6, 7, 8, 10, 12]

def compute(budget):
    """resumable: results are cached in interlude2-figs.cache.json; stops after `budget` seconds and returns None if unfinished"""
    import time
    t0 = time.time(); cp = HERE / "interlude2-figs.cache.json"
    cache = json.loads(cp.read_text(encoding="utf-8")) if cp.exists() else {}
    if "fig1" not in cache:
        cache["fig1"] = fig1(); cp.write_text(json.dumps(cache), encoding="utf-8")
    else: print("  figure 1: from cache")
    for Lam in LAMBDAS:
        key = f"L{Lam}"
        if key in cache: continue
        if time.time() - t0 > budget: break
        fr, dm = lattice_one(Lam); cache[key] = [fr, dm]; cp.write_text(json.dumps(cache), encoding="utf-8")
        print(f"  figure 2: Lambda={Lam:5.1f}  <|u_0|^2/M> = {fr:.3f}  (mass drift {dm:.1e})", flush=True)
    if not all(f"L{Lam}" in cache for Lam in LAMBDAS):
        print("  not finished: run the same command again to continue"); return None
    out = dict(cache["fig1"])
    out["lattice"] = dict(Lambda=LAMBDAS, fraction=[cache[f"L{L}"][0] for L in LAMBDAS], mass_drift_final=max(cache[f"L{L}"][1] for L in LAMBDAS), N=201, T=60.0, dt=0.002)
    print(f"  lattice: largest mass drift at t = 60 over all runs: {out['lattice']['mass_drift_final']:.1e}")
    return out

def svg_plot(panels, W, H, title_font=13):
    """panels: list of dict(x0,y0,w,h, xr,yr, xt,yt, xl,yl, series=[(xs,ys,kind,cssvar)], vlines=[(x,label)], note)"""
    s = [f'<svg viewBox="0 0 {W} {H}" role="img" style="width:100%;height:auto;max-width:{W}px;display:block;margin:.8rem auto" font-family="JetBrains Mono, monospace" font-size="11">']
    for p in panels:
        x0, y0, w, h = p["x0"], p["y0"], p["w"], p["h"]; (xa, xb), (ya, yb) = p["xr"], p["yr"]
        fx = lambda v: x0 + (v - xa) / (xb - xa) * w
        fy = lambda v: y0 + h - (v - ya) / (yb - ya) * h
        s.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="none" stroke="var(--rule)"/>')
        for tv in p["xt"]:
            s.append(f'<line x1="{fx(tv):.1f}" y1="{y0 + h}" x2="{fx(tv):.1f}" y2="{y0 + h + 4}" stroke="var(--dim)"/><text x="{fx(tv):.1f}" y="{y0 + h + 16}" text-anchor="middle" fill="var(--dim)">{tv:g}</text>')
        for tv in p["yt"]:
            s.append(f'<line x1="{x0 - 4}" y1="{fy(tv):.1f}" x2="{x0}" y2="{fy(tv):.1f}" stroke="var(--dim)"/><text x="{x0 - 7}" y="{fy(tv) + 4:.1f}" text-anchor="end" fill="var(--dim)">{tv:g}</text><line x1="{x0}" y1="{fy(tv):.1f}" x2="{x0 + w}" y2="{fy(tv):.1f}" stroke="var(--rule)" stroke-dasharray="2 4"/>')
        s.append(f'<text x="{x0 + w / 2}" y="{y0 + h + 34}" text-anchor="middle" fill="var(--ink)">{p["xl"]}</text>')
        s.append(f'<text x="{x0 + w / 2}" y="{y0 - 10}" text-anchor="middle" fill="var(--gold)" font-size="{title_font}">{p["title"]}</text>')
        s.append(f'<text transform="translate({x0 - 44},{y0 + h / 2}) rotate(-90)" text-anchor="middle" fill="var(--ink)">{p["yl"]}</text>')
        for (vx, lab) in p.get("vlines", []):
            s.append(f'<line x1="{fx(vx):.1f}" y1="{y0}" x2="{fx(vx):.1f}" y2="{y0 + h}" stroke="var(--dim)" stroke-dasharray="5 4"/><text x="{fx(vx) - 5:.1f}" y="{y0 + 14}" text-anchor="end" fill="var(--dim)">{lab}</text>')
        for (xs, ys, kind, col) in p["series"]:
            pts = " ".join(f"{fx(a):.1f},{fy(b):.1f}" for a, b in zip(xs, ys))
            if kind == "line": s.append(f'<polyline points="{pts}" fill="none" stroke="var({col})" stroke-width="2"/>')
            elif kind == "dots":
                for a, b in zip(xs, ys): s.append(f'<circle cx="{fx(a):.1f}" cy="{fy(b):.1f}" r="3.2" fill="var(--bg)" stroke="var({col})" stroke-width="1.6"/>')
            elif kind == "dotline":
                s.append(f'<polyline points="{pts}" fill="none" stroke="var({col})" stroke-width="1.4"/>')
                for a, b in zip(xs, ys): s.append(f'<circle cx="{fx(a):.1f}" cy="{fy(b):.1f}" r="3" fill="var({col})"/>')
        for (lx, ly, txt, col, anch) in p.get("labels", []):
            s.append(f'<text x="{lx}" y="{ly}" fill="var({col})" text-anchor="{anch}">{txt}</text>')
    s.append("</svg>")
    return "\n".join(s)

def build(d):
    pos, neg, lat = d["pos"], d["neg"], d["lattice"]
    f1 = svg_plot([
        dict(x0=62, y0=34, w=300, h=200, xr=(0, 1.0), yr=(0, 2.2), xt=[0, 0.25, 0.5, 0.75, 1.0], yt=[0, 0.5, 1.0, 1.5, 2.0], xl="t", yl="y(t) = &#8747; x&#178;|u|&#178;",
             title=f"E = {pos['E']:+.3f} &gt; 0 (mass {pos['mass']:.2f})", series=[(pos["t"], pos["parabola"], "line", "--gold"), (pos["t"], pos["y"], "dots", "--teal")],
             labels=[(70, 52, "line: y(0) + 8E t&#178;", "--gold", "start"), (70, 68, "circles: numerical", "--teal", "start")]),
        dict(x0=444, y0=34, w=300, h=200, xr=(0, 0.14), yr=(0, 6.0), xt=[0, 0.04, 0.08, 0.12], yt=[0, 2, 4, 6], xl="t", yl="y(t)",
             title=f"E = {neg['E']:+.1f} &lt; 0 (mass {neg['mass']:.1f})", series=[([i * 0.14 / 140 for i in range(141)], [max(0.0, neg['y0'] + 8 * neg['E'] * (i * 0.14 / 140) ** 2) for i in range(141)], "line", "--gold"), (neg["t"], neg["y"], "dots", "--teal")],
             vlines=[(neg["tstar"], f"t* = {neg['tstar']:.3f}")], labels=[(452, 52, "line: y(0) + 8E t&#178;", "--gold", "start"), (452, 68, "circles: computed, 0 to 0.3 t*", "--teal", "start")]),
    ], 780, 290)
    f2 = svg_plot([
        dict(x0=62, y0=34, w=660, h=210, xr=(0, 12.5), yr=(0, 1.05), xt=[0, 2, 4, 6, 8, 10, 12], yt=[0, 0.25, 0.5, 0.75, 1.0], xl="&#923; = &#955;M/J (nonlinearity against hopping)", yl="mass left on the first site",
             title="One occupied site, time average over t in [30, 60]", series=[(lat["Lambda"], lat["fraction"], "dotline", "--teal")], vlines=[(4.0, "&#923; = 4")],
             labels=[(716, 200, "N = 201, J = 1, M = 1, T = 60", "--dim", "end")]),
    ], 780, 300)
    return (f'<div class="figs"><figure>{f1}<figcaption><strong>Figure 1 (computed, floating point).</strong> The virial identity y&#8243; = 16E on the critical equation, checked on a grid. '
            f'Left, E = {pos["E"]:+.4f}: over 0 &le; t &le; 1 the largest gap between the computed y and the parabola y(0) + 8E t&#178; is {pos["maxdev"]:.1e} (relative {pos["maxrel"]:.1e}), and E drifts by at most {pos["Edrift"]:.0e}. '
            f'Right, E = {neg["E"]:+.2f}: over 0 &le; t &le; 0.3 t* = {neg["T"]:.4f} the gap is {neg["maxdev"]:.1e} (relative {neg["maxrel"]:.1e}), E drifts by at most {neg["Edrift"]:.0e}, and the peak amplitude only grows from 2.5 to {neg["peak"]:.1f}. '
            f'The line continues to its zero at t* = {neg["tstar"]:.4f}: that is the <em>latest</em> time the solution can exist, not a prediction of when it collapses, which may be earlier. '
            f'Past about 0.4 t* the same computation fails (the peak jumps to about 30 and the energy is no longer conserved), because the solution has concentrated below one grid spacing; that part is not plotted, '
            f'it is consistent with blow-up before t*, and it does not show it. Both runs keep k<sub>max</sub>&#178;&middot;dt below &pi; (here {pos["stab"]:.1f} and {neg["stab"]:.1f}), which the split-step method needs to stay stable. '
            f'This illustrates the identity; it is not a proof of it.</figcaption></figure>'
            f'<figure>{f2}<figcaption><strong>Figure 2 (computed, floating point).</strong> The lattice has no blow-up: mass is conserved (largest drift at t = 60 in the last run {lat["mass_drift_final"]:.0e}) and |u<sub>n</sub>|&#178; &le; M always. '
            f'What the nonlinearity changes is where the mass goes: for small &#923; it spreads along the lattice and the first site keeps almost none; for large &#923; it stays. '
            f'The values are at the points shown; the sharpness of the rise between &#923; = 3.5 and 4 is read from this one finite run (N = 201, T = 60) and is not a theorem. '
            f'Compare section 6: the radius a&radic;(J/&lambda;) of the CATGT paper and the threshold of the continuum equation have the same functional form, not a shared invariant.</figcaption></figure></div>')

def main():
    if "--from-json" in sys.argv: d = json.loads(JS.read_text(encoding="utf-8"))
    else:
        d = compute(budget=140)
        if d is None: return
        JS.write_text(json.dumps(d), encoding="utf-8"); print("  wrote", JS.name)
    blk = "<!--FIGS-BEGIN-->" + build(d) + "<!--FIGS-END-->"
    txt = PAGE.read_text(encoding="utf-8")
    if "<!--FIGS-BEGIN-->" in txt: txt = re.sub(r"<!--FIGS-BEGIN-->.*?<!--FIGS-END-->", lambda m: blk, txt, flags=re.S)
    else: print("  the page has no FIGS-BEGIN marker; nothing written to it"); return
    PAGE.write_text(txt, encoding="utf-8"); print("  figures written into", PAGE.name)

if __name__ == "__main__": main()
