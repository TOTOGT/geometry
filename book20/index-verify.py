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
  [4] Wald 1943 and Galton 1886: ledger, hash, and the passages chs 1 and 4 rest on;
      Condorcet and Arrow, still wanted, searched for by several patterns
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

# [4] founding papers: held, in the ledger, and the passages the chapters rest on
print("[4] founding papers (Wald 1943, Galton 1886) and what is still wanted")
WA = "9-A method of estimating plane vulnerability ....pdf"
GA = "Galton85.pdf"
def pdfpages(name):
    try:
        t = subprocess.run(["pdftotext", "-layout", str(DL / name), "-"],
                           capture_output=True, text=True, check=True).stdout
        return t.split("\f")
    except (FileNotFoundError, subprocess.CalledProcessError, TypeError):
        return None
def foot(pg):  # Wald reprint folios are printed as "-63-" / "— 1—"
    ls = [l.strip() for l in pg.splitlines() if l.strip()]
    m = re.search(r"(\d+)", ls[-1]) if ls else None
    return int(m.group(1)) if m else None
def jhead(pg):  # Galton: the journal page number sits in the running head
    ls = [l.strip() for l in pg.splitlines() if l.strip()]
    m = re.match(r"^(\d{3})\b", ls[0]) or re.search(r"\b(\d{3})$", ls[0]) if ls else None
    return int(m.group(1)) if m else None
for name, pages_ in ((WA, "100"), (GA, "21")):
    r = rows.get(name)
    check(f"ledger row: {name[:40]}", r is not None and r[0] == pages_, f"pages {r[0] if r else None}")
    if r and DL and (DL / name).exists():
        check(f"file still hashes to ledger: {name[:40]}", sha(DL / name) == r[1], r[1][:16])
W = pdfpages(WA) if DL and (DL / WA).exists() else None
if W:
    parts = {}
    for i, pg in enumerate(W):
        m = re.search(r"(?m)^\s*PART\s+([IVX]+)\s*$", pg)
        if m and m.group(1) not in parts:
            parts[m.group(1)] = foot(pg)
    check("Wald: eight Parts, I-VIII", list(parts) == ["I","II","III","IV","V","VI","VII","VIII"], str(parts))
    check("Wald: Part I on p. 1, Part V (subdivision of the plane) on p. 56",
          parts.get("I") == 1 and parts.get("V") == 56, f"I {parts.get('I')}, V {parts.get('V')}")
    i1 = next((i for i, pg in enumerate(W) if re.search(r"SRG memo 85", pg)), None)
    check("Wald: Part I footnote names SRG memo 85 and AMP memo 76.1",
          i1 is not None and "AMP memo 76.1" in W[i1], f"PDF page {i1 + 1 if i1 is not None else None}")
    ie = next((i for i, pg in enumerate(W) if re.search(r"vulnerability of the engines, the fuselage, and the fuel system", re.sub(r"\s+", " ", pg))), None)
    check("Wald: the engines / fuselage / fuel-system worked example, p. 63",
          ie is not None and foot(W[ie]) == 63, f"PDF page {ie + 1 if ie is not None else None}, printed {foot(W[ie]) if ie is not None else None}")
    ir = next((i for i, pg in enumerate(W) if "for the observed data of this hypothetical example, the engine area is the most vulnerable" in re.sub(r"\s+", " ", pg)), None)
    fl = re.sub(r"\s+", " ", W[ir]) if ir is not None else ""
    check("Wald: in the HYPOTHETICAL example the engines are most vulnerable, p. 65",
          ir is not None and foot(W[ir]) == 65 and "Engines .61 .39" in fl and "Fuselage .95 .05" in fl,
          f"PDF page {ir + 1 if ir is not None else None}; engines downed by one hit .39, fuselage .05")
    ia = next((i for i, pg in enumerate(W) if "guides for locating protective armor" in re.sub(r"\s+", " ", pg)), None)
    check("Wald: 'guides for locating protective armor', the only place armor is named",
          ia is not None and [i for i, pg in enumerate(W) if re.search(r"(?i)armou?r", pg)] == [ia],
          f"PDF page {ia + 1 if ia is not None else None}, printed {foot(W[ia]) if ia is not None else None}")
    iy = next((i for i, pg in enumerate(W) if re.search(r"Reprint\s*-\s*1943", pg)), None)
    check("Wald: report form dates the memoranda 1943", iy is not None, f"PDF page {iy + 1 if iy is not None else None}")
G = pdfpages(GA) if DL and (DL / GA).exists() else None
if G:
    flat = [re.sub(r"\s+", " ", pg) for pg in G]
    ig = next((i for i, pg in enumerate(flat) if "two-thirds of the height-deviate of its mid-parentage" in pg), None)
    check("Galton: the law of regression, 'two-thirds of the height-deviate of its mid-parentage', p. 252",
          ig is not None and jhead(G[ig]) == 252, f"PDF page {ig + 1 if ig is not None else None}, journal page {jhead(G[ig]) if ig is not None else None}")
    check("Galton: J. Anthropological Institute 15 (1886), pp. 246-263",
          "Vol. 15 (1886), pp. 246-263" in flat[0], flat[0][flat[0].find("Source"):][:90])
    heads = [jhead(pg) for pg in G]
    check("Galton: journal pages 246 and 263 both present", 246 in heads and 263 in heads)
names = [p.name for p in DL.iterdir()] if DL else []
firsts = [l.split("\t")[5] if len(l.split("\t")) > 5 else ""
          for l in (ROOT / "docs/floor-texts.tsv").read_text(encoding="utf-8").splitlines()[1:]]
for want, pats in {"Condorcet 1785, Essai": [r"(?i)condorcet", r"(?i)pluralit"],
                   "Arrow 1951, Social Choice and Individual Values": [r"(?i)\barrow\b", r"(?i)social choice"]}.items():
    hit = [x for x in names + firsts for p in pats if re.search(p, x)]
    print(f"     {'HELD?' if hit else 'not found'}: {want}  ({len(pats)} patterns){'  -> ' + hit[0][:60] if hit else ''}")


# [4b] social choice sources, for the chapter placed in Book X (55 states, one voice)
print("[4b] social choice sources for Book X")
SC = {  # file -> (sha256, pages); short papers sit under floor_texts.py's 12-page floor, so hashed here
    "Condorcet1785_ProbabiliteDecisions.pdf": ("775d898573e3401a448f4537b5be3d0638cb0a1e1196cc74b2a5b10f2efed2fa", 197),
    "ArrowProof3.pdf": ("4e7665926a30838639e798e581ee45131566420837db7750c2fd26cfd3c2db41", 6),
    "DP417.pdf": ("0743b37fb2a6292c3f264154a7128587d8d0039ab8b6e03253c7f76ad21a7672", 39),
    "the_pre-history_of_kenneth_arrows_social_choice_and_individual_values_406.pdf":
        ("1b9880ebbb51be71499d357bd9ac8b9743bde6add59414e8076b8a3b0e94fe07", 8),
}
for name, (h, n) in SC.items():
    if DL and (DL / name).exists():
        check(f"held, unchanged: {name[:44]}", sha(DL / name) == h, h[:16])
    else:
        check(f"held: {name[:44]}", False, "not found in Downloads")
F = pdfpages("ArrowProof3.pdf") if DL and (DL / "ArrowProof3.pdf").exists() else None
if F:
    fl = [re.sub(r"\s+", " ", x) for x in F]
    check("Fey 2014: theorem stated on p. 2 (Unanimity + IIA => a dictator)",
          "If a social preference function satisfies Unanimity and IIA, then some indi- vidual is a dictator" in fl[1])
    check("Fey 2014: fully general -- weak orders, any finite N, at least three alternatives",
          "at least three alternatives" in fl[1] and "weak orders" in fl[1])
S = pdfpages("DP417.pdf") if DL and (DL / "DP417.pdf").exists() else None
if S:
    fl = [re.sub(r"\s+", " ", x) for x in S]
    i = next((k for k, x in enumerate(fl) if "first extended illustration of the paradox of voting" in x), None)
    check("Suzumura 2001: Condorcet's first extended illustration concerns restrictions on commerce",
          i is not None and "restriction placed on commerce" in fl[i], f"PDF page {i + 1 if i is not None else None}")
    check("Suzumura 2001 cites Condorcet (1785, Discours preliminaire, p. clxxix) on Borda",
          any("Discours préliminaire, p.clxxix" in x for x in fl))
# Condorcet is a 1785 scan with no text layer. With --ocr, five pages are OCR'd and read.
# Offset read off the book: PDF page 185 carries the folio clxxix that Suzumura cites -> roman = PDF - 6.
if "--ocr" in sys.argv and DL and (DL / "Condorcet1785_ProbabiliteDecisions.pdf").exists():
    import tempfile
    def ocr(pg):
        with tempfile.TemporaryDirectory() as d:
            subprocess.run(["pdftoppm", "-f", str(pg), "-l", str(pg), "-r", "150", "-gray", "-png",
                            str(DL / "Condorcet1785_ProbabiliteDecisions.pdf"), f"{d}/i"], check=True)
            im = sorted(Path(d).glob("i*.png"))[0]
            return subprocess.run(["tesseract", str(im), "-", "-l", "eng"], capture_output=True, text=True).stdout
    try:
        C = {pg: re.sub(r"\s+", " ", ocr(pg)) for pg in (58, 60, 63, 64, 185)}
        check("Condorcet: offset -- PDF 185 is the 'imprimé en entier' page Suzumura cites as p. clxxix",
              "imprim" in C[185] and "Ouvrage" in C[185])
        check("Condorcet p. lii: the commerce example begins ('liberté du commerce')",
              "commerce" in C[58] and "loix générales" in C[58])
        check("Condorcet p. liv: the winning combination 'paroissoit avoir le moins de voix'",
              "moins de voix" in C[60])
        check("Condorcet p. lvii: three candidates, combination III -- any two propositions contradict the third",
              "de deux quelconques des trois" in C[63] and "contraire" in C[63])
        check("Condorcet p. lviii: 60 voters, 23 for A, 19 for B",
              "60 Votans" in C[64] and "23" in C[64] and "19" in C[64])
    except (FileNotFoundError, subprocess.CalledProcessError, IndexError) as e:
        print(f"SKIP Condorcet OCR: {e}")
else:
    print("SKIP Condorcet passages (run with --ocr; needs pdftoppm and tesseract, ~45 s)")
print("     not held: Arrow 1951 itself. Held instead: Fey's proof (2014), Suzumura's Handbook introduction")
print("     (2001), Suppes's history (2005). 'Proving Social Choice Possible' (Lawrence, preprint) is held")
print("     and deliberately not used: an unrefereed claim to overturn the theorem is not a source for it.")

# [4c] the IMO record behind the IMPA case (chapter 1). Snapshot read in a browser; the counts
# below are computed from it, never typed.
print("[4c] IMO record (book20/imo-snapshot.tsv)")
T = [l.split("\t") for l in (ROOT / "book20/imo-snapshot.tsv").read_text(encoding="utf-8").splitlines()
     if l and not l.startswith("#")][1:]
hdr = {l.split("\t")[0][2:]: l.split("\t")[2] for l in (ROOT / "book20/imo-snapshot.tsv").read_text(encoding="utf-8").splitlines() if l.startswith("# 19") or l.startswith("# BRA") or l.startswith("# 2026T")}
def rowsof(tag): return [r for r in T if r[0] == tag]
p87 = [r for r in rowsof("1987") if r[5] == "42"]
p81 = [r for r in rowsof("1981") if r[5] == "42"]
check("1987: perfect scores counted from the table", len(p87) == 22, f"{len(p87)} of {hdr.get('1987')} contestants")
check("1987: Teixeira and Ellenberg both 42", {"Ralph Costa Teixeira", "Jordan S. Ellenberg"} <= {r[1] for r in p87})
check("1981: Saldanha 42", "Nicolau Corçao Saldanha" in {r[1] for r in p81}, f"{len(p81)} perfect of {hdr.get('1981')}")
b42 = rowsof("BRA42")
check("Brazil: exactly two perfect scores 1979-2026", len(b42) == 2, ", ".join(r[1] for r in b42))
teix = [("1985", rowsof("TEIX1985")[0][5]), ("1986", rowsof("TEIX1986")[0][5]), ("1987", "42")]
check("Teixeira: 13 -> 37 -> 42 over three IMOs", [t[1] for t in teix] == ["13", "37", "42"])
b26 = rowsof("BRA2026"); aw = [r[4] for r in b26]
check("Brazil 2026: five silver, one bronze", aw.count("S") == 5 and aw.count("B") == 1 and len(b26) == 6)
t26 = {r[1]: r for r in rowsof("TEAM2026")}
check("Brazil 2026: team rank 11 of 117", t26["BRA"][3] == "11" and hdr.get("2026T") == "117", f"rank {t26['BRA'][3]}, teams {hdr.get('2026T')}")

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

Block [4] reads OCR text layers: Wald's reprint is a 2003 scan and its
front matter is garbled, so only passages the script found verbatim are
printed on the index. It does not establish that a wanted source is absent: it searches
filenames and ledger first lines with a few patterns; a source under another
name, or inside a scanned PDF with no text layer, would not be found. 'not
found' means exactly that. And nothing here reads the chapters, which do not
exist yet.""")
print(f"\n{len(FAIL)} FAIL" + (": " + ", ".join(FAIL) if FAIL else ""))
sys.exit(1 if FAIL else 0)
