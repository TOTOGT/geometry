#!/usr/bin/env python3
"""Book VII -- Alan Turing. Replaces the stub."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figure_chapter import build, TAGCSS

P1 = [
"""The machine is not the brick. Every gallery has Turing for the machine, and the
machine is genuinely his, and it is not why this chapter exists. The brick under this
corpus is the last paper he published: <em>The Chemical Basis of Morphogenesis</em>,
Philosophical Transactions of the Royal Society, 1952. He was prosecuted the same year,
under a law that was not repealed in his lifetime, and died in 1954 at forty-one. The
morphogenesis paper was the work he was doing at the time.
<span class="tag t-cited">CITED</span>""",

"""It asks a question that had no mathematical answer: how does a sphere of identical
cells become a thing with a front and a back? Nothing in the sphere distinguishes one
direction from another. Something has to break the symmetry, and it cannot be an
instruction from outside, because there is nothing outside.""",
]

P2 = [
"""His answer is a paradox stated precisely, and it is the reason the paper is a brick
rather than an essay.""",

'''<div class="box"><div class="box-label">Turing&rsquo;s instability</div>
<p class="block-prose">Take two chemicals that react. Suppose the reaction alone is
<em>stable</em> &mdash; push it off equilibrium and it returns. Now let them diffuse.
<strong>Diffusion, which smooths, can make the stable system unstable</strong>, and the
instability selects a wavelength.</p></div>''',

"""Diffusion is the great destroyer of structure. Drop ink in water and wait. That the
same operator, applied to two species at different rates, <em>creates</em> structure is
not intuition sharpened &mdash; it is intuition reversed, and Turing reversed it with a
linear stability calculation that fits on a page.""",

"""Write the two-species system with diffusion coefficients $1$ and $d$, linearise about
the homogeneous steady state, and look for perturbations $\\propto e^{\\lambda t + ikx}$.
The four conditions are""",

'<div class="box"><div class="box-label">the four Turing conditions</div>'
'<p class="block-prose">$$f_u + g_v &lt; 0,\\qquad f_u g_v - f_v g_u &gt; 0,$$'
'$$d f_u + g_v &gt; 0,\\qquad (d f_u + g_v)^2 &gt; 4d\\,(f_u g_v - f_v g_u)$$</p>'
'<p class="block-prose">The first two say the reaction alone is stable. The last two say '
'that with diffusion it is not. <strong>They are not contradictory, and everything is in '
'the fact that they are not.</strong></p></div>',
]

P3 = [
"""Take the Schnakenberg system, $a = 0.1$, $b = 0.9$. The steady state is
$u^* = 1$, $v^* = 0.9$, and the Jacobian is""",

'<p class="block-prose" style="font-family:ui-monospace,monospace;font-size:.88rem;text-align:center">'
'J = [ +0.8&nbsp;&nbsp;+1.0 ; &minus;1.8&nbsp;&nbsp;&minus;1.0 ]'
' &nbsp;&nbsp; trace = &minus;0.2 &nbsp; det = +1.0</p>',

"""Negative trace, positive determinant: without diffusion it is stable, and it stays
stable no matter how long you wait. Now raise $d$. The third condition needs
$d &gt; 1.25$. The fourth is the one that bites, and it turns on at""",

'<div class="box"><div class="box-label">the threshold</div>'
'<p class="block-prose" style="text-align:center;font-size:1.15rem">'
'$d_c = 8.567627 \\qquad k_c^2 = 0.341641 \\qquad k_c = 0.584500$</p>'
'<p class="block-prose">At $d = 0.98\\,d_c$ the fastest-growing mode has growth rate '
'$-7.86\\times10^{-3}$: everything decays. At $d_c$ it is $-4\\times10^{-9}$ &mdash; zero, '
'numerically. At $1.02\\,d_c$ it is $+7.61\\times10^{-3}$ and a pattern appears with '
'wavenumber $k_c$. <span class="tag t-computed">COMPUTED</span></p></div>',

"""A four-percent change in one ratio takes the system from every perturbation dying to
one specific wavelength growing. <strong>Threshold, not scale.</strong> And the wavelength
is not imposed; $k_c$ falls out of the same algebra that decides whether anything grows at
all. The system is not told how big its stripes should be. It has no alternative.""",
]

P4 = [
"""This is <em>ortogênese</em> in the form the corpus uses the word: form generated under
constraint, in the directions the constraint leaves open. The sphere of identical cells is
not instructed. The chemistry removes every option but one, and the one that is left has a
length.""",

"""Two neighbours in this gallery inherit it directly.
<a href="ch-waddington.html">Waddington</a> drew the epigenetic landscape in 1957 &mdash; the
picture of a cell running out of alternatives &mdash; five years after Turing wrote the
mechanism that carves the valleys. <a href="ch-faraday.html">Faraday</a> and
<a href="ch-sophie-germain.html">Germain</a> hold the other version of the same thing, where
the constraint is a boundary rather than a reaction and the selected wavelength shows up in
sand.""",

'''<div class="box"><div class="box-label">What this chapter does not claim</div>
<p class="block-prose">That real morphogenesis is Turing's mechanism is <em>not</em>
established, and the corpus should not say it is. Turing patterns are confirmed in
chemistry &mdash; the CIMA reaction, Castets and colleagues, 1990 &mdash; and are strongly
supported in a handful of biological systems, including mouse digit spacing and the
ridges of the palate. Across development generally the question is open and actively
argued. <span class="tag t-open">OPEN</span></p>
<p class="block-prose">What is not in doubt is the mathematics, and the mathematics is
what this corpus uses.</p></div>''',
]

build(
 slug="turing",
 name="Alan Turing",
 hero_sub="Not the machine. The last paper: diffusion is what destroys structure, and Turing "
          "showed that two diffusing species can build it &mdash; above one ratio, at one wavelength, "
          "with nothing outside the system to tell it either.",
 description="Alan Turing's 1952 morphogenesis paper: the four Turing conditions, the "
             "diffusion-driven instability, and the threshold d_c = 8.567627 with selected "
             "wavenumber k_c = 0.5845 in the Schnakenberg system.",
 parts=[
   ("Part I &middot; 1952", "The brick is the morphogenesis paper", P1),
   ("Part II &middot; The Reversal", "The smoother that builds", P2),
   ("Part III &middot; The Number", "Where it turns on", P3),
   ("Part IV &middot; Place", "Form under constraint", P4),
 ],
 place_rows=[
   ("C", "two species, one reaction &mdash; the chemistry fixed", "compression: the constraint"),
   ("K", "the diffusion ratio $d$ raised toward $d_c$", "approach to $\\kappa^*$"),
   ("F", "$d = 8.567627$: one mode crosses zero growth",
        "the fold &mdash; threshold, not scale <span class=\"tag t-shown\">SHOWN</span>"),
   ("U", "the pattern at $k_c = 0.5845$, a wavelength nobody chose",
        "unfolding onto the selected branch <span class=\"tag t-computed\">COMPUTED</span>"),
 ],
 refs=[
  "A. M. Turing, &ldquo;The Chemical Basis of Morphogenesis&rdquo;, <em>Phil. Trans. R. Soc. Lond. B</em> 237, 1952, 37&ndash;72.",
  "J. Schnakenberg, &ldquo;Simple chemical reaction systems with limit cycle behaviour&rdquo;, <em>J. Theor. Biol.</em> 81, 1979.",
  "J. D. Murray, <em>Mathematical Biology II: Spatial Models and Biomedical Applications</em>, 3rd ed., Springer, 2003 &mdash; chapter 2 for the conditions as used here.",
  "V. Castets, E. Dulos, J. Boissonade and P. De Kepper, &ldquo;Experimental evidence of a sustained standing Turing-type nonequilibrium chemical pattern&rdquo;, <em>Phys. Rev. Lett.</em> 64, 1990.",
  "R. Sheth <em>et al.</em>, &ldquo;Hox genes regulate digit patterning by controlling the wavelength of a Turing-type mechanism&rdquo;, <em>Science</em> 338, 2012.",
  "C. H. Waddington, <em>The Strategy of the Genes</em>, Allen &amp; Unwin, 1957.",
 ],
 prev=("ch-sophie-germain.html", "Sophie Germain"),
 nxt=("ch-waddington.html", "C. H. Waddington"),
 verify="book7/ch-turing-verify.py",
 extra_css=TAGCSS,
)
