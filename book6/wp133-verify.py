#!/usr/bin/env python3
"""Checks WP-133 figures and structure. Controls at the bottom must FAIL on broken copies."""
import re, sys, os
here=os.path.dirname(os.path.abspath(__file__))
path=sys.argv[1] if len(sys.argv)>1 else os.path.join(here,'wp133-the-grandchildren-of-others.html')
html=open(path,encoding='utf8').read()
fails=[]
def check(n,ok):
    print(('PASS ' if ok else 'FAIL ')+n)
    if not ok: fails.append(n)
# independent arithmetic
w={r:(1+r/100)**-50*100 for r in (2,3,7)}
debt=39.065421
exp={
 'w2_en':f"{w[2]:.1f}",'w3_en':f"{w[3]:.1f}",'w7_en':f"{w[7]:.1f}",
 'ratio_en':f"{6.7/debt*100:.1f}",'r190_en':f"{190/120:.2f}",'r340_en':f"{340/120:.2f}",'r27':f"{w[2]/w[7]:.0f}",
}
def sections(h): return h[h.index('id="en"'):h.index('id="pt"')], h[h.index('id="pt"'):]
def run(h):
    out=[]; ck=lambda n,ok: out.append((n,ok))
    en,pt=sections(h)
    for lang,s in (('EN',en),('PT',pt)):
        dec=(lambda x:x) if lang=='EN' else (lambda x:x.replace('.',','))
        for k in ('w2_en','w3_en','w7_en','ratio_en','r190_en','r340_en'):
            ck(f'{lang}: {k} = {exp[k]}', dec(exp[k]) in s)
        ck(f'{lang}: 2%/7% weight ratio about {exp["r27"]}', f'{exp["r27"]} ' in s or f'{exp["r27"]}x' in s)
        for v in ('7,43','0,73','6,7','6,4','5,8') if lang=='PT' else ('7.43','0.73','6.7','6.4','5.8'):
            ck(f'{lang}: IMF figure {v}', v in s)
        ck(f'{lang}: IMF split 39/32/16/9/4 and 14 Sept 2026 update date',all(x in s for x in ('39%, 32%, 16%, 9%, 4%',)) and (('14 Sept. 2026' in s) if lang=='EN' else ('14 set. 2026' in s)))
        ck(f'{lang}: EPA $120/$190/$340', all(x in s for x in ('120','190','340')))
        ck(f'{lang}: 10 h2', len(re.findall(r'<h2>',s))==10)
        refs=re.search(r'<ol>(.*?)</ol>',s,re.S).group(1); items=re.findall(r'<li>(.*?)</li>',refs,re.S)
        ck(f'{lang}: 9 references',len(items)==9)
        ck(f'{lang}: each reference has link text, access date 3 Oct',all(('Available at' in i or 'Disponível em' in i) and re.search(r'3 (Oct|out)\. 2026',i) for i in items))
        ck(f'{lang}: ABNT capitals',all(re.match(r'[A-ZÇÃÕ][A-ZÇÃÕ\.\' ]{3,}',re.sub(r'<[^>]+>','',i)) for i in items))
        ck(f'{lang}: status table rows',len(re.findall(r'<tr>',s))==7+1+11+1)
        ck(f'{lang}: Nature estimate marked retracted and not used',('Retracted 3 Dec 2025; not used' in s) if lang=='EN' else ('Retratada em 3 dez. 2025; não usada' in s))
        ck(f'{lang}: incidence marked not shown',('Not shown by the sources read' in s) if lang=='EN' else ('Não mostrado pelas fontes lidas' in s))
        ck(f'{lang}: no personal content',not re.search(r'my son|David|Tiffany|Pablo|meu filho',s))
        ck(f'{lang}: links WP-131 and WP-132','wp131-finance' in s and 'wp132-born-appraised' in s)
        ck(f'{lang}: no unsourced year for the UN standard','in 2021' not in s and 'em 2021' not in s)
        ck(f'{lang}: mentions ABNT','ABNT NBR 6023' in s)
    ue=sorted(set(re.findall(r'href="(https?://[^"]+)"',en))); up=sorted(set(re.findall(r'href="(https?://[^"]+)"',pt)))
    ck('EN and PT link the same 9 sources',ue==up and len(ue)==9)
    ck('Swift cited with year',all('1729' in s for s in (en,pt)))
    return out
for n,ok in run(html): check(n,ok)
def expect_fail(name,broken,needle):
    bad=[n for n,ok in run(broken) if not ok]
    check(f'control fails as it should: {name}',any(needle in n for n in bad))
expect_fail('7% weight altered',html.replace('3.4','9.9'),'w7_en')
expect_fail('PT link dropped',html[:html.index('id="pt"')]+html[html.index('id="pt"'):].replace('href="https://www.nature.com/articles/s41586-024-07219-0"','href="#"'),'same 9 sources')
expect_fail('retraction label removed',html.replace('Retracted 3 Dec 2025; not used','Established'),'retracted')
expect_fail('IMF total altered',html.replace('7.43','8.43'),'IMF figure 7.43')
expect_fail('personal name inserted',html.replace('3 October 2026.','Pablo.'),'personal')
expect_fail('year for UN standard inserted',html.replace('has adopted the System','in 2021 adopted the System'),'UN standard')
print()
print('all checks passed' if not fails else f'{len(fails)} FAILED: {fails}')
sys.exit(1 if fails else 0)
