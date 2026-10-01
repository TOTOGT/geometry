#!/usr/bin/env python3
"""Writes docs/axle-issues-to-file-3.html: one more obligation with no AXLE issue."""
import urllib.parse, html
REPO="https://github.com/TOTOGT/AXLE/issues/new"
NEW=[("P_ON (correctOrder drv) > 0: discretisation bound",
 "book4/ch09.html and HVEH/ch09.html carried this sorry under 'AXLE Issue #14'. Real #14 is Theorem T1 (full ODE Gronwall integration, z(t) monotonicity), a different obligation, so the number was removed on 2026-10-01.\n\n"
 "Statement: the discretisation bound behind P_ON (correctOrder drv) > 0. Check whether it reduces to #14 once T1 is proved; if so, close this as a duplicate."),
 ("closurePoints_stationary: lean/Main.lean and AXLE_v8_1.lean state it with a false hypothesis",
 "Found 2026-10-01 while tracing #6. The true statement, with hypothesis Cardinal.aleph0 < alpha.cof, is PrincipiaVol1.closurePoints_stationary in PrincipiaOrthogona1/PrincipiaVol1.lean (V7; built and kernel-checked at Lean/Mathlib v4.14.0, 0 sorry). Two other files carry the theorem with a hypothesis that is not cofinality > omega:\n\n"
 "1. lean/Main.lean (the file commit a1f11b9 changed, 'closes #6') assumes omega < alpha.card.ord, i.e. uncountable cardinality. sup_lt_of_regular as stated there is false: alpha = omega_1 + omega has card omega_1, and s n = omega_1 + n has sup = alpha. The theorem is false too: C = {omega_1 + n : n >= 1} + {alpha} is omega-closed and unbounded below alpha and contains no limit ordinal below alpha. The 2026-09-09 kernel audit also shows lean/Main.lean failing with 59 errors against current Mathlib (Ordinal.sup, Ordinal.IsLimit no longer resolve).\n\n"
 "2. AXLE_v8_1.lean closurePoints_stationary_regular assumes alpha.card.ord = alpha (initial ordinal, not regular). False for alpha = omega_omega: C = {omega_n + 1 : n >= 1} + {alpha} is omega-closed and unbounded and contains no limit below alpha. Its 'honest admit #5' sorry therefore cannot be filled.\n\n"
 "Checked in Lean 4.32.0 / Mathlib v4.32.0 (ClosurePointsCheck.lean in the geometry repository: both counterexamples and the corrected theorem, zero sorry, standard axioms only). AXLE_v8_1.lean was patched with the corrected hypothesis and proof (5 sorries remain instead of 6). Still needed: lean/Main.lean, which does not build against current Mathlib, to be retired or replaced by the V7 theorem; commit the AXLE_v8_1.lean change. #6 was closed citing the regular case, which is true in PrincipiaVol1 but not in the file the closing commit touched."),
 ("Regularity-free closurePoints_stationary (the stated goal of #6) is false when cof alpha = omega",
 "#6 asked to remove the regularity hypothesis from closurePoints_stationary and prove it for all limit ordinals, and was closed with the regular case only. The goal as stated cannot be met (proved in Lean as regularity_free_goal_is_false, ClosurePointsCheck.lean): if cof alpha = omega, take a cofinal strictly increasing omega-sequence of successor ordinals; its range (plus alpha if needed) is omega-closed and unbounded below alpha and contains no limit ordinal below alpha, so the closure points are not stationary. Both options listed in #6 (strengthen the closure axiom; case split on cofinality) fail for the same reason.\n\n"
 "About fifteen pages (GameTheory_Full_Pack, ch-ocio, AMonster/monsterlaw, book1/vol2-dashboard, book5/chV-axle) still show 'Issue 6' as an open boundary ('hyper-Mahlo fixed point without regularity hypothesis'). Needed: state the true scope (cof > omega) on the pages and decide whether the Volume IV hyper-Mahlo claim for all limit ordinals is to be withdrawn or restated."),
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
