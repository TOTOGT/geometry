#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""wp71-verify.py -- companion to book6/wp71-lunar-survivability.html. Written 2026-10-13 (R24, R29 three-point audit).
RECOMPUTED: the bone-loss table, the micrometeoroid compounding table, n* = 2/p and the surface-area rule, the 'even pod counts'
parity remark, lunar/Mars gravity ratios. CHECKED AGAINST THE RETAINED PDF (book6/sources/hrp-rap-for-web-62026.pdf, via pdftotext;
SKIP if absent): the Risk Approach Plan identifiers, dates and quotes the page uses. CHECKED FOR RELEVANCE: the one Lean name the page carries.
NOT CHECKED (no source in the repo; the page's [VERIFIED]/[MODEL] tags are NOT confirmed here): the 0.4 g threshold wording beyond its abstract,
the 0.39 %/wk and 0.22 %/wk bone rates, ISS exercise minutes, the xEMU 1-in-2500 figure, regolith reactivity (50 % in 3.5 h, 10x quartz),
and the 13.4x depth-and-subdivision figure (the page gives no q, k, n or cave definition, so it cannot be reproduced from the page)."""
import math, os, re, subprocess, sys
fails=[]; notes=[]
def check(ok,msg):
    print('    %s  %s'%('PASS' if ok else 'FAIL',msg))
    if not ok: fails.append(msg)
def head(n,t): print('\n'+'='*72+'\n  [%s]  %s\n'%(n,t)+'='*72)
WPM=52.1775/12   # weeks per month

head(1,'bone table: months to lose a fraction x at a constant weekly rate r, compounded: w = ln(1-x)/ln(1-r)')
page={ 'lunar':(0.0039,{0.05:3.0,0.10:6.2,0.20:13.1,0.30:21.0}), 'mars':(0.0022,{0.05:5.4,0.10:11.0,0.20:23.3,0.30:37.3}) }
for k,(r,tab) in page.items():
    for x,pm in tab.items():
        m=math.log(1-x)/math.log(1-r)/WPM
        ok=abs(m-pm)<=0.06   # one decimal; the third digit depends on the weeks-per-month convention (52.18/12 used here; 52/12 shifts it by up to 0.06)
        print('    %-5s %2d%%  computed %.2f  page %.1f'%(k,100*x,m,pm))
        check(ok,'%s %d%% loss: page %.1f vs computed %.2f months'%(k,100*x,pm,m))

head(2,'micrometeoroid compounding: P(at least one) = 1 - (1 - 1/2500)^N (the 1-in-2500 per EVA figure is QUOTED, not checked)')
for N,pm in ((52,2.1),(100,3.9),(500,18)):   # the page prints 18% for N=500
    p=100*(1-(1-1/2500)**N); print('    N=%3d  %.2f%%  (page %.1f%%)'%(N,p,pm)); check(abs(p-pm)<=0.5*10**(-(0 if pm==18 else 1)),'N=%d: %.2f%% vs page %.1f%%'%(N,p,pm))

head(3,'subdivision: loss(n) = n^(-2/3) + p n^(1/3); the minimum is at n = 2/p; skin of n equal-volume pods = n^(1/3) of one pod')
check(abs(8**(1/3)-2)<1e-12,'eight pods have exactly twice the surface of one pod of equal volume')
bad=[]
for p in [0.001,0.002,0.005,0.01,0.02,0.05,0.1]:
    f=lambda n: n**(-2/3)+p*n**(1/3)
    nn=min(range(1,5000),key=f); star=2/p
    ok=abs(nn-star)<=1; print('    p=%.3f  integer argmin %4d  2/p = %.1f'%(p,nn,star))
    if not ok: bad.append((p,nn,star))
check(not bad,'integer argmin within one pod of 2/p at every p tried (0.001 to 0.1): %s'%(bad or 'yes'))

head(4,'parity remark: "with a lose-more-than-half abort criterion, even pod counts are penalised (three beats four) because losing exactly half counts against you"')
from math import comb
def tail(n,q,kmin): return sum(comb(n,k)*q**k*(1-q)**(n-k) for k in range(kmin,n+1))
for q in (0.01,0.05):
    a3=tail(3,q,2); a4_more=tail(4,q,3); a4_half=tail(4,q,2)
    print('    q=%.2f  3 pods (lose >=2) %.3e | 4 pods, strictly MORE than half (>=3) %.3e | 4 pods, HALF OR MORE (>=2) %.3e'%(q,a3,a4_more,a4_half))
check(all(tail(4,q,3)<tail(3,q,2) for q in (0.01,0.05)),'strictly "more than half": four pods BEAT three (so the sentence as written is backwards)')
check(all(tail(4,q,2)>tail(3,q,2) for q in (0.01,0.05)),'"half or more" criterion: three beats four (the sentence is right only for this wording)')

head(5,'gravity ratios')
print('    lunar 1.62/9.80665 = %.4f (page 0.167 = 1/6 rounded) ; Mars 3.71/9.80665 = %.4f (page 0.38)'%(1.62/9.80665,3.71/9.80665))
check(abs(1.62/9.80665-0.167)<0.003 and abs(3.71/9.80665-0.38)<0.005,'0.167 g and 0.38 g within rounding')
check(0.167<0.4/2 and 0.38<0.4,'lunar 0.167 g is under half of 0.4 g; Mars 0.38 g is just under 0.4 g (page says "sits essentially on the boundary")')

head(6,'Risk Approach Plan quotes against the retained PDF')
pdf=os.path.join(os.path.dirname(os.path.abspath(__file__)),'sources','hrp-rap-for-web-62026.pdf')
if not os.path.exists(pdf): print('    SKIP  PDF not present (never a PASS without it)')
else:
    t=subprocess.run(['pdftotext','-layout',pdf,'-'],capture_output=True,text=True).stdout; flat=re.sub(r'\s+',' ',t)
    for s in ('Cancer-104','CV-108','EVA-102','BONE-101','BONE-102','BONE-201','BONE-301','BONE-401','Lunar Hi-Tempo Capabilities: EHP/FOD/OCHMO by 2028','Martian Hi-Tempo Capabilities: EHP/FOD/OCHMO by 2029','Bone Standards and Recommendations: OCHMO by 2028','MRI Informing Pharmaceutical Use TTO 2027','in partial-G: OCHMO by 2033','0-G:'):
        check(s in flat,'present: %s'%s)
    check(re.search(r'Thrombosis in 0-G:.{0,200}OCHMO by 2031',flat) is not None,'0-G likelihood and consequences: OCHMO by 2031')
    check(flat.count('Bone Standards and Recommendations: OCHMO by 2028')==2,'Bone deliverable printed twice (characterisation and countermeasure columns)')
    check(flat.count('Days post-landing prior to initial EVA')==2 and 'prior to initial EVA: OCHMO by 2027' in flat and 'prior to initial EVA: OCHMO by 2033' in flat,'"Days post-landing" appears twice, OCHMO 2027 and 2033')
    check(re.search(r'effects of radiation dose and dose-.{0,200}rate on cancer',flat) is not None,'Cancer-104 wording (wrapped across a column break in the PDF)')
    print('    READ 2026-10-15 (not in the RAP PDF): NASA Astronaut Exercise page says crew average two hours of exercise per day; OCHMO-TB-031 gives 30 min aerobic + 30-60 min resistive, VO2peak baseline ~30 days after return, 45-day reconditioning program. Page text now matches these; the earlier 2.5 h and 45-day-baseline wording was unsupported. Deliverable counts per plan not recounted here')

head(7,'the one Lean name on the page: `discriminant`, linked to book21/Spiral.lean:75')
sp=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','book21','Spiral.lean')
if os.path.exists(sp):
    L=open(sp,encoding='utf-8').read()
    check('theorem discriminant' in L and '-(4 * ω ^ 2)' in L,'Spiral.lean:`discriminant` states tr^2 - 4 det = -4 w^2 for the 2x2 matrix [[mu,-w],[w,mu]]')
    pg=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'wp71-lunar-survivability.html'),encoding='utf-8').read()
    body=re.sub(r'<style.*?</style>|<script.*?</script>|<div class="po-proved-block">.*?</span>\s*</div>|<aside class="po-run".*?</aside>|<div class="correction-note".*?</div>','',pg,flags=re.S)
    check(len(re.findall(r'eigenvalue|determinant|\bmatrix\b|spiral',re.sub(r'<[^>]+>',' ',body),flags=re.I))==0,'the page has no matrix, eigenvalue or spiral content for that theorem to support: the "Proved" block is a NAME MATCH (tools/proved_labels.py matches the word in prose), not evidence for the page')

print('\nRESULT: %s'%('ALL PASS' if not fails else '%d FAIL'%len(fails)))
for f in fails: print('  FAIL:',f)
sys.exit(1 if fails else 0)
