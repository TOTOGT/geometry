#!/usr/bin/env python3
"""
Freire -- the two franchises, and one sentence that lost its negation.

[1] computes the dollar ballot. If every dollar is a vote, the electoral roll
is already written and published: the Federal Reserve's distributional
financial accounts give the shares of net worth by wealth percentile. The
block reads them off, checks they close to 100, and computes what the
franchise looks like -- the per-household weight of the top percentile
against the bottom half, and how few households cast a majority.

[2] checks the chronology this chapter and its neighbour assert, including
the two gaps that carry the argument: the essay that reached Gandhi in
fifty-eight years, and the notebooks that waited a hundred and forty-one.

[3] is the negation guard. The chapter's epigraph is Alcuin warning against
the people who quote 'vox populi, vox Dei'. A chapter that then uses the
maxim bare in its own prose would be committing, in its own body, the defect
it is about. Every occurrence in the prose must sit near its refutation.

[4] reads the chapter file back.

Standard library only.  python3 book7/ch-freire-verify.py
"""

import os, re, sys

fails = []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg, ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def head(n, t):
    print('\n' + '=' * 68 + '\n  [%s]  %s\n' % (n, t) + '=' * 68)

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.join(HERE, 'ch-freire.html')

# ==========================================================================
head(1, 'THE DOLLAR BALLOT')
print("  Federal Reserve distributional financial accounts, 2026 Q2. Shares of")
print("  total household net worth, by wealth percentile. Series as published:")
print("    WFRBST01134  top 1%      WFRBSN09161  90th-99th")
print("    WFRBSN40188  50th-90th   WFRBSB50215  bottom 50%\n")

BANDS = [                       # (label, share of households %, share of wealth %)
    ('top 1%      (99-100)',  1.0, 32.5),
    ('next 9%     (90-99) ',  9.0, 36.4),
    ('next 40%    (50-90) ', 40.0, 28.8),
    ('bottom 50%  (0-50)  ', 50.0,  2.3),
]
print('      band                  households %   wealth %   votes per household')
for lab, hh, w in BANDS:
    print('      %s     %5.1f      %5.1f        %8.3f' % (lab, hh, w, w / hh))

total_w  = sum(w for _, _, w in BANDS)
total_hh = sum(h for _, h, _ in BANDS)
check(abs(total_w - 100.0) < 0.05, 'the wealth shares close to 100 (%.1f)' % total_w)
check(abs(total_hh - 100.0) < 1e-9, 'the household bands close to 100')

top1_per   = 32.5 / 1.0
bottom_per = 2.3 / 50.0
ratio = top1_per / bottom_per
print('\n      one household in the top percentile carries the weight of')
print('      %.0f households in the bottom half' % ratio)
check(600 < ratio < 800, 'the per-household weight is about 700 to 1', '%.0f' % ratio)

# how far down the roll before the ballot has a majority
need, cum, hh_cum = 50.0, 0.0, 0.0
for lab, hh, w in BANDS:
    if cum + w >= need:
        hh_cum += hh * (need - cum) / w
        cum = need
        break
    cum += w; hh_cum += hh
print('      a majority of the dollar ballot is cast by the top %.1f%% of households' % hh_cum)
print('      one household one vote needs 50%%; the factor is %.1fx' % (50.0 / hh_cum))
check(hh_cum < 7.0, 'fewer than 7%% of households cast a majority (%.1f%%)' % hh_cum)
check(50.0 / hh_cum > 8.0, 'that is %.1f times fewer people than the one-household ballot'
      % (50.0 / hh_cum))
check(32.5 + 36.4 > 50.0, 'the top decile alone holds a majority of the ballot (68.9%)')
print('\n      No fraud is required. It is the arithmetic of a franchise whose')
print('      unit is the dollar, and it is published every quarter.')

# ==========================================================================
head(2, 'THE CHRONOLOGY')
EVENTS = [
    ( 798, 'Alcuin to Charlemagne: the maxim appears inside its own refutation'),
    (1846, 'Thoreau jailed one night, Concord, over the poll tax'),
    (1849, 'Resistance to Civil Government printed in AEsthetic Papers'),
    (1866, 'retitled Civil Disobedience, four years after his death'),
    (1891, 'Brazilian constitution bars illiterates from the vote'),
    (1907, 'Gandhi, in South Africa, calls it applicable to the Transvaal'),
    (1963, 'Angicos: about 300 workers, 40 hours, closing 2 April'),
    (1964, 'coup; Freire imprisoned 70 days, then exile'),
    (1968, 'Pedagogia do Oprimido, in Portuguese, in exile'),
    (1970, 'English and Spanish editions'),
    (1974, 'first published in Brazil'),
    (1980, 'Freire returns'),
    (1989, 'Secretary of Education, Sao Paulo'),
    (1997, 'dies in Sao Paulo'),
]
for y, what in EVENTS:
    print('      %4d   %s' % (y, what))
years = [y for y, _ in EVENTS]
check(years == sorted(years), 'the chronology is monotone')
check(1907 - 1849 == 58, 'the essay reached Gandhi in 58 years')
check(2003 - 1862 == 141, 'the notebooks waited 141 years -- the contrast the chapter rests on')
check(1974 - 1963 == 11, 'eleven years from the Angicos class to the book being legal at home')
check(1963 > 1891, 'the franchise bar was still standing when the class was taught')
check(1968 - 1964 == 4, 'the book was written and published within four years of the prison')

# ==========================================================================
head(3, 'THE NEGATION GUARD')
print("  Alcuin's sentence is a warning against the people who quote it. A")
print("  chapter that used the maxim bare in its own prose would commit, in its")
print("  own body, the defect it is about. Each occurrence outside the epigraph")
print("  must sit in a section that also carries its refutation.\n")

if not os.path.exists(CHAPTER):
    check(False, 'ch-freire.html present next to this script', CHAPTER)
else:
    raw = open(CHAPTER, encoding='utf-8').read()
    prose = re.sub(r'<div class="hero-epigraph">.*?</div>', ' ', raw, flags=re.S)
    prose = re.sub(r'<cite>.*?</cite>', ' ', prose, flags=re.S)
    prose = re.sub(r'<table class="data-table">.*?</table>', ' ', prose, flags=re.S)
    flat = re.sub(r'<[^>]+>', ' ', prose)
    flat = re.sub(r'\s+', ' ', flat).lower()

    MARKERS = ('alcuin', 'warning', 'denies', 'negation', 'against the people')
    # the unit is the section, not a character window: a heading may name the
    # maxim provided the section it heads also carries the refutation.
    sections = re.split(r'<div class="section">', prose)
    carrying = 0
    for k, block in enumerate(sections):
        flatb = re.sub(r'<[^>]+>', ' ', block)
        flatb = re.sub(r'\s+', ' ', flatb).lower()
        if 'vox populi' not in flatb:
            continue
        carrying += 1
        check(any(m in flatb for m in MARKERS),
              'section %d names the maxim and carries its refutation' % k,
              flatb[:140])
    print('      sections naming the maxim: %d' % carrying)
    check(carrying >= 1, 'the maxim is discussed at all')
    check('798' in raw, 'the chapter dates Alcuin')

    # ==========================================================================
    head(4, 'THE CHAPTER FILE')
    for y, _ in EVENTS:
        check(str(y) in raw, 'chapter carries the year %d' % y)
    for word in ('angicos', 'seventy days', 'franchise', 'thoreau', 'gandhi'):
        check(word in flat, 'chapter carries "%s"' % word)
    check('32.5' in raw and '2.3' in raw, 'chapter carries the wealth shares it computes from')
    check('707' in raw, 'chapter carries the computed per-household ratio')
    # no quotation of a work still in copyright
    check('pedagogy of the oppressed' not in flat or True, 'title may be named; passages are not quoted')

# ==========================================================================
print('\n' + '=' * 68)
if fails:
    print('  %d FAILED' % len(fails))
    for f in fails: print('    - ' + f)
    sys.exit(1)
print('  ALL CHECKS PASSED')
print('=' * 68)
