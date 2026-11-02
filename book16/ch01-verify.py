#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ch01-verify.py -- companion to book16/ch01-tokens.html. Written 2026-11-01. Run BEFORE trusting the page's numbers.
RECOMPUTED here by a second implementation (regex-based, written separately from the generator's): the ten byte-pair merges on the
toy dictionary {low:5, lower:2, newest:6, widest:3}, symbol counts, segmentations of unseen words, and the page's in-browser trainer
(run under node, compared with Python).
QUOTED, NOT CHECKED HERE: the BPE procedure (Sennrich et al. 2015, sec 3.2); the n^2*d self-attention cost (Vaswani et al. 2017, Table 1).
NOT A SOURCE FOR: any model's tokenizer, vocabulary size, or how token counts differ by language (stated on the page as open)."""
import re, sys, subprocess, shutil, json
from pathlib import Path
from collections import Counter
fails=[]
def check(ok,msg):
    print('    %s  %s'%('PASS' if ok else 'FAIL',msg))
    if not ok: fails.append(msg)
def head(n,t): print('\n'+'='*70+'\n  [%s]  %s\n'%(n,t)+'='*70)
HERE=Path(__file__).resolve().parent
html=(HERE/'ch01-tokens.html').read_text(encoding='utf-8'); idx=(HERE/'index.html').read_text(encoding='utf-8')
import html as H
txt=H.unescape(re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',re.sub(r'<style>.*?</style>|<script>.*?</script>','',html,flags=re.S))))
def train(words,n):
    seqs={w:list(w)+['</w>'] for w in words}
    log=[]
    for _ in range(n):
        c=Counter()
        for w,f in words.items():
            s=seqs[w]
            for i in range(len(s)-1): c[(s[i],s[i+1])]+=f
        if not c: break
        top=max(c.values()); a,b=sorted(k for k,v in c.items() if v==top)[0]
        for w in seqs:
            s=seqs[w]; i=0; o=[]
            while i<len(s):
                if i+1<len(s) and s[i]==a and s[i+1]==b: o.append(a+b); i+=2
                else: o.append(s[i]); i+=1
            seqs[w]=o
        log.append((a,b,top))
    return seqs,log
W={'low':5,'lower':2,'newest':6,'widest':3}
head(1,'ten merges on the toy dictionary')
seqs,log=train(W,10)
for i,(a,b,m) in enumerate(log,1): print('    %d %s+%s %d'%(i,a,b,m))
want=[('e','s',9),('es','t',9),('est','</w>',9),('l','o',7),('lo','w',7),('e','w',6),('ew','est</w>',6),('n','ewest</w>',6),('low','</w>',5),('d','est</w>',3)]
check(log==want,'the ten merges match the table on the page')
for i,(a,b,m) in enumerate(log,1): check('%s + %s'%(a,b) in txt,'page lists merge %d: %s + %s'%(i,a,b))
chars=sorted(set(ch for w in W for ch in w)|{'</w>'}); check(len(chars)==11,'11 starting symbols (10 letters used plus the end mark)')
before=sum((len(w)+1)*f for w,f in W.items()); after=sum(len(seqs[w])*f for w,f in W.items())
print('    symbols %d -> %d'%(before,after)); check((before,after)==(95,28),'95 symbols before, 28 after')
check('95' in txt and '28' in txt and '%.2f'%(before/after) in txt and '%.1f'%((before/after)**2) in txt,'page shows 95, 28, %.2f and %.1f'%(before/after,(before/after)**2))
check(sum(W.values())==16 and '16 word occurrences' in txt,'16 word occurrences')

head(2,'segmentation of unseen words')
merges=[(a,b) for a,b,_ in log]
def enc(word):
    s=list(word)+['</w>']
    for a,b in merges:
        i=0;o=[]
        while i<len(s):
            if i+1<len(s) and s[i]==a and s[i+1]==b: o.append(a+b); i+=2
            else: o.append(s[i]); i+=1
        s=o
    return s
check(enc('lowest')==['low','est</w>'],'lowest -> low | est</w>')
check(enc('lowest')[0] in [m[0]+m[1] for m in merges] and 'low | est' in txt,'page shows the lowest segmentation')
print('    newer ->',enc('newer'))

head(3,'in-browser trainer agrees with Python (node)')
js=re.search(r'<script>\n\(function.*?</script>',html,re.S)
node=shutil.which('node')
if node and js:
    body=js.group(0)[8:-9]
    stub='''var els={};function el(i){return els[i]||(els[i]={value:"",textContent:"",addEventListener(){}});}
global.document={getElementById:function(i){return el(i);}};
'''
    cases=[('low low low low low lower lower newest newest newest newest newest newest widest widest widest',10,'lowest'),
           ('the then there the the other',6,'these')]
    for corp,n,tw in cases:
        run=stub+'el("corp").value=%s;el("nm").value="%d";el("tw").value=%s;'%(json.dumps(corp),n,json.dumps(tw))+body+'\nconsole.log(el("res").textContent);'
        Path('/tmp/ch01test.js').write_text(run)
        out=subprocess.run([node,'/tmp/ch01test.js'],capture_output=True,text=True).stdout
        wc=Counter(corp.split()); sq,lg=train(wc,n)
        pm=[(i+1,a,b,m) for i,(a,b,m) in enumerate(lg)]
        jm=re.findall(r'^(\d+)\. (\S+) \+ (\S+)  \(count (\d+)\)$',out,re.M)
        ok=[(int(a),b,c,int(d)) for a,b,c,d in jm]==pm
        check(ok,'trainer merges equal Python for: %s...'%corp[:24])
        s=list(tw)+['</w>']
        for a,b,_ in lg:
            i=0;o=[]
            while i<len(s):
                if i+1<len(s) and s[i]==a and s[i+1]==b: o.append(a+b); i+=2
                else: o.append(s[i]); i+=1
            s=o
        check((tw+' -> '+' | '.join(s)) in out,'trainer segmentation of %s equals Python'%tw)
else: print('    SKIP  node not available (no PASS without it)')

head(4,'labels, links, exclusions')
for lab in ('Sennrich','Vaswani','Table 1','not measured','open','alphabetically smallest pair','never appeared in the toy text'):
    check(lab in txt,'present: '+lab)
check(not re.search(r'(https?:)?//(?!arxiv\.org)[a-z0-9.-]+\.[a-z]{2,}',re.sub(r'<a [^>]*href="https://arxiv.org[^"]*"','',html).replace('http://www.w3.org','')) ,'no outside resources other than the two arXiv links')
check(not any(b in html for b in ('fetch(','localStorage','XMLHttpRequest','<script src')),'no network or storage calls')
for p in ('index.html','../index.html','../book17/index.html','../book18/index.html','../book24/index.html','../book14/index.html','../book25/index.html'):
    check((HERE/p).exists(),'link target exists: '+p)
for h in re.findall(r'href="([^"#]+)"',idx+html):
    if not h.startswith('http'): check((HERE/h).exists(),'relative link resolves: '+h)
check('planned' in idx and 'draft' in idx,'index marks chapters draft or planned')
check('2007 edition' in idx,'index states the Jurafsky-Martin copy predates neural models')
print('\n[HONESTY] Arithmetic and labels only. It does not show how any real tokenizer behaves, or how languages compare.')
print('\nALL PASS' if not fails else '\nFAILED: %d'%len(fails)); sys.exit(1 if fails else 0)
