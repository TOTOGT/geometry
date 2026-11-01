#!/usr/bin/env python3
"""Checks Book XXV pages: no outside resources load, both languages present, local links resolve."""
import re, os, sys
d=os.path.dirname(os.path.abspath(__file__))
pages=['index.html','ch01-why-brazil.html','translations/index.html','texts/direito-indigena.html']
ok=True
def check(name,cond):
    global ok
    print(('PASS ' if cond else 'FAIL ')+name); ok&=bool(cond)
for p in pages:
    t=open(os.path.join(d,p),encoding='utf-8').read()
    check(p+': no <link>/<script src>/<img>', not re.search(r'<link\b|<script\b|<img\b',t))
    check(p+': no url() loading outside', 'url(' not in t)
    check(p+': has Portuguese blocks', 'lang="pt"' in t)
    for h in re.findall(r'href="([^"#]+)"',t):
        if h.startswith('http'): continue
        check(p+': link '+h, os.path.exists(os.path.normpath(os.path.join(os.path.dirname(os.path.join(d,p)),h))))
t=open(os.path.join(d,'texts/direito-indigena.html'),encoding='utf-8').read()
check('text 1: says summary-not-law, sources for ILO/UNDRIP/marco temporal not claimed','This is a summary, not the law' in t and 'I have not read the sources for these' in t)
check('text 1: Articles 231 (7 paragraphs) and 232 in English',t.count('<li>')==7 and 'Article 232' in t)
# control: a page with an outside font must fail the first test
check('control: outside <link> is caught', bool(re.search(r'<link\b','<link href="https://fonts.googleapis.com">')))
sys.exit(0 if ok else 1)
