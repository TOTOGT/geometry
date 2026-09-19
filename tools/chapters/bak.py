#!/usr/bin/env python3
"""Book VII -- Per Bak. Replaces the stub."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figure_chapter import build, TAGCSS

P1 = [
"""Bak, Tang and Wiesenfeld published <em>Self-Organized Criticality: An Explanation of
1/f Noise</em> in 1987, and the model in it is a pile of sand. Add one grain at a time.
When a site holds four, it topples: four grains leave, one to each neighbour, and grains at
the edge fall off. Repeat.""",

"""The claim was large and Bak made it larger in the book &mdash; <em>How Nature Works</em>,
1996 &mdash; where earthquakes, extinctions, forest fires, traffic and the economy are all
the same pile. <strong>That claim is contested and this page does not endorse it.</strong>
Sandpile experiments with real sand mostly do not show it; the earthquake case is
strong, the biological cases much less so.
<span class="tag t-open">OPEN</span> <span class="tag t-cited">CITED</span>""",

"""The model is a different matter. It is exact, it is beautiful, and it says something
this corpus needed and did not have.""",
]

P2 = [
"""Start with the theorem, because it is the one part of this chapter that is not
statistics.""",

'''<div class="box"><div class="box-label">Dhar, 1990 &mdash; the abelian property</div>
<p class="block-prose">An unstable configuration stabilises to a <strong>unique</strong>
final state, and the number of topplings is the same, <em>whatever order the topplings are
performed in</em>.</p></div>''',

"""Tested by stabilising the same random configuration twice, once last-in-first-out and
once first-in-first-out: <strong>identical final grid and identical toppling count, every
trial.</strong> Not close &mdash; equal.
<span class="tag t-computed">COMPUTED</span>""",

"""This is worth sitting with. The intermediate history is wildly different: different
sites topple, in different orders, at different moments. The endpoint does not care. A
system whose path is arbitrary and whose destination is not &mdash; which is the property
the dm&sup3; chain claims for $G = U \\circ F \\circ K \\circ C$ and rarely gets to verify on
something exact.""",
]

P3 = [
"""Drive the pile &mdash; one grain at a time, always waiting for the avalanche to finish
&mdash; and it walks to a stationary state and stays there.""",

'<div class="box"><div class="box-label">stationary density, grains per site</div>'
'<p class="block-prose" style="font-family:ui-monospace,monospace;font-size:.86rem;line-height:1.9">'
'N = &nbsp;16 &nbsp;&rarr;&nbsp; 2.045<br>'
'N = &nbsp;32 &nbsp;&rarr;&nbsp; 2.084<br>'
'N = &nbsp;64 &nbsp;&rarr;&nbsp; 2.104<br>'
'N = 100 &nbsp;&rarr;&nbsp; 2.109 &nbsp;<span style="opacity:.7">(after 200&thinsp;000 drops)</span><br>'
'literature &nbsp;&rarr;&nbsp; 2.125 as N &rarr; &infin;'
' &nbsp;<span class="tag t-computed">COMPUTED</span></p></div>',

'''<div class="box"><div class="box-label">A measurement this page got wrong first</div>
<p class="block-prose">The N = 100 run initially returned <strong>2.064</strong>, which
would have broken the monotone trend and looked like a real finite-size effect. It was not:
the burn-in was 18&thinsp;000 drops for a 10&thinsp;000-site lattice, and the pile had not
reached stationarity. At 20&thinsp;000 drops the density is 1.982; at 50&thinsp;000 it is
2.106; at 200&thinsp;000, 2.109. <strong>The first number measured the transient and
would have been published as the answer.</strong> It is recorded here rather than
silently replaced.</p></div>''',

"""Nobody set the density. There is no knob. The pile is driven from outside by a process
that knows nothing about criticality &mdash; drop a grain anywhere &mdash; and it arrives at
one particular density and holds it.""",
]

P4 = [
"""And at that density the avalanches have no characteristic size. The distribution is a
power law $P(s) \\sim s^{-\\tau}$ over every decade the lattice is large enough to show. A
grain lands; usually nothing; sometimes four sites topple; occasionally forty thousand.""",

"""<strong>This page does not claim to have measured $\\tau$.</strong> The fits here give
$1.03$ to $1.16$ depending on lattice size and fitting window, against a literature value
near $1.2$ for the two-dimensional model. The discrepancy is the well-known one &mdash;
these exponents are notoriously sensitive to finite size, to the fitting range, and to
whether one counts topplings or distinct sites &mdash; and resolving it needs lattices and
statistics far beyond what a chapter's verify script should run.
<span class="tag t-open">OPEN</span>""",

'''<div class="box"><div class="box-label">The tension this chapter exists to state</div>
<p class="block-prose">This corpus's rule <strong>R10</strong> is <em>threshold, not
scale</em>: the fold happens at a point, the kind changes there, and nothing about it is
gradual. Every chapter in this gallery so far has been an instance &mdash; the conic at
$\\beta = \\alpha$, the plate at a degenerate eigenvalue, the top at $A = B = 2C$, the
reaction at $d_c$.</p>
<p class="block-prose">Bak's pile is the apparent counterexample. Its avalanches are
<em>scale-free</em>: no characteristic size, a power law, the opposite of a threshold.</p>
<p class="block-prose"><strong>They are not in conflict, and saying why is the point.</strong>
R10 governs the control parameter: there is a critical value and the behaviour changes
there. Self-organised criticality is what happens when the dynamics <em>drives the control
parameter to that value and pins it</em>. You do not get scale-free response near the
threshold. You get it <em>at</em> the threshold &mdash; and Bak's contribution is the
mechanism by which a system arrives there with nobody tuning it.</p>
<p class="block-prose">Which is the piece the chain was missing. $K$ drives curvature toward
$\\kappa^*$; nothing in the corpus said why a system should sit at $\\kappa^*$ rather than
pass through it. <span class="tag t-shown">SHOWN</span> for the sandpile;
<span class="tag t-open">OPEN</span> for dm&sup3;.</p></div>''',
]

build(
 slug="bak",
 name="Per Bak",
 hero_sub="A pile of sand drives itself to its own critical point and stays there. That is the "
          "piece the chain was missing &mdash; not where the threshold is, but why a system should "
          "sit on it rather than pass through.",
 description="Per Bak: the abelian sandpile, Dhar's theorem verified exactly, the stationary "
             "density approaching 2.125, and why scale-free avalanches do not contradict "
             "threshold-not-scale.",
 parts=[
   ("Part I &middot; 1987", "A pile of sand, and a claim about everything", P1),
   ("Part II &middot; The Theorem", "The order does not matter", P2),
   ("Part III &middot; The Density Nobody Set", "Where it settles", P3),
   ("Part IV &middot; Scale-Free", "The tension, and why there is none", P4),
 ],
 place_rows=[
   ("C", "one grain, dropped anywhere &mdash; a driving that knows nothing",
        "compression: the constraint applied blindly"),
   ("K", "the density climbing to 2.125 on its own",
        "$\\kappa \\to \\kappa^*$ &mdash; <b>driven by the dynamics, not by a parameter</b>"),
   ("F", "a toppling &mdash; four grains leave, and may set off any number more",
        "the fold <span class=\"tag t-shown\">SHOWN</span>"),
   ("U", "the unique stable configuration, independent of toppling order",
        "Dhar's abelian property <span class=\"tag t-computed\">COMPUTED</span>"),
 ],
 refs=[
  "P. Bak, C. Tang and K. Wiesenfeld, &ldquo;Self-organized criticality: an explanation of 1/f noise&rdquo;, <em>Phys. Rev. Lett.</em> 59, 1987, 381&ndash;384.",
  "D. Dhar, &ldquo;Self-organized critical state of sandpile automaton models&rdquo;, <em>Phys. Rev. Lett.</em> 64, 1990, 1613&ndash;1616 &mdash; the abelian property and the sandpile group.",
  "P. Bak, <em>How Nature Works: The Science of Self-Organized Criticality</em>, Copernicus, 1996 &mdash; and the claims this page marks OPEN.",
  "P. Grassberger and S. S. Manna, &ldquo;Some more sandpiles&rdquo;, <em>J. Physique</em> 51, 1990 &mdash; for the stationary density and the exponent estimates.",
  "H. J. Jensen, <em>Self-Organized Criticality</em>, Cambridge, 1998.",
  "J. Feder, &ldquo;The evidence for self-organized criticality in sandpile dynamics&rdquo;, <em>Fractals</em> 3, 1995 &mdash; on what real sand does and does not do.",
 ],
 prev=("ch-mirzakhani.html", "Maryam Mirzakhani"),
 nxt=("ch-turing.html", "Alan Turing"),
 verify="book7/ch-bak-verify.py",
 extra_css=TAGCSS,
)
