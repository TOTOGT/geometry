#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
build_rh_paper.py — render RH_arithmetic_contact_structure.md as an HTML edition.

The markdown is the manuscript; book4/rh-paper.html is a *rendering* of it, in the
shape a reader expects from a preprint server: title block, abstract, numbered
sections, a table of contents, MathJax, and the DOI at the top where somebody
looking for it will find it.

Two files, one source. Nothing is retyped, so the HTML cannot drift from the
manuscript the way a hand-maintained copy would — which is the same argument
build_book3.py and build_rungs.py make about their own sources.

USAGE
    python3 tools/build_rh_paper.py          # report what would change
    python3 tools/build_rh_paper.py --write  # write book4/rh-paper.html

Exit status is 1 when the HTML is missing or stale, so it can gate a check.
"""

from __future__ import annotations

import html as H
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "RH_arithmetic_contact_structure.md"
OUT = ROOT / "book4" / "rh-paper.html"
DOI = "10.5281/zenodo.22179684"


def inline(t: str) -> str:
    """Markdown inline -> HTML. Math between $ is left alone for MathJax."""
    parts, out = re.split(r"(\$\$[^$]*\$\$|\$[^$\n]*\$|`[^`]*`)", t), []
    for i, seg in enumerate(parts):
        if i % 2:                                   # math or code, untouched
            if seg.startswith("`"):
                out.append(f"<code>{H.escape(seg[1:-1])}</code>")
            else:
                out.append(seg)
            continue
        seg = H.escape(seg)
        seg = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2">\1</a>', seg)
        seg = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", seg)
        seg = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", seg)
        out.append(seg)
    return "".join(out)


def render(md: str) -> tuple[str, list[tuple[int, str, str]]]:
    body, toc, lines, i = [], [], md.split("\n"), 0
    n_sec = 0
    while i < len(lines):
        ln = lines[i]

        if ln.startswith("|") and i + 1 < len(lines) and set(lines[i + 1].replace("|", "").strip()) <= set("-: "):
            head = [c.strip() for c in ln.strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip("|").split("|")])
                i += 1
            body.append("<div class=\"tbl\"><table><thead><tr>"
                        + "".join(f"<th>{inline(c)}</th>" for c in head)
                        + "</tr></thead><tbody>"
                        + "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows)
                        + "</tbody></table></div>")
            continue

        m = re.match(r"^(#{1,3})\s+(.*)$", ln)
        if m:
            lvl, txt = len(m.group(1)), m.group(2).strip()
            if lvl == 1:
                body.append(f"<h1>{inline(txt)}</h1>")
            else:
                n_sec += 1
                sid = f"s{n_sec}"
                tag = "h2" if lvl == 2 else "h3"
                body.append(f'<{tag} id="{sid}">{inline(txt)}</{tag}>')
                toc.append((lvl, sid, txt))
            i += 1
            continue

        if re.match(r"^\d+\.\s", ln) or ln.startswith("- "):
            ordered = bool(re.match(r"^\d+\.\s", ln))
            items = []
            while i < len(lines) and (re.match(r"^\d+\.\s", lines[i]) or lines[i].startswith("- ")
                                      or (items and lines[i].startswith("   ") and lines[i].strip())):
                if re.match(r"^\d+\.\s", lines[i]) or lines[i].startswith("- "):
                    items.append(re.sub(r"^(\d+\.|-)\s+", "", lines[i]))
                else:
                    items[-1] += " " + lines[i].strip()
                i += 1
            t = "ol" if ordered else "ul"
            body.append(f"<{t}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{t}>")
            continue

        if ln.strip() == "---":
            body.append("<hr>")
            i += 1
            continue

        if ln.strip() == "":
            i += 1
            continue

        para = [ln]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,3}\s|\||-\s|\d+\.\s|---$)", lines[i]):
            para.append(lines[i])
            i += 1
        body.append(f"<p>{inline(' '.join(para))}</p>")

    return "\n".join(body), toc


PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Riemann Hypothesis as Non-Integrability of an Arithmetic Contact Structure &middot; Principia Orthogona Book 4</title>
<meta name="description" content="Preprint. A reformulation of the Riemann Hypothesis as a non-vanishing condition on a globally defined arithmetic contact 3-form on the adele class space. RH itself is untouched; the paper says which claims are proved, machine-checked, classical, numerical and open.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<script>MathJax={tex:{inlineMath:[["$","$"],["\\\\(","\\\\)"]],displayMath:[["$$","$$"],["\\\\[","\\\\]"]]},options:{skipHtmlTags:["script","noscript","style","textarea","pre","code"]}};</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js" async></script>
<style>
:root{--ink:#1c1c1c;--paper:#fbfaf7;--rule:#ddd8cc;--gold:#8a7340;--navy:#1a2744;--muted:#6f6a60;--teal:#1a5c5c;--red:#8b1a1a;}
*{box-sizing:border-box;margin:0;padding:0;}
body{background:var(--paper);color:var(--ink);font-family:Georgia,'Times New Roman',serif;line-height:1.7;font-size:17px;}
.bar{background:var(--navy);color:#cfc9bb;padding:.6rem 1.5rem;font-family:'JetBrains Mono',monospace;font-size:.64rem;letter-spacing:.1em;text-transform:uppercase;display:flex;gap:1.4rem;flex-wrap:wrap;justify-content:space-between;}
.bar a{color:#c9a84c;text-decoration:none;}
.wrap{max-width:820px;margin:0 auto;padding:2.6rem 1.6rem 5rem;}
.stamp{font-family:'JetBrains Mono',monospace;font-size:.62rem;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);margin-bottom:1.2rem;}
h1{font-size:clamp(1.5rem,3.4vw,2.1rem);font-weight:400;line-height:1.28;color:var(--navy);margin:0 0 1rem;}
.byline{font-size:.95rem;color:var(--muted);margin-bottom:.4rem;}
.doi{font-family:'JetBrains Mono',monospace;font-size:.72rem;margin:1rem 0 1.6rem;padding:.7rem .9rem;background:#fff;border:1px solid var(--rule);border-left:3px solid var(--gold);}
.doi a{color:var(--teal);}
h2{font-size:1.16rem;font-weight:600;color:var(--navy);margin:2.4rem 0 .7rem;padding-top:.5rem;border-top:1px solid var(--rule);}
h3{font-size:1.02rem;font-weight:600;color:var(--navy);margin:1.7rem 0 .5rem;}
p{margin-bottom:1rem;}
ol,ul{margin:0 0 1.1rem 1.4rem;}
li{margin-bottom:.55rem;}
hr{border:0;border-top:1px solid var(--rule);margin:2rem 0;}
code{font-family:'JetBrains Mono',monospace;font-size:.84em;background:#fff;border:1px solid var(--rule);padding:.05rem .3rem;}
a{color:var(--teal);}
.tbl{overflow-x:auto;margin:1.3rem 0;}
table{width:100%;border-collapse:collapse;font-size:.86rem;background:#fff;}
th{text-align:left;padding:.55rem .7rem;border-bottom:2px solid var(--gold);color:var(--navy);font-weight:600;}
td{padding:.55rem .7rem;border-bottom:1px solid var(--rule);vertical-align:top;}
.toc{background:#fff;border:1px solid var(--rule);padding:1.1rem 1.3rem;margin:1.8rem 0 2.4rem;}
.toc .t{font-family:'JetBrains Mono',monospace;font-size:.6rem;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);margin-bottom:.6rem;}
.toc a{display:block;text-decoration:none;color:var(--ink);font-size:.9rem;padding:.12rem 0;}
.toc a:hover{color:var(--teal);}
.toc a.sub{padding-left:1.3rem;font-size:.85rem;color:var(--muted);}
footer{border-top:1px solid var(--rule);margin-top:3rem;padding-top:1.3rem;font-family:'JetBrains Mono',monospace;font-size:.64rem;line-height:1.9;color:var(--muted);}
footer a{color:var(--gold);text-decoration:none;}
@media print{.bar,.toc{display:none}body{background:#fff}}
</style>
</head>
<body>
<div class="bar">
  <span><a href="../index.html">&#9884; PRINCIPIA ORTHOGONA</a> &middot; <a href="index.html">Book 4</a></span>
  <span><a href="ch12.html">Ch 12 &middot; The Critical Contact</a> &middot; <a href="https://doi.org/__DOI__">Zenodo &#8599;</a></span>
</div>
<div class="wrap">
  <div class="stamp">Preprint &middot; not peer reviewed &middot; Book 4 &middot; the arithmetic arc</div>
__TITLE__
  <p class="byline">Pablo Nogueira Grossi (framework) &middot; Collaborative Draft</p>
  <div class="doi">
    DOI reserved: <a href="https://doi.org/__DOI__">__DOI__</a> &mdash; Zenodo community <em>Principia Orthogona</em>.<br>
    Deposit pending; the DOI will not resolve until the record is published.<br>
    Manuscript source: <code>RH_arithmetic_contact_structure.md</code> &middot; this page is generated from it by <code>tools/build_rh_paper.py</code>.
  </div>
  <div class="toc"><div class="t">Contents</div>__TOC__</div>
__BODY__
  <footer>
    Chapter-form treatment of this material: <a href="ch11.html">Ch 11 &middot; The Arithmetic Seed</a> &middot;
    <a href="ch12.html">Ch 12 &middot; The Critical Contact</a> &middot;
    <a href="ch13.html">Ch 13 &middot; The Adelic Tesseract</a> &middot;
    <a href="ch14.html">Ch 14 &middot; The Positivity Rung</a> &middot;
    <a href="ch15-complex-turn.html">Ch 15 &middot; The Complex Turn</a><br>
    &copy; 2026 Pablo Nogueira Grossi &middot; G6 LLC &middot; <a href="mailto:g6llc@proton.me">g6llc@proton.me</a> &middot;
    ORCID <a href="https://orcid.org/0009-0000-6496-2186">0009-0000-6496-2186</a> &middot; CC BY-NC-ND 4.0
  </footer>
</div>
</body>
</html>
"""


def main() -> int:
    write = "--write" in sys.argv
    md = SRC.read_text(encoding="utf-8")
    body, toc = render(md)

    m = re.search(r"^# (.+)$", md, re.M)
    title = f"<h1>{inline(m.group(1))}</h1>" if m else "<h1>Untitled</h1>"
    body = re.sub(r"<h1>.*?</h1>\s*", "", body, count=1, flags=re.S)

    toc_html = "".join(
        f'<a href="#{sid}" class="{"sub" if lvl == 3 else ""}">{H.escape(txt)}</a>'
        for lvl, sid, txt in toc)

    page = (PAGE.replace("__TITLE__", "  " + title)
                .replace("__TOC__", toc_html)
                .replace("__BODY__", body)
                .replace("__DOI__", DOI))

    old = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
    print(f"source   {SRC.name}: {len(md.splitlines())} lines")
    print(f"rendered {OUT.relative_to(ROOT)}: {len(toc)} sections, {len(page)} bytes")
    if page == old:
        print("\nUP TO DATE — the HTML matches the manuscript.")
        return 0
    if write:
        OUT.write_text(page, encoding="utf-8")
        print("\nWROTE " + str(OUT.relative_to(ROOT)))
        return 0
    print("\nSTALE — the HTML does not match the manuscript. Re-run with --write.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
