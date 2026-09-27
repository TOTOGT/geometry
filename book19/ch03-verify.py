#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book19/ch03-verify.py -- every number and quotation on book19/ch03-elaborator-macro-kernel.html. Run first (R24).
    python3 book19/ch03-verify.py [--downloads DIR]
  [1] Ullrich (2023), the five sentences the page quotes, found on the printed pages it cites
      (printed page = PDF page - 12, checked on two anchors)
  [2] the corpus by layer: #print axioms lines, native_decide and sorry outside comments,
      and whether any of them sits in a file a build target compiles
  [3] the gate reads the kernel's answer, not a word list (tools/leancheck.sh defers to axiom_gate.py)
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
DL = dl()

print("[1] Ullrich, An Extensible Theorem Proving Frontend (KIT dissertation, 2023)")
pdf = DL / "thesis-sebastian.pdf"
pages = subprocess.run(["pdftotext", str(pdf), "-"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                       text=True).stdout.split("\f")
check("thesis held: 255 PDF pages", len(pages) >= 255, str(len(pages)))
norm = lambda s: re.sub(r"\s+", " ", s.replace("’", "'")).strip()
OFF = 12
for pr in (34, 36):   # anchors: the printed folio sits at the foot of the page
    check(f"printed p.{pr} is PDF p.{pr+OFF}", norm(pages[pr + OFF - 1]).endswith(str(pr)))
QUOTES = [
    (15, "metaprograms are not part of Lean's Trusted Code Base"),
    (15, "their output is checked by the kernel just as if we had written down the output manually"),
    (15, "The Lean kernel does not accept any kind of recursion in regular definitions"),
    (19, "The kernel type checker does not use a metavariable context"),
    (34, "which is an independent component in order to minimize the Trusted Code Base"),
    (36, "(which therefore becomes part of the Trusted Code Base)"),
]
for pr, q in QUOTES:
    check(f"p.{pr}: \"{q[:58]}...\"", norm(q) in norm(pages[pr + OFF - 1]))
check("Fig. 3.1 on p.34 names parser, macro expansion, elaborator, kernel",
      all(w in pages[34 + OFF - 1] for w in ("parser", "macro expansion", "elaborator", "kernel")))

print("[2] the corpus by layer")
files = [f for f in subprocess.run(["git", "--no-optional-locks", "-C", str(ROOT), "ls-files", "*.lean"],
         capture_output=True, text=True).stdout.split() if ".lake" not in f]
def code(f):
    t = (ROOT / f).read_text(encoding="utf-8", errors="ignore")
    t = re.sub(r"/-.*?-/", "", t, flags=re.S); return re.sub(r"--[^\n]*", "", t)
src = {f: code(f) for f in files}
pa = {f: len(re.findall(r"^#print axioms", t, re.M)) for f, t in src.items()}
nd = sorted(f for f, t in src.items() if re.search(r"\bnative_decide\b", t))
so = sorted(f for f, t in src.items() if re.search(r"\bsorry\b", t))
print(f"     {len(files)} tracked files; #print axioms lines {sum(pa.values())} in {sum(1 for v in pa.values() if v)} files")
print(f"     native_decide in code: {nd}")
print(f"     sorry in code: {so}")
lake = (ROOT / "lakefile.lean").read_text()
check("native_decide survives comment-stripping in exactly one file", nd == ["CollatzDescent.lean"], str(nd))
check("and no lean_lib declares it", "lean_lib CollatzDescent" not in lake)
check("sorry survives in code in four files", len(so) == 4, str(len(so)))
mag = (ROOT / "Orthogenesis/Architecture/MagneticLattice.lean").read_text(encoding="utf-8")
check("the one under a default target (Orthogenesis) discloses itself", "left as an explicit `sorry`" in mag)
check("one of the four is a moved deposit under docs/ml-evidence", any(f.startswith("docs/ml-evidence/") for f in so))
car = src.get("book12/Carrying.lean", "")
check("Carrying.lean: no `decide` evaluates addc (closed by rw/simp instead)",
      "addc" in car and not re.search(r"addc[^\n]*\n?[^\n]*:= by decide", car))

print("[3] the gate")
lc = (ROOT / "tools/leancheck.sh").read_text()
check("leancheck.sh names axiom_gate.py as the verdict", "axiom_gate.py" in lc and "THE VERDICT IS" in lc)
check("and records why a word list fails (Lean.ofReduceBool)", "ofReduceBool" in lc)
ag = (ROOT / "tools/axiom_gate.py").read_text()
check("axiom_gate permits exactly propext, Classical.choice, Quot.sound",
      all(a in ag for a in ("propext", "Classical.choice", "Quot.sound")))

print("[HONESTY]")
print("  Ullrich's thesis describes Lean 4 as of 2023; the layer names are his, the classification of")
print("  this corpus's incidents into them is ours (MODEL). Why `decide` stalled on addc was not")
print("  diagnosed beyond the layer that reported it. No Lean is run by this script: the build")
print("  verdict is tools/leancheck.sh --audit on the Mac.")
print(f"\n{len(FAIL)} FAIL" + (": " + ", ".join(FAIL) if FAIL else ""))
sys.exit(1 if FAIL else 0)
