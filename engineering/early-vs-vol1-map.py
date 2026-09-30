#!/usr/bin/env python3
"""Map each Volume I statement (book1/vol1-mathematics.html, the current page) to its counterpart in the early
master_book TeX, and report wording differences and Volume I's own status label.
R24: runs before any sentence about withdrawn/corrected claims. R9: nothing in either file is changed."""
import os, re, sys, html, difflib, csv
D = os.environ.get('EARLY_DIR', os.path.expanduser('~/Downloads'))
TEX = sys.argv[1] if len(sys.argv) > 1 else 'master_book_FINAL_v2.tex'
OUT = sys.argv[2] if len(sys.argv) > 2 else None
def plain(x):
    x = html.unescape(re.sub(r'<[^>]+>', ' ', x))
    x = re.sub(r'\\(mathcal|mathrm|text|emph|textbf)\{([^}]*)\}', r'\2', x)
    x = re.sub(r'\\[()\[\]]|\$|\\[a-zA-Z]+|[{}\\]', ' ', x)
    return re.sub(r'\s+', ' ', x).strip().lower()
def words(x): return re.findall(r"[a-z0-9]+", plain(x))
def jacc(a, b):
    a, b = set(a), set(b)
    return len(a & b) / max(1, len(a | b))
h = open('book1/vol1-mathematics.html', errors='ignore').read()
vol = []
for kind, b in re.findall(r'<div class="env-box (theorem|conjecture)">(.*?)</div>\s*(?=<div class="env-box|<div id=|<!--|</div>)', h, re.S):
    lab = re.search(r'env-label">(.*?)</div>', b, re.S); lab = plain(lab.group(1)) if lab else ''
    body = re.sub(r'<div class="env-label">.*?</div>', '', b, flags=re.S)
    paras = re.findall(r'<p[^>]*>(.*?)</p>', body, re.S)
    stmt = paras[0] if paras else body
    status = re.findall(r'class="tag t-[a-z]+">([^<]*)<', b)
    status += re.findall(r'\[(OPEN OBLIGATION[^\]]*|ARGUED[^\]]*)\]', html.unescape(lab and re.search(r'env-label">(.*?)</div>', b, re.S).group(1)))
    if re.search(r'PROVED Theorem', lab, re.I): status.append('PROVED (label prefix)')
    corr = re.search(r'Corrected (\d{4}-\d\d-\d\d)', html.unescape(b))
    vol.append(dict(label=lab, stmt=stmt, status=';'.join(status), corrected=corr.group(1) if corr else '', extra=len(paras) > 1))
t = open(os.path.join(D, TEX), errors='ignore').read()
stm = []
for m in re.finditer(r'\\begin\{(theorem|proposition|lemma|corollary|conjecture)\}(\[[^\]]*\])?(.*?)\\end\{\1\}', t, re.S):
    stm.append(dict(kind=m.group(1), title=(m.group(2) or '').strip('[]'), body=m.group(3), line=t.count('\n', 0, m.start()) + 1))
rows = []
print('%d Volume I statements vs %d statements in %s' % (len(vol), len(stm), TEX))
for v in vol:
    title = re.sub(r'^(proved\s+)?(theorem|conjecture)\s+[\w.]+\s*·?\s*', '', v['label'])
    title = re.sub(r'\[.*?\]', '', title).strip()
    tw = words(title); vw = words(v['stmt'])
    best = None
    for s in stm:
        sc = 0.5 * jacc(tw, words(s['title'])) + 0.5 * jacc(vw, words(s['body']))
        if best is None or sc > best[0]: best = (sc, s)
    sc, s = best
    if sc < 0.25:
        rows.append((v['label'][:60], v['status'] or '-', v['corrected'], 'NO-COUNTERPART', '', 0, ''))
        print('  %-58s status=%-28s NO COUNTERPART in early file (best score %.2f)' % (v['label'][:58], v['status'] or '-', sc)); continue
    a, b = words(s['body']), vw
    sm = difflib.SequenceMatcher(None, a, b)
    diff = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op != 'equal': diff.append('%s:[%s]->[%s]' % (op[0], ' '.join(a[i1:i2])[:50], ' '.join(b[j1:j2])[:50]))
    same = sm.ratio() > 0.97
    rows.append((v['label'][:60], v['status'] or '-', v['corrected'], 'SAME-WORDING' if same else 'DIFFERS', 'L%d %s' % (s['line'], s['title'][:30]), round(sm.ratio(), 2), ' | '.join(diff)[:300]))
    print('  %-58s status=%-28s %s (early L%d, ratio %.2f)%s' % (v['label'][:58], v['status'] or '-', 'same' if same else 'DIFFERS', s['line'], sm.ratio(), ('  corrected ' + v['corrected']) if v['corrected'] else ''))
    if not same: print('      ', ' | '.join(diff)[:260])
if OUT:
    with open(OUT, 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t'); w.writerow(['volume1_label', 'volume1_status', 'corrected', 'early_file', 'early_location', 'ratio', 'wording_diff']); w.writerows(rows)
