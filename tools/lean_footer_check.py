import re, sys, os, subprocess
files = subprocess.run(['git','--no-optional-locks','grep','-l','Proved &middot; kernel-checked','--','*.html'],capture_output=True, text=True).stdout.split()
ent = re.compile(r'<a href="([^"]+\.lean)">([^<]+)</a>\s*<span[^>]*>([^<:]+\.lean):(\d+)</span>')
decl = re.compile(r'^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*(theorem|lemma|def|abbrev|structure|instance|axiom|inductive|class|opaque)\s+(\S+)')
cache = {}
def decls(path):
    if path in cache: return cache[path]
    d = {}
    if os.path.exists(path):
        for i, l in enumerate(open(path, encoding='utf-8', errors='replace'), 1):
            m = decl.match(l)
            if m:
                n = m.group(2)
                d.setdefault(n, []).append(i)
                d.setdefault(n.split('.')[-1], []).append(i)
    cache[path] = d
    return d
tot = ok = 0; bad = []
for f in sorted(files):
    txt = open(f, encoding='utf-8', errors='replace').read()
    for href, name, path, line in ent.findall(txt):
        tot += 1; line = int(line)
        if href.lstrip('./') != path: bad.append((f, name, 'href/path differ', href, path)); continue
        if not os.path.exists(path): bad.append((f, name, 'FILE MISSING', path, line)); continue
        d = decls(path)
        hits = d.get(name) or d.get(name.split('.')[-1])
        if not hits: bad.append((f, name, 'NAME NOT DECLARED', path, line)); continue
        if line in hits: ok += 1
        else: bad.append((f, name, 'LINE cited %d actual %s' % (line, hits), path))
print('pages', len(files), 'entries', tot, 'exact', ok, 'problems', len(bad))
for b in bad: print(b)
