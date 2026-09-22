#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book20/index-verify.py -- every number and address on book20/index.html.

    python3 book20/index-verify.py [--downloads DIR]

Blocks
  [1] the two held texts are rows in docs/floor-texts.tsv (R19: read the ledger),
      and the files on disk still hash to those rows
  [2] addresses in Evans & Rosenthal, located by text search, never copied
  [3] the HURDAT2 file: hash, storm count, year range, basins
  [4] the primary sources the volume WANTS: searched for, by several patterns
  [5] the placements the index names exist at the paths it gives
  [HONESTY]

Primary sources: Evans & Rosenthal, Probability and Statistics: The Science of
Uncertainty; NOAA NHC HURDAT2 (Atlantic). Ellenberg, How Not to Be Wrong (2014),
is held as a guide to structure, not as an authority.

Standard library, plus the `pdftotext` binary (poppler) for block [2]; the block
reports SKIP rather than PASS if it is missing.
"""
import hashlib, os, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAIL = []

def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def downloads():
    if "--downloads" in sys.argv:
        return Path(sys.argv[sys.argv.index("--downloads") + 1])
    for c in ("~/mnt/Downloads", "~/Downloads"):
        p = Path(os.path.expanduser(c))
        if p.is_dir():
            return p
    return None

ER = "Probability and Statistics- The Science of Uncertainty.pdf"
EL = "how-not-to-be-wrong-ellenberg-20169131536812.pdf"
HU = "hurdat2-1851-2025-091226.txt"
DL = downloads()

# [1] ledger
print("[1] ledger rows (docs/floor-texts.tsv)")
rows = {}
for line in (ROOT / "docs/floor-texts.tsv").read_text(encoding="utf-8").splitlines()[1:]:
    f = line.split("\t")
    if len(f) >= 5:
        rows.setdefault(f[4], (f[2], f[3]))
for name, pages in ((ER, "774"), (EL, "532")):
    r = rows.get(name)
    check(f"ledger row: {name[:40]}", r is not None and r[0] == pages,
          f"pages {r[0] if r else None}, expected {pages}")
    if r and DL and (DL / name).exists():
        check(f"file still hashes to ledger: {name[:40]}", sha(DL / name) == r[1], r[1][:16])
    else:
        print(f"SKIP hash of {name[:40]} (Downloads not found)")

# [2] addresses in Evans & Rosenthal
print("[2] addresses in Evans & Rosenthal (PDF page index, 1-based)")
pages = None
if DL and (DL / ER).exists():
    try:
        txt = subprocess.run(["pdftotext", "-layout", str(DL / ER), "-"],
                             capture_output=True, text=True, check=True).stdout
        pages = txt.split("\f")
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print(f"SKIP [2]: {e}")
if pages:
    n = len(pages) - (1 if pages[-1].strip() == "" else 0)
    check("page count from the PDF agrees with the ledger", n == 774, f"{n} pages")
    def first(pat, start=20):
        rx = re.compile(pat)
        for i, p in enumerate(pages):
            if i >= start and rx.search(p):
                return i + 1
        return None
    def printed(pdf):  # the number in the running head or footer of that page
        ls = [l.strip() for l in pages[pdf - 1].splitlines() if l.strip()]
        if re.fullmatch(r"\d+", ls[-1]):          # chapter openers: folio at the foot
            return int(ls[-1])
        m = re.match(r"^(\d+)\s", ls[0]) or re.search(r"\s(\d+)$", ls[0])  # running head
        return int(m.group(1)) if m else None
    # the offset is read off the table of contents, not assumed: 6.3.3 is listed at 332
    toc = pages[4]
    m = re.search(r"6\.3\.3 Testing Hypotheses and P.Values[ .]*?(\d+)", toc)
    toc332 = int(m.group(1)) if m else None
    at = first(r"(?m)^\s*6\.3\.3 Testing Hypotheses and P.Values")
    off = at - toc332 if (at and toc332) else None
    check("printed page = PDF page - offset, offset read from the contents", off is not None, f"offset {off}")
    ADDR = [
        ("Chapter 3, Expectation", r"(?m)^\s*Chapter 3\s*$", 129),
        ("5.1 Why Do We Need Statistics? (survivorship example)", r"(?m)^\s*5\.1 Why Do We Need Statistics\?", 254),
        ("6.3.3 Testing Hypotheses and P-Values", r"(?m)^\s*6\.3\.3 Testing Hypotheses and P.Values", 332),
        ("9.3 The Problem with Multiple Checks", r"(?m)^\s*9\.3 The Problem with Multiple Checks", 509),
        ("Chapter 10, Relationships Among Variables", r"(?m)^\s*Chapter 10\s*$", 511),
        ("10.3 Quantitative Response and Predictors (regression)", r"(?m)^\s*10\.3 Quantitative Response", 538),
    ]
    for label, pat, want in ADDR:
        pdf = first(pat)
        got = pdf - off if (pdf and off is not None) else None
        head = printed(pdf) if pdf else None
        check(f"p. {want}: {label}", got == want and head in (None, got),
              f"PDF page {pdf}, printed {got}, running head {head}")
    # what the held text does NOT carry, by four patterns
    for label, pat in (("Galton", r"(?i)galton"), ("regression toward/to the mean", r"(?i)toward(s)? the mean|regression to the mean"),
                       ("'regression effect'", r"(?i)regression effect"), ("'mediocrity'", r"(?i)mediocr")):
        hits = [i + 1 for i, p in enumerate(pages) if re.search(pat, p)]
        check(f"not in Evans & Rosenthal: {label}", not hits, f"{len(hits)} pages")

# [3] HURDAT2
print("[3] HURDAT2")
if DL and (DL / HU).exists():
    lines = (DL / HU).read_text(encoding="latin-1").splitlines()
    head = [l for l in lines if re.match(r"^[A-Z]{2}\d{6},", l)]
    years = sorted({int(l[4:8]) for l in head})
    basins = sorted({l[:2] for l in head})
    print(f"     sha256 {sha(DL / HU)}")
    print(f"     storms {len(head)}, years {years[0]}-{years[-1]}, basins {basins}, lines {len(lines)}")
    check("HURDAT2 covers 1851-2025", years[0] == 1851 and years[-1] == 2025)
    check("HURDAT2 is Atlantic only", basins == ["AL"])
    check("HURDAT2 storm count is 1988", len(head) == 1988, str(len(head)))
    check("HURDAT2 spans 175 years, inclusive", years[-1] - years[0] + 1 == 175, str(years[-1] - years[0] + 1))
else:
    check("HURDAT2 file present", False, "not found in Downloads")

# [4] wanted primary sources
print("[4] wanted primary sources -- searched, by filename and by ledger first line")
names = [p.name for p in DL.iterdir()] if DL else []
firsts = [l.split("\t")[5] if len(l.split("\t")) > 5 else ""
          for l in (ROOT / "docs/floor-texts.tsv").read_text(encoding="utf-8").splitlines()[1:]]
wants = {
    "Wald 1943, plane vulnerability memo": [r"(?i)wald", r"(?i)vulnerab", r"(?i)damage of survivors"],
    "Galton 1886, regression towards mediocrity": [r"(?i)galton", r"(?i)mediocrity", r"(?i)hereditary stature"],
    "Condorcet 1785, Essai": [r"(?i)condorcet", r"(?i)pluralit"],
    "Arrow 1951, Social Choice and Individual Values": [r"(?i)arrow", r"(?i)social choice"],
}
for want, pats in wants.items():
    hit = [s for s in names + firsts for p in pats if re.search(p, s)]
    print(f"     {'HELD?' if hit else 'not found'}: {want}  ({len(pats)} patterns){'  -> ' + hit[0][:60] if hit else ''}")

# [5] placements
print("[5] placements named on the index")
for path, needle in (("book13/ch09-what-a-model-carries.html", "Beltrami"),
                     ("book18/index.html", "Chain Rule"),
                     ("book10/index.html", "Custody"),
                     ("book17/index.html", "variance_of_not_memLp")):
    p = ROOT / path
    check(f"{path} exists and mentions {needle}", p.exists() and needle in p.read_text(encoding="utf-8"))

print("""
[HONESTY]
This script establishes that the texts the index names are held, unchanged
since the ledger hashed them, and that the addresses and dataset figures the
index prints are what the files say today. It checks that four other pages
exist and carry one word each; it does not check that those pages do the job
the index assigns them.

It does not establish that a wanted source is absent. Block [4] searches
filenames and ledger first lines with a few patterns; a source under another
name, or inside a scanned PDF with no text layer, would not be found. 'not
found' means exactly that. And nothing here reads the chapters, which do not
exist yet.""")
print(f"\n{len(FAIL)} FAIL" + (": " + ", ".join(FAIL) if FAIL else ""))
sys.exit(1 if FAIL else 0)
