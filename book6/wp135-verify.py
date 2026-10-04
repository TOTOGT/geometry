#!/usr/bin/env python3
"""Checks WP-135: the derivations, the figure data, the structure and the honesty labels. Controls at the bottom must FAIL on broken copies."""
import re, sys, os
from decimal import Decimal, ROUND_HALF_UP
here=os.path.dirname(os.path.abspath(__file__))
path=sys.argv[1] if len(sys.argv)>1 else os.path.join(here,'wp135-who-owns-the-machines.html')
html=open(path,encoding='utf8').read()
import re as _re_gen
# R25/R26: the generated blocks (subject tag, Across the series, GSS stamp) carry their own links and are not part of the page's argument
html = _re_gen.sub(r'<!--po-([a-z]+)-->.*?<!--/po-\1-->', '', html, flags=_re_gen.S)
fails=[]
def check(n,ok):
    print(('PASS ' if ok else 'FAIL ')+n)
    if not ok: fails.append(n)
q2=lambda a,b:(Decimal(a)/Decimal(b)).quantize(Decimal('0.01'),ROUND_HALF_UP)

# ---- independent derivation (not imported from the build script) ----
# Piketty Table 7.2 as read from the book (printed p. 248): top 10% / incl. top 1% / middle 40% / bottom 50%
T72={'Europe 1910':(90,50,5,5),'US 2010':(70,35,25,5),'Europe 2010':(60,25,35,5),'Scandinavia':(50,20,40,10),'Low':(30,10,45,25)}
for k,(t10,t1,m,b) in T72.items(): assert t10+m+b==100,k
# first law: alpha = r*beta  =>  beta = alpha/r ; Piketty's own example (pp. 162-163)
beta_cap=0.40/0.05; beta_slave=0.60/0.05
check('Piketty example: capital 8 years, slaves 12, together 20 (alpha/r)',round(beta_cap,6)==8 and round(beta_slave,6)==12 and round(beta_cap+beta_slave,6)==20)
check('first law round trip: alpha = r * (alpha/r) for 9 combinations',all(abs(r*(a/r)-a)<1e-12 for r in (.03,.05,.07) for a in (.1,.2,.3)))
check('two ten-point steps at r=5% add 4.0 years; one adds 2.0',abs(.10/.05-2.0)<1e-12 and abs(.20/.05-4.0)<1e-12)
# per-capita multiples: share / population share
POP=(50,40,9,1)   # bottom 50, middle 40, next 9, top 1
def shares(name):
    t10,t1,m,b=T72[name]; return (b,m,t10-t1,t1)
def mult(name): return [q2(s,p) for s,p in zip(shares(name),POP)]
us=mult('US 2010'); eu=mult('Europe 1910')
check('US 2010: bottom half 0.10 of average per person, top 1% 35.00',us[0]==Decimal('0.10') and us[3]==Decimal('35.00'))
check('Europe 1910: bottom half 0.10, top 1% 50.00',eu[0]==Decimal('0.10') and eu[3]==Decimal('50.00'))
check('equal shares: bottom half gets 10x the US 2010 share (50 vs 5)',50/shares('US 2010')[0]==10)
check('shares by group sum to 100 in every regime',all(sum(shares(k))==100 for k in T72))
check('population shares sum to 100',sum(POP)==100)

def sections(h): return h[h.index('id="en"'):h.index('id="pt"')], h[h.index('id="pt"'):]
GROUPS=['b50','m40','n9','t1']
def run(h):
    out=[]; ck=lambda n,ok: out.append((n,ok))
    en,pt=sections(h)
    for lang,s in (('EN',en),('PT',pt)):
        dec=(lambda x:x) if lang=='EN' else (lambda x:x.replace('.',','))
        ck(f'{lang}: 12 h2',len(re.findall(r'<h2>',s))==12)
        # table Δβ = Δα/r
        t2=[dec(str(q2(d,r))) for r in (3,5,7) for d in (10,20,30)]
        ck(f'{lang}: delta-beta table = delta-alpha / r for all nine cells',all(f'<td class="n">{v}</td>' in s for v in t2))
        # per-capita table: Europe 1910, US 2010, equal
        cells=[]
        for gi in range(4):
            for name in ('Europe 1910','US 2010'): cells.append(dec(str(mult(name)[gi])))
            cells.append(dec('1.00'))
        ck(f'{lang}: per-capita table = share / population share for all twelve cells',all(f'<td class="n">{v}</td>' in s for v in cells))
        ck(f'{lang}: status table has 9 claim rows and the page has 19 rows in all',len(re.findall(r'<tr>',s))==19)
        refs=re.search(r'<ol>(.*?)</ol>',s,re.S).group(1); items=re.findall(r'<li id="ref-\d">(.*?)</li>',refs,re.S)
        ck(f'{lang}: 3 references',len(items)==3)
        ck(f'{lang}: each reference has an access date of 4 Oct 2026',all(re.search(r'4 (Oct|out)\. 2026',i) for i in items))
        ck(f'{lang}: ABNT capitals',all(re.match(r'[A-ZÇÃÕ][A-ZÇÃÕ\.\' ;]{3,}',re.sub(r'<[^>]+>','',i)) for i in items))
        ck(f'{lang}: each reference says how it was read and that it was not read cover to cover',all(('cover to cover' in i if lang=='EN' else 'capa a capa' in i) for i in items))
        ck(f'{lang}: abstract and status table say none was read in full',('The three books were read in full</td><td>No' in s) if lang=='EN' else ('inteiro</td><td>N' in s))
        ck(f'{lang}: page cites present (Piketty 52, 162, 248; Scott 36; Freyre 107, 39)',all(f'p. {x}' in s or f'p. {x}&ndash;' in s or f'pp. {x}' in s for x in (52,162,248,107,39)) and ('36' in s))
        ck(f'{lang}: Freyre page numbers flagged as taken from the index',('edition&rsquo;s index' in s) if lang=='EN' else ('&iacute;ndice' in s))
        ck(f'{lang}: assumption O3 is conditional and says not shown',('which is not shown' in s) if lang=='EN' else ('n&atilde;o &eacute; demonstrado' in s))
        ck(f'{lang}: O7 proposal marked not tested',('The author&rsquo;s proposal; no mechanism given; not tested' in s) if lang=='EN' else ('Proposta do autor; sem mecanismo; n&atilde;o testada' in s))
        ck(f'{lang}: no personal content',not re.search(r'my son|David|Tiffany|Pablo|meu filho|neighbou?r|vizinh',s))
        ck(f'{lang}: links WP-131 to 134',all(x in s for x in ('wp131-finance','wp132-born-appraised','wp133-the-grandchildren','wp134-the-growth')))
        ck(f'{lang}: ABNT mention','ABNT NBR 6023' in s)
        fa=re.search(rf'<figure class="viz" id="figA-{lang.lower()}">(.*?)</figure>',s,re.S)
        fb=re.search(rf'<figure class="viz" id="figB-{lang.lower()}">(.*?)</figure>',s,re.S)
        ck(f'{lang}: both figures present',bool(fa and fb))
        if fa and fb:
            rects=re.findall(r'<rect [^>]*data-regime="(\w+)" data-group="(\w+)" data-share="(\d+)"',fa.group(1))
            byreg={}
            for rg,g,sh in rects: byreg.setdefault(rg,{})[g]=int(sh)
            ck(f'{lang}: figA has 6 regimes x 4 groups',len(byreg)==6 and all(len(v)==4 for v in byreg.values()))
            ck(f'{lang}: figA shares sum to 100 in every regime',all(sum(v.values())==100 for v in byreg.values()))
            want={'E1910':'Europe 1910','US2010':'US 2010','E2010':'Europe 2010','SC':'Scandinavia','LOW':'Low'}
            ok=all(tuple(byreg[k][g] for g in GROUPS)==shares(n) for k,n in want.items() if k in byreg)
            ck(f'{lang}: figA bars equal Table 7.2 as read (five regimes)',ok and set(want)<=set(byreg))
            ck(f'{lang}: figA equal-shares row = population shares',tuple(byreg.get('EQ',{}).get(g) for g in GROUPS)==POP)
            pts=re.findall(r'data-a="(\d+)" data-v="(\d+)"',fb.group(1))
            ck(f'{lang}: figB rings at (40, 8) and (60, 12) match alpha/r at 5%',pts==[('40','8'),('60','12')] and all(abs(int(a)/5-int(v)*1.0)<1e-9 and True for a,v in [(40,8)]) and abs(60/5-12)<1e-9)
            lines=re.findall(r'<polyline points="([^"]+)"[^>]*data-r="(\d+)"',fb.group(1))
            def y_of(py): return (240-float(py))*20/200
            good=len(lines)==3
            for pts_s,r in lines:
                P=[tuple(map(float,p.split(','))) for p in pts_s.split()]
                for (px,py),a in zip(P,range(0,61,10)):
                    if abs(y_of(py)-a/int(r))>0.06: good=False
            ck(f'{lang}: figB lines follow beta = alpha / r at 3, 5, 7%',good)
            ck(f'{lang}: figures credit our arithmetic',('Our arithmetic' in fb.group(1) and 'our own' in fa.group(1)) if lang=='EN' else ('Aritm&eacute;tica nossa' in fb.group(1) and 'nossa' in fa.group(1)))
    ck('EN and PT cite the same three references and link the same WP pages',sorted(set(re.findall(r'href="(#ref-\d|wp13\d[^"]*)"',en)))==sorted(set(re.findall(r'href="(#ref-\d|wp13\d[^"]*)"',pt))))
    ck('Swift cited with year',all('1729' in s for s in (en,pt)))
    return out
for n,ok in run(html): check(n,ok)
def expect_fail(name,broken,needle):
    bad=[n for n,ok in run(broken) if not ok]
    check(f'control fails as it should: {name}',any(needle in n for n in bad))
expect_fail('delta-beta cell altered',html.replace('<td class="n">6.67</td>','<td class="n">6.07</td>',1),'delta-beta')
expect_fail('per-capita cell altered',html.replace('<td class="n">3.89</td>','<td class="n">9.89</td>',1),'per-capita')
expect_fail('figA bar share altered',html.replace('data-regime="US2010" data-group="t1" data-share="35"','data-regime="US2010" data-group="t1" data-share="40"',1),'figA')
expect_fail('figB ring moved',html.replace('data-a="60" data-v="12"','data-a="60" data-v="14"',1),'figB rings')
expect_fail('"not read cover to cover" removed',re.sub(r'not read cover to cover','read',html,count=1),'cover to cover')
expect_fail('O7 label removed',html.replace('no mechanism given; not tested','established'),'O7')
expect_fail('index caveat for Freyre removed',html.replace('edition&rsquo;s index','book'),'Freyre page numbers')
expect_fail('personal name inserted',html.replace('4 October 2026.','Pablo.'),'personal')
expect_fail('WP-134 link dropped from PT',html[:html.index('id="pt"')]+html[html.index('id="pt"'):].replace('wp134-the-growth-imperative-tested.html','#'),'links WP-131')
# a broken first-law derivation must be caught by the independent check
check('control: using alpha*r instead of alpha/r breaks the 8/12/20 example',not (round(0.40*0.05,6)==8))

# ---- optional: check the quoted numbers against the extracted source text, if present on this machine ----
src=os.path.expanduser('~/wp135')
def srcs(name):
    p=os.path.join(src,name)
    return open(p,encoding='utf8',errors='ignore').read() if os.path.exists(p) else None
pk=srcs('piketty.txt'); fr=srcs('freyre.txt')
if pk is None: print('SKIP source-text checks (extracted texts not on this machine)')
else:
    pk1=re.sub(r'\s+',' ',pk); fr1=re.sub(r'\s+',' ',fr)
    check('source text: Table 7.2 row "The bottom 50% ... 25% 10% 5% 5% 5%" present',bool(re.search(r'bottom 50%\s+\W*lower class\W*\s+25%\s+10%\s+5%\s+5%\s+5%',pk)))
    check('source text: Table 7.2 row top 10% 30 50 60 70 90 present',bool(re.search(r'top 10% .upper class.\s+30%\s+50%\s+60%\s+70%\s+90%',pk)))
    check('source text: "twelve years of national income" and "twenty years of national income" present',('twelve years of national income' in pk1) and ('twenty years of national income' in pk1))
    check('source text: Freyre "seu capital, sua máquina de trabalho" present',('seu capital, sua máquina de trabalho' in fr1))
    check('source text: Freyre "pária de usina" present',('pária de usina' in fr1))
print()
print('[HONESTY] This script checks the arithmetic, the figure data, the labels and the structure. It does not check page numbers against the printed books, nor whether machines are owned as capital is; both are stated as open on the page.')
print('all checks passed' if not fails else f'{len(fails)} FAILED: {fails}')
sys.exit(1 if fails else 0)
