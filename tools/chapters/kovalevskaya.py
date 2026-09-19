#!/usr/bin/env python3
"""Book VII -- Sofia Kovalevskaya. Replaces the stub."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figure_chapter import build, TAGCSS

P1 = [
"""She contracted a marriage she did not want in order to leave Russia, because an
unmarried woman could not. Berlin would not admit her, so Weierstrass taught her privately
for four years and then pushed three papers through G&ouml;ttingen for a doctorate
<em>in absentia</em>, 1874. She could not get a post. She taught arithmetic in a girls'
school, and for six years did no mathematics at all. Stockholm took her in 1884, made her
full professor in 1889, and she died of influenza in 1891, forty-one years old.
<span class="tag t-cited">CITED</span>""",

"""In 1888 the Paris Academy set its Bordin Prize on rigid-body motion. Entries were
anonymous. Hers was judged so far beyond the others that the Academy raised the prize from
3&nbsp;000 francs to 5&nbsp;000 before opening the envelope.""",
]

P2 = [
"""A heavy rigid body turning about a fixed point has six state variables and,
generically, three conserved quantities: energy, the vertical component of angular
momentum, and $|\\gamma|^2 = 1$. Three integrals for six variables is one short of what
Liouville integrability needs. <strong>A fourth integral exists only for special bodies.</strong>""",

"""Two were known and had been for a century. Euler's case: no gravity term &mdash; the
body pivots about its centre of mass. Lagrange's case: $A = B$ with the centre of mass on
the symmetry axis &mdash; the top every child has spun.""",

"""Kovalevskaya found the third, and it is not a symmetry anyone would have guessed:""",

'''<div class="box"><div class="box-label">The Kovalevskaya top</div>
<p class="block-prose" style="text-align:center;font-size:1.1rem">$A = B = 2C$, centre of
mass in the <em>equatorial</em> plane</p>
<p class="block-prose" style="text-align:center">
$K = \\big[(p^2 - q^2) - c\\gamma_1\\big]^2 + \\big[2pq - c\\gamma_2\\big]^2$</p></div>''',

"""In 1906 Husson proved there are no others. Three cases, and that is the complete list
for a heavy rigid body about a fixed point. <span class="tag t-cited">CITED</span>""",
]

P3 = [
"""Integrate the Euler&ndash;Poisson equations and watch the four quantities. Energy,
vertical angular momentum and $|\\gamma|^2$ hold to $10^{-14}$ whatever the body, because
they are conserved for every body. $K$ is the one that discriminates:""",

'<div class="box"><div class="box-label">relative drift over 8 time units, RK4, h = 10<sup>&minus;4</sup></div>'
'<p class="block-prose" style="font-family:ui-monospace,monospace;font-size:.86rem">'
'A = B = 2, C = 1.0 &nbsp;&nbsp;(A = B = 2C) &nbsp;&nbsp; K drift &nbsp;<b>3.3 &times; 10<sup>&minus;14</sup></b><br>'
'A = B = 2, C = 1.3 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; K drift &nbsp;9.8 &times; 10<sup>&minus;1</sup><br>'
'A = B = 2, C = 0.8 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; K drift &nbsp;1.2<br>'
'A = B = 2, C = 0.5 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; K drift &nbsp;7.2 &times; 10<sup>&minus;1</sup>'
' &nbsp;<span class="tag t-computed">COMPUTED</span></p></div>',

"""Thirteen orders of magnitude between $C = 1$ and $C = 1.3$. <strong>Integrability is not
a matter of degree.</strong> The quantity is either conserved or it is not, and the set of
bodies for which it is conserved has measure zero in the space of bodies.""",
]

P4 = [
"""The method is the part this corpus should be reading, and it is stranger than the
result.""",

"""She did not look for a conserved quantity. <strong>She asked where the solutions have
their singularities in <em>complex</em> time</strong>, and demanded that they be poles
&mdash; that the solution be meromorphic, single-valued, with no branch points. Then she
solved for which bodies that is true. The answer was $A = B = 2C$ with the centre of mass
off the axis, a condition nobody had reason to write down.""",

"""This is the Painlev&eacute; property, and she is using it in 1888, before Painlev&eacute;.
The logic is: <em>the singularity structure of the continued solution decides the
qualitative behaviour of the real one.</em> Go out into the complex plane, look at what
kind of singularity you find, come back and know something about the motion you can
actually see.""",

'''<div class="box"><div class="box-label">Why this is in the series</div>
<p class="block-prose">The dm&sup3; chain reads a system by its fold &mdash; the place where
the map degenerates &mdash; and infers the branch structure from it. Kovalevskaya's move is
the same move in a different setting: <strong>classify by the singularity, not by the
regular behaviour.</strong> What she adds is that the singularity worth classifying may not
be anywhere on the real trajectory at all.</p>
<p class="block-prose">And the threshold is exact. $A = B = 2C$ is a codimension-one
condition in the space of inertia tensors; a body one percent off it has no fourth
integral, not a slightly worse one. <span class="tag t-shown">SHOWN</span></p></div>''',

"""The other half of her name sits in the corpus's foundations rather than its gallery.
The Cauchy&ndash;Kovalevskaya theorem &mdash; analytic Cauchy data, analytic coefficients,
a unique analytic solution locally &mdash; is the existence statement under every
initial-value problem written in this series, and it is the one theorem here that is
quoted more often than it is attributed.""",
]

build(
 slug="kovalevskaya",
 name="Sofia Kovalevskaya",
 hero_sub="She found the third and last integrable top by asking where the solution "
          "misbehaves in <em>complex</em> time &mdash; and demanding that it misbehave politely. "
          "Classify by the singularity, not by the regular part.",
 description="Sofia Kovalevskaya: the third integrable case of the heavy top at A=B=2C, its "
             "fourth integral verified to 3e-14 and shown to fail by 100% one step off, and the "
             "Painleve method she used in 1888 before Painleve.",
 parts=[
   ("Part I &middot; 1888", "The prize the Academy raised before opening the envelope", P1),
   ("Part II &middot; Three Tops", "One integral short", P2),
   ("Part III &middot; The Number", "Thirteen orders of magnitude", P3),
   ("Part IV &middot; The Method", "Where the solution misbehaves", P4),
 ],
 place_rows=[
   ("C", "the inertia tensor &mdash; the body, fixed once", "compression: the constraint"),
   ("K", "$C$ moved toward $A/2$", "approach to the condition"),
   ("F", "$A = B = 2C$: the fourth integral appears, or does not",
        "the fold &mdash; threshold, not scale <span class=\"tag t-shown\">SHOWN</span>"),
   ("U", "the motion, now foliated by $K$ into invariant tori",
        "the branch the system settles on <span class=\"tag t-computed\">COMPUTED</span>"),
 ],
 refs=[
  "S. Kowalevski, &ldquo;Sur le probl&egrave;me de la rotation d&rsquo;un corps solide autour d&rsquo;un point fixe&rdquo;, <em>Acta Mathematica</em> 12, 1889, 177&ndash;232 &mdash; the Bordin Prize memoir.",
  "S. v. Kowalevsky, &ldquo;Zur Theorie der partiellen Differentialgleichungen&rdquo;, <em>Crelle</em> 80, 1875 &mdash; the Cauchy&ndash;Kovalevskaya theorem.",
  "&Eacute;. Husson, &ldquo;Recherche des int&eacute;grales alg&eacute;briques dans le mouvement d&rsquo;un solide pesant autour d&rsquo;un point fixe&rdquo;, <em>Ann. Fac. Sci. Toulouse</em> 8, 1906 &mdash; the completeness of the three cases.",
  "V. V. Golubev, <em>Lectures on the Integration of the Equations of Motion of a Rigid Body about a Fixed Point</em>, Moscow, 1953.",
  "A. Goriely, <em>Integrability and Nonintegrability of Dynamical Systems</em>, World Scientific, 2001 &mdash; chapter 2 for Kovalevskaya exponents and the Painlev&eacute; test.",
  "R. Cooke, <em>The Mathematics of Sonya Kovalevskaya</em>, Springer, 1984.",
 ],
 prev=("ch-noether.html", "Emmy Noether"),
 nxt=("ch-mirzakhani.html", "Maryam Mirzakhani"),
 verify="book7/ch-kovalevskaya-verify.py",
 extra_css=TAGCSS,
)
