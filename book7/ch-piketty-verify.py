#!/usr/bin/env python3
"""Verify book7/ch-piketty.html against the held copy of Piketty's book.
Checks (1) the arithmetic on the page, (2) that key phrases occur on the stated printed page
(PDF page = printed + 5). SKIP, never PASS, when the PDF is absent. Controls: a phrase
that is not in the book must NOT be found."""
import os, re, subprocess, sys, pathlib
fail = 0
def chk(name, ok):
    global fail
    print(("PASS " if ok else "FAIL ") + name); fail += (not ok)
# (1) arithmetic
chk("alpha = r*beta: 0.05*6 = 0.30", abs(0.05*6-0.30) < 1e-12)
chk("beta = s/g: 0.12/0.02 = 6", abs(0.12/0.02-6) < 1e-12)
for g, b, a in [(0.02, 6, 0.30), (0.015, 8, 0.40), (0.01, 12, 0.60)]:
    chk(f"table row g={g}: beta={b}, alpha={a}", abs(0.12/g-b) < 1e-9 and abs(0.05*b-a) < 1e-9)
# page text on the page itself
here = pathlib.Path(__file__).with_name("ch-piketty.html").read_text(encoding="utf-8")
for must in ["Not established", "not a statement by Thomas Piketty", "ch19-a-toy-for-cycles", "ch-chomsky.html"]:
    chk(f"page contains {must!r}", must in here)
# (2) held copy
pdf = os.environ.get("PIKETTY_PDF") or os.path.expanduser("~/Downloads/Full Capital 21 century - Piketty.pdf")
if not os.path.exists(pdf):
    print("SKIP held copy absent:", pdf); print(f"{fail} FAIL"); sys.exit(1 if fail else 0)
def page(printed):
    out = subprocess.run(["pdftotext", "-f", str(printed+5), "-l", str(printed+5), pdf, "-"],
                         capture_output=True, text=True).stdout
    return re.sub(r"\s+", " ", out.lower())
cases = [(52, "accounting identity"), (166, "second fundamental law"), (168, "asymptotic"),
         (358, "contingent historical proposition"), (571, "central contradiction of capitalism"),
         (24, "figure i.1"), (340, "figure 10.1"), (348, "figure 10.5"), (349, "figure 10.6"),
         (339, "1914")]
for p, ph in cases:
    chk(f"p.{p} contains {ph!r}", ph in page(p))
chk("control: p.52 does NOT contain 'quantum chromodynamics'", "quantum chromodynamics" not in page(52))
chk("control: p.358 does NOT contain 'second fundamental law'", "second fundamental law" not in page(358))
print(f"{fail} FAIL"); sys.exit(1 if fail else 0)
