#!/usr/bin/env python3
"""
Subject tags — the magazine section a chapter files under (MATHEMATICS · PURE,
ECONOMICS · POLICY, HOLOLOGY, ...). Set 2026-09-27 by Pablo.

docs/subjects.tsv is the editorial source: one row per chapter, subject and an
optional secondary. This tool stamps that decision onto the page, between marker
comments, as a visible pill above the first <h1> and as <meta name="po-subject">.
build_indexes.py then reads the tag back off the page (R8, R23).

    python3 tools/subject_tags.py            check: every chapter has a row, every
                                             subject is in VOCAB, every page's stamp
                                             matches its row. exit 1 on any finding
    python3 tools/subject_tags.py --write    stamp / restamp every page (idempotent)
    python3 tools/subject_tags.py --count    subjects by frequency

Standard library only. The chapter set is the one chapter_links.py uses (every
bookNN/*.html except index.html) plus loose root pages carrying <meta name="po-book">.
"""
import glob, html, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TSV = os.path.join(ROOT, 'docs', 'subjects.tsv')

# FIELD -> pill colours (text, background, border). Dark text on a light tint reads on
# both the dark hero pages and the light working-paper pages.
FIELD = {
    'MATHEMATICS': ('#16324f', '#dfeaf4', '#a8c2d8'),
    'PHYSICS':     ('#3b2a63', '#e9e3f6', '#bfb1e0'),
    'CHEMISTRY':   ('#0f4a45', '#dcf1ee', '#9fd3cb'),
    'BIOLOGY':     ('#1f4d1f', '#e2f1dc', '#a9d29c'),
    'MEDICINE':    ('#5c1f2e', '#f6e0e5', '#dfa9b6'),
    'EARTH':       ('#3f4a14', '#eef1d8', '#c9d38c'),
    'ECONOMICS':   ('#5a3a06', '#f7ecd6', '#e0c48a'),
    'BUSINESS':    ('#5a3a06', '#f7ecd6', '#e0c48a'),
    'LAW':         ('#402a1a', '#f0e6dd', '#cdb49e'),
    'COMPUTING':   ('#123f5c', '#dcedf7', '#98c6e2'),
    'ENGINEERING': ('#333333', '#ececec', '#bdbdbd'),
    'HISTORY':     ('#4a2c14', '#f3e7da', '#d6b894'),
    'LITERATURE':  ('#4d1f47', '#f3e0f0', '#d4a6cc'),
    'LINGUISTICS': ('#4d1f47', '#f3e0f0', '#d4a6cc'),
    'PHILOSOPHY':  ('#2c2c54', '#e4e4f4', '#b0b0da'),
    'EDUCATION':   ('#0f4a2f', '#dbf1e5', '#98d2b2'),
    'METHOD':      ('#3a3a3a', '#efece4', '#c9c2ad'),
    'HOLOLOGY':    ('#4a3300', '#fdf0c8', '#e5bf4f'),
    'PROFILE':     ('#3a3a3a', '#ffffff', '#b5b5b5'),
}

VOCAB = {
    'MATHEMATICS · PURE', 'MATHEMATICS · APPLIED', 'MATHEMATICS · FOUNDATIONS',
    'MATHEMATICS · FORMAL VERIFICATION',
    'PHYSICS · THEORETICAL', 'PHYSICS · QUANTUM', 'PHYSICS · COSMOLOGY',
    'PHYSICS · CONDENSED MATTER', 'PHYSICS · PLASMA', 'PHYSICS · PLANETARY', 'PHYSICS · ACOUSTICS',
    'CHEMISTRY', 'CHEMISTRY · CATALYSIS', 'CHEMISTRY · MATERIALS',
    'BIOLOGY · MOLECULAR', 'BIOLOGY · SYSTEMS', 'MEDICINE', 'MEDICINE · NUTRITION',
    'EARTH · CLIMATE',
    'ECONOMICS · MARKETS', 'ECONOMICS · DEVELOPMENT', 'ECONOMICS · POLICY',
    'BUSINESS · VENTURE', 'LAW · POLICY',
    'COMPUTING · THEORY', 'COMPUTING · MACHINE LEARNING', 'ENGINEERING',
    'HISTORY · SCIENCE', 'HISTORY · MATHEMATICS', 'LITERATURE · WRITERS', 'LINGUISTICS',
    'PHILOSOPHY', 'EDUCATION', 'EDUCATION · ENGLISH FOR RESEARCHERS',
    'METHOD · SELF-AUDIT', 'HOLOLOGY', 'PROFILE', 'SERIES APPARATUS',
}
NO_PILL = {'SERIES APPARATUS'}

BEGIN, END = '<!--po-subject-->', '<!--/po-subject-->'
BLOCK = re.compile(re.escape(BEGIN) + r'.*?' + re.escape(END) + r'\n?', re.S)
H1 = re.compile(r'<h1\b', re.I)
BODY = re.compile(r'<body\b[^>]*>', re.I)
HEAD_END = re.compile(r'</head>', re.I)


def chapters():
    out = []
    for d in sorted(glob.glob(os.path.join(ROOT, 'book*'))):
        if not re.match(r'^book\d+$', os.path.basename(d)):
            continue
        for f in sorted(os.listdir(d)):
            if f.endswith('.html') and f != 'index.html':
                out.append(os.path.basename(d) + '/' + f)
    for f in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
        if 'name="po-book"' in open(f, encoding='utf-8', errors='replace').read(8000):
            out.append(os.path.basename(f))
    return out


def rows():
    out = {}
    for line in open(TSV, encoding='utf-8'):
        line = line.rstrip('\n')
        if not line or line.startswith('#') or line.startswith('path\t'):
            continue
        p = line.split('\t') + ['', '', '']
        out[p[0]] = (p[1].strip(), p[2].strip())
    return out


def pill(subject):
    fam = 'PROFILE' if subject == 'PROFILE' else subject.split(' · ')[0]
    fg, bg, bd = FIELD.get(fam, FIELD['METHOD'])
    return (f'<span class="po-subject-tag" style="display:inline-block;font-family:ui-monospace,Menlo,monospace;'
            f'font-size:.62rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;'
            f'color:{fg};background:{bg};border:1px solid {bd};border-radius:3px;'
            f'padding:.22rem .6rem;margin:0 .4rem .4rem 0;line-height:1.3">{html.escape(subject)}</span>')


def stamp(src, subject, secondary):
    src = BLOCK.sub('', src)
    meta = f'<meta name="po-subject" content="{html.escape(subject)}">'
    if secondary:
        meta += f'<meta name="po-subject-2" content="{html.escape(secondary)}">'
    # a head-less fragment page (wp76 is one) gets its meta after </title>, else at the top
    m = HEAD_END.search(src)
    if m:
        at = m.start()
    else:
        t = re.search(r'</title>', src, re.I)
        at = t.end() if t else 0
    src = src[:at] + BEGIN + meta + END + '\n' + src[at:]
    if subject in NO_PILL:
        return src
    tags = pill(subject) + (pill(secondary) if secondary and secondary not in NO_PILL else '')
    block = (f'{BEGIN}<div class="po-subject" style="margin:0 0 .6rem;text-align:inherit" '
             f'aria-label="Section">{tags}</div>{END}\n')
    body = BODY.search(src)
    start = body.end() if body else 0
    h = H1.search(src, start)
    at = h.start() if h else start
    return src[:at] + block + src[at:]


def on_page(src):
    m = re.search(r'<meta name="po-subject" content="([^"]*)">', src)
    m2 = re.search(r'<meta name="po-subject-2" content="([^"]*)">', src)
    return (html.unescape(m.group(1)) if m else '', html.unescape(m2.group(1)) if m2 else '')


def main():
    write = '--write' in sys.argv
    table = rows()
    chs = chapters()
    findings = []
    for p in chs:
        if p not in table:
            findings.append(f'no row      {p}  (add it to docs/subjects.tsv)')
    for p, (a, b) in table.items():
        for s in (a, b):
            if s and s not in VOCAB:
                findings.append(f'unknown     {p}  "{s}"  (not in VOCAB)')
        if not os.path.exists(os.path.join(ROOT, p)):
            findings.append(f'no file     {p}')
    if '--count' in sys.argv:
        from collections import Counter
        c = Counter(a for a, _ in table.values())
        for k, v in c.most_common():
            print(f'{v:5}  {k}')
        c2 = Counter(b for _, b in table.values() if b)
        print('secondary:', ', '.join(f'{k} {v}' for k, v in c2.most_common()))
        return 0
    changed = 0
    for p, (a, b) in sorted(table.items()):
        path = os.path.join(ROOT, p)
        if not os.path.exists(path) or a not in VOCAB or (b and b not in VOCAB):
            continue
        src = open(path, encoding='utf-8', errors='replace').read()
        if write:
            new = stamp(src, a, b)
            if new != src:
                open(path, 'w', encoding='utf-8').write(new)
                changed += 1
        elif on_page(src) != (a, b):
            findings.append(f'stale stamp {p}  page says {on_page(src)}, tsv says {(a, b)}')
    for f in findings:
        print(f)
    print(f'{len(chs)} chapters, {len(table)} rows, {len(findings)} finding(s)'
          + (f', {changed} page(s) stamped' if write else ''))
    return 1 if findings and not write else 0


if __name__ == '__main__':
    sys.exit(main())
