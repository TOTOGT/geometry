#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book19/ch04-verify.py -- every number on book19/ch04-addresses.html. Run first (R24).
    python3 book19/ch04-verify.py
  [1] tools/lean_addresses.py on this repository alone: names that resolve nowhere, case-only, upstream
  [2] the artefact: how many pages carry the generated 'lake env lean FILE.lean' line that the
      address check read as a citation before 2026-09-27
  [3] the shape of the dangling set: cited once, only in retired folders, and the new books
  [4] the plan's "110": what in the repository is actually 110
  [HONESTY]
"""
import re, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)

import atexit, os, shutil, tempfile
PIN = "e6c5e85"   # the corpus as this chapter was written; later books add pages and Lean files
SNAP = Path(tempfile.mkdtemp(prefix="b19ch4-"))
atexit.register(shutil.rmtree, SNAP, True)
arc = subprocess.run(["git", "--no-optional-locks", "-C", str(ROOT), "archive", PIN], capture_output=True).stdout
subprocess.run(["tar", "-x", "-C", str(SNAP)], input=arc, check=True)
if (ROOT / ".lake").exists(): os.symlink(ROOT / ".lake", SNAP / ".lake")   # upstream Mathlib, for UPSTREAM rows

print(f"[1] the address check, on the corpus at {PIN}")
out = subprocess.run([sys.executable, str(ROOT / "tools/lean_addresses.py"), str(SNAP)],
                     capture_output=True, text=True).stdout
print("    " + out.splitlines()[1].strip())
rows = {}
for l in out.splitlines():
    m = re.match(r"\s+(DANGLING|CASE_ONLY|UPSTREAM)\s+(\S+)\s+(\d+)\s+(.*)", l)
    if m:
        pages = [p.strip() for p in m.group(4).split("[")[0].split(",")]
        rows.setdefault(m.group(1), []).append((m.group(2), int(m.group(3)), pages))
D = rows.get("DANGLING", [])
check("98 names resolve nowhere", len(D) == 98, str(len(D)))
check("217 citations of them in the published pages", sum(n for _, n, _ in D) == 217, str(sum(n for _, n, _ in D)))
check("1 resolves only under another case (main.lean vs Main.lean)", [r[0] for r in rows.get("CASE_ONLY", [])] == ["main.lean"])
check("12 resolve upstream in Mathlib and are not the corpus's claims", len(rows.get("UPSTREAM", [])) == 12)
top = sorted(D, key=lambda r: -r[1])[:5]
for nm, n, _ in top: print(f"     {nm:34} {n:3}")
check("most-cited dangling name is AutophagyDm3.lean, 15 pages", top[0][:2] == ("AutophagyDm3.lean", 15), str(top[0][:2]))

print("[2] the artefact")
GEN = re.compile(r"<!--po-run-->.*?<!--/po-run-->", re.S)
carry = [p for p in SNAP.rglob("*.html") if ".lake" not in p.parts
         and any("FILE.lean" in b for b in GEN.findall(p.read_text(encoding="utf-8", errors="ignore")))]
print(f"     pages whose generated run box says FILE.lean: {len(carry)}")
pre = [p for p in carry if not str(p).endswith(("book19/ch02-the-idioms-axle-reinvented.html", "book19/ch03-elaborator-macro-kernel.html"))]
check("96 carried it at the first run (this book's ch2 and ch3 add two since)", len(pre) == 96, str(len(pre)))
check("FILE.lean is absent from today's dangling list", "FILE.lean" not in [r[0] for r in D])
la = (SNAP / "tools/lean_addresses.py").read_text()
check("the fix: lean_addresses strips generated boxes", "GENERATED.sub" in la)

print("[3] the shape")
once = sum(1 for _, n, _ in D if n == 1)
dead = ("_to_delete/", "_archive/", "docs/ml-evidence/")
only_dead = [nm for nm, _, ps in D if all(p.startswith(dead) for p in ps)]
check("60 of the 98 are cited on one page only", once == 60, str(once))
check("4 survive only in retired folders", len(only_dead) == 4, str(only_dead))
new = ("book11/", "book12/", "book18/", "book20/", "book21/")
hits = [nm for nm, _, ps in D if any(p.startswith(new) for p in ps)]
check("books XI, XII, XVIII, XX, XXI (written this session) cite no dangling name", hits == [], str(hits))
b19 = [nm for nm, _, ps in D if any(p.startswith("book19/") for p in ps)]
print(f"     book19's own dangling names: {b19}")

print("[4] the plan's 110")
PIN = "e6c5e85"   # the census is of the corpus as this chapter was written (Book XIX ch2-4 commit)
files = [f for f in subprocess.run(["git", "--no-optional-locks", "-C", str(ROOT), "ls-tree", "-r", "--name-only", PIN],
         capture_output=True, text=True).stdout.split() if f.endswith(".lean") and ".lake" not in f]
check("110 is the number of tracked .lean files", len(files) == 110, str(len(files)))
check("which the tool sees as 109 distinct names: two tracked files share one", "against 109 corpus .lean files" in out)

print("[5] with the sister repositories")
import os
R = [os.path.expanduser(x) for x in ("~/Desktop/AXLE", "~/Desktop/GTCT")]
if all(os.path.isdir(r) for r in R):
    o2 = subprocess.run([sys.executable, str(ROOT / "tools/lean_addresses.py"), str(ROOT), "--roots", *R], capture_output=True, text=True).stdout
    m = re.search(r"(\d+) names resolve nowhere", o2)
    check("49 names resolve nowhere across all three roots", m and m.group(1) == "49", m and m.group(1))
else:
    print("     AXLE/GTCT not present here; the page's 49 is the Mac run of 2026-09-27 (e6c5e85)")
print("[HONESTY]")
print("  Run against this repository alone. The tool accepts --roots ~/Desktop/AXLE ~/Desktop/GTCT;")
print("  [5] reruns with them when present. A name that resolves is not thereby a correct citation;")
print("  decl_resolve.py is the rung above. The index's '110 names' had no recorded run. The first run")
print("  (242 citations) also counted untracked copies in _to_delete/; the tool now skips that folder.")
print(f"\n{len(FAIL)} FAIL" + (": " + ", ".join(FAIL) if FAIL else ""))
sys.exit(1 if FAIL else 0)
