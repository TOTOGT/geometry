#!/usr/bin/env python3
"""
gold_standard.py — a self-assessment stamp against the nine tenets of Gold Standard
Science, Executive Order 14303 (23 May 2025, 90 FR 22601), Sec. 3(a):
  (i) reproducible; (ii) transparent; (iii) communicative of error and uncertainty;
  (iv) collaborative and interdisciplinary; (v) skeptical of its findings and
  assumptions; (vi) structured for falsifiability of hypotheses; (vii) subject to
  unbiased peer review; (viii) accepting of negative results as positive outcomes;
  (ix) without conflicts of interest.
Set 2026-09-27 by Pablo.

THIS IS NOT A CERTIFICATION. No agency has reviewed these pages. Each tenet is scored
from something observable on the page or beside it, the rule is printed in the stamp,
and a tenet the page cannot show is marked as not shown. (vii) is never claimed:
nothing here has been through independent peer review. (ix) is a disclosure, not a
claim of absence.

    python3 tools/gold_standard.py            check: exit 1 if any stamp is stale
    python3 tools/gold_standard.py --write    (re)write every stamp, idempotent
    python3 tools/gold_standard.py --show P   print P's scores and why
"""
import html, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import subject_tags as ST, run_yourself as RY

ROOT = ST.ROOT
BEGIN, END = '<!--po-gss-->', '<!--/po-gss-->'
BLOCK = re.compile(re.escape(BEGIN) + r'.*?' + re.escape(END) + r'\n?', re.S)
EO = 'https://www.federalregister.gov/documents/2025/05/29/2025-09802/restoring-gold-standard-science'
NEG = re.compile(r'withdrawn|retract|thesis failed|null result|0 matches|zero intersections|does not survive|was false|is false', re.I)

def score(rel, src):
    body = BLOCK.sub('', src)
    files = RY.files_for(rel, src)
    scripts = [open(os.path.join(ROOT, f), encoding='utf-8', errors='replace').read() for f in files]
    code = '\n'.join(scripts)
    other_books = len(set(re.findall(r'Book (\w+) &middot;|Book (\w+) ·', body[body.find('<!--po-related-->'):] if '<!--po-related-->' in body else ''))) > 0
    refs = bool(re.search(r'References|Sources|<ol class="refs"|Primary source|Held text', body))
    t = [
      ('reproducible', bool(files), 'a script or Lean file beside the page re-derives its numbers' if files else 'no script or Lean file'),
      ('transparent', bool(files) and refs, 'code downloadable and sources named with addresses' if (files and refs) else 'code or sourced references missing'),
      ('error and uncertainty', bool(re.search(r't-model|t-open|\[HONESTY\]|±|uncertain', body + code)), 'MODEL / OPEN tags or an [HONESTY] block'),
      ('collaborative, interdisciplinary', other_books, 'cross-linked to other volumes' if other_books else 'no cross-volume links'),
      ('skeptical', bool(re.search(r't-open|OPEN\]|not claim|will not claim|What (this|the) .{0,30}(not|does not)', body + code)), 'states what it does not claim, or leaves items open'),
      ('falsifiable', bool(re.search(r'\bFAIL\b', code)), 'its script can print FAIL' if re.search(r'\bFAIL\b', code) else 'no check that can fail'),
      ('unbiased peer review', False, 'not independently peer reviewed'),
      ('negative results', bool(NEG.search(body)), 'reports a withdrawn or failed result' if NEG.search(body) else 'no negative result reported on this page'),
      ('conflicts of interest', None, 'disclosed: author-published through G6 LLC, the author\'s company'),
    ]
    return t

def stamp(rel, src):
    t = score(rel, src)
    n = sum(1 for _, ok, _ in t if ok)
    rows = ''.join(
        f'<li style="margin:.1rem 0"><span style="display:inline-block;width:1.2em">{"&#10003;" if ok else ("&#9675;" if ok is None else "&#10007;")}</span>'
        f'({"i ii iii iv v vi vii viii ix".split()[k]}) {html.escape(name)} <span style="opacity:.6">&mdash; {html.escape(why)}</span></li>'
        for k, (name, ok, why) in enumerate(t))
    return (f'{BEGIN}<aside class="po-gss" style="max-width:860px;margin:1.2rem auto 1rem;padding:.8rem 1.1rem;'
            f'border:1px solid rgba(128,128,128,.35);border-left:3px solid rgba(40,80,150,.85);border-radius:0 6px 6px 0;'
            f'background:rgba(40,80,150,.05);font-family:ui-monospace,Menlo,monospace;font-size:.78rem;line-height:1.55">'
            f'<details><summary style="cursor:pointer;letter-spacing:.08em">'
            f'<b>Gold Standard Science &middot; {n} of 9 tenets shown</b> &middot; self-assessed against '
            f'<a href="{EO}" style="color:inherit">EO 14303 &sect;3(a)</a> &mdash; not a federal certification</summary>'
            f'<ul style="list-style:none;margin:.5rem 0 .3rem;padding:0">{rows}</ul>'
            f'<div style="opacity:.75">Scored by <code>tools/gold_standard.py</code> from what is observable on this page and beside it. '
            f'&#10003; shown &middot; &#10007; not shown &middot; &#9675; disclosure. No agency has reviewed this page.</div>'
            f'</details></aside>{END}\n')

def place(src, b):
    src = BLOCK.sub('', src)
    for marker in ('<!--po-run-->', '<!--po-related-->', '<footer', '</body>'):
        i = src.rfind(marker)
        if i >= 0: return src[:i] + b + src[i:]
    return src + b

def main():
    if '--show' in sys.argv:
        r = sys.argv[sys.argv.index('--show') + 1]
        for name, ok, why in score(r, open(os.path.join(ROOT, r), encoding='utf-8').read()): print(ok, name, '-', why)
        return 0
    write = '--write' in sys.argv; stale = changed = 0; hist = {}
    for rel in ST.chapters():
        if ST.rows().get(rel, ('',))[0] == 'SERIES APPARATUS': continue
        path = os.path.join(ROOT, rel); src = open(path, encoding='utf-8', errors='replace').read()
        new = place(src, stamp(rel, src))
        n = sum(1 for _, ok, _ in score(rel, src) if ok); hist[n] = hist.get(n, 0) + 1
        if new != src:
            if write: open(path, 'w', encoding='utf-8').write(new); changed += 1
            else: stale += 1
    print('tenets shown -> pages:', dict(sorted(hist.items())), f'; {changed} written' if write else f'; {stale} stale')
    return 1 if stale and not write else 0

if __name__ == '__main__':
    sys.exit(main())
