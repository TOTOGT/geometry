#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Find chapters colonised by an off-topic section.

A chapter should stay on its subject and hand other subjects to their own
chapters. The signature of the failure is measurable: one section dominates the
page, and its vocabulary has little to do with the page's title.

    python3 tools/section_balance.py [--share 0.28] [--min-sections 3]

Reports, per page: the largest section's share of body text, and how many content
words its heading shares with the page title. High share + zero overlap is the
shape of a chapter that has grown a second essay.
"""
import argparse, io, os, re

SKIP = {".git", "_to_delete", ".lake", "verify-audit", "node_modules", "_archive"}
STOP = set("the a an of and or in on to for as at by with from is are was were be been "
           "this that these those it its what which who how why when where not no "
           "chapter section vol volume book part one two three four five".split())
HEAD = re.compile(r'<h2[^>]*>(.*?)</h2>|<span class="section-label">(.*?)</span>', re.S | re.I)


def words(t):
    return {w for w in re.findall(r"[a-z]{4,}", t.lower()) if w not in STOP}


def strip(h):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--share", type=float, default=0.28)
    ap.add_argument("--min-sections", type=int, default=3)
    ap.add_argument("--root", default=".")
    a = ap.parse_args()

    out = []
    for dp, dn, fn in os.walk(a.root):
        dn[:] = [d for d in dn if d not in SKIP]
        for f in sorted(fn):
            if not f.endswith(".html") or f.startswith(("index", "master-index")):
                continue
            path = os.path.relpath(os.path.join(dp, f), a.root)
            html = io.open(os.path.join(dp, f), encoding="utf-8", errors="replace").read()
            tm = re.search(r"<title>(.*?)</title>", html, re.S)
            title = strip(tm.group(1)) if tm else path
            body = html[html.find("<body"):]
            marks = [(m.start(), strip(m.group(1) or m.group(2) or "")) for m in HEAD.finditer(body)]
            if len(marks) < a.min_sections:
                continue
            segs = []
            for k, (pos, lab) in enumerate(marks):
                end = marks[k + 1][0] if k + 1 < len(marks) else len(body)
                n = len(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body[pos:end])))
                if lab and not re.match(r"^(references?|notes?|bibliograph)", lab, re.I):
                    segs.append((lab, n))
            tot = sum(n for _, n in segs)
            if tot < 4000 or not segs:
                continue
            # Size is not the signal: "Exercises" should dominate a teaching chapter.
            # The signal is TOPIC DIVERGENCE - the dominant section talking about
            # something the rest of the page does not talk about.
            idx = max(range(len(segs)), key=lambda i: segs[i][1])
            lab, n = segs[idx]
            share = n / tot
            if share < a.share:
                continue
            spans = []
            for k, (pos, _l) in enumerate(marks):
                end = marks[k + 1][0] if k + 1 < len(marks) else len(body)
                spans.append(re.sub(r"<[^>]+>", " ", body[pos:end]))
            keep = [sp for (l, _), sp in zip(segs, spans[:len(segs)])]
            dom = words(keep[idx]) if idx < len(keep) else set()
            rest = set()
            for i, sp in enumerate(keep):
                if i != idx:
                    rest |= words(sp)
            if not dom:
                continue
            novel = len(dom - rest) / len(dom)      # share of its words found nowhere else
            overlap = len(words(lab) & words(title))
            if novel < 0.45:
                continue
            out.append((share, overlap, path, lab, len(segs), novel))

    out.sort(key=lambda r: -(r[0] * r[5]))
    print("%-5s %-6s %-4s %s" % ("share", "novel", "olap", "page / dominant section"))
    for share, ov, path, lab, k, nv in out[:20]:
        print("%4.0f%% %5.0f%% %4d  %s\n                     %s" % (share*100, nv*100, ov, path, lab[:70]))
    print("\n%d pages: one section >= %.0f%% of the body AND >= 45%% of its vocabulary"
          % (len(out), a.share * 100))
    print("appearing nowhere else on the page. Size alone is not the signal; divergence is.")


if __name__ == "__main__":
    main()
