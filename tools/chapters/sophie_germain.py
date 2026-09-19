#!/usr/bin/env python3
"""Book VII -- Sophie Germain. Content; the shell comes from tools/figure_chapter.py."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figure_chapter import build, TAGCSS

P1 = [
"""Sophie Germain taught herself mathematics from her father's library during the
Terror, when she was not permitted to leave the house, and later from lecture notes
borrowed under a dead student's name &mdash; Antoine-Auguste Le Blanc, who had left the
&Eacute;cole Polytechnique. She submitted work under that name to Lagrange, who asked to
meet the author. She wrote to Gauss under it too, for three years, and revealed herself
only when Napoleon's army reached Braunschweig and she feared for his safety.""",

"""Both stories are usually told for their pathos. They are worth telling for something
else: <strong>she chose the pseudonym because the mathematics would be read, and dropped
it when a life was at stake.</strong> The instrument and the judgement were the same
faculty. Gauss wrote back that a woman who overcomes the obstacles to understanding
number theory <em>&ldquo;must have the noblest courage, quite extraordinary talents and
superior genius&rdquo;</em> &mdash; and then, when Go&#776;ttingen offered her an honorary
degree in 1831, she had been dead a month. <span class="tag t-cited">CITED</span>""",

"""She belongs in this gallery twice over, and the two bricks are unrelated to each
other, which is itself unusual. One is in number theory. The other is in the theory of
vibrating surfaces, and it is the one this corpus stands on.""",
]

P2 = [
"""Call a prime $p$ a <em>Germain prime</em> when $2p+1$ is also prime. The first twenty
are""",
'<p class="block-prose" style="font-family:ui-monospace,monospace;font-size:.86rem">2, 3, 5, 11, 23, 29, 41, 53, 83, 89, 113, 131, 173, 179, 191, 233, 239, 251, 281, 293</p>',
"""and there are 190 below $10^4$, 1&nbsp;171 below $10^5$, 7&nbsp;746 below $10^6$.
<span class="tag t-computed">COMPUTED</span> Whether there are infinitely many is open.""",

"""Her theorem, communicated to Legendre and printed in his 1808 supplement, is the first
general result on Fermat's Last Theorem that is not a single exponent:""",

'''<div class="box"><div class="box-label">Germain's theorem &mdash; Case 1</div>
<p class="block-prose">If $p$ is an odd prime and $2p+1$ is prime, then
$x^p + y^p = z^p$ has no integer solution with $p \\nmid xyz$.</p></div>''',

"""One sentence, and it disposes of the first case for infinitely many exponents at once
if the Germain primes are infinite &mdash; and unconditionally for every one of them known.
Legendre extended the auxiliary-prime method she invented; the method, not the
particular primes, is the contribution. Her fuller programme, recovered from the
manuscripts in the 1990s and 2000s, was more ambitious than the corollary she is
remembered for. <span class="tag t-cited">CITED</span>""",
]

P3 = [
"""In 1808 Chladni came to Paris and scattered sand on brass plates. Bowed at the edge,
the sand fled the moving regions and piled on the still ones, and the plate showed its
nodal lines as a figure. Napoleon set a prize: give the mathematical theory of elastic
surfaces and account for Chladni's figures. Nobody entered but Germain. She was the sole
entrant three times, in 1811, 1813 and 1816, and won on the third attempt.""",

"""Her first two attempts were rejected because the variational derivation was wrong in
its handling of the fourth-order terms &mdash; Lagrange corrected it, and the corrected
equation is the one that carries her name. It is a biharmonic:""",

'<div class="box"><div class="box-label">The Germain&ndash;Lagrange plate equation</div>'
'<p class="block-prose">$$D\\,\\nabla^4 w \\;+\\; \\rho h\\,\\frac{\\partial^2 w}{\\partial t^2} \\;=\\; 0,'
'\\qquad \\nabla^4 = \\frac{\\partial^4}{\\partial x^4} + 2\\frac{\\partial^4}{\\partial x^2 \\partial y^2}'
' + \\frac{\\partial^4}{\\partial y^4}$$</p></div>',

"""The prize committee noted that the derivation still rested on assumptions it could not
verify. The corpus's own standard requires saying so: <strong>the equation is right and
her 1816 derivation of it was not complete</strong>, and the modern derivation from
three-dimensional elasticity is Kirchhoff's, in 1850.
<span class="tag t-cited">CITED</span> <span class="tag t-open">OPEN</span>""",
]

P4 = [
"""Here is the brick, and it is the reason this chapter exists rather than being a
biography. Take the simply supported square plate. Its modes are
$w_{mn} = \\sin(m\\pi x/a)\\,\\sin(n\\pi y/a)$ and its frequencies go as $m^2 + n^2$.
Two different modes can therefore ring at exactly the same pitch:""",

'<p class="block-prose" style="font-family:ui-monospace,monospace;font-size:.86rem">'
'm&sup2;+n&sup2; = &nbsp;50 &nbsp;&larr;&nbsp; (1,7) and (5,5)<br>'
'm&sup2;+n&sup2; = &nbsp;65 &nbsp;&larr;&nbsp; (1,8) and (4,7)<br>'
'm&sup2;+n&sup2; = &nbsp;85 &nbsp;&larr;&nbsp; (2,9) and (6,7)<br>'
'm&sup2;+n&sup2; = 125 &nbsp;&larr;&nbsp; (2,11) and (5,10)<br>'
'm&sup2;+n&sup2; = 130 &nbsp;&larr;&nbsp; (3,11) and (7,9)'
' &nbsp;<span class="tag t-computed">COMPUTED</span></p>',

"""These are not the trivial pairs $(m,n)$ and $(n,m)$, which the square's symmetry makes
inevitable. $50 = 1^2+7^2 = 5^2+5^2$ is a genuine coincidence of sums of two squares, and
it is a fact about the integers that leaks into a piece of brass.""",

"""When an eigenvalue is degenerate, <em>any</em> combination
$w = \\cos t\\,\\phi_1 + \\sin t\\,\\phi_2$ is a mode at the same frequency. So the plate does
not have <em>a</em> figure at that pitch. It has a one-parameter family of them, and which
one the sand shows depends on where the plate is clamped and where it is bowed.""",

'''<div class="box"><div class="box-label">Why this is in the series</div>
<p class="block-prose">The boundary does not draw the figure. The boundary <em>removes
options</em>, and what is left is the family the constraint could not exclude. This is the
corpus's own claim about form &mdash; <em>ortogênese</em>, form generated under constraint
in the directions the constraint leaves open &mdash; stated on a square of brass in 1816
with a number-theoretic coincidence doing the work at the degenerate pitches.</p>
<p class="block-prose">And it is a threshold, not a scale: nothing about the figure changes
gradually as the bowing point moves. It holds, and then at a degenerate frequency the
whole family becomes available at once. <span class="tag t-shown">SHOWN</span></p></div>''',

"""The corpus reaches this from the other side. <a href="../impa-portal.html">dm&sup3;
Soundworks</a> works the Chladni figures as resonance; <a href="ch-strang.html">Strang</a>
and <a href="ch-faraday.html">Faraday</a> hold the neighbouring rungs. None of them names
the person who wrote the equation. That is the gap this chapter closes.""",
]

build(
 slug="sophie-germain",
 name="Sophie Germain",
 hero_sub="She wrote under a dead student&rsquo;s name so the mathematics would be read, and "
          "gave the corpus the equation under its own Chladni figures &mdash; where a coincidence "
          "between sums of two squares becomes a family of shapes in sand.",
 description="Sophie Germain: the auxiliary-prime method and Case 1 of Fermat, the "
             "Germain-Lagrange plate equation, and why degenerate modes give Chladni figures "
             "as a family rather than a picture.",
 parts=[
   ("Part I &middot; Le Blanc", "The name she borrowed, and the one she gave back", P1),
   ("Part II &middot; The First Brick", "$p$ and $2p+1$", P2),
   ("Part III &middot; The Second Brick", "Sand on a brass plate", P3),
   (None, "What the degeneracy pays for", P4),
 ],
 place_rows=[
   ("C", "the boundary condition &mdash; a square, clamped", "compression: the constraint that issues the family"),
   ("K", "the driving frequency raised toward a degenerate eigenvalue", "approach to $\\kappa^*$"),
   ("F", "degeneracy: one pitch, a one-parameter family of nodal curves",
        "the fold &mdash; threshold, not scale <span class=\"tag t-shown\">SHOWN</span>"),
   ("U", "the figure the sand actually settles into, selected by where the bow touches",
        "unfolding onto a branch"),
 ],
 refs=[
  "S. Germain, <em>Recherches sur la th&eacute;orie des surfaces &eacute;lastiques</em>, Paris, 1821.",
  "A.-M. Legendre, <em>Th&eacute;orie des nombres</em>, 2nd ed., 1808 &mdash; supplement, where Germain&rsquo;s theorem first appears in print.",
  "E. F. F. Chladni, <em>Die Akustik</em>, Leipzig, 1802.",
  "G. Kirchhoff, &ldquo;&Uuml;ber das Gleichgewicht und die Bewegung einer elastischen Scheibe&rdquo;, <em>Crelle</em> 40, 1850.",
  "R. Laubenbacher and D. Pengelley, &ldquo;&lsquo;Voici ce que j&rsquo;ai trouv&eacute;&rsquo;: Sophie Germain&rsquo;s grand plan to prove Fermat&rsquo;s Last Theorem&rsquo;&rdquo;, <em>Historia Mathematica</em> 37, 2010 &mdash; the manuscripts, and how much larger her programme was.",
  "L. Bucciarelli and N. Dworsky, <em>Sophie Germain: An Essay in the History of the Theory of Elasticity</em>, Reidel, 1980.",
 ],
 prev=("ch-noether.html", "Emmy Noether"),
 nxt=("ch-strang.html", "Gilbert Strang"),
 verify="book7/ch-sophie-germain-verify.py",
 extra_css=TAGCSS,
)
