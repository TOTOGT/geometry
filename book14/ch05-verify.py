#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book14/ch05-verify.py -- every number and quotation on book14/ch05-the-machines-that-read-us.html. Run first (R24).
    python3 book14/ch05-verify.py [--downloads DIR]
  [1] Jurafsky & Martin, Speech and Language Processing, 3rd ed. draft of 19 Aug 2026: the sentences
      the page quotes, on the printed pages it cites (printed = PDF - 8)
  [2] can the subject tags be learned from the text? Multinomial naive Bayes and tf-idf cosine
      nearest-neighbour, 10-fold, against the majority-class baseline (J&M's accuracy trap)
  [3] per-field precision, recall and F1 for the better classifier
  Standard library only. The corpus is pinned (git show at PIN) so the numbers do not drift.
  [HONESTY]
"""
import csv, html, io, math, os, re, subprocess, sys, zlib
from collections import Counter, defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
PIN = "07c785b"
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def git(*a): return subprocess.run(["git", "--no-optional-locks", "-C", str(ROOT), *a],
                                   capture_output=True, text=True, errors="ignore").stdout
def dl():
    if "--downloads" in sys.argv: return Path(sys.argv[sys.argv.index("--downloads") + 1])
    for c in ("~/mnt/Downloads", "~/Downloads"):
        p = Path(os.path.expanduser(c))
        if p.is_dir(): return p

print("[1] Jurafsky & Martin, 3rd ed. draft (19 Aug 2026)")
pdf = dl() / "ed3book_aug26.pdf"
pages = subprocess.run(["pdftotext", str(pdf), "-"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                       text=True).stdout.split("\f")
norm = lambda s: re.sub(r"\s+", " ", s.replace("’", "'").replace("—", "--")).strip()
check("held: the draft dated August 19, 2026", "Draft of August 19, 2026" in pages[0], str(len(pages)))
OFF = 8
for pr in (34, 93, 113, 135, 476):   # 33 and 92 open chapters and carry no folio; their neighbours anchor them
    check(f"printed p.{pr} is PDF p.{pr + OFF}", re.search(rf"(^|\s){pr}\s*$|^\s*{pr}\s", pages[pr + OFF - 1].strip(), re.M) is not None)
Q = [(33, "All tokenization systems also depend on regular expressions as a processing step"),
     (92, "the task of assigning a label or category to a text or document"),
     (113, "Imagine a simple classifier that stupidly classified every tweet"),
     (135, "The dot product acts as a similarity metric"),
     (476, "The earliest and still common algorithm for relation extraction is lexico-syntactic patterns")]
for pr, q in Q:
    check(f'p.{pr}: "{q[:58]}..."', norm(q) in norm(pages[pr + OFF - 1]))

print(f"[2] the subject tags as a classification task (corpus at {PIN})")
rows = list(csv.reader(io.StringIO(git("show", f"{PIN}:docs/subjects.tsv")), delimiter="\t"))
lab = {r[0]: r[1].split(" · ")[0].strip() for r in rows if len(r) >= 2 and r[0].endswith(".html") and not r[0].startswith("#")}
GEN = re.compile(r"<!--po-(run|gss|related|subject)-->.*?<!--/po-\1-->", re.S)
STY = re.compile(r"<(style|script)\b.*?</\1>", re.S | re.I)
META = re.compile(r'<meta name="po-subject"[^>]*>', re.I)
def tokens(f):
    t = git("show", f"{PIN}:{f}")
    t = html.unescape(re.sub(r"<[^>]+>", " ", STY.sub(" ", GEN.sub(" ", META.sub(" ", t)))))
    return [w for w in re.findall(r"[a-zà-ÿ]{3,}", t.lower())]
docs = {f: tokens(f) for f in sorted(lab)}
docs = {f: d for f, d in docs.items() if len(d) >= 50}
fields = Counter(lab[f] for f in docs)
keep = {k for k, v in fields.items() if v >= 10}          # fields with too few pages are not learnable
docs = {f: d for f, d in docs.items() if lab[f] in keep}
Y = {f: lab[f] for f in docs}
N = len(docs)
print(f"     {N} tagged pages in {len(keep)} fields with >= 10 pages: " +
      ", ".join(f"{k.lower()} {v}" for k, v in Counter(Y.values()).most_common()))
fold = {f: zlib.crc32(f.encode()) % 10 for f in docs}      # deterministic 10-fold split

def nb(train, test):
    prior, cnt, tot, V = Counter(), defaultdict(Counter), Counter(), set()
    for f in train:
        c = Y[f]; prior[c] += 1; cnt[c].update(docs[f]); tot[c] += len(docs[f]); V.update(docs[f])
    out = {}
    for f in test:
        tf = Counter(docs[f])
        best = max(prior, key=lambda c: math.log(prior[c]) + sum(n * math.log((cnt[c][w] + 1) / (tot[c] + len(V)))
                                                                  for w, n in tf.items() if w in V))
        out[f] = best
    return out

def knn(train, test):
    df = Counter(); [df.update(set(docs[f])) for f in train]
    n = len(train)
    def vec(f):
        tf = Counter(docs[f])
        v = {w: (1 + math.log(c)) * math.log(n / df[w]) for w, c in tf.items() if df.get(w)}
        z = math.sqrt(sum(x * x for x in v.values())) or 1
        return {w: x / z for w, x in v.items()}
    TV = {f: vec(f) for f in train}
    out = {}
    for f in test:
        q = vec(f)
        best = max(train, key=lambda g: sum(x * TV[g].get(w, 0) for w, x in q.items()))
        out[f] = Y[best]
    return out

def cv(model):
    pred = {}
    for k in range(10):
        train = [f for f in docs if fold[f] != k]; test = [f for f in docs if fold[f] == k]
        pred.update(model(train, test))
    return pred
major = Counter(Y.values()).most_common(1)[0]
base = major[1] / N
P_nb, P_knn = cv(nb), cv(knn)
acc = lambda P: sum(P[f] == Y[f] for f in docs) / N
a_nb, a_knn = acc(P_nb), acc(P_knn)
check("the majority baseline is mathematics", major[0] == "MATHEMATICS")
print(f"     majority baseline (always {major[0].lower()}): {base:.3f}")
print(f"     naive Bayes, 10-fold:                  {a_nb:.3f}")
print(f"     tf-idf cosine 1-nearest-neighbour:      {a_knn:.3f}")
check("both classifiers beat the majority baseline", a_nb > base and a_knn > base)

print("[3] per field, naive Bayes (precision / recall / F1)")
f1s = {}
for c in sorted(keep, key=lambda c: -fields[c]):
    tp = sum(P_nb[f] == c and Y[f] == c for f in docs); fp = sum(P_nb[f] == c and Y[f] != c for f in docs)
    fn = sum(P_nb[f] != c and Y[f] == c for f in docs)
    p = tp / (tp + fp) if tp + fp else 0; r = tp / (tp + fn) if tp + fn else 0
    f1s[c] = 2 * p * r / (p + r) if p + r else 0
    print(f"     {c.lower():12} n={sum(Y[f] == c for f in docs):3}  P {p:.2f}  R {r:.2f}  F1 {f1s[c]:.2f}")
macro = sum(f1s.values()) / len(f1s)
print(f"     macro-F1 {macro:.3f}")
conf = Counter((Y[f], P_nb[f]) for f in docs if P_nb[f] != Y[f])
print("     most common confusions (gold -> predicted):", [(a.lower(), b.lower(), n) for (a, b), n in conf.most_common(4)])

EXPECT = dict(N=472, base=0.453, nb=0.663, knn=0.684, macro=0.391)   # frozen from the first run at PIN
RESULT = dict(N=N, base=round(base, 3), nb=round(a_nb, 3), knn=round(a_knn, 3), macro=round(macro, 3))
print("     RESULT", RESULT)
for k, v in EXPECT.items():
    if v is not None: check(f"{k} = {v}", RESULT[k] == v, str(RESULT[k]))

print("[HONESTY]")
print("  The tags are an editor's decisions, not ground truth about the pages; 'accuracy' here means")
print("  agreement with those decisions. Fields with fewer than 10 pages are left out. Tokens are")
print("  lower-cased letter runs of 3+; no stemming, no stop list. One deterministic 10-fold split.")
print(f"\n{len(FAIL)} FAIL" + (": " + ", ".join(FAIL) if FAIL else ""))
sys.exit(1 if FAIL else 0)
