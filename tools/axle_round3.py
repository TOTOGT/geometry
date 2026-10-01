#!/usr/bin/env python3
"""Writes docs/axle-issues-to-file-3.html: one more obligation with no AXLE issue."""
import urllib.parse, html
REPO="https://github.com/TOTOGT/AXLE/issues/new"
NEW=[("P_ON (correctOrder drv) > 0: discretisation bound",
 "book4/ch09.html and HVEH/ch09.html carried this sorry under 'AXLE Issue #14'. Real #14 is Theorem T1 (full ODE Gronwall integration, z(t) monotonicity), a different obligation, so the number was removed on 2026-10-01.\n\n"
 "Statement: the discretisation bound behind P_ON (correctOrder drv) > 0. Check whether it reduces to #14 once T1 is proved; if so, close this as a duplicate."),
 ("closurePoints_stationary for all limit ordinals (cofinality omega): the part of #6 not delivered",
 "#6 asked to remove the regularity hypothesis from closurePoints_stationary. It was closed by a1f11b9 (2026-03-22) with the statement proved for regular uncountable cardinals only (cf(alpha) > omega), by its own closing comment. The goal stated in its title, all limit ordinals, was not proved: for alpha = omega*2 or omega^omega the sup of the chain can equal alpha.\n\n"
 "About fifteen pages (GameTheory_Full_Pack, ch-ocio, AMonster/monsterlaw, book1/vol2-dashboard, book5/chV-axle) still cite 'Issue 6' as open for exactly this. Options from #6: A, strengthen the closure axiom to IsClosedBelow; B, case split on cf(alpha). "
 "Also: AXLE_v8_1.lean still carries closurePoints_stationary_regular with a sorry (honest admit #5), although #6's closing comment says the regular case is proved in lean/Main.lean; reconcile the two files."),
 ("g6_unconditional_closure: exists m <= 33, crystal saturated and eigenmode locked",
 "TOGT.g6_unconditional_closure (AXLE_v8_1.lean line 154, also lean/Ordinal/MahloClosure.lean) is a sorry. It states a finite G6 crystal saturation within 33 steps for every PhaseVector. It is a dynamics statement, not an ordinal club-filter statement, but GameTheory_Full_Pack.html and ch-ocio.html label it 'Issue 6 / last sorry in the Collatz-dm3 bridge'. "
 "Kernel audit 2026-09-09 shows sorryAx on it. No open issue carries it.")]
rows=[(t,b,REPO+"?"+urllib.parse.urlencode({"title":t,"body":b},quote_via=urllib.parse.quote)) for t,b in NEW]
with open("docs/axle-issues-to-file-3.html","w",encoding="utf-8") as f:
    f.write("<!doctype html><html lang=en><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><title>AXLE issue to file, round 3</title>"
    "<body style='font-family:system-ui,sans-serif;max-width:46rem;margin:1.5rem auto;padding:0 1rem;line-height:1.45'>"
    "<h1>AXLE issue to file, round 3</h1><p>One obligation. Click, then press Submit new issue. Nothing is filed until you do.</p>")
    for t,b,u in rows:
        f.write("<p><b>%s</b></p><p><a href='%s' target=_blank rel=noopener style='display:inline-block;padding:.45rem .9rem;background:#0b5cad;color:#fff;border-radius:6px;text-decoration:none'>Open on GitHub</a></p><pre style='white-space:pre-wrap;font-size:.85rem'>%s</pre>"%(html.escape(t),html.escape(u),html.escape(b)))
    f.write("</body></html>")
