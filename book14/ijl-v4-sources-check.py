#!/usr/bin/env python3
"""IJL v4 pre-submission source check (R24; item 5 of HANDOFF). Reads PDFs from ~/Downloads.
Reports: (1) whether the Atkins & Rundell (2008) quote is in the file named for it,
(2) Jackson 2002 s.8.2 opening question, (3) self-identifying items in ijl_v4_source.md."""
import subprocess, os, re, sys
D = next(p for p in (os.path.expanduser("~/Downloads"), os.path.expanduser("~/mnt/Downloads")) if os.path.isdir(p))
def txt(f, *a):
    return subprocess.run(["pdftotext", *a, os.path.join(D, f), "-"], capture_output=True, text=True).stdout
def pages(f):
    o = subprocess.run(["pdfinfo", os.path.join(D, f)], capture_output=True, text=True).stdout
    return int(re.search(r"Pages:\s+(\d+)", o).group(1))
ok = True
f = "The_Oxford_Guide_to_Practical_Lexicograp.pdf"
n = pages(f); t = " ".join(txt(f).split())
print(f"[1] {f}: {n} pages; review of the book, not the book:", "Downloaded from http://eltj.oxfordjournals.org" in t and "Reviews" in t)
quote = "one of the most demanding tasks in practical lexicography"
print("    quote present:", quote in t, "| 'demanding' hits:", re.findall(r".{25}demanding.{20}", t))
print("    review's own page pointer for regular polysemy:", re.findall(r"regular polysemy \(pp\. [0-9–]+\)", t))
j = "1jackson_howard_lexicography_an_introduction.pdf"
jt = " ".join(txt(j, "-f", "50", "-l", "50").split())
q = "If polysemy is identified, how does a lexicographer decide how many meanings or senses of a word to recognise?"
print("[2] Jackson 2002 s.8.2 (pdf p.50) question verbatim:", q in jt or q in " ".join(txt(j, "-f", "51", "-l", "51").split()), "| heading on pdf p.50:", "8.2 Lumping and splitting" in jt)
s = open(os.path.join(D, "ijl_v4_source.md")).read()
print("[3] identifying items in ijl_v4_source.md:")
print("    'Nogueira Grossi' occurrences:", s.count("Nogueira Grossi"), "| distinct self-cites:", sorted(set(re.findall(r"Nogueira Grossi 20\d\d[ab]?", s))))
print("    'Principia Orthogona' occurrences:", s.count("Principia Orthogona"), "| in Keywords line:", "Principia Orthogona" in [l for l in s.splitlines() if l.startswith("Keywords")][0])
print("    G6 LLC in reference list:", s.count("G6 LLC"), "| github.com/TOTOGT URL:", s.count("github.com/TOTOGT"), "| zenodo DOI:", re.findall(r"10\.5281/zenodo\.\d+", s))
print("    byline placeholder present:", "Author details removed for blind review" in s)
