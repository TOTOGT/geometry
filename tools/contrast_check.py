#!/usr/bin/env python3
"""
contrast_check.py — find text that inherits a colour its own background cannot carry.

    python3 tools/contrast_check.py --class orthogenesis-note FILE.html ...

An element that sets a background but no colour inherits the colour from its
nearest ancestor that sets one -- usually `body`. Put such an element inside a
dark container whose own rule sets no colour either, and the text renders in the
body colour on the container's background. Nothing errors; it is simply
unreadable, and only a person looking at the page finds it.

This resolves, for the element: the nearest ancestor (or inline style) that sets
`color`, the nearest that sets a non-transparent `background`, CSS custom
properties declared on :root, and the WCAG contrast ratio between the two.
Below 4.5 is flagged; below 3.0 is reported as unreadable.
"""
import sys, re, argparse
from html.parser import HTMLParser

def parse_vars(css):
    v = {}
    m = re.search(r':root\s*\{(.*?)\}', css, re.S)
    if m:
        for k, val in re.findall(r'(--[\w-]+)\s*:\s*([^;]+);', m.group(1)):
            v[k] = val.strip()
    return v

def resolve(val, vars_, depth=0):
    if depth > 6: return val
    m = re.search(r'var\(\s*(--[\w-]+)\s*(?:,\s*([^)]+))?\)', val)
    if not m: return val.strip()
    repl = vars_.get(m.group(1), (m.group(2) or '').strip())
    return resolve(val[:m.start()] + repl + val[m.end():], vars_, depth+1)

def to_rgb(c):
    c = c.strip().lower()
    names = {'white': (255,255,255), 'black': (0,0,0)}
    if c in names: return names[c]
    m = re.match(r'#([0-9a-f]{3}|[0-9a-f]{6})$', c)
    if m:
        h = m.group(1)
        if len(h) == 3: h = ''.join(ch*2 for ch in h)
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    m = re.match(r'rgba?\(([^)]+)\)', c)
    if m:
        p = [x.strip() for x in m.group(1).replace('/', ' ').split(',')]
        try: return tuple(int(float(x)) for x in p[:3])
        except ValueError: return None
    return None

def alpha_of(c):
    m = re.match(r'rgba\(([^)]+)\)', c.strip().lower())
    if m:
        p = [x.strip() for x in m.group(1).split(',')]
        if len(p) == 4:
            try: return float(p[3])
            except ValueError: return 1.0
    if c.strip().lower() in ('transparent', 'none'): return 0.0
    return 1.0

def lum(rgb):
    def f(u):
        u /= 255.0
        return u/12.92 if u <= 0.04045 else ((u+0.055)/1.055) ** 2.4
    r, g, b = (f(x) for x in rgb)
    return 0.2126*r + 0.7152*g + 0.0722*b

def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

def decls_for(css, tag, cls, eid):
    """Declarations from rules whose last simple selector matches this element."""
    keys = {tag}
    keys |= {'.' + c for c in cls}
    if eid: keys.add('#' + eid)
    out = {}
    for sel, body in re.findall(r'([^{}]+)\{([^{}]*)\}', css):
        for one in sel.split(','):
            one = one.strip().split()[-1] if one.strip() else ''
            one = re.sub(r'::?[\w-]+(\([^)]*\))?$', '', one)
            if one and one in keys:
                for k, v in re.findall(r'([\w-]+)\s*:\s*([^;]+)', body):
                    out[k.strip()] = v.strip()
    return out

class Finder(HTMLParser):
    """target = a class name, or None to collect every element whose INLINE style
    sets a background but no colour -- the exact shape of the defect."""
    def __init__(self, target):
        super().__init__(convert_charrefs=True)
        self.target, self.stack, self.hit = target, [], None
        self.hits = []
        self.open_collectors = []   # [depth, chars, muted_depth]
        self.text_of = {}
        self.void = {'br','img','hr','meta','link','input','source','col','area','base','wbr'}
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        node = (tag, (a.get('class') or '').split(), a.get('id'), a.get('style') or '')
        sets_colour = bool(re.search(r'(^|;)\s*color\s*:', node[3].lower()))
        # a descendant that sets its own colour is not inheriting: mute it
        for c in self.open_collectors:
            c[0] += 1
            if sets_colour and c[2] is None:
                c[2] = c[0]
        if self.target is None:
            st = node[3].lower()
            if 'background' in st and not sets_colour:
                idx = len(self.hits)
                self.hits.append(self.stack + [node])
                self.open_collectors.append([0, [], None, idx])
        elif self.hit is None and self.target in node[1]:
            self.hit = self.stack + [node]
        if tag not in self.void:
            self.stack.append(node)
    def handle_data(self, data):
        for c in self.open_collectors:
            if c[2] is None:
                c[1].append(data)

    def handle_startendtag(self, tag, attrs): self.handle_starttag(tag, attrs)
    def handle_endtag(self, tag):
        for c in list(self.open_collectors):
            if c[2] is not None and c[0] == c[2]:
                c[2] = None
            c[0] -= 1
            if c[0] < 0:
                self.text_of[c[3]] = ''.join(c[1])
                self.open_collectors.remove(c)
        for i in range(len(self.stack)-1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]; break

    def close_all(self):
        for c in self.open_collectors:
            self.text_of[c[3]] = ''.join(c[1])

def check(path, target):
    src = open(path, encoding='utf-8', errors='replace').read()
    css = '\n'.join(re.findall(r'<style[^>]*>(.*?)</style>', src, re.S))
    vars_ = parse_vars(css)
    f = Finder(target); f.feed(src); f.close_all()
    if target is None:
        out = []
        for i, c in enumerate(f.hits):
            txt = re.sub(r'\s+', ' ', f.text_of.get(i, '')).strip()
            if len(txt) < 3:          # a swatch, bar or rule carries no text
                continue
            r = _resolve_chain(c, css, vars_)
            out.append(r + (txt[:60],))
        return out
    if not f.hit: return None
    return [_resolve_chain(f.hit, css, vars_) + ('',)]

def _resolve_chain(chain, css, vars_):
    colour = bg = None
    for tag, cls, eid, style in chain:              # outermost -> innermost
        d = decls_for(css, tag, cls, eid)
        for k, v in re.findall(r'([\w-]+)\s*:\s*([^;]+)', style):
            d[k.strip()] = v.strip()
        if 'color' in d:
            r = to_rgb(resolve(d['color'], vars_))
            if r: colour = r
        for key in ('background-color', 'background'):
            if key in d:
                val = resolve(d[key], vars_)
                cand = re.findall(r'#[0-9a-fA-F]{3,6}|rgba?\([^)]*\)|\b(?:white|black)\b', val)
                if cand:
                    a = alpha_of(cand[0]); r = to_rgb(cand[0])
                    if r and a >= 0.5: bg = r
                    elif r and a > 0 and bg is not None:
                        bg = tuple(round(a*r[i] + (1-a)*bg[i]) for i in range(3))
                    elif r and a > 0: bg = r
    if colour is None or bg is None: return ('?', colour, bg)
    return (ratio(colour, bg), colour, bg)

ap = argparse.ArgumentParser()
ap.add_argument('--class', dest='cls', default=None,
                help='class to check; omit to scan every element with an inline background and no inline colour')
ap.add_argument('files', nargs='+')
a = ap.parse_args()
bad = 0
for p in a.files:
    rs = check(p, a.cls)
    if not rs: continue
    for ratio_, c, b, txt in rs:
        if ratio_ == '?': continue
        tag = 'UNREADABLE' if ratio_ < 3.0 else ('low' if ratio_ < 4.5 else 'ok')
        if tag == 'ok':
            if a.cls: print(f"  ok          {ratio_:5.2f}:1  {p}  text#{'%02x%02x%02x'%c} on #{'%02x%02x%02x'%b}")
            continue
        bad += 1
        print(f"  {tag:<11} {ratio_:5.2f}:1  {p}  text#{'%02x%02x%02x'%c} on #{'%02x%02x%02x'%b}" + (f'  \u2014 \u201c{txt}\u201d' if txt else ''))
print(f"\n  {bad} below 4.5:1")
