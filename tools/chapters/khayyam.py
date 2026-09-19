#!/usr/bin/env python3
"""Book IX -- Omar Khayyam. Gallery of Mathematical Mystics."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figure_chapter import build9

P1 = [
"""Two people are called Omar Khayyam and they are the same person, which is the whole
reason this chapter is in Book IX rather than Book VII. One wrote the
<em>Treatise on Demonstration of Problems of Algebra</em> around 1070 and solved the cubic
by intersecting conics. The other &mdash; or the same one &mdash; is the voice of the
quatrains, the wine and the potter's shop and the bowl they call the sky.""",

"""The corpus's own standard obliges a warning here, and it is a real one.
<strong>The attribution of the Rub&aacute;iy&aacute;t is a mess.</strong> Quatrains
accumulated under his name for centuries; the manuscripts are late; scholars have argued
the authentic core down to a few dozen and up again. FitzGerald's English of 1859 is a
Victorian poem that made him famous in a language he never read. Whether Khayyam was a
Sufi, a sceptic, or a court astronomer who wrote verse to amuse himself, is contested and
this page does not settle it. <span class="tag t-cited">CITED</span>
<span class="tag t-open">OPEN</span>""",

"""What is not contested is that he wrote philosophical treatises on existence and on
being, that he worked as an astronomer for Malik-Shah, and that he built a calendar. The
practice and the metaphysics were not separate departments of his life. That is the test
for this gallery.""",
]

P2 = [
"""Take $x^3 + ax = b$ with $a, b &gt; 0$. Khayyam had no formula &mdash; nobody would for
another four hundred and fifty years &mdash; so he built the root instead of computing it.""",

'''<div class="theorem-box">
  <div class="label">Khayyam&rsquo;s construction, c. 1070</div>
  <div class="stmt">$x^2 = \\sqrt{a}\\,y \\quad \\cap \\quad x^2 + y^2 = \\tfrac{b}{a}x$</div>
  <p style="font-size:.9rem;color:rgba(243,223,160,.8);margin:0">A parabola and a circle.
  Their second intersection has abscissa the real root.</p>
</div>''',

"""It is exact. For $a = 2$, $b = 5$ the intersection sits at $x = 1.328268855669$ and the
real root of $x^3 + 2x - 5$ is $1.328268855669$ &mdash; agreeing to every digit double
precision carries, across every case tested. <span class="tag t-computed">COMPUTED</span>""",

"""And here the chapter joins <a href="ch-hypatia.html">Hypatia</a>'s, five hundred years
earlier and two thousand miles west. She preserved Apollonius; Khayyam used him. The conic
sections are the only curves available to him, and he classifies the cubics by which pair
of conics is needed &mdash; fourteen types, because he has no negative coefficients and must
treat each arrangement separately. <strong>The classification is forced by the constraint,
not chosen.</strong>""",
]

P3 = [
"""Then he says something a modern paper would have to be brave to say.""",

'''<blockquote>
  <p>We have tried to express these roots by algebra but have failed. It may be that those
  who come after us will succeed.</p>
  <span class="attr">Khayyam, on the general algebraic solution of the cubic &middot;
  paraphrase of the standard translation &middot; <span class="tag t-cited">CITED</span></span>
</blockquote>''',

"""He was right, and he was right about the shape of the future too: del Ferro, Tartaglia
and Cardano got there in the 1530s, and <a href="../book7/ch-cardano.html">Cardano</a>'s
chapter in Book VII picks the story up. What matters here is the sentence itself.
<strong>He marked his own result OPEN.</strong> He had a method that worked, he knew its
boundary, he stated the boundary, and he named it as work for other people. That is the
epistemic standard this corpus tries to hold, written in the eleventh century by someone
who had no reason to and did it anyway.""",
]

P4 = [
"""In 1079 he led the reform that produced the Jalali calendar. Its rule puts 8 leap years
in every 33, which makes the mean year $365 + 8/33$ days.""",

'<div class="op-map">\n<table>\n'
'  <tr><th>Rule</th><th>Mean year</th><th>Error against the tropical year</th><th>One day adrift in</th></tr>\n'
'  <tr><td>Jalali, 8/33</td><td class="mono">365.242424242</td><td class="mono">+0.000234 d/yr</td><td class="mono">4&thinsp;269 yr</td></tr>\n'
'  <tr><td>Gregorian, 97/400</td><td class="mono">365.242500000</td><td class="mono">+0.000310 d/yr</td><td class="mono">3&thinsp;226 yr</td></tr>\n'
'  <tr><td>Julian, 1/4</td><td class="mono">365.250000000</td><td class="mono">+0.007810 d/yr</td><td class="mono">128 yr</td></tr>\n'
'</table>\n</div>',

"""Five centuries before Gregory, and better. <span class="tag t-computed">COMPUTED</span>
But the interesting part is not that it wins; it is <em>why</em> it wins, and the reason is
not astronomy.""",

'''<div class="insight-box">
  <div class="label">8/33 is a convergent; 97/400 is not</div>
  <p>The continued fraction of the tropical-year fraction $0.242190$ is
  $[0;4,7,1,3,24,\\ldots]$, and its convergents are
  $\\tfrac14,\\ \\tfrac{7}{29},\\ \\tfrac{8}{33},\\ \\tfrac{31}{128},\\ \\tfrac{752}{3105},\\ldots$
  &mdash; <strong>$8/33$ is one of them and $97/400$ is not.</strong></p>
  <p>A convergent is a best rational approximation: no fraction with a smaller denominator
  comes closer. The Jalali rule is not merely accurate, it is optimal for a cycle that
  short. And $31/128$ is better still, with a denominator smaller than $400$ &mdash; so the
  Gregorian rule is not even the best available at its own size.
  <span class="tag t-computed">COMPUTED</span></p>
</div>''',

"""Whether Khayyam's committee arrived at $8/33$ through the continued-fraction algorithm
or through observation and arithmetic is not known to this page, and it would be an
invention to say. <span class="tag t-open">OPEN</span> What is known is which number they
chose.""",
]

P5 = [
"""So the two halves close. The quatrains circle one figure over and over: the wheel, the
bowl inverted overhead, the turning that returns to where it began and finds the drinker
gone. Whether that is Sufi doctrine or a sceptic's consolation is the contested question
this page leaves open.""",

"""What is not contested is the shape. A man who spent his working life on curves that
close and cycles that repeat &mdash; the circle cutting the parabola, the thirty-three-year
wheel of intercalation &mdash; wrote verse about a wheel that turns and does not give
anything back. The mathematics and the metaphysics are the same figure seen twice, and he
did not have two vocabularies for it because in the eleventh century nobody did.""",
]

build9(
 slug="khayyam",
 name="Omar Khayyam",
 years="1048&ndash;1131 &middot; Nishapur &middot; Astronomer to Malik-Shah",
 keyword="al-jabr",
 subtitle="The Cubic, the Calendar, and the Wheel",
 description="Omar Khayyam: the cubic solved by intersecting a parabola with a circle, the "
             "Jalali calendar's 8/33 rule as a continued-fraction convergent, and a result "
             "its author marked open in 1070. Gallery of Mathematical Mystics, Omega Point.",
 crumb="Conics &middot; Jalali calendar &middot; Rub&aacute;iy&aacute;t &middot; 1048&ndash;1131",
 optags=[("genesis", "C &middot; Two Conics"), ("logos", "K &middot; 8/33"),
         ("resonance", "U &middot; The Wheel")],
 accent="#7a5ba8",
 parts=[
   (None, P1),
   ("The root he could not compute, so he built it", P2),
   ("The sentence a modern paper would have to be brave to write", P3),
   ("Thirty-three years", P4),
   ("The wheel", P5),
 ],
 place_rows=[
   ("C", "no negative coefficients &mdash; fourteen types, forced", "compression: the constraint that issues the classification"),
   ("K", "the circle swept until it meets the parabola again", "approach to the crossing"),
   ("F", "the second intersection &mdash; the root, constructed not computed",
        'the fold <span class="tag t-shown">SHOWN</span>'),
   ("U", "$8/33$ &mdash; the cycle that closes, and closes best",
        'a convergent <span class="tag t-shown">SHOWN</span>'),
 ],
 refs=[
  "&lsquo;Umar al-Khayy&#257;m&#299;, <em>Ris&#257;la f&#299; l-bar&#257;h&#299;n &lsquo;al&#257; mas&#257;&rsquo;il al-jabr wa-l-muq&#257;bala</em> (Treatise on Demonstration of Problems of Algebra), c. 1070.",
  "R. Rashed and B. Vahabzadeh, <em>Omar Khayyam, the Mathematician</em>, Bibliotheca Persica, 2000 &mdash; the critical edition and translation.",
  "D. S. Kasir, <em>The Algebra of Omar Khayyam</em>, Columbia, 1931.",
  "E. S. Kennedy, &ldquo;The Persian Calendar&rdquo;, <em>Vistas in Astronomy</em> 31, 1988.",
  "E. FitzGerald, <em>Rub&aacute;iy&aacute;t of Omar Khayy&aacute;m</em>, 1859 &mdash; a Victorian poem, and the reason for the fame.",
  "A. Dashti, <em>In Search of Omar Khayyam</em>, trans. L. P. Elwell-Sutton, Allen &amp; Unwin, 1971 &mdash; on how few quatrains survive attribution.",
 ],
 prev=("ch-al-kindi.html", "Al-Kindi"),
 nxt=("ch-rumi.html", "Rumi"),
 verify="omega/ch-khayyam-verify.py",
)
