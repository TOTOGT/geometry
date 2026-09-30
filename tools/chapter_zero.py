#!/usr/bin/env python3
"""chapter_zero.py — generate "Chapter 0 · Definitions and Notation" for Books I–X.

Mechanism: reads docs/definitions.md (the one source, CLAUDE.md R28), and for each
book writes <bookdir>/ch00-definitions.html listing the rows that book actually
uses (a row is kept when its keywords occur on at least one page of that book),
plus <bookdir>/ch00-verify.py (R6). Pages are GENERATED (R8): edit the table in
docs/definitions.md, never the page.

  python3 tools/chapter_zero.py --write     write all ten pages
  python3 tools/chapter_zero.py --check     exit 1 if any page is missing or stale
  python3 tools/chapter_zero.py --write --book 4
Existing Chapter 0 pages (book4/ch00-student-edition.html, book5/ch00.html) are
onboarding pages and are left alone; this page sits beside them.
"""
import argparse, glob, hashlib, html, os, re, sys
from datetime import datetime
try:
    from zoneinfo import ZoneInfo
    TODAY = datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d")   # R2: desk-local date
except Exception:
    TODAY = datetime.now().strftime("%Y-%m-%d")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "docs", "definitions.md")

# number -> (dir, root index page, title, extra root pages that belong to the book)
BOOKS = {
 1: ("book1",  "index-book1.html",  "Book I · GOMC — Operator Algebra", ["vol1-mathematics.html"]),
 2: ("book2",  "index-book2.html",  "Book II · TOGT — Contact Geometry", ["vol2-contact.html", "vol2-toymodel.html"]),
 3: ("book3",  "index-book3.html",  "Book III · The Mini-Beast", []),
 4: ("book4",  "index-book4.html",  "Book IV · GTCT — Formal Theory", []),
 5: ("book5",  "index-book5.html",  "Book V · The Seed — Completeness", []),
 6: ("book6",  "index-book6.html",  "Book VI · Roots", []),
 7: ("book7",  "index-book7.html",  "Book VII · The Scientists", []),
 8: ("book8",  "index-book8.html",  "Book VIII · Dark Matter, Monster Group, Moonshine, Embryogenesis", []),
 9: ("omega",  "index-omega.html",  "Book IX · Omega Point — The Convergence Series", []),
 10:("book10", "index-book10.html", "Book X · Custody, Transmission, and the Continent", []),
}

# first-column symbol (as written in definitions.md) -> keyword regex searched in the book's pages
KEYS = {
 "ε₀": r"ε₀|ε0|ε\*|epsilon_?0|Gronwall|stability radius",
 "B(Γ)": r"basin of attraction|Gronwall basin|inner basin|outer basin|escape region",
 "r*": r"r\*|r\^\\star|r\^\{\\star\}|inner[- ]boundary|0\.7759|fold threshold",
 "r_s": r"saddle (?:equilibrium|root|cubic)|2 ?cos\(3π/7\)",
 "μ_max": r"μ_?max|µmax|\\mu_\{?\\max|Lyapunov exponent",
 "τ": r"embodiment threshold|τ ?= ?2|\\tau ?= ?2|stochastic Lyapunov",
 "τ normalization": r"embodiment threshold|τ ?= ?2|\\tau ?= ?2|stochastic Lyapunov",
 "τ₁₂": r"τ₁₂|\\tau_\{?12|unification",
 "κ*": r"κ\*|κ∗|\\kappa\^\*|critical curvature|curvature threshold",
 "κ chain": r"κ chain|Pythagorean",
 "W(Γ)": r"winding",
 "C, K, F, U": r"operator chain|U ?∘ ?F ?∘ ?K ?∘ ?C|Compression|Unfolding",
 "U family": r"unification operator|U₃|U_3|Unfold operator|unfolding U|U selects",
 "dm³ system": r"dm³|dm\$?\^?\{?3|dm3",
}

def split_cells(line):
    line = line.strip()
    if line.startswith("|"): line = line[1:]
    if line.endswith("|") and not line.endswith("\\|"): line = line[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", line)]

def parse(md):
    sections, cur = [], None
    for line in md.split("\n"):
        if line.startswith("## "):
            cur = {"title": line[3:].strip(), "rows": [], "prose": []}; sections.append(cur); continue
        if cur is None: continue
        if line.startswith("|"):
            cells = split_cells(line)
            if not cells or set("".join(cells)) <= set("-: "): continue
            if cells[0] in ("Symbol",): continue
            if len(cells) >= 4: cur["rows"].append(cells[:4])
        elif line.strip(): cur["prose"].append(line.strip())
    return sections

def fmt(text):
    t = text.replace("\\*", "\u0001").replace("\\|", "\u0002")
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\*(.+?)\*", r"<em>\1</em>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    return t.replace("\u0001", "*").replace("\u0002", "|")

def badge(status):
    s = status.upper()
    good = any(k in s for k in ("DECIDED", "VERIFIED", "DEFINED"))
    if "OPEN" in s and not good: return "open"
    if "OPEN" in s: return "mixed"
    return "ok"

def book_pages(n):
    d, _, _, extra = BOOKS[n]
    files = sorted(glob.glob(os.path.join(ROOT, d, "*.html")))
    files = [f for f in files if os.path.basename(f) != "ch00-definitions.html"]
    files += [os.path.join(ROOT, e) for e in extra if os.path.exists(os.path.join(ROOT, e))]
    return files

def page_texts(n):
    out = []
    for f in book_pages(n):
        try: out.append(open(f, encoding="utf-8", errors="ignore").read())
        except OSError: pass
    return out

CSS = """:root{--navy:#1a2744;--gold:#c9a84c;--cream:#faf7f0;--smoke:#f0ece4;--mid:#3a4f7a;--rule:#8a7340;--text:#1c1c1c;--light:#e8e2d4;--teal:#1a5c5c;--amber:#9a5b00}
*{box-sizing:border-box;margin:0;padding:0}body{font-family:'EB Garamond',Georgia,serif;color:var(--text);background:var(--cream);line-height:1.7;font-size:17px}
nav{background:var(--navy);padding:.75rem 2rem;display:flex;gap:1rem;flex-wrap:wrap;align-items:center;justify-content:space-between}
nav a{color:var(--gold);text-decoration:none;font-family:sans-serif;font-size:.85rem;letter-spacing:.08em}
.hero{background:var(--navy);color:#fff;padding:3rem 2rem 2.4rem}.hero-inner,main{max-width:980px;margin:0 auto}
.eyebrow{font-family:sans-serif;font-size:.72rem;letter-spacing:.2em;color:var(--gold);text-transform:uppercase;margin-bottom:.7rem}
h1{font-size:clamp(1.7rem,4vw,2.6rem);line-height:1.15}h2{color:var(--navy);margin:2.2rem 0 .8rem;border-bottom:1px solid var(--light);padding-bottom:.3rem}
main{padding:1.6rem 1.4rem 3rem}p{margin:.6rem 0}.lede{color:#dcd6c6;margin-top:.8rem;max-width:720px}
table{border-collapse:collapse;width:100%;margin:.8rem 0 1.4rem;font-size:.93rem;background:#fff}
th,td{border:1px solid var(--light);padding:.55rem .65rem;vertical-align:top;text-align:left}th{background:var(--smoke);font-family:sans-serif;font-size:.74rem;letter-spacing:.08em;text-transform:uppercase}
td.sym{font-weight:600;white-space:nowrap}
.chip{display:inline-block;padding:.12rem .5rem;border-radius:3px;font-family:sans-serif;font-size:.72rem;letter-spacing:.04em;white-space:nowrap}
.chip.ok{background:#dff1ec;color:var(--teal)}.chip.open{background:#fbead0;color:var(--amber)}.chip.mixed{background:#ece6f6;color:#4a3c78}
.legend{font-family:sans-serif;font-size:.8rem;color:#555;margin:.8rem 0}.gen{font-family:sans-serif;font-size:.74rem;color:#777;margin-top:2rem}
code{background:var(--smoke);padding:0 .25rem;font-size:.9em}.skip{font-size:.92rem;color:#555}
footer{background:var(--navy);color:#bbb;padding:1.2rem 2rem;font-family:sans-serif;font-size:.74rem}footer a{color:var(--gold)}
@media(max-width:640px){td.sym{white-space:normal}table{font-size:.85rem}nav{padding:.6rem 1rem}}"""

def render(n, sections, sha):
    d, idx, title, _ = BOOKS[n]
    texts = page_texts(n)
    pat = {k: re.compile(v, re.I) for k, v in KEYS.items()}
    body, kept, dropped = [], 0, []
    for sec in sections:
        if not sec["rows"]: continue
        rows = []
        for sym, defi, status, notes in sec["rows"]:
            rx = pat.get(sym.replace("\\*", "*"))
            hits = sum(1 for t in texts if rx.search(t)) if rx else len(texts)
            if rx is not None and hits == 0:
                dropped.append(sym.replace("\\*", "*")); continue
            kept += 1
            use = "" if rx is None else f'<div class="skip">on {hits} page{"s" if hits != 1 else ""} of this book</div>'
            rows.append(f'<tr><td class="sym">{fmt(sym)}</td><td>{fmt(defi)}{use}</td>'
                        f'<td><span class="chip {badge(status)}">{fmt(status)}</span></td><td>{fmt(notes)}</td></tr>')
        if rows:
            body.append(f'<h2>{fmt(sec["title"])}</h2><table><tr><th>Symbol</th><th>Definition</th><th>Status</th><th>Notes</th></tr>{"".join(rows)}</table>')
    tail = next((s for s in sections if not s["rows"] and s["prose"]), None)
    if tail:
        body.append(f'<h2>{fmt(tail["title"])}</h2>' + "".join(f"<p>{fmt(p)}</p>" for p in tail["prose"]))
    if not kept:
        body.insert(0, '<p>No symbol from the framework table appears on a page of this book. The full table lives in '
                       '<code>docs/definitions.md</code> and in the other books\' Chapter 0.</p>')
    note = (f'<p class="skip">Rows that do not occur anywhere in this book are left out: {", ".join(html.escape(x) for x in dropped)}.</p>'
            if dropped else "")
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<title>Ch 0 · Definitions and Notation — Principia Orthogona {html.escape(title.split(' · ')[0])}</title>
<!-- GENERATED by tools/chapter_zero.py from docs/definitions.md (sha1 {sha}). Edit the table, not this page. R28 / R8. -->
<style>{CSS}</style></head><body>
<nav><a href="../{idx}">⚜ PRINCIPIA ORTHOGONA · {html.escape(title.split(' · ')[0]).upper()} ⚜</a><a href="../series-hub.html">Series hub</a></nav>
<div class="hero"><div class="hero-inner"><div class="eyebrow">{html.escape(title)} · Chapter 0</div>
<h1>Definitions and Notation</h1>
<p class="lede">What each symbol means, who decided it, and whether a script has checked it. Rows marked open are not settled; they are shown so a reader can see what is still the author's call.</p></div></div>
<main>
<p class="legend"><span class="chip ok">DECIDED / VERIFIED / DEFINED</span> settled by the author, recomputed by a script, or defined in a paper &nbsp; <span class="chip mixed">mixed</span> part settled, part open &nbsp; <span class="chip open">OPEN</span> the author's call</p>
{''.join(body)}
{note}
<p class="gen">Generated {TODAY} from <code>docs/definitions.md</code> (sha1 {sha}) by <code>tools/chapter_zero.py</code>. Re-check the verified numbers with <code>python3 tools/chapter_zero_verify.py</code>. The Book 4 Student Edition and the Book 5 "How to Begin" chapter are orientation pages; this chapter is the reference.</p>
</main>
<footer>Principia Orthogona · {html.escape(title)} · © 2026 Pablo Nogueira Grossi · G6 LLC · ORCID 0009-0000-6496-2186 · <a href="https://zenodo.org/communities/principia-orthogona">Zenodo</a></footer>
</body></html>
"""

STUB = '''#!/usr/bin/env python3
"""ch00-verify.py — Chapter 0 (Definitions and Notation), {title}. Generated by tools/chapter_zero.py (R6)."""
import os, subprocess, sys
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.exit(subprocess.call([sys.executable, os.path.join(root, "tools", "chapter_zero_verify.py"), "--book", "{n}"]))
'''

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--write", action="store_true"); ap.add_argument("--check", action="store_true")
    ap.add_argument("--book", type=int); a = ap.parse_args()
    md = open(SRC, encoding="utf-8").read(); sha = hashlib.sha1(md.encode()).hexdigest()[:10]
    sections = parse(md); books = [a.book] if a.book else sorted(BOOKS); bad = 0
    for n in books:
        d = BOOKS[n][0]; out = os.path.join(ROOT, d, "ch00-definitions.html")
        page = render(n, sections, sha)
        if a.write:
            os.makedirs(os.path.join(ROOT, d), exist_ok=True)
            open(out, "w", encoding="utf-8").write(page)
            open(os.path.join(ROOT, d, "ch00-verify.py"), "w", encoding="utf-8").write(STUB.format(n=n, title=BOOKS[n][2]))
            print(f"wrote {d}/ch00-definitions.html  ({len(page)} bytes)")
        if a.check:
            ok = os.path.exists(out) and f"sha1 {sha}" in open(out, encoding="utf-8").read()
            print(("ok    " if ok else "STALE ") + f"{d}/ch00-definitions.html"); bad += (not ok)
    if not (a.write or a.check): ap.print_help()
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
