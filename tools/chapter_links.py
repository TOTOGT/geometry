#!/usr/bin/env python3
"""
Every chapter in a volume should be reachable from that volume's index, and
every link in the index should land on a file that exists.

audit.py already finds the second kind (dead_link). This finds the first:
a chapter file sitting in bookNN/ that nothing in bookNN/index.html points
at. Written a chapter, forgot the card -- twice in one week -- and there was
no instrument that could say so.

It also refuses a name collision, which is the other way a chapter goes
missing: a new file written to a path that is already taken silently
replaces a published chapter, and git reports it as an edit, not a loss.

    python3 tools/chapter_links.py              report every volume, exit 0
    python3 tools/chapter_links.py book7        gate one volume, exit 1 on orphans
    python3 tools/chapter_links.py book7 ch-x.html ch-y.html
                                                refuse if those names are taken

Standard library only.
"""

import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def volumes():
    out = []
    for name in sorted(os.listdir(ROOT)):
        d = os.path.join(ROOT, name)
        if re.match(r'^book\d+$', name) and os.path.isdir(d) \
           and os.path.exists(os.path.join(d, 'index.html')):
            out.append(name)
    return out

def chapters(vol):
    d = os.path.join(ROOT, vol)
    return sorted(f for f in os.listdir(d)
                  if f.endswith('.html') and f != 'index.html')

def linked(vol, depth=1):
    """Pages reachable from the volume index, following local .html links one
    hop by default.

    One hop matters. book4/index.html is a 2 KB cover that links only to
    contents.html, and 62 of this script's first run's 75 "orphans" were book4
    chapters listed there. Reading index.html alone and reporting the rest
    absent is R15 -- never report absence from a single search -- committed by
    the instrument written to find missing links."""
    seen, frontier = set(), ['index.html']
    for _ in range(depth + 1):
        nxt = []
        for page in frontier:
            path = os.path.join(ROOT, vol, page)
            if page in seen or not os.path.exists(path):
                continue
            seen.add(page)
            for href in re.findall(r'href="([^"#?]+\.html)"', open(path, encoding='utf-8', errors='replace').read()):
                if '/' not in href:
                    nxt.append(href)
        frontier = nxt
    return seen | set(frontier)

def orphans(vol):
    have = linked(vol)
    return [c for c in chapters(vol) if c not in have]

def main(argv):
    # collision guard
    if len(argv) > 2:
        vol, names = argv[1], argv[2:]
        taken = [n for n in names if os.path.exists(os.path.join(ROOT, vol, n))]
        for n in names:
            print('    %s  %s/%s' % ('TAKEN' if n in taken else 'free ', vol, n))
        if taken:
            print('\n  REFUSED: %d name(s) already in use. Writing there replaces a'
                  ' published chapter and git will report it as an edit.' % len(taken))
            return 1
        print('\n  clear')
        return 0

    vols = [argv[1]] if len(argv) == 2 else volumes()
    gate = len(argv) == 2
    total = 0
    for vol in vols:
        o = orphans(vol)
        total += len(o)
        print('  %-8s  %3d chapters, %3d linked from index, %d orphaned'
              % (vol, len(chapters(vol)), len(linked(vol) & set(chapters(vol))), len(o)))
        for f in o:
            print('             orphan  %s/%s' % (vol, f))
    print('\n  %d orphaned chapter(s) in %d volume(s)' % (total, len(vols)))
    return 1 if (gate and total) else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
