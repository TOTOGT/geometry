#!/usr/bin/env python3
"""Book VII -- Victora & Nussenzweig, germinal centres. Replaces the stub."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figure_chapter import build, TAGCSS

P1 = [
'''<div class="box"><div class="box-label">Another title correction</div>
<p class="block-prose">The stub this page replaces was titled <strong>Victor Nussenzweig</strong>
&mdash; the malaria immunologist at NYU, who with Ruth Nussenzweig developed the
circumsporozoite work behind the RTS,S vaccine. The Book VII index card cites
<em>Victora &amp; Nussenzweig, 2012, review in Cell</em>: that is <strong>Gabriel Victora
and Michel Nussenzweig</strong> at Rockefeller, on germinal centres. Michel is Victor and
Ruth's son. The index card was right; the stub's title named the wrong Nussenzweig.
<span class="tag t-cited">CITED</span></p></div>''',

"""A germinal centre is a structure that appears in a lymph node days after an infection,
runs for a few weeks, and dissolves. Inside it, B cells deliberately mutate the genes
encoding their own antigen receptor, at a rate about a million times the background &mdash;
roughly $10^{-3}$ per base pair per division &mdash; and are then killed unless the mutation
helped.""",

"""<strong>It is directed evolution, run inside a body, on a timescale of days.</strong>
The output is antibody whose affinity has risen by four to five orders of magnitude.""",
]

P2 = [
"""The question Victora and Nussenzweig settled is how the selection step works, and the
answer is not the obvious one.""",

"""The obvious mechanism would be direct: a B cell whose receptor binds antigen better
survives because it binds antigen better. What the two-photon imaging and the
photoactivatable-GFP experiments showed is that the competition is <em>indirect</em>. A B
cell in the light zone captures antigen from follicular dendritic cells, processes it, and
presents it to a T follicular helper cell. <strong>T-cell help is the limiting resource,
and it is allocated in proportion to how much antigen a B cell can present.</strong>""",

'''<div class="box"><div class="box-label">What that buys</div>
<p class="block-prose">Affinity is converted into a <em>presented quantity</em>, and the
selection acts on that. The cells are not compared against a fixed standard; they are
compared against each other, for a supply of help that does not grow. It is a relative
criterion, and it moves as the population improves.</p></div>''',

"""Cells that win help return to the dark zone, divide, mutate again, and come back. The
cyclic re-entry model, proposed decades earlier, was confirmed by photoactivating cells in
one zone and finding them in the other. <span class="tag t-cited">CITED</span>""",
]

P3 = [
"""The arithmetic of the whole process is a compounding, and it is tight.""",

'<div class="box"><div class="box-label">what each round has to deliver</div>'
'<p class="block-prose" style="font-family:ui-monospace,monospace;font-size:.86rem;line-height:1.9">'
'10<sup>6</sup> &rarr; 10<sup>11</sup> L/mol is 10<sup>5</sup>-fold, so<br>'
'&nbsp;5 rounds &nbsp;&rarr;&nbsp; 1.000 dex/round &nbsp;(10.00&times;)<br>'
'&nbsp;6 rounds &nbsp;&rarr;&nbsp; 0.833 dex/round &nbsp;(6.81&times;)<br>'
'&nbsp;8 rounds &nbsp;&rarr;&nbsp; 0.625 dex/round &nbsp;(4.22&times;)<br>'
'10 rounds &nbsp;&rarr;&nbsp; 0.500 dex/round &nbsp;(3.16&times;)'
' &nbsp;<span class="tag t-computed">COMPUTED</span></p></div>',

"""A toy model &mdash; mutate log-affinity by a Gaussian of $0.30$ dex, keep the top ten per
cent, expand, repeat &mdash; reaches $5.89$ dex in ten rounds. That is
$7.8\\times10^{5}$-fold, against an observed $10^{5}$.""",

'''<div class="box"><div class="box-label">The model overshoots, and that is the finding</div>
<p class="block-prose">A toy selection scheme with no biology in it beats the real germinal
centre by most of an order of magnitude. <strong>So something in the real system is holding
it back</strong> &mdash; and the candidates are all interesting: affinity has a ceiling set
by diffusion, most mutations destroy the receptor outright rather than degrading it
gently, the selection is far less than top-ten-per-cent stringent, and the antigen supply
is itself being consumed.</p>
<p class="block-prose">This page does not claim to know which. It claims that the gap
exists and is the right thing to ask about. <span class="tag t-open">OPEN</span></p></div>''',

"""An earlier draft of this chapter went further and claimed an <em>optimal</em> mutation
rate &mdash; too little and nothing improves, too much and the receptors are destroyed. The
model written to show it was monotone: every increase in mutation size improved the
outcome, up to sizes that are biologically absurd. <strong>The claim was dropped rather
than the model tuned until it produced one.</strong> The trade-off is real in the
literature; it is not demonstrated here. <span class="tag t-open">OPEN</span>""",
]

P4 = [
"""The index card for this chapter proposes that each selection round is a step of the
corpus's n-bonacci ladder, converging on $\\tau = 2$. <strong>This page does not assert
that.</strong> The germinal centre's per-round gain is set by mutation size and selection
stringency, both measurable, and nothing measured here produces a recurrence. Recording the
conjecture as a conjecture is the most this chapter can honestly do with it.
<span class="tag t-open">OPEN</span>""",

"""What it can assert is the shape, and the shape is the one this gallery keeps finding.
A blind generator, a constraint that removes almost everything, and iteration &mdash; and
what comes out is not designed but is also not arbitrary, because at every round the
constraint left only a few directions open.""",

"""<a href="ch-klein-thymus.html">The thymus</a> does this once, destructively, to build a
repertoire that will not attack you. The germinal centre does it repeatedly, constructively,
to build one antibody that will. Same operator, opposite sign, and the two organs are the
only places in the body where a cell's own genome is deliberately damaged as part of normal
function.""",
]

P5 = [
"""And where it is taught:""",

'<div class="op-map" style="margin:1.4rem 0">\n<table>\n'
'  <tr><th>Text</th><th>Where</th></tr>\n'
'  <tr><td><em>Janeway&rsquo;s Immunobiology</em>, Murphy &amp; Weaver</td>'
'<td>Germinal centre dynamics and affinity maturation &mdash; the intravital imaging and the '
'cyclic re-entry model of B cells between light and dark zones</td></tr>\n'
'  <tr><td><em>Kuby Immunology</em>, Punt <em>et al.</em></td>'
'<td>B-cell activation, differentiation and memory; germinal centres, Ch. 7 and 10 '
'depending on edition</td></tr>\n'
'  <tr><td><em>Annual Review of Immunology</em></td>'
'<td>Victora &amp; Nussenzweig, &ldquo;Germinal centers&rdquo;, vol. 30, 2012 &mdash; the '
'review this chapter is built on</td></tr>\n'
'</table>\n</div>',

'''<div class="box"><div class="box-label">Reading the primary sources</div>
<p class="block-prose"><strong>&ldquo;Victora-Nussenzweig&rdquo; names two laboratories, not a
book.</strong> The 2012 <em>Annual Review of Immunology</em> article is the consolidation
(PMID 22224772); the 2010 <em>Cell</em> paper is the experiment. Rockefeller deposits its
authors&rsquo; work in its Digital Commons and the primary papers are indexed in PubMed
Central, which is the route in if a library portal is not to hand.</p></div>''',

"""The 2010 <em>Cell</em> paper is eighteen months older than the review, and the review is
in the textbook chapter. <strong>Cyclic re-entry had been a model since the 1990s and an
argument for as long</strong>; photoactivating a cell in one zone and finding it in the
other is what ended the argument, and the speed of the passage into teaching is the
measure of how decisive the experiment was.""",
]

build(
 slug="victora-nussenzweig",
 name="Victora &amp; Nussenzweig",
 hero_sub="B cells mutate their own receptor genes a million times faster than background and "
          "are killed unless it helped. The selection is not on affinity directly &mdash; it is on "
          "how much antigen you can show a T cell that has only so much help to give.",
 description="Gabriel Victora and Michel Nussenzweig on germinal centre dynamics: cyclic "
             "re-entry, T follicular helper cells as the limiting resource, and the compounding "
             "arithmetic of 10^6 to 10^11 affinity maturation.",
 parts=[
   ("Part I &middot; Rockefeller, 2012", "Directed evolution, inside a body", P1),
   ("Part II &middot; The Indirect Criterion", "Help is what is scarce", P2),
   ("Part III &middot; The Arithmetic", "Five orders of magnitude, a few rounds", P3),
   ("Part IV &middot; What This Page Will Not Claim", "Two conjectures, marked", P4),
   ("Part V &middot; Placement", "Where this is taught", P5),
 ],
 place_rows=[
   ("C", "somatic hypermutation &mdash; a blind generator at $10^{-3}$/bp/division",
        "compression: variation, produced without direction"),
   ("K", "antigen captured, processed, presented &mdash; affinity converted to a quantity",
        "the quantity driven toward the selection threshold"),
   ("F", "T follicular helper cells, finite &mdash; the cut is relative and moves",
        "the fold <span class=\"tag t-cited\">CITED</span>"),
   ("U", "return to the dark zone, divide, mutate, come back",
        "cyclic re-entry &mdash; the branch re-entering the chain"),
 ],
 refs=[
  "G. D. Victora and M. C. Nussenzweig, &ldquo;Germinal centers&rdquo;, <em>Annu. Rev. Immunol.</em> 30, 2012, 429&ndash;457. &middot; doi <a href=\"https://doi.org/10.1146/annurev-immunol-020711-075032\">10.1146/annurev-immunol-020711-075032</a> &middot; PMID 22224772.",
  "G. D. Victora <em>et al.</em>, &ldquo;Germinal center dynamics revealed by multiphoton microscopy with a photoactivatable fluorescent reporter&rdquo;, <em>Cell</em> 143, 2010, 592&ndash;605.",
  "A. D. Gitlin, Z. Shulman and M. C. Nussenzweig, &ldquo;Clonal selection in the germinal centre by regulated proliferation and hypermutation&rdquo;, <em>Nature</em> 509, 2014.",
  "C. D. C. Allen, T. Okada and J. G. Cyster, &ldquo;Germinal-center organization and cellular dynamics&rdquo;, <em>Immunity</em> 27, 2007.",
  "K. Murphy and C. Weaver, <em>Janeway&rsquo;s Immunobiology</em>, 10th ed., Garland &mdash; germinal centre dynamics and affinity maturation.",
  "J. Punt <em>et al.</em>, <em>Kuby Immunology</em>, 8th ed., Macmillan &mdash; B-cell activation, differentiation and memory.",
  "M. Meyer-Hermann <em>et al.</em>, &ldquo;A theory of germinal center B cell selection, division, and exit&rdquo;, <em>Cell Reports</em> 2, 2012 &mdash; for the modelling this page's toy scheme is a crude shadow of.",
 ],
 prev=("ch-klein-thymus.html", "Ludger Klein"),
 nxt=("ch-metchnikoff.html", "&Eacute;lie Metchnikoff"),
 verify="book7/ch-victora-nussenzweig-verify.py",
 extra_css=TAGCSS,
)
