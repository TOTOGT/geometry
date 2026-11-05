#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book26/ch14-verify.py -- book26/ch14-options-from-first-principles.html (Template B): Black-Scholes price, Greeks,
implied volatility on SYNTHETIC inputs, for a Quantitative Trader (Index Volatility) application.
  [1] structure   [2] option figures recomputed and found on the page   [3] parity, finite differences, BS equation
  [4] implied-vol round trip, three-strike parabola, parity flag   [5] SOURCE: lists which held files exist; SKIP for the rest
  [6] controls (each check run on a wrong input must fail)   [7] honesty statements on the page
Standard library only.
"""
import html as _h, os, re, sys
from math import erf, exp, log, pi, sqrt
from pathlib import Path
HERE = Path(__file__).resolve().parent
PAGE = HERE / "ch14-options-from-first-principles.html"
FAIL, SKIP = [], []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def skip(label, why): print(f"SKIP {label}  -- {why}"); SKIP.append(label)
raw = PAGE.read_text(encoding="utf-8")
txt = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", raw, flags=re.S)
txt = re.sub(r"\s+", " ", _h.unescape(re.sub(r"<[^>]+>", " ", txt)))

N = lambda x: 0.5 * (1 + erf(x / sqrt(2)))
n = lambda x: exp(-x * x / 2) / sqrt(2 * pi)
def d12(S, K, T, r, q, s):
    d1 = (log(S / K) + (r - q + s * s / 2) * T) / (s * sqrt(T)); return d1, d1 - s * sqrt(T)
def bs(S, K, T, r, q, s, cp):
    d1, d2 = d12(S, K, T, r, q, s)
    if cp == "c": return S * exp(-q * T) * N(d1) - K * exp(-r * T) * N(d2)
    return K * exp(-r * T) * N(-d2) - S * exp(-q * T) * N(-d1)
def greeks(S, K, T, r, q, s, cp):
    d1, d2 = d12(S, K, T, r, q, s)
    delta = exp(-q * T) * (N(d1) if cp == "c" else N(d1) - 1)
    gamma = exp(-q * T) * n(d1) / (S * s * sqrt(T)); vega = S * exp(-q * T) * n(d1) * sqrt(T)
    th = -S * exp(-q * T) * n(d1) * s / (2 * sqrt(T))
    th += (-r * K * exp(-r * T) * N(d2) + q * S * exp(-q * T) * N(d1)) if cp == "c" else (r * K * exp(-r * T) * N(-d2) - q * S * exp(-q * T) * N(-d1))
    return delta, gamma, vega, th
def implied(price, S, K, T, r, q, cp):
    lo, hi = 1e-6, 5.0
    for _ in range(200):
        m = (lo + hi) / 2
        if bs(S, K, T, r, q, m, cp) > price: hi = m
        else: lo = m
    return (lo + hi) / 2
S, K, T, r, q, s = 100.0, 100.0, 0.25, 0.04, 0.0, 0.20
C, P = bs(S, K, T, r, q, s, "c"), bs(S, K, T, r, q, s, "p")
dc, gc, vc, tc = greeks(S, K, T, r, q, s, "c"); dp = greeks(S, K, T, r, q, s, "p")[0]

print("[1] structure")
order = ["posting", "problems", "analysis", "recommendations", "actions", "followthrough", "limits", "updates", "checked", "sources"]
pos = [raw.find(f'id="{i}"') for i in order]
check("sections present and in order", all(p > 0 for p in pos) and pos == sorted(pos))
check("Template B hero and nav", 'class="hero"' in raw and 'class="pillars"' in raw)
check("no network, storage or form code", not re.search(r"<form|fetch\(|XMLHttpRequest|localStorage|sessionStorage|WebSocket", raw))
for lab in ["Questions raised", "Analysis", "Recommendations", "Actions", "Follow-through"]:
    check(f"label '{lab}'", lab in txt)

print("[2] option figures")
for name, val, fmt in [("call", C, "{:.4f}"), ("put", P, "{:.4f}"), ("call delta", dc, "{:.4f}"), ("put delta", dp, "{:.4f}"),
                       ("gamma", gc, "{:.5f}"), ("vega", vc, "{:.3f}"), ("vega per point", vc / 100, "{:.4f}"),
                       ("theta/yr", tc, "{:.4f}"), ("theta/day", tc / 365, "{:.5f}")]:
    shown = fmt.format(abs(val) if "theta" in name or name == "put delta" else val)
    check(f"{name} = {shown} on page", shown in txt, f"{val:.6f}")

print("[3] parity, finite differences, Black-Scholes equation")
par = C - P; rhs = S - K * exp(-r * T)
check("put-call parity", abs(par - rhs) < 1e-12 and f"{par:.4f}" in txt, f"{par:.6f} vs {rhs:.6f}")
h = 1e-3
fd_d = (bs(S + h, K, T, r, q, s, "c") - bs(S - h, K, T, r, q, s, "c")) / (2 * h)
fd_g = (bs(S + h, K, T, r, q, s, "c") - 2 * C + bs(S - h, K, T, r, q, s, "c")) / h ** 2
fd_v = (bs(S, K, T, r, q, s + h, "c") - bs(S, K, T, r, q, s - h, "c")) / (2 * h)
check("finite-difference delta", abs(fd_d - dc) < 1e-6 and f"{fd_d:.5f}" in txt, f"{fd_d:.6f}")
check("finite-difference gamma", abs(fd_g - gc) < 1e-5 and f"{fd_g:.5f}" in txt, f"{fd_g:.6f}")
check("finite-difference vega", abs(fd_v - vc) < 1e-4 and f"{fd_v:.3f}" in txt, f"{fd_v:.4f}")
res = tc + 0.5 * s * s * S * S * gc + r * S * dc - r * C
check("Black-Scholes equation residual below 1e-12", abs(res) < 1e-12, f"{res:.2e}")

print("[4] implied volatility, surface, parity flag")
iv_c, iv_p = implied(C, S, K, T, r, q, "c"), implied(P, S, K, T, r, q, "p")
check("implied vol from call and put is 0.2000", abs(iv_c - s) < 1e-10 and abs(iv_p - s) < 1e-10 and "0.2000" in txt)
xs = [log(k / S) for k in (90, 100, 110)]; ys = [0.24, 0.20, 0.18]
def lagrange(x):
    t = 0.0
    for i in range(3):
        li = 1.0
        for j in range(3):
            if j != i: li *= (x - xs[j]) / (xs[i] - xs[j])
        t += ys[i] * li
    return t
v95, v105 = lagrange(log(95 / S)), lagrange(log(105 / S))
check("parabola passes through its three points", all(abs(lagrange(x) - y) < 1e-12 for x, y in zip(xs, ys)))
check("21.71% at 95 and 18.78% at 105 on page", f"{v95*100:.2f}%" in txt and f"{v105*100:.2f}%" in txt, f"{v95:.5f}, {v105:.5f}")
check("page says the fit is exact by construction", "exact by construction" in txt)
gap = 3.60 - P
check("put quoted 3.60 sits 0.1098 above parity", f"{gap:.4f}" in txt and "0.1098" in txt, f"{gap:.5f}")

print("[5] SOURCE")
for label, rel in [("Bronze/Silver certificates folder", Path.home() / "Desktop/AXLE/NetworkGamesJOMO"),
                   ("posting excerpts", Path.home() / "Desktop/grants/walleye")]:
    if rel.exists():
        names = sorted(p.name for p in rel.iterdir())
        print(f"INFO {label}: {len(names)} files at {rel}")
        gold = [x for x in names if "gold" in x.lower()]
        if label.startswith("Bronze"):
            print("INFO Gold certificate file(s) found: " + (", ".join(gold) if gold else "none"))
    else:
        skip(label, f"{rel} not found here")
skip("posting paraphrase, paper statements", "from the author's files and earlier review; not machine-checkable")

print("[6] controls")
check("control: wrong volatility changes the price", abs(bs(S, K, T, r, q, 0.25, "c") - C) > 0.1)
check("control: wrong rate breaks parity against the page value", abs((C - P) - (S - K * exp(-0.05 * T))) > 1e-4)
check("control: a too-large bump spoils the finite difference", abs((bs(S + 5, K, T, r, q, s, "c") - bs(S - 5, K, T, r, q, s, "c")) / 10 - dc) > 1e-4)
check("control: wrong theta fails the equation", abs((tc + 1.0) + 0.5 * s * s * S * S * gc + r * S * dc - r * C) > 0.5)
check("control: wrong price gives a different implied vol", abs(implied(C + 0.1, S, K, T, r, q, "c") - s) > 1e-3)
check("control: 4.4853 is not the call price on the page", "4.4853" not in txt)

print("[7] honesty and wording")
check("says it is an exercise, not trading experience", "not trading experience" in txt and "has not worked on a trading desk" in txt)
check("says every quote is invented", "Every quote below is invented" in txt and "none is a market price" in txt)
check("says the certificates are for reaching a level, not winning", "reaching a level, not winning a contest" in txt)
check("says nothing was tested on market data", "has not yet been tested on market data" in txt and "not an edge" in txt)
check("gender-neutral: no he/his/him/she/her", not re.search(r"\\b(he|his|him|himself|she|her|hers)\\b", txt, re.I))
check("states Bronze, Silver and Gold as levels reached, three certificates", "three certificates" in txt and "Bronze, Silver and Gold" in txt)
check("no claim that a level is a job, a payment or a placement", not re.search(r"consultant (status|role|position)|paid consultant|hired", txt, re.I))

print(f"\n{'ALL PASS' if not FAIL else 'FAILURES: ' + str(len(FAIL))}  ({len(SKIP)} SKIP)")
sys.exit(1 if FAIL else 0)
