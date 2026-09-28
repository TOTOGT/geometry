#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book14/ch02-verify.py -- every number and quotation on book14/ch02-how-mathematical-prose-parses.html. Run first (R24).
    python3 book14/ch02-verify.py [--downloads DIR]
  [1] the six sources say what the page quotes (Tanswell & Inglis 2023; Arambillete & de Groote 2025;
      Balkir 2014; Corneli et al. 2017; Orth 2013; Fatima, FIRMA)
  [2] proofs as recipes: Tanswell & Inglis's Table 3 imperatives, re-counted per million words in
      this corpus's prose (pinned commit)
  [3] 'orthogonal' as a collective predicate: how the series writes its own title word
  [4] ambiguity as entropy: the operator keys' gloss distributions (Key Register) in bits
  [5] FIRMA's percentages, turned back into the baselines they imply
  [6] the Lean: book14/Collective.lean
  [HONESTY]
"""
import html, math, os, re, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
PIN = "7a471e3"
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def dl():
    if "--downloads" in sys.argv: return Path(sys.argv[sys.argv.index("--downloads") + 1])
    for c in ("~/mnt/Downloads", "~/Downloads"):
        p = Path(os.path.expanduser(c))
        if p.is_dir(): return p
D = dl()
norm = lambda s: re.sub(r"\s+", " ", s.replace("’", "'").replace("“", '"').replace("”", '"').replace("‘", "'")).strip()
def pdf(name, *opt): return norm(subprocess.run(["pdftotext", *opt, str(D / name), "-"], stdout=subprocess.PIPE,
                                          stderr=subprocess.DEVNULL, text=True).stdout)
def git(*a): return subprocess.run(["git", "--no-optional-locks", "-C", str(ROOT), *a],
                                   capture_output=True, text=True, errors="ignore").stdout

print("[1] the sources")
TI = pdf("Tanswell and Inglis (2023) The Language of Proofs A Corpus Linguistic Study.pdf")
AG = pdf("On the use of binary relations as collective predicates in natural mathematics.pdf")
BA = pdf("Using Density Matrices in a Compositional Distributional Model of Meaning.pdf")
CO = pdf("ni17003.pdf")
OR = pdf("Mathematics Orality and Literacy.pdf")
FI = pdf("FIRMA- Bidirectional Formal-Informal Mathematical Language Alignment with Proof-Theoretic Grounding.pdf")
for src, name, q in [
    (TI, "Tanswell & Inglis", "we argue in favour of the recipe model of proofs: that proofs are like recipes, giving instructions for mathematical actions to be carried out"),
    (TI, "Tanswell & Inglis", "the total frequency per million words for our selected verbs is 9406 in the Proof-Only corpus and 6854 in the Non-Proof corpus"),
    (AG, "Arambillete & de Groote", "Every set of prime numbers is a fortiori a set of coprime numbers. Therefore, every prime number is a coprime number"),
    (AG, "Arambillete & de Groote", "coprime is a collective predicate"),
    (BA, "Balkır", "words are represented by mixed states and each eigenstate represents a sense of the word"),
    (CO, "Corneli et al.", "we encode representations in a higherorder nested semantic network"),
    (OR, "Orth", "Much like learning a foreign language, learning mathematics has been based mostly on oral tradition"),
    (FI, "FIRMA", "FIRMA achieves an overall score of 0.304, representing a 277.8% improvement over BFS-Prover-V1-7B and a 6307.5% improvement over REAL-Prover")]:
    check(f'{name}: "{q[:58]}..."', norm(q) in src)
TIL = pdf("Tanswell and Inglis (2023) The Language of Proofs A Corpus Linguistic Study.pdf", "-layout")   # tables keep their rows
TABLE3 = {"Let": (4523, 4035), "Suppose": (944, 512), "Note": (929, 681), "Consider": (570, 314), "Assume": (556, 339),
          "Recall": (304, 265), "Define": (272, 167), "Fix": (255, 106), "Denote": (218, 145), "Observe": (213, 92),
          "Choose": (199, 45), "Take": (178, 49), "Write": (117, 39)}
check("Tanswell & Inglis Table 3: the thirteen verbs and their per-million rates",
      all(re.search(rf"{v} {a} {b}\b", TIL) for v, (a, b) in TABLE3.items()))

print(f"[2] proofs as recipes: the thirteen imperatives in this corpus (prose only, {PIN})")
RETIRED = ("docs/ml-evidence/", "_archive/", "_to_delete/")
pages = [f for f in git("ls-tree", "-r", "--name-only", PIN).split() if f.endswith(".html") and not f.startswith(RETIRED)]
GEN = re.compile(r"<!--po-(run|gss|related|subject)-->.*?<!--/po-\1-->", re.S)
STY = re.compile(r"<(style|script|pre|code)\b.*?</\1>", re.S | re.I)
MATH = re.compile(r"\$\$.+?\$\$|\\\[.+?\\\]|\\\(.+?\\\)|\$[^$\n]{1,400}?\$", re.S)
def prose(src): return re.sub(r"\s+", " ", MATH.sub(" ", html.unescape(re.sub(r"<[^>]+>", " ", STY.sub(" ", GEN.sub(" ", src))))))
T = {f: prose(git("show", f"{PIN}:{f}")) for f in pages}
words = sum(len(re.findall(r"[A-Za-z]+", t)) for t in T.values())
ours = {v: sum(len(re.findall(rf"(?:^|[.!?:]\s+){v}\b", t)) for t in T.values()) for v in TABLE3}
pm = {v: 1e6 * n / words for v, n in ours.items()}
print(f"     {len(pages)} pages, {words:,} words of prose")
print(f"     {'verb':9} {'here':>6} {'per M':>7} | T&I proof  non-proof")
for v in TABLE3: print(f"     {v:9} {ours[v]:6} {pm[v]:7.1f} | {TABLE3[v][0]:9} {TABLE3[v][1]:9}")
tot = sum(pm.values())
print(f"     total per million: here {tot:.0f}; T&I proof-only 9406, non-proof 6854")
top = max(pm, key=pm.get)
EXPECT = dict(words=1392322, total=247, top="Write")       # frozen from the first run at PIN
RES = dict(words=words, total=round(tot), top=top)
print("     RESULT", RES)
for k, v in EXPECT.items():
    if v is not None: check(f"{k} = {v}", RES[k] == v, str(RES[k]))
check("this corpus uses about 38x fewer of the thirteen imperatives than arXiv proofs", 30 < 9406 / tot < 45, f"{9406/tot:.1f}x")
check("its top imperative is 'Write' (course instructions), not 'Let'", top == "Write" and pm["Write"] > pm["Let"])

print("[3] 'orthogonal' as a collective predicate")
O = {k: sum(len(re.findall(rx, t)) for t in T.values()) for k, rx in [
    ("are orthogonal", r"\bare orthogonal\b(?! to)"), ("pairwise orthogonal", r"\bpairwise orthogonal\b"),
    ("mutually orthogonal", r"\bmutually orthogonal\b"), ("orthogonal to", r"\borthogonal to\b"),
    ("is orthogonal", r"\bis orthogonal\b")]}
for k, v in O.items(): print(f"     {k:20} {v:5}")
EXPECT_O = {"are orthogonal": 11, "pairwise orthogonal": 0, "mutually orthogonal": 6, "orthogonal to": 9, "is orthogonal": 35}
if EXPECT_O is not None: check(f"orthogonal counts = {EXPECT_O}", O == EXPECT_O, str(O))
check("the plural collective form ('are orthogonal') is written more often than its explicit pairwise forms",
      O["are orthogonal"] > O["pairwise orthogonal"] + O["mutually orthogonal"])

print("[4] ambiguity as entropy (Key Register at the pinned commit)")
reg = [l.split("\t") for l in git("show", f"{PIN}:docs/key-register.tsv").splitlines()[1:] if l.strip()]
H = {}
for L in "CKFU":
    n = [int(r[2]) for r in reg if r[0] == L]
    tot_ = sum(n); H[L] = -sum(k / tot_ * math.log2(k / tot_) for k in n if k)
    print(f"     {L}: glosses {n}  entropy {H[L]:.3f} bits")
check("F carries 0 bits: one gloss", H["F"] == 0)
check("over glosses, K is the most spread (1.369 bits) and U only 0.956",
      {k: round(v, 3) for k, v in H.items()} == {"C": 0.746, "K": 1.369, "F": 0.0, "U": 0.956})
# over SENSES: glosses in one component (Book XIV ch 3's chain rule) are one sense
HS = {}
for L in "CKFU":
    comp = {}
    for r in reg:
        if r[0] == L: comp[r[3]] = comp.get(r[3], 0) + int(r[2])
    n = list(comp.values()); t_ = sum(n)
    HS[L] = -sum(k / t_ * math.log2(k / t_) for k in n if k)
    print(f"     {L}: senses {n}  entropy {HS[L]:.3f} bits")
check("over senses only U is ambiguous: C, K, F carry 0 bits", HS["C"] == HS["K"] == HS["F"] == 0 and HS["U"] > 0,
      f"U {HS['U']:.3f}")

print("[5] FIRMA's percentages, as baselines")
b1, b2 = 0.304 / (1 + 2.778), 0.304 / (1 + 63.075)
print(f"     implied scores: BFS-Prover-V1-7B {b1:.3f}, REAL-Prover {b2:.4f}; FIRMA 0.304 (of 1)")
check("a 6307.5% improvement on a 0.304 score means the baseline scored under 0.005", b2 < 0.005)

print("[6] the Lean")
lean = (ROOT / "book14/Collective.lean").read_text(encoding="utf-8")
for t in ["primes_pairwise_coprime", "four_is_coprime_distributively", "collective_mono", "orthogonal_not_transitive"]:
    check(f"Collective.lean proves {t}", f"theorem {t}" in lean and f"#print axioms Collective.{t}" in lean)
check("no sorry in code", "sorry" not in re.sub(r"/-.*?-/|--[^\n]*", "", lean, flags=re.S))

print("[HONESTY]")
print("  [2] counts capitalised verbs after a sentence break in prose with formulas and code removed;")
print("  T&I used a proof/non-proof split of arXiv, which this corpus does not have, so the comparison")
print("  is of rates, not of like with like. [4] reads each gloss as an orthogonal pure state, so the")
print("  von Neumann entropy equals the Shannon entropy of the gloss counts; that reading is ours (MODEL).")
print("  FIRMA's scores are its author's, unreplicated here. Orth 2013 is an unpublished essay.")
print(f"\n{len(FAIL)} FAIL" + (": " + ", ".join(FAIL) if FAIL else ""))
sys.exit(1 if FAIL else 0)
