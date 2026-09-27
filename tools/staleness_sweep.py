#!/usr/bin/env python3
"""
staleness_sweep.py -- find citations of a withdrawn claim that were never updated.

WHY THIS EXISTS.  A corpus this size cannot be re-read end to end every time
one file withdraws a claim (G6Crystal.lean's Schumann-resonance section,
2026-09-11, is the case that motivated this: chW-wigner.html kept asserting
the withdrawn coupling for sixteen days because nobody re-swept the corpus
for its keywords -- not a lapse in vigilance, a bandwidth limit). This script
is the sweep, run in seconds instead of by hand.

HOW IT WORKS.  tools/withdrawn_claims.json is a short, hand-maintained list:
one entry per withdrawal, each with the keywords that mark the withdrawn
claim (pulled from the withdrawal's own comment -- no new tagging convention
required). This script greps every tracked .lean/.html/.md file for those
keywords and reports every hit outside the source file, flagging any file
that does not itself contain an acknowledgment word (withdrawn / retracted /
corrected / superseded / deprecated) nearby.

WHAT THIS DOES NOT DO.  It does not know a hit is actually stale -- a file
that quotes the withdrawn claim to explain the history (like this script's
own docstring) will be flagged too. It narrows thousands of pages to a short
list for a human to read, which is the actual bottleneck this fixes.

Usage: python3 tools/staleness_sweep.py [--json]
Exit code: 1 if any unacknowledged stale hit is found, 0 otherwise.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = REPO_ROOT / "tools" / "withdrawn_claims.json"
TRACKED_EXTS = (".lean", ".html", ".md")
ACK_WORDS = re.compile(r"withdrawn|retracted|corrected|superseded|deprecated", re.I)


def tracked_files():
    out = subprocess.run(
        ["git", "ls-files"], cwd=REPO_ROOT, capture_output=True, text=True, check=True
    ).stdout.splitlines()
    return [
        f for f in out
        if f.endswith(TRACKED_EXTS) and not f.startswith(".lake/") and "/.lake/" not in f
    ]


def find_hits(keyword, files):
    # word-ish boundary; keywords may contain '.', '_' so keep it simple/tolerant
    pat = re.compile(re.escape(keyword), re.I)
    hits = []
    for f in files:
        p = REPO_ROOT / f
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if pat.search(text):
            hits.append(f)
    return hits


def main():
    as_json = "--json" in sys.argv
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    files = tracked_files()
    report = []
    any_stale = False

    for entry in manifest:
        source = entry["source"]
        seen_files = {}
        for kw in entry["keywords"]:
            for f in find_hits(kw, files):
                seen_files.setdefault(f, set()).add(kw)

        for f, kws in sorted(seen_files.items()):
            if f == source:
                continue
            text = (REPO_ROOT / f).read_text(encoding="utf-8", errors="ignore")
            acknowledged = bool(ACK_WORDS.search(text))
            if not acknowledged:
                any_stale = True
            report.append({
                "withdrawal_id": entry["id"],
                "withdrawn_date": entry["date"],
                "source": source,
                "file": f,
                "keywords_matched": sorted(kws),
                "acknowledged_in_file": acknowledged,
            })

    if as_json:
        print(json.dumps(report, indent=2))
    else:
        print(f"staleness_sweep: {len(manifest)} withdrawal(s) tracked, "
              f"{len(files)} files scanned\n")
        if not report:
            print("No citations of any withdrawn claim found outside their source file.")
        for row in report:
            flag = "STALE -- no acknowledgment found" if not row["acknowledged_in_file"] else "cites, but acknowledges"
            print(f"[{flag}]")
            print(f"  file:      {row['file']}")
            print(f"  withdrawn: {row['withdrawal_id']} ({row['withdrawn_date']}) -- see {row['source']}")
            print(f"  keywords:  {', '.join(row['keywords_matched'])}")
            print()

    sys.exit(1 if any_stale else 0)


if __name__ == "__main__":
    main()
