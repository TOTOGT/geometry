#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
ch06b-verify.py -- ch06b-an-essay-and-a-result.html (English for Researchers, outside the weekly plan).
  [1] sections S1..S8 and S4m present   [2] every local link resolves
  [3] the mathematics on the page recomputes: the Sidon example, b_5, b_28, the bound table, no sixth mark in 12..16
  [4] the numbers quoted from arXiv 2610.36207 match the paper's text, IF the PDF is in ~/Downloads (else SKIP)
  [5] the essay's address and date are stated (its text is not held here: SKIP, never PASS)
  [6] controls: each check is shown to fail on a broken input (R24)
  [HONESTY] what this does not establish
"""
import re, sys, math, subprocess, hashlib, glob, os
from pathlib import Path
HERE = Path(__file__).resolve().parent
PAGE = HERE / "ch06b-an-essay-and-a-result.html"
fails, skips = [], []
def check(ok, msg, detail=""):
    print("    %s  %s%s" % ("PASS" if ok else "FAIL", msg, ("  -- " + detail) if (detail and not ok) else ""))
    if not ok: fails.append(msg)
def skip(msg):
    print("    SKIP  " + msg); skips.append(msg)
def head(n, t): print("\n" + "=" * 72 + "\n  [%s]  %s\n" % (n, t) + "=" * 72)

def plain(h):
    h = re.sub(r"<script.*?</script>|<style.*?</style>", "", h, flags=re.S)
    h = re.sub(r"<[^>]+>", " ", h)
    for a, b in (("&nbsp;", " "), ("&rsquo;", "'"), ("&ldquo;", '"'), ("&rdquo;", '"'), ("&minus;", "-"), ("&sup2;", "2"),
                 ("&asymp;", "~"), ("&radic;", "sqrt"), ("&ge;", ">="), ("&middot;", "."), ("&alpha;", "a"), ("&beta;", "b"),
                 ("&upsilon;", "u"), ("&odblac;", "o"), ("&aacute;", "a"), ("&amp;", "&")):
        h = h.replace(a, b)
    return re.sub(r"\s+", " ", h)

def sections(html): return [x for x in ["S1","S2","S3","S4","S4m","S5","S6","S7","S8"] if 'id="%s"' % x in html]
def local_links(html):
    out = []
    for h in re.findall(r'href="([^"#]+)"', html):
        if re.match(r"https?:|mailto:|/", h): continue
        out.append(h)
    return out
def is_sidon(r):
    d = [b - a for i, a in enumerate(r) for b in r[i + 1:]]
    return len(d) == len(set(d)), d
def cor11(k): return k * k * (1 / (1 + 0.945 / math.sqrt(k)) - 0.945 / math.sqrt(k)) - 1
def simple(k): return k * k - 1.89 * k ** 1.5

html = PAGE.read_text(encoding="utf-8")
txt = plain(html)

head(1, "SECTIONS")
check(sections(html) == ["S1","S2","S3","S4","S4m","S5","S6","S7","S8"], "sections S1..S8 and S4m all present")
check(len(re.findall(r"<table class=\"cmp\">", html)) == 4, "four tables: essay, result, side by side, bound table")

head(2, "LOCAL LINKS RESOLVE")
ll = local_links(html)
miss = [l for l in ll if not (HERE / l).exists()]
check(len(ll) >= 10 and not miss, "%d local links, none missing" % len(ll), ", ".join(miss))

head(3, "THE MATHEMATICS ON THE PAGE, RECOMPUTED")
ok, d = is_sidon([0, 1, 4, 9, 11])
check(ok and sorted(d) == [1, 2, 3, 4, 5, 7, 8, 9, 10, 11], "{0,1,4,9,11} is a Sidon set; its ten differences are 1..11 without 6")
check(not is_sidon([0, 1, 2, 3])[0], "{0,1,2,3} is not (1-0 = 2-1)")
b5 = (25 - 11) / 5 ** 1.5
check(abs(b5 - 1.252) < 5e-4 and "1.252" in txt, "b_5 = (25-11)/5^(3/2) = %.4f, printed 1.252" % b5)
check(abs(28 ** 1.5 - 56 * math.sqrt(7)) < 1e-9, "28^(3/2) = 56*sqrt(7)")
check(abs(199 / (56 * math.sqrt(7)) - 1.343) < 5e-4 and 28 * 28 - 199 == 585, "b_28 = 199/(56 sqrt 7) = %.4f, and 784 - 199 = 585" % (199 / (56 * math.sqrt(7))))
rows = {5: (6.0, 3.9), 28: (524.2, 504.0)}
for k, (c, s_) in rows.items():
    check(round(cor11(k), 1) == c and round(simple(k), 1) == s_ and ("%.1f" % c) in txt and ("%.1f" % s_) in txt,
          "k=%d: Corollary 1.1 form %.1f, simplified %.1f, both printed" % (k, c, s_))
check(5 and 11 >= cor11(5) and 585 >= cor11(28), "the true diameters 11 and 585 sit above the bound at k = 5 and 28")
ext = [m for m in range(12, 17) if is_sidon([0, 1, 4, 9, 11, m])[0]]
check(ext == [], "no sixth mark among 12..16 keeps the differences distinct (task 2)")
ext2 = next(m for m in range(12, 100) if is_sidon([0, 1, 4, 9, 11, m])[0])
print("          (the first mark that does work after 11 is %d; not printed on the page)" % ext2)
ab = 2 * math.sqrt(0.944814 * 0.941259)
check(abs(ab - 1.88607) < 2e-5, "2*sqrt(alpha*beta) from the printed (0.944814, 0.941259) = %.5f ~ 1.88607 (inputs rounded to 6 places)" % ab)

head(4, "THE PAPER'S TEXT, IF THE PDF IS ON THIS MACHINE")
cands = sorted(glob.glob(os.path.expanduser("~/Downloads/*2610.36207*.pdf")))
NEEDLES = ["1.88607", "0.945", "483", "0.944814", "0.941259", "Corollary 1.1", "AlphaEvolve", "Claude Opus", "Claude Sonnet", "199"]
if not cands:
    skip("arXiv 2610.36207 PDF not in ~/Downloads; the quoted numbers were not checked against the paper by this run")
else:
    try:
        t = subprocess.run(["pdftotext", "-layout", cands[0], "-"], capture_output=True, text=True, timeout=60).stdout
        flat = re.sub(r"\s+", " ", t)
        bad = [n for n in NEEDLES if n not in flat]
        check(not bad, "the paper's text contains every needle the page relies on", ", ".join(bad))
        print("          source md5 %s" % hashlib.md5(open(cands[0], "rb").read()).hexdigest())
    except Exception as e:
        skip("pdftotext failed (%s)" % e.__class__.__name__)

head(5, "THE ESSAY")
check("tammykolda.substack.com/p/what-ai-has-done-to-math-an-illustrated" in html and "3 November 2026" in html, "the essay's address and date are stated")
skip("the essay's text is not held in this repository; its description on the page was not machine-checked")
quotes = re.findall(r"&ldquo;(.*?)&rdquo;", html)
kolda_like = [q for q in quotes if "up to us" in q]
check(len(kolda_like) == 1 and len(kolda_like[0].split()) <= 15, "the essay is quoted once, in under 15 words")

head(6, "CONTROLS (each check must be able to fail)")
check(sections(html.replace('id="S4m"', 'id="XX"')) != ["S1","S2","S3","S4","S4m","S5","S6","S7","S8"], "control: a missing section is detected")
bad_html = html.replace('href="ch06-argument.html"', 'href="no-such-page-ch06b.html"')
check(set(l for l in local_links(bad_html) if not (HERE / l).exists()) == {"no-such-page-ch06b.html"}, "control: a broken local link is detected")
check(not is_sidon([0, 1, 2, 3])[0] and not is_sidon([0, 1, 4, 9, 11, 15])[0], "control: repeated differences are detected ({0,1,2,3}; 15 added to the ruler)")
check(abs(2 * math.sqrt(0.9 * 0.94) - 1.88607) > 2e-5, "control: a wrong alpha makes the 1.88607 check fail")
bad_txt = txt.replace("524.2", "530.0")
check(not (("%.1f" % rows[28][0]) in bad_txt), "control: a wrong table entry (530.0 for 524.2) is detected by the printed-number check")

print("\n[HONESTY] This script does not verify any theorem. It recomputes the arithmetic on the page, checks that the page's links resolve,")
print("          and, only when the PDF is in ~/Downloads, that the numbers quoted from the paper appear in its text.")
print("          The essay's text is not held here; its description is the author's reading of 2026-11-09, not a machine check.")
print("          That 585 is the shortest known 28-mark ruler is an outside fact; only the arithmetic from the paper's b_28 is checked.")
print("\n%s  (%d skipped)" % ("all run checks passed." if not fails else "FAILED: %d" % len(fails), len(skips)))
sys.exit(1 if fails else 0)
