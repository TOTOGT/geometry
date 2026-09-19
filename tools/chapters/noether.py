#!/usr/bin/env python3
"""Book VII -- Emmy Noether. Replaces the stub."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figure_chapter import build, TAGCSS

P1 = [
"""Emmy Noether lectured at G&ouml;ttingen for four years under Hilbert's name because the
faculty would not habilitate a woman, and Hilbert told the senate that he did not see
how a candidate's sex was an argument against her, since the senate was not a bathhouse.
She was paid nothing until 1923. In 1933 she was dismissed by letter, taught for a while
from her flat, and went to Bryn Mawr, where she died in 1935 at fifty-three.
<span class="tag t-cited">CITED</span>""",

"""The reason she is in this gallery is not that biography. It is that <strong>two of the
things this corpus does every day are hers</strong>, and one of them does not survive the
move into contact geometry &mdash; which is more interesting than if it did.""",
]

P2 = [
"""The 1918 paper, <em>Invariante Variationsprobleme</em>, contains two theorems. The first
is the one everyone quotes: to every continuous symmetry of an action there corresponds a
conserved quantity. Time-translation gives energy. Space-translation gives momentum.
Rotation gives angular momentum. It is the reason a physicist, asked why energy is
conserved, can answer with a statement about time rather than a statement about energy.""",

"""The second theorem &mdash; that a symmetry depending on arbitrary functions produces
identities among the equations rather than conservation laws &mdash; is the one that turned
out to govern gauge theory, and was largely ignored for forty years. She wrote it to settle
a problem Hilbert and Klein had run into in general relativity, where energy conservation
behaves strangely. It does behave strangely, and her second theorem says exactly why.""",
]

P3 = [
"""Here is the part that matters for this corpus, and it is a limitation, not a triumph.""",

"""dm&sup3; is not symplectic. It is <em>contact</em>: an odd-dimensional manifold with
$\\alpha = dz - p\\,dq$, and a contact Hamiltonian flow that does not preserve a symplectic
form. Contact systems dissipate; that is what they are for. <strong>Noether's theorem in
its symplectic form therefore does not transfer.</strong> Energy is not conserved along a
contact flow, and no amount of symmetry will make it so.""",

"""What happens instead is sharper than &ldquo;it fails&rdquo;. Take the contact Hamiltonian
$H(q,p,z) = \\tfrac12(p^2+q^2) + \\beta z$ with the standard contact equations""",

'<div class="box"><div class="box-label">contact Hamiltonian flow</div>'
'<p class="block-prose">$$\\dot q = \\frac{\\partial H}{\\partial p},\\qquad'
'\\dot p = -\\frac{\\partial H}{\\partial q} - p\\,\\frac{\\partial H}{\\partial z},\\qquad'
'\\dot z = p\\,\\frac{\\partial H}{\\partial p} - H$$</p></div>',

"""which for this $H$ is the damped oscillator $\\ddot q + \\beta\\dot q + q = 0$. Compute
$\\dot H$ along the flow and the $z$-coupling gives""",

'<div class="box"><div class="box-label">the conformal conservation law</div>'
'<p class="block-prose">$$\\frac{dH}{dt} = -H\\,\\frac{\\partial H}{\\partial z} = -\\beta H'
'\\qquad\\Longrightarrow\\qquad H(t) = H(0)\\,e^{-\\beta t}$$</p>'
'<p class="block-prose">so $H e^{\\beta t}$ is <em>exactly</em> conserved, to $10^{-14}$ '
'relative over two periods under RK4. <span class="tag t-computed">COMPUTED</span></p></div>',

"""<strong>The conserved quantity did not disappear. It became conformally conserved.</strong>
Noether's correspondence survives the move from symplectic to contact, but the thing it
produces is an invariant up to an exponential factor rather than a constant, and the
exponent is the dissipation. That is not a footnote to her theorem; it is the reason a
dissipative system can still be said to have a symmetry at all.""",
]

P4 = [
"""And the damping itself has a threshold, which is the corpus's own shape appearing
where it was not planted.""",

"""The characteristic roots of $\\ddot q + \\beta \\dot q + q = 0$ are
$\\lambda_\\pm = \\tfrac12(-\\beta \\pm \\sqrt{\\beta^2 - 4})$. For $\\beta < 2$ they are a
complex pair with real part exactly $-\\beta/2$: the system rings while it decays. At
$\\beta = 2$ the two roots <em>collide</em> at $-1$. Past it they are real and distinct,
and the slower one climbs back toward zero &mdash; at $\\beta = 4$ the roots are
$-0.2679$ and $-3.7321$, so the <em>most damped</em> setting of the parameter gives the
<em>slowest</em> return. <span class="tag t-computed">COMPUTED</span>""",

'''<div class="box"><div class="box-label">A correction, recorded</div>
<p class="block-prose">An earlier draft of this chapter asserted that $\\mu_{\\max} = -\\beta/2$
throughout, and so that $\\beta = 4$ would give $\\mu_{\\max} = -2$ &mdash; the corpus's own
canonical value. <strong>It does not.</strong> $-\\beta/2$ is the real part only while the
roots are complex, that is only for $\\beta &lt; 2$. The claim was dropped before the page was
written rather than after, and it is recorded here because a number that flatters the
framework is exactly the kind that gets kept without checking.
<span class="tag t-open">OPEN</span></p></div>''',

"""So $\\beta = 2$ is a fold in the parameter, not a scale in it. Nothing about the decay
gets gradually less oscillatory; it oscillates, and then at one value it stops, and the
eigenvalues that were a conjugate pair become two real numbers going opposite ways.""",
]

P5 = [
"""Her other brick is quieter and this corpus leans on it harder. The ascending chain
condition &mdash; the definition that makes a ring <em>Noetherian</em> &mdash; is what lets
finiteness arguments run in commutative algebra at all, and it is a hypothesis in most of
what <a href="ch-grothendieck.html">Grothendieck</a> built on top. The K-group that chapter
is about needs the categories to be well-behaved, and &ldquo;well-behaved&rdquo; is, over
and over, &ldquo;Noetherian&rdquo;.""",

"""She also gave the modern statement of the isomorphism theorems, and the homological
reading of Betti numbers as ranks of groups rather than numbers &mdash; which is why one
says <em>homology group</em> and not <em>homology number</em>. Alexandroff said she taught
the topologists what they had been computing. <span class="tag t-cited">CITED</span>""",
]

build(
 slug="noether",
 name="Emmy Noether",
 hero_sub="Symmetry gives a conserved quantity &mdash; and dm&sup3; is contact, not symplectic, "
          "so the quantity is conserved only up to an exponential. That factor is the dissipation, "
          "and this chapter is where the corpus admits it.",
 description="Emmy Noether: the two 1918 theorems, why the symplectic form of the first does "
             "not transfer to a contact flow, the conformal conservation law H(t)=H(0)e^{-beta t}, "
             "and the eigenvalue collision at beta=2.",
 parts=[
   ("Part I &middot; G&ouml;ttingen", "Lecturing under another name", P1),
   ("Part II &middot; The Theorem", "Two theorems, one of them quoted", P2),
   ("Part III &middot; What Breaks", "Contact is not symplectic, and that is the point", P3),
   (None, "A threshold in the damping", P4),
   ("Part IV &middot; The Quiet Brick", "The ascending chain condition", P5),
 ],
 place_rows=[
   ("C", "the action functional &mdash; a symmetry declared", "compression: what is held fixed"),
   ("K", "$\\beta$ raised toward 2, the roots approaching each other", "approach to $\\kappa^*$"),
   ("F", "$\\beta = 2$: the conjugate pair collides and splits into two reals",
        "the fold &mdash; threshold, not scale <span class=\"tag t-shown\">SHOWN</span>"),
   ("U", "$He^{\\beta t}$ &mdash; the invariant that survives the dissipation",
        "the conserved object of a contact flow <span class=\"tag t-computed\">COMPUTED</span>"),
 ],
 refs=[
  "E. Noether, &ldquo;Invariante Variationsprobleme&rdquo;, <em>Nachr. d. K&ouml;nig. Gesellsch. d. Wiss. zu G&ouml;ttingen</em>, 1918, 235&ndash;257.",
  "E. Noether, &ldquo;Idealtheorie in Ringbereichen&rdquo;, <em>Math. Ann.</em> 83, 1921 &mdash; the ascending chain condition.",
  "Y. Kosmann-Schwarzbach, <em>The Noether Theorems</em>, Springer, 2011 &mdash; including the neglect of the second theorem.",
  "A. Bravetti, H. Cruz and D. Tapias, &ldquo;Contact Hamiltonian mechanics&rdquo;, <em>Ann. Phys.</em> 376, 2017 &mdash; the contact equations used above.",
  "A. Bravetti, &ldquo;Contact Hamiltonian dynamics: the concept and its use&rdquo;, <em>Entropy</em> 19, 2017.",
  "P. Alexandroff, address in memory of Emmy Noether, Moscow Mathematical Society, 1935.",
 ],
 prev=("ch-grothendieck.html", "Alexander Grothendieck"),
 nxt=("ch-sophie-germain.html", "Sophie Germain"),
 verify="book7/ch-noether-verify.py",
 extra_css=TAGCSS,
)
