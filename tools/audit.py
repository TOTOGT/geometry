#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
audit.py — the standard battery for this repo.

    python3 tools/audit.py book1 book2 ... [--json]
    python3 tools/audit.py --all

WHY THE RESOLVER LOOKS LIKE THIS
--------------------------------
Every rule below exists because a naive version produced a false positive or
missed a real defect during the Aug-2026 sweeps. Do not "simplify" them:

1. `/geometry/...` is SITE-ABSOLUTE, not repo-absolute. Pages serves this repo
   at totogt.github.io/geometry/, so the prefix must be stripped. There are ~900
   such links and all of them resolve. Without this they all read as dead.
2. `href="../"` and bare directory targets resolve to that directory's
   index.html. Normalise before the membership test.
3. Fragments must be split off before the file test, and checked separately
   against the target's ids — a live file with a dead anchor is still a defect
   (book7/wp56 pointed at #schwarzschild, which never existed).
4. Tag balance cannot detect CONCATENATED DOCUMENTS: each document is
   internally balanced, so the stack comes out clean. Count <!DOCTYPE instead.
   That is what found HVEH/index and omega-point-v2-draft.
5. ...but doctypes inside JS template literals are not defects (impa-portal.html
   emits a page from a backtick string). Ignore matches inside <script>.
6. WORKING-PAPER NUMBERS fail in two directions and neither survives `ls`.
   Too low: wp73-dnls-d6-ring was written against a stale memory of the highest
   number and collided with wp73-the-stamp-and-the-triple, which already existed.
   Too high: a session claimed the next free number was 81 when the maximum was
   75 — right shape, right magnitude, no referent, the same failure as an
   asserted DOI. And a third: wp71's footer identified it as "Working Paper 54",
   copied from the file it was drafted from. All three are mechanical to detect
   and none is visible to a tag-balance or link check, because every file
   involved is perfectly well-formed.
   Two false positives shaped these rules on first run. book6/wp56 and
   book7/wp56 are NOT a collision — numbering is per-volume, so 6a compares
   within a directory only. And "Vol VIII begins at WP81" is a legitimate plan,
   not a dangling reference, so 6c is informational: it names forward references
   so a later session cannot mistake one for the next free number, which is
   exactly what happened.
"""
import os, re, sys, json, html
from collections import defaultdict
from urllib.parse import unquote

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SKIP_DIRS = {'.git', '_to_delete', '_archive', 'node_modules'}

# NOTE: SKIP_DIRS controls what gets SCANNED, not what can be LINKED TO.
# _archive/ is deliberately not audited, but 52 links point into it and they are
# valid. Build the resolution set from everything except .git.
ALL_FILES, DIRS = set(), set()
for dp, dns, fns in os.walk(ROOT):
    dns[:] = [d for d in dns if d != '.git']
    for f in fns:
        rel = os.path.relpath(os.path.join(dp, f), ROOT)
        ALL_FILES.add(rel)
        d = os.path.dirname(rel)
        while d:
            DIRS.add(d); d = os.path.dirname(d)

# ---- working-paper index (rule 6) -------------------------------------------
# Built from filenames only. _archive and _to_delete are excluded: a superseded
# copy parked there must not count as a live claim on its number.
WP_RE = re.compile(r'(?:^|/)wp(\d+)[-.]', re.I)
WP_FILES = defaultdict(list)
for _rel in ALL_FILES:
    if _rel.startswith(('_archive/', '_to_delete/')):
        continue
    _m = WP_RE.search(_rel)
    if _m and _rel.lower().endswith(('.html', '.htm')):
        WP_FILES[int(_m.group(1))].append(_rel)
WP_MAX = max(WP_FILES) if WP_FILES else 0

# A file's own claim about which paper it is. Deliberately NOT every mention of
# a WP number — a paper legitimately cites its neighbours. Only the two places
# a document names itself: the provenance block and the footer byline.
WP_SELF = re.compile(r'Working Paper\s*(\d+)|<strong>WP[-\s]?(\d+)</strong>', re.I)

# A prose reference to a number ABOVE the highest that exists. Cannot false-fire
# on a cross-reference to a real paper, because those are all <= WP_MAX.
WP_CITE = re.compile(r'\bWP[-\s]?(\d{1,3})\b')

COMMENT = re.compile(r'<!--.*?-->', re.S)
PRE = re.compile(r'<(pre|code)\b.*?</\1\s*>', re.S | re.I)   # Lean docstrings legitimately use **bold**
SCRIPTSTYLE = re.compile(r'<(script|style)\b.*?</\1\s*>', re.S | re.I)
ATTR = re.compile(r'\b(href|src)\s*=\s*"([^"]*)"', re.I)
TAG = re.compile(r'<(/?)([a-zA-Z][\w:-]*)((?:[^<>"\']|"[^"]*"|\'[^\']*\')*?)(/?)>')
VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source',
        'track','wbr','path','circle','rect','line','use','polygon','polyline','ellipse',
        'stop','image','feoffset','fefunca','animate','text','tspan'}

def blank(m): return ' ' * len(m.group(0))
def strip_noncontent(s): return SCRIPTSTYLE.sub(blank, COMMENT.sub(blank, s))
def strip_code(s):       return PRE.sub(blank, s)

def ids_of(path):
    try: s = open(os.path.join(ROOT, path), encoding='utf-8', errors='replace').read()
    except OSError: return set()
    return set(re.findall(r'\bid\s*=\s*"([^"]+)"', s)) | set(re.findall(r'\bname\s*=\s*"([^"]+)"', s))

def resolve(src, link):
    """-> (kind, target). kind in ok|dead|external|anchor|skip"""
    link = link.strip()
    if not link or link.startswith(('mailto:', 'tel:', 'javascript:', 'data:')): return 'skip', ''
    if link.startswith('#'): return 'anchor', link[1:]
    if re.match(r'^[a-z][a-z0-9+.-]*://', link, re.I): return 'external', link
    path, _, frag = link.partition('#')
    path = unquote(path)
    if not path: return 'anchor', frag
    if path.startswith('/'):
        p = path.lstrip('/')
        if p.startswith('geometry/'): p = p[len('geometry/'):]   # rule 1
        joined = os.path.normpath(p) if p else 'index.html'
    else:
        joined = os.path.normpath(os.path.join(os.path.dirname(src), path))
    if joined in ('.', ''): joined = 'index.html'                # rule 2
    if joined.startswith('..'): return 'escape', joined
    if joined in ALL_FILES: return 'ok', joined + (('#' + frag) if frag else '')
    if joined in DIRS or path.endswith('/'):
        cand = os.path.normpath(os.path.join(joined, 'index.html'))
        if cand in ALL_FILES: return 'ok', cand + (('#' + frag) if frag else '')
    return 'dead', joined

STALE = [(r'\bSubmetido ao IMPA\b|\bSubmitted to IMPA\b', 'IMPA submission (declined 2026)'),
         (r'will collide in 4\.5 billion|colidir[ãa]o em 4[,.]5', 'Milky Way-Andromeda as certain (Sawala 2025: ~50/50)'),
         (r'aplica[çc][õo]es federais em curso', 'federal applications "em curso"'),
         (r'data-mjx-error', 'MathJax render error'),
         (r'979-8-9954416-(?:2-5|4-9|5-6)', 'unallocated/HOLD ISBN')]

def audit(targets):
    files = []
    for t in targets:
        base = os.path.join(ROOT, t)
        if os.path.isfile(base) and t.endswith('.html'): files.append(t); continue
        for dp, dns, fns in os.walk(base):
            dns[:] = [d for d in dns if d not in SKIP_DIRS]
            for f in fns:
                if f.lower().endswith(('.html', '.htm')):
                    files.append(os.path.relpath(os.path.join(dp, f), ROOT))
    files = sorted(set(files))
    F = defaultdict(list)

    # rule 6a — two live files claiming the same working-paper number.
    scanned = set(files)
    for n, paths in sorted(WP_FILES.items()):
        bydir = defaultdict(list)
        for p in paths:
            bydir[os.path.dirname(p)].append(p)
        for d, ps in sorted(bydir.items()):
            if len(ps) > 1 and any(p in scanned for p in ps):
                F['wp_number_collision'].append([n, sorted(ps)])

    for rel in files:
        raw = open(os.path.join(ROOT, rel), encoding='utf-8', errors='replace').read()
        body = strip_noncontent(raw)
        line = lambda i: raw[:i].count('\n') + 1

        if len(re.findall(r'(?i)<!DOCTYPE', body)) > 1:       # rules 4 + 5
            F['concatenated_documents'].append([rel, len(re.findall(r'(?i)<!DOCTYPE', body))])

        links = strip_code(body)   # hrefs inside <pre>/<code> are documentation examples
        for m in ATTR.finditer(links):
            kind, tgt = resolve(rel, m.group(2))
            if kind == 'dead':   F['dead_link'].append([rel, m.group(2), line(m.start())])
            elif kind == 'escape':
                if not m.group(2).startswith('../../AXLE/'):                # benign class 3
                    F['escapes_repo'].append([rel, m.group(2)])
            elif kind == 'ok' and '#' in tgt:                  # rule 3
                f2, frag = tgt.split('#', 1)
                if frag not in ids_of(f2):
                    F['dead_anchor'].append([rel, m.group(2), line(m.start())])

        own = set(re.findall(r'\bid\s*=\s*"([^"]+)"', body)) | set(re.findall(r'\bname\s*=\s*"([^"]+)"', body))
        for m in ATTR.finditer(body):
            v = m.group(2).strip()
            if m.group(1).lower() == 'href' and v.startswith('#') and len(v) > 1 and unquote(v[1:]) not in own:
                F['dead_anchor'].append([rel, v, line(m.start())])

        idl = re.findall(r'\bid\s*=\s*"([^"]+)"', body)
        dup = sorted({i for i in idl if idl.count(i) > 1})
        dup = [d for d in dup if not re.match(r'(DejaVu|matplotlib\.|patch_|axes_|figure_|xtick_|ytick_|legend_|line2d_|text_|PolyCollection|QuadMesh|pathcollection_)', d)]
        if dup: F['duplicate_id'].append([rel, dup[:8]])

        stack = []
        for m in TAG.finditer(body):
            closing, name, _, self_ = m.group(1), m.group(2).lower(), m.group(3), m.group(4)
            if name in VOID or self_: continue
            if not closing: stack.append((name, m.start()))
            elif stack and stack[-1][0] == name: stack.pop()
            elif any(n == name for n, _ in stack):
                while stack and stack[-1][0] != name:
                    n, pos = stack.pop(); F['unclosed_tag'].append([rel, n, line(pos)])
                stack.pop()
            else: F['stray_close'].append([rel, name, line(m.start())])
        for n, pos in stack: F['unclosed_tag'].append([rel, n, line(pos)])

        # rule 6b — the file's own claim about which paper it is.
        _fm = WP_RE.search('/' + rel)
        if _fm:
            _n = int(_fm.group(1))
            _foot = body[body.rfind('<footer'):] if '<footer' in body else body[-4000:]
            _claims = {int(a or b) for a, b in WP_SELF.findall(_foot)}
            for _c in sorted(_claims - {_n}):
                F['wp_self_mismatch'].append([rel, _n, _c])

        # rule 6c — a WP cited above the highest that exists. INFORMATIONAL, not
        # a defect: book7/ch-hamilton legitimately says "Vol VIII begins at WP81",
        # a plan, not a claim about a file. What it catches is the reading error —
        # a later session took that forward reference for the next free number and
        # wrote 81 when the maximum was 75. The number to trust is max(WP_FILES)+1.
        for _m in WP_CITE.finditer(strip_code(body)):
            _c = int(_m.group(1))
            if _c > WP_MAX:
                F['wp_above_max'].append([rel, _c, line(_m.start())])

        prose = strip_code(body)                      # benign class 1
        for m in re.finditer(r'\*\*[^*\n]{1,80}\*\*|<strong>[^<]*\*\*', prose):
            F['markdown_leak'].append([rel, line(m.start()), m.group(0)[:52]])
        for m in re.finditer(r'&(?:amp;)+(?:[a-z]{2,8}|#\d+);', body):
            F['double_escaped'].append([rel, m.group(0), line(m.start())])
        for m in re.finditer(r'Ã[\x80-\xbf]|â€', body):
            F['mojibake'].append([rel, m.group(0), line(m.start())])
        for pat, why in STALE:
            for m in re.finditer(pat, body):
                near = body[max(0, m.start()-400):m.start()+400].lower()
                CORRECTION = ('unallocated', 'n\u00e3o alocada', 'nao alocada', 'reserva',
                              'not a valid fallback', 'no isbn of its own', 'foi retirada',
                              'nenhum', 'reserve number', 'no longer the current',
                              'sawala', 'is no longer', 'n\u00e3o \u00e9 mais', 'revised',
                              'addendum', 'stale premise')
                if any(w in near for w in CORRECTION):       # benign class 2
                    break        # the match IS inside its own correction note, not a live claim
                F['stale_claim'].append([rel, why, line(m.start())]); break
    return files, F

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    as_json = '--json' in sys.argv
    if '--all' in sys.argv or not args:
        # Rule 6: --all must include the ~300 loose HTML files at the repo root.
        # An earlier version walked directories only; the root went unaudited for
        # months and was hiding a concatenated gomc-opus and four parse defects.
        args = sorted([d for d in os.listdir(ROOT)
                       if os.path.isdir(os.path.join(ROOT, d)) and d not in SKIP_DIRS]
                      + [f for f in os.listdir(ROOT) if f.lower().endswith(('.html', '.htm'))])
    files, F = audit(args)
    if as_json:
        print(json.dumps({'scanned': len(files), 'findings': F}, indent=1, ensure_ascii=False))
    else:
        dirs = [a for a in args if not a.lower().endswith(('.html', '.htm'))]
        nroot = len(args) - len(dirs)
        where = ', '.join(dirs) + (f' + {nroot} root files' if nroot else '')
        print(f'{len(files)} html scanned in: {where}')
        if not F: print('  clean')
        for k in sorted(F, key=lambda k: -len(F[k])):
            print(f'  {len(F[k]):5d}  {k}')
