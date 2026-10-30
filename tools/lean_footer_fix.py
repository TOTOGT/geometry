#!/usr/bin/env python3
"""lean_footer_fix.py — rewrite the file:line in "Proved · kernel-checked" footers to the
line where the cited declaration is now declared in the cited file. Names and files are
never changed; an entry whose name is not declared in its file is reported and left alone.
    python3 tools/lean_footer_fix.py          report
    python3 tools/lean_footer_fix.py --write  rewrite
"""
import re, os, subprocess, sys
write = '--write' in sys.argv
decl = re.compile(r'^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*(?:theorem|lemma|def|abbrev|structure|instance|axiom|inductive|class|opaque)\s+(\S+)')
ent = re.compile(r'(<a href="[^"]+\.lean">([^<]+)</a>\s*<span[^>]*>)([^<:]+\.lean):(\d+)(</span>)')
cache = {}
def lines_of(path, name):
    if path not in cache:
        d = {}
        if os.path.exists(path):
            for i, l in enumerate(open(path, encoding='utf-8', errors='replace'), 1):
                m = decl.match(l)
                if m: d.setdefault(m.group(1).split('.')[-1], i)
        cache[path] = d
    return cache[path].get(name.split('.')[-1])
files = subprocess.run(['git','--no-optional-locks','grep','-l','Proved &middot; kernel-checked','--','*.html'],capture_output=True,text=True).stdout.split()
changed = unresolved = 0
for f in sorted(files):
    txt = open(f, encoding='utf-8').read()
    def sub(m):
        global changed, unresolved
        actual = lines_of(m.group(3), m.group(2))
        if actual is None:
            unresolved += 1; print('UNRESOLVED', f, m.group(2), m.group(3)); return m.group(0)
        if actual != int(m.group(4)):
            changed += 1; print('%s: %s %s:%s -> %d' % (f, m.group(2), m.group(3), m.group(4), actual))
            return '%s%s:%d%s' % (m.group(1), m.group(3), actual, m.group(5))
        return m.group(0)
    new = ent.sub(sub, txt)
    if write and new != txt: open(f, 'w', encoding='utf-8').write(new)
print('changed', changed, 'unresolved', unresolved, '(written)' if write else '(report only)')
