#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""book26/ch16-verify.py -- book26/ch16-when-bail-is-not-posted.html against the saved outputs in ch16-code/.
[1] sample arithmetic [2] page numbers found in the outputs [3] control [4] honesty and no employer named. CSVs are not stored; the outputs are."""
import html as H,re
from pathlib import Path
D=Path(__file__).resolve().parent;P=D/'ch16-when-bail-is-not-posted.html';C=D/'ch16-code'
F=[]
def check(l,ok):
    print(('PASS ' if ok else 'FAIL ')+l)
    if not ok:F.append(l)
raw=re.sub(r'<(script|style)[^>]*>.*?</\1>','',P.read_text(encoding='utf8'),flags=re.S);txt=re.sub(r'\s+',' ',H.unescape(re.sub(r'<[^>]+>',' ',raw)))
a3=(C/'audit3.txt').read_text();a3b=(C/'audit3b.txt').read_text();a4=(C/'audit4.txt').read_text()
check('status counts sum to continuing cases',387719+73021+42012+1791+1696==506239)
check('continuing + disposed + unknown = local misdemeanors',506239+175604+3614==685457)
def inout(page,src,out):
    return page in txt and src in out
for page,src,out in [('1,028,073','1028073',a3),('898,393','898393',a3),('685,457','685457',a3),('175,604','175604',a3),('24,913','24913',a3),('15,876','n=  15876',a3),('1,413','n=   1413',a3),('22,413','n=  22413',a3),('354,884','n= 354884',a3),('65,576','n=  65576',a3),('13,050','13050',a3),('9,910','9910/15836',a3),('1,265','1265/1407',a3),('5,118','5118/15836',a3),('4,778','4778/15836',a3),('440,248','440248',a4)]:
    check('%s on page and in output'%page,inout(page,src,out))
sec=a3[a3.index('== cohorts through Sep'):]
for lab,v in [('NotPosted >$1','15.9%'),('NotPosted exact$1','8.9%'),('Posted >$1','5.6%'),('Remanded','4.8%'),('ROR','4.1%'),('NMR','2.1%')]:
    m=re.search(r'(?<![A-Za-z])'+re.escape(lab)+r'\s+n=\s*\d+ <=30\s+([\d.]+%)',sec);check('rate %s = %s'%(lab,v),m is not None and m.group(1)==v and v in txt)
for s in ('7.6 [  5.6,  9.3]','7.7 [','7.1 [  5.3,  9.0]','7.6 [  5.6,  9.8]'):check('contrast in output: '+s,s in a3)
check('fixed-population values',all(x in a3b for x in('7.6 [','7.7 [','raw on fixed population: 10.8')))
for s in ('2.41 pp','1.09 pp','0.71 pp'):check('judge slope in output: '+s,s in a4)
check('control: a damaged number is not found',('n=  99999' not in a3) and not inout('1,028,074','1028074',a3))
for w in ('Princeton','Yang,','Crystal'):check('no posting or contact named: '+w,w not in re.sub(r'Dobbie, Goldin and Yang','',txt))
check('states non-causal',"does not show that anyone could not pay" in txt and 'not a 95% confidence interval' in txt)
print('RESULT:','ALL PASS' if not F else '%d FAIL'%len(F));raise SystemExit(bool(F))
