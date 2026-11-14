#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""readcheck.py -- the deep-read step as a machine: does the Lean statement say what the sentence says?

Why. "Compiles" is not "proves what it says". Three times in this corpus a theorem type-checked and
established something disconnected from its name (`∃ shape, True`; `1 = 1`; a Reeb-orbit theorem about a
scalar potential). declaration_scan.py asks whether a named declaration EXISTS; this asks the next question:
read the statement next to the sentence that cites it. A script cannot decide that. It can (1) find every
sentence that cites a declaration, (2) put the sentence and the declaration's ACTUAL statement side by side,
(3) flag the shapes that have failed before, and (4) hand the same pairs, blind, to a second reader and
measure agreement. The verdict is a reading, by two readers; the flags are only leads.

    python3 tools/readcheck.py selftest                       controls: each seeded defect must be flagged, the sound one must not
    python3 tools/readcheck.py extract PAGE [PAGE...] --out DIR     claim units -> DIR/units.tsv, DIR/worklist.tsv (flags, for the first reader)
    python3 tools/readcheck.py sheet DIR                      DIR/blind-statements.tsv, DIR/blind-numbers.tsv, DIR/PROMPT.txt (no flags, no labels)
    python3 tools/readcheck.py agree DIR RETURNED.tsv         compare the second reader's labels with DIR/labels-claude.tsv

Labels, statement sheet:  M  the statement establishes the sentence as written
                          W  weaker or narrower than the sentence (say what is missing)
                          U  about a different object than the sentence names (say which)
                          V  vacuous or trivially true (give the trivial witness)
                          N  cannot tell, or the declaration is not shown
Labels, number sheet:     R  recomputed independently, matches to the stated precision
                          X  recomputed, does NOT match (give your value)
                          C  cannot recompute from what is stated
Standard library only. Flags are heuristics: a flag is a reason to read, never a verdict.
"""
import hashlib, csv, html, os, random, re, subprocess, sys, glob
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
SEED = 20261114
DECL = re.compile(r'^[ \t]*(?:@\[[^\]\n]*\][ \t]*)?(?:(?:private|protected|noncomputable|partial|unsafe)[ \t]+)*'
                  r'(theorem|lemma|def|axiom|abbrev|structure|inductive|class|instance)[ \t]+([^\s:({\[⟨]+)', re.M)

def lean_files():
    tracked = subprocess.run(['git', '-C', ROOT, 'ls-files', '*.lean'], capture_output=True, text=True).stdout.split('\n')
    out = [os.path.join(ROOT, p) for p in tracked if p]
    axle = os.path.expanduser('~/Desktop/AXLE')
    if os.path.isdir(axle):
        for dp, dn, fn in os.walk(axle):
            if '.lake' in dp or '/.git' in dp: continue
            out += [os.path.join(dp, f) for f in fn if f.endswith('.lean')]
    return sorted(set(out))

def split_statement(body):
    """statement = text up to the first top-level ':=' / 'where' / pattern '|' ; proof head = the next 200 chars"""
    depth = 0; i = 0; n = len(body)
    while i < n:
        c = body[i]
        if c in '([{⟨': depth += 1
        elif c in ')]}⟩': depth -= 1
        elif depth <= 0 and body.startswith(':=', i): return body[:i].strip(), body[i + 2:i + 202].strip(), body[i + 2:]
        elif depth <= 0 and body.startswith('\nwhere', i): return body[:i].strip(), body[i:i + 200].strip(), body[i:]
        i += 1
    return body[:1200].strip(), '', ''

def axiom_reports():
    rep = {}
    for p in sorted(glob.glob(os.path.join(ROOT, 'tools', 'verify-audit', '*', '*.axioms.txt'))):
        for line in open(p, encoding='utf-8', errors='replace'):
            m = re.match(r"'([^']+)' depends on axioms: \[(.*)\]", line.strip())
            if m: rep[m.group(1).split('.')[-1]] = ('sorryAx' in m.group(2))
            elif 'does not depend on any axioms' in line:
                m2 = re.match(r"'([^']+)'", line.strip())
                if m2: rep[m2.group(1).split('.')[-1]] = False
    return rep

def conclusion(st):
    """the declared type: text after the first colon at bracket depth 0 (a colon inside (1 : Nat) does not count)"""
    depth = 0
    for i, c in enumerate(st):
        if c in '([{⟨': depth += 1
        elif c in ')]}⟩': depth -= 1
        elif c == ':' and depth == 0 and not st.startswith(':=', i): return st[i + 1:]
    return st

AUTO = re.compile(r'\b(omega|simp|simp_all|linarith|nlinarith|aesop|assumption|positivity|decide|tauto|norm_num|exact\?|polyrith)\b')

def flags(d):
    """heuristic leads for the first reader; each reason is a failure that has actually happened"""
    f = []; st = d['stmt']; concl = conclusion(st)
    body = d['body']
    if d['kind'] in ('def', 'abbrev', 'structure', 'inductive', 'class', 'instance'): f.append('NOT_A_THEOREM(%s)' % d['kind'])
    if d['kind'] == 'axiom': f.append('AXIOM')
    if re.search(r'∃[^,]*,\s*True\b', st) or re.fullmatch(r'\s*True\s*', concl) or re.search(r':\s*True\b', st): f.append('CONCLUSION_TRUE')
    c2 = re.sub(r'\((\S+)\s*:\s*[^()]*\)', r'\1', concl.strip())          # drop type ascriptions: (1 : Nat) -> 1
    if '=' in c2 and '≠' not in c2 and '≤' not in c2 and '≥' not in c2:
        lhs, rhs = c2.rsplit('=', 1)
        if lhs.strip() and lhs.strip() == rhs.strip(): f.append('REFLEXIVE_CONCLUSION')
    if re.match(r'\s*(by\s+)?(rfl|trivial|decide|simp|norm_num)\b', d['head']) and d['kind'] in ('theorem', 'lemma'): f.append('ONE_TACTIC_PROOF')
    if re.search(r'\bsorry\b', body): f.append('SORRY')
    if re.search(r'⟨\s*0\s*,', body[:400]) and '∃' in st: f.append('ZERO_WITNESS')
    if '∀' in st and '→' not in st and re.search(r'\b(n|k|m)\s*:\s*(ℕ|Nat)', st) and re.search(r'∃', st): f.append('NO_POSITIVITY_GUARD')
    hyps = re.findall(r'\((h\w*)\s*:', st)
    if hyps and body and not AUTO.search(body) and all(not re.search(r'\b%s\b' % re.escape(h), body) for h in hyps): f.append('HYPOTHESES_UNUSED')
    if d.get('file_has_axiom'): f.append('FILE_DECLARES_AXIOM')
    return f

def page_text(path):
    s = open(path, encoding='utf-8', errors='replace').read()
    s = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', s)
    s = re.sub(r'(?is)<br\s*/?>|</p>|</li>|</h\d>|</div>|</tr>', '. ', s)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'(?s)<[^>]+>', ' ', s)))

TRIG = re.compile(r'\b(proved|proves|proven|machine-checked|kernel-checked|verified|theorem|lemma|proposition|corollary|converges?|contraction|by (?:mathematical )?necessity|without sorry)\b', re.I)
NUM = re.compile(r'(?:=|≈|\\approx|~)\s*-?\d+\.\d+|\b\d+(?:\.\d+)?\s*(?:%|km|m/s|GPa|MPa|Hz|days?)\b')

def kappa(a, b):
    n = len(a); po = sum(x == y for x, y in zip(a, b)) / n; ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n); return po, (1.0 if pe == 1 else (po - pe) / (1 - pe))

import hashlib, json
def sha(*parts): return hashlib.sha1('\x1f'.join(parts).encode('utf-8')).hexdigest()
def norm(s): return re.sub(r'\s+', ' ', s).strip()
def repo_rev(path):
    d = os.path.dirname(path)
    r = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()
    if not r: return 'no-repo'
    v = subprocess.run(['git', '-C', r, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    return '%s@%s' % (os.path.basename(r), v[:10])

_PROV = {}
def file_prov(path):
    """actual source bytes: repo, tracked?, modified vs HEAD?, sha256 of the file as read, sha256 of HEAD's copy"""
    if path in _PROV: return _PROV[path]
    ap = os.path.realpath(path if os.path.isabs(path) else os.path.join(ROOT, path)); d = os.path.dirname(ap); g = lambda *a: subprocess.run(['git', '-C', d] + list(a), capture_output=True, text=True)
    top = os.path.realpath(g('rev-parse', '--show-toplevel').stdout.strip() or '/nonexistent'); sh = hashlib.sha256(open(ap, 'rb').read()).hexdigest()
    if not top: r = dict(repo='none', head='', tracked='no-repo', dirty='', sha=sh, sha_head='', match=False)
    else:
        rel = os.path.relpath(ap, top); gt = lambda *a: subprocess.run(['git', '-C', top] + list(a), capture_output=True, text=True)
        head = gt('rev-parse', 'HEAD').stdout.strip()[:10]; tracked = gt('ls-files', '--error-unmatch', '--', rel).returncode == 0
        ig = gt('check-ignore', '-q', '--', rel).returncode == 0
        shh = hashlib.sha256(subprocess.run(['git', '-C', top, 'show', 'HEAD:' + rel], capture_output=True).stdout).hexdigest() if tracked else ''
        other = ''
        if not tracked:
            c = gt('log', '--all', '-1', '--diff-filter=AMR', '--format=%H', '--', rel).stdout.strip()
            if c:
                shc = hashlib.sha256(subprocess.run(['git', '-C', top, 'show', c + ':' + rel], capture_output=True).stdout).hexdigest()
                if shc == sh: other = c[:10]
        if other:
            br = gt('branch', '-a', '--contains', other).stdout.split()
            r = dict(repo=os.path.basename(top), head=other, tracked='NOT-IN-CHECKED-OUT-HEAD; bytes equal commit ' + other + ' on ' + ','.join(x for x in br if x != '*')[:80], dirty='', sha=sh, sha_head=sh, match=True)
            r['rel'] = os.path.relpath(ap, ROOT) if ap.startswith(ROOT) else ap; _PROV[path] = r; return r
        r = dict(repo=os.path.basename(top), head=head, tracked=('tracked' if tracked else ('UNTRACKED-ignored' if ig else 'UNTRACKED')), dirty=('' if not tracked else ('modified' if shh != sh else 'clean')), sha=sh, sha_head=shh, match=bool(tracked and shh == sh))
    r['rel'] = os.path.relpath(ap, ROOT) if ap.startswith(ROOT) else ap; _PROV[path] = r; return r
def prov_str(path):
    r = file_prov(path); return '%s@%s %s%s sha256:%s' % (r['repo'], r['head'], r['tracked'], ('/' + r['dirty']) if r['dirty'] else '', r['sha'][:12])

NSEV = re.compile(r'^[ \t]*(namespace|end|section)(?:[ \t]+([A-Za-z0-9_.]+))?[ \t]*$', re.M)
def namespaces_at(s, pos_list):
    """namespace stack at each declaration position (namespace X ... end X); sections push a blank frame"""
    ev = [(m.start(), m.group(1), m.group(2) or '') for m in NSEV.finditer(s)]; out = []
    for p in pos_list:
        st = []
        for q, k, n in ev:
            if q >= p: break
            if k == 'end':
                if st: st.pop()
            else: st.append(n if k == 'namespace' else '')
        out.append('.'.join(x for x in st if x))
    return out

def index_lean():
    idx = defaultdict(list)
    for p in lean_files():
        try: s = open(p, encoding='utf-8', errors='replace').read()
        except OSError: continue
        ms = list(DECL.finditer(s)); nss = namespaces_at(s, [m.start() for m in ms]); rel = os.path.relpath(p, ROOT) if p.startswith(ROOT) else p
        rev = repo_rev(p); fax = bool(re.search(r'^\s*axiom\s', s, re.M))
        for k, m in enumerate(ms):
            end = ms[k + 1].start() if k + 1 < len(ms) else len(s)
            stmt, head, proof = split_statement(s[m.start():end]); name = m.group(2).split('.')[-1]
            idx[name].append(dict(kind=m.group(1), file=rel, line=s.count('\n', 0, m.start()) + 1, ns=nss[k], rev=rev,
                                  stmt=norm(stmt)[:900], head=norm(head)[:200], body=proof, file_declares_axiom=fax))
    return idx

LEANREF = re.compile(r'[A-Za-z0-9_./-]+\.lean')
def resolve(decl, cands, text_near, text_page):
    """-> (status, chosen candidate or None, narrowed candidates). Never picks silently: UNRESOLVED when page evidence does not decide."""
    if len(cands) == 1: return 'UNIQUE', cands[0], cands
    def by_path(txt, cs):      # a link carrying a path (../Orthogenesis/Architecture/X.lean) names one file
        paths = {re.sub(r'^(\.\./|\./)+', '', h) for h in LEANREF.findall(txt) if '/' in h}
        return [c for c in cs if any(c['file'] == h or c['file'].endswith('/' + h) for h in paths)]
    def by_base(txt, cs):      # a bare file name is weaker evidence: two repos can hold the same name
        hints = set(LEANREF.findall(txt)); return [c for c in cs if any(os.path.basename(c['file']) == os.path.basename(h) for h in hints)]
    def by_ns(txt, cs):
        quals = {m.group(1).rstrip('.') for m in re.finditer(r'((?:[A-Za-z][A-Za-z0-9_]*\.)+)' + re.escape(decl) + r'\b', txt)}
        return [c for c in cs if c['ns'] and any(c['ns'] == q or c['ns'].endswith('.' + q) or q.endswith(c['ns']) for q in quals)]
    cs = cands
    for label, fn in (('BY_PAGE_PATH', by_path), ('BY_PAGE_BASENAME', by_base), ('BY_PAGE_NS', by_ns)):
        for txt in (text_near, text_page):
            k = fn(txt, cs)
            if k and len(k) < len(cs): cs = k
            if len(cs) == 1: return label, cs[0], cs
    if len({c['stmt'] for c in cs}) == 1: return 'IDENTICAL_COPIES', sorted(cs, key=lambda c: (c['file'].startswith('/'), c['file']))[0], cs
    return 'UNRESOLVED', None, cs

DEFKINDS = ('def', 'abbrev', 'structure', 'inductive', 'class')
def definitions_for(chosen, idx):
    gaps = []; out = []; seen = set(); files = []
    for tok in re.findall(r"[A-Za-z_][A-Za-z0-9_'.]*", chosen['stmt']):
        t = tok.split('.')[-1]
        if t in seen or t not in idx: continue
        seen.add(t); cs = [c for c in idx[t] if c['kind'] in DEFKINDS]
        if not cs: continue
        same = [c for c in cs if c['file'] == chosen['file']] or cs
        if len({(c['stmt'], norm(re.split(r'/-|--', c['body'].split('\n\n')[0])[0])[:300]) for c in same}) > 1: gaps.append('AMBIGUOUS_DEF:' + t); continue
        c = same[0]; files.append(c['file']); val = re.split(r'/-|--', c['body'].split('\n\n')[0])[0]; out.append('%s := %s' % (c['stmt'], norm(val)[:300]))
        if len(out) >= 6: gaps.append('MORE_DEFS_OMITTED'); break
    return ' || '.join(out), gaps, files

def units(page, idx):
    t = page_text(os.path.join(ROOT, page)); sents = [x.strip() for x in re.split(r'(?<=[.!?])\s+(?=[A-Z0-9\\(])', t) if len(x.strip()) > 25]
    names = {n for n in idx if len(n) >= 6 and ('_' in n or re.search(r'[a-z][A-Z]', n))}
    out_s, out_n, out_c = [], [], []
    for i, s in enumerate(sents):
        ctx = ' '.join(sents[max(0, i - 1):i + 2])[:700]
        toks = set(re.findall(r"[A-Za-z_][A-Za-z0-9_']*", s)); hit = sorted(n for n in toks if n in names)
        if hit: out_s.append((page, s[:500], ctx, hit))
        elif TRIG.search(s) and re.search(r'\bLean\b|\bkernel\b|\bsorry\b|[Ss]orry-free', s): out_c.append((page, s[:500], ctx, 'LEAN_CLAIM_NO_DECL'))
        elif re.search(r'\b(theorem|proposition|lemma|corollary|proved|proves|proven|converges?|contraction|by (?:mathematical )?necessity)\b', s, re.I): out_c.append((page, s[:500], ctx, 'PROSE'))
        if NUM.search(s) and len(s) < 420: out_n.append((page, s[:420]))
    return out_s, out_n, out_c, len(sents)

CAP_CLAIMS, CAP_NUMS = 40, 25
def wtsv(path, header, rows):
    with open(path, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t'); w.writerow(header); w.writerows(rows)
def rtsv(path): return list(csv.DictReader(open(path, encoding='utf-8'), delimiter='\t'))

def cmd_extract(args):
    out = args[args.index('--out') + 1]; pages = [a for a in args if a != '--out' and a != out and not a.startswith('--')]
    os.makedirs(out, exist_ok=True); idx = index_lean(); M = Counter(); S = {}; C = {}; N = {}; overflow = []
    for pg in pages:
        us, ns, cs, nsent = units(pg, idx); M['sentences_scanned'] += nsent
        for page, sent, ctx, decls in us:
            for dn in decls:
                M['unit_rows_raw(sentence x decl)'] += 1; k = (norm(sent), dn)
                if k in S: S[k]['pages'].append(page); M['unit_rows_deduped_away'] += 1
                else: S[k] = dict(id='S-' + sha(*k)[:8], pages=[page], sentence=sent, context=ctx, decl=dn)
        kept = 0
        for page, sent, ctx, origin in cs:
            M['claim_sentences_raw'] += 1; k = norm(sent)
            if k in C: C[k]['pages'].append(page); M['claims_deduped_away'] += 1; continue
            if kept >= CAP_CLAIMS: overflow.append((page, sent, origin)); M['claims_over_cap(%d/page)' % CAP_CLAIMS] += 1; continue
            kept += 1; C[k] = dict(id='C-' + sha(k)[:8], pages=[page], sentence=sent, context=ctx, origin=origin)
        kept = 0
        for page, sent in ns:
            M['number_sentences_raw'] += 1; k = norm(sent)
            if k in N: M['numbers_deduped_away'] += 1; continue
            if kept >= CAP_NUMS: M['numbers_over_cap(%d/page)' % CAP_NUMS] += 1; continue
            kept += 1; N[k] = dict(id='N-' + sha(k)[:8], pages=[page], sentence=sent)
    unit_sents = {k[0] for k in S}
    for k, v in N.items(): v['also_in'] = ','.join(x for x, ok in (('statement-unit', k in unit_sents), ('prose-claim', k in C)) if ok)
    M['numbers_that_are_also_in_a_unit_or_claim'] = sum(1 for v in N.values() if v['also_in'])
    M['POP statement (named declaration, deduped)'] = len(S)
    M['POP claim (prose %d + lean-claim-without-declaration %d)' % (sum(v['origin'] == 'PROSE' for v in C.values()), sum(v['origin'] != 'PROSE' for v in C.values()))] = len(C)
    M['POP number'] = len(N)
    wtsv(os.path.join(out, 'units.tsv'), ['id', 'pages', 'decl', 'sentence', 'context'], [[v['id'], ';'.join(v['pages']), v['decl'], v['sentence'], v['context']] for v in S.values()])
    wtsv(os.path.join(out, 'claims.tsv'), ['id', 'pages', 'origin', 'sentence', 'context'], [[v['id'], ';'.join(v['pages']), v['origin'], v['sentence'], v['context']] for v in C.values()])
    wtsv(os.path.join(out, 'claims-overflow.tsv'), ['page', 'origin', 'sentence'], [[a, c, b] for a, b, c in overflow])
    wtsv(os.path.join(out, 'numbers.tsv'), ['id', 'pages', 'also_in', 'sentence'], [[v['id'], ';'.join(v['pages']), v['also_in'], v['sentence']] for v in N.values()])
    json.dump(dict(M), open(os.path.join(out, 'manifest-extract.json'), 'w'), indent=1)
    print('EXTRACT COUNTS (three separate populations; manifest-extract.json)')
    for k, v in M.items(): print('  %-78s %s' % (k, v))

def cmd_freeze(args):
    d = args[0]; idx = index_lean(); rep = axiom_reports(); units_ = rtsv(os.path.join(d, 'units.tsv')); M = Counter()
    frozen, smap, unres = [], [], []; used_files = set()
    for u in units_:
        cands = idx.get(u['decl'], []); pg = u['pages'].split(';')[0]
        raw = open(os.path.join(ROOT, pg), encoding='utf-8', errors='replace').read()
        status, ch, narrowed = resolve(u['decl'], cands, u['context'] + ' ' + u['sentence'], raw); M['status:' + status] += 1
        cand_s = ' | '.join('%s:%d ns=%s %s' % (c['file'], c['line'], c['ns'] or '-', prov_str(c['file'])) for c in cands)
        if ch is None:
            unres.append([u['id'], u['pages'], u['decl'], cand_s]); smap.append([u['id'], u['pages'], u['decl'], status, '', cand_s, '', '', '', '']); continue
        defs, gaps, dfiles = definitions_for(ch, idx); used_files.update([ch['file']] + dfiles)
        stmt_shown = ch['stmt'] if ch['kind'] not in DEFKINDS else ch['stmt'] + ' := ' + norm(re.split(r'/-|--', ch['body'].split('\n\n')[0])[0])[:300]
        fl = flags(dict(kind=ch['kind'], stmt=ch['stmt'], head=ch['head'], body=ch['body'], file_has_axiom=False))
        k = rep.get(u['decl']); ar = 'no-report' if k is None else ('report:sorryAx' if k else 'report:no-sorryAx')
        row = [u['id'], u['sentence'], u['context'], u['decl'], ch['kind'], stmt_shown, defs]; row.append(sha(*row[1:])); frozen.append(row)
        smap.append([u['id'], u['pages'], u['decl'], status, '%s:%d ns=%s %s' % (ch['file'], ch['line'], ch['ns'] or '-', prov_str(ch['file'])), cand_s, ';'.join(fl),
                     ar + ('; name-is-ambiguous' if len(cands) > 1 and k is not None else ''), 'file-declares-an-axiom' if ch['file_declares_axiom'] else '', ';'.join(gaps)])
    P = [[f, file_prov(f)['repo'], file_prov(f)['head'], file_prov(f)['tracked'], file_prov(f)['dirty'], file_prov(f)['sha'], file_prov(f)['sha_head'], 'yes' if file_prov(f)['match'] else 'NO'] for f in sorted(used_files)]
    wtsv(os.path.join(d, 'provenance.tsv'), ['file(source actually read)', 'repo', 'HEAD', 'git_status', 'vs_HEAD', 'sha256_as_read', 'sha256_at_HEAD', 'bytes_match_HEAD'], P)
    nm = sum(1 for r in P if r[7] == 'NO'); M['source files used'] = len(P); M['source files whose bytes do NOT match a committed HEAD (untracked or modified)'] = nm
    M['INPUT MODE'] = 'working-tree files read; every file is byte-identical to its committed HEAD blob' if nm == 0 else 'WORKING-TREE SNAPSHOT (%d of %d files are not at a committed state)' % (nm, len(P))
    H = ['id', 'sentence', 'context', 'declaration', 'kind', 'statement', 'definitions', 'input_sha']
    wtsv(os.path.join(d, 'frozen-statements.tsv'), H, frozen)
    wtsv(os.path.join(d, 'unresolved.tsv'), ['id', 'pages', 'decl', 'candidates'], unres)
    wtsv(os.path.join(d, 'sourcemap.tsv'), ['id', 'pages', 'decl', 'mapping_status', 'chosen(file:line ns rev)', 'all_candidates', 'flags(heuristic leads)', 'axiom_report(for this NAME only)', 'file_axiom_note(not a dependency claim)', 'context_gaps'], smap)
    fc = []
    for c in rtsv(os.path.join(d, 'claims.tsv')):
        row = [c['id'], c['sentence'], c['context']]; fc.append(row + [sha(*row[1:])])
    wtsv(os.path.join(d, 'frozen-claims.tsv'), ['id', 'sentence', 'context', 'input_sha'], fc)
    fn = []
    for n in rtsv(os.path.join(d, 'numbers.tsv')):
        row = [n['id'], n['sentence']]; fn.append(row + [sha(*row[1:])])
    wtsv(os.path.join(d, 'frozen-numbers.tsv'), ['id', 'sentence', 'input_sha'], fn)
    priv = {r[0]: r for r in smap}
    wtsv(os.path.join(d, 'worklist.tsv'), H + ['flags(private)', 'label_claude', 'note'], [r + [priv[r[0]][6], '', ''] for r in frozen])
    wtsv(os.path.join(d, 'worklist-claims.tsv'), ['id', 'sentence', 'context', 'input_sha', 'label_claude', 'note'], [r + ['', ''] for r in fc])
    wtsv(os.path.join(d, 'worklist-numbers.tsv'), ['id', 'sentence', 'input_sha', 'label_claude', 'note'], [r + ['', ''] for r in fn])
    M['frozen statement rows (go to sheets)'] = len(frozen); M['excluded: UNRESOLVED mapping (not scored)'] = len(unres)
    json.dump(dict(M), open(os.path.join(d, 'manifest-freeze.json'), 'w'), indent=1)
    print('FREEZE COUNTS'); [print('  %-60s %s' % kv) for kv in M.items()]; print('  frozen claims %d, frozen numbers %d' % (len(fc), len(fn)))

PROMPT = """You are the second reader in a two-reader check of a mathematics book. You have NOT seen the first reader's labels or notes. Do not look for them.
Judge each row only from what the row shows. Do not use outside sources for what a declaration "really" says.

STATEMENT SHEET (blind-statements.tsv). Each row has a SENTENCE and its CONTEXT from a book page, the Lean STATEMENT (the declaration's type with its hypotheses, as written)
and DEFINITIONS (the definitions that statement mentions, when available). Decide whether the statement, read literally, establishes what the sentence says.
Do not assume the proof is right and do not reward the name of the declaration. Read the statement. Labels, exactly one per row:
  M  the statement establishes the sentence as written
  W  the statement is weaker or narrower than the sentence (note what is missing)
  U  the statement is about a different object than the sentence names (note which)
  V  the statement is vacuous or trivially true (note the trivial witness: n = 0, an empty set, `True`, `x = x`)
  K  MISSING CONTEXT: a definition, hypothesis or page text needed to judge is not shown (note exactly what). K is not a verdict on the claim.
Try to break each statement first: choose the smallest or degenerate input (0, the empty set, the zero map, a constant function) and see whether the
conclusion holds for the wrong reason. Put what you tried in the note column. One line.

CLAIM SHEET (blind-claims.tsv). Each row is a theorem-shaped sentence with its neighbouring sentences and NO Lean statement. Decide what the page gives for it. Labels:
  P  proved in the context shown
  S  a sketch or an appeal to another result (note which)
  B  a bare assertion, no argument shown
  F  false or unsupported as stated (note a counterexample or the missing hypothesis; try the smallest degenerate case first)
  K  MISSING CONTEXT: what is needed to judge is not shown (note what). K is different from F: do not use F for 'I cannot see it'.
For claims like 'G is a contraction', 'converges', 'by necessity': ask what the operators are, on what space, and whether the context defines them.

NUMBER SHEET (blind-numbers.tsv). Each row has a sentence with a stated number. Recompute it from what the sentence itself states (show the arithmetic in the note column).
  R  matches to the stated precision      X  does not match (give your value)      C  cannot recompute from what is stated (say what is missing)
Never copy a number from memory; compute it.

Return the same file with the last two columns (label, note) filled, tab-separated, same row ids and same other columns, any order. Do not add, delete or edit rows. Include every row."""

CTRL = [  # seeded known-answer rows, expected labels kept in a private file; they look like any other row
 ('S', 'Every function f on the naturals has a fixed point.', '', 'fixedpt_ctrl', 'theorem', 'theorem fixedpt_ctrl (f : ℕ → ℕ) : ∃ x : ℕ, x = x', '', 'V'),
 ('S', 'For every real x > 0, both x^2 > 0 and x^3 > 0.', '', 'pos_ctrl', 'theorem', 'theorem pos_ctrl (x : ℝ) (hx : 0 < x) : 0 < x ^ 2', '', 'W'),
 ('S', 'For every natural number n, n + 0 = n.', '', 'addzero_ctrl', 'theorem', 'theorem addzero_ctrl (n : ℕ) : n + 0 = n', '', 'M'),
 ('S', 'The area of a disk of radius r is 2 pi r.', '', 'circ_ctrl', 'theorem', 'theorem circ_ctrl (r : ℝ) : circumference r = 2 * Real.pi * r', 'def circumference (r : ℝ) : ℝ := 2 * Real.pi * r', 'U'),
 ('C', 'Theorem. Every real sequence converges. Proof: obvious.', 'Every real sequence converges. Proof: obvious. We now use this to bound the error.', '', '', '', '', 'F'),
 ('N', 'The area of a circle of radius 2 is 4 pi = 12.57.', '', '', '', '', '', 'R'),
 ('N', 'The area of a circle of radius 2 is 4 pi = 13.57.', '', '', '', '', '', 'X'),
]

def cmd_chunk(args):
    d = args[0]; ns_, nc_, nn_ = (int(x) for x in args[1:4]); name = args[4] if len(args) > 4 else 'chunk1'
    out = os.path.join(d, name); os.makedirs(out, exist_ok=True); rnd = random.Random(SEED)
    fs = rtsv(os.path.join(d, 'frozen-statements.tsv')); fc = rtsv(os.path.join(d, 'frozen-claims.tsv')); fn = rtsv(os.path.join(d, 'frozen-numbers.tsv'))
    ps = rnd.sample(fs, min(ns_, len(fs))); pc = rnd.sample(fc, min(nc_, len(fc))); pn = rnd.sample(fn, min(nn_, len(fn)))
    S = [[r['id'], r['sentence'], r['context'], r['declaration'], r['kind'], r['statement'], r['definitions'], r['input_sha']] for r in ps]
    C = [[r['id'], r['sentence'], r['context'], r['input_sha']] for r in pc]; N = [[r['id'], r['sentence'], r['input_sha']] for r in pn]; exp = []
    for k, sent, ctx, dn, kd, st, df, lab in CTRL:
        if k == 'S': row = [sent, ctx, dn, kd, st, df]; r = ['S-' + sha(*row)[:8]] + row + [sha(*row)]; S.append(r)
        elif k == 'C': row = [sent, ctx]; r = ['C-' + sha(*row)[:8]] + row + [sha(*row)]; C.append(r)
        else: row = [sent]; r = ['N-' + sha(*row)[:8]] + row + [sha(*row)]; N.append(r)
        exp.append([r[0], lab])
    rnd.shuffle(S); rnd.shuffle(C); rnd.shuffle(N)
    wtsv(os.path.join(out, 'blind-statements.tsv'), ['id', 'sentence', 'context', 'declaration', 'kind', 'statement', 'definitions', 'input_sha', 'label', 'note'], [r + ['', ''] for r in S])
    wtsv(os.path.join(out, 'blind-claims.tsv'), ['id', 'sentence', 'context', 'input_sha', 'label', 'note'], [r + ['', ''] for r in C])
    wtsv(os.path.join(out, 'blind-numbers.tsv'), ['id', 'sentence', 'input_sha', 'label', 'note'], [r + ['', ''] for r in N])
    open(os.path.join(out, 'PROMPT.txt'), 'w', encoding='utf-8').write(PROMPT + '\n')
    wtsv(os.path.join(d, name + '-controls-expected.tsv'), ['id', 'expected'], exp)
    print('%s: %d statement rows, %d claim rows, %d number rows (incl. %d seeded controls; expected labels in %s-controls-expected.tsv, outside the upload folder)' % (name, len(S), len(C), len(N), len(exp), name))

def cmd_verify(args):
    """both readers must hold identical inputs: recompute input_sha from the text columns of every sheet given"""
    bad = 0; seen = {}
    for p in args:
        for r in rtsv(p):
            cols = [r[k] for k in ('sentence', 'context', 'declaration', 'kind', 'statement', 'definitions') if k in r]
            if sha(*cols) != r['input_sha']: print('EDITED row %s in %s' % (r['id'], p)); bad += 1
            if r['id'] in seen and seen[r['id']] != r['input_sha']: print('DIFFERENT INPUT for %s between sheets' % r['id']); bad += 1
            seen[r['id']] = r['input_sha']
    print('verify: %d rows, %s' % (len(seen), 'identical inputs' if not bad else '%d PROBLEMS' % bad)); return 1 if bad else 0

ALLOWED = {'S': 'MWUVK', 'C': 'PSBFK', 'N': 'RXC'}
def cmd_agree(args):
    """primary statistics exclude seeded controls; controls are scored separately; K (missing context) is reported, not hidden"""
    d, ret = args[0], args[1]; lab = {}; ctrl = {}
    ce = os.path.join(d, 'chunk1-controls-expected.tsv')
    if os.path.exists(ce): ctrl = {r['id']: r['expected'] for r in rtsv(ce)}
    for fn in ('worklist.tsv', 'worklist-claims.tsv', 'worklist-numbers.tsv'):
        p = os.path.join(d, fn)
        if os.path.exists(p):
            for r in rtsv(p):
                if r['label_claude'].strip(): lab[r['id']] = r
    theirs = {r['id']: r for r in rtsv(ret)}
    also = {r['id']: r.get('also_in', '') for r in rtsv(os.path.join(d, 'numbers.tsv'))} if os.path.exists(os.path.join(d, 'numbers.tsv')) else {}
    for kind, nm in (('S', 'statement support'), ('C', 'prose claims'), ('N', 'numerical claims')):
        ids = [i for i in lab if i.startswith(kind + '-') and i not in ctrl and i in theirs and (theirs[i].get('label') or '').strip()]
        if not ids: print('[%s] no primary rows labelled by both readers' % nm); continue
        a = {i: lab[i]['label_claude'].strip().upper() for i in ids}; b = {i: theirs[i]['label'].strip().upper() for i in ids}
        invalid = [i for i in ids if a[i] not in ALLOWED[kind] or b[i] not in ALLOWED[kind]]; ok = [i for i in ids if i not in invalid]
        print('[%s] primary rows labelled by both: %d (invalid labels %d)' % (nm, len(ids), len(invalid)))
        if kind != 'N':
            ka = [i for i in ok if a[i] == 'K']; kb = [i for i in ok if b[i] == 'K']; kd = [i for i in ok if (a[i] == 'K') != (b[i] == 'K')]
            print('     missing-context (K) rate: claude %.2f, second reader %.2f | disagree on whether context is sufficient: %d rows (%.2f)' % (len(ka) / max(1, len(ok)), len(kb) / max(1, len(ok)), len(kd), len(kd) / max(1, len(ok))))
            sc = [i for i in ok if 'K' not in (a[i], b[i])]
        else: sc = ok
        if sc:
            po, k = kappa([a[i] for i in sc], [b[i] for i in sc]); print('     scored (no K on either side) %d of %d: exact agreement %.2f, Cohen kappa %.2f' % (len(sc), len(ok), po, k))
            for i in sc:
                if a[i] != b[i]: print('     DISAGREE %s claude=%s second=%s | %s | %s' % (i, a[i], b[i], lab[i].get('note', '')[:60], (theirs[i].get('note') or '')[:60]))
        if kind == 'N': print('     of these %d number rows, %d also appear as a statement or claim row (disclosed overlap; totals are not additive)' % (len(ok), sum(1 for i in ok if also.get(i))))
    if ctrl:
        print('SEEDED CONTROLS (reported separately, never in the statistics above):')
        for who, getl in (('second reader', lambda i: (theirs.get(i, {}).get('label') or '').strip().upper()), ('claude', lambda i: (lab.get(i, {}).get('label_claude') or '').strip().upper())):
            got = {i: getl(i) for i in ctrl}
            if not any(got.values()): print('   %s: no control labels recorded' % who); continue
            print('   %s: %d/%d correct' % (who, sum(got[i] == e for i, e in ctrl.items()), len(ctrl)) + ''.join(' | MISSED %s expected %s gave %s' % (i, e, got[i] or '-') for i, e in ctrl.items() if got[i] != e))
    return 0

CONTROLS = [  # (lean source, flag that MUST appear, or None for the sound control that must have NO flags)
 ('theorem c1 : ∃ shape : Nat, True := ⟨0, trivial⟩', 'CONCLUSION_TRUE'),
 ('theorem c2 : (1 : Nat) = 1 := rfl', 'REFLEXIVE_CONCLUSION'),
 ('theorem c3 : ∀ n : ℕ, ∃ m : ℕ, g n m = 1 := by\n  intro n\n  exact ⟨0, sorry⟩', 'SORRY'),
 ('theorem c4 (n : ℕ) : ∃ m : ℕ, m = 0 ∨ n = 0 := ⟨0, Or.inl rfl⟩', 'ZERO_WITNESS'),
 ('def c5 : Nat := 3', 'NOT_A_THEOREM(def)'),
 ('theorem c6 (n : ℕ) (hn : 0 < n) : n ≠ 0 := by omega', None),
]
def cmd_selftest():
    bad = 0
    for src, want in CONTROLS:
        m = DECL.search(src); chunk = src; stmt, head, proof = split_statement(chunk)
        d = dict(kind=m.group(1), stmt=re.sub(r'\s+', ' ', stmt), head=head, body=proof, file_has_axiom=False); got = flags(d)
        ok = (want in got) if want else (not [g for g in got if g != 'ONE_TACTIC_PROOF'])
        print(('PASS ' if ok else 'FAIL ') + 'control: %-62s flags=%s' % (src.split('\n')[0][:62], got)); bad += (not ok)
    A = dict(file='X/A.lean', ns='N1', stmt='theorem f : 1 = 1', line=1, rev='r'); B = dict(file='Y/A.lean', ns='N2', stmt='theorem f : 2 = 2', line=1, rev='r')
    B2 = dict(B, stmt=A['stmt'])
    for lab, got, want in (('resolve: no evidence + differing statements -> UNRESOLVED', resolve('f', [A, B], '', '')[0], 'UNRESOLVED'),
                           ('resolve: path link names one file', resolve('f', [A, B], 'see ../Y/A.lean', '')[0], 'BY_PAGE_PATH'),
                           ('resolve: qualified name N2.f picks namespace', resolve('f', [A, B], 'N2.f holds', '')[0], 'BY_PAGE_NS'),
                           ('resolve: identical statements, no evidence', resolve('f', [A, B2], '', '')[0], 'IDENTICAL_COPIES'),
                           ('namespaces_at', namespaces_at('namespace P\nsection\ntheorem a\nend\nend P\ntheorem b\n', [20, 40])[0], 'P')):
        ok = got == want; print(('PASS ' if ok else 'FAIL ') + lab + ' -> ' + got); bad += (not ok)
    import tempfile, shutil
    tmp = tempfile.mkdtemp(); run = lambda *a: subprocess.run(['git', '-C', tmp] + list(a), capture_output=True, text=True)
    run('init', '-q'); run('config', 'user.email', 'a@b'); run('config', 'user.name', 'x'); fp = os.path.join(tmp, 'T.lean'); open(fp, 'w').write('theorem t : 1 = 1 := rfl\n'); run('add', 'T.lean'); run('commit', '-qm', 'c')
    q1 = file_prov(fp); _PROV.clear(); open(fp, 'a').write('-- edit\n'); q2 = file_prov(fp); _PROV.clear(); fu = os.path.join(tmp, 'U.lean'); open(fu, 'w').write('x\n'); q3 = file_prov(fu); shutil.rmtree(tmp)
    for lab, ok in (('provenance: committed file reads as tracked, bytes match HEAD', q1['tracked'] == 'tracked' and q1['match']), ('provenance: edited file is flagged modified, no match', q2['dirty'] == 'modified' and not q2['match']), ('provenance: untracked file is flagged, no match', q3['tracked'].startswith('UNTRACKED') and not q3['match'])):
        print(('PASS ' if ok else 'FAIL ') + lab); bad += (not ok)
    print('selftest: %s' % ('ALL PASS' if not bad else '%d FAIL' % bad)); return 1 if bad else 0

if __name__ == '__main__':
    if len(sys.argv) < 2: print(__doc__); sys.exit(2)
    c = sys.argv[1]
    if c == 'selftest': sys.exit(cmd_selftest())
    elif c == 'extract': cmd_extract(sys.argv[2:])
    elif c == 'freeze': cmd_freeze(sys.argv[2:])
    elif c == 'chunk': cmd_chunk(sys.argv[2:])
    elif c == 'verify': sys.exit(cmd_verify(sys.argv[2:]))
    elif c == 'agree': sys.exit(cmd_agree(sys.argv[2:]) or 0)
    else: print(__doc__); sys.exit(2)
