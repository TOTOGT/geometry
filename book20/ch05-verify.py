#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book20/ch05-verify.py -- every number on book20/ch05-the-storms-nobody-counted.html. Run first (R24).

    python3 book20/ch05-verify.py [--downloads DIR]

  [1] the held file: hash and storm count, as the index ledgered them
  [2] the PRE-REGISTERED observable (book20/index.html, 2026-09-21): storms reaching
      tropical-storm strength (>= 34 kt, status TS or HU) per decade, 1851-2025
  [3] ADDED 2026-09-27, after [2] was fixed and before it was run: the same count split
      by whether the storm has a landfall record ('L'). Not pre-registered; labelled so.
  [4] what the file alone can and cannot say
  [HONESTY]
"""
import hashlib, os, sys
from collections import Counter
from pathlib import Path
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
HU = DL / "hurdat2-1851-2025-091226.txt" if DL else None
if not HU or not HU.exists():
    print("SKIP: HURDAT2 not on this machine"); sys.exit(0)

print("[1] the file")
h = hashlib.sha256(HU.read_bytes()).hexdigest()
check("sha256 matches the ledger prefix df63fabce0ad824d", h.startswith("df63fabce0ad824d"), h[:16])
storms, cur = [], None
for line in HU.read_text(encoding="latin-1").splitlines():
    f = [x.strip() for x in line.split(",")]
    if f[0][:2].isalpha():
        cur = {"id": f[0], "year": int(f[0][4:8]), "status": set(), "wind": 0, "landfall": False}
        storms.append(cur)
    else:
        cur["status"].add(f[3]); cur["landfall"] |= (f[2] == "L")
        cur["wind"] = max(cur["wind"], int(f[6]))
check("1988 storms", len(storms) == 1988, str(len(storms)))
ts = [s for s in storms if s["status"] & {"TS", "HU"}]
print(f"     reached TS or HU status: {len(ts)} of {len(storms)}")

print("[2] pre-registered: TS-strength storms per decade")
dec = Counter(10 * (s["year"] // 10) for s in ts)
decs = sorted(d for d in dec if d <= 2020)
for d in decs:
    tag = " (2020-2025, six seasons)" if d == 2020 else ""
    print(f"     {d}s  {dec[d]:4d}  " + "#" * (dec[d] // 5) + tag)
E0, E1, L0, L1 = 1851, 1899, 1970, 2019          # 49 and 50 seasons
ns = lambda a, b, sel=lambda s: True: sum(1 for s in ts if a <= s["year"] <= b and sel(s))
early, late = ns(E0, E1) / 49, ns(L0, L1) / 50
print(f"     per season, 1851-1899: {early:.2f};  1970-2019: {late:.2f};  ratio {late/early:.2f}")
check("the early seasons are lower", early < late)
print("[3] added, not pre-registered: split by landfall record")
rows = {}
for label, sel in (("with a landfall record", True), ("without one", False)):
    e = ns(E0, E1, lambda s: s["landfall"] == sel) / 49
    l = ns(L0, L1, lambda s: s["landfall"] == sel) / 50
    rows[sel] = l / e
    print(f"     {label:24}  1851-1899 {e:5.2f}/season   1970-2019 {l:5.2f}/season   ratio {l/e:.2f}")
print(f"     the simple at-sea-undercount story predicts the second ratio is the larger one;")
print(f"     it is {'larger' if rows[False] > rows[True] else 'NOT larger'}")
check("sanity: both groups are non-empty in both periods", rows[True] > 0 and rows[False] > 0)
first = min(s["year"] for s in ts if s["landfall"])
print(f"     landfall flags present from {first}")

print("""
[HONESTY]
[2] is the observable fixed on the index before this script existed. [3] was added
while writing it: it is a second look, and by Chapter 2's rule it carries less weight
than [2]. The landfall flag is a coding in the file, and a storm with no 'L' record can
still have touched land. On this file the landfall-coded storms rose at least as much
as the rest, which is not what a simple 'only the storms at sea were missed' account
predicts -- but coastlines were thinly watched too, and how a landfall flag came to be
assigned to an 1860 storm is not documented in the held file, so this does not
refute undercounting either.
The file cannot separate climate from counting. That needs a history of how the Atlantic was
observed -- ship traffic, aircraft reconnaissance from the 1940s, satellites from the
1960s -- and no such source is held. The verdict stays open.
""")
print(f"{len(FAIL)} FAIL")
sys.exit(1 if FAIL else 0)
