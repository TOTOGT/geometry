#!/usr/bin/env python3
"""ch07_audit_check.py -- read-only: recompute the corridor totals of ch07/ch08/ch09 from the page's own site data and per-unit figures (audit 2026-11-15)."""
import re, os, sys, collections, datetime
bad = 0
def ck(n, ok):
    global bad; bad += (not ok); print(('PASS ' if ok else 'FAIL ') + n)
here = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(here, 'ch07.html'), encoding='utf-8', errors='replace').read()
rows = re.findall(r'city:"(\w+)",size:"(\w+)"', s)
KW = {'small': 40, 'medium': 200, 'large': 500}; USD = {'small': 60, 'medium': 150, 'large': 500}   # per-unit figures printed on the page (kW, $k)
cnt = collections.Counter(rows)
print('INFO site data (JavaScript):', dict(sorted(cnt.items())))
kw_js = sum(KW[z] for _, z in rows); usd_js = sum(USD[z] for _, z in rows)
ck('site data has 25 sites: Newark 14, Belleville 8, Harrison 3', len(rows) == 25 and sum(1 for c, _ in rows if c == 'Newark') == 14)
# prose mix: Newark 9 small/4 medium/1 large; Belleville 5 small/3 medium (ch09); Harrison 3 medium
prose = {'small': 9+5, 'medium': 4+3+3, 'large': 1}
kw_p = sum(KW[z]*n for z, n in prose.items()); usd_p = sum(USD[z]*n for z, n in prose.items())
print('INFO totals from site data: %d kW, $%dk; from prose mix %s: %d kW, $%dk; page states ~2.6 MW and ~$2.8M' % (kw_js, usd_js, prose, kw_p, usd_p))
ck('Newark class mix: prose says 9 small/4 medium/1 large; site data has 10 small/3 medium/1 large (one unit differs)', cnt[('Newark', 'small')] == 10 and cnt[('Newark', 'medium')] == 3 and (9, 4) != (cnt[('Newark', 'small')], cnt[('Newark', 'medium')]))
ck('stated 2.6 MW matches neither the site data (%.2f MW) nor the prose mix (%.2f MW) at the printed per-unit kW' % (kw_js/1000, kw_p/1000), abs(kw_js-2600) > 100 and abs(kw_p-2600) > 100)
ck('stated ~$2.8M is consistent with both (%.2f and %.2f $M)' % (usd_js/1000, usd_p/1000), round(usd_js/1000, 1) in (2.7, 2.8) and round(usd_p/1000, 1) == 2.8)
ck('Harrison: 3 medium = 600 kW, $450k (ch08)', 3*200 == 600 and 3*150 == 450)
d = (datetime.date(2026, 7, 19) - datetime.date(2026, 6, 11)).days + 1
ck('Jun 11 - Jul 19, 2026 inclusive = 39 days (ch08)', d == 39)
print('NOTE hand argument, not computed: peak 500 kW "at storm scale" and the per-class kW/cost are design estimates with no derivation on the pages; 2.6 MW may use a diversity factor that is not stated. The Resilient NJ NOFA terms (up to $350k, 12-month plan) and the "deadline passed" status were not verified.')
sys.exit(1 if bad else 0)
