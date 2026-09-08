#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
build_rungs.py — keep the dual rung strip honest against its sources.

Seventeen pages carry a two-line strip near the top:

    G3  26 27 28 ... 39   all 44
    G4  0 1 2 ... 26

The numbers are not decoration; they are a claim about where a chapter sits
in a book, and both books grow. Hand-maintaining that claim across seventeen
files means it is stale by construction, which is how it went stale twice:
once when Book 3 gained a chapter mid-sequence and every later number shifted
by one, and again when Book 3 reached 44 and every "all 43" was left behind.

WHAT IS CURATED VS WHAT IS DERIVED — the distinction that matters
-----------------------------------------------------------------
WHICH chapters the G3 rung lists is *editorial*: fourteen out of forty-four,
chosen as a path through the book. This tool never adds or removes a G3 link.

Their NUMBERS and the TOTAL are *derived*, from tools/book3_roster.json, the
same single source of truth build_book3.py uses. Those this tool will fix.

The G4 rung lists Book 4 consecutively from 0, with ONE deliberate omission:
a chapter page does not link to itself. Eleven of the twelve Book 4 chapter
pages carrying the strip follow that rule, and the four non-chapter pages
list the run complete. So the rule is derived from the corpus, not imposed on
it, and the only mechanical repair is removing a self-link. Any other gap is
reported and left alone, because a gap might be a choice.

USAGE
    python3 tools/build_rungs.py            # report drift only, change nothing
    python3 tools/build_rungs.py --write    # apply the derived numbers

Exit status is 1 when drift is found, so it can gate a check.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROSTER = ROOT / "tools" / "book3_roster.json"
SKIP = ("_to_delete", "_archive")

RUNG = re.compile(r'(<div class="rung"><span class="rl">(G\d)</span>)(.*?)(</div>)', re.S)
LINK = re.compile(r'<a href="([^"]+)">([^<]+)</a>')
OWN = {}   # book4 filename -> its own chapter number, filled in main()


def book3_numbers() -> tuple[dict[str, int], int]:
    d = json.loads(ROSTER.read_text(encoding="utf-8"))
    return {c["f"]: c["n"] for c in d["chapters"]}, d["chapter_count"]


def book4_chapters() -> dict[int, str]:
    out = {}
    for p in sorted((ROOT / "book4").glob("*.html")):
        m = re.match(r"ch(\d+)", p.name)
        if m:
            out.setdefault(int(m.group(1)), p.name)
    return out


def fix_block(rung: str, body: str, nums: dict[str, int], total: int,
              b4: dict[int, str], path: Path) -> tuple[str, list[str]]:
    """Return (new_body, notes). Only labels change; hrefs are never invented."""
    notes, new = [], body

    if rung == "G3":
        for href, lab in LINK.findall(body):
            f = href.split("/")[-1]
            if lab.strip().startswith("all"):
                want = f"all {total}"
                if lab != want:
                    notes.append(f"{lab!r} -> {want!r}")
                    new = new.replace(f'<a href="{href}">{lab}</a>',
                                      f'<a href="{href}">{want}</a>')
            elif f not in nums:
                notes.append(f"{f} is linked but is not on the taught path - left alone")
            elif str(nums[f]) != lab:
                notes.append(f"{f}: {lab} -> {nums[f]}")
                new = new.replace(f'<a href="{href}">{lab}</a>',
                                  f'<a href="{href}">{nums[f]}</a>')
        return new, notes

    if rung == "G4":
        links = LINK.findall(body)
        try:
            seen = [int(l) for _, l in links]
        except ValueError:
            notes.append("labels are not all numbers - left alone")
            return new, notes
        own = OWN.get(path.name) if path.parent.name == "book4" else None
        gaps = [n for n in range(max(seen) + 1) if n not in seen]

        if own is not None and own in seen:
            href = next(h for h, l in links if l == str(own))
            notes.append(f"links to itself ({own}) - removed; a page is not its own neighbour")
            new = re.sub(r'\s*<a href="' + re.escape(href) + r'">' + str(own) + r'</a>',
                         "", new, count=1)
        elif own is not None and gaps not in ([], [own]):
            notes.append(f"omits {gaps}, but this page is chapter {own} - left alone")
        elif own is None and gaps:
            notes.append(f"omits {gaps} on a page that is not a Book 4 chapter - left alone")
        return new, notes

    return new, notes


def main() -> int:
    write = "--write" in sys.argv
    nums, total = book3_numbers()
    b4 = book4_chapters()
    # A page's own chapter number comes from its OWN filename. Deriving it by
    # inverting {number: file} silently loses every file whose number is shared
    # with an earlier-sorting sibling (ch11-catgt.html sorts before ch11.html),
    # which is how ch11 and ch15 were first reported as "not a Book 4 chapter".
    for q in (ROOT / "book4").glob("*.html"):
        mm = re.match(r"ch(\d+)", q.name)
        if mm:
            OWN[q.name] = int(mm.group(1))
    print(f"Book 3 roster: {total} chapters   ·   Book 4 on disk: "
          f"{min(b4)}–{max(b4)} ({len(b4)} files)\n")

    files = [p for p in ROOT.rglob("*.html")
             if not any(s in str(p) for s in SKIP)]
    drift, touched = 0, 0
    for p in sorted(files):
        s = p.read_text(encoding="utf-8")
        if 'class="rl">G' not in s:
            continue
        out, notes_all = s, []
        for m in RUNG.finditer(s):
            head, rung, body, tail = m.groups()
            new_body, notes = fix_block(rung, body, nums, total, b4, p)
            if notes:
                notes_all += [f"{rung}: {n}" for n in notes]
            if new_body != body:
                out = out.replace(head + body + tail, head + new_body + tail)
        if notes_all:
            drift += 1
            rel = p.relative_to(ROOT)
            print(f"  {rel}")
            for n in notes_all:
                print(f"      {n}")
        if out != s and write:
            p.write_text(out, encoding="utf-8")
            touched += 1

    print()
    if not drift:
        print("NO DRIFT — every rung number matches its source.")
        return 0
    if write:
        print(f"{touched} file(s) rewritten from the roster and the filesystem.")
        return 0
    print(f"DRIFT FOUND in {drift} file(s). Re-run with --write to fix.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
