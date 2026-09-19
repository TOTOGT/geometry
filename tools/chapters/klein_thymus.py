#!/usr/bin/env python3
"""Book VII -- Ludger Klein, thymic selection. Replaces the stub."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figure_chapter import build, TAGCSS

P1 = [
'''<div class="box"><div class="box-label">A correction to this chapter&rsquo;s own title</div>
<p class="block-prose">The stub this page replaces was titled <strong>Jan Klein</strong>, while
the Book VII index card cited <em>Ludger Klein et al., 2014, Nature Reviews Immunology</em>.
Those are two different immunologists. Jan Klein (1936&ndash;) worked on the evolution of the
MHC and trans-species polymorphism. Ludger Klein, in Munich, wrote the 2014 review on
thymic selection that the index card names. <strong>The index card was right and the stub's
title was wrong</strong>, and this chapter is Ludger Klein's.
<span class="tag t-cited">CITED</span></p></div>''',

"""The thymus has a problem with no obvious solution. It must produce T cells that
recognise <em>foreign</em> peptide presented on <em>self</em> MHC &mdash; so the receptor has
to bind self-MHC, or it will never see anything. But a receptor that binds self-MHC bearing
self-peptide <em>too well</em> is an autoimmune disease waiting to happen.""",

"""<strong>The same molecule is the thing you must recognise and the thing you must not
recognise too well.</strong> There is no way to satisfy that with a filter. It needs a
window.""",
]

P2 = [
"""Which is what the thymus builds. A developing thymocyte carrying a randomly assembled
receptor meets self-peptide&ndash;MHC on cortical epithelium and is read twice:""",

'<div class="box"><div class="box-label">two thresholds, in sequence</div>'
'<p class="block-prose" style="font-family:ui-monospace,monospace;font-size:.86rem;line-height:1.9">'
'binds below &nbsp;lo &nbsp;&rarr;&nbsp; <b>death by neglect</b> &mdash; never receives a survival signal<br>'
'binds between &nbsp;&rarr;&nbsp; <b>positive selection</b> &mdash; matures, leaves<br>'
'binds above &nbsp;hi &nbsp;&rarr;&nbsp; <b>negative selection</b> &mdash; deleted, or diverted to a regulatory fate</p></div>',

"""Roughly <strong>two per cent</strong> of thymocytes complete the passage. The rest die in
place, and the great majority of those die of the first threshold rather than the second
&mdash; neglect, not deletion. <span class="tag t-cited">CITED</span>""",

"""That figure has usually been read as <em>selection is stringent</em>. It is worth reading
instead as a statement about the geometry: <strong>the survivors are the mass of a
distribution between two cuts, and two per cent is what tells you how far apart the cuts
are.</strong>""",
]

P3 = [
"""Take receptor avidity for self-pMHC as a standardised log-scale variable. Then the
surviving fraction is just the mass between the thresholds, and two per cent pins the
window:""",

'<p class="block-prose" style="font-family:ui-monospace,monospace;font-size:.85rem;line-height:1.85">'
'window [1.00, 1.50] &nbsp;&rarr;&nbsp; 9.19&thinsp;%<br>'
'window [1.00, 1.30] &nbsp;&rarr;&nbsp; 6.17&thinsp;%<br>'
'window [1.20, 1.45] &nbsp;&rarr;&nbsp; 4.15&thinsp;%<br>'
'<b>window [1.00, 1.086] &nbsp;&rarr;&nbsp; 2.01&thinsp;%</b>'
' &nbsp;<span class="tag t-computed">COMPUTED</span></p>',

"""<strong>The window is 0.086 standard deviations wide.</strong> Whatever the real
distribution of avidities is &mdash; and it is certainly not a standard normal &mdash; a two
per cent yield through a two-sided cut forces the cuts to be close together, because the
density between them is what survives.""",

'''<div class="box"><div class="box-label">And it is brutally sensitive</div>
<p class="block-prose" style="font-family:ui-monospace,monospace;font-size:.85rem;line-height:1.85">
upper threshold &minus;0.10 sd &nbsp;&rarr;&nbsp; 0.03&thinsp;% survive &nbsp;&mdash;&nbsp; <b>67&times; fewer</b><br>
upper threshold &minus;0.05 sd &nbsp;&rarr;&nbsp; 0.87&thinsp;% &nbsp;&mdash;&nbsp; 0.43&times;<br>
<b>baseline &nbsp;&rarr;&nbsp; 2.01&thinsp;%</b><br>
upper threshold +0.05 sd &nbsp;&rarr;&nbsp; 3.07&thinsp;% &nbsp;&mdash;&nbsp; 1.5&times;<br>
upper threshold +0.10 sd &nbsp;&rarr;&nbsp; 4.09&thinsp;% &nbsp;&mdash;&nbsp; 2.0&times;
&nbsp;<span class="tag t-computed">COMPUTED</span></p>
<p class="block-prose">A tenth of a standard deviation in one direction and the repertoire
collapses; a tenth in the other and twice as many cells escape, carrying receptors that
were supposed to be deleted. <strong>Immunodeficiency and autoimmunity are not opposite
ends of a long scale. They are two sides of one cut</strong>, and the distance between them
is small.</p></div>''',
]

P4 = [
"""The rest of the mechanism is about making the cut in the right place, and the solution
is the part of this biology most worth a corpus's attention.""",

"""A thymocyte in the cortex only ever meets peptides that the thymus happens to express.
A receptor specific for insulin, or for a retinal protein, would never be tested &mdash;
those proteins are not in the thymus. So medullary thymic epithelial cells express them
anyway: driven by AIRE, and by Fezf2, they transcribe thousands of tissue-restricted genes
in a promiscuous, cell-by-cell mosaic, so that a developing T cell walking through the
medulla is shown pieces of organs it will never visit.""",

'''<div class="box"><div class="box-label">Why that is the interesting engineering</div>
<p class="block-prose">The threshold is useless unless the test set covers the space. The
thymus does not make the cut sharper &mdash; it <strong>enlarges what is on the other side
of it</strong>, by manufacturing a representation of the whole body inside one organ.</p>
<p class="block-prose">Mutations in <em>AIRE</em> give APECED, an autoimmune syndrome
attacking several endocrine organs at once. The test set has holes, and the holes are the
disease. <span class="tag t-cited">CITED</span></p></div>''',

"""The dm&sup3; reading is direct, and the index card for this chapter had it: three stages,
survival then positive then negative, are <em>C</em>, <em>K</em>, <em>F</em> &mdash; a
constraint applied, a quantity driven toward a threshold, and a branch taken at it. What
this page adds is that the fold here is <strong>two-sided</strong>, and that the corpus's
usual picture &mdash; one threshold, cross it or do not &mdash; is the special case. A cell
can fail by not reaching the fold at all.""",
]

P5 = [
"""Where this entered the teaching literature, which is the test of whether a finding has
become knowledge rather than a result:""",

'<div class="op-map" style="margin:1.4rem 0">\n<table>\n'
'  <tr><th>Text</th><th>Where</th></tr>\n'
'  <tr><td><em>Janeway&rsquo;s Immunobiology</em>, Murphy &amp; Weaver</td>'
'<td>Thymic selection and central tolerance &mdash; mTEC promiscuous gene expression, AIRE, '
'and the positive/negative selection of the T-cell repertoire</td></tr>\n'
'  <tr><td><em>Kuby Immunology</em>, Punt <em>et al.</em></td>'
'<td>T-cell development and selection in the thymus, Ch. 8</td></tr>\n'
'  <tr><td><em>Annual Review of Immunology</em></td>'
'<td>Klein <em>et al.</em>, antigen presentation and selection in the thymus</td></tr>\n'
'</table>\n</div>',

'''<div class="box"><div class="box-label">Reading the primary sources</div>
<p class="block-prose"><strong>&ldquo;Klein-thymus&rdquo; names a laboratory, not a book.</strong>
There is no textbook by that title; what there is, is a body of papers out of Ludger Klein&rsquo;s
group in Munich and the reviews that consolidated them. The 2014 <em>Nature Reviews
Immunology</em> review is open access at <a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC4757912/">PMC4757912</a>;
the textbook chapters below are where it has been synthesised for teaching, and are the
faster route in for a reader who is not an immunologist.</p></div>''',

"""<strong>The AIRE story is in the textbook chapter, not the further-reading list.</strong>
A mechanism enters a first-year text when the field has stopped arguing about whether it is
true, and central tolerance by promiscuous tissue-antigen expression made that passage
within about a decade of the 2002 <em>Science</em> paper.""",
]

build(
 slug="klein-thymus",
 name="Ludger Klein",
 hero_sub="The same molecule is the thing a T cell must recognise and the thing it must not "
          "recognise too well. That cannot be done with a filter. The thymus builds a window, "
          "and two per cent of cells fit through it.",
 description="Ludger Klein and thymic selection: positive and negative selection as a two-sided "
             "threshold, the 2% survival fraction pinning the window to 0.086 sd, and AIRE-driven "
             "promiscuous gene expression as the enlargement of the test set.",
 parts=[
   ("Part I &middot; The Problem", "Recognise it, but not too well", P1),
   ("Part II &middot; Two Cuts", "Neglect, selection, deletion", P2),
   ("Part III &middot; How Narrow", "Two per cent pins the window", P3),
   ("Part IV &middot; AIRE", "Enlarging what is on the other side", P4),
   ("Part V &middot; Placement", "Where this is taught", P5),
 ],
 place_rows=[
   ("C", "a randomly assembled receptor meeting self-pMHC &mdash; the test applied",
        "compression: the constraint"),
   ("K", "avidity, read against the lower threshold",
        "the quantity driven toward $\\kappa^*$"),
   ("F", "<b>two</b> thresholds, not one &mdash; below is neglect, above is deletion",
        "a two-sided fold <span class=\"tag t-shown\">SHOWN</span>"),
   ("U", "the 2% that leave, and the regulatory lineage diverted rather than killed",
        "the branches <span class=\"tag t-computed\">COMPUTED</span>"),
 ],
 refs=[
  "L. Klein, B. Kyewski, P. M. Allen and K. A. Hogquist, &ldquo;Positive and negative selection of the T cell repertoire: what thymocytes see (and don&rsquo;t see)&rdquo;, <em>Nat. Rev. Immunol.</em> 14, 2014, 377&ndash;391. &middot; doi <a href=\"https://doi.org/10.1038/nri3667\">10.1038/nri3667</a> &middot; PMID 24830344 &middot; open access at <a href=\"https://pmc.ncbi.nlm.nih.gov/articles/PMC4757912/\">PMC4757912</a>.",
  "B. Kyewski and L. Klein, &ldquo;A central role for central tolerance&rdquo;, <em>Annu. Rev. Immunol.</em> 24, 2006.",
  "M. S. Anderson <em>et al.</em>, &ldquo;Projection of an immunological self shadow within the thymus by the Aire protein&rdquo;, <em>Science</em> 298, 2002.",
  "T. Takaba <em>et al.</em>, &ldquo;Fezf2 orchestrates a thymic program of self-antigen expression for immune tolerance&rdquo;, <em>Cell</em> 163, 2015.",
  "K. A. Hogquist and S. C. Jameson, &ldquo;The self-obsession of T cells&rdquo;, <em>Nat. Immunol.</em> 15, 2014.",
  "K. Murphy and C. Weaver, <em>Janeway&rsquo;s Immunobiology</em>, 10th ed., Garland &mdash; thymic selection and central tolerance.",
  "J. Punt <em>et al.</em>, <em>Kuby Immunology</em>, 8th ed., Macmillan &mdash; Ch. 8, T-cell development and selection in the thymus.",
 ],
 prev=("ch-mitchison-kirschner.html", "Mitchison &amp; Kirschner"),
 nxt=("ch-victora-nussenzweig.html", "Victora &amp; Nussenzweig"),
 verify="book7/ch-klein-thymus-verify.py",
 extra_css=TAGCSS,
)
