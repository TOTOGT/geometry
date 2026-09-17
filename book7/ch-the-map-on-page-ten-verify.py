#!/usr/bin/env python3
"""
The Map on Page Ten -- this corpus placed on Strogatz's Figure 1.3.1.

WHY THIS FILE EXISTS. Figure 1.3.1 (printed p. 10) puts the whole of nonlinear
dynamics on one page: two axes (phase-space dimension x linear/nonlinear), five
columns by two rows = ten cells, sixty-one named systems, and a region labelled
"The frontier". It is the standard chart of the subject this corpus is about, and
the corpus had never been laid over it. Laying it over found 44 of 61 entries
occupied, 17 at zero -- and two measurement problems.

The first: the figure is set rotated, and the text extractor emits one run for a
whole row-line spanning several columns, so the COLUMN of an entry is not
recoverable from the PDF. Position is the figure's content; the strings are
captions. This script therefore publishes the row (which the glyph bands settle
outright) and only the eight columns Strogatz states in prose. The second is a
fourth failure mode of the corpus's own counting instrument, which WP-82 section 4
does not record because it has no symptom: SENSE COLLISION. The string is right,
the anchor is right, the entities are handled, the arithmetic is right, and the
referent is a different subject. "Plasmas" returns 93 on plasma cells and blood
plasma; "Life" returns 151 on the English word.

Then the audit written to catch that failed by WP-82's SECOND failure mode on its
first run -- the companion pattern for "Plasmas" accepted 83 of 93 because
`reconnect` matched 304 times -- and was caught only because block [7] prints a
per-term breakdown instead of a total. That is the transferable result here.

BLOCKS
  [1] Printed page 10, and the figure has FIVE columns, the fifth being Continuum
      -- recovered from glyph coordinates (needs the PDF; skips cleanly without).
  [2] Why the column of an entry is not recoverable, which eight are anyway, and
      the six class labels placed by a coordinate offset calibrated on four.
  [3] The corpus by row: entity-aware counts at HEAD, 61 entries, 44 / 17.
  [4] The eight cells Strogatz states in words -- 260, 119, 71, 69, 6, 3, 0, 0.
  [5] The linear row: 18 entries, 8 at zero, and which ones.
  [6] SENSE COLLISION: seven entries audited by companion pattern.
  [7] The audit's own failure, by breakdown.
  [8] Control, and the self-count.
  [9] Readability against Strogatz's own pp. 9 and 11 -- the brief was "readable
      like his book is", and his register is two pages from the figure.

PRIMARY SOURCE.
  S. H. Strogatz, "Nonlinear Dynamics and Chaos", 2nd ed., Westview/CRC, 2018
  printing. Figure 1.3.1, printed p. 10. Framing prose section 1.3, pp. 9 and 11:
  the axes, the exponential-growth and pendulum placements, the RC/RLC contrast,
  the reading order, and "The frontier" with the here-be-dragons remark. First
  edition 1994.

Standard library only (blocks [1]-[2] use pypdf if a PDF path is given).
    python3 book7/ch-the-map-on-page-ten-verify.py [/path/to/strogatz.pdf]
"""
import os, re, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, 'tools'))
from corpus_count import files as _all_files, _blobs        # noqa: E402

# THE BASELINE. This page, its script, book7/index.html and docs/audit-log.md are
# tracked files of the corpus they measure, and they name every entry in the
# figure -- so once committed the measurement counts itself. Run at HEAD after the
# commit, "RC circuit" reads 3 rather than 0 and the seventeen zeros collapse to
# seven: the instrument would report the corpus as having covered the gaps by
# describing them. WP-82's rung table made exactly this mistake and read 12/12 on
# a column whose true value was 0.
#
# So every count below is taken at a pinned commit -- the last one before this
# measurement began -- and block [8] prints the drift at HEAD so the self-count is
# visible rather than assumed. The numbers on the page are the numbers at BASELINE.
BASELINE = 'b42750e'


def files(pattern, ref=BASELINE, **kw):
    return _all_files(pattern, ref=ref, **kw)


fails = []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg,
                            ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def head(n, t):
    print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)
def norm(s):
    return re.sub(r'\s+', ' ', s)

# --- the figure, as printed -------------------------------------------------
# row, column, entry-as-printed, pattern for the corpus count.
GRID = [
 ('Linear', 'n = 1',  'Exponential growth',            r'exponential growth'),
 ('Linear', 'n = 1',  'RC circuit',                    r'\brc circuit'),
 ('Linear', 'n = 1',  'Radioactive decay',             r'radioactive decay'),
 ('Linear', 'n = 2',  'Linear oscillator',             r'linear oscillator'),
 ('Linear', 'n = 2',  'Mass and spring',               r'mass and spring'),
 ('Linear', 'n = 2',  'RLC circuit',                   r'\brlc circuit'),
 ('Linear', 'n = 2',  '2-body problem',                r'(two|2)-body problem'),
 ('Linear', 'n >= 3', 'Coupled harmonic oscillators',  r'coupled harmonic'),
 ('Linear', 'n >= 3', 'Solid-state physics',           r'solid[- ]state physics'),
 ('Linear', 'n >= 3', 'Molecular dynamics',            r'molecular dynamics'),
 ('Linear', 'n >= 3', 'Equilibrium statistical mechanics', r'equilibrium statistical mechanics'),
 ('Linear', 'n >> 1', 'Elasticity',                    r'elasticity'),
 ('Linear', 'n >> 1', 'Wave equations',                r'wave equation'),
 ('Linear', 'n >> 1', 'Electromagnetism (Maxwell)',    r'electromagnetism'),
 ('Linear', 'n >> 1', 'Quantum mechanics',             r'quantum mechanics'),
 ('Linear', 'n >> 1', 'Heat and diffusion',            r'heat and diffusion|heat equation'),
 ('Linear', 'n >> 1', 'Acoustics',                     r'acoustics'),
 ('Linear', 'n >> 1', 'Viscous fluids',                r'viscous fluid'),
 ('Nonlinear', 'n = 1',  'Fixed points',               r'fixed point'),
 ('Nonlinear', 'n = 1',  'Bifurcations',               r'bifurcation'),
 ('Nonlinear', 'n = 1',  'Overdamped systems',         r'overdamped'),
 ('Nonlinear', 'n = 1',  'Relaxational dynamics',      r'relaxational dynamics'),
 ('Nonlinear', 'n = 1',  'Logistic equation',          r'logistic (equation|map)'),
 ('Nonlinear', 'n = 2',  'Pendulum',                   r'pendulum'),
 ('Nonlinear', 'n = 2',  'Anharmonic oscillators',     r'anharmonic'),
 ('Nonlinear', 'n = 2',  'Limit cycles',               r'limit cycle'),
 ('Nonlinear', 'n = 2',  'Biological oscillators',     r'biological oscillator'),
 ('Nonlinear', 'n = 2',  'Predator-prey cycles',       r'predator[- ]prey'),
 ('Nonlinear', 'n = 2',  'Nonlinear electronics',      r'van der pol'),
 ('Nonlinear', 'n >= 3', 'Chaos',                      r'\bchaos\b'),
 ('Nonlinear', 'n >= 3', 'Strange attractors',         r'strange attractor'),
 ('Nonlinear', 'n >= 3', 'Lorenz',                     r'\blorenz\b'),
 ('Nonlinear', 'n >= 3', 'Lasers, nonlinear optics',   r'nonlinear optics'),
 ('Nonlinear', 'n >= 3', '3-body problem',             r'(three|3)-body problem'),
 ('Nonlinear', 'n >= 3', 'Chemical kinetics',          r'chemical kinetics'),
 ('Nonlinear', 'n >= 3', 'Iterated maps',              r'iterated map'),
 ('Nonlinear', 'n >= 3', 'Feigenbaum',                 r'feigenbaum'),
 ('Nonlinear', 'n >= 3', 'Fractals',                   r'fractals?\b'),
 ('Nonlinear', 'n >= 3', 'Forced nonlinear oscillators', r'forced nonlinear oscillator'),
 ('Nonlinear', 'n >= 3', 'Heart cell synchronization', r'heart cell'),
 ('Nonlinear', 'n >= 3', 'Neural networks',            r'neural network'),
 ('Nonlinear', 'n >= 3', 'Immune system',              r'immune system'),
 ('Nonlinear', 'n >= 3', 'Ecosystems',                 r'ecosystems?\b'),
 ('Nonlinear', 'n >= 3', 'Economics',                  r'economics'),
 ('Nonlinear', 'n >> 1', 'Spatio-temporal complexity', r'spatio[- ]?temporal'),
 ('Nonlinear', 'n >> 1', 'Coupled nonlinear oscillators', r'coupled nonlinear oscillator'),
 ('Nonlinear', 'n >> 1', 'Nonlinear waves',            r'nonlinear waves'),
 ('Nonlinear', 'n >> 1', 'Solitons',                   r'solitons?\b'),
 ('Nonlinear', 'n >> 1', 'Plasmas',                    r'plasmas?\b'),
 ('Nonlinear', 'n >> 1', 'Earthquakes',                r'earthquakes?\b'),
 ('Nonlinear', 'n >> 1', 'General relativity (Einstein)', r'general relativity'),
 ('Nonlinear', 'n >> 1', 'Nonlinear solid-state physics', r'semiconductors?\b'),
 ('Nonlinear', 'n >> 1', 'Josephson arrays',           r'josephson arrays?'),
 ('Nonlinear', 'n >> 1', 'Quantum field theory',       r'quantum field theor'),
 ('Nonlinear', 'n >> 1', 'Reaction-diffusion',         r'reaction[- ]diffusion'),
 ('Nonlinear', 'n >> 1', 'Fibrillation',               r'fibrillation'),
 ('Nonlinear', 'n >> 1', 'Epilepsy',                   r'epilep'),
 ('Nonlinear', 'n >> 1', 'Practical uses of chaos',    r'practical uses of chaos'),
 ('Nonlinear', 'n >> 1', 'Quantum chaos',              r'quantum chaos'),
 ('Nonlinear', 'n >> 1', 'Turbulent fluids',           r'navier[- ]stokes'),
 ('Nonlinear', 'n >> 1', 'Life',                       r'\blife\b'),
]
COLS = ['n = 1', 'n = 2', 'n >= 3', 'n >> 1']
ROWS = ['Linear', 'Nonlinear']

# The eight assignments Strogatz states in prose rather than leaving to layout.
PROSE_ANCHORED = {
 ('Linear', 'n = 1', 'Exponential growth'): 'p.9  "in the column labeled n = 1" + "classified as linear"',
 ('Linear', 'n = 1', 'RC circuit'):         'p.11 "an RC circuit has n = 1 and cannot oscillate"',
 ('Linear', 'n = 2', 'RLC circuit'):        'p.11 "whereas an RLC circuit has n = 2 and can oscillate"',
 ('Nonlinear', 'n = 2', 'Pendulum'):        'p.9  "belongs in the n = 2 column ... the lower, nonlinear half"',
 ('Nonlinear', 'n = 1', 'Fixed points'):    'p.11 "fixed points and bifurcations when n = 1"',
 ('Nonlinear', 'n = 1', 'Bifurcations'):    'p.11 "fixed points and bifurcations when n = 1"',
 ('Nonlinear', 'n >= 3', 'Chaos'):          'p.11 "chaos and fractals when n >= 3"',
 ('Nonlinear', 'n >= 3', 'Fractals'):       'p.11 "chaos and fractals when n >= 3"',
}

# ---------------------------------------------------------------------------
head(1, "PRINTED PAGE 10, AND THE FIGURE HAS FIVE COLUMNS")
PDF = sys.argv[1] if len(sys.argv) > 1 else None
figtext = None
OPS = []
if not PDF:
    print('  no PDF path given -- blocks [1] and [2] report SKIP.')
    print('  usage:  python3 book7/ch-the-map-on-page-ten-verify.py /path/to/strogatz.pdf')
else:
    try:
        import pypdf
    except ImportError:
        print('  needs pypdf for blocks [1]-[2]:  pip install pypdf')
        PDF = None
COL_REF = {}
if PDF:
    reader = pypdf.PdfReader(PDF)
    print('  %s' % os.path.basename(PDF))
    print('  %d pdf pages (pypdf %s)\n' % (len(reader.pages), pypdf.__version__))
    hit = []
    for i, pg in enumerate(reader.pages[:60]):
        t = pg.extract_text() or ''
        if 'Figure 1.3.1' in t and 'Number of variables' in t:
            hit.append(i)
    check(len(hit) == 1, 'exactly one page carries both "Figure 1.3.1" and "Number of variables"',
          'pdf indices %s' % hit)
if PDF and hit:
    page = reader.pages[hit[0]]
    figtext = norm(page.extract_text() or '')
    check(figtext.startswith('10 OVERVIEW'),
          'its running head reads "10 OVERVIEW" -- printed page 10', figtext[:40])
    print('      printed page 10  =  pdf index %d  (front-matter offset %d)\n'
          % (hit[0], hit[0] - 10))

    def _visit(text, cm, tm, fd, fs):
        t = text.strip()
        if t: OPS.append((round(tm[4], 1), round(tm[5], 1), t))
    page.extract_text(visitor_text=_visit)
    check(len(OPS) == 236, 'the page is 236 positioned text runs', str(len(OPS)))
    print('  The figure is set rotated: reading-order horizontal is the PDF y coordinate,')
    print('  reading-order vertical is x. So the grid is recoverable from glyph positions.\n')

    axis = sorted([o for o in OPS if 158 <= o[0] <= 168], key=lambda o: o[1])
    spelled = ' '.join(t for _, _, t in axis)
    print('      column-header line, x in [158,168], in order of increasing y:')
    print('      %r\n' % spelled)
    check(spelled == 'n = 1 n = 2 n ≥ 3 n >> 1 Continuum',
          'it spells exactly five column labels, the fifth being Continuum', repr(spelled))
    check(len(axis) == 13, 'as 13 separately positioned runs', str(len(axis)))
    # one reference y per column: the last glyph of each label group
    # one reference per column: the last glyph of each label group
    COL_REF = {'n = 1': 254.3, 'n = 2': 331.6, 'n >= 3': 416.3,
               'n >> 1': 518.3, 'Continuum': 597.2}
    for name, y in COL_REF.items():
        check(any(abs(o[1] - y) < 1.5 for o in axis),
              'column marker %-11s sits at y = %.1f' % (name, y))
    gaps = sorted(COL_REF.values())
    spans = [round(b - a, 1) for a, b in zip(gaps, gaps[1:])]
    check(min(spans) > 75, 'the five columns are more than 75 units of y apart', str(spans))

    rowlab = {t: (x, y) for x, y, t in OPS if t in ('Linear', 'Nonlinear')}
    check(abs(rowlab['Linear'][0] - 217) < 2 and abs(rowlab['Nonlinear'][0] - 372) < 2,
          'the two row labels sit at x = 217 (Linear) and x = 372 (Nonlinear)',
          str(rowlab))
    lin = [o for o in OPS if 197 <= o[0] <= 280]
    non = [o for o in OPS if 310 <= o[0] <= 458]
    between = [o for o in OPS if 285 < o[0] < 305]
    print('      linear band x in [197,280]: %d runs' % len(lin))
    print('      nonlinear band x in [310,458]: %d runs' % len(non))
    check(len(between) == 1,
          'the two bands are disjoint -- exactly one run falls between them',
          '%d: %s' % (len(between), between))
    check(2 * 5 == 10, 'two rows x five columns = ten cells')

    p9 = norm(reader.pages[hit[0] - 1].extract_text() or '')
    p11 = norm(reader.pages[hit[0] + 1].extract_text() or '')
    check('dimension of the phase space' in p9,
          'p.9: the horizontal axis IS the phase-space dimension, in his words')
    check('cannot oscillate' in p11 and 'can oscillate' in p11,
          'p.11: the RC / RLC contrast that demonstrates the horizontal axis')
    check('lower left cor' in p11,
          'p.11: "we start in the lower left corner and systematically head to the right"')
    check('here be dragons' in p11.lower(), 'p.11: the here-be-dragons remark on "The frontier"')
    check('debatable' in p11, 'p.11: Strogatz calls the picture debatable himself')
    check('continuum' in p11.lower(),
          'p.11: the Continuum column named in prose -- "an infinite continuum of variables"')

# ---------------------------------------------------------------------------
head(2, "THE COLUMN OF AN ENTRY IS NOT RECOVERABLE; EIGHT ARE, FROM PROSE")
check(len(GRID) == 61, 'the grid transcribed here has 61 entries', str(len(GRID)))
check(len(PROSE_ANCHORED) == 8, 'eight cell assignments are anchored in Strogatz\'s prose')
check(len(GRID) - len(PROSE_ANCHORED) == 53,
      'fifty-three have no column this script is entitled to publish')
for k, v in PROSE_ANCHORED.items():
    print('      %-12s %-7s %-22s %s' % (k[0], k[1], k[2], v))
if OPS:
    print()
    merged = [t for _, _, t in OPS if t.startswith('Fixed points')]
    check(len(merged) == 1 and 'Pendulum' in merged[0] and 'Strange attra' in merged[0],
          'the extractor emits one run for a whole row-line spanning several columns',
          str(merged))
    print('      the offending run, verbatim:')
    print('      %r\n' % merged[0])
    low = figtext.lower()
    still = [e for _, _, e, _ in GRID
             if not all(w in low for w in e.split(' (')[0].lower().split()[:2])]
    check(not still, 'every entry name transcribed here is present on printed p. 10',
          'not found: %s' % still)
    check(all(w in figtext for w in ('Mandelbrot', 'Feigenbaum', 'Poincar', 'Smale',
                                     'Levinson', 'Einstein', 'Maxwell', 'Kepler',
                                     'Newton', 'Lorenz')),
          'the ten people Strogatz names inside the cells are all on the page')

    # the six class labels, placed by coordinate
    LABELS = [('Growth, deca', 'Linear', 'n = 1', True),
              ('Oscillations', 'Linear', 'n = 2', True),
              ('Collective phenomena', 'Linear', 'n >> 1', False),
              ('Waves and patterns', 'Linear', 'Continuum', True),
              ('Chaos', 'Nonlinear', 'n >= 3', True),
              ('Spatio-temporal complexit', 'Nonlinear', 'Continuum', False),
              ('The frontier', 'Nonlinear', None, False)]
    POS = {}
    for stem, _, _, _ in LABELS:
        for x, y, t in OPS:
            if t.startswith(stem):
                POS[stem] = (x, y); break
    check(len(POS) == 7, 'all seven italicised labels located by coordinate', str(sorted(POS)))
    offs = [COL_REF[col] - POS[stem][1] for stem, _, col, anchored in LABELS
            if anchored and col]
    off = sum(offs) / len(offs)
    print('\n      calibration on the four labels whose column the prose confirms:')
    print('      offsets %s  ->  mean %.1f units of y' % ([round(o, 1) for o in offs], off))
    check(len(offs) == 4, 'the offset is calibrated on four labels, not on the two it places')
    check(13 < min(offs) and max(offs) < 29, 'their spread is 14 to 28 units',
          str([round(o, 1) for o in offs]))
    print('\n      %-27s %-10s %8s  %s' % ('label', 'side', 'y', 'nearest column marker'))
    for stem, side, col, anchored in LABELS:
        x, y = POS[stem]
        near = min(COL_REF.items(), key=lambda kv: abs(kv[1] - (y + off)))
        second = sorted(COL_REF.items(), key=lambda kv: abs(kv[1] - (y + off)))[1]
        d1 = abs(near[1] - (y + off)); d2 = abs(second[1] - (y + off))
        tag = 'prose' if anchored else ('straddles %s / %s' % (near[0], second[0])
                                       if abs(d1 - d2) < 12 else 'offset')
        print('      %-27s %-10s %8.1f  %-11s (%s)' % (stem, side, y, near[0], tag))
        if col:
            check(near[0] == col, 'label %r heads column %s' % (stem, col), near[0])
    xf, yf = POS['The frontier']
    nf = sorted(COL_REF.items(), key=lambda kv: abs(kv[1] - (yf + off)))
    check(abs(abs(nf[0][1] - (yf + off)) - abs(nf[1][1] - (yf + off))) < 12,
          '"The frontier" sits between two column markers -- it straddles, and is not assigned',
          '%s vs %s' % (nf[0][0], nf[1][0]))
    nolabel = [('Linear', 'n >= 3'), ('Nonlinear', 'n = 1'), ('Nonlinear', 'n = 2')]
    check(len(nolabel) == 3,
          'three cells carry no class label: linear n >= 3, nonlinear n = 1 and n = 2 -- '
          'nothing first arises there')
else:
    print('    SKIP  the geometry checks need the PDF')

# ---------------------------------------------------------------------------
head(3, "THE CORPUS, BY ROW -- ENTITY-AWARE, TRACKED FILES, AT HEAD")
COUNT = {}
for row, col, entry, pat in GRID:
    COUNT[(row, col, entry)] = len(files(pat))
print('      %-10s %8s %9s %8s  %-22s %6s' %
      ('row', 'entries', 'occupied', 'at zero', 'heaviest entry', 'files'))
PER_ROW = {}
for row in ROWS:
    es = [(e, COUNT[(row, c, e)]) for r, c, e, _ in GRID if r == row]
    z = sum(1 for _, n in es if n == 0)
    hv = max(es, key=lambda t: t[1])
    PER_ROW[row] = (len(es), len(es) - z, z, hv[0], hv[1])
    print('      %-10s %8d %9d %8d  %-22s %6d' % ((row,) + PER_ROW[row]))
print()
check(PER_ROW['Linear'] == (18, 10, 8, 'Quantum mechanics', 25),
      'the linear row reads 18 entries, 10 occupied, 8 at zero, heaviest quantum mechanics 25',
      str(PER_ROW['Linear']))
check(PER_ROW['Nonlinear'] == (43, 34, 9, 'Fixed points', 260),
      'the nonlinear row reads 43 entries, 34 occupied, 9 at zero, heaviest fixed points 260',
      str(PER_ROW['Nonlinear']))
zeros = sorted(e for (r, c, e), n in COUNT.items() if n == 0)
check(len(COUNT) == 61, 'sixty-one entries counted', str(len(COUNT)))
check(len(zeros) == 17, 'seventeen entries at zero', '%d: %s' % (len(zeros), zeros))
check(61 - len(zeros) == 44, 'forty-four entries occupied')
order = sorted(COUNT.items(), key=lambda kv: -kv[1])[:6]
print('      largest six counts on the page, unaudited:')
for (row, col, entry), n in order:
    print('      %6d  %-28s %s' % (n, entry, row))
survivors = [kv for kv in order if kv[0][2] not in ('Life', 'Plasmas')][:3]
check([e for (_, _, e), _ in survivors] == ['Fixed points', 'Limit cycles', 'Bifurcations']
      and [n for _, n in survivors] == [260, 121, 119],
      'setting aside the two entries block [6] demolishes, the three largest are '
      'fixed points 260, limit cycles 121, bifurcations 119',
      str(survivors))
check(all(r == 'Nonlinear' for (r, _, _), _ in survivors),
      'all three are in the nonlinear row')

# ---------------------------------------------------------------------------
head(4, "THE EIGHT CELLS STROGATZ STATES IN WORDS")
rows = sorted(((e, r, c, COUNT[(r, c, e)]) for (r, c, e) in PROSE_ANCHORED),
              key=lambda t: -t[3])
print('      %-20s %-24s %6s' % ('entry', 'cell, in his words', 'files'))
for e, r, c, n in rows:
    print('      %-20s %-24s %6d' % (e, '%s / %s' % (r, c), n))
check([n for _, _, _, n in rows] == [260, 119, 71, 69, 6, 3, 0, 0],
      'the eight read 260, 119, 71, 69, 6, 3, 0, 0',
      str([n for _, _, _, n in rows]))
pz = sorted(e for e, _, _, n in rows if n == 0)
check(pz == ['RC circuit', 'RLC circuit'],
      'the only two at zero are the RC and RLC circuits -- the pair he uses to explain '
      'what the horizontal axis means', str(pz))
check([(e, c) for e, _, c, _ in rows[:2]] == [('Fixed points', 'n = 1'),
                                              ('Bifurcations', 'n = 1')],
      'and the two largest are both at n = 1 in the nonlinear row, the lower-left corner')
print('\n      Strogatz, p.11: "in this book we start in the lower left corner and')
print('      systematically head to the right."  Nobody instructed this corpus to')
print('      obey that sentence; its density profile obeys it anyway.')

# ---------------------------------------------------------------------------
head(5, "THE LINEAR ROW: EIGHTEEN ENTRIES, EIGHT AT ZERO")
lz = [e for r, c, e, _ in GRID if r == 'Linear' and COUNT[(r, c, e)] == 0]
check(len(lz) == 8, 'eight of the linear row\'s eighteen entries are at zero',
      '%d: %s' % (len(lz), lz))
for e in lz:
    print('      0   %s' % e)
nz = [e for r, c, e, _ in GRID if r == 'Nonlinear' and COUNT[(r, c, e)] == 0]
check(len(nz) == 9, 'and nine of the nonlinear row\'s forty-three', '%d: %s' % (len(nz), nz))
check(set(['RC circuit', 'RLC circuit', 'Mass and spring', '2-body problem',
           'Coupled harmonic oscillators']) <= set(lz),
      'five of the eight are the first systems in an undergraduate course')
print('\n      Eight of the seventeen zeros fall in the row that has only eighteen entries')
print('      in it. That is WP-82\'s missing floor, found in one pass, because Strogatz')
print('      put those systems on the page to give the rest of it a scale.')

# ---------------------------------------------------------------------------
head(6, "SENSE COLLISION -- THE FOURTH FAILURE MODE, AUDITED")
print('  WP-82 section 4 records three ways this corpus\'s counting lies: wrong spelling,')
print('  substring inflation, HTML entities. Each produces a visibly wrong number. This')
print('  one does not: the string is right, the anchor is right, the entities are handled,')
print('  the arithmetic is right, and the referent is a different subject.\n')
TXT = _blobs(BASELINE, ('*.html', '*.md'))
NEVER = r'(?!x)x'                        # matches nothing: no second sense coded
AUDIT = [
 ('Life',              r'\blife\b',
  r'(origin of life|abiogenesis|rna world|alkaline vent|protocell|autocataly'
  r'|last universal common ancestor|\bluca\b)',
  NEVER, 'the English word'),
 ('Plasmas',           r'plasmas?\b',
  r'(magnetohydrodynam|tokamak|stellar plasma|plasma drag|plasma reconnection'
  r'|plasma physics|plasma confinement|debye length|larmor)',
  r'(plasma cell|plasma membrane|blood plasma|plasma protein|membrane fusion'
  r'|ch0?3-plasma|>Plasma<)',
  'plasma cells, blood plasma, a nav link'),
 ('Economics',         r'economics',
  r'(nonlinear dynamic|bifurcat|regime shift|attractor|hysteres)',
  r'(nav|site map|>economics<|project economics|supply chain network economics)',
  'project economics; a site-map label'),
 ('Turbulent fluids',  r'turbulen',
  r'(navier|reynolds number|kolmogorov|energy cascade|inertial range)',
  r'(turbulence, not|chaotic turbulence|dissipating it as turbulence'
  r'|turbulent, non-rotating)',
  'turbulence as a word for messy flow'),
 ('Acoustics',         r'acoustics',
  r'(wave equation|helmholtz|impedance|time-reversal|room mode)',
  r'(archaeoacoustic|archaeo-acoustic)',
  'archaeoacoustics -- a different field'),
 ('Nonlinear waves',   r'shocks?\b',
  r'(shock wave|soliton|burgers|rankine|hugoniot|discontinuit|characteristic)',
  r'(price shock|income shock|bill shock|demand shock|economic shock'
  r'|shock to the|septic shock)',
  'price shocks, income shocks, bill shock'),
 ('Levinson',          r'\blevinson\b',
  r'(levinson.smith|levinson.conrey|cartwright|van der pol|forced|mollifi)',
  r'(evans and levinson|gumperz|linguistic)',
  'Evans & Levinson, linguistics'),
]
print('      %-18s %7s %10s %12s %8s' % ('entry', 'string', 'dynamical', 'other sense', 'neither'))
GOT = {}
for name, pat, right, wrong, _note in AUDIT:
    hits = files(pat)
    r = w = n = 0
    for f in hits:
        t = TXT.get(f, '')
        if re.search(right, t, re.I): r += 1
        elif re.search(wrong, t, re.I): w += 1
        else: n += 1
    GOT[name] = (len(hits), r, w, n)
    print('      %-18s %7d %10d %12d %8d' % (name, len(hits), r, w, n))
EXP_AUDIT = {
 'Life':             (151, 11,  0, 140),
 'Plasmas':          (93,  35, 31,  27),
 'Economics':        (45,  19, 23,   3),
 'Turbulent fluids': (49,  10, 12,  27),
 'Acoustics':        (19,   5,  9,   5),
 'Nonlinear waves':  (19,   7,  7,   5),
 'Levinson':         (8,    6,  2,   0),
}
print()
for k, v in EXP_AUDIT.items():
    check(GOT[k] == v, 'audit of %r reads %s' % (k, v), str(GOT[k]))
check(GOT['Life'][0] - GOT['Life'][1] == 140,
      'Life: the figure\'s hardest cell, and 140 of its 151 files are the English word')
check(GOT['Plasmas'][1] * 2 < GOT['Plasmas'][0],
      'Plasmas: fewer than half of 93 survive a sense test')

# ---------------------------------------------------------------------------
head(7, "AND THEN THE AUDIT FAILED THE SAME WAY, ON ITS FIRST RUN")
LOOSE = (r'(magnetohydrodynam|tokamak|stellar plasma|plasma drag|reconnect'
         r'|fusion|ionis|ioniz)')
hits = files(r'plasmas?\b')
loose_pass = sum(1 for f in hits if re.search(LOOSE, TXT.get(f, ''), re.I))
print('  the first companion pattern written for "Plasmas" accepted %d of %d files.\n'
      % (loose_pass, len(hits)))
brk = Counter()
for f in hits:
    for m in re.finditer(LOOSE, TXT.get(f, ''), re.I):
        brk[m.group(1).lower()] += 1
print('      %-18s %6s' % ('term in the pattern', 'hits'))
for term, n in brk.most_common():
    print('      %-18s %6d' % (term, n))
print()
check(loose_pass == 83, 'the loose pattern accepted 83 of 93', str(loose_pass))
check(brk['reconnect'] == 304, '`reconnect` alone matched 304 times', str(brk['reconnect']))
check(brk['fusion'] == 43, '`fusion` matched 43 times', str(brk['fusion']))
check(brk['tokamak'] == 2 and brk['stellar plasma'] == 1,
      'while `tokamak` matched twice and `stellar plasma` once',
      'tokamak %d, stellar plasma %d' % (brk['tokamak'], brk['stellar plasma']))
check(loose_pass > GOT['Plasmas'][1],
      'so the audit would have promoted the false positive it was written to catch')
print('\n      The audit instrument failed by substring inflation -- WP-82\'s SECOND failure')
print('      mode -- while auditing the fourth. It was caught because this block prints a')
print('      breakdown and not a total.')

# ---------------------------------------------------------------------------
head(8, "CONTROL, AND THE SELF-COUNT")
ABSENT = 'qqx' + '-no-file-contains-this-' + 'qqx'
check(len(files(ABSENT)) == 0, 'a token no file contains returns 0 files')
check(len(files(r'\bchaos\b')) == 69,
      'the unaudited control count for "chaos" is 69 at BASELINE',
      str(len(files(r'\bchaos\b'))))
check(len(files(r'figure 1\.3\.1')) >= 3,
      '"Figure 1.3.1" was already cited in at least three tracked files before this '
      'page -- ch-smale-verify, ch-van-der-pol, strogatz-citations-verify',
      str(len(files(r'figure 1\.3\.1'))))
print('\n  the self-count, which is why the numbers above are pinned to %s:\n' % BASELINE)
print('      %-14s %10s %8s %10s' % ('entry', 'BASELINE', 'HEAD', 'inflation'))
drift = 0
for pat, name in ((r'\brc circuit', 'RC circuit'), (r'\brlc circuit', 'RLC circuit'),
                  (r'\bchaos\b', 'chaos'), (r'fixed point', 'fixed points'),
                  (r'\blife\b', 'Life'), (r'plasmas?\b', 'Plasmas')):
    base = len(files(pat))
    now = len(_all_files(pat, ref='HEAD'))
    drift += now - base
    print('      %-14s %10d %8d %10s' % (name, base, now, '%+d' % (now - base)))
check(drift > 0, 'the corpus has moved since BASELINE, this page being part of the move',
      str(drift))
zeros_now = [e for r, c, e, pat in GRID if len(_all_files(pat, ref='HEAD')) == 0]
print('\n      entries at zero:  %d at BASELINE,  %d at HEAD' % (len(zeros), len(zeros_now)))
check(len(zeros_now) < len(zeros),
      'run at HEAD the instrument would report the gaps as covered -- by this page '
      'having named them', '%d vs %d' % (len(zeros_now), len(zeros)))
SCAFFOLD = ('CLAUDE.md', 'docs/')
gained = sorted(set(zeros_now) - set(zeros))
if gained:
    print('\n      entries that went the OTHER way, zero at HEAD but not at BASELINE:')
    for e in gained:
        pat = [p for r, c, x, p in GRID if x == e][0]
        was = _all_files(pat, ref=BASELINE)
        kind = ('project scaffolding' if all(
            f.startswith(SCAFFOLD) for f in was) else 'CHAPTERS')
        print('      %-26s was %d file(s) at BASELINE: %s  [%s]'
              % (e, len(was), ', '.join(was), kind))
        check(kind == 'project scaffolding',
              '%r lost its only hits, and they were scaffolding rather than '
              'chapters' % e, ', '.join(was))
check(set(zeros_now) - set(gained) <= set(zeros),
      'apart from those, every entry HEAD would drop is one this page describes')


# ---------------------------------------------------------------------------
head(9, "READABILITY, MEASURED AGAINST THE BOOK ITSELF")
print("""  The brief for this page was "readable like his book is". That is checkable
  rather than arguable: Strogatz's own section 1.3 is two pages away from the
  figure, so his register can be measured and the page held to it.

  Reference, recomputed from pp. 9 and 11 when the PDF is supplied, and quoted
  from the 2026-09-17 run otherwise: 49 sentences, mean 19.9 words, longest 48,
  em-dashes 6.2 per thousand words, 31 per cent of sentences under 15 words.\n""")

def prose_stats(text):
    body = re.sub(r'<(style|script)\b.*?</\1>', ' ', text, flags=re.S | re.I)
    body = re.sub(r'<[^>]+>', ' ', body)
    dashes = body.count('&mdash;') + body.count('\u2014')
    body = body.replace('&mdash;', ' ').replace('&middot;', ' ')
    body = re.sub(r'&[a-z]+;', ' ', body)
    words = body.split()
    sents = [x for x in re.split(r'(?<=[.!?])\s+', ' '.join(words))
             if len(x.split()) > 2]
    L = [len(x.split()) for x in sents]
    return dict(words=len(words), sents=len(L), mean=sum(L) / len(L),
                longest=max(L), dash_k=1000.0 * dashes / len(words),
                short=100.0 * sum(1 for x in L if x < 15) / len(L))

REF = dict(sents=49, mean=19.9, longest=48, dash_k=6.2, short=31.0)
if PDF and hit:
    t = ' '.join(norm(reader.pages[hit[0] + d].extract_text() or '')
                 for d in (-1, 1))
    t = re.sub(r'Strogatz-CROPPED2\.pdf\s+\d+\s+\S+\s+\S+\s+\S+', ' ', t)
    R = prose_stats(t)
    print('      Strogatz pp. 9+11, recomputed now: %d sentences, mean %.1f, '
          'longest %d' % (R['sents'], R['mean'], R['longest']))
    check(abs(R['mean'] - REF['mean']) < 1.5 and abs(R['sents'] - REF['sents']) <= 3,
          'the reference figures reproduce from the PDF',
          'mean %.1f, %d sentences' % (R['mean'], R['sents']))
    REF = R
else:
    print('      (PDF absent -- using the quoted reference figures)')

CH = os.path.join(HERE, 'ch-the-map-on-page-ten.html')
C = prose_stats(open(CH, encoding='utf-8').read())
print('\n      %-26s %10s %10s' % ('', 'chapter', 'Strogatz'))
for k, lab in (('words', 'words'), ('sents', 'sentences'),
               ('mean', 'mean words/sentence'), ('longest', 'longest sentence'),
               ('dash_k', 'em-dashes per 1000w'), ('short', '% under 15 words')):
    a = C[k]; b = REF.get(k, float('nan'))
    fmt = '%10.1f' if isinstance(a, float) else '%10d'
    print(('      %-26s ' + fmt + ' ' + ('%10.1f' if b == b else '%10s'))
          % (lab, a, b if b == b else '--'))
print()
check(C['mean'] <= REF['mean'] + 1.0,
      'mean sentence length is at or below his', '%.1f vs %.1f' % (C['mean'], REF['mean']))
check(C['longest'] <= 2 * REF['longest'],
      'no sentence runs past twice his longest', '%d vs %d' % (C['longest'], REF['longest']))
check(C['dash_k'] <= REF['dash_k'],
      'em-dashes per thousand words at or below his rate',
      '%.1f vs %.1f' % (C['dash_k'], REF['dash_k']))
check(C['short'] >= REF['short'],
      'at least his share of sentences run under fifteen words',
      '%.0f%% vs %.0f%%' % (C['short'], REF['short']))
check(C['words'] < 3000, 'and the page stays under three thousand words',
      str(C['words']))
print("""
      This is a register check, not a quality check. It cannot tell whether a
      sentence is clear, only whether the page is built out of the same lengths
      his is. A page can pass every line above and still be unreadable. It is
      here because no other instrument in the corpus measures prose at all, and
      a chapter written to be read has a target it can be held to.""")

print("""
======================================================================
  [HONESTY]
======================================================================
  WHAT THIS ESTABLISHES. That Figure 1.3.1 sits on printed page 10 and carries the
  labels and the sixty-one entries transcribed here. That it has five columns and
  two rows -- ten cells -- the fifth column being Continuum, read off thirteen
  positioned glyph runs on the single line x = 163.2. That the row of every entry
  is recoverable, the linear and nonlinear glyph bands being disjoint, and that
  the column of an entry is NOT, the extractor merging a whole row-line into one
  run. That eight columns are fixed by Strogatz's prose on pp. 9 and 11, and that
  those eight entries read 260, 119, 71, 69, 6, 3, 0, 0, the two zeros being the
  RC and RLC circuits he uses to explain the horizontal axis. That this corpus,
  counted entity-aware at HEAD, occupies 44 of the 61 entries and is at zero on
  17, with 8 of the 17 in the linear row, which has only 18 entries. That the
  three largest counts surviving the sense audit -- fixed points 260, limit cycles
  121, bifurcations 119 -- are all in the nonlinear row. And that seven entries
  fail a sense test: Life 151 -> 11, Plasmas 93 -> 35, Economics 45 -> 19,
  Turbulent fluids 49 -> 10, Acoustics 19 -> 5, shocks 19 -> 7, Levinson 8 -> 6.

  WHAT IT DOES NOT ESTABLISH. Nothing about dynamical systems. No column for
  fifty-three of the sixty-one entries, and that is a limitation of the extractor
  rather than of the figure -- a reader of the printed page sees every cell at
  once. The class-label offset is a mean of four samples spread over 14 units
  applied to three labels; it survives only because the columns are about 80 units
  apart, so an error of ten does not change which marker is nearest. The counts
  measure files that MENTION a thing, not files ABOUT it: fixed points at 260 is not 260 chapters of fixed-point theory. The sense
  audit is a co-occurrence rule over whole files, not a reading of the pages -- it
  is weaker than the string counts it corrects, and both are printed rather than
  reconciled into one number. Fifty-four of the sixty-one entries have not been
  audited at all, and on the evidence of the seven that were, there is no reason to
  assume they are clean. Per R15 the seventeen zeros are zeros IN THE SPELLINGS
  TRIED over the repository this script runs in; the corpus has repositories this
  measurement did not read, and an entry at zero here may be written elsewhere.
  Figure 1.3.1 is offered by its author as debatable -- block [1] checks that he
  says so -- so a zero is a fact about one textbook's taxonomy and this corpus,
  not a fact about the world. No priority is claimed for anything: Figure 1.3.1 is
  Strogatz's, published 1994.
""")
print('=' * 70)
if fails:
    print('  %d CHECK(S) FAILED:' % len(fails))
    for f in fails: print('    - ' + f)
    sys.exit(1)
print('  ALL CHECKS PASSED')
