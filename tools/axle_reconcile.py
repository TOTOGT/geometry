#!/usr/bin/env python3
"""Writes docs/axle-reconciliation.md and docs/axle-issues-to-file-2.html.
Issue numbers below are from docs/axle-issue-map.md (checked against GitHub 2026-09-15).
Nothing here has been re-checked against GitHub since; see the file for what to verify."""
import urllib.parse, html
REPO = "https://github.com/TOTOGT/AXLE/issues/new"

NEW = [
 ("kappa_lipschitz: Lipschitz bound on the dm3 coupling term",
  "Cited as 'AXLE Issue #12' on about 25 pages (Book 4 ch10, chE-gtct-alt, ch-eta-dnls, dm3-lab-index, Book 3 mini-course sessions 2-3 and index pages). "
  "Real #12 is the separation_theorem eigenvalue-API issue, so this obligation has no issue of its own.\n\n"
  "Statement needed: a Lipschitz (or local Lipschitz) constant for K in the coupling eps*(r-1)*exp(-z). "
  "Caution from 2026-10-01: exp(-z) is not globally Lipschitz as z -> -infinity, so the statement must carry a domain such as z >= z_min. "
  "Skeleton in sessao3-esqueleto-lean.html (K_lip : exists L, LipschitzWith L K).\n\nSource pages: book4/ch10.html, sessao3-esqueleto-lean.html."),
 ("Outer basin: convergence domain (z(0) hypothesis) for the helical attractor",
  "book4/ch10-outer-basin-check.py shows the chapter-10 statement 'every r(0) > 1 converges' fails: counterexamples (r0,z0) = (1.5,-2), (2,-1), (1.001,-3), (8,0), (10,0). "
  "At z(0)=0 the largest converging r(0) is about 6.896. Coupling 2(r-1)e^{-z} blows up as z -> -infinity (finite-time blow-up).\n\n"
  "Needed: state and prove (or refute) convergence for z(0) >= z_min(r(0)), or fix the restricted statement z(0)=0, 1<r(0)<=6.8. "
  "Lean statement should carry the hypothesis. Related: #14 (Gronwall integration) and the kappa_lipschitz issue."),
 ("inner_basin_escape: obstruction to inner-basin escape (null-causality route)",
  "Cited as #13 in book8/index.html, book8/ch5-regular.html and book8/notes/issue-13-null-causality.md, and as #14 in book8/ch2-event-horizon.html. "
  "Real #13 is AutophagyDm3 (Mather + Poincare-Bendixson) and real #14 is Theorem T1 (Gronwall), so neither matches.\n\n"
  "Status per the pages themselves: ch2 says the argument does not hold and the obligation reopens; ch5 says the 'PROVED' badge should read open."),
 ("jackknife_correspondence: contact diffeomorphism tractor-trailer to LAW3M",
  "Described in book8/notes/issue-12-jackknife-correspondence.md and cited as #12 in book8/ch3-singularity.html and book8/notes/crop-circle-watch-2026-06-25.md. "
  "Real #12 is separation_theorem. Needs its own issue."),
 ("Matrix.minnorm missing from Mathlib: blocks Proof 6 / Chapter 5 zero-sorry",
  "book4/chIV-orthogonality.html cites 'Issue #15' for this Mathlib gap (about 8 places). Real #15 is an unrelated pasted trading page. "
  "Needed: the lemma, or a workaround in AXLE, so that Chapter 5's Lean file has no sorry."),
 ("P_ON (wrongOrder drv) = 0: formal statement for the wrong operator order",
  "book4/ch09.html and HVEH/ch09.html cite #15 for this sorry. Real #15 is unrelated."),
 ("No homotopy between gamma_K and gamma_F: formal statement",
  "book4/ch09.html and HVEH/ch09.html cite #16 for this sorry (also docs/ml-evidence copy). Real #16 is a discussion thread, not an issue."),
 ("g_arith: connect to Mathlib vonMangoldt",
  "book4/ch11.html, chpt11.md, chpt14.md cite #18. Real #18 is a pull request (rename screenshot), and numbers cannot be reused."),
 ("Critical line as contact symmetry locus: digamma cancellation",
  "book4/chpt12.md, chpt14.md cite #20. Real #20 is a pull request (README for crop circles). Three different meanings of #20 appear in the corpus."),
 ("p-adic local coefficient definition",
  "book4/chpt13.md, chpt14.md cite #21; book4/METHODOLOGY.md also cites #21 for certify_rstar_rigorous.py, a different thing. "
  "#21 is not among the 13 open issues (checked 2026-10-01); it is a pull request or a closed item, so it cannot be this issue's number."),
]

def link(t,b):
    return REPO+"?"+urllib.parse.urlencode({"title":t,"body":b},quote_via=urllib.parse.quote)

md=open("docs/axle-reconciliation.head.md").read() if False else ""
rows=[]
for i,(t,b) in enumerate(NEW,1):
    rows.append((i,t,b,link(t,b)))

with open("docs/axle-issues-to-file-2.html","w",encoding="utf-8") as f:
    f.write("<!doctype html><html lang=en><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><title>AXLE issues to file</title>"
    "<style>body{font-family:system-ui,sans-serif;max-width:46rem;margin:1.5rem auto;padding:0 1rem;line-height:1.45;color:#1a1a1a;background:#fff}"
    "h1{font-size:1.4rem}.row{border:1px solid #ccc;border-radius:8px;padding:.8rem 1rem;margin:.8rem 0}.row.done{background:#eef7ee;border-color:#9c9}"
    ".t{font-weight:600}.go{display:inline-block;margin:.5rem .6rem .3rem 0;padding:.45rem .9rem;background:#0b5cad;color:#fff;border-radius:6px;text-decoration:none}"
    "details{font-size:.88rem;color:#444}pre{white-space:pre-wrap}label{font-size:.9rem}#c{font-size:.9rem;color:#555}"
    "@media(prefers-color-scheme:dark){body{background:#161616;color:#eee}.row{border-color:#444}.row.done{background:#1c2b1c}details,#c{color:#bbb}}</style>"
    "<body><h1>AXLE issues to file</h1><p>Click <b>Open on GitHub</b> on each. The title and body are filled in; press <b>Submit new issue</b> there. "
    "Tick the box when done. Nothing is filed until you submit. Checked 2026-10-01: none of these ten is already open.</p>"
    "<p id=c>0 of %d filed</p>"%len(rows))
    for i,t,b,u in rows:
        f.write("<div class=row id=r%d><div class=t>%d. %s</div><a class=go target=_blank rel=noopener href='%s'>Open on GitHub</a>"
                "<label><input type=checkbox onchange=\"mark(%d,this)\"> filed</label><details><summary>body</summary><pre>%s</pre></details></div>"
                %(i,i,html.escape(t),html.escape(u),i,html.escape(b)))
    f.write("<p style='font-size:.85rem'>After filing, tell Claude the new numbers so they go into <code>docs/axle-issue-map.md</code> and the pages.</p>"
            "<script>function mark(i,e){document.getElementById('r'+i).classList.toggle('done',e.checked);"
            "var n=document.querySelectorAll('input:checked').length;document.getElementById('c').textContent=n+' of %d filed'}</script></body></html>"%len(rows))
with open("docs/axle-issues-to-file-2.md","w",encoding="utf-8") as f:
    f.write("# AXLE issues to file, round 2 (generated)\n\nClick-through links, title and body prefilled. Same content as `axle-issues-to-file-2.html`.\n\n")
    for i,t,b,u in rows:
        f.write("%d. [%s](%s)\n\n"%(i,t,u))
print(len(rows),"issues;",max(len(r[3]) for r in rows),"max url length")
