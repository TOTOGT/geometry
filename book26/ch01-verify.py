#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
ch01-verify.py -- what Book XXVI's index and Chapter 1 say about their own counts.

R6/R24. Checks, from the pages alone:
  [1] the table in index.html has the number of rows ch01 states (22)
  [2] every row carries a month in {Aug, Sep, Oct}; no row claims a sent status or an outcome
  [3] ch01's "roughly a dozen or more industries" is true of the table (>= 12 distinct, 'Not identified' excluded)
  [4] no employer is named: every word on both pages is hashed and compared with a list of hashed
      employer tokens (the names are kept as hashes so this file does not publish them)
  [5] no URL, email address or requisition-style number appears in the table
  [6] the internal links resolve
  [7] tags balance on both pages
Standard library only. Exit 0 iff every block holds. Control: --control feeds a page with an employer word and must exit 1.
"""
import hashlib, re, sys
from html.parser import HTMLParser
from pathlib import Path
H = Path(__file__).resolve().parent
EMPLOYER_HASHES = set({'a0196147fec6598d5d0c3a18bb14b3ce60c4b9ebfe9493ef1ed381d5e893fcb1', '004fc5646cea29f7660019b6dd21ed179c5ebda39965c0ea386e047312bf5069', '54c0bcab0e7334379ea4e9df9706f845ebcd39924b2d291fb78ebc82f1b4317b', '353bd6840895864cca12b11e247bb484cf574e6d5daf76dcbbb4c2a1fd93b805', '966ff20da19b3abb7c59a4f114755f5ff4efe2b65d6d129110711277446a6404', 'a691b6bc04f1996c0ae05aab9c29067fdbcd2d521788b728071b453b1efd840f', 'a744d93f2c6e8830a70b434113ecdebdaf568ba8c0557c63bd0914528760ae53', '08e95543598aa1973b844fb0f148818673b22101df84f6f68bf4f33c22163bf2', '63866302165d1f77ebe4a18e27d0181869e682d375f4d5c864d92cfc17c71f81', 'b8ea7b7963a0fa7baaf4d71f4f0dc75a42aa7e4e1f3a406c809ca5b16ac7e9ab', '75371f5a57ca5232c85c1858415de4b06f5c9e4bc879404e348748c273540986', '4cc4167597f9086cf2c7920cfd1e5aecfea52fc43d99354b6a04699ce0df4e3c', '8146e42cffe6289de974818f68206895f6ff86ce62c72c9455e18bc039582711', 'de6947ad9f13f32ff7dc7b75d0f8994012ac8613a56dc674bae7dfce872c654c', 'b66b59a6600e39bd55cf57edc93f137be5360da2b9a1d2609ed8ff8b95776dc2', 'a0b6832c136c62e43c63753495c1f67f8f328d174081e1c3f3ca5c18c98551f7'})
def words(t): return re.findall(r"[a-z][a-z']+", t.lower())
def text(s): return re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style)[^>]*>.*?</\1>", "", s, flags=re.S|re.I))
def leaks(s): return sorted({w for w in words(text(s)) if hashlib.sha256(w.encode()).hexdigest() in EMPLOYER_HASHES})
class P(HTMLParser):
    def __init__(s): super().__init__(); s.st=[]; s.bad=[]
    def handle_starttag(s,t,a):
        if t not in ("meta","link","br","hr","img","input"): s.st.append(t)
    def handle_endtag(s,t):
        if t=="meta": return
        if not s.st or s.st[-1]!=t: s.bad.append(t)
        else: s.st.pop()
def main():
    fails=[]
    def ok(c,m):
        print(("  ok   " if c else "  FAIL ")+m)
        if not c: fails.append(m)
    idx=(H/"index.html").read_text(encoding="utf8"); ch=(H/"ch01-two-conversations.html").read_text(encoding="utf8")
    if "--control" in sys.argv:
        idx=idx.replace("Local government","Local government Yale"); print("control: planted an employer word")
    rows=re.findall(r"<tr><td class=\"m\">(\w+)</td><td>(.*?)</td><td>(.*?)</td><td class=\"blank\">(.*?)</td><td class=\"blank\">(.*?)</td></tr>", idx)
    print("[1] row count"); n=len(rows); m=re.search(r"lists (\d+) applications", ch)
    ok(n==22, f"table has {n} rows"); ok(bool(m) and int(m.group(1))==n, f"ch01 states {m.group(1) if m else 'nothing'} and the table has {n}")
    print("[2] months and statuses")
    ok(all(r[0] in ("Aug","Sep","Oct") for r in rows), "every month is Aug, Sep or Oct")
    known=[r for r in rows if not (r[3]=="to confirm" and r[4]=="not recorded")]
    ok(all(r[3]=="yes" and r[4]=="not progressing (form letter)" for r in known) and len(known)==1 and known[0][2]=="Business manager",
       "exactly one row asserts an outcome: Business manager, sent 'yes', 'not progressing (form letter)'; every other row is 'to confirm' / 'not recorded'")
    ok("one outcome is recorded" in idx and "a blank is not a rejection" in idx, "index says one outcome is recorded and keeps 'a blank is not a rejection'")
    idx_no=idx.replace('<td class="blank">not progressing (form letter)</td>','<td class="blank">not recorded</td>')
    ok(not all(r[4]=="not recorded" for r in re.findall(r"<tr><td class=\"m\">(\w+)</td><td>(.*?)</td><td>(.*?)</td><td class=\"blank\">(.*?)</td><td class=\"blank\">(.*?)</td></tr>", idx)), "control: the asserted outcome is seen (not every row reads 'not recorded')")
    print("[3] industries")
    inds={r[1] for r in rows if not r[1].startswith("Not identified")}; ok(len(inds)>=12, f"{len(inds)} distinct industries named")
    print("[4] employer names"); L=leaks(idx)+leaks(ch); ok(not L, "no employer token found" if not L else "employer token(s) found: "+", ".join(L))
    print("[5] identifying strings in the table")
    tbl=" ".join(" ".join(r) for r in rows); ok(not re.search(r"https?://|@|\b\d{4,}\b", tbl), "no URL, email or 4+ digit number in any row")
    print("[6] links")
    for page,s in (("index.html",idx),("ch01-two-conversations.html",ch)):
        for h in re.findall(r'href="([^"#]+)"', s):
            if h.startswith("http"): continue
            ok((H/h).resolve().exists(), f"{page} -> {h}")
    print("[7] tags")
    for page,s in (("index.html",idx),("ch01-two-conversations.html",ch)):
        p=P(); p.feed(s); ok(not p.st and not p.bad, f"{page} balanced")
    print("\nall blocks hold." if not fails else f"\n{len(fails)} block(s) failed.")
    sys.exit(1 if fails else 0)
main()
