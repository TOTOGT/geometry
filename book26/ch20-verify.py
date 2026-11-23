#!/usr/bin/env python3
"""book26/ch20-verify.py -- structure and honesty of ch20-two-routes-one-spine.html. Checks wording and markup only;
it does NOT check any Lean declaration, the census, or the mathematics. Each control removes a statement and must fail."""
import re, sys, html as h
from pathlib import Path
P = Path(__file__).resolve().parent / "ch20-two-routes-one-spine.html"
raw = P.read_text(encoding="utf-8")
def vis(r):
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", r, flags=re.S)
    return re.sub(r"\s+", " ", h.unescape(re.sub(r"<[^>]+>", " ", t)))
def checks(r):
    t = vis(r); out = []
    out.append(("sections S1..S8 in order", re.findall(r'data-n="(S\d)"', r) == [f"S{i}" for i in range(1, 9)]))
    out.append(("pinned commit stated", "40e56bab026552e089d7afcfeff08d2defb9c005" in r))
    out.append(("second-hand label present", "SECOND-HAND" in t and "not re-opened" in t.lower()))
    out.append(("no verdict stated", "no verdict" in t))
    out.append(("Claude-tried-routes claim disclaimed", "tried several proof strategies" in t and "Not established here" in t))
    out.append(("no fallacy attributed", "No fallacy is attributed" in t))
    out.append(("no refutation wording", not re.search(r"\b(refuted|disproved|debunked|fell for)\b", t, re.I)))
    out.append(("open items present", len(re.findall(r'data-s="open"', r)) == 6))
    out.append(("no script, form or network code", not re.search(r"<(script|form)|fetch\(|XMLHttpRequest", r)))
    return out
bad = 0
for l, ok in checks(raw):
    print(("PASS " if ok else "FAIL ") + l); bad += (not ok)
for name, mut in (("S3 removed", lambda r: r.replace('data-n="S3"', 'data-n="X"')),
                  ("second-hand removed", lambda r: r.replace("SECOND-HAND", "VERIFIED")),
                  ("disclaimer removed", lambda r: r.replace("tried several proof strategies", "x")),
                  ("verdict word added", lambda r: r.replace("no verdict", "refuted")),
                  ("open item closed", lambda r: r.replace('data-s="open"', 'data-s="done"', 1))):
    if all(ok for _, ok in checks(mut(raw))): print("FAIL control not rejected:", name); bad += 1
    else: print("PASS control rejected:", name)
print("[HONESTY] Checks wording and markup only; not any declaration, census or proof.")
print("ALL PASS" if not bad else f"FAILED: {bad}"); sys.exit(1 if bad else 0)
