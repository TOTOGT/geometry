#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""book24/interlude2-reye.py -- draws r_eye(3,l) (limiting blow-up speed, Merle-Raphael-Rodnianski-Szeftel, arXiv:1912.11009,
eq. (1.4)) into interlude2-frank-merle-blow-up.html between REYE-BEGIN and REYE-END. Formulas only; no PDE is solved.
    r_eye(d,l) = (d+l)/(l+sqrt d)           for l < d
               = 1 + (d-1)/(1+sqrt l)^2     for l > d          (l = 2/(gamma-1))"""
import math, re
from pathlib import Path
PAGE = Path(__file__).resolve().parent / "interlude2-frank-merle-blow-up.html"

def r_eye(d, l):
    if l < d: return (d + l) / (l + math.sqrt(d))
    return 1 + (d - 1) / (1 + math.sqrt(l)) ** 2

def svg():
    W, H, L, R, T, B = 780, 330, 60, 20, 20, 50
    lmax, ymin, ymax = 12.0, 0.9, 1.8
    X = lambda l: L + (W - L - R) * l / lmax
    Y = lambda y: T + (H - T - B) * (ymax - y) / (ymax - ymin)
    s = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="r_eye(3,l) against l" style="width:100%;height:auto;max-width:780px;display:block;margin:.8rem auto" font-family="JetBrains Mono, monospace" font-size="11">']
    s.append(f'<rect x="{L}" y="{T}" width="{W-L-R}" height="{H-T-B}" fill="none" stroke="currentColor" stroke-opacity=".4"/>')
    for l in range(0, 13, 2):
        s.append(f'<line x1="{X(l):.1f}" y1="{H-B}" x2="{X(l):.1f}" y2="{H-B+5}" stroke="currentColor"/><text x="{X(l):.1f}" y="{H-B+18}" text-anchor="middle" fill="currentColor">{l}</text>')
    for y in (1.0, 1.2, 1.4, 1.6, 1.8):
        s.append(f'<line x1="{L-5}" y1="{Y(y):.1f}" x2="{L}" y2="{Y(y):.1f}" stroke="currentColor"/><text x="{L-8}" y="{Y(y)+4:.1f}" text-anchor="end" fill="currentColor">{y:.1f}</text>')
    for lo, hi in ((0.02, 2.999), (3.001, 12.0)):
        n = 200; pts = []
        for i in range(n + 1):
            l = lo + (hi - lo) * i / n; pts.append(f'{X(l):.1f},{Y(r_eye(3, l)):.1f}')
        s.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#c0392b" stroke-width="2"/>')
    x3, y3 = X(3), Y(3 - math.sqrt(3))
    s.append(f'<line x1="{x3:.1f}" y1="{T}" x2="{x3:.1f}" y2="{H-B}" stroke="currentColor" stroke-dasharray="4 4" stroke-opacity=".5"/>')
    s.append(f'<circle cx="{x3:.1f}" cy="{y3:.1f}" r="4" fill="#c0392b"/><text x="{x3+8:.1f}" y="{y3-8:.1f}" fill="currentColor">l = 3: 3 - &#8730;3 = 1.2679 (both branches)</text>')
    for v in (1.0501, 1.1010, 1.1348):
        s.append(f'<circle cx="{x3:.1f}" cy="{Y(v):.1f}" r="3" fill="none" stroke="currentColor"/>')
    s.append(f'<text x="{x3+8:.1f}" y="{Y(1.1010)+4:.1f}" fill="currentColor">r&#8322;, r&#8323;, r&#8324; as quoted in arXiv:2301.10101</text>')
    s.append(f'<text x="{X(0.15):.1f}" y="{Y(1.72):.1f}" fill="currentColor">branch l &lt; 3: (3+l)/(l+&#8730;3)</text>')
    s.append(f'<text x="{X(6.2):.1f}" y="{Y(1.12):.1f}" fill="currentColor">branch l &gt; 3: 1 + 2/(1+&#8730;l)&#178;</text>')
    s.append(f'<text x="{(L+W-R)/2:.1f}" y="{H-8}" text-anchor="middle" fill="currentColor">l = 2/(&#947;-1)</text>')
    s.append('</svg>'); return "\n".join(s)

BLOCK = """<!--REYE-BEGIN--><h2>5c &middot; The limiting speed r<sub>eye</sub></h2>
<p>The symbol r with an eye subscript is the limiting blow-up speed in Theorem 1.1 of Merle, Rapha&euml;l, Rodnianski and Szeftel, <em>On the implosion of a three dimensional compressible fluid</em> (arXiv:1912.11009), defined in their (1.4). With &#8467; = 2/(&#947;&minus;1) and dimension d:</p>
<p style="text-align:center">r<sub>eye</sub>(d,&#8467;) = (d+&#8467;)/(&#8467;+&#8730;d) for &#8467; &lt; d, and r<sub>eye</sub>(d,&#8467;) = 1 + (d&minus;1)/(1+&#8730;&#8467;)&#178; for &#8467; &gt; d.</p>
<p>The theorem (d = 3, &#8467; &ne; 3, &#8467; outside a countable exceptional set) gives a discrete sequence of blow-up speeds 1 &lt; r<sub>k</sub> &lt; r<sub>eye</sub>(3,&#8467;) with r<sub>k</sub> &rarr; r<sub>eye</sub>(3,&#8467;). The curve below is the formula only: no equation is solved here.</p>
__SVG__
<p><strong>What is and is not checked.</strong> The formulas, the range &#8467; &gt; &#8730;3 for Navier&ndash;Stokes and the lower bound &#8467;<sub>0</sub>(3) = &#8730;3 were read from the typeset pages 4 and 5 of arXiv:1912.11009v2 (PDF, 17 June 2020) and agree with the LaTeX source of the arXiv HTML version. A plain-text extraction of the paper had lost every square-root sign and so read &#8467; &gt; 3 and &#947; &lt; (2+&#8730;3)/3; that was an extraction loss, not a difference in the paper. The verifier recomputes the algebra: the branches meet at 3 &minus; &#8730;3 when &#8467; = d = 3, (1.8) solves to &#8467; &gt; &#8467;<sub>0</sub>(d) = (2&#8730;d &minus; d)/(d &minus; 1 &minus; &#8730;d) with &#8467;<sub>0</sub>(3) = &#8730;3, and <em>e</em> &gt; 0 of (1.12) is the same as &#947; &lt; (2+&#8730;3)/&#8730;3. The theorem also excludes &#8467; = 3. The blow-up rates are &#8214;u&#8214;<sub>&#8734;</sub> ~ (T&minus;t)<sup>&minus;(r<sub>k</sub>&minus;1)/r<sub>k</sub></sup> and &#8214;&#961;&#8214;<sub>&#8734;</sub> ~ (T&minus;t)<sup>&minus;&#8467;(r<sub>k</sub>&minus;1)/r<sub>k</sub></sup>. The values r<sub>2</sub>, r<sub>3</sub>, r<sub>4</sub> are quoted from the review arXiv:2301.10101 and not recomputed. The Annals Part I was not read; this is the earlier arXiv paper.</p>
<p><strong>Derived from the equations, not only read.</strong> <a class="mono" href="reye-derive.py">reye-derive.py</a> starts from radial isentropic Euler, puts in the self-similar ansatz with speed r, reduces it to a two-dimensional autonomous ODE, and computes the eigenvalue ratio k at the sonic point. For &#947; = 5/3 and d = 3 it gives exactly k = 2, 3, 4 at the three values r<sub>2</sub>, r<sub>3</sub>, r<sub>4</sub> quoted in the review, so those values and this ODE agree. For &#8467; &lt; d, in five cases ((d,&#8467;) = (3,0.5), (3,1), (3,2), (2,1), (4,2)), the smaller eigenvalue goes to zero linearly as r rises to the formula (d+&#8467;)/(&#8467;+&#8730;d), so k diverges exactly there. For &#8467; &gt; d the same script was not able to resolve the behaviour near the formula&#8217;s r<sub>+</sub> (the sonic-point root finding is noisy), and nothing is claimed about that branch from it. This is floating point, and it does not prove that smooth self-similar profiles exist. <a class="mono" href="ReyeAlgebra.lean">ReyeAlgebra.lean</a> states four algebraic facts about the formula (the branches agree at &#8467; = d for every d, the threshold &#8467; &gt; &#8730;3 for d = 3, and positivity on the r<sub>+</sub> branch) and was compiled by the author and all four theorems are clean (standard axioms only); one of them, <span class="mono">threshold_three</span>, needed a rewrite because the Mathlib lemma name <span class="mono">div_lt_div_iff</span> no longer exists.</p>
<h2>5d &middot; Why two reports, and what the check can and cannot show</h2>
<p>The previous section rests on a check with two independent parties: a value quoted in a review (r<sub>2</sub>, r<sub>3</sub>, r<sub>4</sub> for &#947; = 5/3) and the same value recomputed here from the equations. The check could have failed, and it did not: the ratio came out 2, 3 and 4. That is the whole content of the check. It is not blind, since the review&#8217;s values were known before the ODE was solved, and agreement shows that two routes meet, not that either is right about the fluid. <a class="mono" href="Witness.lean">Witness.lean</a> states the elementary fact behind the practice of this book of giving every number two routes (the exact script and Lean, then the author&#8217;s own compile). Model: a testimony is one report from each party about the same matter, and the only check the parties can run on each other is whether the reports agree. <span class="mono">witness_minimum</span> says that this check can fail for some profile of reports exactly when there are at least two parties and at least two possible reports; with one party it cannot fail, so the report cannot be contradicted by anyone who gave it. <span class="mono">majority_three</span> and <span class="mono">no_majority_two</span> say that with two disagreeing parties a dispute is detected but not located, and that with three yes/no reports a strict majority always exists. The file compiled clean (all six theorems, standard axioms only). It says nothing about truth, independence of the parties, or the sources it is named after; its header says so.</p><!--REYE-END-->"""

h = PAGE.read_text(encoding="utf-8")
blk = BLOCK.replace("__SVG__", svg())
if "<!--REYE-BEGIN-->" in h:
    h = re.sub(r"<!--REYE-BEGIN-->.*?<!--REYE-END-->", lambda m: blk, h, flags=re.S)
else:
    k = h.index("<!--FIGS-END-->") + len("<!--FIGS-END-->")
    h = h[:k] + "\n\n" + blk + h[k:]
PAGE.write_text(h, encoding="utf-8"); print("wrote r_eye section")
