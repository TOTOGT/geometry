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


# ── per-chapter navigation, generated from the roster ────────────────────────
# The taught order is editorial and lives only in the JSON.  Hand-written prev/next
# in 42 chapters is a derived fact maintained by hand, which is how it drifted: on
# 2026-08-29, 14 chapters navigated by *filename* number instead of taught position,
# ch3-circadian pointed back at ch2.html rather than the roster's ch2-allostatic,
# and ch06-pedagogy had no chapter link at all — a dead end at taught position 21
# of 42.  Generating it is the same rule build_indexes.py states: a derived fact is
# regenerated, never maintained.
NAV_CLASS = "b3nav"
_NAV_RE = re.compile(r'<nav class="b3nav".*?</nav>\n?', re.S)

_A = ("color:inherit;text-decoration:none;border-bottom:1px dotted currentColor;"
      "padding-bottom:1px")


def _cell(c: dict | None, which: str) -> str:
    if c is None:
        return '<span style="opacity:.45">&mdash;</span>'
    import html as _h
    t = _h.escape(c["t"])[:46]
    arrow = f'&larr; {c["n"]} &middot; {t}' if which == "prev" else f'{c["n"]} &middot; {t} &rarr;'
    return f'<a href="{c["f"]}" style="{_A}">{arrow}</a>'


def chapter_nav(chapters: list[dict], i: int) -> str:
    c = chapters[i]
    prev = chapters[i - 1] if i else None
    nxt = chapters[i + 1] if i + 1 < len(chapters) else None
    mid = (f'<span style="opacity:.85">'
           f'<a href="journey.html" style="{_A}">Book 3 &middot; the taught path</a>'
           f' &middot; {c["n"]} of {len(chapters)}'
           f' &middot; week {c["wk"]} &middot; phase {c["ph"]} &middot; {c["lv"]}</span>')
    body = f'  {_cell(prev, "prev")}\n  {mid}\n  {_cell(nxt, "next")}'
    return (f'<nav class="{NAV_CLASS}" style="font:600 10.5px/1.7 ui-sans-serif,system-ui,'
            f'-apple-system,Segoe UI,Helvetica,Arial,sans-serif;letter-spacing:.09em;'
            f'text-transform:uppercase;display:flex;flex-wrap:wrap;gap:.35rem 1.5rem;'
            f'justify-content:space-between;align-items:baseline;padding:.75rem 1.4rem;'
            f'border-bottom:1px solid currentColor;opacity:.7">\n{body}\n</nav>\n')


def write_chapter_navs(chapters: list[dict]) -> int:
    changed = 0
    for i, c in enumerate(chapters):
        path = ROOT / c["f"]
        if not path.exists():
            continue
        html = path.read_text(encoding="utf-8", errors="replace")
        nav = chapter_nav(chapters, i)
        if _NAV_RE.search(html):
            new = _NAV_RE.sub(nav, html, count=1)
        else:
            m = re.search(r"<body[^>]*>", html)
            if m:
                new = html[:m.end()] + "\n" + nav + html[m.end():]
            else:
                ends = list(re.finditer(r"</style>", html))
                if not ends:
                    continue
                e = ends[-1].end()
                new = html[:e] + "\n" + nav + html[e:]
        if new != html:
            path.write_text(new, encoding="utf-8")
            changed += 1
    return changed


def nav_drift(chapters: list[dict]) -> list[tuple]:
    """Chapters missing the generated nav, or carrying a stale one.

    This is the gate, and it is about the GENERATED block only.  Once the nav is
    written from the roster, that block *is* the taught order in the chapter, so
    the gate must be able to go green -- a check that can never pass is ignored
    exactly as fast as one that can never fail.
    """
    out = []
    for i, c in enumerate(chapters):
        path = ROOT / c["f"]
        if not path.exists():
            continue
        html = path.read_text(encoding="utf-8", errors="replace")
        m = _NAV_RE.search(html)
        if not m:
            out.append((c["n"], c["f"], ["no generated nav"]))
        elif m.group(0) != chapter_nav(chapters, i):
            out.append((c["n"], c["f"], ["nav is stale -- rerun with --write"]))
    return out


def legacy_conflicts(chapters: list[dict]) -> list[tuple]:
    """Hand-written links that point somewhere other than the taught neighbour.

    Advisory, not drift.  The generated nav is authoritative; these are older
    in-page links left over from when the order followed filenames.  They are
    reported so they can be cleaned by hand, because the markup around them
    varies too much across 42 chapters to rewrite safely.
    """
    out = []
    for i, c in enumerate(chapters):
        path = ROOT / c["f"]
        if not path.exists():
            continue
        html = _NAV_RE.sub("", path.read_text(encoding="utf-8", errors="replace"))
        prev = chapters[i - 1]["f"] if i else None
        nxt = chapters[i + 1]["f"] if i + 1 < len(chapters) else None
        miss = [x for x in (prev, nxt) if x and x not in html]
        if miss:
            out.append((c["n"], c["f"], miss))
    return out


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

    # 7. is the taught order actually in the chapters?
    nd = nav_drift(chapters)
    if nd:
        drift = True
        print(f"\n  GENERATED NAV MISSING OR STALE ({len(nd)}/{len(chapters)}):")
        for n, f, why in nd[:20]:
            print(f"    {n:>3}  {f:<44} {why[0]}")
        print("  Run with --write to generate it from the roster.")
    else:
        print(f"  all {len(chapters)} chapters carry a current taught-order nav")

    lc = legacy_conflicts(chapters)
    if lc:
        print(f"\n  ADVISORY ({len(lc)}) — older in-page links that do not reach the taught"
              f"\n  neighbour. The generated nav is authoritative; these are legacy markup,"
              f"\n  not drift, and are listed so they can be cleaned by hand:")
        for n, f, miss in lc[:20]:
            print(f"    {n:>3}  {f:<44} {', '.join(miss)}")
        if len(lc) > 20:
            print(f"    … and {len(lc) - 20} more")

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

        n = write_chapter_navs(chapters)
        print(f"  chapter nav written from the roster into {n} of {len(chapters)} chapters")

    print("\nDRIFT FOUND" if drift else "\nin sync")
    sys.exit(1 if drift else 0)


if __name__ == "__main__":
    main()
