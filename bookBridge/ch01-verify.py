#!/usr/bin/env python3
"""The Bridge, index + Chapter 1: checks that the numbers the pages print are the numbers the tools produce.
Run from anywhere: python3 bookBridge/ch01-verify.py   (standard library only). Prints SKIP, never PASS, when a tool is missing."""
import os, re, subprocess, sys, math
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
ok = True
def check(name, cond):
    global ok
    print(('PASS ' if cond else 'FAIL ') + name); ok &= bool(cond)
def skip(name, why): print('SKIP ' + name + ' (' + why + ')')
def read(p): return open(p, encoding='utf-8').read()
pages = ['index.html', 'ch01-what-the-bridge-carries.html']
txt = {p: read(os.path.join(here, p)) for p in pages}
plain = {p: re.sub(r'<[^>]+>', ' ', t) for p, t in txt.items()}
ch = plain[pages[1]]

# 1. self-contained pages, links resolve
for p in pages:
    t = txt[p]
    check(p + ': no <link>, <script>, <img>, url()', not re.search(r'<link\b|<script\b|<img\b', t) and 'url(' not in t)
    for h in re.findall(r'href="([^"#]+)"', t):
        if h.startswith('http'): continue
        check(p + ': link ' + h, os.path.exists(os.path.normpath(os.path.join(here, h))))

# 2. the six mu/omega ratios printed in the table, recomputed from the table's own numbers
rows = {'HPA stress': (-0.38, 0.21), 'Neural oscillations': (-0.55, 0.45),
        'Circadian clock': (-0.29, 2 * math.pi / 86400), 'Immune adaptation': (-0.44, 0.18),
        'Plasma reconnection': (-0.42, 0.015), 'Market volatility': (-0.67, 0.28)}
printed = {'HPA stress': '−1.810', 'Neural oscillations': '−1.222', 'Circadian clock': '−3988',
           'Immune adaptation': '−2.444', 'Plasma reconnection': '−28.0', 'Market volatility': '−2.393'}
def fmt(v, name):
    s = ('%.0f' % v) if abs(v) > 1000 else ('%.1f' % v) if name == 'Plasma reconnection' else ('%.3f' % v)
    return s.replace('-', '−')
page_t = re.sub(r'&minus;', '−', txt[pages[1]])
for k, (mu, om) in rows.items():
    r = mu / om
    check('ratio %s: computed %s equals printed %s' % (k, fmt(r, k), printed[k]), fmt(r, k) == printed[k] and printed[k] in page_t)
check('six ratios all different', len({round(mu / om, 3) for mu, om in rows.values()}) == 6)
# control: a wrong expected value must not match
check('control: a wrong ratio is caught', fmt(rows['HPA stress'][0] / rows['HPA stress'][1], 'HPA stress') != '−1.222')

# 3. tools reproduce the printed counts
sim = os.path.join(root, 'tools', 'coherence_similarity.py')
if os.path.exists(sim):
    out = subprocess.run([sys.executable, '-I', sim], capture_output=True, text=True, timeout=60).stdout
    check('similarity tool: 0 of 55 similar pairs', 'similar pairs: 0 of 55 possible' in out and '0 similar pairs out of 55' in ch)
    check('similarity tool: 11 of 11 rows lose more than e^3 per cycle', '11 of 11' in out and 'factor of twenty' in ch)
else: skip('similarity tool', 'tools/coherence_similarity.py missing')
val = os.path.join(root, 'tools', 'bridge', 'validate_bridge_v8_2.py'); yml = os.path.join(root, 'tools', 'bridge', 'coherence_bridge_v8_2.yaml')
if os.path.exists(val) and os.path.exists(yml):
    out = subprocess.run([sys.executable, '-I', val, yml, '--quiet'], capture_output=True, text=True, timeout=60).stdout
    m = re.search(r'Rows:\s*(\d+)\s*\|\s*Passed:\s*(\d+)\s*\|\s*Failed:\s*(\d+)\s*\|\s*Warnings:\s*(\d+)', out)
    got = tuple(map(int, m.groups())) if m else None
    check('validator counts %s equal the page (18, 13, 5, 8)' % (got,), got == (18, 13, 5, 8) and '18 rows, 13 passed, 5 failed, 8 warnings' in ch)
    fails = re.findall(r'\[FAIL\]\s+(\w+)', out)
    check('the five failing rows named on the page are the validator\'s', sorted(fails) == sorted(['neural_microtubule', 'phyllotaxis', 'principia_vol2', 'generative_contact_mechanics', 'biological_transitions_togt']) and all(f in ch for f in fails))
else: skip('validator counts', 'validator or yaml missing')

# 4. files the chapter names exist
for f in ['Orthogenesis/Bridge/CoherenceBridge.lean', 'Orthogenesis/Bifurcation/BifurcationDiscriminator.lean',
          'tools/fold_classifier_controls.py', 'tools/coherence_similarity.py', 'SaturnHexagon.lean']:
    check('named file exists: ' + f, os.path.exists(os.path.join(root, f)))
sat = os.path.join(root, 'SaturnHexagon.lean')
if os.path.exists(sat):
    check('SaturnHexagon.lean states its vectors on Fin 6 (the page says six sectors by construction)', 'Fin 6' in read(sat))

# 5. honesty gates the pages must keep
check('chapter keeps its OPEN box (author\u2019s call)', 'class="box open"' in txt[pages[1]] and 'the author\u2019s call' in ch.replace('&rsquo;','\u2019'))
check('index states the book is unnumbered', 'unnumbered' in plain[pages[0]])
check('index marks unread pages as title only', plain[pages[0]].count('title only') >= 3)
check('chapter says the fold-test run is not yet counted as verified', 'does not count that run as verified' in ch)
check('no commit attribution trailers in the pages', 'Co-Authored-By' not in txt[pages[0]] + txt[pages[1]])
sys.exit(0 if ok else 1)
