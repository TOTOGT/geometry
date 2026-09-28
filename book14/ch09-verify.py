#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book14/ch09-verify.py -- every number and quotation on book14/ch09-what-types-decide.html. Run first (R24).
    python3 book14/ch09-verify.py [--downloads DIR]
  [1] the sources say what the page quotes (Avigad 2021; Aberdein on Ganesalingam; Ganesalingam &
      Gowers; Macmillan; I❤LA; Stathopoulos & Teufel; Matsuzaki et al.)
  [2] Avigad's grammatical claim tested: past tense and modal verbs per million words in this series,
      in Mathematics in Lean, in Avigad's own chapter and in J&M
  [3] Leibniz 1684 (Nova Methodus, as printed in the Gerhardt edition): the page image is held, and the
      quotient rule's two sign readings are checked against the derivative
  [4] the Lean: book14/TypesDecide.lean
  [HONESTY]
"""
import hashlib, html, os, re, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
PIN = "4b4b354"
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
norm = lambda s: re.sub(r"\s+", " ", s.replace("’", "'").replace("“", '"').replace("”", '"').replace("‘", "'").replace("- ", "")).strip()
def raw(name): return subprocess.run(["pdftotext", str(D / name), "-"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True).stdout
def pdf(name): return norm(raw(name))

print("[1] the sources")
S = {
 "Avigad": ("The design of mathematical language.pdf", [
   "there is a sense in which formal systems specify too little, and there is a sense in which they specify too much",
   "There are no subtle variations of tense, modality, or aspect, and the subject is generally devoid of subjunctives and counterfactuals"]),
 "Aberdein": ("Mohan_Ganesalingam_The_Language_of_Mathe.pdf", [
   "Ganesalingam observes that the syntax of mathematics is type-dependent",
   "full adaptivity"]),
 "Ganesalingam & Gowers": ("A fully automatic problem solver with human-style output.pdf", [
   "presents the solutions in a form that is hard to distinguish from solutions that human mathematicians might write"]),
 "Macmillan": ("ON THE GRAMMAR OF PROOF MacMillan_Warrick.pdf", [
   "Syntactic completeness is a criteria for judging constructions which contain no errors and entirely encode an argument's subtlest details"]),
 "I❤LA": ("I ❤ LA- Compilable Markdown for Linear Algebra.pdf", [
   "juxtaposition is multiplication", "depending on the types of the operands"]),
 "Stathopoulos & Teufel": ("Mathematical Information Retrieval based on Type Embeddings and Query Expansion.pdf", [
   "a special kind of technical terminology, referred to as a mathematical type"]),
 "Matsuzaki et al.": ("The Most Uncreative Examinee- A First Step toward Wide Coverage Natural Language Math Problem Solving.pdf", [
   "We evaluated our prototype system on real university entrance exam problems"])}
T = {}
for who, (f, qs) in S.items():
    T[who] = pdf(f)
    for q in qs: check(f'{who}: "{q[:60]}..."', norm(q) in T[who])

print(f"[2] Avigad's claim: tense and modality per million words (this series at {PIN})")
def git(*a): return subprocess.run(["git", "--no-optional-locks", "-C", str(ROOT), *a], capture_output=True, text=True, errors="ignore").stdout
pages = [f for f in git("ls-tree", "-r", "--name-only", PIN).split() if f.endswith(".html") and not f.startswith(("docs/ml-evidence/", "_archive/", "_to_delete/"))]
GEN = re.compile(r"<!--po-(run|gss|related|subject)-->.*?<!--/po-\1-->", re.S); STY = re.compile(r"<(style|script|pre|code)\b.*?</\1>", re.S | re.I)
MATH = re.compile(r"\$\$.+?\$\$|\\\[.+?\\\]|\\\(.+?\\\)|\$[^$\n]{1,400}?\$", re.S)
series = " ".join(MATH.sub(" ", html.unescape(re.sub(r"<[^>]+>", " ", STY.sub(" ", GEN.sub(" ", git("show", f"{PIN}:{f}")))))) for f in pages)
texts = {"this series": series, "Mathematics in Lean": raw("mathematics_in_lean.pdf"),
         "Avigad 2021": raw("The design of mathematical language.pdf"), "J&M 2026 draft": raw("ed3book_aug26.pdf")}
PAST, MODAL = r"\b(was|were)\b", r"\b(would|could|might|should|may|must)\b"
R = {}
for k, t in texts.items():
    w = len(re.findall(r"[A-Za-z]+", t))
    R[k] = (w, round(1e6 * len(re.findall(PAST, t, re.I)) / w), round(1e6 * len(re.findall(MODAL, t, re.I)) / w))
    print(f"     {k:20} {w:10,} words   was/were {R[k][1]:5}/M   modals {R[k][2]:5}/M")
ratio = R["this series"][1] / R["Mathematics in Lean"][1]
check("past tense separates: this series uses about 21x the 'was/were' of Mathematics in Lean", 19 < ratio < 23, f"{ratio:.1f}x")
mod = [v[2] for v in R.values()]
check("modality does not separate: all four within 2,100-3,700 modals per million", min(mod) > 2100 and max(mod) < 3700, str(mod))
check("frozen past-tense rates: series 2900, MIL 136, Avigad 1021, J&M 2073",
      [R[k][1] for k in texts] == [2900, 136, 1021, 2073], str([R[k][1] for k in texts]))

print("[3] Leibniz, Nova Methodus (Acta Eruditorum 1684), page as printed in the Gerhardt edition")
img = ROOT / "book14/img/nova-methodus-1684.png"
check("page image held", img.exists() and hashlib.sha256(img.read_bytes()).hexdigest().startswith("0f4d6fdb320bf841"))
# the printed rules, transcribed: da = 0; d(ax) = a dx; d(z - y + w + x) = dz - dy + dw + dx;
# d(xv) = x dv + v dx; d(v/y) = (± v dy ∓ y dv) / yy
import math
cases = [(lambda x: x * x, lambda x: 2 * x, lambda x: x + 1, lambda x: 1.0),
         (math.sin, math.cos, math.exp, math.exp),
         (lambda x: x ** 3, lambda x: 3 * x * x, lambda x: 2 + math.cos(x), lambda x: -math.sin(x))]
up_ok = lo_ok = prod_ok = True
for v, dv, y, dy in cases:
    for x in (0.3, 1.0, 2.0):
        h = 1e-6
        true_q = ((v(x + h) / y(x + h)) - (v(x - h) / y(x - h))) / (2 * h)
        upper = (+v(x) * dy(x) - y(x) * dv(x)) / y(x) ** 2
        lower = (-v(x) * dy(x) + y(x) * dv(x)) / y(x) ** 2
        up_ok &= abs(upper - true_q) < 1e-5; lo_ok &= abs(lower - true_q) < 1e-5
        true_p = (v(x + h) * y(x + h) - v(x - h) * y(x - h)) / (2 * h)
        prod_ok &= abs(v(x) * dy(x) + y(x) * dv(x) - true_p) < 1e-5
check("Multiplicatio: d(xv) = x dv + v dx holds (9 test points)", prod_ok)
check("Divisio, lower signs (- v dy + y dv)/yy: correct at all 9 points", lo_ok)
check("Divisio, upper signs (+ v dy - y dv)/yy: wrong at every point (the exact negative)", not up_ok)

print("[4] the Lean")
lean = (ROOT / "book14/TypesDecide.lean").read_text(encoding="utf-8")
for t in ["nat_mul_comm", "matrix_mul_not_comm"]:
    check(f"TypesDecide.lean proves {t}", f"theorem {t}" in lean and f"#print axioms TypesDecide.{t}" in lean)
check("no sorry", "sorry" not in re.sub(r"/-.*?-/|--[^\n]*", "", lean, flags=re.S))

print("[HONESTY]")
print("  Ganesalingam's book is not held; his claims are cited through Aberdein's review. The Leibniz text is")
print("  a page image transcribed by eye; the edition's page number is not on the image. Past tense is")
print("  counted as 'was/were' only, a crude proxy; the series' prose includes a gallery of historical")
print("  chapters, which inflates it. Kahle's corpus is too small (2.8k words) to measure and is left out.")
print(f"\n{len(FAIL)} FAIL" + (": " + ", ".join(FAIL) if FAIL else ""))
sys.exit(1 if FAIL else 0)
