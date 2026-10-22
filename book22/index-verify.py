#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book22/index-verify.py -- the Portuguese side of the Book XXII glossary against the source article. Run first (R24).
    python3 book22/index-verify.py [path/to/ROCHA&RIBEIRO.2025.1.pdf]
Source: Rocha & Ribeiro, (Con)Textos Linguisticos v.19 n.42, 2025, printed p. 163 (PDF page 3).
Needs pdftotext. Exits 2 with CANNOT RUN if the PDF is missing.
  [1] each recorded phrase is on PDF page 3 of the article
  [2] the index cites the article (authors, journal, year, p. 163) and says what it was and was not used for
  [3] the index gives PFOL as another name for PLA (the source's wording), not only as an analogue of ESOL
  [4] the index names PLNM as the umbrella term
  [5] controls
  [HONESTY] what this does not establish
"""
import re, os, sys, subprocess, shutil
from pathlib import Path
HERE = Path(__file__).resolve().parent
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def norm(t): return re.sub(r"\s+", " ", t)
def plain(t): return norm(re.sub(r"<[^>]+>", " ", t.replace("&nbsp;", " ")))
PHRASES = [
 "Língua Estrangeira (PLE) aponta para o aprendizado da língua por pessoas que vivem em países onde o português não é o idioma oficial",
 "Português como Língua Adicional (PLA) refere-se à inclusão do português no repertório linguístico de um falante cuja língua materna é outra",
 "também chamado de Português para Falantes de Outras Línguas (PFOL), especialmente em projetos de extensão universitária",
 "Português como Segunda Língua (PL2)",
 "uso do português como língua predominante no contexto social em que o falante está inserido",
 "Português como Língua de Herança (PLH) é aquele transmitido no seio familiar e comunitário fora do país de origem",
 "Português como Língua Não Materna (PLNM) por estar voltado a migrantes em situação de vulnerabilidade",
]
cands = [sys.argv[1]] if len(sys.argv) > 1 else []
cands += [os.environ.get("ROCHA_PDF", ""), str(Path.home() / "Downloads" / "ROCHA&RIBEIRO.2025.1.pdf"),
          str(Path.home() / "mnt" / "Downloads" / "ROCHA&RIBEIRO.2025.1.pdf")]
pdf = next((c for c in cands if c and Path(c).exists()), None)
if pdf is None or shutil.which("pdftotext") is None:
    print("CANNOT RUN: article PDF or pdftotext missing. Pass the PDF path or set ROCHA_PDF."); sys.exit(2)
page = norm(subprocess.run(["pdftotext", "-f", "3", "-l", "3", "-layout", pdf, "-"], capture_output=True, text=True).stdout)
idx = (HERE / "index.html").read_text(encoding="utf-8")
p = plain(idx)
print("[1] source phrases")
miss = [x for x in PHRASES if norm(x) not in page]
check(f"all {len(PHRASES)} recorded phrases are on PDF page 3", not miss, "; ".join(miss))
def cites_ok(t):
    q = plain(t)
    return all(w in q for w in ["Rocha", "Ribeiro", "(Con)Textos Lingu", "2025", "p. 163"]) and "only a secondary source" in q
def pfol_ok(t):
    q = plain(t)
    return "also called PFOL" in q
def plnm_ok(t):
    return "PLNM" in plain(t) and "Português como Língua Não Materna" in plain(t)
print("[2] citation and scope")
check("index cites Rocha & Ribeiro 2025, p. 163, and says it is only a secondary source", cites_ok(idx))
print("[3] PFOL")
check("index says PFOL is another name for PLA (source wording)", pfol_ok(idx))
print("[4] umbrella term")
check("index names PLNM, Português como Língua Não Materna", plnm_ok(idx))
print("[5] controls")
check("control: a changed phrase is caught", bool([x for x in [PHRASES[2].replace("PFOL", "PFOX")] if norm(x) not in page]))
check("control: citation removed is caught", not cites_ok(idx.replace("p. 163", "p. 1")))
check("control: PFOL wording removed is caught", not pfol_ok(idx.replace("also called PFOL", "")))
check("control: PLNM removed is caught", not plnm_ok(idx.replace("PLNM", "")))
def suggests_ok(t):
    q = plain(t)
    return ("What this book suggests you do" in q and "make mistakes" in q and "comedians" in q
            and "an opinion, not a finding" in q
            and "Zelensky" in q and "elected president of Ukraine in 2019" in q and "not evidence for the bet" in q)
print("[6] what the book suggests")
check("index has 'What this book suggests you do', says to make mistakes, and labels the comedians line an opinion", suggests_ok(idx))
check("control: opinion label removed is caught", not suggests_ok(idx.replace("an opinion, not a finding", "")))
check("control: Zelensky joke removed is caught", not suggests_ok(idx.replace("Zelensky", "")))
check("control: heading removed is caught", not suggests_ok(idx.replace("What this book suggests you do", "")))
print("[HONESTY] This checks the Portuguese terms against ONE article, which itself cites Fontana, Camargo and Nunes (2022) for them.")
print("  It does not check the English side (ESL, EFL, ELL, EAL, ENL/ELD/ESOL, World Languages), US law, or the Brazilian curricula claim.")
print("\nFAILED: " + ", ".join(FAIL) if FAIL else "\nALL PASS")
sys.exit(1 if FAIL else 0)
