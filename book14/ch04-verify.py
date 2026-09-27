#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book14/ch04-verify.py -- every number on book14/ch04-holology-as-a-vocabulary.html. Run first (R24).
    python3 book14/ch04-verify.py [--downloads DIR]
  [1] how the operator letters C, K, F, U are glossed across the published pages, at a pinned commit
      ("U — Unfolding", "K: threshold", "U = Union" ...), with Portuguese glosses merged into their English sense
  [2] Chapter 3's test applied to the series itself: senses of one letter joined by a page that uses both
      form one sense (connected components); senses never joined are separate senses
  [3] the GCM Institutional Edition's unified lexicon (Appendix A): which letters it defines
  [4] 'holology': pages that use the word, and how many define it
  [HONESTY]
"""
import html, os, re, subprocess, sys, zipfile
from collections import defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
PIN = "f9e830e"   # the corpus as this chapter was written
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def git(*a): return subprocess.run(["git", "--no-optional-locks", "-C", str(ROOT), *a], capture_output=True, text=True, errors="ignore").stdout
RETIRED = ("docs/ml-evidence/", "_archive/", "_to_delete/")
pages = [f for f in git("ls-tree", "-r", "--name-only", PIN).split() if f.endswith(".html") and not f.startswith(RETIRED)]
GEN = re.compile(r"<!--po-(run|gss|related|subject)-->.*?<!--/po-\1-->", re.S)
STY = re.compile(r"<(style|script)\b.*?</\1>", re.S | re.I)
TAG = re.compile(r"<[^>]+>")
def text(f): return re.sub(r"\s+", " ", html.unescape(TAG.sub(" ", STY.sub(" ", GEN.sub(" ", git("show", f"{PIN}:{f}"))))))
T = {f: text(f) for f in pages}
print(f"[0] {len(pages)} published pages at {PIN} (retired folders excluded)")

SENSES = {
 "C": {"compression": ["compression", "compress", "compressão"], "contact": ["contact"]},
 "K": {"threshold": ["threshold", "limiar"], "curvature": ["curvature", "curvatura"], "gate": ["gate", "portão"]},
 "F": {"fold": ["fold", "folding", "dobramento", "dobra"]},
 "U": {"unfolding": ["unfolding", "unfold", "desdobramento"], "union": ["union", "união"],
       "universal": ["universal"], "unification": ["unification", "unificação"]},
}
print("[1] glosses: a letter, then — – - = : or (, then the gloss word")
use = {L: defaultdict(set) for L in SENSES}
for L, senses in SENSES.items():
    word = {w: s for s, ws in senses.items() for w in ws}
    rx = re.compile(r"(?<![A-Za-z0-9_])" + L + r"\s*(?:—|–|-|=|:|\()\s*(?i:the\s+|a\s+|o\s+)?([A-Za-zçãõéêíóúàÀ-Ú]+)")   # letter case-sensitive
    for f, t in T.items():
        for m in rx.finditer(t):
            s = word.get(m.group(1).lower())
            if s: use[L][s].add(f)
    print(f"     {L}: " + ", ".join(f"{s} {len(use[L][s])}" for s in senses))
N = {L: {s: len(v) for s, v in use[L].items()} for L in use}
check("U is glossed four ways: unfolding 68, union 10, universal 3, unification 3",
      N["U"] == {"unfolding": 68, "union": 10, "universal": 3, "unification": 3}, str(N["U"]))
check("K is glossed threshold 50, curvature 26, gate 12", N["K"] == {"threshold": 50, "curvature": 26, "gate": 12}, str(N["K"]))
check("C is glossed compression 63, contact 17", N["C"] == {"compression": 63, "contact": 17}, str(N["C"]))
check("F has one gloss, fold, on 86 pages", N["F"] == {"fold": 86}, str(N["F"]))

print("[2] Chapter 3's test, on the series' own letters")
def components(L):
    ss = [s for s in SENSES[L] if use[L][s]]
    parent = {s: s for s in ss}
    def find(x):
        while parent[x] != x: x = parent[x]
        return x
    joins = []
    for i, a in enumerate(ss):
        for b in ss[i + 1:]:
            both = use[L][a] & use[L][b]
            if both:
                joins.append((a, b, sorted(both))); parent[find(a)] = find(b)
    comps = defaultdict(list)
    for s in ss: comps[find(s)].append(s)
    return list(comps.values()), joins
R = {}
for L in SENSES:
    comps, joins = components(L); R[L] = comps
    print(f"     {L}: {len(comps)} sense(s) {comps}")
    for a, b, fs in joins: print(f"        joined {a}~{b} on {len(fs)} page(s): {fs[:3]}")
check("U falls into 3 senses: {unfolding, universal}, {union}, {unification}",
      sorted(sorted(c) for c in R["U"]) == [["unfolding", "universal"], ["unification"], ["union"]], str(R["U"]))
check("K is one sense: threshold~curvature joined on 6 pages, threshold~gate on 4",
      len(R["K"]) == 1 and len(use["K"]["threshold"] & use["K"]["curvature"]) == 6 and len(use["K"]["threshold"] & use["K"]["gate"]) == 4)
check("C is one sense, joined on 2 pages", len(R["C"]) == 1 and len(use["C"]["compression"] & use["C"]["contact"]) == 2)

print("[3] the GCM Institutional Edition (2025), Appendix A")
def dl():
    if "--downloads" in sys.argv: return Path(sys.argv[sys.argv.index("--downloads") + 1])
    for c in ("~/mnt/Downloads", "~/Downloads"):
        p = Path(os.path.expanduser(c))
        if p.is_dir(): return p
g = dl() / "GCM-Institutional-Edition.docx"
x = zipfile.ZipFile(g).read("word/document.xml").decode("utf-8", "ignore")
gt = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", x.replace("</w:p>", "\n"))))
a0 = gt.rfind("Appendix A: Unified Lexicon")   # the first hit is the table of contents
app = gt[a0:gt.find("Appendix C", a0)]
ops = re.findall(r"([A-Z][a-z]+(?: [a-z]+)? (?:operator|vector field)) \((\w)\)", app)
print("     operators it defines:", ops)
check("GCM Appendix A defines U as the Unfolding operator", ("Unfolding operator", "U") in ops)
check("and defines no C, K or F", not any(l in ("C", "K", "F") for _, l in ops))

print("[4] holology")
hol = sorted(f for f, t in T.items() if re.search(r"\bholology\b", t, re.I))
defs = sorted(f for f, t in T.items() if re.search(r"\bholology\s*(?:=|—|:|is the|is a)\s", t, re.I))
print(f"     {len(hol)} pages use the word; {len(defs)} define it: {defs}")
check("holology: used on 20 pages, defined on 6", (len(hol), len(defs)) == (20, 6), f"{len(hol)}, {len(defs)}")
snips = [T[f][m.start():m.start() + 400].lower() for f in defs for m in [re.search(r"\bholology\s*(?:=|—|:|is the|is a)\s", T[f], re.I)]]
one = [f for f, x in zip(defs, snips) if any(w in x for w in ("whole", "totality", "global"))]
print(f"     definitions about the whole (whole / totality / global): {len(one)} of {len(defs)}")
check("every definition is about the whole (one sense)", len(one) == len(defs))
check("the paradigm: topology, topography, holography, holology all named on book8/ch12",
      all(w in T["book8/ch12-container.html"].lower() for w in ("topos", "holos", "logy", "graphy")))


print("[5] translation keys: does the domain choose the gloss, or the instantiation?")
import csv
from collections import Counter
subj = {}
for row in csv.reader(open(ROOT / "docs/subjects.tsv", encoding="utf-8"), delimiter="\t"):
    if len(row) >= 2: subj[row[0]] = row[1].split(" · ")[0]
for s_ in ("threshold", "curvature", "gate"):
    c = Counter(subj.get(f, "(untagged)") for f in use["K"][s_])
    print(f"     K {s_:10} " + ", ".join(f"{k} {v}" for k, v in c.most_common(5)))
th = Counter(subj.get(f) for f in use["K"]["threshold"])
check("'threshold' is not a domain word: 9 pages each in mathematics, physics and biology",
      (th["MATHEMATICS"], th["PHYSICS"], th["BIOLOGY"]) == (9, 9, 9))
cu = Counter(subj.get(f) for f in use["K"]["curvature"])
check("'curvature' leans to physics: 9 of its 21 tagged pages", cu["PHYSICS"] == 9 and sum(v for k, v in cu.items() if k) == 21)
INST = [("book7/ch-ada.html", "K: threshold k ≤ n−1 (loop control)", "computing"),
        ("ch-tatiana.html", "Operador K: portão de Heaviside em pH = 4.5", "chemistry"),
        ("book7/ch-kitagawa.html", "K: gate de camada limite", "atmosphere"),
        ("book7/wp59-dark-matter-lensing.html", "K — Curvature Lyapunov descent", "cosmology"),
        ("book8/ch8-6-voa.html", "K (Curvature): The Virasoro algebra", "algebra")]
for f, q, d in INST:
    check(f"instantiation, {d}: '{q}' ({f})", q in T.get(f, ""))
check("U = Union belongs to a second key set, G–L–R–U, on the series hub",
      "G = Genesis · L = Logos · R = Resonance · U = Union" in T["series-hub.html"])

print("[HONESTY]")
print("  The gloss pattern is a letter followed by a separator and a word; it misses glosses written")
print("  other ways and counts a page once per sense. Sense grouping (Portuguese with English, 'unfold'")
print("  with 'unfolding') is ours. A page using two glosses is taken as joining them, which is Chapter")
print("  3's co-predication test read loosely: using both is weaker evidence than saying both at once.")
print("  Five hits per sense were read by eye; one of five 'C — contact' hits was a course legend, not the operator.")
print(f"\n{len(FAIL)} FAIL" + (": " + ", ".join(FAIL) if FAIL else ""))
sys.exit(1 if FAIL else 0)
