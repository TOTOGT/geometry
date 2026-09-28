#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book14/ch08-verify.py -- every number and quotation on book14/ch08-six-lines.html. Run first (R24).
    python3 book14/ch08-verify.py [--downloads DIR]
  [1] Kahle, "Towards the Structure of Mathematical Proof": the Hardy & Wright proof and the
      Wiedijk and Scott sentences it quotes
  [2] the Lean: every Hardy & Wright step tagged HW(k), k = 1..6, has code under it; lines,
      words and library lemmas per sentence
  [HONESTY]
"""
import os, re, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def dl():
    if "--downloads" in sys.argv: return Path(sys.argv[sys.argv.index("--downloads") + 1])
    for c in ("~/mnt/Downloads", "~/Downloads"):
        p = Path(os.path.expanduser(c))
        if p.is_dir(): return p
norm = lambda s: re.sub(r"\s+", " ", s.replace("’", "'").replace("“", '"').replace("”", '"')).strip()
K = norm(subprocess.run(["pdftotext", str(dl() / "paper-22.pdf"), "-"], stdout=subprocess.PIPE,
                        stderr=subprocess.DEVNULL, text=True).stdout)

print("[1] Kahle, Towards the Structure of Mathematical Proof")
check("title and author", "Towards the Structure of Mathematical Proof" in K and "Reinhard Kahle" in K)
HW = ("The traditional proof ascribed to Pythagoras runs as follows. If 2 is rational, then the equation a2 = 2b2 "
      "is soluble in integers a, b with (a, b) = 1. Hence a2 is even, and therefore a is even. If a = 2c, then "
      "4c2 = 2b2 , 2c2 = b2 , and b is also even, contrary to the hypothesis that (a, b) = 1.")
kk = K.replace("√", "")
check("the Hardy & Wright proof, as Kahle quotes it (radicals and superscripts flattened by the PDF)", norm(HW) in kk)
for q in ["Ideally, a computer should be able to take this text as input and check it for its correctness. We clearly are not yet there",
          "One of the reasons for this is that this version of the proof does not have enough detail",
          "What really is a proof?",
          "seventeen theorem provers"]:
    check(f'Kahle: "{q[:60]}"', norm(q) in K)
hw_words = len(re.findall(r"[A-Za-z0-9]+", HW.split("follows.")[1]))
print(f"     Hardy & Wright's argument (after 'runs as follows'): {hw_words} words")

print("[2] the Lean, sentence by sentence")
src = (ROOT / "book14/HardyWright.lean").read_text(encoding="utf-8")
body = src[src.index("theorem no_coprime_solution"):src.index("end HardyWright")]
steps, cur = {}, None
for line in body.splitlines()[1:]:
    m = re.match(r"\s*-- HW\((\d)\)", line)
    if m: cur = int(m.group(1)); steps.setdefault(cur, []); continue
    if cur and line.strip() and not line.strip().startswith("--"): steps[cur].append(line.strip())
check("every Hardy & Wright step 2..6 has code; step 1 is the hypotheses", all(steps.get(k) for k in range(2, 7)) and 1 in steps)
code = [l for k in steps for l in steps[k]]
lean_words = sum(len(re.findall(r"[A-Za-z0-9_.]+", l)) for l in code)
names = re.findall(r"\b(?:Nat\.[A-Za-z_.]+|dvd_mul_right)\b", " ".join(code))
lemmas = sorted({n.split(".")[-1] for n in names} - {"Coprime"})          # library FACTS, not the type name
for k in sorted(steps): print(f"     HW({k}): {len(steps[k])} line(s)  {' | '.join(steps[k])[:110]}")
print(f"     {len(code)} lines of proof, {lean_words} tokens; library lemmas named: {lemmas}")
check("7 lines of proof for Hardy & Wright's steps", len(code) == 7, str(len(code)))
check("5 library facts named, plus the tactic nlinarith (the detail the library carries)",
      lemmas == ["coprime_dvd_left", "coprime_iff_not_dvd", "dvd_mul_right", "dvd_of_dvd_pow", "prime_two"]
      and "nlinarith" in " ".join(code), str(lemmas))
check("the theorem is the one Hardy & Wright state: a^2 = 2*b^2 with (a, b) = 1 is impossible",
      "(hab : Nat.Coprime a b) (h : a ^ 2 = 2 * b ^ 2) : False" in src)
check("no sorry", "sorry" not in re.sub(r"/-.*?-/|--[^\n]*", "", src, flags=re.S))
check("its axioms are printed", "#print axioms HardyWright.no_coprime_solution" in src)
print(f"     RESULT hw_words={hw_words} lines={len(code)} tokens={lean_words}")
check("frozen: 49 words of Hardy & Wright, 7 lines and 52 tokens of Lean", (hw_words, len(code), lean_words) == (49, 7, 52),
      f"{hw_words}, {len(code)}, {lean_words}")

print("[HONESTY]")
print("  The Lean follows Hardy & Wright's order, but it leans on Mathlib: 'a prime dividing a^2 divides a'")
print("  and 'nlinarith' each hide pages of detail. Short is not the same as detail-free; Scott's question")
print("  ('How much detail is needed?') is answered here only for a reader who trusts the library.")
print("  Kahle's xml proposal is not implemented. The seventeen provers book (Wiedijk 2006) is not held.")
print(f"\n{len(FAIL)} FAIL" + (": " + ", ".join(FAIL) if FAIL else ""))
sys.exit(1 if FAIL else 0)
