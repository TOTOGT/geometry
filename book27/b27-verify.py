#!/usr/bin/env python3
"""Verify Book XXVII (UoPeople MSIT study book), draft 2026-11-12.

Run from anywhere:  python3 b27-verify.py
Checks structure, links, that each chapter's unit headings match the official unit
lists read from the UoPeople course pages on 2026-11-12, that the computed worked
examples (critical path, PERT, earned value, risk) are recomputed here and match the
pages, and that the honesty markers are present. It does NOT check that the
theory statements are correct; that is a reading task, not a script task.
"""
import os, re, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
fails = 0
def check(name, ok, detail=""):
    global fails
    print(("PASS  " if ok else "FAIL  ") + name + ("" if ok else "  " + detail))
    if not ok:
        fails += 1
def read(n):
    with open(os.path.join(HERE, n), encoding="utf-8") as f:
        return f.read()

FILES = {
    "index.html": None,
    "b27-ch01-organizational-theory-and-behavior.html": [
        "Introduction to Organizational Theory and Behavior",
        "Organizational Concepts and Theories",
        "Employee Motivation and Rewards",
        "Attitudes, Perceptions, and Behaviors",
        "Organizational Communication",
        "Collaborative Dynamics: Groups and Teams",
        "Leadership, Power, and Conflict",
        "Organizational Culture and Change"],
    "b27-ch02-business-law-ethics-csr.html": [
        "Introduction to Ethics in Business", "Ethics in Accounting",
        "Ethics and Environmental Concerns", "Ethics in Finance", "Ethics in the Law",
        "Ethics in Marketing", "Ethics in Management", "Ethics in Corporate Planning"],
    "b27-ch03-managing-projects-programs.html": [
        "Introduction to Project Management", "Initiation Phase",
        "Project Planning, Part 1", "Project Planning, Part 2", "Project Planning, Part 3",
        "Project Execution", "Control", "Closing and Project Success Factors"],
}

# ---- files, self-containment, links
for fn in FILES:
    check(f"{fn} exists", os.path.exists(os.path.join(HERE, fn)))
pages = {fn: read(fn) for fn in FILES if os.path.exists(os.path.join(HERE, fn))}
for fn, h in pages.items():
    check(f"{fn} has no external resources",
          not re.search(r'(src|href)="https?://', h) and "<script" not in h and "@import" not in h)
    check(f"{fn} has a title and a viewport", "<title>" in h and "viewport" in h)
    check(f"{fn} has no placeholder text", not re.search(r"lorem ipsum|TODO|FIXME", h, re.I))
    for href in re.findall(r'href="([^"#]+)"', h):
        if href.startswith(("http", "mailto")):
            continue
        ok = os.path.exists(os.path.normpath(os.path.join(HERE, href)))
        check(f"{fn} link {href} resolves", ok)

# ---- unit headings match the official lists
def clean(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s.replace("&middot;", "·"))).strip()
for fn, units in FILES.items():
    if units is None or fn not in pages:
        continue
    heads = [clean(m) for m in re.findall(r"<h2>(.*?)</h2>", pages[fn])]
    found = [re.sub(r"^Unit \d+ · ", "", h) for h in heads if h.startswith("Unit ")]
    # chapter 3 titles for planning units carry a subtitle after a colon
    ok = len(found) == len(units) and all(f.startswith(u) for f, u in zip(found, units))
    check(f"{fn} unit headings match the official 8-unit list", ok, f"found {found}")
    check(f"{fn} has 8 self-check questions", pages[fn].count("<b>Self-check</b>") == 8)

# ---- computed worked examples
ACT = {"A": (3, []), "B": (2, ["A"]), "C": (4, ["A"]), "D": (3, ["B"]), "E": (2, ["C"]),
       "F": (4, ["D", "E"])}
es, ef = {}, {}
for a, (d, pre) in ACT.items():
    es[a] = max([ef[p] for p in pre], default=0); ef[a] = es[a] + d
T = max(ef.values()); lf, ls = {}, {}
for a in reversed(list(ACT)):
    succ = [b for b in ACT if a in ACT[b][1]]
    lf[a] = min([ls[b] for b in succ], default=T); ls[a] = lf[a] - ACT[a][0]
flt = {a: ls[a] - es[a] for a in ACT}
crit = [a for a in ACT if flt[a] == 0]
check("CPM: project duration is 13 days", T == 13)
check("CPM: critical path is A, C, E, F", crit == ["A", "C", "E", "F"])
check("CPM: float B = 1 and D = 1", flt["B"] == 1 and flt["D"] == 1)
ch3 = pages.get("b27-ch03-managing-projects-programs.html", "")
check("page states duration 13 and path A→C→E→F",
      "duration is 13 days" in ch3 and "A &rarr; C &rarr; E &rarr; F" in ch3)
for a in ACT:
    row = f"<tr><td>{a}</td><td>{ACT[a][0]}</td><td>{', '.join(ACT[a][1]) or '-'}</td><td>{es[a]}</td><td>{ef[a]}</td><td>{ls[a]}</td><td>{lf[a]}</td><td>{flt[a]}</td></tr>"
    check(f"page table row for activity {a} matches", row in ch3)

o, m_, p = 2, 5, 14
te = F(o + 4 * m_ + p, 6); sd = F(p - o, 6); var = sd ** 2
check("PERT: expected 6, sd 2, variance 4", (te, sd, var) == (6, 2, 4))
check("page states the PERT result", "expected duration is 6 days, the standard deviation 2 days and the variance 4 days squared" in ch3)

BAC, PV, EV, AC = 100000, 40000, 35000, 42000
CPI = F(EV, AC); SPI = F(EV, PV); EAC = F(BAC) / CPI
vals = dict(CV=EV - AC, SV=EV - PV, CPI=float(CPI), SPI=float(SPI), EAC=float(EAC),
            ETC=float(EAC - AC), VAC=float(BAC - EAC), TCPI=float(F(BAC - EV, BAC - AC)))
check("EVM: CV -7000, SV -5000", vals["CV"] == -7000 and vals["SV"] == -5000)
check("EVM: CPI 0.8333, SPI 0.875", abs(vals["CPI"] - 0.8333) < 1e-4 and vals["SPI"] == 0.875)
check("EVM: EAC 120000, ETC 78000, VAC -20000",
      round(vals["EAC"]) == 120000 and round(vals["ETC"]) == 78000 and round(vals["VAC"]) == -20000)
check("EVM: TCPI 1.1207", abs(vals["TCPI"] - 1.1207) < 1e-4)
check("page states the EVM results",
      "CV = -7,000" in ch3 and "SV = -5,000" in ch3 and "CPI = 0.8333" in ch3
      and "SPI = 0.875" in ch3 and "EAC = $120,000" in ch3 and "ETC = $78,000" in ch3
      and "VAC = -20,000" in ch3 and "1.1207" in ch3)
check("risk: 30% of $20,000 = $6,000", F(3, 10) * 20000 == 6000 and "expected value of $6,000" in ch3)

ch1 = pages.get("b27-ch01-organizational-theory-and-behavior.html", "")
check("expectancy example: 0.8 x 0.5 x 6 = 2.4", abs(0.8 * 0.5 * 6 - 2.4) < 1e-9 and "= 2.4" in ch1)

# ---- honesty markers
ch2 = pages.get("b27-ch02-business-law-ethics-csr.html", "")
idx = pages.get("index.html", "")
for name, h in (("ch1", ch1), ("ch2", ch2), ("ch3", ch3), ("index", idx)):
    check(f"{name} carries the study-aid / reading-status statement",
          "not read" in h or "have not read" in h or "has not read" in h or "do not name a textbook" in h)
check("ch1 flags the disagreement between two official pages", "two official pages disagree" in ch1 and 'class="tag">to confirm' in ch1)
check("ch2 says it is not legal advice", "not legal advice" in ch2)
check("ch2 says cases must be re-read in a primary source", "primary source" in ch2)
check("ch3 flags the guessed planning split as to confirm", "to confirm" in ch3 and "exact split" in ch3)
check("every chapter has the 'sourced' unit-list box", all('<span class="tag">sourced</span>' in h for h in (ch1, ch2, ch3)))
check("every chapter has the study-aid box with no-answers statement",
      all("does not contain answers to graded assignments" in h for h in (ch1, ch2, ch3)))
for code in ("5210", "5212", "5214", "5216", "5220", "5224", "5226", "5228", "5230", "5240", "5250", "5260", "5270", "5910", "5113", "5115", "5611"):
    check(f"index lists course {code}", code in idx)
check("index flags the capstone rule and the BUS 5611 prerequisite as to confirm", "B-" in idx and "prerequisite of BUS 5611" in idx and idx.count("to confirm") >= 2)

print()
print("ALL PASS" if fails == 0 else f"{fails} FAILED")
sys.exit(1 if fails else 0)
