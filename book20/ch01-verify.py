#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book20/ch01-verify.py -- every number on book20/ch01-the-planes-that-came-back.html.
Run before the page was written (R24); the page prints what this prints.

    python3 book20/ch01-verify.py [--downloads DIR]

  [1] Wald (1943/1980) is the ledger row and still hashes to it
  [2] Part I: the p.71 example. The root of Wald's equation is q = .850
  [3] Part V: the pp.63-65 example. q(i) = q * delta(i) / gamma(i) reproduces
      Wald's table (.61 .95 .85 .98) and averages back to q
  [4] the inversion: the part with the MOST holes is the LEAST vulnerable
  [5] what the text says, verbatim: "hypothetical", and armor
  [6] Evans & Rosenthal Example 5.1.1 is on p. 254
  [7] this corpus's own survivors: html paths ever added vs tracked today (git)
  [HONESTY]
"""
import hashlib, os, re, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
def dl():
    if "--downloads" in sys.argv: return Path(sys.argv[sys.argv.index("--downloads") + 1])
    for c in ("~/mnt/Downloads", "~/Downloads"):
        p = Path(os.path.expanduser(c))
        if p.is_dir(): return p
DL = dl()
WA = "9-A method of estimating plane vulnerability ....pdf"
ER = "Probability and Statistics- The Science of Uncertainty.pdf"
def pages(name):
    try:
        out = subprocess.run(["pdftotext", "-layout", str(DL / name), "-"], capture_output=True, text=True, timeout=120).stdout
        return out.split("\f")
    except Exception:
        return None

print("[1] ledger")
row = [l.split("\t") for l in open(ROOT / "docs/floor-texts.tsv", encoding="utf-8") if WA in l or "plane vulnerability" in l.lower()]
wa = DL / WA if DL else None
if wa and wa.exists():
    h = sha(wa)
    check("Wald file hashes to a ledger row", any(r[3] == h for r in row) or h in open(ROOT / "book20/index-verify.py").read(), h[:16])
else:
    print("SKIP Wald file not on this machine")

print("[2] Part I, p.71: the root of sum a_i / q^i = 1 - a_0")
a = [.80, .08, .05, .01, .006, .004]          # Wald p.71, N = 500, A = 400,40,25,5,3,2
check("a_i are A_i / N", [round(x/500, 3) for x in (400, 40, 25, 5, 3, 2)] == a)
f = lambda q: sum(a[i] / q**i for i in range(1, 6)) - (1 - a[0])
lo, hi = 0.5, 0.9999
for _ in range(200):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if f(mid) > 0 else (lo, mid)
q = (lo + hi) / 2
check("q = .850 to three places", round(q, 3) == 0.850, f"q = {q:.6f}")
print(f"     probability one hit downs the plane: {1-q:.3f}")
print(f"     planes lost L = 1 - a_0 - ... - a_5 = {1-sum(a):.3f}  (25 of 500 did not return)")

print("[3] Part V, pp.63-65")
area = {"engines": 35, "fuselage": 45, "fuel system": 20, "other": 30}
hits = {"engines": 39, "fuselage": 78, "fuel system": 31, "other": 54}
wald = {"engines": .61, "fuselage": .95, "fuel system": .85, "other": .98}
A = [68, 29, 12, 10]
check("hits on returning planes = A1 + 2A2 + 3A3 + 4A4 = 202", sum((i+1)*x for i, x in enumerate(A)) == 202 == sum(hits.values()))
TA, TH = sum(area.values()), sum(hits.values())
qi = {}
for k in area:
    g, d = area[k] / TA, hits[k] / TH
    qi[k] = 0.85 * d / g
    print(f"     {k:12} gamma {g:.3f}  delta {d:.3f}  q(i) {qi[k]:.3f}  downed by one hit {1-qi[k]:.3f}")
    check(f"{k}: q(i) rounds to Wald's {wald[k]}", round(qi[k], 2) == wald[k])
check("sum gamma(i) q(i) = q exactly", abs(sum(area[k]/TA*qi[k] for k in area) - .85) < 1e-12)

print("[4] the inversion")
most_holes = max(hits, key=lambda k: hits[k] / area[k])
fewest = min(hits, key=lambda k: hits[k] / area[k])
most_vuln = min(qi, key=qi.get)
check("most holes per sq ft: other parts; fuselage close behind", most_holes == "other", f"{ {k: round(hits[k]/area[k],2) for k in area} }")
check("fewest holes per sq ft = most vulnerable = engines", fewest == most_vuln == "engines")
print(f"     engines: {area['engines']/TA:.1%} of the area, {hits['engines']/TH:.1%} of the holes")
print(f"     fuselage has the most holes ({hits['fuselage']}) and the lowest one-hit loss but one ({1-qi['fuselage']:.2f})")

print("[5] the text, verbatim")
P = pages(WA) if DL else None
if P:
    body = "\n".join(P)
    check("p.65 (pdf 74) calls the example hypothetical", "hypothetical example" in P[73])
    check("p.89 (pdf 98): 'guides for locating protective armor'", "guides for locating protective armor" in P[97])
    n = len(re.findall(r"\barmou?r", body, re.I))
    check("'armor' occurs once in the text layer", n == 1, f"{n} occurrence(s)")
    check("Part I was SRG memo 85", "SRG memo 85" in body)
else:
    print("SKIP Wald text (no pdftotext or file)")

print("[6] Evans & Rosenthal")
E_ = pages(ER) if DL else None
if E_:
    p = E_[267]
    check("Example 5.1.1 Stanford Heart Transplant Study on printed p. 254", p.lstrip().startswith("254") and "Stanford Heart Transplant" in p)
    check("treatment survival is Y + Z: waiting time plus time after transplant", "survival times for the treatment group are then given by the values of Y" in E_[268])
else:
    print("SKIP E&R")

print("[7] this corpus")
G = ["git", "--no-optional-locks", "-C", str(ROOT)]
now = set(subprocess.run(G + ["ls-files", "*.html"], capture_output=True, text=True).stdout.split())
added = set(subprocess.run(G + ["log", "--diff-filter=A", "--name-only", "--format=", "--", "*.html"], capture_output=True, text=True).stdout.split())
gone = sorted(p for p in added if p not in now)
print(f"     html paths tracked today: {len(now)}")
print(f"     html paths ever added:    {len(added)}")
print(f"     added and no longer tracked: {len(gone)}  (renames, retirements, retractions)")
check("the site shows only the survivors", len(gone) > 0)

print("""
[HONESTY]
Blocks [2]-[4] recompute Wald's two worked examples from the inputs he prints;
both examples are labelled hypothetical by Wald, so nothing here is a fact about
1943 aircraft. Block [3]'s formula q(i) = q*delta(i)/gamma(i) is the one that
reproduces his table; the page's rendering of it in the scan is garbled, so the
formula is inferred from the numbers, and every one of the four matches.
Block [5] reads an OCR layer: 'armor' once means once in that layer.
Block [7] counts paths, not claims: a path that disappeared may have been a
rename, a duplicate removed, or a retraction, and this script does not say which.
""")
print(f"{len(FAIL)} FAIL")
sys.exit(1 if FAIL else 0)
