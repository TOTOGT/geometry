#!/usr/bin/env python3
"""
run_yourself.py — a one-click "Run it yourself" box on every chapter that has code.
Set 2026-09-27 by Pablo: "a reader should be able to one click download lean and py
if they want to run it themselves."

For each chapter (the set tools/subject_tags.py uses) it collects the scripts and
Lean files the page already names — any href to a .py or .lean, and any bare file
name ending .py/.lean in the text that exists beside the page or in tools/ — and
writes a box of direct download links (the `download` attribute), with the one line
needed to run each kind. Generated between markers, never hand-edited (R8).

    python3 tools/run_yourself.py            check: exit 1 if any box is stale
    python3 tools/run_yourself.py --write    (re)write every box, idempotent
"""
import html, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import subject_tags as ST

ROOT = ST.ROOT
BEGIN, END = '<!--po-run-->', '<!--/po-run-->'
BLOCK = re.compile(re.escape(BEGIN) + r'.*?' + re.escape(END) + r'\n?', re.S)
GENERATED = re.compile(r'<!--po-(run|gss|related|subject)-->.*?<!--/po-\1-->\n?', re.S)
REPO = 'https://github.com/TOTOGT/geometry'

def files_for(rel, src):
    base = os.path.dirname(rel)
    body = GENERATED.sub('', src)       # never read our own or sibling generated boxes
    found = []
    for h in re.findall(r'href="([^"#?]+\.(?:py|lean))"', body):
        if h.startswith(('http:', 'https:')): continue
        found.append(os.path.normpath(os.path.join(base, h)).replace(os.sep, '/'))
    text = re.sub(r'<[^>]+>', ' ', body)
    for name in set(re.findall(r'\b([\w./-]+\.(?:py|lean))\b', text)):
        for cand in (os.path.join(base, name), name, os.path.join(base, os.path.basename(name))):
            cand = os.path.normpath(cand).replace(os.sep, '/')
            if os.path.isfile(os.path.join(ROOT, cand)) and not cand.startswith('_to_delete'):
                found.append(cand); break
    seen, out = set(), []
    for f in found:
        if f not in seen and os.path.isfile(os.path.join(ROOT, f)):
            seen.add(f); out.append(f)
    return sorted(out, key=lambda f: (not f.endswith('.lean'), f))

def box(rel, files):
    if not files:
        return ''
    up = '../' * rel.count('/')
    li = []
    for f in files:
        kind = 'Lean 4' if f.endswith('.lean') else 'Python 3'
        li.append(f'<li style="margin:.2rem 0"><a href="{up}{f}" download style="color:inherit;text-decoration:underline;text-underline-offset:2px">'
                  f'{html.escape(os.path.basename(f))}</a> <span style="opacity:.6">&middot; {kind} &middot; {html.escape(f)}</span></li>')
    has_py = any(f.endswith('.py') for f in files)
    has_lean = any(f.endswith('.lean') for f in files)
    how = []
    if has_py:
        how.append('<b>Python</b>: <code>python3 FILE.py</code> &mdash; standard library only; pages that read a book also need '
                   '<code>pdftotext</code> and the book in <code>~/Downloads</code>, and say SKIP rather than PASS without it.')
    if has_lean:
        how.append(f'<b>Lean</b>: clone <a href="{REPO}" style="color:inherit">the repository</a>, run <code>lake exe cache get</code> once '
                   '(Mathlib, pinned in <code>lakefile.lean</code>), then <code>lake env lean FILE.lean</code>. '
                   'The <code>#print axioms</code> lines at the end should list only <code>propext</code>, <code>Classical.choice</code>, <code>Quot.sound</code>.')
    return (f'{BEGIN}<aside class="po-run" style="max-width:860px;margin:1.6rem auto 1rem;padding:1rem 1.25rem;'
            f'border:1px solid rgba(128,128,128,.35);border-left:3px solid rgba(80,140,110,.85);border-radius:0 6px 6px 0;'
            f'background:rgba(80,140,110,.06);font-family:ui-monospace,Menlo,monospace;font-size:.8rem;line-height:1.6">'
            f'<div style="font-size:.72em;letter-spacing:.16em;text-transform:uppercase;opacity:.85">Run it yourself &middot; one-click download</div>'
            f'<ul style="margin:.4rem 0 .5rem 1.1rem;padding:0">{"".join(li)}</ul>'
            f'<div style="font-size:.92em;opacity:.85">{"<br>".join(how)}</div></aside>{END}\n')

def place(src, b):
    src = BLOCK.sub('', src)
    if not b: return src
    for marker in ('<!--po-related-->', '<footer', '</body>'):
        i = src.rfind(marker)
        if i >= 0: return src[:i] + b + src[i:]
    return src + b

def main():
    write = '--write' in sys.argv
    stale = changed = boxes = 0
    for rel in ST.chapters():
        path = os.path.join(ROOT, rel)
        src = open(path, encoding='utf-8', errors='replace').read()
        files = files_for(rel, src)
        boxes += bool(files)
        new = place(src, box(rel, files))
        if new != src:
            if write: open(path, 'w', encoding='utf-8').write(new); changed += 1
            else: stale += 1
    print(f'{boxes} chapters with code' + (f'; {changed} written' if write else f'; {stale} stale'))
    return 1 if stale and not write else 0

if __name__ == '__main__':
    sys.exit(main())
