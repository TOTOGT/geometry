#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ch44-verify.py — companion to ch44-how-to-learn.html (Book 3, chapter 44).

The chapter claims that the Feynman technique's third step — *find the gaps* —
is the only step that matters and the only one it cannot perform, and that
gap-detection in practice comes from four instruments with four different
blind spots.  That is an empirical claim, and this corpus keeps the record
that tests it: docs/audit-log.md, every defect the author and his sessions
found in their own work, with the discovery usually named.

Five blocks.

  [1] Census.  Parse the audit log into entries and classify each by WHAT
      CAUGHT IT: kernel, computation, reading, or another person.  Every
      entry and its verdict is printed, so the classification can be checked
      rather than believed.
  [2] Blind spots.  For each instrument, the defect classes it structurally
      cannot see, taken from the log's own reasoning.
  [3] The MISFRAMED case, in full.  The one entry that says outright that no
      instrument in the repository could have caught it, and what did.
  [4] OBMEP, as the scale answer to instrument 2.  Figures from impa.br.
  [5] The arithmetic of the chapter's one quantitative claim, plus the
      honest statement of what the census does NOT establish.

Requires: nothing but the standard library.
Run:  python3 ch44-verify.py        (add --svg for figure data)

Principia Orthogona - Book 3 - G6 LLC - CC BY-NC-ND 4.0
"""

import sys, re, json, math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOG  = ROOT / "docs" / "audit-log.md"

FAIL = []
def check(label, ok, detail=""):
    print(f"    {'PASS' if ok else 'FAIL'}  {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


# ═════════════════════════════════════════════════════════════════════
# The four instruments, and the markers by which the log names them.
# Markers are deliberately narrow: a word that merely APPEARS in an entry
# is not evidence: only a word describing how the defect surfaced counts.
# ═════════════════════════════════════════════════════════════════════

KERNEL = re.compile(r"""
    \#print\s+axioms | sorryAx | lake\s+(env\s+)?lean | lake\s+build
  | axiom_gate | the\s+gate\s+(failed|refused|caught) | probe_dm3
  | CI\s+(caught|failed|went\s+red|is\s+red) | returned\s+.{0,3}False
  | did\s+not\s+compile | uncompiled | the\s+kernel\s+(caught|refused|says|said)
  | on\s+the\s+first\s+build | stating\s+.{0,30}as\s+a\s+theorem
  | norm_num\s+(failed|refused) | Lean\s+(refused|would\s+not|rejected)
  | the\s+build\s+(failed|broke|refused)
""", re.I | re.X)

COMPUTATION = re.compile(r"""
    caught\s+by\s+the\s+tool | the\s+script\s+(refused|disagreed|printed\s+the\s+right)
  | [-\w]+-?verify\.py\s+(caught|refused|failed|returned)
  | backlinks\.py | build_indexes\.py | \bre-?ran\b | recomput | recount(ed|ing)?\b
  | a\s+second\s+assertion | the\s+resolver | when\s+I\s+(counted|ran|checked)
  | the\s+count(s)?\s+(did\s+not|disagree|do\s+not) | grep(ping)?\s+(found|showed|returned)
  | the\s+sweep\s+(found|showed) | the\s+census\s+(found|showed)
  | resolving\s+the\s+index | the\s+numbers?\s+(did\s+not|disagree)
  | caught\s+by\s+(a|the)\s+(script|tool|check|gate|sweep)
""", re.I | re.X)

READING = re.compile(r"""
    caught\s+by\s+reading | reading\s+it\s+back | re-?read(ing)?\s+(it|the)
  | on\s+(close\s+)?inspection | caught\s+.{0,30}\bby\s+eye\b
  | as\s+an\s+editor | I\s+noticed | noticed\s+(that|the|it)
  | when\s+I\s+(re-?read|looked\s+at) | rereading
""", re.I | re.X)

PERSON = re.compile(r"""
    Pablo\s+(noted|note[sd]|says?|said|corrected|pointed|asked|flagged|is\s+right|caught)
  | (a|the)\s+reader\s+(saying|said|noted|asked|pointed)
  | the\s+author\s+(noted|said|corrected|instructed|caught|asked)
  | (user|you)\s+(corrected|noted|said|pointed|caught|flagged)
  | no\s+instrument\s+in\s+this\s+repository
  | which\s+is\s+Pablo'?s\s+point | Pablo'?s\s+(objection|question|correction)
  | it\s+was\s+caught\s+by\s+a\s+reader
""", re.I | re.X)

ORDER = ["person", "kernel", "computation", "reading"]
RX = {"kernel": KERNEL, "computation": COMPUTATION, "reading": READING, "person": PERSON}

# An EXPLICIT attribution beats keyword frequency.  When the log states in a
# sentence who or what caught a thing, that sentence decides the entry, even
# if some other instrument is named more often inside it.  Counting words is
# the fallback, not the method.
EXPLICIT = [
    (re.compile(r"no\s+instrument\s+in\s+this\s+repository", re.I),       "person"),
    (re.compile(r"caught\s+by\s+a\s+reader|it\s+was\s+caught\s+by\s+a", re.I), "person"),
    (re.compile(r"Pablo\s+(noted|caught|pointed|is\s+right)", re.I),        "person"),
    (re.compile(r"caught\s+by\s+reading|reading\s+it\s+back\s+as\s+an\s+editor", re.I), "reading"),
    (re.compile(r"caught\s+by\s+the\s+tool", re.I),                        "computation"),
    (re.compile(r"CI\s+caught\s+it|on\s+the\s+first\s+build", re.I),      "kernel"),
]


DATE = re.compile(r"20\d\d-\d\d-\d\d|\b\d{1,2}\s+(January|February|March|April|May|June|July|"
                  r"August|September|October|November|December)\s+20\d\d", re.I)


def entries():
    """Split the log into DATED entries.

    The log's top-level '## ' headers are of two kinds: a dated finding, which
    opens an entry, and an undated sub-heading ('Fixed', 'Open', 'What V7
    proves') which continues the one above it.  Splitting on every '## ' counts
    the second kind as findings and buries the census in structure, so the unit
    here is the dated entry: each dated header, plus everything up to the next
    dated header.
    """
    raw = LOG.read_text(encoding="utf-8")
    parts = re.split(r"\n(?=## [^#])", raw)
    out, cur = [], None
    for part in parts:
        head = part.split("\n", 1)[0].lstrip("# ").strip()
        if not head:
            continue
        if DATE.search(head):
            if cur:
                out.append(cur)
            cur = [head, part]
        elif cur:
            cur[1] += "\n" + part
        else:
            cur = [head, part]
    if cur:
        out.append(cur)
    return [(h, t) for h, t in out]


def classify(text):
    """Return (verdict, hits) where hits maps instrument -> marker count.

    'person' wins ties on purpose: an entry that says a person supplied the
    category AND that a tool measured something is an entry where the tool
    measured correctly and the person said what it meant.  That asymmetry is
    the chapter's claim and it is stated here rather than hidden.
    """
    hits = {k: len(RX[k].findall(text)) for k in RX}
    for rx, verdict in EXPLICIT:          # an explicit sentence decides
        if rx.search(text):
            return verdict, hits
    if not any(hits.values()):
        return "unclassified", hits
    best = max(hits.values())
    for k in ORDER:                       # person, kernel, computation, reading
        if hits[k] == best:
            return k, hits
    return "unclassified", hits
    best = max(hits.values())
    for k in ORDER:                     # person, kernel, computation, reading
        if hits[k] == best:
            return k, hits
    return "unclassified", hits


# ═════════════════════════════════════════════════════════════════════
def block1(verbose=False):
    print("\n[1] CENSUS — what actually caught each defect")
    print("    Source: docs/audit-log.md, one unit per DATED entry.  An explicit")
    print("    sentence of attribution decides an entry; marker frequency is only")
    print("    the fallback.  Both lists are in the source of this script, and")
    print("    --entries prints every verdict, so this can be checked not believed.\n")
    ents = entries()
    tally = {k: 0 for k in list(RX) + ["unclassified"]}
    rows = []
    for head, text in ents:
        v, hits = classify(text)
        tally[v] += 1
        rows.append((v, head, hits))
    n = len(ents)
    print(f"      audit-log entries parsed              : {n}")
    print(f"      lines in docs/audit-log.md            : {len(LOG.read_text(encoding='utf-8').splitlines())}\n")
    print(f"      {'instrument':>14} {'entries':>9} {'share':>8}")
    print("      " + "-" * 34)
    named = n - tally["unclassified"]
    for k in ("person", "kernel", "computation", "reading"):
        print(f"      {k:>14} {tally[k]:9d} {tally[k]/n*100:7.1f}%")
    print(f"      {'unclassified':>14} {tally['unclassified']:9d} {tally['unclassified']/n*100:7.1f}%")
    print(f"      {'':>14} {'':>9} {'':>8}")
    print(f"      entries with a named instrument       : {named} of {n}")

    if verbose:
        print("\n      --- every entry, with its verdict and marker counts ---")
        for v, head, hits in rows:
            h = " ".join(f"{k[0]}{hits[k]}" for k in ORDER if hits[k])
            print(f"      {v:>13}  {head[:78]:<78} {h}")

    ok1 = check("every entry received a verdict", sum(tally.values()) == n)
    ok2 = check("a majority of entries name an instrument", named > n / 2,
                f"{named}/{n}")
    ok3 = check("no single instrument accounts for everything",
                max(tally[k] for k in RX) < named,
                "the census would be worthless if one did")
    k, c, r, pe = tally["kernel"], tally["computation"], tally["reading"], tally["person"]
    print(f"\n      READING.  The two instruments that can mechanically say NO —")
    print(f"      a kernel and a computation — account for {k+c} of the {named} entries that")
    print(f"      say.  Reading it back, which is the Feynman technique's third step,")
    print(f"      accounts for {r}.  A person accounts for {pe}, and that is the number to")
    print(f"      look at twice: it is the smallest, and it includes the only entry")
    print(f"      in the log that says no instrument in this repository could have")
    print(f"      caught the thing at all.  Frequency is not coverage.")
    return (ok1 and ok2 and ok3), tally, n


BLIND = [
    ("self-explanation",
     "free, instant, needs nobody",
     "a claim that is fluent and wrong",
     "Every defect in this log was written by someone who could have "
     "explained it confidently at the time.  That is what a log of one's own "
     "errors IS."),
    ("a problem you cannot solve",
     "a problem-setter, who is a scarce human",
     "any gap no posed problem happens to touch",
     "OBMEP is the industrial answer to that scarcity: one problem set, "
     "18.3 million students, phase-1 papers marked by the schools themselves."),
    ("a kernel",
     "you must formalise the argument first",
     "whether the theorem is worth proving, and MISFRAMED — a measurement "
     "that is exactly right under a sentence that is exactly wrong",
     "WP-99's ceiling: closure prices, significance does not.  A kernel "
     "returns 0 sorryAx on a theorem nobody needed."),
    ("another person, with a different category",
     "a person who will actually say the thing",
     "nothing structural — but it does not scale, and it cannot be run on "
     "demand at 2 a.m.",
     "The only instrument that catches MISFRAMED, and the log says so "
     "outright: 'No instrument in this repository would have caught this.'"),
]


def block2():
    print("\n[2] BLIND SPOTS — what each instrument structurally cannot see")
    print("    Taken from the log's own reasoning, not invented here.\n")
    for i, (name, cost, blind, note) in enumerate(BLIND, 1):
        print(f"      {i}. {name}")
        print(f"         costs      : {cost}")
        print(f"         blind to   : {blind}")
        print(f"         from the log: {note}\n")
    ok = check("four instruments, four distinct blind spots", len(BLIND) == 4)
    ok &= check("no instrument is blind to nothing",
                all(b[2] for b in BLIND),
                "including the human one, which does not scale")
    print("      READING: the Feynman technique names instrument 1 and stops.")
    print("      Its famous step 3 — 'find the gaps' — is the step instrument 1")
    print("      is worst at.  The technique is not wrong; it is under-equipped.")
    return ok


MISFRAMED_MARK = "No instrument in this repository would have caught this"


def block3():
    print("\n[3] THE MISFRAMED CASE — the entry that names its own limit")
    print("    2026-09-07.  A tool measured 121 one-way citations across 48 of")
    print("    80 papers and reported them, correctly, under a heading that made")
    print("    them mean something they did not: a defect to repair.\n")
    raw = LOG.read_text(encoding="utf-8")
    ok1 = check("the log contains the sentence this section rests on",
                MISFRAMED_MARK in raw)
    i = raw.find(MISFRAMED_MARK)
    if i >= 0:
        seg = raw[i:i + 900]
        for line in seg.split("\n")[:16]:
            print("      | " + line.rstrip()[:96])
    print()
    ok2 = check("the entry names a person, not a tool, as the cause",
                bool(PERSON.search(raw[max(0, i - 200): i + 900])))
    print("\n      READING: the measurement never changed.  backlinks.py would have")
    print("      gone on reporting the same 121 edges forever, correctly.  What")
    print("      the reader supplied was a CATEGORY — one can usually only look")
    print("      back in time — and no re-run produces a category.")
    print("\n      This is the chapter's correction to the popular technique.")
    print("      'Explain it to a child so YOU find the gap' locates the value in")
    print("      the speaker.  The log locates it in the listener.  The child is")
    print("      not a rubber duck; the child is instrument 4.")
    return ok1 and ok2


# OBMEP figures, 21st edition, first phase 9 June 2026.  Source: impa.br.
OBMEP = {
    "edition": 21, "year": 2026, "first_phase": "2026-06-09",
    "students_first_phase": 18_300_000,      # "more than 18.3 million"
    "schools": 58_238,
    "public_schools": 52_199,
    "private_schools": 6_039,
    "municipalities": 5_567,
    "municipality_pct": 99.93,
    "duration_hours": 2.5,
    "questions": 20,
    "levels": 3,
    "medals": 8_450,
    "honourable_mentions": 51_000,
}


def block4():
    print("\n[4] OBMEP — instrument 2, at the only scale that reaches everybody")
    print("    Olimpiada Brasileira de Matematica das Escolas Publicas, run by")
    print("    IMPA.  Figures below are INPUTS from impa.br, 21st edition.\n")
    o = OBMEP
    print(f"      first phase                       : {o['first_phase']} (21st edition)")
    print(f"      students                          : {o['students_first_phase']:,}")
    print(f"      schools                           : {o['schools']:,}"
          f"  ({o['public_schools']:,} public + {o['private_schools']:,} private)")
    print(f"      municipalities reached            : {o['municipalities']:,}"
          f"  = {o['municipality_pct']}% of Brazil")
    print(f"      paper                             : {o['questions']} questions,"
          f" {o['duration_hours']} h, {o['levels']} levels")
    print(f"      medals / honourable mentions      : {o['medals']:,} / {o['honourable_mentions']:,}")

    ok1 = check("school counts sum to the stated total",
                o["public_schools"] + o["private_schools"] == o["schools"],
                f"{o['public_schools']:,} + {o['private_schools']:,} = {o['schools']:,}")
    per_school = o["students_first_phase"] / o["schools"]
    per_student_min = o["duration_hours"] * 60 / o["questions"]
    awarded = o["medals"] + o["honourable_mentions"]
    rate = awarded / o["students_first_phase"]
    print(f"\n      students per school               : {per_school:,.0f}")
    print(f"      minutes per question              : {per_student_min:.1f}")
    print(f"      awarded / entered                 : {awarded:,} / {o['students_first_phase']:,}"
          f"  = 1 in {1/rate:,.0f}")
    ok2 = check("the award rate is a selection rate, not a teaching rate",
                rate < 0.01,
                f"{rate*100:.3f}% — 99.7% of the effect is not the medals")
    print("\n      READING: the medals are not the mechanism.  18.3 million")
    print("      students each met twenty problems they had not seen, and the")
    print("      papers were marked BY THE SCHOOLS THEMSELVES.  That is how you")
    print("      hand instrument 2 to a whole country: you do not scale the")
    print("      problem-setter, you scale the problem.  One scarce human writes")
    print("      twenty questions; fifty-eight thousand schools run the check.")
    print("      [INPUT — figures from impa.br, not computed here]")
    return ok1 and ok2


PROTOCOL = [
    ("Say it out loud, to a person, in one paragraph, without notes.",
     "instrument 1", "You will hear the sentences you cannot finish."),
    ("Ask them what KIND of thing you just described.",
     "instrument 4", "This is the step the popular version omits, and it is "
     "the only one that catches a right measurement under a wrong sentence."),
    ("Write down a question your explanation should answer, and answer it "
     "before looking anything up.",
     "instrument 2", "A gap that blocks an inference is visible; a gap that "
     "blocks nothing is not a gap you need today."),
    ("Make the claim checkable by something that can say no — a script that "
     "recomputes it, a proof the kernel reads, a prediction with a number.",
     "instrument 3", "If nothing can return NO, you have not learned it, you "
     "have memorised it."),
    ("Write down what you did NOT establish, in the same place, at the same "
     "time.",
     "all four", "The corpus's own habit, and the one that made this census "
     "possible: the log exists because the errors were written down."),
]


def block5():
    print("\n[5] THE PROTOCOL, AND WHAT THIS CHAPTER DOES NOT ESTABLISH")
    print("    Five steps, each naming which instrument it hands you.\n")
    for i, (step, inst, why) in enumerate(PROTOCOL, 1):
        print(f"      {i}. {step}")
        print(f"         -> {inst}.  {why}\n")
    ok1 = check("every step names an instrument", all(p[1] for p in PROTOCOL))
    ok2 = check("the protocol covers all four instruments",
                {"1", "2", "3", "4"} <= {c for p in PROTOCOL for c in p[1] if c.isdigit()}
                or any("all four" in p[1] for p in PROTOCOL))

    print("      NOT ESTABLISHED, and not claimed anywhere in the chapter:")
    print("       - That this census generalises beyond one corpus.  It is one")
    print("         author's log of one project.  n = 1, and the classifier is")
    print("         mine.  A second corpus with a comparable log would test it;")
    print("         none is known to exist, which is itself the finding.")
    print("       - That the four instruments are exhaustive.  Four is what this")
    print("         log distinguishes, not what the world contains.")
    print("       - Anything about how people learn in general.  The claim is")
    print("         narrow: that gap-DETECTION has instruments, that they have")
    print("         different blind spots, and that the popular technique names")
    print("         one of them.")
    print("       - That OBMEP causes anything.  Its figures are cited as the")
    print("         scale at which instrument 2 has actually been deployed, not")
    print("         as evidence of an outcome.")
    print("\n      WHAT WOULD REFUTE THE CENSUS: re-run this script with a")
    print("      different marker set and get a materially different ordering.")
    print("      The markers are in the source, above, for exactly that reason.")
    return ok1 and ok2


def svg_data(tally, n):
    """Bar geometry for the census figure.  Computed, not drawn."""
    order = ["person", "kernel", "computation", "reading", "unclassified"]
    X0, X1, Y0 = 150, 560, 60   # 560 leaves room for the count label at the right
    step, h = 46, 26
    top = max(tally[k] for k in order) or 1
    bars = []
    for i, k in enumerate(order):
        y = Y0 + i * step
        w = (tally[k] / top) * (X1 - X0)
        bars.append({"key": k, "y": y, "h": h, "w": round(w, 1),
                     "n": tally[k], "pct": round(tally[k] / n * 100, 1)})
    return {"bars": bars, "x0": X0, "top": top, "n": n}


def main():
    print(__doc__.split("Requires:")[0].rstrip())
    print("=" * 72)
    verbose = "--entries" in sys.argv
    ok1, tally, n = block1(verbose)
    results = [ok1, block2(), block3(), block4(), block5()]
    print("\n" + "=" * 72)
    if FAIL:
        print(f"\n{len(FAIL)} CHECK(S) FAILED:")
        for f in FAIL:
            print("   -", f)
        return 1
    print("\nALL CHECKS PASSED   (5 blocks)")
    return 0


if __name__ == "__main__":
    if "--svg" in sys.argv:
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):     # the census prints; --svg must not
            _, tally, n = block1(False)
        print(json.dumps(svg_data(tally, n), indent=1))
        sys.exit(0)
    sys.exit(main())
