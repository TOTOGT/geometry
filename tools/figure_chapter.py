#!/usr/bin/env python3
"""
figure_chapter.py -- emit a Book VII figure chapter in the house shell.

Book VII has seventy ch-<figure>.html pages and one visual grammar, carried in a
6 KB <style> block that is copied from chapter to chapter. Re-typing it per
chapter is how the grammar drifts, so this reads it from a reference chapter at
build time and never stores a second copy.

It emits the shell. THE PROSE IS NOT GENERATED -- it is passed in, written by
hand, chapter by chapter. A generated biography would be worth nothing.

Used by tools/chapters/<slug>.py, each of which holds one chapter's content and
calls build(). Run one of those, not this.
"""
import html as H, io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF  = os.path.join(ROOT, "book7", "ch-grothendieck.html")

def _style():
    s = io.open(REF, encoding="utf-8").read()
    m = re.search(r"<style>(.*?)</style>", s, re.S)
    if not m:
        raise SystemExit("no <style> in the reference chapter %s" % REF)
    return m.group(1)

def build(slug, name, hero_sub, description, parts,
          place_rows=(), refs=(), prev=None, nxt=None, verify=None, extra_css=""):
    """parts: [(part_label_or_None, h2, [raw html blocks])]"""
    body = []
    for label, h2, blocks in parts:
        if label:
            body.append('  <div class="section-label">%s</div>\n' % label)
        body.append("  <h2>%s</h2>\n" % h2)
        for b in blocks:
            b = b.strip()
            body.append("  " + (b if b.startswith("<") else
                                '<p class="block-prose">%s</p>' % b) + "\n")

    if place_rows:
        body.append('  <div class="section-label">Place in the Series</div>\n  <h2>Where this sits on the operator map</h2>\n')
        body.append('  <table>\n    <tr><th>Operator</th><th>In this chapter</th><th>In dm&sup3;</th></tr>\n')
        for a, b, c in place_rows:
            body.append("    <tr><td>%s</td><td>%s</td><td>%s</td></tr>\n" % (a, b, c))
        body.append("  </table>\n")

    if verify:
        body.append('  <h2>Verification</h2>\n  <p class="block-prose">Every number on this page is'
                    ' produced by <code>%s</code>. It records in its own closing block what it'
                    ' establishes and what it does not.</p>\n' % H.escape(verify))

    if refs:
        body.append("  <h2>References</h2>\n  <p class=\"block-prose\" style=\"font-size:.92rem;line-height:1.85\">\n")
        body.append("<br>\n".join("    " + r for r in refs))
        body.append("\n  </p>\n")

    nav = []
    if prev: nav.append('  <a href="%s">&larr; %s</a>\n' % prev)
    nav.append('  <a href="index.html">Back to G7 Index</a>\n')
    if nxt: nav.append('  <a href="%s">%s &rarr;</a>\n' % nxt)

    page = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} &middot; Book 7: Scientist Gallery &middot; Principia Orthogona</title>
<meta name="description" content="{desc}">
<script>MathJax={{tex:{{inlineMath:[['$','$'],['\\\\(','\\\\)']],displayMath:[['$$','$$'],['\\\\[','\\\\]']]}},options:{{skipHtmlTags:['script','noscript','style','textarea','pre']}}}};</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js" async></script>
<style>{style}{extra}</style>
</head>
<body>

<nav>
  <a href="../living-book.html" class="nav-logo">&#9884; Principia Orthogona &middot; G1&ndash;G7</a>
  <div class="nav-links">
    <a href="../book4/index.html">G4</a>
    <a href="../book6/index.html">G6</a>
    <a href="index.html">G7</a>
    <a href="../book13/index.html">G13</a>
    <a href="../omega/omega-point-index.html">Omega Point</a>
  </div>
</nav>

<div class="hero">
  <div class="hero-eyebrow">G7 &middot; The Scientist Gallery &middot; Attribution Series</div>
  <h1>{name}</h1>
  <p class="hero-sub">{sub}</p>
</div>

<div class="page">

{body}
</div>

<div class="ch-nav">
{nav}</div>

<footer>
  <a href="index.html">Book 7</a> &middot; <a href="../series-hub.html">Series Hub</a> &middot; <a href="../chapters-diagram.html">All Chapters</a><br>
  &copy; 2026 Pablo Nogueira Grossi &middot; G6 LLC &middot; Newark, New Jersey &middot; CC BY-NC-ND 4.0<br>
  <span class="prov-add">ORCID <a href="https://orcid.org/0009-0000-6496-2186" target="_blank" rel="noopener">0009-0000-6496-2186</a> &middot; Series <a href="https://zenodo.org/communities/principia-orthogona" target="_blank" rel="noopener">Principia Orthogona community</a></span>
</footer>
</body>
</html>
""".format(name=name, desc=H.escape(description, quote=True), style=_style(),
           extra=extra_css, sub=hero_sub, body="".join(body), nav="".join(nav))

    out = os.path.join(ROOT, "book7", "ch-%s.html" % slug)
    io.open(out, "w", encoding="utf-8").write(page)
    print("wrote book7/ch-%s.html  (%d bytes)" % (slug, len(page.encode("utf-8"))))
    return out

TAGCSS = """
.tag{font-family:ui-monospace,monospace;font-size:.66rem;letter-spacing:.12em;padding:.14rem .5rem;
 border-radius:3px;border:1px solid;white-space:nowrap;vertical-align:middle;}
.tag.t-shown{color:#7a9471;border-color:#7a9471;background:rgba(122,148,113,.12);}
.tag.t-cited{color:#c9a84c;border-color:#c9a84c;background:rgba(201,168,76,.12);}
.tag.t-open{color:#c1613b;border-color:#c1613b;background:rgba(193,97,59,.12);}
.tag.t-computed{color:#6f9bd1;border-color:#6f9bd1;background:rgba(111,155,209,.12);}
"""
