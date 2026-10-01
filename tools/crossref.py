#!/usr/bin/env python3
"""
crossref.py — cross-links between chapters and books. Set 2026-09-27 by Pablo:
"cross link chapters and books when possible".

Every chapter gets a generated "Across the series" box, between marker comments,
listing links it does not already have, in three kinds, strongest first:

  Named here   the page names another chapter in prose -- "WP-64", a Scientist
               Gallery person -- without linking it. The mention is the evidence.
  Cited by     the reverse edge: later pages that name or link THIS one. A first
               edition cannot point forward (backlinks.py, 2026-09-07); this can.
  Same ground  the three nearest pages by vocabulary (TF-IDF cosine over body
               text) that clear a floor, preferring other books. A suggestion,
               labelled as one.

Generated, never hand-edited (R8): change the rules here and re-run.

    python3 tools/crossref.py            check: every chapter's box is current; exit 1 if stale
    python3 tools/crossref.py --write    (re)write every box, idempotent
    python3 tools/crossref.py --show P   print what P's box would hold, with scores

Standard library only. Chapter set and subjects come from tools/subject_tags.py.
"""
import html, math, os, re, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import subject_tags as ST

ROOT = ST.ROOT
BEGIN, END = '<!--po-related-->', '<!--/po-related-->'
BLOCK = re.compile(re.escape(BEGIN) + r'.*?' + re.escape(END) + r'\n?', re.S)
STRIP = re.compile(r'(?is)<(script|style)[^>]*>.*?</\1>')
ROMAN = {1:'I',2:'II',3:'III',4:'IV',5:'V',6:'VI',7:'VII',8:'VIII',10:'X',11:'XI',12:'XII',13:'XIII',
         17:'XVII',18:'XVIII',19:'XIX',20:'XX',21:'XXI',28:'XXVIII',29:'XXIX'}
SIM_FLOOR = 0.15
# surnames shared by two gallery pages, or common words/adjectives: full name only
SURNAME_STOP = {'klein', 'noether', 'thoreau', 'curie', 'ramanujan', 'newton', 'euler', 'hamilton',
                'turing', 'hardy', 'weil', 'bose', 'bak', 'huh', 'levi', 'poe', 'tao', 'thom', 'dirac', 'dyson'}

def book_of(rel, src):
    m = re.match(r'book(\d+)/', rel)
    n = int(m.group(1)) if m else None
    if n is None:
        mm = re.search(r'<meta name="po-book" content="book(\d+)"', src)
        n = int(mm.group(1)) if mm else 3
    return n

def clean_title(src, rel):
    m = re.search(r'<title[^>]*>(.*?)</title>', src, re.S | re.I)
    t = html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip() if m else rel
    t = re.sub(r'\s*[·|—–-]+\s*(Principia Orthogona|Book \w+|G7|G⁶|dm³|Scientist Gallery|The Mini-Beast|Edição Brasil|Book 7: Scientist Gallery).*$', '', t)
    return re.sub(r'\s+', ' ', t).strip() or rel

def body_text(src):
    s = BLOCK.sub('', src)
    s = ST.BLOCK.sub('', s)
    s = STRIP.sub(' ', s)
    return html.unescape(re.sub(r'(?s)<[^>]+>', ' ', s))

def hrefs(src, rel):
    base = os.path.dirname(rel)
    out = set()
    for h in re.findall(r'href="([^"#?]+\.html)', BLOCK.sub('', src)):
        if h.startswith(('http:', 'https:', '//')):
            continue
        out.add(os.path.normpath(os.path.join(base, h)).replace(os.sep, '/'))
    return out

def load():
    rows = ST.rows()
    pages = {}
    for rel in ST.chapters():
        subj = rows.get(rel, ('', ''))[0]
        src = open(os.path.join(ROOT, rel), encoding='utf-8', errors='replace').read()
        if subj == 'SERIES APPARATUS' or 'http-equiv="refresh"' in src.lower():
            continue
        pages[rel] = dict(src=src, title=clean_title(src, rel), book=book_of(rel, src),
                          subj=subj, text=body_text(src), links=hrefs(src, rel))
    return pages

def wp_index(pages):
    by = defaultdict(list)
    for rel in pages:
        m = re.match(r'.*?/wp-?(\d{1,3})[-.]', rel)
        if m:
            by[int(m.group(1))].append(rel)
    return {n: v[0] for n, v in by.items() if len(v) == 1}     # ambiguous numbers are skipped

def people_index(pages):
    out = {}
    for rel, p in pages.items():
        if not rel.startswith('book7/ch-') or p['subj'] == 'SERIES APPARATUS':
            continue
        if rel in NOT_PEOPLE:
            continue
        if rel in ALIASES:
            for n in ALIASES[rel]:
                out.setdefault(n, rel)
            continue
        t = re.sub(r'^(Capítulo|Chapter)\s+\S+\s*·\s*', '', p['title'])
        name = re.split(r'\s*[·:—–]\s*|\s+pela\s+', t)[0].strip()
        if len(name.split()) < 2 and name.lower() in SURNAME_STOP:
            continue
        if name and name not in out:
            out[name] = rel
    return out

NOT_PEOPLE = {'book7/ch-' + x + '.html' for x in (
    '1103-and-26390', 'cross-staff-and-ledger', 'keplers-correspondents', 'ramanujan-1pi', 'rogers-ramanujan',
    'symplectic', 'the-last-of-six', 'the-map-on-page-ten', 'the-salesman', 'tropical', 'what-a-child-can-enter', 'thoreau')}
# gallery pages whose title is not a single person's name
ALIASES = {
    'book7/ch-clapeyron-gibbs.html': ['Clapeyron', 'Josiah Willard Gibbs'],
    'book7/ch-whitehead-russell.html': ['Whitehead and Russell', 'Russell and Whitehead'],
    'book7/ch-mitchison-kirschner.html': ['Mitchison and Kirschner', 'Mitchison & Kirschner'],
    'book7/ch-victora-nussenzweig.html': ['Victora'],
    'book7/ch-thoreau-surveyor.html': ['Henry David Thoreau', 'Thoreau'],
    'book7/ch-escher.html': ['Escher'],
    'book7/ch-curie.html': ['Marie Curie', 'Pierre Curie'],
    'book7/ch-ramanujan.html': ['Srinivasa Ramanujan', 'Ramanujan'],
}

TOK = re.compile(r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ'-]{3,}")
STOP = set('this that with from which their there these those about have been were will would into only also more than such when what where because between after before other same each they them page pages chapter book series here does could should while being over under most many some very then than just even like make made does done used uses using case cases part parts first second third number numbers claim claims result results'.split())

def tfidf(pages):
    docs = {r: Counter(w.lower() for w in TOK.findall(p['text']) if w.lower() not in STOP) for r, p in pages.items()}
    df = Counter(w for c in docs.values() for w in c)
    N = len(docs)
    vec = {}
    for r, c in docs.items():
        v = {w: (1 + math.log(n)) * math.log(N / df[w]) for w, n in c.items() if df[w] > 1 and df[w] < N * 0.3}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1
        vec[r] = {w: x / norm for w, x in v.items()}
    return vec

def cos(a, b):
    if len(a) > len(b): a, b = b, a
    return sum(x * b.get(w, 0) for w, x in a.items())

def plan(pages):
    wps, people = wp_index(pages), people_index(pages)
    named = defaultdict(list)
    for rel, p in pages.items():
        for n in sorted({int(x) for x in re.findall(r'\bWP[-‑\s]?(\d{1,3})\b', p['text'])}):
            t = wps.get(n)
            if t and t != rel:
                named[rel].append((t, f'WP-{n}'))
        for name, t in people.items():
            if t == rel:
                continue
            sur = name.split()[-1]
            hit = (len(name.split()) > 1 and name in p['text']) or (sur.lower() not in SURNAME_STOP and len(sur) >= 5
                                        and len(re.findall(r'\b' + re.escape(sur) + r'\b', p['text'])) >= 2)
            if hit:
                named[rel].append((t, name))
    cited = defaultdict(set)
    for a, lst in named.items():
        for t, _ in lst:
            cited[t].add(a)
    for a, p in pages.items():
        for t in p['links']:
            if t in pages and t != a:
                cited[t].add(a)
    vec = tfidf(pages)
    rels = list(pages)
    out = {}
    for rel, p in pages.items():
        have = p['links'] | {rel}
        n_list, seen = [], set()
        for t, why in named[rel]:
            if t not in have and t not in seen:
                n_list.append((t, why)); seen.add(t)
        c_list = sorted(t for t in cited[rel] if t not in have and t not in seen)
        seen |= set(c_list)
        sims = sorted(((cos(vec[rel], vec[o]), o) for o in rels if o not in have and o not in seen), reverse=True)
        s_list = [(o, s) for s, o in sims if s >= SIM_FLOOR]
        s_list.sort(key=lambda x: (pages[x[0]]['book'] == p['book'], -x[1]))
        out[rel] = (n_list[:6], c_list[:6], s_list[:3])
    return out

def label(pages, t):
    b = pages[t]['book']
    return f'Book {ROMAN.get(b, b)} · {pages[t]["title"]}'

def box(rel, pages, entry):
    n_list, c_list, s_list = entry
    # Definitions line (2026-10-01, Pablo: definitions findable from anywhere): every chapter in a book that has a
    # Chapter 0 points to it. Chapter 0 itself is the target, so it carries no such line.
    d = os.path.dirname(rel)
    has_def = bool(d) and os.path.basename(rel) != 'ch00-definitions.html' \
        and os.path.exists(os.path.join(ROOT, d, 'ch00-definitions.html'))
    if not (n_list or c_list or s_list or has_def):
        return ''
    up = '../' if '/' in rel else ''
    def a(t, extra=''):
        return (f'<li style="margin:.2rem 0"><a href="{up}{t}" style="color:inherit;text-decoration:underline;text-underline-offset:2px">'
                f'{html.escape(label(pages, t))}</a>{extra}</li>')
    parts = []
    if has_def:
        parts.append('<div style="margin:.5rem 0 .2rem;font-size:.7em;letter-spacing:.12em;text-transform:uppercase;opacity:.75">Definitions</div><ul style="margin:0 0 0 1.1rem;padding:0">'
                     '<li style="margin:.2rem 0"><a href="ch00-definitions.html" style="color:inherit;text-decoration:underline;text-underline-offset:2px">Chapter 0 &middot; Definitions and notation for this book</a></li></ul>')
    if n_list:
        parts.append('<div style="margin:.5rem 0 .2rem;font-size:.7em;letter-spacing:.12em;text-transform:uppercase;opacity:.75">Named on this page</div><ul style="margin:0 0 0 1.1rem;padding:0">'
                     + ''.join(a(t, f' <span style="opacity:.6">({html.escape(w)})</span>') for t, w in n_list) + '</ul>')
    if c_list:
        parts.append('<div style="margin:.5rem 0 .2rem;font-size:.7em;letter-spacing:.12em;text-transform:uppercase;opacity:.75">Cited by</div><ul style="margin:0 0 0 1.1rem;padding:0">'
                     + ''.join(a(t) for t in c_list) + '</ul>')
    if s_list:
        parts.append('<div style="margin:.5rem 0 .2rem;font-size:.7em;letter-spacing:.12em;text-transform:uppercase;opacity:.75">Same ground <span style="text-transform:none;letter-spacing:0">&middot; suggested by shared vocabulary</span></div><ul style="margin:0 0 0 1.1rem;padding:0">'
                     + ''.join(a(t) for t, _ in s_list) + '</ul>')
    return (f'{BEGIN}<aside class="po-related" style="max-width:860px;margin:2.2rem auto 1.4rem;padding:1rem 1.25rem;'
            f'border:1px solid rgba(128,128,128,.35);border-left:3px solid rgba(201,168,76,.8);border-radius:0 6px 6px 0;'
            f'background:rgba(128,128,128,.06);font-family:ui-monospace,Menlo,monospace;font-size:.8rem;line-height:1.6">'
            f'<div style="font-size:.72em;letter-spacing:.16em;text-transform:uppercase;opacity:.85">Across the series</div>'
            + ''.join(parts) + f'</aside>{END}\n')

def place(src, b):
    src = BLOCK.sub('', src)
    if not b:
        return src
    for pat in (r'<footer\b', r'</body>'):
        m = list(re.finditer(pat, src, re.I))
        if m:
            i = m[-1].start()
            return src[:i] + b + src[i:]
    return src + b

def main():
    pages = load()
    pl = plan(pages)
    if '--show' in sys.argv:
        r = sys.argv[sys.argv.index('--show') + 1]
        n, c, s = pl[r]
        print('named:', [(t, w) for t, w in n]); print('cited by:', c); print('same ground:', [(t, round(x, 3)) for t, x in s])
        return 0
    write = '--write' in sys.argv
    stale = changed = 0
    tally = Counter()
    for rel, entry in pl.items():
        tally['named'] += len(entry[0]); tally['cited'] += len(entry[1]); tally['same'] += len(entry[2])
        path = os.path.join(ROOT, rel)
        new = place(pages[rel]['src'], box(rel, pages, entry))
        if new != pages[rel]['src']:
            if write:
                open(path, 'w', encoding='utf-8').write(new); changed += 1
            else:
                stale += 1
    print(f'{len(pages)} chapters; links offered: {tally["named"]} named-here, {tally["cited"]} cited-by, '
          f'{tally["same"]} same-ground' + (f'; {changed} page(s) written' if write else f'; {stale} stale'))
    return 1 if stale and not write else 0

if __name__ == '__main__':
    sys.exit(main())
