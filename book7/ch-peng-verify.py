#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ch-peng-verify.py -- companion to book7/ch-peng.html.

Standard library only; needs pdftotext for the sourcing blocks (SKIP, never PASS, when a PDF
is missing). What it checks, and what it does not:

  [1] the schedule arithmetic: 18 + 6 + 18 = 42 months, and the phase month ranges abut
  [2] the metric table: every Phase 2 threshold is at least as demanding as its Phase 1 one
      (control: a table with two columns swapped must be reported as not monotone)
  [3] sourcing against DARPA-PS-26-129 (the statements Part I of the page uses)
  [4] sourcing against Kofoed et al., Nature 2025 (the one mechanism Part II names)
  [5] the corpus's Polylaminin page says what Part III quotes it as saying, and does not
      itself mention PENG (control: the same search finds 'Polylaminin' there)

It does not touch the biology, the funding, or any claim about eligibility.

    python3 book7/ch-peng-verify.py
"""
import os, re, subprocess, sys

FAIL = []
def check(ok, msg):
    print(('    PASS  ' if ok else '    FAIL  ') + msg)
    if not ok: FAIL.append(msg)
def head(n, t): print('\n' + '=' * 72 + '\n  [%s]  %s\n' % (n, t) + '=' * 72)
def norm(s): return re.sub(r'\s+', ' ', s.replace('ﬁ', 'fi').replace('ﬂ', 'fl'))

HERE = os.path.dirname(os.path.abspath(__file__))
_D = next((q for q in (os.path.expanduser('~/Downloads/'), os.path.expanduser('~/mnt/Downloads/')) if os.path.isdir(q)), None)
def pdf(prefix):
    if not _D: return None
    for fn in os.listdir(_D):
        if fn.lower().startswith(prefix):
            try:
                o = subprocess.run(['pdftotext', '-layout', os.path.join(_D, fn), '-'], capture_output=True, text=True, timeout=180)
                if o.returncode == 0 and o.stdout: return norm(o.stdout)
            except Exception:
                return None
    return None

head(1, 'the schedule arithmetic')
p1a, p1b, p2 = 18, 6, 18
check(p1a + p1b + p2 == 42, '18 + 6 + 18 = 42 months')
check((1, 18) == (1, p1a) and (p1a + 1, p1a + p1b) == (19, 24) and (p1a + p1b + 1, p1a + p1b + p2) == (25, 42),
      'the month ranges 1-18, 19-24, 25-42 abut with no gap or overlap')
check(p1a + p1b + p2 != 36, 'control: 36 would be the wrong total')

head(2, 'the metric table: Phase 2 at least as demanding as Phase 1')
# (pillar, Phase 1, Phase 2, direction): +1 means larger is harder; -1 means smaller (e.g. time) is harder
M = [
    ('targeting: percent of nascent proteins edited', 50, 75, +1),
    ('targeting: weeks allowed', 8, 4, -1),
    ('chemistry: edit sites', 3, 5, +1),
    ('chemistry: edits per machine (more than)', 5, 20, +1),
    ('multiplexing: edits per protein (more than)', 2, 3, +1),
    ('multiplexing: cell types (more than)', 2, 3, +1),
    ('readiness: stable weeks (hours-days is under 1 week; more than 3 weeks in Phase 2)', 1, 3, +1),
]
def monotone(rows): return all((b - a) * d >= 0 for _, a, b, d in rows)
check(monotone(M), 'every Phase 2 threshold is at least as demanding as its Phase 1 counterpart (%d rows)' % len(M))
swapped = [(n, b, a, d) for n, a, b, d in M[:2]] + M[2:]
check(not monotone(swapped), 'control: with the first two rows swapped between phases the table is reported NOT monotone')

head(3, 'sourcing against DARPA-PS-26-129 in ~/Downloads')
d = pdf('darpa-ps-26-129')
if d is None:
    print('    SKIP  the solicitation (or pdftotext) is not available; none of the sourcing below is checked')
else:
    for label, needle in [
        ('number and title', 'DARPA-PS-26-129'),
        ('title text', 'Protein ENGineering (PENG)'),
        ('posting date', 'August 7, 2026'),
        ('tentative proposal due date', 'October 19, 2026'),
        ('the three phase lengths', 'Eighteen months for Phase 1A. Six months for Phase 1B. Eighteen months for Phase 2'),
        ('42-month programme', '42-month'),
        ('three structural families', 'globular, transmembrane, and fibrous'),
        ('unannounced targets in Phase 1B', 'previously unannounced'),
        ('in native cells, not isolated preparations', 'not isolated in vitro protein preparations'),
        ('no human subjects research', 'must not include human subjects research'),
        ('gene editing as a permanent binary switch', 'permanent, binary switch'),
        ('the functional execution layer', 'functional execution layer'),
        ('the Muir paper is among the three cited', 'Programmable protein ligation on cell surfaces'),
    ]:
        check(needle in d, 'solicitation: ' + label)
    check('Phase 1A (Base): Platform Foundations (Months 1' in d and 'Phase 1B (Option Period 1): Capability Demonstration (Months 19' in d and 'Phase 2 (Option Period 2): Advanced System Integration (Months 25' in d,
          'solicitation: the month ranges of the three phases')
    check('BioNTech' not in d, 'control: a name the solicitation does not contain is not found')

head(4, 'sourcing against Kofoed et al., Nature 2025 in ~/Downloads')
m = pdf('programmable protein ligation')
if m is None:
    print('    SKIP  the Muir paper (or pdftotext) is not available; none of the sourcing below is checked')
else:
    for label, needle in [
        ('doi', '10.1038/s41586-025-09287-2'),
        ('proximity-gated protein trans-splicing', 'proximity-gated protein trans-splicing'),
        ('two otherwise inactive polypeptide fragments', 'two otherwise inactive polypeptide fragments'),
        ('cell surfaces', 'cell surfaces'),
    ]:
        check(needle in m, 'Muir paper: ' + label)

head(5, 'what the corpus Polylaminin page says')
pp = os.path.join(HERE, 'Polylaminin.html')
if not os.path.exists(pp):
    print('    SKIP  book7/Polylaminin.html not found')
else:
    import html
    t = open(pp, encoding='utf-8', errors='ignore').read()
    t = norm(html.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'(?s)<(script|style).*?</\1>', '', t)))).lower()
    for label, needle in [
        ('laminin polymerised at acidic pH', 'polymerised at acidic ph'),
        ('the 2024 pilot is a preprint, not peer-reviewed', 'not peer-reviewed'),
        ('ANVISA authorised a Phase I safety trial in January 2026', 'anvisa authorised a phase i safety trial in january 2026'),
        ('the fold reading is a Whitney A1 fold', 'whitney a'),
        ('the chapter says its Lean file is not held', 'file not held here'),
    ]:
        check(needle in t, 'Polylaminin page: ' + label)
    check('peng' not in re.findall(r'[a-z]+', t), 'the Polylaminin page does not itself mention PENG (so this chapter adds the link, not the page)')
    check('polylaminin' in t, 'control: the same search finds the word Polylaminin on that page')

print()
if FAIL:
    print('FAILED: %d check(s)' % len(FAIL)); sys.exit(1)
print('all checks passed'); sys.exit(0)
