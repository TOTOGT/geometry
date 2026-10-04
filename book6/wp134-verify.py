#!/usr/bin/env python3
"""Checks WP-134: the derivations, the figure data and the structure. Controls at the bottom must FAIL on broken copies."""
import re, sys, os
here=os.path.dirname(os.path.abspath(__file__))
path=sys.argv[1] if len(sys.argv)>1 else os.path.join(here,'wp134-the-growth-imperative-tested.html')
html=open(path,encoding='utf8').read()
import re as _re_gen
# R25/R26: the generated blocks (subject tag, Across the series, GSS stamp) carry their own links and are not part of the page's argument
html = _re_gen.sub(r'<!--po-([a-z]+)-->.*?<!--/po-\1-->', '', html, flags=_re_gen.S)
fails=[]
def check(n,ok):
    print(('PASS ' if ok else 'FAIL ')+n)
    if not ok: fails.append(n)

# ---- independent derivation (not imported from the build script) ----
D0=1.2259
step=lambda d,r,g,p: d*(1+r)/(1+g)-p
def run_path(d0,r,g,p,n=50):
    d=d0
    for _ in range(n): d=step(d,r,g,p)
    return d
preq=lambda d,r,g: d*(r-g)/(1+g)
# 1. the identity: at p = d(r-g)/(1+g) the ratio is a fixed point, for every r,g tried
fixed_ok=all(abs(step(D0,r,g,preq(D0,r,g))-D0)<1e-12 for r in (0.0,0.02,0.03,0.04,0.1) for g in (0.0,0.01,0.02,0.05))
check('identity: p = d(r-g)/(1+g) makes the debt ratio a fixed point (20 combinations)',fixed_ok)
# 2. scenarios: rising, flat, falling
a=run_path(D0,.03,0,0); b=run_path(D0,.03,0,preq(D0,.03,0)); c=run_path(D0,.02,.03,0)
check('scenario A rises (r=3%, g=0, p=0): ends near 537%',a>D0 and abs(a*100-537)<1)
check('scenario B flat (r=3%, g=0, p=d*r): stays 122.6%',abs(b-D0)<1e-9)
check('scenario C falls (r=2%, g=3%, p=0): ends near 75%',c<D0 and abs(c*100-75.3)<0.2)
# 3. jobs identity and arithmetic
check('BLS 2025 numbers satisfy (1+gY)=(1+gA)(1+gL) to rounding',round(((1.022)*(1.004)-1)*100,1)==2.6)
cut10=(1-1.022**-10)*100; lab50=100*1.022**-50; lab10=100*1.022**-10
check('jobs: 19.6% less labour in ten years at constant output',round(cut10,1)==19.6)
check('jobs: index 80.4 at year 10 and 33.7 at year 50',round(lab10,1)==80.4 and round(lab50,1)==33.7)

def sections(h): return h[h.index('id="en"'):h.index('id="pt"')], h[h.index('id="pt"'):]
def run(h):
    out=[]; ck=lambda n,ok: out.append((n,ok))
    en,pt=sections(h)
    for lang,s in (('EN',en),('PT',pt)):
        dec=(lambda x:x) if lang=='EN' else (lambda x:x.replace('.',','))
        ck(f'{lang}: 12 h2',len(re.findall(r'<h2>',s))==12)
        # surplus table values
        vals=[dec(f"{preq(D0,r/100,g/100)*100:.2f}%") for r in (2,3,4) for g in (0,2)]
        ck(f'{lang}: surplus table = d(r-g)/(1+g) for all six cells',all(f'<td class="n">{v}</td>' in s for v in vals))
        ck(f'{lang}: 19.6 per cent and 122.59 in text',dec('19.6') in s and dec('122.59') in s)
        ck(f'{lang}: 2.2, 2.6 and 0.4 BLS figures in text',all(dec(x) in s for x in ('2.2','2.6','0.4')))
        ck(f'{lang}: 53.8 labour share noted as not used',dec('53.8') in s)
        refs=re.search(r'<ol>(.*?)</ol>',s,re.S).group(1); items=re.findall(r'<li>(.*?)</li>',refs,re.S)
        ck(f'{lang}: 7 references',len(items)==7)
        ck(f'{lang}: each reference has link and access 3 Oct',all(('Available at' in i or 'Disponível em' in i) and re.search(r'3 (Oct|out)\. 2026',i) for i in items))
        ck(f'{lang}: ABNT capitals',all(re.match(r'[A-ZÇÃÕ][A-ZÇÃÕ\.\' ;]{3,}',re.sub(r'<[^>]+>','',i)) for i in items))
        ck(f'{lang}: unread sources are marked (title only / 403)',('Title only' in s and 'Title and publication details only' in s) if lang=='EN' else ('Só o título' in s and 'Só título e dados' in s))
        ck(f'{lang}: tables: 7 + 10 rows',len(re.findall(r'<tr>',s))==7+10)
        ck(f'{lang}: G6 marked as the author’s proposal, not tested',("The author&rsquo;s proposal; no criterion or decider given; not tested" in s) if lang=='EN' else ('Proposta do autor; sem critério nem decisor; não testada' in s))
        ck(f'{lang}: states these are models not proofs',('model results, not proofs about real economies' in s) if lang=='EN' else ('resultados de modelos, não provas sobre economias reais' in s))
        ck(f'{lang}: no personal content',not re.search(r'my son|David|Tiffany|Pablo|meu filho',s))
        ck(f'{lang}: links WP-131, 132, 133',all(x in s for x in ('wp131-finance','wp132-born-appraised','wp133-the-grandchildren')))
        ck(f'{lang}: ABNT mention','ABNT NBR 6023' in s)
        fa=re.search(rf'<figure class="viz" id="figA-{lang.lower()}">(.*?)</figure>',s,re.S)
        fb=re.search(rf'<figure class="viz" id="figB-{lang.lower()}">(.*?)</figure>',s,re.S)
        ck(f'{lang}: both figures present',bool(fa and fb))
        if fa and fb:
            ends=[float(x) for x in re.findall(r'data-end="([\d.]+)"',fa.group(1))]
            ck(f'{lang}: figA end values = scenario results (537, 122.6, 75.3)',len(ends)==3 and abs(ends[0]-a*100)<0.1 and abs(ends[1]-b*100)<0.1 and abs(ends[2]-c*100)<0.1)
            ck(f'{lang}: figA has 3 two-pixel lines',fa.group(1).count('<polyline')==3 and fa.group(1).count('stroke-width="2" stroke-linejoin')==3)
            e=re.findall(r'data-end="([\d.]+)"',fb.group(1)); d10=re.findall(r'data-t="10" data-v="([\d.]+)"',fb.group(1))
            ck(f'{lang}: figB end = 33.7 and year-10 = 80.4',len(e)==1 and abs(float(e[0])-lab50)<0.01 and len(d10)==1 and abs(float(d10[0])-lab10)<0.01)
            ck(f'{lang}: figures credit the source/arithmetic',('Our arithmetic' in fb.group(1) and 'Paths are our arithmetic' in fa.group(1)) if lang=='EN' else ('Nossa aritmética' in fb.group(1) and 'aritmética nossa' in fa.group(1)))
    ue=sorted(set(re.findall(r'href="(https?://[^"]+)"',en))); up=sorted(set(re.findall(r'href="(https?://[^"]+)"',pt)))
    ck('EN and PT link the same 7 sources',ue==up and len(ue)==7)
    ck('Swift cited with year',all('1729' in s for s in (en,pt)))
    return out
for n,ok in run(html): check(n,ok)
def expect_fail(name,broken,needle):
    bad=[n for n,ok in run(broken) if not ok]
    check(f'control fails as it should: {name}',any(needle in n for n in bad))
expect_fail('surplus cell altered',html.replace('3.68%','2.68%',1),'surplus table')
expect_fail('19.6 changed to 12.6',html.replace('19.6','12.6'),'19.6')
expect_fail('PT link dropped',html[:html.index('id="pt"')]+html[html.index('id="pt"'):].replace('href="https://www.nature.com/articles/s41467-025-58777-4"','href="#"'),'same 7')
expect_fail('G6 label removed',html.replace('no criterion or decider given; not tested','established'),'G6')
expect_fail('figA end value altered',re.sub(r'data-end="537\.\d+"','data-end="200.0000"',html,count=1),'figA end')
expect_fail('"models not proofs" caveat removed',html.replace('model results, not proofs about real economies','established'),'models not proofs')
expect_fail('personal name inserted',html.replace('3 October 2026.','Pablo.'),'personal')
# a broken identity must be caught by the independent check
broken_fixed=all(abs(step(D0,r,g,d*0 + D0*(r-g))-D0)<1e-12 for r in (0.03,) for g in (0.02,) for d in (D0,))
check('control: dropping the 1/(1+g) factor breaks the fixed-point test',not broken_fixed)
print()
print('all checks passed' if not fails else f'{len(fails)} FAILED: {fails}')
sys.exit(1 if fails else 0)
