#!/usr/bin/env python3
"""Book VII -- Katherine Johnson. Replaces the stub."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figure_chapter import build, TAGCSS

P1 = [
"""She worked in West Area Computing at Langley, a segregated pool of Black women employed
as human computers. She asked to attend the editorial meetings where the engineers argued
about the work she had done, was told women did not go, and asked whether there was a law
against it. There was not, and she went.""",

"""In 1960 her name went on <em>NASA Technical Note D-233</em>, with T. H. Skopinski:
<em>Determination of Azimuth Angle at Burnout for Placing a Satellite Over a Selected Earth
Position</em>. It was the first report out of her division to carry a woman's name as
author. <span class="tag t-cited">CITED</span> That report is the brick, and this chapter is
about what is in it rather than about the film.""",
]

P2 = [
"""The question it answers is concrete. You are at latitude $\\varphi$. You want an orbit of
inclination $i$. Which way do you point?""",

'<div class="box"><div class="box-label">the launch azimuth</div>'
'<p class="block-prose" style="text-align:center;font-size:1.2rem">'
'$$\\sin\\beta = \\frac{\\cos i}{\\cos\\varphi}$$</p>'
'<p class="block-prose">$\\beta$ measured clockwise from north. Spherical trigonometry: the '
'launch site, the ascending node, and the point of highest latitude form a right spherical '
'triangle, and this is its rule.</p></div>',

"""Cape Canaveral sits at $28.47°$N. For Friendship 7's orbit, $i = 32.5°$, the formula
gives an inertial azimuth of $73.621°$. Then subtract what the Earth is already giving you
&mdash; the pad is moving east at $465.1\\cos\\varphi = 409$ m/s &mdash; and the azimuth to
fly is""",

'<p class="block-prose" style="font-family:ui-monospace,monospace;font-size:.88rem">'
'burnout speed 7400 m/s &nbsp;&rarr;&nbsp; 72.678&deg;<br>'
'burnout speed 7600 m/s &nbsp;&rarr;&nbsp; 72.704&deg;<br>'
'burnout speed 7800 m/s &nbsp;&rarr;&nbsp; 72.729&deg;<br>'
'<b>Mercury-Atlas 6, as flown &nbsp;&rarr;&nbsp; 72.6&deg;</b>'
' &nbsp;<span class="tag t-computed">COMPUTED</span></p>',

"""Within a tenth of a degree, and almost independent of the burnout speed. The correction
is small and it is not optional: leave it out and you are a degree off, which at orbital
distances is a different ocean.""",
]

P3 = [
"""The formula has a boundary, and it is absolute.""",

'''<div class="box"><div class="box-label">the hard floor</div>
<p class="block-prose">$\\sin\\beta \\leq 1$ forces $\\cos i \\leq \\cos\\varphi$, so
<strong>$|i| \\geq |\\varphi|$</strong>. From the Cape you can reach inclination
$28.47°$ &mdash; due east, $\\beta = 90°$ &mdash; and nothing lower. Not
inefficiently, not expensively. There is no azimuth.</p>
<p class="block-prose" style="font-family:ui-monospace,monospace;font-size:.85rem">
i = 28.47&deg; &nbsp;&rarr;&nbsp; sin &beta; = 1.000000 &nbsp; the only solution<br>
i = 28.00&deg; &nbsp;&rarr;&nbsp; sin &beta; = 1.004415 &nbsp; <b>no solution</b><br>
i = 25.00&deg; &nbsp;&rarr;&nbsp; sin &beta; = 1.030988 &nbsp; <b>no solution</b><br>
i = 20.00&deg; &nbsp;&rarr;&nbsp; sin &beta; = 1.068966 &nbsp; <b>no solution</b>
&nbsp;<span class="tag t-computed">COMPUTED</span></p></div>''',

"""This is the corpus's own shape in the plainest form it takes anywhere in this gallery.
The launch azimuth is not chosen. <strong>The latitude and the desired inclination leave
exactly one option, or none</strong>, and which of those it is changes at a point rather
than gradually. A plane change in orbit costs propellant proportional to
$2v\\sin(\\Delta i/2)$, which is why the constraint is worth this much arithmetic: for a
$5°$ change at orbital speed, roughly $680$ m/s &mdash; more than most upper stages have.""",
]

P4 = [
"""The part of the story that belongs in a corpus about verification is the part usually
told as a compliment.""",

"""Before Friendship 7, the trajectory was computed by an IBM 7090 running the new
orbital-mechanics code. Glenn would not fly on it. The request, as it reached her, was to
<em>get the girl to check the numbers</em> &mdash; and what that meant in practice was that
she recomputed the trajectory by hand, on a desk calculator, over days, to see whether the
machine agreed with a method anyone could follow.""",

'''<div class="box"><div class="box-label">The standard, stated in 1962</div>
<p class="block-prose">A new tool produced a result nobody could yet audit. The result was
probably right. It was not <em>checked</em>, and the distinction mattered enough that a
flight waited on it.</p>
<p class="block-prose">This corpus writes a verify script beside every chapter for the same
reason, and it is worth saying plainly that the practice is not new and was not invented
here. <span class="tag t-shown">SHOWN</span></p></div>''',

"""She also worked the rendezvous problem &mdash; two vehicles in different orbits made to
arrive at the same place at the same moment &mdash; and the Apollo lunar-module return,
where the same question is asked with no margin at all. The Presidential Medal of Freedom
came in 2015. She died in 2020, a hundred and one years old.""",
]

build(
 slug="katherine-johnson",
 name="Katherine Johnson",
 hero_sub="Given a latitude and a desired inclination, there is exactly one launch azimuth &mdash; "
          "or none. And before Friendship 7 flew, a trajectory a computer had produced waited on "
          "a hand recomputation.",
 description="Katherine Johnson: NASA TN D-233 and the launch azimuth equation sin(beta) = "
             "cos(i)/cos(phi), verified against Friendship 7's 72.6 degrees, and the hard floor "
             "that inclination cannot fall below launch latitude.",
 parts=[
   ("Part I &middot; West Area Computing", "Whether there was a law against it", P1),
   ("Part II &middot; TN D-233", "Which way do you point?", P2),
   ("Part III &middot; The Floor", "One option, or none", P3),
   ("Part IV &middot; The Check", "Get the girl to check the numbers", P4),
 ],
 place_rows=[
   ("C", "the launch site &mdash; a latitude, fixed and not negotiable",
        "compression: the constraint"),
   ("K", "the desired inclination brought down toward $\\varphi$", "approach to the boundary"),
   ("F", "$i = \\varphi$: $\\sin\\beta = 1$, and below it there is no azimuth at all",
        "the fold &mdash; threshold, not scale <span class=\"tag t-shown\">SHOWN</span>"),
   ("U", "$\\beta = 72.6°$ &mdash; the one heading the constraint leaves",
        "the branch, verified against the flight <span class=\"tag t-computed\">COMPUTED</span>"),
 ],
 refs=[
  "T. H. Skopinski and K. G. Johnson, <em>Determination of Azimuth Angle at Burnout for Placing a Satellite Over a Selected Earth Position</em>, NASA TN D-233, Langley, 1960.",
  "K. G. Johnson and J. C. Young, <em>Two Approaches for Obtaining the Braking Ellipse for Return from a Lunar Mission</em>, NASA TN D-3970, 1967.",
  "NASA, <em>Results of the First United States Manned Orbital Space Flight, February 20, 1962</em>, Manned Spacecraft Center &mdash; for the flown trajectory parameters.",
  "M. L. Shetterly, <em>Hidden Figures</em>, William Morrow, 2016.",
  "R. R. Bate, D. D. Mueller and J. E. White, <em>Fundamentals of Astrodynamics</em>, Dover, 1971 &mdash; chapter 2 for the spherical-triangle derivation.",
 ],
 prev=("ch-dyson.html", "Freeman Dyson"),
 nxt=("ch-hamilton.html", "William Rowan Hamilton"),
 verify="book7/ch-katherine-johnson-verify.py",
 extra_css=TAGCSS,
)
