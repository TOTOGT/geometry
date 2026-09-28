#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book14/ch01-verify.py -- every number and quotation on book14/ch01-the-grammar-of-notation.html. Run first (R24).
    brew install tesseract poppler        # once: Chomsky 1957 is a scan with no text layer
    python3 book14/ch01-verify.py [--downloads DIR]
  [1] Chomsky, Syntactic Structures (2nd ed., 2002 printing): OCR of the three spreads the page
      quotes (scan n holds book pages 2n-18 and 2n-17)
  [2] Pullum (2011) and Jurafsky & Martin (2026 draft): the sentences quoted, by printed page
  [3] ambiguity: parse trees and distinct values of famous expressions under a grammar with
      no precedence conventions, and the Catalan growth of parses
  [4] the corpus's own formulas: how deep do their brackets nest? (SS §3.3), at a pinned commit
  [5] the Lean: book14/Brackets.lean proves SS fn 3 for brackets
  [HONESTY]
"""
import html, os, re, shutil, subprocess, sys, tempfile
from fractions import Fraction
from functools import lru_cache
from math import comb, sin
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
PIN = "eab9581"
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def dl():
    if "--downloads" in sys.argv: return Path(sys.argv[sys.argv.index("--downloads") + 1])
    for c in ("~/mnt/Downloads", "~/Downloads"):
        p = Path(os.path.expanduser(c))
        if p.is_dir(): return p
norm = lambda s: re.sub(r"\s+", " ", s.replace("’", "'").replace("“", '"').replace("”", '"')
                        .replace("‘", "'").replace("-\n", "")).strip()
D = dl()

print("[1] Chomsky, Syntactic Structures (Mouton de Gruyter, 2nd ed. 2002), OCR")
if not (shutil.which("tesseract") and shutil.which("pdftoppm")):
    print("  needs tesseract and pdftoppm:  brew install tesseract poppler"); sys.exit(2)
tmp = Path(tempfile.mkdtemp())
def ocr(scan):
    subprocess.run(["pdftoppm", "-r", "150", "-gray", "-png", "-f", str(scan), "-l", str(scan),
                    str(D / "Chomsky-1957.pdf"), str(tmp / f"s{scan}")], check=True)
    png = next(tmp.glob(f"s{scan}*.png"))
    return subprocess.run(["tesseract", str(png), "-"], capture_output=True, text=True).stdout
S = {n: norm(ocr(n).replace("-\n", "")) for n in (15, 19, 20)}
book = lambda n: (2 * n - 18, 2 * n - 17)
QS = [(15, 13, "the set of 'sentences' of some formalized system of mathematics can be considered a language"),
      (19, 20, "some language such as English or a formalized system of mathematics"),
      (19, 21, "English is not a finite state language"),
      (19, 21, "it is impossible, not just difficult, to construct a device"),
      (19, 21, "We can easily show that each of these three languages is not a finite state language"),
      (20, 22, "the set of well-formed formulas of any formalized system of mathematics or logic will fail to constitute a finite state language, because of paired parentheses or equivalent restrictions"),
      (20, 23, "This is a rough indication of the lines along which a rigorous proof of (9) can be given")]
for scan, pg, q in QS:
    check(f'SS p.{pg} (scan {scan} = pp.{book(scan)[0]}-{book(scan)[1]}): "{q[:52]}..."',
          pg in book(scan) and norm(q).lower() in S[scan].lower())
check("SS (10i) is aⁿbⁿ: 'n occurrences of a followed by n occurrences of b'",
      "n occurrences of a followed by n occurrences of b" in S[19])
check("SS §3.3: a bound on nesting would make it finite state ('less than a million words')",
      "less than a million words" in S[20])

print("[2] Pullum 2011; Jurafsky & Martin 2026 draft")
def pdf_pages(name):
    return subprocess.run(["pdftotext", str(D / name), "-"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                          text=True).stdout.split("\f")
PU = pdf_pages("PULLUM_2011_On_the_mathematics_of_syntactic_structures.pdf")
pu = norm(" ".join(PU))
for q in ["SS contains no proof that English is beyond the power of finite state description",
          "Chomsky did not even attempt such a proof in SS",
          "springs directly out of the work of the mathematical logician Emil Post"]:
    check(f'Pullum: "{q[:60]}..."', norm(q) in pu)
JM = pdf_pages("ed3book_aug26.pdf")
check("J&M p.425 (PDF 433): CFGs 'the backbone of many formal models of the syntax of natural language'",
      norm("Context-free grammars are the backbone of many formal models of the syntax of natural language") in norm(JM[432]))

print("[3] ambiguity without conventions: E -> E op E | E E | sin E | ( E ) | atom")
OPS = {"+": lambda a, b: a + b, "-": lambda a, b: a - b, "*": lambda a, b: a * b,
       "/": lambda a, b: a / b, "÷": lambda a, b: a / b, "^": lambda a, b: a ** b}
def tok(s): return re.findall(r"\d+|sin|[a-z]|[-+*/÷^()]", s)
def parses(ts, env):
    ts = tuple(ts)
    @lru_cache(None)
    def P(i, j):                      # list of (tree, value) for tokens i..j-1
        out = []
        if j - i == 1:
            t = ts[i]
            if t.isdigit(): out.append((t, Fraction(int(t))))
            elif t in env: out.append((t, env[t]))
            return out
        if ts[i] == "(" and ts[j - 1] == ")":
            out += [(f"({a})", v) for a, v in P(i + 1, j - 1)]
        if ts[i] == "sin":
            out += [(f"sin[{a}]", sin(v)) for a, v in P(i + 1, j)]
        for k in range(i + 1, j):
            if ts[k] in OPS:           # E op E
                for a, x in P(i, k):
                    for b, y in P(k + 1, j):
                        try: out.append((f"[{a}{ts[k]}{b}]", OPS[ts[k]](x, y)))
                        except (ZeroDivisionError, OverflowError): pass
            if ts[k - 1] not in OPS and ts[k] not in OPS and ts[k - 1] != "sin":   # juxtaposition E E
                for a, x in P(i, k):
                    for b, y in P(k, j):
                        out.append((f"[{a}·{b}]", x * y))
        return out
    return P(0, len(ts))
CASES = [("6÷2(1+2)", {}, 2, {Fraction(9), Fraction(1)}),
         ("1/2x", {"x": Fraction(3)}, 2, {Fraction(3, 2), Fraction(1, 6)}),
         ("sin x/2", {"x": Fraction(1)}, 2, None),
         ("2^3^2", {}, 2, {Fraction(64), Fraction(512)}),
         ("8/4/2", {}, 2, {Fraction(1), Fraction(4)})]
for expr, env, n, vals in CASES:
    ps = parses(tok(expr), env)
    vs = sorted({round(float(v), 6) for _, v in ps})
    print(f"     {expr:10} {len(ps)} parses: " + "; ".join(f"{t} = {float(v):g}" for t, v in ps))
    check(f"'{expr}' has {n} parses and {len(vs)} distinct values", len(ps) == n and len(vs) == n
          and (vals is None or {v for _, v in ps} == vals))
cat = [comb(2 * k, k) // (k + 1) for k in range(1, 9)]
got = [len(parses(tok("+".join(["1"] * (k + 1))), {})) for k in range(1, 9)]
print(f"     parses of 1+1+...+1 with k plus signs, k = 1..8: {got}")
check("they are the Catalan numbers 1, 2, 5, 14, 42, 132, 429, 1430", got == cat, str(cat))
mix = parses(tok("1+2*3-4/2"), {})
check("'1+2*3-4/2': 14 parses, 9 distinct values; the precedence convention picks one (5)",
      len(mix) == 14 and len({v for _, v in mix}) == 9 and Fraction(5) in {v for _, v in mix},
      f"{len(mix)} parses, values {sorted(float(v) for v in set(v for _, v in mix))}")

print(f"[4] bracket depth in the corpus's own formulas (git show at {PIN})")
def git(*a): return subprocess.run(["git", "--no-optional-locks", "-C", str(ROOT), *a],
                                   capture_output=True, text=True, errors="ignore").stdout
RETIRED = ("docs/ml-evidence/", "_archive/", "_to_delete/")
pages = [f for f in git("ls-tree", "-r", "--name-only", PIN).split() if f.endswith(".html") and not f.startswith(RETIRED)]
STY = re.compile(r"<(style|script)\b.*?</\1>", re.S | re.I)
MATH = re.compile(r"\$\$(.+?)\$\$|\\\[(.+?)\\\]|\\\((.+?)\\\)|(?<![\\$])\$([^$\n]{1,400}?)\$(?!\$)", re.S)
def depth(s):
    s = re.sub(r"\\[{}]|\\left|\\right|\\big+l?|\\Big+l?", "", s)
    d = m = 0
    for ch in s:
        if ch in "([": d += 1; m = max(m, d)
        elif ch in ")]": d = max(0, d - 1)
    return m
depths, deepest = Counter(), (0, "", "")
nform = 0
for f in pages:
    t = html.unescape(STY.sub(" ", git("show", f"{PIN}:{f}")))
    for m in MATH.finditer(t):
        body = next(g for g in m.groups() if g)
        if not re.search(r"[\\^_=+()]", body): continue          # prices and stray dollars
        nform += 1; d = depth(body); depths[d] += 1
        if d > deepest[0]: deepest = (d, f, re.sub(r"\s+", " ", body)[:120])
print(f"     {nform:,} formulas on {len(pages)} pages; depth distribution: " +
      ", ".join(f"{d}:{depths[d]}" for d in sorted(depths)))
print(f"     deepest: {deepest[0]} on {deepest[1]}  {deepest[2]}")
share = sum(v for d, v in depths.items() if d <= 3) / nform
print(f"     share at depth ≤ 3: {share:.3f}")
EXPECT = dict(nform=11808, maxd=3, share=1.0)          # frozen from the first run at PIN
RES = dict(nform=nform, maxd=deepest[0], share=round(share, 3))
print("     RESULT", RES)
check("depths: 8,824 at 0, 2,822 at 1, 157 at 2, 5 at 3", dict(depths) == {0: 8824, 1: 2822, 2: 157, 3: 5}, str(dict(depths)))
for k, v in EXPECT.items():
    if v is not None: check(f"{k} = {v}", RES[k] == v, str(RES[k]))

print("[5] the Lean")
lean = (ROOT / "book14/Brackets.lean").read_text(encoding="utf-8")
check("Brackets.lean proves no_finite_reader and prints its axioms",
      "theorem no_finite_reader" in lean and "#print axioms Brackets.no_finite_reader" in lean)
check("no sorry in code", "sorry" not in re.sub(r"/-.*?-/|--[^\n]*", "", lean, flags=re.S))

print("[HONESTY]")
print("  [1] quotes an OCR of a scan; the OCR is checked for the quoted words, not proof-read. [3]'s")
print("  grammar has no precedence on purpose: it shows how many readings the conventions must")
print("  choose between, not how anyone reads. [4] counts ( ) [ ] inside $...$, $$...$$, \\(...\\),")
print("  \\[...\\]; braces are LaTeX syntax and are not counted. Brackets.lean proves the bracket")
print("  case of SS fn 3 only; whether English is finite state is not addressed.")
print(f"\n{len(FAIL)} FAIL" + (": " + ", ".join(FAIL) if FAIL else ""))
sys.exit(1 if FAIL else 0)
