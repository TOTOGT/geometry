#!/usr/bin/env python3
"""photochem-index-verify.py -- checks behind book7/photochem-index.html (2026-10-04).

The index makes three kinds of statement: that there are four rooms, that each has its own check, and a short list of
findings. This script checks the structure and runs the four room scripts; it does not repeat their arithmetic.

Blocks
 [1] the five pages and four room scripts exist; each room script runs and exits 0
 [2] control: a room script with one constant deliberately broken exits non-zero
 [3] links: every .html link on the five pages resolves; rooms link to the index and to each other in order
 [4] the index's findings are present in the room pages that produce them
 [5] tutor structure (needs tools/photochem_content beside the repo root): four CEFR levels, EN/PT glossary, chooser, one correct quiz option
"""
import os, re, subprocess, sys, html as _html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + ("  " + detail if detail else ""))
    if not ok: FAIL.append(label)

ROOMS = ["light-sources", "spectrometer", "laser", "flash-photolysis"]
pages = ["photochem-index.html"] + [f"photochem-{r}.html" for r in ROOMS]
scripts = [f"photochem-{r}-verify.py" for r in ROOMS]

# [1] -----------------------------------------------------------------------------
check("[1] five pages exist beside this script", all(os.path.exists(os.path.join(HERE, p)) for p in pages))
check("[1] four room scripts exist", all(os.path.exists(os.path.join(HERE, s)) for s in scripts))
for s in scripts:
    r = subprocess.run([sys.executable, os.path.join(HERE, s)], capture_output=True, text=True, cwd=HERE)
    nfail = sum(1 for l in r.stdout.splitlines() if l.startswith("FAIL"))
    npass = sum(1 for l in r.stdout.splitlines() if l.startswith("PASS"))
    check(f"[1] {s} exits 0 with no FAIL lines", r.returncode == 0 and nfail == 0, f"{npass} PASS")

# [2] -----------------------------------------------------------------------------
src = open(os.path.join(HERE, "photochem-flash-photolysis-verify.py"), encoding="utf-8").read()
broken = src.replace("eps, ell = 7e4, 20.0", "eps, ell = 7e3, 20.0")
import tempfile
with tempfile.TemporaryDirectory() as _d:                      # outside the repository: nothing to delete afterwards
    ctl = os.path.join(_d, "flash_broken.py")
    open(ctl, "w", encoding="utf-8").write(broken)
    r = subprocess.run([sys.executable, ctl], capture_output=True, text=True, cwd=_d)
check("[2] control: the flash script with eps = 7e3 instead of 7e4 exits non-zero", broken != src and r.returncode != 0)
check("[2] control: the broken copy actually printed a FAIL line", any(l.startswith("FAIL") for l in r.stdout.splitlines()))

# [3] -----------------------------------------------------------------------------
def text(p):
    t = open(os.path.join(HERE, p), encoding="utf-8").read()
    return re.sub(r"<!--po-([a-z]+)-->.*?<!--/po-\1-->", "", t, flags=re.S)
bad = []
for p in pages:
    for h in re.findall(r'href="([^"#?]+\.html)', text(p)):
        if h.startswith(("http:", "https:", "//")): continue
        if not os.path.exists(os.path.normpath(os.path.join(HERE, h))): bad.append((p, h))
check("[3] every .html link on the five pages resolves", not bad, str(bad[:3]))
idx = text("photochem-index.html")
check("[3] the index links to all four rooms and to the Rohatgi-Mukherjee chapter", all(f"photochem-{r}.html" in idx for r in ROOMS) and "ch-rohatgi-mukherjee.html" in idx)
ok_nav = True
for i, r in enumerate(ROOMS):
    t = text(f"photochem-{r}.html")
    if "photochem-index.html" not in t: ok_nav = False
    if i > 0 and f"photochem-{ROOMS[i-1]}.html" not in t: ok_nav = False
    if i < len(ROOMS) - 1 and f"photochem-{ROOMS[i+1]}.html" not in t: ok_nav = False
    if scripts[i] not in t: ok_nav = False
check("[3] each room links to the index, its neighbours, and names its own verify script", ok_nav)
check("[3] control: a made-up room link is NOT present", "photochem-microscope.html" not in idx)

# [4] -----------------------------------------------------------------------------
flat = lambda p: _html.unescape(re.sub(r"<[^>]+>", " ", text(p)))
r4 = flat("photochem-flash-photolysis.html"); r3 = flat("photochem-laser.html")
check("[4] index finding 1 (flash limit direction) is in Room 4: 'upper limit' printed, 'lower limit' derived", "upper" in r4 and "lower" in r4 and "0.952" in r4)
check("[4] index finding 2 (1e19 W/cm2) is in Room 3 with its numbers", "1e19" in r3 and "4.8e10" in r3 and "2e21" in r3)
check("[4] index finding 3 (sector inflection) is in Room 4", "16.1" in r4 and "first-order" in r4)
check("[4] index small roundings (2.5e19 vs 2.42e19, 0.68 %) are in the rooms", "2.42e19" in r4 and "0.68" in flat("photochem-light-sources.html"))
check("[4] control: the index does not claim a finding the rooms lack ('spectral peak shift of 10 nm')", "10 nm" not in flat("photochem-index.html"))

# [5] -----------------------------------------------------------------------------
tools = os.path.join(ROOT, "tools")
if os.path.isdir(os.path.join(tools, "photochem_content")):
    sys.path.insert(0, tools)
    import importlib
    for r, mod in zip(ROOMS, ("room1", "room2", "room3", "room4")):
        R = importlib.import_module("photochem_content." + mod).ROOM
        lv = sorted(R["concept"].keys())
        q = R["quiz"]
        ok = (lv == ["A2", "B1", "B2", "C1"] and len(R["glossary"]) >= 10 and all(len(g) == 2 and g[0] and g[1] for g in R["glossary"])
              and len(R["chooser"]) >= 6 and len(q["opts"]) == 4 and 0 <= q["correct"] < 4
              and all(set(o) == {"en", "pt"} for o in q["opts"]) and R["slug"] == r)
        check(f"[5] {mod}: four CEFR levels, glossary of EN/PT pairs, chooser, four quiz options with one correct", ok)
    lens = [len(importlib.import_module("photochem_content." + m).ROOM["concept"][k]) for m in ("room1", "room2", "room3", "room4") for k in ("A2", "C1")]
    check("[5] each C1 text is longer than the A2 text of the same room (difficulty calibration is not flat)", all(lens[i + 1] > lens[i] for i in range(0, 8, 2)))
    check("[5] control: the claim that all four rooms put the correct quiz option first is REJECTED",
          not all(importlib.import_module("photochem_content." + m).ROOM["quiz"]["correct"] == 0 for m in ("room1", "room2", "room3", "room4")))
else:
    print("SKIP [5] tools/photochem_content not found beside the repo root")

print("\n[HONESTY] This script checks structure and runs the room scripts. It does not check that the Portuguese is idiomatic (no native speaker has reviewed it), that the CEFR labels match a formal CEFR assessment (they are our judgement of difficulty), or that no passage of the textbook is reproduced (the textbook is not in this repository; the pages paraphrase by page).")
print("[HONESTY] Block [5] confirms C1 text is longer than A2 text, which is a weak proxy for difficulty, not a measurement of it.")
sys.exit(1 if FAIL else 0)
