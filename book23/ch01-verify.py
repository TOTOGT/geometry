#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book23/ch01-verify.py -- book23/ch01-the-22-days.html and index.html. Run first (R24).
    python3 book23/ch01-verify.py [path-to-CPI-report.pdf]
Needs the Senate CPI da Covid final report (Renan Calheiros) PDF and either `pdftotext` or `pypdf`.
If the PDF or a text extractor is missing the script says CANNOT RUN and exits 2: it never reports a pass without the PDF.
  [1] each CPI phrase quoted below is found on the PDF page the chapter cites
  [2] sixteen sections (B, D01..D23, X), each with English and Portuguese text
  [3] the page cites the CPI pages it relies on, and the book says it is unverified by the author where stated
  [4] the hashtag #CPIdaCOVID and the not-reviewed notice are on index.html
  [5] controls: a changed number, a removed phrase page, and a renamed section are all caught
  [HONESTY] what this does not establish
"""
import os, re, shutil, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def plain(t): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t))

NAME = "relatorio-final-renan-calheiros-cpi.pdf"
cands = [Path(sys.argv[1])] if len(sys.argv) > 1 else []
cands += [Path(os.environ["CPI_PDF"])] if os.environ.get("CPI_PDF") else []
cands += [Path.home()/"Downloads"/NAME, Path.home()/"mnt"/"Downloads"/NAME]
pdf = next((c for c in cands if c.exists()), None)

def page_text(n):
    if shutil.which("pdftotext"):
        r = subprocess.run(["pdftotext", "-f", str(n), "-l", str(n), "-layout", str(pdf), "-"], capture_output=True, text=True)
        return re.sub(r"\s+", " ", r.stdout)
    try:
        from pypdf import PdfReader
        return re.sub(r"\s+", " ", PdfReader(str(pdf)).pages[n-1].extract_text() or "")
    except Exception:
        return None

# (PDF page, phrase). PDF page = printed page + 1.
QUOTES = [
 (262, "revogou o Decreto em 27/12/2020"), (262, "Decreto estadual nº 43.234, de 23/12/2020"),
 (263, "qualquer embasamento técnico-científico"), (263, "a partir do dia 2 janeiro"), (263, "28 de dezembro de 2020"),
 (264, "apenas no dia 3 de janeiro de 2021"), (264, "Ofício nº 6672/20, de 30/12/2020"),
 (265, "dia 31 de dezembro"), (265, "em 10 dias"), (265, "89,1%"), (265, "orientações de intervenção precoce"),
 (266, "09 de janeiro de 2021, o Japão"),
 (267, "113.732 casos"), (267, "8 de janeiro de 2021 teve seu foco alterado"),
 (268, "09/01/2021"), (268, "preferindo não medir a saturação"), (268, "noite do dia 7 de janeiro"),
 (268, "150, no dia 8, e 200, no dia 10"), (268, "7h30 da manhã"),
 (270, "14 e 15 de janeiro de 2021"), (273, "por até 20 dias"), (273, "34 pacientes"), (273, "184 prontuários"),
 (274, "15 de janeiro de 2021"), (275, "25.000 m3/dia"),
 (277, "16 de julho de 2020"), (278, "9 de setembro de 2020"),
 (284, "nenhuma usina de oxigênio"), (285, "26 de dezembro de 2020"),
]
SECTIONS = ["B","D01","D04","D07","D08","D09","D12","D14","D15","D16","D19","D20","D21","D22","D23","X"]
CITED = ["p. 261", "p. 262", "p. 263", "p. 264", "p. 266", "p. 267", "p. 272", "p. 273", "p. 274", "p. 276", "p. 282", "p. 284"]

def missing(texts, quotes):
    return [f"p{pg}:{q}" for pg, q in quotes if q not in (texts.get(pg) or "")]
def sections_ok(text):
    got = {}
    for m in re.finditer(r'<div class="sec" data-n="([^"]+)">(.*?</div>)\s*</div>\s*(?=<div class="sec"|<!--end-secs-->)', text, re.S):
        body = m.group(2)
        en = re.search(r'<div lang="en">(.*?)</div>', body, re.S)
        pt = re.search(r'<div lang="pt">(.*?)</div>', body, re.S)
        got[m.group(1)] = bool(en and plain(en.group(1)).strip()) and bool(pt and plain(pt.group(1)).strip())
    return list(got) == SECTIONS and all(got.values())

if pdf is None:
    print("CANNOT RUN: CPI PDF not found. Pass its path, set CPI_PDF, or put it in ~/Downloads."); sys.exit(2)
pages = sorted({pg for pg, _ in QUOTES})
texts = {pg: page_text(pg) for pg in pages}
if any(v is None for v in texts.values()) or not any(texts.values()):
    print("CANNOT RUN: neither pdftotext nor pypdf could read the PDF."); sys.exit(2)
ch_p, ix_p = HERE/"ch01-the-22-days.html", HERE/"index.html"
ch = ch_p.read_text(encoding="utf-8") if ch_p.exists() else ""
ix = ix_p.read_text(encoding="utf-8") if ix_p.exists() else ""
print("[1] CPI quotes on their cited PDF pages")
miss = missing(texts, QUOTES)
check(f"all {len(QUOTES)} recorded phrases are on their PDF pages", not miss, ", ".join(miss))
print("[2] sections")
check("sixteen sections B, D01..D23, X each have EN and PT text", bool(ch) and sections_ok(ch))
print("[3] citations and labels")
pc = plain(ch)
cm = [c for c in CITED if c not in pc]
check("chapter cites the CPI pages it relies on", bool(ch) and not cm, ", ".join(cm))
check("chapter says press items are not independently checked", "not independently checked" in pc)
print("[4] hashtag")
pi = plain(ix)
check("index carries #CPIdaCOVID", "#CPIdaCOVID" in pi)
check("index says posts under the tag are not reviewed or endorsed", "does not collect, review, store or endorse" in pi)
print("[5] controls")
bad = [(pg, q.replace("43.234", "43.243")) for pg, q in QUOTES]
check("control: a changed decree number is caught", bool(missing(texts, bad)))
check("control: a phrase cited on the wrong page is caught", bool(missing(texts, [(277, "revogou o Decreto em 27/12/2020")])))
check("control: a renamed section is caught", bool(ch) and not sections_ok(ch.replace('data-n="D08"', 'data-n="D8"')))
check("control: a missing hashtag is caught", "#CPIdaCOVID" not in plain(ix.replace("#CPIdaCOVID", "")))
print("[HONESTY] This checks that the quoted phrases are on the cited pages of the report, that sections are aligned, and that labels are on.")
print("  It does not check press items (links only), the chart on p. 284, the Portuguese phrasing, or that the CPI's conclusions are right.")
print("  The report is the rapporteur's majority report; its findings are not court findings.")
print("\nFAILED: " + ", ".join(FAIL) if FAIL else "\nALL PASS")
sys.exit(1 if FAIL else 0)
