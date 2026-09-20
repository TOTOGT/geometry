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

DECL = os.path.join(ROOT, 'docs', 'unlisted.tsv')

def declared():
    """An unlisted chapter is declared, or it is a finding -- R9's shape."""
    out = {}
    if not os.path.exists(DECL):
        return out
    for line in open(DECL, encoding='utf-8'):
        line = line.rstrip('\n')
        if not line or line.startswith('#') or line.startswith('path\t'):
            continue
        parts = line.split('\t')
        if len(parts) >= 2:
            out[parts[0]] = parts[1]
    return out

def orphans(vol):
    have = linked(vol)
    d = declared()
    return [c for c in chapters(vol)
            if c not in have and d.get('%s/%s' % (vol, c)) not in ('working', 'instrument')
            and ('%s/%s' % (vol, c)) not in d]

def backlog(vol):
    """Declared unfinished and still unlinked. Reported every run: an
    unfinished chapter is work, not noise."""
    have, d = linked(vol), declared()
    return [c for c in chapters(vol)
            if c not in have and d.get('%s/%s' % (vol, c)) == 'unfinished']

def stale_declarations():
    """Declared unlisted, but the index reaches it now. The declaration rots
    otherwise, and a stale declaration hides a page that came back."""
    out = []
    for path, status in declared().items():
        vol, _, name = path.partition('/')
        if os.path.isdir(os.path.join(ROOT, vol)) and name in linked(vol):
            out.append((path, status))
    return out

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
            print('             ORPHAN   %s/%s  (undeclared)' % (vol, f))
        for f in backlog(vol):
            print('             backlog  %s/%s  unfinished' % (vol, f))
    nb = sum(len(backlog(v)) for v in vols)
    print('\n  %d undeclared orphan(s), %d unfinished chapter(s) waiting, in %d volume(s)'
          % (total, nb, len(vols)))
    missing = [d for d in sorted(os.listdir(ROOT))
               if re.match(r'^book\d+$', d) and os.path.isdir(os.path.join(ROOT, d))
               and not os.path.exists(os.path.join(ROOT, d, 'index.html'))]
    for d in missing:
        pages = [f for f in os.listdir(os.path.join(ROOT, d)) if f.endswith('.html')]
        if not pages:
            print('  reserved  %s is an empty directory -- a rung with no pages yet,'
                  ' not a finding' % d)
            continue
        print('  NO INDEX  %s holds %d page(s) and no index.html, so nothing'
              ' here can audit it' % (d, len(pages)))
        total += 1
    d = declared()
    if d:
        by = {}
        for st in d.values():
            by[st] = by.get(st, 0) + 1
        print('  %d declared in docs/unlisted.tsv (%s)'
              % (len(d), ', '.join('%s %d' % (k, v) for k, v in sorted(by.items()))))
    for path, status in stale_declarations():
        print('  STALE  %s is declared %s but the index reaches it now' % (path, status))
        total += 1
    return 1 if (gate and total) else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
