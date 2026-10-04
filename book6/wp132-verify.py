#!/usr/bin/env python3
"""Checks WP-132 against the numbers it quotes. Run: python3 wp132-verify.py [page.html]
Controls at the bottom must FAIL on deliberately broken copies, or the script proves nothing."""
import re, sys, os
here = os.path.dirname(os.path.abspath(__file__))
path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, 'wp132-born-appraised-the-debt-share-of-a-newborn.html')
html = open(path, encoding='utf8').read()
import re as _re_gen
# R25/R26: the generated blocks (subject tag, Across the series, GSS stamp) carry their own links and are not part of the page's argument
html = _re_gen.sub(r'<!--po-([a-z]+)-->.*?<!--/po-\1-->', '', html, flags=_re_gen.S)
fails = []
def check(name, ok):
    print(('PASS ' if ok else 'FAIL ') + name)
    if not ok: fails.append(name)
    return ok

# independent arithmetic from the sourced inputs
DEBT = 39_065_421e6      # FRED GFDEBTN, end Q1 2026
POP = 341.8e6            # Census Vintage 2025, 1 Jul 2025
BIRTHS = 3_606_400       # CDC provisional 2025
SS75 = 29.3e12           # Trustees 2026, 75-yr PV, 2026 dollars
share = DEBT / POP
exp = {
  'share_en': f"{round(share,-3):,.0f}", 'share_pt': f"{round(share,-3):,.0f}".replace(',', '.'),
  'mult_en': f"{1e6*POP/DEBT:.2f}", 'mult_pt': f"{1e6*POP/DEBT:.2f}".replace('.', ','),
  'acct_en': f"{1000/share*100:.2f}", 'acct_pt': f"{1000/share*100:.2f}".replace('.', ','),
  'cohort_en': f"{BIRTHS*share/1e9:,.0f}", 'cohort_pt': f"{BIRTHS*share/1e9:,.0f}".replace(',', '.'),
  'share2_en': f"{round((DEBT+SS75)/POP,-3):,.0f}", 'share2_pt': f"{round((DEBT+SS75)/POP,-3):,.0f}".replace(',', '.'),
}
def sections(h):
    en = h[h.index('id="en"'):h.index('id="pt"')]
    pt = h[h.index('id="pt"'):]
    return en, pt
def run(h, label=''):
    out = []
    def ck(name, ok): out.append((name, ok))
    en, pt = sections(h)
    ck('both language sections present', bool(en) and bool(pt))
    for lang, s in (('EN', en), ('PT', pt)):
        k = 'en' if lang == 'EN' else 'pt'
        ck(f'{lang}: per-resident share ${exp["share_"+k]}', exp['share_'+k] in s)
        ck(f'{lang}: multiple of debt needed {exp["mult_"+k]}', exp['mult_'+k] in s)
        ck(f'{lang}: account is {exp["acct_"+k]} per cent of share', exp['acct_'+k] in s)
        ck(f'{lang}: cohort figure {exp["cohort_"+k]} billion', exp['cohort_'+k] in s)
        ck(f'{lang}: share with Social Security shortfall {exp["share2_"+k]}', exp['share2_'+k] in s)
        ck(f'{lang}: 11 h2 headings', len(re.findall(r'<h2>', s)) == 11)
        refs = re.search(r'<ol>(.*?)</ol>', s, re.S).group(1)
        items = re.findall(r'<li>(.*?)</li>', refs, re.S)
        ck(f'{lang}: 10 references', len(items) == 10)
        ck(f'{lang}: every reference has Available at/Disponível em, [s. d.] or a date, and access date 3 Oct',
           all(('Available at' in i or 'Disponível em' in i) and re.search(r'3 (Oct|out)\. 2026', i) for i in items))
        ck(f'{lang}: ABNT entries start with capitals', all(re.match(r'[A-Z][A-Z\.\' ]{3,}', re.sub(r'<[^>]+>', '', i)) for i in items))
        tab = re.findall(r'<tr>', s)
        ck(f'{lang}: status table has 9 data rows + 2 headers + 6 numbers rows', len(tab) == 6 + 1 + 9 + 1)
        ck(f'{lang}: 34-35 trillion flagged out of date', ('Out of date' in s) if lang == 'EN' else ('Desatualizada' in s))
        ck(f'{lang}: says no source assigns debt to an SSN', ('Not found in any source read' in s) if lang == 'EN' else ('Não encontrada em nenhuma fonte lida' in s))
        ck(f'{lang}: mentions ABNT', 'ABNT NBR 6023' in s)
        ck(f'{lang}: no personal/family content', not re.search(r'my son|David|Tiffany|Pablo|meu filho', s))
        ck(f'{lang}: links to WP-131', 'wp131-finance-and-accounting-for-human-and-animal-resources.html' in s)
    ue = sorted(set(re.findall(r'href="(https?://[^"]+)"', en)))
    up = sorted(set(re.findall(r'href="(https?://[^"]+)"', pt)))
    ck('EN and PT link the same 10 sources', ue == up and len(ue) == 10)
    ck('swift cited with year in both', all('1729' in s and 'SWIFT, Jonathan' in s for s in (en, pt)))
    return out
res = run(html)
for n, ok in res: check(n, ok)

# ---- controls: each broken copy must fail at least the check it targets ----
def expect_fail(name, broken, needle):
    r = run(broken)
    bad = [n for n, ok in r if not ok]
    check(f'control fails as it should: {name}', any(needle in n for n in bad))
expect_fail('share changed to 134,000', html.replace('114,000', '134,000'), 'per-resident share')
expect_fail('one source link dropped from PT', html[:html.index('id="pt"')] + html[html.index('id="pt"'):].replace('href="https://www.irs.gov/pub/irs-pdf/f4547.pdf"', 'href="#"'), 'same 10 sources')
expect_fail('the "not found" status deleted in EN', html.replace('Not found in any source read', 'Established'), 'no source assigns')
expect_fail('a family name inserted', html.replace('3 October 2026.', 'My son David.'), 'no personal')
expect_fail('multiple 8.75 changed', html.replace('8.75', '2.00'), 'multiple of debt')
print()
print('all checks passed' if not fails else f'{len(fails)} FAILED: {fails}')
sys.exit(1 if fails else 0)
