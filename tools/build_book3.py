#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
build_book3.py — keep Book 3's curriculum and the pages that display it in sync.

Book 3 (Vol III, The Mini-Beast) is a *living book*: it grows weekly, alongside the
Imaginary Origin journal (AXLE/Journal, published Saturdays). A hand-maintained
chapter roster in a living book is stale by construction, not by neglect.

  tools/book3_roster.json   the curated curriculum — SINGLE SOURCE OF TRUTH
  journey.html              Student Journey Map     (generated from the roster)
  chapters-diagram.html     All Chapters            (checked against the roster)

WHAT IS CURATED VS WHAT IS DERIVED — the distinction that matters
-----------------------------------------------------------------
Reading order, pass, week, CEFR level and discussion topics are *editorial*. No crawl
can infer them, and regenerating them from the filesystem would destroy the teaching.
They live in the JSON and only a human changes them.

Completeness is *derived*: whether every chapter's file exists, and which Book 3 files
on disk are not yet on the taught path. That is checked here, every run.

USAGE
    python3 tools/build_book3.py            # report drift only, change nothing
    python3 tools/build_book3.py --write    # also rewrite journey.html's CH array

Exit status is 1 when drift is found, so it can gate a weekly check.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROSTER = ROOT / "tools" / "book3_roster.json"
JOURNEY = ROOT / "journey.html"
DIAGRAM = ROOT / "chapters-diagram.html"

# Files that mention Book 3 but are hubs//front matter, not candidate chapters.
NOT_CHAPTERS = {
    "index.html", "journey.html", "chapters-diagram.html", "living-book.html",
    "series-hub.html", "classroom-index.html", "master-index.html", "pi.html",
}
MARKERS = re.compile(r"Book\s*3\b|Book\s*III\b|Vol\.?\s*III\b|Mini-?Beast", re.I)


def load_roster() -> dict:
    return json.loads(ROSTER.read_text(encoding="utf-8"))


def js_array(chapters: list[dict]) -> str:
    """Render the curriculum back into the JS literal journey.html expects."""
    def q(s: str) -> str:
        return "'" + str(s).replace("\\", "\\\\").replace("'", "\\'") + "'"

    out = []
    for c in chapters:
        topics = ",".join(q(t) for t in c.get("topics", []))
        out.append(
            "  {n:%d, f:%s, t:%s, s:%s, eq:%s, ph:%s, lv:%s, cv:%s, wk:%d,\n"
            "   desc:%s,\n   topics:[%s]}"
            % (c["n"], q(c["f"]), q(c["t"]), q(c["s"]), q(c["eq"]), q(c["ph"]),
               q(c["lv"]), c["cv"], c["wk"], q(c["desc"]), topics))
    return "[\n" + ",\n".join(out) + "\n]"


def replace_ch_array(html: str, new_array: str) -> str:
    i = html.find("const CH=")
    if i == -1:
        raise SystemExit("journey.html: 'const CH=' not found — page structure changed")
    start = html.index("[", i)
    depth = 0
    for j in range(start, len(html)):
        if html[j] == "[":
            depth += 1
        elif html[j] == "]":
            depth -= 1
            if depth == 0:
                break
    return html[:start] + new_array + html[j + 1:]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true",
                    help="rewrite journey.html's CH array from the roster")
    args = ap.parse_args()

    roster = load_roster()
    chapters = roster["chapters"]
    files = [c["f"] for c in chapters]
    drift = False

    print(f"Book 3 roster: {len(chapters)} chapters, weeks "
          f"{min(c['wk'] for c in chapters)}–{max(c['wk'] for c in chapters)}")

    # 1. does every curriculum file exist?
    missing = [f for f in files if not (ROOT / f).exists()]
    if missing:
        drift = True
        print(f"\n  MISSING on disk ({len(missing)}) — roster points at files that are gone:")
        for f in missing:
            print(f"    {f}")
    else:
        print("  all curriculum files present on disk")

    # 2. duplicate ordering / numbering
    ns = [c["n"] for c in chapters]
    if len(set(ns)) != len(ns) or sorted(ns) != list(range(1, len(ns) + 1)):
        drift = True
        print(f"\n  ORDER BROKEN: n values are not 1..{len(ns)} without gaps")

    # 3. the count the page advertises
    if roster.get("chapter_count") != len(chapters):
        drift = True
        print(f"\n  COUNT STALE: chapter_count={roster.get('chapter_count')} "
              f"but there are {len(chapters)} chapters")

    # 4. Book 3 material on disk that is not on the taught path — the growth edge
    on_path = set(files)
    candidates = []
    for p in sorted(ROOT.glob("*.html")):
        rel = p.name
        if rel in on_path or rel in NOT_CHAPTERS or rel.startswith("index-"):
            continue
        if MARKERS.search(p.read_text(encoding="utf-8", errors="replace")[:4000]):
            candidates.append(rel)
    if candidates:
        print(f"\n  NOT YET ON THE TAUGHT PATH ({len(candidates)}) — Book 3 material on "
              f"disk but absent from the curriculum. Not an error: this is the growth\n"
              f"  edge, and what to pick from each week.")
        for c in candidates[:20]:
            print(f"    {c}")
        if len(candidates) > 20:
            print(f"    … and {len(candidates) - 20} more")

    # 5. does chapters-diagram show every taught chapter?
    if DIAGRAM.exists():
        d = DIAGRAM.read_text(encoding="utf-8", errors="replace")
        absent = [f for f in files if f not in d]
        if absent:
            drift = True
            print(f"\n  chapters-diagram.html omits {len(absent)} taught chapter(s):")
            for f in absent:
                print(f"    {f}")
        else:
            print("  chapters-diagram.html lists every taught chapter")

    # 6. optionally push the roster back into journey.html
    if args.write:
        html = JOURNEY.read_text(encoding="utf-8")
        new = replace_ch_array(html, js_array(chapters))
        new = re.sub(r"(<title>[^<]*?·\s*)\d+(\s*chapters)", rf"\g<1>{len(chapters)}\g<2>", new)
        if new != html:
            JOURNEY.write_text(new, encoding="utf-8")
            print(f"\n  journey.html rewritten from the roster ({len(chapters)} chapters)")
        else:
            print("\n  journey.html already matches the roster")

    print("\nDRIFT FOUND" if drift else "\nin sync")
    sys.exit(1 if drift else 0)


if __name__ == "__main__":
    main()
