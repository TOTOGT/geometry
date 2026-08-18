#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
build_indexes.py — regenerate the geometry repo's file indexes from the filesystem.

Writes `master-index.html` plus one `index-<folder>.html` per content cluster into
the repo root. Every page is self-contained (inline CSS + JS, no external deps) to
match the raw-HTML / GitHub Pages workflow.

WHY THIS SCRIPT EXISTS
----------------------
These indexes are *derived facts*. A derived fact written down once and never
recomputed is the failure mode this repo keeps hitting (see CLAUDE.md: the ISBN
table, the Vol IV footer block). An index that says "this file is orphaned" is a
positive claim someone will act on, so it has to be regenerated, not maintained.

Run it after adding or moving any page:

    python3 tools/build_indexes.py

CRAWLER CORRECTNESS — the four things a naive version gets wrong
----------------------------------------------------------------
1. Generated indexes must be EXCLUDED as link sources. master-index.html links to
   every file in the repo; count it and the orphan column reads zero forever.
2. Links resolve by PATH, not basename. `ch-tatiana.html` and `ch6-resonance.html`
   each exist twice (root and a subfolder); basename matching credits links to the
   wrong copy and mislabels a live page as orphaned, and vice versa.
3. Site-absolute hrefs (`/geometry/ch07-four-orbits.html`) are real links.
4. Some nav is built in JavaScript, so `.html` string literals inside <script>
   blocks count too.

Titles are unescaped from the source <title> and re-escaped exactly once; escaping
twice renders a literal "&middot;" on the page.
"""

from __future__ import annotations

import html
import posixpath
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (output suffix, display name, predicate on the posix path)
FOLDERS: list[tuple[str, str, str]] = [
    ("book1", "Book I — Mathematics of Generative Transitions", "book1"),
    ("book2", "Book II — Contact Realization", "book2"),
    ("book3", "Book III — The Mini-Beast", "book3"),
    ("book4", "Book IV — GTCT / Newark", "book4"),
    ("book5", "Book V — AXLE", "book5"),
    ("book6", "Book VI — Working Papers & Applications", "book6"),
    ("book7", "Book VII — The Scientists", "book7"),
    ("book8", "Book VIII — Cosmological / Quantum", "book8"),
    ("omega", "Omega Point", "omega"),
    ("HVEH", "HVEH", "HVEH"),
    ("AMonster", "A Monster's Law", "AMonster"),
    ("Orthogenesis", "Orthogenesis", "Orthogenesis"),
    ("book", "Book (misc/legacy)", "book"),
    ("root", "Root — Standalone Chapters", ""),
    ("_archive", "Archive (legacy)", "_archive"),
]

HREF = re.compile(r'href\s*=\s*["\']([^"\'#?]+)', re.I)
JSREF = re.compile(r'["\']([A-Za-z0-9_\-./]+\.html)["\']')
SCRIPT = re.compile(r"<script\b.*?</script>", re.S | re.I)
TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
H1 = re.compile(r"<h1[^>]*>(.*?)</h1>", re.S | re.I)


def generated_names() -> set[str]:
    """Index files this script owns — never counted as link sources."""
    return {"master-index.html"} | {f"index-{slug}.html" for slug, _, _ in FOLDERS}


def discover() -> list[str]:
    out = []
    skip = generated_names()
    for p in ROOT.rglob("*.html"):
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith(".git/") or "/.git/" in rel:
            continue
        # _to_delete/ holds files retired by hand; device_bash cannot unlink, so they
        # sit on disk until the author removes the folder. They are gitignored and are
        # not part of the site — indexing them reports retired pages as live orphans.
        if rel.startswith("_to_delete/") or "/_to_delete/" in rel:
            continue
        if rel in skip:
            continue
        out.append(rel)
    return sorted(out)


def text_of(raw: str) -> str:
    """Strip tags, unescape entities once, collapse whitespace."""
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", raw))).strip()


def title_of(src: str, rel: str) -> str:
    for pat in (TITLE, H1):
        m = pat.search(src)
        if m:
            t = text_of(m.group(1))
            if t:
                return t
    return posixpath.basename(rel)


def crawl(files: list[str]) -> tuple[dict[str, int], dict[str, str]]:
    known = set(files)
    inbound: dict[str, set[str]] = {f: set() for f in files}
    titles: dict[str, str] = {}

    def resolve(target: str, base_dir: str) -> str | None:
        if target.startswith(("http://", "https://", "mailto:", "javascript:", "data:", "//", "#")):
            return None
        if target.startswith("/geometry/"):
            target = target[len("/geometry/"):]
        elif target.startswith("/"):
            target = target[1:]
        else:
            target = posixpath.join(base_dir, target)
        target = posixpath.normpath(target)
        return target if target in known else None

    for rel in files:
        src = (ROOT / rel).read_text(encoding="utf-8", errors="replace")
        titles[rel] = title_of(src, rel)
        base = posixpath.dirname(rel)
        for t in HREF.findall(src):
            r = resolve(t, base)
            if r and r != rel:
                inbound[r].add(rel)
        for block in SCRIPT.findall(src):
            for t in JSREF.findall(block):
                r = resolve(t, base)
                if r and r != rel:
                    inbound[r].add(rel)

    return {k: len(v) for k, v in inbound.items()}, titles


def bucket(rel: str) -> str:
    top = rel.split("/")[0] if "/" in rel else ""
    for slug, _, prefix in FOLDERS:
        if prefix and top == prefix:
            return slug
    return "root"


CSS = """
:root{
  --bg:#14110d; --surface:#1c1710; --surface2:#241d13;
  --text:#ecdfc4; --muted:#a2937a; --clay:#c1613b; --clay-dim:#8a4630;
  --moss:#7a9471; --amber:#d2a24c; --line:#332a1c;
}
*{box-sizing:border-box}
body{margin:0; background:var(--bg); color:var(--text);
  font-family:Georgia,'Iowan Old Style','Palatino Linotype',serif; line-height:1.5;}
.mono{font-family:ui-monospace,'SFMono-Regular',Menlo,Consolas,monospace}
header.top{padding:3rem 1.5rem 2rem; border-bottom:1px solid var(--line);
  background:linear-gradient(180deg,var(--surface2),var(--bg));}
.eyebrow{text-transform:uppercase; letter-spacing:.14em; font-size:.72rem;
  color:var(--clay); font-family:ui-monospace,monospace; margin:0 0 .6rem;}
h1{font-size:clamp(1.8rem,4vw,2.6rem); margin:0 0 .4rem; font-weight:400; letter-spacing:-.01em;}
.sub{color:var(--muted); font-size:.98rem; max-width:56ch; margin:0 0 1.6rem;}
.stats{display:flex; gap:2rem; flex-wrap:wrap; margin-top:1.2rem;}
.stat b{display:block; font-size:1.9rem; color:var(--text); font-weight:400;}
.stat span{display:block; font-size:.72rem; color:var(--muted); text-transform:uppercase;
  letter-spacing:.08em; font-family:ui-monospace,monospace;}
.searchwrap{position:sticky; top:0; z-index:5; background:var(--bg);
  padding:1rem 1.5rem; border-bottom:1px solid var(--line);}
input[type=search]{width:100%; max-width:640px; padding:.7rem 1rem; border-radius:3px;
  border:1px solid var(--line); background:var(--surface); color:var(--text);
  font-family:ui-monospace,monospace; font-size:.95rem;}
input[type=search]:focus{outline:2px solid var(--clay); outline-offset:1px;}
main{padding:0 1.5rem 4rem; max-width:920px; margin:0 auto;}
.group{margin-top:2.4rem;}
.group h2{font-size:.78rem; text-transform:uppercase; letter-spacing:.1em; color:var(--clay);
  font-family:ui-monospace,monospace; font-weight:400; border-bottom:1px solid var(--line);
  padding-bottom:.5rem; margin-bottom:.2rem;}
.row{display:flex; align-items:baseline; justify-content:space-between; gap:1rem;
  padding:.65rem 0; border-bottom:1px solid var(--line);}
.row a{color:var(--text); text-decoration:none; font-size:1.02rem;}
.row a:hover{color:var(--clay);}
.row .path{color:var(--muted); font-size:.78rem; margin-left:.6rem;}
.tag{font-family:ui-monospace,monospace; font-size:.68rem; padding:.15rem .5rem;
  border-radius:2px; white-space:nowrap; flex-shrink:0;}
.tag.orphan{background:rgba(210,162,76,.14); color:var(--amber); border:1px solid rgba(210,162,76,.35);}
.tag.linked{background:rgba(122,148,113,.12); color:var(--moss); border:1px solid rgba(122,148,113,.25);}
.hidden{display:none !important;}
.empty{color:var(--muted); padding:2rem 0; font-style:italic; display:none;}
footer{padding:2rem 1.5rem 3rem; color:var(--muted); font-size:.8rem; max-width:920px; margin:0 auto;}
a.back{color:var(--clay); text-decoration:none; font-family:ui-monospace,monospace; font-size:.82rem;}
.folderlinks{display:flex; flex-wrap:wrap; gap:.5rem 1.2rem; margin:1.4rem 0 0;}
.folderlink{color:var(--text); text-decoration:none; font-size:.85rem;
  border-bottom:1px dotted var(--line); padding-bottom:2px;}
.folderlink:hover{color:var(--clay); border-color:var(--clay);}
.toggles{margin-top:1rem; display:flex; align-items:center; gap:.5rem;
  font-family:ui-monospace,monospace; font-size:.85rem; color:var(--muted);}
.toggles input{accent-color:var(--amber);}
"""

JS = """
(function(){
  var q=document.getElementById('q'), only=document.getElementById('orphans-only');
  var rows=[].slice.call(document.querySelectorAll('.row'));
  var groups=[].slice.call(document.querySelectorAll('.group'));
  var empty=document.querySelector('.empty');
  function apply(){
    var term=(q.value||'').trim().toLowerCase();
    var orphansOnly=only&&only.checked, shown=0;
    rows.forEach(function(r){
      var ok=(!term||r.dataset.hay.indexOf(term)!==-1)&&(!orphansOnly||r.dataset.orphan==='1');
      r.classList.toggle('hidden',!ok); if(ok)shown++;
    });
    groups.forEach(function(g){
      var any=g.querySelector('.row:not(.hidden)');
      g.classList.toggle('hidden',!any);
    });
    if(empty)empty.style.display=shown?'none':'block';
  }
  q.addEventListener('input',apply);
  if(only)only.addEventListener('change',apply);
})();
"""


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def row_html(rel: str, title: str, n: int, prefix: str = "") -> str:
    orphan = n == 0
    hay = esc(f"{title} {rel}".lower())
    tag = ('<span class="tag orphan">orphaned</span>' if orphan else
           f'<span class="tag linked">{n} link{"" if n == 1 else "s"}</span>')
    return (f'<div class="row" data-hay="{hay}" data-orphan="{"1" if orphan else "0"}">\n'
            f'  <a href="{esc(prefix + rel)}">{esc(title)}'
            f'<span class="path mono">{esc(rel)}</span></a>\n  {tag}\n</div>')


def page(title: str, eyebrow: str, heading: str, sub: str, stats: str,
         extra: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<style>{CSS}</style>
</head><body>
<header class="top">
  <p class="eyebrow">{eyebrow}</p>
  <h1>{esc(heading)}</h1>
  <p class="sub">{sub}</p>
  <div class="stats">{stats}</div>
  {extra}
</header>
<div class="searchwrap">
  <input type="search" id="q" placeholder="Search by title or filename&hellip;" autocomplete="off">
  <div class="toggles"><label><input type="checkbox" id="orphans-only"> show orphaned only</label></div>
</div>
<main>
{body}
<p class="empty">No files match that search.</p>
</main>
<footer>
  Generated {date.today().isoformat()} by <span class="mono">tools/build_indexes.py</span>
  from a filesystem crawl &mdash; not from the hand-built nav. Re-run it after adding or
  moving pages; these counts are derived and go stale on their own.<br>
  Principia Orthogona &middot; G6 LLC &middot; Pablo Nogueira Grossi &middot; Newark NJ &middot; 2026 &middot;
  <a class="back" href="https://zenodo.org/communities/principia-orthogona">Zenodo community</a>
</footer>
<script>{JS}</script>
</body></html>
"""


def main() -> None:
    files = discover()
    counts, titles = crawl(files)

    groups: dict[str, list[str]] = {slug: [] for slug, _, _ in FOLDERS}
    for rel in files:
        groups[bucket(rel)].append(rel)

    total = len(files)
    orphans = sum(1 for f in files if counts[f] == 0)
    names = {slug: name for slug, name, _ in FOLDERS}

    # ---- per-folder indexes -------------------------------------------------
    for slug, name, _ in FOLDERS:
        members = sorted(groups[slug], key=lambda r: titles[r].lower())
        n_orph = sum(1 for m in members if counts[m] == 0)
        rows = "\n".join(row_html(m, titles[m], counts[m]) for m in members)
        body = f'<div class="group"><h2>{esc(name)}</h2>\n{rows}\n</div>'
        stats = (f'<div class="stat"><b>{len(members)}</b><span>files</span></div>'
                 f'<div class="stat"><b style="color:var(--amber)">{n_orph}</b><span>orphaned</span></div>')
        (ROOT / f"index-{slug}.html").write_text(page(
            f"{name} · Index · Principia Orthogona",
            "totogt.github.io/geometry &middot; folder index", name,
            "Every HTML file in this folder, generated from the filesystem. "
            "Amber tags mark files with zero inbound links from anywhere in the repo.",
            stats, '<div class="folderlinks">'
                   '<a href="master-index.html" class="folderlink">&larr; Master index</a></div>',
            body), encoding="utf-8")

    # ---- master -------------------------------------------------------------
    links = "".join(
        f'<a href="index-{slug}.html" class="folderlink">{esc(names[slug])} '
        f'<span class="mono" style="color:var(--muted)">({len(groups[slug])}, '
        f'{sum(1 for m in groups[slug] if counts[m] == 0)} orphaned)</span></a>'
        for slug, _, _ in FOLDERS)

    blocks = []
    for slug, name, _ in FOLDERS:
        members = sorted(groups[slug], key=lambda r: titles[r].lower())
        if not members:
            continue
        rows = "\n".join(row_html(m, titles[m], counts[m]) for m in members)
        blocks.append(
            f'<div class="group"><h2>{esc(name)} &nbsp;<span class="mono" '
            f'style="color:var(--muted); text-transform:none; letter-spacing:0;">&mdash; '
            f'<a href="index-{slug}.html" style="color:var(--clay)">open folder index</a>'
            f'</span></h2>\n{rows}\n</div>')

    stats = (f'<div class="stat"><b>{total}</b><span>total files</span></div>'
             f'<div class="stat"><b style="color:var(--amber)">{orphans}</b><span>orphaned</span></div>'
             f'<div class="stat"><b>{len(FOLDERS)}</b><span>books / folders</span></div>')
    (ROOT / "master-index.html").write_text(page(
        "Master Index · geometry · Principia Orthogona",
        "totogt.github.io/geometry &middot; full repo crawl", "Master Index",
        f"Every HTML file in the geometry repo, generated directly from the filesystem "
        f"&mdash; not the hand-built nav. Search across all {total} chapters, papers and "
        f"pages at once. Amber tags mark files with zero inbound links from anywhere else "
        f"in the repo; the generated indexes themselves are excluded as link sources, so "
        f"they cannot mask an orphan.",
        stats, f'<div class="folderlinks">{links}</div>', "\n".join(blocks)), encoding="utf-8")

    print(f"{total} files, {orphans} orphaned, {len(FOLDERS) + 1} pages written")
    for slug, _, _ in FOLDERS:
        print(f"  index-{slug}.html  {len(groups[slug]):>4} files, "
              f"{sum(1 for m in groups[slug] if counts[m] == 0):>3} orphaned")


if __name__ == "__main__":
    main()
