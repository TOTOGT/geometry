#!/usr/bin/env python3
"""
Build DNLS_D6_ring_draft.pdf.

This generator is kept under version control so the paper's source cannot
evaporate the way the previous draft's did. Regenerate with:

    python3 build_paper.py

Every factual claim about verification status in this document is transcribed
from an actual `lake env lean` run of 2026-08-21. Do not edit those strings
except from a fresh run.
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, KeepTogether)

D = "/usr/share/fonts/truetype/dejavu"
for name, f in [("Serif","DejaVuSerif.ttf"), ("Serif-B","DejaVuSerif-Bold.ttf"),
                ("Serif-I","DejaVuSerif-Italic.ttf"), ("Serif-BI","DejaVuSerif-BoldItalic.ttf"),
                ("Mono","DejaVuSansMono.ttf"), ("Mono-B","DejaVuSansMono-Bold.ttf"),
                ("Sans","DejaVuSans.ttf"), ("Sans-B","DejaVuSans-Bold.ttf")]:
    pdfmetrics.registerFont(TTFont(name, os.path.join(D, f)))
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B",
                              italic="Serif-I", boldItalic="Serif-BI")

INK   = colors.HexColor("#141414")
MUTED = colors.HexColor("#5a5a5a")
RULE  = colors.HexColor("#c8c8c8")
BOX   = colors.HexColor("#f4f4f2")
WARN  = colors.HexColor("#8a2b16")

def S(name, **kw):
    base = dict(name=name, fontName="Serif", fontSize=9, leading=13.2,
                textColor=INK, alignment=TA_JUSTIFY, spaceAfter=6)
    base.update(kw); return ParagraphStyle(**base)

st = {
 "title":  S("title", fontName="Serif-B", fontSize=16, leading=20,
             alignment=TA_CENTER, spaceAfter=4),
 "sub":    S("sub", fontName="Serif-I", fontSize=9.5, leading=13,
             alignment=TA_CENTER, textColor=MUTED, spaceAfter=10),
 "author": S("author", fontSize=10, leading=13, alignment=TA_CENTER, spaceAfter=1),
 "affil":  S("affil", fontSize=7.6, leading=10.5, alignment=TA_CENTER,
             textColor=MUTED, spaceAfter=1),
 "body":   S("body"),
 "abs":    S("abs", fontSize=8.4, leading=12.2),
 "h":      S("h", fontName="Serif-B", fontSize=10.5, leading=14,
             spaceBefore=11, spaceAfter=4),
 "note":   S("note", fontSize=8.2, leading=11.6, textColor=MUTED,
             leftIndent=9, rightIndent=9),
 "warn":   S("warn", fontSize=8.2, leading=11.6, textColor=WARN,
             leftIndent=9, rightIndent=9),
 "mono":   S("mono", fontName="Mono", fontSize=7.4, leading=10.4,
             leftIndent=9, alignment=0),
 "cell":   S("cell", fontSize=7.9, leading=10.8, spaceAfter=0),
 "cellm":  S("cellm", fontName="Mono", fontSize=6.9, leading=9.6, spaceAfter=0),
 "ref":    S("ref", fontSize=7.6, leading=10.4, alignment=0, spaceAfter=2),
 "foot":   S("foot", fontSize=6.8, leading=9, alignment=TA_CENTER, textColor=MUTED),
}

def boxed(flowables, bg=BOX, pad=7):
    t = Table([[flowables]], colWidths=[166*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), bg),
        ("BOX",(0,0),(-1,-1), 0.4, RULE),
        ("LEFTPADDING",(0,0),(-1,-1), pad), ("RIGHTPADDING",(0,0),(-1,-1), pad),
        ("TOPPADDING",(0,0),(-1,-1), pad),  ("BOTTOMPADDING",(0,0),(-1,-1), pad),
    ]))
    return t

def P(t, s="body"): return Paragraph(t, st[s])

story = []
A = story.append

A(P("A Formally Verified D<sub>6</sub>-Equivariant Discrete Nonlinear Schrödinger Ring", "title"))
A(P("Order-dependence, invariant states, an index constraint that is not bridged, "
    "and a verification failure recorded in full", "sub"))
A(P("Pablo Nogueira Grossi", "author"))
A(P("G6 LLC · Newark, New Jersey · ORCID 0009-0000-6496-2186 · g6llc@proton.me", "affil"))
A(P("Draft · 21 August 2026 · not peer-reviewed", "affil"))
A(Spacer(1, 9))

A(boxed([
  P("<b>Abstract.</b> We present a six-site discrete nonlinear Schrödinger (DNLS) ring with "
    "dihedral D<sub>6</sub> symmetry, formalised in Lean 4 with Mathlib. Five results are stated and "
    "kernel-checked: the radial gate commutes with the pointwise cubic nonlinearity but not with "
    "the angular coupling; the sixfold rotation is a symmetry of the coupling; the uniform state is "
    "rotation-invariant; and the uniform state is an eigenvector of the coupling with eigenvalue 2. "
    "The last identifies the uniform hexagonal configuration as the Perron–Frobenius mode of the "
    "cyclic 6-ring, and the coupling's degenerate eigenspaces carry the two-dimensional irreducible "
    "representations of D<sub>6</sub>, which is where symmetry breaking must occur. We separately "
    "record a classical index constraint: a tangent vector field on a sphere has zero-indices "
    "summing to 2, so a D<sub>6</sub>-symmetric flow admitting six vortices must also admit six "
    "saddles. No bridge between the ring and the sphere is established; constructing one is the "
    "principal open problem.", "abs"),
  Spacer(1,4),
  P("Section 7 is not about the model. It records that until 21 August 2026 three of these five "
    "theorems were admitted rather than proved, while the source file's own header asserted that "
    "all five had been kernel-verified — and sets out why no layer of the surrounding "
    "infrastructure could have contradicted that header. Readers with no interest in a six-site "
    "ring may find that section the only part worth their time.", "abs"),
]))
A(Spacer(1, 7))

A(boxed([
  P("<b>Status tags.</b> <b>[PROVED]</b> marks a result whose <font face='Mono' size='7.4'>#print "
    "axioms</font> line is reproduced verbatim in §3 from the run of 21 August 2026. "
    "<b>[CLASSICAL]</b> marks a result cited, not original. <b>[OPEN]</b> marks what is not "
    "established. No claim in this paper is offered as an explanation of any planetary "
    "observation.", "abs")
], bg=colors.HexColor("#eef1f4")))
A(Spacer(1, 4))

# ---------------------------------------------------------------- 1
A(P("1. Motivation, and what is not claimed", "h"))
A(P("Hexagonal planforms recur across pattern-forming systems with planar rotational and "
    "translational symmetry — Rayleigh–Bénard convection, Faraday waves, Turing patterns, Chladni "
    "figures on suitably symmetric plates, and the persistent wavenumber-6 jet at Saturn's north "
    "pole. Equivariant bifurcation theory explains this recurrence [1,2]: hexagonal planforms are "
    "generic outcomes of symmetry breaking in the relevant equivariant class, independently of the "
    "underlying physics."))
A(P("That common explanation is a statement about symmetry, not about mechanism. Saturn's hexagon "
    "is a barotropic instability of a polar jet; a Chladni figure is the nodal set of a Laplacian "
    "eigenmode on an elastic plate. These are different operators with different selection rules. "
    "They share a symmetry group and nothing else, and this paper does not assert otherwise."))
A(P("What follows is deliberately minimal: the smallest D<sub>6</sub>-equivariant discrete model in "
    "which the questions of invariance and of operator order can be posed exactly, together with a "
    "machine-checked account of what that model does and does not settle. Saturn appears here as "
    "motivation only. A six-site ring of real amplitudes is not a rotating shallow-water system, "
    "and no result below should be read as bearing on planetary observation."))

# ---------------------------------------------------------------- 2
A(P("2. The model", "h"))
A(P("State is an amplitude over six angular sextants, θ<sub>k</sub> = kπ/3 for k = 0,…,5, "
    "represented as a function <font face='Mono' size='7.6'>Fin 6 → ℝ</font>. Four operators act "
    "on it."))
A(P("angCoupling v k = v(k−1) + v(k+1) &nbsp;&nbsp;&nbsp;(cyclic; the discrete Laplacian coupling)<br/>"
    "onsite v k = (v k)³ &nbsp;&nbsp;&nbsp;(the λ|ψ|²ψ term, real cube)<br/>"
    "gate v k = v k if k even, 0 if k odd &nbsp;&nbsp;&nbsp;(a 0/1 radial mask, pointwise)<br/>"
    "rot v k = v(k−1) &nbsp;&nbsp;&nbsp;(the generator of the sixfold rotation)", "mono"))
A(Spacer(1,3))
A(P("The uniform or hexagonal configuration is hex c = (c,c,c,c,c,c). Together, angCoupling and "
    "onsite constitute a six-site DNLS ring with real amplitudes: a discrete Laplacian plus a cubic "
    "on-site nonlinearity, closed cyclically [3]."))
A(boxed([P("<b>Note on the formalisation.</b> Operators are defined by explicit pattern match on "
    "<font face='Mono' size='7.4'>Fin 6</font> rather than <font face='Mono' size='7.4'>![…]</font> "
    "vector notation. Mathlib's <font face='Mono' size='7.4'>Matrix.cons_val</font> simplification "
    "lemmas do not chain to index 5 on a <font face='Mono' size='7.4'>Fin 6</font> literal, so the "
    "vector form leaves unsolved goals. See §7, stage one.", "note"),
  Spacer(1,3),
  P("<b>[OPEN]</b> The development defines operators, not a flow. There is no equation of motion in "
    "the formalisation, so questions of stability are not yet well posed within it; see §6.", "note")]))

# ---------------------------------------------------------------- 3
A(P("3. Results [PROVED]", "h"))
A(P("The five theorems below live in <font face='Mono' size='7.6'>SaturnHexagon.lean</font>. The "
    "axiom column is transcribed from this run, on 21 August 2026:"))
A(P("$ cd ~/Desktop/orthogenesis<br/>"
    "$ cp ~/Desktop/geometry/SaturnHexagon.lean /tmp/SH_geom.lean<br/>"
    "$ lake env lean /tmp/SH_geom.lean", "mono"))
A(Spacer(1,4))

rows = [[P("<b>#</b>","cell"), P("<b>statement</b>","cell"), P("<b>reading</b>","cell"),
         P("<b>#print axioms</b>","cell")]]
data = [
 ("T1","gate (onsite v) = onsite (gate v)",
  "The radial gate commutes with the pointwise nonlinearity."),
 ("T2","angCoupling ∘ onsite ≠ onsite ∘ angCoupling",
  "It does not commute with the angular coupling. Order is observable."),
 ("T3","rot (angCoupling v) = angCoupling (rot v)",
  "The sixfold rotation is a symmetry of the coupling: D₆-equivariance."),
 ("T4","rot (hex c) = hex c",
  "The uniform configuration is rotation-invariant."),
 ("T5","angCoupling (hex c) = hex (2c)",
  "The uniform configuration is an eigenvector, eigenvalue 2."),
]
AX = "[propext,<br/>Classical.choice,<br/>Quot.sound]"
for tag, stmt, read in data:
    rows.append([P("<b>%s</b>"%tag,"cell"), P(stmt,"cellm"), P(read,"cell"), P(AX,"cellm")])

t = Table(rows, colWidths=[10*mm, 52*mm, 60*mm, 44*mm])
t.setStyle(TableStyle([
    ("VALIGN",(0,0),(-1,-1),"TOP"),
    ("LINEBELOW",(0,0),(-1,0), 0.6, INK),
    ("LINEBELOW",(0,1),(-1,-2), 0.25, RULE),
    ("LINEBELOW",(0,-1),(-1,-1), 0.6, INK),
    ("TOPPADDING",(0,0),(-1,-1), 3.5), ("BOTTOMPADDING",(0,0),(-1,-1), 3.5),
    ("LEFTPADDING",(0,0),(-1,-1), 3), ("RIGHTPADDING",(0,0),(-1,-1), 3),
]))
A(t)
A(Spacer(1,5))
A(P("No occurrence of <font face='Mono' size='7.4'>sorryAx</font>; no elaboration errors. Two "
    "linter warnings remain, both on the trailing <font face='Mono' size='7.4'>ring</font> in T3, "
    "which is dead because <font face='Mono' size='7.4'>simp</font> closes every branch on its own; "
    "it is retained so the diff against the previous version stays legible."))
A(P("T1 and T2 together are the substantive pair. A gate acting pointwise commutes with any "
    "pointwise map, so T1 is expected; T2 shows that the same gate fails to commute with the "
    "operator that moves amplitude between sextants. Order-dependence in this model is carried "
    "entirely by the angular coupling, and not by the nonlinearity."))
A(boxed([P("<b>[OPEN] Toolchain mismatch.</b> The run above executed under "
    "<font face='Mono' size='7.4'>leanprover/lean4 v4.33.0-rc1</font>, the toolchain of the "
    "auxiliary tree that holds a built Mathlib. The repository containing the source pins "
    "<font face='Mono' size='7.4'>v4.32.0</font>, which is also what its CI uses. The evidence "
    "above is therefore evidence under v4.33.0-rc1 only, and has not yet been reproduced under the "
    "version the repository declares.", "warn")]))

# ---------------------------------------------------------------- 4
A(P("4. Spectral reading of T5", "h"))
A(P("angCoupling is the adjacency operator of the cyclic graph on six vertices. Its eigenvectors "
    "are the discrete Fourier modes v<sub>k</sub>(j) = exp(2πi kj/6) with eigenvalues "
    "λ<sub>k</sub> = 2 cos(2πk/6):"))
spec = [[P("<b>k</b>","cell")] + [P(str(i),"cell") for i in range(6)],
        [P("<b>λ<sub>k</sub></b>","cell")] + [P(v,"cell") for v in ["+2","+1","−1","−2","−1","+1"]]]
ts = Table(spec, colWidths=[16*mm] + [12*mm]*6, hAlign="LEFT")
ts.setStyle(TableStyle([
    ("LINEBELOW",(0,0),(-1,0),0.25,RULE),
    ("TOPPADDING",(0,0),(-1,-1),2.5),("BOTTOMPADDING",(0,0),(-1,-1),2.5),
]))
A(ts)
A(Spacer(1,5))
A(P("The k = 0 mode is the uniform configuration hex c, and its eigenvalue is 2. T5 therefore "
    "states that the hexagonal configuration is the Perron–Frobenius mode of the ring — the top of "
    "the coupling spectrum, and the unique eigenvector of largest eigenvalue with constant sign."))
A(P("The spectrum is doubly degenerate at λ = +1 (k = 1,5) and at λ = −1 (k = 2,4). These "
    "two-dimensional eigenspaces carry the two-dimensional irreducible representations of "
    "D<sub>6</sub>. Any symmetry-breaking bifurcation from the uniform branch must occur in one of "
    "them [1]. The model therefore contains both the invariant state and the modes that compete "
    "with it, which is the minimum needed to pose a mode-selection question."))

# ---------------------------------------------------------------- 5
A(P("5. An index constraint on the sphere [CLASSICAL]", "h"))
A(P("The following is standard and is included because it constrains any attempt to place a "
    "D<sub>6</sub> pattern on a closed surface. By the Poincaré–Hopf theorem, a tangent vector "
    "field with isolated zeros on a closed surface has zero-indices summing to the Euler "
    "characteristic. For the sphere, χ(S²) = 2, so a global flow cannot be everywhere "
    "non-vanishing: fixed points must exist, and their indices must total exactly 2 [4]."))
A(P("Two polar centres, each of index +1, exhaust the budget. A ring of six vortices at the "
    "vertices of a hexagonal pattern contributes +6, and is admissible only if accompanied by six "
    "saddles contributing −6. A configuration of two polar centres and six saddles with no "
    "compensating vortices totals −4 and is impossible on a sphere."))
A(boxed([P("<b>[OPEN] The bridge is absent.</b> The constraint above concerns a vector field on a "
    "two-sphere. The model of §2 is a six-site ring. No map between them is constructed in this "
    "paper, and the vortex–saddle cancellation is therefore not derived from the ring: it is a "
    "property of the sphere, stated alongside. Establishing a correspondence — or showing that none "
    "exists — is the principal open problem here.", "note")]))

# ---------------------------------------------------------------- 6
A(P("6. What is not established [OPEN]", "h"))
for item in [
 "No equation of motion is formalised, so no stability result is available. Writing the flow "
 "explicitly is the immediate next step; linearising the cubic term at hex c gives a Jacobian "
 "3c²I on the diagonal, and a per-mode threshold in λ<sub>k</sub> + 3c² follows immediately. That "
 "calculation is not performed here, and it is the one open item actually within reach.",
 "Which isotropy subgroup breaks first as amplitude grows is not determined.",
 "The correspondence between the ring and any field on a surface is not constructed (§5).",
 "The clean run has not been reproduced under the toolchain the repository pins (§3).",
 "No claim is made that the model bears on Saturn, on Chladni figures, or on any physical system. "
 "The shared symmetry class is not a shared mechanism.",
]:
    A(P("•&nbsp;&nbsp;" + item, "note"))

# ---------------------------------------------------------------- 7
A(P("7. Verification provenance: two failures, recorded", "h"))
A(P("This section exists because the file underlying §3 asserted, in its own header, that it had "
    "been kernel-verified on 20 July 2026 — “All five theorems: 0 sorry … No sorryAx” — and that "
    "assertion was false when written and stayed false for a month. It is retracted in the source "
    "and recorded here."))
A(P("<b>Stage one: a tool that failed quietly.</b> The first formalisation expressed the operators "
    "in <font face='Mono' size='7.4'>![…]</font> vector notation. Mathlib's "
    "<font face='Mono' size='7.4'>Matrix.cons_val</font> simplification lemmas do not chain to "
    "index 5 on a <font face='Mono' size='7.4'>Fin 6</font> literal, so every proof silently failed "
    "into <font face='Mono' size='7.4'>sorry</font> and all five theorems reported "
    "<font face='Mono' size='7.4'>sorryAx</font>. The definitions were rewritten by explicit pattern "
    "match, which reduces definitionally at every index. This stage is a known genre of failure and "
    "the kernel caught it."))
A(P("<b>Stage two: a claim that outran its evidence.</b> The rewrite was never re-run. A header was "
    "written recording a verification that had not taken place, and it survived for a month because "
    "nothing in the pipeline was positioned to contradict it:"))
for item in [
 "The file sat at the root of a repository whose Lake configuration declared a single build target, "
 "<font face='Mono' size='7.4'>lean_lib Orthogenesis</font>, which did not include it. "
 "<font face='Mono' size='7.4'>lake build</font> therefore never compiled it.",
 "The repository's continuous-integration job contained a step named “Real axiom check through the "
 "Lean kernel.” That step probed six definitions — <font face='Mono' size='7.4'>hexNeighbors</font>, "
 "<font face='Mono' size='7.4'>hexToVec2</font>, <font face='Mono' size='7.4'>Cell.center</font>, "
 "<font face='Mono' size='7.4'>Cell.radius</font>, <font face='Mono' size='7.4'>Colony.insert</font>, "
 "<font face='Mono' size='7.4'>Colony.expand</font> — and no theorems. It was a real kernel "
 "invocation about the wrong objects, and it passed.",
 "The repository held no built Mathlib at all, so the file could not have been compiled there even "
 "by hand. The header named a different tree as the site of verification; that tree's copy of the "
 "same file carried the header “KERNEL-VERIFIED: &lt;pending — run and record&gt;”.",
 "Three copies of the file existed on one disk, in three directories, two of them outside version "
 "control. They were not identical: the copy carrying the verification claim was missing a "
 "<font face='Mono' size='7.4'>ring</font> call that the copy carrying “pending” had. The claim and "
 "the code it described had drifted apart.",
]:
    A(P("•&nbsp;&nbsp;" + item, "note"))
A(Spacer(1,3))
A(P("The first actual run, on 21 August 2026, returned "
    "<font face='Mono' size='7.4'>sorryAx</font> for T1, T4 and T5. The cause was mundane: "
    "<font face='Mono' size='7.4'>fin_cases</font> could not synthesize "
    "<font face='Mono' size='7.4'>Fintype (Fin 6)</font> under the imports the file declared, so the "
    "case split never happened, and Lean's error recovery admitted the open goals. Adding "
    "<font face='Mono' size='7.4'>import Mathlib.Data.Fintype.Fin</font> and restoring the missing "
    "<font face='Mono' size='7.4'>ring</font> closed all three. Between the false header and the "
    "clean run the statements did not change, and nothing about them became more true. Only the "
    "evidence changed."))
A(boxed([P("<b>A third failure, of the same kind, in the preparation of this paper.</b> An earlier "
    "draft of this document was assembled by an automated assistant that read the file's header, "
    "took “No sorryAx” at face value, and wrote “Five results are proved without sorry” into the "
    "abstract. The false claim propagated from a comment into a manuscript in a single step, without "
    "any tool being run. That is the ordinary mechanism by which such claims travel, and it is worth "
    "recording that it operated here, in a paper whose subject is that mechanism.", "warn")]))
A(Spacer(1,3))
A(P("<b>The general shape.</b> Each layer of this pipeline checks well-formedness, and "
    "well-formedness is precisely what a false claim can afford. A build succeeds or fails; it "
    "cannot report that the file it never compiled was important. A kernel accepts a proof; it "
    "cannot report that the theorem is vacuous or that the declaration it was asked about is a "
    "definition. A CI badge turns green; it certifies that the steps configured ran, not that the "
    "steps configured were the right ones. A comment asserting verification is indistinguishable, "
    "to every automated reader, from a comment asserting anything else."))
A(P("<b>Remedy applied.</b> <font face='Mono' size='7.4'>SaturnHexagon.lean</font> is now a declared "
    "build target, so <font face='Mono' size='7.4'>lake build</font> compiles it. The "
    "continuous-integration job now contains exactly one step permitted to decide the outcome: it "
    "imports the module, prints the axioms of the five theorems by name, and fails on "
    "<font face='Mono' size='7.4'>sorryAx</font>, on an elaboration error, or on an axiom-line count "
    "other than five. The textual scans — grep for "
    "<font face='Mono' size='7.4'>theorem</font>, grep for "
    "<font face='Mono' size='7.4'>sorry</font> — are retained but marked informational and are not "
    "allowed to gate anything, because neither can distinguish a proof from a comment. The duplicate "
    "copies have been retired, leaving one file under version control. The surviving root-level Lean "
    "files that remain outside every build target are now listed by name in the job's output, as "
    "unchecked."))

# ---------------------------------------------------------------- 8
A(P("8. What this licenses", "h"))
A(P("The model of §2 is a toy: six real amplitudes on a ring, no dynamics, no physics. Its five "
    "theorems are now genuinely machine-checked, and they say something small and exact — that "
    "order-dependence in this operator algebra is carried by the coupling and not by the "
    "nonlinearity, and that the uniform hexagonal state is the top of the coupling spectrum with the "
    "competing modes sitting in the D<sub>6</sub> two-dimensional irreducibles just below it. That "
    "is worth having, and it is all that is claimed."))
A(P("The verification record of §7 is the larger contribution, and it is not a claim about Lean. "
    "The same structure — a well-formed identifier, a green check, a passing job, a confident "
    "sentence in a comment — recurs wherever scholarly infrastructure certifies form and is read as "
    "certifying content. What makes this instance usable is that it is a single corpus, owned by one "
    "author, audited against itself, with the file names, dates, commands and outputs available. The "
    "author's own tooling, written to catch exactly this, did not catch it."))

# ---------------------------------------------------------------- refs
A(P("References", "h"))
for r in [
 "[1] M. Golubitsky, I. Stewart, D. G. Schaeffer. <i>Singularities and Groups in Bifurcation "
 "Theory, Volume II.</i> Springer, 1988.",
 "[2] J. W. Swift. <i>Bifurcation and symmetry in convection.</i> PhD thesis, University of "
 "California, Berkeley, 1984.",
 "[3] P. G. Kevrekidis. <i>The Discrete Nonlinear Schrödinger Equation.</i> Springer Tracts in "
 "Modern Physics 232, 2009.",
 "[4] J. Milnor. <i>Topology from the Differentiable Viewpoint.</i> University Press of Virginia, "
 "1965.",
 "[5] The mathlib Community. <i>The Lean mathematical library.</i> CPP 2020.",
]:
    A(P(r, "ref"))

# ---------------------------------------------------------------- doc
def footer(canv, doc):
    canv.saveState()
    canv.setFont("Serif", 6.8); canv.setFillColor(MUTED)
    canv.setStrokeColor(RULE); canv.setLineWidth(0.3)
    canv.line(22*mm, 15*mm, 188*mm, 15*mm)
    canv.drawString(22*mm, 11*mm,
        "SaturnHexagon.lean · Lean 4 + Mathlib · not peer-reviewed")
    canv.drawRightString(188*mm, 11*mm,
        "© 2026 P. N. Grossi · G6 LLC · CC BY-NC-ND 4.0 · p. %d" % doc.page)
    canv.restoreState()

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "DNLS_D6_ring_draft.pdf")
doc = BaseDocTemplate(out, pagesize=A4,
                      leftMargin=22*mm, rightMargin=22*mm,
                      topMargin=18*mm, bottomMargin=20*mm,
                      title="A Formally Verified D6-Equivariant DNLS Ring",
                      author="Pablo Nogueira Grossi")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="n")
doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=footer)])
doc.build(story)
print("wrote", out)
