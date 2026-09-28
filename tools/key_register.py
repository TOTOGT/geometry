#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
key_register.py -- the series' own dictionary of its operator keys, generated from the pages.

Book XIV ch 4 found that the letters C, K, F, U work as translation keys: one head sense per
key, and a domain-specific filler on each page ("K: portão de Heaviside em pH = 4.5").
This tool writes that finding down as a register and keeps it current (R8: never hand-edit).

    python3 tools/key_register.py            check: exit 1 if the register is stale
    python3 tools/key_register.py --write    regenerate book14/key-register.html and docs/key-register.tsv

For each letter:
  senses     the gloss words ("K: threshold", "U — Union"), Portuguese folded into English
  sense      Book XIV ch 3's rule: glosses joined by a page that uses both are one sense
             (connected components)
  head       the most-used gloss of the largest component
  key set    a component whose pages mostly also name Genesis and Logos (the first two keys of
             the Omega chain G–L–R–U) belongs to that chain, not the dm³ chain
  fillers    the text that follows the gloss on the page, grouped by the page's subject FIELD
             (docs/subjects.tsv): what the key means in that domain

Run order (R25/R26): key_register → subject_tags → run_yourself → crossref → gold_standard.
Standard library only.
"""
import csv, html, os, re, subprocess, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_HTML = os.path.join(ROOT, 'book14', 'key-register.html')
OUT_TSV = os.path.join(ROOT, 'docs', 'key-register.tsv')
RETIRED = ('docs/ml-evidence/', '_archive/', '_to_delete/')
# pages that QUOTE glosses as examples (use/mention): not counted as usage
MENTION = {'book14/ch04-translation-keys.html', 'book14/key-register.html',
           'book14/ch06-words-that-went-wrong.html', 'book14/ch02-how-mathematical-prose-parses.html',
           'book14/ch09-what-types-decide.html'}
SENSES = {
    'C': {'compression': ['compression', 'compress', 'compressão'], 'contact': ['contact']},
    'K': {'threshold': ['threshold', 'limiar'], 'curvature': ['curvature', 'curvatura'],
          'gate': ['gate', 'portão']},
    'F': {'fold': ['fold', 'folding', 'dobramento', 'dobra']},
    'U': {'unfolding': ['unfolding', 'unfold', 'desdobramento'], 'union': ['union', 'união'],
          'universal': ['universal'], 'unification': ['unification', 'unificação']},
}
GEN = re.compile(r'<!--po-(run|gss|related|subject)-->.*?<!--/po-\1-->', re.S)
STY = re.compile(r'<(style|script)\b.*?</\1>', re.S | re.I)
TAG = re.compile(r'<[^>]+>')
# the Omega chain's first two keys; a page naming both is working in that key set
OMEGA_WORDS = (re.compile(r'\bGenesis\b'), re.compile(r'\bLogos\b'))
# a filler ends at a sentence mark, a separator, or the next key ("F — ...")
STOP = re.compile(r'\s[A-Z]\s*(?:—|–|=|:)\s|[.;|·•]\s|\s—\s|\s\(\s*[A-Z]\s*\)|→|\s\d+(?:\.\d+)+\s')


def pages():
    out = subprocess.run(['git', '--no-optional-locks', '-C', ROOT, 'ls-files', '*.html'],
                         capture_output=True, text=True).stdout.split()
    return sorted(f for f in out if not f.startswith(RETIRED) and f not in MENTION)


def text(f):
    t = open(os.path.join(ROOT, f), encoding='utf-8', errors='ignore').read()
    return re.sub(r'\s+', ' ', html.unescape(TAG.sub(' ', STY.sub(' ', GEN.sub(' ', t)))))


def field_of():
    d = {}
    with open(os.path.join(ROOT, 'docs', 'subjects.tsv'), encoding='utf-8') as fh:
        for row in csv.reader(fh, delimiter='\t'):
            if len(row) >= 2 and row[0] and not row[0].startswith('#'):
                d[row[0]] = row[1].split(' · ')[0].strip()
    return d


def build():
    T = {f: text(f) for f in pages()}
    field = field_of()
    use = {L: defaultdict(set) for L in SENSES}
    fill = {L: defaultdict(lambda: defaultdict(list)) for L in SENSES}
    for L, senses in SENSES.items():
        word = {w: s for s, ws in senses.items() for w in ws}
        rx = re.compile(r'(?<![A-Za-z0-9_])' + L +
                        r'\s*(?:—|–|-|=|:|\()\s*(?i:the\s+|a\s+|o\s+)?([A-Za-zçãõéêíóúàÀ-Ú]+)')
        for f, t in T.items():
            for m in rx.finditer(t):
                s = word.get(m.group(1).lower())
                if not s:
                    continue
                use[L][s].add(f)
                tail = t[m.end():m.end() + 140]
                cut = STOP.search(tail)
                ftxt = (tail[:cut.start()] if cut else tail[:90]).strip(' )(,:—–-')
                if 6 <= len(ftxt) <= 110 and (ftxt[0].isalnum() or ftxt[0] in '$κσ'):
                    dom = field.get(f, 'UNTAGGED')
                    if all(ftxt != x for x, _ in fill[L][s][dom]):
                        fill[L][s][dom].append((ftxt, f))
    omega = {f for f, t in T.items() if all(w.search(t) for w in OMEGA_WORDS)}
    reg = []
    for L in SENSES:
        ss = [s for s in SENSES[L] if use[L][s]]
        parent = {s: s for s in ss}

        def find(x):
            while parent[x] != x:
                x = parent[x]
            return x
        for i, a in enumerate(ss):
            for b in ss[i + 1:]:
                if use[L][a] & use[L][b]:
                    parent[find(a)] = find(b)
        comps = defaultdict(list)
        for s in ss:
            comps[find(s)].append(s)
        comps = sorted(comps.values(),
                       key=lambda c: (-len(set().union(*(use[L][s] for s in c))), sorted(c)))
        for ci, c in enumerate(comps):
            cpages = set().union(*(use[L][s] for s in c))
            om = len(cpages & omega) / len(cpages)
            keyset = 'Omega chain (G–L–R–U)' if om > 0.5 else 'dm³ chain (C→K→F→U)'
            head = max(sorted(c), key=lambda s: len(use[L][s]))
            for s in sorted(c, key=lambda s: (-len(use[L][s]), s)):
                reg.append(dict(letter=L, sense=s, component=ci + 1, pages=len(use[L][s]),
                                head=(s == head and ci == 0), comp_head=head, keyset=keyset,
                                fillers=fill[L][s], n_comp=len(comps)))
    return reg, len(T)


def render(reg, npages):
    src = open(os.path.join(ROOT, 'book20', 'ch01-the-planes-that-came-back.html'),
               encoding='utf-8').read()
    css = src[src.find('<style>'):src.find('</style>') + 8]
    e = html.escape
    parts = []
    for L in SENSES:
        rows = [r for r in reg if r['letter'] == L]
        n_comp = rows[0]['n_comp'] if rows else 0
        head = next((r['sense'] for r in rows if r['head']), '—')
        parts.append(f'<div class="eyebrow">key {L}</div><h2>{L} &mdash; head sense: {e(head)}</h2>')
        parts.append(f'<p class="mono" style="font-size:.8rem">{n_comp} sense(s) by Book XIV ch 3&rsquo;s rule.</p>')
        parts.append('<div class="tblwrap"><table><tr><th>gloss</th><th>pages</th><th>sense</th><th>key set</th></tr>')
        for r in rows:
            if r['head']:
                tag = 'head'
            elif r['comp_head'] != r['sense']:
                tag = 'same sense as ' + e(r['comp_head'])
            else:
                tag = 'separate sense'
            parts.append(f'<tr><td class="mono">{e(r["sense"])}</td><td class="n">{r["pages"]}</td>'
                         f'<td>{tag}</td><td>{e(r["keyset"])}</td></tr>')
        parts.append('</table></div>')
        for r in rows:
            if not r['fillers']:
                continue
            parts.append(f'<h3>{L} = {e(r["sense"])}: fillers by domain</h3><ul>')
            for dom in sorted(r['fillers'], key=lambda d: (d == 'UNTAGGED', d)):
                items = r['fillers'][dom][:4]
                li = '; '.join(f'<a href="../{e(f)}">{e(x)}</a>' for x, f in items)
                more = len(r['fillers'][dom]) - len(items)
                parts.append(f'<li><b>{e(dom.lower())}</b>: {li}' +
                             (f' <span class="mono">(+{more})</span>' if more > 0 else '') + '</li>')
            parts.append('</ul>')
    body = '\n'.join(parts)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Key Register &middot; Book XIV &mdash; Principia Orthogona</title>
<meta name="description" content="The series' dictionary of its own operator keys C, K, F, U, generated from {npages} pages: head sense, key set, and what each key means in each domain.">
{css}
</head>
<body>
<!-- GENERATED by tools/key_register.py -- do not hand-edit (R8) -->
<div class="topnav"><span class="crumbs"><a href="../index.html">&#9884; PRINCIPIA ORTHOGONA</a> &middot; Book XIV &middot; Key Register</span>
<span class="meta"><a href="ch04-translation-keys.html">&larr; Ch 4 &middot; Translation Keys</a> &middot; <a href="index.html">Book XIV contents</a></span></div>
<div class="wp-head"><div class="wp-kicker">Book XIV &middot; Reference &middot; generated</div>
<h1>Key <em>Register</em></h1>
<div class="subtitle">The operator letters as dictionary entries: one head sense per key, the key set it belongs to, and what it is filled with in each domain.</div>
<div class="metagrid"><div><strong>Source</strong>{npages} published pages, regenerated by tools/key_register.py</div><div><strong>Method</strong>Book XIV ch 3 (senses as chains) and ch 4 (keys and fillers)</div><div><strong>Idea</strong>letters as translation keys: Pablo Nogueira Grossi</div></div></div>
<div class="wrap">
<div class="lede">Each entry follows Chapter 3's template. The head sense comes first. Glosses that pages join count as one sense. A gloss that belongs to another chain is marked as such. Under each entry, the fillers show what the key becomes in each domain, each one linked to the page that says it.</div>
{body}
<div class="gap"><span class="lab">How to read the fillers</span>A filler is the text that follows the gloss on a page, cut at the next sentence mark or key, so some are fragments. The domain is the page's subject tag; untagged pages are listed last. A filler shows usage and does not verify it.</div>
</div>
<footer><div class="fwrap"><div><a href="../index.html">&#9884; PRINCIPIA ORTHOGONA</a> &middot; Book XIV &middot; Key Register<br>G6 LLC &middot; Pablo Nogueira Grossi &middot; Newark NJ &middot; CC BY-NC-ND 4.0</div>
<div class="disc">Generated. Edit the pages or the tool, never this file.</div></div></footer>
</body>
</html>
'''


def tsv(reg):
    lines = ['letter\tsense\tpages\tcomponent\thead\tkeyset\tdomains']
    for r in reg:
        lines.append(f"{r['letter']}\t{r['sense']}\t{r['pages']}\t{r['component']}\t"
                     f"{'yes' if r['head'] else ''}\t{r['keyset']}\t{len(r['fillers'])}")
    return '\n'.join(lines) + '\n'


def strip_gen(s):
    # later generators stamp their own blocks onto the page; staleness ignores them
    s = re.sub(r'<!--po-(run|gss|related|subject)-->.*?<!--/po-\1-->\n?', '', s, flags=re.S)
    return re.sub(r'<meta name="po-subject"[^>]*>\n?', '', s)


def main():
    reg, n = build()
    h, t = render(reg, n), tsv(reg)
    old_h = open(OUT_HTML, encoding='utf-8').read() if os.path.exists(OUT_HTML) else ''
    old_t = open(OUT_TSV, encoding='utf-8').read() if os.path.exists(OUT_TSV) else ''
    stale = strip_gen(old_h) != strip_gen(h) or old_t != t
    heads = {r['letter']: r['sense'] for r in reg if r['head']}
    if '--write' in sys.argv:
        if stale:
            open(OUT_HTML, 'w', encoding='utf-8').write(h)
            open(OUT_TSV, 'w', encoding='utf-8').write(t)
        print(f"{n} pages; {len(reg)} glosses; heads {heads}; {'written' if stale else '0 stale'}")
        return 0
    print(f"{n} pages; {len(reg)} glosses; {'STALE' if stale else '0 stale'}")
    return 1 if stale else 0


if __name__ == '__main__':
    sys.exit(main())
