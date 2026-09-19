#!/usr/bin/env python3
"""Book VII -- Maryam Mirzakhani. Replaces the stub."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figure_chapter import build, TAGCSS

P1 = [
"""Her 2004 Harvard thesis did three things that had been separate problems, and did them
with one idea. It computed the Weil&ndash;Petersson volumes of moduli space. It gave a new
proof of Witten's conjecture, which Kontsevich had proved in 1992 by an entirely different
route. And it counted simple closed geodesics on a hyperbolic surface. The Fields Medal
came in 2014, the first to a woman. She died in 2017, forty years old.
<span class="tag t-cited">CITED</span>""",

"""The idea is a recursion, and the shape of it is why this chapter belongs in a corpus
about unfolding: <strong>to know a surface, integrate over all the ways of cutting it.</strong>
A pair of pants comes off along a simple closed curve, and what is left is a smaller
surface of the same kind. The volume of the whole is an integral of the volumes of the
pieces over where the cut can be made.""",
]

P2 = [
"""Moduli space $\\mathcal{M}_{g,n}$ &mdash; hyperbolic surfaces of genus $g$ with $n$
boundary geodesics of lengths $L_1, \\ldots, L_n$ &mdash; carries the Weil&ndash;Petersson
symplectic form, and so a volume. Mirzakhani's theorem is that the volume is a
<em>polynomial</em>:""",

'''<div class="box"><div class="box-label">the first few volumes</div>
<p class="block-prose" style="font-family:ui-monospace,monospace;font-size:.85rem;line-height:2">
V<sub>0,3</sub> = 1<br>
V<sub>1,1</sub>(b) = (b&sup2; + 4&pi;&sup2;) / 48<br>
V<sub>0,4</sub>(b<sub>1</sub>&hellip;b<sub>4</sub>) = 2&pi;&sup2; + (b<sub>1</sub>&sup2;+b<sub>2</sub>&sup2;+b<sub>3</sub>&sup2;+b<sub>4</sub>&sup2;)/2<br>
V<sub>1,2</sub>(b<sub>1</sub>,b<sub>2</sub>) = (4&pi;&sup2;+b<sub>1</sub>&sup2;+b<sub>2</sub>&sup2;)(12&pi;&sup2;+b<sub>1</sub>&sup2;+b<sub>2</sub>&sup2;) / 192<br>
V<sub>2,0</sub> = 43&pi;<sup>6</sup> / 2160 = 19.138766353582
</p></div>''',

"""A polynomial in $b_1^2, \\ldots, b_n^2$ of degree $3g - 3 + n$, and
<strong>its coefficients are intersection numbers on moduli space</strong> &mdash; the
$\\psi$-classes of Witten's conjecture. That is the second theorem falling out of the
first: compute the volumes and you have computed the intersection numbers, so Witten's
conjecture follows.""",
]

P3 = [
"""These polynomials are not independent of each other, and the relation between them is
the cleanest check a page like this can carry. Norman Do's identity says that evaluating
the derivative at the <em>imaginary</em> boundary length $2\\pi i$ drops you one step down
the recursion:""",

'<div class="box"><div class="box-label">Do&rsquo;s identity</div>'
'<p class="block-prose" style="text-align:center;font-size:1.1rem">'
'$$\\frac{\\partial V_{g,n+1}}{\\partial L_{n+1}}\\big(L, 2\\pi i\\big) = 2\\pi i\\,(2g-2+n)\\,V_{g,n}(L)$$</p></div>',

"""A boundary of imaginary length is not a boundary. The identity is a statement about the
polynomials, and it holds:""",

'<p class="block-prose" style="font-family:ui-monospace,monospace;font-size:.85rem">'
'V<sub>0,4</sub> &rarr; V<sub>0,3</sub> &nbsp;&nbsp; residual 0<br>'
'V<sub>1,2</sub> &rarr; V<sub>1,1</sub> &nbsp;&nbsp; residual 1.3 &times; 10<sup>&minus;13</sup><br>'
'V<sub>2,1</sub> &rarr; V<sub>2,0</sub> &nbsp;&nbsp; recovers 43&pi;<sup>6</sup>/2160 to 4.5 &times; 10<sup>&minus;13</sup>'
' &nbsp;<span class="tag t-computed">COMPUTED</span></p>',

'''<div class="box"><div class="box-label">It settles a convention, which is why it is here</div>
<p class="block-prose">$V_{1,1}$ is printed in the literature both as
$(b^2+4\\pi^2)/24$ and as $(b^2+4\\pi^2)/48$, the factor of two being an orbifold
convention that different authors absorb in different places. <strong>The identity
decides it.</strong> With $/48$ the residual is $1.3\\times10^{-13}$; with $/24$ it is
$5.55$ &mdash; not a rounding, a wrong answer. <span class="tag t-shown">SHOWN</span></p>
<p class="block-prose">A corpus that quotes a constant from a paper without an internal
check has no way to notice it picked up the other convention. This is what one looks
like.</p></div>''',
]

P4 = [
"""The third result is the one to state last because it is the one that sounds wrong.""",

"""On a closed hyperbolic surface, the number of closed geodesics of length at most $L$
grows like $e^L / L$. Exponentially. That is Huber's theorem and it has been known since
1959. Mirzakhani proved that the number of <em>simple</em> closed geodesics &mdash; those
that do not cross themselves &mdash; grows like""",

'<div class="box"><div class="box-label">Mirzakhani, 2008</div>'
'<p class="block-prose" style="text-align:center;font-size:1.15rem">'
'$$s_X(L) \\sim c_X \\cdot L^{\\,6g-6+2n}$$</p>'
'<p class="block-prose">Polynomial. And $6g-6+2n$ is exactly the dimension of the moduli '
'space the volumes live on &mdash; the constant $c_X$ is a Weil&ndash;Petersson volume.</p></div>',

"""<strong>Simple curves are exponentially rare.</strong> Not rare by a constant factor,
not rare by a slowly growing one: the ratio $s_X(L)/(e^L/L)$ goes to zero faster than any
polynomial. Almost every closed geodesic crosses itself, and the ones that do not are
counted by the geometry of the space of all surfaces rather than by the surface they live
on.""",

'''<div class="box"><div class="box-label">Where this sits in the series</div>
<p class="block-prose">The corpus keeps meeting the same structure: a quantity that is not
a matter of degree. A conic is not gradually more elliptical; a top is not <em>almost</em>
integrable; a plate does not almost have a degenerate mode. Here it is again and in a new
form &mdash; <em>simple</em> is not a small perturbation of <em>not simple</em>, and the gap
between them is the whole difference between a polynomial and an exponential.</p>
<p class="block-prose">And the method is the chain's own: cut, evaluate the pieces,
integrate over where the cut could have gone. <a href="ch-kovalevskaya.html">Kovalevskaya</a>
classified by the singularity; Mirzakhani classifies by the decomposition.</p></div>''',
]

build(
 slug="mirzakhani",
 name="Maryam Mirzakhani",
 hero_sub="To know a surface, integrate over all the ways of cutting it. The volumes came out "
          "polynomial, their coefficients were Witten&rsquo;s intersection numbers, and the simple "
          "closed geodesics turned out to be exponentially rare.",
 description="Maryam Mirzakhani: Weil-Petersson volumes as polynomials, Do's identity used to "
             "settle the V_{1,1} convention, and the polynomial growth of simple closed "
             "geodesics against the exponential growth of all of them.",
 parts=[
   ("Part I &middot; One Idea, Three Theorems", "Cut it, and integrate over the cut", P1),
   ("Part II &middot; The Volumes", "Polynomials whose coefficients are intersection numbers", P2),
   ("Part III &middot; The Check", "A boundary of imaginary length", P3),
   ("Part IV &middot; The Count", "Simple curves are exponentially rare", P4),
 ],
 place_rows=[
   ("C", "the pair-of-pants decomposition &mdash; a surface cut along simple curves",
        "compression: the constraint that issues the pieces"),
   ("K", "integration over where the cut can be made", "accumulation toward the recursion's fixed point"),
   ("F", "$b = 2\\pi i$ &mdash; an imaginary boundary, where the polynomial drops a level",
        "the fold <span class=\"tag t-shown\">SHOWN</span>"),
   ("U", "$s_X(L) \\sim c_X L^{6g-6+2n}$ &mdash; the branch that is polynomially thin",
        "unfolding onto the simple locus <span class=\"tag t-cited\">CITED</span>"),
 ],
 refs=[
  "M. Mirzakhani, &ldquo;Simple geodesics and Weil&ndash;Petersson volumes of moduli spaces of bordered Riemann surfaces&rdquo;, <em>Invent. Math.</em> 167, 2007, 179&ndash;222.",
  "M. Mirzakhani, &ldquo;Weil&ndash;Petersson volumes and intersection theory on the moduli space of curves&rdquo;, <em>J. Amer. Math. Soc.</em> 20, 2007, 1&ndash;23.",
  "M. Mirzakhani, &ldquo;Growth of the number of simple closed geodesics on hyperbolic surfaces&rdquo;, <em>Ann. of Math.</em> 168, 2008, 97&ndash;125.",
  "N. Do, &ldquo;Moduli spaces of hyperbolic surfaces and their Weil&ndash;Petersson volumes&rdquo;, arXiv:1103.4674, 2011 &mdash; the identity used above.",
  "M. Kontsevich, &ldquo;Intersection theory on the moduli space of curves and the matrix Airy function&rdquo;, <em>Comm. Math. Phys.</em> 147, 1992.",
  "H. Huber, &ldquo;Zur analytischen Theorie hyperbolischer Raumformen und Bewegungsgruppen II&rdquo;, <em>Math. Ann.</em> 142, 1961 &mdash; the exponential count of all closed geodesics.",
 ],
 prev=("ch-kovalevskaya.html", "Sofia Kovalevskaya"),
 nxt=("ch-tao.html", "Terence Tao"),
 verify="book7/ch-mirzakhani-verify.py",
 extra_css=TAGCSS,
)
