#!/usr/bin/env python3
"""Audit of the early (model-3 era) Book 2 files in ~/Downloads.
R24: this runs before any sentence about the files is written into the claims register.
Facts marked CITED were read from the publisher / Crossref records on 2026-09-30 (see docs/early-files-audit.md);
everything else is computed from the files themselves. Nothing here decides which figure is canonical (R9)."""
import os, re, sys, collections
D = os.environ.get('EARLY_DIR', os.path.expanduser('~/Downloads'))
fails = []
def check(ok, msg):
    print('    %s  %s' % ('PASS' if ok else 'FLAG', msg))
    if not ok: fails.append(msg)
def head(n, t): print('\n[%d]  %s\n%s' % (n, t, '=' * 72))
def rd(f):
    p = os.path.join(D, f)
    return open(p, errors='ignore').read() if os.path.exists(p) else None

head(1, 'tower height: three figures in the early files, one of them exactly 66 x 228.6 m')
print('    chapter 09 mars.tex: 15,087.6 m / 39,788 m;  main.tex, main-2.tex: 15,080 (text) or 39,808 m;  stated apothem 229 m (main.tex line ~1699)')
check(abs(66 * 228.6 - 15087.6) < 1e-9, '66 x 228.6 = %.1f m (the chapter 09 figure)' % (66 * 228.6))
check(abs(228.6 / 0.3048 - 750) < 1e-9, '228.6 m = 750 ft exactly: the 15,087.6 figure looks like a 750 ft apothem x 66')
g = 3.72 / 9.81
check(abs(15087.6 / g - 39788) < 1, '15,087.6 / (3.72/9.81) = %.0f m: chapter 09 is internally consistent with the exact g ratio' % (15087.6 / g))
check(abs(15087.6 / 0.379 - 39808) < 1, '15,087.6 / 0.379 = %.0f m: the 39,808 in main.tex comes from the rounded 0.379 and 15,087.6, not from 15,080' % (15087.6 / 0.379))
check(229 * 66 == 15114, '229 x 66 = %d (the stated 229 m apothem gives this, not 15,080)' % (229 * 66))
check(round(15080 / 66, 2) not in (228.6, 229.0), '15,080 / 66 = %.2f m: matches neither 228.6 nor 229, so 15,080 is an unsupported rounding' % (15080 / 66))
print('    OPEN (author): which apothem is canonical, 228.6 m (-> 15,087.6 / 39,788) or 229 m (-> 15,114 / 39,900, what main-2-fixed*.tex now say).')

head(2, 'bibliography of main.tex (entries kept as a to-do block at the end of the file)')
s = rd('main.tex')
if s is None:
    print('    main.tex not found in', D)
else:
    m = re.search(r'@article\{Lai2026,(.*?)\n\}', s, re.S)
    bib_auth = re.search(r'author\s*=\s*\{(.*?)\}', m.group(1), re.S).group(1)
    bib_first = [a.strip().split(',')[1].strip() for a in bib_auth.split(' and ')]
    real_first = ['Shoulong', 'Xigui', 'Jiuyang', 'Shijie', 'Ying', 'Longbin', 'Jinhao', 'Zhuangfei', 'Qiuhan', 'Jian', 'Shaobo', 'Chongxin']  # CITED: nature.com/articles/s41586-026-10212-4
    same = sum(1 for a, b in zip(bib_first, real_first) if a == b)
    check(len(bib_first) == len(real_first), 'Lai2026: %d authors listed, %d on the Nature page' % (len(bib_first), len(real_first)))
    check(same == len(real_first), 'Lai2026: %d of %d given names match the Nature page (surnames match, given names differ: %s ...)' % (same, len(real_first), ', '.join(bib_first[:4])))
    check('Bulk hexagonal diamond' in m.group(1), 'Lai2026 title "Bulk hexagonal diamond" matches the Nature page (real paper, DOI resolves)')
    print('    CITED: Dorkenwald 2024 Nature 634:124-138 (Crossref ok); Pospisil 2024 Nature 634:201-209 (Crossref ok, but main.tex labels the key Dorkenwald2024b);')
    print('           Demirtas-Kim-McAllister-Moritz PRL 124(21) 211603 (2020) (Crossref ok); Gukov-Vafa-Witten NPB 584 (2000) 69 (ADS/ScienceDirect listing; Crossref fetch rate-limited, not read).')
    check('Dorkenwald2024b' not in s or 'Pospisil' not in s.split('Dorkenwald2024b')[1][:200], 'key Dorkenwald2024b holds a Pospisil-first-author paper (label mismatch)')

head(3, 'the 114 GPa hardness and which paper it belongs to')
for f in ['main-2-fixed.tex', 'main-2-fixed-2.tex']:
    t = rd(f)
    if t is None: continue
    n = len(re.findall(r'Yang et al\.?,? \\emph\{Nature\} 2026', t))
    check(n == 0, '%s: "Yang et al., Nature 2026" appears %d times; Yang et al. is Nature 644:370-375 (2025), the 2026 paper is Lai et al.  (CITED)' % (f, n))
print('    CITED: the Lai (2026) page says only "slightly higher hardness than CD"; the Yang (2025) page says "only slightly higher than cubic diamond" and gives no number in the accessible text.')
print('    => 114 GPa is not found in either paper as read. UNCONFIRMED; it was asserted in model-era text and propagated.')

head(4, 'master_book / completePrincipia bibliographies')
for f in ['master_book_FINAL_v2.tex', 'completePrincipia.tex']:
    t = rd(f)
    if t is None: continue
    keys = re.findall(r'\\bibitem(?:\[[^\]]*\])?\{([^}]*)\}', t)
    dup = {k: c for k, c in collections.Counter(keys).items() if c > 1}
    check(not dup, '%s: %d bibitems, %d keys defined more than once (%s)' % (f, len(keys), len(dup), ', '.join('%s x%d' % kv for kv in list(dup.items())[:5])))
    z = re.findall(r'zenodo[.:]?\s*\\?texttt\{?([^}]*)\}?', t)
    p = re.findall(r'\\bibitem\{Paper1\}.*?\\bibitem', t, re.S)
    kinds = set('submitted' if 'submitted' in x else 'chapter' for x in p)
    check(len(kinds) <= 1, '%s: Paper1 is described as %s across its bibliographies' % (f, ' and '.join(sorted(kinds))))
    zs = re.findall(r'10\.5281/zenodo\.\d+', t)
    print('    Zenodo DOIs in %s: %s' % (f, sorted(set(zs))))
print('\n' + ('FLAGS: %d (each is a finding, not a script fault)' % len(fails) if fails else 'all checks passed'))
sys.exit(0)
