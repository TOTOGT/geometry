#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book10/ch09-verify.py -- every quoted passage, page number, and hash in
ch09-fifty-five-states-one-voice.html ("55 States, One Voice").

    python3 book10/ch09-verify.py [--downloads DIR] [--ocr]

Blocks
  [1] the four source PDFs are held, unchanged (sha256), at the hashes this
      corpus already recorded for them in book20/index-verify.py block [4b]
  [2] Fey (2014): the exact theorem statement, on the page the chapter cites
  [3] Suzumura (2001): the paradox description, the commerce-example
      propositions, and the Borda footnote (fn. 5, p.clxxix) the page-offset
      arithmetic in section 2's provenance box depends on
  [4] Suppes (2005): confirms the chapter's negative claim -- that this
      source never mentions Condorcet, voting, or the paradox by name, so
      treating it as a separate thread is not a convenient omission
  [5] with --ocr: the five Condorcet pages (58/lii, 60/liv, 63/lvii, 64/lviii,
      185/clxxix), OCR'd fresh, checked against the exact French the chapter
      quotes and against the PDF-to-roman offset the provenance box states
  [6] the chapter page itself: every open/not-held tag is actually on the
      page, and book10/index.html links the chapter
  [HONESTY]

Standard library, plus the `pdftotext` binary (poppler) for blocks [2]-[4],
and `pdftoppm` + `tesseract` for block [5] (SKIP unless run with --ocr).
"""
import hashlib
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
B10 = ROOT / "book10"
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


def pdfpages(path):
    try:
        t = subprocess.run(["pdftotext", "-layout", str(path), "-"],
                            capture_output=True, text=True, check=True).stdout
        return t.split("\f")
    except (FileNotFoundError, subprocess.CalledProcessError, TypeError):
        return None


DL = downloads()

# --------------------------------------------------------------------------
print("[1] the four held sources -- hashes, matching book20/index-verify.py [4b]")
# Same files, same hashes this corpus already recorded when it first confirmed
# them live this session. Repeated here, not re-typed from memory: any drift
# between this dict and book20's is itself a thing worth this script failing on.
SC = {
    "Condorcet1785_ProbabiliteDecisions.pdf":
        ("775d898573e3401a448f4537b5be3d0638cb0a1e1196cc74b2a5b10f2efed2fa", 197),
    "ArrowProof3.pdf":
        ("4e7665926a30838639e798e581ee45131566420837db7750c2fd26cfd3c2db41", 6),
    "DP417.pdf":
        ("0743b37fb2a6292c3f264154a7128587d8d0039ab8b6e03253c7f76ad21a7672", 39),
    "the_pre-history_of_kenneth_arrows_social_choice_and_individual_values_406.pdf":
        ("1b9880ebbb51be71499d357bd9ac8b9743bde6add59414e8076b8a3b0e94fe07", 8),
}
paths = {}
for name, (h, n) in SC.items():
    p = DL / name if DL else None
    if p and p.exists():
        paths[name] = p
        check(f"held, unchanged: {name[:44]}", sha(p) == h, h[:16])
    else:
        check(f"held: {name[:44]}", False, "not found in Downloads")

# --------------------------------------------------------------------------
print()
print("[2] Fey 2014: the theorem, stated exactly")
F = pdfpages(paths["ArrowProof3.pdf"]) if "ArrowProof3.pdf" in paths else None
if F:
    fl = [re.sub(r"\s+", " ", x) for x in F]
    check("theorem statement on p. 2: Unanimity + IIA => a dictator",
          "If a social preference function satisfies Unanimity and IIA, then some indi- vidual is a dictator" in fl[1])
    check("model is fully general: weak orders, >=3 alternatives",
          "at least three alternatives" in fl[1] and "weak orders" in fl[1])
    check("Unanimity is defined on p. 2 (not assumed by this chapter)",
          "Unanimity if for all" in fl[1])
    check("IIA is defined on p. 2 (not assumed by this chapter)",
          "Independence of Irrelevant Alternatives" in fl[1])
else:
    print("SKIP block [2]: ArrowProof3.pdf not reachable or pdftotext missing")

# --------------------------------------------------------------------------
print()
print("[3] Suzumura 2001: the paradox, the commerce propositions, the Borda footnote")
S = pdfpages(paths["DP417.pdf"]) if "DP417.pdf" in paths else None
if S:
    fl = [re.sub(r"\s+", " ", x) for x in S]
    i = next((k for k, x in enumerate(fl) if "may yield a social preference cycle" in x), None)
    check("the paradox is stated as a cycle (A beats B beats C beats A)",
          i is not None and "there exists no Condorcet winner" in fl[i],
          f"PDF page {i + 1 if i is not None else None}")
    j = next((k for k, x in enumerate(fl) if "first extended illustration of the paradox of voting" in x), None)
    check("Condorcet's first illustration is named as the commerce example",
          j is not None and "restriction placed on commerce" in fl[j],
          f"PDF page {j + 1 if j is not None else None}")
    check("the three commerce propositions (A, B, C) are quoted in full",
          all(s in "".join(fl) for s in (
              "any restriction placed on commerce is an injustice",
              "only those restrictions placed through general laws can be just",
              "restrictions placed by particular orders can be just")))
    k = next((x for x in fl if "Discours préliminaire, p.clxxix" in x), None)
    check("footnote 5 cites Condorcet 1785, Discours preliminaire, p.clxxix (the page-offset anchor)",
          k is not None, f"found: {'yes' if k else 'no'}")
else:
    print("SKIP block [3]: DP417.pdf not reachable or pdftotext missing")

# --------------------------------------------------------------------------
print()
print("[4] Suppes 2005: confirms the chapter's negative claim (separate thread)")
P = pdfpages(paths["the_pre-history_of_kenneth_arrows_social_choice_and_individual_values_406.pdf"]) \
    if "the_pre-history_of_kenneth_arrows_social_choice_and_individual_values_406.pdf" in paths else None
if P:
    flat = re.sub(r"\s+", " ", "".join(P))
    hits = [w for w in ("condorcet", "paradox of voting", "voting cycle") if w in flat.lower()]
    check("Suppes never names Condorcet, the voting paradox, or a voting cycle",
          not hits, f"found: {hits}" if hits else "confirmed absent")
    check("Suppes is genuinely about something else (ordinal utility / axiomatic method)",
          "ordinal utility" in flat.lower() or "axiomatic method" in flat.lower())
else:
    print("SKIP block [4]: Suppes PDF not reachable or pdftotext missing")

# --------------------------------------------------------------------------
print()
if "--ocr" in sys.argv and DL and (DL / "Condorcet1785_ProbabiliteDecisions.pdf").exists():
    print("[5] Condorcet, OCR'd fresh: the two examples and the page-offset anchor")

    def ocr(pg):
        with tempfile.TemporaryDirectory() as d:
            subprocess.run(["pdftoppm", "-f", str(pg), "-l", str(pg), "-r", "150", "-gray", "-png",
                             str(DL / "Condorcet1785_ProbabiliteDecisions.pdf"), f"{d}/i"], check=True)
            im = sorted(Path(d).glob("i*.png"))[0]
            return subprocess.run(["tesseract", str(im), "-", "-l", "eng"],
                                   capture_output=True, text=True).stdout

    try:
        C = {pg: re.sub(r"\s+", " ", ocr(pg)) for pg in (58, 60, 63, 64, 185)}
        check("offset anchor: PDF 185 carries the Borda 'imprime en entier' footnote (p.clxxix)",
              "imprim" in C[185] and "Ouvrage" in C[185])
        check("PDF 58 (p. lii): the commerce example, 'liberte du commerce'",
              "commerce" in C[58].lower() or "commence" in C[58].lower())
        check("PDF 60 (p. liv): the winning combination 'moins de voix'",
              "moins de voix" in C[60] or "moins de. voix" in C[60])
        check("PDF 63 (p. lvii): 'de deux quelconques des trois' -- the cycle condition",
              "de deux quelconques des trois" in C[63])
        check("PDF 64 (p. lviii): '60 Votans', 23/19/18 split",
              "60 Votans" in C[64] and "23" in C[64] and "19" in C[64] and "18" in C[64])
    except (FileNotFoundError, subprocess.CalledProcessError, IndexError) as e:
        print(f"SKIP block [5]: {e}")
else:
    print("SKIP block [5] (run with --ocr; needs pdftoppm and tesseract, ~45s)")

# --------------------------------------------------------------------------
print()
print("[6] the chapter page: open tags present, and it is linked from the volume")
CH = B10 / "ch09-fifty-five-states-one-voice.html"
if CH.exists():
    page = CH.read_text(encoding="utf-8")
    check("chapter file exists", True)
    check("Arrow (1951) is marked not held on the page, not silently assumed",
          "Arrow (1951)" in page and page.count('<span class="tag t-open">not held</span>') >= 2)
    check("AU/AfCFTA procedure is marked not examined, not silently assumed",
          "not examined" in page)
    check("the sixty-voter split (23/19/18) appears on the page",
          "23 en faveur de A" in page and "19 en faveur de B" in page and "18 en faveur de C" in page)
    check("the page-offset arithmetic (roman = PDF - 6) is stated, not hidden in this script alone",
          "roman = PDF" in page)
else:
    check("chapter file exists", False, str(CH))

IDX = B10 / "index.html"
if IDX.exists():
    itext = IDX.read_text(encoding="utf-8")
    check("book10/index.html links ch09", "ch09-fifty-five-states-one-voice.html" in itext)
else:
    check("book10/index.html exists", False)

# --------------------------------------------------------------------------
print()
print("=" * 68)
print("[HONESTY]")
print("""
ESTABLISHED. That the two theorems this chapter states are quoted and cited
correctly against the actual source files held for it, at the page numbers
given; that the page-offset arithmetic used to cite Condorcet's 1785 Essai
(a scan with no text layer) is anchored to a real, checkable footnote rather
than assumed; and that Suppes (2005) really does not mention Condorcet or
the voting paradox, so calling it a separate thread is not a convenient
omission.

NOT ESTABLISHED, and not claimed by the chapter either. That Arrow's 1951
book has been read -- it has not, and the page says so. That the African
Union's or AfCFTA's actual decision procedure has been examined against
either theorem -- it has not, and the page says so. That any real vote,
anywhere, has ever produced a Condorcet cycle or hit Arrow's impossibility.
Nothing in this script or the chapter it checks claims any of that.
""")
print("=" * 68)
if FAIL:
    print(f"{len(FAIL)} CHECK(S) FAILED")
    for f in FAIL:
        print("  - " + f)
    sys.exit(1)
print("ALL CHECKS PASSED")
