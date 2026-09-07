#!/usr/bin/env python3
"""
backlinks.py — Principia Orthogona · second-edition worklist

A later note cites the earlier ones it builds on. The earlier note never learns
it was built on, because a first edition cannot point at what happens later.
That is not a defect in the older paper and this tool does not report one.

What it produces is the worklist an edition would fold in: every one-way edge
where A cites B, B is older, and B says nothing about A. Corrections are the
subset worth acting on; extensions are new cross-references the index should
carry. See docs/audit-log.md, "First editions cannot point forward" (2026-09-07).

References count whether they are hyperlinks or prose. A forward pointer that
says "see WP-104" is a forward pointer.

Usage:
    python3 backlinks.py [root]            audit every paper, report one-way citations
    python3 backlinks.py [root] --emit N   print the "Cited later by" block for WP-N

Nothing is written. The emit mode prints HTML for a human to paste.
"""
import os, re, sys, html, collections

ROOT = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else os.path.expanduser("~/mnt/Desktop/geometry")

WP   = re.compile(r'\bWP[-‑\s]?(\d{1,3})\b')
HREF = re.compile(r'href="[^"]*?wp(\d{1,3})[-.]')
NAME = re.compile(r'wp(\d{1,3})[-.]')

def text_of(path):
    s = open(path, encoding='utf-8', errors='replace').read()
    t = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', s)
    return s, html.unescape(re.sub(r'(?s)<[^>]+>', ' ', t))

def emit(pages, cites, n):
    later = sorted(a for a, refs in cites.items() if n in refs and a > n)
    if not later:
        print(f"WP-{n} is not cited by any later paper."); return
    print(f"<!-- paste at the foot of {os.path.basename(pages[n])}, before the references -->")
    print('<div class="eyebrow">Cited later by</div>')
    print('<ul class="lesson-list">' if False else '<ul>')
    for a in later:
        f = os.path.basename(pages[a])
        title = re.sub(r'^wp\d+[-.]', '', f[:-5]).replace('-', ' ')
        print(f'  <li><a href="{f}">WP-{a}</a> &mdash; {title}</li>')
    print('</ul>')

def main():
    pages = {}                      # wp number -> path
    for dirpath, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules', '_to_delete', '.lake')]
        for f in files:
            if not f.endswith('.html'):
                continue
            m = NAME.match(f)
            if m:
                pages.setdefault(int(m.group(1)), os.path.join(dirpath, f))

    cites = {}                      # wp number -> set of wp numbers it refers to
    for n, p in sorted(pages.items()):
        raw, txt = text_of(p)
        s = {int(x) for x in WP.findall(txt)} | {int(x) for x in HREF.findall(raw)}
        cites[n] = {x for x in s if x != n and x in pages}

    if "--emit" in sys.argv:
        emit(pages, cites, int(sys.argv[sys.argv.index("--emit") + 1])); return 0

    print(f"{len(pages)} working papers under {ROOT}\n")
    missing = collections.defaultdict(list)
    for a, refs in cites.items():
        for b in refs:
            if b < a and a not in cites.get(b, set()):
                missing[b].append(a)

    if not missing:
        print("every citation is reciprocated.")
        return 0

    total = sum(len(v) for v in missing.values())
    print(f"{total} one-way citations across {len(missing)} papers.")
    print("Each line: the older paper, and the later papers that cite it without being named back.\n")
    for b in sorted(missing):
        later = ", ".join(f"WP-{a}" for a in sorted(missing[b]))
        print(f"  WP-{b:<4} is cited by {later}")
        print(f"           {os.path.relpath(pages[b], ROOT)}")

    print("\nWhere to start — the hubs, by incoming one-way citations:")
    for b, v in sorted(missing.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:8]:
        print(f"  WP-{b:<4} {len(v):>2} later papers cite it, none named back")

    print("\nBy how far the pointer would have to reach:")
    gaps = collections.Counter(a - b for b, v in missing.items() for a in v)
    for g in sorted(gaps):
        print(f"  {g:>3} paper(s) later : {gaps[g]}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
