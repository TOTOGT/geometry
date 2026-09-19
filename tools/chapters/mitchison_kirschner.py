#!/usr/bin/env python3
"""Book VII -- Mitchison & Kirschner. Replaces the stub."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figure_chapter import build, TAGCSS

P1 = [
"""Before 1984 the assumption about a polymer in solution was that it approaches a steady
state: monomers on, monomers off, length settling toward whatever the concentration
supports. Tim Mitchison and Marc Kirschner looked at individual microtubules and found that
no microtubule does this.""",

"""Each one is either <em>growing</em> or <em>shrinking</em>, at very different speeds,
and switches between the two abruptly and at random. Growth is slow, around
$2\\ \\mu\\mathrm{m}/\\mathrm{min}$; collapse is fast, an order of magnitude faster. The
switch from growth to collapse they named <em>catastrophe</em>; the switch back,
<em>rescue</em>. <span class="tag t-cited">CITED</span>""",

'''<div class="box"><div class="box-label">The observation, stated exactly</div>
<p class="block-prose"><strong>The population is at steady state. No member of it is.</strong>
The mean length of the ensemble sits still while every individual is doing something violent,
and the stillness is a statistical fact about a collection, not a property of anything in
it.</p></div>''',

"""A corpus that reasons about attractors should take that seriously. An average that is
constant is not evidence that anything has settled.""",
]

P2 = [
"""The mechanism they proposed is a threshold, and it is the cleanest one in cell biology.""",

"""Tubulin arrives carrying GTP. It is hydrolysed to GDP some time after it is
incorporated, and GDP-tubulin in the lattice is strained &mdash; it wants to curl outward
and would peel the tubule apart if it were exposed. So long as hydrolysis lags behind
addition, the tip carries a layer of GTP-tubulin holding the strained body together.""",

'''<div class="box"><div class="box-label">the GTP cap</div>
<p class="block-prose">While the cap exists the microtubule grows. If addition falters,
hydrolysis catches the tip, the cap is lost, and the strained lattice below unpeels at full
speed. <strong>Not gradually weaker &mdash; there, then not there.</strong></p></div>''',

"""The fold, in the corpus's own vocabulary: a control quantity (cap size) is driven toward
zero, and at zero the system does not become slightly less stable. It changes branch, and
the branch it changes to is travelling twenty times faster in the other direction.""",
]

P3 = [
"""The two-state model has an exact threshold, and it decides whether a cell can build
anything.""",

'<div class="box"><div class="box-label">bounded or unbounded</div>'
'<p class="block-prose" style="text-align:center;font-size:1.15rem">'
'$$J = v_g f_{\\mathrm{res}} - v_s f_{\\mathrm{cat}}$$</p>'
'<p class="block-prose">$J &lt; 0$: lengths reach a stationary distribution with mean '
'$\\langle L\\rangle = v_g v_s / (v_s f_{\\mathrm{cat}} - v_g f_{\\mathrm{res}})$. '
'$J &gt; 0$: the mean length grows without bound.</p></div>',

"""Simulated, with $v_g = 2$, $v_s = 20\\ \\mu\\mathrm{m}/\\mathrm{min}$,
$f_{\\mathrm{cat}} = 0.3/\\mathrm{min}$:""",

'<p class="block-prose" style="font-family:ui-monospace,monospace;font-size:.85rem;line-height:1.85">'
'f<sub>res</sub>=0.1 &nbsp; J=&minus;5.80 &nbsp; &lang;L&rang;=&nbsp;&nbsp;7.19 &nbsp; theory &nbsp;6.90<br>'
'f<sub>res</sub>=1.0 &nbsp; J=&minus;4.00 &nbsp; &lang;L&rang;=&nbsp;10.42 &nbsp; theory 10.00<br>'
'f<sub>res</sub>=2.0 &nbsp; J=&minus;2.00 &nbsp; &lang;L&rang;=&nbsp;20.19 &nbsp; theory 20.00<br>'
'f<sub>res</sub>=2.9 &nbsp; J=&minus;0.20 &nbsp; &lang;L&rang;=292.41 &nbsp; theory 200.00<br>'
'<b>f<sub>res</sub>=3.0 &nbsp; J=&nbsp;0.00 &nbsp; &lang;L&rang;=711 &nbsp; and rising</b><br>'
'f<sub>res</sub>=5.0 &nbsp; J=+4.00 &nbsp; &lang;L&rang;=7954 &nbsp; and rising'
' &nbsp;<span class="tag t-computed">COMPUTED</span></p>',

'''<div class="box"><div class="box-label">The test is not the number, it is whether the number depends on how long you watch</div>
<p class="block-prose">In the bounded phase $\\langle L\\rangle$ is <em>the same</em> at
$T = 2\\,000$ and $T = 20\\,000$ minutes &mdash; 9.48, 9.46, 10.12, 10.42. In the unbounded
phase it <em>doubles when the observation doubles</em> &mdash; 842, 1955, 4005, 7954.</p>
<p class="block-prose">A single long run cannot tell the two apart; a mean length of 700
looks like a large number either way. Only the dependence on observation time does, and
this is the general form of a mistake this corpus has made twice today in other
chapters: a statistic reported from a run that had not reached the regime it was measuring.
<span class="tag t-shown">SHOWN</span></p></div>''',
]

P4 = [
"""The microtubule has thirteen protofilaments &mdash; thirteen parallel tracks of tubulin
closing into a tube. This is not the only number the lattice can take: assemblies with
eleven to sixteen occur in vitro and in some organisms, and the number is set by the
nucleating template. <strong>Thirteen is the number in almost every animal cell, and it is
the number for which the protofilaments run parallel to the tube axis rather than winding
around it.</strong> A kinesin walking a wound track spirals; on thirteen it goes straight.
<span class="tag t-cited">CITED</span>""",

'''<div class="box"><div class="box-label">A conjecture of this corpus, marked as one</div>
<p class="block-prose">The index card for this chapter reads <em>13 protofilaments
(Fibonacci)</em>, and the temptation is to connect thirteen to the ladder that runs through
Book VI. <strong>This page does not make that connection, because no argument for it exists
here.</strong> Thirteen is a Fibonacci number; so are eight and twenty-one, and the
microtubule is not eight or twenty-one for reasons that are about lattice geometry and the
&gamma;-tubulin ring, not about recurrences.</p>
<p class="block-prose">The established fact is the supertwist: thirteen is where it
vanishes. Whether that has anything to do with the corpus's ladder is
<span class="tag t-open">OPEN</span>, and writing it down as though it were settled would
be the exact failure this series keeps auditing itself for.</p></div>''',

"""What the chapter does establish is the shape. A cell holds a structure in place by
running every element of it at a threshold, letting individuals fail constantly, and
reading only the population. <a href="ch-bak.html">Bak</a>'s pile does the same thing with
sand. The microtubule does it with a nucleotide, and it does it in every dividing cell in
your body, right now, about once a minute.""",
]

build(
 slug="mitchison-kirschner",
 name="Mitchison &amp; Kirschner",
 hero_sub="Every microtubule is either growing or collapsing, and switches at random. The "
          "population sits at a steady state that no individual in it occupies &mdash; which "
          "means a constant average is not evidence that anything has settled.",
 description="Mitchison and Kirschner 1984: dynamic instability, the GTP cap as a threshold, "
             "and the bounded/unbounded transition at J = vg*fres - vs*fcat, with the diagnostic "
             "that only dependence on observation time distinguishes the phases.",
 parts=[
   ("Part I &middot; Nature, 1984", "Nobody is at the steady state", P1),
   ("Part II &middot; The Cap", "There, then not there", P2),
   ("Part III &middot; The Threshold", "Bounded, or not", P3),
   ("Part IV &middot; Thirteen", "What the number is, and what it is not", P4),
 ],
 place_rows=[
   ("C", "tubulin-GTP arriving &mdash; the monomer pool, fixed",
        "compression: the constraint"),
   ("K", "hydrolysis catching up with addition; the cap thinning",
        "curvature driven to $\\kappa^*$"),
   ("F", "catastrophe &mdash; the cap gone, the strained lattice unpeeling at 20 &micro;m/min",
        "the fold <span class=\"tag t-shown\">SHOWN</span>"),
   ("U", "rescue, or the population mean &mdash; whichever is the observable",
        "the branch, read statistically <span class=\"tag t-computed\">COMPUTED</span>"),
 ],
 refs=[
  "T. Mitchison and M. Kirschner, &ldquo;Dynamic instability of microtubule growth&rdquo;, <em>Nature</em> 312, 1984, 237&ndash;242.",
  "T. Mitchison and M. Kirschner, &ldquo;Microtubule assembly nucleated by isolated centrosomes&rdquo;, <em>Nature</em> 312, 1984, 232&ndash;237.",
  "M. Dogterom and S. Leibler, &ldquo;Physical aspects of the growth and regulation of microtubule structures&rdquo;, <em>Phys. Rev. Lett.</em> 70, 1993 &mdash; the bounded/unbounded criterion used here.",
  "D. Chr&eacute;tien and R. H. Wade, &ldquo;New data on the microtubule surface lattice&rdquo;, <em>Biol. Cell</em> 71, 1991 &mdash; protofilament number and supertwist.",
  "H. V. Goodson and E. M. Jonasson, &ldquo;Microtubules and microtubule-associated proteins&rdquo;, <em>Cold Spring Harb. Perspect. Biol.</em> 10, 2018.",
 ],
 prev=("ch-katherine-johnson.html", "Katherine Johnson"),
 nxt=("ch-klein-thymus.html", "Ludger Klein"),
 verify="book7/ch-mitchison-kirschner-verify.py",
 extra_css=TAGCSS,
)
