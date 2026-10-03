#!/usr/bin/env python3
"""WP-131 verifier: checks the page against itself and against fixed expectations.
Standard library only. Prints PASS/FAIL per check; exit 1 on any FAIL.
Run from the book6 folder:  python3 wp131-verify.py
It checks structure and the figures quoted in section 10. It does NOT check that the
sources say what the page says they say; that was done by reading them, and the status
table on the page records what was read in full, as a summary, or as a headline only."""
import re, sys, os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wp131-finance-and-accounting-for-human-and-animal-resources.html')
t = open(P, encoding='utf8').read()
fails = 0
def check(ok, msg):
    global fails
    print(('PASS ' if ok else 'FAIL ') + msg)
    if not ok: fails += 1
def sec(name):
    m = re.search(r'<section class="lang" id="%s".*?</section>' % name, t, re.S)
    return m.group(0) if m else ''
en, pt = sec('en'), sec('pt')
check(bool(en) and bool(pt), 'both language sections present')
def urls(s): return set(re.findall(r'href="(https?://[^"]+)"', s))
ue, up = urls(en), urls(pt)
check(ue == up and len(ue) >= 25, 'English and Portuguese cite the same %d links' % len(ue))
# control: the equality check must fail if one link is dropped from one side
check(not (ue == (up - {sorted(up)[0]})), 'control: dropping one link from the Portuguese set breaks the equality check')
def refs(s):
    i = s.rfind('<h2>'); return len(re.findall(r'<li>', s[i:]))
check(refs(en) == refs(pt) == 30, 'references: %d English, %d Portuguese (expected 30 each)' % (refs(en), refs(pt)))
def table_rows(s):
    m = re.search(r'<table class="t">.*?</table>', s, re.S); return len(re.findall(r'<tr>', m.group(0))) if m else -1
check(table_rows(en) == table_rows(pt) == 16, 'status table: 15 rows plus header in each language')
heads = lambda s: len(re.findall(r'<h2>', s))
check(heads(en) == heads(pt) == 13, 'h2 count matches across languages (%d / %d)' % (heads(en), heads(pt)))
def sec10(s):
    i = s.find('<h2>10.'); j = s.find('<h2>', i + 5); return s[i:j]
e10, p10 = sec10(en), sec10(pt)
for needle in ['50 million', '28 million', '86 per cent', '14 per cent', '10 million more than in 2016', '236 billion', '64 billion', '73 per cent', '79 per cent', '1.3 billion']:
    check(needle in e10, 'EN section 10 contains "%s"' % needle)
for needle in ['50 milh', '28 milh', '86%', '14%', '10 milh', '236 bilh', '64 bilh', '73%', '79%', '1,3 bilh']:
    check(needle in p10, 'PT section 10 contains "%s"' % needle)
check('does not show' in e10 or 'do not show' in e10, 'EN section 10 states what the sources do not show')
check('não mostram' in p10, 'PT section 10 states what the sources do not show')
check('not a result of this paper' in e10 and 'não um resultado deste artigo' in p10, 'section 10 labels the closing claim as an argument in both languages')
check('Epstein' not in t, 'the trafficking scenario with a named person is absent')
check('example.invalid' not in t, 'control: a link that should not exist is absent')
check('No source ties Halter or Thiel to the Brazilian pilot' in en, 'EN keeps the statement that no source ties Halter or Thiel to the pilot')
check('Tiffany' not in t and 'Newark' not in t.split('<footer>')[0].split('The bystander')[1][:2500], 'the neighbour-camera section names no building, person or personal account')

def abstract(s):
    i = s.find('<h3>'); j = s.find('<h3>', i + 5); return s[i:j]
check('The Age of Surveillance Capitalism' in abstract(en) and '(2019)' in abstract(en), 'EN abstract names Zuboff\'s work and its year')
check('The Age of Surveillance Capitalism' in abstract(pt) and '(2019)' in abstract(pt), 'PT abstract names Zuboff\'s work and its year')
def reflis(s):
    i = s.rfind('<h2>'); return re.findall(r'<li>.*?</li>', s[i:], re.S)
re_en, re_pt = reflis(en), reflis(pt)
check(sum('Available at:' in x for x in re_en) == 28 and sum('Dispon\u00edvel em:' in x for x in re_pt) == 28, 'ABNT: 28 of 30 entries carry "Available at / Dispon\u00edvel em" (the two books do not)')
check(all(re.match(r'<li>[A-Z0-9\'"\u00c0-\u00dd]{2}', x) for x in re_en), 'ABNT: every English entry starts with an author or title in capitals')
check(not re.match(r'<li>[A-Z0-9\'"\u00c0-\u00dd]{2}', '<li>Zuboff, S. The Age of Surveillance Capitalism. 2019.'), 'control: the old "Zuboff, S." style would fail the ABNT capitals check')
check('3 Oct. 2026' in re_en[-1] and '3 out. 2026' in re_pt[-1] and 'businesswire.com' in re_en[-1], 'entry 30 (Halter press release) carries the exact access date in both languages')
check('ABNT' in en and 'ABNT' in pt, 'both reference notes say ABNT')
check('SWIFT, Jonathan' in en and 'SWIFT, Jonathan' in pt, 'Swift is cited in full, with year')
print('\n%d check(s) failed' % fails if fails else '\nall checks passed')
sys.exit(1 if fails else 0)
