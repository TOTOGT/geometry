#!/usr/bin/env python3
"""
gold_standard.py — a self-assessment stamp against the nine tenets of Gold Standard
Science, Executive Order 14303 (23 May 2025, 90 FR 22601), Sec. 3(a):
  (i) reproducible; (ii) transparent; (iii) communicative of error and uncertainty;
  (iv) collaborative and interdisciplinary; (v) skeptical of its findings and
  assumptions; (vi) structured for falsifiability of hypotheses; (vii) subject to
  unbiased peer review; (viii) accepting of negative results as positive outcomes;
  (ix) without conflicts of interest.
Set 2026-09-27 by Pablo.

THIS IS NOT A CERTIFICATION. No agency has reviewed these pages. Each tenet is scored
from something observable on the page or beside it, the rule is printed in the stamp,
and a tenet the page cannot show is marked as not shown. (vii) is never claimed:
nothing here has been through independent peer review. (ix) is a disclosure, not a
claim of absence.

    python3 tools/gold_standard.py            check: exit 1 if any stamp is stale
    python3 tools/gold_standard.py --write    (re)write every stamp, idempotent
    python3 tools/gold_standard.py --show P   print P's scores and why
"""
import html, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import subject_tags as ST, run_yourself as RY

ROOT = ST.ROOT
BEGIN, END = '<!--po-gss-->', '<!--/po-gss-->'
BLOCK = re.compile(re.escape(BEGIN) + r'.*?' + re.escape(END) + r'\n?', re.S)
EO = 'https://www.federalregister.gov/documents/2025/05/29/2025-09802/restoring-gold-standard-science'
# 2026-09-27: widened only to phrasings that report a claim this corpus withdrew or refuted
# ("v4 withdraws the prediction", "WP-24 refuted one of its own bridges", "the conjecture is
# refuted"). A bare "failed" or "refuted" is NOT enough: it matched "Escher failed at school",
# "the dam failed" and "Not refuted". Every page this changed is listed in docs/audit-log.md.
NEG = re.compile(r'withdrawn|withdraws? the|withdrew (?:that|the|its|this)|retract|thesis failed|null result|0 matches|zero intersections|does not survive|was false|is false|\brefuted (?:one|an|a|the|its|in)\b|conjecture is refuted', re.I)

# (vii) and (ix) are earned outside the books. docs/peer-review.tsv lists a page only once an
# independent journal has PUBLISHED it: page<TAB>venue<TAB>DOI<TAB>COI statement as printed.
# A submission, a preprint or an acceptance letter does not count.
def peer_ledger():
    path = os.path.join(ROOT, 'docs', 'peer-review.tsv')
    out = {}
    if os.path.exists(path):
        for line in open(path, encoding='utf-8'):
            f = line.rstrip('\n').split('\t')
            if len(f) >= 4 and f[0] and not f[0].startswith('#') and f[2].startswith('10.'):
                out[f[0]] = dict(venue=f[1], doi=f[2], coi=f[3])
    return out
PEER = peer_ledger()

def score(rel, src):
    body = BLOCK.sub('', src)
    files = RY.files_for(rel, src)
    scripts = [open(os.path.join(ROOT, f), encoding='utf-8', errors='replace').read() for f in files]
    code = '\n'.join(scripts)
    other_books = len(set(re.findall(r'Book (\w+) &middot;|Book (\w+) ·', body[body.find('<!--po-related-->'):] if '<!--po-related-->' in body else ''))) > 0
    # 2026-09-27: a page that already links another volume in its own text gets no generated
    # box (crossref only suggests pages not yet linked), and scored "no cross-volume links".
    # Direct links into another top-level folder count too.
    own = rel.split('/')[0] if '/' in rel else ''
    prose = re.sub(r'<!--po-(run|gss|related|subject)-->.*?<!--/po-\1-->', '', body, flags=re.S)
    prose = prose[prose.find('<div class="wrap">'):] if '<div class="wrap">' in prose else prose
    for h in re.findall(r'href="([^"#]+\.html)', prose):
        if h.startswith(('http', 'mailto')):
            continue
        tgt = os.path.normpath(os.path.join(os.path.dirname(rel), h)).split(os.sep)
        if len(tgt) > 1 and tgt[0] not in ('..', own) or (own and len(tgt) == 1):
            other_books = True
            break
    refs = bool(re.search(r'References|Sources|<ol class="refs"|Primary source|Held text', body))
    t = [
      ('reproducible', bool(files), 'a script or Lean file beside the page re-derives its numbers' if files else 'no script or Lean file'),
      ('transparent', bool(files) and refs, 'code downloadable and sources named with addresses' if (files and refs) else 'code or sourced references missing'),
      ('error and uncertainty', bool(re.search(r't-model|t-open|\[HONESTY\]|±|uncertain', body + code)), 'MODEL / OPEN tags or an [HONESTY] block'),
      ('collaborative, interdisciplinary', other_books, 'cross-linked to other volumes' if other_books else 'no cross-volume links'),
      ('skeptical', bool(re.search(r't-open|OPEN\]|not claim|will not claim|What (this|the) .{0,30}(not|does not)', body + code)), 'states what it does not claim, or leaves items open'),
      ('falsifiable', bool(re.search(r'\bFAIL\b', code)), 'its script can print FAIL' if re.search(r'\bFAIL\b', code) else 'no check that can fail'),
      ('unbiased peer review', rel in PEER,
       f"published after peer review: {PEER[rel]['venue']}, doi:{PEER[rel]['doi']}" if rel in PEER else 'not independently peer reviewed'),
      ('negative results', bool(NEG.search(body)), 'reports a withdrawn or failed result' if NEG.search(body) else 'no negative result reported on this page'),
      ('conflicts of interest', (True if rel in PEER and PEER[rel]['coi'].lower().startswith('none') else None),
       f"journal statement: {PEER[rel]['coi']}" if rel in PEER else 'disclosed: author-published through G6 LLC, the author\'s company'),
    ]
    return t

def stamp(rel, src):
    t = score(rel, src)
    n = sum(1 for _, ok, _ in t if ok)
    rows = ''.join(
        f'<li style="margin:.1rem 0"><span style="display:inline-block;width:1.2em">{"&#10003;" if ok else ("&#9675;" if ok is None else "&#10007;")}</span>'
        f'({"i ii iii iv v vi vii viii ix".split()[k]}) {html.escape(name)} <span style="opacity:.6">&mdash; {html.escape(why)}</span></li>'
        for k, (name, ok, why) in enumerate(t))
    return (f'{BEGIN}<aside class="po-gss" style="max-width:860px;margin:1.2rem auto 1rem;padding:.8rem 1.1rem;'
            f'border:1px solid rgba(128,128,128,.35);border-left:3px solid rgba(40,80,150,.85);border-radius:0 6px 6px 0;'
            f'background:rgba(40,80,150,.05);font-family:ui-monospace,Menlo,monospace;font-size:.78rem;line-height:1.55">'
            f'<details><summary style="cursor:pointer;letter-spacing:.08em">'
            f'<b>Gold Standard Science &middot; {n} of 9 tenets shown</b> &middot; self-assessed against '
            f'<a href="{EO}" style="color:inherit">EO 14303 &sect;3(a)</a> &mdash; not a federal certification</summary>'
            f'<ul style="list-style:none;margin:.5rem 0 .3rem;padding:0">{rows}</ul>'
            f'<div style="opacity:.75">Scored by <code>tools/gold_standard.py</code> from what is observable on this page and beside it. '
            f'&#10003; shown &middot; &#10007; not shown &middot; &#9675; disclosure. No agency has reviewed this page. '
            f'<a href="/geometry/gold-standard.html" style="color:inherit">What the order says and why this series follows it</a>.</div>'
            f'</details></aside>{END}\n')

def place(src, b):
    src = BLOCK.sub('', src)
    for marker in ('<!--po-run-->', '<!--po-related-->', '<footer', '</body>'):
        i = src.rfind(marker)
        if i >= 0: return src[:i] + b + src[i:]
    return src + b

TENETS = [
 ('i', 'Reproducible', 'Someone else can re-derive the numbers.', 'A verify script or Lean file sits beside the page.'),
 ('ii', 'Transparent', 'Methods, code and sources are open.', 'The code is there and the sources are named with addresses.'),
 ('iii', 'Communicative of error and uncertainty', 'The page says how sure it is.', 'MODEL or OPEN tags, an [HONESTY] block, or stated uncertainty.'),
 ('iv', 'Collaborative and interdisciplinary', 'The work is connected to other fields.', 'The page links into another volume.'),
 ('v', 'Skeptical of its findings and assumptions', 'The page says what it does not claim.', 'A "what this does not claim" passage, or items left open.'),
 ('vi', 'Structured for falsifiability of hypotheses', 'A result could come out wrong.', 'Its script contains a check that can print FAIL.'),
 ('vii', 'Subject to unbiased peer review', 'Independent experts reviewed it.', 'Only when a journal has published it (docs/peer-review.tsv). Never self-claimed.'),
 ('viii', 'Accepting of negative results as positive outcomes', 'Failed or withdrawn results are reported.', 'The page reports a withdrawn, refuted or failed result.'),
 ('ix', 'Without conflicts of interest', 'Interests are declared.', 'A disclosure: these books are published by G6 LLC, the author\'s company. Scored only from a journal\'s statement.'),
]

def write_index(results, hist):
    import datetime
    esc = html.escape
    def title(src, rel):
        m = re.search(r'<title[^>]*>(.*?)</title>', src, re.S | re.I)
        t = html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip() if m else rel
        return re.sub(r'\s+', ' ', t)
    groups = {}
    for rel, src, sc, n in results:
        g = rel.split('/')[0] if '/' in rel else 'root'
        groups.setdefault(g, []).append((rel, src, sc, n))
    def gkey(g):
        m = re.match(r'book(\d+)$', g)
        return (0, int(m.group(1))) if m else ((1, 0) if g == 'root' else (2, g))
    label = lambda g: ('Book ' + g[4:]) if re.match(r'book\d+$', g) else ('Book IX · Omega Point' if g == 'omega' else 'Root chapters (mostly Book 3)')
    total = len(results)
    hist_cells = ''.join(f'<td>{hist.get(k, 0)}</td>' for k in range(10))
    rows_html = []
    for g in sorted(groups, key=gkey):
        items = sorted(groups[g], key=lambda x: (-x[3], x[0]))
        avg = sum(x[3] for x in items) / len(items)
        rows_html.append(f'<h3 id="{esc(g)}">{esc(label(g))} <span class="dim">&middot; {len(items)} pages &middot; mean {avg:.1f} of 9</span></h3><div class="tw"><table><tbody>')
        for rel, src, sc, n in items:
            marks = ''.join(('<span class="ok">&#10003;</span>' if ok else ('<span class="dc">&#9675;</span>' if ok is None else '<span class="no">&#10007;</span>')) for _, ok, _ in sc)
            rows_html.append(f'<tr><td class="n">{n}</td><td class="m">{marks}</td><td><a href="{esc(rel)}">{esc(title(src, rel))}</a> <span class="dim mono">{esc(rel)}</span></td></tr>')
        rows_html.append('</tbody></table></div>')
    tenet_rows = ''.join(f'<tr><td class="mono">({k})</td><td><b>{esc(a)}</b><br><span class="dim">{esc(b)}</span></td><td>{esc(c)}</td></tr>' for k, a, b, c in TENETS)
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Gold Standard Science · Principia Orthogona</title>
<meta name="description" content="What Executive Order 14303 says Gold Standard Science is, why this series scores itself against its nine tenets, and every chapter's current self-assessment.">
<style>
:root {{ --bg:#fbfaf7; --fg:#1d1d1f; --dim:#6b6a66; --line:#d9d6cf; --accent:#28508f; --ok:#1f7a3a; --no:#a33a2a; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#141416; --fg:#e8e6e1; --dim:#9a988f; --line:#33322f; --accent:#8fb0e8; --ok:#6cc68a; --no:#e58b7c; color-scheme:dark; }} }}
body {{ background:var(--bg); color:var(--fg); font:16px/1.6 Georgia,'Times New Roman',serif; margin:0; padding:2rem 1rem 4rem; }}
.wrap {{ max-width:860px; margin:0 auto; }}
h1 {{ font-size:2rem; line-height:1.2; margin:.2rem 0 .6rem; }} h2 {{ margin-top:2.4rem; font-size:1.35rem; border-bottom:1px solid var(--line); padding-bottom:.3rem; }}
h3 {{ font-size:1.05rem; margin:1.8rem 0 .4rem; }}
a {{ color:var(--accent); }} .dim {{ color:var(--dim); }} .mono, .m, .n {{ font-family:ui-monospace,Menlo,monospace; }}
.kicker {{ font:600 .75rem ui-monospace,Menlo,monospace; letter-spacing:.14em; text-transform:uppercase; color:var(--dim); }}
.tw {{ overflow-x:auto; }} table {{ border-collapse:collapse; width:100%; font-size:.92rem; }}
td, th {{ border-bottom:1px solid var(--line); padding:.35rem .5rem; vertical-align:top; text-align:left; }}
td.n {{ width:2rem; text-align:right; }} td.m {{ white-space:nowrap; letter-spacing:.06em; }}
.ok {{ color:var(--ok); }} .no {{ color:var(--no); }} .dc {{ color:var(--dim); }}
.note {{ border-left:3px solid var(--accent); padding:.6rem 1rem; background:rgba(128,128,128,.07); }}
.hist td, .hist th {{ text-align:center; }}
</style>
</head>
<body><div class="wrap">
<div class="kicker">Principia Orthogona &middot; generated by tools/gold_standard.py &middot; {datetime.date.today().isoformat()}</div>
<h1>Gold Standard Science</h1>
<p>Every chapter in this series carries a small box that scores it against nine tenets. This page says where the tenets come from, why the series uses them, how each one is scored, and where every chapter stands today.</p>

<h2>What the order says</h2>
<p>Executive Order 14303, <a href="{EO}"><i>Restoring Gold Standard Science</i></a>, was signed on 23 May 2025 and published at 90 FR 22601. Section 3(a) defines Gold Standard Science as science conducted in a manner that is (i) reproducible; (ii) transparent; (iii) communicative of error and uncertainty; (iv) collaborative and interdisciplinary; (v) skeptical of its findings and assumptions; (vi) structured for falsifiability of hypotheses; (vii) subject to unbiased peer review; (viii) accepting of negative results as positive outcomes; and (ix) without conflicts of interest. The order directs federal agencies; it does not bind private authors or publishers.</p>

<h2>Why this series follows it</h2>
<p>Nothing requires these books to meet the order. The author adopted its nine tenets on 27 September 2026 as a public bar that anyone can check a page against, set by someone other than the author. The series is written with machine assistance and publishes its own corrections; a bar fixed outside the series keeps the question "how good is this page?" from being answered by the series' own enthusiasm. The rule is that a reader can run the page, and the page says how well it meets the bar.</p>
<div class="note"><b>This is a self-assessment, not a certification.</b> No agency has reviewed these pages. Each tenet is scored from something a reader can see on the page or beside it, by a script whose rules are printed below. Tenet (vii) is never self-claimed: it counts only when an independent journal has published the work. Tenet (ix) is shown as a disclosure. So the highest score a page can reach without journal publication is 7 of 9.</div>

<h2>How each tenet is scored</h2>
<div class="tw"><table><thead><tr><th></th><th>Tenet</th><th>Counted as shown when&hellip;</th></tr></thead><tbody>{tenet_rows}</tbody></table></div>
<p class="dim">These are observable signs, not proof of the quality behind them. A tag or the word FAIL in a script can be present without the substance it stands for; the series' <a href="docs/failure-checklist.md">failure checklist</a> is the companion that asks whether the substance is there.</p>

<h2>What is scored, and what is not</h2>
<p>Scored: every chapter in a numbered book folder, Book IX (<span class="mono">omega/</span>), and root chapters tagged with their book &mdash; {total} pages today. Not scored, because they are not chapters that make claims: navigation hubs and indexes, the course pages in <a href="courses/">courses/</a>, the soundworks and wellness pages in <a href="soundworks/">soundworks/</a>, portfolio and pitch pages in <a href="portfolio/">portfolio/</a>, redirects, and the <span class="mono">_archive/</span> copies. The full list of files is in the <a href="master-index.html">master index</a>.</p>
<div class="tw"><table class="hist"><thead><tr><th>Tenets shown</th>{''.join(f'<th>{k}</th>' for k in range(10))}</tr></thead><tbody><tr><th>Pages</th>{hist_cells}</tr></tbody></table></div>

<h2>Every scored chapter</h2>
<p class="dim">Columns: tenets shown, then the nine marks in order (i)&ndash;(ix): <span class="ok">&#10003;</span> shown, <span class="no">&#10007;</span> not shown, <span class="dc">&#9675;</span> disclosure.</p>
{''.join(rows_html)}
<p class="dim" style="margin-top:2rem">Generated. Do not hand-edit: run <span class="mono">python3 tools/gold_standard.py --write</span>.</p>
</div></body></html>
"""
    open(os.path.join(ROOT, 'gold-standard.html'), 'w', encoding='utf-8').write(page)

def main():
    if '--show' in sys.argv:
        r = sys.argv[sys.argv.index('--show') + 1]
        for name, ok, why in score(r, open(os.path.join(ROOT, r), encoding='utf-8').read()): print(ok, name, '-', why)
        return 0
    write = '--write' in sys.argv; stale = changed = 0; hist = {}; results = []
    for rel in ST.chapters():
        if ST.rows().get(rel, ('',))[0] == 'SERIES APPARATUS': continue
        path = os.path.join(ROOT, rel); src = open(path, encoding='utf-8', errors='replace').read()
        new = place(src, stamp(rel, src))
        sc = score(rel, src); n = sum(1 for _, ok, _ in sc if ok); hist[n] = hist.get(n, 0) + 1
        results.append((rel, src, sc, n))
        if new != src:
            if write: open(path, 'w', encoding='utf-8').write(new); changed += 1
            else: stale += 1
    if write:
        write_index(results, hist)
    print('tenets shown -> pages:', dict(sorted(hist.items())), f'; {changed} written' if write else f'; {stale} stale')
    return 1 if stale and not write else 0

if __name__ == '__main__':
    sys.exit(main())
